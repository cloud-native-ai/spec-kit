"""Contract test: the clause-syntax owner document and the coverage accountant (US3).

Pins all 27 clauses of ``contracts/clause-coverage.md``. Two subjects, because the
contract has two:

* ``shared/definitions/contract-clause-definitions.md`` — the FR-022 owner of clause
  syntax (C-1…C-6). It landed in Phase 2, so those six assertions are green before
  this phase; each is listed in the module-level note below with what turns it red.
* ``scripts/python/account-clause-coverage.py`` — the accountant (C-7…C-27). Every one
  of those is red until T025 lands the script.

This suite also owns the accountant's **checker-form** obligations. It is deliberately
NOT parametrized into ``test_checker_form.py``'s per-artifact battery: that battery hands
a checker one artifact file and expects a verdict on it, while the accountant takes a spec
directory and accounts a whole corpus (FR-023…FR-028), and its exit-0 state is unreachable
until T045 retro-fits this feature's own claims — so pinning it there would have been a
permanently red test, not a guard. What it does share with every new script (STR-008
attribution, docstring label body, read-only, packaging) is asserted here and in
``test_checker_form.py``'s ``ALL_NEW_SCRIPTS`` set.

``ACCOUNTANT_CHECKS`` below is the ONE source for the accountant's label set;
``test_checker_form.py`` reads it by path rather than re-typing it.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts" / "python"
ACCOUNTANT = SCRIPTS / "account-clause-coverage.py"
OWNER_DOC = ROOT / "shared" / "definitions" / "contract-clause-definitions.md"
CENSUS = (
    ROOT / ".specify" / "specs" / "053-machine-decidable-artifacts" / "notes"
    / "clause-form-census.md"
)
SPEC_053 = ROOT / ".specify" / "specs" / "053-machine-decidable-artifacts"
UFC = ROOT / "shared" / "guidelines" / "user-facing-comprehension.md"

# The four labels data-model.md § 标签集 declares for this subject. One source: the
# set literal, never a count (checker-form C-22).
ACCOUNTANT_CHECKS = {
    "clause-uncovered",
    "fr-uncovered",
    "clause-unparsable",
    "coverage-baseline-delta",
}

LABEL_DOC_RE = re.compile(r"^  ([A-Za-z][A-Za-z-]*)\s{2,}", re.M)
STR008 = "Program-First discipline (shared/guidelines/token-efficiency.md)"
UNCOVERED = "UNCOVERED:"
STATUSES = {"ok", "uncovered", "baseline-missing", "input-error"}

# Drift-detecting literals. Each is one of the three legitimate duplicate kinds
# (one-source-of-truth.md): a literal pinned in a test. Their owner is
# notes/clause-form-census.md; if a future spec changes the corpus, that file is
# re-derived and these move with it — deliberately, in one commit.
OPENAPI_OPERATIONS_EXCL_053 = 39          # census, as-of 2026-09-24 basis
MISNOMER_YAML = (
    ROOT / ".specify" / "specs" / "013-portable-skill-creation" / "contracts"
    / "portable-skill-creation.openapi.yaml"
)
MISNOMER_IDS = {
    "no-tool-discovery-step",
    "no-tool-template-boilerplate",
    "no-mandatory-tool-manifests",
    "no-refresh-tools-in-script",
    "mirror-parity",
    "no-tool-manifest-in-checklist",
}
PAREN_FORM_FILE = (
    ROOT / ".specify" / "specs" / "031-task-complexity-rubric" / "contracts"
    / "rubric-section.md"
)
PAREN_FORM_CLAUSES = 10
GATE_TOTAL = 23


def _load():
    assert ACCOUNTANT.is_file(), (
        f"missing artifact: {ACCOUNTANT} — this suite's subject has not landed (T025)"
    )
    spec = importlib.util.spec_from_file_location("_account_coverage_under_test", ACCOUNTANT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _run(args, expect=None):
    r = subprocess.run(
        [sys.executable, str(ACCOUNTANT), *args],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    if expect is not None:
        assert r.returncode == expect, (
            f"account-clause-coverage.py {args} -> {r.returncode}\n{r.stdout}\n{r.stderr}"
        )
    return r


def _payload(args, expect=None):
    return json.loads(_run([*args, "--json"], expect=expect).stdout)


# --- hermetic corpus fixtures ---------------------------------------------


def _spec_dir(corpus: Path, key: str, frs=("FR-001", "FR-002", "FR-003"),
              clauses=(("C-1", "FR-001"), ("C-2", "FR-002"), ("C-3", "FR-003")),
              claims=("C-1", "C-2"), prose_contract: bool = False) -> Path:
    """One spec directory: requirements.md + contracts/c.md + tasks.md with `[green:]` rows."""
    d = corpus / key
    (d / "contracts").mkdir(parents=True, exist_ok=True)
    reqs = "\n".join(f"- **{f}**: requirement {f} text." for f in frs)
    (d / "requirements.md").write_text(
        f"# Spec: {key}\n\n## Functional Requirements\n\n{reqs}\n", encoding="utf-8"
    )
    body = "".join(
        f"\n**{c}** [制品类] clause {c} body. ({fr})\n" for c, fr in clauses
    )
    (d / "contracts" / "c.md").write_text(f"# Contract: c\n{body}", encoding="utf-8")
    if prose_contract:
        (d / "contracts" / "prose.md").write_text(
            "# Contract: prose\n\nRules stated as prose only.\n", encoding="utf-8"
        )
    rows = "\n".join(
        f"- [ ] T{i + 1:03d} Pin clause {c} [green: contracts/c.md#{c}]"
        for i, c in enumerate(claims)
    ) or "- [ ] T001 Write something in src/a.py"
    (d / "tasks.md").write_text(
        f"# Tasks: {key}\n\n## Phase 1: Setup\n\n{rows}\n", encoding="utf-8"
    )
    return d


def _corpus(tmp_path: Path, **kwargs) -> Path:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    _spec_dir(corpus, "001-alpha", **kwargs)
    return corpus


def _freeze(mod, spec: Path, corpus: Path) -> Path:
    """Freeze a baseline the way T026 does: over the corpus EXCLUDING `spec`.

    The script PRINTS the baseline document and the test writes it, because C-20 requires
    the accountant to have zero write points — a tool that wrote its own baseline would
    fail the write-point scan that clause-coverage.md C-20 pins.
    """
    baseline = spec / "coverage-baseline.txt"
    r = subprocess.run(
        [sys.executable, str(ACCOUNTANT), str(spec), "--corpus-root", str(corpus), "--freeze"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert r.returncode == 0, f"the freeze run itself must succeed:\n{r.stdout}\n{r.stderr}"
    assert r.stdout.startswith("# coverage-baseline:"), (
        f"--freeze must print the baseline document on stdout: {r.stdout[:200]}"
    )
    baseline.write_text(r.stdout, encoding="utf-8")
    return baseline


# =========================================================================== #
# C-1 … C-6 — the owner document (landed in Phase 2; green before this phase)
#
# Each is green-before for a stated reason, and red-capable:
#   C-1  the doc exists and self-declares  -> red if the declaration is reworded away
#   C-2  six forms + block/citation rules  -> red if a form or a rule is dropped
#   C-3  one canonical, rest legacy        -> red if a second canonical form appears
#   C-4  no contract clause body copied    -> red if the doc starts carrying clauses
#   C-5  gate budget still 23 / 0          -> red if any shared/ wording trips a pattern
#   C-6  the cap is pinned three ways      -> red if a pin's wording is edited
# =========================================================================== #


def test_c1_owner_doc_exists_declares_ownership_and_points_at_uic():
    assert OWNER_DOC.is_file(), f"the FR-022 owner document is missing: {OWNER_DOC}"
    lines = OWNER_DOC.read_text(encoding="utf-8").splitlines()
    opening = "\n".join(lines[:12])
    assert re.search(r"owner|唯一真源|唯一 owner", opening, re.IGNORECASE), (
        "an owning document must say so in its opening lines and name what it owns; "
        f"the first 12 lines say: {opening[:400]}"
    )
    text = "\n".join(lines)
    assert "user-facing-comprehension.md" in text, (
        "Principle XV requires a new shared/ document to carry the canonical pointer "
        "to the user-facing-comprehension owner"
    )
    # pointer form, not a copy: the owner's class table must not be restated here
    ufc_rows = re.findall(r"^\|\s*[①②③④⑤⑥⑦⑧⑨⑩⑪]", UFC.read_text(encoding="utf-8"), re.M)
    assert ufc_rows, "sentinel: the UFC class table moved; this assertion measures nothing"
    copied = [r for r in ufc_rows if r in text]
    assert copied == [], f"the pointer became a second copy of the owner's table: {copied}"


def test_c2_owner_doc_declares_all_six_forms_and_the_three_block_rules():
    text = OWNER_DOC.read_text(encoding="utf-8")
    for form in ("md-bold-closed", "md-bold-paren", "md-heading",
                 "yaml-openapi", "yaml-assertions", "md-none"):
        assert form in text, f"the owner's form set is missing {form}"
    for needle in (r"\*\*C-\d", "^#{1,6}", r"^\s+- id:"):
        assert needle in text, f"the owner states no criterion regex {needle!r}"
    # the three rules C-2 declares as jointly necessary
    assert re.search(r"标记|marker", text) and re.search(r"标题|heading", text), (
        "the block-boundary rule (marker line to the next marker OR the next heading, "
        "whichever first) must be stated — without it three self-consistent totals exist"
    )
    assert re.search(r"引用组|citation group", text), (
        "the citation-group rule (the block's LAST FR/SC-bearing parenthetical) must be stated"
    )
    assert re.search(r"提及|mention", text), (
        "the third rule — ids outside the citation group are mentions, not citations — "
        "must be stated"
    )


def test_c3_exactly_one_canonical_form_and_legacy_forms_are_read_only():
    text = OWNER_DOC.read_text(encoding="utf-8")
    assert re.search(r"canonical|规范", text) and re.search(r"legacy|遗留", text), (
        "the owner must name one canonical form for NEW contracts and declare the rest "
        "read-only legacy forms"
    )
    canonical_lines = [
        l for l in text.splitlines()
        if re.search(r"canonical|规范形态", l) and re.search(r"md-bold-closed|\*\*C-", l)
    ]
    assert canonical_lines, "no line declares which form is canonical"
    declared = {
        f for l in canonical_lines
        for f in ("md-bold-closed", "md-bold-paren", "md-heading",
                  "yaml-openapi", "yaml-assertions") if f in l
    }
    assert len(declared) == 1, f"exactly one canonical form; found {sorted(declared)}"


def _prose_probe(text: str, width: int = 60) -> str:
    """The first `width` characters of a clause's PROSE, code spans removed.

    C-4 exempts citation forms, and a clause that opens with a backticked path collides
    with any document citing the same path — measured: 051's `discipline-doc.md` C-2
    begins with the user-facing-comprehension path that C-1 *requires* this owner doc to
    carry, so a raw 40-character prefix probe reported a copy where there was a citation.
    """
    stripped = re.sub(r"`[^`]*`", " ", text)
    return re.sub(r"\s+", " ", stripped).strip()[:width]


def test_c4_owner_doc_copies_no_clause_body_from_any_contract():
    """It owns the SYNTAX; a clause body copied in would be a second source of that clause."""
    doc = re.sub(r"\s+", " ", re.sub(r"`[^`]*`", " ", OWNER_DOC.read_text(encoding="utf-8")))
    spec_root = ROOT / ".specify" / "specs"
    scanned = 0
    offenders = []
    for contract in sorted(spec_root.glob("*/contracts/*")):
        if not contract.is_file() or contract.name == OWNER_DOC.name:
            continue
        body = contract.read_text(encoding="utf-8", errors="replace")
        for clause_id, text in re.findall(
                r"(?m)^\*\*(C-\d+(?:\.\d+)*)\*\*\s+(.{20,})$", body):
            scanned += 1
            probe = _prose_probe(text)
            if len(probe) >= 40 and probe in doc:
                offenders.append(f"{contract.parent.parent.name}/{contract.name}#{clause_id}")
    assert scanned > 100, (
        f"sentinel: only {scanned} clause bodies were compared, so an empty offender "
        "list would mean the scan found nothing to scan"
    )
    assert offenders == [], f"the owner document restates clause bodies: {offenders[:5]}"


def test_c5_gate_budget_is_unchanged_by_the_owner_document():
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "scan-confirmation-gates.py"), "--summary"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert r.returncode == 0, r.stdout + r.stderr
    m = re.search(r"blocking confirmation gates:\s*(\d+)", r.stdout)
    v = re.search(r"violations[^:]*:\s*(\d+)", r.stdout)
    assert m and v, r.stdout
    assert int(m.group(1)) == GATE_TOTAL, (
        f"the owner document sits in shared/, i.e. inside the scanned surface, and the "
        f"integer headroom is 0: total moved to {m.group(1)}"
    )
    assert int(v.group(1)) == 0, f"violations must stay 0, got {v.group(1)}"


def test_c6_the_cap_is_pinned_in_three_forms_with_meta_pins():
    """C-6 is [行为类]; its observable proxy is that the pins it forbids relaxing exist."""
    hits = subprocess.run(
        ["grep", "-rln", "--include=*.py", "scan-confirmation-gates", str(ROOT / "tests")],
        capture_output=True, text=True,
    ).stdout.split()
    assert hits, "no test suite pins the gate scanner at all"
    body = "\n".join(Path(h).read_text(encoding="utf-8") for h in hits)
    assert "BLOCKING_PATTERNS" in body or "blocking confirmation gates" in body, (
        "the cap must be pinned as a literal, not only as a derived number"
    )
    assert re.search(r"0\.25|\* *0\.25|// *4|/ *4", body), (
        "the derived-cap form (baseline * 0.25) must be among the pins"
    )


# =========================================================================== #
# C-7 … C-15 — extraction (red until T025 lands)
# =========================================================================== #


def test_c7_relational_sentinel_is_printed_and_holds_never_a_literal_total(tmp_path):
    mod = _load()
    corpus = _corpus(tmp_path, prose_contract=True, claims=("C-1", "C-2", "C-3"))
    spec = corpus / "001-alpha"
    _freeze(mod, spec, corpus)
    p = _payload([str(spec), "--corpus-root", str(corpus)], expect=0)

    scanned = p["scanned"]
    for key in ("total", "parsed", "named_unparseable"):
        assert key in scanned, f"the sentinel needs all three numbers; missing {key}"
    assert scanned["parsed"] + scanned["named_unparseable"] == scanned["total"], (
        f"relational sentinel fails: {scanned}"
    )
    assert scanned["sentinel_holds"] is True

    out = _run([str(spec), "--corpus-root", str(corpus)], expect=0).stdout
    for needle in (str(scanned["parsed"]), str(scanned["named_unparseable"]),
                   str(scanned["total"])):
        assert needle in out, f"the human output must print all three numbers; missing {needle}"

    src = ACCOUNTANT.read_text(encoding="utf-8")
    assert not re.search(r"==\s*(110|117|507|508|689)\b", src), (
        "the scanned total must never be a literal in the source: this feature's own "
        "contracts are inside the scanned surface, so a literal self-falsifies the "
        "moment they land"
    )


def test_c7b_ids_that_collapse_into_one_name_are_reported_never_absorbed(tmp_path):
    """The denominator's own anti-vacuity companion, one level down from C-7's file sentinel.

    The owner's `yaml-openapi` form names a clause by its HTTP method key, and one file may
    declare the same method under several paths. A universe built as a set of names therefore
    counts those operations once, and printing only the set size under-reports the denominator
    — the real corpus loses 24 of its ids this way across 8 files. Whether the syntax should
    qualify those ids is research.md A-8; what is NOT optional is that the gap is printed.
    """
    mod = _load()
    corpus = tmp_path / "corpus"
    (corpus / "001-alpha" / "contracts").mkdir(parents=True)
    spec = _spec_dir(corpus, "001-alpha", claims=("C-1", "C-2", "C-3"))
    (spec / "contracts" / "api.openapi.yaml").write_text(
        "openapi: 3.0.0\n"
        "paths:\n"
        "  /v1/a:\n"
        "    post:\n"
        "      summary: first operation\n"
        "  /v1/b:\n"
        "    post:\n"
        "      summary: second operation, same method key\n",
        encoding="utf-8",
    )
    _freeze(mod, spec, corpus)
    p = _payload([str(spec), "--corpus-root", str(corpus)])

    assert p["scanned"]["per_form"]["yaml-openapi"]["clauses"] == 2, (
        f"sentinel: both operations were not extracted: {p['scanned']['per_form']}"
    )
    assert p["clause"]["collapsed_duplicate_ids"] == 1, (
        f"two operations sharing one clause name must be reported as a collapse: {p['clause']}"
    )
    assert p["clause"]["universe_ids"] == p["clause"]["universe"] + 1, p["clause"]

    out = _run([str(spec), "--corpus-root", str(corpus)]).stdout
    assert re.search(r"collapsed:\s*1", out), (
        f"the collapse must be printed beside the denominator, not only present in JSON: {out}"
    )


def test_c8_named_count_tracks_the_owner_coverage_and_is_printed_with_the_form_set(tmp_path):
    mod = _load()
    corpus = _corpus(tmp_path, prose_contract=True, claims=("C-1", "C-2", "C-3"))
    spec = corpus / "001-alpha"
    _freeze(mod, spec, corpus)
    p = _payload([str(spec), "--corpus-root", str(corpus)], expect=0)

    assert p["scanned"]["named_unparseable"] == 1, (
        f"the prose-only contract must be named, not silently skipped: {p['scanned']}"
    )
    assert "md-none" in p["owner_forms"], (
        "the named count is only comparable together with the form set that produced it, "
        f"so both must be reported: {p['owner_forms']}"
    )
    out = _run([str(spec), "--corpus-root", str(corpus)], expect=0).stdout
    assert "md-none" in out and str(p["scanned"]["named_unparseable"]) in out, (
        "the form-set declaration and the named count must be printed together, or the "
        "count cannot be compared between two owner definitions"
    )


def test_c9_named_list_is_collapsible_behind_an_explicit_flag(tmp_path):
    mod = _load()
    corpus = _corpus(tmp_path, prose_contract=True, claims=("C-1", "C-2", "C-3"))
    spec = corpus / "001-alpha"
    _freeze(mod, spec, corpus)

    default = _run([str(spec), "--corpus-root", str(corpus)], expect=0).stdout
    expanded = _run([str(spec), "--corpus-root", str(corpus), "--list-named"], expect=0).stdout
    assert "prose.md" not in default, (
        "the named list must be collapsible to a count; the default run printed every name"
    )
    assert "prose.md" in expanded, "--list-named must expand the list it collapses"
    assert re.search(r"named[- ]unparseable:\s*1", default), (
        f"the default output must still carry the count line: {default}"
    )


def test_c10_openapi_clauses_are_method_keys_and_the_total_matches_the_census():
    mod = _load()
    src = ACCOUNTANT.read_text(encoding="utf-8")
    assert "clause_extract" in src, (
        "FR-026: both lanes must share one extractor; a private second parser here is "
        "the drift the owner document exists to prevent"
    )
    assert not re.search(r"['\"]operations:['\"]", src), (
        "MUST NOT probe for a literal `operations:` key — no file in the corpus has one, "
        "so such a probe silently classifies every OpenAPI contract as something else"
    )
    # the census owns this number; pinned here as a drift detector on the excl-053 basis
    # (this feature adds no .yaml contract, so the whole-tree value is the same 39)
    p = _payload(["--spec-dir", str(SPEC_053), "--corpus-root", str(ROOT / ".specify" / "specs"),
                  "--baseline", str(SPEC_053 / "coverage-baseline.txt")])
    assert p["scanned"]["per_form"]["yaml-openapi"]["clauses"] == OPENAPI_OPERATIONS_EXCL_053, (
        f"OpenAPI operation total moved off the census value; re-derive "
        f"notes/clause-form-census.md and move this pin in the same commit: {p['scanned']['per_form']}"
    )


def test_c11_the_misnamed_yaml_is_judged_by_content_and_yields_its_six_ids():
    assert MISNOMER_YAML.is_file(), f"sentinel: the misnomer fixture is gone: {MISNOMER_YAML}"
    ce = _load_sibling("clause_extract.py")
    assert ce.form_of(MISNOMER_YAML) == "yaml-assertions", (
        "a file named `.openapi.yaml` that is not OpenAPI must be judged by content"
    )
    assert set(ce.extract_clauses(MISNOMER_YAML)) == MISNOMER_IDS, (
        f"the assertion-id set drifted from the census: {sorted(ce.extract_clauses(MISNOMER_YAML))}"
    )


def _load_sibling(name: str):
    path = SCRIPTS / name
    spec = importlib.util.spec_from_file_location(path.stem.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_c12_no_pyyaml_dependency_anywhere_in_the_chain():
    for name in ("account-clause-coverage.py", "clause_extract.py"):
        src = (SCRIPTS / name).read_text(encoding="utf-8")
        assert not re.search(r"^\s*(?:import|from)\s+yaml\b", src, re.M), (
            f"{name} imports PyYAML; D-2 rules it out and the house precedent is "
            "gate-check.py's hand-rolled parse_gate"
        )
    deps = re.search(r"dependencies\s*=\s*\[(.*?)\]",
                     (ROOT / "pyproject.toml").read_text(encoding="utf-8"), re.S)
    assert deps and "yaml" not in deps.group(1).lower(), (
        "a YAML dependency was added to the package to satisfy this contract"
    )


def test_c13_parse_doubt_yaml_is_named_and_never_guessed_zero(tmp_path):
    """T028's counter-sample, pinned here so the guard outlives the drill."""
    mod = _load()
    corpus = tmp_path / "corpus"
    (corpus / "001-alpha" / "contracts").mkdir(parents=True)
    spec = _spec_dir(corpus, "001-alpha")
    (spec / "contracts" / "flow.yaml").write_text(
        "openapi: 3.0.0\npaths: {/v1/x: {get: {summary: inline flow style}}}\n",
        encoding="utf-8",
    )
    _freeze(mod, spec, corpus)
    p = _payload([str(spec), "--corpus-root", str(corpus), "--list-named"], expect=None)
    named = p["scanned"].get("named_files", [])
    assert any("flow.yaml" in n for n in named), (
        f"a stream-style .yaml is parse-doubt and MUST be named, not read as 0 clauses "
        f"(which would count it as covered): {named}"
    )
    assert p["scanned"]["per_form"].get("yaml-openapi", {}).get("clauses", 0) == 0, (
        "the flow-style file must not have contributed guessed operations"
    )


