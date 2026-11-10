"""Contract cases for parallel-consistency verification (098, C-001…C-012).

Owner of the propositions: `.specify/specs/098-suite-speed-optimizations/contracts/
parallel-consistency.contract.md`. Judgement surface: the failure NAME lists the runner
writes with ``--names-out`` — never a reading of the tests and never a wall-clock threshold
(C-001, C-005). Durations are read only as disclosure fields of a record and compared with
no bound anywhere in this file.

Cases:

1. ``test_the_comparison_record_judges_by_failure_names`` — the contract-subset record
   (T015, ``test-evidence/parallel-consistency-contract.txt``): both commands recorded with
   an explicit bounded ``--workers`` (never ``auto``), one default-parallel arm and one
   ``--serial`` arm on the same recorded tree, the two ``comm`` directions both empty and
   re-derived from the persisted name lists, and the C-012 field set complete.
2. ``test_the_subset_record_does_not_claim_full_suite_safety`` — C-008: the subset record
   declares its scope and MUST NOT claim full-suite safety before the full-tree comparison
   record (the closure stage's) exists.
3. ``test_the_no_xdist_record_shows_a_complete_serial_run`` — the PYTHONPATH-shim record
   (T016, ``test-evidence/parallel-consistency-noxdist.txt``): ``mode=serial reason=no-xdist``,
   pytest's own exit code, a valid name list, and a summary proving the run executed tests
   (C-010/C-011: never an error exit, never an empty run).
4. ``test_non_parallel_safe_fixture_turns_the_comparison_non_empty`` — C-009's drill: two
   tests writing one shared path behind cross-process file barriers must make the two-way
   name comparison non-empty. The drill proves the comparison is a discriminator, not a
   green label; its recorded output lives in ``notes/red-first-evidence.md`` (T014).

Construction constraints: nested runner invocations use a clean environment (no inherited
``PYTEST_XDIST_WORKER``/``PYTHONPATH``/``SPECKIT_TEST_WORKERS``) and an explicit worker
bound, so a case never observes the parent run's shape. The verifier file itself is excluded
from the subset comparison it judges (a record cannot contain the outcome of the case that
asserts on it); the exclusion is pinned by the record's ``excluded_from_comparison`` field
and the guard file's own parallel behaviour is covered by its green run under the runner
(T017) and the closure full-tree comparison (T061).
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

MARK_CONTRACT = pytest.mark.contract

SPEC_DIR = ROOT / ".specify" / "specs" / "098-suite-speed-optimizations"
EVIDENCE_DIR = SPEC_DIR / "test-evidence"
COMPARISON_RECORD = EVIDENCE_DIR / "parallel-consistency-contract.txt"
NOXDIST_RECORD = EVIDENCE_DIR / "parallel-consistency-noxdist.txt"
CLOSURE_RECORD = EVIDENCE_DIR / "closure.txt"
GUARD_FILE = "tests/contract/test_parallel_consistency_contract.py"

COMPARISON_BEGIN = "<!-- parallel-comparison:begin -->"
COMPARISON_END = "<!-- parallel-comparison:end -->"
NOXDIST_BEGIN = "<!-- no-xdist:begin -->"
NOXDIST_END = "<!-- no-xdist:end -->"

#: C-012's field set for the comparison record. Exact: a missing field means the record
#: does not support the claim, and an unexpected field means the schema drifted.
COMPARISON_KEYS = (
    "parallel_tree_root",
    "parallel_tree_head",
    "parallel_command",
    "parallel_exit",
    "parallel_duration_s",
    "parallel_mode_line",
    "parallel_names_path",
    "parallel_names_count",
    "serial_tree_root",
    "serial_tree_head",
    "serial_command",
    "serial_exit",
    "serial_duration_s",
    "serial_mode_line",
    "serial_names_path",
    "serial_names_count",
    "comm_13_count",
    "comm_23_count",
    "pre_existing_failures",
    "scope",
    "full_suite_safety_claimed",
    "excluded_from_comparison",
)

#: The single-run no-xdist record (C-010/C-011); no comm fields exist for one run.
NOXDIST_KEYS = (
    "command",
    "exit",
    "duration_s",
    "mode_line",
    "names_path",
    "names_count",
    "summary",
    "construction",
)

MODE_LINE = re.compile(r"^# test runner: mode=(?P<mode>\w+)(?P<rest>.*)$", re.M)
NODE_ID = re.compile(r"^tests/\S+::.+$")
NUMBER = re.compile(r"^\d+(?:\.\d+)?$")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _python() -> str:
    """The interpreter the runner will resolve: keep the test independent of CWD."""
    return os.environ.get("SPECKIT_PYTHON") or sys.executable


def _run(args, *, cwd=None, env_extra=None):
    """Invoke the runner from a clean environment (construction constraints above)."""
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("PYTEST_XDIST_WORKER", None)
    env.pop("SPECKIT_TEST_WORKERS", None)
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
    match = MODE_LINE.search(stderr)
    assert match is not None, f"no mode line on stderr:\n{stderr}"
    return match.group("mode"), match.group("rest").strip()


def _field(rest: str, name: str) -> str:
    match = re.search(rf"\b{name}=(\S+)", rest)
    assert match is not None, f"mode line carries no {name}= field: {rest!r}"
    return match.group(1)


def _block(path: Path, begin: str, end: str, owner: str) -> dict:
    """Parse the marker-delimited ``key: value`` machine block; any malformation is red."""
    assert path.is_file(), (
        f"the verification record is missing: {path} — {owner} owns this record "
        "(C-012: a record missing its fields does not support the claim)"
    )
    text = path.read_text(encoding="utf-8")
    assert text.count(begin) == 1 and text.count(end) == 1, (
        f"{path} must carry exactly one {begin} / {end} pair"
    )
    body = text.split(begin, 1)[1].split(end, 1)[0]
    fields: dict = {}
    for number, line in enumerate(body.splitlines(), 1):
        stripped = line.strip()
        if not stripped:
            continue
        key, sep, value = stripped.partition(":")
        assert sep, f"{path.name}:{number} is not a 'key: value' field: {stripped!r}"
        key = key.strip()
        assert key not in fields, f"{path.name}: duplicate field {key!r}"
        fields[key] = value.strip()
    return fields


def _require_schema(path: Path, fields: dict, keys, owner: str) -> None:
    missing = sorted(set(keys) - set(fields))
    unexpected = sorted(set(fields) - set(keys))
    assert not missing and not unexpected, (
        f"{path.name} field set must be exactly the declared schema ({owner}): "
        f"missing={missing} unexpected={unexpected}"
    )


def _names(path: Path, source: str) -> list:
    """One node id per line, de-duplicated.

    Ordering is the runner's own `sort -u` under the run locale (en_US.UTF-8 on this host),
    which is what makes the lists comm-readable in the recorded run; the guard deliberately
    re-derives the differences by name through sets, so its judgement never depends on the
    collation of either the host or Python's code-point order.
    """
    assert path.is_file(), f"the recorded names list is missing: {path} ({source})"
    names = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    for number, name in enumerate(names, 1):
        assert NODE_ID.fullmatch(name), f"{path.name}:{number} is not a node id: {name!r}"
    assert len(names) == len(set(names)), f"{path.name} must be de-duplicated"
    return names


def _int_field(fields: dict, key: str, path: Path) -> int:
    assert re.fullmatch(r"\d+", fields[key]), f"{path.name}: {key} is not an integer: {fields[key]!r}"
    return int(fields[key])


def _float_field(fields: dict, key: str, path: Path) -> float:
    assert NUMBER.fullmatch(fields[key]), f"{path.name}: {key} is not a number: {fields[key]!r}"
    return float(fields[key])


def _declared_pre_existing(value: str) -> set:
    if value.strip().lower() == "none":
        return set()
    return {item.strip() for item in value.split(";") if item.strip()}


# --------------------------------------------------------------------------- #
# C-001…C-006, C-012 — the contract-subset record judges by failure names
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_the_comparison_record_judges_by_failure_names():
    fields = _block(
        COMPARISON_RECORD, COMPARISON_BEGIN, COMPARISON_END, "T015"
    )
    _require_schema(COMPARISON_RECORD, fields, COMPARISON_KEYS, "C-012")

    # C-003: one tree — the two arms' recorded identities must agree and be present.
    for key in ("parallel_tree_root", "serial_tree_root", "parallel_tree_head", "serial_tree_head"):
        assert fields[key], f"the record carries no {key}; tree identity is not optional (C-003)"
    assert fields["parallel_tree_root"] == fields["serial_tree_root"], (
        "the two arms were recorded on different tree roots; a cross-tree comparison is "
        "not isolation evidence (C-003)"
    )
    assert fields["parallel_tree_head"] == fields["serial_tree_head"], (
        "the two arms were recorded on different tree heads; a cross-tree comparison is "
        "not isolation evidence (C-003)"
    )

    # C-006: staged order, explicit bounded workers (never `auto` for evidence stability).
    parallel_command = fields["parallel_command"]
    worker_match = re.search(r"--workers[ =]([0-9]+)\b", parallel_command)
    assert worker_match is not None, (
        "the parallel arm MUST carry an explicit numeric --workers bound (never `auto` "
        f"for evidence stability): {parallel_command!r}"
    )
    assert int(worker_match.group(1)) > 0, parallel_command
    assert "--serial" not in parallel_command.split(), (
        f"the parallel arm MUST be the default-parallel run (C-002): {parallel_command!r}"
    )
    assert "tests/contract" in parallel_command and "--names-out" in parallel_command, (
        f"the parallel arm MUST select tests/contract with --names-out (C-006): {parallel_command!r}"
    )
    serial_command = fields["serial_command"]
    assert "--serial" in serial_command.split(), (
        f"the comparison arm MUST be the --serial run; without it the two lists come from "
        f"the same shape and prove nothing (C-002): {serial_command!r}"
    )
    assert "tests/contract" in serial_command and "--names-out" in serial_command, (
        f"the serial arm MUST select tests/contract with --names-out (C-006): {serial_command!r}"
    )
    assert fields["scope"] == "contract-subset", (
        f"the subset record MUST declare scope=contract-subset: {fields['scope']!r}"
    )
    assert fields["excluded_from_comparison"] == GUARD_FILE, (
        "the comparison MUST exclude exactly this verifier file (a record cannot contain "
        f"the outcome of the case that asserts on it): {fields['excluded_from_comparison']!r}"
    )
    assert f"--ignore={GUARD_FILE}" in parallel_command, parallel_command
    assert f"--ignore={GUARD_FILE}" in serial_command, serial_command

    # Same selection on both arms: the mode lines disclose the same tier and slow count.
    parallel_mode, parallel_rest = _mode(fields["parallel_mode_line"])
    serial_mode, serial_rest = _mode(fields["serial_mode_line"])
    assert parallel_mode == "parallel", fields["parallel_mode_line"]
    assert serial_mode == "serial", fields["serial_mode_line"]
    assert _field(parallel_rest, "tier") == _field(serial_rest, "tier") == "fast", (
        f"the two arms MUST share one tier: {parallel_rest} / {serial_rest}"
    )
    assert _field(parallel_rest, "excluded_slow") == _field(serial_rest, "excluded_slow"), (
        f"the two arms MUST share one selection (disclosed slow count): {parallel_rest} / {serial_rest}"
    )

    # Durations are disclosure only — parsed, never compared with a bound (C-001, C-005).
    _float_field(fields, "parallel_duration_s", COMPARISON_RECORD)
    _float_field(fields, "serial_duration_s", COMPARISON_RECORD)

    # C-012/C-002/C-004: the persisted lists are the judgement; both comm directions empty.
    parallel_names = _names(ROOT / fields["parallel_names_path"], "parallel arm")
    serial_names = _names(ROOT / fields["serial_names_path"], "serial arm")
    assert len(parallel_names) == _int_field(fields, "parallel_names_count", COMPARISON_RECORD), (
        f"{fields['parallel_names_path']} does not match its recorded line count"
    )
    assert len(serial_names) == _int_field(fields, "serial_names_count", COMPARISON_RECORD), (
        f"{fields['serial_names_path']} does not match its recorded line count"
    )
    parallel_set, serial_set = set(parallel_names), set(serial_names)
    only_serial = [name for name in serial_names if name not in parallel_set]
    only_parallel = [name for name in parallel_names if name not in serial_set]
    assert _int_field(fields, "comm_13_count", COMPARISON_RECORD) == len(only_serial), (
        "the recorded comm -13 count disagrees with the persisted lists"
    )
    assert _int_field(fields, "comm_23_count", COMPARISON_RECORD) == len(only_parallel), (
        "the recorded comm -23 count disagrees with the persisted lists"
    )
    assert not only_serial, f"comm -13 is non-empty (C-002): {only_serial[:5]}"
    assert not only_parallel, f"comm -23 is non-empty (C-002): {only_parallel[:5]}"

    # C-004: shared failures are compared by name and every shared name is declared.
    declared = _declared_pre_existing(fields["pre_existing_failures"])
    assert declared == parallel_set & serial_set, (
        "every failure present on both sides must be declared pre-existing by name "
        f"(C-004): declared={sorted(declared)} shared={sorted(parallel_set & serial_set)}"
    )

    # The exits are pytest's own codes and agree with the failure lists.
    parallel_exit = _int_field(fields, "parallel_exit", COMPARISON_RECORD)
    serial_exit = _int_field(fields, "serial_exit", COMPARISON_RECORD)
    assert parallel_exit in (0, 1), f"parallel arm exit is not pytest's own code: {parallel_exit}"
    assert serial_exit in (0, 1), f"serial arm exit is not pytest's own code: {serial_exit}"
    assert (parallel_exit != 0) == bool(parallel_names), "parallel exit disagrees with its list"
    assert (serial_exit != 0) == bool(serial_names), "serial exit disagrees with its list"


# --------------------------------------------------------------------------- #
# C-008 — the subset record never claims full-suite safety on its own
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_the_subset_record_does_not_claim_full_suite_safety():
    fields = _block(COMPARISON_RECORD, COMPARISON_BEGIN, COMPARISON_END, "T015")
    assert fields["scope"] == "contract-subset", (
        f"the record's scope MUST stay the verified subset: {fields['scope']!r}"
    )
    claimed = fields["full_suite_safety_claimed"]
    assert claimed in ("yes", "no"), (
        f"full_suite_safety_claimed must be yes|no: {claimed!r}"
    )
    if claimed == "yes":
        assert CLOSURE_RECORD.is_file() and CLOSURE_RECORD.stat().st_size > 0, (
            "the subset record claims full-suite parallel safety, but the full-tree "
            f"comparison record ({CLOSURE_RECORD}) does not exist; a verified subset MUST "
            "NOT be reported as full-suite safety until the full-tree comparison lands (C-008)"
        )


# --------------------------------------------------------------------------- #
# C-010/C-011 — the no-xdist shim completes a serial run and says why
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_the_no_xdist_record_shows_a_complete_serial_run():
    fields = _block(NOXDIST_RECORD, NOXDIST_BEGIN, NOXDIST_END, "T016")
    _require_schema(NOXDIST_RECORD, fields, NOXDIST_KEYS, "C-010/C-011")

    command = fields["command"]
    assert "tests/contract" in command and "--names-out" in command, (
        f"the no-xdist run MUST select tests/contract with --names-out (C-006): {command!r}"
    )
    assert "PYTHONPATH" in command, (
        "the record MUST expose the PYTHONPATH shim construction so the missing-engine "
        f"premise is re-probeable (C-010): {command!r}"
    )

    mode_line = fields["mode_line"]
    assert mode_line.startswith("# test runner: mode=serial"), (
        f"a missing engine MUST fall back to a complete serial run: {mode_line!r}"
    )
    assert "reason=no-xdist" in mode_line, (
        f"the mode line MUST name the missing engine: {mode_line!r}"
    )

    exit_code = _int_field(fields, "exit", NOXDIST_RECORD)
    assert exit_code in (0, 1), (
        f"the no-xdist run MUST exit with pytest's own code, never a runner error (C-010): {exit_code}"
    )
    duration = _float_field(fields, "duration_s", NOXDIST_RECORD)
    assert duration > 0, f"duration_s must be a positive disclosure reading: {duration}"

    names = _names(ROOT / fields["names_path"], "no-xdist arm")
    assert len(names) == _int_field(fields, "names_count", NOXDIST_RECORD), (
        f"{fields['names_path']} does not match its recorded line count"
    )
    assert (exit_code != 0) == bool(names), "the exit code disagrees with the failure list"

    summary = fields["summary"]
    passed_match = re.search(r"(\d+) passed", summary)
    assert passed_match is not None and int(passed_match.group(1)) > 0, (
        "the no-xdist run MUST NOT run nothing (C-011): its summary carries no passing "
        f"count: {summary!r}"
    )
    construction = fields["construction"].lower()
    assert "shim" in construction and "python 3.8" in construction, (
        "the record MUST disclose the declared reduced measurement: no Python 3.8 "
        f"interpreter exists on this host, the PYTHONPATH shim stands in (C-010): "
        f"{fields['construction']!r}"
    )


# --------------------------------------------------------------------------- #
# C-009 — the drill: a non-parallel-safe suite must turn the comparison non-empty
# --------------------------------------------------------------------------- #
#: Two tests write one shared path after a cross-process barrier and read it back after a
#: second barrier. Serial: each test writes then reads its own value — both pass. Parallel:
#: both writes precede both reads, so exactly one test reads the other's value and fails.
#: The barrier yields immediately when no xdist worker owns the process (the serial arm).
DRILL_SUITE = (
    "import os\n"
    "import time\n"
    "from pathlib import Path\n"
    "\n"
    "READY = Path(os.environ['DRILL_READY'])\n"
    "SHARED = Path(os.environ['DRILL_SHARED'])\n"
    "READY.mkdir(parents=True, exist_ok=True)\n"
    "\n"
    "\n"
    "def _signal(phase, name):\n"
    "    (READY / f'{phase}.{name}').write_text('1', encoding='utf-8')\n"
    "\n"
    "\n"
    "def _await_peers(phase, name, timeout=30.0):\n"
    "    if not os.environ.get('PYTEST_XDIST_WORKER'):\n"
    "        return\n"
    "    peer = 'beta' if name == 'alpha' else 'alpha'\n"
    "    deadline = time.monotonic() + timeout\n"
    "    while not all((READY / f'{phase}.{who}').exists() for who in (name, peer)):\n"
    "        if time.monotonic() >= deadline:\n"
    "            raise AssertionError(f'barrier {phase} timed out waiting for {peer}')\n"
    "        time.sleep(0.01)\n"
    "\n"
    "\n"
    "def _race(name):\n"
    "    _signal('intent', name)\n"
    "    _await_peers('intent', name)\n"
    "    SHARED.write_text(name, encoding='utf-8')\n"
    "    _signal('posted', name)\n"
    "    _await_peers('posted', name)\n"
    "    seen = SHARED.read_text(encoding='utf-8')\n"
    "    assert seen == name, f'{name} observed another test write: {seen!r}'\n"
    "\n"
    "\n"
    "def test_alpha():\n"
    "    _race('alpha')\n"
    "\n"
    "\n"
    "def test_beta():\n"
    "    _race('beta')\n"
)


def _write_drill_tree(root: Path) -> Path:
    """A throwaway tree registering the markers the runner's expressions name."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "pytest.ini").write_text(
        "[pytest]\nmarkers =\n"
        "    serial: not parallel-safe\n"
        "    slow: slow tier\n"
        "    contract: selection marker\n",
        encoding="utf-8",
    )
    (root / "test_drill.py").write_text(DRILL_SUITE, encoding="utf-8")
    return root


