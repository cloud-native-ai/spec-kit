"""Contract tests: the migrate engine's declared domain and reuse boundaries (097 T013).

Green claims: contracts/migrate-engine.md C-1 (dimension set/order), C-2
(expected-state sources), C-3 (disposition mapping domain).

The discriminative power of the five source guards is proven inside this suite:
each guard runs against the real ``MIGRATE-ENGINE`` segment (must stay clean)
and against a synthetic second implementation injected in-test (must be
reported). A guard that stays silent on its mutation, or a real source that
grows a second implementation, turns the suite red (DoD-3).
"""

import importlib.util
import inspect
import re
import shutil
from pathlib import Path

import pytest

import specify_cli

ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = ROOT / ".specify" / "specs" / "097-speckit-migrate-command"
SOURCE_PATH = ROOT / "src" / "specify_cli" / "__init__.py"

SEGMENT_RE = re.compile(
    r"# MIGRATE-ENGINE:START(.*?)# MIGRATE-ENGINE:END", re.DOTALL
)
STRING_LITERAL_RE = re.compile(r'"([^"\n]*)"|\'([^\'\n]*)\'')


def _source() -> str:
    return SOURCE_PATH.read_text(encoding="utf-8")


def _segment(source: str) -> str:
    matches = SEGMENT_RE.findall(source)
    assert len(matches) == 1, (
        "expected exactly one MIGRATE-ENGINE:START/END pinned segment in "
        "src/specify_cli/__init__.py"
    )
    return matches[0]


