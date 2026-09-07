# Package validation

**Original edition:** 1.0.0\
**Original packaging date:** 2026-09-06

The results in this file concern the distributed skill files, not a website built
with them. Behavioral fixtures are not executed agent tests.

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
