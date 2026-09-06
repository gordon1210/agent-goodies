# Godot Themes and semantic component scenes

## Organize by role

Create a project UI Theme or extend the existing one. Centralize fonts, role sizes,
colors, spacing constants, icons, and StyleBoxes. Use named type variations for
semantic component families where the installed version supports them; assign
`theme_type_variation` deliberately. Do not produce dozens of arbitrary per-node
color overrides and later call that a design system.

Build reusable scenes for meaningful components such as an action row, resource
instrument, comparison section, or notification. A Theme owns shared style values;
a scene owns structure, state application, and behavior. Neither should know the
whole gameplay implementation.

## All interactive states, not just normal

Check the actual theme properties of the Control class you style. For Buttons,
normal, hovered, pressed, disabled, focus, and toggle-related appearances need a
coherent treatment; class/version details matter. A custom selected/equipped state
may need a separate persistent indicator rather than overloading the focus StyleBox.

Give focus adequate contrast and geometry even when the pointer is hovering another
item. Preserve text readability on disabled but informative controls. Do not hide
an unavailable reason behind a Control the player cannot reach or inspect.

## StyleBox choice

Use `StyleBoxFlat` for deliberate flat geometry, borders, and limited shadows;
`StyleBoxTexture` for authored scalable borders; and empty/custom structures where
an expressive composition requires them. Separate content margins from texture
and expansion margins. Test the component's minimum size after styling changes.

Not every ornament should be one giant StyleBox. A unique crest or brush edge may
be a separate noninteractive TextureRect aligned to a conventional panel interior.
This preserves flexibility when a translation or accessibility setting expands it.

## Resource ownership

Treat shared Theme, StyleBox, material, and font resources as shared unless you
explicitly create an independent instance. Mutating a shared StyleBox to highlight
one row can change its siblings. Duplicate at the appropriate depth when per-instance
mutation is necessary, or use a separate state layer that does not mutate shared
resources. Do not deep-duplicate the whole library on every hover.

Keep variants derived from a common token policy; large-text and high-contrast
modes should not fork the entire component tree unnecessarily. Test runtime changes
for relayout, focus preservation, and lingering cached measurements.

## Gallery and real-screen validation

Create a small component gallery with realistic short/long content and compound
states. Use it for comparison, not as a substitute for actual scene backgrounds.
Validate native accessibility semantics when custom drawing replaces standard
visuals. Prefer native Controls with custom appearance over hand-coded pointer
rectangles that lose keyboard, focus, and assistive behavior.

Acceptance: changing one intended semantic token affects the appropriate family
without corrupting unrelated instances; all states remain identifiable; layout
and behavior are preserved across supported scale settings.

## Evidence anchors

[G03](sources.md#g03) · [G11](sources.md#g11) · [G12](sources.md#g12) · [G13](sources.md#g13) · [G23](sources.md#g23) · [G24](sources.md#g24)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
