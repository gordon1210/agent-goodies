#!/usr/bin/env python3
"""Repo-local handoff helper.

This tool keeps a human-readable HANDOFF.md and an append-only JSONL event
journal under .handoff/. It intentionally avoids SQLite as the primary store so
handoff state remains diffable, reviewable, and merge-friendly.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import quote

SKILL_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_ROOT / "assets"


def load_json_asset(name: str) -> dict[str, Any]:
    path = ASSETS_DIR / name
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Unable to load bundled Handoff asset {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"Bundled Handoff asset must contain a JSON object: {path}")
    return value


EVENT_TYPES = {
    "session_start",
    "session_end",
    "status",
    "plan",
    "decision",
    "change",
    "validation",
    "blocker",
    "risk",
    "question",
    "todo",
    "handoff",
}

RELATION_FIELDS = ("resolves", "supersedes")
LIST_FIELDS = ("scope", "files", "tags", "next_actions", *RELATION_FIELDS)
EVENT_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
TERMINAL_STATUSES = {
    "abandoned",
    "cancelled",
    "canceled",
    "closed",
    "complete",
    "completed",
    "done",
    "merged",
    "resolved",
    "superseded",
}
CONTEXT_STATUSES = {"active", "closed", "merged", "abandoned"}
TERMINAL_CONTEXT_STATUSES = CONTEXT_STATUSES - {"active"}

DEFAULT_CONFIG = load_json_asset("config.template.json")
SCHEMA = load_json_asset("schema.template.json")


@dataclass(frozen=True)
class HandoffPaths:
    root: Path
    handoff_dir: Path
    events_dir: Path
    archive_dir: Path
    handoff_md: Path
    config_file: Path
    schema_file: Path
    readme_file: Path


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso_now() -> str:
    return utc_now().isoformat().replace("+00:00", "Z")


def parse_timestamp(value: Any) -> dt.datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    candidate = value.strip()
    if candidate.endswith("Z"):
        candidate = candidate[:-1] + "+00:00"
    try:
        parsed = dt.datetime.fromisoformat(candidate)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed.astimezone(dt.timezone.utc)


def event_sort_key(event: dict[str, Any]) -> tuple[dt.datetime, str, str]:
    timestamp = parse_timestamp(event.get("ts")) or dt.datetime.min.replace(
        tzinfo=dt.timezone.utc
    )
    return (
        timestamp,
        str(event.get("id", "")),
        str(event.get("__path", "")),
    )


def safe_slug(value: str, fallback: str = "event") -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-._")
    return value[:48] or fallback


# Encoded branch tokens longer than this use a stable prefix+hash form so the
# day/agent/type/branch/commit filename stays well under filesystem NAME_MAX.
BRANCH_FILENAME_MAX = 50


def branch_filename_token(value: str, fallback: str = "no-branch") -> str:
    """Encode a branch name without collapsing distinct Git ref names.

    Short names stay fully percent-encoded. Encoded names longer than
    BRANCH_FILENAME_MAX become ``<prefix>~<sha256[:12]>`` of the original
    branch string so tokens remain injective, stable for batching, and short
    enough for a single path component.
    """
    value = value.strip()
    if not value:
        return fallback
    encoded = quote(value, safe="-._~")
    if len(encoded) <= BRANCH_FILENAME_MAX:
        return encoded
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]
    prefix_budget = BRANCH_FILENAME_MAX - 1 - len(digest)
    prefix = encoded[:prefix_budget]
    # Avoid truncating a percent-escape mid-sequence (e.g. "%2" of "%2F").
    pct = prefix.rfind("%")
    if pct != -1 and pct > len(prefix) - 3:
        prefix = prefix[:pct]
    prefix = prefix.rstrip("-._~")
    if not prefix:
        return f"b~{digest}"
    return f"{prefix}~{digest}"


def find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists():
            return candidate
        if (candidate / "HANDOFF.md").exists() or (candidate / ".handoff").exists():
            return candidate
    return current


def paths(root: Path | None = None) -> HandoffPaths:
    repo = find_repo_root(root)
    handoff_dir = repo / ".handoff"
    return HandoffPaths(
        root=repo,
        handoff_dir=handoff_dir,
        events_dir=handoff_dir / "events",
        archive_dir=handoff_dir / "archive",
        handoff_md=repo / "HANDOFF.md",
        config_file=handoff_dir / "config.json",
        schema_file=handoff_dir / "schema.json",
        readme_file=handoff_dir / "README.md",
    )


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_readme() -> str:
    return """# .handoff

