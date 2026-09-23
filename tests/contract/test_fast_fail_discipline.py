"""Contract tests for the Fast Fail discipline (Feature 052).

Single guard for five contract documents under
``.specify/specs/052-fast-fail-principle/contracts/``. Function names map
one-to-one onto clause numbers, and the mapping is load-bearing:

    discipline-doc.md      C-1..C-22   -> test_c<N>_*
    ambient-section.md     C-1..C-19   -> test_a<N>_*
    constitution-export.md C-1..C-23   -> test_x<N>_*
    dispatch-injection.md  C-1..C-23, C-26 -> test_i<N>_*
    gate-neutrality.md     C-1..C-17   -> test_g<N>_*

``dispatch-injection.md`` C-24 / C-25 are behaviour-class clauses with no
artifact to assert on; they are evidenced by mutation drills recorded in the
spec's ``notes/red-first-evidence.md`` (task T039), not by pytest. Sub-clauses
(``C-1(a)``, ``C-10(a)``, ...) ride inside their parent's function.

**The underscore after the clause number is load-bearing.** ``pytest -k``
matches tokens as *substrings*, so ``-k "c1_"`` selects only ``test_c1_*``
while ``-k "c1"`` would also select ``test_c10_*`` through ``test_c19_*``.
The six verification rows in ``tasks.md`` partition this file by phase using
those underscore-suffixed tokens; renaming a function to ``test_c1a_*`` would
make its token select nothing, and an empty selection passes silently.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

# --- paths -----------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

DOC_NAME = "fast-fail.md"
DOC = ROOT / "shared" / "guidelines" / DOC_NAME
DOC_MIRROR = ROOT / ".specify" / "shared" / "guidelines" / DOC_NAME

INSTR = ROOT / "templates" / "instructions-template.md"
INSTR_LIVE = ROOT / ".specify" / "instructions.md"

SUBAGENT_DEFS = ROOT / "shared" / "definitions" / "subagent-definitions.md"
UFC_DOC = ROOT / "shared" / "guidelines" / "user-facing-comprehension.md"
TEAM_PATTERNS = ROOT / "skills" / "create-team" / "references" / "patterns.md"
CREATE_AGENT_SKILL = ROOT / "skills" / "create-agent" / "SKILL.md"
AGENTS_CMD = ROOT / "templates" / "commands" / "agents.md"
CONST_TPL = ROOT / "templates" / "constitution-template.md"
CONST_CMD = ROOT / "templates" / "commands" / "constitution.md"
CONST_LIVE = ROOT / ".specify" / "memory" / "constitution.md"
PLAN_TPL = ROOT / "templates" / "plan-template.md"

SCANNER = ROOT / "scripts" / "python" / "scan-confirmation-gates.py"
GATE_BASELINE = ROOT / ".specify" / "specs" / "050-proactive-flow-trigger" / "baseline-gates.json"
SWEEP_BASELINE = ROOT / ".specify" / "specs" / "044-reduce-confirmation-flows" / "baseline.json"

DOUBLE_LANDING_TEST = ROOT / "tests" / "contract" / "test_constitution_double_landing.py"
UFC_DOC_TEST = ROOT / "tests" / "contract" / "test_user_facing_comprehension_doc.py"
PROACTIVE_TEST = ROOT / "tests" / "contract" / "test_proactive_trigger_section.py"
SWEEP_TEST = ROOT / "tests" / "contract" / "test_confirmation_gates_sweep.py"

FACTORY_PRESETS = (
    ROOT / "agents" / "skill-verifier.agent.md",
    ROOT / "agents" / "structure-adjuster.agent.md",
)

# --- literals (Shared Strings of requirements.md are the owner) ------------

AMBIENT_HEADING = "## Fast Fail Discipline"          # [[STR-003]]
AMBIENT_POINTER = ".specify/shared/guidelines/fast-fail.md"
DOC_REL = "shared/guidelines/fast-fail.md"           # [[STR-002]]

MARKER_OBS = "[fast-fail]"                           # [[STR-001]]
MARKER_CLAUSE = "fast-fail-clause"                   # [[STR-009]]
MARKER_RETURN = "ANOMALY:"                           # [[STR-010]]
MARKER_CLEAN = "未发现异常"                            # [[STR-013]]

CLAUSE_BEGIN = "<!-- fast-fail-clause:begin -->"
CLAUSE_END = "<!-- fast-fail-clause:end -->"

MECHANICAL_TEST_FIX = (                              # [[STR-005]]
    "如果这次修复的说明里必须出现「假定」,它就不是一次修复,而是一次快速失败。"
)
BLIND_CHECK_SENTINEL = (                             # [[STR-006]]
    "被守物真的坏掉时这条检查会不会变红?答不上来,这次绿就不是证据。"
)
PRINCIPLE_TITLE = (                                  # [[STR-004]]
    "Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest)"
)

# discipline-doc.md C-7 closed tuple. Items 2 and 3 are the [[STR-011]] /
# [[STR-012]] literals owned by requirements.md's Shared Strings table.
SECTION_HEADINGS = (
    "## 分流判据",
    "## Fast Fail List(快速失败清单)",
    "## In-Passing Repair List(顺手修复清单)",
    "## 上送件与披露",
    "## 子代理派发注入",
    "## 生长闭环",
    "## 与相邻纪律的边界",
    "## 冲突裁决顺序",
    "## 范围限制",
)

FORBIDDEN_NAMES = ("spec-kit", "specify-cli", "specify_cli", "cloud-native-ai")

# The four literals C-20 requires to be pairwise non-substring. MARKER_CLEAN is
# deliberately absent: C-20 enumerates exactly these four.
C20_LITERALS = (MARKER_OBS, MARKER_CLAUSE, MARKER_RETURN, DOC_REL)


# --- helpers ---------------------------------------------------------------


def _text(path: Path) -> str:
    """Read an artifact, letting a missing one raise FileNotFoundError.

    Skeletons call this first so that, while the artifact is still absent, the
    failure reads as "artifact missing" rather than as a broken assertion.
    """
    return path.read_text(encoding="utf-8")


def _lines(path: Path) -> list[str]:
    return _text(path).splitlines()


def _unimplemented(clause: str, task: str) -> None:
    """Fail loudly. A skeleton MUST never report green."""
    pytest.fail(f"{clause}: assertion body not implemented yet (lands in {task})")


def _scanner():
    spec = importlib.util.spec_from_file_location("_ff_scan_confirmation_gates", SCANNER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _blocking_re() -> re.Pattern:
    return _scanner().BLOCKING_RE


def _section(text: str, heading: str) -> str:
    """Body of one H2 section, up to the next H2 (or EOF)."""
    lines = text.splitlines()
    out: list[str] = []
    inside = False
    for line in lines:
        if line.strip() == heading:
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if inside:
            out.append(line)
    return "\n".join(out)


# --- discipline-doc.md C-20: implemented (pure string algebra) -------------


def test_c20_marker_literals_are_mutually_disjoint():
    """C-20: the four stable literals are pairwise non-substring.

    Pure string algebra over constants -- it depends on no artifact, so it is
    green from the red-first phase onwards. FR-063 / V1.
    """
    for i, a in enumerate(C20_LITERALS):
        for b in C20_LITERALS[i + 1:]:
            assert a not in b, f"{a!r} is a substring of {b!r}"
            assert b not in a, f"{b!r} is a substring of {a!r}"
    # anti-vacuity: the set really is four distinct non-empty literals
    assert len(C20_LITERALS) == 4
    assert all(lit.strip() for lit in C20_LITERALS)


# --- discipline-doc.md C-1..C-22 (bodies land in T005 / T042 / T050) --------

ENTRY_RE = re.compile(r"^- \*\*(FF|RP)-(\d+) ")
FF_NAMED = tuple(range(2, 9))  # FF-2..FF-5 blind-check causes, FF-6..FF-8 git diff forms
GATE_DOC = ROOT / "shared" / "guidelines" / "confirmation-gates.md"
LESSONS = "docs/reference/history/00-cross-cutting-lessons.md"


def _h2_headings(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.startswith("## ")]


def _entries(text: str, heading: str, prefix: str) -> dict[int, str]:
    """Clause entries of one list section, keyed by their number."""
    out: dict[int, str] = {}
    for line in _section(text, heading).splitlines():
        m = ENTRY_RE.match(line)
        if m and m.group(1) == prefix:
            out[int(m.group(2))] = line
    return out


def test_c1_truth_source_doc_exists():
    """C-1: the truth-source document exists."""
    assert DOC.is_file(), f"missing truth-source doc: {DOC.relative_to(ROOT)}"


def test_c2_mirror_byte_identical():
    """C-2: the runtime mirror is byte-identical to the source."""
    assert DOC.is_file(), f"missing source: {DOC.relative_to(ROOT)}"
    assert DOC_MIRROR.is_file(), f"missing mirror: {DOC_MIRROR.relative_to(ROOT)}"
    assert DOC.read_bytes() == DOC_MIRROR.read_bytes(), (
        f"{DOC.relative_to(ROOT)} and {DOC_MIRROR.relative_to(ROOT)} differ; "
        "run: python3 scripts/python/sync-mirrors.py --write --only shared"
    )


def test_c3_filename_rename_guard():
    """C-3: no `*fast*fail*` filename variant other than fast-fail.md."""
    guidelines = ROOT / "shared" / "guidelines"
    found = sorted(p.name for p in guidelines.glob("*.md") if "fast" in p.name and "fail" in p.name)
    assert found == [DOC_NAME], f"rename or stray variant detected: {found} (expected only {DOC_NAME})"
    # anti-vacuity: the scan is not blind -- it does see the real file
    assert DOC_NAME in found, "sentinel: the scan found nothing at all, so it is blind, not clean"


def test_c4_ownership_first_8_lines():
    """C-4: ownership triple declared within the first 8 lines."""
    head = "\n".join(_lines(DOC)[:8])
    assert head.strip(), "the first 8 lines are empty"
    assert any(k in head for k in ("single source of truth", "唯一真源", "唯一定义处")), (
        "C-4(a): no single-source-of-truth declaration in the first 8 lines"
    )
    assert any(k in head for k in ("MUST NOT copy", "MUST NOT 复制")), (
        "C-4(b): no 'MUST NOT copy' obligation in the first 8 lines"
    )
    assert "templates/instructions-template.md" in head, (
        "C-4(c): the instructions template is not named in the first 8 lines"
    )
    assert AMBIENT_HEADING in head, (
        f"C-4(c): the ambient heading {AMBIENT_HEADING!r} is not named in the first 8 lines"
    )


def test_c5_failure_statement_first_20_lines():
    """C-5: the failure statement covers BOTH sides, as two separate regexes."""
    head = "\n".join(_lines(DOC)[:20])
    assert head.strip(), "the first 20 lines are empty"
    side_a = re.compile(r"(就地修平|修平|用户看不见|看不见)")
    side_b = re.compile(r"(下游.*(?:前提|引用)|当已验证前提)")
    assert side_a.search(head), "C-5(a): the 'silently repaired / invisible to the user' side is absent"
    assert side_b.search(head), "C-5(b): the 'downstream cites it as a verified premise' side is absent"
    assert "静默兜底" in head, "C-5: the failure is not named (静默兜底)"


def test_c6_canonical_ufc_pointer_line():
    """C-6: exactly one *canonical* UFC pointer line, in the header, declaring class ⑪.

    The canonical pointer is the line that declares which interface classes this
    file covers -- not every mention of the UFC path. FR-023 separately requires
    the surface-report section to reference that discipline for wording limits,
    so a plain path mention inside a section is legitimate; a second line
    declaring class coverage is not.
    """
    lines = _lines(DOC)
    ufc_rel = ".specify/shared/guidelines/user-facing-comprehension.md"
    canonical = [i for i, line in enumerate(lines) if ufc_rel in line and "⑪" in line]
    assert len(canonical) == 1, (
        f"C-6: expected exactly one canonical pointer line (path + class ⑪), got {len(canonical)} "
        f"at lines {[i + 1 for i in canonical]}"
    )
    idx = canonical[0]
    h2 = [i for i, line in enumerate(lines) if line.startswith("## ")]
    assert h2, "the document has no H2 section at all"
    assert idx < h2[0], (
        f"C-6: the canonical pointer line (line {idx + 1}) sits inside a criteria section "
        f"(first H2 at line {h2[0] + 1}); it belongs in the header ownership area"
    )
    # anti-vacuity: the header really does carry it, and the path is spelled correctly
    head = "\n".join(lines[:h2[0]])
    assert ufc_rel in head, "sentinel: the UFC path is absent from the header area"


def test_c7_nine_section_closed_tuple():
    """C-7: exactly the nine H2 sections, in order."""
    assert _h2_headings(_text(DOC)) == list(SECTION_HEADINGS), (
        "C-7: H2 section set/order drifted from the closed tuple.\n"
        f"  expected: {list(SECTION_HEADINGS)}\n"
        f"  actual:   {_h2_headings(_text(DOC))}"
    )


def test_c8_rfc2119_keywords():
    """C-8: RFC-2119 uppercase keywords present."""
    text = _text(DOC)
    assert re.search(r"\bMUST NOT\b", text), "C-8: no 'MUST NOT'"
    assert re.search(r"\bMUST\b", text), "C-8: no 'MUST'"


def test_c9_bilingual_h1():
    """C-9: H1 is bilingual."""
    h1 = [line for line in _lines(DOC) if line.startswith("# ")]
    assert h1, "C-9: no H1"
    assert "快速失败" in h1[0], f"C-9: H1 lacks 快速失败: {h1[0]!r}"
    assert "Fast Fail" in h1[0], f"C-9: H1 lacks 'Fast Fail': {h1[0]!r}"


def test_c10_triage_criteria_seven_items():
    """C-10 (a)-(g): the triage-criteria section carries all seven items."""
    sec = _section(_text(DOC), SECTION_HEADINGS[0])
    assert sec.strip(), f"C-10: section {SECTION_HEADINGS[0]!r} is empty"

    # (a) mechanical test literal, exactly once
    assert sec.count(MECHANICAL_TEST_FIX) == 1, (
        f"C-10(a): STR-005 must appear exactly once in the section, found {sec.count(MECHANICAL_TEST_FIX)}"
    )
    # (b) binary enumeration, no third value, no undecidable middle tier
    assert "顺手修复" in sec and "快速失败" in sec, "C-10(b): the binary enumeration is incomplete"
    for banned in ("尽量少停", "视情况", "酌情"):
        assert banned not in sec, f"C-10(b): undecidable middle tier {banned!r} present"
    # (c) the four necessary conditions, all enumerated
    for frag in ("恰有一种", "局部且可逆", "未证伪", "爆炸半径"):
        assert frag in sec, f"C-10(c): necessary condition {frag!r} missing from the enumeration"
    # (d) FR-070 precedence: criteria outrank list membership
    assert "判据优先于清单命中" in sec, "C-10(d): the criteria-outrank-list precedence is not declared"
    # (e) doubtful-strict default
    assert "存疑从严" in sec, "C-10(e): the doubtful-strict default is absent"
    # (f) FR-013 surface-first precedence -- distinct from (d)
    assert "上送极优先" in sec, "C-10(f): the surface-first precedence (both lists hit) is absent"
    # (g) FR-014 two-strike escalation + the identity key that makes 'same' decidable
    assert "两振" in sec, "C-10(g): the two-strike escalation rule is absent"
    assert "第二次" in sec, "C-10(g): the escalation trigger ('second occurrence') is not stated"
    # Recurrence key: the falsified expectation ALONE. Two independent reviewers found
    # that the original (发现点, 被证伪的预期) tuple makes this rule unreachable, because a
    # recurrence almost always surfaces at a different discovery point. Adjudicated
    # 2026-09-23: FR-014 uses the single-key recurrence form; FR-044's independence key
    # keeps the tuple (asserted in test_c18_*).
    assert "被证伪的预期" in sec, "C-10(g): the recurrence key is absent"
    assert re.search(r"不含发现点", sec), (
        "C-10(g): the recurrence key is not stated to EXCLUDE 发现点. Merging it back with "
        "FR-044's independence key silently makes two-strike escalation unreachable for "
        "cross-point recurrence -- a string-presence assertion alone cannot catch that."
    )
    assert re.search(r"复发键|单键", sec), "C-10(g): the recurrence key is not named as a single key"
    # (f) and (d) must be independently locatable -- they are different precedence rules
    d_at = sec.index("判据优先于清单命中")
    f_at = sec.index("上送极优先")
    assert d_at != f_at, "C-10(d)/(f): the two precedence rules collapse into one statement"


def test_c11_blast_radius_decidable():
    """C-11: blast radius is a set-containment test, not an adjective."""
    sec = _section(_text(DOC), SECTION_HEADINGS[0])
    assert "爆炸半径" in sec, "C-11: 爆炸半径 is not defined in the triage section"
    assert "当前动作" in sec, "C-11: the definition does not mention 当前动作"
    assert "声明的范围" in sec or "声明范围" in sec, "C-11: the definition does not mention 声明的范围"
    assert GATE_DOC.name not in sec or "shared/guidelines/" in sec, (
        "C-11: adjacent discipline referenced by name rather than by path"
    )


def test_c12_blind_check_sentinel_reference():
    """C-12: STR-006 exactly once, plus a path reference to the two existing techniques."""
    sec = _section(_text(DOC), SECTION_HEADINGS[0])
    assert sec.count(BLIND_CHECK_SENTINEL) == 1, (
        f"C-12: STR-006 must appear exactly once, found {sec.count(BLIND_CHECK_SENTINEL)}"
    )
    assert LESSONS in sec, f"C-12: the lessons section is not cited by path ({LESSONS})"
    assert "变异演练" in sec and "反空真哨兵" in sec, (
        "C-12: the two companion techniques are not both named"
    )
    # delegate, do not restate: the lessons body's own wording must not be copied in
    lessons_text = _text(ROOT / LESSONS)
    for probe in ("实测在 6 个提交、16 个真实新增", "一次回本"):
        assert probe not in sec, f"C-12: the lessons body is restated rather than referenced ({probe!r})"
    assert lessons_text.strip(), "sentinel: the lessons file read as empty, so the check above is blind"


def test_c13_list_entry_syntax_closed():
    """C-13: both lists non-empty, fixed entry syntax, each carries a criterion, closedness declared."""
    text = _text(DOC)
    for heading, prefix in ((SECTION_HEADINGS[1], "FF"), (SECTION_HEADINGS[2], "RP")):
        sec = _section(text, heading)
        assert sec.strip(), f"C-13(a): {heading!r} is empty"
        entries = _entries(text, heading, prefix)
        assert entries, f"C-13(a): {heading!r} has no entry matching the fixed syntax"
        for num, line in sorted(entries.items()):
            assert "判据:" in line, f"C-13(c): {prefix}-{num} carries no 判据: separator -> {line!r}"
        assert "封闭" in sec, f"C-13(d): {heading!r} does not declare closedness"
        assert "修订本文档" in sec or "修订该文档" in sec, (
            f"C-13(d): {heading!r} does not state that extension goes only through revising this document"
        )
        # numbers are contiguous from 1 -- a gap means an entry was deleted silently
        assert sorted(entries) == list(range(1, len(entries) + 1)), (
            f"C-13(b): {prefix} numbering is not contiguous from 1: {sorted(entries)}"
        )


def test_c14_seven_named_failures_locatable():
    """C-14: the 7 named failure forms are each individually locatable (never by list size)."""
    text = _text(DOC)
    entries = _entries(text, SECTION_HEADINGS[1], "FF")
    for n in FF_NAMED:
        assert n in entries, f"C-14: FF-{n} is not locatable in the fast-fail list"
    # FF-2..FF-5 = the four blind-check causes; FF-6..FF-8 = the three git diff forms
    blind_probes = {2: "输出形态", 3: "基线", 4: "可达范围", 5: "错误的树"}
    for n, probe in blind_probes.items():
        assert probe in entries[n], (
            f"C-14: FF-{n} should carry blind-check cause {probe!r}, got: {entries[n]!r}"
        )
    diff_probes = {6: "--stat", 7: "HEAD", 8: "未跟踪"}
    for n, probe in diff_probes.items():
        assert probe in entries[n], (
            f"C-14: FF-{n} should carry git-diff form {probe!r}, got: {entries[n]!r}"
        )
    # FR-021: evidenced by path reference, body not restated
    for n in FF_NAMED:
        assert "实证:" in entries[n], f"C-14/FR-021: FF-{n} carries no 实证: column"
    # explicitly NOT asserting on len(entries) -- the list is designed to grow (FR-020)


def test_c15_named_failure_sentinel():
    """C-15: anti-vacuity for C-14 -- 'nothing missing' plus 'at least one hit'."""
    text = _text(DOC)
    entries = _entries(text, SECTION_HEADINGS[1], "FF")
    missing = [n for n in FF_NAMED if n not in entries]
    assert missing == [], f"C-15: the named-form set is not fully covered; missing {missing}"
    # sentinel: the emptiness above is because the list is right, not because the scan is blind
    present = [n for n in FF_NAMED if n in entries]
    assert len(present) >= 1, "C-15 sentinel: zero hits -- the scan is blind, not the list clean"
    assert len(entries) >= len(FF_NAMED), (
        f"C-15 sentinel: the list holds {len(entries)} entries but {len(FF_NAMED)} are named"
    )


def test_c16_gate_discipline_delegated_by_path():
    """C-16: the irreversible-action entry delegates by path and copies no gate-list text."""
    text = _text(DOC)
    entries = _entries(text, SECTION_HEADINGS[1], "FF")
    rel = "shared/guidelines/confirmation-gates.md"
    delegating = [n for n, line in entries.items() if rel in line]
    assert delegating, f"C-16: no fast-fail entry delegates by path to {rel}"
    for n in delegating:
        assert "不可撤销" in entries[n], f"C-16: FF-{n} cites the gate doc but is not the irreversible-action entry"
    # MUST NOT copy the gate doc's own list entries verbatim
    gate_lines = [
        line.strip().lstrip("-*| ").strip()
        for line in _text(GATE_DOC).splitlines()
        if len(line.strip().lstrip("-*| ").strip()) >= 12
    ]
    copied = [g for g in gate_lines if g and g in text]
    assert copied == [], f"C-16: gate-governance list text copied verbatim: {copied[:3]}"
    assert gate_lines, "sentinel: the gate doc parsed to zero lines, so the copy check above is blind"
    # the adjacent discipline is named by path, never by its Chinese name (gate-neutrality C-6)
    assert "确认门控治理" not in text and "确认门禁" not in text, (
        "C-16/gate-neutrality C-6: the adjacent discipline's Chinese name appears literally"
    )


def test_c17_surface_report_and_disclosure():
    """C-17 (a)-(e): the surface-report and disclosure section."""
    sec = _section(_text(DOC), SECTION_HEADINGS[3])
    assert sec.strip(), f"C-17: section {SECTION_HEADINGS[3]!r} is empty"

    # (a) the four elements
    for elem in ("发现了什么", "为何吃重", "中间产物", "可选处置"):
        assert elem in sec, f"C-17(a): surface-report element {elem!r} missing"

    # (b) closed disposition set, four values, closedness declared
    for disp in ("按建议处置", "改为顺手修复并继续", "照原样继续", "终止本次运行"):
        assert disp in sec, f"C-17(b): disposition {disp!r} missing from the closed set"
    assert "封闭" in sec, "C-17(b): the disposition set is not declared closed"

    # (c) interface class ownership: ⑪, never ①
    assert "⑪" in sec, "C-17(c): the surface report is not assigned to interface class ⑪"
    assert "① 门控确认提示" not in sec, (
        "C-17(c): the surface report is assigned to class ① -- that would make it a gate prompt "
        "and contradict FR-028"
    )

    # (d) clean runs must say so explicitly, using STR-013
    assert MARKER_CLEAN in sec, f"C-17(d): STR-013 {MARKER_CLEAN!r} absent"
    assert "干净" in sec, "C-17(d): no clean-run explicit-statement obligation"

    # (e) granularity by pointer, not restatement
    assert "shared/guidelines/confirmation-gates.md" in sec, (
        "C-17(e): the execution-report granularity rules are not referenced by path"
    )
    gate_text = _text(GATE_DOC)
    for probe in ("失败点、原因与已产生的中间产物",):
        if probe in gate_text:
            assert probe not in sec, f"C-17(e): the execution-report rule is restated, not referenced ({probe!r})"


def test_c18_growth_loop_marker_and_bidirectional():
    _text(DOC)
    _unimplemented("C-18 (a)-(f)", "T042")


def test_c19_growth_loop_three_numbers():
    _text(DOC)
    _unimplemented("C-19", "T042")


def test_c21_project_neutral():
    """C-21: the document ships to any downstream project, so no repo-specific names."""
    text = _text(DOC)
    hits = [name for name in FORBIDDEN_NAMES if name in text]
    assert hits == [], f"C-21: project-specific names present: {hits}"
    assert text.strip(), "sentinel: the document read as empty, so the neutrality check is blind"



def test_c22_scope_limits_and_accepted_cost():
    _text(DOC)
    _unimplemented("C-22", "T050")


# --- ambient-section.md C-1..C-19 (bodies land in T016 / T050) -------------

DISCIPLINE_ORDER = (
    "## Token Efficiency Discipline",
    "## User-Facing Comprehension",
    "## Fast Fail Discipline",
    "## Dogfooding Practice",
)
CONTIGUOUS_THREE = (
    "## Documentation Map",
    "## Proactive Flow Trigger",
    "## Fact, Correctness & Logic Checks (Input Sanity)",
)
HOUSE_LEAD_HEAD = "The full discipline is defined in a single source of truth — "
HOUSE_LEAD_TAIL = "(do NOT copy its rules; reference the file) — and binds all commands, skills, and agents:"

# ambient-section.md C-16's closed enumeration, located BY FILENAME (never by
# line number -- inserting a line silently shifts every number below it). Each
# value is a fragment of that file's own pre-existing behaviour text, so the
# guard can tell "only a pointer was added" from "the body was rewritten".
INSTANCE_POINTS = {
    "templates/commands/implement.md": "Writability pre-probe",
    "templates/commands/todo.md": "Scanner exit code",
    "templates/commands/analyze.md": "Abort with an error message if any required file is missing",
    "templates/commands/docs.md": "MUST NOT truncate or silently defer the tail",
    "templates/commands/clarify.md": "If no `requirements.md` at all",
    "templates/commands/interview.md": "Surface conflicts; never resolve them silently",
    "skills/create-team/references/create-mode.md": "MUST NOT silently degrade to inline goal creation",
    "skills/draw-diagram/SKILL.md": "静默降级",
}


def _section_of(path: Path, heading: str = AMBIENT_HEADING) -> list:
    lines = _lines(path)
    assert heading in lines, f"{path.relative_to(ROOT)} carries no {heading!r} heading"
    i = lines.index(heading)
    j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith("## ")), len(lines))
    return lines[i:j]


def _in_fence(lines: list, needle: str) -> bool:
    fence = False
    for line in lines:
        if line.startswith("```"):
            fence = not fence
        if needle in line and fence:
            return True
    return False


def test_a1_template_heading_present():
    """C-1: the template carries the ambient heading exactly once."""
    text = _text(INSTR)
    n = text.count(AMBIENT_HEADING)
    assert n == 1, f"C-1: {AMBIENT_HEADING!r} appears {n}x in {INSTR.relative_to(ROOT)}; expected exactly 1"


def test_a2_live_instructions_heading_present():
    """C-2: the regenerated live file carries the same heading exactly once."""
    text = _text(INSTR_LIVE)
    n = text.count(AMBIENT_HEADING)
    assert n == 1, (
        f"C-2: {AMBIENT_HEADING!r} appears {n}x in {INSTR_LIVE.relative_to(ROOT)}; expected exactly 1 "
        "(regenerate with scripts/bash/generate-instructions.sh -- it is never hand-edited)"
    )


def test_a3_exactly_one_pointer_line_each():
    """C-3: each surface carries exactly one pointer line, using the runtime path."""
    for path in (INSTR, INSTR_LIVE):
        hits = [line for line in _section_of(path) if AMBIENT_POINTER in line]
        assert len(hits) == 1, (
            f"C-3: {path.relative_to(ROOT)} carries {len(hits)} pointer lines to {AMBIENT_POINTER}; expected 1"
        )


def test_a4_pointer_count_sentinel():
    """C-4: anti-vacuity -- the body is non-trivial, so 'one pointer' cannot pass on an empty section."""
    for path in (INSTR, INSTR_LIVE):
        body = [line for line in _section_of(path)[1:] if line.strip()]
        assert len(body) >= 3, (
            f"C-4 sentinel: {path.relative_to(ROOT)}'s section body is {len(body)} non-blank lines (<3)"
        )


def test_a5_four_discipline_sections_strict_order():
    """C-5: strict ordering of the four discipline sections (not adjacency)."""
    lines = _lines(INSTR)
    for h in DISCIPLINE_ORDER:
        assert h in lines, f"C-5: {h!r} is missing from the template"
    seq = [lines.index(h) for h in DISCIPLINE_ORDER]
    assert seq == sorted(seq) and len(set(seq)) == len(seq), (
        f"C-5: strict order violated; indices {dict(zip(DISCIPLINE_ORDER, seq))}"
    )


def test_a6_not_inside_three_section_window():
    """C-6: the three pre-existing sections stay contiguous; the new one is not between them."""
    lines = _lines(INSTR)
    for h in CONTIGUOUS_THREE:
        assert h in lines, f"C-6: pre-existing section {h!r} disappeared"
    idx = [lines.index(h) for h in CONTIGUOUS_THREE]
    assert idx == sorted(idx), f"C-6: the three sections lost their order: {idx}"
    # "contiguous" means no OTHER H2 section between the first and the third -- not
    # adjacent line numbers, since each of the three spans many lines of its own.
    between = [
        lines[k] for k in range(idx[0] + 1, idx[2])
        if lines[k].startswith("## ") and lines[k] not in CONTIGUOUS_THREE
    ]
    assert between == [], f"C-6: other sections were inserted between the three: {between}"
    ff = lines.index(AMBIENT_HEADING)
    assert not (idx[0] < ff < idx[2]), "C-6: the new section was inserted inside the contiguous window"


def test_a7_section_counts_18_to_19_and_19_to_20():
    """C-7: top-level counts -- template 19, live 20 (18/19 measured before)."""
    tpl = sum(1 for line in _lines(INSTR) if line.startswith("## "))
    live = sum(1 for line in _lines(INSTR_LIVE) if line.startswith("## "))
    assert tpl == 19, f"C-7: template has {tpl} top-level sections; expected 19 (18 before + 1)"
    assert live == 20, f"C-7: live file has {live} top-level sections; expected 20 (19 before + 1)"
    tpl_set = {l for l in _lines(INSTR) if l.startswith("## ")}
    live_set = {l for l in _lines(INSTR_LIVE) if l.startswith("## ")}
    assert tpl_set <= live_set, f"C-7: template sections missing from live: {sorted(tpl_set - live_set)}"


def test_a8_no_inlined_section_names():
    """C-8: the ambient section inlines none of the truth-source doc's H2 names."""
    sec = "\n".join(_section_of(INSTR))
    inlined = [h.removeprefix("## ") for h in SECTION_HEADINGS if h.removeprefix("## ") in sec]
    assert inlined == [], f"C-8: truth-source section names inlined into the ambient section: {inlined}"


