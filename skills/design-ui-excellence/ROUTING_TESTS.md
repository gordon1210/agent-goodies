# Routing Tests

These examples document the intended dispatcher behavior. They are not additional instructions to load during normal skill use.

## Skill selection when both are available

These are intended behaviors, not claims of executed agent evaluations. Unless
the user selects a skill, choose by the deliverable before dispatching a route.

| Prompt and context | Expected selection and boundary |
| --- | --- |
| Both available: “Implement this approved landing page.” | `webdesign-excellence`; reuse the supplied brief and tokens; do not load both. |
| Both available: “Fix the chart labels and mobile layout.” | `webdesign-excellence`; preserve metrics and data definitions. |
| Both available: “Rewrite our positioning and plan search-oriented pages.” | `design-ui-excellence`, `content-and-seo`; no automatic visual implementation. |
| Both available: “Define reusable semantic tokens and component rules.” | `design-ui-excellence`, `design-system`; distinguish a system from a local styling fix. |
| Both available: “Plan onboarding across account creation, invitation, and setup.” | `design-ui-excellence`, `product-interface` in Plan mode; no automatic build. |
| Both available: “Use design-ui-excellence to implement this homepage.” | Honor explicit selection and use `website`; do not redirect to the default skill. |
| Only this skill available: “Implement this homepage.” | Use `website` locally; no dependency on another skill. |
| Both available: “Plan the brand, then implement the approved website.” | Start here with `brand-direction`; pass approved decisions to `webdesign-excellence` for the build phase without repeated discovery or concurrent full-library loading. |

## Primary routing cases

The following route cases assume this skill has been selected explicitly or is
used alone. When both skills are available without explicit selection, apply the
selection cases above first.

| Prompt shape | Primary route | Initial companions |
| --- | --- | --- |
| “Build a new multi-page B2B website from this brief.” | `routes/website.md` | brief, structure, style contract |
| “Redesign our homepage but keep the brand and component stack.” | `routes/website.md` | brief, structure, style contract |
| “Create a focused page for traffic from this paid ad.” | `routes/landing-page.md` | positioning, conversion/copy, structure |
| “Improve signup conversion on this pricing page.” | `routes/landing-page.md` | positioning, conversion/copy, structure |
| “Design the admin dashboard and all its empty/error states.” | `routes/product-interface.md` | components/states, visual foundations, accessibility |
| “Fix this settings form and make keyboard navigation work.” | `routes/product-interface.md` | components/states, visual foundations, accessibility |
| “Create a launch campaign across web, email, and social.” | `routes/campaign.md` | positioning, style contract, assets/brand |
| “Develop three possible visual identities from this moodboard.” | `routes/brand-direction.md` | references/originality, style contract, assets/brand |
| “Create semantic color tokens and component specs.” | `routes/design-system.md` | style contract, visual foundations, components/states |
| “Rewrite the website messaging and plan search-oriented pages.” | `routes/content-and-seo.md` | positioning, conversion/copy, structure |
| “Frame the audience, problem, and success criteria before design.” | `routes/research-and-strategy.md` | brief, positioning |
| “Make three genuinely different hero directions.” | `routes/prototype-and-variants.md` | brief, references/originality, variant template |
| “Audit this site and explain why it feels AI-generated. Do not edit.” | `routes/audit-and-polish.md` | anti-generic critique, validation |
| “Review accessibility and fix only release-blocking issues.” | `routes/audit-and-polish.md` | validation, accessibility |
| “Compare our site with these references for originality risk.” | `routes/audit-and-polish.md` | validation, references/originality |

## Precedence cases

| Prompt shape | Expected behavior |
| --- | --- |
| “Research competitors and then build the landing page.” | Start with `landing-page`; load reference research as support. Do not make research the deliverable. |
| “Audit this landing page's conversion and hierarchy.” | Start with `audit-and-polish`; load conversion/copy and visual foundations as domain guides. |
| “Create three dashboard concepts.” | Start with `prototype-and-variants`; use product-interface constraints as the constant baseline. |
| “Create the brand, then build the website.” | Run `brand-direction`, persist the style contract, then reroute to `website`. |
| “Turn the selected prototype into production.” | Leave prototype route, load the production route, integrate, verify, and remove prototype-only code. |
| “Write homepage copy only.” | Use `content-and-seo`, not `website`, unless implementation is also requested. |
| “Build an ecommerce product page.” | Use `website`; add conversion/copy and components/states as needed. |
| “Audit design tokens but do not review product UX.” | Use `design-system` in audit mode, not the general visual audit route. |
| “Study this site so our new brand can learn from it.” | Use `brand-direction` in study mode; extract principles and originality boundaries. |
| “Make this component animation feel better.” | Use `product-interface` for implementation or `audit-and-polish` for review; load motion. |

## Context-budget expectations

A compliant invocation:

1. reads `SKILL.md`
2. loads one primary route
3. loads no more than three initial companions
4. avoids unrelated route files
5. reroutes only when the phase or requested output changes

Examples of incorrect behavior:

- loading every guide for a one-button polish task
- reading website, landing-page, campaign, and product-interface routes simultaneously
- creating persistent brief and style files for a local spacing fix
- treating the audit checklist as permission to redesign
- keeping prototype guidance active after production integration begins
