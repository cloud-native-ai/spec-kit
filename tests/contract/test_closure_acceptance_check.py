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
``audit-history`` audit root: registry + two spec dirs (901 blocked-shaped,   audit reports 901, writes
                 902 clean), both claimed ``Implemented``                     nothing, exit 0
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


# --------------------------------------------------------------------------- #
# C-02 / C-04 / C-10 / C-11 / C-12 — the read-only audit mode (081d, T011/T013)
#
# The mode's input is a repository root (`--repo`), not a spec directory: it enumerates the
# `Implemented`-family rows of `<root>/.specify/memory/features.md` and judges each against the
# spec directory that row's own `Spec Path` cell names. `audit-history` is the corpus's only
# audit-root case — a registry plus `.specify/specs/<key>/` directories inside the case — which is
# exactly the shape that makes the mode's zero-write assertion testable (a flat spec-dir case
# cannot be enumerated).
#
# Red before T013 closed: the checker exited `2` with the explicit not-implemented message
# (`ModeNotImplemented`), recorded in slice 081d's red-first evidence reading (b).
# --------------------------------------------------------------------------- #

AUDIT_ROOT = FIXTURES / "audit-history"


def _run_audit(*args):
    """Run the checker in audit mode against `--repo` — never passing `--spec-dir`.

    C-02 rejects `--spec-dir` in audit mode, so a helper that routed every call through
    `_run(spec_dir, …)` would be unable to express the mode's real invocation shape; the one
    leg that passes the flag does so explicitly and expects the refusal.
    """
    assert CHECKER.is_file(), "closure-acceptance-check.py is missing"
    cmd = [sys.executable, str(CHECKER), "--audit-existing", *args]
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))


def _run_audit_json(*args):
    proc = _run_audit("--json", *args)
    assert proc.stdout.strip(), "no audit payload on stdout:\n%s\n%s" % (proc.stdout, proc.stderr)
    return proc, json.loads(proc.stdout)


def _audit_features(payload):
    """`{feature-id: row}` of the payload's per-feature audit records."""
    return {row["feature"]: row for row in payload["features"]}


def _tree_hash(root):
    """`{relative path: sha256}` over every file under `root` — the C-11 subject that can break."""
    import hashlib

    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def test_audit_writes_nothing(tmp_path):
    """C-11, under the contract's own test name: the audit reports and writes nothing.

    Two subjects, because neither alone proves the whole claim. The **fixture copy** under
    `tmp_path` is a tree an implementation actually could modify — a recursive content hash before
    and after the run fails the moment the audit caches, locks, or rewrites anything under the
    root it reads. The **`git status --porcelain`** pair is C-11's named verification, observed
    over the repository this test runs in: it is attributed to the tree it actually observes (the
    checkout), which is why the copy lives outside it — the fixture and the status read never
    share a root, so neither assertion silently stands in for the other.
    """
    case = tmp_path / "audit-history"
    shutil.copytree(AUDIT_ROOT, case)
    before_hash = _tree_hash(case)
    before_status = subprocess.run(
        ["git", "status", "--porcelain"], cwd=str(ROOT), capture_output=True, text=True
    ).stdout

    proc = _run_audit("--repo", str(case))

    after_hash = _tree_hash(case)
    after_status = subprocess.run(
        ["git", "status", "--porcelain"], cwd=str(ROOT), capture_output=True, text=True
    ).stdout

    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert before_hash == after_hash, (
        "the audit modified the tree it read; differing paths: %r"
        % sorted(k for k in set(before_hash) | set(after_hash)
                 if before_hash.get(k) != after_hash.get(k))
    )
    assert before_status == after_status, (
        "C-11's named verification moved: git status --porcelain changed across the audit run"
    )


def test_audit_reports_the_affected_feature_with_claim_verdict_and_every_reason():
    """C-12: the list is readable without re-running the checker.

    901 is the case's would-become-`Blocked` subject: its claim (`Implemented`) exceeds its
    evidence under the new rules, so the report carries the claimed status, the computed verdict
    and **every** reason — the zero-pass refusal and the claim-exceeds-evidence refusal, both —
    rather than a count or a single representative line.
    """
    proc, payload = _run_audit_json("--repo", str(AUDIT_ROOT))
    assert proc.returncode == 0, proc.stderr
    rows = _audit_features(payload)
    blocked = rows["901"]
    assert blocked["claimed_status"] == "Implemented", blocked
    assert blocked["verdict"] == "block", blocked
    instances = sorted(_instance(r) for r in blocked["reasons"])
    assert instances == [
        "status-claims-implemented-but-blocked",
        "zero-final-path-pass",
    ], instances
    # the human report carries the same facts — C-12 governs the output, not only the payload
    human = _run_audit("--repo", str(AUDIT_ROOT)).stdout
    assert "901" in human and "Implemented" in human and "block" in human
    assert "zero-final-path-pass" in human and "status-claims-implemented-but-blocked" in human


