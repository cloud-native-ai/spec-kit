# Checkpoint 01 — requirements

## 1. Artifact verification

- sentinel: `REQUIREMENTS-DONE`（本地原生调用最后一非空行；本拓扑无 watcher 日志）
- U4: `pass` — 独立校验证据：
  - `validate-requirements.py`：`status: ok`，六面 pass，0 error / 0 warning，exit 0
  - `pre-analyze-check.py --stage requirements`：`decision=pass errors=0 advisories=0`，23 FR / 10 SC，exit 0
  - `flow-class-check.py --action lookup`：`flow_class=execution` / `flow_type=-` / `source=declaration`，exit 0
  - `decomposition-check.py --mode plan`：`decision=proceed`（23 FR ≤ 60），exit 0
- artifacts:
  - `.specify/specs/087-arch-diagram-docs/requirements.md`（272 行，23 FR / 10 SC，含 `### Runtime Stack & Dependency Ownership`）
  - `.specify/specs/087-arch-diagram-docs/checklists/requirements.md`
  - commits `779f1a9b`（初稿）→ `ac1ed706`（补运行时栈表，修复 pre-analyze exit 2）
  - `.specify/specs/087-arch-diagram-docs/test-evidence/requirements-loop-state.json`（loop-state 快照）
- loop-state 快照：`loop_state=UNKNOWN` / `artifacts-without-completion`。原因：本地原生拓扑没有 `log-<line>-<stage>.log`，引擎看不到原生子代理返回的末行哨兵；按 checkpoint 协议，U4 判定与哨兵仍是完成权威。spine schema 已为 `v1`、必需字段齐全、`missing_fields=[]`。
- anomaly: `未发现异常`（一次 gate fail 已在 attempt 2 修复：缺 `§ Runtime Stack & Dependency Ownership` → pre-analyze exit 2 → 补表后 exit 0）

## 2. Temporary Goal progress

goal: `.specify/specs/087-arch-diagram-docs/goal/087-arch-diagram-docs/goal.md`（status=active；requirements U4 后创建）

| criterion | degree | evidence_ptr |
|---|---|---|
| 每份经文档流程新建/改进的正式文档带配套架构图或具名豁免；缺失/失步被既有验证步骤确定性报出 | not_evaluated | `requirements.md` FR-004/FR-006/FR-014；本阶段仅为规格定义，尚无运行测量 |
| 配套义务写入 `create-docs` / `improve-docs` 既有步骤与收尾判定，不新增命令/分类 | not_evaluated | `requirements.md` FR-017/FR-018；本阶段仅为规格定义 |
| 绘图能力只经 `draw-diagram` 前门复用，不新增引擎/路由/交付契约 | not_evaluated | `requirements.md` FR-011/FR-012/FR-013；`### Runtime Stack & Dependency Ownership` RS-003/RS-004 |
| 存量文档渐进收敛，框架源与镜像一致 | not_evaluated | `requirements.md` A6 / Out of Scope；本阶段无实现证据 |

说明：requirements 阶段尚无实现或运行证据，按 checkpoint 协议记 `not_evaluated`，不以 0 或估计百分比替代。

## 3. Team configuration review

- evidence: `n/a` — 临时 Team 按 085 流程在 clarify + plan U4 后创建；本 checkpoint 时尚无 `team/`、`wp-report.py` 或 team run report
- symptom: `n/a (temporary team not created yet)`
- proposal: `none`
- ratification: `n/a`
- applied: `no`

## 4. Next stage concurrency / roster

- requested: `24`; effective: `1`; reason: `single-package-stage`（clarify 只有一个有界分析包；并发收益测试不成立）
- stage max_parallel: `1`; verifier reserve: `1`
- roster: `sdd-clarify-analyzer`（单席；U4 由驱动独立校验）
