# Performance and Resource Use

Read this reference when a change may affect runtime latency, throughput, CPU, event-loop delay, memory, I/O, startup, browser responsiveness, bundle size, build time, type-check time, editor performance, CI resource use, or behavior under load.

Performance work is empirical engineering. Preserve correctness, security, and operational safety first; then optimize the bottleneck measurements identify.

## 1. Establish the performance contract

Define what matters before changing code:

- Latency: median, tail, deadline, frame budget, interaction delay, or worst-case bound.
- Throughput: requests, messages, jobs, records, or bytes per unit time.
- Event-loop responsiveness and maximum synchronous task duration.
- CPU: total work, single-request work, worker utilization, or energy budget.
- Memory: live heap, retained heap, RSS, peak use, per-request growth, browser tab use, or CI/build peak.
- I/O: round trips, bytes, syscalls, queries, files, network requests, and storage amplification.
- Startup, cold start, module initialization, hydration, and shutdown time.
- Bundle/chunk size, parse/compile/evaluation cost, and cache behavior.
- Type-check, lint, declaration emit, build, incremental, and editor response time.
- Target runtime/browser, hardware, operating system, architecture, dataset, concurrency, compiler generation, and production build mode.

Do not optimize against “faster” without defining the user/operator/developer outcome. A throughput improvement that harms tail latency, memory, fairness, correctness, or build stability can be a regression.

## 2. Measure before and after

Use a repeatable baseline:

1. Record commit, runtime, TypeScript version, package/lock state, build mode, target, hardware, and relevant configuration.
2. Measure the production artifact or representative equivalent.
3. Separate cold and warm behavior when both matter.
4. Use realistic input distributions, including pathological but valid cases.
5. Run enough samples to distinguish signal from noise.
6. Compare distributions, percentiles, or confidence intervals rather than one best run.
7. Change one meaningful variable at a time.
8. Validate output equivalence, security, cancellation, and resource limits after optimization.

Prefer production profiles/traces and representative system benchmarks over intuition. Microbenchmarks answer narrow questions and can be misleading when JIT warmup, dead-code elimination, allocation, I/O, or framework overhead differs from production.

## 3. Profile the suspected resource

Choose evidence appropriate to the problem:

- CPU sampling/flame charts for hot call paths.
- Event-loop delay and long-task measurement for responsiveness.
- Heap snapshots/allocation profiles for retained memory and churn.
- GC traces for pause/frequency and allocation pressure.
- I/O/query traces for round trips and wait time.
- Browser performance traces for network, main thread, layout, paint, and hydration.
- Bundle analyzers for module/chunk contribution.
- TypeScript extended diagnostics/traces for compiler work.
- CI timing and peak memory for build parallelism.

Interpret profiles carefully:

- A hot function may be called too often rather than be locally inefficient.
- Large RSS may come from native code, workers, mapped files, or runtime caches rather than JS heap.
- Allocation sites may be cheap but retained through caches, listeners, closures, or unresolved promises.
- Low CPU can indicate I/O wait, lock/queue contention, downstream limits, or event-loop starvation elsewhere.
- Development instrumentation and source maps can distort production behavior.

## 4. Algorithm and architecture first

Prefer eliminating work or improving asymptotic behavior:

- Avoid repeated full-array scans when indexing is justified.
- Avoid accidental quadratic concatenation, merging, deduplication, diffing, rendering, or parsing.
- Stream or paginate data that need not be resident at once.
- Batch operations when it reduces fixed overhead without violating latency, transaction, or memory limits.
- Fetch only fields/rows/resources needed.
- Avoid sorting when only min/max/top-k/partition is required.
- Move invariant computation out of loops/request paths.
- Coalesce duplicate in-flight work when semantics allow.
- Cache only when key, consistency, invalidation, memory bound, hit rate, privacy, and failure behavior are defined.

Do not replace a simple structure with a complex one for hypothetical scale.

## 5. Event-loop responsiveness

For Node.js, browser main threads, and similar runtimes:

- Bound synchronous work per request/event/frame.
- Avoid synchronous filesystem, child-process, compression, cryptography, or large parsing on latency-sensitive paths.
- Break or offload genuinely large CPU work only when scheduling/copy cost and correctness are understood.
- Use incremental/streaming processing for large payloads where it preserves backpressure.
- Avoid chains of microtasks that starve timers, I/O, rendering, or cancellation.
- Limit synchronous framework middleware and serialization.
- Measure long tasks/event-loop delay under representative concurrency.

