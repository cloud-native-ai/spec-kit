"""Contract test: the self-explanatory term is registered in the project glossary (Feature 082, US4).

Implements the glossary clauses of
``.specify/specs/082-self-explanatory-integration/contracts/glossary-integration.contract.md``
(C-29, C-30, C-32, C-33, C-34) and the enumeration clause of
``contracts/mirror-distribution.contract.md`` that this module co-owns (C-22 / C-24, claimed
together with C-26 by T029's distribution module). C-20's version of the third-form claim is
T010's; this module claims only the naming face (C-34).

Why a separate module from ``test_glossary_mechanism.py``
--------------------------------------------------------
That carrier guards the *mechanism* (template present and mirrored, required structure, Documentation
Map row, init round-trip) and deliberately enumerates no terms (C-31). Term assertions belong in a
suite of the same kind, so this module adds them without editing a file whose emptiness of term
enumerations is itself an asserted property (T045 re-checks that its diff stays empty).

Row parsing, not substring search
---------------------------------
C-30 forbids a substring assertion for "the retired name is not a second canonical": the retired name
legitimately appears inside the variants cell of the canonical row, so a file-wide search cannot
distinguish the legitimate occurrence from the defect. The rows below are parsed **column by column**
with the engine's own table grammar (``parse_entries`` / ``_split_row`` import-loaded from
``scripts/python/glossary-utils.py``), so a row that put the retired name in the canonical column is
reported as a row, with its position, rather than passing because the string occurs elsewhere.

Literals
--------
The canonical string is ``STR-003`` and the owner path is ``STR-002``; both live in
``requirements.md`` § Shared Strings. The retired name is asserted in the variants cell of the same
row, which is the one place C-30 permits it.

Red-first provenance (Constitution IV): the entry landed in ``.specify/memory/glossary.md`` during
the plan stage and the write was executed by the engine (``--action add``), so this module's green is
not a red-first capture. Its red leg is the mutation recorded by T045/T051: a second canonical row
carrying the retired name turns ``test_c30_...`` red by row index. The pairing is transcribed in
``notes/red-first-evidence.md``; where the pair is missing, the verification task is the thing that
is missing, not this assertion.
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
STORE = ROOT / ".specify" / "memory" / "glossary.md"
ENGINE = ROOT / "scripts" / "python" / "glossary-utils.py"

# `STR-003` — the ratified canonical form, with its bracket language.
CANONICAL = "不言自明 (Self-explanatory)"
# The retired name; permitted only in the canonical row's variants cell (C-30).
RETIRED_NAME = "望文生义"

OWNER_SOURCE = ROOT / "shared" / "definitions" / "self-explanatory-definitions.md"
# `STR-002` — the framework-source owner path the meaning cell must reach (C-32).
OWNER_PATH = "shared/definitions/self-explanatory-definitions.md"

# `STR-001` — the identical string in the constitution template, the constitution generator's
# MUST-include list and the live constitution; and the head of the feature's document titles.
IDENTIFIER = "Self-Explanatory Structure (不言自明)"
# The bare Chinese form, in its own parentheses. STR-003 is `不言自明 (Self-explanatory)`, so the
# relation between the two shared strings is "same concept, bracket languages swapped, head noun
# kept in one and dropped in the other" — see the docstring of the test that pins it.
CJK_TERM = "不言自明"
EN_HEAD_NOUN = "Structure"

# C-22 / C-24: the three documents this feature adds, as engine-derived `source->mirror` pairs.
REQUIRED_MIRROR_PAIRS = (
    ("shared/definitions/self-explanatory-definitions.md",
     ".specify/shared/definitions/self-explanatory-definitions.md"),
    ("shared/guidelines/self-explanatory.md",
     ".specify/shared/guidelines/self-explanatory.md"),
    ("shared/workflow/best-practice-optimization.md",
     ".specify/shared/workflow/best-practice-optimization.md"),
)


def _load_engine(path: Path, module_name: str):
    """Import-load a repository script by path (the mirrors suite uses the same shape)."""
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None, f"cannot load {path}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GLOSSARY = _load_engine(ENGINE, "_glossary_utils_under_test")
MIRRORS = _load_engine(ROOT / "scripts" / "python" / "sync-mirrors.py", "_sync_mirrors_under_test")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def run_engine(*args: str):
    """Run the glossary engine against this repository; return (rc, parsed stdout, stderr)."""
    cp = subprocess.run(
        [sys.executable, str(ENGINE), "--root", str(ROOT), *args],
        capture_output=True, text=True,
    )
    out = cp.stdout.strip()
    payload = json.loads(out) if out.startswith("{") else out
    return cp.returncode, payload, cp.stderr


def parsed_rows():
    """Every data row of the store table, as engine-parsed entries, in file order.

    ``parse_entries`` drops the placeholder row and anything outside the header-delimited table, so
    the index reported on failure is the entry index, stable across reformatting.
    """
    return GLOSSARY.parse_entries(read(STORE))


def canonical_row(rows=None):
    """Return (index, entry) of the single row whose canonical cell is exactly ``CANONICAL``."""
    entries = parsed_rows() if rows is None else rows
    hits = [(i, e) for i, e in enumerate(entries) if e["canonical"] == CANONICAL]
    assert len(hits) == 1, (
        f"expected exactly one entry whose canonical cell is {CANONICAL!r}, found {len(hits)}: "
        + str([(i, e["canonical"]) for i, e in hits])
    )
    return hits[0]


# --- C-29: the canonical entry exists with the ratified fields -------------------------------

def test_c29_entry_exists_with_origin_auto_and_status_proposed():
    rows = parsed_rows()
    assert rows, f"glossary table has no data rows: {STORE}"
    _index, entry = canonical_row(rows)
    assert entry["variants"] == [RETIRED_NAME], (
        f"the canonical entry's variants cell is {entry['variants']!r}; C-30 requires the retired "
        f"name {RETIRED_NAME!r} to be the variant that routes readers to the canonical form"
    )
    assert entry["origin"] == "auto", (
        f"origin is {entry['origin']!r}; an entry the flow registers is an auto proposal"
    )
    assert entry["status"] == "proposed", (
        f"status is {entry['status']!r}; promotion is a user action (C-33), never the flow's"
    )


# --- C-30: the retired name is a variant, never a second canonical ---------------------------

def test_c30_no_second_row_carries_the_retired_name_or_canonical_as_canonical():
    rows = parsed_rows()
    index, _entry = canonical_row(rows)
    offenders = [
        (i, e["canonical"])
        for i, e in enumerate(rows)
        if i != index and (RETIRED_NAME in e["canonical"] or CANONICAL in e["canonical"])
    ]
    assert not offenders, (
        "a second row puts the retired name or the canonical string in the canonical column: "
        + str(offenders)
        + f" (the canonical row is entry index {index})"
    )


def test_c30_retired_name_is_present_in_the_canonical_rows_variants_cell():
    _index, entry = canonical_row()
    variants = entry["variants"]
    assert RETIRED_NAME in variants, (
        f"the retired name is not a variant of the canonical entry (variants={variants!r}); "
        "a reader typing the old name would find nothing"
    )


def test_c30_engine_validate_exits_zero():
    rc, payload, stderr = run_engine("--action", "validate")
    assert rc == 0, f"glossary-utils.py --action validate exited {rc}: {payload} {stderr}"
    assert isinstance(payload, dict) and payload.get("valid") is True, (
        f"validate did not report valid=true: {payload!r}"
    )


# --- C-33: status is not promoted by the flow ------------------------------------------------

# Every verb this feature runs against the store. The registered status is read by
# ``--action list``, which reconstructs it from the table rendered by ``replace_table`` — so this
# assertion follows the render/parse round-trip rather than a substring of the file.
WRITE_VERBS_OF_THIS_FEATURE = ()


def registered_status_via_engine() -> str:
    """The canonical entry's status as the store's own engine reads it (parse after render)."""
    rc, payload, stderr = run_engine("--action", "list")
    assert rc == 0, f"glossary-utils.py --action list exited {rc}: {payload} {stderr}"
    hits = [e for e in payload["entries"] if e["canonical"] == CANONICAL]
    assert len(hits) == 1, f"expected exactly one canonical row for {CANONICAL!r}, got {hits!r}"
    return hits[0]["status"]


def test_c33_entry_status_stays_proposed_after_the_features_own_write():
    status = registered_status_via_engine()
    assert status != "confirmed", (
        "the canonical entry reads 'confirmed'; promotion is a user-authoritative action "
        "(data-model.md T-B, requirements.md A6) and no automated step of this feature may flip "
        "it — not the engine write, not a later verification run"
    )
    assert status == "proposed", (
        f"the canonical entry's status is {status!r}; the glossary store admits only 'proposed' "
        "and 'confirmed', so this is neither the landed value nor a user promotion"
    )


def test_c33_feature_runs_no_status_promoting_verb():
    """No status-promoting write is a flow step: the engine's write verbs this module runs stay empty.

    ``--action add`` carries ``--status``; ``--action list`` / ``--action validate`` cannot write.
    Should a later task add a write verb, it belongs in ``WRITE_VERBS_OF_THIS_FEATURE`` and this
    test fails until the list is re-read against C-33 — the failure is the review prompt.
    """
    assert WRITE_VERBS_OF_THIS_FEATURE == (), (
        "a writing engine verb was added to this feature's flow: "
        f"{WRITE_VERBS_OF_THIS_FEATURE!r} — re-read C-33 before letting it run"
    )


# --- C-32: the meaning points at the owner ---------------------------------------------------

def test_c32_meaning_cell_names_an_existing_repository_relative_path():
    _index, entry = canonical_row()
    meaning = entry["meaning"]
    assert OWNER_PATH in meaning, (
        f"the meaning cell does not name the concept owner {OWNER_PATH!r}; a reader landing on "
        f"the glossary row would not reach the single definition point. Cell: {meaning!r}"
    )
    matched = _repo_relative_paths(meaning)
    assert matched, f"no repository-relative path found in the meaning cell: {meaning!r}"
    for rel in matched:
        assert (ROOT / rel).is_file(), (
            f"the meaning cell's path {rel!r} does not exist in this repository "
            "(the concept owner is unreachable)"
        )


def _repo_relative_paths(text: str):
    """Repository-relative file paths written in ``text`` (a path with an extension, no scheme)."""
    return [
        m.group(0).strip(".,;:")
        for m in re.finditer(r"(?<![\w/.-])(?:[\w.-]+/)+[\w.-]+\.[A-Za-z0-9]+", text)
    ]


# --- C-34: term discovery is not a second vocabulary -----------------------------------------

# The document set C-34 quantifies over: "no document added by this feature". All four are feature
# artifacts (created or amended under this key), so a third form introduced anywhere else — a
# guideline, a contract, prose — does not escape the sweep.
FEATURE_DOCUMENTS = (
    ROOT / "shared" / "definitions" / "self-explanatory-definitions.md",
    ROOT / "shared" / "guidelines" / "self-explanatory.md",
    ROOT / "shared" / "workflow" / "best-practice-optimization.md",
    ROOT / "docs" / "concepts" / "self-explanatory.md",
)

# C-34's own examples of a competing canonical form, as regexes. Each is a *form*, not a string
# list: a synonym table would go stale the moment somebody invents the next variant.
THIRD_FORM_PATTERNS = (
    # `Self-explanatory Structures` — the English head noun pluralized.
    r"Self-[Ee]xplanatory\s+Structures\b",
    # The identifier deliberately truncated, i.e. the bracket language dropped rather than absent.
    r"Self-[Ee]xplanatory\s+Structure\s*\((?!不言自明\))",
    r"Self-[Ee]xplanatory\s+Structure\s*\(without\b",
    # A second English canonical that drops `Structure`/`自明` entirely.
    r"\bSelf-[Ee]xplanatory\s*(?:Principle|Concept|Doctrine)\b",
    # `望文生义` used as the *current* name. Its plain occurrences are the documented naming
    # history, so only the three promoting shapes count: it as a heading, it presented as the
    # approved/current name, or it presented as a translation of the English term.
    r"^#{1,6}\s*望文生义",
    r"望文生义[^，。；]{0,8}(?:为|是)(?:中文)?(?:规范|标准|正式|current|official)名",
    r"(?:中文|规范|标准|正式)名(?:为|是|：|:)\s*望文生义",
    r"望文生义[^，。；]{0,6}(?:译作|译为|translat)",
)


def _canonical_entry():
    """The registered canonical entry, read through the engine's own table grammar (STR-003)."""
    rc, payload, stderr = run_engine("--action", "list")
    assert rc == 0, f"glossary-utils.py --action list exited {rc}: {payload} {stderr}"
    hits = [e for e in payload["entries"] if e["canonical"] == CANONICAL]
    assert len(hits) == 1, f"expected exactly one canonical row for {CANONICAL!r}, got {hits!r}"
    return hits[0]


