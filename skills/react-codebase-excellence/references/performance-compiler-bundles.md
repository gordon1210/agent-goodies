# Performance, React Compiler, and Bundles

Read this reference when investigating responsiveness, loading, rendering cost, memory, bundle size, data waterfalls, React Compiler, or production performance. Performance work requires a defined user-facing contract and evidence; syntax preferences are not benchmarks.

## 1. Define the performance contract

Before changing code, identify:

- affected user journey and device/network class;
- current and target metric;
- production build and realistic data size;
- warm versus cold cache;
- client, server, edge, or mixed bottleneck;
- acceptable memory, CPU, network, and battery cost;
- regression budget and measurement method.

Useful browser-facing metrics may include LCP, INP, CLS, TTFB, resource timing, long tasks, interaction latency, and route transition timing. Component render duration is useful diagnostics but not automatically the product metric.

Do not claim an improvement from fewer lines, an iterator style, a memo wrapper, or a theoretical allocation without representative measurement.

## 2. Diagnose by category

Most React performance problems fall into one or more categories:

1. Data or asset waterfalls.
2. Too much JavaScript or CSS shipped, parsed, or executed.
3. Slow server work or poor cache scope.
4. Excessive serialization or hydration.
5. Broad state/context invalidation.
6. Expensive render calculation.
7. Too many DOM nodes or expensive layout/paint.
8. High-frequency events without scheduling or coalescing.
9. Memory retained by caches, hidden trees, listeners, or detached DOM.
10. Third-party scripts and widgets.

Measure the category before selecting a React-specific fix.

## 3. Measurement tools

Use applicable tools in production mode:

- browser Performance and Network panels;
- Core Web Vitals or application RUM;
- React DevTools Profiler;
- React 19.2 Performance Tracks in Chrome tooling;
- framework server timing and traces;
- bundle analysis and source maps;
- heap snapshots and allocation timelines;
- request logs and cache metrics;
- controlled browser automation on representative hardware.

Development Strict Mode and unoptimized bundles distort render counts and timing. They remain useful for correctness diagnostics, not final performance numbers.

Profile a reproducible interaction. Save baseline conditions and verify the result after the change.

## 4. Eliminate waterfalls first

Latency compounds when independent work starts serially.

Review:

- route loaders and nested server components;
- API routes that await before starting independent work;
- client Effects that wait for parent data before fetching known dependencies;
- code chunks discovered only after data;
- fonts, styles, and images discovered too late;
- authentication/session lookups repeated through a tree.

Start independent work together, but preserve authorization and resource bounds. Use Suspense or framework deferred data when it improves progressive rendering.

Do not parallelize dependent work or launch unbounded requests. A fast denial-of-service against your own backend is not an optimization.

## 5. Preserve useful content during async work

Replacing an already useful screen with a global loading state can make transitions feel slower even when total latency is unchanged.

Use transitions, localized Suspense boundaries, stale-while-refresh data, or optimistic UI when they match product semantics. Keep layout stable and indicate stale/pending status appropriately.

Never simulate loading to create a visual pattern. Pending UI must correspond to real work.

## 6. State placement and subscription breadth

High-frequency state should invalidate only the tree that needs it.

Investigate:

- state lifted above unrelated expensive subtrees;
- context values containing frequently changing and static fields;
- external-store consumers subscribing to entire stores;
- route data copied into broad global state;
- parent render creating expensive child trees even when children do not need the state.

Possible remedies:

- move state closer to the interaction;
- split stable and volatile context where consumer sets differ;
- use store selectors supported by the established library;
- pass children so an owner can update without recreating unrelated content;
- extract a measured expensive child and preserve its inputs;
- avoid subscribing to a value used only inside an event callback when the integration provides a non-rendering read.

Do not restructure a clear tree based only on render count. Cheap renders are normal.

## 7. Render calculation

First reduce unnecessary work algorithmically:

- avoid repeated scans by building an index when the dataset and reuse justify it;
- combine passes when profiling shows traversal cost matters;
- move invariant calculation out of render;
- compute only the visible/needed subset;
- avoid sorting merely to find min/max;
- use appropriate Map/Set lookup for repeated membership or joins;
- move heavy CPU work off the main thread when necessary.

Then consider memoization. A memo cache also consumes memory and comparison work.

Use immutable array methods when mutation would corrupt state; choose them for correctness first, not assumed speed.

## 8. Component memoization

`memo` can skip rendering when props compare equal. It helps only when:

- the component rerenders often;
- rendering is meaningfully expensive;
- props are usually referentially stable or cheaply comparable;
- skipped work improves the user metric;
- state/context updates inside the component are not the actual cause.

Do not wrap every component. Memoization can add noise, comparison cost, retained values, and false confidence.

Custom prop comparators are risky. They must compare every prop relevant to rendering, including functions that close over state. A deep comparator can cost more than rendering and can freeze stale behavior.

React Compiler can add automatic memoization, but profiler evidence and semantic correctness still matter.

