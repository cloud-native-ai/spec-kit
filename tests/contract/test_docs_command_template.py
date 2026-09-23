"""Contract tests for the /speckit.docs domain: command template + skill pair.

Single home for the docs trio after consolidation. It merges what were three
files reading overlapping slices of the same domain:

* ``test_docs_command_template.py`` — the command template structure, driven by
  ``.specify/specs/033-docs-command/contracts/docs-command-template.md`` (C-1…C-12).
  Since the 2026-08-10 revision the command is a thin dispatch layer; the engine
  semantics are pinned on the ``create-docs`` skill.
* ``test_docs_reconcile_orchestration.py`` — additive reconcile orchestration
  (requirement 048, US3; contract
  ``.specify/specs/049-docs-reconcile/contracts/docs-command-orchestration.md``).
  Only its two non-duplicating propositions survive: the
  discovery-routing/alias prohibition and the reference-doc reference-not-copy
  negative. Its exact-top-level-shape pin and its ``R0 需求解析`` negative were
  byte-for-byte re-assertions of C-3/C-7 here; its managed-block literals are
  owned by ``test_docs_target_structure_declaration.py``.
* ``test_docs_skill_pair.py`` — the create-docs / improve-docs pair (spec 033,
  C-18). The docs domain follows the same create/improve split as tools, agents
  and teams: ``create-X`` owns creation plus structure, ``improve-X`` owns
  evidence-driven refinement of the existing artifact, and improving the *skills
  themselves* stays with ``improve-skills``. Those boundary pins survive; the
  mirror-byte-identity and frontmatter/Feedback/unit-id assertions it repeated
  are asserted once here.
"""
from __future__ import annotations

from pathlib import Path
import runpy

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE = REPO_ROOT / "templates" / "commands" / "docs.md"
TARGET_TEMPLATE = REPO_ROOT / "templates" / "docs-target-structure-template.md"
REFERENCE = REPO_ROOT / "docs" / "reference" / "commands" / "docs.md"
INSTRUCTIONS = REPO_ROOT / ".specify" / "instructions.md"
# 2026-08-17: the .specify/templates/commands/ mirror is retired — per-tool
# copies are generated straight from templates/commands/.
SKILL = REPO_ROOT / "skills" / "create-docs" / "SKILL.md"

PAIR = ("create-docs", "improve-docs")
MAX_LINES = 500

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


def pair_skill_path(name: str) -> Path:
    return REPO_ROOT / "skills" / name / "SKILL.md"


def pair_mirror_path(name: str) -> Path:
    return REPO_ROOT / ".specify" / "skills" / name / "SKILL.md"


def pair_skill_text(name: str) -> str:
    path = pair_skill_path(name)
    assert path.is_file(), f"skills/{name}/SKILL.md missing"
    return path.read_text(encoding="utf-8")


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
    headings = [line for line in text.splitlines() if line.startswith("## ")]
    assert headings == SECTION_ORDER, "top-level sections must remain the exact six-section contract"


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
    assert "skills/create-docs/SKILL.md" in text, "command must point at the structure owner"
    assert "skills/improve-docs/SKILL.md" in text, "command must point at the content owner"
    assert text.count("single source of truth") >= 2, "command must name both ownership boundaries"
    assert "structure" in text.lower() and "content" in text.lower()


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
    assert ".specify/docs/target-structure.md" in command
    assert "templates/docs-target-structure-template.md" in command
    assert TARGET_TEMPLATE.is_file(), "target declaration template missing"


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
    assert "stop-and-confirm" in text, "governance keep-list literal must survive"
    assert "R0 需求解析" not in text, "authoring loop internals must not be inlined in the command"


@pytest.mark.contract
def test_c8_feedback_step_conformance():
    text = source_text()
    assert "## Feedback" in text
    assert "feedback-utils.py" in text
    assert '"/speckit.docs"' in text, "feedback unit-id must be /speckit.docs"
    classification = runpy.run_path(str(REPO_ROOT / "tests" / "contract" / "test_feedback_command_classification.py"))
    assert "docs" in classification["COMPLEX_COMMANDS"]
    # The two list lengths are deliberately NOT restated here: their owner is
    # test_feedback_command_classification.py::test_classification_counts, and a second
    # pin would turn every reclassification into a two-file edit. This test's subject is
    # docs.md's own conformance, which the membership assertion above already covers.


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
    assert REFERENCE.is_file(), "docs/reference/commands/docs.md reference doc missing"
    quickstart = (REPO_ROOT / "docs" / "tutorials" / "quickstart.md").read_text(encoding="utf-8")
    assert "/speckit.docs" in quickstart, "quickstart command table missing /speckit.docs"


@pytest.mark.contract
def test_c11a_reference_doc_does_not_copy_static_baseline_enumerations():
    """Reference-not-copy: the reference doc reaches the baseline by path.

    A restated enumeration here is a second roster that drifts the moment the
    owner (``skills/create-docs/SKILL.md``) changes — C-9 pins the owner's copy.
    """
    text = REFERENCE.read_text(encoding="utf-8")
    assert "README.md" not in text
    assert "concepts/ tutorials/ tasks/ reference/ decisions/ contribute/" not in text
    assert "title/created/expires/status/target/tags" not in text


