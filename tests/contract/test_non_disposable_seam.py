"""The four-stage command seam's guard — Feature 092, T111–T115.

Subject: `contracts/four-stage-command.contract.md` C-401…C-407 and C-410, read against the seam's
owner (`skills/internal/manage-history/SKILL.md`, u14's landed text) and its second face
(`templates/commands/history.md`). The seam's **runtime** is prose in two files, so each leg below
derives its verdict from *those bytes* — never from a claim in this file that the bytes are right —
and the derivation is handed to a checker function whose own falsification is observed: every leg
runs its checker against a mutated copy of the real file and asserts the reading goes RED, then
against the unmutated bytes and asserts it goes GREEN. A leg that cannot go red is not evidence.

===================================  ============================================================
leg                                   clause / what it reads
===================================  ============================================================
T111  four-stage ordering             C-401 (both faces, same four names, in order) + C-402 (the
                                      three insertion positions, and execute at Step 6's position)
T112  zero write over two snapshots   C-403 (snapshot pair over the declared roots, byte-identical)
T113  temporary plan only under       C-404 (`.specify/.tmp/` is scratch and is removed; any other
      `.specify/.tmp/`                carrier of the plan before confirmation is a finding)
T114  confirmation granularity +       C-405 (three values, `group` default, no fourth) + C-406
      unconfirmed visibility          (`unconfirmed` is visible, not dropped, not retried, not closed)
T115  group boundary + non-bypass      C-407 (confirmed set only, group boundaries, evidence per
                                      group) + C-410 (a path outside the confirmed rows is a
                                      violation — one reading, not two)
===================================  ============================================================

**Delegated function under test.** The seam fixes the shapes; it does not ship a router. This file
therefore states, in its own data, the reading each clause asks for, as pure functions of the seam
text (`_snapshot_violations`, `_temp_plan_violations`, `_confirmation_violations`,
`_group_violations`) and of a run record (`_unconfirmed_visibility`, `_execute_violations`,
`_confirmation_closure`). Those functions are the falsifiable carrier: a mutation of the *subject*
(seam text) and a mutation of the *checker* (this file's own logic) are both observed going red.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
SEAM = ROOT / "skills" / "internal" / "manage-history" / "SKILL.md"
SEAM_MIRROR = ROOT / ".specify" / "skills" / "internal" / "manage-history" / "SKILL.md"
SEAM_FACE = ROOT / "templates" / "commands" / "history.md"
CONTRACT = ROOT / ".specify" / "archive" / "specs" / "092-non-disposable" / "contracts" / "four-stage-command.contract.md"

#: C-401's four names, in the order the ladder fixes. The spellings are the owner's (§ 四段形态);
#: this tuple is the guard's reading order, not a second statement of the ladder.
STAGES = ("回顾 (review)", "设计（方案） (design)", "用户确认 (user confirm)", "执行 (execute)")
#: The four names' English halves — the command face states them without the Chinese gloss in
#: its bullet, so "the same words" is read on the half both faces spell.
ENGLISH = ("review", "design", "user confirm", "execute")
SHORT_STAGES = ENGLISH

#: C-402's three insertion positions, plus execute bound to the existing write step.
POSITIONS = (("Step 0", "Step 1"), ("Step A", "Step B"))
EXECUTE_POSITION = "Step 6"

#: C-405's closed granularity domain — three values, `group` the default, and nothing else.
GRANULARITIES = ("group", "item", "none-of")
DEFAULT_GRANULARITY = "group"
#: Readings that would make a fourth value or a "confirm once, execute everything" exist.
FOURTH_VALUE_RES = (
    # "the four-value set" (the disposition set) is not a granularity, and the seam's own
    # "**No fourth value**" is the prohibition — only a *plain* fourth-value phrase is a finding.
    re.compile(r"(?<!no\s)\bfourth[- ]value(?!\s*\*\*)", re.IGNORECASE),
    re.compile(r"\b4[- ]value\s+granularit", re.IGNORECASE),
    re.compile(r"`all`\s*\(|`everything`\s*\(|`batch`\s*\("),
    re.compile(r"one confirmation\s*=\s*(?:execute\s+)?everything(?!\s*[\"'`]?\s*MUST NOT)"),
    re.compile(r"`(?:all|everything|batch)`\s*[/|]\s*(?:every|all)\b"),
)
#: The prohibition is a *local* clause: a form is denied when the text immediately before it says
#: so (`-**No fourth value**, and no "…"` / `never "…"`). A window scan is wrong here — the seam's
#: own Step B sits inside a `MUST NOT`-rich region, so any wide window hides a real violation.
_DENIAL_TAIL = re.compile(r"(?:\bno\b|MUST NOT|\bnever\b|\bnot\b)", re.IGNORECASE)
#: C-402's rejection of a renumbering: `0`–`7` in place of the three insertions.
RENUMBER_RE = re.compile(r"Steps 0[–-]7|`0`[–-]`7`|Step 7:")

#: C-403 / C-404: the only sanctioned scratch root, and the tracked carriers it may never use.
SCRATCH = ".specify/.tmp/"
PLAN_NAME = "plan"
SNAPSHOT_NAMES = ("snapshot-before", "snapshot-after-design")

#: C-407 / C-410 — one group per detection class; the fixture groups are named by class id.
GROUP_A = "superseded-live"
GROUP_B = "deferral-marker"


# --------------------------------------------------------------------------- #
# subject loading — a leg that cannot read its subject is red, never an error
# --------------------------------------------------------------------------- #
def _read(path: Path) -> str:
    assert path.is_file(), "the seam face %s is missing — its subject has not landed" % path
    text = path.read_text(encoding="utf-8")
    assert text.strip(), "the seam face %s is empty" % path
    return text


def _sku() -> str:
    return _read(SEAM)


def _face() -> str:
    return _read(SEAM_FACE)


def _mutate(text: str, old: str, new: str = "") -> str:
    """One copy-tree-style mutation, applied in memory to the real bytes we just read."""
    assert old in text, "mutation target %r is absent — the subject moved, so this leg is stale" % old
    return text.replace(old, new, 1)


def _clause(number: str) -> str:
    """The contract clause's own body, so a green here is not a claim the contract never made."""
    text = _read(CONTRACT)
    match = re.search(r"^## %s .*?(?=^## |\Z)" % re.escape(number), text, re.MULTILINE | re.DOTALL)
    assert match, "clause %s is absent from the contract" % number
    return match.group(0)