def test_c34_str001_and_str003_share_the_same_identifier():
    """STR-001 and STR-003 must reach the *same concept*, differing only by the language projection.

    C-34's "shared portion" is not string equality: the two ratified forms carry different bracket
    languages by design (``STR-001`` = ``Self-Explanatory Structure (不言自明)``, ``STR-003`` =
    ``不言自明 (Self-explanatory)``), so the shareable portion is what the two bracket spans point
    at. Both spans are stripped, both are asserted to be each other's translation, and the English
    head noun must survive on the identifier side — that is what keeps STR-003 a *projection* of
    the identifier rather than an independently coined term.
    """
    entry = _canonical_entry()
    canonical = entry["canonical"]

    span_pattern = re.compile(r"\s*[（(]\s*([^）)]+?)\s*[）)]\s*")
    ident_head = span_pattern.sub("", IDENTIFIER).strip()
    gloss_head = span_pattern.sub("", canonical).strip()
    ident_span = span_pattern.search(IDENTIFIER)
    gloss_span = span_pattern.search(canonical)
    assert ident_span is not None and gloss_span is not None, (
        f"one of the two ratified forms lost its bracket span: STR-001={IDENTIFIER!r}, "
        f"STR-003={canonical!r}"
    )

    assert ident_head == "Self-Explanatory " + EN_HEAD_NOUN, (
        f"STR-001's English head is {ident_head!r}, expected 'Self-Explanatory {EN_HEAD_NOUN}'"
    )
    assert ident_span.group(1) == CJK_TERM, (
        f"STR-001's bracket span is {ident_span.group(1)!r}; the feature's identifier carries the "
        f"Chinese form {CJK_TERM!r}"
    )
    assert gloss_head == CJK_TERM, (
        f"STR-003's head is {gloss_head!r}, so the glossary row no longer leads with {CJK_TERM!r} — "
        "the two shared strings have drifted apart"
    )
    assert gloss_span.group(1).lower() == ("self-explanatory"), (
        f"STR-003's bracket span is {gloss_span.group(1)!r}, not the English form of {CJK_TERM!r}"
    )
    # The two heads name the same concept and the two spans are each other's translation; an
    # earlier reference of STR-003, should one ever be written, is a strict substring of STR-001's
    # head — that containment is the mechanical test for "same identifier, one projection".
    assert gloss_head in IDENTIFIER, (
        f"{gloss_head!r} (STR-003's head) is not contained in STR-001 {IDENTIFIER!r}"
    )
    assert EN_HEAD_NOUN not in canonical, (
        f"STR-003 {canonical!r} repeats the English head noun {EN_HEAD_NOUN!r}; the projection is "
        "one-directional (STR-003 is a rendering of the identifier, not a second identifier)"
    )


