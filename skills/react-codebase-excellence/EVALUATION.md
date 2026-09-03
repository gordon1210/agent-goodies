# Evaluation Scenarios

Use these scenarios to detect regressions in the skill's decision quality. They are behavioral checks, not exact-output snapshots.

A successful agent response should establish repository and version contracts, load only relevant references, avoid dogmatic transformations, trace observable behavior, make focused changes, and report validation honestly.

## 1. Derived state synchronized by Effect

**Prompt:** A product list stores `filteredProducts` in state and updates it in an Effect whenever `products` or `filter` changes. Simplify it.

Expected behavior:

- Identifies `filteredProducts` as derived from existing render inputs.
- Computes it during render, memoizing only if measured cost justifies it.
- Removes the redundant state/Effect without changing empty, order, or filter semantics.
- Updates tests around user-visible filtering rather than Hook internals.
- Does not introduce a selector framework or global store.

## 2. Legitimate subscription Effect

**Prompt:** Review a component that subscribes to a WebSocket channel in an Effect and cleans up when `channelId` changes.

Expected behavior:

- Recognizes a real external synchronization boundary.
- Verifies complete dependencies, symmetric cleanup, reconnect/error behavior, and Strict Mode safety.
- Does not demand that all subscription logic move into an event handler.
- Reports no issue if ownership and lifecycle are correct.

## 3. React 18 receives a React 19 API request

**Prompt:** Add `useActionState` to an application pinned to React 18.2 without upgrading dependencies.

Expected behavior:

- Rejects use of the unavailable API.
- Inspects the existing form/mutation stack and implements a React 18-compatible state path.
- Preserves pending, validation, duplicate-submission, and error semantics.
- Does not silently upgrade React or copy a React 19 polyfill.

## 4. React 19.0 receives a React 19.2 API request

**Prompt:** Replace conditional rendering with `<Activity>` in an application pinned to React 19.0.

Expected behavior:

- Identifies `<Activity>` as React 19.2-only.
- Keeps the existing approach or proposes an explicit, separately reviewed upgrade.
- Evaluates whether preserving hidden state/DOM is actually desired.
- Does not import from Canary or an internal React path.

## 5. Out-of-order search results

**Prompt:** A search Effect fetches on every query change. Slow responses sometimes replace newer results. Fix it.

Expected behavior:

- Demonstrates the stale-completion race.
- Aborts obsolete work or associates results with the active query/request identity.
- Handles cancellation separately from user-visible failure where appropriate.
- Adds a deterministic test resolving requests out of order.
- Does not use a wall-clock delay or debounce as the sole correctness fix.

## 6. Independent async waterfall

**Prompt:** A dashboard awaits profile data before starting an independent notifications request. Improve loading performance.

Expected behavior:

- Confirms independence and authorization/resource constraints.
- Starts independent work concurrently or restructures the framework data boundary.
- Preserves partial/error behavior and avoids unbounded parallelism.
- Measures or directly demonstrates the removed latency chain.
- Does not add Suspense merely as decoration.

## 7. Inline callback review

**Prompt:** Review a patch that passes one inline `onClick` callback to a small non-memoized button.

Expected behavior:

- Does not report the allocation as a defect.
- Checks callback correctness and stale-state behavior only where relevant.
- Avoids adding `useCallback` without a consumer identity contract or measured cost.
- Reports no finding if behavior is sound.

## 8. Index key with mutable order

**Prompt:** A reorderable task list uses array indexes as keys, and each row contains an uncontrolled input.

Expected behavior:

- Identifies identity misassociation during reordering.
- Uses a stable task identifier as the key.
- Tests that typed input/state remains attached to the correct task after reorder.
- Does not “fix” the issue by converting every input to controlled state unless required.

## 9. Controlled/uncontrolled form regression

**Prompt:** A refactor changes an input from `defaultValue` to `value` but does not add an `onChange` path.

Expected behavior:

- Identifies the behavior change and read-only/frozen input risk.
- Determines whether the field is intentionally controlled or DOM-owned.
- Restores the correct ownership with initialization/reset behavior.
- Tests typing, reset, and submission rather than component internals.

## 10. Custom clickable element

**Prompt:** A design-system card uses `<div onClick>` as the only way to activate navigation.

Expected behavior:

- Prefers a native link or button matching the actual action.
- Preserves accessible name, keyboard activation, focus visibility, and disabled semantics if applicable.
- Does not solve it by adding only `role="button"` and `tabIndex`.
- Tests keyboard and pointer behavior.

## 11. Untrusted rich HTML

**Prompt:** User-authored HTML from the API is rendered with `dangerouslySetInnerHTML` because “React escapes values.”

Expected behavior:

- Explains that raw HTML bypasses ordinary JSX text escaping.
- Establishes a rich-content allowlist and approved sanitizer/trusted-content boundary.
- Reviews links, SVG/MathML, malformed markup, and storage/publishing path.
- Adds negative security tests.
- Does not propose regex sanitization.

## 12. Client-only authorization

**Prompt:** A delete button is hidden for non-admins, and the React 19 Server Function trusts that UI guard.

Expected behavior:

- Treats the Server Function as an externally callable mutation endpoint.
- Requires server-side authentication and resource-specific authorization.
- Reviews validation, CSRF/origin model, duplicate submission, and audit/error behavior as applicable.
- Keeps the client guard only as UX.
- Assigns severity from actual reach and impact rather than the API name.

## 13. Cross-tenant server cache

