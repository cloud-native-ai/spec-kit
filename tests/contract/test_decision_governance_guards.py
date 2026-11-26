"""Guard tests for Feature 107 — decision-governance machine rules in their red-first form.

This module owns the reverse samples of the ``validate-decisions.py --action records``
guards. US1 lands the two production-accident guards:

* ``test_m02_locator_red_then_green`` — C-103 / M-02: ``same_name_conflict: true`` with an
  empty ``resource_locator`` or with fewer named dimensions than the business resource
  group + region id floor turns red; the completed pair turns green.
* ``test_m08_registered_variant_red`` — M-08: a decision subject that uses a registered
  glossary variant (whose canonical exists) turns red; the full name turns green; an
  *unregistered* abbreviation stays green because only registered words are covered.

Both drive the engine as a real process (``subprocess``) so exit codes, verdict lines and
the JSON payload are observed exactly as a shell caller observes them. Each verdict MUST
carry the rule id, the carrier path, the line and a message, and the run MUST mutate
nothing inside the fixture tree.

Later user stories APPEND their own guard tests (M-01, M-03…M-07, M-09, the payload and
chain snapshots) to this module without touching these assertions.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "validate-decisions.py"
FIXTURES = ROOT / "tests" / "fixtures" / "decision-governance"

VERDICT_LINE_RE = re.compile(r"^M-0[0-9] \S+\.md:\d+: \S", re.M)


def run_records(*args: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, str(ENGINE), "--action", "records", *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(ROOT),
    )


def dir_snapshot(path: Path) -> list[tuple[str, int, int]]:
    return sorted(
        (str(p.relative_to(path)), p.stat().st_size, p.stat().st_mtime_ns)
        for p in path.rglob("*")
        if p.is_file()
    )


def test_m02_locator_red_then_green() -> None:
    """C-103 / M-02: the same-name family needs the locator floor, and nothing else."""
    red_empty = FIXTURES / "m02" / "red-empty-locator.md"
    red_one_dim = FIXTURES / "m02" / "red-single-dimension.md"
    green = FIXTURES / "m02" / "green-complete.md"
    for path in (red_empty, red_one_dim, green):
        assert path.is_file(), f"missing fixture: {path}"

    before = dir_snapshot(FIXTURES / "m02")

    # Red: same_name_conflict: true with an empty resource_locator.
    red = run_records("--carrier", str(red_empty))
    assert red.returncode == 1, (
        f"empty resource_locator exited {red.returncode}, expected 1: {red.stderr}"
    )
    assert "M-02" in red.stdout, f"the verdict does not carry the rule id M-02: {red.stdout!r}"
    assert re.search(r"red-empty-locator\.md:\d+", red.stdout), (
        f"the verdict does not carry carrier path:line: {red.stdout!r}"
    )

    # Red: only one named dimension (region id without the business resource group).
    red2 = run_records("--carrier", str(red_one_dim))
    assert red2.returncode == 1, (
        f"single-dimension locator exited {red2.returncode}, expected 1: {red2.stderr}"
    )
    assert "M-02" in red2.stdout, f"the verdict does not carry M-02: {red2.stdout!r}"

    # The machine-readable payload carries rule, path, line and message too.
    payload = json.loads(run_records("--carrier", str(red_empty), "--json").stdout)
    assert payload["status"] == "fail", f"JSON status: {payload}"
    verdicts = [v for v in payload["violations"] if v["rule"] == "M-02"]
    assert verdicts, f"JSON payload carries no M-02 violation: {payload}"
    verdict = verdicts[0]
    assert verdict["path"].endswith("red-empty-locator.md"), verdict
    assert isinstance(verdict["line"], int) and verdict["line"] > 0, verdict
    assert verdict["message"], verdict

    # Green: business resource group + region id present.
    ok = run_records("--carrier", str(green))
    assert ok.returncode == 0, (
        f"completed locator exited {ok.returncode}, expected 0: {ok.stdout} {ok.stderr}"
    )
    assert not re.search(r"(?m)^M-02 ", ok.stdout), (
        f"a completed locator still carries an M-02 verdict: {ok.stdout!r}"
    )

    assert dir_snapshot(FIXTURES / "m02") == before, "a run mutated the m02 fixture tree"


def test_m08_registered_variant_red() -> None:
    """M-08: a registered glossary variant in the subject is red; only registered words."""
    glossary = FIXTURES / "m08" / "glossary.md"
    red = FIXTURES / "m08" / "red-variant.md"
    green = FIXTURES / "m08" / "green-full-name.md"
    unregistered = FIXTURES / "m08" / "green-unregistered.md"
    for path in (glossary, red, green, unregistered):
        assert path.is_file(), f"missing fixture: {path}"

    before = dir_snapshot(FIXTURES / "m08")

    # Red: the subject uses the registered variant `spec-kit`.
    red_run = run_records("--carrier", str(red), "--glossary", str(glossary))
    assert red_run.returncode == 1, (
        f"registered-variant subject exited {red_run.returncode}, expected 1: "
        f"{red_run.stdout} {red_run.stderr}"
    )
    assert "M-08" in red_run.stdout, (
        f"the verdict does not carry the rule id M-08: {red_run.stdout!r}"
    )
    assert re.search(r"red-variant\.md:\d+", red_run.stdout), (
        f"the verdict does not carry carrier path:line: {red_run.stdout!r}"
    )
    assert VERDICT_LINE_RE.search(red_run.stdout), (
        f"the verdict line does not carry rule/path/line/message: {red_run.stdout!r}"
    )

    payload = json.loads(
        run_records("--carrier", str(red), "--glossary", str(glossary), "--json").stdout
    )
    assert payload["status"] == "fail", f"JSON status: {payload}"
    verdict = next(v for v in payload["violations"] if v["rule"] == "M-08")
    assert verdict["path"].endswith("red-variant.md"), verdict
    assert isinstance(verdict["line"], int) and verdict["line"] > 0, verdict
    assert verdict["message"], verdict

    # Green: the full name.
    ok = run_records("--carrier", str(green), "--glossary", str(glossary))
    assert ok.returncode == 0, (
        f"full-name subject exited {ok.returncode}, expected 0: {ok.stdout} {ok.stderr}"
    )
    assert not re.search(r"(?m)^M-08 ", ok.stdout), (
        f"a full-name subject still carries an M-08 verdict: {ok.stdout!r}"
    )

    # Green: an unregistered abbreviation — only registered words are covered.
    unreg = run_records("--carrier", str(unregistered), "--glossary", str(glossary))
    assert unreg.returncode == 0, (
        f"unregistered abbreviation exited {unreg.returncode}, expected 0 "
        f"(only registered words are covered): {unreg.stdout} {unreg.stderr}"
    )

    assert dir_snapshot(FIXTURES / "m08") == before, "a run mutated the m08 fixture tree"


# --------------------------------------------------------------------------- #
# US3 — record closure, evidence pointers, legacy and reconstruction (T024)
# --------------------------------------------------------------------------- #

M01 = FIXTURES / "m01"
M09 = FIXTURES / "m09"
LEGACY = FIXTURES / "legacy"
RECONSTRUCT = FIXTURES / "reconstruct"
OWNER = ROOT / "shared" / "definitions" / "decision-definitions.md"


def run_records_json(*args: str) -> tuple[subprocess.CompletedProcess, dict]:
    run = run_records(*args, "--json")
    return run, json.loads(run.stdout)


def test_broken_pointer_red() -> None:
    """C-204 / M-09: an unresolvable evidence pointer turns red; a resolvable one stays green."""
    green = M09 / "green-resolvable.md"
    broken = M09 / "red-broken.md"
    broken_anchor = M09 / "red-broken-anchor.md"
    for path in (green, broken, broken_anchor):
        assert path.is_file(), f"missing fixture: {path}"

    before = dir_snapshot(M09)

    ok = run_records("--carrier", str(green))
    assert ok.returncode == 0, (
        f"resolvable pointers exited {ok.returncode}, expected 0: {ok.stdout} {ok.stderr}"
    )
    assert not re.search(r"(?m)^M-09 ", ok.stdout), ok.stdout

    red = run_records("--carrier", str(broken))
    assert red.returncode == 1, (
        f"a broken pointer exited {red.returncode}, expected 1: {red.stdout} {red.stderr}"
    )
    assert "M-09" in red.stdout, f"the verdict does not carry M-09: {red.stdout!r}"
    payload = json.loads(run_records("--carrier", str(broken), "--json").stdout)
    verdict = next(v for v in payload["violations"] if v["rule"] == "M-09")
    assert verdict["path"].endswith("red-broken.md"), verdict
    assert isinstance(verdict["line"], int) and verdict["line"] > 0, verdict
    assert verdict["message"], verdict

    anchor = run_records("--carrier", str(broken_anchor))
    assert anchor.returncode == 1, (
        f"a broken anchor exited {anchor.returncode}, expected 1: {anchor.stdout} {anchor.stderr}"
    )
    assert "M-09" in anchor.stdout, f"the anchor verdict does not carry M-09: {anchor.stdout!r}"

    assert dir_snapshot(M09) == before, "a run mutated the m09 fixture tree"


def test_no_tension_field_copy() -> None:
    """C-205: a record copying the tension six fields is red; a T-NNN cross-reference is green."""
    copy = M01 / "red-tension-copy.md"
    crossref = M01 / "green-tension-ref.md"
    for path in (copy, crossref):
        assert path.is_file(), f"missing fixture: {path}"

    red = run_records("--carrier", str(copy))
    assert red.returncode == 1, (
        f"a copied tension field exited {red.returncode}, expected 1: {red.stdout} {red.stderr}"
    )
    assert "M-01" in red.stdout, f"the verdict does not carry M-01: {red.stdout!r}"
    payload = json.loads(run_records("--carrier", str(copy), "--json").stdout)
    messages = " ".join(
        v["message"] for v in payload["violations"] if v["rule"] == "M-01"
    )
    assert "antithesis" in messages and "binding_constraints" in messages, messages

    ok = run_records("--carrier", str(crossref))
    assert ok.returncode == 0, (
        f"a T-NNN cross-reference exited {ok.returncode}, expected 0: {ok.stdout} {ok.stderr}"
    )

    owner = (ROOT / "shared" / "definitions" / "decision-definitions.md").read_text(encoding="utf-8")
    assert "T-NNN" in owner and "MUST NOT 复制" in owner, (
        "the owner page does not state the cross-reference-only duty"
    )


def test_legacy_two_digit_reported_legacy() -> None:
    """C-206: legacy headings and register rows are reported, never judged or rewritten."""
    register = LEGACY / "register.md"
    legacy_md = LEGACY / "legacy.md"
    incomplete = LEGACY / "incomplete-new-form.md"
    for path in (register, legacy_md, incomplete):
        assert path.is_file(), f"missing fixture: {path}"

    before = dir_snapshot(LEGACY)

    run, payload = run_records_json("--carrier", str(legacy_md), "--register", str(register))
    assert run.returncode == 0, (
        f"the legacy carrier exited {run.returncode}, expected 0: {run.stdout} {run.stderr}"
    )
    assert payload["status"] == "pass", payload
    assert payload["violations"] == [], payload["violations"]

    headings = [e for e in payload["legacy"] if e["kind"] == "heading"]
    texts = [e["text"] for e in headings]
    for prefix in ("### D-1 ", "### D-12 ", "### D-001 "):
        assert any(text.startswith(prefix) for text in texts), (prefix, texts)

    row_ids = {e["id"] for e in payload["legacy"] if e["kind"] == "register-row"}
    assert any(row_id.startswith("D1") for row_id in row_ids), row_ids
    assert "D-001" in row_ids and "D-001-a" in row_ids, row_ids
    assert not any("legacy.md" in v["path"] for v in payload["violations"]), (
        "a legacy heading was judged as a violation"
    )

    # The pair's other half: a block at the minimal qualifying form is new-form even when
    # incomplete — its missing fields are M-01's red, not a legacy report.
    run2, payload2 = run_records_json("--carrier", str(incomplete), "--register", str(register))
    assert run2.returncode == 1, (
        f"the incomplete new-form block exited {run2.returncode}, expected 1: "
        f"{run2.stdout} {run2.stderr}"
    )
    assert any(v["rule"] == "M-01" for v in payload2["violations"]), payload2["violations"]
    assert not any(
        e["kind"] == "heading" and e["text"].startswith("### D-001 ")
        for e in payload2["legacy"]
    ), payload2["legacy"]

    assert dir_snapshot(LEGACY) == before, "a run mutated the legacy fixture tree"


def test_reconstruct_from_register_and_carriers() -> None:
    """C-204: every record is reconstructable from the four carrier types + the register."""
    run, payload = run_records_json(
        "--fixture", str(RECONSTRUCT), "--register", str(RECONSTRUCT / "register.md")
    )
    assert run.returncode == 0, (
        f"the four-carrier fixture exited {run.returncode}, expected 0: {run.stdout} {run.stderr}"
    )
    assert payload["status"] == "pass", payload["violations"]

    records = payload["records"]
    assert len(records) == 4, records
    for suffix in (
        "reconstruct/requirements.md",
        "reconstruct/plan.md",
        "reconstruct/checkpoints/02-implement.md",
        "reconstruct/run-report.md",
    ):
        assert any(record["path"].endswith(suffix) for record in records), (suffix, records)

    base_fields = (
        "decision_class", "context", "options", "chosen_option", "rationale",
        "evidence", "actor", "created_at", "transmission_status",
    )
    for record in records:
        assert record["id"] == "D-001", record
        for field in base_fields:
            assert record["fields"].get(field), (record["path"], field)
        assert record["fields"]["transmission_status"] == "not-transmitted", record

    requirements = next(r for r in records if r["path"].endswith("requirements.md"))
    assert requirements["fields"].get("same_name_conflict") == "true", requirements
    assert "business_resource_group=" in requirements["fields"].get("resource_locator", ""), (
        requirements
    )
    assert not any(v["rule"] == "M-04" for v in payload["violations"]), payload["violations"]
