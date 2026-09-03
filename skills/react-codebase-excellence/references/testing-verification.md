# Testing and Verification

Read this reference when adding or reviewing tests, configuring CI, migrating React versions, validating SSR/hydration/RSC behavior, adopting React Compiler, or diagnosing flaky UI behavior. Tests should provide confidence in observable contracts, not preserve incidental implementation details.

## 1. Start from risk and contract

For the changed behavior, identify:

- user-visible success and failure outcomes;
- accessibility and interaction contracts;
- state transitions and race boundaries;
- server/client and serialization boundaries;
- React and framework version matrix;
- browser/runtime support;
- authentication, authorization, and data integrity risks;
- performance or bundle budgets;
- rollback and migration behavior.

Choose the cheapest test level that exercises the real failure boundary. Do not replace a necessary browser, integration, or server test with a shallow component test merely because it runs faster.

## 2. Use the repository's established stack

Inspect existing scripts, test setup, helpers, fixtures, browser projects, CI workflows, and conventions before introducing tools.

Common layers include:

- pure unit tests for domain logic;
- DOM component tests;
- integration tests across routing, stores, network boundaries, or server functions;
- SSR/hydration tests;
- real-browser end-to-end tests;
- visual regression and component stories;
- accessibility automation and manual checks;
- performance and bundle regression checks.

Do not add a parallel test framework without a demonstrated gap. Follow framework-specific test guidance where it owns rendering or server behavior.

## 3. Test behavior through the user surface

Prefer assertions on:

- accessible role, name, description, state, and value;
- visible text and meaningful status;
- focus movement and keyboard behavior;
- URL/history changes;
- enabled, disabled, pending, error, and success states;
- durable server or store effects;
- calls across an intentional external boundary.

Avoid coupling to:

- component instances;
- private hook state;
- exact child structure without a semantic contract;
- generated class names;
- implementation-only callbacks;
- render counts unless performance or identity is the contract.

A test should survive a behavior-preserving refactor.

## 4. Query priority

For DOM tests, prefer queries that reflect how users and accessibility APIs find the element:

1. Role plus accessible name.
2. Label text for form controls.
3. Placeholder only when it is an intentional user-facing identifier.
4. Visible text, display value, alt text, or title as appropriate.
5. Test ID as a deliberate fallback when no semantic query exists.

Use role/state filters such as `selected`, `checked`, `expanded`, `pressed`, `current`, or level when they express the contract.

A failing role/name query often reveals an accessibility problem. Do not replace it immediately with a test ID merely to make the test pass.

## 5. Interact like a user

Use the established user-event abstraction rather than dispatching low-level events when testing ordinary interactions. A click may require pointer, focus, keyboard, and default-action behavior that a single synthetic event bypasses.

Test relevant alternatives:

- keyboard and pointer activation;
- tab order and focus return;
- typing, selection, paste, and form submission;
- disabled or read-only behavior;
- Escape and outside interaction for dismissible UI;
- browser back/forward where routing state matters.

Use lower-level event dispatch only when the low-level event itself is the integration contract.

## 6. `act` and update flushing

Modern rendering libraries normally wrap public interactions in `act`. Use React's `act` directly when custom renderers, roots, timers, external-store emissions, or imperative callbacks fall outside those helpers.

Do not silence `act` warnings globally. They often indicate that the test finished before an update or that an external event was not flushed.

Prefer awaiting the operation or resulting UI state over manually wrapping arbitrary delays.

In React 19, import `act` from `react`; legacy `react-dom/test-utils` helpers are removed or deprecated. Keep React 18 compatibility only where the repository still supports it.

## 7. Async tests without sleeps

Do not use wall-clock sleeps as synchronization. They make tests slow and timing-dependent.

Prefer:

- awaiting user interactions;
- awaiting a semantic UI condition;
- controlled deferred promises;
- deterministic fake clocks for timer contracts;
- mock servers with explicit request observation;
- framework navigation/test utilities;
- explicit stream or transport controls for SSR/RSC tests.

A timeout is a failure bound, not the synchronization mechanism.

## 8. Deferred-promise pattern

For loading, race, transition, optimistic, or cancellation behavior, control resolution order explicitly:

```ts
type Deferred<T> = {
  promise: Promise<T>;
  resolve(value: T): void;
  reject(reason?: unknown): void;
};

function createDeferred<T>(): Deferred<T> {
  let resolve!: (value: T) => void;
  let reject!: (reason?: unknown) => void;
  const promise = new Promise<T>((resolvePromise, rejectPromise) => {
    resolve = resolvePromise;
    reject = rejectPromise;
  });
  return { promise, resolve, reject };
}
```

