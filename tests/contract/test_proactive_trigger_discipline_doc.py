"""Contract tests for the Proactive Flow Trigger discipline doc (spec 050).

Maps to ``contracts/discipline-doc.md`` clauses C-1 … C-16. C-1…C-7 pin
structural properties (dual surface, closed section set, wording safety,
reference-not-restate, ownership, neutrality, discovery path); C-8…C-16 pin the
normative content each ``## `` section must carry, so that FR-005…FR-019 have a
mechanical stake rather than living only in unnumbered prose.

The doc is the single source of truth for the trigger discipline; the
instructions template carries only a summary + pointer. Pointer *existence* in
the template is asserted by ``test_proactive_trigger_section.py`` (trigger-section
C-1) — C-7 here asserts the complementary doc-side property, so the two files do
not duplicate a fact.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "shared" / "guidelines" / "proactive-trigger.md"
DOC_MIRROR = ROOT / ".specify" / "shared" / "guidelines" / "proactive-trigger.md"
DOC_LINK = "shared/guidelines/proactive-trigger.md"
SCANNER = ROOT / "scripts" / "python" / "scan-confirmation-gates.py"
TEMPLATE = ROOT / "templates" / "instructions-template.md"
CONFIRMATION_GATES = ROOT / "shared" / "guidelines" / "confirmation-gates.md"

# C-2: closed set, exact order.
SECTIONS = [
    "Ownership",
    "Evaluation Cadence",
    "Evidence Budget & Escalation",
    "Suggestion Shape",
    "Ordering Contract",
    "Promotion & Safety Boundary",
    "Telemetry & Retention",
    "Tuning Protocol",
    "Global Switch",
    "Maintenance Duties",
]

# C-6: shipped surface must stay project-neutral (shared/ is copied into every
# downstream project by init).
FORBIDDEN = [
    "spec-kit",
    "specify-cli",
    "specify_cli",
    "Feature 0",
    "cloud-native-ai",
    ".specify/specs/0",
    "requirement 0",
]


def _load_scanner():
    """Import BLOCKING_RE from the real scanner rather than restating the literals."""
    spec = importlib.util.spec_from_file_location("_scan_confirmation_gates", SCANNER)
    assert spec is not None and spec.loader is not None, f"cannot load {SCANNER}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read(p: Path) -> str:
    assert p.is_file(), f"missing file: {p}"
    return p.read_text(encoding="utf-8")


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def h2_headings(text: str) -> list[str]:
    return [line[3:].strip() for line in text.splitlines() if line.startswith("## ")]


def section(text: str, title: str) -> str:
    """Body of the `## <title>` section, up to the next `## ` heading."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("## ") and line[3:].strip() == title:
            start = i
            break
    assert start is not None, f"section {title!r} not found"
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## ") or lines[j].startswith("# "):
            end = j
            break
    return "\n".join(lines[start:end])


def assert_carries(sec_title: str, item: str, phrases: list[str]) -> None:
    """Dual criterion: normalized body must contain at least one accepted phrase."""
    body = norm(section(read(DOC), sec_title)).lower()
    for phrase in phrases:
        if norm(phrase).lower() in body:
            return
    pytest.fail(
        f"{sec_title}: required item {item!r} not carried "
        f"(none of {phrases!r} present in normalized section body)"
    )


# --- C-1: dual surface + byte-identical mirror ---


def test_c1_doc_exists_with_byte_identical_mirror():
    assert DOC.is_file(), f"missing discipline doc: {DOC}"
    assert DOC_MIRROR.is_file(), f"missing discipline doc mirror: {DOC_MIRROR}"
    assert DOC.read_bytes() == DOC_MIRROR.read_bytes(), "discipline doc mirror drift"


# --- C-2: closed section set, exact order ---


def test_c2_section_set_closed_and_ordered():
    found = h2_headings(read(DOC))
    assert found == SECTIONS, (
        f"`## ` heading set must be exactly {SECTIONS} in order; got {found}"
    )


# --- C-3: zero BLOCKING_PATTERNS hits ---


def test_c3_zero_blocking_pattern_hits():
    blocking_re = _load_scanner().BLOCKING_RE
    text = read(DOC)
    hits = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for m in blocking_re.finditer(line):
            hits.append(f"L{lineno}: {m.group(0)!r}")
    assert not hits, (
        "discipline doc must not trip any BLOCKING_PATTERNS literal "
        f"(integer headroom on the gate budget is 0); hits: {hits}"
    )


