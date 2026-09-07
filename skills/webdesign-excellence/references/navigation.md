# Components: navigation, disclosure, tabs, and dialogs

**Load when:** implementing or changing navigation and layered interactive UI.

## Use the appropriate semantic model

Site navigation is usually a list of links, not an ARIA application menu. A mobile
navigation disclosure needs a labeled button with an accurate expanded state and
a relationship to its controlled region. Preserve a visible route back to the main
content. Avoid click-only containers and icon-only controls without names.

Use tabs for switching among panels within a context, not as decorative styling
for unrelated links. Follow the chosen tab pattern's keyboard and selection model.
Automatic activation is appropriate only when panel display is effectively immediate;
otherwise separate focus movement from activation. Keep inactive panels from leaving
stray reachable controls.

## Dialogs and overlays

Use the existing accessible primitive or native dialog where suitable. A modal needs
an accessible name, deliberate initial focus, containment while open, a reachable
close action, and logical focus restoration. Escape normally dismisses the dialog.
Background content must not remain interactable while presenting a true modal.
Do not trap focus in a non-modal popover by accident.

Choose initial focus according to content and risk; not every dialog should focus
the first input. Complex content may need its opening heading or explanatory text
as the focus destination. Preserve the user's position when returning. Avoid
hiding the focused element during a close transition.

## Visual and responsive constraints

A sticky header must not cover anchors or focused controls. Use appropriate scroll
padding/margins, then test the real layout. Keep overflowed menus within the viewport
and usable with a software keyboard. At zoom, a full-screen mobile navigation can
be more reliable than a cramped floating panel, but it still needs correct semantics.

A fancy entrance should not delay interaction or make Escape wait. Keep a stable
backdrop and target boundaries. Treat `mix-blend-mode: difference` as an effect,
not a guarantee of contrast against arbitrary imagery.

**Test:** keyboard-only open/use/close, visible focus, focus return, outside click
where appropriate, Escape, long menu labels, browser zoom, nested overlays, touch,
and blocked or delayed animation. Automated checks alone cannot verify the whole
interaction model.

## Sources

[WAI-ARIA Authoring Practices patterns](https://www.w3.org/WAI/ARIA/apg/patterns/); [APG: Tabs](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/); [APG: Modal dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/); [WAI: Focus Not Obscured (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html).
