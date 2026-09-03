# Frontend, Browser, and UI Engineering

Read this reference for browser applications, component systems, SSR/hydration, forms, client state, data fetching, DOM security, accessibility, routing, browser storage, UI lifecycle, and production browser behavior.

Follow the repository's framework and design system. Do not import patterns from another framework or major version merely because they are familiar.

## 1. Establish the UI contract

Before changing UI code, determine:

- Supported browsers, devices, input modes, locales, themes, zoom, and accessibility requirements.
- Client-only, SSR, streaming SSR, static generation, island, server-component, embedded, extension, or Electron renderer context.
- Which code runs at build time, on the server, in the browser, in a worker, or in a privileged bridge.
- Data ownership, cache, mutation, invalidation, and optimistic-update semantics.
- Navigation and route-state behavior.
- Loading, empty, error, offline, permission, partial, and stale states.
- Form submission, validation, retry, duplication, and unsaved-change behavior.
- Security/privacy boundaries and which values can enter client bundles, DOM, storage, analytics, or URLs.
- Design-system components and established styling/state patterns.

Do not redesign unrelated UI or state architecture while fixing one behavior.

## 2. Components and ownership

A component should own one coherent rendering/lifecycle responsibility.

- Keep domain logic outside framework rendering hooks when it is reusable and independently testable.
- Keep UI-specific state close to the UI that owns it.
- Lift state only when multiple consumers need one source of truth.
- Avoid global stores for local transient state.
- Avoid deeply prop-drilling only when an existing context/composition mechanism cannot express real shared ownership.
- Prefer composition over large configurable “universal” components with many boolean props.
- Use discriminated variants or separate components when prop combinations represent distinct modes.
- Keep effects for synchronization with external systems, not as a substitute for ordinary derivation.
- Do not mirror props/query data into state without a clear ownership/reset rule.

Component extraction is justified by cohesion, reuse, lifecycle, testing, or ownership—not line count.

## 3. State modeling

Model actual UI states rather than independent flags:

```ts
type RemoteState<T> =
  | { readonly status: "idle" }
  | { readonly status: "loading"; readonly requestId: string }
  | { readonly status: "success"; readonly value: T; readonly stale: boolean }
  | { readonly status: "error"; readonly error: UiError };
```

Distinguish:

- Initial load versus refresh/revalidation.
- Empty successful data versus not yet loaded.
- User-cancelled versus failed.
- Unauthorized/forbidden/not-found versus generic error.
- Optimistic pending versus confirmed versus rolled back.
- Stale cached data versus current data.

Show loading UI only while a real operation is pending. Do not simulate loading delays or preserve spinners after data is available merely for visual effect unless product requirements explicitly demand a transition.

## 4. Derived state and effects

Prefer deriving values during render/computation when they depend only on current inputs. Store state when it has independent identity over time.

Avoid effects that:

- Copy one state value into another.
- Recompute pure derived values.
- Trigger chains of state updates that could be one event transition.
- Depend on unstable object/function identities accidentally.
- Fetch without cancellation/staleness handling.
- Register listeners/timers without cleanup.

When an effect synchronizes an external system:

- Declare all dependencies according to framework semantics.
- Make setup/cleanup symmetric and idempotent.
- Handle development double-invocation/replay behavior where the framework uses it.
- Avoid stale closures and race-prone mutable captures.
- Test rerender, unmount, and dependency change.

Do not suppress exhaustive-dependency or lifecycle rules blindly; fix ownership or document a narrow stable invariant.

## 5. Data fetching and cache ownership

Identify one owner for each data lifecycle:

- Framework loader/server function.
- Query/cache library.
- Component-level request.
- Global application service.
- Browser/native cache.

Avoid parallel caches with different freshness and invalidation rules.

Define:

- Cache key and tenant/user scope.
- Freshness/staleness.
- Deduplication/coalescing.
- Retry and deadline.
- Cancellation and navigation behavior.
- Pagination/infinite-list semantics.
- Mutation invalidation or update.
- Error retention.
- Offline/reconnect policy.
- Sensitive data lifetime and storage.

Do not use a generic global fetch wrapper that hides authorization, cancellation, error classification, and response validation.

## 6. Async races and stale responses

A UI can issue overlapping operations through typing, navigation, filters, retries, or rapid actions.

Protect against:

- Older responses overwriting newer user intent.
- Updates after unmount/navigation.
- Duplicate submissions.
- Optimistic updates rolling back newer confirmed data.
- Stale authorization/tenant context.
- Out-of-order pagination.

Use framework cancellation, `AbortController`, request identity, mutation IDs, cache-library semantics, or server-side idempotency as appropriate. Ignoring stale results can be sufficient when cancellation is unavailable, but underlying work and rejection still need ownership.

## 7. Forms and validation

Forms need both client usability and authoritative server validation.

- Use semantic labels, field names, descriptions, and error associations.
- Preserve typed user input during recoverable failures.
- Distinguish parse, validation, authorization, conflict, and dependency failures.
- Validate and authorize on the server even if the client validates first.
- Avoid mass assignment of submitted objects into domain/database models.
- Normalize deliberately; do not silently alter meaningful user input.
- Prevent duplicate submission through UI state and server idempotency where impact requires it.
- Keep password/token values out of logs, analytics, URL parameters, and unnecessary state.
- Define file count/size/type/content validation and upload cancellation.
- Handle browser autofill and password managers rather than fighting them.

