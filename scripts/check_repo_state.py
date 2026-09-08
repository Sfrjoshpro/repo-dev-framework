#!/usr/bin/env python3
"""Compatibility wrapper for the repository health command."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from repo_framework.health import run_health_check


if __name__ == "__main__":
    raise SystemExit(run_health_check())
