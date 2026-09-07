# Sources and maintenance

**Research date: 2026-09-06.** Source links are normal Markdown URLs, not chat-only
citation tokens. Open this register only for provenance or maintenance; it is not
part of the default design-task context.

WCAG is normative; its Understanding documents are explanations. APG examples
require adaptation and testing. Platform documentation establishes API behavior,
not universal browser support or the quality of a design. Brand-system guidance
and practitioner essays supply judgment, not mandatory rules. Repository prompts
are inspiration only. The skill's style taxonomy, compositions, and routing rules
are original synthesis.

## Maintenance rules

Recheck exact browser features before using them on a project. Recheck client install
locations against the installed version. Revisit accessibility criteria and field
performance definitions when updating this package. Do not silently turn a lab
observation into a universal requirement. Preserve source links and record important
changes to a module's intent or behavior. Links may redirect or evolve; a source
being reachable does not make every example production-ready.

## Format, installation, and evaluation

- [Agent Skills specification](https://agentskills.io/specification) — Package format and progressive disclosure.
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) — Codex project and personal skill discovery; client-specific behavior.
- [Claude Code: Skills](https://code.claude.com/docs/en/skills) — Client-specific installation; recheck for the installed client.
- [OpenAI: Testing Agent Skills Systematically](https://developers.openai.com/blog/eval-skills) — Behavioral evaluation approach.

## Accessibility standards and explanations

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) — Normative accessibility standard; not a legal compliance opinion.
- [WAI: Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) — Text contrast thresholds and exceptions.
- [WAI: Target Size (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) — 24 CSS pixel criterion and exceptions.
- [WAI: Focus Not Obscured (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html) — AA focus obstruction criterion.
- [WAI: Text Spacing](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html) — User text-spacing overrides.
- [WAI: Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow) — Narrow viewport and zoom requirements.
- [WAI: Non-text Contrast](https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html) — Contrast for necessary graphical and UI information.
- [WAI: Pause, Stop, Hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html) — Automatically moving and updating information.
- [WAI-ARIA Authoring Practices patterns](https://www.w3.org/WAI/ARIA/apg/patterns/) — Interaction patterns, not a substitute for testing.
- [APG: Modal dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) — Modal focus and dismissal behavior.
- [APG: Tabs](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/) — Tab roles, selection, and keyboard operation.
- [WAI: Form notifications](https://www.w3.org/WAI/tutorials/forms/notifications/) — Error identification and feedback.

## Platform and performance

- [web.dev: Web Vitals](https://web.dev/articles/vitals) — LCP, INP, CLS and real-user assessment.
- [web.dev: Optimize LCP](https://web.dev/articles/optimize-lcp) — Discovery, prioritization, and rendering of LCP resources.
- [web.dev: High-performance CSS animations](https://web.dev/articles/animations-guide) — Animation rendering cost and profiling.
- [MDN: Container queries](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries) — Container sizing and progressive enhancement.
- [MDN: font-optical-sizing](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-optical-sizing) — Optical-size axis behavior.
- [MDN: text-wrap](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-wrap) — Wrapping features; check individual value support.
- [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/prefers-reduced-motion) — Motion preference detection.
- [MDN: forced-colors](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/forced-colors) — System palette behavior.
- [MDN: prefers-reduced-transparency](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/prefers-reduced-transparency) — Optional preference; not a universal fallback.
- [MDN: backdrop-filter](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter) — Backdrop filtering and stacking constraints.
- [MDN: CSS scroll-driven animations](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations) — Scroll and view timelines.
- [MDN: animation-timeline](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline) — Support-sensitive syntax and animation shorthand reset.
- [MDN: Intersection Observer](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API) — Asynchronous visibility observation, not continuous scroll progress.
- [MDN: position](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/position) — Sticky positioning and containing ancestors.
- [MDN: View Transition API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API) — Same-document and cross-document transition mechanisms.
- [MDN: WebGL best practices](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices) — GPU resource constraints and rendering practices.
- [Motion: Accessibility](https://motion.dev/docs/react-accessibility) — Library-specific reduced motion behavior.
- [GSAP: matchMedia](https://gsap.com/docs/v3/GSAP/gsap.matchMedia%28%29/) — Responsive setup and cleanup.
- [Playwright: Visual comparisons](https://playwright.dev/docs/test-snapshots) — Deterministic screenshot testing and limitations.

## Design-system and practitioner guidance

- [Emil Kowalski: Great Animations](https://emilkowal.ski/ui/great-animations) — Practitioner motion principles; not a standard.
- [Emil Kowalski: You Don’t Need Animations](https://emilkowal.ski/ui/you-dont-need-animations) — Restraint in frequently repeated interactions.
- [Carbon: Motion](https://carbondesignsystem.com/elements/motion/overview/) — Productive versus expressive motion; brand-specific advice.
- [Carbon: Typography style strategies](https://carbondesignsystem.com/elements/typography/style-strategies/) — Task versus expressive typography roles.
- [Ahmad Shadeed: Responsive Design](https://ishadeed.com/article/responsive-design/) — Content- and component-aware responsive thinking.

## Inspected inspiration, not production endorsement

- [claude-directory README](https://github.com/pulkitxm/claude-directory/blob/f3d7e12f34bf7d90130dce3ec3b26cf69c29794e/README.md) — Inspiration inventory, not production verification.
- [claude-directory: superdesign-technical-system](https://github.com/pulkitxm/claude-directory/blob/f3d7e12f34bf7d90130dce3ec3b26cf69c29794e/templates/superdesign-technical-system/prompt.md) — Prompt inspected; original site fidelity and runtime quality not verified.
- [claude-directory: superdesign-studio-editorial](https://github.com/pulkitxm/claude-directory/blob/f3d7e12f34bf7d90130dce3ec3b26cf69c29794e/templates/superdesign-studio-editorial/prompt.md) — Prompt inspected; original site fidelity and runtime quality not verified.
- [claude-directory: superdesign-modern-atmospheric](https://github.com/pulkitxm/claude-directory/blob/f3d7e12f34bf7d90130dce3ec3b26cf69c29794e/templates/superdesign-modern-atmospheric/prompt.md) — Prompt inspected; original site fidelity and runtime quality not verified.

Repository references are pinned to an inspected commit. See [research scope](RESEARCH-NOTES.md) for the exact limits of the review.
