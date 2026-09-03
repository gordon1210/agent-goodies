# Build Pipelines, Generated Code, and Framework Integration

Read this reference when a repository uses bundlers, transpilers, framework compilers, custom transformers, compiler plugins, code generation, decorators, JSX, environment replacement, source maps, minification, or multiple build stages.

## 1. Map the complete build pipeline

Before changing build configuration, identify every stage from source to artifact:

1. Source discovery and generated-source preparation.
2. Type-checking and declaration checking.
3. TypeScript/JavaScript syntax transformation.
4. Framework-specific compilation or macro expansion.
5. Module resolution, bundling, chunking, and asset processing.
6. Environment/config replacement.
7. Minification, source-map generation, instrumentation, and hashing.
8. Packaging/container/serverless assembly.
9. Deployment and runtime loading.

For each stage, record:

- Tool and exact version.
- Input/output directories and file extensions.
- Whether it executes TypeScript's compiler API or parses TypeScript independently.
- Whether it performs semantic type-checking or only syntax transformation.
- Module/target assumptions.
- Cache inputs and generated state.
- Runtime/browser/platform target.
- Which stage owns errors, declarations, source maps, and emitted JavaScript.

Do not assume a tool that transpiles TypeScript also validates types. Do not assume `tsc --noEmit` sees the same resolution, macros, environment replacements, or generated files as the production build.

## 2. One owner per artifact

Avoid ambiguous output ownership:

- If a bundler/framework emits JavaScript, configure TypeScript primarily for checking and declarations according to repository policy.
- If `tsc` emits JavaScript, ensure no later tool silently changes module semantics without matching tests.
- Keep declaration output owned by one deliberate stage.
- Avoid two tools writing the same directory or source-map file.
- Keep generated source separate from compiled output.
- Ensure clean builds remove only owned artifacts, never source or another package's output.

Parallel or incremental builds must not race on shared output, cache, or `tsbuildinfo` files.

## 3. Single-file transpilers and isolated semantics

Tools that transform one file at a time cannot rely on cross-file type information for emit.

When such a tool owns JavaScript emission:

- Preserve or enable the repository's isolated-module constraints.
- Use type-only imports/exports where required to avoid incorrect runtime edges.
- Avoid constructs whose emit depends on cross-file semantic analysis unless the pipeline explicitly supports them.
- Check namespace, const-enum, import-elision, re-export, and declaration behavior.
- Keep Babel/SWC/esbuild/framework transform settings aligned with TypeScript syntax and class/decorator semantics.
- Test runtime output, not only type-checking.

Do not enable an isolated-mode flag and then suppress every error. Each diagnostic usually points to a construct the emitter cannot reproduce safely.

## 4. Bundler configuration

A bundler owns more than concatenation:

- Module resolution and aliases.
- Conditional exports and browser mappings.
- Code splitting and dynamic imports.
- Tree shaking and side-effect analysis.
- CSS/assets/workers/Wasm handling.
- Environment replacement and dead-code elimination.
- Target syntax and polyfill integration.
- Minification and source maps.
- Server/client graph separation in some frameworks.

Review changes for both build success and runtime behavior.

### Entry points and chunks

- Keep entry points explicit and minimal.
- Avoid importing server setup, polyfills, telemetry initialization, or global registries into shared modules unintentionally.
- Verify dynamic-import paths remain statically discoverable where required.
- Bound chunk proliferation and startup waterfalls when performance matters.
- Ensure lazy-loaded code handles loading errors and version skew after deployment.
- Test workers and assets through the deployed path, not source-relative assumptions.

### Tree shaking and side effects

- Mark packages/modules side-effect-free only when top-level evaluation is genuinely safe to remove.
- Account for CSS imports, polyfills, registrations, decorators, custom elements, and global initialization.
- Avoid relying on tree shaking as a security boundary; sensitive values must not enter the client graph at all.
- Inspect bundle output before claiming a dependency or secret was removed.
- Keep public export barrels from pulling large side-effectful graphs into consumers.

## 5. Target and transformation semantics

Compiler target, bundler target, and runtime/browser support must agree.

- A higher target can reduce transform cost and bundle size but may break supported runtimes.
- A lower target may introduce helpers, semantic differences, or larger output.
- Syntax transformation does not provide missing runtime APIs.
- Polyfills can affect globals, prototypes, bundle size, and loading order.
- Class fields, private fields, async/await, generators, optional chaining, and top-level await may be transformed differently by tools.
- Do not compare source semantics without inspecting the actual shipped transformation.

