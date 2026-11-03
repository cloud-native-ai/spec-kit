"""Contract tests for contracts/gate-wiring.contract.md — GW-01, GW-04 (Feature 081, T010).

Subject: the **implement call site only** of the closure verdict.

- ``skills/internal/implement-feature/SKILL.md`` **Step 9 — Pre-Status-Flip Gate and Verification Log**
  (the step where the status is actually landed, GW-01)
- ``shared/workflow/feature-integration.md`` § Pre-Status-Flip Gate

Owner of the criteria: ``shared/workflow/acceptance-hardening.md`` + `templates/feature-details-template.md`
§ Canonical Status State Machine. This contract is the **wiring map** — which surface calls which
judgement — so nothing here re-judges a feature; the assertions are about *where the call lives* and
*whether the documented invocation actually runs*.

The second half matters more than the first. A carrier that names a script is a claim; a carrier
whose documented command, extracted verbatim and pointed at the two fixtures, produces `block` /
`accept` is evidence. That is the difference the feature exists to create, so the extraction below
is deliberately mechanical — the invocation is read out of the carrier text, not retyped here.

Red-first (slice 081a, T010): the call site is wired by T016, so this module is red until then, and
its fixture runs stay red until T015 lands the verdict. The red run is recorded in
``.specify/specs/081-acceptance-hardening/notes/red-first-evidence.md`` § 1.4.

**Slice 081c (T008) flips the review half; it does not delete it.** When this module was written,
its last section asserted the **review** *and* **driver** call sites absent, because 081a wires the
implement site only. 081c lands the review site (GW-02), so that half is now asserted in its
**positive** form — the review command names the checker, treats a `block` verdict as a non-pass,
and its own documented invocation is extracted and *run* against `negative` and `positive`. What the
old assertion claimed ("`templates/commands/review.md` does not name the checker") is now false by
design; replacing it with its positive form is what keeps the boundary checkable, and deleting it
would have restored the silent half-wiring it exists to prevent.

The **driver** closure/merge call site (GW-03) is still 081d work: it stays asserted *absent* here,
with its reason kept as data (`REVIEW_DRIVER_DEFERRED`, now shrunk to the driver half alone). 081d
flips that one in the same way. The review-site assertions of this module are a *wiring* reading;
they do not re-judge a feature, and the fixture verdicts they drive are the checker's own.
"""
from __future__ import annotations

import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "internal" / "implement-feature" / "SKILL.md"
INTEGRATION = ROOT / "shared" / "workflow" / "feature-integration.md"
FIXTURES = ROOT / "tests" / "fixtures" / "acceptance-hardening"
REVIEW_CMD = ROOT / "templates" / "commands" / "review.md"
IMPLEMENT_CMD = ROOT / "templates" / "commands" / "implement.md"
INTEGRATE_LINES = ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "integrate-lines.py"
OWNER_DOC = "shared/workflow/acceptance-hardening.md"

CHECKER_REL = "scripts/python/closure-acceptance-check.py"

#: The documented invocation, extracted rather than retyped: `python3 <checker> …` on one line.
INVOCATION = re.compile(r"python3\s+%s[^\n`]*" % re.escape(CHECKER_REL))

#: Scripts that answer *other* questions. Naming one of them as the closure judge inside the gate
#: would be a second judgement source (GW-04), so their absence from the gate's own sentences is
#: part of the wiring assertion.
OTHER_JUDGES = ("validate-requirements.py", "pre-analyze-check.py", "validate-tasks.py")

#: The 081d scope boundary, recorded as data so the remaining absence assertion carries its
#: reason. 081c (T008) moved the review half to its positive form below; this datum therefore
#: names the **driver** call site only.
REVIEW_DRIVER_DEFERRED = (
    "the driver closure/merge call site (GW-03) is 081d work; 081a wires the implement call "
    "site and 081c (this module's own slice) wires the review call site"
)


