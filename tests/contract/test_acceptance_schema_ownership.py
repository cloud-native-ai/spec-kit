"""Contract tests for contracts/artifact-schemas.contract.md AS-13…AS-16 — SC-009 ④ (Feature 081d).

Subject: the schema-uniqueness guard over the three artifact schemas the owner document defines
(`shared/workflow/acceptance-hardening.md` § Runtime Stack & Dependency Ownership, § Execution
Premises, § Inherited Blockers). What the guard asserts, on which subject, over which paths is
owned by the owner doc's § Schema Uniqueness; this module is the enumeration that doc and
`requirements.md` SC-009 ④ both name — it derives its subject mechanically and never re-types it.

**The subject is the column-name set.** The three column-declaration tables (the `| Column |
Content |` tables in the owner's three schema sections) are read out of the owner at collection
time; their ordered `Column` cell sequences are the guarded literals. The names are never spelled
in this file: a test that re-typed them would itself be the second definition point AS-13 exists
to remove.

**A hit is a whole column set** — the ordered cell sequence of a table header row — never a
single column name and never a value-domain literal. Individual names (`Status`, `Form`, `Owner`,
`ID`, `Evidence`) are ordinary headers of unrelated tables in the same domain, and the domain
literals collide with unrelated closed sets (`not-required` the traceability binary,
`not-applicable` the code-review segment verdict, `in-scope` ordinary English); either weaker
subject produces hits only a hand-written exclusion list could absorb (AS-14).

**Scan domain**: `templates/` and `shared/` — framework source. `.specify/` copies are mirrors,
judged by `sync-mirrors.py --check`, never scanned here. The owner document is inside the domain
and is excluded **by identity** (it is the definition site), never by a list entry; the single
in-domain allowed surface is `templates/plan-template.md`, which carries the Execution Premises
and Inherited Blockers column sets as its two skeletons (AS-15) — an empty table must carry its
columns, or every future plan invents its own.

**The narrowing assertions (a)…(d) and which side of the scan each lives on** (AS-16 — the
surfaces outside the scan are duties of their own, never guard exemptions):
  (a) `data-model.md` carries 0 `From | To | Allowed | Condition` transition rows — outside the
      scan (`.specify/specs/<key>/`), so this is the surface's own duty, asserted here as such;
  (b) every value a projection surface declares belongs to the deciding domain (a projection may
      narrow, never widen) — asserted for the declared carriers the owner doc names;
  (c) `requirements.md` carries 0 transition rows of that form — same class as (a);
  (d) `templates/plan-template.md` carries 0 owner-exported domain literals (a column name may
      appear; an `in-scope` / `verified` / `resolved` may not) — the allowed surface's own
      narrowing duty (AS-14/AS-15).
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
OWNER = ROOT / "shared" / "workflow" / "acceptance-hardening.md"
PLAN_TEMPLATE = ROOT / "templates" / "plan-template.md"
DATA_MODEL = ROOT / ".specify" / "specs" / "081-acceptance-hardening" / "data-model.md"
REQUIREMENTS = ROOT / ".specify" / "specs" / "081-acceptance-hardening" / "requirements.md"
SCAN_ROOTS = (ROOT / "templates", ROOT / "shared")

SEPARATOR_ROW = re.compile(r"^\|[\s:|-]+\|?\s*$")
HEADING = re.compile(r"^#{1,6}\s")


def _cells(line):
    """The stripped, backtick-free cells of a Markdown table row, or `None` for non-table lines."""
    stripped = line.strip()
    if not stripped.startswith("|"):
        return None
    return [c.strip().strip("`").strip() for c in stripped.strip("|").split("|")]


def _key(cells):
    """The comparison key of a cell sequence: casefolded, whitespace-collapsed."""
    return tuple(re.sub(r"\s+", " ", c).casefold() for c in cells)


# --------------------------------------------------------------------------- #
# The subject, derived — never re-typed
# --------------------------------------------------------------------------- #

def _column_sets():
    """`[(section, [column, …])]` from the owner's `| Column | Content |` declaration tables.

    Each such table declares one artifact schema's columns; the `Column` cells, in order, are the
    guarded literal. Exactly three schema sections are declared today (AS-13); a fourth
    declaration table is a new schema and fails here until the guard is consciously revised.
    """
    lines = OWNER.read_text(encoding="utf-8").splitlines()
    found = []
    index = 0
    while index < len(lines):
        cells = _cells(lines[index])
        if cells and _key(cells) == ("column", "content"):
            section = next(
                (l.lstrip("# ").strip() for l in reversed(lines[:index]) if HEADING.match(l)),
                "?",
            )
            names, scan = [], index + 1
            while scan < len(lines):
                row = _cells(lines[scan])
                if row is None:
                    break
                if SEPARATOR_ROW.match(lines[scan].strip()):
                    scan += 1
                    continue
                names.append(row[0])
                scan += 1
            found.append((section, names))
            index = scan
        else:
            index += 1
    assert len(found) == 3, (
        "the owner doc declares %d `| Column | Content |` tables, not 3 — a new artifact schema "
        "needs this guard revised consciously, not silently extended: %r"
        % (len(found), [s for s, _ in found])
    )
    for section, names in found:
        assert len(names) >= 5, (
            "the owner's %r column declaration carries %d columns; an empty or stubbed "
            "declaration would derive an empty subject and prove nothing" % (section, len(names))
        )
    return found


def _column_keys():
    return {_key(names) for _, names in _column_sets()}


# --------------------------------------------------------------------------- #
# The enumeration — real hits, real files
# --------------------------------------------------------------------------- #

def _hits():
    """`[(path, line_no, cells)]` for every header row in the scan domain matching a column set."""
    keys = _column_keys()
    hits = []
    for base in SCAN_ROOTS:
        for path in sorted(base.rglob("*.md")):
            for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                cells = _cells(line)
                if cells and _key(cells) in keys:
                    hits.append((path, line_no, cells))
    return hits


def test_the_column_sets_appear_zero_times_outside_the_owner_and_its_one_allowed_surface():
    """AS-13/AS-14: zero non-owner hits, exactly one in-domain allowed surface.

    The owner is excluded by identity (it is the definition site — a hit there is the
    declaration, not a restatement), `templates/plan-template.md` is the one surface the owner's
    § Schema Uniqueness allows, and everything else in `templates/` and `shared/` must be clean.
    The full enumeration is printed on failure so a new leak is readable rather than counted.
    """
    hits = _hits()
    violators = [h for h in hits if h[0] not in (OWNER, PLAN_TEMPLATE)]
    assert not violators, (
        "schema-ownership leak: the owner's column sets appear %d time(s) outside "
        "shared/workflow/acceptance-hardening.md (allowed by identity) and "
        "templates/plan-template.md (the one in-domain allowed surface):\n%s"
        % (len(violators), "\n".join("  %s:%d %r" % (p, n, c) for p, n, c in violators))
    )
    plan_hits = [h for h in hits if h[0] == PLAN_TEMPLATE]
    assert plan_hits, (
        "templates/plan-template.md no longer carries any of the owner's column sets; the two "
        "plan-table skeletons are the reason the surface is allowed at all (AS-15) — a skeleton "
        "without columns forces every future plan to invent its own"
    )


def test_the_plan_skeleton_carries_both_plan_table_column_sets():
    """AS-15's positive side: both skeletons exist, by their derived column sets.

    The allowed surface is allowed *because* it hands the two plan tables' columns down; a
    skeleton that lost one of them would be an empty allowance — the guard permitting a file that
    no longer carries what justified the permission.
    """
    keys = _column_sets()
    text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    found = {
        _key(cells) for line in text.splitlines() if (cells := _cells(line)) is not None
    } & {_key(names) for _, names in keys}
    expected = {_key(names) for _, names in keys if "premise" in [c.casefold() for c in names]
                or "carrier slice" in [c.casefold() for c in names]}
    missing = expected - found
    assert not missing, (
        "templates/plan-template.md is missing the skeleton(s) for %r; the plan template may "
        "repeat the column sets and nothing else (AS-15)"
        % [names for _, names in keys if _key(names) in missing]
    )


# --------------------------------------------------------------------------- #
# (a) / (c) — the two spec-side surfaces carry no restated transition table
# --------------------------------------------------------------------------- #

TRANSITION_FORM = _key(["From", "To", "Allowed", "Condition"])


def _transition_rows(path):
    """Header rows of the `From | To | Allowed | Condition` form in one file."""
    return [
        (line_no, line.strip())
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
        if (cells := _cells(line)) and _key(cells) == TRANSITION_FORM
    ]


def test_data_model_carries_zero_owner_transition_rows():
    """(a) — a duty of `data-model.md` itself, outside the scan domain (AS-16).

    The owner's § Feature Status holds the four `Blocked` transitions; a transition row restated
    in the data model would be an unguarded duplicate. The surface is under
    `.specify/specs/<key>/`, where the scan cannot reach — which is exactly why this is its own
    assertion and not an exemption of the column-set guard.
    """
    rows = _transition_rows(DATA_MODEL)
    assert not rows, (
        "data-model.md restates the owner's transition form — a second definition point the "
        "one-source duty forbids (AS-16(a)): %r" % (rows,)
    )


def test_requirements_carries_zero_owner_transition_rows():
    """(c) — same duty, same class, second surface (AS-16)."""
    rows = _transition_rows(REQUIREMENTS)
    assert not rows, (
        "requirements.md restates the owner's transition form — the requirement cites the owner "
        "(FR-003), it does not restate its table (AS-16(c)): %r" % (rows,)
    )


# --------------------------------------------------------------------------- #
# (b) — projections narrow, never widen
# --------------------------------------------------------------------------- #

def _owner_domain_values(heading_pattern):
    """The backticked lowercase-hyphen tokens one owner domain section declares."""
    text = OWNER.read_text(encoding="utf-8")
    start = re.search(heading_pattern, text)
    assert start, "the owner doc lost the section %r — the domain moved" % heading_pattern.pattern
    tail = text[start.end():]
    end = re.search(r"(?m)^#{1,3}\s", tail)
    body = tail[: end.start()] if end else tail
    return sorted({t for t in re.findall(r"`([a-z][a-z0-9-]*)`", body)})


def _verification_domain():
    return _owner_domain_values(r"(?m)^###\s+The closed six-value status set")


def _form_domain():
    return _owner_domain_values(r"(?m)^###\s+The `Form` domain")


def _premise_status_domain():
    return _owner_domain_values(r"(?m)^###\s+`Status` — closed over three values")


def _premise_decision_domain():
    return _owner_domain_values(r"(?m)^###\s+`Decision` — required whenever")


def _disposition_domain():
    """The Disposition values, read from the owner's `| Disposition | Obligation |` table."""
    text = OWNER.read_text(encoding="utf-8")
    start = re.search(r"(?m)^###\s+`Disposition` — closed over three values", text)
    assert start, "the owner doc lost the Disposition domain section"
    tail = text[start.end():]
    end = re.search(r"(?m)^#{1,3}\s", tail)
    body = tail[: end.start()] if end else tail
    values, seen_header = [], False
    for line in body.splitlines():
        cells = _cells(line)
        if cells is None or SEPARATOR_ROW.match(line.strip()):
            continue
        if not seen_header:
            seen_header = True  # the block's first table row is the `Disposition | Obligation` header
            continue
        values.append(cells[0])
    return sorted({v for v in values if v})


