#!/usr/bin/env python3
"""Validate this skill's package structure without network access or file writes.

Python 3.10+, standard library only. This intentionally validates the small
frontmatter and link syntax used here, not every possible YAML/Markdown construct.
Behavioral evaluation fixtures are checked as data; no agent is invoked.
"""
from __future__ import annotations

import argparse
import ast
import base64
import binascii
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


PACKAGE_FILE_EXTENSIONS = {".md", ".json", ".py"}
# The examples are an optional, self-contained harness. Keep its allowlist
# narrow so adding a runnable example cannot silently broaden the package into
# a binary asset or build-output archive.
EXAMPLE_FILE_EXTENSIONS = {".html", ".css", ".js", ".mjs", ".gltf"}
# Generated/vendor trees make an example non-reproducible and can smuggle a
# dependency archive into the distributed skill even when individual files use
# an allowed extension.
EXAMPLE_FORBIDDEN_DIRECTORIES = {
    ".cache",
    ".mypy_cache",
    ".pytest_cache",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "playwright-report",
    "test-results",
}
EXPECTED_STYLE_COUNT = 12
EXPECTED_TECHNIQUE_COUNT = 18


def prose_without_fences(text: str, label: str, errors: list[str]) -> str:
    """Remove fenced blocks while checking matching fence boundaries."""
    output: list[str] = []
    active: tuple[str, int] | None = None
    for number, line in enumerate(text.splitlines(), 1):
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if active is not None:
            if match:
                mark, tail = match.groups()
                if mark[0] == active[0] and len(mark) >= active[1] and not tail.strip():
                    active = None
            output.append("")
        elif match:
            mark, _ = match.groups()
            active = (mark[0], len(mark))
            output.append("")
        else:
            output.append(line)
    if active is not None:
        errors.append(f"{label}: unclosed fenced code block")
    return "\n".join(output)


def is_in_examples(path: Path, root: Path) -> bool:
    """Return whether path is contained by the optional examples directory."""
    try:
        return path.relative_to(root / "examples") is not None
    except ValueError:
        return False


def validate_gltf(path: Path, root: Path, errors: list[str]) -> None:
    """Validate JSON GLTF fixtures and keep their resource URIs package-local.

    GLB is intentionally not accepted by the package extension allowlist. A
    GLTF with data URIs exercises the same browser loading path while keeping
    the fixture inspectable and self-contained. This is a focused fixture
    check, not a complete Khronos schema validator.
    """
    label = path.relative_to(root).as_posix()
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{label}: invalid GLTF JSON: {exc}")
        return
    if not isinstance(document, dict):
        errors.append(f"{label}: GLTF document must be an object")
        return
    asset = document.get("asset")
    if not isinstance(asset, dict) or asset.get("version") != "2.0":
        errors.append(f"{label}: GLTF asset.version must be '2.0'")
    for collection_name in ("buffers", "images"):
        collection = document.get(collection_name, [])
        if not isinstance(collection, list):
            errors.append(f"{label}: GLTF {collection_name} must be a list")
            continue
        for index, item in enumerate(collection):
            if not isinstance(item, dict):
                errors.append(f"{label}: GLTF {collection_name}[{index}] must be an object")
                continue
            if collection_name == "buffers":
                byte_length = item.get("byteLength")
                if not isinstance(byte_length, int) or isinstance(byte_length, bool) or byte_length < 0:
                    errors.append(f"{label}: GLTF buffers[{index}] has an invalid byteLength")
            uri = item.get("uri")
            if uri is None:
                if collection_name == "buffers":
                    errors.append(f"{label}: GLTF buffers[{index}] must have an embedded or local URI")
                continue
            if not isinstance(uri, str) or not uri:
                errors.append(f"{label}: GLTF {collection_name}[{index}] has an invalid URI")
                continue
            try:
                parsed = urlsplit(uri)
            except ValueError as exc:
                errors.append(f"{label}: GLTF {collection_name}[{index}] has an invalid URI: {exc}")
                continue
            # Data URIs are embedded content and therefore do not create an
            # external request. Every other URI must be a relative package
            # path; protocol-relative and absolute URLs are rejected.
            if parsed.scheme == "data":
                if collection_name == "buffers":
                    header, separator, encoded = uri.partition(",")
                    if separator == "" or not header.lower().endswith(";base64"):
                        errors.append(f"{label}: GLTF buffers[{index}] must use a base64 data URI")
                        continue
                    try:
                        decoded_buffer = base64.b64decode(encoded, validate=True)
                    except (binascii.Error, ValueError):
                        errors.append(f"{label}: GLTF buffers[{index}] contains invalid base64")
                        continue
                    if len(decoded_buffer) != item.get("byteLength"):
                        errors.append(
                            f"{label}: GLTF buffers[{index}] byteLength does not match embedded data"
                        )
                continue
            if parsed.scheme or parsed.netloc or parsed.path.startswith("/"):
                errors.append(f"{label}: GLTF {collection_name}[{index}] uses an external URI: {uri}")
                continue
            decoded = unquote(parsed.path)
            destination = (path.parent / decoded).resolve()
            if not destination.is_relative_to(root):
                errors.append(f"{label}: GLTF resource escapes package: {uri}")
            elif not destination.is_file():
                errors.append(f"{label}: missing GLTF resource: {uri}")


