"""Contract test: the `[green: <contract>#<clause>]` attribution surface (US2).

Subjects: ``templates/tasks-template.md`` (declares the surface) and
``scripts/python/validate-tasks.py`` (parses it and adds four checks). Both are
runnable/real artifacts, so every behavioral assertion goes through the real
module — never a re-implementation of its regexes here.

The 27 clauses of ``contracts/green-point-claim.md`` are pinned one per test
function where the clause is independently falsifiable, and grouped where the
clause is a two-directional criterion (C-12, C-16, C-17, C-21/C-24).

Two disciplines this suite owes the feature it guards:

* **Anti-vacuity in both directions.** Every "MUST NOT warn" assertion is
  paired with a positive control proving the check fires at all — a probe that
  cannot go red shows only that the check was never triggered (C-24, and
  ``contracts/checker-form.md`` C-21). The plan-phase probe for this very defect
  class mis-read a silent check as a clean one because the fixture omitted `[P]`.
* **One source for the label set.** The 10-label roster is owned by
  ``test_validate_tasks_parallel_safety.py::EXPECTED_CHECKS`` (C-25 names that
  literal); this suite reads it by path rather than re-typing it, so the set has
  one owner and cannot drift into two facts.

Cross-phase semantics (C-12) are pinned by that clause's own two-directional
criterion: within one contract, the clause ordinals of the claims must be
non-decreasing in the rows' monotonic ``order``. FR-017's prose ("a later task
exists in the clause's attribution set") under-determines the condition — read
per clause it makes C-12's inverted copy unreachable, and read per contract it
makes the consistent copy warn too. Only the ordinal-inversion reading satisfies
both halves, so that is what is asserted here.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "scripts" / "python"
VALIDATOR = SCRIPTS / "validate-tasks.py"
TASKS_TPL = REPO_ROOT / "templates" / "tasks-template.md"
TASKS_CMD = REPO_ROOT / "templates" / "commands" / "tasks.md"
QUICKSTART = (
    REPO_ROOT / ".specify" / "specs" / "053-machine-decidable-artifacts" / "quickstart.md"
)

# STR-001, the literal declaration surface (owned by requirements.md § Shared Strings).
STR_001 = "[green: <contract>#<clause>]"

REPO_PROPER_NAMES = re.compile(
    r"spec-kit|specify-cli|specify_cli|cloud-native-ai", re.IGNORECASE
)

# The four fields E-4 of data-model.md declares for a parsed claim.
CLAIM_FIELDS = {"contract_file", "clause_id", "task_id", "phase"}

# Literals the implementation site must carry (C-18, C-22, C-23).
GLOSSARY_TERM = "条款分区 (Clause Partition)"
GOVERNOR_TABLE_COMMENT = "closed list of read-only"
BRACKET_SKIP_MECHANISM = "the brackets are outside the match"


def _load(name: str, path: Path = None):
    path = path or (SCRIPTS / name)
    assert path.is_file(), f"missing artifact: {path}"
    spec = importlib.util.spec_from_file_location(path.stem.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _validator():
    return _load("validate-tasks.py", VALIDATOR)


def _sibling_pin(module_file: str, attr: str):
    """Read a pin from a sibling suite by path so the label set keeps ONE owner."""
    path = REPO_ROOT / "tests" / "contract" / module_file
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, attr)


EXPECTED_CHECKS = _sibling_pin("test_validate_tasks_parallel_safety.py", "EXPECTED_CHECKS")

NEW_LABELS = {
    "green-dangling",
    "green-cross-phase",
    "green-clause-collision",
    "green-path-divergence",
}


# --- fixture helpers -------------------------------------------------------


def _contract(tmp_path: Path, name: str = "x.md", clauses=("C-1", "C-2")) -> str:
    """Write a minimal `md-bold-closed` contract; return its spec-dir-relative path."""
    d = tmp_path / "contracts"
    d.mkdir(exist_ok=True)
    body = "".join(f"\n**{c}** [制品类] clause {c} body.\n" for c in clauses)
    (d / name).write_text(f"# Contract: {name}\n{body}", encoding="utf-8")
    return f"contracts/{name}"


def _tasks(tmp_path: Path, body: str, name: str = "tasks.md") -> Path:
    path = tmp_path / name
    path.write_text(f"# Tasks: fixture\n\n{body}\n", encoding="utf-8")
    return path


def _phase(n: int, story: int, rows: list[str]) -> str:
    head = f"## Phase {n}: User Story {story} - fixture (Priority: P{story})\n\n"
    return head + "\n".join(rows) + "\n"


def _labels(messages: list[str], label: str) -> list[str]:
    return [m for m in messages if f"{label}:" in m]


def _run(mod, path: Path):
    errors, warnings = mod.validate(path)
    return errors, warnings


def _declared_ids(path: Path) -> set[str]:
    return set(
        re.findall(r"^- \[[ xX>~]\]\s+(T\d{3}[A-Za-z]?)\b",
                   path.read_text(encoding="utf-8"), re.M)
    )


def _anti_vacuity(mod, path: Path, expected: set[str]) -> None:
    """A clean verdict is evidence only if the rows really parsed as task rows."""
    errors, _ = _run(mod, path)
    structural = [e for e in errors if "green-" not in e]
    assert not structural, (
        f"sentinel: the fixture is malformed, so any clean verdict proves nothing: {structural}"
    )
    assert _declared_ids(path) == expected, (
        f"sentinel: fixture declares {_declared_ids(path)}, test expects {expected}"
    )


# --- C-1 / C-4 / C-5: the declaration surface in the template --------------


def test_c1_template_defines_the_str001_declaration_surface():
    text = TASKS_TPL.read_text(encoding="utf-8")
    assert STR_001 in text, (
        f"tasks-template.md must define the inline attribution surface with the "
        f"STR-001 literal {STR_001!r}; a reader who never opens the spec has no "
        "other place to learn the form"
    )


def test_c4_template_surface_is_project_neutral():
    text = TASKS_TPL.read_text(encoding="utf-8")
    hits = REPO_PROPER_NAMES.findall(text)
    assert hits == [], (
        f"the template is shipped to every consuming project, so a repo proper "
        f"name in it leaks this repository into other people's specs: {sorted(set(hits))}"
    )


def test_c5_declaration_lands_in_the_format_section_beside_blockedby():
    lines = TASKS_TPL.read_text(encoding="utf-8").splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith("## Format:")), None)
    assert start is not None, "sentinel: the `## Format:` section is gone from the template"
    end = next(
        (i for i in range(start + 1, len(lines)) if re.match(r"^#{2,3}\s", lines[i])),
        len(lines),
    )
    section = "\n".join(lines[start:end])
    assert STR_001 in section, (
        "the attribution surface must be explained in the same `## Format:` section "
        "as the `[blockedBy: …]` tag it is modelled on — a label defined in some "
        "other section is not discoverable where the row format is"
    )
    assert "[blockedBy:" in section, (
        "sentinel: the blockedBy definition line moved out of this section, so "
        "'beside the precedent' is no longer what this test measures"
    )


# --- C-2 / C-3 / C-20: the surface is purely additive ---------------------


def test_c2_zero_claims_leaves_a_file_exactly_as_clean_as_today(tmp_path):
    mod = _validator()
    path = _tasks(tmp_path, _phase(1, 1, [
        "- [ ] T001 [US1] Write the widget in src/widget.py",
        "- [ ] T002 [US1] Write the gadget in src/gadget.py",
    ]))
    _anti_vacuity(mod, path, {"T001", "T002"})

    errors, warnings = _run(mod, path)
    assert errors == [] and warnings == [], (
        f"a file with no `[green:]` claim must be judged exactly as before the "
        f"surface existed (pure increment): errors={errors} warnings={warnings}"
    )
    assert mod.main([str(path)]) == 0


def test_c3_claim_folded_onto_a_continuation_line_is_a_row_format_error(tmp_path):
    mod = _validator()
    path = _tasks(tmp_path, _phase(1, 1, [
        "- [ ] T001 [US1] Write the widget in src/widget.py",
        "      [green: contracts/x.md#C-1]",
    ]))
    errors, _ = _run(mod, path)
    assert _labels(errors, "row-format"), (
        "the whole task row must stay on one physical line (owned by "
        "templates/commands/tasks.md:155); folding the claim onto a continuation "
        f"line must be caught by the existing check, not tolerated: {errors}"
    )


def test_c20_claim_only_row_does_not_trip_row_format(tmp_path):
    mod = _validator()
    rel = _contract(tmp_path)
    path = _tasks(tmp_path, _phase(1, 1, [
        f"- [ ] T001 [US1] Pin the first clause [green: {rel}#C-1]",
        "- [ ] T002 [US1] Write the widget in src/widget.py",
    ]))
    _anti_vacuity(mod, path, {"T001", "T002"})

    errors, _ = _run(mod, path)
    assert _labels(errors, "row-format") == [], (
        "a row that declares an attribution but no file path is legal; the "
        f"orthogonality the surface promises is broken: {errors}"
    )


# --- C-6 / C-7 / C-8: parsing ---------------------------------------------


def test_c6_json_emits_one_four_field_object_per_claim(tmp_path, capsys):
    mod = _validator()
    rel = _contract(tmp_path, clauses=("C-1", "C-2", "C-3"))
    path = _tasks(tmp_path, _phase(1, 1, [
        f"- [ ] T001 [US1] Pin two clauses [green: {rel}#C-1] [green: {rel}#C-2]",
        f"- [ ] T002 [US1] Pin the third [green: {rel}#C-3]",
    ]))
    rc = mod.main([str(path), "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0, f"a well-formed claim set must not error: {payload['errors']}"

    claims = payload["green_claims"]
    assert len(claims) == 3, (
        f"one row may declare several claims (FR-015), so all three must parse: {claims}"
    )
    for claim in claims:
        assert set(claim) == CLAIM_FIELDS, (
            f"E-4 of data-model.md declares exactly {sorted(CLAIM_FIELDS)}; got {sorted(claim)}"
        )
    by_task = {c["task_id"]: c for c in claims if c["task_id"] == "T002"}
    assert by_task["T002"]["contract_file"] == rel
    assert by_task["T002"]["clause_id"] == "C-3"
    assert "User Story 1" in by_task["T002"]["phase"], (
        f"the phase must be the nearest `## Phase` heading, got {by_task['T002']['phase']!r}"
    )


def test_c7_clause_id_tolerates_dots_and_hyphens_first_hash_wins(tmp_path, capsys):
    mod = _validator()
    rel = _contract(tmp_path, clauses=("C-3.4",))
    path = _tasks(tmp_path, _phase(1, 1, [
        f"- [ ] T001 [US1] Pin the dotted clause [green: {rel}#C-3.4]",
    ]))
    rc = mod.main([str(path), "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0, f"a dotted clause id must resolve, not dangle: {payload['errors']}"
    claim = payload["green_claims"][0]
    assert (claim["contract_file"], claim["clause_id"]) == (rel, "C-3.4"), (
        f"the separator is the FIRST `#` and everything up to `]` is the id: {claim}"
    )


def test_c8_claim_inside_a_fence_is_not_a_claim(tmp_path, capsys):
    mod = _validator()
    rel = _contract(tmp_path)
    path = _tasks(tmp_path, _phase(1, 1, [
        "- [ ] T001 [US1] Write the widget in src/widget.py",
    ]) + "\n```text\n"
       + f"- [ ] T002 [US1] Example row [green: {rel}#C-1]\n"
       + f"- [ ] T003 [US1] Example dangling [green: contracts/nope.md#C-1]\n"
       + "```\n")
    rc = mod.main([str(path), "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert payload["green_claims"] == [], (
        f"a form inside a fenced block is an EXAMPLE, not a declaration; parsing "
        f"it makes every documentation snippet a source of phantom claims: {payload['green_claims']}"
    )
    assert rc == 0, (
        f"a fenced dangling example must not fail the file: {payload['errors']}"
    )


def test_c8b_claim_inside_an_inline_code_span_is_a_mention_not_a_declaration(tmp_path, capsys):
    """The second non-declaration context, found by dogfooding rather than by design.

    The row that added this surface to the template had to NAME the tag to define it —
    ``with the STR-001 literal tag `[green: <contract>#<clause>]` `` — and the first
    implementation parsed that mention as a real claim on a contract file literally
    named `<contract>`, so the feature's own tasks.md failed its own GATE-7. A document
    that cannot name its own markup cannot describe it, so the rule FR-009 already
    draws for references (backticks make a mention) applies here unchanged.
    """
    mod = _validator()
    rel = _contract(tmp_path)
    path = _tasks(tmp_path, _phase(1, 1, [
        f"- [ ] T001 [US1] Document the `[green: <contract>#<clause>]` form and the "
        f"`[green:]` shorthand, then really claim [green: {rel}#C-1]",
        f"- [ ] T002 [US1] Only ever mentions `[green: {rel}#C-2]` in prose",
    ]))
    rc = mod.main([str(path), "--json"])
    payload = json.loads(capsys.readouterr().out)

    assert rc == 0, f"a mentioned tag must not dangle: {payload['errors']}"
    claims = payload["green_claims"]
    assert [(c["task_id"], c["clause_id"]) for c in claims] == [("T001", "C-1")], (
        f"exactly the bare declaration is a claim; the two backticked forms on T001 "
        f"and the one on T002 are mentions: {claims}"
    )


def test_c8c_an_unclosed_code_span_leaves_the_claim_a_real_claim(tmp_path, capsys):
    """The complement of C-8b: stripping must not swallow declarations either.

    Per CommonMark an unclosed backtick run is literal text, so a claim after a stray
    backtick is still a declaration. Pinning only the negative half would let an
    implementation pass by refusing to parse claims at all.
    """
    mod = _validator()
    rel = _contract(tmp_path)
    path = _tasks(tmp_path, _phase(1, 1, [
        f"- [ ] T001 [US1] A stray backtick ` then a real claim [green: {rel}#C-1]",
    ]))
    rc = mod.main([str(path), "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0, f"sentinel: the claim should resolve, got {payload['errors']}"
    assert [(c["task_id"], c["clause_id"]) for c in payload["green_claims"]] == [
        ("T001", "C-1")
    ], f"an unclosed span made a real declaration invisible: {payload['green_claims']}"


def test_c11_clause_existence_is_resolved_through_the_owner_extractor(tmp_path):
    mod = _validator()
    src = VALIDATOR.read_text(encoding="utf-8")
    assert "clause_extract" in src, (
        "C-11/FR-022: clause resolvability must be judged by the D-1 owner's forms "
        "via scripts/python/clause_extract.py, not by a second private regex here"
    )
    # An `md-none` contract has no machine-decidable clause at all: a claim on it
    # is dangling, and MUST NOT be waved through because "the file exists".
    d = tmp_path / "contracts"
    d.mkdir(exist_ok=True)
    (d / "prose.md").write_text(
        "# Contract: prose\n\nThis contract states its rules as prose only.\n",
        encoding="utf-8",
    )
    path = _tasks(tmp_path, _phase(1, 1, [
        "- [ ] T001 [US1] Pin a prose clause [green: contracts/prose.md#C-1]",
    ]))
    errors, _ = _run(mod, path)
    assert _labels(errors, "green-dangling"), (
        f"a claim on an unparseable (`md-none`) contract must be an ERROR: {errors}"
    )


# --- C-9 / C-10: dangling attribution is an ERROR -------------------------


def test_c9_missing_contract_file_is_an_error_not_a_warning(tmp_path):
    mod = _validator()
    path = _tasks(tmp_path, _phase(1, 1, [
        "- [ ] T001 [US1] Pin a clause [green: contracts/nope.md#C-1]",
    ]))
    errors, warnings = _run(mod, path)
    assert _labels(errors, "green-dangling"), (
        f"a dangling attribution is worse than a cross-phase one, so it is an "
        f"ERROR: errors={errors}"
    )
    assert _labels(warnings, "green-dangling") == [], "it must not be downgraded to a WARN"
    assert mod.main([str(path)]) == 1, "1 = at least one error"


def test_c10_missing_clause_id_is_an_error_naming_file_and_id(tmp_path):
    mod = _validator()
    rel = _contract(tmp_path, clauses=("C-1",))
    path = _tasks(tmp_path, _phase(1, 1, [
        f"- [ ] T001 [US1] Pin a clause that is not there [green: {rel}#C-9]",
    ]))
    errors, _ = _run(mod, path)
    hits = _labels(errors, "green-dangling")
    assert hits, f"an unresolvable clause id is an ERROR: {errors}"
    assert rel in hits[0] and "C-9" in hits[0], (
        f"the message must name both the contract file and the missing id so the "
        f"author can act without re-running the tool: {hits[0]}"
    )
    assert mod.main([str(path)]) == 1


def test_c9b_contract_path_resolves_from_the_repo_root_too(tmp_path):
    """E-4 declares `contract_file` repo-root relative; the spec-dir form must also work.

    A real tasks.md sits inside its spec directory and its contracts are
    `contracts/<name>.md` beside it, so resolution tries the tasks.md directory
    first and the repo root second. Only one of the two forms can be a hard
    requirement, and neither is: pinning one and silently failing the other is
    how a whole feature's claims turn dangling.
    """
    mod = _validator()
    target = REPO_ROOT / "scripts" / "python" / "clause_extract.py"
    assert target.is_file(), f"sentinel: the repo-root-relative target is gone: {target}"
    rel = _contract(tmp_path)
    path = _tasks(tmp_path, _phase(1, 1, [
        f"- [ ] T001 [US1] Spec-dir relative [green: {rel}#C-1]",
        "- [ ] T002 [US1] Repo-root relative [green: pyproject.toml#C-1]",
    ]))
    errors, _ = _run(mod, path)
    spec_dir_hits = [e for e in _labels(errors, "green-dangling") if rel in e]
    assert spec_dir_hits == [], (
        f"a contract beside the tasks.md must resolve: {spec_dir_hits}"
    )
    root_hits = [e for e in _labels(errors, "green-dangling") if "pyproject.toml" in e]
    assert root_hits and "no machine-decidable clause" in root_hits[0], (
        "a repo-root-relative path must be FOUND (and then judged on its clause "
        f"form), not reported as a missing file: {root_hits}"
    )


# --- C-12 / C-13 / C-14: cross-phase green points -------------------------


def test_c12_consistent_order_yields_zero_cross_phase_warnings(tmp_path):
    mod = _validator()
    rel = _contract(tmp_path, clauses=("C-1", "C-2"))
    path = _tasks(tmp_path,
                  _phase(1, 1, [f"- [ ] T001 [US1] Pin clause one [green: {rel}#C-1]"])
                  + "\n"
                  + _phase(2, 2, [f"- [ ] T002 [US2] Pin clause two [green: {rel}#C-2]"]))
    _anti_vacuity(mod, path, {"T001", "T002"})

    errors, warnings = _run(mod, path)
    assert errors == []
    assert _labels(warnings, "green-cross-phase") == [], (
        f"claims in clause order across phases are the normal, correct shape: {warnings}"
    )


def test_c12_inverted_order_yields_a_cross_phase_warning_naming_rows_and_phases(tmp_path):
    mod = _validator()
    rel = _contract(tmp_path, clauses=("C-1", "C-2"))
    path = _tasks(tmp_path,
                  _phase(1, 1, [f"- [ ] T001 [US1] Pin clause two [green: {rel}#C-2]"])
                  + "\n"
                  + _phase(2, 2, [f"- [ ] T002 [US2] Pin clause one [green: {rel}#C-1]"]))
    _anti_vacuity(mod, path, {"T001", "T002"})

    errors, warnings = _run(mod, path)
    hits = _labels(warnings, "green-cross-phase")
    assert errors == []
    assert hits, (
        "an earlier row claiming a LATER clause than a subsequent row means the "
        "earlier row cannot leave the contract green at its own phase — the exact "
        "silent MVP-truncation hazard this check exists for"
    )
    for needle in ("C-1", "C-2", "T001", "T002", "Phase 1", "Phase 2"):
        assert needle in hits[0], (
            f"the message must name the clause, both rows and the phase order so "
            f"the reader can act; missing {needle!r}: {hits[0]}"
        )


def test_c13_cross_phase_compares_monotonic_order_not_a_numeric_phase_index(tmp_path):
    """The phase headings' numbers invert the rows' order here, on purpose.

    `validate-tasks.py` has no numeric phase index (PHASE_HEADING captures the
    heading string; `by_phase` groups by it), and D-8 forbids inventing one. An
    implementation that parsed the heading numbers would read Phase 9 as later
    than Phase 2 and report nothing for this file.
    """
    mod = _validator()
    rel = _contract(tmp_path, clauses=("C-1", "C-2"))
    path = _tasks(tmp_path,
                  _phase(9, 1, [f"- [ ] T001 [US1] Pin clause two [green: {rel}#C-2]"])
                  + "\n"
                  + _phase(2, 2, [f"- [ ] T002 [US2] Pin clause one [green: {rel}#C-1]"]))
    _anti_vacuity(mod, path, {"T001", "T002"})

    _, warnings = _run(mod, path)
    hits = _labels(warnings, "green-cross-phase")
    assert len(hits) == 1, (
        f"row order decides, not the number in the heading (Phase 9 precedes "
        f"Phase 2 in this file): {hits}"
    )

    src = VALIDATOR.read_text(encoding="utf-8")
    assert not re.search(r"phase_(?:index|number|no)\b", src), (
        "a numeric phase index was introduced; D-8 requires the existing "
        "monotonic `order` counter (the same quantity :229-233 compares for "
        "blockedBy forward dependencies)"
    )


def test_c14_warning_only_file_still_exits_zero(tmp_path):
    mod = _validator()
    rel = _contract(tmp_path, clauses=("C-1", "C-2"))
    warn = _tasks(tmp_path,
                  _phase(1, 1, [f"- [ ] T001 [US1] Pin clause two [green: {rel}#C-2]"])
                  + "\n"
                  + _phase(2, 2, [f"- [ ] T002 [US2] Pin clause one [green: {rel}#C-1]"]))
    _, warnings = _run(mod, warn)
    assert warnings, "sentinel: the fixture produced no warning, so exit 0 proves nothing"
    assert mod.main([str(warn)]) == 0, (
        "the existing exit table has two tiers only (0 = no error, 1 = error); "
        "C-14 forbids adding a third for warnings"
    )


# --- C-15 / C-16 / C-17: the two collision classes, reported separately ---


def test_c15_two_rows_claiming_one_clause_collide_and_both_are_named(tmp_path):
    mod = _validator()
    rel = _contract(tmp_path, clauses=("C-1",))
    path = _tasks(tmp_path, _phase(1, 1, [
        f"- [ ] T001 [US1] Pin the clause in tests/contract/test_a.py [green: {rel}#C-1]",
        f"- [ ] T002 [US1] Pin it again in tests/contract/test_b.py [green: {rel}#C-1]",
    ]))
    _anti_vacuity(mod, path, {"T001", "T002"})

    _, warnings = _run(mod, path)
    hits = _labels(warnings, "green-clause-collision")
    assert hits, f"one clause partition claimed by two rows is a collision: {warnings}"
    assert "T001" in hits[0] and "T002" in hits[0], (
        f"both rows must be named so the partition can be re-cut: {hits[0]}"
    )


def test_c16_path_divergence_is_about_differing_green_points_not_a_shared_path(tmp_path):
    """Paired on purpose: the negative half is what makes the label meaningful."""
    mod = _validator()
    rel = _contract(tmp_path, clauses=("C-1", "C-2"))

    diverging = _tasks(tmp_path,
                       _phase(1, 1, [f"- [ ] T001 [US1] Pin clause one in tests/contract/test_x.py [green: {rel}#C-1]"])
                       + "\n"
                       + _phase(2, 2, [f"- [ ] T002 [US2] Pin clause two in tests/contract/test_x.py [green: {rel}#C-2]"]),
                       name="diverging.md")
    _anti_vacuity(mod, diverging, {"T001", "T002"})
    _, warnings = _run(mod, diverging)
    hits = _labels(warnings, "green-path-divergence")
    assert hits, (
        "one test file claimed green at two different points by two rows is the "
        "unsatisfiable pair templates/commands/tasks.md:197 warns about in prose"
    )
    for needle in ("T001", "T002", "tests/contract/test_x.py"):
        assert needle in hits[0], f"the message must name both rows and the path: {hits[0]}"

    agreeing = _tasks(tmp_path,
                      _phase(1, 1, [f"- [ ] T001 [US1] Pin clause one in tests/contract/test_x.py [green: {rel}#C-1]"])
                      + "\n"
                      + _phase(2, 2, [f"- [ ] T002 [US2] Re-verify clause one in tests/contract/test_x.py [green: {rel}#C-1]"]),
                      name="agreeing.md")
    _anti_vacuity(mod, agreeing, {"T001", "T002"})
    _, warnings2 = _run(mod, agreeing)
    assert _labels(warnings2, "green-path-divergence") == [], (
        f"a shared test path with the SAME green point is not a divergence; if "
        f"this warns, the check is really detecting path sharing: {warnings2}"
    )


def test_c17_the_two_collision_labels_are_separately_counted(tmp_path):
    """Each fixture fires exactly one of the pair — the other's count must be 0."""
    mod = _validator()
    rel = _contract(tmp_path, clauses=("C-1", "C-2"))

    collision_only = _tasks(tmp_path, _phase(1, 1, [
        f"- [ ] T001 [US1] Pin clause one in tests/contract/test_a.py [green: {rel}#C-1]",
        f"- [ ] T002 [US1] Pin clause one in tests/contract/test_b.py [green: {rel}#C-1]",
    ]), name="collision.md")
    _, w1 = _run(mod, collision_only)
    assert _labels(w1, "green-clause-collision"), f"sentinel: collision did not fire: {w1}"
    assert _labels(w1, "green-path-divergence") == [], (
        f"a clause collision must not be reported as a path divergence too — the "
        f"two have different remedies and a merged count hides which one applies: {w1}"
    )

    divergence_only = _tasks(tmp_path,
                             _phase(1, 1, [f"- [ ] T001 [US1] Pin clause one in tests/contract/test_x.py [green: {rel}#C-1]"])
                             + "\n"
                             + _phase(2, 2, [f"- [ ] T002 [US2] Pin clause two in tests/contract/test_x.py [green: {rel}#C-2]"]),
                             name="divergence.md")
    _, w2 = _run(mod, divergence_only)
    assert _labels(w2, "green-path-divergence"), f"sentinel: divergence did not fire: {w2}"
    assert _labels(w2, "green-clause-collision") == [], (
        f"a path divergence must not be reported as a clause collision too: {w2}"
    )


