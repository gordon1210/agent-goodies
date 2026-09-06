"""Tests for local utilities; these are not Godot runtime or agent-quality tests."""
from __future__ import annotations

import argparse
import math
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from contrast import contrast_ratio, parse_color, threshold_arg
from validate_package import markdown_anchors, validate


class ContrastTests(unittest.TestCase):
    def test_black_white(self) -> None:
        self.assertAlmostEqual(contrast_ratio("#000000", "#FFFFFF"), 21.0)

    def test_equal_colors(self) -> None:
        self.assertAlmostEqual(contrast_ratio("#829384", "829384"), 1.0)

    def test_symmetry(self) -> None:
        self.assertAlmostEqual(contrast_ratio("#f0a250", "#143b5f"),
                               contrast_ratio("#143b5f", "#f0a250"))

    def test_near_threshold_uses_real_ratio(self) -> None:
        self.assertGreater(contrast_ratio("#767676", "#FFFFFF"), 4.5)
        self.assertLess(contrast_ratio("#777777", "#FFFFFF"), 4.5)

    def test_rejects_alpha_and_invalid_colors(self) -> None:
        for value in ("#FFF", "#FFFFFF80", "ffffff ", "GGGGGG", "", "#-12345"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_color(value)

    def test_threshold_rejects_nonfinite_out_of_range(self) -> None:
        for value in ("nan", "inf", "0.9", "21.1", "bad"):
            with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError):
                threshold_arg(value)

    def test_threshold_accepts_boundary(self) -> None:
        self.assertEqual(threshold_arg("1"), 1.0)
        self.assertEqual(threshold_arg("21"), 21.0)


class PackageTests(unittest.TestCase):
    def test_current_package(self) -> None:
        errors, stats = validate(ROOT)
        self.assertEqual(errors, [])
        self.assertEqual(stats["evaluation_cases"], 12)
        self.assertGreaterEqual(stats["sources"], 50)

    def test_missing_directory_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            errors, _ = validate(Path(temp) / "missing")
            self.assertTrue(errors)

    def test_explicit_and_heading_anchors(self) -> None:
        anchors = markdown_anchors('<a id="x101"></a>\n## Helpful heading\n')
        self.assertIn("x101", anchors)
        self.assertIn("helpful-heading", anchors)

    def test_broken_link_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / ROOT.name
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns("__pycache__"))
            with (target / "README.md").open("a", encoding="utf-8") as handle:
                handle.write("\n[Missing file](references/not-here.md)\n")
            errors, _ = validate(target)
            self.assertTrue(any("Broken local link" in error for error in errors))

    def test_path_escape_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / ROOT.name
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns("__pycache__"))
            with (target / "README.md").open("a", encoding="utf-8") as handle:
                handle.write("\n[Outside](../outside.md)\n")
            errors, _ = validate(target)
            self.assertTrue(any("escapes package" in error for error in errors))


class MaskMathTests(unittest.TestCase):
    """Analytical scalar checks only. They do not compile or render the shader."""
    @staticmethod
    def coverage(mask: float, reveal: float, softness: float) -> float:
        s = max(softness, 0.001)
        threshold = -s + (1 + 2 * s) * min(1.0, max(0.0, reveal))
        t = min(1.0, max(0.0, (threshold - (mask - s)) / (2 * s)))
        return t * t * (3 - 2 * t)

    def test_endpoints(self) -> None:
        for mask in (0.0, 0.25, 0.5, 0.75, 1.0):
            for softness in (0.0, 0.001, 0.05, 0.2):
                self.assertAlmostEqual(self.coverage(mask, 0.0, softness), 0.0)
                self.assertAlmostEqual(self.coverage(mask, 1.0, softness), 1.0)

    def test_monotonic_finite_bounded(self) -> None:
        for mask in (0.0, 0.25, 0.5, 0.75, 1.0):
            values = [self.coverage(mask, value / 100, 0.05) for value in range(101)]
            self.assertTrue(all(math.isfinite(value) and 0 <= value <= 1 for value in values))
            self.assertEqual(values, sorted(values))


if __name__ == "__main__":
    unittest.main()
