# Windows Native Window Effects

## Contents

- Choose Mica, Acrylic, or an opaque fallback
- Configure dependencies and the window
- Apply Mica at runtime
- Use Acrylic deliberately
- Migrate static effect ownership
- Preserve fallbacks and readable theming
- Diagnose Windows-specific failures
- Validate the result

## Choose Mica, Acrylic, or an opaque fallback

Choose the material from the supported Windows versions and intended surface:

| Material | Appropriate use | Support and tradeoff |
| --- | --- | --- |
| Mica | Persistent application, titlebar, or navigation backdrop | Windows 11; efficient and wallpaper-tinted rather than see-through |
| Acrylic | Transient or deliberately frosted, see-through surface | Windows 10 v1809+ and Windows 11; higher GPU and power cost |
| Opaque theme background | Unsupported OS, disabled transparency, or failed activation | Always required as the safe fallback |

Prefer Mica for a main application window on Windows 11. Microsoft recommends
Mica as a foundation layer and generally reserves Acrylic for transient
surfaces. Do not automatically fall back from failed Mica to Acrylic: that
changes both visual semantics and performance.

The `window-vibrancy` Acrylic implementation documents poor resize and drag
performance on affected Windows 10 and early Windows 11 builds. Use it only
when the user actually wants desktop content visible through frosted glass and
accepts that tradeoff.

## Configure dependencies and the window

Keep the native-effect crate target-specific:

```toml
[target.'cfg(target_os = "windows")'.dependencies]
window-vibrancy = "<compatible-version>"
```

Configure the Windows window as transparent. Prefer
`tauri.windows.conf.json` when macOS or Linux use different settings:

```json
{
  "app": {
    "windows": [
      {
        "label": "main",
        "transparent": true
      }
    ]
  }
}
```

Platform configuration is merged with the base Tauri configuration. Preserve
the complete existing window entry and verify the resulting configuration.
Consider Tauri's `noRedirectionBitmap` option only when a white creation flash
is observed and current platform documentation supports it.

## Apply Mica at runtime

Use this Windows 11 baseline with the shared activation command:

```rust
#[cfg(target_os = "windows")]
fn apply_native_effect<R: tauri::Runtime>(
    window: &tauri::WebviewWindow<R>,
) -> Result<Option<&'static str>, String> {
    use window_vibrancy::apply_mica;

    apply_mica(window, None).map_err(|error| error.to_string())?;

    Ok(Some("windows-mica"))
}
```

Passing `None` lets Mica follow the Windows theme. Return the marker only after
the API succeeds. On Windows 10, `apply_mica` reports an unsupported platform
version; keep the frontend opaque unless the product explicitly selected a
different Windows 10 material.

Clear an existing effect before switching owners or materials. Avoid
clear-and-reapply loops during ordinary rendering when the same Mica effect is
already active.

## Use Acrylic deliberately

When desktop Acrylic is an explicit requirement, replace the Mica call and
activation name:

```rust
use window_vibrancy::apply_acrylic;

apply_acrylic(window, None).map_err(|error| error.to_string())?;

Ok(Some("windows-acrylic"))
```

Use a tint only when the design requires it and recheck text contrast in both
themes. Verify resize, drag, power, Remote Desktop, high-contrast, and disabled
transparency behavior. Windows can replace native materials with solid colors
according to system policy; the application's semantic fallback must remain
readable.

Do not use legacy Blur as the default compatibility fallback. It has different
appearance and documented resize performance limitations. Add it only for an
explicitly supported legacy target.

## Migrate static effect ownership

Use the [shared static-owner migration](shared-transparency.md#migrate-an-existing-static-owner)
when adopting this runtime recipe. Remove the target window's static
`windowEffects` owner before runtime activation and preserve the opaque
frontend until the command succeeds. A static setting cannot supply the
activation marker or prove visible material; do not keep both application
paths active.

## Preserve fallbacks and readable theming

Keep the normal application background until Mica or Acrylic succeeds. The
native material follows Windows accessibility and personalization policies,
which can disable transparency or replace it with a solid fallback.

Use semantic application tokens on top of the material. Avoid hard-coded text
colors that assume one wallpaper or theme. Keep ordinary content panes opaque
and give them an explicit application background.

Distinguish Mica from desktop Acrylic in product language. Mica is an opaque,
wallpaper-informed material; Acrylic is the see-through frosted effect. Do not
promise that Mica will reveal windows behind the app.

## Diagnose Windows-specific failures

Check these conditions after the shared transparency diagnostics:

1. Confirm the current Windows build supports the selected effect.
2. Confirm the native API returned success before the frontend marker appeared.
3. Check whether Windows transparency effects, Battery Saver, high contrast, or
   remote-session policy replaced the material with a solid fallback.
4. Verify the Tauri window itself is transparent and the intended content pane
   has not covered the effect.
5. Measure resize and drag behavior before accepting Acrylic or legacy Blur.

Do not compensate for an unsupported native material by making the entire
window transparent. Restore the opaque fallback and select a supported product
behavior.

## Validate the result

- Test Mica on the minimum supported Windows 11 build.
- Test any Acrylic path on every supported Windows 10 and 11 build family.
- Exercise transparency enabled and disabled, Battery Saver, high contrast,
  light and dark themes, activation errors, and Remote Desktop when relevant.
- Confirm resizing, dragging, snapping, maximizing, and multiple monitors.
- Verify opaque content, scrolling, titlebar controls, and window shadows.

Consult these primary sources:

- [Tauri configuration reference](https://v2.tauri.app/reference/config/)
- [`window-vibrancy` repository and Windows APIs](https://github.com/tauri-apps/window-vibrancy)
- [Microsoft system backdrops](https://learn.microsoft.com/en-us/windows/apps/develop/ui/system-backdrops)
- [Microsoft Acrylic guidance](https://learn.microsoft.com/en-us/windows/apps/design/style/acrylic)
