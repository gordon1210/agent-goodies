# Worked example: Meridian Station

**Original fictional brief, not an implemented UI or a Frostpunk 2 reconstruction.**
The aim is to demonstrate dense management UI with authored identity and clear
causality. Values and timings are example proposals, not measured game standards.

## Brief and decision

A strategy game manages a remote orbital habitat. The screen must answer: "Why is
oxygen reserve falling, how long do we have under the current assumptions, and
which intervention can we afford?" Desktop pointer/keyboard leads; controller must
have a usable task path. Preserve the game's existing simulation and pause policy.

## Direction

Choose a civic-instrument identity rather than a generic sci-fi dashboard: cool
mineral surfaces, pale readable type, compact aligned ledgers, deliberate section
rules, and restrained line-drawn infrastructure symbols. A few copper-toned
mechanical details may identify critical equipment, but urgency uses a separate
labeled treatment. Avoid decorative hologram grids behind every value.

A circle denotes a tracked habitat object; a rectangular inspector denotes its
accounting detail; a visibly different warning marker denotes a condition requiring
attention. Define these as this project's symbols, then maintain them across map,
inspector, and notifications. Icons name player goals, not hidden implementation
variables.

## Information and composition

Keep an overview strip for oxygen, energy, food, population, and time. The selected
module remains visible on the map while a bounded right inspector explains it.
Opening a detailed causal ledger expands a focused region rather than stacking
several indistinguishable windows. The time/simulation status stays explicit.

Fixture oxygen instrument:

| Field | Example | Meaning |
|---|---|---|
| Stock | 420 units | Present reserve |
| Net rate | −12 / cycle | Current net flow |
| Estimate | 35 cycles at current rate | Linear estimate; assumes flow remains constant |
| Contributors | Supply +30, demand −42 | Why the rate is negative |
| Proposed remedy | New recycler: estimated +16 / cycle | Preview, not committed actual state |

Show the estimate only while its assumptions are meaningful. At zero/positive net
rate or under intermittent supply, use an appropriate explanation rather than a
misleading countdown. Revalidate intervention cost when committing the plan.

## Density and type

Start with a 520–620-unit inspector at a 1920×1080 logical reference and a designed
48-unit comfort inset. Use aligned number/unit columns and modest section spacing.
The example token profile supplies nominal font sizes, not actual glyph guarantees.
At large text, offer overview → inspector → ledger as explicit stages instead of
squeezing all three into their original geometry.

Use tabular numerals where the selected licensed face supports them. Expose exact
values for decisions while permitting well-labeled abbreviations in the overview.
Do not make all resource changes flash; reserve salience for a material threshold.

## Component and behavior model

`ResourceInstrument` exposes stock, rate, estimate assumptions, urgency, and an
inspect action. `ContributionRow` exposes source identity, signed contribution,
unit, and a navigation target. `InterventionPreview` separates current facts,
projected effects, cost, and commit/cancel.

Selected module, focused contribution, and warning status can coexist. Hover is
not selection. A controller inspect action opens the same explanation as a pointer
interaction. Confirming construction is a transaction; no success animation appears
before acceptance. A failed commit retains the player's plan where recovery is safe.

## Godot decomposition

Use native Control-based regions, reusable ledger rows, semantic Theme variations,
and separate noninteractive instrument ornament. Keep a coherent screen snapshot
so stock, rate, and urgency describe one simulation state. Use targeted dirty
updates rather than rebuilding the inspector every tick. Virtualize only when the
actual dataset and profiling justify it; preserve logical focus by stable ID.

Map navigation may use a structured module list as an alternative to spatial
pointer selection. If a dialog blocks interaction, gate both GUI scopes and any
independently polled game inputs; visual stacking is insufficient.

## Motion and sound

Propose about 90 ms for focus emphasis and 180 ms for an inspector entry, subject
to review. Keep exact numeric state readable immediately. Use restrained one-shot
navigation and warning cues; aggregate repeated low-priority reports. The reduced
motion variant preserves all state without panel travel or looping pulses.

## Acceptance tasks

Identify the deficit's largest contributor; inspect its module; compare two remedies;
preview and cancel construction; commit after resources change; return to the same
map context; repeat without a mouse. Test populated data, long labels, large text,
and the game's busiest background before accepting the result.

Evidence basis: [strategy direction](../references/strategy-management.md),
[interaction](../references/interaction-information.md), and
[data/performance](../references/godot-data-performance.md). The design itself is original.
