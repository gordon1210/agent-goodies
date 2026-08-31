# ACP bridge client

Use the bundled `scripts/grok_acp.py` when a host agent needs to keep one Grok
ACP session alive and control an active turn. The helper uses only the Python
3.9 standard library. It spawns a dedicated `grok agent --no-leader stdio`
child without a shell, keeps Grok's stderr separate, and exposes a small JSONL
control surface.

Prefer `grok -p` when no mid-turn control or live permission loop is needed.
The bridge is deliberately not a general ACP SDK, WebSocket server, daemon, or
multi-session manager.

## Start the bridge

Resolve the helper relative to this skill's `SKILL.md`, then start it through a
host facility that keeps the process alive and permits later writes to stdin:

```bash
python3 "<grok-cli-skill-directory>/scripts/grok_acp.py" \
  --cwd /absolute/project/path
```

Keep stdin open. Closing it is a shutdown request. Consume stdout continuously
so neither the bridge nor Grok is backpressured. Each stdout line is one JSON
event; startup diagnostics from Grok remain on stderr.

Useful launch options:

| Option | Meaning |
|---|---|
| `--session-id <id>` | Load one exact existing ACP session before accepting commands |
| `--auth-method <id>` | Select an advertised noninteractive auth method instead of Grok's advertised default |
| `--control-file auto` | Add an owner-only file channel for background hosts that cannot write stdin |
| `--control-file <absolute-path>` | Create the control file at an explicit, currently unused path |
| `--model <id>` | Pass an explicitly selected discovered model to `grok agent` |
| `--reasoning-effort <value>` | Pass an installed-version-supported effort |
| `--agent-profile <path>` | Explicitly load one trusted, reviewed agent profile file |
| `--sandbox <profile>` | Set `GROK_SANDBOX` for the child to a built-in or existing custom profile |
| `--permission-timeout <seconds>` | Fail an unanswered permission request closed; default 120 |
| `--startup-timeout <seconds>` | Bound initialization and session open; default 30 |
| `--shutdown-timeout <seconds>` | Bound close, terminate, and child reap; default 8 |
| `--always-approve` | Explicitly give every session in this process broad tool approval |

The helper supplies an empty client-requested MCP server list and advertises no
client-owned filesystem or terminal capability. That means the bridge adds no
session MCP server; it does **not** suppress MCP servers, plugins, hooks,
skills, memory, or a default agent profile already enabled by Grok's effective
configuration. The helper does not pass plugin directories, endpoint
overrides, reauthentication flags, or remote transports. `--agent-profile` is
the one deliberate profile override and should point only to reviewed content.

This does not disable Grok's runtime-owned shell, edit, web, or other configured
tools. Permission callbacks cover only requests Grok actually sends to the
client; they are not a sandbox or closed allowlist. Inspect the effective Grok
configuration and establish filesystem, process, network, and tool boundaries
before sending a prompt.

The child otherwise inherits the caller's environment, including credentials
and ambient tool authority. The helper defaults `GROK_DISABLE_AUTOUPDATER=1`
only when the caller has not already set it; it does not mutate persistent Grok
configuration.

`--sandbox` sets the documented `GROK_SANDBOX` child environment variable. The
`ready` and `status` events report the requested launch configuration, but that
report is not proof that the operating system enforced the profile. Read
Grok's startup diagnostics and test representative denied operations. If the
caller already exports `GROK_SANDBOX` and omits the option, the child inherits
that value. A null bridge value also does not prove that Grok's effective
configuration selected no sandbox.

The tested `grok agent` command does not expose headless `--tools`,
`--disallowed-tools`, `--no-subagents`, or `--permission-mode` launch flags.
The bridge cannot manufacture those controls. For a strict read-only
consultation, prefer the constrained `grok -p` baseline in
[Headless mode](headless.md). Use the bridge only after auditing the effective
agent configuration/profile and the runtime tools it can reach.

## Authentication

After `initialize`, the bridge reads `authMethods` and
`_meta.defaultAuthMethodId`. When methods are advertised it sends ACP
`authenticate` with the selected method and `_meta: {"headless": true}` before
creating or loading a session. The selected ID is reported as `authMethodId`;
credentials are never copied into bridge events.

By default only Grok's advertised default is used. `--auth-method` can select a
different advertised method, but the bridge rejects terminal or interactive
methods such as `grok.com`; it never opens a browser, launches `grok login`, or
asks for a secret over JSONL. Establish cached credentials with `grok login` or
provide `XAI_API_KEY` outside the bridge, then restart it. Agents that advertise
no auth methods remain compatible and skip this step.

Loading a session can emit replay events before `ready`, as required by
`session/load`. Do not send a command until the `ready` event supplies the
effective `sessionId`.

Abridged startup shape; additional fields and the command-line envelope are
omitted here:

```json
{
  "event": "ready",
  "sessionId": "<persist this exact ID>",
  "authMethodId": "cached_token",
  "controlFile": "<path or null>",
  "launchConfiguration": {
    "sandbox": "read-only",
    "sandboxSource": "cli",
    "agentProfile": null,
    "alwaysApprove": false
  }
}
```

Read the requested sandbox from `launchConfiguration.sandbox`; there is no
top-level `ready.sandbox` field. The auth method ID varies by environment.

## Background hosts without writable stdin

Some hosts can keep a Bash process in the background and read its output but
cannot later write to that process's stdin. Start the same bridge with an
additional control channel:

```bash
python3 "<grok-cli-skill-directory>/scripts/grok_acp.py" \
  --cwd /absolute/project/path \
  --control-file auto
```

In this mode, stdin EOF does not close the bridge. Read `controlFile` from the
`ready` event, then send each command from a separate process:

```bash
python3 "<grok-cli-skill-directory>/scripts/grok_acp.py" send \
  --control-file /absolute/path/from/ready \
  --json '{"id":"status-1","op":"status"}'
```

The short sender result only confirms that the command was appended. Read the
correlated `status`, `steer_queued`, `turn_completed`, or other result from the
original bridge's stdout.

The bridge creates the file exclusively, writes a versioned marker, restricts
it to the current user on POSIX, and removes only that same inode on clean
shutdown. The sender rejects symlinks, replacement files, permissive POSIX
modes, wrong owners, PIDs no longer running, and unmarked regular files. An
abrupt process kill can leave the owner-only file, including queued prompt
text, behind; treat the emitted path as sensitive task state. JSON passed with
`--json` can also be briefly visible in the sender process arguments, so never
put credentials in a command.

## Send commands

Write one JSON object plus a newline for each command. An `id` is recommended
for correlation; the bridge generates one when omitted.

### Start a turn

```json
{"id":"turn-1","op":"prompt","text":"Inspect the failing test and report the most likely cause. Do not edit."}
```

Wait for `prompt_accepted`, observe streamed events, and treat
`turn_completed` or `turn_failed` as terminal for that prompt. The bridge
rejects a second `prompt` while one is active.

### Read status without disturbing Grok

```json
{"id":"status-1","op":"status"}
```

`status` is computed locally. It does not send a prompt or extension request to
Grok. The snapshot includes phase, active turn, last activity, plan, bounded
tool summaries, usage when reported, pending permissions, learned interjection
support, selected auth method, and requested launch configuration.
The operational phase is `status.status.phase`, not a top-level `status.phase`:

```json
{"event":"status","commandId":"status-1","status":{"phase":"running","sessionId":"<id>","turn":{"commandId":"turn-1"}}}
```

### Steer the active turn

```json
{"id":"steer-1","op":"steer","text":"Stop considering a rewrite. Only verify whether the existing cache key can collide."}
```

`steer_sent` means the bridge sent the request. `steer_queued` means Grok
acknowledged `_x.ai/interject` and will apply it at a safe boundary. It is not a
claim that the model has already acted on the message.

If the installed version returns method-not-found, the bridge emits
`steer_unsupported` and does not silently change the turn. Either wait for the
turn or explicitly cancel it, wait for its terminal event, and send a new
prompt.

### Cancel the active turn

```json
{"id":"cancel-1","op":"cancel"}
```

The bridge sends standard `session/cancel` and answers all pending permission
requests with `cancelled`. `cancel_sent` is only acknowledgement of the local
command. Wait for the original `turn_completed` with stop reason `cancelled`
or for `turn_failed` before submitting another prompt. Cancellation does not
roll back tool side effects or filesystem changes.

### Resolve a permission

When Grok sends `session/request_permission`, the bridge emits a
`permission_required` event containing its exact `requestId`, tool call, valid
options, and timeout. Select only an advertised option:

```json
{"id":"permission-1","op":"permission","requestId":17,"optionId":"allow-once"}
```

Or fail it closed:

```json
{"id":"permission-1","op":"permission","requestId":17,"cancelled":true}
```

The bridge never invents an option and never auto-allows. Invalid choices leave
the request pending. A permission request whose `sessionId` is absent or does
not equal the bridge's one active session is immediately answered
`cancelled`. Timeout, turn cancellation, turn completion, and client shutdown
also answer unresolved permissions with `cancelled` when the connection is
still available. Permission IDs may be strings or integers; copy the value
without converting it.

### Close

```json
{"id":"quit-1","op":"quit"}
```

EOF, SIGINT, and SIGTERM also initiate shutdown. The helper cancels live work,
uses `session/close` when advertised, closes stdin, bounds graceful waiting,
then terminates only the dedicated child it created if necessary. It does not
delete the persisted Grok session or undo changes.

## Event contract

All events include `event`; the command-line sink also adds `v`, monotonic
`seq`, and UTC `timestamp` fields. Important events are:

| Event | Meaning |
|---|---|
| `ready` | Initialization, required noninteractive authentication, and session create/load completed |
| `message` | User or agent message chunk; replay is marked |
| `activity` | Reasoning activity occurred; content is deliberately omitted |
| `plan` | Latest reported plan |
| `tool_call`, `tool_call_update` | Correlated tool lifecycle data |
| `permission_required` | A live agent-to-client request needs a decision |
| `status` | Local state snapshot requested by the caller |
| `turn_completed`, `turn_failed` | Terminal event for one prompt request |
| `steer_queued`, `steer_unsupported` | Grok accepted or rejected interjection support |
| `protocol_warning` | Forward-compatible anomaly that did not corrupt framing |
| `agent_exit`, `fatal`, `closed` | Process or bridge lifecycle |

Thought chunks are converted to content-free `activity` events. Reasoning-like
fields on unknown or extension events are redacted, including payload fields
on tools whose known kind is `think`. Ordinary tool inputs and outputs,
prompts, messages, Grok stderr, and permission data can still contain sensitive
project content; do not persist the stream unless retention is intended.

## Failure behavior

- Invalid input produces `command_error` without killing a healthy session.
- Invalid UTF-8, malformed JSON-RPC, protocol-version mismatch, unusable or
  interactive-only advertised authentication, oversized ACP records, startup
  timeouts, and unexpected child exit fail the bridge.
- Unknown notifications and update variants remain observable. Unknown
  agent-to-client requests receive method-not-found because the bridge did not
  advertise support for them.
- Outgoing request IDs are unique and responses are correlated independently
  of interleaved updates and agent requests.
- Prompt text, command records, ACP records, pending requests, tracked tools,
  and collected final text are bounded by configurable limits.

Exit status is zero after normal EOF or `quit`, nonzero after startup/protocol
failure, and `128 + signal` after SIGINT or SIGTERM.
