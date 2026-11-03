"""Contract tests for contracts/closure-acceptance-check.contract.md — C-01…C-09, C-13…C-16.

Subject: ``scripts/python/closure-acceptance-check.py``. Every assertion below runs the checker as
a subprocess through its real calling surface — no regex of its internals is re-implemented here,
because a second copy of the parser would be a second answer to the same question (GW-04).

Schema owner: ``shared/workflow/acceptance-hardening.md`` § Closure Verdict. This module **pins**
that owner's literals; it never introduces one. The seven reason templates are read from the
declaring specification's ``## Shared Strings`` table (STR-008…STR-014) and membership is judged by
the two-part test that table states — *template match plus a well-formed argument* — never by byte
equality against a table cell. That distinction is the point of the test: a checker that re-spelled
``SC-NNN`` into a concrete id by string concatenation of the table cell would pass a byte test and
fail this one.

Red-first (slice 081a, task T007): the checker landed its calling surface in T006 and its verdict in
T015, so this module is **red until T015** lands ``run()``. Nothing here is faked green: the red run
is recorded in ``.specify/specs/081-acceptance-hardening/notes/red-first-evidence.md`` § 1.1.

Fixture map (``tests/fixtures/acceptance-hardening/``, authored by T003/T004/T021):

===============  ==========================================================  ======================
fixture          shape                                                       verdict / reason
===============  ==========================================================  ======================
``positive``     every ``final`` SC ``pass``, complete smoke record          ``accept`` / 0
``negative``     the 026 shape: zero open tasks, every ``final`` SC blocked   ``block`` / 1, zero-pass
``ladder-mut…``  ``reduced_measurement`` non-empty with ``…_run=no``           ``block`` / 1, ladder
``smoke-mut…``   claimed ``Implemented``, smoke record deleted                ``block`` / 1, claimed
``mixed-path``   one ``final`` pass, one ``final`` fail, one supporting def.  ``block`` / 1, SC-002
``exec-with…``   ``execution`` class, zero ``final`` SC                      ``block`` / 1, zero-pass
``expr-sup…``    ``expression`` class, all ``supporting``                     no final-path reason
===============  ==========================================================  ======================
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts" / "python" / "closure-acceptance-check.py"
FIXTURES = ROOT / "tests" / "fixtures" / "acceptance-hardening"
SPEC = ROOT / ".specify" / "specs" / "081-acceptance-hardening"
REQUIREMENTS = SPEC / "requirements.md"

#: The seven templates' declaring ids, in table order (octets 008…014 of `## Shared Strings`).
REASON_IDS = ("STR-008", "STR-009", "STR-010", "STR-011", "STR-012", "STR-013", "STR-014")

#: Argument grammars for the five argument-taking templates (requirements § Shared Strings).
#: `<feature>:<row>` needs both halves non-empty and admits no whitespace, because the row locator
#: is written by the dependency artifact exactly as it appears there (`SC-006_status`, a `## Deferred`
#: label, …).
ARG_GRAMMAR = {
    "STR-009": r"SC-\d{3}",
    "STR-010": r"SC-\d{3}",
    "STR-011": r"RS-\d{3}",
    "STR-012": r"EP-\d{3}",
    "STR-013": r"\S+:\S+",
}

#: `final_path` is a closed count record (C-08): six status buckets plus the total.
#: `unknown` means "no status row exists"; `partial` is a *measured* status and gets its own bucket.
FINAL_PATH_KEYS = ("pass", "blocked", "deferred", "partial", "fail", "unknown", "total")

PASS_COUNT = re.compile(r"^final_path\b", re.M)


# --------------------------------------------------------------------------- #
# The closed reason set — derived from the owner, never copied
# --------------------------------------------------------------------------- #

def _templates():
    """{STR-id: template} read out of the declaring spec's Shared Strings table."""
    text = REQUIREMENTS.read_text(encoding="utf-8")
    rows = dict(re.findall(r"(?m)^\| `(STR-0\d\d)` \| `([^`]+)` \|", text))
    missing = [sid for sid in REASON_IDS if sid not in rows]
    assert not missing, "requirements.md no longer declares %r — the closed set moved" % (missing,)
    return {sid: rows[sid] for sid in REASON_IDS}


def _split(template):
    """`(prefix, argument-placeholder-or-None)` for one template.

    The instance form is `prefix + ": " + argument`, so the template splits on its FIRST `": "`
    (STR-013's placeholder itself contains a colon, which is why the split is not global).
    """
    prefix, sep, arg = template.partition(": ")
    return prefix, (arg if sep else None)


