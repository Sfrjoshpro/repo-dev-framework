from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TASK_STATES = {"backlog", "clarifying", "ready", "active", "validating", "done", "blocked"}
ACTIVE_STATES = {"idle", "active", "validating", "blocked"}
REQUIRED_FILES = (
    "AGENTS.md",
    "development-state/CURRENT_STATE.yaml",
    "development-state/ACTIVE_WORK.yaml",
    "development-state/UNRESOLVED_UNKNOWNS.yaml",
    "development-state/blueprint/project-model.yaml",
    "tasks/TASK_TEMPLATE.yaml",
)
COMPLETION_FIELDS = (
    "implementation_complete",
    "validation_passed",
    "diff_reviewed",
    "state_updated",
    "blocking_unknowns_resolved",
    "checkpoint_recorded",
)


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def _scalar(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.*?)\s*$", text)
    if not match:
        return None
    value = match.group(1).strip()
    if value in {"", "null", "~"}:
        return None
    return value.strip('"\'')


def _bool_in_block(text: str, block: str, key: str) -> bool | None:
    match = re.search(
        rf"(?ms)^{re.escape(block)}:\s*\n((?:^[ ]+.*\n?)*)",
        text,
    )
    if not match:
        return None
    field = re.search(rf"(?m)^\s+{re.escape(key)}:\s*(true|false)\s*$", match.group(1))
    if not field:
        return None
    return field.group(1) == "true"


def _top_list(text: str, key: str) -> list[str]:
    match = re.search(rf"(?ms)^{re.escape(key)}:\s*\n((?:^[ ]+.*\n?)*)", text)
    if not match:
        return []
    return [m.group(1).strip() for m in re.finditer(r"(?m)^\s+-\s+(.+?)\s*$", match.group(1))]


def _section(text: str, name: str, following: tuple[str, ...]) -> str:
    starts = re.search(rf"(?m)^{re.escape(name)}:\s*$", text)
    if not starts:
        return ""
    end = len(text)
    for marker in following:
        found = re.search(rf"(?m)^{re.escape(marker)}:\s*$", text[starts.end():])
        if found:
            end = min(end, starts.end() + found.start())
    return text[starts.end():end]


def _check_structure() -> Check:
    missing = [p for p in REQUIRED_FILES if not (ROOT / p).exists()]
    return Check("Repository structure", not missing, "OK" if not missing else f"missing: {', '.join(missing)}")


def _check_active_work() -> tuple[Check, str, str | None]:
    text = _read("development-state/ACTIVE_WORK.yaml")
    lifecycle = _scalar(text, "lifecycle_state") or "missing"
    active_task = _scalar(text, "active_task")
    branch = _scalar(text, "branch")
    allowed = _top_list(text, "allowed_paths")

    if lifecycle not in ACTIVE_STATES:
        return Check("Active task", False, f"invalid lifecycle_state: {lifecycle}"), lifecycle, active_task

    if lifecycle == "idle":
        problems = []
        if active_task:
            problems.append("active_task must be null while idle")
        if branch:
            problems.append("branch must be null while idle")
        if allowed:
            problems.append("allowed_paths must be empty while idle")
        return Check("Active task", not problems, "IDLE" if not problems else "; ".join(problems)), lifecycle, active_task

    if not active_task:
        return Check("Active task", False, f"{lifecycle} requires active_task"), lifecycle, active_task
    if not (ROOT / active_task).exists():
        return Check("Active task", False, f"task file not found: {active_task}"), lifecycle, active_task
    if not branch:
        return Check("Active task", False, f"{lifecycle} requires branch"), lifecycle, active_task
    if not allowed:
        return Check("Active task", False, f"{lifecycle} requires allowed_paths"), lifecycle, active_task

    task_text = _read(active_task)
    task_status = _scalar(task_text, "status")
    if task_status != lifecycle:
        return Check("Active task", False, f"ACTIVE_WORK={lifecycle}, task={task_status}"), lifecycle, active_task

    task_allowed = _top_list(task_text, "allowed_paths")
    if set(allowed) != set(task_allowed):
        return Check("Active task", False, "allowed_paths differ from active task contract"), lifecycle, active_task

    return Check("Active task", True, f"{task_status}: {active_task}"), lifecycle, active_task