def test_c18_implementation_cites_the_registered_glossary_term():
    src = VALIDATOR.read_text(encoding="utf-8")
    assert GLOSSARY_TERM in src, (
        f"the collision check mechanizes the registered term {GLOSSARY_TERM!r} "
        "(`.specify/memory/glossary.md`); FR-018 forbids coining a second name for "
        "the same failure mode"
    )


def test_c19_the_prose_self_check_points_at_the_check_and_keeps_one_criterion():
    text = TASKS_CMD.read_text(encoding="utf-8")
    assert "green-path-divergence" in text, (
        "the prose obligation at templates/commands/tasks.md ('flags any test path "
        "appearing in two verification rows with different green points') must "
        "point at the check that now performs it"
    )
    sentences = [s for s in re.split(r"(?<=[.;。])\s+", text) if "different green points" in s]
    assert sentences, "sentinel: the prose obligation was deleted rather than re-pointed"
    assert len(sentences) == 1, (
        f"the criterion must exist once; found {len(sentences)} statements of it"
    )
    assert "green-path-divergence" in sentences[0], (
        f"the surviving statement still asks for manual diligence beside the "
        f"machine check, i.e. two criteria for one rule: {sentences[0][:200]}"
    )


# --- C-21 / C-22 / C-23 / C-24: orthogonality with the path classifier ----


