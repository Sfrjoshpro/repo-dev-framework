# Repository Health

Run the repository health check with:

```text
python -m repo_framework check
```

The command is intentionally standard-library only. It checks persisted repository state rather than attempting to infer hidden model context or token usage.

## What it checks

- required framework files exist
- active work has a valid lifecycle state
- active work and the active task agree on status and allowed paths
- completed tasks contain all required completion evidence
- recorded checkpoints have a matching handoff file
- blueprint edges and flow steps point to existing blueprint nodes
- unresolved unknowns are surfaced

`scripts/check_repo_state.py` remains as a compatibility entry point and runs the same health check.

## Context health

The context indicator is an operational recommendation, not a measurement of ChatGPT token count.

- `GREEN` — an active task is coherent; continue the current chat
- `YELLOW` — work is validating or blocked; persist a checkpoint and consider a fresh chat after the boundary
- `RED` — no task is active; begin the next milestone or task in a fresh chat

A long conversation can still be useful when it stays on one task. A short conversation can still be poor context when it mixes unrelated work. The repository therefore uses milestone/task boundaries and recoverability as the visible signal.

## Why this exists

The repository is intended to be durable project memory. A fresh agent should be able to reconstruct the current development situation from repository state instead of requiring the complete history of previous chats.

Health validation is meant to catch contradictions before handoff. It does not prove that implementation behavior is correct; task-specific tests remain responsible for that.
