# Dependencies, CI, and Infrastructure

## Contents

- Dependency changes
- Build and install execution
- CI trust boundaries
- Artifact and cache integrity
- Containers
- Kubernetes and orchestration
- Infrastructure as code and IAM
- Deployment safety
- Verification and calibration

## Dependency changes

Review manifest and lockfile changes together.

Check:

- intended package identity, registry, source, checksum, and version resolution
- unexpected transitive additions or source switches
- git/path/URL dependencies and mutable references
- install/build scripts and native binaries
- optional features that expand runtime capability
- duplicated versions that bypass a security or correctness fix
- lockfile regeneration scope inconsistent with the manifest change
- license/policy constraints only when repository policy defines them

A known advisory requires current, primary-source evidence, affected-version confirmation, and either reachable vulnerable functionality or an explicit policy violation. Do not invent CVEs from memory.

Typosquatting or maintainer compromise claims require package/source evidence, not a similar-looking name alone.

## Build and install execution

Inspect changes that execute code during dependency installation or build:

- package lifecycle scripts, build scripts, macros, generators, plugins
- downloaded tools or binaries
- checksum/signature verification
- shell pipelines that hide intermediate failure
- executing artifacts from writable or untrusted locations
- credentials and network access available during build
- secrets copied into generated files, layers, caches, or client bundles

`curl | shell`-style behavior is a lead; severity depends on transport, pinning, integrity, privilege, and who controls the source.

## CI trust boundaries

Map event source, checked-out code, credentials, permissions, and executed commands.

Check:

- untrusted fork/PR code executing in a context with secrets or write tokens
- privileged event types combined with checkout of attacker-controlled refs
- interpolation of branch names, tags, PR titles, labels, issue text, commit messages, or matrix values into shell
- overly broad job or workflow permissions relative to changed steps
- reusable workflow caller/callee permission assumptions
- environment protection and approval boundaries
- self-hosted runner persistence and repository trust
- artifact/download source identity across workflow runs
- pull-request comments or commands that trigger privileged actions

Do not treat every write permission as Critical. Prove the untrusted path to secret disclosure, repository mutation, release compromise, or runner takeover.

## Artifact and cache integrity

Inspect:

- artifact names and run/repository identity
- checksum/signature/provenance verification
- cache keys that mix trusted and untrusted builds
- restoring executable caches before trust is established
- mutable tags or branch refs for build actions/images
- release asset replacement and version immutability
- generated source or binaries committed without reproducible origin

Cache poisoning is a finding only when a lower-trust producer can write content later consumed with higher privilege.

## Containers

Review Dockerfiles, compose files, and runtime configuration for changed behavior:

- secrets in build arguments, layers, history, environment, or image contents
- base image identity and mutability
- downloads and package installation integrity
- runtime user, capabilities, privilege, host namespaces, devices, sockets, and mounts
- writable executable/config paths
- exposed/listening ports versus actual network publication
- health checks, signal handling, read-only filesystem, and temporary storage where required
- build-context leakage and `.dockerignore` changes

Running as root is not automatically a vulnerability. Show how an application compromise crosses an important boundary or violates the deployment contract.

## Kubernetes and orchestration

Check changes to:

- RBAC verbs/resources/scope and service-account binding
- privileged containers, host namespaces, hostPath, device access, and container-runtime sockets
- service-account token automount and cloud workload identity
- network exposure, ingress authentication, and NetworkPolicy assumptions
- secret/config injection and namespace separation
- admission, security context, capabilities, seccomp, and filesystem settings
- probes, disruption budgets, replicas, rollout strategy, resource limits, and termination behavior
- jobs/hooks/migrations that may execute multiple times

A missing optional hardening setting is not a finding without an evidenced boundary or policy violation.

## Infrastructure as code and IAM

Inspect:

- public network/storage/database exposure
- IAM principal, action, resource, condition, and trust policy
- wildcard permissions in the context of the workload's actual input and boundary
- cross-account/tenant trust and confused-deputy protections
- secret material in state, outputs, logs, or user data
- encryption key policy and deletion/rotation behavior
- destructive replacement, state movement, and import behavior
- default credentials, debug access, and management ports
- drift between modules, variables, and deployed assumptions

Broad IAM is serious when untrusted code or input can exercise it. Privilege alone does not establish exploitability.

## Deployment safety

Trace standard and rollback deployment sequences:

- database expand/migrate/contract compatibility
- old/new binary coexistence
- feature flag and config ordering
- one-time jobs, hooks, and retry/idempotency
- irreversible operations and backup/restore evidence
- readiness before traffic and graceful termination
- rollback compatibility after schema/data changes
- secret/key rotation overlap

Normal-rollout destructive behavior or deterministic total outage may be Critical. A theoretical bad operator sequence not used by repository automation is not.

## Verification

Use repository evidence first: workflow event definitions, permissions, checked-out refs, manifests, lockfiles, deployment charts, IAM trust policies, and rollout scripts. Use approved primary sources for exact platform semantics when needed.

A finding must state the lower-trust producer, higher-trust consumer, available privilege, and concrete compromised asset or operation.

## Severity calibration

- Untrusted PR code obtaining broad production/repository credentials can be Critical when directly exploitable.
- Release artifact or runner compromise is High/Critical based on downstream reach and containment.
- Reachable excessive IAM, public data exposure, or secret-in-image behavior is usually High.
- Mutable pinning or absent provenance alone is generally hardening/policy, not automatically a defect.
- Deployment incompatibility likely to cause outage is High; deterministic broad irreversible destruction on normal deploy may be Critical.
