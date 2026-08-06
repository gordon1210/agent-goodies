# Handoff Protocol

## Philosophy

The handoff system is a repo-local continuity layer for agents and humans.

It uses two layers:

1. `HANDOFF.md` for humans and quick agent orientation.
2. `.handoff/events/**.jsonl` as append-only machine-readable history.

The event journal is the durable source. `HANDOFF.md` is the compact working summary.

## Why not SQLite as the primary format?

SQLite is excellent for local querying, but it is a poor primary committed handoff format:

- binary diffs are unreadable
- merges are fragile
- code review is weak
- multiple agents editing it can create locking or conflict issues
- many AI agents can inspect Markdown/JSONL more reliably than SQLite

SQLite can still be useful as a generated local cache, but not as the repo source of truth.

## Why JSONL?

JSONL is append-friendly, diffable, grep-friendly, streamable, and easy for any agent/tool to parse.

Shard event files by month and contextual day/agent/type/branch/commit filenames. Encode branch names so distinct refs cannot collapse to the same filename: short names stay fully percent-encoded; encoded names longer than 50 characters use a stable prefix+hash token. The full branch name always remains in event metadata. For detached HEADs, substitute Git's worktree administrative name for the branch. This keeps parallel worktrees in separate append-only batches while still allowing multiple event lines per file.

Legacy one-event `.jsonl` files remain valid. Readers should support mixed history without requiring a rewrite.

## Append-only lifecycle

Do not infer that historical work is still active merely because its event remains in the journal. Reduce active state through explicit references:

- Every event has a stable `id`.
- A next action at index `N` has reference `<event-id>#next:<N+1>`.
- A later event lists completed targets in `resolves` and replaced targets in `supersedes`.
- `session_end` automatically resolves the latest open `session_start` with the same Git context and agent session (or agent name when no session ID exists).
- `context_status` is `active`, `closed`, `merged`, or `abandoned`. Terminal contexts do not appear as active branch/worktree state; a later `active` event reopens one.
- Terminal event statuses such as `completed`, `resolved`, `closed`, or `superseded` prevent that event and its actions from rendering as active.

Generated `HANDOFF.md` lines carry `handoff-ref` HTML comments so agents can resolve items without exposing identifiers in the human-rendered summary. Preserve legacy events that lack lifecycle metadata; resolve them by their existing event/action references in a new event.

## Recommended workflow

Resolve `scripts/handoff.py` relative to the installed Handoff skill's `SKILL.md`. Set a task-local `HANDOFF_TOOL` variable to its absolute path, or substitute that path directly. Keep the target repository as the working directory. Do not add a package-manager wrapper or persist the installed path in the repository.

Start:

```bash
python3 "$HANDOFF_TOOL" status
python3 "$HANDOFF_TOOL" tail --limit 20
python3 "$HANDOFF_TOOL" add --type session_start --summary "Starting work on <scope>" --agent "<agent-name>" --session "<session-id>"
```

During work:

```bash
python3 "$HANDOFF_TOOL" add --type decision --summary "Chose X over Y" --details "Reason..." --agent "<agent-name>"
python3 "$HANDOFF_TOOL" add --type validation --summary "Project tests passed" --details "Command: <project test command>" --resolve "<action-ref>" --agent "<agent-name>"
```

End:

```bash
python3 "$HANDOFF_TOOL" add --type session_end --summary "Finished <scope>" --details "Changed..., validated..., next..." --agent "<agent-name>" --session "<session-id>"
python3 "$HANDOFF_TOOL" render
python3 "$HANDOFF_TOOL" validate
```

Agent identity is important because the helper uses it in event metadata and
filenames. Pass `--agent` on every `handoff add` call. If the current runtime
cannot identify itself confidently, ask the user which agent name should be
recorded instead of silently falling back to `unknown-agent`.

Pass the same `--session` value to `session_start` and `session_end`. If the runtime has no stable session identifier, omit it from both commands; the helper then pairs the latest session for the same agent and Git context.

## Worktrees and conflicts

Record `git.branch`, `git.commit`, and Git's worktree administrative name on new events. Group rendered current state by branch; do not treat the newest event from one parallel branch as the sole project state.

Before a completed branch's final merge-bound commit, append `--context-status closed` in that branch/worktree so the merge carries its terminal state. Use `merged` only when recording from the same context after the merge is known to have completed, and use `abandoned` before preserving or otherwise integrating the final journal state of abandoned work. Do not delete journal history.

Treat `HANDOFF.md` as derived output. When it conflicts, merge the branch-specific JSONL journal files first, run `python3 "$HANDOFF_TOOL" render` against the merged journal, and stage the regenerated Markdown instead of manually combining both rendered versions.
