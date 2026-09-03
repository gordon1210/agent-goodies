# Async, Concurrency, Streams, and Lifecycle

Read this reference whenever code uses promises, timers, event emitters, async iterators, streams, queues, worker threads, Web Workers, child processes, shared memory, retries, deadlines, background tasks, or graceful shutdown.

## 1. Understand the concurrency model

JavaScript commonly runs one task at a time on an event loop, but this does not eliminate concurrency bugs:

- Async operations interleave at suspension points.
- Multiple requests mutate shared process state.
- External systems proceed concurrently.
- Workers and child processes execute in parallel.
- Callbacks, timers, microtasks, streams, and framework lifecycle hooks can reorder work.
- Cancellation or client disconnect can occur between side effects.

“Single-threaded” does not make read-modify-write sequences atomic across `await`, nor does it protect databases, files, caches, or remote APIs.

Use synchronous code when work is naturally sequential and bounded. Use async for I/O or APIs that are inherently asynchronous. Use workers, child processes, native code, or an external job system for CPU-heavy parallelism when justified.

## 2. Promise ownership

Every created promise needs a deliberate owner. It must be:

- Awaited.
- Returned to a caller that owns completion.
- Collected by a bounded supervisor/task group.
- Intentionally detached under an owner that observes rejection, limits lifetime/count, and integrates with shutdown.

Reject:

- Floating promises whose rejection is unobserved.
- `void operation()` used as if it handled failure.
- `.catch(() => undefined)` used to suppress unexpected failure.
- Promise creation inside callbacks that the host does not await without explicit bridging.
- Async event-listener callbacks whose errors disappear into the host API.

`void` can document that a promise is deliberately not awaited, but it does not provide ownership, cancellation, or error handling.

### Detachment gate

Before detaching work, answer:

1. Why may it outlive the current operation?
2. Who observes rejection?
3. What bounds task count, duration, and retained input?
4. What happens during shutdown or navigation?
5. Is lost work acceptable?
6. Can duplicate execution occur after retry/restart?
7. How is tracing/request context propagated or deliberately severed?

If these answers are unclear, do not detach it.

## 3. Structured concurrency

Prefer operations whose child work completes or is cancelled before the parent finishes. JavaScript lacks one universal structured-concurrency primitive, so build the property explicitly with the repository's tools:

- Return/await child promises.
- Use an abort controller owned by the operation.
- Collect workers or tasks in a bounded group.
- Use `try/finally` for cleanup.
- Propagate the first meaningful failure and wait for required cleanup.
- Avoid global registries unless work is truly process-scoped.

A supervisor should define:

- Task admission and capacity.
- Failure policy: fail-fast, isolate, restart, degrade, or stop.
- Cancellation propagation.
- Result/error collection.
- Shutdown deadline and forced termination.
- Observability without unbounded labels or retained errors.

## 4. Event loop and CPU work

Do not block latency-sensitive event loops with:

- Large JSON parsing/stringification.
- Compression/decompression.
- Cryptography or password hashing beyond appropriately asynchronous/native APIs.
- Image/audio/video processing.
- Large template rendering or data transformation.
- Synchronous filesystem or child-process operations.
- Catastrophic regex behavior.
- Tight loops over attacker-controlled cardinality.

Before offloading:

- Measure representative event-loop delay and CPU profiles.
- Check whether a better algorithm, streaming, batching, or data reduction fixes the issue.
- Bound worker pool size and queued work.
- Account for serialization/copying or transferable-object semantics.
- Define cancellation and worker failure behavior.
- Avoid offloading tiny tasks whose scheduling/copy overhead exceeds the work.

Async syntax does not make CPU work asynchronous.

## 5. Cancellation with `AbortSignal`

Use `AbortSignal` or the repository's established cancellation mechanism at operations that can stop meaningful work.

Design rules:

- Accept a caller-provided signal rather than creating an unrelated signal in every layer.
- Check already-aborted state before starting side effects.
- Propagate the signal to fetches, streams, timers, SDKs, workers, and child operations that support it.
- Remove abort listeners or use one-shot listeners to avoid leaks.
- Preserve the caller's abort reason where useful and safe.
- Distinguish cancellation from timeout and arbitrary failure when callers act differently.
- Make cleanup idempotent because cancellation can race with normal completion.

A signal is cooperative. Libraries that ignore it and external work already accepted may continue.

