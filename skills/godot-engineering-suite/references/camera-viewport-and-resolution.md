# Camera, viewport, and resolution

Use for cameras, aspect ratios, stretch policy, subviewports, split-screen, minimaps and render textures.

## Define the display contract

Document:

- authored base resolution;
- stretch mode/aspect policy;
- minimum supported window or viewport size;
- ultrawide, portrait and safe-area behavior;
- pixel-perfect requirements;
- dynamic resolution or render scaling;
- UI scale policy.

Do not fix a layout by hard-coding one desktop resolution.

## Camera ownership

A scene or coordinator should clearly own the active camera. Separate target tracking, look-ahead, bounds, shake and cutscene control into composable behavior where they can overlap. Do not mutate the gameplay target to create camera effects.

## Multiple viewports

Subviewports introduce separate worlds/canvases, input routing, update modes and texture lifetimes. Use them for real isolation: split-screen views, portals, minimaps, UI previews or lower-resolution rendering. Avoid them for ordinary panels.

Explicitly configure:

- viewport size and resize behavior;
- world sharing versus separate worlds;
- update and clear modes;
- input forwarding;
- audio listener/camera ownership;
- texture filtering and HDR requirements.

## Coordinate conversion

When mapping pointer positions or world coordinates across viewports, use the relevant canvas and camera transforms. Do not assume screen coordinates equal local Control or world coordinates.

## Resolution changes

React to viewport size changes through containers and anchors where possible. Recompute camera limits, render targets and projection-dependent values only when necessary. Avoid per-frame layout reconstruction.

## Verification matrix

Test windowed/fullscreen transitions, DPI scaling, at least one narrow and one wide aspect ratio, resize during gameplay, UI focus, mouse mapping and any subviewport input. For pixel art, inspect integer and non-integer scales for shimmer and seams.
