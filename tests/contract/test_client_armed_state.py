"""Contract test: client identity & armed state — the three-valued honest twin
of client capture (Feature 072, User Story 2).

Pins `contracts/client-identity-and-armed-state.md` C-1…C-9 against the
surfaces that own them:

* the **hat judgement** — only the existing owner criterion
  (`.specify/shared/definitions/dogfooding-definitions.md` § 2.1) decides
  client vs framework; a root-level ``feedback/`` directory MUST NOT
  participate (C-1);
* the **armed-state resolver** inside the ``capture`` subcommand of
  `skills/internal/code-review/scripts/git-delta-review.sh` — the feature's
  single parser (C-9), resolved once per run from the probe engine's
  machine-readable output and reused unchanged (C-2);
* the **disclosure vocabulary** — a closed three-value armed-state set
  (`client-channel-armed` / `client-channel-unarmed` / `client-unit-ambiguous`)
  with named one-time guidance for every unarmed case and zero entries for
  every non-capture case (C-3, C-4, C-5);
* the **unit grammar** — `--client-unit` with a value closed at
  `custom:<owner>/<name>`; malformed values and the `/speckit.*` / `skill:`
  families are rejected with one named skip line, never reaching the engine
  (C-6, C-7);
* the **entry scope** — three existing fields (`kind: external`,
  `slice: host-custom`, the `custom:` unit) plus the run id, with no fourth
  scope field and no new id family (C-8);
* the **review command surfaces** — `templates/commands/review.md` and
  `docs/reference/commands/review.md` stay aligned on the parameter, the
  fifth step and the conclusion disclosure (T012), and the Dogfooding Loop B
  recipe uses the `custom:` form (C-7).

Every behavioural assertion executes inside the disposable client project
built by `tests/fixtures/client_project.py` — the framework repository can
never take the client branch of the hat predicate (C-58).
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Dict, List, Optional

import pytest

from fixtures.client_project import (
    FRAMEWORK_ROOT,
    ClientProject,
    make_client_project,
    make_framework_hat_twin,
)

pytestmark = pytest.mark.contract

REVIEW_SCRIPT = FRAMEWORK_ROOT / "skills" / "internal" / "code-review" / "scripts" / "git-delta-review.sh"
SKILL_MD = FRAMEWORK_ROOT / "skills" / "internal" / "code-review" / "SKILL.md"
REVIEW_TEMPLATE = FRAMEWORK_ROOT / "templates" / "commands" / "review.md"
DOCS_REVIEW = FRAMEWORK_ROOT / "docs" / "reference" / "commands" / "review.md"
HAT_OWNER_DOC = FRAMEWORK_ROOT / ".specify" / "shared" / "definitions" / "dogfooding-definitions.md"
PROBE_DEFS = FRAMEWORK_ROOT / ".specify" / "shared" / "definitions" / "probe-definitions.md"

SPEC_DIR = ".specify/specs/072-armed-demo"
RECORD_REL = f"{SPEC_DIR}/code-review.md"
STAMP = "20261027T000000Z"           # REVIEW_RUN_TIMESTAMP override (deterministic)
RUN_ID = "2026-10-27T00:00:00Z"      # the record header date stamp derived from it
UNIT = "custom:fixture/unit"
OTHER_UNIT = "custom:fixture/other"

#: The closed armed-state token set (C-2). The full five-token disclosure set
#: (which adds `no-capture-object` / `counts-unavailable`) is pinned by
#: tests/contract/test_client_capture.py.
ARMED_TOKENS = {
    "client-channel-armed",
    "client-channel-unarmed",
    "client-unit-ambiguous",
}

#: The unit value grammar, closed at `custom:<owner>/<name>` (C-6).
UNIT_GRAMMAR_LITERAL = "custom:<owner>/<name>"

#: The five framework source directories of the hat owner criterion (C-1).
OWNER_HAT_DIRS = ("templates", "skills", "shared", "scripts", "src/specify_cli")

#: The closed frontmatter key set of an existing feedback entry (C-8 proves
#: this feature adds no fourth scope field and no new id family). Owned by
#: feedback-utils.py `dump_frontmatter`'s key order.
ENTRY_KEY_SET = {
    "id", "unit_id", "unit_type", "run_id", "scope", "feature", "feature_id",
    "partial", "created", "summary", "probe", "kind", "slice",
    "disposition", "migrated_from", "introspection_ref", "disposition_reason",
}


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def run_review(project: ClientProject, *args: str,
               extra_env: Optional[Dict[str, str]] = None):
    env = {"REVIEW_RUN_TIMESTAMP": STAMP}
    if extra_env:
        env.update(extra_env)
    return project.run_script(str(REVIEW_SCRIPT), *args, extra_env=env)


def capture_lines(stdout: str) -> List[str]:
    return [line for line in stdout.splitlines() if line.startswith("capture:")]


def external_count(project: ClientProject) -> int:
    return int(project.feedback_list_json(kind="external")["count"])


def total_entries(project: ClientProject) -> int:
    """Every entry in the store, regardless of kind (C-4's legacy-entry guard)."""
    run = project.run_engine(
        "feedback-utils.py", "--action", "list", "--format", "json",
        "--workspace-root", str(project.path),
    )
    assert run.ok, run.describe()
    return int(run.json_stdout()["count"])


def entry_file(project: ClientProject) -> Path:
    listing = project.feedback_list_json(kind="external")
    assert len(listing["matches"]) == 1, listing
    return project.path / listing["matches"][0]["path"]


def qualified_run(project: ClientProject) -> Path:
    """Two commits with a code delta; triage=run; record created (no notes —
    all six counts are zero, the summary gate allows, exit 0)."""
    project.write("src/app.py", "def f():\n    return 1\n")
    project.commit("base", ["src/app.py"])
    project.write("src/app.py", "def f():\n    return 2\n")
    project.commit("change", ["src/app.py"])
    triage = run_review(project, "triage", "--since", "HEAD~1", "--head", "HEAD")
    assert triage.returncode == 0 and "triage=run" in triage.stdout, triage.describe()
    start = run_review(project, "start", "--spec", SPEC_DIR,
                       "--since", "HEAD~1", "--head", "HEAD", "--triage", "run")
    assert start.returncode == 0, start.describe()
    record = project.path / RECORD_REL
    assert record.is_file()
    return record


def armed_capture(project: ClientProject, *extra: str):
    return run_review(project, "capture", "--review-file", RECORD_REL,
                      "--triage", "run", *extra)


# --------------------------------------------------------------------------- #
# C-1 — the hat judgement is made only by the existing owner criterion
# --------------------------------------------------------------------------- #

def test_c1_script_hat_dirs_match_the_owner_criterion():
    owner_text = HAT_OWNER_DOC.read_text(encoding="utf-8")
    for name in OWNER_HAT_DIRS:
        assert name in owner_text, (
            f"the hat owner criterion MUST name {name!r} (dogfooding-definitions § 2.1)"
        )
    script = REVIEW_SCRIPT.read_text(encoding="utf-8")
    match = re.search(r"FRAMEWORK_HAT_DIRS=\(([^)]*)\)", script)
    assert match, "the script must keep its explicit FRAMEWORK_HAT_DIRS list"
    script_dirs = tuple(match.group(1).split())
    assert script_dirs == OWNER_HAT_DIRS, (
        f"the capture step's hat dirs MUST be exactly the owner's five "
        f"(C-1 — no second, relaxed, or extended criterion); got {script_dirs!r}"
    )


@pytest.mark.parametrize("hat", ["client", "framework"])
def test_c1_feedback_directory_does_not_participate_in_the_hat_judgement(hat):
    """C-1: a root-level `feedback/` directory never moves the verdict."""
    factory = make_client_project if hat == "client" else make_framework_hat_twin
    with factory() as project:
        (project.path / "feedback").mkdir(exist_ok=True)
        assert project.hat == hat
        qualified_run(project)
        run = armed_capture(project, "--unit", UNIT)
        assert run.returncode == 0, run.describe()
        lines = capture_lines(run.stdout)
        assert len(lines) == 1, lines
        if hat == "client":
            assert "hat=framework" not in lines[0], (
                "feedback/ MUST NOT flip the verdict to framework (C-1)"
            )
        else:
            assert "hat=framework" in lines[0], (
                "feedback/ MUST NOT flip the verdict to client (C-1)"
            )
            for token in ARMED_TOKENS:
                assert token not in lines[0], (
                    "the hat-refusal line MUST NOT take an armed-state token form"
                )


# --------------------------------------------------------------------------- #
# C-2 — three-valued closed set, resolution order, resolved once per run
# --------------------------------------------------------------------------- #

def test_c2_armed_state_closed_set_literals_in_the_single_resolver():
    script = REVIEW_SCRIPT.read_text(encoding="utf-8")
    tokens = set(re.findall(r"client-(?:channel|unit)-[a-z]+", script))
    assert tokens == ARMED_TOKENS, (
        f"the resolver MUST disclose exactly the closed three-value armed-state "
        f"set {sorted(ARMED_TOKENS)}; found {sorted(tokens)}"
    )
    # C-2 "resolved once per run and reused": the probe facts are read through
    # exactly one call site of the machine-readable probe output.
    assert script.count('probe_facts "$root"') == 1, (
        "the armed state MUST be resolved once per run (single probe_facts call site)"
    )


def test_c2_resolution_order_explicit_unit_beats_probe_multiplicity():
    """Explicit unit first: it disambiguates (C-2) and only needs its own probe."""
    with make_client_project() as project:
        project.arm(UNIT)
        project.arm(OTHER_UNIT)          # two probes — ambiguous without a unit
        qualified_run(project)
        run = armed_capture(project, "--unit", UNIT)
        assert run.returncode == 0, run.describe()
        line = capture_lines(run.stdout)[0]
        assert "client-channel-armed" in line, line
        assert f"unit={UNIT}" in line and f"unit={OTHER_UNIT}" not in line, line
        assert "unit_source=explicit" in line, (
            "an explicit unit MUST be reported as the resolution source (C-2 order)"
        )
        assert external_count(project) == 1


def test_c2_unique_external_probe_auto_hits_without_a_unit():
    with make_client_project() as project:
        project.arm(UNIT)
        qualified_run(project)
        run = armed_capture(project)
        assert run.returncode == 0, run.describe()
        line = capture_lines(run.stdout)[0]
        assert "client-channel-armed" in line, line
        assert f"unit={UNIT}" in line, line
        assert "unit_source=auto:unique-external-probe" in line, (
            "the unique external probe MUST be reported as the resolution source"
        )
        assert external_count(project) == 1


# --------------------------------------------------------------------------- #
# C-3 — a specified unit with no probe object is unarmed, guided to probe-inject
# --------------------------------------------------------------------------- #

def test_c3_explicit_unit_without_probe_is_unarmed_with_probe_inject_guidance():
    with make_client_project() as project:
        qualified_run(project)          # no probe injected at all
        run = armed_capture(project, "--unit", UNIT)
        assert run.returncode == 0, run.describe()
        assert external_count(project) == 0, (
            "an explicit unit without a probe object MUST gain zero entries (C-3)"
        )
        line = capture_lines(run.stdout)[0]
        assert "client-channel-unarmed" in line, line
        assert UNIT in line, "the disclosure MUST name the specified unit (C-3)"
        assert "probe-inject" in line and UNIT in line, (
            "the one-time guidance MUST name probe injection for that unit (C-3)"
        )


# --------------------------------------------------------------------------- #
# C-4 — registry unavailable: unarmed, no record call at all, no legacy entry
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("with_unit", [True, False])
def test_c4_registry_unavailable_is_unarmed_never_records_no_legacy_entry(with_unit):
    with make_client_project() as project:
        project.arm(UNIT)               # armed first, then the runtime degrades
        qualified_run(project)
        project.break_probe_registry()  # un-upgraded .specify/ runtime
        extra = ("--unit", UNIT) if with_unit else ()
        run = armed_capture(project, *extra)
        assert run.returncode == 0, run.describe()
        assert external_count(project) == 0
        assert total_entries(project) == 0, (
            "C-4: the capture step MUST NOT call the record action at all — a "
            "legacy entry without kind/slice would route as a framework entry "
            "(a silent leak path)"
        )
        line = capture_lines(run.stdout)[0]
        assert "client-channel-unarmed" in line, line
        assert ".specify" in line and ("re-initialize" in line or "upgrade" in line), (
            "the one-time guidance MUST point at re-initializing/upgrading "
            f".specify/ (C-4); got: {line}"
        )


# --------------------------------------------------------------------------- #
# C-5 — multiple probes without a unit: ambiguous, never guessed
# --------------------------------------------------------------------------- #

def test_c5_multiple_probes_without_unit_is_ambiguous_and_never_guessed():
    with make_client_project() as project:
        project.arm(UNIT)
        project.arm(OTHER_UNIT)
        qualified_run(project)
        for _ in range(2):              # repeated runs: no rotation, no MRU
            run = armed_capture(project)
            assert run.returncode == 0, run.describe()
            assert external_count(project) == 0, (
                "an ambiguous state MUST gain zero entries (C-5)"
            )
            line = capture_lines(run.stdout)[0]
            assert "client-unit-ambiguous" in line, line
            assert UNIT not in line and OTHER_UNIT not in line, (
                "the ambiguous disclosure MUST NOT name, guess, rotate or pick "
                "a most-recently-used unit (C-5)"
            )
            assert "no guessing" in line or "--unit" in line, (
                "the disclosure MUST name the resolution path (an explicit unit)"
            )


# --------------------------------------------------------------------------- #
# C-6 — `--client-unit` literal, closed grammar, malformed value = named skip
# --------------------------------------------------------------------------- #

def test_c6_template_carries_the_client_unit_literal_and_grammar():
    text = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    assert "--client-unit" in text, (
        "the review command template MUST name the parameter literally `--client-unit` (C-6)"
    )
    assert UNIT_GRAMMAR_LITERAL in text, (
        f"the review command template MUST close the value grammar at {UNIT_GRAMMAR_LITERAL!r} (C-6)"
    )


@pytest.mark.parametrize("bad_value", [
    "banana",
    "custom:owner",          # no slash
    "custom:/name",          # empty owner
    "custom:owner/",         # empty name
])
def test_c6_malformed_unit_value_yields_named_skip_line(bad_value):
    with make_client_project() as project:
        project.arm(UNIT)
        qualified_run(project)
        run = armed_capture(project, "--unit", bad_value)
        assert run.returncode == 0, (
            f"a malformed --unit value MUST NOT block the review run (C-6); {run.describe()}"
        )
        assert external_count(project) == 0, (
            "a malformed --unit value MUST write zero entries (C-6)"
        )
        lines = capture_lines(run.stdout)
        assert len(lines) == 1, lines
        line = lines[0]
        assert "skipped" in line, line
        assert UNIT_GRAMMAR_LITERAL in line, (
            f"the skip line MUST name the expected grammar {UNIT_GRAMMAR_LITERAL!r} (C-6)"
        )
        assert bad_value in line, "the skip line MUST name the rejected value (C-6)"
        for token in ARMED_TOKENS:
            assert token not in line, (
                f"a skip line is not an armed-state disclosure; found {token!r}"
            )


# --------------------------------------------------------------------------- #
# C-7 — `/speckit.*` and `skill:` unit families are rejected for client findings
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("rejected", ["/speckit.review", "skill:code-review"])
def test_c7_framework_unit_families_never_reach_the_client_channel(rejected):
    """C-7: in a client project these either match no probe object or resolve as
    framework-internal units (routed upstream) — so the capture step rejects
    them at the grammar gate with a named skip line, zero entries."""
    with make_client_project() as project:
        qualified_run(project)
        run = armed_capture(project, "--unit", rejected)
        assert run.returncode == 0, run.describe()
        assert external_count(project) == 0
        assert total_entries(project) == 0, (
            "a framework-family unit MUST never be recorded as a client finding (C-7)"
        )
        line = capture_lines(run.stdout)[0]
        assert "skipped" in line and UNIT_GRAMMAR_LITERAL in line, line


# --------------------------------------------------------------------------- #
# C-8 — entry scope: three existing fields + the run, no fourth scope field
# --------------------------------------------------------------------------- #

def test_c8_entry_scope_is_the_three_existing_fields_plus_run():
    with make_client_project() as project:
        project.arm(UNIT)
        qualified_run(project)
        run = armed_capture(project, "--unit", UNIT)
        assert run.returncode == 0, run.describe()
        body = entry_file(project).read_text(encoding="utf-8")
        frontmatter = body.split("---", 2)[1]
        fields = {}
        for line in frontmatter.strip().splitlines():
            key, _, raw = line.partition(":")
            fields[key] = json.loads(raw.strip())
        assert fields["unit_id"] == UNIT, fields
        assert fields["unit_type"] == "custom-unit", fields
        assert fields["kind"] == "external", (
            "the entry's scope kind MUST be `external` (C-8)"
        )
        assert fields["slice"] == "host-custom", (
            "the entry's scope slice MUST be `host-custom` (C-8)"
        )
        assert fields["run_id"] == RUN_ID, fields
        assert set(fields) <= ENTRY_KEY_SET, (
            f"no fourth scope field and no new id family may appear (C-8); "
            f"unexpected keys: {sorted(set(fields) - ENTRY_KEY_SET)}"
        )


# --------------------------------------------------------------------------- #
# C-9 — armed state resolved from the probe engine's machine-readable output;
#       the probe registry itself is never modified by this feature
# --------------------------------------------------------------------------- #

def test_c9_resolution_matches_probe_engine_output_and_registry_untouched():
    with make_client_project() as project:
        project.arm(UNIT)
        qualified_run(project)
        defs = project.path / ".specify" / "shared" / "definitions" / "probe-definitions.md"
        before = hashlib.sha256(defs.read_bytes()).hexdigest()
        # The machine-readable fact the resolver must agree with (C-9).
        assert project.external_probe_units() == [UNIT]
        run = armed_capture(project)
        assert run.returncode == 0, run.describe()
        line = capture_lines(run.stdout)[0]
        assert "client-channel-armed" in line and f"unit={UNIT}" in line, line
        after = hashlib.sha256(defs.read_bytes()).hexdigest()
        assert before == after, (
            "capture MUST NOT modify the probe registry (C-9) — the registry "
            "truth source is read-only for this feature"
        )
    # Framework-side registry face: no Feature 072 additions to the truth source.
    registry_text = PROBE_DEFS.read_text(encoding="utf-8")
    assert "client-channel" not in registry_text and "capture" not in registry_text, (
        "the probe registry truth source carries no capture/armed-state wording (C-9)"
    )


# --------------------------------------------------------------------------- #
# T012 — the review command's two doc surfaces stay aligned
# --------------------------------------------------------------------------- #

def test_t012_review_docs_and_template_aligned_on_capture():
    template = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    docs = DOCS_REVIEW.read_text(encoding="utf-8")
    for name, text in (("template", template), ("docs page", docs)):
        assert "--client-unit" in text, (
            f"the review command {name} MUST document the --client-unit parameter (T012/C-6)"
        )
        assert UNIT_GRAMMAR_LITERAL in text, (
            f"the review command {name} MUST close the grammar at {UNIT_GRAMMAR_LITERAL!r}"
        )
        assert "capture" in text, (
            f"the review command {name} MUST name the fifth capture step (T012/C-10)"
        )
        for token in (
            "client-channel-armed", "client-channel-unarmed",
            "client-unit-ambiguous", "no-capture-object", "counts-unavailable",
        ):
            assert token in text, (
                f"the review command {name} MUST carry the five-value disclosure "
                f"set incl. {token!r} (T012/C-22)"
            )
    assert "fifth" in docs, (
        "the docs page MUST describe client capture as the fifth step of the "
        "non-interactive path, aligned with the skill enumeration"
    )
