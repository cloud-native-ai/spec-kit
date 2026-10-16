"""Structure contract tests for the sdd-project-setup skill.

sdd-project-setup was created outside a numbered-feature flow (2026-10-16,
as the soft-collaboration companion of sdd-loop-driver), so there is no
spec-owned clause numbering. Clause numbers below are local to this file
and pin the structural facts the skill's own documents declare:

  C-1 frontmatter convention fields       C-7 soft-collaboration redlines
  C-2 classification tension annotation   C-8 handoff twin in sdd-loop-driver
  C-3 H2 routing skeleton                 C-9 inventory script contract
  C-4 loop stage chain S0–S5              C-10 mirror byte-identical
  C-5 mechanism matrix + grading          C-11 roster baselines updated
  C-6 reconcile sequence literal          C-12 docs page content blocks
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "skills" / "external" / "sdd-project-setup"
SKILL_MD = SKILL_DIR / "SKILL.md"

PINNED_H2_SECTIONS = [
    "What This Skill Does",
    "When to Load",
    "The Loop (S0–S5)",
    "Hard Requirements",
    "Discipline Defaults",
    "References",
    "Boundary",
    "Wrap-up",  # compiled section (probe registry; AUTO-GENERATED)
]


def _skill_text() -> str:
    return SKILL_MD.read_text(encoding="utf-8")


def _parse_frontmatter(text: str):
    """Minimal frontmatter parser (no PyYAML per repo convention)."""
    if not text.startswith("---"):
        raise AssertionError("SKILL.md has no frontmatter block")
    end = text.find("\n---", 3)
    assert end != -1, "frontmatter block not closed"
    block = text[4:end]
    body = text[end + 4:].lstrip("\n")
    fields = {}
    for line in block.splitlines():
        if not line.strip():
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key.strip()] = value
    return fields, body


def _h2_sections(text: str) -> list:
    return [
        line[3:].strip()
        for line in text.splitlines()
        if line.startswith("## ")
    ]


# ---------------------------------------------------------------- C-1


def test_c1_frontmatter_four_fields():
    fields, _ = _parse_frontmatter(_skill_text())
    assert set(fields) == {
        "name",
        "description",
        "skill_id",
        "classification",
    }, f"frontmatter must carry exactly the four convention fields, got {sorted(fields)}"
    assert fields["name"] == "sdd-project-setup"
    assert fields["description"], "description must be non-empty"
    assert "sdd-project-setup" in fields["description"]
    assert fields["skill_id"] == (
        "<SKILL:.specify/skills/sdd-project-setup/SKILL.md>"
    )
    assert fields["classification"] == "external"


# ---------------------------------------------------------------- C-2


def test_c2_classification_tension_annotation():
    _, body = _parse_frontmatter(_skill_text())
    head = body[:900]
    assert "依赖轴" in head, (
        "first body paragraph must state the dependency-axis ruling"
    )
    assert "external" in head
    assert "语义耦合" in head, (
        "annotation must declare the semantic coupling explicitly"
    )
    assert "软协同" in head and "非强绑定" in head, (
        "soft-collaboration (not strong binding) must be declared up front"
    )


# ---------------------------------------------------------------- C-3


def test_c3_skill_md_section_set():
    sections = _h2_sections(_skill_text())
    assert sections == PINNED_H2_SECTIONS, (
        f"H2 set must equal the pinned routing skeleton, got {sections}"
    )


# ---------------------------------------------------------------- C-4

STAGE_CHAIN = [
    "S0 ENTRY",
    "S1 ASSESS",
    "S2 INSTALL",
    "S3 RECONCILE",
    "S4 VERIFY",
    "S5 SUGGEST",
]


def test_c4_loop_stage_chain_in_order():
    text = _skill_text()
    positions = [text.find(stage) for stage in STAGE_CHAIN]
    assert all(p != -1 for p in positions), f"missing stages: {positions}"
    assert positions == sorted(positions), (
        "S0–S5 must appear in loop order in SKILL.md"
    )


def test_c4_reconcile_sequence_literal():
    text = _skill_text() + (SKILL_DIR / "references" / "setup-recipes.md").read_text(
        encoding="utf-8"
    )
    assert "/speckit.constitution" in text
    assert "/speckit.sanitize" in text
    assert "/speckit.feature" in text
    assert "/speckit.instructions" in text
    assert "/speckit.docs" in text


# ---------------------------------------------------------------- C-5

RECIPES_MD = SKILL_DIR / "references" / "setup-recipes.md"


def _recipes_text() -> str:
    return RECIPES_MD.read_text(encoding="utf-8")


def test_c5_mechanism_matrix_dimensions_pinned():
    text = _recipes_text()
    # the 13 inventory dimensions, by their matrix keys
    for key in [
        "const", "feat", "gloss", "fb", "reg", "kb", "session",
        "tools", "skills", "tmpl", "specs", "src", "compat",
    ]:
        assert re.search(rf"\|\s*{key}\s*\|", text), (
            f"mechanism matrix dimension missing: {key}"
        )


def test_c5_grading_literature_pinned():
    text = _recipes_text()
    for grade in ["absent", "degraded", "partial", "complete"]:
        assert f"`{grade}`" in text, f"grade literal missing: {grade}"
    assert "缺≠错" in text, "reconcile-needed-is-not-wrong ruling must be pinned"
    assert "未处理清单" in text, "declarative-gap ledger must be pinned"


# ---------------------------------------------------------------- C-6


def test_c6_hard_requirements_numbered_five():
    text = _skill_text()
    for n in range(1, 6):
        assert re.search(rf"^{n}\. \*\*", text, re.MULTILINE), (
            f"Hard Requirement {n} missing"
        )
    assert "盘点先于处置" in text
    assert "三态判定" in text or "就绪是三态" in text


# ---------------------------------------------------------------- C-7


def test_c7_suggestion_not_mandate_redline():
    text = _skill_text() + _recipes_text()
    assert "建议而非强制" in text, "advisory-not-mandatory ruling must be pinned"
    assert "不携带任何「必须调用 sdd-loop-driver」的语义" in text, (
        "the semantic redline against mandatory handoff must be pinned verbatim"
    )


def test_c7_governance_commands_only_boundary():
    text = _skill_text()
    assert "不做任何 SDD 阶段推进" in text, (
        "boundary must exclude SDD stage driving (that is sdd-loop-driver's)"
    )
    assert "constitution/sanitize/feature/instructions/docs" in text


# ---------------------------------------------------------------- C-8


def test_c8_handoff_twin_in_loop_driver():
    ld_recipes = (
        REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "references" / "dispatch-recipes.md"
    ).read_text(encoding="utf-8")
    assert "handoff 给 sdd-project-setup" in ld_recipes, (
        "sdd-loop-driver preflight must name the handoff target"
    )
    ld_skill = (
        REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "非强绑定" in ld_skill and "各自可独立运行" in ld_skill, (
        "loop-driver must declare the same soft-collaboration semantics"
    )
    assert "sdd-project-setup" in ld_skill


# ---------------------------------------------------------------- C-9

SCRIPT = SKILL_DIR / "scripts" / "mechanism-inventory.py"


def test_c9_inventory_script_contract():
    text = SCRIPT.read_text(encoding="utf-8")
    assert "--project" in text and 'required=True' in text, (
        "--project is the one required argument"
    )
    assert "--json" in text, "machine-readable output flag must exist"
    assert "return 2" in text, "argument/path errors exit 2"
    assert "specify_dir" in text, "absent grading depends on the specify_dir fact"
    # read-only scanner: no write-side effects anywhere in the script
    assert not re.search(r"open\([^)]*['\"][wax]", text), (
        "inventory script must be read-only (no write-mode open)"
    )
    assert not re.search(r"mkdir|makedirs|shutil|rmtree|unlink|remove\(", text), (
        "inventory script must not mutate the tree"
    )


def test_c9_grading_matches_recipes():
    script = SCRIPT.read_text(encoding="utf-8")
    recipes = _recipes_text()
    for grade in ["absent", "degraded", "partial", "complete"]:
        assert f'"{grade}"' in script, f"script must grade {grade}"
        assert f"`{grade}`" in recipes, f"recipes must document {grade}"


# ---------------------------------------------------------------- C-10


def test_c10_mirror_byte_identical():
    import filecmp

    dst = REPO_ROOT / ".specify" / "skills" / "sdd-project-setup"
    assert dst.exists(), "runtime mirror missing — sync-mirrors not run"
    for rel in ["SKILL.md", "references/setup-recipes.md", "scripts/mechanism-inventory.py"]:
        assert (dst / rel).exists(), f"mirror missing file: {rel}"
        assert filecmp.cmp(SKILL_DIR / rel, dst / rel, shallow=False), (
            f"mirror drift on {rel}"
        )


# ---------------------------------------------------------------- C-11


def test_c11_roster_baselines_updated():
    wiring = (
        REPO_ROOT / "tests" / "contract" / "test_run_skills_wiring.py"
    ).read_text(encoding="utf-8")
    assert '"sdd-project-setup"' in wiring, (
        "BASELINE_EXTERNAL roster must include sdd-project-setup"
    )
    guards = (
        REPO_ROOT / "tests" / "contract" / "test_skill_layer_visibility_guards.py"
    ).read_text(encoding="utf-8")
    assert '"sdd-project-setup"' in guards, (
        "EXTERNAL_SKILLS census must include sdd-project-setup"
    )


# ---------------------------------------------------------------- C-12

DOCS_PAGE = REPO_ROOT / "docs" / "reference" / "skills" / "sdd-project-setup.md"


def test_c12_docs_page_content_blocks():
    text = DOCS_PAGE.read_text(encoding="utf-8")
    assert "sdd-project-setup" in text
    assert "三模式" in text and "入口参数" in text, (
        "docs page must carry the three-mode instantiation guide"
    )
    assert "S0–S5" in text, "docs page must present the five-step loop"
    assert "软协同契约" in text, "docs page must state the soft-collaboration contract"
    assert "可移植" in text, "docs page must explain executor-side portability"
    assert "边界" in text


def test_c12_wrapup_compiled_block_present():
    text = _skill_text()
    assert "## Wrap-up" in text
    assert "AUTO-GENERATED by probe-utils.py" in text
    assert 'unit-id "skill:sdd-project-setup"' in text
