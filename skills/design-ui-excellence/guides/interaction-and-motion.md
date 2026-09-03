# Interaction & Motion

Use this guide when behavior changes over time, elements enter or exit, gestures matter, or an interface needs motion polish.

Motion pays for itself only when it improves feedback, causality, orientation, hierarchy, or storytelling.

## Animation decision

Before animating, answer:

1. What changes?
2. Why should the user see the transition?
3. How often will it occur?
4. Was the action triggered by keyboard, pointer, touch, scroll, or system state?
5. Can it be interrupted?
6. What remains understandable with motion reduced or removed?

High-frequency or keyboard-driven actions should usually be instant or use only brief state feedback. Rare onboarding, explanation, or brand moments can support richer choreography.

## Motion hierarchy

Choose at most one dominant motion idea per surface. Supporting interactions should be quieter.

Do not combine scroll reveals, marquees, parallax, magnetic controls, cursor effects, and animated gradients simply because each is available.

## Timing and easing

Use values that match distance, size, frequency, and personality. Typical starting points:

- press or tiny state feedback: roughly 80–160 ms
- tooltip or small popover: roughly 120–220 ms
- menu, dialog, or panel: roughly 180–360 ms
- explanatory or campaign sequence: longer only when the content needs time

Entrances normally start responsively and settle; movement between on-screen states normally accelerates and decelerates; constant motion uses linear timing. Avoid slow starts on controls that should feel immediate.

Use project tokens or define a small motion scale. Do not assign a different curve to every component.

## Choose the mechanism

- **CSS transition** — interactive states that may reverse or retarget.
- **CSS keyframes** — predetermined, staged sequences.
- **Web Animations API** — programmatic control with browser-native animation.
- **Motion library or spring** — gestures, physics, dynamic layout, or interruptible trajectories.
- **No animation** — repeated operations, unclear purpose, or insufficient performance budget.

Use the mechanism already established by the project when it fits.

## Performance

- Prefer composited properties such as `transform` and `opacity`.
- Name transitioned properties; avoid `transition: all`.
- Avoid broad state updates on every scroll or pointer frame.
- Use observers, motion values, or native browser behavior where appropriate.
- Apply `will-change` only to a proven hotspot and remove it when no longer needed.
- Keep blur, backdrop effects, and large animated layers restrained.
- Measure on representative lower-end devices when motion is central.

## Spatial behavior

- Enter and exit from a location that explains origin or destination.
- Anchored popovers should feel connected to their trigger.
- Modals are viewport-level, not trigger-origin popovers.
- Avoid starting from zero scale; preserve a plausible object.
- Make exits slightly quieter than entrances.
- Stagger only when sequence communicates hierarchy; never delay access to controls.
- Preserve momentum and damping for drag gestures.
- Capture pointer input and handle cancellation safely.

## Feedback

Interactive elements need immediate state feedback:

- visual pressed state
- selected/current state
- pending state tied to real work
- success or error
- undo when appropriate

Motion cannot be the only cue. Pair it with color, shape, label, icon, or position.

## Reduced motion

Under reduced-motion preferences:

- remove parallax, large translation, zoom, and autoplay
- preserve content order and task completion
- use minimal opacity or color changes where useful
- keep urgent feedback perceivable
- provide controls for non-essential autoplaying media

## Verification

Inspect motion at normal speed and slowed down. Check:

- start and end state
- interruption and rapid repeat
- origin
- property synchronization
- dropped frames
- focus and input during animation
- reduced-motion path
- content reflow
- behavior under slow loading

A motion demo is not complete until the interaction still works when animation is disabled.
