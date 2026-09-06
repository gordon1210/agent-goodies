# CI and headless automation

Use for automated imports, tests, exports, dedicated servers and reproducible validation.

## Pin everything that affects output

Pin Godot version/edition, export templates, container image digest where practical, .NET SDK, native compiler/bindings and platform build tools. Log versions at job start.

Do not download and execute an unverified latest binary in every run. Validate checksums/signatures and cache immutable artifacts.

## Job stages

A typical pipeline separates:

1. repository/static checks;
2. Godot import/parse check;
3. language/native builds;
4. targeted/unit/integration tests;
5. export jobs by platform;
6. artifact smoke tests and signing;
7. release publication.

Keep privileged signing/store jobs isolated from untrusted pull-request code.

## Headless commands

Use repository wrappers when present. Common Godot 4 patterns include:

```bash
godot --headless --path . --import
godot --headless --path . --quit-after 1
```

The second command starts the configured project; it may execute game code and is not equivalent to a pure parser. Use a dedicated test runner/scene for reliable assertions.

## Cache policy

Caching `.godot/` can speed imports but couples the cache to engine version, platform, import settings and source asset hashes. Key it accordingly and fall back to a clean import when diagnosing failures. Never treat cache contents as source artifacts.

## Logs and artifacts

Preserve concise test results, crash dumps and export manifests. Avoid leaking environment variables or signing paths. Set timeouts for hung projects and terminate child processes cleanly.

## Platform reality

Desktop and server exports can often run in general CI. Mobile, console, XR and signing may require hosted runners, licensed SDKs or device farms. Keep shared tests portable and platform jobs explicit.