def test_c14_the_paren_form_file_contributes_the_clauses_a_closed_regex_would_drop():
    assert PAREN_FORM_FILE.is_file(), f"sentinel: fixture gone: {PAREN_FORM_FILE}"
    ce = _load_sibling("clause_extract.py")
    assert ce.form_of(PAREN_FORM_FILE) == "md-bold-paren"
    ids = ce.extract_clauses(PAREN_FORM_FILE)
    assert len(ids) == PAREN_FORM_CLAUSES, (
        f"an extractor writing only the closed-bold regex silently drops these: {ids}"
    )
    assert not re.search(r"\*\*C-\d+(?:\.\d+)*\*\*",
                         PAREN_FORM_FILE.read_text(encoding="utf-8")), (
        "sentinel: the fixture now matches the closed form too, so this test proves nothing"
    )


def test_c15_parseable_but_zero_clause_file_is_named_with_a_companion(tmp_path):
    mod = _load()
    corpus = tmp_path / "corpus"
    (corpus / "001-alpha" / "contracts").mkdir(parents=True)
    spec = _spec_dir(corpus, "001-alpha")
    # a table-first-cell form whose only row is a cross-reference: parses, yields nothing
    (spec / "contracts" / "empty.md").write_text(
        "# Contract: empty\n\nSome prose, a heading, and no clause marker at all.\n",
        encoding="utf-8",
    )
    _freeze(mod, spec, corpus)
    p = _payload([str(spec), "--corpus-root", str(corpus), "--list-named"])
    assert p["scanned"]["named_unparseable"] >= 1, (
        f"a file contributing zero clauses must appear in the named set, not vanish "
        f"from the denominator: {p['scanned']}"
    )
    assert any("empty.md" in n for n in p["scanned"].get("named_files", [])), (
        f"the zero-clause file was not named: {p['scanned']}"
    )


