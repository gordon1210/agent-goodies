# Package validation

**Original edition:** 1.0.0\
**Original packaging date:** 2026-09-06

The original sections concern distributed skill files. The dated extension section
also records example runtime/visual checks and bounded agent decision probes.
Behavioral fixture counts alone are never executed agent-test counts.

## Reproduce the structural check

From this directory, run:

```sh
python3 scripts/validate_package.py
```

The script reads package text and returns a JSON report to standard output. It does
not access the network, install dependencies, execute a model, or modify files.
The frontmatter check deliberately supports only the small subset shipped here.

## Checks and limits

The original packaging process checked frontmatter, relative link targets, one-hop reference
reachability, reference load triggers, fenced blocks, fixture path consistency,
Python syntax, and archive integrity. Detailed observed results are recorded below.


## Original packaging results (2026-09-06)

| Check | Result |
|---|---|
| Package files | 56 files: 54 Markdown, 1 JSON fixture collection, 1 optional Python validator |
| Main entry point | 92 lines; 790 whitespace-delimited words, not a tokenizer measurement |
| Reference inventory | 45 modules: 12 styles, 14 techniques, 19 page/foundation/component/quality modules |
| Reference size | 316–582 whitespace-delimited words each; approximately 384 on average |
| Internal Markdown links | 64 local targets checked; none missing or escaping the package |
| Routing reachability | All 45 reference modules directly linked from SKILL.md |
| Frontmatter | Passed the package subset check and an additional PyYAML safe-load check |
| Code fences | All Markdown fences closed |
| CSS specimens | 8 blocks parsed with tinycss2; no parse errors detected |
| Python | Validator syntax parsed successfully; unmodified package check returned success |
| Fixture integrity | 28 unique cases; referenced paths and style constraints checked |
| Validator negative tests | 8 deliberately damaged temporary package copies correctly rejected |
| Sources | 44 register entries; repository inspiration pinned to an inspected commit |
| Archive | One skill root; CRC integrity and extracted-package validation checked |

The eight validator rejection cases were: missing reference, broken local link,
invalid frontmatter, unclosed fence, a disallowed style in a fixture, a chat-only
citation marker, an escaping relative path, and an unexpected binary-file extension.
Those checks were run on disposable copies, not by damaging the delivered package.

## Original evaluation limits

**Agent evaluations executed at packaging time: 0.** The original 28 fixtures were supplied for subsequent
model-in-the-loop testing. No claim is made about routing accuracy across models,
conversion improvement, visual-quality improvement, or installation in a live
Codex/Claude Code session.

CSS parsing is a static syntax check, not browser compatibility, rendering,
interaction, or accessibility verification. No generated website was rendered or
profiled for this delivery. The source register documents research; the package
validator does not crawl external links or guarantee their continuing availability.

The optional validator requires only Python's standard library. PyYAML and tinycss2
were used as additional packaging-time checks, not runtime dependencies of the skill.

## Repository update checks (2026-09-07)

This update separates skill selection from `design-ui-excellence` and adds a
directly routed data-visualization module. Original packaging results above are
historical; they do not claim that archive, CSS-parser, or negative-mutation checks
were repeated for the updated files.

| Check | Observed result |
|---|---|
| Package validator | Passed: 57 files, 55 Markdown files, 46 directly routed reference modules, 70 local links, 37 behavioral fixtures |
| Entry point | 108 lines; 917 whitespace-delimited words |
| Repository validator | Passed both marketplaces, 1 plugin, and 11 standalone skills |
| Local links | Both design skill packages checked; no missing or escaping Markdown targets |
| YAML | Both skill frontmatters and the changed UI metadata parsed with Ruby's `YAML.safe_load`; descriptions satisfy the length limit |
| Claude marketplace validator | Passed |
| Whitespace | `git diff --check` passed |

### Independent routing smoke test

One independent `gpt-6-astra` subagent read only the two current `SKILL.md` files,
without the implementation diff, evaluation fixtures, or intended answers. It
returned these initial selections and actions for eight hypothetical requests:

| Available skills and request | Observed selection |
|---|---|
| Both: build the supplied landing-page design in React; preserve approved copy | `webdesign-excellence`; inspect existing design and implementation |
| Both: define messaging, page inventory, and search intent; no implementation | `design-ui-excellence`; content/SEO planning |
| Both: define tokens and component governance for three products | `design-ui-excellence`; design-system planning |
| Both: repair mobile comparison in a revenue chart; preserve calculations | `webdesign-excellence`; data visualization and responsive guidance |
| Both: explicitly use `design-ui-excellence` to implement a portfolio homepage | `design-ui-excellence`; honor explicit selection |
| Only `design-ui-excellence`: implement settings using existing components | `design-ui-excellence`; use its standalone product-interface route |
| Both: plan onboarding across six screens, then implement the first once settled | `design-ui-excellence` for planning, then `webdesign-excellence`, carrying decisions forward |
| Both: optimize billing SQL; do not touch UI | Neither design skill |

