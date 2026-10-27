"""Contract test: the coverage receipt and the segment verdict (Feature 071).

Pins `contracts/coverage-receipt.md` C-31…C-44 plus the appended C-74 against the
one surface that produces them — the `receipt` subcommand of
`skills/internal/code-review/scripts/git-delta-review.sh` — and against the two
surfaces that copy its four counts (`templates/review-template.md` § 2.1 and the
feature detail's `## Latest Review` review-record entry, C-43/C-44/C-74).

What is measured, and what could not be
---------------------------------------
* The receipt's carrier, closed name set, sorted zero-padded per-file rows, the
  counting identity, the closed exit alphabet, gap-versus-skip, the five-value
  reason set, the mechanical verdict derivation, the renderer-literal equality
  and the gap drill are all measured by **driving the real script inside the
  disposable repository** built by `tests/fixtures/review_git_repo.py` (T003).
* The **four-count three-way agreement** (C-74) is measured on a rendered
  instance: the block comes from the real script, the report subsection is
  rendered from the real `templates/review-template.md`, and the feature-detail
  entry is rendered by the same field-by-field copy act the command performs.
  The reconciliation function is then run against a **tampered** copy, so the
  check is proven able to go red instead of agreeing with itself by
  construction. The carriers are prose-filled at run time (the feature-details
  template carries one free-text token), so what is mechanically pinned is the
  copy rule and the agreement of any carrier that repeats the numbers — not a
  run-time instance of a feature detail that does not exist in this fixture.
* The two closed alphabets get their own negative cases at T018's request: a
  skip reason outside the five legal values exits `1` as a gap, and an
  unresolvable range exits `2` with **no** block written.

The block's grammar is parsed by the fixture's `parse_receipt`, never by a
heuristic here (C-42): the owner of the grammar is the fixture module, and a
second parser in this file would be the drift this feature exists to prevent.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional

import pytest

from fixtures.review_git_repo import (
    FRAMEWORK_ROOT,
    RECEIPT_BEGIN,
    RECEIPT_COUNT_FIELDS,
    RECEIPT_END,
    RECEIPT_SCALAR_FIELDS,
    RECORD_FILENAME,
    Receipt,
    ReviewGitRepo,
    ScriptRun,
    parse_receipt,
)

pytestmark = pytest.mark.contract

REPORT_TEMPLATE = FRAMEWORK_ROOT / "templates" / "review-template.md"
FEATURE_DETAIL_TEMPLATE = FRAMEWORK_ROOT / "templates" / "feature-details-template.md"
COMMAND_TEMPLATE = FRAMEWORK_ROOT / "templates" / "commands" / "review.md"

ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")

#: `templates/review-template.md` § 2.1 carries the four counts as placeholders
#: whose Source cell names the receipt block as their only source (C-9/C-74).
#: The mapping placeholder → block field is pinned here on purpose: it is the
#: copy rule the command executes, and a drift in either name must go red.
COUNT_PLACEHOLDERS = {
    "changed_files": "[CHANGED_COUNT]",
    "judged_files": "[JUDGED_COUNT]",
    "skipped_files": "[SKIPPED_COUNT]",
    "gap_files": "[GAP_COUNT]",
}

#: The disclosure line the record carries when the working tree is dirty
#: (C-44). The prefix is what makes a second run replace the previous sentence
#: instead of stacking a new one, so the record stays one fact with two carriers.
DISCLOSURE_PREFIX = "> **未提交范围"


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

@pytest.fixture()
def repo(tmp_path: Path) -> ReviewGitRepo:
    """A disposable git repository rooted in the case's own `tmp_path`."""
    with ReviewGitRepo(root=tmp_path) as built:
        yield built


def _plain(text: str) -> str:
    return ANSI_RE.sub("", text)


def _kv(run: ScriptRun) -> Dict[str, str]:
    fields: Dict[str, str] = {}
    for line in _plain(run.stdout).splitlines():
        match = re.match(r"^([a-z][a-z0-9_]*)=(.*)$", line.strip())
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields


def _spec(key: str) -> str:
    return f".specify/specs/{key}"


def _standard(repo: ReviewGitRepo) -> dict:
    return repo.build_standard_history()


def _fresh_record(repo: ReviewGitRepo) -> str:
    """Create the record from scratch (no rotation, so no same-second collision).

    Removes the previous record first so `start` has nothing to archive: the
    archive path is a different obligation (`C-12`, pinned by the skill-contract
    group) and a same-second rerun here would red for an unrelated reason.
    """
    if repo.record_path.exists():
        repo.record_path.unlink()
    run = repo.run_script("start", "--spec", _spec(repo.key))
    assert run.returncode == 0, "record creation MUST succeed:\n" + run.describe()
    return str(repo.record_path)


def _receipt(repo: ReviewGitRepo, *args: str, **kwargs) -> ScriptRun:
    return repo.run_script(
        "receipt", "--review-file", str(repo.record_path), *args, **kwargs
    )


def _record_text(repo: ReviewGitRepo) -> str:
    return repo.record_path.read_text(encoding="utf-8")