NEG_ROWS = [
    "- [ ] T001 [P] Write the thing in docs/a.md [green: contracts/x.md#C-1]",
    "- [ ] T002 [P] Write another thing in docs/b.md [green: contracts/x.md#C-2]",
]
POS_ROWS = [
    "- [ ] T001 [P] Write the thing in docs/a.md",
    "- [ ] T002 [P] Write another thing in docs/a.md",
]


def test_c21_claim_path_is_not_a_write_target_but_real_conflicts_still_warn(tmp_path):
    """Positive control FIRST (C-24): a probe that cannot go red proves nothing."""
    mod = _validator()
    pos = _tasks(tmp_path, "## Phase 1: Setup\n\n" + "\n".join(POS_ROWS) + "\n", name="pos.md")
    _, pos_warnings = _run(mod, pos)
    assert [w for w in pos_warnings if "parallel-safe" in w], (
        "sentinel: two [P] rows writing the SAME real path did not warn, so the "
        "clean verdict below would only show that the check never ran"
    )

    d = tmp_path / "contracts"
    d.mkdir(exist_ok=True)
    (d / "x.md").write_text("# Contract: x\n\n**C-1** a.\n\n**C-2** b.\n", encoding="utf-8")
    neg = _tasks(tmp_path, "## Phase 1: Setup\n\n" + "\n".join(NEG_ROWS) + "\n", name="neg.md")
    errors, warnings = _run(mod, neg)
    assert not errors, f"sentinel: the neg fixture should be clean, got {errors}"
    assert [w for w in warnings if "parallel-safe" in w] == [], (
        f"docs/a.md and docs/b.md differ; a warning here names the contract path "
        f"from inside the `[green:]` label, which is a false conflict: {warnings}"
    )


