# Workflow and shared-history design

## One host, two external peers

The current agent is the host. The runner cannot call back into that agent's
private runtime, so it deliberately pauses at host boundaries. The host reads a
brief, writes a contribution with its normal file tool, and asks the runner to
advance the peers. This preserves the original workflow without an extra
Codex process, another host subscription call, an SDK, or an always-on service.

The helper supports an explicit `--host-name` for the display label, defaulting
to `Codex`. This does not launch or authenticate that host. The external peers
remain exactly `grok` and `claude`; this is not a generic arbitrary-command agent
framework. Both peer adapters are included, so installing this skill alone does
not produce sibling-path import failures.

## Commands

Set the normal shell variable `COUNCIL` to the installed script's absolute path.
In a repository checkout it can point to
`skills/agent-council/scripts/council.py`. All examples below use an existing,
approved workspace parent and the intended project's absolute working directory.

```bash
COUNCIL=/absolute/path/to/agent-council/scripts/council.py
python3 "$COUNCIL" doctor --cwd /absolute/project
python3 "$COUNCIL" init \
  --run-dir /approved/work/council-01 \
  --cwd /absolute/project \
  --topic-file /approved/work/topic.md \
  --rounds 4 --config-reviewed
python3 "$COUNCIL" brief --run-dir /approved/work/council-01
```

Read the **entire** `brief` result. Its `revision` is a state revision, not a
round number. Use the returned integer directly. In the example below, `1` is
valid only if the fresh brief actually returned `revision: 1`:

```bash
python3 "$COUNCIL" host \
  --run-dir /approved/work/council-01 \
  --message-file /approved/work/host-round-01.md \
  --expect-revision 1
python3 "$COUNCIL" advance --run-dir /approved/work/council-01
python3 "$COUNCIL" brief --run-dir /approved/work/council-01
```

Do not wrap this in an unattended shell loop that invents host text or repeats
the same file every round. The agent must actually reason about the new peer
contributions. Revision checks reject stale input; they cannot prove the agent
read or understood the brief.

| Command | Behavior |
|---|---|
| `doctor` | Version/help/config metadata probes, no model call |
| `init` | New immutable task/config snapshot and private run directory |
| `status` | Lightweight state, next action, sessions, pending attempt |
| `brief` | Full canonical context, discussion, assessments, revision |
| `host` | Commit the current host's actual next contribution |
| `advance` | Run due peers, stopping at a host boundary; never invent host turns |
| `note` | Add an approved correction/evidence update without rewriting history |
| `recover --accept` | Commit a valid already captured result without a new call |
| `recover --discard` | Explicitly abandon an uncertain attempt and its native session |
| `finalize` | Store the host's actual synthesis; require completion or explicit partial status |
| `export` | Regenerate derived transcripts/report from authoritative state |

`host`, `note`, and `finalize` require `--message-file` and a fresh
`--expect-revision`. A changed requirement after final assessments begin needs a
new council, rather than silently making those assessments stale.

## Initialization options

Defaults are four rounds, 500 words of response guidance, 240 seconds per peer
call, four internal agent turns, a 256 KiB full-prompt cap, native resume, and
Grok's `read-only` sandbox. Set another explicit value when the task requires it.
The round range is 1–8; normally use 3–5. One round is useful for smoke tests.

`--context-file` may be repeated. Its text is captured at initialization; later
filesystem edits cannot silently change the supplied evidence. Use a `note` for
an approved correction, labeling its source and verification status. Neither
provider fetches a file merely because the topic names its path.

Optional `--claude-model`, `--grok-model`, `--claude-effort`, and `--grok-effort`
are passed through as explicit argument values. Otherwise each CLI uses its
configured model. Discover valid names from the target installation. This skill
does not freeze speculative model IDs, choose fallbacks, or rewrite preferences.

The input cap is a byte budget, **not a model-token estimate**. If it is exceeded,
the runner stops before the next request and preserves the complete history.
Raising it with a new approved run does not increase the model's context window.
There is no hidden compaction or truncation policy. Responses above 64 KiB are
also rejected instead of quietly shortened.

## Resume versus replay

**`--session-mode resume` (default):** capture each peer's returned UUID and use
that exact ID on its next call. Nevertheless, every request includes a complete
current discussion snapshot. Earlier native snapshots are explicitly marked
historical. There is no per-peer incremental cursor that could silently omit a
contribution after a partial failure or native compaction.

The tradeoff is real: native sessions accumulate repeated snapshots. This costs
more context and input usage than a correct incremental-only implementation.
For short 3–5-round discussions this favors inspectability and explicit delivery
of the requested full history. It is not advertised as token-minimal.

**`--session-mode replay`:** start a fresh native session on every call, supplying
the same complete canonical context. Logical discussion continuity remains in
`state.json`, not native memory. This avoids accumulating old snapshots inside
one session, and is useful when context size matters or native persistence is
unreliable. It does not rely on hidden native memories.

Both modes guarantee what the script **submits**, not that a model attends to
all tokens or that the provider never changes/trims its internal context. A
successful process result is not proof of semantic recall. Input snapshots and
hashes make the transport inspectable.

## Final coverage

A sequential discussion has an unavoidable asymmetry: the first speaker cannot
see later contributions until another input is delivered. After the last round,
two final-assessment calls give both peers the same completed discussion. Each
assessment is stored separately and withheld from the other assessment prompt.
The host then gets both assessments and the entire discussion in `brief`.

For `N` rounds the runner makes `2N + 2` peer calls, excluding explicit retries.
There are `3N` discussion contributions plus two final assessments. The host's
report is not another debate turn. The peers do not receive the host's final
report automatically, and the script never claims they have endorsed it.

## Synthesis rubric

Give the recommended decision and the strongest evidence behind it. State which
alternatives were rejected and why. Preserve remaining dissent and identify the
smallest concrete validation steps that could change the decision. Attribute
important objections by peer/message ID where useful. Distinguish consensus,
factual evidence, plausible inference, and missing information.

The script writes no model-generated host synthesis. Without a real host
contribution file, it cannot finish the run.
