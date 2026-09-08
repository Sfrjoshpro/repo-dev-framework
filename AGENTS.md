# Repository Instructions

This file is the entry point for coding agents. Keep it short.

## Start here

Read, in order:

1. `development-state/CURRENT_STATE.yaml`
2. `development-state/ACTIVE_WORK.yaml`
3. the active task file, if one is named
4. only the project docs required by that task

Do not scan the entire repository by default.

## Working rules

- Treat `docs/` as design truth.
- Treat `development-state/` as current implementation truth.
- Treat the active task as the scope contract.
- Search existing project knowledge before asking for a design decision.
- Do not implement unresolved assumptions.
- Do not start implementation until the task is `ready` and active work is recorded.
- Do not edit outside `allowed_paths`; if another path is required, stop and update the task contract first.
- Do not refactor unrelated code while completing a task.
- Prefer the smallest coherent change that satisfies the task.
- Run the task's listed validation before declaring it complete.
- Run `python scripts/task_guard.py --task <task-file>` before implementation and again before handoff.
- Review the final diff for accidental scope growth.
- Update current state and handoff notes when a checkpoint changes project understanding.

## Source of truth

If two documents conflict, do not guess. Record the conflict in the active task or blocker state and resolve it before implementation continues.
