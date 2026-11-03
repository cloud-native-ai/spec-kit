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

Scope boundary, stated so the next slice does not read it as a defect: the **review** and **driver**
call sites are 081c / 081d work. They are asserted *absent* here, with the reason, so a half-wired
call site cannot appear silently — and so this module's own boundary is checkable rather than
implied. Those two assertions are expected to be replaced by their slices, not deleted.
"""
from __future__ import annotations

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

#: 081a scope boundary, recorded as data so the absence assertions below carry their reason.
REVIEW_DRIVER_DEFERRED = (
    "the review call site (GW-02) is 081c work and the driver closure/merge call site (GW-03) is "
    "081d work; 081a wires the implement call site only"
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
# 081a scope boundary — the other two call sites are absent, with a reason
# --------------------------------------------------------------------------- #

def test_the_review_and_driver_call_sites_are_still_unwired():
    """Asserted absent *in this slice*; 081c and 081d replace this assertion with their own.

    The reason is data (`REVIEW_DRIVER_DEFERRED`), not a comment: the review call site is 081c
    work and the driver closure/merge call site is 081d work, so 081a wires the implement call
    site only. When either slice lands, this assertion flips to its positive form — deleting it
    would restore the silent half-wiring it exists to prevent.
    """
    assert CHECKER_REL not in REVIEW_CMD.read_text(encoding="utf-8"), (
        "templates/commands/review.md now names the checker — if 081c landed, replace this "
        "boundary assertion with its positive form instead of deleting it"
    )
    if INTEGRATE_LINES.is_file():
        assert CHECKER_REL not in INTEGRATE_LINES.read_text(encoding="utf-8"), (
            "integrate-lines.py now names the checker — if 081d landed, replace this boundary "
            "assertion with its positive form instead of deleting it"
        )
    assert "081c" in REVIEW_DRIVER_DEFERRED and "081d" in REVIEW_DRIVER_DEFERRED
