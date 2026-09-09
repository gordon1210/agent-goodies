"""Regression tests for the webdesign package validator.

These tests mutate disposable copies only. They do not invoke a browser,
renderer, model, or network service.
"""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_package import validate  # noqa: E402


class PackageValidatorTests(unittest.TestCase):
    def copy_package(self) -> Path:
        # Keep task-created scratch copies for post-run inspection. Avoid an
        # implicit recursive cleanup that could hide the exact mutation set.
        target = Path(tempfile.mkdtemp(prefix="webdesign-validator-")) / ROOT.name
        shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns("__pycache__"))
        return target

    @staticmethod
    def write_valid_gltf(path: Path, *, uri: str = "data:application/octet-stream;base64,AA==",
                         byte_length: int = 1) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "asset": {"version": "2.0"},
            "buffers": [{"byteLength": byte_length, "uri": uri}],
        }) + "\n", encoding="utf-8")

    def test_current_package_passes_and_contains_new_routes(self) -> None:
        result = validate(ROOT)
        self.assertTrue(result["passed"], result["errors"])
        self.assertEqual(result["techniques"], 18)
        self.assertGreaterEqual(result["example_files"], 1)
        fixture = json.loads((ROOT / "evals" / "routing-cases.json").read_text(encoding="utf-8"))
        ids = {case["id"] for case in fixture["cases"]}
        self.assertTrue({
            "micro-transition-no-library",
            "kinetic-beat-map",
            "explicit-interactive-3d",
            "layered-2-5d-no-webgl",
            "supplied-video-integration",
            "reference-motion-reconstruction",
        } <= ids)

    def test_example_source_allowlist_is_scoped(self) -> None:
        target = self.copy_package()
        example = target / "examples" / "validator-fixture.js"
        example.parent.mkdir(parents=True, exist_ok=True)
        example.write_text("export const fixture = true;\n", encoding="utf-8")
        result = validate(target)
        self.assertTrue(result["passed"], result["errors"])

    def test_example_extension_outside_harness_is_rejected(self) -> None:
        target = self.copy_package()
        path = target / "assets" / "unexpected.js"
        path.write_text("export {};\n", encoding="utf-8")
        result = validate(target)
        self.assertTrue(any("Unexpected file type: assets/unexpected.js" in error
                            for error in result["errors"]))

    def test_example_html_asset_escape_is_rejected(self) -> None:
        target = self.copy_package()
        path = target / "examples" / "escape.html"
        path.write_text('<script src="%2e%2e/%2e%2e/outside.js"></script>\n', encoding="utf-8")
        result = validate(target)
        self.assertTrue(any("local asset reference escapes package" in error
                            for error in result["errors"]))

    def test_gltf_external_and_missing_resources_are_rejected(self) -> None:
        target = self.copy_package()
        external = target / "examples" / "external.gltf"
        self.write_valid_gltf(external, uri="https://assets.example.test/model.bin")
        result = validate(target)
        self.assertTrue(any("uses an external URI" in error for error in result["errors"]))

        # Leave the first malformed copy intact so both rejection fixtures are
        # independently inspectable if a test run fails.
        missing = target / "examples" / "missing.gltf"
        self.write_valid_gltf(missing, uri="assets/not-present.bin")
        result = validate(target)
        self.assertTrue(any("missing GLTF resource" in error for error in result["errors"]))

    def test_gltf_embedded_buffer_integrity_is_checked(self) -> None:
        target = self.copy_package()
        path = target / "examples" / "bad-buffer.gltf"
        self.write_valid_gltf(path, byte_length=2)
        result = validate(target)
        self.assertTrue(any("byteLength does not match embedded data" in error
                            for error in result["errors"]))

    def test_gltf_version_and_base64_are_checked(self) -> None:
        target = self.copy_package()
        path = target / "examples" / "bad-encoding.gltf"
        self.write_valid_gltf(path, uri="data:application/octet-stream;base64,not-base64")
        document = json.loads(path.read_text(encoding="utf-8"))
        document["asset"]["version"] = "1.0"
        path.write_text(json.dumps(document), encoding="utf-8")
        result = validate(target)
        self.assertTrue(any("asset.version must be '2.0'" in error for error in result["errors"]))
        self.assertTrue(any("contains invalid base64" in error for error in result["errors"]))

    def test_vendored_example_tree_is_rejected(self) -> None:
        target = self.copy_package()
        path = target / "examples" / "node_modules" / "three" / "index.js"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("export {};\n", encoding="utf-8")
        result = validate(target)
        self.assertTrue(any("generated/vendor directory" in error
                            for error in result["errors"]))

    def test_symlink_is_rejected(self) -> None:
        target = self.copy_package()
        outside = target.parent / "outside.js"
        outside.write_text("export {};\n", encoding="utf-8")
        link = target / "examples" / "linked.js"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlinks unavailable: {exc}")
        result = validate(target)
        self.assertTrue(any("Symlinks are not part of this distribution" in error
                            for error in result["errors"]))

    def test_malformed_fixture_json_is_reported(self) -> None:
        target = self.copy_package()
        fixture = target / "evals" / "routing-cases.json"
        fixture.write_text('{"schema_version": 1,\n', encoding="utf-8")
        result = validate(target)
        self.assertTrue(any("Evaluation fixture is not valid JSON" in error
                            for error in result["errors"]))

    def test_missing_reference_is_rejected(self) -> None:
        target = self.copy_package()
        (target / "references" / "technique-motion.md").unlink()
        result = validate(target)
        self.assertTrue(any("missing local link target" in error for error in result["errors"]))

    def test_broken_markdown_link_is_rejected(self) -> None:
        target = self.copy_package()
        with (target / "README.md").open("a", encoding="utf-8") as handle:
            handle.write("\n[Missing](references/not-present.md)\n")
        result = validate(target)
        self.assertTrue(any("missing local link target" in error for error in result["errors"]))

    def test_invalid_frontmatter_is_rejected(self) -> None:
        target = self.copy_package()
        skill = target / "SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8").replace("name: webdesign-excellence", "name: Webdesign", 1),
                         encoding="utf-8")
        result = validate(target)
        self.assertTrue(any("Frontmatter does not match" in error for error in result["errors"]))

    def test_unclosed_markdown_fence_is_rejected(self) -> None:
        target = self.copy_package()
        with (target / "README.md").open("a", encoding="utf-8") as handle:
            handle.write("\n```js\nconst incomplete = true;\n")
        result = validate(target)
        self.assertTrue(any("unclosed fenced code block" in error for error in result["errors"]))

    def test_fixture_cannot_route_a_disallowed_style(self) -> None:
        target = self.copy_package()
        fixture_path = target / "evals" / "routing-cases.json"
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        for case in fixture["cases"]:
            if case["id"] == "technical-saas":
                case["allowed_styles"] = ["luxury"]
                break
        fixture_path.write_text(json.dumps(fixture), encoding="utf-8")
        result = validate(target)
        self.assertTrue(any("route imports a disallowed style" in error
                            for error in result["errors"]))

    def test_chat_only_citation_marker_is_rejected(self) -> None:
        target = self.copy_package()
        with (target / "README.md").open("a", encoding="utf-8") as handle:
            handle.write("\nciteturn0search0\n")
        result = validate(target)
        self.assertTrue(any("chat-only citation marker" in error for error in result["errors"]))

    def test_markdown_path_escape_is_rejected(self) -> None:
        target = self.copy_package()
        with (target / "README.md").open("a", encoding="utf-8") as handle:
            handle.write("\n[Outside](../outside.md)\n")
        result = validate(target)
        self.assertTrue(any("local link escapes package" in error for error in result["errors"]))

    def test_unapproved_file_extension_is_rejected(self) -> None:
        target = self.copy_package()
        (target / "artifact.bin").write_bytes(b"fixture")
        result = validate(target)
        self.assertTrue(any("Unexpected file type: artifact.bin" in error
                            for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
