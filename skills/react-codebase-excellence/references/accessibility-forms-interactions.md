# Accessibility, Forms, and Interactions

Read this reference when changing semantic markup, controls, forms, keyboard behavior, focus, overlays, dynamic status, errors, motion, drag-and-drop, or design-system interactions. Accessibility is part of component correctness, not a post-processing lint pass.

## 1. Establish the accessibility contract

Inspect:

- repository policy and target standard, commonly WCAG 2.2 AA where applicable;
- existing design-system primitives;
- supported browsers and assistive technologies;
- keyboard and screen-reader critical paths;
- localization, right-to-left layout, zoom, forced colors, reduced motion, and high contrast;
- automated and manual test practice;
- legal or customer-specific requirements.

Do not claim conformance from automated tests alone. They detect only a subset of issues.

## 2. Native semantics first

Use the native element that represents the action:

- `<button>` for an action;
- `<a href>` for navigation;
- `<input>`, `<select>`, and `<textarea>` for form controls;
- headings in meaningful order;
- lists for list relationships;
- tables for tabular data;
- `<details>`/`<summary>` where their behavior fits;
- landmarks such as `main`, `nav`, `header`, and `footer` where appropriate.

Native elements supply keyboard behavior, focus, semantics, form integration, and platform conventions. Recreating a button with a `<div>` requires handling every one of those contracts and is rarely justified.

ARIA supplements semantics; it does not repair an unsuitable interaction model automatically. Prefer “no ARIA is better than bad ARIA.”

## 3. Accessible names and descriptions

Every interactive control needs a meaningful accessible name.

Prefer, in order where appropriate:

- visible text content;
- an associated `<label>`;
- `aria-labelledby` referencing visible text;
- `aria-label` when no visible label can exist.

Keep visible label text within the accessible name so speech-input users can address the control by what they see.

Use descriptions for supporting instructions or errors, not as a substitute for the name. Connect them with `aria-describedby` or the relevant native relationship.

Icon-only buttons need an accessible name. Decorative icons should not duplicate the name and may be hidden from the accessibility tree, but never place `aria-hidden="true"` on a focusable element or an ancestor of one.

## 4. IDs and relationships

Use explicit domain IDs when available. Use `useId` for stable component-instance relationships such as:

- label to input;
- input to help text;
- input to validation error;
- trigger to panel;
- heading to dialog or region.

Do not use `useId` for list keys. In reusable components, allow an explicit ID override where consumers must integrate with external markup.

Ensure IDs remain unique across repeated components, SSR hydration, and multiple roots.

## 5. Keyboard operability

Every pointer interaction must have an equivalent keyboard path unless the task is inherently pointer-specific and an accessible alternative exists.

Check:

- Tab and Shift+Tab order;
- Enter and Space activation according to native pattern;
- arrow-key behavior for composite widgets when the pattern requires it;
- Escape behavior for dismissible overlays;
- Home/End/Page keys where expected;
- focus visibility;
- no keyboard trap except an intentional modal trap with an exit;
- shortcuts do not conflict with typing, browser, or assistive technology;
- drag-and-drop has a non-pointer alternative.

Do not add `tabIndex={0}` to every element. Composite widgets often use one tab stop plus managed internal navigation; ordinary content should retain native order.

## 6. Focus management

Move focus only when it helps users understand a meaningful context change.

Common required cases:

- opening a modal dialog;
- closing an overlay and restoring the trigger;
- moving to the first invalid field or error summary after failed submission, according to product policy;
- route/page transition focus or announcement where the framework does not provide it;
- inserting an editing surface that users explicitly requested;
- destructive confirmation or authentication step.

Avoid stealing focus during background refresh, optimistic updates, or passive content changes.

When removing the focused element, choose where focus should go next. Do not let it fall to `<body>` unexpectedly in a critical workflow.

Focus indicators must remain clearly visible. Do not remove outlines without an equivalent indicator that survives themes, forced colors, and zoom.

## 7. Dialogs and modal overlays

A modal dialog needs:

- `role="dialog"` or native `<dialog>` behavior used correctly;
- an accessible name and optional description;
- initial focus placed according to content and risk;
- focus contained while modal when required;
- background interaction prevented and hidden/inert according to the implementation;
- Escape or an explicit close path unless closing is intentionally blocked for a justified critical step;
- focus restoration to the logical trigger or next location;
- nested-overlay coordination;
- scroll behavior and mobile viewport handling.

Do not put `aria-hidden` on an ancestor containing the dialog portal. Use an established primitive when available and test in a real browser.

## 8. Menus, tabs, comboboxes, and other composites

Custom composite widgets have detailed keyboard and ARIA contracts. Follow the WAI-ARIA Authoring Practices pattern appropriate to the actual widget, not a visually similar one.

Examples:

