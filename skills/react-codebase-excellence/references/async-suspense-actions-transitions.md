# Async Work, Suspense, Actions, and Transitions

Read this reference when implementing data loading, code splitting, mutations, Suspense, transitions, optimistic UI, React 19 Actions, `use`, retries, or cancellation. Async UI needs explicit ownership and user-facing states; React APIs coordinate rendering but do not replace application guarantees.

## 1. Classify the async operation

Determine whether the operation is:

- initial route or page data;
- nested or deferred data;
- client-triggered query;
- mutation or form submission;
- background refresh;
- code/module loading;
- image, font, stylesheet, or script loading;
- subscription or stream;
- local CPU-heavy computation;
- server rendering or RSC work.

Then identify the owner: framework, router, query cache, form layer, component, worker, browser, or server platform.

Do not put every Promise in component state. Do not make React own a lifecycle already handled by a router or cache.

## 2. Model user-visible states

For each operation, define applicable states:

- not requested;
- pending with or without previous content;
- partial data;
- success;
- empty result;
- validation failure;
- authorization failure;
- retryable or terminal error;
- cancelled or superseded;
- optimistic state;
- confirmed state;
- rollback or conflict;
- stale data during refresh.

A spinner is not a state model. Preserve context where useful, avoid layout shift, keep actions understandable, and make errors recoverable.

Never show a loading state when no actual work is pending. Conversely, do not leave a mutation enabled if duplicate submission would violate the domain contract.

## 3. Promise ownership

Every Promise used by React should have a stable owner and lifetime.

Ask:

- Who creates it?
- Is its identity stable for the resource key?
- Who caches or deduplicates it?
- How is it cancelled or abandoned?
- Where is rejection handled?
- Is the result scoped to the current user, tenant, locale, permission, and request?
- Can it be reused across renders or requests safely?

Creating a Promise during every client render and passing it to React 19 `use` produces unstable suspension and is unsupported unless a framework/library owns caching.

Module-level caches on a server can leak data across users. Request-local React `cache` deduplication is not automatically a durable cross-request cache.

## 4. Eliminate accidental waterfalls

A waterfall exists when independent work starts only after unrelated work completes.

Bad:

```tsx
const account = await loadAccount(accountId);
const flags = await loadFlags();
```

when neither depends on the other.

Better:

```tsx
const accountPromise = loadAccount(accountId);
const flagsPromise = loadFlags();
const [account, flags] = await Promise.all([accountPromise, flagsPromise]);
```

Use parallel execution only when:

- work is independent;
- resource pressure remains bounded;
- fail-fast semantics are acceptable or errors are handled individually;
- authorization prerequisites are not bypassed;
- cancellation and tracing remain coherent.

“Start early, await late” can improve latency, but do not scatter orphaned Promises that may reject without an owner.

For partial dependencies, start every currently independent branch and await prerequisites only where needed. Prefer clear control flow over introducing a scheduling library for a small graph.

## 5. Suspense contract

Suspense coordinates rendering when a supported resource or lazy module suspends. It does not automatically fetch data or catch ordinary event-handler errors.

A boundary defines:

- which existing content remains visible;
- fallback content and layout;
- reveal grouping;
- retry and error boundary relationship;
- server streaming and hydration unit;
- accessibility of pending content;
- whether transitions should avoid replacing already visible content.

Place boundaries around meaningful user experience regions. Too high creates a blank page; too low creates fallback confetti and excessive coordination.

Fallbacks should preserve layout and context where possible. Do not make every fallback a global spinner.

## 6. Suspense data sources

Use only data sources integrated with Suspense by the framework or an established library, or deliberately implement the required resource cache contract.

Do not throw arbitrary fetch Promises from components without stable caching and invalidation. A naïve wrapper can:

- refetch on every render;
- retain data forever;
- leak across users on the server;
- lose rejection handling;
- have no invalidation or cancellation policy;
- conflict with framework rendering.

React 19 `use` makes resource reading more direct but does not solve ownership, cache scope, invalidation, or security.

## 7. Lazy code loading

Use `lazy` or framework code splitting for components that are expensive enough and reached late enough to justify a separate chunk.

Review:

- chunk size and shared dependencies;
- loading and error UI;
- preloading/prefetching at a real intent signal;
- SSR support;
- named export adaptation;
- retry behavior after a chunk failure;
- deploy version skew and stale HTML;
- whether splitting increases request overhead more than it saves.

Do not dynamically import tiny always-used components. Do not place the lazy declaration inside render.

## 8. Transitions

A transition marks state updates as non-urgent so urgent interactions can remain responsive.

Appropriate examples:

- navigating or changing a large view while preserving current content;
- updating an expensive result panel after an urgent selection;
- background tab or filter content rendering;
- router transitions when the router integrates with React.

Do not wrap the state update controlling a text input's visible value in a transition. Keep typing urgent; defer the expensive derived view with a separate state update or `useDeferredValue`.