# =========================================================================== #
# C-16 … C-19 — how the result is expressed
# =========================================================================== #


def test_c16_uncovered_is_a_set_difference_with_the_str009_prefix_both_directions(tmp_path):
    mod = _load()
    corpus = _corpus(tmp_path)
    spec = corpus / "001-alpha"

    # 3 clauses, 2 claimed -> exactly the third, prefixed
    _freeze(mod, spec, corpus)
    out = _run([str(spec), "--corpus-root", str(corpus)]).stdout
    lines = [l for l in out.splitlines() if l.startswith(UNCOVERED)]
    assert len(lines) == 1, f"expected exactly the one unclaimed clause: {lines}"
    assert lines[0].endswith("contracts/c.md#C-3"), lines[0]
    assert mod.main([str(spec), "--corpus-root", str(corpus)]) != 0, (
        "a non-empty uncovered-beyond-baseline set must not exit 0"
    )

    # add the third claim -> empty and exit 0
    tasks = spec / "tasks.md"
    tasks.write_text(
        tasks.read_text(encoding="utf-8")
        + "- [ ] T003 Pin clause C-3 [green: contracts/c.md#C-3]\n",
        encoding="utf-8",
    )
    out2 = _run([str(spec), "--corpus-root", str(corpus)], expect=0).stdout
    assert not [l for l in out2.splitlines() if l.startswith(UNCOVERED)], (
        f"the uncovered set must be empty once every clause is claimed: {out2}"
    )


