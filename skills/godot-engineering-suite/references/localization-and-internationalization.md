# Localization and internationalization

Use for translations, locale switching, pluralization, formatting, fonts and RTL layouts.

## Stable source text

Use stable translation keys or the project's established source-text workflow. Do not concatenate translated fragments into sentences. Provide translator context for ambiguous strings, variables and UI constraints.

Use the engine's translation APIs and plural support rather than hand-selecting singular/plural forms. Keep gameplay identifiers separate from localized display names.

## Formatting

Locale-sensitive numbers, dates, units and lists need a deliberate formatter. Do not assume decimal separators, word order, capitalization or ASCII digits. Keep placeholders named or documented and validate they remain present in translations.

## Layout

Design for expansion, wrapping, font fallback and right-to-left direction. Use containers rather than fixed label widths. Mirror navigation/layout only where language direction requires it; gameplay coordinates usually should not mirror automatically.

## Fonts

Verify glyph coverage, shaping, fallback order and font licensing. CJK/complex-script/emoji support affects export size and ICU/font data. Test actual representative strings, not only Latin pseudo-localization.

## Runtime locale changes

Refresh cached text, formatted values and layout after locale changes. Do not rebuild unrelated gameplay state. Persist the locale as a user setting and handle removed/unsupported locales.

## Voice and assets

Map localized voice, images and videos through a manifest or resource remap strategy. Define fallback behavior and keep subtitles available independently from voice packs.

## Verification

Run pseudo-localization, longest target strings, RTL, CJK/complex scripts, missing-key fallback and locale switching during active UI. Check line breaks, focus order, input prompts, fonts and export contents.