def _requirements_path() -> Path:
    matches = sorted(
        (FRAMEWORK_ROOT / ".specify" / "specs").glob("071-*/requirements.md")
    )
    assert len(matches) == 1, f"expected exactly one 071 requirements owner, got {matches}"
    return matches[0]


def _owner_text() -> str:
    return _requirements_path().read_text(encoding="utf-8")


def _shared_strings() -> Dict[str, str]:
    """Read the Shared Strings table: the literal source for every STR-NNN."""
    table: Dict[str, str] = {}
    for line in _owner_text().splitlines():
        match = re.match(r"^\|\s*`(STR-\d{3})`\s*\|\s*`([^`]+)`\s*\|", line)
        if match:
            table[match.group(1)] = match.group(2)
    assert table, "the Shared Strings table MUST be readable from its owner"
    return table


def _legal_skip_reasons() -> List[str]:
    """The five-value closed reason set, read from its owner (FR-014).

    Read rather than hard-coded: the script holds its own copy, and the drift
    between the two is exactly what this case exists to catch (C-36).
    """
    owner = _owner_text()
    match = re.search(r"跳过理由的取值封闭为([^；]+)", owner)
    assert match, "FR-014 MUST state the closed skip-reason set verbatim"
    reasons = re.findall(r"`([^`]+)`", match.group(1))
    assert len(reasons) == 5, f"the closed set has five values, read {reasons!r}"
    return reasons


def _fresh_delta(repo: ReviewGitRepo) -> tuple:
    """A first-write receipt over the code shape; returns (run, block)."""
    shapes = _standard(repo)
    _fresh_record(repo)
    run = _receipt(
        repo, "--since", shapes["code"].base, "--head", shapes["code"].head
    )
    return run, shapes


def _subsection_template() -> str:
    """The report's code subsection (`### 2.1`) as authored by its owner."""
    text = REPORT_TEMPLATE.read_text(encoding="utf-8")
    start = text.index("### 2.1")
    rest = text[start:]
    following = re.search(r"\n## ", rest)
    assert following, "§ 2.1 MUST be followed by a top-level section"
    return rest[: following.start()]


def _render_report_subsection(receipt: Receipt, verdict: str = "pass") -> str:
    """Render the report's code subsection by copying the block field by field.

    This is the command's copy act, verbatim: every placeholder is replaced by
    the block field it names, and no number is computed here.
    """
    rendered = _subsection_template()
    for field, placeholder in COUNT_PLACEHOLDERS.items():
        assert placeholder in rendered, (
            f"§ 2.1 MUST carry the {placeholder} placeholder (C-9/C-74)"
        )
        rendered = rendered.replace(placeholder, receipt.get(field, ""))
    rendered = rendered.replace("[BASE_SHA]", receipt.get("base", ""))
    rendered = rendered.replace("[HEAD_SHA]", receipt.get("head", ""))
    rendered = rendered.replace("[BASE_SOURCE]", receipt.get("base_source", ""))
    rendered = rendered.replace("[RENDERER_MODE]", f"renderer: {receipt.get('renderer')}")
    rendered = rendered.replace("[SEGMENT_VERDICT]", verdict)
    return rendered


def _render_feature_detail_entry(receipt: Receipt, verdict: str = "pass") -> str:
    """Render the feature detail's `## Latest Review` review-record entry.

    The entry carries no structured field of its own (C-13): it repeats the
    record path, the verdict and the four counts, all copied from the block.
    """
    return (
        f"- review record: `{RECORD_FILENAME}` — code segment {verdict}; "
        f"changed {receipt.get('changed_files')} / judged {receipt.get('judged_files')} "
        f"/ skipped {receipt.get('skipped_files')} / gap {receipt.get('gap_files')} "
        "(copied field by field from the receipt block)"
    )


_COUNT_ROW_LABEL = re.compile(r"(?i)changed\s*/\s*judged\s*/\s*skipped\s*/\s*gap")
_COUNT_CELL = re.compile(r"(\d+)\s*/\s*(\d+)\s*/\s*(\d+)\s*/\s*(\d+)")
_COUNT_PROSE = re.compile(
    r"changed\s+(\d+)\s*/\s*judged\s+(\d+)\s*/\s*skipped\s+(\d+)\s*/\s*gap\s+(\d+)"
)
_COUNT_NAMES = ("changed_files", "judged_files", "skipped_files", "gap_files")


def _counts_from_carrier(text: str) -> Optional[Dict[str, int]]:
    """Read the four counts off a carrier, whatever its prose shape (C-74).

    Two shapes are legal and both are pinned here: the report's table row
    (`Changed / judged / skipped / gap files | 2 / 2 / 0 / 0`) and the free-text
    review-record entry. One function serves both carriers, so "the three agree"
    is a single reconciliation rather than two ad-hoc comparisons.
    """
    for line in text.splitlines():
        if _COUNT_ROW_LABEL.search(line):
            match = _COUNT_CELL.search(line.replace("[", " ").replace("]", " "))
            if match:
                return dict(zip(_COUNT_NAMES, (int(value) for value in match.groups())))
    match = _COUNT_PROSE.search(text)
    if match:
        return dict(zip(_COUNT_NAMES, (int(value) for value in match.groups())))
    return None