def test_c22_fix_extracts_before_classifying_and_leaves_the_governor_list_closed():
    mod = _validator()
    assert "green" not in mod.POINTER_GOVERNOR.pattern.lower(), (
        "`[green:` was added to POINTER_GOVERNOR. That table is deliberately a "
        "closed list of unambiguous read-only governor WORDS; `[green:` is a label "
        "prefix, so adding it makes the table's own comment false"
    )
    src = VALIDATOR.read_text(encoding="utf-8")
    assert GOVERNOR_TABLE_COMMENT in src, (
        "the rejection of the governor-list route must be recorded where a future "
        "editor would otherwise take it"
    )
    body = src[src.index("def validate("):]
    strip_at = next(
        (i for i, l in enumerate(body.splitlines())
         if "green" in l.lower() and re.search(r"\b(sub|strip|extract|pop|replace)\b", l)),
        None,
    )
    classify_at = next(
        (i for i, l in enumerate(body.splitlines()) if "_classify_paths(" in l), None
    )
    assert strip_at is not None, "sentinel: no claim-extraction step found in validate()"
    assert classify_at is not None, "sentinel: no path-classification step found in validate()"
    assert strip_at < classify_at, (
        "claims must be extracted BEFORE the residual text is path-classified, so "
        "that orthogonality is a construction property rather than a regex special "
        f"case (extraction at line {strip_at}, classification at {classify_at})"
    )


