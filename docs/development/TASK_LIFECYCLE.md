# Task Lifecycle

Tasks move through a small set of explicit states. The purpose is to prevent implementation from starting before the work is understood and bounded.

## States

`backlog`
: Work is known, but has not been prepared.

`clarifying`
: Requirements, dependencies, or unknowns are still being resolved.

`ready`
: Goal, scope, dependencies, unknowns, and validation are sufficiently defined to begin.

`active`
: Implementation is in progress.

`validating`
: Implementation is complete and the task is being tested and reviewed against its contract.

`blocked`
: Progress cannot continue without a dependency, decision, or external change.

`done`
: Implementation, validation, diff review, and required state updates are complete.

## Allowed transitions

```text
backlog -> clarifying
backlog -> ready
clarifying -> ready
clarifying -> blocked
ready -> active
active -> validating
active -> blocked
validating -> active
validating -> blocked
validating -> done
blocked -> clarifying
blocked -> ready
blocked -> active
```

A task must not move directly from `backlog` or `clarifying` to `active`.

## Definition of Ready

A task may enter `ready` when:

- the observable goal is stated
- allowed paths are declared
- non-goals are declared
- dependencies are known enough to proceed
- unresolved design decisions are absent or explicitly isolated
- validation commands or checks are known

An empty `allowed_paths` list means implementation is not authorized.

## Definition of Done

A task may enter `done` only when:

- implementation is complete
- validation passed
- the diff was reviewed against scope
- repository state was updated where required
- no unresolved scope violation remains

## Blocked work

Use `blocked` when the task cannot proceed without changing its contract or resolving a real dependency or decision. Record the blocker rather than silently widening scope.
