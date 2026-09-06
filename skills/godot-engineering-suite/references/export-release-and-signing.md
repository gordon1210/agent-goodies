# Export, release, and signing

Use for `export_presets.cfg`, export templates, release artifacts, dedicated servers, signing and store packaging.

## Pin the toolchain

Use the exact Godot branch and matching export templates. Record platform SDK/JDK/Xcode/.NET/native tool versions in CI or project documentation. Do not export with an arbitrary local editor and call the artifact reproducible.

## Preset discipline

Treat `export_presets.cfg` as code. Review:

- selected resources and filters;
- feature tags and renderer;
- architecture and debug/release mode;
- permissions/entitlements;
- application identifiers and versions;
- dedicated-server stripping;
- encryption/signing configuration;
- custom templates and plugins.

Never commit passwords, private keys, API secrets or store credentials. Inject secrets through the platform/CI secret mechanism and ensure logs do not echo them.

## Resource inclusion

Verify that required dynamically loaded resources are included and development/test/source assets are excluded. Resource paths constructed only at runtime can evade dependency discovery; use explicit filters or manifests.

## Build metadata

Embed or publish game version, commit, engine version, content/protocol/save schema and build channel. Keep debug and production services/configuration separate.

## Signing and stores

Signing/notarization is a deployment boundary. Limit key access, use short-lived CI credentials where possible and separate unsigned build generation from signing. Follow current platform/store documentation rather than hard-coded historical commands.

## Verification

1. clean import with pinned engine;
2. release export using the real preset;
3. inspect artifact contents and size;
4. launch/install on target OS/device;
5. verify save paths, permissions, networking and renderer;
6. scan logs for debug output/secrets;
7. verify signature/notarization/store validation;
8. retain checksums and provenance.

A successful export command does not prove the artifact runs or meets store requirements.
