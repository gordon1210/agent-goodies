# Reliability and Performance

## Contents

- Failure containment
- Timeouts, retries, and backoff
- Resource ownership and limits
- Shutdown and recovery
- Backpressure and overload
- Performance proof
- Common high-value patterns
- Verification and calibration

## Failure containment

Trace how a failure propagates across request, worker, service, and process boundaries.

Check:

- one malformed item failing an entire batch unexpectedly
- panic/exception crossing the intended isolation boundary
- partial response or partial durable state treated as success
- fallback returning stale/unsafe data beyond its contract
- circuit breaker or health state shared too broadly
- fatal process exit from a recoverable request/job error
- supervisor restart loops
- error handling that loses enough context to retry or compensate safely
- health/readiness reporting success while required dependencies or initialization are unavailable

Do not demand isolation when fail-fast is explicitly the correct invariant.

## Timeouts, retries, and backoff

For every remote/blocking operation changed, inspect:

- connection, request, idle, and total timeout semantics
- cancellation propagation
- retryable status/error classification
- maximum attempts and total time budget
- exponential backoff, cap, and jitter where many clients may synchronize
- honoring server retry hints where required
- retry of non-idempotent operations
- nested retries multiplying attempts
- timeout shorter than normal operation or longer than caller budget
- unknown outcome after timeout

A missing timeout is a finding when the call can consume a bounded shared resource indefinitely or violate an established latency/shutdown contract.

## Resource ownership and limits

Check lifecycle and bounds for:

- connections, transactions, cursors, response bodies, files, sockets
- goroutines/tasks/threads and executors
- event listeners, timers, watchers, subscriptions
- queues, buffers, caches, maps, and cardinality
- child processes and captured output
- large request/response bodies and decompression
- temporary files and disk usage
- GPU/model context, tool calls, or external API spend

Identify both release on all paths and an upper bound under plausible load.

## Shutdown and recovery

Inspect:

- stop accepting new work before draining
- cancellation and deadline propagation
- in-flight transaction/job acknowledgment behavior
- closing shared resources after users finish
- signal handling and forced-shutdown deadline
- startup recovery of partial/in-progress state
- restart-safe locks, leases, temp files, and idempotency
- readiness only after migrations/config/cache/model are usable

A clean happy-path shutdown is insufficient if cancellation leaves durable ambiguity.

## Backpressure and overload

Check:

- bounded versus unbounded queues/channels/executors
- producer response when capacity is exhausted
- fan-out per request/item
- concurrency limits at the correct scope
- load shedding and admission control
- retry storms and thundering herds
- cache stampede and single-flight behavior where required
- slow consumer handling
- pagination/streaming versus loading all data
- work amplification from malformed or adversarial input

Do not report theoretical unboundedness when an upstream hard limit is verified and small.

## Performance proof

A performance finding needs all of:

1. an in-scope path that is hot, repeated, or accepts scalable input
2. an operation whose cost grows materially in CPU, memory, I/O, locks, network calls, or external spend
3. a plausible workload or repository evidence of scale
4. a consequence such as latency SLO violation, resource exhaustion, contention, or cost increase
5. no effective batching, cache, limit, optimizer, or off-path execution that disproves it

Use complexity plus realistic constants. Avoid micro-optimization comments.

## Common high-value patterns

Investigate when reachable:

- query or RPC inside a per-item loop (N+1/fan-out)
- full table/list scan introduced on request path
- repeated parse/compile/serialization of invariant data
- copying large buffers/collections unnecessarily across layers
- holding a global lock during I/O or long computation
- synchronous/blocking I/O on an event loop or constrained executor
- eager loading where streaming/pagination was required
- cache key explosion or no eviction
- quadratic matching/deduplication on user-sized input
- retry multiplication across layers
- rendering/recomputing large UI subtrees on frequent state changes

Confirm framework/database behavior; an apparent loop may be batched or optimized.

## Verification

Prefer existing benchmarks, query plans, metrics comments, limits, fixtures, and load assumptions. A focused benchmark may help when safe, but do not create noisy or environment-dependent numbers and present them as production truth.

State:

- workload and scale
- operation count/complexity before and after
- constrained resource
- expected consequence
- mitigations checked

## Severity calibration

- Cheap external trigger causing reliable broad outage may be High/Critical depending containment and Critical gates.
- Common-path resource leak or N+1 causing likely production degradation is High or Medium based on scale.
- Uncommon bounded latency regression is Medium/Low.
- “Could be faster” without a contract or plausible impact is not a finding.
