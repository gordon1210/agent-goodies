---
name: react-codebase-excellence
description: Use this skill when designing, implementing, reviewing, refactoring, debugging, testing, securing, optimizing, upgrading, or preparing CI and releases for a small-to-medium React web application, component library, design system, embedded widget, SSR application, or React Server Components boundary. Apply production-grade React engineering for React 19, with an explicit React 18 compatibility path, without framework cargo cults, speculative abstractions, blanket memoization, unnecessary state libraries, or unrelated rewrites. Preserve the repository's exact React and renderer versions, framework contracts, public component APIs, accessibility behavior, server/client boundaries, browser support, and established architecture unless the task explicitly changes them.
license: MIT
metadata:
  version: "1.0.0"
  last-reviewed: "2026-09-03"
  compatibility: React 19 and React 18 with React DOM for web applications and libraries. Honor the installed React, renderer, framework, TypeScript, compiler, lint, test, build-tool, runtime, and browser versions; gate every version-specific API accordingly.
---

# React Codebase Excellence

Produce the smallest coherent change that is correct, accessible, secure, testable, and appropriate for the repository. Optimize for durable behavior and clear ownership, not for demonstrating every React API or adopting the newest pattern everywhere.

## Rule hierarchy

Apply guidance in this order:

1. Explicit user requirements and repository-local instructions.
2. Security, correctness, data integrity, privacy, and accessibility.
3. Externally observable behavior, public component APIs, persisted or wire formats, and server/client contracts.
4. Exact installed React, renderer, framework, compiler, runtime, and supported-browser behavior.
5. Existing repository architecture, state ownership, data-loading model, design system, and conventions.
6. Simplicity, readability, testability, and operational clarity.
7. Measured user-facing performance and resource constraints.
8. Stylistic preferences not enforced by the project.

When rules conflict, follow the higher-ranked rule and state the trade-off. Never silently change a contract or assume a framework capability from React alone.

## Required workflow

### 1. Establish the repository contract

Before editing, inspect the relevant subset of:

- `package.json`, lockfile, workspaces, package-manager policy, scripts, and exact React/ecosystem versions.
- TypeScript or JavaScript, JSX, modules, aliases, generated types, ESLint, formatter, and compiler configuration.
- Build, SSR/RSC, deployment, code generation, Storybook, test, and CI configuration.
- Adjacent components, hooks, providers, routes, data boundaries, styles, tests, and stories.
- Public exports, props, relied-on DOM, accessibility, browser, localization, and design-system contracts.

Determine:

- The exact React and renderer minor/patch, including every supported workspace or peer range.
- Client rendering, SSR, streaming, static generation, hydration, RSC, Server Functions, and framework ownership.
- Application versus published library/design-system constraints and the type-safety boundary.
- Ownership of local, URL, form, server, cache, and external-store state.
- Client/server serialization, compiler status, trust boundaries, and critical accessibility behavior.

Do not run installs or package scripts in an untrusted repository until lifecycle scripts, local packages, plugins, generators, and configuration have been inspected and execution is appropriately sandboxed.

### 2. Load only relevant references

Read each selected file before deciding on the implementation. For repository-wide audits, read the review playbook and every applicable domain reference. Load the source index only when guidance must be verified or maintained.

| Trigger | Reference |
|---|---|
| React 18/19 differences, upgrades, removed APIs, React 19.1/19.2, library compatibility | [version-compatibility-react18-react19.md](references/version-compatibility-react18-react19.md) |
| Repository layout, framework boundaries, TypeScript, packages, lint, build and public exports | [architecture-tooling-typescript.md](references/architecture-tooling-typescript.md) |
| Component boundaries, props, composition, context APIs, controlled state, refs and design systems | [components-composition-api-design.md](references/components-composition-api-design.md) |
| State shape, reducers, custom hooks, context, URL state, server state and external stores | [state-data-flow-hooks.md](references/state-data-flow-hooks.md) |
| Effects, dependencies, stale closures, subscriptions, timers, observers and imperative DOM work | [effects-events-external-systems.md](references/effects-events-external-systems.md) |
| Promises, data loading, Suspense, transitions, Actions, optimistic UI and cancellation | [async-suspense-actions-transitions.md](references/async-suspense-actions-transitions.md) |
| DOM roots, portals, SSR, hydration, streaming, RSC, Server Functions and resource APIs | [rendering-dom-ssr-hydration-rsc.md](references/rendering-dom-ssr-hydration-rsc.md) |
| Profiling, waterfalls, rerenders, bundle cost, lists, React Compiler and user-facing metrics | [performance-compiler-bundles.md](references/performance-compiler-bundles.md) |
| Semantic HTML, keyboard and focus behavior, forms, errors, announcements and reduced motion | [accessibility-forms-interactions.md](references/accessibility-forms-interactions.md) |
| XSS, unsafe content, URLs, client secrets, auth boundaries, RSC advisories and supply chain | [security-content-dependencies.md](references/security-content-dependencies.md) |
| Unit, component, Hook, Effect, Suspense, Action, form and interaction testing | [testing-verification.md](references/testing-verification.md) |
| SSR/hydration/RSC, browser/E2E, compiler, compatibility, security, performance and CI verification | [testing-server-browser-ci.md](references/testing-server-browser-ci.md) |
| Patch, design, migration, performance, security and accessibility review; severity and false positives | [review-playbooks.md](references/review-playbooks.md) |
| Repository-wide and subsystem audit coverage matrices | [review-audit-matrices.md](references/review-audit-matrices.md) |
| Updating this skill or verifying disputed API, version, browser, framework or tool behavior | [sources.md](references/sources.md) |

