"""Small stdlib-only CLI transport. Kept identical in the two standalone skills.

No SDK, shell interpolation, credential discovery, config mutation, or retries.
The caller owns authorization, prompt selection, and any retained artifacts.
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import signal
import stat
import subprocess
import tempfile
import time
from typing import Callable, Iterator
import uuid

MAX_INPUT = 2 * 1024 * 1024
MAX_OUTPUT = 8 * 1024 * 1024


class CliError(RuntimeError):
    """An actionable failure, never a successful model contribution."""


def utc_now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def encode_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"


def digest(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def text_digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def checked_text(text: str, limit: int = MAX_INPUT) -> str:
    if not text.strip():
        raise CliError("Input must not be blank.")
    if "\0" in text:
        raise CliError("NUL bytes are not supported in text input.")
    if len(text.encode("utf-8")) > limit:
        raise CliError(f"Input exceeds {limit} bytes; nothing was truncated or sent.")
    return text


def read_text(path: Path, limit: int = MAX_INPUT) -> str:
    # Open nonblocking first, then fstat: opening a FIFO normally could hang
    # before a regular-file check. Symlinks to user-supplied input files are OK.
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    with os.fdopen(os.open(path, flags), "rb") as handle:
        if not stat.S_ISREG(os.fstat(handle.fileno()).st_mode):
            raise CliError(f"Not a regular file: {path}")
        raw = handle.read(limit + 1)
    if len(raw) > limit:
        raise CliError(f"File exceeds {limit} bytes: {path}")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CliError(f"Expected UTF-8 text: {path}") from exc


def read_json(path: Path, limit: int = MAX_OUTPUT) -> object:
    def reject_constant(token: str) -> None:
        raise ValueError(token)
    try:
        return json.loads(read_text(path, limit), parse_constant=reject_constant)
    except (ValueError, TypeError) as exc:
        raise CliError(f"Invalid JSON: {path}") from exc


def private_file(path: Path):
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    flags |= getattr(os, "O_NOFOLLOW", 0)
    return os.fdopen(os.open(path, flags, 0o600), "wb")


def atomic_text(path: Path, text: str) -> None:
    """Replace only an artifact owned by this run; never follow its symlink."""
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise CliError(f"Refusing non-regular output: {path}")
    fd, temp_name = tempfile.mkstemp(prefix=".write-", dir=path.parent)
    temporary = Path(temp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(text.encode("utf-8"))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        if os.name == "posix":
            descriptor = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
    finally:
        if temporary.exists():
            temporary.unlink()  # Only the private file created by this function.


def atomic_json(path: Path, value: object) -> None:
    atomic_text(path, encode_json(value))


@contextlib.contextmanager
def exclusive_lock(path: Path) -> Iterator[None]:
    """OS-released lock. Keep the inode; deleting lock files introduces races."""
    flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags, 0o600)
    if not stat.S_ISREG(os.fstat(fd).st_mode):
        os.close(fd)
        raise CliError(f"Not a regular lock file: {path}")
    with os.fdopen(fd, "r+b") as handle:
        if os.name == "nt":
            import msvcrt
            if os.fstat(handle.fileno()).st_size == 0:
                handle.write(b"0")
                handle.flush()
            handle.seek(0)
            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as exc:
                raise CliError("Another process owns this run; no changes were made.") from exc
            try:
                yield
            finally:
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as exc:
                raise CliError("Another process owns this run; no changes were made.") from exc
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def executable(value: str) -> str:
    found = shutil.which(value)
    if not found:
        raise CliError(f"Executable not found: {value}. Install/login separately; this helper will not do it.")
    path = Path(found).resolve()
    if path.suffix.lower() in {".bat", ".cmd"}:
        raise CliError("Use the native CLI executable, not a .bat/.cmd shim. Shell execution is intentionally disabled.")
    return str(path)


def exact_session(value: str) -> str:
    # UUID-only prevents accidentally invoking a name search or a session picker.
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError) as exc:
        raise CliError("An exact UUID session ID is required; names/latest are not accepted.") from exc
    if str(parsed) != value.lower():
        raise CliError("Use the canonical hyphenated UUID returned by the CLI.")
    return value


def positive_number(value: float, label: str) -> float:
    if not math.isfinite(value) or value <= 0:
        raise CliError(f"{label} must be finite and positive.")
    return value


def claude_command(binary: str, *, session_id: str | None = None,
                   model: str | None = None, effort: str | None = None,
                   tools: str = "none", max_turns: int = 4) -> list[str]:
    if tools not in {"none", "read"}:
        raise CliError("Only tool-free and read-only built-in tool profiles are supported.")
    if not 1 <= max_turns <= 50:
        raise CliError("max_turns must be between 1 and 50.")
    selected = "" if tools == "none" else "Read,Glob,Grep"
    command = [binary, "-p", "--output-format", "json", "--safe-mode",
               "--tools", selected, "--permission-mode", "dontAsk",
               "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
               "--disallowedTools", "mcp__*", "--disable-slash-commands",
               "--no-chrome", "--settings", '{"disableAllHooks":true}',
               "--max-turns", str(max_turns)]
    if selected:
        command += ["--allowedTools", selected]
    if session_id:
        command += ["--resume", exact_session(session_id)]
    for flag, value in [("--model", model), ("--effort", effort)]:
        if value:
            if value.startswith("-") or "\0" in value:
                raise CliError(f"Invalid {flag} value.")
            command += [flag, value]
    return command


def _terminate(proc: subprocess.Popen, grace: float = 2.0) -> None:
    """Terminate only the process/group this invocation just created."""
    if os.name == "posix":
        try:
            os.killpg(proc.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            proc.wait(timeout=grace)
        except subprocess.TimeoutExpired:
            pass
        # The leader may exit before a descendant; finish the owned group too.
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    else:
        # Native Windows: kill the owned CLI process. No claim of tree isolation.
        if proc.poll() is None:
            proc.terminate()
        try:
            proc.wait(timeout=grace)
        except subprocess.TimeoutExpired:
            proc.kill()
    proc.wait()


def run_process(command: list[str], *, cwd: Path, directory: Path,
                input_file: Path | None = None, timeout: float = 240.0,
                env_overrides: dict[str, str] | None = None,
                on_start: Callable[[int], None] | None = None,
                output_limit: int = MAX_OUTPUT) -> dict:
    """Capture stdout/stderr separately; no prompt in argv, no automatic retries.

    The output cap is monitored every 50ms, so a burst may overshoot it on disk.
    Parsing remains bounded. Directory must already exist and be caller-owned.
    """
    positive_number(timeout, "timeout")
    if not cwd.is_dir():
        raise CliError(f"Working directory does not exist: {cwd}")
    if output_limit < 1:
        raise CliError("output_limit must be positive.")
    env = os.environ.copy()
    env.update(env_overrides or {})
    stdout = directory / "stdout.json"
    stderr = directory / "stderr.log"
    started = time.monotonic()
    reason = None
    proc = None
    with contextlib.ExitStack() as stack:
        # A normal supervisor SIGTERM must stop our owned child rather than
        # orphaning it. This is local to this transport invocation.
        import threading
        if threading.current_thread() is threading.main_thread():
            previous = signal.getsignal(signal.SIGTERM)
            def interrupted(signum: int, frame: object) -> None:
                raise KeyboardInterrupt
            signal.signal(signal.SIGTERM, interrupted)
            stack.callback(signal.signal, signal.SIGTERM, previous)
        out = stack.enter_context(private_file(stdout))
        err = stack.enter_context(private_file(stderr))
        source = stack.enter_context(input_file.open("rb")) if input_file else subprocess.DEVNULL
        try:
            proc = subprocess.Popen(command, cwd=cwd, env=env, stdin=source,
                                    stdout=out, stderr=err, shell=False,
                                    start_new_session=(os.name == "posix"))
            if on_start:
                on_start(proc.pid)
            while proc.poll() is None:
                if time.monotonic() - started > timeout:
                    reason = "timeout"
                    _terminate(proc)
                    break
                if stdout.stat().st_size > output_limit or stderr.stat().st_size > output_limit:
                    reason = "output_limit"
                    _terminate(proc)
                    break
                time.sleep(0.05)
            if stdout.stat().st_size > output_limit or stderr.stat().st_size > output_limit:
                reason = reason or "output_limit"
        except KeyboardInterrupt:
            reason = "interrupted"
            if proc:
                _terminate(proc)
        except BaseException:
            if proc:
                _terminate(proc)
            raise
        finally:
            out.flush()
            err.flush()
            os.fsync(out.fileno())
            os.fsync(err.fileno())
    outcome = {"returncode": proc.returncode if proc else None, "failure": reason,
               "elapsed_seconds": round(time.monotonic() - started, 3),
               "completed_at": utc_now()}
    atomic_json(directory / "outcome.json", outcome)
    return outcome


def parse_claude(payload: object, expected_session: str | None = None) -> dict:
    if not isinstance(payload, dict):
        raise CliError("Claude JSON must be one terminal object, not text, an array, or a stream.")
    if payload.get("type") != "result" or payload.get("subtype") != "success" or payload.get("is_error") is not False:
        raise CliError("Claude did not return a successful terminal result; inspect stdout.json and stderr.log.")
    if payload.get("stop_reason") not in (None, "end_turn", "stop_sequence"):
        raise CliError(f"Claude returned an incomplete stop reason: {payload.get('stop_reason')!r}")
    if payload.get("permission_denials"):
        raise CliError("Claude encountered permission denials; the contribution was not accepted as complete.")
    text = payload.get("result")
    session = payload.get("session_id")
    if not isinstance(text, str) or not text.strip() or not isinstance(session, str):
        raise CliError("Claude result requires nonempty result text and a session_id.")
    exact_session(session)
    if expected_session and session != expected_session:
        raise CliError("Claude returned a different session ID from the requested resume ID.")
    return {"text": checked_text(text), "session_id": session,
            "stop_reason": payload.get("stop_reason", "success"),
            "usage": payload.get("usage"), "model_usage": payload.get("modelUsage"),
            "reported_cost_usd": payload.get("total_cost_usd")}


def completed_payload(directory: Path) -> object:
    outcome = read_json(directory / "outcome.json")
    if not isinstance(outcome, dict) or outcome.get("failure") or outcome.get("returncode") != 0:
        raise CliError(f"CLI call failed or was interrupted. Inspect {directory}; no automatic retry was attempted.")
    return read_json(directory / "stdout.json")


def probe(command: list[str], cwd: Path) -> dict:
    """Read-only CLI metadata probe, with its own bounded temporary output."""
    with tempfile.TemporaryDirectory(prefix="agent-cli-probe-") as folder:
        directory = Path(folder)
        outcome = run_process(command, cwd=cwd, directory=directory, timeout=30)
        return {"command": command, **outcome,
                "stdout": read_text(directory / "stdout.json", MAX_OUTPUT),
                "stderr": read_text(directory / "stderr.log", MAX_OUTPUT)}


def probe_flags(help_text: str, flags: list[str]) -> list[str]:
    """Diagnostic only: some official flags are deliberately hidden from help."""
    return [flag for flag in flags if not re.search(re.escape(flag) + r"(?=[\s=,\[<]|$)", help_text)]