def test_c3_scanner_reports_no_gate_in_this_doc():
    """The doc lives under shared/ (in SCAN_DIRS) and matches no governance path."""
    scanner = _load_scanner()
    rel = DOC.relative_to(ROOT)
    assert not scanner.GOVERNANCE_RE.search(rel.as_posix()), (
        "unexpected: this doc now matches a governance path pattern, "
        "which would silently exempt its hits from the budget"
    )


# --- C-4: reference, not restate ---


def test_c4_does_not_restate_confirmation_gates_tables():
    body = read(DOC)
    gates = read(CONFIRMATION_GATES)
    # The governance-kept table header and the destructive-list bullets are the
    # two enumerations that must never be copied.
    header = "| 门控 | 所在面 | 保留理由 |"
    assert header in gates, "fixture assumption broke: header not in the owner doc"
    assert header not in body, "governance-kept classification table restated"
    for bullet in (
        "- 删除文件或数据(delete / 清空存储)",
        "- 移动/归档既有工件(move / archive / restructure)",
        "- 覆盖用户既有内容",
    ):
        assert bullet not in body, f"destructive list restated: {bullet!r}"
    assert "shared/guidelines/confirmation-gates.md" in body, (
        "the destructive criteria must be reached by path reference"
    )


def test_c4_does_not_restate_seed_rule_or_situation_table():
    body = read(DOC)
    # Situation/rule identifier rows belong to the seed file + data model only.
    assert not re.search(r"(?m)^\|\s*s[0-9]{2}\s*\|", body), (
        "named-situation table restated (situation rows `| sNN |` must not appear)"
    )
    assert not re.search(r"\br-0[0-9]{2}\b", body), (
        "seed rule ids restated; the doc references the seed by path only"
    )
    assert "templates/proactive-trigger-seed.json" in body, (
        "the seed file must be named as the owner of the rule/situation data"
    )


def test_c4_does_not_restate_engine_envelope_keys():
    body = read(DOC)
    for key in (
        "semanticJudgmentPending",
        "workspaceRoot",
        "generatedAt",
        "semanticChecksPending",
    ):
        assert key not in body, f"engine envelope key restated: {key!r}"
    assert "contracts/trigger-engine.md" in body, (
        "envelope/CLI detail must be reached by reference to the engine contract"
    )


# --- C-5: owns the escalation criteria and declares ownership ---


def test_c5_ownership_declared():
    body = norm(section(read(DOC), "Ownership")).lower()
    for owned in (
        "evaluation cadence",
        "evidence budget",
        "suggestion shape",
        "ordering contract",
        "telemetry",
        "tuning protocol",
        "global switch",
    ):
        assert owned in body, f"Ownership must declare {owned!r} as owned here"
    assert "single source of truth" in body or "单一真源" in body, (
        "Ownership must state this doc is the single source of truth"
    )


def test_c5_escalation_table_p1_to_p5_complete():
    sec = section(read(DOC), "Evidence Budget & Escalation")
    for pid in ("P1", "P2", "P3", "P4", "P5"):
        assert re.search(rf"(?m)^\|\s*\**{pid}\**\s*\|", sec), (
            f"escalation criteria row {pid} missing from the P1-P5 table"
        )
    rows = [l for l in sec.splitlines() if re.match(r"^\|\s*\**P[1-5]\**\s*\|", l)]
    assert len(rows) == 5, f"P1-P5 table must have exactly 5 rows, got {len(rows)}"
    for row in rows:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        assert len(cells) >= 2 and all(cells[:2]), (
            f"each escalation row needs a condition and a probe target: {row!r}"
        )


def test_c5_data_model_copy_marked_as_design_record():
    """The design-time table in data-model.md is a dated record, not drift."""
    body = norm(section(read(DOC), "Ownership")).lower()
    assert "data-model.md" in body, (
        "Ownership must name data-model.md's copy as a design-period record"
    )
    assert "dated record" in body or "设计期记录" in body, (
        "must classify the data-model copy as a dated record per one-source-of-truth"
    )


# --- C-6: project neutral ---


def test_c6_project_neutral():
    low = read(DOC).lower()
    for token in FORBIDDEN:
        assert token.lower() not in low, f"project-specific token {token!r} leaked"


