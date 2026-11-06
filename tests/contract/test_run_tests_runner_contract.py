"""Contract cases for the canonical runner's execution model (086, C-001…C-016).

Owner of the propositions: `.specify/specs/086-efficient-test-execution/contracts/
runner-contract-086.contract.md`. This module is the WP-A1 red-first slice: it carries the
default-mode, worker-resolution, escape-hatch, two-pass and output clauses. The serial-marker
cases (C-010/C-011) live in WP-A4's slice of the same file.

Construction constraints (contract § F):

- Cases that must not depend on this host's CPU count pass ``--workers 2`` explicitly.
- The "no xdist" case stubs the engine instead of uninstalling it: a temporary ``PYTHONPATH``
  shim directory shadows ``xdist.py`` with a module whose import raises ``ImportError``, so
  ``<interpreter> -c 'import xdist'`` fails while every other module resolves normally.
- No case asserts a wall-clock threshold.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "scripts" / "bash" / "run-tests.sh"
MIRROR = ROOT / ".specify" / "scripts" / "bash" / "run-tests.sh"

MARK_CONTRACT = pytest.mark.contract

MODE_LINE = re.compile(r"^# test runner: mode=(?P<mode>\w+)(?P<rest>.*)$", re.M)
LIST_LINE = re.compile(
    r"^# failed-name list written: (?P<path>.+?) \((?P<n>\d+) entries\) passes=(?P<k>\d+)$", re.M
)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _python() -> str:
    """The interpreter the runner will resolve: keep the test independent of CWD."""
    return os.environ.get("SPECKIT_PYTHON") or sys.executable


def _write_suite(root: Path, failing: int = 0, serial_failing: int = 0) -> Path:
    """A throwaway suite: ``failing`` plain failures plus a ``serial``-marked block."""
    suite = root / "suite"
    suite.mkdir(parents=True, exist_ok=True)
    lines = []
    for i in range(3):
        lines.append(f"def test_pass_{i}():\n    assert True\n")
    for i in range(failing):
        lines.append(f"def test_fail_{i}():\n    assert False\n")
    if serial_failing:
        lines.append(
            "import pytest\n\n"
            "@pytest.mark.serial\n"
            f"def test_serial_fail():\n    assert False\n"
        )
    (suite / "test_sample.py").write_text("\n".join(lines), encoding="utf-8")
    # keep the marker registered so a run on this fixture tree never emits an
    # unknown-mark warning (pyproject.toml registers it for the real tree)
    (root / "pytest.ini").write_text("[pytest]\nmarkers =\n    serial: x\n", encoding="utf-8")
    return suite


def _run(args, *, cwd=None, env_extra=None):
    """Invoke the runner from a *clean* environment.

    Every case here asserts a mode the runner must DECIDE, so the ambient
    ``PYTEST_XDIST_WORKER`` that pytest's own entry scripts export is dropped: inheriting it
    would make every case observe the (correct) nested auto-serial branch instead of the
    branch under test, and would present as a red case that blames the runner.
    """
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("PYTEST_XDIST_WORKER", None)
    env["SPECKIT_PYTHON"] = _python()
    if env_extra is not None:
        env.update(env_extra)
    return subprocess.run(
        ["bash", str(RUNNER), *[str(a) for a in args]],
        capture_output=True,
        text=True,
        cwd=str(cwd or ROOT),
        env=env,
    )


def _mode(stderr: str):
    """Return ``(mode, rest)`` from the mode line, or fail with the real stderr."""
    match = MODE_LINE.search(stderr)
    assert match is not None, f"no mode line on stderr:\n{stderr}"
    return match.group("mode"), match.group("rest").strip()


def _list_line(stderr: str):
    match = LIST_LINE.search(stderr)
    assert match is not None, f"no failed-name list line on stderr:\n{stderr}"
    return match


def _names(path: Path):
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def is_worker_switch(token: str) -> bool:
    """True for every spelling of a worker-count switch (``-n N``, ``-nN``, ``-n=N``,
    ``--numprocesses``, ``--numprocesses=N``). ``N`` itself is a separate token in the
    separated form and is not counted here."""
    if token in ("-n", "--numprocesses"):
        return True
    return bool(re.fullmatch(r"(?:-n=?|--numprocesses=).+", token))


def _command_lines(stderr: str):
    return [ln for ln in stderr.splitlines() if ln.startswith("# test runner: ") and "mode=" not in ln]


# --------------------------------------------------------------------------- #
# C-001 / C-002 / C-003 — default parallel, mode line, truthful header
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_c001_default_run_is_parallel_without_a_parallel_argument(tmp_path):
    suite = _write_suite(tmp_path)
    done = _run(["--workers", "2", str(suite), "-q"], cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr
    mode, _ = _mode(done.stderr)
    assert mode == "parallel", done.stderr
    header = _command_lines(done.stderr)
    assert len(header) == 1, done.stderr
    assert "-n 2" in header[0], header[0]
    assert "--dist load" in header[0], header[0]


@MARK_CONTRACT
def test_c002_and_c003_mode_line_and_truthful_header(tmp_path):
    suite = _write_suite(tmp_path)
    done = _run(["--serial", "--workers", "2", str(suite), "-q"], cwd=tmp_path)
    mode, rest = _mode(done.stderr)
    assert mode == "serial", done.stderr
    assert "reason=explicit" in rest, rest
    header = _command_lines(done.stderr)
    assert len(header) == 1, done.stderr
    # C-003: the header describes what ran — a resolved-but-unapplied worker count
    # must not appear, and the serial pass carries -n0.
    assert "--workers" not in header[0], header[0]
    assert "-n 2" not in header[0], header[0]
    assert "-n0" in header[0], header[0]


# --------------------------------------------------------------------------- #
# C-004 — explicit serial is a complete run
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_c004_explicit_serial_runs_the_full_selection(tmp_path):
    suite = _write_suite(tmp_path, failing=1)
    names = tmp_path / "names.txt"
    done = _run(["--serial", "--names-out", names, str(suite), "-q"], cwd=tmp_path)
    assert done.returncode == 1, done.stdout + done.stderr
    assert _names(names) == ["suite/test_sample.py::test_fail_0"]
    mode, rest = _mode(done.stderr)
    assert mode == "serial" and "reason=explicit" in rest
    # a serial run is never labelled degraded / partial / unsupported
    lowered = done.stderr.lower()
    for word in ("degrad", "partial", "unsupported"):
        assert word not in lowered, done.stderr
    assert "mode=serial" in done.stderr


# --------------------------------------------------------------------------- #
# C-005 — nested run auto-serialises and starts no second pool
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_c005_nested_run_is_serial_and_derives_no_second_pool(tmp_path):
    suite = _write_suite(tmp_path)
    done = _run(
        ["--workers", "2", str(suite), "-q"],
        cwd=tmp_path,
        env_extra={"PYTEST_XDIST_WORKER": "gw3"},
    )
    assert done.returncode == 0, done.stdout + done.stderr
    mode, rest = _mode(done.stderr)
    assert mode == "serial", done.stderr
    assert "reason=nested" in rest, rest
    header = _command_lines(done.stderr)
    assert len(header) == 1, done.stderr
    assert "-n0" in header[0], header[0]
    assert "-n 2" not in header[0], header[0]
    assert "--dist" not in header[0], header[0]


# --------------------------------------------------------------------------- #
# C-006 — engine missing: serial, complete, pytest's exit code kept
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_c006_missing_xdist_falls_back_to_a_complete_serial_run(tmp_path):
    """Mechanism (recorded here per contract § F, so the premise is re-probeable): a temporary
    ``PYTHONPATH`` shim reproduces "this interpreter has no parallel engine" without
    uninstalling anything.

    The shim has three parts, and all three are load-bearing:

    1. ``xdist.py`` — a *module*, not a package — wins the search for ``xdist`` and raises
       ``ImportError``. That is exactly what the runner's own probe
       (``<interpreter> -c 'import xdist'``) sees on a Python-3.8 downstream.
    2. ``xdist_dist/`` — the real engine, relocated and with its internal
       ``from xdist.…`` imports rewritten to the alias, so the plugin still works.
    3. ``pytest_xdist-0.0.0.dist-info`` — registers itself as the ``pytest11`` distribution
       named ``pytest-xdist`` whose entry points load the alias, so pytest's plugin manager
       never tries to import the shadowed name. Without part 3 pytest imports the shadow
       eagerly and aborts the whole session with exit 3, which is a broken environment rather
       than an absent engine.

    Re-probe with the shim on ``PYTHONPATH``: ``-c 'import xdist'`` fails,
    ``python -m pytest -q <a passing test>`` exits 0, and ``python -m pytest -n 2 …`` fails.
    """
    shim = _build_no_xdist_shim(tmp_path)
    shim_env = {**os.environ, "PYTHONPATH": str(shim)}
    shim_env.pop("PYTEST_XDIST_WORKER", None)
    probe = subprocess.run(
        [_python(), "-c", "import xdist"], capture_output=True, text=True, env=shim_env
    )
    assert probe.returncode != 0, "the shim did not hide the engine; the premise is broken"

    suite = _write_suite(tmp_path, failing=1)
    names = tmp_path / "names.txt"
    done = _run(["--workers", "2", "--names-out", names, str(suite), "-q"],
                cwd=tmp_path, env_extra={"PYTHONPATH": str(shim)})
    # no error exit, no empty run, pytest's own exit code
    assert done.returncode == 1, done.stdout + done.stderr
    mode, rest = _mode(done.stderr)
    assert mode == "serial", done.stderr
    assert "reason=no-xdist" in rest, rest
    assert "xdist" in rest, f"the fallback note must name what is missing: {rest}"
    assert _names(names) == ["suite/test_sample.py::test_fail_0"]


def _build_no_xdist_shim(tmp_path: Path) -> Path:
    """Build the three-part shim documented in the C-006 case above."""
    import importlib.util
    import shutil

    shim = tmp_path / "shim"
    shim.mkdir()
    (shim / "xdist.py").write_text(
        'raise ImportError("xdist is shadowed by the 086 no-xdist contract case")\n',
        encoding="utf-8",
    )
    spec = importlib.util.find_spec("xdist")
    if spec is None or not spec.origin:
        pytest.skip("the host interpreter has no xdist to relocate; the case would prove nothing")
    real = Path(spec.origin).resolve().parent
    alias = shim / "xdist_dist"
    shutil.copytree(real, alias, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for source in alias.rglob("*.py"):
        text = source.read_text(encoding="utf-8")
        rewritten = (
            text.replace("from xdist.", "from xdist_dist.")
            .replace("from xdist import", "from xdist_dist import")
            .replace("import xdist.", "import xdist_dist.")
        )
        if rewritten != text:
            source.write_text(rewritten, encoding="utf-8")
    dist_info = shim / "pytest_xdist-0.0.0.dist-info"
    dist_info.mkdir()
    (dist_info / "METADATA").write_text(
        "Metadata-Version: 2.1\nName: pytest-xdist\nVersion: 0.0.0\n", encoding="utf-8"
    )
    (dist_info / "entry_points.txt").write_text(
        "[pytest11]\nxdist = xdist_dist.plugin\nxdist.looponfail = xdist_dist.looponfail\n",
        encoding="utf-8",
    )
    return shim


# --------------------------------------------------------------------------- #
# C-007 — flag > env > auto
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_c007_workers_flag_beats_the_environment_variable(tmp_path):
    suite = _write_suite(tmp_path)
    done = _run(
        ["--workers", "2", str(suite), "-q"],
        cwd=tmp_path,
        env_extra={"SPECKIT_TEST_WORKERS": "3"},
    )
    assert done.returncode == 0, done.stdout + done.stderr
    header = _command_lines(done.stderr)
    assert len(header) == 1, done.stderr
    assert "-n 2" in header[0], header[0]
    assert "-n 3" not in header[0], header[0]


@MARK_CONTRACT
def test_c007_environment_variable_beats_the_auto_default(tmp_path):
    suite = _write_suite(tmp_path)
    done = _run([str(suite), "-q"], cwd=tmp_path, env_extra={"SPECKIT_TEST_WORKERS": "3"})
    assert done.returncode == 0, done.stdout + done.stderr
    header = _command_lines(done.stderr)
    assert len(header) == 1, done.stderr
    assert "-n 3" in header[0], header[0]
    assert "-n auto" not in header[0], header[0]


# --------------------------------------------------------------------------- #
# C-008 — malformed worker value is a named error, never a silent fallback
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
@pytest.mark.parametrize("bad", ["abc", "0", "-2"])
def test_c008_malformed_worker_value_exits_non_zero_with_a_named_error(tmp_path, bad):
    suite = _write_suite(tmp_path)
    done = _run(["--workers", bad, str(suite), "-q"], cwd=tmp_path)
    assert done.returncode != 0, done.stdout + done.stderr
    assert "workers" in done.stderr.lower(), done.stderr
    assert bad in done.stderr, done.stderr
    # nothing ran: a silent fallback to one worker would have produced a pytest summary
    assert "passed" not in done.stdout, done.stdout


@MARK_CONTRACT
def test_c008_malformed_environment_value_is_also_a_named_error(tmp_path):
    suite = _write_suite(tmp_path)
    done = _run([str(suite), "-q"], cwd=tmp_path, env_extra={"SPECKIT_TEST_WORKERS": "abc"})
    assert done.returncode != 0, done.stdout + done.stderr
    assert "SPECKIT_TEST_WORKERS" in done.stderr, done.stderr


# --------------------------------------------------------------------------- #
# C-009 — the caller's own worker switch is never duplicated
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
@pytest.mark.parametrize(
    "caller_args, expected_token",
    [
        (["-n", "4"], "-n"),
        (["-n4"], "-n4"),
        (["--numprocesses", "4"], "--numprocesses"),
        (["--numprocesses=4"], "--numprocesses=4"),
    ],
)
def test_c009_caller_worker_switch_is_not_duplicated(tmp_path, caller_args, expected_token):
    suite = _write_suite(tmp_path)
    done = _run([*caller_args, "--workers", "2", str(suite), "-q"], cwd=tmp_path)
    header = _command_lines(done.stderr)
    assert len(header) == 1, done.stderr
    line = header[0]
    assert expected_token in line.split(), line
    # exactly one worker-count switch in total: the caller's own
    occurrences = [t for t in line.split() if is_worker_switch(t)]
    assert len(occurrences) == 1, line
    assert "--dist" not in line, line


@MARK_CONTRACT
def test_c009_caller_switch_suppresses_an_appended_dist(tmp_path):
    suite = _write_suite(tmp_path)
    done = _run(["-n", "2", str(suite), "-q"], cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr
    header = _command_lines(done.stderr)
    assert len(header) == 1, done.stderr
    assert "--dist" not in header[0], header[0]
    assert header[0].count("-n 2") == 1, header[0]


# --------------------------------------------------------------------------- #
# C-013 / C-014 / C-015 — combined list, entry + pass count, combined exit code
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_c013_names_out_is_one_sorted_deduplicated_list(tmp_path):
    suite = _write_suite(tmp_path, failing=2)
    names = tmp_path / "names.txt"
    done = _run(["--serial", "--names-out", names, str(suite), "-q"], cwd=tmp_path)
    assert done.returncode == 1, done.stdout + done.stderr
    listed = _names(names)
    assert listed == sorted(set(listed)), listed
    assert listed == [
        "suite/test_sample.py::test_fail_0",
        "suite/test_sample.py::test_fail_1",
    ]


@MARK_CONTRACT
def test_c013_the_list_combines_every_pass(tmp_path):
    """A two-pass run must write ONE list carrying the failures of both passes (mutation leg
    M-6: writing the list from the parallel pass alone loses the serial exception)."""
    root = tmp_path / "two-pass"
    root.mkdir()
    (root / "pytest.ini").write_text("[pytest]\nmarkers =\n    serial: x\n", encoding="utf-8")
    (root / "test_mixed.py").write_text(
        "import pytest\n\n"
        "def test_parallel_fail():\n    assert False\n\n"
        "@pytest.mark.serial\n"
        "def test_serial_fail():\n    assert False\n",
        encoding="utf-8",
    )
    names = tmp_path / "names.txt"
    done = _run(["--workers", "2", "--names-out", names, str(root), "-q"], cwd=tmp_path)
    assert done.returncode == 1, done.stdout + done.stderr
    mode, rest = _mode(done.stderr)
    assert mode == "parallel", done.stderr
    match = _list_line(done.stderr)
    assert int(match.group("k")) == 2, f"both passes must contribute: {done.stderr}"
    assert sorted(n.rsplit("::", 1)[-1] for n in _names(names)) == [
        "test_parallel_fail",
        "test_serial_fail",
    ], _names(names)
    assert int(match.group("n")) == 2, done.stderr


@MARK_CONTRACT
def test_c014_list_line_carries_both_entry_and_pass_counts(tmp_path):
    suite = _write_suite(tmp_path, failing=1)
    names = tmp_path / "names.txt"
    done = _run(["--serial", "--names-out", names, str(suite), "-q"], cwd=tmp_path)
    match = _list_line(done.stderr)
    assert match.group("path") == str(names), done.stderr
    assert int(match.group("n")) == len(_names(names)) == 1, done.stderr
    assert int(match.group("k")) >= 1, done.stderr


@MARK_CONTRACT
def test_c014_empty_list_is_distinguishable_from_a_missing_one(tmp_path):
    suite = _write_suite(tmp_path)
    names = tmp_path / "names.txt"
    done = _run(["--serial", "--names-out", names, str(suite), "-q"], cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr
    assert names.is_file()
    assert _names(names) == []
    match = _list_line(done.stderr)
    assert int(match.group("n")) == 0, done.stderr


# --------------------------------------------------------------------------- #
# C-012 — exit 5 is normalized for the serial pass only
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_c012_serial_pass_exit_5_normalized_but_parallel_pass_exit_5_is_not(tmp_path):
    root = tmp_path / "two-pass"
    root.mkdir()
    # a suite where every test is marked `serial`: the parallel pass collects nothing
    # (exit 5) while the serial pass collects everything. A correct runner keeps the two
    # apart, so the empty parallel pass is the one that fails this run.
    (root / "pytest.ini").write_text("[pytest]\nmarkers =\n    serial: x\n", encoding="utf-8")
    (root / "test_all_serial.py").write_text(
        "import pytest\n\n"
        "@pytest.mark.serial\n"
        "def test_a():\n    assert True\n\n"
        "@pytest.mark.serial\n"
        "def test_b():\n    assert True\n",
        encoding="utf-8",
    )
    done = _run(["--workers", "2", "--names-out", tmp_path / "n.txt", str(root), "-q"], cwd=tmp_path)
    assert done.returncode == 5, (
        "the parallel pass collected nothing, so exit 5 must NOT be normalized:\n"
        + done.stdout + done.stderr
    )
    mode, rest = _mode(done.stderr)
    assert mode == "parallel", done.stderr

    # and the mirror-image case: a parallel pass with work, a serial pass with none
    green = _write_suite(tmp_path / "green")
    ok = _run(["--workers", "2", "--names-out", tmp_path / "g.txt", str(green), "-q"], cwd=tmp_path)
    assert ok.returncode == 0, (
        "an empty serial pass must normalize to 0:\n" + ok.stdout + ok.stderr
    )
    match = _list_line(ok.stderr)
    assert int(match.group("k")) >= 1, ok.stderr


@MARK_CONTRACT
def test_c015_exit_code_is_non_zero_iff_a_pass_failed(tmp_path):
    ok = _write_suite(tmp_path / "green")
    green = _run(["--serial", "--names-out", tmp_path / "g.txt", str(ok), "-q"], cwd=tmp_path)
    assert green.returncode == 0, green.stdout + green.stderr

    bad = _write_suite(tmp_path / "red", failing=1)
    red = _run(["--serial", "--names-out", tmp_path / "r.txt", str(bad), "-q"], cwd=tmp_path)
    assert red.returncode == 1, red.stdout + red.stderr


# --------------------------------------------------------------------------- #
# C-016 — byte-identical carriers
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_c016_runner_carriers_are_byte_identical():
    assert RUNNER.is_file() and MIRROR.is_file()
    assert RUNNER.read_bytes() == MIRROR.read_bytes(), (
        "scripts/bash/run-tests.sh and .specify/scripts/bash/run-tests.sh drifted — "
        "regenerate the mirror with `python3 scripts/python/sync-mirrors.py --write --only scripts/bash`"
    )
