# Planning Quality

Use these checks to turn an approved design into executable work without
silently redesigning it.

## Test verticality

A vertical slice crosses every layer needed to prove one narrow outcome. Judge
it by observable behavior, not by the number of components changed.

Prefer:

- create and retrieve one valid record end to end;
- complete one happy-path interaction with its minimum persistence and tests;
- migrate one safe cohort and prove rollback;
- expose one integration path with failure handling and telemetry.

Avoid a sequence such as “create schema,” “build service,” “add interface,” then
“write tests.” Those tasks postpone usable evidence and make partial progress
hard to evaluate. Fold supporting work into the first behavior that consumes it.

Keep a foundation slice only when it has its own consumer, contract test,
migration proof, or other independently useful result.

## Control slice size

Make a slice small enough for one focused implementation session but large
enough to produce meaningful evidence. Split it when it contains multiple user
outcomes, unrelated risks, independent rollout decisions, or several completion
conditions. Merge it when neither half can be verified without the other.

Use the first slice as a tracer through the real boundaries. Expand depth,
variants, edge cases, and operational hardening in later slices without creating
temporary architecture that contradicts the approved design.

## Maintain two-way traceability

Require both directions:

1. Map each approved requirement, acceptance criterion, and consequential design
   decision to work and verification.
2. Map each slice to an approved outcome, requirement, or named risk reduction.

Allow many-to-many mappings. Split broad requirements into stable local labels
when needed, but do not rewrite their meaning. Treat an unmapped requirement as
missing work and an unmapped slice as probable scope creep.

## Keep dependencies honest

Declare a dependency only when a slice cannot begin or cannot be verified
without another slice's result. Do not encode a preferred reading order as a
blocker.

- Refer to dependencies by stable slice identifier.
- Keep shared contracts stable before claiming parallel execution.
- Move setup into the earliest consumer unless several slices truly share it.
- Check for cycles and needlessly long serial chains.
- Order migrations, compatibility windows, release controls, and recovery steps
  around the state transitions they protect.

## Ground detail in evidence

Inspect the project before asserting paths, package names, commands, or tooling.
Match detail to confidence:

- Name an exact path only after locating it.
- Name a component or responsibility when its path is not yet established.
- Include a bounded discovery action when ownership must be found during a slice.
- Copy command syntax only from confirmed project configuration or documentation.
- State the verification intent without a command when no command is known.

Do not use plausible-looking detail as a substitute for evidence. A concise,
accurate plan is more executable than a precise fiction.

## Demand meaningful verification

Give each slice evidence at the boundary where it creates value. Combine methods
when the risk requires them:

- focused automated checks for logic and contracts;
- end-to-end or integration evidence for boundary crossings;
- observable scenarios for user-facing behavior;
- migration, compatibility, rollback, or recovery evidence for state changes;
- telemetry and alert evidence for operational behavior;
- targeted security, privacy, accessibility, or performance checks when those
  qualities affect acceptance.

Name the expected result, not merely the act of “testing.” Include negative and
failure-path evidence where silent failure would be costly.

## Reject false readiness

Stop planning when any unresolved question could materially change:

- the promised outcome or acceptance criteria;
- scope or explicit non-goals;
- system ownership, boundaries, or interfaces;
- persistent data, migration, or compatibility;
- security, privacy, or permissions;
- rollout, rollback, or operational responsibility.

Return the smallest such decision to design or design review. Do not disguise it
as “investigate,” “decide,” or “finalize” inside an implementation slice.

Before presenting the plan, reject it if it contains orphaned requirements,
unjustified work, unverifiable slices, invented paths or commands, circular
dependencies, hidden design choices, or unresolved placeholders.
