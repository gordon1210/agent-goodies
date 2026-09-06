# Typography: build a hierarchy that survives actual play

## Define roles before selecting fonts

Use a small intentional role set: display/title, actionable item, body/explanation,
compact metadata, numeric instrument, and input prompt. Roles may share a font;
different roles do not require six families. Choose a display face for identity
and an appropriately readable companion for dense decisions when necessary.

Describe width, weight, case, spacing, and line height per role. A narrow display
face can create authority without becoming the default for long tooltips. Reserve
all caps for brief labels where the project direction supports them. Do not
simulate elegance with universally thin text or excessive letter spacing.

## Size by output, not a nominal token alone

A Godot `font_size` is not automatically the visible glyph height. Font metrics,
scale, viewport policy, and display resolution all matter. Measure representative
rendered text at the target device and viewing distance. Xbox guidance uses actual
rendered glyph dimensions and recommends different default minima for PC and
console; consult the accessibility module for the values and scope.

Proposed starting tokens in this package are design experiments, not compliance
certificates. Establish readable body text first, then derive headline and metadata
roles. Do not shrink all text to fit an overloaded layout; simplify or reflow.

## Numerical typography

Where columns update frequently, prefer tabular numerals if the selected font
actually supplies them. Align signs, decimal places, and units consistently.
Keep a stable allocated field width for predictable counters; excessive digit
rolling is not a substitute for precise status. Show stock and rate as distinct
roles. Choose abbreviations according to the game, and expose exact values when
rounding could change a decision.

## Texture and type must cooperate

Keep the text area materially quieter than its frame. Use an adequately opaque
backing where the world can become bright or detailed. A shadow can improve
separation, but repeated heavy outline + glow + shadow can damage letterforms.
Evaluate the actual composited background, not just a palette swatch.

At final scale, inspect narrow strokes, punctuation, accented characters, descenders,
and button-glyph labels. Check fallback characters beside the primary font rather
than approving each font in isolation.

## Localized typography is part of identity

Test long labels, plurals, CJK, combining marks, and RTL where relevant. Provide
suitable fonts and role equivalents, not a blanket Latin-font rule. Do not bake
functional labels into textures. Keep translated strings whole; avoid constructing
sentences by concatenating labels and values with assumed word order.

Acceptance: a player can read the relevant decision without zooming a screenshot;
headlines add identity without dominating every state; numbers remain stable under
updates; larger text uses designed reflow rather than clipping or microscopic fallback.

## Evidence anchors

[G09](sources.md#g09) · [G25](sources.md#g25) · [X101](sources.md#x101) · [X102](sources.md#x102)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
