# Technique: texture, halftone, and ghost typography

**Load when:** a chosen art direction needs a restrained material or graphic cue.

## Decide the material

Paper grain, film grain, halftone, dither, and a construction grid are different
visual languages. Select one that belongs to the direction. Add it to an intended
surface or image layer, not as an indiscriminate overlay over text and controls.
Texture is optional; a clean surface can be equally distinctive.

Start with a small prepared tile or image. Compare the design with and without it
at realistic display size. A few percent opacity can be a useful initial experiment,
but the actual pattern, blend mode, colors, and pixel density determine intensity.
No opacity range guarantees good taste or contrast.

## Layering

Place decorative texture behind content, with pointer events disabled and no
accessibility-tree representation. Use isolated local stacking contexts where blend
modes would otherwise affect unrelated surfaces. Avoid huge animated SVG turbulence
filters or full-screen noise that repaints continuously for no information benefit.
Static pre-rendered texture is often more predictable.

Halftone and dither should preserve recognizable subjects. They can be part of an
explicit graphic or retro vocabulary, but rarely belong behind dense reading text.
Check how the pattern compresses and resizes; moire and banding can appear only at
particular scales.

## Ghost type

A large faint word, index, or mark can add compositional structure without another
illustration. Treat it as decorative if it carries no unique information and hide
only that decorative duplicate from assistive technology. If it is meaningful,
render a separate readable label and do not rely on the faded artwork alone.

Do not allow enormous background type to create page overflow, obscure focus, or
compete with the actual heading. Crop the decoration deliberately while preserving
all functional content. Use the brand's own vocabulary, not fake technical numbers.

**Fallback:** remove the decorative layer. The layout, meaning, and interaction
must remain complete. **Test:** text contrast, screenshots at multiple zoom levels,
different pixel densities, low-quality image compression, forced colors, and GPU/paint
cost if a procedural effect is proposed.

**Reject:** the layer is noticeable before the content without that being the
explicit design purpose, or it exists only to make the output look less generated.
