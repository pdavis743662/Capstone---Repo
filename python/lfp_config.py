"""Shared constants for the dynamical LFP pipeline.

Band edges must match Stage 3 in data_ingestion.ipynb so windowed columns
line up with features_session.csv names.

Column naming used everywhere:
    {region}_abs_{band}          absolute band power
    {region}_rel_{band}          power as a fraction of 1-100 Hz
    {region}_abs_{band}__vs_bl1  that week's maze (or inj) vs its own BL1
    {a}-{b}_wpli_{band}          weighted phase-lag index for one pair
    {col}_winmean / {col}_winvar session mean/variance of 10 s windows

Do not name this file config.py: that collides with other packages.
"""

from __future__ import annotations

import itertools

# Three bipolar-ish sites. Order is used for plots and pair generation.
REGIONS = ("BLA", "vHPC", "mPFC")
# Unordered pairs: BLA-vHPC, BLA-mPFC, vHPC-mPFC.
PAIRS = tuple(itertools.combinations(REGIONS, 2))

# Rodent theta is 4-12 Hz, not the 4-8 Hz human EEG convention.
BANDS = {
    "delta": (1.0, 4.0),
    "theta": (4.0, 12.0),
    "beta": (13.0, 30.0),
    "lgamma": (30.0, 60.0),
    "hgamma": (60.0, 100.0),
}

# Shared palette for Stage 9 / F11 / F12 so a band is the same color everywhere.
BAND_COLORS = {
    "delta": "#4C78A8",
    "theta": "#F58518",
    "beta": "#54A24B",
    "lgamma": "#E45756",
    "hgamma": "#B279A2",
}

# Stage 9: window-table figure/movie (no raw LFP).
BAND_COMPARE_SPEED = 4.0      # LFP seconds per video second if --movie
BAND_COMPARE_END_S = 2.0      # hold last frame for the end card
BAND_COMPARE_POWER = "bl1"    # bl1 = abs / that week's BL1 mean; also raw | rel
BAND_COMPARE_REGIONS = ("BLA", "vHPC")
BAND_COMPARE_PAIR = "BLA-vHPC"
BAND_COMPARE_FRAC_GRID = 51   # shared 0-1 time axis for group mean traces (F11)
# Thick traces on the per-mouse F12 figure; other bands are drawn muted.
BAND_COMPARE_FOCUS = {
    "BLA": "beta",
    "vHPC": "theta",
    "wpli": "beta",
}

# Stage 6 sliding windows. Hop of 5 s on a 10 s window means 50% overlap.
WIN_S = 10.0
HOP_S = 5.0
NPERSEG_S = 1.0               # Welch segment length inside each window
MAX_ARTIFACT_FRAC = 0.2       # drop the window if union mask exceeds this

FMIN_SPEC = 1.0
FMAX_SPEC = 100.0

# Confirmatory C1/C2 family. Stage 5 FDR is across this list only.
# Do not append metrics here without an explicit instruction.
PRIMARY_METRICS = (
    "burst_rate_per_min",
    "BLA_abs_beta",
    "BLA_abs_beta__vs_bl1",
    "vHPC_abs_theta",
    "vHPC_abs_theta__vs_bl1",
    "BLA-vHPC_wpli_beta",
    "BLA-vHPC_wpli_beta_winmean",
    "BLA-vHPC_wpli_beta_winvar",
)

# Band-specificity / coupling follow-ups. Own FDR family; never mixed with PRIMARY.
# BLA_abs_beta__vs_bl1 and vHPC_abs_theta__vs_bl1 appear in both so the
# exploratory correction still tests "is this band-specific".
EXPLORATORY_METRICS = (
    "BLA_abs_delta__vs_bl1",
    "BLA_abs_theta__vs_bl1",
    "BLA_abs_beta__vs_bl1",
    "BLA_abs_lgamma__vs_bl1",
    "BLA_abs_hgamma__vs_bl1",
    "vHPC_abs_delta__vs_bl1",
    "vHPC_abs_theta__vs_bl1",
    "vHPC_abs_beta__vs_bl1",
    "vHPC_abs_lgamma__vs_bl1",
    "vHPC_abs_hgamma__vs_bl1",
    "BLA_rel_beta__vs_bl1",
    "vHPC_rel_theta__vs_bl1",
    "BLA-vHPC_wpli_theta_winmean",
    "BLA-vHPC_wpli_theta_winvar",
)
