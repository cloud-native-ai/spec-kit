"""Reusable fixtures for AI Tools Support feature (Feature 022).

Provides minimal workspace builders, resource path factories, and helper
functions shared across contract, integration, and unit tests.
"""

from pathlib import Path
from typing import List, Optional

import pytest

_OFFICIAL_ASSISTANTS = ["copilot", "claude", "qwen", "opencode", "qoder"]


def official_assistants() -> List[str]:
    """Return the list of officially supported assistant keys."""
    return list(_OFFICIAL_ASSISTANTS)


def assert_all_official_assistants_present(found: List[str], context: str = "") -> None:
    """Assert that all official assistants are present in a collection."""
    missing = set(_OFFICIAL_ASSISTANTS) - set(found)
    assert not missing, (
        f"Missing official assistants {sorted(missing)} in {context}: found {sorted(found)}"
    )


def make_resource_with_skills(
    root: Path, assistants: Optional[List[str]] = None
) -> Path:
    """Create a minimal resource root with templates, memory, scripts, and skills."""
    if assistants is None:
        assistants = _OFFICIAL_ASSISTANTS

    # templates/commands/*.md
    commands_dir = root / "templates" / "commands"
    commands_dir.mkdir(parents=True, exist_ok=True)
    for cmd in [
        "constitution",
        "feature",
        "requirements",
        "plan",
        "tasks",
        "implement",
    ]:
        (commands_dir / f"{cmd}.md").write_text(
            f'---\ndescription: "{cmd} command"\nsh: |\n  echo {cmd}\n---\n\n'
            f"# {cmd}\n\nScript: {{SCRIPT}}\n\nAgent: __AGENT__\n",
            encoding="utf-8",
        )

    # templates/instructions-template.md
    (root / "templates" / "instructions-template.md").parent.mkdir(
        parents=True, exist_ok=True
    )
    (root / "templates" / "instructions-template.md").write_text(
        "# Instructions\n\nSupported agents: copilot, claude, qwen, opencode, qoder\n",
        encoding="utf-8",
    )

    # templates/vscode-settings.json
    (root / "templates" / "vscode-settings.json").write_text("{}\n", encoding="utf-8")

    # templates/claudeignore-template
    (root / "templates" / "claudeignore-template").write_text(
        "node_modules/\n", encoding="utf-8"
    )

    # memory
    memory_dir = root / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    (memory_dir / "constitution.md").write_text(
        "# Constitution\n\nSupported: Claude Code, GitHub Copilot, Qwen Code, opencode, Qoder\n",
        encoding="utf-8",
    )
    (memory_dir / "features.md").write_text(
        "# Features\n\n| ID | Name | Status |\n", encoding="utf-8"
    )

    # scripts
    scripts_dir = root / "scripts" / "bash"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    (scripts_dir / "common.sh").write_text("#!/usr/bin/env bash\necho ok\n")

    # skills
    skills_dir = root / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    (skills_dir / "analysis-project").mkdir(parents=True, exist_ok=True)
    (skills_dir / "analysis-project" / "SKILL.md").write_text(
        "# Analysis Project Skill\n", encoding="utf-8"
    )

    return root


@pytest.fixture
def ai_tools_resource_root(tmp_path: Path) -> Path:
    """Create a reusable test resource root for AI tools support tests."""
    return make_resource_with_skills(tmp_path / "resource")
