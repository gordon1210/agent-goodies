# Agent mode and ACP

`grok agent` starts a long-lived coding-agent process. It is a transport and
protocol integration surface, not a synonym for delegation and not the same as
Grok's internal subagents. Use `grok -p` when one process invocation and a
terminal answer are sufficient.

This reference was checked against Grok Build 1.0.13. Inspect `grok agent
--help` and the chosen mode's help before constructing a launch command.

## Choose a transport

| Command | Transport and scope | Use when |
|---|---|---|
| `grok agent stdio` | JSON-RPC over the child process's stdin/stdout | One local IDE, SDK, harness, or host agent owns the subprocess |
| `grok agent serve` | Self-hosted WebSocket server | Trusted clients need reconnects or network-local access |
| `grok agent headless` | WebSocket relay connection | A deliberately configured remote workflow needs relay access |
| `grok agent leader` | Shared backend leader process | Multiple compatible clients intentionally share a backend |

Prefer stdio for a local integration. It has the smallest exposure surface and
a clear parent/child lifetime. `serve` is a server running on the user's
machine; it is not a hosted Grok sandbox.

## Put options in the right place

Agent-wide options belong after `agent` and before the transport. Transport
options belong after the transport:

```bash
grok agent --no-leader --model <discovered-model-id> stdio

grok agent --no-leader serve \
  --bind 127.0.0.1:2419 \
  --secret <strong-random-token>
```

Current agent-wide options include model, reasoning effort, always-approve,
reauthentication, agent profile, repeatable plugin directories, leader choice,
endpoint overrides, and debug logging. Do not pass an option merely because a
headless `-p` command accepts it; the surfaces differ.

Omit `--model` unless a discovered model is required. Omit `--always-approve`
for clients that can implement ACP permission callbacks. Never use `--reauth`,
endpoint overrides, or `--plugin-dir` as an incidental fix for startup.

## ACP lifecycle

ACP uses JSON-RPC 2.0. A normal client:

1. Starts or connects to the transport.
2. Sends `initialize` with its protocol version and capabilities.
3. Reads the returned agent capabilities, extensions, and `authMethods`.
4. If auth methods are advertised, sends `authenticate` with a selected
   noninteractive method before opening a session.
5. Creates a session with `session/new` or loads an existing supported session.
6. Sends a turn with `session/prompt`.
7. Consumes interleaved `session/update` notifications.
8. Responds to permission requests when the session is not always-approve.
9. Waits for the matching prompt response, then continues, cancels, or closes.

Do not assume the next line after a request is its response. Notifications and
other responses can interleave. Use unique request IDs, a response map, an
independent notification loop, bounded queues, and explicit cancellation and
process-exit handling. Keep stdout protocol-only for stdio; route logs and
diagnostics to stderr or a debug file.

### Authentication is part of startup

Do not confuse ACP `authenticate` with starting `grok login`. The initialize
response can advertise methods such as an existing cached token, an API key,
or an interactive `grok.com` flow, and may identify a default in
`_meta.defaultAuthMethodId`. A headless client should select only an advertised
noninteractive method, send `authenticate` with `_meta.headless: true`, and
fail clearly if only interactive login is usable. It must not open a browser or
collect credentials through its ordinary command stream.

Run `grok login` separately when the user intends to establish cached
credentials, or inject `XAI_API_KEY` through a deliberately controlled child
environment. Never log the key or authentication payload. Older compatible
agents can omit `authMethods`; clients may then proceed without this handshake.

Known `session/update` values in the tested version include:

- `agent_message_chunk`
- `agent_thought_chunk`
- `tool_call`
- `tool_call_update`
- `plan`

Treat the list as extensible. Render or record operational events, but do not
surface hidden reasoning as chain-of-thought. A client should correlate tool
updates by their IDs and preserve ordering within a session.

The bundled [ACP bridge client](acp-client.md) implements this state machine for
one local Grok process and one session. Use it when a host agent needs live
status, mid-turn steering, cancellation, or permission responses. Do not
reproduce the simplified TypeScript example from the installed Grok guide: it
reuses request IDs and assumes the next line is the matching response, which is
not safe once notifications and agent-to-client requests interleave.

