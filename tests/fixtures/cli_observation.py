#!/usr/bin/env python3
"""Executable CLI-profile observation fixture (SC-006 / FR-038/FR-039).

One invocation consumes exactly one observation event and applies the write
order owned by `references/cli/index.md`:

    cli_observations (state spine) -> provenance row -> feedback entry

An event that matches the profile's current value produces a spine record and
**zero** feedback entries.  An event that changes the profile produces the
spine record, one provenance row, and exactly one retrievable
`cli-profile:<cli>` feedback entry.

Usage:
  cli_observation.py --workspace W --profile FILE --event JSON \
      [--cli qodercli] [--run-id r20261020T120000Z-a1b2] \
      [--spine FILE] [--feedback-engine FILE]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FEEDBACK_ENGINE = REPO_ROOT / ".specify" / "scripts" / "python" / "feedback-utils.py"


def parse_row(profile_text: str, dimension: str):
    lines = profile_text.splitlines()
    for index, line in enumerate(lines):
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and cells[0] == dimension:
            return lines, index, cells
    raise SystemExit(f"dimension not found in profile: {dimension}")


def replace_value(cells: list[str], value: str) -> str:
    cells = list(cells)
    cells[2] = value.replace("|", "/")
    return "| " + " | ".join(cells) + " |"


def append_provenance(profile_text: str, row: str) -> str:
    lines = profile_text.splitlines()
    start = next(
        (i for i, line in enumerate(lines) if line.strip() == "## Provenance"), None
    )
    if start is None:
        raise SystemExit("profile has no ## Provenance section")
    end = start + 1
    last_table_line = None
    while end < len(lines) and not lines[end].startswith("## "):
        if lines[end].strip().startswith("|"):
            last_table_line = end
        end += 1
    insert_at = (last_table_line + 1) if last_table_line is not None else end
    lines.insert(insert_at, row)
    return "\n".join(lines) + "\n"


def record_feedback(engine: Path, workspace: Path, cli: str, run_id: str, event: dict) -> tuple[int, str]:
    review = f"cli-profile:{cli} {event['dimension']} changed: {event['observation']}"
    points = f"cli-profile:{cli} {event['dimension']}"
    proc = subprocess.run(
        [sys.executable, str(engine), "--action", "record",
         "--workspace-root", str(workspace),
         "--unit-id", "skill:sdd-loop-driver", "--unit-type", "skill",
         "--run-id", run_id, "--review", review, "--points", points],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise SystemExit(f"feedback record failed: {proc.stdout} {proc.stderr}")
    payload = json.loads(proc.stdout)
    return 1, payload.get("id", "")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="cli_observation.py")
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--event", required=True, help="JSON object or @path")
    parser.add_argument("--cli", default="qodercli")
    parser.add_argument("--run-id", default="r20261020T120000Z-a1b2")
    parser.add_argument("--spine")
    parser.add_argument("--feedback-engine", default=str(DEFAULT_FEEDBACK_ENGINE))
    args = parser.parse_args(argv)

    workspace = Path(args.workspace).expanduser().resolve()
    profile_path = Path(args.profile).expanduser().resolve()
    raw = args.event
    if raw.startswith("@"):
        raw = Path(raw[1:]).read_text(encoding="utf-8")
    event = json.loads(raw)
    for required in ("dimension", "observed_value", "observation", "trigger", "cli_version", "evidence"):
        if not event.get(required):
            raise SystemExit(f"event missing field: {required}")

    spine = Path(args.spine) if args.spine else (
        workspace / ".specify" / "memory" / "exec-quant" / "cli-observations.jsonl"
    )
    spine.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "event": "cli-observation",
        "cli": args.cli,
        "run_id": args.run_id,
        "at": int(time.time()),
        **event,
    }
    with spine.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")

    profile_text = profile_path.read_text(encoding="utf-8")
    lines, index, cells = parse_row(profile_text, event["dimension"])
    current = cells[2] if len(cells) > 2 else ""
    changed = event["observed_value"] != current
    feedback_count = 0
    feedback_id = ""
    provenance_appended = False
    if changed:
        lines[index] = replace_value(cells, event["observed_value"])
        updated = "\n".join(lines) + "\n"
        feedback_count, feedback_id = record_feedback(
            Path(args.feedback_engine), workspace, args.cli, args.run_id, event
        )
        provenance_row = (
            f"| {time.strftime('%Y-%m-%d')} | {event['trigger']} | {event['observation']} "
            f"| {event['dimension']}: {current[:60]} -> {event['observed_value'][:60]} "
            f"(cli {event['cli_version']}; {event['evidence']}) | {feedback_id} |"
        )
        updated = append_provenance(updated, provenance_row)
        profile_path.write_text(updated, encoding="utf-8")
        provenance_appended = True

    print(json.dumps({
        "changed": changed,
        "feedback_count": feedback_count,
        "feedback_id": feedback_id,
        "provenance_appended": provenance_appended,
        "spine": str(spine),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
