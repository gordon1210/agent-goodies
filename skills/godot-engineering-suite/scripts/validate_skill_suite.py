#!/usr/bin/env python3
"""Validate the Godot Engineering Suite without third-party dependencies."""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

ALLOWED_FRONTMATTER = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"\[[^\]]+\]\((references|scripts|assets)/([^)#]+)(?:#[^)]+)?\)")


def parse_frontmatter(skill_file: Path) -> tuple[dict[str, str], set[str]]:
    text = skill_file.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("SKILL.md must begin with YAML frontmatter")

    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("SKILL.md frontmatter is not closed") from error

    scalars: dict[str, str] = {}
    top_level: set[str] = set()
    for line in lines[1:end]:
        if not line or line[0].isspace() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", line)
        if not match:
            raise ValueError(f"Invalid top-level frontmatter line: {line!r}")
        key, value = match.groups()
        top_level.add(key)
        if value:
            scalars[key] = value.strip().strip('"').strip("'")
    return scalars, top_level


def validate(skill_root: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_root / "SKILL.md"
    if not skill_file.is_file():
        return [f"Missing {skill_file}"]

    try:
        scalars, fields = parse_frontmatter(skill_file)
    except (OSError, ValueError) as error:
        return [str(error)]

    unknown = fields - ALLOWED_FRONTMATTER
    if unknown:
        errors.append(f"Unsupported Agent Skills frontmatter fields: {sorted(unknown)}")

    name = scalars.get("name", "")
    description = scalars.get("description", "")
    if not NAME_PATTERN.fullmatch(name):
        errors.append(f"Invalid skill name: {name!r}")
    if name != skill_root.name:
        errors.append(f"Skill name {name!r} does not match directory {skill_root.name!r}")
    if not description or len(description) > 1024:
        errors.append("Description must contain 1-1024 characters")
    if "allowed-tools" in fields:
        errors.append("Suite policy forbids allowed-tools grants")

    skill_text = skill_file.read_text(encoding="utf-8")
    if len(skill_text.splitlines()) > 500:
        errors.append("SKILL.md exceeds the 500-line progressive-disclosure recommendation")

    referenced: set[Path] = set()
    for directory, relative in LINK_PATTERN.findall(skill_text):
        target = skill_root / directory / relative
        referenced.add(target.resolve())
        if not target.is_file():
            errors.append(f"Broken internal link: {directory}/{relative}")

    reference_root = skill_root / "references"
    if not reference_root.is_dir():
        errors.append("Missing references directory")
    else:
        for path in sorted(reference_root.glob("*.md")):
            if path.resolve() not in referenced:
                errors.append(f"Unrouted reference file: {path.name}")
            if len(path.read_text(encoding="utf-8").splitlines()) > 250:
                errors.append(f"Reference is too large for focused loading: {path.name}")
        nested = [path for path in reference_root.rglob("*") if path.is_file() and path.parent != reference_root]
        if nested:
            errors.append("References must remain one directory level below SKILL.md")

    for path in sorted((skill_root / "scripts").glob("*.py")):
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, SyntaxError) as error:
            errors.append(f"Python syntax error in {path.name}: {error}")

    for path in skill_root.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        data = path.read_bytes()
        if data and not data.endswith(b"\n"):
            errors.append(f"File lacks final newline: {path.relative_to(skill_root)}")
        if b"\r\n" in data:
            errors.append(f"File uses CRLF instead of LF: {path.relative_to(skill_root)}")

    return errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skill-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Path to the skill directory containing SKILL.md.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = args.skill_root.expanduser().resolve()
    errors = validate(root)
    if errors:
        print("Skill suite validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    reference_count = len(list((root / "references").glob("*.md")))
    print(f"Skill suite is valid: {root} ({reference_count} routed references)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
