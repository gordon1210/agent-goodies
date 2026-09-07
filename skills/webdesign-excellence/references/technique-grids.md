# Technique: structural grids, hairlines, and bento

**Load when:** the content needs visible structure, deliberate asymmetry, or heterogeneous tile composition.

## Use the grid for a reason

A structural grid exposes alignment or shared boundaries. A decorative background
grid supplies atmosphere only. Do not pretend these are interchangeable. A bento
layout is useful when different kinds of content deserve different spans; it is
not the default for a list of equal features.

Map each item to a communication role before choosing its span. Give the most
important item enough space for meaningful content, not an empty giant rectangle.
Keep related labels and images aligned across cells. Avoid dense auto-placement
that changes visual order relative to source and keyboard order.

## Shared hairline planes

```css
.system-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 1px;
  border: 1px solid var(--divider);
  background: var(--divider);
}
.system-grid > article {
  min-inline-size: 0;
  padding: clamp(1.25rem, 2vw, 2.5rem);
  background: var(--surface);
}
@media (min-width: 48rem) {
  .system-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
```

Define the tokens in the selected system. Opaque cells prevent the grid background
from tinting content. At responsive breakpoints, inspect all seams and unfinished
rows. For irregular mosaics, a simple shared-gap trick can leave unwanted filled
areas; use explicit borders or a deliberate region background instead of forcing it.

## Asymmetry and background grids

Use a stable alignment spine and unequal spans only where hierarchy supports them.
Avoid arbitrary per-card radii as a substitute for composition. Keep a conventional
row or table when comparison is the job. Decorative grid layers belong behind the
content, ignore pointer events, and should not enter the accessibility tree.

A masked CSS background can fade a grid away from the focal point, but the page
must remain legible without the mask. Start with 1 CSS pixel structural lines;
subpixel lines can look inconsistent at different zoom and device pixel ratios.
Distinguish a quiet decorative line from a necessary control boundary.

**Fallback:** one-column content flow with useful local separators. No image, text,
or CTA becomes inaccessible because its designed span disappeared.

**Test:** source order, long content, odd item counts, zoom, background seam artifacts,
forced colors, and real control contrast. Delete the visible grid if it competes
with the information rather than clarifying it.
