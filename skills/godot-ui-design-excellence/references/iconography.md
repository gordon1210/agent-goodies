# Iconography: make a small coherent language

## Start with player meaning

Name the player-visible purpose before drawing the symbol. The icon for "collect
income" should communicate that goal, not merely an internal relationship variable
that the action modifies. A Frostpunk 2 designer's case study documents precisely
this kind of mismatch between player intent and underlying system terminology.
Use that lesson to review the whole label/icon/action relationship.

Give state shape a consistent vocabulary. If a marker opens a particular class of
panel, keep its identifying geometry recognizable across marker, panel, and focus
state. Consistency should assist recognition, not become arbitrary decoration.

## Author a family specification

Record nominal icon box, optical occupied area, padding, stroke families, corner
behavior, filled/outlined policy, and treatment of negative space. Keep difficult
shapes optically balanced rather than forcing every contour to exactly the same
bounding box. Test beside actual type and prompt glyphs.

Create small/standard/large variants only when the smallest size genuinely needs
simplification. Scaling a complex emblem down is not icon design. At final size,
check counterspaces, narrow gaps, silhouette, and distinction from adjacent icons.
An atlas preview helps find stylistic outliers.

## Distinguish categories and actions

A category emblem, a state indicator, a currency unit, a warning, and a platform
button glyph do different jobs. They can coexist without sharing identical artwork,
but should obey a common alignment and contrast system. Do not fabricate console
button legends that contradict the active controller. Derive prompts from action
bindings and actual device mapping, with authorized glyph assets.

Accompany unfamiliar icons with labels in decision-critical contexts. If a tooltip
is needed to discover what every button does, simplify the language or expose
labels rather than merely reducing tooltip delay.

## State design

Do not reduce opacity indiscriminately for disabled items if essential labels become
unreadable. Add a clear unavailable treatment and reason. Selection and focus may
coexist; reserve distinct frame or marker space for each. Animated glints should
not be the sole indicator that a control is available.

## Production

Keep source vector files when available. Verify import behavior instead of assuming
SVG means unlimited runtime resolution. For textured symbols, author intentional
alpha and safe padding. Separate gameplay symbols from decorative insignia; avoid
mixing random open-source families without normalization and license records.

Acceptance: nearby icons remain distinguishable without color, communicate the
player's goal, and share optical weight. Correct the concept before refining the
stroke quality of an ambiguous symbol.

## Evidence anchors

[D02](sources.md#d02) · [G22](sources.md#g22) · [G29](sources.md#g29) · [X103](sources.md#x103)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
