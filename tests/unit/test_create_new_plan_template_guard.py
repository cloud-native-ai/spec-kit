"""P1 Agent B — a missing or empty plan template is a failure, not a warning.

Ported fix shape: upstream 3238fa928 ("[bug-fix] Fix missing-plan-template: reject
empty plan setup", #4962). Upstream fixed setup-plan.sh; this fork's twins are
create-new-plan.sh and implement-plan.sh, both of which carried the same defect:

    echo "Warning: Plan template not found at $TEMPLATE"
    touch "$IMPL_PLAN"

Measured before the port: with no template present, create-new-plan.sh exited 0 and
left a zero-byte plan.md. Every downstream gate then read that empty file as a real
plan — check-prerequisites.sh tests only ``-f``, so MODE became B and /speckit.implement
proceeded against nothing. The empty file is the pollution; refusing to create it is
the fix, so both failure paths leave the tree exactly as they found it.

The read-side companion of that upstream commit (rejecting an already-empty plan.md in
check-prerequisites.sh) is deliberately NOT ported here: this fork's contract case
tests/contract/test_specify_script_paths.py::test_review_prerequisite_flags_are_supported
tolerates a non-zero exit only when stderr matches ``(plan|tasks)\\.md not found``, so a
new "is empty" rejection would turn that case red whenever the resolved feature happens
to own an empty plan — re-binding a flag-acceptance test to repo state, which its own
docstring rules out. Removing the source of empty plans is the root-cause half.

Master's key names and the requirements.md artifact name are preserved throughout.
"""
from __future__ import annotations

import json

import pytest

from tests.unit.bash_hardening_sandbox import (
    make_repo,
    needs_host_lib,
    plan_template,
    run_script,
    shell,  # noqa: F401  — pytest fixture, imported into this module's namespace
    spec_dir,
)

pytestmark = needs_host_lib

TEMPLATE_TEXT = "# Implementation Plan\n\n**Branch**: 001-demo\n\nreal content\n"
SCAFFOLDERS = ["create-new-plan.sh", "implement-plan.sh"]


def _feature(proj):
    spec_dir(proj, "001-demo")
    (proj / ".specify" / "specs" / "001-demo" / "requirements.md").write_text(
        "**Feature ID**: 001\n**Feature Name**: demo\n", encoding="utf-8"
    )


def _plan_path(proj):
    return proj / ".specify" / "specs" / "001-demo" / "plan.md"


@pytest.mark.parametrize("script", SCAFFOLDERS)
def test_missing_template_exits_1_and_creates_no_plan(tmp_path, shell, script):
    proj = make_repo(tmp_path)
    _feature(proj)
    plan_template(proj, None)
    proc = run_script(proj, script, "--json", overlay=shell, SPECIFY_FEATURE="001-demo")
    assert proc.returncode == 1, f"{script} accepted a missing template: {proc.stdout!r}"
    assert not _plan_path(proj).exists(), f"{script} created a plan.md with no template"
    assert "Plan template not found" in proc.stderr
    assert "no new plan.md was created" in proc.stderr
    assert proc.stdout.strip() == "", "a failure path must not emit a success payload"


@pytest.mark.parametrize("script", SCAFFOLDERS)
def test_empty_template_exits_1_and_creates_no_plan(tmp_path, shell, script):
    proj = make_repo(tmp_path)
    _feature(proj)
    plan_template(proj, "")
    proc = run_script(proj, script, "--json", overlay=shell, SPECIFY_FEATURE="001-demo")
    assert proc.returncode == 1, f"{script} accepted an empty template: {proc.stdout!r}"
    assert not _plan_path(proj).exists(), f"{script} created an empty plan.md"
    assert "Plan template is empty" in proc.stderr
    assert "no new plan.md was created" in proc.stderr


@pytest.mark.parametrize("script", SCAFFOLDERS)
def test_failure_leaves_an_existing_plan_untouched(tmp_path, shell, script):
    """--force plus a broken template must not truncate the plan it was asked to write."""
    proj = make_repo(tmp_path)
    _feature(proj)
    _plan_path(proj).write_text("# finished plan\n", encoding="utf-8")
    plan_template(proj, "")
    args = ["--json", "--force"] if script == "create-new-plan.sh" else ["--json"]
    proc = run_script(proj, script, *args, overlay=shell, SPECIFY_FEATURE="001-demo")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert _plan_path(proj).read_text(encoding="utf-8") == "# finished plan\n"


