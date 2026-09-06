# Editor tools and tool scripts

Use for `@tool`, EditorPlugin, custom inspectors, docks, gizmos, import plugins and editor automation.

## Security and execution

`@tool` scripts and enabled editor plugins execute inside the editor while authoring. Opening an unfamiliar project can therefore execute code. Review before launching and load `security-and-untrusted-content.md`.

## Tool-script discipline

- Gate runtime-only behavior with `Engine.is_editor_hint()` where appropriate.
- Expect partial scene state, repeated property updates, undo/redo and script reloads.
- Avoid destructive work in setters, `_ready()` or notification loops.
- Never write outside the project or user-data scope without explicit user action.
- Debounce expensive previews and avoid continuously dirtying scenes.
- Do not depend on game autoload state unless the plugin owns that contract.

## Undo/redo

Editor-visible mutations should integrate with the editor's undo/redo system. Register both do and undo methods and preserve object lifetime. A tool that bypasses undo must make that consequence explicit before running.

## EditorPlugin lifecycle

Register controls, inspectors, importers, autoloads and types in `_enter_tree()`, and remove exactly what was registered in `_exit_tree()`. Handle plugin disable/reload without duplicate docks, menus or signals.

## Import plugins

Treat imported source as untrusted and bound parsing time/memory. Produce deterministic outputs and include importer versioning so changes trigger intended reimports. Do not perform network fetches during import.

## Scene mutation

Use owner and edited-scene-root semantics correctly so nodes persist. Avoid resaving unrelated open scenes. Verify generated paths and collision with existing files before writing.

## Verification

Test enable, disable, reload, project restart, undo/redo, empty/partial selection, read-only files and multiple open scenes. Inspect the repository diff after every tool-generated mutation.
