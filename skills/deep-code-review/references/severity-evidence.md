# Evidence and Severity

## Contents

- Evidence threshold
- Finding eligibility
- Severity model
- Critical gates
- Security calibration
- Downgrade and rejection rules
- Merge guidance

## Evidence threshold

Classify the proof before assigning severity.

### Confirmed

The repository or a safe reproduction establishes the trigger, path, missing/incorrect control, and consequence. No material assumption remains.

### Strong

The code and repository contracts establish the result, but the behavior was not executed. Language/library semantics are clear and all material guards were inspected.

### Conditional

One explicit runtime or deployment premise cannot be verified, but it is plausible and changes the outcome. State the premise. Conditional findings should be rare and cannot be `CRITICAL`.

### Speculative

The trigger, reachability, control, or impact depends on multiple guesses or an unsupported environment. Do not report it as a finding.

Only Confirmed or Strong candidates are normal findings. Conditional candidates belong in a clearly marked verification section when their potential impact justifies human follow-up.

## Finding eligibility

A candidate is reportable only when all are true:

1. **Introduced or exposed:** the reviewed change creates the defect, removes a control, makes a dormant defect reachable, or violates a newly changed contract.
2. **Reachable:** a concrete actor, input, state, version combination, or workload reaches it.
3. **Incorrect:** behavior conflicts with an invariant, requirement, security boundary, or established contract.
4. **Consequential:** it has an observable impact beyond taste or theoretical purity.
5. **Actionable:** the changed code contains a plausible place to fix or guard it.
6. **Supported:** evidence is Confirmed or Strong, or explicitly Conditional under the rule above.

Do not report a concern merely because best practice is absent.

## Severity model

Severity is determined by:

- impact
- realistic reachability and likelihood
- blast radius
- recoverability
- privilege required
- existing controls

Category names do not determine severity. “Injection,” “race,” “crypto,” or “data loss” can fall at different levels depending on the proven path.

### CRITICAL

Catastrophic and realistically reachable. This rating is exceptional.

All Critical gates below must pass.

Typical impacts:

- unauthenticated or low-privilege remote code execution in a production-reachable service
- systemic authentication or authorization bypass granting broad administrative or cross-tenant control
- broad disclosure of highly sensitive production data or credentials enabling broad compromise
- deterministic, irreversible loss or corruption of primary production data at large scale during a normal operation or rollout
- incorrect high-value financial/signing execution at scale
- reliable total outage of a critical service through a normal deployment or cheap external trigger, with no effective containment

### HIGH

A serious defect on a normal or plausible path that materially compromises security, data integrity, availability, or a core user workflow. Fix before merge.

Typical impacts:

- cross-tenant or unauthorized read/write affecting a bounded resource set
- duplicate charge, order, message, or irreversible side effect under plausible retry/concurrency behavior
- deployment or migration incompatibility likely to cause an outage or failed rollout
- common-path crash, deadlock, or data loss with meaningful blast radius
- reachable injection or SSRF with significant but bounded capability
- broken authentication/session behavior affecting a substantial path

### MEDIUM

A real defect under a specific but realistic condition, with limited blast radius or straightforward recovery. Usually fix before merge unless consciously accepted.

Typical impacts:

- wrong result at a boundary or uncommon state
- recoverable per-user data inconsistency
- localized availability failure
- resource growth that becomes harmful under a plausible but non-default workload
- information exposure of limited sensitivity
- compatibility break affecting an uncommon but supported client

### LOW

A concrete, low-impact defect or robustness problem. Non-blocking by default.

Examples include misleading diagnostics, minor resource leakage on a bounded path, or a failure mode with small and easily recoverable impact.

### SUGGESTION

An improvement, simplification, optional hardening, or style preference rather than a demonstrated defect. Omit by default unless the user requests suggestions.

## Critical gates

Assign `CRITICAL` only when every answer is yes:

1. **Production reachability:** Is the path reachable in the deployed or standard rollout model evidenced by the repository?
2. **Realistic trigger:** Can a normal operation or credible attacker trigger it without implausible access, timing, or resources?
3. **Catastrophic impact:** Is the proven impact broad, systemic, highly sensitive, or irreversibly destructive?
4. **No effective mitigation:** Have relevant authentication, authorization, isolation, validation, rollback, backup, rate limit, and platform controls been checked and found ineffective for this path?
5. **Introduced by change:** Does the reviewed change create or materially expose the condition?
6. **High confidence:** Is the finding Confirmed or Strong with no material unresolved premise?

If any gate fails, use `HIGH` or lower. Do not use Critical to mean “important,” “security-related,” or “should block merge.”

## Security calibration

Use these constraints to prevent category inflation:

- A missing rate limit is not automatically a vulnerability; prove an abuse path and meaningful impact.
- A dependency advisory is not a code-review finding without affected-version evidence and a reachable vulnerable feature or a policy that explicitly blocks it.
- SSRF is not Critical merely because an internal address might exist. Prove reachable sensitive targets, redirect/DNS behavior, credentials, and resulting capability.
- XSS severity depends on who can inject, who renders it, available session/token protections, and the action scope of the victim.
- A hardcoded value is not a secret unless it is sensitive and usable in the relevant environment. A valid broad production credential may be Critical; a documented test fixture is not a finding.
- A crash is not Critical unless it causes a broad, reliable outage with realistic triggering and poor containment.
- “Potential data loss” requires an actual write/delete path and a state in which recovery is absent or materially costly.
- Cryptographic deviations require a violated security property in context, not merely a non-preferred primitive name.
- Client-side permission hiding is not an authorization defect when the server enforces the policy; server-side absence is the relevant issue.

## Downgrade and rejection rules

Downgrade or reject when:

- exploitation requires administrator or local-machine access already equivalent to the outcome
- the path is test-only, dead, feature-disabled, or unreachable in the reviewed deployment
- a caller, middleware, schema, type, database constraint, sandbox, or framework primitive enforces the claimed missing invariant
- impact is confined, reversible, or requires several unlikely simultaneous failures
- the issue predates the target and was not made reachable or worse by it
- the concern is missing defense in depth rather than violation of the current threat model
- the behavior is explicitly required and safe under the repository's contract
- the proposed “fix” would only express a preference

Do not lower confidence and keep high severity. Uncertain evidence must affect reportability or severity.

## Merge guidance

- Any Confirmed/Strong `CRITICAL` or `HIGH`: recommend blocking merge.
- `MEDIUM`: normally request a fix or an explicit risk acceptance.
- `LOW`: non-blocking unless repository policy says otherwise.
- Conditional items: request verification; do not present them as proven blockers.

Severity describes impact and reachability. It is not a measure of reviewer enthusiasm or fix size.
