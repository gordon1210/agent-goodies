# Collaboration patterns

Use Grok as a collaborator with a named role, a bounded authority envelope, and
an explicit return contract. The host agent remains accountable for synthesis,
verification, and user-facing actions.

## Select a pattern

| Desired interaction | Session strategy | Grok authority | Default surface |
|---|---|---|---|
| Independent second opinion | Fresh | Read-only | `grok -p` |
| Architecture or design consultation | Fresh, then optional exact resume | Read-only | `grok -p` |
| Rubber duck | Resume one exact ID | No tools or read-only | `grok -p` |
| Grok as pair navigator | Resume one exact ID | Read-only | `grok -p`; ACP when live steering is needed |
| Grok as pair driver | Resume one exact ID | Named edits and commands | `grok -p`; ACP for live permission/control loops |
| Bounded implementation delegation | Fresh in a dedicated worktree | Named edits and validation | `grok -p` |
| Code or security review | Fresh | Read-only | `grok -p` with structured output |
| IDE or live permission loop | Persistent ACP session | Per-call approvals | `grok agent stdio` |
| Parallel specialist panel | One fresh session per independent slice | Usually read-only | Several host-managed `grok -p` calls |

Use a fresh session when independence matters. Resume the returned session ID
when continuity matters. Do not use `-c` for concurrent work.

For ACP pairing, use the bundled [ACP bridge client](acp-client.md). Read status
from its local event state; do not interrupt Grok merely to ask how far it is.
Use `steer` only for a material mid-turn correction. A normal follow-up after
completion remains a new `prompt` in the same session.

## Collaboration control loop

Every pattern follows the same loop:

1. **Frame:** state the role, objective, evidence, scope, permissions, output,
   and stop conditions.
2. **Execute:** run with the least tools and a bounded turn count.
3. **Observe:** capture status, tool calls, final answer, and session ID.
4. **Verify:** inspect cited code, diff, tests, and external facts from the host.
5. **Respond:** accept, reject, ask a targeted follow-up, or escalate to the
   user.

Never ask Grok merely to “take a look” when the expected decision or artifact
can be stated. Never accept a result solely because two models agree.

## Common task contract

Start from this packet and remove irrelevant fields:

```text
Role: You are the <role> collaborating with a separate host agent.

Objective:
<One observable outcome.>

Scope:
- Working directory: <absolute path>
- Inspect: <paths, symbols, diff, logs, or facts>
- Own/edit: <none, or exact paths>
- Do not touch: <unrelated work and excluded paths>

Known evidence:
- <facts already observed, with locations or command output>

Constraints:
- Follow discovered repository instructions.
- Do not widen scope, delete/discard work, commit, push, deploy, publish,
  contact external systems, or change configuration.
- Do not spawn subagents unless this packet explicitly permits it.
- Stop if the requested outcome requires an unlisted side effect.

Allowed actions:
- <read-only inspection, exact edits, exact validation commands>

Deliverable:
- <answer, ranked options, findings, patch, next step, or schema>
- Separate observed facts from inferences.
- Cite paths, symbols, commands, and outputs as evidence.
- State uncertainty and what would resolve it.

Done when:
- <acceptance checks>
```

The command-level controls must agree with the packet. Natural-language limits
do not compensate for a broader tool or permission grant.

## Independent consultation

Use for architectural judgment, API design, trade-offs, migration planning, or
a second opinion.

### Packet

```text
Role: Independent technical consultant. You are advisory and read-only.

Question:
<decision to make>

Context and constraints:
<relevant facts only>

Before recommending anything:
1. Inspect the cited code and instructions.
2. Identify assumptions and missing evidence.
3. Generate at least two viable options, including keeping the current design
   when credible.
4. Compare correctness, compatibility, complexity, testability, operations,
   migration cost, and reversibility.

Return:
- Observed facts
- Options and trade-offs
- Recommendation with rationale
- Main counterargument
- Unknowns and cheapest checks to resolve them

Do not edit files or run write-capable commands.
```

Ask Grok before supplying the host's preferred conclusion. After the response,
compare its evidence to the code and then expose the conclusion for a targeted
critique if needed.

### Invocation

Use the read-only baseline from [Headless mode](headless.md). Enable web only
when current external facts are required and the user permits that data flow.
Start a fresh session; resume only for follow-up questions on the same decision.

## Rubber-duck dialogue