### Cancellation safety

At each `await` inside a multi-step side-effecting operation, ask:

- What has already changed?
- Can the operation be retried safely?
- Can data be lost, duplicated, reordered, or partially persisted?
- Does a transaction, lease, lock, stream, file, permit, or temporary resource remain open?
- Does remote work continue after the local caller stops waiting?
- Is compensation or idempotency required?

Validate before side effects. Use atomic/transactional operations and idempotency keys where appropriate. Do not promise cancellation semantics the downstream API does not provide.

## 6. Timeouts and deadlines

A timeout limits how long a caller waits only if underlying work is also cancelled or safely abandoned.

Prefer an absolute deadline or remaining budget propagated across layers. Independent per-layer timeouts can exceed the caller's total budget and multiply retries.

A timeout policy must define:

- Connection, first-byte, idle, per-operation, and total limits where applicable.
- What happens to the underlying operation.
- Whether a database connection, stream, worker, or request remains usable afterward.
- Whether the outcome is known-not-applied or unknown.
- Whether retry is safe.
- Cleanup and telemetry behavior.

`Promise.race` does not cancel losing promises. If a timeout wins, observe or cancel the underlying operation so late rejection/completion does not leak or mutate state unexpectedly.

## 7. Promise combinators

### `Promise.all`

- Starts/observes all supplied promises and rejects when one rejects, but other operations generally continue.
- Can create unbounded fan-out when built from attacker-controlled arrays.
- Does not provide rollback for completed siblings.

Use it for a bounded set of operations whose partial completion semantics are understood.

### `Promise.allSettled`

Use when every outcome must be collected. Still bound concurrency; it waits for all operations and can retain many results/errors.

### `Promise.race`

Use for first-settled semantics only when losing work is cancelled or safely allowed to continue. Observe all late failures.

### `Promise.any`

Use when one success is sufficient and duplicate side effects are safe. Account for aggregate errors and ongoing losing work.

### Sequential loops

Sequential `for...of` with `await` is correct when ordering, rate limits, shared state, or resource constraints require it. Do not flag it automatically as slow.

### Array callbacks

`forEach` does not await async callbacks. Prefer a loop, a mapped promise collection, or a bounded-concurrency utility according to semantics.

## 8. Bounded concurrency and backpressure

Map resource budgets to explicit limits:

- In-flight HTTP/RPC calls.
- Database operations and pool connections.
- Open files and streams.
- Worker tasks and child processes.
- Queue length and payload size.
- Batch size and buffered results.
- Retry/hedge volume.

Define behavior when capacity is exhausted:

- Wait with a deadline.
- Reject or shed load.
- Coalesce equivalent work.
- Drop best-effort updates.
- Spill to a durable queue.
- Apply upstream flow control.

A semaphore without queue limits or deadlines can merely move unbounded growth into waiting promises. A large queue converts overload into memory pressure and stale work.

Avoid creating one promise/closure for every huge input before applying the limit; use a producer/worker pattern or async iterator that bounds retained work.

## 9. Races in shared state

An `await` splits a function into interleavable segments. This can race:

```ts
const current = cache.get(key);
await refresh();
cache.set(key, transform(current));
```

Review:

- Read-modify-write sequences across suspension.
- Check-then-act authorization or existence checks.
- Cache stampedes and stale overwrites.
- Duplicate submission.
- Request-local data stored globally.
- UI requests whose older response overwrites newer state.
- Cleanup racing with callbacks.

Use the simplest mechanism that owns the invariant:

- Atomic database operation or transaction.
- Version/ETag/optimistic concurrency.
- Single-flight/coalescing by key with bounded retention.
- Queue/actor ownership.
- Mutex/semaphore from an established library where necessary.
- Request IDs or abort controllers to reject stale UI results.

Do not add a process-local mutex to solve a distributed race across instances.

## 10. Locks and synchronization libraries

JavaScript mutexes coordinate async tasks in one process; they do not protect external systems or other processes.

When using one:

- Keep critical sections minimal and bounded.
- Avoid arbitrary callbacks while locked.
- Define lock order for multiple locks.
- Ensure rejection/cancellation releases the lock.
- Avoid waiting on work that re-enters the same non-reentrant lock.
- Bound lock wait and expose contention if operationally relevant.
- Keyed locks must evict unused keys safely to avoid memory leaks.

