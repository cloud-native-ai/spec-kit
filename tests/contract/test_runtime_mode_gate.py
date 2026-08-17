"""Contract test: runtime-mode gate (Spec Kit project vs standalone).

Spec Kit skills are also deployed to standalone agent applications
(QoderWork, Wukong, OpenClaw, ...) whose working directory has no
``.specify/`` directory. Enforces ``shared/workflow/runtime-mode.md``:

* the canonical convention doc exists in ``shared/`` and its ``.specify`` mirror;
* every ``skills/*/SKILL.md`` ``## Feedback`` section begins with the
  runtime-mode gate (source tree and runtime mirror);
* ``templates/skills-template.md`` and ``shared/workflow/feedback-step.md``
  carry the gate;
* ``create-skills`` documents mode detection and the standalone skips
  (role-agent propagation / engine-backed feedback).
"""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
GATE_MARKER = "**Runtime-mode gate.**"
GATE_CHECK = "`${SKILL_WORKDIR}/.specify/` does not exist"


def _skill_files(base: Path):
    return sorted(base.glob("*/SKILL.md"))


def _missing_gate(base: Path):
    return [
        f.parent.name
        for f in _skill_files(base)
        if GATE_MARKER not in f.read_text(encoding="utf-8")
    ]


@pytest.mark.contract
def test_runtime_mode_doc_exists_in_source_and_mirror():
    source = REPO_ROOT / "shared" / "workflow" / "runtime-mode.md"
    mirror = REPO_ROOT / ".specify" / "shared" / "workflow" / "runtime-mode.md"
    assert source.exists(), "shared/workflow/runtime-mode.md is missing"
    text = source.read_text(encoding="utf-8")
    assert "standalone" in text and ".specify" in text
    if mirror.exists():
        assert text == mirror.read_text(encoding="utf-8"), (
            "runtime-mode.md mirror differs from source"
        )


@pytest.mark.contract
def test_every_source_skill_feedback_carries_mode_gate():
    missing = _missing_gate(REPO_ROOT / "skills")
    assert not missing, f"skills/ SKILL.md missing runtime-mode gate: {missing}"


@pytest.mark.contract
def test_every_runtime_mirror_skill_feedback_carries_mode_gate():
    skills_dir = REPO_ROOT / ".specify" / "skills"
    if not skills_dir.exists():
        pytest.skip(".specify/skills mirror not present")
    missing = _missing_gate(skills_dir)
    assert not missing, f".specify/skills/ SKILL.md missing runtime-mode gate: {missing}"


@pytest.mark.contract
def test_skills_template_carries_mode_gate():
    text = (REPO_ROOT / "templates" / "skills-template.md").read_text(encoding="utf-8")
    assert GATE_MARKER in text and GATE_CHECK in text


@pytest.mark.contract
def test_feedback_step_canonical_block_carries_mode_gate():
    for base in ("shared", ".specify/shared"):
        path = REPO_ROOT / base / "workflow" / "feedback-step.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        assert GATE_MARKER in text, f"{path} canonical block missing runtime-mode gate"


@pytest.mark.contract
def test_create_skills_documents_standalone_mode():
    text = (REPO_ROOT / "skills" / "create-skills" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "Detect the runtime mode" in text, (
        "create-skills lacks the runtime-mode detection step"
    )
    assert "standalone mode" in text
    # Spec-Kit-specific steps must be declared conditional. Registration is
    # gone in every mode (2026-08-17 registry retirement); the still-gated
    # steps are engine-backed Feedback and role-agent propagation.
    assert "self-contained" in text and "`## Feedback`" in text, (
        "create-skills engine-backed Feedback step is not gated to Spec Kit project mode"
    )
    assert "in Spec Kit project mode" in text and "skip this step" in text, (
        "create-skills agent propagation step is not gated to Spec Kit project mode"
    )