def test_a9_house_lead_sentence_form():
    """C-9: the section uses the house lead-sentence form."""
    sec = "\n".join(_section_of(INSTR))
    assert HOUSE_LEAD_HEAD in sec, f"C-9: the house lead-in {HOUSE_LEAD_HEAD!r} is absent"
    assert HOUSE_LEAD_TAIL in sec, f"C-9: the house lead-out {HOUSE_LEAD_TAIL!r} is absent"
    assert f"`{AMBIENT_POINTER}`" in sec, "C-9: the backticked owner path is absent from the lead sentence"


def test_a10_no_engine_invocation_form():
    """C-10: no engine-invocation forms in a standing summary section."""
    sec = "\n".join(_section_of(INSTR))
    assert "--action" not in sec, "C-10: a bare --action flag leaked into the ambient section"
    assert "$ARGUMENTS" not in sec, "C-10: $ARGUMENTS leaked into the ambient section"
    found = re.findall(r"<[a-z][a-z0-9-]*>", sec)
    assert not found, f"C-10: placeholder forms leaked into the ambient section: {found}"


def test_a11_project_neutral():
    """C-11: the section ships to every downstream project, so no repo-specific names."""
    sec = _section_of(INSTR)
    body = "\n".join(sec).lower()
    hits = [name for name in FORBIDDEN_NAMES if name.lower() in body]
    assert hits == [], f"C-11: project-specific names in the ambient section: {hits}"
    assert len(sec) >= 3, "sentinel: the section read as near-empty, so the neutrality check is blind"