def _three_way_agreement(receipt: Receipt, subsection: str, entry: str) -> List[str]:
    """Every disagreement between the block and its two copies."""
    block = {name: receipt.count(name) for name in RECEIPT_COUNT_FIELDS}
    problems: List[str] = []
    for label, text in (("report subsection", subsection), ("feature detail entry", entry)):
        copied = _counts_from_carrier(text)
        if copied is None:
            problems.append(f"{label} carries no four-count row")
        elif copied != block:
            problems.append(f"{label} disagrees with the block: {copied} != {block}")
    return problems


# --------------------------------------------------------------------------- #
# C-31 — the carrier: one delimited block, inside the record, nowhere else
# --------------------------------------------------------------------------- #

def test_c31_the_receipt_is_one_delimited_block_inside_the_record(repo: ReviewGitRepo):
    run, _shapes = _fresh_delta(repo)
    assert run.returncode == 0, run.describe()

    record = _record_text(repo)
    assert record.count(RECEIPT_BEGIN) == 1, "exactly one begin delimiter per record"
    assert record.count(RECEIPT_END) == 1, "exactly one end delimiter per record"
    assert record.index(RECEIPT_BEGIN) < record.index(RECEIPT_END)

    in_record = parse_receipt(record)
    assert in_record is not None, "the block MUST live in the record (C-31)"
    on_stdout = parse_receipt(_plain(run.stdout))
    assert on_stdout is not None, (
        "the command MUST also print the block it wrote, so a caller can hand it on"
    )
    assert on_stdout.raw == in_record.raw, (
        "the printed block and the recorded block MUST be the same bytes; a drift "
        "between them would make two receipts out of one run"
    )

    produced = {path.name for path in repo.spec_dir.iterdir() if path.is_file()}
    assert produced == {"requirements.md", "plan.md", RECORD_FILENAME}, (
        "the receipt MUST NOT be written to a second artifact file, and MUST leave "
        f"no scratch file behind; found {sorted(produced)}"
    )


# --------------------------------------------------------------------------- #
# C-32 / C-33 / C-42 — closed name set, ordered rows, parseable grammar
# --------------------------------------------------------------------------- #

def test_c32_the_block_name_set_is_closed(repo: ReviewGitRepo):
    run, _shapes = _fresh_delta(repo)
    receipt = run.receipt_from_stdout_or_raise()

    assert receipt.unknown_names == [], (
        f"a name outside the closed set is a violation (C-32); found {receipt.unknown_names}"
    )
    assert set(receipt.fields) == set(RECEIPT_SCALAR_FIELDS), (
        "the block MUST carry exactly the closed scalar set; missing "
        f"{sorted(set(RECEIPT_SCALAR_FIELDS) - set(receipt.fields))}, extra "
        f"{sorted(set(receipt.fields) - set(RECEIPT_SCALAR_FIELDS))}"
    )
    for name in RECEIPT_SCALAR_FIELDS:
        assert receipt.get(name) not in (None, ""), f"{name} MUST carry a value"

    for row in receipt.rows:
        assert row.verdict in ("reviewed", "skipped"), (
            f"the per-file verdict is binary (E8), got {row.verdict!r}"
        )
        if row.verdict == "skipped":
            assert row.reason, "a skipped entry MUST carry its reason (C-32)"
        else:
            assert row.reason is None, (
                "a `reviewed` entry MUST NOT carry a reason; the field is legal only "
                "where the verdict is `skipped` (C-32)"
            )
    assert receipt.get("receipt_version") == "1"


def test_c33_the_rows_are_sorted_and_zero_padded_and_a_rerun_is_byte_identical(
    repo: ReviewGitRepo,
):
    """Zero padding only discriminates past nine files, so this case builds ten."""
    shapes = _standard(repo)
    _fresh_record(repo)
    many = [f"src/bulk_{index:02d}.py" for index in range(10)]
    for position, path in enumerate(many):
        repo.write(path, f"VALUE = {position}\n")
    bulk = repo.commit("feat: ten code paths in one delta", many)
    expected_paths = repo.delta_paths(shapes["code"].base, bulk)

    run = repo.run_script(
        "receipt",
        "--review-file",
        str(repo.record_path),
        "--since",
        shapes["code"].base,
        "--head",
        bulk,
    )
    assert run.returncode == 0, run.describe()
    receipt = run.receipt_from_stdout_or_raise()

    assert receipt.count("changed_files") == len(expected_paths), (
        f"the changed set is the delta's file set ({len(expected_paths)} files), got "
        f"{receipt.count('changed_files')}"
    )
    assert receipt.paths == sorted(expected_paths), (
        "the per-file entry set MUST equal the delta's changed-file set (C-33)"
    )
    assert receipt.paths == sorted(receipt.paths), (
        f"per-file rows MUST be emitted in sorted path order (C-33); got {receipt.paths}"
    )
    assert receipt.ordinals == list(range(1, len(receipt.rows) + 1)), (
        f"ordinals MUST be contiguous from 1, got {receipt.ordinals}"
    )
    width = max(2, len(str(len(receipt.rows))))
    for row in receipt.rows:
        assert row.ordinal_token == str(row.ordinal).zfill(width), (
            "ordinals MUST be zero-padded to the width the row count needs (C-33); "
            f"got {row.ordinal_token!r} for {row.path!r} at width {width}"
        )

    again = repo.run_script(
        "receipt",
        "--review-file",
        str(repo.record_path),
        "--since",
        shapes["code"].base,
        "--head",
        bulk,
    )
    assert again.returncode == 0, again.describe()
    assert again.receipt_from_stdout_or_raise().raw == receipt.raw, (
        "two runs over the same repository state MUST produce a byte-identical block "
        "(C-33 / SC-002)"
    )