def _is_member(reason):
    """The two-part membership test: template match AND a well-formed argument.

    Deliberately grammar-based. A byte test against a table cell cannot express "an instance of
    `final-path-not-pass: SC-NNN`", and a checker whose reasons only match the cell would carry no
    argument at all.
    """
    for sid, template in _templates().items():
        prefix, arg = _split(template)
        if arg is None:
            if reason == prefix:
                return True
            continue
        if not reason.startswith(prefix + ": "):
            continue
        tail = reason[len(prefix) + 2:]
        if re.fullmatch(ARG_GRAMMAR[sid], tail):
            return True
    return False


def _instance(reason):
    """`{code, target}` → the emitted instance, `prefix + ": " + argument`.

    The payload slot is `reasons: [{code, target}]` (plan § D2). For the two argument-less
    templates `target` is empty and the instance is the code itself.
    """
    if isinstance(reason, str):
        return reason
    code = reason.get("code", "")
    target = reason.get("target") or ""
    return code if not target else "%s: %s" % (code, target)


# --------------------------------------------------------------------------- #
# Running the checker
# --------------------------------------------------------------------------- #

def _run(spec_dir, *args):
    assert CHECKER.is_file(), "closure-acceptance-check.py is missing — T006 has not landed"
    cmd = [sys.executable, str(CHECKER), "--spec-dir", str(spec_dir), *args]
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))


def _json(spec_dir, *args):
    proc = _run(spec_dir, "--json", *args)
    assert proc.stdout.strip(), "no payload on stdout:\n%s\n%s" % (proc.stdout, proc.stderr)
    return proc, json.loads(proc.stdout)


def _fixture(name):
    path = FIXTURES / name
    assert path.is_dir(), "fixture set %r is missing — T003/T004/T021 has not landed" % name
    return path


def _load_checker():
    """Import the checker by path, for the one assertion that judges a pure function.

    The filename carries hyphens, so it is not importable by name. Everything else in this
    module drives the real CLI; this hook exists only where the subject is a single
    computation that no fixture can express without inventing a file for it.
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location("closure_acceptance_check", CHECKER)
    assert spec and spec.loader, "cannot load %s" % CHECKER
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.final_path_counts


def _instances(payload):
    return [_instance(r) for r in payload.get("reasons", [])]


def _assert_schema(payload):
    """C-05/C-07/C-08/C-09: the payload's shape, independent of any one fixture."""
    assert payload["verdict"] in ("accept", "block"), payload["verdict"]
    counts = payload["final_path"]
    assert set(counts) == set(FINAL_PATH_KEYS), sorted(counts)
    assert counts["total"] == sum(counts[k] for k in FINAL_PATH_KEYS if k != "total"), counts
    reasons = _instances(payload)
    for reason in reasons:
        assert _is_member(reason), (
            "reason %r is outside the closed set — membership is template match plus a "
            "well-formed argument, not a third spelling" % reason
        )
    if payload["verdict"] == "block":
        assert reasons, "a block MUST carry at least one reason (C-09)"
    else:
        assert reasons == [], "an accept carries no blocking reason (C-07)"


# --------------------------------------------------------------------------- #
# C-07 / C-08 / C-09 — the seven fixtures
# --------------------------------------------------------------------------- #

def test_positive_accepts_and_counts_a_single_final_pass():
    """A complete feature is not over-blocked: exit 0, verdict `accept`, no reason."""
    proc, payload = _json(_fixture("positive"))
    _assert_schema(payload)
    assert proc.returncode == 0, proc.stderr
    assert payload["verdict"] == "accept", payload
    assert payload["final_path"]["total"] == 1
    assert payload["final_path"]["pass"] == 1


def test_negative_blocks_with_zero_final_path_pass():
    """The 026 shape: bookkeeping complete, main journey never measured."""
    proc, payload = _json(_fixture("negative"))
    _assert_schema(payload)
    assert proc.returncode == 1, proc.stderr
    assert payload["verdict"] == "block"
    assert payload["final_path"]["total"] == 2
    assert payload["final_path"]["pass"] == 0
    codes = [c["code"] for c in payload["reasons"]]
    assert codes == ["zero-final-path-pass"], codes


def test_ladder_mutation_blocks_with_the_ladder_reason():
    """All five ladder fields present, `reduced_measurement` non-empty with `run=no` — illegal."""
    proc, payload = _json(_fixture("ladder-mutation"))
    _assert_schema(payload)
    assert proc.returncode == 1, proc.stderr
    reasons = _instances(payload)
    assert "blocked-without-measurement-ladder: SC-001" in reasons, reasons


