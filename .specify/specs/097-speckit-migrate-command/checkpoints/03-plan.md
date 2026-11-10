# Checkpoint 03 — plan（097-speckit-migrate-command）

- 哨兵 PLAN-DONE；U4 PASS
- 产物：`plan.md`、`research.md`、`data-model.md`、`contracts/migrate-cli.md`、`contracts/migrate-engine.md`、`contracts/migrate-template.md`、`quickstart.md`、`feature-ref.md`；Feature 024 `Draft → Planned`（`features.md` 行 + `features/024-*.md` 同步，requirements 阶段的 registry 待办恢复点关闭）
- 门禁：`validate-decision-tensions.py` status=ok（2 记录 / 0 error）；`pre-analyze-check.py --stage plan` decision=pass（0 error / 44 advisory，全部为计划内待创建路径或显式不存在路径：`.specify/version`（拒绝新增）、`.specify/templates/commands`（已退役）、`.specify/tools/`（被检测的旧态）、计划将创建的文件）；`decomposition-check.py --mode plan` decision=proceed（fr_count=25 / 上限 120）；plan 完整性：1 个 `# Implementation Plan:` 标题、无占位符残留、Requirement→Feature 戳存在
- 规划期基线（`test-evidence/plan-gates.txt`）：`regen-command-copies.py --check` exit 0；`sync-mirrors.py --check` exit 0；`anchor-layout-migrate.py --action check` 对全新 init 项目 clean exit 0；`specify init` 示例 exit 0 并产出 `.specify/source.json`；`specify migrate --help` exit 2（命令尚不存在，作为 quickstart 未执行声明的前提）
- 决策张力：T-001（init 参照树整体投影 vs 逐文件重写比较）、T-002（框架源工作区委托既有检查器 vs 统一参照树）
- 并发读数：requested=8 effective=1 effective_reason=`dependency-edge`（研究派发 → 设计定稿 → 工件撰写 → 复核派发 的 dispatch 区间互不重叠；证据：research 子代理完成后才写契约，复核子代理在全部工件落盘后派发）
- 方向审计：on-track（未扩张范围；未改 install/init 职责；未吸收 sanitize 周期治理；未吸收 goal/team 迁移）
- 5b：n/a