def _step9():
    text = SKILL.read_text(encoding="utf-8")
    start = re.search(r"(?m)^###\s+Step 9\b[^\n]*$", text)
    assert start, "implement-feature/SKILL.md no longer carries `### Step 9 — …`"
    tail = text[start.end():]
    nxt = re.search(r"(?m)^#{2,3}\s", tail)
    return tail[: nxt.start()] if nxt else tail


def _pre_status_flip():
    text = INTEGRATION.read_text(encoding="utf-8")
    start = re.search(r"(?m)^##\s+Pre-Status-Flip Gate[^\n]*$", text)
    assert start, "feature-integration.md no longer carries § Pre-Status-Flip Gate"
    tail = text[start.end():]
    nxt = re.search(r"(?m)^##\s", tail)
    return tail[: nxt.start()] if nxt else tail


def _invocation(section, where):
    match = INVOCATION.search(section)
    assert match, (
        "%s must name the closure checker invocation `python3 %s --spec-dir <dir>` — a gate that "
        "names no runnable command leaves the judgement to whoever reads it (GW-01/GW-04)"
        % (where, CHECKER_REL)
    )
    return match.group(0).strip()


def _run_invocation(invocation, spec_dir):
    """Run the carrier's own command line against a fixture directory."""
    argv = shlex.split(invocation)
    assert argv and argv[0].startswith("python3"), argv
    if "--spec-dir" in argv:
        argv[argv.index("--spec-dir") + 1] = str(spec_dir)
    else:
        argv += ["--spec-dir", str(spec_dir)]
    proc = subprocess.run([sys.executable] + argv[1:], capture_output=True, text=True,
                          cwd=str(ROOT))
    return proc


# --------------------------------------------------------------------------- #
# GW-01 — the two implement-side carriers name the invocation
# --------------------------------------------------------------------------- #

def test_step_9_names_the_closure_checker_invocation():
    """Step 9 is the status-landing step; a judgement that runs elsewhere can be skipped."""
    section = _step9()
    assert CHECKER_REL in section, section[:400]
    _invocation(section, "implement-feature/SKILL.md Step 9")


def test_the_pre_status_flip_gate_names_the_closure_checker_invocation():
    section = _pre_status_flip()
    assert CHECKER_REL in section, section[:400]
    _invocation(section, "feature-integration.md § Pre-Status-Flip Gate")


def test_both_carriers_point_at_the_owner_and_restate_no_criteria():
    """One definition point: the carriers call, the owner defines (GW-01's second sentence)."""
    for name, section in (("Step 9", _step9()), ("§ Pre-Status-Flip Gate", _pre_status_flip())):
        assert OWNER_DOC in section, "%s must reach the criteria by path: %r" % (name, section[:300])
        assert not re.search(r"(?i)four conjunctive", section), (
            "%s restates the four conditions; it must point at the owner's block instead" % name
        )


# --------------------------------------------------------------------------- #
# GW-01 — `block` lands `Blocked`, never `Implemented`
# --------------------------------------------------------------------------- #

def test_a_block_lands_blocked_and_never_implemented():
    for name, section in (("Step 9", _step9()), ("§ Pre-Status-Flip Gate", _pre_status_flip())):
        assert re.search(r"`?Blocked`?", section), (
            "%s must name the status it lands on `block`" % name
        )
        assert re.search(r"(?i)MUST NOT[^.]*\bImplemented\b", section), (
            "%s must forbid writing `Implemented` on a `block` — the zero-final-pass "
            "`Implemented` is the exact hole this feature closes" % name
        )


# --------------------------------------------------------------------------- #
# GW-01 — the command template the operator actually runs says the same thing
# --------------------------------------------------------------------------- #

def _feature_integration_section():
    """`templates/commands/implement.md` § Feature Integration — the flip's home."""
    text = IMPLEMENT_CMD.read_text(encoding="utf-8")
    start = re.search(r"(?m)^##\s+Feature Integration\s*$", text)
    assert start, "templates/commands/implement.md no longer carries § Feature Integration"
    tail = text[start.end():]
    nxt = re.search(r"(?m)^##\s", tail)
    return tail[: nxt.start()] if nxt else tail