def test_c42_the_grammar_needs_no_heuristic(repo: ReviewGitRepo):
    run, _shapes = _fresh_delta(repo)
    receipt = run.receipt_from_stdout_or_raise()
    assert receipt.equality_violations() == [], (
        f"the block MUST satisfy its own grammar and identity: {receipt.equality_violations()}"
    )
    assert receipt.counting_identity_holds, (
        "judged_files + skipped_files + gap_files == changed_files (C-42)"
    )
    body = _record_text(repo).split(RECEIPT_BEGIN, 1)[1].split(RECEIPT_END, 1)[0]
    for line in body.strip().splitlines():
        assert line.strip(), "the block MUST NOT carry blank lines inside it"
        assert "=" in line, f"every block line is one name=value pair; got {line!r}"


# --------------------------------------------------------------------------- #
# C-34 / C-35 — the closed exit alphabet, one meaning per code
# --------------------------------------------------------------------------- #

def test_the_exit_alphabet_is_closed_at_three_with_one_meaning_each(repo: ReviewGitRepo):
    """`0` complete, `1` coverage gap, `2` cannot evaluate — measured, not asserted.

    Each of the three conditions is driven on its own, and the three codes are
    read back: a run that swapped `1` and `2` would fail here even if it produced
    the right number of non-zero exits.
    """
    measured: Dict[str, int] = {}

    run, shapes = _fresh_delta(repo)
    measured["complete"] = run.returncode
    assert run.returncode == 0, (
        "the sets are equal and every changed file carries a verdict -> `0`:\n"
        + run.describe()
    )

    # a changed file with no verdict: delete its rows and re-run (the gap drill)
    repo.record_path.write_text(
        _drop_entry(_record_text(repo), repo.CODE_PATH), encoding="utf-8"
    )
    range_args = ("--since", shapes["code"].base, "--head", shapes["code"].head)
    run_gap = _receipt(repo, *range_args)
    measured["gap"] = run_gap.returncode
    assert run_gap.returncode == 1, (
        "a changed file with no entry is a coverage gap -> `1`:\n" + run_gap.describe()
    )

    # a record that does not exist: nothing can be evaluated
    missing = repo.run_script(
        "receipt", "--review-file", str(repo.spec_dir / "absent-record.md")
    )
    measured["cannot evaluate"] = missing.returncode
    assert missing.returncode == 2, (
        "a missing record cannot be evaluated -> `2`:\n" + missing.describe()
    )

    assert measured == {"complete": 0, "gap": 1, "cannot evaluate": 2}, (
        "the alphabet is closed at `0` / `1` / `2` with one meaning each and `1` and "
        f"`2` are not interchangeable; measured {measured}"
    )


def test_c35_exit_2_writes_no_block_and_names_its_reason(repo: ReviewGitRepo):
    _standard(repo)
    _fresh_record(repo)
    before = _record_text(repo)

    run = _receipt(repo, "--since", "does-not-exist", "--head", "HEAD")
    assert run.returncode == 2, (
        "an unresolvable range cannot be evaluated -> `2`:\n" + run.describe()
    )
    assert run.receipt() is None, "exit 2 MUST write no block, not even a partial one"
    assert _record_text(repo) == before, (
        "the record MUST be left exactly as it was; a partial block is never written"
    )
    text = _plain(run.stdout + run.stderr)
    assert re.search(r"reason=|not-evaluated", text), (
        "exit 2 MUST name why it could not evaluate:\n" + run.describe()
    )


# --------------------------------------------------------------------------- #
# C-36 — gap versus skip, and the five-value reason set
# --------------------------------------------------------------------------- #

def test_c36_a_legal_skip_is_disclosed_and_earns_no_coverage(repo: ReviewGitRepo):
    shapes = _standard(repo)
    _fresh_record(repo)
    reason = _legal_skip_reasons()[0]
    run = _receipt(
        repo,
        "--since",
        shapes["code"].base,
        "--head",
        shapes["code"].head,
        "--skip-with-reason",
        "src/*",
        "--reason",
        reason,
    )
    assert run.returncode == 0, (
        "a reasoned skip is a legal verdict, so the command still exits `0`:\n"
        + run.describe()
    )
    receipt = run.receipt_from_stdout_or_raise()
    assert receipt.count("skipped_files") == 1
    assert receipt.count("judged_files") == 1, (
        "a skip MUST be excluded from judged_files: it is disclosed, never counted "
        "as coverage the run did not earn (C-36)"
    )
    row = receipt.row_for(repo.CODE_PATH)
    assert row is not None and row.verdict == "skipped" and row.reason == reason
    assert _kv(run).get("verdict") != _shared_strings()["STR-006"], (
        "with skipped_files > 0 the segment verdict MUST NOT be `pass` (C-37)"
    )


