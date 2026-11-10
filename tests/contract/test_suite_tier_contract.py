"""Contract cases for the runner's tier selection (098, tier-selection § E obligations 1–10).

Owner of the propositions: `.specify/specs/098-suite-speed-optimizations/contracts/
tier-selection.contract.md` (§ A–C clauses C-001…C-011, carried here as obligations 1–10).
WP-2 appends the slow-membership guard cases (slow-membership C-005…C-009) to this file;
nothing here covers them, and obligation 11 (full-collection equality) lands with WP-3.

Construction constraints:

- Every case runs on a throwaway fixture tree whose ``pytest.ini`` registers the
  ``serial``, ``slow`` and ``contract`` markers, so an unknown-mark warning can never be
  mistaken for a tier decision.
- The runner is invoked from a clean environment (no inherited ``PYTEST_XDIST_WORKER``,
  no ``PYTHONPATH``, no ``SPECKIT_TEST_WORKERS``) so a nested run never replaces the
  branch under test.
- ``--workers 2`` is passed explicitly wherever parallelism matters, so the cases do not
  depend on the host's CPU count.
- No case asserts a wall-clock threshold (contract § E preamble).
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

MODE_LINE = re.compile(r"^# test runner: mode=(?P<mode>\w+)(?P<rest>.*)$", re.M)
EMPTY_ERROR = "# test runner: error=empty-selection-after-tier-exclusion"

PLAIN_OK = "def test_plain_ok():\n    assert True\n"
SLOW_FAIL = (
    "import pytest\n\n"
    "@pytest.mark.slow\n"
    "def test_slow_fails():\n    assert False\n"
)

CONTRACT_TREE = {
    "test_selection.py": (
        "import pytest\n\n"
        "def test_unmarked_ok():\n    assert True\n\n"
        "@pytest.mark.contract\n"
        "def test_contract_ok():\n    assert True\n\n"
        "@pytest.mark.contract\n"
        "@pytest.mark.slow\n"
        "def test_contract_slow_fails():\n    assert False\n"
    )
}

INTERSECTION_TREE = {
    "test_intersection.py": (
        "import pytest\n\n"
        "def test_plain_ok():\n    assert True\n\n"
        "@pytest.mark.serial\n"
        "def test_serial_only_ok():\n    assert True\n\n"
        "@pytest.mark.slow\n"
        "def test_slow_only_fails():\n    assert False\n\n"
        "@pytest.mark.serial\n"
        "@pytest.mark.slow\n"
        "def test_serial_slow_fails():\n    assert False\n"
    )
}


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _python() -> str:
    """The interpreter the runner will resolve: keep the test independent of CWD."""
    return os.environ.get("SPECKIT_PYTHON") or sys.executable


def _write_tree(root: Path, files: dict) -> Path:
    """A throwaway fixture tree registering the three markers its cases rely on."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "pytest.ini").write_text(
        "[pytest]\nmarkers =\n"
        "    serial: not parallel-safe\n"
        "    slow: slow tier\n"
        "    contract: selection marker\n",
        encoding="utf-8",
    )
    for name, body in files.items():
        (root / name).write_text(body, encoding="utf-8")
    return root


def _run(args, *, cwd=None, env_extra=None):
    """Invoke the runner from a clean environment (see module docstring constraints)."""
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
    """Return ``(mode, rest)`` of the first mode line, or fail with the real stderr."""
    match = MODE_LINE.search(stderr)
    assert match is not None, f"no mode line on stderr:\n{stderr}"
    return match.group("mode"), match.group("rest").strip()


def _field(rest: str, name: str) -> str:
    """One ``name=value`` field from the mode line's tail."""
    match = re.search(rf"\b{name}=(\S+)", rest)
    assert match is not None, f"mode line carries no {name}= field: {rest!r}"
    return match.group(1)


def _command_lines(stderr: str):
    return [
        ln for ln in stderr.splitlines()
        if ln.startswith("# test runner: ") and "mode=" not in ln
    ]


def _collected(done):
    return {ln.strip() for ln in done.stdout.splitlines() if "::" in ln}


def _names(path: Path):
    return [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]


def _m_tokens(line: str):
    """Marker-expression tokens after the ``python -m pytest`` command word (the
    interpreter's own ``-m`` is not a marker option)."""
    tokens = line.split()
    if "pytest" in tokens:
        tokens = tokens[tokens.index("pytest") + 1:]
    return [t for t in tokens if t == "-m" or t.startswith("-m=")]


