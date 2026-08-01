# Agent Goodies

Portable agent skills and plugins for skills.sh, Codex/ChatGPT, and Claude
Code.

[![Validate](https://github.com/gordon1210/agent-goodies/actions/workflows/validate.yml/badge.svg)](https://github.com/gordon1210/agent-goodies/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Skills and plugins

### Add Tauri Native Window Effects

`add-tauri-native-window-effects` implements and diagnoses native window
materials in Tauri 2 apps. It covers macOS vibrancy and Liquid Glass, Windows
Mica and Acrylic, the shared WebView transparency stack, and a safe opaque
fallback for unsupported platforms. Its canonical package lives at
`skills/add-tauri-native-window-effects` and is installable through the skills
CLI.

### Handoff

`handoff` keeps compact, repo-local continuity state so substantial work can
survive agent and session changes. Its canonical package lives at
`skills/handoff`, which makes it directly discoverable by the skills CLI while
Claude Code's marketplace references that same directory directly. Codex users
install this standalone skill through the skills CLI. It activates for existing
handoff repositories, explicit continuity requests, and agent/session
transitions; initializing handoff state in a new repository remains opt-in.

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
├── plugins/
│   └── idea-workbench/
│       ├── .codex-plugin/plugin.json
│       ├── .claude-plugin/plugin.json
│       └── skills/
└── skills/
    ├── add-tauri-native-window-effects/
    │   └── SKILL.md
    └── handoff/
        └── SKILL.md
```

The repository has independent marketplace catalogs for Codex/ChatGPT and
Claude Code. This lets each catalog expose a different set or order of
packages and use host-specific marketplace metadata. Standalone skills remain
installable through the skills CLI even when they are not wrapped as a plugin
for a host marketplace.

- `.agents/plugins/marketplace.json`: Codex/ChatGPT marketplace bucket
- `.claude-plugin/marketplace.json`: Claude Code marketplace bucket

## Add a portable plugin or skill

Use `skills/<skill-name>/SKILL.md` for a standalone skill. This is the canonical
layout discovered by the skills CLI. Claude Code can expose that directory as
a manifestless marketplace entry by setting `strict` to `false` and declaring
the skill path in the entry.

Use `plugins/<plugin-name>/skills/<skill-name>/SKILL.md` for a plugin that
bundles several skills, needs a Codex marketplace entry, or includes other
components. Codex plugin archives currently need a real `skills/` subtree;
do not depend on symlinks inside that archive. Add each package only to the
catalogs that can load its layout:

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

With the skills CLI, install either standalone skill globally so it is
available in every repository:

```bash
npx skills add gordon1210/agent-goodies --skill add-tauri-native-window-effects --global
npx skills add gordon1210/agent-goodies --skill handoff --global
```

Omit `--global` for a project-scoped installation. The bundled helper stays
inside the installed skill and requires no `package.json` script or launcher
configuration. Running the helper requires Python 3.9 or newer; it has no
third-party Python dependencies.

For Codex/ChatGPT:

```bash
codex plugin marketplace add gordon1210/agent-goodies
```

Then install `idea-workbench` from the `agent-goodies` marketplace in the
Plugins browser. Install `handoff` with the skills CLI shown above.

For Claude Code:

```bash
claude plugin marketplace add gordon1210/agent-goodies
claude plugin install idea-workbench@agent-goodies
claude plugin install handoff@agent-goodies
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
python3 -m unittest tests/test_handoff.py -v
```

## Contributing and releases

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the
authoring and validation workflow.

Plugins are versioned independently. See [RELEASING.md](RELEASING.md) for the
versioning, changelog, tag, and GitHub Release process.

## License

MIT. See [LICENSE](LICENSE).