# --------------------------------------------------------------------------- #
# checker 1 — C-401 / C-402: the ladder, its order, and its positions
# --------------------------------------------------------------------------- #
def _ladder_line(text: str):
    """The first line that carries all four stage names — the ladder's one statement."""
    for line in text.splitlines():
        if all(name in line for name in STAGES):
            return line
    return None


def _stage_order_violations(text: str):
    """Return findings for one face: a missing stage name, or stages out of the ladder's order.

    The order is read on the ladder's one statement, not on the file's offsets: both faces repeat
    a stage name later (the execute segment's heading, the delegation bullet), so a file-wide
    "first occurrence" reading would measure layout, not the ladder.
    """
    findings = []
    for name in STAGES:
        if name not in text:
            findings.append("stage name %r is absent" % name)
    line = _ladder_line(text)
    if line is None:
        findings.append("no single line states all four stage names")
        return findings
    offsets = [line.find(name) for name in STAGES]
    if offsets != sorted(offsets):
        findings.append("the ladder's names are out of order: offsets %r" % (offsets,))
    for half in ENGLISH:
        if half not in text:
            findings.append("the English half %r is absent" % half)
    return findings


def _at(text: str, label: str):
    """Where the step is *placed*: its own heading, not the first prose mention of its name."""
    at = text.find("### %s:" % label)
    return at if at >= 0 else text.find(label)


def _position_violations(text: str):
    """C-402: 0 → A → B precede Step 6, and execute keeps Step 6's position and name."""
    findings = []
    # The three insertions, in order, each placed before the step it is inserted ahead of.
    hop = (_at(text, "Step 0"), _at(text, "Step A"))
    if hop[0] < 0 or hop[1] < 0 or hop[0] >= hop[1]:
        findings.append("Step 0 does not precede Step A (C-402's insertion order)")
    for before, after in POSITIONS:
        if before not in text or after not in text:
            findings.append("insertion %r/%r is not named" % (before, after))
            continue
        if _at(text, before) >= _at(text, after):
            findings.append("insertion %r does not precede %r" % (before, after))
    if EXECUTE_POSITION not in text:
        findings.append("the execute segment is not bound to %r" % EXECUTE_POSITION)
    elif not re.search(r"%s'?s? position" % re.escape(EXECUTE_POSITION), text):
        findings.append("execute is not stated as sitting at %r's position" % EXECUTE_POSITION)
    if RENUMBER_RE.search(text):
        findings.append("the seam renumbers the step list (C-402 forbids `0`–`7`)")
    return findings


def _seam_violations(text: str):
    return _stage_order_violations(text) + _position_violations(text)


# --------------------------------------------------------------------------- #
# T111 — four stages, named identically and in order in both faces
# --------------------------------------------------------------------------- #
def test_t111_both_faces_name_the_four_stages_in_order():
    """C-401: the same four names, in the ladder's order, in the skill and in the command template."""
    skill = _sku()
    face = _face()
    assert _seam_violations(skill) == [], "skill face: %r" % _seam_violations(skill)
    assert _stage_order_violations(face) == [], "command face: %r" % _stage_order_violations(face)
    # "the same words": one `→`-joined sequence, spelled identically in both faces.
    ladder = " → ".join(STAGES)
    assert ladder in skill and ladder in face, (
        "the two faces do not share one ladder statement")
    # The ladder is stated, not implied: all four names sit on one line of that face.
    assert _ladder_line(skill) is not None and _ladder_line(face) is not None
    assert "four stages" in _clause("C-401"), "C-401 moved: this leg reads a clause that no longer says four"