The goal is to improve the user's or host's reasoning, not to outsource the
answer prematurely.

### First turn

```text
Role: Socratic rubber duck. Do not edit files and do not propose a solution yet.

Problem statement:
<current explanation>

For this turn:
- Restate my claimed behavior in at most three sentences.
- Identify the single most important ambiguity or untested assumption.
- Ask exactly one concrete question.
- Do not list multiple questions, diagnose conclusively, or give implementation
  advice unless I explicitly switch modes.
```

Capture the returned `sessionId`. For each answer, resume that exact ID:

```text
My answer: <answer and evidence>

Continue as the same rubber duck. Update your short model of the problem, then
ask exactly one next question. Prefer a question that separates competing
hypotheses. Do not solve it yet.
```

When ready to switch:

```text
Switch from questioning to synthesis. List the confirmed facts, remaining
assumptions, the smallest falsifiable hypothesis set, and the cheapest next
experiment. Do not edit files.
```

Disable all tools when the dialogue needs no repository context. Otherwise use
read-only tools, no memory, no web, no MCP, and no subagents.

## Pairing: Grok as navigator

The host is the driver and owns all edits. Grok reads the live code or diff,
checks reasoning, and proposes one next move.

### Initial packet

```text
Role: Pair-programming navigator. The host agent is the driver and owns edits.

Goal and acceptance criteria:
<goal>

Current state:
<evidence and current approach>

Your responsibilities:
- Inspect the relevant code and current diff.
- Check the driver's hypothesis against evidence.
- Name one risk or missed edge case when present.
- Recommend exactly one smallest next step and how to validate it.

Do not edit, run write-capable commands, expand the task, or produce a full
replacement implementation.
```

Resume the same session after the host makes each change:

```text
The driver completed the proposed step. Re-read the current diff and relevant
code; do not trust the summary alone.

Evidence from validation:
<output>

Return: what changed in your model, any regression, and exactly one next step.
```

Use a fresh read-only audit after several turns or a major design pivot. A long
pairing session accumulates assumptions and can become over-anchored.

## Pairing: Grok as driver

The host is navigator and approval boundary. Use only when edits are intended.
Give Grok one coherent step at a time, exact ownership, and exact validation.

### Step packet

```text
Role: Pair-programming driver. Implement only the step below.

Owned paths:
- <exact paths>

Step:
<one small behavior change>

Preserve:
- <public APIs, compatibility, unrelated user changes>

Allowed validation:
- <exact commands>

Stop before:
- Any file outside owned paths
- Dependency, schema, configuration, generated-file, lockfile, or public API
  changes not named above
- Deletion, Git history changes, commit, push, network side effects, or external
  mutations

Return:
- Files changed and why
- Validation actually run with result
- Remaining uncertainty
```

After each turn, the host inspects the diff before resuming. If Grok needs a
broader change, it reports the proposed expansion without making it. Use a
dedicated host-created worktree when the driver is not sharing the host's exact
working copy.

## Bounded implementation delegation

Use for an independently testable slice with clear ownership. Do not delegate
a vague repository-wide goal or overlap another agent's files.

### Preconditions

- The user requested the implementation, not merely advice.
- Existing worktree state and ownership are known.
- A dedicated worktree was created by the host when isolation is needed.
- The assignment has acceptance criteria and a finite validation command set.
- Destructive, remote, commit, push, publish, deploy, and cleanup actions are
  excluded unless separately authorized.

### Constrained invocation shape

Adapt the paths and exact validation commands to the repository:

```bash
GROK_MEMORY=0 grok --cwd /absolute/dedicated-worktree \
  --prompt-file /authorized/path/task-packet.md \
  --output-format streaming-json \
  --tools "read_file,search_replace,grep,list_dir,run_terminal_cmd" \
  --no-subagents \
  --disable-web-search \
  --permission-mode dontAsk \
  --sandbox workspace \
  --allow "Edit(src/owned-area/**)" \
  --allow "Write(src/owned-area/**)" \
  --allow "Bash(git status*)" \
  --allow "Bash(git diff*)" \
  --allow "Bash(<exact validation command>*)" \
  --deny "MCPTool" \
  --max-turns <bounded-count> \
  --no-auto-update
```

This is a shape, not a universal policy. Confirm exact tool IDs and permission
matching on the installed version. `workspace` still reads broadly, allows
network, and permits writes anywhere under the working directory; path-scoped
permission rules and the host-created worktree are necessary additional
layers. An unmatched operation is denied by `dontAsk`.

