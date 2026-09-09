# Provider contracts

Reviewed **2026-09-09**. The Grok adapter is based on the repository's existing
Grok Build 1.0.13 headless contract and current official documentation. Native
Grok and Claude executables were not exercised against authenticated accounts
while building this distribution. CLI compatibility must be smoke-tested on
the target installation; fixture versions are not production version claims.

## Claude

Only the installed `claude -p` executable is used. Prompts go through stdin.
JSON completion uses `type`, `subtype`, `is_error`, `result`, and `session_id`;
internal-turn limits and incomplete results do not count as contributions.
Exact resumes require a canonical UUID matching the result's session ID.

The adapter reuses the same portable transport/profile as **claude-cli**:
ordinary `-p`, `--safe-mode`, an empty built-in tool set, `dontAsk`, empty strict
MCP configuration, a deny rule for MCP tools, disabled skills/browser, and a
per-invocation hooks-disable setting. It does **not** use `--bare`, which the
reviewed documentation says omits subscription credentials. Safe-mode deliberately
skips ordinary project instructions; the host supplies applicable rules explicitly.

Managed policy can retain executable hooks or other startup behavior. These
controls are not an OS sandbox and are not authority to bypass organizational
policy. Check the effective environment before using the council on sensitive
material. Existing authentication/provider settings still determine access and
billing. No token extraction, proxy, API key setup, or environment credential
substitution is implemented.

## Grok

Grok receives `--prompt-file`, which starts headless execution. **Do not pipe the
prompt into `grok -p`:** the repository's tested headless contract says it does
not consume that stdin as the prompt. A prompt file also avoids argv size limits
and exposing the full discussion in a process listing.

The actual argument list includes:

```text
grok --cwd <project> --prompt-file <owned-prompt-file>
  --output-format json --tools ''
  --no-subagents --disable-web-search
  --permission-mode dontAsk --deny MCPTool
  --sandbox read-only --max-turns 4 --no-auto-update
```

Invocation-local documented environment variables disable cross-session memory,
subagents, web fetch, writes, MCP tool discovery, and LSP tools, and suppress
Grok's auto-updater. They do not alter credentials, `HOME`, `GROK_HOME`, or
persistent configuration. They do not claim to disable every startup extension.

The accepted final envelope has nonempty `text`, a canonical `sessionId`, and
`stopReason: end_turn`. Other stop reasons, missing fields, invalid JSON, and
nonzero exits pause the run. Optional usage and incomplete-accounting indicators
remain metadata; they are not coerced into a fabricated cost total.

`--tools ''` removes built-in model tools, not necessarily every MCP meta-tool
or executable plugin/hook surface. The explicit MCP deny rule and config review
are separate requirements. `doctor` runs `grok inspect --json` for that review.
Do not blindly add a made-up universal `GROK_DISABLE_HOOKS` switch; the skill
makes no unsupported claim that such a switch closes all extension paths.

## Sandbox failures

Default Grok profile: `read-only`; `strict` may be selected explicitly at init.
A requested sandbox is intent, not proof the OS applied it. Review startup
warnings and stop on failed or degraded enforcement; do not accept a successful
answer as proof of confinement. The runner never retries by dropping a sandbox.
It preserves stderr and process status, but cannot universally interpret every
new platform-specific sandbox warning; the host must review material diagnostics.

The existing Grok skill records a macOS/Docker Desktop runtime-socket startup
incompatibility in 1.0.13. Never alter Docker sockets, filesystem ownership,
user configuration, or trust to make the council start.

An **explicit new** council may use `--grok-sandbox off` only when the entire task
is prompt-supplied, tools remain empty, and every relevant executable extension
has been disabled or reviewed as compatible with the tool-free boundary. This
is an **unsandboxed, tool-free consultation**, not filesystem read-only. Keep
the failed run separate; do not mutate its configuration or reuse its session
with a weaker sandbox. Otherwise stop and report the incompatibility.

## Drift and authority

The doctor records versions/help; its `ready` flag means metadata probes ran,
not that a model call or sandbox was verified. Missing help entries are reported
because some documented flags are hidden. Any unsupported argument fails the
actual call, without a fallback to a less-restricted command.

Do not hard-code a newer version number as tested, guess model IDs, or claim
fixture tests validated native auth/permissions. Where the existing grok-cli
skill imposes a stricter installed/stable/tested-version gate, honor that gate
when using it. Refresh behavior deliberately rather than adding silent legacy
fallbacks here.

## Sources

- Existing Grok skill, inspected at repository revision `e1f48462632e91f05f0e302ef7d3e9c16979ecee`: https://github.com/gordon1210/agent-goodies/tree/main/skills/grok-cli
- Existing headless contract: https://github.com/gordon1210/agent-goodies/blob/main/skills/grok-cli/references/headless.md
- xAI/SpaceXAI CLI reference: https://docs.x.ai/build/cli/reference
- Headless/scripting: https://docs.x.ai/build/cli/headless-scripting
- Sessions: https://docs.x.ai/build/features/sessions
- Environment/settings: https://docs.x.ai/build/settings/reference
- Hooks: https://docs.x.ai/build/features/hooks
- Claude CLI reference: https://code.claude.com/docs/en/cli-reference
- Claude headless usage: https://code.claude.com/docs/en/headless
- Claude hooks and managed-policy limits: https://code.claude.com/docs/en/hooks
