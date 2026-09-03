# Server, Browser, and CI Verification

Read this reference when testing SSR, hydration, React Server Components, Server Functions, React Compiler, React-version compatibility, real-browser behavior, security, accessibility, performance, or CI policy. Use the repository and framework's real integration layer; component mocks cannot prove server or browser contracts.

## 1. SSR output

Use the framework's server test harness where available. Validate meaningful aspects of the server response:

- status, headers, redirects, and cache policy;
- escaped and authorized content;
- stable identifiers and document structure;
- no request-state leakage;
- error and abort behavior;
- streaming shell/content sequencing where contractually relevant;
- CSP nonce/resource integration;
- no secret serialized into HTML.

Avoid brittle full-document snapshots for large pages. Assert critical semantics and use focused snapshots only for stable complex fragments.

## 2. Hydration

Hydration tests require server markup plus client hydration, preferably in a real browser for browser-dependent behavior.

Cover:

- deterministic initial output;
- `useId`/identifier consistency;
- locale, time, random, media-query, and storage boundaries;
- recoverable mismatch reporting where configured;
- user interaction before or during hydration;
- external-store server snapshots;
- streamed or framework-owned route behavior;
- deployment skew where supported.

Do not use `suppressHydrationWarning` in the fixture to hide the failure being tested.

## 3. React Server Components and Server Functions

RSC behavior is framework/bundler-owned. Use the supported integration harness rather than simulating Flight payloads in ordinary DOM tests.

Verify as applicable:

- server/client module boundaries;
- serializable props;
- authorization on reads and Server Functions;
- request/tenant cache isolation;
- error redaction;
- streaming and navigation behavior;
- stale client/server deployment compatibility;
- exact package versions required by current advisories.

A component unit test cannot validate the RSC transport or bundler contract.

## 4. React Compiler

Validate compiler adoption in the actual production transform:

- compile representative modules;
- run behavior tests with the compiler enabled;
- inspect compiler diagnostics and lint output;
- profile production behavior rather than assuming memoization helped;
- test libraries/build outputs in the mode consumers receive;
- preserve a controlled opt-out for incompatible code while fixing root causes.

Do not delete existing `memo`, `useMemo`, or `useCallback` across the repository in one unreviewed change. Remove manual memoization only when compatibility, semantics, and measured behavior remain sound.

## 5. React 18 and React 19 compatibility

Applications should test the single installed version they support. Libraries or shared packages claiming React 18/19 support should define a real matrix.

Check:

- minimum and maximum peer ranges;
- runtime tests against supported majors;
- type tests against supported `@types/react` majors where applicable;
- exports/build artifacts;
- ref behavior and public component types;
- server entry points and conditions;
- no accidental React 19.2 API in a React 19.0 or React 18 path;
- duplicate React detection in representative consumers.

Do not infer compatibility because TypeScript compiled once against the newest types.

## 6. Removed and deprecated test APIs

Do not introduce new dependencies on:

- `react-test-renderer`;
- shallow rendering as the main confidence layer;
- removed `react-dom/test-utils` helpers;
- legacy root APIs in new tests.

When maintaining an existing React 18 suite, migrate incrementally. Preserve useful regression coverage while moving toward DOM or integration tests that exercise user-visible behavior.

## 7. Mocking policy

Mock at intentional system boundaries, not every module between the component and the boundary.

Prefer:

- a real reducer/store with an isolated instance;
- a request-level mock server for HTTP behavior;
- a fake clock abstraction for time-sensitive domain logic;
- lightweight adapters for browser capabilities;
- actual child components unless their independent cost or behavior obscures the test.

Avoid:

- mocking React hooks globally;
- replacing every child with a stub;
- asserting exact internal call order without a contract;
- broad module mocks that silently diverge from exports;
- reimplementing framework routing or RSC behavior in mocks.

A mock must model the failure and concurrency behavior the test depends on.

## 8. Network tests

Exercise success, validation, authentication, authorization, timeout, abort, malformed response, retry, and stale-result behavior proportionate to risk.

Assert request method, route, essential headers, and validated payload when these are contracts. Avoid asserting incidental header ordering or transport internals.

Prevent ambient network access in deterministic tests unless the suite explicitly owns an integration environment.

## 9. Browser end-to-end tests

Use E2E tests for critical cross-boundary journeys such as:

- authentication and session changes;
- navigation and deep links;
- server mutations and persistence;
- upload/download;
- browser capabilities;
- hydration and streaming interactions;
- multi-tab/session behavior;
- focus, keyboard, and overlay workflows;
- production security headers or CSP;
- recovery from server/client failures.

Keep journeys focused and seed data through stable APIs/fixtures. Do not make every component case an expensive E2E test.

## 10. Accessibility verification

Combine:

- semantic queries in component/integration tests;
- automated accessibility checks;
- keyboard/focus assertions;
- real-browser checks for complex widgets;
- manual screen-reader and zoom/reflow review for high-risk UI.

