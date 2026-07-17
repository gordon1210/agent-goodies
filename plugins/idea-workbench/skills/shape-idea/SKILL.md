---
name: shape-idea
description: Turn a rough product, feature, workflow, or system vision into a grounded, decision-ready idea brief by clarifying the problem, outcome, evidence, appetite, boundaries, constraints, risks, and unknowns. Use when an idea is fuzzy, oversized, solution-first, or missing the shared context needed to compare approaches or write a design doc.
---

# Shape an Idea

Create shared understanding before exploring solutions. Keep the work at problem-and-scope level; do not design the system or plan its implementation.

## Work with the user

- Inspect the conversation, repository, existing product behavior, and nearby documents before asking anything. Resolve accessible factual questions yourself and cite their sources in the brief.
- Ask one high-leverage question at a time. When asking for a choice, give a recommendation and its main tradeoff.
- Ask the user for judgments and priorities, not facts available in the working context. Never make a product or scope decision silently.
- Scale the depth to the idea. Preserve useful ambiguity while the idea is young, but make every uncertainty visible.
- Keep facts, assumptions, hypotheses, decisions, and open questions separate. Do not promote one category into another without new evidence or explicit agreement.

## Classify the project context

Classify the work before shaping its boundaries:

- **Greenfield:** No implementation baseline exists. Treat proposed platforms,
  structure, and conventions as choices or assumptions rather than facts.
- **Existing system:** The idea changes a running product or established
  codebase. Ground the brief in current behavior, constraints, integration
  points, and behavior that must be preserved.
- **Hybrid:** A new component or product must connect to an existing system.
  State which side is new, which side is established, and where the seam lies.

Do not infer `Greenfield` merely because a repository is unavailable. Use
`Unclear` when the evidence is insufficient and resolve the classification only
when it could change scope, constraints, or the next decision. Carry the
classification and its evidence into the brief.

## Shape the brief

1. **Ground the idea.** Summarize the starting vision and inspect relevant context. Record what is known, where it came from, and what remains uncertain.
2. **Find the problem.** Identify who is affected, what happens today, what evidence supports the problem, why it matters now, and what a better outcome would change. Reframe a proposed feature as a problem when necessary.
3. **Choose a meaningful slice.** Define the smallest coherent scope that can create or test value. If the idea is a grab-bag, propose smaller slices and ask the user which one to shape.
4. **Set appetite and boundaries.** Capture the acceptable investment and risk, in-scope behavior, non-goals, constraints, and behavior that must be preserved.
5. **Expose uncertainty.** Record assumptions, falsifiable hypotheses, risks, rabbit holes, and open questions. Investigate cheap factual unknowns from available context; describe evidence needed for hypotheses.
6. **Make success observable.** State outcome signals that could show whether the idea helped without pretending that early targets are proven facts.
7. **Write the artifact.** Copy and complete [assets/idea-brief-template.md](assets/idea-brief-template.md). Remove unused guidance rather than inventing content.

## Apply the readiness gate

Read [references/readiness.md](references/readiness.md) before declaring the brief ready.

- If a blocking item is missing, keep the status `Draft`, name the blocker, and ask only the next question needed to resolve it.
- If the gate passes, set the status to `Ready for approval`, present the complete brief, and ask the user to approve or revise it.
- After explicit approval, record the approval and set the status to `Approved`.

**Hard stop:** Do not explore solution options, write a design doc, or plan implementation until the user explicitly approves the written brief. After approval, recommend `explore-options` as the next stage without starting it automatically.
