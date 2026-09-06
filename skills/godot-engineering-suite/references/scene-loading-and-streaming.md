# Scene loading and streaming

Use for scene transitions, loading screens, large resources, world chunks and background loading.

## Define ownership and transition states

A transition coordinator should make these states explicit:

```text
idle -> requesting -> loading -> activating -> active
                    -> failed/cancelled
```

Prevent overlapping transitions unless the design supports them. Keep the previous scene alive until the next state is ready or a deliberate blank/loading state owns the viewport.

## Loading choice

- `preload`: small fixed dependencies needed whenever the script is parsed.
- synchronous `load`: dynamic content whose stall is acceptable.
- threaded/interactive ResourceLoader workflow: visible or large loading where progress/cancellation matters.
- custom chunk streaming: worlds too large for one scene/resource boundary.

Do not perform scene-tree mutation from worker threads. Poll or receive load completion on the main thread and validate that the request is still current.

## Loading screen behavior

A loading screen must render at least one frame before blocking work starts. Keep it in a process mode/layer that remains responsive during transition. Progress values are estimates unless every stage has measurable work; do not fake precise percentages.

## World streaming

Separate persistent state from loaded presentation nodes. Define chunk identity, load radius, hysteresis, dependencies, save deltas, navigation/physics activation and memory budget. Avoid unloading a chunk still referenced by AI, quests, projectiles or asynchronous work.

## Resource lifetime

Loaded resources may be cached while references remain. Release scene instances and references intentionally, then measure memory rather than assuming a scene change frees everything immediately.

## Failure and cancellation

Handle missing/incompatible resources, cancellation, stale requests and activation exceptions without leaving duplicate roots or an unusable UI. Log the requested resource and transition ID.

## Verification

Test slow storage, repeated transitions, cancel/back, missing content, save/load during transitions, memory after cycles and exported builds. Measure worst-case frame stalls and peak memory.
