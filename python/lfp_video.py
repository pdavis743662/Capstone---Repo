"""Time-locked 3-site LFP dashboard rendered to MP4.

Analog of an HNN laminar movie using BLA / vHPC / mPFC traces, spectrograms,
beta-burst rasters, and 10 s wPLI/coherence. Not a cortical column or scalp map.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FFMpegWriter
from matplotlib.patches import Circle
from scipy import signal

from lfp_bursts import bursts_by_region, load_session_thresholds
from lfp_config import FMAX_SPEC, FMIN_SPEC, NPERSEG_S, PAIRS, REGIONS
from lfp_io import load_clean
from lfp_windows import window_features

TRACE_WIN_S = 4.0
DEFAULT_SPEED = 40.0
DEFAULT_FPS = 20.0
PAIR_WPLI = "BLA-vHPC_wpli_beta"
PAIR_COH = "BLA-vHPC_coh_beta"
_NODE_XY = {"BLA": (0.50, 0.78), "vHPC": (0.18, 0.22), "mPFC": (0.82, 0.22)}
_EDGE_CMAP = plt.cm.viridis


def triangle_edge_vals(row: pd.Series | None, suffix: str = "") -> dict[tuple[str, str], float]:
    """β wPLI per pair from a window row or a ``*_winmean`` feature row."""
    out: dict[tuple[str, str], float] = {}
    for a, b in PAIRS:
        keys = [f"{a}-{b}_wpli_beta{suffix}", f"{a}-{b}_wpli_beta"]
        val = np.nan
        if row is not None:
            for k in keys:
                if k in row.index and pd.notna(row[k]):
                    val = float(row[k])
                    break
        out[(a, b)] = val
    return out


def paint_wpli_triangle(
    ax,
    edge_vals: dict[tuple[str, str], float],
    *,
    title: str = "",
    fontsize: int = 7,
) -> tuple[dict, dict]:
    """Draw a 3-node β wPLI triangle. Returns ``(edge_lines, node_circs)``."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=fontsize + 1)
    edge_lines = {}
    for a, b in PAIRS:
        (el,) = ax.plot(
            [_NODE_XY[a][0], _NODE_XY[b][0]],
            [_NODE_XY[a][1], _NODE_XY[b][1]],
            color="0.6", lw=2, zorder=1, solid_capstyle="round",
        )
        edge_lines[(a, b)] = el
    node_circs = {}
    for r, (x, y) in _NODE_XY.items():
        c = Circle((x, y), 0.08, facecolor="0.85", edgecolor="0.2", lw=1.0, zorder=3)
        ax.add_patch(c)
        node_circs[r] = c
        ax.text(x, y, r, ha="center", va="center", fontsize=fontsize, zorder=4)
    apply_wpli_triangle(edge_lines, edge_vals)
    return edge_lines, node_circs


def apply_wpli_triangle(edge_lines, edge_vals: dict[tuple[str, str], float]) -> None:
    for (a, b), el in edge_lines.items():
        val = edge_vals.get((a, b), np.nan)
        if not np.isfinite(val):
            el.set_color("0.85")
            el.set_linewidth(1.0)
        else:
            el.set_color(_EDGE_CMAP(np.clip(val, 0, 1)))
            el.set_linewidth(1.2 + 8.0 * val)


def _move_vline(ln, t: float) -> None:
    ln.set_xdata([t, t])


def _ffmpeg_path() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as e:  # noqa: BLE001
        raise SystemExit(
            "ffmpeg not found. Install ffmpeg or `pip install imageio-ffmpeg`."
        ) from e


def _read_stem_windows(derived: Path, stem: str) -> pd.DataFrame:
    parquet = derived / "windows.parquet"
    csv_path = derived / "windows.csv"
    win = None
    if parquet.exists():
        win = pd.read_parquet(parquet)
    elif csv_path.exists():
        win = pd.read_csv(csv_path)
    if win is None or win.empty or "stem" not in win.columns:
        return pd.DataFrame()
    return win[win.stem == stem].copy()


