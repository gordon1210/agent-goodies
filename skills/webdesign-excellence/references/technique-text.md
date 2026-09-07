# Technique: clipped text, stagger, and kinetic display

**Load when:** a short display phrase genuinely benefits from a reveal or controlled text transformation.

## Keep the sentence intact

Treat text as content first. Use line or word motion for short display copy, not
letter-by-letter animation for paragraphs. The final message must remain selectable,
searchable, readable by assistive technology, and present without JavaScript.

If visual splitting changes the accessible reading, retain one accessible original
and make only its decorative replica hidden from assistive technology. Do not expose
every letter as a separate navigable object. Do not aria-hide a parent containing
real links or controls. Avoid splitting emoji, combining characters, or other
languages with naive character operations.

## Original CSS-only short-heading specimen

```css
.display-clip {
  display: inline-block;
  overflow: clip;
  padding-block: .12em;
}
.display-word { display: inline-block; }
@media (prefers-reduced-motion: no-preference) {
  .display-word {
    animation: word-in 520ms cubic-bezier(.2,.8,.2,1) both;
  }
}
@keyframes word-in {
  from { transform: translateY(105%); }
  to { transform: translateY(0); }
}
```

This illustrates a one-shot entrance for a short, non-interactive display word;
it is not an intersection observer implementation. Keep meaningful spaces between
word spans. Review the padded clip for the actual font's accents and descenders.
Do not animate every heading merely because the utility class exists.

For scroll-triggered text, start with visible markup, enhance only after setup,
and fail open. Recompute line wrappers after fonts or widths change when required.
Prefer no line-splitting dependency when a single wrapper is sufficient.

## Pacing and variants

A brief word stagger can establish reading order. Cap its cumulative delay so the
last word does not wait through a long queue. A rotating phrase needs adequate
reserved space for every variant, a stable accessible message, and a way to stop
ongoing motion when required. Prefer a fixed phrase when the rotation adds no meaning.
Blur is optional and often unnecessary; it is not part of the definition of a
premium reveal. Avoid scrambling or typewriter effects on essential instructions.

**Fallback:** the complete static phrase in normal flow, with no clipping artifacts.
**Test:** long translation, text zoom, font failure, reduced motion, copy/paste,
accessibility tree, fast navigation, and no-JS behavior. The animation should improve
the introduction without becoming the only way to read it.

## Sources

[WAI: Text Spacing](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html); [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/prefers-reduced-motion).
