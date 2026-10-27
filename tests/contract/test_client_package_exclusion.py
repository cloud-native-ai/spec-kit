"""Contract test: digest path & follow-up carriers — client findings are
digested in place through Path A and never flow upstream (Feature 072, User
Story 3).

Pins `contracts/digest-and-carriers.md` C-25…C-32 against the surfaces that
own them:

* the **digest path uniqueness** (C-25) — client entries are digested only
  through the feedback command's existing Path A; the feature adds no second
  consumption path, no second inventory, and no second cleanup flow;
* the **packaging exclusion** (C-25) — the engine's `package` action excludes
  `kind: external` entries unconditionally, reports the excluded count, and
  carries no switch, parameter, or environment variable that could bypass the
  exclusion;
* the **carrier closed set** (C-26, C-27) — a digested client entry receives
  exactly one follow-up carrier, drawn from a closed set of three existing
  mechanisms (the todo command's Park mode as the default, a new requirements
  specification, one subject loop of the improvement command); the carriers'
  boundaries are cited to their owners, never restated;
* the **two-side target closure** (C-28) — framework friction stays
  framework-side, client defects never reach the framework side, the same
  observation never appears on both sides, and the one-directional refinement
  (internal → this project, never external upstream) is preserved with every
  move reported in the digest;
* the **digest report / routing-backlog discipline** (C-29…C-32) — the report
  carries hat + armed state + resolution, both-side counts and dispositions,
  and the four loop-metric readings; each digested external entry writes
  exactly one routing-backlog row naming its unique carrier; undecidable
  entries are reported `undecided`, never silently dropped; a vanished client
  unit leaves its entries readable and surfaces a named finding; both non-empty
  sides run in the same session.

Behavioural assertions execute inside the disposable client project built by
`tests/fixtures/client_project.py` — the framework repository can never take
the client branch of the hat predicate (C-58).
"""
from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path
from typing import Dict, List

import pytest

from fixtures.client_project import (
    FRAMEWORK_ROOT,
    ClientProject,
    make_client_project,
)

pytestmark = pytest.mark.contract

ENGINE_SRC = FRAMEWORK_ROOT / "scripts" / "python" / "feedback-utils.py"
SKILL_MD = FRAMEWORK_ROOT / "skills" / "internal" / "manage-feedback" / "SKILL.md"
PATH_A = (
    FRAMEWORK_ROOT
    / "skills" / "internal" / "manage-feedback" / "references" / "path-a-digest.md"
)
PATH_B = (
    FRAMEWORK_ROOT
    / "skills" / "internal" / "manage-feedback" / "references" / "path-b-and-probe.md"
)
REFERENCES_DIR = PATH_A.parent
FEEDBACK_TEMPLATE = FRAMEWORK_ROOT / "templates" / "commands" / "feedback.md"
DOCS_FEEDBACK = FRAMEWORK_ROOT / "docs" / "reference" / "commands" / "feedback.md"

#: The carrier owner citations (C-27) — each carrier's boundary is owned by
#: exactly one existing document; the digest reference cites them, never
#: restates their content.
CARRIER_OWNERS = (
    "shared/guidelines/todo-in-context.md",      # Park store boundary
    "templates/commands/requirements.md",        # new-requirements-spec flow
    "shared/workflow/self-improvement-workflow.md",  # improvement subject loop
)

#: Tokens that would constitute a bypass switch for the external exclusion
#: (C-25): no flag, parameter, or environment variable may carry them.
BYPASS_TOKENS = (
    "include-external",
    "include_external",
    "no-exclude-external",
    "skip-external-exclusion",
    "PACKAGE_EXTERNAL",
    "INCLUDE_EXTERNAL",
)