def _window_at(win: pd.DataFrame, t: float) -> pd.Series | None:
    if win is None or win.empty:
        return None
    inside = win[(win.t_start <= t) & (t < win.t_end)]
    if not inside.empty:
        return inside.iloc[0]
    mid = 0.5 * (win.t_start + win.t_end)
    return win.loc[(mid - t).abs().idxmin()]


def _spans_in(starts: np.ndarray, ends: np.ndarray, t0: float, t1: float):
    out = []
    for s, e in zip(starts, ends):
        if e < t0 or s > t1:
            continue
        out.append((max(s, t0), min(e, t1)))
    return out


def _spectrogram(x: np.ndarray, fs: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    nper = int(round(NPERSEG_S * fs))
    nper = max(8, min(nper, len(x)))
    f, ts, Sxx = signal.spectrogram(x, fs=fs, nperseg=nper, noverlap=nper // 2)
    band = (f >= FMIN_SPEC) & (f <= FMAX_SPEC)
    db = 10 * np.log10(np.maximum(Sxx[band], 1e-20))
    return ts, f[band], db


def render_session_video(
    stem: str,
    *,
    derived: Path,
    out: Path,
    manifest: pd.DataFrame,
    speed: float = DEFAULT_SPEED,
    fps: float = DEFAULT_FPS,
    dpi: int = 110,
    trace_win_s: float = TRACE_WIN_S,
) -> Path:
    """Write one MP4 for ``stem`` under ``out`` (parent should already exist)."""
    derived = Path(derived)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)

    row = manifest.loc[manifest.stem == stem]
    if row.empty:
        raise SystemExit(f"stem not in manifest: {stem}")
    meta = row.iloc[0]
    clean_dir = derived / "clean"
    print(f"loading {stem} ...", flush=True)
    lfp, msk, fs = load_clean(clean_dir / f"{stem}.npz")
    n = int(next(iter(lfp.values())).shape[-1])
    dur = n / fs
    regions = [r for r in REGIONS if r in lfp]

    thr = load_session_thresholds(manifest, str(meta.session_uid), clean_dir, load_clean)
    mode = "BL1 threshold" if thr is not None else "within-recording threshold"
    bursts = bursts_by_region(lfp, msk, fs, thr)

    win = _read_stem_windows(derived, stem)
    if win.empty:
        print(f"  window table miss; computing 10 s features ...", flush=True)
        win = window_features(lfp, msk, fs)
    if not win.empty:
        win = win.sort_values("t_start").reset_index(drop=True)

    specs = {r: _spectrogram(lfp[r], fs) for r in regions}
    hop = max(1, int(fs // 250))
    t_full = np.arange(n) / fs

    ylims = {}
    for r in regions:
        x = lfp[r]
        lo, hi = np.percentile(x, [1, 99])
        pad = 0.15 * (hi - lo + 1e-9)
        ylims[r] = (lo - pad, hi + pad)

    dt = speed / fps
    times = np.arange(0.0, dur, dt)
    if len(times) == 0 or times[-1] < dur - 1e-9:
        times = np.append(times, dur)
    print(
        f"  {dur:.1f}s LFP → {len(times)} frames ({speed:.0f}×, {fps:.0f} fps, {mode})",
        flush=True,
    )

    fig = plt.figure(figsize=(16, 9), dpi=dpi)
    gs = fig.add_gridspec(
        5, 4,
        height_ratios=[1.0, 1.0, 1.0, 0.85, 1.1],
        width_ratios=[1.35, 1.25, 0.55, 0.55],
        hspace=0.32, wspace=0.32,
        left=0.055, right=0.985, top=0.90, bottom=0.07,
    )
    ax_lfp = [fig.add_subplot(gs[i, 0]) for i in range(3)]
    ax_spec = [fig.add_subplot(gs[0, 1])]
    ax_spec += [fig.add_subplot(gs[i, 1], sharex=ax_spec[0]) for i in range(1, 3)]
    ax_net = fig.add_subplot(gs[0:3, 2:])
    ax_rast = fig.add_subplot(gs[3, :])
    ax_coup = fig.add_subplot(gs[4, :], sharex=ax_rast)

    lfp_lines = []
    lfp_burst_spans: list = []
    for i, r in enumerate(REGIONS):
        ax = ax_lfp[i]
        if r not in lfp:
            ax.set_visible(False)
            lfp_lines.append(None)
            continue
        (ln,) = ax.plot([], [], color="0.15", lw=0.7)
        lfp_lines.append(ln)
        ax.set_ylabel(r, fontweight="bold")
        ax.set_ylim(*ylims[r])
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    ax_lfp[2].set_xlabel("time (s)")
    lfp_burst_spans = [[] for _ in REGIONS]

    spec_cursors = []
    for i, r in enumerate(REGIONS):
        ax = ax_spec[i]
        if r not in specs:
            ax.set_visible(False)
            spec_cursors.append(None)
            continue
        ts, ff, db = specs[r]
        vmax = np.percentile(db, 99)
        vmin = np.percentile(db, 5)
        ax.pcolormesh(ts, ff, db, shading="auto", cmap="magma", vmin=vmin, vmax=vmax)
        ax.set_ylim(FMIN_SPEC, FMAX_SPEC)
        ax.set_ylabel("Hz" if i == 1 else "")
        ax.set_title(r, fontsize=9)
        ln = ax.axvline(0, color="w", lw=1.2, ls="--")
        spec_cursors.append(ln)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    ax_spec[2].set_xlabel("time (s)")
    for ax in ax_spec:
        ax.set_xlim(0, dur)

    ax_net.set_xlim(0, 1)
    ax_net.set_ylim(0, 1)
    ax_net.set_aspect("equal")
    ax_net.axis("off")
    ax_net.set_title("β wPLI", fontsize=10)
    edge_lines = {}
    for a, b in PAIRS:
        (el,) = ax_net.plot(
            [_NODE_XY[a][0], _NODE_XY[b][0]],
            [_NODE_XY[a][1], _NODE_XY[b][1]],
            color="0.6", lw=2, zorder=1, solid_capstyle="round",
        )
        edge_lines[(a, b)] = el
    node_circs = {}
    node_txt = {}
    cmap = plt.cm.viridis
    for r, (x, y) in _NODE_XY.items():
        c = Circle((x, y), 0.08, facecolor="0.85", edgecolor="0.2", lw=1.2, zorder=3)
        ax_net.add_patch(c)
        node_circs[r] = c
        node_txt[r] = ax_net.text(x, y, r, ha="center", va="center", fontsize=8, zorder=4)

    colors = {"BLA": "tab:blue", "vHPC": "tab:orange", "mPFC": "tab:green"}
    for i, r in enumerate(REGIONS):
        if r not in bursts:
            continue
        s, e = bursts[r]
        if len(s):
            ax_rast.broken_barh(
                list(zip(s, np.maximum(e - s, 0))),
                (i - 0.35, 0.7),
                facecolors=colors[r],
                edgecolors="none",
                alpha=0.85,
            )
    ax_rast.set_yticks(range(len(REGIONS)))
    ax_rast.set_yticklabels(list(REGIONS))
    ax_rast.set_ylabel("bursts")
    ax_rast.set_xlim(0, dur)
    ax_rast.spines["top"].set_visible(False)
    ax_rast.spines["right"].set_visible(False)
    rast_cursor = ax_rast.axvline(0, color="k", lw=1.2)

    if not win.empty and PAIR_WPLI in win.columns:
        tc = 0.5 * (win.t_start + win.t_end)
        ax_coup.plot(tc, win[PAIR_WPLI], color="tab:blue", lw=1.5, label="wPLI")
        if PAIR_COH in win.columns:
            ax_coup.plot(tc, win[PAIR_COH], color="0.45", lw=1.1, ls="--", label="coherence")
        ax_coup.legend(fontsize=8, loc="upper right", frameon=False)
    ax_coup.set_ylim(0, 1)
    ax_coup.set_ylabel("BLA–vHPC β")
    ax_coup.set_xlabel("time (s)")
    ax_coup.set_xlim(0, dur)
    ax_coup.spines["top"].set_visible(False)
    ax_coup.spines["right"].set_visible(False)
    coup_cursor = ax_coup.axvline(0, color="k", lw=1.2)

    title = fig.suptitle("", fontsize=13, fontweight="bold")

    def _update_net(wrow: pd.Series | None) -> None:
        for (a, b), el in edge_lines.items():
            col = f"{a}-{b}_wpli_beta"
            val = float(wrow[col]) if wrow is not None and col in wrow.index else np.nan
            if not np.isfinite(val):
                el.set_color("0.85")
                el.set_linewidth(1.0)
            else:
                el.set_color(cmap(np.clip(val, 0, 1)))
                el.set_linewidth(1.2 + 8.0 * val)
        for r, circ in node_circs.items():
            col = f"{r}_abs_beta"
            val = float(wrow[col]) if wrow is not None and col in wrow.index else np.nan
            if not np.isfinite(val) or val <= 0:
                rad = 0.07
            else:
                rad = float(np.clip(0.05 + 0.08 * np.log10(val + 1e-12), 0.05, 0.14))
            circ.set_radius(rad)

    def update(t: float) -> None:
        half = trace_win_s / 2
        t0 = max(0.0, t - half)
        t1 = min(dur, t + half)
        if t1 - t0 < trace_win_s and t1 >= dur:
            t0 = max(0.0, t1 - trace_win_s)
        i0, i1 = int(t0 * fs), int(t1 * fs)
        tt = t_full[i0:i1:hop]
        for i, r in enumerate(REGIONS):
            ax = ax_lfp[i]
            ln = lfp_lines[i]
            if ln is None:
                continue
            sl = lfp[r][i0:i1:hop]
            art = np.asarray(msk[r][i0:i1:hop], dtype=bool) if r in msk else None
            y = np.asarray(sl, dtype=float)
            if art is not None and len(art) == len(y):
                y = y.copy()
                y[art] = np.nan
            ln.set_data(tt[: len(y)], y[: len(tt)])
            ax.set_xlim(t0, t1)
            for p in lfp_burst_spans[i]:
                p.remove()
            lfp_burst_spans[i].clear()
            if r in bursts:
                for s, e in _spans_in(*bursts[r], t0, t1):
                    p = ax.axvspan(s, e, color=colors[r], alpha=0.18, lw=0)
                    lfp_burst_spans[i].append(p)
        for ln in spec_cursors:
            if ln is not None:
                _move_vline(ln, t)
        _move_vline(rast_cursor, t)
        _move_vline(coup_cursor, t)
        _update_net(_window_at(win, t))
        title.set_text(
            f"{stem}   {meta.drug} {meta.rectype}   T = {t:7.2f} s / {dur:.1f} s"
        )

    plt.rcParams["animation.ffmpeg_path"] = _ffmpeg_path()
    writer = FFMpegWriter(
        fps=fps,
        metadata={"artist": "Capstone LFP", "title": stem},
        bitrate=3600,
        extra_args=["-pix_fmt", "yuv420p"],
    )
    nfr = len(times)
    with writer.saving(fig, str(out), dpi=dpi):
        for k, t in enumerate(times):
            update(float(t))
            writer.grab_frame()
            if k == 0 or (k + 1) % 25 == 0 or k + 1 == nfr:
                print(f"  frame {k + 1}/{nfr}", flush=True)
    plt.close(fig)
    print(f"Wrote {out}", flush=True)
    return out