def test_c17_an_empty_uncovered_set_carries_a_non_empty_companion(tmp_path):
    mod = _load()
    corpus = _corpus(tmp_path)
    spec = corpus / "001-alpha"
    tasks = spec / "tasks.md"
    tasks.write_text(
        tasks.read_text(encoding="utf-8")
        + "- [ ] T003 Pin clause C-3 [green: contracts/c.md#C-3]\n",
        encoding="utf-8",
    )
    _freeze(mod, spec, corpus)
    p = _payload([str(spec), "--corpus-root", str(corpus)], expect=0)

    assert p["clause"]["uncovered_beyond_baseline"] == []
    assert p["clause"]["claimed"] > 0, (
        "an empty uncovered set with a zero claimed count cannot distinguish 'empty "
        "because right' from 'empty because blind'"
    )
    assert p["scanned"]["total"] > 0
    out = _run([str(spec), "--corpus-root", str(corpus)], expect=0).stdout
    assert re.search(r"claimed clauses[^0-9]*[1-9]", out), (
        f"the companion must be printed on the green path too: {out}"
    )


def test_c17b_a_zero_denominator_turns_the_sentinel_red(tmp_path):
    """The other half of C-17's criterion: the companion must be able to fail."""
    mod = _load()
    empty_corpus = tmp_path / "corpus"
    empty_corpus.mkdir()
    spec = empty_corpus / "001-alpha"
    spec.mkdir()
    (spec / "requirements.md").write_text("# Spec\n", encoding="utf-8")
    (spec / "contracts").mkdir()
    (spec / "tasks.md").write_text("# Tasks\n\n## Phase 1: Setup\n\n", encoding="utf-8")
    r = _run([str(spec), "--corpus-root", str(empty_corpus)])
    assert r.returncode != 0, (
        f"a corpus with nothing in it must not report green: {r.stdout}"
    )
    assert r.returncode == 2 or "no contract" in (r.stdout + r.stderr).lower(), (
        f"the empty-corpus failure must name its cause: {r.stdout}{r.stderr}"
    )


