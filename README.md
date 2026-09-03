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
`skills/add-tauri-native-window-effects`, which makes it directly discoverable
by the skills CLI while Claude Code's marketplace references that same
directory directly.

### Handoff

`handoff` keeps compact, repo-local continuity state so substantial work can
survive agent and session changes. Its canonical package lives at
`skills/handoff`, which makes it directly discoverable by the skills CLI while
Claude Code's marketplace references that same directory directly. Codex users
install this standalone skill through the skills CLI. It activates for existing
handoff repositories, explicit continuity requests, and agent/session
transitions; initializing handoff state in a new repository remains opt-in.

### Grok CLI

`grok-cli` orchestrates xAI Grok Build as a bounded coding collaborator. It
covers the interactive CLI, headless `grok -p` automation, structured output,
sessions, ACP through `grok agent`, configuration, permissions, sandboxing, and
extensions, with detailed patterns for delegation, agent pairing, consulting,
rubber-duck dialogue, and independent review. A dependency-free Python bridge
adds live ACP status, steering, cancellation, and permission handling. Its
canonical package lives at `skills/grok-cli`, which makes it directly
discoverable by the skills CLI while Claude Code's marketplace references that
same directory directly.

### Rust Codebase Excellence

`rust-codebase-excellence` guides production-grade Rust design, implementation,
review, testing, security, performance, and release work while preserving
repository contracts and avoiding speculative complexity. Its canonical package
lives at `skills/rust-codebase-excellence`, which makes it directly discoverable
by the skills CLI while Claude Code's marketplace references that same
directory directly.

### Deep Code Review

`deep-code-review` performs evidence-driven reviews of pull requests, commits,
patches, and working-tree changes. It traces changed behavior through callers,
state, data flows, trust boundaries, tests, configuration, and deployment
contracts while aggressively filtering speculative findings. Its canonical
package lives at `skills/deep-code-review`, which makes it directly discoverable
by the skills CLI while Claude Code's marketplace references that same directory
directly.

### Design & UI Excellence

`design-ui-excellence` routes website, landing-page, marketing, product UI,
design-system, content, prototyping, and audit work through focused workflows,
guides, and reusable templates. Its canonical package lives at
`skills/design-ui-excellence`, which makes it directly discoverable by the
skills CLI while Claude Code's marketplace references that same directory
directly.

### React Codebase Excellence

`react-codebase-excellence` guides production-grade React 18 and 19 design,
implementation, review, testing, accessibility, security, performance, and
upgrades while preserving exact repository and framework contracts. Its
canonical package lives at `skills/react-codebase-excellence`, which makes it
directly discoverable by the skills CLI while Claude Code's marketplace
references that same directory directly.

### TypeScript Codebase Excellence

`typescript-codebase-excellence` guides production-grade TypeScript design,
implementation, review, testing, security, performance, packaging, and
TypeScript 6/7 migration work without speculative architecture or incidental
toolchain changes. Its canonical package lives at
`skills/typescript-codebase-excellence`, which makes it directly discoverable
by the skills CLI while Claude Code's marketplace references that same
directory directly.

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
    ├── handoff/
    │   └── SKILL.md
    ├── grok-cli/
    │   └── SKILL.md
    ├── deep-code-review/
    │   └── SKILL.md
    ├── rust-codebase-excellence/
    │   └── SKILL.md
    ├── design-ui-excellence/
    │   └── SKILL.md
    ├── react-codebase-excellence/
    │   └── SKILL.md
    └── typescript-codebase-excellence/
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

With the skills CLI, install a standalone skill globally so it is
available in every repository:

```bash
npx skills add gordon1210/agent-goodies --skill add-tauri-native-window-effects --global
npx skills add gordon1210/agent-goodies --skill handoff --global
npx skills add gordon1210/agent-goodies --skill grok-cli --global
npx skills add gordon1210/agent-goodies --skill deep-code-review --global
npx skills add gordon1210/agent-goodies --skill rust-codebase-excellence --global
npx skills add gordon1210/agent-goodies --skill design-ui-excellence --global
npx skills add gordon1210/agent-goodies --skill react-codebase-excellence --global
npx skills add gordon1210/agent-goodies --skill typescript-codebase-excellence --global
```

Omit `--global` for a project-scoped installation. A bundled helper, when
present, stays inside the installed skill and requires no `package.json` script
or launcher configuration. Running the helper requires Python 3.9 or newer; it
has no third-party Python dependencies.

For Codex/ChatGPT:

```bash
codex plugin marketplace add gordon1210/agent-goodies
```

Then install `idea-workbench` from the `agent-goodies` marketplace in the
Plugins browser. Install standalone skills with the skills CLI shown above.

For Claude Code:

```bash
claude plugin marketplace add gordon1210/agent-goodies
claude plugin install idea-workbench@agent-goodies
claude plugin install add-tauri-native-window-effects@agent-goodies
claude plugin install handoff@agent-goodies
claude plugin install grok-cli@agent-goodies
claude plugin install deep-code-review@agent-goodies
claude plugin install rust-codebase-excellence@agent-goodies
claude plugin install design-ui-excellence@agent-goodies
claude plugin install react-codebase-excellence@agent-goodies
claude plugin install typescript-codebase-excellence@agent-goodies
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
python3 -m unittest tests/test_grok_acp.py -v
```

## Contributing and releases

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the
authoring and validation workflow.

Plugins are versioned independently. See [RELEASING.md](RELEASING.md) for the
versioning, changelog, tag, and GitHub Release process.

## License

MIT. See [LICENSE](LICENSE).