A TypeScript form type does not validate `FormData`, URL-encoded input, or server payloads.

## 8. Optimistic updates

Use optimistic UI only when:

- The likely outcome is success.
- A reversible local model exists.
- Conflicts and out-of-order responses are handled.
- The user can understand failure/rollback.
- Security/authorization is still enforced server-side.

Define:

- Temporary identity.
- Merge with server result.
- Rollback scope.
- Multiple concurrent mutations.
- Retry and duplicate semantics.
- Navigation/reload behavior.

Do not optimistically show irreversible or security-sensitive actions as complete when confirmation is required.

## 9. Routing and navigation

Treat route, query, and history state as external input.

- Parse and validate route/query values.
- Keep canonical URL and state synchronization deliberate.
- Avoid sensitive data in URLs because URLs enter history, logs, analytics, referrers, and screenshots.
- Encode path segments and query parameters with URL APIs, not string concatenation.
- Handle back/forward navigation and scroll/focus restoration.
- Cancel or supersede route-owned requests.
- Define behavior for unsaved changes without trapping users unexpectedly.
- Authorize server data independently of client route guards.
- Keep redirects/return URLs constrained to prevent open redirects.

## 10. SSR and hydration

Server-rendered UI creates a serialization and environment boundary.

- Ensure server and client initially render semantically compatible output.
- Avoid nondeterministic values such as current time, random IDs, locale, viewport, or browser-only state unless coordinated.
- Do not access browser globals during server execution or server globals in client modules.
- Serialize only values with a defined representation; dates, bigints, maps, sets, class instances, errors, and undefined need explicit handling.
- Escape hydration data safely in its embedding context.
- Keep secrets, internal errors, and server-only data out of markup and hydration payloads.
- Prevent request-specific state from leaking through process-global caches or module singletons.
- Test production hydration, not only development mode.

Do not silence hydration mismatches globally. Identify whether the discrepancy is intentional and isolate it narrowly.

## 11. Server/client and privileged boundaries

Framework labels or file directives are only useful when the build enforces them.

- Keep server-only modules from client import graphs.
- Avoid shared modules with top-level environment-specific side effects.
- Treat calls from client to server functions as network/trust boundaries even when syntax appears local.
- Revalidate input, authentication, authorization, and tenancy on the server.
- Avoid serializing database entities or internal exceptions directly to clients.
- For Electron/extensions/native bridges, expose narrow validated operations rather than generic execution/filesystem/process access.
- Test the built bundle/manifest to ensure boundary enforcement.

## 12. DOM safety

Prefer safe APIs that create text/nodes/attributes through the framework or DOM.

Elevated-risk operations include:

- Raw HTML insertion.
- Dynamic script/style creation.
- URL-bearing attributes.
- SVG and MathML content.
- DOM parsing.
- Dynamic event-handler strings.
- `eval`, `Function`, and string timers.
- Markdown/rich-text rendering.

Use the project's approved sanitizer for rich content, configured for the exact context. Validate URL protocols separately. A `SanitizedHtml` type is trustworthy only if creation is controlled and cannot be forged through assertions or unvalidated deserialization.

## 13. Accessibility as a functional contract

Build on native semantic elements before recreating behavior with generic containers.

Verify:

- Accessible name, role, state, value, and relationships.
- Keyboard navigation and activation.
- Visible focus and logical focus order.
- Focus management for dialogs, navigation, validation errors, and removed content.
- Labels, instructions, and error association.
- Announcements for meaningful async updates.
- Reduced motion and user preferences.
- Zoom/reflow/responsive behavior.
- Pointer, touch, keyboard, and assistive-technology interaction.
- Color-independent status communication.

ARIA does not add missing keyboard or behavioral semantics automatically. Avoid redundant or invalid ARIA on native elements.

Automated checks catch only a subset; critical flows need browser and, where required, manual assistive-technology verification.

## 14. Dialogs, overlays, and focus

For modal UI:

- Move focus to a meaningful element when opened.
- Trap focus only while truly modal.
- Restore focus to a valid origin when closed.
- Support Escape/close semantics according to product requirements.
- Prevent background interaction and scrolling appropriately.
- Maintain accessible labeling and description.
- Handle nested overlays carefully; avoid stacking-manager complexity unless needed.
- Clean up global listeners and portal roots.

Use the design system/framework primitive when it already implements these contracts.

## 15. Lists, tables, and identity

- Use stable domain identity for keyed rendering; array indexes are unsafe when items reorder, insert, or retain local state.
- Preserve selection/focus across updates deliberately.
- Use semantic table markup for tabular data.
- Define sorting/filtering/pagination semantics and announce changes where needed.
- Avoid rendering unbounded result sets.
- Virtualization must preserve keyboard navigation, accessibility relationships, measurement, and scroll behavior.
- Do not use object identity as a stable key across parsed/refetched data.

