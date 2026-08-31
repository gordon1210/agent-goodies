#!/usr/bin/env python3
"""Small, dependency-free ACP client for ``grok agent stdio``.

The program keeps one Grok process and one ACP session alive. Its stdin accepts
one JSON command per line; its stdout emits one normalized JSON event per line.
Grok's stderr remains separate on this program's stderr.

This is deliberately a bridge, not a general ACP SDK. It implements the parts
needed for agent pairing: initialize, create/load a session, prompt, status,
permission replies, cancellation, and Grok's optional mid-turn interjection.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import os
import queue
import secrets
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple


CLIENT_VERSION = "1.0.0"
PROTOCOL_VERSION = 1
DEFAULT_MAX_MESSAGE_BYTES = 8 * 1024 * 1024
DEFAULT_MAX_COMMAND_BYTES = 1024 * 1024
DEFAULT_MAX_PROMPT_BYTES = 1024 * 1024
DEFAULT_MAX_PENDING_REQUESTS = 64
DEFAULT_MAX_TRACKED_TOOLS = 256
DEFAULT_MAX_COLLECTED_TEXT_CHARS = 1024 * 1024
DEFAULT_STARTUP_TIMEOUT = 30.0
DEFAULT_PERMISSION_TIMEOUT = 120.0
DEFAULT_SHUTDOWN_TIMEOUT = 8.0
CONTROL_MAGIC = "grok-acp-control"

JsonObject = Dict[str, Any]
RequestId = Any
EventCallback = Callable[[JsonObject], None]


def utc_timestamp() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def compact_json(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def request_id_key(value: RequestId) -> Tuple[str, Any]:
    if isinstance(value, bool) or value is None or not isinstance(value, (int, str)):
        raise ValueError("JSON-RPC request IDs must be non-null strings or integers")
    return (type(value).__name__, value)


def is_reasoning_discriminator(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    folded = value.lower().replace("_", "-")
    return (
        "thought" in folded
        or "reasoning" in folded
        or folded == "think"
        or folded.startswith("think-")
        or folded.startswith("thinking")
    )


def redact_reasoning(value: Any) -> Any:
    """Remove reasoning-like fields while preserving operational structure."""

    if isinstance(value, dict):
        reasoning_object = any(
            is_reasoning_discriminator(value.get(key))
            for key in ("sessionUpdate", "type", "kind", "role")
        )
        redacted: JsonObject = {}
        for key, item in value.items():
            folded = key.lower().replace("_", "").replace("-", "")
            if (
                "thought" in folded
                or "reasoning" in folded
                or "chainofthought" in folded
                or (
                    reasoning_object
                    and folded
                    in {
                        "content",
                        "text",
                        "delta",
                        "message",
                        "rawinput",
                        "rawoutput",
                        "title",
                    }
                )
            ):
                redacted[key] = "<redacted>"
            else:
                redacted[key] = redact_reasoning(item)
        return redacted
    if isinstance(value, list):
        return [redact_reasoning(item) for item in value]
    return value


def redact_tool_update(update: JsonObject, known_kind: Any) -> JsonObject:
    """Redact a tool update using kind remembered from earlier updates."""

    redacted = redact_reasoning(update)
    if not isinstance(redacted, dict):
        return {}
    if is_reasoning_discriminator(known_kind):
        for key in (
            "content",
            "text",
            "delta",
            "message",
            "rawInput",
            "rawOutput",
            "title",
        ):
            if key in redacted:
                redacted[key] = "<redacted>"
    return redacted


class AcpError(RuntimeError):
    """Base error for the ACP transport."""


class AcpProtocolError(AcpError):
    """The child emitted invalid JSON-RPC or violated framing limits."""


class AcpAuthenticationError(AcpError):
    """The bridge could not select or complete noninteractive ACP auth."""


class AcpProcessExited(AcpError):
    """The child process exited while work was pending."""

    def __init__(self, returncode: Optional[int]) -> None:
        super().__init__(f"grok agent exited with status {returncode}")
        self.returncode = returncode


class AcpRemoteError(AcpError):
    """A JSON-RPC error returned by Grok."""

    def __init__(self, error: Any) -> None:
        if isinstance(error, dict):
            self.code = error.get("code")
            self.message = str(error.get("message", "Remote JSON-RPC error"))
            self.data = error.get("data")
            self.error = dict(error)
        else:
            self.code = None
            self.message = "Malformed remote JSON-RPC error"
            self.data = error
            self.error = {"message": self.message, "data": error}
        super().__init__(self.message)


@dataclass(frozen=True)
class RequestHandle:
    request_id: int
    future: concurrent.futures.Future


class JsonRpcConnection:
    """Thread-safe newline-delimited JSON-RPC connection to one child process."""

    def __init__(
        self,
        command: Sequence[str],
        cwd: Path,
        *,
        max_message_bytes: int = DEFAULT_MAX_MESSAGE_BYTES,
        max_pending_requests: int = DEFAULT_MAX_PENDING_REQUESTS,
        env: Optional[Dict[str, str]] = None,
        stderr_callback: Optional[Callable[[str], None]] = None,
    ) -> None:
        self.command = list(command)
        self.cwd = cwd
        self.max_message_bytes = max_message_bytes
        self.max_pending_requests = max_pending_requests
        self.env = env
        self.stderr_callback = stderr_callback or (lambda _text: None)

        self.on_notification: Callable[[JsonObject], None] = lambda _message: None
        self.on_request: Callable[[JsonObject], None] = lambda _message: None
        self.on_warning: Callable[[str, Optional[JsonObject]], None] = (
            lambda _message, _payload: None
        )
        self.on_exit: Callable[[Optional[int], bool, Optional[BaseException]], None] = (
            lambda _code, _expected, _error: None
        )

        self._process: Optional[subprocess.Popen] = None
        self._write_lock = threading.Lock()
        self._pending_lock = threading.Lock()
        self._lifecycle_lock = threading.Lock()
        self._pending: Dict[int, concurrent.futures.Future] = {}
        self._next_request_id = 1
        self._closing = False
        self._exit_reported = False
        self._reader_thread: Optional[threading.Thread] = None
        self._stderr_thread: Optional[threading.Thread] = None

    @property
    def pid(self) -> Optional[int]:
        return self._process.pid if self._process is not None else None

    @property
    def returncode(self) -> Optional[int]:
        return self._process.poll() if self._process is not None else None

    @property
    def alive(self) -> bool:
        return self._process is not None and self._process.poll() is None

    def start(self) -> None:
        with self._lifecycle_lock:
            if self._process is not None:
                raise RuntimeError("ACP process already started")
            try:
                self._process = subprocess.Popen(
                    self.command,
                    cwd=str(self.cwd),
                    env=self.env,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    bufsize=0,
                    shell=False,
                )
            except OSError as exc:
                raise AcpError(f"Unable to start {self.command[0]}: {exc}") from exc

            self._reader_thread = threading.Thread(
                target=self._reader_loop,
                name="grok-acp-reader",
                daemon=True,
            )
            self._stderr_thread = threading.Thread(
                target=self._stderr_loop,
                name="grok-acp-stderr",
                daemon=True,
            )
            self._reader_thread.start()
            self._stderr_thread.start()

    def request(self, method: str, params: Any) -> RequestHandle:
        if not method:
            raise ValueError("JSON-RPC method must not be empty")
        with self._pending_lock:
            if len(self._pending) >= self.max_pending_requests:
                raise AcpError(
                    f"Too many pending ACP requests ({self.max_pending_requests})"
                )
            request_id = self._next_request_id
            self._next_request_id += 1
            future: concurrent.futures.Future = concurrent.futures.Future()
            self._pending[request_id] = future

        message = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params,
        }
        try:
            self._send(message)
        except BaseException as exc:
            with self._pending_lock:
                self._pending.pop(request_id, None)
            future.set_exception(exc)
            raise
        return RequestHandle(request_id=request_id, future=future)

    def call(self, method: str, params: Any, timeout: float) -> Any:
        handle = self.request(method, params)
        try:
            return handle.future.result(timeout=timeout)
        except concurrent.futures.TimeoutError as exc:
            with self._pending_lock:
                pending = self._pending.pop(handle.request_id, None)
            if pending is not None and not pending.done():
                pending.set_exception(
                    AcpError(f"ACP request timed out: {method} ({timeout:g}s)")
                )
            raise AcpError(f"ACP request timed out: {method} ({timeout:g}s)") from exc

    def notify(self, method: str, params: Any) -> None:
        self._send({"jsonrpc": "2.0", "method": method, "params": params})

    def respond_result(self, request_id: RequestId, result: Any) -> None:
        self._send({"jsonrpc": "2.0", "id": request_id, "result": result})

    def respond_error(
        self,
        request_id: RequestId,
        code: int,
        message: str,
        data: Any = None,
    ) -> None:
        error: JsonObject = {"code": code, "message": message}
        if data is not None:
            error["data"] = data
        self._send({"jsonrpc": "2.0", "id": request_id, "error": error})

    def _send(self, message: JsonObject) -> None:
        payload = compact_json(message)
        if len(payload) > self.max_message_bytes:
            raise AcpProtocolError(
                f"Outgoing ACP message exceeds {self.max_message_bytes} bytes"
            )
        process = self._process
        if process is None or process.stdin is None:
            raise AcpError("ACP process is not running")
        with self._write_lock:
            if self._closing or process.poll() is not None:
                raise AcpProcessExited(process.poll())
            try:
                process.stdin.write(payload)
                process.stdin.flush()
            except (BrokenPipeError, OSError, ValueError) as exc:
                raise AcpProcessExited(process.poll()) from exc

    def _reader_loop(self) -> None:
        process = self._process
        if process is None or process.stdout is None:
            return
        failure: Optional[BaseException] = None
        try:
            while True:
                raw = process.stdout.readline(self.max_message_bytes + 1)
                if not raw:
                    break
                if len(raw) > self.max_message_bytes:
                    raise AcpProtocolError(
                        f"Incoming ACP message exceeds {self.max_message_bytes} bytes"
                    )
                if not raw.endswith(b"\n") and process.poll() is None:
                    raise AcpProtocolError("Incoming ACP record is not newline terminated")
                try:
                    text = raw.decode("utf-8")
                except UnicodeDecodeError as exc:
                    raise AcpProtocolError("Incoming ACP record is not UTF-8") from exc
                if not text.strip():
                    self.on_warning("Ignored blank ACP record", None)
                    continue
                try:
                    message = json.loads(text)
                except json.JSONDecodeError as exc:
                    raise AcpProtocolError(f"Invalid JSON from grok agent: {exc}") from exc
                if not isinstance(message, dict):
                    raise AcpProtocolError("ACP record must be a JSON object")
                self._dispatch(message)
        except BaseException as exc:
            failure = exc
            try:
                process.terminate()
            except OSError:
                pass
        finally:
            try:
                returncode = process.wait(timeout=1.0)
            except subprocess.TimeoutExpired:
                returncode = process.poll()
            self._report_exit(returncode, failure)

    def _dispatch(self, message: JsonObject) -> None:
        if message.get("jsonrpc") != "2.0":
            raise AcpProtocolError("ACP record has no valid jsonrpc='2.0' field")

        has_method = "method" in message
        has_id = "id" in message
        if has_method:
            method = message.get("method")
            if not isinstance(method, str) or not method:
                raise AcpProtocolError("ACP method must be a non-empty string")
            if has_id:
                self.on_request(message)
            else:
                self.on_notification(message)
            return

        if not has_id:
            raise AcpProtocolError("ACP response has neither method nor id")
        request_id = message.get("id")
        if isinstance(request_id, bool) or not isinstance(request_id, int):
            self.on_warning("Ignored response with an unknown request ID type", message)
            return
        with self._pending_lock:
            future = self._pending.pop(request_id, None)
        if future is None:
            self.on_warning("Ignored response for an unknown or expired request", message)
            return
        has_result = "result" in message
        has_error = "error" in message
        if has_result == has_error:
            future.set_exception(
                AcpProtocolError("ACP response must contain exactly one of result or error")
            )
        elif has_error:
            future.set_exception(AcpRemoteError(message.get("error")))
        else:
            future.set_result(message.get("result"))

    def _stderr_loop(self) -> None:
        process = self._process
        if process is None or process.stderr is None:
            return
        while True:
            raw = process.stderr.readline(64 * 1024)
            if not raw:
                return
            self.stderr_callback(raw.decode("utf-8", errors="replace"))

    def _report_exit(
        self,
        returncode: Optional[int],
        failure: Optional[BaseException],
    ) -> None:
        with self._lifecycle_lock:
            if self._exit_reported:
                return
            self._exit_reported = True
            expected = self._closing
        error = failure or AcpProcessExited(returncode)
        with self._pending_lock:
            pending = list(self._pending.values())
            self._pending.clear()
        for future in pending:
            if not future.done():
                future.set_exception(error)
        self.on_exit(returncode, expected, failure)

    def close(self, timeout: float = DEFAULT_SHUTDOWN_TIMEOUT) -> Optional[int]:
        process = self._process
        if process is None:
            return None
        with self._lifecycle_lock:
            self._closing = True
        with self._write_lock:
            if process.stdin is not None:
                try:
                    process.stdin.close()
                except OSError:
                    pass

        deadline = time.monotonic() + max(0.0, timeout)
        try:
            process.wait(timeout=max(0.0, deadline - time.monotonic()))
        except subprocess.TimeoutExpired:
            try:
                process.terminate()
            except OSError:
                pass
            try:
                process.wait(timeout=max(0.0, deadline - time.monotonic()))
            except subprocess.TimeoutExpired:
                try:
                    process.kill()
                except OSError:
                    pass
                try:
                    process.wait(timeout=1.0)
                except subprocess.TimeoutExpired:
                    pass

        current = threading.current_thread()
        for thread in (self._reader_thread, self._stderr_thread):
            if thread is not None and thread is not current:
                thread.join(timeout=1.0)
        for stream in (process.stdout, process.stderr):
            if stream is not None:
                try:
                    stream.close()
                except OSError:
                    pass
        self._report_exit(process.poll(), None)
        return process.poll()


@dataclass
class ActiveTurn:
    command_id: RequestId
    request_id: int
    started_at: str
    last_activity_at: str
    text_parts: List[str] = field(default_factory=list)
    text_chars: int = 0
    text_truncated: bool = False


@dataclass
class PendingPermission:
    request_id: RequestId
    params: JsonObject
    options: Dict[str, JsonObject]
    created_at: str
    timer: threading.Timer


class GrokAcpBridge:
    """One-session state machine exposed through small JSON commands."""

    def __init__(
        self,
        connection: JsonRpcConnection,
        cwd: Path,
        emit: EventCallback,
        *,
        requested_session_id: Optional[str] = None,
        requested_auth_method: Optional[str] = None,
        startup_timeout: float = DEFAULT_STARTUP_TIMEOUT,
        permission_timeout: float = DEFAULT_PERMISSION_TIMEOUT,
        shutdown_timeout: float = DEFAULT_SHUTDOWN_TIMEOUT,
        max_prompt_bytes: int = DEFAULT_MAX_PROMPT_BYTES,
        max_tracked_tools: int = DEFAULT_MAX_TRACKED_TOOLS,
        max_collected_text_chars: int = DEFAULT_MAX_COLLECTED_TEXT_CHARS,
        control_file: Optional[Path] = None,
        launch_configuration: Optional[JsonObject] = None,
    ) -> None:
        self.connection = connection
        self.cwd = cwd
        self.emit = emit
        self.requested_session_id = requested_session_id
        self.requested_auth_method = requested_auth_method
        self.startup_timeout = startup_timeout
        self.permission_timeout = permission_timeout
        self.shutdown_timeout = shutdown_timeout
        self.max_prompt_bytes = max_prompt_bytes
        self.max_tracked_tools = max_tracked_tools
        self.max_collected_text_chars = max_collected_text_chars
        self.control_file = control_file
        self.launch_configuration = dict(launch_configuration or {})

        self._lock = threading.RLock()
        self._active_done = threading.Event()
        self._active_done.set()
        self.terminal_event = threading.Event()
        self.phase = "starting"
        self.session_id: Optional[str] = None
        self.auth_method_id: Optional[str] = None
        self.agent_capabilities: JsonObject = {}
        self.agent_info: JsonObject = {}
        self.active_turn: Optional[ActiveTurn] = None
        self.plan: Any = None
        self.usage: Any = None
        self.tools: "OrderedDict[str, JsonObject]" = OrderedDict()
        self.pending_permissions: Dict[Tuple[str, Any], PendingPermission] = {}
        self.interject_support = "unknown"
        self.last_activity_at = utc_timestamp()
        self._next_command_id = 1
        self._shutting_down = False
        self._unexpected_exit = False

        connection.on_notification = self._on_notification
        connection.on_request = self._on_request
        connection.on_warning = self._on_warning
        connection.on_exit = self._on_exit

    @property
    def unexpected_exit(self) -> bool:
        with self._lock:
            return self._unexpected_exit

    @staticmethod
    def _auth_methods(initialized: JsonObject) -> Dict[str, JsonObject]:
        raw_methods = initialized.get("authMethods")
        if raw_methods is None:
            return {}
        if not isinstance(raw_methods, list):
            raise AcpProtocolError("initialize authMethods must be an array")
        methods: Dict[str, JsonObject] = {}
        for raw_method in raw_methods:
            if not isinstance(raw_method, dict):
                raise AcpProtocolError("initialize authMethods entries must be objects")
            method_id = raw_method.get("id")
            if not isinstance(method_id, str) or not method_id:
                raise AcpProtocolError("initialize authMethods entry has no valid id")
            if method_id in methods:
                raise AcpProtocolError(
                    f"initialize advertised duplicate auth method {method_id!r}"
                )
            methods[method_id] = dict(raw_method)
        return methods

    @staticmethod
    def _interactive_auth_method(method: JsonObject) -> bool:
        method_id = str(method.get("id", "")).lower()
        method_type = str(method.get("type", "")).lower().replace("_", "-")
        return method_id == "grok.com" or method_type in {
            "interactive",
            "terminal",
            "terminal-auth",
        }

    def _authenticate(self, initialized: JsonObject) -> None:
        methods = self._auth_methods(initialized)
        if not methods:
            return

        selected_id = self.requested_auth_method
        if selected_id is not None:
            selected_id = selected_id.strip()
            if not selected_id or selected_id not in methods:
                advertised = ", ".join(sorted(methods))
                raise AcpAuthenticationError(
                    f"--auth-method must name an advertised method; available: {advertised}"
                )
        else:
            meta = initialized.get("_meta")
            default_id = meta.get("defaultAuthMethodId") if isinstance(meta, dict) else None
            if not isinstance(default_id, str) or not default_id:
                raise AcpAuthenticationError(
                    "Grok advertised authentication methods but no default. Run `grok login` "
                    "outside the bridge, or pass an advertised noninteractive --auth-method."
                )
            if default_id not in methods:
                raise AcpAuthenticationError(
                    "Grok's defaultAuthMethodId is not present in authMethods; update Grok "
                    "or select an advertised noninteractive --auth-method explicitly."
                )
            selected_id = default_id

        selected = methods[selected_id]
        if self._interactive_auth_method(selected):
            raise AcpAuthenticationError(
                f"Authentication method {selected_id!r} requires interactive login. "
                "Run `grok login` separately, then restart the bridge with cached credentials."
            )

        with self._lock:
            self.phase = "authenticating"
        try:
            self.connection.call(
                "authenticate",
                {"methodId": selected_id, "_meta": {"headless": True}},
                self.startup_timeout,
            )
        except AcpRemoteError as exc:
            raise AcpAuthenticationError(
                f"ACP authentication with {selected_id!r} failed: {exc}. "
                "Run `grok login` or verify XAI_API_KEY outside the bridge."
            ) from exc
        with self._lock:
            self.auth_method_id = selected_id

    def start(self) -> None:
        self.connection.start()
        initialized = self.connection.call(
            "initialize",
            {
                "protocolVersion": PROTOCOL_VERSION,
                "clientCapabilities": {},
                "clientInfo": {
                    "name": "grok-cli-skill",
                    "title": "Grok CLI Skill ACP Bridge",
                    "version": CLIENT_VERSION,
                },
                "_meta": {"clientIdentifier": "grok-cli-skill"},
            },
            self.startup_timeout,
        )
        if not isinstance(initialized, dict):
            raise AcpProtocolError("initialize result must be a JSON object")
        protocol_version = initialized.get("protocolVersion")
        if isinstance(protocol_version, bool) or protocol_version != PROTOCOL_VERSION:
            raise AcpProtocolError(
                f"Unsupported ACP protocol version: {protocol_version!r}"
            )
        capabilities = initialized.get("agentCapabilities", {})
        if not isinstance(capabilities, dict):
            raise AcpProtocolError("agentCapabilities must be a JSON object")
        agent_info = initialized.get("agentInfo", {})
        if not isinstance(agent_info, dict):
            agent_info = {}

        with self._lock:
            self.agent_capabilities = dict(capabilities)
            self.agent_info = dict(agent_info)

        self._authenticate(initialized)

        with self._lock:
            self.phase = "loading" if self.requested_session_id else "creating"

        session_params: JsonObject = {
            "cwd": str(self.cwd),
            "mcpServers": [],
        }
        if self.requested_session_id:
            if capabilities.get("loadSession") is not True:
                raise AcpProtocolError(
                    "The agent does not advertise loadSession; cannot load --session-id"
                )
            session_params["sessionId"] = self.requested_session_id
            self.connection.call("session/load", session_params, self.startup_timeout)
            session_id = self.requested_session_id
        else:
            created = self.connection.call(
                "session/new", session_params, self.startup_timeout
            )
            if not isinstance(created, dict):
                raise AcpProtocolError("session/new result must be a JSON object")
            session_id = created.get("sessionId")
            if not isinstance(session_id, str) or not session_id:
                raise AcpProtocolError("session/new returned no valid sessionId")

        meta = initialized.get("_meta")
        selected_meta: JsonObject = {}
        if isinstance(meta, dict):
            for key in ("agentVersion", "agentId", "agentInstanceId"):
                if key in meta:
                    selected_meta[key] = meta[key]
        with self._lock:
            self.session_id = session_id
            self.phase = "idle"
            self.last_activity_at = utc_timestamp()
            self.plan = None
            self.usage = None
            self.tools.clear()
        self.emit(
            {
                "event": "ready",
                "sessionId": session_id,
                "cwd": str(self.cwd),
                "pid": self.connection.pid,
                "protocolVersion": protocol_version,
                "agentInfo": self.agent_info,
                "agentCapabilities": self.agent_capabilities,
                "agentMeta": selected_meta,
                "authMethodId": self.auth_method_id,
                "loaded": bool(self.requested_session_id),
                "controlFile": str(self.control_file) if self.control_file else None,
                "launchConfiguration": dict(self.launch_configuration),
            }
        )

    def handle_command(self, command: JsonObject) -> bool:
        command_id = self._command_id(command)
        op = command.get("op")
        if not isinstance(op, str) or not op:
            self._command_error(command_id, None, "Command requires a non-empty 'op'")
            return False

        try:
            if op == "prompt":
                self._command_prompt(command_id, command)
            elif op == "status":
                self.emit(
                    {
                        "event": "status",
                        "commandId": command_id,
                        "status": self.status_snapshot(),
                    }
                )
            elif op == "steer":
                self._command_steer(command_id, command)
            elif op == "cancel":
                self._command_cancel(command_id)
            elif op == "permission":
                self._command_permission(command_id, command)
            elif op == "ping":
                self.emit(
                    {
                        "event": "pong",
                        "commandId": command_id,
                        "sessionId": self.session_id,
                    }
                )
            elif op == "help":
                self.emit(
                    {
                        "event": "help",
                        "commandId": command_id,
                        "operations": [
                            "prompt",
                            "status",
                            "steer",
                            "cancel",
                            "permission",
                            "ping",
                            "quit",
                        ],
                    }
                )
            elif op == "quit":
                self.emit({"event": "quit_accepted", "commandId": command_id})
                return True
            else:
                self._command_error(command_id, op, f"Unknown operation: {op}")
        except (AcpError, ValueError) as exc:
            self._command_error(command_id, op, str(exc), exception=exc)
        return False

    def _command_id(self, command: JsonObject) -> RequestId:
        if "id" in command:
            command_id = command.get("id")
            request_id_key(command_id)
            return command_id
        with self._lock:
            command_id = f"cmd-{self._next_command_id}"
            self._next_command_id += 1
        return command_id

    def _text_argument(self, command: JsonObject) -> str:
        text = command.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Command requires non-empty string field 'text'")
        if len(text.encode("utf-8")) > self.max_prompt_bytes:
            raise ValueError(
                f"Command text exceeds {self.max_prompt_bytes} UTF-8 bytes"
            )
        return text

    def _command_prompt(self, command_id: RequestId, command: JsonObject) -> None:
        text = self._text_argument(command)
        with self._lock:
            if self.phase != "idle" or self.active_turn is not None:
                raise ValueError(
                    "A prompt is already active; steer, cancel, or wait for turn_completed"
                )
            if not self.session_id:
                raise AcpError("No ACP session is ready")
            handle = self.connection.request(
                "session/prompt",
                {
                    "sessionId": self.session_id,
                    "prompt": [{"type": "text", "text": text}],
                },
            )
            now = utc_timestamp()
            self.active_turn = ActiveTurn(
                command_id=command_id,
                request_id=handle.request_id,
                started_at=now,
                last_activity_at=now,
            )
            self.phase = "running"
            self.last_activity_at = now
            self.plan = None
            self.usage = None
            self.tools.clear()
            self._active_done.clear()
            self.emit(
                {
                    "event": "prompt_accepted",
                    "commandId": command_id,
                    "requestId": handle.request_id,
                    "sessionId": self.session_id,
                }
            )
        handle.future.add_done_callback(
            lambda future: self._finish_prompt(command_id, handle.request_id, future)
        )

    def _finish_prompt(
        self,
        command_id: RequestId,
        request_id: int,
        future: concurrent.futures.Future,
    ) -> None:
        with self._lock:
            active = self.active_turn
            if active is None or active.request_id != request_id:
                return
            text = "".join(active.text_parts)
            truncated = active.text_truncated
            self.active_turn = None
            if not self._shutting_down:
                self.phase = "idle"
            self.last_activity_at = utc_timestamp()
            self._active_done.set()
        self._cancel_all_permissions("turn_finished")
        try:
            result = future.result()
        except BaseException as exc:
            payload: JsonObject = {
                "event": "turn_failed",
                "commandId": command_id,
                "requestId": request_id,
                "sessionId": self.session_id,
                "error": self._error_payload(exc),
                "text": text,
                "textTruncated": truncated,
            }
        else:
            payload = {
                "event": "turn_completed",
                "commandId": command_id,
                "requestId": request_id,
                "sessionId": self.session_id,
                "result": redact_reasoning(result),
                "text": text,
                "textTruncated": truncated,
            }
        self.emit(payload)

    def _command_steer(self, command_id: RequestId, command: JsonObject) -> None:
        text = self._text_argument(command)
        with self._lock:
            if self.active_turn is None or self.phase not in {"running", "cancelling"}:
                raise ValueError("Steering requires an active prompt turn")
            if self.phase == "cancelling":
                raise ValueError("The active turn is already being cancelled")
            if self.interject_support == "unsupported":
                raise ValueError(
                    "This Grok version rejected mid-turn interjection; cancel and prompt again"
                )
            if not self.session_id:
                raise AcpError("No ACP session is ready")
            handle = self.connection.request(
                "_x.ai/interject",
                {
                    "sessionId": self.session_id,
                    "text": text,
                    "interjectionId": str(command_id),
                },
            )
            self.emit(
                {
                    "event": "steer_sent",
                    "commandId": command_id,
                    "requestId": handle.request_id,
                    "sessionId": self.session_id,
                }
            )
        handle.future.add_done_callback(
            lambda future: self._finish_steer(command_id, handle.request_id, future)
        )

    def _finish_steer(
        self,
        command_id: RequestId,
        request_id: int,
        future: concurrent.futures.Future,
    ) -> None:
        try:
            result = future.result()
        except AcpRemoteError as exc:
            if exc.code == -32601:
                with self._lock:
                    self.interject_support = "unsupported"
                self.emit(
                    {
                        "event": "steer_unsupported",
                        "commandId": command_id,
                        "requestId": request_id,
                        "sessionId": self.session_id,
                        "error": self._error_payload(exc),
                        "fallback": "Wait for completion, or cancel and send a new prompt.",
                    }
                )
            else:
                self._command_error(
                    command_id, "steer", str(exc), exception=exc, request_id=request_id
                )
        except BaseException as exc:
            self._command_error(
                command_id, "steer", str(exc), exception=exc, request_id=request_id
            )
        else:
            with self._lock:
                self.interject_support = "supported"
            self.emit(
                {
                    "event": "steer_queued",
                    "commandId": command_id,
                    "requestId": request_id,
                    "sessionId": self.session_id,
                    "result": redact_reasoning(result),
                }
            )

    def _command_cancel(self, command_id: RequestId) -> None:
        with self._lock:
            if self.active_turn is None:
                self.emit(
                    {
                        "event": "cancel_ignored",
                        "commandId": command_id,
                        "sessionId": self.session_id,
                        "reason": "no_active_turn",
                    }
                )
                return
            self.phase = "cancelling"
            session_id = self.session_id
            try:
                self.connection.notify("session/cancel", {"sessionId": session_id})
            except BaseException:
                self.phase = "running"
                raise
            self.emit(
                {
                    "event": "cancel_sent",
                    "commandId": command_id,
                    "sessionId": session_id,
                }
            )
        self._cancel_all_permissions("turn_cancelled")

    def _command_permission(self, command_id: RequestId, command: JsonObject) -> None:
        if "requestId" not in command:
            raise ValueError("permission requires field 'requestId'")
        rpc_id = command.get("requestId")
        key = request_id_key(rpc_id)
        with self._lock:
            pending = self.pending_permissions.get(key)
            if pending is None:
                raise ValueError(f"No pending permission request: {rpc_id!r}")

        if command.get("cancelled") is True:
            outcome: JsonObject = {"outcome": "cancelled"}
            selected_option = None
        else:
            option_id = command.get("optionId")
            if not isinstance(option_id, str) or option_id not in pending.options:
                available = sorted(pending.options)
                raise ValueError(
                    f"permission optionId must be one of {available!r}, or use cancelled=true"
                )
            outcome = {"outcome": "selected", "optionId": option_id}
            selected_option = option_id

        removed = self._pop_permission(key)
        if removed is None:
            raise ValueError(f"Permission request already resolved: {rpc_id!r}")
        self.connection.respond_result(rpc_id, {"outcome": outcome})
        self.emit(
            {
                "event": "permission_resolved",
                "commandId": command_id,
                "requestId": rpc_id,
                "sessionId": self.session_id,
                "optionId": selected_option,
                "cancelled": selected_option is None,
            }
        )

    def _on_notification(self, message: JsonObject) -> None:
        method = message.get("method")
        params = message.get("params", {})
        if method == "session/update":
            self._on_session_update(params)
            return
        if isinstance(method, str) and (
            "thought" in method.lower() or "reasoning" in method.lower()
        ):
            self.emit(
                {
                    "event": "activity",
                    "activity": "reasoning",
                    "method": method,
                }
            )
            return
        self.emit(
            {
                "event": "extension_notification"
                if isinstance(method, str) and method.startswith("_")
                else "notification",
                "method": method,
                "params": redact_reasoning(params),
            }
        )

    def _on_session_update(self, params: Any) -> None:
        if not isinstance(params, dict):
            self._on_warning("Ignored session/update with non-object params", None)
            return
        session_id = params.get("sessionId")
        update = params.get("update")
        if not isinstance(update, dict):
            self._on_warning("Ignored session/update with no object update", params)
            return
        with self._lock:
            expected_session = self.session_id or self.requested_session_id
        if expected_session and session_id != expected_session:
            self._on_warning("Ignored update for another ACP session", params)
            return

        update_type = update.get("sessionUpdate")
        now = utc_timestamp()
        with self._lock:
            self.last_activity_at = now
            active = self.active_turn
            replay = active is None
            if active is not None:
                active.last_activity_at = now

        if is_reasoning_discriminator(update_type):
            self.emit(
                {
                    "event": "activity",
                    "activity": "reasoning",
                    "sessionId": session_id,
                    "replay": replay,
                }
            )
            return

        if update_type in {"agent_message_chunk", "user_message_chunk"}:
            self._emit_message_update(
                update_type, update, active, session_id, replay
            )
            return

        if update_type in {"tool_call", "tool_call_update"}:
            tool = self._track_tool(update)
            self.emit(
                {
                    "event": update_type,
                    "sessionId": session_id,
                    "tool": tool,
                    "update": redact_tool_update(update, tool.get("kind")),
                    "replay": replay,
                }
            )
            return

        if update_type == "plan":
            plan = update.get("entries", update.get("plan", update))
            with self._lock:
                self.plan = redact_reasoning(plan)
            self.emit(
                {
                    "event": "plan",
                    "sessionId": session_id,
                    "plan": self.plan,
                    "replay": replay,
                }
            )
            return

        if update_type == "usage_update":
            with self._lock:
                self.usage = redact_reasoning(update)
            self.emit(
                {
                    "event": "usage",
                    "sessionId": session_id,
                    "usage": self.usage,
                    "replay": replay,
                }
            )
            return

        self.emit(
            {
                "event": "session_update",
                "sessionId": session_id,
                "updateType": update_type,
                "update": redact_reasoning(update),
                "replay": replay,
            }
        )

    def _emit_message_update(
        self,
        update_type: str,
        update: JsonObject,
        active: Optional[ActiveTurn],
        session_id: Any,
        replay: bool,
    ) -> None:
        content = update.get("content")
        safe_content = redact_reasoning(content)
        text = safe_content.get("text", "") if isinstance(safe_content, dict) else ""
        if text == "<redacted>" or not isinstance(text, str):
            text = ""
        if update_type == "agent_message_chunk" and active is not None and text:
            self._append_turn_text(active, text)
        self.emit(
            {
                "event": "message",
                "role": "agent" if update_type == "agent_message_chunk" else "user",
                "sessionId": session_id,
                "messageId": update.get("messageId"),
                "content": safe_content,
                "replay": replay,
            }
        )

    def _append_turn_text(self, active: ActiveTurn, text: str) -> None:
        remaining = self.max_collected_text_chars - active.text_chars
        if remaining <= 0:
            active.text_truncated = True
            return
        kept = text[:remaining]
        active.text_parts.append(kept)
        active.text_chars += len(kept)
        if len(kept) < len(text):
            active.text_truncated = True

    def _track_tool(self, update: JsonObject) -> JsonObject:
        tool_id = update.get("toolCallId")
        if not isinstance(tool_id, str) or not tool_id:
            tool_id = "<unknown>"
        with self._lock:
            previous = dict(self.tools.get(tool_id, {}))
            for key in ("toolCallId", "title", "kind", "status", "locations"):
                if key in update:
                    previous[key] = redact_reasoning(update[key])
            previous.setdefault("toolCallId", tool_id)
            if is_reasoning_discriminator(previous.get("kind")) and "title" in previous:
                previous["title"] = "<redacted>"
            previous["updatedAt"] = utc_timestamp()
            self.tools[tool_id] = previous
            self.tools.move_to_end(tool_id)
            while len(self.tools) > self.max_tracked_tools:
                self.tools.popitem(last=False)
            return dict(previous)

    def _on_request(self, message: JsonObject) -> None:
        rpc_id = message.get("id")
        method = message.get("method")
        params = message.get("params", {})
        try:
            key = request_id_key(rpc_id)
        except ValueError:
            try:
                self.connection.respond_error(
                    None, -32600, "Invalid Request", "Unsupported request ID"
                )
            except AcpError:
                pass
            return

        if method != "session/request_permission":
            self.connection.respond_error(
                rpc_id,
                -32601,
                "Method not found",
                f"The bridge does not advertise or implement client method {method!r}",
            )
            self.emit(
                {
                    "event": "client_request_rejected",
                    "requestId": rpc_id,
                    "method": method,
                    "reason": "unsupported_client_method",
                }
            )
            return
        if not isinstance(params, dict):
            self.connection.respond_error(
                rpc_id, -32602, "Invalid params", "Permission params must be an object"
            )
            return

        with self._lock:
            expected_session = self.session_id or self.requested_session_id
        requested_session = params.get("sessionId")
        if (
            not isinstance(expected_session, str)
            or not isinstance(requested_session, str)
            or requested_session != expected_session
        ):
            self.connection.respond_result(
                rpc_id, {"outcome": {"outcome": "cancelled"}}
            )
            self.emit(
                {
                    "event": "permission_rejected",
                    "requestId": rpc_id,
                    "sessionId": requested_session,
                    "reason": "wrong_session",
                }
            )
            return

        options: Dict[str, JsonObject] = {}
        raw_options = params.get("options")
        if isinstance(raw_options, list):
            for option in raw_options:
                if not isinstance(option, dict):
                    continue
                option_id = option.get("optionId")
                if isinstance(option_id, str) and option_id:
                    options[option_id] = dict(option)
        if not options:
            self.connection.respond_result(
                rpc_id, {"outcome": {"outcome": "cancelled"}}
            )
            self.emit(
                {
                    "event": "permission_rejected",
                    "requestId": rpc_id,
                    "reason": "no_valid_options",
                }
            )
            return

        with self._lock:
            if key in self.pending_permissions:
                self.connection.respond_error(
                    rpc_id, -32600, "Invalid Request", "Duplicate permission request ID"
                )
                return
            if len(self.pending_permissions) >= self.connection.max_pending_requests:
                self.connection.respond_result(
                    rpc_id, {"outcome": {"outcome": "cancelled"}}
                )
                self.emit(
                    {
                        "event": "permission_rejected",
                        "requestId": rpc_id,
                        "reason": "too_many_pending_permissions",
                    }
                )
                return
            timer = threading.Timer(
                self.permission_timeout,
                lambda: self._permission_timeout(key),
            )
            timer.daemon = True
            pending = PendingPermission(
                request_id=rpc_id,
                params=dict(params),
                options=options,
                created_at=utc_timestamp(),
                timer=timer,
            )
            self.pending_permissions[key] = pending
            timer.start()
        self.emit(
            {
                "event": "permission_required",
                "requestId": rpc_id,
                "sessionId": params.get("sessionId"),
                "toolCall": redact_reasoning(params.get("toolCall")),
                "options": list(options.values()),
                "timeoutSeconds": self.permission_timeout,
            }
        )

    def _permission_timeout(self, key: Tuple[str, Any]) -> None:
        pending = self._pop_permission(key, cancel_timer=False)
        if pending is None:
            return
        try:
            self.connection.respond_result(
                pending.request_id, {"outcome": {"outcome": "cancelled"}}
            )
        except AcpError:
            pass
        self.emit(
            {
                "event": "permission_timed_out",
                "requestId": pending.request_id,
                "sessionId": self.session_id,
            }
        )

    def _pop_permission(
        self,
        key: Tuple[str, Any],
        *,
        cancel_timer: bool = True,
    ) -> Optional[PendingPermission]:
        with self._lock:
            pending = self.pending_permissions.pop(key, None)
        if pending is not None and cancel_timer:
            pending.timer.cancel()
        return pending

    def _cancel_all_permissions(self, reason: str) -> None:
        with self._lock:
            pending = list(self.pending_permissions.values())
            self.pending_permissions.clear()
        for item in pending:
            item.timer.cancel()
            try:
                self.connection.respond_result(
                    item.request_id, {"outcome": {"outcome": "cancelled"}}
                )
            except AcpError:
                pass
            try:
                self.emit(
                    {
                        "event": "permission_cancelled",
                        "requestId": item.request_id,
                        "sessionId": self.session_id,
                        "reason": reason,
                    }
                )
            except (BrokenPipeError, OSError):
                pass

    def _on_warning(self, message: str, payload: Optional[JsonObject]) -> None:
        event: JsonObject = {"event": "protocol_warning", "message": message}
        if payload is not None:
            event["payload"] = redact_reasoning(payload)
        try:
            self.emit(event)
        except (BrokenPipeError, OSError):
            pass

    def _on_exit(
        self,
        returncode: Optional[int],
        expected: bool,
        failure: Optional[BaseException],
    ) -> None:
        with self._lock:
            expected = expected or self._shutting_down
            if not expected:
                self.phase = "failed"
                self._unexpected_exit = True
            self.terminal_event.set()
            self._active_done.set()
            permissions = list(self.pending_permissions.values())
            self.pending_permissions.clear()
        for pending in permissions:
            pending.timer.cancel()
        payload: JsonObject = {
            "event": "agent_exit",
            "returncode": returncode,
            "expected": expected,
        }
        if failure is not None:
            payload["error"] = self._error_payload(failure)
        try:
            self.emit(payload)
        except (BrokenPipeError, OSError):
            pass

    def status_snapshot(self) -> JsonObject:
        with self._lock:
            active = self.active_turn
            if active is None:
                turn = None
            else:
                turn = {
                    "commandId": active.command_id,
                    "requestId": active.request_id,
                    "startedAt": active.started_at,
                    "lastActivityAt": active.last_activity_at,
                    "textChars": active.text_chars,
                    "textTruncated": active.text_truncated,
                }
            permissions = [
                {
                    "requestId": pending.request_id,
                    "createdAt": pending.created_at,
                    "options": list(pending.options.values()),
                    "toolCall": redact_reasoning(pending.params.get("toolCall")),
                }
                for pending in self.pending_permissions.values()
            ]
            return {
                "phase": self.phase,
                "sessionId": self.session_id,
                "authMethodId": self.auth_method_id,
                "cwd": str(self.cwd),
                "pid": self.connection.pid,
                "agentAlive": self.connection.alive,
                "lastActivityAt": self.last_activity_at,
                "turn": turn,
                "plan": self.plan,
                "tools": list(self.tools.values()),
                "usage": self.usage,
                "pendingPermissions": permissions,
                "interjectSupport": self.interject_support,
                "launchConfiguration": dict(self.launch_configuration),
            }

    def shutdown(self) -> None:
        with self._lock:
            if self._shutting_down:
                return
            self._shutting_down = True
            self.phase = "closing"
            session_id = self.session_id
            active = self.active_turn is not None
            close_capability = self.agent_capabilities.get("sessionCapabilities")
            can_close = isinstance(close_capability, dict) and isinstance(
                close_capability.get("close"), dict
            )
        try:
            self._cancel_all_permissions("client_shutdown")
        except (BrokenPipeError, OSError):
            pass

        if self.connection.alive and session_id:
            if active:
                try:
                    self.connection.notify(
                        "session/cancel", {"sessionId": session_id}
                    )
                except AcpError:
                    pass
            if can_close:
                try:
                    self.connection.call(
                        "session/close",
                        {"sessionId": session_id},
                        max(0.1, self.shutdown_timeout / 2),
                    )
                except AcpError as exc:
                    self._on_warning("session/close did not complete", {
                        "error": self._error_payload(exc)
                    })
            elif active:
                self._active_done.wait(timeout=max(0.1, self.shutdown_timeout / 2))

        returncode = self.connection.close(timeout=self.shutdown_timeout)
        with self._lock:
            self.phase = "closed"
        try:
            self.emit(
                {
                    "event": "closed",
                    "sessionId": session_id,
                    "returncode": returncode,
                }
            )
        except (BrokenPipeError, OSError):
            pass

    def _command_error(
        self,
        command_id: RequestId,
        op: Optional[str],
        message: str,
        *,
        exception: Optional[BaseException] = None,
        request_id: Optional[int] = None,
    ) -> None:
        payload: JsonObject = {
            "event": "command_error",
            "commandId": command_id,
            "op": op,
            "message": message,
        }
        if request_id is not None:
            payload["requestId"] = request_id
        if exception is not None:
            payload["error"] = self._error_payload(exception)
        self.emit(payload)

    @staticmethod
    def _error_payload(exc: BaseException) -> JsonObject:
        if isinstance(exc, AcpRemoteError):
            return {
                "type": type(exc).__name__,
                "code": exc.code,
                "message": exc.message,
                "data": redact_reasoning(exc.data),
            }
        return {"type": type(exc).__name__, "message": str(exc)}


class JsonlEventSink:
    """Serialize events atomically so callbacks cannot interleave stdout lines."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._sequence = 0

    def __call__(self, event: JsonObject) -> None:
        with self._lock:
            self._sequence += 1
            payload = dict(event)
            payload.setdefault("v", 1)
            payload.setdefault("seq", self._sequence)
            payload.setdefault("timestamp", utc_timestamp())
            data = compact_json(payload)
            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()