def test_a12_no_speckit_command_form():
    """C-12: no /speckit.* forms -- this is a standing summary, not a workflow step."""
    sec = "\n".join(_section_of(INSTR))
    found = re.findall(r"/speckit\.[a-z]+", sec)
    assert found == [], f"C-12: command invocation forms in the ambient section: {found}"


def test_a13_recovery_path_names_real_cli_asset():
    _text(INSTR)
    _unimplemented("A-13", "T050")


def test_a14_no_refresh_instructions_restores_mirror():
    _text(INSTR)
    _unimplemented("A-14", "T050")


def test_a15_forbidden_sentence_mutation_drill():
    _text(INSTR)
    _unimplemented("A-15 (drill evidenced in T051)", "T050")


def test_a16_instance_points_one_pointer_each():
    """C-16: each named instance point carries exactly one pointer, its body verbatim intact."""
    assert len(INSTANCE_POINTS) == 8, (
        f"C-16: the closed enumeration holds {len(INSTANCE_POINTS)} files; the contract names 8"
    )
    for rel, fragment in INSTANCE_POINTS.items():
        path = ROOT / rel
        assert path.is_file(), f"C-16: enumerated instance point does not exist: {rel}"
        lines = _lines(path)
        hits = [line for line in lines if AMBIENT_POINTER in line]
        assert len(hits) == 1, f"C-16: {rel} carries {len(hits)} pointer lines; expected exactly 1"
        assert not _in_fence(lines, AMBIENT_POINTER), (
            f"C-16: {rel}'s pointer line sits inside a fenced code block, so it renders as example text"
        )
        assert fragment in "\n".join(lines), (
            f"C-16: {rel} lost its named behaviour text ({fragment!r}) -- the body was rewritten, not pointed at"
        )


