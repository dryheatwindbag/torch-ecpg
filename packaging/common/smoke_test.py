"""Smoke test a bundled tecpg launcher.

This script is intended to run against an unpacked distribution artifact, not
the source checkout. Pass the packaged launcher path explicitly.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


HELP_COMMANDS = (
    ("--help",),
    ("data", "--help"),
    ("run", "mlr", "--help"),
)


def run_help_command(launcher: Path, args: tuple[str, ...]) -> None:
    command = [str(launcher), *args]
    result = subprocess.run(
        command,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        sys.stderr.write(f"Command failed: {' '.join(command)}\n")
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise SystemExit(result.returncode)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run tecpg bundled launcher smoke tests."
    )
    parser.add_argument(
        "launcher",
        type=Path,
        help="Path to the packaged tecpg launcher.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    launcher = args.launcher
    if not launcher.exists():
        raise SystemExit(f"Launcher does not exist: {launcher}")

    for help_args in HELP_COMMANDS:
        run_help_command(launcher, help_args)


if __name__ == "__main__":
    main()
