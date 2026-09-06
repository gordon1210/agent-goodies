# Rendering and lighting

Use for renderer selection, lighting, shadows, GI, environments, culling and post-processing.

## Renderer contract

Detect whether the project uses Forward+, Mobile or Compatibility and which target platforms constrain that choice. Do not enable a feature before confirming renderer and platform support.

Renderer changes are project-wide migrations. Compare visuals, shaders, materials, particles, post-processing and exports; do not make them incidentally.

## Lighting strategy

Choose per environment and target:

- baked lighting for mostly static geometry and predictable cost;
- dynamic lights for moving/time-varying sources;
- mixed approaches for dynamic actors in static worlds;
- GI only when the visual benefit justifies target cost and compatibility.

Do not turn on SDFGI, volumetrics, SSAO/SSIL, glow or high-quality shadows as generic quality improvements. Measure GPU time and memory on target hardware.

## Shadows

Control shadow-casting lights/objects, distances, atlas sizes and update modes. Camera far distance and cascades affect directional shadow quality. Verify acne, peter-panning and temporal instability from gameplay cameras.

## Culling and LOD

Use frustum/occlusion culling, visibility ranges, LOD meshes and impostors according to world structure. Culling setup can cost CPU/GPU memory; profile representative scenes. Do not hide gameplay-relevant objects without preserving simulation requirements.

## Environments and post-processing

Have one clear environment owner per viewport/world. Keep exposure and tonemapping consistent with authored assets. Validate HDR and SDR separately when HDR output is targeted.

## Diagnostics

Use render profiler/frame captures, monitors, overdraw/debug views and controlled feature toggles. Change one major feature at a time and retain before/after frame timings and screenshots.

## Verification

Test all supported renderers/devices affected, camera extremes, indoor/outdoor transitions and exported builds. Editor viewport appearance alone is insufficient.