def test_the_implement_command_template_names_the_checker_and_the_blocked_landing():
    """The command surface must not be silently unwired.

    Steps 9 and § Pre-Status-Flip Gate are the *procedure*; this template is the
    *invocation* an operator hands the model.  A line that only exists in a skill
    the command delegates to can be dropped from the command's own story without
    any assertion noticing, so it is pinned here: delete the bullet and this test
    goes red.

    Placement is part of the assertion: the bullet MUST live in
    § Feature Integration (where the `Planned → Implemented` transition is owned),
    not inside the 077 class-read card (`### 类别读取与文档型门禁`), which owns a
    different question — one document, one feature.
    """
    section = _feature_integration_section()
    assert CHECKER_REL in section, (
        "templates/commands/implement.md § Feature Integration must name "
        "`%s` — the flip's closure judgement is not optional at this surface:\n%s"
        % (CHECKER_REL, section)
    )
    assert re.search(r"`?Blocked`?", section), (
        "§ Feature Integration must name the status a `block` lands — `Blocked`: %r" % section
    )
    assert re.search(r"(?i)MUST NOT[^.]*\bImplemented\b", section), (
        "§ Feature Integration must forbid writing `Implemented` on a `block` — the "
        "zero-final-pass `Implemented` is the hole this feature closes: %r" % section
    )
    assert OWNER_DOC in section, (
        "§ Feature Integration must reach the verdict's criteria by path (one owner, "
        "no restatement): %r" % section
    )
    # The wiring card belongs to Feature 077 and answers the class-read question.
    # A 081 gate line inside it would make the card own two unrelated obligations —
    # and would silently move the card's stripped bytes (C-007 of Feature 077).
    card_start = re.search(r"(?m)^###\s+类别读取与文档型门禁\s*$", IMPLEMENT_CMD.read_text(encoding="utf-8"))
    if card_start:
        tail = IMPLEMENT_CMD.read_text(encoding="utf-8")[card_start.end():]
        nxt = re.search(r"(?m)^#{1,3}\s", tail)
        card = tail[: nxt.start()] if nxt else tail
        assert CHECKER_REL not in card, (
            "the 081 closure gate line is back inside the 077 class-read card — it "
            "belongs to § Feature Integration (the semantic home); one document must "
            "not own two features"
        )


# --------------------------------------------------------------------------- #
# GW-04 — no second judgement source in either carrier
# --------------------------------------------------------------------------- #

def test_no_second_judgement_source_is_offered():
    for name, section in (("Step 9", _step9()), ("§ Pre-Status-Flip Gate", _pre_status_flip())):
        for other in OTHER_JUDGES:
            assert other not in section, (
                "%s offers %r as a closure judge; the verdict has exactly one source (GW-04)"
                % (name, other)
            )
        assert re.search(r"(?i)MUST NOT[^.]*(model|judgement|another script)", section), (
            "%s must forbid substituting a model judgement or a second script for the checker"
            % name
        )


# --------------------------------------------------------------------------- #
# The extraction must execute — a carrier's command is a claim until it runs
# --------------------------------------------------------------------------- #

def test_the_documented_invocation_blocks_the_negative_fixture():
    invocation = _invocation(_step9(), "implement-feature/SKILL.md Step 9")
    fixture = FIXTURES / "negative"
    assert fixture.is_dir(), "the negative fixture is missing — T003 has not landed"
    proc = _run_invocation(invocation, fixture)
    assert proc.returncode == 1, (
        "the carrier's own invocation, run against the 026-shape fixture, must block "
        "(exit 1):\nstdout:\n%s\nstderr:\n%s" % (proc.stdout, proc.stderr)
    )
    assert "zero-final-path-pass" in (proc.stdout + proc.stderr), (
        "the block must carry its named reason:\n%s%s" % (proc.stdout, proc.stderr)
    )


