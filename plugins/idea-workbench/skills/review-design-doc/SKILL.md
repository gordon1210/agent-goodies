---
name: review-design-doc
description: Evaluate an existing product or technical design document for comprehension, consistency, risk coverage, and implementation readiness. Use before approval or implementation planning, after substantial design changes, or when a team needs an independent critique that exposes missing decisions, contradictions, unsupported assumptions, unsafe failure modes, and verification gaps without rewriting the source by default.
---

# Review a Design Doc

Judge whether a capable reader can safely act on the document as written. Treat the review as read-only unless the user explicitly asks to revise the source.

## Preserve a fresh-reader view

1. Read the design document before reconstructing intent from surrounding conversation.
2. Summarize the problem, chosen direction, boundaries, and validation approach using only what the document communicates.
3. Record ambiguities rather than silently resolving them from your own knowledge.
4. Then read linked briefs, research, decision records, and relevant project material to verify alignment and factual claims.
5. Label any inference that is not stated or evidenced by the source.

## Set the review depth

Classify the design as low, medium, or high risk using reversibility, blast radius, novelty, data sensitivity, migration difficulty, external dependencies, and operational burden. Review proportionally, but always examine the core decision, boundaries, behavior, uncertainty, and validation.

Read [review-method.md](references/review-method.md) before performing the detailed review. Use its coverage lenses, severity definitions, and verdict rules.

## Review in two passes

### Test comprehension

Act as a capable implementer who was absent from prior discussions. Determine whether the document makes the following clear without guesswork:

- The problem, desired outcome, scope, and non-goals.
- The chosen direction, rejected alternatives, and accepted trade-offs.
- The important flows, boundaries, contracts, state changes, and ownership.
- The assumptions and open decisions that remain.
- The evidence that will demonstrate success and safe delivery.

### Challenge the design

Try to make the proposal fail. Walk realistic success, failure, recovery, misuse, migration, concurrency, and boundary scenarios through it. Look for contradictions across sections and linked artifacts, hidden dependencies, unsupported claims, irreversible steps, unowned operational work, and validation that proves only the happy path.

Do not manufacture issues to appear thorough. Prefer a few consequential findings over a catalogue of stylistic preferences.

## Report actionable findings

Copy and adapt [design-review-template.md](assets/design-review-template.md). For every finding:

- Assign a stable identifier and severity.
- Point to the relevant section or state that the material is absent.
- State the evidence, not merely a conclusion.
- Explain the credible impact or failure scenario.
- Describe the decision, evidence, or clarification needed to resolve it without prescribing unnecessary implementation detail.

Separate blockers from improvements. Do not downgrade a missing core decision because a likely answer seems obvious, and do not elevate a wording preference into a delivery risk.

## Give an explicit verdict

Choose exactly one verdict using the rules in the review method:

- **Ready:** Safe to proceed to implementation planning.
- **Ready with follow-ups:** Safe to plan only under the listed, bounded conditions.
- **Not ready:** Requires design decisions or evidence before planning can proceed responsibly.

State the verdict first, justify it briefly, and list any conditions. If no actionable findings remain, say so and name the residual risks or untested areas instead of implying certainty.

Apply the approval gate after the verdict:

- For **Ready**, ask the user to approve the reviewed design for implementation planning or request revisions.
- For **Ready with follow-ups**, ask the user to accept the listed conditions explicitly before treating the design as approved.
- For **Not ready**, do not ask for planning approval; recommend the smallest design revision or evidence-gathering step that addresses the blocking findings.

Record approval only when the user states it explicitly. A positive verdict,
silence, or agreement with one finding is not approval.

Present the review separately from the source document. Stop after the verdict,
findings, and approval request: do not edit the design, create an implementation
plan, or begin implementation unless the user explicitly asks for that
additional work.
