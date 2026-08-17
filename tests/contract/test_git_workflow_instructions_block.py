"""Contract test: git-workflow branch data lives in a dedicated state file.

The skill records branch roles into the managed block of
``.specify/git-workflow.md`` — the single source of truth for every git
operation. The instructions template carries only a pointer section; an inline
``## Git Workflow`` block inside the instructions file is legacy content that
``/speckit.instructions`` migrates into the state file.
"""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "templates" / "instructions-template.md"
INSTRUCTIONS_CMD = REPO_ROOT / "templates" / "commands" / "instructions.md"
LIVE_INSTRUCTIONS = REPO_ROOT / ".specify" / "instructions.md"
STATE_FILE = REPO_ROOT / ".specify" / "git-workflow.md"
SKILL_DIR = REPO_ROOT / "skills" / "git-workflow"
SKILL_MD = SKILL_DIR / "SKILL.md"
BLOCK_ASSET = SKILL_DIR / "assets" / "git-workflow-block.md"
LOOKUP_REF = SKILL_DIR / "references" / "instructions-lookup.md"
BOOTSTRAP_REF = SKILL_DIR / "references" / "bootstrap-commands.md"
MIRROR_DIR = REPO_ROOT / ".specify" / "skills" / "git-workflow"

START = "<!-- GIT_WORKFLOW_START -->"
END = "<!-- GIT_WORKFLOW_END -->"
HEADING = "## Git Workflow"


@pytest.mark.contract
def test_template_git_workflow_section_is_a_pointer():
    text = TEMPLATE.read_text(encoding="utf-8")
    assert HEADING in text, "instructions template must keep the Git Workflow section heading"
    assert START not in text and END not in text, \
        "the managed block must not live in the instructions template anymore"
    assert ".specify/git-workflow.md" in text, "pointer must name the dedicated state file"
    assert "Resource Registry" not in text, "registry section must be gone from the template"


@pytest.mark.contract
def test_instructions_command_owns_the_migration_path():
    text = INSTRUCTIONS_CMD.read_text(encoding="utf-8")
    assert ".specify/git-workflow.md" in text, "scope zones must name the state file"
    assert "git-workflow` skill" in text, "the state file's owner must be named"
    assert "MUST NOT be lost" in text, \
        "legacy branch-role migration into the state file must be data-preserving"


@pytest.mark.contract
def test_state_file_carries_the_managed_block():
    text = STATE_FILE.read_text(encoding="utf-8")
    assert START in text and END in text, "state file is missing the managed block"
    assert text.index(START) < text.index(END), "markers out of order"
    block = text[text.index(START):text.index(END)]
    assert "| Role | Branch | Tracking | Purpose |" in block, "block needs the fixed table header"
    assert "None yet." in block, "unestablished workflow must keep the placeholder row"


@pytest.mark.contract
def test_live_instructions_carry_only_the_pointer():
    text = LIVE_INSTRUCTIONS.read_text(encoding="utf-8")
    assert HEADING in text, "live instructions must keep the pointer section"
    assert START not in text and END not in text, \
        "live instructions must not carry the managed block (legacy content migrated out)"
    assert ".specify/git-workflow.md" in text, "pointer must name the state file"


@pytest.mark.contract
def test_skill_reads_and_writes_the_state_file_not_a_document():
    text = SKILL_MD.read_text(encoding="utf-8")
    assert "## Git Workflow 块维护" in text, "skill must document block maintenance"
    assert ".specify/git-workflow.md" in text, "skill must target the dedicated state file"
    assert "归口 instructions 文件的 `## Git Workflow` 块" not in text, \
        "the instructions file must no longer be named as the block's home"
    # the previous data-source contract (frontmatter of a memory document) must be gone
    assert "frontmatter 读取分支映射" not in text, \
        "branch mapping must no longer be read from a document's frontmatter"


@pytest.mark.contract
def test_block_asset_is_a_full_file_template():
    assert BLOCK_ASSET.is_file(), "assets/git-workflow-block.md missing"
    asset = BLOCK_ASSET.read_text(encoding="utf-8")
    assert START in asset and END in asset, "block asset must ship the markers"
    assert "# Git Workflow Branch Roles" in asset, \
        "asset must render the whole state file, header included"
    for placeholder in ("<MAIN>", "<PRE>", "<DEV>", "<MAIN_TRACKING>", "<DATE>"):
        assert placeholder in asset, f"block asset missing placeholder {placeholder}"


@pytest.mark.contract
def test_lookup_reference_pins_marker_only_replacement_and_single_source():
    text = LOOKUP_REF.read_text(encoding="utf-8")
    assert "只替换" in text and START in text, \
        "write rule must confine edits to the marker range"
    assert ".specify/git-workflow.md" in text, "lookup must resolve to the fixed state file"
    assert "单一数据源" in text, "reference must forbid a second branch-data source"
    assert "归口 instructions 文件" not in text, \
        "lookup must not route branch reads/writes through the instructions file anymore"
    assert "早期版本把托管块写在" in text, \
        "lookup must document migrating the legacy inline instructions block"


@pytest.mark.contract
def test_legacy_stores_are_only_referenced_as_migration_sources():
    """Legacy paths must still be detected, so an existing project can migrate."""
    text = SKILL_MD.read_text(encoding="utf-8")
    assert "docs/git-workflow.md" in text and ".specify/memory/git-workflow.md" in text, \
        "Phase 0 must detect both legacy config locations"
    assert "不自动删除" in text, "legacy files must never be deleted automatically"
    boot = BOOTSTRAP_REF.read_text(encoding="utf-8")
    assert "不再生成独立工作流文档" in boot, "bootstrap must keep the no-second-document rule"
    assert "旧版 instructions.md 内联的 `## Git Workflow` 块" in boot, \
        "the inline instructions block must be listed as a legacy source"


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
