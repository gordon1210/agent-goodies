# Components, Composition, and API Design

Read this reference when designing or reviewing components, props, variants, slots, compound components, providers, refs, controlled state, portals, error boundaries, or design-system APIs. Good component architecture makes valid use obvious without forcing every component into the same pattern.

## 1. Start from responsibility and observable behavior

A component boundary is justified when it provides one or more of:

- a coherent UI responsibility;
- local state or lifecycle ownership;
- a reusable semantic interaction;
- a rendering or error isolation boundary;
- a meaningful composition point;
- a public design-system contract;
- independent loading, Suspense, or code-splitting behavior.

Do not extract a component solely because JSX exceeds a line count. Conversely, a small accessible interaction may deserve a component because its behavior must remain consistent.

A component should make clear:

- what data it receives;
- which state it owns;
- which events it emits;
- what element or semantic pattern it renders;
- what happens when data is empty, pending, invalid, or unavailable;
- whether it can be controlled;
- whether and where it forwards a ref.

## 2. Preserve render purity

During render, a component may calculate JSX and derived values from its inputs. It must not:

- mutate props or objects from previous renders;
- write to external stores or storage;
- subscribe, schedule timers, send analytics, or issue imperative DOM updates;
- call state setters unconditionally;
- depend on random, current time, or browser-only values when deterministic SSR output is required;
- call another component as a regular function.

Lazy initialization passed to `useState` is still render-time logic and may be invoked more than once in development. It must remain pure.

## 3. Component identity and remounting

React associates state with a component's type and position. Preserve identity unless reset is intentional.

Avoid defining component types inside another component:

```tsx
function Parent() {
  function Editor() {
    const [value, setValue] = useState('');
    return <input value={value} onChange={(event) => setValue(event.target.value)} />;
  }

  return <Editor />;
}
```

A new component type is created on every parent render, so child state is reset. Move the definition to module scope or render ordinary JSX.

A `key` can intentionally reset a subtree when domain identity changes. Do not use a changing key to hide stale state, effect, hydration, or controlled-input defects.

## 4. Props are a contract

Props should represent stable concepts rather than expose the implementation's internal switches.

Prefer:

- domain-relevant names;
- explicit callback timing and payloads;
- discriminated variants for mutually exclusive modes;
- native semantics where a component wraps a native control;
- defaults that are safe and unsurprising;
- minimal required props.

Avoid:

- mirroring every internal state setter as a prop;
- ambiguous inverse booleans such as `disableNotFound`;
- several booleans whose combinations describe unrelated component modes;
- callbacks named `onChange` that fire for unrelated lifecycle events;
- accepting arbitrary objects when a smaller stable contract is enough;
- spreading untrusted configuration directly onto a DOM node.

### Boolean props: use judgment

Boolean props are correct for genuine independent binary semantics:

```tsx
<TextField disabled required />
```

They become a design smell when each flag selects a component mode or when combinations are invalid:

```tsx
<Dialog compact fullscreen sidebar destructive />
```

Use explicit variants, separate components, or composition when that removes invalid combinations and makes behavior clearer. Do not replace a simple boolean with an elaborate compound API for style.

## 5. Composition choices

Choose the least powerful mechanism that expresses the need.

### Ordinary children

Use `children` when consumers place content in a clear region and the component does not need to control its structure deeply.

### Named slots

Use explicit node props or slot components when several regions have distinct semantics:

```tsx
<Card header={<AccountHeader />} footer={<Actions />}>
  <Details />
</Card>
```

Avoid a dozen optional `renderX` props when ordinary nodes or children are sufficient.

### Render functions

A render function is appropriate when the consumer needs internal state or actions to render a region:

```tsx
<DataBoundary resource={resource}>
  {({ data, refresh }) => <View data={data} onRefresh={refresh} />}
</DataBoundary>
```

Document call timing and keep the payload stable. Do not use a render function merely to avoid creating a small component.

### Compound components

Compound components can provide a clear API for a coordinated widget:

```tsx
<Tabs value={tab} onValueChange={setTab}>
  <Tabs.List>
    <Tabs.Trigger value="overview">Overview</Tabs.Trigger>
    <Tabs.Trigger value="history">History</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Panel value="overview">...</Tabs.Panel>
</Tabs>
```

Use them when:

- several parts share state and accessibility relationships;
- consumers need layout flexibility;
- the semantic pattern is stable;
- context cost and error messages are acceptable.

Do not use them for a component with one fixed child arrangement. Validate missing provider use, duplicate values, ordering assumptions, nested instances, SSR IDs, and keyboard semantics.

### Cloning children

`cloneElement` and child introspection are fragile because they couple the parent to child shape and can conflict with refs, keys, wrappers, and Server Components. Prefer context, explicit props, or slots. Use cloning only when the structural contract is narrow, documented, and tested.

## 6. Controlled and uncontrolled state

A controlled component receives the current value and emits requested changes. An uncontrolled component owns current state and may accept an initial default.

Define:

- controlled detection;
- initial value semantics;
- whether mode can change after mount;
- reset behavior;
- callback timing;
- validation and normalization;
- ref or form integration;
- behavior when the parent declines an update.

A common API is:

```tsx
type DisclosureProps = {
  open?: boolean;
  defaultOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
};
```

Do not silently switch ownership when `open` changes between `undefined` and a value. Warn or document unsupported switching according to repository policy.

Keep the callback as a request or notification, not an implicit promise that state already changed. Tests should cover controlled, uncontrolled, reset, and disabled behavior if the component supports them.

## 7. Variants and state machines

Use a discriminated union or explicit state machine when transitions and impossible combinations are central to correctness. For example, a payment component may distinguish idle, submitting, challenge, success, and failure with state-specific data.

Do not turn ordinary visual styling into an elaborate state machine. CSS variants or a small enum are enough when there is no lifecycle or invariant to enforce.

Keep domain transitions separate from animation states. An animation completing should not be the only source of truth for business completion unless the product contract truly depends on it.

## 8. Context API design

Context is useful for data needed by a coherent subtree where explicit threading would obscure the component API. It is not a default global store.

A provider contract should specify:

- value and action shape;
- default or missing-provider behavior;
- ownership and lifetime;
- whether nested providers are supported;
- update frequency and consumer scope;
- server/client constraints;
- testing wrapper.

Prefer a missing-provider error for required contexts rather than a fabricated default that hides incorrect composition:

```tsx
const DialogContext = createContext<DialogContextValue | null>(null);

function useDialogContext(): DialogContextValue {
  const value = useContext(DialogContext);
  if (value === null) {
    throw new Error('Dialog components must be rendered inside Dialog.Root.');
  }
  return value;
}
```

For React 18 compatibility, use `<Context.Provider>`. React 19 shorthand is optional syntax, not a design improvement by itself.

Split context when consumers need independent update frequencies and profiling shows broad invalidation. Do not split every field preemptively; more providers can make ownership harder to follow.

## 9. Ref API design

Refs are escape hatches for imperative capabilities.

Forward a DOM ref when consumers genuinely need native focus, measurement, selection, scrolling, media, or integration. Preserve the semantic element across compatible releases or document the ref-target change.

Use an imperative handle when exposing a smaller, stable capability is safer than exposing DOM internals:

```tsx
type EditorHandle = {
  focus(): void;
  selectAll(): void;
};
```

Keep methods synchronous or document async/error behavior explicitly. Do not expose internal setters or mutable objects that bypass component invariants.

React 19 can receive `ref` as a prop. Libraries supporting React 18 should normally retain `forwardRef`; a global ref migration is not required.

Ref callbacks must support detach and, on React 19, may return cleanup. Verify Strict Mode double invocation in development.

## 10. Native element wrappers

A wrapper must preserve the native control's contract unless deviation is deliberate.

For buttons:

- set or document the default `type`;
- preserve disabled behavior;
- do not fire application actions while disabled;
- keep keyboard activation and accessible name;
- forward form-related props when promised.

For inputs:

- preserve `name`, value/defaultValue, form association, autocomplete, input mode, constraints, and labels;
- do not debounce the controlled value itself in a way that makes typing lag or cursor position unstable;
- separate displayed value from deferred expensive results;
- forward the actual input ref if consumers depend on it.

For links:

- use anchors for navigation and buttons for actions;
- preserve URL, target, rel, download, and modified-click behavior;
- integrate through the repository's router without destroying native semantics.

## 11. Error boundaries and recovery

Error Boundaries isolate render failures below them. Place boundaries around meaningful recovery regions, not every component.