def test_a17_instance_points_sentinel():
    """C-17: anti-vacuity for C-16 -- the convergence actually happened."""
    total = sum(
        1 for rel in INSTANCE_POINTS for line in _lines(ROOT / rel) if AMBIENT_POINTER in line
    )
    assert total >= 1, "C-17 sentinel: no instance point gained a pointer at all"
    assert total == len(INSTANCE_POINTS), (
        f"C-17 sentinel: {total} pointer lines across {len(INSTANCE_POINTS)} points -- "
        "'zero body changes' must mean 'only pointers were added', not 'nothing was done'"
    )


# "## 范围限制" is a generic heading that another discipline's owner document
# legitimately uses as its own section (measured: shared/guidelines/
# user-facing-comprehension.md). A heading collision between two disciplines is
# not a restatement of this one's criteria, so it is excluded from the sweep --
# explicitly, with the collision named, rather than by loosening every needle.
GENERIC_HEADING_SHARED_WITH_ANOTHER_DISCIPLINE = "## 范围限制"


def test_a18_convergence_scope_bounded():
    """C-18: no second restatement of the criteria anywhere under shared/ or templates/."""
    heading_needles = [
        h for h in SECTION_HEADINGS if h != GENERIC_HEADING_SHARED_WITH_ANOTHER_DISCIPLINE
    ]
    literal_needles = [MECHANICAL_TEST_FIX, BLIND_CHECK_SENTINEL, "- **FF-", "- **RP-"]
    offenders = {}
    for base in ("shared", "templates"):
        for path in sorted((ROOT / base).rglob("*.md")):
            if path == DOC:
                continue
            body = path.read_text(encoding="utf-8")
            lines = {line.strip() for line in body.splitlines()}
            hit = [h for h in heading_needles if h in lines]
            hit += [n for n in literal_needles if n in body]
            if hit:
                offenders[str(path.relative_to(ROOT))] = hit
    assert offenders == {}, (
        "C-18: the criteria are restated outside the owner (a second definition point that will "
        f"drift): {offenders}"
    )
    # sentinel: the owner really does carry every needle, so an empty offender set
    # means "clean", not "the scan could not see anything"
    owner = _text(DOC)
    owner_lines = {line.strip() for line in owner.splitlines()}
    missing = [h for h in heading_needles if h not in owner_lines]
    missing += [n for n in literal_needles if n not in owner]
    assert missing == [], f"C-18 sentinel: the owner itself lacks these needles: {missing}"
    # the excluded heading is excluded for a measured reason, not silently: it must
    # still exist in the owner and in the other discipline's document
    assert GENERIC_HEADING_SHARED_WITH_ANOTHER_DISCIPLINE in owner_lines, (
        "C-18: the excluded generic heading is not even a section of the owner"
    )
    other = ROOT / "shared" / "guidelines" / "user-facing-comprehension.md"
    assert GENERIC_HEADING_SHARED_WITH_ANOTHER_DISCIPLINE in {
        line.strip() for line in _text(other).splitlines()
    }, (
        "C-18: the exclusion reason no longer holds -- "
        f"{other.relative_to(ROOT)} no longer uses that heading, so put it back in the needle set"
    )


