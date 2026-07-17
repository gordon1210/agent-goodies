# Agent Goodies

Portable agent plugins packaged for both Codex/ChatGPT and Claude Code.

[![Validate](https://github.com/gordon1210/agent-goodies/actions/workflows/validate.yml/badge.svg)](https://github.com/gordon1210/agent-goodies/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Plugins

### Idea Workbench

`idea-workbench` turns a rough vision into a reviewed design and an
implementation-ready plan. Its skills form one composable path, but each can
also start from an existing artifact:

```text
rough vision
    -> shape-idea -> idea brief
    -> explore-options -> chosen direction
    -> write-design-doc -> design document
    -> review-design-doc -> readiness review
    -> plan-implementation -> delivery plan
```

Use `develop-idea` when the right starting stage is unclear. It routes to one
of the five artifact-producing skills without owning another document.

The workflow adapts to greenfield projects, changes to existing systems, and
hybrid work that connects something new to an established system. See the
[Idea Workbench guide](plugins/idea-workbench/README.md) for usage examples and
entry points.

## Repository layout

```text
.
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    └── idea-workbench/
        ├── .codex-plugin/plugin.json
        ├── .claude-plugin/plugin.json
        └── skills/
```

The repository has independent marketplace catalogs for Codex/ChatGPT and
Claude Code. This lets each catalog expose a different set or order of plugins
and use host-specific marketplace metadata. Each host also keeps its own plugin
manifest, while both load the same `skills/`, `scripts/`, and `assets/`
directories.

- `.agents/plugins/marketplace.json`: Codex/ChatGPT marketplace bucket
- `.claude-plugin/marketplace.json`: Claude Code marketplace bucket

## Add a portable plugin or skill

Create each plugin in `plugins/<plugin-name>/`, then add its independent entry
to one or both marketplace catalogs. Put shared skills in
`plugins/<plugin-name>/skills/<skill-name>/SKILL.md`:

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

## Installation

For Codex/ChatGPT:

```bash
codex plugin marketplace add gordon1210/agent-goodies
```

Then install `idea-workbench` from the `agent-goodies` marketplace in the
Plugins browser and start a new task.

For Claude Code:

```bash
claude plugin marketplace add gordon1210/agent-goodies
claude plugin install idea-workbench@agent-goodies
```

## Local development

Clone the repository, then add the local checkout as a marketplace:

```bash
codex plugin marketplace add .
claude plugin marketplace add .
```

Claude Code can also load the plugin directly while iterating:

```bash
claude --plugin-dir ./plugins/idea-workbench
```

Run the repository validator before committing:

```bash
python3 scripts/validate_repo.py
```

## Contributing and releases

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the
authoring and validation workflow.

Plugins are versioned independently. See [RELEASING.md](RELEASING.md) for the
versioning, changelog, tag, and GitHub Release process.

## License

MIT. See [LICENSE](LICENSE).
