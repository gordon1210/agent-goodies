# Technique: carousels, marquees, and horizontal sequences

**Load when:** a collection genuinely benefits from a bounded horizontal presentation.

## Distinguish browsing from decoration

A carousel is interactive browsing. A marquee is usually an automatically moving
strip. A horizontal narrative driven by vertical scrolling is a third, higher-cost
interaction. Do not choose one merely to avoid editing a large collection.

For related images or products, a native overflow region with optional scroll snap
and visible previous/next controls can be simpler than a carousel engine. Essential
content should be discoverable without dragging. Avoid strict snapping that prevents
access to an oversized item. Keep page scroll behavior familiar.

## Interaction design

Use real buttons with names and disabled or unavailable states where appropriate.
Make slide position understandable without a row of tiny unlabeled dots. Do not
move focus automatically when the user scrolls. If controls change which item is
shown, preserve a sensible focus position and announce only useful changes.

Pause automatic movement when the user interacts, but do not rely on hover alone
as the pause mechanism. Supply a keyboard-operable pause/stop control when required.
Reduced-motion behavior should use a static grid/list or user-controlled sequence.
Do not restart motion unexpectedly after the user chose to stop it.

## Seamless loops without duplicate semantics

Repeated visual copies can make a loop seamless. Decorative duplicates must not
repeat accessible content or tab stops. Do not put `aria-hidden` around still-focusable
links; make decorative clones truly non-interactive. Keep one canonical readable
and operable collection. Measure after fonts and images load, and inspect the seam
at multiple widths.

For a logo strip, use only authorized real logos. Do not turn anonymous sample
companies into implied customers. A stationary trust row is often clearer and cheaper.
For a long catalog, prefer filtering or pagination to an endless sideways ribbon.

**Fallback:** a useful static or manually scrollable collection in source order.
**Test:** keyboard controls, touch scrolling, pause persistence, reduced motion,
long items, duplicate tab stops, blocked images, and horizontal overflow boundaries.

## Sources

[WAI: Pause, Stop, Hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html); [WAI-ARIA Authoring Practices patterns](https://www.w3.org/WAI/ARIA/apg/patterns/).
