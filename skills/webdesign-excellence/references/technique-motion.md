# Technique: a coherent motion system

**Load when:** introducing animation, changing interaction timing, or reviewing motion quality.

For a coordinated multi-phase scene, load [choreography](technique-choreography.md).
A local transition fix stays here and reuses existing tokens.

## Classify the job

Use motion to acknowledge input, explain a state or spatial relationship, guide
attention, or support a narrative. A visual identity may have expressive moments,
but repeated task interactions should stay economical. Do not animate simply because
an element entered the viewport. A still interface is a valid finished design.

Define a small vocabulary rather than forcing one curve onto every behavior.
Entrances can decelerate, dismissals can be brief, and directly manipulated objects
may need a damped spring. Linear motion fits uniform progress or a conveyor, not
all interactions. Keep transition origins related to the triggering control.

## Original starting tokens — tune, do not worship

```css
:root {
  --motion-feedback: 140ms;
  --motion-state: 220ms;
  --motion-reveal: 560ms;
  --ease-enter: cubic-bezier(.2, .8, .2, 1);
  --ease-exit: cubic-bezier(.4, 0, 1, 1);
}
```

These are house starting points, not measured universal optima. Feedback generally
belongs in roughly 100–200ms, ordinary state motion around 160–300ms, and occasional
editorial reveals around 400–700ms. Longer movement needs an actual narrative reason.
Controls must work immediately, not after their animation completes.

Make transitions interruptible. Repeated clicks, opening then immediately closing,
route changes, and preference changes must settle to the correct state. Never add
a fake network delay to show off a spinner. Base pending and success on real operations.
Bound total stagger delay rather than multiplying an attractive delay by fifty items.

## Accessibility and lifecycle

Provide a reduced-motion design, not a global .001ms hack. Remove large displacement,
parallax, zoom, and decorative loops; retain immediate state changes and useful
non-spatial feedback. Make essential content visible with motion disabled. Do not
make application logic depend solely on an animation-end event that may never fire.

Pause invisible work. Clean up listeners, timelines, observers, and frame loops.
Prefer transform and opacity for cheap motion where possible, but profile actual
compositing, paint, and layer costs. Large layers and filters can still be expensive.
Animating height may be justified for a small disclosure; do not categorically ban
it or assume every CSS animation is compositor-only.

**Test:** interruption, rapid interaction, keyboard usage, reduced motion changed
at runtime, busy main thread, low-end device, hidden tab, resize, and zero-animation
fallback. Reject motion that makes frequent actions feel ceremonially slow.

## Sources

[Emil Kowalski: Great Animations](https://emilkowal.ski/ui/great-animations); [Carbon: Motion](https://carbondesignsystem.com/elements/motion/overview/); [web.dev: High-performance CSS animations](https://web.dev/articles/animations-guide); [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/prefers-reduced-motion).
