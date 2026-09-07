# Repo Development Framework

A small, reusable repository structure for disciplined agent-assisted software development.

The framework keeps project intent, current development state, task scope, and validation evidence separate so work can move between developers or coding agents without repeatedly rediscovering the repository.

## What it provides

- a short root entry point for coding agents
- a clear split between design truth and current implementation state
- bounded task contracts
- context and token-budget rules
- a repeatable plan → implement → validate → review → handoff loop
- project blueprint and flow tracking
- lightweight Git and pull-request conventions

## Core rule

Do not code an unresolved design decision.

When a task reaches an unknown, first search the project's existing knowledge. Escalate only decisions that genuinely require a maintainer.

## Repository layout

```text
AGENTS.md                  Agent entry point and operating rules
docs/                      Long-lived project knowledge
development-state/         Current project and milestone state
tasks/                     Small, bounded units of work
scripts/                   Local validation helpers
.github/                   Pull request and issue conventions
```

## Getting started

1. Copy this repository or use it as a template.
2. Replace the example project information in `docs/` and `development-state/`.
3. Keep `AGENTS.md` short. Put durable project knowledge in `docs/` instead.
4. Create work as a task contract before implementation begins.
5. Update current state and leave a handoff after meaningful checkpoints.

See [`docs/development/WORKFLOW.md`](docs/development/WORKFLOW.md) for the development loop and [`docs/development/CONTEXT_POLICY.md`](docs/development/CONTEXT_POLICY.md) for context-budget rules.

## Status

Early public draft. The structure is intentionally small and expected to evolve through real project use.

## License

MIT
