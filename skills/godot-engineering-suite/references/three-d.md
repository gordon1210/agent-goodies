# 3D systems

Use for Node3D scenes, transforms, meshes, environments, materials and 3D content composition.

## Units and transforms

Treat one world unit as one meter unless the project documents otherwise. Keep authored assets, physics, navigation, audio and camera values on the same scale.

Use local/global transforms correctly; do not compose Euler angles casually. Prefer basis/quaternion operations for orientation interpolation and maintain normalized transforms. Avoid non-uniform scaling on physics bodies, skeletons and frequently transformed hierarchies unless validated.

## Scene composition

- Keep imported source scenes separate from gameplay wrappers.
- Instance visual models beneath an authored gameplay root containing collision, scripts, sockets and interaction nodes.
- Expose stable attachment points rather than depending on arbitrary imported child names.
- Use resources for material/configuration variants and scenes for lifecycle-bearing variants.

## Materials and environments

Share materials intentionally. Duplicate before runtime mutation when the material is otherwise shared. Choose transparency modes carefully; transparent geometry affects sorting, depth behavior and performance.

Use one clear owner for world environment settings. Avoid placing competing `WorldEnvironment` nodes in reusable child scenes.

## Lighting and geometry

Select baked, dynamic or mixed lighting based on movement, target hardware and iteration workflow. Do not enable expensive GI or shadows without a measured visual requirement. Configure culling, LOD and visibility ranges with camera behavior in mind.

## Imported animation and skeletons

Preserve source naming/retargeting contracts. Keep gameplay scripts outside reimported scenes. Verify root motion, bone attachments and animation libraries after model reimports.

## Spatial queries

Use layers and masks to restrict queries. Reuse query parameters where it improves clarity, but do not cache stale world state. Decide whether a query belongs in physics time and whether exclusion lists remain valid after objects are freed.

## Verification

Inspect from representative camera distances and target renderers. Test collision, lighting, shadows, navigation, animation and LOD after scale or import changes. Visual editor inspection remains necessary for many 3D changes.
