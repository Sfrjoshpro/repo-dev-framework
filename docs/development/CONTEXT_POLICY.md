# Context Policy

Repository context is a budget, not a collection target.

## Default startup set

Load only:

1. `AGENTS.md`
2. `development-state/CURRENT_STATE.yaml`
3. `development-state/ACTIVE_WORK.yaml`
4. the named active task
5. `development-state/ACTIVE_CONTEXT.yaml`

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

## Machine-readable working set

`development-state/ACTIVE_CONTEXT.yaml` persists the current task's working set and budget. It records:

- the active task
- current context tier
- baseline working paths
- justified dependency expansions
- broad-search count and reasons
- maximum tier, total paths, expansions, and broad searches

After a task is activated, initialize its context before implementation:

```text
python -m repo_framework context init
```

Inspect the current budget at any time:

```text
python -m repo_framework context
```

Before reading a direct dependency outside the current working set, record it first:

```text
python -m repo_framework context add path/to/file --reason "direct dependency required by X"
```

Tier 4 investigation is disabled by default. If a task genuinely requires broad exploration, the context budget must be explicitly revised first and the search must be recorded:

```text
python -m repo_framework context broaden --reason "evidence shows the failure crosses the current boundary"
```

When the repository returns to idle, clear the active context:

```text
python -m repo_framework context reset
```

The task guard and repository health check validate this state. An active task with a missing, mismatched, or over-budget context is not healthy.

## Rules

- Do not read an entire docs tree "just in case."
- Do not read an entire source tree at session start.
- Prefer indexes, state files, and targeted search over broad scans.
- Avoid rereading unchanged files when an adequate current summary exists.
- Summarize findings before expanding to a wider scope.
- Record dependency expansion before reading the new path.
- Treat a context-budget increase as visible scope growth, not an invisible convenience.
- Split oversized tasks instead of compensating with ever-larger context.

Token efficiency is a design constraint: better project structure should reduce the amount of repository text required to make a correct change.