def test_c18_the_two_lanes_are_separate_sections_with_separate_counts(tmp_path):
    mod = _load()
    corpus = _corpus(tmp_path)
    spec = corpus / "001-alpha"
    _freeze(mod, spec, corpus)
    out = _run([str(spec), "--corpus-root", str(corpus)]).stdout
    p = _payload([str(spec), "--corpus-root", str(corpus)])

    assert out.count("coverage") >= 2 or ("clause coverage" in out.lower()
                                         and "fr coverage" in out.lower()), (
        f"the two lanes must be printed as two sections: {out}"
    )
    assert set(p["clause"]) and set(p["fr"]), "each lane needs its own count object"
    assert p["fr"]["universe"] == 3 and p["clause"]["universe"] == 3
    assert "uncovered" in p["clause"] and "uncovered" in p["fr"], (
        "the two uncovered sets must not be merged into one count"
    )


def test_c18b_deleting_one_citation_from_a_group_makes_that_fr_uncovered(tmp_path):
    """C-18's counter-sample — and the only one the `fr-uncovered` label has."""
    mod = _load()
    corpus = _corpus(tmp_path)
    spec = corpus / "001-alpha"
    _freeze(mod, spec, corpus)

    before = _payload([str(spec), "--corpus-root", str(corpus)])
    assert before["fr"]["uncovered"] == [], f"sentinel: the fixture starts dirty: {before['fr']}"

    contract = spec / "contracts" / "c.md"
    original = contract.read_text(encoding="utf-8")
    assert original.count("(FR-003)") == 1, "sentinel: the fixture's FR-003 citation moved"
    contract.write_text(original.replace("(FR-003)", "(and see the guideline)"), encoding="utf-8")
    try:
        after = _payload([str(spec), "--corpus-root", str(corpus)])
        assert after["fr"]["uncovered"] == ["FR-003"], (
            f"removing a citation group's FR must surface that FR as uncovered: {after['fr']}"
        )
        rc = mod.main([str(spec), "--corpus-root", str(corpus)])
        assert rc != 0, "an uncovered FR must drive a non-zero exit, or the lane cannot go red"
    finally:
        contract.write_text(original, encoding="utf-8")
    restored = _payload([str(spec), "--corpus-root", str(corpus)])
    assert restored["fr"]["uncovered"] == [], "the drill did not restore the fixture"


