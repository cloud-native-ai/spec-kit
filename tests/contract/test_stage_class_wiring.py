"""Contract tests for the seven stage templates' class-read wiring (077, T009).

Owns the wiring-form and execution-zero-change assertions of
``.specify/specs/077-doc-sdd-integration/contracts/stage-wiring.md``
(C-001 … C-013) that ``tasks.md`` T009 names:

* **C-001** the wiring face is exactly seven command templates —
  ``requirements`` / ``clarify`` / ``plan`` / ``tasks`` / ``checklist`` /
  ``analyze`` / ``implement``. ``clarify`` is inside: the gate owner registers two
  operator rows for it, and excluding it would leave that stage as the only one
  without class awareness.
* **C-002** each template carries **exactly one** wiring subsection whose heading
  is the sole literal registered in ``research.md`` R-9 (the test reads it from
  there — it does not keep a second copy), holding **exactly one** lookup call of
  the form ``flow-class-check.py --action lookup --unit-id "spec:<spec 目录名>"``.
* **C-003** the subsection carries the two owner pointers, one two-branch
  sentence, one visible-degradation sentence and **one exit-code-1 stop
  sentence**; it carries no ``G-`` operator id, no six-face id table, no
  ``flow_class=`` / ``flow_class:`` assignment form and no allow-list keyed on a
  feature number, a path, a keyword or a file type.
* **C-007** execution-class zero behaviour change, judged by **bytes**: stripping
  the subsection with R-9's frozen algorithm must restore the baseline commit
  ``c1cd4600`` byte for byte (SHA-256 pinned below, measured with
  ``git show c1cd4600:<path> | shasum -a 256``), **and** the subsection must be
  present — otherwise the guard spins green on an unwired tree.
* **C-011** the per-tool command copies carry the same subsection; the copy set
  is derived from the generator's own registry (``src/specify_cli``), never
  hard-coded here.
* ``docs.md`` / ``humanize.md`` are the two other wiring entry points and MUST
  keep their pre-077 bytes — this feature does not touch them.

Red-first (Constitution IV): today the seven templates carry the wiring nowhere
(measured: zero hits for ``flow_class|flow-class|expression`` in each of them), so
every wiring assertion below is the intended pre-implementation red, while the
byte guard is red for the opposite reason — there is nothing to strip yet, which
is exactly the "do not spin green" property it must have.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO_ROOT / ".specify" / "specs" / "077-doc-sdd-integration"
RESEARCH = SPEC_DIR / "research.md"
COMMANDS_DIR = REPO_ROOT / "templates" / "commands"

STAGE_STEMS = (
    "requirements",
    "clarify",
    "plan",
    "tasks",
    "checklist",
    "analyze",
    "implement",
)
UNCHANGED_STEMS = ("docs", "humanize")

CLASS_OWNER = "shared/definitions/flow-class-definitions.md"
GATE_OWNER = "shared/workflow/expression-gates.md"
OWNER_PATHS = (CLASS_OWNER, GATE_OWNER)

# The lookup call's argument form (contract C-002 / data-model E4).
LOOKUP_ARG = '--action lookup --unit-id "spec:<spec 目录名>"'
ENGINE_NAME = "flow-class-check.py"

# The six-face closed set (owner: shared/workflow/expression-gates.md § 六面).
# A wiring card never copies a face table, so none of these ids may appear in it.
FACE_IDS = (
    "requirements-clarity",
    "reader-purpose",
    "evidence-asof",
    "structure-links-build",
    "fact-consistency",
    "review",
)

# R-9's strip algorithm, endpoint pattern: the next same-or-higher level heading.
HEADING_STOP_RE = re.compile(r"^#{1,3} ")

BASELINE_COMMIT = "c1cd4600"

# SHA-256 of `git show c1cd4600:templates/commands/<stem>.md` (measured 2026-10-30).
# A legitimate later edit to one of these templates re-measures its row; the guard
# is "stripping the wiring card restores THIS baseline", not "the file never moves".
BASELINE_SHA256 = {
    "requirements": "31d0e1b43079a35f87c35029053ecee8557b75a282a5949079e2f90c6701a82b",
    "clarify": "baf687495d7f5bee1befbb61941aa348085148fe047c15360222e0ecab95cb92",
    "plan": "1833be4a713f7b9cc80f6953303428469e095f9f3efb9472dff225ec835f485c",
    "tasks": "205fa17fe0050ad1002f344783bb4239a5c70ef12144745e6883b45997d0c93d",
    "checklist": "54ca213e7c102af6eb8c173854863c1d19de34364001df31825fb7ccea387d8e",
    "analyze": "31dc261d9bf76243e4a50af62909dbb0c07fd7aa555ebf6acc0970c2eff8151b",
    "implement": "86974490811efa04008f955a44b60e2e739a36ea2bd83b6fe90e1af4c4d2eda9",
}

# The two pre-077 wiring entry points keep their bytes in this feature.
# humanize re-measured 2026-10-31 (079 WC-13): the template was rewritten by 079,
# then its short-description was shortened to satisfy the 50-char frontmatter guard.
# feature 079 (run-then-report repositioning + breaking-change/migration block),
# so its pinned bytes move with that rewrite; docs is untouched.
UNCHANGED_SHA256 = {
    "docs": "3684c30ed841ab4256e4c30ff9382f769ccc1f68713b94e7c1ccd4832c0407c9",
    "humanize": "39c6d42e8a25245a4f6a693a17bc38bccd88021d4703693b47377ffcbe1cb498",
}


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _read(path: Path) -> str:
    assert path.is_file(), "wiring target missing: %s" % path.relative_to(REPO_ROOT)
    return path.read_text(encoding="utf-8")


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _r9_section() -> str:
    """R-9's body — the single registration point of the heading literal."""
    text = _read(RESEARCH)
    marker = "## R-9"
    assert marker in text, "research.md lost its R-9 section (the literal's owner)"
    tail = text[text.index(marker) + len(marker):]
    following = re.search(r"^## ", tail, re.MULTILINE)
    return tail[: following.start()] if following else tail