# --------------------------------------------------------------------------- #
# Obligation 1 — default tier: the slow test is excluded and disclosed
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_obligation_1_default_tier_excludes_the_slow_test(tmp_path):
    root = _write_tree(tmp_path / "tree", {"test_mixed.py": PLAIN_OK + "\n" + SLOW_FAIL})

    default = _run(["--workers", "2", str(root), "-q"], cwd=tmp_path)
    assert default.returncode == 0, default.stdout + default.stderr
    mode, rest = _mode(default.stderr)
    assert mode == "parallel", default.stderr
    assert _field(rest, "tier") == "fast", rest
    assert _field(rest, "excluded_slow") == "1", rest
    assert "1 passed" in default.stdout, default.stdout
    assert "failed" not in default.stdout, default.stdout

    full = _run(["--workers", "2", "--full", str(root), "-q"], cwd=tmp_path)
    assert full.returncode == 1, full.stdout + full.stderr
    mode, rest = _mode(full.stderr)
    assert _field(rest, "tier") == "full", rest
    assert _field(rest, "excluded_slow") == "0", rest
    assert "1 failed" in full.stdout, full.stdout


# --------------------------------------------------------------------------- #
# Obligation 2 — a tree without slow tests: selection equals the full selection
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_obligation_2_a_tree_without_slow_tests_equals_the_full_selection(tmp_path):
    root = _write_tree(tmp_path / "tree", {"test_plain.py": (
        "def test_a():\n    assert True\n\n"
        "def test_b():\n    assert True\n\n"
        "def test_c():\n    assert True\n"
    )})

    default = _run(["--workers", "2", "--collect-only", "-q", str(root)], cwd=tmp_path)
    full = _run(["--workers", "2", "--full", "--collect-only", "-q", str(root)], cwd=tmp_path)
    assert default.returncode == 0, default.stdout + default.stderr
    assert full.returncode == 0, full.stdout + full.stderr
    assert len(_collected(default)) == 3, default.stdout
    assert _collected(default) == _collected(full), (default.stdout, full.stdout)
    mode, rest = _mode(default.stderr)
    assert _field(rest, "tier") == "fast" and _field(rest, "excluded_slow") == "0", rest
    _, rest_full = _mode(full.stderr)
    assert _field(rest_full, "tier") == "full", rest_full


# --------------------------------------------------------------------------- #
# Obligation 3 — a caller -m owns the selection in both spellings
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
@pytest.mark.parametrize("expr_args", [["-m", "contract"], ["-m=contract"]])
def test_obligation_3_the_caller_m_owns_the_selection(tmp_path, expr_args):
    root = _write_tree(tmp_path / "tree", CONTRACT_TREE)
    done = _run(["--workers", "2", *expr_args, str(root), "-q"], cwd=tmp_path)
    # The caller's expression selects the slow-marked contract test too; it fails, so a
    # merged default exclusion (which would have kept it out and the run green) is caught.
    assert done.returncode == 1, done.stdout + done.stderr
    mode, rest = _mode(done.stderr)
    assert _field(rest, "tier") == "caller", rest
    assert _field(rest, "excluded_slow") == "0", rest
    assert "1 passed" in done.stdout and "1 failed" in done.stdout, done.stdout
    header = _command_lines(done.stderr)
    assert len(header) == 1, done.stderr
    assert len(_m_tokens(header[0])) == 1, f"a second -m was emitted: {header[0]}"


# --------------------------------------------------------------------------- #
# Obligation 4 — paths and -k narrow inside the tier, they never suppress it
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_obligation_4_path_and_k_do_not_suppress_the_tier(tmp_path):
    root = _write_tree(tmp_path / "tree", {
        "test_alpha.py": PLAIN_OK + "\n" + SLOW_FAIL,
        "test_beta.py": "def test_beta_plain():\n    assert True\n",
    })

    by_path = _run(["--workers", "2", str(root / "test_alpha.py"), "-q"], cwd=tmp_path)
    assert by_path.returncode == 0, by_path.stdout + by_path.stderr
    _, rest = _mode(by_path.stderr)
    assert _field(rest, "tier") == "fast", rest
    assert _field(rest, "excluded_slow") == "1", rest
    assert "1 passed" in by_path.stdout, by_path.stdout
    assert "failed" not in by_path.stdout, by_path.stdout

    by_k = _run(["--workers", "2", str(root), "-k", "beta", "-q"], cwd=tmp_path)
    assert by_k.returncode == 0, by_k.stdout + by_k.stderr
    _, rest = _mode(by_k.stderr)
    assert _field(rest, "tier") == "fast", rest
    # the slow test is outside the -k selection, so the disclosed count is 0 — the count
    # follows the caller's selection, never a hardcoded tree total
    assert _field(rest, "excluded_slow") == "0", rest
    assert "1 passed" in by_k.stdout, by_k.stdout