def test_t111_the_contract_names_the_four_stages_it_guards():
    """The contract is an input, not a label: its own clause names the staged order."""
    body = _clause("C-401")
    for short in SHORT_STAGES:
        assert short in body.lower(), "C-401 no longer names %r" % short


@pytest.mark.parametrize("stage", STAGES)
def test_t111_mutation_leg_deleting_one_stage_name_reddens_the_face(stage):
    """C-401's named mutation: delete one stage name from one file and the reading goes red."""
    for loader in (_sku, _face):
        clean = loader()
        assert _stage_order_violations(clean) == [], "precondition: the unmutated face is green"
        broken = clean.replace(stage, "")          # every occurrence, as the contract says
        assert stage not in broken
        assert _stage_order_violations(broken), (
            "deleting %r did not redden the reading — this leg would pass on a broken seam" % stage)


def test_t111_mutation_leg_reordering_two_stage_names_reddens():
    """Order, not mere presence: swapping design and user-confirm is a violation."""
    clean = _sku()
    swapped = _mutate(clean, " → ".join(STAGES),
                      " → ".join((STAGES[0], STAGES[2], STAGES[1], STAGES[3])))
    assert " → ".join(STAGES) not in swapped
    assert _stage_order_violations(swapped), "reordering the ladder did not redden the reading"


def test_t111_mutation_leg_a_misplaced_insertion_reddens():
    """C-402: Step A moved behind Step B (or a renumbering to `0`–`7`) is a violation."""
    clean = _sku()
    head_a = clean.find("### Step A:")
    head_b = clean.find("### Step B:")
    head_0 = clean.find("### Step 0:")
    # The insertion order is 0 → A → B (the pipeline's headings follow in whatever order the
    # skill already had), and a move across any pair is the mutation.
    assert 0 <= head_0 < head_a < head_b, "precondition: 0 → A → B"
    assert _position_violations(clean) == [], "precondition: the clean seam's positions are green"
    # Swap the position of Step 0 and Step A: `Step 0` now sits after `Step A`.
    broken = clean[:head_0] + clean[head_a:head_b] + clean[head_0:head_a] + clean[head_b:]
    assert broken.find("### Step A:") < broken.find("### Step 0:") < broken.find("### Step B:")
    assert _position_violations(broken), "a misplaced insertion did not redden the reading"
    renumbered = _mutate(clean, "Steps 1–6 keep their numbering", "Steps 0–7 keep their numbering")
    assert _position_violations(renumbered), "a renumbering did not redden the reading"


# --------------------------------------------------------------------------- #
# checker 2 — C-403: the two snapshots and their byte identity
# --------------------------------------------------------------------------- #
_REVIEW_CMD = "non-disposable-check.py --json"
_SNAPSHOT_READS = ("git status --porcelain=v1", "sha256sum", SCRATCH + "history-seam-snapshot-before.txt",
                   SCRATCH + "history-seam-snapshot-after-design.txt")


def _two_snapshots(text: str):
    """Extract the before and after snapshot *commands* the seam prescribes (C-403).

    A snapshot is one build of `<readings> > .specify/.tmp/<target>`: the command's window runs from
    its own `mkdir -p` line down to the redirect line, and the target name is the *output* of that
    window. Two lines merely *name* a target without writing it (the prose "…to `.specify/.tmp/
    <name>`, then compare") and the `diff` that reads the pair are therefore not snapshots.
    """
    snapshots = {}
    lines = [line.strip() for line in text.splitlines()]
    for name in SNAPSHOT_NAMES:
        block = None
        # Each `mkdir -p .specify/.tmp` opens one snapshot command's window.
        for index, line in enumerate(lines):
            if not line.startswith("mkdir"):
                continue
            window = lines[index:index + 7]
            target = next((part for part in window if name in part and " > " in part), None)
            if target is None:
                continue
            block = " | ".join(part for part in window[:window.index(target) + 1] if part)
            break
        if block is None:
            # The after-design step says "same command as Step 0" and so carries no copy of it.
            # C-403's "both snapshots must use one command" makes that reading legitimate: the
            # after-block is the before-block with its target name substituted, and nothing else.
            same = re.search(r"[Ss]napshot #[^.]*[^.]same command as Step 0", text)
            if same and name == SNAPSHOT_NAMES[1] and snapshots.get(SNAPSHOT_NAMES[0]):
                block = snapshots[SNAPSHOT_NAMES[0]].replace(SNAPSHOT_NAMES[0], name)
        snapshots[name] = block
    return snapshots


