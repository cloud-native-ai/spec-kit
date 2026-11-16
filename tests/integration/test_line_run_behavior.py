"""Integration test: the `line-run.sh` lifecycle (102, US1).

Pins ``.specify/specs/102-line-registry-registration/contracts/line-run.contract.md``
**C-06…C-14, C-16, C-18** by observing the engine's own registry entries, the digest's rendered
reading and the wrapper's exit status — never by reading the wrapper's text.

Isolation: every case owns a ``SPECIFY_LINE_REGISTRY_DIR`` under ``tmp_path`` and runs the
wrapper with this repository as cwd, so the identity is the real git toplevel while the
registry is disposable. The digest case reads the same isolated registry, which is what makes
`active` visible at run time and `nothing-running` the correct reading after the only line
closes.
"""
from __future__ import annotations

import json
import os
import shlex
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[2]
WRAPPER = REPO_ROOT / "scripts" / "bash" / "line-run.sh"
DIGEST = REPO_ROOT / "scripts" / "python" / "status-digest.py"

RUN_ID_OK = "r20261116T090000Z-a001"
RUN_ID_FAIL = "r20261116T090000Z-a002"


def _registry(tmp_path: Path) -> Path:
    registry = tmp_path / "registry"
    (registry / "runtime").mkdir(parents=True, exist_ok=True)
    return registry


def _env(registry: Path) -> dict:
    env = os.environ.copy()
    env["SPECIFY_LINE_REGISTRY_DIR"] = str(registry)
    env["SPECIFY_LINE_RUNTIME_DIR"] = str(registry / "runtime")
    return env


def _run(args, registry: Path, cwd: Path | None = None, timeout: int = 60):
    return subprocess.run(
        ["bash", str(WRAPPER), *args],
        capture_output=True,
        text=True,
        env=_env(registry),
        cwd=str(cwd or REPO_ROOT),
        timeout=timeout,
    )


def _entry(registry: Path, line_id: str) -> dict:
    path = registry / f"{line_id}.json"
    assert path.is_file(), f"registry entry missing: {path}"
    return json.loads(path.read_text(encoding="utf-8"))


def _digest(registry: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(DIGEST), "--action", "digest", "--workspace", str(REPO_ROOT)],
        capture_output=True,
        text=True,
        env=_env(registry),
        cwd=str(REPO_ROOT),
        timeout=60,
    )


def _wait_for_entry(registry: Path, line_id: str, state: str, timeout: float = 20.0) -> dict:
    path = registry / f"{line_id}.json"
    deadline = time.time() + timeout
    seen: dict = {}
    while time.time() < deadline:
        if path.is_file():
            try:
                seen = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                seen = {}
            if seen.get("state") == state:
                return seen
        time.sleep(0.1)
    raise AssertionError(
        f"entry {line_id} never reached state={state}; last read={seen}; "
        f"registry={sorted(p.name for p in registry.iterdir())}"
    )


# --------------------------------------------------------------------------- success path
def test_success_registers_active_runs_the_command_and_closes_completed(tmp_path):
    registry = _registry(tmp_path)
    composed = f"demo-batch-{RUN_ID_OK}"

    proc = _run(["--line-id", "demo-batch", "--run-id", RUN_ID_OK, "--", "true"], registry)

    assert proc.returncode == 0, proc.stderr
    entry = _entry(registry, composed)
    assert entry["line_id"] == composed
    assert entry["run_id"] == RUN_ID_OK
    assert entry["state"] == "closed"
    assert entry["last_event"] == "completed"
    assert entry["run_history"][-1]["outcome"] == "completed"


# --------------------------------------------------------------------------- failure path
def test_failed_command_propagates_its_status_and_closes_failed(tmp_path):
    registry = _registry(tmp_path)
    composed = f"demo-fail-{RUN_ID_FAIL}"

    proc = _run(
        ["--line-id", "demo-fail", "--run-id", RUN_ID_FAIL, "--", "bash", "-c", "exit 7"],
        registry,
    )

    assert proc.returncode == 7, proc.stdout + proc.stderr
    entry = _entry(registry, composed)
    assert entry["state"] == "closed"
    assert entry["last_event"] == "failed"
    assert entry["run_history"][-1]["outcome"] == "failed"


