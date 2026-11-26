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


# --------------------------------------------------------------------------- #
# US4 — transmission: block completeness, acknowledgement, receipt, chain (T032)
# --------------------------------------------------------------------------- #

PAYLOAD = FIXTURES / "payload"
CHAIN = FIXTURES / "chain"
M05 = FIXTURES / "m05"
M06 = FIXTURES / "m06"
M07 = FIXTURES / "m07"

#: The five decision-block fields (C-301), as the dispatch payload carries them.
BLOCK_FIELDS = (
    "decision_id", "decision_class", "chosen_option",
    "implementation_constraints", "archive_pointer",
)
#: The four implementation-receipt members (C-304).
RECEIPT_FIELDS = ("decision_id", "implementation_summary", "evidence", "divergence")


def run_action(action: str, *args: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, str(ENGINE), "--action", action, *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(ROOT),
    )


def run_payload(*args: str) -> subprocess.CompletedProcess:
    return run_action("payload", *args)


def run_chain(*args: str) -> subprocess.CompletedProcess:
    return run_action("chain", *args)


def owner_section(*tokens: str) -> str:
    """Body of the first H2 heading carrying every token, up to the next H2 or EOF."""
    lines = OWNER.read_text(encoding="utf-8").splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.startswith("## ") and all(token in line for token in tokens):
            start = index
            break
    assert start is not None, f"missing H2 section carrying {tokens!r}"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start + 1:end])


def flat(text: str) -> str:
    return " ".join(text.split())


def transmission_section() -> str:
    return flat(owner_section("传递与实施", "Transmission and Implementation"))


def test_m06_block_completeness() -> None:
    """C-301 / M-06: the decision block carries all five fields; each omission turns red."""
    complete = PAYLOAD / "complete.md"
    assert complete.is_file(), f"missing fixture: {complete}"

    section = transmission_section()
    for field in BLOCK_FIELDS:
        assert f"`{field}`" in section, (
            f"§ Transmission and Implementation does not name the block field `{field}`"
        )

    before = dir_snapshot(M06)
    ok = run_payload("--fixture", str(complete))
    assert ok.returncode == 0, (
        f"the complete block exited {ok.returncode}, expected 0: {ok.stdout} {ok.stderr}"
    )
    assert not re.search(r"(?m)^M-06 ", ok.stdout), (
        f"a complete block still carries an M-06 verdict: {ok.stdout!r}"
    )

    red_samples = {
        "red-missing-id.md": "decision_id",
        "red-missing-class.md": "decision_class",
        "red-missing-chosen.md": "chosen_option",
        "red-missing-constraints.md": "implementation_constraints",
        "red-missing-archive.md": "archive_pointer",
    }
    for name, field in red_samples.items():
        path = M06 / name
        assert path.is_file(), f"missing fixture: {path}"
        red = run_payload("--fixture", str(path))
        assert red.returncode == 1, (
            f"{name} exited {red.returncode}, expected 1: {red.stdout} {red.stderr}"
        )
        assert "M-06" in red.stdout, f"{name} carries no M-06 verdict: {red.stdout!r}"
        payload = json.loads(run_payload("--fixture", str(path), "--json").stdout)
        verdict = next(v for v in payload["violations"] if v["rule"] == "M-06")
        assert verdict["path"].endswith(name), verdict
        assert isinstance(verdict["line"], int) and verdict["line"] > 0, verdict
        assert field in verdict["message"], (name, verdict["message"])

    assert dir_snapshot(M06) == before, "a run mutated the m06 fixture tree"


def test_m06_dispatch_without_block_refused() -> None:
    """C-302 / M-06: a decision-backed dispatch without a block is refused; non-decision is legal."""
    no_block = M06 / "red-no-block.md"
    non_decision = PAYLOAD / "non-decision.md"
    for path in (no_block, non_decision):
        assert path.is_file(), f"missing fixture: {path}"

    red = run_payload("--fixture", str(no_block))
    assert red.returncode == 1, (
        f"a decision-backed dispatch without a block exited {red.returncode}, expected 1: "
        f"{red.stdout} {red.stderr}"
    )
    assert "M-06" in red.stdout, f"the verdict does not carry M-06: {red.stdout!r}"
    payload = json.loads(run_payload("--fixture", str(no_block), "--json").stdout)
    verdict = next(v for v in payload["violations"] if v["rule"] == "M-06")
    assert verdict["path"].endswith("red-no-block.md"), verdict
    assert isinstance(verdict["line"], int) and verdict["line"] > 0, verdict
    assert "decision_block" in verdict["message"], verdict

    # BC-02 bridge: a non-decision dispatch without a block stays legal.
    ok = run_payload("--fixture", str(non_decision))
    assert ok.returncode == 0, (
        f"a non-decision dispatch exited {ok.returncode}, expected 0: {ok.stdout} {ok.stderr}"
    )
    assert not re.search(r"(?m)^M-06 ", ok.stdout), ok.stdout

    # The whole m06 directory reds (the directory form the quickstart records).
    directory = run_payload("--fixture", str(M06))
    assert directory.returncode == 1, (
        f"the m06 directory exited {directory.returncode}, expected 1: {directory.stdout}"
    )


