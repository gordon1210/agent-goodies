# Core Review Method

## Contents

- Review contract
- Change map
- Behavior-first passes
- Candidate verification
- Validation strategy
- Large changes
- Stop conditions

## Review contract

Establish the exact target before judging code.

1. Prefer an explicit base/head, PR diff, commit range, patch, or file scope supplied by the user.
2. For “review my changes,” include staged and unstaged tracked changes unless the user narrowed the scope. Note untracked files separately and include them only when clearly part of the change.
3. For a branch review without an explicit base, use the configured upstream or merge-base with the repository's default branch when it can be determined without guessing. State the chosen range.
4. Read the task, PR description, issue, acceptance criteria, relevant design records, and repository instructions available in the workspace.
5. Decide whether the review is change-scoped or a full audit. Default to change-scoped.

Do not silently substitute a whole-repository audit for a diff review or vice versa.

## Build a change map

Start with the changed-file and diff summary, then group files by behavior rather than directory.

For each behavior, identify:

- Entry points: routes, commands, event handlers, scheduled jobs, public functions, UI actions
- Changed decisions: branches, validation, policy, defaults, feature flags
- Data path: input, transformations, persistence, output
- State path: lifecycle, transitions, retries, cancellation, cleanup
- Trust boundaries: caller identity, tenant, process, service, network, file, model/tool boundary
- Contracts: schemas, APIs, events, configuration, migration and deployment order
- Dependencies: callers, callees, shared helpers, generated artifacts, external systems
- Evidence: tests, types, constraints, framework behavior, runtime checks

Use the map to select reference modules. Do not open unrelated modules “just in case.”

## Review behavior, not lines

Perform these passes over each changed behavior.

### 1. Intended outcome

Infer intent from requirements first, then tests, callers, names, comments, and existing conventions. Comments are evidence, not authority, when code and contracts disagree.

Write down the key invariant in one sentence, for example:

- “A user may update only resources in their tenant.”
- “An acknowledged job is durably persisted exactly once.”
- “Old and new service versions can coexist during rollout.”

A finding must show how the change violates an invariant or explicit requirement.

### 2. Normal path

Trace a representative valid input through the changed path. Check returned values, side effects, ordering, persistence, and externally visible behavior.

### 3. Boundary and failure paths

Trace the smallest meaningful set of distinct cases, not an exhaustive input list:

- absent, empty, zero, minimum, maximum, duplicate, malformed
- first/last item, page boundary, retry, timeout, cancellation
- partial failure before and after irreversible side effects
- stale state, concurrent actor, repeated delivery, reordered event
- old/new schema or version combinations during rollout

Select only cases that can reach the changed code.

### 4. Cross-boundary effects

Follow changed values or decisions across file boundaries until one of these is reached:

- a trusted, validated invariant
- a durable sink or external effect
- a public response or contract
- an authorization decision
- a bounded, safe library primitive

Do not stop at a wrapper merely because its name sounds safe.

### 5. Security triage

Apply `security-triage.md` to executable changes. Security review is data-flow and decision-flow reasoning, not keyword matching.

### 6. Operational behavior

Check rollout, retries, idempotency, resource bounds, observability of failure, and compatibility where the change touches those concerns.

### 7. Test integrity

Use tests to confirm assumptions. Inspect changed tests for weakened assertions, mocks that bypass the changed behavior, incorrect fixtures, and success-only coverage. Do not equate line coverage with correctness.

## Candidate verification: prove or drop

For every candidate issue, create an internal proof record:

- **Changed cause:** the exact changed statement, omitted action, or contract transition
- **Trigger:** concrete input, state, actor, version combination, or workload
- **Path:** caller/source through relevant guards to failure/sink
- **Consequence:** observable wrong result, security effect, data damage, outage, or contract break
- **Existing controls checked:** validators, middleware, constraints, retries, framework guarantees, permissions, deployment sequencing
- **Introduction:** why the target change creates or exposes the issue
- **Validation:** test, static trace, documentation, or safe command result

Then attempt to disprove it:

1. Search all relevant callers, not only the changed caller.
2. Inspect upstream validation and downstream checks.
3. Confirm actual library or language semantics instead of relying on a remembered pattern.
4. Check configuration, feature flags, environment assumptions, and deployment topology present in the repository.
5. Check whether the supposedly dangerous value is attacker-controlled or already canonicalized.
6. Check whether the path is reachable and used.
7. Compare against the base version to confirm introduction.
8. Check tests for intentional behavior or a counterexample.

Drop the candidate if a material link in the proof remains speculative. When one explicit, plausible runtime premise cannot be verified from the repository, report it only as conditional and follow the confidence rules in `severity-evidence.md`.

## Validation strategy

Prefer the cheapest reliable evidence:

1. Static trace and repository contracts
2. Focused existing test
3. Existing typecheck, lint, build, or analyzer command
4. Small non-destructive reproduction using existing project tooling

Do not install packages, change lockfiles, launch deployments, run migrations, contact production services, or execute destructive/integration commands without explicit authorization. Tests may write caches or temp files; follow repository guidance and disclose commands run.

A command failure is not automatically a product finding. Distinguish:

- defect exposed by the change
- pre-existing failure
- environment/tooling failure
- unavailable dependency or service

## Large changes

For a large PR:

1. Partition by independent behavior or trust boundary.
2. Prioritize authentication/authorization, irreversible data changes, public contracts, migrations, concurrency, and externally reachable parsing.
3. Review shared primitives before their callers.
4. Track reviewed groups to avoid omissions and duplicate findings.
5. If the client supports parallel agents, independent scoped passes may be used, but every returned finding must still pass the same central disproof and severity gates.

Do not lower evidence standards because the diff is large.

## Stop conditions

Stop only when:

- every changed behavior has an identified invariant
- each changed trust, state, and contract boundary has been traced
- all selected modules have been applied
- every reported finding has survived disproof
- duplicate symptoms have been merged under one root cause
- validation performed and validation omitted are recorded

Do not keep searching merely to produce a minimum number of comments. Zero findings is a valid result.