## 9. `useMemo`

Use `useMemo` for:

- measured expensive pure calculation;
- a stable object/value required by another semantic contract;
- preserving a dependency or memoized-child input where identity matters;
- library integration documented to require stable identity.

Do not use it for a trivial primitive expression, as a correctness mechanism, or to hide an impure calculation.

React may discard memoized values in circumstances allowed by its contract. Code must remain correct without the cache.

In compiler-enabled code, prefer clear calculation and let the compiler optimize unless manual control is required. Existing memoization can remain; remove only with tests and measurement.

## 10. `useCallback`

`useCallback` caches a function identity, not its execution result.

Use it when:

- a subscription or imperative API needs stable identity;
- a memoized child is expensive and callback churn defeats a demonstrated optimization;
- a custom Hook documents stable returned actions;
- an Effect dependency must represent a stable semantic function.

Do not use it to prevent a function from being allocated by principle. Function allocation is often negligible, and dependencies still need to be correct.

A callback with an empty dependency array that reads changing state is a stale-closure bug, not an optimization.

## 11. React Compiler

React Compiler 1.x performs build-time automatic memoization and validates Rules-of-React assumptions.

Before adoption, inspect:

- exact compiler and runtime versions;
- supported React target;
- framework/build integration;
- compilation mode and gating;
- ESLint preset and diagnostics;
- third-party or generated code exclusions;
- production source maps and debugging;
- build-time impact;
- rollback strategy.

### Existing applications

Adopt incrementally:

1. Enable current React Hooks/Compiler diagnostics without changing runtime output if supported.
2. Fix genuine purity, mutation, ref, and Hook violations.
3. Compile a bounded package or directory.
4. Compare production behavior, performance, bundle, and error telemetry.
5. Expand only when evidence is positive.

A compiler bailout is not automatically a defect. The component remains normal React code. Treat a bailout as important when the performance contract depends on compilation or it reveals a correctness violation.

### Manual memoization

Do not delete existing `memo`, `useMemo`, or `useCallback` in bulk. The compiler may preserve or reason about them differently, and some encode intentional identity.

For new compiler-enabled code, rely on declarative code by default and add manual memoization only for explicit control.

### Directives

Use compiler opt-in/opt-out directives only according to the installed compiler's documented mode. `"use no memo"` is a narrow temporary escape hatch, not a blanket fix for incompatible code. Record why compilation is unsafe and how the exception will be removed.

### Libraries

Published compiled code must target consumers' supported React versions and include any required runtime dependency. Test the packed artifact in clean consumer projects. Do not assume every consumer runs the same compiler.

## 12. Context performance

A provider update rerenders consuming components according to React context semantics.

Optimize only after identifying broad invalidation:

- move provider closer to consumers;
- separate volatile data from stable actions/configuration;
- reduce value changes;
- split contexts by actual consumer/update patterns;
- use an established selector-capable store when context semantics cannot meet the requirement.

Memoizing the provider value helps only if its fields are stable. It does not stop rerenders when a field actually changes.

Do not replace all context with a state library because a benchmark uses an artificial high-frequency case.

## 13. Lists and large collections

For large lists, inspect:

- item count and DOM node count;
- item render cost;
- update frequency;
- scroll and keyboard requirements;
- dynamic row height;
- search/filter complexity;
- image and asset loading;
- accessibility and find-in-page requirements.

Options include:

- pagination or progressive disclosure;
- virtualization/windowing;
- `content-visibility` for long offscreen content;
- incremental rendering;
- server filtering;
- memoized item boundaries when measured;
- stable keys and localized state.

Virtualization reduces DOM but adds complexity around keyboard navigation, screen readers, measurement, sticky content, print, and browser find. Use it when the dataset and measured cost justify it.

`content-visibility` can help rendering cost while retaining DOM, but test focus, anchors, measurement, accessibility, and browser support.

## 14. Bundle size

Measure parsed and executed cost, not only compressed bytes.

Review:

- large dependencies used for a small feature;
- duplicate versions;
- accidental server code in client bundles;
- locale/data bundles;
- icon libraries and broad entry points;
- CSS-in-JS/runtime styling cost;
- polyfills above the browser target;
- development-only code in production;
- source map publication policy;
- third-party scripts.

Use bundle analysis tied to an actual route or entry. A dependency in the lockfile is not proof it ships to the browser.

## 15. Imports and barrels

Direct imports can reduce transform or bundle cost when a package's broad entry point is poorly tree-shaken, has side effects, or causes server/client boundary leakage. Modern bundlers can also optimize well-designed barrels.

Before rewriting imports:

- inspect package `exports` and `sideEffects`;
- inspect the production bundle;
- measure build/test transform cost;
- check public API stability of subpaths;
- avoid private file paths not covered by package exports;
- verify type-only imports.

Do not impose “no barrels” repository-wide without evidence. Public library barrels can be a deliberate stable API.

## 16. Code splitting

