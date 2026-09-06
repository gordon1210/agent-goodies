# Godot text, fonts, and localization

## Preserve native text

Use Label, RichTextLabel, and appropriate native controls for functional words,
numbers, input prompts, and accessible names. Rich text is useful for structured
emphasis; it is not permission to encode the entire interface as one unmanageable
BBCode string. Keep data, translation keys, and presentation separated.

Use complete translatable messages with named values or the project's established
formatting system. Do not build translated sentences by English-order concatenation.
Choose actual font coverage and fallback resources for supported languages. Font
files are project assets with provenance; this skill does not provide them.

## Sharpness and metrics

Inspect final output at the intended resolution and scale. Imported font settings,
hinting, oversampling, MSDF, and renderer behavior have trade-offs; choose with the
actual font and target. MSDF is not a universal cure for every small glyph, weight,
or script. Avoid arbitrary nonuniform scaling of text to force a fit.

FontVariation can expose supported OpenType features. Tabular numerals are useful
for changing counters only when the face supports them. Do not assume the feature
exists or infer accessibility from the nominal `font_size` setting.

## Layout policy per role

Specify wrapping, maximum useful line length, overflow, and user access to full
content. Truncation may be acceptable in a compact list if full content is available
on inspection; it is unacceptable when the hidden text changes the decision.
Never silently shrink critical text below the approved readable role size.

Distinguish `minimum_size`, allocated region, and actual shaped content. Larger
fonts can change both line count and focus geometry. Reflow the component and
refresh navigation rather than only applying a font-size override.

## Localization test set

Use Godot's supported pseudolocalization tools to reveal expansion and hardcoded
strings, then test actual target languages. Include accents, CJK, combining marks,
long compounds, plural forms, mixed numerals, and RTL where relevant. A fixed
"German is 30% longer" rule cannot establish coverage.

Mirror layout intentionally for RTL where the UI requires it, while preserving
meaningful nonmirrored content such as certain diagrams or artwork. Review icons,
text alignment, reading order, and navigation together. Text-reveal effects should
respect the engine's shaping/grapheme behavior rather than slicing bytes.

## Accessibility semantics

Provide meaningful names, roles, values, states, and reading order where platform
and engine support allow it. Custom-drawn symbols may need additional semantics.
Verify narration/assistive behavior on the actual target; a native-looking control
or a valid script does not prove screen-reader compatibility.

Acceptance: actual supported strings remain legible and reachable at large text,
numbers do not jitter unnecessarily, fallback fonts fit the direction, and any
truncation leaves a clear path to the full information.

## Evidence anchors

[G09](sources.md#g09) · [G10](sources.md#g10) · [G25](sources.md#g25) · [G26](sources.md#g26) · [G33](sources.md#g33) · [X101](sources.md#x101) · [X106](sources.md#x106)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
