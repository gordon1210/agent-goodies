# Technique: choreographing a sequence

**Load when:** several visual changes must communicate one idea over time or scroll.
A hover, disclosure, or local transition fix uses existing tokens and
[motion](technique-motion.md), without a beat-map exercise. This is a technique,
not a primary style. Type, masks, objects, and lighting may cooperate in one
signature scene; competing attention systems are the problem.

## Design the understanding before the timeline

Classify the driver: direct feedback acknowledges input; a state transition explains
change; scroll gives the reader pacing; authored time sets a presentation's pacing;
ambient decoration must remain subordinate. Real application state authorizes real
results. A presentation clock never authorizes business success.

For a substantial sequence, write a compact beat map in the working design notes:

| Decision | Make it observable |
|---|---|
| Purpose | What can the viewer explain afterward? |
| Driver | Time, scroll progress, user action, or real application state? |
| Start | Composition, stable anchor, and objects whose identity persists |
| Action | One focal subject and the next intended attention destination |
| Phases | Entry, transition, landing, readable hold, and ending where useful |
| Adaptation | Narrow/short layout, interruption, reduced-motion equivalent |
| Acceptance | Named states, continuity constraints, readable content, usable controls |

Do not prescribe shot count, duration, or a universal narrative arc. Set hold lengths
by reading the actual copy at its rendered size. Eliminate time that adds neither
understanding nor a deliberate pause. Frequent interactions rarely need anticipation.

## Give movement a reason

**Staging:** isolate the focal change with stillness, contrast, or available space.
**Object permanence:** keep a recognisable label, silhouette, color, or position
through a change. **Cause and effect:** let a chosen input visibly explain its result.
**Anticipation:** a slight directional preparation can clarify a large deliberate
move; omit it when it postpones an ordinary click response. **Follow-through and
overlap:** let subordinate elements settle after the main mass, without delaying
controls. **Arcs:** use a curved path to express a pivot or physical relationship,
not to send every panel on a scenic route. **Acceleration/deceleration:** accelerate
departures and land clearly; preserve velocity when continuing the same gesture.
**Motion contrast and pauses:** the quiet interval makes the next action legible.

Check continuity of position, shape, scale, hierarchy, direction, and velocity.
A match transition carries a recognisable shape into a new context. A semantic
handoff keeps identity in the label even when shape changes. Use an intentional cut
when entities are unrelated or a morph distorts exact text or quantitative geometry.
An overview-to-detail move needs a recognisable route back to context. Depth should
explain layers, not shrink essential text beyond reading size.

## Three original mechanisms to adapt

- **Selection becomes a result:** select a labeled source; preserve its name and
  accent while a connecting line reaches the result area; settle the computed local
  result beside that identity. Other choices stay still. Changing input interrupts
  decorative travel and recomputes from the new selection. Label illustrative data;
  never imply a backend request. Static mode shows selected input and result together.
- **Type reorganizes around an anchor:** hold one word or graphic mark fixed while
  supporting words change from a wide sentence into a compact proposition. Move
  the largest group first; reveal the explanatory line after its landing. Reflow
  groups on narrow screens rather than squeezing the desktop mask. Preserve exact
  accessible text separately from decorative fragments. Replay restores the same
  start; a static version uses the settled proposition.
- **Layer reveals a component:** hold the base, lift one named part along its real
  assembly axis, transfer emphasis to its annotation, hold, then reassemble from
  canonical transforms. Keep the camera still during the critical separation;
  an optional overview adjustment happens before it. Do not invent real internals.
  Reduced motion uses labeled assembled/exploded still states with direct selection.

## Choose implementation and ownership

| Need | Adequate mechanism |
|---|---|
| Local hover or state | CSS transition; no timeline dependency |
| Finite controllable keyframes | Web Animations API (WAAPI) |
| Existing layout/gesture integration | Installed compatible motion library |
| Authored overlapping phases | One seekable coordinated timeline or explicit sampler |
| Precise paths, masks, diagrams | SVG with the same progress authority |
| Actual volumetric occlusion or camera freedom | Existing renderer; [3D production](technique-3d-production.md) |

Inspect manifest, lockfile, and installed API before choosing a library. Assign
each property one writer: CSS layout owns the outer frame, a timeline owns an inner
translation, and pointer rotation may own a separate nested layer. For 3D, use
named scene groups for intentional composition. React updates, camera controls,
imported tracks, and a timeline must not race on the same transform.

## Make authored states reproducible

Derive every authored property from explicit progress and baseline values, or use
an initialized timeline with explicit starting values. For WAAPI, pause the animation
and set `currentTime`; for GSAP, labels and `seek()`/`progress()` permit sampling.
Do not require earlier callbacks or chained `setTimeout` calls to establish state.
Keep analytics, requests, and mutations outside presentation replay.

An original pure phase sampler (normalized intervals are design choices):

```js
const phase = (p, start, end) => {
  const t = Math.max(0, Math.min(1, (p - start) / (end - start)));
  return t * t * (3 - 2 * t);
};
const lift = p => phase(p, .15, .4) * (1 - phase(p, .7, .95));
// Render from baseline + lift(progress) * offset; never accumulate offsets.
```

Inspect `sampleKinetic(progress)` in the original [motion example](../examples/motion.js)
for directly sampled DOM composition; the same file keeps illustrative product
selection separate from decorative playback. These examples are optional code
references, not dependencies or templates for ordinary work.

Time playback advances by elapsed timestamps, not a fixed increment per frame.
Store progress on pause and establish a fresh clock origin on resume. Simulation
and springs also carry velocity/state: use repeatable initialization and an
appropriate timestep strategy, not a claim that any simulation is seekable by
progress alone. Reverse is meaningful for a spatial reveal, not an undo operation
for a purchase. Use a cut or a new transition when reversal changes meaning.

Reuse [implementation lifecycle](implementation.md#lifecycle-and-state) and
[motion accessibility](technique-motion.md#accessibility-and-lifecycle). Re-measure
geometry after fonts/assets settle and on resize; resample current progress without
replaying side effects. Restore intended progress on history navigation. Track
explicit user pause separately from temporary visibility suspension.

**Diagnose:** simultaneous movement → freeze supporting layers; identical easing →
distinguish roles; endless float/bounce → choose a landing; arbitrary blur → remove
it and repair continuity; excessive stagger → group by meaning; disconnected reveals
→ rewrite the causal handoff. **Verify:** sample start, transitions, holds, and end
in random order and reverse; compare replay; interrupt rapidly; resize mid-beat;
change preference; remount. Watch playback as well as stills. **Fallback:** immediate
states or an annotated semantic sequence preserving the message and controls.

## Sources

API behavior reviewed 2026-09-09: [GSAP Timeline](https://gsap.com/docs/v3/GSAP/Timeline/),
[GSAP matchMedia](https://gsap.com/docs/v3/GSAP/gsap.matchMedia%28%29/),
[WAAPI currentTime](https://developer.mozilla.org/en-US/docs/Web/API/Animation/currentTime),
[requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame).
Beat maps, recipes, and phase intervals are original design heuristics, not measured optima.