UNIT = "custom:fixture/unit"
RUN_EXT = "2026-10-27T01:00:00Z"
RUN_INT = "2026-10-27T02:00:00Z"


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def record_entry(project: ClientProject, unit_id: str, unit_type: str,
                 run_id: str) -> Dict:
    run = project.run_engine(
        "feedback-utils.py", "--action", "record",
        "--unit-id", unit_id, "--unit-type", unit_type, "--run-id", run_id,
        "--review", "fixture review body for the digest path",
        "--points", "fixture-point-one",
        "--workspace-root", str(project.path),
    )
    assert run.ok, run.describe()
    return run.json_stdout()


def two_sided_store(project: ClientProject) -> None:
    """One external (client-unit) and one internal (framework-unit) open entry."""
    project.arm(UNIT)
    record_entry(project, UNIT, "custom-unit", RUN_EXT)
    record_entry(project, "/speckit.plan", "command", RUN_INT)
    assert int(project.feedback_list_json(kind="external")["count"]) == 1
    assert int(project.feedback_list_json(kind="internal")["count"]) == 1


def package_json(project: ClientProject, extra_env: Dict[str, str] = None) -> Dict:
    run = project.run_engine(
        "feedback-utils.py", "--action", "package", "--format", "json",
        "--workspace-root", str(project.path),
        extra_env=extra_env,
    )
    assert run.ok, run.describe()
    return run.json_stdout()


# --------------------------------------------------------------------------- #
# C-25 — digestion only through existing Path A; packaging exclusion is
#          unconditional and reports the count; no bypass surface
# --------------------------------------------------------------------------- #

def test_c25_digest_goes_through_existing_path_a_only():
    """No second consumption path, inventory, or cleanup flow is introduced."""
    skill_text = SKILL_MD.read_text(encoding="utf-8")
    # The routing table sends client external entries to Path A — the single
    # digest path — and there is no third path.
    assert "`kind: external`" in skill_text and "Path A" in skill_text
    assert "Path C" not in skill_text, (
        "C-25: no second digest path may exist alongside Path A / Path B"
    )
    refs = sorted(p.name for p in REFERENCES_DIR.glob("*.md"))
    assert refs == ["path-a-digest.md", "path-b-and-probe.md"], (
        f"C-25: exactly two path references own digestion and packaging; "
        f"found {refs!r} (a third reference file would be a second path)"
    )
    assert "digest" in PATH_A.read_text(encoding="utf-8").lower()
    assert "package" in PATH_B.read_text(encoding="utf-8").lower()
    # The engine has no second consumption action: entries are consumed via
    # the existing list / dispose / package actions only.
    source = ENGINE_SRC.read_text(encoding="utf-8")
    choices = re.search(r"--action.*?choices=\[([^\]]+)\]", source, re.S)
    assert choices, "the engine must keep an explicit --action choice list"
    action_names = set(re.findall(r'"([a-z-]+)"', choices.group(1)))
    for forbidden in ("digest", "consume", "settle", "resolve"):
        assert forbidden not in action_names, (
            f"C-25: --action {forbidden!r} would be a second consumption path; "
            f"actions stay {sorted(action_names)}"
        )


def test_c25_package_excludes_external_unconditionally_and_reports_the_count():
    with make_client_project() as project:
        two_sided_store(project)
        result = package_json(project)
        assert int(result["excluded_external"]) == 1, (
            f"C-25: the package report MUST carry the excluded-external count; "
            f"got {result!r}"
        )
        assert int(result["packaged"]) >= 1, (
            "the internal (framework-unit) entry is still packaged normally"
        )
        zip_path = project.path / result["zip"]
        assert zip_path.is_file(), result["zip"]
        with zipfile.ZipFile(zip_path) as zf:
            names = zf.namelist()
            manifest = zf.read("MANIFEST.md").decode("utf-8")
            entry_bodies = [
                zf.read(n).decode("utf-8")
                for n in names
                if n.endswith(".md") and n not in ("MANIFEST.md", "SUBMISSION-NOTES.md")
            ]
        assert entry_bodies, "the package must contain the internal entry"
        for body in entry_bodies:
            assert 'kind: "external"' not in body, (
                "C-25: no external entry may appear inside the package zip"
            )
        assert "ext-" not in manifest or "external-custom" not in manifest, (
            "C-25: the package MANIFEST must not carry the external probe object"
        )
        # Packaging is NOT a cleanup flow: the external entry stays in the
        # store, readable, for Path A to digest.
        assert int(project.feedback_list_json(kind="external")["count"]) == 1, (
            "C-25: packaging must never consume the external side "
            "(no second cleanup flow)"
        )


