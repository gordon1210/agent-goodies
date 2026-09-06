---
name: handoff
description: Maintain accurate repo-local continuity across agents and sessions. Use when a repository already contains HANDOFF.md or .handoff/, the user explicitly asks to create or update handoff state, work must survive an imminent agent/session transition, or a HANDOFF.md conflict needs regeneration. Do not bootstrap or write handoff files in a new repository without explicit user opt-in, and do not use for ordinary repository work that has no handoff state or continuity request.
---

# Handoff Skill

You maintain reliable repo-local continuity between agents, sessions, and humans.

This skill exists because multiple agents may work on the same repository over time. Your job is to keep the handoff state accurate, compact, and useful without polluting the main conversation.

## Source of truth

Use the repository root, not this skill folder, as the source of truth.

Expected repo-local files:

- `HANDOFF.md` — human-readable current state summary.
- `.handoff/` — append-only machine-readable event journal.

The skill folder may contain scripts/templates, but project state must stay in the repo.

## Read-only tasks

When the active task is read-only or an audit, inspect existing handoff state without changing it. Do not initialize, append, render, repair, stage, commit, or otherwise update handoff or generated process files unless the user separately authorizes those mutations. Report the update that would otherwise be useful in the main response. This rule overrides every write or completion instruction below.

Read [the protocol reference](references/HANDOFF_PROTOCOL.md) when bootstrapping a repository, repairing conflicts, or evaluating storage behavior.

## Preferred storage model

Prefer this structure:

```text
HANDOFF.md
.handoff/
  README.md
  config.json
  schema.json
  events/
    YYYY-MM/
      YYYYMMDDZ-<agent>-<type>-<branch>-<commit>.jsonl
  archive/
```

Design rules:

- `.handoff/events/**` is append-only.
- New events should append to a contextual JSONL batch keyed by UTC day + agent + type + branch + commit.
- Record the full branch name in each event. Encode it for the filename without collapsing distinct refs (`feature/foo` vs `feature-foo`). Short names stay fully encoded; names that would make the token longer than 50 characters use a stable prefix+hash form.
- For detached HEADs, use Git's worktree administrative name in place of the branch so detached worktrees at the same commit remain distinct.
- Existing one-event JSONL files remain valid and should be read without migration.
- Avoid central mutable JSON files for active state.
- `HANDOFF.md` is generated from the journal; do not maintain independent state in it.
- If `HANDOFF.md` has a merge conflict, regenerate it from `.handoff/events/**` when possible.
- Do not store secrets, tokens, credentials, private keys, or personal data.
- Always provide agent identity when writing events. Pass `--agent` on every
  `handoff add` call so filenames and event metadata stay attributable.
- If the current runtime cannot reliably identify itself, ask the user what
  agent/tool name should be recorded before writing events. Do not silently
  accept `unknown-agent` unless the user explicitly wants that fallback.

## Required behavior at session start

Before planning or editing a repo:

1. Find the repo root.
2. Check whether `HANDOFF.md` or `.handoff/` exists.
3. If neither exists, bootstrap only when the user explicitly requested handoff state. For an imminent transition, offer initialization once; do not write anything unless the user opts in.
4. Read `HANDOFF.md` first when present.
5. Read recent `.handoff/events/**` only as needed.
6. Summarize the current state in a few bullets.
7. Identify blockers, active tasks, current branch assumptions, and next actions.

Resolve the bundled helper before running commands:

1. Treat the directory containing this `SKILL.md` as the skill directory.
2. Resolve `scripts/handoff.py` relative to that directory. Set a task-local `HANDOFF_TOOL` variable to its absolute path, or substitute that path directly in the examples below.
3. Keep the target repository as the command working directory so the helper finds the correct handoff state.

Do not add a package-manager script, install a global binary, create another copy or wrapper outside the installed skill, or persist its machine-specific installed path. Skill installers place bundled resources alongside `SKILL.md`; resolve that installed copy at runtime.

The bundled helper requires Python 3.9 or newer and has no third-party dependencies.
Writes also require directory-relative no-follow operations and POSIX file
locking; native Windows Python rejects writes. Read-only commands remain
available. See the protocol reference for filesystem trust and failure limits.

```bash
python3 "$HANDOFF_TOOL" status
python3 "$HANDOFF_TOOL" tail --limit 20
```

If the bundled helper cannot be resolved, inspect the files directly and report that limitation.

## Required behavior during work

When handoff writes are authorized, add events when there is something future agents need to know.

Good event moments:

- session started with important scope
- plan was created or changed
- architectural decision was made
- files were changed meaningfully
- tests/lint/build were run
- blocker discovered
- risky assumption identified
- question needs user/human answer
- session ends or agent is about to switch

Keep active state accurate:

- Active work, blockers, risks, questions, and next actions carry stable references in generated `HANDOFF.md` comments and in the JSONL event IDs.
- When later work completes an item, add a new event with `--resolve <reference>`.
- When a newer item replaces an older one, add a new event with `--supersede <reference>`.
- A `session_end` event automatically resolves the latest matching `session_start` for the same branch/worktree and agent session.
- When a branch/worktree context is finished, mark it with `--context-status closed`, `merged`, or `abandoned`. Use `--context-status active` to reopen it.
- Never edit or delete the older event to change its state.

Do not log noise:

- trivial command attempts
- raw logs without summary
- obvious file reads
- repeated statements already captured

## Required behavior before stopping

Before ending a substantial turn/session in a repository that already uses handoff state, update it when handoff writes are authorized. In a read-only task without that separate authorization, leave the repository unchanged and report the continuity information in the response instead.

Minimum end-of-session update:

1. What changed.
2. What was validated.
3. Current blockers or risks.
4. Next recommended action.
5. Files touched or relevant paths.