# --------------------------------------------------------------------------- #
# Obligation 5 — --full together with a caller -m: tier=caller, no exclusion
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_obligation_5_full_with_a_caller_m_is_still_the_callers_selection(tmp_path):
    root = _write_tree(tmp_path / "tree", CONTRACT_TREE)
    done = _run(["--workers", "2", "--full", "-m", "contract", str(root), "-q"], cwd=tmp_path)
    assert done.returncode == 1, done.stdout + done.stderr
    _, rest = _mode(done.stderr)
    assert _field(rest, "tier") == "caller", rest
    assert _field(rest, "excluded_slow") == "0", rest
    assert "1 passed" in done.stdout and "1 failed" in done.stdout, done.stdout
    header = _command_lines(done.stderr)
    assert len(header) == 1 and len(_m_tokens(header[0])) == 1, done.stderr


# --------------------------------------------------------------------------- #
# Obligation 6 — --serial is orthogonal to the tier: one pass, injected expression
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_obligation_6_serial_mode_never_selects_a_tier(tmp_path):
    mixed = _write_tree(tmp_path / "mixed", {"test_mixed.py": PLAIN_OK + "\n" + SLOW_FAIL})

    fast = _run(["--serial", str(mixed), "-q"], cwd=tmp_path)
    assert fast.returncode == 0, fast.stdout + fast.stderr
    mode, rest = _mode(fast.stderr)
    assert mode == "serial", fast.stderr
    assert _field(rest, "tier") == "fast", rest
    assert _field(rest, "excluded_slow") == "1", rest
    header = _command_lines(fast.stderr)
    assert len(header) == 1, fast.stderr
    assert "-n0" in header[0] and '-m "not slow"' in header[0], header[0]
    assert "# test runner exceptions:" not in fast.stderr, fast.stderr

    full = _run(["--serial", "--full", str(mixed), "-q"], cwd=tmp_path)
    assert full.returncode == 1, full.stdout + full.stderr
    _, rest = _mode(full.stderr)
    assert _field(rest, "tier") == "full", rest
    assert _field(rest, "excluded_slow") == "0", rest
    header = _command_lines(full.stderr)
    assert len(header) == 1 and "-n0" in header[0], full.stderr
    assert _m_tokens(header[0]) == [], header[0]

    contract = _write_tree(tmp_path / "contract", CONTRACT_TREE)
    caller = _run(["--serial", "-m", "contract", str(contract), "-q"], cwd=tmp_path)
    assert caller.returncode == 1, caller.stdout + caller.stderr
    _, rest = _mode(caller.stderr)
    assert _field(rest, "tier") == "caller", rest
    assert _field(rest, "excluded_slow") == "0", rest
    header = _command_lines(caller.stderr)
    assert len(header) == 1 and "-n0" in header[0].split(), caller.stderr
    assert len(_m_tokens(header[0])) == 1, header[0]


# --------------------------------------------------------------------------- #
# Obligation 7 — one test marked both serial and slow
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_obligation_7_a_serial_and_slow_test_is_excluded_from_both_fast_passes(tmp_path):
    root = _write_tree(tmp_path / "tree", INTERSECTION_TREE)

    default = _run(["--workers", "2", str(root), "-q"], cwd=tmp_path)
    assert default.returncode == 0, default.stdout + default.stderr
    _, rest = _mode(default.stderr)
    assert _field(rest, "tier") == "fast", rest
    assert _field(rest, "excluded_slow") == "2", rest
    # one passing test per pass (plain in the parallel pass, serial-only in the serial
    # pass): the intersection member is in neither fast pass
    assert default.stdout.count("1 passed") == 2, default.stdout
    assert "failed" not in default.stdout, default.stdout
    assert "declared serial test(s)" in default.stderr, default.stderr

    names = tmp_path / "names.txt"
    full = _run(["--serial", "--full", "--names-out", names, str(root), "-q"], cwd=tmp_path)
    assert full.returncode == 1, full.stdout + full.stderr
    assert sorted(n.rsplit("::", 1)[-1] for n in _names(names)) == [
        "test_serial_slow_fails",
        "test_slow_only_fails",
    ], _names(names)


