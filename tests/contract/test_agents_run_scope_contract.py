"""Contract tests for change-set containment and the zero-second-mechanism bounds
(104-agents-run, US3 — SC-005 / INV-12).

Clause source: .specify/specs/104-agents-run/requirements.md SC-005 and
contracts/agents-run-dispatch.contract.md C-22.

This module is a **containment guard** (migration/regression exception, no red-first step):
the red form is a change set that carries a forbidden path, demonstrated by the synthetic
fixture legs below. The comparison unit is the five product-surface roots of SC-005; the
process / evidence / registry paths (`.specify/specs/104-agents-run/**`,
`.specify/features.md`, `.specify/features/019-agents-command.md`, `.specify/memory/**`,
`.specify/state/**`) sit outside that unit and never enter the complement assertion.

The live judgement runs `git diff <base>..HEAD`, base = the implement-entry commit recorded
in `notes/pre-change-measurements.md`; the closure stage re-runs the same module after every
product commit has landed, so the final reading covers the whole change set.

Clause-class honesty (FR-023): this module pins structural facts only (path sets, added-file
censuses, owner-file invariance); it does not claim contract coverage of runtime behaviour.
Behavior-class clauses are evidenced by truth-source text + review + mutation drill.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
PRE_CHANGE_NOTE = (
    REPO_ROOT / ".specify" / "specs" / "104-agents-run" / "notes" / "pre-change-measurements.md"
)

# SC-005 comparison unit: the five product-surface roots (closed set).
PRODUCT_ROOTS = (
    "templates/commands/",
    "skills/internal/",
    "docs/reference/commands/",
    "docs/reference/agents/",
    "docs/tutorials/",
    "tests/",
    ".claude/commands/speckit.agents",
    ".github/prompts/speckit.agents",
    ".qoder/commands/speckit.agents",
    ".opencode/command/speckit.agents",
    ".specify/skills/internal/run-agent/",
)

# The allowed differences inside the comparison unit: the fan-out closure of the edited
# sources (SC-005). `tests/**` stays a class-level allow because SC-005 names it as a root;
# the added-file census below narrows what may be *new* there.
ALLOWED_EXACT = frozenset(
    {
        "templates/commands/agents.md",
        "docs/reference/commands/agents.md",
        "docs/reference/agents/command-and-skills.md",
        "docs/reference/agents/overview.md",
        "docs/reference/agents/design.md",
        "docs/tutorials/installation.md",
        "docs/tutorials/quickstart.md",
    }
)
ALLOWED_PREFIXES = (
    "skills/internal/run-agent/",
    "tests/",
    ".claude/commands/speckit.agents",
    ".github/prompts/speckit.agents",
    ".qoder/commands/speckit.agents",
    ".opencode/command/speckit.agents",
    ".specify/skills/internal/run-agent/",
)

EXPECTED_NEW_MODULES = frozenset(
    {
        "tests/contract/test_agents_run_command_contract.py",
        "tests/contract/test_agents_run_docs_contract.py",
        "tests/contract/test_agents_run_multi_child_edges.py",
        "tests/contract/test_agents_run_scope_contract.py",
        "tests/contract/test_agents_run_skill_wiring.py",
    }
)

PROCESS_EVIDENCE_REGISTRY_PREFIXES = (
    ".specify/specs/104-agents-run/",
    ".specify/features/",
    ".specify/memory/",
    ".specify/state/",
)
PROCESS_EVIDENCE_REGISTRY_EXACT = frozenset(
    {
        ".specify/features.md",
        ".specify/features/019-agents-command.md",
    }
)


def _base_commit() -> str:
    text = PRE_CHANGE_NOTE.read_text(encoding="utf-8")
    match = re.search(r"\$ git rev-parse --short HEAD\n([0-9a-f]{7,40})", text)
    assert match, (
        "the implement-entry base commit is not recorded in notes/pre-change-measurements.md"
    )
    return match.group(1)


def _change_set() -> list[tuple[str, str]]:
    result = subprocess.run(
        ["git", "diff", "--name-status", f"{_base_commit()}..HEAD"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "git diff failed:\n" + result.stderr
    entries = []
    for line in result.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        entries.append((parts[0].strip(), parts[-1].strip()))
    return entries


def _in_comparison_unit(path: str) -> bool:
    return any(path == root or path.startswith(root) for root in PRODUCT_ROOTS)


def _is_allowed(path: str) -> bool:
    return path in ALLOWED_EXACT or any(path.startswith(prefix) for prefix in ALLOWED_PREFIXES)


def _exempt(path: str) -> bool:
    return path in PROCESS_EVIDENCE_REGISTRY_EXACT or any(
        path.startswith(prefix) for prefix in PROCESS_EVIDENCE_REGISTRY_PREFIXES
    )


def judge_change_set(entries: list[tuple[str, str]]) -> list[str]:
    """The complement: paths inside the comparison unit that the allowed closure excludes."""
    complement = set()
    for _status, path in entries:
        if _exempt(path):
            continue
        if not _in_comparison_unit(path):
            continue
        if not _is_allowed(path):
            complement.add(path)
    return sorted(complement)


@pytest.fixture(scope="module")
def change_set() -> list[tuple[str, str]]:
    return _change_set()


def test_live_change_set_complement_is_empty(change_set):
    """SC-005: inside the five product-surface roots, nothing falls outside the closure."""
    complement = judge_change_set(change_set)
    assert complement == [], (
        "the change set carries product paths outside the allowed closure: %s" % complement
    )


def test_containment_red_form_forbidden_paths():
    """Red form demo: a forbidden product path inside the unit lands in the complement."""
    fixture = [
        ("M", "templates/commands/team.md"),                     # sibling command edited
        ("A", "templates/commands/new-command.md"),              # a new /speckit.* command
        ("M", "docs/reference/agents/templates-and-agents.md"),  # unnamed doc surface
        ("A", "skills/internal/create-agent/new-skill.md"),      # a new skill file
        ("M", "docs/tutorials/unrelated.md"),                    # unnamed tutorial
    ]
    complement = judge_change_set(fixture)
    assert complement == sorted(path for _status, path in fixture)


def test_containment_exempts_flow_evidence_and_registry_paths():
    """Process / evidence / registry paths are outside the unit and never judged."""
    fixture = [
        ("M", ".specify/specs/104-agents-run/tasks.md"),
        ("A", ".specify/specs/104-agents-run/test-evidence/implement.jsonl"),
        ("M", ".specify/features.md"),
        ("M", ".specify/features/019-agents-command.md"),
        ("A", ".specify/memory/feedback/entry.md"),
        ("M", ".specify/state/104-agents-run.md"),
    ]
    assert judge_change_set(fixture) == []


def test_containment_allows_the_declared_closure():
    """The edited sources and their fan-out products stay inside the allowed closure."""
    fixture = [
        ("M", "templates/commands/agents.md"),
        ("M", "skills/internal/run-agent/SKILL.md"),
        ("A", "skills/internal/run-agent/references/new-note.md"),
        ("M", "docs/reference/commands/agents.md"),
        ("M", "docs/reference/agents/command-and-skills.md"),
        ("M", "docs/reference/agents/overview.md"),
        ("M", "docs/reference/agents/design.md"),
        ("M", "docs/tutorials/installation.md"),
        ("M", "docs/tutorials/quickstart.md"),
        ("A", "tests/contract/test_agents_run_scope_contract.py"),
        ("M", "tests/scenarios/agents-command/single-entry-routing-scenario.md"),
        ("M", ".claude/commands/speckit.agents.md"),
        ("M", ".github/prompts/speckit.agents.prompt.md"),
        ("M", ".qoder/commands/speckit.agents.md"),
        ("M", ".opencode/command/speckit.agents.md"),
        ("M", ".specify/skills/internal/run-agent/SKILL.md"),
    ]
    assert judge_change_set(fixture) == []


def test_zero_new_commands_and_skills(change_set):
    """INV-12: no new command surface and no new skill file enters the change set."""
    added_commands = [p for s, p in change_set if s == "A" and p.startswith("templates/commands/")]
    added_skills = [p for s, p in change_set if s == "A" and p.startswith("skills/")]
    assert added_commands == [], "a new /speckit.* command template was added: %s" % added_commands
    assert added_skills == [], "a new skill file was added: %s" % added_skills
    added_tests = {p for s, p in change_set if s == "A" and p.startswith("tests/")}
    unexpected = sorted(added_tests - EXPECTED_NEW_MODULES)
    assert unexpected == [], (
        "new test files beyond the five declared modules: %s" % unexpected
    )


def test_engine_owner_and_glossary_roots_untouched(change_set):
    """INV-12: no new engine/renderer/scheduler/queue, no owner edit, no glossary entry."""
    forbidden = []
    for status, path in change_set:
        if path.startswith(("scripts/", "src/", "shared/", ".specify/shared/")):
            forbidden.append(path)
        if path == "templates/" or (path.startswith("templates/")
                                    and not path.startswith("templates/commands/")):
            forbidden.append(path)
        if path == ".specify/glossary.md":
            forbidden.append(path)
    assert forbidden == [], (
        "the change set touches an owner/engine/glossary surface: %s" % sorted(forbidden)
    )


def test_history_forbidden_surface_is_not_edited(change_set):
    """C-34: dated history records stay read-only."""
    edited = [p for _s, p in change_set if p.startswith("docs/reference/history/")]
    status = subprocess.run(
        ["git", "status", "--porcelain", "--", "docs/reference/history/"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert status.returncode == 0, status.stderr
    assert edited == [], "a dated history record was committed: %s" % edited
    assert status.stdout.strip() == "", (
        "a dated history record carries working-tree changes:\n" + status.stdout
    )


def test_behavior_class_honesty_label():
    """C-22: no new module claims contract-level coverage of behavior-class clauses."""
    phrase = "contract " + "coverage"  # built from parts so this scanner does not flag itself
    roots = sorted({path for path in EXPECTED_NEW_MODULES if (REPO_ROOT / path).is_file()})
    assert roots, "none of the five new modules exists — nothing to scan"
    negations = ("not claim", "does not", "do not", "never", "MUST NOT")
    offenders = []
    for relative in roots:
        for lineno, line in enumerate(
            (REPO_ROOT / relative).read_text(encoding="utf-8").splitlines(), start=1
        ):
            if phrase in line and not any(token in line for token in negations):
                offenders.append(f"{relative}:{lineno}: {line.strip()}")
    assert offenders == [], (
        "a module claims runtime coverage as contract-level:\n" + "\n".join(offenders)
    )