Define:

- what fallback users see;
- whether retry remounts or resets state;
- what diagnostic context is reported;
- what errors are intentionally allowed to reach a parent;
- how SSR/framework error boundaries interact;
- whether sensitive data is removed from reports.

Error Boundaries do not catch every event-handler or arbitrary async error. Handle mutation and event failures in their own lifecycle.

A retry implemented by changing a key is acceptable when deliberate remount is the recovery contract. It is not a generic error-clearing mechanism.

## 12. Portals and overlays

Portals change DOM placement, not React ownership or event propagation. Overlays require more than `createPortal`:

- accessible naming and role;
- initial focus and focus restoration;
- modal focus containment when appropriate;
- background inertness/interaction policy;
- Escape and outside-interaction behavior;
- scroll locking and nested overlay coordination;
- stacking and host container ownership;
- SSR-safe container resolution;
- cleanup when the host disappears.

Use an established accessible primitive when the repository has one. Do not implement a custom dialog solely because rendering into `document.body` is easy.

## 13. Design-system primitives

A design-system component should encode stable semantics and interaction, not only style.

Preserve:

- native behavior and accessibility;
- theme and token contracts;
- ref and event semantics;
- controlled/uncontrolled behavior;
- composability without DOM leakage;
- predictable class/style merging;
- package and React-version compatibility.

Avoid forcing all application components through primitives that add no behavioral or styling consistency. A one-off domain layout can remain ordinary markup.

When adding a variant, check whether it represents a reusable design decision or one screen's incidental condition. Domain-specific variants often belong outside the primitive.

## 14. Styling and class composition

Keep style ownership explicit. A component API may support class names, CSS variables, style objects, or slots according to repository conventions, but merging order is observable.

- Do not allow consumer styles to break hidden, disabled, focus, or accessibility invariants silently.
- Avoid generating unbounded dynamic class names that the build tool cannot detect.
- Keep layout responsibilities between parent and child clear.
- Treat CSS order changes from package or toolchain updates as compatibility risks.
- Do not inline large dynamic style objects merely to avoid a stylesheet when it creates new objects or CSP problems without benefit.

## 15. Lists and keys

A key represents identity among siblings. Use a stable domain ID whenever items can be inserted, removed, filtered, or reordered.

Index keys are acceptable when all are true:

- the list order is fixed;
- items are not inserted or removed independently;
- children do not hold state whose identity matters;
- no stable domain key exists;
- the invariant is likely to remain true.

Random keys and generated-on-render keys are wrong because they force remounting. `useId` is not a list-key generator.

Duplicate keys are a correctness issue even if the UI appears to render.

## 16. Callback API semantics

Define callbacks by observable event:

- `onOpenChange(nextOpen)` requests or reports an open-state transition.
- `onSubmit(values)` should state whether it may return a Promise and how errors are surfaced.
- `onValueCommit` should differ clearly from high-frequency `onValueChange`.
- Native handlers should preserve the native event when consumers need preventDefault, target data, or composition state.

Do not invoke callbacks during render. Be explicit about ordering relative to internal state updates, validation, navigation, and focus.

Stable callback identity is only a public contract when documented or required by an integration. Inline callbacks are not inherently defective.

## 17. Common false positives

Do not report these without a concrete impact:

- A component has more than one prop.
- A boolean prop exists.
- An inline callback or object literal exists.
- A component is “too large” by line count alone.
- Context is used for a coherent low-frequency subtree.
- An index key is used for a truly static decorative list.
- A component is not wrapped in `memo`.
- State is local instead of global.
- Composition uses a node prop instead of a compound component.
- `forwardRef` remains in a library supporting React 18.

## 18. Completion gate

Before completing component API work, confirm:

- Responsibility and state ownership are clear.
- Invalid prop combinations are prevented or documented proportionately.
- Native semantics, form behavior, accessible name, keyboard, and focus are preserved.
- Controlled and uncontrolled contracts are stable.
- Keys reflect domain identity where it matters.
- Context and composition mechanisms are no more powerful than required.
- Ref targets and imperative handles are deliberate and version-compatible.
- Public types, callbacks, DOM, CSS, and package exports were checked for consumers.
- Tests cover the meaningful variants and interaction sequences rather than implementation structure.
