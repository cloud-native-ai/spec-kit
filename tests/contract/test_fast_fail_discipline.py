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


def test_c1_truth_source_doc_exists():
    _text(DOC)
    _unimplemented("C-1", "T005")


def test_c2_mirror_byte_identical():
    _text(DOC)
    _unimplemented("C-2", "T005")


def test_c3_filename_rename_guard():
    _text(DOC)
    _unimplemented("C-3", "T005")


def test_c4_ownership_first_8_lines():
    _text(DOC)
    _unimplemented("C-4", "T005")


def test_c5_failure_statement_first_20_lines():
    _text(DOC)
    _unimplemented("C-5", "T005")


def test_c6_canonical_ufc_pointer_line():
    _text(DOC)
    _unimplemented("C-6", "T005")


def test_c7_nine_section_closed_tuple():
    _text(DOC)
    _unimplemented("C-7", "T005")


def test_c8_rfc2119_keywords():
    _text(DOC)
    _unimplemented("C-8", "T005")


def test_c9_bilingual_h1():
    _text(DOC)
    _unimplemented("C-9", "T005")


def test_c10_triage_criteria_seven_items():
    _text(DOC)
    _unimplemented("C-10 (a)-(g)", "T005")


def test_c11_blast_radius_decidable():
    _text(DOC)
    _unimplemented("C-11", "T005")


def test_c12_blind_check_sentinel_reference():
    _text(DOC)
    _unimplemented("C-12", "T005")


def test_c13_list_entry_syntax_closed():
    _text(DOC)
    _unimplemented("C-13", "T005")


def test_c14_seven_named_failures_locatable():
    _text(DOC)
    _unimplemented("C-14", "T005")


def test_c15_named_failure_sentinel():
    _text(DOC)
    _unimplemented("C-15", "T005")


def test_c16_gate_discipline_delegated_by_path():
    _text(DOC)
    _unimplemented("C-16", "T005")


def test_c17_surface_report_and_disclosure():
    _text(DOC)
    _unimplemented("C-17 (a)-(e)", "T005")


def test_c18_growth_loop_marker_and_bidirectional():
    _text(DOC)
    _unimplemented("C-18 (a)-(f)", "T042")


def test_c19_growth_loop_three_numbers():
    _text(DOC)
    _unimplemented("C-19", "T042")


def test_c21_project_neutral():
    _text(DOC)
    _unimplemented("C-21", "T005")


def test_c22_scope_limits_and_accepted_cost():
    _text(DOC)
    _unimplemented("C-22", "T050")


# --- ambient-section.md C-1..C-19 (bodies land in T016 / T050) -------------


def test_a1_template_heading_present():
    _text(INSTR)
    _unimplemented("A-1", "T016")


def test_a2_live_instructions_heading_present():
    _text(INSTR_LIVE)
    _unimplemented("A-2", "T016")


def test_a3_exactly_one_pointer_line_each():
    _text(INSTR)
    _unimplemented("A-3", "T016")


def test_a4_pointer_count_sentinel():
    _text(INSTR)
    _unimplemented("A-4", "T016")


def test_a5_four_discipline_sections_strict_order():
    _text(INSTR)
    _unimplemented("A-5", "T016")


def test_a6_not_inside_three_section_window():
    _text(INSTR)
    _unimplemented("A-6", "T016")


def test_a7_section_counts_18_to_19_and_19_to_20():
    _text(INSTR)
    _unimplemented("A-7", "T016")


def test_a8_no_inlined_section_names():
    _text(INSTR)
    _unimplemented("A-8", "T016")


def test_a9_house_lead_sentence_form():
    _text(INSTR)
    _unimplemented("A-9", "T016")


def test_a10_no_engine_invocation_form():
    _text(INSTR)
    _unimplemented("A-10", "T016")


def test_a11_project_neutral():
    _text(INSTR)
    _unimplemented("A-11", "T016")


def test_a12_no_speckit_command_form():
    _text(INSTR)
    _unimplemented("A-12", "T016")


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
    _text(DOC)
    _unimplemented("A-16", "T016")


def test_a17_instance_points_sentinel():
    _text(DOC)
    _unimplemented("A-17", "T016")


def test_a18_convergence_scope_bounded():
    _text(INSTR)
    _unimplemented("A-18", "T016")


def test_a19_channel_one_unobservable_self_statement():
    _text(INSTR)
    _unimplemented("A-19", "T016")


# --- constitution-export.md C-1..C-23 (bodies land in T025 / T050) ---------


def test_x1_template_principle_xiv():
    _text(CONST_TPL)
    _unimplemented("X-1", "T025")


def test_x2_command_must_include_entry():
    _text(CONST_CMD)
    _unimplemented("X-2", "T025")


def test_x3_double_landing_neither_side_missing():
    _text(CONST_TPL)
    _unimplemented("X-3 (drill: delete either side -> red)", "T025")


def test_x4_live_constitution_principle_xvi():
    _text(CONST_LIVE)
    _unimplemented("X-4", "T025")


def test_x5_live_version_minor_bump():
    _text(CONST_LIVE)
    _unimplemented("X-5", "T025")


def test_x6_sync_impact_report_prepended():
    _text(CONST_LIVE)
    _unimplemented("X-6", "T025")


def test_x7_version_three_segment_form():
    _text(CONST_LIVE)
    _unimplemented("X-7", "T025")


def test_x8_principle_block_structure():
    _text(CONST_TPL)
    _unimplemented("X-8", "T025")


def test_x9_principle_block_pointer_and_no_new_mechanism():
    _text(CONST_TPL)
    _unimplemented("X-9", "T025")


def test_x10_principle_block_lines_under_100():
    _text(CONST_TPL)
    _unimplemented("X-10", "T025")


def test_x11_principle_block_no_restated_content():
    _text(CONST_TPL)
    _unimplemented("X-11", "T025")


def test_x12_principle_block_project_neutral():
    _text(CONST_TPL)
    _unimplemented("X-12", "T025")


def test_x13_double_landing_three_count_pins():
    _text(DOUBLE_LANDING_TEST)
    _unimplemented("X-13", "T025")


def test_x14_min_version_floor_semantics():
    _text(DOUBLE_LANDING_TEST)
    _unimplemented("X-14", "T025")


def test_x15_watchlist_gains_principle_title():
    _text(DOUBLE_LANDING_TEST)
    _unimplemented("X-15", "T025")


def test_x16_plan_template_zero_change():
    _text(PLAN_TPL)
    _unimplemented("X-16", "T025")


def test_x17_plan_template_enumeration_sentinel():
    _text(PLAN_TPL)
    _unimplemented("X-17", "T025")


def test_x18_downstream_gate_rows_15_to_16():
    _text(PLAN_TPL)
    _unimplemented("X-18", "T025")


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