def test_acknowledgement_present() -> None:
    """C-303: the return carries an acknowledgement echoing the id; the producers owe the duty."""
    snapshot = PAYLOAD / "returns" / "return-acknowledged.md"
    assert snapshot.is_file(), f"missing fixture: {snapshot}"
    text = snapshot.read_text(encoding="utf-8")
    assert "- **decision_id**: D-001" in text, "the return does not echo the decision_id"
    assert "acknowledgement" in text and "accepted for implementation" in text, (
        "the return carries no acknowledgement stating acceptance for implementation"
    )
    for member in RECEIPT_FIELDS:
        assert f"**{member}**" in text, f"the receipt does not carry `{member}`"

    section = transmission_section()
    for token in (
        "acknowledgement",
        "回显 `decision_id`",
        "接受",
        "回传",
        "`acknowledged_at`",
        "`transmission_status`",
    ):
        assert token in section, f"§ Transmission and Implementation lacks {token!r}"
    assert "superagent-definitions.md" in section, (
        "§ Transmission does not reach the existing return channel by pointer"
    )

    for rel in ("skills/internal/run-agent/SKILL.md", "skills/internal/run-team/SKILL.md"):
        body = flat((ROOT / rel).read_text(encoding="utf-8"))
        assert "decision-definitions.md" in body, (
            f"{rel} does not reach the owner page by pointer"
        )
        assert "implementation_receipt" in body, (
            f"{rel} does not carry the implementation-receipt duty"
        )


def test_m05_receipt_reverse_samples() -> None:
    """C-304 / M-05: receipt presence and decision_id resolvability; a missing item reds."""
    green = CHAIN / "green-complete.md"
    assert green.is_file(), f"missing fixture: {green}"

    section = transmission_section()
    for member in RECEIPT_FIELDS:
        assert f"`{member}`" in section, (
            f"§ Transmission does not name the receipt member `{member}`"
        )
    for token in ("不完整", "MUST NOT 消费", "补齐"):
        assert token in section, f"§ Transmission lacks the incomplete-return rule ({token!r})"

    before = dir_snapshot(M05)
    ok = run_chain("--fixture", str(green))
    assert ok.returncode == 0, (
        f"the complete chain exited {ok.returncode}, expected 0: {ok.stdout} {ok.stderr}"
    )
    assert not re.search(r"(?m)^M-05 ", ok.stdout), ok.stdout
    for member in RECEIPT_FIELDS:
        assert f"**{member}**" in green.read_text(encoding="utf-8"), (
            f"the green chain receipt does not carry `{member}`"
        )

    red_samples = {
        "red-no-receipt.md": "receipt",
        "red-no-id.md": "decision_id",
        "red-unresolvable.md": "resolve",
    }
    for name, needle in red_samples.items():
        path = M05 / name
        assert path.is_file(), f"missing fixture: {path}"
        red = run_chain("--fixture", str(path))
        assert red.returncode == 1, (
            f"{name} exited {red.returncode}, expected 1: {red.stdout} {red.stderr}"
        )
        assert "M-05" in red.stdout, f"{name} carries no M-05 verdict: {red.stdout!r}"
        payload = json.loads(run_chain("--fixture", str(path), "--json").stdout)
        verdict = next(v for v in payload["violations"] if v["rule"] == "M-05")
        assert verdict["path"].endswith(name), verdict
        assert isinstance(verdict["line"], int) and verdict["line"] > 0, verdict
        assert needle in verdict["message"], (name, verdict["message"])

    assert dir_snapshot(M05) == before, "a run mutated the m05 fixture tree"


def test_silent_redecision_is_anomaly() -> None:
    """C-305: a child's silent re-decision breaks the chain (explicit anomaly, never silence)."""
    silent = CHAIN / "red-silent-redecision.md"
    escalated = PAYLOAD / "returns" / "return-escalated.md"
    for path in (silent, escalated):
        assert path.is_file(), f"missing fixture: {path}"

    red = run_chain("--fixture", str(silent))
    assert red.returncode == 1, (
        f"a silent re-decision exited {red.returncode}, expected 1: {red.stdout} {red.stderr}"
    )
    assert "M-07" in red.stdout, f"the verdict does not carry M-07: {red.stdout!r}"
    payload = json.loads(run_chain("--fixture", str(silent), "--json").stdout)
    verdicts = [v for v in payload["violations"] if v["rule"] == "M-07"]
    assert verdicts, payload["violations"]
    assert any("D-002" in v["message"] for v in verdicts), verdicts

    # The correct alternative is the explicit escalation: no receipt, an anomaly line.
    escalation = escalated.read_text(encoding="utf-8")
    assert "ANOMALY:" in escalation, "the escalation snapshot carries no explicit anomaly line"
    assert "implementation_receipt" not in escalation, (
        "an escalated return must not fabricate a receipt"
    )

    section = transmission_section()
    for token in ("MUST NOT 静默重决", "fast-fail", "不完整"):
        assert token in section, f"§ Transmission lacks the no-silent-re-decision duty ({token!r})"


