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

The **driver** closure/merge call site (GW-03) is wired here too (slice 081d, T007), in the same
positive form and for the same reason: its absence assertion (`test_the_driver_call_site_is_still_
unwired`) was true only while the site was unwired, and 081d replaced it — not deleted it. The
driver half asserts the checker as the **default** gate through the existing `--gate-cmd` hook, and
its evidence is a verdict, not a string match: the two fixtures are run through the command the
script builds, and two real git worktrees show what a `block` and an input error do to the line.
The review-site assertions of this module are a *wiring* reading; they do not re-judge a feature,
and the fixture verdicts they drive are the checker's own.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from fixtures.line_fixtures import engine_json, make_line_id, make_run_id

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
# 081d / GW-03 — the driver call site, now wired (T007 replaced the absence half)
# --------------------------------------------------------------------------- #

DRIVER_CALL_SITE = "the driver closure/merge call site (`integrate-lines.py`)"
INTEGRATION_RECORD_REASONS = ("closure-blocked", "closure-input-error", "quality-gate")


def _integrate_module():
    """Load the driver's coordinator by path — no package import, one engine file."""
    spec = importlib.util.spec_from_file_location("integrate_lines_081", INTEGRATE_LINES)
    assert spec and spec.loader, "cannot load %s" % INTEGRATE_LINES
    module = importlib.util.module_from_spec(spec)
    sys.modules["integrate_lines_081"] = module
    spec.loader.exec_module(module)
    return module


def test_the_driver_call_site_names_the_closure_checker_as_its_default_gate():
    """GW-03: the closure/merge step defaults its quality gate to the checker.

    The absence assertion this replaces (`test_the_driver_call_site_is_still_unwired`) was true
    only while the site was unwired — the same move 081c made for the review half, and the same
    reason: replacing it keeps the boundary checkable, deleting it would have restored the silent
    half-wiring it exists to prevent.
    """
    source = INTEGRATE_LINES.read_text(encoding="utf-8")
    assert CHECKER_REL in source, (
        "integrate-lines.py must name `%s` as the gate it runs at the feature line's closure "
        "(GW-03): a gate that names no runnable command leaves the judgement to whoever reads it"
        % CHECKER_REL
    )
    engine = _integrate_module()
    assert engine.CHECKER_REL == CHECKER_REL, (
        "the built command and this contract must name the checker by the same relative path"
    )
    for other in OTHER_JUDGES:
        assert other not in source, (
            "%s offers %r as a closure judge; the verdict has exactly one source (GW-04)"
            % (DRIVER_CALL_SITE, other)
        )


def test_the_default_gate_runs_through_the_single_existing_hook():
    """GW-04: one gate execution, reached through `--gate-cmd` — never a second code path.

    Two readings, both mechanical: the script has exactly one `bash -c <gate>` execution site (so
    an override and the default travel the same path), and the default is *built* into that site
    rather than branched around it — an override is honoured and the built default is simply what
    `--gate-cmd` was empty.
    """
    source = INTEGRATE_LINES.read_text(encoding="utf-8")
    assert len(re.findall(r'run\(\["bash", "-c",\s*gate_cmd\]', source)) == 1, (
        "the driver must keep exactly one gate execution site; a second one is the second code "
        "path GW-03 forbids:\n%s" % source[-2000:]
    )
    assert '--gate-cmd' in source, "the existing hook must stay the only way to override the gate"
    engine = _integrate_module()
    assert callable(engine.build_gate_cmd) and callable(engine.resolve_spec_dir), (
        "the default gate must be built by the module (so this contract can run the exact "
        "command), not inlined as a second spell of the checker invocation"
    )
    # The timing obligation's carrier is the doc surface (T009), but the code side is checkable
    # the same way: the gate is resolved per *line*, and no slice-level switch exists on the
    # calling surface.
    flags = set(re.findall(r'add_argument\(\s*"(--[a-z0-9-]+)"', source))
    assert not [flag for flag in flags if "slice" in flag], (
        "the driver must not expose a slice-scoped switch: the judgement runs at the feature "
        "line's closure, and slice merges are the review gate's (GW-03); got %r" % flags
    )