## Negotiate; do not guess

The base protocol covers sessions, prompts, streamed messages, tool lifecycle,
plans, permissions, and cancellation. It does not define mid-turn user-message
injection. Grok also implements `x.ai/*` extensions for areas such as:

- Filesystem access
- Git status, diffs, staging, commit, and discard
- Worktree creation, application, removal, listing, and garbage collection
- Search and file indexing
- Terminals and process output
- Session fork, resume, rewind, compaction, and history
- Authentication, feedback, and telemetry

The extension set is non-exhaustive and changes with releases. Discover
advertised capabilities from the initialize response. Some Grok extensions are
implemented but not advertised individually. Do not send a speculative
side-effecting probe: attempt such a method only for the requested operation,
treat JSON-RPC `-32601` as unsupported, and preserve an explicit fallback.
An advertised or successfully probed method is a capability, not user
authorization—especially for write, discard, commit, worktree removal,
telemetry upload, and remote operations.

### Status, cancellation, and steering are different

- Derive status locally from `session/update`: active/idle state, plan, tool
  lifecycle, permissions, last activity, and the eventual prompt result. A
  status check should not consume model context.
- Cancel a running turn with the standard `session/cancel` notification. Wait
  for the original `session/prompt` response before sending another prompt.
- For a requested mid-turn direction change, Grok Build 1.0.13 implements the
  logical extension `x.ai/interject`; ACP custom methods place an underscore on
  the wire, so the client sends `_x.ai/interject` with `sessionId`, `text`, and
  an optional `interjectionId`. Grok queues it for a safe processing boundary.
- The tested initialize response does not advertise interjection separately.
  Treat the real steering request as the capability probe. If it returns
  `-32601`, keep the original turn running and let the caller explicitly choose
  between waiting or cancelling and starting a new prompt.

Use an ACP SDK that matches the client's language when practical. If building
the framing directly, test request multiplexing, malformed records, unknown
notifications, permission timeouts, cancellation, reconnects, and child
process death.

## Session creation and metadata

A minimal session creation request supplies an absolute working directory and
the MCP servers added by this client:

```json
{
  "cwd": "/absolute/project/path",
  "mcpServers": []
}
```

An empty `mcpServers` array means the client adds none for that session. It does
not prove that Grok's effective configuration has no MCP servers, plugins,
hooks, skills, or agent profile. Inspect the effective runtime separately.

The tested Grok extension accepts selected `_meta` fields on `session/new`:

| Field | Effect |
|---|---|
| `rules` | Append extra task rules |
| `systemPromptOverride` | Replace the normal system prompt |
| `agentProfile` | Select or provide an agent profile |
| `yoloMode` | Enable always-approve for that session |
| `autoMode` | Enable auto permission behavior unless always-approve supersedes it |

Some releases and SDK integrations also support session-scoped plugin
directories. Feature-detect them. A plugin directory is executable trusted
content, not merely prompt context.

Prefer appended `rules` over a system-prompt replacement so normal project
instructions remain active. Use absolute, canonical working directories and
ensure the user's intended project is the one Grok discovers.

## Permission design

Best order of preference:

1. Keep normal permissions and implement the client's permission callback.
2. Use a deny-by-default effective policy with explicit allowed operations.
3. Use always-approve only for a trusted, bounded execution environment whose
   filesystem, process, network, extensions, and external tools are separately
   constrained.

Always-approve can be set process-wide with `grok agent --always-approve ...`
or per session with `_meta.yoloMode: true`. Process-wide scope affects every
session served by that agent. Deny rules, hooks, administrative locks, and some
shell ask rules may still block calls; always-approve is neither unrestricted
root access nor a security sandbox.

Do not automatically approve a permission request just because it came over
ACP. Display enough information to identify the tool, exact command or target,
working directory, session, and consequence. Time out unanswered prompts and
fail closed for noninteractive clients.

Read [Permissions, sandbox, and trust](permissions-sandbox-trust.md) before
exposing tools through an agent server.