Automated scanners do not prove usable focus order, meaningful announcements, understandable errors, or correct interaction models.

## 11. Visual regression

Visual tests are useful for stable layout, responsive variants, themes, complex charts, and component-library surfaces.

Control:

- fonts and rendering environment;
- animations and time;
- random/test data;
- viewport and device scale;
- network-loaded assets;
- reduced-motion and color-scheme variants.

Do not approve broad snapshot changes without understanding why pixels changed. Visual equality does not establish semantics or accessibility.

## 12. Performance verification

Use production builds and representative devices/data. Record baseline conditions.

Depending on the contract, test:

- Core Web Vitals/RUM guardrails;
- route or interaction budgets;
- bundle/chunk size;
- server render and data-fetch timing;
- hydration cost;
- memory after repeated navigation;
- list rendering at expected scale;
- React Profiler output for a controlled interaction.

Avoid microbenchmarks that omit the browser/server work dominating the real path.

## 13. Security verification

Add negative tests at trusted boundaries for:

- authorization and tenant isolation;
- unsafe rich content and URLs;
- CSRF/origin policy;
- serialization leakage;
- cache key scope;
- malformed/oversized input;
- replay/idempotency;
- current package/advisory policy where CI owns it.

Do not claim a component snapshot proves the server boundary safe.

## 14. Determinism and isolation

Tests must not depend accidentally on:

- execution order;
- wall-clock time or local timezone;
- random values without a seed;
- shared browser storage;
- global mutable stores;
- ambient network;
- ports left by another test;
- previous navigation/session state;
- locale or environment defaults;
- production credentials.

Reset only state the test owns. Prefer constructing isolated resources over global cleanup that can hide leaks.

## 15. Flake handling

Do not solve flakes by increasing retries or timeouts before identifying the cause.

Classify:

- missing synchronization;
- leaked state/resource;
- nondeterministic fixture;
- product race;
- environment capacity;
- external dependency;
- browser-specific behavior.

Retries may provide temporary containment for known infrastructure noise, but they must not make a real race appear healthy.

## 16. Snapshot policy

Use snapshots for complex, stable output where the diff is reviewable. Keep explicit assertions for critical semantics, security, and accessibility.

Avoid snapshots of:

- entire application pages with frequent unrelated churn;
- generated class names or non-deterministic IDs;
- huge serialized stores or RSC payloads;
- implementation detail trees from deprecated renderers;
- errors containing unstable stack traces.

A snapshot update is a behavior decision, not routine maintenance.

## 17. Coverage

Coverage helps locate unexercised code. It does not measure assertion quality, boundary realism, race coverage, or usability.

Use coverage as a diagnostic and repository guardrail, not as the sole acceptance criterion. Critical paths may require near-complete meaningful branch coverage while low-risk declarations do not.

Do not add tests with no behavioral assertion merely to satisfy a percentage.

## 18. CI validation order

Use repository-provided commands first. A typical risk-scaled order is:

1. Formatting or generated-file consistency.
2. Type checking for affected packages/configurations.
3. Lint and React Compiler diagnostics where configured.
4. Focused unit/component tests.
5. Broader package/workspace tests.
6. Production build.
7. SSR/hydration/RSC integration checks.
8. Browser, accessibility, security, bundle, and performance checks as applicable.
9. React/version/browser matrix for libraries or compatibility changes.

Do not install tools, rewrite lockfiles, upgrade runtimes, or change CI policy merely to run one local check without approval.

## 19. Test review questions

Before accepting a test, ask:

- Would it fail for the old bug or absent behavior?
- Does it exercise the meaningful boundary?
- Could it pass while the user-visible behavior is broken?
- Is synchronization explicit?
- Is cleanup/parallel execution safe?
- Is the assertion resilient to behavior-preserving refactoring?
- Does it cover the relevant error/race/accessibility path?
- Does CI actually run it in the supported configuration?

Missing tests are a finding only when an important behavior remains materially unverified. State that behavior and risk.

## 20. Verification reporting

Report commands exactly as executed and distinguish:

- passed;
- failed;
- skipped by configuration;
- unavailable in the environment;
- not run due to trust/sandbox constraints;
- remaining unverified platform/version behavior.

Do not say “tests pass” when only a focused subset ran. Do not infer production build success from type checking.

## 21. Completion gate

Before completing:

- Tests target observable contracts and identified risks.
- Query and interaction style reflects actual users.
- Async behavior is deterministic and race-aware.
- Effects, cleanup, Strict Mode, and external resources are covered where relevant.
- SSR, hydration, RSC, compiler, and version behavior use the real integration layer.
- Accessibility and security have negative/interaction checks proportionate to risk.
- The supported React/type/browser matrix is explicit.
- CI commands are repository-aligned.
- No deprecated React testing API was added.
- Executed validation and remaining gaps are reported honestly.
