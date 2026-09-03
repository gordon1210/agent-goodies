# Architecture, Tooling, and TypeScript

Read this reference when changing repository structure, package boundaries, framework integration, public exports, TypeScript models, lint/build configuration, or component-library packaging. The objective is coherent ownership and predictable contracts, not a universal React folder layout.

## 1. Classify the codebase before changing it

Identify which environment owns each concern:

| Context | Primary concerns |
|---|---|
| Client-only application | root ownership, routing, client data lifecycle, bundle and browser behavior |
| SSR application | deterministic initial render, request isolation, streaming, hydration and server/client module safety |
| RSC application | framework boundaries, serializable values, cache scope, Server Functions and patched transport packages |
| Embedded widget | multiple roots, host-page CSS/DOM conflicts, teardown, CSP and version isolation |
| Published component library | peer dependencies, public types, package exports, styling contract and multi-version testing |
| Design system | accessibility invariants, composability, theming, token stability and migration policy |
| Monorepo | dependency direction, package ownership, shared config, build graph and duplicate React prevention |

Do not import conventions from Next.js, Remix, React Router, Vite, Astro, Storybook, or another host unless that host is actually present and owns the behavior.

## 2. Repository contract inventory

Inspect:

- Workspace packages and application entry points.
- Package manager and lockfile.
- `exports`, `imports`, `types`, `main`, `module`, `sideEffects`, and publish files.
- JSX transform and development transform.
- TypeScript project references, composite builds, generated declaration output, and strictness flags.
- Build plugins and transforms, including React Compiler.
- Framework route, loader, action, server/client, middleware, and cache conventions.
- CSS strategy, token source, theming, resets, portals, and shadow DOM use.
- Test environments: DOM emulation, real browser, SSR, Storybook, visual regression, and E2E.
- Browser target, polyfills, runtime target, edge constraints, and deployment adapters.

Repository-local commands and architecture outrank generic examples. Preserve the package manager and established task graph.

## 3. Component and feature boundaries

Organize by cohesion and ownership:

- A feature boundary is useful when behavior, state, tests, and data contracts change together.
- A shared component belongs in a shared package only after multiple consumers need the same stable contract.
- A route-specific component need not become “generic” merely because it has JSX.
- A custom Hook belongs near its only consumer until reuse or independent testing justifies movement.
- A design-system primitive should not import application state, routing, data clients, or domain services.
- Domain code should not depend on DOM or React unless the UI is part of the domain contract.

Avoid folder taxonomies that separate every file by noun while scattering a feature's behavior. Also avoid giant catch-all feature directories with unrestricted cross-imports. Favor a small number of explicit dependency directions.

A practical direction often looks like:

```text
application composition
  -> features/routes
      -> domain/application services
      -> shared UI primitives
          -> tokens and platform helpers
```

This is a diagnostic, not a mandate. Preserve a simpler existing layout when dependencies are already clear.

## 4. Framework boundaries

Frameworks own more than routing. Determine whether they own:

- Initial data loading and request cancellation.
- Mutation actions and revalidation.
- Server/client module partitioning.
- Head metadata and resource hints.
- SSR streaming, RSC transport, hydration, and error boundaries.
- Asset URLs, environment variables, code splitting, and prefetching.
- Authentication session propagation and request context.

Do not build a second lifecycle beside the framework. For example, an effect that refetches data already supplied by a route loader can create races, duplicate requests, loading flashes, and incompatible cache ownership.

Framework APIs are not interchangeable merely because they wrap React. When reviewing current behavior, verify the installed framework version from its primary documentation.

## 5. Client and server module discipline

Classify modules by where they may execute:

- Browser-only modules may use DOM, storage, media, and browser APIs.
- Server-only modules may access secrets, databases, files, private networks, and request credentials.
- Shared modules must be safe in both environments and must not execute environment-specific work at import time.
- RSC client modules must respect the framework's client boundary and serializable prop contract.

Guarding a browser API inside a function is different from importing a browser-only dependency at module scope. SSR can fail before the guarded function runs.

Do not expose a server capability by importing it through a shared barrel. Keep server-only entry points explicit, and use framework-supported poison/server-only markers when available.

Avoid mutable request data in module scope. A long-lived server process can serve concurrent users, and an edge or serverless runtime can reuse an instance unexpectedly.

## 6. Public component and package APIs

Treat these as compatibility surfaces:

