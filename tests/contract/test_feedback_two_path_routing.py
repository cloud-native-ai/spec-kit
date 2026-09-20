"""Contract test: /speckit.feedback's two-path routing decision.

Guards the router itself — the part that replaced five input-keyed modes on
2026-09-20. The engine's ``--action`` surface is unchanged and is guarded
elsewhere (``test_dogfooding_practice.py`` pins the closed 14-action set by
equality); what this file pins is the *judgment*: how the command decides which
side an item falls on, and the four edge rules that keep the decision honest.

Two of these assertions exist because the thing they guard is easy to lose
without noticing. The pinned literal ``confirmation of the report`` is also in
``test_confirmation_gates_sweep.py``'s KEEP_LIST, but that test only checks the
string exists somewhere in the file — it would still pass if the sentence drifted
out of the cleanup step and lost its meaning, so its position is re-asserted
here. And the one-directional refinement rule is the only thing stopping a
future edit from routing a client project's own feedback upstream, which the
engine would reject at exit 2 but only after the agent had already promised it.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates" / "commands" / "feedback.md"

# The generated copies, not just the source: rewrite_paths only runs on them, so
# a criterion that is correct in the template can be inverted in every copy an
# agent actually reads.
COPIES = [
    ROOT / ".claude" / "commands" / "speckit.feedback.md",
    ROOT / ".qoder" / "commands" / "speckit.feedback.md",
    ROOT / ".opencode" / "command" / "speckit.feedback.md",
    ROOT / ".github" / "prompts" / "speckit.feedback.prompt.md",
]

OUTLINE = "## Outline"
PATH_A = "### Path A"
PATH_B = "### Path B"
INJECTION = "### Probe Injection"
BEHAVIOR = "## Behavior Rules"
CLEANUP = "#### A5 — Cleanup"


def _text() -> str:
    return TEMPLATE.read_text(encoding="utf-8")


def _slice(start: str, end: str) -> str:
    text = _text()
    i = text.find(start)
    j = text.find(end)
    assert i >= 0, f"section missing: {start!r}"
    assert j > i, f"section {end!r} does not follow {start!r}"
    return text[i:j]


def _outline() -> str:
    return _slice(OUTLINE, BEHAVIOR)


def _path_a() -> str:
    return _slice(PATH_A, PATH_B)


@pytest.mark.contract
def test_outline_is_substantive():
    """Anti-vacuity sentinel: every assertion below reads a slice of ## Outline,
    so an accidentally empty slice would make them all pass for nothing."""
    outline = _outline()
    assert len(outline) > 4000, f"the Outline section is suspiciously thin: {len(outline)} chars"
    assert outline.count("\n1. ") + outline.count("\n2. ") >= 2, "the routing flow is not numbered"
    for path in (PATH_A, PATH_B, INJECTION):
        assert path in _text(), f"missing section: {path}"


@pytest.mark.contract
def test_hat_is_the_primary_discriminator():
    """The bug this test exists for: `kind` alone cannot decide the route, because
    "points at this project" is a relation between an entry and the repo you are
    standing in. In the framework repo every entry points at this project, so a
    kind-based router recommends packaging feedback for manual delivery to yourself.
    """
    outline = _outline()
    assert "hat decides first" in outline, (
        "the Outline must state that the hat is the primary discriminator and "
        "kind the secondary one"
    )
    for needle in ("templates", "skills", "src/specify_cli"):
        assert needle in outline, f"the hat criterion no longer names {needle}"
    assert "Do NOT gate on `feedback/` directory existence" in outline, (
        "the hat criterion must keep its caveat — a client project can have a "
        "feedback/ directory for unrelated purposes, so its existence proves nothing"
    )
    # Framework project => everything is Path A material, and Path B is not selected.
    assert "Path B is not selected" in outline or "Path B is reachable only by an explicit" in outline, (
        "in the framework project the router must not select Path B on its own"
    )


@pytest.mark.contract
def test_framework_project_does_not_auto_package():
    text = _text()
    path_b = _slice(PATH_B, INJECTION)
    assert "Reached automatically only from a client project" in path_b, (
        "Path B must declare that the framework project reaches it only on request — "
        "a zip packaged in the framework repo is addressed to that same repository"
    )
    assert "taken on request rather than by judgment" in path_b


@pytest.mark.contract
def test_hat_criterion_survives_the_per_tool_path_rewrite():
    """`regen-command-copies.py` runs `rewrite_paths`, which turns any `templates/`,
    `shared/`, `scripts/` or `memory/` reference that starts a path into its
    `.specify/` mirror form. That is correct for a doc path a reader opens at
    runtime and **inverts the meaning** of a criterion that tests for framework
    *source* directories: `.specify/templates/` exists in every client project, so
    the gate would pass everywhere. This assertion reads the generated copies —
    the artifacts an agent actually runs — not the source template.
    """
    for copy in COPIES:
        assert copy.is_file(), f"missing generated copy: {copy}"
        text = copy.read_text(encoding="utf-8")
        gate_line = next(
            (ln for ln in text.splitlines() if "hat this repo wears" in ln), None
        )
        assert gate_line, f"{copy.name}: the hat criterion line is missing"
        assert ".specify/templates" not in gate_line, (
            f"{copy.name}: the hat criterion was rewritten to the runtime mirror, so "
            "it now passes in every client project. Name the source directories "
            "without a trailing slash — rewrite_paths only matches `segment/`."
        )
        for needle in ("`templates`", "`skills`", "`src/specify_cli`"):
            assert needle in gate_line, f"{copy.name}: hat criterion lost {needle}"


@pytest.mark.contract
def test_owning_hat_rule_is_not_contradicted_by_the_rewrite():
    """Same hazard, second instance: the Path A rule says "act on the framework
    source, never in the .specify/ mirror". Rewritten, it listed .specify/templates/
    as the source and then forbade .specify/ mirrors — self-contradictory guidance
    in every copy an agent reads."""
    for copy in COPIES:
        text = copy.read_text(encoding="utf-8")
        line = next((ln for ln in text.splitlines() if "Fix at the owning hat" in ln), None)
        assert line, f"{copy.name}: the owning-hat rule is missing"
        assert ".specify/templates" not in line, (
            f"{copy.name}: the owning-hat rule names the runtime mirror as the "
            "framework source and then forbids editing mirrors"
        )
        assert "never in the `.specify/` runtime mirror" in line


@pytest.mark.contract
def test_classification_uses_the_stored_kind_field():
    outline = _outline()
    assert "kind" in outline, "the router must name the field it classifies on"
    assert "external" in outline and "internal" in outline
    assert "host-custom" in outline, "the external slice must be named"
    assert "custom:<owner>/<name>" in outline, (
        "the router must say what makes an entry external — a unit id in the "
        "custom: namespace, not a judgment call"
    )


@pytest.mark.contract
def test_content_refinement_is_one_directional():
    outline = _outline()
    assert "one-directional" in outline, (
        "the refinement rule must state its direction; an unstated rule reads "
        "as symmetric and a future edit will route external entries upstream"
    )
    assert "upstream-bound" in outline and "local-sink" in outline
    assert "exit 2" in outline, (
        "the rule must name the engine's enforcement, so it reads as a fact "
        "about the engine rather than as this document's preference"
    )


@pytest.mark.contract
def test_both_sides_non_empty_runs_a_then_b():
    outline = _outline()
    assert "Path A then Path B" in outline, (
        "when both sides have work, the order must be stated — digestion can "
        "change what is left to package"
    )
    assert "Never silently drop one side" in outline


@pytest.mark.contract
def test_empty_scope_writes_no_report_file():
    outline = _outline()
    assert "Do NOT write an empty report file" in outline, (
        "an empty run must not leave an artifact behind; a report file with no "
        "findings is indistinguishable from a report nobody read"
    )


@pytest.mark.contract
def test_undecidable_input_asks_exactly_one_question():
    outline = _outline()
    assert "one** elicitation question" in outline or "ONE elicitation question" in outline, (
        "an undecidable target must produce a single question, not a loop"
    )
    assert "do not guess silently" in outline.lower() or "do NOT guess silently" in outline


@pytest.mark.contract
def test_package_is_an_explicit_shortcut():
    """`package` must stay a valid user-facing invocation.

    It is no longer what the wrap-up prompt names — the prompt points at
    `/speckit.feedback` and lets the command judge, because naming a disposition the
    judgment has not made is how the framework project ended up being told to package a
    zip addressed to itself. What stays load-bearing is that an explicit request still
    reaches Path B in either hat.
    """
    user_input = _slice("## User Input", "## Glossary")
    assert "package" in user_input, "the short-circuit must be documented at the entry point"
    path_b = _slice(PATH_B, INJECTION)
    assert "explicit `package` request" in path_b, (
        "Path B must state that an explicit request still reaches it — including from the "
        "framework project, where the router never selects it on its own"
    )


@pytest.mark.contract
def test_probe_injection_is_declared_outside_the_router_with_a_reason():
    text = _text()
    injection = _slice(INJECTION, BEHAVIOR)
    assert "cannot be inferred" in injection, (
        "injection sits outside the automatic router for a stated reason — an "
        "unexplained exception invites the next edit to fold it back in"
    )
    assert "--action probe-inject" in injection
    # The route table must carry it as an out-of-scope row, the house form.
    assert "超出自动分流" in _outline()


@pytest.mark.contract
def test_cleanup_confirmation_literal_is_inside_the_cleanup_step():
    """Position, not just presence: the sweep test's KEEP_LIST only checks the
    string exists in the file."""
    cleanup = _slice(CLEANUP, "#### A6")
    assert "confirmation of the report" in cleanup, (
        "the pinned literal must stay in Path A's cleanup step, where it means "
        "'the user confirms the routing decisions, not that every routed run "
        "finished' — elsewhere in the file it guards nothing"
    )
    assert "NOT completion of every downstream routed run" in cleanup
    # The gate confirmation-gates.md's governance-kept list names: a
    # pre-delete confirmation owned by this file.
    assert "Orphan preserve-first precondition" in cleanup
    assert "consume-log.md" in cleanup


@pytest.mark.contract
def test_judgment_is_reported_not_assumed():
    behavior = _slice(BEHAVIOR, "## Documentation")
    assert "reported, not assumed" in behavior, (
        "the run must state which hat it detected, how many items landed on "
        "each side, and anything the content analysis moved — otherwise a "
        "mis-route is invisible to the user reading the output"
    )


@pytest.mark.contract
def test_no_mode_numbering_survives_anywhere():
    text = _text()
    assert not re.findall(r"(?m)^#{2,4} Mode \d", text)
    for stale in ("five execution modes", "Mode 1", "Mode 2", "Mode 3", "Mode 4", "Mode 5",
                  "模式三", "模式四"):
        assert stale not in text, f"stale mode reference survived: {stale!r}"


@pytest.mark.contract
def test_command_template_carries_no_blocking_gate_wording():
    """The gate-count budget has zero integer headroom, and this file is inside
    the scanner's scope. Reuses the real scanner's own compiled pattern rather
    than a copy of it (precedent: test_ask_record_repeat.py)."""
    import importlib.util

    scanner = ROOT / "scripts" / "python" / "scan-confirmation-gates.py"
    spec = importlib.util.spec_from_file_location("scg", scanner)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    hits = [
        (i + 1, m.group(0))
        for i, line in enumerate(_text().splitlines())
        if (m := module.BLOCKING_RE.search(line))
    ]
    assert not hits, (
        f"templates/commands/feedback.md gained blocking-gate wording {hits}; the "
        "scanner's total is pinned at exactly 23 with zero headroom"
    )
