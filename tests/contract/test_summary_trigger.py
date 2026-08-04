"""Contract tests for summary trigger points and gating.

Pins `contracts/summary-trigger.contract.md` rules TG-1…TG-18. These are structural
contract tests (Constitution Principle VII's template-only gate): the trigger points
live in prompt-layer artifacts, so the assertions verify that each artifact carries
the normative rule, across the canonical source, its mirror, and every per-tool copy.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

SKILL_CANONICAL = REPO_ROOT / "skills/create-team/SKILL.md"
SKILL_MIRROR = REPO_ROOT / ".specify/skills/create-team/SKILL.md"
CMD_CANONICAL = REPO_ROOT / "templates/commands/team.md"
CMD_MIRROR = REPO_ROOT / ".specify/templates/commands/team.md"
PER_TOOL_COPIES = [
    REPO_ROOT / ".claude/commands/speckit.team.md",
    REPO_ROOT / ".github/prompts/speckit.team.prompt.md",
    REPO_ROOT / ".qoder/commands/speckit.team.md",
    REPO_ROOT / ".qwen/commands/speckit.team.toml",
    REPO_ROOT / ".opencode/command/speckit.team.md",
]
PRESETS = sorted((REPO_ROOT / "skills/create-team/templates/teams").glob("*.md"))

# STR-005 — the four permitted summary outcomes
STATUS_VOCAB = ["produced", "skipped(cadence)", "skipped(budget)", "declined(no-material)"]

pytestmark = pytest.mark.contract


def skill_text() -> str:
    return SKILL_CANONICAL.read_text(encoding="utf-8")


# --------------------------------------------------------------------------
# Trigger points — one per pattern, plus the terminal summary (TG table)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("path", [SKILL_CANONICAL, SKILL_MIRROR], ids=["canonical", "mirror"])
def test_continuous_loop_has_a_summarize_phase_after_report(path: Path) -> None:
    """The summary reads the run report as provenance, so it runs after REPORT."""
    text = path.read_text(encoding="utf-8")
    loop = text.split("### Per-Cycle Loop", 1)[1].split("###", 1)[0]
    assert "SUMMARIZE" in loop, "continuous per-cycle loop has no SUMMARIZE phase"
    assert loop.index("REPORT") < loop.index("SUMMARIZE"), (
        "SUMMARIZE must come after REPORT — the report is a provenance source"
    )


@pytest.mark.parametrize(
    "pattern_heading,boundary",
    [
        ("§ Iteration Pattern", "DECIDE"),
        ("§ Serial Chain Pattern", "handoff"),
        ("§ Parallel Dispatch Pattern", "aggregat"),
    ],
)
def test_each_pattern_declares_its_summary_boundary(pattern_heading: str, boundary: str) -> None:
    text = skill_text()
    assert pattern_heading in text, f"pattern section {pattern_heading} missing"
    section = text.split(pattern_heading, 1)[1].split("\n## ", 1)[0]
    assert "ummar" in section, f"{pattern_heading} declares no summary trigger point"
    window = section[section.lower().index("summar") - 600 : section.lower().index("summar") + 600]
    assert boundary.lower() in window.lower(), (
        f"{pattern_heading}: summary trigger does not reference its boundary ({boundary})"
    )


def test_terminal_summary_is_declared() -> None:
    """A run that meets the goal / converges / halts still produces one summary."""
    text = skill_text()
    assert re.search(r"terminal summary|终态总结|final summary", text, re.I), (
        "no terminal-summary rule (goal met / converged / halt / manual stop)"
    )


# --------------------------------------------------------------------------
# Gate order — budget outranks cadence outranks material (TG-1…TG-4)
# --------------------------------------------------------------------------


def test_budget_outranks_cadence() -> None:
    text = skill_text()
    assert re.search(r"budget.{0,200}(outrank|precede|优先|before cadence)", text, re.I | re.S), (
        "TG-1: budget priority over cadence is not stated"
    )


def test_summary_is_the_first_step_dropped_under_budget_pressure() -> None:
    text = skill_text()
    assert re.search(r"first step (to be )?dropped|第一个被跳过", text, re.I), (
        "TG-3: the summary must be declared the first step dropped under budget pressure"
    )


def test_boundary_coalescing_is_declared() -> None:
    text = skill_text()
    assert re.search(r"coalesc|合并为一次", text, re.I), (
        "TG-4: two boundaries in rapid succession must coalesce into one refresh"
    )


# --------------------------------------------------------------------------
# Status line (TG-5…TG-8) — what makes "not observed" distinguishable
# --------------------------------------------------------------------------


@pytest.mark.parametrize("path", [SKILL_CANONICAL, SKILL_MIRROR], ids=["canonical", "mirror"])
@pytest.mark.parametrize("token", STATUS_VOCAB)
def test_status_line_vocabulary_is_complete(path: Path, token: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert token in text, f"status-line vocabulary missing {token!r}"


def report_contract_block() -> str:
    """The fenced report template after `### Report contract`.

    Extracted as a fenced block rather than by splitting on `## `, because the
    template inside the fence legitimately contains its own `## Result Summary`,
    `## Deliverables` … headings, which would truncate a naive split.
    """
    text = skill_text()
    after = text.split("### Report contract", 1)[1]
    start = after.index("```")
    end = after.index("```", start + 3)
    return after[start:end]


def test_status_line_is_required_in_every_run_report() -> None:
    block = report_contract_block()
    assert "Summary:" in block, (
        "the Report contract template does not require a summary status line"
    )
    for token in STATUS_VOCAB:
        assert token in block, f"Report contract status line missing {token!r}"


def test_first_run_activation_is_disclosed() -> None:
    """TG-12 / FR-028 — opt-out must not change pre-existing teams silently."""
    block = report_contract_block()
    assert re.search(r"first|首度|首次", block, re.I), (
        "no one-time activation disclosure for a team's first ever summary"
    )


# --------------------------------------------------------------------------
# Enablement (TG-9…TG-11)
# --------------------------------------------------------------------------


def test_summary_is_enabled_by_default() -> None:
    text = skill_text()
    assert re.search(r"opt-out|still ENABLED|默认.*启用", text, re.I), (
        "TG-9: opt-out semantics (enabled when config.summary is absent) not stated"
    )


def test_continuous_default_cadence_is_not_every_cycle() -> None:
    """TG-10 — the single highest-cost failure mode this mechanism must avoid."""
    text = skill_text()
    assert re.search(r"never every cycle|not every cycle|MUST NOT.*每 cycle|不得每 cycle", text, re.I), (
        "TG-10: the continuous default must explicitly exclude every-cycle charting"
    )


def test_config_key_nests_under_config() -> None:
    """TG-11 — preset files already use a top-level `summary:` for their digest."""
    text = skill_text()
    assert "config.summary" in text or re.search(r"config:\n(.|\n)*?  summary:", text), (
        "the summary config key must be nested under `config`"
    )


@pytest.mark.parametrize("preset", PRESETS, ids=lambda p: p.stem)
def test_presets_declare_a_summary_cadence(preset: Path) -> None:
    """T047 — the three shipped presets state their pattern's default cadence."""
    text = preset.read_text(encoding="utf-8")
    assert re.search(r"^\s{2}summary:", text, re.M), (
        f"{preset.name} does not declare config.summary"
    )


