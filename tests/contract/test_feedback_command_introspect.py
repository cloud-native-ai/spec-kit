"""Structural contract test: /speckit.feedback's introspection step.

Originally pinned req 047's ``### Mode 5``. The command's five input-keyed modes
were collapsed into two auto-selected paths on 2026-09-20, so the section keys
moved — ``### Mode 5`` is now ``#### A3 — Introspection`` inside ``### Path A``,
and ``### Mode 2`` is now ``### Path B``. **Every substance assertion the
mode-keyed version made is kept here**; only the way the slices are located
changed. Re-keying without carrying the substance over would have turned this
file into a tautology, which is the failure mode this repo's blind-check lesson
(``docs/reference/history/00-cross-cutting-lessons.md`` § 十二) is about.

What is still guarded: the five introspection steps by name and in order, the
re-introspection ``supersedes`` rule, both red lines, external-never-upstream,
the token-efficiency discipline, Path B's report-enriched packaging offer, and
all four regenerated per-tool copies.
"""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates" / "commands" / "feedback.md"
COPIES = [
    ROOT / ".claude" / "commands" / "speckit.feedback.md",
    ROOT / ".qoder" / "commands" / "speckit.feedback.md",
    ROOT / ".opencode" / "command" / "speckit.feedback.md",
    ROOT / ".github" / "prompts" / "speckit.feedback.prompt.md",
]

PATH_A = "### Path A"
INTROSPECTION = "#### A3 — Introspection"
ROUTE_STEP = "#### A4 — Reconcile and route findings"
PATH_B = "### Path B"
INJECTION = "### Probe Injection"


def _template_text() -> str:
    return TEMPLATE.read_text(encoding="utf-8")


def _slice(text: str, start: str, end: str) -> str:
    """Bounded slice, with the bounds asserted so a renamed heading cannot
    silently collapse this to an empty or whole-file slice."""
    i = text.find(start)
    j = text.find(end)
    assert i >= 0, f"section missing: {start!r}"
    assert j > i, f"section {end!r} does not follow {start!r}"
    return text[i:j]


def _introspection() -> str:
    return _slice(_template_text(), INTROSPECTION, ROUTE_STEP)


def _path_a() -> str:
    return _slice(_template_text(), PATH_A, PATH_B)


def _path_b() -> str:
    return _slice(_template_text(), PATH_B, INJECTION)


@pytest.mark.contract
class TestIntrospectionPresenceAndPosition:
    """The analysis step exists, sits inside Path A, and precedes deletion."""

    def test_introspection_section_present_inside_path_a(self):
        text = _template_text()
        assert text.find(INTROSPECTION) > 0, "introspection section missing"
        assert text.find(PATH_A) > 0, "Path A section missing"
        assert text.find(PATH_A) < text.find(INTROSPECTION), (
            "introspection must live inside Path A — it is the digest path's "
            "analysis step, not a separately-triggered mode"
        )

    def test_analysis_precedes_cleanup(self):
        """Req 047 pinned Mode 5 before Mode 4 for the same reason: the routing
        analysis must be stated before the step that deletes the intake."""
        text = _template_text()
        assert text.find(INTROSPECTION) < text.find("#### A5 — Cleanup"), (
            "introspection must precede Path A's cleanup step — routing is "
            "decided before anything is deleted"
        )

    def test_introspect_wording_present(self):
        assert "introspect" in _template_text()

    def test_frontmatter_names_two_paths_and_introspection(self):
        text = _template_text()
        head = text.split("---")[1] if text.startswith("---") else text[:600]
        assert "two execution paths" in head or "Path A" in head, head
        assert "自省" in head, "the frontmatter must still surface 自省"


@pytest.mark.contract
class TestIntrospectionDiscipline:
    """Token discipline + both red lines + external-never-upstream."""

    def test_token_efficiency_note(self):
        assert "摘要优先" in _template_text() or "Token 效率" in _template_text()

    def test_red_lines_stated(self):
        scope = _path_a()
        assert "MUST NOT" in scope or "禁止" in scope
        assert "自动传输" in scope

    def test_external_never_upstream(self):
        scope = _introspection()
        assert "local-sink" in scope
        assert "external" in scope.lower()
        # The constraint is engine-enforced, not advisory — the template says so.
        assert "引擎" in scope, (
            "the external-never-upstream rule must name the engine as its "
            "enforcer; a prose-only admonition is weaker than what the engine does"
        )


@pytest.mark.contract
class TestGeneratedCopies:
    """All four per-tool copies carry the introspection step."""

    @pytest.mark.parametrize("copy", COPIES, ids=[p.parts[-2] for p in COPIES])
    def test_copy_contains_introspection(self, copy: Path):
        assert copy.exists(), f"missing generated copy: {copy}"
        text = copy.read_text(encoding="utf-8")
        assert INTROSPECTION in text
        assert PATH_A in text and PATH_B in text


@pytest.mark.contract
class TestIntrospectionFlowCompleteness:
    """The five steps by name and in order, plus the re-introspection rule."""

    def test_five_steps_in_order(self):
        scope = _introspection()
        steps = ["范围快照", "场景化分析", "报告产出", "用户确认", "路由建议"]
        positions = [scope.find(s) for s in steps]
        assert all(p > 0 for p in positions), \
            f"missing steps: {[s for s, p in zip(steps, positions) if p <= 0]}"
        assert positions == sorted(positions), "steps out of order"

    def test_reintrospection_supersede_rule(self):
        scope = _introspection()
        assert "supersedes" in scope
        assert "重复自省" in scope


@pytest.mark.contract
class TestPackagingIntegration:
    """Path B still offers report-enriched packaging and still points at the
    introspection step as an advised-but-optional pre-run."""

    def test_path_b_offers_include_introspection(self):
        assert "--include-introspection" in _path_b()

    def test_threshold_note_mentions_introspection(self):
        assert "Introspection" in _path_b() or "introspect" in _path_b()

    def test_introspection_is_advisory_not_mandatory(self):
        scope = _path_b()
        assert "建议而非强制" in scope, (
            "running introspection before packaging must stay advisory — "
            "making it mandatory would block a user who only wants to package"
        )
