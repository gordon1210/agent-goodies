# Review and Audit Playbooks

Read this reference when reviewing a patch, auditing a React repository, assessing a React/framework migration, evaluating a component API, or reporting performance, accessibility, or security findings. The objective is evidence-based risk reduction, not converting the codebase to a preferred style.

## 1. Review principles

- Review the requested scope first.
- Establish exact React, renderer, framework, compiler, type, test, runtime, and browser contracts before judging code.
- Trace observable behavior, not isolated syntax.
- Prefer concrete failure modes and maintenance costs over generic best-practice statements.
- Distinguish defects from optional improvements.
- Attempt to disprove a suspected problem before reporting it.
- Recommend the smallest sound remediation.
- Do not invent findings when a patch is correct.
- State validation and blind spots precisely.
- Treat generated, vendored, compatibility, migration, story, fixture, and test code according to its role.

A review that produces many low-value comments can hide the one issue that matters.

## 2. Establish review scope

Record the applicable scope:

- changed files or audited packages;
- application, library, design system, widget, or framework integration;
- React 18, React 19.0/19.1, React 19.2+, or a multi-version library matrix;
- client rendering, SSR, hydration, streaming, RSC, Server Functions, or static output;
- supported browsers and runtimes;
- public component/API and package-export expectations;
- accessibility target and critical workflows;
- authentication, authorization, tenant, content, and privacy boundaries;
- test/build commands available and actually executed;
- repository trust level and sandbox constraints.

Do not generalize a finding beyond the versions, routes, users, or deployment modes demonstrated by evidence.

## 3. Review modes

### Patch review

Focus on behavior introduced, changed, or made reachable by the diff.

Inspect:

- task, issue, and acceptance criteria;
- full diff and generated/lockfile changes;
- adjacent callers, consumers, CSS, tests, stories, loaders/actions, and server boundaries;
- old and new render/interaction/async paths;
- compatibility and rollout implications.

Do not turn a focused patch review into a repository audit. A pre-existing issue belongs in findings only when the patch materially relies on it, worsens it, or cannot be safe without addressing it.

### Repository audit

Define packages, routes, surfaces, trust boundaries, deployment modes, and depth. Audit in passes:

1. Versions, architecture, package boundaries, and build/runtime model.
2. Public component and data contracts.
3. Rendering, state, effects, and lifecycle correctness.
4. Async work, Suspense, actions, transitions, races, and recovery.
5. SSR, hydration, RSC, request isolation, and serialization.
6. Accessibility and form/interaction behavior.
7. Security, dependencies, browser capabilities, and privacy.
8. Tests, CI, compatibility matrix, and operational visibility.
9. Performance only where measured or structurally high-risk.

A bounded audit cannot prove absence of defects. Report coverage and unreviewed areas.

### Design review

Review before implementation:

- user and system requirements;
- non-requirements;
- state ownership and source of truth;
- component/public API;
- server/client and trust boundaries;
- async states, cancellation, retries, and rollback;
- accessibility interaction model;
- failure and recovery behavior;
- version/framework constraints;
- alternatives and why added complexity is justified;
- test and rollout strategy.

Reject abstractions justified only by hypothetical reuse or a fashionable pattern.

### Migration review

For React, framework, router, state, test, compiler, bundler, or TypeScript migration:

- separate mechanical changes from semantic changes;
- identify removed/deprecated APIs and changed behavior;
- define old/new compatibility windows;
- inspect types and runtime independently;
- review package peer ranges and duplicate React risk;
- preserve or deliberately change hydration, error, Suspense, ref, form, and effect behavior;
- validate production builds and deployment skew;
- require rollback or staged rollout where failure has broad impact.

Do not combine a major migration with unrelated architecture cleanup unless necessary for compatibility.

### Performance review

Require:

- user-facing metric or resource budget;
- representative production conditions;
- profile, trace, bundle evidence, or a directly provable waterfall;
- correctness/accessibility/security regression checks;
- before/after measurement for claimed improvements.

