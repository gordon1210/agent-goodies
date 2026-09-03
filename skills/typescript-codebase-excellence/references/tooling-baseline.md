# Tooling and Validation Baseline

Read this reference when selecting package-manager commands, TypeScript checks, lint/test/build/package workflows, CI stages, diagnostics, or optional ecosystem tools. Repository-local scripts and support policy take precedence.

Do not install packages, run lifecycle scripts, load executable config, build, test, lint, generate, package, or execute repository code from an untrusted project without review and appropriate isolation.

## 1. Command selection principles

- Use repository scripts, task runner, and CI commands first.
- Use the authoritative package manager and lockfile.
- Run the narrowest useful check early, then expand to affected dependents and the promised matrix.
- Keep formatting, type-check, lint, runtime tests, type tests, build, declarations, package, browser, security, and compatibility checks conceptually separate.
- Do not invent a script name and claim it is standard; inspect `package.json` and orchestration config.
- Do not silently install missing tools or use a command that downloads packages implicitly.
- Do not update lockfiles, snapshots, generated code, or dependencies unless the task requires it.
- Record exact commands and versions actually executed.

## 2. Determine package manager and versions

Inspect, in order:

- `package.json` `packageManager` field.
- Authoritative lockfile.
- Corepack/package-manager configuration.
- CI and developer instructions.
- Workspace/task-runner configuration.

Common lockfiles include:

- npm: `package-lock.json`.
- pnpm: `pnpm-lock.yaml`.
- Yarn: `yarn.lock` plus Yarn configuration/version metadata.
- Bun: Bun's current lockfile format as selected by the repository.

Do not generate another manager's lockfile. If signals conflict, follow repository instructions or resolve the conflict before mutation.

Record:

```text
package manager + version
runtime + version
TypeScript compiler + version
affected workspace/package/project
module/build mode
```

Use the repository's version manager, Corepack, container, or pinned tooling rather than a random global installation.

## 3. Installation baselines

Use only after trust review. Typical immutable/frozen forms are:

```bash
npm ci
pnpm install --frozen-lockfile
yarn install --immutable
bun install --frozen-lockfile
```

These are templates, not universal commands:

- Workspace/offline/config flags may differ.
- Lockfile/version compatibility matters.
- Installation can execute lifecycle scripts and native builds.
- Disabling scripts can be useful for initial inspection but may not produce a runnable project.
- Registry/auth configuration and patches/overrides can affect resolution.

Never run a broad update command as part of installation unless dependency changes are explicitly requested.

## 4. Discover repository commands

Inspect root and affected package scripts plus CI/task-runner definitions.

Typical script purposes—not guaranteed names—include:

- `format` / `format:check`.
- `typecheck` / `check`.
- `lint`.
- `test`, focused/unit/integration/type/E2E variants.
- `build`.
- `generate` / `codegen`.
- `pack` / `release`.
- `audit` / `validate`.

Run scripts through the chosen package manager, for example:

```bash
npm run <script> -- <args>
pnpm run <script> -- <args>
yarn <script> <args>
bun run <script> -- <args>
```

Argument forwarding differs by manager/script; follow repository examples. Avoid ad-hoc global binaries that can select a different version.

## 5. TypeScript compiler discovery

Do not assume `tsc` on `PATH` is the repository compiler.

Use a repository script or local package binary through the authoritative manager. Confirm version explicitly:

```bash
<package-manager-local-exec> tsc --version
```

Then identify:

- `typescript` package version and lockfile resolution.
- Any TypeScript compatibility aliases.
- Which `tsconfig` script/CI/editor selects.
- Whether a framework/bundler invokes another compiler/parser.
- Whether tools import `typescript` as an API.

For TypeScript 7 coexistence with TypeScript 6, read [typescript-6-7-compatibility.md](typescript-6-7-compatibility.md) before choosing binaries.

## 6. Type-check baselines

Use repository scripts first. Direct compiler shapes, adapted to the project, include:

```bash
tsc -p tsconfig.json --noEmit
tsc -b
tsc -b path/to/tsconfig.json
```

Caveats:

- `--noEmit` is appropriate only when another tool owns all required emit and declaration behavior.
- `tsc -b` follows project references and can emit/update build information.
- A root `tsc -p` may not check all workspace packages or referenced projects as CI intends.
- Framework virtual files/generated types may require generation or framework-specific checks.
- Tests/build tools may have separate configs.

Run focused project checks first, then affected dependents and the supported matrix.

## 7. Effective configuration and file scope

Useful compiler diagnostics include:

```bash
tsc -p path/to/tsconfig.json --showConfig
tsc -p path/to/tsconfig.json --listFilesOnly
tsc -p path/to/tsconfig.json --traceResolution
```

Use them to answer:

- Which options win through `extends`.
- Which files and ambient types are included.
- Why a module resolves to a particular file/declaration.
- Whether output/generated/test directories enter the project.
- Whether package conditions and path mappings match intent.