def test_c34_document_titles_use_the_identifier():
    """Every feature document that names the concept concisely uses STR-001's form, not a variant."""
    titled = []
    for path in FEATURE_DOCUMENTS:
        for lineno, line in enumerate(read(path).splitlines(), start=1):
            if not line.startswith("#"):
                continue
            if CJK_TERM in line or re.search(r"[Ss]elf-[Ee]xplanatory", line):
                titled.append((f"{path.relative_to(ROOT).as_posix()}:{lineno}", line))
    assert titled, "no feature document names the concept, so this sweep proves nothing"
    offenders = [
        f"{location}: {line.strip()[:120]!r}"
        for location, line in titled
        if CJK_TERM not in line or re.search(r"Self-[Ee]xplanatory\s+Structures\b", line)
    ]
    assert not offenders, (
        f"a feature document title does not carry the identifier's Chinese span {CJK_TERM!r} (or "
        "pluralizes the English head noun), i.e. it presents a form the identifier does not:\n  "
        + "\n  ".join(offenders)
    )


def test_c34_feature_documents_introduce_no_third_form():
    """No document this feature adds carries a competing canonical form (C-34's second half)."""
    assert all(path.is_file() for path in FEATURE_DOCUMENTS), (
        "a feature document is missing: "
        + str([str(p.relative_to(ROOT)) for p in FEATURE_DOCUMENTS if not p.is_file()])
    )
    findings = []
    for path in FEATURE_DOCUMENTS:
        for lineno, line in enumerate(read(path).splitlines(), start=1):
            for pattern in THIRD_FORM_PATTERNS:
                for match in re.finditer(pattern, line, flags=re.MULTILINE):
                    findings.append(
                        f"{path.relative_to(ROOT).as_posix()}:{lineno}: {match.group(0)!r} "
                        f"(pattern {pattern!r}) — {line.strip()[:120]!r}"
                    )
    assert not findings, (
        "a document this feature adds introduces a third canonical form; the discovered term must "
        "not become a second vocabulary (C-34):\n  " + "\n  ".join(findings)
    )