def test_the_documented_invocation_accepts_the_positive_fixture():
    invocation = _invocation(_pre_status_flip(), "feature-integration.md § Pre-Status-Flip Gate")
    fixture = FIXTURES / "positive"
    assert fixture.is_dir(), "the positive fixture is missing — T003 has not landed"
    proc = _run_invocation(invocation, fixture)
    assert proc.returncode == 0, (
        "a complete feature must not be blocked by the wired gate:\nstdout:\n%s\nstderr:\n%s"
        % (proc.stdout, proc.stderr)
    )


# --------------------------------------------------------------------------- #
# 081c / GW-02 — the review call site, now wired (T008 flipped this half)
# --------------------------------------------------------------------------- #

def _arc_section():
    """`templates/commands/review.md` § The Acceptance Reality Check — the review site."""
    text = REVIEW_CMD.read_text(encoding="utf-8")
    start = re.search(r"(?m)^##\s+The Acceptance Reality Check\s*$", text)
    assert start, (
        "templates/commands/review.md no longer carries § The Acceptance Reality Check — the "
        "review call site has no home left"
    )
    tail = text[start.end():]
    nxt = re.search(r"(?m)^##\s", tail)
    return tail[: nxt.start()] if nxt else tail


def _sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text)) if s.strip()]


def _closed_reason_codes():
    """The checker's own closed reason set — read from its code, not copied here.

    The owner is `scripts/python/closure-acceptance-check.py` (`REASON_CODES`, whose seven
    literals `requirements.md` § Shared Strings names STR-008…STR-014). Importing it keeps this
    module from becoming a second spelling of the set: an eighth code added there is admitted
    here automatically, and a reason the checker invents is outside it by construction.
    """
    import importlib.util

    checker = ROOT / CHECKER_REL
    spec = importlib.util.spec_from_file_location("closure_acceptance_check", checker)
    assert spec and spec.loader, "cannot load %s" % checker
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return tuple(module.REASON_CODES)


def test_the_review_call_site_names_the_closure_checker():
    """GW-02: the review site runs the verdict, so it must name the one program that owns it.

    This replaces 081a's absence assertion (`CHECKER_REL not in review.md`), which was true only
    while the review site was unwired. It stayed a *wiring* assertion: naming the script is the
    claim, and the two fixture runs below are the evidence.
    """
    section = _arc_section()
    assert CHECKER_REL in section, (
        "templates/commands/review.md § The Acceptance Reality Check must name `%s` — the review "
        "site's closure judgement is not optional (GW-02):\n%s" % (CHECKER_REL, section)
    )
    _invocation(section, "templates/commands/review.md § The Acceptance Reality Check")


def test_the_review_call_site_treats_block_as_a_non_pass():
    """GW-02's second limb: `block` refuses the transition; it is never a caveat to carry.

    A call site that names the checker and then reads a `block` verdict as advisory is the
    half-wiring this contract exists to catch, so the sentence that mentions `block` must carry
    both the non-pass label and the refusal — the two together are the obligation, and either
    alone would pass a site that only quotes the vocabulary.
    """
    section = _arc_section()
    mentioning = [s for s in _sentences(section) if re.search(r"`block`", s)]
    assert mentioning, (
        "§ The Acceptance Reality Check must name the checker's `block` verdict literal — a site "
        "that never names it cannot have decided what to do with it (GW-02):\n%s" % section
    )
    joined = " ".join(mentioning).lower()
    assert "non-pass" in joined, (
        "the `block` verdict must be stated as a **non-pass**; found: %r" % (mentioning,)
    )
    assert "refus" in joined, (
        "a `block` verdict must refuse the transition, naming the failed condition (GW-02); "
        "found: %r" % (mentioning,)
    )
    flat = re.sub(r"\s+", " ", section)
    assert "F-ACCEPTANCE" in flat and re.search(r"`P0`", flat), (
        "the refusal path must still name the fixed item `F-ACCEPTANCE` at `P0` (RC-15):\n%s"
        % section
    )


