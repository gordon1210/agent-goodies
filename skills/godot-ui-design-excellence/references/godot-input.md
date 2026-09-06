# Godot focus, input ownership, and real modality

## Input is more than one callback

Godot distinguishes general input dispatch, GUI input, shortcuts, and unhandled
input. Disabling `_input()` processing on a parent is not a universal GUI blocker,
and consuming an event does not disable independent polling through the `Input`
singleton. A gameplay system that polls movement or attack needs its own input
context gate while a blocking UI owns the interaction.

Use the project's existing input-context system where one exists. Keep supported
actions semantic and rebind-aware. Do not globally repurpose UI navigation actions
for gameplay without considering focus and dialog behavior.

## Choose a modal mechanism deliberately

A supported `Window`/dialog transient/exclusive arrangement may provide the desired
behavior; verify embedding, parent relationships, and platform behavior. For
Control-based overlays, implement explicit scope ownership rather than assuming
that draw order or one full-screen rectangle creates complete modality.

In reviewed Godot 4.7 APIs, recursive mouse/focus behavior can gate a subtree, but
an explicitly enabled descendant can override a disabled ancestor. Audit overrides
and preserve previous values. Older versions require an equivalent supported scope
strategy; never copy a new property into an older scene and hope it works.

## Modal lifecycle contract

The following is an algorithm, not invented Godot API:

1. Record the previous valid focus and the lower scope's interaction settings.
2. Activate the new scope; block underlying pointer, navigation, shortcuts, and
   gameplay action paths according to modality. Decide whether simulation pauses.
3. Put initial focus on a safe meaningful control after it is in the tree, visible,
   and focusable. Constrain focus neighbors and tab order to the active scope.
4. Handle back/cancel once. Prevent the opening input's remaining press/release
   phase from activating a default action or leaking to the lower scope.
5. On dismissal, restore the exact previous policy and valid prior focus, or a
   documented fallback. A freed, hidden, or disabled control is not a valid target.

Nested overlays require a stack of ownership/restoration records, not one global
`previous_focus` value. Hidden overlays must stop accepting actions; animations
must not determine authority merely because they are still visible.

## Device coexistence

Switch prompt glyphs from meaningful device input, accounting for analog deadzones
and a small anti-flicker policy. Do not erase logical selection when the mouse
moves. Keep focused items scrolled into view and rebuild explicit neighbors after
layout changes. For large grids, focus logical items, not stale recycled cells.

Test keyboard, controller, pointer, hotplug, rebinding, rapid back/confirm, nested
modals, and gameplay polling under an overlay. No successful screenshot can verify
these behaviors. Report exactly which devices were actually exercised.

## Evidence anchors

[G04](sources.md#g04) · [G13](sources.md#g13) · [G21](sources.md#g21) · [G27](sources.md#g27) · [G29](sources.md#g29) · [X112](sources.md#x112) · [X113](sources.md#x113)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
