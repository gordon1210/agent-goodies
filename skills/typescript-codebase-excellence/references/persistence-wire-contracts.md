# Persistence, Wire Formats, and Data Contracts

Read this reference when code reads or writes JSON, HTTP/RPC payloads, events, queues, databases, caches, files, browser storage, generated clients, schemas, or migrations. Static TypeScript types do not preserve or validate data across these boundaries.

## 1. Identify the source of truth

For each data contract, determine whether the source of truth is:

- Runtime schema/validator.
- OpenAPI, JSON Schema, GraphQL, Protocol Buffers, Avro, database schema, or another IDL.
- TypeScript types plus handwritten parser/serializer.
- Generated code.
- Existing persisted data and compatibility fixtures.
- External provider documentation/API behavior.

Avoid two independently edited sources that can drift. If both runtime schema and TypeScript types exist, establish which generates/derives/checks the other and how drift is detected.

## 2. Boundary model versus domain model

External and persisted shapes often should not be the same objects used internally.

Use a boundary parser/mapper when it provides value:

- Field names, nullability, precision, or representation differ.
- Validation/normalization is required.
- External versions must map to one internal model.
- Sensitive or irrelevant fields should be dropped.
- Generated clients expose transport-specific types.
- Domain invariants require constructors or brands.

Do not create DTOs and mappers mechanically for every object. Keep one representation when the boundary shape already expresses the domain safely and stably.

## 3. JSON semantics

JSON supports objects, arrays, strings, booleans, null, and finite numeric syntax. JavaScript values do not map losslessly:

- `undefined`, functions, symbols, and many object properties can disappear.
- `bigint` is not serialized by standard JSON without explicit conversion.
- Dates become strings only through deliberate serialization behavior.
- `Map`, `Set`, typed arrays, class instances, errors, and prototypes lose their semantics.
- `NaN`, infinities, and negative zero can change representation.
- Large integers can exceed safe JavaScript number precision.
- Duplicate object keys may be accepted with last-value behavior before validation sees them.

Define explicit wire representations for nontrivial values. Test round trips only for information the format is intended to preserve.

## 4. Optionality and nullability

Distinguish at every boundary:

- Missing field.
- Present with null.
- Present with an empty value.
- Present with a default value.
- Present with undefined before serialization.

Database nullability, GraphQL nullability, JSON Schema required fields, TypeScript optional properties, and runtime object presence are not interchangeable.

Migration and compatibility logic must specify whether a missing old field receives a default, is rejected, or remains semantically absent.

## 5. Numeric values, money, and precision

- Do not use binary floating-point for money/accounting when exact decimal semantics are required without an explicit rounding model.
- Define integer ranges and safe-number requirements at JSON/JavaScript boundaries.
- Represent large integers as strings, bigint-aware codecs, or a protocol type with explicit conversion.
- Validate decimals, scale, currency, units, rounding mode, and overflow.
- Do not convert bigint to number without a checked range.
- Define behavior for non-finite values before persistence or transport.
- Use database numeric/decimal types and drivers deliberately; many drivers return strings to preserve precision.

A TypeScript `number` annotation does not guarantee integer, finite, safe, positive, or exact values.

## 6. Dates, time, and duration

- Use unambiguous timestamp representations with specified timezone/offset and precision.
- Distinguish wall-clock timestamp, calendar date, local date/time, duration, and monotonic elapsed time.
- Do not parse unspecified locale date strings.
- Define whether timestamps are normalized to UTC and how offsets are preserved when needed.
- Account for daylight-saving transitions and clock skew for business rules.
- Avoid treating JavaScript `Date` serialization as a complete domain contract.
- Store durations as an explicitly named unit or structured representation.
- Version precision changes; milliseconds versus microseconds/nanoseconds can break ordering and equality.

Test timezone, leap-day, DST, min/max, and precision boundaries relevant to the domain.

## 7. Identifiers and enumerations

- Treat identifiers as opaque strings unless arithmetic/order is part of the contract.
- Define case sensitivity, normalization, namespace, allowed format, and maximum length.
- Avoid exposing sequential internal IDs where guessability or tenant isolation matters.
- Validate external enum/discriminant values at runtime.
- Design unknown enum handling for forward compatibility.
- Adding a variant can break exhaustive TypeScript consumers even when the wire format is additive.
- Do not reuse identifiers across tenants or resource types without an explicit namespace.

## 8. Schema evolution principles

For long-lived formats:

- Add versions or reliable feature/shape detection.
- Prefer additive changes when old readers can ignore unknown fields and new readers can default missing fields safely.
- Do not reuse a field name/tag for a different meaning.
- Do not change units, precision, normalization, or requiredness silently.
- Keep old and new representations during rolling deployments where mixed versions coexist.
- Separate migration/backfill from destructive cleanup.
- Define the compatibility window and when old writers/readers may be removed.
- Preserve unknown fields only when required; doing so can retain untrusted/sensitive data and complicate validation.

