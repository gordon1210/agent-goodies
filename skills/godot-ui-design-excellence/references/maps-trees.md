# Maps and trees: keep topology, state, and navigation distinct

## A graph is not just a grid with lines

Define what nodes and edges mean: prerequisite, unlocked path, influence, travel,
or visual grouping. Distinguish available, planned, selected, purchased, blocked,
and currently focused. A dependency line should not be confused with a selected
route or a region boundary.

Place labels and detail according to zoom level. Far views show structure; medium
views show recognizable nodes; close views expose labels and decisions. Preserve
access to important information even when a visual layer becomes hidden. Do not
make discovery depend on finding a tiny unlabelled icon at one zoom.

## Navigation model

For pointer input, define pan, zoom center, selection, and drag thresholds explicitly.
For keyboard/controller, choose logical graph navigation, focusable regions, or a
structured list alternative. Geometric nearest-neighbor movement can be wrong when
one edge represents the real prerequisite relationship. Document how tabbing and
directional input differ where both exist.

Keep the focused node visible after zoom, filtering, and data refresh. Preserve
selected identity when recentering. Offer a reset/recenter action without destroying
the user's inspection. Prevent accidental activation when a drag ends over a node.

## Decision detail

Use an inspector to show prerequisites, cost, effect, dependencies, and what will
change after purchase. During route or construction planning, distinguish provisional
geometry from committed state. Validate against the game again at commitment.
If a planned route becomes invalid, identify the invalid segment and preserve
recoverable work rather than silently discarding everything.

## Visual composition

Let the graph or map carry spatial context; keep its inspector materially quieter.
Use line weight and value to express edge classes before adding more colors.
Ensure edges terminate clearly instead of appearing to pass through unrelated
nodes. Check overlapping labels and crossing lines on the densest actual content.

On an ultrawide screen, more map context may be useful while text remains in a
bounded panel. On a narrow screen, an inspector may become a separate stage with
clear back navigation. Do not shrink a full desktop tree until labels are illegible.

## Godot implementation concerns

Separate the logical graph from rendered nodes. Only instantiate or update the
visible subset when scale demands it, but keep logical focus and accessibility
information independent of recycled visuals. Cache static drawing and request
redraw only when its inputs change. For world projection, define coordinate
conversion and clipping explicitly; decorative lines do not create input semantics.

Acceptance: follow a prerequisite chain, locate an unavailable node's reason,
change zoom without losing selection, and perform the key operation without a mouse.

## Evidence anchors

[G19](sources.md#g19) · [G21](sources.md#g21) · [X112](sources.md#x112) · [X113](sources.md#x113)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
