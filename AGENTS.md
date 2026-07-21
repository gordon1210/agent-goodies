# Repository Instructions

## Purpose

This repository distributes skills and plugins through skills.sh,
Codex/ChatGPT, and Claude Code. Keep shared behavior portable and isolate
host-specific packaging or configuration.

## Repository layout

- `.agents/plugins/marketplace.json` is the Codex/ChatGPT marketplace.
- `.claude-plugin/marketplace.json` is the Claude Code marketplace.
- `skills/<skill-name>/SKILL.md` is the canonical standalone-skill layout used
  by the skills CLI.
- Claude Code may expose a standalone skill directly with a manifestless
  marketplace entry using `strict: false` and an explicit `skills` path.
- Multi-skill plugins live under `plugins/<plugin-name>/`, with both host
  manifests and a `skills/<skill-name>/SKILL.md` subtree.
- Keep supporting scripts, references, and assets inside the relevant plugin or
  standalone skill root.

## Authoring rules

- Use lowercase kebab-case names. A plugin directory and both manifest names
  must match.
- Keep the two plugin manifest versions aligned when a plugin targets both
  hosts.
- Keep the version in each host manifest, not in a marketplace entry. The
  manifests are the release source of truth.
- Add a plugin only to the marketplace buckets that should expose it. The two
  catalogs may contain different plugins and ordering.
- Preserve existing marketplace ordering unless a reorder is requested.
- Codex marketplace entries must include installation policy, authentication
  policy, and category. Omit product gating unless explicitly requested.
- Reference only paths inside the plugin root and keep manifest paths relative.
- Keep top-level `skills/<skill-name>` entries as real directories because the
  skills CLI's repository scan skips symlink directory entries.
- Codex marketplace plugins need a real plugin-local `skills/` subtree. Its
  current cache installation does not preserve symlinks, so materialize and
  verify a wrapper if one is required for a canonical standalone skill.
- Declare apps, MCP servers, hooks, or other host integrations only when their
  real companion configuration exists.
- Do not leave placeholder metadata or unfinished TODO markers in manifests.

## Portable skills

- Prefer the common `name` and `description` frontmatter fields.
- Describe capabilities rather than naming provider-specific tools.
- Avoid host-specific frontmatter, substitutions, channels, and directives in
  shared skills.
- Put genuinely host-specific behavior in host-specific configuration or a
  host-specific skill instead of branching throughout a shared skill.
- Keep each `SKILL.md` concise and place detailed material in nearby references
  or scripts.

## Verification

- Parse every changed JSON file.
- Confirm marketplace source paths resolve to the intended plugin directories.
- Confirm plugin names and versions agree across applicable catalogs and
  manifests.
- Run `python3 scripts/validate_repo.py` before committing a plugin change.
- Run `python3 -m unittest tests/test_handoff.py -v` after changing the Handoff
  skill.
- Run the relevant Codex and Claude validators when available. Report any
  validator that could not be run.
- Keep `README.md` accurate when repository structure or installation changes.

## Releases

- Version each plugin independently with semantic versioning.
- Update both host manifests and the plugin changelog in the same change.
- Tag releases as `<plugin-name>--v<version>`; never move or reuse a release
  tag.
- Create releases only from the default branch after validation passes.
- Follow `RELEASING.md` for the full release process.

Do not install, publish, commit, push, or release changes unless explicitly
requested.
