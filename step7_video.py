"""
Stage 7 -- Per-session LFP dashboard videos, grouped by mouse.

One MP4 per recording. Playback spans the full LFP at ``--speed`` (LFP seconds
per video second). Default 40× turns a ~10 min EZM into a ~15 s clip.

Run:
    python step7_video.py --derived derived --demo
    python step7_video.py --derived derived --stem Psi_C1_psi_F1_EZM
    python step7_video.py --derived derived --mouse C1_F1
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
from scipy import signal as _scipy_signal  # noqa: F401  load before python/ is on path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "python"))

from lfp_video import DEFAULT_FPS, DEFAULT_SPEED, render_session_video  # noqa: E402

DEMO_STEMS = ("Psi_C1_psi_F1_EZM", "Psi_C1_sal_F1_EZM")


def resolve_stems(man: pd.DataFrame, stems: list[str] | None, mouse: str | None, demo: bool) -> list[str]:
    if demo:
        return list(DEMO_STEMS)
    if stems:
        missing = [s for s in stems if s not in set(man.stem)]
        if missing:
            raise SystemExit(f"Unknown stem(s): {missing}")
        return list(stems)
    if mouse:
        hit = man[man.subject_uid == mouse]
        if hit.empty:
            hit = man[man.session_uid == mouse]
        if hit.empty:
            raise SystemExit(
                f"No recordings for --mouse {mouse!r}. "
                "Pass a subject_uid (C1_F1) or session_uid (C1_psi_F1)."
            )
        return hit.sort_values(["group", "rectype"]).stem.tolist()
    raise SystemExit("Pass --stem, --mouse, or --demo.")


def run(
    *,
    derived: Path,
    out: Path,
    stems: list[str] | None = None,
    mouse: str | None = None,
    demo: bool = False,
    speed: float = DEFAULT_SPEED,
    fps: float = DEFAULT_FPS,
) -> list[Path]:
    derived = Path(derived)
    out_root = Path(out)
    man = pd.read_csv(derived / "manifest.csv")
    want = resolve_stems(man, stems, mouse, demo)
    written: list[Path] = []
    n = len(want)
    for i, stem in enumerate(want, 1):
        meta = man.loc[man.stem == stem].iloc[0]
        dest = out_root / str(meta.subject_uid) / f"{stem}.mp4"
        print(f"[{i}/{n}] {stem} → {dest}", flush=True)
        written.append(
            render_session_video(
                stem,
                derived=derived,
                out=dest,
                manifest=man,
                speed=speed,
                fps=fps,
            )
        )
    return written


def main() -> None:
    ap = argparse.ArgumentParser(description="Stage 7: per-session LFP dashboard videos")
    ap.add_argument("--derived", type=Path, default=Path("derived"))
    ap.add_argument("--out", type=Path, default=Path("figures_video"),
                    help="Root folder; files go in <out>/<subject_uid>/<stem>.mp4")
    ap.add_argument("--stem", dest="stems", nargs="*", default=None,
                    help="One or more filename stems")
    ap.add_argument("--mouse", default=None,
                    help="subject_uid (C1_F1) or session_uid (C1_psi_F1)")
    ap.add_argument("--demo", action="store_true",
                    help="C1 F1 psi EZM and C1 F1 sal EZM")
    ap.add_argument("--speed", type=float, default=DEFAULT_SPEED,
                    help="LFP seconds per video second (default 40)")
    ap.add_argument("--fps", type=float, default=DEFAULT_FPS)
    args = ap.parse_args()
    run(
        derived=args.derived,
        out=args.out,
        stems=args.stems,
        mouse=args.mouse,
        demo=args.demo,
        speed=args.speed,
        fps=args.fps,
    )


if __name__ == "__main__":
    main()
