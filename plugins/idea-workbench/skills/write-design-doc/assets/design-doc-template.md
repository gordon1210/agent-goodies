# Design: [Concise title]

> Adapt this template to the change and its risk. Remove irrelevant subsections; briefly explain any omission that would otherwise be expected for a medium- or high-risk change.

| Field | Value |
| --- | --- |
| Status | Draft / Ready for review / Approved |
| Owner | [Decision owner] |
| Reviewers | [Required reviewers] |
| Last updated | [Date] |
| Source brief | [Link or reference] |
| Risk | Low / Medium / High — [reason] |

## Summary

[Explain the problem, chosen direction, and expected result in a short paragraph.]

## Context

### Problem and evidence

[Describe the current situation, affected people or systems, and the evidence that makes the problem worth solving.]

### Goals and success signals

- [Outcome and how it will be observed]

### Scope

- **In:** [Included behavior or boundary]
- **Out:** [Explicit non-goal]

### Constraints

- [Time, compatibility, policy, platform, cost, or organizational constraint]

## Decision ledger

### Known facts

| Fact | Evidence |
| --- | --- |
| [Supported fact] | [Source or observation] |

### Decisions

| Decision | Rationale and accepted trade-off |
| --- | --- |
| [Choice] | [Why this choice fits] |

### Assumptions

| Assumption | Impact if wrong | Validation action |
| --- | --- | --- |
| [Unverified belief] | [Consequence] | [How and when to test it] |

### Open questions

| Question | Blocking? | Impact | Next decision-maker or action |
| --- | --- | --- | --- |
| [Unresolved choice] | Yes / No | [What depends on it] | [Owner and next step] |

## Options considered

### Chosen direction

[Describe the direction and why it best satisfies the goals and constraints.]

### Alternatives

| Alternative | Advantage | Reason not chosen |
| --- | --- | --- |
| [Credible alternative] | [What it does better] | [Relevant drawback] |

## Detailed design

### Boundaries and ownership

[Identify what changes, what remains untouched, and who or what owns each responsibility.]

### User and system flows

[Walk the important end-to-end scenarios, including state transitions and boundary conditions.]

### Components and dependencies

[Describe responsibilities, collaboration points, and external dependencies.]

### Interfaces and contracts

[Define inputs, outputs, invariants, compatibility rules, authorization, and versioning where applicable.]

### Data and state

[Describe the data model, source of truth, lifecycle, migration, retention, and concurrency behavior where applicable.]

### Failure and recovery

[Describe expected failures, timeouts, retries, partial completion, degraded behavior, and recovery paths.]

## Cross-cutting concerns

### Security, privacy, and abuse

[State trust boundaries, sensitive data handling, permissions, compliance needs, and plausible misuse.]

### Performance, capacity, and cost

[State relevant budgets, expected load, bottlenecks, and cost implications.]

### Compatibility and accessibility

[State compatibility promises, transition behavior, and applicable accessibility needs.]

## Validation and operations

### Acceptance scenarios

- **Given** [starting condition], **when** [event], **then** [observable result].

### Test strategy

[Map important behavior and risks to automated, manual, integration, or exploratory checks.]

### Observability and ownership

[Define signals, logs, metrics, alerts, dashboards, support ownership, and operational thresholds.]

## Delivery

### Migration and rollout

[Describe sequencing, compatibility windows, feature exposure, and go/no-go checks.]

### Rollback and recovery

[Define how to stop or reverse the change and how to repair affected state.]

## Risks and rabbit holes

| Risk | Likelihood / impact | Mitigation or contingency |
| --- | --- | --- |
| [Failure mode or uncertainty] | [Assessment] | [Response] |

## Readiness

- **Result:** Ready for review / Not ready
- **Blocking items:** [None, or the decisions and evidence still required]
- **Next action:** [Smallest useful next step]
