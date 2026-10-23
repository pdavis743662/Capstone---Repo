"""Multi-band saline vs psilocybin EZM movie from the 10 s window table.

No raw LFP. Shared session-fraction time. Power default is abs / that week's
BL1 mean so delta and high-gamma share an axis (1.0 = home cage).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FFMpegWriter

from lfp_config import (
    BAND_COLORS,
    BAND_COMPARE_END_S,
    BAND_COMPARE_FOCUS,
    BAND_COMPARE_FRAC_GRID,
    BAND_COMPARE_PAIR,
    BAND_COMPARE_POWER,
    BAND_COMPARE_REGIONS,
    BAND_COMPARE_SPEED,
    BANDS,
)
from lfp_pair import paired_uids_in_windows, pair_weeks_in_windows
from lfp_video import DEFAULT_FPS, _ffmpeg_path, _read_stem_windows, _window_at

POWER_MODES = ("bl1", "raw", "rel")
# Display names for column headers. Drug token in the data is still "sal" / "psi".
DRUG_LABEL = {"sal": "saline week", "psi": "psilocybin week"}


def _band_names() -> tuple[str, ...]:
    """Band keys in BANDS order (delta, theta, beta, lgamma, hgamma)."""
    return tuple(BANDS.keys())


def stem_duration(win: pd.DataFrame) -> float:
    """Session length from the last kept window's t_end (not raw LFP)."""
    if win is None or win.empty or "t_end" not in win.columns:
        return float("nan")
    return float(np.nanmax(win.t_end.to_numpy()))


def power_col(region: str, band: str, mode: str) -> str:
    """windows.csv column: {region}_rel_{band} or {region}_abs_{band}."""
    if mode == "rel":
        return f"{region}_rel_{band}"
    return f"{region}_abs_{band}"


def wpli_col(band: str, pair: str = BAND_COMPARE_PAIR) -> str:
    """windows.csv column: {pair}_wpli_{band}, default BLA-vHPC."""
    return f"{pair}_wpli_{band}"


def bl1_means(bl1: pd.DataFrame, *, mode: str) -> dict[str, float]:
    """Region×band BL1 session means (abs or rel columns)."""
    out: dict[str, float] = {}
    if bl1 is None or bl1.empty:
        return out
    for region in BAND_COMPARE_REGIONS:
        for band in _band_names():
            col = power_col(region, band, mode)
            key = f"{region}_{band}"
            if col in bl1.columns:
                out[key] = float(np.nanmean(bl1[col].to_numpy(dtype=float)))
            else:
                out[key] = float("nan")
    return out


def window_power(
    win: pd.DataFrame,
    band: str,
    region: str,
    *,
    mode: str,
    means: dict[str, float],
) -> np.ndarray:
    col = power_col(region, band, "rel" if mode == "rel" else "raw")
    if win is None or win.empty or col not in win.columns:
        n = 0 if win is None or win.empty else len(win)
        return np.full(n, np.nan)
    y = win[col].to_numpy(dtype=float)
    if mode != "bl1":
        return y
    # Divide each window by that week's BL1 session mean so 1.0 = home cage.
    den = means.get(f"{region}_{band}", float("nan"))
    if not np.isfinite(den) or den == 0:
        return np.full_like(y, np.nan)
    return y / den


def window_wpli(win: pd.DataFrame, band: str) -> np.ndarray:
    col = wpli_col(band)
    if win is None or win.empty or col not in win.columns:
        n = 0 if win is None or win.empty else len(win)
        return np.full(n, np.nan)
    return win[col].to_numpy(dtype=float)


def frac_times(win: pd.DataFrame, dur: float) -> np.ndarray:
    """Window midpoints as a fraction of session length (0 at start, 1 at end)."""
    if win is None or win.empty or not np.isfinite(dur) or dur <= 0:
        return np.array([])
    mid = 0.5 * (win.t_start.to_numpy(dtype=float) + win.t_end.to_numpy(dtype=float))
    return np.clip(mid / dur, 0.0, 1.0)


