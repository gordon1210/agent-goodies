# React 18 and React 19 Compatibility

Read this reference for version-sensitive implementation, upgrades, library support, removed APIs, React 19.1 and 19.2 additions, or mixed-version workspaces. React APIs must be selected from the repository's installed versions, not from the current documentation site's default version.

## 1. Establish the exact version surface

Inspect, rather than infer:

- `react`, `react-dom`, renderer-specific packages, and matching type packages.
- Framework, router, bundler, compiler, test renderer, and RSC integration versions.
- Lockfile resolution, workspace overrides, package-manager catalogs, and peer dependency warnings.
- Whether more than one React copy can enter the bundle.
- Whether the package is an application, a framework integration, or a library with React peer ranges.
- Whether stable, Canary, or experimental builds are intentionally pinned.

`react` and its renderer must remain compatible. A library's declared peer range is not proof that every path was tested on every supported minor.

Useful checks depend on the package manager, but should answer:

```text
Which exact React packages are installed?
Why was each version selected?
Are react and react-dom aligned?
Does any workspace resolve another copy?
Which supported versions are exercised in CI?
```

Do not use a React 19 feature merely because `@types/react` is newer, or vice versa. Runtime and type versions must agree with repository policy.

## 2. Capability map

Use this as a routing summary, then verify exact minor behavior when material.

| Capability | React 18 | React 19.0 | React 19.1 | React 19.2 |
|---|---:|---:|---:|---:|
| `createRoot`, `hydrateRoot` | Yes | Yes | Yes | Yes |
| Automatic batching with modern roots | Yes | Yes | Yes | Yes |
| `startTransition`, `useTransition`, `useDeferredValue` | Yes | Yes | Yes | Yes |
| `useId`, `useSyncExternalStore`, `useInsertionEffect` | Yes | Yes | Yes | Yes |
| Form Actions and function `action`/`formAction` props | No | Yes | Yes | Yes |
| `useActionState`, `useOptimistic`, `use` | No | Yes | Yes | Yes |
| `useFormStatus` | No | Yes | Yes | Yes |
| Function-component `ref` as a normal prop | No | Yes | Yes | Yes |
| `<Context value={...}>` provider shorthand | No | Yes | Yes | Yes |
| Ref callback cleanup functions | No | Yes | Yes | Yes |
| Document metadata and React DOM resource APIs | Limited/framework-specific | Yes | Yes | Yes |
| `captureOwnerStack` | No | No | Yes, development only | Yes, development only |
| `<Activity>` | No | No | No | Yes |
| `useEffectEvent` | No | No | No | Yes |
| `cacheSignal` | No | No | No | Yes, RSC only |
| Partial pre-render resume APIs | No | No | No | Yes, integration-level |

This table does not authorize using an API. Frameworks may expose, restrict, wrap, or own the corresponding lifecycle.

## 3. React 18 baseline

React 18 remains a valid production target and needs more than compatibility shims.

### Modern roots

- Client-rendered applications should use `createRoot`.
- Hydrated applications should use `hydrateRoot`.
- Automatic batching and concurrent capabilities are tied to the modern root model; legacy rendering preserves legacy behavior and is removed in React 19.
- Root ownership matters. Keep the returned root for unmounting rather than calling legacy DOM APIs.

### Concurrency-facing APIs

React 18 provides:

- `startTransition` and `useTransition` for non-urgent state updates.
- `useDeferredValue` for rendering a lagging view of an urgent value.
- Suspense improvements and streaming SSR support.
- `useId` for stable server/client accessibility identifiers.
- `useSyncExternalStore` for external mutable source subscriptions.
- `useInsertionEffect`, primarily for CSS-in-JS library integration before layout effects.

Do not describe these APIs as background threads. Rendering may be interruptible or deferred, but JavaScript work still runs under the host runtime's scheduling constraints.

### Development Strict Mode

React 18 development Strict Mode deliberately stresses mount and cleanup behavior. Code must tolerate render replay and effect setup-cleanup-setup without externally observable corruption. Do not use a `didRun` ref to conceal missing cleanup unless the operation is explicitly process-global and owned outside component lifecycle.

### React 18 alternatives to React 19 APIs

When the repository stays on React 18:

- Use the existing form or mutation layer rather than inventing a `useActionState` clone.
- Model optimistic state with established state/data infrastructure and explicit rollback.
- Read context with `useContext` and render providers with `<Context.Provider>`.
- Expose function component refs with `forwardRef` where required.
- Keep non-reactive effect logic in a stable repository-approved pattern; do not emulate `useEffectEvent` by suppressing dependencies.
- Use framework-supported Suspense data integration, loaders, or a data library rather than throwing arbitrary client-created promises from render.

A compatibility implementation should preserve semantics, not merely copy React 19 API names.

## 4. React 18.3 as an upgrade bridge

React 18.3 has React 18.2 behavior plus warnings for APIs and patterns that need attention before React 19. For an intentional 18-to-19 migration, upgrading to 18.3 first is usually the cleanest diagnostic step.

Treat 18.3 warnings as migration evidence, not permission for a broad rewrite. Resolve them in focused groups, keep application behavior stable, and run the existing test and browser matrix before changing the major version.

## 5. React 19.0 baseline

React 19 adds application-facing capabilities and removes long-deprecated APIs. It does not make every codebase an RSC application or make every new API appropriate by default.

### Required JSX transform

React 19 requires the modern JSX transform. Confirm the repository's TypeScript, Babel, SWC, Oxc, framework, or other transform configuration before upgrading. A dependency still publishing output for an obsolete transform may also block the migration.

### Actions and forms

React 19 supports asynchronous Actions and form integration, including:

- Functions passed to form `action` and button/input `formAction`.
- `useActionState` for an action's returned state and pending status.
- `useOptimistic` for temporary optimistic state while an Action is pending.
- `useFormStatus` for status from a parent form submission.
- Transition-aware async mutations and automatic form reset behavior for successful uncontrolled forms.

Preserve domain behavior around validation, authorization, idempotency, duplicate submission, errors, retries, focus, announcements, optimistic rollback, and cache invalidation. React handles UI coordination; it does not supply those application guarantees.

### `use`

`use` can read supported resources such as a Promise or context. Unlike ordinary Hooks, it may be called in conditions and loops, but it still must run while React is rendering a component or Hook and has additional restrictions.

- Do not create a fresh client Promise during every render and pass it to `use`.
- Prefer framework- or library-owned cached promises for client use.
- Keep error handling compatible with Suspense and Error Boundaries; do not wrap `use` in unsupported control flow merely to catch suspension.
- Treat Promise identity, cache scope, request ownership, and rejection behavior as contracts.

### Refs

Function components in React 19 may receive `ref` as a prop when their props declare it. `forwardRef` continues to work and remains important for React 18-compatible libraries.

Ref callbacks may return cleanup functions. This changes two practical contracts:

- Cleanup must release observers, listeners, or imperative resources created for that node.
- An implicit expression return from a ref callback may accidentally look like a cleanup return to TypeScript. Use a block when assigning the node.

Do not read `element.ref`; ref is represented as a prop in React 19 and direct element introspection is already an escape hatch.

### Context provider shorthand

React 19 accepts:

```tsx
<ThemeContext value={theme}>{children}</ThemeContext>
```

React 18 requires:

```tsx
<ThemeContext.Provider value={theme}>{children}</ThemeContext.Provider>
```

The shorthand does not change context update semantics or justify converting all providers. Shared libraries supporting both majors should normally retain the compatible form.

### Error reporting

React 19 changed render error reporting and added root callbacks such as `onUncaughtError`, `onCaughtError`, and `onRecoverableError`. Review integrations that depended on errors being rethrown or on duplicate development logging. Preserve Error Boundary behavior and ensure telemetry does not leak sensitive props or payloads.

### Suspense behavior

React 19 can commit the nearest fallback sooner and then pre-warm suspended siblings. Do not assert React 18's exact sibling-render timing. Test user-visible fallback, reveal, error, and retry behavior instead.

### Document and resource integration

React 19 can coordinate metadata, stylesheets, scripts, and resource hints. Frameworks often own the same concerns. Do not create duplicate head management, preload, or script systems alongside the framework's established integration.

### RSC and Server Functions

React 19 exposes stable user-facing RSC features, but implementation APIs used by frameworks and bundlers may not follow ordinary minor-version SemVer. Applications should consume RSC through a supported framework or integration and follow its pinning policy.

