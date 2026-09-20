"""Contract test: discipline-doc — structure of the User-Facing Comprehension truth doc.

Implements ``.specify/specs/051-user-facing-comprehension/contracts/discipline-doc.md``
clauses **C-1…C-18**, and additionally carries ``contracts/gate-neutrality.md`` **C-2,
C-3, C-5, C-6** per that file's ownership table. Without this file carrying them those
four clauses would exist only in the contract document and never enter CI (the ownership
table names T003 as their sole author).

Naming: ``test_cN_*`` maps one-to-one onto discipline-doc's C-N. The four carried
gate-neutrality clauses use ``test_gn_cN_*`` so they do not collide with discipline-doc's
own C-2/C-3/C-5/C-6 numbering.

Reading C-6: the clause requires the document to *contain* the seven named H2 sections; it
does not forbid further H2 sections. C-8 separately requires a scope-limit clause and C-17
permits the observation convention to live either in its own section or under that clause,
so an eighth ``## 范围限制`` section is expected and is not a C-6 violation.

Pin hygiene: paths are existence-checked, counts derive from parsed structure or globs
rather than hard-coded literals, and the scanner's own constants are reused via importlib
instead of being restated here (precedent: ``test_ask_record_repeat.py:41,106-108``).
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path

import pytest

DOC_NAME = "user-facing-comprehension.md"   # STR-002 basename; its stem is STR-005's marker value

ROOT = Path(__file__).resolve().parents[2]
GUIDELINES = ROOT / "shared" / "guidelines"
DOC = GUIDELINES / DOC_NAME
DOC_MIRROR = ROOT / ".specify" / "shared" / "guidelines" / DOC_NAME
SCANNER = ROOT / "scripts" / "python" / "scan-confirmation-gates.py"
SPEC_DIR = ROOT / ".specify" / "specs" / "051-user-facing-comprehension"
NOTES = SPEC_DIR / "notes" / "pre-change-measurements.md"

AMBIENT_HEADING = "## User-Facing Comprehension"   # STR-004
AMBIENT_POINTER = f".specify/shared/guidelines/{DOC_NAME}"  # STR-001

# C-6: the seven H2 section names, verbatim and in a closed tuple.
SEVEN_SECTIONS = (
    "许可行话(白名单)",
    "禁用行话(黑名单)",
    "上下文下限",
    "上下文上限与裁决顺序",
    "机械判据",
    "面向用户界面类",
    "基准读者与覆盖协议",
)

# C-15: proprietary names that must not leak into a shipped surface.
FORBIDDEN_NAMES = ("spec-kit", "specify-cli", "specify_cli", "cloud-native-ai")

# FR-005's five whitelist categories, by a distinctive fragment of each.
WHITELIST_CATEGORIES = (
    "已先行使用",        # ① a term the reader already used in this consumption unit
    "canonical",         # ② glossary canonical term, annotated in place at first use
    "逐字键入",          # ③ identifiers the reader must type or copy verbatim
    "业务术语",          # ④ the reader's own project/domain vocabulary
    "输出格式自身定义",   # ⑤ short forms defined and named by the output format itself
)

# FR-006's four blacklist categories.
BLACKLIST_CATEGORIES = (
    "用户视角途径",      # ① engine/script call form when a user-facing path exists
    "内部标识",          # ② internal identifiers leaking into reader-facing prose
    "无就地注解",        # ③ abbreviation first used in the unit without in-place annotation
    "代码符号名",        # ④ a code symbol name standing in for a behavioural concept
)

# FR-009's context floor items.
FLOOR_ITEMS = ("为何此刻出现", "将改变什么", "用户可以做什么")
FLOOR_GATE_ITEM = "不可撤销后果"

# FR-014's eleven surface classes, by their circled numerals.
ELEVEN_CLASSES = tuple("①②③④⑤⑥⑦⑧⑨⑩⑪")

# C-18(b): declaration-shaped needles. Deliberately narrow — a bare "外部读者" would match
# 17 ordinary prose occurrences across one skill and count nothing meaningful.
BASELINE_NEEDLES = (
    re.compile(r"Written for [^.]*stakeholders"),
    re.compile(r"外部读者不读代码也能看懂"),
)
BASELINE_SCAN_DIRS = ("shared", "templates", "skills")
# Mechanical copies and generated trees are exempt: they are regenerated, never authored.
BASELINE_SCAN_EXEMPT = (
    ".specify/", ".claude/", ".github/", ".qoder/", ".opencode/", "docs/public/",
)


def _text(path: Path) -> str:
    """Read a file, letting a missing artifact surface as FileNotFoundError.

    Unguarded on purpose: at red-first time (T005) the failure reason must read as
    "artifact missing", not as an assertion that was written wrong.
    """
    return path.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    """Body of an H2 section, up to the next H2 or EOF."""
    m = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    assert m, f"missing H2 section: ## {heading}"
    return m.group(1)


def _list_items(body: str) -> list[str]:
    """Top-level list items (bullet or numbered) in a section body."""
    return [ln for ln in body.splitlines() if re.match(r"^\s*(?:[-*]|\d+[.)])\s+\S", ln)]


def _load_scanner():
    """Load the real gate scanner and reuse its constants — never restate them here."""
    spec = importlib.util.spec_from_file_location("_scan_gates_ufc", SCANNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _base_sha() -> str:
    m = re.search(r"^BASE_SHA=([0-9a-f]{40})$", _text(NOTES), re.M)
    assert m, f"BASE_SHA not recorded in {NOTES.relative_to(ROOT)} (T001 must run first)"
    return m.group(1)


def _end_sha() -> str:
    """Upper bound of this feature's commit span, recorded when it closed.

    Required, not optional: an absent end bound silently degrades C-5/C-6 back to
    `git diff BASE_SHA` against the **live worktree**, which is a claim about every
    future change to those paths rather than about this feature. That half-open form
    is what made both clauses go red on the first later edit to `scripts/` after this
    feature was merged — green for the feature they judged, red for work they never
    saw. Failing loudly here keeps the range honest.
    """
    m = re.search(r"^FEATURE_END_SHA=([0-9a-f]{40})$", _text(NOTES), re.M)
    assert m, (
        f"FEATURE_END_SHA not recorded in {NOTES.relative_to(ROOT)} — the feature's "
        "comparison range has no upper bound, so C-5/C-6 would judge the live worktree "
        "instead of this feature's commit span"
    )
    return m.group(1)


def _changed_files(base: str, paths: list[str], end: str | None = None) -> list[str]:
    """Paths added or modified between ``base`` and ``end``, or against the live worktree
    when ``end`` is None.

    ``end`` given (the normal case once a feature has closed): a bounded ``base..end``
    diff, which is a historical fact about that span and stays true forever.

    ``end`` None (mid-feature): ``git diff <sha>`` reaches tracked paths only, so a
    brand-new file joins the change set only once committed — and mid-feature, this
    feature's own artifacts are precisely the uncommitted ones. Omitting untracked
    paths would leave both clauses blind in the only window where they can fire, so
    the untracked half is unioned in.
    """
    revision = f"{base}..{end}" if end else base
    tracked = subprocess.run(
        ["git", "diff", "--name-only", "--no-renames", "--diff-filter=ACMR", revision, "--", *paths],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    if end:
        # An untracked file is in no commit, so it cannot belong to a closed range.
        return sorted({ln for ln in tracked.splitlines() if ln.strip()})
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "--", *paths],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    return sorted({ln for ln in (tracked + untracked).splitlines() if ln.strip()})


# --- existence and mirror (C-1, C-2, C-3) ---


@pytest.mark.contract
def test_c1_doc_exists():
    assert DOC.is_file(), f"truth document missing: {DOC.relative_to(ROOT)}"


@pytest.mark.contract
def test_c2_mirror_is_byte_identical():
    assert DOC_MIRROR.is_file(), (
        f"mirror missing: {DOC_MIRROR.relative_to(ROOT)} — run "
        "`python3 scripts/python/sync-mirrors.py --write --only shared`"
    )
    assert DOC.read_bytes() == DOC_MIRROR.read_bytes(), "truth-doc mirror drift"


@pytest.mark.contract
def test_c3_filename_is_exact_and_not_renamed():
    # Two independent literals for one fact, so a typo in either fails: the path constant
    # and the STR-005 marker value the observation protocol retrieves entries by.
    assert DOC.stem == "user-facing-comprehension", (
        f"the basename is the source of the STR-005 observation marker; got {DOC.stem!r}"
    )

    # The normative half of C-3 is "MUST NOT be renamed", which a constant check cannot
    # see — it has to be caught against the tree, and it must fail *here* rather than only
    # in C-1, because "missing" and "renamed" have different repairs.
    variants = sorted(
        p.name for p in GUIDELINES.glob("*.md")
        if "comprehension" in p.stem and p.name != DOC_NAME
    )
    assert not variants, (
        f"shared/guidelines/ holds a renamed variant of the truth document: {variants}. "
        f"The name is pinned to {DOC_NAME!r} because STR-005's observation marker takes its "
        "value from the basename — rename the marker's source and every observation recorded "
        "under it stops being retrievable."
    )
    assert DOC.is_file(), (
        f"truth document missing at its canonical name: {DOC.relative_to(ROOT)}"
    )


# --- ownership declaration (C-4, C-5) ---


@pytest.mark.contract
def test_c4_ownership_declaration_in_first_eight_lines():
    head = "\n".join(_text(DOC).splitlines()[:8])
    assert re.search(r"single source of truth|唯一定义处|唯一真源", head, re.I), (
        "C-4(a): the first 8 lines must declare single-source-of-truth ownership"
    )
    assert re.search(r"MUST NOT copy|MUST NOT 复制", head), (
        "C-4(b): the declaration must state the reference-not-copy obligation"
    )
    assert "instructions-template.md" in head and AMBIENT_HEADING in head, (
        "C-4(c): the declaration must name where its ambient pointer lives"
    )


@pytest.mark.contract
def test_c5_failure_statement_covers_both_surfaces():
    head = "\n".join(_text(DOC).splitlines()[:20])
    assert re.search(r"解码|decode", head), "C-5: the failure statement must cover term-decoding"
    assert re.search(r"翻页|page", head), "C-5: it must also cover paging-for-context"
    assert re.search(r"自信|confiden", head), (
        "C-5: the decoding surface fails as a *confidently wrong* answer — say so"
    )


# --- the seven sections (C-6, C-7, C-8) ---


@pytest.mark.contract
def test_c6_seven_sections_present_verbatim():
    headings = re.findall(r"(?m)^## (.+)$", _text(DOC))
    missing = [name for name in SEVEN_SECTIONS if name not in headings]
    assert not missing, f"C-6: missing H2 sections (names are verbatim): {missing}"


@pytest.mark.contract
def test_c7_rfc2119_keywords_present():
    text = _text(DOC)
    assert re.search(r"\bMUST\b", text), "C-7: no uppercase MUST"
    assert "MUST NOT" in text, "C-7: no MUST NOT"


@pytest.mark.contract
def test_c8_scope_limit_clause_present():
    text = _text(DOC)
    assert re.search(r"范围限制|Scope limits", text), "C-8: no scope-limit clause"
    # The clause must name the machinery it refuses, not merely assert "no new machinery".
    for refused in ("lint", "评分", "成熟度报告", "台账"):
        assert refused in text, f"C-8: the scope limit must name {refused!r} as refused"
    assert re.search(r"one-source-of-truth\.md", text), (
        "C-8: the clause must cite the house precedent it aligns with"
    )


# --- content floors (C-9 … C-13) ---


@pytest.mark.contract
def test_c9_whitelist_floor_and_categories():
    body = _section(_text(DOC), SEVEN_SECTIONS[0])
    items = _list_items(body)
    assert len(items) >= 5, f"C-9: whitelist has {len(items)} items, need >= 5"
    for fragment in WHITELIST_CATEGORIES:
        assert fragment in body, f"C-9: whitelist omits FR-005 category {fragment!r}"
    assert re.search(r"白名单之外.*违规|一律按违规", body), (
        "C-9: the whitelist must state that anything outside it is a violation"
    )
    assert "该消费单元内" in body, (
        "C-9: the consumption-unit qualifier MUST NOT be simplified to bare '首次出现' — "
        "dropping it silently reverts per-unit accounting to per-session accounting (FR-008)"
    )


@pytest.mark.contract
def test_c10_blacklist_floor_categories_and_instance_source():
    body = _section(_text(DOC), SEVEN_SECTIONS[1])
    items = _list_items(body)
    assert len(items) >= 4, f"C-10: blacklist has {len(items)} items, need >= 4"
    for fragment in BLACKLIST_CATEGORIES:
        assert fragment in body, f"C-10: blacklist omits FR-006 category {fragment!r}"
    assert "该消费单元内" in body, "C-10: same qualifier constraint as C-9"
    # The instance source for category ② must be named, and it must be a real path.
    m = re.search(r"(skills/summarize-project/references/reporting-playbook\.md)", body)
    assert m, "C-10: the blacklist must name category ②'s instance source"
    assert (ROOT / m.group(1)).is_file(), f"C-10: named instance source does not exist: {m.group(1)}"
    assert re.search(r"§\s*1\.7|1\.7", body), "C-10: name the section, not just the file"


@pytest.mark.contract
def test_c11_context_floor_items_and_path_reference():
    body = _section(_text(DOC), SEVEN_SECTIONS[2])
    items = _list_items(body)
    assert len(items) >= 3, f"C-11: context floor has {len(items)} items, need >= 3"
    for fragment in FLOOR_ITEMS:
        assert fragment in body, f"C-11: floor omits {fragment!r}"
    assert FLOOR_GATE_ITEM in body, "C-11: gate-class surfaces need the irreversibility item"
    assert "confirmation-gates.md" in body, (
        "C-11: the execution-report triad must be reached by path reference"
    )
    assert "执行报告" in body, "C-11: name what is being referenced"


@pytest.mark.contract
def test_c12_ceiling_constraints_adjudication_and_accepted_cost():
    body = _section(_text(DOC), SEVEN_SECTIONS[3])
    items = _list_items(body)
    assert len(items) >= 3, f"C-12: ceiling section has {len(items)} items, need >= 3"
    assert "路径引用" in body, "C-12: the carrying form must be facts plus path reference"
    assert "单行" in body, "C-12: the non-blocking-one-line constraint must be present"
    assert re.search(r"机器管理数据|原文", body), "C-12: must forbid injecting raw managed data"
    # Two adjudications, matching FR-012's two named conflicts.
    assert "单行" in body and "摘要优先" in body, (
        "C-12: both of FR-012's conflicts (floor vs one-line, floor vs summary-first) "
        "must be adjudicated"
    )
    adjudications = re.findall(r"裁决", body)
    assert len(adjudications) >= 2, (
        f"C-12: found {len(adjudications)} adjudications, need >= 2"
    )
    # The accepted cost must be recorded explicitly, with its acceptance condition.
    assert "没有长度界" in body or "无长度界" in body, (
        "C-12: must record clarify R2-Q3=A's accepted cost — two surfaces have no length bound"
    )
    assert "形态" in body, "C-12: the acceptance condition is 'bound the form, not the length'"


@pytest.mark.contract
def test_c13_verdict_questions_baselines_and_consumption_unit():
    text = _text(DOC)

    verdict_body = _section(text, SEVEN_SECTIONS[4])
    questions = re.findall(r"(?m)^\s*(?:[-*]|\d+[.)])\s+.*\?\s*$", verdict_body)
    assert len(questions) >= 2, (
        f"C-13: mechanical-verdict section has {len(questions)} questions, need >= 2 "
        "(one jargon-side, one context-side)"
    )
    assert re.search(r"两个独立评审者|同一结论", verdict_body), (
        "C-13: must state the goal form — two independent reviewers reach the same verdict"
    )

    baseline_body = _section(text, SEVEN_SECTIONS[6])
    globals_found = re.findall(r"全局基准读者", baseline_body)
    assert len(globals_found) == 1, (
        f"C-13: expected exactly 1 global baseline definition, found {len(globals_found)}"
    )
    assert "声明处生效" in baseline_body, "C-13: overrides take effect where declared"
    assert re.search(r"MUST NOT 回写", baseline_body), "C-13: overrides must not be written back"

    units = re.findall(r"消费单元\s*\(consumption unit\)|`消费单元`|消费单元（consumption unit）", baseline_body)
    assert len(units) == 1, (
        f"C-13: expected exactly 1 consumption-unit definition, found {len(units)}"
    )
    assert re.search(r"按消费单元计.*而非按会话计|按消费单元计", baseline_body), (
        "C-13: the in-place annotation duty is accounted per consumption unit, not per session"
    )


@pytest.mark.contract
def test_c14_surface_class_table():
    text = _text(DOC)
    body = _section(text, SEVEN_SECTIONS[5])
    header, data_rows = _class_table(text)
    assert len(data_rows) == 11, f"C-14: expected 11 class rows, found {len(data_rows)}"

    for numeral in ELEVEN_CLASSES:
        assert any(numeral in r[0] or numeral in " ".join(r) for r in data_rows), (
            f"C-14: class {numeral} missing from the table"
        )

    # Paths are counted **from the rule-source column only**. The override column (C-18)
    # names declaration sites, which are a different set — counting the whole section body
    # would fold the two together and make the pinned 8 unsatisfiable.
    src = _column(header, "规则真源")
    paths = re.findall(r"`([a-z0-9_./-]+\.md)`", " ".join(r[src] for r in data_rows))
    assert paths, "C-14: no repo-relative rule-source paths found in the table"
    deduped = sorted(set(paths))
    assert len(deduped) == 8, (
        f"C-14: expected 8 deduplicated rule-source paths, found {len(deduped)}: {deduped}"
    )
    missing = [p for p in deduped if not (ROOT / p).is_file()]
    assert not missing, f"C-14: rule-source paths that do not exist: {missing}"

    assert re.search(r"封闭集|closed set", body), "C-14: the class set must be declared closed"
    assert re.search(r"只经修订|only by revising", body), (
        "C-14: extension must go through revising this document"
    )


# --- neutrality and gate budget (C-15, C-16) ---


@pytest.mark.contract
def test_c15_project_neutral():
    text = _text(DOC).lower()
    leaks = [name for name in FORBIDDEN_NAMES if name.lower() in text]
    assert not leaks, f"C-15: shipped surface leaks proprietary names: {leaks}"


@pytest.mark.contract
def test_c16_zero_blocking_gate_hits():
    scanner = _load_scanner()
    hits = [ln for ln in _text(DOC).splitlines() if scanner.BLOCKING_RE.search(ln)]
    assert not hits, (
        f"C-16: {len(hits)} line(s) hit BLOCKING_RE — the gate budget's integer headroom is 0, "
        f"so any hit breaks two existing contract tests. First: {hits[0][:120]!r}"
    )


# --- observation hook (C-17) ---


@pytest.mark.contract
def test_c17_observation_convention():
    text = _text(DOC)
    assert DOC.stem in text, (
        f"C-17: the observation marker literal {DOC.stem!r} (STR-005) must appear"
    )
    # All three red lines, not a subset.
    assert re.search(r"空洞观察条目|empty observation", text), "C-17: red line 1 missing"
    assert re.search(r"编造计数|fabricat", text), "C-17: red line 2 missing"
    assert re.search(r"阻塞宿主流程|block the host", text), "C-17: red line 3 missing"
    assert "token-efficiency.md" in text, (
        "C-17: the form must follow the token-efficiency marker precedent"
    )


# --- reader-baseline counting (C-18) ---


def _class_table(text: str) -> tuple[list[str], list[list[str]]]:
    """Header cells and data rows of the surface-class table (C-14 / C-18)."""
    body = _section(text, SEVEN_SECTIONS[5])
    rows = [ln for ln in body.splitlines() if ln.strip().startswith("|")]
    assert len(rows) >= 2, "the surface-class table is missing (header + rows expected)"
    parsed = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    header, rest = parsed[0], parsed[1:]
    data = [r for r in rest if not all(re.fullmatch(r"[\s:-]*", c or " ") for c in r)]
    return header, data


def _column(header: list[str], needle: str) -> int:
    """Index of a column located **by header name**, never by position.

    C-14 counts rule-source paths while C-18 counts override sites — two different columns
    of one table. Resolving them by position would silently move an assertion onto the
    wrong column the day a column is reordered.
    """
    for i, cell in enumerate(header):
        if needle in cell:
            return i
    raise AssertionError(f"table header has no column matching {needle!r}: {header}")


def _override_cells(text: str) -> list[str]:
    header, rows = _class_table(text)
    idx = _column(header, "reader_baseline_override")
    return [r[idx] for r in rows if len(r) > idx]


def _declared_overrides(text: str) -> list[str]:
    """Override cells that actually declare something (an em dash means "not declared")."""
    return [c for c in _override_cells(text) if c and c not in ("—", "-", "–")]


@pytest.mark.contract
def test_c18a_override_registry_has_at_most_two_entries():
    text = _text(DOC)
    assert _class_table(text)[1], "C-18(a): the class table has no rows"
    # The override column is located by header name; an em dash means "not declared", so
    # counting is by **class**, not by line — one class declaring twice is still one entry.
    declared = _declared_overrides(text)
    assert len(declared) <= 2, (
        f"C-18(a): {len(declared)} classes declare a reader-baseline override, max is 2 "
        "(with C-13's single global baseline this is what makes SC-018's <= 3 hold)"
    )
    # Each declaration must name a real file, so C-18(b) can locate it mechanically.
    for cell in declared:
        m = re.search(r"`?([a-z0-9_./-]+\.md)`?", cell)
        assert m, f"C-18(a): override entry names no file: {cell!r}"
        assert (ROOT / m.group(1)).is_file(), (
            f"C-18(a): declared override site does not exist: {m.group(1)}"
        )


@pytest.mark.contract
def test_c18b_baseline_declarations_only_at_registered_sites():
    text = _text(DOC)
    registered: set[str] = set()
    for cell in _declared_overrides(text):
        m = re.search(r"`?([a-z0-9_./-]+\.md)`?", cell)
        if m:
            registered.add(m.group(1))
    assert registered, (
        "C-18(b): no override site is registered, so every declaration in the tree would "
        "count as unregistered — the needle scan cannot be evaluated"
    )

    hits: list[str] = []
    for d in BASELINE_SCAN_DIRS:
        for path in sorted((ROOT / d).rglob("*.md")):
            rel = path.relative_to(ROOT).as_posix()
            if any(part in rel for part in BASELINE_SCAN_EXEMPT):
                continue
            if rel == DOC.relative_to(ROOT).as_posix():
                continue  # the truth document itself is exempt
            try:
                content = path.read_text(encoding="utf-8")
            except OSError:
                continue
            if any(needle.search(content) for needle in BASELINE_NEEDLES):
                hits.append(rel)

    unregistered = sorted(set(hits) - registered)
    assert not unregistered, (
        f"C-18(b): reader-baseline declarations outside the registered override sites: "
        f"{unregistered}. Registered: {sorted(registered)}. Each must be converged to a "
        "pointer (C-18(c)) — a declaration elsewhere is an unregistered fourth baseline, "
        "which would make SC-018's <= 3 false."
    )


# --- carried from contracts/gate-neutrality.md (C-2, C-3, C-5, C-6) ---


@pytest.mark.contract
def test_gn_c2_gate_scan_total_unchanged():
    """Run the real scanner and assert equality — not <=, per the clause."""
    proc = subprocess.run(
        ["python3", str(SCANNER), "--root", str(ROOT), "--json"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["total"] == 23, (
        f"gate total moved to {payload['total']}; the frozen budget is 23 and the integer "
        "headroom is 0, so any new BLOCKING_RE hit in scan scope lands here"
    )
    assert payload["violations"] == [], f"violations: {payload['violations']}"


@pytest.mark.contract
def test_gn_c3_scanner_constants_unmodified():
    """Content comparison, not container comparison.

    POLICY_DOCS is a tuple of PosixPath and SELF_REL is a PosixPath, so comparing either
    against a list of str is unconditionally False — an assertion written that way is
    permanently red, or gets "fixed" into a no-op.
    """
    scanner = _load_scanner()
    assert tuple(str(p) for p in scanner.POLICY_DOCS) == (
        "shared/patterns/reconcile-pattern.md",
        "shared/patterns/interview-pattern.md",
    ), "POLICY_DOCS was modified — this feature must achieve gate neutrality by design avoidance"
    assert str(scanner.SELF_REL) == "shared/guidelines/confirmation-gates.md", "SELF_REL changed"
    assert len(scanner.BLOCKING_PATTERNS) == 17, (
        f"BLOCKING_PATTERNS has {len(scanner.BLOCKING_PATTERNS)} entries, expected 17"
    )


@pytest.mark.contract
def test_gn_c5_no_new_executable_scripts():
    """Whole-repo probe: this feature added no executable scripts outside tests/contract.

    Bounded to the feature's own commit span, so it stays a true statement about that
    span instead of becoming a prohibition on every later change to the repository.
    """
    changed = _changed_files(_base_sha(), ["."], _end_sha())
    offenders = [
        p for p in changed
        if re.search(r"\.(py|sh)$", p) and not p.startswith("tests/contract/")
    ]
    # Asserted as a filtered count so an empty match and a genuine pass are distinguishable.
    assert offenders == [], f"new executable scripts outside tests/contract/: {offenders}"
    added_tests = [p for p in changed if p.startswith("tests/contract/") and p.endswith(".py")]
    assert added_tests, (
        "sanity: this feature's own test files should appear as additions across its span; "
        "an empty set suggests the recorded BASE_SHA/FEATURE_END_SHA pair is wrong rather "
        "than that nothing was added"
    )


@pytest.mark.contract
def test_gn_c6_zero_change_surfaces_untouched():
    """Compared against a bounded BASE_SHA..FEATURE_END_SHA range, never HEAD.

    `git diff HEAD` is blind to this feature's own commits (the commit discipline requires
    committing per task) and is unconditionally vacuous under CI, where a clean checkout
    makes the worktree equal to HEAD. No extension filter either: templates/plan-template.md
    is a .md and scripts/ holds non-py/sh tracked files that a filter would let escape.
    The upper bound is what keeps this a claim about the feature rather than about the
    live tree — see _end_sha().
    """
    surfaces = ["src/specify_cli/", "scripts/", "templates/plan-template.md"]
    changed = _changed_files(_base_sha(), surfaces, _end_sha())
    assert changed == [], f"zero-change surfaces were modified: {changed}"
