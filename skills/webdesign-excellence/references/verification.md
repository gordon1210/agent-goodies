# Verification and evidence before handoff

**Load when:** completing an implementation, substantial refinement, or evidence-based review.

## Keep verification proportional and real

For a targeted fix, check the changed component, affected states, relevant widths,
and nearby regressions. For a new page, verify the full composition and primary
flow. Do not install testing packages or run arbitrary project scripts without
inspecting them and respecting repository policy.

Use available browser tooling. If it is unavailable, perform static checks and say
which browser behavior remains unverified. Never claim to have viewed screenshots,
run a build, or tested assistive technology when that did not happen.

## Minimum evidence set for a new page

- **Composition:** wide and narrow views plus a full-page review. Include long
  content and the actual media/font state, not only ideal placeholders.
- **Operation:** primary action, keyboard navigation, visible focus, forms, open
  overlays, and relevant pending/success/failure states.
- **Constraints:** reduced motion, zoom/reflow, a short viewport, missing/slow assets,
  and supported-browser checks proportional to the features used.

Test around intended breakpoints and between them. Confirm no horizontal overflow
except deliberate two-dimensional regions. Inspect touched controls in forced colors
when custom borders, shadows, or transparency may hide their affordance.

## Tools and limits

Use the project's build, typecheck, lint, and existing tests. Record exact commands
and results. A passing build does not establish design quality. Automated accessibility
checks catch only part of the problem; verify interaction manually. Local performance
audits do not establish real-user percentile metrics.

Visual regression tests need a controlled viewport, browser, operating environment,
fonts, data, and motion state. Wait for meaningful readiness rather than arbitrary
sleep durations. Screenshots with animations disabled are useful for layout, but
also inspect real motion separately. Review baseline changes instead of accepting
every new screenshot automatically.

Compare source order with the accessibility tree for split text, duplicated marquees,
responsive reordering, dialogs, and custom controls. Test rapid interruption for
animated state changes. Revisit the final state after back navigation and resize.

## Completion gates

No known blocked primary flow, hidden required content, fabricated success, or
unreachable control. Selected style invariants remain coherent. Optional effects
have usable fallbacks. No unexplained dependency or unapproved external request.
Known limitations are explicit rather than disguised by screenshots.

**Handoff:** what changed; selected direction or preserved system; verified commands
and states; actual screenshots or measurements when captured; remaining limitations.
Do not write a universal “production-ready” claim from a small local check.

## Sources

[Playwright: Visual comparisons](https://playwright.dev/docs/test-snapshots); [WAI-ARIA Authoring Practices patterns](https://www.w3.org/WAI/ARIA/apg/patterns/); [web.dev: Web Vitals](https://web.dev/articles/vitals).
