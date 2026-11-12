"""Contract tests for the retired goal/team classification vocabulary (FR-022, SC-008).

Tasks rows T064, T069, T070 (US5). The scan is a **criterion** scan, not a word ban:
``temporary`` remains a legitimate member-lifecycle value and ``global`` a legitimate
non-goal word, so only *classification uses* are hits —

* a ``temporary``/``临时`` word adjacent to a ``goal``/``team`` noun (the retired
  "Temporary Goal / Temporary Team" class names),
* a ``global`` word adjacent to a ``goal``/``team`` noun (the retired "Global Goal" /
  "Global Team" class names),
* the retired scope values in a scope position (``--scope global|spec``,
  ``scope: global|spec``, ``scope = spec``).

Exemptions, exactly as the row states: the concept owner's historical record
(``shared/definitions/goal-definitions.md`` § Terminology Boundaries, which maps the
retired names forward) and the temp-directory exemption (`.specify/.tmp/` and the
temp-directory owner are a different axis and never a goal/team criterion).

Measured baseline 2026-11-09, before the US5 rewrites: 29 hits across
``shared/definitions/sdd-routing-definitions.md``, ``skills/internal/create-team/references/
{create-mode,conceptual-model}.md``, ``skills/external/sdd-loop-driver/references/
{checkpoint-protocol,decomposition-model}.md`` and ``skills/external/sdd-loop-driver/
SKILL.md``, ``templates/commands/{goal,team}.md`` and ``scripts/python/sdd-route.py`` —
so this module is authored red-first and turns green when those row-owned surfaces are
rewritten.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ROUTING = REPO_ROOT / "shared/definitions/sdd-routing-definitions.md"

SCAN_DIRS = ("shared", "skills", "scripts", "templates", "src")
SCAN_SUFFIXES = {".md", ".py", ".sh", ".bash", ".yaml", ".yml"}

#: The files allowed to name the retired terms: the concept owner's historical record,
#: which feature 101 split — the Anchor owner carries the retired-name map-forward and the
#: action-level Goal owner keeps its own boundary record.
HISTORICAL_RECORD = ("shared/definitions/goal-definitions.md",
                     "shared/definitions/anchor-definitions.md")

TEMP_DIR_TOKENS = (".specify/.tmp", "temp-directory", "运行临时区")

CRITERION_PATTERNS = (
    ("temporary-goal-team",
     re.compile(r"(?i)\b(?:temporary|临时)\s*[\(\-]?\s*(?:run-scoped\s*[\)\-]?\s*)?"
                r"(?:goals?|teams?)\b")),
    ("goal-team-temporary",
     re.compile(r"(?i)\b(?:goals?|teams?)\s*[\(\-]?\s*(?:run-scoped\s*[\)\-]?\s*)?"
                r"(?:temporary|临时)\b")),
    ("global-goal-team",
     re.compile(r"(?i)\bglobal\s*[\(\-]?\s*(?:goals?|teams?)\b")),
    ("retired-scope-value",
     re.compile(r"(?i)(?:--scope\s+|scope\s*[:=]\s*)(?:global|spec)\b")),
)


def _criterion_hits():
    hits = []
    for directory in SCAN_DIRS:
        for path in (REPO_ROOT / directory).rglob("*"):
            if not path.is_file() or path.suffix not in SCAN_SUFFIXES:
                continue
            rel = path.relative_to(REPO_ROOT).as_posix()
            if rel in HISTORICAL_RECORD:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for lineno, line in enumerate(text.splitlines(), 1):
                if any(token in line for token in TEMP_DIR_TOKENS):
                    continue
                for name, pattern in CRITERION_PATTERNS:
                    if pattern.search(line):
                        hits.append(f"{rel}:{lineno} [{name}] {line.strip()[:140]}")
    return hits


def _section(path: Path, heading: str) -> str:
    text = path.read_text(encoding="utf-8")
    start = text.find(heading)
    assert start != -1, f"{path} has no {heading!r} section"
    tail = text[start + len(heading):]
    end = re.search(r"(?m)^## ", tail)
    return tail[: end.start()] if end else tail


# ---------------------------------------------------------------------------
# T064 / FR-022 / SC-008 — zero classification hits on the runtime surfaces
# ---------------------------------------------------------------------------
def test_no_runtime_surface_uses_temporary_or_global_as_a_criterion():
    hits = _criterion_hits()
    assert not hits, (
        "the retired classification vocabulary survives on a runtime surface "
        "(FR-022 allows it only in the owner's historical record and the temp-directory "
        f"exemption); hits: {len(hits)}\n" + "\n".join(hits))


# ---------------------------------------------------------------------------
# T069 / C-91 — the rewritten carve-out keeps the hierarchy prohibition verbatim
# ---------------------------------------------------------------------------
HIERARCHY_PROHIBITION = "一次 SDD 运行 MUST NOT 创建/重绑/改范围/终止共享档案中的既有定义"


def test_the_routing_carve_out_keeps_the_hierarchy_prohibition_verbatim():
    section = _section(ROUTING, "## Hierarchy")
    assert HIERARCHY_PROHIBITION in section, (
        "C-91 keeps this prohibition verbatim when the Temporary carve-out is "
        f"replaced: {HIERARCHY_PROHIBITION!r}")
    offenders = [
        f"{name}: {line.strip()[:120]}"
        for line in section.splitlines()
        for name, pattern in CRITERION_PATTERNS
        if pattern.search(line) and not any(t in line for t in TEMP_DIR_TOKENS)
    ]
    assert not offenders, (
        "the carve-out must contain no Temporary / 临时 (or Global goal/team) "
        f"criterion name: {offenders}")


# ---------------------------------------------------------------------------
# T070 / C-92 — the carve-out cites both owners and restates no domain
# ---------------------------------------------------------------------------
def test_the_carve_out_cites_owners_and_restates_no_domain():
    section = _section(ROUTING, "## Hierarchy")
    assert "shared/definitions/goal-definitions.md" in section, (
        "the goal-side concept owner is cited by path (C-92)")
    assert "skills/internal/create-team/references/conceptual-model.md" in section, (
        "the team-side concept owner is cited by path (C-92)")

    restated = [
        line.strip()[:140]
        for line in section.splitlines()
        if all(value in line for value in ('"sdd-run"', '"command-run"', '"human"'))
        or all(value in line for value in ("`sdd-run`", "`command-run`", "`human`"))
    ]
    assert not restated, (
        "the carve-out must not restate the owner value domain (C-92); a line "
        f"enumerating all three owner values is a duplicate: {restated}")
