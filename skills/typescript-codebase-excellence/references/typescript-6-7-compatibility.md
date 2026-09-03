# TypeScript 6 and 7 Compatibility

Read this reference whenever selecting, upgrading, or supporting TypeScript 6/7; changing tsconfig defaults/deprecations; using the native compiler; comparing diagnostics/declarations; tuning compiler parallelism; or integrating tools that import the TypeScript compiler/language-service API.

Last behavior review: 2026-09-03. Re-check official sources before relying on version-specific statements in a later TypeScript 7.x release.

## 1. Treat TypeScript 6 and 7 as separate compatibility dimensions

TypeScript 6 and TypeScript 7 are not merely two patch levels of the same implementation.

- TypeScript 6 is the final release line based on the JavaScript compiler/language-service codebase and is the transition bridge from 5.9 to 7.
- TypeScript 7 is the native Go-based compiler/language-server line with parallel execution and different integration architecture.
- TypeScript 7.0 ships a stable `tsc` CLI but no stable programmatic compiler API.
- Tools that import `typescript`, use custom transformers, embed the language service, inspect AST/compiler internals, or depend on JavaScript API behavior may still require TypeScript 6 even when the project uses TypeScript 7 for CLI checking.
- Future TypeScript 7.x releases may add a new API; do not assume it is drop-in compatible with the TypeScript 6 API.

Therefore evaluate separately:

1. Source type-check compatibility.
2. Command-line compiler behavior.
3. JavaScript/declaration emit.
4. Editor/language-server behavior.
5. Linter/parser/framework integration.
6. Programmatic compiler API/custom transform integration.
7. Package consumer compatibility.
8. Build performance and resource behavior.

## 2. Preserve the repository's selected generation

Do not migrate compiler generation as incidental cleanup.

Before any change, determine:

- Version declared in each relevant `package.json`.
- Resolved version in the lockfile.
- Actual version printed by every compiler binary used by scripts/CI.
- Editor workspace compiler/language server.
- Framework-specific type-checkers and embedded-language services.
- Type-aware linter/parser version and selected TypeScript peer.
- Build/test/documentation/codegen tools that import or parse TypeScript.
- Published compiler support policy for libraries/plugins.

A global `tsc`, editor-bundled service, package script, framework checker, and CI binary can all differ. Record exact paths/versions rather than assuming one `typescript` dependency controls everything.

## 3. TypeScript 6 is a valid support baseline

Do not describe continued TypeScript 6 use as technical debt merely because TypeScript 7 exists.

TypeScript 6 remains appropriate when:

- Required tooling imports the TypeScript 6 API.
- Embedded-language/framework tooling has not adopted a compatible TypeScript 7 integration.
- Custom transforms/plugins depend on old AST/printer/service behavior.
- A published library promises TypeScript 6 consumers.
- Migration validation has not covered declarations, artifacts, and runtime behavior.
- Build-time improvement does not justify current compatibility risk.

Keep TypeScript 6 deprecation-clean so eventual migration remains possible. Do not hide migration debt indefinitely behind `ignoreDeprecations`.

## 4. TypeScript 6 default changes

TypeScript 6 changed several defaults. Existing repositories should make behavior-critical values explicit rather than relying on floating defaults.

Review at least:

- `strict` defaults to `true`.
- `module` defaults to `esnext`.
- `target` defaults to the most recent stable ECMAScript version immediately before `esnext`; this is intentionally moving over time.
- `noUncheckedSideEffectImports` defaults to `true`.
- `libReplacement` defaults to `false`.
- `rootDir` defaults to the directory containing the tsconfig (`.` relative to that config), rather than inferred common source root.
- `types` defaults to `[]` rather than automatically including every visible `@types` package.

Migration rules:

- Set an explicit `target` from runtime/browser support; do not accept a moving target accidentally.
- Set `module` and `moduleResolution` from the actual runtime/bundler.
- Preserve strictness intentionally. Do not set `strict: false` merely to reduce migration work; if legacy behavior must remain temporarily, scope and plan it explicitly.
- Set `rootDir` when output layout or project membership depends on it.
- List only required ambient `types` per environment instead of using `types: ["*"]` as a broad permanent fix.
- Keep Node, browser, worker, test, and build-tool globals in the projects that own them.
- Fix missing side-effect imports rather than disabling checking globally.
- Inspect effective config through `--showConfig`; `extends` chains may conceal reliance on old defaults.

## 5. TypeScript 6 deprecations and removals relevant to 7

TypeScript 7.0 hard-errors on flags/constructs deprecated for the transition. Before attempting 7, remove `ignoreDeprecations` and resolve every deprecation under TypeScript 6.

Review the official release notes for the complete list. Important areas include:

- `target: es5` and `downlevelIteration`.
- `moduleResolution: node` / `node10` and `classic`.
- `module: amd`, `umd`, `systemjs`, and `none`.
- `baseUrl` as an implicit resolution root; make `paths` mappings explicit relative to the project.
- `esModuleInterop: false` and `allowSyntheticDefaultImports: false`.
- `alwaysStrict: false` and sloppy-mode assumptions.
- Legacy `module Foo {}` namespace syntax; use `namespace` where still appropriate.
- Import assertion `assert` syntax; use the supported import-attributes form where runtime/tooling supports it.
- Legacy no-default-lib directives and related behavior.
- `outFile`/legacy concatenation workflows; use an appropriate bundler/compiler pipeline when still required.
- Command-line file arguments in a directory with a tsconfig unless explicitly opting to ignore the config.

Do not replace each deprecated option mechanically:

- A Node application and a bundled browser/Bun application need different module-resolution decisions.
- Raising the target can break supported consumers.
- Replacing `baseUrl` must preserve both TypeScript and runtime resolution.
- Replacing a legacy module emitter may require a bundler and deployment change outside the authorized scope.

If the product still requires behavior no longer supported by TypeScript 7, remain on an appropriate compiler/toolchain or plan a separate build migration.

## 6. `stableTypeOrdering` is a migration diagnostic

TypeScript 7 uses stable ordering needed for deterministic parallel checking. TypeScript 6 provides `stableTypeOrdering` to make type/declaration ordering more comparable.

Use it to:

- Reduce declaration diff noise between 6 and 7.
- Surface inference that accidentally depends on processing order.
- Diagnose errors that appear only under stable ordering.

Do not enable it permanently without a reason. Official guidance identifies it as migration-focused and notes that it can materially slow TypeScript 6 type-checking.

Recommended workflow:

1. Establish a clean TypeScript 6 baseline without `ignoreDeprecations`.
2. Run TypeScript 6 with stable ordering.
3. Fix real inference issues with the smallest explicit annotation/type argument that states intended behavior.
4. Compare declarations and diagnostics with TypeScript 7.
5. Remove the TypeScript 6 migration flag when continuous comparison is no longer required.

Do not normalize away declaration differences before reviewing whether they change public inference or semantics.

## 7. TypeScript 7.0 CLI versus compiler API

At TypeScript 7.0, the native package provides the `tsc` CLI but not the old programmatic API.

Inventory tools that may require an API:

- `typescript-eslint` and type-aware lint infrastructure.
- Custom transformers and compiler wrappers.
- Language-service plugins.
- Framework/embedded-language type-checkers.
- Documentation/API extractors.
- AST-based code generators and codemods.
- Test runners/build plugins that call `transpileModule`, create programs, or use compiler hosts.
- Tools importing `typescript` directly or declaring it as a peer dependency.
- Internal scripts using `ts`, `tsserverlibrary`, or compiler-internal modules.

Search source, lockfile, and package metadata; do not rely only on direct dependencies.

### Side-by-side compatibility package

The TypeScript project publishes `@typescript/typescript6` for transition scenarios. It provides a `tsc6` executable and re-exports the TypeScript 6 API.

An official-compatible shape can use package-manager aliases so:

- The dependency named `typescript` resolves to the TypeScript 6 compatibility package for tools expecting the old peer/API.
- A separate alias resolves to the TypeScript 7 package and exposes the native `tsc` binary.

Official transition shape as of the review date—pin or constrain versions according to repository policy and verify package-manager behavior:

```json
{
  "devDependencies": {
    "@typescript/native": "npm:typescript@^7.0.2",
    "typescript": "npm:@typescript/typescript6@^6.0.2"
  }
}
```

Do not paste this blindly:

- Alias/bin conflict behavior differs by package manager/version.
- Scripts must prove which `tsc`/`tsc6` binary they execute.
- Peer dependency resolution and workspace hoisting may select unexpected identities.
- Some tools check exact package names/versions or load internal paths.
- Two compiler generations increase lockfile, cache, and CI complexity.

Test the exact installed graph and binaries.

## 8. Editor and embedded-language compatibility

TypeScript 7 uses an LSP-based native language server, while some ecosystems embed TypeScript or require language-service plugins.

For each editor/framework/language:

- Check current official compatibility for the exact installed version.
- Determine whether syntax highlighting/basic LSP, project diagnostics, rename/refactors, framework templates, virtual files, and plugins all use the same engine.
- Do not assume CLI TypeScript 7 support means editor/template/framework support.
- Do not assume editor success means CI/compiler API tools use TypeScript 7.
- Keep TypeScript 6 editor/tooling where required while using TypeScript 7 CLI only if the split is documented, reproducible, and validated.
- Avoid forcing contributors to install undocumented global editor extensions.

