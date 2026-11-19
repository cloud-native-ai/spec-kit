"""P1 Agent B — shell-injection hardening of get_feature_paths and its eval callers.

Ported fix shape: upstream 46bc65b1cefc487e507aa7b809ce4e48b96ba4ec ("harden bash
scripts against shell injection and improve robustness", #1809). Two defects, both
measured on this fork before the port:

* ``get_feature_paths`` emitted ``KEY='value'`` lines from an unquoted heredoc and
  four callers ran ``eval $(get_feature_paths)``. A branch name carrying a single
  quote broke out of that quoting and the remainder ran as code — a marker file was
  created by a ``touch`` embedded in SPECIFY_FEATURE.
* ``find_feature_dir_by_prefix`` answered an ambiguous numeric prefix with a guessed
  fallback path and status 0, so a caller could not tell "resolved" from "guessed".

The key names are this fork's contract and are NOT upstream's: REQUIREMENTS_DIR (not
FEATURE_DIR) and FEATURE_SPEC pointing at requirements.md. Every case below pins that
contract, so a future sync cannot quietly rename it back.

Anti-vacuity: each injection case asserts BOTH that the payload did not execute and
that the payload survived verbatim as data. A resolver that returned nothing, or a
consumer that dropped the value, fails the second assertion.
"""
from __future__ import annotations

import json

import pytest

from tests.unit.bash_hardening_sandbox import (
    SAFE_EVAL,
    SOURCE_COMMON,
    make_repo,
    needs_host_lib,
    plan_template,
    run_script,
    run_snippet,
    shell,  # noqa: F401  — pytest fixture, imported into this module's namespace
    spec_dir,
)

pytestmark = needs_host_lib

#: The four callers that consume get_feature_paths through eval.
EVAL_CALLERS = [
    "check-prerequisites.sh",
    "create-new-plan.sh",
    "implement-plan.sh",
    "research-project.sh",
]

#: Every key get_feature_paths publishes, in this fork's naming.
MASTER_KEYS = [
    "REPO_ROOT",
    "CURRENT_BRANCH",
    "BRANCH_RESOLVED_FROM_SPEC_DIR",
    "REQUIREMENT_ID",
    "HAS_GIT",
    "REQUIREMENTS_DIR",
    "FEATURE_SPEC",
    "IMPL_PLAN",
    "TASKS",
    "RESEARCH",
    "DATA_MODEL",
    "QUICKSTART",
    "CONTRACTS_DIR",
]


def _paths(proj, shell, **extra):
    return run_snippet(proj, SOURCE_COMMON + SAFE_EVAL + 'printf "%s" "$REQUIREMENTS_DIR"',
                       overlay=shell, **extra)


def test_quote_breakout_payload_is_data_and_never_executes(tmp_path, shell):
    proj = make_repo(tmp_path)
    marker = tmp_path / "PWNED"
    payload = f"003-x';touch {marker};'"
    proc = _paths(proj, shell, SPECIFY_FEATURE=payload)
    assert proc.returncode == 0, proc.stderr
    assert not marker.exists(), f"payload executed: {proc.stdout!r} {proc.stderr!r}"
    assert proc.stdout == str(proj / ".specify" / "specs" / payload)


def test_command_substitution_payload_is_not_expanded(tmp_path, shell):
    proj = make_repo(tmp_path)
    marker = tmp_path / "PWNED_SUBST"
    payload = f"003-$(touch {marker})"
    proc = _paths(proj, shell, SPECIFY_FEATURE=payload)
    assert proc.returncode == 0, proc.stderr
    assert not marker.exists(), "command substitution in a branch name was expanded"
    assert proc.stdout == str(proj / ".specify" / "specs" / payload)


def test_backtick_payload_is_not_expanded(tmp_path, shell):
    proj = make_repo(tmp_path)
    marker = tmp_path / "PWNED_BACKTICK"
    payload = f"003-`touch {marker}`"
    proc = _paths(proj, shell, SPECIFY_FEATURE=payload)
    assert proc.returncode == 0, proc.stderr
    assert not marker.exists(), "backtick substitution in a branch name was expanded"
    assert proc.stdout == str(proj / ".specify" / "specs" / payload)


def test_newline_in_branch_name_does_not_smuggle_a_second_assignment(tmp_path, shell):
    proj = make_repo(tmp_path)
    marker = tmp_path / "PWNED_NEWLINE"
    payload = f"003-a\nREPO_ROOT=$(touch {marker})\n003-b"
    proc = run_snippet(
        proj,
        SOURCE_COMMON + SAFE_EVAL + 'printf "%s|%s" "$REQUIREMENTS_DIR" "$REPO_ROOT"',
        overlay=shell, SPECIFY_FEATURE=payload,
    )
    assert proc.returncode == 0, proc.stderr
    assert not marker.exists(), "a newline in the branch name injected an assignment"
    assert proc.stdout == f"{proj / '.specify' / 'specs' / payload}|{proj}"


def test_glob_metacharacters_are_not_expanded(tmp_path, shell):
    proj = make_repo(tmp_path)
    payload = "003-*"
    proc = _paths(proj, shell, SPECIFY_FEATURE=payload)
    assert proc.returncode == 0, proc.stderr
    # No 003-* directory exists, so the resolver returns the literal branch path.
    # An unquoted `eval $(...)` puts the value through pathname expansion, where the
    # heredoc's single quotes are literal characters and protect nothing.
    assert proc.stdout == str(proj / ".specify" / "specs" / payload)
    assert "*" in proc.stdout, "the payload lost its metacharacter; nothing is measured"


