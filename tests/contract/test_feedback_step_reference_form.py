"""Contract test: the embedded `## Feedback` step is a reference, not a copy.

Owner: ``shared/workflow/feedback-step.md`` § *Embedded reference forms*.

Before this guard existed the owner told embedders to "copy the canonical block below
verbatim (adjusting only the ``<unit-id>`` / ``<unit-type>`` placeholders)" — an
instruction that cannot be followed literally, because the block carries a skills-only
runtime-mode gate and a placeholder unit id. 59 surfaces ended up with 9 distinct
wordings and ~144 KB of duplicated rule text, and a rule change had to be hand-applied
to every one of them. The embedded section is now a short pointer plus the unit id.

The surface set is derived from the filesystem, never enumerated here, so a new skill or
command template is covered the moment it grows a ``## Feedback`` section. The simple
command list is imported from the classification test rather than restated.
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
OWNER = REPO_ROOT / "shared" / "workflow" / "feedback-step.md"
OWNER_MIRROR = REPO_ROOT / ".specify" / "shared" / "workflow" / "feedback-step.md"
OWNER_CITE = "feedback-step.md"
FORMS_HEADING = "## Embedded reference forms"

# A reference section stays a pointer. 1500 B matches the bound the sibling
# `## Documentation` step is held to (test_docs_step_injection.py); the converted
# surfaces measure ~700 B (command) and ~915 B (skill).
MAX_SECTION_BYTES = 1500

# Anti-vacuity sentinel: the glob-derived surface set must be substantial, so a pattern
# that silently matched nothing cannot pass as "every surface conforms".
MIN_SURFACES = 40

GATE_MARKER = "**Runtime-mode gate.**"

# Characteristic literals of the owner's own rule text. Their presence in an embedded
# section is the copy this guard exists to prevent.
OWNER_ONLY_LITERALS = (
    "No significant optimization points identified this run.",
    "原文转储",
    "Threshold prompt protocol",
    "Abort / partial-run rule",
    "Nesting rule",
    "Gate on qualification & completion",
)


def _load_simple_commands() -> tuple[str, ...]:
    path = REPO_ROOT / "tests" / "contract" / "test_feedback_command_classification.py"
    spec = importlib.util.spec_from_file_location("_fb_class", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return tuple(module.SIMPLE_COMMANDS)


SIMPLE_COMMANDS = _load_simple_commands()


def _surfaces() -> list[tuple[Path, str, str]]:
    """(path, kind, unit-id) for every surface carrying a `## Feedback` section."""
    out: list[tuple[Path, str, str]] = []
    for path in sorted((REPO_ROOT / "templates" / "commands").glob("*.md")):
        out.append((path, "command", f"/speckit.{path.stem}"))
    for path in sorted((REPO_ROOT / "skills").glob("*/SKILL.md")):
        out.append((path, "skill", f"skill:{path.parent.name}"))
    template = REPO_ROOT / "templates" / "skills-template.md"
    out.append((template, "skill", "skill:{{SKILL_NAME}}"))
    return [
        (p, kind, unit)
        for p, kind, unit in out
        if re.search(r"(?m)^## Feedback[ \t]*$", p.read_text(encoding="utf-8"))
    ]


SURFACES = _surfaces()


def _sid(v):
    return str(v.relative_to(REPO_ROOT)) if isinstance(v, Path) else str(v)


def _slice_section(text: str, heading: str, where: str) -> str:
    """Slice `heading`'s body, stopping at the next top-level heading that is OUTSIDE a
    fenced code block. A plain `^## ` search silently truncates at a heading that appears
    inside a ```markdown example — which is exactly what the owner's reference forms
    contain, so the naive slice looked fine and returned half a section."""
    lines = text.splitlines(keepends=True)
    start = None
    in_fence = False
    for idx, line in enumerate(lines):
        bare = line.rstrip("\n")
        if start is None:
            if bare.rstrip() == heading:
                start = idx
            continue
        if bare.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and bare.startswith("## "):
            return "".join(lines[start:idx])
    assert start is not None, f"{where}: missing heading {heading!r}"
    return "".join(lines[start:])


def _section(path: Path) -> str:
    return _slice_section(
        path.read_text(encoding="utf-8"), "## Feedback",
        str(path.relative_to(REPO_ROOT)),
    )


def test_surface_set_is_substantial():
    assert len(SURFACES) >= MIN_SURFACES, (
        f"only {len(SURFACES)} surfaces carry a '## Feedback' section — the glob-derived "
        f"set looks empty or truncated, which would make every per-surface assertion below "
        f"pass vacuously"
    )


@pytest.mark.parametrize("name", SIMPLE_COMMANDS)
def test_simple_command_carries_no_section(name: str):
    path = REPO_ROOT / "templates" / "commands" / f"{name}.md"
    text = path.read_text(encoding="utf-8")
    assert "## Feedback" not in text, f"{name}.md is a simple command and must not embed the step"
    assert "feedback-utils.py" not in text, f"{name}.md must not name the feedback engine"


@pytest.mark.parametrize("path,kind,unit", SURFACES, ids=_sid)
def test_embedded_section_is_a_reference(path: Path, kind: str, unit: str):
    rel = path.relative_to(REPO_ROOT)
    body = _section(path)

    assert OWNER_CITE in body, f"{rel}: the section must cite its owner"
    assert len(body.encode()) < MAX_SECTION_BYTES, (
        f"{rel}: '## Feedback' is {len(body.encode())} B — a reference section stays under "
        f"{MAX_SECTION_BYTES} B; this one has grown back into a copy of the owner's rules"
    )
    assert f'--unit-id "{unit}"' in body, (
        f"{rel}: the unit id is the one per-surface fact; expected {unit!r}"
    )
    assert f"--unit-type {kind}" in body, f"{rel}: unit type must match the surface class"
    assert "feedback-utils.py" in body, f"{rel}: the engine name must survive (embed marker)"

    restated = [lit for lit in OWNER_ONLY_LITERALS if lit in body]
    assert not restated, (
        f"{rel}: the section restates the owner's rules {restated[:3]} — repair by deleting "
        f"the copy and leaving the pointer, not by re-wording it to agree"
    )
    assert not re.search(r"(?m)^## (?!Feedback)", body), (
        f"{rel}: the section must not introduce another top-level heading (it would break "
        f"the Feedback → Documentation → Handoffs adjacency)"
    )


@pytest.mark.parametrize("path,kind,unit", SURFACES, ids=_sid)
def test_runtime_mode_gate_tracks_the_surface_class(path: Path, kind: str, unit: str):
    """The gate is part of the skill form only: skills also ship standalone, commands
    only ever run inside a Spec Kit project. Asserting both directions keeps the two
    forms distinguishable instead of collapsing into one."""
    body = _section(path)
    if kind == "skill":
        assert GATE_MARKER in body, f"{path.relative_to(REPO_ROOT)}: skill form lost its gate"
        assert "`${SKILL_WORKDIR}/.specify/` does not exist" in body, (
            f"{path.relative_to(REPO_ROOT)}: the gate's detection condition is missing"
        )
    else:
        assert GATE_MARKER not in body, (
            f"{path.relative_to(REPO_ROOT)}: the command form must not carry the skill-only gate"
        )


def test_owner_carries_both_reference_forms():
    text = OWNER.read_text(encoding="utf-8")
    assert FORMS_HEADING in text, "the owner no longer names its embedded reference forms"
    forms = _slice_section(text, FORMS_HEADING, "feedback-step.md")
    assert '--unit-type command' in forms, "command form missing from the owner"
    assert '--unit-type skill' in forms, "skill form missing from the owner"
    assert GATE_MARKER in forms, "the skill form in the owner lost its runtime-mode gate"
    assert forms.count("```markdown") == 2, (
        f"expected exactly two copy-ready forms, found {forms.count('```markdown')}"
    )


def test_owner_declares_reference_not_copy():
    text = OWNER.read_text(encoding="utf-8")
    assert "they do not copy it" in text, (
        "the owner must state the embedding rule; without it the forms are advisory and "
        "the 59 surfaces drift apart again"
    )
    assert "copy the canonical block below verbatim" not in text, (
        "the impossible verbatim-copy instruction is back — it is what produced the drift"
    )


def test_owner_keeps_the_procedure_substance():
    """The rules moved into the owner; they must still be there. Without this the
    conversion could pass by deleting the section bodies *and* the rules."""
    text = OWNER.read_text(encoding="utf-8")
    for literal in OWNER_ONLY_LITERALS + (
        "代做确定性工作",
        "重复读取",
        "token-efficiency.md",
        "不编造",
        "optional observation sensor",
        "self-improvement-definitions.md",
    ):
        assert literal in text, f"owner lost substance: {literal!r}"


def test_owner_mirror_is_byte_identical():
    assert OWNER_MIRROR.is_file(), "missing .specify mirror of feedback-step.md"
    assert OWNER.read_bytes() == OWNER_MIRROR.read_bytes(), (
        "feedback-step.md mirror drift — run sync-mirrors.py --write shared"
    )
