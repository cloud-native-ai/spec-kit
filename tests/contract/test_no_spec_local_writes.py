"""Structural invariant: no code path writes a spec-local goal or team tree (FR-013, SC-002).

Feature 094, tasks rows T076 / T077, contracts `owner-rewrites-and-tests.md` C-106 / C-108.
The engine's **action table** (its module docstring's Read/Write groups, projected into the
parser's `--help`) is the one enumerable place a writing surface may live: every write
action is derived from it, the three archive roots are pinned, and no function that
performs a write may reference the spec-local tree. The prose surfaces that persist or
instruct a definition write — the `create-team` persistence step and the driver
instructions — are scanned for the retired spec-local targets directly.

The mutation arms (T077) re-run the same checkers over in-memory reverted copies — no tree
edit — and re-inject one retired classification phrase into a copy of the C-107 vocabulary
scan's input, proving both guards go red when their implementation is removed.
"""

from __future__ import annotations

import ast
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"

#: The three sanctioned roots — the only destinations a definition write may resolve to.
SANCTIONED_ROOTS = {
    "ARCHIVE_DIRNAME": ".specify/anchoring",
    "TEAM_DIRNAME": ".specify/teams",
    "ARCHIVE_HISTORY_DIRNAME": ".specify/archive/goal-team",
}

#: The engine's writing actions, derived from the action table and pinned so a new write
#: action cannot appear without this module re-reading it.
EXPECTED_WRITE_ACTIONS = {
    "create", "status", "objective", "criteria", "targets", "migrate", "bind",
    "migrate-archive", "backfill-bindings", "handoff-ref",
}

WRITE_PRIMITIVES = {
    "write_text", "write_bytes", "mkdir", "rename", "replace", "move", "unlink",
    "rmdir", "rmtree", "copy", "copy2", "copytree", "touch", "symlink_to",
}

#: A spec-local definition path, as written in prose or in code.
SPEC_LOCAL = re.compile(
    r"(?:\.specify/specs/[^\s`'\"()]+|<spec-dir>)/(?:goal|team)(?:/|\b)")

CREATE_TEAM_SURFACES = (
    REPO_ROOT / "skills/internal/create-team/SKILL.md",
    REPO_ROOT / "skills/internal/create-team/references/create-mode.md",
)
DRIVER_SURFACES = (
    REPO_ROOT / "skills/external/sdd-loop-driver/SKILL.md",
    REPO_ROOT / "skills/external/sdd-loop-driver/references/checkpoint-protocol.md",
)
SANITIZE_TEMPLATE = REPO_ROOT / "templates/commands/sanitize.md"


def _read(path: Path) -> str:
    assert path.is_file(), f"surface missing: {path}"
    return path.read_text(encoding="utf-8")


def _table_actions(source: str) -> dict[str, str]:
    """Parse the docstring action table: action name -> read|write."""
    doc = ast.get_docstring(ast.parse(source)) or ""
    actions: dict[str, str] = {}
    mode = None
    for line in doc.splitlines():
        header = re.match(r"^(Read|Write) group", line)
        if header:
            mode = header.group(1).lower()
            continue
        if line.startswith("Exit codes:"):
            break
        if mode:
            match = re.match(r"^\s{2}([a-z][a-z-]*)\b", line)
            if match:
                actions[match.group(1)] = mode
    return actions


def _help_actions() -> dict[str, str]:
    """Parse the same table as the parser projects it (the public surface)."""
    proc = subprocess.run([sys.executable, str(ENGINE), "--help"],
                          capture_output=True, text=True, cwd=REPO_ROOT)
    assert proc.returncode == 0, f"engine --help failed: {proc.stderr}"
    actions: dict[str, str] = {}
    for line in proc.stdout.splitlines():
        match = re.match(r"^\s{2,}([a-z][a-z-]+)\s{2,}(.*)$", line)
        if not match:
            continue
        name, desc = match.group(1), match.group(2)
        if not desc.startswith(("read", "write")):
            continue
        actions[name] = "write" if re.search(r"\bwrite\b", desc) else "read"
    return actions


