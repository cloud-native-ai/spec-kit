# Quickstart — 068 Exec-Quant Feedback Channel

**Phase 1 output** (`/speckit.plan`, 2026-10-22). 四个场景按通道时序排列；每个命令
示例标注其执行-核验路由：(a) = 本阶段已对真实工具执行（输出已贴），(b) = 由
契约测试钉住有效性（实现阶段落地时按测试断言核验）。**本阶段不实现任何运行时
行为**，场景 1–3 的引擎命令尚不存在——逐例前提（premises）逐条列出，供
`/speckit.tasks` 与 `/speckit.implement` 重测而非继承。

---

## 场景 0 — 存储形态探测（今天可执行，route a）

两条既有引擎命令，实测于本仓与样例客户项目（2026-10-22）：

```bash
# route (a): 已执行, exit=0 — 首行即 schema_version=1 遗留记录（v1/v2 并存的实证）
python3 .specify/scripts/python/exec-quant.py --action list-records --format json
#   → [ { "kind": "speckit.exec-quant", "schema_version": 1,
#         "unit_id": "/speckit.implement", "run_id": "059-exec-quant-smoke", ... }, ... ]

python3 .specify/scripts/python/feedback-utils.py --action status --format json
#   → {"count_since_submission": 114, "threshold": 10, "should_prompt": true, ...} (exit=0)

# 样例客户项目存储形态（route (a), ls 实测）:
ls /storage/project/cloud-native-tools/cws-lib-python/.specify/memory/exec-quant/records/
#   → 20261022T031603362890Z-fbc69dd4.json ...（7 条 v2）
ls /storage/project/cloud-native-tools/cws-lib-python/.specify/memory/exec-quant/scores/
#   → （空目录）
```

**证明点**: 两类存储布局（本仓 records/ + 遗留 jsonl 并存；样例项目仅 records/ +
空 scores/）与字段形态混合真实存在——FR-007 的容忍面不是假设。

## 场景 1 — 客户项目打包（实现后；route b：由
`tests/contract/test_feedback_exec_quant_payload.py` 钉住，见 premises）

```bash
# 在客户项目（如 cws-lib-python）根目录：
python3 .specify/scripts/python/feedback-utils.py --action package --format json
# 期望输出新增: "exec_quant_payload": {"record_count": 7, "skipped_unreadable": 0,
#   "truncated_count": 0, "source_form_counts": {"records-dir": 7, "legacy-jsonl": 0}, ...}
unzip -l .specify/memory/feedback/packages/feedback-<ts>.zip | grep exec-quant
#   → exec-quant/payload-manifest.json + exec-quant/records/*.json（7 条）
```

**Premises（逐例，实现前均为待重测假设）**: ① 输出键名 `exec_quant_payload`
与子键集合为设计态（C-PL-07）；② `exec-quant/` 成员路径前缀（C-PL-03）；
③ 该项目 instructions.md 含 Project Name 行 → 身份 identified（C-PL-05）；
④ FR-019：若该项目 feedback 条目为空而记录 ≥1，同命令仍产出包
（`Entries: 0` + 载荷，C-PL-08）。测试钉住 ①②④ 的断言形态；③ 由
test_feedback_exec_quant_payload 的身份用例钉住。

## 场景 2 — spec-kit 接收（实现后；route b：由
`tests/contract/test_feedback_intake_exec_quant.py` 钉住）

```bash
# 手工送达的包落 feedback/ 后，Path A A2 步骤内：
python3 .specify/scripts/python/feedback-utils.py --action ingest-exec-quant \
  --package feedback/feedback-<ts>.zip --format json
# 期望输出: {"record_count": 7, "ingested": 7, "duplicates_skipped": 0, ...}
# 二次执行同一包 → {"ingested": 0, "duplicates_skipped": 7}（幂等, C-IN-04）
ls .specify/memory/exec-quant/aggregated/cws-lib-python-*/records/ | wc -l   # → 7
ls .specify/memory/feedback/*.md | grep -c exec-quant || true               # → 0（零混入）
```

