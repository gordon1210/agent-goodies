# Testing and Verification

Read this reference for test design, runtime versus type-level evidence, linting, type-checking, builds, declarations, package-consumer tests, browser/E2E tests, compiler/runtime matrices, coverage, fuzzing, CI, and honest validation reporting.

## 1. Verification starts from the changed contract

Choose checks from the risks touched by the change:

| Change | Minimum focused verification |
|---|---|
| Pure internal logic | Runtime regression test plus normal type-check/lint scope |
| External input/schema | Valid, malformed, boundary, adversarial, and resource-limit tests |
| Public library API | Runtime consumer test, type tests, declaration/package inspection, SemVer review |
| Package exports or module mode | Packed-package tests in every promised loader/runtime |
| tsconfig or compiler generation | Effective config, full type-check/build, declarations, tooling and compiler matrix |
| Async or background behavior | Rejection, cancellation, timeout, saturation, late completion, and shutdown tests |
| Browser UI | Component behavior plus real-browser coverage for platform/security/accessibility-sensitive paths |
| SSR/server-client boundary | Server and client builds, serialization, hydration, security, and production-mode tests |
| Parser/decoder/protocol | Malformed, truncated, oversized, ambiguous, round-trip, and fuzz/property tests where valuable |
| Database/schema/migration | Migration, rollback/recovery, concurrency, mixed-version, and real-driver tests |
| Performance fix | Representative before/after benchmark or profile plus correctness/resource regression suite |
| Build/code generation | Clean generation/build, stale-output detection, generated diff, artifact execution |
| Security boundary | Abuse cases, authorization scope, redaction, limits, and dependency/build execution review |

Do not substitute one large generic test run for a focused regression test that proves the intended behavior.

## 2. Distinguish evidence types

A TypeScript project needs several kinds of evidence:

- **Runtime tests:** prove observable JavaScript behavior for exercised cases.
- **Type-checking:** proves the selected compiler accepts the selected project/configuration.
- **Type tests:** prove public inference, assignability, expected errors, narrowing, or declaration behavior.
- **Linting:** detects configured code patterns; type-aware linting may use compiler information but is not a build.
- **Build/bundle checks:** prove artifacts can be created under one pipeline.
- **Artifact/consumer tests:** prove packed or deployed output resolves and executes as consumers see it.
- **Browser/platform tests:** prove behavior in actual engines/environments.
- **Static security/dependency checks:** identify known or patterned risk; they do not prove safety.

No single layer replaces the others. A passing type-check does not validate external data. A passing unit test does not prove declaration compatibility. A successful source-run test does not prove the package or production bundle.

## 3. Test layers

### Unit tests

Use for:

- Pure domain logic.
- Parsing and validation helpers.
- State transitions and error classification.
- Boundary values and combinatorial cases.
- Small lifecycle components with controlled dependencies.

Keep unit tests fast and deterministic. Do not expose implementation publicly merely to test it.

### Integration tests

Use for:

- Multiple modules/packages interacting.
- Filesystem, database, HTTP, queue, process, worker, framework, and configuration boundaries.
- Real serialization and runtime validation.
- Dependency failure, cleanup, and retry semantics.
- Public APIs as an external caller uses them.

Prefer real lightweight boundaries when mocks would reproduce the implementation rather than the contract.

### Component tests

Use framework-supported component tests for UI behavior where they provide realistic rendering, events, state, and accessibility semantics. Keep framework internals out of assertions.

### End-to-end tests

Use selectively for critical user journeys and deployment boundaries:

- Authentication/authorization transitions.
- Navigation and hydration.
- Real browser APIs.
- Cross-service wiring.
- Production artifact startup.
- Packaging/installation flows.

Keep lower-level behavior covered by faster tests so E2E failures remain diagnosable.

## 4. Runtime tests versus type tests

A runtime test cannot prove a type rejects misuse. A type test cannot prove a function behaves correctly.

Use type tests for:

- Public generic inference.
- Overload selection.
- Discriminated union narrowing.
- Branded/opaque constructor boundaries.
- Expected compile-time rejection.
- Package declaration consumption.
- Compatibility across supported TypeScript generations.

Use the repository's existing type-test mechanism, such as compiler fixture projects, `@ts-expect-error`, assertion helpers, or a dedicated type-test tool. Do not add a new framework for one simple contract.

Rules:

