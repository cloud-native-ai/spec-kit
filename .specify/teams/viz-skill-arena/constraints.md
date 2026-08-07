# 约束文件（viz-skill-arena）

> 每 cycle 开始时读取。kill-switch / 预算 / 范围是硬约束，违反即停。

## Kill-switch

- `loop-pause-all`：设置本值即暂停全部后续 cycle（halt），直到人工清除。

## 范围（允许做什么）

- **允许改**：四个技能 canonical 目录（`skills/draw-d3js`、`skills/draw-echarts`、`skills/draw-mermaid`、`skills/draw-plantuml`，含 SKILL.md/references/scripts）——仅在 R2 接受（无回退）后由 supervisor 合并；结论账本 `.specify/memory/knowledge/visualization-skill-selection.md`。
- **允许读**：四个技能的 canonical/.specify/.qoder 副本、用户任务上下文、STATE 与历史 run report。
- **运行中间件**：一律在 `.specify/teams/.work/viz-skill-arena/`（git-ignored）。

## 禁止（MUST NOT）

- 不得手改被评图表（score = f(target) 不变式）：被评图必须由最新技能 target 重生成；
- 不得直接编辑 `.specify/skills/`、`.qoder/skills/` 镜像副本（由 sync-mirrors.py --write 与显式副本同步产生）；
- 不得在 canonical 技能里写入未通过 R2 无回退门的变更；
- 不得修改其他团队目录（`.specify/teams/other-slug/**`）；
- 不得修改 `templates/`、`agents/`、`src/` 等非本团队领地；
- 无回退门：某技能重绘加权分 < R1 自身分 → 该技能本轮变更作废（保留结论，不合并）。

## 质量维度（Σ = 1.0）

| 维度 | 权重 | 含义 |
|------|------|------|
| semantic-fidelity | 0.30 | 语义正确/信息保真（不臆造、忠实源结构） |
| visual-quality | 0.30 | 视觉美观/排版清晰/对齐配色 |
| requirement-fit | 0.25 | 需求契合/表达适切 |
| reproducibility | 0.15 | 可复现/可维护（源文件清晰、可重渲） |

- 冠军采纳线：R2 加权分 ≥ 0.85；
- 预算：max_cycles_per_day 3；tokens 80% → report-only，100% → halt。