Render count alone is not a severity signal.

### Security review

Map trust and execution boundaries first. Trace data from source through validation, authorization, serialization, rendering, storage, and side effects.

Check exact installed packages and current advisories for RSC/server-capable stacks. Do not rely on a historical patched-version statement.

### Accessibility review

Evaluate actual user journeys with semantics, keyboard, focus, labels, state, errors, and announcements. Automated lint/scanner output is evidence to investigate, not a complete review.

## 4. Severity model

Use repository-defined severity when available. Otherwise use the following.

### Critical

A credible path to catastrophic impact, such as:

- remote code execution or arbitrary server/module execution;
- broad credential or sensitive-data compromise;
- systemic cross-tenant disclosure or modification;
- persistent script execution affecting privileged users at scale;
- irreversible systemic data loss or corruption;
- complete security-boundary bypass with broad impact.

Critical requires reachability and plausible impact. A vulnerable-looking API name alone is not enough.

### High

A likely or material failure with broad impact, difficult recovery, or no practical user mitigation, such as:

- missing server authorization on a core protected action;
- cross-user cache leakage;
- exploitable stored/reflected XSS on an important surface;
- a core workflow unusable for keyboard users with no alternative;
- stale async completion corrupting persisted user data;
- hydration or deployment behavior that breaks most production requests;
- a breaking published component API presented as compatible;
- uncontrolled resource exhaustion reachable by ordinary untrusted input.

### Medium

A real defect with bounded impact, conditional trigger, recoverable failure, or meaningful maintenance risk, such as:

- out-of-order results displayed for a specific interaction;
- duplicate submission under a timing window;
- leaked listener or timer during repeated navigation;
- an inaccessible control with a reachable alternative but material friction;
- a React-version path that fails for part of the supported matrix;
- incorrect reset behavior when entity identity changes;
- an unsupported browser path claimed as supported;
- a hydration mismatch on a conditional locale/time state with recoverable output.

### Low

A concrete but small reliability, accessibility, diagnosability, compatibility, or maintenance issue with limited impact, such as:

- a non-critical status not announced;
- an error state with poor association but still visible and understandable;
- a bounded redundant request;
- a small public API ambiguity with a demonstrated consumer cost;
- a cleanup issue reachable only in a rare development/tooling path.

### Suggestion

A non-defect simplification, naming improvement, optional performance experiment, consistency improvement, or future hardening idea. Suggestions must not be presented as required fixes.

Severity reflects likelihood and impact in the actual product, not code size, rule category, or reviewer preference.

## 5. Confidence

State confidence when material context is missing:

- **High:** directly demonstrated by code, test, reproduction, specification, or authoritative version behavior.
- **Medium:** strongly implied but depends on an unverified caller, deployment setting, browser, framework transform, or data invariant.
- **Low:** plausible hypothesis requiring targeted evidence; normally ask for or describe the needed verification rather than blocking the patch.

Do not increase severity to compensate for low confidence.

## 6. Finding quality bar

A finding must contain:

1. **Concrete title:** observable failure, not a rule name.
2. **Location:** smallest useful file and line range.
3. **Contract:** expected behavior or boundary.
4. **Trigger:** user action, data, timing, version, browser, route, or deployment state.
5. **Impact:** what users, data, security, accessibility, or operators experience.
6. **Evidence:** traced code path, reproduction, test, specification, or authoritative documentation.
7. **Remediation direction:** smallest sound fix, not an unnecessary rewrite.
8. **Severity and confidence.**

Example:

```markdown
### Medium — A slower search response can replace newer results

`src/search/use-search.ts:41-68`

Each query starts a request, but completion writes results without checking which
query is current. When the `ab` request completes after `abc`, the UI displays
results for `ab` while the input still shows `abc`.

Abort obsolete requests or associate each completion with the active query, and
add a deterministic test that resolves both requests out of order.

Confidence: high.
```