def test_smoke_mutation_blocks_because_the_claim_exceeds_the_evidence():
    """Claimed `Implemented` with the smoke record gone: the only fixture for this reason.

    `zero-final-path-pass` cannot fire here — every `final` SC still passes — which is exactly why
    the fixture exists: without it the claimed-but-not-accepted reason would carry no
    counter-example and could rot into dead code.
    """
    proc, payload = _json(_fixture("smoke-mutation"))
    _assert_schema(payload)
    assert proc.returncode == 1, proc.stderr
    reasons = _instances(payload)
    assert "status-claims-implemented-but-blocked" in reasons, reasons
    assert "zero-final-path-pass" not in reasons, reasons


def test_execution_without_final_blocks_with_zero_final_path_pass():
    """`execution` class with zero `final` SC: `final_path.total = 0`, and the zero-pass reason."""
    proc, payload = _json(_fixture("execution-without-final"))
    _assert_schema(payload)
    assert proc.returncode == 1, proc.stderr
    assert payload["flow_class"] == "execution", payload
    assert payload["final_path"]["total"] == 0
    assert "zero-final-path-pass" in _instances(payload), payload["reasons"]


def test_mixed_path_names_the_failing_criterion_and_not_the_zero_pass_reason():
    """One `final` pass and one `final` fail: the reason names SC-002.

    The lone non-`pass` `supporting` SC (SC-003, deferred with the full ladder) produces no reason
    of its own — promoting a supporting criterion into a blocker would make every hygiene note a
    release gate.
    """
    proc, payload = _json(_fixture("mixed-path"))
    _assert_schema(payload)
    assert proc.returncode == 1, proc.stderr
    reasons = _instances(payload)
    assert "final-path-not-pass: SC-002" in reasons, reasons
    assert "zero-final-path-pass" not in reasons, "a passing final path exists; zero-pass is wrong"
    assert not [r for r in reasons if "SC-003" in r], (
        "a non-`pass` supporting criterion MUST NOT produce a blocking reason: %r" % (reasons,)
    )


def test_expression_feature_is_not_forced_to_invent_a_final_criterion():
    """The `final`-path rule is vacuous for a declared `expression` feature.

    The class is read from the declaration, so the exemption is mechanical: the payload reports
    `final_path.total = 0` and no final-path reason appears. The verdict is not pinned beyond
    schema validity — what is pinned is that the absence of a `final` SC is not itself a refusal.
    """
    proc, payload = _json(_fixture("expr-supporting-only"))
    _assert_schema(payload)
    assert payload["flow_class"] == "expression", payload
    assert payload["final_path"]["total"] == 0
    reasons = _instances(payload)
    assert "zero-final-path-pass" not in reasons, reasons
    assert not [r for r in reasons if r.startswith("final-path-not-pass")], reasons
    assert proc.returncode == (0 if payload["verdict"] == "accept" else 1)


# --------------------------------------------------------------------------- #
# C-02 / C-10 — a missing input is exit 2, never a block
# --------------------------------------------------------------------------- #

def test_missing_spec_dir_is_exit_two(tmp_path):
    proc = _run(tmp_path / "does-not-exist")
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert proc.stderr.strip(), "an input error MUST name what was missing"


def test_missing_required_input_is_exit_two_and_never_block(tmp_path):
    """A missing artifact is a defect of the artifact, not a finding about the feature (C-02)."""
    spec_dir = tmp_path / "fixture"
    shutil.copytree(_fixture("positive"), spec_dir)
    (spec_dir / "verification.md").unlink()
    proc = _run(spec_dir, "--json")
    assert proc.returncode == 2, (
        "a missing input MUST NOT be reported as `block` (exit 1): %s%s" % (proc.stdout, proc.stderr)
    )
    assert "verification.md" in proc.stderr, proc.stderr


# --------------------------------------------------------------------------- #
# C-05 / C-08 — the human output and the counts the caller copies
# --------------------------------------------------------------------------- #

def test_human_output_carries_the_verdict_every_reason_and_the_counts():
    """C-05: the default output is the report — verdict, every reason, the final-path counts."""
    proc = _run(_fixture("mixed-path"))
    out = proc.stdout
    assert "block" in out
    assert "final-path-not-pass: SC-002" in out
    line = PASS_COUNT.search(out)
    assert line, "no `final_path` count block in the human output:\n%s" % out
    counts_line = out[line.start():].split("\n")[0]
    for key in ("pass", "blocked", "deferred", "total"):
        assert key in counts_line, "the count block omits %r: %r" % (key, counts_line)


def test_final_path_counts_are_computed_from_the_rows_not_recounted_by_the_test():
    """C-08: one computation. The values are asserted from the fixture's own recorded statuses."""
    _, payload = _json(_fixture("mixed-path"))
    counts = payload["final_path"]
    assert (counts["pass"], counts["fail"], counts["total"]) == (1, 1, 2), counts
    assert (counts["blocked"], counts["deferred"], counts["partial"], counts["unknown"]) == (
        0, 0, 0, 0,
    ), counts


