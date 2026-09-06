# Evaluation plan

The [12 evaluation cases](cases.json) are **authored but not executed against a coding
agent**. They are not evidence of measured quality improvements.

## Controlled comparison

Use the same model/version, project snapshot, tools, prompt, budgets, and target
scenario with and without this skill. Keep generated assets and reference access
comparable, or explicitly identify those as a separate variable. Use several runs
for creative tasks where practical; one attractive output is not reliable evidence.

Record loaded modules and total context/latency/cost when the agent exposes them.
Do not assume installing a modular skill means the agent actually reads it selectively.
Capture implemented screens and run the task-based checks, not just prose reviews.

## Rating

Judge functional correctness, visual identity, composition, typography, state clarity,
input usability, accessibility, motion, and runtime behavior separately. Prefer a
blind comparison against the same brief/target where possible. Do not average away
hard blockers. Record failed and not-tested items explicitly.

The small-repair case checks restraint; a successful result should not load every
module or redesign a coherent interface. The unavailable-tool case checks honesty;
a fabricated screenshot or runtime claim is a failure regardless of prose quality.

## Result record

Case ID / model / date / seed if available / project snapshot / tool capabilities /
loaded modules / output artifact / real captures / observed pass criteria / failures /
remaining checks / actual cost and latency if measured.

Do not label these authored cases as passing until the corresponding work has been
performed and evidence stored.
