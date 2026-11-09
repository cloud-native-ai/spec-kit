"""Contract test: the measured 085 disposal table (FR-041, SC-010).

Tasks row T065. Three decidable claims:

1. **The table is complete and disposed.** Every row of `tasks.md` § 085 disposal table
   names an existing module, carries exactly one disposition from the closed set
   (`rewrite` / `remove` / `historical`) and a one-line reason (C-103).
2. **The list is re-measured, not inherited.** A programmatic scan of the test tree with
   the *specific* retired-surface predicate finds no module outside the table and outside
   this feature's own SC-map modules (whose vocabulary is their subject, per C-109) —
   a fourth 085-era module appearing later turns this red instead of being absorbed.
3. **The post-disposal reading is baseline-internal for the disposal's own surface.**
   The recorded contract-suite reading adds no new failing id for a module this feature
   authored or disposed; a new failure in one of the table modules must be attributed by
   name in the recorded attribution file (C-104's "never silently").

The full-tree NEW-vs-plan comparison is the closure gate's job (GATE-1); this module
pins the disposal's own causal surface and never re-runs the suite from inside pytest.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO_ROOT / ".specify/specs/094-goal-team-parallel"
TASKS = SPEC_DIR / "tasks.md"
BASELINE = SPEC_DIR / "test-evidence/plan-baseline-names.txt"
READING = SPEC_DIR / "test-evidence/wp05-contract-post-disposal.txt"
ATTRIBUTION = SPEC_DIR / "test-evidence/wp05-disposal-attribution.txt"

DISPOSITIONS = {"rewrite", "remove", "historical"}

#: The retired-surface predicate, narrower than the table's dated count grep: a bare
#: `temporary` (member lifecycle, the temp-directory discipline) and a bare `spec-local`
#: (skill-directory locality) are different axes and are not hits here.
RETIRED_SURFACE = re.compile(
    r"(?i)(?:spec-local\s+(?:goal|team)"
    r"|temp_goal|temp_team"
    r"|--scope\s+(?:spec|global)"
    r"|scope\s*[:=]\s*(?:spec|global)"
    r"|\.specify/specs/[^\s`'\"]*/(?:goal|team)/)"
)

#: Modules this feature authored (contracts/owner-rewrites-and-tests.md C-109 map, plus
#: the row-guard modules). Their vocabulary is the subject under test, never a residue.
#: Closed set: it grows only by revising this module.
FEATURE_MODULES = {
    "tests/contract/test_command_run_goal_team.py",
    "tests/contract/test_no_spec_local_writes.py",
    "tests/integration/test_archive_migration_real_data.py",
    "tests/contract/test_archive_migration.py",
    "tests/integration/test_parallel_lines.py",
    "tests/contract/test_handoff_contract.py",
    "tests/contract/test_handoff_territory.py",
    "tests/contract/test_criterion_vocabulary_scan.py",
    "tests/contract/test_binding_model.py",
    "tests/contract/test_085_disposal_table.py",
    "tests/contract/test_migration_interruption.py",
    "tests/contract/test_resident_backfill.py",
    "tests/contract/test_parallel_lines.py",
    "tests/contract/test_command_family.py",
    "tests/contract/test_declaration_facts.py",
    "tests/contract/test_sdd_loop_driver_skill.py",
    "tests/contract/test_framework_map_archive_row.py",
    "tests/contract/test_goal_command_template.py",
}

ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|\s*(\d+)\s*\|\s*([a-z]+)\s*\|\s*(.+?)\s*\|$")


def _table_rows() -> list[dict]:
    text = TASKS.read_text(encoding="utf-8")
    start = text.index("## 085 disposal table")
    tail = text[start:]
    end = tail.find("\n## ", 1)
    section = tail[: end if end != -1 else len(tail)]
    rows = []
    for line in section.splitlines():
        match = ROW.match(line)
        if match:
            index, module, count, disposition, reason = match.groups()
            rows.append({"index": int(index), "module": module,
                         "count": int(count), "disposition": disposition,
                         "reason": reason.strip()})
    return rows


def _measured_modules() -> set:
    found = set()
    for path in (REPO_ROOT / "tests").rglob("*.py"):
        text = path.read_text(encoding="utf-8", errors="replace")
        if RETIRED_SURFACE.search(text):
            found.add(path.relative_to(REPO_ROOT).as_posix())
    return found


def test_every_measured_module_has_exactly_one_disposition():
    rows = _table_rows()
    assert len(rows) == 12, f"the measured disposal table must carry 12 rows, got {len(rows)}"

    modules = [row["module"] for row in rows]
    assert len(set(modules)) == len(modules), f"a module carries two rows: {modules}"
    assert [row["index"] for row in rows] == list(range(1, 13)), "row ordinals must be 1..12"

    for row in rows:
        module = row["module"]
        assert (REPO_ROOT / module).is_file(), f"disposed module missing: {module}"
        assert row["disposition"] in DISPOSITIONS, (
            f"{module}: disposition {row['disposition']!r} outside the closed set")
        assert row["reason"], f"{module}: a disposition without its one-line reason is a defect"
        assert row["count"] > 0, f"{module}: the dated matching-line count must be positive"

    # Re-measurement: the table is the measured list, so a module with a live retired
    # surface is either table-owned or a module this feature authored. A fourth 085-era
    # module turns this red rather than being absorbed by the table.
    measured = _measured_modules()
    unowned = measured - set(modules) - FEATURE_MODULES
    assert not unowned, (
        "a module carries the retired spec-local/scope surface but appears in no "
        f"disposition row: {sorted(unowned)}")


def _reading_meta() -> dict:
    assert READING.is_file(), (
        f"the post-disposal contract reading is missing: {READING} (record it with "
        "scripts/bash/run-tests.sh tests/contract --names-out ...)")
    meta = {}
    for line in READING.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            key, _sep, value = line[2:].partition(": ")
            meta[key.strip().lower()] = value
    return meta


def _reading_failures() -> set:
    return {line.strip() for line in READING.read_text(encoding="utf-8").splitlines()
            if line.strip().startswith("tests/")}


def test_the_post_disposal_reading_is_baseline_internal_for_the_disposal_surface():
    meta = _reading_meta()
    assert "command" in meta, "the reading records the command line it came from"
    assert "exit status" in meta, "the reading records the exit status"
    assert BASELINE.is_file(), f"the frozen serial baseline is missing: {BASELINE}"
    baseline = {line.strip() for line in BASELINE.read_text(encoding="utf-8").splitlines()
                if line.strip()}

    new = _reading_failures() - baseline
    # The reading predates the evidence file it reads, so the reading test itself is
    # listed in its own first capture; that self-reference is excluded, and the test's
    # other arms are covered by the live suite.
    new = {name for name in new
           if "test_085_disposal_table.py::test_the_post_disposal_reading" not in name}

    # The disposal's own guards introduce no new failing id.
    owner_prefixes = tuple(FEATURE_MODULES)
    owned_new = {name for name in new if name.split("::")[0] in owner_prefixes}
    assert not owned_new, (
        "the disposal's own modules add new failing ids against the serial baseline: "
        f"{sorted(owned_new)}")

    # A new failure in a disposed module is attributable by name — never silent.
    table_modules = {row["module"] for row in _table_rows()}
    table_new = {name for name in new if name.split("::")[0] in table_modules}
    if table_new:
        assert ATTRIBUTION.is_file(), (
            f"new failures in disposed modules are unattributed: {sorted(table_new)}")
        recorded = ATTRIBUTION.read_text(encoding="utf-8")
        unattributed = sorted(
            name for name in table_new
            if name.split("::")[1].split(" ")[0] not in recorded)
        assert not unattributed, (
            "these new failures in disposed modules carry no recorded attribution: "
            f"{unattributed}")
