"""Contract test: /speckit.docs command template structure (spec 033).

Driven by ``.specify/specs/033-docs-command/contracts/docs-command-template.md``
(C-1…C-12). Since the 2026-08-10 revision the command is a thin dispatch
layer; the engine semantics are pinned on the ``create-docs`` skill.
"""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE = REPO_ROOT / "templates" / "commands" / "docs.md"
# 2026-08-17: the .specify/templates/commands/ mirror is retired — per-tool
# copies are generated straight from templates/commands/.
SKILL = REPO_ROOT / "skills" / "create-docs" / "SKILL.md"
SKILL_MIRROR = REPO_ROOT / ".specify" / "skills" / "create-docs" / "SKILL.md"

SECTION_ORDER = [
    "## User Input",
    "## Glossary",
    "## Outline",
    "## Feedback",
    "## Documentation",
    "## Handoffs",
]

REGISTRY_SEEDS = ["README.md", "ARCHITECTURE.md", "CONTRIBUTING.md", "CHANGELOG.md"]
TYPE_DIRS = ["concepts/", "tutorials/", "tasks/", "reference/", "decisions/", "contribute/", "notes/"]


def source_text() -> str:
    assert SOURCE.is_file(), "templates/commands/docs.md missing"
    return SOURCE.read_text(encoding="utf-8")


def skill_text() -> str:
    assert SKILL.is_file(), "skills/create-docs/SKILL.md missing"
    return SKILL.read_text(encoding="utf-8")


@pytest.mark.contract
def test_c1_source_and_mirror():
    assert SOURCE.is_file()
    assert not (REPO_ROOT / ".specify" / "templates" / "commands" / "docs.md").exists(), (
        "commands mirror retired (2026-08-17); remove any recreated mirror"
    )


@pytest.mark.contract
def test_c2_frontmatter_and_shared_refs():
    text = source_text()
    assert text.startswith("---\n"), "frontmatter missing"
    fm = text.split("---", 2)[1]
    assert "description:" in fm
    assert "handoffs:" in fm
    assert "shared/patterns/reconcile-pattern.md" in text, "must cite the reconcile pattern"


@pytest.mark.contract
def test_c3_section_order():
    text = source_text()
    positions = []
    for heading in SECTION_ORDER:
        idx = text.find(heading)
        assert idx != -1, f"missing section {heading}"
        positions.append(idx)
    assert positions == sorted(positions), "sections out of order"


@pytest.mark.contract
def test_c4_scope_resolution_and_tiered_gates():
    skill = skill_text()
    for marker in ["全量", "单目标", "扇出", "ootstrap", "写作", "authoring"]:
        assert marker in skill, f"skill scope resolution table missing {marker}"
    assert "自动执行" in skill, "safe-write auto tier missing"
    assert "干跑计划" in skill, "dry-run plan gate missing"
    command = source_text()
    for scope in ["全量", "单目标", "写作", "扇出", "Bootstrap"]:
        assert scope in command, f"command outline must name scope {scope}"


@pytest.mark.contract
def test_c4a_mandatory_delegation():
    text = source_text()
    assert "create-docs" in text, "command must delegate to the create-docs skill"
    assert "skills/create-docs/SKILL.md" in text, "command must point at the skill path"
    assert "single source of truth" in text, "command must name the skill as the engine SoT"


@pytest.mark.contract
def test_c5_four_mandatory_artifacts_with_workspace_paths():
    skill = skill_text()
    assert ".specify/docs/plans/" in skill
    assert ".specify/docs/audit/" in skill
    for artifact in ["观察快照", "残差报告", "审计日志", "干跑计划"]:
        assert artifact in skill, f"mandatory artifact {artifact} missing from skill"
    assert "零收敛" in skill or "无净变化" in skill, "no-op audit rule missing"
    command = source_text()
    for artifact in ["观察快照", "残差报告", "审计日志", "干跑计划"]:
        assert artifact in command, f"command should name artifact {artifact}"


@pytest.mark.contract
def test_c6_archive_zone_and_no_delete_discipline():
    skill = skill_text()
    assert "docs/archive/" in skill
    assert "只归档不删除" in skill


@pytest.mark.contract
def test_c7_thin_dispatch_references():
    text = source_text()
    assert "reconcile-pattern.md" in text
    assert "docs-utils.py" in text or "docs/commands/docs.md" in text
    assert "R0 需求解析" not in text, "authoring loop internals must not be inlined in the command"


@pytest.mark.contract
def test_c8_feedback_step_conformance():
    text = source_text()
    assert "## Feedback" in text
    assert "feedback-utils.py" in text
    assert '"/speckit.docs"' in text, "feedback unit-id must be /speckit.docs"


@pytest.mark.contract
def test_c9_baseline_registry_and_taxonomy():
    skill = skill_text()
    for seed in REGISTRY_SEEDS:
        assert seed in skill, f"registry seed {seed} missing from skill"
    for d in TYPE_DIRS:
        assert d in skill, f"type dir {d} missing from skill"


@pytest.mark.contract
def test_c10_runtime_copies_exist_for_every_present_tool():
    history_copies = [
        p for p in REPO_ROOT.glob("**/speckit.history.*")
        if ".specify" not in p.parts and "specs" not in p.parts
        and ".venv" not in p.parts and "node_modules" not in p.parts
    ]
    assert history_copies, "no tool runtime dirs detected via history copies"
    missing = []
    for hist in history_copies:
        expected = hist.with_name(hist.name.replace("speckit.history", "speckit.docs"))
        if not expected.exists():
            missing.append(str(expected.relative_to(REPO_ROOT)))
    assert not missing, f"missing runtime copies: {missing}"


@pytest.mark.contract
def test_c11_reference_doc_and_quickstart_row():
    ref = REPO_ROOT / "docs" / "reference" / "commands" / "docs.md"
    assert ref.is_file(), "docs/reference/commands/docs.md reference doc missing"
    quickstart = (REPO_ROOT / "docs" / "tutorials" / "quickstart.md").read_text(encoding="utf-8")
    assert "/speckit.docs" in quickstart, "quickstart command table missing /speckit.docs"


@pytest.mark.contract
def test_c12_skill_source_mirror_and_feedback():
    assert SKILL.is_file(), "skills/create-docs/SKILL.md missing"
    assert SKILL_MIRROR.is_file(), ".specify/skills/create-docs/SKILL.md mirror missing"
    assert SKILL.read_bytes() == SKILL_MIRROR.read_bytes(), "skill mirror drift"
    text = skill_text()
    assert text.startswith("---\n"), "skill frontmatter missing"
    fm = text.split("---", 2)[1]
    assert "name: create-docs" in fm
    assert "description:" in fm
    assert "skill_id" in fm
    assert "## Feedback" in text
    assert '"skill:create-docs"' in text, "skill feedback unit-id must be skill:create-docs"
