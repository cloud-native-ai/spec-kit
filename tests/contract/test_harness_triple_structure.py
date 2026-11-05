"""Contract tests for feature 084's declaration layer, shared read entry and judging engine.

**Subjects** (two new framework-source files plus one new data surface):

* ``scripts/python/harness-triple-check.py`` — the read-only judging engine
  (``contracts/harness-triple-check.contract.md`` C-026…C-041).
* ``scripts/python/declaration_reader.py`` — the one YAML-subset parser
  (``contracts/shared-reader.contract.md`` C-052…C-059, whose boundary guard C-058 is a leg here).
* ``shared/declarations/`` — the yaml layer (``contracts/declaration-schema.contract.md`` C-001…C-012).

**Why every leg runs the engine as a subprocess**: the calling surface is
``python3 scripts/python/harness-triple-check.py`` and nothing less. A test that imported the module and
called its functions would prove the functions, not the surface a consumer uses — the same reason
``tests/contract/test_closure_acceptance_check.py`` runs its checker rather than its internals (GW-04).

**The six reason templates are read from the declaring specification, never re-spelled here.**
``REQUIREMENTS`` § Shared Strings owns the literal text and the placeholder grammar; this module renders
the expected instance by substituting arguments into the template it read, so an engine that produced a
"close enough" string fails while a template edit upstream would move both sides together.

**Fixture trees** (``tests/fixtures/harness-triple-structure/``, one directory per feature). Each tree is
a miniature repository: carriers under the three screen surfaces, engines under ``scripts/python/`` or
``<skill>/scripts/``, and the declaration layer under ``shared/declarations/``. One file is deliberately
**not** stored in the fixtures: ``shared/declarations/contract.yaml`` is copied in from the framework
source at test time, because the value domains have exactly one owner
(``contracts/declaration-schema.contract.md`` C-002) and a per-fixture copy would be a second one.

=================  ============================================================================
fixture            proves
=================  ============================================================================
``positive``       every candidate is declared or excluded ⇒ ``coverage`` exit 0, zero findings;
                   ``verify`` exit 0; ``lookup`` answers for both selectors
``negative-…``     one tree per reason template (six), each asserting exit 1 + the verbatim instance
``dual-writer``    two branches, one added fact file each ⇒ two distinct paths, both trees exit 0,
                   and an appended exclusion row never reorders the rows already there
``legacy-project`` no declaration layer at all ⇒ exit 2 with an explicit label naming the missing
                   directory, no traceback, never 0
``screen-boundary`` a carrier that only mentions a script path in prose enters the candidate set and is
                   retired by one exclusion record, not by a second "does it really call it" test
=================  ============================================================================

**Red-first** (T005): this module was authored before the engine and the reader existed. The red run is
recorded in ``notes/red-first-evidence.md``; ``GATE-1`` in ``tasks.md`` is the row it binds.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "harness-triple-check.py"
READER = ROOT / "scripts" / "python" / "declaration_reader.py"
CONTRACT = ROOT / "shared" / "declarations" / "contract.yaml"
FIXTURES = ROOT / "tests" / "fixtures" / "harness-triple-structure"
SPEC = ROOT / ".specify" / "specs" / "084-harness-triple-structure"
REQUIREMENTS = SPEC / "requirements.md"

#: The closed six, ids only — the text lives in `requirements.md` § Shared Strings.
REASON_IDS = ("STR-009", "STR-010", "STR-011", "STR-012", "STR-013", "STR-014")

SHARED_STRING_ROW = re.compile(r"^\|\s*`(STR-\d{3})`\s*\|\s*`(.+?)`\s*\|", re.M)
PLACEHOLDER = re.compile(r"<[^<>]+>")


def shared_strings() -> dict:
    """`{STR-NNN: template}` read from the specification that owns the literals."""
    text = REQUIREMENTS.read_text(encoding="utf-8")
    table = text.split("## Shared Strings", 1)[1]
    rows = dict(SHARED_STRING_ROW.findall(table))
    missing = [rid for rid in REASON_IDS if rid not in rows]
    assert not missing, "requirements.md § Shared Strings lost templates: %s" % missing
    return rows


def instance(rid: str, *args) -> str:
    """Substitute arguments into a template, in placeholder order (the grammar is the table's)."""
    template = shared_strings()[rid]
    parts = PLACEHOLDER.split(template)
    gaps = PLACEHOLDER.findall(template)
    assert len(gaps) == len(args), "%s takes %d placeholder(s), got %d" % (
        rid, len(gaps), len(args))
    out = parts[0]
    for arg, tail in zip(args, parts[1:]):
        out += arg + tail
    return out


def make_tree(tmp_path: Path, name: str) -> Path:
    """Copy one fixture tree into `tmp_path` and drop the shipped `contract.yaml` into it."""
    src = FIXTURES / name
    assert src.is_dir(), "missing fixture tree: %s" % src
    dst = tmp_path / name.replace("/", "-")
    shutil.copytree(src, dst)
    declarations = dst / "shared" / "declarations"
    if declarations.is_dir():
        shutil.copyfile(CONTRACT, declarations / "contract.yaml")
    return dst


def run(repo: Path, *args, cwd: Path | None = None):
    """Run the engine as a consumer does; returns (exit code, stdout, stderr)."""
    proc = subprocess.run(
        [sys.executable, str(ENGINE), *args, "--repo", str(repo)],
        capture_output=True, text=True, cwd=str(cwd or ROOT),
    )
    return proc.returncode, proc.stdout, proc.stderr


def field(stdout: str, key: str) -> list[str]:
    """Every value of one flat `key: value` line, in order."""
    pattern = re.compile(r"^%s:\s?(.*)$" % re.escape(key), re.M)
    return [match.group(1).strip() for match in pattern.finditer(stdout)]


def unit_blocks(stdout: str) -> dict:
    """`{unit path: {field: [values]}}` from the `unit: <path>` blocks ``coverage`` prints."""
    blocks: dict[str, dict[str, list[str]]] = {}
    current = None
    for line in stdout.splitlines():
        if line.startswith("unit: "):
            current = blocks.setdefault(line[len("unit: "):].strip(), {})
            continue
        if current is None or ":" not in line:
            continue
        key, value = line.split(":", 1)
        current.setdefault(key.strip(), []).append(value.strip())
    return blocks


def first(block: dict, key: str) -> str:
    values = block.get(key) or [""]
    return values[0]


def overlay(dst: Path, name: str) -> None:
    """Merge one ``dual-writer`` branch directory (what a branch *adds*) onto an existing tree."""
    src = FIXTURES / name
    assert src.is_dir(), "missing overlay directory: %s" % src
    for path in src.rglob("*"):
        if path.is_dir():
            continue
        target = dst / path.relative_to(src)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)