def test_c36_the_five_value_reason_set_is_read_from_its_owner(repo: ReviewGitRepo):
    """Every value of the owner's closed set is accepted; the set is not guessed."""
    reasons = _legal_skip_reasons()
    shapes = _standard(repo)
    accepted: List[str] = []
    for reason in reasons:
        _fresh_record(repo)
        run = _receipt(
            repo,
            "--since",
            shapes["code"].base,
            "--head",
            shapes["code"].head,
            "--skip-with-reason",
            "src/*",
            "--reason",
            reason,
        )
        assert run.returncode == 0, (
            f"the owner's legal reason {reason!r} MUST be accepted:\n" + run.describe()
        )
        receipt = run.receipt_from_stdout_or_raise()
        row = receipt.row_for(repo.CODE_PATH)
        assert row is not None and row.reason == reason
        accepted.append(row.reason)
    assert accepted == reasons, (
        "the script's accepted set MUST equal the owner's set, value for value "
        f"(C-36); accepted {accepted!r} against owner {reasons!r}"
    )


def test_c36_an_unrecognised_skip_reason_is_a_gap_not_a_legal_skip(repo: ReviewGitRepo):
    shapes = _standard(repo)
    _fresh_record(repo)
    run = _receipt(
        repo,
        "--since",
        shapes["code"].base,
        "--head",
        shapes["code"].head,
        "--skip-with-reason",
        "src/*",
        "--reason",
        "because I felt like it",
    )
    assert run.returncode == 1, (
        "free text is not a legal reason, so it is a coverage gap -> `1`:\n"
        + run.describe()
    )
    receipt = run.receipt_from_stdout_or_raise()
    assert receipt.count("skipped_files") == 0, (
        "an unrecognised reason MUST NOT be recorded as a skip (C-36)"
    )
    assert receipt.count("gap_files") == 1, (
        "the file it would have skipped is a gap instead (V34)"
    )


# --------------------------------------------------------------------------- #
# C-37 / C-38 — the verdict is derived from three signals, by presence
# --------------------------------------------------------------------------- #

def _add_blocking(repo: ReviewGitRepo) -> None:
    noted = repo.run_script(
        "note",
        "-s",
        "blocking",
        "-f",
        repo.CODE_PATH,
        "-c",
        "a real defect",
        "--review-file",
        str(repo.record_path),
    )
    assert noted.returncode == 0, noted.describe()


def test_c37_c38_the_verdict_is_the_conjunction_of_the_three_signals(repo: ReviewGitRepo):
    strings = _shared_strings()
    pass_literal = strings["STR-006"]
    blocked_literal = strings["STR-007"]
    not_evaluated = strings["STR-002"]
    shapes = _standard(repo)
    seen: Dict[str, str] = {}

    # gap 0, skip 0, no blocking -> pass
    _fresh_record(repo)
    run = _receipt(repo, "--since", shapes["code"].base, "--head", shapes["code"].head)
    assert run.returncode == 0, run.describe()
    seen["clean"] = _kv(run)["verdict"]
    assert seen["clean"] == pass_literal

    # gap 0, skip 0, one blocking -> blocked
    _fresh_record(repo)
    _add_blocking(repo)
    run = _receipt(repo, "--since", shapes["code"].base, "--head", shapes["code"].head)
    seen["clean+blocking"] = _kv(run)["verdict"]
    assert seen["clean+blocking"] == blocked_literal

    # gap 0, skip > 0, no blocking -> not-evaluated (a skip is not coverage)
    _fresh_record(repo)
    run = _receipt(
        repo,
        "--since",
        shapes["code"].base,
        "--head",
        shapes["code"].head,
        "--skip-with-reason",
        "src/*",
        "--reason",
        _legal_skip_reasons()[-1],
    )
    seen["skip"] = _kv(run)["verdict"]
    assert seen["skip"] == not_evaluated, (
        "a focus-driven skip cannot be presented as a complete pass (C-37)"
    )

    # gap 0, skip > 0, one blocking -> blocked
    _fresh_record(repo)
    _add_blocking(repo)
    run = _receipt(
        repo,
        "--since",
        shapes["code"].base,
        "--head",
        shapes["code"].head,
        "--skip-with-reason",
        "src/*",
        "--reason",
        _legal_skip_reasons()[-1],
    )
    seen["skip+blocking"] = _kv(run)["verdict"]
    assert seen["skip+blocking"] == blocked_literal

    # gap > 0 -> not-evaluated, whatever the other two say
    _fresh_record(repo)
    _add_blocking(repo)
    run = _receipt(repo, "--since", shapes["code"].base, "--head", shapes["code"].head)
    assert run.returncode == 0, run.describe()
    record = _record_text(repo)
    repo.record_path.write_text(
        _drop_entry(record, repo.CODE_PATH), encoding="utf-8"
    )
    gapped = _receipt(repo, "--since", shapes["code"].base, "--head", shapes["code"].head)
    assert gapped.returncode == 1, gapped.describe()
    seen["gap+blocking"] = _kv(gapped)["verdict"]
    assert seen["gap+blocking"] == not_evaluated, (
        "a gap is not a conclusion, so it outranks the blocking signal (E9)"
    )

    assert len(set(seen.values())) >= 3, (
        f"the verdict MUST be derived, never defaulted; seen {seen}"
    )


