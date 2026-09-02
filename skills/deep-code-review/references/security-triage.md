# Security Triage

Apply this lightweight pass to every executable change, then load only the specialized security modules selected by the result.

## Build the threat slice

For each changed behavior, identify:

- **Actor:** anonymous user, authenticated user, tenant member, administrator, service, CI job, local user, plugin, model, or operator
- **Source:** request, header, token, database row, event, file, URL, environment, dependency metadata, model output
- **Asset:** account, tenant data, secret, money, signing authority, host, network, availability, audit trail
- **Decision or sink:** authorization branch, query, renderer, serializer, shell, filesystem, network request, cryptographic operation, deployment action
- **Boundary:** browser/server, tenant/tenant, service/service, container/host, repository/CI secret, model/tool, trusted/untrusted file
- **Control:** validation, canonicalization, parameterization, authorization, sandbox, isolation, rate/resource bound, signature, encryption, rollback

A security finding needs a concrete path from an actor-controlled or lower-trust source to a security decision or dangerous sink.

## Triage questions

1. Did the change add or widen an externally reachable entry point?
2. Did it remove, relocate, or duplicate an authentication or authorization check?
3. Does identity, role, tenant, ownership, or policy now come from an untrusted value?
4. Does untrusted data reach a query, renderer, command, expression engine, parser, file path, URL, redirect, or deserializer?
5. Does the change expose, log, cache, persist, or transmit sensitive data differently?
6. Does it create or verify tokens, passwords, signatures, hashes, encryption, randomness, or certificates?
7. Does it add outbound network access, file/archive handling, child processes, plugins, or callbacks?
8. Does it alter dependencies, CI permissions, release artifacts, containers, IAM, or deployment boundaries?
9. Does a model, agent, retrieval result, or tool output influence privileged actions?
10. Can repeated, concurrent, malformed, or large input turn bounded work into an availability or cost attack?

Load the matching specialized module for every “yes” or plausible “unknown.” Do not load a module merely because a file contains a related keyword.

## Trace requirements

For each candidate:

- prove who controls the source
- identify every transformation and validation step
- inspect the actual sink or policy decision semantics
- verify whether encoding/canonicalization occurs in the correct context
- inspect framework middleware ordering and route composition
- check privilege and tenant context at the final resource access, not only at the entry point
- check whether the attack crosses a boundary that materially increases capability
- identify the concrete confidentiality, integrity, availability, financial, or authorization impact

Pattern matches are leads, not findings.

## Business-logic abuse

Do not restrict security review to classic injection categories. Inspect changed workflows for:

- replay, double spend, duplicate redemption, or repeated side effects
- step skipping and out-of-order transitions
- negative quantities, refunds greater than payment, or limit-reset manipulation
- race-assisted quota, inventory, invitation, or approval bypass
- trusting client-computed prices, roles, entitlements, or workflow state
- privilege retained after membership, ownership, role, or credential changes
- batch operations whose per-item policy is not enforced
- indirect object access through exports, search, counts, errors, or background jobs

Require the same concrete trigger and impact as any other finding.

## Security non-findings

Do not report solely because:

- a function name contains `unsafe`, `raw`, `admin`, or `eval`
- validation is absent locally but enforced by a verified caller or safe typed primitive
- a stronger hardening control could be added without a demonstrated threat-model violation
- a sensitive-looking constant is a public identifier or test fixture
- a dependency is old without evidence of a relevant defect
- an error includes internal detail that never crosses a lower-trust boundary
- a service listens on an address that is not exposed by the deployment
- a client UI allows an action that the server correctly denies

Route and investigate; do not convert checklists into findings.
