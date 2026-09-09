# Technique: producing and debugging browser 3D

**Load when:** implementing, importing, exporting, integrating, or debugging actual
mesh-based 3D. Use [art direction](technique-3d-art-direction.md) for image-making
decisions and [rendering](technique-rendering.md) for shared fallback/semantics.

## Select assets and tooling deliberately

Inspect installed manifest/lockfile versions and renderer/backend support before
using APIs or selecting dependencies. Prefer an existing compatible renderer.
Three.js, React Three Fiber (R3F), and Blender are optional; do not force React,
WebGPU migration, installation, accounts, or hosted rendering. If a required tool
is unavailable, report the blocked operation and continue independent work.

Inspect user assets first. Use approved licensed assets when they fit identity;
procedural modeling for original controllable forms; optional local Blender when
its modeling/export tools add value. Request missing identity-critical geometry
instead of guessing a real product. Record author, source, license, permitted use,
and derivatives using [assets](assets.md). Keep customer originals, large authoring
files, and generated caches outside the distributed skill.

For imports, inventory dimensions, units, axes, bounding boxes, hierarchy, pivots,
normals, UVs, materials, textures, animation tracks, and external resource URLs.
Inspect glTF JSON/extensions and network requests; GLB packaging does not prove no
external references. Do not run embedded downloaded scene scripts. Resolve resources
to inspected permitted locations before load, rather than allowing hidden fetches.

glTF/GLB delivers runtime geometry, PBR materials, and supported animation data;
it is not a portable Blender scene. Core animation channels cover node translation,
rotation, scale, and morph weights; arbitrary material animation needs separately
supported extensions. `KHR_lights_punctual` covers directional, point, and spot lights,
not a complete studio world. Check the installed exporter and loader's extension
intersection. Bake procedural noise/color-ramp appearance to UV-mapped images when
the exporter cannot represent those nodes; bake constraint-driven motion to supported
transform/skin samples when necessary and inspect the exported animation.
Lights, world shading, compositing, and arbitrary node graphs do not transfer
unchanged. Test the actual browser result before accepting an export.

Optional Blender procedure: retain the original; create named objects/materials and
explicit units in a task-owned scene; model purposeful silhouette and edges; establish
origins/parent groups; record reproducible operations or a local script; export the
selected intended objects; reload and render the exported asset in the target runtime.
For an original dial, reproducible operations could be: create a 64-sided cylinder
with radius 1 and depth .24; bevel its rim .035 with three segments; name it
`dial-shell`; create a smaller separate grip ring and inset face sharing its axis;
assign shell/face/metal-accent materials; parent parts to `dial-root`; retain their
local transforms; export that selection and compare front/three-quarter renders.
These are tunable conceptual proportions, not a tested Blender recipe or a real
product specification. Inspect the local operator's supported arguments before scripting export. Do not
blindly apply transforms or merge nodes used for animation or selection. Preserve
original transforms and a small reproducible source for fixtures.

For an executable non-Blender authoring path, inspect the original
[asset author](../examples/author-asset.py), then `mountScene()` in
[scene.js](../examples/scene.js) for actual glTF loading. Its `sampleAssembly()`
evaluates canonical part offsets; `frameCamera()` and `projectLabels()` show
container-aware framing and coordinate projection. Follow the example's run and
validation record before assuming those specific visual decisions fit another object.

Compression is conditional on measured transfer/decode needs. Draco/Meshopt geometry
and KTX2 textures require compatible decoder/transcoder configuration. Inspect
extension support for installed versions, host required decoder files within approved
asset delivery, and test failures; compression can add startup work. Do not copy an
unverified exporter command or assume every extension is supported automatically.

## Ownership, initialization, and updates

Keep HTML explanation and controls visible before renderer startup. Isolate client-only
renderer construction from SSR where required. Handle loading/error/ready explicitly;
ignore stale async results after teardown and release their owned resources. Measure
the canvas container, update backing resolution/DPR and projection on resize, then
resample the intended scene state. Do not measure only the browser window.

One render-loop owner updates input, authored state, world matrices, labels, and
rendering in order. One writer owns each transform. Separate user orbit, authored
camera, and imported tracks into explicit modes or groups; disable/rebase controls
when transferring ownership. Use elapsed seconds for time-based movement. No
per-frame reactive state updates or temporary-vector allocation when reusable values
will do. See [choreography](technique-choreography.md) for replay and simulation rules.

For reversible part motion, snapshot local position/quaternion/scale once after
asset preparation. Evaluate from that baseline, never add an offset each frame:

```js
// Three.js: original and offset are retained Vector3 instances.
part.position.copy(original).addScaledVector(offset, progress);
```

