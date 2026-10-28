"""Contract tests for driver-side Wrap-up accounting (2026-10-27).

Guards the mechanism added after a real SDD line (Feature 046) left analyze /
analyze2 with zero feedback and zero run-determination records: the dispatch said
"strictly read-only", the analyze surface said "no file writes", the executor
skipped its Wrap-up and deferred to the orchestrator, and U4 had no check that
could notice. The fix is four surfaces plus one owner rule:

  * ``references/stage-prompts.md`` — read-only dispatch variant + U4 accounting
  * ``SKILL.md``                     — U4 line / Hard Requirement 2 carry it
  * ``templates/commands/analyze.md``— no *artifact* writes, exception named
  * ``shared/workflow/feedback-step.md`` — feature attribution is mandatory
  * ``docs/reference/skills/sdd-loop-driver.md`` — reachability

The negative assertions matter as much as the positive ones: the old "no file
writes" phrasing and the old three-condition wording must not survive.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / "skills" / "external" / "sdd-loop-driver"
SKILL_MIRROR = ROOT / ".specify" / "skills" / "sdd-loop-driver"

PROMPTS = SKILL_DIR / "references" / "stage-prompts.md"
PROMPTS_MIRROR = SKILL_MIRROR / "references" / "stage-prompts.md"
SKILL = SKILL_DIR / "SKILL.md"
SKILL_MIRROR_FILE = SKILL_MIRROR / "SKILL.md"

ANALYZE_CMD = ROOT / "templates" / "commands" / "analyze.md"
FEEDBACK_STEP = ROOT / "shared" / "workflow" / "feedback-step.md"
FEEDBACK_STEP_MIRROR = ROOT / ".specify" / "shared" / "workflow" / "feedback-step.md"
DRIVER_DOC = ROOT / "docs" / "reference" / "skills" / "sdd-loop-driver.md"

FORBIDDEN = ["spec-kit", "specify-cli", "specify_cli", "cloud-native-ai",
             ".specify/specs/0", "Feature 0"]


def read(path: Path) -> str:
    assert path.is_file(), f"missing file: {path}"
    return path.read_text(encoding="utf-8")


def section(text: str, heading: str) -> str:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i
            break
    assert start is not None, f"section heading {heading!r} not found"
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## ") or lines[j].startswith("# "):
            end = j
            break
    return "\n".join(lines[start:end])


@pytest.mark.contract
def test_read_only_variant_carries_the_wrapup_exception():
    text = read(PROMPTS)
    body = section(text, "### 只读阶段变体（Read-only Stage Variant）")
    assert "no file writes" in body and "no artifact writes" in body, (
        "the variant must translate the command-surface phrasing"
    )
    assert "Wrap-up 记账必需" in body
    assert "WRAPUP-DEFERRED" in body
    assert "MUST 照常执行" in body


@pytest.mark.contract
def test_u4_has_wrapup_accounting_condition():
    text = read(PROMPTS)
    u4 = section(text, "## Independent Verification（独立校验程序，U4）")
    assert "四条件同时成立" in u4, "the U4 preamble must count four conditions"
    assert "三条件同时成立" not in text, "the old three-condition wording must not survive"
    assert "Wrap-up 记账核验" in u4
    assert "`simple-unit`" in u4 and "`duplicate`" in u4, (
        "engine-documented skips must count as satisfied"
    )
    assert "--feature" in u4, "feature attribution must be checked"
    assert "WRAPUP-DEFERRED" in u4, "the deferred path must hand accounting to the driver"
    assert "INCOMPLETE" in u4


@pytest.mark.contract
def test_skill_carries_the_accounting_requirement():
    text = read(SKILL)
    assert "Wrap-up 记账核验" in text
    assert "WRAPUP-DEFERRED" in text


@pytest.mark.contract
def test_analyze_surface_scopes_read_only_to_artifacts():
    text = read(ANALYZE_CMD)
    assert "no file writes" not in text, (
        "the unqualified 'no file writes' clause is the dispatch trap this fix removes"
    )
    assert "no artifact writes" in text
    assert "sanctioned bookkeeping exception" in text
    assert "read-only **on artifacts**" in text


@pytest.mark.contract
def test_feedback_step_requires_feature_attribution():
    text = read(FEEDBACK_STEP)
    assert "Feature attribution." in text
    assert "--feature <requirement-key>" in text
    assert "--feature-id" in text
    assert "valid only for feature-less units" in text


@pytest.mark.contract
def test_driver_reference_doc_reaches_the_rule():
    text = read(DRIVER_DOC)
    assert "Wrap-up 记账核验" in text
    assert "WRAPUP-DEFERRED" in text


@pytest.mark.contract
@pytest.mark.parametrize(
    "src,dst",
    [
        (PROMPTS, PROMPTS_MIRROR),
        (SKILL, SKILL_MIRROR_FILE),
        (FEEDBACK_STEP, FEEDBACK_STEP_MIRROR),
    ],
)
def test_runtime_mirrors_match_sources(src: Path, dst: Path):
    assert src.read_bytes() == dst.read_bytes(), (
        f"{src.relative_to(ROOT)} drifted from {dst.relative_to(ROOT)}; "
        "run scripts/python/sync-mirrors.py --write"
    )
