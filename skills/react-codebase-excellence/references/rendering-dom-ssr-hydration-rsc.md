# Rendering, DOM, SSR, Hydration, and RSC

Read this reference when changing roots, portals, DOM ownership, SSR, streaming, static rendering, hydration, React Server Components, Server Functions, document metadata, resource APIs, or request-scoped caches. React rendering modes share component semantics but have different execution, security, and compatibility boundaries.

## 1. Identify the rendering architecture

Determine which paths exist:

- client-only root;
- client root embedded into a host page;
- server-rendered HTML followed by hydration;
- streaming SSR;
- static pre-rendering;
- partial pre-rendering and resume;
- React Server Components with client islands;
- Server Functions/Actions;
- multiple roots or micro-frontends;
- framework-controlled combinations.

Do not infer RSC from SSR, or SSR from React 19. RSC and SSR solve different problems and may be combined by a framework.

## 2. Root ownership

Use `createRoot` for client-owned DOM and `hydrateRoot` when React must attach to server-rendered React HTML.

A root owns the DOM inside its container. External code should not arbitrarily remove or rewrite nodes React manages.

Keep the root handle when the host integration needs teardown:

```tsx
const root = createRoot(container);
root.render(<Widget />);

return () => {
  root.unmount();
};
```

For embedded widgets, define:

- who creates and removes the container;
- whether multiple instances can coexist;
- CSS isolation and host reset interaction;
- event, focus, and portal boundaries;
- version isolation and duplicate React risk;
- mount/update/unmount API;
- what happens if the host removes the container first.

Do not call `createRoot` repeatedly on the same container to update UI. Reuse the root and render again.

## 3. Multiple roots

Multiple roots are legitimate for incremental adoption or embedded surfaces, but they do not share one React tree.

Review:

- context does not cross roots;
- event and focus coordination may need an external owner;
- global stores require correct subscriptions;
- `useId` collisions can be prevented with consistent `identifierPrefix` when roots share a document;
- portals cannot bridge unrelated React ownership casually;
- root teardown must be explicit;
- duplicate React copies remain prohibited within each renderer relationship.

A single root is simpler when one application owns the page, but do not consolidate independent host integrations without a concrete reason.

## 4. DOM ownership and escape hatches

React may coexist with imperative DOM code at explicit boundaries.

Safe pattern:

- React owns the container element and its attributes.
- An imperative library owns children inside a dedicated ref container.
- React does not render competing children into that container.
- lifecycle setup, update, and destruction are explicit.

Avoid:

- changing React-managed children through `innerHTML`;
- moving nodes React expects in place;
- querying global DOM when a ref identifies the correct instance;
- relying on `findDOMNode`;
- mutating DOM during render;
- storing DOM nodes in serializable state.

When browser behavior can be expressed through markup, attributes, or CSS, prefer the declarative path.

## 5. Portals

A portal changes physical DOM placement while preserving React ancestry. Context and React event propagation follow the React tree.

This has consequences:

- a click in a portal can reach a React ancestor whose DOM node is elsewhere;
- outside-click detection based only on DOM containment can be wrong;
- focus and tab order follow the document, not visual layout;
- server rendering needs a deterministic portal strategy;
- event delegation and host-page listeners can interact.

For dialogs, menus, tooltips, toasts, and popovers, use the repository's accessible overlay infrastructure. `createPortal` alone does not implement the interaction pattern.

## 6. Server rendering APIs

Select the API through framework/runtime ownership:

- string rendering is simple but does not stream suspended content;
- Node streaming uses pipeable streams;
- Web Streams runtimes use readable streams;
- static pre-rendering waits for data and produces static output;
- React 19.2 resume APIs support architecture-level partial pre-rendering.

Do not replace a framework rendering pipeline with raw React DOM server APIs inside a focused feature patch.

Server rendering must define:

- status code and header timing;
- redirects and not-found behavior;
- shell and all-ready behavior;
- abort timeout/disconnect handling;
- error logging without duplicate or sensitive output;
- CSP nonce propagation;
- asset manifest and preload integration;
- request-local context and cache lifetime;
- client bundle/version compatibility.

## 7. Server render purity and request isolation

Server rendering may run concurrently for different requests in one process. Never store request identity, authorization, locale, tenant, draft, or response state in mutable module variables.

Module-level immutable configuration can be safe. Module-level caches require an explicit cross-request policy and keys that include every relevant identity dimension.

Rendering can be restarted, aborted, or retried. Do not perform irreversible writes during render. Mutations belong in explicit server actions, route handlers, or service boundaries.

## 8. Hydration contract

Hydration requires the client's initial rendered output to match the server HTML structurally and semantically.

Common mismatch sources:

- current time, random values, generated IDs, locale, or timezone differences;
- browser-only branches such as `typeof window !== 'undefined'` in rendered output;
- data changing between server render and client boot;
- invalid HTML nesting corrected differently by the browser;
- extension or CDN rewriting;
- inconsistent CSS-in-JS insertion order;
- missing serialized state;
- different feature flags, auth, or experiments;
- malformed table or form markup;
- client code using a different component/version bundle.

Fix the source. `suppressHydrationWarning` is a narrow one-level escape hatch for known unavoidable differences, not a repair mechanism. React may not patch mismatched text under that escape hatch.

## 9. Stable IDs

Use domain IDs when they represent data identity. Use `useId` for component-instance relationships such as label/description/error IDs that must match between server and client.

Do not use `useId` for:

- list keys;
- database IDs;
- cache keys;
- request correlation IDs;
- values that must remain stable across unrelated mounts.

For multiple roots, coordinate `identifierPrefix` between server and client.

## 10. Browser-only data and two-pass UI

When UI truly depends on browser-only data, choose a deliberate strategy:

- render a server-safe default that remains acceptable after hydration;
- reserve layout and update after an Effect;
- use a framework client-only boundary;
- pass a server-derived hint while accepting that it may be stale;
- read an external browser store with a server snapshot.

A post-hydration second render adds cost and can cause visible change. Do not use it for values the server could provide.

Never expose secrets or trust decisions through client-only branching. The server remains authoritative.

## 11. Hydration errors and telemetry

Use `hydrateRoot` recovery callbacks or framework equivalents when custom reporting is required.

Capture:

- error category and cause;
- component stack where available;
- route/build version;
- safe environment metadata;
- enough information to group mismatches without serializing props or personal data.

Do not suppress console output globally or treat every recoverable mismatch as harmless. Repeated recovery can discard server work, lose state, break event attachment, and hide deployment skew.

## 12. Streaming SSR and Suspense

Suspense boundaries form streaming and selective hydration units.

Choose boundaries based on:

- shell usefulness;
- data dependencies;
- layout stability;
- interaction priority;
- error isolation;
- network and server latency;
- whether fallback content remains accessible;
- whether a boundary would block critical metadata or status decisions.

Start independent data work before descending through sequential component boundaries when the framework permits it. A deeply nested fetch hierarchy can serialize server rendering.

Abort work when the client disconnects or a deadline expires, but distinguish abandoned response work from mutations that may already have committed.

## 13. CSP and streamed content

Streaming and hydration can involve inline scripts, bootstrap data, and resource hints. Follow framework support for CSP nonces or hashes.

Do not weaken CSP globally to make hydration work. Ensure:

- nonce reaches every generated inline script that requires it;
- serialized data cannot terminate script context or inject markup;
- source maps and error payloads do not expose secrets;
- third-party scripts are intentionally allowed;
- Trusted Types policy is compatible with React and the framework when enforced.

## 14. React Server Components

Server Components render in a server/build environment and can reduce client JavaScript by keeping server-only work out of the client graph. They are not simply components that render during SSR.

Define:

- which modules are server or client;
- what props and return values can cross the boundary;
- where data is fetched and cached;
- how mutations revalidate rendered data;
- how errors and Suspense cross boundaries;
- bundle and deployment integration;
- security patch ownership.

