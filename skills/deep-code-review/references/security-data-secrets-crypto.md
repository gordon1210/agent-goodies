# Data, Secrets, and Cryptography

## Contents

- Data classification and minimization
- Exposure paths
- Secret lifecycle
- Passwords and tokens
- Cryptographic operations
- Signatures and webhooks
- Verification and calibration

## Data classification and minimization

Identify what the changed path handles:

- public data
- internal operational data
- personal data
- authentication data
- financial, health, location, or other sensitive data
- cryptographic keys and production credentials

Then trace collection, persistence, access, transformation, output, logging, caching, analytics, backup, and deletion. Report only concrete boundary violations or contract regressions, not generic privacy advice.

Check whether the change:

- returns more fields than the caller is authorized to see
- copies sensitive fields into lower-trust stores, queues, search indexes, browser state, or telemetry
- changes retention or deletion behavior
- creates shared cache/temp/export locations
- leaks existence, metadata, or identifiers through errors or counts
- serializes secrets into URLs, command lines, process listings, build logs, crash reports, or client bundles
- weakens tenant or purpose separation

## Exposure paths

Inspect all outputs, not only API responses:

- structured logs and exception details
- tracing attributes, metrics labels, analytics events
- debugging endpoints and health/status pages
- notification/email content
- generated files, exports, reports, and download names
- caches, temporary files, browser storage, service workers, and source maps
- CI logs, artifacts, container layers, build arguments, and package metadata

Redaction must happen before data crosses the lower-trust boundary. A logger's formatting behavior and structured-field capture matter.

## Secret lifecycle

For keys, tokens, passwords, and credentials, check:

- whether the value is actually secret, environment-relevant, and usable
- generation source and entropy
- storage at rest and access permissions
- transmission channel
- scope, audience, privilege, and expiration
- rotation and revocation
- accidental copies in logs, caches, URLs, history, artifacts, or client code
- fallback/default credentials and development-to-production leakage
- secret comparison and disclosure through error messages

Do not report public API identifiers, example placeholders, checksums, or intentionally public keys as secrets. Verify active-looking credentials without attempting unauthorized use.

## Passwords and authentication secrets

Check that changed password handling preserves:

- a password-specific adaptive hash through an established library
- unique salts managed by the library
- appropriate handling of pepper/key material where the system uses it
- no plaintext or reversible storage
- bounded verification cost and safe migration between hash parameters
- generic external errors without breaking useful internal diagnostics
- reset/recovery tokens that are scoped, expiring, random, one-time, and stored safely

A different work factor is not automatically a vulnerability; establish that the change materially weakens the threat model or creates operational denial of service.

## Tokens

Inspect token creation and verification for:

- signature/MAC verification before trusting claims
- algorithm and key selection fixed by trusted policy, not token-controlled fallback
- issuer, audience, subject, scope, expiry, not-before, nonce, and token type
- separation among access, refresh, reset, verification, invitation, and webhook tokens
- replay, revocation, and rotation behavior
- leakage via URL query strings, referrers, logs, browser history, or third parties
- confusion between encoding and authenticity

Decoding a token is not verification.

## Cryptographic operations

Trace the required security property: confidentiality, integrity, authenticity, non-repudiation, password resistance, or randomness.

Check changes for:

- established library use rather than custom primitives/protocols
- authenticated encryption where integrity is required
- nonce/IV uniqueness and correct generation
- secure random generation for security decisions
- key size, type, use, separation, and rotation consistent with the protocol
- signature verification over the exact canonical bytes and all security-relevant fields
- verification result actually checked before use
- certificate/hostname verification and trust-store behavior
- downgrade/fallback behavior
- constant-time comparison where a remotely observable secret comparison makes it relevant
- integer, encoding, or canonicalization differences between signing and verification

Do not flag a primitive name in isolation. Show the broken property in the actual protocol.

## Signatures and webhooks

For signed callbacks or artifacts, inspect:

- raw bytes versus parsed/re-serialized body
- timestamp/freshness window
- replay identifier or idempotency handling
- key selection and rotation
- canonicalization and duplicate fields
- algorithm agility/downgrade
- whether verification occurs before parsing side effects or durable state changes
- secret selection by tenant/account without accepting an attacker-chosen tenant blindly

A valid signature proves possession of a key, not authorization for every referenced object or action.

## Verification

A finding should state:

- data/secret classification
- source and lower-trust destination
- exact changed exposure or cryptographic property violation
- who can observe or exploit it
- scope and recoverability
- controls checked

Do not include secret values in the review output. Redact identifiers sufficiently to remain actionable.

## Severity calibration

- A valid broad production credential enabling administrative compromise may be Critical.
- A scoped credential, token leak, or sensitive per-tenant disclosure is generally High.
- Limited personal-data or metadata exposure may be Medium depending sensitivity and audience.
- Logging a value is not automatically severe; determine log destination, access, retention, and actual field content.
- Weak crypto is not automatically Critical; prove the attack and resulting capability under realistic conditions.
