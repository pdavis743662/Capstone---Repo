"""
Stage 6 -- Time-resolved (10 s) power and connectivity.

Reads Stage-2 clean npz files, writes a window table, then reduces to
per-recording mean/variance and merges onto the session feature table.

Run:
    python step6_windows.py --derived ../derived --limit 6
    python step6_windows.py --derived ../derived
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
from scipy import signal as _scipy_signal  # noqa: F401  load before python/ is on path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "python"))

from lfp_io import is_dataless, load_clean, prefetch  # noqa: E402
from lfp_windows import reduce_windows, window_features  # noqa: E402



def _write_windows(df: pd.DataFrame, dest: Path) -> Path:
    """Parquet if pyarrow/fastparquet is available, else CSV."""
    dest = Path(dest)
    try:
        df.to_parquet(dest, index=False)
        return dest
    except ImportError:
        csv_path = dest.with_suffix(".csv")
        df.to_csv(csv_path, index=False)
        print(f"parquet engine missing; wrote {csv_path}")
        return csv_path


def _read_windows(derived: Path) -> pd.DataFrame:
    parquet = derived / "windows.parquet"
    csv_path = derived / "windows.csv"
    if parquet.exists():
        return pd.read_parquet(parquet)
    if csv_path.exists():
        return pd.read_csv(csv_path)
    raise FileNotFoundError(f"No window table in {derived}")


def process_stems(
    stems: list[str],
    clean_dir: Path,
    *,
    progress: bool = True,
) -> tuple[pd.DataFrame, list[dict]]:
    """Compute window rows for each stem. Failed files are listed, not raised."""
    rows: list[pd.DataFrame] = []
    fails: list[dict] = []
    n = len(stems)
    paths = [clean_dir / f"{stem}.npz" for stem in stems]
    n_cloud = prefetch(paths)
    if n_cloud:
        print(f"Requested iCloud download for {n_cloud} dataless npz files", flush=True)
    for i, stem in enumerate(stems, 1):
        path = clean_dir / f"{stem}.npz"
        extra = " (waiting on iCloud)" if is_dataless(path) else ""
        print(f"[{i}/{n}] {stem}{extra} ...", flush=True)
        try:
            lfp, msk, fs = load_clean(path)
            w = window_features(lfp, msk, fs)
            if w.empty:
                fails.append({"stem": stem, "error": "no kept windows"})
                if progress:
                    print(f"[{i}/{n}] {stem} no kept windows")
                continue
            w.insert(0, "stem", stem)
            rows.append(w)
            if progress:
                print(f"[{i}/{n}] {stem} {len(w)} windows")
        except Exception as e:  # noqa: BLE001
            fails.append({"stem": stem, "error": repr(e)})
            if progress:
                print(f"[{i}/{n}] {stem} FAILED: {e}")
    win = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    return win, fails


def merge_dynamic(derived: Path, reduced: pd.DataFrame) -> pd.DataFrame:
    """Session features + window mean/variance. Prefer the BL1-normalized table."""
    norm = derived / "features_normalized.csv"
    sess = derived / "features_session.csv"
    base_path = norm if norm.exists() else sess
    if not base_path.exists():
        raise FileNotFoundError(f"Need {sess} or {norm}")
    base = pd.read_csv(base_path)
    return base.merge(reduced, on="stem", how="left")


def run(
    *,
    derived: Path,
    clean_dir: Path | None = None,
    limit: int | None = None,
    stems: list[str] | None = None,
    reduce_only: bool = False,
) -> None:
    derived = Path(derived)
    derived.mkdir(parents=True, exist_ok=True)
    clean_dir = Path(clean_dir) if clean_dir is not None else derived / "clean"

    if not reduce_only:
        man = pd.read_csv(derived / "manifest.csv")
        if stems:
            want = set(stems)
            man = man[man.stem.isin(want)]
        elif limit:
            man = man.head(int(limit))
        if man.empty:
            raise SystemExit("No stems to process.")
        if not clean_dir.is_dir():
            raise SystemExit(f"Clean npz directory not found: {clean_dir}")

        win, fails = process_stems(man.stem.tolist(), clean_dir)
        out_win = _write_windows(win, derived / "windows.parquet")
        print(f"Wrote {out_win} ({len(win)} rows, {win.stem.nunique() if len(win) else 0} files)")
        if fails:
            fail_path = derived / "windows_failures.csv"
            pd.DataFrame(fails).to_csv(fail_path, index=False)
            print(f"Wrote {fail_path} ({len(fails)} failures)")

    win = _read_windows(derived)
    reduced = reduce_windows(win)
    dyn = merge_dynamic(derived, reduced)
    dest = derived / "features_dynamic.csv"
    dyn.to_csv(dest, index=False)
    print(f"Wrote {dest} ({len(dyn)} rows, {sum(c.endswith('_winvar') for c in dyn.columns)} winvar cols)")


def main() -> None:
    print("step6 starting", flush=True)
    ap = argparse.ArgumentParser(description="Stage 6: 10 s windowed LFP features")
    ap.add_argument("--derived", type=Path, default=Path("../derived"))
    ap.add_argument("--clean", type=Path, default=None,
                    help="npz directory (default: <derived>/clean)")
    ap.add_argument("--limit", type=int, default=None,
                    help="Process only the first N manifest rows (smoke test)")
    ap.add_argument("--stems", nargs="*", default=None,
                    help="Process only these filename stems")
    ap.add_argument("--reduce-only", action="store_true",
                    help="Rebuild features_dynamic.csv from an existing window table")
    args = ap.parse_args()
    run(
        derived=args.derived,
        clean_dir=args.clean,
        limit=args.limit,
        stems=args.stems,
        reduce_only=args.reduce_only,
    )


if __name__ == "__main__":
    main()
