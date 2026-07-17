---
name: develop-idea
description: Route an idea through the idea-workbench workflow by assessing its current maturity and recommending the single next skill. Use when a user has a vision, brief, options note, design doc, review, or implementation plan but is unsure what to do next, or asks for help taking an idea from concept toward implementation.
---

# Develop Idea

Act only as a router. Inspect the available context, identify the earliest unmet
gate, and recommend one next skill. Do not create or edit an artifact, perform
the recommended work, or invoke another skill.

## Assess maturity

1. Inspect the conversation and existing project artifacts only far enough to
   identify the latest decisions and their approval status.
2. Judge substance rather than filenames. Treat an artifact as approved only
   when the user has explicitly approved it.
3. Select the earliest unmet gate in this canonical flow:

| Gate | Evidence required | Recommend |
| --- | --- | --- |
| Frame the idea | Clear problem, intended outcome, affected people, appetite, boundaries, and important unknowns | `shape-idea` |
| Choose a direction | Credible alternatives, tradeoffs, evidence, and a reasoned choice | `explore-options` |
| Define the design | Chosen approach developed into an implementation-oriented design with relevant boundaries, interfaces, data, risks, and verification strategy | `write-design-doc` |
| Validate the design | Design reviewed for ambiguity, coverage, consistency, feasibility, and risk, then explicitly approved | `review-design-doc` |
| Prepare the work | Approved design decomposed into traceable, ordered, independently verifiable slices | `plan-implementation` |

If an approved implementation plan already exists, state that the workflow is
complete instead of inventing another step.

## Add a bounded detour when needed

Attach at most one detour to the recommendation when a high-impact uncertainty
would make the next artifact speculative:

- Recommend a research detour for a factual question that can be settled with
  existing evidence, documentation, project inspection, or user data.
- Recommend a disposable prototype detour for behavior, usability, performance,
  or integration uncertainty that is cheaper to test than to debate.

State the exact question and the evidence that would end the detour. Keep it
inside the selected stage, record the result in that stage's artifact, and then
resume the canonical flow. Do not turn a detour into a permanent extra stage.

## Return the recommendation

Return only:

- the current maturity stage;
- the evidence used to classify it;
- one recommended next skill, or `workflow complete`;
- a short reason;
- the artifact or context to carry forward; and
- the bounded detour, only when one is necessary.

Stop after the recommendation. Let the user decide whether to continue.
