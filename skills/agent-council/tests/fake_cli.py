#!/usr/bin/env python3
"""Offline CLI fixture, never a real model. Driven by adjacent control.json."""
import json
import os
from pathlib import Path
import sys
import time
import uuid

args = sys.argv[1:]
provider = "claude" if "claude" in Path(sys.argv[0]).name else "grok"
base = Path(sys.argv[0]).parent
control_file = base / "control.json"
control = json.loads(control_file.read_text()) if control_file.exists() else {}

def value(flag):
    return args[args.index(flag) + 1] if flag in args else None

if "--help" in args:
    print("--output-format --safe-mode --tools --resume --strict-mcp-config --settings --permission-mode --prompt-file --sandbox --max-turns --no-auto-update --no-chrome --disable-slash-commands --mcp-config --disallowedTools --model --effort --allowedTools")
    sys.exit(0)
if "--version" in args or "version" in args:
    print("Claude fixture 0.0.0" if provider == "claude" else '{"version":"1.0.13-fixture"}')
    sys.exit(0)
if "inspect" in args:
    print('{"hooks":[],"plugins":[],"mcpServers":[],"fixture":true}')
    sys.exit(0)

prompt_file = value("--prompt-file")
prompt = Path(prompt_file).read_text(encoding="utf-8") if prompt_file else sys.stdin.read()
resume = value("--resume")
session = resume or str(uuid.uuid4())
log = base / "calls.jsonl"
existing = log.read_text().splitlines() if log.exists() else []
record = {"provider": provider, "args": args, "prompt": prompt, "session": session,
          "cwd": os.getcwd(), "number": len(existing) + 1,
          "grok_memory": os.environ.get("GROK_MEMORY")}
with log.open("a", encoding="utf-8") as handle:
    handle.write(json.dumps(record, ensure_ascii=False) + "\n")
mode = control.get("mode", "success")
if control.get("provider", provider) != provider or control.get("call", len(existing) + 1) != len(existing) + 1:
    mode = "success"
if mode == "sleep":
    time.sleep(20)
if mode == "huge":
    print("x" * (10 * 1024 * 1024))
    sys.exit(0)
if mode == "malformed":
    print("not JSON")
    sys.exit(0)
if mode == "banner":
    print("unexpected banner before result")
if mode == "different-session":
    session = str(uuid.uuid4())
seen = "unknown"
if "COUNCIL INPUT (JSON)\n" in prompt:
    packet = json.loads(prompt.split("COUNCIL INPUT (JSON)\n", 1)[1])
    seen = str(packet["seen_through"])
text = f"{provider} fixture response, input through {seen}. Unicode: Café — ∑∞. This is an offline fixture, not model reasoning."
if mode == "blank":
    text = " "
if mode == "overlong":
    text = "x" * (65 * 1024)
if provider == "claude":
    output = {"type": "result", "subtype": "success", "is_error": False,
              "result": text, "session_id": session, "stop_reason": "end_turn",
              "usage": {"input_tokens": 100, "output_tokens": 30}}
    if mode == "error":
        output.update(subtype="error_max_turns", is_error=True)
    if mode == "incomplete":
        output["stop_reason"] = "max_tokens"
else:
    output = {"text": text, "sessionId": session, "stopReason": "end_turn",
              "usage": {"input_tokens": 100, "output_tokens": 30}}
    if mode in {"error", "incomplete"}:
        output["stopReason"] = "permission_cancelled"
if mode == "missing-session":
    output.pop("session_id" if provider == "claude" else "sessionId")
print(json.dumps(output, ensure_ascii=False))
print("fixture stderr, not part of model output", file=sys.stderr)
sys.exit(3 if mode == "nonzero" else 0)
