"""Contract tests for Feature 082 US4 — one owner, a closed membership table, no copied rules.

Owns the *ownership* face of
``.specify/specs/082-mechanism-policy-separation/contracts/owner-document.contract.md``
(OD-07 / OD-08) and the cross-check ``data-model.md`` § GM-03 row V-19 names. The
membership ruling itself lives in ``shared/definitions/mechanism-policy-definitions.md``
(the owner); this module only asserts that the ruling is **closed**, **recomputable by a
third party** and **quotes no neighbour owner's rules**.

Legs:

* **OD-07 membership table** — exactly three ``included`` rows, two ``excluded`` rows and
  one ``command-surface`` row; the C1 predicate quoted verbatim from
  ``requirements.md`` § Constraints; each exclusion reason hits the same predicate and
  names the ``improve-skills`` channel; the predicate-change consequence sentence present.
* **V-19 cross-check** — the ``included`` set equals the skill directories implied by the
  allowed-difference set registered in ``data-model.md`` § GM-03 rows 1–8 (parsed, never
  copied).
* **OD-08 boundaries** — the six named neighbour owners are listed with their owned fact,
  and none of their rule literals appears in the owner document (including
  ``dogfooding-definitions.md`` § 1's own definition, which MUST remain unrewritten).

Red-first (Constitution IV / GM-01): before T005/T006 land the legs red as "artifact
missing". Every shape assertion carries a **negative case** (GM-07): the same assertion
function runs against a ``tmp_path`` copy broken on purpose and must turn red.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

OWNER_REL = Path("shared/definitions/mechanism-policy-definitions.md")
REQUIREMENTS_REL = Path(".specify/specs/082-mechanism-policy-separation/requirements.md")
DATA_MODEL_REL = Path(".specify/specs/082-mechanism-policy-separation/data-model.md")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _read(path: Path) -> str:
    assert path.is_file(), "artifact missing: %s" % path
    return path.read_text(encoding="utf-8")


def _section(text: str, title: str) -> str:
    """Return the body of the ``## <title>`` section (heading level 2), or assert."""
    m = re.search(r"^## %s\s*$" % re.escape(title), text, re.MULTILINE)
    assert m, "section not found: %r" % title
    rest = text[m.end():]
    nxt = re.search(r"^## ", rest, re.MULTILINE)
    return rest[: nxt.start()] if nxt else rest


def _table_rows(block: str) -> list[list[str]]:
    """Return each markdown table row as a cell list; header and rule rows dropped."""
    rows: list[list[str]] = []
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        rows.append(cells)
    return rows[1:] if rows else rows


def _c1_predicate() -> str:
    """Read the C1 predicate verbatim out of requirements.md § Constraints."""
    text = _read(REPO_ROOT / REQUIREMENTS_REL)
    m = re.search(r"\*\*C1（[^）]*）\*\*：(.+?)(?:\n\n|\n- )", text, re.DOTALL)
    assert m, "artifact missing: requirements.md carries no C1 constraint paragraph"
    body = m.group(1)
    # The predicate is the sentence up to its first full stop, bold markers stripped.
    predicate = body.split("。")[0].replace("**", "").strip()
    assert predicate, "the C1 predicate could not be extracted"
    return predicate


# --------------------------------------------------------------------------- #
# OD-07 — the closed membership table
# --------------------------------------------------------------------------- #
MEMBERSHIP_HEADER = ("流程", "产出", "裁定", "理由/接线位置")
EXPECTED_INCLUDED = {"create-skills", "improve-skills", "merge-skills"}
EXPECTED_EXCLUDED = {"coaching-skills", "run-skills"}
IMPROVE_CHANNEL = "improve-skills"
VALUE_DOMAIN = ("included", "excluded")