Do not report a rule violation without explaining why it matters in this code.

## 7. Patch review procedure

### Step 1: Restate the behavioral delta

Identify:

- what changes for users, consumers, or operators;
- what must remain compatible;
- new states, Effects, requests, subscriptions, caches, actions, dependencies, or DOM behavior;
- the validation needed to establish correctness.

### Step 2: Map affected boundaries

Map:

- component ownership and public props;
- source of truth and state reset identity;
- event and Effect boundaries;
- data/request ownership;
- server/client and serialization edges;
- authentication/authorization and tenant scope;
- DOM/accessibility interaction model;
- React/framework/browser version gates.

### Step 3: Trace execution paths

Trace applicable paths:

- initial render and empty state;
- ordinary success;
- invalid/boundary input;
- loading/pending and partial content;
- rejection/error and retry;
- duplicate interaction;
- out-of-order completion;
- cancellation, navigation, unmount, and remount;
- Strict Mode setup/cleanup replay;
- optimistic update, rollback, and authoritative reconciliation;
- server error, aborted stream, and hydration mismatch;
- unauthorized and cross-tenant access;
- keyboard/focus/announcement behavior.

### Step 4: Check compatibility

Check:

- exact React API availability;
- runtime and `@types/react` behavior;
- public props, refs, exports, and DOM relied on by consumers;
- framework loaders/actions/caches and client/server directives;
- SSR/RSC serializability;
- supported browsers and polyfills;
- package peer dependencies and duplicate React;
- persisted URL/storage/form/server data.

### Step 5: Inspect tests

Determine whether tests:

- fail against the old defect or missing behavior;
- exercise the meaningful boundary;
- cover relevant error/race/accessibility behavior;
- avoid incidental tree/scheduling assertions;
- remain deterministic and parallel-safe;
- run in the supported CI configuration.

Missing tests are not a standalone defect unless a material behavior remains unverified. Name that behavior and risk.

### Step 6: Validate selectively

Use repository commands. Start focused, then expand according to risk. Do not execute untrusted scripts without a suitable sandbox.

### Step 7: Re-read the final diff

Look for:

- unrelated rewrites;
- lockfile or generated-file churn;
- stale comments and debug output;
- broad lint suppressions;
- accidental client/server boundary changes;
- new public exports or DOM changes;
- unnecessary state/effects/memoization;
- hidden hydration warnings;
- accessibility regressions;
- test snapshots approved without semantic review.

## 8. False-positive controls

Before filing a finding, attempt to disprove it:

- Search for validation or authorization earlier/later in the path.
- Check type/schema constructors and framework guarantees.
- Check the exact installed React/framework version.
- Check whether the component is public or internal.
- Check whether order/identity can actually change.
- Check whether an Effect owns a real external synchronization.
- Check whether a callback identity is observed by a memoized child or API.
- Check whether the operation is cold, bounded, or outside the client bundle.
- Check tests, stories, design-system contracts, and documented deployment assumptions.
- Reproduce timing-dependent behavior with controlled ordering.

Do not report the following mechanically.

### Inline callbacks and objects

An inline callback/object allocation is normally cheap and correct. Report only when identity causes demonstrated expensive invalidation, subscription churn, Effect churn, or a contractual instability.

### Missing memoization

A component without `memo`, `useMemo`, or `useCallback` is not defective. Require measured render cost or a semantic identity contract.

### Existing manual memoization

In a compiler-enabled repository, existing memoization is not automatically obsolete. It may encode an API or protect mixed compiled/uncompiled consumers.

### Boolean props

Independent semantic booleans such as `disabled`, `required`, `readOnly`, or `multiple` are normal. Report boolean proliferation when combinations are invalid/ambiguous or the API creates concrete consumer complexity.

### Index keys

