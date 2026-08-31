# Headless mode: `grok -p`

Use headless mode for a bounded request whose answer can return through stdout.
It is the default integration surface for delegation, consultation, review,
pair-agent turns, and rubber-duck conversations.

This reference was checked against Grok Build 1.0.13. Re-run `grok --help`
before relying on exact flags.

## Core behavior

```bash
grok --cwd /absolute/project/path \
  -p "Describe the task precisely" \
  --output-format json
```

- `-p` and `--single` are equivalent. The process handles one prompt and exits.
- `--prompt-file` and `--prompt-json` also start headless mode.
- Each invocation creates a fresh session unless `--resume` or `--continue` is
  used.
- Headless mode may still loop through several model and tool turns. “Single”
  means one user prompt, not one model call.
- The configured model is used when `--model` is omitted. Discover available
  choices with `grok models`; do not freeze a model name into automation.
- Project-root discovery walks upward from `--cwd` to a Git root. That root and
  the current directory affect instructions, configuration, skills, sessions,
  and title-based resume.

## Start from a read-only baseline

For a repository-only consultation that needs no shell, web, MCP, memory, or
nested agents, start with this POSIX shape:

```bash
GROK_MEMORY=0 grok --cwd /absolute/project/path \
  -p "<task packet>" \
  --output-format json \
  --tools "read_file,grep,list_dir" \
  --no-subagents \
  --disable-web-search \
  --permission-mode dontAsk \
  --deny "MCPTool" \
  --sandbox read-only \
  --no-auto-update
```

Adapt only what the task needs. Important limits of this baseline:

- The `read-only` sandbox protects ordinary project paths from writes but can
  still read broadly and permits Grok state and temporary-file writes.
- `--tools` is a built-in-tool allowlist, but always-on MCP meta-tools can
  remain available. The MCP deny rule and an inspection of effective MCP
  configuration are therefore separate controls.
- Configured plugins and hooks are executable code. Review `grok inspect
  --json` before trusting a checkout or extension set.
- On macOS, sandbox network restrictions are not equivalent to Linux network
  enforcement. `--disable-web-search` does not itself neutralize every child
  process or MCP server.

For source review that genuinely needs read-only shell commands such as
`git status` and `git diff`, add `run_terminal_cmd` to `--tools` while retaining
`dontAsk` and a non-write sandbox. Built-in recognized read-only commands can
run; other unmatched operations are denied rather than prompted. Review the
installed permissions guide because the recognized-command set can change.

## Prompt input

### Inline text

Use `-p` for short, non-sensitive packets:

```bash
grok -p "Return three concrete risks, each with file and evidence."
```

Inline prompts can be visible in shell history and process listings. Do not put
credentials or private payloads there.

### Prompt file

Use `--prompt-file /path/to/prompt.md` when a prepared prompt is large, must
preserve formatting, or should not appear in the process argument list. Create
such a file only in an authorized location, give it restrictive permissions
when sensitive, and retain or remove it according to the caller's data policy.

### JSON content blocks

Use `--prompt-json '<json>'` when a client needs supported structured content
blocks. Confirm the accepted shape in the installed guide or help before
generating it; do not assume an API payload and a CLI prompt payload are
interchangeable.

### Standard input

Headless mode does not consume piped stdin as the prompt. Do not rely on:

```bash
git diff | grok -p "Review this"
```

Instead, let a tightly constrained Grok shell tool read the diff, construct an
explicit prompt, or use a prepared prompt file. Avoid command substitution for
large or secret material because it copies the payload into the process
arguments and is subject to shell size and quoting rules.

### Prompt transformation

`--rules` appends task-specific rules to the normal prompt context.
`--system-prompt-override` replaces the system prompt and can bypass default or
discovered instruction behavior. Do not use an override for routine
collaboration. Use `--verbatim` only when exact prompt transmission is a tested
requirement.

## Output formats

| Format | Shape | Best use |
|---|---|---|
| `plain` | Final human-readable text | Direct terminal use |
| `json` | One terminal JSON object | Scripts needing final text, session ID, stop reason, and usage |
| `streaming-json` | xAI-native NDJSON events | Live progress, tool audit, and robust native integration |
| `streaming-messages-json` | Messages-style NDJSON | Existing consumers of that wire shape |

### Plain

Plain output is convenient but loses structured status and session metadata.
Do not scrape it for correctness-critical automation.

### JSON

On a completed model turn, the current envelope can include:

- `text`
- `stopReason`
- `sessionId`
- `requestId`
- `num_turns`
- `usage`
- `modelUsage`
- complete cost fields when the backend reports them

Fields may be omitted when no model call occurred or accounting is incomplete.
The absence of a cost field does not mean the call was free. Treat
`usage_is_incomplete` and `cost_is_partial` as explicit uncertainty, and do not
sum partial model rows into a fabricated total.

### Native streaming JSON