def test_a19_channel_one_unobservable_self_statement():
    """C-19: the doc states channel one cannot be observed by a contract test.

    Green point belongs to Phase 6 (T037): the self-statement lives in the doc's
    dispatch-injection section, which T028 fills.
    """
    text = _text(DOC)
    assert "通道一" in text, "C-19: the doc does not name channel one"
    assert re.search(r"通道一[^\n]{0,120}(不可|无法|不能被)[^\n]{0,60}(观测|测)", text), (
        "C-19: the doc carries no self-statement that channel one's compliance is not observable "
        "by a contract test"
    )


# --- constitution-export.md C-1..C-23 (bodies land in T025 / T050) ---------

PRINCIPLE_TITLE = "Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest)"
TPL_HEADING = f"### XIV. {PRINCIPLE_TITLE}"
LIVE_HEADING = f"### XVI. {PRINCIPLE_TITLE}"
PRINCIPLE_RE = re.compile(r"^### ([IVXLC0-9]+)\. (.+)$", re.M)
REJECTED_MECHANISMS = ("anomaly-detection engine", "triage scorer", "maturity report", "ledger")
PLAN_NO_HARDCODE = "Do NOT hard-code principle names here"
PLAN_ENUMERATE = "enumerate every heading matching"


def _principle_block(text: str, heading: str) -> str:
    lines = text.splitlines()
    assert heading in lines, f"principle block {heading!r} is absent"
    i = lines.index(heading)
    j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith("### ") or lines[k].startswith("## ")), len(lines))
    return "\n".join(lines[i:j])


