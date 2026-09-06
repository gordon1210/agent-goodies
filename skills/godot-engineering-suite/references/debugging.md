# Debugging

Use for parser errors, runtime errors, crashes, incorrect behavior and flaky failures.

## Evidence-first loop

1. Reproduce with the smallest reliable command/scene.
2. Capture exact Godot version, renderer, platform and error output.
3. Identify the first relevant error, not the largest downstream stack.
4. Trace ownership and lifecycle around the failing object.
5. Form one falsifiable hypothesis.
6. Add the narrowest instrumentation or test.
7. Fix the cause, remove noisy diagnostics and rerun the reproducer.

Do not start by adding null checks to every access or deferred calls to every mutation.

## Common classes

### Parse/type/import failure

Check engine version, syntax, class_name collisions, cyclic dependencies, missing resources, path case and import status. C# also requires a successful build before the editor sees changes.

### Freed or null object

Determine whether the reference is required, optional, not ready yet or stale after an await/scene change. Repair the ownership/lifecycle contract. Use `is_instance_valid()` only when freeing is a legitimate runtime possibility.

### Signal duplication/order

Locate every connection, connection lifetime and synchronous side effect. Verify callback signatures and whether scene re-entry reconnects without teardown.

### Physics anomaly

Inspect tick rate, body type, velocity semantics, collision layers/masks, shape transforms and mutation timing. Enable visible collision shapes.

### Render-only issue

Confirm renderer, material sharing, camera/environment owner, transparency/depth and imported resource settings. Use render debug views and frame captures.

### Crash/native failure

Collect native stack traces, matching symbols, extension versions and minimal reproduction. Treat unknown native libraries as untrusted.

## Logging

Include stable entity/request IDs and relevant state transitions. Rate-limit repetitive frame errors. Do not log secrets, tokens or private user data.

## Verification

Rerun the original reproduction plus nearby edge cases. A disappearing error without a causal explanation is not a confirmed fix.
