# Compute Market Routing Contract

## Purpose

The framework should minimize the total cost of producing **verified useful development work** while preserving user-selected quality, time, risk, privacy, and budget constraints.

The developer owns the workflow, project state, policies, benchmarks, and evidence. Model providers, local models, subscription products, CI, and deterministic tools are replaceable compute resources.

The framework must not optimize for the cheapest token in isolation. It must optimize for the cheapest reliable path to a verified result.

## Core principles

1. **User-owned workflow** — provider choice must not become project architecture.
2. **Deterministic first** — use Git, parsers, tests, linters, local scripts, and other non-LLM computation when they can reliably perform the step.
3. **Cheapest sufficient intelligence** — use the least expensive qualified resource expected to complete the step reliably.
4. **Verified cost, not token price** — include failed attempts, retries, escalation, validation, and rework when comparing routes.
5. **Risk-aware routing** — high-impact architecture, security, data-loss, migration, or concurrency work may justify stronger reasoning immediately.
6. **Market-aware, never market-owned** — model names and prices are mutable market data, not hard-coded workflow roles.
7. **Evidence over marketing** — provider metadata informs eligibility; observed project results inform routing quality.
8. **Fail safe** — stale prices, unavailable providers, missing credentials, unsupported automation, or uncertain capabilities must degrade to explicit safe behavior rather than guessed routing.

## Optimization objective

For each development step, the router should minimize expected total cost to a result that passes the required verification threshold.

Conceptually:

`expected verified cost = attempt cost + expected retry cost + expected escalation cost + expected validation cost + expected rework cost`

The decision is constrained by:

- minimum quality/confidence
- maximum risk
- time/latency preference
- hard and soft monetary budgets
- privacy/data-placement policy
- provider/resource availability
- task/tool capability requirements
- context-window and input-size requirements
- user or organization restrictions

A cheaper model that frequently fails may be a worse route than a more expensive model that succeeds once.

## Compute resource classes

The framework should reason about capabilities, not permanent model names. Logical roles may include:

- `deterministic_tool`
- `local_worker`
- `economy_model`
- `standard_coder`
- `strong_reasoner`
- `frontier_reviewer`
- `specialized_model`

Current providers/models are mapped into these roles by the market catalog and qualification evidence. A role may have multiple eligible resources and may change providers without changing task contracts.

## Resource inventory

The system may consider resources the user has explicitly made available, including:

- deterministic local scripts and tools
- CI runners
- local CPU/GPU models
- metered model APIs
- supported provider batch/flex/priority modes
- subscription products **only when a supported automatable interface exists and its terms permit the intended use**

A paid subscription is not interchangeable with API credit. The framework must not pretend subscription capacity is programmatically available when it is not.

## Market catalog

The framework should maintain a machine-readable catalog for candidate resources. Model/provider entries should support, when known:

- provider identifier
- model identifier and version/alias information
- status: candidate, qualified, active, deprecated, unavailable
- pricing units and currency
- input price
- cached-input price
- output price
- batch/flex/priority pricing where applicable
- context/input/output limits
- reasoning modes or effort controls
- tool/function calling support
- structured-output support
- multimodal capabilities
- code-related capabilities
- latency class or measured latency
- rate/concurrency limits when known
- geographic/data-placement constraints when relevant
- provider source URLs or source identifiers
- `observed_at`
- `effective_at` when supplied by the provider
- refresh/freshness state
- normalized capability tags
- benchmark qualification state

Unknown values must remain unknown. The system must not invent a capability or price to make routing possible.

## Market freshness and provenance

Market information changes independently of repository releases. The catalog therefore needs freshness and provenance rules.

Preferred source order:

1. provider-supported machine-readable pricing/capability metadata when available
2. official provider API/model documentation
3. official provider pricing documentation
4. explicitly configured trusted secondary source only when official data is unavailable

Every externally refreshed value should record provenance and observation time.

The router should define freshness thresholds by data class. Pricing and availability generally require tighter freshness than stable capability metadata.

When price/capability data is stale beyond policy:

- do not silently assume it is current
- mark the candidate stale
- either refresh, use a still-fresh qualified candidate, or require an explicit fallback policy
- preserve the last-known value for audit/history without presenting it as current

Market refresh must be separable from routing so a provider-page change cannot immediately redirect important work without qualification.

## Candidate qualification