def test_c25_post_package_cleanup_never_touches_external_entries():
    with make_client_project() as project:
        two_sided_store(project)
        result = package_json(project)
        run = project.run_engine(
            "feedback-utils.py", "--action", "cleanup", "--package", "latest",
            "--workspace-root", str(project.path),
        )
        assert run.ok, run.describe()
        out = run.json_stdout()
        assert int(project.feedback_list_json(kind="external")["count"]) == 1, (
            "C-25: post-package cleanup removes only entries inside the zip — "
            "the external entry was never packaged, so it must survive"
        )
        assert int(project.feedback_list_json(kind="internal")["count"]) == 0, (
            "the packaged internal entry is archived and removed by cleanup"
        )
        log = (project.feedback_dir / "cleanup-log.md").read_text(encoding="utf-8")
        assert UNIT not in log, (
            "C-25: the cleanup log must never name a client unit "
            "(cleanup never reaches the external side)"
        )
        assert result["zip"] in out["package"] or out["package"] == result["zip"]


def test_c25_no_bypass_switch_parameter_or_environment_variable():
    source = ENGINE_SRC.read_text(encoding="utf-8")
    # The exclusion is one unconditional filter in the package action …
    assert "selected = [e for e in selected if e.get(\"kind\") != \"external\"]" \
        in source, (
        "C-25: the package action must keep its unconditional external filter"
    )
    # … and the excluded count is always reported.
    assert 'result["excluded_external"] = excluded_external' in source, (
        "C-25: the excluded-external count must be reported on every package run"
    )
    for token in BYPASS_TOKENS:
        assert token not in source, (
            f"C-25: {token!r} would be a bypass switch for the external exclusion"
        )
    # The only environment variable the engine reads at all is the threshold
    # prompt setting — and it must not influence the exclusion either.
    env_reads = re.findall(r'os\.environ\.get\("([A-Z_]+)"\)', source)
    assert env_reads == ["SPECKIT_FEEDBACK_THRESHOLD"], (
        f"C-25: no new environment variable may join the engine surface; "
        f"found reads {env_reads!r}"
    )
    with make_client_project() as project:
        two_sided_store(project)
        result = package_json(project, extra_env={"SPECKIT_FEEDBACK_THRESHOLD": "1"})
        assert int(result["excluded_external"]) == 1, (
            "C-25: even the threshold environment variable must not bypass "
            "the unconditional exclusion"
        )


# --------------------------------------------------------------------------- #
# C-26 — carrier closed set: exactly three, Park default, one entry one carrier
# --------------------------------------------------------------------------- #

def test_c26_carrier_closed_set_is_exactly_three_with_park_default():
    text = PATH_A.read_text(encoding="utf-8")
    for carrier in ("Park", "/speckit.requirements", "subject loop"):
        assert carrier in text, (
            f"C-26: the digest reference MUST name the carrier {carrier!r}"
        )
    assert "exactly one follow-up carrier" in text, (
        "C-26: each digested client entry receives exactly one follow-up carrier"
    )
    assert "no fourth carrier" in text, (
        "C-26: the carrier set is closed at three — no fourth carrier"
    )
    assert re.search(r"Park[^\n]*default|default[^\n]*Park", text), (
        "C-26: Park is the default landing for free-floating improvement ideas"
    )