- Exported component and Hook names.
- Prop names, requiredness, defaults, discriminated variants, and callback timing.
- Ref target and imperative handle shape.
- Controlled/uncontrolled behavior.
- Context provider and consumer contracts.
- DOM semantics, accessible names, CSS selectors, data attributes, and slot structure that consumers intentionally rely on.
- Error behavior and thrown/suspended promises.
- CSS variables, design tokens, class hooks, and theme names.
- Package entry points, subpath exports, tree-shaking behavior, and type declarations.

Not every DOM node is public, but changing rendered structure can break CSS, tests, analytics, browser autofill, form submission, accessibility, or third-party integration. Search consumers before declaring markup private.

For a published library, avoid exporting internal types merely because TypeScript inferred them into declarations. Define deliberate public types and inspect the emitted package.

## 7. TypeScript principles for React

### Model valid component states

Use a discriminated union when combinations have different required data or behavior:

```tsx
type NoticeProps =
  | { kind: 'loading'; message?: string }
  | { kind: 'error'; message: string; onRetry?: () => void }
  | { kind: 'success'; message: string };
```

Do not replace every pair of booleans with a union. Independent binary properties such as `disabled`, `required`, or `readOnly` can remain independent.

### Keep `children` explicit

Declare `children` only when the component accepts it, and choose the narrowest useful contract:

- `ReactNode` for arbitrary renderable children.
- A render function when the child needs values and that pattern is intentional.
- A specific element type only when cloning or structural assumptions are unavoidable and documented.

Do not rely on a component type alias to add `children` implicitly if that obscures the API.

### Reuse platform prop types deliberately

For a wrapper around a native element, derive the compatible native props rather than recreating them:

```tsx
type ButtonProps = {
  tone?: 'neutral' | 'danger';
} & React.ComponentPropsWithoutRef<'button'>;
```

Resolve naming conflicts explicitly and preserve native event, `disabled`, `type`, `name`, form, and accessibility props. A wrapper that renders a `<button>` should not accidentally default to form submission when the design-system contract says otherwise.

### Event and ref types

Use the event type corresponding to the actual element and callback contract. Do not widen every handler to `Event`, `any`, or an unrelated element type.

For refs:

- Type the real imperative target.
- Use `ComponentPropsWithRef` or related helpers when forwarding intrinsic props.
- Expose `useImperativeHandle` only when a deliberate stable imperative API is better than a DOM node.
- For React 18-compatible libraries, preserve `forwardRef` in the implementation.

### External data remains untrusted

TypeScript types do not validate JSON, URL params, storage, form data, postMessage payloads, RSC/Server Function inputs, or API responses. Parse and validate at boundaries. Use `unknown` until evidence narrows the value.

Avoid assertions that merely silence a mismatch. Prefer runtime validation, control-flow narrowing, exhaustive checks, or a corrected upstream type. Keep unavoidable assertions close to the verified boundary and explain the invariant.

### Generic and polymorphic components

Generic components are appropriate when the type relationship matters to callers, such as selected item types. Avoid generics that only hide a concrete internal type.

Polymorphic `as` APIs have substantial cost:

- complex inference and refs;
- invalid prop combinations;
- semantic and accessibility drift;
- harder documentation and testing;
- larger declaration surfaces.

Prefer explicit variants or a small slot API unless consumers genuinely need arbitrary element substitution and the repository can own the type and semantic complexity.

### Default values

For function components, use parameter defaults. Preserve the distinction between omitted and explicitly supplied `undefined` according to the repository's TypeScript options and API expectations.

Do not add defaults that silently turn required domain data into fabricated UI values.

## 8. Hooks as architecture boundaries

A custom Hook should encapsulate a coherent React-facing lifecycle or reusable stateful capability. It should not merely move five lines to another file.

A useful Hook normally has at least one of:

- reusable state transition logic;
- an external subscription lifecycle;
- framework/data integration hidden behind a stable domain API;
- a testable coordination boundary;
- normalization of platform behavior across consumers.

Name Hooks for the capability they provide, not the primitive they happen to call. Keep rendering in components unless returning JSX is an intentional component abstraction.

Do not create “service Hooks” that can only be called from event handlers but secretly read render-time context unless that lifecycle is clear and tested.

## 9. State, data, and dependency ownership

Before adding infrastructure, map owners:

