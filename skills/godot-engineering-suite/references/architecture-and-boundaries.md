# Architecture and boundaries

Use this for project structure, ownership, dependency direction, autoloads, services and large features.

## Default architecture

Prefer scene composition and explicit dependencies:

- A scene owns the lifecycle of nodes that form one reusable gameplay or presentation unit.
- Child nodes expose narrow methods, properties and signals.
- Parents coordinate children they own.
- Reusable configuration and authored data live in custom `Resource` types.
- Cross-scene services exist only for genuinely application-wide lifetimes.
- External systems are wrapped at one boundary rather than called throughout gameplay code.

## Dependency direction

Use a stable inward direction:

```text
platform / SDK / network adapters
             -> application services
             -> gameplay domain/state
             -> scene presentation and input adapters
```

Godot nodes often combine presentation and lifecycle, but domain state should not require a specific scene tree when it can remain plain data or a `RefCounted`/`Resource` object.

## Autoload policy

Use an autoload only when all are true:

- one instance is required for the process or active game session;
- its lifetime genuinely spans scene changes;
- its public API is small and stable;
- ownership cannot be expressed more clearly by a root scene;
- tests can reset or substitute its state.

Good candidates include a deliberately scoped save service, platform adapter or scene transition coordinator. Poor candidates include every manager, level-specific state, UI panels, temporary caches and convenience accessors.

## Avoid architecture-by-label

Do not add ECS, service locators, dependency injection containers, global event buses, repositories, command buses or generic state machines merely because they are common elsewhere. Introduce an abstraction after a concrete seam exists and at least two callers benefit.

## Feature slicing

For a feature, identify:

1. authoritative state;
2. commands that may change it;
3. emitted events;
4. persistence/replication boundary;
5. presentation adapters;
6. teardown and scene-change behavior;
7. test seam.

Keep one owner for mutable state. UI and effects observe state; they should not become alternate authorities.

## Folder structure

Follow the existing repository. For a new project, prefer feature-oriented grouping once the project is non-trivial:

```text
features/player/
features/combat/
features/inventory/
shared/ui/
shared/resources/
platform/
tests/
```

A global `scripts/`, `scenes/`, `resources/` split is acceptable for a small project but becomes costly when one feature spans many distant folders.
