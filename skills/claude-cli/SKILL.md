---
name: claude-cli
description: Use the installed Claude Code CLI through claude -p for a bounded second opinion, source review, consulting, or an exact-session follow-up. Includes a standard-library Python wrapper for stdin prompts, structured results, timeouts, and --resume UUID. Use when the user requests Claude or authorizes Claude as a collaborator. Not for the Claude web app, direct API calls, an Agent SDK, an app server, or multi-agent council orchestration.
license: MIT
compatibility: "Python 3.10+ and an installed, authenticated Claude Code CLI supporting the documented flags. No SDK or Python packages required."
metadata:
  version: "1.0.0"
  last-reviewed: "2026-09-09"
  validation: "Offline fixture and subprocess tests; native CLI smoke test required on the target installation."
---

# Claude CLI

Use the real installed `claude` executable, only through non-interactive `-p`.
Keep the delegated task bounded. The host remains responsible for verification.
For a discussion with Grok, Claude, and the host, use **agent-council** instead
of building another orchestration script.

## Before calling

Confirm that sending the selected material to Claude is authorized. An opinion
request does not authorize repository edits, shell execution, web access, MCP,
or nested delegation. Do not send credentials or unrelated conversation.

Resolve this skill's actual installed directory. Invoke its bundled
`scripts/ask_claude.py` by absolute path; do not assume a particular host's
skill installation layout. Run its `doctor` with the intended project `--cwd`
once per environment, and again after CLI or configuration changes:

```bash
python3 /path/to/claude-cli/scripts/ask_claude.py doctor --cwd /absolute/project
```

Inspect the reported version and help against
[the CLI contract](references/cli-contract.md). Missing advertised flags are
reported, not silently removed. Check that applicable managed policies and
remaining executable startup behavior are acceptable. The helper never logs
in, updates the CLI, edits persistent configuration, changes `HOME`, or extracts
OAuth credentials. Existing CLI authentication and billing configuration remain
in force; it does not convert a subscription to an API connection.

**Do not use `--bare` as an isolation shortcut:** the reviewed documentation
says it skips subscription credentials. The wrapper uses `--safe-mode` with
explicit tool/MCP restrictions instead. Managed policy still applies. If the
installed CLI rejects a control flag, stop; do not retry with fewer controls.

## Prepare the task packet

Include the objective, relevant facts or source excerpts, applicable repository
instructions, constraints, questions, and expected evidence. The wrapper's
safe-mode deliberately omits normal project customizations, so pass the relevant
rules explicitly. For an independent opinion, do not prime Claude with the
host's preferred answer unless comparison is the actual assignment.

Prefer a UTF-8 prompt file or `--stdin`, especially for diffs or long/private
material. The wrapper feeds Claude through stdin, keeping the prompt out of
Claude's argument list. `--prompt` is available for short non-sensitive input,
but that input is visible in the **wrapper's** argv and possibly shell history.

## Invoke the bundled wrapper

```bash
python3 /path/to/claude-cli/scripts/ask_claude.py ask \
  --cwd /absolute/project \
  --prompt-file /approved/work/claude-question.md \
  --out-dir /approved/work/claude-call-01
```

The output directory must be new. Without `--out-dir`, the helper creates and
retains a uniquely named temporary directory and prints its location. Stdout
contains normalized JSON with `text`, `session_id`, usage when reported, and
`artifact_dir`. Stderr contains operational diagnostics. `--text` prints only
the answer; `result.json` still retains metadata.

| Need | Wrapper option |
|---|---|
| Follow up on this exact conversation | `--resume <returned UUID>` |
| Read source with no shell or edits | `--tools read` enables only `Read,Glob,Grep` |
| Override the configured model/effort | `--model <verified name>`, `--effort <supported level>` |
| Bound CLI agent loops / wall-clock time | `--max-turns 4`, `--timeout 240` |
| Inspect argv without a model call | `--dry-run` |

Default `--tools none` is a **tool-free consultation**, not an OS sandbox.
Even the read profile is not a filesystem allowlist: do not promise that only
one named file can be read. No edit, shell, browser, web, MCP, or Agent tool is
enabled by this wrapper. For a task requiring those capabilities, stop at the
authority boundary; do not improvise broader arguments during consultation.

## Continue and verify

Read the returned `session_id`, then send just the follow-up needed for normal
one-to-one consultation, with `--resume` and the same `--cwd`. Use a new artifact
directory per call. Never use `--continue`, titles, guessed IDs, or another
agent's session. `--session-id` creates a session; it is not a resume substitute.
Serialize calls that target the same native session.

Accept an answer only when the process exits zero **and** a valid, nonempty,
successful terminal result is present. The helper rejects error results, turn
caps, permission denials, malformed JSON, and unexpected resume IDs. Retain
artifacts on failures; there is no automatic retry or permission escalation.
A timed-out invocation may have changed its native session. Inspect it before
resuming; fresh, independently authorized consultation is often safer.

Verify claims and any quoted source locations in the host environment. Do not
claim that Claude browsed, ran tests, or modified files based on its prose.
Report its conclusion, material dissent, session ID when useful, and what the
host actually verified. Usage fields are not subscription billing amounts.

See [CLI contract and boundaries](references/cli-contract.md),
[recipes](references/recipes.md), and [validation](references/validation.md).