def validate_example_references(path: Path, root: Path, errors: list[str]) -> int:
    """Check local HTML/CSS resource references used by the optional harness."""
    if path.suffix not in {".html", ".css"}:
        return 0
    label = path.relative_to(root).as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{label}: cannot read example source: {exc}")
        return 0
    if "\ufffd" in text or "\x00" in text:
        errors.append(f"{label}: broken encoding")
    if path.suffix == ".html":
        values = re.findall(r"\b(?:src|href|poster)\s*=\s*[\"']([^\"']+)[\"']", text, re.IGNORECASE)
    else:
        values = re.findall(r"url\(\s*[\"']?([^\"')]+)[\"']?\s*\)", text, re.IGNORECASE)
    checked = 0
    for value in values:
        value = value.strip()
        try:
            parsed = urlsplit(value)
        except ValueError as exc:
            errors.append(f"{label}: malformed local asset reference: {value}: {exc}")
            continue
        if not value or parsed.scheme or parsed.netloc or value.startswith("#"):
            continue
        decoded = unquote(parsed.path)
        if not decoded:
            continue
        destination = (path.parent / decoded).resolve()
        checked += 1
        if not destination.is_relative_to(root):
            errors.append(f"{label}: local asset reference escapes package: {value}")
        elif not destination.is_file():
            errors.append(f"{label}: missing local asset reference: {value}")
    return checked


