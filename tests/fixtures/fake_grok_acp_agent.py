#!/usr/bin/env python3
"""Deterministic JSON-RPC fixture for the Grok ACP bridge tests."""

from __future__ import annotations

import json
import os
import sys
import threading
from typing import Any, Dict, Optional


SESSION_ID = "11111111-1111-4111-8111-111111111111"
WRITE_LOCK = threading.Lock()
ACTIVE_PROMPT_ID: Optional[int] = None
ACTIVE_MODE: Optional[str] = None
PERMISSION_ID = "permission-1"
AUTHENTICATED = False
STARTUP_MODE = os.environ.get("FAKE_GROK_STARTUP", "normal")


def send(value: Dict[str, Any]) -> None:
    data = json.dumps(value, separators=(",", ":"), ensure_ascii=False) + "\n"
    with WRITE_LOCK:
        sys.stdout.write(data)
        sys.stdout.flush()


def response(request_id: Any, result: Any) -> None:
    send({"jsonrpc": "2.0", "id": request_id, "result": result})


def update(value: Dict[str, Any]) -> None:
    send(
        {
            "jsonrpc": "2.0",
            "method": "session/update",
            "params": {"sessionId": SESSION_ID, "update": value},
        }
    )


def finish_active(
    stop_reason: str, extra_result: Optional[Dict[str, Any]] = None
) -> None:
    global ACTIVE_MODE, ACTIVE_PROMPT_ID
    request_id = ACTIVE_PROMPT_ID
    ACTIVE_PROMPT_ID = None
    ACTIVE_MODE = None
    if request_id is not None:
        result: Dict[str, Any] = {"stopReason": stop_reason}
        if extra_result:
            result.update(extra_result)
        response(request_id, result)


def prompt_text(params: Any) -> str:
    if not isinstance(params, dict):
        return ""
    prompt = params.get("prompt")
    if not isinstance(prompt, list):
        return ""
    for block in prompt:
        if isinstance(block, dict) and block.get("type") == "text":
            text = block.get("text")
            if isinstance(text, str):
                return text
    return ""


def request_permission(session_id: str) -> None:
    send(
        {
            "jsonrpc": "2.0",
            "id": PERMISSION_ID,
            "method": "session/request_permission",
            "params": {
                "sessionId": session_id,
                "toolCall": {
                    "toolCallId": "tool-permission",
                    "title": "Write file",
                    "status": "pending",
                    "rawInput": {"path": "owned.txt"},
                },
                "options": [
                    {
                        "optionId": "allow-once",
                        "name": "Allow once",
                        "kind": "allow_once",
                    },
                    {
                        "optionId": "reject-once",
                        "name": "Reject",
                        "kind": "reject_once",
                    },
                ],
            },
        }
    )


def error_response(request_id: Any, code: int, message: str) -> None:
    send(
        {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": code, "message": message},
        }
    )


def handle_initialize(request_id: Any) -> None:
    if STARTUP_MODE == "malformed":
        sys.stdout.write("{not-json\n")
        sys.stdout.flush()
        return
    if STARTUP_MODE == "oversize":
        response(
            request_id,
            {
                "protocolVersion": 1,
                "agentCapabilities": {},
                "padding": "x" * 4096,
            },
        )
        return
    auth_fields: Dict[str, Any] = {}
    if STARTUP_MODE != "legacy-no-auth":
        auth_fields["authMethods"] = [
            {"id": "cached_token", "name": "Cached token"},
            {"id": "grok.com", "name": "Log in with grok.com"},
        ]
    meta = {"agentVersion": "test"}
    if STARTUP_MODE == "auth-interactive-default":
        meta["defaultAuthMethodId"] = "grok.com"
    elif STARTUP_MODE not in {"legacy-no-auth", "auth-no-default"}:
        meta["defaultAuthMethodId"] = "cached_token"
    response(
        request_id,
        {
            "protocolVersion": 1,
            "agentCapabilities": {
                "loadSession": True,
                "sessionCapabilities": {"close": {}, "resume": {}},
            },
            "agentInfo": {
                "name": "fake-grok",
                "title": "Fake Grok",
                "version": "test",
            },
            "_meta": meta,
            **auth_fields,
        },
    )


def handle_authenticate(request_id: Any, params: Any) -> None:
    global AUTHENTICATED
    method_id = params.get("methodId") if isinstance(params, dict) else None
    metadata = params.get("_meta") if isinstance(params, dict) else None
    if (
        STARTUP_MODE == "auth-rejected"
        or method_id != "cached_token"
        or not isinstance(metadata, dict)
        or metadata.get("headless") is not True
    ):
        error_response(request_id, -32001, "noninteractive authentication required")
        return
    AUTHENTICATED = True
    response(request_id, {})


def authentication_ready(request_id: Any) -> bool:
    if STARTUP_MODE == "legacy-no-auth" or AUTHENTICATED:
        return True
    error_response(request_id, -32001, "authenticate first")
    return False


def handle_session_load(request_id: Any) -> None:
    if not authentication_ready(request_id):
        return
    update(
        {
            "sessionUpdate": "agent_thought_chunk",
            "content": {"type": "text", "text": "historical secret reasoning"},
        }
    )
    update(
        {
            "sessionUpdate": "agent_message_chunk",
            "messageId": "history-1",
            "content": {"type": "text", "text": "historical answer"},
        }
    )
    response(request_id, None)


