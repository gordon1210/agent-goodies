# Security, Content, and Dependencies

Read this reference when code handles untrusted content, authentication, authorization, mutations, browser capabilities, server rendering, React Server Components, third-party scripts, package changes, secrets, or multi-tenant data. React prevents some classes of accidental DOM injection, but it is not a complete security boundary.

## 1. Establish the threat model

Before changing security-sensitive code, identify:

- trust levels of users, tenants, administrators, APIs, files, and third parties;
- browser, server, edge, worker, and build-time execution boundaries;
- authentication and authorization decisions;
- data classified as public, internal, personal, credential, or secret;
- mutation endpoints and anti-automation controls;
- persisted or rendered rich content;
- server-rendered or RSC payloads crossing to the client;
- package managers, registries, build plugins, code generators, and install scripts;
- CSP, Trusted Types, iframe, origin, and deployment assumptions.

Do not describe a component as safe merely because it uses React. Trace the complete path from untrusted source to security-relevant sink.

## 2. JSX escaping: useful but contextual

React escapes primitive values rendered as JSX text and attribute values. This protects the ordinary pattern:

```tsx
<p>{comment.body}</p>
```

It does not establish that the same value is safe for:

- raw HTML insertion;
- a URL with an unsafe scheme or destination;
- a CSS value with security or UI-redress implications;
- script, JSON, or inline bootstrap serialization;
- an iframe `srcDoc` document;
- a command, database query, header, path, or server template outside React;
- third-party components that interpret strings as markup or code.

Review the final sink, not only the JSX expression.

## 3. Raw HTML and rich content

Treat `dangerouslySetInnerHTML`, direct `innerHTML`, `outerHTML`, `insertAdjacentHTML`, and HTML-producing library APIs as explicit security boundaries.

For untrusted rich content:

1. Define the exact supported markup and URL policy.
2. Use an established sanitizer configured for that policy.
3. Sanitize at a clear boundary and preserve a trusted representation.
4. Test event handlers, scriptable URLs, SVG/MathML, malformed markup, encoded payloads, and parser differentials.
5. Re-sanitize when policy or sanitizer semantics change.

Do not build a sanitizer from regular expressions or a hand-maintained tag blacklist. Escaping HTML is not equivalent to preserving safe rich HTML.

When Trusted Types is part of the deployment policy, integrate the sanitizer with an explicit policy and keep bypass creation narrowly scoped. Trusted Types can constrain DOM XSS sinks; it does not validate business authorization or make arbitrary content benign.

## 4. Markdown, MDX, syntax highlighting, and editors

Determine whether the renderer permits raw HTML, executable components, custom protocols, embedded media, or plugin transforms.

- Disable raw HTML unless the product requires it.
- Sanitize generated HTML even when the source format appears restricted.
- Treat MDX or component-capable content as code, not ordinary user text.
- Review plugins as executable dependencies.
- Validate link and image destinations.
- Keep preview and production rendering policies identical.
- Prevent privileged users from unintentionally publishing content with broader execution rights than intended.

A Markdown parser is not automatically an HTML sanitizer.

## 5. URLs and navigation

Validate untrusted values used in `href`, `src`, `action`, `formAction`, redirects, `window.open`, router navigation, CSS URLs, iframe URLs, or resource hints.

Prefer:

- parsing with `URL` against an explicit base;
- allowlisting schemes appropriate to the feature;
- allowlisting origins or hosts where external navigation is constrained;
- normalizing before comparison;
- generating internal destinations from route identifiers rather than accepting arbitrary URLs;
- adding `noopener` behavior for untrusted new-window navigation where the browser/framework does not already guarantee it.

Reject or explicitly handle scriptable, data-bearing, credential-bearing, protocol-relative, encoded, and mixed-origin forms according to policy. Do not validate a URL with a substring, suffix-only host check, or regex that ignores parser behavior.

An open redirect, phishing destination, cross-tenant resource URL, or unsafe form target remains a defect even when React rendered the attribute safely.

## 6. Style, SVG, and custom elements

React style objects avoid concatenating an HTML `style` attribute, but arbitrary CSS values can still:

- obscure security-relevant UI;
- create deceptive overlays;
- trigger external resource requests in supported properties;
- leak or expose information through product-specific behavior;
- make content unusable or inaccessible.

Allow only expected properties and constrained values when users control styling.

Treat untrusted SVG as active rich content. SVG can contain links, external resources, animation, foreign content, and browser-sensitive features. Sanitize it with an SVG-aware policy or rasterize it in an isolated service when the product does not require editable SVG.

