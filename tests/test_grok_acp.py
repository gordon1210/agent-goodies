from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import os
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Dict, List, Optional


REPO_ROOT = Path(__file__).resolve().parents[1]
CLIENT_SCRIPT = REPO_ROOT / "skills" / "grok-cli" / "scripts" / "grok_acp.py"
FAKE_AGENT = REPO_ROOT / "tests" / "fixtures" / "fake_grok_acp_agent.py"


def load_client_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("grok_acp_under_test", CLIENT_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {CLIENT_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


CLIENT = load_client_module()


def readline_with_timeout(stream: Any, timeout: float = 3.0) -> str:
    result: "queue.Queue[str]" = queue.Queue(maxsize=1)
    thread = threading.Thread(target=lambda: result.put(stream.readline()), daemon=True)
    thread.start()
    try:
        return result.get(timeout=timeout)
    except queue.Empty as exc:
        raise AssertionError("Timed out waiting for subprocess output") from exc


def send_control_command(control_file: str, command: Dict[str, Any]) -> Dict[str, Any]:
    sent = subprocess.run(
        [
            sys.executable,
            str(CLIENT_SCRIPT),
            "send",
            "--control-file",
            control_file,
            "--json",
            json.dumps(command),
        ],
        text=True,
        capture_output=True,
        timeout=3,
        check=False,
    )
    if sent.returncode != 0:
        raise AssertionError(sent.stdout + sent.stderr)
    result = json.loads(sent.stdout)
    if result.get("sent") is not True:
        raise AssertionError(sent.stdout)
    return result


def read_until_events(
    stream: Any,
    events: List[Dict[str, Any]],
    required: set[str],
    timeout: float = 3.0,
) -> None:
    deadline = time.monotonic() + timeout
    while not required.issubset(
        {str(event.get("event")) for event in events}
    ):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise AssertionError(
                f"Timed out waiting for {sorted(required)!r}: {events!r}"
            )
        events.append(json.loads(readline_with_timeout(stream, remaining)))


class EventCollector:
    def __init__(self) -> None:
        self.events: List[Dict[str, Any]] = []
        self.condition = threading.Condition()

    def __call__(self, event: Dict[str, Any]) -> None:
        with self.condition:
            self.events.append(dict(event))
            self.condition.notify_all()

    def wait_for(
        self,
        event_name: str,
        predicate: Optional[Callable[[Dict[str, Any]], bool]] = None,
        timeout: float = 3.0,
    ) -> Dict[str, Any]:
        deadline = time.monotonic() + timeout
        with self.condition:
            while True:
                for event in self.events:
                    if event.get("event") != event_name:
                        continue
                    if predicate is None or predicate(event):
                        return event
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    self.fail_with_events(event_name)
                self.condition.wait(remaining)
        raise AssertionError("unreachable")

    def fail_with_events(self, event_name: str) -> None:
        rendered = json.dumps(self.events, indent=2, sort_keys=True)
        raise AssertionError(f"Timed out waiting for {event_name!r}. Events:\n{rendered}")


class GrokAcpBridgeTests(unittest.TestCase):
    def make_bridge(
        self,
        *,
        requested_session_id: Optional[str] = None,
        requested_auth_method: Optional[str] = None,
        permission_timeout: float = 1.0,
        startup_mode: str = "normal",
        max_message_bytes: int = CLIENT.DEFAULT_MAX_MESSAGE_BYTES,
    ) -> tuple[Any, EventCollector, List[str]]:
        events = EventCollector()
        stderr: List[str] = []
        env = os.environ.copy()
        env["FAKE_GROK_STARTUP"] = startup_mode
        connection = CLIENT.JsonRpcConnection(
            [sys.executable, str(FAKE_AGENT)],
            REPO_ROOT,
            env=env,
            max_message_bytes=max_message_bytes,
            stderr_callback=stderr.append,
        )
        bridge = CLIENT.GrokAcpBridge(
            connection,
            REPO_ROOT,
            events,
            requested_session_id=requested_session_id,
            requested_auth_method=requested_auth_method,
            startup_timeout=2.0,
            permission_timeout=permission_timeout,
            shutdown_timeout=1.0,
        )
        bridge.start()
        self.addCleanup(bridge.shutdown)
        return bridge, events, stderr

    def test_authenticates_advertised_default_before_creating_session(self) -> None:
        bridge, events, _stderr = self.make_bridge()

        ready = events.wait_for("ready")

        self.assertEqual(ready["authMethodId"], "cached_token")
        self.assertEqual(bridge.status_snapshot()["authMethodId"], "cached_token")

    def test_legacy_agent_without_auth_methods_remains_supported(self) -> None:
        bridge, events, _stderr = self.make_bridge(startup_mode="legacy-no-auth")

        ready = events.wait_for("ready")

        self.assertIsNone(ready["authMethodId"])
        self.assertIsNone(bridge.status_snapshot()["authMethodId"])

    def test_missing_default_auth_method_fails_without_interactive_login(self) -> None:
        events = EventCollector()
        env = os.environ.copy()
        env["FAKE_GROK_STARTUP"] = "auth-no-default"
        connection = CLIENT.JsonRpcConnection(
            [sys.executable, str(FAKE_AGENT)], REPO_ROOT, env=env
        )
        bridge = CLIENT.GrokAcpBridge(
            connection, REPO_ROOT, events, startup_timeout=1.0, shutdown_timeout=0.5
        )
        self.addCleanup(bridge.shutdown)

        with self.assertRaisesRegex(
            CLIENT.AcpAuthenticationError, "--auth-method|grok login"
        ):
            bridge.start()

    def test_explicit_noninteractive_auth_method_can_replace_missing_default(self) -> None:
        bridge, events, _stderr = self.make_bridge(
            startup_mode="auth-no-default",
            requested_auth_method="cached_token",
        )

        self.assertEqual(events.wait_for("ready")["authMethodId"], "cached_token")

    def test_interactive_default_and_rejected_cached_auth_fail_clearly(self) -> None:
        cases = (
            ("auth-interactive-default", "interactive login"),
            ("auth-rejected", "ACP authentication"),
        )
        for startup_mode, message in cases:
            with self.subTest(startup_mode=startup_mode):
                events = EventCollector()
                env = os.environ.copy()
                env["FAKE_GROK_STARTUP"] = startup_mode
                connection = CLIENT.JsonRpcConnection(
                    [sys.executable, str(FAKE_AGENT)], REPO_ROOT, env=env
                )
                bridge = CLIENT.GrokAcpBridge(
                    connection,
                    REPO_ROOT,
                    events,
                    startup_timeout=1.0,
                    shutdown_timeout=0.5,
                )
                try:
                    with self.assertRaisesRegex(
                        CLIENT.AcpAuthenticationError, message
                    ):
                        bridge.start()
                finally:
                    bridge.shutdown()

    def test_complete_turn_tracks_status_and_redacts_reasoning(self) -> None:
        bridge, events, stderr = self.make_bridge()

        bridge.handle_command({"id": "prompt-1", "op": "prompt", "text": "complete"})
        completed = events.wait_for("turn_completed")

        self.assertEqual(completed["result"]["stopReason"], "end_turn")
        self.assertEqual(completed["text"], "hello")
        self.assertLess(
            next(i for i, event in enumerate(events.events) if event["event"] == "prompt_accepted"),
            next(i for i, event in enumerate(events.events) if event["event"] == "turn_completed"),
        )
        self.assertTrue(any(event.get("event") == "tool_call" for event in events.events))
        self.assertTrue(any(event.get("event") == "plan" for event in events.events))
        self.assertNotIn("private chain of thought", json.dumps(events.events))
        self.assertNotIn(
            "SENTINEL_PRIVATE_REASONING_RESULT", json.dumps(events.events)
        )
        self.assertTrue(any("fake grok stderr" in line for line in stderr))

        snapshot = bridge.status_snapshot()
        self.assertEqual(snapshot["phase"], "idle")
        self.assertIsNone(snapshot["turn"])
        self.assertEqual(snapshot["tools"][0]["status"], "completed")

    def test_mid_turn_steer_is_correlated_and_updates_capability(self) -> None:
        bridge, events, _stderr = self.make_bridge()
        bridge.handle_command({"id": "prompt", "op": "prompt", "text": "wait"})
        events.wait_for("message", lambda event: event.get("content", {}).get("text") == "working")

        bridge.handle_command(
            {"id": "steer-1", "op": "steer", "text": "Change direction"}
        )
        queued = events.wait_for("steer_queued")
        completed = events.wait_for("turn_completed")

        self.assertEqual(queued["commandId"], "steer-1")
        self.assertEqual(completed["text"], "working:steered")
        self.assertEqual(bridge.status_snapshot()["interjectSupport"], "supported")
        self.assertLess(
            next(i for i, event in enumerate(events.events) if event["event"] == "steer_sent"),
            next(i for i, event in enumerate(events.events) if event["event"] == "steer_queued"),
        )

    def test_unsupported_steer_fails_without_silently_cancelling(self) -> None:
        bridge, events, _stderr = self.make_bridge()
        bridge.handle_command(
            {"id": "prompt", "op": "prompt", "text": "no-interject"}
        )
        events.wait_for("message")

        bridge.handle_command({"id": "steer", "op": "steer", "text": "Try"})
        unsupported = events.wait_for("steer_unsupported")

        self.assertEqual(unsupported["error"]["code"], -32601)
        self.assertEqual(bridge.status_snapshot()["phase"], "running")
        bridge.handle_command({"id": "cancel", "op": "cancel"})
        completed = events.wait_for("turn_completed")
        self.assertEqual(completed["result"]["stopReason"], "cancelled")
        self.assertLess(
            next(i for i, event in enumerate(events.events) if event["event"] == "cancel_sent"),
            next(i for i, event in enumerate(events.events) if event["event"] == "turn_completed"),
        )

    def test_permission_requires_a_valid_explicit_option(self) -> None:
        bridge, events, _stderr = self.make_bridge()
        bridge.handle_command(
            {"id": "prompt", "op": "prompt", "text": "permission"}
        )
        required = events.wait_for("permission_required")

        bridge.handle_command(
            {
                "id": "bad-permission",
                "op": "permission",
                "requestId": required["requestId"],
                "optionId": "invented",
            }
        )
        events.wait_for(
            "command_error", lambda event: event.get("commandId") == "bad-permission"
        )
        self.assertEqual(len(bridge.status_snapshot()["pendingPermissions"]), 1)

        bridge.handle_command(
            {
                "id": "allow",
                "op": "permission",
                "requestId": required["requestId"],
                "optionId": "allow-once",
            }
        )
        events.wait_for("permission_resolved")
        completed = events.wait_for("turn_completed")
        self.assertIn("permission:allow-once", completed["text"])

    def test_permission_timeout_fails_closed_and_unblocks_turn(self) -> None:
        bridge, events, _stderr = self.make_bridge(permission_timeout=0.1)
        bridge.handle_command(
            {"id": "prompt", "op": "prompt", "text": "permission"}
        )

        events.wait_for("permission_timed_out")
        completed = events.wait_for("turn_completed")
        self.assertIn("permission:cancelled", completed["text"])

    def test_permission_for_another_session_is_cancelled_immediately(self) -> None:
        bridge, events, _stderr = self.make_bridge()
        bridge.handle_command(
            {"id": "prompt", "op": "prompt", "text": "wrong-session-permission"}
        )

        rejected = events.wait_for(
            "permission_rejected",
            lambda event: event.get("reason") == "wrong_session",
        )
        completed = events.wait_for("turn_completed")

        self.assertEqual(rejected["sessionId"], "another-session")
        self.assertIn("permission:cancelled", completed["text"])
        self.assertEqual(bridge.status_snapshot()["pendingPermissions"], [])

    def test_concurrent_prompt_is_rejected_locally(self) -> None:
        bridge, events, _stderr = self.make_bridge()
        bridge.handle_command({"id": "first", "op": "prompt", "text": "wait"})
        events.wait_for("message")

        bridge.handle_command({"id": "second", "op": "prompt", "text": "complete"})
        error = events.wait_for(
            "command_error", lambda event: event.get("commandId") == "second"
        )

        self.assertIn("already active", error["message"])
        bridge.handle_command({"id": "cancel", "op": "cancel"})
        events.wait_for("turn_completed")

    def test_session_load_marks_replay_and_never_emits_thought_text(self) -> None:
        bridge, events, _stderr = self.make_bridge(requested_session_id=CLIENT_SCRIPT_SESSION_ID)

        ready = events.wait_for("ready")
        history = events.wait_for(
            "message", lambda event: event.get("messageId") == "history-1"
        )

        self.assertTrue(ready["loaded"])
        self.assertTrue(history["replay"])
        self.assertEqual(bridge.session_id, CLIENT_SCRIPT_SESSION_ID)
        self.assertNotIn("historical secret reasoning", json.dumps(events.events))

    def test_unknown_updates_are_forward_compatible_but_reasoning_is_redacted(self) -> None:
        bridge, events, _stderr = self.make_bridge()
        bridge.handle_command(
            {"id": "prompt", "op": "prompt", "text": "unknown-update"}
        )
        update = events.wait_for("session_update")
        events.wait_for("turn_completed")

        self.assertEqual(update["updateType"], "future_event")
        self.assertEqual(update["update"]["value"], 42)
        self.assertEqual(update["update"]["reasoning"], "<redacted>")
        rendered = json.dumps(events.events)
        self.assertNotIn("extension thought must not leak", rendered)
        self.assertIn("<redacted>", rendered)

    def test_think_tool_payload_is_redacted_even_when_updates_omit_kind(self) -> None:
        bridge, events, _stderr = self.make_bridge()
        bridge.handle_command(
            {"id": "prompt", "op": "prompt", "text": "think-tool"}
        )
        events.wait_for("turn_completed")

        rendered = json.dumps(events.events)
        self.assertNotIn("SENTINEL_PRIVATE_REASONING_INPUT", rendered)
        self.assertNotIn("SENTINEL_PRIVATE_REASONING_OUTPUT", rendered)
        self.assertNotIn("SENTINEL_PRIVATE_REASONING_MESSAGE", rendered)
        tool = bridge.status_snapshot()["tools"][0]
        self.assertEqual(tool["kind"], "think")
        self.assertEqual(tool["title"], "<redacted>")

    def test_unexpected_child_exit_fails_the_active_turn(self) -> None:
        bridge, events, _stderr = self.make_bridge()
        bridge.handle_command({"id": "prompt", "op": "prompt", "text": "crash"})

        failed = events.wait_for("turn_failed")
        exited = events.wait_for("agent_exit")

        self.assertEqual(failed["error"]["type"], "AcpProcessExited")
        self.assertFalse(exited["expected"])
        self.assertTrue(bridge.unexpected_exit)

    def test_malformed_agent_output_fails_startup(self) -> None:
        events = EventCollector()
        env = os.environ.copy()
        env["FAKE_GROK_STARTUP"] = "malformed"
        connection = CLIENT.JsonRpcConnection(
            [sys.executable, str(FAKE_AGENT)], REPO_ROOT, env=env
        )
        bridge = CLIENT.GrokAcpBridge(
            connection, REPO_ROOT, events, startup_timeout=1.0, shutdown_timeout=0.5
        )
        self.addCleanup(bridge.shutdown)

        with self.assertRaises(CLIENT.AcpProtocolError):
            bridge.start()

    def test_oversized_agent_output_fails_startup(self) -> None:
        events = EventCollector()
        env = os.environ.copy()
        env["FAKE_GROK_STARTUP"] = "oversize"
        connection = CLIENT.JsonRpcConnection(
            [sys.executable, str(FAKE_AGENT)],
            REPO_ROOT,
            env=env,
            max_message_bytes=512,
        )
        bridge = CLIENT.GrokAcpBridge(
            connection, REPO_ROOT, events, startup_timeout=1.0, shutdown_timeout=0.5
        )
        self.addCleanup(bridge.shutdown)

        with self.assertRaises(CLIENT.AcpProtocolError):
            bridge.start()


CLIENT_SCRIPT_SESSION_ID = "11111111-1111-4111-8111-111111111111"


class GrokAcpCliTests(unittest.TestCase):
    def test_client_source_parses_with_python_39_grammar(self) -> None:
        ast.parse(
            CLIENT_SCRIPT.read_text(encoding="utf-8"),
            filename=str(CLIENT_SCRIPT),
            feature_version=(3, 9),
        )

    def test_cli_jsonl_round_trip_keeps_stderr_separate(self) -> None:
        with tempfile.TemporaryDirectory(prefix="grok-acp-test-") as tmp:
            fake_grok = Path(tmp) / "grok"
            shutil.copyfile(FAKE_AGENT, fake_grok)
            fake_grok.chmod(0o700)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(CLIENT_SCRIPT),
                    "--grok",
                    str(fake_grok),
                    "--cwd",
                    str(REPO_ROOT),
                    "--agent-profile",
                    str(FAKE_AGENT),
                    "--sandbox",
                    "read-only",
                    "--startup-timeout",
                    "2",
                    "--shutdown-timeout",
                    "1",
                ],
                input=(
                    '{"id":"status-1","op":"status"}\n'
                    '{"id":"quit-1","op":"quit"}\n'
                ),
                text=True,
                capture_output=True,
                timeout=5,
                check=False,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        output_events = [
            json.loads(line) for line in completed.stdout.splitlines() if line.strip()
        ]
        names = [event["event"] for event in output_events]
        self.assertEqual(names[0], "ready")
        self.assertEqual(output_events[0]["authMethodId"], "cached_token")
        self.assertEqual(
            output_events[0]["launchConfiguration"]["sandbox"], "read-only"
        )
        self.assertEqual(
            output_events[0]["launchConfiguration"]["agentProfile"],
            str(FAKE_AGENT.resolve()),
        )
        self.assertIn("status", names)
        self.assertIn("quit_accepted", names)
        self.assertEqual(names[-1], "closed")
        self.assertEqual(
            [event["seq"] for event in output_events],
            list(range(1, len(output_events) + 1)),
        )
        self.assertNotIn("fake grok stderr", completed.stdout)
        self.assertIn("fake grok stderr", completed.stderr)

    def test_control_file_supports_background_hosts_without_writable_stdin(self) -> None:
        with tempfile.TemporaryDirectory(prefix="grok-acp-control-test-") as tmp:
            fake_grok = Path(tmp) / "grok"
            shutil.copyfile(FAKE_AGENT, fake_grok)
            fake_grok.chmod(0o700)
            process = subprocess.Popen(
                [
                    sys.executable,
                    str(CLIENT_SCRIPT),
                    "--grok",
                    str(fake_grok),
                    "--cwd",
                    str(REPO_ROOT),
                    "--control-file",
                    "auto",
                    "--startup-timeout",
                    "2",
                    "--shutdown-timeout",
                    "1",
                ],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            try:
                if process.stdout is None:
                    self.fail("missing bridge stdout")
                ready = json.loads(readline_with_timeout(process.stdout))
                control_file = ready["controlFile"]
                self.assertTrue(Path(control_file).is_file())

                events = [ready]
                send_control_command(
                    control_file,
                    {"id": "prompt-file", "op": "prompt", "text": "wait"},
                )
                read_until_events(process.stdout, events, {"message"})

                send_control_command(
                    control_file, {"id": "status-file", "op": "status"}
                )
                send_control_command(
                    control_file,
                    {
                        "id": "steer-file",
                        "op": "steer",
                        "text": "Use the narrower direction",
                    },
                )
                read_until_events(
                    process.stdout,
                    events,
                    {"status", "steer_queued", "turn_completed"},
                )
                send_control_command(
                    control_file, {"id": "quit-file", "op": "quit"}
                )

                remainder, stderr = process.communicate(timeout=5)
            finally:
                if process.poll() is None:
                    process.kill()
                    process.wait(timeout=2)

        events.extend(
            json.loads(line) for line in remainder.splitlines() if line.strip()
        )
        self.assertEqual(process.returncode, 0, stderr)
        status = next(event for event in events if event.get("event") == "status")
        completed = next(
            event for event in events if event.get("event") == "turn_completed"
        )
        self.assertEqual(status["status"]["phase"], "running")
        self.assertEqual(completed["text"], "working:steered")
        self.assertEqual(events[-1]["event"], "closed")
        self.assertFalse(Path(control_file).exists())

    def test_send_refuses_an_unmarked_regular_file(self) -> None:
        with tempfile.TemporaryDirectory(prefix="grok-acp-control-test-") as tmp:
            unrelated = Path(tmp) / "unrelated.jsonl"
            unrelated.write_text("{}\n", encoding="utf-8")
            unrelated.chmod(0o600)

            sent = subprocess.run(
                [
                    sys.executable,
                    str(CLIENT_SCRIPT),
                    "send",
                    "--control-file",
                    str(unrelated),
                    "--json",
                    '{"op":"status"}',
                ],
                text=True,
                capture_output=True,
                timeout=3,
                check=False,
            )

        self.assertEqual(sent.returncode, 2)
        self.assertFalse(json.loads(sent.stdout)["sent"])

    def test_agent_command_places_agent_options_before_stdio(self) -> None:
        args = argparse.Namespace(
            grok=sys.executable,
            model="model-id",
            reasoning_effort="high",
            always_approve=True,
            agent_profile=str(FAKE_AGENT),
        )

        command = CLIENT.build_agent_command(args)

        self.assertEqual(command[1:3], ["agent", "--no-leader"])
        self.assertEqual(command[-1], "stdio")
        self.assertLess(command.index("--model"), command.index("stdio"))
        self.assertLess(command.index("--always-approve"), command.index("stdio"))
        self.assertEqual(
            command[command.index("--agent-profile") + 1],
            str(FAKE_AGENT.resolve()),
        )

    def test_child_environment_applies_explicit_sandbox_profile(self) -> None:
        args = argparse.Namespace(sandbox="read-only")

        child_env = CLIENT.build_child_environment(args, {"EXISTING": "kept"})

        self.assertEqual(child_env["EXISTING"], "kept")
        self.assertEqual(child_env["GROK_SANDBOX"], "read-only")
        self.assertEqual(child_env["GROK_DISABLE_AUTOUPDATER"], "1")

    def test_child_environment_preserves_inherited_sandbox_when_not_overridden(self) -> None:
        args = argparse.Namespace(sandbox=None)

        child_env = CLIENT.build_child_environment(
            args, {"GROK_SANDBOX": "strict"}
        )

        self.assertEqual(child_env["GROK_SANDBOX"], "strict")

    def test_decode_command_requires_a_json_object(self) -> None:
        self.assertEqual(
            CLIENT.decode_command(b'{"id":"one","op":"status"}\n'),
            {"id": "one", "op": "status"},
        )
        with self.assertRaisesRegex(ValueError, "JSON object"):
            CLIENT.decode_command(b"[]\n")


if __name__ == "__main__":
    unittest.main()
