# Skill Evaluations

These cases test the skill's most important property: high recall for consequential defects without manufacturing findings from dangerous-looking syntax.

## How to run

1. Present one case from `cases.md` to a coding agent with this skill installed.
2. Ask for a change-scoped review and no code modifications.
3. Compare the result with the expected outcome and severity.
4. Repeat with each model/client you intend to use.

Use a clean context for each case. For realistic evaluation, implement the snippets in small repositories with callers, tests, and configuration matching the stated facts.

## Acceptance criteria

The skill should:

- report every positive case with the stated root cause
- avoid findings in negative cases
- keep `CRITICAL` limited to cases that pass all Critical gates
- identify unresolved premises as verification needs, not facts
- anchor findings to the changed cause
- separate pre-existing defects
- avoid “add tests,” style, and generic hardening comments

Precision is the primary gate. A review system that flags everything trains maintainers to ignore it.

## Regression use

When editing the skill:

- add a positive case for every missed consequential defect
- add a negative case for every false positive
- keep paired cases where similar syntax has different reachability or controls
- test severity separately from detection
