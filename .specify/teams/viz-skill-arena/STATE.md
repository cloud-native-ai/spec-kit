# STATE（viz-skill-arena）

> 跨 cycle 记忆：最近结论、采纳记录、待办。supervisor 每 cycle 更新。

## Team
- slug: viz-skill-arena
- pattern: continuous | maturity: L2 | cadence: on-demand（用户下发任务触发）
- skills: 5（draw-d3js / draw-echarts / draw-excalidraw / draw-mermaid / draw-plantuml）— cycle 3 起扩展为五技能

## Last cycle
- **Date**: 2026-09-15T09:00:00Z
- **Cycle**: 4（语义/语法分离架构首循环）
- **Task**: 复刻三区域部署拓扑图（SDS 驱动：语义层产几何+weight_plan，5 语法层并行实现）
- **Champion**: draw-d3js
- **R2 weighted scores (2-judge avg)**:
  - draw-d3js: 0.95 ★冠军
  - draw-echarts: 0.92
  - draw-excalidraw: 0.89
  - draw-plantuml: 0.81
  - draw-mermaid: 0.59（无重绘，Phase A 基线）
- **采纳门 (≥0.85)**: d3js / echarts / excalidraw 通过；plantuml 未达冠军线但无回退通过故采纳；mermaid 无重绘 → 不采纳
- **无回退门**: d3js +0.004 / echarts +0.004 / excalidraw +0.006 / plantuml +0.062 PASS；mermaid N/A（无重绘）
- **采纳技能**: d3js / echarts / excalidraw / plantuml（references/cycle4-improvements.md dated record）+ draw-diagram（semantic-model.md 增 auto_layout_intent）；mermaid 工作副本变更未合并
- **关键发现**: 分离契约成立——绝对坐标三引擎零/近零偏离且 readback QA 使零偏离可验证；自动布局引擎量化声明偏离（plantuml |dx| 217→39.5px 全在界内）；SDS auto_layout_intent 使自动布局降级可检查

## 结论账本索引（需求类型 → 技能）
- Kubernetes 系统架构图（含组件/部署/序列图）→ **draw-plantuml**（cycle 1-2）
- 部署拓扑图/架构复刻图（多区域等高分区 + 组件散点布局 + hub-spoke 连线 + 单色精确复现）→ **draw-d3js**（cycle 3；替代：echarts=交互式HTML，excalidraw=可编辑白板）
- 全量结论见 `.specify/memory/knowledge/visualization-skill-selection.md`

## 技能采纳记录
- draw-d3js: 已采纳（2026-08-07T16:30:00Z cycle 2，无回退门通过且有变更）
- draw-echarts: 已采纳（2026-08-07T16:30:00Z cycle 2，无回退门通过且有变更）
- draw-mermaid: 已采纳（2026-08-07T16:30:00Z cycle 2，无回退门通过且有变更）
- draw-plantuml: 已采纳（2026-08-07T16:30:00Z cycle 2，冠军 + 无回退门通过）
- draw-d3js: 已采纳（2026-08-07T18:30:00Z cycle 2，无回退门通过且有变更）
- draw-echarts: 已采纳（2026-08-07T18:30:00Z cycle 2，无回退门通过且有变更）
- draw-plantuml: 已采纳（2026-08-07T18:30:00Z cycle 2，冠军 + 无回退门通过）
- draw-d3js: 已采纳（2026-09-15T02:30:00Z cycle 3，冠军 + 无回退门通过）
- draw-echarts: 已采纳（2026-09-15T02:30:00Z cycle 3，无回退门通过，+0.10 最大提升）
- draw-excalidraw: 已采纳（2026-09-15T02:30:00Z cycle 3，首次参赛，无回退门通过）
- draw-mermaid: 已采纳（2026-09-15T02:30:00Z cycle 3，无回退门通过）
- draw-plantuml: 已采纳（2026-09-15T02:30:00Z cycle 3，无回退门通过）
- draw-d3js: 已采纳（2026-09-15T09:00:00Z cycle 4，冠军 + 无回退 PASS；SDS-YAML 单一几何源 + QA 链）
- draw-echarts: 已采纳（2026-09-15T09:00:00Z cycle 4，无回退 PASS；readback-qa 像素验证）
- draw-excalidraw: 已采纳（2026-09-15T09:00:00Z cycle 4，无回退 PASS；roundness 12px + 实测读回 manifest）
- draw-plantuml: 已采纳（2026-09-15T09:00:00Z cycle 4，无回退 PASS；等高分区脚手架 + 量化偏离）
- draw-diagram: 已采纳（2026-09-15T09:00:00Z cycle 4，语义层 auto_layout_intent schema）
- draw-mermaid: 未采纳（2026-09-15T09:00:00Z cycle 4，无重绘 → 变更未验证）

