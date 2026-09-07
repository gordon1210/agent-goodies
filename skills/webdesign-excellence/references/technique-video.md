# Technique: video-led heroes and moving media

**Load when:** moving media is selected for a narrative or product explanation.

## Prove the poster first

Choose a first frame that already communicates the intended message. Define mobile
and desktop crops and a stable text contrast region. A video is not an excuse to
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

Pause work when off-screen or the document is hidden. Avoid continuously decoding
several unseen videos. Reduced-motion mode should ordinarily keep a still poster
for decorative backgrounds; essential demonstrations can remain user-initiated.
Do not assume autoplay availability from desktop testing.

## Moving-content obligations

Automatically starting movement lasting more than five seconds and shown alongside
other content generally needs a pause, stop, or hide mechanism unless essential.
Auto-updating information has its own criterion conditions. Merely pausing while
a pointer hovers is not a complete broadly operable control. Apply the standard's
actual scope rather than treating every short transition as a violation.

Provide a discoverable keyboard-operable playback or effects control where required.
A change of scene should not suddenly invert the contrast behind text. Avoid rapid
flashes and strong involuntary zoom or parallax.

**Fallback:** a meaningful poster with normal content and actions. **Test:** slow
connection, failed download, blocked autoplay, reduced motion, background tab,
mobile crop, captions, pause persistence, and memory/decoding behavior.

## Sources

[WAI: Pause, Stop, Hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html).