`"use server"` marks Server Functions; it does not mark Server Components. Server Functions are network-reachable mutation boundaries and require server-side authentication, authorization, validation, rate/resource limits, and current security patches.

## 6. React 19.1 additions and behavior changes

React 19.1 is not merely a patch-equivalent step between 19.0 and 19.2. Gate the following behavior on an installed 19.1-or-newer runtime and renderer.

### Owner Stacks and `captureOwnerStack`

Owner Stacks identify the chain of components responsible for rendering a component. They complement Component Stacks, which describe the component hierarchy leading to an error.

- `captureOwnerStack` is a React 19.1 development-only diagnostic API.
- Never make product behavior, production error handling, alerting, or required telemetry depend on it.
- Keep production observability on supported root callbacks, Error Boundaries, application context, and the framework's error integration.
- Call it only where an owner stack is meaningful, and tolerate an unavailable or `null` result.
- Do not log sensitive application data merely to make the owner stack actionable.

### Suspense and hydration scheduling

React 19.1 changed and fixed several Suspense and hydration scheduling paths, including client rendering of unfinished boundaries and reduced unnecessary client work. Test observable fallback, reveal, retry, focus, and hydration behavior rather than scheduler internals or an exact render sequence.

### `useId` values are opaque

React 19.1 changed the generated `useId` format to values that can participate in valid CSS selectors. Never parse, sort, persist, snapshot as a business value, or derive semantics from a React-generated identifier. Use it only to connect elements within the rendered UI.

### DOM and test-environment details

- React 19.1 added `beforetoggle` and `toggle` event support for `<dialog>`.
- HTML comment nodes are no longer supported as React DOM containers.
- Development-only APIs such as `act` are not production-runtime contracts; run React tests with the repository's intended development or test build.
- The RSC `unstable_prerender` API introduced on this line remains experimental and integration-level. Do not present it as the stable React DOM 19.2 partial pre-render/resume surface.

## 7. React 19.2 additions

Gate these on an installed version that provides them.

### `<Activity>`

`<Activity>` can hide a subtree while preserving its state. In hidden mode, React hides the DOM, tears down Effects, and deprioritizes updates; on visibility, Effects mount again.

Use it when preserving state or pre-rendering hidden UI is a real product requirement. Do not replace every conditional with Activity:

- Hidden subtrees still have memory and rendering implications.
- Effect teardown means hidden connections, media, listeners, and subscriptions stop.
- Accessibility and focus behavior must be verified when a focused subtree becomes hidden.
- Security-sensitive or tenant-sensitive state should not be retained without an explicit lifecycle decision.

### `useEffectEvent`

`useEffectEvent` extracts non-reactive logic that an Effect needs to call while observing current values. It is not a general callback hook and not a way to evade dependencies.

- Call Effect Events only from Effects or related effect lifecycle code.
- Keep genuinely reactive inputs in the Effect dependency model.
- Use it to separate “latest value used when the external event occurs” from “value whose change must resubscribe.”
- On React 18 or 19.0/19.1, restructure the effect or use the repository's established stable-callback pattern with equivalent tests.

### `cacheSignal`

`cacheSignal` is for React Server Components and ties cancellable work to a React cache lifetime. Do not use it in ordinary client components or as a generic request cancellation API.

### Partial pre-rendering and resume APIs

React DOM 19.2 includes integration APIs for pre-rendering resumable output. These are architecture-level choices normally owned by a framework or rendering platform. Validate protocol compatibility, deployment behavior, cache policy, CSP/nonces, error reporting, abort behavior, and mixed-version rollout before adopting them.

## 8. Removed or changed React 19 APIs

Search the codebase and dependencies for at least the following when upgrading:

- `ReactDOM.render`, `ReactDOM.hydrate`, and `unmountComponentAtNode`.
- `ReactDOM.findDOMNode`.
- `react-dom/test-utils` APIs; `act` moves to `react`, and the rest are removed.
- Function-component `propTypes` runtime checking and function-component `defaultProps`.
- Legacy context through `contextTypes` and `getChildContext`.
- String refs.
- Module-pattern component factories and `React.createFactory`.
- `react-test-renderer/shallow`; reconsider shallow rendering rather than moving it mechanically.
- UMD React builds.
- Libraries that access React internals.

