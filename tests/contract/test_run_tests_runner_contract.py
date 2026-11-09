"""Contract cases for the canonical runner's execution model (086, C-001…C-016).

Owner of the propositions: `.specify/specs/086-efficient-test-execution/contracts/
runner-contract-086.contract.md`. Two slices share this file, and the split is additive — WP-A4's
block is appended after WP-A1's and rewrites none of it:

- WP-A1 carries default mode, worker resolution, the escape hatches, the two-pass list/exit
  semantics and the exit-5 normalization.
- WP-A4 carries the serial-exception clauses C-010/C-011, the two-pass green point, the
  C-003/C-008 truthfulness pairs named by T012, and the parallel-safety disposition (T013).

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


@MARK_CONTRACT
@pytest.mark.parametrize("dist_args", [["--dist", "loadfile"], ["--dist=loadfile"]])
def test_c009_caller_scheduler_is_not_overridden(tmp_path, dist_args):
    """The runner's default ``--dist load`` never lands on top of the caller's own scheduler.

    Without this guard ``--workers 2 --dist loadfile`` becomes ``-n 2 --dist load
    --dist loadfile`` and the mode line reports ``dist=load``; the A13 experiment
    (quickstart S-5 / T016) could not then compare ``load`` with ``loadfile``.
    """
    suite = _write_suite(tmp_path)
    done = _run(["--workers", "2", *dist_args, str(suite), "-q"], cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr
    header = _command_lines(done.stderr)
    assert len(header) == 1, done.stderr
    tokens = header[0].split()
    assert tokens.count("--dist") + sum(t.startswith("--dist=") for t in tokens) == 1, header[0]
    assert "loadfile" in header[0], header[0]
    assert header[0].count("-n 2") == 1, header[0]
    mode = [line for line in done.stderr.splitlines() if "mode=parallel" in line]
    assert mode and "dist=loadfile" in mode[0], done.stderr


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
# C-016 — carriers under the declared projection (superseded clause)
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_c016_runner_carriers_follow_the_declared_projection():
    """C-016 under the declared projection: the mirror equals source + bash-version-guard.

    086's C-016 asked for byte identity. That carriage clause is **superseded by
    `.specify/specs/089-script-interface-contract/contracts/mirror-projection.contract.md`**
    (source + declared projection, C-34/C-35): `run-tests.sh` now carries the projected
    version answer, so the pair is judged by the projection the sync engine declares, not
    by raw equality — the mirror is still generated, never hand-edited (089 C-33).
    """
    import importlib.util

    assert RUNNER.is_file() and MIRROR.is_file()
    spec = importlib.util.spec_from_file_location(
        "sync_mirrors_under_test", ROOT / "scripts" / "python" / "sync-mirrors.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    expected, applied = module.project_source(RUNNER.read_text(encoding="utf-8"),
                                              "bash-version-guard")
    assert applied, f"the projection refused the pair: {expected}"
    assert expected == MIRROR.read_text(encoding="utf-8"), (
        "scripts/bash/run-tests.sh and .specify/scripts/bash/run-tests.sh drifted from the "
        "declared projection — regenerate with `sync-mirrors.py --write --only scripts`"
    )


# =========================================================================== #
# WP-A4 slice (tasks T004, T005, T012, T013) — appended after WP-A1's cases.
#
# The cases above are WP-A1's; the block below is additive and carries the C-010/C-011
# serial-exception clauses (T004), the two-pass green point (T005), the truthfulness
# pairs T012 names explicitly, and the parallel-safety disposition (T013).
# =========================================================================== #

EXCEPTIONS_LINE = re.compile(
    r"^# test runner exceptions: (?P<n>\d+) declared serial test\(s\)$", re.M
)
MIXED_SUITE = (
    "import pytest\n\n"
    "def test_plain_a():\n    assert True\n\n"
    "def test_plain_b():\n    assert True\n\n"
    "@pytest.mark.serial\n"
    "def test_marked_ok():\n    assert True\n"
)
EXPECTED_TYPO_ERRORS = {
    "--workers": "error: --workers expects a positive integer or \"auto\", got \"abc\"",
    "SPECKIT_TEST_WORKERS": (
        "error: SPECKIT_TEST_WORKERS expects a positive integer or \"auto\", got \"abc\""
    ),
}


def _write_mixed_suite(root: Path, body: str = MIXED_SUITE) -> Path:
    """A small suite whose ``serial``-marked members are what C-010/C-011 talk about."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "pytest.ini").write_text("[pytest]\nmarkers =\n    serial: x\n", encoding="utf-8")
    (root / "test_mixed.py").write_text(body, encoding="utf-8")
    return root


