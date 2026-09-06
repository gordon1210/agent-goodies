# Inventory and buildcraft: preserve identity and support comparison

## Define the decision model

Separate browsing, inspecting, comparing, equipping, upgrading, and discarding.
Keep the selected item distinct from equipped status. Use stable item identifiers;
position in a sorted list is not identity. After a change, restore useful context
or choose a documented neighbor when the object no longer exists.

Begin with realistic fixture data: long names, missing artwork, duplicate names,
unique modifiers, stack counts, locked items, and a partially full inventory.
Do not approve a layout from six identical placeholder swords.

## Comparison structure

Place current and candidate values in a consistent order with units, signed deltas,
and clear direction-of-benefit semantics. Lower weight may be beneficial while
lower damage is not. Distinguish additive stats, multipliers, caps, prerequisites,
and nonnumeric effects. Do not compress trade-offs into an unsupported universal
"better" score.

Provide enough persistent context to compare across a scroll. When simultaneous
columns cannot fit, use an explicit comparison mode rather than truncating half
the data. Explain which item or slot is being replaced. Forecast derived stats
using the actual build rules and label approximations.

## Browsing controls

Expose filters and sorting without displacing the primary selection. Communicate
active filters and provide a clear way to reset them. Keep sort behavior stable
when values update; continuous resorting during an inspection can be disorienting.
For virtualized grids, focus should follow the logical item and scroll it into view
before interaction, rather than jumping between recycled cell nodes.

## Transaction feedback

Preview an equip or upgrade, validate the actual game state at commit, then show
success only after acceptance. During asynchronous inventory changes, reject
stale previews and prevent accidental duplicate requests through transaction state,
not only disabled artwork. Give failure a useful explanation and preserve context.

Use confirmation for irreversible destructive actions proportional to the loss.
If undo is supported, expose its scope and lifetime clearly. Do not silently consume
rare resources on a double activation or on the input release that opened a dialog.

## Art direction without sacrificing utility

Let a portrait, item silhouette, or section ornament carry expression. Keep repeated
stat rows quiet and consistently aligned. Do not place a rich image behind tiny
modifier text. A rare item may have a distinct emblem or border, but rarity should
not overpower the currently focused decision.

Acceptance: compare and equip two visually similar items using each supported
input method, recover from an invalidated choice, keep context after sorting,
and understand a nonnumeric trade-off. Repeat with large text and missing thumbnails.

## Evidence anchors

[G23](sources.md#g23) · [G28](sources.md#g28) · [X112](sources.md#x112) · [X115](sources.md#x115)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
