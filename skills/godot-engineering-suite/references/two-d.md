# 2D systems

Use for Node2D scenes, sprites, tiles, 2D cameras, coordinates and 2D rendering behavior.

## Coordinate and transform discipline

Know whether a value is local, canvas or global. Use `to_local()`/`to_global()` and transform operations rather than manually adding positions across rotated/scaled parents. Avoid non-uniform scaling on physics bodies unless the engine behavior is explicitly intended.

## Sprites and pixel art

- Match import filtering, mipmaps and compression to the visual target.
- Keep pixels-per-unit and authored resolution consistent.
- Apply pixel snapping only when the camera and movement model support it; it can introduce jitter elsewhere.
- Use atlases when they improve authoring or batching, not as a blanket requirement.

## Tile worlds

For current Godot 4 projects, prefer `TileMapLayer` over the deprecated `TileMap`; verify the project's exact engine branch before migrating an existing map. Separate semantic layers when collision, navigation, occlusion or update frequency differ.

Do not rebuild large tile regions every frame. Batch edits and understand when navigation or physics data is regenerated.

## Z ordering and canvas layers

Use scene hierarchy and `z_index` deliberately for world elements. Use `CanvasLayer` for independent canvas transforms such as HUDs, not to paper over ordering mistakes. Document Y-sorting boundaries and verify nested sorting behavior.

## Cameras

Keep gameplay positions independent from camera shake and presentation offsets. Prefer a camera rig or explicit modifiers when multiple effects combine. Clamp only after considering zoom and viewport size.

## Collisions

Use dedicated collision shapes; visual bounds are not authoritative. Keep collision layers/masks named in project settings. Verify scaled and rotated shapes, one-way collisions and high-speed motion.

## Performance

Profile canvas draw calls, overdraw, particles, lights, large transparent textures and tile updates. Do not assume node count alone is the bottleneck. Use server APIs or MultiMesh only after measuring a relevant hot path.
