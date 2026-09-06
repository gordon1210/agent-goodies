# Networking and multiplayer

Use for MultiplayerAPI, RPCs, replication, dedicated servers, lobbies and networked gameplay.

## Authority first

Document who may change each piece of state. A client request is not authoritative evidence. The server or designated authority validates identity, ownership, timing, ranges, inventory, rate limits and game rules before mutation.

Keep transport/session management, game protocol and presentation separate. UI should not call low-level peers directly throughout the project.

## RPC contract

For every RPC define:

- caller and allowed authority;
- reliable/unreliable mode and channel;
- argument types, bounds and semantic validation;
- ordering and idempotency expectations;
- behavior for late, duplicate or missing messages;
- protocol version compatibility.

Never accept resource paths, file paths, class names or arbitrary serialized objects from remote peers without a strict allowlist and schema.

## Replication

Replicate authoritative state or events at a designed cadence. Interpolate presentation separately. Do not send complete node trees or per-frame reliable transforms.

Use stable network IDs distinct from transient instance IDs and scene-tree paths. Define spawn/despawn ownership and behavior for packets arriving before spawn or after despawn.

## Dedicated servers

A headless build must not require rendering, local input, audio devices or editor-only code. Guard platform integrations and secrets. Use server-side configuration and environment variables rather than client resources for credentials.

## Prediction and rollback

Prediction requires reconciliation and an explicit simulation tick. Side effects must not duplicate during replay. Load `determinism-replays-and-lockstep.md` for rollback or lockstep claims.

## Security and abuse

Bound message sizes/rates, authenticate before privileged actions, avoid detailed internal errors, time out dead peers and treat chat/user text as untrusted. TLS and platform identity do not replace game-rule validation.

## Verification

Test latency, jitter, loss, reordering, reconnect, late join, host migration if supported, malicious values and mismatched builds. Run multiple isolated peers; one local process is not adequate evidence.
