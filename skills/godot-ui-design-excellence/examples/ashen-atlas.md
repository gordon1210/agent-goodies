# Worked example: Ashen Atlas

**Original fictional brief, not an implementation or an Expedition 33 reconstruction.**
All dimensions and timings below are initial proposals. No screenshot or shipped
asset is implied. Use this to learn the design-to-Godot reasoning, not as a mandatory skin.

## Brief and player question

A turn-based RPG follows surveyors mapping a landscape that is slowly erasing itself.
The first screen is a battle skill chooser: "Which action can I afford, who will it
hit, and what trade-off does it create?" Desktop keyboard/mouse and controller are
in scope; 1080p–4K, an ultrawide adaptation, and large text must remain functional.
The existing combat simulation is not being redesigned.

## Visual grammar

The interface resembles an expedition record without literally turning every panel
into a notebook. Use warm pale type, a deep ink reading surface, thin cartographic
line work, and an occasional irregular painted edge. The character illustration
carries emotion; the action list carries the decision. Avoid gear-shaped ornaments,
random filigree, and unrelated generic fantasy emblems.

Shape roles: a short vertical mark identifies selection, an open bracket indicates
focus, an inset seal identifies the currently equipped discipline, and a clear lock
with text explains unavailability. Never use the same bright frame for all four.

Material roles: quiet opaque ink behind words; rough edge outside the reading area;
a restrained warm accent only for focus or a meaningful action emphasis. No busy
paper grain through the body text. Use the `ashen-atlas` token profile as a starting
experiment, measuring actual text and contrast before acceptance.

## Composition proposal

At a 1920×1080 logical reference, begin with a 56-unit designed comfort inset.
Place a bounded 480–560-unit decision column in the right third, a compact turn
context region on the left, and resources close to the acting character's action
context. Keep the central target silhouette clear. These widths depend on actual
ability descriptions and large-text testing; do not hard-code them as universal.

The action column has three tiers: action name and cost; concise mechanical effect;
optional expanded inspection. Target preview remains visible while choosing an
ability. At narrower usable widths or large text, move detail into an explicit
inspection step rather than shrinking the entire menu. On ultrawide, expand world
context but keep action reading width bounded.

## Example content and state

Fixture ability: **Surveyor's Refrain**, cost 3 focus, targets one opponent, applies
an exposed-state effect. Exact damage and status behavior must come from the game.
The fixture only tests layout; it is not a newly invented gameplay requirement.

| Situation | Appearance | Behavior |
|---|---|---|
| Focused, affordable | Focus bracket and strong label | Confirm enters targeting |
| Selected during target preview | Persistent slim selection mark | Back returns to the same ability |
| Insufficient focus | Unavailable treatment plus required/current cost | Inspect remains available; activation does not commit |
| Target invalidated | Explicit reason near target preview | Return to valid choice; do not act on stale identity |

## Asset decomposition and Godot mapping

Keep functional text in native controls. Author one outer brush silhouette, two
edge endcaps, a small set of cartographic symbols, and a portrait independently.
Do not bake the entire screen into an image.

```text
BattleHUD (CanvasLayer)
  UIRoot (Control with project Theme)
    ContextRegion (Control)
    DecisionSlot (Control; responsive allocation)
      OrnamentLayer (Control; noninteractive)
      MotionRoot (Control)
        ReadingPanel (PanelContainer)
          Content (VBoxContainer)
            ActionRows (VBoxContainer; reusable ActionRow scenes)
            TargetSummary (native text/control structure)
    InputHints (rebind-aware native controls)
```

The scene tree is a proposed structure, not a copy-paste `.tscn`. The controller
owns interaction context; the transition does not own whether an action is legal.
Shared styles remain immutable during a single row's focus changes.

## Motion proposal

Apply focus semantically immediately; settle its bracket over about 100 ms.
Establish the reading panel promptly; allow a decorative edge reveal of about
340 ms only on meaningful first entry. Repeated choice navigation must not replay
that whole entrance. On back, restore context without a mandatory cinematic wait.
Reduced motion uses final state and a static bracket. No hover camera shake.

## Acceptance experiment

Capture bright and dark battle backgrounds; focus an unavailable long-name ability;
enter and cancel targeting repeatedly; remove a target during preview; switch
controller/pointer; resize; enable large text and reduced motion. Compare the
whole frame against the approved composition before inspecting decorative crops.
Do not accept unless target clarity and action readability survive together.

Evidence basis: [reference analysis](../references/reference-analysis.md),
[cinematic RPG](../references/cinematic-rpg.md), and
[Godot layout](../references/godot-layout.md). The concrete design is original.
