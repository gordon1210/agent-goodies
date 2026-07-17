# Design Coverage Guide

Use this guide to choose proportional coverage. Treat it as a thinking aid, not a demand to fill every heading.

## Classify the risk

- **Low:** Local, familiar, reversible, and limited in blast radius. Cover the core and any concern the change directly touches.
- **Medium:** Crosses a component or team boundary, changes a shared contract or persistent data, introduces a meaningful dependency, or requires coordinated delivery. Cover the core plus every relevant conditional concern.
- **High:** Difficult to reverse, security- or privacy-sensitive, externally committed, operationally critical, novel, costly, or migration-heavy. Examine every relevant concern, attach evidence to key assumptions, and make recovery and ownership explicit.

Raise the classification when uncertainty compounds. A small change with an unknown migration path or an untrusted boundary is not low risk.

## Cover the core

Every design should make these points understandable:

1. **Problem and outcome:** Who or what is affected, what evidence exists, and how success becomes observable.
2. **Scope and boundaries:** What changes, what does not, and where responsibilities begin and end.
3. **Decision:** Which direction was chosen, what credible alternative was rejected, and which trade-off was accepted.
4. **Behavior:** The important end-to-end scenarios, states, and boundary conditions.
5. **Uncertainty:** Which statements are facts, decisions, assumptions, or open questions.
6. **Verification:** How the intended behavior and the riskiest claims will be tested.

## Add conditional coverage

### Product and interaction

Cover actors, permissions, discoverability, empty and error states, accessibility, and changes to established expectations. Make acceptance scenarios observable rather than subjective.

### Architecture and dependencies

Cover component responsibilities, seams, ownership, dependency direction, build-versus-buy choices, and behavior when a dependency is unavailable or changes.

### Interfaces and compatibility

Cover contract shape, invariants, validation, authentication and authorization, idempotency, ordering, versioning, rate limits, and compatibility windows.

### Data and state

Cover source of truth, schema evolution, lifecycle, retention, deletion, consistency, concurrency, backfill, audit needs, and repair after partial failure.

### Reliability and recovery

Cover timeouts, retries, duplicate work, partial completion, degradation, recovery point, recovery time, and the distinction between rollback and roll-forward repair.

### Security, privacy, and misuse

Cover trust boundaries, sensitive inputs and outputs, least privilege, secret handling, data exposure, abuse cases, compliance obligations, and safe defaults.

### Performance, capacity, and cost

Cover relevant budgets, expected and peak load, growth assumptions, bottlenecks, resource ceilings, cost drivers, and what happens when a limit is reached.

### Delivery and migration

Cover sequencing, compatibility during transition, feature exposure, data migration, go/no-go signals, rollback feasibility, and cleanup after stabilization.

### Operations and ownership

Cover logs, metrics, traces, alert thresholds, dashboards, runbooks, support path, operational owner, and how responders distinguish expected noise from failure.

## Keep statements honest

Record each material item in the appropriate form:

- **Known fact:** Include its evidence or source.
- **Decision:** Include the reason and accepted downside.
- **Assumption:** Include the consequence if wrong and a validation action.
- **Open question:** Include whether it blocks progress, what depends on it, and who decides next.

A document may be complete while retaining non-blocking questions. It is not ready when an implementer must silently convert a critical assumption or open question into a design decision.
