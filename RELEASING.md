# Releasing plugins

Every plugin in this repository has its own semantic version and release
history. The repository itself does not have a single shared version.

## Version source of truth

For a plugin that supports both hosts, keep these values identical:

- `plugins/<plugin-name>/.codex-plugin/plugin.json`
- `plugins/<plugin-name>/.claude-plugin/plugin.json`

Do not repeat the version in a marketplace entry. Claude Code gives the plugin
manifest precedence, so a duplicated marketplace version can become stale.

Use semantic versioning:

- patch: fixes and backward-compatible refinements;
- minor: new skills, artifacts, or backward-compatible capabilities;
- major: incompatible changes to names, behavior, artifacts, or workflow
  contracts.

Before `1.0.0`, use a minor bump for an incompatible behavior change and call
it out clearly in the changelog.

## Prepare a release

1. Update both plugin manifests to the new version.
2. Add a dated `## [<version>] - YYYY-MM-DD` section to the plugin's
   `CHANGELOG.md`.
3. Run `python3 scripts/validate_repo.py`.
4. Test installation in both supported hosts when their CLIs are available.
5. Merge the release change into `main` and wait for the Validate workflow to
   pass.

## Publish a release

Run the **Release plugin** workflow from the GitHub Actions page on `main` and
enter the plugin name and version. The workflow validates the repository,
checks the manifest versions and changelog, creates the immutable tag, and
publishes a GitHub Release using that changelog entry.

Tags use this format:

```text
<plugin-name>--v<version>
```

For example:

```text
idea-workbench--v0.1.0
```

The double-hyphen form is compatible with Claude Code's versioned plugin
dependency resolution. Never delete, move, or reuse a published release tag;
prepare a new patch version instead.