# --------------------------------------------------------------------------- #
# the positive tree: exit 0, zero findings, both actions, both lookups
# --------------------------------------------------------------------------- #
def test_positive_tree_reads_clean(tmp_path):
    tree = make_tree(tmp_path, "positive")
    rc, out, err = run(tree, "--action", "coverage")
    assert rc == 0, out + err
    assert field(out, "findings") == ["0"], out

    blocks = unit_blocks(out)
    assert sorted(blocks) == [
        "shared/workflow/feedback-step.md",
        "skills/external/draw-diagram/SKILL.md",
    ], out

    migrated = blocks["shared/workflow/feedback-step.md"]
    assert first(migrated, "disposition") == "in-scope"
    assert first(migrated, "state") == shared_strings()["STR-004"], out
    assert migrated["fact"] == ["feedback-prompt-threshold"], out

    retired = blocks["skills/external/draw-diagram/SKILL.md"]
    assert first(retired, "disposition") == "excluded"
    assert first(retired, "reason") == shared_strings()["STR-007"], out


def test_verify_is_clean_on_the_positive_tree(tmp_path):
    tree = make_tree(tmp_path, "positive")
    rc, out, err = run(tree, "--action", "verify")
    assert rc == 0, out + err
    assert field(out, "findings") == ["0"], out
    assert field(out, "declarations") == ["1"], out

    # Anti-vacuous sentinel: both consistency directions were counted over a non-empty surface,
    # so "zero findings" cannot be the silence of a check that never looked at anything.
    forward = field(out, "consistency-declarations-to-carriers")[0]
    backward = field(out, "consistency-carriers-to-declarations")[0]
    for reading in (forward, backward):
        matched, total = reading.split("/")
        assert int(total) > 0 and matched == total, reading


