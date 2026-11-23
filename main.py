#!/usr/bin/env python3
"""Entry point for the 22 November 2026 news-image bounty.

Copies the pre-drawn front page (entry.png, shipped in this repo) to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output). Standard library only,
no network, fully deterministic: the same bytes are written every run.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    source = HERE / "entry.png"
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    shutil.copyfile(source, target)
    if target.stat().st_size != source.stat().st_size:
        raise SystemExit("entry.png copy size mismatch")
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