def resample_to_grid(
    frac: np.ndarray,
    y: np.ndarray,
    grid: np.ndarray,
) -> np.ndarray:
    """Linear interpolate a per-window series onto a shared 0–1 fraction grid."""
    out = np.full(grid.shape, np.nan, dtype=float)
    if frac is None or y is None or len(frac) < 2:
        return out
    m = np.isfinite(frac) & np.isfinite(y)
    if m.sum() < 2:
        return out
    order = np.argsort(frac[m])
    xf, yf = frac[m][order], y[m][order]
    uniq = np.concatenate([[True], np.diff(xf) > 1e-12])
    xf, yf = xf[uniq], yf[uniq]
    if len(xf) < 2:
        return out
    inside = (grid >= xf[0]) & (grid <= xf[-1])
    out[inside] = np.interp(grid[inside], xf, yf)
    return out


def ezm_means(
    win: pd.DataFrame,
    *,
    mode: str,
    means: dict[str, float],
) -> dict[str, dict[str, float]]:
    """Per-band EZM means for BLA power, vHPC power, and BLA–vHPC wPLI."""
    out = {"BLA": {}, "vHPC": {}, "wpli": {}}
    for band in _band_names():
        out["BLA"][band] = float(np.nanmean(window_power(win, band, "BLA", mode=mode, means=means)))
        out["vHPC"][band] = float(np.nanmean(window_power(win, band, "vHPC", mode=mode, means=means)))
        out["wpli"][band] = float(np.nanmean(window_wpli(win, band)))
    return out


@dataclass
class BandSide:
    """One drug week's window table plus BL1 means, already aligned to session fraction."""
    drug: str
    label: str
    stem: str
    dur: float
    win: pd.DataFrame
    means: dict[str, float]
    frac: np.ndarray
    stats: dict[str, dict[str, float]] = field(default_factory=dict)


def _load_side(
    *,
    drug: str,
    stems: dict,
    derived: Path,
    mode: str,
) -> BandSide:
    """Pull maze and BL1 rows from windows.csv. No npz load."""
    win = _read_stem_windows(derived, stems["beh"])
    if win.empty:
        raise SystemExit(f"{stems['beh']}: no rows in windows.csv")
    win = win.sort_values("t_start").reset_index(drop=True)
    bl1 = _read_stem_windows(derived, stems["BL1"])
    means = bl1_means(bl1, mode="rel" if mode == "rel" else "raw")
    dur = stem_duration(win)
    frac = frac_times(win, dur)
    return BandSide(
        drug=drug,
        label=DRUG_LABEL[drug],
        stem=stems["beh"],
        dur=dur,
        win=win,
        means=means,
        frac=frac,
        stats=ezm_means(win, mode=mode, means=means),
    )


def _fmt(x: float, nd: int = 2) -> str:
    return "-" if not np.isfinite(x) else f"{x:.{nd}f}"


def _live_text(values: dict[str, float]) -> str:
    """One-line per-band readout drawn on the optional movie, not the PDF."""
    parts = []
    for band in _band_names():
        short = {"delta": "δ", "theta": "θ", "beta": "β", "lgamma": "lγ", "hgamma": "hγ"}[band]
        parts.append(f"{short} {_fmt(values.get(band, float('nan')))}")
    return "  ".join(parts)


def _panel_ylims(
    sides: dict[str, BandSide],
    *,
    mode: str,
) -> dict[str, tuple[float, float]]:
    """Shared y limits across saline and psi columns so the two weeks are comparable."""
    ylims: dict[str, tuple[float, float]] = {}
    for row_key, kind in (("BLA", "power"), ("vHPC", "power"), ("wpli", "wpli")):
        if kind == "wpli":
            ylims[row_key] = (0.0, 1.0)
            continue
        if mode == "rel":
            ylims[row_key] = (0.0, 1.0)
            continue
        ys = []
        for side in sides.values():
            for band in _band_names():
                ys.append(window_power(side.win, band, row_key, mode=mode, means=side.means))
        cat = np.concatenate([y for y in ys if len(y)]) if ys else np.array([0.0, 1.0])
        finite = cat[np.isfinite(cat)]
        if mode == "raw":
            pos = finite[finite > 0]
            if len(pos) < 4:
                ylims[row_key] = (1.0, 10.0)
            else:
                lo, hi = np.percentile(pos, [2, 98])
                ylims[row_key] = (max(lo * 0.5, pos.min() * 0.5), hi * 1.4)
        else:
            if len(finite) < 4:
                ylims[row_key] = (0.0, 2.5)
            else:
                lo, hi = np.percentile(finite, [2, 98])
                ylims[row_key] = (min(0.0, lo - 0.1), max(2.0, hi * 1.15))
    return ylims