def test_coverage_is_deterministic(tmp_path):
    tree = make_tree(tmp_path, "positive")
    first_run = run(tree, "--action", "coverage")
    second_run = run(tree, "--action", "coverage")
    assert first_run[0] == second_run[0] == 0
    assert first_run[1] == second_run[1], "two consecutive coverage runs must be byte-identical"


def test_lookup_answers_both_selectors(tmp_path):
    tree = make_tree(tmp_path, "positive")
    rc, out, err = run(tree, "--action", "lookup", "--unit-id", "shared/workflow/feedback-step.md")
    assert rc == 0, out + err
    assert field(out, "disposition") == ["in-scope"], out
    assert "feedback-prompt-threshold" in out

    rc, out, err = run(tree, "--action", "lookup", "--fact", "feedback-prompt-threshold")
    assert rc == 0, out + err
    assert field(out, "fact") == ["feedback-prompt-threshold"], out
    assert field(out, "kind") == ["threshold"], out

    report = tmp_path / "report.json"
    rc, _, err = run(tree, "--action", "verify", "--json-out", str(report))
    assert rc == 0, err
    assert json.loads(report.read_text(encoding="utf-8"))["action"] == "verify"


# --------------------------------------------------------------------------- #
# the six reasons, each verbatim, each with exit 1
# --------------------------------------------------------------------------- #
#: (reason id, fixture tree, action, extra argv, arguments substituted into the template)
#: `STR-010` lives in `negative-declaration-outside-subset/` — that tree *is* the subset-violation
#: fixture; a second directory for the same defect would be a second copy of one assertion.
REASON_CASES = (
    ("STR-009", "negative-third-layer-missing", "verify", (),
     ("shared/workflow/feedback-step.md",)),
    ("STR-010", "negative-declaration-outside-subset", "verify", (),
     ("shared/declarations/facts/feedback-prompt-threshold.yaml",)),
    ("STR-011", "negative-duplicated-fact-literal", "verify", (),
     ("feedback-prompt-threshold",
      "shared/declarations/facts/feedback-prompt-threshold-copy.yaml")),
    ("STR-012", "negative-exclusion-anchor-unresolvable", "verify", (),
     ("skills/internal/humanize/SKILL.md",)),
    ("STR-013", "negative-unclassified-candidate", "coverage", (),
     ("shared/workflow/gate-roster.md",)),
    ("STR-014", "negative-declaration-absent", "lookup",
     ("--fact", "feedback-prompt-threshold"), ("feedback-prompt-threshold",)),
)


@pytest.mark.parametrize(
    "reason, fixture, action, extra_argv, args",
    REASON_CASES,
    ids=[case[0] for case in REASON_CASES],
)
def test_each_reason_is_emitted_verbatim(tmp_path, reason, fixture, action, extra_argv, args):
    tree = make_tree(tmp_path, fixture)
    rc, out, err = run(tree, "--action", action, *extra_argv)
    expected = instance(reason, *args)
    assert rc == 1, "a finding exits 1 (%s)\n%s%s" % (reason, out, err)
    assert expected in out.splitlines() or ("finding: " + expected) in out, (
        "expected the verbatim instance %r in:\n%s" % (expected, out))


def test_every_reason_has_a_negative_fixture_and_every_action_a_positive_one():
    covered = {case[0] for case in REASON_CASES}
    assert covered == set(REASON_IDS), "a reason without a fixture is not a finding (C-041)"
    actions = {case[2] for case in REASON_CASES} | {"coverage", "verify", "lookup"}
    assert actions == {"coverage", "verify", "lookup"}


