# Shaders and VFX

Use for `.gdshader`, ShaderMaterial, compute shaders, screen textures, particles and effects.

## Establish shader context

Confirm shader type (`canvas_item`, `spatial`, `particles`, `sky`, `fog` or compute), renderer, coordinate spaces, blend/depth modes and target platforms. Do not copy shader snippets across contexts without adapting semantics.

## Uniforms and materials

Use typed uniforms, hints and sensible defaults. Keep per-instance variation out of duplicated materials when instance uniforms or authored parameters fit. Avoid mutating a shared material accidentally.

Document coordinate-space expectations for vectors, normals, depth and screen UVs. Reconstruct positions using the exact matrices and depth convention of the project version.

## Screen-reading effects

Screen/depth/normal textures have renderer and ordering constraints. Avoid assuming transparent objects, multiple screen-reading materials or subviewports compose automatically. Test overlapping effects and target renderers.

## Performance

- Avoid unbounded loops and divergent expensive branches.
- Limit texture samples, high-frequency noise and overdraw.
- Keep particle counts, trails and collision modes within measured budgets.
- Understand shader variant growth from render modes/features.
- Prefer lower-resolution buffers for suitable full-screen effects.
- Profile GPU time; CPU frame time cannot diagnose shader cost.

## Compute

Validate device/renderer support, buffer sizes, dispatch dimensions and synchronization. Never trust GPU-generated indices or lengths without bounds. Keep a fallback when required by supported hardware.

## VFX ownership

Effects should react to authoritative events without owning gameplay outcomes. Pool only when spawn/destruction cost is measured and reset semantics include particles, materials, timers and audio.

## Verification

Compile on each supported renderer, inspect editor and exported builds, test missing textures/default uniforms, overlapping transparency, resize/subviewport behavior and low/high quality settings. Capture GPU timings before claiming an optimization.