Split at natural low-frequency or heavy boundaries:

- route or large feature;
- editor, chart, map, media, or rich widget;
- admin-only capability;
- modal reached by a minority of users;
- provider SDK loaded only after activation.

Avoid excessive micro-chunks and chains of dependent lazy imports. Preload on a credible user intent signal when it improves latency and does not waste bandwidth.

Test chunk failure and deployment skew. A lazy import needs an Error Boundary/recovery path appropriate to the application.

## 17. Third-party scripts

Analytics, support widgets, experimentation, ads, and monitoring can dominate main-thread and network cost.

- load non-critical scripts after critical interaction or according to consent;
- use `async`/`defer` or framework script controls correctly;
- avoid duplicate SDK initialization;
- lazy-load the integration when users activate it;
- measure long tasks, network, and privacy cost;
- clean up single-page navigation hooks;
- maintain CSP and integrity policy.

Do not defer security-critical code or required accessibility functionality merely to improve a metric.

## 18. Images, fonts, and resources

React performance includes browser resource behavior.

- provide dimensions or aspect ratio to prevent layout shift;
- choose responsive image sizes and modern formats through established tooling;
- lazy-load below-the-fold images without delaying the primary content image;
- preload only genuinely critical fonts/resources;
- subset fonts when the product and localization matrix permit it;
- use `font-display` according to visual requirements;
- avoid early connections to third parties without likely benefit and privacy approval.

Framework image/font systems may already own these optimizations. Do not duplicate them.

## 19. Server and RSC performance

Review:

- repeated request work that can be deduplicated safely;
- data fetching nested into a waterfall;
- cache scope and invalidation;
- over-serialization to Client Components;
- large RSC payloads;
- module-level shared state;
- unbounded per-request concurrency;
- slow auth/session lookup repeated across layers;
- blocking logging or post-response work;
- CPU-heavy render and serialization;
- streaming boundaries and backpressure.

React `cache` can deduplicate calls in an appropriate React server lifecycle; it is not a general cross-request LRU. Use application caching only with explicit identity and memory policy.

Never improve cache hit rate by weakening tenant or permission keys.

## 20. Hydration cost

Reduce hydration cost by:

- keeping server-only components out of the client graph in an RSC architecture;
- moving client boundaries down;
- serializing only necessary props;
- avoiding duplicated large data blobs;
- code-splitting non-critical interactive regions;
- using native HTML behavior where JavaScript adds no value;
- avoiding a second post-hydration render for server-known data.

Do not remove interactivity or accessibility to reduce JavaScript without a product decision.

## 21. JavaScript and browser work

When profiling identifies hot JavaScript:

- reduce algorithmic complexity first;
- build indexes for repeated lookup;
- cache pure expensive results at the correct scope;
- batch DOM reads and writes;
- use passive listeners where semantically correct;
- coalesce high-frequency pointer/scroll/resize work;
- move heavy independent CPU work to a Worker;
- avoid parsing or cloning large data repeatedly;
- bound caches and queues.

Micro-optimizations in cold render code should not displace clarity.

## 22. Memory and lifecycle

Look for retained:

- subscriptions/listeners without cleanup;
- timers and observers;
- module/global caches without bounds;
- hidden Activity trees retaining state and DOM;
- object URLs, media, workers, and widget instances;
- closures retaining large data;
- pending promises and retry queues;
- detached DOM nodes.

A performance fix that trades bounded latency for unbounded memory is not complete. Measure steady state and repeated navigation, not only first render.

## 23. Common false positives

Do not report these without evidence:

- An inline callback or object exists.
- A component rerenders.
- `memo`, `useMemo`, or `useCallback` is absent.
- A short array uses `filter` and `map` separately.
- A barrel import exists.
- A small clone occurs in a cold path.
- A provider value is allocated occasionally.
- A small list is not virtualized.
- A dependency has a large installed size but is not in the client bundle.
- A transition is absent when the interaction is already responsive.

## 24. Common harmful optimizations

- Memoizing everything before profiling.
- Deep custom prop comparisons.
- Stale callbacks with intentionally missing dependencies.
- Moving local state global to avoid parent renders.
- Splitting into many tiny chunks.
- Preloading every possible route.
- Caching user data without correct identity scope.
- Disabling Strict Mode to reduce development render counts.
- Hiding hydration warnings instead of fixing mismatches.
- Virtualizing a small list while breaking keyboard/screen-reader behavior.
- Removing validation or error handling from a hot path without equivalent protection.

## 25. Performance completion gate

Before claiming success, confirm:

- A representative baseline and target were defined.
- The production bottleneck category was demonstrated.
- The smallest relevant change was applied.
- Correctness, accessibility, security, and compatibility remain intact.
- Improvement was remeasured under comparable conditions.
- Bundle, server, hydration, memory, or browser side effects were checked as applicable.
- Compiler and memoization behavior was validated in the actual production build.
- Remaining uncertainty and measurement limitations are stated.