def validate(root: Path) -> dict[str, object]:
    errors: list[str] = []
    if not root.is_dir():
        return {"passed": False, "errors": [f"Not a directory: {root}"]}
    root = root.resolve()
    entries = sorted(root.rglob("*"))
    files = [p for p in entries if p.is_file() and not p.is_symlink()]
    for entry in entries:
        if entry.is_symlink():
            errors.append(f"Symlinks are not part of this distribution: {entry.relative_to(root)}")
        if entry.is_dir() and is_in_examples(entry, root):
            relative_parts = entry.relative_to(root).parts
            for index, part in enumerate(relative_parts):
                if part in EXAMPLE_FORBIDDEN_DIRECTORIES and not any(
                    previous in EXAMPLE_FORBIDDEN_DIRECTORIES for previous in relative_parts[:index]
                ):
                    errors.append(f"Forbidden generated/vendor directory in examples: {part}")
                    break
    for path in files:
        allowed = path.suffix in PACKAGE_FILE_EXTENSIONS
        allowed = allowed or (is_in_examples(path, root) and path.suffix in EXAMPLE_FILE_EXTENSIONS)
        if not allowed:
            errors.append(f"Unexpected file type: {path.relative_to(root)}")
    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        return {"passed": False, "errors": errors + ["Missing SKILL.md"]}
    skill = skill_path.read_text(encoding="utf-8")
    front = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
    if front is None:
        errors.append("SKILL.md: missing delimited frontmatter")
    else:
        # The shipped subset is exactly a plain name and a folded description.
        fields = re.fullmatch(r"name: ([a-z0-9-]+)\ndescription: >-\n((?:  [^\n]+\n?)+)", front.group(1))
        if fields is None:
            errors.append("Frontmatter does not match this package's documented subset")
        else:
            name, raw_description = fields.groups()
            description = " ".join(line.strip() for line in raw_description.splitlines())
            if len(name) > 64 or name.startswith("-") or name.endswith("-") or "--" in name:
                errors.append("Invalid skill name")
            if name != root.name:
                errors.append("Skill name must match the directory name")
            if not 1 <= len(description) <= 1024:
                errors.append("Description must contain 1–1024 characters")
    if len(skill.splitlines()) > 500:
        errors.append("Main skill exceeds the package's 500-line ceiling")

    markdown = [p for p in files if p.suffix == ".md"]
    local_links = 0
    directly_routed: set[Path] = set()
    for path in markdown:
        label = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        if "\ufffd" in text or "\x00" in text or "" in text:
            errors.append(f"{label}: broken encoding or chat-only citation marker")
        prose = prose_without_fences(text, label, errors)
        for target in re.findall(r"\[[^\]\n]*\]\(([^\s)]+)\)", prose):
            try:
                parsed = urlsplit(target)
            except ValueError as exc:
                errors.append(f"{label}: malformed link target: {target}: {exc}")
                continue
            if parsed.scheme or parsed.netloc or target.startswith("#"):
                continue
            decoded = unquote(parsed.path)
            if not decoded:
                continue
            destination = (path.parent / decoded).resolve()
            local_links += 1
            if not destination.is_relative_to(root):
                errors.append(f"{label}: local link escapes package: {target}")
            elif not destination.is_file():
                errors.append(f"{label}: missing local link target: {target}")
            elif path == skill_path:
                directly_routed.add(destination)
    references = sorted((root / "references").glob("*.md"))
    for path in references:
        if path.resolve() not in directly_routed:
            errors.append(f"Reference is not directly routed from SKILL.md: {path.name}")
        text = path.read_text(encoding="utf-8")
        if not text.startswith("# ") or "**Load when:**" not in text:
            errors.append(f"Reference lacks a title or load trigger: {path.name}")
        if len(text.split()) > 1500:
            errors.append(f"Reference exceeds this package's 1500-word guardrail: {path.name}")
    style_paths = [p for p in references if p.stem.startswith("style-") and p.stem != "style-selection"]
    styles = {p.stem.removeprefix("style-") for p in style_paths}
    techniques = [p for p in references if p.stem.startswith("technique-")]
    if len(styles) != EXPECTED_STYLE_COUNT or len(techniques) != EXPECTED_TECHNIQUE_COUNT:
        errors.append(
            "Update the documented inventory: expected "
            f"{EXPECTED_STYLE_COUNT} styles and {EXPECTED_TECHNIQUE_COUNT} techniques"
        )

    example_files = [path for path in files if is_in_examples(path, root)]
    example_local_links = 0
    for path in example_files:
        if path.suffix == ".gltf":
            validate_gltf(path, root, errors)
        elif path.suffix in {".html", ".css"}:
            example_local_links += validate_example_references(path, root, errors)

    fixture_path = root / "evals" / "routing-cases.json"
    case_count = 0
    if not fixture_path.is_file():
        errors.append("Missing behavioral evaluation fixtures")
    else:
        try:
            fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"Evaluation fixture is not valid JSON: {exc}")
            fixture = None
        if not isinstance(fixture, dict) or fixture.get("schema_version") != 1:
            errors.append("Unsupported evaluation fixture schema")
        elif not isinstance(fixture.get("cases"), list):
            errors.append("Evaluation cases must be a list")
        else:
            ids: set[str] = set()
            for item in fixture["cases"]:
                case_count += 1
                if not isinstance(item, dict):
                    errors.append("Evaluation case must be an object")
                    continue
                case_id = item.get("id")
                if not isinstance(case_id, str) or not case_id or case_id in ids:
                    errors.append(f"Invalid or duplicate case id: {case_id}")
                    continue
                ids.add(case_id)
                for field in ("prompt", "scope", "style_mode"):
                    if not isinstance(item.get(field), str) or not item[field].strip():
                        errors.append(f"{case_id}: missing {field}")
                allowed = item.get("allowed_styles")
                if not isinstance(allowed, list) or any(not isinstance(s, str) or s not in styles for s in allowed):
                    errors.append(f"{case_id}: unknown allowed style")
                    allowed = []
                mode = item.get("style_mode")
                if mode not in {"none", "preserve", "single", "alternatives", "scoped-hybrid"}:
                    errors.append(f"{case_id}: unknown style mode")
                if mode in {"none", "preserve"} and allowed:
                    errors.append(f"{case_id}: preserved direction must not request a new style")
                if mode == "single" and len(allowed) != 1:
                    errors.append(f"{case_id}: single style must specify one expected direction")
                assertions = item.get("assertions")
                if not isinstance(assertions, list) or not assertions or any(not isinstance(a, str) or not a for a in assertions):
                    errors.append(f"{case_id}: missing assertions")
                trigger = item.get("should_trigger")
                if not isinstance(trigger, bool):
                    errors.append(f"{case_id}: should_trigger must be boolean")
                budget = item.get("max_initial_reference_reads")
                if not isinstance(budget, int) or isinstance(budget, bool) or budget < 0:
                    errors.append(f"{case_id}: invalid initial read budget")
                routes = item.get("relevant_by_completion")
                if not isinstance(routes, list):
                    errors.append(f"{case_id}: routes must be a list")
                    continue
                if trigger is False and (routes or mode != "none" or budget != 0):
                    errors.append(f"{case_id}: negative trigger has active routes")
                for route in routes:
                    if not isinstance(route, str):
                        errors.append(f"{case_id}: route must be a string")
                        continue
                    path = (root / route).resolve()
                    if not route.startswith("references/") or not path.is_relative_to(root) or not path.is_file():
                        errors.append(f"{case_id}: invalid route: {route}")
                    if path.stem.startswith("style-") and path.stem != "style-selection":
                        if path.stem.removeprefix("style-") not in allowed:
                            errors.append(f"{case_id}: route imports a disallowed style: {route}")
    for path in files:
        if path.suffix == ".py":
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except SyntaxError as exc:
                errors.append(f"Python syntax error: {exc}")
    return {
        "passed": not errors,
        "files": len(files),
        "markdown_files": len(markdown),
        "main_lines": len(skill.splitlines()),
        "main_whitespace_words": len(skill.split()),
        "reference_modules": len(references),
        "styles": len(styles),
        "techniques": len(techniques),
        "example_files": len(example_files),
        "example_local_links_checked": example_local_links,
        "gltf_fixtures": sum(path.suffix == ".gltf" for path in example_files),
        "local_links_checked": local_links,
        "behavioral_fixtures": case_count,
        "agent_evaluations_executed": 0,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        result = validate(args.root)
    except (OSError, UnicodeError, ValueError) as exc:
        print(json.dumps({"passed": False, "errors": [str(exc)]}, indent=2), file=sys.stdout)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
