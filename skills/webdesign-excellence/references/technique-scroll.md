# Technique: scroll narratives and persistent context

**Load when:** scroll position should explain a sequence, chapter, relationship, or reading progress.

## Pick the right mechanism

**Triggered:** entering a region starts a finite animation. **Driven:** scroll
progress continuously controls an animation. **Observed state:** the current section
updates navigation. These need different implementations. IntersectionObserver is
a visibility signal, not a frame-by-frame progress engine.

Default to normal document scrolling. A sticky caption beside sequential visual
chapters can preserve context without replacing browser scroll behavior. Keep each
chapter's content in the DOM in meaningful order. A changing decorative side title
must not become the only accessible copy of the chapter.

For multi-phase explanations, establish the beat map and directly seekable state
with [choreography](technique-choreography.md) before connecting scroll progress.

## Implementation sequence

First build a readable vertical story. Add sticky context only when the viewport
has enough space. For active-section state, use a non-zero observation band or a
measured center-distance strategy; define deterministic tie-breaking when several
sections are visible. Account for headers, short final sections, rapid scrolling,
restored scroll positions, and resize. Do not assume a zero-height center band
with -50% margins detects every crossing reliably.

For continuous effects, use supported CSS scroll/view timelines or an existing
animation engine. Guard the exact features and maintain the static baseline:

```css
.story-media { opacity: 1; transform: none; }
@media (prefers-reduced-motion: no-preference) {
  @supports (animation-timeline: view()) and (animation-range: entry 0% cover 30%) {
    .story-media {
      animation: media-arrive 1s linear both;
      animation-timeline: view();
      animation-range: entry 0% cover 30%;
    }
  }
}
@keyframes media-arrive {
  from { opacity: .4; transform: translateY(1rem); }
  to { opacity: 1; transform: none; }
}
```

Use for supporting media, not essential interactive text. Declare timeline settings
after the `animation` shorthand, which resets them. Feature detection is not a
substitute for testing the exact target browsers and scroller configuration.

## Bound the narrative

Pin only when its content fits the available viewport height. Never require several
screens of empty scrolling to reach normal content. Provide direct chapter links
where useful, preserve back/forward behavior, and offset anchors around fixed headers.
Do not use an automatic live region to announce every scroll-driven title change.

**Fallback:** sequential chapters with static headings, useful anchor links, and
no large parallax or mandatory pinning. **Test:** keyboard/page scrolling, direct
anchors, restored history, touch, zoom, short landscape screens, reduced motion,
and screenshots at multiple progress positions.

## Sources

[MDN: Intersection Observer](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API); [MDN: CSS scroll-driven animations](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations); [MDN: animation-timeline](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline); [MDN: position](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/position).
