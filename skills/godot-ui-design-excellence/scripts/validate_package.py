#!/usr/bin/env python3
"""Read-only structural checks for this skill package. No network or engine execution."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

LINK = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)")
SOURCE_LINK = re.compile(r"sources\.md#([a-z][0-9]{2,3})")


def markdown_anchors(text: str) -> set[str]:
    """Support explicit anchors and the simple heading slugs used by this package."""
    anchors = set(re.findall(r'<a\s+id="([^"]+)"', text))
    for title in re.findall(r"^#{1,6}\s+(.+)$", text, flags=re.MULTILINE):
        title = re.sub(r"[`*_]", "", title).lower().strip()
        title = re.sub(r"[^\w\s-]", "", title)
        anchors.add(re.sub(r"\s", "-", title))
    return anchors


def validate(root: Path) -> tuple[list[str], dict[str, int]]:
    root = root.resolve()
    errors: list[str] = []
    stats: dict[str, int] = {}
    if not root.is_dir():
        return [f"Package directory not found: {root}"], stats
    required = ["SKILL.md", "README.md", "references/sources.md", "assets/sources.json", "evals/cases.json"]
    for name in required:
        if not (root / name).is_file():
            errors.append(f"Missing required file: {name}")
    if errors:
        return errors, stats
    files = sorted(p for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    if any(p.is_symlink() for p in root.rglob("*")):
        return ["Package contains a symbolic link; expected self-contained ordinary files."], stats
    texts: dict[Path, str] = {}
    for path in files:
        if path.suffix in {".md", ".json", ".py", ".gdshader", ".txt"}:
            try:
                texts[path] = path.read_text(encoding="utf-8")
            except (UnicodeError, OSError) as exc:
                errors.append(f"Cannot read {path.relative_to(root)} as UTF-8: {exc}")
    skill = texts.get(root / "SKILL.md", "")
    # Deliberately validate the simple metadata shape in this package, not all YAML.
    front = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
    if front is None:
        errors.append("SKILL.md must start with YAML frontmatter.")
    else:
        name = re.search(r"^name:\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*$", front.group(1), re.MULTILINE)
        if name is None or len(name.group(1)) > 64:
            errors.append("Missing or invalid skill name.")
        elif name.group(1) != root.name:
            errors.append("Skill name must match the package directory name.")
        description_match = re.search(r"^description:\s*>-?\n((?:[ \t]+[^\n]*\n?)*)", front.group(1), re.MULTILINE)
        description = " ".join(description_match.group(1).split()) if description_match else ""
        if not 1 <= len(description) <= 1024:
            errors.append("Description must be a nonempty folded string no longer than 1024 characters.")
    if len(skill.splitlines()) > 500:
        errors.append("SKILL.md exceeds the recommended 500-line limit.")
    if len(re.findall(r"\S+", skill)) > 1800:
        errors.append("Router exceeds this package's 1800-word guardrail.")
    for path, text in texts.items():
        if path.suffix in {".md", ".json"} and any(marker in text for marker in ("\ue200cite", "\ue200filecite", "turn0search")):
            errors.append(f"Nonportable tool citation in {path.relative_to(root)}")
        if path.suffix != ".md":
            continue
        # The package uses simple inline links, not a general-purpose Markdown dialect.
        prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        for value in LINK.findall(prose):
            value = value.strip().strip("<>")
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc:
                continue
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            if not target.is_relative_to(root):
                errors.append(f"Local link escapes package: {path.relative_to(root)} -> {value}")
                continue
            if not target.is_file():
                errors.append(f"Broken local link: {path.relative_to(root)} -> {value}")
                continue
            if parsed.fragment and target.suffix == ".md":
                content = texts.get(target, "")
                if unquote(parsed.fragment) not in markdown_anchors(content):
                    errors.append(f"Missing local anchor: {path.relative_to(root)} -> {value}")
    json_data: dict[str, object] = {}
    for path, text in texts.items():
        if path.suffix == ".json":
            try:
                json_data[path.relative_to(root).as_posix()] = json.loads(text)
            except json.JSONDecodeError as exc:
                errors.append(f"Invalid JSON in {path.relative_to(root)}: {exc}")
    source_file = json_data.get("assets/sources.json")
    ids: set[str] = set()
    if isinstance(source_file, dict) and isinstance(source_file.get("sources"), list):
        for item in source_file["sources"]:
            if not isinstance(item, dict):
                errors.append("Source record is not an object.")
                continue
            sid = item.get("id")
            if not isinstance(sid, str) or not re.fullmatch(r"[A-Z][0-9]{2,3}", sid):
                errors.append("Invalid source ID.")
                continue
            if sid in ids:
                errors.append(f"Duplicate source ID: {sid}")
            ids.add(sid)
            url = item.get("url")
            if not isinstance(url, str) or urlsplit(url).scheme != "https" or not urlsplit(url).netloc:
                errors.append(f"Invalid source URL: {sid}")
            if not item.get("reviewed_on") or not item.get("supports"):
                errors.append(f"Incomplete source record: {sid}")
        for path, text in texts.items():
            if path.suffix == ".md":
                for linked_id in SOURCE_LINK.findall(text):
                    if linked_id.upper() not in ids:
                        errors.append(f"Unknown source {linked_id} in {path.relative_to(root)}")
    else:
        errors.append("Source register has no valid sources array.")
    modules = {p.stem for p in (root / "references").glob("*.md")}
    for module in modules:
        if f"references/{module}.md" not in skill:
            errors.append(f"Module is not directly routed from SKILL.md: {module}")
    evaluation_file = json_data.get("evals/cases.json")
    cases: list[object] = []
    if isinstance(evaluation_file, dict) and isinstance(evaluation_file.get("cases"), list):
        cases = evaluation_file["cases"]
        seen: set[str] = set()
        for case in cases:
            if not isinstance(case, dict) or not isinstance(case.get("id"), str):
                errors.append("Malformed evaluation case.")
                continue
            cid = case["id"]
            if cid in seen:
                errors.append(f"Duplicate evaluation case: {cid}")
            seen.add(cid)
            if not case.get("prompt") or not case.get("pass_criteria"):
                errors.append(f"Incomplete evaluation case: {cid}")
            for module in case.get("relevant_modules", []):
                if module not in modules:
                    errors.append(f"Unknown evaluation module: {module}")
    else:
        errors.append("Evaluation file has no valid cases array.")
    stats.update(files=len(files), markdown_files=sum(p.suffix == ".md" for p in files),
                 reference_modules=len(modules), sources=len(ids), evaluation_cases=len(cases),
                 router_lines=len(skill.splitlines()), router_words=len(re.findall(r"\S+", skill)))
    return errors, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    errors, stats = validate(args.root)
    if args.as_json:
        print(json.dumps({"passed": not errors, "stats": stats, "errors": errors}, indent=2))
    else:
        print("PASS" if not errors else "FAIL")
        print(json.dumps(stats, indent=2))
        for error in errors:
            print(f"ERROR: {error}")
        print("Structural checks only; no external URL availability, Godot execution, or visual-quality evaluation.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
