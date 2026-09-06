# Physics

Use for bodies, areas, collision shapes, queries, layers, masks and fixed-step gameplay.

## Choose the correct body

- `CharacterBody2D/3D`: code-controlled characters using movement helpers.
- `RigidBody2D/3D`: simulation-controlled bodies; apply forces/impulses through supported APIs.
- `StaticBody2D/3D`: immovable world collision.
- `AnimatableBody2D/3D`: moved platforms/objects intended to affect other bodies predictably.
- `Area2D/3D`: overlap detection, fields and triggers without solid-body response.

Do not move a rigid body by overwriting transforms every frame unless using a documented integration mode.

## Time and mutation

Run motion and physics queries in the physics step when they affect simulation. Keep fixed-step rates independent of render FPS. Defer collision-shape or scene-tree mutations only where Godot prohibits changing them while physics queries are flushing; do not defer all physics code automatically.

## Layers and masks

Name layers in project settings and treat the matrix as part of the design. A layer states what an object is; a mask states what it queries/collides with. Restrict monitoring and raycasts to relevant layers.

## Character movement

- Set velocity intentionally before `move_and_slide()`.
- Distinguish grounded, airborne, wall and slope behavior.
- Define jump buffering, coyote time and moving-platform semantics explicitly if needed.
- Handle floor normals and up direction consistently.
- Avoid multiplying velocity by `delta` before APIs that already integrate velocity over the physics step.

## Queries

Use typed query parameter objects and exclude the caller when required. Query results are snapshots; validate returned objects before later use. Avoid broad raycasts or shape queries every frame for every entity without profiling.

## Determinism

Godot physics is not guaranteed deterministic across platforms, builds or runs. Do not base lockstep networking or authoritative replays on raw physics state without a deliberately deterministic layer.

## Verification

Test at the project's physics tick rate and low/high render rates. Include edges, slopes, moving platforms, high velocity, spawn overlap, pause/resume and scene reload. Use visible collision shapes and profiler monitors during diagnosis.
