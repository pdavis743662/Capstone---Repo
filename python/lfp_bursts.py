"""Hilbert-envelope beta-burst detection (Stage 3).

Constants and thresholding match ``data_ingestion.ipynb`` Stage 3:
BL1 envelope percentile of that session, then detect on the target recording.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import numpy as np
from scipy import signal

from lfp_config import BANDS, REGIONS

BURST_BAND = tuple(BANDS["beta"])
BURST_PCTILE = 75.0
BURST_MIN_MS = 150.0
BURST_MERGE_MS = 50.0


def beta_envelope(
    x: np.ndarray,
    fs: float,
    band: tuple[float, float] = BURST_BAND,
) -> tuple[np.ndarray, np.ndarray]:
    sos = signal.butter(4, band, btype="bandpass", fs=fs, output="sos")
    xb = signal.sosfiltfilt(sos, np.asarray(x, dtype=np.float64))
    return xb, np.abs(signal.hilbert(xb))


def envelope_threshold(
    x: np.ndarray,
    fs: float,
    good: np.ndarray,
    pctile: float = BURST_PCTILE,
    band: tuple[float, float] = BURST_BAND,
) -> float:
    """Amplitude threshold from one recording — normally that animal's BL1."""
    _, env = beta_envelope(x, fs, band)
    ref = env[good] if good.sum() > 10 * fs else env
    return float(np.percentile(ref, pctile))


def detect_bursts(
    x: np.ndarray,
    fs: float,
    good: np.ndarray,
    band: tuple[float, float] = BURST_BAND,
    pctile: float = BURST_PCTILE,
    min_ms: float = BURST_MIN_MS,
    merge_ms: float = BURST_MERGE_MS,
    thr: float | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return ``(starts_s, ends_s, beta_filtered)``.

    ``thr=None`` uses a within-recording percentile. Pass the BL1 envelope
    threshold for drug-vs-baseline burst rates (Stage 3 default).
    """
    xb, env = beta_envelope(x, fs, band)
    if thr is None:
        ref = env[good] if good.sum() > 10 * fs else env
        thr = float(np.percentile(ref, pctile))

    above = (env > thr) & np.asarray(good, dtype=bool)
    d = np.diff(above.astype(int), prepend=0, append=0)
    starts = np.flatnonzero(d == 1)
    ends = np.flatnonzero(d == -1)
    if starts.size == 0:
        return starts.astype(float), ends.astype(float), xb

    if len(starts) > 1:
        gap = (starts[1:] - ends[:-1]) / fs * 1000
        keep = np.concatenate([[True], gap > merge_ms])
        new_s, new_e = [], []
        for i, k in enumerate(keep):
            if k:
                new_s.append(starts[i])
                new_e.append(ends[i])
            else:
                new_e[-1] = ends[i]
        starts, ends = np.asarray(new_s), np.asarray(new_e)

    dur_ms = (ends - starts) / fs * 1000
    ok = dur_ms >= min_ms
    return starts[ok] / fs, ends[ok] / fs, xb


def thresholds_from_bl1(
    lfp: Mapping[str, np.ndarray],
    msk: Mapping[str, np.ndarray],
    fs: float,
) -> dict[str, float]:
    """Per-region BL1 envelope thresholds (75th percentile of good samples)."""
    out: dict[str, float] = {}
    for r in REGIONS:
        if r not in lfp:
            continue
        good = ~np.asarray(msk[r], dtype=bool) if r in msk else np.ones(len(lfp[r]), dtype=bool)
        out[r] = envelope_threshold(lfp[r], fs, good)
    return out


def bursts_by_region(
    lfp: Mapping[str, np.ndarray],
    msk: Mapping[str, np.ndarray],
    fs: float,
    thr: Mapping[str, float] | None = None,
) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    """``{region: (starts_s, ends_s)}`` using BL1 thresholds when provided."""
    out: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for r, x in lfp.items():
        good = ~np.asarray(msk[r], dtype=bool) if r in msk else np.ones(len(x), dtype=bool)
        t = None if thr is None else thr.get(r)
        s, e, _ = detect_bursts(x, fs, good, thr=t)
        out[r] = (s, e)
    return out


def bl1_stem_for_session(manifest, session_uid: str) -> str | None:
    """Filename stem of the BL1 recording in the same session week."""
    hit = manifest[(manifest.session_uid == session_uid) & (manifest.rectype == "BL1")]
    if hit.empty:
        return None
    return str(hit.stem.iloc[0])


def load_session_thresholds(
    manifest,
    session_uid: str,
    clean_dir: Path,
    load_clean,
) -> dict[str, float] | None:
    """Load that week's BL1 and return per-region thresholds, or None."""
    stem = bl1_stem_for_session(manifest, session_uid)
    if stem is None:
        return None
    path = Path(clean_dir) / f"{stem}.npz"
    if not path.exists():
        return None
    try:
        lfp, msk, fs = load_clean(path)
    except OSError as e:
        print(f"  BL1 {stem} unreadable ({e}); using within-recording burst threshold")
        return None
    return thresholds_from_bl1(lfp, msk, fs)
