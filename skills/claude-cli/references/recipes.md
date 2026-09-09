# Recipes

Examples use POSIX shell syntax. Set `CLAUDE_HELPER` to the actual installed
script path; it is a normal shell variable, not a host-specific skill macro.
The directories and material must already be authorized for this task.

```bash
CLAUDE_HELPER=/absolute/path/to/claude-cli/scripts/ask_claude.py
python3 "$CLAUDE_HELPER" doctor --cwd /absolute/project
```

## Independent second opinion

Write a question packet containing the relevant source/diff, the decision
criteria, verified facts, and remaining uncertainties. Then:

```bash
python3 "$CLAUDE_HELPER" ask \
  --cwd /absolute/project \
  --prompt-file /approved/work/question.md \
  --out-dir /approved/work/claude-opinion-01
```

Read `text` and `session_id` in stdout. Do not compare conclusions by vote;
compare evidence, assumptions, and counterexamples.

## Exact-session follow-up

Write the next message to a file, then replace the example UUID below with the
actual ID returned by the first call:

```bash
python3 "$CLAUDE_HELPER" ask \
  --cwd /absolute/project \
  --resume 12345678-1234-4123-8123-123456789abc \
  --prompt-file /approved/work/follow-up.md \
  --out-dir /approved/work/claude-opinion-02
```

For ordinary one-to-one dialogue, new context is enough because the native
session contains earlier turns. A council has stronger shared-history needs;
use its canonical transcript and bundled orchestrator instead.

## Source review

```bash
python3 "$CLAUDE_HELPER" ask \
  --cwd /absolute/project \
  --tools read \
  --prompt-file /approved/work/review-packet.md \
  --out-dir /approved/work/claude-source-review
```

Include applicable project instructions explicitly because safe-mode skips
ordinary customizations. Read tools may access more than the named task files;
the prompt's scope is not an OS-enforced path restriction. For stricter data
minimization, supply selected excerpts to the default tool-free profile.

## Stdin without a prompt argument

```bash
cat /approved/work/question.md | python3 "$CLAUDE_HELPER" ask \
  --cwd /absolute/project --stdin \
  --out-dir /approved/work/claude-stdin-call
```

The wrapper rejects blank, invalid UTF-8 file input, and oversized input. Do not
try to fit sensitive or large data into command substitution or positional argv.

## Failure handling

Inspect `request.json`, `stdout.json`, `stderr.log`, and `outcome.json` in the
retained directory. `result.json` exists only after validation succeeds. An
exit-zero native process is insufficient on its own. A failure makes no claim
that the native session was untouched. Never retry a timed-out resume blindly.
