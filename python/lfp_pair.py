"""Resolve saline vs psilocybin weeks for one C1/C2 mouse.

Weeks are labeled by ``drug`` (sal / psi), not calendar order.
``subject_uid`` is cohort_mouse (C1_F1) and does not include the drug.
``session_uid`` is cohort_group_mouse (C1_psi_F1) and is one test week.

pair_weeks needs local EZM/EPM npz files (Stage 7/8 movies).
pair_weeks_in_windows only needs those stems in windows.csv (Stage 9 / F11).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from lfp_io import is_dataless

# C1/C2 maze is EZM; EPM is included so a mislabeled file still pairs.
BEHAVIOR = ("EZM", "EPM")
DRUGS = ("sal", "psi")
NEEDED = ("BL1", "beh")


def _stem_for(week: pd.DataFrame, rectypes: tuple[str, ...]) -> str | None:
    """First filename stem in this week whose rectype is in ``rectypes``."""
    hit = week[week.rectype.isin(rectypes)]
    if hit.empty:
        return None
    return str(hit.stem.iloc[0])


def pair_weeks(
    manifest: pd.DataFrame,
    subject_uid: str,
    clean_dir: Path,
    *,
    require_local_ezm: bool = True,
) -> dict | None:
    """Return ``{drug: {BL1, beh, session_uid, ...}}`` or None if unpaired.

    ``weeks[drug]['beh']`` is the EZM/EPM stem. ``require_local_ezm=False`` skips
    the npz-on-disk check (Stage 9 uses the window table instead).
    """
    sub = manifest[manifest.subject_uid == subject_uid]
    if sub.empty:
        return None
    out: dict = {"subject_uid": subject_uid, "cohort": str(sub.cohort.iloc[0]),
                 "mouse": str(sub.mouse.iloc[0]), "weeks": {}}
    clean_dir = Path(clean_dir)
    for drug in DRUGS:
        week = sub[sub.drug == drug]
        if week.empty:
            return None
        bl1 = _stem_for(week, ("BL1",))
        beh = _stem_for(week, BEHAVIOR)
        if not bl1 or not beh:
            return None
        beh_path = clean_dir / f"{beh}.npz"
        if require_local_ezm and (not beh_path.exists() or is_dataless(beh_path)):
            return None
        out["weeks"][drug] = {
            "BL1": bl1,
            "beh": beh,
            "session_uid": str(week.session_uid.iloc[0]),
            "rectype_beh": str(week.loc[week.stem == beh, "rectype"].iloc[0]),
        }
    return out


def paired_subject_uids(manifest: pd.DataFrame, clean_dir: Path) -> list[str]:
    """C1/C2 mice with both sal and psi behavior npz files on disk."""
    uids = (
        manifest[manifest.cohort.isin(["C1", "C2"])]
        .subject_uid.drop_duplicates()
        .tolist()
    )
    ok = []
    for uid in uids:
        if pair_weeks(manifest, uid, clean_dir) is not None:
            ok.append(uid)
    return ok


def pick_demo_mouse(manifest: pd.DataFrame, clean_dir: Path) -> str:
    """First C1 paired mouse, else any paired C1/C2 mouse."""
    paired = paired_subject_uids(manifest, clean_dir)
    if not paired:
        raise SystemExit(
            "No C1/C2 mouse has both saline and psilocybin EZM/EPM npz files local. "
            "Download derived/clean for one paired animal."
        )
    c1 = [u for u in paired if u.startswith("C1_")]
    return c1[0] if c1 else paired[0]


def pair_weeks_in_windows(
    manifest: pd.DataFrame,
    subject_uid: str,
    windows: pd.DataFrame,
    *,
    require_bl1: bool = True,
) -> dict | None:
    """Like ``pair_weeks`` but both behavior (and optional BL1) stems must be in the window table."""
    pair = pair_weeks(manifest, subject_uid, Path("."), require_local_ezm=False)
    if pair is None or windows is None or windows.empty or "stem" not in windows.columns:
        return None
    stems = set(windows.stem.astype(str))
    for drug in DRUGS:
        w = pair["weeks"][drug]
        if str(w["beh"]) not in stems:
            return None
        if require_bl1 and str(w["BL1"]) not in stems:
            return None
    return pair


def paired_uids_in_windows(
    manifest: pd.DataFrame,
    windows: pd.DataFrame,
    *,
    require_bl1: bool = True,
) -> list[str]:
    """C1/C2 mice whose sal and psi EZM/EPM (and BL1) stems exist in ``windows.csv``."""
    uids = (
        manifest[manifest.cohort.isin(["C1", "C2"])]
        .subject_uid.drop_duplicates()
        .tolist()
    )
    return [
        u for u in uids
        if pair_weeks_in_windows(manifest, u, windows, require_bl1=require_bl1) is not None
    ]


def pick_demo_mouse_windows(
    manifest: pd.DataFrame,
    windows: pd.DataFrame,
    *,
    prefer: str | None = "C1_F1",
) -> str:
    """First C1 mouse with both weeks in the window table (prefer ``C1_F1``)."""
    paired = paired_uids_in_windows(manifest, windows)
    if not paired:
        raise SystemExit(
            "No C1/C2 mouse has both saline and psilocybin EZM/EPM rows in windows.csv."
        )
    if prefer and prefer in paired:
        return prefer
    c1 = [u for u in paired if str(u).startswith("C1_")]
    return c1[0] if c1 else paired[0]
