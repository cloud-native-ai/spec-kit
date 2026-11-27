# Mermaid 官方能力总览（00）

> Mermaid 是一个基于 JavaScript 的图表渲染库：用类 Markdown 文本定义图表，浏览器/CLI/服务器渲染为 SVG/PNG。本技能以「复刻 PlantUML 图表能力」为目标组织用法。

## 1. 图表类型全景（v11）

| 分类 | 类型 |
|------|------|
| 流程图 | flowchart（含 subgraph、样式类、交互） |
| UML | sequenceDiagram、classDiagram、stateDiagram-v2、erDiagram |
| 项目/计划 | gantt、journey、timeline、kanban（实验） |
| 架构 | C4Context、C4Container、C4Component、C4Dynamic、C4Deployment、architecture（实验）、block（实验） |
| 数据 | pie、quadrantChart、xychart-beta、sankey-beta、packet-beta |
| 需求/版本 | requirementDiagram、gitGraph |
| 树 | mindmap |

## 2. 与 PlantUML 的对照起点

- 原生匹配：classDiagram / sequenceDiagram / stateDiagram-v2 / erDiagram / gantt / mindmap / C4 系列；
- 语义映射：activity→flowchart、WBS→mindmap、usecase/component/deployment/package/object→flowchart 或 classDiagram 近似；
- 无匹配：timing（xychart 近似不等效）、composite/profile/archimate/ditaa/ebnf/regex——向用户说明。
- 完整对照表见 SKILL.md「PlantUML ↔ Mermaid 图表类型对照」与 howto/01。

## 3. 渲染方式

| 方式 | 用途 |
|------|------|
| 浏览器（本地 mermaid.js bundle） | 网页内嵌 |
| mermaid-cli（mmdc） | 本地渲染 SVG/PNG/PDF（需 Chrome） |
| 服务器后端（mermaid.ink 兼容协议） | URL 即渲染（本技能默认后端：内网共享服务） |
| 编辑器插件（VS Code Markdown Preview Mermaid） | 预览调试 |

## 4. 本技能使用的工具链

- 渲染：`scripts/render-mermaid.sh`（服务器后端（mermaid.ink 兼容）+ 本地 mmdc）；
- 量测：`scripts/measure-svg-layout.py`（WBS/甘特版面三判据）；
- 兜底：`scripts/svg-to-png-cjk.cjs`（SVG→PNG，CJK 字体与内容裁剪）；
