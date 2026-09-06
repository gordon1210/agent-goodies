# Package validation

Build/research date: **2026-09-06**.

## Completed local checks

| Check | Result | Scope |
|---|---|---|
| Package structure, routing, local links and anchors | PASS | 32 reference files, including the source register; all directly routed |
| Bundled SKILL.md metadata | PASS | YAML parsed during authoring; package-specific validator also passed |
| JSON files and source/evaluation references | PASS | 58 source records and 12 authored evaluation cases |
| Router size | PASS | 103 lines; 891 whitespace-delimited words |
| Python 3.10 grammar compatibility | PASS | AST parsing with Python 3.10 feature grammar; not execution on every Python release |
| Standard-library unit tests | PASS | 14 tests on the authoring environment |
| Contrast CLI | PASS | Positive, below-threshold, and invalid-input exit paths checked |
| Optional shader scalar math | PASS | Analytical coverage endpoints, monotonicity, bounds; not shader compilation |
| ZIP integrity | PASS | Archive CRC check and byte-for-byte content comparison after packaging |

The unit tests cover contrast calculations, invalid inputs, structural-validator
behavior, broken/path-escaping links, and the scalar mask formula. They do not
prove Godot API correctness or generated UI quality. The complete source tree was
also reviewed for unresolved package links and nonportable chat citation markers.

## Not performed

- Godot compilation, rendered scene inspection, or GPU/renderer verification.
- Keyboard/controller/device/assistive-technology tests against a running game.
- Empirical coding-agent runs or an A/B evaluation of this skill.
- Full frame-by-frame analysis of embedded portfolio videos or the listed GDC talk.
- External asset-rights clearance or platform/accessibility certification.

No Godot executable was available in the authoring environment. The optional
shader is therefore documentation-reviewed and analytically checked, but remains
uncompiled and unrendered. The two worked examples are written original briefs,
not implemented or visually approved screens.

The 12 agent cases in `evals/cases.json` are explicitly **authored-not-executed**.
Run them in an appropriate project/tool environment before claiming measured
improvements in visual quality or context efficiency.

## Reproduce local checks

From this package folder, with Python 3.10 or later:

```bash
python scripts/validate_package.py
python -m unittest discover -s tests -v
python scripts/contrast.py '#F2E7D3' '#172028' --threshold 4.5 --json
```

The scripts do not connect to the network, install dependencies, or modify project
content. Unit tests create temporary copies for negative cases. External URLs were
used during research, but the structural validator does not test their ongoing
availability. Research limitations are recorded per source in the source register.