“Tolerant reader” behavior must not permit security-sensitive ambiguity or silently accept malformed critical fields.

## 9. API request and response contracts

For each endpoint/operation define:

- Authentication and authorization scope.
- Request method/path/query/header/body schema and size limits.
- Content type and encoding.
- Success and error response schema/status.
- Pagination, filtering, sorting, and consistency.
- Idempotency and retry semantics.
- Timeouts/cancellation.
- Version and deprecation policy.
- Sensitive-field exposure and redaction.

Validate at the server even when a generated or typed client constructs the request. Treat response validation according to trust and blast radius; third-party and cross-team services can violate contracts.

Do not expose raw persistence entities, ORM objects, internal errors, or secret-bearing configuration directly.

## 10. OpenAPI and JSON Schema

When using OpenAPI/JSON Schema:

- Identify the supported specification/dialect and generator versions.
- Review `required`, nullable values, unions, discriminators, additional properties, formats, defaults, examples, and read/write-only semantics.
- Do not assume a `format` keyword performs validation unless the validator is configured accordingly.
- Ensure runtime validator and generated TypeScript agree on coercion and unknown fields.
- Keep request and response schemas separate when fields/requiredness differ.
- Test recursive schemas and maximum depth/resource use.
- Review generated clients for authentication, base URL, retries, cancellation, and error typing.
- Treat schema changes as public API changes and diff them deliberately.

Generated TypeScript alone does not enforce the schema.

## 11. GraphQL

GraphQL provides a typed schema but still requires runtime resolver correctness and authorization.

- Distinguish nullable field, nullable list, and nullable list elements.
- Validate custom scalar input/output and serialization.
- Enforce authorization in resolvers/data access, not only UI/query visibility.
- Bound query depth, complexity, aliases, list sizes, and batching.
- Prevent N+1 behavior without cross-tenant cache leakage.
- Handle partial data plus errors deliberately in clients.
- Review persisted-query and introspection policy according to threat model.
- Keep generated operations/types synchronized and remove stale operations.
- Treat schema changes, deprecations, and enum additions as consumer compatibility events.

## 12. Binary/IDL protocols

For Protocol Buffers, Avro, MessagePack, CBOR, or custom binary formats:

- Define field/tag evolution rules and unknown-field behavior.
- Validate lengths, nesting, allocation, enum values, and required semantic invariants.
- Preserve integer precision and byte/string distinctions.
- Define canonical encoding only when signatures/hashes/deduplication require it.
- Review generated defaults and absent-field behavior.
- Test old/new readers and writers with stored fixtures.
- Avoid custom codecs for security-sensitive formats when established implementations exist.
- Keep schema and generator versions pinned/reproducible.

## 13. Database boundaries

Database schemas and drivers are runtime contracts.

- Validate driver-returned values when type generation cannot guarantee runtime schema/version.
- Account for numeric/date/binary conversion behavior.
- Use parameterized queries.
- Whitelist dynamic identifiers/operators/sort expressions.
- Include tenant/authorization scope in queries.
- Bound result count and bulk operations.
- Use transactions appropriate to invariants and isolation requirements.
- Handle uniqueness, foreign key, check, serialization, and deadlock errors as structured outcomes where callers act differently.
- Do not assume ORM model optionality matches database nullability/default/generated columns.
- Keep read/write models and migrations compatible during rolling deployment.

## 14. Transactions and atomicity

Define the invariant and transaction boundary before writing code.

- Validate input and authorization before costly/irreversible effects where possible.
- Keep transactions short enough for contention/lock budgets.
- Avoid network calls inside a database transaction unless the consistency protocol explicitly requires and tolerates them.
- Handle retryable serialization/deadlock failures only when the transaction is safe to rerun.
- Do not acknowledge queue work before required state commits.
- Use an outbox/inbox/idempotency pattern when coordinating database and messaging effects requires it.
- Distinguish committed-but-response-lost from not committed.
- Ensure cancellation/timeout returns the connection to a known usable state.

A TypeScript transaction callback type does not prove all operations use the same transaction context.

## 15. Migrations

Treat migrations as production code.

Before release:

- Define forward, mixed-version, rollback, and recovery behavior.
- Assess table size, locks, indexes, replication, backfill duration, and resource load.
- Separate additive schema, application rollout, data backfill, read switch, write switch, and destructive cleanup where needed.
- Make migrations deterministic and idempotent only when the migration framework/semantics support it.
- Avoid network calls and undeclared environment dependence.
- Test on representative data volume and database version.
- Back up and test restore for destructive/irreversible steps.
- Instrument progress/failure without logging sensitive rows.
- Never edit an already-applied migration unless repository policy explicitly supports immutable replacement before release.

