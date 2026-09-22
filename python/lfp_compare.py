"""Side-by-side saline-week vs psilocybin-week EZM movie for one mouse.

Shared session-fraction time. BL1 triangles are session-mean β wPLI (before maze).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FFMpegWriter

from lfp_bursts import bursts_by_region, load_session_thresholds
from lfp_config import PAIRS, REGIONS
from lfp_io import load_clean
from lfp_pair import pair_weeks
from lfp_video import (
    DEFAULT_FPS,
    PAIR_COH,
    PAIR_WPLI,
    TRACE_WIN_S,
    _ffmpeg_path,
    _read_stem_windows,
    _spans_in,
    _window_at,
    apply_wpli_triangle,
    paint_wpli_triangle,
    triangle_edge_vals,
)
from lfp_windows import window_features

COMPARE_SPEED = 4.0
COLORS = {"BLA": "tab:blue", "vHPC": "tab:orange", "mPFC": "tab:green"}
EDGE_LABELS = {
    ("BLA", "vHPC"): "BLA–vHPC",
    ("BLA", "mPFC"): "BLA–mPFC",
    ("vHPC", "mPFC"): "vHPC–mPFC",
}


@dataclass
class Side:
    drug: str
    label: str
    stem: str
    dur: float
    fs: float
    lfp: dict
    msk: dict
    bursts: dict
    win: pd.DataFrame
    ylims: dict
    hop: int
    t_full: np.ndarray
    bl1_edges: dict
    stats: dict


def _mean_edges(win: pd.DataFrame) -> dict:
    if win is None or win.empty:
        return triangle_edge_vals(None)
    means = win[[c for c in win.columns if c.endswith("_wpli_beta")]].mean()
    return triangle_edge_vals(means)


def _row_for_stem(feat: pd.DataFrame | None, stem: str) -> pd.Series | None:
    if feat is None or feat.empty or "stem" not in feat.columns:
        return None
    hit = feat[feat.stem == stem]
    return None if hit.empty else hit.iloc[0]


def _load_side(
    *,
    drug: str,
    stems: dict,
    derived: Path,
    manifest: pd.DataFrame,
    feat: pd.DataFrame | None,
) -> Side:
    stem = stems["beh"]
    meta = manifest.loc[manifest.stem == stem].iloc[0]
    clean = derived / "clean"
    print(f"  loading {stem} ({drug} {stems['rectype_beh']}) ...", flush=True)
    lfp, msk, fs = load_clean(clean / f"{stem}.npz")
    n = int(next(iter(lfp.values())).shape[-1])
    dur = n / fs
    thr = load_session_thresholds(manifest, stems["session_uid"], clean, load_clean)
    bursts = bursts_by_region(lfp, msk, fs, thr)
    win = _read_stem_windows(derived, stem)
    if win.empty:
        win = window_features(lfp, msk, fs)
    if not win.empty:
        win = win.sort_values("t_start").reset_index(drop=True)
    bl1_win = _read_stem_windows(derived, stems["BL1"])
    bl1_row = _row_for_stem(feat, stems["BL1"])
    beh_row = _row_for_stem(feat, stem)
    if bl1_row is not None:
        bl1_edges = triangle_edge_vals(bl1_row, suffix="_winmean")
    else:
        bl1_edges = _mean_edges(bl1_win)
    ylims = {}
    for r, x in lfp.items():
        lo, hi = np.percentile(x, [1, 99])
        pad = 0.15 * (hi - lo + 1e-9)
        ylims[r] = (lo - pad, hi + pad)
    hop = max(1, int(fs // 250))
    stats = {
        "burst_rate": _num(beh_row, "burst_rate_per_min"),
        "burst_rate_bl1": _num(bl1_row, "burst_rate_per_min"),
    }
    for a, b in PAIRS:
        col = f"{a}-{b}_wpli_beta_winmean"
        stats[f"{a}-{b}_ezm"] = _num(beh_row, col) if beh_row is not None else _mean_edges(win).get((a, b), np.nan)
        stats[f"{a}-{b}_bl1"] = bl1_edges.get((a, b), np.nan)
        stats[f"{a}-{b}_d"] = stats[f"{a}-{b}_ezm"] - stats[f"{a}-{b}_bl1"]
    label = "saline week" if drug == "sal" else "psilocybin week"
    return Side(
        drug=drug, label=label, stem=stem, dur=dur, fs=fs, lfp=lfp, msk=msk,
        bursts=bursts, win=win, ylims=ylims, hop=hop,
        t_full=np.arange(n) / fs, bl1_edges=bl1_edges, stats=stats,
    )


def _num(row: pd.Series | None, col: str) -> float:
    if row is None or col not in row.index or pd.isna(row[col]):
        return float("nan")
    return float(row[col])


def _fmt(x: float, nd: int = 2) -> str:
    return "—" if not np.isfinite(x) else f"{x:.{nd}f}"


def render_compare_video(
    subject_uid: str,
    *,
    derived: Path,
    out: Path,
    manifest: pd.DataFrame,
    feat: pd.DataFrame | None = None,
    speed: float = COMPARE_SPEED,
    fps: float = DEFAULT_FPS,
    dpi: int = 100,
    trace_win_s: float = TRACE_WIN_S,
) -> Path:
    derived = Path(derived)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    pair = pair_weeks(manifest, subject_uid, derived / "clean")
    if pair is None:
        raise SystemExit(
            f"{subject_uid}: need local sal and psi EZM/EPM npz (both weeks)."
        )
    sides = {
        d: _load_side(
            drug=d, stems=pair["weeks"][d], derived=derived,
            manifest=manifest, feat=feat,
        )
        for d in ("sal", "psi")
    }
    max_dur = max(s.dur for s in sides.values())
    n_motion = max(2, int(round(max_dur / speed * fps)))
    n_hold = int(round(3.0 * fps))
    nfr = n_motion + n_hold
    print(
        f"  compare {subject_uid}: {n_motion} motion + {n_hold} end-card frames "
        f"({speed:.0f}×, {fps:.0f} fps)",
        flush=True,
    )

    fig = plt.figure(figsize=(16, 9), dpi=dpi)
    gs = fig.add_gridspec(
        6, 8,
        height_ratios=[0.85, 1.0, 1.0, 1.0, 0.75, 1.05],
        hspace=0.45, wspace=0.45,
        left=0.04, right=0.99, top=0.90, bottom=0.06,
    )
    ax_bl1 = {
        "sal": fig.add_subplot(gs[0, 0:2]),
        "psi": fig.add_subplot(gs[0, 4:6]),
    }
    col0 = {"sal": (0, 3), "psi": (4, 7)}
    artists = {}
    for drug, side in sides.items():
        c0, c1 = col0[drug]
        ax_lfp = [fig.add_subplot(gs[1 + i, c0]) for i in range(3)]
        ax_net = fig.add_subplot(gs[1:4, c0 + 1:c1])
        ax_rast = fig.add_subplot(gs[4, c0:c1])
        ax_coup = fig.add_subplot(gs[5, c0:c1])
        paint_wpli_triangle(ax_bl1[drug], side.bl1_edges, title=f"BL1 {side.label}", fontsize=8)
        lines, spans = [], [[] for _ in REGIONS]
        for i, r in enumerate(REGIONS):
            ax = ax_lfp[i]
            if r not in side.lfp:
                ax.set_visible(False)
                lines.append(None)
                continue
            (ln,) = ax.plot([], [], color="0.15", lw=0.6)
            lines.append(ln)
            ax.set_ylabel(r if drug == "sal" else "", fontweight="bold", fontsize=8)
            ax.set_ylim(*side.ylims[r])
            ax.tick_params(labelsize=7)
        ax_lfp[2].set_xlabel("time (s)", fontsize=8)
        elines, _ = paint_wpli_triangle(ax_net, triangle_edge_vals(None), title="EZM β wPLI")
        for i, r in enumerate(REGIONS):
            if r not in side.bursts:
                continue
            s, e = side.bursts[r]
            if len(s):
                ax_rast.broken_barh(
                    list(zip(s, np.maximum(e - s, 0))),
                    (i - 0.35, 0.7), facecolors=COLORS[r], edgecolors="none", alpha=0.85,
                )
        ax_rast.set_yticks(range(3))
        ax_rast.set_yticklabels(list(REGIONS) if drug == "sal" else [])
        ax_rast.set_xlim(0, side.dur)
        ax_rast.tick_params(labelsize=7)
        rc = ax_rast.axvline(0, color="k", lw=1.0)
        if not side.win.empty and PAIR_WPLI in side.win.columns:
            tc = 0.5 * (side.win.t_start + side.win.t_end)
            ax_coup.plot(tc, side.win[PAIR_WPLI], color="tab:blue", lw=1.2, label="wPLI")
            if PAIR_COH in side.win.columns:
                ax_coup.plot(tc, side.win[PAIR_COH], color="0.45", lw=0.9, ls="--")
        ax_coup.set_ylim(0, 1)
        ax_coup.set_xlim(0, side.dur)
        ax_coup.set_xlabel("time (s)", fontsize=8)
        if drug == "sal":
            ax_coup.set_ylabel("BLA–vHPC β", fontsize=8)
        cc = ax_coup.axvline(0, color="k", lw=1.0)
        ax_coup.tick_params(labelsize=7)
        artists[drug] = {
            "lfp": ax_lfp, "lines": lines, "spans": spans, "net": elines,
            "rast_c": rc, "coup_c": cc, "side": side,
        }

    ax_end = fig.add_subplot(gs[0, 6:8])
    ax_end.axis("off")
    title = fig.suptitle("", fontsize=13, fontweight="bold")

    def update_side(drug: str, frac: float) -> None:
        A = artists[drug]
        side: Side = A["side"]
        t = float(np.clip(frac, 0, 1) * side.dur)
        half = trace_win_s / 2
        t0 = max(0.0, t - half)
        t1 = min(side.dur, t + half)
        if t1 - t0 < trace_win_s and t1 >= side.dur:
            t0 = max(0.0, t1 - trace_win_s)
        i0, i1 = int(t0 * side.fs), int(t1 * side.fs)
        tt = side.t_full[i0:i1:side.hop]
        for i, r in enumerate(REGIONS):
            ln = A["lines"][i]
            ax = A["lfp"][i]
            if ln is None:
                continue
            sl = side.lfp[r][i0:i1:side.hop]
            art = np.asarray(side.msk[r][i0:i1:side.hop], dtype=bool) if r in side.msk else None
            y = np.asarray(sl, dtype=float)
            if art is not None and len(art) == len(y):
                y = y.copy()
                y[art] = np.nan
            ln.set_data(tt[: len(y)], y[: len(tt)])
            ax.set_xlim(t0, t1)
            for p in A["spans"][i]:
                p.remove()
            A["spans"][i].clear()
            if r in side.bursts:
                for s, e in _spans_in(*side.bursts[r], t0, t1):
                    A["spans"][i].append(ax.axvspan(s, e, color=COLORS[r], alpha=0.18, lw=0))
        A["rast_c"].set_xdata([t, t])
        A["coup_c"].set_xdata([t, t])
        apply_wpli_triangle(A["net"], triangle_edge_vals(_window_at(side.win, t)))

    def draw_endcard(visible: bool) -> None:
        ax_end.clear()
        ax_end.axis("off")
        if not visible:
            ax_end.set_title("")
            return
        sal, psi = sides["sal"].stats, sides["psi"].stats
        lines = [
            f"{subject_uid}  (exploratory)",
            "",
            f"{'':18} saline     psi",
            f"burst/min EZM    {_fmt(sal['burst_rate']):>6}  {_fmt(psi['burst_rate']):>6}",
        ]
        for a, b in PAIRS:
            lab = EDGE_LABELS[(a, b)]
            lines.append(
                f"Δ wPLI {lab:9} {_fmt(sal[f'{a}-{b}_d'], 3):>6}  {_fmt(psi[f'{a}-{b}_d'], 3):>6}"
            )
        lines += ["", "Δ = EZM − BL1  (same mouse)"]
        ax_end.text(0.0, 1.0, "\n".join(lines), va="top", ha="left",
                    fontsize=7.5, family="monospace", transform=ax_end.transAxes)

    plt.rcParams["animation.ffmpeg_path"] = _ffmpeg_path()
    writer = FFMpegWriter(
        fps=fps, metadata={"title": f"{subject_uid} sal vs psi"},
        bitrate=4000, extra_args=["-pix_fmt", "yuv420p"],
    )
    with writer.saving(fig, str(out), dpi=dpi):
        for k in range(nfr):
            hold = k >= n_motion
            frac = 1.0 if hold else (k / max(n_motion - 1, 1))
            for drug in ("sal", "psi"):
                update_side(drug, frac)
            draw_endcard(hold)
            t_sal = frac * sides["sal"].dur
            t_psi = frac * sides["psi"].dur
            title.set_text(
                f"{subject_uid}   saline week vs psilocybin week   "
                f"{100 * frac:.0f}%   "
                f"(sal {t_sal:.0f}s / {sides['sal'].dur:.0f}s   "
                f"psi {t_psi:.0f}s / {sides['psi'].dur:.0f}s)"
            )
            writer.grab_frame()
            if k == 0 or (k + 1) % 25 == 0 or k + 1 == nfr:
                print(f"  frame {k + 1}/{nfr}", flush=True)
    plt.close(fig)
    print(f"Wrote {out}", flush=True)
    return out
