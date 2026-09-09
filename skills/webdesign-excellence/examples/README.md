# Original form and sequence examples

Selectively open these examples when implementing choreography or real 3D. They
are an isolated teaching harness, not a site template or normal skill dependency.
No fonts, media, libraries or resources are fetched from external hosts.

## Run

Python 3.10+ serves the files. A and B use browser APIs only. C uses an **already
installed Three.js package**, tested with 0.185.1. Point to its package directory;
do not copy node_modules into this skill. No install occurs in these commands.

```sh
python3 skills/webdesign-excellence/examples/serve.py --three-root /absolute/path/to/node_modules/three
```

Open `http://127.0.0.1:8765/`. Without `--three-root`, A/B and the media specimen
still run and C exposes its semantic alternative. This is an unavailable-tool
fallback, not completion of a brief that explicitly needs interactive 3D. The
server binds only loopback and confines paths to the example or specified renderer.
The harness needs HTTP module loading, ResizeObserver, modern CSS and WebGL2 for C.
Only Chromium 152.0.7977.76 was tested; other browsers are unverified.

## What to inspect

- **A — kinetic composition:** [motion.js](motion.js), `sampleKinetic(p)`, owns all
  scene property writes. A persistent coral point connects one idea to a clear
  direction; an entry hold, connection, handoff and settled hold are sampled
  without historical callbacks. Six seconds is this example's tuned duration,
  not a recommended universal cadence. Pause/replay/range controls remain live.
  Static explanatory text and the reduced-motion final state preserve the message.
- **B — product workflow:** [motion.js](motion.js), form submit handler. The selected
  edition name, page count and coral identity carry into a revealed calculation
  path. The actual 50-copy arithmetic result is available immediately, independent
  of motion. A subsequent selection invalidates the old estimate. This is explicitly
  illustrative local data, not network progress, live pricing or stock status.
- **C — loaded multipart 3D:** [scene.js](scene.js), `mountScene`, `sampleAssembly`,
  `frameCamera`, `projectLabels`. A flared rolled-rim shade, diffuser, stem, foot
  and cap form an original fictional light. Warm key/cool separation, a matte
  shell, contrasting diffuser and grounded shadow explain its proportions.
  Absolute retained transforms prevent drift; the fixed reveal envelope fits
  wide, narrow and short canvases. HTML descriptions and keyboard-accessible
  controls retain meaning outside the renderer. Projected labels test occlusion
  and collisions and defer to the full DOM list when hidden. This is not a CAD
  model, real product internals, free-orbit inspector or production quality tier.
- **Optional existing video:** [video.html](video.html), [video.js](video.js).
  File selection integrates the actual local asset through an object URL. It does
  not reconstruct it or request generation. A separately labeled button produces
  a small synthetic circle clip with native MediaRecorder for decoder tests only.
  The media timeline owns the displayed timestamp, with rVFC and seek/timeupdate
  fallback. Offscreen observation pauses playback without automatic resume; if IntersectionObserver is absent, user controls and document visibility still work. No autoplay, upload, source mutation, audio muting or scrubbing promise.
  Arbitrary-file codec/audio inspection still requires an actual media inspector.

## Reproduce the asset

```sh
python3 skills/webdesign-excellence/examples/author-asset.py
```

[author-asset.py](author-asset.py) uses only Python's standard library and writes
[assets/lumen.gltf](assets/lumen.gltf). This original task-authored fixture contains
five named meshes, embedded geometry, material definitions and no textures or
external URIs. It inherits the repository's licensing terms. No third-party model,
customer asset, technical internals or downloaded script was incorporated. The
radial sections are the retained editable source; rendered review corrected face
winding and the shade's outward normals before acceptance. Byte-for-byte reproduction verified; SHA256 `bda80ffde64373424ace8c69e5a75c37f4939c47ca020c14509a57c7a31542cb`. Buffer: 79,968 bytes;
uncompressed glTF file 110,874 bytes. Compression was unnecessary here.
The synthetic clip is created in memory, is not user-supplied footage and is never
included as a campaign asset. FFmpeg and Blender were unavailable and not installed.
The final synthetic specimen run observed 12,551 blob bytes, fetch-reported MIME
`video/webm`, 640×360 decoded pixels and 1.965724 seconds. The authoring intention
is two seconds at 30 requested capture fps; encoder scheduling makes this fixture
variable, not frame-exact. These observations do not inspect arbitrary-file codecs
or source audio.