A Server Component may access server resources according to application architecture. A Client Component must not import server-only modules or secrets.

Do not add a client boundary high in the tree merely to use one stateful leaf. Move the boundary down when that reduces serialization and client bundle cost without complicating composition.

## 15. RSC serialization

Values crossing the RSC boundary must be supported by the installed framework/React protocol.

Review:

- serializable value types;
- object size and duplication;
- class instances and methods;
- Dates, Maps, Sets, promises, and special values according to exact support;
- error redaction;
- stable identifiers;
- tenant and permission scope;
- whether a value accidentally contains a database row, secret, or server capability.

Pass the minimum data needed by the client. Do not serialize a broad object because it is already available on the server.

Protocol details can change through framework/bundler integration. Verify primary documentation for the installed version.

## 16. Server Functions and `"use server"`

`"use server"` marks functions callable through the server-function transport. It does not mark a component as a Server Component.

Treat each callable function as a public network endpoint:

- authenticate on the server;
- authorize the specific resource and operation;
- parse and validate all arguments;
- avoid trusting hidden inputs, client roles, or object ownership fields;
- limit payload size and expensive work;
- protect cookie-based mutations according to framework CSRF/origin controls;
- make repeated requests safe or explicitly rejected;
- use transactions and define partial failure;
- return minimal safe data;
- log without exposing input or source secrets;
- keep React/framework RSC packages currently patched.

A function reference being difficult to guess is not access control.

## 17. Cache scope

Different caches have different contracts:

- request deduplication;
- render-lifetime cache;
- user/session cache;
- route revalidation cache;
- process-local LRU;
- distributed application cache;
- CDN response cache;
- browser data cache.

React `cache` and RSC integration do not automatically provide cross-request persistence or authorization-safe keys.

For every cache, define:

- key and identity dimensions;
- lifetime and eviction;
- invalidation;
- negative/error caching;
- tenant/user/locale/permission scope;
- mutation coherence;
- memory/resource bounds;
- deployment consistency.

Do not cache a response before authorization and then reuse it across identities.

## 18. React 19 document metadata

React 19 can hoist metadata elements such as `title`, `meta`, and `link` to the document head. Frameworks may provide richer route-aware metadata systems.

Preserve:

- deterministic ownership and precedence;
- route transitions and nested metadata;
- duplicate prevention;
- security-sensitive attributes;
- SSR output order;
- social/SEO tags;
- compatibility with framework head management.

Do not combine two head managers without a defined precedence model.

## 19. Stylesheets, scripts, and resource hints

React 19 DOM APIs can coordinate stylesheet precedence, async scripts, preconnect, preload, preinit, and related resources.

Use them only when the framework/build tool does not already own the resource and when loading evidence justifies it.

Check:

- URL validation and trusted origins;
- `crossOrigin`, integrity, nonce, fetch priority, and resource type;
- duplicate insertion;
- CSS precedence and blocking behavior;
- script execution ordering;
- hydration and streaming placement;
- privacy impact of early third-party connections.

Do not preload every route chunk or third-party asset. Competing hints can delay more important resources.

## 20. React 19.2 Activity and hidden DOM

An Activity hidden subtree preserves state but hides DOM, tears down Effects, and deprioritizes work.

Review:

- current focus when hidden;
- accessibility tree behavior;
- media, connections, subscriptions, and timers being stopped;
- memory retained by state and DOM;
- stale data on reactivation;
- whether sensitive state should be destroyed instead;
- SSR/hydration behavior in the framework.

Use ordinary conditional rendering when unmount/reset is the correct lifecycle.

## 21. Partial pre-rendering and resume

React 19.2 resume APIs can support pre-rendering a shell and resuming postponed work later. This is normally framework infrastructure.

Adoption requires:

- exact React/server/client version alignment;
- serialized postponed-state compatibility;
- deployment and cache-version strategy;
- abort and timeout handling;
- CSP/bootstrap integration;
- invalidation and personalized content policy;
- observability across pre-render and resume phases;
- rollback when mixed deployments serve incompatible artifacts.

