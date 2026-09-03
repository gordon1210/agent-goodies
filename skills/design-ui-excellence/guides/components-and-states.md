# Components, States, Forms & Navigation

Use this guide for product components and any marketing surface with meaningful interaction.

A component is a behavioral contract, not a styled rectangle.

## Choose the right source

Prefer in order:

1. healthy existing component
2. native platform element
3. accessible primitive already used by the project
4. proven library compatible with the stack
5. custom component when behavior is simple or truly unique

Inspect dependencies before adding another library. Do not hand-roll difficult behavior merely to avoid one justified dependency, and do not import a design system for a static section.

## Component contract

Specify:

- purpose and boundaries
- anatomy
- data and content
- semantic element
- variants and sizes
- default behavior
- interaction model
- state model
- keyboard behavior
- focus behavior
- responsive behavior
- localization and overflow
- accessibility name and announcements
- composition constraints
- error and recovery
- analytics when appropriate

Variants should represent semantic differences, not arbitrary visual choices.

## State inventory

Consider:

- default
- hover
- focus-visible
- active/pressed
- selected/current
- disabled
- read-only
- loading
- empty
- validation error
- system error
- success
- permission denied
- stale or partial data
- offline
- destructive pending
- undo
- overflow and long content

Only implement states relevant to the component, but never assume the populated happy path is sufficient.

## Buttons and links

- Use a button for an action.
- Use a link with a real destination for navigation.
- Preserve open-in-new-tab and copy-link behavior for links.
- Keep labels direct and stable.
- Make primary, secondary, and destructive hierarchy clear.
- Avoid disabled states that conceal how to proceed.
- Provide immediate visual feedback without relying on motion alone.
- Keep hit areas adequate for the supported input.

## Forms

- Preserve visible labels.
- Use correct `type`, `name`, `autocomplete`, and `inputmode`.
- Group fields by user intent.
- Keep help and error text associated with the field.
- Focus or summarize errors appropriately after submission.
- Retain entered values after recoverable errors.
- Do not block paste.
- Explain required format before failure when practical.
- Keep destructive or irreversible actions separate from routine submission.

## Navigation

- Show current location.
- Distinguish global, local, utility, and contextual navigation.
- Preserve predictable keyboard order.
- Collapse navigation based on available space and priority, not one assumed device width.
- Avoid hiding primary destinations behind menus merely for visual cleanliness.
- Ensure mobile drawers, popovers, and menus trap or manage focus correctly as their pattern requires.
- Keep action buttons out of navigation when they are not destinations.

## Dialogs and overlays

- Use a dialog only for focused interruption or confirmation.
- Move focus inside, contain it where required, and restore it to the trigger.
- Close through explicit controls and expected keyboard behavior.
- Do not rely on outside-click for critical completion.
- Confirm destructive actions with the named object and consequence.
- Preserve background and scroll behavior intentionally.

## Loading and empty states

Loading corresponds to actual pending work. Choose skeletons, progress, or status based on what is known and how long the operation may take.

Empty states should distinguish:

- first use
- no search results
- active filters
- permission or availability
- error

Orient the user and provide the most relevant next step.

## Avoid cardification

Use a container when grouping, selection, comparison, or elevation has meaning. Use alignment, whitespace, headings, and dividers when they communicate structure more directly.