def test_exit_codes_are_closed_at_zero_one_and_two(tmp_path):
    tree = make_tree(tmp_path, "positive")
    assert run(tree, "--action", "coverage")[0] == 0
    assert run(tree, "--action", "bogus")[0] == 2, "an unknown action is an input error"
    assert run(tree, "--action", "lookup")[0] == 2, "neither selector is an input error"
    assert run(tree, "--action", "lookup", "--unit-id", "x", "--fact", "y")[0] == 2, (
        "both selectors is an input error")

    dirty = make_tree(tmp_path, "negative-unclassified-candidate")
    assert run(dirty, "--action", "coverage")[0] == 1


def test_subset_violation_is_rejected_rather_than_patched(tmp_path):
    tree = make_tree(tmp_path, "negative-declaration-outside-subset")
    rc, out, err = run(tree, "--action", "verify")
    assert rc == 1, out + err
    assert instance("STR-010", "shared/declarations/facts/feedback-prompt-threshold.yaml") in out
    # No best-effort parse: the flow sequence's members never surface as a read value.
    for member in ("first-member", "second-member"):
        assert member not in out, "a construct outside the subset was parsed anyway: %r\n%s" % (
            member, out)


# --------------------------------------------------------------------------- #
# coverage's three-state readings; a pending unit is a reading, not a failure
# --------------------------------------------------------------------------- #
def test_coverage_reads_three_states_without_turning_red(tmp_path):
    complete_tree = make_tree(tmp_path, "positive")
    rc, out, err = run(complete_tree, "--action", "coverage")
    assert rc == 0, out + err
    assert first(unit_blocks(out)["shared/workflow/feedback-step.md"], "state") == \
        shared_strings()["STR-004"]

    pending_tree = make_tree(tmp_path, "negative-third-layer-missing")
    rc, out, err = run(pending_tree, "--action", "coverage")
    assert rc == 0, "a pending unit must not turn coverage red (C-043)\n" + out + err
    block = unit_blocks(out)["shared/workflow/feedback-step.md"]
    assert first(block, "disposition") == "in-scope"
    assert first(block, "state") == shared_strings()["STR-005"], out
    # The pending reason names the missing layer, from the template read out of the spec, not re-spelled.
    assert first(block, "reason") == shared_strings()["STR-009"].split(":")[0], out

    unclassified_tree = make_tree(tmp_path, "negative-unclassified-candidate")
    rc, out, err = run(unclassified_tree, "--action", "coverage")
    assert rc == 1, out + err
    assert first(unit_blocks(out)["shared/workflow/gate-roster.md"], "disposition") == "unclassified"


def test_a_unit_named_by_a_declaration_and_a_row_is_a_finding(tmp_path):
    tree = make_tree(tmp_path, "positive")
    (tree / "shared" / "declarations" / "exclusions" / "no-machine-fact.yaml").write_text(
        "- unit: shared/workflow/feedback-step.md\n"
        "  carrier: scripts/python/feedback-utils.py\n"
        "  anchor: shared/workflow/feedback-step.md#Feedback step\n",
        encoding="utf-8",
    )
    rc, out, err = run(tree, "--action", "coverage")
    assert rc == 1, "one unit, two dispositions, must never resolve by file order\n" + out + err
    assert instance("STR-013", "shared/workflow/feedback-step.md") in out, out


def test_a_fact_declared_twice_keeps_its_unit_pending(tmp_path):
    """E-6 (a) / R-6: "exactly one declaration" is a verdict from the run, not a file's existence.

    The reading was red against the engine as first written: one fact, two declarations, and the unit
    still printed ``state: complete`` — a declaration file existing was taken as evidence for (a), which
    is the false green E-6 R-6 forbids. The finding beside it (``STR-011``) never repaired that.
    """
    tree = make_tree(tmp_path, "negative-duplicated-fact-literal")
    rc, out, err = run(tree, "--action", "coverage")
    assert rc == 1, out + err
    block = unit_blocks(out)["shared/workflow/feedback-step.md"]
    assert first(block, "disposition") == "in-scope", out
    assert first(block, "state") == shared_strings()["STR-005"], (
        "one fact claimed by two declarations fails (a), so the unit is never `complete`\n" + out)
    assert first(block, "reason") == shared_strings()["STR-011"].split(":")[0], out