@pytest.mark.contract
def test_c11b_discovery_routes_index_refresh_and_forbids_alias_edits():
    """The one docs.md rule with a real blast radius: alias files are symlinks.

    Editing a compatibility alias directly severs the link and the affected AI
    agent CLI silently diverges, so the command must route the refresh through
    ``/speckit.instructions`` and say so.
    """
    text = source_text()
    assert "human index" in text.lower()
    assert "/speckit.instructions" in text
    assert ".specify/instructions.md" in text
    assert "Documentation Map" in text
    assert "must not edit compatibility instruction aliases" in text.lower()


@pytest.mark.contract
def test_c12_skill_source_mirror_byte_identity():
    """Source → ``.specify/skills/`` projection for both halves of the pair.

    Frontmatter, ``## Feedback`` and the feedback unit-id are pinned per member by
    ``test_c18_pair_member_shape``, so this asserts only byte-identity and the two
    cannot drift apart about who owns what.
    """
    for name in PAIR:
        src, mirror = pair_skill_path(name), pair_mirror_path(name)
        assert src.is_file(), f"skills/{name}/SKILL.md missing"
        assert mirror.is_file(), f".specify/skills/{name}/SKILL.md mirror missing"
        assert src.read_bytes() == mirror.read_bytes(), f"{name}: skill mirror drift"


# --------------------------------------------------------------------------
# C-18 — the create-docs / improve-docs pair (merged from test_docs_skill_pair)
# --------------------------------------------------------------------------


@pytest.mark.contract
@pytest.mark.parametrize("name", PAIR)
def test_c18_pair_member_shape(name: str):
    text = pair_skill_text(name)
    assert text.startswith("---\n"), f"{name}: frontmatter missing"
    frontmatter = text.split("---", 2)[1]
    assert f"name: {name}" in frontmatter, f"{name}: frontmatter name must match the directory"
    assert "description:" in frontmatter, f"{name}: description missing"
    assert f'skill_id: "<SKILL:.specify/skills/{name}/SKILL.md>"' in frontmatter, \
        f"{name}: skill_id must be the canonical resource id"
    assert "Use this when the user mentions" in frontmatter, f"{name}: description needs triggers"
    assert "## Feedback" in text, f"{name}: mandatory Feedback section missing"
    assert f'"skill:{name}"' in text, f"{name}: feedback unit-id must be skill:{name}"
    assert len(text.splitlines()) < MAX_LINES, f"{name}: SKILL.md exceeds {MAX_LINES} lines"


@pytest.mark.contract
def test_c18_registry_rows_must_not_return_to_instructions():
    """Registry retired (2026-08-17): the skills directory is the discovery surface."""
    instructions = INSTRUCTIONS.read_text(encoding="utf-8")
    rows = [
        line
        for name in PAIR
        for line in instructions.splitlines()
        if line.startswith(f"| {name} |")
    ]
    assert not rows, f"skill registry rows must not return to instructions.md: {rows}"


@pytest.mark.contract
def test_c18_improve_docs_targets_documents_not_the_skill():
    """The improve half refines documentation artifacts; skill self-improvement is improve-skills."""
    text = pair_skill_text("improve-docs")
    assert "improve-skills" in text, \
        "improve-docs must route skill self-improvement to improve-skills"
    assert "one existing document" in text.lower(), \
        "improve-docs must declare a single existing document as its target"


@pytest.mark.contract
def test_c18_improve_docs_does_not_own_structure():
    """Creation, placement, moves and archiving stay with create-docs."""
    text = pair_skill_text("improve-docs")
    assert "create-docs" in text, "improve-docs must name create-docs as the structure owner"
    for obligation in ("Never create, move, rename, or archive", "hand off"):
        assert obligation in text, f"improve-docs must state the boundary obligation: {obligation}"
    assert "never rewrite" in text.lower(), \
        "improve-docs must forbid rewriting decision history"


@pytest.mark.contract
def test_c18_create_docs_keeps_structural_ownership():
    """The create half remains the desired-state/structure authority for the space."""
    text = pair_skill_text("create-docs")
    assert "Desired-State Baseline" in text, "create-docs must keep the desired-state baseline"
    assert "Bootstrap" in text, "create-docs must keep bootstrap ownership"


@pytest.mark.contract
def test_c18_improve_docs_excludes_target_contract_and_names_run_artifacts_precisely():
    text = pair_skill_text("improve-docs")
    assert ".specify/docs/target-structure.md" in text
    assert "cross-run non-document contract" in text
    assert "never edit" in text.lower()
    assert ".specify/docs/plans/" in text
    assert ".specify/docs/audit/" in text
    assert ".specify/docs/**` run artifacts" not in text