### 3. Plan around observable contracts

Identify before coding:

- User-visible states, interactions, DOM semantics, focus, announcements, and keyboard behavior.
- Props, callbacks, refs, context, exports, and version/public compatibility.
- Loading, empty, success, error, retry, cancellation, optimistic, and rollback paths.
- Serialization, authorization, caching, invalidation, hydration, and test invariants.

Prefer a focused change, existing infrastructure, render-time derivation, event logic for interactions, native HTML, composition where it reduces invalid modes, and framework-owned data boundaries where already established. Use an approved dependency rather than improvised security-sensitive sanitization, focus management, or protocol code.

Do not mix unrelated cleanup into the patch. Prerequisite refactors must materially reduce risk and remain behavior-preserving.

### 4. Implement defensively

#### Render and component correctness

- Keep components and Hooks pure during render; do not mutate inputs, module state, or previously created values.
- Call components through JSX and Hooks only at valid call sites. Keep component types stable unless remounting is intentional.
- Use keys from stable data identity; accept index keys only when identity and order are provably static.
- Treat controlled/uncontrolled changes as behavioral and preserve initialization, reset, validation, and submission.
- Reserve refs for imperative integration or non-rendering mutable values, not hidden UI state.

#### State and data flow

- Store the minimum source of truth; derive values unless they are intentional snapshots or independently editable.
- Avoid contradictory, duplicated, or needlessly nested state. Keep it near its owner and lift it only for real coordination.
- Use reducers for meaningful named transitions or coordinated invariants, not field count.
- Distinguish UI, URL, form, server, cache, and external-store state and give each an owner and lifecycle.
- Use the established external-store integration or `useSyncExternalStore`; do not assume direct mutable-global reads are concurrency-safe.

#### Events, effects, and cleanup

- Use effects only to synchronize external systems or lifecycle; derive render data and handle interactions elsewhere.
- Represent reactive dependencies honestly instead of suppressing lint to force timing.
- Give subscriptions, listeners, observers, timers, requests, and imperative resources symmetrical cleanup.
- Handle stale completion, cancellation, unmount, dependency changes, and out-of-order responses.
- Fix lifecycle defects exposed by Strict Mode. Use `useLayoutEffect` only for required pre-paint DOM work.

#### Async UI and concurrency

- Start independent work without accidental waterfalls; use `Promise.all` only when independence and fail-fast semantics fit.
- Place Suspense boundaries around intended reveal and recovery experiences, not mechanically.
- Use transitions for non-urgent rendering, not to hide synchronous work or control urgent text input.
- Model genuine pending, error, retry, optimistic, confirmed, and rollback states; never simulate loading.
- Treat Server Functions and framework actions as externally callable endpoints with server-side authentication and authorization.

#### Accessibility and forms

- Prefer semantic elements and native controls before ARIA or custom interaction emulation.
- Preserve accessible names, descriptions, roles, states, structure, visible focus, and tab order.
- Implement the pattern's keyboard, focus entry/containment/restoration, and Escape behavior.
- Associate textual validation errors and pending status without disruptive announcements or unexpected focus loss.
- Use `useId` only for UI relationships when no explicit ID exists, never as a list key.

#### Security and trust boundaries

- JSX text interpolation escapes text context; it is not a sanitizer for HTML, URLs, CSS, SVG, scripts, or server boundaries.
- Use `dangerouslySetInnerHTML` only through an explicit trust policy and approved sanitizer or trusted-content pipeline.
- Validate untrusted URLs, content, serialized props, mutation inputs, and resource attributes at their boundary.
- Keep secrets out of client code and serialized output; enforce resource-specific authentication and authorization server-side.
- For RSC stacks, check current React/framework advisories and use a patched release rather than relying on platform mitigations.

#### Version-gated APIs

- Use only APIs provided by the exact installed React and renderer versions.
- React 18 code must not receive React 19-only APIs such as Actions, `useActionState`, `useOptimistic`, `use`, ref-as-prop, or context provider shorthand without an explicit upgrade or compatibility layer.
- React 19.0 code must not receive the React 19.1-only development diagnostic `captureOwnerStack`.
- React 19.0/19.1 code must not receive React 19.2-only APIs such as `<Activity>`, `useEffectEvent`, or `cacheSignal`.
- For libraries supporting React 18 and 19, preserve the shared public surface or use deliberate versioned builds. Do not replace `forwardRef` merely because React 19 accepts `ref` as a prop.
- Treat Canary and experimental APIs as unavailable unless the repository intentionally pins that channel and the task accepts its stability contract.

### 5. Validate using the repository's real matrix

