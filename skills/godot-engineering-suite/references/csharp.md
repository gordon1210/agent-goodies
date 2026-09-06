# C# and Godot .NET

Use when a project contains `.csproj`, `.sln` or C# scripts, or when choosing between GDScript and C#.

## Match the project toolchain

Detect the Godot .NET version, target framework, SDK pinning (`global.json`), nullable settings, analyzers and formatting rules. Do not convert a Standard project to .NET or add a C# project as an incidental change.

Run the repository's build command; otherwise use `dotnet build` from the correct solution/project directory. A successful C# build does not prove Godot scene bindings or runtime behavior.

## Godot integration

- Node classes must be `partial` where required by Godot's generated integration.
- Match Godot callback and signal method signatures exactly.
- Use `[Export]` only for editor-authored configuration and preserve serialized property names/types.
- Use generated signal-name and method-name helpers when the project convention supports them.
- Dispose managed wrappers only when ownership requires it; do not assume normal .NET lifetime maps directly to engine object lifetime.
- Check `GodotObject.IsInstanceValid()` where a referenced engine object may have been freed.

## Boundaries

Keep engine-facing node code thin when domain logic can be plain C#. Plain classes are easier to unit test and should not depend on scene-tree globals without need.

Avoid reflection-heavy or dynamic patterns in hot paths and exported targets. Verify AOT/trimming/platform restrictions before adding libraries that depend on runtime code generation, unsupported native binaries or desktop-only APIs.

## Signals and callables

Prefer C# events or Godot signals according to the boundary:

- Godot signal for editor-visible or cross-language engine communication;
- C# event/delegate for internal managed-domain communication;
- explicit method call for owned child coordination.

Unsubscribe long-lived publishers from short-lived subscribers when normal tree teardown will not break the reference.

## Serialization

Godot serializes supported exported types, not arbitrary .NET object graphs. Use Resources, ConfigFile, JSON or a deliberate save schema rather than expecting general-purpose .NET serialization to integrate with scenes.

## Verification

1. `dotnet build` with repository flags.
2. Matching Godot headless startup or targeted scene.
3. Export/AOT test on each relevant platform when dependencies or reflection behavior changed.
4. Inspect generated and imported file churn; do not commit transient `.godot/mono` build state unless the repository explicitly does.