# --- C-7: discovery via the new `## ` section's pointer, not a doc-map row ---


def test_c7_discovery_does_not_depend_on_documentation_map():
    body = read(DOC)
    low = norm(body).lower()
    assert "documentation map" not in low or "not the only" in low or "唯一" in low, (
        "discovery must not be routed through a Documentation Map table row; "
        "additive reconcile only propagates whole `## ` sections"
    )
    # The doc must state how it is reached: a pointer from the instructions
    # template's own `## ` section.
    assert DOC_LINK in body or "instructions-template.md" in body, (
        "the doc must name the pointer surface that makes it reachable"
    )
    assert "`## Proactive Flow Trigger`" in body or "## Proactive Flow Trigger" in body, (
        "the doc must name the template section that carries its pointer"
    )


# --- C-8: Evaluation Cadence ---


def test_c8_evaluation_cadence():
    assert_carries("Evaluation Cadence", "every turn", ["every user turn", "每个用户回合"])
    assert_carries(
        "Evaluation Cadence",
        "silent assessment",
        ["zero user-visible output", "零用户可见输出", "assessment is silent", "评估是静默"],
    )
    assert_carries(
        "Evaluation Cadence",
        "cadence != suggestion rate",
        [
            "评估节奏 ≠ 建议节奏",
            "evaluation cadence is not the suggestion rate",
            "cadence is not the suggestion rate",
        ],
    )


# --- C-9: Evidence Budget & Escalation ---


def test_c9_context_only_by_default():
    assert_carries(
        "Evidence Budget & Escalation",
        "default uses only in-context information",
        ["already in context", "已在上下文", "only information already", "default is no file reads"],
    )


def test_c9_probe_is_count_existence_setdiff_only():
    assert_carries(
        "Evidence Budget & Escalation",
        "probe limited to existence/count/set-difference",
        ["存在性/计数/集合差", "existence, counting and set difference", "existence/count/set-difference"],
    )
    body = norm(section(read(DOC), "Evidence Budget & Escalation"))
    assert "MUST NOT" in body, "the probe limit must be stated normatively"
    assert re.search(r"MUST NOT[^\n]{0,80}(全文|full (text|artifact|body))", body), (
        "must forbid reading whole artifact content"
    )


def test_c9_escalation_budget_cap_and_denominator():
    assert_carries(
        "Evidence Budget & Escalation",
        "escalation rate cap 20%",
        ["20%", "20 %"],
    )
    assert_carries(
        "Evidence Budget & Escalation",
        "denominator is assess invocations",
        ["`assess` 调用数", "assess invocations", "assess calls"],
    )


# --- C-10: Suggestion Shape ---


def test_c10_one_line_non_blocking_with_exact_invocation():
    assert_carries(
        "Suggestion Shape",
        "one non-blocking line = purpose + exact invocation",
        [
            "一行非阻塞提示",
            "one non-blocking line",
        ],
    )
    assert_carries(
        "Suggestion Shape",
        "exact invocation form from the engine",
        ["确切调用形式", "exact invocation form", "copy-ready invocation"],
    )


def test_c10_frequency_bounded_by_session_suppression():
    assert_carries(
        "Suggestion Shape",
        "bound defined by session-level repeat suppression",
        ["会话级重复抑制", "session-level repeat suppression", "session-level suppression"],
    )
    assert "trigger-engine.md" in read(DOC), (
        "the suppression mechanism's structural guarantee lives in the engine contract"
    )


def test_c10_converges_to_single_highest_priority():
    assert_carries(
        "Suggestion Shape",
        "multiple hits converge to one",
        ["收敛为一条", "converge to a single", "highest priority"],
    )


def test_c10_no_suggestion_when_nothing_applies():
    assert_carries(
        "Suggestion Shape",
        "honestly suggest nothing",
        ["如实不建议", "MUST NOT pad", "no filler suggestion", "suggest nothing"],
    )


# --- C-11: Ordering Contract ---


def test_c11_compliance_first_same_pass():
    assert_carries(
        "Ordering Contract",
        "compliance check first, flow selection continues in the same pass",
        ["同一趟", "same pass", "same analysis pass"],
    )


def test_c11_suggestion_not_before_compliance():
    body = norm(section(read(DOC), "Ordering Contract"))
    assert re.search(r"MUST NOT[^\n]{0,120}(早于|before|precede)", body), (
        "must forbid emitting a suggestion before the compliance check"
    )