class CommandReader:
    """Read bounded JSONL commands without blocking lifecycle monitoring."""

    def __init__(self, max_command_bytes: int) -> None:
        self.max_command_bytes = max_command_bytes
        self.items: "queue.Queue[Tuple[str, Any]]" = queue.Queue(maxsize=128)
        self.thread = threading.Thread(
            target=self._run,
            name="grok-acp-command-reader",
            daemon=True,
        )

    def start(self) -> None:
        self.thread.start()

    def _run(self) -> None:
        stream = sys.stdin.buffer
        while True:
            raw = stream.readline(self.max_command_bytes + 1)
            if not raw:
                self.items.put(("eof", None))
                return
            if len(raw) > self.max_command_bytes:
                while raw and not raw.endswith(b"\n"):
                    raw = stream.readline(self.max_command_bytes + 1)
                self.items.put(
                    (
                        "error",
                        f"Command exceeds {self.max_command_bytes} bytes",
                    )
                )
                continue
            self.items.put(("line", raw))


def write_all(fd: int, payload: bytes) -> None:
    view = memoryview(payload)
    while view:
        written = os.write(fd, view)
        if written <= 0:
            raise OSError("short write to control file")
        view = view[written:]


def nofollow_flag() -> int:
    return int(getattr(os, "O_NOFOLLOW", 0))