**Premises**: ① 动作名 `ingest-exec-quant` 与 `--package` 旗标（C-IN-01）；
② 分组目录 `aggregated/<source-slug>/records/` 与 slug 形态（data-model § E6）；
③ 幂等输出键（C-IN-07）。全部由测试断言钉住；`feedback/` 清单核对（零混入，
C-CS-07）由测试的 store 隔离断言钉住。

## 场景 3 — 跨项目汇总（实现后；route b：由
`tests/contract/test_exec_quant_aggregate.py` 钉住）

```bash
# 聚合层含 ≥2 源项目后，维护者显式执行（接收不自动汇总, C-AG-06）：
python3 .specify/scripts/python/exec-quant.py --action aggregate --format json
# 期望: stdout JSON（sources[] 按 project 分组, units/quality/coverage/record_files,
#       totals）+ 落盘 .specify/memory/exec-quant/aggregated/summaries/<id>.json
```

**Premises**: ① 动作名 `aggregate` 与 `--format` 旗标（C-AG-01）；② 视图字段
集合（C-AG-03）；③ 产物路径与文件形态（C-AG-05）。测试钉住断言形态；
`record_files[]` 可对账（FR-011）由测试的名单重放断言钉住。

## 场景 4 — 回归基线比对（实现前后各一次，route a：实现前基线已于本阶段冻结）

```bash
python3 -m pytest tests/contract/test_feedback_utils_cli.py \
  tests/contract/test_feedback_entry_schema.py \
  tests/contract/test_feedback_mechanism_boundary.py \
  tests/contract/test_feedback_skill_conformance.py \
  tests/contract/test_feedback_two_path_routing.py \
  tests/contract/test_feedback_command_template.py \
  tests/contract/test_feedback_command_classification.py \
  tests/contract/test_feedback_introspection_engine.py \
  tests/contract/test_feedback_introspection_report.py \
  tests/contract/test_feedback_probe_cli.py \
  tests/contract/test_feedback_probe_entry_schema.py \
  tests/contract/test_feedback_probe_registry.py \
  tests/contract/test_feedback_step_reference_form.py \
  tests/contract/test_token_efficiency_feedback.py \
  tests/contract/test_exec_quant_engine.py \
  tests/contract/test_exec_quant_dispatch.py \
  tests/unit/test_feedback_package.py tests/unit/test_feedback_utils.py \
  tests/integration/test_feedback_command_record.py \
  tests/integration/test_feedback_dedup.py tests/integration/test_feedback_partial.py \
  tests/integration/test_feedback_selective_triggering.py \
  tests/integration/test_feedback_skill_record.py \
  tests/integration/test_feedback_threshold.py -q
# 实现前基线（本阶段 2026-10-22 实跑）: 全部通过, 0 failed —— 见
# test-evidence/log-baseline-pre-impl.txt（排序 nodeid 失败名单 = 空名单）
```

**核验形态**（SC-006 / C-CS-03）: 实现后重跑同一命令集，排序失败 nodeid 名单与
冻结基线逐名比对零新增；**名字级**而非计数级（新增通过的用例不算回归，新增
失败必须逐名解释）。

## 场景 5 — 无载荷包零差异（实现后；route b：由
`tests/contract/test_feedback_intake_exec_quant.py` 无载荷用例钉住）

```bash
# 068 前形态入站包（如 feedback/feedback-20261022T062525Z.zip 同构）:
python3 .specify/scripts/python/feedback-utils.py --action ingest-exec-quant \
  --package feedback/feedback-<ts>.zip --format json
# 期望: {"record_count": 0, "ingested": 0, ...} exit=0；feedback 条目处理行为零变化
```

**Premises**: 无载荷 → 零计数零写入零报错（C-IN-02 / C-CS-04）；聚合层目录
零创建（无写入即无 mkdir 副作用）。该真实基线包本身为只读参考
（`feedback/feedback-20261022T062525Z.zip` 禁改禁删——本线派发约束），测试用
自构等构包，不触碰真实包。