GROUP_FOOTER = (
    "C1/C2 group FDR (n=11-12 mice; not this animal): BLA beta bursts down, "
    "BLA beta/BL1 down, vHPC theta/BL1 up, BLA-vHPC beta wPLI n.s."
)


def _load_windows_table(derived: Path) -> pd.DataFrame:
    """Prefer parquet; fall back to the CSV checked into derived/."""
    derived = Path(derived)
    parquet = derived / "windows.parquet"
    csv_path = derived / "windows.csv"
    if parquet.exists():
        return pd.read_parquet(parquet)
    if csv_path.exists():
        return pd.read_csv(csv_path)
    raise SystemExit(f"No window table at {csv_path}")


def _pair_sides(
    subject_uid: str,
    *,
    derived: Path,
    manifest: pd.DataFrame,
    mode: str,
) -> dict[str, BandSide]:
    """Load sal and psi BandSide objects, or exit if either week is missing."""
    all_win = _load_windows_table(derived)
    pair = pair_weeks_in_windows(manifest, subject_uid, all_win, require_bl1=True)
    if pair is None:
        raise SystemExit(
            f"{subject_uid}: need sal and psi EZM/EPM + BL1 stems in windows.csv."
        )
    return {
        d: _load_side(drug=d, stems=pair["weeks"][d], derived=derived, mode=mode)
        for d in ("sal", "psi")
    }


def _row_ylabels(mode: str) -> list[tuple[str, str, str]]:
    """(panel key, kind, y-axis label) for the three rows of F12."""
    if mode == "bl1":
        bla, vh = "BLA power / BL1", "vHPC power / BL1"
    elif mode == "rel":
        bla, vh = "BLA relative power", "vHPC relative power"
    else:
        bla, vh = "BLA abs power", "vHPC abs power"
    return [
        ("BLA", "power", bla),
        ("vHPC", "power", vh),
        ("wpli", "wpli", "BLA–vHPC wPLI"),
    ]


def _band_style(panel: str, band: str) -> dict:
    """Thick if this band is the confirmatory focus for that panel."""
    focus = BAND_COMPARE_FOCUS.get(panel)
    if band == focus:
        return {"lw": 2.35, "alpha": 1.0, "zorder": 3}
    return {"lw": 0.95, "alpha": 0.38, "zorder": 2}


def _feat_num(feat: pd.DataFrame | None, stem: str, col: str) -> float:
    """Session-level value from features_dynamic.csv (used for burst rate)."""
    if feat is None or feat.empty or "stem" not in feat.columns or col not in feat.columns:
        return float("nan")
    hit = feat[feat.stem.astype(str) == str(stem)]
    if hit.empty or pd.isna(hit.iloc[0][col]):
        return float("nan")
    return float(hit.iloc[0][col])


def _rel_mean(win: pd.DataFrame, region: str, band: str) -> float:
    """Mean relative power across kept EZM windows (share of 1-100 Hz)."""
    col = power_col(region, band, "rel")
    if win is None or win.empty or col not in win.columns:
        return float("nan")
    return float(np.nanmean(win[col].to_numpy(dtype=float)))


def _wpli_var(win: pd.DataFrame, band: str) -> float:
    """Sample variance of 10 s wPLI (Kirkby-style, but for any band)."""
    y = window_wpli(win, band)
    y = y[np.isfinite(y)]
    if len(y) < 2:
        return float("nan")
    return float(np.var(y, ddof=1))


def mouse_focus_stats(
    sides: dict[str, BandSide],
    feat: pd.DataFrame | None = None,
) -> dict[str, dict[str, float]]:
    """This-mouse numbers for the stats strip (not a hypothesis test)."""
    out: dict[str, dict[str, float]] = {}
    for drug, side in sides.items():
        out[drug] = {
            "burst": _feat_num(feat, side.stem, "burst_rate_per_min"),
            "BLA_beta": side.stats["BLA"]["beta"],
            "vHPC_theta": side.stats["vHPC"]["theta"],
            "BLA_rel_beta": _rel_mean(side.win, "BLA", "beta"),
            "vHPC_rel_theta": _rel_mean(side.win, "vHPC", "theta"),
            "wpli_beta": side.stats["wpli"]["beta"],
            "wpli_theta": side.stats["wpli"]["theta"],
            "wpli_beta_var": _wpli_var(side.win, "beta"),
            "wpli_theta_var": _wpli_var(side.win, "theta"),
        }
    return out


