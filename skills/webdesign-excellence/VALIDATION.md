# Package validation

**Edition:** 1.0.0\
**Date:** 2026-09-06

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

The packaging process checks frontmatter, relative link targets, one-hop reference
reachability, reference load triggers, fenced blocks, fixture path consistency,
Python syntax, and archive integrity. Detailed observed results are recorded below.


## Observed results

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

## Not executed or established

**Agent evaluations executed: 0.** The 28 fixtures are available for subsequent
model-in-the-loop testing. No claim is made about routing accuracy across models,
conversion improvement, visual-quality improvement, or installation in a live
Codex/Claude Code session.

CSS parsing is a static syntax check, not browser compatibility, rendering,
interaction, or accessibility verification. No generated website was rendered or
profiled for this delivery. The source register documents research; the package
validator does not crawl external links or guarantee their continuing availability.

The optional validator requires only Python's standard library. PyYAML and tinycss2
were used as additional packaging-time checks, not runtime dependencies of the skill.
