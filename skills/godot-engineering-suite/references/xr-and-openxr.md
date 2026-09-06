# XR and OpenXR

Use for VR/AR rigs, OpenXR, tracking, interaction, comfort and XR performance.

## Version and runtime

Verify the Godot branch, renderer, OpenXR plugin/runtime and target headset. Extension availability differs by runtime and platform; query capabilities and provide fallbacks.

## Rig ownership

Keep the XR origin, tracked head/cameras and controllers in a clear rig scene. Move the origin for locomotion; do not overwrite tracked head/controller transforms. Separate tracking pose, gameplay body and visual avatar.

## Interaction

Use action maps and semantic poses rather than device-specific button indices. Define grab ownership, two-hand interactions, haptics and tracking-loss behavior. Never assume both controllers or hand tracking are present.

## Comfort and safety

Provide comfort options appropriate to the game: snap/smooth turn, vignette, locomotion speed, seated/standing mode, height calibration, handedness and recentering. Avoid moving the virtual camera independently from tracked motion without a deliberate comfort design.

## Rendering and performance

XR has strict frame-time and latency budgets. Profile per-eye resolution, MSAA, shadows, transparency, post-processing, particles and CPU submission on the headset. Avoid desktop-only GI assumptions. Use foveation or platform features only after capability checks and visual validation.

## UI

Prefer world-space or XR-aware surfaces at readable distance and scale. Support ray/direct interaction, focus feedback and controller-independent navigation. Avoid tiny text and edge-clipped HUDs.

## Verification

Test on real target hardware for tracking loss, recenter, boundary changes, pause/system overlays, controller hot-plug, performance, motion comfort and release export. A desktop simulator is useful but insufficient.
