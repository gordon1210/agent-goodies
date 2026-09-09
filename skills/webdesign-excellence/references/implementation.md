# Implementation in the existing stack

**Load when:** turning the design into code or changing interactive behavior.

## Inspect first

Read the relevant components, styles, tokens, route structure, package manifest,
lockfile, and project instructions. Reuse installed primitives and accessible UI
patterns. Do not migrate frameworks, replace the styling system, regenerate lockfiles,
or add an animation engine for a local visual improvement.

Keep domain behavior, validation, analytics contracts, and accessibility intact.
Separate visual tokens from business state. Establish a small component vocabulary
rather than either one enormous page component or a wrapper component for every span.
Use semantic HTML, typed interfaces, and existing lint conventions. Avoid `any` and
unsafe type assertions; use proper narrowing when runtime values need validation.

## Technology ladder

Use HTML/CSS for layout and state styling. Use CSS transitions or WAAPI for small
motion where appropriate. Reuse an installed animation library for complex state or
layout coordination. Add a new dependency only after explaining the missing capability,
actual bundle cost, lifecycle requirements, and fallback. Do not stack engines that
compete for the same element's transform or scroll ownership.

Native CSS is not automatically performant, and JavaScript is not automatically slow.
Verify current syntax and support for the exact feature: basic container size queries,
scroll-state queries, view timelines, and view transitions are not one feature with
one support status. Prefer a robust base plus enhancement over a fragile universal claim.

## Lifecycle and state

For SSR or hydration, do not render random coordinates or client-only viewport values
into server markup. Keep the initial static design deterministic. Scope listeners,
observers, animation contexts, and timers; clean them up on unmount and media changes.
Avoid component state updates for every pointer or scroll frame when refs, CSS variables,
or library motion values can drive the visual layer. Honor document visibility.

Keep content visible in base markup. An enhancement failure must not leave the whole
page at opacity zero. Handle font loading, image decoding, resize, restored scroll,
interrupted transitions, and back navigation. Functional content should not depend
on a canvas renderer. If a product inherently needs JavaScript, offer a clear usable
failure state rather than claiming an impossible full no-JS replica.

Use [choreography](technique-choreography.md) for coordinated playback ownership and
repeatable sampling, or [3D production](technique-3d-production.md) for scene resource
lifetimes. These specialized routes extend the shared lifecycle rules above.

## Stack-specific checks, only when selected

Motion's reduced-motion configuration does not make every media or opacity effect
appropriate; inspect those explicitly. With GSAP, use the installed API and matchMedia
cleanup model; do not copy obsolete snippets from an old demo. React is not required
by this skill. CSS examples are patterns to adapt, not a scaffold mandate.

**Exit:** minimal scoped implementation, no new unexplained dependencies, correct
states, cleanup verified, and browser limitations recorded.

## Sources

[Motion: Accessibility](https://motion.dev/docs/react-accessibility); [GSAP: matchMedia](https://gsap.com/docs/v3/GSAP/gsap.matchMedia%28%29/); [MDN: animation-timeline](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline).