# --------------------------------------------------------------------------
# Confirmation-gate disclosure (TG-13, TG-14, TG-18)
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "path", [CMD_CANONICAL, CMD_MIRROR, *PER_TOOL_COPIES], ids=lambda p: p.name
)
def test_confirmation_gate_discloses_the_summary_decision(path: Path) -> None:
    """TG-13/TG-14/TG-18 must reach every tool copy, not just the canonical source."""
    text = path.read_text(encoding="utf-8")
    assert re.search(r"summar", text, re.I), f"{path.name} never mentions the summary"
    gate_region = text.split("Confirmation gate", 1)
    assert len(gate_region) > 1, f"{path.name} has no confirmation gate section"
    window = gate_region[1][:2500]
    assert re.search(r"summar", window, re.I), (
        f"{path.name}: the confirmation gate does not disclose the summary decision"
    )


@pytest.mark.parametrize(
    "path", [CMD_CANONICAL, CMD_MIRROR, *PER_TOOL_COPIES], ids=lambda p: p.name
)
def test_gate_discloses_goal_identity_and_target_directory(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    assert "project/goal/" in text, f"{path.name} does not name the goal delivery directory"


# --------------------------------------------------------------------------
# TG-15 — the corrected team-directory assertion (regression guard)
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "path",
    [SKILL_CANONICAL, SKILL_MIRROR, CMD_CANONICAL, CMD_MIRROR, *PER_TOOL_COPIES],
    ids=lambda p: p.name,
)
def test_no_artifact_claims_the_team_directory_holds_only_team_md_and_runs(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    assert not re.search(r"holds \*\*only\*\* `team\.md` (and|\+) `runs/`", text), (
        f"{path.name} still carries the stale team-directory assertion (TG-15)"
    )
