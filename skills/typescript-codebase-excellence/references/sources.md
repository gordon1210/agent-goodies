# Primary Sources and Maintenance Notes

Last reviewed: 2026-09-03.

This skill contains derived engineering guidance rather than copied prose. Re-check primary sources whenever updating version-sensitive TypeScript, runtime, package-manager, browser, framework, security, or tooling behavior.

## Source hierarchy

When behavior is disputed, prefer:

1. The repository's exact pinned version, source, configuration, and reproducible behavior.
2. Official documentation/release notes for that exact version.
3. Language/runtime/specification text.
4. Maintainer issue/PR discussion for unresolved implementation detail.
5. Secondary sources only for orientation, never as the sole basis for version-sensitive rules.

Do not generalize from one bundler, package manager, framework, editor, or runtime to another.

## Agent Skills format

- Agent Skills specification: https://agentskills.io/specification
- Agent Skills integration and progressive disclosure: https://agentskills.io/client-implementation/adding-skills-support
- Agent Skills authoring guidance: https://agentskills.io/skill-creation/best-practices
- Reference validator: https://github.com/agentskills/agentskills/tree/main/skills-ref

## TypeScript language and compiler

- TypeScript documentation: https://www.typescriptlang.org/docs/
- TypeScript handbook: https://www.typescriptlang.org/docs/handbook/intro.html
- TSConfig reference: https://www.typescriptlang.org/tsconfig/
- TypeScript source repository: https://github.com/microsoft/TypeScript
- TypeScript releases: https://github.com/microsoft/TypeScript/releases
- TypeScript 6.0 announcement and migration details: https://devblogs.microsoft.com/typescript/announcing-typescript-6-0/
- TypeScript 7.0 announcement, side-by-side strategy, and parallel controls: https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/
- TypeScript 6/7 JavaScript and implementation differences maintained during the native port: https://github.com/microsoft/typescript-go/blob/main/CHANGES.md

## TypeScript modules, declarations, and projects

- Modules handbook: https://www.typescriptlang.org/docs/handbook/modules.html
- Module reference: https://www.typescriptlang.org/docs/handbook/modules/reference.html
- Declaration files introduction: https://www.typescriptlang.org/docs/handbook/declaration-files/introduction.html
- Declaration file publishing: https://www.typescriptlang.org/docs/handbook/declaration-files/publishing.html
- Project references: https://www.typescriptlang.org/docs/handbook/project-references.html
- TypeScript performance guidance: https://github.com/microsoft/TypeScript/wiki/Performance
- Compiler API wiki (TypeScript 6/API-era behavior; verify exact version): https://github.com/microsoft/TypeScript/wiki/Using-the-Compiler-API

## JavaScript and web specifications

- ECMAScript language specification: https://tc39.es/ecma262/
- HTML standard: https://html.spec.whatwg.org/
- DOM standard: https://dom.spec.whatwg.org/
- URL standard: https://url.spec.whatwg.org/
- Fetch standard: https://fetch.spec.whatwg.org/
- Streams standard: https://streams.spec.whatwg.org/
- Encoding standard: https://encoding.spec.whatwg.org/
- Web IDL standard: https://webidl.spec.whatwg.org/
- Content Security Policy: https://w3c.github.io/webappsec-csp/
- Trusted Types: https://w3c.github.io/trusted-types/dist/spec/
- Web Content Accessibility Guidelines 2.2: https://www.w3.org/TR/WCAG22/
- WAI-ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/

## Node.js

- Node.js API documentation: https://nodejs.org/api/
- Packages and package exports: https://nodejs.org/api/packages.html
- ECMAScript modules: https://nodejs.org/api/esm.html
- TypeScript support/type stripping: https://nodejs.org/api/typescript.html
- Process lifecycle and signals: https://nodejs.org/api/process.html
- Async context: https://nodejs.org/api/async_context.html
- Worker threads: https://nodejs.org/api/worker_threads.html
- Child processes: https://nodejs.org/api/child_process.html
- Streams: https://nodejs.org/api/stream.html
- Filesystem: https://nodejs.org/api/fs.html
- URL: https://nodejs.org/api/url.html
- Node.js security best practices: https://nodejs.org/en/learn/getting-started/security-best-practices

## Other runtimes

- Bun documentation: https://bun.sh/docs
- Deno documentation: https://docs.deno.com/

Use the exact runtime/version documentation selected by the repository. Compatibility claims and TypeScript execution behavior can change quickly.

## Package managers and package metadata