Prefer transactional external operations or ownership transfer when the invariant lives outside the process.

## 11. Streams and async iterators

Streams are useful for large or incremental data only when backpressure and cleanup remain intact.

Define:

- Maximum frame/chunk/record size.
- Buffer/high-water marks.
- Who owns pausing/resuming or pulling.
- Error propagation in both directions.
- Cancellation and early-consumer exit.
- Partial output semantics.
- Encoding boundaries and incomplete multibyte data.
- Resource closure on success and failure.

### Node and Web streams

Do not assume Node streams and WHATWG streams are identical. When adapting:

- Verify backpressure translation.
- Propagate abort/cancel and errors.
- Avoid converting to a full buffer unless bounded.
- Test early termination, slow consumers, and source failure.

For async iterators, implement or trigger cleanup when iteration stops early. A consumer `break` must not leave a socket/file/subscription active.

## 12. Event emitters and callbacks

Event listeners are lifecycle resources.

- Register and unregister symmetrically.
- Avoid anonymous listener functions when removal requires identity.
- Define whether multiple events can overlap async handlers.
- Observe handler failures; many emitter APIs ignore returned promises.
- Bound listener count and investigate warnings rather than raising global limits blindly.
- Avoid retaining request/user objects through long-lived listeners.
- Define event ordering and whether missed/coalesced events are acceptable.

Bridge callback APIs to promises carefully:

- Settle once.
- Handle synchronous throw and asynchronous callback.
- Remove listeners on completion/cancellation.
- Preserve multiple callback values deliberately.
- Account for callbacks invoked more than once by faulty or streaming APIs.

## 13. Timers and scheduling

- Store timer handles when cancellation matters.
- Clear timers/intervals on shutdown, component unmount, request cancellation, or test cleanup.
- Prefer self-scheduling after completion over `setInterval` when overlapping runs are unsafe.
- Add jitter to distributed periodic work when synchronization storms matter.
- Do not use timer accuracy as a correctness guarantee; event-loop delay and platform throttling apply.
- Use monotonic elapsed-time APIs for durations where available.
- Bound recurring task duration and define overlap policy.
- Consider whether a timer keeps a Node process alive and use unref behavior only when lost work is acceptable.

Avoid wall-clock sleeps in tests; use fake/controlled timers.

## 14. Retries, hedging, and idempotency

Retry only when:

- Failure is classified as transient.
- The operation is idempotent or protected by an idempotency mechanism.
- The outcome is sufficiently known.
- The deadline permits another attempt.
- Attempts, elapsed time, and concurrent retry volume are bounded.
- Backoff and jitter prevent synchronized load.

Do not retry validation, authentication, authorization, deterministic conflicts, unsupported requests, or non-idempotent unknown outcomes blindly.

Prevent retry multiplication across browser, API gateway, service, SDK, queue, and database layers. One logical request can otherwise cause exponential work.

Hedging/racing duplicate requests is appropriate only when duplicates are safe, downstream capacity can absorb them, and losing work is cancelled/deduplicated.

## 15. Workers and child processes

Use workers/processes when isolation or parallel CPU work justifies transfer and lifecycle cost.

For every worker/process:

- Bound count and queued work.
- Validate messages and result sizes.
- Define ownership, startup, readiness, error, exit, restart, and shutdown behavior.
- Handle worker crash and partially completed work.
- Avoid passing secrets or broad environment unnecessarily.
- Bound stdout/stderr and prevent deadlock from unread pipes.
- Terminate process trees, not only an immediate child, when required.
- Use direct executable/argument APIs rather than shell strings for untrusted values.
- Account for serialization/copy cost, transferable objects, and shared-memory safety.

Do not spawn one worker/process per untrusted item.

## 16. Shared memory and atomics

`SharedArrayBuffer`, typed arrays, and `Atomics` create real multi-threaded memory semantics.

For nontrivial protocols, document:

- Memory layout and ownership.
- Which atomic operation synchronizes with which.
- State transitions and valid values.
- Wait/notify behavior and shutdown.
- Overflow, wraparound, ABA-like state reuse, and lost wakeups.
- What happens if a worker crashes mid-protocol.

Prefer message passing or established primitives over custom lock-free algorithms. Ordinary tests cannot exhaust interleavings; use targeted stress/model techniques where available and keep a written protocol proof.

