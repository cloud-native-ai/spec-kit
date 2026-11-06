# Checkpoint 06 — analyze

## 1. Artifact verification

- sentinel: `ANALYZE-DONE`（round 2 只读复核最后一非空行；round 1 报告与 repair 证据已落盘）
- U4: `pass` — round 2 findings：**0 CRITICAL / 0 HIGH / 4 MEDIUM / 7 LOW**；放行判据（CRITICAL/HIGH 为零或已处置）成立。
  - round 1：0 CRITICAL / 2 HIGH（F-01 契约→test/green 绑定错位；F-02 docs/ 零改动冲突）/ 7 MEDIUM / 7 LOW
  - 有界修复 `7b6b6cc6`：39/39 可判定条款 ID 各声明一次 + `C-008a` 子条款经 `I::test_c008a_*` 具名断言（不重编号）；F-02 收窄为「`docs/` 恰一行 `docs/concepts/documentation-model.md`」；MEDIUM/LOW 处置；coverage 基线 573
  - round 2：F-01/F-02 闭环；回归 19/19 宪法、EP-001/Inherited、Feature Planned、Mirror Obligations、无越界均通过；门禁读数一致（validate-tasks PASS / decomposition proceed 76 / pre-analyze tasks pass 77 advisories / tensions 0 error / requirements ok / coverage clause pass 573）
- artifacts:
  - `test-evidence/analyze-report-round1.md`、`test-evidence/analyze-repair-round1.md`、`test-evidence/analyze-stage-status.jsonl`（round 2 更新同一行，仍恰一行六字段）
  - repair commit `7b6b6cc6`
- 残留（MEDIUM/LOW，已记录，交 implement 阶段处置或登记）:
  - M1：plan 表 A/B 的具名断言清单与 tasks 清单存在漂移；diagram C-009/C-015 的断言在 tasks 中缺名；flow C-022 槽位被 FR-021 主体占用；plan 应作为唯一登记处，tasks 改为指向它。
  - M2：F-02 收窄未传播到 `requirements.md:289` Out of Scope、`plan.md:30/32/81`、`feature-ref.md:72`；操作门 GATE-6 已正确。requirements 的 Out of Scope 修正属 re-baseline 事件，交 implement 前的驱动处置或 review 承接。
  - M3：C-01 夹具不变量仅在 `data-model.md` E6 改为「仓库副本 == 登记构成」；`plan.md:493`、`tasks.md:22/77`、`quickstart.md:164` 仍是旧读法；DoD-4 字面不可满足。
  - M4：测试文件预算「2 个新文件」与 tasks 的 4 个新文件（T009 carriers、T028/T031/T032/T034 reuse）矛盾；plan 表 A C-014 引用 reuse 文件。
  - L1：`feature-ref.md:30` 仍列 `.specify/templates/commands/docs.md` 为生成副本（不存在/已退役）。
  - L2：`feature-ref.md:75`、`plan.md:84` 仍称 OI-087-01 未决；register 已 resolved。
  - L3：`data-model.md:46` 仍把「封闭五值 + 有序优先级」记在 C-004 名下；C-016 是唯一 owner。
  - L4：`quickstart.md:217` 用 unit 文件 `-k reconcile` 选 C-008a 断言；实际断言在 integration 文件。
  - L5：`quickstart.md:307`、`diagram-obligation.contract.md:322` 引用 plan 不存在的章节。
  - L6：repair 证据写 pre-analyze advisories=84，round 2 实测 77。
  - L7：C-012 四项「各由自己的夹具驱动」与 11 夹具/DoD-2 的可达性表述不完全一致。
- anomaly: 无阶段协议异常；M2 的 requirements Out of Scope 与 FR-001 的张力按「FR-001 为显式交付、Out of Scope 为旧措辞」处理，驱动在 implement 前决定是否做 re-baseline。

## 2. Temporary Goal progress

| criterion | degree | evidence_ptr |
|---|---|---|
| 每份正式文档带配套架构图或具名豁免；缺失/失步被既有验证步骤确定性报出 | not_evaluated | analyze pass；无实现证据 |
| 配套义务写入 `create-docs` / `improve-docs` 既有步骤，不新增命令/分类 | not_evaluated | analyze pass；无实现证据 |
| 绘图能力只经 `draw-diagram` 前门复用，不新增引擎/路由/交付契约 | not_evaluated | analyze pass；无实现证据 |
| 存量文档渐进收敛，框架源与镜像一致 | not_evaluated | analyze pass；无实现证据 |

## 3. Team configuration review

- evidence: `test-evidence/analyze-stage-status.jsonl`；temp team active（`54fb818e`），尚无 team run report / wp-report
- symptom: `n/a (no run report yet)`
- proposal: `none`
- ratification: `n/a`
- applied: `no`

## 4. Next stage concurrency / roster

- requested: `24`; effective: `1`; reason: `single-package + segmented-dispatch + verifier-reserve`（implement 按 ≤16 任务/段串行派发；每段一个写执行者）
- stage max_parallel: `1`; verifier reserve: `1`
- roster: `sdd-implement-executor`（按段串行；U4 由驱动独立校验；baseline 槽位由驱动在 implement 起点执行一次）
- baseline slot: `planned` — `run-tests.sh --names-out <spec>/baseline-failed.txt`，全量一次，E2 行写状态脊
