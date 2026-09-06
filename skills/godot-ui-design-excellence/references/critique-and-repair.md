# Critique and repair: diagnose why an interface looks unfinished

## Start with the failure, not an effect

| Symptom | Likely cause to investigate | Useful first correction |
|---|---|---|
| Looks like a generic app | Uniform cards, no world relationship, default type hierarchy | Recompose one screen around its decision and identity |
| Expensive art, poor readability | Texture behind small text, weak value separation | Calm the reading area and establish a dependable backing |
| Everything feels important | Equal saturation/contrast/motion | Reserve emphasis for active choice and true urgency |
| Feels cheap despite animation | Inconsistent spacing, icons, state transitions | Repair rhythm and state grammar before adding effects |
| Looks good only in a hero image | No content or state stress testing | Render dense and unavailable states with real data |
| Controller feels broken | Focus not modeled with state/scrolling | Fix scope, order, visibility, and restoration |
| Painterly frame stretches badly | Unique art treated as arbitrary nine-slice | Separate fixed ornaments from scalable structure |
| Large text breaks the screen | Fixed interior geometry and untested overflow | Reflow or restructure, not shrink the text back down |
| Motion feels sticky | Queued tweens, delayed input, long staggers | Replace transitions, remove unnecessary input waits |

These are diagnostic hypotheses, not automatic accusations. Inspect the actual
screen and code before choosing a cause. Respect established project constraints;
a deliberate plain tactical interface is not "bad" because it lacks ornament.

## Order corrections by consequence

First fix hidden actions, incorrect state, unreadable essential information,
modal leaks, and data loss. Then repair reading hierarchy and composition. Next
fix typography, spacing, component consistency, and responsive behavior. Only then
refine texture, transitions, and sound. Do not bury a major usability defect under
minor art comments.

## A concrete review statement

Bad: "Make it more AAA."
Better: "In the comparison screen, the portrait and warning share the same maximum
contrast while the replacement item name is secondary. Reduce the portrait's
background detail, keep the warning persistent but compact, and promote the current
comparison header. Verify at the smallest target resolution."

Every comment should name the observed state, location, impact on the player,
likely cause, and bounded change. Distinguish observed failure from untested risk.
Use screenshots/crops and reproduction steps; do not invent exact pixels from an
unmeasured reference.

## Acceptance rubric

Rate each axis separately using anchored language: missing/broken; basic; coherent;
carefully authored; validated against the agreed target and task set. Axes are
identity, composition, typography, state clarity, interaction, responsiveness,
accessibility, motion, asset craft, and measured runtime behavior. Do not sum the
scores into a pseudo-scientific AAA rating.

A hard blocker remains a blocker regardless of visual score. A missing test stays
"not tested," not an inferred pass. Agree on a bounded next pass and preserve the
accepted design decisions so iterative criticism does not randomly change identity.

## Evidence anchors

[D05](sources.md#d05) · [D08](sources.md#d08) · [X101](sources.md#x101) · [X112](sources.md#x112) · [X113](sources.md#x113)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