Custom elements and third-party web components may interpret attributes or properties differently from React. Review their contract rather than assuming ordinary DOM semantics.

## 7. Prop spreading and configuration-driven UI

Spreading trusted component props is not inherently unsafe. Spreading untrusted or overly broad configuration can expose behaviors the schema did not intend:

```tsx
<button {...remoteConfig} />
```

Possible consequences include unexpected navigation, form submission, focus behavior, DOM identifiers, accessibility corruption, resource loading, or data exposure through downstream components.

Define and validate a narrow schema. Map validated fields to explicit props. Do not pass arbitrary server JSON through a component tree because it is “just props.”

JSON cannot create JavaScript event-handler functions by itself, but a configuration system may select registered handlers, components, templates, or commands. Review that indirection as executable behavior.

## 8. Client code is public code

Assume users can inspect, alter, replay, and call everything shipped to the browser.

Never rely on client code for:

- authorization;
- price or entitlement enforcement;
- tenant isolation;
- anti-fraud decisions;
- secret storage;
- integrity of submitted values;
- rate-limit enforcement;
- hiding an endpoint or feature as a security control.

Client-side guards improve UX. The server must independently authenticate, authorize, validate, and enforce invariants on every relevant entry path.

## 9. Environment variables and secrets

Inspect the framework's public/private environment-variable rules. Values embedded in a client bundle, HTML, source map, RSC payload, hydration data, or network request are not secrets.

- Keep credentials and private tokens server-only.
- Never expose a privileged API key to avoid implementing a server boundary.
- Treat build logs, preview deployments, error overlays, and source maps as potential disclosure paths.
- Rotate credentials that were committed or deployed; removing them from current code is insufficient.
- Do not log environment objects or authorization headers during debugging.

A name such as `SECRET`, `PRIVATE`, or `SERVER_ONLY` has no effect unless the build/runtime enforces the boundary.

## 10. Authentication and authorization

For every protected read or mutation, verify:

1. Authentication source and session validity.
2. Authorization for the specific resource and action.
3. Tenant or organization scope.
4. Object ownership and indirect identifiers.
5. Field-level restrictions where applicable.
6. Revalidation after state changes or long-lived interactions.
7. Error behavior that does not disclose unauthorized existence unnecessarily.

Do not authorize solely when rendering a button or route. Review alternate API routes, Server Functions, form actions, loaders, background work, and cached paths.

Keep authorization close to the data operation or in a mandatory trusted service boundary. Convenience wrappers are useful only when all entry paths are forced through them.

## 11. Server Functions, Actions, and mutations

Treat a callable Server Function, action, route handler, or mutation endpoint as a public network entry point even when the framework generates the transport.

Require as applicable:

- authentication and action-specific authorization;
- schema validation and canonicalization;
- CSRF/origin protections consistent with session transport and framework behavior;
- idempotency for retried or duplicate submissions;
- transaction boundaries and rollback behavior;
- optimistic-UI reconciliation with authoritative results;
- rate, size, and concurrency limits;
- audit logging without sensitive payload leakage;
- safe error mapping.

A closure over a user or resource does not prove the caller is still authorized when the function executes.

## 12. CSRF and origin assumptions

Cookie-authenticated state changes may require CSRF protection. Determine the actual session mechanism, SameSite policy, browser support, framework protections, alternate content types, and cross-origin deployment topology.

Do not claim CSRF safety from any single control without checking the complete request path. Common controls include framework-generated action tokens, unpredictable anti-CSRF tokens, origin validation, SameSite cookies, and requiring non-simple request characteristics. Apply the framework's documented model and test bypass paths.

CORS is not a CSRF defense by itself, and CSRF protection does not replace authorization.

## 13. RSC transport and package advisories

React Server Components add a framework-integrated serialization and execution boundary. Determine whether the application or framework includes `react-server-dom-*`, Server Functions, RSC request decoding, or compatible transport packages even when application code does not import them directly.

Before approving an RSC-capable deployment:

- check current React and framework security advisories;
- identify the exact installed React, React DOM, RSC transport, and framework versions;
- verify the framework's patched-version guidance and lockfile resolution;
- inspect mixed deployment or stale-server risks;
- test that untrusted payloads cannot reach unintended module references or execution paths;
- keep edge/server variants on compatible patched releases.

Do not hardcode an old “safe version” into permanent guidance. Security fixes can be superseded by follow-up advisories.

## 14. Request isolation, caches, and multi-tenancy

SSR and RSC servers may process many users in one process. Never store request identity, permissions, locale, feature flags, or mutable response data in shared module state.

For every cache, state:

- key dimensions, including user/tenant/locale/authorization context;
- scope: render, request, process, region, deployment, or external store;
- freshness and invalidation;
- maximum size and eviction;
- whether failures or unauthorized results can be cached;
- whether data may be serialized to another trust boundary.

Per-request deduplication is not the same as a cross-request cache. A missing identity dimension can become a cross-tenant disclosure.

## 15. Serialization and server-to-client data

Only send data the client is authorized and needs to receive. Hidden DOM, non-rendered props, source maps, RSC payloads, preload state, and serialized caches are still observable.

- Project database/domain objects to explicit transport shapes.
- Avoid spreading full session, user, or ORM records into Client Components.
- Keep secrets and internal authorization metadata server-side.
- Handle dates, large integers, binary values, class instances, errors, and custom prototypes deliberately.
- Use framework-supported serialization for inline bootstrap data.
- Prevent `</script>` and parser-context breakout when generating scripts manually.
- Review error serialization and stack traces.

TypeScript privacy and omitted UI fields do not remove runtime properties from an object already sent to the browser.

## 16. Browser storage and messaging

Treat `localStorage`, `sessionStorage`, IndexedDB, Cache Storage, history state, BroadcastChannel, and service-worker messages as attacker-influenceable within the origin and persistent beyond the current render.

- Do not store long-lived high-value credentials when safer transport is available.
- Version and validate persisted schemas.
- Bound size and retention.
- Clear user-specific data on logout/account switching where required.
- Avoid assuming storage events are authenticated messages.

For `postMessage`:

- use a specific target origin whenever possible;
- verify `event.origin` and, where needed, `event.source`;
- validate message schema and operation authorization;
- avoid passing secrets to broad or untrusted origins;
- treat transferred ports and objects as capabilities.

## 17. Browser capabilities and user activation

Clipboard, fullscreen, camera, microphone, geolocation, notifications, file-system access, downloads, popups, and payments cross privacy or security boundaries.

- Request the minimum permission at the moment the user expects it.
- Preserve required user activation through the real event path.
- Explain failure and denial states without coercive loops.
- Release streams, object URLs, workers, and device resources.
- Validate file type by content and policy on the server; the browser `accept` attribute is only a picker hint.
- Never treat a client-side file scan as the sole protection for uploads.

## 18. Third-party scripts, widgets, and iframes

A third-party script in the page typically has the origin's effective DOM and data access. Review necessity, ownership, data collection, update mechanism, CSP impact, availability, and failure behavior.

Prefer, where compatible:

- delaying non-critical scripts until after useful content or consent;
- sandboxed iframes with the minimum capabilities;
- explicit `allow`/Permissions Policy;
- constrained `postMessage` contracts;
- CSP nonces or hashes generated according to deployment architecture;
- Subresource Integrity for immutable cross-origin assets;
- self-hosting only when update and license obligations are understood.

Do not add `unsafe-inline` or broad origins to make one integration work without reviewing the resulting boundary.

## 19. Content Security Policy and Trusted Types

CSP is defense in depth and deployment policy, not a substitute for fixing injection.

Review:

- nonce/hash generation and propagation through SSR and streaming;
- script/style requirements of the framework and third parties;
- `connect-src`, `img-src`, `font-src`, `frame-src`, `worker-src`, and form/navigation restrictions;
- report-only rollout and violation telemetry privacy;
- development exceptions that must not reach production;
- Trusted Types compatibility for DOM sinks.

Do not copy a generic CSP without testing the actual production document, streamed content, hydration, route transitions, and error pages.

## 20. Dependency and supply-chain review

A package addition or update can execute code at install, build, test, development, and runtime.

Before adding or materially upgrading a dependency, inspect:

- exact package and registry/source identity;
- maintainers, ownership changes, release history, and maintenance state;
- advisories and known compromises;
- license and organizational policy;
- package contents, exports, and provenance where available;
- lifecycle scripts, native code, downloaded binaries, and code generation;
- transitive dependencies and optional/default features;
- peer ranges for React and React DOM;
- browser/server bundle impact;
- supported runtimes, browsers, module formats, and TypeScript versions;
- lockfile and workspace effects.

Do not add a dependency merely to avoid a small clear implementation. Do not hand-roll a sanitizer, parser, cryptographic primitive, or security protocol merely to avoid a dependency.

## 21. Untrusted repositories and package commands

Do not run install, build, test, lint, dev-server, Storybook, code-generation, package-manager, or framework commands in an untrusted repository until execution risks are understood and an appropriate sandbox is available.

Static inspection should include:

- root and workspace manifests;
- lifecycle scripts and shell commands;
- package-manager hooks and configuration;
- build plugins and custom loaders;
- executable config files;
- native addons and downloaded binaries;
- Git dependencies, patched packages, and registry overrides;
- test setup and browser automation hooks;
- container and CI definitions.

A `lint` or `test` script is arbitrary code. Script names do not confer safety.

## 22. Build-time and development-server boundaries

Vite, webpack, Rspack, Rollup, Babel, SWC, TypeScript plugins, framework config, Storybook addons, test runners, and React Compiler integrations execute trusted code during development or build.

- Keep development servers bound and exposed according to policy.
- Do not proxy arbitrary destinations without SSRF controls.
- Protect source maps, environment endpoints, and debug overlays.
- Review plugins before enabling them.
- Pin or constrain critical build dependencies according to repository policy.
- Avoid evaluating remote configuration as JavaScript.

A build-only dependency can still compromise credentials, source code, release artifacts, or CI runners.

## 23. Logging, errors, and privacy

Do not expose or retain:

- access/refresh tokens, cookies, authorization headers, or API keys;
- full form submissions or uploaded content by default;
- sensitive URL/query values;
- raw server errors or stack traces to untrusted clients;
- cross-tenant identifiers without need;
- personal data in analytics dimensions or metric labels.

Use structured error categories and request/trace identifiers. Redact at the boundary rather than relying on every log caller. Ensure client observability SDKs collect only approved data and cannot read sensitive DOM/input content by default.

## 24. Resource exhaustion and abuse

React applications can expose expensive rendering, parsing, query, upload, export, preview, or mutation paths.

Bound as applicable:

- request and upload size;
- rich-text/Markdown nesting and expansion;
- image dimensions and decompression;
- list/filter result size;
- server render time and memory;
- concurrent actions and background work;
- retries, optimistic queues, and client caches;
- RSC payload and serialization size;
- third-party requests;
- regex and parser complexity.

Client-side limits improve responsiveness but are not enforcement. Apply authoritative limits at trusted server boundaries.

## 25. Security testing

Test the behavior that establishes the boundary:

- unauthorized and cross-tenant reads/mutations;
- alternate entry paths and direct action invocation;
- malformed, oversized, duplicate, and replayed submissions;
- rich-content payloads and sanitizer policy;
- unsafe URL schemes and redirect forms;
- serialization leakage;
- cache key isolation;
- CSRF/origin controls;
- CSP/Trusted Types in a production-like document;
- dependency and advisory policy in CI where established;
- stale/mixed deployment behavior for server protocols.

A snapshot of escaped markup is not sufficient evidence for a complete XSS policy. Automated scanners complement, but do not replace, data-flow and authorization review.

## 26. Common false positives

Do not report these without a concrete unsafe path:

- Rendering an untrusted string through ordinary JSX text.
- Spreading a statically typed, trusted internal prop object.
- Using `localStorage` for non-sensitive, versioned user preferences.
- Opening a fixed trusted URL in a new tab where opener behavior is already constrained.
- A package has lifecycle-script capability but the installed package executes no relevant script.
- A Client Component receives public display data.
- A server cache exists and its key/scope demonstrably includes every security dimension.
- CSP permits a source intentionally required by a reviewed integration.

Security review should reduce credible risk, not label every browser API as a vulnerability.

## 27. Common critical failures

Escalate based on actual reachability and impact, including:

- server-side authorization missing on a protected read or mutation;
- cross-tenant cache or serialization leakage;
- attacker-controlled raw HTML reaching an executable DOM context;
- privileged secrets bundled to the client;
- arbitrary code or module execution through a server/RSC boundary;
- install/build compromise in a trusted release environment;
- unrestricted file, URL, proxy, or command behavior crossing a server boundary;
- persistent injection affecting privileged users.

Do not assign critical severity from a rule name alone. Demonstrate the trigger, boundary bypass, and plausible impact.

## 28. Security completion gate

Before completing a security-sensitive change or review, confirm:

- Trust, execution, and data boundaries were mapped.
- Client checks are backed by trusted-server enforcement.
- Content reaches only context-appropriate safe sinks.
- URLs, serialization, storage, and messaging follow explicit policies.
- SSR/RSC state and caches preserve request/tenant isolation.
- Mutations include authentication, authorization, validation, and replay/CSRF controls as applicable.
- Exact installed packages and current advisories were checked where material.
- Build and dependency execution risk was considered.
- Sensitive telemetry and error paths were reviewed.
- Negative tests exercise the actual boundary.
- Remaining assumptions and deployment dependencies are stated.
