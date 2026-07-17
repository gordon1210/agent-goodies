# Design Review Method

Use this method to produce an independent, risk-based review rather than a rewrite or style edit.

## Start with a cold read

Before consulting background material, test whether the document stands on its own:

1. Restate the problem, outcome, scope, and chosen direction.
2. Trace one normal scenario and one failure scenario end to end.
3. Identify every point where an implementer must guess a requirement, contract, state transition, owner, or recovery behavior.
4. Note terms that change meaning, claims without evidence, and conclusions whose rationale is absent.

After the cold read, compare the document with linked briefs, decisions, project conventions, and the current system. Report both contradictions and important context that never reached the document.

## Apply review lenses

Select lenses in proportion to risk. Always apply the first four.

### Intent and scope

- Does the proposal solve the stated problem and respect the desired outcome, appetite, constraints, and non-goals?
- Are success signals observable, and can they distinguish improvement from activity?
- Has unrelated scope entered the design without justification?

### Decision quality

- Is the chosen direction explicit and supported by relevant evidence?
- Were credible alternatives considered, including a simpler or more reversible option?
- Are accepted trade-offs visible, or does the document claim only benefits?

### Comprehension and consistency

- Can an unfamiliar reader explain the boundaries, flows, responsibilities, and state transitions?
- Do summaries, diagrams, contracts, examples, and delivery steps describe the same system?
- Are facts, decisions, assumptions, and open questions distinguishable?

### Validation and traceability

- Does every material goal or requirement reach a design element and an observable check?
- Do tests cover risky behavior, boundaries, and recovery rather than only the happy path?
- Can rollout signals show when to continue, stop, or reverse?

### Interfaces and dependencies

- Are contracts, validation, authorization, ownership, versioning, ordering, idempotency, limits, and degraded behavior defined where relevant?
- Are external dependencies and failure responsibilities explicit?
- Will existing callers, users, or downstream systems remain compatible during transition?

### Data and concurrency

- Are source of truth, lifecycle, retention, deletion, migration, consistency, concurrency, and repair behavior clear?
- What happens after partial writes, duplicate events, reordered work, or a failed backfill?
- Can rollback restore code while leaving data in an incompatible state?

### Reliability and operations

- Are timeouts, retries, partial completion, degradation, recovery, and capacity limits credible?
- Do telemetry and alerts expose the stated failure modes with actionable thresholds?
- Is operational ownership named for launch and steady state?

### Security, privacy, and misuse

- Are trust boundaries, permissions, sensitive data, secret handling, abuse cases, and safe defaults addressed?
- Does the design expand access or retention without an explicit reason?
- Can an attacker or accidental caller exploit an ambiguous contract or failure path?

### Delivery and reversibility

- Is sequencing compatible across components and versions?
- Are migration, exposure, go/no-go checks, rollback, and roll-forward repair distinct and feasible?
- Does any supposedly reversible step create an external commitment or persistent state that cannot be undone?

## Attack the riskiest assumptions

For each assumption with material impact:

1. State what the design expects.
2. Construct a credible case in which it is false.
3. Trace the consequence through users, data, dependencies, operations, and delivery.
4. Check whether a validation action, mitigation, or contingency exists.

Treat missing evidence as uncertainty, not proof of failure. Treat an unstated but necessary choice as a design gap, not permission for the implementer to decide silently.

## Assign severity

- **Blocker:** The document cannot support safe planning because a core product or architectural decision is missing or contradictory, a high-impact failure has no credible response, or the proposed path could cause unacceptable irreversible harm.
- **Major:** A material gap is likely to cause significant rework, incorrect behavior, unsafe operation, or failed delivery, but resolving it need not replace the entire direction.
- **Minor:** A bounded ambiguity, weak rationale, or coverage gap should be clarified but does not prevent responsible planning.

Base severity on credible impact and decision risk, not word count, section count, or personal preference.

## Choose the verdict

- **Ready:** No blocker or major findings remain. Minor findings and residual risks are explicit and can be handled during planning.
- **Ready with follow-ups:** No blockers remain. Each major finding has a bounded, named resolution or accepted condition that does not require inventing core behavior during planning; list those conditions beside the verdict.
- **Not ready:** Any blocker remains, a major finding lacks a bounded resolution, the design requires implementers to make core decisions, or incompleteness is broad enough that a reliable plan would be fiction.

Do not average findings into a verdict. One genuine blocker is sufficient for **Not ready**.

## Keep findings useful

Anchor each finding to evidence and a plausible consequence. Ask for the missing decision or proof; avoid dictating an implementation unless only one safe option exists. Consolidate findings with the same root cause, omit cosmetic commentary, and state when a review lens found no issue only if that absence supports the verdict.
