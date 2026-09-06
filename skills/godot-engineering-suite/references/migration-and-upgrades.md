# Migration and upgrades

Use for Godot minor/major upgrades, deprecated APIs, addon updates and project conversion.

## Keep migration isolated

Perform an engine upgrade on a dedicated branch/worktree with a clean baseline. Do not mix it with gameplay features or broad refactoring.

## Before opening in the new editor

1. Record the exact current engine and export templates.
2. Commit or back up all source assets and project files.
3. Read official release, migration and known-issue notes for every crossed minor.
4. Verify addons, GDExtensions, C#/.NET and custom modules support the target.
5. Capture representative screenshots, performance numbers, exports and tests.
6. Ensure CI can obtain the target binary/templates.

Opening/resaving may change project settings, imports, text scenes and resources. Expect and review this churn.

## Migration order

- engine/project settings and script parsing;
- addons/native bindings;
- imports and source assets;
- scenes/resources and deprecated nodes;
- rendering/shaders/lighting;
- physics/navigation behavior;
- UI/theme changes;
- C# builds and serialization;
- exports and platform SDKs;
- save/network/replay compatibility;
- performance regression checks.

## Deprecations

Replace deprecated APIs because the target requires it or as a separately reviewed cleanup. Do not mechanically substitute names without checking changed semantics.

## Content compatibility

Decide whether old saves, replays, mods and multiplayer clients remain supported. Bump schemas/protocols and add migrations or explicit rejection.

## Rollback

Keep the previous production branch and toolchain usable until target exports pass. Generated import caches are not a rollback strategy; source control is.

## Completion criteria

The project parses, tests pass, representative scenes match intended visuals/physics, target exports launch, native/addon dependencies are verified and migration-specific diffs are understood.
