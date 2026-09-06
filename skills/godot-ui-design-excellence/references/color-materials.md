# Color and materials: reserve contrast for meaning

## Define semantic roles

Separate text hierarchy, grouping surfaces, interaction accent, focus, selection,
positive/negative change, urgency, and faction identity. Avoid making the same
saturated color mean a selectable action, a selected tab, a rare item, and danger
without a second distinguishing cue.

Choose a restrained neutral foundation, a focal family, and semantic exceptions.
Those are relationships, not a mandatory palette. A bright snowy management UI,
a warm paper RPG menu, and a dark tactical interface can all be contemporary.
Gold, dark gray, glass, and neon are not quality requirements.

## Material grammar

Assign a material job before authoring its texture:

- A printed or painted backing can tie the interface to a fictional artifact.
- A fine hard edge can separate an instrument from the world.
- A translucent surface can preserve context but cannot guarantee contrast.
- A reactive light or reveal can identify an interaction boundary.

Keep material cues internally consistent: edge hardness, roughness impression,
texture frequency, and highlight placement should belong together. Do not apply
unrelated drop shadows and bevels to every component. Small text interiors should
usually be calmer than decorative borders.

## Design values before hue

Check whether the active target is legible in grayscale. If state differences
vanish, add shape, fill, stroke, icon, or wording before increasing saturation.
Use strong value contrast selectively to guide attention. High-density screens
need a quiet background hierarchy so warnings are not competing with ordinary
separators.

For contrast checks, evaluate the final foreground/background pair after alpha
compositing. Check several actual gameplay backgrounds: bright, dark, highly
detailed, and effect-heavy. A sampled opaque pair is a diagnostic, not proof that
an animated transparent panel passes everywhere.

## Avoid common material failures

Large blur areas can flatten the entire scene and consume rendering budget.
Fine repeated grain can shimmer while scaling. Compressed translucent edges can
produce halos. Nine-slice stretching can destroy a unique brush stroke. Diagnose
these in the engine at the smallest and largest supported sizes, not only in a
large source image.

Prefer independent layers: readable fill, border/ornament, state indicator, text.
That separation permits high-contrast and reduced-effect variants without changing
interaction layout. Keep color data masks distinct from artwork where import
settings differ. Do not store semantic state only in a shader uniform.

Acceptance: a dimmed or color-impaired view still reveals interaction and urgency;
texture supports hierarchy; readable content does not depend on one convenient
background; and the low-effects alternative still belongs to the same visual family.

## Evidence anchors

[D05](sources.md#d05) · [G08](sources.md#g08) · [G22](sources.md#g22) · [X102](sources.md#x102) · [X103](sources.md#x103)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
