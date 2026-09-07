# Technique: sticky card stacks

**Load when:** an ordered portfolio or short visual sequence benefits from a layered deck metaphor.

## Use only when the metaphor helps

Stacking cards can express progression through a small set of projects. It is a
poor substitute for a searchable catalog, a comparison table, or a set of task
controls. The visual overlap must not remove access to content or focusable elements.

## Build from normal flow

Render the cards as an ordered sequence. Give each enough height for its actual
content. Only enable sticky behavior when the viewport width and height can show
the complete relevant card area. Sticky needs an inset and enough space in its
containing block; inspect overflow and scrolling ancestors before blaming z-index.

Use a wrapper for sticky positioning and a child for scale or brightness changes.
This separates the geometry used for scroll calculations from the element being
transformed. Increase stacking order deliberately. Compute progress from the
approaching card's measured position and clamp it to 0–1. Recalculate after image,
font, or layout changes rather than caching stale dimensions forever.

Keep the layering quiet: a small scale reduction and subtle overlay can indicate
that an earlier card recedes. Tune the amount to the content; never dim essential
text below readable contrast merely to exaggerate depth. A sticky-only version may
be enough, with no scroll-linked transform at all.

## Focus and content risks

An overlapped card can contain a link that receives keyboard focus behind the next
card. Solve that explicitly: prefer non-overlapping interactive regions, disable
stacking for focus navigation where appropriate, or provide a normal list instead.
Do not blindly toggle `inert` on scroll and unexpectedly remove the user's focus.
Do not put the only project description in an area that becomes permanently covered.

Check the final card and the next section. The deck should naturally release into
normal content, not leave a large dead spacer or a pinned layer over the footer.
If the motion or viewport conditions change, remove inline transforms and restore
ordinary layout and reachable content.

**Fallback:** normal non-overlapping project cards. This is the default for reduced
motion or insufficient available height when stacking would obscure information.
**Test:** rapid scroll, keyboard tabbing through every card, 200% text size, long
project names, loaded images, mobile landscape, last-card release, and back navigation.

**Reject the technique** if making the deck accessible requires more interaction
complexity than its narrative value justifies.

## Sources

[MDN: position](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/position); [WAI: Focus Not Obscured (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html).
