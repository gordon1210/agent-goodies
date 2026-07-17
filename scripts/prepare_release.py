#!/usr/bin/env python3
"""Check and prepare metadata for the manual GitHub release workflow."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from validate_repo import NAME_RE, ROOT, SEMVER_RE, Validator, extract_changelog_entry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("plugin", help="lowercase kebab-case plugin name")
    parser.add_argument("version", help="semantic version already present in both manifests")
    parser.add_argument("--github-output", type=Path)
    parser.add_argument("--notes-file", type=Path)
    return parser.parse_args()


def fail(message: str) -> int:
    print(f"Release preparation failed: {message}", file=sys.stderr)
    return 1


def main() -> int:
    args = parse_args()
    if not NAME_RE.fullmatch(args.plugin):
        return fail("plugin must be lowercase kebab-case")
    if not SEMVER_RE.fullmatch(args.version):
        return fail("version must use strict semantic versioning")

    errors = Validator().run()
    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    plugin_dir = ROOT / "plugins" / args.plugin
    if not plugin_dir.is_dir():
        return fail(f"unknown plugin: {args.plugin}")

    manifests = (
        plugin_dir / ".codex-plugin/plugin.json",
        plugin_dir / ".claude-plugin/plugin.json",
    )
    found_versions: list[str] = []
    for path in manifests:
        if path.is_file():
            data = json.loads(path.read_text(encoding="utf-8"))
            found_versions.append(data.get("version", ""))
    if not found_versions or any(version != args.version for version in found_versions):
        return fail("requested version does not match every host manifest")

    notes = extract_changelog_entry(plugin_dir, args.version)
    if notes is None:
        return fail("the changelog has no non-empty entry for this version")

    tag = f"{args.plugin}--v{args.version}"
    tag_check = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", f"refs/tags/{tag}"],
        cwd=ROOT,
        check=False,
    )
    if tag_check.returncode == 0:
        return fail(f"tag already exists: {tag}")
    if tag_check.returncode not in (0, 1):
        return fail("could not inspect existing git tags")

    codex_manifest = json.loads(manifests[0].read_text(encoding="utf-8"))
    title_name = codex_manifest.get("interface", {}).get("displayName", args.plugin)
    title = f"{title_name} v{args.version}".replace("\n", " ")

    if args.notes_file:
        args.notes_file.parent.mkdir(parents=True, exist_ok=True)
        args.notes_file.write_text(notes + "\n", encoding="utf-8")
    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as output:
            output.write(f"tag={tag}\n")
            output.write(f"title={title}\n")

    print(f"Release ready: {tag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
