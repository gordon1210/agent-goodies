# GDScript

Use this for `.gd` implementation, review and refactoring.

## Version and style

Match the project's Godot minor version and existing GDScript style. Prefer the official naming convention unless the repository establishes another one: PascalCase classes, snake_case functions and variables, and CONSTANT_CASE constants.

## Types

Use static types where they improve contracts, editor tooling and refactor safety:

- exported properties;
- node and resource references;
- public methods and signals;
- collections crossing subsystem boundaries;
- values whose inferred type would be too broad.

Do not add noisy annotations where inference is exact and local. Avoid `Variant` as an escape hatch. Narrow dynamically loaded or dictionary data at the boundary.

## Node contracts

- Required children should use typed references and fail clearly if the scene contract is broken.
- Optional nodes should be explicitly nullable and handled deliberately.
- Use `@export` for author-controlled configuration, not for every internal variable.
- Use `@onready` only for values that genuinely depend on tree readiness.
- Avoid fragile absolute paths and repeated tree searches.

## Lifecycle and time

- Put physics movement and physics queries in `_physics_process()` unless the engine API specifies otherwise.
- Put visual/non-physics updates in `_process()`.
- Scale rates by `delta`; do not multiply one-shot impulses or already time-based engine values blindly.
- Disable processing only with a clear path to re-enable it.
- Understand pause/process modes for nodes expected to run while paused.

## Async and signals

`await` suspends the current function; the owner may be freed or state may change before resumption. Revalidate references and operation identity after awaiting. Avoid awaiting inside per-frame state branches where multiple concurrent continuations can accumulate.

Prefer typed signals and direct callables. Do not connect the same signal repeatedly. Do not turn every interaction into a global signal.

## Errors and invariants

Use assertions and explicit errors for programmer mistakes in development. Handle expected runtime failures without spamming logs. A null guard is not a substitute for repairing a required node path.

## Performance

Do not cargo-cult micro-optimizations. Built-in value types such as vectors are normal to create locally. Profile before pooling, caching broad tree state or replacing clear code with server APIs.

## Review checks

- exported names/types remain serialization-compatible;
- integer division, typed collections and nullable values behave as intended;
- signal callback signatures match;
- scene paths and resource paths exist with correct case;
- loops and callbacks cannot create unbounded nodes, timers, tweens or coroutines;
- freed objects are not retained or accessed;
- debug-only behavior is not shipped accidentally.