# ------------------------------------------------------- visible at run time, gone afterwards
def test_digest_lists_the_line_while_running_and_renders_nothing_running_after(tmp_path):
    registry = _registry(tmp_path)
    composed = f"demo-live-{RUN_ID_OK}"

    proc = subprocess.Popen(
        ["bash", str(WRAPPER), "--line-id", "demo-live", "--run-id", RUN_ID_OK, "--",
         "bash", "-c", "sleep 3"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=_env(registry),
        cwd=str(REPO_ROOT),
    )
    try:
        entry = _wait_for_entry(registry, composed, "active")
        assert entry["last_event"] == "registered"

        during = _digest(registry)
        assert during.returncode == 0, during.stdout + during.stderr
        assert composed in during.stdout, during.stdout
        assert "nothing-running" not in during.stdout, during.stdout
    finally:
        proc.communicate(timeout=60)

    assert proc.returncode == 0
    assert _entry(registry, composed)["state"] == "closed"

    after = _digest(registry)
    assert after.returncode == 3, after.stdout + after.stderr
    assert "nothing-running" in after.stdout, after.stdout


# ------------------------------------------------------------- registration failure: no run
def test_registration_failure_never_starts_the_command(tmp_path):
    registry = tmp_path / "registry"
    registry.mkdir()
    sentinel = tmp_path / "ran"

    registry.chmod(0o500)
    try:
        proc = _run(
            ["--line-id", "demo-denied", "--run-id", RUN_ID_OK, "--",
             "bash", "-c", f"touch {sentinel}"],
            registry,
        )
    finally:
        registry.chmod(0o700)

    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "register" in proc.stderr, proc.stderr
    assert not sentinel.exists(), "a refused registration must not start the wrapped command"
    assert not (registry / f"demo-denied-{RUN_ID_OK}.json").exists()


# ------------------------------------------------------------------------ no git identity: 4
def test_no_git_toplevel_exits_four_and_never_starts_the_command(tmp_path):
    registry = _registry(tmp_path)
    nongit = tmp_path / "nongit"
    nongit.mkdir()
    sentinel = tmp_path / "ran"

    proc = _run(
        ["--line-id", "demo-nogit", "--run-id", RUN_ID_OK, "--", "bash", "-c", f"touch {sentinel}"],
        registry,
        cwd=nongit,
    )

    assert proc.returncode == 4, proc.stdout + proc.stderr
    assert not sentinel.exists(), "an unresolved identity must not start the wrapped command"


# ------------------------------------------------------------------------------- A-24 double
def test_double_failure_keeps_the_command_status_and_surfaces_the_close_failure(tmp_path):
    registry = _registry(tmp_path)
    composed = f"demo-double-{RUN_ID_OK}"
    quoted = shlex.quote(str(registry))

    try:
        proc = _run(
            ["--line-id", "demo-double", "--run-id", RUN_ID_OK, "--",
             "bash", "-c", f"chmod 500 {quoted}; exit 5"],
            registry,
        )
    finally:
        registry.chmod(0o700)

    assert proc.returncode == 5, proc.stdout + proc.stderr
    assert "close failed" in proc.stderr, proc.stderr
    assert "engine exit 6" in proc.stderr, "the close failure must stay readable on stderr"
    assert _entry(registry, composed)["state"] == "active"


def test_close_failure_over_a_successful_command_exits_with_the_engine_status(tmp_path):
    registry = _registry(tmp_path)
    quoted = shlex.quote(str(registry))

    try:
        proc = _run(
            ["--line-id", "demo-closedeny", "--run-id", RUN_ID_OK, "--",
             "bash", "-c", f"chmod 500 {quoted}"],
            registry,
        )
    finally:
        registry.chmod(0o700)

    # A-24: with the child at 0, the engine's own status (6 = registry I/O) becomes ours.
    assert proc.returncode == 6, proc.stdout + proc.stderr
    assert "close failed" in proc.stderr, proc.stderr


# ------------------------------------------------------------------------- SIGKILL: residue
def test_a_killed_wrapper_leaves_the_entry_active_and_visible(tmp_path):
    registry = _registry(tmp_path)
    composed = f"demo-kill-{RUN_ID_OK}"

    proc = subprocess.Popen(
        ["bash", str(WRAPPER), "--line-id", "demo-kill", "--run-id", RUN_ID_OK, "--",
         "bash", "-c", "sleep 60"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=_env(registry),
        cwd=str(REPO_ROOT),
        start_new_session=True,
    )
    try:
        _wait_for_entry(registry, composed, "active")
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        proc.wait(timeout=20)
    finally:
        if proc.poll() is None:  # pragma: no cover - defensive teardown
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            proc.wait(timeout=20)

    entry = _entry(registry, composed)
    assert entry["state"] == "active", "a killed wrapper must not fabricate a close"
    assert entry["last_event"] == "registered"

    reading = _digest(registry)
    assert reading.returncode == 0, reading.stdout + reading.stderr
    assert composed in reading.stdout, reading.stdout