def test_c26_no_entry_assigned_two_carriers_and_undecided_is_reported():
    text = PATH_A.read_text(encoding="utf-8")
    assert "no entry is ever assigned two carriers" in text, (
        "C-26: one entry, one carrier — double assignment is forbidden"
    )
    assert "undecided" in text, (
        "C-26/C-30: an entry whose carrier cannot be decided is reported "
        "`undecided` and kept for the next digest"
    )
    assert "never silently dropped" in text or "never silently drop" in text, (
        "C-30: an undecidable entry is never silently dropped"
    )


# --------------------------------------------------------------------------- #
# C-27 — carrier boundaries: cite the owners, restate none of their content
# --------------------------------------------------------------------------- #

def test_c27_carrier_sections_cite_owners_without_restatement():
    text = PATH_A.read_text(encoding="utf-8")
    for owner in CARRIER_OWNERS:
        assert owner in text, (
            f"C-27: the digest reference MUST cite the carrier owner {owner!r} "
            "instead of restating its content"
        )
    # The Park store location is owner content of the todo-in-context
    # guideline — the digest reference cites the owner and must not copy it.
    assert ".specify/memory/todo/" not in text, (
        "C-27: the Park store path is owned by shared/guidelines/"
        "todo-in-context.md — the digest reference cites, never restates"
    )


# --------------------------------------------------------------------------- #
# C-28 — two-side target closure and the one-directional refinement
# --------------------------------------------------------------------------- #

def test_c28_entry_kinds_split_by_side_in_the_client_fixture():
    """The stored kind is the discriminator: external entries never name a
    framework unit, internal entries never name a client unit."""
    with make_client_project() as project:
        two_sided_store(project)
        external = project.feedback_list_json(kind="external")["matches"]
        internal = project.feedback_list_json(kind="internal")["matches"]
        assert [e["unit_id"] for e in external] == [UNIT]
        assert all(e["unit_id"].startswith("/speckit.") for e in internal), (
            "C-28: framework friction lives on framework units only"
        )
        overlap = {e["id"] for e in external} & {e["id"] for e in internal}
        assert not overlap, "the same observation never appears on both sides"


def test_c28_two_side_closure_and_refinement_direction_preserved():
    text = SKILL_MD.read_text(encoding="utf-8") + PATH_A.read_text(encoding="utf-8")
    assert "can never move an external entry upstream" in text, (
        "C-28: the one-directional refinement (internal → this project, never "
        "external upstream) is preserved verbatim"
    )
    assert "never appears on both sides" in text, (
        "C-28: the two-side target closure — the same observation never appears "
        "on both sides — must be stated on the digest surface"
    )
    assert "every move is reported in the digest" in text, (
        "C-28: every refinement move must be reported in the digest report"
    )


# --------------------------------------------------------------------------- #
# C-29…C-32 — digest report facts, routing backlog rows, vanished units,
#              both-sides-same-session
# --------------------------------------------------------------------------- #

def test_c29_digest_report_carries_the_three_facts():
    text = PATH_A.read_text(encoding="utf-8")
    assert "armed state" in text, (
        "C-29: the digest report carries this run's hat and armed state plus "
        "how the armed state was resolved"
    )
    assert "four loop metrics" in text, (
        "C-29: the digest report carries the readings of the four loop metrics"
    )
    assert "client-metrics" in text, (
        "C-29: the metrics readings come from the read-only engine action — "
        "the report cites the action, never recomputes"
    )
    assert "atomic cleanup" in text, (
        "C-29: Path A's atomic-cleanup semantics stay unchanged"
    )
    assert re.search(r"metric[^\n]*(never|not)[^\n]*cleanup", text), (
        "C-29: metric computation is never merged into the cleanup action"
    )


