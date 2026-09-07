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
approved task scope
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

## 3. Bound the change

A task should define its goal, allowed area, non-goals, expected validation, and known dependencies.

## 4. Implement

Prefer a narrow change over opportunistic cleanup. If new work is discovered, record it separately unless it blocks the current task.

## 5. Validate

Run the task's checks. Validation should prove the requested behavior, not just compilation or import success.

## 6. Review

Review the diff against the task contract. Look for scope growth, undocumented assumptions, accidental API changes, and missing tests.

## 7. Persist state

Update `development-state/` when the repository's actual state changes. Leave a handoff when another session or contributor may need to continue the work.