def test_audit_reports_only_affected_features_and_exits_zero_despite_the_finding():
    """C-10: findings do not change the exit code — 0 whenever the inputs parse.

    902 is the case's unaffected subject: the same `Implemented` claim, but with the evidence the
    rules demand, so the audit judges it `accept`. An audit that reported every enumerated row, or
    one that turned a finding into a non-zero exit, would be a verdict engine wearing an audit's
    name — the mode's exit code reflects input validity only.
    """
    proc, payload = _run_audit_json("--repo", str(AUDIT_ROOT))
    rows = _audit_features(payload)
    clean = rows["902"]
    assert clean["verdict"] == "accept", clean
    assert clean["reasons"] == [], clean
    assert payload["summary"]["affected"] == 1, payload["summary"]
    assert payload["summary"]["judged"] == 2, payload["summary"]
    assert proc.returncode == 0, (
        "an audit's exit code reflects input validity only (C-10): a reported finding MUST NOT "
        "turn it non-zero: %s%s" % (proc.stdout, proc.stderr)
    )


def test_audit_rejects_spec_dir_and_names_the_flag():
    """C-02: `--spec-dir` is refused in audit mode — naming the flag, never silently ignored.

    The mode check comes first and is its own branch: an audit invocation that named a spec
    directory must learn that the flag is not an audit input, not be told that some spec
    directory is missing. That ordering is why this leg passes a spec directory that does not
    exist at all — if the checker reported the missing directory instead, it would have applied
    the single-feature branch's rule to an audit invocation.
    """
    proc = _run_audit("--repo", str(AUDIT_ROOT), "--spec-dir", "/no-such-spec-dir-for-audit-mode")
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "--spec-dir" in proc.stderr, proc.stderr
    assert "not an audit" in proc.stderr or "audit" in proc.stderr, proc.stderr


def test_audit_exit_two_is_reserved_for_missing_or_unparsable_input(tmp_path):
    """C-10's other half: the mode's non-zero exits are input failures, never verdicts."""
    missing_root = tmp_path / "not-a-repo"
    proc = _run_audit("--repo", str(missing_root))
    assert proc.returncode == 2, proc.stdout + proc.stderr

    empty_root = tmp_path / "empty-repo"
    (empty_root / ".specify" / "memory").mkdir(parents=True)
    proc = _run_audit("--repo", str(empty_root))
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "features.md" in proc.stderr, (
        "the refusal must name the registry the audit could not find: %s" % proc.stderr
    )

    unparsable = tmp_path / "unparsable-repo"
    (unparsable / ".specify" / "memory").mkdir(parents=True)
    (unparsable / ".specify" / "memory" / "features.md").write_text(
        "| ID | Name |\n|----|------|\n| 901 | no Status column |", encoding="utf-8"
    )
    proc = _run_audit("--repo", str(unparsable))
    assert proc.returncode == 2, proc.stdout + proc.stderr


def test_audit_skips_a_row_whose_spec_path_names_nothing_without_leaving_the_mode(tmp_path):
    """A registry row that claims `Implemented` but names no spec dir is reported, not obeyed.

    The real registry carries such rows (a feature implemented before the `Spec Path` column
    existed). Turning one into an input error would end the audit of an entire repository over a
    fact about a single row; silently skipping it would be the false green C-02 exists to remove.
    The audit reports the row as not judged, with the reason, and keeps exit 0.
    """
    case = tmp_path / "audit-history"
    shutil.copytree(AUDIT_ROOT, case)
    registry = case / ".specify" / "memory" / "features.md"
    registry.write_text(
        registry.read_text(encoding="utf-8").replace(
            ".specify/specs/901-audit-blocked/requirements.md", "-"
        ),
        encoding="utf-8",
    )
    proc, payload = _run_audit_json("--repo", str(case))
    assert proc.returncode == 0, proc.stdout + proc.stderr
    rows = _audit_features(payload)
    assert rows["901"]["verdict"] is None, rows["901"]
    assert "Spec Path" in rows["901"]["detail"], rows["901"]
    assert payload["summary"]["not_judgeable"] == 1, payload["summary"]
