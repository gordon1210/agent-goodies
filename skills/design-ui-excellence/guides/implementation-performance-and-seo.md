# Implementation, Responsive Engineering, Performance & SEO

Use this guide when design decisions become production code or when auditing technical delivery.

## Fit the existing stack

Before implementation, inspect:

- framework and rendering model
- route and content architecture
- styling system
- component library
- motion library
- tokens
- image and font pipeline
- testing and linting conventions
- browser support
- analytics, privacy, and deployment constraints

Extend healthy conventions. Do not rewrite the stack, add a second styling system, or introduce a dependency merely because a reference implementation uses it.

When exact framework behavior or current best practice matters, verify it against primary documentation.

## Build semantic structure first

- Use meaningful HTML landmarks and controls.
- Keep content order valid without CSS positioning.
- Use progressive enhancement where it improves resilience.
- Preserve real link URLs and browser navigation behavior.
- Avoid client-side JavaScript for behavior the platform already provides well.
- Keep visual components separate from domain and data behavior where that boundary helps maintenance.
- Do not abstract one-off layout before repetition exists.

## Responsive engineering

Design against content and available space:

- intrinsic sizing and wrapping
- flexible grid and container rules
- explicit minimums and maximums
- stable media aspect ratios
- long-content fixtures
- navigation adaptation
- table and data-density strategy
- touch versus pointer behavior
- safe areas and virtual keyboard where relevant

Test a continuum of widths, not only named devices. Never use global overflow hiding to conceal a broken layout.

## Performance

Prioritize:

- stable layout
- responsive interaction
- fast meaningful content
- restrained JavaScript
- efficient images
- intentional font loading
- isolated animation work
- cacheable static assets
- sensible third-party scripts

Review:

- image dimensions, formats, responsive sources, and loading priority
- font subsets, weights, fallback metrics, and preload decisions
- hydration and client-component boundaries
- bundle and dependency cost
- repeated renders and expensive effects
- large DOM and virtualized data where needed
- layout shifts from media, fonts, embeds, and late content
- network behavior under slower conditions

Measure representative pages and flows. Do not claim performance from source inspection alone.

## SEO and discovery

For indexable pages:

- unique, descriptive title and primary heading
- concise description aligned with visible content
- canonical and robots behavior
- meaningful URL
- navigable internal links
- crawlable primary content
- correct language and alternate-language signals when used
- social metadata and usable share image
- structured data only for visible, factual entities and content
- sitemap and update behavior when the site requires them

Search optimization begins with satisfying a real intent. Avoid keyword stuffing, duplicate doorway pages, hidden text, or schema that overstates the page.

Campaign, private, duplicate, and temporary pages need deliberate indexing decisions.

## Privacy and safety

- Collect only necessary form and analytics data.
- Do not leak secrets or personal data into client bundles, screenshots, examples, logs, or analytics.
- Respect project consent and retention requirements.
- Sanitize or encode untrusted content according to the stack.
- Use safe link, embed, and upload behavior.
- Do not install or run code from reference material without authorization.

## Engineering verification

Run the project's applicable:

- formatter
- linter
- type checker
- unit or component tests
- production build
- browser or end-to-end checks
- accessibility checks
- performance measurement
- link and metadata validation

Report commands and outcomes. Do not broaden unrelated refactors while fixing design work.