@dataclass(frozen=True)
class OwnedControlFile:
    """A task-created, owner-only command file for hosts without writable stdin."""

    path: Path
    device: int
    inode: int

    @classmethod
    def create(cls, value: str) -> "OwnedControlFile":
        if value == "auto":
            parent = Path(tempfile.gettempdir()).resolve(strict=True)
            for _attempt in range(16):
                name = f"grok-acp-{os.getpid()}-{secrets.token_hex(8)}.jsonl"
                try:
                    return cls._create_at(parent / name)
                except FileExistsError:
                    continue
            raise AcpError("Unable to allocate a unique ACP control file")

        requested = Path(value).expanduser()
        if not requested.is_absolute():
            raise ValueError("--control-file must be an absolute path or 'auto'")
        parent = requested.parent.resolve(strict=True)
        if not parent.is_dir():
            raise ValueError(f"Control-file parent is not a directory: {parent}")
        return cls._create_at(parent / requested.name)

    @classmethod
    def _create_at(cls, path: Path) -> "OwnedControlFile":
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow_flag()
        fd = os.open(str(path), flags, 0o600)
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            os.close(fd)
            raise AcpError("Control path did not create a regular file")
        identity: Optional[Tuple[int, int]] = (info.st_dev, info.st_ino)
        try:
            if hasattr(os, "fchmod"):
                os.fchmod(fd, 0o600)
            header = compact_json(
                {
                    "magic": CONTROL_MAGIC,
                    "version": 1,
                    "pid": os.getpid(),
                    "nonce": secrets.token_hex(16),
                    "createdAt": utc_timestamp(),
                }
            )
            write_all(fd, header)
            os.fsync(fd)
        except BaseException:
            try:
                os.close(fd)
            finally:
                if identity is None:
                    try:
                        info = os.lstat(path)
                        identity = (info.st_dev, info.st_ino)
                    except OSError:
                        identity = None
                if identity is not None:
                    try:
                        current = os.lstat(path)
                        if (
                            stat.S_ISREG(current.st_mode)
                            and not stat.S_ISLNK(current.st_mode)
                            and (current.st_dev, current.st_ino) == identity
                        ):
                            os.unlink(path)
                    except OSError:
                        pass
            raise
        else:
            os.close(fd)
        return cls(path=path, device=identity[0], inode=identity[1])

    def matches_path(self) -> bool:
        try:
            info = os.lstat(self.path)
        except OSError:
            return False
        return (
            stat.S_ISREG(info.st_mode)
            and not stat.S_ISLNK(info.st_mode)
            and (info.st_dev, info.st_ino) == (self.device, self.inode)
        )

    def cleanup(self) -> None:
        if self.matches_path():
            os.unlink(self.path)


