# Routing Matrix & Exclusivity Registry（draw-diagram 前门路由权威）

> 证据源：竞技场结论账本 `${SKILL_WORKDIR}/.specify/memory/knowledge/visualization-skill-selection.md`
> （viz-skill-arena 各轮 cycle 的冠军与匹配结论）。本文件只登记**路由判据**；引擎语法与渲染细节归各 draw-* 技能。

## 1. 独占登记（Exclusivity Registry —— 只有一家能画）

命中即定引擎，跳过比较：

| 图种 / 产物诉求 | 唯一引擎 | 独占理由 |
|----------------|---------|---------|
| WBS、甘特图、Salt UI 线框图、JSON 可视化、YAML 显示效果图、ER 实体关系（crow's foot） | **draw-plantuml** | 原生 `@start` 族标签与 entity 语法，其余引擎无等价表达 |
| 可编辑白板产物（`.excalidraw` 拖回继续编辑）、手绘美学、mermaid→手绘桥接 | **draw-excalidraw** | 场景 JSON 是唯一可继续编辑的白板源文件 |
| ECharts 仪表板嵌入、标准数据系列图且要 toolbox/联动交互 | **draw-echarts** | ECharts 生态与系列目录原生支持 |
| 既有图像的像素级复刻、超出目录的 bespoke D3 交互 | **draw-d3js** | 绝对坐标 SVG 控制，无布局引擎干预 |
| 仓库原生声明式文本图（GitHub/CI 免工具链直渲、diff 友好） | **draw-mermaid** | 平台原生 mermaid 渲染，文本即产物 |

## 2. 图类矩阵（默认引擎 + 替代切换）

| 图类 / 意图 | 默认引擎 | 替代（artifact_intent 命中即切换） | 证据 |
|------------|---------|----------------------------------|------|
| 部署/架构拓扑**复刻**（像素级、散点布局、等高分区、单色） | **draw-d3js** | echarts（interactive-html）、excalidraw（editable-whiteboard） | cycle 3 冠军 R2 0.95 |
| UML 语义架构图（component/deployment/sequence/class/package） | **draw-plantuml** | d3js（仅复刻形态） | cycle 1-2 冠军 |
| 自由版面架构/拓扑**新建**（要可继续编辑） | **draw-excalidraw** | d3js（像素自定义）、plantuml（UML 严格） | cycle 3 R2 0.94 |
| 流程图 / 状态机 / 简单时序（text-first、进仓库维护） | **draw-mermaid** | plantuml（UML 严格语义） | 可维护性优先 |
| 数据可视化（柱/线/饼/散点/力导向/树图/热力） | **draw-echarts** | d3js（bespoke 交互） | 系列目录覆盖 |
| 思维导图 | **draw-plantuml**（原生） | mermaid（repo-text）、excalidraw（editable） | 三引擎皆可，按产物形态 |

## 3. Tie-break 顺序（artifact_intent 优先）

1. `editable-whiteboard` → draw-excalidraw
2. `interactive-dashboard` → draw-echarts
3. `repo-text` → draw-mermaid
4. `pixel-reproduction` → draw-d3js
5. `uml-strict` / `static-embed` → draw-plantuml

并列仍不可决 → 一轮 AskUserQuestion（≤4 问）附推荐项；推荐项 = 矩阵默认引擎。

## 4. 反路由红线（MUST NOT）

- 不得因"某引擎也会画"而绕过独占登记（如用 mermaid 画甘特替代 plantuml 原生甘特）
- 不得把复刻请求路由到自动布局引擎（mermaid/plantuml）——等高分区与散点版面会被布局算法改写（cycle 3 证据：mermaid 0.755）
- 不得为凑"全面性"让下层技能承接非其独特的图种；路由责任在前门
