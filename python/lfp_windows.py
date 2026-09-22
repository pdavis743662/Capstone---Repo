"""Time-resolved power, coherence, and wPLI in sliding windows.

Named ``lfp_windows`` so it does not collide with ``scipy.signal.windows``.

Each window is scored independently (no concatenating good samples across the
session). Windows whose union artifact fraction exceeds ``MAX_ARTIFACT_FRAC``
are dropped so they do not enter session mean/variance.
"""

from __future__ import annotations

from collections.abc import Mapping

import numpy as np
import pandas as pd
from scipy import signal

from lfp_config import (
    BANDS,
    FMAX_SPEC,
    FMIN_SPEC,
    HOP_S,
    MAX_ARTIFACT_FRAC,
    NPERSEG_S,
    PAIRS,
    WIN_S,
)

_trapz = getattr(np, "trapezoid", None) or np.trapz


def _nperseg(fs: float, n: int) -> int:
    nper = int(round(NPERSEG_S * fs))
    return max(8, min(nper, n))


def band_powers(f: np.ndarray, p: np.ndarray, prefix: str = "") -> dict[str, float]:
    """Absolute and relative band power from a PSD, 1–100 Hz total."""
    tot_m = (f >= FMIN_SPEC) & (f <= FMAX_SPEC)
    total = float(_trapz(p[tot_m], f[tot_m])) if tot_m.any() else 0.0
    out: dict[str, float] = {}
    for name, (lo, hi) in BANDS.items():
        m = (f >= lo) & (f < hi)
        val = float(_trapz(p[m], f[m])) if m.any() else float("nan")
        out[f"{prefix}abs_{name}"] = val
        out[f"{prefix}rel_{name}"] = val / total if total > 0 else float("nan")
    out[f"{prefix}total_1_100"] = total
    return out


def segment_csd(
    x: np.ndarray,
    y: np.ndarray,
    fs: float,
    nperseg: int,
    noverlap: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Per-segment cross-spectral density: ``(freqs, array[n_seg, n_freq])``."""
    nperseg = int(nperseg)
    noverlap = nperseg // 2 if noverlap is None else int(noverlap)
    step = nperseg - noverlap
    n = (len(x) - noverlap) // step
    if n < 2:
        f = np.fft.rfftfreq(nperseg, 1 / fs)
        return f, np.zeros((1, len(f)), complex)
    hann = np.hanning(nperseg)
    idx = np.arange(nperseg)[None, :] + step * np.arange(n)[:, None]
    X = np.fft.rfft(x[idx] * hann, axis=1)
    Y = np.fft.rfft(y[idx] * hann, axis=1)
    return np.fft.rfftfreq(nperseg, 1 / fs), X * np.conj(Y)


def window_connectivity(
    x: np.ndarray,
    y: np.ndarray,
    fs: float,
    tag: str,
    nperseg: int | None = None,
) -> dict[str, float]:
    """Band-averaged magnitude-squared coherence and wPLI for one window."""
    nper = _nperseg(fs, min(len(x), len(y))) if nperseg is None else int(nperseg)
    f, cxy = signal.coherence(x, y, fs=fs, nperseg=nper, noverlap=nper // 2)
    fz, pxy = segment_csd(x, y, fs, nper)
    im = np.imag(pxy)
    den = np.mean(np.abs(im), axis=0)
    num = np.abs(np.mean(im, axis=0))
    wpli = np.divide(num, den, out=np.full_like(num, np.nan), where=den > 0)
    out: dict[str, float] = {}
    for name, (lo, hi) in BANDS.items():
        m = (f >= lo) & (f < hi)
        out[f"{tag}_coh_{name}"] = float(np.nanmean(cxy[m])) if m.any() else float("nan")
        mz = (fz >= lo) & (fz < hi)
        out[f"{tag}_wpli_{name}"] = float(np.nanmean(wpli[mz])) if mz.any() else float("nan")
    return out


def union_artifact_mask(
    msk: Mapping[str, np.ndarray],
    n: int,
) -> np.ndarray:
    """True where any region's artifact mask is True."""
    out = np.zeros(n, dtype=bool)
    for v in msk.values():
        if len(v) == n:
            out |= np.asarray(v, dtype=bool)
    return out


def window_features(
    lfp: Mapping[str, np.ndarray],
    msk: Mapping[str, np.ndarray],
    fs: float,
    *,
    win_s: float = WIN_S,
    hop_s: float = HOP_S,
    max_artifact_frac: float = MAX_ARTIFACT_FRAC,
) -> pd.DataFrame:
    """One row per kept window: band power per region, coh/wPLI per pair."""
    if not lfp:
        return pd.DataFrame()
    n = int(next(iter(lfp.values())).shape[-1])
    win_n = int(round(win_s * fs))
    hop = int(round(hop_s * fs))
    if n < win_n or hop < 1:
        return pd.DataFrame()

    union = union_artifact_mask(msk, n)
    nper = _nperseg(fs, win_n)
    rows: list[dict[str, float]] = []
    for i0 in range(0, n - win_n + 1, hop):
        i1 = i0 + win_n
        frac = float(union[i0:i1].mean())
        if frac > max_artifact_frac:
            continue
        sl = slice(i0, i1)
        row: dict[str, float] = {
            "t_start": i0 / fs,
            "t_end": i1 / fs,
            "frac_artifact": frac,
        }
        for r, x in lfp.items():
            f, p = signal.welch(x[sl], fs=fs, nperseg=nper, noverlap=nper // 2)
            row.update(band_powers(f, p, prefix=f"{r}_"))
        for a, b in PAIRS:
            if a in lfp and b in lfp:
                row.update(window_connectivity(lfp[a][sl], lfp[b][sl], fs, f"{a}-{b}", nper))
        rows.append(row)
    return pd.DataFrame(rows)


def reduce_windows(win: pd.DataFrame) -> pd.DataFrame:
    """Per-stem mean and variance of every numeric window column.

    Variance uses sample ddof=1. Stems with fewer than two kept windows get
    NaN variance.
    """
    if win.empty or "stem" not in win.columns:
        return pd.DataFrame(columns=["stem"])
    skip = {"stem", "t_start", "t_end", "frac_artifact"}
    numeric = [c for c in win.columns if c not in skip and pd.api.types.is_numeric_dtype(win[c])]
    if not numeric:
        return win[["stem"]].drop_duplicates()
    g = win.groupby("stem", sort=False)
    mean = g[numeric].mean().add_suffix("_winmean")
    var = g[numeric].var(ddof=1).add_suffix("_winvar")
    nwin = g.size().rename("n_windows")
    return mean.join(var).join(nwin).reset_index()
