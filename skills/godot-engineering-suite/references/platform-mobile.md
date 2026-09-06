# Mobile platforms

Use for Android/iOS exports, touch, lifecycle, permissions, safe areas and mobile performance.

## Design for lifecycle interruption

The app may pause, lose focus, lose its rendering surface, receive a low-memory warning or be terminated without a graceful quit. Persist critical progress at safe checkpoints and make resume/reconnect idempotent.

Do not rely on a final shutdown callback as the only save path.

## Input and layout

Use touch-safe target sizes, multi-touch IDs, safe areas and orientation-aware layouts. Test software keyboard appearance, back/cancel semantics, gesture areas and controller coexistence on real devices.

## Permissions and privacy

Request only required permissions and explain them in context. Platform manifests, privacy declarations and SDK data collection are release artifacts requiring review. Do not add an SDK that expands permissions or tracking without explicit approval.

## Performance and memory

Profile representative low/mid target devices. Control texture formats/sizes, shader complexity, transparency, particles, lights, audio voices, scene loading and thermal load. Desktop measurements are not substitutes.

Handle memory pressure by reducing content peaks and import sizes before adding complex manual unload logic.

## Packaging

Follow the project's pinned Android/iOS tooling. Keep application IDs, signing teams, minimum versions, architectures and store channels explicit. Inject signing credentials through secure build infrastructure.

## Platform services

Wrap purchases, achievements, notifications, authentication and cloud saves. Handle cancellation, offline behavior, duplicate callbacks and store restore flows. Never grant an entitlement solely from a client-side success flag.

## Verification

Use physical Android and iOS devices affected by the change. Test fresh install, upgrade, background/foreground, interruption, rotation, safe areas, permissions denied, offline mode, low storage, thermal throttling and release-signed builds.
