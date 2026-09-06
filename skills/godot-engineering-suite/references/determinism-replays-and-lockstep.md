# Determinism, replays, and lockstep

Use for replay systems, rollback, deterministic simulation, seeded runs and lockstep multiplayer.

## Start with the requirement

Distinguish:

- input replay for debugging;
- cinematic/ghost playback that may drift;
- authoritative event log reconstruction;
- rollback networking;
- deterministic lockstep across machines.

These require very different guarantees.

## Godot constraints

Do not assume scene-tree order, floating-point math, physics, navigation avoidance, particles, animation timing or iteration over unordered data is deterministic across platforms or engine versions. Rendering determinism is a separate problem from gameplay determinism.

## Safer replay model

For ordinary games, record versioned inputs/events plus periodic authoritative snapshots and checksums. During playback, detect divergence and recover or report it. Store engine version, game build, content version, tick rate and seed.

## Deterministic simulation layer

If lockstep is mandatory:

- isolate simulation from Nodes and nondeterministic engine services;
- use a fixed tick and deterministic ordering;
- use integer/fixed-point math where required;
- define RNG streams and call order;
- serialize canonical state deterministically;
- hash state each tick or interval;
- treat physics/rendering as presentation or implement a deterministic substitute;
- run cross-platform golden tests.

## Rollback

Keep a bounded ring of compact snapshots or reversible state. Side effects such as audio, particles, achievements and network sends must be idempotent or delayed until confirmed. Re-simulation must not duplicate them.

## Compatibility

A replay format is a public data format. Version it and either migrate old recordings or reject them with a clear reason. Do not silently play an incompatible replay.
