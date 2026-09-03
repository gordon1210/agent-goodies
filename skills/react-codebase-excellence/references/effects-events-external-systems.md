# Effects, Events, and External Systems

Read this reference when code uses `useEffect`, `useLayoutEffect`, `useInsertionEffect`, subscriptions, timers, observers, browser APIs, analytics, storage, third-party widgets, or imperative resources. An Effect is a synchronization boundary, not a general place for code that should run “after render.”

## 1. Effect decision tree

Before adding an Effect, ask in order:

1. Can the value be calculated from props and state during render?
2. Is the work caused by a specific user or application event?
3. Does the repository's router, loader, data cache, form layer, or framework already own the lifecycle?
4. Is the code synchronizing React with an external system that exists independently of rendering?
5. Does the work actually require post-paint or pre-paint timing?

Use an Effect only when step 4 is true or the framework explicitly requires an effect lifecycle.

Typical legitimate external systems:

- network connections and subscriptions;
- browser event targets and observers;
- timers tied to mounted UI;
- imperative DOM or media APIs;
- third-party widgets;
- storage synchronization;
- telemetry caused by visibility/mount state;
- non-React stores or SDKs.

## 2. Derive during render

Do not use an Effect to calculate data that render can derive:

```tsx
const visibleItems = items.filter((item) => matches(item, query));
```

If the calculation is expensive, first confirm it is a measured bottleneck. Then use the repository's compiler or focused memoization policy. State plus Effect adds stale intermediate output and more work.

Do not use an Effect to notify a parent of data that the parent can calculate from the same inputs. Lift the source of truth or pass the event that caused the change.

## 3. Put interaction logic in the event

If code runs because the user clicked, submitted, selected, or dismissed something, put it in that event path:

```tsx
function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
  event.preventDefault();
  submitDraft(draft);
}
```

Do not set `submitted = true` and use an Effect to perform the submission. That separates cause from work, can repeat under resets/remounts, and creates hidden state.

An Effect may still synchronize the result with an external system when that synchronization is not owned by the event itself.

## 4. Effect lifecycle model

An Effect describes how to start synchronizing with the current reactive inputs and how to stop that exact synchronization.

```tsx
useEffect(() => {
  const connection = connect(roomId);
  connection.open();

  return () => {
    connection.close();
  };
}, [roomId]);
```

When `roomId` changes, cleanup for the old room must run before setup for the new room. On unmount, cleanup must release the remaining resource.

Do not think only in terms of “mount” and “unmount.” Dependencies can change repeatedly, and development Strict Mode intentionally exercises setup and cleanup.

## 5. Dependency correctness

Every reactive value read by an Effect belongs in its dependency model unless the code is deliberately made non-reactive through a supported mechanism.

Reactive values include:

- props and state;
- values and functions declared in the component;
- context and Hook results;
- derived objects created during render.

Do not omit a dependency to request “run once.” If the Effect truly represents process-global initialization, move ownership outside the component or use a framework application boundary.

To reduce dependencies correctly:

- move constants outside the component;
- construct effect-only objects inside the Effect;
- use functional state updates when only prior state is needed;
- move interaction code into handlers;
- split independent synchronization processes;
- stabilize a dependency only when its identity is semantically important;
- on React 19.2, use an Effect Event for non-reactive logic that must observe current values.

A suppression is acceptable only when the non-reactive invariant is real, documented, and protected by tests or architecture.

## 6. Object and function dependencies

A freshly created object or function changes identity on every render. Do not automatically wrap it in `useMemo` or `useCallback`.

Prefer moving an effect-local object into the Effect:

```tsx
useEffect(() => {
  const options = { serverUrl, roomId };
  const connection = createConnection(options);
  return () => connection.disconnect();
}, [serverUrl, roomId]);
```

Prefer moving a helper outside the component when it does not use reactive values.

Use callback memoization only when another contract requires stable identity, such as a subscription API, memoized child with measured cost, or public Hook result. React Compiler may handle many identity optimizations, but it does not excuse incorrect dependencies.

## 7. React 19.2 `useEffectEvent`

Use `useEffectEvent` when an Effect has non-reactive logic that needs current values but should not cause resubscription.

Conceptually:

```tsx
const onConnected = useEffectEvent(() => {
  showNotification(`Connected with ${theme.name}`);
});

useEffect(() => {
  const connection = connect(roomId);
  connection.on('connected', onConnected);
  return () => connection.close();
}, [roomId]);
```

Changing `roomId` must reconnect; changing `theme` should affect the next notification without reconnecting.

Constraints:

- React 19.2+ only.
- Call Effect Events from Effects or effect-owned callbacks, not as ordinary event handlers.
- Do not use them to hide values that should resynchronize the external system.
- Follow the installed hooks lint version; Effect Events are intentionally omitted from dependencies.