def _engine_env():
    """Environment for the raw-engine probes: no ``SPECKIT_PYTHON``, no inherited worker id."""
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("PYTEST_XDIST_WORKER", None)
    return env


def _exception_count(done):
    """The declared-exception count the runner reported, or ``None`` when it reported none.

    C-011's enumeration is the property under test here (not a formatting detail), so a runner
    that states the count in another wording still satisfies it; the assertion in each case is
    about the *value*.
    """
    match = EXCEPTIONS_LINE.search(done.stderr)
    return None if match is None else int(match.group("n"))


def _assert_no_unknown_mark(done, where: str) -> None:
    assert "PytestUnknownMarkWarning" not in done.stderr, (
        f"{where}: the `serial` marker is not registered, so the exception set is not a "
        f"declared exception:\n{done.stderr}"
    )


# --------------------------------------------------------------------------- #
# C-010 — the marked test leaves the parallel pass and is re-run serially
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_c010_marked_test_is_excluded_from_the_parallel_pass(tmp_path):
    """C-010, first half. The discriminating observation is the *engine's own* report of what
    the parallel pass collected: when marked tests are excluded the parallel pass reports the two
    unmarked tests, and when they are not excluded it reports all three (the case below). The
    two counts differ by exactly the marked member, so neither half can pass vacuously."""
    root = _write_mixed_suite(tmp_path / "tree")
    done = _run(["--workers", "2", str(root), "-q"], cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr
    mode, _ = _mode(done.stderr)
    assert mode == "parallel", done.stderr
    assert _exception_count(done) == 1, done.stderr
    _assert_no_unknown_mark(done, "parallel pass")

    parallel = subprocess.run(
        [_python(), "-m", "pytest", str(root), "-q", "-n", "2", "--dist", "load",
         "-m", "not serial"],
        capture_output=True,
        text=True,
        cwd=str(tmp_path),
        env=_engine_env(),
    )
    assert parallel.returncode == 0, parallel.stdout + parallel.stderr
    assert re.search(r"\b2 passed\b", parallel.stdout), (
        "the parallel pass must collect the unmarked tests only:\n" + parallel.stdout
    )

    serial = subprocess.run(
        [_python(), "-m", "pytest", str(root), "-q", "-n0", "-m", "serial"],
        capture_output=True,
        text=True,
        cwd=str(tmp_path),
        env=_engine_env(),
    )
    assert serial.returncode == 0, serial.stdout + serial.stderr
    assert re.search(r"\b1 passed\b", serial.stdout), (
        "the serial pass must collect exactly the marked exception:\n" + serial.stdout
    )


@MARK_CONTRACT
def test_c010_marked_test_is_included_when_the_marker_is_ignored(tmp_path):
    """C-010's negative control: the same tree without the exclusion collects all three tests.
    Without this leg the case above could pass on a suite that simply has two tests."""
    root = _write_mixed_suite(tmp_path / "tree")
    everything = subprocess.run(
        [_python(), "-m", "pytest", str(root), "-q"],
        capture_output=True,
        text=True,
        cwd=str(tmp_path),
        env=_engine_env(),
    )
    assert everything.returncode == 0, everything.stdout + everything.stderr
    assert re.search(r"\b3 passed\b", everything.stdout), everything.stdout


@MARK_CONTRACT
def test_c010_the_runner_re_runs_the_exception_reaching_the_combined_exit_code(tmp_path):
    """C-010, second half: exclusion alone would silently drop the marked test. A failure
    injected into it must still be executed, must appear in the combined list and must reach
    the run's exit code."""
    root = _write_mixed_suite(
        tmp_path / "tree",
        "import pytest\n\n"
        "def test_plain_ok():\n    assert True\n\n"
        "@pytest.mark.serial\n"
        "def test_marked_fail():\n    assert False\n",
    )
    names = tmp_path / "names.txt"
    done = _run(["--workers", "2", "--names-out", names, str(root), "-q"], cwd=tmp_path)
    assert done.returncode == 1, (
        "the failure lives in the serial pass, so the combined exit code must carry it:\n"
        + done.stdout + done.stderr
    )
    assert _names(names) == ["tree/test_mixed.py::test_marked_fail"], _names(names)
    match = _list_line(done.stderr)
    assert int(match.group("k")) == 2, f"both passes must contribute: {done.stderr}"


def _engine_env():
    """Environment for the raw-engine probes: no ``SPECKIT_PYTHON``, no inherited worker id."""
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("PYTEST_XDIST_WORKER", None)
    return env


# --------------------------------------------------------------------------- #
# C-011 — the exception set is enumerable by name, with a recordable size
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_c011_exception_set_is_enumerable_by_name_and_counted(tmp_path):
    root = _write_mixed_suite(tmp_path / "tree")
    enumerated = subprocess.run(
        [_python(), "-m", "pytest", "-m", "serial", "--collect-only", "-q", str(root)],
        capture_output=True,
        text=True,
        cwd=str(tmp_path),
        env=_engine_env(),
    )
    assert enumerated.returncode == 0, enumerated.stdout + enumerated.stderr
    members = [ln.strip() for ln in enumerated.stdout.splitlines() if "::" in ln]
    assert len(members) == 1, enumerated.stdout
    assert members[0].endswith("test_mixed.py::test_marked_ok"), members

    done = _run(["--workers", "2", str(root), "-q"], cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr


@MARK_CONTRACT
def test_c011_runner_records_the_exception_count_it_acted_on(tmp_path):
    """The count the runner acts on is displayed and equals the enumerable member count, so a
    global "parallel off" switch (which would have no member list) cannot satisfy the clause."""
    root = _write_mixed_suite(tmp_path / "tree")
    done = _run(["--workers", "2", str(root), "-q"], cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr
    # the count the runner acted on is the enumerable member count (readable from stderr) ...
    assert _exception_count(done) == 1, done.stderr
    # ... and the mode is still parallel with a second pass: a global "parallel off" switch,
    # which has no member list at all, could satisfy neither observation.
    mode, note = _mode(done.stderr)
    assert mode == "parallel", done.stderr
    assert "passes=2" in note, note


@MARK_CONTRACT
def test_c011_a_tree_without_exceptions_records_zero(tmp_path):
    """The count is truthful in the other direction too: no marked test, no second pass, and
    the run is still reported as one parallel pass."""
    suite = _write_suite(tmp_path / "plain")
    done = _run(["--workers", "2", str(suite), "-q"], cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr
    assert _exception_count(done) is None, done.stderr
    mode, note = _mode(done.stderr)
    assert mode == "parallel", done.stderr
    assert "passes=1" in note, note


# --------------------------------------------------------------------------- #
# C-015 (T005's green point) — a green parallel pass with an empty serial pass exits 0
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_c015_green_parallel_pass_with_an_empty_serial_pass_exits_zero(tmp_path):
    """The two-pass green point (T005): the serial pass is *reachable and empty* — every marked
    member is deselected because the caller's selection is a single unmarked test — yet the run
    exits 0, because C-012 normalizes the serial pass's exit 5. The two halves are asserted
    together, so "green" cannot be produced by skipping the second pass: the runner must record
    that the pass ran (``passes=``) while reporting zero failures in the combined list."""
    root = _write_mixed_suite(
        tmp_path / "tree",
        "import pytest\n\n"
        "def test_plain_a():\n    assert True\n\n"
        "def test_plain_b():\n    assert True\n\n"
        "@pytest.mark.serial\n"
        "def test_marked_ok():\n    assert True\n\n"
        "def test_deselect_me():\n    assert True\n",
    )
    plain = tmp_path / "tree" / "test_mixed.py"
    names = tmp_path / "names.txt"
    done = _run(
        [
            "--workers", "2", "--names-out", names,
            str(plain) + "::test_plain_a", str(plain) + "::test_plain_b", str(plain) + "::test_marked_ok",
            "-q",
        ],
        cwd=tmp_path,
    )
    assert done.returncode == 0, (
        "an empty serial pass must normalize to 0 — a green parallel pass stays green:\n"
        + done.stdout + done.stderr
    )
    assert _exception_count(done) == 1, (
        "the declared member must still be enumerated, otherwise the serial pass was skipped "
        "rather than run and normalized:\n" + done.stderr
    )
    match = _list_line(done.stderr)
    assert int(match.group("k")) == 2, done.stderr
    assert int(match.group("n")) == 0, done.stderr
    assert names.is_file() and _names(names) == []


# --------------------------------------------------------------------------- #
# T012 — truthfulness: the header never names an unapplied argument, and a typo is named
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
@pytest.mark.parametrize(
    "flag_args, env_extra, expected",
    [
        (["--workers", "3"], {}, "-n 3"),
        # the runner's own environment variable is a *config* source, not a pytest argument:
        # forwarding it is what FR-003 forbids, so the effective count must still reach the
        # header (as the resolved value, never as the variable's name)
        ([], {"SPECKIT_TEST_WORKERS": "3"}, ("-n 3", "--numprocesses=3")),
        (["--serial", "--workers", "3"], {}, "-n0"),
    ],
)
def test_t012_header_never_names_an_unapplied_worker_argument(
    tmp_path, flag_args, env_extra, expected
):
    """C-003 in its concrete form: ``--workers`` / ``SPECKIT_TEST_WORKERS`` are the runner's own
    inputs, never pytest arguments. In serial mode a tuned worker count is resolved but not
    applied, so it must not appear in the command header at all."""
    suite = _write_suite(tmp_path)
    done = _run([*flag_args, str(suite), "-q"], cwd=tmp_path, env_extra=env_extra)
    assert done.returncode == 0, done.stdout + done.stderr
    header = _command_lines(done.stderr)
    assert len(header) == 1, done.stderr
    line = header[0]
    assert "--workers" not in line, line
    assert "SPECKIT_TEST_WORKERS" not in line, line
    alternatives = expected if isinstance(expected, tuple) else (expected,)
    assert any(alt in line for alt in alternatives), line
    # exactly one worker-count switch in the applied form (no-resolved-yet-unapplied value
    # survives the dedup above, because the resolved count either IS the switch or is absent)
    applied = [t for t in line.split() if is_worker_switch(t)]
    assert len(applied) == 1, f"exactly one worker-count switch must run: {line}"


@MARK_CONTRACT
@pytest.mark.parametrize("source", ["--workers", "SPECKIT_TEST_WORKERS"])
def test_t012_config_typo_is_refused_before_anything_runs(tmp_path, source):
    """A typo must not become a healthy-looking single-worker run: whichever of the two inputs
    carried it, the runner exits non-zero and names the offending value and its own source."""
    suite = _write_suite(tmp_path)
    args = ["--workers", "abc"] if source == "--workers" else []
    env_extra = {} if source == "--workers" else {"SPECKIT_TEST_WORKERS": "abc"}
    done = _run([*args, str(suite), "-q"], cwd=tmp_path, env_extra=env_extra)
    assert done.returncode == 2, done.stdout + done.stderr
    assert EXPECTED_TYPO_ERRORS[source] in done.stderr, done.stderr
    assert "# test runner: mode=" not in done.stderr, (
        "a refused configuration must not reach mode resolution:\n" + done.stderr
    )


@MARK_CONTRACT
def test_t012_typo_leaves_no_trace_of_a_run(tmp_path):
    """The corollary that makes the previous case load-bearing: nothing was executed, so no
    failed-name list is written and no pytest output is produced."""
    suite = _write_suite(tmp_path, failing=1)
    names = tmp_path / "names.txt"
    done = _run(["--workers", "nope", "--names-out", names, str(suite), "-q"], cwd=tmp_path)
    assert done.returncode == 2, done.stdout + done.stderr
    assert not names.exists(), done.stderr
    assert "FAILED" not in done.stdout, done.stdout


# --------------------------------------------------------------------------- #
# T013 — parallel-safety disposition: excluded, re-run, combined exactly once
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_t013_one_failure_per_member_across_both_passes(tmp_path):
    """The disposition case: one marked failure and one plain failure land in the combined list
    exactly once each, and the run is still ONE run (one list, one exit code)."""
    root = _write_mixed_suite(
        tmp_path / "tree",
        "import pytest\n\n"
        "def test_plain_fail():\n    assert False\n\n"
        "@pytest.mark.serial\n"
        "def test_marked_fail():\n    assert False\n",
    )
    names = tmp_path / "names.txt"
    done = _run(["--workers", "2", "--names-out", names, str(root), "-q"], cwd=tmp_path)
    assert done.returncode == 1, done.stdout + done.stderr
    listed = _names(names)
    assert sorted(listed) == [
        "tree/test_mixed.py::test_marked_fail",
        "tree/test_mixed.py::test_plain_fail",
    ], listed
    assert len(listed) == len(set(listed)), f"the combined list must not repeat a name: {listed}"
    match = _list_line(done.stderr)
    assert int(match.group("n")) == 2 and int(match.group("k")) == 2, done.stderr
    assert len(_command_lines(done.stderr)) == 1, "one run, one command header"


@MARK_CONTRACT
def test_t013_unmarked_tests_keep_their_full_parallel_freedom(tmp_path):
    """The exception must not cost the rest of the suite its parallelism: with only the marked
    member present, the parallel pass must still be a real multi-worker pass (the header names
    the engine switch), so declaring an exception is not a silent global serial switch."""
    root = _write_mixed_suite(tmp_path / "tree")
    done = _run(["--workers", "2", str(root), "-q"], cwd=tmp_path)
    assert done.returncode == 0, done.stdout + done.stderr
    header = _command_lines(done.stderr)[0]
    assert "-n 2" in header and "--dist load" in header, header
