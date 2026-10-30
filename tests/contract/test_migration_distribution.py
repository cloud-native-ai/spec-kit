"""Contract tests for migration compatibility and distribution (069b, T010).

Owns the assertions of
``.specify/specs/069b-isomorphism-migration-metrics/contracts/migration-distribution.md``
that ``tasks.md`` T010 names:

* C-1  an unrefreshed project keeps its old behaviour: no command template and no
  skill carries a call to one of the new engine actions (``check`` /
  ``delegation`` / ``faces`` / ``isomorphism``), and the shipped file-name sets
  are unchanged (27 command templates, 52 skills — 51 at the 069b baseline; the
  2026-10-30 Feature 078 rename swaps one name in place, so the count is unchanged);
* C-2  a refresh lands every payload from the same release package: the owner and
  the engine travel via ``pyproject.toml`` force-include (``shared`` /
  ``scripts``), the command copies via ``templates``, the skills via
  ``src/hatch_build.py``'s staging step, and ``src/specify_cli/__init__.py``
  copies ``shared/`` into the project's ``.specify/shared``;
* C-3  the new actions are not call sites: neither templates nor skills invoke
  them (the gate owner's call-point table is left to its own owner);
* C-4  zero project-side storage and zero project-side read points: nothing under
  ``.specify/memory/`` stores a unit→class mapping, and the engine never reads
  that tree;
* C-6  the three SC-002 samples are frozen with all declared fields (project,
  HEAD, branch, dirty-file count, 069a payload status, suite command);
* C-7/C-8 the name-level outcome of each snapshot is recorded in
  ``notes/quickstart-run.md`` § 场景 6 as either zero new failing node ids
  (``comm -13`` empty) or ``not-evaluated`` with a reason — never as a failure
  *count*;
* C-12 the refreshed payload is actually executed, not merely present: each
  snapshot records the installed engine's ``lookup`` for two units (exit 0,
  ``source=ledger``) and the framework-only actions' named refusal
  (``framework-source-required``, exit 2) — file presence alone is not evidence.

The owner-document pointer convergence (P1 / P3 / P4) is asserted here too: T011
removes every ``069b 承接`` handoff pointer, makes the literal registry name the
parent spec as the semantic owner, and states that a project's own knowledge-space
record is never read by the framework.

Red-first discipline (Constitution IV): before T011 the owner still carries eleven
``069b 承接`` pointers and neither the literal-registry nor the ownership sentence
has converged, so the real-tree assertions fail as "owner keeps a dangling
handoff" — never as an import or collection error. The negative assertions
(no call sites, no project-side store, frozen file-name sets) are green before the
implementation by design; a green there does not mean the change exists.

Frozen baselines below are pinned copies of the pre-change inventory (a legitimate
drift-detection duplicate under
``.specify/shared/guidelines/one-source-of-truth.md``).
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
OWNER = REPO_ROOT / "shared" / "definitions" / "flow-class-definitions.md"
ENGINE = REPO_ROOT / "scripts" / "python" / "flow-class-check.py"
COMMANDS_DIR = REPO_ROOT / "templates" / "commands"
SKILLS_DIR = REPO_ROOT / "skills"
PYPROJECT = REPO_ROOT / "pyproject.toml"
INIT_PY = REPO_ROOT / "src" / "specify_cli" / "__init__.py"
HATCH_BUILD = REPO_ROOT / "src" / "hatch_build.py"
MEMORY_DIR = REPO_ROOT / ".specify" / "memory"
SPEC_DIR = REPO_ROOT / ".specify" / "specs" / "069b-isomorphism-migration-metrics"
SAMPLES = SPEC_DIR / "notes" / "migration-samples.md"
QUICKSTART = SPEC_DIR / "notes" / "quickstart-run.md"

# Contract C-3 / T010: the four actions that MUST NOT become call sites.
NEW_ACTIONS = ("check", "delegation", "faces", "isomorphism")
NEW_ACTION_CALL_RE = re.compile(
    r"--action\s+(?:check|delegation|faces|isomorphism)\b"
)
ENGINE_REF = "flow-class-check.py"

# Contract C-1: the frozen pre-change inventory (27 command templates, 52 skills).
# 2026-10-30 (Feature 078): the pre-existing external skill unit now named
# `coaching-skills` was renamed in place (FR-001/FR-018), so the shipped file-name
# set swaps one name for another and the count stays 52 = 15 external + 37 internal.
# The retired literal is not repeated here: these rosters are inside A10's closed
# surface, where SC-006 permits it exactly once (the CLI upgrade-registry entry).
COMMAND_BASELINE = frozenset(
    {
        "agents", "analyze", "checklist", "clarify", "constitution", "derive",
        "docs", "feature", "feedback", "goal", "history", "humanize",
        "implement", "improve", "instructions", "interview", "plan",
        "requirements", "research", "review", "sanitize", "session", "skills",
        "tasks", "team", "todo", "tools",
    }
)
SKILL_BASELINE = frozenset(
    {
        "create-docs", "create-pages", "create-skills", "database-utils",
        "document-utils", "draw-diagram", "git-utils", "humanize",
        "improve-docs", "improve-skills", "merge-skills", "sdd-house-keeping",
        "sdd-loop-driver", "sdd-project-setup", "coaching-skills", "analyze-artifacts",
        "archive-session", "clarify-artifact", "code-review",
        "collect-evidence", "create-agent", "create-checklist", "create-plan",
        "create-requirements", "create-tasks", "create-team", "create-tools",
        "derive-architecture", "implement-feature", "improve-agent",
        "improve-team", "improve-tools", "manage-agents",
        "manage-constitution", "manage-features", "manage-feedback",
        "manage-goal", "manage-history", "manage-instructions", "manage-todo",
        "memory-recall", "memory-record", "research-feature",
        "review-sdd-process", "run-agent", "run-interview", "run-skills",
        "run-team", "sanitize-materials", "self-improvement", "study-project",
        "summarize-project",
    }
)
assert len(COMMAND_BASELINE) == 27
assert len(SKILL_BASELINE) == 52

# Contract C-2: the four payload classes and where the release package carries them.
FORCE_INCLUDE_EXPECTED = {
    "shared": "specify_cli/shared",
    "scripts": "specify_cli/scripts",
    "templates": "specify_cli/templates",
}

# Contract C-4: shapes that would make ``.specify/memory/`` a category store.
LEDGER_HEADER = "| unit_id | flow_class |"
LEDGER_ROW_RE = re.compile(
    r"^\|\s*(?:/speckit\.[a-z0-9][a-z0-9-]*|skill:[a-z0-9][a-z0-9-]*)"
    r"\s*\|\s*(?:execution|expression)\s*\|",
    re.MULTILINE,
)
STRUCTURED_SUFFIXES = {".json", ".yaml", ".yml", ".csv", ".toml", ".ini"}

# T011 / P1: the literal registry must name the parent spec as the semantic owner.
PARENT_OWNER_PHRASES = ("父规格", "语义 owner", "同源投影")
# T011 / P3: the ownership section must say the framework never reads a
# project's own knowledge-space record and never lets it change a gate.
PROJECT_SPACE_PHRASES = ("自己的知识空间", "不读取")
GATE_EFFECT_PHRASES = ("改变门禁", "影响门禁")

# C-6: the sample table's required semantic columns (header text fragments).
SAMPLE_COLUMNS = ("项目", "HEAD", "分支", "工作树脏文件", "载荷", "套件命令")

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


# --------------------------------------------------------------------------- #
# generic helpers
# --------------------------------------------------------------------------- #
def _read(path: Path, label: str) -> str:
    assert path.is_file(), f"{label} missing: {path.relative_to(REPO_ROOT)}"
    return path.read_text(encoding="utf-8")


def _cells(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def _is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", cell) for cell in cells)


def _table_after(text: str, header_first_cell: str) -> tuple[list[str], list[list[str]]]:
    """Return (header, data rows) of the first table whose first header cell matches."""
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.strip().startswith("|"):
            continue
        cells = _cells(line)
        if cells and cells[0] == header_first_cell:
            data: list[list[str]] = []
            for candidate in lines[index + 1 :]:
                if not candidate.strip().startswith("|"):
                    break
                row = _cells(candidate)
                if _is_separator(row):
                    continue
                data.append(row)
            return cells, data
    return [], []


def _section(text: str, heading_prefix: str) -> str | None:
    """Return the body of the first heading whose text starts with ``heading_prefix``.

    Headings inside fenced code blocks are not headings — a ``# comment`` in a
    bash snippet must not truncate the section.
    """
    lines = text.splitlines()
    start = None
    level = None
    in_fence = False
    for index, line in enumerate(lines):
        if line.strip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if match and match.group(2).startswith(heading_prefix):
            start = index + 1
            level = len(match.group(1))
            break
    if start is None:
        return None
    body: list[str] = []
    in_fence = False
    for line in lines[start:]:
        if line.strip().startswith(("```", "~~~")):
            in_fence = not in_fence
            body.append(line)
            continue
        match = None if in_fence else HEADING_RE.match(line)
        if match and len(match.group(1)) <= (level or 0):
            break
        body.append(line)
    return "\n".join(body)


# --------------------------------------------------------------------------- #
# C-1 / C-3 — unrefreshed shape: zero call sites, unchanged file-name sets
# --------------------------------------------------------------------------- #
def test_command_templates_never_call_a_new_action() -> None:
    offenders = []
    for path in sorted(COMMANDS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if ENGINE_REF in text and NEW_ACTION_CALL_RE.search(text):
            offenders.append(path.relative_to(REPO_ROOT).as_posix())
    assert not offenders, (
        "command templates must not register the new actions as call sites "
        f"(contract C-1/C-3): {offenders}"
    )


def test_skills_never_call_a_new_action() -> None:
    offenders = []
    for path in sorted(SKILLS_DIR.rglob("*")):
        if not path.is_file() or path.suffix not in {".md", ".py", ".sh", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if ENGINE_REF in text and NEW_ACTION_CALL_RE.search(text):
            offenders.append(path.relative_to(REPO_ROOT).as_posix())
    assert not offenders, (
        "skills must not register the new actions as call sites "
        f"(contract C-1/C-3): {offenders}"
    )


def test_command_template_name_set_matches_frozen_baseline() -> None:
    names = {path.stem for path in COMMANDS_DIR.glob("*.md")}
    assert names == COMMAND_BASELINE, (
        "templates/commands file-name set changed: "
        f"unexpected={sorted(names - COMMAND_BASELINE)} "
        f"missing={sorted(COMMAND_BASELINE - names)}"
    )


def test_skill_name_set_matches_frozen_baseline() -> None:
    names = {
        path.parent.name
        for path in SKILLS_DIR.rglob("SKILL.md")
        if path.parent.parent.name in {"external", "internal"}
    }
    assert names == SKILL_BASELINE, (
        "skills file-name set changed: "
        f"unexpected={sorted(names - SKILL_BASELINE)} "
        f"missing={sorted(SKILL_BASELINE - names)}"
    )


# --------------------------------------------------------------------------- #
# C-2 — one release package carries all four payload classes
# --------------------------------------------------------------------------- #
def test_pyproject_force_include_carries_shared_scripts_templates() -> None:
    text = _read(PYPROJECT, "pyproject.toml")
    match = re.search(
        r"^\[tool\.hatch\.build\.targets\.wheel\.force-include\]\s*$"
        r"([\s\S]*?)(?=^\[|\Z)",
        text,
        re.MULTILINE,
    )
    assert match, "pyproject.toml must keep the wheel force-include table"
    block = match.group(1)
    for source, destination in FORCE_INCLUDE_EXPECTED.items():
        line = f'"{source}" = "{destination}"'
        assert line in block, (
            f"pyproject force-include must carry {line!r} (contract C-2); "
            f"block was:\n{block}"
        )


def test_init_copies_shared_directory_into_the_project() -> None:
    text = _read(INIT_PY, "src/specify_cli/__init__.py")
    assert 'shared_dest = project_path / ".specify" / "shared"' in text, (
        "the init flow must copy shared/ into the project's .specify/shared"
    )
    assert 'copy_tree_with_rewrite(\n                resource_path / "shared",\n                shared_dest,' in text, (
        "the init flow must copy the packaged shared/ tree to shared_dest"
    )


def test_hatch_build_stages_skills_into_the_wheel() -> None:
    text = _read(HATCH_BUILD, "src/hatch_build.py")
    assert "def _stage_skills(build_data)" in text, (
        "src/hatch_build.py must keep the skills staging stage"
    )
    assert '"specify_cli/skills"' in text, (
        "the staged skills tree must land at specify_cli/skills in the wheel"
    )
    assert "_stage_skills(build_data)" in text, (
        "the staging stage must be invoked from the build hook"
    )


def test_owner_and_engine_payloads_exist() -> None:
    assert OWNER.is_file(), "classification owner payload missing"
    assert ENGINE.is_file(), "engine payload missing"
    assert "## 同构映射（8 阶段 × 3 面）" in OWNER.read_text(encoding="utf-8"), (
        "the owner payload must carry the isomorphism map chapter"
    )
    assert "## 不可同构边界" in OWNER.read_text(encoding="utf-8"), (
        "the owner payload must carry the non-isomorphism boundary chapter"
    )


# --------------------------------------------------------------------------- #
# C-4 — zero project-side storage, zero project-side read points
# --------------------------------------------------------------------------- #
def test_memory_tree_stores_no_unit_to_class_mapping() -> None:
    offenders: list[str] = []
    for path in sorted(MEMORY_DIR.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(REPO_ROOT).as_posix()
        if re.search(r"flow[-_]class", path.name):
            offenders.append(f"{rel} (category-store file name)")
            continue
        if path.suffix in STRUCTURED_SUFFIXES:
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "flow_class" in text:
                offenders.append(f"{rel} (structured flow_class data)")
            continue
        if path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if LEDGER_HEADER in text or LEDGER_ROW_RE.search(text):
            offenders.append(f"{rel} (ledger-shaped rows)")
    assert not offenders, (
        "a project-side category store appeared under .specify/memory/ "
        f"(contract C-4): {offenders}"
    )


def test_engine_reads_no_project_side_memory() -> None:
    text = _read(ENGINE, "scripts/python/flow-class-check.py")
    assert ".specify/memory" not in text, (
        "the engine must not read project-side memory (contract C-4); "
        "the only lookup path is the framework owner"
    )


# --------------------------------------------------------------------------- #
# T011 / P1, P3, P4 — owner pointer convergence
# --------------------------------------------------------------------------- #
def test_owner_drops_every_069b_handoff_pointer() -> None:
    text = _read(OWNER, "flow-class-definitions.md")
    assert "069b 承接" not in text, (
        "the owner must not keep a '069b 承接' handoff pointer once 069b has "
        "landed; point at the landed mapping / boundary / gate owners instead"
    )
    assert "069b承接" not in text


def test_owner_literal_registry_names_the_parent_spec_as_semantic_owner() -> None:
    text = _read(OWNER, "flow-class-definitions.md")
    opening = "\n".join(text.splitlines()[:12])
    missing = [phrase for phrase in PARENT_OWNER_PHRASES if phrase not in opening]
    assert not missing, (
        "the literal registry (§ opening block) must declare the parent spec as "
        f"the semantic owner with the 069a/069b tables as projections; missing {missing}"
    )


def test_owner_ownership_section_never_reads_a_project_record() -> None:
    text = _read(OWNER, "flow-class-definitions.md")
    section = _section(text, "所有权")
    assert section is not None, "the owner must keep the § 所有权 section"
    assert "MAY" in section, "the § 所有权 section must keep the MAY declaration"
    missing = [phrase for phrase in PROJECT_SPACE_PHRASES if phrase not in section]
    assert not missing, (
        "§ 所有权 must state that a project MAY record the class in its own "
        f"knowledge space while the framework never reads it; missing {missing}"
    )
    assert any(phrase in section for phrase in GATE_EFFECT_PHRASES), (
        "§ 所有权 must state that a project-side record never changes / affects "
        "a gate"
    )


def test_mixed_oracle_rows_point_at_the_landed_contract() -> None:
    text = _read(OWNER, "flow-class-definitions.md")
    header, rows = _table_after(text, "unit_id")
    assert header == ["unit_id", "flow_class", "basis", "neutral", "notes"], (
        f"unexpected ledger header: {header}"
    )
    mixed = [row for row in rows if len(row) >= 5 and row[2] == "mixed-oracle"]
    assert mixed, "the ledger must keep its mixed-oracle rows"
    assert "contracts/ledger-reconciler.md" in text, (
        "the owner must point at the landed mixed-oracle contract "
        "(contracts/ledger-reconciler.md) instead of the 069b handoff"
    )
    assert "C-7" in text, "the pointer must name the landed clause C-7"
    offenders = [
        row[0]
        for row in mixed
        if "ledger-reconciler.md" not in row[4] or "C-7" not in row[4]
    ]
    assert not offenders, (
        "every mixed-oracle ledger row's notes must point at "
        f"contracts/ledger-reconciler.md C-7; offenders: {offenders}"
    )
    assert all(row[1] == "execution" for row in mixed), (
        "mixed-oracle rows stay execution — only the pointer may change"
    )


# --------------------------------------------------------------------------- #
# C-6 — the three SC-002 samples are frozen with all declared fields
# --------------------------------------------------------------------------- #
def test_migration_samples_freeze_three_complete_rows() -> None:
    text = _read(SAMPLES, "notes/migration-samples.md")
    header, rows = _table_after(text, "#")
    assert header, "migration-samples.md must carry the frozen sample table"
    for fragment in SAMPLE_COLUMNS:
        assert any(fragment in cell for cell in header), (
            f"sample table header must carry a {fragment!r} column: {header}"
        )
    index = {cell: position for position, cell in enumerate(header)}

    def column(row: list[str], fragment: str) -> str:
        for cell, position in index.items():
            if fragment in cell:
                return row[position] if position < len(row) else ""
        return ""

    assert len(rows) == 3, f"exactly three frozen samples are expected, got {len(rows)}"
    for row in rows:
        project = column(row, "项目")
        head = column(row, "HEAD")
        branch = column(row, "分支")
        dirty = column(row, "工作树脏文件")
        payload = column(row, "载荷")
        suite = column(row, "套件命令")
        assert project, f"sample row missing project: {row}"
        assert re.fullmatch(r"`?[0-9a-f]{7,40}`?", head), (
            f"sample row missing a commit HEAD: {row}"
        )
        assert branch, f"sample row missing branch: {row}"
        assert dirty.isdigit(), f"sample row dirty-file count must be a number: {row}"
        assert payload in {"无", "有"}, (
            f"sample row payload status must be 无/有: {row}"
        )
        assert suite, f"sample row missing suite command: {row}"


# --------------------------------------------------------------------------- #
# C-7 / C-8 — the name-level snapshot outcome is recorded, never a failure count
# --------------------------------------------------------------------------- #
def test_quickstart_records_name_level_snapshot_outcomes() -> None:
    text = _read(QUICKSTART, "notes/quickstart-run.md")
    section = _section(text, "场景 6")
    assert section is not None, (
        "notes/quickstart-run.md must carry § 场景 6 (migration & distribution)"
    )
    for project in ("xuanji-agent", "xuanji-cli", "xuanji-function"):
        assert project in section, f"scenario 6 must record the {project} snapshot"
        rows = [
            line
            for line in section.splitlines()
            if line.strip().startswith("|") and project in line
        ]
        verdicts = [
            line
            for line in rows
            if "comm -13" in line
            or "not-evaluated" in line
            or "零新增" in line
        ]
        assert verdicts, (
            f"{project} needs a result row carrying the name-level comparison "
            f"(comm -13) or a not-evaluated reason; rows were: {rows}"
        )
        line = verdicts[0]
        if "not-evaluated" in line:
            assert re.search(r"not-evaluated[（(][^）)]+[）)]", line), (
                f"{project} not-evaluated must carry a reason: {line}"
            )
        else:
            assert re.search(r"(?:comm -13[^|]*空|零新增)", line), (
                f"{project} must record an empty comm -13 (zero new failing "
                f"node ids), never a failure count: {line}"
            )


# --------------------------------------------------------------------------- #
# C-12 — the refreshed payload is executed, not merely present
# --------------------------------------------------------------------------- #
def test_migration_samples_record_the_payload_smoke() -> None:
    text = _read(SAMPLES, "notes/migration-samples.md")
    section = _section(text, "2026-10-25 刷新载荷冒烟")
    assert section, (
        "notes/migration-samples.md must record the post-refresh payload smoke "
        "(C-12); file presence alone is not evidence"
    )
    for project in ("xuanji-agent", "xuanji-cli", "xuanji-function"):
        rows = [
            line
            for line in section.splitlines()
            if line.strip().startswith("|") and project in line
        ]
        assert rows, f"the payload-smoke table must carry a {project} row: {section}"
        row = rows[0]
        assert "exit 0" in row, f"{project} must record the lookup exit code: {row}"
        assert "framework-source-required" in row, (
            f"{project} must record the framework-only actions' named refusal: {row}"
        )
        assert "reader-oracle" in section or "mixed-oracle" in section, (
            "the lookup assertions must record the resolved class/basis, not just exit 0"
        )


def test_quickstart_records_the_payload_smoke_for_every_snapshot() -> None:
    text = _read(QUICKSTART, "notes/quickstart-run.md")
    section = _section(text, "6.3b")
    assert section, (
        "notes/quickstart-run.md § 场景 6 must carry 6.3b (payload smoke) — the "
        "product suite never loads specify or .specify/"
    )
    for project in ("xuanji-agent", "xuanji-cli", "xuanji-function"):
        assert project in section, f"6.3b must record the {project} payload smoke"
    assert "framework-source-required" in section, (
        "6.3b must record that the framework-only actions exit 2 with a named label"
    )
    assert "source=ledger" in section, (
        "6.3b must record that lookup resolved the class from the installed owner"
    )

if __name__ == "__main__":  # pragma: no cover - manual red/green runs
    raise SystemExit(pytest.main([__file__, "-q", "-p", "no:cacheprovider"]))