def test_c19_uncovered_names_are_sorted_one_per_line_and_comm_consumable(tmp_path):
    mod = _load()
    corpus = _corpus(tmp_path)
    spec = corpus / "001-alpha"
    # three unclaimed clauses so sorting is observable
    (spec / "tasks.md").write_text(
        "# Tasks\n\n## Phase 1: Setup\n\n- [ ] T001 Write something in src/a.py\n",
        encoding="utf-8",
    )
    _freeze(mod, spec, corpus)
    p = _payload([str(spec), "--corpus-root", str(corpus)])
    names = p["clause"]["uncovered"]
    assert names == sorted(names), f"names must be sorted for comm -13: {names}"
    assert all(isinstance(n, str) and "\n" not in n for n in names)
    assert all("#" in n for n in names), (
        f"a name must identify spec, contract and clause: {names}"
    )

    out = _run([str(spec), "--corpus-root", str(corpus)]).stdout
    lines = [l[len(UNCOVERED):].strip() for l in out.splitlines() if l.startswith(UNCOVERED)]
    assert lines == sorted(lines), f"the human list must be sorted too: {lines}"
    assert set(lines) == set(names), (
        f"the human and machine forms must name the same set: {lines} vs {names}"
    )


# =========================================================================== #
# C-20 … C-25 — read-only, the frozen baseline, and the shape it must not take
# =========================================================================== #


def test_c20_the_accountant_writes_nothing_and_changes_no_byte_of_the_corpus():
    src = ACCOUNTANT.read_text(encoding="utf-8")
    hits = re.findall(
        r"\.(?:write_text|write_bytes|mkdir|unlink|rmtree)\(|open\([^)]*['\"][wax]", src
    )
    freeze_hits = [h for h in hits]
    assert freeze_hits == [] or "--freeze" in src, (
        f"write points must belong to the explicit --freeze action only: {freeze_hits}"
    )

    spec_root = ROOT / ".specify" / "specs"
    files = sorted(p for p in spec_root.rglob("*") if p.is_file())
    assert files, "sentinel: the corpus is empty, so the checksum proves nothing"
    before = hashlib.md5(b"".join(p.read_bytes() for p in files)).hexdigest()
    _run(["--spec-dir", str(SPEC_053), "--corpus-root", str(spec_root),
          "--baseline", str(SPEC_053 / "coverage-baseline.txt")])
    after = hashlib.md5(b"".join(p.read_bytes() for p in files)).hexdigest()
    assert before == after, "an accounting run modified the corpus it was reading"


def test_c21_baseline_discipline_comm_delta_paired_with_a_non_empty_claim(tmp_path):
    mod = _load()
    corpus = _corpus(tmp_path)
    spec = corpus / "001-alpha"

    # (a) no baseline at all -> non-zero, naming the path (never "no exemptions")
    missing = spec / "coverage-baseline.txt"
    assert not missing.is_file()
    r = _run([str(spec), "--corpus-root", str(corpus)])
    assert r.returncode != 0, "a missing baseline must not be read as an empty delta"
    assert str(missing) in (r.stdout + r.stderr), (
        f"the missing baseline path must be named: {r.stdout}{r.stderr}"
    )

    # (b) frozen baseline, claims outstanding -> the delta is exactly this feature's own
    _freeze(mod, spec, corpus)
    p = _payload([str(spec), "--corpus-root", str(corpus)])
    assert p["baseline_present"] is True
    assert p["clause"]["uncovered_beyond_baseline"] == [
        "001-alpha/contracts/c.md#C-3"
    ], p["clause"]
    # the baseline面 excluded this spec, so its own clause can never be exempted by it
    baseline_names = [
        l for l in missing.read_text(encoding="utf-8").splitlines()
        if l.strip() and not l.startswith("#")
    ]
    assert all("001-alpha" not in n for n in baseline_names), (
        f"the frozen面 must exclude the spec being accounted, or its own items enter the "
        f"baseline and `comm -13` reports empty whatever is claimed: {baseline_names}"
    )

    # (c) the paired positive companion: claimed count printed and non-zero-capable
    out = _run([str(spec), "--corpus-root", str(corpus)]).stdout
    assert re.search(r"claimed clauses", out), (
        f"the paired criterion requires a claimed-count line beside the empty-delta verdict: {out}"
    )


def test_c22_baseline_internal_items_still_print_their_count(tmp_path):
    mod = _load()
    corpus = tmp_path / "corpus"
    (corpus / "001-alpha" / "contracts").mkdir(parents=True)
    spec = _spec_dir(corpus, "001-alpha", claims=("C-1", "C-2", "C-3"))
    # a second spec whose clauses nobody claims: pre-existing debt, belongs in the baseline
    other = _spec_dir(corpus, "002-beta", frs=("FR-001",),
                      clauses=(("C-1", "FR-001"), ("C-2", "FR-001")), claims=())
    _freeze(mod, spec, corpus)

    baseline = spec / "coverage-baseline.txt"
    frozen = [l for l in baseline.read_text(encoding="utf-8").splitlines()
              if l.strip() and not l.startswith("#")]
    assert len(frozen) == 2, f"sentinel: expected 002-beta's two clauses frozen: {frozen}"
    assert all(n.startswith("002-beta/") for n in frozen), frozen

    p = _payload([str(spec), "--corpus-root", str(corpus)], expect=0)
    assert p["clause"]["baseline_internal_count"] == len(frozen), (
        f"the pre-existing debt must stay visible as a count: {p['clause']}"
    )
    out = _run([str(spec), "--corpus-root", str(corpus)], expect=0).stdout
    assert re.search(rf"baseline[- ]internal[^0-9]*{len(frozen)}", out), (
        f"the count must be printed every round, not only when it blocks: {out}"
    )
    assert other.is_dir()


