"""Framework-wide confirmation-gate governance (structural contract).

Single home for the gate family. It merges what were four files, each reading a
different slice of one discipline:

* **sweep** — drives the real scanner (Program-First measurement) and pins the
  protected keep list, including every pre-delete confirmation.
* **taxonomy** (was ``test_confirmation_gates_taxonomy.py``) —
  ``shared/guidelines/confirmation-gates.md`` is the criteria truth source:
  destructive-list floor, governance-kept floor, doubtful-strict, anti-backflow.
* **execution report** (was ``test_confirmation_gates_execution_report.py``) — the
  report convention's home plus the non-blocking / never-auto-transmit red line.
* **team flow** (was ``test_confirmation_gates_team_flow.py``) — the
  zero-confirmation flow's source surfaces must carry no blocking wording.

Contracts: ``.specify/specs/044-reduce-confirmation-flows/contracts/`` —
confirmation-taxonomy-contract.md C-1…C-7, execution-report-contract.md C-1…C-5,
team-flow-contract.md; FR-007/FR-011/FR-034.

Two deliberate absences, both deduplication rather than loss:

* The execution-report triad (执行内容 / 产出·变更工件 / 修改途径) is **not** pinned
  here. ``test_user_facing_comprehension_pointers.py`` C-5 pins those three exact
  literals section-scoped in the same document, which is strictly stronger than the
  substring checks the merged files carried.
* The blocking-wording negative carries **no phrase list of its own**. It loads
  ``BLOCKING_RE`` from ``scripts/python/scan-confirmation-gates.py`` so the guard
  strengthens automatically whenever the scanner's pattern set does (precedent:
  ``test_feedback_two_path_routing.py``, ``test_ask_record_repeat.py``). The scanner
  itself is never modified here.

``shared/guidelines/confirmation-gates.md`` is hash-frozen section-by-section by
C-4 of that same pointers test; nothing in this file edits it.
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCANNER = REPO_ROOT / "scripts" / "python" / "scan-confirmation-gates.py"
BASELINE = (
    REPO_ROOT
    / ".specify/specs/044-reduce-confirmation-flows/baseline.json"
)
DOC = REPO_ROOT / "shared" / "guidelines" / "confirmation-gates.md"
FEEDBACK_STEP = REPO_ROOT / "shared" / "workflow" / "feedback-step.md"

TEAM_CMD = REPO_ROOT / "templates" / "commands" / "team.md"
TEAM_SURFACES = (
    TEAM_CMD,
    REPO_ROOT / "skills" / "create-team" / "SKILL.md",
    REPO_ROOT / "skills" / "create-team" / "references" / "create-mode.md",
    REPO_ROOT / "skills" / "create-team" / "references" / "execution-guide.md",
)

# (file, marker) — every protected gate MUST keep a stable textual anchor.
# Rows naming a destructive action (delete/overwrite/force-push) are the ones that
# must never be "simplified away": dropping one silently removes a pre-delete
# confirmation the scanner cannot re-derive.
KEEP_LIST = [
    ("templates/commands/feedback.md", "confirmation of the report"),
    ("templates/commands/docs.md", "stop-and-confirm"),
    ("templates/commands/session.md", "same-name"),
    ("templates/commands/feature.md", "status"),
    ("templates/commands/analyze.md", "explicitly approve"),
    ("templates/commands/interview.md", "confirm"),
    ("templates/constitution-template.md", "irreversible"),
    ("templates/commands/todo.md", "only execute on explicit user approval"),
    ("templates/commands/implement.md", "only execute on explicit user approval"),
    ("templates/commands/implement.md", "CONFIRM"),
    ("templates/commands/tools.md", "confirm"),
    ("skills/git-workflow/SKILL.md", "force-with-lease"),
    ("shared/workflow/glossary.md", "--confirmed-resolution"),
    ("shared/definitions/tool-definitions.md", "Execution never happens before user confirmation via preview gate"),
    ("skills/create-team/references/operating-loops.md", "分级确认"),
    ("templates/commands/sanitize.md", "等待用户确认后才执行"),
]

REQUIRED_SECTIONS = [
    "两级判据",
    "破坏性动作清单",
    "治理保留清单",
    "存疑从严",
    "回流约束",
    "执行报告",
]

DESTRUCTIVE_MIN_ITEMS = [
    "删除",
    "移动",
    "归档",
    "远程推送",
    "覆盖",
]

GOVERNANCE_KEPT_MIN_ROWS = [
    "访谈",
    "宪章",
    "commit",
    "CONFIRM",
    "git-workflow",
    "tools invoke",
]

# Every auto-executed flow surface must disclose the execution-report convention.
AUTO_EXEC_SURFACES = [
    REPO_ROOT / "templates" / "commands" / "team.md",
    REPO_ROOT / "skills" / "create-team" / "SKILL.md",
    REPO_ROOT / "templates" / "commands" / "goal.md",
    REPO_ROOT / "templates" / "commands" / "todo.md",
    REPO_ROOT / "templates" / "commands" / "agents.md",
    REPO_ROOT / "templates" / "commands" / "skills.md",
]


# --------------------------------------------------------------------------
# scanner-driven measurement
# --------------------------------------------------------------------------


def run_scanner() -> dict:
    proc = subprocess.run(
        [sys.executable, str(SCANNER), "--root", str(REPO_ROOT), "--json"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def _scanner_module():
    """Load the real scanner so its own ``BLOCKING_RE`` is the only phrase list."""
    spec = importlib.util.spec_from_file_location("scg_gates_sweep", SCANNER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_no_reversible_gates_remain_blocking() -> None:
    payload = run_scanner()
    reversible = [g for g in payload["gates"] if g["action_class"] == "reversible"]
    assert reversible == [], (
        "reversible gates still present in blocking form: "
        + ", ".join(f"{g['file']}:{g['line']}" for g in reversible[:10])
    )


def test_residual_total_within_sc002_target() -> None:
    if not BASELINE.is_file():
        pytest.skip("baseline.json not present (pre-implementation checkout)")
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    payload = run_scanner()
    cap = baseline["total"] * 0.25
    assert payload["total"] <= cap, (
        f"SC-002 target missed: residual {payload['total']} > 25% of baseline {baseline['total']}"
    )


GOAL_SURFACES = (
    REPO_ROOT / "templates" / "commands" / "goal.md",
    REPO_ROOT / "shared" / "definitions" / "goal-definitions.md",
)


@pytest.mark.parametrize("surface", GOAL_SURFACES, ids=lambda p: p.name)
def test_goal_surface_adds_nothing_to_the_gate_count(surface: Path) -> None:
    """F-13 ③ registers goal's destructive write *by reference*, and the budget's
    integer headroom is 0 — one blocking-pattern hit in either surface moves the total
    off all three pins at once. Zero-hit wording is the only route back to green."""
    payload = run_scanner()
    rel = surface.relative_to(REPO_ROOT).as_posix()
    hits = [g for g in payload["gates"] if g["file"] == rel]
    assert not hits, f"{rel} entered the gate count: {hits}"


@pytest.mark.parametrize("rel_path,marker", KEEP_LIST)
def test_protected_gate_preserved(rel_path: str, marker: str) -> None:
    path = REPO_ROOT / rel_path
    assert path.is_file(), f"protected surface missing: {rel_path}"
    text = path.read_text(encoding="utf-8")
    assert marker in text, f"protected gate marker lost in {rel_path}: {marker!r}"


# --------------------------------------------------------------------------
# taxonomy truth source: shared/guidelines/confirmation-gates.md
# --------------------------------------------------------------------------


@pytest.fixture(scope="module")
def doc_text() -> str:
    assert DOC.is_file(), f"taxonomy truth source missing: {DOC}"
    return DOC.read_text(encoding="utf-8")


def _section_bodies(text: str) -> dict[str, str]:
    bodies: dict[str, str] = {}
    matches = list(re.finditer(r"^##\s+(?!#)(.+?)\s*$", text, flags=re.M))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        bodies[m.group(1).strip()] = text[m.end() : end]
    return bodies


def test_all_required_sections_present(doc_text: str) -> None:
    sections = _section_bodies(doc_text)
    for name in REQUIRED_SECTIONS:
        assert any(name in s for s in sections), f"missing section: {name}"


def test_two_level_taxonomy_normative(doc_text: str) -> None:
    body = next(b for s, b in _section_bodies(doc_text).items() if "两级判据" in s)
    assert "MUST" in body
    assert "破坏性" in body and "可逆" in body
    assert "前置" in body and ("自动执行" in body or "自动" in body)


def test_destructive_list_floor(doc_text: str) -> None:
    body = next(b for s, b in _section_bodies(doc_text).items() if "破坏性动作清单" in s)
    bullets = [l for l in body.splitlines() if l.strip().startswith("-")]
    assert len(bullets) >= 4, "destructive list must be conservative and enumerable (>=4)"
    for item in DESTRUCTIVE_MIN_ITEMS:
        assert any(item in b for b in bullets), f"destructive list missing: {item}"


def test_goal_empty_overwrite_is_registered_as_destructive(doc_text: str) -> None:
    """F-13 ③: goal's empty-overwrite of an authored criteria set is enumerated in the
    bucket, so it is classified by the list rather than by the 存疑从严 fallback.
    Registered inside the existing 覆盖 bullet — the list enumerates action *classes*,
    and this is one instance of 覆盖用户既有内容, exactly as glossary and session are.
    It MUST NOT migrate into 治理保留清单: a row there would claim a gate surface
    goal.md does not carry (the guard is the engine's exit 2), and the row count is
    frozen by C-4 of test_user_facing_comprehension_pointers.py."""
    body = next(b for s, b in _section_bodies(doc_text).items() if "破坏性动作清单" in s)
    assert "goal 判据" in body, "goal's criteria empty-overwrite is not registered"


def test_governance_kept_list_floor(doc_text: str) -> None:
    body = next(b for s, b in _section_bodies(doc_text).items() if "治理保留清单" in s)
    for row in GOVERNANCE_KEPT_MIN_ROWS:
        assert row.lower() in body.lower(), f"governance-kept list missing: {row}"


def test_doubtful_strict_rule(doc_text: str) -> None:
    body = next(b for s, b in _section_bodies(doc_text).items() if "存疑从严" in s)
    assert "MUST" in body
    assert "破坏性" in body


def test_anti_backflow_rule(doc_text: str) -> None:
    body = next(b for s, b in _section_bodies(doc_text).items() if "回流约束" in s)
    assert "MUST NOT" in body
    assert "非破坏性" in body or "可逆" in body


def test_execution_report_granularity_and_failure_rules(doc_text: str) -> None:
    """The two clauses of ## 执行报告 that C-5's triad pin does not cover.

    The triad itself (执行内容 / 产出·变更工件 / 修改途径) is pinned by
    ``test_user_facing_comprehension_pointers.py`` C-5 with exact literals in this
    same section; re-asserting substrings of them here would be a weaker copy.
    """
    body = next(b for s, b in _section_bodies(doc_text).items() if "执行报告" in s)
    assert "琐碎" in body, "granularity exemption (trivial merge) missing"
    assert "失败" in body, "failure reporting clause missing"


def test_concept_basis_reference(doc_text: str) -> None:
    assert "reconcile-pattern" in doc_text, "must reference the tiered-confirmation concept basis"


def test_nonblocking_submission_notice_rule(doc_text: str) -> None:
    """FR-034: the rule source for surface classes ①②⑩⑪ must keep the red line.

    Both literals live on the same line that carries the comprehension-discipline
    pointer, so promoting that rule to a reference must not drop them. The pointer's
    own placement is C-2's assertion in ``test_user_facing_comprehension_pointers.py``.
    """
    assert "非阻塞" in doc_text
    assert "自动传输" in doc_text


@pytest.mark.parametrize("surface", AUTO_EXEC_SURFACES, ids=lambda p: p.name)
def test_auto_exec_surface_carries_report_instructions(surface: Path) -> None:
    assert surface.is_file(), f"missing surface: {surface}"
    text = surface.read_text(encoding="utf-8")
    has_reference = "confirmation-gates.md" in text or "执行报告" in text
    has_report_words = ("呈现" in text or "Report" in text) and (
        "修改" in text or "modify" in text or "improve" in text
    )
    assert has_reference or has_report_words, (
        f"{surface.name}: no execution-report reference or report+modification instructions"
    )


# --------------------------------------------------------------------------
# zero-confirmation team flow
# --------------------------------------------------------------------------


@pytest.mark.parametrize("surface", TEAM_SURFACES, ids=lambda p: p.name)
def test_team_surface_carries_no_blocking_wording(surface: Path) -> None:
    """Reuses the scanner's own ``BLOCKING_RE`` instead of a second phrase list.

    The hand-maintained list this replaces matched 8 of the scanner's patterns and
    silently stopped matching the ninth: ``BLOCKING_RE`` is case-sensitive, so its
    ``confirmation gate`` alternative never caught a capitalised "Confirmation
    gate". The case-insensitive guard below closes exactly that gap and nothing
    else — the scanner is not modified.
    """
    module = _scanner_module()
    # Anti-vacuity sentinel: an empty or broken pattern would make every negative
    # below pass for nothing.
    assert module.BLOCKING_RE.search("等待用户确认"), "scanner BLOCKING_RE loaded empty"
    assert surface.is_file(), f"missing source surface: {surface}"
    text = surface.read_text(encoding="utf-8")
    hits = [
        (i + 1, m.group(0))
        for i, line in enumerate(text.splitlines())
        if (m := module.BLOCKING_RE.search(line))
    ]
    assert not hits, f"blocking gate wording survived in {surface.name}: {hits}"
    ci = re.findall(r"(?i)confirmation gate", text)
    assert not ci, (
        f"blocking gate wording survived in {surface.name} in a casing BLOCKING_RE "
        f"cannot see: {ci}"
    )


def test_team_command_direct_persist_and_report() -> None:
    text = TEAM_CMD.read_text(encoding="utf-8")
    assert "直接落盘" in text or "Persist directly" in text
    assert "confirmation-gates.md" in text, "single-line taxonomy reference missing"
    assert "执行报告" in text or "execution report" in text.lower()
    assert "modify" in text and ("improve-team" in text), "modification path missing"


def test_wrapup_submission_prompt_nonblocking() -> None:
    """The wrap-up prompt's semantics are owned by shared/workflow/feedback-step.md.

    create-team embeds a pointer to that owner rather than a copy, so this guard reads
    the substance where it lives and additionally checks the pointer chain is intact —
    a broken pointer would silently leave the team flow with no prompt semantics at all.
    """
    assert FEEDBACK_STEP.is_file(), f"missing owner surface: {FEEDBACK_STEP}"
    owner = FEEDBACK_STEP.read_text(encoding="utf-8")
    assert "非阻塞" in owner, "wrap-up submission prompt must be non-blocking"
    assert "/speckit.feedback" in owner, "user-facing submission path must be disclosed"
    assert "自动传输" in owner and "MUST NOT" in owner, "no-auto-transmission red line missing"
    skill = (REPO_ROOT / "skills" / "create-team" / "SKILL.md").read_text(encoding="utf-8")
    assert "## Feedback" in skill and "feedback-step.md" in skill, (
        "create-team's Feedback section must point at the owner that carries the "
        "non-blocking / no-auto-transmission semantics"
    )


def test_continuous_tiered_gates_untouched() -> None:
    """Continuous loops keep their tiered gates — both paths are in the scanner's
    ``GOVERNANCE_PATH_PATTERNS``, so losing the wording would drop the gate count
    without tripping the reversible-gate check."""
    ops = REPO_ROOT / "skills" / "create-team" / "references" / "operating-loops.md"
    ws = REPO_ROOT / "skills" / "create-team" / "templates" / "teams" / "project-cluster.md"
    for path in (ops, ws):
        assert path.is_file(), f"missing source surface: {path}"
        text = path.read_text(encoding="utf-8")
        assert "confirm" in text.lower() or "确认" in text, (
            f"continuous-loop tiered gates must be preserved in {path.name}"
        )