# --------------------------------------------------------------------------- #
# the dual-writer property: two branches, two paths, both green
# --------------------------------------------------------------------------- #
def test_dual_writer_fact_files_land_on_distinct_paths(tmp_path):
    base = make_tree(tmp_path, "positive")
    branch_a = tmp_path / "branch-a"
    branch_b = tmp_path / "branch-b"
    shutil.copytree(base, branch_a)
    shutil.copytree(base, branch_b)
    overlay(branch_a, "dual-writer/branch-a")
    overlay(branch_b, "dual-writer/branch-b")

    added_a = {p.relative_to(branch_a) for p in branch_a.rglob("*.yaml")
               if not (base / p.relative_to(branch_a)).exists()}
    added_b = {p.relative_to(branch_b) for p in branch_b.rglob("*.yaml")
               if not (base / p.relative_to(branch_b)).exists()}

    assert len(added_a) == 1 and len(added_b) == 1, (added_a, added_b)
    assert added_a.isdisjoint(added_b), (
        "two branches adding one fact file each must not write the same path: %s vs %s"
        % (added_a, added_b))

    for tree in (branch_a, branch_b):
        rc, out, err = run(tree, "--action", "coverage")
        assert rc == 0, "%s must exit 0 after the merge\n%s%s" % (tree.name, out, err)


def test_an_appended_exclusion_row_never_reorders_the_existing_rows(tmp_path):
    tree = make_tree(tmp_path, "positive")

    def add_unit(skill: str, line: str) -> None:
        carrier = tree / "skills" / "external" / skill / "SKILL.md"
        carrier.parent.mkdir(parents=True, exist_ok=True)
        carrier.write_text("# %s\n\nCalls `skills/external/%s/scripts/run.py`.\n" % (skill, skill),
                           encoding="utf-8")
        script = tree / "skills" / "external" / skill / "scripts" / "run.py"
        script.parent.mkdir(parents=True, exist_ok=True)
        script.write_text("def run():\n    return 0\n", encoding="utf-8")
        with exclusions.open("a", encoding="utf-8") as handle:
            handle.write(line)

    exclusions = tree / "shared" / "declarations" / "exclusions" / "no-machine-fact.yaml"
    add_unit("alpha-tool", "- unit: skills/external/alpha-tool/SKILL.md\n"
                           "  carrier: skills/external/alpha-tool/scripts/run.py\n"
                           "  anchor: skills/external/alpha-tool/SKILL.md#alpha-tool\n")
    before = exclusions.read_text(encoding="utf-8").splitlines()
    assert run(tree, "--action", "coverage")[0] == 0

    # A second unit arrives on a second branch: one appended row, never a reordering of the first.
    add_unit("beta-tool", "- unit: skills/external/beta-tool/SKILL.md\n"
                          "  carrier: skills/external/beta-tool/scripts/run.py\n"
                          "  anchor: skills/external/beta-tool/SKILL.md#beta-tool\n")
    after = exclusions.read_text(encoding="utf-8").splitlines()
    assert after[:len(before)] == before, "the rows already in the file were reordered"
    rc, out, err = run(tree, "--action", "coverage")
    assert rc == 0, out + err


# --------------------------------------------------------------------------- #
# legacy project: explicit degradation, never a pass, never a traceback
# --------------------------------------------------------------------------- #
def test_a_legacy_project_degrades_to_exit_2(tmp_path):
    tree = make_tree(tmp_path, "legacy-project")
    rc, out, err = run(tree, "--action", "coverage")
    combined = out + err
    assert rc == 2, "a project without the declaration layer is an input error\n" + combined
    assert shared_strings()["STR-002"] in combined, (
        "the label must name the missing directory %r\n%s"
        % (shared_strings()["STR-002"], combined))
    assert "Traceback" not in combined, combined
    assert field(out, "findings") == [], "degradation is not a finding, and never a pass"


