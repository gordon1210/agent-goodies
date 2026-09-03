# Security, Dependencies, and Supply Chain

Read this reference for untrusted input, authorization, tenancy, browser and server security, filesystem/process/network boundaries, secrets, denial-of-service resistance, dependencies, package lifecycle scripts, native addons, build tooling, and security review.

## 1. Define the trust boundary

Before implementing security-sensitive behavior, identify:

- Which data is attacker-controlled, tenant-controlled, user-controlled, administrator-controlled, third-party-controlled, or merely malformed by accident.
- Which operations cross browser/server, process, worker, network, filesystem, database, privilege, native-code, or package/build boundaries.
- Which resources an attacker can cause the system to consume.
- Which identity, role, tenant, ownership, and delegation rules apply.
- Which data is confidential, integrity-sensitive, regulated, security-relevant, or safe for client exposure.
- What happens after partial failure, retry, restart, duplicate delivery, or concurrent execution.
- Which assumptions are enforced at runtime versus represented only in TypeScript.

Validate and authorize at the boundary closest to the protected resource. Convert external data to a validated internal representation. Do not repeatedly cast/reinterpret raw values throughout the codebase.

## 2. Types are not security controls

Reject security claims based only on:

- A type annotation, interface, generic parameter, or branded primitive.
- `private`/`protected` members.
- A type assertion after parsing.
- A generated API type without runtime validation.
- An enum or union whose discriminant came from untrusted input.
- A client-side permission check.
- A hidden UI control.
- A package declared as “internal.”

Runtime validation, server-side authorization, deployment isolation, and cryptographic verification must enforce the actual boundary.

## 3. Input validation and resource limits

Validation must cover meaning and cost.

Check as applicable:

- String/byte length, item count, nesting depth, recursion, and aggregate decoded size.
- Numeric range, precision, `NaN`, infinities, signedness, allocation calculations, and bigint/number conversion.
- Encoding, Unicode normalization, confusable identifiers, case folding, duplicate fields, unknown fields, and canonical form.
- Object prototype, inherited properties, accessors, symbols, and dangerous property names.
- URL scheme, host, port, credentials, fragments, redirects, DNS behavior, and destination policy.
- Path roots, traversal, symlinks, case sensitivity, reserved names, race windows, and platform behavior.
- Archive entry count, expansion ratio, nested archives, links, absolute paths, and extraction destination.
- Regex/parser/algorithmic complexity.
- Request body, multipart file, decompression, image/media dimension, and upload limits.
- Database query cardinality, pagination, sort/filter complexity, and batch size.
- Concurrent work, retries, queued work, worker/process count, and retained results.

Do not allocate or spawn directly from an untrusted declared size/count without a verified upper bound.

## 4. Objects, records, and prototype hazards

Plain objects inherit behavior unless created or handled deliberately.

When untrusted strings become keys:

- Use own-property checks rather than trusting `in` when inherited properties are not valid.
- Reject or safely handle keys such as prototype-related names according to the operation.
- Avoid recursively merging untrusted objects into configuration, options, class instances, or privileged state.
- Prefer `Map`, a null-prototype dictionary, or explicit finite keys when semantics fit.
- Do not invoke getters or proxy traps unintentionally during validation, copying, logging, or serialization.
- Bound key count and recursion.
- Avoid spreading hostile objects into trusted options without a whitelist.

`Record<string, T>` is a static shape, not a runtime guarantee about ownership, safe keys, or presence.

## 5. Parsing and serialization

- Treat parsing as structural conversion, not complete validation.
- Validate semantic invariants after JSON, form, query, YAML, XML, CSV, binary, or framework parsing.
- Configure parser limits and safe schema/features.
- Avoid formats/features capable of constructing arbitrary objects or executing code.
- Define duplicate-key and unknown-field behavior deliberately.
- Keep versioned wire/storage schemas and reject unsupported versions safely.
- Do not deserialize directly into privileged class instances or invoke constructors/methods from untrusted type names.
- Avoid dynamic module/function resolution from untrusted discriminator values.
- Keep error messages bounded and do not echo entire hostile payloads.