def test_space_in_repo_root_round_trips_exactly(tmp_path, shell):
    proj = make_repo(tmp_path)
    spec_dir(proj, "001-demo")
    proc = run_snippet(
        proj, SOURCE_COMMON + SAFE_EVAL + 'printf "%s" "$REPO_ROOT"',
        overlay=shell, SPECIFY_FEATURE="001-demo",
    )
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == str(proj)
    assert " " in proc.stdout, "the sandbox lost its space; the case measures nothing"


def test_master_key_contract_is_preserved(tmp_path, shell):
    proj = make_repo(tmp_path)
    spec_dir(proj, "001-demo")
    proc = run_snippet(
        proj, SOURCE_COMMON + "_out=$(get_feature_paths) || exit 1; printf '%s' \"$_out\"",
        overlay=shell, SPECIFY_FEATURE="001-demo",
    )
    assert proc.returncode == 0, proc.stderr
    emitted = dict(line.split("=", 1) for line in proc.stdout.splitlines())
    assert sorted(emitted) == sorted(MASTER_KEYS), f"key set drifted: {sorted(emitted)}"
    # The values are shell-quoted, so read them back through eval rather than by
    # stripping quotes by hand.
    read = run_snippet(
        proj,
        SOURCE_COMMON + SAFE_EVAL + 'printf "%s\\n%s\\n%s\\n%s" "$REQUIREMENTS_DIR" '
        '"$FEATURE_SPEC" "$CURRENT_BRANCH" "$BRANCH_RESOLVED_FROM_SPEC_DIR"',
        overlay=shell, SPECIFY_FEATURE="001-demo",
    )
    assert read.returncode == 0, read.stderr
    requirements_dir, feature_spec, branch, resolved = read.stdout.split("\n")
    assert requirements_dir == str(proj / ".specify" / "specs" / "001-demo")
    assert feature_spec == str(proj / ".specify" / "specs" / "001-demo" / "requirements.md")
    assert branch == "001-demo"
    assert resolved == "true"


def test_ambiguous_prefix_fails_instead_of_guessing(tmp_path, shell):
    proj = make_repo(tmp_path)
    spec_dir(proj, "002-alpha")
    spec_dir(proj, "002-beta")
    proc = run_snippet(
        proj,
        SOURCE_COMMON + 'find_feature_dir_by_prefix "$PWD" "002-demo"; echo "rc=$?"',
        overlay=shell, SPECIFY_FEATURE="002-demo",
    )
    assert "rc=1" in proc.stdout, f"ambiguous prefix did not fail: {proc.stdout!r}"
    assert "Multiple spec directories" in proc.stderr
    paths = run_snippet(
        proj, SOURCE_COMMON + 'get_feature_paths >/dev/null; echo "rc=$?"',
        overlay=shell, SPECIFY_FEATURE="002-demo",
    )
    assert "rc=1" in paths.stdout, "get_feature_paths swallowed the resolver's failure"


def test_single_match_still_resolves_by_prefix(tmp_path, shell):
    """The new failure path must not break the prefix-sharing feature it guards."""
    proj = make_repo(tmp_path)
    spec_dir(proj, "001-demo")
    proc = _paths(proj, shell, SPECIFY_FEATURE="001-other-name")
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == str(proj / ".specify" / "specs" / "001-demo")


@pytest.mark.parametrize("script", EVAL_CALLERS)
def test_every_eval_caller_exits_on_an_ambiguous_prefix(tmp_path, shell, script):
    proj = make_repo(tmp_path)
    spec_dir(proj, "002-alpha")
    spec_dir(proj, "002-beta")
    proc = run_script(proj, script, "--json", overlay=shell, SPECIFY_FEATURE="002-demo")
    assert proc.returncode == 1, f"{script} accepted an ambiguous prefix: {proc.stdout!r}"
    assert "Multiple spec directories" in proc.stderr
    assert not (proj / ".specify" / "specs" / "002-demo" / "plan.md").exists(), (
        f"{script} scaffolded into a guessed directory"
    )


@pytest.mark.parametrize("script", EVAL_CALLERS)
def test_every_eval_caller_carries_the_payload_as_data(tmp_path, shell, script):
    """Each caller resolves the payload, echoes it back verbatim, and runs none of it."""
    proj = make_repo(tmp_path)
    plan_template(proj, "# Plan\n\nreal content\n")
    marker = tmp_path / f"PWNED_{script.replace('.', '_').replace('-', '_')}"
    payload = f"003-x';touch {marker};'"
    args = ["--json"]
    if script == "check-prerequisites.sh":
        args.append("--paths-only")
    proc = run_script(proj, script, *args, overlay=shell, SPECIFY_FEATURE=payload)
    assert not marker.exists(), f"{script} executed the branch-name payload"
    assert proc.returncode == 0, f"{script}: {proc.stdout!r} {proc.stderr!r}"
    payload_json = json.loads(proc.stdout)
    assert payload_json["BRANCH"] == payload, (
        f"{script} lost or altered the branch value: {payload_json['BRANCH']!r}"
    )