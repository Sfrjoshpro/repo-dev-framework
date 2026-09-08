# Blueprint Visualization Contract

This document defines the durable behavior contract for visualizing the repository project model.

The canonical project model remains `development-state/blueprint/project-model.yaml`. A visualization is a read-only presentation of that model. It must not become a second source of truth, infer undocumented architecture from source code, or redefine node, edge, flow, or status semantics.

## Purpose

The visualization exists to make the machine-readable project model easier to use for:

- project orientation
- architecture navigation
- dependency inspection
- user, logic, and data-flow inspection
- implementation-status awareness
- bounded context selection
- debugging and handoff support

The visualization should help a developer or agent answer practical questions with less repository scanning. It should not encourage loading the entire repository when a smaller context set is sufficient.

## Source-of-truth boundary

The visualization consumes the project model as authored.

It must:

- use stable model IDs as identity
- present only node types defined by the model
- present only edge types defined by the model
- present only flow types defined by the model
- present only status values defined by the model
- preserve edge direction
- preserve flow step order
- preserve explicit paths, requirement references, test references, responsibilities, tags, flow entry nodes, and flow outcomes when those fields are present
- expose missing or unknown model information as missing or unknown rather than inventing values

It must not:

- write changes back into the project model as part of this contract
- derive new project-model semantics from directory layout or source-code inspection
- synthesize dependency relationships that are not represented by model edges
- treat display names as identity when stable IDs exist
- reinterpret project-model status as Git branch, pull-request, CI, or runtime status

## Supported model vocabulary

The visualization must be able to represent the vocabulary already defined by the project model.

### Node types

- `system`
- `component`
- `module`
- `file`
- `requirement`
- `test`
- `external`

### Edge types

- `contains`
- `depends_on`
- `routes_to`
- `reads`
- `writes`
- `constrains`
- `implements`
- `verifies`
- `triggers`

### Flow types

- `user`
- `logic`
- `data`

### Status values

- `unknown`
- `designed`
- `planned`
- `implementing`
- `verified`
- `blocked`

No visualization-specific status vocabulary is introduced by this contract.

## Required views

A conforming visualization must support three conceptual views. They may be rendered in any future interface, but the behavior must remain the same.

### Project overview

The project overview presents the highest useful level of the modeled project without requiring every node to be visible at once.

The overview must allow a user to identify:

- major modeled systems
- their current model status
- directly modeled high-level relationships
- important flows available for inspection

The overview should prefer the smallest useful representation of the project. Lower-level nodes may remain hidden until they are relevant or explicitly requested.

### Focused architecture view

Selecting or focusing a node must make its local modeled context inspectable.

At minimum, the focused view must be able to expose:

- stable node ID
- node type
- human-readable name
- model status
- responsibility
- repository paths
- requirement references
- test references
- tags when present
- incoming explicit edges
- outgoing explicit edges
- flow membership when the node participates in a modeled flow

The focused view must distinguish relationship direction so that, for example, `A depends_on B` is not presented as equivalent to `B depends_on A`.

### Flow view

A flow view must present modeled user, logic, or data flows independently from the architecture dependency layout.

For a selected flow it must expose:

- stable flow ID
- flow name
- flow type
- flow status
- entry node
- ordered steps
- each step's referenced node
- each step's action
- observable outcome

Flow order must be preserved exactly as modeled. Architecture edges may be shown alongside a flow when useful, but they must not replace or reorder the flow's explicit step sequence.

## Drill-down and zoom behavior

The visualization must support progressive disclosure rather than assuming that all model detail belongs on screen at once.

The intended drill-down direction is:

`project / systems -> components or modules -> files and evidence`

Only levels that actually exist in the model may be shown. The visualization must not fabricate intermediate hierarchy solely to make the display look complete.

When a user drills into a node, the visualization should prioritize:

1. the selected node
2. directly connected modeled relationships
3. directly referenced requirements and tests
4. flow steps that include the node
5. contained or containing nodes when represented by explicit `contains` edges

Broader graph expansion should be deliberate rather than automatic.

## Filtering

A visualization must be able to narrow the presented model using fields already present in the project model.

At minimum, filtering behavior should be definable by:

- node type
- status
- flow
- tag when tags are present

Filtering changes presentation only. It must not change the underlying project model or create new relationships.

## Status presentation

Status must remain visible enough to distinguish model maturity and blockers during navigation.

The visualization must preserve the project model's status value exactly. Any future visual treatment such as icons, labels, grouping, or styling is presentation-only and must not alter meaning.

`unknown` must remain visibly distinct from a missing status field or from `planned`.

`blocked` must remain visibly distinct from incomplete but unblocked states.

## Bounded-context behavior

The visualization is a context-selection aid, not permission to expand implementation scope.

When used for an active task, the expected behavior is:

1. begin from the task's declared `required_context` and approved paths
2. locate matching modeled nodes
3. inspect only directly relevant edges, flow steps, requirements, tests, or containing nodes
4. expand farther only when a concrete dependency requires it

The visualization must not imply that a connected node is automatically authorized for editing.

The active task's `allowed_paths` remains the implementation boundary even when the visualization shows related nodes outside that boundary.

## Selection details and traceability

A selected model element should be traceable back to persisted repository knowledge.

For nodes, the visualization should expose repository paths and requirement/test references exactly as recorded when present.

For edges, it should expose source node ID, target node ID, and edge type.

For flows, it should expose flow ID and the ordered node/action sequence.

If a referenced path or relationship is absent from the model, the visualization must not silently infer one.

## Missing, unknown, and invalid information

The visualization must make uncertainty visible.

A future implementation should distinguish at least these conditions:

- an explicitly modeled `unknown` status
- an optional field that is not present
- a reference that cannot be resolved within the loaded model

This contract does not define repository-health validation behavior. Invalid references remain the concern of existing model and repository validation. A visualization may surface such information, but it must not repair or reinterpret it automatically.

## Read-only interaction boundary

This milestone defines inspection and navigation only.

A future visualization may support interactions such as selecting, focusing, filtering, expanding, collapsing, and switching between architecture and flow views.

Editing nodes, edges, flows, tasks, repository files, or model status is outside this contract. Any future write-back capability requires its own explicit design and task scope.

## Self-hosting acceptance example

The existing self-hosted repository-health subsystem provides a concrete model that a future visualization should be able to present without additional semantics.

A user inspecting `framework.repo_health` should be able to see that it is a verified module, identify its repository path and responsibility, inspect its explicit outgoing `reads` relationships to persisted state and blueprint nodes, inspect its `implements` relationship to persisted-state requirements, and see its participation in the repository-health flow.

A user inspecting `flow.repository_health` should be able to follow the ordered steps from the repository-health module through active work, task contract, blueprint, and back to the health module outcome without the visualization inventing extra runtime steps.

This example is acceptance evidence for the contract only. It does not add or modify project-model content.

## Conformance criteria

A future visualization conforms to this contract when it can:

- load and present the existing project model without changing its semantics
- identify modeled systems and status at project level
- focus a node and inspect its directly modeled context
- preserve edge direction and type
- preserve flow type and ordered step sequence
- progressively reveal lower-level modeled detail
- filter presentation by existing model fields
- keep unknown or missing information explicit
- support bounded context selection without overriding task `allowed_paths`
- trace presented elements back to stable model IDs and persisted references

## Explicit non-goals

This contract does not:

- implement a web, desktop, IDE, or terminal visualization
- select a frontend framework
- select a graph library
- select a rendering engine
- select a transport protocol
- define automatic source-code graph or dependency extraction
- change project-model node, edge, flow, or status semantics
- change repository-health behavior
- change task-guard behavior
- define blueprint editing or write-back
- define the next development milestone