Offsets are in the part parent's coordinate space. Use a separate parent group
when imported tracks own the part. Quaternion rotation needs a retained baseline
and an explicit interpolation target, not cumulative Euler increments.

Demand rendering suits settled scenes. R3F `frameloop="demand"` needs `invalidate()`
for external mutations; invalidation schedules a frame, not synchronous rendering.
Keep invalidating while damping, authored motion, or camera movement continues.
For Three.js controls, update while damping/auto-rotate is active; use the documented
delta-seconds argument for frame-rate-independent auto-rotation. Resume without
overriding explicit user pause. Reuse [lifecycle](implementation.md#lifecycle-and-state).

Dispose only scene-owned geometries, materials, textures, render targets, controls,
listeners, and loops. Removing a mesh is not GPU disposal. Shared/cached resources
need an explicit lifetime; do not traverse-dispose another consumer's assets.
ImageBitmap-backed resources can need separate `close()` handling when exclusively
owned. On context loss, retain functional HTML and report failure; restore/rebuild
only through the renderer's supported lifecycle. Test repeated mount/unmount.

## Spatial annotations and interaction

Store an anchor in its part's local coordinates. Update world matrices, transform
the anchor to world space, then project through the current camera to normalized
device coordinates. Map to the canvas's CSS rectangle, accounting for its page
offset, not DPR pixels. Reject points behind the camera/outside its frustum; check
depth or raycast for occlusion when labels must describe visible surfaces. Resolve
label collisions by priority/alternate positions or a separate annotation list.
Keep full meaningful HTML text available even if a floating label is suppressed.
Provide keyboard/touch part selection and named view controls alongside dragging.

## Diagnose the rendered symptom

Freeze at the failing state, capture the actual view, inspect one cause class,
apply one targeted remedy, and compare. Avoid changing camera, lights, and materials
simultaneously.

| Symptom | Likely causes → inspection → targeted remedy |
|---|---|
| Blank scene | Load error, zero canvas, hidden/culled mesh → network/console/bounds → fix resource, size, or frustum first |
| Flat/cheap | Poor silhouette, frontal light, uniform response → neutral-material/grazing-light render → refine form or separate highlights |
| Floating | Ground gap or absent contact → side view and shadow receiver → correct contact and shadow coverage |
| Wrong colors/materials | Color-space error, normals, exposure, transparency → inspect maps and neutral light → mark color textures sRGB, leave data maps uncolored, correct normals/tone pipeline |
| Clipped product | Animated bounds exceed frustum → project extrema in all states → refit camera and near/far range |
| Broken pivots | Wrong origin, parent space, competing tracks → axes and hierarchy → dedicated pivot group; preserve original transforms |
| Detached labels | Stale matrices, wrong space, fixed pixels → inspect projected anchor and canvas rect → update coordinate chain/collision rules |
| Fighting camera | Controls and timeline both write → disable each in turn → explicit ownership handoff |
| Stutter | Main thread, draw calls, fill/overdraw, decode, shader compile → profile each separately → target measured bottleneck |
| Leaks | Unreleased resources/listeners or cache confusion → repeated mount and memory trend → repair ownership and teardown |

## Measure and accept

Record device, browser, renderer/backend, viewport/DPR, asset bytes, test duration,
and method. Separate CPU frame work from GPU cost; renderer draw-call counters do
not measure GPU time. Compare resolution reduction (fill rate), effect removal
(shader/postprocessing), texture sizes (memory), draw-call reduction, and asset
transfer/decode independently. Choose quality tiers from those measurements; no
universal triangle budget or powerful-desktop performance claim.

**Verify:** actual loaded/exported appearance, random progress/reverse/replay,
resize, asset failure, context failure, touch/keyboard, runtime reduced-motion change,
user pause, and repeated mounting. Inspect stills and playback. Software/headless
rendering can verify function and composition, not representative GPU performance.
**Fallback:** useful semantic part list and labeled static views with normal actions;
report unavailable essential 3D interaction honestly.

## Sources

Reviewed 2026-09-09: [GLTFLoader](https://threejs.org/docs/pages/GLTFLoader.html),
[OrbitControls](https://threejs.org/docs/pages/OrbitControls.html),
[R3F demand rendering](https://r3f.docs.pmnd.rs/advanced/scaling-performance),
[R3F pitfalls](https://r3f.docs.pmnd.rs/advanced/pitfalls),
[official Blender glTF exporter](https://github.com/KhronosGroup/glTF-Blender-IO).
[glTF specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
defines core channels; extension support remains version-specific.
Check the [Blender manual](https://docs.blender.org/manual/en/latest/addons/scene_gltf2.html)
matching the installed version before export; this is not a tested Blender command recipe.
