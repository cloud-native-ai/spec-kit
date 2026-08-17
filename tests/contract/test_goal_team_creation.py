"""Structural contract tests for the goal-based create branch (042-goal-team-creation, T002).

Contract: .specify/specs/042-goal-team-creation/contracts/goal-based-create.contract.md

US1 lives in the command template: branch recognition (C-1), definition load and
the two rejections (C-2), the four-element analysis disclosure (C-3), the
single-team derivation (C-4 subset), and the landing invariants (C-5). These are
authored instructions, so this suite pins that the template carries every
normative element the contract declares — engine command lines, the verbatim
STR-003 error prefix, the four analysis elements, advisory-not-gate wording, and
the goal.md zero-write red line. Copy parity derives the copy list from the tree
(no second hard-coded list; only tool dirs that actually carry copies are pinned).
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

CANONICAL = REPO_ROOT / "templates/commands/team.md"

# Per-tool copy list is derived from the tree: the six assistant dirs the regen
# script fans out to, filtered down to those that actually hold a copy today.
_COPY_CANDIDATES = (
    REPO_ROOT / ".claude/commands/speckit.team.md",
    REPO_ROOT / ".github/prompts/speckit.team.prompt.md",
    REPO_ROOT / ".opencode/command/speckit.team.md",
    REPO_ROOT / ".qoder/commands/speckit.team.md",
    REPO_ROOT / ".hermes/commands/speckit.team.md",
    REPO_ROOT / ".codex/commands/speckit.team.md",
)
PER_TOOL_COPIES = tuple(p for p in _COPY_CANDIDATES if p.is_file())

STR_GOAL_UNDEFINED = "goal 未定义:"  # [[STR-003]]

pytestmark = pytest.mark.contract


def _text() -> str:
    return CANONICAL.read_text(encoding="utf-8")


def test_canonical_exists():
    assert CANONICAL.is_file(), f"command source of truth missing: {CANONICAL}"


# --------------------------------------------------------------------------
# C-1 branch recognition: deterministic, engine-enumerated, exact match
# --------------------------------------------------------------------------

def test_recognition_is_driven_by_the_engine_enumeration():
    text = _text()
    assert "list --json" in text, (
        "branch recognition MUST be driven by `goal-utils.py list --json`"
    )
    assert "goal-utils.py" in text


def test_recognition_requires_exact_match_with_no_semantic_guessing():
    text = _text()
    assert "精确匹配" in text, "exact-match wording missing"
    assert "语义猜测" in text, "the no-semantic-guessing constraint missing"


def test_near_miss_is_not_a_hit_and_falls_back_to_free_text():
    text = _text()
    assert "近似" in text and "不构成命中" in text, (
        "near-miss-is-not-a-hit rule missing"
    )
    assert "自由文本" in text, "free-text fallback path missing"


def test_branch_entry_requires_user_confirmation():
    text = _text()
    assert "确认" in text, "user confirmation gate before entering the branch missing"


# --------------------------------------------------------------------------
# C-2 definition load and the two rejections
# --------------------------------------------------------------------------

def test_definition_load_parses_and_restates_to_the_user():
    text = _text()
    assert "parse_goal" in text, "engine parse must be named as the loader"
    assert "复述" in text, "the restate-to-user confirmation step missing"


def test_dangling_reference_error_prefix_is_verbatim():
    text = _text()
    assert STR_GOAL_UNDEFINED in text, "STR-003 verbatim prefix missing"


def test_dangling_reference_points_to_goal_create_and_never_degrades():
    text = _text()
    assert "/speckit.goal create" in text, "the recovery pointer missing"
    assert "内联" in text, "the no-silent-degradation-to-inline rule missing"
    assert "零产物" in text or "零写入" in text, "zero-artifact rule missing"


def test_terminal_goal_is_explicitly_rejected_in_create():
    text = _text()
    assert "achieved" in text and "abandoned" in text, (
        "terminal states must be named in the create-side rejection"
    )
    assert "拒绝" in text, "explicit rejection wording missing"


# --------------------------------------------------------------------------
# C-3 four-element analysis disclosure (advisory, not a gate)
# --------------------------------------------------------------------------

def test_analysis_covers_the_four_elements():
    text = _text()
    for element in ("维度", "判据覆盖", "既有 Target", "可达成性"):
        assert element in text, f"analysis element missing: {element}"


def test_analysis_states_rationale_per_element():
    text = _text()
    assert "理由" in text, "per-element rationale requirement missing"


def test_missing_criteria_must_be_declared_not_invented():
    text = _text()
    assert "None provided." in text, (
        "the missing-criteria marker must be declared verbatim, never invented"
    )


def test_analysis_conclusion_is_advisory_not_a_gate():
    text = _text()
    assert "非门禁" in text or ("建议" in text and "裁决" in text), (
        "advisory-not-gate wording missing: the user adjudicates single-team vs decompose"
    )


# --------------------------------------------------------------------------
# C-4 (single-team subset): derivation from the loaded goal
# --------------------------------------------------------------------------

def test_single_team_declares_goal_slug_and_reports_mismatch():
    text = _text()
    assert "goal_slug" in text, "goal_slug reference binding missing"
    assert "定义权威" in text, "definition-authority rule for inline goal missing"


def test_derivation_reasons_enter_the_confirmation_preview():
    text = _text()
    assert "派生理由" in text, "derivation reasons must enter the confirmation preview"


def test_preset_matching_reuses_the_existing_mechanism():
    text = _text()
    assert "match-team-preset.py" in text, "preset matching script must be reused"


# --------------------------------------------------------------------------
# C-5 landing invariants: team.md only, goal.md zero-write
# --------------------------------------------------------------------------

def test_goal_md_zero_write_red_line_is_stated():
    text = _text()
    assert "goal.md" in text, "goal.md write-face rule missing"
    assert "零写入" in text or "零写" in text, (
        "the create branch MUST declare zero writes to goal.md"
    )


# --------------------------------------------------------------------------
# decomposition proposal (042 US2): decomposition-proposal.contract.md C-2..C-4
# --------------------------------------------------------------------------

STR_PROPOSAL = "分解提议"  # [[STR-002]]


def test_proposal_section_is_present_verbatim():
    text = _text()
    assert STR_PROPOSAL in text, "the STR-002 section name must appear verbatim"


def test_every_statement_is_dry_run_checked_before_the_gate():
    text = _text()
    assert "--check" in text, "the dry-run check command must be named"
    assert "呈现" in text and "通过" in text, (
        "the all-passed-before-presentation rule missing"
    )


def test_approval_is_one_merged_confirmation_then_per_statement_add():
    text = _text()
    assert "合并确认" in text, "single merged confirmation wording missing"
    assert "逐条" in text, "per-statement execution wording missing"
    assert "--add" in text, "the engine add command must be the only landing path"


def test_engine_rejections_are_reported_and_never_bypassed():
    text = _text()
    assert "原样上报" in text, "exit-2 verdicts must be reported verbatim"
    assert "绕过" in text, "the no-engine-bypass rule missing"
    assert "手写" in text, "hand-writing ## Targets must be forbidden"


def test_proposal_set_is_an_unordered_set():
    text = _text()
    assert "无序" in text, "unordered-set wording missing"
    assert "依赖边" in text, "dependency-edge prohibition missing"


def test_independent_candidates_are_directed_to_a_separate_goal():
    text = _text()
    assert "另立 goal" in text, "the GD-3 litmus → separate-goal guidance missing"


def test_reuse_baseline_rules_are_stated():
    text = _text()
    assert "复用基线" in text, "reuse-baseline wording missing"
    assert "不重复授权" in text, "no-duplicate-authorization rule missing"
    assert "顺带重开" in text, "terminal entries must not be silently reopened"


# --------------------------------------------------------------------------
# group creation (042 US3): goal-based-create.contract.md C-4 template face
# --------------------------------------------------------------------------

def test_group_creation_covers_every_open_target():
    text = _text()
    assert "每个 open Target" in text, "one team per open Target rule missing"
    assert "同一 `goal_slug`" in text or "同一个 `goal_slug`" in text, (
        "N teams : 1 Goal binding rule missing"
    )


def test_focus_target_field_position_and_value_are_pinned():
    text = _text()
    assert "focus_target" in text
    assert "goal_slug" in text and "之后" in text, (
        "focus_target MUST be documented as inserted after goal_slug"
    )


def test_team_slug_derivation_pattern_is_pinned():
    text = _text()
    assert "-t<nnn>" in text, "the <goal-slug>-t<nnn> derivation pattern missing"
    assert "查重" in text, "slug uniqueness check against .specify/teams/ missing"


def test_existing_teams_trigger_reuse_or_coordinate():
    text = _text()
    assert "coordinate" in text, "hand-off to /speckit.goal coordinate missing"
    assert "重复建队" in text, "no-silent-duplicate-creation rule missing"


def test_confirmation_gate_discloses_the_five_piece_bundle():
    text = _text()
    for piece in ("分支判定", "分析结论", "路径决策", "territory"):
        assert piece in text, f"gate disclosure piece missing: {piece}"


def test_territory_verify_script_is_named_and_mandatory():
    text = _text()
    assert "verify-territory-disjoint.py" in text, "the verify script must be named"
    assert "静默落盘" in text, "the no-silent-overlap-landing rule missing"


# --------------------------------------------------------------------------
# territory disjoint verify (042 US3): creation-territory-disjoint.contract.md
# --------------------------------------------------------------------------

import importlib.util  # noqa: E402
import json  # noqa: E402  (used by the verify group below)
import subprocess  # noqa: E402
import sys  # noqa: E402

VERIFY = REPO_ROOT / "skills/create-team/scripts/verify-territory-disjoint.py"


def _team_dir(repo: Path, slug: str, frontmatter: list[str]) -> None:
    d = repo / ".specify/teams" / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "team.md").write_text(
        "---\n" + "\n".join(frontmatter) + "\n---\n\n# t\n", encoding="utf-8")


def _proposal(tmp_path, teams: list[dict], goal_slug: str = "g") -> Path:
    p = tmp_path / "proposals.json"
    p.write_text(json.dumps({"goal_slug": goal_slug, "teams": teams}),
                 encoding="utf-8")
    return p


def _verify(repo: Path, proposal: Path):
    return subprocess.run(
        [sys.executable, str(VERIFY), "--input", str(proposal),
         "--repo-root", str(repo), "--json"],
        capture_output=True, text=True)


def test_verify_script_exists():
    assert VERIFY.is_file(), f"verify script missing: {VERIFY}"


def test_all_disjoint_proposals_exit_0(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    proposal = _proposal(tmp_path, [
        {"slug": "g-t001", "write": ["src/a/"], "read": [], "forbidden": [], "non_path": []},
        {"slug": "g-t002", "write": ["src/b/"], "read": [], "forbidden": [], "non_path": []},
    ])
    out = _verify(repo, proposal)
    assert out.returncode == 0, out.stderr + out.stdout


def test_write_overlap_exits_4_with_contested_paths(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    proposal = _proposal(tmp_path, [
        {"slug": "g-t001", "write": ["src/shared/"], "read": [], "forbidden": [], "non_path": []},
        {"slug": "g-t002", "write": ["src/shared/x.py"], "read": [], "forbidden": [], "non_path": []},
    ])
    out = _verify(repo, proposal)
    assert out.returncode == 4
    payload = json.loads(out.stdout)
    contested = [v for v in payload["verdicts"] if v.get("contested")]
    assert contested, "the contested area must be listed"
    assert any("src/shared" in str(c.get("contested")) for c in contested)


def test_existing_team_with_undeclared_territory_is_undecidable(tmp_path):
    repo = tmp_path / "repo"
    _team_dir(repo, "g-existing", ["slug: g-existing", "goal_slug: g"])
    proposal = _proposal(tmp_path, [
        {"slug": "g-t001", "write": ["src/a/"], "read": [], "forbidden": [], "non_path": []},
    ])
    out = _verify(repo, proposal)
    assert out.returncode == 4
    assert "undecidable" in out.stdout


def test_invalid_json_exits_2(tmp_path):
    repo = tmp_path / "repo"
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    out = _verify(repo, bad)
    assert out.returncode == 2


def test_nonexistent_repo_root_exits_3(tmp_path):
    """A --repo-root that does not exist is a resolution failure (exit 3); a
    valid root WITHOUT .specify/teams/ is a fresh project — zero existing
    teams, proposals only, not an error."""
    repo = tmp_path / "nonexistent-root"
    proposal = _proposal(tmp_path, [
        {"slug": "g-t001", "write": ["src/a/"], "read": [], "forbidden": [], "non_path": []},
    ])
    out = _verify(repo, proposal)
    assert out.returncode == 3


def test_non_path_entries_never_intersect(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    proposal = _proposal(tmp_path, [
        {"slug": "g-t001", "write": ["src/a/"], "read": [], "forbidden": [],
         "non_path": [{"type": "runtime", "target": "same dimension"}]},
        {"slug": "g-t002", "write": ["src/b/"], "read": [], "forbidden": [],
         "non_path": [{"type": "runtime", "target": "same dimension"}]},
    ])
    out = _verify(repo, proposal)
    assert out.returncode == 0, "non_path entries are listed for arbitration, never intersected"


def test_verdicts_match_direct_detect_overlaps(tmp_path):
    """Grammar-parity pin: the wrapper must not fork the overlap grammar."""
    spec = importlib.util.spec_from_file_location(
        "bsi_parity", REPO_ROOT / "skills/create-team/scripts/build-summary-input.py")
    bsi = importlib.util.module_from_spec(spec)
    sys.modules["bsi_parity"] = bsi
    spec.loader.exec_module(bsi)

    teams = [
        {"slug": "g-t001", "write": ["src/shared/"], "read": [], "forbidden": [], "non_path": []},
        {"slug": "g-t002", "write": ["src/shared/x.py"], "read": [], "forbidden": [], "non_path": []},
    ]
    a, b = teams[0], teams[1]
    wa, wb = bsi.expand_scopes(a["write"]), bsi.expand_scopes(b["write"])
    expected = bsi.overlap_verdict(a["slug"], {"write": a["write"]},
                                   b["slug"], {"write": b["write"]})
    assert bsi.scopes_overlap("src/shared/x.py", "src/shared/x.py")
    assert expected["verdict"] in ("overlap", "no-overlap", "undecidable")

    repo = tmp_path / "repo"
    repo.mkdir()
    out = _verify(repo, _proposal(tmp_path, teams))
    payload = json.loads(out.stdout)
    pair = [v for v in payload["verdicts"]
            if {v["a"], v["b"]} == {"g-t001", "g-t002"}]
    assert pair and pair[0]["verdict"] == expected["verdict"]


# --------------------------------------------------------------------------
# per-tool copies carry the goal-based branch
# --------------------------------------------------------------------------

@pytest.mark.parametrize("path", PER_TOOL_COPIES, ids=lambda p: p.name)
def test_per_tool_copies_carry_the_goal_based_branch(path):
    assert path.is_file(), f"generated copy missing: {path}"
    text = path.read_text(encoding="utf-8")
    assert STR_GOAL_UNDEFINED in text, f"{path.name} lacks the STR-003 prefix"
    assert "判据覆盖" in text, f"{path.name} lacks the analysis disclosure"
