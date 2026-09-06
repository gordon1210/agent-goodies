# Visual validation: test what is displayed, not what the code intended

## Reproducible evidence

Record engine version, renderer, OS/device, exact scene, viewport/window size,
UI scale, language, input method, fixture/scenario, and capture path. Use a
repeatable scenario with deterministic data where possible. Mark fixture data and
concept renders as such. Never fabricate a screenshot or describe an unseen scene.

A syntax check or headless import check is useful engineering evidence but cannot
prove the final visual result. To inspect the rendered viewport through code, use
the engine's supported capture path at the appropriate rendered-frame boundary;
verify the viewport is valid and rendering. Do not claim headless black output is
a successful visual regression test.

## A proportional matrix

For a desktop project, a proposed starting matrix is 1920×1080, 2560×1440,
3840×2160, a 16:10 target, and a 21:9 target. Replace or reduce this with the actual
supported devices; it is not a requirement to target every resolution. Include the
smallest supported output and largest agreed text/UI scale.

Capture normal, focused, hovered, selected+focused, unavailable, long-content,
error, modal, and missing-asset/loading cases where relevant. Test both bright and
dark/busy game backgrounds. A screen with empty placeholder rows is not a density test.

## Inspect in three passes

1. **Composition:** full frame, then thumbnail/grayscale diagnostics. Identify the
   first decision, competing focal points, lost world context, and generic layout.
2. **Craft:** actual playing size and targeted crops. Inspect typography, alignment,
   borders, icon consistency, alpha halos, texture scaling, and state distinctions.
3. **Behavior:** real input and a recording. Check focus, press/release, interruption,
   reflow, time scale, back-stack ownership, data updates, and stale operations.

Compare against the approved target at matched scale and representative content.
A visual difference is not automatically a defect; localization and platform
adaptation may require intentional changes. Pixel diffs can help with stable
fixtures, but animation, fonts, and renderer differences need controlled conditions
and human/agent visual judgment rather than a universal numeric threshold.

## Task-based checks

Execute the actual player tasks in the screen contract. Include rapid confirm/back,
input-device switching, reopening, nested dialogs, and invalidated data. Test the
reduced-motion path separately. Confirm required information and actions remain
available after resizing or changing text size.

## Report evidence, then conclusions

Use the [review template](../assets/visual-review.md). List observed issues with
location, reproduction, consequence, and proposed correction. Prioritize the next
few meaningful changes; avoid an unbounded "polish everything" loop. Mark each
acceptance axis passed, failed, or not tested with evidence.

No access to images means no final visual approval. No controller means controller
behavior is untested, even if the code looks plausible. Deliver useful work with
those limits stated rather than inventing validation.

## Evidence anchors

[G21](sources.md#g21) · [X101](sources.md#x101) · [X112](sources.md#x112) · [X113](sources.md#x113)

The application recipes above are original synthesis, not quotations or measured specifications of the referenced games.
