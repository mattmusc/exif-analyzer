#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


DIR_TARGETS = {
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    "htmlcov",
    "dist",
    "build",
}

FILE_TARGETS = {
    ".coverage",
}

def rm_tree(p: Path) -> None:
    shutil.rmtree(p, ignore_errors=True)

def rm_file(p: Path) -> None:
    try:
        p.unlink()
    except FileNotFoundError:
        pass

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--venv", action="store_true", help="Also remove .venv")
    args = parser.parse_args()

    root = Path(".")

    # Remove known directories anywhere in the repo
    for name in DIR_TARGETS:
        for p in root.rglob(name):
            if p.is_dir():
                rm_tree(p)

    # Remove egg-info directories anywhere
    for p in root.rglob("*.egg-info"):
        if p.is_dir():
            rm_tree(p)

    # Remove known files (root or anywhere)
    for name in FILE_TARGETS:
        for p in root.rglob(name):
            if p.is_file():
                rm_file(p)

    if args.venv:
        rm_tree(Path(".venv"))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
