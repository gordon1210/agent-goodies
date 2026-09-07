# Color, surfaces, and theme ownership

**Load when:** defining a palette, fixing contrast, or shaping elevation and dark/light themes.

## Name roles before colors

Use semantic roles such as canvas, surface, elevated surface, text, muted text,
border, accent, accent text, focus, success, warning, and danger. Do not encode the
brand hue into the role name. One accent is a useful restraint for some directions;
a multi-color graphic identity is equally valid when roles and contrast are controlled.

Separate decorative lines from interactive boundaries. A subtle hairline may organize
a page but cannot be the only necessary cue for a control when it is too faint.
A shadow is not automatically bad, nor is a border automatically sufficient.
Pick a surface grammar: flat planes, restrained elevation, hard offset layers, or
translucent chrome. Avoid combining all four without explicit ownership.

## Contrast is a rendered relationship

Check normal text at 4.5:1 and qualifying large text at 3:1, respecting the standard's
exceptions. Large text is at least 18pt regular or 14pt bold, approximately 24px or
18.67px in CSS terms. Required non-text UI cues generally need 3:1 against adjacent
colors, subject to the criterion's scope and exceptions. Do not apply that rule to
every decorative divider, and do not exempt all muted metadata.

Opacity, gradients, images, and blending change the effective background. Measure
worst intended states rather than a palette swatch. Glass over media needs a stable
readable surface or scrim. Thin glyphs may need more contrast than the threshold
suggests. Do not represent status with color alone.

## Theme deliberately

Map semantic tokens per theme instead of inverting screenshots. Reassess imagery,
shadows, focus, borders, and charts. Use system color preferences when the product
calls for them; an authored campaign does not automatically need a theme toggle.
If a user override exists, preserve it and avoid a flash of the wrong theme.

Perceptual color spaces can help author ramps, but equal lightness steps are not a
contrast guarantee. Add advanced color syntax only when it fits supported browsers,
with a fallback where needed. Do not replace WCAG 2.2 checks with a different
contrast algorithm while claiming WCAG conformance.

**Checks:** all meaningful text roles and control states; bright and dark media;
forced colors; charts without color; disabled versus unavailable explanations;
hover/focus text after any inversion or grayscale treatment.

## Sources

[WAI: Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html); [WAI: Non-text Contrast](https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html); [MDN: forced-colors](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/forced-colors).
