# Asset production: turn direction into engine-ready UI art

## Decompose before generating

List native text and values, semantic controls, repeating frames, unique ornaments,
portraits, icons, masks, and optional material textures separately. A generated
full-screen image can explore direction, but it is not a functional interface.
Do not ship baked labels, simulated input prompts, or fake numbers as UI.

Use the [asset manifest](../assets/asset-manifest.example.json) to record purpose,
source/license, target dimensions, alpha policy, scalable region, state variants,
import intent, and approval. Dimensions in templates are examples; choose actual
ones from the project's design and rendering scale.

## A bounded art brief

Specify subject/role, silhouette, optical weight, edge treatment, material,
palette roles, level of detail at playing size, transparent/background requirements,
and exclusions. Define invariants for a family: stroke logic, lighting direction,
texture frequency, color meaning, and text-safe interior.

Approve one representative asset in context, then produce siblings using the same
brief and reference. Do not independently prompt each icon and hope the family
matches. When generation/editing tools are unavailable, provide the brief and
explicit placeholders; never pretend the requested asset has been created.

## Scalable ornament

For repeatable panels, define corners, repeat/stretch edges, and a flexible center.
Separate texture margins, content margins, and decorative expansion. Nine-slice is
appropriate for repeatable borders, not automatically for a unique painted gesture.
A long brush stroke may need independent endcaps and a tiled center, or separate
outer ornament that does not scale with text.

Inspect straight alpha and edge halos on light and dark backing. Verify transparent
pixels rather than trusting a checkerboard painted into the image. Keep important
features away from crop edges. Normalize dimensions, padding, pivot, and naming
with ordinary tools after creative work.

## Import deliberately

Godot normally rasterizes SVG during import; the reviewed 4.7 documentation also
describes DPITexture behavior for suitable SVG imports. Confirm actual version and
settings instead of assuming any SVG stays infinitely sharp. For raster UI,
inspect downscaling, mipmaps, compression, filtering, and atlas bleeding in context.
Choose each based on the asset, not one universal import preset.

Keep text and nondecorative symbols separate from noise/reveal masks. Do not use
lossy compressed detail where artifacts undermine thin strokes or alpha edges.
Store editable sources outside generated import caches according to repo policy.

## Approval

Check a contact sheet, the real screen at target sizes, all states, and low-effects
mode. Reject an individually attractive asset that violates the family's grammar.
Record unverified provenance as a shipping blocker rather than calling it "free"
from a search thumbnail. This package bundles no third-party game images or fonts.

## Evidence anchors

[G11](sources.md#g11) · [G22](sources.md#g22) · [D01](sources.md#d01)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
