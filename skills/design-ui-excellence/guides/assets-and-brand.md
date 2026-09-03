# Assets, Imagery & Brand Fidelity

Use this guide when recognition, product visuals, photography, illustration, iconography, or generated assets materially shape the work.

## Recognition hierarchy

For most branded work, recognition depends on:

1. real logo and approved lockups
2. real product imagery, interface captures, or packaging
3. distinctive photography or illustration system
4. typography and composition
5. color

A palette without the actual assets often produces a category-themed page, not the brand.

## Asset inventory

Before designing, inspect:

- logos and favicon
- product screenshots and recordings
- product photography
- campaign or editorial imagery
- illustrations
- icons
- fonts
- diagrams and charts
- social/share images
- light/dark variants
- licenses, attribution, and permissions

Record missing assets rather than silently inventing replacements.

## Sourcing order

Prefer:

1. repository and user-provided approved assets
2. official brand or product sources
3. licensed asset libraries
4. commissioned or generated assets with a clear brief
5. an honest, labeled placeholder

Do not redraw a recognizable logo or product in CSS because the actual asset is missing. Do not substitute a generic fake application screenshot for product evidence.

## Art-direction system

Define:

- anchor asset
- subject and point of view
- composition
- crop and negative space
- lighting
- palette relationship
- material or texture
- level of realism
- human presence
- typography relationship
- motion behavior
- prohibited drift

Every asset in a set should look as though it belongs to the same world. Reuse the visual bible; do not re-invent prompts from memory.

## Generated imagery

A useful generation brief states:

- use case and output format
- exact subject and action
- environment
- composition and camera
- lighting and material
- palette relationship
- emotional tone
- required negative space
- exact exclusions
- reference roles
- originality boundaries

Do not depend on generated raster text for critical web copy, product labels, legal copy, or exact wordmarks. Render text in HTML or use approved vector assets whenever possible.

Validate outputs for:

- subject accuracy
- brand meaning
- composition and crop
- unwanted text or marks
- continuity across a set
- originality
- usable resolution
- responsive crops
- accessibility and content sensitivity

Version iterations non-destructively.

## Product screenshots

- Use current, approved product states.
- Scrub personal and sensitive data.
- Keep data believable without implying false customers or results.
- Avoid tiny unreadable screenshots presented as proof.
- Crop around the story while retaining necessary context.
- Use annotation sparingly and consistently.
- Do not fake browser or device chrome when real context is available.

## Icons

- Prefer one coherent icon family per surface.
- Match stroke/fill and optical weight to surrounding type.
- Use `currentColor` where appropriate.
- Fill can communicate selected state when the system defines it.
- Do not use emoji as replacement UI icons unless the product language intentionally calls for them.
- Icon-only controls require accessible names.

## Responsive media

Specify:

- intrinsic dimensions
- aspect ratio
- crop focal point
- `srcset` or equivalent responsive source behavior
- loading priority
- format and compression
- dark-mode variant when necessary
- fallback
- alt-text purpose

Protect layout stability. Do not load desktop-scale assets into small mobile slots without reason.