def test_c23_the_false_positive_mechanism_is_recorded_at_the_implementation_site():
    src = VALIDATOR.read_text(encoding="utf-8")
    assert "PATH_TOKEN" in src and BRACKET_SKIP_MECHANISM in src, (
        "C-23: the comment must explain WHY the old bracket skip did not protect "
        "the claim path — PATH_TOKEN's trailing class has no `#`, so the matched "
        "token itself contains no bracket and `if \"[\" in tok` never sees one. "
        "Without that note the next reader re-adds the label to the governor list."
    )


def test_c24_scenario_4_runs_the_positive_control_before_judging_the_negative():
    text = QUICKSTART.read_text(encoding="utf-8")
    scenario = text.split("## 场景 4")[1].split("## 场景 5")[0]
    pos_at = scenario.index("pos.md;")
    neg_at = scenario.index("neg.md;")
    assert pos_at < neg_at, (
        "the positive control must be RUN before the negative is judged; the "
        "plan-phase probe for this defect mis-read a never-triggered check as a "
        "clean one because the fixture omitted `[P]`"
    )
    assert "先跑 POS" in scenario, (
        "the ordering duty must be stated, not merely performed once in a sample"
    )


# --- C-25 / C-26 / C-27: pin growth and the counter-sample battery --------


def test_c25_label_roster_grew_by_exactly_the_four_new_labels():
    mod = _validator()
    doc = mod.__doc__ or ""
    labels = set(re.findall(r"^  ([A-Za-z][A-Za-z-]*)\s{2,}", doc, re.M))
    assert labels, "sentinel: no labels parsed from the docstring — the roster check is blind"
    assert labels == EXPECTED_CHECKS, (
        f"the docstring roster and EXPECTED_CHECKS must be extended in the SAME "
        f"commit (C-25); docstring={sorted(labels)} pin={sorted(EXPECTED_CHECKS)}"
    )
    assert NEW_LABELS <= labels, f"the four US2 labels are missing: {sorted(NEW_LABELS - labels)}"
    assert len(NEW_LABELS) == 4


