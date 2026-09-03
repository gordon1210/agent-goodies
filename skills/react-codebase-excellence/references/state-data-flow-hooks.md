# State, Data Flow, and Hooks

Read this reference when designing state, reducers, providers, custom Hooks, URL state, form state, server state, external stores, or update flows. The central question is not “which state library should we use?” but “what is the source of truth, who owns it, and when may it change?”

## 1. Classify each value

Before adding state, classify the value:

| Kind | Examples | Typical owner |
|---|---|---|
| Props | selected account, permissions, configuration | parent or framework |
| Derived render value | filtered rows, full name, validation summary | calculate during render |
| Local UI state | open disclosure, active tab, draft text | nearest stable component |
| Form state | fields, touched/dirty, submit status | native form or established form layer |
| URL state | route, page, filter, selected resource | router/search parameters |
| Server state | remote entities, freshness, retries, invalidation | loader or data cache |
| External source | media query, browser store, imperative SDK | subscription adapter |
| Intentional snapshot | initial value retained for comparison | local state/ref with explicit semantics |
| Process/request state | server cache, request context | server/framework, never client component state |

Do not copy a value into state merely because it is used more than once. Every duplicate source creates synchronization and invalidation work.

## 2. Store the minimum source of truth

Prefer:

```tsx
function Profile({ firstName, lastName }: Props) {
  const fullName = `${firstName} ${lastName}`;
  return <span>{fullName}</span>;
}
```

over synchronizing derived state:

```tsx
function Profile({ firstName, lastName }: Props) {
  const [fullName, setFullName] = useState('');

  useEffect(() => {
    setFullName(`${firstName} ${lastName}`);
  }, [firstName, lastName]);

  return <span>{fullName}</span>;
}
```

The effect version renders stale data first, adds another update, and introduces a state combination that should not exist.

State is justified when the value can change independently, is an intentional historical snapshot, or is edited before it is committed upstream.

## 3. Shape state to prevent contradictions

Avoid separate values that can disagree:

```tsx
const [status, setStatus] = useState<'idle' | 'saving' | 'success' | 'error'>('idle');
```

is usually safer than several flags such as `isSaving`, `isSaved`, and `hasError` when only one mode may exist.

Prefer IDs over duplicated selected objects when the object already lives in a collection:

```tsx
const [selectedId, setSelectedId] = useState<string | null>(null);
const selected = items.find((item) => item.id === selectedId) ?? null;
```

Normalize collections when independent updates would otherwise require deeply nested mutation, but do not normalize small local state into database-like tables without benefit.

## 4. Immutability is semantic

React state updates must create new values along every changed path. Do not mutate an object and set the same reference.

Prefer focused updates:

```tsx
setDraft((current) => ({ ...current, title: nextTitle }));
```

For nested structures, consider whether the state shape is too deep before adding a general immutable-update dependency.

Do not clone the entire application graph on every keystroke. Keep frequently edited state local and narrow.

Mutable values are appropriate in refs or external systems when they do not directly define rendered output. The boundary between mutable source and React rendering still needs a correct subscription.

## 5. Update queues and functional updates

Use functional updates when the next value depends on the queued previous value:

```tsx
setCount((count) => count + 1);
```

This avoids stale closure problems and composes with batching. Do not use functional syntax mechanically when the next value is independent:

```tsx
setSelectedId(item.id);
```

React batches updates according to the root and runtime behavior. Do not rely on reading state immediately after a setter. State variables are snapshots for the current render.

When multiple fields must transition atomically under domain rules, either update one structured state value or use a reducer. Do not scatter coordinated setters across unrelated callbacks and effects.

## 6. Initialize state deliberately

Use lazy initialization for expensive pure computation:

```tsx
const [index] = useState(() => buildIndex(initialItems));
```

The initializer may run more than once in development checks, so it must not mutate external state, consume a one-shot resource, or issue I/O.

A prop named `initialX` or `defaultX` communicates snapshot semantics. A prop named `x` usually implies current controlled data. Do not initialize from a current prop and then silently ignore later prop changes unless that is the documented contract.

## 7. Reset, preserve, or migrate state intentionally

React preserves state by component identity and tree position.

Use a stable domain `key` to reset an entire subtree when identity truly changes, for example switching from editing one user to another. Do not use a random or ever-changing key to force effects or hide stale state.

For partial reset:

- update the relevant state in the event that changes identity;
- model drafts by resource ID;
- lift the draft owner if it must survive navigation;
- use the router or form layer's reset lifecycle when it owns the workflow.