def test_the_built_gate_command_blocks_the_negative_fixture():
    """The command the script builds, run verbatim against the 026-shape fixture: it must block."""
    engine = _integrate_module()
    fixture = FIXTURES / "negative"
    assert fixture.is_dir(), "the negative fixture is missing — T003 has not landed"
    cmd = engine.build_gate_cmd(ROOT, fixture)
    assert CHECKER_REL in cmd, "the built command must be the checker invocation: %r" % cmd
    proc = subprocess.run(["bash", "-c", cmd], cwd=str(ROOT), capture_output=True, text=True)
    assert proc.returncode == 1, (
        "the built gate, run against the 026-shape fixture, must block (exit 1):\n%s\n%s"
        % (proc.stdout, proc.stderr)
    )
    assert "zero-final-path-pass" in (proc.stdout + proc.stderr), proc.stdout + proc.stderr


def test_the_built_gate_command_accepts_the_positive_fixture():
    engine = _integrate_module()
    fixture = FIXTURES / "positive"
    assert fixture.is_dir(), "the positive fixture is missing — T003 has not landed"
    cmd = engine.build_gate_cmd(ROOT, fixture)
    proc = subprocess.run(["bash", "-c", cmd], cwd=str(ROOT), capture_output=True, text=True)
    assert proc.returncode == 0, (
        "a complete feature must not be blocked by the wired gate:\n%s\n%s"
        % (proc.stdout, proc.stderr)
    )


# --- the verdict half: a real line, a real worktree, the recorded result -------------------- #

FEATURES_HEADER = (
    "| ID | Name | Description | Status | Feature Details | Spec Path | Last Updated |\n"
    "|----|------|-------------|--------|-----------------|-----------|--------------|\n"
)


def _features_md(rows: list[tuple[str, str]]) -> str:
    body = "".join(
        "| %s | fixture | fixture feature | Planned | .specify/memory/features/%s.md | %s | 2026-11-03 |\n"
        % (fid, fid, cell)
        for fid, cell in rows
    )
    return "# features\n\n## Features\n\n" + FEATURES_HEADER + body


def _make_line_repo(tmp_path: Path, name: str, branch: str, *, spec_cell: str,
                    fixture: str | None, features_rows: list[tuple[str, str]] | None = None):
    """A trunk repo plus a worktree on `branch` carrying exactly the gate's inputs.

    The worktree is a real git worktree (the coordinator rebases before the gate) whose tree
    carries the checker, the feature registry and — when a fixture is named — a copy of that
    fixture's spec directory. Nothing here is the real repository.
    """
    repo = tmp_path / ("repo-" + name)
    repo.mkdir()
    for args in (["git", "init", "-q", "-b", "main", str(repo)],
                 ["git", "-C", str(repo), "config", "user.email", "t@example.com"],
                 ["git", "-C", str(repo), "config", "user.name", "T"],
                 ["git", "-C", str(repo), "commit", "-q", "--allow-empty", "-m", "base"]):
        subprocess.run(args, check=True)
    wt = tmp_path / ("wt-" + name)
    subprocess.run(["git", "-C", str(repo), "worktree", "add", "-q", "-b", branch, str(wt), "main"],
           check=True)
    (wt / "scripts" / "python").mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / CHECKER_REL, wt / CHECKER_REL)
    (wt / ".specify" / "memory").mkdir(parents=True, exist_ok=True)
    (wt / ".specify" / "memory" / "features.md").write_text(
        _features_md(features_rows or [("081", spec_cell)]), encoding="utf-8")
    if fixture is not None:
        spec_dir = wt / Path(spec_cell).parent
        shutil.copytree(FIXTURES / fixture, spec_dir)
    for args in (["git", "-C", str(wt), "add", "-A"],
                 ["git", "-C", str(wt), "commit", "-q", "-m", "gate inputs"]):
        subprocess.run(args, check=True)
    return repo, wt


def _register_line(reg: Path, repo: Path, wt: Path, branch: str) -> str:
    line_id = make_line_id(slug="line081")
    engine_json("register", "--line-id", line_id, "--run-id", make_run_id(),
                "--project-dir", str(repo), "--repo-root", str(repo),
                "--worktree-path", str(wt), "--branch", branch, reg=reg)
    engine_json("update", "--line-id", line_id, "--state", "completed", reg=reg)
    engine_json("integration-enqueue", "--line-id", line_id, reg=reg)
    return line_id


def _run_integrator(tmp_path: Path, repo: Path, reg: Path, line_id: str | None):
    env = os.environ.copy()
    env["SPECIFY_LINE_REGISTRY_DIR"] = str(reg)
    proc = subprocess.run(
        [sys.executable, str(INTEGRATE_LINES), "--repo", str(repo), "--trunk", "main",
         "--registry", str(reg), "--archive", str(tmp_path / "archive")]
        + (["--lines", line_id] if line_id else []),
        capture_output=True, text=True, env=env,
    )
    assert proc.stdout.strip().startswith("{"), (
        "the coordinator must print its JSON summary:\n%s%s" % (proc.stdout, proc.stderr)
    )
    return proc, json.loads(proc.stdout)


