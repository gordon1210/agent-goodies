# Calibration Examples

Use these examples to calibrate evidence and severity. Match the properties of the path, not just the vulnerability name.

## Critical

### Normal deployment destroys primary data

A new migration unconditionally drops a populated production table as part of the standard deploy path, no copy/backfill exists, and application code still requires the data. This is Critical because the trigger is the normal rollout, the damage is broad and irreversible from the application, and the changed migration is the direct cause.

### Unauthenticated model output reaches privileged shell execution

An internet-facing chat endpoint passes model-generated text to a shell with host credentials and no command policy or sandbox. An untrusted user can influence the model through the normal endpoint. This can be Critical when the trace proves arbitrary command execution and broad production capability.

## High, not Critical

### Cross-tenant object access

A changed query drops the tenant predicate for one authenticated resource endpoint. The path discloses or modifies another tenant's records. This is normally High: serious and merge-blocking, but bounded to the affected object/path unless the evidence proves systemic administrative compromise.

### Duplicate payment after retry

The change acknowledges a payment attempt after the external charge but before recording the idempotency key. A timeout causes a retry and a second charge. This is High under a plausible failure path. It becomes Critical only with evidence of systemic, high-value execution at scale and no containment.

### Rolling deployment contract break

A producer starts emitting a required enum value that currently deployed consumers reject, and both versions coexist during rollout. A likely processing outage is High. It may become Critical only when the affected service is critical, total outage is reliable, and rollback/containment is ineffective.

## Medium

### Supported date boundary returns the wrong day

A new conversion interprets a local date as UTC, shifting the result for users west of UTC near midnight. The affected path is real and supported but bounded and recoverable: Medium.

### Goroutine or listener leak on repeated reconnect

The change leaves one goroutine/listener alive per reconnect. Reconnects are plausible but infrequent and resource exhaustion requires sustained churn: Medium unless normal production behavior makes exhaustion rapid and broad.

## Low

### Misleading error on a bounded path

A changed parser reports “not found” for one malformed optional configuration value, delaying diagnosis but not changing operation or security. This is a concrete Low defect, not a merge blocker by default.

## Not findings

### Parameterized query mistaken for SQL injection

A query string contains placeholders and untrusted values are passed through the driver's parameter API. The table name comes from a closed internal enum. String appearance alone is not evidence of injection.

### Authentication enforced outside the changed handler

A handler lacks a local authentication call, but all routes in the mounted group pass through verified authentication and object authorization middleware. Do not report “missing auth” without a bypass path.

### `unwrap` on an invariant established by construction

Rust code unwraps a value produced from a static compile-time constant during startup, and process termination is the intended response to invalid packaged configuration. `unwrap` is not automatically a bug.

### Dependency advisory without reachability

A lockfile changes a package version that appears in an advisory, but the affected API is not used and no repository policy blocks the version. Record a verification need only when affected-version and reachability evidence can be established.

### Missing test without a demonstrated defect

A branch has no new test. That may be a process concern, but it is not a product bug unless repository policy explicitly requires it or the test change itself masks a regression.

### Theoretical race with no concurrent access

A mutable value is unsynchronized, but construction and all access occur on one event-loop task before publication. Do not report a race because the type could theoretically be shared.

### Hardening suggestion presented as a vulnerability

An authenticated low-volume endpoint has no additional rate limiter, while global limits and bounded work already contain abuse. Extra defense may be useful, but absence is not a proven vulnerability.
