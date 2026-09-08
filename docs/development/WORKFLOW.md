# Development Workflow

The default development loop is:

```text
project knowledge
    ↓
understanding check
    ↓
search existing knowledge
    ↓
resolve real unknowns
    ↓
ready task contract
    ↓
activate task + scope
    ↓
implementation
    ↓
validation
    ↓
diff review
    ↓
state update
    ↓
handoff / pull request
```

## 1. Understand

Read the current state, active work, task contract, and only the design documents relevant to the task.

## 2. Resolve unknowns

Search the repository before asking a maintainer. A missing answer is not automatically a new design decision.

If a real design decision remains unresolved, stop implementation for that portion of the work and record it.

## 3. Make the task ready

A task should define its goal, allowed paths, non-goals, expected validation, dependencies, and known unknowns.

Use the lifecycle in `TASK_LIFECYCLE.md`. Implementation begins only after the task reaches `ready`.

## 4. Activate and enforce scope

Record the task in `development-state/ACTIVE_WORK.yaml`, set `lifecycle_state: active`, and copy the approved `allowed_paths` into active work.

An empty `allowed_paths` list does not authorize implementation.

Run:

```text
python scripts/task_guard.py --task tasks/<task>.yaml
```

When validating a branch against a base ref, run:

```text
python scripts/task_guard.py --task tasks/<task>.yaml --base-ref origin/main
```

If a required change falls outside the declared paths, stop and revise the task contract before making the edit. Do not widen scope silently.

## 5. Implement

Prefer a narrow change over opportunistic cleanup. If new work is discovered, record it separately unless it blocks the current task.

## 6. Validate

Move the task to `validating`, run the task's checks, and prove the requested behavior rather than only compilation or import success.

## 7. Review

Review the diff against the task contract. Look for scope growth, undocumented assumptions, accidental API changes, and missing tests. Re-run the task guard against the branch base.

## 8. Persist state

Move the task to `done` only after implementation, validation, diff review, and required state updates are complete. Clear or advance `ACTIVE_WORK.yaml` and leave a handoff when another session or contributor may need to continue the work.