def _result_for(summary: dict, line_id: str) -> dict:
    rows = [row for row in summary["results"] if row["line_id"] == line_id]
    assert rows, "the summary lost line %s: %r" % (line_id, summary)
    return rows[0]


def _stored_entry(reg: Path, line_id: str) -> dict:
    return json.loads((reg / f"{line_id}.json").read_text(encoding="utf-8"))


def test_a_block_lands_blocked_after_the_record(tmp_path):
    """GW-03's verdict, on a real line: the failed result is recorded, then the line lands blocked.

    GATE-5 reads this leg: the gate is the default (no `--gate-cmd` given), the fixture blocks,
    the line carries `integration_result.status=failed` with the `closure-blocked` reason, its
    state is `blocked` — and no `--result merged` follows, because a `blocked` line is
    structurally out of the integration queue (A6 item 5).
    """
    repo, wt = _make_line_repo(tmp_path, "neg", "081-neg",
                               spec_cell=".specify/specs/081-neg/requirements.md", fixture="negative")
    reg = tmp_path / "reg"
    reg.mkdir()
    line_id = _register_line(reg, repo, wt, "081-neg")
    proc, summary = _run_integrator(tmp_path, repo, reg, line_id)

    assert proc.returncode != 0, "a blocked feature must refuse the merge:\n%s" % proc.stdout
    row = _result_for(summary, line_id)
    assert row["status"] == "failed" and row["reason"] == "closure-blocked", (
        "the block must be recorded with the closure reason, not the override's `quality-gate`: "
        "%r" % (row,)
    )
    assert "zero-final-path-pass" in row.get("detail", ""), (
        "the recorded refusal must name what failed, not merely that it failed: %r" % (row,)
    )
    entry = _stored_entry(reg, line_id)
    assert entry["state"] == "blocked", "the line must land `blocked`; got %r" % entry["state"]
    assert entry["blocked_reason"] == "closure-blocked", entry
    assert entry["integration_result"]["status"] == "failed", entry["integration_result"]
    assert entry["integration_result"]["reason"] == "closure-blocked", entry["integration_result"]
    assert not entry.get("merge_ready"), "the recorded failure clears merge_ready before the flip"
    # The order is a constraint, and both halves together prove it: the result exists *and* the
    # line is blocked, which only the record-then-transition order can reach (A6 item 5 keeps
    # `integration-record` unreachable from `blocked`).
    queued = engine_json("integration-plan", reg=reg)
    assert line_id not in [row["line_id"] for row in queued], (
        "the blocked line must be out of the queue — no `--result merged` follows a block"
    )


def test_an_input_error_refuses_the_merge_and_leaves_the_state_completed(tmp_path):
    """GW-03's exit-2 limb, on a real line: input error ≠ quality failure.

    The spec directory exists but is missing a required input, so the checker itself exits 2. The
    driver records `closure-input-error` while the line is still `completed`, leaves the state
    alone, and refuses the merge.
    """
    repo, wt = _make_line_repo(tmp_path, "inp", "082-inp",
                               spec_cell=".specify/specs/082-inp/requirements.md", fixture="negative")
    (wt / ".specify" / "specs" / "082-inp" / "verification.md").unlink()
    subprocess.run(["git", "-C", str(wt), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(wt), "commit", "-q", "-m", "remove verification"], check=True)
    reg = tmp_path / "reg"
    reg.mkdir()
    line_id = _register_line(reg, repo, wt, "082-inp")
    proc, summary = _run_integrator(tmp_path, repo, reg, line_id)

    assert proc.returncode != 0, "an input error must refuse the merge:\n%s" % proc.stdout
    row = _result_for(summary, line_id)
    assert row["reason"] == "closure-input-error", (
        "a checker exit 2 is an input error, never a quality failure or a block: %r" % (row,)
    )
    entry = _stored_entry(reg, line_id)
    assert entry["state"] == "completed", (
        "exit 2 must leave the line's state unchanged — it is not marked blocked and it does not "
        "become completed: %r" % entry["state"]
    )
    assert entry["integration_result"]["status"] == "failed", entry["integration_result"]
    assert entry["integration_result"]["reason"] == "closure-input-error", entry


