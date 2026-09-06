# Accessibility: explicit design acceptance, not a badge

## Readability and scale

Xbox Accessibility Guideline 101 measures actual rendered glyph height, not merely
a nominal font setting. Its PC default recommendation is 18 px at 1080p and 36 px
at 4K; console recommendations are 26 px and 52 px respectively. It also recommends
text enlargement up to 200% without loss of content or functionality. These are
reference recommendations, not proof that a given font is readable or a game is
certified. Viewing distance, glyph metrics, and contrast still require evaluation.

Apply scale changes to the layout, not only the font resource. Preserve full access
to content without requiring simultaneous horizontal and vertical text scrolling.
Offer a simpler readable text style when an ornate direction needs an alternative.

## Contrast and non-color cues

XAG 102 recommends 4.5:1 for standard important text/visual elements and 3:1 for
large ones. At 1080p its large-text thresholds are 36 px on PC and 52 px on
console; the thresholds double at 4K. Inactive text has a 3:1 recommendation;
the high-contrast mode recommendation is 7:1. Evaluate the actual composite, including
alpha and variable gameplay backgrounds. High-contrast backing is more dependable
than assuming blur solves every scene.

Pair color with shape, icon, text, or position for important distinctions. A
selected frame, a lock mark with reason, and a labeled warning carry meaning even
when a hue distinction disappears. Check focus against all relevant surfaces.

## Reachability and input

Keep essential tasks reachable through supported alternative inputs, not just
through pointer drag or hover. Use predictable focus, visible state, modal scope,
and scroll-to-focus. A complex map may need a structured list or direct inspection
path. Do not claim controller support from the presence of button glyphs.

Accommodate relevant remapping and alternatives to repeated or sustained actions.
Place accessibility options where users can reach them before affected content.
Test input switching and hotplug without erasing logical selection.

## Motion, audio, captions, and semantics

Provide reduced motion and effects options that preserve informational state.
Avoid forced decorative camera movement or looping distraction near text. Do not
self-certify photosensitivity safety from a simple "less than N flashes" rule;
aggregate contrast, area, color, and composite effects require appropriate review.

Provide visual meaning for essential audio, readable captions with speaker context,
and meaningful interface semantics for supported narration. Test actual output;
custom visuals do not automatically inherit useful accessible labels.

## Scope of a review

Record tested platform, hardware, settings, input, language, and assistive tools.
Distinguish an implemented option, a functional test, and validation with affected
players. These guidelines help define acceptance; they are not platform certification,
a legal compliance opinion, or a substitute for user testing.

Block delivery on inaccessible essential actions, unreadable required information,
focus traps, or lost content at the agreed text scale. Do not average these failures
away with high visual-polish scores.

## Evidence anchors

[X101](sources.md#x101) · [X102](sources.md#x102) · [X103](sources.md#x103) · [X104](sources.md#x104) · [X106](sources.md#x106) · [X112](sources.md#x112) · [X113](sources.md#x113) · [X117](sources.md#x117) · [X118](sources.md#x118)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