def _snapshot_violations(text: str):
    """C-403: two readings, one command, and their byte identity asserted with no tolerance."""
    findings = []
    for reading in _SNAPSHOT_READS:
        if reading not in text:
            findings.append("snapshot reading %r is not prescribed" % reading)
    shots = _two_snapshots(text)
    for name, line in shots.items():
        if line is None:
            findings.append("snapshot %r is not taken" % name)
    before, after = shots.get(SNAPSHOT_NAMES[0]), shots.get(SNAPSHOT_NAMES[1])
    if before and after:
        # One command: the two blocks differ only by their target file name.
        if before.replace(SNAPSHOT_NAMES[0], "SNAP") != after.replace(SNAPSHOT_NAMES[1], "SNAP"):
            findings.append("the two snapshots are not one command")
        for reading in _SNAPSHOT_READS[:2]:
            if reading not in before or reading not in after:
                findings.append("the pair does not read %r twice" % reading)
    lines = [line.strip() for line in text.splitlines()]
    compared = any(
        any(verb in line for verb in ("diff ", "cmp "))
        and SNAPSHOT_NAMES[0] in "\n".join(lines[index:index + 2])
        and SNAPSHOT_NAMES[1] in "\n".join(lines[index:index + 2])
        for index, line in enumerate(lines))
    if not compared:
        findings.append("the pair is never compared")
    if "byte-identical" not in text:
        findings.append("byte identity is not asserted, so the pair proves nothing")
    # The review reading (Step 0's engine call) sits between the two snapshots, not before both.
    at_before = text.find(SNAPSHOT_NAMES[0])
    at_after = text.find(SNAPSHOT_NAMES[1])
    at_review = text.find(_REVIEW_CMD)
    if min(at_before, at_after, at_review) < 0 or not (at_before < at_review < at_after):
        findings.append("the review reading is not bracketed by the two snapshots")
    return findings


def test_t112_the_seam_brackets_review_and_design_with_one_snapshot_command():
    """C-403: the two snapshots exist, share one command, and are compared byte-for-byte."""
    text = _sku()
    assert _snapshot_violations(text) == [], "seam: %r" % _snapshot_violations(text)
    body = _clause("C-403")
    assert "byte-identical" in body and "git status --porcelain=v1" in body, (
        "C-403 moved: it no longer states the snapshot pair this leg reads")
    # The owner face binds the pair to Steps 0 and A, the two zero-write stages.
    step0 = text.find("### Step 0:")
    step_a = text.find("### Step A:")
    step_b = text.find("### Step B:")
    assert 0 <= step0 < step_a < step_b, "the zero-write window is not Step 0 .. Step A"
    assert step0 < text.find(SNAPSHOT_NAMES[0]) < step_a
    assert step_a < text.find(SNAPSHOT_NAMES[1]) < step_b


def test_t112_a_differing_snapshot_pair_is_a_violation_not_a_detail():
    """The seam's own instruction: a difference stops the run before Step B."""
    text = _sku()
    at = text.find("MUST be byte-identical")
    assert at >= 0, "the pair's byte identity is not stated"
    window = _flat(text[at:at + 400])
    assert "stop before Step B" in window, "a differing pair is not instructed to stop the run"
    assert "never continue and call it a detail" in window


def test_t112_mutation_leg_a_second_snapshot_command_reddens():
    """C-403's mutation: the after-reading taken with a different command is no comparison.

    A "different" reading is one whose own write verb names the after-target, so the seam would
    take the second snapshot with another command — the pair is then not one command.
    """
    clean = _sku()
    assert _snapshot_violations(clean) == [], "precondition: the clean seam is green"
    # C-402 / C-403: "both snapshots must use one command" is what the mutation breaks — the
    # after-design step stops deferring to Step 0's command, so it carries no command of its own
    # and its redirect (when it is written out) reads a different file.
    broken = _mutate(clean, "3. **Snapshot #2, after the design** — same command as Step 0, to",
                     "3. **Snapshot #2, after the design** — a lighter reading, to")
    assert "same command as Step 0" not in broken
    shots = _two_snapshots(broken)
    assert shots[SNAPSHOT_NAMES[1]] != shots[SNAPSHOT_NAMES[0]], (
        "the mutation did not change the second snapshot block")
    assert _snapshot_violations(broken), "two different commands did not redden the reading"


def test_t112_mutation_leg_a_review_outside_the_window_reddens():
    """The mutation removes the review reading from between the snapshots: nothing is measured."""
    clean = _sku()
    assert _snapshot_violations(clean) == [], "precondition: the clean seam is green"
    head0 = clean.find("### Step 0:")
    head_a = clean.find("### Step A:")
    window = clean[head0:head_a]
    assert _REVIEW_CMD in window, "precondition: the review reading sits in Step 0"
    broken = clean[:head0] + window.replace(_REVIEW_CMD, "review reading omitted") + clean[head_a:]
    assert _REVIEW_CMD not in broken[head0:head_a]
    assert _snapshot_violations(broken), "a review outside the snapshot window did not redden"


