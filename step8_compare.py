"""
Stage 8 -- Per-mouse saline vs psilocybin comparison movie.

One MP4: saline EZM | psilocybin EZM (shared session-fraction time),
BL1 β-wPLI triangles as 'before maze' insets, end card with that mouse's Δ.

Run:
    python step8_compare.py --derived derived --demo
    python step8_compare.py --derived derived --mouse C1_F1 --speed 4
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
from scipy import signal as _scipy_signal  # noqa: F401

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "python"))

from lfp_compare import COMPARE_SPEED, render_compare_video  # noqa: E402
from lfp_pair import pick_demo_mouse  # noqa: E402
from lfp_video import DEFAULT_FPS  # noqa: E402


def _features(derived: Path) -> pd.DataFrame | None:
    dyn = derived / "features_dynamic.csv"
    sess = derived / "features_session.csv"
    if dyn.exists():
        return pd.read_csv(dyn)
    if sess.exists():
        return pd.read_csv(sess)
    return None


def run(
    *,
    derived: Path,
    out: Path,
    mouse: str | None = None,
    demo: bool = False,
    speed: float = COMPARE_SPEED,
    fps: float = DEFAULT_FPS,
) -> Path:
    derived = Path(derived)
    man = pd.read_csv(derived / "manifest.csv")
    uid = pick_demo_mouse(man, derived / "clean") if demo or not mouse else mouse
    if uid not in set(man.subject_uid):
        raise SystemExit(f"Unknown --mouse {uid!r} (use a subject_uid like C1_F1)")
    feat = _features(derived)
    dest = Path(out) / uid / "compare_sal_vs_psi.mp4"
    print(f"{uid} → {dest}", flush=True)
    return render_compare_video(
        uid, derived=derived, out=dest, manifest=man, feat=feat,
        speed=speed, fps=fps,
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="Stage 8: sal vs psi comparison movie")
    ap.add_argument("--derived", type=Path, default=Path("derived"))
    ap.add_argument("--out", type=Path, default=Path("figures_video"))
    ap.add_argument("--mouse", default=None, help="subject_uid, e.g. C1_F1")
    ap.add_argument("--demo", action="store_true",
                    help="First C1 mouse with both EZM npz files local")
    ap.add_argument("--speed", type=float, default=COMPARE_SPEED,
                    help="LFP seconds per video second (default 4)")
    ap.add_argument("--fps", type=float, default=DEFAULT_FPS)
    args = ap.parse_args()
    run(
        derived=args.derived, out=args.out, mouse=args.mouse,
        demo=args.demo, speed=args.speed, fps=args.fps,
    )


if __name__ == "__main__":
    main()