- Keep expected errors on the exact expression and explain why the error is required.
- Ensure an expected-error directive becomes unused if the compiler stops reporting the error.
- Avoid asserting exact diagnostic wording unless diagnostics are the product.
- Verify positive and negative cases.
- Compile tests as an external consumer when the public package surface matters.
- Run type tests with every compiler generation the package promises.

## 5. Test behavior, not implementation trivia

A good test states one coherent behavior and may contain multiple related assertions.

Prefer:

- Input, operation, observable result.
- Domain-specific names and failure reasons.
- Stable semantic assertions.
- Explicit regression setup for the bug being fixed.
- Public APIs and artifacts at integration boundaries.

Avoid:

- One test per line, getter, or private helper.
- Tests coupled to internal call order without a contract.
- Mocking every dependency until the test only confirms the mock setup.
- Exact full error strings when structured classification exists.
- Broad snapshots where a few semantic assertions are clearer.
- Tests that still pass if the intended behavior is removed.
- Type assertions in tests that bypass the misuse the test should detect.

For a bug fix, prove the test fails against the old behavior when practical.

## 6. Determinism and isolation

Tests may run concurrently, in arbitrary order, under different process counts, and with caches.

- Do not share fixed filenames, ports, database rows, environment variables, local-storage keys, current directories, users, queues, or process-global registries without explicit isolation.
- Use unique temporary directories/resources and robust cleanup.
- Bind ephemeral ports rather than guessing, while accounting for handoff races.
- Use seeded randomness and preserve the seed on failure.
- Inject clocks or use fake timers instead of sleeping.
- Avoid ambient network access in unit tests.
- Bound every wait; tests should fail rather than hang.
- Restore environment, globals, mocks, timers, fetch patches, and process state even on failure.
- Avoid depending on locale, timezone, filesystem ordering, object key ordering outside guarantees, or machine CPU count without explicit setup.
- Run important suites under more than one shard/order when order dependence is a known risk.

Code that inherently mutates process-global state may need a separate test process rather than global serialization of the entire suite.

## 7. Boundary and failure coverage

For each changed operation, consider relevant cases:

- Empty, missing, null, undefined, zero, false, and minimum input.
- Maximum accepted input and one beyond it.
- Malformed, truncated, duplicated, reordered, unknown, or ambiguous fields.
- Unicode normalization, surrogate pairs, invalid encoding at byte boundaries, and locale-sensitive operations.
- Numeric precision, overflow-like arithmetic, `NaN`, infinities, negative zero, bigint, and narrowing.
- Paths, URL schemes, redirects, symlinks, case sensitivity, and platform-specific separators.
- Missing permissions, unavailable dependencies, connection loss, timeout, cancellation, and shutdown.
- Partial writes, stale data, optimistic-concurrency conflict, and duplicate delivery.
- Thrown non-`Error` values and late promise rejection.
- Cleanup after each failure point.

Test only applicable categories, but make omission deliberate.

## 8. Validation and schema tests

For runtime validators/parsers:

- Test valid minimal and full examples.
- Test each required field and semantic invariant.
- Test unknown-field policy and duplicate keys where the parser exposes them.
- Test maximum sizes, nesting, array counts, and aggregate decoded size.
- Test prototype-related keys and inherited properties for object-like inputs.
- Test error redaction and bounded diagnostics.
- Test version compatibility and migrations.
- Test that validated output has the intended normalized representation.

Do not rely exclusively on generated/random cases; keep readable regression fixtures for important contracts.

## 9. Property-based and fuzz testing

Property tests are useful when many inputs share a compact invariant:

- Parse/serialize round trips subject to the format's information loss.
- Normalization idempotence.
- Ordering and set laws.
- State-machine transitions.
- Reference versus optimized implementation equivalence.
- Permission/resource-scope invariants.
- Generated encoder/decoder compatibility.

Fuzzing is valuable for:

- Parsers, codecs, archives, URL/path handling, protocol frames, and schema validators.
- JavaScript/TypeScript transforms and code generators.
- Inputs where a crash, hang, excessive allocation, regex blowup, or injection is security-relevant.

A fuzz target should:

- Be deterministic for one input.
- Avoid unbounded external side effects.
- Apply memory/time/depth limits.
- Assert useful invariants, not only “does not throw.”
- Preserve minimized regressions.

Do not add fuzz infrastructure to trivial code without a risk-based reason.

## 10. Async and concurrency tests

Use controlled promises, abort controllers, fake timers, test servers, and deterministic queues to exercise:

- Rejection and thrown non-`Error` values.
- Cancellation before start and at meaningful suspension points.
- Timeout while underlying work completes or rejects late.
- Partial completion of aggregate operations.
- Queue saturation and capacity deadlines.
- Retry classification and idempotency.
- Stream backpressure, early exit, source/sink failure, and cleanup.
- Worker/process crash and forced termination.
- Repeated shutdown signals and partial startup.
- Stale UI responses and component unmount/navigation.

Avoid timing races with arbitrary sleeps. A test should orchestrate the state transition it intends to verify.

## 11. Mocks, fakes, and test seams

Choose the least fake boundary that keeps tests deterministic and meaningful:

- Pure fake for a domain-owned external capability.
- In-memory implementation when semantics genuinely match.
- Protocol-level test server for HTTP/RPC behavior.
- Ephemeral real database/container when driver/schema/transaction semantics matter and repository infrastructure supports it.
- Spy only when call occurrence/order is itself part of the contract.

Reject mocks that:

- Duplicate the implementation under test.
- Return values impossible for the real dependency.
- Hide serialization, retry, cancellation, transaction, or module-loading behavior.
- Require broad type assertions to satisfy interfaces.
- Become a second independently maintained specification.

Do not add interfaces solely for mocking when a function parameter, existing client boundary, or local test server is simpler.

## 12. Snapshot tests

Use snapshots for complex, human-reviewed stable output such as:

- Generated code or documents.
- Compiler/linter diagnostics when wording is intentionally part of the product.
- Structured CLI output.
- UI rendering where semantic queries alone are insufficient.
- Large protocol examples with stable representation.

Rules:

- Review snapshot diffs as code.
- Normalize timestamps, paths, random IDs, ports, ordering, and platform-specific separators.
- Keep explicit assertions for status, authorization, redaction, accessibility, and critical fields.
- Avoid giant snapshots that hide meaningful changes.
- Do not auto-accept snapshots in CI or accept unrelated broad changes.

## 13. Browser tests

DOM emulators are useful for fast logic and component tests but do not reproduce all browser behavior.

Use real-browser tests when behavior depends on:

- Layout, focus, selection, scrolling, pointer/touch input, or accessibility tree.
- Navigation, history, service workers, storage, CSP, cross-origin behavior, downloads, or uploads.
- Streams, workers, media, WebAssembly, or browser-specific APIs.
- Hydration and production bundling.
- Security-sensitive DOM sinks or URL behavior.
- Supported engine differences.

Test only the browser matrix the product promises, but include enough engines to cover materially different behavior.

## 14. Accessibility verification

Automated accessibility rules are useful but incomplete.

As applicable, verify:

- Semantic roles, names, labels, and relationships.
- Keyboard operation and visible focus.
- Focus movement after navigation, dialogs, errors, and async updates.
- Screen-reader announcements for dynamic status.
- Contrast and reduced-motion behavior through design/system tooling.
- Zoom/reflow and responsive interaction.
- Error identification and recovery.

Prefer semantic user queries over brittle CSS selectors in component/E2E tests. Keep manual checks for critical flows where automation cannot establish usability.

## 15. Package and declaration tests

For libraries or independently consumed packages:

1. Build or pack from a clean checkout.
2. Inspect the packed file list.
3. Install the tarball into representative clean consumers.
4. Type-check consumer examples through public exports only.
5. Execute runtime examples in promised module systems/runtimes.
6. Verify declaration/source-map paths and no monorepo-only references.
7. Test peer dependency and optional dependency behavior.
8. Test tree shaking/side effects when advertised.
9. Run type tests under supported TypeScript 6/7 versions.

Workspace source tests can pass while the published package is broken. Artifact tests close that gap.

## 16. Type-check and build matrices

Derive the matrix from actual support claims:

- Affected tsconfig projects and dependents.
- TypeScript 6 and/or 7.
- Node/Bun/Deno/browser/worker/edge environments.
- ESM and/or CommonJS.
- Development and production build modes when semantics differ.
- Optional packages, peer dependencies, feature flags, and generated clients.
- Supported operating systems/architectures for path/native/process behavior.

Do not test an arbitrary combinatorial powerset. Curate supported combinations and include negative checks for intentionally invalid ones.

## 17. Compiler configuration verification

After tsconfig changes:

