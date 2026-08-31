---
name: grok-cli
description: Operate and orchestrate the xAI Grok Build CLI as a bounded coding collaborator. Use when invoking `grok`, especially `grok -p` for headless prompts, `grok agent` for ACP integrations, exact session continuation, delegated implementation or review, agent pairing, consulting, rubber-duck dialogue, structured output, or CLI configuration and diagnostics. Do not use for the Grok web app or direct xAI API integration unless Grok Build CLI behavior is involved.
license: MIT
metadata:
  version: "1.0.1"
  last-reviewed: "2026-08-31"
  tested-cli-version: "1.0.13"
  compatibility: "Grok Build CLI; verify commands against the installed version because the CLI and documentation evolve quickly."
---

# Grok CLI

Use the installed Grok Build CLI as a deliberately scoped collaborator. Choose
the smallest mode that fits the interaction, give Grok a complete task packet,
and independently verify its result before accepting it.

## Resolve version drift first

For every new environment, establish the live contract before relying on a
flag or output field:

```bash
command -v grok
grok version --json
grok --help
grok inspect --json
```

Run `grok <command> --help` for every subcommand used. If present, the bundled
guide under `~/.grok/docs/user-guide/` is normally closer to the installed
binary than the website. Apply sources in this order:

1. The installed binary's version and command help.
2. The guide bundled with that installation.
3. Current official documentation, changelog, and source.
4. This skill's tested patterns.

Do not hard-code a current model ID or copy an old example flag without this
check. In particular, do not pass speculative prompt flags such as
`--best-of-n`, `--check`, or `--self-verify` to `grok -p` unless its current
help advertises them. A similarly named flag can have a separate valid meaning;
for example, the tested `grok update --check` only checks for an update.

Do not install or update Grok, start an interactive login, sign out, fetch
managed setup, or mutate configuration merely to complete a consulting call.
Those are separate user-authorized operations. An ACP client still has to send
the protocol's `authenticate` request when Grok advertises an existing cached
or environment-backed method; that selects already available credentials and
is distinct from initiating `grok login`.

## Choose the operating mode

| Need | Mode | Why |
|---|---|---|
| Human-led interactive work | `grok [PROMPT]` | Full TUI, approvals, slash commands, and direct supervision |
| One bounded task or a scripted follow-up | `grok -p ...` | Starts, returns an answer, and exits; easiest delegation primitive |
| A persistent local client integration | `grok agent stdio` | Long-lived bidirectional ACP over JSON-RPC stdio |
| A local WebSocket service | `grok agent serve` | Persistent ACP server for one or more trusted clients |
| A remote relay connection | `grok agent headless` | Connects the agent through a Grok WebSocket relay |
| Shared backend process | `grok agent leader` | Coordinates compatible clients through a leader process |
| Grok itself needs child workers | Grok subagents | Child sessions inside one Grok session, distinct from `grok agent` |

Prefer `grok -p` for delegation, review, pair-agent turns, consulting, and
rubber-duck work. Choose `grok agent` only when a client needs a long-lived,
bidirectional protocol, streamed tool lifecycle, permission callbacks, or
mid-turn control. For status, steering, cancellation, and permissions from a
host agent, use the bundled stdlib-only JSONL bridge instead of hand-writing
JSON-RPC. Read
[Headless mode](references/headless.md) or
[Agent mode and ACP](references/agent-acp.md) before invoking the selected mode;
read [ACP bridge client](references/acp-client.md) before using the helper.

## Establish the authority envelope

Default to advisory, read-only access. A request to ask Grok for an opinion is
not authority for Grok to edit files, run write-capable commands, contact
external systems through MCP, or fan out into its own subagents.

Before a call, determine:

- The exact working directory and project root.
- Which repository and user instructions Grok will discover there.
- Whether Grok may only read, may edit named paths, or may run named validation
  commands.
- Whether web, MCP, plugins, hooks, memory, or nested subagents are needed.
- Which existing worktree changes belong to the user or another agent.
- The expected output, evidence, turn limit, and stop conditions.

For write delegation, give Grok exclusive ownership of explicit files or a
dedicated host-created worktree. Never assume `grok -p --worktree` provides
isolation: in Grok Build 1.0.13, current `grok --help` explicitly says headless
mode does not create a worktree from that flag. Create and inspect the
worktree outside Grok, then pass its absolute path with `--cwd`. Do not delete
or clean it automatically afterward.

