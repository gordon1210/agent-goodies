# Navigation and AI

Use for navigation maps, meshes/polygons, agents, avoidance, pathfinding and behavior logic.

## Pick the pathfinding model

- Navigation mesh/polygon: free movement through continuous space.
- AStar/AStarGrid: authored graphs, grids or deterministic tactical costs.
- Direct steering: simple unobstructed movement.
- Custom planner: domain-specific constraints not represented by geometric shortest paths.

Do not use NavigationAgent as the behavior tree. Path planning, steering, perception and decision-making are separate concerns.

## Navigation lifecycle

Navigation maps synchronize asynchronously with scene changes. Do not request a path immediately after adding or baking navigation and assume the map is ready. Use the relevant map-change/synchronization contract for the project version.

Update target positions only when goals materially change; constant reassignment can trigger unnecessary path work. Call agent path APIs at the cadence expected by the engine and move the owning body through its correct physics API.

## Avoidance

Avoidance produces a suggested safe velocity; it does not move the body or guarantee collision-free motion. Limit participation to agents that need it, configure layers/priorities deliberately and profile crowds.

## Dynamic worlds

Choose between rebaking, navigation obstacles, local steering and graph updates based on change frequency. Do not rebake large regions for transient actors.

## AI architecture

Separate:

1. perception snapshot;
2. authoritative game state;
3. decision/planning;
4. navigation request;
5. movement/animation presentation.

Make state transitions observable in debug builds. Time-slice expensive planning and invalidate stale paths/goals when the world changes.

## Verification

Test unreachable targets, partial paths, moving goals, narrow passages, spawn before navigation sync, scene reload and many agents. Visualize navigation and agent paths; measure path/avoidance costs before changing algorithms.