def _check_tasks() -> Check:
    problems: list[str] = []
    for path in sorted((ROOT / "tasks").glob("*.yaml")):
        if path.name == "TASK_TEMPLATE.yaml":
            continue
        text = path.read_text(encoding="utf-8")
        task_id = _scalar(text, "id") or path.stem
        status = _scalar(text, "status")
        if status not in TASK_STATES:
            problems.append(f"{task_id}: invalid status {status}")
            continue
        if status == "done":
            for field in COMPLETION_FIELDS:
                if _bool_in_block(text, "completion", field) is not True:
                    problems.append(f"{task_id}: done but {field} is not true")
            if _bool_in_block(text, "completion", "checkpoint_recorded") is True:
                handoff = ROOT / "development-state" / "handoffs" / f"{task_id}.yaml"
                if not handoff.exists():
                    problems.append(f"{task_id}: checkpoint marked recorded but handoff is missing")
    return Check("Task lifecycle", not problems, "OK" if not problems else "; ".join(problems))


def _check_blueprint() -> Check:
    text = _read("development-state/blueprint/project-model.yaml")
    nodes = _section(text, "nodes", ("edges", "flows"))
    edges = _section(text, "edges", ("flows",))
    flows = _section(text, "flows", ())
    node_ids = set(re.findall(r"(?m)^\s+- id:\s*([^\s]+)\s*$", nodes))
    problems: list[str] = []

    if not node_ids:
        problems.append("no blueprint nodes found")

    for source, target in re.findall(r"(?ms)^\s+- from:\s*([^\s]+)\s*\n\s+to:\s*([^\s]+)", edges):
        if source not in node_ids:
            problems.append(f"edge source missing: {source}")
        if target not in node_ids:
            problems.append(f"edge target missing: {target}")

    for ref in re.findall(r"(?m)^\s+(?:entry|node):\s*([^\s]+)\s*$", flows):
        if ref not in node_ids:
            problems.append(f"flow node missing: {ref}")

    return Check("Blueprint references", not problems, f"OK ({len(node_ids)} nodes)" if not problems else "; ".join(problems))


def _check_unknowns() -> Check:
    text = _read("development-state/UNRESOLVED_UNKNOWNS.yaml")
    open_count = len(re.findall(r"(?m)^\s+status:\s*open\s*$", text))
    return Check("Unknowns", True, f"{open_count} open")


def _context_advice(lifecycle: str, active_task: str | None) -> tuple[str, str]:
    if lifecycle == "idle":
        return "RED", "START NEW CHAT for the next milestone/task"
    if lifecycle in {"validating", "blocked"}:
        return "YELLOW", "CHECKPOINT SOON; start a new chat after the boundary is persisted"
    if lifecycle == "active" and active_task:
        return "GREEN", "CONTINUE THIS CHAT while this task remains coherent"
    return "YELLOW", "REVIEW REPOSITORY STATE before continuing"


def run_health_check() -> int:
    checks: list[Check] = [_check_structure()]
    active_check, lifecycle, active_task = _check_active_work()
    checks.extend([active_check, _check_tasks(), _check_blueprint(), _check_unknowns()])

    width = max(len(check.name) for check in checks)
    print("Repository Health")
    print("-" * (width + 24))
    for check in checks:
        status = "OK" if check.ok else "FAIL"
        print(f"{check.name:<{width}}  {status:<4}  {check.detail}")

    context, advice = _context_advice(lifecycle, active_task)
    print(f"{'Context health':<{width}}  {context}")
    print(f"{'Chat recommendation':<{width}}  {advice}")

    failed = [check for check in checks if not check.ok]
    if failed:
        print(f"\nResult: FAIL ({len(failed)} check(s))")
        return 1
    print("\nResult: PASS")
    return 0