## Execute checks

Syntax checks do not execute browser assertions:

```sh
node --check skills/webdesign-excellence/examples/motion.js
node --check skills/webdesign-excellence/examples/scene.js
node --check skills/webdesign-excellence/examples/video.js
node --check skills/webdesign-excellence/examples/test-browser.js
```

With the server running and an existing Playwright installation:

```sh
node skills/webdesign-excellence/examples/run-browser.mjs /absolute/path/to/node_modules/playwright
```

Alternatively pass the absolute path of [test-browser.js](test-browser.js) as the
`filename` argument to Playwright's `browser_run_code_unsafe` tool. The file is a
page-accepting test expression, not a self-starting Node test. Only execute this
maintained local source. That tool route was executed on 2026-09-09: **30 assertions
passed**, including direct/reverse sampling, fixed anchor, explicit pause, truthful
calculation and identity transfer, actual canonical part positions after reassembly,
responsive overflow, preference changes, remount, stale failed/successful load isolation,
persisted page and media lifecycles, missing asset/renderer, context loss, synthetic playback,
timeline seek and pause preservation through hidden/visible events, active interruption, media error and offscreen pause. Context loss and persisted lifecycle events were injected, not
claims of real GPU loss or successful browser bfcache admission. The media lifecycle test
retains the existing blob URL through injected persisted pagehide/pageshow, confirms
explicit pause, then executes playback and rVFC callbacks again. Persisted departure
stops an in-flight synthetic capture without replacing the selected clip; final
departure releases its owned URL. Restoration never starts playback automatically. The independent
CLI wrapper was syntax-checked but not executed in this checkout.

Visual review inspected PNGs at 1280×900, 390×720 and 1000×450: silhouette, shade
surface, base contact, exploded part order, framing and labels; kinetic connection
and reduced state; workflow result; synthetic video seek. Evidence is outside the
package at `/tmp/webdesign-3d-{wide,exploded,narrow,short}.png`,
`/tmp/webdesign-kinetic-{middle,reduced,narrow,short}.png`, `/tmp/webdesign-workflow.png` and
`/tmp/webdesign-video.png`. These task-local artifacts are not distributed.
A live playback recording was captured at
`/tmp/webdesign-motion-recordings/page@dac5ddb97fa5a9f712d0df2f8a6db89e.webm`;
continuous playback smoothness was not visually reviewed. Still review and state assertions do not establish smoothness on target hardware.

Measured in Chromium 152 on macOS (navigator reports MacIntel), DPR 1, 1280×900:
11 rendered calls, 7,938 rendered triangles including shadow passes, six geometries.
A tight 60-sample loop around sampleAssembly measured median 0.10 ms and p95 0.30 ms
CPU submission time. This excludes GPU completion, decode and display pacing, and
is **not representative GPU performance evidence**. Renderer is demand-driven
outside the user-initiated 650 ms reveal. There is no production performance claim.
Assistive-technology behavior, real source audio, arbitrary codecs, low-end GPU
performance, cross-browser playback and general agent skill gains remain untested.

Technical API references reviewed 2026-09-09: [Three.js documentation](https://threejs.org/docs/),
[MDN animation sampling](https://developer.mozilla.org/en-US/docs/Web/API/Animation/currentTime),
[MDN video frame callbacks](https://developer.mozilla.org/en-US/docs/Web/API/HTMLVideoElement/requestVideoFrameCallback).
Composition and tuning are original design choices; measured observations are
limited to the environment and method stated above.
