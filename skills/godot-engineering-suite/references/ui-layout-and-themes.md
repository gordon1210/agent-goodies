# UI layout and themes

Use for Control nodes, containers, anchors, themes, reusable widgets, HUDs and menus.

## Layout hierarchy

Prefer containers for adaptive layout and anchors/offsets for placement relative to a parent. Avoid scripts that continuously assign Control positions and sizes when the container system can express the contract.

A typical reusable widget root is a `Control` or `Container`; use `CanvasLayer` only when the entire UI needs an independent canvas layer. Keep gameplay-world UI and screen-space UI clearly separated.

## Containers

Choose the container that owns layout. Child size flags and custom minimum sizes communicate constraints; manually changing a child rect managed by a container will be overridden.

Avoid deeply nested generic containers. Every layer should have a layout responsibility such as margin, flow, grid, centering, aspect or scroll.

## Themes

Use shared Theme resources and typed theme overrides instead of individually styling every Control. Define semantic component variants through theme type variations or reusable scenes. Keep text sizes, spacing, focus visuals and disabled states consistent.

Do not mutate a shared theme/style resource per widget unless shared mutation is intended. Duplicate before runtime customization.

## Responsive behavior

Define base resolution and scaling policy in project documentation. Test translated text, long labels, narrow aspect ratios, DPI scaling and safe areas. Do not size buttons only for English strings.

Use anchors and containers before breakpoint scripts. Introduce alternate layouts when the information architecture truly changes, not for small size differences.

## Reusable components

Expose a narrow API and signals. Internal node paths remain private. Make state variants explicit: normal, focused, hovered, pressed, disabled, selected, loading and error as relevant.

## Performance

Avoid rebuilding large item trees every frame. Virtualize or recycle large lists only when needed and carefully reset state. Limit complex RichTextLabel effects, clipping layers, subviewports and unique materials after profiling.

## Verification

Inspect at supported resolutions, languages and input methods. Verify mouse filtering, clipping, scroll behavior, z/layer order, focus visibility and theme inheritance.
