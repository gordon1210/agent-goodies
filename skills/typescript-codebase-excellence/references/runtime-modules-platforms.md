# Runtime, Modules, Resolution, and Platforms

Read this reference whenever code or configuration depends on ESM/CommonJS, import resolution, package exports, JavaScript emit, Node.js, Bun, Deno, browsers, workers, edge runtimes, Electron, native TypeScript execution, or environment-specific globals.

## 1. Separate the four systems

A TypeScript project often has four related but distinct systems:

1. **The checker** decides whether imports and types are valid.
2. **The emitter/transpiler/bundler** decides what JavaScript and specifiers are produced.
3. **The package resolver/loader** decides what files a specifier identifies at runtime.
4. **The deployment platform** decides which APIs, syntax, module formats, conditions, permissions, and file semantics exist.

A successful editor import or `tsc --noEmit` does not prove that the deployed runtime can load the module. A successful bundler build does not prove that direct Node.js, test-runner, or package consumers resolve it the same way.

Before changing imports or compiler options, identify who owns each system.

## 2. Establish the environment matrix

For each project, record:

- Runtime and minimum version.
- Operating systems and CPU architectures.
- Browser targets and whether legacy/transpiled output is required.
- Main thread, Web Worker, service worker, edge worker, server, build process, test process, or Electron main/preload/renderer.
- ESM, CommonJS, script, IIFE, AMD, or platform-specific module expectations.
- Direct source execution, emitted JavaScript, bundled artifact, serverless package, or published package.
- Available global APIs and ambient type libraries.
- Filesystem, path, URL, permissions, signals, process, network, and subprocess behavior.
- Native addons, WebAssembly, or platform-specific dependencies.

Do not type-check several environments in one project merely because their globals are convenient. Accidental ambient compatibility can conceal code that cannot run in its deployment context.

## 3. Align `module` and `moduleResolution`

`module` affects emitted module syntax and, in modern TypeScript modes, can also model runtime-specific behavior. `moduleResolution` determines how imports are interpreted during checking.

Rules:

- Choose settings that model the actual runtime or bundler, not a generic preference.
- Preserve repository-local pairings and framework presets unless a migration is explicit.
- For code executed directly by Node.js, use Node-aware modes appropriate to the supported Node behavior.
- For code always handled by a capable bundler, a bundler-oriented resolution mode can be appropriate.
- Do not use a bundler resolution model to claim that emitted files will execute directly in Node.js.
- Do not use legacy resolution merely to keep old aliases working without understanding runtime behavior.
- Confirm whether import attributes, package conditions, top-level await, JSON modules, extension rules, and CommonJS interop match the selected modes.

After configuration changes, inspect `tsc --showConfig` and trace representative module resolution when behavior is unclear.

## 4. ESM and CommonJS are runtime contracts

Determine module format from the complete contract:

- Package `type`.
- `.js`, `.mjs`, `.cjs`, `.ts`, `.mts`, and `.cts` extensions.
- TypeScript `module` and emit behavior.
- Package export conditions.
- Runtime loader and version.
- Test runner, bundler, framework, and code generator behavior.
- Whether consumers use `import`, dynamic `import()`, or `require`.

Do not infer module format from source syntax alone. TypeScript can parse `import` syntax under configurations that emit or load differently.

### Node-style ESM

Review:

- Required relative file extensions in emitted/runtime imports.
- URL-based module identity and `import.meta` APIs.
- Lack of CommonJS globals unless deliberately recreated.
- JSON/Wasm import rules and attributes for the supported runtime.
- Directory imports and package main/index assumptions.
- Top-level await and its effect on dependency initialization.
- Dynamic import behavior from CommonJS callers.

Do not append `.ts` to runtime imports unless the runtime/build pipeline explicitly supports and preserves that contract. Many emitted-JavaScript projects should author the extension that exists after emit.

### CommonJS

Review:

- `module.exports` versus `exports` mutation.
- Synthetic/default import behavior and helper emission.
- Cyclic initialization and partially initialized exports.
- `require` cache identity.
- Dynamic loading and conditional require behavior.
- Whether ESM-only dependencies can be consumed.

Do not enable interop options merely to silence an import error without testing the emitted runtime behavior.

## 5. Dual-package hazards

Publishing both ESM and CommonJS increases compatibility surface:

- One logical package may be loaded twice, producing duplicate singletons, symbols, contexts, class identities, caches, or registries.
- Default/named export shapes can differ between loaders and transpilers.
- Types can resolve to a declaration that does not match the runtime condition.
- Relative specifiers and file extensions can differ.
- Bundlers may select different conditions from direct runtimes.
- Deep imports can bypass the intended condition map.

Prefer one format when consumer requirements allow it. When dual output is required:

- Define explicit export conditions and declaration routing.
- Preserve one public API shape.
- Test installed tarballs from representative ESM and CommonJS consumers.
- Test `instanceof`, singleton/token identity, side effects, and default/named access when relevant.
- Avoid sharing mutable state through two independently evaluated entry graphs.

## 6. Package exports and conditions

Treat `exports` as a public API and compatibility boundary.

- Export only supported root and subpaths.
- Keep runtime and declaration paths aligned.
- Include `import`, `require`, `types`, browser, development, production, or platform conditions only when the package genuinely supports them.
- Understand condition priority and how supported consumers select conditions.
- Do not publish source-only paths that require the consumer to understand the monorepo's transpilation settings unless that is deliberate.
- Prevent accidental deep imports if internal layout may change.
- Verify package contents contain every referenced file.
- Test self-references and package `imports` aliases under the actual runtime.

A condition map that works in one bundler can still fail in Node.js, a test runner, or another bundler.

## 7. TypeScript path mapping

`baseUrl`/`paths` or equivalent aliases primarily inform compile-time resolution. They generally do not rewrite emitted import specifiers.

Before adding an alias, identify how runtime resolution is provided:

- Bundler alias.
- Package `imports` or workspace package exports.
- Runtime loader/hook.
- Framework resolver.
- Test-runner mapping.
- Code-generation transformation.

Keep all relevant systems aligned. Prefer real package/subpath boundaries or platform-native imports when they simplify the complete toolchain.

Reject aliases that:

- Work only in the editor.
- Point across package internals and bypass public exports.
- Create duplicate module identity through two specifiers.
- Leak monorepo source paths into declarations.
- Require production-only loader magic that tests do not exercise.
- Obscure browser/server boundaries.

## 8. Import and export hygiene

- Use type-only imports/exports when the compiler/transpiler needs them to erase runtime edges correctly or repository policy requires them.
- Do not rely on TypeScript to infer away imports when another transpiler processes one file at a time.
- Preserve side-effect imports deliberately. If side-effect import checking is enabled, fix missing or misspelled modules rather than suppressing them broadly.
- Avoid barrel-induced cycles and eager module initialization.
- Keep import specifiers stable across source, emitted files, and package exports.
- Do not use namespace imports, default imports, or synthetic defaults based only on what one transpiler accepts; verify runtime shape.
- Remember that importing a type from a package can still affect dependency/declaration requirements even when no runtime import is emitted.

## 9. Circular dependencies and initialization

Module cycles are legal in many environments but can expose partially initialized exports and ordering-sensitive side effects.

Review cycles for:

- Top-level reads before the exporting module initializes a binding.
- Class inheritance from an uninitialized value.
- Decorator or metadata evaluation order.
- Registration side effects.
- Singletons whose construction depends on the cycle.
- CommonJS snapshots versus ESM live bindings.
- Barrel files that create a cycle absent in direct imports.

Prefer breaking cycles through dependency direction, extracting a small stable contract, moving composition to a higher layer, or delaying a runtime lookup deliberately. Do not create an interface package solely to hide every cycle; fix the ownership boundary.

## 10. Ambient types and globals

`types`, `typeRoots`, and `lib` control what ambient declarations are visible. Frameworks and test tools can also inject globals.

Rules:

- Include only environment types the project actually owns.
- Keep Node.js globals out of browser-only projects and DOM globals out of server/worker projects when they create false compatibility.
- Separate test-only globals from production compilation.
- Do not fix missing globals by adding broad `types` packages to the root config without checking every project.
- Prefer explicit imports over test/framework globals when repository convention values isolation.
- Treat declaration conflicts as an environment/configuration problem; do not hide them with blanket `skipLibCheck`.
- Verify lib/API support against the runtime, not merely the available declaration version.

A type definition can describe a newer API than the supported runtime implements. Add polyfills or guards deliberately and test them.

## 11. Node.js-specific boundaries

For Node.js code, inspect:

- Supported Node versions and corresponding syntax/API availability.
- Event-loop and stream semantics.
- Filesystem paths versus file URLs.
- Process signals, exit behavior, unhandled rejections, and shutdown.
- `worker_threads`, child processes, native addons, and thread/process ownership.
- Package exports, ESM/CommonJS loader behavior, and module cache identity.
- Environment variables, permissions, current working directory, and executable lookup.
- HTTP client/server limits, proxy behavior, TLS, and DNS assumptions.

Do not use `process.exit()` in ordinary library or cleanup paths; it can skip pending output and cleanup. Set exit status and let owned shutdown finish unless immediate termination is the explicit contract.

### Native TypeScript execution/type stripping

Some runtimes can execute TypeScript source by removing erasable syntax. This is not equivalent to a full compiler transform.