Read [Permissions, sandbox, and trust](references/permissions-sandbox-trust.md)
before granting edits, shell access, web access, MCP tools, plugins, or
always-approve.

## Build a complete task packet

Give Grok only the context required for the assignment, organized as:

```text
Role: <consultant, reviewer, navigator, driver, implementer, rubber duck>
Objective: <one concrete outcome>
Working directory: <absolute path and relevant project root>
Scope: <owned files, symbols, diff, or questions>
Known facts: <evidence already established>
Constraints: <repo rules, compatibility, safety, no-go actions>
Allowed actions: <read, edit paths, exact commands, web/MCP if needed>
Deliverable: <format, detail, schema, or patch expectations>
Validation: <evidence and commands required>
Stop conditions: <ambiguity, destructive action, scope expansion, turn cap>
```

Do not paste an entire host-agent transcript when a concise packet is enough.
Do not include credentials, unrelated private files, or hidden reasoning. For
an independent second opinion, ask Grok before revealing the host agent's
conclusion; compare evidence afterward instead of deciding by vote.

Use the ready-made packets and command shapes in
[Collaboration patterns](references/collaboration-patterns.md).

## Run and evaluate the call

1. Inspect the current worktree and effective Grok configuration without
   changing either.
2. Select the least-capable tool set, permission mode, sandbox, and extension
   set that can complete the task. Headless `grok -p` exposes the strongest
   per-invocation controls. The tested `grok agent` surface does not expose the
   same `--tools`, `--no-subagents`, or permission-mode flags, so use an audited
   effective configuration or agent profile there; choose `grok -p` when a
   strict per-call read-only boundary is required.
3. Treat sandbox application as a startup result, not as intent expressed by a
   flag. If a requested sandbox warns, fails, or exits before the model turn,
   never retry automatically without it. A fresh, explicit `--sandbox off`
   tool-free consultation is allowed only when the complete bounded input is
   supplied in the prompt and effective hooks, plugins, MCP, web, memory,
   permissions, configuration, and subagents have been disabled or
   independently reviewed. If Grok needs any local tool capability, or an
   executable extension cannot be proven inactive or non-mutating, stop until
   the intended sandbox can be enforced.
4. Use a fresh session for independent review. Resume the exact returned
   session ID for pairing or rubber-duck continuity.
5. Capture stderr separately from structured stdout when automating.
6. Check the process exit code, terminal event or result object, stop reason,
   incomplete-usage markers, and requested deliverable.
7. Verify factual claims, diffs, and test results in the host environment.
8. Treat Grok's answer as advisory until that verification passes.

An exit code of zero means the prompt completed, not that the proposed change
is correct. An interrupted run does not roll back file changes.

## Load the relevant reference

| Task | Reference |
|---|---|
| `-p`, prompt inputs, output formats, JSON/NDJSON, sessions, automation | [headless.md](references/headless.md) |
| ACP lifecycle, stdio, WebSocket server, relay, leader, client design | [agent-acp.md](references/agent-acp.md) |
| Bundled ACP bridge, JSONL commands/events, status, steering, cancellation, permissions | [acp-client.md](references/acp-client.md) |
| Delegation, pairing, consulting, rubber duck, review, parallel work | [collaboration-patterns.md](references/collaboration-patterns.md) |
| Permissions, tools, sandbox, secrets, hooks, MCP, plugins, trust | [permissions-sandbox-trust.md](references/permissions-sandbox-trust.md) |
| TUI, sessions, agents, rules, memory, configuration, operational commands | [cli-areas.md](references/cli-areas.md) |
| Source hierarchy, official links, version notes, maintenance | [sources.md](references/sources.md) |

## Report the outcome

State the mode, working directory, authority granted, session ID when useful,
Grok's conclusion or changes, host-side verification performed, and any
unresolved uncertainty. Do not claim that Grok used a tool, passed a check, or
made no edits unless the captured events, diff, or local verification support
that claim. If a tool-free call follows a failed sandbox start, report the two
attempts separately: the requested sandbox and its startup failure; whether the
later call explicitly used `--sandbox off`; that it was tool-free rather than
filesystem-read-only; which extension surfaces were inspected or disabled;
and whether a model turn occurred and which session ID belongs to it. Attribute
conclusions and usage or cost only to the output that actually contains them;
do not assign a conclusion, session ID, tool audit, usage, or cost to the
failed start unless its captured output contains that field.
