"""Contract test: /speckit.docs command template structure (spec 033).

Driven by ``.specify/specs/033-docs-command/contracts/docs-command-template.md``
(C-1…C-11).
"""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE = REPO_ROOT / "templates" / "commands" / "docs.md"
MIRROR = REPO_ROOT / ".specify" / "templates" / "commands" / "docs.md"

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


@pytest.mark.contract
def test_c1_source_and_mirror():
    assert SOURCE.is_file()
    assert MIRROR.is_file(), ".specify/templates/commands/docs.md mirror missing"
    assert SOURCE.read_bytes() == MIRROR.read_bytes(), "mirror drift"


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
    text = source_text()
    for marker in ["全量", "单目标", "扇出", "ootstrap"]:
        assert marker in text, f"scope resolution table missing {marker}"
    assert "自动执行" in text, "safe-write auto tier missing"
    assert "干跑计划" in text, "dry-run plan gate missing"


@pytest.mark.contract
def test_c5_four_mandatory_artifacts_with_workspace_paths():
    text = source_text()
    assert ".specify/docs/plans/" in text
    assert ".specify/docs/audit/" in text
    for artifact in ["观察快照", "残差报告", "审计日志", "干跑计划"]:
        assert artifact in text, f"mandatory artifact {artifact} missing"
    assert "零收敛" in text or "无净变化" in text, "no-op audit rule missing"


@pytest.mark.contract
def test_c6_archive_zone_and_no_delete_discipline():
    text = source_text()
    assert "docs/archive/" in text
    assert "只归档不删除" in text


@pytest.mark.contract
def test_c7_thin_dispatch_references():
    text = source_text()
    assert "reconcile-pattern.md" in text
    assert "docs/commands/docs.md" in text or "docs-utils.py" in text


@pytest.mark.contract
def test_c8_feedback_step_conformance():
    text = source_text()
    assert "## Feedback" in text
    assert "feedback-utils.py" in text
    assert '"/speckit.docs"' in text, "feedback unit-id must be /speckit.docs"


@pytest.mark.contract
def test_c9_baseline_registry_and_taxonomy():
    text = source_text()
    for seed in REGISTRY_SEEDS:
        assert seed in text, f"registry seed {seed} missing"
    for d in TYPE_DIRS:
        assert d in text, f"type dir {d} missing"


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
    ref = REPO_ROOT / "docs" / "commands" / "docs.md"
    assert ref.is_file(), "docs/commands/docs.md reference doc missing"
    quickstart = (REPO_ROOT / "docs" / "quickstart.md").read_text(encoding="utf-8")
    assert "/speckit.docs" in quickstart, "quickstart command table missing /speckit.docs"
