# webdesign-excellence

A portable, English-language agent skill for coherent web art direction and
implementation. Small entry point; **12 separate styles**, **18 opt-in techniques**,
page-specific routes, and explicit quality checks. No framework, font stack, color
palette, animation library, or plugin is mandatory.

## Choosing a design skill

Use this skill for concrete web pages, components, charts, and visual refinement.
When `design-ui-excellence` is also available, prefer it for strategy, messaging
and SEO, content architecture, campaigns, brand and design systems, and UX planning
across screens. An explicit skill choice takes precedence.

Both packages work independently. Use the relevant guidance available in the
selected skill; do not require the other package or load both full workflows.
For mixed projects, carry the existing brief and decisions into the next phase
without restarting discovery.

## Start here

Install the entire `webdesign-excellence` directory, not just SKILL.md. Its relative
links need `references/` alongside it. Do not paste the entire library into a system
prompt; that defeats the routing.

| Host | Project installation | Personal installation |
|---|---|---|
| Codex | `.agents/skills/webdesign-excellence/` | `~/.agents/skills/webdesign-excellence/` |
| Claude Code | `.claude/skills/webdesign-excellence/` | `~/.claude/skills/webdesign-excellence/` |

Use one installation scope per host unless there is a deliberate reason for multiple
copies. Check discovery in the installed client; do not assume duplicate copies are
merged. In other Agent Skills-compatible hosts, use that host's documented skill
location. This ZIP is a skill directory, not a universally installable plugin bundle.

Installation references, checked 2026-09-06:
[OpenAI](https://learn.chatgpt.com/docs/build-skills),
[Claude Code](https://code.claude.com/docs/en/skills), and
[Agent Skills format](https://agentskills.io/specification).

Example request:

```text
Use webdesign-excellence to design and implement this landing page.
Preserve the existing stack. Choose one coherent direction from the brief,
load only relevant references, and verify the actual result.
```

For a targeted change:

```text
Use webdesign-excellence to fix this mobile layout problem.
Preserve the existing visual system and unrelated behavior.
Do not perform a style exploration or add an animation library.
```

Claude Code also supports explicit invocation as `/webdesign-excellence` followed
by the task. Other hosts may expose a picker or their own invocation syntax; use
that client's documented mechanism.

## How routing works

```text
Task
  ├─ New direction → brief → choose one style → page route
  ├─ Existing extension → preserve system → affected page/component
  ├─ Targeted fix → immediate issue only; normally no style dossier
  └─ Review → evidence-based critique; no automatic redesign

Selected work → relevant foundation / technique → implementation → verification
```

The router recommends 2–4 reference files initially, with additional modules read
when a phase needs them. All reference modules are directly discoverable from
[SKILL.md](SKILL.md); no multi-hop catalog traversal is required. Reference count
is not a request to load the full set.

Styles own the visual grammar. Techniques implement a specific mechanism. An
editorial page can use a grid and a restrained image treatment without importing
three additional styles. A genuine hybrid needs ownership of typography, palette,
geometry, imagery, and motion. Separate alternatives remain separate.

## Coverage

| Area | Included |
|---|---|
| Styles | Editorial, technical, product-led, quiet luxury, organic, expressive graphic, neo-brutalist, cinematic, atmospheric, glass, retro-futurist, immersive spatial |
| Techniques | Structural grids, motion systems, text reveals, scroll narratives, stacking cards, product demos, image treatments, texture, light/glass, pointer effects, view transitions, existing video, SVG/Canvas/3D, carousels, choreography, motion-reference analysis, 3D art direction, 3D production |
| Page types | Marketing/services, commerce, portfolios, publications/docs, working applications |
| Data visualization | Chart selection, honest scales and data states, labeling, responsive composition, accessible interaction and alternatives |
| Foundations | Brief, style selection, composition, typography, color, responsive behavior, assets, implementation |
| Quality | Navigation/forms, accessibility, performance, critique, verification |
| Optional handoff | Design contract, implementation handoff, review template |

Each style describes a visual thesis, concrete composition, boundaries, and how it
survives mobile/fallback conditions. Technique modules describe when to use the
mechanism, implementation considerations, and cases where it should be omitted.
They are guidance, not a copy-paste production component library.

## Guardrails that matter

Preserve semantics, accessible controls, truthful feedback, and existing project
rules. No fake progress or successful requests. No invented customers, endorsements,
metrics, or live status. No paid-source bypass. No hidden cursor as a default.
No forced motion, decorative scroll capture, or essential content trapped in an
unavailable enhancement. No arbitrary reference-code execution or external upload.

Conversely, the skill does **not** ban cards, gradients, rounded corners, color,
symmetry, or familiar typefaces. Their suitability follows the brief. “Modern”
means a coherent solution to the job, not an obligatory collection of effects.

## Optional motion, 3D, and existing-video routes

Use choreography for substantial multi-phase sequences; a hover or disclosure fix
needs no beat map. 3D art direction and production are techniques: an editorial
page with one interactive product section retains its editorial primary style.
Explicit interactive 3D must be implemented as requested, with a useful failure
alternative and missing capabilities reported honestly.

To select existing-video integration within this skill, say:

```text
Use webdesign-excellence to integrate my supplied product-demo.mp4 as an
inline player. Preserve its meaningful audio and use the existing page design.
```

This separately selectable route is documented in [existing video](references/technique-video.md),
not a nested skill or a new slash command. It never generates video. Embedding the
actual clip, reconstructing selected behavior in web code, and taking loose inspiration
are different requests; an attachment alone does not select one.

The [original examples](examples/README.md) cover kinetic composition, a truthful
local workflow, loaded mesh-based 3D, and a minimal synthetic-media test specimen.
Load their source only when useful for implementation. They are mechanisms to adapt,
not a mandatory site template or evidence of general agent quality.

## Package and verification

Normal skill activation requires no runtime dependencies, hooks, MCP server,
renderer, or media tooling. The optional [example harness](examples/README.md) uses
an existing compatible Three.js installation for its 3D specimen; those dependencies
belong to examples only. No downloaded fonts, third-party media, or upstream prompts
are bundled. The optional Python validator is
for maintainers; agents do not need to execute it for design work. It uses only the
Python 3.10+ standard library and does not access the network or write project files.

From the skill directory:

```sh
python3 scripts/validate_package.py
```

On systems where Python is named `python`, use that executable instead. The validator
checks this package's deliberately small frontmatter subset, local link targets,
reference reachability, Markdown fences, and evaluation fixture integrity. It is
not a general Markdown/YAML parser or an agent-behavior test suite.

See [VALIDATION.md](VALIDATION.md) for the actual checks performed at packaging time.
The [behavioral fixtures](evals/README.md) are supplied for real agent evaluation;
they are not represented as executed model tests.

## Sources and limits

[Research notes](RESEARCH-NOTES.md) document what was inspected and what was not.
[Sources](SOURCES.md) includes normal clickable URLs, pinned repository references,
and maintenance guidance. The skill is original synthesis, not a redistribution
of the gallery or its paid inspirations. Historical packaging claims remain dated. See [current validation](VALIDATION.md)
for the exact runtime, visual, and agent checks performed for this update.