When multiple tools transform the same syntax, define which one owns it and disable duplicate/incompatible transforms.

## 6. JSX and UI compilation

JSX behavior depends on:

- Framework/runtime.
- Classic versus automatic transform.
- Import source and development transform.
- Server/client component or template compiler rules.
- Babel/SWC/framework plugins.
- TypeScript JSX setting and ambient JSX types.

Do not change JSX mode or import source incidentally. It can alter runtime imports, element semantics, development diagnostics, bundle output, and declarations.

Keep framework-specific generated types and virtual modules synchronized with the framework's build/generation command. Avoid declaring broad ambient shims merely to silence missing virtual modules without verifying runtime generation.

## 7. Decorators and metadata

Decorator behavior varies across legacy TypeScript transforms, current JavaScript decorator semantics, framework compilers, and metadata libraries.

Before changing decorator settings or compiler generation:

- Identify the exact decorator proposal/transform expected by the framework.
- Check evaluation order, initializer behavior, field semantics, and emitted helper format.
- Determine whether runtime type metadata is emitted or reflected.
- Check whether minification/renaming affects metadata consumers.
- Verify declaration and source-map output.
- Test dependency injection, serialization, ORM, validation, routing, or test mocking that consumes metadata.

Do not enable metadata emission globally without a consumer and a privacy/bundle-size review. Runtime metadata can expose names and increase coupling.

## 8. Environment replacement and configuration

Build tools often replace expressions such as environment variables at build time.

- Identify which values are build-time constants, runtime configuration, or secrets.
- Maintain a strict server/client allowlist for values embedded into browser bundles.
- Validate missing/invalid configuration before building or starting as appropriate.
- Avoid dynamic property access when the replacement mechanism only supports static expressions.
- Do not rely on minification to remove secrets from unreachable branches.
- Keep development, test, preview, and production modes explicit and test meaningful differences.
- Ensure cached builds include relevant environment/config fingerprints without exposing secret values in cache keys or logs.

A variable with a server-sounding name can still be bundled if imported into a client graph. Verify the artifact.

## 9. Framework-owned boundaries

Frameworks may own routing, data loading, server/client splitting, serialization, cache/revalidation, request context, middleware ordering, or build-time generation.

Guidance:

- Follow the exact installed framework version and repository conventions.
- Do not apply guidance from another major version or rendering mode.
- Keep domain logic independent from framework hooks when that improves testability without creating unnecessary layers.
- Respect framework lifecycle and cleanup semantics.
- Treat server/client, static/dynamic, build/request, and trusted/untrusted transitions as explicit boundaries.
- Do not bypass framework security or escaping primitives through assertions or raw rendering APIs.
- Test production builds; development servers often have different resolution, caching, error handling, and rendering behavior.
- Avoid replacing a framework mechanism with a parallel custom abstraction unless a demonstrated limitation requires it.

## 10. SSR, prerendering, and hydration build concerns

For SSR or prerendered systems:

- Ensure modules imported by server and client are safe in both environments or split them explicitly.
- Avoid top-level access to `window`, `document`, filesystem, process, or request-local data in shared modules.
- Keep request-specific state out of process-global singletons unless safely keyed and bounded.
- Serialize only values that have a defined wire representation.
- Prevent secrets and server-only implementation from entering hydration payloads.
- Verify build-time execution does not depend on production-only services or leak credentials into generated pages.
- Test hydration against the production minified bundle and deployed asset URLs.

Framework type generation does not replace runtime serialization or authorization checks.

## 11. Code generation

Code generation is appropriate when a machine-readable source of truth owns repetitive contracts, such as protocol schemas, database schemas, routes, API clients, parser tables, or asset manifests.

For every generator, define:

- Authoritative input.
- Generator package and exact version.
- Deterministic invocation.
- Expected outputs and ownership.
- Whether outputs are committed.
- How stale output is detected.
- Network access and schema provenance.
- Compatibility and review process for generated changes.

Rules:

- Never hand-edit generated output.
- Keep generated files visibly marked.
- Normalize timestamps, absolute paths, host-specific ordering, and nondeterministic IDs.
- Fail clearly when inputs are invalid or versions mismatch.
- Do not execute untrusted generators with host credentials or broad filesystem access.
- Review generated code for unsafe defaults, over-broad types, nullable/optional semantics, authentication omissions, and breaking schema changes.
- Keep custom templates small; large forks of generated output become maintenance liabilities.

### Generated types and runtime validators

