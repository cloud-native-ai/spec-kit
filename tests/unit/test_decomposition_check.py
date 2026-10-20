"""Unit tests for decomposition-check.py (large-feature decomposition gate)."""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "decomposition-check.py"


def _req(path, count):
    lines = ["# Requirements"]
    lines += ["- **FR-%03d**: fixture requirement" % i for i in range(1, count + 1)]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _tasks(path, count):
    lines = ["# Tasks"]
    lines += ["- [ ] T%03d fixture task" % i for i in range(1, count + 1)]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True)


def test_plan_at_ceiling_proceeds(tmp_path):
    req = _req(tmp_path / "requirements.md", 30)
    proc = _run("--mode", "plan", "--requirements", str(req))
    assert proc.returncode == 0, proc.stderr
    record = json.loads(proc.stdout)
    assert record["decision"] == "proceed"
    assert record["measured"] == {
        "fr_count": 30, "task_count": None,
        "fr_ceiling": 30, "task_ceiling": 40,
    }


def test_plan_above_ceiling_requires_split(tmp_path):
    req = _req(tmp_path / "requirements.md", 31)
    proc = _run("--mode", "plan", "--requirements", str(req))
    assert proc.returncode == 1, proc.stderr
    record = json.loads(proc.stdout)
    assert record["decision"] == "split-required"
    assert "ceiling 30" in record["reasons"][0]


def test_tasks_at_ceiling_proceeds(tmp_path):
    req = _req(tmp_path / "requirements.md", 30)
    tasks = _tasks(tmp_path / "tasks.md", 40)
    proc = _run("--mode", "tasks", "--requirements", str(req), "--tasks", str(tasks))
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout)["decision"] == "proceed"


def test_task_rows_above_ceiling_requires_split(tmp_path):
    req = _req(tmp_path / "requirements.md", 10)
    tasks = _tasks(tmp_path / "tasks.md", 41)
    proc = _run("--mode", "tasks", "--requirements", str(req), "--tasks", str(tasks))
    assert proc.returncode == 1, proc.stderr
    record = json.loads(proc.stdout)
    assert record["decision"] == "split-required"
    assert "task rows=41" in record["reasons"][0]


def test_wide_task_markers_count(tmp_path):
    req = _req(tmp_path / "requirements.md", 10)
    tasks = tmp_path / "tasks.md"
    lines = ["# Tasks"] + ["- [%s] T%03d row" % ("x" if i % 2 else ">", i)
                           for i in range(1, 42)]
    tasks.write_text("\n".join(lines) + "\n", encoding="utf-8")
    proc = _run("--mode", "tasks", "--requirements", str(req), "--tasks", str(tasks))
    assert proc.returncode == 1
    assert json.loads(proc.stdout)["measured"]["task_count"] == 41


def test_tasks_mode_requires_tasks_file(tmp_path):
    req = _req(tmp_path / "requirements.md", 10)
    proc = _run("--mode", "tasks", "--requirements", str(req))
    assert proc.returncode == 2
    assert "requires --tasks" in proc.stderr


def test_empty_requirements_is_input_error(tmp_path):
    req = tmp_path / "requirements.md"
    req.write_text("# Requirements\n\nno definitions\n", encoding="utf-8")
    proc = _run("--mode", "plan", "--requirements", str(req))
    assert proc.returncode == 2
    assert "no FR definitions" in proc.stderr


def test_missing_requirements_is_input_error(tmp_path):
    proc = _run("--mode", "plan", "--requirements", str(tmp_path / "absent.md"))
    assert proc.returncode == 2


def test_json_out_written(tmp_path):
    req = _req(tmp_path / "requirements.md", 31)
    out = tmp_path / "gate.json"
    proc = _run("--mode", "plan", "--requirements", str(req), "--json-out", str(out))
    assert proc.returncode == 1
    record = json.loads(out.read_text(encoding="utf-8"))
    assert record["decision"] == "split-required"
