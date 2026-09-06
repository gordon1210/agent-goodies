# Settings, confirmation, and dialogue

## Settings are transactions

Classify each setting by application policy: immediate, apply/cancel, restart
required, or display-change confirmation with safe reversion. Communicate that
policy next to the relevant control. Show actual current values, staged values,
and defaults distinctly; "Reset" must explain its scope.

For risky display changes, use the project's established tested fallback and
persistence strategy. Do not invent a timer alone and call display recovery solved.
Keep keyboard/controller access available throughout preview and reversion.
Accessibility settings should be discoverable before the player must endure the
content they are intended to change.

Use a readable options layout with value, explanation, and interaction cue. Avoid
hiding all explanations behind pointer hover. Respect remapped input actions in
button prompts. A visual theme may carry the game's identity without compromising
the clarity of this utilitarian screen.

## Destructive confirmation

State the exact action and loss, use an explicit verb, and select a safe default
where appropriate. Make cancel/back reliable. Do not let the opening input's
remaining phase activate the default button. Revalidate the target when confirming;
a dialog opened for one item must not act on a newly selected item.

Escape/back should close the current layer once rather than simultaneously closing
a modal, unpausing, and triggering a gameplay action. Undo can be preferable when
action semantics support it; confirmation is not a universal substitute for recovery.

## Dialogue and captions

Separate decorative dialogue framing from readable spoken content. Record speaker,
text, optional portrait, timing, choices, and access to history where the game
requires it. Do not let a portrait failure block the words. Handle long lines,
multiple speakers, and a missing voice line without corrupting the layout.

Typing effects must operate on appropriate text boundaries, support instant reveal
or disabling, and preserve reading control. Do not slice translated strings by
assumed ASCII characters. A confirm input used to reveal a line should not also
skip the next line unintentionally.

Subtitles and captions need their own readability rules, background options,
positioning, and speaker identification; they are not simply a smaller ornate
menu label. Audio-only meaning should have an appropriate visual alternative.

## Choices and consequences

Let the user compare choice text without a moving selection or uncontrolled
countdown unless that constraint is deliberate gameplay. Clearly identify locked
choices and reasons. If a choice has irreversible consequences, communicate only
what the design intends players to know; do not fabricate outcome spoilers.

Acceptance: reach and adjust accessibility options with each supported device,
cancel a risky change safely, read the longest actual dialogue, and distinguish
reveal/advance/confirm behavior under rapid input.

## Evidence anchors

[G10](sources.md#g10) · [G26](sources.md#g26) · [X104](sources.md#x104) · [X112](sources.md#x112) · [X115](sources.md#x115)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
