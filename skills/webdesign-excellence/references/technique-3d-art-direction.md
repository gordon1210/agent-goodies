# Technique: art-directing spatial work

**Load when:** requested depth, geometry, materials, lighting, or camera work needs
visual decisions. For mesh runtime/assets also load [3D production](technique-3d-production.md).
An editorial page can contain one 3D view without changing its primary style.

## Choose the representation that meets the brief

| Representation | Appropriate requirement | Limit |
|---|---|---|
| CSS/DOM 2.5D | Layered panels, tilt, readable interface planes | No real curved volume or physical material response |
| SVG/isometric illustration | Controlled diagram, exact labels, fixed projection | View-dependent drawn occlusion |
| Pre-rendered views | Fixed art-directed viewpoints without inspection | No free camera or arbitrary part selection |
| Existing video | Already-authored movement as media | Playback is not geometry interaction |
| Mesh-based 3D | Real occlusion, volumetric form, changing light/view, part inspection | Asset, rendering, and interaction responsibilities |

Use the least complex adequate representation. Explicit interactive 3D cannot
silently become a stock image or rotating flat card; an unavailable renderer is a
reported limitation, with a useful fallback while required work remains incomplete.
Conversely, a layered interface does not justify installing a renderer.

For CSS depth, `perspective` on a parent gives children a common viewpoint;
`transform-origin` sets the hinge. Apply `transform-style: preserve-3d` along the
necessary non-leaf chain; it is not inherited. Decide whether backs should show
with `backface-visibility`. Inspect ancestors when depth disappears: opacity below
1, filters, masks, paint containment, and overflow other than `visible`/`clip` can
force flattening. Put clipping/effects on an appropriate outer layer, keeping
readable controls outside steeply rotated planes. Test stacking and hit regions.

## Establish a scene contract

Choose the focal object, intended silhouette/proportions, material family, light
mood, projection/framing, page palette and type relationship, motion purpose, copy/CTA
safe areas, and narrow/short composition. If taste is delegated, make these decisions;
ask for missing identity-critical assets, not every roughness or camera choice.

Progress through **asset inspection → blockout → silhouette and framing → material
response and light → visible detail → page integration → choreography → optimization**.
Save intermediate renders. Change one class of variables per diagnostic pass so
the result has an attributable cause. A functioning canvas is not visual acceptance.

## Build recognizable form

Block out the main volume and meaningful component relationships at consistent scale
and orientation. Judge the silhouette at intended display size before subdivision
or textures. Use purposeful proportions, edge treatment, openings, and junctions.
A small bevel can catch light and express manufacture; a giant bevel can erase
identity. Inspect normals and smooth/hard edges under a grazing light. More polygons
do not repair a poor profile. Define pivots by actual movement and name part groups.

Stylized geometry is finished when simplification is consistent, joins and edges
are deliberate, and the intended silhouette reads. Unrefined primitives with
unresolved intersections are placeholders. Do not invent real product internals;
use supplied relationships or label an original conceptual object as such.

## Make materials and lights describe form

Establish distinct surface responses: a coated shell, a less reflective gasket,
and a metal accent should not all look like glossy plastic. Inspect broad highlights
while varying roughness; metalness represents metallic versus dielectric response,
not a universal shininess knob. Match texture scale to the object. Transmission and
clearcoat need a specific material reason; thickness and closed surfaces matter for
intended volumetric transmission. Prefer opaque materials when transparency adds
no information.

Use a key or environment to establish readable planes; add fill only to recover
necessary detail, and rim/reflection contrast only where the silhouette merges
with the background. Ground the object with visible contact and deliberate shadow
softness. Environment reflections describe shiny surfaces; an HDRI is not an
unexplained quality setting. Bloom cannot fix exposure or missing shape.

If flat, temporarily inspect a neutral material under one directional light, then
restore materials. If detached, inspect ground distance, shadow placement, and
scale. If washed out, inspect exposure/tone mapping, color-space handling, normals,
and light intensity separately. If transparent faces pop, inspect draw ordering,
intersections, sidedness, and whether an opaque or transmission solution better
fits the intended substance. Diagnose before adding effects.

## Frame the scene in the page

Orthographic projection maintains parallel scale for diagrams. Perspective expresses
depth; field of view and camera distance jointly set apparent proportions. A
moderate vertical FOV around 30–45 degrees is a studio starting heuristic, not a
requirement. Increase distance and refit instead of using an extreme wide angle
to squeeze in the object. Set a meaningful target; keep near/far planes as tight
as the full movement permits, with a positive perspective near plane.

Fit the union of relevant animated bounds to the actual available canvas area.
Project bounds at sampled states and check them against copy and controls, not just
the screen edge. Camera movement changes the whole scene; object movement explains
a part. Avoid both moving during a critical handoff unless the resulting path stays
readable. Land with a stable focal subject, not endless orbit.

For narrow screens, move copy outside the canvas and refit the camera. For short
screens, reduce occupied height or use a different sequence without pinning. Change
layout/projection when needed rather than scaling annotations to illegibility.
Depth and occlusion must never hide the primary action.

## Three original look recipes — opt in

| Look | Construction and starting relationships | Camera and motion | Failure signs / avoid when |
|---|---|---|---|
| Restrained studio product | Purposeful shell bevel, inset seams, limited accents. Try dielectric roughness .35–.65 against a rougher base; metal only on plausible metal parts. Broad highlight, weaker fill, grounded contact. | Moderate perspective, slight three-quarter view; one reveal then stillness. | Plastic look → separate roughness and inspect highlights; floating → fix contact. Avoid when engineering relationships need equal-scale projection. |
| Precise technical reveal | Named parts and truthful assembly axes; neutral opaque surfaces, one accent for active component. Even enough fill to retain edges, directional key for depth. | Orthographic or mild perspective; retain base, separate one layer, annotate, return from original transforms. | Confetti explosion → shorten offsets/group parts; invisible gaps → change view. Avoid without verified internals for a real product. |
| Expressive editorial space | Original sculptural silhouette, intentional negative space, limited material contrast. One colored light or reflective accent relates to page palette; quieter environment. | Compose object weight opposite headline; controlled arc to a readable landing, typography remains stable. | Decorative soup → remove competing motion/materials; unreadable type → restore safe area. Avoid for frequent task UI or a restrained existing brand without a fitting scope. |

All ranges and recipes are tunable design heuristics, not measured quality formulas.

**Verify:** inspect wide, narrow, short, assembled/detail states and playback; compare
silhouette, proportions, contact, material separation, camera clipping, typography,
annotations, and controls. Review at actual size, not only a large render. A pleasing
still does not prove good movement or interaction. **Fallback:** accurate labeled
views or semantic diagrams preserving the message; retain an explicit 3D requirement
as incomplete if its required interaction cannot run.

## Sources

API/representation details reviewed 2026-09-09:
[MDN transform-style](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/transform-style),
[Three.js PerspectiveCamera](https://threejs.org/docs/pages/PerspectiveCamera.html),
[glTF overview](https://www.khronos.org/gltf/).
Scene contracts, diagnostic ordering, and look recipes are original guidance.
