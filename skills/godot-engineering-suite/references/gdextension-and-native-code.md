# GDExtension and native code

Use for `.gdextension`, C/C++, Rust or other native bindings loaded by Godot.

## Risk model

A native extension runs with the process's operating-system privileges. Loading the project or editor may execute native code. Treat unknown binaries and build scripts as untrusted; load `security-and-untrusted-content.md` before running them.

## Compatibility

- Detect the minimum/maximum Godot versions declared by the extension.
- Match `godot-cpp` or binding versions to the intended engine branch.
- Review platform/architecture library entries in the `.gdextension` file.
- Do not assume a binary built for one patch, compiler runtime or architecture is portable.
- Verify debug and release library selection and feature tags.

## API boundary

Expose a small, typed interface. Validate all script-provided data at the boundary. Define ownership for Objects, RefCounted values, raw pointers, callbacks and threads. Never hold a pointer to an engine object without a lifecycle strategy.

Do not call scene-tree or rendering APIs from arbitrary worker threads. Marshal results back to the main thread using a supported project pattern.

## Build system

Follow the repository's pinned compiler, SCons/CMake/Cargo wrapper and CI environment. Do not upgrade binding generators or regenerate all bindings as part of an unrelated fix.

Keep generated binding code separate from authored code. Preserve visibility/export macros and platform-specific linker settings.

## Failure handling

- Avoid exceptions crossing C ABI or engine boundaries.
- Convert failures into explicit error values/logging consistent with the project.
- Guard callbacks during shutdown and hot reload.
- Ensure initialization can fail cleanly without partially registered classes.
- Free resources in the matching termination level.

## Verification

Build all affected architectures, then load with the exact Godot binary. Test editor startup if editor classes are registered, headless startup if server use is supported, and release export if library stripping/packaging changed. Check that the exported artifact contains the correct native libraries and no developer-only binaries.
