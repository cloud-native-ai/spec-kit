"""P1 Agent B — complete JSON string escaping on the bash reporting surface.

Ported fix shape: upstream 9c0c1446ecc7b8e92d866050b5cbc620d8a307e5 (complete RFC 8259
escape) and 2e55bdd3f279849a4e499a4a7c1a0d63d39f117b (residual control characters
encoded as \\uXXXX, never stripped).

Measured on this fork before the port:
* ``report_error`` / ``report_success`` doubled only the double quote, so a backslash
  produced ``{"message": "back\\slash"}`` — json.loads: "Invalid \\escape" — and a
  newline produced a raw control character: "Invalid control character".
* ``implement-plan.sh`` already called ``json_escape`` at its printf, but no such
  function was reachable: common.sh did not publish it, so every value came out
  empty and stderr carried "json_escape: command not found".

Adaptation note (the reason there is no new escaper body in common.sh): the complete
escaper is owned by the host shell library, ``$CWS_LIB_BASH_HOME/profile.d/04_format.sh``.
common.sh's library-link captures each published name with ``declare -f`` inside a
subshell that sources the host library FIRST, so a json_escape defined at common.sh's
file scope is shadowed before capture — it would be dead code. The port therefore
publishes the host owner and routes every interpolated value through it. These cases
pin the behaviour, not the implementation, so they stay true if the owner changes.

Anti-vacuity: every case compares the PARSED value against the original payload, so an
escaper that dropped, stripped or emptied a character fails; and the caller cases
assert the values are non-empty, which is exactly what the old defect produced.
"""
from __future__ import annotations

import json

import pytest