## 17. Request context propagation

Request/job context may include trace identifiers, tenant/authorization context, deadlines, and safe diagnostic fields.

- Pass context explicitly where practical.
- When using runtime context APIs such as async-local storage, understand which callbacks/promises preserve context and where custom bridges break it.
- Do not use ambient context as the sole authorization source when explicit resource scope is safer.
- Avoid retaining large request objects in long-lived contexts.
- Ensure detached tasks deliberately inherit or sever request context.
- Test context across queues, event emitters, worker boundaries, and third-party callbacks.

## 18. Service and application shutdown

Graceful shutdown is a protocol:

1. Make shutdown initiation idempotent.
2. Stop accepting new work.
3. Mark readiness false/draining where applicable.
4. Signal cancellation to owned tasks.
5. Close producers and reject or drain queued work according to policy.
6. Let in-flight work complete within a deadline or abort it safely.
7. Flush/commit critical state and bounded telemetry.
8. Close servers, pools, streams, workers, and child processes.
9. Force termination after an explicit deadline when necessary.
10. Exit with a meaningful status.

Handle repeated signals and shutdown during partial startup. Do not wait forever for an uncooperative dependency. Do not call immediate process termination before critical cleanup unless corruption or security requires it.

Libraries should not install process-wide signal handlers without an explicit application-level contract.

## 19. Browser and UI lifecycle

Async UI work must account for navigation, rerender, unmount, and stale responses.

- Cancel or ignore stale requests deliberately.
- Clean up subscriptions, observers, event listeners, object URLs, workers, and timers.
- Prevent older responses from overwriting newer user intent.
- Avoid updating state after an owning component/view is gone.
- Bound prefetching, retries, and concurrent uploads/downloads.
- Preserve accessibility state and focus through async transitions.
- Do not simulate loading states when no actual operation is pending.

Follow the framework's lifecycle primitives rather than creating a parallel global task manager.

## 20. Queue and background job semantics

Define:

- Delivery semantics: at-most-once, at-least-once, or another explicit contract.
- Acknowledgement point.
- Idempotency/deduplication.
- Visibility timeout or lease renewal.
- Retry classification/backoff.
- Poison-message and dead-letter behavior.
- Ordering and concurrency by key.
- Payload and queue size limits.
- Shutdown/drain behavior.
- Schema version and mixed-deployment compatibility.

Avoid “exactly once” claims unless the complete end-to-end side effect and deduplication protocol proves them.

## 21. Async testing

Test relevant combinations of:

- Success and synchronous throw.
- Rejected promise and thrown non-`Error` value.
- Cancellation before start, during each important wait, and after a side effect.
- Timeout with late completion/rejection.
- Queue saturation and capacity wait.
- Partial `Promise.all` completion.
- Slow stream producer/consumer and early termination.
- Event listener cleanup and duplicate events.
- Worker crash and forced shutdown.
- Repeated shutdown signals and partial startup.
- Retry known-failure versus unknown-outcome paths.
- UI stale response/unmount behavior.

Use fake clocks and controlled deferred promises instead of sleeps. Bound every wait so failures do not hang indefinitely.

## Common failures to reject

- Floating promises hidden by `void`.
- Async `forEach` callbacks assumed to be awaited.
- `Promise.race` timeout assumed to cancel work.
- Unbounded `Promise.all` over external input.
- Catching and suppressing every rejection.
- Synchronous CPU or filesystem work on a latency-sensitive event loop.
- Process-local locking used to solve a cross-instance race.
- Async event handlers whose host ignores returned promises.
- Streams converted to unbounded full buffers.
- Intervals whose runs overlap and accumulate.
- Detached tasks with no shutdown owner.
- Retries after unknown non-idempotent outcomes.

## Async completion checklist

- Every promise and asynchronous resource has an owner.
- Cancellation and deadlines propagate to work that can stop.
- Timeouts do not leave unobserved operations.
- Fan-out, queues, workers, retries, buffers, and retained results are bounded.
- Event-loop blocking and CPU parallelism are intentional.
- Shared-state races and external atomicity are addressed at the correct boundary.
- Streams preserve backpressure and early-exit cleanup.
- Timers, listeners, workers, and child processes have lifecycle cleanup.
- Shutdown is bounded, idempotent, and tested.
- Tests cover failure, cancellation, saturation, late completion, and cleanup—not only success.
