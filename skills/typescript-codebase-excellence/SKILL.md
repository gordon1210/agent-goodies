---
name: typescript-codebase-excellence
description: >-
  Use this skill when designing, implementing, reviewing, refactoring,
  debugging, testing, securing, optimizing, packaging, or operating a
  small-to-medium TypeScript codebase: application, service, CLI, library,
  monorepo, browser UI, worker, serverless function, build tool, or mixed
  JavaScript/TypeScript project. Apply production-grade TypeScript engineering
  without speculative abstractions, type-system theater, blanket rewrites, or
  unnecessary dependencies. Preserve the repository's compiler generation,
  runtime, package manager, module system, public API, emitted artifacts,
  platform matrix, and established architecture unless the task explicitly
  changes them.
license: MIT
metadata:
  version: "1.0.0"
  last-reviewed: "2026-09-03"
  compatibility: >-
    TypeScript 6 and TypeScript 7. Honor the repository's pinned compiler,
    runtime, package manager, tsconfig hierarchy, module and resolution mode,
    declaration strategy, supported platforms, framework, and CI commands.
    Treat TypeScript 7 compiler-CLI adoption separately from compatibility with
    tools that import the TypeScript compiler API.
---

# TypeScript Codebase Excellence

Produce the smallest coherent change that is correct at runtime, sound at trust boundaries, maintainable, secure, testable, and appropriate for the repository. Optimize for long-term product quality—not for demonstrating advanced types, fashionable architecture, or a preferred toolchain.

## Rule hierarchy

Apply guidance in this order:

1. Explicit user requirements and repository-local instructions.
2. Security, runtime correctness, data integrity, and externally observable behavior.
3. Public API, wire/storage format, package, runtime, module, platform, and compiler compatibility.
4. Existing repository architecture, framework, tooling, and conventions.
5. Simplicity, readability, testability, and operational clarity.
6. Measured performance and resource constraints.
7. Stylistic preferences not enforced by the project.

When rules conflict, follow the higher-ranked rule and state the trade-off. Never silently change a contract. Type-checking success is evidence, not proof of runtime correctness.

## Required workflow

### 1. Establish the repository contract

Before editing, inspect the relevant subset of:

- Repository instructions and the task's acceptance criteria.
- Root and affected `package.json` files, the `packageManager` field, workspace configuration, package-manager config, and the authoritative lockfile.
- All applicable `tsconfig*.json` files, `extends` chains, project references, generated configs, and the actual compiler selected by scripts and CI.
- Formatting, linting, testing, build, bundling, code-generation, packaging, release, and deployment configuration.
- CI workflows, container/devcontainer files, runtime version files, browser targets, and platform matrices.
- Adjacent implementation, callers, tests, public exports, declaration output, configuration, schemas, database migrations, protocols, and generated artifacts affected by the change.

Determine:

- Application, service, CLI, library, browser UI, SSR application, worker, serverless function, build tool, plugin, Electron application, or mixed JavaScript/TypeScript context.
- Monorepo/workspace boundaries and which package owns the behavior.
- TypeScript 6 versus TypeScript 7, exact installed version, and whether editor, CI, build, and package scripts use the same compiler.
- Whether any tool imports `typescript`, uses the compiler API, custom transformers, language-service plugins, AST positions, declaration internals, or version-sensitive parser behavior.
- Runtime and minimum versions: Node.js, Bun, Deno, browser, Web Worker, service worker, edge runtime, embedded host, or a combination.
- ESM, CommonJS, or dual-package contract; package `type`, file extensions, `exports`/`imports`, module resolution, and who owns JavaScript emit.
- Whether `tsc` emits JavaScript, declarations only, or performs type-checking while a bundler, transpiler, runtime, or framework owns emit.
- Public API, declaration, package export, CLI, configuration, environment, wire, storage, schema, and generated-code contracts.
- Whether untrusted input, secrets, authorization, persistence, concurrency, native addons, subprocesses, filesystem access, or browser DOM sinks are involved.

Do not run package-manager installation, lifecycle scripts, builds, tests, generators, or repository binaries in an untrusted repository until manifests, scripts, configuration hooks, native addons, and executable dependencies have been reviewed and execution is isolated appropriately. TypeScript projects can execute arbitrary code during install, build, test, lint, and generation.

### 2. Load only relevant references

Read each selected file before deciding on the implementation. For repository-wide audits, read the review playbook and every applicable domain reference. Load the source index only when guidance must be verified or maintained.