def test_partial_is_its_own_bucket_and_unknown_stays_a_missing_row():
    """C-08's two easy-to-confuse buckets, judged at the unit of the count itself.

    No existing fixture carries a *`final`-path* `partial` row (the `mixed-path` fixture's
    `partial`-shaped criterion is `supporting`), and adding one would mean a new fixture file
    for a fact this level can measure directly. So the count is exercised here on the
    computation, and the end-to-end shape is covered by `_assert_schema` over the fixtures:
    `partial` must be counted as itself, never folded into `unknown` — a measured status and a
    missing measurement are different facts about the feature.
    """
    final_path_counts = _load_checker()

    counts = final_path_counts(
        {"SC-001": "final", "SC-002": "final", "SC-003": "supporting"},
        {"SC-001": ["partial"], "SC-003": ["fail"]},  # SC-002 has no status row at all
    )
    assert counts["partial"] == 1, counts
    assert counts["unknown"] == 1, counts
    assert counts["fail"] == 0, "a `supporting` criterion never enters the record: %r" % (counts,)
    assert counts["total"] == 2, counts


# --------------------------------------------------------------------------- #
# C-06 — `--waive CODE:TARGET` removes a reason and counts it as waived
# --------------------------------------------------------------------------- #

def test_waiving_the_only_reason_turns_the_verdict_and_records_the_waiver():
    _, before = _json(_fixture("negative"))
    assert [c["code"] for c in before["reasons"]] == ["zero-final-path-pass"]

    proc, after = _json(_fixture("negative"), "--waive", "zero-final-path-pass:negative")
    _assert_schema(after)
    assert after["verdict"] == "accept", (
        "a waived reason MUST be absent from the blocking set — the verdict turns: %s" % after
    )
    assert proc.returncode == 0
    waived = [_instance(w) for w in after.get("waived", [])]
    assert waived == ["zero-final-path-pass"], (
        "a waived reason MUST still be counted as waived in the summary (C-06): %r" % (after,)
    )


def test_waiving_one_final_path_reason_leaves_the_other_findings_intact():
    """A waiver removes exactly one reason; it is not a mode that silences the checker."""
    _, payload = _json(_fixture("mixed-path"), "--waive", "final-path-not-pass:SC-002")
    assert payload["verdict"] == "accept", payload
    assert [_instance(w) for w in payload.get("waived", [])] == ["final-path-not-pass: SC-002"], (
        payload.get("waived")
    )


def test_a_malformed_waiver_is_an_input_error_not_a_silent_no_op():
    """`CODE:TARGET` with a missing half is an invocation defect — exit 2, never a quiet accept."""
    proc = _run(_fixture("negative"), "--waive", "zero-final-path-pass")
    assert proc.returncode == 2, proc.stdout + proc.stderr


# --------------------------------------------------------------------------- #
# The membership test itself — it must be able to reject, or it proves nothing
# --------------------------------------------------------------------------- #

def test_membership_rejects_bare_prefixes_trailing_colons_and_malformed_arguments():
    """Anti-vacuity for the two-part test: every near-miss is outside the closed set.

    Without this, `_is_member` could be an `assert True` in disguise and every reason assertion
    above would pass on any string.
    """
    assert _is_member("final-path-not-pass: SC-002")
    assert _is_member("inherited-blocker-undisposed: 026:SC-006_status")
    assert _is_member("zero-final-path-pass")
    for outsider in (
        "final-path-not-pass",          # bare prefix of an argument-taking template
        "final-path-not-pass:",         # trailing colon, no argument
        "final-path-not-pass: SC-2",    # argument does not satisfy SC-\d{3}
        "final-path-not-pass SC-002",   # third spelling: no separator
        "zero-final-path-pass:",        # an argument-less template never takes a separator
        "zero-final-path-pass: extra",  # …nor an argument
        "total-final-path-pass",        # not in the set at all
    ):
        assert not _is_member(outsider), "%r must not be a member" % outsider


def test_the_seven_templates_are_read_from_the_declaring_specification():
    """The set is closed at seven and owned by requirements § Shared Strings, not by this file."""
    templates = _templates()
    assert len(templates) == 7, templates
    prefixes = {_split(t)[0] for t in templates.values()}
    assert prefixes == {
        "zero-final-path-pass",
        "final-path-not-pass",
        "blocked-without-measurement-ladder",
        "runtime-dependency-not-owned",
        "falsified-premise-undecided",
        "inherited-blocker-undisposed",
        "status-claims-implemented-but-blocked",
    }, sorted(prefixes)