Embedded languages and framework-generated virtual files are especially sensitive because they often depend on compiler/language-service APIs. Re-check support rather than maintaining a permanent hardcoded framework list.

## 9. JavaScript and JSDoc compatibility

TypeScript 7 intentionally aligns JavaScript checking more closely with TypeScript and removes several legacy/Closure-oriented special cases.

Treat migration as high risk when a project uses:

- `allowJs`/`checkJs` extensively.
- Declaration emit from `.js` files.
- Constructor functions/prototype assignment instead of classes.
- Expando properties and namespace-like CommonJS patterns.
- Closure-flavored JSDoc types/tags.
- `@class`, `@constructor`, `@enum`, standalone `?`, or legacy function-type syntax.
- Values used as types without `typeof`.
- `this` aliasing patterns or top-level CommonJS `this` assumptions.

Migration procedure:

1. Inventory JS/JSDoc constructs using representative source and emitted declaration fixtures.
2. Run TypeScript 6 and 7 checks side-by-side.
3. Compare `.d.ts` emit from JavaScript explicitly.
4. Modernize source/JSDoc in focused mechanical changes where authorized.
5. Test runtime CommonJS/ESM behavior; checker changes do not transform every legacy pattern.
6. Keep TypeScript 6 if required semantics cannot be migrated safely within scope.

Do not replace unsupported JSDoc with `any` everywhere merely to make TypeScript 7 pass. Preserve useful contracts or convert affected code to explicit modern JavaScript/TypeScript patterns.

## 10. Type-system and declaration differences

Even when most code checks identically, review:

- Stable union/property ordering in declarations and diagnostics.
- Template-literal inference over Unicode code points versus UTF-16 code units.
- Inference that changes under stable ordering.
- Declaration conflict reporting that may surface despite `skipLibCheck` expectations.
- JavaScript/JSDoc inference and declaration emit.
- Generated API reports/snapshots whose ordering changed.
- Type tests relying on exact printed representation rather than assignability.

Do not auto-accept declaration/API snapshots because differences look like ordering. Confirm exported assignability, inference, overload behavior, and consumer impact.

For string type utilities intentionally modeling UTF-16 indexing, add explicit tests under both generations and decide whether the semantic change is breaking.

## 11. Compiler API and AST migration risk

For tools eventually moving from the TypeScript 6 API to a TypeScript 7.x API:

- Treat the new API as a separate port, not a package-version bump.
- Use public documented APIs only where possible.
- Revalidate node kinds, factories, source positions, encodings, trivia/comments, parent links, symbols/types, printer output, source maps, incremental hosts, and cancellation.
- Do not assume offsets/positions use the same encoding or units.
- Do not mutate compiler-owned nodes or depend on object identity/order.
- Maintain fixture suites for syntax, JSX, JSDoc, modules, declarations, transforms, and diagnostics.
- Pin supported compiler API generations and fail clearly outside them.
- Keep a compatibility adapter isolated rather than scattering version checks throughout business logic.

Wait for the exact official API contract and tool support when required; do not invent compatibility shims against undocumented native internals.

## 12. Migration preparation on TypeScript 6

Before first TypeScript 7 comparison:

1. Pin a current approved TypeScript 6 version.
2. Remove `ignoreDeprecations` and resolve every diagnostic.
3. Make target, module, resolution, rootDir, types, libs, JSX, decorators, emit, and strictness explicit.
4. Verify package exports/runtime resolution independently from tsconfig paths.
5. Run full TypeScript 6 source, build, declaration, type-test, package, and runtime suites.
6. Run TypeScript 6 with stable ordering and review new diagnostics/declarations.
7. Inventory all compiler API/parser/editor/framework integrations.
8. Record performance and memory baseline.
9. Commit or preserve a clean migration baseline before introducing TypeScript 7 changes.

Do not combine deprecation fixes, module migration, framework upgrade, dependency refresh, and native compiler cutover in one opaque change when they can be reviewed separately.

## 13. Side-by-side validation

Use separate explicit commands/jobs whose compiler identity is visible.

Compare:

- `--version` output and resolved binary path.
- Effective tsconfig and included files.
- Exit status and diagnostics.
- Emitted JavaScript if `tsc` owns emit.
- `.d.ts` and declaration maps.
- Generated API reports/type snapshots.
- Type tests and representative downstream consumers.
- Framework/bundler/test/lint/codegen output.
- Production package/bundle/runtime tests.
- Clean/incremental/watch behavior where relevant.
- Wall time, peak memory, process count, and CI stability.

Normalize only known nondeterministic/environment data. Keep a reviewed allowlist of expected differences; do not pipe both outputs through broad sorting or ignore rules that could hide semantic changes.

