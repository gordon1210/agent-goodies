# Input and device support

Use for Input Map actions, keyboard, mouse, touch, controllers, rebinding and device switching.

## Model intent, not physical controls

Gameplay code should consume actions such as `move_left`, `jump`, `confirm` and `pause`, not hard-coded key codes. Keep UI navigation actions distinct when remapping gameplay must not break menu access.

Use event callbacks for discrete events and the `Input` singleton for held state. Respect `_gui_input()`, `_input()` and `_unhandled_input()` propagation rather than handling everything globally.

## Rebinding

- Store one or more `InputEvent` bindings per action using a versioned settings schema.
- Detect conflicts and protected navigation/cancel bindings.
- Normalize display labels by device and layout; a physical key and a character are not interchangeable.
- Support dead zones for analog actions.
- Ignore the input event that opened a rebinding dialog until capture is armed.
- Allow reset to defaults.
- Test hot-plugging and controller reassignment if local multiplayer is supported.

## Device-aware prompts

Track the last meaningful input family without flapping on mouse drift or noisy axes. UI icons are presentation state; gameplay actions remain device-independent.

## Mouse and pointer

Treat captured, confined and visible mouse modes as explicit states. Restore a usable cursor on pause, focus loss and error paths. Scale look input consistently; do not multiply event-relative mouse motion by frame `delta` unless the chosen API semantics require it.

## Touch

Design touch controls as first-class input, not mouse emulation pasted over desktop UI. Account for multi-touch IDs, safe areas, gesture cancellation and app lifecycle interruption. Use sufficiently large targets and test real devices.

## Accessibility

Provide remapping, alternate bindings, hold/toggle options where relevant, sensitivity/dead-zone controls and non-color-only feedback. Avoid time-critical rebinding or menus that require a pointer.

## Verification

Test at least keyboard, the primary controller family and any target touch device affected. Verify input while paused, after focus loss, across scene changes and with UI focus active.
