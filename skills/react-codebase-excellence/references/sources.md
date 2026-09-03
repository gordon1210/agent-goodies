# Primary Sources and Maintenance Notes

Last reviewed: 2026-09-03.

This skill contains derived engineering guidance rather than copied external prose. Re-check primary documentation whenever a rule depends on React, React DOM, React Compiler, TypeScript, browser, accessibility, security, testing, framework, or package-manager behavior. Repository-local and framework-specific contracts take precedence where they own the integration.

## Agent Skills format

- Agent Skills specification: https://agentskills.io/specification
- Progressive disclosure and client integration: https://agentskills.io/client-implementation/adding-skills-support
- Skill authoring best practices: https://agentskills.io/skill-creation/best-practices
- Reference validator: https://github.com/agentskills/agentskills/tree/main/skills-ref

## React versions and releases

- Supported/current documentation versions: https://react.dev/versions
- React 19 release: https://react.dev/blog/2024/12/05/react-19
- React 19 upgrade guide: https://react.dev/blog/2024/04/25/react-19-upgrade-guide
- React 19.1 release notes: https://github.com/react/react/releases/tag/v19.1.0
- `captureOwnerStack`: https://react.dev/reference/react/captureOwnerStack
- React 19.2 release: https://react.dev/blog/2025/10/01/react-19-2
- React Compiler 1.0: https://react.dev/blog/2025/10/07/react-compiler-1
- React releases repository: https://github.com/react/react/releases

Use exact installed versions. Do not infer that every React 19 API exists in React 19.0, or that a Canary API is stable.

## React fundamentals and rules

- Keeping components pure: https://react.dev/learn/keeping-components-pure
- Rules of React: https://react.dev/reference/rules
- Rules of Hooks: https://react.dev/reference/rules/rules-of-hooks
- Components and Hooks must be pure: https://react.dev/reference/rules/components-and-hooks-must-be-pure
- React calls components and Hooks: https://react.dev/reference/rules/react-calls-components-and-hooks
- State as a snapshot: https://react.dev/learn/state-as-a-snapshot
- Queueing state updates: https://react.dev/learn/queueing-a-series-of-state-updates
- Choosing state structure: https://react.dev/learn/choosing-the-state-structure
- Sharing state: https://react.dev/learn/sharing-state-between-components
- Preserving and resetting state: https://react.dev/learn/preserving-and-resetting-state
- Extracting state logic into a reducer: https://react.dev/learn/extracting-state-logic-into-a-reducer
- Passing data deeply with context: https://react.dev/learn/passing-data-deeply-with-context
- Scaling with reducer and context: https://react.dev/learn/scaling-up-with-reducer-and-context
- Reusing logic with custom Hooks: https://react.dev/learn/reusing-logic-with-custom-hooks

## Effects, events, and external systems

- Synchronizing with Effects: https://react.dev/learn/synchronizing-with-effects
- You might not need an Effect: https://react.dev/learn/you-might-not-need-an-effect
- Lifecycle of reactive Effects: https://react.dev/learn/lifecycle-of-reactive-effects
- Separating events from Effects: https://react.dev/learn/separating-events-from-effects
- Removing Effect dependencies: https://react.dev/learn/removing-effect-dependencies
- `useEffect`: https://react.dev/reference/react/useEffect
- `useLayoutEffect`: https://react.dev/reference/react/useLayoutEffect
- `useInsertionEffect`: https://react.dev/reference/react/useInsertionEffect
- `useEffectEvent` (React 19.2): https://react.dev/reference/react/useEffectEvent
- `useSyncExternalStore`: https://react.dev/reference/react/useSyncExternalStore

## Components, refs, forms, and DOM

- `useId`: https://react.dev/reference/react/useId
- `useImperativeHandle`: https://react.dev/reference/react/useImperativeHandle
- `forwardRef`: https://react.dev/reference/react/forwardRef
- `<form>`: https://react.dev/reference/react-dom/components/form
- `<input>`: https://react.dev/reference/react-dom/components/input
- `<select>`: https://react.dev/reference/react-dom/components/select
- `<textarea>`: https://react.dev/reference/react-dom/components/textarea
- Common DOM components: https://react.dev/reference/react-dom/components/common
- `createPortal`: https://react.dev/reference/react-dom/createPortal
- Custom HTML elements in React 19: https://react.dev/reference/react-dom/components#custom-html-elements