def parse_membership(owner_text: str) -> dict:
    """Parse the membership table into its three ruled groups."""
    block = _section(owner_text, "Meta-layer Membership")
    rows = [r for r in _table_rows(block) if len(r) == 4 and r[0] != "流程"]
    groups: dict = {"included": [], "excluded": [], "command-surface": []}
    for cells in rows:
        ruling = cells[2].strip("` ")
        groups.setdefault(ruling, []).append(cells)
    return groups


def assert_membership_closed(owner_text: str) -> list[str]:
    """Return the list of membership-table violations (empty means closed and consistent)."""
    problems: list[str] = []
    block = _section(owner_text, "Meta-layer Membership")
    header = [r for r in _table_rows(block) if r[0] == "流程"] if "流程" in block else []
    raw_header = None
    for line in block.splitlines():
        stripped = line.strip()
        if stripped.startswith("| 流程"):
            raw_header = tuple(c.strip() for c in stripped.strip("|").split("|"))
            break
    if raw_header != MEMBERSHIP_HEADER:
        problems.append(
            "membership table header is %r, expected the fixed shape %r"
            % (raw_header, MEMBERSHIP_HEADER)
        )

    groups = parse_membership(owner_text)
    included = {cells[0].strip("` ") for cells in groups.get("included", [])}
    excluded = {cells[0].strip("` ") for cells in groups.get("excluded", [])}
    surface = [cells for cells in groups.get("command-surface", [])]

    if included != EXPECTED_INCLUDED:
        problems.append(
            "`included` set is %s — the closed set is exactly %s (OD-07: the table is a "
            "ruling result, not a list a consumer may extend)"
            % (sorted(included), sorted(EXPECTED_INCLUDED))
        )
    if excluded != EXPECTED_EXCLUDED:
        problems.append(
            "`excluded` set is %s — the closed set is exactly %s"
            % (sorted(excluded), sorted(EXPECTED_EXCLUDED))
        )
    if len(surface) != 1:
        problems.append("expected exactly one command-surface row, found %d" % len(surface))
    else:
        name = surface[0][0].strip("` ")
        if "speckit.skills" not in name:
            problems.append("the command-surface row names %r, expected /speckit.skills" % name)

    unknown = set(groups) - set(VALUE_DOMAIN) - {"command-surface"}
    if unknown:
        problems.append(
            "the ruling column carries values outside the closed domain %s: %s"
            % (VALUE_DOMAIN, sorted(unknown))
        )

    for cells in groups.get("excluded", []):
        reason = cells[3]
        if IMPROVE_CHANNEL not in reason:
            problems.append(
                "the %r exclusion reason does not name the %r channel (FR-014)"
                % (cells[0].strip("` "), IMPROVE_CHANNEL)
            )
        if "不命中谓词" not in reason and "does not hit the predicate" not in reason.lower():
            problems.append(
                "the %r exclusion reason does not hit the C1 predicate (OD-07)"
                % cells[0].strip("` ")
            )

    if "全表重算" not in block:
        problems.append(
            "the owner does not state the predicate-change consequence (a changed predicate "
            "recomputes the whole table, never one row)"
        )
    if "唯一依据" not in block:
        problems.append("the owner does not declare the C1 predicate to be the sole basis")
    return problems


def test_od07_membership_table_is_closed_and_recomputable():
    problems = assert_membership_closed(_read(REPO_ROOT / OWNER_REL))
    assert not problems, "OD-07 violations:\n- %s" % "\n- ".join(problems)


def test_od07_predicate_is_quoted_verbatim_from_requirements():
    owner_text = _read(REPO_ROOT / OWNER_REL)
    block = _section(owner_text, "Meta-layer Membership")
    quoted = [ln for ln in block.splitlines() if ln.strip().startswith(">")]
    assert quoted, "artifact missing: the owner quotes no predicate"
    predicate = _c1_predicate()
    joined = " ".join(quoted).replace("**", "").replace("`", "")
    assert predicate in joined, (
        "the quoted predicate does not match requirements § Constraints C1 verbatim:\n"
        "  requirements: %r\n  owner quote : %r" % (predicate, joined.strip())
    )


