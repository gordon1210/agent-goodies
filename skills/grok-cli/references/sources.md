# Sources and maintenance

Grok Build changes quickly. This skill records durable operating patterns for
the current stable release and routes exact version behavior to one small note.
Older CLI releases are intentionally unsupported.

## Review record

Last full review: 2026-08-31.

Focused follow-up: 2026-09-04. Rechecked built-in shell and subagent tool IDs,
`--tools` filtering, and `dontAsk` cancellation behavior against the installed
1.0.13 guide and binary plus concrete headless feedback. No paid model call was
made during the follow-up.

Tested installation:

```text
grok 1.0.13 (5e9a58528b76) [stable]
```

## Supported stable contract

- [Grok Build 1.0.13](versions/1.0.13.md) contains the few exact tool-filter,
  subagent, and cancellation details that differ from otherwise durable
  guidance.

Load only the note for the supported stable release. When stable changes,
refresh this skill and route to the new note; do not add compatibility branches
for older installations to the operational references.

The review covered:

- Top-level help and help for every advertised command.
- Nested help for `grok agent`, MCP, plugins and marketplaces, sessions,
  worktrees and their database commands, leader processes, memory, setup,
  tracing, updating, authentication, diagnostics, export, clone, and terminal
  wrapping.
- The complete 27-chapter guide bundled with the tested installation.
- Effective configuration shape from `grok inspect --json` without copying
  user-specific configuration into this skill.
- A metadata-only `grok agent stdio` initialize probe, without creating a
  session or sending a model prompt. It confirmed protocol version 1,
  `cached_token` and `grok.com` auth method IDs, and `cached_token` as the
  advertised default for the tested authenticated environment.
- Official online Grok Build documentation, changelog, and source repository.
- The Agent Client Protocol overview and protocol concepts.

No third-party wrapper or blog is authoritative for command behavior.

## Authority order

When sources disagree, use:

1. `grok version --json` and live `grok ... --help` from the executable that
   will run.
2. The guide shipped alongside that executable.
3. Official documentation and changelog current for that release.
4. A matching tag or revision in the official source repository.
5. This skill's examples and explanations.

Help establishes accepted syntax, but the guide may contain essential semantic
limits absent from help. Verify both for permissions, sandboxing, output
fidelity, sessions, hooks, plugins, MCP, and ACP.

The public source repository can move ahead of or behind a managed binary.
Match a release tag or build revision before treating source details as exact.

## Known drift observed during this review

### Headless worktrees

Some bundled and online tables describe `--worktree` generically as creating a
worktree. The tested live top-level help adds a decisive qualification:
headless `-p` does not create one from this flag. This skill therefore requires
a host-created worktree plus `--cwd` for isolated headless writes.

### Session identifiers

Historical examples can imply that `-s` resumes or upserts a conversation. The
tested CLI defines `--session-id` as a UUID for a new conversation and rejects
an existing ID. Resume with `-r` or `-c`; scripts should use the exact ID
returned in structured output.

### Flags and command inventory

The public CLI reference can list compatibility or transitional commands and
flags that the tested binary's primary help does not advertise, while the
binary may expose newer nested subcommands not yet summarized online. Do not
infer support from a web table. Examples include memory switches, import
surfaces, worktree behavior, and plugin or session subcommands.

### Models

Examples and defaults change as models are released or retired. Discover the
available list with `grok models` and avoid embedding a model ID unless the
caller is deliberately pinning it.

### ACP authentication

The simplified ACP example in the tested bundled agent-mode chapter proceeds
from `initialize` directly to session creation. Grok Build 1.0.13's live
initialize response advertises `authMethods` and a default method, while the
current official headless client source performs `authenticate` before
`session/new` or `session/load`. The base ACP authentication specification also
defines this negotiation. Robust clients must implement the live/official
handshake and treat the bundled example as illustrative framing, not a complete
startup sequence.

### Runtime-socket sandbox startup