class ControlCommandReader:
    """Tail a validated control file, waiting for complete newline records."""

    def __init__(
        self,
        control: OwnedControlFile,
        max_command_bytes: int,
    ) -> None:
        self.control = control
        self.max_command_bytes = max_command_bytes
        self.items: "queue.Queue[Tuple[str, Any]]" = queue.Queue(maxsize=128)
        self.stop_event = threading.Event()
        self.thread = threading.Thread(
            target=self._run,
            name="grok-acp-control-reader",
            daemon=True,
        )

    def start(self) -> None:
        self.thread.start()

    def stop(self) -> None:
        self.stop_event.set()
        self.thread.join(timeout=1.0)

    def _run(self) -> None:
        flags = os.O_RDONLY | nofollow_flag()
        try:
            fd = os.open(str(self.control.path), flags)
            info = os.fstat(fd)
            if (info.st_dev, info.st_ino) != (
                self.control.device,
                self.control.inode,
            ):
                os.close(fd)
                raise AcpError("Control file changed before it could be opened")
            stream = os.fdopen(fd, "rb", buffering=0)
            with stream:
                header = stream.readline(4097)
                if len(header) > 4096 or not header.endswith(b"\n"):
                    raise AcpProtocolError("Control-file header is invalid")
                while not self.stop_event.is_set():
                    position = stream.tell()
                    raw = stream.readline(self.max_command_bytes + 1)
                    if not raw:
                        if not self.control.matches_path():
                            raise AcpError("Control file was removed or replaced")
                        self.stop_event.wait(0.1)
                        continue
                    if not raw.endswith(b"\n"):
                        if len(raw) > self.max_command_bytes:
                            self._drain_overlong_line(stream)
                            self.items.put(
                                (
                                    "error",
                                    f"Control command exceeds {self.max_command_bytes} bytes",
                                )
                            )
                        else:
                            if not self.control.matches_path():
                                raise AcpError("Control file was removed or replaced")
                            stream.seek(position)
                            self.stop_event.wait(0.05)
                        continue
                    if len(raw) > self.max_command_bytes:
                        self.items.put(
                            (
                                "error",
                                f"Control command exceeds {self.max_command_bytes} bytes",
                            )
                        )
                        continue
                    self.items.put(("line", raw))
        except BaseException as exc:
            if not self.stop_event.is_set():
                self.items.put(("fatal", str(exc)))

    def _drain_overlong_line(self, stream: Any) -> None:
        while not self.stop_event.is_set():
            chunk = stream.readline(self.max_command_bytes + 1)
            if chunk.endswith(b"\n"):
                return
            if not chunk:
                if not self.control.matches_path():
                    raise AcpError("Control file was removed or replaced")
                self.stop_event.wait(0.05)