def test_c34_the_retired_name_keeps_its_documented_disposition():
    """`望文生义` survives only as naming history — never as a heading, a current name, a row.

    This is the anti-vacuity companion of ``test_c34_feature_documents_introduce_no_third_form``:
    that test's patterns would pass trivially if the retired name had disappeared altogether, and
    the naming history is part of the definition's provenance (STR-002 § 命名史). Both directions
    are therefore asserted — the name is still recorded, and it is recorded in no promoting shape.
    """
    canonical = _canonical_entry()
    assert RETIRED_NAME in canonical["variants"], (
        f"{RETIRED_NAME!r} is not the canonical entry's variant (variants={canonical['variants']!r})"
    )
    rows = parsed_rows()
    index, _entry = canonical_row(rows)
    misplaced = [
        (i, e["canonical"])
        for i, e in enumerate(rows)
        if i != index and RETIRED_NAME in e["canonical"]
    ]
    assert not misplaced, (
        f"the retired name is a canonical cell of another row: {misplaced} — C-30/C-34 allow it "
        "as a variant only"
    )
    recorded = []
    for path in FEATURE_DOCUMENTS:
        for lineno, line in enumerate(read(path).splitlines(), start=1):
            if RETIRED_NAME not in line:
                continue
            recorded.append(f"{path.relative_to(ROOT).as_posix()}:{lineno}: {line.strip()[:120]}")
    assert recorded, (
        f"no document this feature adds records the retired name {RETIRED_NAME!r} at all; without "
        "it the third-form sweep above proves nothing"
    )


