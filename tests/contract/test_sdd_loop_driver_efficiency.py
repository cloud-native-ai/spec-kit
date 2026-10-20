"""Contract tests for Feature 063 efficiency clauses.

One named test function per clause:
  FL-01…FL-10 (fast lane), TB-01…TB-10 (test budget),
  PC-01…PC-11 (plan constraint), PD-01…PD-10 (progress decoupling),
  DI-01…DI-09 (delivery and invariants).

The file is authored incrementally per user story; each story's tests go
red-first. The T046 coverage meta-test asserts that every clause id in
``contracts/*.md`` has its named function.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "skills" / "external" / "sdd-loop-driver"
EFFICIENCY = SKILL_DIR / "references" / "efficiency-model.md"
RECIPES = SKILL_DIR / "references" / "dispatch-recipes.md"
PROMPTS = SKILL_DIR / "references" / "stage-prompts.md"
WATCH = SKILL_DIR / "references" / "watch-model.md"
SKILL_MD = SKILL_DIR / "SKILL.md"
DOCS_PAGE = REPO_ROOT / "docs" / "reference" / "skills" / "sdd-loop-driver.md"
SPEC_DIR = REPO_ROOT / ".specify" / "specs" / "063-sdd-loop-efficiency"
REQUIREMENTS = SPEC_DIR / "requirements.md"
CONTRACTS = SPEC_DIR / "contracts"


def _text(path):
    assert path.exists(), "missing required file: %s" % path
    return path.read_text(encoding="utf-8")


def _run(args):
    return subprocess.run(
        [sys.executable] + [str(item) for item in args],
        capture_output=True, text=True,
    )


def _script_help(name):
    script = SKILL_DIR / "scripts" / name
    prefix = ["bash"] if name.endswith(".sh") else [sys.executable]
    completed = subprocess.run(
        prefix + [str(script), "--help"], capture_output=True, text=True)
    assert completed.returncode == 0, completed.stderr
    return completed.stdout + completed.stderr


# ------------------------------------------------------------------ FL-01


def test_fl_01_opt_in_literal_pinned():
    text = _text(EFFICIENCY)
    assert "fast-lane=opt-in" in text
    assert "唯一" in text and "启用" in text
    assert "无人值守" in text
    assert "自然语言" in text


# ------------------------------------------------------------------ FL-02


def test_fl_02_admission_point_and_sequence_policy():
    recipes = _text(RECIPES)
    assert "tasks" in recipes and "checklist" in recipes
    assert "admission-check.py" in recipes
    assert "快车道保留 analyze" in recipes or ("保留" in recipes and "analyze" in recipes)
    efficiency = _text(EFFICIENCY)
    assert "tasks.md" in efficiency and "checklist" in efficiency
    assert "analyze" in efficiency and "review" in efficiency


# ------------------------------------------------------------------ FL-03


def test_fl_03_criteria_table_pinned():
    efficiency = _text(EFFICIENCY)
    for criterion in "abcdefg":
        assert re.search(r"\|\s*\(%s\)" % criterion, efficiency), (
            "criterion (%s) missing from the owner table" % criterion)
    requirements = _text(REQUIREMENTS)
    assert "`^- **FR-[0-9]{3}**:`" in requirements
    assert "`^- \\[[ xX]\\] T[0-9]{3}`" in requirements
    assert "`^- \\[[ xX>~]\\] T[0-9]{3}`" in requirements
    source = _text(SKILL_DIR / "scripts" / "admission-check.py")
    assert "FR_MIN = 8" in source and "FR_MAX = 30" in source
    assert "TASK_MIN = 10" in source and "TASK_MAX = 40" in source
    assert "数据模型" in efficiency or "lines.manifest" in efficiency


# ------------------------------------------------------------------ FL-04


def test_fl_04_admission_record_fields():
    efficiency = _text(EFFICIENCY)
    for field in ("decision", "entry_evidence", "criteria", "measured",
                  "decided_at", "reversion"):
        assert field in efficiency, "admission record field missing: %s" % field
    assert "checklist=skipped(fast-lane)" in efficiency
    data_model = _text(SPEC_DIR / "data-model.md")
    assert "E1 — Fast-Lane Admission Record" in data_model


# ------------------------------------------------------------------ FL-05


def test_fl_05_downstream_publication():
    prompts = _text(PROMPTS)
    assert "checklist=skipped(fast-lane)" in prompts
    assert "admission" in prompts.lower() or "准入" in prompts
    assert "implement" in prompts and "review" in prompts
    efficiency = _text(EFFICIENCY)
    assert "下游" in efficiency and "发布" in efficiency


# ------------------------------------------------------------------ FL-06


def test_fl_06_reversion_procedure():
    efficiency = _text(EFFICIENCY)
    assert "回退" in efficiency
    assert "checklist" in efficiency
    assert "analyze" in efficiency
    assert "证据" in efficiency
    recipes = _text(RECIPES)
    assert "回退" in recipes


# ------------------------------------------------------------------ FL-07


def test_fl_07_analyze_review_unchanged():
    efficiency = _text(EFFICIENCY)
    assert "CRITICAL" in efficiency and "HIGH" in efficiency
    assert "有界回环" in efficiency or "一轮" in efficiency
    assert "review" in efficiency
    assert "不削弱" in efficiency or "不变" in efficiency


# ------------------------------------------------------------------ FL-08


def test_fl_08_admission_script_interface():
    help_text = _script_help("admission-check.py")
    for flag in ("--project", "--base-ref", "--requirements", "--tasks",
                 "--checklists", "--entry-evidence", "--lines-manifest",
                 "--expected-branch"):
        assert flag in help_text, "admission-check flag missing: %s" % flag
    source = _text(SKILL_DIR / "scripts" / "admission-check.py")
    assert "admissible" in source and "rejected" in source and "input" in source
    assert "standard library" in source.lower() or "stdlib" in source
    imports = re.findall(r"^import\s+([A-Za-z_][A-Za-z0-9_]*)", source, re.MULTILINE)
    allowed = {"argparse", "json", "os", "re", "subprocess", "sys", "time", "pathlib"}
    assert set(imports) <= allowed, "unexpected import: %s" % (set(imports) - allowed)
    assert ".specify/scripts" not in source


# ------------------------------------------------------------------ FL-09


def test_fl_09_definition_owned_and_pinned():
    efficiency = _text(EFFICIENCY)
    assert "唯一 owner" in efficiency or "唯一owner" in efficiency
    assert "快车道" in efficiency
    assert "tests/contract/test_sdd_loop_driver_efficiency.py" in efficiency
    assert (SKILL_DIR / "scripts" / "admission-check.py").exists()


# ------------------------------------------------------------------ FL-10


def test_fl_10_self_application_exclusion():
    requirements = _text(REQUIREMENTS)
    assert "**FR-010**" in requirements
    assert "完整阶段链" in requirements
    efficiency = _text(EFFICIENCY)
    assert "063" in efficiency and "完整阶段链" in efficiency
    assert "MUST NOT" in efficiency
    feature_ref = _text(SPEC_DIR / "feature-ref.md")
    assert "自应用" in feature_ref


# ------------------------------------------------------------------ TB-01


def test_tb_01_full_run_definition():
    efficiency = _text(EFFICIENCY)
    assert "全量测试运行" in efficiency
    assert "运行线" in efficiency
    assert "不带路径" in efficiency or "无路径" in efficiency
    contract = _text(CONTRACTS / "test-budget.md")
    assert "TB-01" in contract and "运行线" in contract


# ------------------------------------------------------------------ TB-02


def test_tb_02_two_slots_only():
    efficiency = _text(EFFICIENCY)
    assert "恰好两个槽位" in efficiency or "两个全量槽位" in efficiency
    assert "baseline" in efficiency and "closure" in efficiency
    assert "review" in efficiency and "合并之前" in efficiency


# ------------------------------------------------------------------ TB-03


def test_tb_03_baseline_prompt():
    prompts = _text(PROMPTS)
    assert "--names-out" in prompts
    assert "STATE_SPINE_PATH" in prompts
    assert "第二次全量" in prompts or "禁止第二次全量" in prompts
    assert "baseline_slot=skip(closure-repair)" in prompts
    efficiency = _text(EFFICIENCY)
    assert "implement 起点" in efficiency
    assert "E2" in efficiency and "状态脊" in efficiency


# ------------------------------------------------------------------ TB-04


def test_tb_04_name_level_diff():
    source = _text(SKILL_DIR / "scripts" / "audit-test-budget.py")
    assert "comm -13" in source or "comm" in source
    assert "baseline_compare" in source
    efficiency = _text(EFFICIENCY)
    assert "comm -13" in efficiency
    assert "名称级" in efficiency


# ------------------------------------------------------------------ TB-05


def test_tb_05_targeted_selection_rule():
    efficiency = _text(EFFICIENCY)
    assert "targeted-set-v1" in efficiency
    for token in ("stage_base", "changed_paths", "test_roots",
                  "LC_ALL=C sort -u", "(a)", "(b)", "(c)"):
        assert token in efficiency, "targeted-set-v1 input missing: %s" % token
    contract = _text(CONTRACTS / "test-budget.md")
    assert "targeted-set-v1" in contract and "TB-05" in contract


# ------------------------------------------------------------------ TB-06


def test_tb_06_evidence_fields():
    efficiency = _text(EFFICIENCY)
    for token in ("selected_paths", "selection_basis", "sufficiency",
                  "new_failures", "not-run-docs-only",
                  "not-applicable-skipped-stage", "empty-selection-escalated"):
        assert token in efficiency, "E3 evidence token missing: %s" % token
    assert "六项" in efficiency or "缩减字段集" in efficiency


# ------------------------------------------------------------------ TB-07


def test_tb_07_ledger_audit_unknown():
    help_text = _script_help("audit-test-budget.py")
    for flag in ("--spine", "--spec-dir", "--logs-dir", "--stage-check"):
        assert flag in help_text, "audit flag missing: %s" % flag
    source = _text(SKILL_DIR / "scripts" / "audit-test-budget.py")
    assert "unknown" in source
    assert "stage-status" in source
    assert "stages=" in source and "complete=" in source
    assert "test-budget:begin" in source and "test-budget:end" in source


# ------------------------------------------------------------------ TB-08


def test_tb_08_exception_and_rerun():
    efficiency = _text(EFFICIENCY)
    assert "out-of-slot-exception" in efficiency
    assert "in-slot-rerun" in efficiency
    assert "槽外" in efficiency and "槽内" in efficiency
    source = _text(SKILL_DIR / "scripts" / "audit-test-budget.py")
    assert "out-of-slot-exception" in source
    assert "in-slot-rerun" in source


# ------------------------------------------------------------------ TB-09


def test_tb_09_environment_failure_no_slot():
    efficiency = _text(EFFICIENCY)
    assert "environment-failure" in efficiency
    assert "不消耗槽位" in efficiency
    source = _text(SKILL_DIR / "scripts" / "audit-test-budget.py")
    assert "environment-failure" in source
    assert "environment_evidence" in source


# ------------------------------------------------------------------ TB-10


def test_tb_10_orchestration_layer_only():
    efficiency = _text(EFFICIENCY)
    assert "编排层" in efficiency
    assert "框架命令内部" in efficiency
    contract = _text(CONTRACTS / "test-budget.md")
    assert "TB-10" in contract and "编排层" in contract


# ------------------------------------------------------------------ PC-01


def test_pc_01_activation_point():
    efficiency = _text(EFFICIENCY)
    for token in ("plan_constraint=active", "activated_at", "plan_commit",
                  "approved_baseline_commit"):
        assert token in efficiency, "PC-01 token missing: %s" % token
    recipes = _text(RECIPES)
    assert "plan_constraint" in recipes or "只小修" in recipes


# ------------------------------------------------------------------ PC-02


def test_pc_02_minor_definition():
    efficiency = _text(EFFICIENCY)
    for token in ("错别字", "断链", "格式", "行级一致性"):
        assert token in efficiency, "minor definition token missing: %s" % token


# ------------------------------------------------------------------ PC-03


def test_pc_03_substantive_final_diff():
    efficiency = _text(EFFICIENCY)
    assert "实质改动" in efficiency
    assert "最终 diff" in efficiency or "最终差异" in efficiency
    assert "范围" in efficiency and "架构" in efficiency


# ------------------------------------------------------------------ PC-04


def test_pc_04_prompt_block_and_plan_edit():
    prompts = _text(PROMPTS)
    assert "PLAN-EDIT:" in prompts
    assert "ANOMALY:" in prompts
    assert "只小修" in prompts
    assert "tasks" in prompts and "implement" in prompts and "review" in prompts


# ------------------------------------------------------------------ PC-05


def test_pc_05_u4_diff_check():
    efficiency = _text(EFFICIENCY)
    assert "git diff --name-only" in efficiency
    assert "git status --porcelain" in efficiency
    assert "U4" in efficiency


# ------------------------------------------------------------------ PC-06


def test_pc_06_routing_branches():
    efficiency = _text(EFFICIENCY)
    assert "approved_baseline_commit" in efficiency
    assert "四要素" in efficiency
    assert "(a)" in efficiency and "(b)" in efficiency
    assert "requirements.md" in efficiency


# ------------------------------------------------------------------ PC-07


def test_pc_07_analyze_repair_unchanged():
    efficiency = _text(EFFICIENCY)
    assert "analyze" in efficiency
    assert "不取消" in efficiency or "不削弱" in efficiency
    assert "重过该门" in efficiency or "重过" in efficiency


# ------------------------------------------------------------------ PC-08


def test_pc_08_wrapup_reporting():
    efficiency = _text(EFFICIENCY)
    assert "收尾汇总" in efficiency
    assert "分类" in efficiency and "处置" in efficiency


# ------------------------------------------------------------------ PC-09


def test_pc_09_explicit_exclusion():
    efficiency = _text(EFFICIENCY)
    assert "显式排除" in efficiency
    assert "手工调用" in efficiency
    assert "框架命令内部" in efficiency


# ------------------------------------------------------------------ PC-10


def test_pc_10_audit_script_interface():
    help_text = _script_help("audit-plan-changes.py")
    for flag in ("--repo", "--base", "--head", "--plan-owned", "--declarations"):
        assert flag in help_text, "audit-plan-changes flag missing: %s" % flag
    source = _text(SKILL_DIR / "scripts" / "audit-plan-changes.py")
    for token in ("touched_paths", "declaration_lines", "undeclared", "diff_stats"):
        assert token in source, "output field missing: %s" % token
    imports = re.findall(r"^import\s+([A-Za-z_][A-Za-z0-9_]*)", source, re.MULTILINE)
    allowed = {"argparse", "json", "os", "re", "subprocess", "sys", "pathlib"}
    assert set(imports) <= allowed, "unexpected import: %s" % (set(imports) - allowed)
    assert ".specify/scripts" not in source


# ------------------------------------------------------------------ PC-11


def test_pc_11_reanchoring():
    efficiency = _text(EFFICIENCY)
    for token in ("rebaseline_events", "approved_baseline_commit",
                  "未提交", "不可定位", "plan 重审"):
        assert token in efficiency, "PC-11 token missing: %s" % token
    assert "此后一律使用**最新**锚点" in efficiency
    recipes = _text(RECIPES)
    assert "activated_at" in recipes or "重入" in recipes
    contract = _text(CONTRACTS / "plan-constraint.md")
    assert "PC-11" in contract


# ------------------------------------------------------------------ PD-01


def test_pd_01_stream_default_and_raw():
    efficiency = _text(EFFICIENCY)
    assert "stream-json" in efficiency
    assert "raw-<line>-<stage>.jsonl" in efficiency
    assert "064" in efficiency
    runner = _text(SKILL_DIR / "scripts" / "stage-runner.sh")
    assert "stream-json" in runner
    help_text = _script_help("stage-runner.sh")
    assert "--mode" in help_text and "--cli-args" in help_text


# ------------------------------------------------------------------ PD-02


def test_pd_02_incremental_live_log():
    efficiency = _text(EFFICIENCY)
    assert "增量" in efficiency
    assert "120" in efficiency
    derive = _text(SKILL_DIR / "scripts" / "derive-live-log.py")
    assert "evt=" in derive and "at=" in derive
    assert "flush" in derive
    help_text = _script_help("derive-live-log.py")
    for flag in ("--events", "--out", "--finish"):
        assert flag in help_text, "derive flag missing: %s" % flag


# ------------------------------------------------------------------ PD-03


def test_pd_03_sentinel_from_result_only():
    efficiency = _text(EFFICIENCY)
    assert "终止" in efficiency and "result" in efficiency
    assert "非终止" in efficiency
    derive = _text(SKILL_DIR / "scripts" / "derive-live-log.py")
    assert "result" in derive
    runner = _text(SKILL_DIR / "scripts" / "stage-runner.sh")
    assert "sentinel" in runner


# ------------------------------------------------------------------ PD-04


def test_pd_04_watcher_unchanged():
    watch_text = _text(WATCH)
    assert "raw" in watch_text and "stream" in watch_text
    help_text = _script_help("watch-target.sh")
    assert "--raw-stream" in help_text
    assert "0 DONE" in help_text and "14 TIMEOUT" in help_text
    efficiency = _text(EFFICIENCY)
    assert "判定" in efficiency and "不变" in efficiency


# ------------------------------------------------------------------ PD-05


def test_pd_05_degradation_marker():
    runner = _text(SKILL_DIR / "scripts" / "stage-runner.sh")
    for token in ("degraded", "derivation-recovered", "buffered-fallback",
                  "sentinel=0"):
        assert token in runner, "degradation token missing: %s" % token
    efficiency = _text(EFFICIENCY)
    assert "降级" in efficiency and "伪完成" in efficiency


# ------------------------------------------------------------------ PD-06


def test_pd_06_nohup_both_topologies():
    recipes = _text(RECIPES)
    assert "nohup" in recipes
    assert "</dev/null" in recipes
    assert "ssh" in recipes
    efficiency = _text(EFFICIENCY)
    assert "nohup" in efficiency and "本地" in efficiency and "远端" in efficiency


# ------------------------------------------------------------------ PD-07


def test_pd_07_reentry_once():
    prompts = _text(PROMPTS)
    assert "--once" in prompts
    recipes = _text(RECIPES)
    assert "--once" in recipes
    efficiency = _text(EFFICIENCY)
    assert "--once" in efficiency


# ------------------------------------------------------------------ PD-08


def test_pd_08_watcher_raw_and_selftests():
    help_text = _script_help("watch-target.sh")
    assert "--raw-stream" in help_text
    watch_source = _text(SKILL_DIR / "scripts" / "watch-target.sh")
    for case in ("stream-nonterminal-sentinel", "stream-result-sentinel",
                 "stream-derive-failure", "stream-detached-survives"):
        assert case in watch_source, "self-test case missing: %s" % case


# ------------------------------------------------------------------ PD-09


def test_pd_09_no_new_wait_or_service():
    efficiency = _text(EFFICIENCY)
    assert "sleep" in efficiency
    assert "常驻服务" in efficiency
    assert "MUST NOT" in efficiency
    runner = _text(SKILL_DIR / "scripts" / "stage-runner.sh")
    assert "sleep" in runner


# ------------------------------------------------------------------ PD-10


def test_pd_10_runner_interface():
    help_text = _script_help("stage-runner.sh")
    for flag in ("--cli", "--cli-args", "--project-dir", "--prompt-file",
                 "--sentinel", "--line", "--stage", "--state-dir", "--mode",
                 "--detached"):
        assert flag in help_text, "runner flag missing: %s" % flag
    runner = _text(SKILL_DIR / "scripts" / "stage-runner.sh")
    for token in ("exit", "status", "heartbeat", "detached"):
        assert token in runner
    derive = _text(SKILL_DIR / "scripts" / "derive-live-log.py")
    imports = re.findall(r"^import\s+([A-Za-z_][A-Za-z0-9_]*)", derive, re.MULTILINE)
    allowed = {"argparse", "json", "os", "re", "sys", "time", "pathlib"}
    assert set(imports) <= allowed, "unexpected import: %s" % (set(imports) - allowed)
    assert "jq" not in derive


# ------------------------------------------------------------------ DI-01


def test_di_01_confirmation_gates_unchanged():
    skill = _text(SKILL_MD)
    assert "push" in skill
    assert "确认门" in skill or "确认" in skill
    docs = _text(DOCS_PAGE)
    assert "确认门" in docs or "确认" in docs


# ------------------------------------------------------------------ DI-02


def test_di_02_independent_verification_unchanged():
    prompts = _text(PROMPTS)
    assert "独立校验" in prompts
    assert "校验者不是该阶段的执行子代理" in prompts
    skill = _text(SKILL_MD)
    assert "独立校验" in skill


# ------------------------------------------------------------------ DI-03


def test_di_03_stall_handling_unchanged():
    fixture = _text(REPO_ROOT / "tests" / "fixtures" / "sdd_loop_efficiency"
                    / "driver-stall-fixture.py")
    assert "initial_retries" in fixture
    assert "exit_code" in fixture
    assert "watch-target.sh" in fixture
    baseline = json.loads((SPEC_DIR / "notes" / "stall-behavior-baseline.json")
                          .read_text(encoding="utf-8"))
    assert baseline["initial_retries"] == 0
    assert len(baseline["scenarios"]) == 4
    assert {scenario["next_stage_dispatched"]
            for scenario in baseline["scenarios"]} == {"yes", "no"}
    for scenario in baseline["scenarios"]:
        assert set(scenario["exit_code"]) == {"watcher", "runner"}
        assert not scenario["evidence_ptr"].startswith(("/var/folders/", "/tmp/"))
    prompts = _text(PROMPTS)
    assert "四要素" in prompts and "状态脊" in prompts


# ------------------------------------------------------------------ DI-04


def test_di_04_quality_gates_not_weakened():
    skill = _text(SKILL_MD)
    assert "analyze" in skill and "review" in skill
    assert "不可省略" in skill
    efficiency = _text(EFFICIENCY)
    assert "不削弱" in efficiency or "MUST NOT 改变" in efficiency
    assert "测试预算" in efficiency


# ------------------------------------------------------------------ DI-05


def test_di_05_delivery_and_mirror():
    docs = _text(DOCS_PAGE)
    assert "运行效率优化" in docs
    check = _run([REPO_ROOT / "scripts" / "python" / "sync-mirrors.py",
                  "--check", "--only", "skills/external/sdd-loop-driver"])
    assert check.returncode == 0, check.stdout + check.stderr
    for path in ("SKILL.md", "references/efficiency-model.md",
                 "scripts/admission-check.py", "scripts/audit-test-budget.py",
                 "scripts/audit-plan-changes.py", "scripts/derive-live-log.py",
                 "scripts/stage-runner.sh", "scripts/watch-target.sh"):
        assert (SKILL_DIR / path).exists(), "deliverable missing: %s" % path


# ------------------------------------------------------------------ DI-06


def test_di_06_contract_and_fixtures():
    fixtures = REPO_ROOT / "tests" / "fixtures" / "sdd_loop_efficiency"
    for path in ("medium", "large", "plan-repo", "state-spine-valid.md",
                 "stream/non_terminal_sentinel.jsonl",
                 "stream/result_sentinel.jsonl", "stream/malformed.jsonl",
                 "stub-cli.sh", "driver-stall-fixture.py"):
        assert (fixtures / path).exists(), "fixture missing: %s" % path
    for path in ("tests/unit/test_admission_check.py",
                 "tests/unit/test_audit_test_budget.py",
                 "tests/unit/test_audit_plan_changes.py",
                 "tests/unit/test_derive_live_log.py",
                 "tests/integration/test_sdd_loop_efficiency_runner.py",
                 "tests/integration/test_sdd_loop_efficiency_regression.py"):
        assert (REPO_ROOT / path).exists(), "test missing: %s" % path


# ------------------------------------------------------------------ DI-07


def test_di_07_self_application():
    requirements = _text(REQUIREMENTS)
    assert "**FR-010**" in requirements
    assert "完整阶段链" in requirements
    assert (SPEC_DIR / "checklists" / "requirements.md").exists()
    assert (SPEC_DIR / "checklists" / "efficiency.md").exists()
    feature_ref = _text(SPEC_DIR / "feature-ref.md")
    assert "自应用" in feature_ref
    efficiency = _text(EFFICIENCY)
    assert "063" in efficiency and "MUST NOT" in efficiency


# ------------------------------------------------------------------ DI-08


def test_di_08_backward_compatible():
    docs = _text(DOCS_PAGE)
    assert "progress=degraded" in docs
    assert "完成判定不变" in docs
    efficiency = _text(EFFICIENCY)
    assert "完整链是缺省行为" in efficiency
    prompts = _text(PROMPTS)
    assert "sentinel" in prompts.lower() or "哨兵" in prompts
    watch_help = _script_help("watch-target.sh")
    assert "0 DONE" in watch_help and "15 INCOMPLETE" in watch_help


# ------------------------------------------------------------------ DI-09


def test_di_09_orchestration_layer_only():
    efficiency = _text(EFFICIENCY)
    assert "编排层" in efficiency
    assert "框架命令内部" in efficiency
    assert "显式排除" in efficiency
    contract = _text(CONTRACTS / "delivery-and-invariants.md")
    assert "DI-09" in contract and "编排层" in contract


# ------------------------------------------------------- coverage meta-test


def test_all_contract_clauses_have_named_tests():
    source = Path(__file__).read_text(encoding="utf-8")
    clauses = []
    for contract in sorted(CONTRACTS.glob("*.md")):
        text = contract.read_text(encoding="utf-8")
        for match in re.finditer(r"^- \*\*(FL|TB|PC|PD|DI)-(\d{2})", text,
                                 re.MULTILINE):
            clauses.append((match.group(1), match.group(2)))
    assert len(clauses) == 50, "expected 50 clauses, found %d" % len(clauses)
    missing = []
    for prefix, number in clauses:
        name = "test_%s_%s_" % (prefix.lower(), number)
        if ("def %s" % name) not in source:
            missing.append("%s-%s" % (prefix, number))
    assert not missing, "clauses without a named test: %s" % missing