Add a resolution event for each completed referenced item; omit that command when nothing was resolved.

```bash
python3 "$HANDOFF_TOOL" add --type validation --summary "<validated result>" --resolve "<completed-action-or-blocker-ref>" --agent "<agent-name>"
python3 "$HANDOFF_TOOL" add --type session_end --summary "<short summary>" --details "<concise details>" --agent "<agent-name>" --session "<session-id>"
python3 "$HANDOFF_TOOL" render
python3 "$HANDOFF_TOOL" validate
```

## Event types

Use these event types where possible:

- `session_start`
- `session_end`
- `status`
- `plan`
- `decision`
- `change`
- `validation`
- `blocker`
- `risk`
- `question`
- `todo`
- `handoff`

## JSONL event shape

Each line should be valid JSON.

Required fields:

```json
{
  "v": 1,
  "id": "uuid-or-stable-id",
  "ts": "2026-04-30T12:34:56Z",
  "type": "change",
  "summary": "Short human-readable summary"
}
```

Recommended fields:

```json
{
  "agent": {
    "name": "codex",
    "model": "gpt-5.5",
    "session": "short-session-id"
  },
  "git": {
    "branch": "feature/example",
    "commit": "full-commit-hash",
    "worktree": "worktree-name"
  },
  "scope": ["apps/web", "apps/api"],
  "files": ["apps/web/src/example.ts"],
  "details": "Concise details future agents need.",
  "next_actions": ["Run the project tests", "Split FooService"],
  "resolves": ["prior-event-id", "prior-event-id#next:1"],
  "supersedes": ["older-plan-event-id"],
  "tags": ["cleanup", "api"],
  "status": "open",
  "context_status": "active"
}
```

Generated next-action references use `<event-id>#next:<one-based-index>`. Keep legacy string-valued `next_actions` valid; close them through those generated references rather than rewriting their source event.

## Handoff markdown rules

`HANDOFF.md` should be compact and useful.

Preferred sections:

1. Latest state by active branch/worktree
2. Active work
3. Decisions
4. Blockers / risks
5. Validation status
6. Next actions
7. Recently changed / important files
8. Event journal pointer

Keep it short. If it grows too large, move detail into `.handoff/events/**` and keep only the current summary.

## CLI usage

This skill includes a Python helper at:

```text
scripts/handoff.py
```

Use the resolved bundled helper; no repository configuration or package-manager wrapper is required:

```bash
python3 "$HANDOFF_TOOL" init
python3 "$HANDOFF_TOOL" status
python3 "$HANDOFF_TOOL" add --type decision --summary "Use JSONL event journal" --details "SQLite was rejected because it is binary and hard to merge." --agent "copilot-cli"
python3 "$HANDOFF_TOOL" add --type validation --summary "Tests passed" --resolve "<action-ref>" --agent "copilot-cli"
python3 "$HANDOFF_TOOL" add --type plan --summary "Replaced the earlier plan" --supersede "<plan-event-id>" --agent "copilot-cli"
python3 "$HANDOFF_TOOL" add --type status --summary "Feature branch is complete and ready to merge" --context-status closed --agent "copilot-cli"
python3 "$HANDOFF_TOOL" render
python3 "$HANDOFF_TOOL" validate
python3 "$HANDOFF_TOOL" tail --limit 20
```

Use `status`, `tail`, or the `handoff-ref` comments in generated `HANDOFF.md` to obtain event/action references. The helper rejects unknown references, duplicate event IDs, malformed timestamps and lists, invalid configuration, and invalid events before append. Rendering also refuses invalid journal state rather than publishing a partial summary.

Identity guidance:

- Treat `--agent` as required in normal usage unless `HANDOFF_AGENT` is set.
- Prefer a stable agent/tool name such as `copilot-cli`, `codex`, or another
  user-recognizable runtime label.
- When available, also pass `--model` and `--session` so future agents can
  trace where an event came from.
- If you do not know your own identity with confidence, stop and ask the user
  before creating new handoff events.

## Git behavior

Recommended:

- Commit `HANDOFF.md`.
- Commit `.handoff/README.md`, `.handoff/config.json`, `.handoff/schema.json`.
- Commit `.handoff/events/**` when they contain project-relevant continuity.
- Do not commit generated caches or local lock files.
- Before the final commit that will be merged from a completed branch, append `--context-status closed` and rerender so the merge carries that terminal context event. Use `merged` only when the event is being recorded in that branch/worktree context after the merge is known to have completed.

If event volume grows too much, archive only self-contained, fully closed event chains under `.handoff/archive/`, keeping referenced targets and their resolving/superseding events together. Alternatively replace closed history with a monthly summary event. Run `validate` after compaction.

## Conflict handling

If `HANDOFF.md` conflicts and conflict repair is authorized:

1. Merge or resolve `.handoff/events/**` first; those files are the source of truth.
2. Do not manually combine the generated Markdown sections.
3. Regenerate `HANDOFF.md` from the merged journal.
4. Stage the regenerated `HANDOFF.md` as the conflict resolution.
5. Add a `handoff` or `status` event only when the resolution itself adds useful context.

JSONL event files from attached worktrees on distinct branches use branch-specific paths. Detached worktrees use their Git worktree names. Legacy single-event files stay immutable.

## Security rules

Never write secrets into handoff files.

Redact:

- API keys
- tokens
- passwords
- private URLs if sensitive
- customer data
- personal data
- production credentials

Write references like "secret is configured via env var `FOO_API_KEY`" instead of actual values.

## Response style

When using this skill, be brief in the main conversation:

- Say what handoff state says.
- Say what you updated.
- Say the next action.

Do not paste the full event journal unless explicitly asked.