# --------------------------------------------------------------------------- #
# Obligation 8 — empty-after-exclusion is a named error; exit 5 keeps its meaning
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_obligation_8_empty_after_exclusion_is_a_named_error(tmp_path):
    all_slow = _write_tree(tmp_path / "all_slow", {"test_all_slow.py": (
        "import pytest\n\n"
        "@pytest.mark.slow\n"
        "def test_a():\n    assert True\n\n"
        "@pytest.mark.slow\n"
        "def test_b():\n    assert True\n"
    )})
    done = _run(["--workers", "2", str(all_slow), "-q"], cwd=tmp_path)
    assert done.returncode == 2, done.stdout + done.stderr
    assert f"{EMPTY_ERROR} tier=fast excluded_slow=2" in done.stderr, done.stderr
    assert "passed" not in done.stdout, done.stdout

    two_pass = _write_tree(tmp_path / "two_pass", {"test_two.py": (
        "import pytest\n\n"
        "@pytest.mark.serial\n"
        "def test_serial_ok():\n    assert True\n\n"
        "@pytest.mark.slow\n"
        "def test_slow_ok():\n    assert True\n"
    )})
    module = two_pass / "test_two.py"
    kept = _run(
        [
            "--workers", "2",
            f"{module}::test_serial_ok", f"{module}::test_slow_ok",
            "-q",
        ],
        cwd=tmp_path,
    )
    # the parallel pass collects nothing, the serial pass runs the marked test: 086 C-012's
    # exit 5, not the tier error
    assert kept.returncode == 5, kept.stdout + kept.stderr
    assert "empty-selection-after-tier-exclusion" not in kept.stderr, kept.stderr

    green = _write_tree(tmp_path / "green", {"test_plain.py": PLAIN_OK})
    empty = _run(["--full", "-k", "definitely_no_match", str(green), "-q"], cwd=tmp_path)
    assert empty.returncode == 5, empty.stdout + empty.stderr
    assert "empty-selection-after-tier-exclusion" not in empty.stderr, empty.stderr


# --------------------------------------------------------------------------- #
# Obligation 9 — --help lists --full; an undeclared option still exits non-zero
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_obligation_9_help_lists_full_and_an_undeclared_option_still_exits_non_zero(tmp_path):
    helped = _run(["--help"], cwd=tmp_path)
    assert helped.returncode == 0, helped.stdout + helped.stderr
    assert "--full" in helped.stdout, helped.stdout

    refused = _run(["--definitely-undeclared"], cwd=tmp_path)
    assert refused.returncode != 0, refused.stdout + refused.stderr


# --------------------------------------------------------------------------- #
# Obligation 10 — the header carries the injected expression when one is applied
# --------------------------------------------------------------------------- #
@MARK_CONTRACT
def test_obligation_10_the_header_carries_the_injected_expression(tmp_path):
    plain = _write_tree(tmp_path / "plain", {"test_plain.py": PLAIN_OK + "\n" + SLOW_FAIL})
    one_pass = _run(["--workers", "2", str(plain), "-q"], cwd=tmp_path)
    assert one_pass.returncode == 0, one_pass.stdout + one_pass.stderr
    header = _command_lines(one_pass.stderr)
    assert len(header) == 1, one_pass.stderr
    assert '-m "not slow"' in header[0], header[0]

    mixed = _write_tree(tmp_path / "mixed", {"test_mixed.py": (
        "import pytest\n\n"
        "def test_plain_ok():\n    assert True\n\n"
        "@pytest.mark.serial\n"
        "def test_serial_ok():\n    assert True\n\n"
        "@pytest.mark.slow\n"
        "def test_slow_fails():\n    assert False\n"
    )})
    two_pass = _run(["--workers", "2", str(mixed), "-q"], cwd=tmp_path)
    assert two_pass.returncode == 0, two_pass.stdout + two_pass.stderr
    header = _command_lines(two_pass.stderr)
    assert len(header) == 1, two_pass.stderr
    assert '-m "not serial and not slow"' in header[0], header[0]

    full = _run(["--workers", "2", "--full", str(plain), "-q"], cwd=tmp_path)
    assert full.returncode == 1, full.stdout + full.stderr
    header = _command_lines(full.stderr)
    assert len(header) == 1, full.stderr
    assert _m_tokens(header[0]) == [], header[0]
