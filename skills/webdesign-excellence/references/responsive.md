# Responsive composition, not desktop shrinkage

**Load when:** introducing layout, complex type, sticky content, mobile navigation, or overflow fixes.

## Choose breakpoints where the content fails

Begin with semantic source order and a useful narrow layout. Add columns when the
content has room, not because a framework has a named breakpoint. Test between the
usual presets. A laptop with a short viewport is a different problem from a phone.

Use intrinsic layouts for repeated components. Container queries can adapt a component
to its available width; viewport queries remain appropriate for page-wide behavior.
A container query styles eligible descendants, not the queried container itself.
Size containment can affect layout, so apply it intentionally.

```css
.feature {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: minmax(0, 1fr);
}
.feature-shell { container-type: inline-size; }
@container (min-width: 42rem) {
  .feature { grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); }
}
.feature > * { min-inline-size: 0; }
```

The base layout remains useful without container queries. Establish whether a
rearranged visual stays consistent with reading and tab order.

## Art-direct the small-screen version

Replace a huge composited hero with a purposeful crop and shorter composition,
not unreadable scaled-down artwork. Reorder only when semantics allow it. Use a
static list instead of a pinned story when the viewport cannot display its content.
Keep the primary action reachable; do not hide critical proof, controls, or content
merely to make a layout fit. Choose a real mobile menu, not a disappeared desktop nav.

Treat hover as optional. Test coarse pointers and touch directly; viewport width
is not an input-capability detector. For orientation and browser bars, choose `svh`,
`dvh`, or content-driven sizing by behavior rather than replacing every `vh` blindly.
A minimum height is usually safer than locking text-heavy sections to a viewport.

## Failure probes

Test around 320, 390, 768, 1024, and 1440 CSS pixels as an initial sample, plus the
actual breakpoints and short landscape windows. These are test samples, not a
guarantee of coverage. Check browser zoom and at least 200% text enlargement.
WCAG reflow generally assesses vertical content at 320 CSS pixels without two-axis
scrolling; genuinely two-dimensional content has scoped exceptions.

Contain wide tables or code deliberately with visible access and semantics. Never
use `overflow-x: hidden` on the page as the first fix for a layout defect: it can
mask unreachable content. Test long labels, URLs, translated content, RTL where in
scope, empty states, errors, and the software keyboard.

## Sources

[Ahmad Shadeed: Responsive Design](https://ishadeed.com/article/responsive-design/); [MDN: Container queries](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries); [WAI: Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow).
