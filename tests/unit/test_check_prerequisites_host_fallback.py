"""Regression: check-prerequisites keeps its --json path without the host shell library.

Backlog F1 (2026-11-23): when ``CWS_LIB_BASH_HOME`` is unset, ``common.sh``'s
library-link publishes no host helpers, and ``check-prerequisites.sh --json`` lost
``json_escape`` / ``is_git_repo`` — 17 occurrences reported. The scaffold path already
carries its own escaper; this test pins the same no-host guarantee for the
prerequisite JSON surface. The fallback is consumer-local and only takes effect when
the host did not publish the helper, so the host library stays the owner when present.

Red-first: the test copies the current ``scripts/bash`` tree into a sandbox project and
runs with ``CWS_LIB_BASH_HOME`` empty; before the fallback it fails with a missing
helper (or non-JSON output), not with a wrong assertion.
"""
from __future__ import annotations

import json

import pytest

from tests.unit.bash_hardening_sandbox import (
    make_repo,
    run_script,
    shell,  # noqa: F401  — pytest fixture
    spec_dir,
)

pytestmark = pytest.mark.unit

NASTY = 'Evil "Name" \\ backslash'


def _write_requirements(proj) -> None:
    d = spec_dir(proj, "001-demo")
    (d / "requirements.md").write_text(
        "**Feature ID**: 001\n**Feature Name**: %s\n" % NASTY, encoding="utf-8"
    )
    # The default --json path validates plan.md before it renders; the paths-only
    # variant does not. MODE is therefore B (plan present, tasks absent).
    (d / "plan.md").write_text("# Plan\n\nMinimal fixture.\n", encoding="utf-8")


def test_json_round_trips_without_host_library(tmp_path, shell):
    proj = make_repo(tmp_path)
    _write_requirements(proj)
    proc = run_script(
        proj, "check-prerequisites.sh", "--json",
        overlay=shell, CWS_LIB_BASH_HOME="",
    )
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    doc = json.loads(proc.stdout)
    assert doc["REQUIREMENT_ID"] == "001"
    assert doc["FEATURE_ID"] == "001"
    assert doc["FEATURE_NAME"] == NASTY, (
        "the no-host json_escape fallback must round-trip quotes and backslashes"
    )
    assert doc["MODE"] == "B"


def test_paths_only_json_round_trips_without_host_library(tmp_path, shell):
    proj = make_repo(tmp_path)
    _write_requirements(proj)
    proc = run_script(
        proj, "check-prerequisites.sh", "--json", "--paths-only",
        overlay=shell, CWS_LIB_BASH_HOME="",
    )
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    doc = json.loads(proc.stdout)
    assert doc["REQUIREMENT_ID"] == "001"
    assert doc["FEATURE_NAME"] == NASTY
    assert doc["BRANCH"] == "001-demo"