def _drop_entry(record: str, path: str) -> str:
    """Remove one file's per-file rows from the block (the gap drill's act)."""
    lines = record.splitlines()
    drop_ordinal = None
    for line in lines:
        match = re.match(r"^file\.(\d+)\.path=(.*)$", line)
        if match and match.group(2) == path:
            drop_ordinal = match.group(1)
    assert drop_ordinal is not None, f"fixture precondition: {path} has a per-file row"
    kept = [
        line
        for line in lines
        if not re.match(rf"^file\.{drop_ordinal}\.(path|verdict|reason)=", line)
    ]
    return "\n".join(kept) + "\n"


def test_c38_the_blocking_signal_is_a_presence_test_not_a_resolved_state(repo: ReviewGitRepo):
    strings = _shared_strings()
    shapes = _standard(repo)
    _fresh_record(repo)
    _add_blocking(repo)
    record = _record_text(repo)
    annotated = record.replace(
        "[BLOCKING] src/fixture_demo.py",
        "[BLOCKING] src/fixture_demo.py (已解决 / resolved)",
    )
    assert annotated != record, "fixture precondition: the blocking heading was annotated"
    repo.record_path.write_text(annotated, encoding="utf-8")

    run = _receipt(repo, "--since", shapes["code"].base, "--head", shapes["code"].head)
    assert _kv(run)["verdict"] == strings["STR-007"], (
        "the third signal is a presence test over the current record's headings: the "
        "feature defines no clearing action and no cleared state, so an entry nobody "
        "removed still blocks even when prose calls it resolved (C-38 / V35)"
    )

    # A later record with no blocking heading no longer blocks; nothing is cleared.
    _fresh_record(repo)
    clean = _receipt(repo, "--since", shapes["code"].base, "--head", shapes["code"].head)
    assert _kv(clean)["verdict"] == strings["STR-006"], (
        "a fresh record with zero blocking headings MUST allow — replacive, not cleared"
    )


def test_c38_an_empty_delta_never_reaches_the_receipt(repo: ReviewGitRepo):
    strings = _shared_strings()
    shapes = _standard(repo)
    _fresh_record(repo)
    before = _record_text(repo)

    run = _receipt(
        repo, "--since", shapes["empty"].base, "--head", shapes["empty"].head
    )
    assert run.returncode == 2, (
        "an empty changed set is triaged `not-applicable` BEFORE this step; it MUST "
        "NOT be reported as a 0/0/0 pass (C-38 / V20):\n" + run.describe()
    )
    assert run.receipt() is None, "no block, not even a 0/0/0 one"
    assert _record_text(repo) == before
    text = _plain(run.stdout + run.stderr)
    assert strings["STR-001"] in text or "empty delta" in text, (
        "the refusal MUST name the empty delta / not-applicable answer:\n" + run.describe()
    )
    assert f"verdict={strings['STR-006']}" not in text, (
        "no `pass` may be derived over nothing"
    )


# --------------------------------------------------------------------------- #
# C-40 / C-41 — the renderer literal and the measured line counts
# --------------------------------------------------------------------------- #

def test_c40_the_block_renderer_equals_the_record_header_marker(repo: ReviewGitRepo):
    shapes = _standard(repo)
    _fresh_record(repo)
    # `start` was told to claim the rendered mode; the receipt re-derives it by the
    # two-condition rule (no TTY here) and MUST leave the two forms in agreement.
    started = repo.run_script("start", "--spec", _spec(repo.key), "--renderer", "delta")
    assert started.returncode == 0, started.describe()
    pre = _record_text(repo)
    assert "renderer: delta" in pre, "fixture precondition: the header claims delta"

    run = _receipt(repo, "--since", shapes["code"].base, "--head", shapes["code"].head)
    assert run.returncode == 0, run.describe()
    receipt = run.receipt_from_stdout_or_raise()
    record = _record_text(repo)
    header_has_delta = "renderer: delta" in record
    header_has_text = "renderer: text" in record
    assert header_has_text != header_has_delta, (
        "the header MUST carry exactly one mode marker (C-21)"
    )
    header_mode = "delta" if header_has_delta else "text"
    assert receipt.get("renderer") == header_mode, (
        "the block's `renderer` and the record's marker are written by the same "
        f"invocation and MUST agree; block={receipt.get('renderer')!r} "
        f"header={header_mode!r} (C-40)"
    )
    assert header_mode == "text", (
        "a piped call takes text mode even though the renderer may exist here "
        "(quickstart Scenario D, the no-TTY case)"
    )
    assert _kv(run).get("renderer") == header_mode


