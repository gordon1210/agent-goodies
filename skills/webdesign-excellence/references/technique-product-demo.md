# Technique: product as artwork

**Load when:** a product interaction or workflow can communicate the offer better than decorative illustration.

## Choose an honest demonstration mode

Use one of three modes: a real interactive product slice; an explicitly illustrative
local simulation; or a static annotated product view. Label simulations where viewers
could mistake them for actual activity. Never invent customers, live telemetry,
performance numbers, security results, or capabilities for visual credibility.

Identify one user question the demo answers. Show the input, the consequential state
change, and the useful output. A smaller legible interaction is usually better than
a complete miniature dashboard with unreadable text. Browser chrome is optional,
not required proof that something is software.

For a coordinated input-to-result sequence, use
[choreography](technique-choreography.md). If the subject requires mesh-based
inspection, add [3D art direction](technique-3d-art-direction.md) and then
[3D production](technique-3d-production.md) when implementing.

## Compose the micro-product

Use realistic content lengths, credible relationships, and the actual domain's
vocabulary. Remove irrelevant navigation from the showcased slice while preserving
what makes the workflow understandable. Keep the marketing explanation near the
visual event it describes. A highlighted element or short annotation can be more
effective than a permanently moving fake cursor.

Represent state explicitly: idle, chosen input, illustrative operation if applicable,
result, and reset. User-controlled stepping is often preferable to an endless loop.
When auto-play is justified, provide a pause mechanism and reset predictably when
the user chooses to interact. Never keep moving controls away from the pointer.

## Implementation boundaries

A decorative replica should not fill the tab order with non-working controls. A
real interactive demo needs native semantics, labels, keyboard access, and visible
focus. Do not make fake buttons look usable while silently ignoring clicks. Avoid
third-party services, production credentials, analytics, or live customer data unless
authorized and necessary.

Keep essential product explanations outside a canvas. Reduced-motion and static
versions should show the final useful state or a short annotated sequence, not an
empty panel. Resize the composition by simplifying it, not scaling text to 7px.

**Fallback:** an accurate still or semantic sequence with the same explanation.
**Test:** whether the demo actually teaches something in a few seconds; valid
interaction states; keyboard and touch; replay/pause; real versus illustrative data;
slow loading; and privacy of every visible field.

**Pass:** removing the demo would remove useful product understanding. Otherwise
it may just be another decorative hero dressed as UI.
