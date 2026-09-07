# Technique: choosing SVG, Canvas, and WebGL

**Load when:** a diagram, generative visual, shader, particle field, or 3D scene is under consideration.

## Pick the least expensive adequate representation

| Need | Candidate | Why not automatically use the next tier? |
|---|---|---|
| Static rich visual | Responsive image or pre-rendered scene | No permanent renderer needed |
| Meaningful vector diagram | SVG plus semantic text | DOM relationships and scaling may matter |
| Many decorative 2D marks | Canvas 2D | Avoid excessive DOM nodes |
| Real 3D inspection or shader effect | WebGL through an appropriate existing library | GPU, asset, and lifecycle cost needs a reason |

Do not create a full rendering engine for a radial gradient. Conversely, do not
force thousands of animated DOM nodes into an effect whose actual job is a particle
field. A visually spatial style can still be delivered with static renders.

## Rendering contract

Specify the effect's purpose, visible area, quality tiers, frame budget, resource
budget, and static fallback. Cap device pixel ratio based on profiling rather than
blindly rendering at the device maximum. Test realistic GPU memory and fill-rate
cost. Avoid unnecessarily oversized textures and transparent layers.

For responsive canvas sizing, distinguish CSS dimensions from backing resolution.
Handle resize, initialization failure, context loss, and teardown. Dispose textures,
geometries, materials, observers, and event listeners according to the actual library.
Stop rendering static scenes on every frame; render on demand where possible. Pause
animation off-screen and when the document is hidden.

## Semantics and interaction

Keep the site's headings, links, purchase controls, and explanation in HTML. If a
canvas conveys meaningful relationships, provide an equivalent understandable
representation. Keyboard and touch users must be able to perform the actual task,
not merely see a poster of inaccessible functionality.

Limit camera movement and make controls discoverable. Do not require dragging as
the only way to perform an essential action. A static fallback must explain the
same core content and preserve the next action.

**Fallback:** a designed image, diagram, or alternate semantic view. **Test:** real
low-end hardware, throttled CPU, high/low pixel density, slow assets, context loss,
reduced motion, pointer cancellation, keyboard alternatives, and repeated mount/unmount.
A fast desktop recording does not establish production readiness.

## Sources

[MDN: WebGL best practices](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices).