def test_c41_the_line_counts_are_measured_from_numstat(repo: ReviewGitRepo):
    shapes = _standard(repo)
    _fresh_record(repo)
    run = _receipt(repo, "--since", shapes["code"].base, "--head", shapes["code"].head)
    assert run.returncode == 0, run.describe()
    receipt = run.receipt_from_stdout_or_raise()

    raw = repo.git("diff", "--numstat", f"{shapes['code'].base}..{shapes['code'].head}")
    added = deleted = 0
    for line in raw.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        added += int(parts[0])
        deleted += int(parts[1])
    assert receipt.count("lines_added") == added, (
        f"lines_added MUST be measured from `git diff --numstat` ({added})"
    )
    assert receipt.count("lines_deleted") == deleted
    assert added > 0, "fixture precondition: the code shape really adds lines"


# --------------------------------------------------------------------------- #
# SC-002 — the gap drill
# --------------------------------------------------------------------------- #

def test_sc002_the_gap_drill_deletes_one_entry_and_the_rerun_goes_red(repo: ReviewGitRepo):
    run, shapes = _fresh_delta(repo)
    assert run.returncode == 0, run.describe()
    assert run.receipt_from_stdout_or_raise().count("gap_files") == 0

    record = _record_text(repo)
    repo.record_path.write_text(_drop_entry(record, repo.CODE_PATH), encoding="utf-8")

    red = _receipt(repo, "--since", shapes["code"].base, "--head", shapes["code"].head)
    assert red.returncode == 1, (
        "after one per-file entry is deleted the command MUST go red (SC-002):\n"
        + red.describe()
    )
    red_receipt = red.receipt_from_stdout_or_raise()
    assert red_receipt.count("gap_files") == 1, (
        "the rewritten block MUST carry gap_files equal to the number of unjudged files"
    )
    assert red_receipt.count("changed_files") == 2, (
        "the changed set did not move; only the judged set did"
    )

    repo.record_path.write_text(record, encoding="utf-8")
    green = _receipt(repo, "--since", shapes["code"].base, "--head", shapes["code"].head)
    assert green.returncode == 0, (
        "restoring the entry returns the command to `0`:\n" + green.describe()
    )
    assert green.receipt_from_stdout_or_raise().count("gap_files") == 0


# --------------------------------------------------------------------------- #
# C-43 / C-44 / C-74 — the counts and the disclosure on both carriers
# --------------------------------------------------------------------------- #

def test_c74_the_four_counts_agree_three_ways(repo: ReviewGitRepo):
    run, _shapes = _fresh_delta(repo)
    receipt = run.receipt_from_stdout_or_raise()
    subsection = _render_report_subsection(receipt)
    entry = _render_feature_detail_entry(receipt)

    assert _three_way_agreement(receipt, subsection, entry) == [], (
        "the block's four counts, the report subsection and the feature detail entry "
        "MUST agree field by field (C-74)"
    )

    # The check must be able to go red: a carrier that drifts from the block reds.
    copied_cell = " / ".join(
        str(receipt.count(name)) for name in RECEIPT_COUNT_FIELDS
    )
    tampered = subsection.replace(copied_cell, "99 / 99 / 99 / 99", 1)
    assert tampered != subsection, "fixture precondition: the copy was tampered with"
    assert _three_way_agreement(receipt, tampered, entry), (
        "a carrier that recomputes or re-aggregates its numbers MUST be detected; a "
        "check that stays green here would prove nothing"
    )

    # Provenance: the rule that makes the copies copies, read from their owners.
    template = _subsection_template()
    assert re.search(r"copied field by field|抄自", template), (
        "§ 2.1 MUST state that the four counts are copied field by field from the "
        "receipt block"
    )
    assert re.search(r"never recomputed|MUST NOT 独立计算|不.{0,2}重算|never re-aggregate", template), (
        "§ 2.1 MUST forbid recomputation of the four counts"
    )
    command = COMMAND_TEMPLATE.read_text(encoding="utf-8")
    assert "Latest Review" in command, (
        "the command template MUST name the feature detail's `## Latest Review` entry "
        "as the second verifiable carrier (C-13/C-43)"
    )
    detail = FEATURE_DETAIL_TEMPLATE.read_text(encoding="utf-8")
    assert "## Latest Review" in detail, (
        "the carrier MUST be the existing `## Latest Review` entry, not a new field"
    )


def test_c43_a_non_zero_gap_or_skip_count_is_surfaced_outside_the_block(repo: ReviewGitRepo):
    shapes = _standard(repo)
    _fresh_record(repo)
    run = _receipt(
        repo,
        "--since",
        shapes["code"].base,
        "--head",
        shapes["code"].head,
        "--skip-with-reason",
        "src/*",
        "--reason",
        _legal_skip_reasons()[-1],
    )
    assert run.returncode == 0, run.describe()
    receipt = run.receipt_from_stdout_or_raise()
    assert receipt.count("skipped_files") == 1

    subsection = _render_report_subsection(receipt, verdict=_kv(run)["verdict"])
    outside_block = subsection
    assert RECEIPT_BEGIN not in outside_block, (
        "fixture precondition: the report subsection is a carrier of its own, not a "
        "second copy of the block"
    )
    assert _counts_from_carrier(outside_block) == {
        name: receipt.count(name) for name in RECEIPT_COUNT_FIELDS
    }, "a shortfall visible only inside the block is not a disclosure (C-43)"
    assert _kv(run).get("skipped_files") == "1", (
        "the command's own report of the run MUST name the skip count too, so the "
        "process report can copy it rather than recompute it"
    )


