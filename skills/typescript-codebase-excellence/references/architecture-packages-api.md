# Architecture, Packages, Workspaces, and Public API

Read this reference for repository structure, workspace/package boundaries, tsconfig architecture, dependency direction, public exports, declaration files, package publishing, compatibility, and release design.

## 1. Start from the actual product boundary

Classify each affected package before changing structure:

- **Application or service:** optimized for reproducible deployment, operational behavior, controlled upgrades, and internal cohesion.
- **CLI:** optimized for automation contracts, platform behavior, startup time, diagnostics, exit codes, and distributable artifacts.
- **Published library:** optimized for downstream compatibility, narrow exports, declaration quality, module/runtime support, and dependency containment.
- **Browser application:** optimized for user-visible behavior, bundle boundaries, accessibility, security, browser support, and deployment assets.
- **SSR/full-stack application:** owns at least two execution environments; server/client separation and serialization boundaries are architectural contracts.
- **Worker or serverless function:** constrained by runtime APIs, startup, resource ceilings, deployment packaging, concurrency model, and lifecycle semantics.
- **Build tool, plugin, or code generator:** executes in another tool's process or build graph and may depend on version-sensitive APIs.
- **Shared internal package:** useful only when several packages consume one stable capability; it is not automatically a public library.
- **Mixed JavaScript/TypeScript package:** has `allowJs`, `checkJs`, JSDoc, declaration emit, and migration behavior that may differ from pure TypeScript.

Do not apply library stability rules mechanically to an internal application, or application shortcuts to a package consumed independently.

## 2. Module versus package

Prefer a **module or directory** when code:

- Is released, versioned, tested, and deployed with its parent package.
- Shares the same runtime, target, dependency policy, and ownership.
- Needs a visibility/cohesion boundary rather than independent distribution.
- Has no credible independent consumer.
- Would require awkward public APIs, duplicated types, or cycles if extracted.
- Would gain only a shorter file or a fashionable layer name.

Create a **package** only when at least one durable boundary exists:

- Multiple independently built packages consume a stable capability.
- Runtime, platform, module, browser/server, or dependency constraints differ materially.
- A package must be published or versioned independently.
- An integration/plugin boundary requires a stable external contract.
- Native code, generated code, security-sensitive code, or build tooling benefits from dependency and execution isolation.
- Ownership, release cadence, deployment, or compliance controls are genuinely separate.
- Measured build-graph or caching benefits outweigh coordination and API cost.

A directory being large, having many files, or being called “domain” is not sufficient reason to create a package.

### Package extraction gate

Before extracting, answer:

1. What contract will the new package own?
2. Which consumers build, deploy, or version it independently?
3. Which runtime, dependency, or platform concerns become better isolated?
4. What public declaration and SemVer burden is introduced?
5. How will cycles and duplicate dependency instances be prevented?
6. Could a private module or workspace path solve the actual problem?

If the answers are weak, keep the code in one package.

## 3. Source and module hygiene

- Organize modules around cohesive responsibilities and owned invariants, not arbitrary line counts or one-symbol-per-file rules.
- Keep entry points focused on composition, startup, and export curation rather than accumulating business logic.
- Avoid catch-all `utils`, `helpers`, `common`, `shared`, or `types` modules that become dependency sinks. Name the capability precisely.
- Keep domain logic independent from transport, framework, persistence, and process-global state when that creates a real testable boundary.
- Use file/module/package visibility conventions consistently. TypeScript's `private` and compile-time visibility do not create a security boundary.
- Keep import direction acyclic and intentional. Lower-level domain code should not import application wiring, UI, or deployment layers.
- Co-locate focused tests where repository convention supports it; keep consumer, package, runtime, and cross-package tests at the boundary they verify.
- Isolate generated, vendored, compatibility, platform-specific, and native-wrapper code so normal review and lint scope stays clear.
- Split a file when cohesion, navigation, ownership, generated/manual separation, or platform boundaries improve—not to satisfy an arbitrary maximum.

## 4. Workspace discipline

For npm, pnpm, Yarn, Bun, or other workspaces:

- Identify the authoritative workspace declaration and lockfile.
- Keep dependency versions centralized only when packages genuinely share support policy and upgrade cadence.
- Do not create a “shared” package for values used in only one package or for framework-specific implementation leakage.
- Avoid circular package dependencies even when the package manager or bundler can tolerate them. Cycles complicate initialization, declarations, builds, and ownership.
- Keep browser-only, server-only, build-only, and test-only dependencies in the package that owns them.
- Distinguish source imports from package-consumer imports. Workspace source aliases can hide missing exports or packaging defects.
- Ensure task orchestration reflects real dependency order and cache inputs. A green cached build must not depend on undeclared files, environment, or generated state.
- Do not assume every package should share one tsconfig, lint rule set, runtime target, or strictness exception.
- Keep root scripts as orchestration. Package scripts should remain runnable enough to diagnose package-local failures.

### Internal package consumption

Choose deliberately among:

- Consuming built package artifacts through declared exports.
- Consuming source through a framework/bundler that understands workspace source.
- Using project references and declaration outputs.
- Using a monorepo-specific pipeline.

Do not mix these accidentally. Source consumption can hide packaging errors; artifact consumption can slow development; project references add build contracts. Follow the repository's established model unless the task explicitly changes it.

## 5. Package manager and lockfile contract

Treat these as compatibility and reproducibility decisions:

- `packageManager` and version constraints.
- Lockfile format and repository policy.
- Workspace hoisting/isolation behavior.
- Peer-dependency resolution.
- Patch/override/resolution mechanisms.
- Registry and source policy.
- Lifecycle-script and native-build behavior.
- Frozen/immutable installation flags in CI.

Rules:

- Use the package manager selected by the repository. Do not generate a second lockfile.
- Do not update the lockfile incidentally through an unrelated command.
- Review new package sources, tarball integrity, transitive additions, duplicate versions, peer changes, engines, native modules, and scripts.
- Keep overrides narrow, documented, and temporary unless they represent deliberate policy.
- Do not treat a lockfile as proof of safe or reproducible execution; install scripts, native toolchains, environment, network downloads, and generated files can still vary.
- For published libraries, remember that consumers resolve their own graph. Test supported dependency ranges and peer contracts, not only one workspace resolution.

## 6. tsconfig architecture

A tsconfig is part of the build contract, not an editor preference.

Inspect:

- `extends` chains and whether paths resolve inside published packages or only the monorepo.
- `include`, `exclude`, `files`, `rootDir`, `outDir`, `declarationDir`, and generated-source boundaries.
- `composite`, `incremental`, `tsBuildInfoFile`, and project references.
- `module`, `moduleResolution`, `target`, `lib`, `types`, `typeRoots`, JSX, decorators, and class-field behavior.
- `noEmit`, declaration-only emit, source maps, declaration maps, and who owns JavaScript emit.
- Strictness and repository-specific safety flags.
- Test, build-tool, Node, browser, worker, storybook, and framework-specific configs.

Guidance:

- Use separate configs when environments, emit, or ambient globals differ materially—not merely to avoid understanding one config.
- Keep production source out of test-only ambient types and vice versa.
- Avoid broad `include` globs that pull generated output, fixtures, build directories, or unrelated packages into a project.
- Keep output outside input. Never let emitted files become source inputs on later runs.
- Give each incremental project a distinct build-info location where parallel jobs or multiple configs could collide.
- Do not use `skipLibCheck` as a substitute for fixing duplicate or incompatible declarations. If retained for build-time reasons, understand which errors it can hide and keep dependency/type compatibility checks elsewhere.
- Treat enabling project references as an architecture/build change. It affects declaration boundaries, incremental state, editor behavior, and task ordering.

## 7. Project references

Project references are useful when packages or large projects have real dependency boundaries and benefit from incremental builds or declaration isolation.

Before adding them, verify:

- Dependency direction is acyclic.
- Referenced projects can emit the declarations/artifacts consumers need.
- Build scripts invoke `tsc --build` or an equivalent repository flow correctly.
- Clean, incremental, editor, and CI behavior agree.
- Build-info files and outputs are ignored or committed according to policy.
- Tests and framework builds do not accidentally consume stale declarations.
- Path aliases and package exports do not create two competing notions of identity.

Do not add references merely because a repository is a monorepo. Small packages may be simpler with independent type-check commands.

## 8. Public API is broader than exported functions

Public API can include:

- Package root and subpath exports, export conditions, and module format.
- Exported types, values, classes, interfaces, namespaces, enums, symbols, constants, and declaration merging.
- Function overloads, optional parameters, generic defaults and constraints, type predicates, assertion signatures, and inferred return types.
- Class constructors, public/protected members, nominal private-field identity, inheritance behavior, and `instanceof` expectations.
- Union members and discriminants callers switch over.
- Error classes, codes, causes, and rejection behavior.
- Declaration files, declaration maps, JSDoc, and editor-visible documentation.
- Package dependencies whose types appear in exported signatures.
- CLI flags/output/exit codes, configuration keys/defaults, environment variables, wire/storage schemas, and generated clients.
- Runtime side effects, initialization order, tree-shaking metadata, and singleton identity.
- Supported runtimes, compiler versions, module loaders, browsers, and minimum platform versions.

An internal application may still have stable internal APIs between independently owned packages or deployment components.

## 9. Export design

- Default to no export, then package-internal export, then public package export only when independent consumption is intended.
- Curate entry points explicitly. Do not expose every source file through wildcard package exports unless deep import is the deliberate contract.
- Prefer exporting behavior and validated data shapes over mutable implementation objects.
- Avoid leaking framework, ORM, validation-library, compiler-API, or internal dependency types unless that commitment is intentional.
- Avoid “barrel” files that create cycles, eager side effects, poor tree shaking, or unclear ownership. A curated public barrel can be appropriate.
- Use `export type` where required by emit semantics and to avoid runtime edges; do not treat it as a stylistic rewrite target.
- Preserve symbol identity. Rebundling or dual publishing must not produce duplicate class, token, context, or singleton instances for one logical package.
- Do not add a default export merely for convenience when named exports are the established API, or vice versa.

