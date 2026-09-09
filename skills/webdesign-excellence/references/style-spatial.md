# Style: immersive spatial design

**Load when:** immersive spatial design is the selected primary style; one 3D section alone does not select it.

## Design thesis

Use space to communicate something a flat view cannot show as effectively. This
may be a physical product, a relationship among objects, or an authored narrative.
A rotating abstract object alone is not a reason to choose a spatial architecture.

## Grammar to establish

Define one visual world: material, lighting, camera, depth range, and focal object.
Keep DOM typography and controls in a stable readable layer. Match the rendered
object's light and palette to the rest of the page rather than pasting an unrelated
3D asset into a conventional landing template.

Pick a purposeful camera behavior. Inspection, a constrained rotation, or a guided
chapter can be meaningful; unrestricted camera motion is often unnecessary for
marketing. Do not require fine pointer control to understand or purchase anything.

## Concrete composition

For a physical product, begin with a legible object view and clear proposition.
Offer optional rotation or a detail selection, then connect each selected detail to
plain-language content. Keep specifications and the primary action outside the
renderer. A static set of views may be a better implementation than real-time 3D
when the brief does not require interactive 3D.

## Optional techniques and boundaries

Use the rendering module to choose SVG, pre-rendered media, Canvas, or WebGL by
purpose. A spatial identity can be executed with still renders and CSS layering;
it does not require a particular library. Keep camera movement, scroll narration,
and pointer response from competing for control of the same experience.

**Avoid:** continuous rendering with no visible change; an unbounded particle count;
loading the scene before the page can be read; a full-site canvas; essential text
in textures; blocked navigation until assets finish; assuming flagship-GPU results
represent real devices.

## Adaptation and acceptance

Prepare meaningful static views, not a blank rectangle. Handle initialization failure,
context loss, resize, visibility changes, and reduced motion. Scale quality by measured
cost; do not infer hardware capability from a small screen. Keep all core tasks
available without 3D and expose an equivalent explanation of spatial information.

**Pass:** space improves understanding, controls remain accessible, and the fallback
is a complete designed experience rather than a technical error state.

## Sources

[MDN: WebGL best practices](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices).
