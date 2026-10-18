"""Contract test: the Progress Reporting discipline (long-run visible rhythm).

The discipline lives in a dedicated single-source doc
(``shared/guidelines/progress-reporting.md``); the instructions template carries
only a summary + pointer, and the ``/speckit.instructions`` command reaches it by
reference without a second copy of the interval literal.

Three surfaces are pinned (the house pattern — owner doc → ambient section →
drift guard):

* the owner doc still defines the interval, its anchor, the override order, the
  content floor, the late-report rule, the confirmation-gate separation and the
  subagent dispatch clause;
* the ambient section states the same default interval (reachability surface)
  and keeps the summary shape;
* nobody else restates the number, and both template mirrors stay byte-identical.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "templates" / "instructions-template.md"
MIRROR = ROOT / ".specify" / "templates" / "instructions-template.md"
DOC = ROOT / "shared" / "guidelines" / "progress-reporting.md"
DOC_MIRROR = ROOT / ".specify" / "shared" / \
    "guidelines" / "progress-reporting.md"
COMMAND = ROOT / "templates" / "commands" / "instructions.md"
DOC_LINK = "shared/guidelines/progress-reporting.md"

HEADING = "## Progress Reporting Discipline"
# Project identifiers that MUST NOT leak into a project-neutral shared section.
FORBIDDEN = ["spec-kit", "specify-cli", "specify_cli", "cloud-native-ai"]

# One default-interval owner, one reachability reminder — never a third surface.
TEMPLATE_INTERVAL_RE = re.compile(r"\*\*(\d+)\s+minutes?\s+by\s+default", re.I)
DOC_INTERVAL_RE = re.compile(r"默认间隔\s*(\d+)\s*分钟")


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def section(text: str) -> str:
    """Return the `## Progress Reporting Discipline` section (up to the next `## `)."""
    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines)
                 if ln.strip() == HEADING), None)
    assert start is not None, f"section heading {HEADING!r} not found"
    end = next(
        (j for j in range(start + 1, len(lines))
         if lines[j].startswith(("## ", "# "))),
        len(lines),
    )
    return "\n".join(lines[start:end])


# --- ambient section + pointer, in both template copies ---


def test_heading_and_pointer_present_in_both_template_copies():
    for rel, p in (("templates", SRC), (".specify/templates", MIRROR)):
        body = section(read(p))
        assert DOC_LINK in body, f"pointer link {DOC_LINK!r} missing in {rel}"


def test_template_mirrors_are_byte_identical():
    assert SRC.read_bytes() == MIRROR.read_bytes(
    ), "instructions-template mirrors diverged"


def test_ambient_section_carries_the_five_keywords():
    body = section(read(SRC)).lower()
    for keyword in ("rhythm", "content floor", "measured, not invented",
                    "boundary-respecting", "exemptions and precedence"):
        assert keyword in body, f"summary is missing its {keyword!r} bullet"


# --- owner doc: full discipline, and its mirror ---


def test_doc_exists_with_byte_identical_mirror():
    assert DOC.is_file(), f"missing owner doc: {DOC}"
    assert DOC_MIRROR.is_file(), f"missing owner doc mirror: {DOC_MIRROR}"
    assert DOC.read_bytes() == DOC_MIRROR.read_bytes(), "owner doc mirror drift"


def test_doc_defines_the_load_bearing_clauses():
    text = read(DOC)
    clauses = {
        "long-run applicability": "长时任务",
        "short-run exemption": "短任务",
        "anchor (task start, not last report)": "锚点是任务开始时刻",
        "override order": "覆盖方式",
        "content floor": "四要素",
        "measured figures": "数字须可溯源",
        "late report at the step boundary": "补报",
        "report is not a confirmation gate": "汇报不是确认门",
        "subagents are injected at dispatch": "派发载荷",
        "boundaries with sibling disciplines": "判定边界",
    }
    for label, needle in clauses.items():
        assert needle in text, f"owner doc no longer defines: {label} ({needle!r})"


def test_doc_ships_no_machinery():
    """The discipline binds behaviour, not infrastructure (no timer, no store)."""
    text = read(DOC)
    assert "不引入机制" in text, "the no-machinery boundary clause is missing"


# --- one owner for the interval literal ---


def test_default_interval_agrees_between_owner_and_reachability_surface():
    doc_match = DOC_INTERVAL_RE.search(read(DOC))
    tmpl_match = TEMPLATE_INTERVAL_RE.search(section(read(SRC)))
    assert doc_match, "owner doc no longer states the default interval"
    assert tmpl_match, "ambient section no longer states the default interval"
    assert doc_match.group(1) == tmpl_match.group(1), (
        "the ambient summary and the owner doc disagree on the default interval: "
        f"{tmpl_match.group(1)} vs {doc_match.group(1)}"
    )


def test_command_template_points_at_the_owner_without_restating_the_interval():
    text = read(COMMAND)
    assert DOC_LINK in text, "the command template no longer points at the owner doc"
    interval = TEMPLATE_INTERVAL_RE.search(section(read(SRC))).group(1)
    for restatement in (f"{interval} minutes", f"{interval} 分钟", f"{interval}min"):
        assert restatement not in text, (
            f"the command template restates the default interval as {restatement!r}; "
            "the owner doc is its only definition point"
        )


# --- project-neutral: no repo-specific identifiers ---


def test_section_and_doc_are_project_neutral():
    for name, text in (("template section", section(read(SRC))), ("owner doc", read(DOC))):
        low = text.lower()
        for token in FORBIDDEN:
            assert token.lower(
            ) not in low, f"project-specific token {token!r} leaked into {name}"