Transitions do not make synchronous computation cheaper. Move CPU-heavy work, reduce it, virtualize, or use a worker when needed.

After an `await`, updates may need a new transition boundary depending on the React version and API path. Test pending semantics against the installed version rather than assuming all async continuations remain transitioned.

## 9. `useTransition`

`useTransition` provides a pending signal scoped to transitions started through its function.

Use the pending state to communicate real progress without needlessly hiding usable content. Define whether controls:

- stay enabled for superseding transitions;
- disable to prevent invalid duplicates;
- expose `aria-busy` or status text;
- preserve focus;
- allow cancellation through a new selection.

Do not derive business completion from `isPending` alone. A transition can coordinate rendering around work; the server mutation still needs its own result and error contract.

## 10. `useDeferredValue`

`useDeferredValue` lets a rendered consumer lag behind an urgent source value.

Common use:

```tsx
const deferredQuery = useDeferredValue(query);
const isStale = deferredQuery !== query;
```

The input remains responsive while an expensive result view catches up.

It does not debounce network requests by itself. The producer may still run for each value. Combine with the repository's request/cache policy if network coalescing is needed.

Provide a visual stale indication only when it helps users; do not dim or announce on every keystroke by default.

## 11. React 19 Actions

An Action is an async transition-aware operation used for mutations and form workflows. React can coordinate pending state, errors, optimistic state, and form reset, but domain correctness remains explicit.

An Action must define:

- input parsing and validation;
- authentication and resource-level authorization;
- idempotency or duplicate-submission handling;
- transaction and partial-failure behavior;
- error classification for user versus telemetry;
- cache invalidation/revalidation;
- optimistic state and rollback;
- focus and announcement after failure/success;
- abort/supersession behavior where supported.

Treat a Server Function Action as a public endpoint. A hidden button or client guard provides no security.

## 12. Form `action` and `formAction`

React 19 allows functions as form Actions. Preserve native form semantics:

- field `name` values and `FormData` encoding;
- submitter-specific `formAction`;
- Enter-key submission;
- browser validation policy;
- disabled controls not being submitted;
- multiple submit buttons;
- uncontrolled form reset after success;
- progressive enhancement where the framework supports it;
- accessible validation and status.

Do not prevent default submission automatically when the framework or React Action model owns it.

A successful uncontrolled form may reset. If preserving values is required, use controlled state or a deliberate failure/result contract rather than restoring fields in an unrelated Effect.

## 13. `useActionState`

`useActionState` manages state returned by an Action and exposes pending status.

The Action receives the previous state plus submitted arguments. Keep the returned state serializable when the framework needs to cross server/client boundaries.

Use returned state for meaningful results such as field errors or confirmation data. Do not return raw exceptions, database rows, secrets, stack traces, or unbounded payloads.

Define initial state carefully so server-rendered and hydrated markup agree. A framework may support a permalink/progressive enhancement path; follow its exact contract.

Do not mirror `useActionState` pending/result into separate component state unless another owner genuinely needs an independent snapshot.

## 14. `useFormStatus`

`useFormStatus` reads status for the parent form submission. It belongs in a descendant of that form, such as a submit button or status region.

Use it to:

- disable or label the submitting action when duplicates are invalid;
- show real pending status;
- expose accessible busy/status information;
- inspect submitted data only when needed and safe.

Do not assume it observes an unrelated form or a form rendered by the same component outside the required parent relationship. Test nested forms and multiple submitters according to actual markup.

## 15. `useOptimistic`

Optimistic UI should make the likely successful result visible before confirmation while preserving a trustworthy rollback path.

Define:

- stable identity for optimistic records;
- how pending and confirmed records reconcile;
- what happens if results arrive out of order;
- whether multiple optimistic mutations compose;
- error rollback or conflict display;
- duplicate prevention;
- accessibility announcement policy;
- whether destructive actions should be optimistic at all.

Do not fabricate a permanent ID that can collide with server data. Keep a client mutation identifier separate from the eventual domain ID.

For high-risk destructive or financial operations, an optimistic final-success presentation may be inappropriate. Product semantics outrank API availability.

React 18 can implement equivalent behavior with the existing state/data layer; do not add a pseudo-`useOptimistic` abstraction solely to copy React 19 syntax.

## 16. React 19 `use`

`use` may read a Promise or context during render.

For Promises:

- pass a stable framework/library-owned Promise;
- pair suspension with an appropriate Suspense boundary;
- pair rejection with an Error Boundary or framework error path;
- preserve request and tenant scope;
- do not recreate the Promise on every client render;
- avoid unsupported try/catch patterns around suspension;
- validate serialized results crossing RSC boundaries.

For context, `use(Context)` can be called conditionally where `useContext` cannot. Do not use this to make component control flow opaque or to bypass a clearer component boundary.

React 18 code must use compatible APIs.

## 17. Errors and retry

Classify errors:

- validation error the user can fix;
- authentication/authorization failure;
- not found or stale resource;
- conflict;
- rate/resource limit;
- transient dependency failure;
- permanent server failure;
- client code/chunk failure;
- cancellation/supersession.