def test_a_passing_line_merges_and_records_merged(tmp_path):
    """The positive side of the same gate: a passing feature merges and is recorded merged.

    Without this leg the negative leg could pass for the wrong reason — a pipeline that cannot
    merge at all also refuses. Here the gate passes, the merge lands on trunk, and the record
    carries `merged` with the real commit.
    """
    repo, wt = _make_line_repo(tmp_path, "pos", "081-pos",
                               spec_cell=".specify/specs/081-pos/requirements.md", fixture="positive")
    reg = tmp_path / "reg"
    reg.mkdir()
    line_id = _register_line(reg, repo, wt, "081-pos")
    proc, summary = _run_integrator(tmp_path, repo, reg, line_id)

    assert proc.returncode == 0, "a passing feature must merge:\n%s%s" % (proc.stdout, proc.stderr)
    row = _result_for(summary, line_id)
    assert row["status"] == "merged" and row.get("commit"), row
    entry = _stored_entry(reg, line_id)
    assert entry["state"] == "completed", entry["state"]
    assert entry["integration_result"]["status"] == "merged", entry["integration_result"]
    assert entry["integration_result"]["commit"] == row["commit"]


def test_the_resolution_input_error_shapes_refuse_without_inventing_a_spec_dir(tmp_path):
    """The four GW-03 shapes are input errors (exit-2 class), each naming its subject.

    Per shape, the whole pipeline runs on its own worktree: the resolution refuses, the reason is
    `closure-input-error`, the line keeps its `completed` state and no merge follows. The branches
    below are the shapes the live registry actually exposes (most lines carry a branch with no
    three-digit prefix), which is why a silent skip would have made the gate a no-op for most of
    the fleet.
    """
    shapes = [
        # (name, branch, features rows, expected subject fragment)
        ("branchless", "feature-no-id", [("081", ".specify/specs/081/requirements.md")], "branch"),
        ("no-row", "081-norow", [("999", ".specify/specs/999/requirements.md")], "081"),
        ("dash-cell", "081-dash", [("081", "-")], "Spec Path"),
        ("missing-dir", "081-missing", [("081", ".specify/specs/999-absent/requirements.md")],
         "999-absent"),
    ]
    reg = tmp_path / "reg"
    reg.mkdir()
    for name, branch, rows, subject in shapes:
        repo, wt = _make_line_repo(tmp_path, name, branch,
                                   spec_cell=".specify/specs/unused/requirements.md",
                                   fixture=None, features_rows=rows)
        line_id = _register_line(reg, repo, wt, branch)
        proc, summary = _run_integrator(tmp_path, repo, reg, line_id)
        assert proc.returncode != 0, "%s: an unresolvable spec dir must refuse the merge" % name
        row = _result_for(summary, line_id)
        assert row["reason"] == "closure-input-error", (
            "%s: the shape is an input error, not a block and not a `quality-gate`: %r"
            % (name, row)
        )
        assert subject in row.get("detail", ""), (
            "%s: the refusal must name its subject %r; got %r" % (name, subject, row.get("detail"))
        )
        entry = _stored_entry(reg, line_id)
        assert entry["state"] == "completed", (
            "%s: the resolution error leaves the line where it was: %r" % (name, entry["state"])
        )
        assert entry["integration_result"]["reason"] == "closure-input-error", entry

    # No fallback invents `.specify/specs/<branch>`: a branch-derived path would have made the
    # `081-dash` shape "succeed" against a directory the registry row never named.
    engine = _integrate_module()
    with pytest.raises(engine.GateInputError) as excinfo:
        engine.resolve_spec_dir({"line_id": "demo-20261103T000000Z-ab12", "branch": "081-dash"},
                                tmp_path)
    assert not (tmp_path / ".specify" / "specs" / "081-dash").exists(), (
        "the refusal must not create or consult an invented `.specify/specs/<branch>` path"
    )


def test_an_overridden_gate_keeps_the_quality_gate_reason():
    """`--gate-cmd` stays overridable (GW-03) and its failure is never mislabelled.

    A caller-supplied gate is not the closure verdict, so its failure keeps the historical
    `quality-gate` reason instead of borrowing the closure vocabulary.
    """
    source = INTEGRATE_LINES.read_text(encoding="utf-8")
    assert "gate_cmd is None" in source or "args.gate_cmd" in source, (
        "the override must remain the caller's own command:\n%s" % source[-2000:]
    )
    engine = _integrate_module()
    assert engine.REASON_QUALITY_GATE == "quality-gate"
    assert engine.REASON_CLOSURE_BLOCKED == "closure-blocked"
    assert engine.REASON_CLOSURE_INPUT_ERROR == "closure-input-error"
    for reason in INTEGRATION_RECORD_REASONS:
        assert reason in source, "the driver's reason vocabulary lost %r:\n%s" % (reason, source)