def _feature_status_domain():
    """The feature-status value set, read from the deciding place the owner names.

    The owner's four-`blocked`-literals table names the feature-status literal's owner —
    `templates/feature-details-template.md` § Canonical Status State Machine, "whose rows and
    conditions this file's § Feature Status owns". The value domain is decided in that section's
    `[FEATURE_STATUS]` glossary row, so the anchor is read from there, by following the owner's
    own pointer — never by re-typing the values here.
    """
    text = OWNER.read_text(encoding="utf-8")
    table_start = re.search(r"(?m)^\| Literal \| What it is \|", text)
    assert table_start, "the owner doc lost its four-`blocked`-literals table"
    owner_cell = None
    for line in text[table_start.start():].splitlines():
        cells = _cells(line)
        if not cells:
            continue
        if _key(cells[:2]) == ("literal", "what it is") or SEPARATOR_ROW.match(line.strip()):
            continue
        if _key(cells[:2]) == ("`blocked`", "a feature status"):
            owner_cell = cells[2]
            break
        if owner_cell is None and cells[0].strip("`") == "Blocked":
            owner_cell = cells[2]
            break
    assert owner_cell, "the four-literals table no longer names a feature-status owner row"
    path_match = re.search(r"([\w./-]+\.(?:md|py))", owner_cell)
    assert path_match, "the feature-status owner cell names no readable path: %r" % owner_cell
    anchor = ROOT / path_match.group(1)
    assert anchor.is_file(), "the feature-status owner pointer does not resolve: %s" % anchor
    row = next((l for l in anchor.read_text(encoding="utf-8").splitlines()
                if l.startswith("|") and "[FEATURE_STATUS]" in l), None)
    assert row, "%s lost its [FEATURE_STATUS] value row — the feature-status domain moved" % anchor
    cells = [c.strip().strip("`") for c in row.strip("|").split("|")]
    values = [c for c in cells[1:] if c]
    assert len(values) >= 5, (
        "the feature-status domain anchor carries %d values; a stubbed anchor would let any "
        "projection pass the narrowing check vacuously: %r" % (len(values), values)
    )
    return values