- Verify the exact runtime version and supported syntax.
- Use the repository's compatibility option, such as erasable-syntax checking, when adopted.
- Avoid syntax requiring transformation—such as some enums, namespaces, parameter properties, or legacy decorator behavior—unless the runtime explicitly supports it.
- Confirm import extensions and package resolution for `.ts` source.
- Remember that type stripping does not perform type-checking.
- Keep production validation in CI even when local source executes directly.

Do not switch an emitted project to direct source execution incidentally.

## 12. Bun and Deno

Treat Bun and Deno as distinct runtimes, not interchangeable “Node-compatible” replacements.

For either runtime, verify:

- Exact supported version and API compatibility.
- Module/package resolution and TypeScript handling.
- Lockfile and dependency-source policy.
- Node compatibility layer behavior where used.
- Permission/security model.
- Test runner, bundler, package scripts, and workspace behavior.
- Native addon and subprocess support.
- Deployment target behavior versus local development.

Do not change the runtime to simplify tooling without testing all platform, dependency, and operational contracts.

## 13. Browser targets

Browser type-checking and transpilation must match supported users:

- Define the browser/version target from product policy and telemetry, not personal preference.
- Separate syntax transpilation from API polyfills.
- Ensure bundler target, TypeScript target, CSS processing, and test browsers are coherent.
- Do not assume a DOM declaration means the browser supports the API.
- Use feature detection or controlled polyfills when required.
- Account for module scripts, cross-origin loading, CSP, import maps, service workers, and cache behavior.
- Keep server-only modules, credentials, and filesystem/process assumptions out of client bundles.

Test critical behavior in actual supported browser engines, not only a DOM emulator.

## 14. Web Workers, service workers, and edge runtimes

These environments differ from both browsers and Node.js:

- Global scope and available DOM APIs differ.
- Lifecycle can be event-driven and termination can occur between operations.
- Persistent connections, background timers, filesystem access, native modules, and process APIs may be unavailable.
- CPU time, memory, request body, subrequest, and execution duration may be constrained.
- Streams and fetch behavior can be platform-specific.
- Service workers have installation/activation/cache versioning contracts.

Use environment-specific `lib` and types. Do not include both DOM window and worker globals merely to silence errors. Test deployment artifacts in the representative platform or emulator.

## 15. Electron and multi-context applications

Electron commonly has at least main, preload, and renderer contracts.

- Keep Node privileges out of renderers unless explicitly required.
- Use a narrow, validated preload bridge rather than exposing broad process or filesystem APIs.
- Validate IPC messages and authorize operations in the privileged process.
- Use separate tsconfigs/types/bundles for main, preload, and renderer when environments differ.
- Define object serialization and error mapping across IPC.
- Treat navigation, external URL opening, webviews, and remote content as security boundaries.
- Ensure packaging includes correct native modules and platform artifacts.

TypeScript visibility does not secure an IPC surface.

## 16. Paths, URLs, and platform semantics

- Use filesystem path APIs for local paths and URL APIs for URLs; do not concatenate either manually when semantics matter.
- Preserve Windows drive, UNC, case-sensitivity, separator, reserved-name, and symlink behavior where supported.
- Do not convert arbitrary paths to URLs or back without using platform APIs.
- Treat current working directory as configuration, not a stable module location.
- Resolve packaged assets relative to the correct runtime artifact, not source-tree assumptions.
- Test case-sensitive production filesystems when development is case-insensitive.
- Avoid imports whose casing differs from the file name.

## 17. Source maps and stack traces

- Decide whether source maps are for local debugging, production observability, package consumers, or browser devtools.
- Ensure paths map to files available in the intended environment without exposing sensitive source unexpectedly.
- Upload private source maps to observability tooling when public distribution is not acceptable.
- Preserve source-map chaining through TypeScript, transpiler, bundler, minifier, and instrumentation stages.
- Validate stack traces from the deployed artifact.
- Avoid relying on exact stack formatting as a stable API.

## 18. Platform verification matrix

For each supported environment, decide which evidence is required:

- Type-check under the environment's config and ambient types.
- Build/bundle for the real target.
- Execute the built artifact or packed package.
- Run native tests on supported operating systems.
- Run browser tests in required engines.
- Run worker/edge/serverless integration tests in representative tooling.
- Test ESM and CommonJS consumers if both are promised.
- Test path, signal, filesystem, URL, and case behavior where platform-specific.

Cross-compilation or bundling proves artifact creation, not runtime semantics.

## Runtime completion checklist

- Checker, emitter, loader, and deployment responsibilities are explicit.
- `module`, resolution, package type, extensions, and exports agree.
- Aliases resolve in every actual runtime and test path.
- Ambient types match each execution environment.
- ESM/CommonJS identity and interop behavior are tested where promised.
- Browser, worker, server, and privileged contexts remain separated.
- Platform-specific paths, URLs, globals, and lifecycle assumptions are verified.
- The packaged/deployed artifact—not only source—has been exercised.