- A site navigation list is usually not an ARIA `menu`.
- A group of filtering buttons is not automatically a tablist.
- An autocomplete is more than an input plus a positioned list.
- A tooltip is not interactive content that users must tab into.

Prefer a proven design-system primitive. If implementing one, test roles, properties, active descendant or roving focus, typeahead, selection, disabled items, orientation, Home/End behavior, and screen-reader announcements.

## 9. Forms and labels

Every field needs a programmatic label. Placeholder text is not a label.

Preserve:

- native field type;
- `name` and form association;
- autocomplete tokens;
- input mode;
- required/read-only/disabled semantics;
- constraints and instructions;
- grouping with `fieldset` and `legend` where related controls need a group label;
- error relationships;
- browser autofill and password-manager behavior;
- input method editor composition.

A custom visual label must remain clickable/focus-associated when users expect it.

Do not prevent paste, autofill, or password-manager behavior without a defensible security and usability requirement.

## 10. Validation and errors

On invalid submission:

- identify the field or form problem in text;
- associate field errors with controls;
- use `aria-invalid` when appropriate;
- preserve entered values unless security requires clearing them;
- provide a correction path;
- focus or summarize errors according to the workflow;
- avoid relying only on color, icon, or border;
- distinguish client guidance from authoritative server validation.

Do not announce every keystroke validation error. Choose validation timing that is useful and not disruptive.

An error summary should contain links or controls that move users to relevant fields when practical. Server errors must not expose internal details.

## 11. Pending and submission state

Pending UI must be perceivable without unexpectedly removing the current focus.

Options include:

- changing button text while preserving the button node;
- `aria-busy` on the region whose content is updating;
- a nearby status message;
- disabling only when duplicate action is unsafe;
- keeping previous content visible during transition;
- exposing progress for long determinate work.

Do not replace the focused submit button with a spinner-only element. If disabling it causes focus or discoverability problems, consider preserving it with `aria-disabled` plus guarded activation—but only when semantic and form behavior remain correct.

Avoid repeated live-region announcements for every render or transition update.

## 12. Live regions and dynamic content

Use live regions for important updates users would otherwise miss:

- submission result;
- asynchronous validation summary;
- item added/removed where focus does not move;
- background completion important to the current task;
- connection or session status changes.

Choose polite versus assertive priority conservatively. Keep messages concise and stable enough to be announced.

Do not put large changing containers in a live region. Do not duplicate an announcement through both focus movement and an assertive message unless necessary.

A visually present spinner with no accessible status communicates nothing to nonvisual users.

## 13. Loading, Suspense, and optimistic UI

For loading states:

- preserve heading and region context;
- avoid focusable skeleton controls;
- prevent layout shift;
- indicate busy state at a meaningful scope;
- keep previous content available when safe;
- provide retry on failure.

For optimistic UI:

- distinguish pending from confirmed state when the distinction matters;
- announce failure and rollback;
- keep keyboard position stable;
- do not announce transient list changes repeatedly;
- avoid presenting a high-risk operation as final success before confirmation.

Suspense fallback placement is also an accessibility decision. Replacing an entire page can remove landmarks, headings, and focus context.

## 14. Disabled, read-only, and unavailable states

Use native `disabled` for form controls when removal from interaction and form submission is correct.

Use `readOnly` when users may focus/copy a value but not edit it.

`aria-disabled` communicates disabled state but does not prevent focus, activation, or form behavior. Code must enforce the behavior and the interaction must justify retaining focusability.

Do not disable a control without explaining why when the reason is not obvious. Sometimes allowing activation and showing validation is more usable than a permanently unexplained disabled button.

## 15. Links and navigation

Links require meaningful destination text. Avoid repeated “click here” labels without context.

Preserve:

- native href and modified-click behavior;
- focus and visited semantics;
- target behavior and safe `rel` values;
- download semantics;
- current-page indication;
- route change focus/announcement policy.

Use buttons for actions such as opening a dialog or deleting an item. Styling does not change semantics.

Client routing should not erase native keyboard, context menu, open-in-new-tab, and URL behavior.

## 16. Tables, grids, and lists

Use a table for data with row/column relationships. Include headers, caption or accessible name, and scope/association as needed.

Do not use ARIA grid unless spreadsheet-like keyboard interaction is required. A responsive visual card layout can still preserve table semantics when relationships matter, or use a different accessible presentation deliberately.

Lists communicate item count and grouping. Do not remove list semantics through inappropriate roles solely for CSS.

For sortable tables, communicate current sort and provide keyboard-operable headers.

## 17. Images, icons, SVG, and canvas

Images need alternative text based on purpose:

- informative: convey equivalent content;
- functional: name the action or destination;
- decorative: empty alt or hidden appropriately;
- complex: provide adjacent detailed description.

Do not repeat surrounding caption text as alt without benefit.

