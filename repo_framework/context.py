from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE_WORK = "development-state/ACTIVE_WORK.yaml"
ACTIVE_CONTEXT = "development-state/ACTIVE_CONTEXT.yaml"


@dataclass
class ContextState:
    active_task: str | None
    context_tier: int
    working_set: list[str]
    expanded_paths: list[str]
    expansion_log: list[str]
    broad_searches: int
    broad_search_log: list[str]
    max_tier: int
    max_files: int
    max_expansions: int
    max_broad_searches: int

    @property
    def total_files(self) -> int:
        return len(dict.fromkeys(self.working_set + self.expanded_paths))


def _read(root: Path, relative: str) -> str:
    return (root / relative).read_text(encoding="utf-8")


def _scalar(text: str, key: str) -> str | None:
    prefix = f"{key}:"
    for line in text.splitlines():
        if line.startswith(prefix):
            value = line[len(prefix):].strip()
            if value in {"", "null", "~"}:
                return None
            return value.strip("'\"")
    return None


def _top_list(text: str, key: str) -> list[str]:
    lines = text.splitlines()
    marker = f"{key}:"
    for index, line in enumerate(lines):
        if line != marker:
            continue
        values: list[str] = []
        for child in lines[index + 1 :]:
            if child and not child.startswith((" ", "\t")):
                break
            stripped = child.strip()
            if stripped.startswith("- "):
                values.append(stripped[2:].strip().strip("'\""))
        return values
    return []


def _block_int(text: str, block: str, key: str, default: int) -> int:
    lines = text.splitlines()
    marker = f"{block}:"
    prefix = f"  {key}:"
    in_block = False
    for line in lines:
        if line == marker:
            in_block = True
            continue
        if in_block and line and not line.startswith((" ", "\t")):
            break
        if in_block and line.startswith(prefix):
            try:
                return int(line[len(prefix):].strip())
            except ValueError:
                return default
    return default


def _as_int(value: str | None, default: int) -> int:
    try:
        return int(value) if value is not None else default
    except ValueError:
        return default


def _dedupe(paths: list[str]) -> list[str]:
    return list(dict.fromkeys(path for path in paths if path))


def load_context(root: Path = ROOT) -> ContextState | None:
    path = root / ACTIVE_CONTEXT
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    return ContextState(
        active_task=_scalar(text, "active_task"),
        context_tier=_as_int(_scalar(text, "context_tier"), 0),
        working_set=_top_list(text, "working_set"),
        expanded_paths=_top_list(text, "expanded_paths"),
        expansion_log=_top_list(text, "expansion_log"),
        broad_searches=_as_int(_scalar(text, "broad_searches"), 0),
        broad_search_log=_top_list(text, "broad_search_log"),
        max_tier=_block_int(text, "budget", "max_tier", 3),
        max_files=_block_int(text, "budget", "max_files", 12),
        max_expansions=_block_int(text, "budget", "max_expansions", 4),
        max_broad_searches=_block_int(text, "budget", "max_broad_searches", 0),
    )


def write_context(state: ContextState, root: Path = ROOT) -> None:
    def emit_list(name: str, values: list[str]) -> list[str]:
        if not values:
            return [f"{name}: []"]
        return [f"{name}:", *[f"  - {value}" for value in values]]

    lines = [
        "version: 1",
        f"active_task: {state.active_task or 'null'}",
        f"context_tier: {state.context_tier}",
        "",
        *emit_list("working_set", state.working_set),
        *emit_list("expanded_paths", state.expanded_paths),
        *emit_list("expansion_log", state.expansion_log),
        f"broad_searches: {state.broad_searches}",
        *emit_list("broad_search_log", state.broad_search_log),
        "",
        "budget:",
        f"  max_tier: {state.max_tier}",
        f"  max_files: {state.max_files}",
        f"  max_expansions: {state.max_expansions}",
        f"  max_broad_searches: {state.max_broad_searches}",
        "",
    ]
    (root / ACTIVE_CONTEXT).write_text("\n".join(lines), encoding="utf-8")


def active_task_path(root: Path = ROOT) -> str | None:
    return _scalar(_read(root, ACTIVE_WORK), "active_task")


def _task_list(root: Path, task_path: str, key: str) -> list[str]:
    return _top_list(_read(root, task_path), key)


def init_context(root: Path = ROOT, force: bool = False) -> ContextState:
    task_path = active_task_path(root)
    if not task_path:
        state = ContextState(None, 0, [], [], [], 0, [], 0, 0, 0, 0)
        write_context(state, root)
        return state

    existing = load_context(root)
    if existing and existing.active_task == task_path and not force:
        raise RuntimeError("active context already exists for this task; use --force to rebuild it")

    startup = [
        "AGENTS.md",
        "development-state/CURRENT_STATE.yaml",
        "development-state/ACTIVE_WORK.yaml",
        task_path,
    ]
    required = _task_list(root, task_path, "required_context")
    allowed = _task_list(root, task_path, "allowed_paths")
    working_set = _dedupe(startup + required + allowed)
    state = ContextState(
        active_task=task_path,
        context_tier=2,
        working_set=working_set,
        expanded_paths=[],
        expansion_log=[],
        broad_searches=0,
        broad_search_log=[],
        max_tier=3,
        max_files=len(working_set) + 4,
        max_expansions=4,
        max_broad_searches=0,
    )
    write_context(state, root)
    return state


