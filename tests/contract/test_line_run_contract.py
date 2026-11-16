"""Contract test: the `line-run.sh` surface (102, US1).

Pins ``.specify/specs/102-line-registry-registration/contracts/line-run.contract.md``
**C-01…C-05, C-13 (usage row), C-19**. Every case answers from the wrapper alone — no registry,
git or engine state is prepared, because the clauses under test are precisely the ones that
must hold *before* the wrapper touches any of them.

The design rule this file enforces: the answer to `-h` / `--help` / `--version` is an
observation, never an action. The registry snapshot around each answer is taken over an
isolated ``SPECIFY_LINE_REGISTRY_DIR``, so a stray read that created or rewrote an entry would
show up as a snapshot difference rather than as a silent pass.
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
WRAPPER = REPO_ROOT / "scripts" / "bash" / "line-run.sh"

#: A run id the engine's own ``RUN_ID_RE`` accepts (A-18); the wrapper never re-validates it.
RUN_ID = "r20261116T090000Z-a001"


def _env(registry: Path) -> dict:
    env = os.environ.copy()
    env["SPECIFY_LINE_REGISTRY_DIR"] = str(registry)
    env["SPECIFY_LINE_RUNTIME_DIR"] = str(registry / "runtime")
    return env


def _run(args, registry: Path, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(WRAPPER), *args],
        capture_output=True,
        text=True,
        env=_env(registry),
        cwd=str(cwd or REPO_ROOT),
        timeout=60,
    )


def _snapshot(root: Path):
    """Every path under ``root`` with its kind and content hash; ``None`` when absent."""
    if not root.exists():
        return None
    rows = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_dir():
            rows.append((rel, "dir", ""))
        elif path.is_file():
            rows.append((rel, "file", hashlib.sha256(path.read_bytes()).hexdigest()))
        else:
            rows.append((rel, "other", ""))
    return tuple(rows)


@pytest.mark.parametrize("flag", ["-h", "--help"])
def test_c01_c05_help_answers_zero_without_registry_side_effects(tmp_path, flag):
    registry = tmp_path / "registry"
    registry.mkdir()
    before = _snapshot(registry)

    proc = _run([flag], registry)

    assert proc.returncode == 0, proc.stderr
    assert "usage:" in proc.stdout
    assert "--line-id" in proc.stdout and "--run-id" in proc.stdout
    assert _snapshot(registry) == before, "an answering flag must not write the registry"


def test_c01_c05_version_answers_zero_without_registry_side_effects(tmp_path):
    registry = tmp_path / "registry"
    registry.mkdir()
    before = _snapshot(registry)

    proc = _run(["--version"], registry)

    assert proc.returncode == 0, proc.stderr
    assert re.fullmatch(r"line-run\.sh \S+\n", proc.stdout), proc.stdout
    assert _snapshot(registry) == before, "an answering flag must not write the registry"


def test_c04_undeclared_option_is_refused_and_the_command_never_runs(tmp_path):
    registry = tmp_path / "registry"
    sentinel = tmp_path / "ran"
    proc = _run(
        ["--line-id", "demo", "--run-id", RUN_ID, "--bogus", "--",
         "bash", "-c", f"touch {sentinel}"],
        registry,
    )

    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "unrecognized option" in proc.stderr
    assert not sentinel.exists(), "a usage error must not start the wrapped command"


def test_c02_opt_equals_value_form_is_refused(tmp_path):
    registry = tmp_path / "registry"
    sentinel = tmp_path / "ran"
    proc = _run(
        [f"--line-id=demo", f"--run-id={RUN_ID}", "--", "bash", "-c", f"touch {sentinel}"],
        registry,
    )

    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert not sentinel.exists(), "a usage error must not start the wrapped command"


def test_c04_missing_option_value_is_refused(tmp_path):
    registry = tmp_path / "registry"
    proc = _run(["--line-id", "demo", "--run-id"], registry)

    assert proc.returncode == 2, proc.stdout + proc.stderr


def test_c04_missing_bare_separator_is_refused(tmp_path):
    registry = tmp_path / "registry"
    sentinel = tmp_path / "ran"
    proc = _run(
        ["--line-id", "demo", "--run-id", RUN_ID, "bash", "-c", f"touch {sentinel}"],
        registry,
    )

    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert not sentinel.exists(), "a usage error must not start the wrapped command"


def test_c04_empty_command_is_refused(tmp_path):
    registry = tmp_path / "registry"
    proc = _run(["--line-id", "demo", "--run-id", RUN_ID, "--"], registry)

    assert proc.returncode == 2, proc.stdout + proc.stderr


def test_c03_a_flag_after_the_separator_belongs_to_the_wrapped_command(tmp_path):
    registry = tmp_path / "registry"
    proc = _run(
        ["--line-id", "demo-flag", "--run-id", RUN_ID, "--", "printf", "%s\n", "-h"],
        registry,
    )

    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == "-h\n", f"the wrapper must not answer the child's flag: {proc.stdout!r}"


def test_c19_the_wrapper_never_reaches_for_the_journal_writer():
    text = WRAPPER.read_text(encoding="utf-8")
    assert "journal-utils.py" not in text, (
        "registry writes go only through line-registry.py; the observer journal is a "
        "different store (FR-005 / C-19)"
    )
