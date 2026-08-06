from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from types import ModuleType


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "prepare_release.py"


def load_prepare_release() -> ModuleType:
    # prepare_release imports validate_repo from the same scripts/ directory.
    scripts_dir = str(SCRIPT.parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    spec = importlib.util.spec_from_file_location("prepare_release_under_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


PREPARE = load_prepare_release()


class ReleaseTitleNameTests(unittest.TestCase):
    def test_prefers_codex_interface_display_name(self) -> None:
        manifests = [
            {"interface": {"displayName": "Codex Title"}},
            {"displayName": "Claude Title"},
        ]
        self.assertEqual(PREPARE.release_title_name(manifests, "fallback"), "Codex Title")

    def test_claude_only_uses_top_level_display_name(self) -> None:
        manifests = [{"displayName": "Claude Only", "version": "1.0.0"}]
        self.assertEqual(PREPARE.release_title_name(manifests, "fallback"), "Claude Only")

    def test_falls_back_to_plugin_name(self) -> None:
        self.assertEqual(PREPARE.release_title_name([{}], "my-plugin"), "my-plugin")
        self.assertEqual(
            PREPARE.release_title_name([{"displayName": "  "}], "my-plugin"),
            "my-plugin",
        )


if __name__ == "__main__":
    unittest.main()