| Trigger | Reference |
|---|---|
| Workspaces, package boundaries, public exports, declarations, SemVer, publishing | [architecture-packages-api.md](references/architecture-packages-api.md) |
| Type modeling, narrowing, assertions, generics, errors, invariants | [types-modeling-errors.md](references/types-modeling-errors.md) |
| ESM/CommonJS, resolution, Node/Bun/Deno/browser/worker behavior, environment types | [runtime-modules-platforms.md](references/runtime-modules-platforms.md) |
| Bundlers, transpilers, frameworks, decorators, code generation, source maps | [build-generated-code-frameworks.md](references/build-generated-code-frameworks.md) |
| Promises, cancellation, streams, workers, queues, lifecycle, shutdown | [async-concurrency-lifecycle.md](references/async-concurrency-lifecycle.md) |
| Unit/integration/type/browser/E2E tests, linting, CI, matrices, declarations | [testing-verification.md](references/testing-verification.md) |
| Untrusted input, auth, browser/server security, dependencies, install scripts, supply chain | [security-dependencies-supply-chain.md](references/security-dependencies-supply-chain.md) |
| Runtime latency, memory, event loop, bundles, compiler/build/type-level performance | [performance-resource-use.md](references/performance-resource-use.md) |
| Browser UI, SSR/hydration, accessibility, DOM safety, client state and lifecycle | [frontend-browser-ui.md](references/frontend-browser-ui.md) |
| JSON and other wire formats, schemas, databases, migrations, generated clients | [persistence-wire-contracts.md](references/persistence-wire-contracts.md) |
| API docs, comments, configuration, telemetry, services, CLIs, operations | [documentation-observability-operations.md](references/documentation-observability-operations.md) |
| Patch review, repository audit, migration review, finding severity and evidence | [review-playbooks.md](references/review-playbooks.md) |
| Concrete command baselines and optional ecosystem tools | [tooling-baseline.md](references/tooling-baseline.md) |
| TypeScript 6/7 coexistence, migration gates, defaults, deprecations, native compiler | [typescript-6-7-compatibility.md](references/typescript-6-7-compatibility.md) |
| Updating this skill or verifying disputed version/tool behavior | [sources.md](references/sources.md) |

### 3. Plan the change around contracts

Identify what must remain true and what must change. Trace runtime behavior, type-level behavior, emitted output, package consumers, failure paths, cleanup, compatibility, and test seams before coding.

Prefer:

- A focused implementation over a framework or repository-wide cleanup.
- Existing abstractions and libraries over parallel mechanisms.
- A module over a new package unless a durable package boundary exists.
- Concrete functions and objects over an interface, generic, class hierarchy, or dependency-injection layer with only one credible implementation.
- A discriminated union over boolean combinations or class hierarchies when the state set is closed.
- Runtime validation at external boundaries over assertions that merely silence the checker.
- Standard platform APIs over a dependency when the local implementation remains clear, portable, and safe.
- An established dependency over custom security-sensitive parsing, cryptography, sanitization, protocol, or concurrency code when the dependency is appropriately scoped and approved.

Do not mix unrelated modernization into the patch. Separate prerequisite refactors only when they materially reduce risk and remain behavior-preserving.

### 4. Implement defensively

#### Runtime boundaries and invariants

- Treat network data, JSON, database rows, environment variables, command-line input, local storage, postMessage payloads, filesystem content, and third-party SDK results as runtime values—not as trusted TypeScript types.
- Accept uncertain external data as `unknown` or an appropriately narrow primitive, validate it once, and convert it into a validated internal representation.
- Make absent, optional, nullable, empty, zero, and default states distinct when the domain distinguishes them.
- Preserve units, ranges, encoding, normalization, timezone, precision, identifier namespace, and ordering explicitly.
- Ensure transactions, temporary state, subscriptions, timers, listeners, streams, workers, child processes, sockets, and file handles are completed, cancelled, closed, or rolled back on every relevant path.
- Bound attacker-controlled sizes, nesting, concurrency, retries, buffering, retained history, and cache growth.

#### Types and narrowing

- Prefer inference where it is precise; add annotations at public boundaries, recursive definitions, overloads, exported values, complex inference points, and places where they document a contract.
- Prefer `unknown` over `any` for values that require inspection. Explicit `any` is an unchecked escape hatch and must represent a genuinely dynamic contract, not a shortcut around an error.
- Prefer control-flow narrowing, discriminated unions, `satisfies`, type predicates, assertion functions, validated constructors, and schema parsers over type assertions.
- Do not use `as T`, angle-bracket assertions, double assertions, or non-null assertions to convert missing evidence into certainty. When an interop boundary makes an assertion unavoidable, keep it narrow and adjacent to the evidence, state the invariant, and test it. Honor stricter repository policies that prohibit assertions entirely.
- Do not weaken `strict`, enable broad `skipLibCheck`, add `@ts-ignore`, or relax a safety-relevant compiler/lint rule merely to make a change compile.
- Use `@ts-expect-error` only for an intentional, tested error at the narrowest line, with a reason that explains the contract; remove it when the expected error disappears.
- Avoid type-level cleverness whose maintenance, diagnostics, declaration output, or compiler cost exceeds the defect class it prevents.

