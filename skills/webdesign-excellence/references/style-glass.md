# Style: layered glass and translucent chrome

**Load when:** glass is an explicit primary direction or a carefully bounded brand surface treatment.

## Design thesis

Use translucency to express that a control plane floats above content. It is not
a reason to make all information transparent. This dossier describes a web design
approach, not pixel-identical reproduction of a platform's proprietary material.

## Grammar to establish

Separate background content, translucent chrome, and opaque reading surfaces.
Give the chrome a consistent tint, edge treatment, corner family, and restrained
depth. Maintain enough surface opacity to protect labels. Choose a controlled
background where material variation is meaningful but not chaotic.

Reflection, refraction, blur, translucency, and a white highlight are different
visual mechanisms. `backdrop-filter` alone is not a physically accurate glass
renderer. Do not promise a platform material just because a CSS blur exists.

## Concrete composition

A navigation bar over photography, a compact media control strip, or a floating
workspace toolbar can communicate layering usefully. Keep article text, forms,
and dense tables on stable content surfaces. A glass-led landing page still needs
an actual proposition and a focal image or product view.

Establish the opaque baseline first. Add the material only to selected components
when the background and performance budget support it. Use the light/glass technique
module for fallbacks and contrast strategy.

## Optional techniques and boundaries

Subtle depth transitions and responsive content cropping may fit. Dynamic
refraction, shader highlights, and pointer-following light are expensive optional
mechanisms, not required signs of quality. Do not nest several independent
backdrop filters or use blurred text as a material cue.

**Avoid:** low-alpha cards on arbitrary images; glass within glass within glass;
controls whose hit area is unclear; all-white text regardless of backdrop;
large animated blur radii; depending only on a limited-support transparency preference.
Do not pair hard offset brutalist shadows with soft glass without a scoped rationale.

## Adaptation and acceptance

Test scrolling, bright/dark media, disabled filtering, forced colors, and long labels.
Provide stable opaque surfaces when the material cannot be used. On low-end devices,
removing blur should preserve the structure and control affordance.

**Pass:** translucency explains spatial hierarchy, not just decoration; text remains
readable across the actual backdrop; the opaque version is fully usable.

## Sources

[MDN: backdrop-filter](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter); [MDN: prefers-reduced-transparency](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/prefers-reduced-transparency).
