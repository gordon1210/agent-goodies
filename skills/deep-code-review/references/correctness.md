# Correctness

## Contents

- Contract and invariants
- Inputs and boundaries
- State and lifecycle
- Errors and cleanup
- Collections and ordering
- Time and numeric behavior
- Parsing and serialization
- Configuration and generated behavior
- Verification

## Contract and invariants

State the in-scope behavior's invariant before looking for patterns.

Check whether the implementation:

- fulfills every explicit acceptance criterion, including negative requirements
- preserves caller-visible behavior not intentionally changed
- returns, persists, emits, and acknowledges the same logical outcome
- handles every supported state transition exactly once
- keeps validation and execution based on the same canonical value
- maintains relationships among fields rather than validating each field independently
- avoids partial success being reported as complete success

Use existing tests and callers to discover implicit contracts, but prefer explicit product and protocol requirements when they conflict.

## Inputs and boundaries

Select reachable boundary classes:

- absent versus present-but-empty
- zero, negative, minimum, maximum, and one beyond boundary
- duplicate or repeated input
- malformed, truncated, partial, or unexpected-but-valid input
- single item versus multiple items
- first/last page or index
- exact threshold versus just below/above
- normalized versus non-normalized representation

Inspect in-scope defaults carefully:

- `false`, `0`, empty string, empty collection, and `null` may be valid values
- `x || default` may differ from `x ?? default`
- omitted fields may differ from explicitly null fields
- an empty update may mean no-op, clear, or invalid depending on contract

Do not enumerate impossible cases excluded by a verified type/schema/constructor.

## State and lifecycle

Trace object/job/request lifecycle from creation to terminal state.

Look for:

- invalid or skipped transitions
- repeated completion, cancellation, acknowledgment, or cleanup
- state updated before an operation that can fail, leaving a false success state
- side effect completed before durable state needed for retry/idempotency
- stale state reused after refresh, reconnect, navigation, or retry
- mutation of shared data through aliases or cached references
- lifecycle callbacks registered twice or never removed
- terminal states that still accept work
- initialization order and use before ready
- shutdown order and work accepted after shutdown begins

For state machines, compare every in-scope transition against allowed predecessor and successor states.

## Errors and cleanup

Trace failures at each step that can fail, especially around side effects.

Check:

- swallowed, overwritten, or incorrectly converted errors
- success returned from a failure path
- broad catch/recover blocks that hide corruption or cancellation
- retrying permanent errors or failing to retry transient ones under the established contract
- cleanup skipped by early return, panic/exception, cancellation, or partial initialization
- cleanup that masks the original error
- double close/release/rollback
- resource ownership unclear after transfer or partial success
- transaction committed despite a failed required sub-operation
- response/ack sent before durable completion

Do not insist every error be propagated. Verify the intended error boundary and fallback semantics.

## Collections, ordering, and pagination

Inspect:

- off-by-one and inclusive/exclusive range mistakes
- unstable or inconsistent comparators
- sorting that mutates shared input unexpectedly
- iteration while mutating the same collection
- duplicate collapse or deduplication with the wrong identity key
- map/set key equality and normalization
- missing deterministic ordering where consumers rely on it
- pagination cursor derived from non-unique or mutable fields
- filtered page sizes causing skips or duplicates
- aggregation over empty input
- batching that drops remainder or changes error behavior

A nondeterministic order is only a finding when the contract or downstream behavior requires stability.

## Time and numeric behavior

Check:

- seconds versus milliseconds, bytes versus elements, percentages versus fractions
- integer width, overflow, underflow, truncation, and signedness
- floating-point equality and accumulation where precision matters
- money represented and rounded according to the established contract
- local time versus UTC, timezone conversion, daylight-saving transitions
- calendar duration versus elapsed duration
- wall clock used for ordering/timeouts where monotonic time is required
- expiry boundary (`<` versus `<=`) and clock skew
- parsing ambiguous date/number formats
- negative duration or timeout behavior

Do not report generic floating-point concerns without a violated tolerance or financial/data invariant.

## Parsing and serialization

Trace round trips and version boundaries.

Check:

- missing/unknown fields and default behavior
- `null` versus absent and zero-value omission
- enum additions and unknown-value handling
- duplicate fields/keys and parser precedence
- case sensitivity and normalization
- precision or type loss during encode/decode
- binary length/tag/version validation
- partial input accepted as complete
- serializer output that consumers cannot parse
- changed field names, tags, aliases, or casing
- validation applied before a later transformation changes meaning

When parser/library semantics are uncertain, verify them rather than infer from API names.

## Configuration, flags, and generated behavior

Check:

- defaults for missing environment/config values
- precedence among CLI, environment, file, remote config, and hardcoded default
- boolean/string parsing and whitespace/case handling
- feature flag behavior for on, off, missing, stale, and mixed-version states
- configuration read at build time versus runtime
- generated files matching their source/schema/template
- source and generated artifacts being out of sync
- stale caches or code generation not invalidated
- debug/test configuration accidentally becoming production default

A configuration option is part of a contract when deployment or users depend on it.

## Verification

For each correctness candidate, provide:

- the intended invariant
- a concrete reachable input/state
- the exact mode-appropriate cause: changed cause for `change_review`, current in-scope cause for `full_audit`
- the resulting wrong value, state, side effect, or error
- guards and callers checked
- for `change_review`, evidence that the base behavior did not have the defect or that the change newly exposes it; `full_audit` has no base-introduction requirement

Prefer a focused existing test or small reproduction when safe. A failed broad test suite without a causal trace is not enough by itself.
