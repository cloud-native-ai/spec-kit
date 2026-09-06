"""Integration test — User Story 1: land a handed-in reference list as a verifiable
graded source table (048 / Feature 049, Priority P1).

Driving contract: .specify/specs/048-derive-command/contracts/derivation-model.md
                  (§2 grades & anchoring, §6 title_mismatch & verification)
Success criterion: SC-001 (source table grouped by grade / access / title_mismatch
                  over the fixed four-class corpus).

End-to-end over the shared synthetic corpus: init -> moves-add -> write the
archive -> validate, then read the four classes the way the Dead-Link Protocol
produces them — a live primary, a wayback-rescued retitled primary, a community
listicle (a finding aid, never an anchor), and a dead unverifiable source that is
recorded rather than dropped.
"""

from __future__ import annotations

import pytest

from tests.derive_fixtures import (
    CHAIN,
    SOURCES,
    TOPIC,
    build_artifact,
    codes,
    scaffold,
    seed_library,
    validate,
    write_artifact,
)

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def story(tmp_path_factory):
    ws = tmp_path_factory.mktemp("derive-us1")
    code, env = scaffold(ws)
    assert code == 0, env
    seed_library(ws)
    write_artifact(ws, build_artifact(), TOPIC)
    vcode, venv = validate(ws, TOPIC)
    return ws, vcode, venv


def test_the_whole_list_lands_and_validates_clean(story):
    _, code, env = story
    assert code == 0, env.get("errors")
    assert env["ok"] is True and env["errors"] == []
    assert env["payload"]["sources"]["total"] == 4


def test_sc001_grouping_by_grade_and_access(story):
    _, _, env = story
    src = env["payload"]["sources"]
    assert src["byGrade"] == {"primary": 2, "authoritative-secondary": 0,
                              "community": 1, "unverified": 1}
    assert src["byAccess"] == {"live": 2, "wayback": 1, "dead": 1, "paywalled": 0, "unknown": 0}


def test_live_primary_is_grounded_directly(story):
    _, _, env = story
    row = next(r for r in _source_rows() if r["id"] == "S-001")
    assert row["grade"] == "primary" and row["access"] == "live" and row["resolved_via"] == "direct"
    assert env["payload"]["sources"]["byGrade"]["primary"] >= 1


def test_wayback_rescue_does_not_downgrade_the_grade(story):
    """C-10: a snapshot recovering the author's own page is still `primary`; the
    wayback + primary combination is legal and raises no grade/access error."""
    _, _, env = story
    row = next(r for r in _source_rows() if r["id"] == "S-002")
    assert row["grade"] == "primary" and row["access"].startswith("wayback:")
    assert "grade-not-in-enum" not in codes(env)
    assert "unknown-access-with-verified-grade" not in codes(env)


def test_the_retitle_is_computed_not_asserted(story):
    """SC-001: exactly one mismatch (the wayback-rescued retitled source), and the
    count is the engine's normalized comparison, not the agent's claim."""
    _, _, env = story
    assert env["payload"]["sources"]["titleMismatch"] == 1
    # A3: the retitled source is cited by its resolved title in the step that uses it.
    assert "resolved-title-not-cited" not in codes(env)
    assert "In search of the ideal identifier" in CHAIN
    assert "title-mismatch-asserted" not in codes(env)


def test_community_listicle_is_a_finding_aid_never_an_anchor(story):
    """S-003 is `community`: it may appear only in `leads`, never in `premises`."""
    _, _, env = story
    row = next(r for r in _source_rows() if r["id"] == "S-003")
    assert row["grade"] == "community"
    assert "- leads: S-003" in CHAIN
    assert "premise-grade-ineligible" not in codes(env)


def test_dead_unverifiable_source_is_recorded_not_dropped(story):
    """A2 / FR-005: the dead source is graded unverified, recorded in
    ## Unverifiable Sources with its reason, and never used as an anchor."""
    ws, _, env = story
    row = next(r for r in _source_rows() if r["id"] == "S-004")
    assert row["grade"] == "unverified" and row["access"] == "dead"
    assert "unverified-source-unrecorded" not in codes(env)
    text = (ws / ".specify" / "derive" / TOPIC / "derive.md").read_text(encoding="utf-8")
    unverifiable = text.split("## Unverifiable Sources", 1)[1].split("## ", 1)[0]
    assert "S-004" in unverifiable


def test_zero_steps_anchor_on_community_or_unverified(story):
    """C1: every anchoring premise is primary/authoritative-secondary; both steps
    are anchorable, so the count of anchored steps equals the count of steps."""
    _, _, env = story
    steps = env["payload"]["steps"]
    assert steps["total"] == 2 and steps["anchorable"] == 2
    assert "premise-grade-ineligible" not in codes(env)
    # the only premise sources are the two primaries
    assert "S-001" in CHAIN and "S-002" in CHAIN
    assert "premises: S-003" not in CHAIN and "premises: S-004" not in CHAIN


def _source_rows():
    """Positional read of the fixture's ## Sources rows (synthetic, no escaped pipes)."""
    cols = ("id", "claimed_title", "resolved_title", "title_mismatch", "grade",
            "url", "access", "resolved_via", "verification")
    rows = []
    for line in SOURCES.splitlines():
        if not line.startswith("| S-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(dict(zip(cols, cells)))
    assert rows, "fixture source table changed shape"
    return rows
