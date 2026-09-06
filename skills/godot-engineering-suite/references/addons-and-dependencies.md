# Addons and dependencies

Use when introducing, updating, configuring or reviewing third-party Godot addons and SDKs.

## Before adding

Confirm the requirement cannot be met cleanly with existing code or the engine. Review:

- maintainer and repository provenance;
- license and redistribution terms;
- supported Godot versions/renderers/platforms;
- editor/runtime code and native binaries;
- transitive downloads or build steps;
- open issues and update cadence;
- data/network access;
- project files/autoloads/settings the addon changes.

Do not install from an unpinned branch or arbitrary release URL in automated agent work.

## Pinning

Record an exact version, commit or immutable artifact hash. Keep license notices and source URL. For vendored code, isolate local patches and document them. Do not silently modify vendored code to match project style.

## Enablement

Editor plugins, autoloads and project settings are mutating changes. Enable only the required plugin and inspect resulting diffs. Never copy an addon's sample project settings wholesale over the game.

## Updates

Read release and migration notes. Update one dependency at a time, with a clean baseline. Verify editor startup, imports, scenes that use the addon, exports and native libraries on affected platforms.

## Removal

Search scenes/resources/scripts/project settings for classes, resources, autoloads and UIDs before deleting files. Disable the plugin first, migrate data, then remove and verify a clean import.

## Security

Treat addon code exactly like application code, and native addons as executable binaries. Avoid addons requiring broad filesystem, credential or network access without a documented need and sandbox boundary.
