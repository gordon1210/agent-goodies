# CLI areas and operational map

Grok Build is more than `grok -p`. It includes an interactive TUI, ACP agent
server, project-context discovery, extensions, sessions, worktrees, terminal
integration, monitoring, and administrative commands. Use this map to find the
right surface without treating every available command as authorized.

This reference was checked against Grok Build 1.0.13. Current command help and
the bundled guide remain authoritative.

## Interactive TUI

Run `grok` with no arguments for the full-screen interface, or provide an
initial prompt:

```bash
grok
grok "Explain the architecture before changing anything"
```

The TUI is best when a human will inspect context, approve tools, switch modes,
and steer continuously. It supports:

- File references and context selection.
- Slash commands for settings, models, permissions, sessions, skills,
  workflows, agents, MCP servers, plugins, hooks, docs, and diagnostics.
- Plan and always-approve or auto permission modes.
- Session resume, fork, rewind, compaction, and export workflows.
- Full-screen, inline, alternate-screen, and experimental minimal rendering.
- Mouse, clipboard, image, multiline input, and terminal-dependent shortcuts.

Do not memorize shortcut keys from an older release. Use the TUI's help and
`/docs`, and read the bundled keyboard and slash-command chapters for the
installed build. Terminal families can reserve or remap key combinations.

## Installation, authentication, and updates

These are lifecycle operations, not prerequisites to perform silently:

- `grok login` starts supported authentication flows; device-code options are
  useful on headless machines.
- `grok logout` clears cached credentials.
- `grok setup` fetches and installs managed configuration.
- `grok update` checks for or installs CLI versions and channels.
- `grok version` and `grok version --json` inspect the installed version.

Only version inspection is a routine read-only preflight. Installation,
authentication, logout, setup, channel switching, and update require explicit
user intent and can change credentials, executable files, or managed policy.

For a headless environment, existing cached auth or an injected `XAI_API_KEY`
can be used. Never print, persist, or copy the key into a prompt, config example,
trace, or log. Do not rewrite the Grok home or credential context to simulate a
clean installation.

## Effective configuration

Run:

```bash
grok inspect
grok inspect --json
```

This is the primary way to see what Grok resolved for the current directory,
including config sources and warnings, project root and instructions, skills,
agents, plugins, hooks, MCP servers, permissions, and compatibility layers.

Configuration can come from CLI flags, environment, organizational
requirements and managed config, runtime overlays, user config, project config,
and compatibility settings. Precedence and merge behavior vary by setting, so
do not infer the winner from filenames alone. Use the effective inspection.

Common locations include:

- User configuration and state under `~/.grok/`.
- Project configuration and rules under `.grok/`.
- `AGENTS.md` and compatible instruction or settings formats discovered from
  project root to working directory.
- System and user managed or requirements files in enterprise deployments.

Do not edit config to bypass a task failure. Persistent config changes affect
future sessions and require separate user intent.

## Models and reasoning effort

Use `grok models` to discover models currently available to the authenticated
account and installation. Select with `--model` or the TUI model command only
when the task needs a specific choice.

Reasoning-effort values are model-dependent. The CLI may advertise canonical
tiers and model-specific menu IDs. Query the installed menu or help instead of
assuming every model accepts every level.

Record the chosen model when reproducibility matters, but design scripts to
handle retirement or unavailability. Model names shown in documentation are
examples, not permanent contracts.

## Instructions, rules, skills, and workflows

### Instructions and rules

Grok discovers repository instructions from the project root toward `--cwd`,
plus Grok-native rules and enabled compatibility formats. `--rules` appends
session-specific rules. `--system-prompt-override` replaces the system prompt
and should not be used to evade repository instructions or normal safety.

### Skills

Skills are instruction packages discovered from supported project, user, and
compatibility locations. Their descriptions can trigger automatic use, and
user-invocable skills can appear in the slash-command surface. Inspect the
skills resolved for the actual directory; duplicate names can be qualified by
their source.

Reading a skill is low risk; installing or modifying one changes future agent
behavior. Skills can instruct tools and should be reviewed like code-adjacent
automation.

### Workflows and commands

Saved workflows and slash commands package repeated prompt sequences. Browse
their source and instructions before invocation. A friendly command name does
not reveal the tools, hooks, or external calls it may cause.

## Main agents, personas, and subagents

Keep these concepts separate:

- `--agent <name-or-path>` selects a main-agent definition or profile.
- `--agents <json>` supplies inline child-agent definitions in headless mode.
- Personas or agent definitions change behavior and available tools.
- Grok subagents are child sessions spawned by a running Grok session.
- `grok agent` is an ACP server transport, not a child agent.

