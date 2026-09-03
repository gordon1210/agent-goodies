# Review and Audit Playbooks

Read this reference when reviewing a patch, auditing a repository, assessing a migration, or reporting findings. The goal is evidence-based risk reduction, not stylistic churn or architecture performance.

## 1. Review principles

- Review the requested scope first; do not bury the answer under unrelated repository issues.
- Establish compiler, runtime, module, build, package, browser, and support contracts before judging a design.
- Distinguish TypeScript checker evidence from JavaScript runtime behavior.
- Prefer concrete failure modes and maintainability costs over generic best-practice claims.
- Distinguish correctness/security defects from optional improvements.
- Do not demand a rewrite when a focused fix removes the risk.
- Do not assume code is unused, unreachable, private, server-only, client-only, generated, or unsupported without evidence.
- Treat generated, vendored, migration, fixture, declaration, compatibility, and build code according to its role.
- Confirm version-sensitive TypeScript/runtime/tool behavior from primary documentation when uncertain.
- Attempt to disprove each suspected finding before filing it.

## 2. Review modes

### Patch review

Focus on changed behavior and risks introduced or exposed by the diff.

Inspect:

- Task/issue and acceptance criteria.
- Complete diff, including package metadata, lockfiles, configs, generated files, declarations, snapshots, and migrations.
- Callers, consumers, tests, schemas, exports, and artifacts adjacent to changed code.
- Runtime input, errors, rejection, cancellation, cleanup, retry, concurrency, and compatibility paths.
- Whether source, build, package, and deployment behavior differ.

Do not turn a patch review into a general repository audit unless a pre-existing issue directly makes the patch unsafe or impossible to validate.

### Repository audit

Establish scope explicitly: packages, tsconfigs, compiler generations, runtimes, module systems, browsers, deployment artifacts, trust boundaries, environments, and time/evidence limits.

Audit in passes:

1. Architecture, package/workspace metadata, tsconfig hierarchy, and support policy.
2. Public exports, declarations, wire/storage/configuration contracts.
3. Runtime correctness, validation, type modeling, and error handling.
4. Modules, build pipeline, generated code, and artifact behavior.
5. Async, lifecycle, concurrency, streams, and resource bounds.
6. Security, authorization, browser/server boundaries, dependencies, and executable supply chain.
7. Tests, lint, CI, runtime/browser/compiler matrix, and package verification.
8. Performance and operational behavior where relevant.
9. Documentation, migrations, and maintenance risks.

An audit cannot prove absence of defects. State coverage and blind spots precisely.

### Design review

Review before implementation:

- Requirements and non-requirements.
- Product/package/runtime boundaries.
- Trust, state, ownership, and failure boundaries.
- Public, persisted, generated, and deployment contracts.
- Async, cancellation, idempotency, ordering, recovery, and resource limits.
- Type model versus runtime validation.
- Alternatives and why each layer/dependency/abstraction is justified.
- Validation, rollout, compatibility, migration, and rollback strategy.

Reject abstractions that solve only hypothetical future requirements.

### Migration review

For TypeScript, runtime, module system, package manager, framework, bundler, linter, test runner, database, schema, or dependency migrations:

- Separate mechanical changes from semantic changes.
- Define old/new compatibility window and support matrix.
- Identify all tools that parse/import/transform TypeScript.
- Compare diagnostics, declarations, runtime artifacts, generated output, and consumers.
- Identify irreversible data/package/deployment steps and rollback limits.
- Validate mixed-version deployments where applicable.
- Review full lockfile and transitive dependency changes.
- Require targeted regression tests for changed semantics.

A green build after a migration is not sufficient evidence.

### Security review

Start with a threat model:

- Assets and trust boundaries.
- Attacker-controlled data and cost.
- Authentication/authorization/tenant scope.
- Browser/server/privileged boundaries.
- Process/filesystem/network/database/native/package execution.
- Partial failure, retries, races, and logging.

Prioritize reachable, high-impact paths. Scanners inform review but do not replace it.

## 3. Severity model

Use the repository's established severity model when one exists. Otherwise use:

### Critical

A credible path to catastrophic impact, such as remote code execution, broad key/sensitive-data compromise, systemic data loss/corruption, arbitrary privileged process or build execution, or complete security-boundary bypass.

