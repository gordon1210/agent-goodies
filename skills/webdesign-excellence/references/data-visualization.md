# Data visualization: questions, encodings, and trustworthy comparisons

**Load when:** creating, changing, or reviewing a quantitative chart or metric
comparison. Do not load for every dashboard or add charts as decoration.

## Preserve the meaning before choosing the shape

Name the reader's question: compare categories, inspect a trend, understand a
distribution, find a relationship, or look up exact values. Use the supplied data
and metric definitions. Preserve units, denominators, aggregation, filters, time
window, timezone, and business rules. If these are ambiguous, resolve that specific
dependency; a styling task does not authorize redefining revenue or cleaning records.
Keep illustrative data visibly distinct from live results.

## Choose the encoding

| Reader's question | Useful starting point | Decision that matters |
|---|---|---|
| Which category is larger? | Horizontal bars; grouped bars for a few series | Keep labels readable; use a meaningful category order or clearly identified ranking. |
| How did a measure change over time? | Line; columns for separate period totals | Preserve chronological spacing and distinguish observations from interpolated values. |
| How are values distributed? | Histogram, dot plot, or box plot | State bins or explain the summary; do not replace a distribution with its average. |
| Do two measures vary together? | Scatter plot | Label both units; association does not establish causation. |
| What contributes to a total? | Stacked bars or a simple part-to-whole chart | Use a real shared whole; prefer aligned bars when exact component comparison matters. |
| What are the exact values? | Table, optionally beside a chart | Keep precision, units, and sortable relationships; a chart is not always needed. |

Avoid decorative 3D perspective, pictorial area distortions, and gratuitous gauges.
A familiar chart that answers the question is preferable to a novel unreadable one.
Reuse the existing suitable library or renderer; no dependency is required by this
module. Consult [rendering](technique-rendering.md) only if renderer choice is at issue.

## Make scales and comparisons honest

Bars and areas whose length or area encodes magnitude need a zero baseline;
negative bars extend from zero in the opposite direction. This does not force
interval marks or uncertainty bands to zero: their endpoints encode a range.
Do not truncate magnitude encodings to dramatize a difference.
A line or scatter domain may exclude zero when that clarifies variation: show the
actual axis bounds and ticks, and explain a narrowed range when it affects the
interpretation. Never make a cropped line look like a zero-based filled area.

Use a linear scale by default. A log scale can clarify multiplicative differences
across orders of magnitude, but label it explicitly and explain the tick intervals.
An ordinary log scale cannot plot zero or negative values: do not silently drop
them or substitute a small positive number. Choose another representation or resolve
the required treatment against the metric definition.

Comparable panels should use common units, periods, and scales. If independent
domains are necessary for within-series trends, make that difference conspicuous;
do not invite magnitude comparisons between equally tall panels. Prefer separate
aligned charts to unrelated measures on dual axes. Keep series identity stable
across filters and themes. Do not silently clip outliers or reorder time to fit a
preferred story.

## Label context and incomplete evidence

Show a useful title, series names, units, period, and relevant filter or aggregation
near the chart. Distinguish counts from rates, percent from percentage points, and
currency units from compact display suffixes. Make source or last-update information
available when it affects trust. Do not compare an unfinished period to a full one
without identifying that mismatch.

Zero is an observed value; missing is an absent observation. A stale value is a
previous observation with an age, not a new result. Show these states separately
from loading, failure, and an empty filtered set. Leave meaningful gaps in a series;
do not connect missing intervals as if measured. Label any domain-approved estimate
or interpolation. Render supplied uncertainty as a labeled band, interval, or note
and explain its meaning; do not invent confidence bounds, significance, or forecast
certainty. Mark forecasts separately from observations.

## Equivalent access and responsive composition

Use direct labels where practical, with markers, line patterns, or other cues so
color is not the only series identifier. Apply [color](color.md) checks to meaningful
marks and text. Give the chart an accessible name and a concise factual summary;
provide an associated description or semantic data table conveying its essential
values and relationships. A name such as “revenue chart” alone is insufficient.
Keep that alternative synchronized with filtering and current data. Preserve it
when a rendering enhancement fails, and without JavaScript where the delivery
architecture supports that baseline. An inherently JavaScript-dependent application
needs a clear unavailable/failure state, not a mandatory full no-JS replica; follow
[implementation](implementation.md). A table must retain real headers; do not
flatten it into a huge `aria-label`.

Essential values and actions cannot be hover-only. Make details available through
keyboard focus/selection and touch, or an equivalent operable table. Provide named
controls for series toggles, range changes, and any essential zoom or selection;
do not require dragging. Use an established keyboard pattern instead of thousands
of tab stops. Preserve focus on updates; tooltips must be dismissible and must not
obscure their trigger or become the only source of units and context.

Recompose at narrow widths: use fewer labeled ticks without dropping observations,
wrap labels, switch long-category columns to horizontal bars, or use small multiples.
Retain meaningful scales and uncertainty; do not simply shrink text or discard
series. If a wide plot needs a scroll region, make its extent and access discoverable
and retain a readable summary/table. Preserve essential outliers if a documented
display sampling strategy is needed; do not silently change business aggregation.

## Validation

Check rendered values, units, labels, tooltips, and the alternative against retained
input data, including negative and zero values, a missing interval, an outlier, and
an incomplete period where applicable. Test one-point and empty sets, long labels,
filters, stale/error states, and supplied uncertainty. Inspect narrow and wide views,
zoom, keyboard/touch access, color-independent interpretation, and reduced motion
if animated. Confirm the chart and alternative tell the same story. A screenshot
alone does not verify data correctness or interaction.

**Pass:** the reader can answer the intended question without a misleading scale,
invented data, hidden context, or pointer-only access. Report checks actually run.

## Sources

- [Carbon: Chart types](https://carbondesignsystem.com/data-visualization/chart-types/) — Purpose-led chart selection; not a library requirement.
- [ONS: Axes and gridlines](https://service-manual.ons.gov.uk/data-visualisation/guidance/axes-and-gridlines) — Baselines, consistent scales, and nonlinear/dual-axis cautions.
- [ONS: Showing uncertainty in charts](https://service-manual.ons.gov.uk/data-visualisation/guidance/showing-uncertainty-in-charts) — Communicating ranges that affect interpretation; adapt presentation to the supplied statistics.
- [WAI: Complex images](https://www.w3.org/WAI/tutorials/images/complex/) — Short identification and detailed equivalent information for charts.