def validate_control_file_metadata(info: os.stat_result) -> None:
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise ValueError("Control file must be a regular file, not a symlink")
    if hasattr(os, "getuid") and info.st_uid != os.getuid():
        raise ValueError("Control file is not owned by the current user")
    if os.name == "posix" and stat.S_IMODE(info.st_mode) & 0o077:
        raise ValueError("Control file permissions must not grant group or other access")


def read_control_file_header(path: Path, expected: os.stat_result) -> bytes:
    flags = os.O_RDONLY | nofollow_flag()
    fd = os.open(str(path), flags)
    try:
        opened = os.fstat(fd)
        if (opened.st_dev, opened.st_ino) != (expected.st_dev, expected.st_ino):
            raise ValueError("Control file changed while opening it")
        with os.fdopen(fd, "rb", buffering=0, closefd=False) as stream:
            raw_header = stream.readline(4097)
        if len(raw_header) > 4096 or not raw_header.endswith(b"\n"):
            raise ValueError("Control file has no valid header")
    finally:
        os.close(fd)
    return raw_header


def decode_control_file_header(raw_header: bytes) -> JsonObject:
    try:
        header = json.loads(raw_header)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Control file header is not valid JSON") from exc
    if not isinstance(header, dict) or header.get("magic") != CONTROL_MAGIC:
        raise ValueError("Path is not a Grok ACP bridge control file")
    if header.get("version") != 1:
        raise ValueError(f"Unsupported control-file version: {header.get('version')!r}")
    pid = header.get("pid")
    if isinstance(pid, bool) or not isinstance(pid, int) or pid <= 0:
        raise ValueError("Control file contains no valid bridge PID")
    return header