def test_x1_template_principle_xiv():
    """C-1: the template carries principle XIV under the exact title."""
    text = _text(CONST_TPL)
    assert text.count(TPL_HEADING) == 1, (
        f"C-1: {TPL_HEADING!r} appears {text.count(TPL_HEADING)}x in {CONST_TPL.relative_to(ROOT)}"
    )


def test_x2_command_must_include_entry():
    """C-2: the command's MUST-include list carries the same title."""
    text = _text(CONST_CMD)
    needle = f'**MUST include** a principle for "{PRINCIPLE_TITLE}"'
    assert text.count(needle) == 1, (
        f"C-2: the MUST-include entry appears {text.count(needle)}x in {CONST_CMD.relative_to(ROOT)}"
    )


def test_x3_double_landing_neither_side_missing():
    """C-3: neither side may be missing -- the title lands verbatim on both.

    The delete-either-side mutation drill is carried by the pre-existing guard
    tests/contract/test_constitution_double_landing.py, which already probes the
    watchlist (its DOUBLE_LANDING_WATCHLIST gains this title in T023). Restating
    the drill here would make two owners of one proposition.
    """
    tpl, cmd = _text(CONST_TPL), _text(CONST_CMD)
    assert PRINCIPLE_TITLE in tpl, "C-3: the template side is missing the title"
    assert PRINCIPLE_TITLE in cmd, "C-3: the command side is missing the title"
    # the two occurrences must be the SAME string, not two near-misses
    tpl_titles = set(PRINCIPLE_RE.findall(tpl))
    assert any(title == PRINCIPLE_TITLE for _num, title in tpl_titles), (
        "C-3: the template heading title does not match the command entry title verbatim"
    )


def test_x4_live_constitution_principle_xvi():
    """C-4: the live constitution carries the corresponding principle."""
    text = _text(CONST_LIVE)
    assert text.count(LIVE_HEADING) == 1, (
        f"C-4: {LIVE_HEADING!r} appears {text.count(LIVE_HEADING)}x in {CONST_LIVE.relative_to(ROOT)}"
    )


def test_x5_live_version_minor_bump():
    """C-5: the live version took the MINOR bump to 1.13.0."""
    text = _text(CONST_LIVE)
    m = re.search(r"^\*\*Version\*\*:\s*([0-9.]+)", text, re.M)
    assert m, "C-5: no anchored `**Version**:` line found"
    assert m.group(1) == "1.13.0", f"C-5: live version is {m.group(1)}; expected 1.13.0"
    # anchored on purpose: an unanchored scan matches the Sync Impact Report's
    # "Version change: 1.11.0 ->" line and reports a stale value.


def test_x6_sync_impact_report_prepended():
    """C-6: a Sync Impact Report block is prepended, in the house form."""
    lines = _lines(CONST_LIVE)
    head = "\n".join(lines[:40])
    assert "Sync Impact Report" in head, "C-6: no Sync Impact Report in the first 40 lines"
    assert re.search(r"Version change:.*→", head), "C-6: the report does not state the version change"
    for field in ("- Added principles:", "- Modified principles:", "- Removed sections:",
                  "- Templates requiring updates:", "- Follow-up TODOs:", "- Preserved by design:"):
        assert field in head, f"C-6: the report is missing the {field!r} field"
    assert "✅" in head, "C-6: the report carries no per-item ✅ / ⚠ status"
    assert PRINCIPLE_TITLE.split(" (")[0] in head, "C-6: the report does not name the added principle"


def test_x7_version_three_segment_form():
    """C-7: the version is a 3-segment number (upstream's 4-segment rule is a recorded divergence)."""
    m = re.search(r"^\*\*Version\*\*:\s*([0-9.]+)", _text(CONST_LIVE), re.M)
    assert m, "C-7: no `**Version**:` line"
    parts = m.group(1).split(".")
    assert len(parts) == 3 and all(p.isdigit() for p in parts), (
        f"C-7: version {m.group(1)!r} is not 3 numeric segments"
    )


def test_x8_principle_block_structure():
    """C-8: both new blocks follow the house structure."""
    for path, heading in ((CONST_TPL, TPL_HEADING), (CONST_LIVE, LIVE_HEADING)):
        block = _principle_block(_text(path), heading)
        lines = block.splitlines()
        assert lines[0] == heading, "C-8: the block does not start with its heading"
        # The claim sentence is hard-wrapped (<100 chars per line, C-10), so it spans
        # every line between the heading and the first bullet -- the colon terminates
        # the SENTENCE, not the first line. House Principle XIII wraps the same way.
        body = lines[1:]
        cut = next((k for k, l in enumerate(body) if l.startswith("- ")), len(body))
        claim = " ".join(l.strip() for l in body[:cut] if l.strip())
        assert claim.endswith(":"), f"C-8: the claim sentence does not end in a colon: {claim[-70:]!r}"
        bullets = [l for l in lines if l.startswith("- ")]
        assert bullets, "C-8: the block has no `- ` bullets"
        joined = "\n".join(bullets)
        assert "MUST" in joined and "MUST NOT" in joined, "C-8: the bullets carry no MUST / MUST NOT"
        assert "Rationale:" in block, "C-8: no Rationale paragraph"
        # exactly one blank line immediately before Rationale: the separator must be
        # "\n\n" and not "\n\n\n". (An earlier form of this check rstripped the text and
        # then asserted it did not end in a newline -- vacuously true, i.e. a blind check.)
        pre = block[: block.index("Rationale:")]
        assert pre.endswith("\n\n"), f"C-8: Rationale is not preceded by a blank line: {pre[-40:]!r}"
        assert not pre.endswith("\n\n\n"), f"C-8: more than one blank line before Rationale: {pre[-40:]!r}"


