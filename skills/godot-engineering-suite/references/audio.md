# Audio

Use for audio buses, playback nodes, spatial sound, music transitions and runtime audio settings.

## Bus architecture

Define a small stable bus tree, typically Master plus categories such as Music, SFX, UI and Voice. Route through buses rather than changing every player individually for global settings. Preserve bus names used by saves, scripts and snapshots.

## Playback ownership

The node that owns an audio event should normally own or request playback. Use a scoped pool/service for frequent one-shot sounds only when scene-local players are impractical. Ensure one-shots survive long enough after their visual source is freed, without leaking permanent nodes.

## Music and ambience

Model transitions explicitly: current track, target track, fade/crossfade, interruption and scene-change behavior. Avoid multiple scene roots competing for music ownership.

## Spatial audio

- Match attenuation distances to world scale.
- Configure listeners deliberately for split-screen/subviewports.
- Limit expensive effects and active voices on target hardware.
- Treat occlusion/reverb as authored systems, not default per-source raycasts.

## Settings

Store linear user-facing values but convert appropriately for bus decibels. Handle mute separately where needed and avoid invalid logarithms at zero. Apply settings after buses exist and when devices change.

## Assets

Use streaming for long tracks when appropriate and sample-based loading for short latency-sensitive effects, following current import options. Check loop metadata, channel layout and compression artifacts.

## Verification

Test scene changes, rapid repeated events, pause behavior, focus loss, output-device changes where supported, low-volume curves and exported builds. Use bus meters/profiler to detect clipping and excessive voices.
