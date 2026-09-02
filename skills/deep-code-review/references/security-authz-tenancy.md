# Authentication, Authorization, and Tenancy

## Contents

- Identity establishment
- Session and token lifecycle
- Authorization decisions
- Tenant and object isolation
- Workflow and delegated authority
- Caches and background work
- Verification and calibration

## Identity establishment

Trace how the application establishes identity and where that identity becomes trusted.

Check changes to:

- credential verification and account lookup
- issuer, audience, subject, expiry, not-before, signature, and key selection for tokens
- login linking, social identity mapping, email normalization, and account merge behavior
- password reset, email verification, MFA enrollment/recovery, device trust, and magic links
- fallback or anonymous identities
- service-to-service identities, workload credentials, and impersonation
- middleware ordering and route-group coverage

Do not accept a user ID, tenant ID, role, email, or service name from a request merely because it matches a field in a valid token. Prove the binding to the authenticated principal.

## Session and token lifecycle

Inspect whether the change preserves:

- session rotation after login, privilege change, or account recovery
- expiry and revocation semantics
- logout invalidation where the contract promises it
- refresh-token reuse detection and rotation where applicable
- invalidation after password reset, user disablement, tenant removal, or role downgrade
- cookie scope, transport protection, and cross-site behavior
- separation between access, refresh, verification, reset, and API tokens
- one-time use and replay resistance for action links or codes

A longer lifetime or missing rotation is not automatically a finding. Show the security property the change breaks and the resulting capability.

## Authorization decisions

Trace authorization at the final operation on the protected resource.

Check:

- function-level access: who may invoke the operation
- object-level access: who may read or modify this exact object
- field-level access: which fields may be seen or changed
- action-level access: whether state and prior approvals permit the transition
- tenant scoping in reads, writes, joins, aggregates, exports, and counts
- default-deny behavior for new enum values, roles, routes, or resource types
- batch and bulk operations: policy must apply to each target
- indirect access through search, autocomplete, errors, existence checks, or side channels
- authorization before side effects, not only before response generation
- TOCTOU: policy may change between check and use

Authentication is not authorization. Route middleware that proves identity does not prove object ownership.

## Tenant and object isolation

For multi-tenant code, follow the trusted tenant context through every layer:

- route or message entry
- service method
- database query and joins
- cache key
- object storage path or bucket prefix
- queue/event payload
- background worker
- search index and analytics query
- logs, exports, notifications, and webhooks

Look for:

- tenant IDs accepted from body/query parameters when a trusted context exists
- missing predicates on reads, updates, deletes, and upserts
- joins that reintroduce rows from another tenant
- globally unique ID assumptions that replace authorization
- cache entries keyed only by object ID or URL
- shared temporary files or predictable export names
- background jobs that reconstruct identity or tenant incorrectly
- admin or support impersonation without explicit scope and auditability

A globally unique identifier reduces accidental collision; it does not grant access.

## Workflow and delegated authority

Review stateful security workflows for:

- invitation accepted by a different identity than intended
- approval performed by the requester or after approver authority was revoked
- owner/admin removal leaving an invalid or uncontrolled resource
- role escalation through editable role/permission fields
- confused-deputy behavior where a privileged service acts on untrusted target identifiers
- delegated tokens usable outside their resource, action, tenant, or time scope
- replay of signed requests, webhooks, links, or recovery artifacts
- sequence bypass: calling completion before prerequisites or reusing an already consumed step

Check both API paths and background/event-driven paths.

## Caches and background work

Authorization context must survive asynchronous boundaries.

Inspect:

- whether jobs carry a trusted principal/tenant or re-resolve policy at execution time
- whether queued work remains valid after role or membership changes
- cache keys that omit role, tenant, locale, policy version, or visibility state
- negative authorization results cached beyond policy changes
- retry paths that skip the original check
- scheduled jobs running with a global service identity and user-controlled targets

Do not assume the authorization at enqueue time remains valid indefinitely.

## Verification

A reportable finding should include:

- principal and privilege level
- target resource/action
- path to the final access or side effect
- missing or incorrect policy decision
- why middleware, query constraints, or downstream checks do not prevent it
- blast radius: one object, one tenant, many tenants, or system-wide

Search route registration, middleware composition, policy helpers, database constraints, and all relevant callers before claiming a missing check.

## Severity calibration

- One reachable cross-tenant read/write path is generally High.
- A bounded disclosure of low-sensitivity metadata may be Medium.
- Systemic unauthenticated administrative access or broad cross-tenant control may be Critical when all Critical gates pass.
- A client-side visibility bug is Low/Medium as a UI defect when the server denies the action; it is not an authorization vulnerability.
- An admin-only path is not automatically harmless, but required privilege reduces reachability and must affect severity.