def test_m07_chain_three_segments() -> None:
    """C-306 / M-07: record → dispatch attempt → receipt; any missing segment turns red."""
    green = CHAIN / "green-complete.md"
    ok = run_chain("--fixture", str(green))
    assert ok.returncode == 0, (
        f"the complete chain exited {ok.returncode}, expected 0: {ok.stdout} {ok.stderr}"
    )
    assert not re.search(r"(?m)^M-07 ", ok.stdout), ok.stdout

    section = transmission_section()
    for token in ("决策记录", "派发尝试", "实施回执", "显式异常"):
        assert token in section, f"§ Transmission does not name the chain element {token!r}"

    red_samples = {
        "red-missing-record.md": "record",
        "red-missing-dispatch.md": "dispatch",
        "red-missing-receipt.md": "receipt",
        "red-inconsistent-id.md": "D-003",
    }
    before = dir_snapshot(M07)
    for name, needle in red_samples.items():
        path = M07 / name
        assert path.is_file(), f"missing fixture: {path}"
        red = run_chain("--fixture", str(path))
        assert red.returncode == 1, (
            f"{name} exited {red.returncode}, expected 1: {red.stdout} {red.stderr}"
        )
        assert "M-07" in red.stdout, f"{name} carries no M-07 verdict: {red.stdout!r}"
        payload = json.loads(run_chain("--fixture", str(path), "--json").stdout)
        verdict = next(v for v in payload["violations"] if v["rule"] == "M-07")
        assert verdict["path"].endswith(name), verdict
        assert isinstance(verdict["line"], int) and verdict["line"] > 0, verdict
        assert needle in verdict["message"], (name, verdict["message"])

    assert dir_snapshot(M07) == before, "a run mutated the m07 fixture tree"


def test_multi_hop_same_id() -> None:
    """C-307: every hop carries the block and every receipt keeps the same decision_id."""
    green = CHAIN / "multi-hop-green.md"
    red = CHAIN / "red-multi-hop-id.md"
    for path in (green, red):
        assert path.is_file(), f"missing fixture: {path}"

    text = green.read_text(encoding="utf-8")
    assert text.count("## Dispatch Attempt") == 2, "the multi-hop fixture is not two hops"
    assert text.count("## Receipt") == 2, "the multi-hop fixture carries two receipts"
    assert text.count("- **decision_id**: D-001") == 5, (
        "not every hop segment references the recorded decision id "
        "(record + two dispatch attempts + two receipts)"
    )

    ok = run_chain("--fixture", str(green))
    assert ok.returncode == 0, (
        f"the multi-hop chain exited {ok.returncode}, expected 0: {ok.stdout} {ok.stderr}"
    )
    assert not re.search(r"(?m)^M-07 ", ok.stdout), ok.stdout

    broken = run_chain("--fixture", str(red))
    assert broken.returncode == 1, (
        f"a diverging hop id exited {broken.returncode}, expected 1: "
        f"{broken.stdout} {broken.stderr}"
    )
    assert "M-07" in broken.stdout, f"the verdict does not carry M-07: {broken.stdout!r}"

    section = transmission_section()
    for token in ("多跳", "每一跳", "同一 `decision_id`"):
        assert token in section, f"§ Transmission does not name the multi-hop rule ({token!r})"


def test_supersession_preserves_old() -> None:
    """C-308: a re-decision adds a record and preserves the old record and its receipt state."""
    carrier = CHAIN / "carriers" / "redecision.md"
    lossy = CHAIN / "carriers" / "redecision-lossy.md"
    register = CHAIN / "carriers" / "register.md"
    for path in (carrier, lossy, register):
        assert path.is_file(), f"missing fixture: {path}"

    before = carrier.read_bytes()
    run, payload = run_records_json("--carrier", str(carrier), "--register", str(register))
    assert run.returncode == 0, (
        f"the re-decision carrier exited {run.returncode}, expected 0: {run.stdout} {run.stderr}"
    )
    assert payload["status"] == "pass", payload["violations"]
    ids = [record["id"] for record in payload["records"]]
    assert ids == ["D-001", "D-002"], ids
    old = next(record for record in payload["records"] if record["id"] == "D-001")
    assert old["fields"]["superseded_by"].startswith("D-002"), old
    assert old["fields"]["transmission_status"] == "diverged", old
    assert old["fields"]["implemented_at"], old
    assert carrier.read_bytes() == before, "the run rewrote the carrier"

    red = run_records("--carrier", str(lossy), "--register", str(register))
    assert red.returncode == 1, (
        f"a rewritten old record exited {red.returncode}, expected 1: {red.stdout} {red.stderr}"
    )
    assert "M-01" in red.stdout, f"the verdict does not carry M-01: {red.stdout!r}"
    lossy_payload = json.loads(
        run_records("--carrier", str(lossy), "--register", str(register), "--json").stdout
    )
    messages = " ".join(
        v["message"] for v in lossy_payload["violations"] if v["rule"] == "M-01"
    )
    assert "implemented_at missing" in messages, messages

    section = transmission_section()
    for token in ("`superseded_by`", "保留", "重决"):
        assert token in section, f"§ Transmission lacks the supersession duty ({token!r})"
