"""
Stage 9 -- Per-mouse multi-band saline vs psilocybin comparison.

Default: static PDF (2×3 traces + this-mouse stats). Optional --movie.

Driven by derived/windows.csv (no raw LFP). Shared session-fraction time.

Run:
    python step9_band_compare.py --derived derived --mouse C1_F1
    python step9_band_compare.py --derived derived --demo
    python step9_band_compare.py --derived derived --mouse C1_F1 --movie
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "python"))

from lfp_band_compare import (  # noqa: E402
    POWER_MODES,
    render_band_compare_figure,
    render_band_compare_video,
)
from lfp_config import BAND_COMPARE_POWER, BAND_COMPARE_SPEED  # noqa: E402
from lfp_pair import pick_demo_mouse_windows  # noqa: E402
from lfp_video import DEFAULT_FPS  # noqa: E402


def _all_windows(derived: Path) -> pd.DataFrame:
    """Full window table used to decide which mice have both weeks."""
    parquet = derived / "windows.parquet"
    csv_path = derived / "windows.csv"
    if parquet.exists():
        return pd.read_parquet(parquet)
    if csv_path.exists():
        return pd.read_csv(csv_path)
    raise SystemExit(f"No window table at {csv_path}")


def _features(derived: Path) -> pd.DataFrame | None:
    """Burst rate lives on the session table; window power is computed in the renderer."""
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
    speed: float = BAND_COMPARE_SPEED,
    fps: float = DEFAULT_FPS,
    power: str = BAND_COMPARE_POWER,
    movie: bool = False,
) -> Path:
    """Write PDF by default, or MP4 if ``movie`` is True.

    Demo mouse is chosen from windows.csv (C1_F1 preferred), not from local npz.
    """
    derived = Path(derived)
    man = pd.read_csv(derived / "manifest.csv")
    windows = _all_windows(derived)
    # --demo (or no --mouse) picks C1_F1 if that pair exists in windows.csv.
    uid = (
        pick_demo_mouse_windows(man, windows)
        if demo or not mouse
        else mouse
    )
    if uid not in set(man.subject_uid):
        raise SystemExit(f"Unknown --mouse {uid!r} (use a subject_uid like C1_F1)")
    feat = _features(derived)
    if movie:
        dest = Path(out) / uid / "band_compare_sal_vs_psi.mp4"
        print(f"{uid} → {dest}", flush=True)
        return render_band_compare_video(
            uid, derived=derived, out=dest, manifest=man,
            speed=speed, fps=fps, power=power,
        )
    dest = Path(out) / f"F12_{uid}_band_compare.pdf"
    print(f"{uid} → {dest}", flush=True)
    return render_band_compare_figure(
        uid, derived=derived, out=dest, manifest=man, feat=feat, power=power,
    )


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Stage 9: multi-band sal vs psi figure (or --movie) from windows.csv",
    )
    ap.add_argument("--derived", type=Path, default=Path("derived"))
    ap.add_argument(
        "--out", type=Path, default=None,
        help="default: figures_clean (PDF) or figures_video (--movie)",
    )
    ap.add_argument("--mouse", default=None, help="subject_uid, e.g. C1_F1")
    ap.add_argument(
        "--demo", action="store_true",
        help="First C1 mouse with both EZM weeks in windows.csv (prefers C1_F1)",
    )
    ap.add_argument(
        "--speed", type=float, default=BAND_COMPARE_SPEED,
        help="LFP seconds per video second (movie only; default 4)",
    )
    ap.add_argument("--fps", type=float, default=DEFAULT_FPS)
    ap.add_argument(
        "--power", choices=POWER_MODES, default=BAND_COMPARE_POWER,
        help="bl1 = abs / that week's BL1 mean (default); raw = log abs; rel = relative",
    )
    ap.add_argument(
        "--movie", action="store_true",
        help="Also encode the playhead MP4 (default is static PDF only)",
    )
    args = ap.parse_args()
    out = args.out
    if out is None:
        out = Path("figures_video") if args.movie else Path("figures_clean")
    run(
        derived=args.derived, out=out, mouse=args.mouse,
        demo=args.demo, speed=args.speed, fps=args.fps, power=args.power,
        movie=args.movie,
    )


if __name__ == "__main__":
    main()
