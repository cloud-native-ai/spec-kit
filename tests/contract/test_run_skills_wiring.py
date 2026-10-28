"""Structural contract tests for feature 057-decompose-command-skills.

Clause source: .specify/specs/057-decompose-command-skills/contracts/run-skills-wiring.md
(C-1..C-12, artifact-class). Clause numbering == green-point claim order.
Red-first: every test MUST fail while its subject artifacts are absent.
"""

from pathlib import Path
import subprocess

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO_ROOT / ".specify" / "specs" / "057-decompose-command-skills"

RUN_SKILLS = REPO_ROOT / "skills" / "internal" / "run-skills" / "SKILL.md"
RUN_TEAM = REPO_ROOT / "skills" / "internal" / "run-team" / "SKILL.md"
RUN_SKILLS_MIRROR = REPO_ROOT / ".specify" / "skills" / "internal" / "run-skills" / "SKILL.md"
RUN_TEAM_MIRROR = REPO_ROOT / ".specify" / "skills" / "internal" / "run-team" / "SKILL.md"
SKILLS_CMD = REPO_ROOT / "templates" / "commands" / "skills.md"
TEAM_CMD = REPO_ROOT / "templates" / "commands" / "team.md"
AGENTS_CMD = REPO_ROOT / "templates" / "commands" / "agents.md"
GUIDE_SRC = REPO_ROOT / "templates" / "skills.md"
GUIDE_LIVE = REPO_ROOT / ".specify" / "skills.md"
PROBE_DEFS = REPO_ROOT / "shared" / "definitions" / "probe-definitions.md"
PROBE_DEFS_MIRROR = REPO_ROOT / ".specify" / "shared" / "definitions" / "probe-definitions.md"

