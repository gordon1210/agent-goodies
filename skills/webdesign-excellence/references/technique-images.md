# Technique: image treatment, masks, and color restraint

**Load when:** photography needs consistent art direction, focal control, or a meaningful reveal.

## Fix source quality before filters

Match subject, light, crop, and palette before trying to unify unrelated images
with grayscale. A filter cannot make a poor crop useful. Define the subject that
must remain visible at each aspect ratio. Use separate responsive crops when one
image cannot serve both the wide and narrow layout.

Grayscale can quiet a mixed portfolio so typography leads. Use it only when color
is not essential: never hide a product colorway, safety signal, or meaningful chart
encoding. A transition to color can reward attention, but the baseline must already
communicate the content. Keyboard focus needs equivalent useful feedback.

```css
.work-image {
  display: block;
  inline-size: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
}
@media (hover: hover) and (pointer: fine) {
  .work-image { filter: grayscale(1); }
  .work-link:hover .work-image,
  .work-link:focus-visible .work-image { filter: grayscale(0); }
}
```

This optional specimen leaves touch imagery in color and introduces no motion.
Use a subtle transition only after consulting the motion system and preferences.

## Masks and composition

Use a mask or clip to strengthen the chosen form vocabulary, not to conceal bad
asset edges. Keep the content and hit area understandable. Apply masks to media,
not to whole controls with essential labels. Use a basic rectangular rendering as
fallback. Check the target browser's mask behavior before relying on a complex SVG.

A slow image scale on hover should happen inside a stable frame and never trigger
layout movement. Keep a useful resting crop. Do not combine hover zoom, tilt, blur,
color inversion, and a cursor-following annotation on the same asset by default.

**Fallback:** a well-cropped static image with the same meaning. **Test:** face and
product visibility, different aspect ratios, long captions, touch/focus equivalence,
reduced motion, image failure, and real contrast where text overlays the image.
