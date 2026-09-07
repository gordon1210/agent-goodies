# Design & UI Excellence

A single routed agent skill for website creation, marketing strategy, conversion work, digital product design, visual direction, design systems, content, prototyping, and critique.

It is designed for progressive disclosure: the root `SKILL.md` selects one primary route, and that route loads only the small set of specialist guides needed for the current phase. The full library does not need to enter the context window.

## Choosing a design skill

When both this skill and `webdesign-excellence` are available, use this skill for
strategy, messaging and SEO, content architecture, campaigns, brand and design
systems, and UX planning across screens. Use `webdesign-excellence` for concrete
web pages, components, charts, and visual refinement.

An explicit skill choice takes precedence. This skill retains its page and product
routes for standalone use and explicit selection; it does not require the other
package. Mixed projects can hand off the brief, content, constraints, and decisions
between phases without loading both workflows or restarting discovery.

## What it covers

- Greenfield websites and existing-site redesigns
- Landing pages, pricing pages, signup flows, and conversion work
- Product interfaces, dashboards, forms, onboarding, and data views
- Campaign systems and product launches
- Brand direction, visual language, assets, and reference studies
- Design systems, components, tokens, themes, and governance
- Messaging, UX writing, content architecture, and SEO
- Research, briefs, audience framing, and competitive context
- Divergent prototypes and design variants
- Visual, UX, accessibility, originality, and implementation audits

## Structure

```text
design-ui-excellence/
├── SKILL.md                  # Small dispatcher and shared quality contract
├── agents/openai.yaml        # OpenAI agent metadata
├── routes/                   # One primary workflow per deliverable
├── guides/                   # Focused knowledge loaded only when needed
├── templates/                # Optional persistent project artifacts
├── ROUTING_TESTS.md          # Example prompts and expected routing
├── SOURCES.md                # Upstream research and attribution
└── LICENSE
```

## Usage

Copy the complete folder into the skills directory configured for your agent. Invoke `design-ui-excellence` explicitly, or allow implicit invocation when the agent supports it.

Examples:

```text
Use design-ui-excellence to redesign this B2B homepage.
Preserve the current brand and implementation stack, but fix the hierarchy,
message clarity, responsiveness, and generic AI-generated feel.
```

```text
Use design-ui-excellence to create three genuinely different
hero concepts for this launch. Keep the offer and copy constant so the
comparison tests composition and art direction rather than wording.
```

```text
Use design-ui-excellence in audit mode. Review the rendered
application and source, rank only consequential findings, and do not edit.
```

## Routing model

The dispatcher chooses the route from the requested output, then follows that route's own loading instructions.

Typical chains:

```text
research-and-strategy → brand-direction → website → audit-and-polish
landing-page → audit-and-polish
design-system → product-interface → audit-and-polish
prototype-and-variants → selected production route
```

Routes are sequential phases, not files to load all at once.

## Design philosophy

A modern result is not a collection of current visual trends. It is a specific response to a specific audience, product, context, and task. The skill therefore prioritizes:

- intent and content before styling
- coherent direction before component volume
- real evidence before decorative claims
- reference intelligence without imitation
- complete states and accessible behavior
- restraint, hierarchy, and brand specificity
- rendered verification instead of self-assessment

## Customization

The values in the guides are decision frameworks, not a house style. Project-specific brand rules and the user's explicit direction take precedence.

To add a specialized workflow, create one route with a precise trigger boundary and reference existing guides. Add a new guide only when its knowledge cannot live cleanly in an existing file. Update `ROUTING_TESTS.md` whenever routing behavior changes.
