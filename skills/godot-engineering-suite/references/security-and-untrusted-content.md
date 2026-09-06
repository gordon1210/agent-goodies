# Security and untrusted content

Use whenever the project processes network data, mods, saves, downloaded assets, user text/files, native code or external services.

## Trust boundaries

Mark every external boundary: remote peer, HTTP response, save/mod file, command-line argument, deep link, clipboard, OS path, platform callback, addon, native library and editor import. Validate at the boundary before converting data into engine objects or paths.

## Filesystem

- Keep writes under intended `user://` locations unless explicit user export is requested.
- Canonicalize and verify paths; reject traversal, absolute paths and unexpected schemes.
- Bound file size, count, nesting and decompression output.
- Do not load arbitrary `.gd`, `.tscn`, `.tres`, `.pck`, `.zip` or native libraries from untrusted users.
- Use allowlisted extensions and parse data formats with schemas.

## Network

Use TLS where appropriate, validate certificates through supported platform behavior, set timeouts and size limits, and treat all responses as untrusted. Authenticate and authorize server-side. Do not embed durable service secrets in exported clients.

## Multiplayer

Validate RPC caller, authority, rate, ranges and state transitions. Never trust client-side inventory, movement, cooldown or purchase results. Avoid exposing internal filesystem/resource paths in protocol fields.

## Mods and scripting

A PCK, scene, Resource, GDScript or native extension can contain executable behavior. Safe data-only modding requires a deliberately restricted schema/interpreter and asset allowlist. Do not market arbitrary project-content loading as sandboxed.

## External processes and URLs

Do not build shell command strings from user input. Use argument arrays and strict allowlists. Confirm before opening external URLs or files, and restrict schemes.

## Logging/privacy

Do not log tokens, passwords, personal data or full untrusted payloads. Sanitize user-visible rich text/BBCode and bound rendering complexity.

## Release review

Search exported resources and logs for keys/endpoints, review permissions/entitlements, verify debug interfaces are disabled and test malformed input. Native dependencies require separate vulnerability and provenance review.