Do not show every failure as “Something went wrong.” Preserve actionable information without leaking internals.

Retry must consider:

- idempotency;
- duplicate mutations;
- retry budget and backoff;
- current connectivity;
- whether credentials or permissions changed;
- whether optimistic state remains valid;
- whether the user already superseded the request.

Error Boundaries are appropriate for render/resource failures. Event and mutation errors usually need explicit local handling or framework action handling.

## 18. Cancellation and supersession

Cancellation means different things:

- the client no longer cares about a query result;
- network work can be aborted;
- server work may already continue;
- a newer navigation or mutation supersedes an older one;
- component unmount ends ownership;
- an RSC cache lifetime ends.

Use an AbortSignal where the underlying operation supports it. Still guard against stale completion because not every layer honors abort.

For mutations, aborting the request does not prove the server rolled back. Design idempotent operations, operation IDs, or reconciliation when outcome can be unknown.

React 19.2 `cacheSignal` applies to RSC cache lifetime, not generic client cancellation.

## 19. Race conditions

Common races:

- response for old selection overwrites new selection;
- repeated autosave commits out of order;
- optimistic delete and background refetch resurrect an item;
- two transitions reveal stale data;
- route navigation completes after logout;
- duplicate form submissions create repeated effects;
- component unmount loses mutation outcome.

Mitigate with resource keys, sequence/mutation IDs, abort, cache ownership, server version checks, idempotency keys, transactional updates, or last-write policy chosen deliberately.

Do not rely on “requests usually finish in order.”

## 20. Server rendering and streaming

For SSR/RSC:

- start independent data work high enough to avoid nested waterfalls;
- scope caches to the correct request or authenticated identity;
- choose Suspense boundaries for useful streaming chunks;
- handle disconnect/abort;
- avoid client-only state in initial render;
- keep serialized data minimal and safe;
- ensure status codes, headers, redirects, and errors remain framework-correct;
- test hydration under slow code and data.

Do not move data loading into a leaf client Effect when the server/framework can render it directly and the repository architecture expects that path.

## 21. Resource hints and preloading

Preload or prefetch only when evidence shows the resource is likely to be needed and early loading improves user experience.

- Use correct resource type, credentials mode, and origin.
- Avoid competing with critical resources.
- Deduplicate framework and React resource hints.
- Trigger intent-based preload on hover/focus only when it benefits likely navigation and does not create excessive network use.
- Consider privacy and authorization before prefetching user-specific resources.

A hint is not a substitute for removing a waterfall or reducing the resource.

## 22. Testing async UI

Tests should cover applicable sequences:

- pending appears only during real work;
- existing content remains or fallback appears as intended;
- success commits the correct data;
- validation and server errors are visible and associated correctly;
- retry does not duplicate an unsafe mutation;
- stale completion cannot overwrite newer state;
- cancellation/unmount prevents obsolete UI updates;
- optimistic state reconciles or rolls back;
- focus remains sensible;
- multiple submissions and submitters behave correctly;
- Suspense and Error Boundaries recover;
- React 18 and 19 paths use only supported APIs.

Use controllable deferred Promises or request fakes rather than arbitrary sleeps. Do not assert exact internal scheduling order.

## 23. Common failure modes

- A client Promise is created during every render and passed to `use`.
- Independent requests form a serial waterfall.
- `Promise.all` bypasses an authorization prerequisite or overloads a service.
- Suspense fallback replaces an entire page for a minor refresh.
- A transition controls the input value and typing lags.
- `useDeferredValue` is mistaken for network debounce.
- Pending state is simulated with a timeout.
- A server Action trusts client-supplied ownership or role data.
- Optimistic state has no rollback or reconciliation identity.
- Aborted mutation is assumed not to have executed server-side.
- A module-level server cache crosses tenants.
- Every error is retried, including validation or authorization failures.

## 24. False-positive controls

Do not report these without concrete impact:

- Requests are sequential when the second genuinely depends on the first.
- A page has one coarse Suspense boundary because the reveal experience is atomic.
- Existing content is replaced by a fallback when that is the intended navigation contract.
- A form disables submission while pending because the operation cannot be safely duplicated.
- Optimistic UI is not used for a destructive or high-risk action.
- Data loads in an Effect in a client-only architecture with correct race handling and no existing loader/cache owner.
- A small always-used component is not lazy-loaded.

## 25. Completion gate

Before completing async work, confirm:

- The operation and Promise have explicit owners and scope.
- User-visible states include real error and cancellation behavior.
- Independent work is parallelized only where safe and bounded.
- Suspense boundaries match the reveal and recovery experience.
- Transitions preserve urgent input responsiveness.
- Actions enforce server-side validation and authorization.
- Optimistic UI has stable identity, reconciliation, and rollback.
- Stale completion and duplicate mutation paths are controlled.
- SSR/RSC caches cannot cross trust boundaries.
- Tests use deterministic async control and exercise observable outcomes.
