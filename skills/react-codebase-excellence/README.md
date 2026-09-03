# React Codebase Excellence Skill

A production-oriented Agent Skill for designing, implementing, reviewing, refactoring, debugging, testing, securing, optimizing, and upgrading React web codebases.

The skill provides full stable React 19 coverage, including React 19.2 and React Compiler guidance, while retaining a deliberate React 18 compatibility path for existing applications and libraries. It is framework-aware but framework-neutral: installed framework rules own routing, data loading, RSC transport, caching, and deployment details.

The guidance is intentionally non-dogmatic. It preserves repository contracts and favors the smallest sound change over speculative architecture, blanket memoization, mandatory state libraries, effect purges, or framework cargo cults.

## Contents

```text
react-codebase-excellence/
├── SKILL.md
├── README.md
├── EVALUATION.md
├── LICENSE
└── references/
    ├── accessibility-forms-interactions.md
    ├── architecture-tooling-typescript.md
    ├── async-suspense-actions-transitions.md
    ├── components-composition-api-design.md
    ├── effects-events-external-systems.md
    ├── performance-compiler-bundles.md
    ├── rendering-dom-ssr-hydration-rsc.md
    ├── review-audit-matrices.md
    ├── review-playbooks.md
    ├── security-content-dependencies.md
    ├── sources.md
    ├── state-data-flow-hooks.md
    ├── testing-server-browser-ci.md
    ├── testing-verification.md
    └── version-compatibility-react18-react19.md
```

`SKILL.md` contains the operating workflow and high-value default rules. It routes the agent to focused references only when the task needs them, keeping ordinary context use bounded while retaining broad coverage for reviews and audits.

## Coverage

| Area | Included |
|---|---|
| Versions | React 18, React 18.3 migration bridge, React 19.0/19.1, React 19.2, Canary gating |
| Components | Boundaries, props, composition, controlled/uncontrolled APIs, refs, context, design systems |
| State | State shape, reducers, custom Hooks, URL/form/server state, external stores |
| Effects | Dependencies, stale closures, cleanup, subscriptions, timers, observers, browser APIs |
| Async | Promises, race prevention, cancellation, Suspense, transitions, Actions, optimistic UI |
| Rendering | DOM roots, portals, SSR, streaming, hydration, static APIs, RSC, Server Functions |
| Performance | Waterfalls, bundle/client cost, render work, lists, memory, profiling, React Compiler |
| Accessibility | Semantics, labels, keyboard, focus, forms, errors, announcements, motion, responsive UI |
| Security | XSS/content sinks, URLs, auth, tenancy, RSC advisories, secrets, browser APIs, dependencies |
| Testing | Unit, component, integration, browser, SSR/hydration/RSC, accessibility, performance, CI |
| Reviews | Patch, design, migration, performance, security, accessibility, and repository-audit playbooks |

## Intended use

Use the skill for:

- Focused React implementation and debugging.
- Pull-request and patch review.
- Repository-wide quality, security, accessibility, or production-readiness audits.
- Component-library and design-system API work.
- React 18 maintenance and React 18-to-19 migration.
- React 19 Actions, Suspense, transitions, Owner Stack diagnostics, Activity, Effect Events, and resource APIs.
- SSR, streaming, hydration, React Server Components, and Server Functions.
- React Compiler adoption and performance work.
- Test and CI design for applications or published libraries.

It is optimized for small-to-medium codebases and bounded packages/subsystems inside larger monorepos.

## Design principles

### Exact-version behavior

The skill checks the installed version before recommending APIs:

- React 18 does not receive React 19-only APIs.
- React 19.0 does not receive React 19.1-only development diagnostics.
- React 19.0/19.1 does not receive React 19.2-only APIs.
- Canary APIs remain unavailable unless the repository intentionally pins that channel.
- Libraries claiming React 18 and 19 support preserve a shared public contract or use an explicit compatibility strategy.

### Progressive disclosure

The main skill stays operational and routes detailed guidance into domain references. A routine component fix should not load RSC, compiler, security, and repository-audit material unless those boundaries are involved.

### Evidence over cargo cults

The skill deliberately avoids several common review and generation failures:

- No blanket ban on Effects, context, boolean props, index keys, inline callbacks, or uncontrolled inputs.
- No automatic `memo`, `useMemo`, or `useCallback` policy.
- No assumption that React Compiler makes all manual memoization removable.
- No automatic global-state, reducer, custom-Hook, compound-component, Suspense, or Server Component conversion.
- No performance finding without a metric, demonstrated cost, or directly provable waterfall.
- No accessibility finding from ARIA preference alone when native semantics are already correct.
- No security finding without a reachable source-to-sink or boundary failure.
- No invented finding when a patch is correct.

### Framework boundaries

React does not define an application's complete routing, data-loading, caching, RSC transport, or deployment model. The skill first inspects the installed framework and then applies React guidance inside that contract.

Next.js-, Remix-, React Router-, TanStack-, Vite-, Astro-, or custom-renderer recommendations are not applied generically.

## Scope and exclusions

This package targets React DOM web applications and libraries.

It does not attempt to be a complete React Native, Expo, Electron, browser-extension, graphics/canvas, or framework-specific operational guide. The React-level rules still apply where relevant, but platform-owned APIs, security boundaries, accessibility behavior, packaging, and deployment require their own guidance.

It also does not promise compatibility with unpinned experimental or Canary features.

## Installation

Place the `react-codebase-excellence` directory in the Agent Skills directory used by the host application. The directory name must remain identical to the `name` field in `SKILL.md`.

Example repository-local layout:

```text
<repository>/
└── .agents/
    └── skills/
        └── react-codebase-excellence/
            ├── SKILL.md
            └── references/
```

Host paths and discovery rules vary. Follow the host's current Agent Skills documentation rather than assuming one universal location.

## Validation

From the parent repository, validate the package with the Agent Skills reference validator when available:

```bash
skills-ref validate ./skills/react-codebase-excellence
```

Also validate:

- YAML frontmatter and directory/name agreement.
- All local Markdown links.
- Main `SKILL.md` progressive-disclosure size.
- ZIP/archive contents.
- Behavioral scenarios in `EVALUATION.md` after material rule changes.

## Evaluation

`EVALUATION.md` contains behavioral scenarios designed to catch common failures such as:

- recommending React 19 APIs in React 18;
- treating every Effect or rerender as a defect;
- missing stale-request races;
- breaking React 18 library refs during React 19 modernization;
- hiding hydration mismatches;
- trusting client-side authorization;
- missing cross-tenant RSC/cache exposure;
- over-reporting performance or style issues;
- using deprecated test renderers;
- inventing findings in a correct patch.

The scenarios assess decisions and evidence, not exact phrasing.

## Sources

The guidance is derived primarily from official React/React DOM/React Compiler documentation, web-platform specifications, W3C accessibility guidance, MDN/OWASP security guidance, TypeScript documentation, and official tool documentation.

Vercel's React Best Practices and Composition Patterns skills informed prioritization of performance and component-API topics. Their framework-specific recommendations were not copied into framework-neutral rules. See `references/sources.md` for the maintained source index.

## Versioning

The skill uses semantic versioning in `SKILL.md` metadata:

- Patch: clarification or source refresh without materially changing expected decisions.
- Minor: compatible expansion of supported tasks or a new focused reference.
- Major: changed rule hierarchy, required workflow, compatibility policy, or behavior that can materially alter generated code or review outcomes.

## License

MIT. See `LICENSE`.