Generated migration success on an empty database does not prove safe production rollout.

## 16. ORMs and query builders

- Understand lazy/eager loading, transactions, connection ownership, serialization, lifecycle hooks, and default scopes.
- Avoid mass assignment from untrusted objects.
- Review raw-query and expression escape hatches as security-sensitive.
- Inspect generated SQL/query plans for critical paths.
- Keep entities/domain objects/API responses distinct when invariants or exposure differ.
- Do not hide database errors behind one generic error when conflict/retry behavior matters.
- Ensure migrations are reviewed independently from model changes.
- Verify code generation against the actual schema and deployment version.

Do not add repository/service layers automatically around an ORM; add boundaries where domain or testing ownership requires them.

## 17. Events, queues, and messages

Messages are versioned wire contracts.

Define:

- Schema/version and producer/consumer ownership.
- Delivery semantics.
- Ordering and partition key.
- Idempotency/deduplication.
- Maximum payload and headers.
- Trace/security/tenant context.
- Retry/dead-letter behavior.
- Retention and privacy.
- Mixed producer/consumer deployment compatibility.

Validate messages at consumption even when the producer is typed. Do not place secrets or large raw payloads in messages without a governed requirement. Avoid coupling consumers to internal database entity shapes.

## 18. Caches

A cache has a data contract and consistency model.

- Define key namespace/version/tenant scope.
- Validate cached values on read when corruption/version skew is possible.
- Bound entry size, count, and lifetime.
- Define invalidation, freshness, stale-while-revalidate, and failure behavior.
- Avoid cache keys containing secrets or unbounded user text.
- Prevent cross-tenant key collisions.
- Treat cache stampede and negative caching deliberately.
- Do not rely on a cache as the sole durable source unless it is designed and operated as one.
- Version serialized entries when deployment changes representation.

## 19. File and browser-storage formats

For config/state/files/local storage/IndexedDB:

- Validate and version on every read.
- Write atomically where partial data is harmful.
- Define locking/concurrent-writer behavior.
- Set permissions and path roots for sensitive server files.
- Handle corruption, missing files, quota, eviction, and old versions.
- Do not store secrets in script-readable browser storage when safer session mechanisms exist.
- Remove user/tenant data on logout/account switch as required.
- Keep migration and recovery bounded; do not load unbounded files into memory.

## 20. Generated clients and SDKs

Generated code often models transport, not domain guarantees.

Review:

- Base URL and environment selection.
- Authentication injection and credential forwarding.
- Cancellation/deadline support.
- Retry defaults and idempotency.
- Response/error parsing and unknown statuses.
- Runtime validation.
- Pagination and streaming.
- Browser/server compatibility and bundle impact.
- Versioning and generator/source provenance.

Wrap a client only when a boundary adds real policy such as auth, validation, retries, telemetry, or domain mapping. Do not add a pass-through service layer solely to rename methods.

## 21. Compatibility testing

For durable contracts, maintain fixtures representing:

- Oldest supported persisted/message/API version.
- Current version.
- Missing/unknown/additive fields.
- Invalid/truncated/oversized data.
- Numeric/date/Unicode boundary cases.
- Mixed old/new producer-consumer combinations.
- Migration interruption and recovery.
- Package/compiler-generated declaration differences where relevant.

Test both reading old data and preventing unsupported old writers when required. Round-trip tests should state what information is intentionally normalized or lost.

## 22. Data privacy and retention

- Classify fields before persisting, caching, logging, or emitting events.
- Collect and retain only what the product/legal contract requires.
- Keep tenant/user deletion and correction flows consistent across primary stores, caches, queues, analytics, backups, and derived data.
- Encrypt in transit and at rest according to platform policy, while managing keys separately.
- Avoid placing personal/sensitive data in identifiers, cache keys, URLs, metrics labels, or event routing keys.
- Define retention and access controls for fixtures, snapshots, and debugging exports.
- Redact generated examples and migration logs.

## Persistence completion checklist

- Every boundary has an explicit source of truth and runtime validation strategy.
- Boundary representations map deliberately to domain models.
- Optionality, precision, time, identifiers, and non-JSON values are explicit.
- Schema evolution and mixed-version behavior are defined.
- API/database/message/cache/storage contracts include limits, authorization, and error semantics.
- Transactions and retries preserve atomicity/idempotency.
- Migrations are deployable, observable, recoverable, and tested on representative data.
- Generated clients/types remain aligned with runtime behavior.
- Compatibility fixtures cover old/new and malformed data.
- Privacy, retention, and tenant scope survive every copy of the data.
