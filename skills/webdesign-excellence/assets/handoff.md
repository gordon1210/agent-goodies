# Design implementation handoff

Use when the task benefits from a written handoff. Keep only relevant headings.
Never turn this template into an assertion that unperformed checks passed.

## Changed

[Specific components, routes, styles, and behavior changed. Mention preserved scope.]

## Design decisions

[Primary direction or existing system; composition; type roles; selected techniques.]
[Why each non-obvious effect exists and what was deliberately excluded.]

## Evidence

| Check | Method / environment | Result | Evidence or limitation |
|---|---|---|---|
| Build / static checks | [Exact commands] | [Pass / fail / not run] | [Output or scope] |
| Layout | [Actual widths and content] | [Observed result] | [Screenshot when captured] |
| Operation | [Keyboard and main flow] | [Observed result] | [States covered] |
| Preferences | [Reduced motion / relevant others] | [Observed result] | [Fallback inspected] |
| Performance | [Real measurement conditions] | [Observed result] | [Lab or field; never conflate] |

Delete irrelevant rows. Add supported browsers, assistive technology, or repeated
navigation checks only when they were actually exercised.

## Assets and dependencies

[New assets and their rights/provenance; fonts; approved dependencies; external requests.]
[State explicitly when no new dependency or external request was introduced.]

## Remaining limitations

[Unverified behavior, missing content, known defects, and exact remaining approval.]
[Do not hide blockers behind the phrase “production ready.”]
