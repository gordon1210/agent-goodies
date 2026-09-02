# Tests and Validation

## Contents

- Tests as evidence
- Changed-test review
- Missing coverage
- Mocks and fixtures
- Flakiness and determinism
- Safe command execution
- Interpreting results

## Tests as evidence

Use tests to answer concrete review questions:

- What behavior is promised?
- Which boundary cases are intentional?
- Does a candidate reproduce?
- Does the test exercise the changed production path?
- Does the assertion prove the invariant or only implementation detail?

Passing tests do not disprove a path they never execute. Failing tests require causal analysis.

## Changed-test review

Inspect whether the change:

- deletes or weakens an assertion
- broadens a matcher enough to accept incorrect output
- updates expected output to match a regression without changed requirements
- mocks the exact code whose integration needs validation
- stops awaiting async work
- catches/retries an assertion until it passes
- skips, focuses, quarantines, or marks expected failure
- changes fixtures so the dangerous state is no longer represented
- snapshots unstable or irrelevant output while missing the key property
- asserts only that no exception occurred
- tests a helper instead of the public behavior
- uses a different configuration/path than production

A test change can be the changed cause of a regression even when production code is unchanged.

## Missing coverage

Do not report “missing test” as a product defect by default.

It may be a separate process finding only when:

- repository policy explicitly requires a test for this class of change
- the task explicitly requires regression coverage
- a critical invariant has no practical validation and the review cannot establish correctness statically
- the change removes existing coverage

Even then, state the unverified behavior rather than inventing a bug.

## Mocks and fixtures

Check:

- mock contract matches the real dependency's return, error, retry, and ordering behavior
- fixtures satisfy realistic constraints and tenant/auth context
- generated IDs/timestamps do not hide collisions or boundaries
- in-memory database differs in transactions, constraints, collation, or concurrency
- fake clock advances all relevant timers and monotonic/wall-clock behavior
- network mocks test headers/body/status and not merely call count
- mock assertions do not couple harmless implementation details
- shared mutable fixtures do not leak across tests
- cleanup restores global state, environment, files, ports, and handlers

## Flakiness and determinism

Inspect changed tests for:

- sleeps instead of waiting on an observable condition
- real wall clock, timezone, locale, randomness, network, or external service
- order dependence and shared state
- data races or ports/files with global names
- assertions before asynchronous work settles
- retries that conceal deterministic failure
- exact timing thresholds with no margin
- unordered collection comparison through ordered snapshots

A potentially flaky pattern is reportable when a plausible interleaving/environment causes false pass/fail and the changed test matters to CI signal.

## Safe command execution

Use existing repository commands when clearly safe and permitted.

Prefer focused scope first:

1. test directly covering changed behavior
2. package/module test
3. typecheck/static analyzer
4. broader suite if cost and environment are reasonable

Do not:

- install or update dependencies
- mutate lockfiles
- run migrations against shared databases
- invoke production/cloud resources
- publish, deploy, push, or release
- execute untrusted build/test scripts with secrets or elevated privilege

Follow repository instructions. Report commands and relevant results exactly.

## Interpreting results

Classify failures:

- **Change-caused:** trace from changed code/test to failure
- **Pre-existing:** reproduce on base or evidence clearly predates change
- **Environment:** missing service/tool/config/platform capability
- **Flaky/unknown:** non-deterministic or not enough evidence

Do not turn an environment error into a code finding. Do not claim “all tests pass” when only a subset ran.

## Validation note

The final review should state:

- commands run
- scope of tests
- pass/fail result
- failures not attributed to the change
- relevant validation not run and why