def test_c11_no_per_turn_principle_enumeration():
    assert_carries(
        "Ordering Contract",
        "plan-time per-principle gate not moved to every turn",
        ["plan-template.md", "Constitution Check"],
    )
    body = norm(section(read(DOC), "Ordering Contract"))
    assert re.search(r"MUST NOT[^\n]{0,160}(每回合|every turn|per turn)", body), (
        "must forbid carrying the plan-time enumeration gate into every turn"
    )


def test_c11_compliance_done_flag_declared():
    assert_carries(
        "Ordering Contract",
        "must pass --compliance-done explicitly",
        ["--compliance-done"],
    )
    assert_carries(
        "Ordering Contract",
        "default false reports ordering-violation",
        ["ordering-violation"],
    )


# --- C-12: Promotion & Safety Boundary ---


def test_c12_threshold_promotion_and_single_decline_reset():
    assert_carries(
        "Promotion & Safety Boundary",
        "consecutive acceptance to threshold (default 3) promotes",
        ["默认 3", "default 3", "threshold of 3"],
    )
    assert_carries(
        "Promotion & Safety Boundary",
        "one decline resets",
        ["一次拒绝即重置", "a single decline resets", "one decline resets"],
    )


def test_c12_destructive_never_promotes_by_reference():
    assert_carries(
        "Promotion & Safety Boundary",
        "destructive/irreversible never promoted",
        ["永不晋升", "never promoted", "never promote"],
    )
    body = section(read(DOC), "Promotion & Safety Boundary")
    assert "shared/guidelines/confirmation-gates.md" in body, (
        "destructive criteria must be reached by path reference in this section"
    )
    assert_carries(
        "Promotion & Safety Boundary",
        "doubtful-strict",
        ["存疑从严", "doubtful cases default to strict", "when in doubt, treat as destructive"],
    )


def test_c12_auto_execute_still_reports():
    assert_carries(
        "Promotion & Safety Boundary",
        "auto-execution still produces an execution report",
        ["执行报告", "execution report"],
    )


def test_c12_auto_execute_never_preempts_current_request():
    assert_carries(
        "Promotion & Safety Boundary",
        "must not preempt the user's current request",
        ["抢占用户当前请求", "preempt the user", "yield", "让位"],
    )


def test_c12_user_can_reset_or_downgrade():
    assert_carries(
        "Promotion & Safety Boundary",
        "user can reset one rule or downgrade globally",
        ["复位", "reset a single rule", "downgrade"],
    )


# --- C-13: Telemetry & Retention ---


def test_c13_per_turn_row_fields_and_purpose():
    assert_carries(
        "Telemetry & Retention",
        "one telemetry row per turn",
        ["每回合", "one row per turn", "per turn"],
    )
    assert_carries(
        "Telemetry & Retention",
        "telemetry.jsonl named",
        ["telemetry.jsonl"],
    )


def test_c13_window_default_and_append_truncates_invariant():
    assert_carries(
        "Telemetry & Retention",
        "default window 200",
        ["200"],
    )
    assert_carries(
        "Telemetry & Retention",
        "append-then-truncate invariant",
        ["追加即截断", "append then truncate", "never exceeds the declared window"],
    )


def test_c13_rotation_does_not_clear_learning():
    assert_carries(
        "Telemetry & Retention",
        "promotion counters are aggregate state on the rule",
        ["聚合态", "aggregate state"],
    )
    body = norm(section(read(DOC), "Telemetry & Retention"))
    assert re.search(r"(轮转|rotat|truncat)[^\n]{0,120}(不清空|does not clear|never clears|MUST NOT clear)", body), (
        "rotation/truncation must not clear learning results"
    )


def test_c13_honest_measurement_boundary():
    assert_carries(
        "Telemetry & Retention",
        "telemetry cannot prove a skipped assessment",
        ["无法证明", "cannot prove", "skipped the assessment"],
    )


# --- C-14: Tuning Protocol ---


def test_c14_four_evidence_kinds():
    body = norm(section(read(DOC), "Tuning Protocol"))
    for kind in ("命中率", "拒绝率", "误报", "漏报"):
        assert kind in body, f"evidence kind {kind!r} missing from Tuning Protocol"


