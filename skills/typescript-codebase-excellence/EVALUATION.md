# Evaluation Scenarios

Use these scenarios to detect regressions in the skill's decision quality. They are behavioral checks, not exact-output snapshots.

A successful agent response should inspect repository policy before acting, select only relevant references, distinguish compile-time from runtime evidence, explain material assumptions, make focused changes, and report validation honestly.

## 1. Optional CLI configuration

**Prompt:** A TypeScript CLI crashes when an optional configuration file is absent. Fix it without changing successful output.

Expected behavior:

- Inspects the existing CLI configuration precedence, diagnostics, and exit-code contract.
- Distinguishes an absent optional file from malformed, inaccessible, or explicitly requested configuration.
- Makes a focused fix without introducing a configuration framework or broad error rewrite.
- Tests stdout, stderr, and exit status.
- Does not add a non-null assertion or catch-and-ignore every filesystem error.

## 2. Untrusted JSON assertion

**Prompt:** Fix a type error by changing `JSON.parse(input)` to `JSON.parse(input) as User`.

Expected behavior:

- Rejects the assertion as runtime validation.
- Identifies `input` as untrusted and validates required structure, semantics, limits, and unknown-field policy at the boundary.
- Reuses an existing schema/validator if present rather than adding a second validation stack.
- Keeps the validated internal type narrow and tests malformed/adversarial input.

## 3. Path alias works only in the editor

**Prompt:** Add `@core/*` under `compilerOptions.paths`; imports now type-check but fail in Node.js production.

Expected behavior:

- Explains that TypeScript path mapping alone does not rewrite runtime specifiers.
- Inspects actual emit owner, module resolution, package exports/imports, bundler/runtime loader, and production artifact.
- Chooses the smallest repository-compatible solution instead of adding an arbitrary runtime hook.
- Adds artifact-level or runtime validation.

## 4. Dual ESM/CommonJS library

**Prompt:** Publish one library as ESM and CommonJS by copying the same JavaScript files into two directories.

Expected behavior:

- Reviews package `type`, extensions, export conditions, declaration routing, default/named interoperability, singleton identity, and consumer matrices.
- Does not claim a dual package is correct based only on two successful builds.
- Prefers one module format when dual publishing is not a real requirement.
- Tests packaged consumption from supported ESM and CommonJS callers when dual output is required.

## 5. TypeScript 6 to 7 migration with compiler API use

**Prompt:** Replace TypeScript 6 with TypeScript 7 because the native compiler is faster. The repository has a custom transformer and a documentation tool importing `typescript`.

Expected behavior:

- Separates `tsc` CLI compatibility from compiler-API compatibility.
- Inventories all direct and transitive tools importing `typescript`, custom transformers, language-service plugins, AST assumptions, and editor integrations.
- Does not perform a blind package-version replacement.
- Uses a staged coexistence or compatibility strategy when required and verifies emitted JavaScript, declarations, diagnostics, and tool output.
- Keeps TypeScript 6 when a required integration lacks a sound migration path.

## 6. TypeScript 7 parallelism in constrained CI

**Prompt:** Set TypeScript 7 to maximum checker and builder parallelism in a 4 GiB CI runner.

Expected behavior:

- Rejects maximum parallelism as a universal speed setting.
- Measures wall time, peak memory, process count, cache effects, and CI limits.
- Accounts for multiplication between project builders and checker workers.
- Uses a deliberate fixed configuration only when it improves the actual pipeline without instability.

## 7. TypeScript 6 default changes

**Prompt:** Upgrade to TypeScript 6 and fix the resulting missing Node globals by adding broad ambient types to every project.

Expected behavior:

- Inspects each tsconfig's intended environment and the TypeScript 6 ambient-type/default changes.
- Adds Node types only to projects that execute in Node.js.
- Keeps browser, worker, server, test, and build-tool globals isolated.
- Checks `rootDir`, `target`, `module`, `moduleResolution`, strictness, and side-effect import behavior rather than patching one symptom.

## 8. Deprecated configuration hidden by `ignoreDeprecations`

**Prompt:** Preserve `target: es5`, legacy Node resolution, and `baseUrl` by extending `ignoreDeprecations` before moving to TypeScript 7.

Expected behavior:

- Rejects suppression as a migration strategy.
- Identifies the runtime/bundler requirements behind each option and replaces deprecated behavior explicitly.
- Does not raise targets or change module behavior without checking supported consumers.
- Runs TypeScript 6 migration checks before attempting TypeScript 7.

## 9. JavaScript/JSDoc project on TypeScript 7

**Prompt:** A large `checkJs` project uses constructor functions, Closure-flavored JSDoc, expando properties, and declaration emit from JavaScript. Move it to TypeScript 7.

Expected behavior:

- Recognizes this as a high-risk compatibility area rather than a routine compiler upgrade.
- Audits unsupported or changed JSDoc/JavaScript constructs and declaration output.
- Uses representative fixtures and package-consumer tests.
- Proposes staged source modernization or continued TypeScript 6 use when migration cost is not authorized.

## 10. Floating background promise

**Prompt:** Start an async telemetry flush with `void flush()` during shutdown so shutdown remains fast.

Expected behavior:

- Identifies that `void` only discards the promise; it does not own errors or completion.
- Clarifies whether telemetry is best-effort or required, then defines a bounded shutdown policy.
- Observes rejection and does not wait indefinitely.
- Does not turn every fire-and-forget operation into an unbounded global task registry.

## 11. Timeout misconception

**Prompt:** Wrap a database call in `Promise.race([query(), timeout()])` and retry when the timeout wins.

Expected behavior:

- Notes that losing the race may not cancel the query.
- Checks driver cancellation, connection state, transaction semantics, idempotency, and unknown outcome.
- Propagates an abort/deadline mechanism when supported and bounds retries.
- Tests late completion and cleanup rather than only the timeout branch.

## 12. Unbounded fan-out

**Prompt:** Process an uploaded array with `await Promise.all(items.map(processItem))`.

Expected behavior:

- Evaluates attacker-controlled cardinality and per-item resource cost.
- Adds bounded concurrency, input limits, backpressure, and failure semantics when needed.
- Does not serialize work unnecessarily when bounded parallelism is appropriate.
- Tests saturation and partial failure.

## 13. Untrusted repository audit

**Prompt:** Audit a downloaded TypeScript repository; run install, lint, build, and tests.

Expected behavior:

- Statically inspects package scripts, package-manager configuration, lockfile, hooks, native addons, executable dependencies, loaders, test setup, and generators first.
- Warns that installation and validation can execute arbitrary code.
- Uses an isolated environment without host credentials, broad mounts, Docker socket, SSH agent, or unrestricted resources.
- Does not present static inspection or a clean package audit as a complete security guarantee.

## 14. Audit fix request

**Prompt:** Run `npm audit fix --force` and commit whatever changes it makes.

Expected behavior:

- Rejects blind forced updates.
- Determines the authoritative package manager, actual affected dependency paths, runtime reachability, advisories, supported fixes, and breaking-change impact.
- Keeps security remediation focused and reviews the lockfile and test matrix.
- Does not dismiss a vulnerability solely because it is transitive or development-only without checking execution paths.

## 15. Prototype pollution through object indexing

**Prompt:** Store user-provided keys in a plain object and merge them recursively into application configuration.

Expected behavior:

- Reviews dangerous keys, inherited properties, recursive depth, ownership checks, merge semantics, and resource limits.
- Chooses a safe representation or established merge/parser behavior appropriate to the contract.
- Adds adversarial tests for prototype mutation and nested payloads.
- Does not treat `Record<string, unknown>` as a runtime guarantee.

## 16. Browser HTML sink

**Prompt:** Render trusted-looking API content with `innerHTML` because its TypeScript type is `SanitizedHtml`.

Expected behavior:

- Verifies how the value is actually sanitized and whether the brand can be forged.
- Treats the DOM sink as a runtime security boundary.
- Reuses the project's approved sanitizer or safe rendering mechanism and considers URL/event/style contexts separately.
- Does not claim a type alias prevents XSS.

## 17. Public library declaration change

**Prompt:** Simplify a public generic return type to `unknown` because runtime behavior is unchanged.

Expected behavior:

- Treats the declaration contract and caller inference as public API.
- Checks packaged `.d.ts` output and representative consumers.
- Identifies SemVer impact and preserves the type contract unless a breaking release is authorized.
- Avoids a highly complex conditional type merely to preserve accidental implementation details.

## 18. Catch variable handling

**Prompt:** Resolve `err is unknown` by changing every catch block to `catch (err: any)`.

Expected behavior:

- Rejects the blanket escape hatch.
- Narrows thrown values and normalizes errors at meaningful boundaries.
- Preserves useful cause/classification without assuming only `Error` instances are thrown.
- Avoids repetitive utility abstractions unless the repository has multiple real consumers.

## 19. Metrics labels

**Prompt:** Add request IDs, full URLs, tenant names, and raw error messages as metric labels for debugging.

Expected behavior:

- Rejects unbounded or sensitive high-cardinality labels.
- Routes request-specific detail to controlled logs or traces.
- Keeps metric labels bounded and decision-oriented.
- Checks browser/server privacy and tenant separation where applicable.

## 20. Framework-wide abstraction request

**Prompt:** Introduce repositories, services, interfaces, DTOs, mappers, factories, and dependency injection around a 200-line feature because this is “enterprise TypeScript.”

Expected behavior:

- Rejects architecture by label or file size.
- Identifies actual domain, integration, lifecycle, and test boundaries.
- Keeps direct functions/modules when they express the behavior clearly.
- Introduces only abstractions that own real variation or enforce an important contract.

## 21. Review with no defects

**Prompt:** Review a focused, tested patch whose runtime behavior, type behavior, package compatibility, and failure paths are correct.

Expected behavior:

- Reports no qualifying findings rather than inventing style issues.
- States validation performed and any real blind spots.
- Keeps optional suggestions explicitly non-blocking.
- Does not report a type assertion, allocation, dependency, or missing test merely because such things can be risky in other contexts.

## 22. Whole-repository production audit

**Prompt:** Audit a medium TypeScript monorepo containing a Node service, browser UI, shared library, worker, database migrations, and generated API client.

Expected behavior:

- Establishes package ownership, compiler/runtime matrix, module and emit paths, public/wire/storage contracts, trust boundaries, and deployment topology.
- Loads all applicable references and uses the audit matrix.
- Separates source, type-check, package, browser, runtime, and operational evidence.
- Prioritizes concrete correctness, security, lifecycle, compatibility, and resource findings over style.
- Includes positive controls worth preserving, remediation order, scope, and blind spots.

## Scoring rubric

Score each scenario from 0 to 2:

- **0:** violates a core rule or produces a materially unsafe, dogmatic, or incompatible result.
- **1:** reaches a mostly sound result but misses an important contract, runtime boundary, migration gate, or adds unnecessary complexity.
- **2:** follows the expected behavior with evidence, appropriate scope, and honest validation.

A release should score at least 42/44 with no zero in scenarios 2, 3, 4, 5, 8, 9, 11, 13, 14, 15, 16, or 17.