def wiring_heading() -> str:
    """The subsection heading, read from its single registration point (R-9)."""
    candidates = sorted(set(re.findall(r"`(### [^`\n]+)`", _r9_section())))
    assert len(candidates) == 1, (
        "R-9 must register exactly one heading literal; found %r" % candidates
    )
    return candidates[0]


def _bounds(lines: list[str], heading: str) -> tuple[int, int]:
    """R-9's frozen strip endpoints: (start, end), both inclusive."""
    starts = [index for index, line in enumerate(lines) if line == heading]
    assert len(starts) == 1, (
        "%s must carry exactly %d wiring subsection(s) headed %r, found %d"
        % ("the template", 1, heading, len(starts))
    )
    start = starts[0]
    end = len(lines) - 1
    for index in range(start + 1, len(lines)):
        if HEADING_STOP_RE.match(lines[index]):
            end = index - 1
            break
    return start, end


def wiring_block(path: Path) -> tuple[str, str]:
    """Return ``(heading, body)`` of the wiring card and assert its boundary shape.

    R-9 makes the strip reproducible only when the block ends on **exactly one**
    blank line: two or more blanks leave a stray separator behind after the strip.
    """
    heading = wiring_heading()
    lines = _read(path).split("\n")
    start, end = _bounds(lines, heading)
    block = lines[start:end + 1]
    assert len(block) > 1, (
        "%s: the wiring subsection is empty — a heading with no instruction is not a card"
        % path.name
    )
    assert block[-1].strip() == "", (
        "%s: the wiring block must end on a blank line (R-9's strip endpoint); "
        "last line is %r" % (path.name, block[-1])
    )
    assert block[-2].strip() != "", (
        "%s: the block end must be EXACTLY one blank line — two or more make the "
        "strip non-reproducible" % path.name
    )
    if end + 1 < len(lines):
        assert re.match(r"^#{1,2} ", lines[end + 1]), (
            "%s: the block must be followed by a section heading, got %r"
            % (path.name, lines[end + 1])
        )
    return heading, "\n".join(block)


def strip_wiring(text: str) -> tuple[str, str]:
    """Apply R-9's strip algorithm; return ``(stripped_text, block)``."""
    heading = wiring_heading()
    lines = text.split("\n")
    start, end = _bounds(lines, heading)
    stripped = "\n".join(lines[:start] + lines[end + 1:])
    return stripped, "\n".join(lines[start:end + 1])


def _stage_path(stem: str) -> Path:
    return COMMANDS_DIR / ("%s.md" % stem)


