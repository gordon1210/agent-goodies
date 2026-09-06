# Engine modules and custom builds

Use for compiling Godot, engine modules, custom patches and export templates.

## Decide whether engine modification is justified

Prefer GDScript/C#, GDExtension or an addon when they provide the required API and performance. An engine module or fork is justified for deep engine integration, unsupported platform work, compile-time features or proven performance constraints.

## Pin source and toolchain

Record Godot commit/branch, SCons options, compiler, SDKs, submodules/patches and build host. Keep custom patches small and rebased independently from game features.

## Module lifecycle

Follow engine registration/initialization levels and unregister symmetrically. Define ownership, thread affinity and serialization/API exposure. Engine crashes can originate from module teardown long after gameplay code exits.

## API design

Expose a narrow stable Godot-facing API with validated arguments. Keep internal implementation details out of ClassDB unnecessarily. Document editor-only versus runtime availability and platform feature tags.

## Custom templates

Editor and export templates must come from the same compatible source/configuration. Build debug and release templates required by the project, and package platform libraries/resources exactly as the export expects.

## Upstreamability

Where feasible, isolate changes so they can be proposed upstream or dropped when a future version provides the feature. Track upstream issue/PR and removal criteria.

## Verification

- build cleanly from documented commands;
- run engine/version smoke tests;
- load the project and affected classes;
- run native sanitizers/tests where available;
- create and launch target exports;
- verify stripping, symbols and licenses;
- compare performance with a stock engine when optimization motivated the fork.

Treat all source-build scripts and produced binaries as privileged executable code.