Index keys are valid for a provably static list with no identity-sensitive state. Report when insertion, deletion, sorting, filtering, animation, focus, uncontrolled input, or item-local state can misassociate identity.

### Effects

An Effect synchronizing a subscription, timer, widget, network request, document API, or other external system is legitimate. Report only redundant synchronization, stale behavior, missing cleanup, races, or incorrect dependencies.

### Context

Context is appropriate for coherent shared configuration/state. Report broad invalidation or hidden coupling only when it creates a concrete cost or correctness issue.

### `forwardRef`

`forwardRef` remains necessary for React 18 compatibility and may be part of a library contract. Do not demand ref-as-prop solely because an application uses React 19.

### Uncontrolled inputs

Uncontrolled inputs are valid when the DOM owns transient input and the product does not require controlled synchronization. Report only an actual reset, validation, formatting, or state-coordination failure.

### `dangerouslySetInnerHTML`

The API is not automatically a vulnerability. Trace content trust and sanitization. Trusted static or correctly sanitized content may be valid.

### Barrel exports

A barrel file is not inherently a bundle defect. Check package side effects, tree shaking, transform behavior, and measured output.

### Rerenders

React rendering work is expected. Report excessive rendering only with material work, interaction impact, or a proven avoidable invalidation.

## 9. Migration review checklist

For React 18 to React 19 or later:

- Use React 18.3 warnings as a migration aid when feasible.
- Inventory removed DOM/root/test APIs and legacy component patterns.
- Verify modern JSX transform.
- Review ref callback cleanup and TypeScript inference changes.
- Review Suspense/error reporting changes rather than treating upgrade as compile-only.
- Gate React 19.2 APIs separately from React 19.0.
- Preserve library React 18 public behavior where claimed.
- Run production SSR/hydration and framework builds.
- Review exact RSC security posture.
- Stage compiler adoption separately unless already part of the upgrade plan.

For React Compiler:

- confirm supported compiler and target configuration;
- run lint/diagnostics before broad compilation;
- adopt incrementally;
- preserve behavior tests;
- profile production output;
- do not bulk-delete manual memoization;
- track narrow opt-outs.

## 10. Review output format

For a patch review:

1. Findings ordered by severity, then impact.
2. Open questions or assumptions only when they affect correctness.
3. Validation performed and meaningful gaps.
4. Optional suggestions clearly separated.

For an audit:

1. Executive assessment and exact scope.
2. Findings by severity.
3. Coverage matrix and methods.
4. Positive controls worth preserving.
5. Prioritized remediation sequence.
6. Residual risks and unreviewed areas.

For a migration/design review:

1. Recommendation.
2. Blocking contract issues.
3. Compatibility/migration risks.
4. Smallest viable implementation or staged path.
5. Verification and rollback requirements.

If there are no qualifying findings, say so directly. List only real validation gaps; do not manufacture a style issue to appear useful.

## 11. Remediation prioritization

Prioritize risk reduction per unit of change:

1. Contain active security, data integrity, availability, or accessibility blockers.
2. Add a deterministic reproduction or boundary test where practical.
3. Apply the smallest correct fix.
4. Address the same root cause in directly affected paths.
5. Refactor only when the current structure prevents a safe, understandable fix.
6. Optimize after correctness and only against a defined performance contract.

Do not bundle a large component/state rewrite into an urgent bug fix unless necessary to restore the invariant.

## 12. Completion gate

A review is complete when:

- Scope, versions, rendering model, public contracts, and trust boundaries are explicit.
- Changed and high-risk paths were traced across success, error, race, cleanup, and accessibility behavior.
- Findings meet the evidence bar and duplicates are consolidated.
- Severity reflects actual likelihood and impact.
- False-positive controls were applied.
- Suggested fixes preserve higher-priority contracts and avoid needless architecture.
- Executed validation and remaining blind spots are stated accurately.
- A correct patch is allowed to pass without invented findings.
