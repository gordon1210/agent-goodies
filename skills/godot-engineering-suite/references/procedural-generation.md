# Procedural generation

Use for seeded worlds, runtime content generation, loot, terrain and reproducible random systems.

## Reproducibility contract

Define what a seed reproduces and across which engine versions/platforms. Store the seed plus generator/schema version. Do not promise cross-version identical output when relying on unspecified engine ordering, physics or changing random implementations.

Use dedicated RNG instances per independent system when call-order changes must not perturb unrelated generation. Do not use one global random stream for world layout, loot, VFX and audio.

## Separate phases

1. Generate pure data from inputs and seed.
2. Validate constraints.
3. Instantiate scenes/resources from the data.
4. Bake or update navigation/physics as needed.
5. Stream or serialize the resulting state.

Keeping generation data separate from nodes makes tests, retries, networking and background work safer.

## Constraints and failure

Bound retry loops. Detect impossible parameter combinations and report the seed/configuration. Prefer constructive algorithms or fallback paths over unbounded rejection sampling.

## Performance

Chunk work and move pure computation off the main thread when safe. Scene-tree mutations, resource loading and rendering operations generally return to the main thread. Avoid creating thousands of nodes at once; instantiate progressively or use data-oriented rendering when measured.

## Persistence and networking

For single-player, save seed plus player/world deltas only when regeneration is stable and versioned. Otherwise save explicit generated state. In multiplayer, the authority generates and distributes either the seed with a strict algorithm version or authoritative results.

## Verification

Use fixed seed fixtures, property/invariant tests, boundary sizes and failure seeds. Record generation timing and output counts. A visual sample is useful but does not replace structural assertions.