A newly discovered model must not automatically become a trusted development worker.

Candidate progression:

`discovered -> metadata-valid -> benchmarked -> qualified -> active`

Qualification should consider:

- compatibility with required tools/interfaces
- successful structured output when required
- task-class benchmark results
- reliability/error rate
- latency
- cost
- validation success
- safety/privacy policy compatibility

A new low-price model may enter the catalog immediately but should route real work only after it satisfies the configured qualification threshold.

## Development task classification

Before model selection, the framework should classify the current step using repository evidence. Classification may include:

- deterministic/mechanical
- retrieval/orientation
- summarization/transformation
- straightforward implementation
- test generation
- refactor with strong tests
- debugging
- concurrency/distributed-state debugging
- architecture/design
- migration/data-loss-risk work
- security-sensitive work
- final review/audit

Classification should also estimate:

- reversibility
- blast radius
- quality threshold
- available automated verification
- expected context size
- expected output size
- failure cost
- latency sensitivity

The classification must be persisted or auditable enough to explain why a route was selected.

## User compute policy

Routing is governed by user/project policy, not provider defaults.

The policy model should support at least:

- optimization mode: `economy`, `balanced`, `quality`, or custom
- hard spend limit per task/session/day/month or configured accounting period
- soft warning thresholds
- minimum quality for task classes
- deterministic-first preference
- local-compute preference
- allowed/blocked providers
- data/privacy restrictions
- maximum automatic escalation level
- approval requirements above a cost/risk threshold
- latency preference
- whether experimental/candidate models are permitted

The default intent should be equivalent to:

> Minimize verified cost without materially reducing correctness or increasing project risk.

## Routing behavior

A routing decision should proceed in this order:

1. determine whether the step can be completed deterministically
2. classify task/risk/verification characteristics
3. determine the minimum required capability role
4. filter resources by availability, policy, privacy, tools, context capacity, and freshness
5. estimate cost for the expected input/output and any known cached portion
6. combine estimated cost with observed success/retry/escalation history for the task class
7. choose the best expected-value candidate under policy
8. execute the attempt
9. run required verification
10. record outcome and actual usage/cost when available
11. finish on success or escalate according to policy

The router must be able to explain the selected route in terms meaningful to a developer: task class, risk, policy, candidate eligibility, expected cost, evidence, and escalation boundary.

## Escalation ladder

The framework should not automatically begin every step with frontier reasoning, and it should not repeatedly waste cheap attempts when evidence shows they are poor fits.

A route may progress conceptually as:

`deterministic -> economy -> standard -> strong -> frontier/specialist`

but the starting level depends on task evidence.

Examples:

- low-risk code with strong tests may begin cheaply
- architecture changes without executable verification may begin with a strong reasoner
- task classes with poor historical economy-model performance may skip the economy tier
- a failed attempt may retry at the same tier only when failure evidence suggests the route remains reasonable

Escalation should be triggered by evidence such as:

- verification failure
- explicit uncertainty
- unsupported capability
- repeated tool failure
- exceeded retry threshold
- task reclassification showing higher risk/complexity

Every paid failed attempt remains part of the verified-cost history.

## Verification and completion

A route is successful only when the task's required verification succeeds or the configured human-review requirement is satisfied.

Model self-confidence alone is not verification.

Verification sources may include:

- tests
- type/lint/static checks
- task guards
- repository health
- deterministic comparisons
- schema validation
- benchmark graders
- human approval when required

The router must not learn that an attempt was successful merely because the model returned an answer.

## Cost accounting

Cost records should distinguish:

- input tokens/units
- cached input
- output tokens/units
- reasoning or provider-specific billable units when exposed
- tool charges when applicable
- batch/flex/priority mode
- local compute estimates when configured
- attempt number
- failed/retried/escalated status
- validation cost
- total cost to verified completion

Provider invoices remain authoritative for billing. Framework accounting is routing/audit data and should retain enough provenance to reconcile differences.

The primary optimization metric is **cost per verified result** by task class, not raw token price.

## Empirical performance history

The framework should build a user/project-owned evidence store from real completed work.

For a resource and task class, useful measurements include:

- attempts
- first-pass verified success rate
- eventual success rate
- average retries
- average escalation rate
- average input/output size
- average actual cost
- average total verified cost
- latency
- tool-call reliability
- validation failure categories
- sample size and recency

