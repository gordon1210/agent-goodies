# Audit & Polish Route

Use this route for visual review, UX review, conversion audit, accessibility review, implementation QA, originality review, design debt, or requests to explain why an interface feels generic, inconsistent, or unfinished.

Default to **audit-only** when the user asks for a review. Edit only when the user asks to fix or improve.

Apply the entrypoint's read-only boundary through completion: no product
repairs, process/report files, handoff updates, or staging without separate
authorization. Use the audit-report template as response structure when file
writes are not authorized.

## Load now

- [`../guides/anti-generic-critique.md`](../guides/anti-generic-critique.md)
- [`../guides/validation-and-qa.md`](../guides/validation-and-qa.md)

Load only the domain guide implicated by the task:

- conversion and messaging → [`../guides/conversion-and-copy.md`](../guides/conversion-and-copy.md)
- visual hierarchy and foundations → [`../guides/visual-foundations.md`](../guides/visual-foundations.md)
- components and states → [`../guides/components-and-states.md`](../guides/components-and-states.md)
- motion → [`../guides/interaction-and-motion.md`](../guides/interaction-and-motion.md)
- accessibility → [`../guides/accessibility-and-localization.md`](../guides/accessibility-and-localization.md)
- implementation, responsiveness, performance, or SEO → [`../guides/implementation-performance-and-seo.md`](../guides/implementation-performance-and-seo.md)
- brand/reference overlap → [`../guides/references-and-originality.md`](../guides/references-and-originality.md)

## Establish the audit boundary

State:

- artifact and flows checked
- source, rendered output, viewports, states, and references available
- requested audit dimensions
- whether fixes are authorized
- anything inaccessible or unverified

Do not clear an entire product after checking one screenshot or the default state.

## Review in impact order

Inspect:

1. **Intent and comprehension** — Can the intended audience understand the page or task?
2. **Hierarchy and flow** — Does attention move to the right information and action?
3. **Content and trust** — Are claims specific, consistent, supported, and honest?
4. **Interaction and state** — Can users complete, recover, and understand system status?
5. **Accessibility and inclusion** — Can users operate and understand it through supported input and assistive paths?
6. **Responsive and content resilience** — Does it survive narrow widths, zoom, long content, localization, and missing data?
7. **Visual coherence and brand** — Do tokens, assets, density, and details form one system?
8. **Motion and performance** — Does behavior help without creating delay, instability, or distraction?
9. **Originality and specificity** — Does it express this product without copying a reference or falling into generic defaults?
10. **Implementation quality** — Does source structure support the visible result without unnecessary complexity?

## Severity discipline

Use severity based on user and business impact:

- **Critical** — blocks a core task, causes data loss/security harm, creates a major legal/accessibility barrier, or makes the artifact unusable for a substantial supported context.
- **High** — materially damages comprehension, conversion, task completion, recovery, or brand trust.
- **Medium** — visible or recurring inconsistency that degrades quality but does not block the main outcome.
- **Low** — isolated polish with limited impact.

Do not label subjective style preferences as critical. Group repeated symptoms under one root cause.

## Evidence format

For each finding, provide:

- severity
- location or state
- observed evidence
- user or business impact
- smallest effective fix
- verification method

When comparing references, cite both the current artifact and the reference. Describe overlaps and originality risk; do not make unsupported legal conclusions.

## Fix mode

When edits are authorized:

1. fix critical and high-impact root causes first
2. preserve working behavior and established conventions
3. make the smallest coherent change set
4. rerun affected states and regression checks
5. do not expand into a redesign unless required

Safe, local polish can be fixed directly. Surface tradeoffs before changes that alter brand, content meaning, navigation, conversion strategy, or core interaction.

## Verdict

Use one:

- **Approve in checked scope**
- **Approve with follow-up**
- **Changes recommended**
- **Block release**
- **Blocked by missing evidence**

Never approve coverage that was not inspected.

Use [`../templates/audit-report.md`](../templates/audit-report.md) for substantial reviews.