def _constant_violations(source: str) -> list[str]:
    violations = []
    for name, expected in SANCTIONED_ROOTS.items():
        match = re.search(rf"(?m)^{name}\s*=\s*[\"']([^\"']+)[\"']", source)
        if match is None:
            violations.append(f"{name} is not declared as a literal root")
        elif match.group(1) != expected:
            violations.append(
                f"{name} is {match.group(1)!r}, not the sanctioned root {expected!r}")
    return violations


def _has_write_primitive(node: ast.AST) -> bool:
    for sub in ast.walk(node):
        if not isinstance(sub, ast.Call):
            continue
        func = sub.func
        name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
        if name in WRITE_PRIMITIVES:
            return True
    return False


def _engine_violations(source: str) -> list[str]:
    """Every violation a reverted engine surface would produce, as data."""
    violations = _constant_violations(source)

    table = _table_actions(source)
    writes = {name for name, mode in table.items() if mode == "write"}
    if writes != EXPECTED_WRITE_ACTIONS:
        violations.append(
            f"the action table's write set changed: {sorted(writes)} vs the pinned "
            f"{sorted(EXPECTED_WRITE_ACTIONS)} — re-read this invariant")
    for name, mode in table.items():
        if mode == "read" and name in EXPECTED_WRITE_ACTIONS:
            violations.append(f"{name} is classified read in the action table")

    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not _has_write_primitive(node):
            continue
        segment = ast.get_source_segment(source, node) or ""
        for hint in ("_specs_root", ".specify/specs", '"specs"'):
            if hint in segment:
                violations.append(
                    f"function {node.name!r} (line {node.lineno}) writes and references "
                    f"the spec-local tree via {hint!r}")
    return violations


def _prose_hits(text: str) -> list[str]:
    return [f"line {lineno}: {line.strip()[:140]}"
            for lineno, line in enumerate(text.splitlines(), 1)
            if SPEC_LOCAL.search(line)]


def _surface_texts() -> dict[str, str]:
    surfaces = {"engine": _read(ENGINE)}
    for label, paths in (("create-team", CREATE_TEAM_SURFACES),
                         ("driver", DRIVER_SURFACES)):
        surfaces[label] = "\n".join(_read(path) for path in paths)
    return surfaces


# ---------------------------------------------------------------------------
# T076 / C-106 — the structural invariant over the engine, create-team and the driver
# ---------------------------------------------------------------------------

def test_no_writing_surface_targets_a_spec_local_goal_or_team():
    surfaces = _surface_texts()

    # 1. The engine's action table covers every parser action, and its write set is the
    #    pinned one; every writing function stays clear of the spec-local tree. Read
    #    actions may be documented in more depth than the table lists, but a write action
    #    the parser accepts without a table row would be a writing surface outside the
    #    one enumerable place — that is the divergence this assertion refuses.
    table = _table_actions(surfaces["engine"])
    help_table = _help_actions()
    parser_writes = {name for name, mode in help_table.items() if mode == "write"}
    table_writes = {name for name, mode in table.items() if mode == "write"}
    assert parser_writes == table_writes == EXPECTED_WRITE_ACTIONS, (
        "the engine's write actions and its action table disagree — the table is the "
        f"one enumerable place a writing surface may live; parser={sorted(parser_writes)} "
        f"table={sorted(table_writes)} pinned={sorted(EXPECTED_WRITE_ACTIONS)}")
    dangling = sorted(set(table) - set(help_table))
    assert not dangling, f"the action table names actions the parser does not accept: {dangling}"
    assert not _engine_violations(surfaces["engine"]), "\n".join(
        _engine_violations(surfaces["engine"]))

    # 2. The create-team persistence step lands in the team archive layer only.
    assert not _prose_hits(surfaces["create-team"]), (
        "the create-team persistence step names a spec-local definition target:\n"
        + "\n".join(_prose_hits(surfaces["create-team"])))
    assert ".specify/teams/<slug>/team.md" in surfaces["create-team"], (
        "create-mode.md must declare the team archive as the persistence landing point")

    # 3. The driver instructions name the two archive layers and no spec-local target.
    assert not _prose_hits(surfaces["driver"]), (
        "the driver instructions name a spec-local definition target:\n"
        + "\n".join(_prose_hits(surfaces["driver"])))
    for landing in (".specify/anchoring/<slug>/goal.md", ".specify/teams/<slug>/team.md"):
        assert landing in surfaces["driver"], (
            f"the driver instructions must name the archive landing {landing}")


