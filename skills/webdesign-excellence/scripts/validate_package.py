#!/usr/bin/env python3
"""Validate this skill's package structure without network access or file writes.

Python 3.10+, standard library only. This intentionally validates the small
frontmatter and link syntax used here, not every possible YAML/Markdown construct.
Behavioral evaluation fixtures are checked as data; no agent is invoked.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


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
    for path in files:
        if path.suffix not in {".md", ".json", ".py"}:
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
            parsed = urlsplit(target)
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
    if len(styles) != 12 or len(techniques) != 14:
        errors.append("Update the documented inventory: expected 12 styles and 14 techniques")

    fixture_path = root / "evals" / "routing-cases.json"
    case_count = 0
    if not fixture_path.is_file():
        errors.append("Missing behavioral evaluation fixtures")
    else:
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
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