def _apply_ylim(ax, key: str, kind: str, mode: str, ylims: dict) -> None:
    """wPLI and relative power stay 0-1. Raw abs uses log. BL1 mode draws y=1."""
    if kind == "wpli" or mode == "rel":
        ax.set_ylim(*ylims[key if kind == "power" else "wpli"])
        return
    if mode == "raw":
        ax.set_yscale("log")
        ax.set_ylim(*ylims[key])
        return
    ax.set_ylim(*ylims[key])
    ax.axhline(1.0, color="0.55", lw=0.8, ls="--")


def _draw_pair_panels(
    fig,
    gs,
    sides: dict[str, BandSide],
    *,
    mode: str,
    ylims: dict,
    nrows: int = 3,
) -> dict:
    """2×3 traces; focus bands thick. ``gs`` is nrows × 2 (stats row not included)."""
    row_meta = _row_ylabels(mode)
    axes: dict = {}
    for col, drug in enumerate(("sal", "psi")):
        side = sides[drug]
        axes[drug] = []
        for r, (key, kind, ylab) in enumerate(row_meta):
            ax = fig.add_subplot(gs[r, col])
            focus = BAND_COMPARE_FOCUS[key]
            for band in _band_names():
                y = (
                    window_wpli(side.win, band)
                    if kind == "wpli"
                    else window_power(side.win, band, key, mode=mode, means=side.means)
                )
                sty = _band_style(key, band)
                ax.plot(
                    side.frac, y, color=BAND_COLORS[band],
                    label=band if col == 0 and r == 0 else None,
                    **sty,
                )
            ax.set_xlim(0, 1)
            _apply_ylim(ax, key, kind, mode, ylims)
            ax.set_ylabel(ylab if col == 0 else "", fontsize=8)
            ax.set_title(side.label if r == 0 else "", fontsize=10, fontweight="bold")
            if r == nrows - 1:
                ax.set_xlabel("session fraction", fontsize=8)
            else:
                ax.set_xticklabels([])
            ax.tick_params(labelsize=7)
            ax.text(
                0.99, 0.96, focus,
                transform=ax.transAxes, ha="right", va="top",
                fontsize=7, color=BAND_COLORS[focus], fontweight="bold", alpha=0.9,
            )
            axes[drug].append(ax)
    return axes


def _stats_strip_text(
    subject_uid: str,
    focus: dict[str, dict[str, float]],
) -> str:
    """Monospace table for the bottom of F12. Deltas are this mouse, not FDR."""
    sal, psi = focus["sal"], focus["psi"]

    def dlt(key: str) -> float:
        return psi[key] - sal[key]

    lines = [
        f"{subject_uid}  this mouse only (not a p-value)",
        "",
        f"{'':22} {'saline':>8} {'psi':>8} {'Δ psi−sal':>10}",
        f"{'BLA β bursts / min':22} {_fmt(sal['burst']):>8} {_fmt(psi['burst']):>8} {_fmt(dlt('burst')):>10}",
        f"{'BLA β / BL1':22} {_fmt(sal['BLA_beta']):>8} {_fmt(psi['BLA_beta']):>8} {_fmt(dlt('BLA_beta')):>10}",
        f"{'vHPC θ / BL1':22} {_fmt(sal['vHPC_theta']):>8} {_fmt(psi['vHPC_theta']):>8} {_fmt(dlt('vHPC_theta')):>10}",
        f"{'BLA rel β':22} {_fmt(sal['BLA_rel_beta'], 3):>8} {_fmt(psi['BLA_rel_beta'], 3):>8} {_fmt(dlt('BLA_rel_beta'), 3):>10}",
        f"{'vHPC rel θ':22} {_fmt(sal['vHPC_rel_theta'], 3):>8} {_fmt(psi['vHPC_rel_theta'], 3):>8} {_fmt(dlt('vHPC_rel_theta'), 3):>10}",
        f"{'wPLI β mean':22} {_fmt(sal['wpli_beta'], 3):>8} {_fmt(psi['wpli_beta'], 3):>8} {_fmt(dlt('wpli_beta'), 3):>10}",
        f"{'wPLI θ mean':22} {_fmt(sal['wpli_theta'], 3):>8} {_fmt(psi['wpli_theta'], 3):>8} {_fmt(dlt('wpli_theta'), 3):>10}",
        f"{'wPLI β var':22} {_fmt(sal['wpli_beta_var'], 3):>8} {_fmt(psi['wpli_beta_var'], 3):>8} {_fmt(dlt('wpli_beta_var'), 3):>10}",
        f"{'wPLI θ var':22} {_fmt(sal['wpli_theta_var'], 3):>8} {_fmt(psi['wpli_theta_var'], 3):>8} {_fmt(dlt('wpli_theta_var'), 3):>10}",
        "",
        "Thick lines = BLA beta, vHPC theta, BLA-vHPC beta wPLI.  Delta is this animal, not the FDR test.",
        "wPLI is the FC measure (not MSC).  1.0 on power = that week's BL1.",
        GROUP_FOOTER,
    ]
    return "\n".join(lines)


