# Web platform

Use for HTML5/Web exports, browser APIs, hosting, storage, threading and download performance.

## Browser constraints

Verify the project's Godot version, renderer and browser support matrix. Native libraries and arbitrary filesystem/process access are unavailable. Some language/runtime features and extensions are platform/version-sensitive; verify official docs before promising support.

## Hosting

Serve with correct MIME types and caching. Threads/shared memory require the browser isolation headers and hosting configuration expected by the current Godot release. Do not enable those headers without considering embedded/third-party resources.

Use HTTPS for APIs requiring a secure context. Configure CORS on the server; client-side workarounds do not bypass browser policy.

## Startup and size

The initial download, decompression, shader compilation and first import/load define user experience. Measure compressed transfer size and cold-cache startup. Split optional content or stream assets only when the hosting/design supports it.

## Storage

Browser storage is quota-limited and may be cleared. Flush/synchronize persistent virtual filesystem data according to the project version and test private browsing/quota failure. Critical cloud progress needs server-side persistence and conflict handling.

## Audio and input

Browsers commonly require user interaction before audio playback or pointer capture. Handle focus, tab visibility, pointer lock, touch gestures and keyboard shortcuts that the browser reserves.

## Security

Treat JavaScript bridges, URL parameters, postMessage, clipboard and downloaded data as untrusted. Keep secrets server-side. Apply a suitable Content Security Policy and dependency review for surrounding web code.

## Verification

Test release exports on supported Chromium, Firefox and Safari variants, with cold cache, slow network, resize/fullscreen, focus loss, mobile browser behavior, storage persistence and the production hosting headers.