def _tool_copies(stem: str) -> list[Path]:
    """Every per-tool copy the generator would actually produce in this repo.

    Derived from the generator's own registry so the copy count is never a
    number this test owns (the registry allows up to six targets; only the
    directories that exist in this checkout are written).
    """
    sys.path.insert(0, str(REPO_ROOT / "src"))
    try:
        import specify_cli
    except ImportError as exc:  # pragma: no cover — the repo always ships it
        raise AssertionError("cannot import src/specify_cli: %s" % exc)
    finally:
        sys.path.pop(0)

    copies = []
    for agent, rel in specify_cli._ASSISTANT_COMMAND_DIRS.items():
        directory = REPO_ROOT / rel
        if not directory.is_dir():
            continue
        ext = specify_cli._ASSISTANT_EXTENSIONS[agent]
        copies.append(directory / ("speckit.%s.%s" % (stem, ext)))
    return copies


def _assert_card_contract(stem: str, body: str) -> None:
    """C-002 / C-003 content assertions, applied to one stage's card."""
    lookups = body.count(ENGINE_NAME)
    assert lookups == 1, (
        "%s: the card must name the engine exactly once (one read per stage run), "
        "found %d" % (stem, lookups)
    )
    assert LOOKUP_ARG in body, (
        "%s: the single lookup must be spelled `%s` (contract C-002), got:\n%s"
        % (stem, LOOKUP_ARG, body)
    )
    for owner in OWNER_PATHS:
        assert owner in body, (
            "%s: the card must point at %s (C-003)" % (stem, owner)
        )

    # Two branches only: expression runs the stage's operator rows; everything
    # else keeps the existing gate set verbatim.
    assert "表达类" in body, "%s: the card must name the expression branch" % stem
    assert "既有门禁集" in body and "逐字不变" in body, (
        "%s: the card must state that the other branch keeps the existing gate set "
        "verbatim (C-004)" % stem
    )

    # Visible degradation: the label and the exit-2 path, never a silent skip.
    assert "owner-unavailable" in body, (
        "%s: the card must make the degradation visible by name" % stem
    )
    assert "退出码 2" in body, (
        "%s: the card must name the exit-2 degradation path" % stem
    )
    assert "不中断" in body, (
        "%s: the degradation path must state that the stage is not interrupted" % stem
    )

    # Exit-code-1 stop sentence (C-003 / FR-005).
    assert "退出码 1" in body, (
        "%s: the card must carry the exit-code-1 stop sentence" % stem
    )
    assert "停下" in body, (
        "%s: exit code 1 must stop the stage, not fall through to the gate set" % stem
    )
    assert "ANOMALY" in body, (
        "%s: the stop must end on the stage-protocol anomaly line (ANOMALY: …)" % stem
    )
    assert "行号" in body, (
        "%s: the stop must name the file and the line number" % stem
    )


# --------------------------------------------------------------------------- #
# C-001 / C-002 — one card per stage, exactly one lookup
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("stem", STAGE_STEMS)
def test_each_stage_template_carries_exactly_one_wiring_card(stem):
    heading, _body = wiring_block(_stage_path(stem))
    assert heading == wiring_heading(), (
        "%s: the card heading must be the R-9 literal verbatim, got %r"
        % (stem, heading)
    )


@pytest.mark.parametrize("stem", STAGE_STEMS)
def test_the_card_calls_the_single_lookup_once(stem):
    _heading, body = wiring_block(_stage_path(stem))
    _assert_card_contract(stem, body)


@pytest.mark.parametrize("stem", STAGE_STEMS)
def test_the_card_points_at_both_owners(stem):
    _heading, body = wiring_block(_stage_path(stem))
    for owner in OWNER_PATHS:
        assert owner in body, "%s: missing owner pointer %s" % (stem, owner)
    assert "--unit-id" in body, (
        "%s: the lookup must carry the spec key, not a bare unit id" % stem
    )


@pytest.mark.parametrize("stem", STAGE_STEMS)
def test_the_card_states_the_two_branches_and_the_degradation(stem):
    _heading, body = wiring_block(_stage_path(stem))
    assert "表达类" in body and "既有门禁集" in body
    assert "owner-unavailable" in body and "退出码 2" in body


@pytest.mark.parametrize("stem", STAGE_STEMS)
def test_the_card_stops_on_author_input_errors(stem):
    _heading, body = wiring_block(_stage_path(stem))
    assert "退出码 1" in body and "停下" in body and "ANOMALY" in body


