# Technique: page and shared-element transitions

**Load when:** a route or state change benefits from visual continuity.

## Preserve identity, do not delay navigation

Use a shared element when the same object persists across views: a selected artwork,
a product image, or a meaningful container. A full-screen wipe on every navigation
can be slower and less informative than no transition. Retain normal URLs, links,
back/forward behavior, scroll restoration, and route semantics.

Differentiate same-document transitions from cross-document transitions. Support
and requirements differ; check the exact API and target browsers at implementation
time. Do not infer support for every transition feature from the existence of one
method. The fallback is normal successful navigation.

For transitions within an authored scene, see
[choreography](technique-choreography.md) for semantic handoffs and property ownership.

## Implementation decisions

Let the router or page architecture own navigation and data. Wrap only the relevant
visual update; do not wait on an ornamental timeout. Give shared elements stable,
unique transition names while they participate. Handle list duplicates and outgoing/
incoming elements deliberately; name collisions can prevent the expected transition.

Keep the transition region small when a full-page snapshot is unnecessary. Large
images and composited snapshots can increase memory cost. Do not treat a snapshot
as a new accessible control tree. Ensure the actual destination's heading, focus,
and announcements are correct once navigation occurs.

## Interruption and preferences

Rapid navigation, failed data loading, an aborted transition, and back navigation
must converge to the correct page. Clean up stale classes and names. Under reduced
motion, skip large spatial transitions and preserve a direct state change or minimal
feedback. Do not let an animated screenshot obstruct an active control after the
underlying state has changed.

Avoid promising exact continuity when the two views have radically different crops
or object identities. In those cases a short simple transition may be more honest
and visually cleaner than a distorted morph.

**Fallback:** normal navigation or immediate state update with correct focus and
scroll behavior. **Test:** two fast clicks, back/forward, long loading, errors,
reduced motion, duplicate items, missing images, keyboard navigation, and each
supported browser engine.

## Sources

[MDN: View Transition API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API).
