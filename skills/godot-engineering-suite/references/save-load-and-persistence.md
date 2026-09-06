# Save/load and persistence

Use for save games, settings, checkpoints, cloud-sync files and schema migrations.

## Treat saves as an external data format

Define a stable versioned schema independent from scene layout. Do not serialize arbitrary nodes, script instances or resource graphs and expect long-term compatibility.

A save should contain authoritative state and stable IDs, not derived UI values, transient node paths or cached resources.

## Storage

Use `user://` for writable user data. Resolve platform paths through Godot; do not hard-code home directories. Keep profile slots and settings separate from large world saves where their lifecycles differ.

## Write safely

1. serialize to a temporary file;
2. flush/close and validate when practical;
3. retain or rotate a previous known-good copy;
4. atomically replace the active file using the safest supported platform pattern;
5. never leave the only valid save truncated after a crash.

Protect concurrent save requests with a queue or generation token. A background serializer may process pure data, but filesystem and engine-object access must obey thread constraints.

## Validation and security

Assume save files can be corrupted or modified. Bound lengths/counts, validate types and versions, reject unsafe paths and never instantiate arbitrary classes/scripts from save data. Encryption without authenticated integrity does not prevent tampering; obfuscation is not security.

Do not store service secrets in a client save.

## Migration

- Include schema and content/build versions.
- Migrate one version step at a time or through a clearly tested canonical path.
- Preserve unknown optional fields only if forward compatibility is a goal.
- Back up before destructive migration.
- Fail with an actionable message rather than silently resetting progress.

## Settings

Apply defaults first, then validated user overrides. Handle removed devices/resolutions and renamed input actions. Save settings independently from gameplay autosaves.

## Verification

Test new profile, round trip, old-version fixtures, partial/corrupt/truncated data, missing content IDs, full disk/permission failure, rapid repeated saves and platform path behavior. Compare loaded authoritative state, not merely file existence.
