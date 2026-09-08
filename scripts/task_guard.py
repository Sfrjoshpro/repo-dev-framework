#!/usr/bin/env python3
"""Validate task lifecycle, changed-file scope, and active context state."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from repo_framework.context import validate_context

ACTIVE_WORK = ROOT / "development-state" / "ACTIVE_WORK.yaml"
TASK_TEMPLATE = ROOT / "tasks" / "TASK_TEMPLATE.yaml"

VALID_STATES = {
    "backlog",
    "clarifying",
    "ready",
    "active",
    "validating",
    "blocked",
    "done",
}


def _scalar(lines: list[str], key: str) -> str | None:
    prefix = f"{key}:"
    for line in lines:
        if line.startswith(prefix):
            value = line[len(prefix):].strip()
            if value in {"", "null", "~"}:
                return None
            return value.strip("'\"")
    return None


def _list(lines: list[str], key: str) -> list[str]:
    prefix = f"{key}:"
    for index, line in enumerate(lines):
        if not line.startswith(prefix):
            continue
        inline = line[len(prefix):].strip()
        if inline == "[]":
            return []
        values: list[str] = []
        for child in lines[index + 1 :]:
            if child and not child.startswith((" ", "\t")):
                break
            stripped = child.strip()
            if stripped.startswith("- "):
                values.append(stripped[2:].strip().strip("'\""))
        return values
    return []


def _read(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def _git_changed_paths(base_ref: str) -> list[str]:
    command = ["git", "diff", "--name-only", f"{base_ref}...HEAD"]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git diff failed")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _matches(path: str, allowed: str) -> bool:
    normalized = allowed.rstrip("/")
    return path == normalized or path.startswith(normalized + "/")


def validate_task_file(path: Path) -> list[str]:
    lines = _read(path)
    errors: list[str] = []
    status = _scalar(lines, "status")
    allowed_paths = _list(lines, "allowed_paths")
    unknowns = _list(lines, "unknowns")
    validation = _list(lines, "validation")

    if status not in VALID_STATES:
        errors.append(f"invalid task status: {status!r}")
    if status in {"ready", "active", "validating", "done"}:
        if not allowed_paths:
            errors.append(f"{status} task must declare at least one allowed path")
        if not validation:
            errors.append(f"{status} task must declare validation")
    if status in {"ready", "active"} and unknowns:
        errors.append(f"{status} task cannot contain unresolved unknowns")
    return errors


def validate_active_work(base_ref: str | None) -> list[str]:
    lines = _read(ACTIVE_WORK)
    errors: list[str] = []
    active_task = _scalar(lines, "active_task")
    lifecycle_state = _scalar(lines, "lifecycle_state")
    allowed_paths = _list(lines, "allowed_paths")

    if active_task is None:
        if lifecycle_state not in {None, "idle"}:
            errors.append("ACTIVE_WORK without an active task must use lifecycle_state: idle")
        errors.extend(validate_context(ROOT))
        return errors

    if lifecycle_state not in {"active", "validating", "blocked"}:
        errors.append("active work lifecycle_state must be active, validating, or blocked")
    if lifecycle_state in {"active", "validating"} and not allowed_paths:
        errors.append("active work must declare at least one allowed path")

    if base_ref and allowed_paths:
        try:
            changed = _git_changed_paths(base_ref)
        except RuntimeError as exc:
            errors.append(str(exc))
        else:
            framework_paths = {"development-state/ACTIVE_WORK.yaml"}
            violations = [
                path
                for path in changed
                if path not in framework_paths
                and not any(_matches(path, allowed) for allowed in allowed_paths)
            ]
            if violations:
                errors.append(
                    "scope violation: changed paths outside allowed_paths: "
                    + ", ".join(sorted(violations))
                )

    errors.extend(validate_context(ROOT))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=Path, help="validate a task contract file")
    parser.add_argument("--base-ref", help="compare HEAD with this Git ref and enforce ACTIVE_WORK allowed_paths")
    args = parser.parse_args()

    errors = validate_active_work(args.base_ref)
    if args.task:
        task_path = args.task if args.task.is_absolute() else ROOT / args.task
        errors.extend(validate_task_file(task_path))
    else:
        errors.extend(validate_task_file(TASK_TEMPLATE))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("task guard: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