def test_x9_principle_block_pointer_and_no_new_mechanism():
    """C-9: each block carries a pointer bullet and a no-new-mechanism bullet."""
    for path, heading in ((CONST_TPL, TPL_HEADING), (CONST_LIVE, LIVE_HEADING)):
        block = _principle_block(_text(path), heading)
        assert DOC_REL in block or f".specify/{DOC_REL}" in block, (
            f"C-9(a): {path.name}'s block does not cite the discipline doc by path"
        )
        assert "reference it" in block and "do not restate it" in block, (
            f"C-9(a): {path.name}'s pointer bullet does not state reference-not-restate"
        )
        missing = [m for m in REJECTED_MECHANISMS if m not in block]
        assert not missing, f"C-9(b): {path.name}'s block does not name the rejected mechanisms {missing}"


def test_x10_principle_block_lines_under_100():
    """C-10: every line of both new blocks is hard-wrapped under 100 characters."""
    for path, heading in ((CONST_TPL, TPL_HEADING), (CONST_LIVE, LIVE_HEADING)):
        block = _principle_block(_text(path), heading)
        over = [(len(l), l[:50]) for l in block.splitlines() if len(l) >= 100]
        assert not over, f"C-10: {path.name}'s block has lines >= 100 chars: {over[:3]}"


def test_x11_principle_block_no_restated_content():
    """C-11: the blocks reference the discipline; they do not restate it."""
    for path, heading in ((CONST_TPL, TPL_HEADING), (CONST_LIVE, LIVE_HEADING)):
        block = _principle_block(_text(path), heading)
        for needle, what in (
            (MECHANICAL_TEST_FIX, "STR-005 mechanical test"),
            (BLIND_CHECK_SENTINEL, "STR-006 blind-check sentinel"),
            ("- **FF-", "fast-fail list entries"),
            ("- **RP-", "in-passing repair list entries"),
            (CLAUSE_BEGIN, "the injection clause owner literal"),
        ):
            assert needle not in block, f"C-11: {path.name}'s block restates {what}"
        inlined = [h for h in SECTION_HEADINGS if h in block]
        assert not inlined, f"C-11: {path.name}'s block inlines truth-source section headings {inlined}"


def test_x12_principle_block_project_neutral():
    """C-12: the template block ships downstream, so no repo-specific names."""
    block = _principle_block(_text(CONST_TPL), TPL_HEADING).lower()
    hits = [n for n in FORBIDDEN_NAMES if n.lower() in block]
    assert hits == [], f"C-12: project-specific names in the template principle block: {hits}"


def test_x13_double_landing_three_count_pins():
    """C-13: the three count pins were raised in the same batch."""
    src = _text(DOUBLE_LANDING_TEST)
    for name, want in (("TEMPLATE_COUNT", 14), ("LIVE_COUNT", 16), ("COMMAND_COUNT", 8)):
        m = re.search(rf"^{name} = (\d+)", src, re.M)
        assert m, f"C-13: {name} not found in the guard"
        assert int(m.group(1)) == want, f"C-13: {name} is {m.group(1)}; expected {want}"
    # and the counts are true of the artifacts, not just of the pins
    assert len(PRINCIPLE_RE.findall(_text(CONST_TPL))) == 14, "C-13: the template does not actually hold 14"
    assert len(PRINCIPLE_RE.findall(_text(CONST_LIVE))) == 16, "C-13: the live constitution does not hold 16"
    assert len(re.findall(r'\*\*MUST include\*\* a principle for "([^"]+)"', _text(CONST_CMD))) == 8, (
        "C-13: the command list does not actually hold 8 entries"
    )


def test_x14_min_version_floor_semantics():
    """C-14: MIN_VERSION is a floor, raised to (1, 13), and compared with >=."""
    src = _text(DOUBLE_LANDING_TEST)
    m = re.search(r"^MIN_VERSION = \((\d+),\s*(\d+)\)", src, re.M)
    assert m, "C-14: MIN_VERSION not found"
    assert (int(m.group(1)), int(m.group(2))) == (1, 13), (
        f"C-14: MIN_VERSION is ({m.group(1)}, {m.group(2)}); expected (1, 13)"
    )
    assert re.search(r"got >= MIN_VERSION", src), (
        "C-14: MIN_VERSION is no longer used as a floor (>=); floor semantics are the point of the pin"
    )


def test_x15_watchlist_gains_principle_title():
    """C-15: the double-landing watchlist gained this title (2 -> 3)."""
    src = _text(DOUBLE_LANDING_TEST)
    m = re.search(r"DOUBLE_LANDING_WATCHLIST = \((.*?)\n\)", src, re.S)
    assert m, "C-15: DOUBLE_LANDING_WATCHLIST not found"
    entries = re.findall(r'"([^"]+)"', m.group(1))
    assert PRINCIPLE_TITLE in entries, f"C-15: the watchlist lacks {PRINCIPLE_TITLE!r}"
    assert len(entries) == 3, f"C-15: the watchlist holds {len(entries)} entries; expected 3"


def test_x16_plan_template_zero_change():
    """C-16: plan-template.md needed no edit -- it enumerates dynamically.

    The git-level zero-change proof is GATE-3 (a diff against the frozen BASE_SHA
    literal); a test cannot own a SHA. What a test CAN own is the substance: the
    template hard-codes no principle name, so a new principle reaches every
    downstream plan gate without an edit here.
    """
    text = _text(PLAN_TPL)
    assert PRINCIPLE_TITLE not in text, (
        "C-16: plan-template.md now hard-codes this principle's name -- it is supposed to enumerate "
        "dynamically, so any hard-coded name is drift waiting to happen"
    )
    known = [t for _n, t in PRINCIPLE_RE.findall(_text(CONST_LIVE))]
    hard = [t for t in known if t in text]
    assert hard == [], f"C-16: plan-template.md hard-codes live principle names: {hard}"


def test_x17_plan_template_enumeration_sentinel():
    """C-17: anti-vacuity for C-16 -- the enumeration instruction is still there."""
    text = _text(PLAN_TPL)
    assert PLAN_NO_HARDCODE in text, (
        f"C-17 sentinel: {PLAN_NO_HARDCODE!r} is gone, so 'zero change' may mean the mechanism was deleted"
    )
    assert PLAN_ENUMERATE in text, f"C-17 sentinel: {PLAN_ENUMERATE!r} instruction is gone"
    assert "### <roman-or-arabic-numeral>. <name>" in text or re.search(r"###\s*<[^>]*numeral[^>]*>", text), (
        "C-17 sentinel: the heading pattern the enumeration keys on is no longer stated"
    )