@MARK_CONTRACT
def test_non_parallel_safe_fixture_turns_the_comparison_non_empty(tmp_path):
    tree = _write_drill_tree(tmp_path / "tree")
    parallel_names = tmp_path / "parallel-names.txt"
    serial_names = tmp_path / "serial-names.txt"

    parallel = _run(
        ["--workers", "2", "--names-out", parallel_names, str(tree), "-q"],
        cwd=tmp_path,
        env_extra={
            "DRILL_READY": str(tmp_path / "ready-parallel"),
            "DRILL_SHARED": str(tmp_path / "shared-parallel.txt"),
        },
    )
    assert parallel.returncode == 1, parallel.stdout + parallel.stderr
    mode, rest = _mode(parallel.stderr)
    assert mode == "parallel", parallel.stderr
    assert _field(rest, "workers") == "2", rest

    serial = _run(
        ["--serial", "--names-out", serial_names, str(tree), "-q"],
        cwd=tmp_path,
        env_extra={
            "DRILL_READY": str(tmp_path / "ready-serial"),
            "DRILL_SHARED": str(tmp_path / "shared-serial.txt"),
        },
    )
    assert serial.returncode == 0, serial.stdout + serial.stderr
    mode, _ = _mode(serial.stderr)
    assert mode == "serial", serial.stderr

    parallel_failed = [
        ln.strip() for ln in parallel_names.read_text(encoding="utf-8").splitlines() if ln.strip()
    ]
    serial_failed = [
        ln.strip() for ln in serial_names.read_text(encoding="utf-8").splitlines() if ln.strip()
    ]
    # The barrier construction makes exactly one parallel test read the other's write; a
    # serial run cannot observe a peer, so its list stays empty. The comparison therefore
    # MUST be non-empty — otherwise this drill proves the comparison is a green label.
    assert len(parallel_failed) == 1, (
        f"the drill's parallel arm must show exactly one name; got {parallel_failed}"
    )
    assert serial_failed == [], f"the drill's serial arm must be clean; got {serial_failed}"
    only_parallel = [name for name in parallel_failed if name not in set(serial_failed)]
    assert only_parallel, (
        "the parallel-vs-serial name comparison came out empty on a non-parallel-safe "
        "fixture; the comparison is not a discriminator (C-009)"
    )
