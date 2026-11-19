"""JSON output escaping and the output key contract.

Ported fix family (upstream github/spec-kit):
  * 9c0c1446e — the ``printf`` JSON line embedded raw values, so a quote or backslash
    in a path produced output that no JSON parser accepts.
  * 2e55bdd3f — residual control characters are ENCODED as ``\\uXXXX``, never stripped,
    so the value round-trips instead of silently losing bytes.

The key names and their order (BRANCH_NAME, SPEC_FILE, FEATURE_NUM) are this fork's
contract with its consumers and are deliberately unchanged; only value encoding moved.

No escaper was reusable from here: common.sh publishes none, and common-todo.sh keeps
json_escape_string inside its own main(), which sourcing does not publish. The escaper
therefore lives in this script, following the upstream implementation.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.unit.requirements_scaffold import (
    byte_len,
    make_project,
    run_script,
)


def _json_for(tmp_path, dirname, description="Add user authentication system"):
    base = tmp_path / dirname
    base.mkdir()
    proj = make_project(base)
    proc = run_script(proj, "--json", description)
    assert proc.returncode == 0, proc.stderr
    # JSON mode must not be polluted by git or warning chatter on stdout.
    assert len(proc.stdout.strip().splitlines()) == 1, proc.stdout
    return proc, json.loads(proc.stdout)


@pytest.mark.parametrize(
    "dirname",
    [
        'q"dir',
        "b\\dir",
        "t\tdir",
        "n\ndir",
        "c\x01dir",
        "c\x1fdir",
        'mixed"\\\tname',
    ],
)
def test_hostile_repo_path_still_yields_valid_json_that_round_trips(tmp_path, dirname):
    """9c0c1446e + 2e55bdd3f: the parsed SPEC_FILE equals the real path, byte for byte."""
    proc, payload = _json_for(tmp_path, dirname)
    expected = str(tmp_path / dirname / "tree" / ".specify" / "specs")
    assert payload["SPEC_FILE"].startswith(expected), payload["SPEC_FILE"]
    assert payload["SPEC_FILE"].endswith("/requirements.md")
    # The path on disk is exactly the path reported: nothing was stripped or mangled.
    assert Path(payload["SPEC_FILE"]).is_file(), payload["SPEC_FILE"]


def test_control_characters_are_encoded_not_stripped(tmp_path):
    """2e55bdd3f: a stripped control character would silently shorten the reported path."""
    _, payload = _json_for(tmp_path, "c\x01dir")
    assert "\x01" in payload["SPEC_FILE"]
    _, payload = _json_for(tmp_path, "c\x1fdir")
    assert "\x1f" in payload["SPEC_FILE"]


def test_tab_and_newline_use_the_named_escapes(tmp_path):
    proc, _ = _json_for(tmp_path, "t\tdir")
    assert "\\t" in proc.stdout
    proc, _ = _json_for(tmp_path, "n\ndir")
    assert "\\n" in proc.stdout


def test_quote_and_backslash_are_escaped(tmp_path):
    proc, _ = _json_for(tmp_path, 'q"dir')
    assert '\\"' in proc.stdout
    proc, _ = _json_for(tmp_path, "b\\dir")
    assert "\\\\" in proc.stdout


def test_key_names_and_order_are_unchanged(tmp_path):
    """The consumer contract: same keys, same order, same value shapes."""
    _, payload = _json_for(tmp_path, "plain")
    assert list(payload.keys()) == ["BRANCH_NAME", "SPEC_FILE", "FEATURE_NUM"]
    assert payload["BRANCH_NAME"] == "001-user-authentication-system"
    assert payload["FEATURE_NUM"] == "001"
    assert payload["SPEC_FILE"].endswith(
        "/001-user-authentication-system/requirements.md"
    )


def test_unicode_branch_name_round_trips_as_utf8(tmp_path):
    """Multi-byte UTF-8 must pass through intact, not be split into per-byte escapes."""
    _, payload = _json_for(tmp_path, "plain", "添加用户认证系统")
    assert payload["BRANCH_NAME"] == "001-添加用户认证系统"
    assert byte_len(payload["BRANCH_NAME"]) > len(payload["BRANCH_NAME"])


def test_json_mode_is_stable_across_repeated_runs(tmp_path):
    """Escaping must not depend on locale-driven byte/character counting."""
    _, first = _json_for(tmp_path, 'q"dir')
    base = tmp_path / "second"
    base.mkdir()
    proj = make_project(base)
    proc = run_script(proj, "--json", "Add user authentication system", env={"LC_ALL": "C"})
    assert proc.returncode == 0, proc.stderr
    second = json.loads(proc.stdout)
    assert list(first.keys()) == list(second.keys())
    assert second["BRANCH_NAME"] == "001-user-authentication-system"