"""Narrow, tool-free adapters for the official installed Claude and Grok CLIs."""
from __future__ import annotations

from pathlib import Path

from cli_runtime import (CliError, checked_text, claude_command, exact_session,
                         executable, parse_claude, probe, probe_flags)

# Invocation-local feature restrictions. Never change HOME, GROK_HOME, credentials,
# persistent settings, active contexts, or user/project files to manufacture safety.
GROK_ENV = {
    "GROK_MEMORY": "0", "GROK_SUBAGENTS": "0", "GROK_WEB_FETCH": "0",
    "GROK_WRITE_FILE": "0", "GROK_TOOL_SEARCH": "0", "GROK_LSP_TOOLS": "0",
    "GROK_DISABLE_AUTOUPDATER": "1",
}


def command_for(provider: str, config: dict, prompt_file: Path,
                session_id: str | None) -> tuple[list[str], Path | None, dict[str, str]]:
    if provider == "claude":
        return (claude_command(config["claude_bin"], session_id=session_id,
                               model=config.get("claude_model"), effort=config.get("claude_effort"),
                               tools="none", max_turns=config["max_agent_turns"]), prompt_file, {})
    if provider != "grok":
        raise CliError(f"Unknown provider: {provider}")
    sandbox = config["grok_sandbox"]
    if sandbox not in {"read-only", "strict", "off"}:
        raise CliError("Unsupported Grok sandbox profile.")
    command = [config["grok_bin"], "--cwd", config["cwd"],
               "--prompt-file", str(prompt_file), "--output-format", "json",
               "--tools", "", "--no-subagents", "--disable-web-search",
               "--permission-mode", "dontAsk", "--deny", "MCPTool",
               "--sandbox", sandbox, "--max-turns", str(config["max_agent_turns"]),
               "--no-auto-update"]
    if session_id:
        command += ["--resume", exact_session(session_id)]
    for key, flag in (("grok_model", "--model"), ("grok_effort", "--effort")):
        value = config.get(key)
        if value:
            if not isinstance(value, str) or value.startswith("-") or "\0" in value:
                raise CliError(f"Invalid {key}.")
            command += [flag, value]
    return command, None, GROK_ENV.copy()


def parse_result(provider: str, payload: object, expected_session: str | None = None) -> dict:
    if provider == "claude":
        return parse_claude(payload, expected_session)
    if provider != "grok" or not isinstance(payload, dict):
        raise CliError("Grok JSON must be one terminal object.")
    # Do not silently treat unknown/new stop reasons as successful completion.
    if payload.get("stopReason") != "end_turn" or payload.get("error") or payload.get("is_error"):
        raise CliError(f"Grok did not complete normally (stopReason={payload.get('stopReason')!r}); inspect artifacts.")
    text, session = payload.get("text"), payload.get("sessionId")
    if not isinstance(text, str) or not text.strip() or not isinstance(session, str):
        raise CliError("Grok result requires nonempty text and sessionId.")
    exact_session(session)
    if expected_session and expected_session != session:
        raise CliError("Grok returned a different session ID from the requested resume ID.")
    return {"text": checked_text(text), "session_id": session, "stop_reason": "end_turn",
            "usage": payload.get("usage"), "model_usage": payload.get("modelUsage"),
            "usage_is_incomplete": payload.get("usage_is_incomplete"),
            "cost_is_partial": payload.get("cost_is_partial")}


def doctor(cwd: Path, claude_bin: str, grok_bin: str) -> dict:
    result = {"cwd": str(cwd), "providers": {}, "ready": True,
              "notice": "Metadata probes only; no model calls. Review Grok inspect and managed Claude policies before approving config. Never paste this private inspection into model prompts."}
    for provider, value in (("claude", claude_bin), ("grok", grok_bin)):
        try:
            binary = executable(value)
            version_command = [binary, "--version"] if provider == "claude" else [binary, "version", "--json"]
            version = probe(version_command, cwd)
            help_result = probe([binary, "--help"], cwd)
            required = (["--output-format", "--safe-mode", "--tools", "--resume", "--strict-mcp-config"]
                        if provider == "claude" else ["--prompt-file", "--output-format", "--tools", "--resume", "--sandbox", "--permission-mode"])
            detail = {"binary": binary, "version": version, "help": help_result,
                      "not_advertised_in_help": probe_flags(help_result["stdout"], required)}
            probes = [version, help_result]
            if provider == "grok":
                detail["inspect"] = probe([binary, "--cwd", str(cwd), "inspect", "--json"], cwd)
                probes.append(detail["inspect"])
            if any(item["returncode"] != 0 or item["failure"] for item in probes):
                result["ready"] = False
            result["providers"][provider] = detail
        except (CliError, OSError) as exc:
            result["providers"][provider] = {"error": str(exc)}
            result["ready"] = False
    return result