def test_c44_a_dirty_tree_is_disclosed_on_both_carriers_without_a_conclusion(
    repo: ReviewGitRepo,
):
    shapes = _standard(repo)
    _fresh_record(repo)
    dirty_paths = repo.make_dirty(untracked="src/untracked_work.py")
    assert dirty_paths

    run = _receipt(repo, "--since", shapes["code"].base, "--head", shapes["code"].head)
    assert run.returncode == 0, run.describe()

    receipt = run.receipt_from_stdout_or_raise()
    assert receipt.count("changed_files") == 2, (
        "the uncommitted scope MUST NOT be folded into the review object (FR-005)"
    )
    assert "src/untracked_work.py" not in receipt.paths

    record = _record_text(repo)
    disclosures = [line for line in record.splitlines() if line.startswith(DISCLOSURE_PREFIX)]
    assert len(disclosures) == 1, (
        "the record MUST carry exactly one disclosure line, replaced rather than "
        f"stacked on a re-run (C-44); found {disclosures}"
    )
    sentence = disclosures[0]
    assert "src/untracked_work.py" in sentence or "1" in sentence, (
        "the disclosure MUST name the scope it excludes"
    )
    assert not re.search(r"通过|pass|已评审", sentence), (
        "the disclosure MUST NOT issue any conclusion over the unreviewed scope (C-44)"
    )
    assert _kv(run).get("uncommitted_scope") == str(len(dirty_paths)), (
        "the same fact MUST reach the report carrier as a field the report copies (C-44)"
    )

    # A clean tree carries no disclosure, so the line is a measurement, not boilerplate.
    repo.clean_worktree()
    _fresh_record(repo)  # the clean sweep removed the untracked record too
    clean = _receipt(repo, "--since", shapes["code"].base, "--head", shapes["code"].head)
    assert clean.returncode == 0, clean.describe()
    assert not [
        line
        for line in _record_text(repo).splitlines()
        if line.startswith(DISCLOSURE_PREFIX)
    ], "a clean tree MUST NOT leave a stale disclosure behind"


# --------------------------------------------------------------------------- #
# T018 — the quickstart alphabets, plus the interactive path that must not degrade
# --------------------------------------------------------------------------- #

def test_t018_an_illegal_skip_reason_exits_1_and_an_unresolvable_range_exits_2(
    repo: ReviewGitRepo,
):
    shapes = _standard(repo)
    _fresh_record(repo)

    illegal = _receipt(
        repo,
        "--since",
        shapes["code"].base,
        "--head",
        shapes["code"].head,
        "--skip-with-reason",
        "src/*",
        "--reason",
        "free text is not a reason",
    )
    assert illegal.returncode == 1, (
        "the first closed alphabet: a reason outside the five values is a gap -> `1`"
    )
    assert illegal.receipt_from_stdout_or_raise().count("gap_files") == 1

    _fresh_record(repo)
    before = _record_text(repo)
    unresolvable = _receipt(repo, "--since", "no-such-ref", "--head", "HEAD")
    assert unresolvable.returncode == 2, (
        "the second closed alphabet: an unresolvable range -> `2`"
    )
    assert unresolvable.receipt() is None and _record_text(repo) == before, (
        "`2` writes no block, so the two alphabets cannot be swapped"
    )


def test_t018_the_interactive_walk_and_the_six_level_validation_are_intact(
    repo: ReviewGitRepo,
):
    """Driven end to end, not read off the script (C-28)."""
    delta = ReviewGitRepo.host_delta_bin()
    if not delta:
        pytest.skip("no renderer on this host; the interactive walk needs one")

    shapes = _standard(repo)
    walk = repo.run_script(
        "review",
        "--yes",
        "--since",
        shapes["code"].base,
        "--head",
        shapes["code"].head,
        delta_bin=delta,
    )
    assert walk.returncode == 0, (
        "the non-interactive per-file walk MUST still complete:\n" + walk.describe()
    )
    produced = sorted(repo.review_dir.glob("*.md"))
    assert len(produced) == 1, f"the walk MUST still write its report, found {produced}"
    body = produced[0].read_text(encoding="utf-8")
    assert repo.CODE_PATH in body and "统计" in body, (
        "the walk MUST still render every changed file and its statistics table"
    )

    severities = ("blocking", "important", "suggestion", "nitpick", "question", "praise")
    for severity in severities:
        noted = repo.run_script(
            "note",
            "-s",
            severity,
            "-f",
            repo.CODE_PATH,
            "-c",
            f"{severity} level accepted",
            "--review-file",
            str(produced[0]),
        )
        assert noted.returncode == 0, (
            f"the six-level vocabulary MUST still accept {severity!r}:\n" + noted.describe()
        )
    rejected = repo.run_script(
        "note",
        "-s",
        "critical",
        "-f",
        repo.CODE_PATH,
        "-c",
        "a level outside the closed set",
        "--review-file",
        str(produced[0]),
    )
    assert rejected.returncode != 0, (
        "the six-level validation MUST still reject a value outside the closed set"
    )
    assert "critical" in _plain(rejected.stdout + rejected.stderr)