Consume one JSON object per line and dispatch on `type`. Known 1.0.13 events
include `text`, `thought`, `tool_call`, `tool_call_update`, `usage`, `plan`,
`available_commands`, `end`, and `error`. Additional events can appear. Ignore
unknown types safely, preserve ordering, and require the terminal `end` event
for a complete successful stream.

Do not display or persist `thought` events as chain-of-thought. Operational
clients normally need final text, tool calls, results, status, and usage—not
private reasoning traces.

### Messages-style streaming JSON

This stream emits a `system` initialization record, `assistant` and `user`
message records, then a terminal `result`. `--include-partial-messages` only
affects this format and adds raw streaming frames. Some init, usage, duration,
and cost fields are adapted or unavailable; read the installed fidelity notes
before treating them as billing or correlation truth. Per-line `uuid` values
are not stable message or session identifiers.

Use native `streaming-json` when Messages compatibility is not required.

## Structured answers

`--json-schema` constrains the model answer and implies JSON output:

```bash
grok --cwd /absolute/project/path \
  -p "Review the patch. Report only evidence-backed findings." \
  --json-schema '{"type":"object","required":["findings"],"properties":{"findings":{"type":"array","items":{"type":"object","required":["severity","path","reason"],"properties":{"severity":{"type":"string"},"path":{"type":"string"},"reason":{"type":"string"}}}}}}'
```

Treat the CLI result envelope separately from the schema-constrained payload.
Probe the installed version before fixing a parser to one field location. In
Messages-style streaming output the terminal result uses
`structured_output`; other formats may expose the constrained value through
their documented envelope. Handle structured-output retry failures explicitly
instead of parsing the final prose as if it necessarily matched.

Keep schemas small. Use them for data interchange, not to force a complex
reasoning process into dozens of fields.

## Sessions and multi-turn collaboration

### Fresh by default

Use a fresh session for an independent review, adversarial critique, or second
opinion. It reduces anchoring and prevents unrelated prior conversation from
silently shaping the result.

### Resume the returned ID

Capture `sessionId` from JSON output, then resume that exact ID:

```bash
grok --cwd /absolute/project/path \
  -p "Act as a rubber duck. Ask one diagnostic question." \
  --output-format json

grok --cwd /absolute/project/path \
  --resume <returned-session-id> \
  -p "Here is my answer: ..." \
  --output-format json
```

Use this for navigator/driver pairing, consulting follow-ups, and rubber-duck
dialogue. Store the ID as data, not as a guessed title.

### Do not confuse the flags

- `-r` or `--resume` resumes an existing ID or a resolvable title.
- `-c` or `--continue` resumes the most recent session for the current
  directory. It is race-prone when jobs run concurrently.
- `-s` or `--session-id` assigns a valid UUID to a new conversation. It does
  not resume an existing session.
- `--fork-session` with resume or continue creates a new conversation ID from
  the old context. Use it when branches must diverge without appending to the
  original.

Scripts should prefer exact returned IDs over titles or `-c`.

Resume normally restores conversation, not the filesystem state that existed
at the prior turn. `--restore-code` has special snapshot and remote-session
semantics; inspect current help before using it. Conversation rewind likewise
does not undo file changes.

## Turn limits, completion, and interruption

Use `--max-turns` to bound agentic loops. A turn cap is a resource and control
limit, not a quality guarantee. Inspect `stopReason` or the terminal stream
event to distinguish normal completion from maximum tokens, maximum turns,
refusal, cancellation, or runtime failure.

Current documented process exit codes are:

| Exit | Meaning |
|---|---|
| `0` | Prompt completed normally |
| `1` | Authentication, network, runtime, or other error |
| `130` | Interrupted by SIGINT |
| `143` | Terminated by SIGTERM |

On interruption, the session is saved through the last completed tool call,
but file modifications are not rolled back. Always inspect the worktree before
resuming or retrying.

## Worktrees in headless mode

Do not pass `--worktree` to `grok -p` and assume isolation. Grok Build 1.0.13's
live top-level help states that this flag does not create a worktree in
headless mode, even though some documentation examples still imply otherwise.

For isolated write delegation:

1. Let the host create a dedicated Git worktree by an ordinary, authorized
   workflow.
2. Resolve and inspect its absolute path and starting revision.
3. Pass that path through `--cwd`.
4. Give Grok named ownership and narrow permissions.
5. Review the resulting diff from the host process.
6. Keep cleanup a separate, explicitly authorized operation.

## Automation checklist

- Pin behavior to a tested Grok CLI version or feature-detect it.
- Use `--no-auto-update` for reproducible invocations.
- Keep structured stdout separate from stderr logs.
- Set a timeout in the host and handle exits 130 and 143.
- Use exact session IDs for continuation.
- Treat event types and optional usage fields as forward-compatible.
- Disable nested subagents unless their fan-out is intentional.
- Do not treat allow rules as a closed allowlist; combine `dontAsk`, narrow
  allows, deny rules, and a sandbox.
- Verify the worktree, not merely the final prose.
- Record what was sent to the remote model according to the user's privacy and
  retention requirements.
