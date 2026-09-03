# Design System Route

Use this route for token systems, component libraries, themes, pattern libraries, component specifications, governance, adoption, or audits of an existing design system.

Do not create a broad design system when the task is one page or one component. Extract a system only when decisions genuinely repeat.

## Load now

- [`../guides/style-contract.md`](../guides/style-contract.md)
- [`../guides/visual-foundations.md`](../guides/visual-foundations.md)
- [`../guides/components-and-states.md`](../guides/components-and-states.md)

Load [`../guides/accessibility-and-localization.md`](../guides/accessibility-and-localization.md) for every production system, [`../guides/interaction-and-motion.md`](../guides/interaction-and-motion.md) when behavior is standardized, and [`../guides/validation-and-qa.md`](../guides/validation-and-qa.md) for audits or release.

## 1. Establish scope

Identify:

- products and platforms served
- current libraries and token sources
- teams and ownership
- recurring inconsistencies
- accessibility and localization requirements
- theming or brand needs
- expected adoption path
- what is explicitly out of scope

Decide whether the need is a token layer, a focused component set, a full system, or remediation of an existing system.

## 2. Audit before replacing

Inventory actual usage, not only the design library:

- raw values bypassing tokens
- duplicate components
- incompatible naming
- state and behavior differences
- inaccessible variants
- styling forks
- unsupported themes
- documentation gaps
- high-cost migration areas

Preserve healthy conventions. A redesign of the system must justify migration cost.

## 3. Define foundations semantically

Build tokens by role and relationship:

- background, surface, text, border, action, status, data
- typography roles and scale
- spacing and sizing
- grid and breakpoints
- radius and shape grammar
- elevation and overlays
- motion durations, curves, and reduced-motion behavior
- iconography and imagery
- themes and modes

Separate primitive values from semantic aliases and component tokens when the project needs those layers. Do not add token tiers that have no consumer.

Color documentation must define which foreground/background pairs are valid for text, icons, fills, borders, and focus indicators. A palette alone is insufficient.

## 4. Specify behavior, not just appearance

Each component specification should cover:

- purpose and non-purpose
- anatomy
- variants tied to semantic use
- size and density
- content rules
- interaction states
- keyboard model
- focus management
- accessibility name and announcements
- responsive behavior
- localization and overflow
- loading, error, empty, and permission states
- composition rules
- examples and misuse

Variants should express meaning, hierarchy, or context. Avoid variants created only because a color or radius exists.

## 5. Reuse the platform and proven primitives

Prefer native semantics and accessible primitives. Keep public APIs small. Good defaults should cover the common case without extensive configuration.

Add dependencies only when they reduce behavioral risk or maintenance. Avoid wrapping every primitive in abstraction before real usage proves the need.

## 6. Plan adoption

Define:

- source of truth
- package and versioning boundaries
- contribution and review path
- migration sequence
- compatibility policy
- visual and interaction regression checks
- deprecation policy
- documentation ownership
- success indicators

A design system that teams cannot adopt is a style guide, not infrastructure.

## Deliverable

Provide a scoped system proposal or implementation with an inventory, foundations, component priorities, specifications, migration plan, governance, and verified examples. Report remaining bypasses and unsupported states honestly.