`--traceResolution` can be large; target a representative project/import and retain only relevant evidence.

## 8. Build mode and cleanup

For project references:

```bash
tsc -b --verbose
tsc -b --clean
```

Use cleanup only when output ownership is known; never delete broad directories from an untrusted or ambiguous config.

Validate:

- Clean build.
- No-op incremental build.
- Leaf edit and shared-package edit.
- Distinct `tsBuildInfoFile`/output locations.
- Parallel CI/task-runner behavior.
- Stale declaration/generated output detection.

Do not depend on stale local artifacts to make a build pass.

## 9. Compiler performance diagnostics

When type-check/build performance is material, use repository-supported compiler diagnostics such as:

```bash
tsc -p tsconfig.json --extendedDiagnostics
tsc -p tsconfig.json --generateTrace .tmp/ts-trace
```

Treat exact flag availability/output as compiler-version-specific and verify before use.

Record:

- Clean versus incremental.
- Files/types/instantiations where reported.
- Parse/bind/check/emit time.
- Memory.
- Project/reference structure.
- TypeScript generation and parallel settings.

Do not commit traces containing source paths or sensitive names unless policy permits.

## 10. TypeScript 7 parallel controls

TypeScript 7 can parallelize checking and project builds. In TypeScript 7.0, the checker/builder tuning flags are experimental; relevant controls include checker workers, project builders, and single-threaded mode.

Rules:

- Preserve repository settings unless tuning is the task.
- Measure wall time and peak memory.
- Account for multiplication between concurrent project builders and checker workers.
- Use explicit lower concurrency or single-threaded mode for constrained CI or diagnosis when appropriate.
- Do not set worker counts from host CPU count alone.
- Keep commands/version-specific documentation in repository CI if flags are required.

See [typescript-6-7-compatibility.md](typescript-6-7-compatibility.md).

## 11. Formatting

Run the configured formatter/check script. Do not introduce another formatter or manually restyle formatter-owned code.

- Scope formatting to intended files when repository scripts permit.
- Avoid broad format churn in a focused patch.
- Keep generated/vendored code under its source-of-truth policy.
- Ensure editor and CI use compatible formatter versions/config.
- Treat import sorting as part of one configured tool; avoid competing formatter/linter/editor sorters.

## 12. ESLint and type-aware linting

Use the repository's ESLint version, flat/legacy config model, parser, plugins, and scripts.

For type-aware rules, verify:

- Parser/tool versions support the selected TypeScript generation.
- The intended tsconfig/project service includes each linted file.
- Generated/output/config/test files have deliberate scope.
- The linter does not create many redundant compiler programs unnecessarily.
- CI and editor use the same effective configuration.

Run the focused lint scope, then broader repository scope when required.

Do not:

- Add `--fix` over the whole repository without reviewing changes.
- Disable type-aware rules globally for one incompatible file.
- Turn every available strict/stylistic rule into an error at once.
- Use broad ignore patterns to hide owned code.
- Assume a lint parser accepting syntax means the compiler/build/runtime supports it.

## 13. Type-level tests

Use the repository's existing mechanism. Common patterns include:

- Dedicated fixture tsconfigs.
- `@ts-expect-error` negative cases with explanations.
- Compile-time assertion utilities.
- Dedicated type-test packages/tools.
- Consumer projects installed from a packed tarball.

Run type tests under every TypeScript generation promised to consumers. Keep diagnostics resilient unless exact messages are part of the product.

Do not install a type-test framework solely to assert one straightforward assignability rule.

## 14. Runtime tests

Use the configured runner and repository scripts. Determine:

- Node/browser/runtime environment.
- ESM/CommonJS transformation.
- Test config and setup files.
- Worker/process/shard behavior.
- Fake timer mode.
- Coverage/instrumentation transforms.
- Whether tests execute source or built artifacts.

Run focused tests first, then affected package/workspace suites. Use exact test selection syntax documented by the repository/runner; it differs across tools.

Never claim a test suite covers production module/build behavior if it uses a separate transform/resolution path.

## 15. Browser and E2E tools

Use the adopted browser framework and pinned browser versions.

- Install browsers/dependencies only through repository-provisioned commands and after trust review.
- Test production builds when hydration/chunking/minification/cache behavior matters.
- Retain traces/screenshots/videos only according to privacy and artifact policy.
- Use stable semantic selectors.
- Avoid arbitrary sleeps; wait on observable conditions.
- Bound external dependencies and isolate test users/data.
- Run required browser engines/platforms from the support contract.

## 16. Build and code generation

Run generators/builds only after reviewing their scripts/config/plugins/network access.

Validate:

- Clean generation/build.
- No uncommitted generated diff when outputs should be committed.
- Correct output directories and no source overwrite.
- Production mode and target.
- Declarations and source maps.
- Server/client graph separation.
- Environment replacement and secret exposure.
- Artifact smoke tests.