# --------------------------------------------------------------------------- #
# checker 3 — C-404: the temporary plan's only home
# --------------------------------------------------------------------------- #
_PATHISH = re.compile(r"`([^`\s]+)`")


def _temp_plan_violations(text: str):
    """C-404: the plan's carrier is `.specify/.tmp/`, and the execute segment removes it."""
    findings = []
    if SCRATCH not in text:
        findings.append("the sanctioned scratch root %r is not named" % SCRATCH)
    # Every carrier named next to the word "plan" and a write verb must sit under the scratch root.
    for line in text.splitlines():
        if "plan" not in line.lower():
            continue
        if not re.search(r"\b(?:write|writes|written|lands?|land)\b", line, re.IGNORECASE):
            continue
        for target in _PATHISH.findall(line):
            if target.startswith(SCRATCH) or not target.startswith("."):
                continue
            findings.append("the plan may be written to tracked path %r" % target)
    if not re.search(r"execute segment\s+deletes it|deleted by the execute segment|"
                     r"Delete the `\.specify/\.tmp/` plan", text):
        findings.append("the temporary plan is never removed by the execute segment")
    if not re.search(r"MUST NOT|No tracked path is written before the confirmation",
                     text, re.IGNORECASE):
        findings.append("no prohibition guards a tracked write before confirmation")
    return findings


def test_t113_the_temporary_plan_lives_only_under_the_scratch_root():
    """C-404: `.specify/.tmp/` is the only carrier, and the execute segment deletes it."""
    text = _sku()
    assert _temp_plan_violations(text) == [], "seam: %r" % _temp_plan_violations(text)
    assert "`.specify/.tmp/`" in _clause("C-404")


