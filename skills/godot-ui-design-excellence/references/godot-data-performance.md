# Godot UI data and performance: coherent snapshots, measured work

## Separate state, view data, and presentation

Expose a screen-oriented snapshot or view model instead of making each label reach
into unrelated game internals. Keep identifiers stable. Actions request changes;
the authoritative game state validates and commits them. Derive display values,
units, and comparison deltas consistently.

Use events or dirty-state updates for values that change discretely. Continuous
meters, timers, tracking markers, or animation may appropriately update each frame
or at a measured cadence. "Never poll" is not a universal performance rule. The
problem is unnecessary work or incoherent state, not the existence of `_process`.

## Coherence during updates

Apply related values as one understandable state transition where possible.
Resource stock, rate, and warning must not briefly describe three different
simulation moments. For frequent numbers, keep displayed actual values distinct
from any interpolated visual indicator. Do not hide a real deficit until an
animated counter finishes catching up.

When selection changes, cancel or invalidate obsolete work. Attach stable identity
and a generation/request token to asynchronous previews so a late result cannot
replace the current item's thumbnail or description. Apply scene changes through
the engine's supported thread-safe/main-thread mechanisms.

## Scale the representation

Large grids and long event logs may need virtualization, paging, or incremental
construction. Preserve logical focus and selection independent of recycled visuals.
Make scrolling an item into view part of navigation. Avoid a full subtree rebuild
for one changed value if a targeted update is adequate.

Do not prescribe object pooling everywhere. First profile instantiation, layout,
text shaping, texture upload, shader cost, and overdraw. A small static options
menu has a different bottleneck from thousands of changing map labels.

## Honest loading states

Show loading only while something is actually loading. Do not insert artificial
spinners to make local operations feel substantial. For real loading, define
placeholder dimensions to prevent layout shifts, cancellation, retry, error state,
and whether the user may continue another task. Background resource loading does
not prove the final GPU upload or scene instantiation is hitch-free.

## Budget and measurement

Record target hardware, resolution, renderer, scene, UI scenario, baseline frame
time, and cost with the new feature. Separate CPU layout/script cost, GPU passes,
texture memory, and extra viewports. No fixed universal node count or blur budget
can substitute for that measurement.

Use representative worst cases: populated inventory, many alerts, expanded tree,
large text, and the game running behind a translucent panel. Document measurements
actually taken and distinguish them from proposed budgets.

Acceptance: data stays coherent under rapid changes, stale responses are rejected,
selection survives updates, and the measured work fits the project's explicit
performance target without sacrificing basic readability.

## Evidence anchors

[G21](sources.md#g21) · [G27](sources.md#g27) · [G28](sources.md#g28) · [G32](sources.md#g32)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
