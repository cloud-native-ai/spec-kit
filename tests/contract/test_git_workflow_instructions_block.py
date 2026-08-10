"""Contract test: git-workflow branch data lives in the instructions file.

The skill no longer generates a standalone workflow document. Branch roles are
recorded into the ``## Git Workflow`` managed block of the project's canonical
instructions file, and that block must be registered as a managed range so a
later ``/speckit.instructions`` refresh cannot overwrite it.
"""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "templates" / "instructions-template.md"
INSTRUCTIONS_CMD = REPO_ROOT / "templates" / "commands" / "instructions.md"
LIVE_INSTRUCTIONS = REPO_ROOT / ".specify" / "instructions.md"
SKILL_DIR = REPO_ROOT / "skills" / "git-workflow"
SKILL_MD = SKILL_DIR / "SKILL.md"
BLOCK_ASSET = SKILL_DIR / "assets" / "git-workflow-block.md"
LEGACY_ASSET = SKILL_DIR / "assets" / "git-workflow-template.md"
LOOKUP_REF = SKILL_DIR / "references" / "instructions-lookup.md"
MIRROR_DIR = REPO_ROOT / ".specify" / "skills" / "git-workflow"

START = "<!-- GIT_WORKFLOW_START -->"
END = "<!-- GIT_WORKFLOW_END -->"
HEADING = "## Git Workflow"


@pytest.mark.contract
def test_template_defines_the_managed_block_before_the_registry():
    text = TEMPLATE.read_text(encoding="utf-8")
    assert HEADING in text, "instructions template must define the Git Workflow section"
    assert START in text and END in text, "managed block markers missing from the template"
    assert text.index(START) < text.index(END), "markers out of order"
    assert text.index(HEADING) < text.index("## Resource Registry"), \
        "Git Workflow section must sit before the Resource Registry section"
    block = text[text.index(START):text.index(END)]
    assert "| Role | Branch | Tracking | Purpose |" in block, "block needs the fixed table header"
    assert "None yet." in block, "unestablished workflow must keep the placeholder row"


@pytest.mark.contract
def test_instructions_command_registers_the_block_as_a_managed_range():
    text = INSTRUCTIONS_CMD.read_text(encoding="utf-8")
    assert "`GIT_WORKFLOW`" in text, "scope zones must list GIT_WORKFLOW as machine-owned"
    assert f"{START} ... {END}" in text, \
        "the preserve-managed-ranges list must enumerate the GIT_WORKFLOW marker pair"
    assert "git-workflow` skill" in text, "the block's owner must be named"


@pytest.mark.contract
def test_live_instructions_carry_the_block():
    text = LIVE_INSTRUCTIONS.read_text(encoding="utf-8")
    assert START in text and END in text, "live instructions file is missing the managed block"


@pytest.mark.contract
def test_skill_reads_and_writes_the_block_not_a_document():
    text = SKILL_MD.read_text(encoding="utf-8")
    assert "## Git Workflow 块维护" in text, "skill must document block maintenance"
    assert "no separate workflow document is generated" in text, \
        "description must state that no standalone document is produced"
    assert "不生成独立工作流文档" in text, "skill body must forbid a second data source"
    # the previous data-source contract (frontmatter of a memory document) must be gone
    assert "frontmatter 读取分支映射" not in text, \
        "branch mapping must no longer be read from a document's frontmatter"
    assert "`## Git Workflow` 块读取分支映射" in text, \
        "branch mapping must be read from the managed block"


@pytest.mark.contract
def test_block_asset_replaced_the_document_template():
    assert BLOCK_ASSET.is_file(), "assets/git-workflow-block.md missing"
    assert not LEGACY_ASSET.exists(), \
        "the 216-line document template must be gone; its procedure lives in the references"
    asset = BLOCK_ASSET.read_text(encoding="utf-8")
    assert START in asset and END in asset, "block asset must ship the markers"
    for placeholder in ("<MAIN>", "<PRE>", "<DEV>", "<MAIN_TRACKING>", "<DATE>"):
        assert placeholder in asset, f"block asset missing placeholder {placeholder}"


@pytest.mark.contract
def test_lookup_reference_pins_marker_only_replacement_and_single_source():
    text = LOOKUP_REF.read_text(encoding="utf-8")
    assert "只替换" in text and START in text, \
        "write rule must confine edits to the marker range"
    assert "单一数据源" in text, "reference must forbid a second branch-data source"
    assert "符号链接" in text, "reference must warn that instructions aliases are symlinks"


@pytest.mark.contract
def test_legacy_stores_are_only_referenced_as_migration_sources():
    """Both legacy paths must still be detected, so an existing project can migrate."""
    text = SKILL_MD.read_text(encoding="utf-8")
    assert "docs/git-workflow.md" in text and ".specify/memory/git-workflow.md" in text, \
        "Phase 0 must detect both legacy config locations"
    assert "不自动删除" in text, "legacy files must never be deleted automatically"


@pytest.mark.contract
def test_skill_mirror_is_byte_identical():
    drift = []
    for source in sorted(SKILL_DIR.rglob("*")):
        if not source.is_file():
            continue
        mirror = MIRROR_DIR / source.relative_to(SKILL_DIR)
        if not mirror.is_file() or mirror.read_bytes() != source.read_bytes():
            drift.append(source.relative_to(SKILL_DIR).as_posix())
    assert not drift, f"git-workflow mirror drift: {drift}"