def render_band_compare_figure(
    subject_uid: str,
    *,
    derived: Path,
    out: Path,
    manifest: pd.DataFrame,
    feat: pd.DataFrame | None = None,
    power: str = BAND_COMPARE_POWER,
    dpi: int = 150,
) -> Path:
    """Per-mouse static 2×3 band compare (PDF/PNG)."""
    mode = power if power in POWER_MODES else BAND_COMPARE_POWER
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    sides = _pair_sides(subject_uid, derived=Path(derived), manifest=manifest, mode=mode)
    ylims = _panel_ylims(sides, mode=mode)
    focus = mouse_focus_stats(sides, feat)

    fig = plt.figure(figsize=(11.8, 9.8), dpi=dpi)
    gs = fig.add_gridspec(
        4, 2,
        height_ratios=[1.05, 1.05, 1.05, 1.35],
        hspace=0.38, wspace=0.26,
        left=0.08, right=0.98, top=0.86, bottom=0.03,
    )
    axes = _draw_pair_panels(fig, gs, sides, mode=mode, ylims=ylims)
    handles, labels = axes["sal"][0].get_legend_handles_labels()
    fig.legend(
        handles, labels, loc="upper center", ncol=5, frameon=False,
        fontsize=8, bbox_to_anchor=(0.54, 0.935),
    )
    ax_txt = fig.add_subplot(gs[3, :])
    ax_txt.axis("off")
    ax_txt.text(
        0.0, 1.0, _stats_strip_text(subject_uid, focus),
        va="top", ha="left", fontsize=7.4, family="monospace",
        transform=ax_txt.transAxes,
    )
    fig.suptitle(
        f"{subject_uid}  —  saline week vs psilocybin week  (10 s windows)",
        fontsize=13, fontweight="bold", y=0.98,
    )
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print(f"Wrote {out}", flush=True)
    return out


