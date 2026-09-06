#!/usr/bin/env python3
"""Produce a compact, read-only inventory of a Godot project.

The script does not launch Godot, import assets, modify files, or access the
network. It intentionally reports high-value project facts rather than dumping
full project settings into an agent context.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

SKIP_DIRECTORIES = {
    ".git",
    ".godot",
    ".idea",
    ".vscode",
    ".vs",
    ".mono",
    "node_modules",
    "bin",
    "obj",
    "build",
    "dist",
}

LANGUAGE_EXTENSIONS = {
    ".gd": "GDScript",
    ".cs": "C#",
    ".gdshader": "Godot Shader",
    ".glsl": "GLSL",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".c": "C",
    ".h": "C/C++ headers",
    ".hpp": "C/C++ headers",
    ".rs": "Rust",
}

CONTENT_EXTENSIONS = {
    ".tscn": "text scenes",
    ".scn": "binary scenes",
    ".tres": "text resources",
    ".res": "binary resources",
    ".gdextension": "GDExtensions",
    ".godot": "project files",
}


@dataclass(frozen=True)
class ProjectInventory:
    project_root: str
    project_name: str | None
    main_scene: str | None
    feature_tags: list[str]
    inferred_engine_branch: str | None
    renderers: list[str]
    languages: dict[str, int]
    content: dict[str, int]
    autoloads: dict[str, str]
    enabled_editor_plugins: list[str]
    addons: list[str]
    gdextensions: list[str]
    export_presets: list[str]
    test_locations: list[str]
    project_profile: str | None
    repository_instructions: list[str]
    warnings: list[str]
    scanned_files: int
    scan_truncated: bool


def find_project_root(start: Path) -> Path:
    candidate = start.expanduser().resolve()
    if candidate.is_file():
        candidate = candidate.parent

    for directory in (candidate, *candidate.parents):
        if (directory / "project.godot").is_file():
            return directory

    raise FileNotFoundError(
        f"No project.godot found at or above {candidate}. Pass --root explicitly."
    )


def decode_quoted_strings(value: str) -> list[str]:
    values: list[str] = []
    for match in re.finditer(r'"(?:\\.|[^"\\])*"', value):
        try:
            decoded = json.loads(match.group(0))
        except json.JSONDecodeError:
            continue
        if isinstance(decoded, str):
            values.append(decoded)
    return values


def extract_scalar(text: str, key: str) -> str | None:
    pattern = rf"(?m)^{re.escape(key)}\s*=\s*(.+?)\s*$"
    match = re.search(pattern, text)
    if not match:
        return None

    raw = match.group(1).strip()
    quoted = decode_quoted_strings(raw)
    if quoted:
        return quoted[0]
    return raw or None


def extract_packed_strings(text: str, key: str) -> list[str]:
    pattern = rf"(?m)^{re.escape(key)}\s*=\s*PackedStringArray\((.*?)\)\s*$"
    match = re.search(pattern, text)
    return decode_quoted_strings(match.group(1)) if match else []


def section_body(text: str, section: str) -> str:
    pattern = rf"(?ms)^\[{re.escape(section)}\]\s*$(.*?)(?=^\[|\Z)"
    match = re.search(pattern, text)
    return match.group(1) if match else ""


def parse_autoloads(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in section_body(text, "autoload").splitlines():
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+?)\s*$", line)
        if not match:
            continue
        values = decode_quoted_strings(match.group(2))
        result[match.group(1)] = values[0] if values else match.group(2).strip()
    return result


def parse_editor_plugins(text: str) -> list[str]:
    body = section_body(text, "editor_plugins")
    match = re.search(r"(?m)^enabled\s*=\s*PackedStringArray\((.*?)\)\s*$", body)
    return sorted(decode_quoted_strings(match.group(1))) if match else []


def infer_engine_branch(features: Iterable[str]) -> str | None:
    candidates = [
        item
        for item in features
        if re.fullmatch(r"\d+\.\d+(?:\.\d+)?", item.strip())
    ]
    if not candidates:
        return None
    # config/features is a compatibility hint, not an exact executable version.
    return candidates[0]


def parse_renderers(text: str, features: Iterable[str]) -> list[str]:
    detected: set[str] = set()
    mappings = {
        "gl_compatibility": "Compatibility",
        "gl compatibility": "Compatibility",
        "compatibility": "Compatibility",
        "mobile": "Mobile",
        "forward_plus": "Forward+",
        "forward plus": "Forward+",
        "forward+": "Forward+",
    }

    configured_values = [
        extract_scalar(text, "renderer/rendering_method"),
        extract_scalar(text, "renderer/rendering_method.mobile"),
        extract_scalar(text, "renderer/rendering_method.web"),
    ]
    for value in [*configured_values, *features]:
        if value is None:
            continue
        normalized = value.strip().lower()
        label = mappings.get(normalized)
        if label:
            detected.add(label)

    return sorted(detected)


def walk_files(root: Path, limit: int) -> tuple[list[Path], bool]:
    files: list[Path] = []
    truncated = False

    for current_root, directories, filenames in os.walk(root, followlinks=False):
        base = Path(current_root)
        directories[:] = [
            name
            for name in directories
            if name not in SKIP_DIRECTORIES
            and not name.startswith(".cache")
            and not (base / name).is_symlink()
        ]
        for filename in filenames:
            path = base / filename
            if path.is_symlink():
                continue
            if len(files) >= limit:
                truncated = True
                return files, truncated
            files.append(path)

    return files, truncated


def contains_tool_script(paths: Iterable[Path]) -> bool:
    for path in paths:
        if path.suffix.lower() != ".gd":
            continue
        try:
            if path.stat().st_size > 1_000_000:
                continue
            if "@tool" in path.read_text(encoding="utf-8", errors="ignore"):
                return True
        except OSError:
            continue
    return False


def parse_export_presets(path: Path) -> list[str]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    return sorted(set(re.findall(r'(?m)^name\s*=\s*"([^"]+)"\s*$', text)))


def relative_strings(root: Path, paths: Iterable[Path]) -> list[str]:
    return sorted(path.relative_to(root).as_posix() for path in paths)


def build_inventory(root: Path, max_files: int) -> ProjectInventory:
    project_file = root / "project.godot"
    text = project_file.read_text(encoding="utf-8", errors="replace")
    files, truncated = walk_files(root, max_files)

    language_counts: Counter[str] = Counter()
    content_counts: Counter[str] = Counter()
    gdextensions: list[Path] = []

    for path in files:
        suffix = path.suffix.lower()
        if suffix in LANGUAGE_EXTENSIONS:
            language_counts[LANGUAGE_EXTENSIONS[suffix]] += 1
        if suffix in CONTENT_EXTENSIONS:
            content_counts[CONTENT_EXTENSIONS[suffix]] += 1
        if suffix == ".gdextension":
            gdextensions.append(path)

    addons_root = root / "addons"
    addons = (
        sorted(path.name for path in addons_root.iterdir() if path.is_dir())
        if addons_root.is_dir()
        else []
    )

    test_candidates = [
        root / name
        for name in ("test", "tests", "spec", "specs")
        if (root / name).exists()
    ]
    test_candidates.extend(
        path
        for path in files
        if path.name.lower() in {"gut_cmdln.gd", "gdunit4_testadapter.cs"}
    )

    instruction_files = [
        root / name
        for name in ("AGENTS.md", "CLAUDE.md", "README.md")
        if (root / name).is_file()
    ]
    profile = root / "GODOT_PROJECT.md"

    features = extract_packed_strings(text, "config/features")
    warnings: list[str] = []
    if parse_editor_plugins(text):
        warnings.append("Enabled editor plugins may execute code when the editor starts.")
    if gdextensions:
        warnings.append("Native GDExtension libraries may execute when the project loads.")
    if contains_tool_script(files):
        warnings.append("The project contains @tool scripts; review them before editor/import execution.")
    if truncated:
        warnings.append(f"File scan stopped at the --max-files limit ({max_files}).")

    return ProjectInventory(
        project_root=str(root),
        project_name=extract_scalar(text, "config/name"),
        main_scene=extract_scalar(text, "run/main_scene"),
        feature_tags=features,
        inferred_engine_branch=infer_engine_branch(features),
        renderers=parse_renderers(text, features),
        languages=dict(sorted(language_counts.items())),
        content=dict(sorted(content_counts.items())),
        autoloads=parse_autoloads(text),
        enabled_editor_plugins=parse_editor_plugins(text),
        addons=addons,
        gdextensions=relative_strings(root, gdextensions),
        export_presets=parse_export_presets(root / "export_presets.cfg"),
        test_locations=relative_strings(root, set(test_candidates)),
        project_profile="GODOT_PROJECT.md" if profile.is_file() else None,
        repository_instructions=relative_strings(root, instruction_files),
        warnings=warnings,
        scanned_files=len(files),
        scan_truncated=truncated,
    )


def format_mapping(mapping: dict[str, object]) -> str:
    if not mapping:
        return "none detected"
    return ", ".join(f"{key}={value}" for key, value in mapping.items())


def format_list(values: list[str]) -> str:
    return ", ".join(values) if values else "none detected"


def render_markdown(inventory: ProjectInventory) -> str:
    lines = [
        "# Godot project inventory",
        "",
        f"- Root: `{inventory.project_root}`",
        f"- Name: `{inventory.project_name or 'unknown'}`",
        f"- Engine branch hint: `{inventory.inferred_engine_branch or 'unknown'}`",
        f"- Feature tags: {format_list(inventory.feature_tags)}",
        f"- Renderer hints: {format_list(inventory.renderers)}",
        f"- Main scene: `{inventory.main_scene or 'not configured/detected'}`",
        f"- Languages: {format_mapping(inventory.languages)}",
        f"- Content: {format_mapping(inventory.content)}",
        f"- Autoloads: {format_mapping(inventory.autoloads)}",
        f"- Editor plugins: {format_list(inventory.enabled_editor_plugins)}",
        f"- Addons: {format_list(inventory.addons)}",
        f"- GDExtensions: {format_list(inventory.gdextensions)}",
        f"- Export presets: {format_list(inventory.export_presets)}",
        f"- Test locations: {format_list(inventory.test_locations)}",
        f"- Project profile: {inventory.project_profile or 'missing'}",
        f"- Repository instructions: {format_list(inventory.repository_instructions)}",
        f"- Files scanned: {inventory.scanned_files}{' (truncated)' if inventory.scan_truncated else ''}",
    ]
    if inventory.warnings:
        lines.extend(["", "## Safety notes", ""])
        lines.extend(f"- {warning}" for warning in inventory.warnings)
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Project directory or a descendant of it (default: current directory).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of compact Markdown.",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=50_000,
        help="Maximum files to inspect before truncating the inventory (default: 50000).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.max_files < 1:
        print("error: --max-files must be positive", file=sys.stderr)
        return 2

    try:
        root = find_project_root(args.root)
        inventory = build_inventory(root, args.max_files)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(asdict(inventory), indent=2, sort_keys=True))
    else:
        print(render_markdown(inventory))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
