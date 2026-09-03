# Validation, Browser QA & Handoff

Use this guide before declaring substantial visual or interaction work complete.

Verification is evidence, not confidence.

## Build an acceptance matrix

Derive gates from the user's request and project constraints:

| Gate | Method | Pass condition | Evidence |
| --- | --- | --- | --- |
| Requirement | Inspection, test, render, measurement, or comparison | Observable result | Command, screenshot, trace, source location |

Use only relevant gates. Prefer binary conditions to vague scores.

## Source review

Check:

- implementation matches the intended structure
- tokens and components are used consistently
- semantic elements are correct
- all relevant states exist
- content and assets are real or honestly labeled
- error and accessibility wiring are present
- no unsafe reference instructions or data leaks entered the implementation
- no unrelated refactor or dependency expansion occurred

Source review cannot prove rendered quality.

## Rendered review

Inspect representative pages and states at:

- narrow mobile
- wide mobile or small tablet when relevant
- laptop
- wide desktop
- intermediate widths where layout transitions
- zoomed text or viewport
- reduced motion
- light/dark or themes that actually ship

Use realistic short, long, missing, translated, and error content.

Check:

- hierarchy and reading order
- wrapping, clipping, overlap, and overflow
- media crop and quality
- navigation and wayfinding
- all interactive states
- pointer and touch behavior
- keyboard operation and focus
- loading, empty, error, disabled, and permission states
- motion start, interruption, and fallback
- layout stability
- console and network errors

## Functional walkthrough

Complete the core task from entry to exit. Test recovery:

- invalid input
- failed request
- retry
- cancellation
- back navigation
- duplicate action
- slow response
- lost permission or unavailable content
- destructive action and undo where offered

Confirm that status and next steps are understandable.

## Design-system comparison

Compare the rendered result to the active style contract:

- hierarchy
- typography
- palette pairings
- spacing and density
- radius and surface logic
- assets
- icons
- content voice
- motion
- explicit do-not list

Do not compare from memory.

## Cross-browser and device scope

Use the project's supported matrix. When no matrix exists, state what was checked and avoid implying universal support.

Check platform-sensitive behavior such as:

- font rendering
- sticky positioning
- viewport and safe-area sizing
- form controls
- focus indicators
- backdrop and filter effects
- animation
- input and virtual keyboard
- scrolling and overscroll

## Iterate

For every failed gate:

1. identify the root cause
2. make the smallest coherent repair
3. rerun the failed check
4. rerun affected regression checks
5. update evidence

Do not churn on cosmetic variants while a structural or functional gate remains failed.

## Handoff

Report:

- changed artifacts
- decisions made
- verified gates and evidence
- tests or commands run
- supported viewports and states checked
- known limitations
- blocked or unverified areas
- follow-up only when it is genuinely outside scope

Do not present a self-score as proof. Use screenshots, results, and observable behavior where available.