JavaScript JSON behavior for bigint, dates, undefined, non-finite numbers, maps, sets, prototypes, and precision must be handled explicitly at the contract boundary.

## 6. Filesystem safety

- Treat path validation and file opening as one security-sensitive operation; a path can change between checks and use.
- Resolve paths against an explicit allowed root and define symlink policy.
- Canonicalization alone is not a complete traversal defense, especially for nonexistent paths and mutable trees.
- Prefer capability-style directory handles or safe platform APIs when race resistance matters.
- Avoid string-prefix containment checks that ignore separator, case, encoding, or normalization semantics.
- Create temporary files/directories through secure APIs; do not guess names.
- Set sensitive permissions explicitly and account for platform differences.
- Use atomic replace patterns for state/configuration writes where partial files are unacceptable.
- Bound file size, file count, directory traversal, archive extraction, and open handles.
- Avoid following links during recursive delete/copy unless explicitly safe.
- Do not serve arbitrary files based only on a TypeScript path type or extension allowlist.

## 7. Command and process execution

- Prefer direct executable and argument-array APIs over shell strings.
- Never concatenate untrusted input into a shell command.
- Treat executable lookup through `PATH`, current directory, extensions, environment, and working directory as part of the trust model.
- Use an explicit executable path and environment allowlist for privileged or sensitive subprocesses.
- Bound runtime, stdin, stdout, stderr, process count, and child tree size.
- Define signal/termination behavior for the process tree, not only the immediate child.
- Distinguish spawn failure, nonzero exit, timeout, signal termination, and output limit.
- Do not expose secrets in command-line arguments when safer channels exist.
- Treat scripts, package binaries, build tools, and interpreters as arbitrary code.

Escaping is shell-specific and brittle; avoid the shell boundary entirely when possible.

## 8. Network and SSRF boundaries

When users influence destinations:

- Allow only required schemes.
- Parse with a URL implementation rather than string concatenation.
- Validate hostname, port, credentials, and destination policy.
- Revalidate every redirect target and bound redirects.
- Account for DNS rebinding, multiple addresses, IPv4/IPv6 forms, encoded addresses, private/link-local/loopback ranges, and cloud metadata according to threat model.
- Ensure the actual connected address remains within policy; pre-resolution string checks may be insufficient.
- Bound connect, read, write, idle, and total time.
- Bound headers, response bodies, decompressed content, and concurrent requests.
- Configure proxy behavior deliberately; environment proxies can alter routing.
- Verify TLS identities and never disable certificate validation outside controlled tests.
- Prevent credential forwarding to redirected or cross-origin destinations.

A URL type or allowlisted hostname string alone is not a complete SSRF defense.

## 9. HTTP and protocol safety

- Limit request line, header count/size, body size, frame size, message count, and decompressed size.
- Validate content type and encoding before interpretation.
- Handle partial reads/writes and aborted connections.
- Prevent request smuggling ambiguities by relying on maintained servers/proxies and consistent parsing.
- Use explicit idempotency and retry semantics.
- Validate WebSocket/SSE/message frames and bound connection count and queueing.
- Do not trust forwarding headers unless they come from an authenticated proxy chain.
- Define CORS as a browser read policy, not authentication.
- Avoid reflecting untrusted headers or error text into responses without encoding and policy.

## 10. Authentication, authorization, and tenancy

Authentication establishes identity. Authorization decides whether that identity may perform a concrete operation on a concrete resource.

- Enforce authorization server-side and close to the data mutation/read.
- Include tenant/owner scope in database queries and updates, not as a later filter.
- Do not rely on identifiers being unguessable.
- Check indirect object relationships and nested resources.
- Recheck authorization after relevant state changes and before committing sensitive operations.
- Keep administrative/service credentials scoped to required operations.
- Distinguish unauthenticated, unauthorized, not-found, and conflict responses according to disclosure policy.
- Treat cached authorization decisions and role/tenant context as invalidatable security state.
- Audit sensitive operations with structured, tamper-aware events that omit secrets.
- Prevent confused-deputy behavior when acting on behalf of another identity/service.

Client-side types, route guards, hidden buttons, and generated clients do not enforce authorization.

## 11. Sessions, cookies, CSRF, and tokens

As applicable:

- Use secure, HTTP-only, appropriately scoped cookies for session material.
- Choose SameSite policy based on actual cross-site flows and add CSRF protection where cookie-authenticated state changes remain possible.
- Rotate/revoke sessions according to account and privilege changes.
- Validate token issuer, audience, signature/algorithm, expiration, not-before, nonce/state, and key rotation as required.
- Do not decode a signed token and treat it as verified.
- Avoid placing sensitive tokens in URLs, logs, local storage, analytics, or referrers.
- Keep refresh-token and access-token lifecycles distinct.
- Bound login/reset/invitation attempts and avoid account-enumeration leakage according to policy.
- Use established protocol libraries; do not implement OAuth/OIDC/JWT/PAKE/session cryptography from scratch.

## 12. Browser injection and DOM safety

Treat these as security-sensitive sinks:

- HTML insertion and template bypass APIs.
- Script, style, CSS, URL, navigation, iframe, SVG, and event-handler contexts.
- DOM clobbering and named element access.
- Dynamic code execution such as `eval`, `Function`, and string-based timers.
- Markdown/HTML rendering and rich text.
- postMessage and extension/native bridges.

Rules:

- Prefer framework escaping and text APIs.
- Use an established sanitizer configured for the exact context when rich HTML is required.
- Do not trust a type alias/brand unless construction is controlled by verified sanitization and the sink context matches.
- Validate URLs and protocols separately from HTML sanitization.
- Use Trusted Types/CSP where adopted, but do not treat policy presence as proof all sinks are safe.
- Avoid bypass APIs and review every use.
- Validate message origin, source, schema, and authorization for cross-window/worker communication.

Encoding is context-specific. HTML escaping does not make a value safe for JavaScript, CSS, URL, or attribute contexts.

## 13. CSP, CORS, clickjacking, and browser policy

- Design CSP around actual scripts/styles/resources; avoid broad unsafe directives without documented necessity.
- Use nonces/hashes correctly and keep them request-scoped where required.
- Restrict framing with appropriate headers/policies.
- Configure CORS to exact origins, methods, headers, credentials, and caching semantics.
- Never use permissive CORS as a substitute for authentication/authorization.
- Apply referrer, permissions, MIME-sniffing, and transport policies appropriate to the application.
- Test policy in production-like builds because development tooling may require weaker behavior.

## 14. Secrets and sensitive data

- Do not hard-code or commit secrets in source, fixtures, snapshots, source maps, generated files, lockfile metadata, images, or build output.
- Keep server-only secrets out of client import graphs and hydration payloads.
- Validate build-time public variable allowlists; names alone do not prevent bundling.
- Redact authorization headers, cookies, tokens, signed URLs, credentials, private keys, and personal data from logs/errors/traces.
- Minimize secret lifetime and copies; ordinary JavaScript strings cannot be reliably zeroized.
- Separate user-facing errors from detailed internal diagnostics.
- Use secret managers or controlled files/environment according to deployment policy.
- Rotate and revoke exposed secrets; deleting them from the latest commit is not sufficient.
- Treat hashes as identifiers, not automatic anonymization.

Do not serialize whole request/config/environment objects for convenience.

## 15. Cryptography and randomness

- Use platform or established library cryptography appropriate to the environment.
- Do not invent encryption, password hashing, signatures, token formats, key derivation, or random ID schemes.
- Use cryptographically secure randomness for security-sensitive tokens.
- Do not use `Math.random()` for secrets, nonces, reset links, sessions, or unpredictable identifiers.
- Use password hashing algorithms and parameters from current platform/security policy.
- Verify authentication tags/signatures before using plaintext/claims.
- Define key identifiers, rotation, storage, algorithm agility, and failure behavior.
- Avoid exposing detailed cryptographic errors to attackers.

TypeScript's type system cannot protect key material or make comparisons constant-time.

## 16. Regex and algorithmic denial of service

- Avoid vulnerable nested/backtracking patterns on untrusted long input.
- Bound input before matching.
- Prefer simple parsers or linear-time regex engines/libraries when the risk justifies them.
- Benchmark/adversarially test suspect patterns.
- Do not assume one successful example proves complexity safety.
- Account for repeated global matching, Unicode expansion, normalization, and replacement callbacks.