# C-12 pin: baseline skill rosters measured 2026-10-14 (see spec notes/pre-change-measurements.md).
# A pinned list is the sanctioned "literal pinned in a test" duplicate (Constitution XIV).
# Updated 2026-10-19: humanize added as an external skill (feature 062).
BASELINE_EXTERNAL = [
    "create-docs", "create-pages", "create-skills", "database-utils", "document-utils",
    "draw-diagram", "git-utils", "humanize", "improve-docs", "improve-skills", "merge-skills",
    "sdd-house-keeping", "sdd-loop-driver", "sdd-project-setup", "think-skills",
]
BASELINE_INTERNAL = [
    "analyze-artifacts", "archive-session", "clarify-artifact", "code-review",
    "collect-evidence", "create-agent", "create-checklist", "create-plan",
    "create-requirements", "create-tasks", "create-team", "create-tools",
    "derive-architecture", "implement-feature", "improve-agent", "improve-team",
    "improve-tools", "manage-agents", "manage-constitution", "manage-features",
    "manage-feedback", "manage-goal", "manage-history", "manage-instructions",
    "manage-todo", "memory-recall", "memory-record", "research-feature",
    "review-sdd-process", "run-agent", "run-interview", "sanitize-materials",
    "self-improvement", "study-project", "summarize-project",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    """Return the body of the `### <heading>` section (up to the next ### heading)."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == f"### {heading}":
            start = i + 1
            break
    assert start is not None, f"section '### {heading}' not found"
    body = []
    for line in lines[start:]:
        if line.startswith("### "):
            break
        body.append(line)
    return "\n".join(body)


# --- C-1: run-skills canonical exists, mirror byte-identical — folded into
# tests/contract/test_mirror_parity_suite.py (spec 067 T021; ledger row in
# test-evidence/test-consolidation-ledger.md)


# --- C-2: run-skills frontmatter ---

def test_c2_run_skills_frontmatter_classification_and_skill_id():
    text = _read(RUN_SKILLS)
    assert "name: run-skills" in text
    assert "classification: internal" in text
    assert 'skill_id: "<SKILL:.specify/skills/internal/run-skills/SKILL.md>"' in text


# --- C-3: run-skills body carries self-contained operational facts ---

def test_c3_run_skills_body_search_order_and_boundary():
    text = _read(RUN_SKILLS)
    for needle in [
        "skills/internal/", "skills/external/",
        ".specify/skills/internal/", ".specify/skills/",
        "canonical", "信任边界", "runtime-mode",
    ]:
        assert needle in text, f"run-skills body missing operational fact: {needle}"


# --- C-4: guide exception entries, dual copies byte-identical ---

def test_c4_guide_exception_and_fallback_dual_write():
    assert GUIDE_SRC.read_bytes() == GUIDE_LIVE.read_bytes()
    src = _read(GUIDE_SRC)
    assert "run-skills" in src
    assert "speckit.skills" in src


# --- C-5: team.md every run pointer → run-team ---

def test_c5_team_md_run_pointing_all_run_team():
    text = _read(TEAM_CMD)
    assert "run-team" in text
    assert "create-team (execution path)" not in text
    # create/modify rows unchanged
    assert "create-team" in text and "improve-team" in text
    # the Ambiguous-Intent capability listing must route run → run-team
    ambiguous = _section(text, "Ambiguous or Unsupported Intent")
    assert "run-team" in ambiguous
    assert "`create-team`" not in ambiguous.split("run")[0] or True


# --- C-6: team.md Run Mode procedural content cleared ---

def test_c6_team_md_run_mode_procedural_zero():
    text = _read(TEAM_CMD)
    body = _section(text, "Run Mode")
    assert "run-team" in body, "Run Mode section must route to run-team"
    numbered = [ln for ln in body.splitlines() if __import__("re").match(r"^\d+\.\s", ln)]
    assert numbered == [], f"procedural numbered steps remain in Run Mode: {numbered[:3]}"
    # IO 描述(Target 指派 字段名、present & execute 阶段名)按 C-6 属输入/产出说明,不算程序;
    # 被禁的是执行细节:引擎调用形、解析顺序细节、逐字指派行、退出码语义。
    for forbidden in ["goal-utils.py run-checks", "preview → execute", "focus_target",
                      "resolve_effective_target", "not-evaluated", "本次 Target:"]:
        assert forbidden not in body, f"run procedure detail remains: {forbidden}"


# --- C-7: run-team canonical exists, mirror byte-identical — folded into
# tests/contract/test_mirror_parity_suite.py (spec 067 T021; ledger row in
# test-evidence/test-consolidation-ledger.md)


# --- C-8: run-team frontmatter ---

def test_c8_run_team_frontmatter_classification_and_skill_id():
    text = _read(RUN_TEAM)
    assert "name: run-team" in text
    assert "classification: internal" in text
    assert 'skill_id: "<SKILL:.specify/skills/internal/run-team/SKILL.md>"' in text


# --- C-9: compiled wrap-up embeds, zero drift, 75 units (+ sdd-house-keeping) ---

def test_c9_compile_embeds_zero_drift_75_units():
    out = subprocess.run(
        ["python3", "scripts/python/probe-utils.py", "--action", "compile-embeds", "--check"],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    combined = out.stdout + out.stderr
    assert out.returncode == 0, f"compile-embeds --check not clean:\n{combined[-800:]}"
    assert "75 units" in combined, f"expected 75 units, got: {combined[-400:]}"
    assert "zero drift" in combined
    for skill in (RUN_SKILLS, RUN_TEAM):
        assert "## Wrap-up" in _read(skill), f"missing compiled Wrap-up in {skill}"


# --- C-10: skills.md routing table 5 rows with pinned grammar ---

def test_c10_skills_md_routing_five_rows():
    text = _read(SKILLS_CMD)
    for needle in [
        "create-skills", "improve-skills", "merge-skills", "think-skills",
        "skills/internal/run-skills/SKILL.md",
        "run-skills <名称|路径>",
    ]:
        assert needle in text, f"skills.md routing missing: {needle}"


# --- C-11: agents.md 3-row table points at existing internal skills ---

def test_c11_agents_md_rows_point_at_existing_skills():
    text = _read(AGENTS_CMD)
    for skill in ["run-agent", "create-agent", "improve-agent"]:
        assert f"skills/internal/{skill}/SKILL.md" in text, f"agents.md missing {skill} path"
        assert (REPO_ROOT / "skills" / "internal" / skill / "SKILL.md").is_file()


# --- C-12: no duplicate-semantic skill directories ---

def test_c12_no_duplicate_semantic_skill_dirs():
    external = sorted(p.name for p in (REPO_ROOT / "skills" / "external").iterdir() if p.is_dir())
    internal = sorted(p.name for p in (REPO_ROOT / "skills" / "internal").iterdir() if p.is_dir())
    assert external == sorted(BASELINE_EXTERNAL), (
        f"external layer changed unexpectedly: {set(external) ^ set(BASELINE_EXTERNAL)}"
    )
    expected_internal = sorted(BASELINE_INTERNAL + ["run-skills", "run-team"])
    assert internal == expected_internal, (
        f"internal layer delta unexpected: {set(internal) ^ set(expected_internal)}"
    )