### High

A likely or material correctness, security, availability, privacy, or compatibility failure with broad impact, difficult recovery, or no practical mitigation. Examples: cross-tenant access, persistent corruption, exploitable unbounded resource consumption, lost acknowledged jobs, server secrets bundled to clients, or a breaking package/API migration presented as compatible.

### Medium

A real defect with bounded impact, conditional trigger, recoverable failure, or meaningful maintenance/operational risk. Examples: stale UI overwrite, task/listener leak under a specific path, retry amplification, incorrect edge-case validation, unsupported module/compiler combination claimed by CI, or declaration break for a subset of consumers.

### Low

A concrete but small reliability, diagnostics, accessibility, compatibility, or maintainability issue unlikely to cause serious immediate impact. It still needs a plausible trigger and consequence.

### Suggestion

A non-defect improvement, simplification, naming change, optional hardening, or future work. Do not present suggestions as required fixes.

Severity reflects impact and likelihood in the actual system, not line count, rule category, or theoretical worst case.

## 4. Confidence

State confidence when evidence is incomplete:

- **High:** directly demonstrated by code, tests, specification, artifact, or reproducible behavior.
- **Medium:** strongly implied but depends on an unverified caller, deployment, runtime, browser, package, or configuration detail.
- **Low:** plausible hypothesis requiring targeted confirmation; normally ask for evidence or omit it from blocking findings.

Do not inflate severity to compensate for low confidence. Do not lower a demonstrated high-impact issue merely because reproduction is inconvenient.

## 5. Finding quality bar

A finding must contain:

1. **Title:** concrete failure, not a rule name.
2. **Location:** smallest useful file and line range.
3. **Trigger:** input, state, timing, runtime, module, compiler, feature, platform, or call sequence.
4. **Impact:** observable consequence.
5. **Evidence:** code path, type/runtime mismatch, declaration/artifact, contract, test, documentation, or reproduction.
6. **Remediation:** smallest sound direction without prescribing an unnecessary rewrite.
7. **Severity and confidence.**

Example:

```markdown
### High — Timed-out writes continue and are retried with an unknown outcome

`src/orders/save-order.ts:72-103`

`Promise.race()` rejects after five seconds, but the database operation receives no cancellation signal and may still commit. The catch path immediately retries with a new transaction. Under a slow connection, both writes can complete, creating duplicate orders despite the UI seeing one timeout.

Propagate the driver's cancellation/deadline mechanism and add an idempotency key or uniqueness invariant before retrying. Add a test where the first write completes after the local timeout.

Confidence: high.
```

Do not report:

- A lint/style preference with no failure or maintenance cost.
- `any`, an assertion, non-null assertion, dependency, class, interface, or generic merely because it exists; show how it invalidates a contract.
- A hypothetical race without an interleaving and shared/external state.
- An allocation/bundle/type complexity without evidence it matters.
- A missing test as a standalone defect when no important unverified behavior is identified.
- A public API break without confirming the export/declaration/package support contract.
- A runtime validation issue when a trustworthy validator already dominates every reachable path.
- A promise as floating when the host/framework intentionally owns and observes it.
- A browser issue in code proven server-only by the production build boundary.

## 6. Patch review procedure

### Step 1: Restate the behavioral delta

Identify:

- What changes for callers, users, operators, package consumers, or generated artifacts.
- What must remain compatible.
- New inputs, states, errors, exports, dependencies, scripts, tasks, schemas, or persisted data.
- Which checks should establish correctness.

### Step 2: Trace runtime paths

Trace at least applicable paths:

- Normal success.
- Missing/null/empty/boundary/malformed input.
- Dependency failure and thrown non-`Error` values.
- Partial progress and cleanup.
- Promise rejection, timeout, cancellation, and late completion.
- Concurrent access, duplicate delivery, stale UI response, and shutdown.
- Authorization/tenant scope.
- Browser/server/worker/privileged transitions.

### Step 3: Trace static/build/package paths

Check:

- Public signatures, inference, overloads, and declarations.
- Type assertions/guards/validators and whether evidence matches claims.
- tsconfig selection and included files.
- ESM/CommonJS, imports, path aliases, package exports, and runtime loader.
- Bundler/framework/codegen output.
- TypeScript 6/7 and parser/compiler-API compatibility.
- Packaged/deployed artifact behavior.