Tested built-in child roles include a general-purpose worker, a read-oriented
explorer, and a planning role. Their exact tools and names can evolve. A child
has its own context, can report a summary to the parent, and may support
background execution, dedicated worktree isolation, explicit working
directory, resume, and custom definitions.

Subagents are useful for genuinely independent research or implementation
slices. They are poor fits for tight user dialogue, shared mutable ownership,
or tasks where the host must approve each step. Child agents can inherit parent
MCP access and multiply turns and cost.

Use `--no-subagents` when the host owns orchestration. Do not assume a fixed
maximum depth from old documentation; inspect the current config reference.

## Memory

Cross-session memory can retain useful project knowledge and can also bias an
independent consultation. The tested process-level switch `GROK_MEMORY=0`
disables it for a call. Use that for clean reviews and independent opinions.

`grok memory clear` destroys stored memory at a selected scope. Do not use it
to manufacture independence; disable memory for the process instead. Clearing
pre-existing memory requires explicit, bounded user authorization.

## Sessions and transcripts

Headless and TUI conversations are persisted under Grok state. Relevant
surfaces include:

- `grok sessions list`
- `grok sessions search`
- `grok sessions delete`
- `grok export`
- `--resume`, `--continue`, `--session-id`, and `--fork-session`
- TUI resume, fork, rewind, compact, rename, and export commands

Listing and searching are read-only. Export can write a transcript to a target
or reveal sensitive conversation and tool data. Delete is destructive.

Resume by exact returned ID in automation. Titles can be ambiguous, and
`--continue` races across concurrent jobs in the same directory. A rewind or
conversation fork changes session history; it does not roll back filesystem
changes.

## Worktrees

Interactive Grok sessions can create and manage Git worktrees. The command
family includes inspection and operations such as list, show, detach, salvage,
remove, garbage collection, artifact cleanup, and database inspection.

Use read-only list/show/database inspection first. Removal, garbage collection,
detach, salvage, and cleanup can change Git or filesystem state. Validate exact
targets, ownership, provenance, and existing work before any such operation.

Do not rely on `grok -p --worktree`: the current 1.0.13 top-level help says the
headless flag does not create a worktree. A host-created worktree plus `--cwd`
is the reliable isolation pattern for delegated writes.

## MCP servers

The `grok mcp` family can:

- List effective servers.
- Add stdio, HTTP, or SSE server definitions at supported scopes.
- Enable or disable servers.
- Remove definitions.
- Diagnose startup, authentication, and protocol issues.

List and carefully scoped diagnostics are the normal inspection path. Add,
remove, enable, and disable mutate configuration. Server startup can execute a
local program or contact a remote endpoint, and tools can mutate remote state.

Inspect server command or URL, environment and headers, scope, tool schemas,
authentication, and target account before use. Subagents can inherit connected
servers.

## Plugins and marketplaces

The `grok plugin` family covers listing, installation, uninstallation, update,
enable/disable, details, validation, tagging, and marketplace management.

Plugins can bundle skills, agents, hooks, MCP servers, LSP servers, and other
code. Enabling and trusting are distinct concepts in ordinary plugin flows, but
some locations are automatically trusted. In ACP mode, `--plugin-dir` is a
highest-priority process scope and always trusts its hooks and MCP servers.

Safe inspection starts with list, details, and validation. Install, update,
enable, disable, trust, tag, marketplace add/remove/update, and uninstall are
state-changing. Tagging with a push option can change a remote Git repository.
Do not perform them without explicit user intent.

## Hooks

Hooks run commands or HTTP requests at session and tool lifecycle events. They
can add context, audit, deny a tool, rewrite input, trigger validation, or keep
an agent working.

Inspect hook origin, matcher, handler, executable or URL, environment, and
timeout. Project and plugin hooks are part of the repository trust decision;
global hooks are ambient behavior. Hook failures normally fail open, so hooks
must supplement rather than replace permissions and sandboxing.

## Permissions and sandbox

Permissions answer “may this tool call run?”; the sandbox answers “what can the
process reach even if it runs?” They are independent. Plan mode and worktrees
are separate again.

Read [Permissions, sandbox, and trust](permissions-sandbox-trust.md) before
using edit tools, shell, web, MCP, plugins, custom profiles, or always-approve.

## Plan mode

Plan mode supports design-first work and normally gates edit tools to the plan
file. Use it to produce and review an implementation plan before coding.

It is not a confinement mechanism: shell writes and subagent behavior are not
fully covered by the edit gate in the tested version. If planning must be
read-only, remove write and shell capabilities and apply a suitable sandbox.