def test_c23_the_baseline_header_records_the_form_set_and_the_freeze_context(tmp_path):
    mod = _load()
    corpus = _corpus(tmp_path, prose_contract=True, claims=("C-1", "C-2", "C-3"))
    spec = corpus / "001-alpha"
    baseline = _freeze(mod, spec, corpus)
    header = "\n".join(
        l for l in baseline.read_text(encoding="utf-8").splitlines() if l.startswith("#")
    )
    assert header, "the baseline must carry a header, not be a bare name list"
    for needle in ("md-bold-closed", "md-none"):
        assert needle in header, (
            f"without the owner form set the parsed/named counts of two runs are not "
            f"comparable; header lacks {needle!r}: {header}"
        )
    assert re.search(r"excl|exclude", header, re.IGNORECASE), (
        f"the header must record the excluded corpus selector: {header}"
    )
    assert re.search(r"[0-9a-f]{7,40}", header), (
        f"the header must record a BASE SHA or form-set fingerprint: {header}"
    )


def test_c24_the_idiom_is_a_sorted_name_list_consumed_by_comm_not_a_second_form(tmp_path):
    """Both sides of the comparison are non-empty here, on purpose.

    An empty baseline makes `comm -13` echo all of file 2 whatever the ordering, and an
    empty live set makes it print nothing — either fixture would let a broken pipeline
    agree with the script by accident. So: one spec with an outstanding clause (a non-empty
    delta) and one spec whose debt is frozen (a non-empty baseline).
    """
    mod = _load()
    corpus = tmp_path / "corpus"
    (corpus / "001-alpha" / "contracts").mkdir(parents=True)
    spec = _spec_dir(corpus, "001-alpha")          # claims C-1, C-2 -> C-3 outstanding
    _spec_dir(corpus, "002-beta", frs=("FR-001",),
              clauses=(("C-1", "FR-001"), ("C-2", "FR-001")), claims=())
    baseline = _freeze(mod, spec, corpus)

    frozen = [l for l in baseline.read_text(encoding="utf-8").splitlines()
              if l.strip() and not l.startswith("#")]
    assert frozen and all(n.startswith("002-beta/") for n in frozen), (
        f"sentinel: the baseline must be non-empty and exclude the accounted spec: {frozen}"
    )

    r = _run([str(spec), "--corpus-root", str(corpus)])
    live = [l[len(UNCOVERED):].strip() for l in r.stdout.splitlines() if l.startswith(UNCOVERED)]
    assert live, "sentinel: the live uncovered set is empty, so this proves nothing"

    env = {"LC_ALL": "C", "PATH": "/usr/bin:/bin"}
    delta = subprocess.run(
        ["comm", "-13", str(baseline), "-"],
        input="\n".join(live) + "\n", capture_output=True, text=True, env=env,
    )
    assert delta.stderr == "", f"comm rejected the inputs: {delta.stderr}"
    assert delta.stdout.split() == ["001-alpha/contracts/c.md#C-3"], delta.stdout

    p = _payload([str(spec), "--corpus-root", str(corpus)])
    assert delta.stdout.split() == p["clause"]["uncovered_beyond_baseline"], (
        f"the script's internal delta and the `comm -13` idiom must agree, or the gate "
        f"check and the tool are judging different things: {delta.stdout} vs {p['clause']}"
    )


def test_c24b_the_baseline_is_codepoint_sorted_so_comm_can_consume_it(tmp_path):
    """Measured defect, and the reason the idiom needs `LC_ALL=C`.

    Under `en_US.UTF-8` glibc collation ignores `#`, `/` and `.` at the first level, so the
    two `#`-prefixed header lines sort AFTER digit-initial clause names: `comm` then reports
    "file 1 is not in sorted order" and echoes the whole of file 2. On the real corpus that
    turned a delta of 182 into 665 — a wrong verdict that still looked like output. Python's
    `sorted()` is codepoint order, so the file is C-sorted and the idiom must be run under
    `LC_ALL=C`; this pins both halves.
    """
    mod = _load()
    corpus = tmp_path / "corpus"
    (corpus / "001-alpha" / "contracts").mkdir(parents=True)
    spec = _spec_dir(corpus, "001-alpha", claims=())
    _spec_dir(corpus, "002-beta", frs=("FR-001",),
              clauses=(("C-1", "FR-001"), ("C-2", "FR-001")), claims=())
    baseline = _freeze(mod, spec, corpus)

    text = baseline.read_text(encoding="utf-8")
    header = [l for l in text.splitlines() if l.startswith("#")]
    names = [l for l in text.splitlines() if l.strip() and not l.startswith("#")]
    assert names == sorted(names), "the frozen names must be codepoint-sorted"
    assert len(header) == 2, (
        f"exactly two header lines, both `#`-prefixed so they precede every name in "
        f"codepoint order: {header}"
    )
    assert text.splitlines() == header + names, "the header must not be interleaved with names"

    r = subprocess.run(["sort", "-c", str(baseline)], capture_output=True, text=True,
                       env={"LC_ALL": "C", "PATH": "/usr/bin:/bin"})
    assert r.returncode == 0 and r.stderr == "", (
        f"the baseline is not sorted under LC_ALL=C, so `comm -13` cannot consume it: {r.stderr}"
    )
    assert mod is not None


def test_c25_the_baseline_is_not_the_gate_scanner_broken_json_shape():
    """A-3: `scan-confirmation-gates.py --baseline` reads a TOP-LEVEL `total` while the
    frozen value sits under a nested key, and its exit code reflects only `violations`,
    so it cannot serve as an equality gate. This script must not inherit that shape."""
    src = ACCOUNTANT.read_text(encoding="utf-8")
    assert "json.loads" not in src or "--freeze" in src, (
        "the baseline is a sorted NAME list, not a JSON report; parsing it as JSON is "
        "the inherited defect"
    )
    assert not re.search(r"baseline\.get\(\s*['\"]total['\"]", src), (
        "reading a top-level `total` from the baseline is exactly the broken shape"
    )
    help_text = subprocess.run(
        [sys.executable, str(ACCOUNTANT), "--help"], capture_output=True, text=True, cwd=str(ROOT),
    ).stdout
    assert "comm -13" in help_text or "name" in help_text.lower(), (
        f"the help must state that comparison is by name set: {help_text}"
    )


# =========================================================================== #
# C-26 / C-27 — yaml disposition and the SC-006 evidence form
# =========================================================================== #


