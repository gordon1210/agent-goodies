---
name: explore-options
description: Generate and compare credible solution directions for an approved idea brief, then produce an evidence-aware recommendation and decision record. Use when the problem and boundaries are understood but the solution is not chosen, when a team is converging too quickly on one approach, or when a proposed direction needs alternatives and tradeoffs made explicit before design work.
---

# Explore Solution Options

Compare genuinely different ways to achieve the same outcome before committing to a design. Stay at solution-direction level; do not turn the chosen direction into a detailed design or implementation plan.

## Establish the decision frame

- Inspect the conversation, repository, current system, and existing artifacts first. Locate the approved idea brief when one exists.
- Confirm the decision question, desired outcome, appetite, boundaries, constraints, and non-goals. If any of these are too weak to compare options honestly, stop and recommend `shape-idea`.
- Derive evaluation criteria from the brief instead of applying a generic scorecard. Ask one high-leverage question at a time when a priority or tradeoff belongs to the user; include a recommendation with the question.
- Keep facts, assumptions, hypotheses, decisions, and open questions separate. Investigate accessible facts rather than asking the user to recall them.

## Build credible options

1. Produce two to four meaningfully different directions. Vary the primary mechanism, boundary, ownership, or risk profile—not just implementation details.
2. Include a simpler, reuse-first, integration, or unchanged-state option when it is genuinely credible.
3. Give every option enough detail to understand its rough user flow or system shape, dependencies, operating burden, reversibility, and main risks.
4. Avoid straw alternatives. If fewer than two honest options survive, explain why and ask the user whether to proceed rather than inventing a foil.

## Compare and recommend

Read [references/evaluation.md](references/evaluation.md) before evaluating the options.

- Support factual claims with repository evidence or primary sources where available.
- Compare options against the same criteria and constraints. Prefer explained qualitative judgments to false numerical precision.
- Identify assumptions and hypotheses that could reverse the ranking. Resolve cheap factual unknowns; propose a focused investigation for unresolved empirical questions.
- Recommend one coherent direction. State the decisive tradeoff, strongest argument against it, why the other options are not preferred now, and what future evidence would change the recommendation.
- Copy and complete [assets/options-template.md](assets/options-template.md). Remove unused guidance rather than padding the document.

## Apply the decision gate

- If framing, evidence, or a decision-critical unknown is blocking an honest recommendation, keep the status `Draft`, name the blocker, and ask only the next question needed.
- If the comparison is sound, set the status to `Ready for decision`, present the complete artifact, and ask the user to select, revise, or reject the recommendation.
- After an explicit selection, record the rationale and set the status to `Chosen`.

**Hard stop:** Do not write the design doc, prototype the full solution, or plan implementation until the user explicitly chooses a direction. After selection, recommend `write-design-doc` as the next stage without starting it automatically.
