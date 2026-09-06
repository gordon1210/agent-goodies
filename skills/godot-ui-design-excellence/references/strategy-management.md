# Strategy and management: dense information without visual noise

## Design around causality

The central question is rarely just "how many resources do I have?" It is often
"what is changing, why, when does it become a problem, and what can I do?"
Separate stock, net rate, capacity, forecast horizon, and urgency. Show units and
signs consistently. A red number is not a sufficient explanation of a deficit.

A proposed resource instrument might show `420 units`, `−12 / cycle`, and a
separately labeled `35 cycles at current rate`. Do not compute the forecast when
rates are intermittent or constraints invalidate a linear estimate without
explaining those assumptions. Keep exact data available when abbreviations hide
important thresholds.

## Layer the information

| Layer | Job | Example |
|---|---|---|
| Persistent overview | Reveal developing conditions | Resource strip, pressure indicators |
| Selection inspector | Explain the current object | District output and operating costs |
| Causal detail | Show the contributors | Sources, sinks, policy effects |
| Decision preview | Explain the proposed change | Construction cost and projected effect |
| Escalation | Demand attention proportionally | Forecast problem vs active failure |

A Frostpunk-2-like brief should study consistent links between map markers,
communities, inspectors, and the underlying decisions—not merely recreate cold
colors and small numerals. The original designer portfolios show that mockups,
implementation, animation, and input-specific flows are separate work products.

## Preserve situational context

Keep enough world or map visible to relate an inspector to the object it describes.
Maintain a clear selected-object marker while a panel is open. Consider a compact
inspector, expanded planner, and explicit modal rather than accumulating floating
windows with identical visual priority.

Distinguish paused simulation, paused input, and a blocked dialog. A confirmation
must not silently allow a resource to disappear while the user is reading unless
that behavior is an intentional, communicated rule. Revalidate costs at commit.

## Density grammar

Use aligned rows, repeated units, section spacing, and selective separators before
adding nested cards. Give high-frequency facts stable positions. Separate category
color from urgency so a faction color cannot look like an error. Keep neutral
figures calmer than changes that need action.

Let an expert scan while a novice can inspect explanations. Tooltips need a
controller/keyboard path, pinning or persistent detail for longer content, and a
clear relationship to their triggering object. Do not hide essential actions
inside mouse-only hover chains.

## Input and scalability

A PC-oriented planner may lead with efficient pointer interaction without becoming
mouse-exclusive. Provide direct navigation or a list alternative for key spatial
actions. Controller adaptation can reorganize a flow; moving a cursor with a stick
is not automatically an adequate implementation of every dense screen.

Acceptance tasks: identify the cause of a deficit, compare remedies, inspect a
community, preview a commitment, cancel safely, and return to the same world context.
Verify these tasks at the highest realistic data density, not only a new empty city.

## Evidence anchors

[D03](sources.md#d03) · [D04](sources.md#d04) · [D09](sources.md#d09) · [G29](sources.md#g29) · [X112](sources.md#x112)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