## `stdio`: preferred local integration

Start a dedicated process per trust boundary:

```bash
grok agent --no-leader stdio
```

The parent should:

- Spawn without a shell when possible and pass arguments as an array.
- Supply only the required environment; account for credentials and secrets
  inherited by child tools.
- Keep stderr separate from JSON-RPC stdout.
- Tie child lifetime to the parent and terminate it cleanly.
- Bound message size, pending requests, prompt duration, and queued updates.
- Use a separate process when sessions have different extension or permission
  trust.

Do not combine protocol stdout with banners, logging wrappers, or command
substitution.

## `serve`: self-hosted WebSocket server

The current default bind is loopback `127.0.0.1:2419`. Keep it on loopback
unless the user explicitly requests network exposure:

```bash
grok agent --no-leader serve \
  --bind 127.0.0.1:2419 \
  --secret <strong-random-token>
```

If `--secret` is omitted, Grok generates one at startup. Capture and transmit
it through a protected channel; do not place a real secret in repository
configuration, shell history, logs, or examples. `GROK_AGENT_SECRET` is also
supported, but environment inheritance and process inspection still matter.

For any non-loopback deployment, add an explicit threat model for transport
encryption, authentication, secret rotation, origin/proxy behavior, firewall,
client authorization, rate limits, logs, and the authority of tools reachable
from the working directory. A token alone does not make a coding-agent server
safe for the public internet.

## `headless`: relay connection

`grok agent headless` attaches through a WebSocket relay. It changes the
network and trust boundary: remote prompts can drive a local agent and its
tools. Use it only when remote operation is explicitly intended and the relay,
endpoint overrides, authentication, working directory, permissions, and
lifetime have been reviewed.

Do not swap endpoint or proxy URLs to work around an error. A custom endpoint
is a separate security and data-routing decision.

## `leader`: shared backend

Leader mode allows compatible clients to share one backend process. Sharing
can improve reuse, but it couples lifecycle and trust. Use a dedicated leader
socket per intended boundary, inspect existing leaders before connecting, and
do not kill one merely because it appears stale without confirming ownership
and clients.

Relevant behaviors in the tested version:

- `--leader` connects a transport to a shared leader; `--no-leader` forces a
  dedicated agent.
- A requested non-`off` sandbox profile refuses leader mode so tool execution
  stays in-process.
- Leader mode can stay alive after disconnect and can connect a relay eagerly
  or on demand, depending on its flags.

Prefer `--no-leader` for isolated tests, sensitive work, and clients whose
failure or permission boundary must not affect another session.

## Persistent collaboration patterns

ACP is useful for collaboration when the client owns a session state machine:

- **Pair navigator:** keep one read-only session, send the host's current diff
  or let Grok inspect it, and request one next step per turn.
- **Rubber duck:** keep one session, disable write-capable tools, and require
  exactly one diagnostic question until the user requests synthesis.
- **Interactive delegation:** stream tool requests, require explicit approval
  for scope changes, and show the final diff and validation events.
- **Consulting panel:** create separate fresh sessions for independent views;
  do not mix histories or let one consultant see another's answer first.

If the only desired persistence is conversational context, repeated
`grok -p --resume <id>` calls are simpler than operating an ACP server.
If the host must observe or redirect an already-running turn, use the bundled
[ACP bridge client](acp-client.md).

## Integration verification

Test at least:

- Initialize and capability negotiation.
- Advertised default authentication before session creation, explicit
  noninteractive selection, and rejection of interactive-only login.
- New session with the intended `cwd` and no unintended MCP servers.
- One prompt with streamed text and a tool call.
- Permission allow, deny, timeout, and client disconnect.
- Unknown extension and unknown update handling.
- Cancellation and agent process termination.
- Session load or resume if supported by the client.
- Concurrent requests or an explicit rejection of concurrency.
- Secret rejection and reconnect behavior for WebSocket mode.
- No protocol corruption from stderr, updates, or logging.

Capture protocol fixtures without credentials, prompt secrets, internal
reasoning, or private source content.