## Terminal and background tasks

The TUI can create terminal sessions, run commands, and keep selected processes
or monitors in the background. Long-running monitors should emit bounded,
line-buffered, filtered output; unfiltered streams can overwhelm context and
may be stopped automatically.

Starting a terminal executes repository code with the user's environment and
permissions. Inspect scripts, build hooks, dependency installers, and secrets
before allowing it. Do not leave orphaned servers or watchers; report their
process and ownership when intentionally left running.

`grok wrap <command...>` runs an arbitrary command through a local PTY with OSC
52 clipboard forwarding. Its risk is the wrapped command's full behavior, not
the convenience wrapper.

## Interface, dashboard, and monitoring

Grok includes:

- `grok dashboard` for the Agent Dashboard view.
- UI themes, status-line customization, minimal/fullscreen behavior, and
  terminal capability handling.
- Session and tool monitoring views.
- Notifications and optional telemetry or feedback integrations.

UI settings are persistent configuration when saved. Monitoring can expose
prompt, file, command, cost, and session data. Treat telemetry, feedback, and
remote monitoring as external data transfer requiring explicit intent.

## Diagnostics and maintenance

| Command | Default posture |
|---|---|
| `grok version [--json]` | Read-only version inspection |
| `grok inspect [--json]` | Read-only effective-context inspection |
| `grok doctor` | Diagnostic; review help before any fix mode |
| `grok du` | Read-only Grok-home disk usage |
| `grok models` | Read-only account/model discovery, may use network |
| `grok completions <shell>` | Prints completion script unless redirected |
| `grok export` | May write or expose session transcript data |
| `grok trace --local ...` | Local trace export; writes potentially sensitive data |
| `grok trace ...` without local-only intent | Can upload trace data |
| `grok leader list/info` | Read-only process inspection |
| `grok leader kill` | Terminates a shared process |

Use local-only trace export unless the user explicitly wants an upload. Review
trace contents before sharing. A diagnostic failure does not authorize
`grok doctor fix`, elevated privileges, broader access, update, or
configuration changes.

## Clone and repository access

`grok clone` uses Grok's lazy-clone integration, backed by platform-specific
filesystem mechanisms. It can access a remote repository, create local state,
and mount or coordinate helper processes. It is not equivalent to a read-only
URL lookup. Use it only when the user wants that repository materialized and
the destination and credentials are in scope.

## Top-level command risk map

| Family | Typical safe inspection | State-changing or sensitive operations |
|---|---|---|
| `agent` | Help and local capability design | Starts persistent local or network agent service |
| `clone` | Help | Network clone, mount, filesystem creation |
| `completions` | Emit to stdout | Redirecting writes shell configuration or files |
| `dashboard` | Open local view | Can expose session/tool data on screen |
| `doctor` | Diagnose | Fix modes can change configuration |
| `du` | Inspect disk usage | None in ordinary mode |
| `export` | Preview intended session and target | Writes or discloses transcript |
| `inspect` | Inspect effective context | None in ordinary mode |
| `leader` | List and inspect | Kill or persistent leader startup |
| `login` / `logout` | Help/status where supported | Credential creation or clearing |
| `mcp` | List and diagnose | Add/remove/enable/disable; server execution |
| `memory` | Inspect supported help | Clear stored memory |
| `models` | List available models | Network/account metadata access |
| `plugin` | List/details/validate | Install/update/trust/enable/uninstall/tag/push |
| `sessions` | List/search | Permanently delete session history |
| `setup` | JSON preview if current help guarantees it | Install managed configuration |
| `trace` | Explicit local export | Upload or sensitive local artifact creation |
| `update` | Version check | Binary/channel update |
| `version` | Inspect | None |
| `worktree` | List/show/database inspection | Remove/gc/detach/salvage/clean artifacts |
| `wrap` | Help | Executes the supplied command |

Always inspect nested help immediately before a state-changing subcommand. The
availability of a confirmation flag is not permission to proceed.

## Bundled documentation map

The tested installation ships dedicated chapters for:

1. Getting started and authentication.
2. Keyboard shortcuts and slash commands.
3. Configuration and theming.
4. MCP, skills, plugins, and hooks.
5. Models, rules, and memory.
6. Headless and ACP agent modes.
7. Subagents, sessions, sandbox, and plan mode.
8. Background tasks and terminal support.
9. Permissions and safety.
10. Dashboard, monitoring, status line, and configuration reference.
11. Lazy clone.

Read the relevant installed chapter rather than relying on this map for an
exact flag, schema, shortcut, file path, or precedence rule.