A build command can execute arbitrary plugins and repository code.

## 17. Package verification

Packaging commands can run lifecycle scripts such as prepare/prepack. Treat them as executable.

For a publishable package, use repository tooling to:

- Inspect the dry-run/packed file list.
- Create a tarball in a controlled directory.
- Install it into clean representative consumers.
- Type-check and execute public entry points.
- Verify `exports`, `types`, declarations, maps, bins, assets, and peer dependencies.
- Test ESM/CommonJS and compiler generations promised.

Common npm packaging commands exist, but use them only when npm is the package's release contract and lifecycle behavior has been reviewed.

Optional package-quality tools may check export/declaration/package metadata, but actual consumer tests remain authoritative.

## 18. Dependency graph inspection

Use the authoritative manager's installed/resolved graph commands to answer specific questions:

- Why is a package present?
- Which version(s) are resolved?
- Which package owns it?
- Which peer/optional constraints apply?
- Does a browser bundle include it?

Typical managers provide list/why/explain commands. Verify exact syntax for the pinned version.

Inspect lockfile diffs directly. Do not rely only on top-level `package.json`.

## 19. Security and license checks

Use repository-approved tools and advisory sources.

Possible checks include:

- Package-manager audit.
- Lockfile/dependency scanners.
- License/source policy.
- Secret scanning.
- Static application/security rules.
- SBOM/provenance generation.
- Container/artifact scanning.

Rules:

- Do not auto-force fixes.
- Triage exact dependency paths, environments, reachability, and fixed versions.
- Keep exceptions scoped, owned, and expiring.
- Recognize build/install/dev dependencies can still be security-critical.
- Absence of findings is not proof of safety.

## 20. Optional tools by purpose

Adopt only when the repository has a recurring need. Pin/provision them reproducibly and define what they gate.

### Public API/declarations

Tools can extract or compare declaration/API surfaces. Useful for published libraries, but they do not cover runtime behavior, package conditions, inference in all consumers, or wire semantics.

### Package metadata and resolution

Package validators can detect inconsistent `exports`, declaration paths, module formats, and compatibility. Confirm findings through packed consumer tests.

### Unused/dependency analysis

Unused-file/export/dependency tools can help large repositories. Review false positives from dynamic imports, framework conventions, generated files, plugins, and public exports before deleting anything.

### Dependency graphs/cycles

Graph tools can reveal package/module cycles and forbidden direction. Confirm runtime cycle impact and avoid architecture churn for harmless type-only edges.

### Bundle analysis and budgets

Use framework/bundler analyzers and deliberate size budgets when client performance is a product contract. Inspect parse/evaluation and chunks, not only compressed total.

### Coverage and mutation testing

Coverage is diagnostic; mutation testing can assess assertion quality for important logic. Neither is a universal merge gate.

### Fuzz/property testing

Use for parsers, validators, transforms, protocol/data boundaries, and security-sensitive input logic.

### Performance/load testing

Use the repository's runtime/browser/load harness with representative production artifacts. Record environment and acceptance thresholds.

## 21. CI stage template

Adapt rather than copy:

1. **Metadata/lockfile/format** — fast structural checks.
2. **Type-check and lint** — affected projects and configured type-aware scope.
3. **Unit/integration tests** — deterministic runtime behavior.
4. **Build/generation** — production artifacts and stale-output checks.
5. **Type/declaration/package tests** — public consumer contract.
6. **Runtime/module/browser/platform/compiler matrix** — only promised combinations.
7. **Security/license/supply chain** — advisories, sources, secrets, artifacts.
8. **Migration/E2E** — deployment-critical flows.
9. **Scheduled specialized checks** — fuzz, mutation, broad browsers, load, bundle, long compatibility matrices.

Keep merge-critical checks reliable and sufficiently fast. Do not move essential compatibility or security evidence out of pull requests solely for convenience.

## 22. TypeScript 6/7 matrix shape

When a package promises both generations, validate separately:

- Source type-check.
- Type tests and expected errors.
- Declaration consumption/emission as relevant.
- Linter/parser compatibility.
- Build framework/plugins.
- Editor/language-service integration where product-critical.
- Compiler API consumers/custom transforms.
- Runtime/package artifacts.

Do not assume one lockfile can select two `typescript` package identities cleanly without aliases/separate jobs. Follow the staged strategy in the compatibility reference.

## 23. Completion record

For every delivered change, record:

- Package manager/runtime/TypeScript versions.
- Packages/projects/configs and target environments checked.
- Exact successful commands.
- Failed commands and whether they reveal a defect or environment limitation.
- Generated/lockfile/artifact changes reviewed.
- Checks skipped and why.
- Remaining compiler, runtime, module, browser, package, or platform contracts unverified.

Never replace this record with “all checks pass” unless the actual promised matrix was executed.
