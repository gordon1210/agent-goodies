# Godot UI Design Excellence

An installable, English-language agent skill for distinctive, high-craft game UI
in Godot. It combines art direction, interaction design, native implementation,
and evidence-based visual review. Expedition 33 and Frostpunk 2 are reference
points for craft—not two mandatory skins to copy.

## Install

Copy the **entire `godot-ui-design-excellence` folder**, not just `SKILL.md`.
Choose the location for the agent you actually use:

| Agent / scope | Destination |
|---|---|
| Codex, project | `.agents/skills/godot-ui-design-excellence/` |
| Codex, personal | `~/.agents/skills/godot-ui-design-excellence/` |
| Claude Code, project | `.claude/skills/godot-ui-design-excellence/` |
| Claude Code, personal | `~/.claude/skills/godot-ui-design-excellence/` |

These paths were checked against official documentation on 2026-09-06:
[Codex](references/sources.md#a02), [Claude Code](references/sources.md#a03).
Do not install duplicate copies for the same agent scope. For another Agent
Skills-compatible tool, use its documented skill directory; no universal path
is claimed. No MCP server, plugin, package manager, or third-party game skill is required.

## Use

Codex can be addressed with `$godot-ui-design-excellence`; Claude Code with
`/godot-ui-design-excellence`. The folder also includes a descriptive trigger for
automatic discovery. Explicit invocation avoids ambiguity when several UI skills
are installed.

```text
Use godot-ui-design-excellence to design and implement the [specific screen] in
this Godot project. Preserve the existing architecture and inspect the project
before proposing changes. Target the craft of [references], but create an original
visual grammar for this game rather than copying its assets.

First resolve any genuinely missing design constraints, analyze relevant visual
references, and define one representative screen contract. Then implement and
iterate using actual in-engine captures and the relevant state/input tests.
Keep functional correctness, visual quality, and accessibility evidence separate.
Do not claim checks that your available tools cannot perform.
```

For a targeted fix, say so: "Keep the approved style. Fix selection/focus restoration
after sorting; do not redesign the inventory." The router includes a narrow repair
path and should not force a full art-direction process for every request.

## What is included

- [SKILL.md](SKILL.md): a compact entry point with direct task-to-module routing.
- **31 focused knowledge modules plus a source register**, covering visual direction,
  typography, materials, screen patterns, states, motion, asset production, Godot
  engineering, accessibility, and visual critique.
- Two original worked briefs: [Ashen Atlas](examples/ashen-atlas.md), a painterly RPG,
  and [Meridian Station](examples/meridian-station.md), a dense strategy interface.
- Reusable [design brief](assets/design-brief.md), [screen contract](assets/screen-contract.md),
  [review](assets/visual-review.md), and [handoff](assets/handoff.md) templates.
- Example [semantic tokens](assets/design-tokens.example.json) and
  [asset manifest](assets/asset-manifest.example.json), not production assets.
- An optional [decorative mask shader](examples/masked_ornament.gdshader), with
  explicit runtime-validation limits.
- [12 evaluation cases](evals/cases.json) and a [controlled evaluation plan](evals/README.md).
- Two optional local utilities and their standard-library unit tests.

All knowledge modules are directly reachable from the router. Load only the modules
needed for the current stage, usually 2–4; the full source register and examples
are not required for every edit. Routing is an instruction, not a technical guarantee
about a particular model's context use.

## What the skill teaches beyond basic UI scaffolding

It turns reference images into a visual grammar; maps player decisions to information;
separates focus, selection, and domain state; composes native text with authored art;
and requires a representative screen to survive real data and visual review before
its styling spreads across the project. It does not equate premium UI with glass,
rounded cards, gold borders, or mandatory overshoot animation.

The implementation modules address practical failure modes: container/tween conflicts,
modal input leaks, mixed safe-area coordinate spaces, mutable shared resources,
stale async previews, localization-driven reflow, and screen-reading shader ordering.
Those modules are documentation-based guidance, not a pre-tested UI runtime framework.

## Tools and scope

The core skill is instruction-only. Python **3.10+** is needed only for the optional
local checks below. No Python dependencies, network calls, account connections,
or installation commands are embedded in the skill.

To fully validate visual output, the coding agent needs an approved way to run the
project, inspect screenshots, and exercise relevant input. Asset generation requires
an actual authorized image/DCC tool; the skill does not provide one. Without those
capabilities, it must label visual/interactive acceptance as unverified.

Godot **4.7 documentation** is the research reference, not a minimum project version
or an instruction to upgrade. Resolve APIs against the actual project. Preserve
GDScript/C# choice, renderer, and existing architecture unless the user requests change.
Console input usability is not equivalent to proprietary-console export readiness.

## Local checks

From the skill folder:

```bash
python scripts/validate_package.py
python -m unittest discover -s tests -v
python scripts/contrast.py '#F2E7D3' '#172028' --threshold 4.5 --json
```

Use `python3` where that is the installed Python command. The structural validator
checks this package's simple frontmatter, local Markdown links/anchors, JSON, source
IDs, route reachability, and evaluation references. It is not a general YAML/Markdown
validator and does not contact external websites.

The contrast tool checks **opaque six-digit sRGB pairs only**. It rejects alpha
rather than pretending to evaluate compositing. Exit code 0 means the pair meets
the chosen threshold, 1 means below it, and 2 means invalid CLI input. This is not
whole-screen testing, a text-size assessment, or accessibility certification.
See [calculation reference](references/sources.md#w01).

## Research and validation honesty

Research date: **2026-09-06**. The [source register](references/sources.md) contains
58 linked sources: direct game-UI creators, first-party design articles, official
engine/agent documentation, original UX guidance, and accessibility references.
The [machine-readable register](assets/sources.json) records purpose and limits.
External sources retain their rights; no copyrighted game art or font files are bundled.

The local validation results are in [VALIDATION.md](VALIDATION.md). Python tests and
structural checks are separate from the 12 agent evaluation cases. **No coding-agent
A/B evaluation, rendered Godot demo, or device test was performed for this package.**
The optional shader was not compiled in Godot. The two worked examples are original
written design briefs, not screenshots or delivered game scenes.

This skill can guide better work; it cannot guarantee an AAA outcome. Success still
requires suitable model/tool capability, approved assets, product decisions, and
actual visual/interaction iteration.

Original package material is provided under [LICENSE.txt](LICENSE.txt). The three
skills discussed before this package are not bundled or required; their source text
was not copied into this skill.
