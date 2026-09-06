# Motion design: communicate state with an intentional character

## Assign a job to each motion

Choose one primary purpose: acknowledge input, direct attention, explain spatial
continuity, communicate progress, express importance, or establish identity.
Remove effects without a defensible job. A fast hover, a deliberate panel reveal,
and a major reward do not deserve identical duration or amplitude.

Do not default to spring, squash, camera shake, or hit-stop. Restrained motion can
be highly authored. A mechanical instrument may intentionally use linear travel;
a painterly edge can reveal softly; an expressive editorial screen can use a cut.
Curve choice should support the metaphor and task, not a universal ban on linearity.

## Proposed starting ranges—not reference-game measurements

| Motion | Experiment with | Constraint |
|---|---|---|
| Focus / hover emphasis | 80–140 ms | Actionable immediately; repeated navigation never queues |
| Small contextual panel | 160–240 ms | Keep source relationship readable |
| Full screen decorative entrance | 250–450 ms | Do not make the whole interval a forced input wait |
| Exit | Often shorter than entrance | Preserve destination clarity and cancel behavior |
| Status instrument | Match information semantics | Real values must not be hidden by decorative interpolation |

Tune with the actual display, input cadence, and gameplay intensity. These are
original hypotheses. Record chosen values as tokens only after review.

## Choreography

Name the lead element, supporting elements, and settlement. A panel can establish
its readable backing first, then the text, then optional ornament. Avoid long
cumulative per-item staggers across large lists. Reveal group structure rather
than forcing the player to watch twenty rows arrive serially.

Keep hit regions stable during pointer interactions. Establish semantic selection
at input time; visual emphasis may settle afterward. Preserve spatial continuity
when entering a detail view, but use an immediate state change when animation
would imply the wrong causal relationship.

## Interruptions are part of the design

Define opening, open, closing, and hidden behavior for repeated actions. On a new
transition, replace conflicting motion and start from the current visible state.
Do not accumulate scale on every hover or wait forever for a cancelled animation.
Test rapid open-close-open, device changes, resize, scene exit, and paused gameplay.

Audio and motion should agree on when the action happened. An ornamental completion
sound must not claim success before a transaction has succeeded.

## Reduced motion

Create an alternate behavior, not merely a zero-duration value applied to an
untested tween chain. Replace travel, zoom, parallax, shake, and repeated pulses
with instantaneous state, a short safe opacity change where appropriate, or a
static marker. Keep all information and focus cues. Avoid claiming flash safety
from an informal frequency rule; evaluate the composite output separately.

Acceptance: motion clarifies meaning, survives interruption, returns to the correct
resting state, and does not impose unnecessary navigation latency. Watch a recording
at normal speed before analyzing isolated frames.

## Evidence anchors

[D06](sources.md#d06) · [G07](sources.md#g07) · [X117](sources.md#x117) · [X118](sources.md#x118)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
