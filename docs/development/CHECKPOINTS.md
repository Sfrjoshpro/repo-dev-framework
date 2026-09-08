# Checkpoints and Handoffs

Checkpoints exist to make repository state recoverable without rereading an entire work session.

Create a checkpoint when:

- a task reaches a meaningful implementation boundary
- validation changes the understanding of the problem
- work becomes blocked
- another contributor or session may continue the task
- a pull request is ready for review or merge

A checkpoint should record:

- task and branch
- what changed
- validation run and its result
- unresolved unknowns or blockers
- the smallest valid next action
- relevant paths

Use `development-state/HANDOFF_TEMPLATE.yaml` as the shape for handoff records. Store completed handoffs under `development-state/handoffs/` using a task-and-date based filename.

## Decision records

Use an ADR when a durable architecture or development-policy decision is made. Do not use ADRs for routine implementation details.

Proposed decisions may be recorded before implementation. Accepted decisions become part of design truth. If a decision is reversed, supersede the original ADR rather than silently rewriting history.

## Completion evidence

A task may move to `done` only when:

- requested behavior is implemented
- listed validation has passed
- final diff has been reviewed against scope
- current state is updated
- unresolved unknowns that block completion are resolved
- a handoff or checkpoint exists when future work needs continuation context

The repository validator may reject a completed task when this evidence is missing.
