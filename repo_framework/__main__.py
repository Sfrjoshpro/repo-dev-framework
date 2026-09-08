from __future__ import annotations

import sys

from .health import run_health_check


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] != "check":
        print("Usage: python -m repo_framework check")
        return 2
    return run_health_check()


if __name__ == "__main__":
    raise SystemExit(main())