def test_valid_template_copies_and_stdout_is_pure_json(tmp_path, shell):
    proj = make_repo(tmp_path)
    _feature(proj)
    tpl = plan_template(proj, TEMPLATE_TEXT)
    proc = run_script(proj, "create-new-plan.sh", "--json", overlay=shell,
                      SPECIFY_FEATURE="001-demo")
    assert proc.returncode == 0, proc.stderr
    assert _plan_path(proj).read_bytes() == tpl.read_bytes()
    assert len(proc.stdout.splitlines()) == 1, f"stdout is not pure JSON: {proc.stdout!r}"
    doc = json.loads(proc.stdout)
    assert doc["IMPL_PLAN"] == str(_plan_path(proj))
    assert doc["FEATURE_SPEC"].endswith("/requirements.md")
    assert doc["SPECS_DIR"] == str(proj / ".specify" / "specs" / "001-demo")
    assert doc["BRANCH"] == "001-demo"
    assert doc["HAS_GIT"] == "true"
    assert "Copied plan template" in proc.stderr, "the status line belongs on stderr in JSON mode"


def test_text_mode_keeps_the_copy_message_on_stdout(tmp_path, shell):
    """Master's text-mode contract is unchanged: the message stays on stdout."""
    proj = make_repo(tmp_path)
    _feature(proj)
    plan_template(proj, TEMPLATE_TEXT)
    proc = run_script(proj, "create-new-plan.sh", overlay=shell, SPECIFY_FEATURE="001-demo")
    assert proc.returncode == 0, proc.stderr
    assert "Copied plan template" in proc.stdout
    assert "IMPL_PLAN: " in proc.stdout
    assert "SPECS_DIR: " in proc.stdout


def test_existing_plan_is_not_clobbered_without_force(tmp_path, shell):
    proj = make_repo(tmp_path)
    _feature(proj)
    plan_template(proj, TEMPLATE_TEXT)
    _plan_path(proj).write_text("# finished plan\n", encoding="utf-8")
    proc = run_script(proj, "create-new-plan.sh", "--json", overlay=shell,
                      SPECIFY_FEATURE="001-demo")
    assert proc.returncode == 1
    assert "already exists" in proc.stderr
    assert _plan_path(proj).read_text(encoding="utf-8") == "# finished plan\n"


def test_force_overwrites_an_existing_plan(tmp_path, shell):
    proj = make_repo(tmp_path)
    _feature(proj)
    tpl = plan_template(proj, TEMPLATE_TEXT)
    _plan_path(proj).write_text("# stale plan\n", encoding="utf-8")
    proc = run_script(proj, "create-new-plan.sh", "--json", "--force", overlay=shell,
                      SPECIFY_FEATURE="001-demo")
    assert proc.returncode == 0, proc.stderr
    assert _plan_path(proj).read_bytes() == tpl.read_bytes()


def test_implement_plan_runs_the_workflow_once(tmp_path, shell):
    """An unconditional `main "$@"` above the source guard ran everything twice."""
    proj = make_repo(tmp_path)
    _feature(proj)
    plan_template(proj, TEMPLATE_TEXT)
    proc = run_script(proj, "implement-plan.sh", "--json", overlay=shell,
                      SPECIFY_FEATURE="001-demo")
    assert proc.returncode == 0, proc.stderr
    assert len(proc.stdout.splitlines()) == 1, (
        f"two JSON documents on stdout means main ran twice: {proc.stdout!r}"
    )
    assert proc.stderr.count("Executing /speckit.plan workflow") == 1
    assert proc.stderr.count("Starting Phase 0: Research") == 1
    assert proc.stderr.count("Phase 1: Design & Contracts completed") == 1
    json.loads(proc.stdout)


@pytest.mark.parametrize("script", SCAFFOLDERS)
def test_help_with_a_write_flag_writes_nothing(tmp_path, shell, script):
    """The flag scan still outranks every write after the guard changes."""
    proj = make_repo(tmp_path)
    _feature(proj)
    plan_template(proj, TEMPLATE_TEXT)
    args = ["--help", "--force"] if script == "create-new-plan.sh" else ["--help", "--input", "x"]
    proc = run_script(proj, script, *args, overlay=shell, SPECIFY_FEATURE="001-demo")
    assert proc.returncode == 0, proc.stderr
    assert not _plan_path(proj).exists(), f"{script} wrote on a --help invocation"


def test_empty_plan_already_on_disk_is_not_silently_re_scaffolded(tmp_path, shell):
    """The guard is about creation: an existing plan is never overwritten by accident."""
    proj = make_repo(tmp_path)
    _feature(proj)
    plan_template(proj, TEMPLATE_TEXT)
    _plan_path(proj).write_text("", encoding="utf-8")
    proc = run_script(proj, "create-new-plan.sh", "--json", overlay=shell,
                      SPECIFY_FEATURE="001-demo")
    assert proc.returncode == 1
    assert "already exists" in proc.stderr
    assert _plan_path(proj).read_text(encoding="utf-8") == ""