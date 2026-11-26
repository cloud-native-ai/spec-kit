"""Scoped tests for references/types/plantuml/scripts/runtime-evidence.py.

Fixtures are synthetic: a launcher-style launch JSON and a CLI-style stream JSONL
are created in tmp_path and passed explicitly. No private path is embedded.
"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "runtime-evidence.py"

LAUNCH = {
    "schema": "qoder-execution/2",
    "name": "unit-run",
    "actual_argv": [
        "qodercli",
        "--model", "ModelX",
        "--context-window", "123000",
        "--reasoning-effort", "max",
        "--permission-mode", "accept_edits",
        "--session-id", "sid-0001",
    ],
    "cwd": "/work/repo",
    "requested_session_id": "sid-0001",
    "profile": {
        "model": "ModelX",
        "context_window": 123000,
        "reasoning_effort": "max",
        "config_root": "/work/config",
    },
}

INIT = {
    "type": "system",
    "subtype": "init",
    "protocol_version": "1.5.0",
    "cwd": "/work/repo",
    "model": "ModelX",
    "permissionMode": "acceptEdits",
    "session_id": "sid-0001",
    "tools": ["Read", "Bash"],
    "skills": ["draw-diagram"],
}

LATER = {"type": "assistant", "model": "provider-alias", "session_id": "sid-0001"}


def write_evidence(tmp_path, launch=LAUNCH, init=INIT, stream_lines=None):
    launch_path = tmp_path / "launch.json"
    stream_path = tmp_path / "stream.jsonl"
    launch_path.write_text(json.dumps(launch), encoding="utf-8")
    if stream_lines is None:
        stream_lines = [init, LATER]
    stream_path.write_text(
        "\n".join(json.dumps(line) for line in stream_lines) + "\n", encoding="utf-8"
    )
    return launch_path, stream_path


def run_tool(tmp_path, launch_path, stream_path, output_name="report.json", extra=()):
    output_path = tmp_path / output_name
    args = [sys.executable, "-B", str(SCRIPT), "--output", str(output_path)]
    if launch_path is not None:
        args += ["--launch", str(launch_path)]
    if stream_path is not None:
        args += ["--stream", str(stream_path)]
    args += list(extra)
    proc = subprocess.run(args, capture_output=True, text=True)
    report = None
    if output_path.exists():
        try:
            report = json.loads(output_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            report = None
    return proc, report


def test_consistent_evidence_separates_requested_and_observed(tmp_path):
    launch_path, stream_path = write_evidence(tmp_path)
    proc, report = run_tool(tmp_path, launch_path, stream_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert report["status"] == "consistent"
    assert report["requested"]["model"] == "ModelX"
    assert report["requested"]["context_window"] == "123000"
    assert report["requested"]["config_root"] == "/work/config"
    assert report["runtime_observed"]["init_model"] == "ModelX"
    assert report["runtime_observed"]["init_session_id"] == "sid-0001"
    assert report["verdicts"]["model"] == "match"
    assert report["verdicts"]["session_id"] == "match"
    assert report["verdicts"]["permission_mode"] == "match"
    assert report["verdicts"]["context_window"] == "not_evaluated"
    assert report["verdicts"]["reasoning_effort"] == "not_evaluated"
    assert report["verdicts"]["config_root"] == "not_evaluated"
    assert "context_window" in report["not_evaluated"]
    assert report["runtime_observed"]["init_model"] != "provider-alias"


def test_model_mismatch_is_not_evaluated_and_flags_mismatch(tmp_path):
    init = {**INIT, "model": "OtherModel"}
    launch_path, stream_path = write_evidence(tmp_path, init=init)
    proc, report = run_tool(tmp_path, launch_path, stream_path)
    assert proc.returncode == 3
    assert report["status"] == "mismatch"
    assert "model" in report["mismatches"]
    assert report["verdicts"]["model"] == "mismatch"


def test_missing_stream_is_unavailable_not_guessed(tmp_path):
    launch_path, _ = write_evidence(tmp_path)
    missing = tmp_path / "does-not-exist.jsonl"
    proc, report = run_tool(tmp_path, launch_path, missing)
    assert proc.returncode == 3
    assert report["status"] == "not_evaluated"
    assert report["runtime_observed"] == {}
    assert report["evidence"]["stream"]["status"] == "unavailable"
    assert "not found" in report["evidence"]["stream"]["reason"]


def test_missing_launch_keeps_observed_side(tmp_path):
    _, stream_path = write_evidence(tmp_path)
    missing = tmp_path / "no-launch.json"
    proc, report = run_tool(tmp_path, missing, stream_path)
    assert proc.returncode == 3
    assert report["status"] == "not_evaluated"
    assert report["runtime_observed"]["init_model"] == "ModelX"
    assert report["requested"] == {}


def test_stream_without_init_is_unavailable(tmp_path):
    launch_path, stream_path = write_evidence(tmp_path, stream_lines=[LATER])
    proc, report = run_tool(tmp_path, launch_path, stream_path)
    assert proc.returncode == 3
    assert report["evidence"]["stream"]["status"] == "unavailable"
    assert "system/init" in report["evidence"]["stream"]["reason"]


def test_overwrite_refused(tmp_path):
    launch_path, stream_path = write_evidence(tmp_path)
    output_path = tmp_path / "report.json"
    output_path.write_text("keep me", encoding="utf-8")
    proc, _ = run_tool(tmp_path, launch_path, stream_path)
    assert proc.returncode == 2
    assert output_path.read_text(encoding="utf-8") == "keep me"


def test_unknown_flag_and_missing_evidence_args(tmp_path):
    launch_path, stream_path = write_evidence(tmp_path)
    proc, _ = run_tool(tmp_path, launch_path, stream_path, extra=["--bogus"])
    assert proc.returncode == 2
    proc = subprocess.run(
        [sys.executable, "-B", str(SCRIPT), "--output", str(tmp_path / "x.json")],
        capture_output=True, text=True,
    )
    assert proc.returncode == 2


def test_help_and_version_are_non_acting():
    for flag in ("--help", "--version"):
        proc = subprocess.run([sys.executable, "-B", str(SCRIPT), flag], capture_output=True, text=True)
        assert proc.returncode == 0
        assert proc.stdout.strip()
