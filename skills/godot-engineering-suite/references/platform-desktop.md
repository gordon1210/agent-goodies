# Desktop platforms

Use for Windows, macOS and Linux behavior, packaging and native integration.

## Keep platform code behind adapters

Gameplay should not branch on operating-system names throughout the codebase. Wrap file dialogs, notifications, rich presence, native windows, platform stores and OS services behind narrow interfaces with a fallback.

## Files and process behavior

Use Godot path APIs and `user://`. Account for path case, separators, permissions, sandboxed app locations and read-only install directories. Never assume the working directory is the project or executable directory.

External process launching needs argument arrays, strict input validation and explicit user intent. Avoid depending on shell built-ins.

## Windowing and display

Test DPI scaling, multiple monitors, focus loss, fullscreen/windowed transitions, minimize/restore, high-polling input, different refresh rates and graphics backends. Persist a safe fallback resolution/mode so invalid settings cannot make the game unusable.

## Windows

Verify code signing, runtime/native DLL packaging, Defender/SmartScreen behavior, controller APIs and both supported display backends. Do not ship developer DLL search paths or rely on case-insensitive paths.

## macOS

Verify universal/target architecture, code signing, hardened runtime, entitlements and notarization. Test Retina scaling, app bundle resource paths and permission prompts. Native libraries must be signed consistently inside the bundle.

## Linux

Test the intended distribution baseline and graphics/window systems. Avoid linking native extensions against newer system libraries than the target supports. Check Wayland/X11 behavior, executable bits, desktop integration and case-sensitive paths.

## Verification

Run the release export on each supported OS, preferably on a clean machine or VM. Check install/update/uninstall, first-run permissions, save location, crash logs, GPU fallback and native dependency resolution.
