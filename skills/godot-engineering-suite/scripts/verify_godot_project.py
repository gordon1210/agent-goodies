#!/usr/bin/env python3
"""Run explicit, bounded Godot CLI verification for a project.

Only the `version` mode is non-project-executing. Import, startup, and scene
modes may execute editor plugins, @tool scripts, autoloads, project scripts, or
native extensions. They therefore require --acknowledge-project-code.
"""

from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path


def find_project_root(start: Path) -> Path:
    candidate = start.expanduser().resolve()
    if candidate.is_file():
        candidate = candidate.parent
    for directory in (candidate, *candidate.parents):
        if (directory / "project.godot").is_file():
            return directory
    raise FileNotFoundError(f"No project.godot found at or above {candidate}")


def executable_candidates(explicit: str | None) -> list[str]:
    values: list[str] = []
    for value in (explicit, os.environ.get("GODOT_BIN"), os.environ.get("GODOT_PATH")):
        if value:
            values.append(value)

    for name in ("godot", "godot4"):
        found = shutil.which(name)
        if found:
            values.append(found)

    home = Path.home()
    if sys.platform == "darwin":
        values.extend(
            [
                "/Applications/Godot.app/Contents/MacOS/Godot",
                str(home / "Applications/Godot.app/Contents/MacOS/Godot"),
            ]
        )
    elif os.name == "nt":
        values.extend(
            [
                r"C:\Program Files\Godot\Godot.exe",
                r"C:\Program Files\Godot\Godot_v4.exe",
                str(home / "Godot/Godot.exe"),
            ]
        )
    else:
        values.extend(["/usr/bin/godot", "/usr/local/bin/godot", "/snap/bin/godot"])

    # Preserve order while removing duplicates.
    return list(dict.fromkeys(values))


def resolve_executable(explicit: str | None) -> Path:
    attempted: list[str] = []
    for candidate in executable_candidates(explicit):
        attempted.append(candidate)
        expanded = Path(candidate).expanduser()
        if expanded.is_file():
            return expanded.resolve()
        found = shutil.which(candidate)
        if found:
            return Path(found).resolve()
    raise FileNotFoundError("No Godot executable found. Tried: " + ", ".join(attempted))


def build_command(args: argparse.Namespace, binary: Path, root: Path) -> list[str]:
    if args.mode == "version":
        return [str(binary), "--version"]

    command = [str(binary), "--headless", "--path", str(root)]
    if args.mode == "import":
        command.append("--import")
    elif args.mode == "startup":
        command.extend(["--quit-after", str(args.iterations)])
    elif args.mode == "scene":
        if not args.scene:
            raise ValueError("--scene is required when --mode=scene")
        if not args.scene.startswith("res://"):
            raise ValueError("--scene must be a res:// path")
        if ".." in args.scene.split("/"):
            raise ValueError("--scene must not contain path traversal")
        command.extend(["--scene", args.scene, "--quit-after", str(args.iterations)])
    else:
        raise ValueError(f"Unsupported mode: {args.mode}")
    return command


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--godot", help="Explicit Godot executable path.")
    parser.add_argument(
        "--mode",
        choices=("version", "import", "startup", "scene"),
        default="version",
        help="Verification mode (default: version).",
    )
    parser.add_argument("--scene", help="Scene path for --mode=scene, e.g. res://tests/smoke.tscn")
    parser.add_argument(
        "--iterations",
        type=int,
        default=2,
        help="Frames/iterations before startup or scene mode quits (default: 2).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=120.0,
        help="Maximum process runtime in seconds (default: 120).",
    )
    parser.add_argument(
        "--acknowledge-project-code",
        action="store_true",
        help="Acknowledge that the selected mode may execute project/editor/native code.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.iterations < 1:
        print("error: --iterations must be at least 1", file=sys.stderr)
        return 2
    if args.timeout <= 0:
        print("error: --timeout must be positive", file=sys.stderr)
        return 2
    if args.mode != "version" and not args.acknowledge_project_code:
        print(
            "error: this mode may execute project/editor/native code; review the repository "
            "and pass --acknowledge-project-code to proceed",
            file=sys.stderr,
        )
        return 2

    try:
        binary = resolve_executable(args.godot)
        root = find_project_root(args.root)
        command = build_command(args, binary, root)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print("command:", shlex.join(command))
    try:
        completed = subprocess.run(
            command,
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            errors="replace",
            timeout=args.timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        print(f"error: Godot exceeded the {args.timeout:g}s timeout", file=sys.stderr)
        if error.stdout:
            print("--- stdout ---")
            print(error.stdout)
        if error.stderr:
            print("--- stderr ---", file=sys.stderr)
            print(error.stderr, file=sys.stderr)
        return 124
    except OSError as error:
        print(f"error: failed to execute Godot: {error}", file=sys.stderr)
        return 1

    if completed.stdout:
        print("--- stdout ---")
        print(completed.stdout.rstrip())
    if completed.stderr:
        print("--- stderr ---", file=sys.stderr)
        print(completed.stderr.rstrip(), file=sys.stderr)
    print(f"exit-code: {completed.returncode}")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
