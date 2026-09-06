# Animation

Use for AnimationPlayer, AnimationTree, state machines, imported clips, skeletons, tweens and procedural animation.

## Select the mechanism

- `AnimationPlayer`: authored tracks, deterministic property sequences, cutscenes and reusable clips.
- `AnimationTree`: blending, locomotion graphs and animation state machines driven by parameters.
- Tween: short runtime transitions, UI motion and simple property interpolation.
- Code/procedural animation: behavior driven by simulation or IK where authored tracks are insufficient.

Do not implement a full character animation graph with unrelated ad-hoc tweens.

## Track contracts

Animation tracks reference node/property paths. Renaming or moving nodes can silently break them. Search animations before scene refactors and inspect track diffs after editor resaves.

Avoid using animation tracks to mutate authoritative gameplay state unless the timing is intentionally animation-driven and tested. Prefer method/call tracks or emitted events at explicit synchronization points rather than relying on a visual property as state.

## AnimationTree

Treat the tree as presentation logic. Gameplay state drives parameters; animation should not become a second gameplay state machine. Centralize parameter names or access patterns to avoid string drift.

## Root motion and movement

Define whether animation or gameplay owns displacement. Do not apply both. Verify scale, import settings, skeleton orientation and physics interaction.

## Tweens

Keep ownership clear. Kill or replace obsolete tweens when state changes. A tween bound to a node may stop while paused depending on process configuration. Avoid starting new tweens every frame.

## Imported clips

Keep source files and import settings stable. Use animation libraries and retargeting according to the project version. Reimport tests must include loop boundaries, root motion, bone attachments and call tracks.

## Verification

Exercise transition interruption, reverse direction, pause, time scaling, scene teardown and low FPS. Visual inspection is required for blending, foot sliding, clipping and timing.