def render_band_compare_video(
    subject_uid: str,
    *,
    derived: Path,
    out: Path,
    manifest: pd.DataFrame,
    speed: float = BAND_COMPARE_SPEED,
    fps: float = DEFAULT_FPS,
    power: str = BAND_COMPARE_POWER,
    dpi: int = 100,
) -> Path:
    """Write ``figures_video/<uid>/band_compare_sal_vs_psi.mp4``."""
    mode = power if power in POWER_MODES else BAND_COMPARE_POWER
    derived = Path(derived)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)

    sides = _pair_sides(subject_uid, derived=derived, manifest=manifest, mode=mode)
    ylims = _panel_ylims(sides, mode=mode)
    max_dur = max(s.dur for s in sides.values())
    n_motion = max(2, int(round(max_dur / speed * fps)))
    n_hold = max(1, int(round(BAND_COMPARE_END_S * fps)))
    nfr = n_motion + n_hold
    print(
        f"  band-compare {subject_uid}: {n_motion} motion + {n_hold} end-card frames "
        f"({speed:.0f}×, {fps:.0f} fps, power={mode})",
        flush=True,
    )

    fig = plt.figure(figsize=(14.2, 8.6), dpi=dpi)
    gs = fig.add_gridspec(
        4, 2,
        height_ratios=[1.0, 1.0, 1.0, 0.72],
        hspace=0.38, wspace=0.28,
        left=0.07, right=0.98, top=0.90, bottom=0.05,
    )
    row_meta = [
        ("BLA", "power", "BLA power / BL1" if mode == "bl1"
         else ("BLA relative power" if mode == "rel" else "BLA abs power")),
        ("vHPC", "power", "vHPC power / BL1" if mode == "bl1"
         else ("vHPC relative power" if mode == "rel" else "vHPC abs power")),
        ("wpli", "wpli", "BLA–vHPC wPLI"),
    ]
    artists: dict = {}
    for col, drug in enumerate(("sal", "psi")):
        side = sides[drug]
        axes = []
        vlines = []
        live = []
        for r, (key, kind, ylab) in enumerate(row_meta):
            ax = fig.add_subplot(gs[r, col])
            for band in _band_names():
                if kind == "wpli":
                    y = window_wpli(side.win, band)
                else:
                    y = window_power(side.win, band, key, mode=mode, means=side.means)
                ax.plot(
                    side.frac, y, color=BAND_COLORS[band], lw=1.35,
                    label=band if col == 0 and r == 0 else None,
                )
            ax.set_xlim(0, 1)
            if kind == "wpli" or mode == "rel":
                ax.set_ylim(*ylims[key if kind == "power" else "wpli"])
            elif mode == "raw":
                ax.set_yscale("log")
                ax.set_ylim(*ylims[key])
            else:
                ax.set_ylim(*ylims[key])
                ax.axhline(1.0, color="0.55", lw=0.8, ls="--")
            ax.set_ylabel(ylab if col == 0 else "", fontsize=8)
            ax.set_title(side.label if r == 0 else "", fontsize=10, fontweight="bold")
            if r == 2:
                ax.set_xlabel("session fraction", fontsize=8)
            else:
                ax.set_xticklabels([])
            ax.tick_params(labelsize=7)
            vl = ax.axvline(0.0, color="k", lw=1.1)
            txt = ax.text(
                0.99, 0.97, "", transform=ax.transAxes,
                ha="right", va="top", fontsize=6.5, family="monospace",
            )
            axes.append(ax)
            vlines.append(vl)
            live.append(txt)
        artists[drug] = {"axes": axes, "vlines": vlines, "live": live, "side": side}

    artists["sal"]["axes"][0].legend(
        loc="upper left", fontsize=7, ncol=5, frameon=False, bbox_to_anchor=(0.0, 1.28),
    )
    ax_end = fig.add_subplot(gs[3, :])
    ax_end.axis("off")
    title = fig.suptitle("", fontsize=13, fontweight="bold")

    def current_vals(side: BandSide, t: float) -> tuple[dict, dict, dict]:
        """Band values at the window covering clock time t (movie playhead)."""
        row = _window_at(side.win, t)
        bla, vh, wp = {}, {}, {}
        for band in _band_names():
            if row is None:
                bla[band] = vh[band] = wp[band] = float("nan")
                continue
            tmp = pd.DataFrame([row])
            bla[band] = float(window_power(tmp, band, "BLA", mode=mode, means=side.means)[0])
            vh[band] = float(window_power(tmp, band, "vHPC", mode=mode, means=side.means)[0])
            wp[band] = float(window_wpli(tmp, band)[0])
        return bla, vh, wp

    def draw_endcard(visible: bool) -> None:
        ax_end.clear()
        ax_end.axis("off")
        if not visible:
            ax_end.set_title("")
            return
        sal, psi = sides["sal"].stats, sides["psi"].stats
        hdr = f"{'band':8}  {'BLA/BL1':>16}  {'vHPC/BL1':>16}  {'BLA–vHPC wPLI':>22}"
        sub = f"{'':8}  {'sal':>7} {'psi':>7}  {'sal':>7} {'psi':>7}  {'sal':>6} {'psi':>6} {'Δ':>6}"
        lines = [
            f"{subject_uid}  EZM mean  (one mouse; not a group result)",
            "",
            hdr,
            sub,
        ]
        for band in _band_names():
            ds = sal["BLA"][band]
            dp = psi["BLA"][band]
            vs = sal["vHPC"][band]
            vp = psi["vHPC"][band]
            ws = sal["wpli"][band]
            wp = psi["wpli"][band]
            lines.append(
                f"{band:8}  {_fmt(ds):>7} {_fmt(dp):>7}  "
                f"{_fmt(vs):>7} {_fmt(vp):>7}  "
                f"{_fmt(ws, 3):>6} {_fmt(wp, 3):>6} {_fmt(wp - ws, 3):>6}"
            )
        lines.append("")
        lines.append("Δ = psi − sal  (same mouse).  wPLI is the FC measure, not MSC.")
        ax_end.text(
            0.0, 1.0, "\n".join(lines), va="top", ha="left",
            fontsize=7.5, family="monospace", transform=ax_end.transAxes,
        )

    plt.rcParams["animation.ffmpeg_path"] = _ffmpeg_path()
    writer = FFMpegWriter(
        fps=fps, metadata={"title": f"{subject_uid} band compare sal vs psi"},
        bitrate=4000, extra_args=["-pix_fmt", "yuv420p"],
    )
    with writer.saving(fig, str(out), dpi=dpi):
        for k in range(nfr):
            hold = k >= n_motion
            frac = 1.0 if hold else (k / max(n_motion - 1, 1))
            for drug in ("sal", "psi"):
                side: BandSide = artists[drug]["side"]
                t = float(np.clip(frac, 0, 1) * side.dur)
                bla, vh, wp = current_vals(side, t)
                for vl in artists[drug]["vlines"]:
                    vl.set_xdata([frac, frac])
                artists[drug]["live"][0].set_text(_live_text(bla))
                artists[drug]["live"][1].set_text(_live_text(vh))
                artists[drug]["live"][2].set_text(_live_text(wp))
            draw_endcard(hold)
            title.set_text(
                f"{subject_uid}   saline week vs psilocybin week   "
                f"{100 * frac:.0f}%   "
                f"(sal {frac * sides['sal'].dur:.0f}s / {sides['sal'].dur:.0f}s   "
                f"psi {frac * sides['psi'].dur:.0f}s / {sides['psi'].dur:.0f}s)"
            )
            writer.grab_frame()
            if k == 0 or (k + 1) % 25 == 0 or k + 1 == nfr:
                print(f"  frame {k + 1}/{nfr}", flush=True)
    plt.close(fig)
    print(f"Wrote {out}", flush=True)
    return out