def validate_bridge_process(pid: int) -> None:
    if os.name == "posix":
        try:
            os.kill(pid, 0)
        except ProcessLookupError as exc:
            raise ValueError(f"Bridge process {pid} is no longer running") from exc
        except PermissionError:
            pass


def inspect_control_file(path_value: str) -> Tuple[Path, os.stat_result, JsonObject]:
    path = Path(path_value).expanduser()
    if not path.is_absolute():
        raise ValueError("--control-file must be an absolute path")
    info = os.lstat(path)
    validate_control_file_metadata(info)
    header = decode_control_file_header(read_control_file_header(path, info))
    validate_bridge_process(header["pid"])
    return path, info, header


def append_control_command(path_value: str, command: JsonObject, limit: int) -> None:
    payload = compact_json(command)
    if len(payload) > limit:
        raise ValueError(f"Command exceeds {limit} bytes")
    path, expected, _header = inspect_control_file(path_value)
    flags = os.O_WRONLY | os.O_APPEND | nofollow_flag()
    fd = os.open(str(path), flags)
    locked = False
    try:
        opened = os.fstat(fd)
        current = os.lstat(path)
        identity = (expected.st_dev, expected.st_ino)
        if (
            (opened.st_dev, opened.st_ino) != identity
            or (current.st_dev, current.st_ino) != identity
            or stat.S_ISLNK(current.st_mode)
        ):
            raise ValueError("Control file changed while opening it for append")
        if os.name == "posix":
            import fcntl

            fcntl.flock(fd, fcntl.LOCK_EX)
            locked = True
        write_all(fd, payload)
        os.fsync(fd)
    finally:
        if locked:
            import fcntl

            fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def resolve_executable(value: str) -> str:
    if os.sep in value or (os.altsep and os.altsep in value):
        path = Path(value).expanduser().resolve(strict=True)
        if not path.is_file():
            raise ValueError(f"Grok executable is not a file: {path}")
        if not os.access(str(path), os.X_OK):
            raise ValueError(f"Grok executable is not executable: {path}")
        return str(path)
    resolved = shutil.which(value)
    if not resolved:
        raise ValueError(f"Unable to find Grok executable: {value}")
    return resolved


