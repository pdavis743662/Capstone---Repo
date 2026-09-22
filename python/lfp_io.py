"""Load Stage-2 clean ``.npz`` recordings.

Put ``python/`` on ``sys.path`` and ``from lfp_io import load_clean``.
This file is named ``lfp_io`` so it does not shadow the stdlib ``io`` module.

On this machine ``derived/clean`` lives on the Desktop, so most ``.npz`` files
are iCloud ubiquitous items. When macOS has evicted the local bytes they show
up as ``dataless``; ``np.load`` then gets Errno 89 (ECANCELED) or hangs.
Hydrate from iCloud, copy to a temp file, then load.
"""

from __future__ import annotations

import errno
import os
import subprocess
import tempfile
import time
from pathlib import Path

import numpy as np

from lfp_config import REGIONS

_ECANCELED = getattr(errno, "ECANCELED", 89)
_SF_DATALESS = 0x40000000
_CHUNK = 256 * 1024


def _canceled(exc: BaseException) -> bool:
    return isinstance(exc, OSError) and getattr(exc, "errno", None) == _ECANCELED


def is_dataless(path: Path | str) -> bool:
    """True when macOS has evicted the file body (iCloud placeholder)."""
    try:
        return bool(os.stat(path).st_flags & _SF_DATALESS)
    except OSError:
        return False


def start_icloud_download(path: Path | str) -> None:
    """Ask macOS to fetch a ubiquitous file. Safe to call if already local."""
    src = str(Path(path).resolve())
    script = (
        "from Foundation import NSFileManager, NSURL\n"
        "url = NSURL.fileURLWithPath_(sys.argv[1])\n"
        "NSFileManager.defaultManager()"
        ".startDownloadingUbiquitousItemAtURL_error_(url, None)\n"
    )
    try:
        subprocess.run(
            ["/usr/bin/python3", "-c", "import sys\n" + script, src],
            timeout=15,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.TimeoutExpired):
        pass


def prefetch(paths: list[Path]) -> int:
    """Kick off iCloud downloads for every dataless path. Returns how many."""
    n = 0
    for p in paths:
        if p.exists() and is_dataless(p):
            start_icloud_download(p)
            n += 1
    return n


def hydrate(path: Path | str, *, timeout_s: float = 180) -> None:
    """Block until ``path`` is not dataless, or raise OSError."""
    src = Path(path)
    if not is_dataless(src):
        return
    start_icloud_download(src)
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        if not is_dataless(src):
            return
        time.sleep(0.5)
    raise OSError(_ECANCELED, f"timed out waiting for iCloud to download {src.name}")


def _scratch_dirs(src: Path) -> list[Path]:
    dirs = [Path(tempfile.gettempdir()), src.parent / ".npz_tmp"]
    out: list[Path] = []
    seen: set[Path] = set()
    for d in dirs:
        try:
            d = d.resolve()
            d.mkdir(parents=True, exist_ok=True)
        except OSError:
            continue
        if d not in seen:
            seen.add(d)
            out.append(d)
    if not out:
        raise RuntimeError("No writable temp directory for npz copy")
    return out


def _copy_chunked(src: Path, dest: Path) -> None:
    with open(src, "rb") as inf, open(dest, "wb") as out:
        while True:
            buf = inf.read(_CHUNK)
            if not buf:
                break
            out.write(buf)
        out.flush()
        os.fsync(out.fileno())


def _arrays_from_npz(path: Path) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray], float]:
    with np.load(path, allow_pickle=False) as z:
        fs = float(z["fs"])
        lfp = {
            r: np.array(z[f"lfp_{r}"], dtype=np.float32, copy=True)
            for r in REGIONS
            if f"lfp_{r}" in z
        }
        msk = {
            r: np.array(z[f"mask_{r}"], dtype=bool, copy=True)
            for r in REGIONS
            if f"mask_{r}" in z
        }
    return lfp, msk, fs


def load_clean(
    path: Path | str,
    *,
    retries: int = 4,
    retry_sleep_s: float = 0.4,
    hydrate_timeout_s: float = 180,
) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray], float]:
    """Return ``({region: lfp}, {region: artifact_mask}, fs)`` from a Stage-2 npz."""
    src = Path(path)
    hydrate(src, timeout_s=hydrate_timeout_s)
    last: BaseException | None = None
    scratch_dirs = _scratch_dirs(src)
    for attempt in range(retries):
        dest_dir = scratch_dirs[attempt % len(scratch_dirs)]
        fd, tmp_name = tempfile.mkstemp(prefix="lfp_", suffix=".npz", dir=dest_dir)
        os.close(fd)
        tmp_path = Path(tmp_name)
        try:
            _copy_chunked(src, tmp_path)
            return _arrays_from_npz(tmp_path)
        except OSError as e:
            last = e
            if is_dataless(src):
                start_icloud_download(src)
            if not _canceled(e) or attempt == retries - 1:
                raise
            time.sleep(retry_sleep_s * (attempt + 1))
        finally:
            tmp_path.unlink(missing_ok=True)
    assert last is not None
    raise last