### Package `exports` and `imports`

- Make runtime and type declarations resolve through the same intended subpaths.
- Order conditions according to runtime/package-tool expectations and test them in supported consumers.
- Prevent unintentional deep imports by exposing only supported paths.
- Keep internal aliases under package `imports` or repository tooling when appropriate rather than publishing accidental names.
- Include all files referenced by exports in the packed artifact.
- Test source maps and declaration maps from the installed package when they are part of the developer experience.

## 10. Declaration design and emit

For published or independently consumed packages:

- Inspect emitted `.d.ts`, not only source types.
- Add explicit exported annotations when inference depends on private names, unstable internals, enormous inferred structures, or compiler-version-specific details.
- Avoid exposing anonymous inferred types that make declarations unreadable or non-portable.
- Ensure declarations do not reference monorepo-only paths, source files, test globals, unpublished packages, or missing ambient types.
- Keep declaration output deterministic enough for review and API comparison.
- Verify `declarationMap` paths do not expose unavailable or sensitive sources unintentionally.
- Use `isolatedDeclarations` only when the ecosystem/build pipeline benefits and migration cost is authorized; do not enable it as a style exercise.
- Treat declaration emit changes across compiler generations as compatibility work even when runtime JavaScript is unchanged.

Generated declarations are artifacts, not proof that the runtime implementation honors the types.

## 11. SemVer and compatibility review

Before publishing, inspect changes to:

- Removed, renamed, moved, or newly hidden exports and subpaths.
- Parameter types, optionality, return types, overload order, generic constraints/defaults, and inference behavior.
- Widened or narrowed unions, discriminants, literal types, tuple structure, readonly-ness, and property optionality.
- Interface/class members, constructor visibility, inheritance, private/protected identity, and static members.
- Enums and const enums, especially runtime values and inlining assumptions.
- Error classes/codes and rejection or throw behavior.
- Package export conditions, ESM/CommonJS format, side effects, and default/named interop.
- Declaration files under every supported compiler generation.
- Minimum runtime, compiler, DOM/lib, module resolver, and browser support.
- Peer dependency and optional dependency ranges.
- Wire, storage, configuration, CLI, and behavior contracts.

Type changes can be breaking even when JavaScript is unchanged. Conversely, a source-level type refactor may be non-breaking if the packaged declaration and runtime contract remain identical. Validate the artifact and representative consumers.

Automated API extractors or declaration-diff tools are useful evidence, not complete SemVer analysis. They can miss inference, conditional exports, runtime identity, behavior, and configuration changes.

## 12. Generated code and source of truth

- Mark generated outputs clearly and keep the generator, inputs, version, and command reproducible.
- Do not hand-edit generated clients, schemas, declarations, route manifests, or bundles.
- Keep generated code out of normal formatting/lint scope when the generator owns its representation.
- Review generated diffs for contract changes, secrets, unstable timestamps/paths, and unexpected dependency or endpoint exposure.
- Decide deliberately whether generated artifacts are committed, built during packaging, or generated downstream.
- Ensure clean-checkout and packed-package builds do not rely on untracked local generated state.
- When generation executes third-party code or downloads schemas, apply supply-chain and network trust controls.

## 13. Packaging and release

Treat the installed package or deployed artifact—not the workspace source tree—as the release input.

Before release, as applicable:

- Inspect the packed file list and exclude secrets, fixtures, tests, source credentials, local state, caches, oversized artifacts, and accidental configs.
- Install or consume the packed tarball in a clean representative project.
- Verify every export condition and declaration path from supported runtimes/module systems.
- Verify source maps, licenses, README, type declarations, executable permissions, bin shims, and native assets.
- Check side effects and tree-shaking metadata against actual module initialization.
- Confirm package version, changelog, peer ranges, engines, compiler support, browser support, and migration notes.
- Build from a reviewed source revision through repository-approved release tooling.
- Generate SBOM, provenance, signatures, or attestations when the distribution/compliance contract requires them.
- Define deprecation, rollback, yanking/unpublishing constraints, and security advisory handling.

Do not publish directly from an unreviewed dirty tree or bypass package verification merely to make the release command succeed.

## Architecture completion checklist

- Package and module boundaries reflect real ownership, runtime, and release contracts.
- Dependency direction is intentional and acyclic.
- Package manager, lockfile, workspace, and tsconfig hierarchy are preserved deliberately.
- No accidental compiler, runtime, target, module, JSX, decorator, or ambient-type change.
- Public exports and declarations are minimal, usable, and compatible.
- Generated output has a clear source of truth.
- Package artifacts resolve and execute in supported consumers.
- SemVer-sensitive type and runtime changes are identified.
- Release contents and provenance match the reviewed source.