def test_t113_the_scratch_root_is_git_ignored_on_this_tree():
    """The claim "already matched by `.gitignore`" is measured, not repeated."""
    proc = subprocess.run(["git", "check-ignore", "-q", ".specify/.tmp/seam-probe"],
                          cwd=str(ROOT), capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, (
        ".specify/.tmp/ is not git-ignored here (exit %d) — C-404's premise does not hold"
        % proc.returncode)


def test_t113_mutation_leg_a_tracked_plan_path_reddens():
    """C-404's named mutation: write the design plan to a tracked path and assert red."""
    clean = _sku()
    assert _temp_plan_violations(clean) == [], "precondition: the clean seam is green"
    # The mutation inserts a plan write onto a tracked path, in the seam's own voice.
    anchor = "**Write nothing**, with one sanctioned exception"
    broken = _mutate(clean, anchor,
                     "**Write the plan** to `.specify/specs/092-non-disposable/plan.md`.\n"
                     + anchor)
    assert _temp_plan_violations(broken), "a tracked plan write did not redden the reading"


# --------------------------------------------------------------------------- #
# checker 4 — C-405 / C-406: granularity domain, and the visible `unconfirmed`
# --------------------------------------------------------------------------- #
def _granularity_table(text: str):
    """The granularity table's first cells at Step B — the default marker stripped off."""
    tail = text[text.find("### Step B:"):]
    # The first cell may carry the default marker (`group` (**default**)); the value is the token.
    return [re.split(r"[\s（(]", row.strip())[0]
            for row in re.findall(r"^\|\s*`([^`]+)`(?=[^`]*\|)", tail, re.MULTILINE)]


def _granularity_violations(text: str):
    """C-405: exactly the three values, `group` the default, and no fourth value anywhere."""
    findings = []
    tail = text[text.find("### Step B:"):]
    members = _granularity_table(text)
    for row in members:
        if row not in GRANULARITIES:
            findings.append("a fourth granularity value %r is a table member" % row)
    for value in GRANULARITIES:
        if value not in members:
            findings.append("granularity %r is not a table member at Step B" % value)
    if DEFAULT_GRANULARITY not in tail or "default" not in tail:
        findings.append("`group` is not stated as the default")
    if not re.search(r"Absent input resolves to `group`", tail):
        findings.append("absent input is not resolved to the default")
    if not re.search(r"[Nn]o fourth value", tail):
        findings.append("the closed-ness of the domain is not stated")
    for pattern in FOURTH_VALUE_RES:
        for match in pattern.finditer(text):
            # Local clause: the denial must sit in the same sentence, close to the form.
            before = text[max(0, match.start() - 40):match.start()].replace("\n", " ")
            before = before.split(".")[-1]
            if _DENIAL_TAIL.search(before):
                continue
            findings.append("a fourth-value / execute-everything form survives: %r" % match.group(0))
    if re.search(r"granularit\w*\s*[:=]\s*(?:one|all|everything|batch)\b", tail, re.IGNORECASE):
        findings.append("a fourth granularity value is listed")
    return findings


def _unconfirmed_visibility(entries, confirmed_ids, reviewed_ids=()):
    """C-406: one reading of a run's report; every reviewed entry carries a visible state.

    Returns the findings the report makes visible. An entry outside the confirmed set must be
    `unconfirmed` — visible, not dropped (absent), not auto-retried, not counted as closed.
    ``reviewed_ids`` is the third term that makes "dropped" decidable: the comparison set
    (the review's entry set) is split into confirmed and unconfirmed, so an entry missing from
    the report is a finding rather than an entry nobody remembers.
    """
    findings = []
    seen = {entry["entry_id"]: entry for entry in entries}
    for entry_id in reviewed_ids:
        if entry_id not in seen:
            findings.append("reviewed entry %r is absent from the report" % entry_id)
    for entry_id, entry in seen.items():
        if entry_id in confirmed_ids:
            if entry.get("state") != "disposed":
                findings.append("confirmed entry %r is not disposed" % entry_id)
            continue
        state = entry.get("state")
        if state is None:
            findings.append("unconfirmed entry %r is absent from the report" % entry_id)
        elif state != "unconfirmed":
            findings.append("unconfirmed entry %r reports state %r" % (entry_id, state))
        if state == "disposed":
            findings.append("unconfirmed entry %r claims a closure it does not have" % entry_id)
        if entry.get("retried"):
            findings.append("unconfirmed entry %r was retried automatically" % entry_id)
        if entry.get("counted_as_closed"):
            findings.append("unconfirmed entry %r is counted toward this round's closure" % entry_id)
    return findings


def _closure_count(entries):
    """The round's closure: only `disposed` / in-force `exempt` entries are closed (E-1 / E-2)."""
    return sum(1 for entry in entries
               if entry.get("state") == "disposed" or entry.get("state") == "exempt")


def _confirmation_violations(text: str):
    return _granularity_violations(text)


def test_t114_three_granularities_group_default_no_fourth():
    """C-405: the closed domain, read off Step B, with `group` as the absent-input default."""
    text = _sku()
    assert _confirmation_violations(text) == [], "seam: %r" % _confirmation_violations(text)
    body = _clause("C-405")
    for value in GRANULARITIES:
        assert "`%s`" % value in body, "C-405 does not name %r" % value
    assert "There is no fourth value" in body
    # The command face states the same three values and the same default.
    face = _face()
    assert "`group` (default when absent)" in face
    assert all("`%s`" % value in face for value in GRANULARITIES)


def test_t114_a_partial_confirmation_leaves_the_rest_visible_as_unconfirmed():
    """C-406: confirmed group disposed; the other group visible as `unconfirmed`, not closed."""
    confirmed = {GROUP_A + "/carrier.md:12"}
    reviewed = confirmed | {GROUP_B + "/carrier.md:7"}
    entries = [
        {"entry_id": GROUP_A + "/carrier.md:12", "state": "disposed"},
        {"entry_id": GROUP_B + "/carrier.md:7", "state": "unconfirmed"},
    ]
    assert _unconfirmed_visibility(entries, confirmed, reviewed) == []
    assert _closure_count(entries) == 1, "only the confirmed group closes"

    # An unconfirmed entry that disappears is a violation, not a tidy report.
    dropped = [entries[0]]
    assert _unconfirmed_visibility(dropped, confirmed, reviewed), (
        "a dropped unconfirmed entry stayed green")
    # An unconfirmed entry retried this round is a violation.
    retried = [entries[0], dict(entries[1], retried=True)]
    assert _unconfirmed_visibility(retried, confirmed, reviewed)
    # An unconfirmed entry counted toward closure is a violation.
    counted = [entries[0], dict(entries[1], counted_as_closed=True)]
    assert _unconfirmed_visibility(counted, confirmed, reviewed), (
        "a self-counted unconfirmed entry is caught by the visibility reading")
    assert _closure_count(counted) == 1, (
        "the closure count follows the state: `unconfirmed` never closes, whatever it claims")


def _flat(text: str) -> str:
    """One line: the seam wraps its prose, so a phrase is read across the wrap, not by column."""
    return re.sub(r"\s+", " ", text)


def test_t114_the_seam_states_every_unconfirmed_obligation():
    """C-406's three MUST NOTs, each read as presence in the owner face's Step B."""
    skill = _sku()
    tail = _flat(skill[skill.find("### Step B:"):skill.find("### Step 1:")])
    assert "`unconfirmed`" in tail
    for phrase in ("MUST NOT be silently dropped", "MUST NOT be retried automatically next round",
                   "MUST NOT count toward this round's closure"):
        assert phrase in tail, "the seam no longer states %r" % phrase
    assert 'not "no design yet", not a disposition value' in tail
    assert "MUST NOT count toward this round's closure" in tail
    body = _flat(_clause("C-406"))
    assert "unconfirmed" in body and "MUST NOT be silently dropped" in body
    assert "MUST NOT count toward this round's closure" in body


@pytest.mark.parametrize("value", GRANULARITIES)
def test_t114_mutation_leg_dropping_a_granularity_reddens(value):
    """C-405's mutation: remove one value's table row and the domain is no longer the closed three."""
    clean = _sku()
    assert _granularity_violations(clean) == [], "precondition: the clean seam is green"
    row = [line for line in clean.splitlines()
           if re.match(r"^\|\s*`%s`(?![\w-])" % re.escape(value), line)]
    assert len(row) == 1, "precondition: %r has exactly one table row at Step B" % value
    broken = _mutate(clean, row[0] + "\n", "")
    assert not re.search(r"^\|\s*`%s`(?![\w-])" % re.escape(value), broken, re.MULTILINE)
    assert _granularity_violations(broken), "dropping %r did not redden the reading" % value


def test_t114_mutation_leg_a_fourth_value_reddens():
    """A fourth granularity (`all`) is a finding even when the three are untouched."""
    clean = _sku()
    anchor = "| `none-of` |"
    line = [ln for ln in clean.splitlines() if ln.startswith(anchor)][0]
    broken = _mutate(clean, line, line + "\n| `all` | one confirmation covers the whole tree |")
    assert broken.count(line) == 1 and "| `all` |" in broken, "the mutation did not insert a value"
    assert "all" in _granularity_table(broken), (
        "the mutated table was not re-read — the fourth row must be visible to the checker")
    assert _granularity_violations(broken), (
        "a fourth value did not redden: table=%r" % (_granularity_table(broken),))
    # A "one confirmation = execute everything" form reddens too, when Step B states it itself —
    # and the clause that denies it is local, so removing the denial flips the same sentence red.
    undaunted = _mutate(clean, '**No fourth value**, and no "one confirmation = execute everything"',
                        'A **fourth value** exists, and "one confirmation = execute everything"')
    assert "no \"one confirmation = execute everything\"" not in undaunted
    assert _granularity_violations(undaunted), (
        "an undaunted 'one confirmation = execute everything' did not redden the reading")


def test_t114_mutation_leg_a_swallowed_unconfirmed_entry_reddens():
    """C-406's mutation: the unconfirmed entry is silently dropped and the reading goes red."""
    confirmed = {GROUP_A + "/carrier.md:12"}
    entries = [
        {"entry_id": GROUP_A + "/carrier.md:12", "state": "disposed"},
        {"entry_id": GROUP_B + "/carrier.md:7", "state": "unconfirmed"},
    ]
    assert _unconfirmed_visibility(entries, confirmed) == [], "precondition: the clean run is green"
    swallowed = [entries[0], dict(entries[1], state="disposed")]  # smuggled into the closure
    assert _unconfirmed_visibility(swallowed, confirmed), (
        "calling an unconfirmed entry disposed did not redden the reading")


# --------------------------------------------------------------------------- #
# checker 5 — C-407 / C-410: group boundaries and the no-bypass reading
# --------------------------------------------------------------------------- #
def _group_violations(text: str):
    """C-407: write at group boundaries, one evidence file per group, never mid-entry."""
    findings = []
    start = text.find("### 执行段")
    if start < 0:
        start = text.find("execute segment")   # the heading's missing is itself a finding below
    tail = _flat(text[max(start, 0):])
    if start < 0 or not tail:
        findings.append("the execute segment is not present")
        return findings
    if not re.search(r"[Gg]roup by group", tail):
        findings.append("the execute segment does not write group by group")
    if not re.search(r"group boundar", tail):
        findings.append("group boundaries are not named as the write granularity")
    if not re.search(r"never splitting an entry", tail):
        findings.append("an entry is not protected from being split across a boundary")
    if not re.search(r"one evidence file", tail):
        findings.append("the per-group evidence file is not prescribed")
    for segment in ("`readings`", "`paths`", "`corpus`", "`dispositions`"):
        if segment not in tail:
            findings.append("evidence segment %s is not named at the execute segment" % segment)
    if not re.search(r"Every path the run touches MUST be named in a \*\*confirmed\*\* design row",
                     tail):
        findings.append("C-410's no-bypass rule is not stated at the execute segment")
    return findings


def _execute_violations(touched_paths, confirmed_rows):
    """C-407 / C-410, one reading: every touched path is named in a confirmed design row."""
    return sorted(path for path in touched_paths if path not in confirmed_rows)


def test_t115_execute_writes_at_group_boundaries_and_only_the_confirmed_set():
    """C-407: group-by-group writes, one evidence file per group, confirmed set only."""
    text = _sku()
    assert _group_violations(text) == [], "seam: %r" % _group_violations(text)
    body = _clause("C-407")
    assert "group boundaries" in body and "confirmed set" in body


def test_t115_a_one_group_confirmation_touches_no_path_outside_that_group():
    """C-407's reading: confirming GROUP_A leaves GROUP_B's carriers untouched."""
    confirmed_rows = {GROUP_A + "/carrier.md", ".specify/specs/092-non-disposable/test-evidence/g-A.md"}
    touched = [GROUP_A + "/carrier.md", ".specify/specs/092-non-disposable/test-evidence/g-A.md"]
    assert _execute_violations(touched, confirmed_rows) == []

    # The mutation: the run also writes one path from the unconfirmed group.
    bypassed = touched + [GROUP_B + "/carrier.md"]
    assert _execute_violations(bypassed, confirmed_rows) == [GROUP_B + "/carrier.md"], (
        "a write into an unconfirmed group stayed green")


def test_t115_a_path_outside_the_confirmed_design_rows_is_a_violation():
    """C-410: the same reading as C-407's execute rule, not a second one."""
    confirmed_rows = {GROUP_A + "/carrier.md"}
    assert _execute_violations([GROUP_A + "/carrier.md"], confirmed_rows) == []
    for outside in (".specify/memory/features.md", GROUP_B + "/other.md", "skills/x/SKILL.md"):
        assert _execute_violations([outside], confirmed_rows) == [outside]
    seam_rule = _clause("C-410")
    assert "not named in a confirmed design row is a violation" in seam_rule
    assert "not a second one" in seam_rule.replace("\n", " ")


def test_t115_the_two_clauses_are_one_reading():
    """C-410 says it is C-407's reading; this leg fails if the two ever drift into two."""
    c407 = _clause("C-407")
    c410 = _clause("C-410")
    for body in (c407, c410):
        assert "confirmed" in body
    assert "violation" in c410 and "no path outside that group was touched" in c407


def test_t115_mutation_leg_a_write_inside_an_unconfirmed_group_reddens():
    """C-407's named mutation: touch a path from an unconfirmed group and assert red."""
    confirmed_rows = {GROUP_A + "/carrier.md"}
    touched = [GROUP_A + "/carrier.md"]
    assert _execute_violations(touched, confirmed_rows) == [], "precondition: the clean run is green"
    assert _execute_violations(touched + [GROUP_B + "/carrier.md"], confirmed_rows), (
        "the mutation did not redden the reading")


def test_t115_mutation_leg_a_seam_that_gives_up_its_boundary_reddens():
    """C-407's subject mutation: drop the boundary rule from the execute segment and assert red."""
    clean = _sku()
    assert _group_violations(clean) == [], "precondition: the clean seam is green"
    broken = _mutate(clean, "**Group by group, boundary by boundary.** ",
                     "**Write everything at once.** ")
    assert _group_violations(broken), "a seam with no group boundary did not redden the reading"
    no_bypass = _mutate(clean, "**No bypass.** Every path the run touches MUST be named in a",
                        "Every path the run touches MAY be named in a")
    assert any("no-bypass" in finding for finding in _group_violations(no_bypass)), (
        "weakening the no-bypass rule did not redden the reading")


# --------------------------------------------------------------------------- #
# the faces the seam lives on — read paths, and the whole file observed green
# --------------------------------------------------------------------------- #
def test_the_seam_faces_are_the_two_the_contract_names():
    """C-401's owners exist as live paths; the run-time mirror is the same bytes."""
    for path in (SEAM, SEAM_FACE, CONTRACT):
        assert path.is_file() and path.stat().st_size > 0, "%s is not a live face" % path
    if SEAM_MIRROR.is_file():
        assert hashlib.sha256(_sku().encode()).hexdigest() == \
            hashlib.sha256(_read(SEAM_MIRROR).encode()).hexdigest(), (
                "the .specify/ mirror of the seam skill is not the framework source's copy")
    assert "回顾" in _clause("C-401") or "four stages" in _clause("C-401")


def test_every_leg_observed_red_then_green_in_one_pass():
    """One pass over all five checkers: clean bytes green, the canonical mutation red."""
    clean = _sku()
    assert _seam_violations(clean) == []
    assert _snapshot_violations(clean) == []
    assert _temp_plan_violations(clean) == []
    assert _confirmation_violations(clean) == []
    assert _group_violations(clean) == []
    # The five canonical mutations, each reddening exactly its own checker.
    c401 = clean.replace(STAGES[1], "")
    c403 = _mutate(clean, "3. **Snapshot #2, after the design** — same command as Step 0, to",
                   "3. **Snapshot #2, after the design** — a lighter reading, to")
    c404 = _mutate(clean, "**Write nothing**, with one sanctioned exception",
                   "**Write the plan** to `.specify/specs/x/plan.md`.\n"
                   "**Write nothing**, with one sanctioned exception")
    c405 = _mutate(clean, "| `item` |", "| `batch` |")
    c407 = _mutate(clean, "**Group by group, boundary by boundary.** ", "**All at once.** ")
    assert _seam_violations(c401), "C-401 mutation not red"
    assert _snapshot_violations(c403), "C-403 mutation not red"
    assert _temp_plan_violations(c404), "C-404 mutation not red"
    assert _granularity_violations(c405), "C-405 mutation not red"
    assert _group_violations(c407), "C-407 mutation not red"
