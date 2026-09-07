# Accessibility: non-negotiable checks

**Load when:** introducing interactive or visual behavior, reviewing accessibility, or validating a substantial change.

## Standard, scope, and honest claims

Use WCAG 2.2 AA as the default technical target unless the project specifies another
applicable target. This is not a legal compliance determination or certification.
A few passing checks do not establish whole-site conformance. Identify the actual
pages, states, technologies, and assistive interaction covered by the work.

## Visual access

Check the actual rendered foreground/background combinations. Use the color module
for text and necessary non-text contrast criteria. Do not lower important metadata
contrast to imitate a reference. Keep meaning independent of color. Test forced
colors, especially controls defined only by shadows or transparent boundaries.

Support text enlargement and narrow reflow without clipping content or controls.
Text-spacing override tests are distinct from default typography choices. Do not
make required headings images or animated letter fragments with no intact equivalent.
Provide meaningful alternatives for informative visuals; decorative elements should
not create noise in the accessibility tree.

## Keyboard, focus, and targets

Use semantic links and controls with clear names. Preserve logical reading and
focus order; avoid positive tabindex values to repair a visually reordered layout.
All tasks need an appropriate keyboard route. Prevent focus traps except deliberate
modal containment with a usable exit.

WCAG 2.2 AA focus-not-obscured requires that the focused component not be entirely
hidden by author-created content. This skill's stronger design goal is full visibility
where feasible. Do not mislabel that stronger preference as the AA minimum.

Target-size minimum is 24×24 CSS pixels or a qualifying exception, including the
specified spacing rule, inline targets, equivalents, and other defined cases. Prefer
larger comfortable targets where possible; 44×44 is not the blanket WCAG 2.2 AA
minimum. Do not use a blanket exception for every icon control.

## Motion and operation

Respect reduced motion and provide an appropriate static experience. Consider
pause/stop/hide obligations for automatic movement; hover-only pause is insufficient
for a general control. Avoid flashing content. Preserve a non-dragging way to do
actionable operations when needed. Meaningful media needs the appropriate alternatives.

For forms, dialogs, and tabs, use the specific component guidance. Avoid announcing
decorative updates or every scroll position in live regions. Preserve actual focus
when the interface changes. Never aria-hide focusable descendants as a shortcut.

## Verify, do not infer

Run automated checks where available, then manually test keyboard order, focus,
zoom/reflow, motion preference, actual text contrast over media, and a screen-reader
sample of changed patterns. Report known failures and untested cases. Static markup
inspection cannot establish that an animated overlay never obscures focus.

## Sources

[WCAG 2.2](https://www.w3.org/TR/WCAG22/); [WAI: Target Size (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html); [WAI: Focus Not Obscured (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html); [WAI: Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow); [MDN: forced-colors](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/forced-colors).