Repo-local continuity journal for humans and AI agents.

- `HANDOFF.md` is the compact human-readable current-state summary.
- `.handoff/events/**.jsonl` is the append-only machine-readable event journal.
- New event batches append to contextual files named like `YYYYMMDDZ-<agent>-<type>-<branch>-<commit>.jsonl`.
- Branch names are encoded for filenames without collapsing distinct refs. Short names stay fully encoded; longer names use a stable prefix+hash token. Detached worktrees use their Git worktree name instead.
- Existing one-event `.jsonl` files remain valid; the reader supports mixed history.
- Generated `handoff-ref` comments identify active events and next actions. Resolve or supersede them through a new event; never rewrite their source line.
- Mark completed branch/worktree contexts `closed`, `merged`, or `abandoned` so they leave active state.
- Do not store secrets, tokens, credentials, private keys, or personal data here.

The helper requires Python 3.9 or newer and is bundled as `scripts/handoff.py` inside the installed Handoff skill. Resolve it relative to that skill's `SKILL.md`, keep the target repository as the working directory, and run:

```bash
python3 "<handoff-skill-directory>/scripts/handoff.py" status
python3 "<handoff-skill-directory>/scripts/handoff.py" tail --limit 20
python3 "<handoff-skill-directory>/scripts/handoff.py" add --type decision --summary "Chose JSONL handoff journal" --agent "copilot-cli"
python3 "<handoff-skill-directory>/scripts/handoff.py" add --type validation --summary "Tests passed" --resolve "<action-ref>" --agent "copilot-cli"
python3 "<handoff-skill-directory>/scripts/handoff.py" render
python3 "<handoff-skill-directory>/scripts/handoff.py" validate
```
"""


def build_handoff_template() -> str:
    path = ASSETS_DIR / "HANDOFF.template.md"
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"Unable to load bundled Handoff asset {path}: {exc}") from exc


def load_config(p: HandoffPaths) -> tuple[dict[str, Any], list[str]]:
    if not p.config_file.exists():
        return dict(DEFAULT_CONFIG), []
    try:
        raw = json.loads(p.config_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return dict(DEFAULT_CONFIG), [f"{p.config_file}: invalid JSON: {exc}"]
    if not isinstance(raw, dict):
        return dict(DEFAULT_CONFIG), [f"{p.config_file}: config must be a JSON object"]

    config = dict(DEFAULT_CONFIG)
    config.update(raw)
    errors: list[str] = []
    version = config.get("version")
    if type(version) is not int or version != 1:
        errors.append(f"{p.config_file}: field 'version' must be 1")
    recent_limit = config.get("max_recent_events_in_markdown")
    if type(recent_limit) is not int or recent_limit < 0:
        errors.append(
            f"{p.config_file}: field 'max_recent_events_in_markdown' "
            "must be a non-negative integer"
        )
    return config, errors


def read_config(p: HandoffPaths) -> dict[str, Any]:
    config, errors = load_config(p)
    if errors:
        raise ValueError("Invalid handoff configuration:\n- " + "\n- ".join(errors))
    return config


def validate_support_files(p: HandoffPaths) -> list[str]:
    _, errors = load_config(p)
    if p.schema_file.exists():
        try:
            schema = json.loads(p.schema_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{p.schema_file}: invalid JSON: {exc}")
        else:
            if not isinstance(schema, dict):
                errors.append(f"{p.schema_file}: schema must be a JSON object")
    return errors


def init_repo(args: argparse.Namespace) -> int:
    p = paths()
    p.events_dir.mkdir(parents=True, exist_ok=True)
    p.archive_dir.mkdir(parents=True, exist_ok=True)

    if not p.config_file.exists() or args.force:
        write_json(p.config_file, DEFAULT_CONFIG)
    if not p.schema_file.exists() or args.force:
        write_json(p.schema_file, SCHEMA)
    if not p.readme_file.exists() or args.force:
        p.readme_file.write_text(build_readme(), encoding="utf-8")
    if not p.handoff_md.exists() or args.force:
        p.handoff_md.write_text(build_handoff_template(), encoding="utf-8")

    print(f"Initialized handoff files in {p.root}")
    return 0


def parse_list(values: list[str] | None) -> list[str]:
    if not values:
        return []
    result: list[str] = []
    for value in values:
        for part in value.split(","):
            item = part.strip()
            if item:
                result.append(item)
    return result


def normalized_env(name: str) -> str | None:
    value = os.environ.get(name)
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def require_agent_name(args: argparse.Namespace) -> str:
    if isinstance(args.agent, str) and args.agent.strip():
        return args.agent.strip()
    env_agent = normalized_env("HANDOFF_AGENT")
    if env_agent:
        return env_agent
    raise ValueError("Agent identity required. Pass --agent <name> or set HANDOFF_AGENT.")


def git_output(root: Path, *args: str) -> str | None:
    completed = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return None
    value = completed.stdout.strip()
    return value or None


def git_commit(root: Path, short: bool = False) -> str | None:
    if short:
        return git_output(root, "rev-parse", "--short=12", "HEAD")
    return git_output(root, "rev-parse", "HEAD")


def git_branch(root: Path) -> str | None:
    return git_output(root, "symbolic-ref", "--quiet", "--short", "HEAD")


def git_worktree_name(root: Path) -> str | None:
    git_dir = git_output(root, "rev-parse", "--git-dir")
    if not git_dir:
        return None
    name = Path(git_dir.rstrip("/\\")).name
    return "main" if name == ".git" else (name or "main")


def git_metadata(root: Path) -> dict[str, Any] | None:
    commit = git_commit(root)
    branch = git_branch(root)
    worktree = git_worktree_name(root)
    metadata: dict[str, Any] = {}
    if commit:
        metadata["commit"] = commit
    if branch:
        metadata["branch"] = branch
    if worktree:
        metadata["worktree"] = worktree
    if commit and not branch:
        metadata["detached"] = True
    return metadata or None


def event_context_key(event: dict[str, Any]) -> str:
    git = event.get("git")
    if not isinstance(git, dict):
        return "no-git-context"
    branch = git.get("branch")
    if isinstance(branch, str) and branch.strip():
        return f"branch:{branch.strip()}"
    commit = str(git.get("commit", "")).strip()
    worktree = str(git.get("worktree", "")).strip()
    if git.get("detached") is True:
        return f"detached:{worktree or commit or 'unknown'}"
    return "legacy:unknown-branch" if commit else "no-git-context"


def event_context_label(event: dict[str, Any]) -> str:
    git = event.get("git")
    if not isinstance(git, dict):
        return "no Git context"
    branch = git.get("branch")
    if isinstance(branch, str) and branch.strip():
        return branch.strip()
    commit = str(git.get("commit", "")).strip()
    worktree = str(git.get("worktree", "")).strip()
    if git.get("detached") is True:
        return f"detached:{worktree or commit[:12] or 'unknown'}"
    if commit:
        return f"unknown branch@{commit[:12]}"
    return "no Git context"


def event_branch_token(event: dict[str, Any]) -> str:
    git = event.get("git")
    if not isinstance(git, dict):
        return "no-branch"
    branch = git.get("branch")
    if isinstance(branch, str) and branch.strip():
        return branch_filename_token(branch)
    worktree = str(git.get("worktree", "")).strip()
    if git.get("detached") is True:
        return branch_filename_token(f"detached-{worktree or 'unknown'}")
    return "no-branch"


def event_batch_path(p: HandoffPaths, event: dict[str, Any]) -> Path:
    event_ts = str(event.get("ts", ""))
    month = event_ts[:7] if re.fullmatch(r"\d{4}-\d{2}-\d{2}T.*Z", event_ts) else utc_now().strftime("%Y-%m")
    day = (
        event_ts[:10].replace("-", "") + "Z"
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}T.*Z", event_ts)
        else utc_now().strftime("%Y%m%dZ")
    )
    agent_name = safe_slug(str((event.get("agent") or {}).get("name", "")), "agent")
    event_type = safe_slug(str(event.get("type", "")), "event")
    branch = event_branch_token(event)
    commit = str((event.get("git") or {}).get("commit", "")).strip()
    commit_slug = safe_slug(commit[:12], "no-commit")
    filename = f"{day}-{agent_name}-{event_type}-{branch}-{commit_slug}.jsonl"
    return Path(month) / filename


def build_event(args: argparse.Namespace, root: Path) -> dict[str, Any]:
    event_type = args.type.strip()
    if event_type not in EVENT_TYPES and not args.allow_custom_type:
        allowed = ", ".join(sorted(EVENT_TYPES))
        raise ValueError(f"Unsupported event type '{event_type}'. Allowed: {allowed}")

    agent: dict[str, str] = {}
    agent_name = require_agent_name(args)
    model_name = args.model.strip() if isinstance(args.model, str) and args.model.strip() else normalized_env("HANDOFF_MODEL")
    session_id = args.session.strip() if isinstance(args.session, str) and args.session.strip() else normalized_env("HANDOFF_SESSION")
    agent["name"] = agent_name
    if model_name:
        agent["model"] = model_name
    if session_id:
        agent["session"] = session_id

    event: dict[str, Any] = {
        "v": 1,
        "id": uuid.uuid4().hex,
        "ts": iso_now(),
        "type": event_type,
        "summary": args.summary.strip(),
        "agent": agent,
    }
    git = git_metadata(root)
    if git:
        event["git"] = git

    optional_fields: list[tuple[str, Any]] = [
        ("details", args.details),
        ("status", args.status),
        ("context_status", args.context_status),
        ("scope", parse_list(args.scope)),
        ("files", parse_list(args.file)),
        ("tags", parse_list(args.tag)),
        ("next_actions", parse_list(args.next)),
        ("resolves", parse_list(args.resolve)),
        ("supersedes", parse_list(args.supersede)),
    ]

    for key, value in optional_fields:
        if value:
            event[key] = value

    return event


def link_matching_session_start(
    event: dict[str, Any], existing_events: list[dict[str, Any]]
) -> None:
    if event.get("type") != "session_end":
        return
    closed = closed_references(existing_events)
    for candidate in reversed(ordered_events(existing_events)):
        candidate_id = str(candidate.get("id", "")).strip()
        if (
            candidate.get("type") == "session_start"
            and candidate_id
            and candidate_id not in closed
            and sessions_match(candidate, event)
        ):
            resolves = event.setdefault("resolves", [])
            if isinstance(resolves, list) and candidate_id not in resolves:
                resolves.append(candidate_id)
            return


def add_event(args: argparse.Namespace) -> int:
    p = paths()
    if not p.handoff_dir.exists():
        init_repo(argparse.Namespace(force=False))

    event = build_event(args, p.root)
    existing_events, parse_errors = load_events(p)
    support_errors = validate_support_files(p)
    if parse_errors or support_errors:
        raise ValueError(
            "Cannot append to an invalid handoff journal:\n- "
            + "\n- ".join([*parse_errors, *support_errors])
        )
    link_matching_session_start(event, existing_events)
    validation_errors = validate_event_collection([*existing_events, event])
    if validation_errors:
        raise ValueError(
            "Cannot append invalid handoff event:\n- "
            + "\n- ".join(validation_errors)
        )

    event_path = p.events_dir / event_batch_path(p, event)
    event_path.parent.mkdir(parents=True, exist_ok=True)
    existed = event_path.exists()
    with event_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")

    rel = event_path.relative_to(p.root)
    print(f"{'Appended' if existed else 'Wrote'} {rel}")

    if args.render:
        render_markdown(argparse.Namespace(limit=None))

    return 0


def iter_event_files(p: HandoffPaths) -> Iterable[Path]:
    if not p.events_dir.exists():
        return []
    return sorted(p.events_dir.rglob("*.jsonl"))


def load_events(p: HandoffPaths) -> tuple[list[dict[str, Any]], list[str]]:
    events: list[dict[str, Any]] = []
    errors: list[str] = []

    for path in iter_event_files(p):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            errors.append(f"{path}: {exc}")
            continue

        for line_no, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                event = json.loads(stripped)
            except json.JSONDecodeError as exc:
                errors.append(f"{path}:{line_no}: invalid JSON: {exc}")
                continue
            if isinstance(event, dict):
                event["__path"] = str(path.relative_to(p.root))
                events.append(event)
            else:
                errors.append(f"{path}:{line_no}: line is not a JSON object")

    events.sort(key=event_sort_key)
    return events, errors


def validate_event(event: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = ["v", "id", "ts", "type", "summary"]
    for key in required:
        if key not in event:
            errors.append(f"missing required field: {key}")
    if type(event.get("v")) is not int or event.get("v") != 1:
        errors.append("field 'v' must be 1")
    if not isinstance(event.get("id"), str) or not event.get("id", "").strip():
        errors.append("field 'id' must be a non-empty string")
    elif not EVENT_ID_RE.fullmatch(event["id"].strip()):
        errors.append(
            "field 'id' may contain only letters, numbers, dots, underscores, and hyphens"
        )
    if parse_timestamp(event.get("ts")) is None:
        errors.append("field 'ts' must be an ISO 8601 timestamp with a timezone")
    if not isinstance(event.get("summary"), str) or not event.get("summary", "").strip():
        errors.append("field 'summary' must be a non-empty string")
    if not isinstance(event.get("type"), str) or not event.get("type", "").strip():
        errors.append("field 'type' must be a non-empty string")

    for string_key in ["details", "status"]:
        if string_key in event and (
            not isinstance(event[string_key], str) or not event[string_key].strip()
        ):
            errors.append(f"field '{string_key}' must be a non-empty string when present")

    if "context_status" in event:
        context_status = event.get("context_status")
        if not isinstance(context_status, str) or context_status not in CONTEXT_STATUSES:
            allowed = ", ".join(sorted(CONTEXT_STATUSES))
            errors.append(f"field 'context_status' must be one of: {allowed}")

    if "agent" in event:
        agent = event.get("agent")
        if not isinstance(agent, dict):
            errors.append("field 'agent' must be an object")
        else:
            for agent_key in ["name", "model", "session"]:
                value = agent.get(agent_key)
                if value is not None and (
                    not isinstance(value, str) or not value.strip()
                ):
                    errors.append(
                        f"field 'agent.{agent_key}' must be a non-empty string when present"
                    )
    if "git" in event:
        git = event.get("git")
        if not isinstance(git, dict):
            errors.append("field 'git' must be an object")
        else:
            branch = git.get("branch")
            if branch is not None and (not isinstance(branch, str) or not branch.strip()):
                errors.append("field 'git.branch' must be a non-empty string when present")
            commit = git.get("commit")
            if commit is not None and (not isinstance(commit, str) or not commit.strip()):
                errors.append("field 'git.commit' must be a non-empty string when present")
            detached = git.get("detached")
            if detached is not None and not isinstance(detached, bool):
                errors.append("field 'git.detached' must be a boolean when present")
            worktree = git.get("worktree")
            if worktree is not None and (not isinstance(worktree, str) or not worktree.strip()):
                errors.append("field 'git.worktree' must be a non-empty string when present")
    for list_key in LIST_FIELDS:
        if list_key not in event:
            continue
        value = event[list_key]
        if not isinstance(value, list):
            errors.append(f"field '{list_key}' must be a list")
            continue
        for index, item in enumerate(value):
            if not isinstance(item, str) or not item.strip():
                errors.append(
                    f"field '{list_key}[{index}]' must be a non-empty string"
                )
    return errors


def action_reference(event: dict[str, Any], index: int) -> str:
    event_id = str(event.get("id", "")).strip()
    if not event_id or index < 0:
        raise ValueError("Cannot create an action reference without an event id and index")
    return f"{event_id}#next:{index + 1}"


def event_location(event: dict[str, Any]) -> str:
    return str(event.get("__path") or f"event {event.get('id', '<unknown>')}")


def validate_event_collection(events: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    ids: dict[str, dict[str, Any]] = {}
    known_references: set[str] = set()

    for event in events:
        location = event_location(event)
        for error in validate_event(event):
            errors.append(f"{location}: {error}")

        event_id = event.get("id")
        if not isinstance(event_id, str) or not event_id.strip():
            continue
        event_id = event_id.strip()
        if event_id in ids:
            errors.append(
                f"{location}: duplicate event id '{event_id}' "
                f"(first seen in {event_location(ids[event_id])})"
            )
        else:
            ids[event_id] = event
        known_references.add(event_id)

        actions = event.get("next_actions")
        if isinstance(actions, list):
            for index, action in enumerate(actions):
                if isinstance(action, str) and action.strip():
                    known_references.add(action_reference(event, index))

    for event in events:
        event_id = event.get("id")
        location = event_location(event)
        for relation in RELATION_FIELDS:
            targets = event.get(relation)
            if not isinstance(targets, list):
                continue
            for target in targets:
                if not isinstance(target, str) or not target.strip():
                    continue
                normalized = target.strip()
                if isinstance(event_id, str) and (
                    normalized == event_id or normalized.startswith(f"{event_id}#")
                ):
                    errors.append(f"{location}: field '{relation}' cannot target itself")
                elif normalized not in known_references:
                    errors.append(
                        f"{location}: field '{relation}' references unknown id '{normalized}'"
                    )

    return errors


def validate(args: argparse.Namespace) -> int:
    p = paths()
    events, parse_errors = load_events(p)
    errors = [*parse_errors, *validate_support_files(p), *validate_event_collection(events)]

    if errors:
        print("Handoff validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Handoff validation passed: {len(events)} event(s)")
    return 0


def ordered_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(events, key=event_sort_key)


def relation_targets(events: list[dict[str, Any]]) -> set[str]:
    targets: set[str] = set()
    for event in events:
        for relation in RELATION_FIELDS:
            values = event.get(relation)
            if isinstance(values, list):
                targets.update(
                    value.strip()
                    for value in values
                    if isinstance(value, str) and value.strip()
                )
    return targets


def sessions_match(start: dict[str, Any], end: dict[str, Any]) -> bool:
    if event_context_key(start) != event_context_key(end):
        return False
    start_agent = start.get("agent") if isinstance(start.get("agent"), dict) else {}
    end_agent = end.get("agent") if isinstance(end.get("agent"), dict) else {}
    start_session = str(start_agent.get("session", "")).strip()
    end_session = str(end_agent.get("session", "")).strip()
    if start_session and end_session:
        return start_session == end_session
    start_name = str(start_agent.get("name", "")).strip()
    end_name = str(end_agent.get("name", "")).strip()
    return bool(start_name and start_name == end_name)


def closed_references(events: list[dict[str, Any]]) -> set[str]:
    closed = relation_targets(events)
    open_sessions: list[dict[str, Any]] = []

    for event in ordered_events(events):
        event_id = str(event.get("id", "")).strip()
        if not event_id:
            continue
        if event.get("type") == "session_start":
            if event_id not in closed:
                open_sessions.append(event)
            continue
        if event.get("type") != "session_end":
            continue
        for index in range(len(open_sessions) - 1, -1, -1):
            candidate = open_sessions[index]
            candidate_id = str(candidate.get("id", "")).strip()
            if candidate_id in closed:
                open_sessions.pop(index)
                continue
            if sessions_match(candidate, event):
                closed.add(candidate_id)
                open_sessions.pop(index)
                break

    return closed


def closed_context_keys(events: list[dict[str, Any]]) -> set[str]:
    states: dict[str, str] = {}
    for event in ordered_events(events):
        context_status = event.get("context_status")
        if isinstance(context_status, str) and context_status in CONTEXT_STATUSES:
            states[event_context_key(event)] = context_status
    return {
        context
        for context, context_status in states.items()
        if context_status in TERMINAL_CONTEXT_STATUSES
    }


def event_is_open(
    event: dict[str, Any],
    closed: set[str],
    closed_contexts: set[str],
) -> bool:
    event_id = str(event.get("id", "")).strip()
    status = str(event.get("status", "")).strip().lower()
    return (
        bool(event_id)
        and event_id not in closed
        and status not in TERMINAL_STATUSES
        and event_context_key(event) not in closed_contexts
    )


def event_line(event: dict[str, Any], *, include_reference: bool = False) -> str:
    ts = str(event.get("ts", "unknown-time"))
    event_type = str(event.get("type", "event"))
    summary = str(event.get("summary", "")).strip()
    context = event_context_label(event)
    reference = str(event.get("id", "")).strip()
    suffix = f" <!-- handoff-ref: {reference} -->" if include_reference and reference else ""
    return f"- `{ts}` [{context}] **{event_type}** — {summary}{suffix}"


def section_for(
    events: list[dict[str, Any]],
    types: set[str],
    limit: int = 8,
    *,
    hide_closed_contexts: bool = True,
) -> list[str]:
    closed = closed_references(events)
    closed_contexts = closed_context_keys(events) if hide_closed_contexts else set()
    selected = [
        event
        for event in reversed(ordered_events(events))
        if event.get("type") in types and event_is_open(event, closed, closed_contexts)
    ]
    if not selected:
        return ["- None recorded."]
    return [event_line(event, include_reference=True) for event in selected[:limit]]


def collect_next_actions(events: list[dict[str, Any]], limit: int = 10) -> list[str]:
    actions: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str]] = set()
    closed = closed_references(events)
    closed_contexts = closed_context_keys(events)
    for event in reversed(ordered_events(events)):
        if not event_is_open(event, closed, closed_contexts):
            continue
        for index, action in enumerate(event.get("next_actions", []) or []):
            if isinstance(action, str):
                normalized = action.strip()
                context_key = event_context_key(event)
                key = (context_key, normalized.lower())
                reference = action_reference(event, index)
                if normalized and key not in seen and reference not in closed:
                    actions.append((event_context_label(event), normalized, reference))
                    seen.add(key)
            if len(actions) >= limit:
                return [
                    f"- [{context}] {action} <!-- handoff-ref: {reference} -->"
                    for context, action, reference in actions
                ]
    if actions:
        return [
            f"- [{context}] {action} <!-- handoff-ref: {reference} -->"
            for context, action, reference in actions
        ]
    return ["- None recorded."]


def collect_files(events: list[dict[str, Any]], limit: int = 12) -> list[str]:
    files: list[str] = []
    seen: set[str] = set()
    for event in reversed(events):
        for file_name in event.get("files", []) or []:
            if isinstance(file_name, str):
                normalized = file_name.strip()
                if normalized and normalized not in seen:
                    files.append(normalized)
                    seen.add(normalized)
            if len(files) >= limit:
                return [f"- `{file_name}`" for file_name in files]
    if files:
        return [f"- `{file_name}`" for file_name in files]
    return ["- None recorded."]


def latest_state(events: list[dict[str, Any]], limit: int = 12) -> list[str]:
    if not events:
        return ["- No handoff events yet."]
    closed_contexts = closed_context_keys(events)
    latest_by_context: dict[str, dict[str, Any]] = {}
    for event in ordered_events(events):
        context = event_context_key(event)
        if context not in closed_contexts:
            latest_by_context[context] = event
    latest = sorted(
        latest_by_context.values(),
        key=event_sort_key,
        reverse=True,
    )
    if not latest:
        return ["- No active branch or worktree contexts recorded."]
    return [event_line(event) for event in latest[:limit]]


def render_markdown(args: argparse.Namespace) -> int:
    p = paths()
    p.handoff_dir.mkdir(parents=True, exist_ok=True)
    p.events_dir.mkdir(parents=True, exist_ok=True)

    events, parse_errors = load_events(p)
    errors = [
        *parse_errors,
        *validate_support_files(p),
        *validate_event_collection(events),
    ]
    if errors:
        raise ValueError(
            "Cannot render an invalid handoff journal:\n- " + "\n- ".join(errors)
        )
    config = read_config(p)
    limit = args.limit if args.limit is not None else int(config.get("max_recent_events_in_markdown", 20))
    if limit < 0:
        raise ValueError("Render limit must be a non-negative integer")
    recent = list(reversed(events))[:limit]

    lines: list[str] = [
        "# Handoff",
        "",
        "> Generated from `.handoff/events/**.jsonl`. Keep this file compact. Resolve active-item references through new journal events. If this file conflicts, regenerate it from the merged journal.",
        "",
        "## Latest state by active branch / worktree",
        "",
        *latest_state(events),
        "",
        "## Active work",
        "",
        *section_for(events, {"session_start", "plan", "todo"}),
        "",
        "## Decisions",
        "",
        *section_for(events, {"decision"}, hide_closed_contexts=False),
        "",
        "## Blockers / risks",
        "",
        *section_for(events, {"blocker", "risk", "question"}),
        "",
        "## Validation status",
        "",
        *section_for(events, {"validation"}, hide_closed_contexts=False),
        "",
        "## Next actions",
        "",
        *collect_next_actions(events),
        "",
        "## Recently changed / important files",
        "",
        *collect_files(events),
        "",
        "## Recent event journal",
        "",
    ]

    if recent:
        lines.extend(event_line(event) + f" (`{event.get('__path', '')}`)" for event in recent)
    else:
        lines.append("- None recorded.")

    lines.append("")
    p.handoff_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Rendered {p.handoff_md.relative_to(p.root)}")
    return 0


def status(args: argparse.Namespace) -> int:
    p = paths()
    events, parse_errors = load_events(p)
    errors = [
        *parse_errors,
        *validate_support_files(p),
        *validate_event_collection(events),
    ]
    current_git = git_metadata(p.root)
    current_context = event_context_label({"git": current_git}) if current_git else "no Git context"
    current_key = event_context_key({"git": current_git}) if current_git else "no-git-context"
    print(f"Repo: {p.root}")
    print(f"Context: {current_context}")
    print(f"HANDOFF.md: {'yes' if p.handoff_md.exists() else 'no'}")
    print(f"Events: {len(events)}")
    if events:
        current_events = [event for event in events if event_context_key(event) == current_key]
        latest = current_events[-1] if current_events else events[-1]
        label = "Latest in current context" if current_events else "Latest project event"
        print(f"{label}: {latest.get('ts')} {latest.get('type')} - {latest.get('summary')}")
    closed = closed_references(events)
    closed_contexts = closed_context_keys(events)
    open_blockers = [
        event
        for event in events
        if event.get("type") in {"blocker", "risk", "question"}
        and event_is_open(event, closed, closed_contexts)
    ]
    if open_blockers:
        print("Unresolved blockers/risks/questions:")
        for event in list(reversed(open_blockers))[:5]:
            print(f"{event_line(event)} (ref: {event.get('id')})")
    next_actions = collect_next_actions(events, limit=5)
    if next_actions != ["- None recorded."]:
        print("Open next actions:")
        for action in next_actions:
            print(action.replace(" <!-- handoff-ref: ", " (ref: ").replace(" -->", ")"))
    if errors:
        print("Validation warnings:")
        for error in errors[:10]:
            print(f"- {error}")
    return 0


def tail(args: argparse.Namespace) -> int:
    p = paths()
    events, errors = load_events(p)
    for event in list(reversed(events))[: args.limit]:
        print(json.dumps({k: v for k, v in event.items() if k != "__path"}, sort_keys=True))
    if errors:
        print("Parse warnings:", file=sys.stderr)
        for error in errors[:10]:
            print(f"- {error}", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Repo-local handoff helper")
    sub = parser.add_subparsers(dest="command", required=True)

    init_parser = sub.add_parser("init", help="Create HANDOFF.md and .handoff/ structure")
    init_parser.add_argument("--force", action="store_true", help="Overwrite existing template/config/schema files")
    init_parser.set_defaults(func=init_repo)

    add_parser = sub.add_parser("add", help="Append one handoff event to its contextual JSONL journal file")
    add_parser.add_argument("--type", required=True, help="Event type")
    add_parser.add_argument("--summary", required=True, help="Short event summary")
    add_parser.add_argument("--details", help="Concise details")
    add_parser.add_argument("--status", help="Optional status value")
    add_parser.add_argument(
        "--context-status",
        choices=sorted(CONTEXT_STATUSES),
        help="Mark the current branch/worktree context active, closed, merged, or abandoned",
    )
    add_parser.add_argument("--scope", action="append", help="Scope path/list; can be repeated or comma-separated")
    add_parser.add_argument("--file", action="append", help="Relevant file path; can be repeated or comma-separated")
    add_parser.add_argument("--tag", action="append", help="Tag; can be repeated or comma-separated")
    add_parser.add_argument("--next", action="append", help="Next action; can be repeated or comma-separated")
    add_parser.add_argument(
        "--resolve",
        action="append",
        help="Event or action reference resolved by this event; can be repeated",
    )
    add_parser.add_argument(
        "--supersede",
        action="append",
        help="Event or action reference superseded by this event; can be repeated",
    )
    add_parser.add_argument("--agent", help="Agent/tool name (required unless HANDOFF_AGENT is set)")
    add_parser.add_argument("--model", help="Model name")
    add_parser.add_argument("--session", help="Session id")
    add_parser.add_argument("--render", action="store_true", help="Render HANDOFF.md after adding the event")
    add_parser.add_argument("--allow-custom-type", action="store_true", help="Allow event types outside the recommended set")
    add_parser.set_defaults(func=add_event)

    render_parser = sub.add_parser("render", help="Regenerate HANDOFF.md from event journal")
    render_parser.add_argument("--limit", type=int, help="Recent event count for HANDOFF.md")
    render_parser.set_defaults(func=render_markdown)

    validate_parser = sub.add_parser(
        "validate", help="Validate JSONL events and handoff configuration"
    )
    validate_parser.set_defaults(func=validate)

    status_parser = sub.add_parser("status", help="Print compact handoff status")
    status_parser.set_defaults(func=status)

    tail_parser = sub.add_parser("tail", help="Print recent events as JSONL")
    tail_parser.add_argument("--limit", type=int, default=20)
    tail_parser.set_defaults(func=tail)

    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
