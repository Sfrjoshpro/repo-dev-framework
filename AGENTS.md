# Repository Instructions

This file is the entry point for coding agents. Keep it short.

## Start here

Read, in order:

1. `development-state/CURRENT_STATE.yaml`
2. `development-state/ACTIVE_WORK.yaml`
3. the active task file, if one is named
4. `development-state/ACTIVE_CONTEXT.yaml`
5. only the project docs/files named by the active context

Do not scan the entire repository by default.

## Working rules

- Treat `docs/` as design truth.
- Treat `development-state/` as current implementation truth.
- Treat the active task as the scope contract.
- Treat `ACTIVE_CONTEXT.yaml` as the current read/working-set budget.
- After activating a new task, run `python -m repo_framework context init` before the pre-implementation guard.
- Before reading an undeclared direct dependency, record it with `python -m repo_framework context add <path> --reason "<why>"`.
- Do not perform Tier 4 broad repository exploration unless the active context explicitly authorizes it; record an authorized broad search with `python -m repo_framework context broaden --reason "<why>"`.
- Search existing project knowledge before asking for a design decision.
- Record durable architecture decisions as ADRs.
- Record unresolved questions in `development-state/UNRESOLVED_UNKNOWNS.yaml` when they block or materially affect work.
- Do not implement unresolved assumptions.
- Do not start implementation until the task is `ready`, active work is recorded, active context is valid, and the task guard passes.
- Do not edit outside `allowed_paths`; if another path is required, stop and update the task contract first.
- Do not refactor unrelated code while completing a task.
- Prefer the smallest coherent change that satisfies the task.
- Run the task's listed validation before declaring it complete.
- Run `python scripts/task_guard.py --task <task-file>` before implementation and again before handoff.
- Review the final diff for accidental scope growth.
- Create a checkpoint/handoff when work is blocked, changes hands, or reaches a meaningful boundary.
- Do not mark a task `done` until completion evidence is recorded.
- Update current state when a checkpoint changes project understanding.
- Reset active context when returning the repository to idle.

## Source of truth

If two documents conflict, do not guess. Record the conflict in the active task or blocker state and resolve it before implementation continues.
