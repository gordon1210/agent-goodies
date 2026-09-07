# Components: forms and truthful feedback

**Load when:** designing inputs, validation, submission, loading, errors, and status messages.

## Make the action understandable

Use persistent labels, relevant instructions, and suitable native input types.
A placeholder is not the only label. Mark required fields clearly and explain
format constraints before an error occurs. Use autocomplete and input purpose
metadata where appropriate. Do not add friction solely to make a form feel premium.

Group related fields with useful semantics. Align label, control, help, and error
as one component. Leave space for realistic translations and multiline errors;
do not force every field to a fixed total height. Mobile users need usable controls
with their keyboard open, not a perfectly centered screenshot.

## Validation and state

Show errors near the relevant fields and associate them programmatically. For a
failed multi-field submission, use a useful summary and focus strategy rather than
only a disappearing toast. Preserve valid entries. Distinguish validation problems,
network failures, rejected operations, and successful completion.

Represent idle, pending, success, and failure from actual state. Start loading only
when work starts. Show success only when the relevant operation succeeds, unless
an explicitly designed optimistic interaction is clearly recoverable. Prevent
accidental duplicate submission without hiding the state or trapping keyboard focus.

Clipboard feedback must reflect the actual write result. A simulated product demo
may show an illustrative sequence but must not impersonate a successful real submission.
Do not store or transmit form data to an unapproved service.

## Visual detail

Use a coherent field surface, label weight, border, and focus treatment. Do not
remove outlines without a replacement. Error meaning needs text or another
non-color cue. Keep required controls recognizable under forced colors. Use concise
feedback near its cause; reserve toasts for events that make sense outside the field.

Avoid disabling a submit action with no explanation of how to proceed. Sometimes
allowing submission to reveal specific errors is more useful than silent disablement;
follow the product's established pattern and actual requirements.

**Test:** empty submission, invalid input, long errors, slow requests, offline failure,
retry, double activation, keyboard-only completion, autofill, password managers where
relevant, and software keyboard. No failure should erase the user's work unnecessarily.

## Sources

[WAI: Form notifications](https://www.w3.org/WAI/tutorials/forms/notifications/).
