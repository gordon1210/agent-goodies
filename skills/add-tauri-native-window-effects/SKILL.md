---
name: add-tauri-native-window-effects
description: Add and debug native window materials in Tauri 2 desktop apps on macOS and Windows. Use when implementing macOS vibrancy or Liquid Glass, Windows Mica or Acrylic, a translucent sidebar or titlebar, transparent WebView content, platform-specific opaque fallbacks, or diagnosing a native effect hidden behind gray, white, black, Canvas, or other opaque frontend backgrounds.
---

# Add Tauri Native Window Effects

Implement a native operating-system material behind a transparent Tauri
WebView. Treat the result as one rendering stack: the native effect,
transparent window, transparent WebView ancestors, and intentionally opaque
content panes must all agree.

## Read the relevant references

Read [the shared rendering stack](references/shared-transparency.md) before
editing any target. Then read only the platform reference that applies:

- [macOS effects](references/macos-effects.md) for AppKit vibrancy or Liquid
  Glass.
- [Windows effects](references/windows-effects.md) for Mica or Acrylic.

Use their snippets as baselines, then adapt crate and framework APIs to the
versions already installed in the target repository.

## Establish the constraints

1. Inspect the Tauri, WebView, frontend, Tailwind, and native-effect versions,
   plus the minimum supported operating-system versions.
2. Identify which surfaces should reveal native material and which must remain
   opaque. Prefer a transparent shell with explicit opaque content panes.
3. Choose the platform material deliberately. Do not present macOS vibrancy,
   Liquid Glass, Windows Mica, and Acrylic as interchangeable visual systems.
4. Preserve unsupported platforms with an opaque, readable fallback.
5. Check repository rules before launching a GUI. Ask before opening or
   activating the app unless the user already authorized it.

## Choose one native effect owner

Use either Tauri's static `windowEffects` configuration or a runtime
`window-vibrancy` integration for a window. Never stack both.

Use static configuration when the effect is always on and the minimum OS
version guarantees support. Prefer runtime integration when support must be
observed, the effect can change, or an unsupported host must fall back safely.

## Gate transparency on real activation

Keep the normal application background until the native effect reports
success. Let the native layer return the activated effect name or no effect;
set a `data-native-window-effect` marker only for a real effect.

Use `isTauri()` only to distinguish a Tauri WebView from a normal browser. It
does not identify macOS or Windows and must not authorize transparency by
itself. On errors or unsupported platforms, leave the marker absent and keep
the interface opaque.

## Route each platform

- On macOS, prefer semantic AppKit vibrancy such as Sidebar for the classic
  path. Treat macOS 26 Liquid Glass as a separate, version-gated path.
- On Windows 11, prefer Mica for a persistent application or navigation
  backdrop. Use Acrylic only when genuine see-through frosted glass is wanted
  and its power and resizing costs are acceptable. Do not silently fall back
  from Mica to Acrylic.
- On Linux, keep an opaque fallback. Native desktop blur is compositor-owned
  and is outside the portable Tauri baseline. Investigate a compositor-specific
  implementation only when the user explicitly requests that target.

## Implement the complete stack

1. Configure target-specific dependencies and window settings.
2. Apply the selected effect to the real Tauri WebView window.
3. Return an activation result that distinguishes success from unsupported or
   failed activation.
4. Make `html`, `body`, the root node, and every shell ancestor above the
   material region transparent only after success.
5. Keep ordinary content panes explicitly opaque.
6. Keep permanent transparency overrides outside Tailwind cascade layers.

Do not substitute CSS `backdrop-filter` for a native window material. It only
filters content inside the WebView and cannot reveal the desktop behind the
native window.

## Validate the result

- Run frontend tests, type checking, linting, and a production build.
- Run Rust formatting, tests, and clippy for the Tauri crate.
- Compile every supported platform path in CI when available.
- Inspect light, dark, high-contrast, and disabled-transparency fallbacks.
- Confirm opaque content, scrolling, titlebar drag regions, and controls still
  work.
- Remove diagnostic styles, commands, timers, and logging before finishing.

After two failed hypotheses, return to the native activation result and
computed backgrounds instead of adding more blur, opacity, or fallback layers.
