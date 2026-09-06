# Godot rendering: artwork and effects without losing UI semantics

## Prefer the simplest layer that achieves the design

Use a native fill/StyleBox for readable structure, texture or vector-imported art
for authored boundaries, custom drawing for deliberate geometry, and a shader only
for effects that need it. Complexity is not a proxy for premium visual quality.
Keep Labels and semantic Controls above decorative effect layers when possible.

Custom drawing should expose meaningful minimum size, request redraw when needed,
and preserve interaction/accessibility through native controls or explicit semantics.
A shader changing visible shape does not automatically change hit testing or focus.

## A mask-driven ornament reveal

An optional original shader is bundled at
[masked_ornament.gdshader](../examples/masked_ornament.gdshader). It modulates alpha
using a grayscale mask; it is intended for decorative artwork, not text or a whole
interactive panel. It is documentation-reviewed but not compiled in Godot here.
Supply and validate your own mask texture; no art asset is bundled.

Keep each material's runtime state independent where components animate separately.
Mutating a shared ShaderMaterial uniform changes all users of that material.
Use intentional resource instances or a supported per-instance mechanism for the
actual engine version. Never claim a material is local simply because two nodes
have different names.

## Screen-reading and blur hazards

Godot 2D screen-reading shaders use a captured screen buffer. Multiple overlapping
readers do not necessarily see the progressively composited result you expect;
BackBufferCopy and node order can matter. Blur needs appropriate sampling/mipmap
behavior and sufficient copied bounds. Verify the renderer and version.

Do not stack fullscreen readers casually. Measure cost at target resolution and
check transparent edges, bleeding, and stale regions. An opaque or controlled-alpha
backing is a useful fallback. Blur is not an accessibility guarantee over every
scene and cannot repair intrinsically tiny text.

## Texture fidelity

Inspect alpha, compression artifacts, filtering, scale, texture padding, and
mipmap behavior at final play size. Fine grain can alias and shimmer. A brush edge
can look convincing at source size but turn to mud on a smaller panel. Keep a
low-effects option and test that it retains the approved grammar.

Separate opacity intended for a decorative layer from opacity applied to all
children. Fading an entire ancestor can accidentally reduce focus and text contrast.
Be explicit about canvas layering, clipping, and the lifetime of temporary effects.

## Performance and acceptance

Profile transparent overdraw, fullscreen samples, and additional viewports under
real gameplay load. A small editor preview is not target hardware evidence. Prefer
bounded effects and shared immutable assets; optimize based on measurement instead
of rewriting every widget into a custom renderer.

Acceptance: the effect strengthens the visual direction, does not obscure state,
has correct compositing in overlapping panels, survives scaling, and has a readable
fallback. Record any renderer-specific limitation rather than hiding it.

## Evidence anchors

[G08](sources.md#g08) · [G14](sources.md#g14) · [G15](sources.md#g15) · [G16](sources.md#g16) · [G19](sources.md#g19) · [G22](sources.md#g22) · [G24](sources.md#g24) · [G32](sources.md#g32)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
