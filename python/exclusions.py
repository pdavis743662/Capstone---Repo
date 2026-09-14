"""Dead-channel exclusion for the LFP pipeline.

Thresholds
----------
LOG_RMS_FLOOR = 2.0 comes from the QC amplitude distribution: the main RMS
clouds sit near log10 = 2.6–2.9, while a distinct dead/disconnected cluster
sits near 1.05. 2.0 is the gap between those modes.

KURTOSIS_CEILING = 20.0 flags channels whose amplitude distribution is
dominated by rare transients rather than neural signal.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

REGIONS = ("BLA", "vHPC", "mPFC")

# See module docstring for the empirical justification.
LOG_RMS_FLOOR = 2.0
KURTOSIS_CEILING = 20.0
ROBUST_MAD_K = 5.0
MAD_SCALE = 1.4826

META_COLS = ("cohort", "group", "drug", "rectype", "mouse", "subject_uid")


def _log10_rms(rms: pd.Series) -> pd.Series:
    """log10(RMS); non-positive / NaN -> NaN (caller treats as dead)."""
    rms = pd.to_numeric(rms, errors="coerce")
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.log10(rms.where(rms > 0))


def _robust_floor(log_rms: pd.Series) -> float:
    x = np.asarray(log_rms, float)
    x = x[np.isfinite(x)]
    if len(x) == 0:
        return float("nan")
    med = float(np.median(x))
    mad = float(np.median(np.abs(x - med)))
    return med - ROBUST_MAD_K * MAD_SCALE * mad


def find_bad_channels(
    qc: pd.DataFrame,
    log_rms_floor: float = LOG_RMS_FLOOR,
    kurtosis_ceiling: float = KURTOSIS_CEILING,
) -> pd.DataFrame:
    """Flag dead / high-kurtosis / missing channels.

    Returns a long DataFrame with columns
    [stem, region, reason, log_rms, kurtosis].
    """
    if "stem" not in qc.columns:
        raise KeyError("qc.csv is missing required column 'stem'")

    rows: list[dict] = []
    print("RMS thresholds (fixed vs robust-per-region; only the fixed floor is applied):")
    for region in REGIONS:
        rms_col = f"{region}_rms"
        kurt_col = f"{region}_kurtosis"
        present_col = f"{region}_present"
        if rms_col not in qc.columns:
            raise KeyError(f"qc.csv is missing required column {rms_col!r}")
        if kurt_col not in qc.columns:
            raise KeyError(f"qc.csv is missing required column {kurt_col!r}")

        log_rms = _log10_rms(qc[rms_col])
        kurt = pd.to_numeric(qc[kurt_col], errors="coerce")
        if present_col in qc.columns:
            present = qc[present_col].fillna(False).astype(bool)
        else:
            present = pd.Series(True, index=qc.index)

        robust = _robust_floor(log_rms[present])
        n_finite = int(np.isfinite(log_rms[present]).sum())
        print(
            f"  {region}: fixed floor={log_rms_floor:.3f}  "
            f"robust (median - {ROBUST_MAD_K:g}·1.4826·MAD)={robust:.3f}  "
            f"n_finite={n_finite}"
        )

        for i in qc.index:
            stem = qc.at[i, "stem"]
            lr = log_rms.at[i]
            k = kurt.at[i]
            rec = dict(stem=stem, region=region, log_rms=lr, kurtosis=k)
            if not bool(present.at[i]):
                rows.append({**rec, "reason": "missing"})
                continue
            if not np.isfinite(lr) or lr < log_rms_floor:
                rows.append({**rec, "reason": "dead_channel"})
            if np.isfinite(k) and k > kurtosis_ceiling:
                rows.append({**rec, "reason": "high_kurtosis"})

    cols = ["stem", "region", "reason", "log_rms", "kurtosis"]
    return pd.DataFrame(rows, columns=cols)


def bad_channel_map(bad_df: pd.DataFrame) -> dict[str, set[str]]:
    """Return dict: stem -> set of bad region names."""
    out: dict[str, set[str]] = {}
    if bad_df is None or bad_df.empty:
        return out
    for stem, sub in bad_df.groupby("stem"):
        out[str(stem)] = set(sub["region"].astype(str))
    return out


def _column_touches_region(col: str, region: str) -> bool:
    """True for `{region}_...` columns and pair prefixes like `BLA-vHPC_`."""
    if col.startswith(f"{region}_"):
        return True
    head = col.split("_", 1)[0]
    if "-" in head:
        return region in head.split("-")
    return False


def apply_exclusions(
    df: pd.DataFrame,
    bad_map: dict[str, set[str]],
    drop_if_bad: tuple[str, ...] = ("BLA",),
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """NaN region-specific and structurally dependent metrics.

    (a) Region-wise: columns belonging to a bad region (including connectivity
        pairs that include that region) are set to NaN. A bad mPFC does not
        wipe a BLA-only measurement.
    (b) Structural: `burst_*` depends on BLA; `phase_*` depends on BLA and
        vHPC. Those column groups are NaN'd so dropna() downstream drops them
        from the relevant tests without discarding the rest of the row.

    `drop_if_bad` lists regions whose structural dependents are NaN'd (BLA
    for bursts). Phase always NaNs if BLA or vHPC is bad.
    """
    if "stem" not in df.columns:
        raise KeyError("features table is missing required column 'stem'")

    clean = df.copy()
    drop_if_bad = tuple(drop_if_bad)
    audit_rows: list[dict] = []

    for i in clean.index:
        stem = str(clean.at[i, "stem"])
        bad = set(bad_map.get(stem, ()))
        if not bad:
            continue

        meta = {c: clean.at[i, c] for c in META_COLS if c in clean.columns}
        for region in sorted(bad):
            audit_rows.append({"stem": stem, "region": region, **meta})
            for col in clean.columns:
                if _column_touches_region(col, region):
                    clean.at[i, col] = np.nan

        if "BLA" in drop_if_bad and "BLA" in bad:
            for col in clean.columns:
                if col.startswith("burst_"):
                    clean.at[i, col] = np.nan
        if bad & {"BLA", "vHPC"}:
            for col in clean.columns:
                if col.startswith("phase_"):
                    clean.at[i, col] = np.nan

    audit_cols = ["stem", "region", *[c for c in META_COLS if c in df.columns]]
    audit_df = pd.DataFrame(audit_rows, columns=audit_cols)
    return clean, audit_df


def exclusion_report(audit_df: pd.DataFrame, qc: pd.DataFrame) -> pd.DataFrame:
    """Count excluded files per (cohort, group, region) and group-level %."""
    if audit_df is None or audit_df.empty:
        print("\n=== Exclusion report ===")
        print("  No channels excluded.")
        return pd.DataFrame(
            columns=["cohort", "group", "region", "n_excluded",
                     "n_files_in_group", "pct_of_group_files"]
        )

    need = {"stem", "region"}
    missing = need - set(audit_df.columns)
    if missing:
        raise KeyError(f"audit_df missing columns {sorted(missing)}")

    audit = audit_df.copy()
    if "cohort" not in audit.columns or "group" not in audit.columns:
        meta = [c for c in ("stem", "cohort", "group", "drug", "rectype") if c in qc.columns]
        audit = audit.merge(qc[meta].drop_duplicates("stem"), on="stem", how="left")

    counts = (
        audit.groupby(["cohort", "group", "region"], dropna=False)
        .stem.nunique()
        .rename("n_excluded")
        .reset_index()
    )
    group_n = (
        qc.groupby(["cohort", "group"], dropna=False)
        .stem.nunique()
        .rename("n_files_in_group")
        .reset_index()
    )
    out = counts.merge(group_n, on=["cohort", "group"], how="left")
    out["pct_of_group_files"] = 100.0 * out["n_excluded"] / out["n_files_in_group"]

    affected = (
        audit.groupby(["cohort", "group"], dropna=False)
        .stem.nunique()
        .rename("n_files_affected")
        .reset_index()
    )
    grp = group_n.merge(affected, on=["cohort", "group"], how="left")
    grp["n_files_affected"] = grp["n_files_affected"].fillna(0).astype(int)
    grp["pct_files_affected"] = 100.0 * grp["n_files_affected"] / grp["n_files_in_group"]

    print("\n=== Excluded files per (cohort, group, region) ===")
    print(out.to_string(index=False))
    print("\n=== Share of each group's files with ≥1 excluded channel ===")
    print(grp.to_string(index=False))
    return out


def _parse_args(argv=None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Flag dead LFP channels from qc.csv")
    ap.add_argument("--derived", type=Path, default=Path("../derived"))
    ap.add_argument("--qc", type=Path, default=None)
    return ap.parse_args(argv)


def main(argv=None) -> None:
    args = _parse_args(argv)
    qc_path = args.qc if args.qc is not None else args.derived / "qc.csv"
    if not qc_path.exists():
        raise SystemExit(f"qc.csv not found: {qc_path}")

    qc = pd.read_csv(qc_path)
    bad = find_bad_channels(qc)
    args.derived.mkdir(parents=True, exist_ok=True)
    dest = args.derived / "exclusions.csv"
    bad.to_csv(dest, index=False)
    print(f"\nWrote {dest} ({len(bad)} rows)")
    if not bad.empty:
        print(bad.to_string(index=False))
    else:
        print("(no bad channels)")

    summary = exclusion_report(bad, qc)
    audit_dest = args.derived / "exclusion_audit.csv"
    summary.to_csv(audit_dest, index=False)
    print(f"\nWrote {audit_dest} ({len(summary)} rows)")


if __name__ == "__main__":
    main()
