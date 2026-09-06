---
name: godot-engineering-suite
description: Engineering guidance and task routing for Godot 4 projects. Use when implementing, reviewing, debugging, testing, profiling, refactoring, importing assets, building UI, 2D or 3D gameplay, networking, editor tools, exports, migrations, GDScript, C#, shaders, GDExtension, XR, or platform-specific Godot work. Detect the project's exact engine version and load only the relevant bundled references.
license: MIT
metadata:
  compatibility: Agent Skills compatible coding agents; targets Godot 4.x. A matching local Godot CLI is optional for validation.
  author: godot-skill-suite-contributors
  version: "1.0.0"
  context-strategy: "single-router-progressive-disclosure"
  target-engine: "godot-4.x"
---

# Godot Engineering Suite

Use this skill as a router, not as a monolithic handbook. Read only the references needed for the current task.

## Non-negotiable rules

1. Detect the project's Godot version, language, renderer, target platforms, addons, and existing conventions before proposing architecture or API changes.
2. Treat repository instructions and existing project patterns as authoritative unless they are demonstrably broken.
3. Do not require an MCP server. Prefer normal file tools and the matching Godot CLI. Use an existing MCP integration only when the repository already trusts it and the user asked for or approved it.
4. Do not grant yourself tools, install packages, access the network, launch a GUI, or run untrusted project code merely because this skill is active.
5. Never edit generated import state under `.godot/`, imported artifacts, binary `.scn` or `.res` files, or third-party addon code unless the task explicitly requires it.
6. Keep changes narrow. Preserve scene ownership, UIDs, resource references, node paths, signal contracts, input actions, and serialized property types.
7. Verify with the smallest useful check first. Use the exact engine branch expected by the project.
8. Do not hide broken invariants behind blanket null checks, deferred calls, object pools, autoloads, or speculative abstractions.

## Start every task

1. Locate `project.godot` and the repository root.
2. Read applicable `AGENTS.md`, `CLAUDE.md`, `GODOT_PROJECT.md`, README, and nearby implementation files.
3. Read [project discovery](references/project-discovery.md).
4. Read [change workflow](references/change-workflow.md) before editing scenes, resources, project settings, addons, exports, or native code.
5. If an API, node, property, CLI flag, or compatibility detail is uncertain, read [official docs and versioning](references/official-docs-and-versioning.md) and verify against documentation for the detected minor version.
6. Load the smallest relevant set of topic files below. Usually two to four references are enough.

The optional read-only command `python scripts/inspect_godot_project.py --root .` produces a compact project profile. Do not run it when execution is unavailable or disallowed; inspect the same facts manually instead.

## Routing map

### Project structure and core engine model

- Architectural boundaries, autoloads, composition, dependency direction: [architecture and boundaries](references/architecture-and-boundaries.md)
- Scene ownership, node lifecycle, node references, instancing: [scenes, nodes, and ownership](references/scenes-nodes-and-ownership.md)
- Custom resources, configuration, data-driven systems: [resources and data models](references/resources-and-data-models.md)
- Text scenes, UIDs, subresources, merge-safe edits: [serialization and text scenes](references/serialization-and-text-scenes.md)
- Signals, event buses, state machines, game state: [signals, events, and state](references/signals-events-and-state.md)
- Loading screens, background loading, world chunks: [scene loading and streaming](references/scene-loading-and-streaming.md)

### Languages and native integration

- `.gd`, typing, lifecycle methods, coroutines, style: [GDScript](references/gdscript.md)
- Godot .NET projects and C# integration: [C#](references/csharp.md)
- Native libraries and extension APIs: [GDExtension and native code](references/gdextension-and-native-code.md)
- Engine modules, source builds, custom export templates: [engine modules and custom builds](references/engine-modules-and-custom-builds.md)

### Gameplay systems

- Action maps, keyboard, mouse, touch, gamepads, rebinding: [input and device support](references/input-and-device-support.md)
- Sprites, TileMapLayer, 2D transforms and cameras: [2D](references/two-d.md)
- Meshes, transforms, environments and 3D scene composition: [3D](references/three-d.md)
- Cameras, viewports, scaling, split-screen, render targets: [camera, viewport, and resolution](references/camera-viewport-and-resolution.md)
- Bodies, areas, layers, masks, fixed-step simulation: [physics](references/physics.md)
- Pathfinding, avoidance, behavior and agents: [navigation and AI](references/navigation-and-ai.md)
- AnimationPlayer, AnimationTree, skeletons, state transitions: [animation](references/animation.md)
- Audio buses, playback, spatial sound, transitions: [audio](references/audio.md)
- Procedural worlds and reproducible generation: [procedural generation](references/procedural-generation.md)
- Replays, lockstep assumptions, deterministic state: [determinism, replays, and lockstep](references/determinism-replays-and-lockstep.md)