def _engine_module(filename: str):
    path = Path(specify_cli.get_resource_path()) / "scripts" / "python" / filename
    module_name = "_migrate_contract_" + path.stem.replace("-", "_")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _builders():
    path = Path(__file__).resolve().parents[1] / "fixtures" / "migrate-097" / "builders.py"
    spec = importlib.util.spec_from_file_location("_migrate_097_builders_contract", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _string_literals(text: str) -> set:
    literals = set()
    for double, single in STRING_LITERAL_RE.findall(text):
        literals.add(double or single)
    return literals


# ---------------------------------------------------------------------------
# Source guards — callables over source text; empty list == clean
# ---------------------------------------------------------------------------

REGEX_CALL_RE = re.compile(r"re\.(?:sub|subn|compile)\(\s*r?(\"[^\"\n]*\"|'[^'\n]*')")
PATH_REWRITE_MARKERS = ("memory/", "skills/internal", "skills/external", ".specify/")
COMMAND_RENDER_MARKERS = ("AUTO-GENERATED", "speckit.{")
MIRROR_PAIR_TUPLE_RE = re.compile(
    r"\(\s*[\"'](?:templates|skills/external|skills/internal|agents|scripts|shared)[\"']\s*,"
)
OBSOLETE_ASSIGNMENT_RE = re.compile(r"^\s*_OBSOLETE_\w+\s*=", re.MULTILINE)


def guard_second_path_rewrite(text: str) -> list:
    violations = []
    for match in REGEX_CALL_RE.finditer(text):
        pattern = match.group(1)
        if any(marker in pattern for marker in PATH_REWRITE_MARKERS):
            violations.append(f"second path-rewrite regex: {pattern}")
    return violations


def guard_second_command_renderer(text: str) -> list:
    return [
        f"second command renderer marker: {marker!r}"
        for marker in COMMAND_RENDER_MARKERS
        if marker in text
    ]


def guard_second_link_roster(text: str) -> list:
    roster = tuple(_engine_module("sanitize-utils.py").COMPAT_SYMLINKS)
    found = sorted(name for name in roster if name in _string_literals(text))
    if len(found) >= 2:
        return [f"second compat-link roster: {found}"]
    return []


def guard_second_mirror_pair_roster(text: str) -> list:
    sources = tuple(src for src, _mirror, *_rest in
                    _engine_module("sync-mirrors.py").MIRROR_PAIRS)
    found = sorted(src for src in sources if src in _string_literals(text))
    violations = []
    if len(found) >= 2:
        violations.append(f"second mirror-pair roster: {found}")
    if MIRROR_PAIR_TUPLE_RE.search(text):
        violations.append("mirror-pair tuple literal inside the migrate segment")
    return violations


def guard_second_obsolete_roster(text: str) -> list:
    violations = []
    if OBSOLETE_ASSIGNMENT_RE.search(text):
        violations.append("defines an _OBSOLETE_* roster inside the migrate segment")
    names = set(specify_cli._OBSOLETE_SKILLS)
    found = sorted(name for name in names if name in _string_literals(text))
    if len(found) >= 3:
        violations.append(f"second obsolete registry roster: {found[:3]}…")
    return violations


GUARD_CASES = [
    pytest.param(
        guard_second_path_rewrite,
        'SECOND_PATH_RE = re.compile(r"(?<![\\w./-])memory/features/")\n',
        id="path-rewrite",
    ),
    pytest.param(
        guard_second_command_renderer,
        'MARKER = "AUTO-GENERATED from templates/commands/x.md — do not edit"\n',
        id="command-renderer",
    ),
    pytest.param(
        guard_second_link_roster,
        'COMPAT = ["CLAUDE.md", "QODER.md"]\n',
        id="link-roster",
    ),
    pytest.param(
        guard_second_mirror_pair_roster,
        'PAIRS = [("skills/external", ".specify/skills")]\n',
        id="mirror-pair-roster",
    ),
    pytest.param(
        guard_second_obsolete_roster,
        '_OBSOLETE_SKILLS = ("agent-setup", "cli-setup", "docx-utils")\n',
        id="obsolete-roster",
    ),
]


# ---------------------------------------------------------------------------
# Pinned segment + declared domains
# ---------------------------------------------------------------------------


def test_migrate_segment_is_pinned_and_non_empty():
    segment = _segment(_source())
    assert len(segment) >= 500, "the pinned migrate segment is suspiciously small"
    assert "MIGRATE_DIMENSIONS" in segment
    assert "MIGRATE_DISPOSITIONS" in segment
    assert "migrate_receipts_dir" in segment


def test_migrate_segment_has_no_specify_version_marker():
    segment = _segment(_source())
    assert ".specify/version" not in segment, (
        "FR-005/FR-020: no .specify/version marker may drive any branch"
    )


def test_dimension_tokens_and_order_come_from_data_model_e8():
    text = (SPEC_DIR / "data-model.md").read_text(encoding="utf-8")
    section = text[text.index("## E-8"):text.index("## E-9")]
    e8 = tuple(re.findall(r"^\| `([a-z-]+)` \|", section, re.MULTILINE))
    assert e8, "E-8 dimension rows are not readable from data-model.md"
    assert tuple(specify_cli.MIGRATE_DIMENSIONS) == e8


def test_disposition_domain_extracted_from_fr014_byte_for_byte():
    text = (SPEC_DIR / "requirements.md").read_text(encoding="utf-8")
    line = next(
        line for line in text.splitlines() if line.startswith("- **FR-014**:")
    )
    tokens = []
    for token in re.findall(r"`([a-z]+)`", line):
        if token not in tokens:
            tokens.append(token)
    assert tuple(tokens) == tuple(specify_cli.MIGRATE_DISPOSITIONS), (
        f"FR-014 declares {tokens}; the executable mirror reads "
        f"{tuple(specify_cli.MIGRATE_DISPOSITIONS)}"
    )


# ---------------------------------------------------------------------------
# Five source guards: clean on the real segment, loud on injected mutations
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("guard,mutation", GUARD_CASES)
def test_guard_is_clean_on_real_segment(guard, mutation):
    section = _segment(_source())
    assert guard(section) == [], (
        f"{guard.__name__} reports a second implementation in the real migrate "
        f"segment: {guard(section)}"
    )


@pytest.mark.parametrize("guard,mutation", GUARD_CASES)
def test_guard_reports_injected_second_implementation(guard, mutation):
    violations = guard(mutation)
    assert violations, (
        f"{guard.__name__} stayed silent on its synthetic second "
        "implementation — the guard has no discriminative power"
    )


# ---------------------------------------------------------------------------
# Init <-> migrate decision equivalence on one declaration-driven fixture
# ---------------------------------------------------------------------------


@pytest.mark.contract
def test_init_and_migrate_share_one_decision_function(tmp_path):
    builders = _builders()
    workspace = builders.build_legacy_project(tmp_path / "legacy")

    obsolete_decisions = specify_cli.plan_obsolete_framework_asset_removals(
        workspace, "qoder"
    )
    assert obsolete_decisions, "legacy fixture yields no obsolete-asset decision"
    cleanup_copy = tmp_path / "init-cleanup"
    shutil.copytree(workspace, cleanup_copy, symlinks=True)
    removed = {
        str(Path(path)) for path in
        specify_cli.cleanup_obsolete_framework_assets(cleanup_copy, "qoder")
    }
    assert removed == {decision["path"] for decision in obsolete_decisions}

    flat_decisions = specify_cli.plan_flat_internal_skill_migrations(workspace)
    assert flat_decisions, "legacy fixture yields no flat-internal decision"
    flat_copy = tmp_path / "init-flat"
    shutil.copytree(workspace, flat_copy, symlinks=True)
    flat_result = specify_cli.migrate_flat_internal_skills(flat_copy)
    assert {d["path"] for d in flat_decisions if d["action"] == "move"} == set(
        flat_result["moved"]
    )
    assert {
        d["path"] for d in flat_decisions if d["action"] == "remove-stale"
    } == set(flat_result["removed_stale"])

    cleanup_source = inspect.getsource(
        specify_cli.cleanup_obsolete_framework_assets
    )
    flat_source = inspect.getsource(specify_cli.migrate_flat_internal_skills)
    assert "plan_obsolete_framework_asset_removals(" in cleanup_source
    assert "plan_flat_internal_skill_migrations(" in flat_source
