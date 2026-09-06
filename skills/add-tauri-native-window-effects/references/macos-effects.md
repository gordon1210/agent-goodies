# macOS Native Window Effects

## Contents

- Choose classic vibrancy or Liquid Glass
- Configure dependencies and the window
- Apply classic vibrancy at runtime
- Migrate static effect ownership
- Handle Liquid Glass separately
- Preserve readable theming
- Configure overlay titlebars
- Validate and disclose distribution constraints

## Choose classic vibrancy or Liquid Glass

Treat these as separate macOS visual systems:

- Use semantic `NSVisualEffectView` vibrancy such as Sidebar for the stable,
  classic navigation and titlebar path.
- Use `NSGlassEffectView` Liquid Glass only when macOS 26 or newer is an
  explicit target and the installed native-effect crate exposes a compatible
  API.

Default to classic vibrancy when the request simply says glass, blur, or a
translucent sidebar. Do not silently convert a classic vibrancy design into
Liquid Glass.

The examples below follow the Tauri 2 and `window-vibrancy` 0.7 API shape.
Inspect the versions installed in the target repository before copying them.

## Configure dependencies and the window

Merge the required Tauri feature into the existing dependency. Preserve every
existing feature and keep the native-effect crate target-specific:

```toml
[dependencies]
tauri = { version = "<existing-version>", features = ["macos-private-api"] }

[target.'cfg(target_os = "macos")'.dependencies]
window-vibrancy = "<compatible-version>"
```

Configure the macOS window as transparent. Prefer
`tauri.macos.conf.json` when other platforms should keep different window
settings:

```json
{
  "app": {
    "macOSPrivateApi": true,
    "windows": [
      {
        "label": "main",
        "title": "",
        "titleBarStyle": "Overlay",
        "transparent": true
      }
    ]
  }
}
```

Platform configuration is merged with the base Tauri configuration. Preserve
the complete existing window entry and verify the resulting configuration
instead of replacing application-specific fields blindly.

Omit the empty title and overlay titlebar when HTML does not occupy the
titlebar. The transparent window and WebView canvas are still required for a
native material behind application content.

## Apply classic vibrancy at runtime

Use this target-gated helper with the shared activation command:

```rust
#[cfg(target_os = "macos")]
fn apply_native_effect<R: tauri::Runtime>(
    window: &tauri::WebviewWindow<R>,
) -> Result<Option<&'static str>, String> {
    use window_vibrancy::{
        apply_vibrancy,
        clear_vibrancy,
        NSVisualEffectMaterial,
    };

    clear_vibrancy(window).map_err(|error| error.to_string())?;
    apply_vibrancy(
        window,
        NSVisualEffectMaterial::Sidebar,
        None,
        None,
    )
    .map_err(|error| error.to_string())?;

    Ok(Some("macos-vibrancy"))
}
```

Clearing first makes repeated development-time activation deterministic. Use
the actual semantic material requested by the design. Avoid deprecated
appearance materials such as Dark and Light; control foreground contrast with
scoped application tokens.

Return the effect name only after `apply_vibrancy` succeeds. Let the shared
frontend marker reveal the transparent WebView after that result.

## Migrate static effect ownership

Use the [shared static-owner migration](shared-transparency.md#migrate-an-existing-static-owner)
when adopting this runtime recipe. Remove the target window's static
`windowEffects` owner before runtime activation and preserve the opaque
frontend until the command succeeds. A static setting cannot supply the
activation marker or prove visible material; do not keep both application
paths active.

## Handle Liquid Glass separately

Current `window-vibrancy` releases expose `apply_liquid_glass` and
`clear_liquid_glass` for macOS 26 or newer. Their signatures and required view
handling can change faster than classic vibrancy, so inspect the installed
crate and current upstream Tauri example before editing.

Use an explicit `macos-liquid-glass` activation result only after the call
succeeds. Decide with the user whether an unsupported OS should fall back to
classic vibrancy or remain opaque; do not make that product choice silently.

Liquid Glass can require different view placement or WebView content-view
handling from `NSVisualEffectView`. Preserve the shared transparent-canvas
diagnostics, but do not assume the classic view hierarchy is sufficient.

## Preserve readable theming

Keep a material sidebar on dark semantic tokens when its sampled desktop
material is dark, even if the main application uses a light theme. Scope the
existing dark token set to the material surface instead of hard-coding
foreground utilities.

Keep the material container transparent. A theme scope may change text, muted,
accent, badge, border, and control tokens, but must not add an opaque overlay.

If Tailwind `dark:` variants appear inside the scoped surface, extend the
project's custom dark variant so descendants of the material theme scope match
it. Keep the main content outside the scope.

## Configure overlay titlebars

Use `titleBarStyle: "Overlay"` only when HTML must occupy the titlebar. Then:

- reserve leading space for the traffic lights;
- mark only inert toolbar surfaces with `data-tauri-drag-region`;
- keep buttons and inputs interactive;
- prevent title text selection while dragging; and
- expect titlebar height and control positions to vary across macOS versions.

## Validate and disclose distribution constraints

- Verify classic vibrancy on every supported macOS version.
- Verify Liquid Glass and its chosen fallback separately.
- Inspect light and dark application themes against light and dark desktops.
- Confirm the opaque content pane and titlebar interactions remain correct.
- Test resizing, fullscreen, focus changes, and multiple-window labels.

Tauri documents that transparent macOS windows require its private API support
and warns that private APIs prevent Mac App Store acceptance. Surface that
tradeoff before selecting this approach for a store-distributed app.

Consult these primary sources:

- [Tauri configuration reference](https://v2.tauri.app/reference/config/)
- [`window-vibrancy` repository and examples](https://github.com/tauri-apps/window-vibrancy)
- [AppKit `NSVisualEffectView`](https://developer.apple.com/documentation/appkit/nsvisualeffectview)
- [AppKit `NSGlassEffectView`](https://developer.apple.com/documentation/appkit/nsglasseffectview)
