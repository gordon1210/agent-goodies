# Resources and data models

Use this for custom `Resource` classes, configuration, data-driven gameplay and shared assets.

## What belongs in a Resource

Use a custom `Resource` for authored or serializable data with identity or reuse, such as item definitions, abilities, dialogue entries, enemy tuning, loot tables and theme data. Keep per-instance mutable runtime state separate unless shared mutation is explicitly intended.

Because loaded resources are cached and references can be shared, mutating a resource may affect every consumer. Duplicate intentionally when each instance needs independent state, and understand deep versus shallow duplication for nested resources.

## Design rules

- Give custom resources a clear `class_name` when editor discoverability benefits.
- Export strongly typed fields and arrays.
- Store data, validation and small data-centric helpers; avoid scene-tree assumptions.
- Prefer stable identifiers over display names or array positions for persistence and networking.
- Validate authored data at editor time, import time, startup or test time rather than failing deep in gameplay.
- Keep schema changes backward-compatible or migrate persisted resources deliberately.

## Configuration versus state

```text
Definition Resource: shared authored facts
Runtime State: mutable per session/entity
Presentation: nodes observing the state
```

Do not put current health, cooldown progress or temporary selection into a shared item/character definition resource.

## Loading

- `preload()` is appropriate for fixed dependencies known at parse time.
- `load()` or `ResourceLoader` is appropriate for dynamic paths and optional content.
- Do not load from disk in hot frame callbacks.
- Use interactive or threaded loading for large content when loading time is visible.
- Check type after dynamic loads and handle missing or invalid resources explicitly.

## Serialization hygiene

When editing `.tres` by hand, also load `serialization-and-text-scenes.md`. Preserve script references, UIDs, subresource IDs and typed values. For broad changes, use Godot to resave only the intended resources with a reviewed migration script.

## Data compatibility

Version external save/network representations independently from editor resources. Resource serialization is convenient for trusted project content, but it is not automatically a safe interchange format for untrusted files.
