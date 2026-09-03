# Brief, Design Read & Assumptions

Use this guide to establish enough shared context to make good decisions without turning every task into an interview.

## Minimum viable brief

Capture only what affects the work:

- **Deliverable** — what must exist at the end
- **Audience** — who must understand or use it
- **Outcome** — what should change for that audience or the business
- **Primary action or task** — what matters most in the artifact
- **Context** — traffic source, workflow entry, device, environment, or campaign
- **Inputs** — content, research, code, brand, assets, references
- **Constraints** — technical, brand, legal, accessibility, localization, performance, timeline
- **Protected elements** — behavior, identity, content, or architecture that must remain
- **Definition of done** — observable acceptance conditions
- **Non-goals** — what this work must not expand into

For an existing codebase, inspect before asking. Source code, tokens, assets, nearby copy, and current behavior often answer questions more reliably than a questionnaire.

## Design read

Summarize the task in a compact block:

```yaml
Design read:
  artifact: <site, landing page, dashboard, campaign, component, system, audit>
  mode: <persuade, operate, read, experience>
  change: <greenfield, extension, preserve redesign, overhaul>
  audience: <primary audience and context>
  outcome: <desired result>
  primary-action: <one action or task>
  visual-thesis: <specific direction, not "clean and modern">
  dials:
    variance: <1-10>
    motion: <1-10>
    density: <1-10>
    brand-fidelity: <1-10>
    art-direction: <1-10>
```

The dials are decision variables:

- Higher **variance** permits more asymmetric or unconventional composition.
- Higher **motion** permits a stronger motion narrative, not more animation everywhere.
- Higher **density** reduces spacing and increases simultaneous information.
- Higher **brand fidelity** limits deviation from existing identity.
- Higher **art direction** increases dependence on distinctive assets and composition.

Do not invent numbers ceremonially. Each value must alter the work.

## Clarification policy

Ask one grouped question only when a missing answer:

- materially changes the strategy or architecture
- cannot be found in available project context
- would make proceeding unsafe, misleading, or expensive to reverse

Otherwise make a conservative assumption, label it, and continue.

Useful clarification categories:

- audience or user role
- primary outcome or action
- must-preserve behavior
- actual proof or assets
- supported platforms and viewports
- brand or legal restrictions

Do not ask the user to choose implementation details that the agent can responsibly decide.

## Assumption ledger

Record only material assumptions:

| Assumption | Why it is needed | Risk if wrong | How to verify |
| --- | --- | --- | --- |
| Example | Missing input that blocks a decision | Concrete consequence | User, source, analytics, test |

Resolve assumptions as evidence arrives. Do not let stale assumptions silently become requirements.

## Acceptance gates

Convert subjective requests into observable checks:

| Goal | Evidence | Pass condition |
| --- | --- | --- |
| “Clear” | Five-second comprehension check | Audience, offer/task, and next action are identifiable |
| “Modern” | Design-system and reference review | Current, coherent choices without trend stacking |
| “Responsive” | Rendered viewport checks | No lost content, overflow, or broken hierarchy |
| “Accessible” | Keyboard, semantics, contrast, motion checks | Required flows work through supported access paths |
| “On brand” | Style contract and asset comparison | Protected assets and defining system choices remain consistent |

Prefer pass/fail evidence to arbitrary scores.

## Output discipline

For a small task, state the design read and assumptions briefly in the response.

For substantial work, use [`../templates/design-brief.md`](../templates/design-brief.md). Keep the brief focused on decisions; do not pad it with generic design-process prose.
