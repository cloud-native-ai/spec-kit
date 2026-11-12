"""G-1 (T062) — the Anchor command surface: seven modes, scope set cited by path.

Subject: `templates/commands/anchor.md` (the packaged source; the four per-tool copies are
generated from it by `scripts/python/regen-command-copies.py` and are asserted for the
positioning they inherit). The guard turns red when the template is missing, when its
`argument-hint` does not declare exactly the seven modes, when it offers a Goal-only mode, or
when it restates the closed `--scope` member set instead of reaching the owner by path.

Red-first readings: `notes/red-first-evidence.md` § WP-05 — the three injection tests below
run the same predicates against a deliberately broken template and report red; the driver
record in the notes is the same predicate through this module with `SPECKIT_GUARD_ROOT`
pointing at a mutated copy.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = Path(os.environ.get("SPECKIT_GUARD_ROOT") or REPO_ROOT)
TEMPLATE = ROOT / "templates/commands/anchor.md"

MODE_SET = ("create", "view", "modify", "targets", "migrate", "migrate-archive", "coordinate")
GOAL_ONLY_MODES = ("status", "goal-create")
SCOPE_OWNER = "anchor-definitions.md"
ARCHIVE_PATH = ".specify/anchoring/<anchor-slug>/anchor.md"
COPIES = (
    ".claude/commands/speckit.anchor.md",
    ".github/prompts/speckit.anchor.prompt.md",
    ".qoder/commands/speckit.anchor.md",
    ".opencode/command/speckit.anchor.md",
)

SCOPE_RESTATEMENT_PATTERNS = (
    # a literal `--scope` example naming a member, followed by more members
    r"`?--scope`?[^\n]{0,20}\b(anchor|teams|goals|auto)\b[^\n]{0,20}\b(teams|goals|auto)\b",
    # the four members rendered as a pipe-separated set
    r"\banchor\s*\|\s*teams\s*\|\s*goals\s*\|\s*auto\b",
    # the same set in the project's Chinese phrasing
    r"锚点\s*/\s*团队\s*/\s*行动级\s*(Goal)?\s*/\s*auto",
)


def _read(path: Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def hint_modes(text: str) -> list[str]:
    """The mode list the command's `argument-hint` declares (first bracket group)."""
    match = re.search(r"(?m)^argument-hint:\s*(.*)$", text)
    if not match:
        return []
    group = re.search(r"\[([^\[\]]+)\]", match.group(1))
    if not group:
        return []
    return [part.strip() for part in group.group(1).split("|") if part.strip()]


def scope_restatements(text: str) -> list[str]:
    """Patterns that enumerate the closed scope member set instead of citing its owner."""
    body = "\n".join(line for line in text.splitlines() if not line.startswith("argument-hint:"))
    return [pattern for pattern in SCOPE_RESTATEMENT_PATTERNS if re.search(pattern, body)]


def surface_problems(template: Path) -> list[str]:
    """Every way the Anchor command surface is off-contract, as human-readable strings."""
    template = Path(template)
    if not template.is_file():
        return [f"template missing: {template}"]
    text = _read(template)
    problems: list[str] = []
    modes = hint_modes(text)
    if len(modes) != len(MODE_SET) or sorted(modes) != sorted(MODE_SET):
        problems.append(f"modes {modes} != {list(MODE_SET)}")
    if set(modes) & set(GOAL_ONLY_MODES):
        problems.append(f"goal-only modes offered: {sorted(set(modes) & set(GOAL_ONLY_MODES))}")
    if "sole authoring entry" not in text:
        problems.append("positioning does not name the sole authoring entry")
    if ARCHIVE_PATH not in text:
        problems.append(f"positioning does not name {ARCHIVE_PATH}")
    if SCOPE_OWNER not in text:
        problems.append(f"scope owner {SCOPE_OWNER} is not cited")
    restated = scope_restatements(text)
    if restated:
        problems.append(f"scope member set restated: {restated}")
    return problems


def test_template_exists() -> None:
    assert TEMPLATE.is_file(), f"missing packaged command template: {TEMPLATE}"


def test_hint_declares_exactly_the_seven_modes() -> None:
    modes = hint_modes(_read(TEMPLATE))
    assert len(modes) == 7, f"expected 7 modes, read {len(modes)}: {modes}"
    assert sorted(modes) == sorted(MODE_SET)


def test_no_goal_only_mode_is_offered() -> None:
    modes = set(hint_modes(_read(TEMPLATE)))
    assert not modes & set(GOAL_ONLY_MODES), (
        f"the Anchor entry offers Goal-only modes {sorted(modes & set(GOAL_ONLY_MODES))}")


def test_positioning_names_the_archive_and_the_sole_authoring_entry() -> None:
    text = _read(TEMPLATE)
    assert "sole authoring entry" in text
    assert ARCHIVE_PATH in text
    # the migration is the same entry's job, so the mode and its purpose are both declared
    assert "migrate-archive" in text


def test_scope_set_is_cited_by_path_not_restated() -> None:
    text = _read(TEMPLATE)
    assert SCOPE_OWNER in text, "the closed scope set's owner is not cited"
    assert "§ Archive Layers" in text, "the owner's archive-layers section is not cited"
    assert not scope_restatements(text), (
        f"the scope member set is restated: {scope_restatements(text)}")


def test_generated_copies_carry_the_inherited_positioning() -> None:
    missing = [copy for copy in COPIES if not (ROOT / copy).is_file()]
    assert not missing, f"generated per-tool copies missing: {missing}"
    for copy in COPIES:
        text = _read(ROOT / copy)
        assert "AUTO-GENERATED from templates/commands/anchor.md" in text, copy
        assert "sole authoring entry" in text, f"{copy} lost the positioning"
        assert ARCHIVE_PATH in text, f"{copy} lost the archive path"


def test_injection_missing_template_is_red(tmp_path: Path) -> None:
    problems = surface_problems(tmp_path / "anchor.md")
    assert problems and problems[0].startswith("template missing:")


def test_injection_wrong_mode_count_is_red() -> None:
    text = _read(TEMPLATE).replace("|coordinate", "")
    modes = hint_modes(text)
    assert len(modes) != 7, "the injected template still declares seven modes"
    assert surface_problems_text(text), "the guard did not notice the dropped mode"


def test_injection_restated_scope_is_red() -> None:
    text = _read(TEMPLATE) + (
        "\nThe closed scope set is `--scope anchor|teams|goals|auto`.\n")
    assert scope_restatements(text), "the guard did not notice the restated member set"


def surface_problems_text(text: str) -> list[str]:
    """`surface_problems` for an in-memory template (injection cases only)."""
    problems: list[str] = []
    modes = hint_modes(text)
    if len(modes) != len(MODE_SET) or sorted(modes) != sorted(MODE_SET):
        problems.append(f"modes {modes} != {list(MODE_SET)}")
    if scope_restatements(text):
        problems.append("scope member set restated")
    return problems
