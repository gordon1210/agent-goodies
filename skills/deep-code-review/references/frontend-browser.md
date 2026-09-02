# Frontend and Browser

## Contents

- State and rendering
- Async effects and races
- Forms and user actions
- Server/client boundaries
- Browser security and storage
- Navigation, caching, and errors
- Accessibility as behavior
- Verification

## State and rendering

Trace source of truth and ownership for each changed UI state.

Check:

- derived state copied and becoming stale
- props/server data overwritten by local initialization
- updates based on stale closures or stale snapshots
- unstable keys causing state to move between items
- mutation that prevents change detection or corrupts shared state
- controlled/uncontrolled input transitions
- conditional rendering that loses required state or cleanup
- optimistic updates whose rollback restores the wrong version
- loading, empty, error, and success states matching actual requests
- duplicated state across URL, cache, form, and component

Do not require loading indicators when no real asynchronous operation occurs.

## Async effects and races

Inspect:

- older request response overwriting newer state
- effect/task continuing after unmount, route change, or dependency change
- cancellation/abort signal not propagated
- duplicate requests from lifecycle or dependency mistakes
- missing dependency causing stale behavior versus extra dependency causing loops
- event listener, timer, subscription, observer, or worker cleanup
- concurrent optimistic mutations and rollback order
- retries after user intent changed
- background refresh replacing unsaved edits

Provide the concrete sequence of user actions and response ordering.

## Forms and user actions

Check:

- double submission and disabled-state timing
- button default type causing unintended submit
- validation mismatch between displayed and submitted values
- normalization after validation
- stale hidden fields or entity IDs after navigation
- cancel/reset restoring correct initial state
- partial failure in multi-step forms
- keyboard and pointer behavior triggering different actions
- destructive action confirmation when explicitly required by product policy
- server rejection correctly reconciling optimistic UI

Client validation improves UX; server validation and authorization remain authoritative.

## Server/client boundaries

For SSR, hydration, server components, islands, or pre-rendering, inspect:

- browser-only APIs executed on server
- non-deterministic values causing hydration mismatch
- secrets/server-only modules included in client bundles
- authorization-sensitive data serialized to the browser
- server cache reused across users/tenants
- request-specific state stored globally
- serialization of unsupported values
- stale pre-render/cache behavior after mutations
- differences between direct navigation and client navigation

A hidden component is not a security boundary.

## Browser security and storage

Route security-specific paths to the security modules as well.

Check:

- raw HTML/markdown/SVG insertion and URL schemes
- `postMessage` origin and source validation
- opener/iframe relationships and target origin
- sensitive tokens/data in localStorage, sessionStorage, IndexedDB, URL, history, or logs
- CSRF-relevant state-changing requests under the application's authentication model
- CORS assumptions used as authorization
- downloads and filenames derived from untrusted input
- service-worker cache mixing users or versions
- clipboard/paste content reaching dangerous sinks

Do not report framework text interpolation as XSS without an escaping bypass.

## Navigation, caching, and errors

Inspect:

- URL/query state parsing and back/forward behavior
- navigation before persistence finishes
- route guards based only on stale client state
- cache invalidation keys and optimistic updates
- error boundaries that hide retryable state or loop
- redirects losing intended destination or sensitive parameters
- stale data after login/logout/tenant switch
- offline/reconnect behavior and duplicate replay
- pagination/infinite-scroll cursor and deduplication

## Accessibility as behavior

Report accessibility as a defect when the change makes a required interaction unavailable or misleading, not as generic polish.

Check:

- keyboard access to an action
- focus moved/lost after dialogs, navigation, or dynamic updates
- semantic control replaced with non-interactive element
- label/name/state exposed incorrectly to assistive technology
- modal focus containment and restoration
- error association and status announcements where users otherwise cannot perceive completion/failure

Use repository/product accessibility requirements when present. Pure preference belongs outside defect findings.

## Verification

A finding should include a reproducible user sequence, browser/server state, and observed wrong outcome. Inspect the data layer/cache/router and server enforcement before blaming the component in isolation.