## Async rendering, Suspense, and Actions

- `<Suspense>`: https://react.dev/reference/react/Suspense
- `lazy`: https://react.dev/reference/react/lazy
- `startTransition`: https://react.dev/reference/react/startTransition
- `useTransition`: https://react.dev/reference/react/useTransition
- `useDeferredValue`: https://react.dev/reference/react/useDeferredValue
- `use`: https://react.dev/reference/react/use
- `useActionState`: https://react.dev/reference/react/useActionState
- `useOptimistic`: https://react.dev/reference/react/useOptimistic
- `useFormStatus`: https://react.dev/reference/react-dom/hooks/useFormStatus
- `<Activity>` (React 19.2): https://react.dev/reference/react/Activity
- `cache`: https://react.dev/reference/react/cache
- `cacheSignal` (React 19.2): https://react.dev/reference/react/cacheSignal

## Client rendering, SSR, hydration, and resources

- `createRoot`: https://react.dev/reference/react-dom/client/createRoot
- `hydrateRoot`: https://react.dev/reference/react-dom/client/hydrateRoot
- React DOM client APIs: https://react.dev/reference/react-dom/client
- React DOM server APIs: https://react.dev/reference/react-dom/server
- `renderToPipeableStream`: https://react.dev/reference/react-dom/server/renderToPipeableStream
- `renderToReadableStream`: https://react.dev/reference/react-dom/server/renderToReadableStream
- React DOM static APIs: https://react.dev/reference/react-dom/static
- `prerender`: https://react.dev/reference/react-dom/static/prerender
- `resume`: https://react.dev/reference/react-dom/server/resume
- Resource preloading APIs: https://react.dev/reference/react-dom#resource-preloading-apis
- React DOM Performance Tracks: https://react.dev/reference/dev-tools/react-performance-tracks

Framework documentation is authoritative for framework-owned routing, data loading, streaming, prerendering, RSC transport, caching, and deployment behavior.

## React Server Components and Server Functions

- Server Components: https://react.dev/reference/rsc/server-components
- Server Functions: https://react.dev/reference/rsc/server-functions
- `'use client'`: https://react.dev/reference/rsc/use-client
- `'use server'`: https://react.dev/reference/rsc/use-server

RSC implementation details and bundler/framework APIs may not follow ordinary React semantic versioning. Check the framework's exact supported React/RSC packages.

## React Compiler

- React Compiler introduction: https://react.dev/learn/react-compiler
- Installation: https://react.dev/learn/react-compiler/installation
- Incremental adoption: https://react.dev/learn/react-compiler/incremental-adoption
- Debugging and troubleshooting: https://react.dev/learn/react-compiler/debugging
- Compiler configuration: https://react.dev/reference/react-compiler/configuration
- Compiler directives: https://react.dev/reference/react-compiler/directives
- `'use memo'`: https://react.dev/reference/react-compiler/directives/use-memo
- `'use no memo'`: https://react.dev/reference/react-compiler/directives/use-no-memo
- `eslint-plugin-react-hooks`: https://react.dev/reference/eslint-plugin-react-hooks
- `memo`: https://react.dev/reference/react/memo
- `useMemo`: https://react.dev/reference/react/useMemo
- `useCallback`: https://react.dev/reference/react/useCallback

Do not assume the compiler makes every manual memoization redundant. Verify compiler diagnostics, production output, API identity contracts, and measured behavior.

## React testing and deprecations

- `act`: https://react.dev/reference/react/act
- `react-test-renderer` warning: https://react.dev/warnings/react-test-renderer
- React DOM Test Utils warning: https://react.dev/warnings/react-dom-test-utils
- Testing overview (legacy but useful migration context): https://legacy.reactjs.org/docs/testing.html

## Testing Library

- Guiding principles: https://testing-library.com/docs/guiding-principles/
- Query priority: https://testing-library.com/docs/queries/about/
- `ByRole`: https://testing-library.com/docs/queries/byrole/
- `ByTestId`: https://testing-library.com/docs/queries/bytestid/
- Async methods: https://testing-library.com/docs/dom-testing-library/api-async/
- User Event introduction: https://testing-library.com/docs/user-event/intro/

Testing Library is an ecosystem tool, not a React requirement. Use the repository's established test stack when it provides equivalent behavior-oriented coverage.