def reset_context(root: Path = ROOT) -> ContextState:
    state = ContextState(None, 0, [], [], [], 0, [], 0, 0, 0, 0)
    write_context(state, root)
    return state


def validate_context(root: Path = ROOT) -> list[str]:
    task_path = active_task_path(root)
    state = load_context(root)
    errors: list[str] = []

    if not task_path:
        if state is None:
            errors.append("ACTIVE_CONTEXT.yaml is missing")
            return errors
        if state.active_task is not None:
            errors.append("idle repository must have active_task: null in ACTIVE_CONTEXT")
        if state.working_set or state.expanded_paths or state.broad_searches:
            errors.append("idle repository must have an empty active context")
        return errors

    if state is None:
        return ["active task requires development-state/ACTIVE_CONTEXT.yaml"]
    if state.active_task != task_path:
        errors.append(f"ACTIVE_CONTEXT task mismatch: {state.active_task!r} != {task_path!r}")

    required_startup = {
        "AGENTS.md",
        "development-state/CURRENT_STATE.yaml",
        "development-state/ACTIVE_WORK.yaml",
        task_path,
    }
    available = set(state.working_set) | set(state.expanded_paths)
    missing_startup = sorted(required_startup - available)
    if missing_startup:
        errors.append("context missing startup paths: " + ", ".join(missing_startup))

    required_context = set(_task_list(root, task_path, "required_context"))
    missing_required = sorted(required_context - available)
    if missing_required:
        errors.append("context missing required_context paths: " + ", ".join(missing_required))

    if state.context_tier > state.max_tier:
        errors.append(f"context tier {state.context_tier} exceeds max_tier {state.max_tier}")
    if state.total_files > state.max_files:
        errors.append(f"context files {state.total_files} exceed max_files {state.max_files}")
    if len(state.expanded_paths) > state.max_expansions:
        errors.append(
            f"context expansions {len(state.expanded_paths)} exceed max_expansions {state.max_expansions}"
        )
    if state.broad_searches > state.max_broad_searches:
        errors.append(
            f"broad searches {state.broad_searches} exceed max_broad_searches {state.max_broad_searches}"
        )
    if len(state.expansion_log) != len(state.expanded_paths):
        errors.append("every expanded path must have exactly one expansion-log reason")
    if len(state.broad_search_log) != state.broad_searches:
        errors.append("every broad search must have exactly one broad-search-log reason")
    return errors


def context_health(state: ContextState | None, errors: list[str]) -> tuple[str, str]:
    if errors or state is None:
        return "RED", "RECONCILE CONTEXT STATE before continuing"
    if state.active_task is None:
        return "RED", "START FRESH SESSION for the next task"

    file_ratio = state.total_files / state.max_files if state.max_files else 1.0
    expansion_ratio = (
        len(state.expanded_paths) / state.max_expansions if state.max_expansions else 0.0
    )
    if file_ratio >= 0.75 or expansion_ratio >= 0.75 or state.context_tier >= state.max_tier:
        return "YELLOW", "CHECKPOINT SOON before expanding context further"
    return "GREEN", "CONTINUE with the current bounded working set"


def print_context(root: Path = ROOT) -> int:
    state = load_context(root)
    errors = validate_context(root)
    health, recommendation = context_health(state, errors)

    print("Context Working Set")
    print("--------------------------------------------")
    if state is None:
        print("State               MISSING")
    else:
        print(f"Active task         {state.active_task or 'IDLE'}")
        print(f"Context tier        {state.context_tier}/{state.max_tier}")
        print(f"Working files       {state.total_files}/{state.max_files}")
        print(f"Expansions          {len(state.expanded_paths)}/{state.max_expansions}")
        print(f"Broad searches      {state.broad_searches}/{state.max_broad_searches}")
    print(f"Context health      {health}")
    print(f"Recommendation      {recommendation}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


def add_expansion(path: str, reason: str, root: Path = ROOT) -> ContextState:
    state = load_context(root)
    if state is None or state.active_task is None:
        raise RuntimeError("no active context to expand")
    if path in state.working_set or path in state.expanded_paths:
        return state
    if len(state.expanded_paths) + 1 > state.max_expansions:
        raise RuntimeError("context expansion budget exhausted; checkpoint or explicitly revise the budget")
    if state.total_files + 1 > state.max_files:
        raise RuntimeError("context file budget exhausted; checkpoint or explicitly revise the budget")
    if state.max_tier < 3:
        raise RuntimeError("dependency expansion requires max_tier >= 3")
    state.context_tier = max(state.context_tier, 3)
    state.expanded_paths.append(path)
    state.expansion_log.append(f"{path} :: {reason}")
    write_context(state, root)
    return state


def record_broad_search(reason: str, root: Path = ROOT) -> ContextState:
    state = load_context(root)
    if state is None or state.active_task is None:
        raise RuntimeError("no active context")
    if state.max_tier < 4:
        raise RuntimeError("Tier 4 investigation is not authorized by this context budget")
    if state.broad_searches + 1 > state.max_broad_searches:
        raise RuntimeError("broad-search budget exhausted")
    state.context_tier = 4
    state.broad_searches += 1
    state.broad_search_log.append(reason)
    write_context(state, root)
    return state
