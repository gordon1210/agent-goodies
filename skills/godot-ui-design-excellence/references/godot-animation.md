# Godot animation: preserve layout and survive interruptions

## Separate allocation from presentation

A useful scene pattern is `LayoutSlot (Control) → MotionRoot (Control) → Content`.
The surrounding Container manages LayoutSlot; MotionRoot carries presentation
transforms; Content retains native controls and text. Ensure the slot's minimum
size represents its content. Avoid transforming the actual pointer target so far
that it visibly moves away during activation.

Use an AnimationPlayer for authored multi-track choreography when appropriate,
and a Tween for a small state-driven transition. Neither is universally superior.
Keep the semantic state outside the animation: opening, open, closing, hidden,
and any transaction state must have explicit ownership.

## One owner for each animated property

Before starting a conflicting Tween, stop the previous owner. Begin from the current
visible value when reversing an interaction rather than resetting to a stale start.
Godot's Tween documentation recommends avoiding competing tweens on the same
property and explains lifecycle binding. Use node-bound creation where appropriate;
do not reuse a finished Tween as a permanent animation object.

Store resting values deliberately. If a component's designed scale is not one,
blindly resetting to `Vector2.ONE` is wrong. Recompute pivot and layout-dependent
origins on resize as needed. Do not let repeated hover calls multiply scale.

## Cancellation contract

Do not make business logic depend on awaiting a Tween that another action may kill.
Use a transition generation/token or equivalent state ownership so stale callbacks
cannot hide a newly reopened panel. Define completion and cancellation separately.
On teardown, clear owners and prevent callbacks from mutating freed or repurposed
nodes. A queue of old animations is not a reliable state machine.

For a reopen during closing, preserve the current opacity/offset and head toward
open. For a close during opening, revoke or retain interaction according to the
screen contract immediately; decorative completion can follow.

## Time and pause

Time scale and SceneTree pause behavior are different concerns. Confirm both the
Tween's time-scale policy and the bound node's pause/process behavior for the target
release. A paused game should not accidentally freeze its own pause menu. Do not
change global time scale to create a routine button animation.

## Reduced motion path

Apply semantic state directly, then establish its final visible representation.
Do not assume setting every duration to zero preserves callback order, focus, and
layout. Test that branch as a real implementation. Status interpolation may remain
when it communicates information, but essential values should be directly readable.

Acceptance sequence: open → close immediately → reopen → resize → pause → close
scene. Verify final visibility, focus, state, opacity, transform, and absence of
stale callbacks. Read the motion module for visual timing; this module owns runtime
correctness, not a mandatory aesthetic.

## Evidence anchors

[G07](sources.md#g07) · [G30](sources.md#g30) · [G31](sources.md#g31)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
