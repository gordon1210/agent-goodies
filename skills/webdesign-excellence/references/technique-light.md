# Technique: atmospheric light and robust glass

**Load when:** a selected design needs blur, light fields, translucent chrome, or local glow.

## Separate the jobs

A glow behind a focal object directs attention. A blurred background color field
creates atmosphere. A translucent control plane explains layering. Do not combine
these automatically. Keep useful text and controls optically quiet.

Begin with an opaque, readable surface. Add blur as enhancement, not as the thing
that makes white text readable. For known backdrops, choose a sufficiently strong
tint and test the full background range. For uncontrolled imagery, preserve a
stable opaque text region or scrim.

```css
.glass-toolbar {
  background: var(--surface-opaque);
  color: var(--text-on-surface);
  border: 1px solid var(--control-border);
}
@supports (backdrop-filter: blur(1px)) {
  .glass-toolbar[data-material="glass"] {
    background: var(--surface-glass-readable);
    backdrop-filter: blur(12px);
  }
}
@media (prefers-reduced-transparency: reduce), (forced-colors: active) {
  .glass-toolbar[data-material="glass"] {
    background: var(--surface-opaque);
    backdrop-filter: none;
  }
}
```

Define all tokens in the actual theme. The readable glass token must be validated
against the intended backdrops; it is not a magic universal alpha. Reduced-transparency
support varies, so the opaque baseline and readable enhanced state remain necessary.
Provide an in-product reduced-effects option only when justified by the experience.

## Rendering discipline

Limit filtered area and nesting. Prefer a pre-rendered blurred image or static
radial gradients where equivalent. Keep glow behind the target rather than blurring
the target's text. Avoid animating blur radius or multiple full-viewport color fields
without profiling. Be aware that backdrop roots and stacking contexts can affect
which content is sampled; inspect the actual composition.

A border or highlight can suggest a material edge. Do not describe a blurred rectangle
as physical refraction. Use shader-based materials only when the rendering route
justifies their cost and provides fallback.

**Fallback:** an opaque, clearly bounded surface with all controls intact.
**Test:** brightest/darkest backdrop, scrolling content behind the plane, unsupported
filtering, reduced transparency, forced colors, low-end compositing, and focus outlines.

## Sources

[MDN: backdrop-filter](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter); [MDN: prefers-reduced-transparency](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/prefers-reduced-transparency); [MDN: forced-colors](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/forced-colors).