- npm package.json: https://docs.npmjs.com/cli/configuring-npm/package-json
- npm lifecycle scripts: https://docs.npmjs.com/cli/using-npm/scripts
- npm clean install: https://docs.npmjs.com/cli/commands/npm-ci
- npm security auditing: https://docs.npmjs.com/auditing-package-dependencies-for-security-vulnerabilities
- npm provenance: https://docs.npmjs.com/generating-provenance-statements
- pnpm documentation: https://pnpm.io/
- pnpm install: https://pnpm.io/cli/install
- pnpm workspaces: https://pnpm.io/workspaces
- Yarn documentation: https://yarnpkg.com/
- Yarn install: https://yarnpkg.com/cli/install
- Yarn workspaces: https://yarnpkg.com/features/workspaces
- Bun package manager: https://bun.sh/docs/pm

Verify commands against the pinned package-manager major version; lockfile and lifecycle behavior are version-sensitive.

## Linting and formatting

- ESLint documentation: https://eslint.org/docs/latest/
- typescript-eslint documentation: https://typescript-eslint.io/
- typescript-eslint dependency/version support: https://typescript-eslint.io/users/dependency-versions/
- Prettier documentation: https://prettier.io/docs/

The repository's exact parser/plugin/compiler matrix is authoritative. Do not assume latest TypeScript support from generic syntax acceptance.

## Testing and browser automation

- Node.js test runner: https://nodejs.org/api/test.html
- Vitest documentation: https://vitest.dev/guide/
- Jest documentation: https://jestjs.io/docs/getting-started
- Playwright documentation: https://playwright.dev/docs/intro
- Web Platform Tests: https://web-platform-tests.org/

Use only the test tools adopted by the repository unless adding infrastructure is explicitly justified.

## Packaging and module compatibility

- Node.js package exports: https://nodejs.org/api/packages.html#package-entry-points
- npm package contents and publishing: https://docs.npmjs.com/cli/commands/npm-pack
- npm publish: https://docs.npmjs.com/cli/commands/npm-publish
- publint: https://publint.dev/
- Are the Types Wrong?: https://arethetypeswrong.github.io/

Packaging commands can execute lifecycle scripts. Package validators complement, but do not replace, clean consumer tests.

## Data and protocol specifications

- JSON (RFC 8259): https://www.rfc-editor.org/rfc/rfc8259
- JSON Schema specification: https://json-schema.org/specification
- OpenAPI specification: https://spec.openapis.org/oas/latest.html
- GraphQL specification: https://spec.graphql.org/
- Protocol Buffers language guides: https://protobuf.dev/programming-guides/
- WHATWG MIME sniffing: https://mimesniff.spec.whatwg.org/

Use the exact dialect/specification and generator version selected by the project.

## Security guidance

- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
- OWASP Application Security Verification Standard: https://owasp.org/www-project-application-security-verification-standard/
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OWASP API Security Top 10: https://owasp.org/www-project-api-security/
- CWE: https://cwe.mitre.org/
- NIST Secure Software Development Framework: https://csrc.nist.gov/Projects/ssdf
- SLSA supply-chain framework: https://slsa.dev/spec/
- Sigstore documentation: https://docs.sigstore.dev/

Security guidance must be adapted to the actual threat model, platform, and regulatory policy.

## Observability

- OpenTelemetry specification: https://opentelemetry.io/docs/specs/otel/
- W3C Trace Context: https://www.w3.org/TR/trace-context/
- Prometheus metric and instrumentation guidance: https://prometheus.io/docs/practices/

Use the repository's telemetry stack and privacy/retention policy.

## Performance and diagnostics

- TypeScript performance wiki: https://github.com/microsoft/TypeScript/wiki/Performance
- Node.js diagnostics guides: https://nodejs.org/en/learn/diagnostics
- Chrome DevTools performance documentation: https://developer.chrome.com/docs/devtools/performance/
- Web performance specifications and metrics: https://www.w3.org/webperf/

Benchmark the exact production artifact/runtime; guidance and engine behavior change over time.

## Maintenance policy

When updating this skill:

1. Preserve repository-local policy precedence and the non-dogmatic stance.
2. Re-check the latest stable TypeScript 6 and 7 releases and whether TypeScript 7 now exposes a stable programmatic API.
3. Re-check `@typescript/typescript6` coexistence guidance and package names/binaries.
4. Re-check TypeScript 6 defaults/deprecations and TypeScript 7 hard errors against official release notes.
5. Re-check TypeScript 7 checker/builder/single-threaded controls and defaults.
6. Re-check JavaScript/JSDoc and declaration differences.
7. Re-check typescript-eslint, embedded-language frameworks, build tools, editors, and compiler-API consumers at their exact supported versions.
8. Verify package-manager commands against current major versions; remove stale examples rather than accumulating alternatives.
9. Keep optional tools optional and purpose-specific.
10. Re-run Agent Skills format/link validation and the scenarios in `EVALUATION.md`.
11. Update `metadata.version` and `metadata.last-reviewed` in `SKILL.md`.