def test_c26_new_exit_tiers_follow_the_existing_two_tier_table(tmp_path):
    mod = _validator()
    rel = _contract(tmp_path, clauses=("C-1", "C-2"))

    dangling = _tasks(tmp_path, _phase(1, 1, [
        "- [ ] T001 [US1] Pin a clause [green: contracts/nope.md#C-1]",
    ]), name="dangling.md")
    assert mod.main([str(dangling)]) == 1, "green-dangling is an ERROR → 1"

    warn_only = _tasks(tmp_path,
                       _phase(1, 1, [
                           f"- [ ] T001 [US1] Pin clause two in tests/contract/test_a.py [green: {rel}#C-2]",
                           f"- [ ] T002 [US1] Pin clause two in tests/contract/test_b.py [green: {rel}#C-2]",
                       ])
                       + "\n"
                       + _phase(2, 2, [
                           f"- [ ] T003 [US2] Pin clause one in tests/contract/test_a.py [green: {rel}#C-1]",
                       ]),
                       name="warn_only.md")
    _, warnings = _run(mod, warn_only)
    assert warnings, f"sentinel: the warn-only fixture produced nothing: {warnings}"
    assert mod.main([str(warn_only)]) == 0, (
        "cross-phase and both collision classes are WARN → still 0 (C-14, C-26)"
    )


