# Design and Maintainability

Use this module for broad refactors, new abstractions, ownership/layering changes, or duplicated policy. It is not a license for taste-based comments.

## Reportability threshold

A design finding must show a concrete consequence such as:

- a domain/security invariant can now be bypassed
- two code paths will produce divergent externally visible behavior
- ownership/lifecycle is ambiguous enough to cause leak, double action, or stale state
- a public abstraction cannot express a required supported case
- dependency direction creates an actual initialization, build, or deployment cycle
- duplicated policy already differs or the change updates only one reachable copy
- the design makes safe rollback/compatibility impossible under the evidenced rollout model
- hidden global state causes cross-request/test/tenant interference

“More elegant,” “cleaner,” “too many lines,” or “I would extract this” is not enough.

## Boundaries and ownership

Check:

- one clear owner for mutable state and resource lifecycle
- policy enforced at the boundary that owns the protected operation
- domain invariants centralized where all entry points pass through them
- abstractions do not expose partially initialized/invalid states
- responsibilities do not require callers to know undocumented ordering
- server/client, tenant/global, request/process, and library/application state remain separated
- shared helpers do not silently depend on ambient identity/config/transaction

## Abstraction fit

Inspect whether a new abstraction:

- models the real variability rather than one current call site
- preserves error, cancellation, transaction, and authorization context
- avoids boolean/optional combinations that permit invalid states
- has a stable contract independent of implementation leakage
- does not generalize unrelated behaviors under one switch-heavy interface
- does not hide expensive or irreversible effects behind innocent accessors
- supports test doubles without changing semantics

Do not demand abstraction for a single simple use. Premature generalization is not automatically a bug either; show the concrete failure/risk.

## Duplication and divergence

Duplicated code is reportable when the duplicated element is a correctness/security contract and divergence is evidenced or immediately created.

High-value examples:

- authorization rules copied between route and worker, with one missing a role
- currency/rounding logic implemented differently in preview and charge paths
- schema validation copied but one path normalizes after validation
- retry/idempotency policy duplicated with different keys
- serializer/deserializer updated on only one side

Do not report ordinary small duplication without consequence.

## Dependency direction and cycles

Check new dependencies for:

- module/package initialization cycles
- runtime import cycle causing partial values
- domain code depending on transport/UI/infrastructure details that bypass testable policy
- shared package importing application-specific singleton/config
- deployment unit coupling that defeats independent versioning evidenced by the repo
- plugin extension point gaining direct privileged internals

A theoretical layering violation is a suggestion unless it causes an observable build, lifecycle, testing, security, or compatibility problem.

## Simplicity

Flag accidental complexity only when it creates a defect path or makes a required invariant unverifiable:

- multiple sources of truth
- hidden side effects
- implicit fallthrough/default allow
- state encoded through unrelated booleans
- recursive/reentrant flow without bounds
- abstraction requiring caller-specific exceptions
- generalized framework replacing a direct operation while changing semantics

Prefer the narrowest fix that restores the invariant. Do not turn review into a rewrite proposal.

## Verification

Trace all entry points through the abstraction or duplicated policy. Compare contracts, errors, state, and side effects. A design finding should cite at least one concrete present failure or an unavoidable supported-case failure, not a hypothetical future maintenance concern.
