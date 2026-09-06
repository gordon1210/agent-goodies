# Change workflow

Use this for implementation, refactoring and fixes that affect Godot-owned files.

## 1. Define the behavioral slice

State the smallest observable behavior that must change. Trace it through scene ownership, scripts, resources, signals, input actions and project settings. Avoid broad cleanups unless they are required for correctness.

## 2. Establish invariants

Before editing, identify contracts that must remain true:

- scene root type and external owner;
- node names and paths referenced by scripts, animations or tracks;
- exported property names and serialized types;
- resource paths and UIDs;
- signal names and argument types;
- autoload names;
- input action names;
- RPC annotations and authority rules;
- save-data keys and versions;
- addon or engine-version constraints.

## 3. Choose the least fragile edit path

- Prefer script-only changes when scene serialization is unnecessary.
- Prefer the editor or a trusted deterministic tool for large scene/resource restructures.
- Hand-edit text `.tscn` and `.tres` only for small, understood changes.
- Never convert binary `.scn` or `.res` files opportunistically.
- Do not regenerate unrelated imports or resave the entire project.

## 4. Implement narrowly

Follow nearby style and ownership. Keep reusable data in resources, behavior in the owning node or service, and presentation logic near presentation. Do not introduce a global singleton to avoid passing one dependency.

For required scene children, fail visibly during development rather than silently continuing with null references. For optional children, model optionality explicitly.

## 5. Inspect serialized diffs

For scene/resource/project-setting changes, check for:

- unrelated property churn;
- reordered external or subresource IDs;
- lost UIDs;
- changed owners;
- detached scripts;
- broken animation track paths;
- unexpected imported-resource changes;
- accidental input/export/project-setting modifications.

A large diff for a small behavior change is a failure signal. Revert and choose a narrower method.

## 6. Verify incrementally

Use the verification ladder from `SKILL.md`. Match the project binary. Run targeted scenes or tests before full exports. Never claim editor, device or multiplayer validation that was not performed.

## 7. Report residual risk

Call out editor-only workflows, visual tuning, platform SDK checks, real-device input, network topology, save migration and performance measurements that still require human or target-environment verification.
