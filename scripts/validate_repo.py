#!/usr/bin/env python3
"""Validate the portable plugin marketplace without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
CHANGELOG_HEADING_RE = re.compile(
    r"^## \[([^]]+)] - (\d{4}-\d{2}-\d{2})$", re.MULTILINE
)
MARKDOWN_LINK_RE = re.compile(r"!?\[[^]]*]\(([^)]+)\)")
REQUIRED_PUBLIC_METADATA = (
    "description",
    "homepage",
    "repository",
    "license",
    "keywords",
)


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


class Validator:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self._json_cache: dict[Path, Any] = {}
        self.cataloged_plugins: set[str] = set()

    def error(self, path: Path, message: str) -> None:
        self.errors.append(f"{display_path(path)}: {message}")

    def require(self, condition: bool, path: Path, message: str) -> None:
        if not condition:
            self.error(path, message)

    def load_json(self, path: Path) -> Any | None:
        if path in self._json_cache:
            return self._json_cache[path]
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            self.error(path, f"invalid JSON: {exc}")
            return None
        self._json_cache[path] = value
        return value

    def validate_all_json(self) -> None:
        for path in sorted(ROOT.rglob("*.json")):
            if ".git" not in path.parts:
                self.load_json(path)

    def resolve_plugin_source(self, path: Path, source: str) -> Path | None:
        if not source.startswith("./"):
            self.error(path, "marketplace source must start with './'")
            return None
        target = (ROOT / source[2:]).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            self.error(path, "marketplace source escapes the repository")
            return None
        if not target.is_dir():
            self.error(path, f"marketplace source does not exist: {source}")
            return None
        return target

    def validate_codex_marketplace(self) -> None:
        path = ROOT / ".agents/plugins/marketplace.json"
        data = self.load_json(path)
        if not isinstance(data, dict):
            self.error(path, "marketplace root must be an object")
            return
        self.require(bool(data.get("name")), path, "missing marketplace name")
        plugins = data.get("plugins")
        if not isinstance(plugins, list):
            self.error(path, "plugins must be an array")
            return

        seen: set[str] = set()
        for index, entry in enumerate(plugins):
            label = f"plugins[{index}]"
            if not isinstance(entry, dict):
                self.error(path, f"{label} must be an object")
                continue
            name = entry.get("name")
            if not isinstance(name, str) or not NAME_RE.fullmatch(name):
                self.error(path, f"{label}.name must be lowercase kebab-case")
                continue
            self.require(name not in seen, path, f"duplicate Codex plugin entry: {name}")
            seen.add(name)
            self.cataloged_plugins.add(name)

            source = entry.get("source")
            if not isinstance(source, dict):
                self.error(path, f"{label}.source must be an object")
                continue
            self.require(
                source.get("source") == "local",
                path,
                f"{label}.source.source must be 'local'",
            )
            source_path = source.get("path")
            if not isinstance(source_path, str):
                self.error(path, f"{label}.source.path must be a string")
                continue
            plugin_dir = self.resolve_plugin_source(path, source_path)
            if plugin_dir is not None:
                self.require(
                    plugin_dir.name == name,
                    path,
                    f"{label} name does not match source directory",
                )
                manifest_path = plugin_dir / ".codex-plugin/plugin.json"
                self.require(
                    manifest_path.is_file(),
                    path,
                    f"{label} points to a plugin without a Codex manifest",
                )

            policy = entry.get("policy")
            if not isinstance(policy, dict):
                self.error(path, f"{label}.policy must be an object")
            else:
                self.require(
                    policy.get("installation")
                    in {"NOT_AVAILABLE", "AVAILABLE", "INSTALLED_BY_DEFAULT"},
                    path,
                    f"{label}.policy.installation is invalid",
                )
                self.require(
                    policy.get("authentication") in {"ON_INSTALL", "ON_USE"},
                    path,
                    f"{label}.policy.authentication is invalid",
                )
            self.require(bool(entry.get("category")), path, f"{label} needs a category")

    def validate_claude_marketplace(self) -> None:
        path = ROOT / ".claude-plugin/marketplace.json"
        data = self.load_json(path)
        if not isinstance(data, dict):
            self.error(path, "marketplace root must be an object")
            return
        self.require(bool(data.get("name")), path, "missing marketplace name")
        plugins = data.get("plugins")
        if not isinstance(plugins, list):
            self.error(path, "plugins must be an array")
            return

        seen: set[str] = set()
        for index, entry in enumerate(plugins):
            label = f"plugins[{index}]"
            if not isinstance(entry, dict):
                self.error(path, f"{label} must be an object")
                continue
            name = entry.get("name")
            if not isinstance(name, str) or not NAME_RE.fullmatch(name):
                self.error(path, f"{label}.name must be lowercase kebab-case")
                continue
            self.require(name not in seen, path, f"duplicate Claude plugin entry: {name}")
            seen.add(name)
            self.cataloged_plugins.add(name)
            self.require(
                "version" not in entry,
                path,
                f"{label} duplicates the version from plugin.json",
            )

            source = entry.get("source")
            if not isinstance(source, str):
                self.error(path, f"{label}.source must be a relative string")
                continue
            plugin_dir = self.resolve_plugin_source(path, source)
            if plugin_dir is not None:
                self.require(
                    plugin_dir.name == name,
                    path,
                    f"{label} name does not match source directory",
                )
                manifest_path = plugin_dir / ".claude-plugin/plugin.json"
                self.require(
                    manifest_path.is_file(),
                    path,
                    f"{label} points to a plugin without a Claude manifest",
                )

    def validate_manifest_metadata(
        self, path: Path, data: dict[str, Any], plugin_name: str
    ) -> None:
        self.require(data.get("name") == plugin_name, path, "manifest name mismatch")
        version = data.get("version")
        self.require(
            isinstance(version, str) and bool(SEMVER_RE.fullmatch(version)),
            path,
            "version must be strict semantic versioning",
        )
        for key in REQUIRED_PUBLIC_METADATA:
            self.require(bool(data.get(key)), path, f"missing public metadata: {key}")

        author = data.get("author")
        if not isinstance(author, dict):
            self.error(path, "author must be an object")
        else:
            self.require(bool(author.get("name")), path, "author.name is required")
            self.require(
                isinstance(author.get("url"), str)
                and author["url"].startswith("https://"),
                path,
                "author.url must be an HTTPS URL",
            )

        for key in ("homepage", "repository"):
            value = data.get(key)
            self.require(
                isinstance(value, str) and value.startswith("https://"),
                path,
                f"{key} must be an HTTPS URL",
            )
        self.require(data.get("license") == "MIT", path, "license must be MIT")
        keywords = data.get("keywords")
        self.require(
            isinstance(keywords, list)
            and bool(keywords)
            and all(isinstance(item, str) and item for item in keywords),
            path,
            "keywords must be a non-empty string array",
        )

    def validate_skill(self, skill_dir: Path) -> None:
        path = skill_dir / "SKILL.md"
        if not path.is_file():
            self.error(skill_dir, "skill directory is missing SKILL.md")
            return
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            self.error(path, "SKILL.md must start with YAML frontmatter")
            return
        end = text.find("\n---\n", 4)
        if end == -1:
            self.error(path, "SKILL.md frontmatter is not closed")
            return

        fields: dict[str, str] = {}
        for line in text[4:end].splitlines():
            match = re.match(r"^([A-Za-z0-9_-]+):\s*(.+)$", line)
            if match:
                fields[match.group(1)] = match.group(2).strip().strip("'\"")
        name = fields.get("name", "")
        description = fields.get("description", "")
        self.require(name == skill_dir.name, path, "frontmatter name must match directory")
        self.require(bool(NAME_RE.fullmatch(name)), path, "skill name must be kebab-case")
        self.require(len(name) <= 64, path, "skill name must be at most 64 characters")
        self.require(bool(description), path, "frontmatter description is required")
        self.require(
            len(description) <= 1024,
            path,
            "frontmatter description must be at most 1024 characters",
        )

    def validate_markdown_links(self, plugin_dir: Path) -> None:
        plugin_root = plugin_dir.resolve()
        for path in sorted(plugin_dir.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            for match in MARKDOWN_LINK_RE.finditer(text):
                raw_target = match.group(1).strip()
                if raw_target.startswith("<") and raw_target.endswith(">"):
                    raw_target = raw_target[1:-1]
                target = raw_target.split(" ", 1)[0]
                if (
                    not target
                    or target.startswith("#")
                    or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target)
                ):
                    continue
                target = unquote(target.split("#", 1)[0])
                resolved = (path.parent / target).resolve()
                try:
                    resolved.relative_to(plugin_root)
                except ValueError:
                    self.error(path, f"relative link escapes plugin root: {raw_target}")
                    continue
                self.require(
                    resolved.exists(), path, f"broken relative link: {raw_target}"
                )

    def validate_changelog(self, plugin_dir: Path, version: str | None) -> None:
        path = plugin_dir / "CHANGELOG.md"
        if not path.is_file():
            self.error(plugin_dir, "published plugin is missing CHANGELOG.md")
            return
        text = path.read_text(encoding="utf-8")
        versions = [match.group(1) for match in CHANGELOG_HEADING_RE.finditer(text)]
        self.require(bool(versions), path, "changelog has no dated version entries")
        self.require(
            len(versions) == len(set(versions)), path, "changelog versions must be unique"
        )
        for item in versions:
            self.require(
                bool(SEMVER_RE.fullmatch(item)),
                path,
                f"invalid semantic version in changelog: {item}",
            )
        if version:
            self.require(
                version in versions,
                path,
                f"missing changelog entry for manifest version {version}",
            )

    def validate_plugin(self, plugin_dir: Path) -> None:
        name = plugin_dir.name
        self.require(bool(NAME_RE.fullmatch(name)), plugin_dir, "plugin name must be kebab-case")
        self.require(len(name) <= 64, plugin_dir, "plugin name must be at most 64 characters")

        manifests: dict[str, dict[str, Any]] = {}
        for host, relative_path in (
            ("codex", ".codex-plugin/plugin.json"),
            ("claude", ".claude-plugin/plugin.json"),
        ):
            path = plugin_dir / relative_path
            if not path.is_file():
                continue
            data = self.load_json(path)
            if not isinstance(data, dict):
                self.error(path, "manifest root must be an object")
                continue
            manifests[host] = data
            self.validate_manifest_metadata(path, data, name)

        self.require(bool(manifests), plugin_dir, "plugin has no host manifest")
        versions = {
            data.get("version")
            for data in manifests.values()
            if isinstance(data.get("version"), str)
        }
        self.require(
            len(versions) <= 1,
            plugin_dir,
            "Codex and Claude manifest versions do not match",
        )

        codex_data = manifests.get("codex")
        if codex_data is not None:
            path = plugin_dir / ".codex-plugin/plugin.json"
            interface = codex_data.get("interface")
            if not isinstance(interface, dict):
                self.error(path, "Codex manifest requires an interface object")
            else:
                for key in (
                    "displayName",
                    "shortDescription",
                    "longDescription",
                    "developerName",
                    "category",
                    "capabilities",
                    "defaultPrompt",
                ):
                    self.require(
                        bool(interface.get(key)), path, f"interface.{key} is required"
                    )
                prompts = interface.get("defaultPrompt")
                self.require(
                    isinstance(prompts, list)
                    and 1 <= len(prompts) <= 3
                    and all(isinstance(item, str) and len(item) <= 128 for item in prompts),
                    path,
                    "interface.defaultPrompt must contain 1-3 strings of at most 128 characters",
                )

        self.require(
            (plugin_dir / "README.md").is_file(), plugin_dir, "plugin is missing README.md"
        )
        license_path = plugin_dir / "LICENSE"
        self.require(license_path.is_file(), plugin_dir, "plugin is missing LICENSE")
        if license_path.is_file():
            self.require(
                "MIT License" in license_path.read_text(encoding="utf-8"),
                license_path,
                "plugin license is not MIT",
            )

        skills_dir = plugin_dir / "skills"
        self.require(skills_dir.is_dir(), plugin_dir, "plugin is missing skills directory")
        if skills_dir.is_dir():
            skill_dirs = sorted(path for path in skills_dir.iterdir() if path.is_dir())
            self.require(bool(skill_dirs), skills_dir, "plugin has no skills")
            for skill_dir in skill_dirs:
                self.validate_skill(skill_dir)
        self.validate_markdown_links(plugin_dir)
        version = next(iter(versions)) if len(versions) == 1 else None
        self.validate_changelog(plugin_dir, version)

    def run(self) -> list[str]:
        self.validate_all_json()
        self.validate_codex_marketplace()
        self.validate_claude_marketplace()

        plugins_dir = ROOT / "plugins"
        self.require(plugins_dir.is_dir(), plugins_dir, "plugins directory is missing")
        plugin_dirs = (
            sorted(
                path
                for path in plugins_dir.iterdir()
                if path.is_dir()
                and (
                    (path / ".codex-plugin/plugin.json").is_file()
                    or (path / ".claude-plugin/plugin.json").is_file()
                )
            )
            if plugins_dir.is_dir()
            else []
        )
        self.require(bool(plugin_dirs), plugins_dir, "repository has no plugins")
        for plugin_dir in plugin_dirs:
            self.validate_plugin(plugin_dir)
            self.require(
                plugin_dir.name in self.cataloged_plugins,
                plugin_dir,
                "plugin is not exposed by either marketplace",
            )

        self.require((ROOT / "README.md").is_file(), ROOT, "missing README.md")
        self.require((ROOT / "LICENSE").is_file(), ROOT, "missing LICENSE")
        self.require((ROOT / "SECURITY.md").is_file(), ROOT, "missing SECURITY.md")
        self.require((ROOT / "CONTRIBUTING.md").is_file(), ROOT, "missing CONTRIBUTING.md")
        return self.errors


def extract_changelog_entry(plugin_dir: Path, version: str) -> str | None:
    """Return the Markdown body for one version, excluding its heading."""

    path = plugin_dir / "CHANGELOG.md"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    heading = re.compile(
        rf"^## \[{re.escape(version)}] - \d{{4}}-\d{{2}}-\d{{2}}\s*$",
        re.MULTILINE,
    )
    match = heading.search(text)
    if match is None:
        return None
    next_heading = re.search(r"^## \[", text[match.end() :], re.MULTILINE)
    end = match.end() + next_heading.start() if next_heading else len(text)
    body = text[match.end() : end].strip()
    return body or None


def main() -> int:
    errors = Validator().run()
    if errors:
        print(f"Validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    plugin_count = sum(
        1
        for path in (ROOT / "plugins").iterdir()
        if path.is_dir()
        and (
            (path / ".codex-plugin/plugin.json").is_file()
            or (path / ".claude-plugin/plugin.json").is_file()
        )
    )
    print(f"Validated {plugin_count} plugin(s) and both marketplaces.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