from tests.unit.bash_hardening_sandbox import (
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

#: Short payloads on purpose: the owner escapes per character, so a long corpus would
#: make this module slow without measuring anything more.
PAYLOADS = [
    "",
    "plain text",
    'quote " inside',
    "back\\slash",
    'both \\" mixed',
    "line1\nline2",
    "tab\there",
    "carriage\rreturn",
    "back\bspace",
    "form\ffeed",
    "residual\x01\x02\x07\x0b\x0e\x1f",
    "unicode 世界 café",
    "emoji 👋 and \"quotes\"",
    "shell $(id) `id` ; | & *",
    "single'quote",
    "path/to/requirements.md",
    "mixed\n\t\"\\\x01end",
]

#: One line on purpose: check-prerequisites reads FEATURE_NAME with a line-oriented
#: sed, so a newline cannot survive that extraction and is not this case's subject
#: (newline handling in a *branch* value is covered by the injection module).
NASTY_FEATURE_NAME = 'evil "name" \\backslash\ttabbed\x01 世界'


def _report(proj, shell, helper, *args):
    """One bash run that reports every payload, one JSON document per line."""
    extra = " ".join(args)
    snippet = SOURCE_COMMON + f'for _a in "$@"; do {helper} "$_a" {extra} true; done'
    return run_snippet(proj, snippet, *PAYLOADS, overlay=shell)


def _messages(proc):
    lines = proc.stdout.splitlines()
    assert len(lines) == len(PAYLOADS), (
        f"expected one JSON document per payload, got {len(lines)}: {proc.stdout!r} "
        f"{proc.stderr!r}"
    )
    return [json.loads(line) for line in lines]


def test_json_escape_is_reachable_from_a_sourcing_caller(tmp_path, shell):
    """The defect was an undefined function, so reachability is itself the assertion."""
    proj = make_repo(tmp_path)
    proc = run_snippet(proj, SOURCE_COMMON + 'type -t json_escape', overlay=shell)
    assert proc.stdout.strip() == "function", (
        f"json_escape is not published to a caller that sources common.sh: "
        f"{proc.stdout!r} {proc.stderr!r}"
    )


def test_report_error_payloads_round_trip(tmp_path, shell):
    proj = make_repo(tmp_path)
    proc = _report(proj, shell, "report_error")
    assert proc.returncode == 0, proc.stderr
    for payload, doc in zip(PAYLOADS, _messages(proc)):
        assert doc["status"] == "error"
        assert doc["message"] == payload, f"report_error altered {payload!r}"


def test_report_success_payloads_round_trip(tmp_path, shell):
    proj = make_repo(tmp_path)
    proc = _report(proj, shell, "report_success", '""')
    assert proc.returncode == 0, proc.stderr
    for payload, doc in zip(PAYLOADS, _messages(proc)):
        assert doc["status"] == "success"
        assert doc["message"] == payload, f"report_success altered {payload!r}"


def test_report_success_keeps_the_caller_data_fragment(tmp_path, shell):
    """The fragment is caller-authored JSON: escaped message, untouched structure."""
    proj = make_repo(tmp_path)
    proc = run_snippet(
        proj,
        SOURCE_COMMON + 'report_success "$1" \'"path": "/tmp/x", "count": 3\' true',
        'msg "q" \\ end', overlay=shell,
    )
    assert proc.returncode == 0, proc.stderr
    doc = json.loads(proc.stdout)
    assert doc["message"] == 'msg "q" \\ end'
    assert doc["path"] == "/tmp/x"
    assert doc["count"] == 3


def test_control_characters_are_encoded_not_stripped(tmp_path, shell):
    """2e55bdd3f's subject: stripping loses data, \\uXXXX preserves it."""
    proj = make_repo(tmp_path)
    payload = "".join(chr(c) for c in range(1, 32) if c not in (9, 10, 13))
    proc = run_snippet(
        proj, SOURCE_COMMON + 'report_error "$1" true', payload, overlay=shell,
    )
    assert proc.returncode == 0, proc.stderr
    doc = json.loads(proc.stdout)
    assert doc["message"] == payload, "a control character was stripped or altered"
    assert "\\u00" in proc.stdout, "residual control characters were not \\uXXXX-encoded"


def _feature(proj, shell, name=NASTY_FEATURE_NAME):
    """A resolved feature with requirements.md AND plan.md, so MODE is B."""
    spec_dir(proj, "001-demo")
    (proj / ".specify" / "specs" / "001-demo" / "requirements.md").write_text(
        f"**Feature ID**: 001\n**Feature Name**: {name}\n", encoding="utf-8"
    )
    plan_template(proj, "# Plan\n\nreal content\n")
    (proj / ".specify" / "specs" / "001-demo" / "plan.md").write_text(
        "# Plan\n\nreal content\n", encoding="utf-8"
    )


def test_check_prerequisites_json_round_trips_feature_name(tmp_path, shell):
    proj = make_repo(tmp_path)
    _feature(proj, shell)
    proc = run_script(proj, "check-prerequisites.sh", "--json", "--require-spec",
                      "--include-spec", "--include-plan", overlay=shell,
                      SPECIFY_FEATURE="001-demo")
    assert proc.returncode == 0, proc.stderr
    doc = json.loads(proc.stdout)
    assert doc["FEATURE_NAME"] == NASTY_FEATURE_NAME
    assert doc["FEATURE_ID"] == "001"
    assert doc["MODE"] == "B"
    assert isinstance(doc["WRITABLE"], bool), "WRITABLE must stay a JSON boolean"
    assert doc["AVAILABLE_DOCS"] == ["requirements.md", "plan.md"]
    assert all(isinstance(d, str) for d in doc["AVAILABLE_DOCS"])


def test_check_prerequisites_paths_only_json_round_trips(tmp_path, shell):
    proj = make_repo(tmp_path)
    _feature(proj, shell)
    proc = run_script(proj, "check-prerequisites.sh", "--json", "--paths-only",
                      overlay=shell, SPECIFY_FEATURE="001-demo")
    assert proc.returncode == 0, proc.stderr
    doc = json.loads(proc.stdout)
    assert doc["FEATURE_NAME"] == NASTY_FEATURE_NAME
    assert doc["REQUIREMENTS_DIR"] == str(proj / ".specify" / "specs" / "001-demo")
    assert doc["FEATURE_SPEC"].endswith("/requirements.md")
    assert isinstance(doc["WRITABLE"], bool)


def test_check_prerequisites_empty_docs_array_is_still_valid_json(tmp_path, shell):
    proj = make_repo(tmp_path)
    spec_dir(proj, "001-demo")
    plan_template(proj, "# Plan\n")
    (proj / ".specify" / "specs" / "001-demo" / "plan.md").write_text("# Plan\n", encoding="utf-8")
    proc = run_script(proj, "check-prerequisites.sh", "--json", overlay=shell,
                      SPECIFY_FEATURE="001-demo")
    assert proc.returncode == 0, proc.stderr
    doc = json.loads(proc.stdout)
    assert doc["AVAILABLE_DOCS"] == []


def test_implement_plan_json_is_one_payload_with_real_values(tmp_path, shell):
    """Before the port every value was empty and stdout carried two JSON documents."""
    proj = make_repo(tmp_path)
    _feature(proj, shell)
    user_input = 'price "100" \\$ & 世界👋\nsecond line'
    proc = run_script(proj, "implement-plan.sh", "--json", "--input", user_input,
                      overlay=shell, SPECIFY_FEATURE="001-demo")
    assert proc.returncode == 0, proc.stderr
    assert "command not found" not in proc.stderr, proc.stderr
    assert len(proc.stdout.splitlines()) == 1, (
        f"stdout is not a single JSON document: {proc.stdout!r}"
    )
    doc = json.loads(proc.stdout)
    assert doc["BRANCH"] == "001-demo"
    assert doc["HAS_GIT"] == "true"
    assert doc["USER_INPUT"] == user_input
    assert doc["FEATURE_SPEC"] == str(proj / ".specify" / "specs" / "001-demo" / "requirements.md")
    assert doc["IMPL_PLAN"] == str(proj / ".specify" / "specs" / "001-demo" / "plan.md")
    assert doc["SPECS_DIR"] == str(proj / ".specify" / "specs" / "001-demo")
    for key in ("FEATURE_SPEC", "IMPL_PLAN", "SPECS_DIR", "BRANCH"):
        assert doc[key], f"{key} came out empty — the undefined-escaper defect is back"


def test_create_new_plan_json_round_trips_a_hostile_branch(tmp_path, shell):
    proj = make_repo(tmp_path)
    plan_template(proj, "# Plan\n\nreal content\n")
    payload = '003-hostile "branch" \\ end'
    proc = run_script(proj, "create-new-plan.sh", "--json", overlay=shell,
                      SPECIFY_FEATURE=payload)
    assert proc.returncode == 0, proc.stderr
    assert len(proc.stdout.splitlines()) == 1, f"stdout is not pure JSON: {proc.stdout!r}"
    doc = json.loads(proc.stdout)
    assert doc["BRANCH"] == payload
    assert doc["FEATURE_SPEC"].endswith("/requirements.md")
    assert doc["HAS_GIT"] == "true"


def test_research_project_json_round_trips(tmp_path, shell):
    proj = make_repo(tmp_path)
    _feature(proj, shell)
    proc = run_script(proj, "research-project.sh", "--json", overlay=shell,
                      SPECIFY_FEATURE="001-demo")
    assert proc.returncode == 0, proc.stderr
    doc = json.loads(proc.stdout)
    assert doc["BRANCH"] == "001-demo"
    assert doc["SPECS_DIR"] == str(proj / ".specify" / "specs" / "001-demo")
    assert isinstance(doc["BRANCH_NOTE"], str) and doc["BRANCH_NOTE"]