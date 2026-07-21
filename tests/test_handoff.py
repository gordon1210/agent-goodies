from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
HANDOFF_SCRIPT = REPO_ROOT / "skills" / "handoff" / "scripts" / "handoff.py"


def load_handoff_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("handoff_under_test", HANDOFF_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {HANDOFF_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


HANDOFF = load_handoff_module()


class HandoffPathTests(unittest.TestCase):
    def event(
        self,
        *,
        branch: str | None = None,
        worktree: str = "main",
        detached: bool = False,
    ) -> dict[str, Any]:
        git: dict[str, Any] = {
            "commit": "90daa453930d6de8fdaad6901da175264922012e",
            "worktree": worktree,
        }
        if branch:
            git["branch"] = branch
        if detached:
            git["detached"] = True
        return {
            "v": 1,
            "id": branch or worktree,
            "ts": "2026-07-20T12:00:00Z",
            "type": "change",
            "summary": "Changed something",
            "agent": {"name": "codex"},
            "git": git,
        }

    def test_lossless_branch_encoding_keeps_similar_refs_distinct(self) -> None:
        slash = HANDOFF.branch_filename_token("feature/foo")
        hyphen = HANDOFF.branch_filename_token("feature-foo")

        self.assertEqual(slash, "feature%2Ffoo")
        self.assertEqual(hyphen, "feature-foo")
        self.assertNotEqual(slash, hyphen)

    def test_attached_worktrees_at_same_commit_use_distinct_branch_batches(self) -> None:
        slash = HANDOFF.event_batch_path(None, self.event(branch="feature/foo"))
        hyphen = HANDOFF.event_batch_path(None, self.event(branch="feature-foo"))

        self.assertNotEqual(slash, hyphen)
        self.assertIn("feature%2Ffoo", slash.name)
        self.assertIn("feature-foo", hyphen.name)

    def test_detached_worktrees_at_same_commit_use_distinct_batches(self) -> None:
        first = HANDOFF.event_batch_path(
            None,
            self.event(worktree="detached-a", detached=True),
        )
        second = HANDOFF.event_batch_path(
            None,
            self.event(worktree="detached-b", detached=True),
        )

        self.assertNotEqual(first, second)
        self.assertIn("detached-detached-a", first.name)
        self.assertIn("detached-detached-b", second.name)

    def test_current_state_keeps_one_latest_event_per_branch(self) -> None:
        events = [
            self.event(branch="feature/foo"),
            self.event(branch="feature-foo")
            | {"ts": "2026-07-20T12:00:01Z", "summary": "Other branch"},
        ]

        rendered = "\n".join(HANDOFF.latest_state(events))

        self.assertIn("[feature/foo]", rendered)
        self.assertIn("[feature-foo]", rendered)

    def test_custom_event_types_remain_valid(self) -> None:
        event = self.event(branch="main") | {"type": "custom-event"}

        self.assertEqual(HANDOFF.validate_event(event), [])

    def test_validation_rejects_malformed_required_and_list_fields(self) -> None:
        event = self.event(branch="main") | {
            "id": "",
            "ts": "not-a-date",
            "scope": [42],
        }

        errors = HANDOFF.validate_event(event)

        self.assertTrue(any("'id'" in error for error in errors))
        self.assertTrue(any("'ts'" in error for error in errors))
        self.assertTrue(any("scope" in error for error in errors))


class HandoffLifecycleTests(unittest.TestCase):
    def event(
        self,
        event_id: str,
        timestamp: str,
        event_type: str,
        summary: str,
        *,
        branch: str = "feature/demo",
        **extra: Any,
    ) -> dict[str, Any]:
        event: dict[str, Any] = {
            "v": 1,
            "id": event_id,
            "ts": timestamp,
            "type": event_type,
            "summary": summary,
            "agent": {"name": "codex", "session": "session-1"},
            "git": {
                "branch": branch,
                "commit": "90daa453930d6de8fdaad6901da175264922012e",
                "worktree": "demo",
            },
        }
        event.update(extra)
        return event

    def test_session_end_closes_matching_session_start(self) -> None:
        events = [
            self.event(
                "session-start",
                "2026-07-20T10:00:00Z",
                "session_start",
                "Started implementation",
            ),
            self.event(
                "session-end",
                "2026-07-20T11:00:00Z",
                "session_end",
                "Finished implementation",
            ),
        ]

        rendered = "\n".join(
            HANDOFF.section_for(events, {"session_start", "status", "plan"})
        )

        self.assertNotIn("Started implementation", rendered)
        self.assertIn("None recorded", rendered)

    def test_resolved_blocker_is_omitted(self) -> None:
        events = [
            self.event(
                "blocker-1",
                "2026-07-20T10:00:00Z",
                "blocker",
                "CI is unavailable",
                status="open",
            ),
            self.event(
                "resolution-1",
                "2026-07-20T11:00:00Z",
                "status",
                "CI recovered",
                status="resolved",
                resolves=["blocker-1"],
            ),
        ]

        rendered = "\n".join(
            HANDOFF.section_for(events, {"blocker", "risk", "question"})
        )

        self.assertNotIn("CI is unavailable", rendered)
        self.assertIn("None recorded", rendered)

    def test_completed_next_action_is_omitted(self) -> None:
        plan = self.event(
            "plan-1",
            "2026-07-20T10:00:00Z",
            "plan",
            "Implement feature",
            next_actions=["Run tests", "Write release notes"],
        )
        events = [
            plan,
            self.event(
                "validation-1",
                "2026-07-20T11:00:00Z",
                "validation",
                "Tests passed",
                resolves=[HANDOFF.action_reference(plan, 0)],
            ),
        ]

        rendered = "\n".join(HANDOFF.collect_next_actions(events))

        self.assertNotIn("Run tests", rendered)
        self.assertIn("Write release notes", rendered)

    def test_superseded_decision_is_omitted(self) -> None:
        events = [
            self.event(
                "decision-1",
                "2026-07-20T10:00:00Z",
                "decision",
                "Use the old format",
            ),
            self.event(
                "decision-2",
                "2026-07-20T11:00:00Z",
                "decision",
                "Use the new format",
                supersedes=["decision-1"],
            ),
        ]

        rendered = "\n".join(
            HANDOFF.section_for(
                events,
                {"decision"},
                hide_closed_contexts=False,
            )
        )

        self.assertNotIn("old format", rendered)
        self.assertIn("new format", rendered)

    def test_closed_context_is_omitted_from_latest_state(self) -> None:
        events = [
            self.event(
                "old-status",
                "2026-07-20T10:00:00Z",
                "status",
                "Feature underway",
                branch="feature/old",
            ),
            self.event(
                "old-closed",
                "2026-07-20T11:00:00Z",
                "status",
                "Feature merged",
                branch="feature/old",
                context_status="merged",
            ),
            self.event(
                "main-status",
                "2026-07-20T12:00:00Z",
                "status",
                "Work continues",
                branch="main",
            ),
        ]

        rendered = "\n".join(HANDOFF.latest_state(events))

        self.assertNotIn("feature/old", rendered)
        self.assertIn("[main]", rendered)


class HandoffWorktreeIntegrationTests(unittest.TestCase):
    def run_command(
        self,
        args: list[str],
        *,
        cwd: Path,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            args,
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True,
        )

    def git(
        self,
        repo: Path,
        *args: str,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        return self.run_command(["git", *args], cwd=repo, check=check)

    def handoff(
        self,
        repo: Path,
        *args: str,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        return self.run_command(
            [sys.executable, str(HANDOFF_SCRIPT), *args],
            cwd=repo,
            check=check,
        )

    def initialize_repo(self, root: Path) -> Path:
        repo = root / "repo"
        self.run_command(["git", "init", "--initial-branch=main", str(repo)], cwd=root)
        self.git(repo, "config", "user.name", "Handoff Test")
        self.git(repo, "config", "user.email", "handoff@example.invalid")
        self.git(repo, "config", "commit.gpgsign", "false")
        (repo / "README.md").write_text("# Test repository\n", encoding="utf-8")
        self.git(repo, "add", "README.md")
        self.git(repo, "commit", "-m", "Initial commit")
        self.handoff(repo, "init")
        self.git(repo, "add", "HANDOFF.md", ".handoff")
        self.git(repo, "commit", "-m", "Initialize handoff")
        return repo

    def add_event(self, worktree: Path, summary: str, *, render: bool = False) -> None:
        args = [
            "add",
            "--type",
            "change",
            "--summary",
            summary,
            "--agent",
            "codex",
        ]
        if render:
            args.append("--render")
        self.handoff(worktree, *args)

    def read_only_event(self, worktree: Path) -> tuple[Path, dict[str, Any]]:
        event_files = list((worktree / ".handoff" / "events").rglob("*.jsonl"))
        self.assertEqual(len(event_files), 1)
        event_file = event_files[0]
        event = json.loads(event_file.read_text(encoding="utf-8").strip())
        return event_file, event

    def test_parallel_branches_merge_journals_and_rerender_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            repo = self.initialize_repo(root)
            base_commit = self.git(repo, "rev-parse", "HEAD").stdout.strip()
            slash_worktree = root / "slash-worktree"
            hyphen_worktree = root / "hyphen-worktree"
            self.git(repo, "worktree", "add", "-b", "feature/foo", str(slash_worktree), base_commit)
            self.git(repo, "worktree", "add", "-b", "feature-foo", str(hyphen_worktree), base_commit)

            self.add_event(slash_worktree, "Slash branch", render=True)
            self.add_event(hyphen_worktree, "Hyphen branch", render=True)

            slash_file, slash_event = self.read_only_event(slash_worktree)
            hyphen_file, hyphen_event = self.read_only_event(hyphen_worktree)
            self.assertNotEqual(slash_file.name, hyphen_file.name)
            self.assertIn("feature%2Ffoo", slash_file.name)
            self.assertIn("feature-foo", hyphen_file.name)
            self.assertEqual(slash_event["git"]["branch"], "feature/foo")
            self.assertEqual(hyphen_event["git"]["branch"], "feature-foo")
            self.assertEqual(slash_event["git"]["commit"], base_commit)
            self.assertEqual(hyphen_event["git"]["commit"], base_commit)

            self.git(slash_worktree, "add", "HANDOFF.md", ".handoff/events")
            self.git(slash_worktree, "commit", "-m", "Record slash branch handoff")
            self.git(hyphen_worktree, "add", "HANDOFF.md", ".handoff/events")
            self.git(hyphen_worktree, "commit", "-m", "Record hyphen branch handoff")

            self.git(repo, "merge", "--no-ff", "--no-edit", "feature/foo")
            second_merge = self.git(
                repo,
                "merge",
                "--no-ff",
                "--no-edit",
                "feature-foo",
                check=False,
            )
            if second_merge.returncode != 0:
                unresolved = self.git(repo, "diff", "--name-only", "--diff-filter=U").stdout.splitlines()
                self.assertEqual(unresolved, ["HANDOFF.md"])
                self.handoff(repo, "render")
                self.git(repo, "add", "HANDOFF.md")
                self.git(repo, "commit", "--no-edit")

            validation = self.handoff(repo, "validate")
            self.assertIn("2 event(s)", validation.stdout)
            rendered = (repo / "HANDOFF.md").read_text(encoding="utf-8")
            self.assertIn("[feature/foo]", rendered)
            self.assertIn("[feature-foo]", rendered)

    def test_detached_worktrees_at_same_commit_get_distinct_git_contexts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            repo = self.initialize_repo(root)
            base_commit = self.git(repo, "rev-parse", "HEAD").stdout.strip()
            first_worktree = root / "detached-a"
            second_worktree = root / "detached-b"
            self.git(repo, "worktree", "add", "--detach", str(first_worktree), base_commit)
            self.git(repo, "worktree", "add", "--detach", str(second_worktree), base_commit)

            self.add_event(first_worktree, "First detached worktree")
            self.add_event(second_worktree, "Second detached worktree")

            first_file, first_event = self.read_only_event(first_worktree)
            second_file, second_event = self.read_only_event(second_worktree)
            self.assertNotEqual(first_file.name, second_file.name)
            self.assertTrue(first_event["git"]["detached"])
            self.assertTrue(second_event["git"]["detached"])
            self.assertNotEqual(first_event["git"]["worktree"], second_event["git"]["worktree"])

    def test_copied_skill_bundle_needs_no_repository_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            installed_skill = root / "installed" / "handoff"
            project = root / "project"
            shutil.copytree(REPO_ROOT / "skills" / "handoff", installed_skill)
            project.mkdir()

            installed_script = installed_skill / "scripts" / "handoff.py"
            initialization = self.run_command(
                [sys.executable, str(installed_script), "init"],
                cwd=project,
            )

            self.assertIn("Initialized handoff files", initialization.stdout)
            self.assertTrue((project / "HANDOFF.md").is_file())
            self.assertTrue((project / ".handoff" / "schema.json").is_file())
            self.assertFalse((project / "package.json").exists())

    def test_invalid_event_is_rejected_before_append(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repo = Path(temporary_directory)
            self.handoff(repo, "init")

            result = self.handoff(
                repo,
                "add",
                "--type",
                "change",
                "--summary",
                "",
                "--agent",
                "codex",
                check=False,
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("summary", result.stderr)
            self.assertEqual(list((repo / ".handoff" / "events").rglob("*.jsonl")), [])

    def test_corrupt_config_fails_validation_and_rendering(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repo = Path(temporary_directory)
            self.handoff(repo, "init")
            original_handoff = (repo / "HANDOFF.md").read_text(encoding="utf-8")
            (repo / ".handoff" / "config.json").write_text("{broken", encoding="utf-8")

            validation = self.handoff(repo, "validate", check=False)
            rendering = self.handoff(repo, "render", check=False)

            self.assertEqual(validation.returncode, 1)
            self.assertIn("config.json", validation.stdout)
            self.assertEqual(rendering.returncode, 2)
            self.assertIn("config.json", rendering.stderr)
            self.assertEqual(
                (repo / "HANDOFF.md").read_text(encoding="utf-8"),
                original_handoff,
            )

    def test_duplicate_event_ids_fail_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repo = Path(temporary_directory)
            self.handoff(repo, "init")
            self.handoff(
                repo,
                "add",
                "--type",
                "change",
                "--summary",
                "Changed something",
                "--agent",
                "codex",
            )
            event_file = next((repo / ".handoff" / "events").rglob("*.jsonl"))
            event_line = event_file.read_text(encoding="utf-8")
            event_file.write_text(event_line + event_line, encoding="utf-8")

            validation = self.handoff(repo, "validate", check=False)

            self.assertEqual(validation.returncode, 1)
            self.assertIn("duplicate event id", validation.stdout)

    def test_session_end_records_and_renders_session_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repo = Path(temporary_directory)
            self.handoff(repo, "init")
            self.handoff(
                repo,
                "add",
                "--type",
                "session_start",
                "--summary",
                "Started implementation",
                "--agent",
                "codex",
                "--session",
                "session-1",
            )
            self.handoff(
                repo,
                "add",
                "--type",
                "session_end",
                "--summary",
                "Finished implementation",
                "--agent",
                "codex",
                "--session",
                "session-1",
                "--render",
            )

            events = [
                json.loads(line)
                for event_file in (repo / ".handoff" / "events").rglob("*.jsonl")
                for line in event_file.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            session_start = next(event for event in events if event["type"] == "session_start")
            session_end = next(event for event in events if event["type"] == "session_end")
            rendered = (repo / "HANDOFF.md").read_text(encoding="utf-8")

            self.assertIn(session_start["id"], session_end["resolves"])
            active_work = rendered.split("## Active work", 1)[1].split("## Decisions", 1)[0]
            self.assertIn("None recorded", active_work)
            self.assertNotIn("Started implementation", active_work)

    def test_cli_resolves_action_and_rejects_unknown_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repo = Path(temporary_directory)
            self.handoff(repo, "init")
            self.handoff(
                repo,
                "add",
                "--type",
                "plan",
                "--summary",
                "Implement feature",
                "--next",
                "Run tests",
                "--agent",
                "codex",
            )
            plan_file = next((repo / ".handoff" / "events").rglob("*.jsonl"))
            plan = json.loads(plan_file.read_text(encoding="utf-8").strip())
            action_ref = HANDOFF.action_reference(plan, 0)

            resolved = self.handoff(
                repo,
                "add",
                "--type",
                "validation",
                "--summary",
                "Tests passed",
                "--resolve",
                action_ref,
                "--agent",
                "codex",
                "--render",
            )
            rejected = self.handoff(
                repo,
                "add",
                "--type",
                "status",
                "--summary",
                "Invalid relation",
                "--resolve",
                "missing-event",
                "--agent",
                "codex",
                check=False,
            )
            rendered = (repo / "HANDOFF.md").read_text(encoding="utf-8")

            self.assertEqual(resolved.returncode, 0)
            next_actions = rendered.split("## Next actions", 1)[1].split(
                "## Recently changed", 1
            )[0]
            self.assertIn("None recorded", next_actions)
            self.assertNotIn("Run tests", next_actions)
            self.assertEqual(rejected.returncode, 2)
            self.assertIn("unknown id", rejected.stderr)


if __name__ == "__main__":
    unittest.main()