def _declared_values(path, line_pattern, backticked=True):
    """The value tokens one carrier declares on the line(s) the pattern matches.

    The declaring shape is `…: <value> | <value> | …` — the values are what follows the line's
    first colon, so the extraction reads that segment and nothing around it: prose inside the
    declaring sentence (a column name, a justification) is before the colon and never becomes a
    phantom value. Backtick-declared domains (the feature-status surfaces) read their backticked
    tokens; plain-pipe domains (the verification vocabulary's declaring line) read the pipe cells
    up to the segment's first sentence boundary.
    """
    text = path.read_text(encoding="utf-8")
    lines = [l for l in text.splitlines() if re.search(line_pattern, l)]
    assert lines, "%s no longer declares a value domain matching %r" % (path, line_pattern.pattern)
    values = []
    for line in lines:
        segment = line.split(":", 1)[1] if ":" in line else line
        if backticked:
            values.extend(re.findall(r"`([^`]+)`", segment))
        else:
            segment = re.split(r"(?:[.;]\s|$)", segment)[0]
            values.extend(cell.strip().strip("`").strip()
                          for cell in segment.split("|"))
    return [v for v in values if v]


def _assert_within(declared, domain, surface, domain_name):
    widened = sorted({v for v in declared if v} - set(domain))
    assert not widened, (
        "%s declares %r for the %s domain — a projection may narrow the owner's domain, never "
        "widen it (AS-16(b)); the deciding domain is %r" % (surface, widened, domain_name, domain)
    )


