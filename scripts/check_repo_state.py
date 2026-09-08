#!/usr/bin/env python3
"""Compatibility wrapper for the repository health command."""

from repo_framework.health import run_health_check


if __name__ == "__main__":
    raise SystemExit(run_health_check())
