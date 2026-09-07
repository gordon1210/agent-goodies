# Critique: diagnose before restyling

**Load when:** reviewing a design, comparing alternatives, or responding to “this does not look modern.”

## Establish the reference and scope

Inspect the supplied design or running page. If only code or a written prompt is
available, state that the visual result has not been seen. Identify the audience,
task, intended direction, and any existing brand constraints. Do not judge a
working application by the criteria of a cinematic portfolio.

## Review in the right order

| Lens | Question | Useful evidence |
|---|---|---|
| Task | Can the user understand and complete the main job? | Flow, content, real states |
| Composition | Is there a controlled focal hierarchy? | Full-page and viewport screenshots |
| Type | Do roles, measure, wrapping, and scale work? | Real copy at several widths |
| Identity | Do choices form one coherent visual system? | Repeated tokens and image direction |
| Interaction | Does motion or feedback clarify a change? | Actual keyboard/touch/pointer behavior |
| Robustness | Does it survive realistic constraints? | Zoom, loading, errors, preferences, profiling |

Do not average away a blocked task with a high visual score. A trend label is not
a finding. Glass, cards, gradients, or serif type are not automatically defects.
Specify what the treatment does wrong in this context.

## Write actionable findings

For each important issue, give the location, observable problem, user/design impact,
and smallest useful correction. Label hypotheses as hypotheses. Distinguish actual
breakage from art-direction preference and polish. Prioritize blocked access or
false information, then major comprehension issues, then consistency and detail.

Weak: “Looks dated; use bento and add motion.”
Strong: “The price, title, and purchase action compete at the same weight. Reduce
the metadata emphasis, group price with the action, and align the gallery to that
block. Preserve the existing palette and verify at 390px.”

## Repair loop

Keep the direction fixed while correcting the largest failure. Re-render and compare
under the same conditions. Change a small coherent set of variables so the result
can be attributed to a decision. Do not simultaneously replace fonts, colors,
layout, assets, and motion unless the task is an approved redesign.

Use a static-first critique. If the design depends on a recording to appear polished,
check its resting state and loading state. Do not claim a screenshot confirms
keyboard operation, reduced motion, performance, or conversion improvement.

**Exit:** a short prioritized diagnosis with evidence and concrete changes—not a
new style dossier unless the existing direction is actually the problem.
