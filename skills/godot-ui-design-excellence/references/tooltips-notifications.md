# Tooltips and notifications: information with a controlled lifetime

## Tooltip roles

Separate a brief label, an explanatory tooltip, a rich inspector, and a nested
reference. A long interactive pane should behave like a deliberate inspector,
not a fragile hover bubble. Important costs or required instructions must have
an accessible path that does not depend exclusively on hovering.

Use a configurable dwell for optional explanation and immediate presentation for
information needed to choose safely. A proposed initial hover dwell of 250–400 ms
is only a tuning hypothesis, not a measured industry standard. Inspect the actual
interaction: frequent expertise use and unfamiliar choices may need different rules.

## Placement and persistence

Anchor near the relevant object without covering its actionable area or essential
comparison. Clamp to the available UI region and flip placement intentionally.
For nested content, provide a reliable corridor or an explicit pin/inspect action;
do not require a perfect diagonal mouse movement. Controller focus should expose
the same information through an inspect action or persistent pane.

When source data changes, update or mark it stale without moving the tooltip
unnecessarily. Close it when its source disappears, or convert it into a clearly
identified pinned inspection. Recycled list cells must not leak a previous item's
content into the new tooltip.

## Notification grammar

Define urgency by consequence: routine collection, completed objective, actionable
warning, and immediate danger. Give each class an interruption policy, aggregation
rule, persistence, and recovery path. Do not interrupt every collection with an
identical full-size banner.

Coalesce repetitive low-priority changes without hiding exact details from the
history or relevant inventory. Critical state may need a persistent indicator,
not just a one-time toast. Let reading duration track content and accessibility
settings; allow dismissal or a history when important information would otherwise
vanish.

## Presentation

Reserve the strongest motion and audio for truly important events. Keep the world
visible where action continues. Match placement to the game's attention budget;
a banner should not cover incoming attacks or the selected build target.

Use native text with stable wrapping. A decorative title can establish identity,
but the consequence and next action should remain straightforward. Do not color
all positive events green if that conflicts with the established faction system.

## Failure cases to test

Trigger several notifications together, pause during one, resize with a nested
tooltip open, switch devices while reading, remove the underlying item, and enable
large text. Confirm that the player can still act, read, and recover information.
An empty notification queue is not evidence that its priority behavior works.

## Evidence anchors

[D09](sources.md#d09) · [G21](sources.md#g21) · [G28](sources.md#g28) · [X103](sources.md#x103) · [X112](sources.md#x112) · [X117](sources.md#x117)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
