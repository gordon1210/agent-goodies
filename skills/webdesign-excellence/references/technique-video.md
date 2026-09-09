# Technique: optional existing-video integration

**Load when:** integrating an actual supplied or approved existing video into a web
page. This separately selectable route is optional, not a nested skill. Example:
“Use webdesign-excellence to integrate my supplied product-demo.mp4 as an inline
player, preserving its audio.” No slash command or video-generation workflow is
implied. [Reference reconstruction](technique-motion-reference.md) is a different
operation; an attachment alone does not resolve which operation the user wants.

## Inspect the available asset

Confirm the file is accessible before promising a result. With available approved
local tools, inspect duration, dimensions/aspect, bytes, container/codec, audio,
and transparency when relevant. Watch representative content and sample around
transitions; record important subjects and text safe areas. Separate observed
metadata from assumptions. If the asset is missing, request that essential input,
build independent layout, and mark playback checks unexecuted.

Classify its role: meaningful player/demo, decorative background, inline supporting
media, advanced scroll-linked scene, or renderer texture. Choose the simplest mode
meeting the request. A supplied recording does not authorize generation, uploading
to external tools, a new player dependency, tracking, or unrelated media downloads.
Preserve meaningful source audio and original footage; do not silently mute, trim,
or otherwise modify it beyond the task.

## Prove the poster first

Choose a representative poster that already communicates the intended message; it
need not be the source's first frame. Reserve dimensions/aspect before loading. Define mobile
and desktop crop/contain behavior and a stable text contrast region. Use contain
when cropping would remove essential demonstration content. A video is not an excuse to
leave the page blank while loading. Do not turn a decorative movie into the first
critical download without measuring its impact.

Distinguish meaningful video from decorative background footage. Meaningful media
needs appropriate captions, transcript or descriptive alternatives, and controls
for its actual content. Decorative media should not create a misleading accessible
name or duplicate adjacent meaning. Do not autoplay audible media.

## Loading and playback

Use approved local or trusted media with rights recorded. Choose file size, duration,
resolution, codec, and playback method based on actual delivery needs. A short
loop may not need a streaming library. Let user-initiated playback defer expensive
resources when that suits the story. Handle a rejected `play()` promise without
hiding the poster or leaving a false playing state.

Track explicit user pause separately from temporary offscreen/visibility suspension;
returning onscreen must not undo a deliberate pause. Pause work when off-screen or
the document is hidden. Avoid continuously decoding
several unseen videos. Reduced-motion mode should ordinarily keep a still poster
for decorative backgrounds; essential demonstrations can remain user-initiated.
Do not assume autoplay availability from desktop testing.

## Follow the media timeline

For synchronized overlays, derive state from media time, never a separate elapsed
clock. Feature-detect `requestVideoFrameCallback`; its `metadata.mediaTime` identifies
the presented frame's media timestamp. Re-register callbacks while needed and cancel
them on teardown. Callback timing is limited by browser paint/video frame rates and
main-thread scheduling; it does not guarantee frame-exact DOM/video compositing.
For older browsers, a playback-only animation-frame loop reading `currentTime` can
drive approximate overlays; `timeupdate` is suitable for coarse state, not smooth
frame matching. Resample on `loadedmetadata`, `seeked`, pause, and ended; do not
assume a seek displays its requested frame synchronously. Keep essential information
in persistent HTML rather than a fleeting overlay.

The optional [video specimen](../examples/video.js), particularly `requestFrame()`,
demonstrates media-time observation and cancellation using a synthetic local fixture.
Its frame-callback path and event fallback have different timing precision; consult
the example validation record for which browser behavior was actually exercised.

Scroll scrubbing is an advanced conditional route: inspect seekable ranges and test
decode/seek latency under realistic scrolling before committing to it. Keyframe
spacing, resolution, codec, and device affect results. Coalesce desired times and
bound outstanding seeks; do not default to writing `currentTime` every scroll frame
or exporting huge image sequences. Use normal user-played video or static chapters
when the source cannot scrub reliably. A video texture also inherits playback
errors, media readiness, and renderer resource ownership; see [3D production](technique-3d-production.md).

## Local derivatives, only when needed

FFmpeg/metadata tools are optional available capabilities, not installation
requirements. Inspect the actual local version/options before issuing commands.
For authorized poster extraction, trimming, or transcode, retain the source, use
a distinct derivative path, record purpose and settings, and verify dimensions,
content, codec and audio afterward. Do not overwrite the original or upload it.
A synthetic test clip must be labeled synthetic; it is not inspected campaign media.

## Moving-content obligations

Automatically starting movement lasting more than five seconds and shown alongside
other content generally needs a pause, stop, or hide mechanism unless essential.
Auto-updating information has its own conditions; apply the criterion's actual scope.
Reuse [accessibility](accessibility.md), [motion](technique-motion.md), and
[performance](performance.md) for controls and shared checks. Hover-only pausing is
insufficient. Keep overlays readable through scene changes and provide a discoverable
keyboard-operable playback/effects control where required.

**Fallback:** a meaningful poster with normal content and actions. **Test:** slow
connection, failed download, blocked autoplay, reduced motion, background tab,
mobile crop, captions, pause persistence, and memory/decoding behavior.

## Sources

Reviewed 2026-09-09: [WAI: Pause, Stop, Hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html),
[MDN: requestVideoFrameCallback](https://developer.mozilla.org/en-US/docs/Web/API/HTMLVideoElement/requestVideoFrameCallback),
[MDN: seeked](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/seeked_event).
