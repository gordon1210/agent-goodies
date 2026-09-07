# Page route: working web applications

**Load when:** designing dashboards, operational tools, settings, or repeated task flows.

## Task clarity is the aesthetic foundation

Identify the primary repeated task, relevant state, and failure cost. Preserve the
existing product's interaction vocabulary. A design refresh should improve scanning,
selection, correction, and confidence—not turn a table into a cinematic landing page.

Define hierarchy at the page, panel, row, and field level. Use consistent alignment
and density. Comparable values should remain comparable; tables are not obsolete
because cards look more decorative. Charts need labels, units, context, and truthful
data. Distinguish zero, missing, stale, loading, and error rather than showing all as a dash.

## States and information architecture

Design empty, loading, partial, error, unauthorized, unavailable, and success states
where relevant. Explain what users can do next. Skeletons or spinners represent real
work only. Do not invent a progress percentage for an operation that cannot report one.
For optimistic updates, follow the application's actual rollback/error model.

Keep primary actions near their context. Reserve destructive emphasis for real
risk and preserve confirmation or undo flows already specified by the product.
Do not replace labeled actions with mysterious icons to appear minimal.

## Interaction detail

Menus, tabs, dialogs, and forms should reuse proven accessible primitives. Preserve
focus through updates. Sorting, filtering, pagination, and selection should keep a
predictable relationship to navigation state. Review keyboard operation and touch,
not just pointer hover. Do not put all controls behind hover in dense rows.

Motion should explain a change or acknowledge an action. Avoid animated counters,
per-row entrance staggers, continuous background shaders, and long route ceremonies
for frequently repeated work. Decorative effects are optional and secondary.

## Acceptance

Test realistic data volume, long labels, empty results, partial access, slow and
failed requests, rapid edits, and recovery. Verify color-independent state meaning,
tab order, focused item visibility, and small-screen access to secondary actions.

A visual review is not a security audit. Preserve authentication and authorization
behavior, and escalate underlying logic issues instead of silently rewriting them
under a styling task.

## Sources

[Emil Kowalski: You Don’t Need Animations](https://emilkowal.ski/ui/you-dont-need-animations).