### Step 4: Inspect durable contracts

Check:

- Wire/storage/schema/configuration/CLI behavior.
- Error codes/classes/status and retry semantics.
- Runtime/browser/platform support.
- Database migrations and mixed deployments.
- Security/privacy/logging/telemetry.
- Resource limits and operational lifecycle.

### Step 5: Inspect tests

Determine whether tests:

- Fail against the old defect or absent behavior.
- Exercise meaningful behavior rather than implementation trivia.
- Use runtime tests and type tests for their respective contracts.
- Remain deterministic, isolated, and bounded.
- Cover negative/cleanup/cancellation/authorization behavior proportionate to risk.
- Execute in the CI compiler/runtime/browser/package matrix.
- Exercise production or packed artifacts when source execution is insufficient.

### Step 6: Validate selectively

Use repository commands first. Start with focused checks, then expand according to risk. Never claim unexecuted validation.

### Step 7: Re-read the final diff

Look for accidental:

- Lockfile/dependency updates.
- Generated/snapshot churn.
- Broad formatting.
- New exports or declaration changes.
- `any`, assertions, non-null assertions, suppression directives, or weakened config.
- Floating promises, listeners/timers, unbounded fan-out, or leaked resources.
- Debug logs, secrets, raw payloads, source maps, or client bundle changes.
- Stale comments and unrelated cleanup.

## 7. Repository audit matrix

Use applicable rows and record evidence:

| Area | Questions |
|---|---|
| Architecture | Are module/package boundaries coherent? Is dependency direction acyclic? |
| Workspace | Is package-manager/lockfile/task ownership explicit and reproducible? |
| TypeScript config | Are compiler generation, strictness, project refs, roots, ambient types, and emit roles correct? |
| Runtime/modules | Do module settings, imports, exports, loaders, and platform behavior agree? |
| Build | Are checker, emitter, bundler, framework, generator, cache, and artifact responsibilities clear? |
| Public API | Are exports/declarations/minimum versions stable, documented, and consumer-tested? |
| Types | Do types model validated runtime possibilities without unjustified escape hatches? |
| Input | Are structure, semantics, size, depth, encoding, prototype, path, URL, and cost validated? |
| Errors | Are thrown/rejected/result errors classified, causal, safe, and owned? |
| Async | Are promises, cancellation, deadlines, late completion, and detached work owned? |
| Concurrency | Are fan-out, queues, workers, shared state, retries, and backpressure bounded? |
| Security | Are auth, authorization, tenancy, browser sinks, secrets, process/network/filesystem boundaries sound? |
| Dependencies | Are lifecycle scripts, native code, build tools, source, licenses, advisories, and lockfile reviewed? |
| Persistence | Are schemas, transactions, migrations, compatibility, backup, and recovery defined? |
| Frontend | Are state, effects, SSR/hydration, accessibility, DOM safety, storage, and stale async behavior correct? |
| Tests | Do runtime, type, integration, browser, package, and failure tests protect critical behavior? |
| CI | Does CI cover promised compiler/runtime/module/browser/artifact matrices? |
| Performance | Are hot paths measured and runtime/build resource growth bounded? |
| Operations | Are configuration, telemetry, health, retries, lifecycle, deployment, and runbooks coherent? |
| Documentation | Can users, consumers, and maintainers safely operate and evolve the system? |

## 8. Common high-value TypeScript checks

### Runtime validation and types

- Assertion or generic used instead of validating JSON, database, message, storage, or SDK data.
- Guard/predicate that checks fewer properties than its type promise.
- `any` contamination escaping a boundary.
- Non-null assertion reachable under ordinary runtime state or race.
- Optional/undefined/null mismatch across config, schema, API, and persistence.
- Exhaustive switch over an unvalidated external discriminant.
- Unsafe record indexing or prototype-sensitive merge.

### Modules and packaging

- `paths` alias accepted by TypeScript but unresolved in runtime/artifact.
- Incorrect file extensions/package `type` under Node ESM.
- Type declaration condition mismatched with runtime export.
- Dual package evaluated twice or exposing different API shapes.
- Server-only code/secrets imported into client bundle.
- Workspace source imports bypassing package exports and hiding publish failure.
- Cyclic top-level initialization.