def test_the_boundary_unit_is_a_candidate_and_is_retired_by_its_row(tmp_path):
    tree = make_tree(tmp_path, "screen-boundary")
    unit = "skills/internal/summarize-project/SKILL.md"
    rc, out, err = run(tree, "--action", "coverage")
    assert rc == 0, out + err
    assert first(unit_blocks(out)[unit], "disposition") == "excluded", out
    assert first(unit_blocks(out)[unit], "reason") == shared_strings()["STR-006"], out

    # Remove the row: the same text still enters the candidate set, and now nothing retires it.
    (tree / "shared" / "declarations" / "exclusions" / "no-machine-fact.yaml").unlink()
    rc, out, err = run(tree, "--action", "coverage")
    assert rc == 1, out + err
    assert first(unit_blocks(out)[unit], "disposition") == "unclassified", out


# --------------------------------------------------------------------------- #
# read-only (C-039) and the single-parser boundary (C-058 / FR-019)
# --------------------------------------------------------------------------- #
def test_a_run_leaves_the_judged_tree_byte_identical():
    def porcelain() -> str:
        return subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain"],
                              capture_output=True, text=True).stdout

    before = porcelain()
    rc, out, err = run(ROOT, "--action", "coverage")
    assert rc in (0, 1), "the repository tree itself must be judgeable\n" + out + err
    assert porcelain() == before, "a run wrote into the tree it judged"


#: The two grandfathered parsers and why they are grandfathered. The reason strings carry the owner's
#: label (`requirements.md` § Non-Goals N4), so the allowlist cannot quietly grow a third entry.
SHARED_READ_ENTRY = "scripts/python/declaration_reader.py"
GRANDFATHERED = {
    "scripts/python/execution-config.py":
        "N4 — grandfathered inline subset parser, registered and not touched by this feature",
    "scripts/python/gate-check.py":
        "N4 — grandfathered line-level gate parser, registered and not touched by this feature",
}

PARSER_SHAPED = re.compile(r"^\s*def (parse_yaml_subset|parse_gate|parse_subset)\b", re.M)


def test_the_shared_read_entry_is_the_only_subset_parser():
    found = set()
    for base in ("scripts", "skills"):
        for path in sorted((ROOT / base).rglob("*.py")):
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            if PARSER_SHAPED.search(text):
                found.add(path.relative_to(ROOT).as_posix())

    # Anti-vacuous sentinel: the detector must see the shared read entry, or the assertion below
    # would mean "the search is blind", not "there is one parser".
    assert SHARED_READ_ENTRY in found, (
        "the boundary detector did not see the shared read entry; it is searching for the wrong shape")
    assert found == {SHARED_READ_ENTRY} | set(GRANDFATHERED), (
        "a second subset parser appeared: %s"
        % sorted(found - {SHARED_READ_ENTRY} - set(GRANDFATHERED)))
    for path, reason in GRANDFATHERED.items():
        assert "N4" in reason, "%s is allowlisted without its N4 reason" % path