Static regex scanners are useful signals but require contextual review.

## 17. Database and query safety

- Use parameterized queries or the repository's safe query builder; never concatenate untrusted SQL fragments.
- Whitelist dynamic identifiers, columns, sort direction, operators, and table names because parameters usually cannot represent syntax.
- Include authorization/tenant scope in reads and writes.
- Bound result cardinality, pagination, joins, filters, and bulk operations.
- Use transactions and concurrency controls appropriate to the invariant.
- Avoid mass assignment from untrusted objects into persistence models.
- Treat ORM/query-builder escape hatches and raw queries as elevated review points.
- Protect migration and administrative credentials from application code.
- Do not expose raw database errors or SQL in user responses.

Compile-time query types do not guarantee authorization, bounded cost, or runtime schema alignment.

## 18. Dependencies as executable code

A dependency can add:

- Runtime code with application privileges.
- Lifecycle scripts executed during install/publish.
- Native addon builds and binary downloads.
- Compiler, linter, test, bundler, framework, or codegen plugins executed during development/CI.
- Transitive packages, peer constraints, registry sources, licenses, and maintainers.
- New network/filesystem/environment behavior.
- Browser code and bundle exposure.
- Type declarations that change checking without runtime changes.

Before adding a package:

1. Confirm it is better than clear local/platform code for this problem.
2. Inspect ownership, maintenance, releases, source repository, issue/security history, and documentation.
3. Inspect package contents, exports, engines, types, module formats, and supported runtimes.
4. Review direct/transitive graph, peer dependencies, optional packages, duplicate versions, and native code.
5. Review install/lifecycle scripts and postinstall downloads.
6. Check license and source policy.
7. Assess whether its types/classes leak into public API.
8. Verify tree-shaking/side effects and client bundle impact where relevant.
9. Review the lockfile diff and integrity/source changes.
10. Add the narrowest appropriate dependency scope.

Do not add a package merely because it is popular or has many downloads. Popularity is neither maintenance nor security proof.

## 19. Package-manager and install-script safety

Installing a TypeScript project may execute arbitrary code.

For unknown repositories:

- Inspect package scripts, workspace hooks, package-manager configuration/plugins, lockfile sources, patches, overrides, native addons, and downloaded binaries first.
- Prefer an install mode that disables scripts for initial static dependency inspection when supported, while recognizing the project may not build until approved scripts run.
- Run required scripts only in an isolated disposable environment.
- Do not expose home directories, SSH agents, cloud credentials, npm tokens, signing keys, browser profiles, Docker sockets, or host package-manager caches containing credentials.
- Restrict network and filesystem access according to task needs.
- Bound CPU, memory, process count, disk, output, and time.
- Treat package binaries and config files loaded by tools as arbitrary code.

A lockfile pins content resolution; it does not make lifecycle scripts trustworthy.

## 20. Dependency vulnerabilities and audit output

Use repository-approved scanners and advisory sources, but triage findings.

For each advisory:

- Confirm the exact affected package/version and dependency path.
- Determine whether the vulnerable functionality executes in production, build, test, install, or developer environments.
- Evaluate exploitability, attacker control, privileges, and compensating controls.
- Identify a compatible fixed version or replacement.
- Review breaking changes and lockfile graph impact.
- Record temporary exceptions with owner, rationale, expiry/review condition, and scope.

Do not:

- Run forced automated fixes and accept all changes blindly.
- Ignore an advisory solely because the package is transitive or development-only; build/install compromise can still matter.
- Claim no vulnerabilities because one scanner reports none.
- Keep indefinite exceptions without ownership.

Distinguish vulnerability, malicious package, unmaintained package, deprecated package, license issue, typo-squatting risk, and informational notice.

## 21. Registry, source, and provenance policy

- Use approved registries and scoped-registry configuration.
- Avoid unpinned Git or URL dependencies; pin immutable commits when unavoidable.
- Review dependency confusion risk for internal package names/scopes.
- Protect publish credentials and enable strong account controls.
- Restrict who can publish and use provenance/signing features according to policy.
- Pin CI actions and downloaded tools where reproducibility/security requires it.
- Verify checksums/signatures for external binaries when supported.
- Generate SBOM/provenance/attestations when deployment or compliance requires them.
- Treat ownership transfer, maintainer changes, package renames, and sudden script/native additions as elevated events.

