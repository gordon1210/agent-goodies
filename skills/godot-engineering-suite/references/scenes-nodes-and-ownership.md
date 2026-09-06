# Scenes, nodes, and ownership

Use this for scene design, node trees, lifecycle callbacks, child references and instancing.

## Scene boundary

Create a separate scene when a unit is independently reusable, testable, instanced multiple times, authored by a different workflow, or has a clear lifecycle. Do not split every node into a scene.

The root node should represent the scene's role, not a generic wrapper added without purpose. Keep node trees shallow enough to understand, but do not flatten meaningful ownership.

## Ownership and lifecycle

- The parent that creates or instances a child is normally responsible for configuring and removing it.
- Set owner correctly when creating persistent editor-time nodes; runtime children do not need scene ownership.
- Understand `_enter_tree()`, `_ready()`, `_exit_tree()`, processing callbacks and notifications before moving initialization code.
- Connect signals once and disconnect only when the connection outlives normal tree teardown or is otherwise dynamic.
- Cancel pending asynchronous work when the owning node exits or the operation becomes stale.

## Node references

Choose references by contract:

- required direct child: typed `@onready` path or scene-unique name when the uniqueness contract is intentional;
- exported dependency: typed exported node/resource reference for author-controlled wiring;
- dynamic peer: group, registry or explicit injection owned by a coordinator;
- optional dependency: `get_node_or_null()` or nullable exported reference with explicit fallback.

Do not repeatedly search the entire tree from frame callbacks. Do not make absolute `/root/...` paths the default.

## Scene inheritance and editable children

Use inherited scenes sparingly. They are useful for authored variants with stable bases, but can become fragile when the base tree changes. Prefer composition for behavior variants and resources for data variants.

Do not enable editable children merely to reach into an instanced scene and override arbitrary internals. Expose supported configuration on the child scene instead.

## Runtime instancing

- Load or preload the `PackedScene` at an appropriate lifetime.
- Configure required data before or immediately after `add_child()` according to the child's lifecycle contract.
- Add the instance under the owner responsible for cleanup.
- Use `queue_free()` for normal scene-tree removal; avoid using deferred calls as a universal fix.
- Reuse objects only when profiling proves allocation/lifecycle churn is material and reset semantics are reliable.

## Renames and moves

Before renaming a node or moving it in the tree, search scripts, animation tracks, signals, NodePaths, scene-unique references, editor metadata and tests. Treat animation track paths as code-level dependencies.
