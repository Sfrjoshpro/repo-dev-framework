# Context Policy

Repository context is a budget, not a collection target.

## Default startup set

Load only:

1. `AGENTS.md`
2. `development-state/CURRENT_STATE.yaml`
3. `development-state/ACTIVE_WORK.yaml`
4. the named active task

Expand context only when the task requires it.

## Context tiers

### Tier 0 — orientation

Entry instructions and current state.

### Tier 1 — task knowledge

The task contract and directly relevant design documents.

### Tier 2 — implementation surface

Files expected to change and their direct tests.

### Tier 3 — dependencies

Direct callers, callees, interfaces, fixtures, schemas, or configuration needed to reason safely.

### Tier 4 — broader investigation

Repository-wide exploration only when evidence shows the problem crosses the current boundary.

## Rules

- Do not read an entire docs tree "just in case."
- Do not read an entire source tree at session start.
- Prefer indexes, state files, and targeted search over broad scans.
- Avoid rereading unchanged files when an adequate current summary exists.
- Summarize findings before expanding to a wider scope.
- Split oversized tasks instead of compensating with ever-larger context.

Token efficiency is a design constraint: better project structure should reduce the amount of repository text required to make a correct change.