### UI and presentation

- Control layout, containers, anchors, themes, reusable components: [UI layout and themes](references/ui-layout-and-themes.md)
- Focus, gamepad navigation, text scaling, accessibility: [UI input and accessibility](references/ui-input-and-accessibility.md)
- Renderers, lighting, shadows, GI, post-processing: [rendering and lighting](references/rendering-and-lighting.md)
- CanvasItem and spatial shaders, compute, particles, VFX: [shaders and VFX](references/shaders-and-vfx.md)
- Localization resources, locale changes, formatting and RTL: [localization and internationalization](references/localization-and-internationalization.md)

### Content, persistence, online systems

- Source assets, import options, reimport safety, 3D pipelines: [asset import and content pipeline](references/asset-import-and-content-pipeline.md)
- Saves, settings, migrations, atomic writes and `user://`: [save/load and persistence](references/save-load-and-persistence.md)
- RPCs, authority, replication, dedicated servers and validation: [networking and multiplayer](references/networking-and-multiplayer.md)
- WorkerThreadPool, threads, synchronization and main-thread boundaries: [threading and background work](references/threading-and-background-work.md)

### Quality and maintenance

- Test seams, unit/integration/scene tests and headless checks: [testing](references/testing.md)
- Parser errors, runtime failures, crashes and diagnostic workflow: [debugging](references/debugging.md)
- Profiler-driven CPU, GPU, memory and loading optimization: [performance and profiling](references/performance-and-profiling.md)
- Review checklist for scripts, scenes, resources, exports and security: [code review](references/code-review.md)
- Godot minor upgrades, deprecated APIs and conversion: [migration and upgrades](references/migration-and-upgrades.md)
- Project profile and durable documentation: [documentation and project profile](references/documentation-and-project-profile.md)

### Tooling, delivery and platforms

- `@tool`, EditorPlugin, inspectors, import plugins and editor safety: [editor tools and tool scripts](references/editor-tools-and-tool-scripts.md)
- Third-party addons, vendoring, update policy and licenses: [addons and dependencies](references/addons-and-dependencies.md)
- Agent permissions, MCP scope, editor execution and automation: [agent and MCP safety](references/agent-and-mcp-safety.md)
- Filesystem, network, mods, native code and untrusted input: [security and untrusted content](references/security-and-untrusted-content.md)
- Export presets, templates, reproducible artifacts, signing: [export, release, and signing](references/export-release-and-signing.md)
- Windows, macOS and Linux behavior: [desktop platforms](references/platform-desktop.md)
- Android and iOS lifecycle, touch and packaging: [mobile platforms](references/platform-mobile.md)
- Browser constraints, isolation, storage and download size: [web platform](references/platform-web.md)
- Console constraints and licensed SDK boundaries: [console platforms](references/platform-console.md)
- OpenXR rigs, tracking, interaction and performance: [XR and OpenXR](references/xr-and-openxr.md)
- CI imports, headless checks, exports and artifact handling: [CI and headless automation](references/ci-and-headless-automation.md)

## Cross-cutting load rules

- Any `.tscn`, `.tres`, UID, or external-resource edit: also load [serialization and text scenes](references/serialization-and-text-scenes.md).
- Any project that accepts remote, user-authored, modded, downloaded, or save-file content: also load [security and untrusted content](references/security-and-untrusted-content.md).
- Any performance request: load [performance and profiling](references/performance-and-profiling.md) before prescribing an optimization, then load the relevant subsystem reference.
- Any platform build or export change: load [export, release, and signing](references/export-release-and-signing.md) plus the target-platform file.
- Any engine-version change: load [migration and upgrades](references/migration-and-upgrades.md), [official docs and versioning](references/official-docs-and-versioning.md), and the affected subsystem references.
- Any agent-driven scene mutation or project execution: load [agent and MCP safety](references/agent-and-mcp-safety.md).

## Verification ladder

Stop after the first level that provides sufficient evidence, unless repository instructions require more:

1. Inspect changed files and `git diff --check`.
2. Parse/build the affected language: GDScript through Godot, C# through `dotnet build`, native code through its configured build system.
3. Run a headless import or startup check with the project's matching Godot binary.
4. Run targeted tests or the affected scene.
5. Run broader integration tests and target exports only when justified.

Before running Godot, identify whether doing so executes `@tool` scripts, editor plugins, autoloads, native extensions, or project startup code. Treat unfamiliar repositories as untrusted.

## Completion report

State:

- files and behavior changed;
- validation actually executed and its result;
- validation not executed and why;
- compatibility or migration risks;
- any required editor-side or platform-side verification.