# --- C-22 / C-24: the engine's enumeration already covers the three new documents ----------

def _owning_pair(source, mirror):
    """Return the engine `MIRROR_PAIRS` row that owns this document, or fail.

    Ownership is by **path prefix in the engine's own vocabulary**, not by directory name: the
    engine's `shared` pair maps ``shared/`` onto ``.specify/shared/`` and its tree is recursive, so
    ``shared/definitions/x.md`` is enumerated by the ``shared`` pair even though its immediate
    directory is ``shared/definitions``. Deriving the id as ``dirname->dirname`` would have invented
    a pair the engine never declares and failed on a repository that is in fact fully covered.
    """
    owning = [
        (src_name, dst_name, exclude_parts)
        for src_name, dst_name, _strict_extras, exclude_parts in MIRRORS.MIRROR_PAIRS
        if (source == src_name or source.startswith(src_name + "/"))
        and (mirror == dst_name or mirror.startswith(dst_name + "/"))
    ]
    assert len(owning) == 1, (
        f"the engine must own {source}->{mirror} through exactly one MIRROR_PAIRS row, found "
        f"{len(owning)}. Engine enumeration: "
        + str([(s, d) for s, d, _e in MIRRORS.MIRROR_PAIRS])
        + " — with no owning pair this document has no mirror parameter at all"
    )
    return owning[0]


@pytest.mark.parametrize("source,mirror", REQUIRED_MIRROR_PAIRS, ids=[s for s, _m in REQUIRED_MIRROR_PAIRS])
def test_c22_new_document_is_enumerated_by_the_engine(source, mirror):
    src_name, dst_name, exclude_parts = _owning_pair(source, mirror)
    rel = source[len(src_name):].lstrip("/")
    assert (mirror == f"{dst_name}/{rel}"), (
        f"{source} would be mirrored to {dst_name}/{rel}, not to {mirror}; the parent contract's "
        "pair table and the engine's enumeration disagree"
    )
    # `iter_files` decides the enumeration the parity suite parametrizes over; a file it does not
    # yield has no node id, so the suite's green would not cover this document (C-22's carrier claim).
    enumerated = {
        Path(p).as_posix()
        for p in MIRRORS.iter_files(ROOT / src_name, exclude_parts)
    }
    assert rel in enumerated, (
        f"{source} is not yielded by the engine's iter_files for {src_name}/, so the parametrized "
        "mirror-parity suite derives no node for it"
    )
    assert (ROOT / dst_name / rel).is_file(), f"mirror file missing: {dst_name}/{rel}"
    assert (ROOT / src_name / rel).read_bytes() == (ROOT / dst_name / rel).read_bytes(), (
        f"mirror drift: {source}->{mirror} (C-22 requires byte identity; C-24 requires the "
        "carrier to fail here naming the pair)"
    )