def test_c14_small_sample_guard_named():
    assert_carries(
        "Tuning Protocol",
        "small-sample guard hits < 5",
        ["hits < 5", "hits<5", "少于 5", "默认 5"],
    )
    assert_carries(
        "Tuning Protocol",
        "skipped rules named in notes",
        ["具名", "named in", "notes[]"],
    )


def test_c14_proposals_are_candidates_written_only_after_approval():
    assert_carries(
        "Tuning Protocol",
        "presented as candidates",
        ["候选形态", "as candidates", "candidate form"],
    )
    body = norm(section(read(DOC), "Tuning Protocol"))
    assert re.search(r"(用户批准|user approv|after approval)[^\n]{0,80}(写入|writ|appl)", body), (
        "proposals must be written to the rule set only after user approval"
    )
    assert re.search(r"未经用户批准[^\n]{0,60}MUST NOT|MUST NOT[^\n]{0,80}(without|before)[^\n]{0,40}approv", body), (
        "must state the rule set MUST NOT change without approval"
    )


def test_c14_state_machine_and_traceability():
    body = norm(section(read(DOC), "Tuning Protocol"))
    for token in ("proposed", "ratified", "applied"):
        assert token in body, f"SM-2 state {token!r} missing"
    assert_carries(
        "Tuning Protocol",
        "approval linked to evidence for later lookup",
        ["evidenceRef", "证据", "可回查"],
    )


# --- C-15: Global Switch ---


def test_c15_disabled_semantics():
    assert_carries(
        "Global Switch",
        "enabled=false means no suggestions and no auto-execution",
        ["enabled=false", "enabled` = `false", "config.enabled"],
    )
    body = norm(section(read(DOC), "Global Switch"))
    assert re.search(r"(不产出建议|no suggestions)[^\n]{0,80}(不自动执行|no auto)", body), (
        "both halves of the disabled semantics must be stated"
    )


def test_c15_user_choice_overrides_framework_default():
    assert_carries(
        "Global Switch",
        "explicit user off overrides framework default",
        ["优先于框架默认", "overrides the framework default", "takes precedence"],
    )


def test_c15_off_state_survives_instructions_regeneration():
    assert_carries(
        "Global Switch",
        "state separated from the instructions file",
        ["指令再生", "instructions regeneration", "regenerated"],
    )
    body = norm(section(read(DOC), "Global Switch"))
    assert re.search(r"MUST NOT[^\n]{0,120}(覆盖|overwrit|clobber|reset by)", body), (
        "the off state must not be overwritten by regeneration"
    )


def test_c15_reenable_clears_session_suppression():
    assert_carries(
        "Global Switch",
        "false -> true clears session suppression state",
        ["清空会话抑制态", "clears the session suppression", "suppression state is cleared"],
    )


# --- C-16: Maintenance Duties ---


def test_c16_handoffs_edit_must_sync_seed():
    assert_carries(
        "Maintenance Duties",
        "editing Handoffs must sync the seed",
        ["## Handoffs", "Handoffs"],
    )
    body = norm(section(read(DOC), "Maintenance Duties"))
    assert re.search(r"(同步|sync)[^\n]{0,120}(种子|seed)", body), (
        "must require syncing the seed file after editing a source section"
    )
    assert re.search(r"(修复方式|the fix|repair)[^\n]{0,120}(同步|sync)", body), (
        "must state the fix is to sync, not to loosen the test"
    )
    assert re.search(r"(放宽|loosen|weaken)[^\n]{0,80}(测试|test)", body), (
        "must forbid loosening the drift-detection test as the fix"
    )


def test_c16_vocabulary_expansion_only_via_approval():
    assert_carries(
        "Maintenance Duties",
        "situation vocabulary expands only through user approval",
        ["用户批准通道", "user approval", "approval channel"],
    )
    body = norm(section(read(DOC), "Maintenance Duties"))
    assert re.search(r"MUST NOT[^\n]{0,80}(临场造词|invent|coin)", body), (
        "must forbid coining situation words on the fly"
    )


def test_c16_new_action_flag_or_exit_code_revises_engine_contract():
    body = norm(section(read(DOC), "Maintenance Duties"))
    assert re.search(r"MUST[^\n]{0,120}(同批|in the same batch|same change)", body), (
        "new actions/flags/exit codes must revise the engine contract in the same batch"
    )
    for token in ("C-9", "C-10", "C-22"):
        assert token in body, f"engine-contract clause {token} must be named for revision"