No material selection contradiction was reported. The mixed-phase request still
requires task context to establish when its plan is settled; the routing rule does
not itself add an approval checkpoint.

This was one routing-only pass, not execution of the 37 project fixtures or a
benchmark of host auto-discovery. No chart implementation, browser rendering,
assistive-technology run, or measured visual-quality comparison was performed.
The package validator's `agent_evaluations_executed: 0` describes that script: it
checks fixture data and never invokes a model.

## Motion and 3D extension (2026-09-09)

The baseline was the clean current checkout, retained as a task-created temporary
snapshot. Its validator passed: 57 files, 46 references, 14 techniques, 37 behavioral
fixtures, 108 entrypoint lines and 917 whitespace-delimited words. No prior
packaging result was substituted for an executed check.

### Bounded baseline/updated decision probes

Two fresh native `astra_specialist` agents (`gpt-6-astra`, medium) each received the
same three held-out briefs and a different skill path. Both had no conversation
history, no expected answers, no authored examples/evals/maintainer docs, no browser,
no editing, and the same maximum 350-word response allowance per brief. They could
read the entrypoint and select references. The three briefs shared one context
within each probe; later answers could reuse earlier reference knowledge.

Prompts requested implementation decision records, not code:

1. Existing white/blue library site: user-played exact “A place to read. A place to
   meet.” type sequence around one persistent blue circle, ending beside the hours
   link; native CSS/JS, direct jumps, 390×520 viewport.
2. Established editorial bike shop: supplied named glTF hub, washed-out aluminum,
   drifting end cap after repeated explosion/reassembly, detached narrow-screen
   HTML label; installed Three.js; asset/screenshot inaccessible in the exercise.
3. Existing preferences panel: repair slow disclosure only, ignore an attached
   promotional recording, preserve explicit pause on the existing demo.

| Observed behavior | Baseline | Updated |
|---|---|---|
| Motion initial routes | Motion + text (2) | Motion + choreography + text + responsive (4) |
| 3D initial routes | Motion + rendering (2) | Rendering + 3D art direction + production (3) |
| Small fix | Local timing and existing mechanism; no video route | Local token assignment; no video or choreography route |
| Sequence ownership | Explicit progress sampler, stable anchor, pause and resize | Same fundamentals plus explicit beat/hold planning and elapsed timestamps |
| 3D diagnosis | Baseline transforms, material/color checks, projected labels | Same fundamentals plus imported-track ownership, ordered world-matrix updates and collision handling |
| Evidence limits | Missing actual assets/runtime acknowledged | Missing actual assets/runtime acknowledged |

Both probes handled the briefs plausibly. The baseline already produced strong
technical decisions; these observations do **not** establish a general quality gain
or a numerical improvement score. The updated probe found the specialized knowledge
through selective routes without choosing a new primary style or video workflow.
This was six hypothetical decision responses across two agent runs, not six built
sites or execution of the 49 routing fixtures. Comparable-budget implementation and
rendered-quality agent benchmarks remain unexecuted. Raw responses are retained in
this task's native agent records (`baseline_probe`, `updated_probe`).

### Entrypoint and loading impact

The updated entrypoint is 132 lines / 1,141 whitespace-delimited words: +24 lines and
+224 words. There are 50 directly routed references, including 18 techniques and the
unchanged 12 styles. Initial loading remains 2–4 references; new modules are opt-in
and staged as needed. Examples and maintainer records are not initial reference
loads. Each new specialized reference stays below the existing 1,500-word ceiling.

### Structural and source checks

