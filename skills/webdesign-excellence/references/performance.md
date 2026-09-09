# Performance: the visual budget must be earned

**Load when:** introducing media, fonts, motion, expensive layers, or assessing page responsiveness.

## Separate targets from measurements

Core Web Vitals currently define good thresholds as LCP ≤2.5s, INP ≤200ms, and CLS
≤0.1, assessed at the 75th percentile of real-user visits with the relevant device
segmentation. A local Lighthouse run is diagnostic, not proof that the field
thresholds pass. Report the device, throttling, cache state, and measurement scope.
Recheck metric definitions when maintaining this skill.

Choose project budgets for critical images, fonts, JavaScript, rendering area,
and frame work. There is no universal transfer-size budget that fits every page.
An intentional large media asset needs evidence of value and a plan for constrained
conditions, not a “premium” exemption from performance.

## The first useful view

Make the LCP resource discoverable early and avoid lazy-loading the known LCP image.
Use appropriate resource priority deliberately, not on every image. Do not make
critical content wait for JavaScript, a cosmetic intro, or a late CSS background
request when a better structure is available. Reserve dimensions for images,
embeds, and other asynchronously inserted content.

Load only needed font variants; control fallback behavior and layout movement.
Do not preload the entire type family. Avoid third-party embeds and runtime
libraries when a static or native representation achieves the goal.

## Interaction and rendering

Keep pointer and scroll effects from monopolizing the main thread. Profile layout,
paint, rasterization, compositing, and memory rather than relying on property-name
folklore. Transforms and opacity are often efficient, but layer count, filtered
area, and backing resolution can make a simple-looking effect expensive.

Avoid framework state updates on every visual frame. Scope listeners and observers,
stop idle rendering, and release resources. Do not add `will-change` globally or
permanently promote every card. Test cleanup through repeated navigation.

For a selected renderer, use the [3D profiling and diagnosis procedure](technique-3d-production.md)
to distinguish transfer/decode, main-thread, draw-call, fill-rate, and resource costs.
For supplied media, use [existing video](technique-video.md) before choosing scrubbing.

## Decision rule

Compare the effect on and off under realistic conditions. Keep it only if its
communication value is worth the measured cost. Degrade expensive decoration before
removing essential content. Do not replace a poor-performing animation with a
static image so large that the loading experience becomes worse.

**Test:** cold load, warm navigation, slow network, CPU throttling, modest GPU,
image/font failures, hidden tab, reduced motion, long content, and multiple mounted
views. Record measurements and limitations; never invent a perfect performance score.

## Sources

[web.dev: Web Vitals](https://web.dev/articles/vitals); [web.dev: Optimize LCP](https://web.dev/articles/optimize-lcp); [web.dev: High-performance CSS animations](https://web.dev/articles/animations-guide).
