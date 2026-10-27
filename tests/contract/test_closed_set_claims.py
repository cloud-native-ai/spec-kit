"""Contract tests for the Closed-Set Claims discipline.

Guards the mechanism added after a real client project's spec (2026-10-27) declared
a two-item closed list of allowed generated-content changes while the feature's
shared shell snippets fanned out into every generated script template, and gated
its DoD on an undefined "unaffected leaf" predicate. Two analyze rounds were spent
repairing one root cause: the allowed-delta set was hand-enumerated at byte-site
granularity instead of derived from the edited sources' fan-out.

House pattern (owner doc -> ambient section -> contract test):
  * ``shared/guidelines/closed-set-claims.md`` — owner (+ runtime mirror)
  * ``templates/instructions-template.md`` — ambient section (+ mirror, + live)
  * ``skills/internal/analyze-artifacts/references/detection-and-severity.md`` — F-pass hook
  * ``shared/guidelines/requirements-guidelines.md`` — authoring hook

The ambient section is a pointer: the five requirements, the void conditions and the
dated anchor stay in the owner. ``DOC_ONLY_MARKERS`` is the negative half — without
it, the section could quietly grow into a second definition point.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

OWNER = ROOT / "shared" / "guidelines" / "closed-set-claims.md"
OWNER_MIRROR = ROOT / ".specify" / "shared" / "guidelines" / "closed-set-claims.md"
OWNER_LINK = ".specify/shared/guidelines/closed-set-claims.md"

TEMPLATE = ROOT / "templates" / "instructions-template.md"
TEMPLATE_MIRROR = ROOT / ".specify" / "templates" / "instructions-template.md"
LIVE = ROOT / ".specify" / "instructions.md"

ANALYZE = (
    ROOT / "skills" / "internal" / "analyze-artifacts" / "references"
    / "detection-and-severity.md"
)
ANALYZE_MIRROR = (
    ROOT / ".specify" / "skills" / "internal" / "analyze-artifacts" / "references"
    / "detection-and-severity.md"
)

REQUIREMENTS = ROOT / "shared" / "guidelines" / "requirements-guidelines.md"
REQUIREMENTS_MIRROR = ROOT / ".specify" / "shared" / "guidelines" / "requirements-guidelines.md"

HEADING = "## Closed-Set Claims (封闭清单声明)"
SECTION_SIZE_CAP = 1400

# Strings that live in the owner body only. Their presence in the ambient section
# would mean the section restates the discipline instead of pointing at it.
DOC_ONLY_MARKERS = [
    "两类断言必须分开",
    "允许差异集的来源",
    "补集断言与结构不变量",
    "拒绝形态（命中即 void）",
    "dated record，不作为现行事实引用",
]

# Shipped surfaces stay project-neutral (the dated anchor names no project).
FORBIDDEN = [
    "spec-kit", "specify-cli", "specify_cli", "cloud-native-ai",
    ".specify/specs/0", "Feature 0",
]


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
def test_owner_document_exists_and_declares_ownership():
    text = read(OWNER)
    assert "唯一真源" in text and "single source of truth" in text
    for label in ("基线参照物", "比较单元", "允许差异集的来源", "补集断言与结构不变量",
                  "未定义聚合词清零"):
        assert label in text, f"owner lost a required element: {label}"
    assert "void" in text and "拒绝形态" in text
    assert "dated record" in text, "dated evidence anchor lost its record marker"


@pytest.mark.contract
@pytest.mark.parametrize(
    "src,dst",
    [
        (OWNER, OWNER_MIRROR),
        (TEMPLATE, TEMPLATE_MIRROR),
        (ANALYZE, ANALYZE_MIRROR),
        (REQUIREMENTS, REQUIREMENTS_MIRROR),
    ],
)
def test_runtime_mirrors_match_sources(src: Path, dst: Path):
    assert src.read_bytes() == dst.read_bytes(), (
        f"{src.relative_to(ROOT)} drifted from {dst.relative_to(ROOT)}; "
        "run scripts/python/sync-mirrors.py --write"
    )


@pytest.mark.contract
def test_ambient_section_present_in_template_and_live_instructions():
    for path in (TEMPLATE, LIVE):
        text = read(path)
        assert text.count(HEADING) == 1, f"{path} must carry {HEADING!r} exactly once"


@pytest.mark.contract
def test_ambient_section_is_a_pointer_not_a_second_definition():
    body = section(read(TEMPLATE), HEADING)
    assert OWNER_LINK in body, "ambient section must cite the owner by runtime path"
    assert len(body) <= SECTION_SIZE_CAP, (
        f"ambient section grew to {len(body)} chars; the five requirements belong "
        "to the owner, not to the shipped instructions"
    )
    for marker in DOC_ONLY_MARKERS:
        assert marker not in body, (
            f"ambient section restates owner content ({marker!r}); convert it back "
            "into a reference"
        )


@pytest.mark.contract
def test_analyze_pass_and_severity_hook_the_owner():
    text = read(ANALYZE)
    assert OWNER_LINK in text, "the F pass must cite the owner"
    f_pass = section(text, "### F. Inconsistency")
    assert "containment claim" in f_pass.lower()
    assert "fan-out" in f_pass, "the detection hook must cover omitted fan-out"
    assert "Containment claims." in text, "severity routing for containment claims missing"
    assert "HIGH" in text.split("Containment claims.", 1)[1][:600]


@pytest.mark.contract
def test_requirements_guideline_hooks_the_owner():
    text = read(REQUIREMENTS)
    assert "closed-set-claims.md" in text, "authoring surface must cite the owner"
    assert "Stability / containment claims" in text
    assert "Stability and containment claims" in text


@pytest.mark.contract
def test_shipped_surfaces_stay_project_neutral():
    for path in (OWNER, TEMPLATE, ANALYZE, REQUIREMENTS):
        text = read(path)
        for token in FORBIDDEN:
            assert token not in text, f"{path} carries project-specific token {token!r}"