# --------------------------------------------------------------------------- #
# C-003 / C-009 — text hygiene: no table copies, no allow-lists
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("stem", STAGE_STEMS)
def test_the_card_carries_no_copied_tables_or_allow_lists(stem):
    _heading, body = wiring_block(_stage_path(stem))
    assert not re.search(r"\bG-[a-z]", body), (
        "%s: the card must not copy an operator id (the operator table has one owner)"
        % stem
    )
    for face_id in FACE_IDS:
        assert face_id not in body, (
            "%s: the card must not copy the six-face table (%r found)"
            % (stem, face_id)
        )
    assert "flow_class=" not in body and "flow_class:" not in body, (
        "%s: the card must not assign the class key" % stem
    )
    assert "077" not in body, (
        "%s: the card must not key on a feature number (switching is class-driven "
        "only, FR-012)" % stem
    )
    for allow_list_word in ("允许列表", "白名单", "whitelist"):
        assert allow_list_word not in body, (
            "%s: the card must not carry a path/keyword allow-list (%r)"
            % (stem, allow_list_word)
        )


@pytest.mark.parametrize("stem", STAGE_STEMS)
def test_the_template_names_no_feature_number(stem):
    text = _read(_stage_path(stem))
    assert "077" not in text, (
        "%s: the whole template must stay feature-neutral — no feature number may "
        "decide whether the docs gate runs (FR-012)" % stem
    )


def test_clarify_is_inside_and_the_other_entry_points_are_untouched():
    assert "clarify" in STAGE_STEMS, (
        "clarify must be wired: the gate owner registers two operator rows for it"
    )
    for stem in UNCHANGED_STEMS:
        path = _stage_path(stem)
        assert path.is_file(), "sentinel: %s moved" % path.relative_to(REPO_ROOT)
        assert _sha256_text(_read(path)) == UNCHANGED_SHA256[stem], (
            "%s is a pre-077 wiring entry point and must keep its bytes in this "
            "feature" % path.relative_to(REPO_ROOT)
        )


# --------------------------------------------------------------------------- #
# C-011 — the generated per-tool copies carry the same card
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("stem", STAGE_STEMS)
def test_each_generated_command_copy_carries_the_card(stem):
    copies = _tool_copies(stem)
    assert copies, (
        "sentinel: no per-tool command directory exists, so this leg would spin green"
    )
    heading = wiring_heading()
    for path in copies:
        assert path.is_file(), "generated command copy missing: %s" % path.relative_to(
            REPO_ROOT
        )
        text = path.read_text(encoding="utf-8")
        assert text.count(heading) == 1, (
            "%s: the copy must carry the wiring card exactly once (run "
            "regen-command-copies.py)" % path.relative_to(REPO_ROOT)
        )
        assert text.count(ENGINE_NAME) == 1, (
            "%s: the copy must carry the single lookup (run regen-command-copies.py)"
            % path.relative_to(REPO_ROOT)
        )


# --------------------------------------------------------------------------- #
# C-007 — execution zero change, judged by bytes, and never vacuous
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("stem", STAGE_STEMS)
def test_stripping_the_card_restores_the_baseline_bytes(stem):
    text = _read(_stage_path(stem))
    stripped, block = strip_wiring(text)

    assert block.strip(), (
        "%s: the strip found an empty block — the guard would spin green on an "
        "unwired template (C-013's anti-empty-green clause)" % stem
    )
    assert stripped != text, (
        "%s: stripping changed nothing, so the byte judge measured the unwired file "
        "against itself" % stem
    )
    assert _sha256_text(stripped) == BASELINE_SHA256[stem], (
        "%s: stripping the wiring card must restore %s byte for byte (C-007); the "
        "execution-class behaviour difference this feature is allowed to introduce "
        "is exactly zero" % (stem, BASELINE_COMMIT)
    )


@pytest.mark.parametrize("stem", STAGE_STEMS)
def test_the_card_is_not_inside_another_section(stem):
    """The card sits after ``## User Input`` and before the next ``## `` heading."""
    heading = wiring_heading()
    lines = _read(_stage_path(stem)).split("\n")
    start, _end = _bounds(lines, heading)
    user_input = [i for i, line in enumerate(lines) if line.strip() == "## User Input"]
    assert len(user_input) == 1, "%s: expected one `## User Input` heading" % stem
    anchor = user_input[0]
    assert anchor < start, (
        "%s: the card must come after `## User Input` (R-9's placement)" % stem
    )
    between = [
        line
        for line in lines[anchor + 1:start]
        if re.match(r"^#{1,3} ", line)
    ]
    assert between == [], (
        "%s: the card must be the first heading block after `## User Input`, found "
        "%r before it" % (stem, between)
    )