def test_c27_each_new_label_has_its_own_counter_sample_hitting_only_itself(tmp_path):
    mod = _validator()
    rel = _contract(tmp_path, clauses=("C-1", "C-2"))

    samples = {
        "green-dangling": "## Phase 1: User Story 1 - s (Priority: P1)\n\n"
                          "- [ ] T001 [US1] Pin a clause [green: contracts/nope.md#C-1]\n",
        "green-cross-phase":
            _phase(1, 1, [f"- [ ] T001 [US1] Pin clause two [green: {rel}#C-2]"])
            + "\n"
            + _phase(2, 2, [f"- [ ] T002 [US2] Pin clause one [green: {rel}#C-1]"]),
        "green-clause-collision": _phase(1, 1, [
            f"- [ ] T001 [US1] Pin clause one in tests/contract/test_a.py [green: {rel}#C-1]",
            f"- [ ] T002 [US1] Pin clause one in tests/contract/test_b.py [green: {rel}#C-1]",
        ]),
        "green-path-divergence":
            _phase(1, 1, [f"- [ ] T001 [US1] Pin clause one in tests/contract/test_x.py [green: {rel}#C-1]"])
            + "\n"
            + _phase(2, 2, [f"- [ ] T002 [US2] Pin clause two in tests/contract/test_x.py [green: {rel}#C-2]"]),
    }
    assert set(samples) == NEW_LABELS, "sentinel: the battery does not cover the four labels"

    for label, body in samples.items():
        path = _tasks(tmp_path, body, name=f"{label}.md")
        errors, warnings = _run(mod, path)
        own = _labels(errors, label) + _labels(warnings, label)
        assert own, f"counter-sample {label!r} did not fire its own label: {errors + warnings}"
        others = [
            o for o in NEW_LABELS - {label}
            if _labels(errors, o) or _labels(warnings, o)
        ]
        assert not others, (
            f"counter-sample {label!r} also fired {others} — a sample that breaks "
            "two propositions at once cannot attribute a red to either"
        )
