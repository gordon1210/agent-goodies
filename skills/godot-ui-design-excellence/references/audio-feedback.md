# UI audio: a small semantic vocabulary

## Define events, not random sounds per widget

Create a restrained family for focus/navigation, confirm, cancel/back, unavailable,
transaction success/failure, warning, and exceptional reward. Map sound to a
meaningful state transition, not to every draw or property update. A hovered row
repaint should not retrigger its cue.

Relate sonic character to the interface metaphor: a soft material tick, a brief
mechanical response, or a restrained tonal cue can support identity. These are
creative options, not prescribed samples. Avoid turning every menu into an impact
sound demonstration. Keep long or dramatic events rare enough to retain meaning.

## Cadence and overlap

Repeated controller navigation can produce many cues rapidly. Establish cooldown,
voice limiting, or coalescing so short sounds do not accumulate into noise. Do not
queue obsolete navigation sounds after the focus has already moved. Distinguish
intentional hold-repeat input from many separate committed actions.

Use a UI bus or the project's existing equivalent for independent adjustment.
Test it beside dialogue, music, and combat; a cue that is clear in isolation may
be masked or excessively sharp in context. Avoid silently ducking critical game
audio whenever a tooltip appears.

## Synchronization

Play acknowledgement at the meaningful input response; play success after actual
success. The decorative visual can continue afterward. A cancel sound should
correspond to the dismissed layer, not sound twice as one back input propagates
through several screens.

If an asynchronous request fails, communicate the failure visually and semantically
as well as sonically. Do not let an optimistic confirm sound imply an irreversible
transaction already completed.

## Accessibility and preference

No critical meaning should exist only in audio. Provide a clear visual indication
of errors, warnings, and completion, and preserve navigational meaning when UI
sounds are muted. Reduced-motion mode may use the same short semantic audio cues,
but audio should not become a compulsory replacement for missing visual state.

Keep sound intensity, pitch repetition, and duration comfortable during extended
navigation. Review with rapid inputs and long sessions, not only a single button
press. Use existing licensed project audio when possible; do not fetch or install
sound libraries without checking permissions and provenance.

Acceptance: sound confirms the correct event once, stops or yields appropriately,
does not overwhelm gameplay, and can be muted without losing essential meaning.
The skill specifies behavior; it does not supply audio assets or claim audio
quality without listening to the actual output.

## Evidence anchors

[D03](sources.md#d03) · [X103](sources.md#x103)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
