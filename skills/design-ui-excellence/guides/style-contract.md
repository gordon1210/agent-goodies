# Visual Direction & Style Contract

Use this guide to convert a brief, references, and existing brand into a coherent system that can survive multiple pages, screens, and contributors.

A style contract prevents drift. It is not a generic design-system essay.

## Establish the thesis

Write one sentence that links the design to the audience and outcome:

```text
The experience should feel <specific qualities> because <audience/context>,
expressed through <observable composition, type, asset, and motion choices>.
```

Avoid empty descriptors such as `clean`, `modern`, `premium`, or `bold` unless each is translated into decisions.

## Source precedence

1. explicit current user direction
2. established project and brand rules
3. resolved project decisions
4. observed references and product context
5. general defaults

Do not silently replace an existing direction because another style is fashionable.

## Contract sections

Record only fields that matter:

### Direction

- thesis
- experience mode
- audience and context
- visual dials
- signature moment
- major risk

### Palette

- semantic roles
- light/dark strategy
- valid text, icon, fill, border, and focus pairings
- status and data-color behavior
- prohibited combinations

A list of hex values is not a color system. Document relationships and verify them in actual use.

### Typography

- families and fallbacks
- role mapping
- scale and line-height logic
- measure and wrapping
- numeric/data treatment
- supported scripts
- loading strategy

### Shape and surface

- radius grammar
- borders versus elevation
- surface hierarchy
- overlay behavior
- image treatment

### Spacing and layout

- base rhythm
- density
- container and grid
- section spacing
- component padding
- breakpoint or content-driven reflow rules

### Assets

- logo and lockups
- anchor imagery
- photography or illustration treatment
- icon family and stroke/fill behavior
- provenance and unresolved gaps

### Motion

- purpose and personality
- duration and easing tokens
- high-frequency exceptions
- spatial origin
- reduced-motion behavior
- signature sequence, if any

### Content

- voice
- terminology
- headline behavior
- CTA conventions
- data and proof rules

### Do / do not

List specific project choices, not universal taste advice.

## Establish from an existing project

Extract tokens and recurring behavior from source before changing values. Distinguish:

- deliberate system
- legacy inconsistency
- one-off exception
- implementation bug

Preserve recognizable assets and healthy patterns. Consolidate only where the new contract clearly improves coherence.

## Establish from references

Trace each major choice to:

- user-supplied direction
- observable reference principle
- product/audience need
- technical requirement

Do not import a token merely because it exists in the reference. The new system needs its own meaning.

## Use and change

For one-off work, keep the contract concise in the response.

For multi-surface work, persist it using [`../templates/style-contract.md`](../templates/style-contract.md).

When the user changes direction:

1. update the thesis
2. identify affected contract sections
3. update representative components first
4. verify contrast, content fit, and responsive behavior again
5. avoid leaving two visual systems active