def test_v19_included_set_equals_the_allowed_difference_skill_dirs():
    model = _read(REPO_ROOT / DATA_MODEL_REL)
    gm03 = _section(model, "GM-03 — 允许差异集（SC-003 封闭集声明，供给 `contracts/guard-and-measurement.contract.md` 要件 3）")
    rows = _table_rows(gm03)
    registered = []
    for cells in rows:
        if len(cells) < 4:
            continue
        m = re.match(r"`?(skills/[^`]+)`?", cells[1])
        if m:
            registered.append((cells[0], m.group(1)))
    in_unit = [(n, p) for n, p in registered if n in {str(i) for i in range(1, 9)}]
    assert len(in_unit) == 8, (
        "artifact missing: GM-03 rows 1–8 must be the allowed-difference set inside the "
        "comparison unit, found %d rows" % len(in_unit)
    )
    # GM-03 rows 1–8 involve four external skill directories: the three `included` members
    # AND the two `excluded` members' reference-coordinate rewrites (rows 7 and 8, SW-05).
    # V-19 is a cross-check between two *different* facts — "which flows are judged" versus
    # "whose files are allowed to differ" — so the excluded members are subtracted, never
    # required to disappear from the allowed set.
    involved = set()
    for _, path in in_unit:
        parts = path.split("/")
        if path.startswith("skills/external/"):
            involved.add(parts[2])
        elif path.startswith("skills/internal/"):
            involved.add(parts[2])
    groups = parse_membership(_read(REPO_ROOT / OWNER_REL))
    included = {cells[0].strip("` ") for cells in groups.get("included", [])}
    excluded = {cells[0].strip("` ") for cells in groups.get("excluded", [])}
    assert excluded <= involved, (
        "GM-03 rows 1–8 must also register the excluded members' reference-coordinate "
        "rewrites (SW-05): absent %s" % sorted(excluded - involved)
    )
    implied = involved - excluded
    assert included == implied, (
        "the `included` set %s does not equal the skill directories GM-03 rows 1–8 imply "
        "once the excluded members' rewrites are removed %s (V-19)"
        % (sorted(included), sorted(implied))
    )


def test_od07_membership_table_has_one_row_per_ruled_flow():
    """No flow appears twice — a duplicate row would make "included" look satisfied while a
    second ruling silently overrides it (set comparison alone cannot see a duplicate)."""
    block = _section(_read(REPO_ROOT / OWNER_REL), "Meta-layer Membership")
    rows = [r for r in _table_rows(block) if len(r) == 4 and r[0] != "流程"]
    names = [cells[0].strip("` ") for cells in rows]
    duplicates = sorted({n for n in names if names.count(n) > 1})
    assert not duplicates, "the membership table rules %s more than once" % duplicates


def test_od07_negative_case_duplicating_a_row_turns_red(tmp_path):
    text = _read(REPO_ROOT / OWNER_REL)
    anchor = "| `merge-skills` |"
    assert anchor in text, "artifact missing: the membership table has no merge-skills row"
    row = next(ln for ln in text.splitlines() if ln.startswith(anchor))
    injected = text.replace(row, row + "\n" + row.replace("included", "excluded"), 1)
    broken = tmp_path / "mechanism-policy-definitions.md"
    broken.write_text(injected, encoding="utf-8")
    block = _section(_read(broken), "Meta-layer Membership")
    rows = [r for r in _table_rows(block) if len(r) == 4 and r[0] != "流程"]
    names = [cells[0].strip("` ") for cells in rows]
    assert len(names) != len(set(names)), "a duplicated membership row passed the duplicate check"


