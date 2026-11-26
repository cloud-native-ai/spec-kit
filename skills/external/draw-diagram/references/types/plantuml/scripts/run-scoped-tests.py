#!/usr/bin/env python3
"""run-scoped-tests.py - capture complete evidence for one scoped test run.

Runs the repository's canonical test entry (`scripts/bash/run-tests.sh`) with the
caller's explicit test paths, and writes one JSON evidence record containing the
exact command, environment additions, exit code, wall-clock duration, and the
complete stdout/stderr. It never invokes pytest directly, never deletes anything,
and refuses to overwrite an existing evidence file.

Interface:
  run-scoped-tests.py --test-paths <path> [<path> ...] --output <new.json>
                      [--label <text>] [--env KEY=VALUE ...]

Exit codes:
  0  the test run exited 0
  1  the test run exited non-zero (evidence still written)
  2  usage or I/O error (including refusing to overwrite the evidence file)
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import subprocess
import sys
import time
from pathlib import Path

VERSION = "1.0.0"


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for _ in range(15):
        if (current / "scripts" / "bash" / "run-tests.sh").is_file() and (current / ".git").exists():
            return current
        if current.parent == current:
            break
        current = current.parent
    raise SystemExit("error: cannot locate repository root containing scripts/bash/run-tests.sh")


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="run-scoped-tests.py",
        description="Run scripts/bash/run-tests.sh for explicit test paths and capture one "
                    "complete evidence record (command, stdout, stderr, exit code, duration).",
        epilog="Exit codes: 0 tests passed, 1 tests failed (evidence written), 2 usage/IO error.",
    )
    parser.add_argument("--test-paths", nargs="+", required=True,
                        help="test file or directory paths forwarded to the runner")
    parser.add_argument("--output", required=True, help="new evidence JSON path")
    parser.add_argument("--label", default=None, help="human-readable label for this run")
    parser.add_argument("--env", action="append", default=[], metavar="KEY=VALUE",
                        help="extra environment variable for the test process (repeatable)")
    parser.add_argument("--version", action="version", version=f"run-scoped-tests.py {VERSION}")
    args = parser.parse_args(argv)

    output_path = Path(args.output)
    if output_path.exists():
        print(f"error: refusing to overwrite existing evidence: {output_path}", file=sys.stderr)
        return 2
    repo = find_repo_root(Path(__file__))
    runner = repo / "scripts" / "bash" / "run-tests.sh"
    env = os.environ.copy()
    additions = {}
    for item in args.env:
        key, sep, value = item.partition("=")
        if not sep or not key:
            print(f"error: --env expects KEY=VALUE, got {item!r}", file=sys.stderr)
            return 2
        additions[key] = value
        env[key] = value
    command = ["bash", str(runner), *args.test_paths, "-q"]
    started = datetime.datetime.now(datetime.timezone.utc)
    clock = time.monotonic()
    proc = subprocess.run(command, cwd=str(repo), env=env, capture_output=True, text=True)
    duration = time.monotonic() - clock
    finished = datetime.datetime.now(datetime.timezone.utc)
    evidence = {
        "schema": "plantuml-scoped-test-evidence/1",
        "tool": {"name": "run-scoped-tests.py", "version": VERSION},
        "label": args.label,
        "cwd": str(repo),
        "command": command,
        "env_additions": additions,
        "started_at": started.isoformat(),
        "finished_at": finished.isoformat(),
        "duration_seconds": round(duration, 3),
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"exit_code": proc.returncode, "duration_seconds": round(duration, 3),
                      "evidence": str(output_path)}, ensure_ascii=False))
    return 0 if proc.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