## 待办 / 已知问题
- excalidraw 共享渲染服务 (127.0.0.1:8383) 持续 HTTP 500（page.waitForFunction timeout），cycle 3 两次均 fallback 到 local 模式；需排查或重建共享服务
- mermaid.ink 服务端不支持 sans-serif fontFamily，cycle 3 redraw 使用本地 vendored mermaid 11.12.2 bundle 渲染；远端优先策略在此场景下受限
- plantuml render-plantuml.sh 的 strip_style 会删除 flat skinparam ArrowThickness 行并注入 2，需用 !define macro 绕过（cycle 3 已验证有效）

## Post-Run Critique
- cycle 2 复盘（2026-08-07T16:30:00Z）：Phase C 技能工作副本写入与加载闭环已修复（.specify/teams/.work/viz-skill-arena/skills-work/），四个技能变更全部经无回退门采纳并合并回 canonical；R2 四技能加权分全部较 R1 提升（mermaid 0.73→0.87、plantuml 0.86→0.90、echarts 0.70→0.76、d3js 0.73→0.79），证明优化闭环有效。
- cycle 2 复盘（2026-08-07T18:30:00Z）：本轮 Phase C 技能工作副本写入与加载闭环生效，四技能重绘均加载工作副本；R2 中 plantuml/echarts/d3js 无回退且加权分 ≥0.85（plantuml 0.82→0.87 显著提升），其技能变更已合并回 canonical 并同步镜像；mermaid 重绘回退（0.79→0.74，无回退=false），变更未采纳，留待下轮观察。
- cycle 3 复盘（2026-09-15T02:30:00Z）：首次五技能竞技（新增 draw-excalidraw）。ALL 5 无回退门通过（历史首次全员通过），echarts 提升最大（+0.10）。冠军 d3js（0.95）凭借像素级绝对坐标复现胜出；excalidraw 首赛即达 0.94（与 echarts 并列第二），证明手绘引擎在 roughness:0 下可胜任精确复刻。mermaid 仍为最弱（0.755），等高分区问题经 ghost-spacer 脚手架改善但未根治（自动布局引擎固有限制）。Phase C 改进文件（CYCLE3-IMPROVEMENTS.md）作为 reference 合并至 canonical，未直接修改 SKILL.md 主体——下轮可考虑将通用规则提升为 SKILL.md 正式条目。
- cycle 4 复盘（2026-09-15T09:00:00Z）：语义/语法分离架构首次成立——SDS 成为唯一语义源（裁判对 SDS 判覆盖），偏离声明机制使自动布局降级可检查（plantuml |dx| 217→39.5px、7 项全在界内），readback QA 链把"零偏离"从声明变为证据（建议下轮提升为语法层必备项）。mermaid 重绘被人工中断拒绝，按规则其变更本轮不采纳；其改进单（ghost-chain 共秩 + 边直线化）已写好待下轮验证。T-tier 术语曾出现并行会话与本次重构的双写冲突（T3/T4 语义），已统一为 T3=数据流/T4=注释并以 5 个语法层 tier 映射为准。