Grok Build 1.0.13 (`5e9a58528b76`) on macOS arm64 failed closed before a model
turn when Docker Desktop exposed its documented
`/var/run/docker.sock -> ~/.docker/run/docker.sock` endpoint symlink. The exact
error class was `runtime-socket deny resolution failed`, followed by `endpoint
is a symlink`, and the process exited with status 1. Docker documents that
**Allow the default Docker socket to be used** creates this compatibility path
for third-party clients and targets the per-user socket; see Docker's
[Desktop settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/)
and its
[macOS permission requirements](https://docs.docker.com/desktop/setup/install/mac-permission-requirements/).

This mandatory runtime-socket path is narrower than the general bundled
platform statement that a failed built-in sandbox may warn and continue, and
it is absent from the general
[built-in-profile documentation](https://docs.x.ai/build/features/sandbox).
The stable update check on 2026-08-31 reported 1.0.13 as both current and
latest. Re-test the next stable Grok version with the endpoint symlink present.
Delete this version-specific caveat only after host-side evidence shows that
`--sandbox read-only` applies successfully and representative local read, shell,
and edit tools remain confined.

## Bundled guide

When installed in the standard location, read relevant files under
`~/.grok/docs/user-guide/`:

| Chapter | Area |
|---|---|
| `01-getting-started.md` | Installation, modes, tools, first sessions |
| `02-authentication.md` | OAuth, API key, device, OIDC, helper flows |
| `03-keyboard-shortcuts.md` | Terminal-dependent interaction |
| `04-slash-commands.md` | Interactive command catalog |
| `05-configuration.md` | Sources, precedence, compatibility, discovery |
| `06-theming.md` | TUI themes and rendering |
| `07-mcp-servers.md` | MCP transports, config, tools, diagnostics |
| `08-skills.md` | Skill discovery, precedence, invocation |
| `09-plugins.md` | Plugins, marketplaces, trust, packaging |
| `10-hooks.md` | Lifecycle hooks, decisions, failure behavior |
| `11-custom-models.md` | Model definitions and endpoints |
| `12-project-rules.md` | Project instructions and rules |
| `13-memory.md` | Cross-session memory and controls |
| `14-headless-mode.md` | `-p`, scripting, outputs, sessions, exits |
| `15-agent-mode.md` | ACP transports, lifecycle, extensions |
| `16-subagents.md` | Child agents, personas, isolation, inheritance |
| `17-sessions.md` | Persistence, resume, fork, rewind, export |
| `18-sandbox.md` | Built-in/custom profiles and platform limits |
| `19-plan-mode.md` | Planning workflow and edit gate |
| `20-background-tasks.md` | Processes, monitors, output control |
| `21-terminal-support.md` | Terminal, clipboard, image, shell behavior |
| `22-permissions-and-safety.md` | Modes, rule matching, approval pipeline |
| `23-dashboard.md` | Agent Dashboard |
| `24-monitoring-usage.md` | Usage and monitoring |
| `25-status-line.md` | Status-line configuration |
| `26-config-reference.md` | Full configuration schema |
| `27-grok-clone.md` | Lazy clone behavior and platform integration |

Do not assume every installation uses this path or contains the same chapter
set. Enumerate what is present.

## Official online sources

- [Grok Build overview](https://docs.x.ai/build/overview)
- [Modes and commands](https://docs.x.ai/build/modes-and-commands)
- [Headless and scripting](https://docs.x.ai/build/cli/headless-scripting)
- [CLI reference](https://docs.x.ai/build/cli/reference)
- [SpaceXAI documentation index for language models](https://docs.x.ai/llms.txt)
- [Official Grok Build source repository](https://github.com/xai-org/grok-build)
- [Grok Build interjection extension source](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-shell/src/extensions/interject.rs)
- [Grok Build headless ACP client source](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/src/headless.rs)
- [Grok Build changelog](https://x.ai/build/changelog)
- [Agent Client Protocol introduction](https://agentclientprotocol.com/get-started/introduction)
- [Agent Client Protocol authentication](https://agentclientprotocol.com/protocol/v1/authentication)
- [Agent Client Protocol prompt-turn specification](https://agentclientprotocol.com/protocol/prompt-turn)
- [Agent Client Protocol extensibility](https://agentclientprotocol.com/protocol/v1/extensibility)

Use official documentation for product claims and current behavior. Use the ACP
site for base protocol semantics; use Grok's installed guide and initialize
capabilities for `x.ai/*` extensions.

## Maintenance procedure

When updating this skill:

1. Compare `grok version --json` with `grok update --check --json`; continue
   only when installed and latest stable versions agree.
2. Diff top-level help and recursively inspect new or changed subcommands.
3. Enumerate and read every changed bundled-guide chapter.
4. Compare official online docs and the changelog.
5. Match source code to the tested binary before using implementation detail.
6. Re-check all command templates without making a paid model call or changing
   user state unless that test is explicitly authorized.
7. Re-test the high-risk claims:
   - Headless worktree behavior.
   - `-s`, `-r`, `-c`, fork, and restore semantics.
   - Permission precedence and `dontAsk` behavior.
   - Current `--tools` IDs for shell and subagent access, including the combined
     requirements for intentional nested fan-out.
   - Headless permission rejection behavior, including whether
     `permission_cancelled` terminates the prompt before a final deliverable.
   - Built-in sandbox paths and platform network enforcement.
   - Non-`off` sandbox startup when known container-runtime socket paths are
     real files, sockets, absent paths, and endpoint symlinks on each supported
     platform.
   - Sandbox failures neither enter a model turn nor silently retain requested
     local tools without enforcement.
   - The tool-free branch has an empty built-in tool set, no reachable MCP
     tools, nested subagents, or web tools, and no unreviewed executable hooks
     or plugins.
   - MCP retention under `--tools`.
   - Hook fail-open behavior.
   - ACP auth methods, default selection, headless authentication ordering, and
     interactive-only failure behavior.
   - Agent option placement and ACP session metadata.
   - Output event names, terminal records, cost uncertainty, and structured
     output location.
8. Replace the supported-stable version route and note. Keep operational
   references free of compatibility branches for older releases.
9. Update the frontmatter review date and tested version.
10. Validate the skill package and all repository catalogs.

Keep observed release-specific conflicts in the routed version note.
