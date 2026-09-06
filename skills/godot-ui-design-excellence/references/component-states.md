# Component states: do not collapse different meanings into one highlight

## Model independent dimensions

Define at least these dimensions where relevant:

| Dimension | Example states |
|---|---|
| Availability | Available, disabled, locked with reason |
| Pointer | Outside, hover, pressed |
| Navigation | Unfocused, focused |
| Selection | Unselected, selected |
| Domain status | Equipped, researched, tracked, pending |
| Operation | Idle, processing, failed, succeeded |

Not every component needs every dimension. Explicitly specify legal combinations,
visual precedence, and what action is allowed. A selected item can lose focus;
a focused locked item can still expose its unlock explanation; an equipped item
is not necessarily the current inspection target.

## Compose visual channels

Use separate channels instead of replacing the whole appearance for each state.
For example: surface for availability, thin persistent marker for selection,
outer focus bracket for keyboard/controller, icon for equipped status, and concise
text for failure. The exact channels must match the art direction.

Specify pressed feedback without moving the hit target. Keep focus apparent during
hover coexistence and after a transition. Do not trigger an audio cue every time a
paint update re-applies the same state.

## Build the component contract

For a reusable component, record semantic role, input action, data fields, emitted
events, allowed state combinations, size constraints, text-overflow policy,
accessibility label, and visual variant. Events describe intent (`equip_requested`)
rather than directly mutating unrelated game systems.

Test at minimum: normal; focused; hovered; selected but unfocused; selected and
focused; disabled; locked with reason; long label; large text; error where relevant.
A gallery scene is useful, but it is not a substitute for the component in its
real gameplay context.

## Busy means real work

Use a processing state only for an actual operation. Short local state changes do
not need a fake spinner or artificial delay. For asynchronous work, distinguish
queued/loading, cancellable progress, failure, and stale response. Do not leave a
visual busy flag as the only guard against duplicate transactions.

## Token and theme mapping

Name variants after roles: `PrimaryAction`, `LedgerRow`, `InspectionPanel`, not
`BlueButton3`. Map shared values centrally; document component-specific exceptions.
In Godot, BaseButton built-in states are useful but do not automatically represent
all domain states above. Keep the domain state in a view model or component
contract and apply the corresponding layers deliberately.

Acceptance: two screenshots of compound states can be explained unambiguously;
input follows the same state model as the appearance; and an unavailable action
never masquerades as a working control.

## Evidence anchors

[G12](sources.md#g12) · [G13](sources.md#g13) · [G23](sources.md#g23) · [X113](sources.md#x113)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
