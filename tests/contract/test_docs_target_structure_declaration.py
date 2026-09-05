"""Contract tests for the project-specific docs target declaration (requirement 048)."""
from __future__ import annotations

from pathlib import Path
import re

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
COMMAND = REPO_ROOT / "templates" / "commands" / "docs.md"
TARGET_TEMPLATE = REPO_ROOT / "templates" / "docs-target-structure-template.md"
BASELINE_OWNER = REPO_ROOT / "skills" / "create-docs" / "SKILL.md"
DOCS_ENGINE = REPO_ROOT / "scripts" / "python" / "docs-utils.py"

START = "<!-- DOCS_TARGET_STRUCTURE_START -->"
END = "<!-- DOCS_TARGET_STRUCTURE_END -->"
REQUIRED_FIELDS = [
    "项目形态",
    "目标读者",
    "静态基线引用",
    "项目专属扩展",
    "内容盘点摘要",
    "固定检索入口",
    "最后确认",
]


def _command() -> str:
    return COMMAND.read_text(encoding="utf-8")


def _target_template() -> str:
    assert TARGET_TEMPLATE.is_file(), "target declaration template missing"
    return TARGET_TEMPLATE.read_text(encoding="utf-8")


def _owned_baseline_tokens() -> set[str]:
    text = BASELINE_OWNER.read_text(encoding="utf-8")
    section = text.split("### Desired-State Baseline", 1)[1].split("## Workflow", 1)[0]
    return {
        token
        for token in re.findall(r"`([^`]+)`", section)
        if (token.endswith(".md") and "/" not in token)
        or (token.endswith("/") and token not in {"/", "docs/"})
    }


@pytest.mark.contract
def test_target_declaration_has_stable_root_path_and_managed_block() -> None:
    command = _command()
    template = _target_template()
    assert ".specify/docs/target-structure.md" in command
    assert ".specify/docs/plans/target-structure.md" not in command
    assert ".specify/docs/audit/target-structure.md" not in command
    assert template.count(START) == 1
    assert template.count(END) == 1
    assert template.index(START) < template.index(END)


@pytest.mark.contract
def test_target_template_has_required_fields_without_copying_owner_facts() -> None:
    template = _target_template()
    for field in REQUIRED_FIELDS:
        assert field in template, f"target declaration field missing: {field}"
    assert ".specify/skills/create-docs/SKILL.md" in template
    assert ".specify/instructions.md" in template
    assert "Documentation Map" in template
    assert "/speckit.instructions" in template
    copied = sorted(token for token in _owned_baseline_tokens() if token in template)
    assert not copied, f"target declaration copied baseline-owner facts: {copied}"


@pytest.mark.contract
def test_command_preserves_bytes_outside_managed_block_and_stops_on_invalid_markers() -> None:
    command = _command()
    assert START in command and END in command
    assert "outside-block bytes" in command
    assert "missing, unpaired, or unparseable" in command
    assert "stop" in command.lower()
    assert "never overwrite the whole file" in command.lower()


@pytest.mark.contract
def test_underdetermined_design_asks_at_most_three_questions_before_writing() -> None:
    command = _command()
    assert "1–3 necessary questions" in command
    assert "before answers arrive" in command
    assert "no declaration or convergence write" in command.lower()


@pytest.mark.contract
def test_substantive_drift_only_proposes_confirmed_redesign() -> None:
    command = _command()
    assert "substantive drift" in command.lower()
    assert "redesign proposal" in command.lower()
    assert "before confirmation" in command.lower()
    assert "R4" in command


@pytest.mark.contract
def test_declaration_does_not_expand_docs_engine_actions() -> None:
    engine = DOCS_ENGINE.read_text(encoding="utf-8")
    assert ".specify/docs/target-structure.md" not in engine
    assert "DOCS_TARGET_STRUCTURE_START" not in engine