## 16. Browser storage and offline data

Treat cookies, local/session storage, IndexedDB, Cache Storage, and service-worker caches as persistence boundaries.

- Validate and version stored values on read.
- Scope keys by user/tenant/environment where needed.
- Remove sensitive data on logout/account change.
- Avoid long-lived access tokens or secrets in script-readable storage when safer session mechanisms exist.
- Handle quota, eviction, private mode, corruption, and partial writes.
- Define cross-tab synchronization and race behavior.
- Encrypting client storage with a key available to the same client does not protect against script compromise.
- Migrate or invalidate old schemas deliberately.
- Keep offline mutation queues idempotent and user-visible when conflicts occur.

## 17. Service workers and caching

- Version caches and define activation/update behavior.
- Avoid serving stale application shells or APIs indefinitely after deployment.
- Distinguish navigation, static asset, and API caching strategies.
- Do not cache authenticated/private responses without correct key and privacy semantics.
- Bound cache growth and cleanup old versions.
- Handle offline fallback without hiding important failures.
- Test updates with multiple open tabs and old/new clients.
- Ensure background sync/retries are idempotent and authorization remains valid.

A service worker can make rollback and incident response harder; maintain an explicit update/disable path.

## 18. Errors and recovery UI

- Show actionable, user-appropriate messages without exposing internals.
- Preserve safe context and user input where recovery is possible.
- Distinguish field validation, permission, conflict, offline, timeout, and unexpected failure.
- Provide retry only when the operation is safe and useful.
- Avoid infinite retry loops or repeated alerts.
- Keep operator diagnostics in logs/traces with correlation, not raw stack traces in UI.
- Ensure error boundaries do not swallow authorization/security failures into misleading fallback content.
- Test error UI with keyboard/screen-reader focus and announcements.

## 19. Internationalization and user-facing text

- Keep user-facing text in the repository's localization system.
- Do not construct sentences from fragments whose grammar changes by locale.
- Use locale-aware formatting for numbers, dates, durations, and lists.
- Store/transport canonical values; localize at presentation boundaries.
- Account for text expansion, right-to-left layout, pluralization, and timezone.
- Avoid using localized text as a programmatic identifier or test selector.
- Treat translation files as untrusted-ish content if external contributors/systems can modify them; preserve escaping semantics.

## 20. Styling and layout

Follow the design system and existing styling model.

- Avoid global selectors and overrides that create unrelated regressions.
- Preserve responsive behavior and content reflow.
- Prefer logical properties when bidirectional layout is supported.
- Do not encode state solely through color.
- Keep z-index/layering policy coherent rather than escalating arbitrary values.
- Avoid layout reads/writes that cause measured thrashing.
- Ensure hidden content semantics match visual hiding and accessibility expectations.
- Verify high contrast, forced colors, reduced motion, and zoom when product support requires them.

## 21. Client performance

Measure production behavior before optimizing.

- Keep critical bundles/chunks bounded and server-only dependencies out.
- Avoid unnecessary broad rerenders or expensive derivation.
- Memoize only when dependencies and retention are correct and measurement justifies it.
- Lazy-load noncritical code without creating request waterfalls or inaccessible loading states.
- Bound list rendering, prefetching, uploads, and cached data.
- Avoid giant JSON hydration payloads.
- Use browser performance traces for interaction and rendering issues.
- Test low-end devices/network profiles when part of the support contract.

## 22. Telemetry and privacy in UI

- Collect only fields required for product/operational decisions.
- Avoid DOM text, form values, query strings, URLs with sensitive parameters, tokens, and user-generated content by default.
- Bound event names/properties and metric cardinality.
- Respect consent, retention, tenant separation, and regional policy.
- Do not let telemetry failures block interactions indefinitely.
- Prevent duplicate events caused by rerender/effect behavior.
- Test that error/reporting SDKs redact and do not upload source maps or payloads contrary to policy.

## 23. Frontend testing

Use a layered approach:

- Unit tests for pure state/domain helpers.
- Component tests for rendering, events, lifecycle, and accessibility semantics.
- Integration tests for data/cache/routing/form boundaries.
- Real-browser E2E tests for critical user flows and platform behavior.
- Production build/hydration tests for SSR/bundling.
- Security tests for raw HTML, URLs, messages, and server authorization.

Prefer user-observable queries. Avoid snapshots as the sole evidence for interactive behavior. Test loading only while actual controlled promises are pending, and test stale/cancelled results.

## Frontend completion checklist

- Component and state ownership are coherent and no broader than necessary.
- Loading, empty, stale, error, permission, cancellation, and optimistic states match real operations.
- Effects/listeners/timers/subscriptions have symmetric lifecycle cleanup.
- Overlapping requests cannot overwrite newer intent incorrectly.
- Forms are accessible and server-authoritative.
- SSR/hydration and server/client boundaries are deterministic and secure.
- DOM sinks, URLs, storage, messages, and privileged bridges are validated.
- Accessibility is treated as behavior, not markup decoration.
- Browser storage/cache data is versioned, bounded, and scoped.
- Production browser artifacts and critical engines receive appropriate tests.
