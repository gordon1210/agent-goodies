# Typography as an adaptive system

**Load when:** selecting fonts, shaping hierarchy, correcting wrapping, or using display type.

## Assign roles, not a compulsory font count

Define display, reading, interface, and metadata roles. One well-chosen family can
cover all four. Add another family only for useful contrast. A third font needs a
specific job and a justified loading cost. Mono is useful for aligned identifiers
or genuine technical data; it is not a mandatory sign of sophistication.

Inspect x-height, width, weight, numerals, punctuation, and language coverage with
actual copy. Avoid copying a font name from a reference when the licensed asset is
unavailable. A similar category does not guarantee equivalent metrics.

## Practical starting ranges — heuristics, not accessibility requirements

Body text often starts around 1–1.125rem, with a 1.45–1.7 line height and a reading
measure near 45–75 characters. Dense product UI and other scripts may need different
values. Display text can be tighter, but test accents, descenders, localization, and
user overrides. Negative tracking is a font-specific decision, not a global reset.

```css
.page-title {
  font-size: clamp(2.75rem, 1.7rem + 4.8vw, 7.25rem);
  line-height: 1.02;
  letter-spacing: -0.035em;
  max-inline-size: 14ch;
  text-wrap: balance;
}
.prose {
  max-inline-size: 66ch;
  font-size: 1.0625rem;
  line-height: 1.65;
}
.metrics {
  font-variant-numeric: tabular-nums;
}
```

This is an original layout specimen, not a default theme. `clamp()` with relative
units still needs zoom testing; a viewport term can limit apparent growth. Prefer
rem-based body and control text. Do not shrink all text to preserve a desktop layout.
Balance short headings where supported; retain natural wrapping as fallback. Avoid
manual line breaks unless intentional at the tested widths and language variants.

## Fine control

Use actual font weights rather than browser-synthesized styles. Variable fonts with
an optical-size axis can use `font-optical-sizing: auto`; the declaration does not
create an axis in a font that lacks one. Keep selectable text as text. Decorative
outline or ghost lettering must not be the only representation of meaningful copy.

Reserve enough block space for font changes, labels, validation messages, and long
names. Do not add fixed text heights to make a screenshot look aligned. Measure
font swaps and loading behavior using the asset/performance modules when relevant.

**Checks:** loaded and fallback fonts; short and long strings; 200% text enlargement;
320 CSS pixel reflow; text-spacing overrides. User spacing must not clip or overlap:
1.5 line height, 2em paragraph spacing, .12em letter spacing, .16em word spacing are
override test values, not a requirement to author every page with those defaults.

## Sources

[Carbon: Typography style strategies](https://carbondesignsystem.com/elements/typography/style-strategies/); [MDN: font-optical-sizing](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-optical-sizing); [MDN: text-wrap](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-wrap); [WAI: Text Spacing](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html).
