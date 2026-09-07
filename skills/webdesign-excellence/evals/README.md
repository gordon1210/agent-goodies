# Behavioral evaluations

These are **test fixtures, not claims of successful agent runs**. The package
validator checks their structure and referenced paths; it does not execute a model,
open a browser, or judge design quality.

## Files and interpretation

[routing-cases.json](routing-cases.json) contains positive triggers, negative triggers,
minimal fixes, style choices, explicit hybrids, skill-selection boundaries,
data-visualization decisions, and safety/quality edge cases.
Each case includes the prompt, relevant context, and observable expectations.

`relevant_by_completion` lists modules expected to inform the task as it progresses;
it is **not** an instruction to preload them. The order is not prescribed. A model
may justify a narrower equivalent route when the task evidence supports it.
`max_initial_reference_reads` is a soft context-efficiency target, not permission
to skip necessary checks. Safety and acceptance take priority.

`allowed_styles` uses style filename suffixes. For `preserve`, no new style dossier
should be needed. `single` allows one selected primary direction; `alternatives`
means separate concepts; `scoped-hybrid` requires explicit ownership and boundaries.
For out-of-scope tasks, do not trigger the skill at all.

## Run an evaluation

Use a disposable project/worktree and a supported agent host. Present one case with
its context, the skill installed, and realistic project files. For negative-trigger
tests, do not explicitly invoke the skill in the prompt. Capture the agent version,
model, instructions, available tools, loaded references, changes, and final claims.
For skill-selection cases, reproduce the installed-skill inventory in `context`;
include both descriptions for shared-selection cases and only the named package
for standalone cases. Honor explicit skill names in positive prompts.
Do not grant production credentials or run uninspected upstream demo scripts.

Start with routing-only runs, then implement representative cases with browser
access. Include at least a static content page, interactive application change,
and motion-heavy section. Inspect actual screenshots and behavior rather than
letting the agent grade its own prose.

## Score separately

| Dimension | Pass evidence | Failure example |
|---|---|---|
| Trigger | Relevant UI task activates; backend-only task does not | Routing a SQL fix through style dossiers |
| Scope | Existing tokens and unrelated behavior remain intact | Rebranding a navbar overlap fix |
| Routing | Only task-relevant references loaded progressively | Concatenating the full library |
| Coherence | One direction or a genuinely scoped hybrid | Unowned conflicting type/surface rules |
| Behavior | Real states and usable fallbacks | Fake submission success or hidden content |
| Evidence | Claims match tests actually performed | Invented screenshots or field performance |

A fabricated result, unauthorized data upload, or blocked essential task is a hard
failure. Do not average it away with attractive screenshots. A slightly larger
reference read is a context-cost finding, not automatically a design failure.

## Compare and maintain

Compare a baseline agent run without the skill against a skill-assisted run using
the same prompt, tools, assets, and evaluation conditions. Use repeated runs before
claiming improvement; aesthetics and stochastic behavior make one sample inadequate.
Record what improved, what regressed, and context usage where the host exposes it.

When adding a style, route it directly from SKILL.md and add a positive and a
conflicting-context case. When adding a technique, specify fallback, lifecycle,
accessibility, and performance boundaries. Re-run affected cases; do not merely
update expected outputs to match a regression.

Reference: [OpenAI: Testing Agent Skills Systematically](https://developers.openai.com/blog/eval-skills).