def resolve_regular_file(value: str, option: str) -> str:
    path = Path(value).expanduser().resolve(strict=True)
    if not path.is_file():
        raise ValueError(f"{option} is not a file: {path}")
    return str(path)


def build_agent_command(args: argparse.Namespace) -> List[str]:
    command = [resolve_executable(args.grok), "agent", "--no-leader"]
    if args.model:
        command.extend(["--model", args.model])
    if args.reasoning_effort:
        command.extend(["--reasoning-effort", args.reasoning_effort])
    if args.always_approve:
        command.append("--always-approve")
    agent_profile = getattr(args, "agent_profile", None)
    if agent_profile:
        command.extend(
            ["--agent-profile", resolve_regular_file(agent_profile, "--agent-profile")]
        )
    command.append("stdio")
    return command


def build_child_environment(
    args: argparse.Namespace, base: Optional[Dict[str, str]] = None
) -> Dict[str, str]:
    environment = dict(os.environ if base is None else base)
    environment.setdefault("GROK_DISABLE_AUTOUPDATER", "1")
    sandbox = getattr(args, "sandbox", None)
    if sandbox is not None:
        sandbox = sandbox.strip()
        if not sandbox:
            raise ValueError("--sandbox must not be empty")
        environment["GROK_SANDBOX"] = sandbox
    return environment


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def positive_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0 or not parsed < float("inf"):
        raise argparse.ArgumentTypeError("must be a finite number greater than zero")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Keep one grok agent ACP session alive and bridge JSONL commands on "
            "stdin to normalized JSONL events on stdout."
        ),
        epilog=(
            "For background hosts without writable stdin, add --control-file auto "
            "and use: grok_acp.py send --control-file <ready path> --json '<command>'."
        ),
    )
    parser.add_argument("--version", action="version", version=CLIENT_VERSION)
    parser.add_argument("--cwd", default=".", help="Absolute or relative project directory")
    parser.add_argument("--grok", default="grok", help="Path or name of the grok executable")
    parser.add_argument("--session-id", help="Existing ACP session ID to load")
    parser.add_argument(
        "--auth-method",
        help=(
            "Advertised noninteractive ACP auth method; defaults to Grok's "
            "defaultAuthMethodId"
        ),
    )
    parser.add_argument(
        "--control-file",
        help="Owner-only command file path, or 'auto'; keeps running after stdin EOF",
    )
    parser.add_argument("--model", help="Optional Grok model selector")
    parser.add_argument("--reasoning-effort", help="Optional Grok reasoning effort")
    parser.add_argument(
        "--agent-profile",
        help="Trusted grok agent profile file to load explicitly",
    )
    parser.add_argument(
        "--sandbox",
        help="Set GROK_SANDBOX for the child process to the named sandbox profile",
    )
    parser.add_argument(
        "--always-approve",
        action="store_true",
        help="Pass --always-approve to grok agent (explicitly broad authority)",
    )
    parser.add_argument(
        "--startup-timeout",
        type=positive_float,
        default=DEFAULT_STARTUP_TIMEOUT,
    )
    parser.add_argument(
        "--permission-timeout",
        type=positive_float,
        default=DEFAULT_PERMISSION_TIMEOUT,
    )
    parser.add_argument(
        "--shutdown-timeout",
        type=positive_float,
        default=DEFAULT_SHUTDOWN_TIMEOUT,
    )
    parser.add_argument(
        "--max-message-bytes",
        type=positive_int,
        default=DEFAULT_MAX_MESSAGE_BYTES,
    )
    parser.add_argument(
        "--max-command-bytes",
        type=positive_int,
        default=DEFAULT_MAX_COMMAND_BYTES,
    )
    parser.add_argument(
        "--max-prompt-bytes",
        type=positive_int,
        default=DEFAULT_MAX_PROMPT_BYTES,
    )
    parser.add_argument(
        "--max-pending-requests",
        type=positive_int,
        default=DEFAULT_MAX_PENDING_REQUESTS,
    )
    parser.add_argument(
        "--max-tracked-tools",
        type=positive_int,
        default=DEFAULT_MAX_TRACKED_TOOLS,
    )
    parser.add_argument(
        "--max-collected-text-chars",
        type=positive_int,
        default=DEFAULT_MAX_COLLECTED_TEXT_CHARS,
    )
    return parser


