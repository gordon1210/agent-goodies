# Godot code review

Use for reviewing a change set. Review behavior and serialized assets, not only scripts.

## Scope and evidence

Identify the requested behavior, project engine version and files changed. Read the owning scenes/resources and validation results. Large generated diffs require explanation.

## Scripts

Check:

- lifecycle and ownership are correct;
- required versus optional node references are modeled accurately;
- exported names/types remain serialization-compatible;
- signals connect once and callback signatures match;
- async work handles teardown/staleness;
- physics and render timing use the correct callbacks/delta semantics;
- no unbounded timers, tweens, coroutines, nodes or logs;
- state has one authority;
- paths and input actions are valid/case-correct;
- errors are handled without hiding invariants.

## Scenes and resources

Check:

- root/owner/instance relationships;
- external and subresource IDs/UIDs;
- scripts, signals and animation paths;
- shared mutable resources;
- accidental editor/import churn;
- node renames and deleted exported properties;
- project settings/autoload/input changes;
- text-scene diff proportionality.

## Security and data

Check untrusted paths, RPC authority, size/rate bounds, save migrations, secrets, native/addon provenance, external process construction and debug endpoints.

## Performance

Reject unsupported claims. Ask for profiler evidence when the change adds pooling, caching, threading, lower-level servers, GI/render changes or broad update loops.

## Delivery

Check tests actually exercise the regression, target exports/configuration remain valid, platform-specific changes are gated and manual validation gaps are stated.

## Review output

Prioritize findings by correctness/security/data-loss risk. Give exact file/line and causal reasoning. Do not bury blocking issues beneath style notes. Distinguish confirmed defect, likely risk and optional improvement.
