# Serialization and text scenes

Use this whenever `.tscn`, `.tres`, `.uid`, `project.godot` or `export_presets.cfg` changes.

## Safe edit boundary

Text scene/resource files are structured serialization, not casual configuration. Small hand edits are acceptable only when the format and surrounding IDs are understood. Prefer Godot or a trusted deterministic migration for structural changes.

Never hand-edit:

- binary `.scn` or `.res` files;
- files under `.godot/`;
- imported cache artifacts;
- generated UID caches;
- third-party addon resources as collateral cleanup.

## Preserve

- `[gd_scene]` or `[gd_resource]` format and load steps;
- `ext_resource` paths and UIDs;
- `sub_resource` IDs and references;
- node parent/owner relationships;
- `instance=ExtResource(...)` links;
- typed property values;
- signal connections;
- editable-instance metadata;
- animation track paths and resource bindings.

Do not renumber IDs or reorder blocks unless required. Godot may accept multiple layouts, but unnecessary churn creates merge conflicts and hides semantic changes.

## External paths

Use `res://` for project resources and `user://` for user data. Do not serialize machine-specific absolute paths into project resources. Preserve path case because exports and non-Windows platforms may be case-sensitive.

## UIDs

Treat UIDs as stable identity managed by Godot. Do not invent, copy or globally rewrite them. When moving resources, use the project's supported editor/version workflow and inspect all references. A path can still matter even when a UID exists, especially across versions and tools.

## Scene diff review

After an edit, confirm:

1. only intended nodes/resources changed;
2. no script or owner disappeared;
3. no external resource became a subresource accidentally;
4. overridden properties still target the intended instance;
5. signal targets and method names exist;
6. no import metadata or editor-only state leaked into the diff;
7. the file loads with the matching engine.

## Project settings

`project.godot` changes can affect every scene and export. Make targeted edits, preserve existing feature tags and input-event arrays, and explain settings with operational consequences. Never replace the file with a generated minimal version.
