"""Shared constants for the dynamical LFP pipeline.

Keep band edges identical to Stage 3 so windowed features line up with
``features_session.csv`` column names.
"""

from __future__ import annotations

import itertools

REGIONS = ("BLA", "vHPC", "mPFC")
PAIRS = tuple(itertools.combinations(REGIONS, 2))

BANDS = {
    "delta": (1.0, 4.0),
    "theta": (4.0, 12.0),
    "beta": (13.0, 30.0),
    "lgamma": (30.0, 60.0),
    "hgamma": (60.0, 100.0),
}

WIN_S = 10.0
HOP_S = 5.0
NPERSEG_S = 1.0
MAX_ARTIFACT_FRAC = 0.2

FMIN_SPEC = 1.0
FMAX_SPEC = 100.0

# Confirmatory C1/C2 tests for Stage 5 (FDR across this list).
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
