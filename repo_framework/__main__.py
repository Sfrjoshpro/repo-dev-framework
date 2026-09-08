from __future__ import annotations

import argparse

from .context import add_expansion, init_context, print_context, record_broad_search, reset_context
from .health import run_health_check


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m repo_framework")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("check", help="validate repository framework health")

    context_parser = subparsers.add_parser("context", help="inspect or manage the active context working set")
    context_sub = context_parser.add_subparsers(dest="context_command")

    init_parser = context_sub.add_parser("init", help="initialize context from the active task")
    init_parser.add_argument("--force", action="store_true")

    add_parser = context_sub.add_parser("add", help="record a justified dependency read")
    add_parser.add_argument("path")
    add_parser.add_argument("--reason", required=True)

    broad_parser = context_sub.add_parser("broaden", help="record an authorized Tier 4 broad search")
    broad_parser.add_argument("--reason", required=True)

    context_sub.add_parser("reset", help="clear context after the repository becomes idle")

    args = parser.parse_args()
    if args.command == "check":
        return run_health_check()
    if args.command == "context":
        try:
            if args.context_command == "init":
                init_context(force=args.force)
            elif args.context_command == "add":
                add_expansion(args.path, args.reason)
            elif args.context_command == "broaden":
                record_broad_search(args.reason)
            elif args.context_command == "reset":
                reset_context()
        except RuntimeError as exc:
            print(f"ERROR: {exc}")
            return 1
        return print_context()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