### TypeScript 6/7

- TypeScript 7 CLI upgrade despite tools importing the TypeScript 6 compiler API.
- Deprecated TypeScript 6 options hidden through suppression instead of migrated.
- TypeScript 6 default changes altering strictness, target, root, ambient types, or side-effect imports unexpectedly.
- TypeScript 7 JavaScript/JSDoc/declaration differences ignored in mixed projects.
- Parallel checker/builder settings causing memory/process explosion.
- Claim of dual-version support without declaration/tool/consumer matrix.

### Async and lifecycle

- Floating promise or async event handler with lost rejection.
- `Promise.race` timeout without cancelling/observing losing work.
- Unbounded `Promise.all` or queue.
- Retry after unknown non-idempotent outcome.
- Listener/timer/subscription/stream/worker leak.
- Older UI request overwriting newer state.
- Shutdown dropping accepted work or waiting forever.

### Security

- Authorization checked only in UI or route wrapper, not at resource operation.
- Tenant scope omitted from query/update/cache key.
- Raw HTML/URL/message sink trusted through a type brand alone.
- User input concatenated into shell, SQL, path, or URL.
- SSRF controls that validate only hostname text before redirects/DNS/connect.
- Secrets/raw payloads in logs, metrics labels, source maps, hydration, or browser storage.
- Lifecycle/postinstall/native/compiler plugin added without executable supply-chain review.
- Blind forced dependency audit update.

### Persistence and operations

- JSON number precision/date/bigint/undefined mismatch.
- Queue acknowledgement before durable commit.
- Migration incompatible with rolling deployment or unsafe on production volume.
- Cache key/version/tenant collision.
- High-cardinality metrics or duplicate error logging.
- Health check causing restart storms.
- Build-time config embedded into the wrong environment.

## 9. False-positive controls

Before filing a finding:

- Search for validation/authorization earlier in the actual call path.
- Check whether a validated constructor/brand is inaccessible externally.
- Check tsconfig/project/include and build graph.
- Check package exports, bundler conditions, and server/client directives in the production build.
- Check framework/host ownership of promises, lifecycle, escaping, and cleanup.
- Check whether code is generated, test-only, fixture-only, migration-only, or intentionally process-fatal.
- Check runtime/compiler/browser versions and repository support claims.
- Check tests and documentation that define intended behavior.
- Check whether a wrapper owns retries, cancellation, error reporting, or resource cleanup.
- Reproduce with the packed/deployed artifact when source assumptions are uncertain.

If a conclusion depends on missing deployment/context, state the dependency and confidence instead of presenting certainty.

## 10. Review output format

For a code review:

1. Findings ordered by severity, then impact.
2. Open questions/assumptions only when they affect correctness.
3. Brief validation summary.
4. Optional non-blocking suggestions clearly separated.

If no qualifying findings exist, say so directly and list meaningful validation gaps. Do not invent a finding to make the review appear useful.

For an audit:

1. Executive assessment and scope.
2. Findings by severity.
3. Coverage matrix and methods.
4. Positive controls worth preserving.
5. Prioritized remediation sequence.
6. Residual risks and unverified areas.

## 11. Remediation prioritization

Prioritize risk reduction per unit of change:

1. Contain active security, corruption, privacy, or availability risk.
2. Add a regression test/invariant that demonstrates the failure where practical.
3. Apply the smallest correct fix.
4. Add broader hardening only where the same root cause exists.
5. Refactor only when necessary to make correctness understandable and maintainable.
6. Plan compatibility/migration work separately when immediate containment can preserve contracts.

Do not combine large architecture/toolchain modernization with an urgent fix unless the current structure prevents a safe focused change.

## 12. Completion gate

A review is complete when:

- Requested scope and support matrix are clear.
- Changed and high-risk runtime/static/artifact paths were traced.
- Findings meet the trigger/evidence/impact bar and duplicates are consolidated.
- Severity reflects actual likelihood and impact.
- Suggested fixes preserve higher-priority contracts and avoid needless architecture.
- Executed validation and remaining blind spots are stated accurately.
