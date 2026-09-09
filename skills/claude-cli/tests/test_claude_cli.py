"""Offline transport tests. Model responses are fixtures, not live validation."""
from __future__ import annotations
import contextlib
import io
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
import uuid

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import ask_claude
import cli_runtime as runtime

SESSION = "12345678-1234-4123-8123-123456789abc"


def result(**overrides):
    data = {"type": "result", "subtype": "success", "is_error": False,
            "result": "A verified fixture result.", "session_id": SESSION}
    data.update(overrides)
    return data


class ClaudeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="claude-cli-test-")
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)

    def test_parse_success(self):
        self.assertEqual(SESSION, runtime.parse_claude(result())["session_id"])

    def test_parse_keeps_unknown_usage_unknown(self):
        self.assertIsNone(runtime.parse_claude(result())["usage"])
        self.assertIsNone(runtime.parse_claude(result())["reported_cost_usd"])

    def test_parse_ignores_unknown_fields(self):
        self.assertEqual(SESSION, runtime.parse_claude(result(future_field={"foo": True}))["session_id"])

    def test_array_is_not_terminal_result(self):
        with self.assertRaises(runtime.CliError):
            runtime.parse_claude([result()])

    def test_wrong_type_is_failure(self):
        with self.assertRaises(runtime.CliError):
            runtime.parse_claude(result(type="assistant"))

    def test_error_is_failure_even_with_text(self):
        with self.assertRaises(runtime.CliError):
            runtime.parse_claude(result(is_error=True))

    def test_turn_cap_is_incomplete(self):
        with self.assertRaises(runtime.CliError):
            runtime.parse_claude(result(subtype="error_max_turns"))

    def test_unknown_stop_reason_fails_closed(self):
        with self.assertRaises(runtime.CliError):
            runtime.parse_claude(result(stop_reason="new_incomplete_reason"))

    def test_permission_denials_are_not_clean_success(self):
        with self.assertRaises(runtime.CliError):
            runtime.parse_claude(result(permission_denials=[{"tool_name": "Read"}]))

    def test_missing_error_marker_is_not_assumed_success(self):
        payload = result()
        del payload["is_error"]
        with self.assertRaises(runtime.CliError):
            runtime.parse_claude(payload)

    def test_missing_session_is_failure(self):
        with self.assertRaises(runtime.CliError):
            runtime.parse_claude(result(session_id=None))

    def test_mismatched_resume_is_failure(self):
        with self.assertRaises(runtime.CliError):
            runtime.parse_claude(result(), str(uuid.uuid4()))

    def test_blank_result_is_failure(self):
        with self.assertRaises(runtime.CliError):
            runtime.parse_claude(result(result=" \n"))

    def test_names_and_latest_are_rejected(self):
        for candidate in ["latest", "project-session", "", "--continue", "1234"]:
            with self.subTest(candidate=candidate), self.assertRaises(runtime.CliError):
                runtime.exact_session(candidate)

    def test_consult_profile_preserves_subscription_login_surface(self):
        command = runtime.claude_command("claude")
        self.assertIn("-p", command)
        self.assertIn("--safe-mode", command)
        self.assertNotIn("--bare", command)
        self.assertEqual("", command[command.index("--tools") + 1])
        self.assertIn("--strict-mcp-config", command)

    def test_read_profile_has_no_shell_edit_web_or_agent(self):
        command = runtime.claude_command("claude", tools="read")
        self.assertEqual("Read,Glob,Grep", command[command.index("--tools") + 1])
        self.assertNotIn("Bash", command)

    def test_explicit_model_effort_and_session(self):
        command = runtime.claude_command("claude", session_id=SESSION, model="configured-model", effort="high")
        self.assertEqual(SESSION, command[command.index("--resume") + 1])
        self.assertIn("configured-model", command)

    def test_bad_model_flags_rejected(self):
        with self.assertRaises(runtime.CliError):
            runtime.claude_command("claude", model="--dangerously-skip-permissions")

    def test_invalid_turn_count_rejected(self):
        for count in [0, -1, 51]:
            with self.subTest(count=count), self.assertRaises(runtime.CliError):
                runtime.claude_command("claude", max_turns=count)

    def test_unicode_is_preserved(self):
        text = "Café\n∑∞\n---\n"
        file = self.base / "input.txt"
        file.write_text(text, encoding="utf-8")
        self.assertEqual(text, runtime.read_text(file))

    def test_size_limit_is_in_bytes(self):
        with self.assertRaises(runtime.CliError):
            runtime.checked_text("é" * 10, 10)

    def test_nul_rejected(self):
        with self.assertRaises(runtime.CliError):
            runtime.checked_text("hi\0there")

    def test_nan_timeout_rejected(self):
        with self.assertRaises(runtime.CliError):
            runtime.positive_number(float("nan"), "timeout")

    def test_invalid_utf8_rejected(self):
        path = self.base / "input.txt"
        path.write_bytes(b"\xff")
        with self.assertRaises(runtime.CliError):
            runtime.read_text(path)

    def test_nonfinite_json_rejected(self):
        path = self.base / "x.json"
        path.write_text('{"value": NaN}')
        with self.assertRaises(runtime.CliError):
            runtime.read_json(path)

    @unittest.skipUnless(os.name == "posix", "POSIX FIFO")
    def test_fifo_does_not_block(self):
        path = self.base / "fifo"
        os.mkfifo(path)
        with self.assertRaises(runtime.CliError):
            runtime.read_text(path)

    @unittest.skipUnless(os.name == "posix", "POSIX symlink")
    def test_atomic_write_refuses_symlink(self):
        target = self.base / "owned-by-user"
        target.write_text("original")
        path = self.base / "output.txt"
        path.symlink_to(target)
        with self.assertRaises(runtime.CliError):
            runtime.atomic_text(path, "changed")
        self.assertEqual("original", target.read_text())

    def test_atomic_json_round_trip(self):
        path = self.base / "state.json"
        runtime.atomic_json(path, {"unicode": "Café"})
        self.assertEqual({"unicode": "Café"}, runtime.read_json(path))

    def test_missing_binary_is_actionable(self):
        with self.assertRaises(runtime.CliError):
            runtime.executable("there-is-no-such-cli-abcdef123")

    def test_stdout_and_stderr_remain_separate(self):
        outcome = runtime.run_process([sys.executable, "-S", "-c", 'import sys;print("hello");print("warning",file=sys.stderr)'], cwd=self.base, directory=self.base)
        self.assertEqual(0, outcome["returncode"])
        self.assertEqual("hello\n", (self.base / "stdout.json").read_text())
        self.assertEqual("warning\n", (self.base / "stderr.log").read_text())

    def test_prompt_file_goes_to_stdin_without_shell_parsing(self):
        file = self.base / "prompt.txt"
        text = "$(touch /tmp/not-executed) ; echo 'hello'\n∑∞"
        file.write_text(text)
        runtime.run_process([sys.executable, "-S", "-c", 'import sys;sys.stdout.write(sys.stdin.read())'], cwd=self.base, directory=self.base, input_file=file)
        self.assertEqual(text, (self.base / "stdout.json").read_text())

    def test_timeout_kills_owned_process(self):
        outcome = runtime.run_process([sys.executable, "-S", "-c", 'import time;time.sleep(30)'], cwd=self.base, directory=self.base, timeout=0.1)
        self.assertEqual("timeout", outcome["failure"])
        self.assertNotEqual(0, outcome["returncode"])

    def test_output_limit_stops_call(self):
        outcome = runtime.run_process([sys.executable, "-S", "-c", 'print("x" * 100000)'], cwd=self.base, directory=self.base, output_limit=1024)
        self.assertEqual("output_limit", outcome["failure"])

    def test_no_result_is_accepted_after_nonzero_exit(self):
        runtime.run_process([sys.executable, "-S", "-c", 'import sys;print("{}");sys.exit(2)'], cwd=self.base, directory=self.base)
        with self.assertRaises(runtime.CliError):
            runtime.completed_payload(self.base)

    @unittest.skipUnless(os.name == "posix", "POSIX process groups")
    def test_timeout_also_kills_owned_descendant(self):
        marker = self.base / "descendant-survived"
        child = 'import signal,time,pathlib;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(0.7);pathlib.Path(' + repr(str(marker)) + ').write_text("bad")'
        parent = 'import subprocess,sys,time;subprocess.Popen([sys.executable,"-S","-c",' + repr(child) + ']);time.sleep(30)'
        runtime.run_process([sys.executable, "-S", "-c", parent], cwd=self.base, directory=self.base, timeout=0.2)
        time.sleep(0.8)
        self.assertFalse(marker.exists())

    @unittest.skipUnless(os.name == "posix", "POSIX locks")
    def test_concurrent_writer_rejected(self):
        path = self.base / ".lock"
        with runtime.exclusive_lock(path):
            with self.assertRaises(runtime.CliError):
                with runtime.exclusive_lock(path):
                    self.fail("Unexpected second writer")
        with runtime.exclusive_lock(path):
            pass
        self.assertTrue(path.exists())

    def test_wrapper_end_to_end(self):
        # A local executable fixture. It records the exact stdin and emits a
        # deterministic result, without importing anything from the other skill.
        binary = self.base / "claude-fixture"
        source = '#!' + sys.executable + ' -S\nimport sys,json\nprompt=sys.stdin.read()\nprint(json.dumps(' + repr(result()) + '))\n'
        binary.write_text(source)
        binary.chmod(0o700)
        prompt = self.base / "prompt.md"
        prompt.write_text("Review this argument.")
        out = self.base / "call"
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(io.StringIO()):
            code = ask_claude.main(["ask", "--claude-bin", str(binary), "--cwd", str(self.base), "--prompt-file", str(prompt), "--out-dir", str(out)])
        self.assertEqual(0, code)
        self.assertEqual(SESSION, json.loads(stdout.getvalue())["session_id"])
        self.assertTrue((out / "result.json").exists())
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(1, ask_claude.main(["ask", "--claude-bin", str(binary), "--prompt-file", str(prompt), "--out-dir", str(out)]))


if __name__ == "__main__":
    unittest.main()