## 14. TypeScript 7 parallelism

TypeScript 7 parallelizes parsing, checking, and emit. In 7.0, the checker/builder tuning flags are experimental, and single-threaded operation is available for diagnosis or constrained environments.

Important behavior:

- TypeScript 7.0 defaults to four checker workers. Increasing the count can improve large builds but increases duplicated work and memory.
- Lower checker count can help small or memory-constrained CI.
- Parallel project builders can multiply with checker workers. For example, several builders each using several checkers can create many concurrent checker workers.
- Project dependency graph limits useful builder parallelism.
- Single-threaded mode is useful for diagnosis, external orchestration, deterministic comparison, or severe resource constraints.
- Varying checker count can rarely expose order-dependent results; using an explicit count across environments may improve reproducibility where this is observed.

Tuning procedure:

1. Validate correctness first.
2. Measure clean, incremental, and CI workloads separately.
3. Record CPU allocation, memory limit, process limit, and external task-runner parallelism.
4. Sweep a small set of checker/builder combinations.
5. Choose the simplest stable configuration with meaningful benefit.
6. Add an explicit CI setting only when defaults are unsuitable.

Do not set both values to host CPU count or “maximum.”

## 15. Library support for TypeScript 6 and 7

A library that claims support for both must define what support means:

- Its published declarations parse and type-check under both.
- Public inference and negative type tests behave as documented.
- Runtime package works in promised module/runtimes independently of compiler.
- Dependencies/peer types support both.
- Examples and generated API docs remain valid.
- No declaration references unavailable libs or compiler-only internals.

Use clean consumer projects for each compiler generation. Avoid emitting declarations with a newer generation that use syntax/semantics an older promised compiler cannot consume without testing.

Decide whether support covers only consuming declarations or also building the source. Document minimum supported patch/range and do not infer it from one successful local install.

## 16. Applications and hybrid toolchains

An application may adopt TypeScript 7 CLI checks while retaining TypeScript 6 for lint/framework/compiler-API tools.

This is acceptable only when:

- Each command names/selects its compiler unambiguously.
- CI validates both sides.
- Diagnostics do not conflict silently.
- The build artifact owner is clear.
- Contributors/editors receive documented behavior.
- Lockfile/aliases are stable under the package manager.
- Generated declarations/artifacts come from one deliberate compiler.
- Rollback is straightforward.

Avoid running both compilers redundantly forever without a reason. Remove TypeScript 6 only when every required API/tool integration has a verified replacement.

## 17. Rollout and rollback

For a deliberate TypeScript 7 rollout:

- Keep the migration changes reviewable and separate from unrelated code.
- Roll out CI comparison before making 7 required when feasible.
- Capture expected differences and failures.
- Monitor build time, memory, crash rate, editor/tooling issues, declaration changes, and false diagnostics.
- Pin the approved compiler version; do not float immediately across early minor releases without policy.
- Keep a lockfile/package rollback path.
- Avoid releasing public declarations or packages from TypeScript 7 until consumer checks pass.
- Document temporary TypeScript 6 tooling and removal criteria.

Rollback must consider generated declarations, build caches, API snapshots, and editor settings—not only `package.json`.

## 18. Common migration failures to reject

- Changing `typescript` to 7.x and assuming every tool follows.
- Hiding TypeScript 6 deprecations with `ignoreDeprecations` until the 7 cutover.
- Adding `types: ["*"]` globally to restore ambient behavior without environment isolation.
- Accepting the floating target/module defaults accidentally.
- Replacing module resolution without testing runtime/package behavior.
- Comparing TypeScript 6 declarations without stable ordering and accepting all diff noise.
- Leaving stable ordering enabled permanently without need despite TypeScript 6 performance cost.
- Using TypeScript 7 for a custom transformer despite no compatible API.
- Claiming framework/editor support from `tsc` success.
- Treating JavaScript/JSDoc projects as ordinary `.ts` migrations.
- Maximizing `--checkers` and `--builders` on constrained CI.
- Claiming TypeScript 6/7 library support from one workspace build.

## TypeScript 6/7 completion checklist

- Exact compiler binaries and integrations are inventoried.
- Repository compiler generation is preserved unless migration is explicit.
- TypeScript 6 defaults and deprecations are handled deliberately without suppression.
- Stable ordering is used only as a migration diagnostic where needed.
- CLI and compiler-API compatibility are evaluated separately.
- JS/JSDoc, declarations, type tests, packages, and consumers are compared.
- Editor/framework/linter/build tools are verified at exact versions.
- TypeScript 7 parallelism is tuned against real memory/CI constraints.
- Dual-generation support has an explicit matrix and clean consumer evidence.
- Rollout, temporary coexistence, and rollback are documented and reproducible.
