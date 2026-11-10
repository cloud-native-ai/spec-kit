"""Concurrency coverage — every execution body carries the obligation pointer.

Owner of the obligation text: `shared/definitions/subagent-definitions.md` § The Concurrency Obligation.
This guard asserts the POINTER only (marker + owner path), never the rule text: a command template or a
skill that loses the pointer is an execution body that will never ask the concurrency question.
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
COMMANDS = REPO_ROOT / "templates" / "commands"
SKILLS = REPO_ROOT / "skills"
MARKER = "Concurrency obligation（执行义务，按指针抵达）"
OWNER_PATH = "shared/definitions/subagent-definitions.md"


def _surfaces() -> tuple[list[Path], list[Path]]:
    commands = sorted(COMMANDS.glob("*.md"))
    skills = sorted(SKILLS.glob("*/SKILL.md")) + sorted(SKILLS.glob("*/*/SKILL.md"))
    return commands, skills


def _label(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _offenders(paths: list[Path]) -> list[str]:
    return [
        _label(path)
        for path in paths
        if MARKER not in path.read_text(encoding="utf-8")
    ]


def test_every_command_and_skill_carries_the_pointer():
    commands, skills = _surfaces()
    assert len(commands) >= 29, "the command roster shrank unexpectedly: %d" % len(commands)
    assert len(skills) >= 50, "the skill roster shrank unexpectedly: %d" % len(skills)
    missing = _offenders(commands + skills)
    assert not missing, (
        "execution bodies without the concurrency pointer (they would never ask the "
        "concurrency question): %r" % (missing,)
    )


def test_the_pointer_cites_the_owner_document():
    commands, skills = _surfaces()
    bad = [
        str(path.relative_to(REPO_ROOT))
        for path in commands + skills
        if MARKER in path.read_text(encoding="utf-8")
        and OWNER_PATH not in path.read_text(encoding="utf-8")
    ]
    assert not bad, "the pointer must reach the obligation owner by path: %r" % (bad,)


def test_the_audit_turns_red_when_one_surface_loses_the_pointer(tmp_path):
    """Red-first drill: the checker reports a surface whose pointer was removed."""
    commands, _skills = _surfaces()
    source = commands[0].read_text(encoding="utf-8")
    synthetic = tmp_path / "synthetic-command.md"
    synthetic.write_text(source.replace(MARKER, "REMOVED"), encoding="utf-8")
    offenders = _offenders([synthetic])
    assert offenders, "a surface without the pointer must be reported"