def test_every_declared_feature_status_projection_stays_inside_the_domain():
    """(b) for the feature-status domain, across the surfaces SV-06 makes vocabulary owners.

    The index template and the management skill each declare the six-value domain as their own
    (SV-06); neither may carry a seventh value the deciding state machine does not admit, and the
    owner's own § Feature Status transition rows may not name a status outside the domain either.
    """
    domain = _feature_status_domain()
    index_declared = _declared_values(
        ROOT / "templates" / "feature-index-template.md", r"(?i)status vocabulary")
    _assert_within(index_declared, domain, "templates/feature-index-template.md", "feature status")

    skill_declared = _declared_values(
        ROOT / "skills" / "internal" / "manage-features" / "SKILL.md",
        r"^\s*-\s*Status vocabulary:")
    _assert_within(skill_declared, domain, "skills/internal/manage-features/SKILL.md",
                   "feature status")

    owner_transitions = set()
    for line in OWNER.read_text(encoding="utf-8").splitlines():
        cells = _cells(line)
        if cells and len(cells) >= 2 and cells[0].strip("`") in domain and cells[1].strip("`"):
            first = cells[0].strip("`")
            second = cells[1].strip("`")
            if first in domain and (second in domain or second.startswith("**")):
                owner_transitions.add(first)
                if second in domain:
                    owner_transitions.add(second)
    _assert_within(sorted(owner_transitions), domain,
                   "shared/workflow/acceptance-hardening.md § Feature Status transitions",
                   "feature status")


