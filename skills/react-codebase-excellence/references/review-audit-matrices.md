# Repository Audit Matrices

Read this reference for repository-wide or subsystem audits after establishing scope with [review-playbooks.md](review-playbooks.md). Use only applicable rows, record evidence, and avoid turning every question into a finding. The matrices are coverage prompts, not automatic severity rules.

## How to use the matrices

1. Record the exact package, route, rendering mode, React version, and trust boundary covered.
2. Mark each applicable row as reviewed, not reviewed, or not applicable.
3. Link evidence such as code paths, tests, configuration, traces, or authoritative version behavior.
4. Report a finding only when the evidence meets the quality bar in the review playbook.
5. State blind spots rather than inferring safety from an unchecked row.

## 1. Component and API review matrix

| Area | Questions |
|---|---|
| Responsibility | Does the component own one coherent behavior without becoming an arbitrary mode engine? |
| Props | Are required/optional states clear and invalid combinations avoidable? |
| Composition | Is composition simpler for consumers than additional configuration? |
| Controlled state | Are value/default/reset/change semantics explicit? |
| Refs | Is imperative behavior minimal and version-compatible? |
| Context | Is provider scope coherent and update breadth acceptable? |
| Identity | Are component type, keys, and state reset identity stable? |
| Native behavior | Does custom UI preserve browser semantics? |
| Public API | Are exports, DOM, CSS hooks, types, and ref contracts compatible? |
| Design system | Are variants, tokens, slots, and accessibility behavior consistent? |

## 2. State, Hooks, and Effects matrix

| Area | Questions |
|---|---|
| Source of truth | Is state minimal, non-contradictory, and owned correctly? |
| Derived data | Can it be computed during render instead of synchronized? |
| Updates | Are functional updates used when based on prior state? |
| Reset | Does state reset or persist according to domain identity? |
| Reducers | Is transition complexity sufficient to justify a reducer? |
| Rules of Hooks | Are calls unconditional, top-level, and statically analyzable? |
| Dependencies | Does every reactive value participate correctly? |
| Cleanup | Is setup mirrored and idempotent? |
| Stale closure | Can late callbacks observe obsolete state or props? |
| External store | Are snapshots stable and server/hydration behavior correct? |

## 3. Async and data matrix

| Area | Questions |
|---|---|
| Ownership | Which layer starts, cancels, retries, caches, and reports work? |
| Waterfalls | Are independent operations unnecessarily serial? |
| Race safety | Can obsolete completion overwrite newer intent? |
| Cancellation | Is cancellation distinguishable from failure where needed? |
| Pending UI | Does it correspond to real work and preserve useful content? |
| Suspense | Are boundaries placed by UX/recovery needs rather than decoration? |
| Transitions | Is urgent work kept urgent and latest intent preserved? |
| Actions | Are validation, authorization, duplicate submission, and rollback correct? |
| Optimism | Can authoritative state reconcile or reject the optimistic state? |
| Bounds | Are concurrency, retries, queues, and payload sizes bounded? |

## 4. SSR, hydration, and RSC matrix

| Area | Questions |
|---|---|
| Request isolation | Can module or global state leak between requests or tenants? |
| Determinism | Does initial client output match server output? |
| IDs | Are labels and identifiers stable across server/client roots? |
| Streaming | Are shell, errors, aborts, and crawler/bot behavior correct? |
| Serialization | Is only authorized, serializable, necessary data sent? |
| Boundaries | Are server/client modules and directives valid? |
| Caches | Are scope, identity keys, invalidation, and bounds explicit? |
| Server Functions | Are they treated as authenticated public endpoints? |
| Deployment skew | Can old/new client-server artifacts interoperate as promised? |
| Advisories | Are exact RSC/framework packages on a currently patched line? |

## 5. Accessibility matrix

| Area | Questions |
|---|---|
| Semantics | Is native HTML used where possible? |
| Name/description | Can users identify controls and errors? |
| Keyboard | Is every action operable with expected keys? |
| Focus | Is focus visible, ordered, moved, contained, and restored correctly? |
| State | Are selected, expanded, pressed, invalid, and pending states exposed? |
| Forms | Are labels, instructions, validation, and submission behavior coherent? |
| Announcements | Are meaningful async changes perceivable without excessive noise? |
| Motion | Are reduced-motion and vestibular needs respected? |
| Responsive | Does zoom/reflow preserve content and operation? |
| Tests | Were semantic queries plus real keyboard/focus behavior checked? |

## 6. Security and privacy matrix

| Area | Questions |
|---|---|
| Content | Does untrusted data reach HTML, URL, CSS, SVG, script, or third-party sinks? |
| Authentication | Is caller identity established at every protected server boundary? |
| Authorization | Is the specific resource/action/tenant relationship enforced server-side? |
| Tenancy | Can identifiers, caches, or serialization cross tenant boundaries? |
| Mutation | Are schema, CSRF/origin, idempotency, and rate/size controls appropriate? |
| Secrets | Can credentials reach bundles, HTML, payloads, logs, or source maps? |
| Browser APIs | Are storage, messaging, files, media, and permissions constrained? |
| Third parties | Are scripts, iframes, and data collection bounded? |
| Supply chain | Are scripts, plugins, sources, lockfile, and advisories reviewed? |
| Telemetry | Are personal/sensitive values redacted and labels bounded? |
| Abuse | Are expensive operations and retries bounded at trusted boundaries? |

## 7. Performance matrix

| Area | Questions |
|---|---|
| Contract | Is there a metric, baseline, target, and representative environment? |
| Waterfalls | Can independent network, data, or chunk work start earlier? |
| Bundle | Is unnecessary client code shipped or eagerly executed? |
| State scope | Do high-frequency updates invalidate unrelated work? |
| Render cost | Is expensive calculation demonstrated and reducible? |
| DOM/layout | Are node count, layout, paint, and high-frequency events material? |
| Server | Are request work, cache scope, and serialization efficient and correct? |
| Hydration | Is client JavaScript or serialization larger than necessary? |
| Memory | Are caches, hidden trees, listeners, and resources bounded and released? |
| Compiler | Is the actual compiled production output measured? |

## 8. Tests, tooling, and operations matrix

| Area | Questions |
|---|---|
| Tests | Do tests exercise observable failure boundaries and race/error paths? |
| Determinism | Are time, network, storage, globals, and ordering controlled? |
| Accessibility verification | Do automated and interaction checks cover the critical workflows? |
| CI | Does CI run the supported React, type, browser, and build matrix? |
| Production build | Was the framework, compiler, and bundler output validated? |
| Dependencies | Are peer ranges, exports, scripts, licenses, and lockfile intentional? |
| Diagnostics | Are errors and telemetry useful without leaking data? |
| Rollout | Are feature flags, mixed versions, rollback, and stale assets considered? |
| Resource lifecycle | Are listeners, streams, workers, caches, and retries observable and bounded? |

## 9. Audit coverage report

For each applicable matrix, summarize:

- scope and evidence reviewed;
- qualifying findings;
- positive controls worth preserving;
- unverified packages, routes, browsers, deployment modes, or trust boundaries;
- the next highest-value verification step.

Do not report a percentage without defining the denominator and review depth. A checked row means it was investigated; it does not prove absence of defects.
