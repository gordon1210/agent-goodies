# Shared Native-Effect Rendering Stack

## Contents

- Rendering contract
- Runtime activation result
- Frontend activation
- WebView transparency and cascade layers
- Layout and theme boundaries
- Diagnostic procedure
- Cross-platform fallback
- Validation

## Rendering contract

Use the same stack on macOS and Windows:

```text
desktop or underlying windows
  -> native operating-system material
  -> transparent Tauri window and WebView canvas
  -> transparent application shell and material region
  -> opaque application content panes
```

Every layer is required. A native effect can be active but invisible because a
WebView ancestor paints over it. A transparent frontend can also become
unreadable when the native effect is unsupported or fails.

Prefer a runtime integration when the application supports multiple operating
systems or OS versions. It provides an observable result that can gate
frontend transparency. Use static `windowEffects` only when the effect is
always on and support is guaranteed by the application's minimum OS version.

## Runtime activation result

Return the activated effect name from the native command. Return `None` on a
platform where the portable skill intentionally provides no effect. Return an
error when a supported target attempted activation and failed.

Use one target-gated `apply_native_effect` implementation from the applicable
platform reference and this shared command:

```rust
use tauri::Manager;

#[tauri::command]
pub fn enable_native_window_effect(
    app_handle: tauri::AppHandle,
) -> Result<Option<String>, String> {
    let window = app_handle
        .get_webview_window("main")
        .ok_or_else(|| "main window not found".to_string())?;

    apply_native_effect(&window).map(|effect| effect.map(str::to_owned))
}

#[cfg(not(any(target_os = "macos", target_os = "windows")))]
fn apply_native_effect<R: tauri::Runtime>(
    _window: &tauri::WebviewWindow<R>,
) -> Result<Option<&'static str>, String> {
    Ok(None)
}
```

Register the command exactly once:

```rust
tauri::Builder::default().invoke_handler(tauri::generate_handler![
    enable_native_window_effect,
    // Existing commands...
]);
```

Use the actual window label when the project does not use `main`. Keep native
dependencies target-specific so the unsupported path remains buildable.

## Frontend activation

Use `isTauri()` only to avoid invoking a native command from a normal browser.
The returned effect name, not `isTauri()`, decides whether the document becomes
transparent:

```ts
import { invoke, isTauri } from "@tauri-apps/api/core"

type NativeWindowEffect =
  | "macos-vibrancy"
  | "macos-liquid-glass"
  | "windows-mica"
  | "windows-acrylic"

export async function enableNativeWindowEffect() {
  delete document.documentElement.dataset.nativeWindowEffect

  if (!isTauri()) return

  try {
    const effect = await invoke<NativeWindowEffect | null>(
      "enable_native_window_effect",
    )

    if (effect) {
      document.documentElement.dataset.nativeWindowEffect = effect
    }
  } catch (error) {
    console.warn("Could not enable the native window effect", error)
  }
}
```

Apply the effect before rendering the application shell when practical. If the
command returns `null` or throws, render normally with the existing opaque
application background.

Do not treat a no-op native command as success. A no-op must return `None`, or
the frontend will reveal a transparent window with no material behind it.

## WebView transparency and cascade layers

Keep ordinary base styling in the project's existing Tailwind layer:

```css
@layer base {
  body {
    @apply min-h-svh bg-background text-foreground antialiased;
  }
}
```

Place the native-effect override after layered imports and rules, outside every
`@layer`:

```css
/* Keep this unlayered so the WebView canvas cannot cover native material. */
html[data-native-window-effect],
html[data-native-window-effect] body,
html[data-native-window-effect] #root {
  background-color: transparent;
}
```

Also clear any application-shell background above the intended material region
when inspection shows that it paints. Do not make unrelated content
transparent.

An unlayered author rule outranks normal declarations inside explicit cascade
layers, even when the unlayered rule appears earlier or has lower specificity.
This matters when an imported stylesheet supplies an unlayered `body {
background: Canvas; }` rule while the project's transparency override lives in
`@layer base`. The system `Canvas` color then paints over a working native
effect.

Use inline `!important` only to prove that an element is blocking the native
material. Remove it immediately and place the permanent selector outside the
cascade layers.

## Layout and theme boundaries

Keep only the intended material regions transparent:

```tsx
<main className="flex h-svh flex-col bg-transparent">
  <Titlebar />
  <div className="flex min-h-0 flex-1 overflow-hidden">
    <aside className="bg-transparent">...</aside>
    <section className="min-w-0 flex-1 bg-background">...</section>
  </div>
</main>
```

Reuse semantic theme tokens for text, muted controls, borders, and accents on
the material surface. Scope dark tokens to a dark sampled material when needed,
but do not give the theme scope an opaque background.

Keep the main content outside that scope so it can follow the application's
Light, Dark, or System selection independently. Verify high-contrast and
disabled-transparency fallbacks rather than assuming the native material is
always visible.

## Diagnostic procedure

Diagnose from the frontend toward the native window:

1. Confirm the native command returned the expected effect name.
2. Confirm `data-native-window-effect` exists only after that result.
3. Inspect computed backgrounds for `html`, `body`, the root, the application
   shell, and the intended material element.
4. Treat the first nontransparent ancestor as the current blocker.
5. Inspect matched CSS rules and cascade layers when a background resolves to
   `Canvas`, white, gray, or black.
6. Verify that an opaque content pane has not expanded across the material
   region.

Use this browser-console probe with selectors adapted to the application:

```js
for (const selector of ["html", "body", "#root", "main", ".glass-sidebar"]) {
  const element = document.querySelector(selector)
  if (!element) continue

  console.log(selector, getComputedStyle(element).backgroundColor)
}
```

Temporarily force only the suspected element transparent. If the material
appears immediately, stop changing native code and fix the winning CSS rule.
If it does not appear, return to the native command result, target window
label, and window configuration.

## Cross-platform fallback

Keep the marker absent and retain the normal opaque background when:

- the host is a normal browser;
- the target OS is unsupported;
- the selected material is unavailable on the current OS version;
- native activation failed.

Some native APIs still report successful activation when an accessibility,
power, or personalization policy replaces the material with a system-provided
solid fallback. In that case the marker can remain, but the application's
semantic foreground and content-pane colors must stay readable against the
native solid fallback.

The portable Linux behavior is an opaque fallback. The upstream native-effect
crate does not implement Linux because blur and vibrancy are compositor-owned.
Do not add a generic CSS blur and call it native desktop glass. Treat KDE,
GNOME, Wayland, X11, and compositor-specific protocols as separate work that
requires an explicit Linux target.

## Validation

- Run frontend tests, type checking, linting, and a production build.
- Run Rust formatting, tests, and clippy for the Tauri crate.
- Compile target-gated code for macOS and Windows in CI when runners exist.
- Exercise the opaque fallback in a browser and on every unsupported target.
- Verify supported, unsupported, disabled-transparency, and activation-error
  states.
- Inspect light, dark, and high-contrast presentation.
- Confirm titlebar drag regions, interactive controls, resizing, and scrolling.
- Remove temporary styles, console probes, timers, and diagnostic commands.

Consult these primary sources when adapting the baseline:

- [Tauri configuration reference](https://v2.tauri.app/reference/config/)
- [`window-vibrancy` repository](https://github.com/tauri-apps/window-vibrancy)
- [CSS cascade layers](https://www.w3.org/TR/css-cascade-5/#layer-order)
- [CSS system colors](https://www.w3.org/TR/css-color-4/#css-system-colors)