## 22. Native addons, WebAssembly, and FFI-like boundaries

Native addons and WebAssembly can bypass JavaScript memory/type assumptions or add platform-specific execution.

- Verify source, prebuilt binary provenance, supported platforms, ABI/runtime versions, and fallback behavior.
- Define ownership for buffers, handles, callbacks, threads, and cleanup.
- Validate lengths, offsets, encodings, enum values, and typed-array boundaries.
- Prevent callbacks after owning objects are disposed.
- Avoid blocking the event loop with synchronous native work.
- Treat crashes, memory corruption, and process compromise as possible impact.
- Test on actual supported platforms and architectures.
- Review install-time compilation/download behavior.

A TypeScript declaration for a native module is not a safety proof.

## 23. Code generation and build-tool trust

Generators, framework plugins, compiler transforms, linters, test runners, and bundlers execute with CI/developer privileges.

- Pin versions and review source/configuration changes.
- Restrict schema/codegen network access and verify source endpoints.
- Do not feed secrets into generators unless output handling and redaction are controlled.
- Review generated output for embedded endpoints, credentials, unsafe defaults, and over-broad clients.
- Keep output deterministic; unexpected network/time/environment dependence is a supply-chain signal.
- Sandbox untrusted schemas/plugins and avoid loading executable configuration from attacker-controlled pull requests with secrets.

## 24. Client dependencies and third-party scripts

Browser dependencies and remote scripts execute in the user's security context.

- Prefer bundled/pinned dependencies over mutable remote scripts when feasible.
- Use integrity and strict origin policy for external static resources where appropriate.
- Minimize third-party scripts and privileges.
- Prevent sensitive data from flowing to analytics/ads/widgets without explicit policy and consent requirements.
- Isolate risky content with sandboxed frames where possible.
- Review update and compromise blast radius.
- Keep API keys intended for browsers constrained by origin, operation, and quota; public client keys are not secrets.

## 25. Logging, telemetry, and error security

- Treat log fields as an output boundary requiring encoding and redaction.
- Prevent terminal/control-character and structured-log injection.
- Bound logged values and avoid raw request/response bodies by default.
- Do not use user IDs, full URLs, tokens, tenant names, or raw errors as unbounded metric labels.
- Keep trace baggage/context small and free of secrets.
- Separate security audit events from debug logs and protect integrity/access/retention.
- Ensure telemetry failure cannot block critical work indefinitely.
- Review browser telemetry for personal data, query strings, DOM content, and cross-tenant leakage.

## 26. Security testing and review

Use layered evidence according to risk:

- Unit/integration tests for validation, authorization, redaction, and limits.
- Negative tests for every sensitive endpoint/resource relationship.
- Fuzz/property tests for parsers, URLs, paths, archives, and complex validators.
- Static dependency, secret, SAST, and license checks.
- Dynamic testing against production-like configuration.
- Browser security-policy tests.
- Manual threat modeling and code review for critical flows.
- Independent review for authentication, authorization, cryptography, sandboxing, package execution, and high-impact migrations.

Passing scanners and tests does not prove absence of vulnerabilities. Preserve the threat model and explicit invariants.

## Security completion checklist

- Trust boundaries, identities, tenant scope, and attacker-controlled costs are explicit.
- Runtime validation includes semantic and resource limits.
- Object/prototype, parsing, filesystem, process, network, and database boundaries are safe where applicable.
- Browser sinks, messages, cookies/tokens, and policy headers are handled deliberately.
- Authorization is server-side and resource-scoped.
- Secrets cannot enter client bundles, logs, errors, snapshots, source maps, or generated artifacts.
- Dependencies, lockfile changes, lifecycle scripts, native code, and build tools receive supply-chain review.
- Untrusted installation/build/test execution is sandboxed.
- Security exceptions have owner, scope, and review conditions.
- Tests cover abuse, redaction, limits, partial failure, and authorization—not only valid use.