Use the repository's lint/type policy; the example demonstrates deterministic ownership, not a mandatory helper shape.

Exercise out-of-order completion, rejection, duplicate submission, unmount/navigation, retry, and stale-result protection where relevant.

## 9. State and reducer tests

Test pure reducers and domain transitions directly when they contain meaningful logic. Also test at least one consuming UI path when wiring, effects, or accessibility matters.

Cover:

- initial state and lazy initialization;
- valid transitions;
- invalid or ignored events;
- reset behavior on identity changes;
- immutable updates;
- derived selectors where incorrect derivation would be material.

Do not duplicate every reducer assertion through slow DOM tests. Do not test only the reducer when integration can break the user behavior.

## 10. Hook tests

Prefer exercising a custom hook through a small representative consumer when its value is primarily UI behavior. A hook-only harness is appropriate for reusable non-visual contracts, external-store integration, lifecycle behavior, or complex state machines.

Test:

- parameter changes;
- cleanup and re-subscription;
- Strict Mode behavior;
- stale closures and event timing;
- error and cancellation paths;
- server/client restrictions;
- referential stability only when promised by the API.

Do not assert callback or object identity unless consumers rely on it.

## 11. Effect and lifecycle tests

For Effects that synchronize external systems, verify:

- setup uses current inputs;
- cleanup undoes the corresponding setup;
- dependency changes clean up before re-subscribing;
- repeated setup/cleanup is safe;
- unmount releases resources;
- late async completion cannot corrupt current state;
- global listeners are not multiplied;
- timers, observers, widgets, workers, and object URLs are released.

Run representative component tests under Strict Mode when the application does. Development replay is a diagnostic for cleanup correctness, not behavior to suppress.

## 12. External stores

For `useSyncExternalStore` integrations, test:

- consistent snapshot identity when data has not changed;
- subscription and unsubscription;
- update propagation;
- selector/equality behavior provided by the store library;
- server snapshot and hydration consistency;
- multiple consumers and teardown;
- updates during render/transition boundaries where the store permits them.

Avoid mutating shared store fixtures across parallel tests without isolation.

## 13. Suspense

Test each meaningful Suspense boundary independently:

- fallback or retained-content behavior;
- successful reveal;
- rejection and Error Boundary behavior;
- nested boundary ordering;
- transitions that should preserve already revealed content;
- retry behavior;
- accessibility of pending status;
- SSR streaming behavior when owned by the framework.

Do not rely on exact internal scheduling or commit counts. Assert the product-visible sequencing contract.

## 14. Actions, forms, and optimistic UI

For React 19 Actions, `useActionState`, `useFormStatus`, or `useOptimistic`, test:

- native form semantics and submission paths;
- client validation and authoritative server validation;
- pending state tied to the real submission;
- duplicate clicks and concurrent submissions;
- optimistic success and rollback/reconciliation;
- rejected/returned validation errors;
- authorization and stale-session behavior;
- keyboard submission and focus/error announcement;
- no-JavaScript/progressive behavior where promised by the framework.

A unit mock that directly calls the action does not prove that form ownership and pending state are wired correctly.

## 15. Transitions and deferred values

Test transitions by observable urgency:

- urgent input remains responsive;
- non-urgent content eventually reflects the latest input;
- obsolete work cannot overwrite newer intent;
- pending indication follows product semantics;
- already useful content is retained when intended;
- errors reach the correct boundary.

Do not assert a fixed number of renders or exact scheduler interleaving. Those are not stable public contracts.

## 16. Portals, dialogs, and focus

Render portal targets according to application structure and test:

- semantic role/name;
- initial focus;
- focus containment when required;
- Escape and close controls;
- background interaction/inert behavior;
- focus restoration to a valid trigger or fallback;
- nested overlays and teardown;
- server rendering/hydration only if the product supports it.

DOM presence alone does not establish an accessible modal.

## 17. Component and interaction test completion gate

Before completing focused component, Hook, Effect, Suspense, Action, form, or interaction tests, confirm:

- Assertions target observable behavior and semantic accessibility contracts.
- Interactions use the repository's user-facing event abstraction.
- Async ordering is controlled without wall-clock sleeps.
- Cleanup, Strict Mode, stale completion, and unmount behavior are covered where relevant.
- Identity is asserted only when it is part of the API.
- The chosen test layer exercises the actual failure boundary.
- Executed checks and remaining integration gaps are reported honestly.
