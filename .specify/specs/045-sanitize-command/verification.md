# Verification Log — 045-sanitize-command

# -- Baseline (recorded once, BEFORE any /speckit.implement work changes the tree) --

baseline_commit=d5c8e8dd
baseline_date=2026-08-20
baseline_failed_names=44(baseline-failed.txt,冻结于 T001;全套件 44 failed / 1989 passed)

# -- Per-SC verification --

SC-001_status=pass
SC-001_value=夹具 + 本仓 dogfood 双源
SC-001_note=夹具:tests/fixtures/sanitize/stale-todo/parked-todo.md 复刻真实案例,tests/integration/test_sanitize_us1.py::test_us1_collect_record_status_flow 断言发现携带 commit 级证据引用(green)。dogfood(T031):本仓真实运行 collect→record,`.specify/memory/sanitize/findings.json` 落账 stale-residue 发现 1 条,evidenceRefs=[1a090c72, f86b8c23](证据包经 C-16 修订后无日期过滤 + 片段 glob 才命中——见 mechanism notes)。

SC-002_status=pass
SC-002_value=全量快照零变更
SC-002_note=契约测试 test_collect_creates_store_and_writes_nothing_else(前后快照,新文件仅台账)+ US1 集成 test_us1_collect_record_status_flow(new_files == {findings.json, verdicts.json}, changed == [])双断言 green;status 动作零写(test_status_is_zero_write)。

SC-003_status=pass
SC-003_value=确认前删除/移动数 = 0
SC-003_note=契约测试 test_apply_rejects_unconfirmed_plan_exits_2_zero_execution + 越界 target 拒绝(test_apply_rejects_out_of_whitelist_target_exits_2,用户代码 src/leak.py 存活)+ US3 集成 test_us3_gate_then_confirmed_apply(未确认 → 材料存活 → 确认 → 删除 → pending→resolved → 三要素执行报告)green。

SC-004_status=pass
SC-004_value=四类确定性判定零 LLM 参与
SC-004_note=tests/integration/test_sanitize_us2.py::test_us2_all_four_categories_programmatic 断言四类发现 detection==programmatic(SC-004);死引用/索引/链接/镜像单元测试 32 条全部为纯函数/文件系统断言。引擎侧 collect 对确定性发现不经 agent 径直入账(record 仅收语义判定,detection=programmatic 的输入被拒)。

SC-005_status=pass
SC-005_value=证据不足显式标记 + 证据引用可复核
SC-005_note=US1 集成断言证据不足材料不入账(vague.md 不在 store)+ 无 commit/path 证据的语义判定被 schema 拒绝(exit 2,tests/integration/test_sanitize_us1.py::test_us1_record_rejects_ungrounded_semantic_finding)。抽检:dogfood 落账的 stale-residue 发现 evidenceRefs 均为真实提交哈希(git show 可复核)。

# -- Task closure summary --

tasks_total=32
tasks_closed=32
tasks_deferred=0
deferred_tasks=

# -- Mechanism notes (dogfood-driven refinements, Loop B) --

# 1. 冻结历史豁免(C-1 修订):首轮 dogfood 926 项死引用中绝大多数来自
#    .specify/archive/spec/ 与 .specify/history/——引用描述归档时点的历史状态,
#    "失效"按设计。修订后死引用 917→691,残留 667 项集中于存活 specs(001-044
#    引用 docs 重构前的旧路径)——真实的历史累积信号,留待用户确认清理。
# 2. feedback 簿记文件豁免(C-7 修订):cleanup-log/consume-log/migration-log/
#    migration-plan/probe-map 是存储脚手架非条目;磁盘侧只认时间戳命名形态。
# 3. 孤儿目录补检收窄至 skills 对(C-12 修订):.specify/agents/ 的
#    templates/instances/execution 是 agent-definitions 分类法的合法运行时
#    结构,源侧无对应不构成改名残留;skills 对保留完整检测。
# 4. 证据包重设计(C-16 修订):真实案例的矛盾提交(1a090c72,07-30)早于声明
#    日期(08-12)——结转抄写陈旧结论的典型形态;--since 时间窗恰好滤掉矛盾
#    证据。修订:无日期过滤 + 计数截断(20)+ 文件名片段 glob(*platforms/
#    opencode.mjs 命中深层路径),两条真实案例回归测试固化。
# 5. sync-mirrors lane 局部性:mirror-drift 子进程仅在"工作区==引擎仓"时运行
#    (sync-mirrors 按脚本自身定位解析根,对外来工作区会检查错误的树)。

# -- Incident record (honest failure report) --

# 2026-08-20:Phase 3 提交(a0197299)意外包含 .specify/memory/todo/
# 20260812-evidence-session-backlog.md 的删除——未经过用户确认,违背确认门控
# 纪律;根因未能完全重建(疑为夹具制作期间的路径误操作,git add -A 将工作区
# 删除静默入册)。处置:git checkout d5c8e8dd -- <file> 恢复,经后续提交落盘
# (未 amend);dogfood 流程接管其处置(过期残留发现 pending,清理待用户确认)。
# 教训已记 feedback(审计 git add -A 的删除面)。

# -- Mirror obligations verification --

mirror_engine=diff -q scripts/python/sanitize-utils.py .specify/scripts/python/sanitize-utils.py → identical
mirror_probe_definitions=diff -q shared/definitions/probe-definitions.md .specify/shared/definitions/probe-definitions.md → identical
mirror_sync_check=python3 scripts/python/sync-mirrors.py --check → exit 0(all pairs ok)
regen_check=python3 scripts/python/regen-command-copies.py --check → zero stale;4 份 speckit.sanitize 副本存在且含源内容

# -- Governance surfaces --

gate_scanner=total 23(22+1 新破坏性清理门控,action_class=destructive,verdict=keep_gate);violations=[]
classification=复杂命令 17→18(test_feedback_command_classification.py)
probe_objects=+2(speckit-sanitize-wrapup / gate-sanitize-destructive-cleanup)
tool_record=.specify/memory/tools/sanitize-utils.py.md(Verified)
user_doc=docs/reference/commands/sanitize.md

# -- Final regression --

final_suite=44 failed / 2098 passed / 1 skipped(基线 44F/1989P;新增 109 通过,名字级 comm -13 为空,零新增失败)
completion_gate=GATE-1..6 全过(回归零新增/镜像 diff 一致 + sync-check exit 0/零未决任务行/SC-001..005 全覆盖/门控扫描 total 23 violations 空/regen --check 零 stale + 4 副本在位)
