#!/usr/bin/env python3
"""runtime-evidence.py - consume caller-provided CLI execution evidence.

Reads ONLY the evidence files named on the command line and separates:
  * requested / argv-attested values: what the launcher asked the CLI to use
    (model, context window, reasoning effort, config root, session id);
  * runtime-observed values: what the CLI's own init event reports
    (init model, session id, cwd, permission mode, protocol version);
  * values with no observation channel: reported as "unavailable" and placed
    in not_evaluated - never guessed and never reconstructed from prose.

No credentials, configuration roots or other files are read.

Interface:
  runtime-evidence.py [--launch <launch.json>] [--stream <stream.jsonl>]
                      --output <new-report.json>
  At least one of --launch / --stream is required.

Exit codes:
  0  evidence is complete and consistent
  1  (reserved; consistency problems are reported as not_evaluated)
  2  usage or I/O error (including refusing to overwrite the output)
  3  report written, but evidence is missing/mismatched/incomplete
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

VERSION = "1.0.0"
ARG_FLAGS = {
    "--model": "model",
    "--context-window": "context_window",
    "--reasoning-effort": "reasoning_effort",
    "--permission-mode": "permission_mode",
    "--session-id": "session_id",
    "--output-format": "output_format",
    "--append-system-prompt": "append_system_prompt",
    "--settings": "settings",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_argv(argv):
    parsed = {}
    i = 0
    while i < len(argv):
        token = str(argv[i])
        key = ARG_FLAGS.get(token)
        if key:
            if i + 1 < len(argv) and not str(argv[i + 1]).startswith("--"):
                parsed[key] = argv[i + 1]
                i += 2
                continue
            parsed[key] = None
            i += 1
            continue
        i += 1
    return parsed


def load_launch(path: Path | None):
    if path is None:
        return {"status": "unavailable", "reason": "no --launch path provided"}, {}
    if not path.is_file():
        return {"status": "unavailable", "reason": "launch evidence file not found"}, {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return {"status": "unavailable", "reason": f"launch evidence unreadable: {exc}"}, {}
    argv = data.get("actual_argv") or []
    profile = data.get("profile") or {}
    parsed = parse_argv(argv)
    return {
        "status": "available",
        "path": str(path),
        "sha256": sha256_file(path),
        "requested": {
            "model": parsed.get("model", profile.get("model")),
            "context_window": parsed.get("context_window", profile.get("context_window")),
            "reasoning_effort": parsed.get("reasoning_effort", profile.get("reasoning_effort")),
            "permission_mode": parsed.get("permission_mode"),
            "config_root": profile.get("config_root"),
            "session_id": data.get("requested_session_id") or parsed.get("session_id"),
        },
        "argv_attested": parsed,
        "profile": {
            "model": profile.get("model"),
            "context_window": profile.get("context_window"),
            "reasoning_effort": profile.get("reasoning_effort"),
            "config_root": profile.get("config_root"),
        },
        "cwd": data.get("cwd"),
        "start_time": data.get("start_time"),
        "prompt_sha256": data.get("prompt_sha256"),
        "permissions_sha256": data.get("permissions_sha256"),
        "argv_has_model": "--model" in [str(a) for a in argv],
        "argv_has_context_window": "--context-window" in [str(a) for a in argv],
        "argv_has_reasoning_effort": "--reasoning-effort" in [str(a) for a in argv],
    }, data


def load_stream(path: Path | None):
    if path is None:
        return {"status": "unavailable", "reason": "no --stream path provided"}, {}
    if not path.is_file():
        return {"status": "unavailable", "reason": "stream evidence file not found"}, {}
    init = None
    model_values = []
    events = 0
    try:
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                events += 1
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event.get("type") == "system" and event.get("subtype") == "init" and init is None:
                    init = event
                elif isinstance(event.get("model"), str):
                    model_values.append(event["model"])
    except OSError as exc:
        return {"status": "unavailable", "reason": f"stream evidence unreadable: {exc}"}, {}
    if init is None:
        return {
            "status": "unavailable",
            "reason": "no system/init event in the stream",
            "path": str(path),
            "sha256": sha256_file(path),
            "events": events,
        }, {}
    return {
        "status": "available",
        "path": str(path),
        "sha256": sha256_file(path),
        "events": events,
        "runtime_observed": {
            "init_model": init.get("model"),
            "init_session_id": init.get("session_id") or init.get("sessionId"),
            "init_cwd": init.get("cwd"),
            "permission_mode": init.get("permissionMode"),
            "protocol_version": init.get("protocol_version"),
            "output_style": init.get("output_style"),
            "api_key_source": init.get("apiKeySource"),
            "tool_count": len(init.get("tools") or []),
            "skill_count": len(init.get("skills") or []),
        },
        "post_init_model_values": sorted(set(model_values)),
    }, {}


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="runtime-evidence.py",
        description="Consume caller-provided launch/stream evidence and report the CLI runtime "
                    "identity without guessing or reading configuration.",
        epilog="Exit codes: 0 consistent, 2 usage/IO error, 3 missing/mismatched/incomplete evidence.",
    )
    parser.add_argument("--launch", default=None, help="launcher-owned launch JSON")
    parser.add_argument("--stream", default=None, help="CLI stream JSONL containing the init event")
    parser.add_argument("--output", required=True, help="new report path; must not already exist")
    parser.add_argument("--version", action="version", version=f"runtime-evidence.py {VERSION}")
    args = parser.parse_args(argv)

    if not args.launch and not args.stream:
        print("error: at least one of --launch / --stream is required", file=sys.stderr)
        return 2
    output_path = Path(args.output)
    if output_path.exists():
        print(f"error: refusing to overwrite existing report: {output_path}", file=sys.stderr)
        return 2

    launch, launch_raw = load_launch(Path(args.launch) if args.launch else None)
    stream, _stream_raw = load_stream(Path(args.stream) if args.stream else None)

    requested = launch.get("requested") if launch.get("status") == "available" else {}
    observed = stream.get("runtime_observed") if stream.get("status") == "available" else {}

    def compare(requested_value, observed_value):
        if requested_value is None or observed_value is None:
            return "not_evaluated"
        return "match" if str(requested_value) == str(observed_value) else "mismatch"

    def normalize_mode(value):
        return "".join(ch for ch in str(value).lower() if ch.isalnum())

    if requested.get("permission_mode") is not None and observed.get("permission_mode") is not None:
        permission_mode = ("match" if normalize_mode(requested["permission_mode"])
                           == normalize_mode(observed["permission_mode"]) else "mismatch")
    else:
        permission_mode = "not_evaluated"

    verdicts = {
        "model": compare(requested.get("model"), observed.get("init_model")),
        "session_id": compare(requested.get("session_id"), observed.get("init_session_id")),
        "permission_mode": permission_mode,
        "cwd": compare(launch.get("cwd"), observed.get("init_cwd")),
        "context_window": "not_evaluated",
        "reasoning_effort": "not_evaluated",
        "config_root": "not_evaluated",
    }
    reasons = {
        "context_window": "argv-attested only; the init event exposes no runtime context-window value",
        "reasoning_effort": "argv-attested only; the init event exposes no runtime effort value",
        "config_root": "launcher profile only; no runtime observation channel without reading config",
    }
    not_evaluated = [key for key, value in verdicts.items() if value == "not_evaluated"]
    mismatch = [key for key, value in verdicts.items() if value == "mismatch"]
    if launch.get("status") != "available" or stream.get("status") != "available":
        status = "not_evaluated"
        reason = "evidence unavailable: " + "; ".join(
            item.get("reason", "") for item in (launch, stream) if item.get("status") != "available"
        )
        exit_code = 3
    elif mismatch:
        status = "mismatch"
        reason = "requested/argv-attested values disagree with runtime-observed init values"
        exit_code = 3
    elif any(value == "not_evaluated" for key, value in verdicts.items()
             if key in ("model", "session_id")):
        status = "not_evaluated"
        reason = "model/session observation missing; no comparable runtime value"
        exit_code = 3
    else:
        status = "consistent"
        reason = "requested/argv-attested model and session match the runtime init event"
        exit_code = 0

    report = {
        "schema": "plantuml-runtime-evidence/1",
        "tool": {"name": "runtime-evidence.py", "version": VERSION},
        "evidence": {"launch": launch, "stream": stream},
        "requested": requested,
        "runtime_observed": observed,
        "verdicts": verdicts,
        "verdict_reasons": reasons,
        "status": status,
        "reason": reason,
        "not_evaluated": not_evaluated,
        "mismatches": mismatch,
        "limits": [
            "Server-side model revision and effective context window are not independently proven by "
            "argv or the init event; they stay not_evaluated.",
            "post_init_model_values are informational only; a provider alias there is not treated as "
            "an identity mismatch.",
            "The execution record written after the CLI exits is intentionally not consumed here.",
        ],
    }
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "verdicts": verdicts, "report": str(output_path)}, ensure_ascii=False))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