Do not broaden to always-approve merely because a validation command was
blocked. Add one reviewed exact permission or let the host run the check.

### Acceptance

The host, not Grok, confirms:

- Only owned files changed.
- Existing user changes were preserved.
- The diff implements the stated behavior without unrelated cleanup.
- Reported commands actually ran and their outputs support the claim.
- Failure, cancellation, and cleanup paths are sound.
- No commit, push, external mutation, or hidden generated state occurred.

## Code review

Use a fresh, read-only session. Let Grok inspect the actual diff and surrounding
code rather than only a prose summary.

### Packet

```text
Role: Independent code reviewer. Read-only.

Review target:
<commit range, diff, or owned paths>

Intended behavior:
<spec and invariants>

Look only for concrete problems in correctness, data integrity, security,
concurrency, compatibility, error handling, performance, or missing tests.

For each finding return:
- Severity: blocker, high, medium, or low
- Path and smallest useful location
- Concrete failure mode
- Evidence and triggering scenario
- Smallest credible remediation
- Test that would catch it

Separate findings from questions. Do not report style preferences without a
real maintenance or behavior cost. If there are no findings, say so and list
what remained unverified. Do not edit files.
```

Use `--json-schema` when another process consumes findings. Verify every cited
location and failure mode from the host before presenting it as a confirmed
finding.

## Adversarial and security review

Start from a fresh session with memory, shell, web, MCP, plugins, and subagents
disabled unless a specific source is necessary. Do not execute untrusted build
scripts, tests, samples, or proof-of-concept payloads merely to confirm a
finding.

Ask for:

- Assets, trust boundaries, attacker capabilities, and assumptions.
- Entry points and concrete exploit paths.
- Existing mitigations and why they fail or hold.
- Severity separated from confidence.
- Evidence that is safe to reproduce.
- A remediation and regression test.

Run a second targeted turn only after the independent pass, supplying the host's
hypothesis and asking Grok to falsify it.

## Debugging consultant

Use Grok to maintain a falsifiable hypothesis ladder rather than generate many
speculative fixes:

```text
Role: Debugging consultant. Read-only until explicitly switched.

Observed symptom:
<exact symptom>

Evidence:
<logs, reproducer, recent changes, checks already run>

Return:
1. Confirmed facts versus assumptions.
2. At most three mutually distinguishing hypotheses.
3. The cheapest safe observation that separates them.
4. The expected result under each hypothesis.

Do not propose a code change until the evidence selects a hypothesis.
```

Resume the exact session with each observation. Start a fresh session if the
conversation becomes committed to a repeatedly falsified theory.

## Parallel specialist panel

Parallelize only independent questions whose results can be reconciled without
shared writes. Examples include API compatibility, security, tests, and
operational risk for the same proposed design.

The host should:

1. Define non-overlapping questions and one common evidence packet.
2. Start a fresh read-only session for each specialist.
3. Pass `--no-subagents` so fan-out remains host-controlled.
4. Capture each answer and uncertainty independently.
5. Synthesize by evidence and constraints, not majority vote.
6. Run a final conflict-resolution question only for material disagreements.

Never run parallel write delegates in the same worktree or with overlapping
ownership. Use separate, positively identified worktrees and integrate through
an explicit host review if parallel writes are genuinely required.

## Conflict resolution

When Grok and the host disagree:

1. Restate the disputed proposition in testable terms.
2. List the evidence each conclusion depends on.
3. Inspect the primary source or run the cheapest safe discriminating check.
4. Ask a fresh Grok session to evaluate the evidence without the conclusions.
5. Keep uncertainty explicit if the evidence remains incomplete.

Do not resolve disagreement by asking the same anchored session repeatedly or
by counting model votes.

## Stop and escalate

Stop the collaboration turn and return control to the user when Grok needs:

- Access outside the agreed working directory or owned paths.
- Credentials, private data, a new plugin, MCP server, marketplace, or endpoint.
- A destructive command or deletion of pre-existing state.
- A database, cloud, deployment, CI, issue-tracker, messaging, or other remote
  mutation.
- A dependency, architecture, public API, schema, or compatibility change not
  covered by the task.
- More cost, parallel fan-out, or an open-ended loop beyond the agreed bound.

Report the exact blocker and proposed next action. A failed Grok call never
widens the authority envelope.