| Concern | Typical owner |
|---|---|
| Ephemeral visual state | local component |
| Coordinated local workflow | lifted state or reducer/provider |
| URL-visible navigation/filter state | router or URL layer |
| Remote resource cache | framework loader or data library |
| Form field lifecycle | native form or established form layer |
| Cross-tree application state | established store/provider when justified |
| Browser/external mutable source | adapter using `useSyncExternalStore` or existing library |

Duplicating a source into another owner creates invalidation and synchronization work. A new store is not simplification if route data, cache data, and local copies can diverge.

## 10. Barrels and import boundaries

Barrel files are not inherently defective. Evaluate:

- public package API intent;
- build-tool tree shaking and side effects;
- type-only exports;
- circular dependency risk;
- editor and test transform cost;
- accidental client import of server code;
- whether one import pulls a broad dependency graph.

Use explicit subpath imports when they improve boundary safety or measured bundle/build behavior. Do not rewrite imports across a repository based on a generic performance rule without evidence.

## 11. Package exports and library builds

For published packages, verify the actual tarball or packed artifact:

- Runtime entry points resolve under supported ESM/CJS conditions.
- Type declarations map to the same entry points.
- React is a peer dependency where appropriate, not bundled as a second runtime.
- JSX runtime imports match the minimum supported React version.
- Server-only and client-only entry points are separated.
- CSS and other assets are included and have documented import semantics.
- `sideEffects` metadata is truthful; marking effectful CSS or initialization as removable can break consumers.
- Source maps and declarations do not leak private paths or secrets.
- Build output does not depend on monorepo-only aliases.

Test a clean consumer installation, not only workspace symlinks.

## 12. React Compiler and lint architecture

Identify whether the repository uses:

- Compiler disabled.
- Lint diagnostics only.
- Opt-in directories or annotations.
- Opt-out gating.
- Full compilation.
- Precompiled library output.

Keep compiler configuration centralized and aligned with the build tool. Do not add Babel solely for one component if the framework has another supported integration.

React Hooks linting is a correctness control. Compiler-related lints combine correctness and optimizability signals; understand the rule before treating it as blocking. A component skipped by the compiler still needs correct React behavior.

Do not suppress a Rules-of-React violation to force compilation. Conversely, do not redesign a clear component merely to satisfy an optional optimization when compilation can safely skip it.

## 13. Toolchain changes

A toolchain change can alter more than syntax:

- JSX development output and stack traces.
- CSS ordering and extraction.
- module resolution and condition selection;
- environment variable exposure;
- chunking and preload behavior;
- SSR externalization;
- RSC transforms;
- test environment semantics;
- browser transpilation;
- source maps and error reporting.

Keep package-manager, bundler, framework, TypeScript, and lint upgrades separate when practical. Review generated lockfiles and output artifacts.

## 14. CI baseline

Use the repository's commands. A production-oriented React package commonly needs applicable checks for:

- deterministic install from the committed lockfile;
- formatting and lint;
- type checking;
- unit/component tests;
- production application or library build;
- browser/E2E tests for critical paths;
- package artifact validation for libraries;
- SSR/hydration/RSC smoke tests;
- accessibility checks;
- supported React/browser/runtime matrices;
- dependency/advisory policy.

Do not add every check to every pull request if cost is disproportionate. Split fast required checks from scheduled or release matrices while ensuring risky paths are actually exercised before release.

## 15. Common architecture failure modes

- A “shared” package imports route state or application services.
- A client barrel re-exports server-only code.
- Module-scoped request state leaks between users.
- The same remote data is independently cached in a loader, query library, global store, and component state.
- A presentational primitive performs navigation, data fetching, and authorization.
- A public component clones and introspects arbitrary children with undocumented structural assumptions.
- A package bundles React or resolves a duplicate copy.
- Type declarations expose a React 19-only type while claiming React 18 support.
- Environment variables intended as secrets are injected into the client bundle.
- A large folder migration obscures the behavioral change under review.

## 16. Completion gate

Before completing architecture or tooling work, confirm:

- Boundaries and dependency direction are explicit and no more complex than required.
- Framework-owned lifecycle is not duplicated.
- Client/server imports and request isolation are sound.
- Public props, refs, exports, DOM, CSS, and types were treated as contracts.
- TypeScript models valid states without replacing runtime validation.
- React is not duplicated or bundled incorrectly.
- Production build and package artifacts were inspected where relevant.
- Toolchain changes are intentional, version-compatible, and separately reviewable where practical.
