# Accessibility, Localization & Inclusive Design

Use this guide for production websites and interfaces. Accessibility is part of the component and content contract, not a final visual patch.

Default to the project's required conformance target; when none is specified, use a robust AA-level baseline and verify the requirements that apply.

## Use the platform

- Use semantic HTML and native controls whenever they fit.
- Use buttons for actions and links for destinations.
- Give the document a coherent heading and landmark structure.
- Provide one visible primary content region.
- Add skip navigation when repeated chrome precedes substantial content.
- Prefer less ARIA over incorrect ARIA.

## Keyboard and focus

- Every pointer action needs a keyboard path when the interaction is relevant to keyboard users.
- Preserve logical tab order; avoid positive `tabindex`.
- Make `:focus-visible` clearly visible.
- Manage focus when dialogs, menus, drawers, or routed views open and close.
- Restore focus to the initiating control when appropriate.
- Support expected keys for composite widgets.
- Do not place focusable controls inside hidden or inert content.

## Names, labels, and status

- Every control needs an accessible name.
- Every field needs a persistent label.
- Connect helper and error text programmatically.
- Mark validation state and focus the first invalid field or provide an accessible summary.
- Use polite status announcements for routine updates and urgent announcements only for urgent errors.
- Ensure visible labels are contained in accessible names.
- Hide purely decorative media from assistive technology.

## Visual access

- Verify actual foreground/background combinations.
- Do not use color as the only indicator.
- Preserve visible state and boundaries in forced-color or high-contrast environments where supported.
- Ensure controls remain distinguishable at different states.
- Make text and controls usable at zoom and enlarged text settings.
- Avoid fixed-height text containers that clip content.

## Motion and media

- Honor reduced-motion preferences.
- Do not require motion to understand state or sequence.
- Provide pause/stop controls for non-essential autoplay.
- Avoid flashes and motion patterns that can cause harm.
- Provide captions, transcripts, descriptions, or alternatives required by the media's purpose.
- Keep time-limited content adjustable where the product permits.

## Touch and input

- Make interactive targets large enough for the supported context and avoid overlapping hit areas.
- Do not rely on hover.
- Gate hover-only visual effects to devices that actually support hover.
- Preserve pinch zoom.
- Use input types and modes that summon appropriate keyboards.
- Support pointer cancellation and avoid gesture-only completion.

## Reflow and content resilience

Check:

- narrow viewport and high zoom
- no loss of content or action
- no unintended two-dimensional scrolling except where essential
- long headings, labels, URLs, and numbers
- user-generated content
- empty and error states
- browser text spacing overrides

## Localization

- Keep messages as complete translation units.
- Use locale-aware dates, times, numbers, currencies, and pluralization.
- Support text expansion.
- Avoid hard-coded left/right behavior when RTL is supported.
- Mirror directional icons only when their meaning is spatial.
- Choose fonts that cover the target scripts.
- Avoid culture-specific metaphors without intent.
- Do not embed translatable text in images.

## Testing

At minimum, perform or explicitly mark unverified:

- keyboard-only task walkthrough
- focus order and focus visibility
- accessible names, roles, and states
- form labels and error recovery
- contrast in actual states
- zoom/reflow and text expansion
- reduced-motion behavior
- automated audit as a supplement, not sole proof

For high-impact products, validate with users who rely on relevant assistive technologies.
