"""Structure contract for sdd-house-keeping (external periodic maintenance skill)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / "skills" / "external" / "sdd-house-keeping"
SKILL_MD = SKILL_DIR / "SKILL.md"
RECIPES = SKILL_DIR / "references" / "maintenance-recipes.md"
DOCS = ROOT / "docs" / "reference" / "skills" / "sdd-house-keeping.md"

PINNED_H2 = [
    "What This Skill Does",
    "When to Load",
    "The Loop (H0–H5)",
    "Hard Requirements",
    "Discipline Defaults",
    "References",
    "Subagent Delegation",
    "Boundary",
    "Self-Improvement Contract",
    "Wrap-up",
]

STAGE_CHAIN = ["H0 ENTRY", "H1 ASSESS", "H2 RECONCILE", "H3 STRENGTHEN",
               "H4 VERIFY", "H5 REPORT"]


def _skill() -> str:
    return SKILL_MD.read_text(encoding="utf-8")


def _recipes() -> str:
    return RECIPES.read_text(encoding="utf-8")


def _frontmatter(text: str):
    assert text.startswith("---")
    end = text.find("\n---", 3)
    assert end != -1
    fields = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key.strip()] = value
    return fields


def _h2(text: str):
    return [line[3:].strip() for line in text.splitlines()
            if line.startswith("## ")]


def test_frontmatter_four_fields():
    fields = _frontmatter(_skill())
    assert set(fields) == {"name", "description", "skill_id", "classification"}
    assert fields["name"] == "sdd-house-keeping"
    assert fields["skill_id"] == (
        "<SKILL:.specify/skills/sdd-house-keeping/SKILL.md>")
    assert fields["classification"] == "external"
    for trigger in ("sdd-house-keeping", "项目管家", "house keeping",
                    "记录回收", "retention cleanup"):
        assert trigger in fields["description"]


def test_classification_annotation_and_soft_collaboration():
    body = _skill().split("---", 2)[2]
    head = body[:900]
    assert "依赖轴" in head and "external" in head
    assert "语义耦合" in head
    assert "软协同" in head and "sdd-project-setup" in head
    assert "sdd-loop-driver" in head


def test_routing_skeleton():
    assert _h2(_skill()) == PINNED_H2


def test_loop_stage_chain_in_order():
    text = _skill()
    positions = [text.find(stage) for stage in STAGE_CHAIN]
    assert all(pos != -1 for pos in positions)
    assert positions == sorted(positions)


def test_commands_and_retention_lane_pinned():
    text = _skill() + _recipes()
    for command in ("/speckit.sanitize", "/speckit.feature",
                    "/speckit.instructions", "/speckit.docs",
                    "/speckit.history", "/speckit.research"):
        assert command in text, f"missing command: {command}"
    assert "--lane retention" in text
    assert "record-retention.py" not in _skill() or "apply" in text
    assert "没有 retention receipt 不删除" in text
    assert "MUST NOT 新增第二道确认门" in text
    assert "30" in text and "宽限" in text


def test_target_resolution_traps():
    text = _skill() + _recipes()
    owner = (ROOT / "shared" / "workflow" / "target-resolution.md").read_text(
        encoding="utf-8")
    assert "shared/workflow/target-resolution.md" in text
    assert "git rev-parse --show-toplevel" in owner
    assert "basename 为 `.specify`" in text or "basename 为 `.specify`" in owner
    assert "框架源仓" in text
    assert "MUST NOT 启动 `qodercli`" in text
    assert "向上搜索" in text
    assert "拒绝执行" in text
    assert "sdd-project-setup" in text
    assert "不向上搜索" not in text


def test_h2_trigger_is_h1_or_owner_drift():
    text = _skill() + _recipes()
    assert "H1 缺口 OR owner 自检报告的漂移" in text
    assert "/speckit.sanitize check" in text
    assert "/speckit.sanitize --lane retention check" in text
    assert "/speckit.sanitize --lane all" in text
    assert "bootstrap-gap" in text
    assert "record-retention.py" in text and "not_evaluated" in text


def test_hard_requirements_numbered():
    text = _skill()
    for n in range(1, 11):
        assert re.search(rf"^{n}\. \*\*", text, re.MULTILINE), (
            f"Hard Requirement {n} missing")
    assert "目标项目治理优先" in text
    assert "盘点先于处置" in text
    assert "不推进 SDD 阶段" in text


def test_boundary_does_not_duplicate_owners():
    text = _skill()
    assert "不安装、不 init、不 bootstrap constitution" in text
    assert "sdd-project-setup" in text
    assert "sdd-loop-driver" in text
    assert "不新增调度器" in text
    assert "不自动上送" in text


def test_scripts_present_and_read_only():
    inv = (SKILL_DIR / "scripts" / "mechanism-inventory.py").read_text(encoding="utf-8")
    logic = (SKILL_DIR / "scripts" / "logical-framework.py").read_text(encoding="utf-8")
    hook = (SKILL_DIR / "scripts" / "hook-health.py").read_text(encoding="utf-8")
    for text in (inv, logic):
        assert "--project" in text and "--json" in text
        assert not re.search(r"open\([^)]*['\"][wax]", text)
        assert not re.search(r"mkdir|makedirs|shutil|rmtree|unlink|remove\(", text)
    for flag in ("--project", "--settings", "--max-sync-timeout", "--fix", "--json"):
        assert flag in hook
    assert "vendor-managed" in hook and "fixable" in hook and "return 10" in hook


def _strip_provenance(text: str) -> str:
    return "\n".join(line for line in text.splitlines()
                     if not line.startswith("# Provenance:")
                     and not line.startswith("# so this external skill")
                     and not line.startswith("# tests/contract/test_sdd_house_keeping_skill.py"))


def test_inventory_script_parity_with_setup_copy():
    for name in ("mechanism-inventory.py", "logical-framework.py"):
        setup = (ROOT / "skills" / "external" / "sdd-project-setup" / "scripts" / name
                 ).read_text(encoding="utf-8")
        house = (SKILL_DIR / "scripts" / name).read_text(encoding="utf-8")
        assert _strip_provenance(house).rstrip("\n") == setup.rstrip("\n"), (
            f"copied script drifted: {name}")


def test_docs_page_and_registries():
    assert DOCS.is_file(), "docs page must exist"
    text = DOCS.read_text(encoding="utf-8")
    for anchor in ("sdd-house-keeping", "H0–H5", "retention", "软协同", "边界"):
        assert anchor in text, f"docs page missing: {anchor}"
    probe = (ROOT / "shared" / "definitions" / "probe-definitions.md").read_text(
        encoding="utf-8")
    assert "skill-sdd-house-keeping-wrapup" in probe
    flow = (ROOT / "shared" / "definitions" / "flow-class-definitions.md").read_text(
        encoding="utf-8")
    assert "skill:sdd-house-keeping" in flow