Do not adopt raw resume APIs inside an application feature without owning the rendering platform.

## 22. Custom elements

React 19 improved custom-element integration. Still verify the actual element contract:

- property versus attribute behavior;
- boolean and complex values;
- event names and listener options;
- upgrade timing;
- SSR output and hydration;
- TypeScript JSX declarations;
- ref and imperative lifecycle;
- sanitization of values crossing into the element.

Wrap a custom element when a stable React API, event normalization, or SSR guard adds value. Do not wrap it merely to rename every property.

## 23. Error Boundaries across rendering modes

Understand which layer catches what:

- component Error Boundaries catch descendant render/lifecycle errors according to React semantics;
- Suspense handles suspension, not arbitrary failure;
- framework route boundaries may catch loader/action/server errors;
- server rendering errors may occur before or after the shell is sent;
- Server Function errors need an explicit safe result or framework error path;
- event-handler errors are not automatically caught by component boundaries.

Keep user recovery, HTTP response, telemetry, and data rollback responsibilities separate.

## 24. Deployment skew

HTML, RSC payloads, JavaScript chunks, CSS, and server code can come from different deployment versions through caches or rolling rollout.

Mitigate with framework-supported build IDs, immutable assets, cache policy, compatible wire formats, and error recovery. Test stale HTML requesting new/removed chunks where the deployment model makes it credible.

Do not treat intermittent hydration or chunk errors after deployment as harmless user cache problems without evidence.

## 25. Testing rendering boundaries

Applicable tests include:

- client root mount/update/unmount;
- multiple widget instances and teardown;
- server render does not access browser-only APIs;
- server HTML and client initial render hydrate without mismatch;
- `useId` relationships remain stable;
- streaming shell, fallback, reveal, error, and abort;
- root error callback integration;
- portal events and focus;
- RSC serializable props and client boundary size;
- Server Function authentication, authorization, validation, duplicates, and error redaction;
- cache isolation across users/tenants;
- CSP nonce and resource behavior;
- production build and deployment artifact compatibility.

Use a real browser for focus, script, CSS, hydration, and browser parser behavior that DOM emulation cannot prove.

## 26. Common failure modes

- `createRoot` used on server-rendered HTML instead of hydrating.
- Root recreated for every update.
- Random/time/browser-only render output causes hydration mismatch.
- `suppressHydrationWarning` hides a structural defect.
- Invalid HTML is corrected by the browser before hydration.
- Mutable module state leaks one request's user into another.
- A broad client boundary serializes large server data and ships unnecessary code.
- A Server Function trusts client-supplied authorization fields.
- An RSC cache omits tenant or locale from its key.
- Framework head/resource management is duplicated.
- Portal outside-click logic ignores React ancestry or nested overlays.
- Raw partial pre-rendering is adopted without versioned deployment support.

## 27. False-positive controls

Do not report these without concrete impact:

- Multiple roots exist for genuinely independent host widgets.
- A browser-only component updates after hydration using an intentional stable fallback.
- A coarse Suspense boundary represents an atomic page experience.
- A small serializable object crosses an RSC boundary.
- A module-level immutable constant exists on the server.
- A framework owns head tags, resource hints, and RSC internals rather than application code.
- Conditional rendering is used instead of Activity when unmounting is desired.

## 28. Completion gate

Before completing rendering-boundary work, confirm:

- Root type and ownership match the existing HTML lifecycle.
- DOM and portal ownership are unambiguous.
- Server output and client initial render are deterministic.
- Request state and caches cannot cross users or tenants incorrectly.
- RSC/client boundaries minimize data and code without breaking composition.
- Server Functions enforce full server-side security controls.
- Framework metadata/resource/rendering systems are not duplicated.
- Exact React/framework versions support introduced APIs.
- Production SSR/hydration/RSC/browser tests cover the changed boundary.