def test_od07_negative_case_a_fourth_included_row_turns_red(tmp_path):
    text = _read(REPO_ROOT / OWNER_REL)
    anchor = "| `merge-skills` |"
    assert anchor in text, "artifact missing: the membership table has no merge-skills row"
    injected = text.replace(
        anchor,
        "| `create-tools` | 一个新工具记录 | `included` | 产出新工具，命中谓词 |\n" + anchor,
        1,
    )
    broken = tmp_path / "mechanism-policy-definitions.md"
    broken.write_text(injected, encoding="utf-8")
    problems = assert_membership_closed(_read(broken))
    assert any("`included` set is" in p for p in problems), (
        "the negative case did not turn the closed-set assertion red: %s" % problems
    )


# --------------------------------------------------------------------------- #
# OD-08 — neighbour owners named, their rule literals absent
# --------------------------------------------------------------------------- #
# Each entry: (label the boundary table must name, owner path, rule literals that MUST NOT
# be restated in this owner's text). The label is the **owner**, not the file name: three of
# the six neighbours live in ``shared/guidelines/`` and are cited there by domain name
# (``directory-governance``, ``one-source-of-truth``, ``temp-directory-discipline``).
NEIGHBOURS = (
    (
        "dogfooding-definitions",
        "shared/definitions/dogfooding-definitions.md",
        (
            "这个实例是哪个机制产生的",
            "问题修复 (Problem Fix)",
            "机制修复 (Mechanism Fix)",
        ),
    ),
    (
        "directory-governance",
        "shared/guidelines/directory-governance.md",
        (
            "每层只做一件事",
            "one directory, one purpose",
        ),
    ),
    (
        "create-skills",
        "skills/external/create-skills/SKILL.md",
        (
            "`${SKILL_HOME}` 是技能资产根",
            "SKILL_HOME resolves to the skill directory",
        ),
    ),
    (
        "one-source-of-truth",
        "shared/guidelines/one-source-of-truth.md",
        (
            "只有三种副本合法",
            "only three duplicates are legal",
        ),
    ),
    (
        "bilingual-expression",
        "shared/guidelines/bilingual-expression.md",
        (
            "括号语言随文档主语言",
            "the bracket language follows the document",
        ),
    ),
    (
        "temp-directory-discipline",
        "shared/guidelines/temp-directory-discipline.md",
        (
            "禁止裸用系统临时目录",
            "bare system temp is forbidden",
        ),
    ),
)

# The dogfooding owner's own definition of its § 1 is the one literal the feature MUST NOT
# rewrite — it stays byte-identical to its committed form and never travels into this file.
DOGFOODING_SECTION1_MARKER = "## 1. 问题与机制 (Problem vs Mechanism)"


def assert_boundaries_named(owner_text: str) -> list[str]:
    problems: list[str] = []
    block = _section(owner_text, "Boundaries")
    for label, path, _literals in NEIGHBOURS:
        if path not in block:
            problems.append("the boundaries table does not name the owner path %r" % path)
        if label not in block:
            problems.append("the boundaries table does not name %r" % label)
    return problems


def assert_no_neighbour_rule_literals(owner_text: str) -> list[str]:
    problems: list[str] = []
    for label, _path, literals in NEIGHBOURS:
        for literal in literals:
            if literal in owner_text:
                problems.append(
                    "restates %r's rule literal %r — reach the owner, never copy it (OD-08 / C2)"
                    % (label, literal)
                )
    return problems


def assert_boundary_labels_grounded(owner_text: str) -> list[str]:
    """Each boundary row must point the label at its owner: the stem the project names it by.

    A label is a pointer, not a name this document may coin. For a ``shared/guidelines/``
    neighbour the project convention is the **domain stem** (``one-source-of-truth``, no
    ``.md``); a table that labels it ``one-source-of-truth.md`` gives a reader a file name
    where the naming convention says domain name (Grounded Naming / OD-08).
    """
    block = _section(owner_text, "Boundaries")
    problems: list[str] = []
    for label, path, _literals in NEIGHBOURS:
        row = next((ln for ln in block.splitlines() if path in ln), None)
        if row is None:
            problems.append("no boundary row names %r" % path)
            continue
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) != 3:
            problems.append("the %r row does not carry exactly three cells" % path)
            continue
        first = cells[0]
        stem = Path(path).stem
        if path.startswith("shared/guidelines/"):
            if ("`%s.md`" % stem) in first or ("`%s.md`" % label) in first:
                problems.append(
                    "the %r row labels the neighbour by file name instead of %r" % (path, stem)
                )
        if "§" not in cells[2] and "本文" not in cells[2]:
            problems.append(
                "the %r row's answer cell names no section of either side — the boundary is "
                "a pointer to a location, not a sentence" % path
            )
    return problems


