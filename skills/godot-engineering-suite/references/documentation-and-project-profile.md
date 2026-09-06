# Documentation and project profile

Use when documenting durable Godot constraints or reducing repeated discovery cost.

## Keep two layers

- `GODOT_PROJECT.md`: concise current facts and commands needed by humans and agents.
- Deeper docs/ADRs: rationale for decisions with lasting tradeoffs.

Do not turn the project profile into a tutorial or file-by-file catalog. Facts already obvious from one nearby file do not need duplication unless they are easy to misuse.

## High-value profile fields

- exact Godot branch/edition and how it is pinned;
- renderer and target platforms;
- main scene and major ownership boundaries;
- scripting/native languages;
- autoload responsibilities;
- authoritative state and networking model;
- save/protocol/content schema versions;
- addons/native SDKs and license constraints;
- import/source-asset policy;
- commands for import, tests, builds and exports;
- files/directories that must not be edited;
- required manual/device/editor checks.

Use `assets/GODOT_PROJECT.template.md` as a starting point.

## Commands

Document repository wrappers, not a generic command that bypasses required environment variables or tool versions. Include expected working directory and whether the command executes project/editor code.

## API constraints

For non-obvious engine behavior, link versioned official documentation and state the affected engine range. Avoid copying extensive class reference text.

## Architecture decisions

Write an ADR when alternatives, migration cost or cross-feature constraints matter. Record context, decision, consequences and revisit trigger. Do not create an ADR for trivial implementation detail.

## Maintenance

Update docs in the same change that alters a durable contract. Remove stale instructions rather than appending contradictory history. Validate paths and commands in CI where practical.
