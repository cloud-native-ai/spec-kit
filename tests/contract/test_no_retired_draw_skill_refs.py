"""Contract test: no LIVE surface may still name the six retired draw-* engine skills.

On 2026-10-12 `draw-{d3js,drawio,echarts,excalidraw,mermaid,plantuml}` were merged into
`draw-diagram` as internal engine layers under `draw-diagram/references/types/<engine>/`.
A retirement that leaves live references behind fails in two directions at once: the
reference dangles (the skill is gone from every load directory), and the reader is pointed
at a competing entry point that no longer exists — which is exactly why `_OBSOLETE_SKILLS`
alone is not sufficient: it reclaims directories, not prose.

Scope is the LIVE surface — what a reader consults as current reality. Dated records are
deliberately excluded and MUST NOT be rewritten: a run report, spec, or history page that
names a then-existing skill is a true statement about its own time, and editing it would
falsify the record (One Source Of Truth: a dated record is a legitimate duplicate).

Two live-looking files are exempt by design, and each exemption is asserted so it cannot
silently widen:
  * the capability-inheritance record and its frozen baselines, which exist precisely to
    name the sources;
  * `_OBSOLETE_SKILLS`, which names them in order to delete them.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

RETIRED = ("draw-d3js", "draw-drawio", "draw-echarts", "draw-excalidraw",
           "draw-mermaid", "draw-plantuml")
SLUG = re.compile(r"\b(?:" + "|".join(RETIRED) + r")\b")
# A team directory really is named draw-plantuml-optimizer and still exists; renaming the
# reference would dangle the path. The team name is not a skill reference.
TEAM_NAME = re.compile(r"\bdraw-plantuml-optimizer\b")

LIVE_ROOTS = ("skills", "templates", "shared", "docs", "src")
LIVE_FILES = (".specify/instructions.md", ".specify/shared",
              ".specify/memory/knowledge", ".specify/memory/glossary.md")

# Dated records and generated artifacts: true statements about their own time, or
# machine-owned output that is regenerated rather than edited.
EXCLUDED_PARTS = (
    "history",            # docs/reference/history/**
    "public",             # docs/public/** — Hugo build output, regenerated
    "specs",              # .specify/specs/**
    "teams",              # .specify/teams/**  (run reports, team definitions)
    "review",             # .specify/review/**
    "notes",              # docs/notes/** — lesson notes tied to a dated instance
    "node_modules", "__pycache__", ".git",
)
EXCLUDED_FILES = {
    # the record that owns the merge's provenance, and its frozen fact baselines
    "merge-provenance.md",
    # the reclaim registry names the retired skills in order to delete them
    "__init__.py",
}
EXCLUDED_SUFFIXES = (".baseline.txt",)
# Whole-file exemption, kept to exactly one entry and asserted narrow below: the arena
# benchmark ledger. Its data is a dated measurement that must not be rewritten, and it
# carries a superseded banner (asserted by its own test) naming the current authority.
BANNER_REQUIRED = ".specify/memory/knowledge/visualization-skill-selection.md"
EXEMPT_WITH_BANNER = {BANNER_REQUIRED}


def _is_exempt(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if any(part in EXCLUDED_PARTS for part in path.parts[:-1]):
        return True
    if path.name in EXCLUDED_FILES:
        return True
    if rel.endswith(EXCLUDED_SUFFIXES) or rel in EXEMPT_WITH_BANNER:
        return True
    return rel.startswith(".specify/memory/feedback/") or rel.startswith(
        ".specify/memory/evidence/") or rel.startswith(".specify/memory/session/")


def _live_candidates():
    for root in LIVE_ROOTS:
        base = ROOT / root
        if base.is_dir():
            yield from (p for p in sorted(base.rglob("*")) if p.is_file())
    for rel in LIVE_FILES:
        p = ROOT / rel
        if p.is_file():
            yield p
        elif p.is_dir():
            yield from (q for q in sorted(p.rglob("*")) if q.is_file())


def _offenders():
    out = []
    for path in _live_candidates():
        if _is_exempt(path) or path.suffix.lower() in {".png", ".svg", ".ico", ".woff2"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if TEAM_NAME.search(line):
                line = TEAM_NAME.sub("", line)
            if SLUG.search(line):
                out.append(f"{path.relative_to(ROOT)}:{i}")
    return out


@pytest.mark.contract
def test_no_live_surface_names_a_retired_draw_skill():
    offenders = _offenders()
    assert not offenders, (
        "live surface(s) still name a retired draw-* engine skill — the six are internal\n"
        "engine layers of draw-diagram now (references/types/<engine>/). Re-point the\n"
        "reference to draw-diagram, or to the engine layer path when the statement is\n"
        f"about one engine:\n  " + "\n  ".join(offenders[:25])
        + ("\nIf the file is a dated record, add its directory to EXCLUDED_PARTS —\n"
           "do NOT rewrite the record." if len(offenders) > 25 else ""))


@pytest.mark.contract
def test_the_superseded_knowledge_ledger_carries_its_banner():
    """The one live file allowed to keep the old names must say why."""
    path = ROOT / BANNER_REQUIRED
    assert path.is_file(), f"sentinel: the ledger moved: {BANNER_REQUIRED}"
    text = path.read_text(encoding="utf-8")
    assert "已超越" in text and "routing-matrix.md" in text, (
        f"{BANNER_REQUIRED} keeps arena data naming the retired skills; it must carry a\n"
        "superseded banner that points at the current routing authority, or a reader\n"
        "takes a 2026-08 benchmark as today's skill topology.")


@pytest.mark.contract
def test_the_exemptions_are_narrow():
    """Guard the guard: exemptions must not widen into a hole."""
    assert EXCLUDED_FILES == {"merge-provenance.md", "__init__.py"}
    assert EXCLUDED_SUFFIXES == (".baseline.txt",)
    assert EXEMPT_WITH_BANNER == {
        ".specify/memory/knowledge/visualization-skill-selection.md"}
    # the provenance record really does name all six, i.e. the exemption is load-bearing
    record = ROOT / "skills/external/draw-diagram/references/merge-provenance.md"
    assert record.is_file(), "sentinel: the capability-inheritance record is missing"
    text = record.read_text(encoding="utf-8")
    for slug in RETIRED:
        assert slug in text, f"the record no longer names {slug} — exemption is stale"


@pytest.mark.contract
def test_engine_layers_exist_where_the_record_says():
    base = ROOT / "skills/external/draw-diagram/references/types"
    for engine in ("d3js", "drawio", "echarts", "excalidraw", "mermaid", "plantuml"):
        entry = base / engine / f"{engine}.md"
        assert entry.is_file(), f"engine layer entry doc missing: {entry.relative_to(ROOT)}"
        assert not (base / engine / "SKILL.md").exists(), (
            f"{engine} engine layer ships a nested SKILL.md — it is a reference doc, not "
            "a skill (test_no_nested_skills.py forbids this)")
