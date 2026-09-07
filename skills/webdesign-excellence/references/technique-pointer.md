# Technique: pointer response without pointer dependence

**Load when:** a fine-pointer enhancement has a specific expressive purpose.

## Optional, never essential

Tilt, a spotlight, magnetic attraction, and a trailing cursor are decorative
mechanisms. Use at most the one that reinforces the chosen concept. A user should
not need to discover the hover effect to understand a link, image, or action.

Keep the native cursor. A decorative follower must not replace it, intercept events,
obscure selection, or become the only location cue. Use the existing browser cursor
for text, drag, resize, and pointer affordances. Do not apply `cursor: none` to the body.

## Geometry and input

Gate optional behavior with the relevant pointer/hover capability and reduced-motion
preference, not just screen width. Mixed-input devices require graceful behavior when
input changes. Return to a stable resting state on pointer leave, cancellation,
visibility changes, and lost focus.

Map pointer position to local bounds and clamp the result. For a magnetic button,
keep the real hit target stationary and move a visual child slightly. Do not make
the clickable target flee the pointer. For tilt, use a stable wrapper for measurements
so the transformed rectangle does not feed back into its own calculation.

Throttle updates through one managed animation loop or suitable motion values.
Avoid framework rerenders for every mouse event. Reuse measurements sensibly but
invalidate on resize and layout change. Keep visual movement subtle enough that
text remains easy to read. Stop the loop when idle or off-screen.

## Accessibility and fallback

Provide normal hover and focus feedback independent of the effect. A keyboard user
does not need a simulated pointer animation; they need visible focus and predictable
activation. A touch user should receive the complete static design. Never make
critical content appear only under a moving circular reveal mask.

**Fallback:** normal links, buttons, images, and focus styles. **Test:** touch, pen,
keyboard, reduced motion, rapid pointer leave, scrolling under a stationary pointer,
zoomed layout, and overlays. Check that no visual layer blocks clicks.

**Reject:** the effect consumes attention without explaining or expressing anything,
causes motion discomfort, or takes more code and lifecycle complexity than its value.

## Sources

[MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/prefers-reduced-motion).
