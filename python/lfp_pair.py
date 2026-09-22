"""Resolve saline vs psilocybin weeks for one C1/C2 mouse.

Weeks are labeled by ``drug`` (sal / psi), not calendar order. Both EZM (or EPM)
``.npz`` files must be local; BL1 can come from the window table if the npz is
evicted.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from lfp_io import is_dataless

BEHAVIOR = ("EZM", "EPM")
DRUGS = ("sal", "psi")
NEEDED = ("BL1", "beh")


def _stem_for(week: pd.DataFrame, rectypes: tuple[str, ...]) -> str | None:
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
    """Return ``{drug: {BL1, beh, session_uid, ...}}`` or None if unpaired."""
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
