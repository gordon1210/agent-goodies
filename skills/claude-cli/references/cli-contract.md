# CLI contract and boundaries

Reviewed against official documentation on **2026-09-09**. No native installed
Claude Code version was live-tested while producing this skill. The tests use
explicitly labeled fixtures. Do not interpret the review date as a version pin.

## Transport

The wrapper invokes a subprocess with an argument list and `shell=False`. It
passes UTF-8 input via stdin and captures the final JSON object and stderr in
separate files. It neither imports an SDK nor speaks an API, ACP, or app-server
protocol. Authentication is handled by the installed official CLI.

Normal invocation controls:

```text
claude -p --output-format json
  --safe-mode
  --tools ""
  --permission-mode dontAsk
  --strict-mcp-config --mcp-config '{"mcpServers":{}}'
  --disallowedTools 'mcp__*'
  --disable-slash-commands --no-chrome
  --settings '{"disableAllHooks":true}'
  --max-turns 4
```

The read profile replaces the empty built-in tool set with `Read,Glob,Grep` and
preapproves those same tools. It does not enable Bash, edits, web, or subagents.
The wrapper supplies `--resume` only for an explicit canonical UUID.

`--safe-mode` disables ordinary customizations while preserving the normal
authentication path. It is not `--bare`: the latter does not read subscription
OAuth credentials. Managed hooks and other applicable policy can survive local
controls. Never remove required organizational controls or rebind home/config
paths to evade them. Inspect the target installation and stop if its remaining
startup behavior violates the agreed envelope. The helper does not guarantee
that native CLI telemetry, credential helpers, internal state persistence, or
managed startup code cannot run.

Model access and billing follow existing environment/configuration. In
particular, an already configured API key/provider may affect billing. The
helper neither removes it nor silently substitutes subscription credentials.
Do not use CLI usage estimates as an invoice or as proof of a free call.

## Result handling

The accepted envelope is one object with `type: result`, `subtype: success`,
`is_error: false`, nonempty `result`, and a canonical UUID `session_id`. Known
incomplete stop reasons and permission-denial records are rejected. Unknown
optional usage fields are not needed for correctness. An array, NDJSON stream,
plain text, banner-prefixed JSON, or schema-shaped answer is not accepted as a
terminal result. This wrapper intentionally does not request `--json-schema`.

If a newer CLI changes its output contract, update the parser and fixtures
from actual documentation/captured output. Never add broad regex extraction or
coerce an error response into a successful answer.

## Operational limits

Input cap: 2 MiB of UTF-8. Captured stdout/stderr cap: 8 MiB each, monitored at
50 ms intervals, so a fast burst may briefly overshoot on disk. No truncation
is presented as a complete answer. Output files remain available for diagnosis.

On POSIX systems, timeout/interruption terminates the process group created by
this helper. Native Windows terminates the owned CLI process; this is **not** a
Windows process-tree or filesystem sandbox. Use native `.exe` installations;
`.bat` and `.cmd` shims are deliberately rejected rather than invoking a shell.
Only Linux fixture/process tests have been executed for this bundle.

Files the helper creates are mode 0600 and directories mode 0700 on POSIX.
These are not portable Windows ACL guarantees or encryption. Native CLI session
files follow Claude's own policy. Retained prompt/output artifacts may be
sensitive; do not commit or upload them without reviewing them. Cleanup remains
an explicit caller operation. Only helper-owned transient write/probe files are
removed automatically.

## Sources

- Anthropic, CLI reference: https://code.claude.com/docs/en/cli-reference
- Anthropic, programmatic/headless usage, including stdin, bare mode and result output: https://code.claude.com/docs/en/headless
- Anthropic, exact session continuation: https://code.claude.com/docs/en/sessions
- Anthropic, settings precedence: https://code.claude.com/docs/en/settings
- Anthropic, managed-hook boundary: https://code.claude.com/docs/en/hooks

Use the installed executable/help and current official documentation together.
Help omits some official flags, so a missing help entry is diagnostic rather
than proof a flag is invalid. A rejected flag still stops the actual call.