def test_the_review_call_sites_own_invocation_blocks_the_negative_fixture():
    """The review site's documented command, extracted verbatim and run: it must refuse.

    Extraction rather than a retyped command line is the point — a carrier whose command is only
    quoted can drift from the one that runs, and no assertion would notice.
    """
    invocation = _invocation(_arc_section(), "templates/commands/review.md ARC")
    fixture = FIXTURES / "negative"
    assert fixture.is_dir(), "the negative fixture is missing — T003 has not landed"
    proc = _run_invocation(invocation, fixture)
    assert proc.returncode == 1, (
        "the review site's own invocation, run against the 026-shape fixture, must refuse "
        "(exit 1):\nstdout:\n%s\nstderr:\n%s" % (proc.stdout, proc.stderr)
    )
    payload = json.loads(proc.stdout) if proc.stdout.strip().startswith("{") else {}
    codes = [r.get("code", "") for r in payload.get("reasons", [])]
    assert codes, (
        "the refusal must carry at least one named reason (GW-02: 'with a named condition'):\n%s"
        % (proc.stdout or proc.stderr)
    )
    outside = [code for code in codes if code not in _closed_reason_codes()]
    assert not outside, (
        "the refusal reasons %r are outside the checker's closed set %r — a call site that "
        "accepts an invented reason is not reading the owner's verdict (GW-04)"
        % (outside, list(_closed_reason_codes()))
    )
    assert payload.get("verdict") == "block", (
        "the review site's run must report the `block` verdict it treats as a non-pass; "
        "measured %r" % (payload.get("verdict"),)
    )


def test_the_review_call_sites_own_invocation_accepts_the_positive_fixture():
    invocation = _invocation(_arc_section(), "templates/commands/review.md ARC")
    fixture = FIXTURES / "positive"
    assert fixture.is_dir(), "the positive fixture is missing — T003 has not landed"
    proc = _run_invocation(invocation, fixture)
    assert proc.returncode == 0, (
        "a complete feature must not be refused by the wired review site:\nstdout:\n%s\n"
        "stderr:\n%s" % (proc.stdout, proc.stderr)
    )


def test_the_review_call_site_offers_no_second_judgement_source():
    """GW-04 at the review site: the checker is the verdict; no sibling script, no model call."""
    section = _arc_section()
    for other in OTHER_JUDGES:
        assert other not in section, (
            "§ The Acceptance Reality Check offers %r as a closure judge; the verdict has exactly "
            "one source (GW-04)" % other
        )
    flat = re.sub(r"\s+", " ", section)
    assert re.search(r"(?i)(no model judgement|MUST NOT)", flat), (
        "the review site must forbid substituting a model judgement for the checker (GW-04):"
        "\n%s" % section
    )


# --------------------------------------------------------------------------- #
# 081d scope boundary — the driver call site is absent, with its reason
# --------------------------------------------------------------------------- #

def test_the_driver_call_site_is_still_unwired():
    """Asserted absent *in 081c*; 081d replaces this assertion with its own.

    What moved in 081c: the review half of this boundary became the positive assertions above,
    because 081c wired that call site (GW-02). What did not move: the driver closure/merge call
    site is still 081d's (GW-03), so it stays asserted absent — deleting the assertion would
    restore the silent half-wiring it exists to prevent. The reason is data
    (`REVIEW_DRIVER_DEFERRED`), not a comment.
    """
    if INTEGRATE_LINES.is_file():
        assert CHECKER_REL not in INTEGRATE_LINES.read_text(encoding="utf-8"), (
            "integrate-lines.py now names the checker — if 081d landed, replace this boundary "
            "assertion with its positive form instead of deleting it"
        )
    assert "081d" in REVIEW_DRIVER_DEFERRED and "GW-03" in REVIEW_DRIVER_DEFERRED, (
        "the deferred datum must name the slice and the clause that own the driver call site, "
        "so the absence above reads as a boundary rather than as an oversight"
    )
