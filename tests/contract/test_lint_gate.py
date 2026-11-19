"""Contract: the local lint gate locks the subprocess shell posture.

Adapted-from: 24d76b5d9 ("Add pytest and Python linting (ruff) to CI") and 8e76ff3d5
("harden: reject shell=True in run_command"), whose `[tool.ruff.lint]` extend-select is the
lock this port localises. Upstream runs the gate as a GitHub Actions workflow; this fork tracks
no `.github/workflows` (its remotes are intranet GitLab/Gitee), so the gate is a local command
and these cases guard its configuration and its verdicts instead of a workflow file. Upstream's
workflow linted `src/`; the equivalent shipped surface here is `src scripts skills`. The suite is
not a lint subject: its regression cases seed `shell=True` calls as negative samples, which are
the subject of a guard rather than a defect the gate should report.

Three subjects, because none alone proves a gate: the enabled rule set is exactly the
shell-execution trio (an inherited default set is not a lock), ruff stays dev-only tooling
outside the shipping dependency boundary, and the gate both passes on the shipped surface and
goes red on a seeded `shell=True`. The ruff cases need the binary; without it they report
themselves as skipped, never as passed.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PYPROJECT = REPO_ROOT / "pyproject.toml"

pytestmark = pytest.mark.contract

#: The gate's scope, pinned here as the test's own literal: the shipped Python surface — the CLI
#: package plus the two payload roots that carry `.py` files into the wheel. The suite is out of
#: scope by design: regression cases seed `shell=True` calls as negative samples (data, not defects).
GATE_PATHS = ("src", "scripts", "skills")
#: The shell-execution trio upstream locked; a reintroduced `shell=True` must be visible in review.
SHELL_RULES = {"S602", "S604", "S605"}
#: One seed per rule: a subprocess call, any call carrying `shell=True`, and a shell start.
#: This is lint *input data* — written to a throwaway file and read by ruff, never imported or
#: executed by the suite, so the unsafe forms below are the subject of the check, not its behaviour.
SEED = (
    "import os\n"
    "import subprocess\n"
    "\n"
    "def launch(cmd, shell=False):\n"
    "    pass\n"
    "\n"
    "subprocess.run('ls', shell=True)\n"
    "launch('ls', shell=True)\n"
    "os.system('ls')\n"
)

needs_ruff = pytest.mark.skipif(shutil.which("ruff") is None, reason="ruff binary not installed")


def _section(name: str) -> str:
    """One TOML table's body, read without a TOML engine so the case runs on every supported Python.

    The header is matched at the start of its own line: a prose comment may name the same table
    (the dev-group comment points at `[tool.ruff]`), and that mention is not the table.
    """
    text = PYPROJECT.read_text(encoding="utf-8")
    header = re.search(r"^\[%s\][ \t]*$" % re.escape(name), text, re.M)
    assert header, "pyproject.toml carries no [%s] table" % name
    rest = text[header.end():]
    nxt = re.search(r"^\[", rest, re.M)
    return rest[:nxt.start()] if nxt else rest


def _list_body(section: str, key: str) -> str:
    match = re.search(r"%s\s*=\s*\[(.*?)\]" % re.escape(key), section, re.S)
    assert match, "the table carries no %s list" % key
    return match.group(1)


def _ruff(*args: str) -> subprocess.CompletedProcess:
    """Run the gate engine without writing a cache into the tree it reads."""
    return subprocess.run(
        ["ruff", "check", "--no-cache", "--output-format", "concise", *args],
        cwd=str(REPO_ROOT), capture_output=True, text=True,
    )


def test_the_gate_selects_exactly_the_shell_execution_rules():
    """The enabled set is pinned by `select`, so ruff's defaults cannot widen or move it silently."""
    lint = _section("tool.ruff.lint")
    assert re.search(r"^select\s*=", lint, re.M), (
        "the gate must pin its own rule set with `select`; `extend-select` alone inherits "
        "ruff's defaults, which are a moving set and carry this tree's existing lint debt"
    )
    codes = set(re.findall(r'"([A-Z]+\d+)"', _list_body(lint, "select")))
    assert codes == SHELL_RULES, (
        "the local lint gate enables exactly the shell-execution trio %r; got %r"
        % (sorted(SHELL_RULES), sorted(codes))
    )


def test_the_gate_targets_the_oldest_python_the_package_supports():
    """`target-version` is derived from `requires-python`, not a second independent guess."""
    floor = re.search(r'requires-python\s*=\s*">=3\.(\d+)"', _section("project"))
    assert floor, "pyproject.toml declares no >=3.x requires-python floor"
    expected = "py3%s" % floor.group(1)
    target = re.search(r'target-version\s*=\s*"([^"]+)"', _section("tool.ruff"))
    assert target, "the [tool.ruff] table declares no target-version"
    assert target.group(1) == expected, (
        "the lint gate must target the package's oldest supported Python (%s); got %s"
        % (expected, target.group(1))
    )


def test_ruff_is_dev_only_tooling():
    """The lint engine never crosses the shipping boundary: dev group yes, runtime dependencies no."""
    runtime = _list_body(_section("project"), "dependencies")
    dev = _list_body(_section("project.optional-dependencies"), "dev")
    assert "ruff" not in runtime, "ruff must not become a runtime dependency of the CLI"
    assert re.search(r'"ruff(?:[<>=!~;\[]|")', dev), (
        "the sanctioned dev group must carry the gate engine; got %r" % (dev,)
    )


@needs_ruff
def test_the_gate_passes_on_the_shipped_surface():
    proc = _ruff(*GATE_PATHS)
    assert proc.returncode == 0, (
        "the local lint gate is red (rc=%s):\n%s%s" % (proc.returncode, proc.stdout, proc.stderr)
    )


@needs_ruff
def test_the_gate_turns_red_on_a_seeded_shell_true(tmp_path):
    """A green check is a claim, not evidence: the landed config must report all three seeded rules."""
    seed = tmp_path / "seeded_shell_true.py"
    seed.write_text(SEED, encoding="utf-8")
    proc = _ruff("--config", str(PYPROJECT), str(seed))
    assert proc.returncode != 0, (
        "the gate passed a file that starts processes with a shell; the config enables nothing:\n%s"
        % (proc.stdout,)
    )
    reported = set(re.findall(r"\b(S\d+)\b", proc.stdout))
    assert SHELL_RULES <= reported, (
        "every locked rule must fire on its own seed; reported %r\n%s"
        % (sorted(reported), proc.stdout)
    )