Adding `async` or wrapping work in a resolved promise does not yield to another thread and may not improve responsiveness.

## 6. Bounded concurrency

Concurrency hides wait time but can multiply memory, connections, downstream load, and retries.

- Bound in-flight operations according to local and downstream capacity.
- Avoid unbounded `Promise.all` over external cardinality.
- Bound queued work as well as active work.
- Include deadlines/rejection behavior for capacity waits.
- Avoid one worker/process per item.
- Separate CPU and I/O limits.
- Check fairness and tail latency; maximum throughput can starve low-volume or latency-sensitive work.
- Account for per-task retained closures, buffers, context, and errors.

A larger pool is not automatically faster. Measure saturation, queueing, and memory.

## 7. Data structures

Choose structures from access pattern and semantics:

- Array for ordered dense sequences and iteration.
- Map for arbitrary keys, explicit absence, insertion order, and non-string keys.
- Set for membership and deduplication.
- Object/record for controlled JSON-like string-keyed data.
- Heap/index/tree/specialized structure only when operations/cardinality justify it.

Consider:

- Lookup/update frequency.
- Ordering/determinism.
- Key trust and prototype semantics.
- Memory overhead.
- Serialization needs.
- Stable output requirements.
- Cardinality and tiny-collection behavior.

For small collections, a linear scan can be simpler and faster than building an index. Measure representative sizes.

## 8. Allocation and object lifetime

Before micro-optimizing allocation:

1. Eliminate unnecessary data/work.
2. Avoid retaining large objects longer than needed.
3. Stream or process incrementally when possible.
4. Reuse buffers/objects only when ownership remains clear and races are impossible.
5. Reduce intermediate arrays/strings on proven hot paths.
6. Consider specialized representations only after profiling.

Watch for logical leaks through:

- Unbounded caches/maps/sets.
- Event listeners and subscriptions.
- Timers/intervals.
- Pending promises and queues.
- Closures retaining request/UI graphs.
- Request context stores.
- Worker/process references.
- DOM nodes detached but referenced.
- Object URLs, observers, streams, and sockets.
- Metrics labels and telemetry buffers.

Garbage collection can reclaim unreachable objects, not reachable objects that should have been removed.

## 9. Arrays, iteration, and intermediate collections

Loops and array methods can both be clear and fast. Choose semantics first.

- Avoid `map(...).filter(...).reduce(...)` chains that allocate several large intermediates when one readable loop materially reduces cost.
- Keep functional transformations when data is small/cold and clarity wins.
- Avoid repeated spreads in a loop that copy growing arrays/objects.
- Preallocate only when a reliable bounded size is known and the runtime pattern benefits.
- Prefer direct iteration to index arithmetic when it prevents mistakes; use indexes when the algorithm needs them.
- Do not replace every loop with array methods or vice versa based on folklore.
- Beware sparse arrays, holes, and mutating an array during iteration.

Benchmark the complete operation with realistic sizes and JIT warmup.

## 10. Strings, bytes, JSON, and parsing

- Parse once at trust boundaries into an internal representation.
- Avoid repeated JSON stringify/parse as a cloning/conversion mechanism on hot paths; it is lossy and allocates heavily.
- Avoid quadratic string concatenation for large output; use arrays/chunks/streams or established builders as appropriate.
- Use bytes/typed arrays for binary data and text encoders/decoders deliberately.
- Preserve incremental decoder state across chunk boundaries.
- Bound body and decoded sizes before full buffering.
- Avoid repeated normalization, case conversion, regex parsing, and date/number parsing.
- Use a parser suited to the format; avoid regex for complex nested grammars.
- Validate zero-copy slices/views do not retain a huge backing buffer unnecessarily.

Large JSON parsing/stringification is synchronous in common runtimes; measure event-loop impact.

## 11. Object shapes and runtime optimization

Modern JavaScript engines optimize common object/function patterns, but engine internals are not stable application contracts.

General guidance:

- Prefer consistent object shapes in proven hot code.
- Avoid adding/removing many dynamic properties repeatedly when a stable representation is clearer.
- Avoid polymorphic values and megamorphic dispatch only when profiles show it matters.
- Keep hot numeric arrays free of mixed unexpected values where semantics allow.
- Do not contort domain models around speculative hidden-class or inline-cache folklore.
- Re-test across supported runtimes/versions; engine optimizations differ.

Readable correct code plus profiling beats cargo-cult V8 tuning.

## 12. Database and network performance

- Remove N+1 query/request patterns when a bounded batch/join is semantically correct.
- Select only needed data.
- Paginate/stream large results and cap page size.
- Use indexes based on actual query plans and workload, not ORM model intuition.
- Reuse connections through bounded pools with deadlines and health policy.
- Batch writes within transaction, latency, conflict, and payload limits.
- Avoid retry amplification.
- Cache remote results only with explicit freshness, tenant scope, invalidation, and memory policy.
- Compress only when payload, CPU, latency, and existing protocol compression justify it.
- Respect backpressure instead of buffering entire uploads/downloads.

A faster application loop cannot compensate for an unbounded query or remote call fan-out.

## 13. Browser loading and bundle performance

Measure the user-visible path:

- Network transfer and compression.
- Number and ordering of requests.
- JavaScript parse/compile/evaluate time.
- Main-thread blocking and hydration.
- CSS/font/image behavior.
- Cacheability and versioning.
- Route/interaction-specific chunks.

Guidance:

- Keep server-only and unused dependencies out of client graphs.
- Prefer targeted imports when package exports and tree shaking support them.
- Verify `sideEffects` metadata before relying on dead-code elimination.
- Lazy-load code that is truly noncritical; excessive splitting can add waterfalls and failure modes.
- Avoid shipping huge schemas/locales/polyfills/data sets when a subset suffices.
- Optimize images/fonts/assets through the repository's pipeline.
- Measure production-minified output, not source module count.
- Add bundle budgets only when the team owns their maintenance and they correlate with user outcomes.

Small compressed bytes can still have high parse/evaluation cost.

## 14. Rendering and UI performance

- Measure actual interaction/render traces before adding memoization.
- Keep state localized enough to avoid broad invalidation, but do not fragment it into unmanageable stores.
- Avoid deriving the same expensive value repeatedly; compute/cache only with correct dependencies and bounded lifetime.
- Virtualize large views only when list size/render cost requires it and accessibility/measurement remains correct.
- Debounce/throttle based on product semantics; do not lose required final events.
- Cancel/ignore stale async results.
- Batch DOM reads/writes when layout thrashing is measured.
- Avoid deep cloning state to signal change.
- Test production framework mode; development diagnostics can exaggerate or change render behavior.

Memoization has lookup, memory, invalidation, and complexity cost. It is not a default fix.

## 15. Startup and cold start

Inspect:

- Eager imports and top-level initialization.
- Configuration/schema loading.
- Dependency graph and native addon startup.
- Database/network connection strategy.
- Framework bootstrap and route registration.
- Source-map/instrumentation overhead.
- Serverless package size and initialization.

Move work lazily only when delayed failure and first-use latency are acceptable. Required configuration and critical invariants should still fail early and clearly.

Avoid dynamic import solely to make one benchmark look better if it shifts latency to a critical request.

## 16. Memory bounds and caches

Every cache needs:

- Key and tenant/security scope.
- Maximum entries/bytes.
- Expiration/eviction policy.
- Invalidation/freshness semantics.
- Behavior on loader failure.
- Stampede/coalescing policy.
- Observability with bounded labels.
- Shutdown/restart implications.

Avoid caching promises/errors forever unintentionally. Remove failed in-flight entries according to retry semantics. Use weak collections only when key reachability genuinely owns lifetime; they do not provide size control or iteration.

## 17. Type-level and compiler performance

TypeScript performance can degrade through source/configuration shape independently of runtime performance.

Common causes:

- Huge unions/intersections and distributive conditional types.
- Deep recursive mapped/conditional types.
- Generic inference across enormous object literals.
- Repeated inline structural types instead of named reusable boundaries.
- Broad declaration merging and ambient globals.
- Very large inferred exported types/declarations.
- Broad `include` globs and duplicate project membership.
- Multiple type-aware lint programs over the same files.
- Unnecessary library/type packages in every project.
- Project-reference cycles or stale/generated outputs.
- Compiler plugins and declaration transforms.