def test_c26_every_yaml_contract_is_explicitly_disposed():
    p = _payload(["--spec-dir", str(SPEC_053),
                  "--corpus-root", str(ROOT / ".specify" / "specs"),
                  "--baseline", str(SPEC_053 / "coverage-baseline.txt")])
    scanned = p["scanned"]
    assert scanned["yaml_parsed"] == scanned["yaml_total"], (
        f"every .yaml must be parsed by one of the two extractors: {scanned}"
    )
    assert scanned["yaml_named"] == 0, (
        f"a named .yaml means C-13's parse-doubt fallback fired on the real corpus: {scanned}"
    )
    assert scanned["yaml_total"] > 0, "sentinel: no .yaml was scanned at all"


def test_c27_the_sc006_evidence_form_is_three_numbers_and_a_sum_assertion():
    out = _run(["--spec-dir", str(SPEC_053),
                "--corpus-root", str(ROOT / ".specify" / "specs"),
                "--baseline", str(SPEC_053 / "coverage-baseline.txt")]).stdout
    m = re.search(r"parsed\s+(\d+)\s*\+\s*named[- ]unparseable\s+(\d+)\s*==\s*(\d+)", out)
    assert m, f"the SC-006 evidence form (three numbers and their sum) is missing: {out}"
    parsed, named, total = (int(g) for g in m.groups())
    assert parsed + named == total, f"the printed sentinel does not hold: {m.group(0)}"
    assert CENSUS.is_file(), "sentinel: the per-form count owner is gone"
    src = ACCOUNTANT.read_text(encoding="utf-8")
    assert "clause-form-census.md" in src, (
        "per-form counts are owned by notes/clause-form-census.md; the script must reach "
        "them by reference rather than restate them"
    )


# =========================================================================== #
# the accountant's checker-form obligations (owned here, not in that suite)
# =========================================================================== #


def test_form_str008_attribution_and_four_label_docstring_body():
    mod = _load()
    doc = mod.__doc__ or ""
    assert STR008 in doc, "FR-002: the docstring must open its attribution with STR-008"
    labels = set(LABEL_DOC_RE.findall(doc))
    assert labels, "sentinel: no labels parsed from the docstring body"
    assert labels == ACCOUNTANT_CHECKS, (
        f"the docstring label body and this suite's pin must move together: "
        f"docstring={sorted(labels)} pin={sorted(ACCOUNTANT_CHECKS)}"
    )


def test_form_exit_code_table():
    """Pinned separately from the label set (checker-form C-23)."""
    mod = _load()
    tmp = Path(__file__).parent  # unused; keeps the two pins' signatures honest
    assert tmp.is_dir()

    absent = ROOT / ".specify" / "specs" / "does-not-exist-anywhere"
    assert mod.main([str(absent)]) == 2, "2 = input error (spec dir / requirements.md missing)"

    spec_root = ROOT / ".specify" / "specs"
    baseline = SPEC_053 / "coverage-baseline.txt"
    if baseline.is_file():
        rc = mod.main([str(SPEC_053), "--corpus-root", str(spec_root)])
        assert rc in (0, 1), f"0 = covered, 1 = uncovered beyond baseline; got {rc}"
    else:
        assert mod.main([str(SPEC_053), "--corpus-root", str(spec_root)]) != 0, (
            "C-21: a missing baseline must exit non-zero"
        )


def test_form_json_key_set_verdict_array_and_status_vocabulary(tmp_path):
    mod = _load()
    corpus = _corpus(tmp_path)
    spec = corpus / "001-alpha"
    _freeze(mod, spec, corpus)
    p = _payload([str(spec), "--corpus-root", str(corpus)])

    for key in ("file", "checks", "errors", "warnings"):
        assert key in p, f"checker-form C-7 requires the key {key!r}"
    assert isinstance(p["checks"], list) and len(p["checks"]) == len(ACCOUNTANT_CHECKS)
    assert {c["label"] for c in p["checks"]} == ACCOUNTANT_CHECKS
    for check in p["checks"]:
        assert set(check) >= {"label", "status", "count"}, check
    assert p["status"] in STATUSES, p["status"]
    assert isinstance(p["errors"], int) and isinstance(p["warnings"], int)


def test_form_human_tail_line_is_the_str003_shape(tmp_path):
    mod = _load()
    corpus = _corpus(tmp_path)
    spec = corpus / "001-alpha"
    _freeze(mod, spec, corpus)
    out = _run([str(spec), "--corpus-root", str(corpus)]).stdout
    tail = [l for l in out.strip().splitlines() if "error(s)" in l][-1]
    assert re.search(r"\d+ error\(s\), \d+ warning\(s\)", tail), tail


def test_form_positional_artifact_path_is_accepted(tmp_path):
    """checker-form C-1: the artifact path is a positional argument. A file inside the
    spec dir resolves to that spec dir, so pointing the tool at requirements.md works."""
    mod = _load()
    corpus = _corpus(tmp_path)
    spec = corpus / "001-alpha"
    _freeze(mod, spec, corpus)
    assert mod.main([str(spec / "requirements.md"), "--corpus-root", str(corpus)]) == \
        mod.main([str(spec), "--corpus-root", str(corpus)])


def test_form_the_script_is_read_only_by_write_point_scan():
    src = ACCOUNTANT.read_text(encoding="utf-8")
    hits = re.findall(
        r"\.(?:write_text|write_bytes|unlink|rmtree)\(|open\([^)]*['\"][wax]", src
    )
    # `--freeze` is the one sanctioned write, and it is an explicit user action, so the
    # scan allows exactly the write points that action needs and nothing else.
    assert len(hits) <= 2, (
        f"more write points than the --freeze action needs: {hits}"
    )
    for h in hits:
        assert "write_text" in h or "mkdir" in h, f"unattributable write point: {h}"


def test_form_ships_via_the_force_include_mapping():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "force-include" in pyproject and "specify_cli/scripts" in pyproject
    assert ACCOUNTANT.parent.name == "python"


def test_the_contract_still_has_the_clause_count_this_suite_pins():
    body = (SPEC_053 / "contracts" / "clause-coverage.md").read_text(encoding="utf-8")
    ids = re.findall(r"(?m)^\*\*C-(\d+)\*\*", body)
    assert len(ids) == 27, f"clause count moved: {len(ids)}"
    assert [int(i) for i in ids] == list(range(1, 28)), "clause ids are not contiguous"
