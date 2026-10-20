"""Unit tests for skills/external/sdd-loop-driver/scripts/derive-live-log.py.

Red-first: the script does not exist yet. The derivation converts the raw
NDJSON event stream into an incrementally growing live log; only the terminal
``result`` text may end the log with the sentinel, and every derived line must
carry its raw event sequence and receive timestamp.
"""

import json
import re
import select
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "derive-live-log.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "sdd_loop_efficiency"
STUB = FIXTURES / "stub-cli.sh"

DERIVED = re.compile(r"\[evt=(\d+) at=([0-9]+(?:\.[0-9]+)?)\]")


def _last_nonempty(text):
    lines = [line for line in text.splitlines() if line.strip()]
    return lines[-1] if lines else ""


def _run(events, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--events", str(events), *args],
        capture_output=True, text=True,
    )


def test_non_terminal_sentinel_not_bare_last_line():
    completed = _run(FIXTURES / "stream" / "non_terminal_sentinel.jsonl")
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.strip(), "expected progress lines"
    assert _last_nonempty(completed.stdout) != "PLAN-DONE"
    assert "PLAN-DONE" in completed.stdout


def test_terminal_result_appended_verbatim():
    completed = _run(FIXTURES / "stream" / "result_sentinel.jsonl")
    assert completed.returncode == 0, completed.stderr
    assert _last_nonempty(completed.stdout) == "PLAN-DONE"
    assert "the stage finished its work" in completed.stdout
    assert "the final line is exact" in completed.stdout


def test_no_events_no_fabricated_progress(tmp_path):
    empty = tmp_path / "empty.jsonl"
    empty.write_text("", encoding="utf-8")
    completed = _run(empty)
    assert completed.returncode == 0
    assert completed.stdout.strip() == ""


def test_finish_recovers_terminal_result():
    completed = _run(FIXTURES / "stream" / "result_sentinel.jsonl", "--finish")
    assert completed.returncode == 0, completed.stderr
    assert _last_nonempty(completed.stdout) == "PLAN-DONE"


def test_malformed_or_missing_result_not_fake_done(tmp_path):
    completed = _run(FIXTURES / "stream" / "malformed.jsonl")
    assert completed.returncode == 0
    assert _last_nonempty(completed.stdout) != "PLAN-DONE"

    finished = _run(FIXTURES / "stream" / "malformed.jsonl", "--finish")
    assert finished.returncode == 1
    assert _last_nonempty(finished.stdout) != "PLAN-DONE"

    no_result = tmp_path / "no_result.jsonl"
    no_result.write_text(
        '{"type":"assistant","message":{"content":[{"type":"text","text":"x PLAN-DONE"}]}}\n',
        encoding="utf-8")
    streamed = _run(no_result)
    assert _last_nonempty(streamed.stdout) != "PLAN-DONE"


def test_pipe_incremental_output_before_exit():
    stub = subprocess.Popen(
        ["bash", str(STUB), "--output-format", "stream-json", "--delay", "1"],
        stdout=subprocess.PIPE, text=True,
    )
    deriver = subprocess.Popen(
        [sys.executable, str(SCRIPT)],
        stdin=stub.stdout, stdout=subprocess.PIPE, text=True,
    )
    assert stub.stdout is not None
    stub.stdout.close()
    line = ""
    try:
        ready, _, _ = select.select([deriver.stdout], [], [], 5.0)
        assert ready, "no incremental output before the process exited"
        line = deriver.stdout.readline()
    finally:
        deriver.wait(timeout=30)
        stub.wait(timeout=30)
    assert DERIVED.search(line), "first live line missing raw origin: %r" % line


def test_event_to_derived_line_latency_traceable():
    started = time.time()
    completed = _run(FIXTURES / "stream" / "non_terminal_sentinel.jsonl")
    assert completed.returncode == 0
    stamps = []
    seqs = []
    for line in completed.stdout.splitlines():
        match = DERIVED.search(line)
        if match:
            seqs.append(int(match.group(1)))
            stamps.append(float(match.group(2)))
    assert seqs == sorted(seqs) and len(set(seqs)) == len(seqs)
    for stamp in stamps:
        assert stamp >= started - 5
        assert started + 120 >= stamp, "derived line latency exceeds 120 seconds"


def test_derived_lines_all_have_raw_origin():
    events = [json.loads(line) for line in
              (FIXTURES / "stream" / "non_terminal_sentinel.jsonl").read_text(
                  encoding="utf-8").splitlines() if line.strip()]
    progress_events = [event for event in events if event.get("type") != "result"]
    completed = _run(FIXTURES / "stream" / "non_terminal_sentinel.jsonl")
    derived = [line for line in completed.stdout.splitlines() if DERIVED.search(line)]
    assert len(derived) == len(progress_events), (
        "fabricated or missing derived lines: %d derived vs %d raw"
        % (len(derived), len(progress_events)))
    seqs = {int(DERIVED.search(line).group(1)) for line in derived}
    assert seqs <= set(range(1, len(events) + 1))
