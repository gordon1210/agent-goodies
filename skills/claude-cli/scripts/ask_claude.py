#!/usr/bin/env python3
"""Invoke the installed Claude Code CLI with -p; Python 3.10+, stdlib only."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import tempfile

from cli_runtime import (CliError, MAX_INPUT, atomic_json, atomic_text, checked_text,
                         claude_command, completed_payload, encode_json,
                         executable, parse_claude, probe, probe_flags, read_text,
                         run_process, text_digest)


def doctor(binary: str, cwd: Path) -> dict:
    version = probe([binary, "--version"], cwd)
    help_result = probe([binary, "--help"], cwd)
    flags = ["--output-format", "--safe-mode", "--tools", "--resume",
             "--permission-mode", "--strict-mcp-config", "--settings"]
    return {"binary": binary, "cwd": str(cwd), "version": version,
            "help": help_result,
            "not_advertised_in_help": probe_flags(help_result["stdout"], flags),
            "note": "Metadata only, not a live authenticated smoke test. Some flags may be hidden; unsupported flags fail without fallback. Managed policy still applies."}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    for action in ("doctor", "ask"):
        part = sub.add_parser(action)
        part.add_argument("--claude-bin", default="claude")
        part.add_argument("--cwd", type=Path, default=Path.cwd())
        if action == "ask":
            source = part.add_mutually_exclusive_group(required=True)
            source.add_argument("--prompt", help="For short non-sensitive input; otherwise use a file or stdin.")
            source.add_argument("--prompt-file", type=Path)
            source.add_argument("--stdin", action="store_true")
            part.add_argument("--resume", help="Exact returned UUID, not a title or latest session.")
            part.add_argument("--model")
            part.add_argument("--effort")
            part.add_argument("--tools", choices=("none", "read"), default="none")
            part.add_argument("--max-turns", type=int, default=4)
            part.add_argument("--timeout", type=float, default=240)
            part.add_argument("--out-dir", type=Path, help="New artifact directory; never overwrite an existing directory.")
            part.add_argument("--dry-run", action="store_true")
            part.add_argument("--text", action="store_true", help="Print only the answer; metadata remains in result.json.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        cwd = args.cwd.expanduser().resolve(strict=True)
        binary = executable(args.claude_bin)
        if args.action == "doctor":
            result = doctor(binary, cwd)
            print(encode_json(result), end="")
            return 0 if all(result[key]["returncode"] == 0 and not result[key]["failure"] for key in ("version", "help")) else 1
        if args.stdin:
            prompt = sys.stdin.read(MAX_INPUT + 1)
        elif args.prompt_file:
            prompt = read_text(args.prompt_file)
        else:
            prompt = args.prompt
        checked_text(prompt)
        command = claude_command(binary, session_id=args.resume, model=args.model,
                                 effort=args.effort, tools=args.tools, max_turns=args.max_turns)
        request = {"command": command, "cwd": str(cwd), "prompt_sha256": text_digest(prompt),
                   "input_transport": "stdin", "tool_profile": args.tools,
                   "prompt_bytes": len(prompt.encode("utf-8"))}
        if args.dry_run:
            print(encode_json(request), end="")
            return 0
        if args.out_dir:
            if args.out_dir.is_symlink():
                raise CliError("Refusing a symlink output directory.")
            directory = args.out_dir.expanduser().absolute()
            directory.mkdir(mode=0o700, exist_ok=False)
        else:
            directory = Path(tempfile.mkdtemp(prefix="claude-cli-"))
        print(f"Claude CLI artifacts: {directory}", file=sys.stderr)
        atomic_text(directory / "prompt.txt", prompt)
        atomic_json(directory / "request.json", request)
        run_process(command, cwd=cwd, directory=directory, input_file=directory / "prompt.txt", timeout=args.timeout)
        result = parse_claude(completed_payload(directory), args.resume)
        result["artifact_dir"] = str(directory)
        atomic_json(directory / "result.json", result)
        print(result["text"] if args.text else encode_json(result), end="\n" if args.text else "")
        return 0
    except (CliError, OSError, ValueError) as exc:
        print(f"claude-cli: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("claude-cli: interrupted; inspect retained artifacts before another call.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
