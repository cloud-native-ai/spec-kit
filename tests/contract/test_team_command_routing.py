"""Contract tests for the `/speckit.team` command surface (`templates/commands/team.md`).

Merged scope — three former files, one subject (the team.md command template):

- `/speckit.team` routing (SC-002, Feature 027): the three modes and their skill
  routing, plus the migration-contract M6 negatives on `templates/commands/agents.md`.
- goal-based create branch (042-goal-team-creation, T002/T011): the engine wiring
  the branch depends on, plus the `verify-territory-disjoint.py` behavior table
  (exit codes, contested paths, undecidable territory, grammar parity with
  `build-summary-input.py`).
- run `--target` assignment (038-goal-target, T012): per-tool copy parity.

Contracts:
  .specify/specs/042-goal-team-creation/contracts/goal-based-create.contract.md
  .specify/specs/042-goal-team-creation/contracts/decomposition-proposal.contract.md
  .specify/specs/042-goal-team-creation/contracts/creation-territory-disjoint.contract.md
  .specify/specs/038-goal-target/contracts/run-target-assignment.contract.md

What this suite deliberately does NOT pin: the template's prose wording. A
single-phrase wording pin passes for any file containing a common phrase and
fails on a harmless rewrite, so it cannot localize a defect. Every surviving
assertion here names either a machine identifier the agent must actually invoke
(engine command line, script path, slug pattern, verbatim error prefix), a
file/parity property, or a behavior the real script is executed against.

Wording-level propositions that used to be pinned here are owned by behavioral
suites, which are stronger owners because they execute code:
  - five-check preview, focus_target semantics, disclosure forms, report field:
    `tests/contract/test_focus_target_resolution.py`
    + `tests/integration/test_run_target_validation.py`
  - terminal-goal (`achieved`/`abandoned`) rejection and `--add` landing:
    `tests/contract/test_goal_targets_engine.py` (real engine, exit-code table)
  - `## Feedback` / `## Documentation` wrap-up steps on complex commands:
    `tests/contract/test_feedback_command_classification.py`
    + `tests/contract/test_docs_step_injection.py`
  - `None provided.` missing-criteria marker (engine-rendered output):
    `tests/contract/test_goal_definition.py` + `tests/unit/test_goal_utils.py`

Copy parity derives the copy list from the tree (no second hard-coded list; only
tool dirs that actually carry copies are pinned).
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

TEAM_CMD = REPO_ROOT / "templates" / "commands" / "team.md"
AGENTS_CMD = REPO_ROOT / "templates" / "commands" / "agents.md"

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

VERIFY = REPO_ROOT / "skills/create-team/scripts/verify-territory-disjoint.py"

pytestmark = pytest.mark.contract


def _text() -> str:
    return TEAM_CMD.read_text(encoding="utf-8")


# --------------------------------------------------------------------------
# /speckit.team routing (Feature 027) + migration contract M6
# --------------------------------------------------------------------------

class TestTeamCommandRouting:
    def test_team_command_exists(self):
        assert TEAM_CMD.exists(), "templates/commands/team.md must exist (source of /speckit.team)"

    def test_team_command_exposes_three_modes(self):
        content = TEAM_CMD.read_text(encoding="utf-8").lower()
        for mode in ("create", "modify", "run"):
            assert mode in content, f"team.md must document the '{mode}' mode"

    def test_team_command_routes_to_team_skills(self):
        content = TEAM_CMD.read_text(encoding="utf-8")
        assert "create-team" in content, "team.md must route create/run to create-team"
        assert "improve-team" in content, "team.md must route modify to improve-team"

    def test_team_command_has_preview_confirm_gate(self):
        content = TEAM_CMD.read_text(encoding="utf-8").lower()
        assert "static structure" in content and "dynamic structure" in content, (
            "team.md run mode must render Static + Dynamic structure"
        )
        assert "confirm" in content, "team.md run mode must require explicit confirmation"

    def test_agents_command_does_not_route_team_ops(self):
        content = AGENTS_CMD.read_text(encoding="utf-8")
        assert "organize-agents" not in content, (
            "agents.md must not reference organize-agents after migration"
        )
        # No orchestration/team-execution routing left in the single-agent command.
        assert not re.search(r"team[\s-]?loop", content, flags=re.IGNORECASE), (
            "agents.md must not route team-loop orchestration"
        )
        assert "team-supervisor" not in content.lower(), (
            "agents.md must not offer the team-supervisor authoring mode"
        )


# --------------------------------------------------------------------------
# Goal-based create branch (042 C-1 / C-4 / C-5): engine wiring the agent runs
# --------------------------------------------------------------------------

def test_recognition_is_driven_by_the_engine_enumeration():
    """C-1: branch recognition is deterministic and engine-enumerated.

    Pins the exact command line the agent must run. Without it recognition
    degrades to the agent guessing a slug from memory — a silent failure with no
    other mechanical stake.
    """
    text = _text()
    assert "list --json" in text, (
        "branch recognition MUST be driven by `goal-utils.py list --json`"
    )
    assert "goal-utils.py" in text


def test_preset_matching_reuses_the_existing_mechanism():
    """C-4: roster/pattern derivation must reuse the existing preset matcher."""
    text = _text()
    assert "match-team-preset.py" in text, "preset matching script must be reused"


def test_goal_md_zero_write_red_line_is_stated():
    """C-5 write confinement: the create branch never writes goal.md."""
    text = _text()
    assert "goal.md" in text, "goal.md write-face rule missing"
    assert "零写入" in text or "零写" in text, (
        "the create branch MUST declare zero writes to goal.md"
    )


def test_team_slug_derivation_pattern_is_pinned():
    """US3: derived team slugs live under `.specify/teams/<goal-slug>-t<nnn>`."""
    text = _text()
    assert "-t<nnn>" in text, "the <goal-slug>-t<nnn> derivation pattern missing"
    assert "查重" in text, "slug uniqueness check against .specify/teams/ missing"


def test_territory_verify_script_is_named_and_mandatory():
    """US3: the disjointness verifier below must actually be wired into the command."""
    text = _text()
    assert "verify-territory-disjoint.py" in text, "the verify script must be named"
    assert "静默落盘" in text, "the no-silent-overlap-landing rule missing"


# --------------------------------------------------------------------------
# territory disjoint verify (042 US3): creation-territory-disjoint.contract.md
# --------------------------------------------------------------------------

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
# per-tool copies carry the goal-based branch (042) and the --target face (038)
# --------------------------------------------------------------------------

@pytest.mark.parametrize("path", PER_TOOL_COPIES, ids=lambda p: p.name)
def test_per_tool_copies_carry_the_goal_based_branch(path):
    assert path.is_file(), f"generated copy missing: {path}"
    text = path.read_text(encoding="utf-8")
    assert STR_GOAL_UNDEFINED in text, f"{path.name} lacks the STR-003 prefix"
    assert "判据覆盖" in text, f"{path.name} lacks the analysis disclosure"


@pytest.mark.parametrize("path", PER_TOOL_COPIES, ids=lambda p: p.name)
def test_per_tool_copies_carry_target_validation(path):
    assert path.is_file(), f"generated copy missing: {path}"
    text = path.read_text(encoding="utf-8")
    assert "--target" in text, f"{path.name} lacks --target content"
    assert "本次 Target:" in text, f"{path.name} lacks the disclosure line"