def group_band_grid(
    windows: pd.DataFrame,
    manifest: pd.DataFrame,
    *,
    mode: str = BAND_COMPARE_POWER,
    n_grid: int = BAND_COMPARE_FRAC_GRID,
) -> dict[str, dict[str, dict[str, np.ndarray]]]:
    """Resample each C1/C2 paired mouse onto a shared fraction grid.

    Returns ``out[panel][band][drug]`` as array ``(n_mice, n_grid)``.
    Panels: ``BLA``, ``vHPC``, ``wpli``. Used by F11; one mouse = one row.
    """
    grid = np.linspace(0.0, 1.0, int(n_grid))
    uids = paired_uids_in_windows(manifest, windows, require_bl1=True)
    panels = ("BLA", "vHPC", "wpli")
    store = {
        p: {b: {"sal": [], "psi": []} for b in _band_names()}
        for p in panels
    }
    for uid in uids:
        pair = pair_weeks_in_windows(manifest, uid, windows, require_bl1=True)
        if pair is None:
            continue
        for drug in ("sal", "psi"):
            stems = pair["weeks"][drug]
            beh = windows[windows.stem.astype(str) == str(stems["beh"])].sort_values("t_start")
            bl1 = windows[windows.stem.astype(str) == str(stems["BL1"])]
            if beh.empty:
                continue
            means = bl1_means(bl1, mode="rel" if mode == "rel" else "raw")
            dur = stem_duration(beh)
            frac = frac_times(beh, dur)
            for band in _band_names():
                store["BLA"][band][drug].append(
                    resample_to_grid(frac, window_power(beh, band, "BLA", mode=mode, means=means), grid)
                )
                store["vHPC"][band][drug].append(
                    resample_to_grid(frac, window_power(beh, band, "vHPC", mode=mode, means=means), grid)
                )
                store["wpli"][band][drug].append(
                    resample_to_grid(frac, window_wpli(beh, band), grid)
                )
    out: dict = {}
    for p in panels:
        out[p] = {}
        for band in _band_names():
            out[p][band] = {}
            for drug in ("sal", "psi"):
                rows = store[p][band][drug]
                out[p][band][drug] = (
                    np.vstack(rows) if rows else np.empty((0, len(grid)))
                )
    return out