SVGs need correct title/name strategy when meaningful and should be hidden when decorative. Avoid many duplicated IDs inside repeated inline SVG components.

Canvas needs an accessible fallback or parallel DOM representation for meaningful interaction and content.

## 18. Color, contrast, and non-text cues

Do not use color as the only indication of error, selection, status, or required fields.

Preserve sufficient contrast for text, controls, focus indicators, and meaningful graphics according to the target standard. Test states: default, hover, focus, active, selected, disabled, error, and forced colors.

CSS opacity can reduce contrast unexpectedly. Disabled styling may have different conformance treatment but still needs to remain understandable.

## 19. Motion and animation

Respect `prefers-reduced-motion` for nonessential motion and provide alternatives for motion necessary to understand state.

Avoid:

- rapid flashes;
- large parallax or zoom without reduction;
- animation that blocks interaction;
- focus moving with animated DOM before the target is ready;
- relying on animation completion as the only state signal.

Transitions and React scheduling do not replace CSS/media accessibility controls.

## 20. Touch, pointer, and responsive behavior

Ensure controls remain operable at zoom and reflow without requiring two-dimensional scrolling except where the content inherently requires it.

Check:

- target size and spacing according to the target standard;
- hover-only information also available on focus/touch;
- pointer cancellation for destructive actions;
- orientation and viewport changes;
- on-screen keyboard overlap;
- no gesture-only operation without an alternative;
- drag handles and resize controls have keyboard alternatives.

Do not make critical content appear only on hover.

## 21. Internationalization and bidirectionality

Accessibility and localization interact.

- Do not construct sentences from fragments that translators cannot reorder.
- Keep accessible names localized with visible text.
- Support text expansion without clipping.
- Use logical CSS properties where RTL support matters.
- Preserve correct document and element language.
- Format dates, numbers, pluralization, and relative time with locale-aware tools.
- Avoid using visual order as reading order.

Server and client locale/timezone must agree for hydration or use a deliberate post-hydration strategy.

## 22. Focus and hidden content

Hidden content should not remain focusable.

Review:

- CSS-only offscreen panels;
- collapsed disclosures;
- inactive tabs;
- hidden Activity subtrees;
- modal background;
- animated exits;
- virtualized items;
- portal hosts.

`aria-hidden="true"` removes content from the accessibility tree but does not itself prevent focus. Never apply it to a focusable element or an ancestor containing focusable descendants.

When a React 19.2 Activity becomes hidden, effects are removed and the DOM is hidden; still test current focus and restoration behavior.

## 23. Testing strategy

Automated:

- lint obvious semantic/ARIA issues;
- run an accessibility engine on representative states;
- query by role/name in component tests;
- test keyboard paths and focus movement;
- test errors, pending, and live status;
- test responsive states where feasible.

Manual, proportionate to risk:

- keyboard-only navigation;
- focus visibility and order;
- one or more supported screen reader/browser combinations;
- zoom/reflow;
- forced colors/high contrast;
- reduced motion;
- touch and mobile viewport;
- localization/RTL.

Real-browser testing is required for many focus, dialog, CSS, layout, and assistive-technology behaviors. DOM emulation cannot prove them.

## 24. Common failure modes

- Clickable `<div>` with no native keyboard behavior.
- Icon button with no accessible name.
- Placeholder used as label.
- Error shown only by red border.
- Focus lost when a pending button is replaced.
- Modal opens without focus management or background isolation.
- `aria-hidden` ancestor contains a focusable element.
- `aria-disabled` control still activates.
- Custom menu semantics applied to ordinary navigation.
- Live region announces every keystroke.
- Skeleton contains tabbable fake controls.
- Index-key reorder moves state/focus to the wrong list item.
- Route transition changes content without a focus/announcement policy.
- Reduced-motion preference ignored.

## 25. False-positive controls

Do not report these without context:

- An element lacks an ARIA role when native semantics are sufficient.
- A button does not handle Enter/Space manually; native buttons already do.
- `aria-label` is absent when visible text supplies the name.
- Focus is not moved after a passive background update.
- A native disabled control leaves the tab order.
- A live region is absent for a change users can perceive through focus or direct interaction.
- A component uses `div` for noninteractive layout.
- A dialog library owns focus behavior outside the local file; verify integration before filing a finding.

## 26. Completion gate

Before completing interaction work, confirm:

- Native semantics are used where possible.
- Every control has a meaningful accessible name.
- Keyboard behavior, focus order, focus movement, and restoration are correct.
- Form labels, errors, pending status, and correction paths are programmatically connected.
- Dynamic changes are announced only where needed.
- Hidden content cannot receive focus unexpectedly.
- Color, motion, zoom, responsive, and localization behavior remain usable.
- Automated checks and direct keyboard/focus tests were run, with real-browser or assistive-technology checks proportionate to risk.