Routing must account for sample size and recency. A single successful task is not sufficient evidence to declare a model best.

Project-local evidence may override generic benchmark preference when it is sufficiently strong and applicable.

## Benchmarking new market entrants

Automatic market awareness must not mean automatic production trust.

A new or materially changed model should be evaluated against a bounded benchmark suite representative of the developer's workload. Benchmarks should favor tasks with objective verification.

The system may compare:

- verified success
- verified cost
- first-pass success
- latency
- tool reliability
- context handling
- failure modes

Promotion into normal routing should require a configured evidence threshold.

A provider price change can update cost calculations immediately when provenance is fresh, but a model capability/behavior change should not erase historical qualification evidence without version awareness.

## Budget behavior

The router should remain useful as budget changes.

Example policy behavior:

- healthy budget: normal balanced routing
- soft threshold reached: prefer deterministic/local/economy routes more aggressively and surface warning state
- near hard limit: strong models only for blockers or policy-defined high-risk work
- hard limit reached: stop metered execution unless the user explicitly changes the budget; continue deterministic/local or otherwise authorized zero-metered-cost work

The system must never silently exceed a hard user budget.

## Privacy and credentials

Provider credentials are runtime secrets and must not be committed to project state.

Routing metadata may name configured provider profiles but should not contain API keys, session cookies, passwords, or other secrets.

The router must filter candidates against privacy/data-placement policy before cost optimization. A cheaper disallowed provider is not an eligible candidate.

## Auditability

Every automated route should be explainable after the fact.

An execution record should be able to answer:

- what development step was attempted?
- what task class and risk were assigned?
- what context set was used?
- which resources were eligible and ineligible, and why?
- which resource was selected?
- what market data/pricing snapshot informed the choice?
- what was the expected cost?
- what was the actual reported usage/cost when known?
- what validation ran?
- did the attempt pass, retry, or escalate?
- what was the final total cost to verified completion?

This evidence belongs to the user and should remain portable across providers.

## Failure and fallback behavior

The router must stop or fall back explicitly when:

- no qualified candidate satisfies policy
- required pricing is stale and policy requires fresh pricing
- provider availability cannot be established
- credentials are missing
- budget is exhausted
- task classification is too uncertain for safe automatic routing
- required verification is unavailable for a policy that demands it

Fallback must never silently downgrade a quality/privacy/risk requirement.

## Vendor independence

The durable architecture must not encode statements such as "Model X is the coding model." It should encode capability and policy roles.

Provider/model adapters translate market-specific interfaces into framework capabilities. Task contracts and project workflow remain unchanged when provider rankings change.

The intended ownership boundary is:

**User owns**
- project knowledge
- task/scope state
- context state
- compute policy
- market-history snapshots
- benchmark results
- verified-cost history
- routing evidence

**Provider supplies**
- interchangeable compute and provider-specific capability/pricing metadata

## Relationship to context control

Context and compute optimization are complementary.

The context working-set system minimizes what information must be sent/read. The compute router minimizes which resource performs the work and how much intelligence is purchased.

A routing estimate should consume the bounded active-context size rather than assuming whole-repository context.

## Future implementation boundaries

This contract intentionally precedes implementation. Likely future milestones should remain independently bounded, for example:

1. compute policy schema
2. provider/model market catalog schema
3. official-source refresh adapters and freshness validation
4. usage/cost accounting
5. task classification contract
6. deterministic-first candidate selection
7. provider/model routing and escalation
8. benchmark qualification and empirical performance store
9. local-compute/resource inventory integration
10. user-facing reporting and budget controls

These are implementation directions, not permission to implement them in V10.

## Acceptance criteria for future implementations

A future compute-routing implementation satisfies this contract only if it can demonstrate that:

- changing the best-value provider does not require changing project workflow semantics
- stale market data is visible and handled by policy
- hidden/unknown prices or capabilities are not fabricated
- hard budgets are respected
- deterministic work can bypass paid LLM execution
- failed attempts are included in total verified cost
- validation determines success
- escalation is evidence-driven
- routing decisions are auditable
- user/project evidence can influence future routing
- provider credentials remain outside repository state
- the user can disable a provider or automatic escalation

The long-term goal is simple: the developer states what should be built; the framework continuously chooses the most cost-effective reliable way to move the repository toward that goal without surrendering workflow ownership to any AI vendor.
