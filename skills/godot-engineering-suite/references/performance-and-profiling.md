# Performance and profiling

Use before proposing any optimization.

## Define the budget

State target platform, scene, resolution, renderer, frame-rate target and hardware class. Convert frame rate to frame-time budget. Separate CPU main thread, physics, rendering/GPU, memory, loading and network goals.

## Measure before changing

Use Godot profiler/monitors, render profiler, debugger, frame captures, platform tools and controlled benchmarks. Capture median and bad-frame behavior after warm-up. Compare the same build and workload.

Do not infer a bottleneck from node count, allocation folklore or a single FPS number.

## Optimization order

1. Remove unnecessary work.
2. Reduce frequency or scope.
3. Select a more suitable algorithm/data representation.
4. Batch or cache with explicit invalidation.
5. Move pure work off the main thread.
6. Reduce quality/content cost with measured tradeoffs.
7. Pool or use low-level servers only when lifecycle/allocation overhead is proven.

## CPU checks

Look for broad tree searches, per-frame resource loading, repeated pathfinding, signal storms, unbounded coroutines/timers, expensive string/log work, high script callback counts and avoidable physics queries.

## GPU checks

Look for overdraw, transparent layers, shader cost, shadowed lights, GI/post effects, particles, render-target count, resolution, material/state changes and excessive visible geometry. Profile on target GPUs.

## Memory/loading

Track peak and steady-state memory across repeated transitions. Identify retained references, caches, large textures/audio and duplicate resources. Optimize source/import settings before writing elaborate runtime unload systems.

## Correctness guard

An optimization must preserve simulation, visual, input and network contracts. Do not disable processing with no reactivation path, share mutable resources accidentally or introduce stale caches.

## Report

Include before/after measurements, command/build, hardware, scene, variance and tradeoffs. If no profiler was run, label suggestions as hypotheses.