# --------------------------------------------------------------------------- #
# migration legs (T008–T014): one declaration, one read point, one pointer
# --------------------------------------------------------------------------- #
#: The facts T008–T014 migrate, each with the three things C-047's steps 3–5 leave behind: an engine
#: that holds a locatable read point and no longer declares the value itself, carriers that point at the
#: declaration, and one declaration file. The rows are the *reading*, not a second roster: the roster is
#: `contracts/migration-batches.contract.md` C-042 / C-044, and this table quotes the slugs it names.
#:
#: `inline` holds the source patterns that MUST be gone once the fact is declared. They are the engine
#: side's former shape, so a re-introduced copy fails here instead of drifting silently (C-048 (c)).
MIGRATED = {
    "feedback-prompt-threshold": {
        "kind": "threshold",
        "engines": ["scripts/python/feedback-utils.py"],
        "carriers": ["shared/workflow/feedback-step.md"],
        "inline": [r"^DEFAULT_THRESHOLD\s*="],
    },
    "evidence-seven-states": {
        "kind": "closed-set",
        "engines": ["scripts/python/evidence-utils.py"],
        "carriers": ["skills/internal/collect-evidence/references/evidence-discipline.md",
                     "shared/guidelines/better-harness.md"],
        "inline": [r"^SEVEN_STATES\s*="],
    },
    "evidence-lanes": {
        "kind": "closed-set",
        "engines": ["scripts/python/evidence-utils.py"],
        "carriers": ["shared/workflow/evidence-step.md",
                     "skills/internal/collect-evidence/SKILL.md"],
        "inline": [r"^LANE_NAMES\s*="],
    },
    "flow-class-classes": {
        "kind": "closed-set",
        "engines": ["scripts/python/flow-class-check.py"],
        "carriers": ["shared/definitions/flow-class-definitions.md"],
        "inline": [r"^CLASS_VALUES\s*="],
    },
    "flow-class-basis": {
        "kind": "closed-set",
        "engines": ["scripts/python/flow-class-check.py"],
        "carriers": ["shared/definitions/flow-class-definitions.md"],
        "inline": [r"^BASIS_VALUES\s*="],
    },
    "flow-class-document-types": {
        "kind": "closed-set",
        "engines": ["scripts/python/flow-class-check.py"],
        "carriers": ["shared/definitions/flow-class-definitions.md"],
        "inline": [r"^FLOW_TYPE_VALUES\s*="],
    },
    "flow-class-ledger-columns": {
        "kind": "ordered-operator-table",
        "engines": ["scripts/python/flow-class-check.py"],
        "carriers": ["shared/definitions/flow-class-definitions.md"],
        "inline": [r"^REQUIRED_LEDGER_COLUMNS\s*="],
    },
    "flow-class-neutral-categories": {
        "kind": "closed-set",
        "engines": ["scripts/python/flow-class-check.py"],
        "carriers": ["shared/definitions/flow-class-definitions.md"],
        "inline": [r"^NEUTRAL_CATEGORIES\s*="],
    },
    "success-criterion-path-values": {
        "kind": "closed-set",
        "engines": ["scripts/python/validate-requirements.py",
                    "scripts/python/closure-acceptance-check.py"],
        "carriers": ["shared/workflow/acceptance-hardening.md",
                     "templates/commands/requirements.md",
                     "skills/internal/create-requirements/SKILL.md"],
        "inline": [r"^PATH_VALUES\s*=", r'^\s*if value not in \("final", "supporting"\)'],
    },
    "expression-gate-faces": {
        "kind": "mapping",
        "engines": ["scripts/python/flow-class-check.py"],
        "carriers": ["shared/workflow/expression-gates.md"],
        "inline": [r"^FACES_EXPECTED\s*="],
    },
    "expression-stage-operator-table": {
        "kind": "ordered-operator-table",
        "engines": ["scripts/python/flow-class-check.py"],
        "carriers": ["shared/workflow/expression-gates.md"],
        "inline": [r'^    required = \("阶段"'],
    },
    "driver-stage-sequence": {
        "kind": "ordered-operator-table",
        "engines": ["skills/external/sdd-loop-driver/scripts/loop-state.py"],
        "carriers": ["skills/external/sdd-loop-driver/SKILL.md"],
        "inline": [],
    },
    "driver-stage-artifacts": {
        "kind": "mapping",
        "engines": ["skills/external/sdd-loop-driver/scripts/loop-state.py"],
        "carriers": ["skills/external/sdd-loop-driver/references/dispatch-recipes.md"],
        "inline": [],
    },
    "driver-completion-sentinels": {
        "kind": "mapping",
        "engines": ["skills/external/sdd-loop-driver/scripts/loop-state.py"],
        "carriers": ["skills/external/sdd-loop-driver/SKILL.md"],
        "inline": [r'^    return "%s-DONE" % str\(stage\)\.upper\(\)'],
    },
    "driver-gate-roster": {
        "kind": "mapping",
        "engines": ["skills/external/sdd-loop-driver/scripts/pre-analyze-check.py"],
        "carriers": ["skills/external/sdd-loop-driver/references/dispatch-recipes.md"],
        "inline": [],
    },
}

