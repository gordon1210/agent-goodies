# Data, State, and Concurrency

## Contents

- Transactions and atomicity
- Database constraints and queries
- Migrations and backfills
- Idempotency and retries
- Queues and events
- Caches
- Local concurrency
- Distributed coordination
- Verification and calibration

## Transactions and atomicity

Identify the logical operation and all durable/external side effects it requires.

Check:

- operations that must commit or roll back together
- external side effects inside a database transaction that may retry or roll back
- state committed before an external action whose failure must be recoverable
- side effect completed before durable idempotency/audit state
- nested transaction/savepoint semantics
- transaction object accidentally not passed to one query
- isolation level versus the invariant being protected
- reads performed outside the transaction and used for a later write
- error paths that commit partial state
- long transactions spanning network calls or user work

“Uses a transaction” does not prove atomicity across services.

## Database constraints and queries

Inspect changes to:

- uniqueness and identity definition
- foreign keys and cascading behavior
- not-null/default/check constraints
- upsert conflict target and update set
- affected-row checks for update/delete
- joins, filters, grouping, and aggregation
- read-modify-write sequences
- locking or compare-and-swap/version predicates
- pagination and deterministic ordering
- nullable columns and three-valued logic

Application checks can race unless the database or an equivalent serialized boundary enforces the invariant.

Check whether zero affected rows means not found, unauthorized, stale version, or success under the contract.

## Migrations and backfills

Trace forward deploy, mixed-version operation, rollback, and retry.

Check:

- expand/migrate/contract ordering
- old code reading/writing the new schema and new code reading/writing the old schema
- adding required columns without safe defaults/backfill
- changing type/meaning while old binaries coexist
- index/constraint creation locking or scanning large tables on the normal path
- non-idempotent migrations or hooks retried after partial completion
- backfill batching, ordering, resume cursor, and concurrent writes
- data transformation reversibility and rollback compatibility
- destructive drops/renames before all consumers move
- application assumptions before backfill completion

Do not assume zero-downtime requirements unless deployment evidence or repository policy establishes them, but standard rolling orchestration is relevant evidence.

## Idempotency and retries

For repeatable operations, identify the idempotency identity, durable record, and response replay behavior.

Check:

- idempotency key scope: tenant, actor, operation, payload/version
- key stored before/after irreversible side effects
- concurrent requests with the same key
- same key reused with a different payload
- expiration shorter than realistic retry windows
- failure between effect and record/ack
- retry classification and retry budget
- duplicate message/event delivery
- client, proxy, queue, and server retries combining unexpectedly
- retry of non-idempotent operations

A retry bug becomes severe when the repeated effect is financial, destructive, externally visible, or difficult to reverse.

## Queues and events

Trace producer, broker semantics, consumer, durable state, and acknowledgment.

Check:

- at-most-once, at-least-once, or effectively-once assumptions
- acknowledgment before durable completion
- poison-message behavior and retry storms
- ordering/partition-key changes
- event schema compatibility
- deduplication identity and retention
- consumer concurrency and per-key serialization
- transactional outbox/inbox correctness where used
- event emitted from state that later rolls back
- missing wakeup or lost notification between state write and enqueue
- dead-letter handling that silently loses required work

Do not demand exactly-once semantics when the workflow is safely idempotent.

## Caches

Identify source of truth, key, value, invalidation, and consistency promise.

Check:

- tenant/user/role/locale/version omitted from key
- negative or authorization result cached too broadly
- invalidation before a write that can fail
- write succeeds but invalidation/event fails
- stale value used for a security or irreversible decision
- cache stampede or unbounded key/cardinality growth
- mutable object references shared through in-memory cache
- TTL incompatible with correctness requirement
- key collisions or normalization differences
- cache warming/backfill changing load behavior

Staleness is only a defect relative to an explicit or established consistency contract.

## Local concurrency

Identify shared mutable state and all concurrent execution contexts.

Check:

- lost update and check-then-act races
- map/list/object access without required synchronization
- lock held across blocking or awaited work
- inconsistent lock ordering and re-entrancy
- missed wakeups, channel close ownership, and send-after-close
- task/goroutine/thread leaks after cancellation or failure
- cancellation leaving half-applied state
- callbacks executed concurrently despite single-thread assumptions
- unsafe publication or stale visibility
- atomic operations whose ordering does not establish the required invariant

Do not report a race without proving two reachable overlapping accesses and at least one write or invalid lifecycle transition.

## Distributed coordination

Check:

- lease duration, renewal, fencing token, and clock assumptions
- lock owner identity and safe release
- failover causing two active workers
- leader election transition and stale leader writes
- uniqueness enforced only by best-effort distributed locks
- saga/compensation ordering and irreversible steps
- network timeout interpreted as operation failure when outcome is unknown
- split-brain handling
- monotonic version/revision checks

A distributed lock without fencing may not protect an external resource from a paused former owner.

## Verification

A concurrency/data finding must specify an interleaving or failure point:

1. initial state
2. actor/task A action
3. actor/task B or failure action
4. resulting persisted/external state
5. invariant violated

For migrations, specify old/new version combination and rollout step. For retries, specify exactly where the timeout/crash occurs.

## Severity calibration

- Broad irreversible primary-data destruction on the normal deploy path may be Critical.
- Plausible duplicate financial/destructive effects, cross-tenant cache leakage, or likely rollout outage are High.
- Recoverable per-record inconsistency or uncommon race is usually Medium.
- The mere absence of a lock/transaction is not a finding when the invariant is enforced elsewhere.