| Executed check | Result |
|---|---|
| `python3 skills/webdesign-excellence/scripts/validate_package.py` | Passed: 74 files, 50 references, 18 techniques, 12 styles, 49 behavioral fixtures, one glTF fixture; no containment/link errors |
| `python3 scripts/validate_repo.py` | Passed: one plugin, 11 standalone skills and both marketplaces |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/webdesign-excellence/tests -v` | 18 tests passed, including malformed additions and retained historical rejection classes |
| `claude plugin validate .claude-plugin/marketplace.json` | Passed |
| Ruby `YAML.safe_load` of SKILL frontmatter | Passed name/description checks |
| `node --check` on the example JavaScript files | Passed; syntax only |
| JSON parsing of `evals/routing-cases.json` | Passed |
| Asset regeneration in task-created scratch using `author-asset.py` | Exact byte match: 110,874-byte glTF; 79,968 embedded buffer bytes |
| `git diff --check` | Passed |

Asset SHA256: `bda80ffde64373424ace8c69e5a75c37f4939c47ca020c14509a57c7a31542cb`.
The reproducibility check executed a copied authoring script in a new temporary
directory and compared the generated bytes to the shipped fixture. It did not
modify the fixture during review.

The bundled skill-creator `quick_validate.py` was attempted but could not start:
`ModuleNotFoundError: No module named 'yaml'`. No package was installed to satisfy
that optional check. Ruby YAML and the package subset validator passed independently.
The installed Codex CLI exposes no dedicated validation subcommand under `plugin`;
no live installation or discovery test was claimed. No manifests were changed.
The native JS/HTML harness has no TypeScript compilation, bundler, or configured
lint task; its executed syntax and browser checks are reported separately.

### Browser behavior and rendered review

The [example README](examples/README.md) is the reproducible runtime/evidence record.
Its exact commands serve the native harness with an existing Three.js 0.185.1
package and execute `examples/test-browser.js` via the available Playwright tool's
`browser_run_code_unsafe` filename argument. **30 browser assertions passed** in
Chromium 152.0.7977.76. The optional standalone Playwright CLI wrapper was
syntax-checked but not executed; no new dependency was installed.

Executed behavior includes forward/reverse/random sequence sampling, persistent
anchor geometry, replay/pause, rapid reveal interruption, actual part-position
reassembly equality, immediate truthful local calculations, selection identity,
resize/reflow, runtime reduced-motion changes, explicit pause across visibility
changes, repeated mounting, stale successful/failed loads, missing model/renderer,
injected context loss, and injected persisted page lifecycle. The video specimen
exercised synthetic decode/playback, seek-driven overlays, offscreen pause, failure
fallback, retained media after restoration, and resumed frame callbacks.

Injected context/lifecycle events test handlers; they do not prove a real GPU
context loss or browser bfcache admission. Other browser engines were not tested.
The synthetic local clip measured 640×360, 12,551 bytes, fetched MIME `video/webm`,
and 1.965724 seconds in the final run versus two seconds of authored recording
intent. Generation time and bytes can vary. It has no audio track by construction;
no real source audio, arbitrary codec, or campaign footage was inspected.

Astra inspected screenshots at 1280×900, 390×720 and 1000×450, covering assembled
and exploded 3D, kinetic connection/reduced/narrow/short states, workflow result,
and video seek. Review corrected inward shade winding/normals, projected label
placement, and reveal interruption behavior. Screenshots are task-local at:

- `/tmp/webdesign-3d-wide.png`, `/tmp/webdesign-3d-exploded.png`,
  `/tmp/webdesign-3d-narrow.png`, `/tmp/webdesign-3d-short.png`
- `/tmp/webdesign-kinetic-middle.png`, `/tmp/webdesign-kinetic-reduced.png`,
  `/tmp/webdesign-kinetic-narrow.png`, `/tmp/webdesign-kinetic-short.png`
- `/tmp/webdesign-workflow.png`, `/tmp/webdesign-video.png`

A playback recording was captured at
`/tmp/webdesign-motion-recordings/page@dac5ddb97fa5a9f712d0df2f8a6db89e.webm`.
Continuous playback smoothness was not visually reviewed; screenshots and sampled
states do not establish it. These recordings and screenshots are not distributed
assets. The browser-generated console log was preserved outside the repository
in task-created temporary storage.

Performance observations: macOS browser reporting MacIntel, Chromium 152, DPR 1,
1280×900; 11 rendered calls, 7,938 rendered triangles including shadow passes, six
geometries. A tight 60-sample `sampleAssembly` loop measured 0.10 ms median and
0.30 ms p95 CPU submission. This excludes GPU completion, asset decode and display
pacing and is not representative hardware performance evidence. No universal
budget or production performance claim follows from it.

Blender and FFmpeg were unavailable and uninstalled. Screen-reader/assistive-
technology behavior, real audio, low-end GPU performance, cross-browser playback,
continuous-motion smoothness, and rendered baseline/updated agent implementation
benchmarks remain unverified. The authored examples, fixture validator, visual
stills and decision probes are separately reported evidence, not substitutes for
one another. Final review retained ordinary static/small-fix routes, primary-style
ownership, truthful state, and optional dependencies; all edits are package-local.