# ---------------------------------------------------------------------------
# T077 / C-108 — the guard goes red when one writing surface is reverted
# ---------------------------------------------------------------------------

def test_the_guard_goes_red_when_one_surface_is_reverted():
    engine = _read(ENGINE)
    assert not _engine_violations(engine), "baseline engine surface is already red"

    reverted = engine.replace(
        'ARCHIVE_DIRNAME = ".specify/anchoring"',
        'ARCHIVE_DIRNAME = ".specify/specs/900-fixture/goal"', 1)
    assert reverted != engine, "synthetic mutation did not apply"
    reverted_violations = _engine_violations(reverted)
    assert reverted_violations, (
        "the guard stayed green after the engine's goal root was reverted to a "
        "spec-local tree")
    assert any("ARCHIVE_DIRNAME" in row for row in reverted_violations)

    create_mode = _read(CREATE_TEAM_SURFACES[1])
    assert not _prose_hits(create_mode), "baseline create-mode surface is already red"
    reverted_prose = create_mode.replace(
        ".specify/teams/<slug>/team.md",
        ".specify/specs/900-fixture/team/<slug>/team.md")
    assert reverted_prose != create_mode, "synthetic prose mutation did not apply"
    assert _prose_hits(reverted_prose), (
        "the scan stayed green after the create-team persistence step was reverted to "
        "a spec-local target")


# ---------------------------------------------------------------------------
# T077 / C-108 — the C-107 vocabulary scan goes red when one old phrase returns
# ---------------------------------------------------------------------------

def _load_sibling(name: str):
    path = Path(__file__).with_name(f"{name}.py")
    spec = importlib.util.spec_from_file_location(f"_094_{name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _criterion_hits_in(text: str, scan) -> list[str]:
    hits = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if any(token in line for token in scan.TEMP_DIR_TOKENS):
            continue
        for name, pattern in scan.CRITERION_PATTERNS:
            if pattern.search(line):
                hits.append(f"line {lineno} [{name}]: {line.strip()[:120]}")
    return hits


def test_the_vocabulary_scan_goes_red_when_one_old_phrase_is_re_injected():
    scan = _load_sibling("test_criterion_vocabulary_scan")
    surface = _read(REPO_ROOT / "skills/internal/manage-goal/SKILL.md")
    assert not _criterion_hits_in(surface, scan), (
        "the scanned surface is already red under the C-107 patterns")

    mutated = surface + "\nA temporary goal is created for one run only.\n"
    assert _criterion_hits_in(mutated, scan), (
        "re-injecting one retired classification phrase into a scanned surface did not "
        "turn the C-107 vocabulary scan red")


# ---------------------------------------------------------------------------
# T078 / FR-030 — /speckit.sanitize renders the residual reading without migrating
# ---------------------------------------------------------------------------

def test_the_sanitize_template_renders_the_probe_without_migrating():
    text = _read(SANITIZE_TEMPLATE)
    assert "probe-residual" in text, (
        "the sanitize template must name the read-only residual probe action")
    assert "goal-utils.py" in text, (
        "the action owner (the goal engine) must be cited for the probe")
    assert "goal-utils.py probe-residual" in text, (
        "the probe must be the engine's read action, invoked through it")
    assert "goal-utils.py migrate-archive" not in text, (
        "the migration entry belongs to /speckit.goal; /speckit.sanitize must invoke "
        "no migration action")
    assert "/speckit.goal" in text, (
        "the template must point to the migration/creation entry that owns the write")
    assert "只读" in text or "read-only" in text, (
        "the template must state that the residual reading is read-only")
    assert "逐字" in text or "verbatim" in text, (
        "the template must render the reading verbatim")
    assert ".specify/.tmp/" in text, (
        "the template must state that the run scratch area is outside the reading")
