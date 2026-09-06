# Asset import and content pipeline

Use for textures, audio, fonts, models, animations, import settings and source-content workflows.

## Separate source and runtime concerns

Preserve editable source assets outside destructive generated workflows. Godot project assets should have a known source of truth, ownership and reimport path. Do not hand-edit imported cache data under `.godot/`.

For imported 3D scenes, prefer a wrapper scene for gameplay nodes, scripts, collision and stable sockets. Reimporting the source model should not erase authored gameplay behavior.

## Import settings are part of behavior

Review settings relevant to the asset type:

- texture filtering, mipmaps, compression, color space and normal-map detection;
- audio sample/stream mode, looping and compression;
- font fallback, glyph ranges and variation data;
- 3D scale, materials, animation slicing, tangents, mesh compression and generated collision;
- platform-specific overrides.

Do not apply one preset to every asset category. Pixel art, UI, world textures and data textures require different choices.

## Naming and paths

Use stable lowercase or project-standard paths and preserve case. Avoid source-tool names that encode temporary hierarchy assumptions. Keep resource paths below the project root and do not serialize machine-specific source paths.

## Reimport safety

Before a broad reimport:

1. use the exact Godot version expected by the repository;
2. ensure source assets and import settings are committed;
3. close or coordinate with an open editor;
4. record a clean baseline;
5. reimport only the affected assets where possible;
6. inspect scene, animation, material, UID and file-size changes;
7. run representative scenes and target exports.

## Generated content

Generated atlases, baked meshes, lightmaps, navigation data and converted audio should have deterministic generation commands or clear editor instructions. State whether generated files are committed and why.

## Licensing

Track asset licenses, attribution, redistribution and model/font restrictions. Do not download or introduce an asset merely because it is technically accessible. Keep provenance with the asset manifest or project documentation.
