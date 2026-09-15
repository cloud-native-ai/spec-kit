---
name: draw-excalidraw
description: |
  Draw hand-drawn-style diagrams with Excalidraw scene JSON, render to SVG/PNG via a self-hosted Excalidraw render service, and output as HTML with rendered images.
  Excalidraw 是手绘风格（白板风）绘图：架构图、流程图、拓扑图、思维导图、时序示意、ER 图等自由画布图表；标准流程图/时序图/类图也可走 Mermaid 桥接自动布局。
  Use when the user mentions "excalidraw", "手绘风格图", "手绘图", "手绘风", "白板图", "白板", "手绘架构图", "手绘流程图", "sketch style diagram", "hand-drawn diagram", "whiteboard diagram",
  "画个手绘风格的", "用 excalidraw 画", "excalidraw 场景", ".excalidraw 文件", "mermaid 转手绘", "mermaid 转 excalidraw", "生成 excalidraw", "excalidraw 渲染", "excalidraw 出图"
skill_id: "<SKILL:.specify/skills/draw-excalidraw/SKILL.md>"
---

# 手绘风格图表绘制技能（Excalidraw）

使用 Excalidraw 场景 JSON（`.excalidraw` 明文格式）绘制手绘风格图表，通过**自部署的 Excalidraw 渲染服务**渲染为 SVG/PNG，并输出为包含渲染图表和说明文字的完整 HTML 文档。与 draw-plantuml 同构：源文件 → 远端渲染服务 → SVG/PNG → HTML。

## 核心原则

- **自由画布 = 坐标自负**：Excalidraw 没有自动布局引擎，每个元素的 `x/y/width/height` 都由本技能计算——先规划网格再落坐标，宁可稀疏不可拥挤
- **两条生成路径，按图选型**：标准结构图（流程图/时序/类/ER/状态）优先走 **Mermaid 桥接**（布局自动、成功率最高）；自由布局图（架构图/拓扑/脑图/版面自定义）走**场景 JSON 直出**
- **远端渲染优先**：默认只使用渲染服务（`render-excalidraw.sh` 默认 `EXCALIDRAW_BACKEND=server`）；服务不可用时必须先询问用户（修正 `EXCALIDRAW_SERVER` 地址，或经确认后以 `EXCALIDRAW_BACKEND=local` 本机临时起服务），**未获用户确认不得静默切换**
- **渲染后必回看**：读取渲染出的 PNG 与用户要求比对（重叠/错位/溢出/漏元素），发现问题改场景 JSON 重渲——坐标是算出来的，必须用眼睛验收
- **手绘美学**：`roughness: 1`、Excalidraw 标准色板、容器圆角、箭头微弯——不要画成僵硬的 CAD 图

## 工作流

按以下 7 个步骤顺序执行：

### Step 1: 语义解析 + 吃透上下文

分析用户输入理解绘制意图；必要时用 `AskUserQuestion` 确认（最多一轮 ≤4 问）。面对文档/代码等丰富上下文，先产出带出处的上下文摘要（组件、关系、核心流程），后续绘图对着它，不臆造。

→ [00-semantic-analysis.md](references/howto/00-semantic-analysis.md)

### Step 2: 选图类型 + 选生成路径

从图表类型决定生成路径：

| 场景 | 路径 | 依据 |
|------|------|------|
| 流程图、时序图、类图、ER 图、状态图、甘特 | **Mermaid 桥接** | 官方转换器自动布局+文本绑定，LLM 写 Mermaid 成功率高 |
| 架构图、拓扑图、思维导图、分区/分层示意、任何需要自定义版面的图 | **场景 JSON 直出** | Mermaid 表达不了自由版面 |

→ [01-path-selection.md](references/howto/01-path-selection.md)

### Step 3: 布局规划（场景 JSON 路径必做）

编码前先在"纸面"规划空间语义：网格（列宽/行高/间距）、角色位置（枢纽居中、上下游左右/上下排布）、分组框选（frame 或大矩形背景）、连线路径（正交优先、避免穿元素）。文本宽度按估算公式预留（CJK ≈ fontSize×字数，ASCII ≈ fontSize×0.6×字数）。

→ [02-layout-planning.md](references/howto/02-layout-planning.md)

### Step 4: 生成场景 JSON / Mermaid 代码

场景 JSON 路径：按元素规范写 `.excalidraw` 文件——先容器后文本再箭头；文本优先用**容器绑定**（`containerId`，渲染服务会自动按真实字体度量重算尺寸并居中）；箭头写全两端 binding。Mermaid 路径：写标准 Mermaid 语法即可。

→ [03-scene-json-generation.md](references/howto/03-scene-json-generation.md)、[scene-schema-reference.md](references/guide/scene-schema-reference.md)

### Step 5: 渲染

用 [render-excalidraw.sh](scripts/render-excalidraw.sh) 渲染，同时产出 PNG 与 SVG（默认远端：`EXCALIDRAW_BACKEND=server` + `EXCALIDRAW_SERVER`；服务不可达时脚本给出指引，须先询问用户）。Mermaid 桥接路径先把 Mermaid 转成场景（`/mermaid-to-scene`）存为 `.excalidraw`，再走同一渲染脚本——保证两条路径交付物一致且源文件可编辑。

→ [04-rendering-and-output.md](references/howto/04-rendering-and-output.md)

### Step 6: 回看比对与微调

读取渲染 PNG 检查：元素齐全？文本溢出容器？箭头穿元素？布局失衡？发现问题回到 Step 3/4 调整坐标/尺寸/文案后重渲，直到满意。Mermaid 路径不满意版面时，可转为场景 JSON 路径手动微调（转换结果就是可编辑场景）。

### Step 7: 组装 HTML 输出

按输出要求组装 HTML（渲染图为主体，场景 JSON 源码放可折叠「复现性附录」）。HTML 由 Agent 组装，渲染脚本只产 PNG/SVG。

→ [04-rendering-and-output.md §HTML 组装](references/howto/04-rendering-and-output.md)

## 输出要求

- 输出为单个 HTML 文档：渲染图为主体；原始场景 JSON 不嵌入正文，仅放入可折叠「复现性附录」`<details>` 块（默认收起），附录内容必须与磁盘实际渲染的 `.excalidraw` 逐字节一致
- 图表通过 [render-excalidraw.sh](scripts/render-excalidraw.sh) 渲染，同时产出 PNG 与 SVG
- **默认优先选用 PNG** 引用/嵌入图片；仅当图表过大需无损缩放时用 SVG
- **嵌入 Markdown 文档时**：PNG 与 SVG 引用须用同一机制——首选全内联 HTML（`<a href=x.svg target=_blank rel=noopener><img src=x.png></a>`），渲染器剥 HTML 时回退全纯 Markdown
- PNG/SVG 与 HTML 同目录，HTML 相对路径引用图片
- `.excalidraw` 源文件必须保存（用户可直接拖入 excalidraw.com 或自部署白板继续编辑）
- 每张图至少包含标题、渲染图片和简要说明

## 渲染服务部署

渲染服务（[scripts/server/](scripts/server/)）是本技能的配套后端，部署方式（本机 Node 直跑 / Docker / 远端服务器）与 API 详见 [server-deployment.md](references/guide/server-deployment.md)。首次使用且服务未部署时，先读该文档与用户确认部署方式。

## 参考文档

完整索引见 [references/index.md](references/index.md)。

**实战沉淀（务必阅读）**：[best-practices/best-practices.md](best-practices/best-practices.md)（最佳实践）与 [best-practices/pitfalls.md](best-practices/pitfalls.md)（陷阱）——绘制前对照最佳实践，绘制后自查陷阱清单。