def emit_complete_turn() -> None:
    update(
        {
            "sessionUpdate": "plan",
            "entries": [{"content": "Inspect", "status": "in_progress"}],
        }
    )
    update(
        {
            "sessionUpdate": "tool_call",
            "toolCallId": "tool-1",
            "title": "Read a file",
            "kind": "read",
            "status": "pending",
            "rawInput": {"path": "demo.py"},
        }
    )
    update(
        {
            "sessionUpdate": "tool_call_update",
            "toolCallId": "tool-1",
            "status": "completed",
        }
    )
    update(
        {
            "sessionUpdate": "agent_message_chunk",
            "messageId": "message-1",
            "content": {"type": "text", "text": "hello"},
        }
    )
    finish_active(
        "end_turn", {"reasoning": "SENTINEL_PRIVATE_REASONING_RESULT"}
    )


def emit_think_tool_turn() -> None:
    update(
        {
            "sessionUpdate": "agent_message_chunk",
            "messageId": "message-reasoning",
            "content": {
                "type": "reasoning",
                "text": "SENTINEL_PRIVATE_REASONING_MESSAGE",
            },
        }
    )
    update(
        {
            "sessionUpdate": "tool_call",
            "toolCallId": "tool-think",
            "title": "Private analysis",
            "kind": "think",
            "status": "in_progress",
            "rawInput": {"text": "SENTINEL_PRIVATE_REASONING_INPUT"},
        }
    )
    update(
        {
            "sessionUpdate": "tool_call_update",
            "toolCallId": "tool-think",
            "status": "completed",
            "rawOutput": {"text": "SENTINEL_PRIVATE_REASONING_OUTPUT"},
            "content": [
                {"type": "text", "text": "SENTINEL_PRIVATE_REASONING_OUTPUT"}
            ],
        }
    )
    finish_active("end_turn")


def emit_unknown_update_turn() -> None:
    update(
        {
            "sessionUpdate": "future_event",
            "value": 42,
            "reasoning": "must not leak",
        }
    )
    send(
        {
            "jsonrpc": "2.0",
            "method": "_x.ai/session/update",
            "params": {
                "sessionId": SESSION_ID,
                "update": {
                    "sessionUpdate": "agent_thought_chunk",
                    "content": {
                        "type": "text",
                        "text": "extension thought must not leak",
                    },
                },
            },
        }
    )
    finish_active("end_turn")


def emit_waiting_turn() -> None:
    update(
        {
            "sessionUpdate": "tool_call",
            "toolCallId": "tool-wait",
            "title": "Waiting",
            "kind": "other",
            "status": "in_progress",
        }
    )
    update(
        {
            "sessionUpdate": "agent_message_chunk",
            "messageId": "message-wait",
            "content": {"type": "text", "text": "working"},
        }
    )


def handle_prompt(request_id: Any, params: Any) -> None:
    global ACTIVE_MODE, ACTIVE_PROMPT_ID
    if ACTIVE_PROMPT_ID is not None:
        error_response(request_id, -32000, "prompt already active")
        return
    mode = prompt_text(params)
    ACTIVE_PROMPT_ID = request_id
    ACTIVE_MODE = mode
    if mode == "crash":
        os._exit(7)
    update(
        {
            "sessionUpdate": "agent_thought_chunk",
            "content": {"type": "text", "text": "private chain of thought"},
        }
    )
    if mode == "complete":
        emit_complete_turn()
    elif mode == "permission":
        request_permission(SESSION_ID)
    elif mode == "wrong-session-permission":
        request_permission("another-session")
    elif mode == "think-tool":
        emit_think_tool_turn()
    elif mode == "unknown-update":
        emit_unknown_update_turn()
    else:
        emit_waiting_turn()


def handle_interject(request_id: Any) -> None:
    if ACTIVE_MODE == "no-interject":
        error_response(request_id, -32601, "Method not found")
        return
    response(request_id, {"status": "queued"})
    update(
        {
            "sessionUpdate": "agent_message_chunk",
            "messageId": "message-steered",
            "content": {"type": "text", "text": ":steered"},
        }
    )
    finish_active("end_turn")


def handle_request(message: Dict[str, Any]) -> None:
    request_id = message.get("id")
    method = message.get("method")
    params = message.get("params")
    if method == "initialize":
        handle_initialize(request_id)
    elif method == "authenticate":
        handle_authenticate(request_id, params)
    elif method == "session/new":
        if authentication_ready(request_id):
            response(request_id, {"sessionId": SESSION_ID})
    elif method == "session/load":
        handle_session_load(request_id)
    elif method == "session/prompt":
        handle_prompt(request_id, params)
    elif method == "_x.ai/interject":
        handle_interject(request_id)
    elif method == "session/close":
        finish_active("cancelled")
        response(request_id, {})
    else:
        error_response(request_id, -32601, f"Unknown method: {method}")


def handle_message(message: Dict[str, Any]) -> None:
    if "method" in message:
        method = message.get("method")
        if "id" in message:
            handle_request(message)
        elif method == "session/cancel":
            finish_active("cancelled")
        return

    if message.get("id") == PERMISSION_ID and "result" in message:
        outcome = message.get("result", {}).get("outcome", {})
        selected = outcome.get("optionId", outcome.get("outcome", "unknown"))
        update(
            {
                "sessionUpdate": "agent_message_chunk",
                "messageId": "message-permission",
                "content": {"type": "text", "text": f"permission:{selected}"},
            }
        )
        finish_active("end_turn")


def main() -> int:
    sys.stderr.write("fake grok stderr remains separate\n")
    sys.stderr.flush()
    for line in sys.stdin:
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            return 2
        if isinstance(value, dict):
            handle_message(value)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
