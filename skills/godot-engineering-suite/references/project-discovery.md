# Project discovery

Load this before any non-trivial Godot task. The goal is a compact, evidence-based project model, not a full repository dump.

## Discover in this order

1. Find the nearest `project.godot`; do not assume the Git root and Godot root are identical.
2. Read applicable repository instructions and `GODOT_PROJECT.md` when present.
3. Inspect `project.godot` for:
   - `config/features` and renderer features;
   - main scene and application settings;
   - enabled editor plugins;
   - autoloads;
   - input actions relevant to the task;
   - display, physics and rendering settings relevant to the task.
4. Identify languages and native boundaries from `.gd`, `.csproj`, `.sln`, `.gdextension`, C/C++ and shader files.
5. Inspect `addons/`, `export_presets.cfg`, test folders, CI configuration and project wrapper scripts.
6. Read only the scenes, scripts and resources on the dependency path of the requested behavior.

## Version detection

Prefer evidence in this order:

1. Repository wrapper, lock file, container image or CI configuration pinning a binary.
2. `GODOT_PROJECT.md` or project documentation.
3. A permitted `godot --version` invocation using the repository's configured executable.
4. `config/features` in `project.godot` as a lower-bound hint, not proof of the exact patch release.

Do not migrate APIs merely because a newer engine exists. Match the project's current minor branch unless the user explicitly requests an upgrade.

## Compact inventory

Record only facts needed by the task:

```text
root: /path/to/project
engine: 4.x.y, standard or .NET
renderer: Forward+ | Mobile | Compatibility
targets: desktop | mobile | web | console | XR
languages: GDScript | C# | native
main scene: res://...
affected ownership chain: scene -> child scene -> script/resource
relevant addons/autoloads:
validation commands:
```

The bundled `scripts/inspect_godot_project.py` can produce this inventory without launching Godot.

## Red flags requiring extra caution

- unfamiliar `@tool` scripts or enabled `EditorPlugin`s;
- `.gdextension` libraries or engine modules;
- post-import scripts;
- executable wrapper scripts fetched from the network;
- project files containing secrets or production service endpoints;
- very large generated text scenes;
- multiple Godot projects in one repository;
- an editor likely open on the same scenes the agent will rewrite.

If any red flag applies, load `security-and-untrusted-content.md` and `agent-and-mcp-safety.md` before execution.
