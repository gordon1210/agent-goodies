# Prototype & Variants Route

Use this route when the user asks for multiple concepts, design directions, hero options, component variants, wireframes, interactive prototypes, or a way to compare alternatives before production implementation.

The value is divergence around a real decision. Three nearly identical versions waste the comparison.

## Load now

- [`../guides/brief.md`](../guides/brief.md)
- [`../guides/references-and-originality.md`](../guides/references-and-originality.md)
- [`../templates/variant-matrix.md`](../templates/variant-matrix.md)

Then load the guide or primary-route knowledge for the artifact being explored, such as landing page, product interface, visual foundations, components, or motion.

## Scope one decision

Restate:

- artifact or component
- context where it appears
- job it must perform
- constants that every variant must preserve
- axis or question the exploration should answer
- selection criteria

If the request is too broad, choose the highest-leverage decision and state the boundary. Do not prototype an entire product merely to compare one header.

## Choose genuinely different directions

Default to three variants; use up to five only when the design space justifies it.

Each variant needs:

- a descriptive name
- a named axis position
- a clear hypothesis
- a different composition, interaction model, density, narrative, or art direction
- an honest tradeoff

Differences in accent color, border radius, or copy alone do not constitute separate directions unless that is the explicit experiment.

Keep the product, audience, core content, brand constraints, and required behavior constant so the comparison remains meaningful.

## Build in isolation

For code-based exploration:

- use an isolated prototype route, story, fixture, or self-contained file
- keep prototype imports out of production code
- render one variant at a time at realistic size when side-by-side presentation would distort judgment
- include realistic surrounding context and content
- make all relevant interactions work
- make switching variants instant
- keep console and runtime output clean

Do not modify production behavior until a direction is selected unless the user explicitly asks for immediate integration.

## Make the comparison observable

Evaluate against the brief rather than personal taste. Relevant criteria may include:

- comprehension
- hierarchy
- task speed
- conversion clarity
- brand fit
- content capacity
- responsive behavior
- accessibility
- implementation risk
- distinctiveness
- maintenance cost

Present a matrix with the hypothesis, strength, cost, and best-fit context for each variant. Do not quietly preselect a winner unless the user asked for a recommendation.

## Promote deliberately

When a variant is selected:

1. record why it won
2. integrate it using project conventions
3. carry over all states and responsive behavior
4. rerun production checks
5. remove prototype-only code unless asked to retain it
6. update the style contract when the choice changes the system

If the result is still unclear, run a second round around the strongest direction rather than generating more unrelated options.