An effect that resets state after render can show one frame of old data and trigger child effects with the wrong identity. Prefer identity-aware structure or event-time changes.

## 8. State placement

Keep state at the lowest common owner that needs to coordinate it.

Lift state when:

- siblings must agree;
- a parent controls selection or ordering;
- state must survive replacement of a presentational child;
- a stable integration boundary owns persistence or validation.

Keep state local when:

- no other component needs it;
- frequent updates would invalidate a broad tree;
- it is an implementation detail of an accessible primitive;
- lifting would expose setters without a domain reason.

Do not equate “shared by two components” with “global.” A small provider or route owner may be enough.

## 9. Reducers

A reducer is useful when:

- transitions have names and invariants;
- several fields change together;
- the same transitions are triggered from multiple places;
- event logs or deterministic transition tests add value;
- the next state depends on the previous state in nontrivial ways.

A reducer should remain pure:

```tsx
type Action =
  | { type: 'titleChanged'; title: string }
  | { type: 'submitted' }
  | { type: 'failed'; message: string };
```

Effects, navigation, requests, and telemetry belong outside the reducer. Do not encode commands by mutating action objects or performing I/O inside the reducer.

Use exhaustive checks for closed action sets. Avoid a single action with many optional fields that recreates unstructured setters.

A reducer is not automatically better for multiple `useState` calls. Keep simple independent state simple.

## 10. Context

Context transports a value through a subtree. It does not provide selective subscriptions or persistence by itself.

Use context when:

- a coherent component family shares state/actions;
- a cross-cutting value such as theme, locale, or authenticated session is genuinely needed through a subtree;
- passing the value through many uninterested layers would obscure APIs;
- a provider is the natural owner.

Avoid context when:

- only one or two levels need the value;
- the value changes at high frequency across a broad tree;
- consumers need fine-grained selectors and the current model rerenders too much;
- module configuration or an ordinary imported constant is enough;
- it would hide a dependency that should be explicit in a reusable component.

Provider value identity matters when consumers observe it. In a non-compiler codebase, memoize a compound provider value only when it prevents meaningful invalidation or satisfies an identity contract. Do not wrap every provider value automatically.

Split data and actions or separate contexts when update frequency and consumer sets differ materially. Measure before turning one clear provider into many layers.

## 11. External stores and `useSyncExternalStore`

An external store is a mutable source outside React, such as a custom store, browser API, SDK, or global cache.

A correct adapter needs:

- a subscribe function with symmetrical unsubscribe;
- a stable snapshot whose identity changes only when observed data changes;
- a server snapshot for SSR when the source is read during server rendering;
- consistent behavior during concurrent renders;
- clear ownership of initialization and disposal.

`useSyncExternalStore` exists to let React read external mutable sources without tearing. Do not replace it with “subscribe in an effect, copy into state” when the source can change between render and subscription.

Avoid returning a freshly allocated object from `getSnapshot` on every call. Cache or select a stable snapshot according to store semantics.

When using an established state library, follow its current React integration rather than wrapping it again unless a concrete gap exists.

## 12. Server state

Remote data has concerns local state does not:

- loading and stale data;
- request deduplication;
- retries and backoff;
- invalidation and refetch;
- pagination and partial data;
- optimistic mutation and rollback;
- authentication and tenant scope;
- offline and reconnect behavior;
- cache lifetime and garbage collection.

Use the repository's framework loader or data cache when it already owns these concerns. Do not copy query results into local or global state solely to make them “available.” Select or derive from the cache.

Local editable drafts may intentionally diverge from server state. Define when they initialize, rebase, conflict, save, discard, and react to background updates.

Do not treat a server cache as authorization. Cached data must remain correctly scoped per user, tenant, and permission.

## 13. URL state

Use the URL for state that users should be able to link, bookmark, navigate back/forward through, or restore on reload, such as resource identity, tabs, pagination, filters, and search.

Define:

- parsing and validation;
- defaults and canonicalization;
- replace versus push history behavior;
- multi-value and encoding rules;
- invalid parameter behavior;
- server-render and hydration consistency;
- whether updates are urgent or transitioned;
- interaction with loader invalidation.

Do not maintain an independent component copy and URL copy without a clear source of truth. Avoid updating the URL on every keystroke when that creates unusable history or expensive reloads; use deliberate commit/debounce semantics owned by the router layer.