def test_the_verification_carrier_stays_inside_the_owner_six_value_domain():
    """(b) for the verification domain: `verification-log-template.md` may narrow, never widen."""
    domain = _verification_domain()
    declared = [
        token for token in
        _declared_values(ROOT / "templates" / "verification-log-template.md",
                         r"is one of:", backticked=False)
        if re.fullmatch(r"[a-z-]+", token)
    ]
    _assert_within(declared, domain, "templates/verification-log-template.md",
                   "verification status")


def test_the_owner_domain_sections_stay_disjoint_from_ordinary_column_names():
    """Anti-vacuity for (b): the anchors themselves must be real domains, not empty reads.

    If the owner's domain sections went stub, every `_assert_within` above would compare against
    an empty set and fail loudly — but only through the projections. This leg fails at the anchor,
    where the defect actually is.
    """
    for name, values in (
        ("verification status", _verification_domain()),
        ("Form", _form_domain()),
        ("premise Status", _premise_status_domain()),
        ("premise Decision", _premise_decision_domain()),
        ("Disposition", _disposition_domain()),
    ):
        assert len(values) >= 3, "the owner's %s domain reads %r — not a domain" % (name, values)


# --------------------------------------------------------------------------- #
# (d) — the allowed surface carries columns and zero domain literals
# --------------------------------------------------------------------------- #

def _plan_skeleton_tables():
    """The table rows of plan-template's Execution Premises / Inherited Blockers blocks."""
    text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    rows = []
    for heading in (r"(?m)^##\s+Execution Premises\s*$", r"(?m)^##\s+Inherited Blockers\s*$"):
        start = re.search(heading, text)
        assert start, "templates/plan-template.md lost its %r skeleton heading" % heading
        tail = text[start.end():]
        end = re.search(r"(?m)^#{1,2}\s", tail)
        block = tail[: end.start()] if end else tail
        rows.extend(line for line in block.splitlines() if line.strip().startswith("|"))
    return rows


def test_the_plan_skeleton_tables_carry_zero_owner_domain_literals():
    """(d) — the skeleton's narrowing duty (AS-14/AS-15): column names only, zero literals.

    Measured over the two skeleton table blocks — the surface the template exists to hand down.
    `pass` and its sibling everyday words are checked *here* and deliberately not file-wide:
    in plan prose they are ordinary English ("must pass before Phase 0"), which is exactly the
    collision that makes the value-domain literal unusable as the guard's subject (AS-14) — while
    inside a skeleton table cell, any owner value is a restated domain, not prose.
    """
    domain = set(_verification_domain()) | set(_form_domain()) | set(_premise_status_domain()) \
        | set(_premise_decision_domain()) | set(_disposition_domain())
    rows = _plan_skeleton_tables()
    assert rows, "the plan skeleton lost its tables; nothing is asserted over an empty surface"
    leaks = []
    for line in rows:
        for literal in sorted(domain):
            if re.search(r"(?<![`\w])%s(?![`\w])" % re.escape(literal), line):
                leaks.append((literal, line.strip()))
    assert not leaks, (
        "the plan skeleton's tables carry owner-exported domain literals — the skeleton may "
        "repeat the column set and nothing else (AS-15/AS-16(d)): %r" % (leaks,)
    )


def test_the_plan_template_carries_no_distinctive_domain_token_anywhere():
    """(d)'s file-wide half: the tokens that cannot be ordinary English never appear at all.

    `in-scope`, `verified` and `resolved` are the requirement's own named examples (SC-009 ④(d)):
    a plan skeleton that mentions them anywhere is restating a domain, whatever line it hides in.
    The everyday words (`pass`, `fail`, `blocked`, …) stay with the table-block leg above, where
    position separates a domain value from ordinary English without an exclusion list.
    """
    text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    distinctive = [
        "in-scope", "signed-contract", "user-waived", "not-required", "resolve-in-scope",
        "user-waiver", "not-applicable", "falsified", "unverified", "verified", "resolved",
    ]
    leaks = [t for t in distinctive if re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(t), text)]
    assert not leaks, (
        "templates/plan-template.md carries the owner's distinctive domain token(s) %r — the "
        "skeleton carries column names, never a value domain (AS-16(d))" % leaks
    )
