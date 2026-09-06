# Godot layout: separate composition, allocation, and drawing

## Use three coordinate concepts explicitly

Distinguish logical UI coordinates, rendered viewport pixels, and OS display/window
coordinates. A reference-resolution design does not imply that each logical unit
is one physical screen pixel. Record stretch mode, aspect policy, content scaling,
and any separate 3D rendering scale before computing margins or sizes.

`canvas_items` with an intentional reference resolution is a useful non-pixel-art
starting point, not a mandatory setting for every project. Preserve an established
policy unless a measured defect requires change. A lower-resolution 3D world need
not force text to be rendered at that same resolution.

## Allocation versus composition

Use Containers for flowing text, repeated rows, grids, padding, and flexible groups.
Their layout owns the position and size of managed children. A `PanelContainer`
is still a Container, not an escape from container layout. For deliberate free
composition, put a plain `Control` layout slot inside the surrounding container,
then position internal children within that slot.

Use anchors plus explicit offsets deliberately. Setting anchors alone does not
necessarily reset existing offsets. Where the intended operation changes both,
use the appropriate anchor-and-offset API for the installed version. Fixed logical
measurements inside a responsive region are valid; scattered absolute window
pixels without a scaling policy are not.

Represent expressive geometry in separate ornament layers. Irregular edges can
extend beyond a readable interior while text and input remain regular and stable.
Do not use a huge invisible decoration Control that intercepts every click.

## Responsive behavior contract

Name minimum usable size, preferred composition width, text wrapping policy, and
breakpoints based on content failure. Specify what happens at narrow, standard,
and ultrawide aspect ratios. A bounded inspection column can remain readable while
the map or background expands. Rebuild navigation when reflow changes geometry.

Test long content and large text before locking panel dimensions. Newer convenience
properties such as size limits are version-sensitive; a measured wrapper layout
may be needed on older releases. Do not add unsupported properties to `.tscn` files.

## Safe areas without coordinate mistakes

The reviewed DisplayServer documentation describes platform-specific safe-area
behavior; outside Android/iOS the returned fallback is a usable display rectangle,
not automatically a cutout inset for your game window.

For an OS-reported rectangle: establish its coordinate space; intersect with the
actual client content region; convert through the applicable window/viewport/UI
transform; then derive nonnegative local insets. Account for letterboxing, HiDPI,
window position, and embedded-window behavior. For ordinary axis-aligned roots,
transform the corners; for rotated/skewed roots, use a conservative usable region
rather than treating an enclosing rectangle as wholly safe.

Keep designed comfort margins separate from OS cutouts. No universal four-line
snippet can correctly skip these assumptions. Verify windowed and fullscreen
behavior on the actual target platform.

## Evidence anchors

[G05](sources.md#g05) · [G06](sources.md#g06) · [G13](sources.md#g13) · [G14](sources.md#g14) · [G30](sources.md#g30)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
