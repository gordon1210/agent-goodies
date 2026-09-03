# Product Interface Route

Use this route for dashboards, SaaS products, internal tools, settings, onboarding, editors, forms, search, tables, data views, and task-oriented application screens.

Do not style operational UI like a cinematic marketing page. Repeated work rewards clarity, density, predictability, and speed.

## Load now

- [`../guides/components-and-states.md`](../guides/components-and-states.md)
- [`../guides/visual-foundations.md`](../guides/visual-foundations.md)
- [`../guides/accessibility-and-localization.md`](../guides/accessibility-and-localization.md)

Load [`../guides/interaction-and-motion.md`](../guides/interaction-and-motion.md) when behavior, transition, or gesture design is material, [`../guides/brief.md`](../guides/brief.md) for a new workflow, and [`../guides/validation-and-qa.md`](../guides/validation-and-qa.md) before delivery.

## 1. Model the work

Identify:

- user role and permission level
- primary job and frequency
- entry conditions
- required information
- decisions and actions
- system states and transitions
- failure and recovery paths
- completion and return behavior

For complex components or flows, write the state model before styling. A polished happy path does not compensate for missing states.

## 2. Respect the product system

Inspect the existing component library, tokens, density, interaction patterns, keyboard behavior, data conventions, and terminology.

Prefer:

1. existing healthy components
2. established accessible primitives already in the stack
3. a proven dependency that solves difficult behavior
4. custom implementation for simple or truly unique needs

Do not import a second UI system for one component. Do not hand-roll complex focus management, selection, virtualization, or drag behavior when the project already has a suitable primitive.

## 3. Design hierarchy for scanning and action

- Keep the primary task obvious.
- Use stable alignment for comparable values.
- Preserve useful density; whitespace is not automatically quality.
- Separate navigation, context, content, status, and actions.
- Reserve strong color and contrast for decisions or state.
- Show units, timestamps, data freshness, filters, and scope where they affect interpretation.
- Use cards only when they express grouping, selection, or elevation.

Data visualization must make comparison and meaning easier. Avoid effects that distort scale or obscure labels. Provide a text or tabular alternative when the chart alone is insufficient.

## 4. Cover the state space

Include the relevant states:

- initial and populated
- hover, focus, active, selected
- loading and incremental loading
- empty and filtered-empty
- validation and submission error
- partial failure and stale data
- offline or unavailable
- disabled and read-only
- permission denied
- destructive confirmation and undo
- overflow, long text, large numbers, and many items

Loading indicators must correspond to real asynchronous work. Never simulate loading merely to make the interface feel active.

## 5. Write operational copy

Use existing product vocabulary. Keep routine actions neutral and direct. Make destructive, security, and data-loss consequences explicit. Error messages should explain recovery close to the failure.

Buttons name actions; links name destinations. Do not vary terminology for style.

## 6. Use motion as feedback

Animate state and spatial relationships only where it improves understanding. High-frequency and keyboard-driven operations should be instant or near-instant. Preserve static cues so motion is never the sole carrier of state.

## 7. Verify the workflow

Walk the task with:

- keyboard only
- pointer or touch as applicable
- representative permissions
- empty, loading, error, and large-data conditions
- narrow and wide viewports
- zoom and text expansion
- reduced motion
- slow or failed network when relevant

Confirm that focus moves and returns predictably, actions cannot fire accidentally, and recovery does not require starting over.