- Inspect the effective configuration.
- Verify included files and project boundaries.
- Check declaration/output locations.
- Trace representative module resolution when aliases/conditions change.
- Validate clean and incremental/project-reference builds.
- Ensure test/generated/build directories are included or excluded deliberately.
- Confirm editor and CI select the intended config/compiler.
- Compare declarations and diagnostics across supported compiler generations.

A root `tsc --noEmit` command may not check referenced projects or package-specific configs the way CI/build does. Follow repository scripts and inspect what they execute.

## 18. Linting

Lint policy should detect credible defects and remain compatible with the repository's parser/compiler matrix.

- Run the configured linter and formatter through repository scripts.
- Distinguish syntax-only from type-aware lint rules.
- Ensure type-aware rules point to the intended tsconfig(s) without pulling unrelated files into expensive programs.
- Curate rules for promises, unsafe access, assertions, imports, security, framework lifecycle, and tests according to project risk.
- Fix owned-code warnings rather than adding broad disable comments.
- Keep suppressions narrow and explain the current invariant.
- Avoid enabling every strict/stylistic/experimental rule as an error in one change.
- Treat linter/parser upgrades as toolchain changes with TypeScript-generation compatibility review.
- Do not use formatting rules to replace a formatter.

Lint output is evidence, not proof of runtime safety or API compatibility.

## 19. Coverage and mutation testing

Coverage identifies code not exercised by a suite. It does not measure assertion strength, input space, type contracts, browser realism, race coverage, or requirement correctness.

- Investigate uncovered error, cleanup, authorization, and boundary paths first.
- Do not optimize tests for a percentage alone.
- Exclude generated code only with a documented policy.
- Review branch/function insight, not only lines.
- Use thresholds only when the team owns them and they do not encourage low-value tests.

Mutation testing can reveal weak assertions for important pure logic. Use it selectively; it can be expensive and noisy around generated, framework, and type-only code.

## 20. Flaky tests

A retry can collect diagnostics but must not normalize flakiness.

When a test flakes:

1. Preserve logs, seed, browser trace, timing, worker, and shard information.
2. Identify time, ordering, process-global state, external service, port, cache, or resource assumptions.
3. Make the dependency deterministic or isolate it.
4. Keep retries temporary or limited to known external instability.
5. Track and remove the root cause.

A test that passes on retry is still a failed reliability signal.

## 21. CI design

A proportionate pipeline may separate:

1. Metadata/lockfile validation and formatting.
2. Type-check and type-aware lint.
3. Unit/integration tests.
4. Production build and generated-output consistency.
5. Type/declaration/package-consumer tests.
6. Runtime/module/browser/platform/compiler matrix.
7. Dependency, license, secret, and supply-chain policy.
8. E2E/migration/security tests.
9. Scheduled performance, fuzz, mutation, broad browser, or compatibility checks.

Pin actions/tools according to repository policy. Use immutable/frozen installs. Cache only declared outputs and inputs; cache correctness must never be required for build correctness.

Keep required checks fast enough to run reliably, but do not move a merge-critical contract to scheduled CI merely because it is inconvenient.

## 22. Untrusted execution

Installation, type-checking, linting, tests, builds, generators, and package scripts can execute code through:

- Lifecycle scripts.
- Native addon builds.
- Compiler/linter/bundler plugins.
- Config files loaded as JavaScript/TypeScript.
- Test setup and test files.
- Code generators and schema downloads.
- Framework/build hooks.
- Package-manager plugins.

For unknown code, inspect statically first and execute in an isolated environment without host credentials, broad home mounts, SSH agents, Docker sockets, cloud metadata, or unrestricted resources/network.

## 23. Validation reporting

Record:

- Package manager and version used.
- Runtime, TypeScript compiler, target platform, and relevant environment.
- Projects/packages/configs checked.
- Exact commands that succeeded.
- Commands that failed and whether failure indicates a defect or environment limitation.
- Checks skipped and why.
- Remaining compiler, runtime, module, browser, artifact, or platform gaps.

Never replace this with “all tests pass” unless the actual promised matrix was executed.

## Verification completion checklist

- A focused regression test proves the requested behavior.
- Runtime, type, lint, build, and artifact evidence are not conflated.
- Tests are deterministic, isolated, bounded, and parallel-safe.
- Error, cleanup, cancellation, authorization, and boundary paths relevant to the change are covered.
- Type tests protect public inference and misuse where applicable.
- Production and package artifacts are tested when source behavior is insufficient.
- Compiler/runtime/module/browser matrices match real support claims.
- Every reported command was actually executed; gaps are explicit.