Use repository-provided commands first. Do not install tools, upgrade packages, regenerate broad lockfiles, or change compiler configuration without approval.

When applicable, run:

1. Scoped format, lint, type, and production-build checks.
2. Focused regression tests, then broader tests proportionate to risk.
3. Browser/component checks for interaction, focus, routing, forms, portals, and browser APIs.
4. SSR, streaming, hydration, RSC, or server-action checks for changed boundaries.
5. Accessibility checks plus direct keyboard/focus verification.
6. Bundle, profiler, user-metric, memory, or compiler-output checks for performance claims.
7. React/browser/build/export/framework matrices for compatibility work.
8. Current advisory and dependency checks for security-sensitive server packages or new dependencies.

Do not claim a command passed unless it was executed successfully. If a check cannot run, state the exact reason and what remains unverified.

### 6. Review the final diff

Before completing:

- Re-read changed code without relying on intent.
- Trace render, interaction, async completion, error, retry, cancellation, cleanup, unmount, remount, and rollback paths.
- Check DOM semantics, accessible name, keyboard behavior, focus movement, and announcements.
- Check public props, exports, refs, context, data formats, server/client serialization, browser support, and React-version compatibility.
- Remove stale derived state, accidental effect loops, missing cleanup, broad lint suppressions, debugging output, unnecessary memoization, unstable keys, and unrelated edits introduced by the patch.
- Confirm tests exercise observable behavior and would fail for the old defect when practical.
- Confirm the result is no more abstract, global, or dependency-heavy than the problem requires.

## React Compiler policy

- Treat React Compiler as a repository build decision; inspect version, target, gating, lint, framework support, and production output.
- Adopt incrementally and fix real Rules-of-React violations surfaced by compiler diagnostics.
- Do not bulk-delete `memo`, `useMemo`, or `useCallback`; identity contracts and generated output require focused tests and measurement.
- In compiler-enabled new code, add manual memoization only for demonstrated identity or performance needs.
- Use opt-out directives narrowly, with a concrete incompatibility and follow-up path.

## Lint policy

- Fix owned-code Rules-of-Hooks and dependency problems instead of silencing them.
- Keep suppressions at the narrowest scope and explain the invariant or tool limitation that makes the rule inapplicable.
- Do not enable every available React, JSX, accessibility, performance, or compiler lint as an error without curating it for the repository and version matrix.
- Do not turn heuristic performance lints into correctness rules.
- Let the configured formatter decide formatting; do not spend review effort on mechanically enforced style.

## Testing policy

- Test observable behavior, accessibility, and integration contracts rather than internals or Hook call counts.
- Prefer user-like queries and interactions; use test IDs only without a meaningful semantic selector.
- Cover relevant success, pending, error, retry, cancellation, stale completion, rollback, and regression paths.
- Keep tests deterministic by controlling time, randomness, network, storage, viewport, and browser APIs.
- Avoid incidental scheduler/tree assertions, snapshot-only proof, deprecated shallow rendering, and new `react-test-renderer` usage.

## Dependency and tooling policy

- Add no state, data, form, animation, component, or utility library merely to save a few clear lines or conform to a trend.
- Do not hand-roll sanitizers, complex focus traps, parsers, cryptography, or security-sensitive protocols merely to avoid a dependency.
- Before adding or upgrading a dependency, inspect maintenance, source, license, peer ranges, React support, ESM/CJS exports, browser/runtime support, transitive graph, install scripts, bundle impact, and security advisories.
- Preserve the repository's package manager and lockfile policy. Dependency updates must be intentional and separately reviewable when practical.
- Avoid introducing framework-specific APIs into framework-neutral packages.

## Prohibited default actions

Unless explicitly required, do not:

- Upgrade React, the framework, TypeScript, the router, state layer, form layer, test stack, bundler, or package manager.
- Convert a client-rendered application to SSR, RSC, Server Functions, or a framework.
- Enable React Compiler repository-wide or remove manual memoization repository-wide.
- Add global state, a reducer, context, a custom Hook, compound components, render props, polymorphic `as` props, or portals preemptively.
- Replace all effects, all context, all boolean props, all index keys, all inline callbacks, or all uncontrolled inputs by rule.
- Add `memo`, `useMemo`, or `useCallback` without a concrete identity contract or measured render cost.
- Add Suspense boundaries, transitions, optimistic UI, or loading indicators when no genuine async experience requires them.
- Use `suppressHydrationWarning`, dependency-lint suppression, a remounting `key`, or a one-time ref guard to hide an underlying lifecycle defect.
- Rewrite adjacent code, rename broad APIs, reorganize folders, or replace the design system outside the requested scope.
- Claim performance, accessibility, or security improvement without evidence appropriate to the claim.

## Completion report

Report:

1. What changed and why.
2. Observable, accessibility, public API, server/client, and version contracts intentionally preserved or changed.
3. Tests and validation commands actually executed.
4. Any remaining risk, uncertainty, browser gap, React-version gap, framework gap, or unverified assumption.

For code reviews and audits, use the evidence, severity, confidence, and false-positive rules in [review-playbooks.md](references/review-playbooks.md). Report no finding without a concrete trigger and observable impact or maintainability cost.
