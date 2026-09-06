# Official documentation and versioning

Use this whenever an API, CLI flag, property, node, annotation, platform feature or migration behavior is uncertain.

## Source order

1. Documentation for the project's exact `major.minor` branch, for example `https://docs.godotengine.org/en/4.7/`.
2. Matching class reference for the same branch.
3. Godot release notes and migration guides between the project's current and target branches.
4. Engine source or official demo projects when documentation is insufficient.
5. Third-party material only as supporting evidence, never as the source of truth for current APIs.

Do not use the `latest` documentation for a stable project unless the task explicitly targets an unreleased engine. Do not assume `stable` matches the project's branch.

## Version-sensitive checks

Verify before using:

- deprecated or newly introduced nodes and properties;
- rendering features and renderer availability;
- GDScript syntax and annotation support;
- C# target framework and platform support;
- Web, mobile, XR and console export constraints;
- navigation and physics behavior;
- import formats and export options;
- command-line flags;
- GDExtension compatibility and minimum engine versions.

## Upgrade policy

Patch upgrades within one stable branch are normally lower risk, but still use version control and targeted regression checks. Minor upgrades require explicit review of migration notes, deprecated APIs, addon support, imports, rendering output, physics behavior and exports.

Do not mix an API migration into an unrelated feature or bug fix. When a workaround is needed for multiple supported minors, isolate the compatibility boundary and document when it can be removed.

## Citation discipline inside project documentation

When adding a non-obvious engine constraint to `GODOT_PROJECT.md` or an ADR, link the exact versioned official page and state the affected engine range. Avoid copying large documentation passages into the repository.
