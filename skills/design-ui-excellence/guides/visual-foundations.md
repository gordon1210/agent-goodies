# Visual Foundations: Hierarchy, Type, Color, Spacing & Layout

Use this guide when composing or auditing the visual system beneath a page or interface.

The goal is controlled relationships, not universal magic numbers.

## Visual hierarchy

Decide the intended attention order before styling.

Use:

- scale
- weight
- contrast
- position
- whitespace
- density
- imagery
- motion

Do not let every heading, card, button, badge, and illustration compete. One primary element should dominate each view or decision point.

Run a squint test on the rendered surface: major groups and the primary action should remain legible as shapes.

## Layout and grid

- Start from content hierarchy and expected reading order.
- Use a consistent container and alignment logic.
- Let important elements break the grid only intentionally.
- Keep related items closer than unrelated groups.
- Align comparable data and controls.
- Avoid empty columns and decorative imbalance.
- Use intrinsic sizing, `minmax(0, 1fr)`, wrapping, and content-driven breakpoints where appropriate.
- Test minimum and maximum content, not only the ideal fixture.

Asymmetry can create identity, but it must preserve reading order and responsive stability.

## Typography

Define roles rather than assigning sizes ad hoc:

- display
- page title
- section heading
- body
- supporting text
- label
- data
- code

Check:

- family supports required scripts and weights
- contrast between roles is clear
- line length is comfortable for the reading mode
- line height fits type size and density
- headings wrap at meaningful points
- UI labels remain single-line where wrapping would break controls
- numeric values align when comparison matters
- browser font loading does not destabilize layout

Do not reject a font because it is common. Reject it when it fails brand, language, readability, or system requirements.

## Color

Start with semantic roles:

- page background
- surfaces
- primary and muted text
- action
- border/divider
- focus
- success, warning, error, information
- data series

For every foreground/background pairing in use, verify whether it is valid for:

- normal text
- large text
- icons and graphical objects
- state-carrying boundaries
- decorative boundaries

Never rely on color alone for state. Do not assume a light label works on every saturated fill.

Use accent color to establish hierarchy. If everything is accented, nothing is.

## Spacing

Use a limited scale that fits the project. Relationships matter:

- internal spacing groups a component
- external spacing separates components
- section spacing reflects narrative importance
- dense operational UI uses tighter, stable rhythm
- marketing moments may use larger pauses

Nested elements should feel geometrically related. Internal padding should not create a more generous gap inside a component than between unrelated components without a deliberate reason.

## Shape and surface

Define what radius, border, shadow, and fill mean.

- Use radius consistently by component role.
- Keep nested radii visually concentric.
- Use borders for structure or state.
- Use elevation for actual layering.
- Avoid shadows on every surface.
- Do not mix pills, sharp rectangles, and soft cards without semantic logic.
- Overlays must separate clearly from the background and preserve focus.

## Density

Choose density from task frequency, information volume, and device:

- persuasive pages can pace information
- editorial surfaces need readable measure
- dashboards need scanable density
- touch surfaces need adequate targets
- expert tools can be compact without becoming ambiguous

Whitespace is a tool, not proof of quality.

## Responsive foundations

Define behavior, not only breakpoints:

- content priority
- grid collapse
- order changes
- navigation adaptation
- control reflow
- media crop
- data table strategy
- readable measure
- long-word handling
- safe-area behavior

Never fix overflow by hiding meaningful content globally.