For React 18 or 19.0/19.1, restructure the synchronization or use the repository's established latest-callback adapter. Preserve equivalent lifecycle tests.

## 8. Cleanup symmetry

Every setup operation should have a matching cleanup when the external system retains anything:

| Setup | Cleanup |
|---|---|
| `addEventListener` | `removeEventListener` with same target/type/options/listener |
| subscription | unsubscribe/dispose |
| interval/timeout | clear interval/timeout |
| observer `.observe()` | disconnect or unobserve |
| connection open | close/disconnect |
| widget mount | destroy/unmount |
| object URL creation | revoke URL |
| abortable request | abort when ownership ends |
| DOM mutation | restore when required by contract |

Cleanup should not perform unrelated new work. It must tolerate partial setup and repeated development lifecycles.

A missing cleanup is not only a memory concern. It can cause duplicate events, stale updates, leaked credentials, background CPU/network use, focus corruption, or writes to the wrong resource.

## 9. Development Strict Mode

Development Strict Mode may run setup, cleanup, and setup again to expose lifecycle defects. Correct code should produce the same externally observable state as one setup.

Do not “fix” duplicate behavior with:

```tsx
const didRun = useRef(false);
if (didRun.current) return;
didRun.current = true;
```

This hides missing cleanup and still breaks if the real resource identity changes or the component remounts.

For globally one-time initialization, use a process/application-owned idempotent initializer outside component lifecycle, and define teardown separately if needed.

## 10. Async work in Effects

An Effect callback itself must not be `async` because it must return cleanup, not a Promise. Start an inner async operation.

Protect against:

- stale completion after dependencies change;
- out-of-order responses;
- unmount;
- abortable network work continuing without an owner;
- state changes after the requested resource is obsolete;
- swallowed errors.

A typical pattern:

```tsx
useEffect(() => {
  const controller = new AbortController();
  let active = true;

  async function load(): Promise<void> {
    try {
      const result = await fetchResource(resourceId, controller.signal);
      if (active) {
        setResource(result);
      }
    } catch (error) {
      if (!controller.signal.aborted && active) {
        setError(toDisplayableError(error));
      }
    }
  }

  void load();

  return () => {
    active = false;
    controller.abort();
  };
}, [resourceId]);
```

The exact pattern should follow the repository. An `active` guard prevents stale state writes; abort may also save resources. Abort alone is insufficient if downstream work does not honor it.

Prefer a router loader or data library when it already owns caching, request deduplication, invalidation, retries, and navigation cancellation.

## 11. Subscriptions

A subscription Effect must define:

- source identity;
- event types and ordering;
- initial snapshot;
- duplicate and reconnect behavior;
- cleanup;
- backpressure or update coalescing for high-frequency sources;
- error and retry behavior;
- visibility and offline behavior if relevant.

For an external mutable store read during render, use `useSyncExternalStore` or the store library's React adapter rather than copying events into local state after paint.

Do not recreate a global subscription for every leaf consumer if a shared owner is more appropriate. Conversely, do not centralize unrelated subscriptions into one provider without lifecycle reason.

## 12. Event listeners

Use the narrowest target and correct listener options. Global listeners need special scrutiny:

- Can the event be handled on the relevant element instead?
- Are listeners duplicated across component instances?
- Is passive behavior appropriate for touch/scroll listeners?
- Does cleanup use the same options and callback identity?
- Does the handler need the latest state or should state changes resubscribe?
- Does the listener interfere with nested dialogs, shortcuts, input composition, or browser defaults?

Keyboard shortcuts must respect focus context, editable elements, platform modifiers, and accessibility. A document-level listener that steals common keys can be a product defect.

## 13. Timers and clocks

Define whether time is:

- a display concern;
- a deadline;
- a polling schedule;
- a debounce/throttle boundary;
- an animation frame;
- a retry backoff.

Store timer handles in effect scope or refs, clear them, and account for browser throttling and background tabs. Do not assume an interval fires exactly on schedule. Compute deadlines from a clock rather than counting ticks when accuracy matters.

For debounced input, update the visible controlled value urgently and debounce the external query or committed value. Do not delay the input's own value update.

Use fake clocks in tests only with deliberate microtask and scheduler handling.

## 14. DOM measurement and mutation

Prefer declarative layout and CSS. Use refs plus layout synchronization when measurement is genuinely required.

`useLayoutEffect` runs before paint and can block it. Keep work narrow:

- measure only relevant nodes;
- batch reads before writes;
- avoid repeated forced layout;
- respond to ResizeObserver or other platform signals when size can change;
- clean up observers;
- define SSR behavior because layout effects do not run on the server.

