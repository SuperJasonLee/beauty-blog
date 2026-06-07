#!/usr/bin/env python3
"""Audit script: detect duplicate featured/cover images.

Walks:
  - static/images/posts/*-featured.jpg
  - static/images/eye-surgery-news/*-cover.jpg

Computes a SHA-256 of each file, groups by hash, and reports any hash that
appears more than once. Used to catch the regression where a new post
silently inherits another post's cover (the original 2026-06-07 bug).

Exit code:
  - 0  no duplicates (default mode) OR duplicates present in non-strict mode
  - 1  duplicates present in --strict mode

Usage:
  python3 scripts/audit-dup-covers.py            # report, exit 0
  python3 scripts/audit-dup-covers.py --strict   # report, exit 1 on dup
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AUDIT_DIRS = [
    REPO_ROOT / "static" / "images" / "posts",
    REPO_ROOT / "static" / "images" / "eye-surgery-news",
]
GLOB_PATTERNS = ["*-featured.jpg", "*-cover.jpg"]


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_files() -> list[Path]:
    files: list[Path] = []
    for d in AUDIT_DIRS:
        if not d.exists():
            continue
        for pat in GLOB_PATTERNS:
            files.extend(sorted(d.glob(pat)))
    return files


def group_by_hash(paths: list[Path]) -> dict[str, list[Path]]:
    groups: dict[str, list[Path]] = defaultdict(list)
    for p in paths:
        groups[sha256_of(p)].append(p)
    return groups


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on any duplicate.")
    args = parser.parse_args()

    files = collect_files()
    if not files:
        print(f"OK: no files matched under {[str(d) for d in AUDIT_DIRS]}", file=sys.stderr)
        return 0

    groups = group_by_hash(files)
    dup_groups = {h: paths for h, paths in groups.items() if len(paths) > 1}
    unique_count = sum(1 for paths in groups.values() if len(paths) == 1)

    if not dup_groups:
        print(f"OK: {len(files)} files, all unique (across {len(groups)} hashes).")
        return 0

    print(f"DUPLICATES FOUND: {len(dup_groups)} hash collision(s) across {len(files)} files.", file=sys.stderr)
    for h, paths in sorted(dup_groups.items()):
        print(f"  sha256: {h}", file=sys.stderr)
        for p in paths:
            try:
                rel = p.relative_to(REPO_ROOT)
            except ValueError:
                rel = p
            print(f"    - {rel}", file=sys.stderr)
    print(f"({unique_count} files are unique.)", file=sys.stderr)

    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