`react-test-renderer` itself is deprecated and no longer a sound basis for new test architecture.

## 9. React 19 TypeScript changes

When using React 19 types, review:

- `useRef` requires an initial argument and returns mutable ref objects under the updated model.
- Ref callbacks must not accidentally return assigned nodes; return cleanup deliberately or return nothing.
- Unparameterized `ReactElement` props default to `unknown` instead of `any`.
- Types for removed APIs disappear or move.
- A component accepting `ref` as a prop must declare the correct ref type.
- Function defaults should use parameter defaults rather than function `defaultProps`.

Run type codemods only on a clean branch, review every change, and keep mechanical migration separate from semantic refactors.

## 10. React Compiler compatibility

React Compiler 1.x is stable and can target React 17 and later, but adoption is still a build-system and rollout decision.

For React 18:

- Confirm the configured compiler target and required runtime package.
- Validate both development and production builds.
- Do not assume React 19 APIs become available because the compiler is enabled.

For React 19:

- Compiler support does not change API minor gating.
- Existing manual memoization may be left in place; removing it can change generated output or identity behavior.
- Compiler diagnostics often reveal Rules-of-React violations. Fix the violation rather than disabling compilation for an entire repository.

Libraries must decide whether to publish compiled output, uncompiled source, or both according to their consumer and build contracts. Test the actual package artifact, not only the source workspace.

## 11. Application upgrade playbook: React 18 to 19

1. Record current behavior, browser support, bundle/build baseline, SSR/hydration behavior, and critical test coverage.
2. Align `react`, `react-dom`, type packages, framework, router, and test ecosystem within supported ranges.
3. Move to React 18.3 and resolve warnings without changing product behavior.
4. Confirm the modern JSX transform.
5. Replace removed root, hydration, unmount, DOM lookup, legacy context, ref, and test APIs.
6. Update TypeScript-sensitive ref and element code.
7. Upgrade React and the renderer together; review the lockfile for duplicate React copies and peer conflicts.
8. Run focused tests, production build, browser tests, SSR/hydration tests, and error-reporting checks.
9. Test Suspense timing, Strict Mode, ref callbacks, controlled forms, portals, and third-party components.
10. Only after the migration is stable, evaluate React 19 features as separate product or architecture changes.

Do not combine a major-version migration with state-library replacement, folder reorganization, design-system rewrite, or RSC adoption unless the migration is impossible otherwise.

## 12. Published library strategy

A library supporting both React 18 and 19 should normally:

- Declare an honest peer range and test each supported major.
- Avoid runtime imports or JSX output that force a second React copy.
- Use APIs common to the supported range in the public implementation.
- Retain `forwardRef` where consumers on React 18 need ref forwarding.
- Retain `<Context.Provider>` when source or distributed JSX must execute on React 18.
- Avoid exposing React 19-only types through a React 18-compatible declaration surface.
- Validate ESM/CJS exports, JSX runtime, tree shaking, SSR import safety, and package artifact contents.
- Document whether compiler-processed output is shipped and the minimum runtime it requires.

Separate entry points can support different majors, but only when the package exports, bundler resolution, tests, and documentation make selection deterministic. A conditional maze is usually worse than retaining the common API.

## 13. Canary and experimental features

Treat View Transitions, Fragment refs, experimental directives, or other Canary-only APIs as unavailable unless all of the following are true:

- The repository intentionally pins a compatible channel.
- Framework and renderer versions are aligned.
- The task explicitly accepts unstable behavior and migration cost.
- Tests cover fallback and rollback.
- Public consumers are not accidentally forced onto the channel.

Do not present a conference demo, Labs post, or Canary documentation as stable React 19 behavior.

## 14. Compatibility completion gate

Before completing version-sensitive work, confirm:

- Exact runtime, renderer, type, framework, and compiler versions are known.
- Every introduced API exists in the minimum supported version.
- React and renderer versions remain aligned without duplicate runtime copies.
- Removed APIs and dependency internals have been searched.
- SSR, hydration, Suspense, Strict Mode, refs, forms, and error reporting were tested where affected.
- Library peer and declaration compatibility were validated against installed artifacts.
- Current RSC security advisories were checked when the stack supports RSC.
- No unrelated adoption of React 19 features was smuggled into the upgrade.
