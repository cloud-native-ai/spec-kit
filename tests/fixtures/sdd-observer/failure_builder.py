"""Failure fixtures for the observer lifecycle (Feature 096, wp03 T023).

Two fixtures compose ``line_builder.build_line`` under a caller-provided ``tmp_path``:

- ``build_start_failure(root)`` — the observer never starts. The state spine carries one
  ``state: failed`` observer record with a one-line reason and the dispatch attempt leaves an
  unsettled status envelope (no ``exit=``); no observer execution triplet ever exists.
- ``build_mid_run_kill(root)`` — execution A starts, is killed mid-run (a failed status envelope
  plus a ``state: failed`` spine record), the line advances through its remaining stub stages and
  execution B restarts from the same instance at the next stage boundary.

In both fixtures the simulated line reaches its terminal stage with the runner quartet intact
(``exit=0`` / ``sentinel=1``), and no stage verdict text mentions the observer: the failure is a
recorded non-observation, never a gate (SC-003, FR-009, FR-020).
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent
LINE_BUILDER_PATH = FIXTURES / "line_builder.py"

RECORD_HEADING = "## Observer Record — "


def _line_builder():
    spec = importlib.util.spec_from_file_location(
        "sdd_observer_failure_line_builder", LINE_BUILDER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _drop_observer_records(spine: Path) -> None:
    """Remove every observer record section, leaving the rest of the spine untouched."""
    text = spine.read_text(encoding="utf-8")
    cut = text.find("\n" + RECORD_HEADING)
    if cut != -1:
        spine.write_text(text[:cut] + "\n", encoding="utf-8")


def _write_status_envelope(state_dir: Path, line_id: str, text: str) -> Path:
    state_dir.mkdir(parents=True, exist_ok=True)
    path = state_dir / ("status-%s-observer" % line_id)
    path.write_text(text + "\n", encoding="utf-8")
    return path


def _write_triplet(triplet_dir: Path, label: str, state_text: str, log_line: str) -> None:
    triplet_dir.mkdir(parents=True, exist_ok=True)
    (triplet_dir / ("%s.live.log" % label)).write_text(log_line + "\n", encoding="utf-8")
    (triplet_dir / ("%s.jsonl" % label)).write_text('{"event": "observer"}\n', encoding="utf-8")
    (triplet_dir / ("%s.status" % label)).write_text(state_text + "\n", encoding="utf-8")


def read_observer_records(spine: Path):
    """The append-only observer record sections, in file order (latest wins is the reader's rule)."""
    records = []
    current = None
    for line in Path(spine).read_text(encoding="utf-8").splitlines():
        if line.startswith(RECORD_HEADING):
            if current is not None:
                records.append(current)
            current = {"heading": line[len(RECORD_HEADING):]}
            continue
        if current is not None and line.startswith("- "):
            key, _, value = line[2:].partition(":")
            current[key.strip()] = value.strip()
    if current is not None:
        records.append(current)
    return records


def build_start_failure(root, line_id=None, run_id=None, spec_key=None):
    """The observer cannot start: one failed spine record, no execution, line still terminal."""
    builder = _line_builder()
    line = builder.build_line(
        root,
        line_id=line_id or builder.LINE_ID,
        run_id=run_id or builder.RUN_ID,
        spec_key=spec_key or builder.SPEC_KEY,
    )
    reason = "observer start failed (fixture: dispatch refused)"
    _drop_observer_records(line["spine"])
    builder.append_observer_record(
        line["spine"], line["line_id"], line["run_id"], line["spec_key"],
        execution_label="-", started_at="-", state="failed", reason=reason,
    )
    for suffix in ("live.log", "jsonl", "status"):
        stale = line["triplet_dir"] / ("%s.%s" % (line["execution_label"], suffix))
        if stale.exists():
            stale.unlink()
    envelope = _write_status_envelope(
        line["state_dir"], line["line_id"],
        "state=failed reason=%s at=%d line=%s stage=- event=status"
        % (reason, line["start_epoch"] + 2, line["line_id"]),
    )
    result = dict(line)
    result.update({
        "kind": "start-failure",
        "reason": reason,
        "execution_label": None,
        "restart_label": None,
        "status_envelope": envelope,
        "observer_records": read_observer_records(line["spine"]),
        "terminal_stage": line["stages"][-1],
    })
    return result


def build_mid_run_kill(root, line_id=None, run_id=None, spec_key=None):
    """Execution A is killed mid-run; execution B restarts at the next stage boundary."""
    builder = _line_builder()
    line = builder.build_line(
        root,
        line_id=line_id or builder.LINE_ID,
        run_id=run_id or builder.RUN_ID,
        spec_key=spec_key or builder.SPEC_KEY,
    )
    start_epoch = line["start_epoch"]
    label_a = line["execution_label"]
    label_b = "%s--%s-b--observer" % (line["line_id"], line["run_id"])
    reason = "observer killed mid-run (fixture: status envelope left failed)"

    _write_triplet(line["triplet_dir"], label_a,
                   "state=failed\nreason=%s" % reason, "observer killed")
    envelope = _write_status_envelope(
        line["state_dir"], line["line_id"],
        "state=failed exit=137 reason=%s at=%d line=%s stage=- event=status"
        % (reason, start_epoch + 10, line["line_id"]),
    )
    builder.append_observer_record(
        line["spine"], line["line_id"], line["run_id"], line["spec_key"],
        execution_label=label_a, started_at=builder.utc(start_epoch + 10),
        state="failed", reason=reason,
    )
    _write_triplet(line["triplet_dir"], label_b, "state=running", "observer restart")
    builder.append_observer_record(
        line["spine"], line["line_id"], line["run_id"], line["spec_key"],
        execution_label=label_b, started_at=builder.utc(start_epoch + 20),
        state="started",
    )
    result = dict(line)
    result.update({
        "kind": "mid-run-kill",
        "reason": reason,
        "execution_label": label_a,
        "restart_label": label_b,
        "status_envelope": envelope,
        "observer_records": read_observer_records(line["spine"]),
        "terminal_stage": line["stages"][-1],
    })
    return result
