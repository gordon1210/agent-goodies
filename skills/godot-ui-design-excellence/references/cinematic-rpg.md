# Cinematic and painterly RPG interfaces

## Identify the relationship between character, world, and decision

Do not treat an RPG interface as one reskinned application. Battle, equipment,
party overview, dialogue, and rewards have different attention requirements.
Establish a shared type/material vocabulary, then give each screen an appropriate
composition. A battle HUD should preserve the readable action; a build screen can
make room for considered comparison.

For an Expedition-33-inspired brief, investigate the useful principles of the
actual reference: authored irregular silhouettes, expressive art/type relationships,
and native information integrated with the composition. Its creator's concepts
are references for analysis, not a library to trace or a guaranteed shipped spec.
The project's own fiction must supply the final marks, symbols, and assets.

## Compose a battle decision

Define stable regions for acting character, action selection, target, resources,
turn/context information, and consequence preview. Do not let a decorative action
wheel conceal important target state. Preserve a predictable action order unless
reordering is itself a clear gameplay mechanic.

A strong pattern is a quiet decision interior framed by a more expressive boundary:
a clean text column over a controlled-value backing, with separate painterly
silhouette pieces beyond the text area. Irregular outer geometry does not require
irregular line spacing or ambiguous hit areas.

During targeting, distinguish candidate, confirmed target, valid area, and invalid
reason. Track the camera's framing changes so HUD and portraits do not hide the
selected enemy or telegraph. Offer a target cycle or list when spatial selection
is difficult.

## Build character and equipment screens around a question

Let illustration establish emotional presence without covering essential comparison.
Use a stable character crop and controlled focal lighting. Separate large display
name from working stats. Make equipment slots, active inspection, and committed
build visibly different. Keep the character composition from shifting every time
an item name wraps.

Avoid decorative dependency chains: text should not need a rendered portrait or a
loaded 3D model before it becomes readable. A preview fallback must preserve all
functional information.

## Motion character

Propose short directional entries, soft settling, masked ornament reveals, or
subtle ink/material changes according to the chosen identity. These are original
options, not measured Expedition 33 timings. Establish the actionable state before
or independently of decorative completion. Repeated navigation should be faster
and calmer than a first entry or major reward.

Keep impact feedback attached to gameplay significance. A rare reward can use a
larger visual event; every inventory hover should not shake the camera or squash
the panel. Reduced-motion mode can retain state through instantaneous emphasis.

## Godot decomposition

Use native Labels/RichTextLabels and Buttons inside bounded layout regions.
Use separate TextureRects or custom drawing for ornament, a restrained ShaderMaterial
for optional reveals, and a dedicated preview surface for a portrait if required.
Share role tokens, not one massive scene containing every menu.

Acceptance: the screen has expressive silhouette and typographic character while
remaining readable over real combat backgrounds, navigable with supported inputs,
and stable with long names and large-text settings.

## Evidence anchors

[D01](sources.md#d01) · [D07](sources.md#d07) · [G12](sources.md#g12) · [G17](sources.md#g17)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