Guidance:

- Measure with compiler diagnostics/traces.
- Name complex shared types when it improves reuse and diagnostics.
- Prefer interfaces/simple object types over clever transformations when equivalent and measured cheaper.
- Prevent distributivity with the standard tuple-wrapping technique only when semantics require it.
- Bound recursive type depth and avoid parsing arbitrary large string literal types.
- Add explicit exported annotations to avoid unstable/huge inferred declarations.
- Scope projects and ambient types precisely.
- Do not weaken type safety broadly merely to improve compile time without evidence and alternatives.

## 18. Project references and incremental builds

Project references can improve incremental work when boundaries are real, but add declaration/build coordination.

Measure:

- Clean type-check/build.
- Incremental edit in a leaf and a shared package.
- Editor responsiveness.
- Declaration emit and downstream rebuild scope.
- CI cache behavior.
- Peak memory and process count.

Ensure outputs and build-info files do not collide. Avoid splitting packages solely for parallel compilation if API/coordination costs exceed the gain.

## 19. TypeScript 6 versus 7 performance

TypeScript 7's native compiler and parallel controls can change build-time performance and resource behavior, but migration is not merely a benchmark decision.

- Validate correctness, declarations, tools, compiler API integrations, and runtime artifacts first.
- Measure the repository's actual clean/incremental/build/watch workloads.
- Record checker and project-builder parallelism.
- Account for peak memory and CI process limits.
- Avoid maximum parallelism by default; nested builder/checker concurrency can multiply workers.
- Use single-threaded or lower-concurrency modes for diagnosis and constrained environments when appropriate.
- Do not retain TypeScript 6 migration-only ordering flags as permanent performance costs without need.

See [typescript-6-7-compatibility.md](typescript-6-7-compatibility.md) for migration gates.

## 20. Lint, test, and build pipeline performance

- Avoid constructing separate expensive type programs for many overlapping lint invocations.
- Scope lint/test/build jobs to declared packages while preserving dependent contracts.
- Use caching only with complete inputs and reproducible outputs.
- Keep generated files out of unnecessary lint/type-test paths.
- Shard large tests based on measured duration and isolation.
- Do not use retries to hide slow/flaky tests.
- Separate merge-critical checks from expensive scheduled exploration only when merge safety remains sufficient.
- Measure developer feedback time as well as CI throughput.

Do not “optimize” by skipping declaration, package, security, or compatibility checks that protect real release contracts.

## 21. Benchmark design

A benchmark should state:

- The question it answers.
- Inputs and distributions.
- Setup included/excluded.
- Runtime/compiler/build mode and target.
- Warmup and JIT strategy.
- Concurrency and downstream dependencies.
- Expected noise sources.
- Correctness checks outside timed regions.
- Practical threshold for accepting complexity.

Avoid:

- Benchmarking development builds for production claims.
- Timing only a synthetic micro-operation while ignoring serialization/I/O/GC.
- Constant-foldable or dead-code-eliminated work.
- Comparing different runtimes/tools/configurations as if only code changed.
- Treating statistically significant but operationally irrelevant differences as justification for complexity.

## 22. Performance review gate

Before accepting an optimization, verify:

- The bottleneck was measured on a representative workload/artifact.
- The change improves the stated metric, not only a proxy.
- Correctness, security, determinism, compatibility, cancellation, and resource limits remain intact.
- Memory, tail latency, fairness, startup, and downstream load were considered.
- Complexity is proportionate to the gain.
- A benchmark or regression guard protects the property when practical.
- Non-obvious assumptions are documented close to the code.

Reject speculative optimization that adds complexity without evidence or a concrete budget.

## Performance completion checklist

- Performance objective and target environment are explicit.
- Before/after measurements are repeatable and representative.
- Algorithmic and architectural waste is addressed before micro-tuning.
- Event-loop, concurrency, memory, I/O, browser, and bundle effects are bounded.
- Runtime and build/type-check performance are measured separately.
- Type-level complexity and project scope remain maintainable.
- TypeScript 7 parallelism is tuned against memory and compatibility, not maximized blindly.
- Correctness and operational tests still pass on the production artifact.