Generated static types do not validate responses. Use generated codecs/validators when the source system provides reliable runtime checks, or validate at the boundary according to risk.

Ensure generated types correctly represent:

- Nullability versus optionality.
- Numeric precision and special formats.
- Unknown fields and versioning.
- Discriminated variants.
- Date/time, byte, bigint, map, and enum representation.
- Error responses and pagination.

## 12. Custom transformers and compiler plugins

Custom TypeScript transformers, language-service plugins, AST tools, and compiler wrappers are version-sensitive integrations.

Before modifying or upgrading them:

- Identify whether they use public or internal compiler APIs.
- Check node kinds, factory APIs, source positions, symbols/types, printer behavior, comments, source maps, and declaration transforms.
- Verify plugin loading in editor, CLI, framework, and test environments.
- Add fixture-based tests for representative syntax and emitted output.
- Avoid mutating compiler-owned nodes or relying on undocumented properties.
- Pin supported compiler generations and fail with a useful diagnostic outside them.
- Keep transforms deterministic and free from ambient network/time/filesystem behavior unless explicitly part of the contract.

TypeScript 7 adoption requires a separate compatibility decision for tools importing the JavaScript compiler API; see [typescript-6-7-compatibility.md](typescript-6-7-compatibility.md).

## 13. Compiler-independent parsers and AST tools

Linters, formatters, codemods, documentation tools, and bundlers may parse TypeScript without using TypeScript's own parser.

- Verify support for the exact syntax and compiler generation used by the repository.
- Do not assume accepting syntax means reproducing TypeScript's semantic checking or emit.
- Test decorators, JSX, import attributes, using declarations, new syntax, and mixed JS/JSDoc where applicable.
- Keep parser/linter versions compatible with the selected TypeScript generation and ESLint version.
- Review autofixes and codemods as code changes; never run broad transforms and accept all output blindly.
- Preserve comments, source maps, shebangs, directives, and formatting source of truth.

## 14. Minification and property mangling

Minification can affect more than size:

- Stack traces and diagnostics.
- Function/class names used by reflection or frameworks.
- Property names accessed externally, serialized, or by native code.
- Side-effect ordering assumptions.
- Dead-code elimination around environment checks.
- Error messages and privacy.

Property mangling requires an explicit safe-name policy. Never mangle protocol fields, public API properties, DOM attributes, serialized keys, framework metadata, or dynamically accessed names without proof.

Run critical tests against minified production output when minification could alter behavior.

## 15. Source maps and instrumentation

A multi-stage pipeline must preserve mapping across every transform.

- Configure each stage to consume previous maps where supported.
- Avoid publishing private source content accidentally through inline maps.
- Verify line/column mapping from deployed errors.
- Ensure coverage/instrumentation does not change production bundles unless intended.
- Keep build paths reproducible and avoid leaking developer home directories.
- Treat source-map upload credentials and release identifiers as secrets/configuration.

## 16. Build caching and reproducibility

A correct cache key includes every input that can affect output:

- Source and generated input.
- Tool versions and configuration.
- Compiler/bundler/framework plugins.
- Relevant environment values.
- Lockfile and workspace dependency artifacts.
- Platform/architecture when native or platform-specific output exists.

Do not include secrets directly in keys or logs. Avoid undeclared network data and current time in deterministic builds.

Test a clean build periodically. Incremental success can hide stale generated files, undeclared dependencies, and output collisions.

## 17. Build verification

When build behavior changes, validate as applicable:

1. Clean generation.
2. Type-check.
3. Development build only if it owns meaningful semantics.
4. Production build.
5. Declaration emit.
6. Packaged artifact or container/serverless bundle.
7. Runtime smoke/integration tests from the artifact.
8. Browser/worker/framework deployment mode.
9. Source-map and error mapping.
10. Bundle content/size and secret scan.
11. Incremental/repeated build and clean behavior.
12. Supported TypeScript compiler generations and tool plugins.

Do not claim build compatibility from source tests alone.

## Build completion checklist

- Every build stage, owner, input, output, and executable extension is known.
- Type-checking and transpilation responsibilities are not conflated.
- Module, target, JSX, decorator, and class semantics agree across tools.
- Generated output has one source of truth and is deterministic.
- Framework server/client and build/request boundaries are preserved.
- Environment replacement cannot expose secrets to client artifacts.
- Compiler plugins and AST tools are version-compatible and fixture-tested.
- Production, packaged, and minified artifacts receive appropriate runtime validation.
- Caches do not hide undeclared inputs or stale output.