def test_x18_downstream_gate_rows_15_to_16():
    """C-18: rendering the enumeration logic gives 16 rows, up from 15."""
    live = _text(CONST_LIVE)
    rows = PRINCIPLE_RE.findall(live)
    assert len(rows) == 16, f"C-18: the enumeration yields {len(rows)} gate rows; expected 16"
    # the 15 side is measured, not asserted from memory: drop this principle's block
    lines = live.splitlines()
    i = lines.index(LIVE_HEADING)
    j = next(k for k in range(i + 1, len(lines)) if lines[k].startswith("## "))
    sample = "\n".join(lines[:i] + lines[j:])
    before = PRINCIPLE_RE.findall(sample)
    assert len(before) == 15, f"C-18: without this principle the enumeration yields {len(before)}; expected 15"
    # sentinel: the enumeration is not returning 16 for a trivial reason
    assert any(title == PRINCIPLE_TITLE for _n, title in rows), "C-18 sentinel: this principle is not among the rows"
    assert not any(title == PRINCIPLE_TITLE for _n, title in before), (
        "C-18 sentinel: the sample still contains the principle, so the 15 is not a real before-state"
    )


def test_x19_ufc_class_eleven_gains_fast_fail_path():
    _text(UFC_DOC_TEST)
    _unimplemented("X-19", "T048 (assertion lives in the UFC doc test)")


def test_x20_ufc_dedup_pin_raised_to_nine():
    _text(UFC_DOC_TEST)
    _unimplemented("X-20", "T048 (pin raise lives in the UFC doc test)")


def test_x21_ufc_override_column_unchanged():
    _text(UFC_DOC_TEST)
    _unimplemented("X-21", "T048 (carried by the existing test_c18a)")


def test_x22_cross_discipline_change_recorded():
    _text(UFC_DOC)
    _unimplemented("X-22 (four-place trace verified in T049)", "T050")


def test_x23_surface_report_ownership_split():
    _text(DOC)
    _unimplemented("X-23", "T050")


# --- dispatch-injection.md C-1..C-23, C-26 (bodies land in T036) -----------


def test_i1_exactly_one_delimiter_pair():
    _text(DOC)
    _unimplemented("I-1", "T036")


def test_i2_clause_identifier_present():
    _text(DOC)
    _unimplemented("I-2", "T036")


def test_i3_three_mandatory_contents():
    _text(DOC)
    _unimplemented("I-3 (a)-(c)", "T036")


def test_i4_path_may_not_substitute():
    _text(DOC)
    _unimplemented("I-4", "T036")


def test_i5_clause_within_10_lines_1200_bytes():
    _text(DOC)
    _unimplemented("I-5", "T036")


def test_i6_clause_lines_zero_blocking_hits():
    _text(DOC)
    _unimplemented("I-6", "T036")


def test_i7_clause_size_and_hits_anti_vacuity_sentinels():
    _text(DOC)
    _unimplemented("I-7", "T036")


def test_i8_channel_two_command_authoring_requirement():
    _text(AGENTS_CMD)
    _unimplemented("I-8", "T036")


def test_i9_channel_two_skill_authoring_requirement():
    _text(CREATE_AGENT_SKILL)
    _unimplemented("I-9", "T036")


def test_i10_channel_two_factory_presets_byte_equal():
    _text(FACTORY_PRESETS[0])
    _unimplemented("I-10", "T036")


def test_i11_channel_two_mirrors_and_per_tool_copies():
    _text(FACTORY_PRESETS[0])
    _unimplemented("I-11", "T036")


def test_i12_channel_two_bounded_set():
    _text(DOC)
    _unimplemented("I-12 (MUST NOT enumerate .specify/agents/instances/)", "T036")


def test_i13_channel_three_payload_sixth_field_row():
    _text(TEAM_PATTERNS)
    _unimplemented("I-13", "T036")


def test_i14_context_isolation_rules_unchanged():
    _text(TEAM_PATTERNS)
    _unimplemented("I-14", "T036")


def test_i15_channel_one_inline_prompt_landing():
    _text(DOC)
    _unimplemented("I-15", "T036")


def test_i16_three_channels_not_mutually_exclusive():
    _text(DOC)
    _unimplemented("I-16", "T036")


def test_i17_subagent_definitions_dispatch_section():
    _text(SUBAGENT_DEFS)
    _unimplemented("I-17", "T036")


def test_i18_visibility_vs_governance_split():
    _text(SUBAGENT_DEFS)
    _unimplemented("I-18", "T036")


def test_i19_pre_dispatch_probe_obligation():
    _text(DOC)
    _unimplemented("I-19", "T036")


def test_i20_anomaly_return_line_obligation():
    _text(DOC)
    _unimplemented("I-20", "T036")


def test_i21_anomaly_halt_excluded_from_failure_rules():
    _text(DOC)
    _unimplemented("I-21", "T036")


def test_i22_three_modes_equally_bound():
    _text(DOC)
    _unimplemented("I-22", "T036")


def test_i23_per_hop_reinjection_and_precedence():
    _text(DOC)
    _unimplemented("I-23", "T036")


def test_i26_channel_one_enforced_by_review():
    _text(DOC)
    _unimplemented("I-26", "T036")


# --- gate-neutrality.md C-1..C-17 (bodies land in T050) --------------------


def test_g1_prechange_baseline_frozen_relative():
    _text(GATE_BASELINE)
    _unimplemented("G-1 (incl. C-1(a): the quoted scanner line never lands in a scanned file)", "T050")


def test_g2_scanner_zero_change():
    _text(SCANNER)
    _unimplemented("G-2", "T050")


def test_g3_counting_unit_is_matching_lines():
    _text(SCANNER)
    _unimplemented("G-3", "T050")


def test_g4_scan_surface_covers_new_text():
    _text(SCANNER)
    _unimplemented("G-4", "T050")


def test_g5_specify_dir_skipped():
    _text(SCANNER)
    _unimplemented("G-5", "T050")


def test_g6_adjacent_discipline_name_avoided():
    _text(DOC)
    _unimplemented("G-6", "T050")


def test_g7_stop_semantics_zero_hit():
    _text(DOC)
    _unimplemented("G-7", "T050")


def test_g8_stop_semantics_anti_vacuity_sentinels():
    _text(DOC)
    _unimplemented("G-8", "T050")


def test_g9_total_equals_frozen_baseline():
    _text(GATE_BASELINE)
    _unimplemented("G-9", "T050")


def test_g10_three_pins_independently_locatable():
    """C-10 + C-10(a): the pin table's three rows each resolve to a real assert.

    Forms differ per row -- a literal ``== 23``, an equality against the frozen
    baseline, and a derived ``<= cap``. Searching for ``== 23`` alone finds only
    the first; that is how the third pin went uncounted during planning.
    """
    _text(UFC_DOC_TEST)
    _unimplemented("G-10 / C-10(a)", "T050")


def test_g11_pins_and_baselines_not_modified():
    _text(GATE_BASELINE)
    _unimplemented("G-11", "T050")


def test_g12_avoidance_is_wording_only():
    _text(DOC)
    _unimplemented("G-12", "T050")


def test_g13_rewording_triggers_consistency_rerun():
    _text(DOC)
    _unimplemented("G-13", "T050")


def test_g14_accepted_cost_in_scope_limits():
    _text(DOC)
    _unimplemented("G-14", "T050")


def test_g15_cost_not_only_in_spec_mutation_drill():
    _text(INSTR_LIVE)
    _unimplemented("G-15 (drill evidenced in T051)", "T050")


def test_g16_six_engines_zero_change():
    _text(SCANNER)
    _unimplemented("G-16", "T050")


def test_g17_mirrors_produced_by_engines_only():
    _text(ROOT / "scripts" / "python" / "sync-mirrors.py")
    _unimplemented("G-17", "T050")