def test_c30_routing_backlog_one_named_carrier_row_per_entry():
    text = PATH_A.read_text(encoding="utf-8")
    assert "backlog.md" in text, (
        "C-30: the routing backlog (`.specify/memory/feedback/backlog.md`) "
        "carries the carrier assignment"
    )
    assert re.search(r"exactly one (row|backlog row)", text), (
        "C-30: each digested external entry writes exactly one routing-backlog "
        "row naming its unique carrier"
    )
    assert "digest report" in text, (
        "C-30: the carrier row is listed in the digest report"
    )


def test_c31_vanished_client_unit_entries_stay_readable():
    text = PATH_A.read_text(encoding="utf-8")
    assert "never rewritten, deleted, or re-attributed" in text, (
        "C-31: when a client unit vanishes from the probe registry its existing "
        "entries stay readable and are never rewritten, deleted, or re-attributed"
    )
    assert "named finding" in text, (
        "C-31: the digest report lists the unit's resolution failure as a "
        "named finding"
    )


def test_c32_both_sides_run_in_the_same_session():
    text = SKILL_MD.read_text(encoding="utf-8")
    assert "same session" in text and "Never silently drop one side" in text, (
        "C-32: both non-empty sides run in the same session and are both "
        "reported — one side is never silently dropped to keep the run short"
    )


# --------------------------------------------------------------------------- #
# T015 — the feedback command surfaces carry the client-digest pointers
# --------------------------------------------------------------------------- #

def test_t015_feedback_command_surfaces_carry_client_digest_pointers():
    template = FEEDBACK_TEMPLATE.read_text(encoding="utf-8")
    docs = DOCS_FEEDBACK.read_text(encoding="utf-8")
    for name, text in (("template", template), ("docs page", docs)):
        assert "client-metrics" in text, (
            f"the feedback command {name} MUST point at the read-only "
            "client-metrics action for the digest report's metric readings (T015)"
        )
        assert "Park" in text, (
            f"the feedback command {name} MUST name the Park carrier for "
            "digested client entries (T015/C-26)"
        )
        assert "undecided" in text, (
            f"the feedback command {name} MUST carry the undecided rule for "
            "undecidable carrier assignments (T015/C-30)"
        )
        assert "armed state" in text, (
            f"the feedback command {name} MUST carry the digest-report fact "
            "of this run's hat and armed state (T015/C-29)"
        )
    # The existing packaging and introspection paths stay untouched: the
    # exclusion report and the introspection step remain documented verbatim.
    assert "excluded_external" in docs, (
        "T015: the docs page keeps documenting the engine's excluded-external "
        "packaging report (the packaging path is not moved)"
    )
    assert "introspection" in template.lower() and "introspection" in docs.lower(), (
        "T015: the introspection path stays documented on both surfaces"
    )


# --------------------------------------------------------------------------- #
# T022 — the digest presents the four metric readings as read-only context:
#        never merged into cleanup, never a gate / status transition /
#        threshold input
# --------------------------------------------------------------------------- #

def test_t022_digest_surfaces_present_metrics_as_read_only_non_gate():
    template = FEEDBACK_TEMPLATE.read_text(encoding="utf-8")
    docs = DOCS_FEEDBACK.read_text(encoding="utf-8")
    for name, text in (("template", template), ("docs page", docs)):
        assert "client-metrics" in text, (
            f"T022: the feedback command {name} MUST keep pointing at the "
            "read-only client-metrics action for the metric readings"
        )
    # Template (Chinese surface): the readings are read-only presentation.
    assert "不并入清理" in template, (
        "T022: the feedback command template MUST state that metric readings "
        "are never merged into the cleanup action"
    )
    assert "门禁" in template and "阈值" in template, (
        "T022: the feedback command template MUST state that the readings are "
        "not a gate and not a threshold input"
    )
    # Docs page (English surface): the full non-influence statement.
    for phrase in ("never merged into cleanup", "never a gate",
                   "status-transition", "threshold input"):
        assert phrase in docs, (
            f"T022: the feedback command docs page MUST carry {phrase!r} — "
            "the readings influence nothing"
        )