#### API and abstraction shape

- Keep exports minimal. A new export, package subpath, declaration, enum member, union member, overload, generic constraint, nominal brand, or error class can be a compatibility commitment.
- Model related states with a discriminated union when exhaustive handling has real value.
- Introduce branded or opaque values for validated identifiers, units, or otherwise confusable primitives only when they eliminate credible mistakes and can be constructed safely.
- Add an interface or generic abstraction for multiple implementations, a stable capability, a real integration boundary, or a proven test seam—not solely because “everything should be injectable.”
- Prefer plain functions and data for stateless behavior. Use classes when identity, lifecycle, polymorphism, encapsulated mutable state, or framework integration makes them the clearest model.
- Use overloads only when they materially improve caller behavior and every signature matches the implementation. Prefer unions when callers do not receive correlated return types.
- Keep generated and handwritten types distinct; do not hand-edit generated output.

#### Errors

- Remember that JavaScript may throw any value. Narrow caught values before reading properties.
- Preserve useful causes and classifications across layers. Add context at ownership boundaries and report once rather than logging the same failure repeatedly.
- Use exceptions for exceptional failure in codebases built around exceptions. Use explicit result unions when failure is an ordinary branch and the existing architecture benefits. Do not force either style repository-wide.
- Make retryability, cancellation, timeout, conflict, validation, authorization, and not-found outcomes distinguishable where callers act differently.
- Do not expose secrets, credentials, raw sensitive payloads, SQL, internal paths, stack traces, or unnecessary implementation details to users or telemetry.
- Never swallow a promise rejection or catch an error without a deliberate recovery, translation, cleanup, or reporting decision.

#### Modules and runtime behavior

- Align `module`, `moduleResolution`, package `type`, file extensions, `exports`, import specifiers, bundler behavior, and the actual runtime. A TypeScript path mapping alone does not make a runtime import resolvable.
- Use type-only imports/exports where required by the project's emit model, but do not churn imports solely for style.
- Do not change ESM/CommonJS mode, import extension policy, package conditions, target, libraries, JSX transform, decorators, or emit ownership incidentally.
- Ensure server-only code and secrets cannot enter client bundles. Keep browser, Node, worker, test, and framework-global types scoped to the projects that own them.
- Test the packaged or deployed artifact, not only source execution inside the workspace.

#### Async, concurrency, and lifecycle

- Every promise must be awaited, returned, deliberately aggregated, or deliberately detached under an owner that handles rejection and shutdown.
- Propagate cancellation through `AbortSignal` or the repository's established mechanism. A rejected waiter or timeout does not necessarily stop underlying work.
- Bound `Promise.all` fan-out, queues, worker creation, stream buffering, retries, and concurrent external calls.
- Do not block the event loop with large synchronous parsing, compression, hashing, rendering, filesystem work, or CPU loops on latency-sensitive paths.
- Define ownership and termination for timers, event listeners, subscriptions, workers, child processes, sockets, and background jobs.
- Preserve ordering, idempotency, atomicity, and partial-failure behavior across asynchronous steps.

### 5. Validate using the repository's real matrix

Use repository-provided scripts and CI commands first. Use the authoritative package manager and lockfile. Do not install tools, update dependencies, regenerate broad outputs, or change compiler/runtime versions without approval.

At minimum, when applicable and supported by the repository:

1. Formatting check.
2. Type-check for the affected project and its dependents.
3. Lint with the repository's configured type-aware scope.
4. Focused regression tests for changed behavior.
5. Broader package/workspace tests.
6. Production build, declaration emit, or package build.
7. Consumer/package-export validation for libraries.
8. Supported runtime, browser, platform, module, and compiler-generation matrices.
9. Security, schema/migration, E2E, performance, bundle-size, or compatibility checks when the changed contract requires them.

For TypeScript 6/7 support, validate the actual promised matrix. Do not claim support for both merely because source type-checks once. Compiler CLI, declarations, editor/language service, lint parser, build plugins, and compiler-API consumers may have different compatibility.

Do not claim a command passed unless it was executed successfully. If a check cannot run, state the exact reason and what remains unverified.

### 6. Review the final diff

Before completing:

- Re-read changed code without relying on intent.
- Trace success, invalid input, thrown non-`Error` values, rejection, cancellation, timeout, partial progress, cleanup, retry, and shutdown paths as applicable.
- Check public API, declaration, package export, module, runtime, browser, configuration, wire/storage, schema, generated-code, and operational compatibility.
- Inspect lockfile, package metadata, generated files, snapshots, source maps, and built artifacts for unintended changes.
- Remove dead code, stale comments, debugging output, broad suppressions, accidental `any`, unjustified assertions, non-null assertions, duplicate validation, floating promises, unbounded work, and unrelated edits introduced by the patch.
- Confirm tests prove the missing or broken behavior and would fail against the old implementation when practical.
- Confirm the solution is no more abstract than the problem requires.

## Lint and suppression policy

- Fix warnings in owned code instead of silencing them.
- Keep suppressions at the narrowest possible scope and explain why the rule does not apply to the current invariant.
- Prefer a repository-supported `@ts-expect-error` with a precise reason over `@ts-ignore` for intentional compile-time negative cases.
- Do not disable strictness, type-aware linting, promise rules, unsafe-access rules, import rules, or security rules project-wide to accommodate one site.
- Do not enable every strict, stylistic, or experimental lint as an error without curating it for the codebase and compiler/runtime matrix.
- Let the configured formatter decide formatting. Do not spend review effort on formatter-owned details.

## Testing policy

- Test externally meaningful behavior, invariants, package contracts, and failure modes—not line-by-line implementation details.
- Use runtime tests for runtime behavior and type tests for type-level contracts. Neither replaces the other.
- Cover success, boundary, malformed input, dependency failure, rejection, cancellation, timeout, retry, cleanup, and regression paths relevant to the change.
- Keep tests deterministic, isolated, parallel-safe, and bounded. Avoid wall-clock sleeps, shared process-global mutation, ambient network access, fixed ports, and order dependence.
- Prefer fake clocks, seeded randomness, temporary isolated resources, and explicit integration seams where needed.
- Use snapshots for complex stable output only when diffs are reviewed and critical semantics remain explicit.
- Treat coverage as a diagnostic, not a quality target. High coverage does not prove boundary safety, type soundness, race freedom, or useful assertions.

## Dependency policy

- Add no dependency merely to save a few clear lines or avoid learning an existing platform API.
- Add no custom cryptography, sanitizer, parser, authentication protocol, archive extractor, concurrency primitive, or security-sensitive codec merely to reduce dependency count.
- Inspect package source, ownership, maintenance, releases, license, exports, types, supported runtimes, engine constraints, default behavior, transitive graph, native code, install/lifecycle scripts, postinstall downloads, and security history before adding a dependency.
- Prefer the repository's existing dependency when it already solves the need safely.
- Preserve package-manager and lockfile policy. Dependency updates must be intentional and separately reviewable when practical.
- Never run automated audit fixes blindly; review resolved versions, breaking changes, reachability, and lockfile effects.

## Prohibited default actions

Unless explicitly required, do not:

- Upgrade TypeScript, the runtime, package manager, framework, bundler, test runner, linter, module system, JSX transform, decorators mode, or workspace orchestrator.
- Migrate TypeScript 6 to 7 or replace the JavaScript compiler with the native compiler as incidental cleanup.
- Change ESM/CommonJS mode, package `type`, export conditions, import extensions, target, libs, declaration layout, or emit ownership.
- Turn off `strict`, enable blanket `skipLibCheck`, add `@ts-ignore`, introduce `any`, or add assertions/non-null assertions merely to suppress errors.
- Add a validation library, state library, dependency-injection framework, ORM, schema generator, or monorepo tool when the repository already has an adequate mechanism.
- Split a package, create a shared `utils` package, add an interface, generic abstraction, base class, factory, repository layer, or plugin system for hypothetical reuse.
- Change public API, serialized data, database schema, environment/config keys, CLI output, exit codes, telemetry fields, or client bundle contents silently.
- Update unrelated dependencies, reformat unrelated files, rewrite generated output by hand, or accept broad snapshot changes without review.
- Optimize runtime, bundle, or compiler performance without a stated bottleneck, representative evidence, or explicit resource budget.

## Completion report

Report:

1. What changed and why.
2. Contracts intentionally preserved or intentionally changed.
3. Exact tests and validation commands actually executed.
4. Any remaining risk, uncertainty, platform/compiler gap, integration gap, or unverified assumption.

For code reviews, use the severity and evidence rules in [review-playbooks.md](references/review-playbooks.md). Report no finding without a concrete trigger and observable impact or maintainability cost.