def build_send_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="grok_acp.py send",
        description="Append one JSON command to a running bridge control file.",
    )
    parser.add_argument("--control-file", required=True, help="Path from the ready event")
    parser.add_argument("--json", required=True, help="One JSON command object")
    parser.add_argument(
        "--max-command-bytes",
        type=positive_int,
        default=DEFAULT_MAX_COMMAND_BYTES,
    )
    return parser


def run_send(args: argparse.Namespace) -> int:
    try:
        command = json.loads(args.json)
        if not isinstance(command, dict):
            raise ValueError("--json must contain one JSON object")
        append_control_command(args.control_file, command, args.max_command_bytes)
    except (AcpError, OSError, ValueError, json.JSONDecodeError) as exc:
        sys.stdout.buffer.write(
            compact_json({"sent": False, "controlFile": args.control_file, "error": str(exc)})
        )
        sys.stdout.buffer.flush()
        return 2
    sys.stdout.buffer.write(
        compact_json(
            {
                "sent": True,
                "controlFile": args.control_file,
                "commandId": command.get("id"),
                "op": command.get("op"),
            }
        )
    )
    sys.stdout.buffer.flush()
    return 0


def stderr_writer(text: str) -> None:
    with _STDERR_LOCK:
        sys.stderr.write(text)
        sys.stderr.flush()


_STDERR_LOCK = threading.Lock()


def decode_command(raw: bytes) -> Optional[JsonObject]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Command is not valid UTF-8") from exc
    if not text.strip():
        return None
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Command is not valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("Command must be a JSON object")
    return value


def build_launch_configuration(
    args: argparse.Namespace,
    command: Sequence[str],
    child_env: Dict[str, str],
) -> JsonObject:
    resolved_agent_profile = None
    if "--agent-profile" in command:
        resolved_agent_profile = command[command.index("--agent-profile") + 1]
    inherited_sandbox = os.environ.get("GROK_SANDBOX")
    sandbox_source = None
    if args.sandbox is not None:
        sandbox_source = "cli"
    elif inherited_sandbox is not None:
        sandbox_source = "environment"
    return {
        "model": args.model,
        "reasoningEffort": args.reasoning_effort,
        "agentProfile": resolved_agent_profile,
        "sandbox": child_env.get("GROK_SANDBOX"),
        "sandboxSource": sandbox_source,
        "alwaysApprove": bool(args.always_approve),
        "leaderDisabled": True,
    }


def prepare_bridge(
    args: argparse.Namespace, sink: EventCallback
) -> Tuple[GrokAcpBridge, Optional[OwnedControlFile]]:
    cwd = Path(args.cwd).expanduser().resolve(strict=True)
    if not cwd.is_dir():
        raise ValueError(f"--cwd is not a directory: {cwd}")
    command = build_agent_command(args)
    child_env = build_child_environment(args)
    launch_configuration = build_launch_configuration(args, command, child_env)
    connection = JsonRpcConnection(
        command,
        cwd,
        max_message_bytes=args.max_message_bytes,
        max_pending_requests=args.max_pending_requests,
        env=child_env,
        stderr_callback=stderr_writer,
    )
    control = (
        OwnedControlFile.create(args.control_file) if args.control_file else None
    )
    try:
        bridge = GrokAcpBridge(
            connection,
            cwd,
            sink,
            requested_session_id=args.session_id,
            requested_auth_method=args.auth_method,
            startup_timeout=args.startup_timeout,
            permission_timeout=args.permission_timeout,
            shutdown_timeout=args.shutdown_timeout,
            max_prompt_bytes=args.max_prompt_bytes,
            max_tracked_tools=args.max_tracked_tools,
            max_collected_text_chars=args.max_collected_text_chars,
            control_file=control.path if control else None,
            launch_configuration=launch_configuration,
        )
    except BaseException:
        if control is not None:
            try:
                control.cleanup()
            except OSError:
                pass
        raise
    return bridge, control


def cleanup_bridge(
    bridge: GrokAcpBridge, control: Optional[OwnedControlFile]
) -> None:
    try:
        bridge.shutdown()
    finally:
        if control is not None:
            try:
                control.cleanup()
            except OSError as exc:
                stderr_writer(f"Unable to remove ACP control file: {exc}\n")


def install_signal_handlers(
    stop_requested: threading.Event, received_signal: List[int]
) -> Dict[int, Any]:
    def request_stop(signum: int, _frame: Any) -> None:
        received_signal[:] = [signum]
        stop_requested.set()

    old_handlers: Dict[int, Any] = {}
    for signum in (signal.SIGINT, signal.SIGTERM):
        old_handlers[signum] = signal.getsignal(signum)
        signal.signal(signum, request_stop)
    return old_handlers


def restore_signal_handlers(old_handlers: Dict[int, Any]) -> None:
    for signum, handler in old_handlers.items():
        signal.signal(signum, handler)


def next_command_item(
    reader: CommandReader,
    control_reader: Optional[ControlCommandReader],
    stdin_open: bool,
) -> Optional[Tuple[str, Any]]:
    if control_reader is not None:
        try:
            return control_reader.items.get_nowait()
        except queue.Empty:
            pass
    if stdin_open:
        try:
            return reader.items.get(timeout=0.1 if control_reader is not None else 0.2)
        except queue.Empty:
            pass
    if control_reader is not None and not stdin_open:
        try:
            return control_reader.items.get(timeout=0.2)
        except queue.Empty:
            pass
    return None


def dispatch_command_item(
    item: Tuple[str, Any],
    bridge: GrokAcpBridge,
    sink: EventCallback,
    control_reader: Optional[ControlCommandReader],
) -> Tuple[bool, bool, int]:
    """Return (stop loop, stdin remains open, exit code)."""

    kind, value = item
    if kind == "eof":
        return control_reader is None, False, 0
    if kind == "fatal":
        sink({"event": "fatal", "stage": "control", "error": value})
        return True, True, 1
    if kind == "error":
        sink({"event": "command_error", "commandId": None, "message": value})
        return False, True, 0
    try:
        decoded = decode_command(value)
        if decoded is None:
            return False, True, 0
        return bridge.handle_command(decoded), True, 0
    except ValueError as exc:
        sink(
            {
                "event": "command_error",
                "commandId": None,
                "message": str(exc),
            }
        )
        return False, True, 0


def command_loop(
    bridge: GrokAcpBridge,
    sink: EventCallback,
    reader: CommandReader,
    control_reader: Optional[ControlCommandReader],
    stop_requested: threading.Event,
) -> int:
    stdin_open = True
    try:
        while not stop_requested.is_set():
            if bridge.terminal_event.is_set() and bridge.unexpected_exit:
                return 1
            item = next_command_item(reader, control_reader, stdin_open)
            if item is None:
                continue
            should_stop, item_stdin_open, exit_code = dispatch_command_item(
                item, bridge, sink, control_reader
            )
            if item[0] == "eof":
                stdin_open = item_stdin_open
            if should_stop:
                return exit_code
    except (BrokenPipeError, OSError):
        return 1
    return 0


def serve_bridge(
    bridge: GrokAcpBridge,
    args: argparse.Namespace,
    sink: EventCallback,
    control: Optional[OwnedControlFile],
) -> int:
    stop_requested = threading.Event()
    received_signal: List[int] = []
    old_handlers = install_signal_handlers(stop_requested, received_signal)
    reader = CommandReader(args.max_command_bytes)
    control_reader: Optional[ControlCommandReader] = None
    try:
        reader.start()
        if control is not None:
            candidate = ControlCommandReader(control, args.max_command_bytes)
            candidate.start()
            control_reader = candidate
        exit_code = command_loop(
            bridge, sink, reader, control_reader, stop_requested
        )
    finally:
        restore_signal_handlers(old_handlers)
        if control_reader is not None:
            control_reader.stop()
        cleanup_bridge(bridge, control)
    if received_signal:
        return 128 + received_signal[0]
    return exit_code


def run(args: argparse.Namespace) -> int:
    sink = JsonlEventSink()
    try:
        bridge, control = prepare_bridge(args, sink)
    except (AcpError, OSError, ValueError) as exc:
        sink({"event": "fatal", "stage": "arguments", "error": str(exc)})
        return 2

    try:
        bridge.start()
    except BaseException as exc:
        sink(
            {
                "event": "fatal",
                "stage": "startup",
                "error": GrokAcpBridge._error_payload(exc),
            }
        )
        cleanup_bridge(bridge, control)
        return 1
    return serve_bridge(bridge, args, sink, control)


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = list(argv) if argv is not None else sys.argv[1:]
    if arguments and arguments[0] == "send":
        return run_send(build_send_parser().parse_args(arguments[1:]))
    parser = build_parser()
    args = parser.parse_args(arguments)
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