A ref callback can own node-specific setup. In React 19 it may return cleanup; in React 18 use explicit detach handling or an Effect according to the integration.

`useInsertionEffect` is primarily for style-injection library authors. Application code should rarely need it.

## 15. Third-party widgets

An imperative widget integration needs:

- stable container ownership;
- one instance per intended lifecycle;
- update versus recreate policy;
- destruction and listener cleanup;
- server-safe imports;
- strict-mode resilience;
- error containment;
- focus and accessibility integration;
- sanitization and CSP compatibility;
- behavior when hidden by Suspense or Activity.

Do not allow both React and the widget to own the same DOM subtree. React may own the container; the widget owns its internal nodes.

## 16. Storage and cross-tab synchronization

Storage reads and writes are external-system work.

- Parse untrusted stored values and version schemas.
- Keep data minimal and avoid secrets or unnecessarily sensitive data.
- Handle quota, disabled storage, malformed values, and migrations.
- Avoid blocking repeated storage reads during render.
- Use the `storage` event or an external-store adapter for cross-tab updates.
- Define whether server rendering has a default snapshot and how hydration avoids flicker.

Do not mirror every state update into storage without a retention, privacy, and failure policy.

## 17. Analytics and telemetry

Send analytics for meaningful events or visibility states with an explicit ownership model.

- Do not send during render.
- Avoid duplicate events under Strict Mode, retries, remounts, or navigation replay.
- Do not include secrets, raw form values, personal data, or unbounded payloads without approved policy.
- Distinguish “component mounted” from “content actually became visible” when that matters.
- Keep telemetry failure non-blocking unless the product contract says otherwise.

A mount Effect is not automatically an accurate page-view signal in an SSR, nested route, Suspense, or Activity application.

## 18. Browser and media APIs

For APIs such as media queries, geolocation, clipboard, visibility, online status, observers, or media playback:

- feature-detect according to browser policy;
- handle permissions and user activation;
- define unavailable and denied states;
- clean up listeners;
- avoid server imports that touch browser globals;
- preserve accessible alternatives;
- use an external-store adapter when rendering must track a mutable browser snapshot.

Do not make browser capability checks during SSR render produce different initial markup unless hydration is designed for it.

## 19. Effect splitting and ordering

Each Effect should synchronize one coherent process. Split effects when setup, dependencies, or cleanup are independent.

Do not split a single atomic lifecycle into several Effects merely for line count. Relative effect ordering can become a hidden contract and is harder to maintain.

If one Effect sets state solely to trigger another Effect, collapse the chain into the original event or synchronization path. Effect chains often render multiple unnecessary intermediate states.

## 20. Testing Effects

Test observable outcomes:

- subscription receives current data;
- dependency change disconnects old source and connects new source;
- unmount cleans up;
- stale request cannot overwrite newer data;
- abort and errors behave correctly;
- Strict Mode does not duplicate external effects;
- timers stop and do not update obsolete state;
- server render does not access browser-only APIs.

Do not assert exact effect call counts unless the count is itself an external contract. Development and production lifecycles may differ.

## 21. Common failure modes

- Derived state in an Effect.
- Event-caused work relayed through a flag and Effect.
- Missing dependency suppressed to force mount-only behavior.
- Object dependency recreated every render, causing reconnect loops.
- Listener or timer without cleanup.
- Async completion overwrites a newer selection.
- Abort errors displayed as user failures.
- DOM measurement in a passive Effect causes visible jump.
- Storage parsed as trusted data.
- Global shortcut captures typing.
- Third-party widget instantiated twice under Strict Mode.
- Analytics duplicated by remounts.
- `useEffectEvent` used as a dependency escape hatch.

## 22. False-positive controls

Do not report these without concrete impact:

- An Effect exists.
- A dependency array contains an object when its identity is intentionally the synchronization key.
- An Effect runs after every render because the external system requires it and cleanup is correct.
- `useLayoutEffect` is used for verified pre-paint measurement.
- A stable callback is not memoized when no identity contract exists.
- A fetch occurs in an Effect in a client-only application that has no established loader/data layer and handles races correctly.
- A mount Effect initializes an approved imperative widget with complete cleanup.

## 23. Completion gate

Before completing Effect work, confirm:

- The code truly synchronizes an external system.
- Event-time and render-time logic were not displaced into an Effect.
- Dependencies reflect reactive inputs honestly.
- Setup and cleanup are symmetric and Strict-Mode-safe.
- Async work handles stale completion, cancellation, and errors.
- Global listeners, timers, observers, and widgets have explicit ownership.
- SSR and hydration do not touch browser-only state incorrectly.
- Tests exercise lifecycle outcomes rather than implementation call counts.
