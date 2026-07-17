---
name: write-design-doc
description: Turn an approved idea brief, selected solution direction, or established product and technical context into a risk-scaled design document. Use when a direction has been chosen and implementation needs concrete boundaries, flows, interfaces, data behavior, failure handling, validation, and delivery decisions, or when an existing draft needs to become ready for independent review and planning.
---

# Write a Design Doc

Create the smallest design document that lets a reviewer understand the decision and lets a planner proceed without inventing core behavior.

## Establish the design basis

1. Read the conversation, linked briefs, research, decision records, and relevant project material.
2. Synthesize settled context. Do not restart the discovery interview or ask the user to repeat information already available.
3. Inspect the existing system where the proposal must fit. Confirm paths, interfaces, constraints, and conventions before relying on them.
4. Confirm the project context and design accordingly:
   - **Greenfield:** Distinguish proposed foundations from observed facts and
     settle the platform, structure, ownership, and bootstrap decisions needed
     for planning.
   - **Existing system:** Make current behavior, integration points,
     conventions, compatibility, migration, and preserved behavior explicit.
   - **Hybrid:** Define the new and existing sides separately, then make their
     boundary, contract, ownership, and failure behavior concrete.
   Do not infer `Greenfield` from missing repository access alone.
5. Separate the input into:
   - **Known facts:** supported by evidence.
   - **Decisions:** choices already made, with their rationale.
   - **Assumptions:** beliefs that still require validation and the consequence if wrong.
   - **Open questions:** unresolved choices, marked as blocking or non-blocking.
6. Investigate discoverable facts directly. Ask the user only for consequential decisions that cannot be inferred safely.

## Scale the depth to risk

Classify the change as low, medium, or high risk using reversibility, blast radius, novelty, data sensitivity, migration difficulty, external dependencies, and operational burden. State the classification and why it applies.

Read [design-coverage.md](references/design-coverage.md) to select the concerns that deserve treatment. Cover every core concern, then add conditional concerns in proportion to risk. Do not inflate a local, reversible change into an architecture treatise, and do not compress an irreversible change into a happy-path sketch.

## Draft the document

Copy and adapt [design-doc-template.md](assets/design-doc-template.md). Preserve an established project template when one exists, while ensuring the same decisions remain visible.

Write for a capable reader who was not part of the conversation:

- Define the problem, desired outcome, scope, and non-goals before describing mechanics.
- Record the chosen direction and the meaningful alternatives rejected.
- Make boundaries, ownership, user and system flows, interfaces, data behavior, and failure recovery concrete where applicable.
- Explain why each material choice fits the constraints and what trade-off it accepts.
- Use diagrams, examples, or pseudocode only when they remove ambiguity.
- Cite evidence for externally verifiable claims. Do not present guesses as facts.
- Prefer stable responsibilities and contracts over speculative file lists or implementation code.
- Record risks, rabbit holes, mitigations, rollout, rollback, and verification at the depth warranted by the risk classification.

## Test the design on paper

Walk representative success, failure, recovery, and boundary scenarios through the proposed design. Check that each stated goal has observable evidence of success and that each important constraint is reflected in a decision. Surface contradictions instead of smoothing them over.

## Declare readiness

Mark the document **ready for review** only when:

- The problem, outcome, scope, and non-goals agree with the established brief.
- The chosen direction and its consequential trade-offs are explicit.
- Critical flows, boundaries, contracts, data changes, and failure behavior are concrete enough for the assessed risk.
- Assumptions include validation actions, and open questions identify their impact and next decision-maker.
- Validation, rollout, recovery, and ownership are credible where applicable.
- A planner can decompose the work without inventing product behavior or architectural choices.

Otherwise mark it **not ready**, name the blocking decisions or evidence, and recommend the smallest next action.

Present the completed document and readiness result. Ask the user to accept it
as ready for independent review or request revisions. Stop there: do not review
the document, create an implementation plan, or begin implementation unless the
user separately asks for that work.