## Web platform, HTML, and accessibility

- HTML Living Standard: https://html.spec.whatwg.org/
- WAI-ARIA 1.2: https://www.w3.org/TR/wai-aria-1.2/
- ARIA Authoring Practices Guide: https://www.w3.org/WAI/ARIA/apg/
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- WCAG 2.2 Quick Reference: https://www.w3.org/WAI/WCAG22/quickref/
- Accessible Name and Description Computation: https://www.w3.org/TR/accname-1.2/
- MDN accessibility guides: https://developer.mozilla.org/en-US/docs/Web/Accessibility
- MDN forms accessibility: https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/How_to_structure_a_web_form
- `prefers-reduced-motion`: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- `inert`: https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/inert

Native HTML semantics and browser behavior take precedence over re-created patterns. ARIA does not add browser interaction automatically.

## Browser security and content safety

- MDN XSS overview: https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/XSS
- MDN `innerHTML`: https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML
- MDN Content Security Policy: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP
- MDN Trusted Types API: https://developer.mozilla.org/en-US/docs/Web/API/Trusted_Types_API
- MDN `postMessage`: https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage
- MDN Subresource Integrity: https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity
- OWASP XSS Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
- OWASP DOM-based XSS Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html
- OWASP CSRF Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
- OWASP Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- OWASP Web Security Testing Guide: https://owasp.org/www-project-web-security-testing-guide/

## React security advisories

- React Server Components security advisory (December 2025): https://react.dev/blog/2025/12/03/critical-security-vulnerability-in-react-server-components
- Follow-up React Server Components vulnerabilities: https://react.dev/blog/2025/12/11/denial-of-service-and-source-code-exposure-in-react-server-components
- React security advisories: https://github.com/react/react/security/advisories

When reviewing RSC-capable software, check current advisories and framework notices at review time. Do not preserve a static patched-version list in the operational rules.

## TypeScript and JavaScript modules

- TypeScript JSX: https://www.typescriptlang.org/docs/handbook/jsx.html
- TSConfig reference: https://www.typescriptlang.org/tsconfig/
- TypeScript module reference: https://www.typescriptlang.org/docs/handbook/modules/reference.html
- Package `exports` and Node.js packages: https://nodejs.org/api/packages.html

Honor repository-local TypeScript versions and strictness. Runtime validation remains necessary at untrusted boundaries.

## Package managers, build tools, and client environment

- npm scripts: https://docs.npmjs.com/cli/v11/using-npm/scripts/
- npm package specification: https://docs.npmjs.com/cli/v11/configuring-npm/package-json
- pnpm scripts: https://pnpm.io/cli/run
- Yarn scripts: https://yarnpkg.com/features/scripting
- Vite environment variables and modes: https://vite.dev/guide/env-and-mode

Install, build, test, lint, Storybook, and code-generation commands can execute repository-controlled code.

## Practitioner references used for prioritization

These sources informed performance and composition prioritization but do not override React, framework, browser, or accessibility specifications:

- Vercel React Best Practices announcement: https://vercel.com/blog/introducing-react-best-practices
- Vercel React Best Practices skill: https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices
- Vercel Composition Patterns skill: https://github.com/vercel-labs/agent-skills/tree/main/skills/composition-patterns

The skill deliberately avoids copying Vercel's framework-specific recommendations into framework-neutral React rules. Apply Next.js-specific guidance only inside a Next.js repository and after checking its installed version.

## Maintenance policy

When updating this skill:

1. Preserve repository-local policy precedence and the non-dogmatic stance.
2. Verify stable versus Canary status and exact React minor availability.
3. Re-check React 18/19 migration and TypeScript behavior.
4. Re-check current React/RSC security advisories and framework patch guidance.
5. Verify React Compiler configuration and lint behavior against current official docs.
6. Verify testing API deprecations and established ecosystem guidance.
7. Re-check HTML, WCAG, ARIA, browser-security, and browser-support claims.
8. Remove stale or duplicated recommendations rather than accumulating alternatives.
9. Keep `SKILL.md` small enough for progressive disclosure; route detail to focused references.
10. Run skill-format validation, local-link checks, and all scenarios in `EVALUATION.md`.
11. Update `metadata.version` and `metadata.last-reviewed` in `SKILL.md`.