## 14. Form state

Start with the browser and the repository's established form model.

Native uncontrolled forms are often appropriate when:

- the browser can own field values;
- values are needed at submission time;
- native validation/autofill semantics matter;
- per-keystroke React rendering adds no value.

Controlled fields are appropriate when:

- rendering or validation must react immediately to the current value;
- formatting or dependent fields require a React source of truth;
- the component is a controlled design-system primitive.

Do not alternate controlled and uncontrolled mode. Preserve input method editor composition, cursor position, autofill, reset, and disabled/read-only semantics.

A form library is justified by real workflow complexity, not merely the presence of several fields. Avoid layering a second form state model over React 19 Actions or a framework action unless responsibilities are explicit.

## 15. Refs as non-rendering state

A ref is suitable for:

- DOM nodes and imperative handles;
- timer or observer handles;
- latest non-rendering metadata used by an external callback;
- previous values used for diagnostics or comparison;
- mutable integration objects whose changes should not render.

A ref is not suitable for visible values that must update the UI. Writing `ref.current` does not schedule rendering.

Do not read or write refs during render except for safe initialization patterns explicitly supported by React. Render-time ref mutation can break purity and compiler assumptions.

## 16. Custom Hooks

A custom Hook shares stateful logic, not state instances. Each call owns its own state unless it subscribes to a shared source.

A Hook contract should define:

- inputs and reactive behavior;
- returned data and action stability where material;
- loading/error state;
- subscription or request ownership;
- cleanup and cancellation;
- server-render behavior;
- whether it may suspend or throw;
- version/framework requirements.

Do not name an ordinary function `useX` unless it follows Hook call rules. Do not call a Hook conditionally by hiding it inside another function.

Prefer domain-facing results over leaking the implementation library's entire object when that coupling would make replacement or testing harder. Conversely, do not wrap an established data Hook in a trivial pass-through abstraction with no stable contract.

## 17. Rules of Hooks and Rules of React

- Call Hooks only at the top level of components and custom Hooks, except for APIs such as React 19 `use` that explicitly have different call rules.
- Call React components through JSX, not as ordinary functions.
- Do not dynamically mutate Hooks or components after definition.
- Do not pass Hooks around as values to be invoked later.
- Keep render pure and state immutable.
- Do not conditionally return before some Hook calls on one render and reach them on another.

A lint suppression does not change React's runtime contract. Restructure the component or Hook.

## 18. State and concurrency

Write updates so they remain correct if React:

- batches multiple updates;
- starts rendering and abandons the result;
- renders a component more than once in development;
- delays non-urgent updates;
- reveals a Suspense fallback;
- hides and restores a React 19.2 Activity subtree.

Do not perform irreversible work in render or state updater functions. Do not assume every intermediate state commits to the DOM.

External stores and imperative systems must tolerate subscription replay and cleanup. Async completion must verify that it still belongs to the current resource or mutation.

## 19. Common failure modes

- Derived state synchronized through an effect.
- Prop copied to state without intentional snapshot semantics.
- State object mutated in place.
- A stale closure increments from an old value.
- Several setters create a briefly impossible state observed by effects.
- A random `key` forces remounting to “refresh” data.
- A giant context invalidates the application on each keystroke.
- Remote data is copied into a global store and diverges from the query cache.
- URL and component state update each other in a loop.
- An external mutable store is read directly during render without a React-compatible subscription.
- A custom Hook hides a conditional Hook call.
- A reducer performs I/O.
- A ref stores visible state and the UI becomes stale.

## 20. False-positive controls

Do not report these without a concrete trigger and impact:

- Multiple `useState` calls exist.
- A reducer is not used.
- State is local rather than global.
- Context is used for a stable coherent subtree.
- A provider value is not memoized in a cold path.
- A controlled input rerenders on keystrokes as designed.
- A ref stores an imperative handle.
- A server query is not copied into another store.
- A custom Hook is small but encodes a real lifecycle boundary.

## 21. Completion gate

Before completing state work, confirm:

- One source of truth exists for each value.
- State cannot enter contradictory combinations relevant to the workflow.
- Updates are immutable and use functional form where previous queued state matters.
- Reset and preservation follow domain identity.
- Local, URL, form, server, and external state have explicit owners.
- Reducers and Hooks remain pure where required.
- External subscriptions are concurrent-safe and clean up correctly.
- Async completion cannot overwrite newer state.
- Tests cover the meaningful transition and ownership boundaries.
