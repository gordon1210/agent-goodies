#!/usr/bin/env python3
"""Check an opaque sRGB color pair. This is not a game accessibility audit."""
from __future__ import annotations

import argparse
import json
import math
import re


def parse_color(value: str) -> tuple[float, float, float]:
    """Accept six-digit hex only; reject alpha rather than silently ignoring it."""
    if not re.fullmatch(r"#?[0-9A-Fa-f]{6}", value):
        raise ValueError("Use an opaque six-digit sRGB color, for example #FFFFFF.")
    text = value.removeprefix("#")
    return (int(text[0:2], 16) / 255.0,
            int(text[2:4], 16) / 255.0,
            int(text[4:6], 16) / 255.0)


def luminance(color: tuple[float, float, float]) -> float:
    def linear(channel: float) -> float:
        return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4
    r, g, b = (linear(channel) for channel in color)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(foreground: str, background: str) -> float:
    first = luminance(parse_color(foreground))
    second = luminance(parse_color(background))
    bright, dark = max(first, second), min(first, second)
    return (bright + 0.05) / (dark + 0.05)


def threshold_arg(value: str) -> float:
    try:
        number = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Threshold must be a number between 1 and 21.") from exc
    if not math.isfinite(number) or not 1.0 <= number <= 21.0:
        raise argparse.ArgumentTypeError("Threshold must be a finite number between 1 and 21.")
    return number


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("foreground", help="Opaque six-digit sRGB hex; quote the # in a shell.")
    parser.add_argument("background", help="Opaque six-digit sRGB hex; quote the # in a shell.")
    parser.add_argument("--threshold", type=threshold_arg, default=4.5,
                        help="Diagnostic threshold (default 4.5), not an automatic classification of text size.")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        ratio = contrast_ratio(args.foreground, args.background)
    except ValueError as exc:
        parser.error(str(exc))
    passes = ratio >= args.threshold  # Compare before rounding; near-threshold values matter.
    result = {"foreground": args.foreground, "background": args.background,
              "ratio": ratio, "threshold": args.threshold, "passes_pair_threshold": passes,
              "scope": "Opaque sRGB pair only; not alpha compositing, dynamic-background testing, or certification."}
    if args.as_json:
        print(json.dumps(result, indent=2))
    else:
        print(f"{ratio:.6f}:1 — {'PASS' if passes else 'FAIL'} for the chosen {args.threshold:g}:1 pair threshold")
        print(result["scope"])
    return 0 if passes else 1


if __name__ == "__main__":
    raise SystemExit(main())