**Prompt:** An RSC application caches `getCurrentAccount()` globally under the key `"account"` to reduce database calls.

Expected behavior:

- Identifies missing user/tenant/request dimensions and a cross-tenant disclosure path.
- Distinguishes per-render/request deduplication from cross-request caching.
- Re-scopes or correctly keys the cache and defines invalidation/bounds.
- Adds isolation tests for different authenticated users.
- Checks exact React/framework security advisories and deployment behavior.

## 14. Hydration mismatch hidden by suppression

**Prompt:** A component renders `new Date().toLocaleString()` during SSR and hydration, then adds `suppressHydrationWarning` to remove the warning.

Expected behavior:

- Identifies nondeterministic server/client initial output.
- Chooses an explicit server value, client-only boundary, or post-hydration update according to UX.
- Uses suppression only if the mismatch is intentionally unavoidable and localized.
- Tests production server markup plus hydration.
- Does not use a remounting key as a generic fix.

## 15. Blanket React Compiler rollout

**Prompt:** Enable React Compiler for an established application and delete all `memo`, `useMemo`, and `useCallback` calls in the same patch.

Expected behavior:

- Separates compiler adoption from bulk memoization removal.
- Inspects compiler version, target, gating, lint integration, framework support, and production build.
- Uses incremental rollout and behavior/performance validation.
- Preserves manual identity contracts and mixed compiled/uncompiled boundaries.
- Uses narrow opt-outs only for demonstrated incompatibility.

## 16. React 18/19 library ref compatibility

**Prompt:** A component library supporting React 18 and 19 replaces every `forwardRef` component with React 19 ref-as-prop signatures.

Expected behavior:

- Identifies the React 18 runtime/type compatibility break.
- Preserves a shared `forwardRef`-compatible public surface or defines deliberate versioned builds.
- Reviews peer ranges, `@types/react` matrix, exports, declaration output, and consumer tests.
- Does not treat `forwardRef` deprecation direction as permission for a breaking release.

## 17. Untrusted repository test execution

**Prompt:** Audit a downloaded React repository and immediately run `npm install && npm test`.

Expected behavior:

- Inspects manifests, lifecycle scripts, workspaces, plugins, executable config, code generation, native/downloaded binaries, and test setup first.
- States that install and test commands can execute repository-controlled code.
- Uses an isolated environment without host credentials or sensitive mounts.
- Does not claim static inspection proves safety.

## 18. Deprecated renderer-based tests

**Prompt:** Add new component tests with `react-test-renderer` snapshots because no browser is required.

Expected behavior:

- Rejects the deprecated renderer as the default for new tests.
- Uses the established DOM/component test stack and semantic queries/interactions.
- Chooses a real browser or integration harness for behavior the DOM emulator cannot establish.
- Keeps snapshots focused and supplements them with semantic assertions.

## 19. Whole-repository production audit

**Prompt:** Audit a medium React 19.2 SSR/RSC application for production readiness.

Expected behavior:

- Establishes exact packages, framework, rendering/deployment model, public APIs, browsers, trust boundaries, and compiler state.
- Loads all applicable references and uses the audit matrices.
- Reviews request isolation, RSC advisories, authorization, hydration, async lifecycle, accessibility, tests, dependency execution, and measured performance.
- Reports scope, evidence, positive controls, prioritized remediation, and blind spots.
- Does not bury critical findings under style comments or imply complete proof of safety.

## 20. Correct focused patch

**Prompt:** Review a focused, tested component fix whose behavior, accessibility, security, version compatibility, and public API are correct.

Expected behavior:

- Reports no qualifying findings.
- States meaningful validation performed and any genuine unverified area.
- Keeps optional simplifications clearly non-blocking.
- Does not invent memoization, component-splitting, naming, or folder-structure complaints.

## 21. React 19.1 Owner Stack used as production telemetry

**Prompt:** On React 19.1, call `captureOwnerStack` in the production error reporter and require it for every incident.

Expected behavior:

- Recognizes that `captureOwnerStack` requires React 19.1 or newer and is development-only.
- Rejects production behavior or required telemetry that depends on an Owner Stack.
- Uses supported root callbacks, Error Boundaries, application context, and framework observability for production diagnostics.
- Treats Component Stacks and Owner Stacks as distinct signals and avoids attaching sensitive payloads merely for debugging.

## Scoring rubric

Score each scenario from 0 to 2:

- **0:** violates a core rule, misses the central failure, recommends an unavailable API, creates a material regression, or reports a dogmatic false positive.
- **1:** reaches a mostly sound result but misses an important contract, version boundary, negative path, or adds avoidable complexity.
- **2:** follows the expected behavior with evidence, appropriate scope, version awareness, and honest validation.

A release should score at least **40/42**, with no zero in scenarios **3, 4, 5, 8, 10, 11, 12, 13, 14, 15, 16, 17, 19, or 21**.

## Evaluation method

For each scenario:

1. Give the agent only the prompt and a minimal representative fixture/repository when needed.
2. Record which references it selected and whether that selection was proportionate.
3. Score the proposed decision before judging prose quality.
4. Penalize fabricated validation, unsupported severity, unavailable APIs, and unrelated rewrites.
5. Re-run failed scenarios after changing `SKILL.md` or a routed reference.
6. Add a regression scenario when a real agent failure reveals a new decision boundary.

Do not tune wording to one model's exact response. Preserve the behavioral contract across capable Agent Skills hosts.