def test_od08_boundary_labels_are_the_owners_not_invented_names():
    problems = assert_boundary_labels_grounded(_read(REPO_ROOT / OWNER_REL))
    assert not problems, "OD-08 violations:\n- " + "\n- ".join(problems)


def test_od08_negative_case_a_bare_file_name_label_turns_red(tmp_path):
    text = _read(REPO_ROOT / OWNER_REL)
    broken_text = text.replace(
        "`shared/guidelines/one-source-of-truth.md`",
        "`one-source-of-truth.md` (见 `shared/guidelines/one-source-of-truth.md`)",
        1,
    )
    assert broken_text != text, "artifact missing: the one-source-of-truth row is absent"
    broken = tmp_path / "mechanism-policy-definitions.md"
    broken.write_text(broken_text, encoding="utf-8")
    problems = assert_boundary_labels_grounded(_read(broken))
    assert any("one-source-of-truth" in p for p in problems), (
        "a bare file-name label did not turn the assertion red: %s" % problems
    )


def test_od08_six_named_neighbour_owners_are_boundaried():
    problems = assert_boundaries_named(_read(REPO_ROOT / OWNER_REL))
    assert not problems, "OD-08 violations:\n- %s" % "\n- ".join(problems)


def test_od08_no_neighbour_rule_literal_is_restated():
    problems = assert_no_neighbour_rule_literals(_read(REPO_ROOT / OWNER_REL))
    assert not problems, "OD-08 violations:\n- %s" % "\n- ".join(problems)


def test_c2_dogfooding_section1_definition_is_not_rewritten():
    dogfooding = REPO_ROOT / "shared/definitions/dogfooding-definitions.md"
    text = _read(dogfooding)
    assert DOGFOODING_SECTION1_MARKER in text, (
        "artifact missing: the dogfooding owner's § 1 marker is gone — this feature must not "
        "rewrite that definition (C2)"
    )
    owner_text = _read(REPO_ROOT / OWNER_REL)
    assert DOGFOODING_SECTION1_MARKER not in owner_text, (
        "the owner document restates the dogfooding owner's own definition (C2)"
    )


def test_od08_negative_case_restating_a_neighbour_rule_turns_red(tmp_path):
    broken = tmp_path / "mechanism-policy-definitions.md"
    broken.write_text(
        _read(REPO_ROOT / OWNER_REL) + "\n\n修复前先问：这个实例是哪个机制产生的。\n",
        encoding="utf-8",
    )
    problems = assert_no_neighbour_rule_literals(_read(broken))
    assert any("dogfooding-definitions" in p for p in problems), (
        "the negative case did not turn the neighbour-literal assertion red: %s" % problems
    )


def test_od08_negative_case_dropping_a_neighbour_row_turns_red(tmp_path):
    text = _read(REPO_ROOT / OWNER_REL)
    block = _section(text, "Boundaries")
    kept = [ln for ln in block.splitlines() if "directory-governance.md" not in ln]
    broken_text = text.replace(block, "\n".join(kept), 1)
    broken = tmp_path / "mechanism-policy-definitions.md"
    broken.write_text(broken_text, encoding="utf-8")
    problems = assert_boundaries_named(_read(broken))
    assert any("directory-governance" in p for p in problems), (
        "the negative case did not turn the boundary-row assertion red: %s" % problems
    )
