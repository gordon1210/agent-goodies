---
name: deep-code-review
description: Performs deep, evidence-driven reviews of pull requests, commits, diffs, patches, and working-tree changes. Use for code review, security review of code changes, regression hunting, or merge-risk assessment when the goal is to find real bugs with minimal false positives. Traces changed behavior through callers, state, data flows, trust boundaries, tests, configuration, and deployment contracts while loading only relevant reference modules.
license: MIT
metadata:
  version: "1.0.0"
  compatibility: Portable across Agent Skills clients. Requires read access to the reviewed code; git and project-specific validation tools are optional.
---

# Deep Code Review

Find actionable defects introduced or materially exposed by the reviewed change. Review behavior, not aesthetics. Remain read-only unless the user explicitly asks for fixes.

## Start here

Before analyzing findings, read:

1. [Core review method](references/core-method.md)
2. [Evidence and severity](references/severity-evidence.md)

At reporting time, read [output format](references/output-format.md).

Do not load every reference. Build a change map first, then open only the modules selected by the routing table. Multiple modules may apply.

## Routing

| Change signal | Load |
|---|---|
| Any executable behavior | [Correctness](references/correctness.md) and [Security triage](references/security-triage.md) |
| Authentication, sessions, roles, permissions, ownership, tenant boundaries, admin paths | [Authorization and tenancy](references/security-authz-tenancy.md) |
| Request parsing, queries, templates, HTML, commands, expressions, deserialization, uploads, paths | [Untrusted input and execution](references/security-input-execution.md) |
| Personal/sensitive data, credentials, tokens, logging, encryption, signatures, randomness | [Data, secrets, and cryptography](references/security-data-secrets-crypto.md) |
| URLs, HTTP clients, redirects, webhooks, files, archives, temporary files, child processes | [Network, files, and processes](references/security-network-files-processes.md) |
| Dependencies, lockfiles, CI, release scripts, containers, Kubernetes, Terraform, cloud IAM | [Dependencies, CI, and infrastructure](references/security-dependencies-ci-infra.md) |
| LLMs, agents, RAG, MCP, tools, memory, model-generated actions | [AI and agent security](references/security-ai-agents.md) |
| C/C++, unsafe code, FFI, binary parsing, manual allocation | [Native memory safety](references/native-memory-safety.md) |
| Database/schema changes, transactions, caches, queues, retries, async state, locks, parallelism | [Data, state, and concurrency](references/data-state-concurrency.md) |
| Public APIs, events, schemas, serialization, CLI flags, configuration contracts, rolling deploys | [Contracts and compatibility](references/contracts-compatibility.md) |
| Timeouts, retries, shutdown, backpressure, resource use, hot paths, large inputs | [Reliability and performance](references/reliability-performance.md) |
| Browser UI, forms, client state, SSR/hydration, browser storage | [Frontend and browser](references/frontend-browser.md) |
| Tests, fixtures, mocks, snapshots, or validation commands changed | [Tests and validation](references/tests-validation.md) |
| New abstraction, broad refactor, ownership/layering change, duplicated policy | [Design and maintainability](references/design-maintainability.md) |
| TypeScript or JavaScript | [TypeScript and JavaScript](references/language-typescript-javascript.md) |
| Rust | [Rust](references/language-rust.md) |
| Go | [Go](references/language-go.md) |
| Python | [Python](references/language-python.md) |

Language modules supplement domain modules; they never replace them. Route by behavior, not filename alone.

Use [calibration examples](references/calibration-examples.md) only when deciding whether a candidate is real or how severe it is.

## Non-negotiable rules

- Honor repository-local instructions and the stated requirements before applying generic advice.
- Inspect the diff plus enough surrounding code to understand callers, callees, guards, state, configuration, and rollout behavior.
- Report only issues introduced by the target change unless the user asks for a full audit. Clearly separate pre-existing issues when requested.
- For every candidate, actively search for evidence that disproves it: upstream validation, middleware, type or framework guarantees, compensating controls, unreachable paths, or tests.
- A missing test is not itself a product bug. A style preference is not a finding. A theoretical weakness without a realistic trigger is not a finding.
- Security findings require a source-to-sink or source-to-decision path, an attacker or trust-boundary model, and a concrete impact.
- Performance findings require a hot or scalable path and a plausible workload. Do not report micro-optimizations.
- Never inflate severity because a category sounds dangerous. Apply the gates in `severity-evidence.md` literally.
- Deduplicate by root cause. Prefer one precise finding over several symptoms.
- Do not install dependencies, run migrations, deploy, push, commit, or mutate external systems. Run existing validation only when it is clearly safe and permitted; disclose what was not run.
- If evidence is insufficient, state the unresolved assumption as a verification note or omit the candidate. Never fabricate certainty.

## Completion condition

A review is complete when each changed behavior and boundary has been traced, selected modules have been applied, all surviving candidates have passed the disproof and severity gates, and validation limits are recorded.
