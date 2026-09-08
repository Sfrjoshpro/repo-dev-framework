# Project Model

The project model is the machine-readable map used for planning, navigation, debugging, scope selection, and handoff.

Its source lives at `development-state/blueprint/project-model.yaml`.

## What to model

Model enough detail to answer practical development questions without forcing a whole-repository scan:

- major systems and responsibilities
- components, modules, and important files
- dependency direction
- requirements and the code that implements them
- tests or checks that verify those requirements
- important user flows
- important runtime, logic, or data flows
- persistence boundaries and external interfaces
- current implementation status

Do not try to model every function. Add detail when it improves planning, debugging, ownership, or context selection.

## Nodes

Each node has a stable `id` and a `type`.

Supported node types are:

- `system`
- `component`
- `module`
- `file`
- `requirement`
- `test`
- `external`

A useful node records:

- `id`
- `type`
- `name`
- `status`
- `responsibility`
- relevant repository `paths`
- `requirement_refs`
- `test_refs`
- optional `tags`

Stable IDs matter more than display names because edges, flows, tasks, and future tooling should reference IDs.

## Edges

Edges describe directed relationships between nodes. Keep them explicit rather than relying on folder proximity.

Supported edge types are:

- `contains`
- `depends_on`
- `routes_to`
- `reads`
- `writes`
- `constrains`
- `implements`
- `verifies`
- `triggers`

Use the narrowest relationship that explains why one node is relevant to another.

## Flows

Flows describe behavior across multiple nodes. They are intentionally separate from dependency edges because architecture structure and runtime/user sequence are different concerns.

Supported flow types are:

- `user`
- `logic`
- `data`

Each flow should define:

- stable `id`
- human-readable `name`
- `type`
- `status`
- `entry` node
- ordered `steps`
- observable `outcome`

A step references a node ID plus a short action. This makes a flow useful at multiple zoom levels: a UI may show only systems at first, then reveal modules or files as the user drills down.

## Status

The shared status vocabulary is:

- `unknown`
- `designed`
- `planned`
- `implementing`
- `verified`
- `blocked`

Status describes the current confidence or delivery state of the modeled item, not Git branch state.

## Context selection

The blueprint should help an agent narrow context, not justify expanding it.

For an active task:

1. start from the task's `required_context` and approved paths
2. locate the matching blueprint nodes
3. follow only edges or flow steps that are directly relevant
4. inspect broader nodes only when a concrete dependency requires them

The blueprint never overrides the task's `allowed_paths`. It informs understanding; the task contract controls implementation scope.

## Self-hosting

This repository should model itself as the framework evolves. That gives us a real project on which to test whether the blueprint is useful before building visualization or automatic graph extraction.