#: The rows above this part has actually migrated: C-042 rows 1–8, closed by T008–T012. The roster's
#: remaining rows keep their shape in ``MIGRATED`` but are deliberately **not asserted yet** —
#: ``success-criterion-path-values`` is T013's, batch 2 is T014–T015's and batch 3 is T016's. C-046 (and
#: DoD-5 after it) makes each batch independently acceptable: "an unfinished batch k+1 MUST NOT be
#: reported as a failure of batch k". A leg parametrized over an un-migrated row would report exactly
#: that — a red id owned by a task that has not run — so the parametrization reads this tuple and each
#: later task appends its slugs as it closes them.
MIGRATED_SO_FAR = (
    "feedback-prompt-threshold",
    "evidence-seven-states",
    "evidence-lanes",
    "flow-class-classes",
    "flow-class-basis",
    "flow-class-document-types",
    "flow-class-ledger-columns",
    "flow-class-neutral-categories",
)


@pytest.mark.parametrize("slug", sorted(MIGRATED_SO_FAR))
def test_a_migrated_fact_has_one_declaration_with_the_required_keys(slug):
    """C-047 step 2 / C-003 / C-004 — one file, the slug as identity, the required keys present."""
    row = MIGRATED[slug]
    path = ROOT / "shared" / "declarations" / "facts" / (slug + ".yaml")
    assert path.is_file(), "no declaration for %s" % slug
    text = path.read_text(encoding="utf-8")
    assert re.search(r"^fact:\s*%s$" % re.escape(slug), text, re.M), (
        "%s: the `fact:` key must equal the file stem" % slug)
    assert re.search(r"^kind:\s*%s$" % re.escape(row["kind"]), text, re.M), (
        "%s: kind must be declared as %s" % (slug, row["kind"]))
    for key in ("statement", "consumers", "former_carriers"):
        assert re.search(r"^%s:" % key, text, re.M), "%s: missing required key %s" % (slug, key)


@pytest.mark.parametrize("slug", sorted(MIGRATED_SO_FAR))
def test_a_migrated_fact_keeps_a_locatable_read_point_and_drops_the_inline_copy(slug):
    """C-047 step 3 / C-048 (c) — the engine names the read entry and the slug; the constant is gone."""
    row = MIGRATED[slug]
    for engine in row["engines"]:
        text = (ROOT / engine).read_text(encoding="utf-8")
        assert "declaration_reader" in text, "%s does not read through the shared entry" % engine
        assert slug in text, "%s does not name the fact it reads (%s)" % (engine, slug)
        for pattern in row["inline"]:
            assert not re.search(pattern, text, re.M), (
                "%s still declares %s inline (%s)" % (engine, slug, pattern))


@pytest.mark.parametrize("slug", sorted(MIGRATED_SO_FAR))
def test_a_migrated_fact_carrier_points_at_the_declaration(slug):
    """C-047 step 4 — the carrier reaches the value by `<path>#/<key-path>`, it does not restate it."""
    row = MIGRATED[slug]
    pointer = "shared/declarations/facts/%s.yaml#/" % slug
    for carrier in row["carriers"]:
        text = (ROOT / carrier).read_text(encoding="utf-8")
        assert pointer in text, "%s carries no pointer to %s" % (carrier, slug)


def test_the_declaration_layer_parses_without_an_input_error():
    """The whole layer must stay schema- and subset-clean as rows land (C-004 / C-008).

    Exit 0 and 1 are both readings about *dispositions* (a tree with unmigrated units exits 1, C-043);
    exit 2 is the layer itself being unreadable, which no migration row may cause.
    """
    rc, out, err = run(ROOT, "--action", "coverage")
    assert rc in (0, 1), "the declaration layer is not readable\n%s\n%s" % (out, err)
    assert "input-error" not in err, err
