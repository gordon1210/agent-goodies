# Agent Goodies

Portable agent skills packaged for both Codex/ChatGPT and Claude Code.

## Repository layout

```text
.
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    └── agent-goodies/
        ├── .codex-plugin/plugin.json
        ├── .claude-plugin/plugin.json
        ├── skills/
        ├── scripts/
        └── assets/
```

The repository has independent marketplace catalogs for Codex/ChatGPT and
Claude Code. This lets each catalog expose a different set or order of plugins
and use host-specific marketplace metadata. Each host also keeps its own plugin
manifest, while both load the same `skills/`, `scripts/`, and `assets/`
directories.

- `.agents/plugins/marketplace.json`: Codex/ChatGPT marketplace bucket
- `.claude-plugin/marketplace.json`: Claude Code marketplace bucket

## Add a portable skill

Create a directory at `plugins/agent-goodies/skills/<skill-name>/` containing a
`SKILL.md` file:

```markdown
---
name: skill-name
description: Explain what the skill does and when it should be used.
---

Write provider-neutral instructions here.
```

Keep shared skills portable:

- Describe capabilities instead of naming host-specific tools.
- Use relative paths for references, scripts, and assets.
- Avoid Claude-only frontmatter and substitutions in shared skills.
- Avoid Codex-only channels, directives, or tool names in shared skills.
- Put genuinely host-specific behavior in host-specific configuration instead
  of branching throughout a shared skill.

## Local installation

For Codex/ChatGPT:

```bash
codex plugin marketplace add .
```

Then install `agent-goodies` from the `agent-goodies` marketplace in the
Plugins browser and start a new task.

For Claude Code:

```bash
claude plugin marketplace add .
claude plugin install agent-goodies@agent-goodies
```

During development, Claude Code can also load the plugin directly:

```bash
claude --plugin-dir ./plugins/agent-goodies
```

## Release checklist

1. Keep both plugin manifests on the same semantic version.
2. Validate every `SKILL.md` and all referenced relative paths.
3. Validate the Codex plugin manifest and the Claude marketplace/plugin.
4. Test installation in both hosts before publishing a release.
