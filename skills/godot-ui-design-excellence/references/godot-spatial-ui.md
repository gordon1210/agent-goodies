# Godot portraits, previews, and world-space UI

## Choose the least expensive representation that fits

A still portrait, pre-rendered sequence, animated 2D composition, and live 3D preview
are different production choices. Use live rendering when its changing pose,
equipment, lighting, or interaction matters—not merely to claim sophistication.
Keep a fallback that preserves all functional information when art is unavailable.

For a live preview, separate its scene, camera, lighting, and material environment
from menu text. Choose a camera crop that leaves space for labels and avoids
clipping unusual equipment. Normalize framing by designed bounds or authored
poses, not by arbitrary scale changes per character.

## SubViewport contract

A SubViewport needs a usable size and an explicit way to display its output,
usually a ViewportTexture in the intended composition. Decide update mode and
rendering resolution deliberately. Stop or reduce work for hidden previews where
appropriate; confirm update behavior when reopened. A transparent preview needs
correct background and compositing settings.

Do not render every inventory thumbnail through an always-updating live viewport.
Cache or pre-render stable images when that fits the design. Measure memory and
frame time on the actual target. Avoid letting a high-cost character preview
reduce the readability or responsiveness of the UI around it.

## World-space information

Define whether an element is diegetic, spatially attached, or a screen-space cue
for a world object. This determines occlusion, distance scaling, accessibility,
and input behavior. A marker behind the camera should not project as a plausible
on-screen target; handle visibility and edge-clamping intentionally.

Keep important content readable under camera motion. For interactive world panels,
map pointer coordinates through the actual surface projection before dispatching
GUI input. Do not assume rendering a Control on a 3D surface automatically produces
correct interaction. Provide an alternate inspection path where perspective or
occlusion prevents access.

## Composition and effects

Protect text from depth of field, motion blur, dramatic exposure, or scene effects
when those would impair reading. A world-space fallback can be a stable screen-space
inspector, not necessarily a duplicated permanent HUD. When a menu animates the
camera, reserve safe composition regions for both the subject and decision UI.

Acceptance: inspect the largest and smallest relevant subjects, rapidly switch
between previews, close during loading, resize, and run over demanding gameplay.
Confirm that stale assets cannot appear under another character's name, the selected
object stays identifiable, and a missing preview does not block the decision.

## Evidence anchors

[G18](sources.md#g18) · [G20](sources.md#g20) · [G21](sources.md#g21) · [G28](sources.md#g28) · [G32](sources.md#g32)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
