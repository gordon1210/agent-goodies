# UI input and accessibility

Use for keyboard/gamepad focus, pointer handling, screen readers, text scaling, motion and inclusive UX.

## Focus is a graph

Every interactive screen needs:

- an initial focused control;
- predictable directional/tab navigation;
- visible focus state;
- cancel/back behavior;
- focus restoration when a modal closes;
- handling for controls becoming hidden or disabled.

Let containers and automatic neighbors work where reliable, but set explicit focus neighbors for non-linear layouts. Test with a controller, not only a mouse.

## Input propagation

Set `mouse_filter` deliberately. Overlays that block gameplay need to consume pointer input; decorative Controls should not. Use `_gui_input()` for control-local input and `_unhandled_input()` for gameplay actions that UI did not consume.

Prevent one input from both activating a button and reaching gameplay beneath it. Pause menus must use a process mode that remains active while the tree is paused.

## Accessibility baseline

- Remappable actions and keyboard/controller-only operation.
- Text scaling without clipping or loss of information.
- Sufficient contrast and a non-color-only representation of state.
- Captions/subtitles and separate voice/music/SFX controls where applicable.
- Reduced motion or skippable animation for disruptive effects.
- Adjustable timing, hold/toggle alternatives and sensitivity where gameplay benefits.
- Meaningful control names and ordering for supported screen-reader paths.

## Text and icons

Do not encode required information solely in an icon or color. Localize accessible labels and control prompts. Support font fallback and scripts used by target locales.

## Touch

Use target sizes and spacing suitable for fingers, safe-area margins and scroll behavior that does not conflict with gestures. Provide non-hover feedback.

## Verification

Navigate each screen without a pointer, at increased text scale, with representative translations and with motion/contrast options enabled. Verify focus after scene changes, modal stacks, dynamic list updates and device switching.
