---
name: draw-plantuml
description: |
  Draw system architecture diagrams with PlantUML, render to SVG/PNG via PlantUML server, and output as HTML with rendered images.
  Use standard UML semantics (Component, Deployment, Sequence, Class/Package) to describe system architecture.
  Use when the user mentions "架构图", "architecture diagram", "UML图", "plantuml", "系统架构图", "画架构", "设计图", "组件图", "部署图", "时序图", "类图", "包图", "系统设计",
  "流程图", "状态图", "活动图", "用例图", "状态机图", "模块图", "交互图",
  "sequence diagram", "class diagram", "component diagram", "deployment diagram",
  "activity diagram", "state diagram", "use case diagram", "package diagram",
  "复刻图", "图片重绘", "图片转UML", "replicate diagram", "redraw", "image to UML"
skill_id: "<SKILL:.specify/skills/draw-plantuml/SKILL.md>"
---

# 架构图绘制技能

使用 PlantUML 语法和标准 UML 语义绘制系统架构图，通过 PlantUML 服务器渲染为 SVG/PNG，并输出为包含渲染图表和说明文字的完整 HTML 文档。

## 核心原则

### 1. UML 语义，而非随意方框
每张图必须遵循标准 UML 图表类型。避免临时性的"方框和箭头"——使用正确的 UML 元素（组件、节点、生命线、类）和正确的关系（依赖、关联、实现等）。

### 2. 架构优先的叙事
Markdown 文字应该讲述一个故事：从系统上下文开始，然后深入到组件及其交互。图和文字互补——文字解释*为什么*，图展示*什么*。

### 3. PlantUML 最佳实践
关于 PlantUML 特定的约定（语法、样式、元素类型、关系表示法），参见 [plantuml-guide.md](references/plantuml-guide.md)。关于布局优化、内容组织和协作规范，参见 [plantuml-best-practices.md](references/plantuml-best-practices.md)。关键原则：使用 `skinparam` 保持统一样式，每张图核心元素 ≤7 个（硬上限 ≤15），通过方向关键字和分组控制布局，使用有意义的标签。

## 工作流

本技能基于已有信息（用户描述、代码、文档、图片）绘制 UML 图并添加相应的文字说明。按以下步骤顺序执行——**Step 0（语义分析）必须在选择图表类型之前执行**。

### Step 0: 语义分析与意图理解

**必须**先分析用户输入以理解绘制意图，再选择图表类型。详细方法参见 [00-semantic-analysis.md](references/howto/00-semantic-analysis.md)。

#### 0.1 意图分类

识别输入类型：

| 意图类型 | 检测信号 | 处理方式 |
|---------|---------|---------|
| **直接描述型** | 用户提供清晰的系统/组件/流程文字描述 | 直接提取元素和关系 |
| **图片复刻型** | 用户引用图片文件（"复刻***.jpg"、"重绘***.png"、"replicate this image"） | 读取并分析图片，提取视觉元素 |
| **模糊/不完整型** | 描述简短、不清晰或缺少关键细节（如"画个系统图"） | 识别信息缺口，提出澄清问题 |
| **代码可视化型** | 用户提供源代码要求可视化 | 分析代码结构，提取类/模块/流程 |

#### 0.2 提取绘制内容

根据意图类型，提取：
- **系统边界**：系统内部 vs. 外部
- **核心元素**：组件、角色、类、节点、状态
- **关系**：依赖、消息、状态转换、关联
- **范围**：单图 vs. 多图（C4 层级）

对于**图片复刻**请求，**必须**使用 `Read` 工具读取引用的图片文件，提取：图表类型、元素、关系、布局和分组结构。

#### 0.3 差距分析与交互式确认

如果任何必需信息缺失或不明确，**必须**使用 `AskUserQuestion` 在进入 Step 1 之前进行澄清。需要检查的关键缺口：

- [ ] 系统范围和边界是否明确定义？
- [ ] 所有关键元素是否已识别？
- [ ] 元素间的关系是否清晰？
- [ ] 图表目的是否明确（架构总览 vs. 详细交互）？
- [ ] 详细程度是否合适（草图 vs. 蓝图）？

发现缺口时，最多提问**一轮**（≤4 个问题）。确认后输出简短的意图摘要，然后进入 Step 1。

**只有当绘制意图完全明确时才进入 Step 1**——无论是来自用户的原始描述还是交互式澄清后。

### Step 1: 选择图表类型

**必须**先阅读 [01-choose-diagram-type.md](references/howto/01-choose-diagram-type.md) 以确定合适的 UML 图表类型。

根据用户描述，识别他们想表达的内容并匹配到正确的图表：

- 使用**快速匹配表**将用户关键词映射到图表类型
- 使用**按开发阶段推荐**表（如果用户提到特定阶段）
- 使用**选择决策流程**区分结构图 vs. 行为图

如果需要表达多个方面，选择多种图表类型——每张图聚焦一个视角。

### Step 2: 遵循操作指南

确定图表类型后，**必须**阅读并遵循对应的操作指南获取详细绘制说明：

| 图表类型 | 操作指南 |
|---------|---------|
| 类图 (Class Diagram) | [02-class-diagram.md](references/howto/02-class-diagram.md) |
| 包图 (Package Diagram) | [06-package-diagram.md](references/howto/06-package-diagram.md) |
| 组件图 (Component Diagram) | [03-component-diagram.md](references/howto/03-component-diagram.md) |
| 部署图 (Deployment Diagram) | [04-deployment-diagram.md](references/howto/04-deployment-diagram.md) |
| 时序图 (Sequence Diagram) | [05-sequence-diagram.md](references/howto/05-sequence-diagram.md) |
| 用例图 (Use Case Diagram) | [07-usecase-diagram.md](references/howto/07-usecase-diagram.md) |
| 活动图 (Activity Diagram) | [08-activity-diagram.md](references/howto/08-activity-diagram.md) |
| 状态机图 (State Machine Diagram) | [09-state-machine-diagram.md](references/howto/09-state-machine-diagram.md) |

每个操作指南提供：
- **关键元素**：UML 元素及其 PlantUML 语法
- **完整示例**：可运行的 PlantUML 代码块
- **建模步骤**：构建图表的分步说明
- **最佳实践**：常见模式和陷阱

额外的 PlantUML 语法细节也可参考 [plantuml-guide.md](references/plantuml-guide.md)。

### Step 3: 语义布局规划

在编写 PlantUML 代码之前，分析组件间的语义关系以确定它们的自然位置。这通过预先建立基于语义的空间排列来防止布局问题。

#### 3.1 识别组件角色

对每个组件进行分类：

| 角色 | 说明 | 典型位置 |
|------|------|---------|
| **Hub（中心端）** | 多个其他组件连接的核心组件 | 中上方 |
| **Edge（节点端）** | 以 1:many 模式连接到中心的组件 | 中心下方 |
| **Peer（对等端）** | 同级、功能相似的组件 | 并排（`together {}`） |
| **Entry（入口）** | 外部访问点 | 左侧或顶部 |
| **Sink（汇聚端）** | 数据终点、存储、外部服务 | 右侧或底部 |
| **External（外部）** | 系统边界之外 | 主框架外侧 |

#### 3.2 关系映射到布局

| 关系模式 | 布局规则 | PlantUML 技术 |
|---------|---------|--------------|
| **1:many（中心-辐射）** | 中心在上，节点在下 | Hub 放入上层 frame，Edge 放入下层 frame |
| **对等（同级）** | 并排 | `together {}` 块 |
| **链式** | 按流向排列 | 默认箭头 `-->` |
| **层次** | 父在上子在下 | 嵌套容器 |

#### 3.3 绘制位置草图

在编写代码之前先画一个粗略的位置草图。Kubernetes 示例：

```
[External: Users] → [Entry: Ingress → Service]
                              ↓ ClusterIP
[Hub: Control Plane]   [Edge: Node 1]  [Edge: Node 2]  → [Sink: PV]
(Sched, CM → API → etcd) (kubelet, Pod)  (kubelet, Pod)
                              ↓ pull
                       [Sink: Registry]
```

位置草图决定：布局方向、元素声明顺序、`together{}` 分组和嵌套结构。

#### 3.4 多区域复杂布局图

对于包含多个分组区域、水平流向、角色和丰富注释的图表，应用以下技巧：

- **虚线边框分组区域**：使用 `rectangle "Zone Title" as zone_alias #line.dashed { ... }` 创建带虚线边框的视觉分区，将相关组件分组。
- **水平流向**：在图表顶部使用 `left to right direction` 实现从左到右的流向布局（常见于管道型、数据流型和 DevOps 架构图）。
- **角色外置声明**：在所有 `rectangle` 或容器块之外声明 `actor` 元素，使其作为独立的人形图标通过箭头连接到区域。
- **彩色强调文本**：当区域标题或组件名需要彩色文本（如红色强调）时，在标签内使用 PlantUML 标记如 `<color:red>text</color>` 或 `<font color=red>text</font>`。注意**必须省略** `skinparam monochrome true`（见 Step 5），否则颜色会被去除。
- **全面注释覆盖**：复刻参考图时，包含所有文字注释——缺失注释会显著降低正确性。使用 `note top/bottom/left/right of <element>` 添加多行说明文字，使用**箭头标签**（`: short text`）添加简短连线标注。计算源图注释数量并验证输出匹配。
- **反馈/回流箭头**：管道图通常有反馈循环（与主流向相反的箭头）。使用虚线箭头和描述性标签表示：`elementB ..> elementA : feedback label`。

#### 3.5 布局故障排除

实践中发现的常见布局陷阱：

- **`left to right direction` 模式下的方向箭头**：使用 `left to right direction` 时，主流向使用普通 `-->`（自动走右）。**不要**使用 `-right->`，因为它会被重新解释并可能导致垂直布局。垂直于主流向的连接使用 `.down.>` 和 `.up.>`（带方向提示的点线样式）。
- **角色与区域的交互**：当角色连接到虚线边框区域矩形**内部**的元素时，区域会扩展以视觉包含角色，导致布局变形。解决方案：
  - 将角色连接到区域容器本身（`developer ..> zone1`）而非内部元素
  - 或使用 `together {}` 单独分组角色，用 `.down.>` / `.up.>` 进行垂直定位
- **CJK 字体渲染**：PlantUML 服务器通常缺少 CJK 字体，导致中文字符零宽度渲染。包含中文文字的图表：
  - 使用配套脚本 `scripts/svg-to-png-cjk.cjs` 通过 Playwright 使用系统 CJK 字体渲染 PNG
  - 在纯 CJK 标签周围添加填充空格：`"  业务系统  "` 给服务器合理的宽度度量
  - 渲染管道：PlantUML 服务器 -> SVG -> 后处理（移除 textLength）-> Playwright -> PNG
- **`note over` 仅限时序图**：在组件/矩形图中，使用 `note top of X`、`note bottom of X`、`note right of X`、`note left of X` 替代 `note over X,Y`。
- **区域内的注释**：附加在区域内元素上的注释会导致区域扩展以容纳注释。当源布局显示区域内注释时，这通常是期望行为。需提前规划注释位置以匹配源图。
- **默认方向下的角色定位**：在默认（从上到下）方向中使用 `-right->` 实现水平流向时，角色通过 `.down.>` 和 `.up.>` 自然定位在管道上下方。这通常比 `left to right direction`（角色容易聚集）提供更好的角色分布。权衡：默认方向需要在每条主流箭头上显式使用 `-right->`。
- **嵌套 `rectangle` 中的 `together {}` 可能失效**：当 `together {}` 放在嵌套 `rectangle` 块内时可能不生效，元素无法对齐。将 `together {}` 移到 rectangle 容器外部。
- **LTR 模式下 `.down.>` 方向不可预测**：在 `left to right direction` 模式下，`.down.>` 可能产生右向或斜向箭头而非垂直向下。需测试实际效果或切换到默认方向模式进行垂直连接。
- **三方权衡**：对于同时需要区域边框 + 角色定位 + 完整注释的复杂图表，参见 [plantuml-engine-behaviors.md](references/plantuml-engine-behaviors.md)。当前最优策略（70/100）：默认方向 + 无区域边框 + actor→元素 + 完整注释。

### Step 4: 草拟 PlantUML 代码

基于操作指南和用户的系统信息：

1. 从用户描述中识别关键元素（参与者/节点/组件/类等）
2. 定义它们之间的关系（依赖、消息、状态转换等）
3. 编写 PlantUML 代码，用 `@startuml` / `@enduml` 包裹
4. 每张图聚焦单一主题：核心元素 ≤7 个（可接受 ≤12，硬上限 15）；过大则拆分为多张图
5. **应用布局最佳实践**：使用方向关键字（`-right->`、`-down->`），分组关联元素（`together{}`），先声明元素再声明关系
6. **标签精简（≤10 字符）并使用富文本注释补充细节**（适用于所有图类型的通用规则）：
   - 元素名称和关系标签不得超过 10 个字符——适用于所有 UML 图类型，无例外
   - 当短标签无法充分表达元素用途时，**必须**附加 `note` 元素补充详细说明
   - **注释位置**：`note right of <element>`、`note left of`、`note top of`、`note bottom of` 用于定位注释；`note "text" as N` + `N .. element` 用于浮动注释
   - **箭头标签**：箭头上保持 ≤10 字符（`: short text`）；更长描述使用 `note on link`
   - **多行注释**：使用 `note ... end note` 语法进行多段落说明
   - 详细的注释模式和示例参见 [plantuml-best-practices.md §2.5](references/plantuml-best-practices.md)

PlantUML 语法细节（元素类型、关系表示法、样式、模式）参考 [plantuml-guide.md](references/plantuml-guide.md)。该指南包含覆盖 7 种图表类型的**按图表类型的快速语法参考表**。

**还必须**遵循 [plantuml-best-practices.md](references/plantuml-best-practices.md)：
- 内容组织（§2）：单一职责、C4 分层拆分、**标签长度 ≤10 字符 + 富文本注释（§2.5）**、元素排序
- 布局优化（§1）：方向控制、隐藏连接、分组、间距
- 视觉高亮（§3）：注释放置模式、别名可读性、关键路径着色
- 按图表类型的布局指南（§5）：每种 UML 类型的推荐方向和布局重点

### Step 5: 应用标准样式

草拟 PlantUML 代码后，**必须**应用 [plantuml-style.md](references/plantuml-style.md) 中定义的标准样式配置。对每张图：

1. 在 `@startuml` 之后（图表内容之前）插入**基础样式块**：
   ```plantuml
   skinparam shadowing false
   skinparam roundCorner 20
   skinparam dpi 300
   scale 4
   skinparam defaultFontSize 14
   skinparam defaultFontName "Arial, Helvetica, sans-serif"
   skinparam padding 8
   skinparam ArrowThickness 2
   skinparam BorderThickness 2
   skinparam svgDimensionStyle false
   skinparam svgLinkTarget _blank
   ```
   **色彩模式选择**（在基础样式块之后添加以下之一）：
   - **单色图**（大多数技术文档的默认选择），添加：`skinparam monochrome true`
   - **需要彩色的图**（如红/蓝强调文本、彩色区域、品牌色），**完全省略** monochrome 设置。`skinparam monochrome true` 会将所有颜色转换为灰度，使 `<color:red>` 或 `<font color=red>` 等彩色文本不可见。

   仅**类图/组件图/部署图**还需要在第一行添加 `top to bottom direction`。时序图/活动图/状态图/用例图**不要**添加。
2. 如果图表包含 `actor` 元素或属于用例图，额外添加：
   ```plantuml
   skinparam actorStyle awesome
   ```
3. 验证位置：所有样式声明必须出现在 `@startuml` 之后、元素定义之前
4. 验证无冲突：确保图表正文中没有重复或覆盖的 `skinparam` 声明

**注意：** `.puml` 源文件统一使用 `scale 4 + dpi 300`（面向 SVG 最高质量）。PNG 渲染由 `render-plantuml.sh` 脚本**自动计算**合适的 scale/dpi 参数，确保 PNG 输出 ≤ 4095×4095（低于 PlantUML Server 硬上限 4096）。无需手动为 PNG 调整样式。

### Step 6: 编写配套文字

对每张图，准备以下说明内容（将包含在最终 HTML 中）：
1. **图表标题**（将成为 HTML 中的 H2/H3 标题）
2. **上下文**：1-2 句话说明此图代表什么以及为何选择此类型
3. **PlantUML 源代码**：保存为 `.puml` 文件供参考和渲染
4. **说明**：每个关键元素和关系的要点
5. **设计理由**：为何选择此结构/交互模式（如适用）

### Step 7: 渲染 PlantUML 为 SVG/PNG

草拟并完成所有 PlantUML 代码的样式后，使用渲染脚本将每张图渲染为 SVG（首选）和 PNG。

**渲染脚本：** [scripts/render-plantuml.sh](scripts/render-plantuml.sh)

该脚本实现 **SVG/PNG 双策略渲染**：
- **SVG**：始终使用 `scale 4 + dpi 300`（矢量格式，无尺寸限制，无损缩放）
- **PNG**：自适应计算 scale/dpi，确保输出 ≤ 4095×4095（低于 PlantUML Server 硬上限 4096）
  - 从 SVG viewBox 推算图表实际大小
  - 自动选择最大化质量且不超限的 scale + dpi 组合
  - 渲染后验证 PNG 非空白（文件大小合理性检查）
  - 若检测到空白输出，自动降级重试

**每张图的操作流程：**
```bash
bash ${SKILL_HOME}/scripts/render-plantuml.sh diagram-01.puml output_dir 01-system-overview
```

**输出文件**（在 `output_dir` 中）：
- `01-system-overview.puml` — 应用了 SVG 样式块的 PlantUML 源文件（scale 4）
- `01-system-overview.svg` — SVG（首选，矢量，无限缩放）
- `01-system-overview.png` — PNG（自适应分辨率，≤ 4095×4095）

**验证：**
1. 检查脚本输出报告的尺寸有效（中等图表的 SVG viewBox 应至少在一个轴上 ≥ 3840）
2. 验证 SVG 文件是有效的 XML：`file diagram-01.svg` 应显示 "SVG document"
3. 验证 PNG 文件：`file diagram-01.png` 应显示 "PNG image data" 且两个轴尺寸 ≤ 4095
4. 验证 PNG 非空白：4000+ 像素图片的文件大小应 > 100KB（空白的 4096×4096 ≈ 60KB）
5. 文件命名要有描述性：`{nn}-{short-title}`（如 `01-system-overview`）

**优先使用 SVG** 以获得任意缩放级别的清晰渲染；当用户明确要求或目标平台不支持 SVG 时使用 PNG。

**PNG 限制说明：** PlantUML Server 对 PNG 有 4096×4096 硬上限。当图表元素过多（>15）时，PNG 质量可能受限。此时应强制使用 SVG。

**CJK 渲染：** 包含 CJK（中文/日文/韩文）文字的图表，还需运行 CJK 渲染配套脚本：`node ${SKILL_HOME}/scripts/svg-to-png-cjk.cjs <input.svg> <output-cjk.png> 2`。该脚本在浏览器中使用系统 CJK 字体渲染，确保文字正确显示。

### Step 8: 组装最终 HTML 文档

将所有渲染的图表和文字组合为**单个 HTML 文档**，展示架构图并嵌入 SVG/PNG 图片（而非原始 PlantUML 代码）。

**HTML 结构：**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>[System Name] Architecture</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; max-width: 960px; margin: 0 auto; padding: 2rem; line-height: 1.6; color: #333; }
    h1 { border-bottom: 2px solid #eee; padding-bottom: 0.5rem; }
    h2 { margin-top: 2rem; color: #2c3e50; }
    h3 { color: #34495e; }
    .diagram { text-align: center; margin: 1.5rem 0; }
    .diagram img { max-width: 100%; height: auto; border: 1px solid #eee; border-radius: 4px; }
    .explanation { background: #f8f9fa; padding: 1rem; border-radius: 4px; margin: 1rem 0; }
  </style>
</head>
<body>
  <h1>[System Name] Architecture</h1>
  <section>
    <h2>Overview</h2>
    <p>[High-level system description]</p>
  </section>
  <section>
    <h2>Architecture Diagrams</h2>
    <h3>[Diagram 1 Title]</h3>
    <p>[Context]</p>
    <div class="diagram">
      <img src="01-diagram-name.svg" alt="[Diagram 1 Title]" />
    </div>
    <div class="explanation">
      [Explanation + Rationale]
    </div>
    <h3>[Diagram 2 Title]</h3>
    ...
  </section>
  <section>
    <h2>Summary</h2>
    <p>[Key architectural decisions and trade-offs]</p>
  </section>
</body>
</html>
```

**关键规则：**
- 使用**相对路径**引用 SVG/PNG 文件（图表和 HTML 在同一输出目录中）
- 或者，如果只有一张图，可以直接在 HTML 中内联嵌入 SVG 内容：`<svg>...</svg>`
- 确保所有图片有有意义的 `alt` 属性
- HTML 应自包含，可直接在浏览器中打开 `.html` 文件查看

## 输出要求

- 输出为**单个 HTML 文档**（`.html` 文件），包含渲染的 SVG/PNG 图表
- 图表**必须**通过 [render-plantuml.sh](scripts/render-plantuml.sh) 脚本渲染（该脚本内部调用 PlantUML 服务器）——最终输出中**不要**嵌入原始 PlantUML 文本
- SVG/PNG 图片文件与 HTML 保存在同一输出目录中
- HTML 通过相对路径引用图片（如 `<img src="01-overview.svg" />`）
- 单图输出时，内联 SVG 嵌入可作为替代方案
- PlantUML 源文件（`.puml`）也应保存以供未来编辑/重新生成
- HTML 语义元素中的文字描述（标题、段落、列表）
- 默认语言：遵循用户首选语言（本项目默认中文）
- 每张图至少包含：标题、渲染图片和简要说明

## 参考文档

### 操作指南（`references/howto/`）

按图表类型和 PlantUML 语法组织的分步指南。从此处开始动手绘制：

| # | 文档 | 内容 |
|---|------|------|
| 0 | [00-semantic-analysis.md](references/howto/00-semantic-analysis.md) | 语义分析与意图理解——分类输入类型、提取内容、差距分析、图表类型选择前的交互式确认 |
| 1 | [01-choose-diagram-type.md](references/howto/01-choose-diagram-type.md) | 如何根据用户描述、开发阶段和系统类型选择合适的 UML 图表类型 |
| 2 | [02-class-diagram.md](references/howto/02-class-diagram.md) | 如何画类图——类定义、6 种关系类型的 PlantUML 语法、包、GRASP 设计原则 |
| 3 | [03-component-diagram.md](references/howto/03-component-diagram.md) | 如何画组件图——分层架构、微服务模式、接口和依赖建模 |
| 4 | [04-deployment-diagram.md](references/howto/04-deployment-diagram.md) | 如何画部署图——物理拓扑、Kubernetes、云服务、节点间通信 |
| 5 | [05-sequence-diagram.md](references/howto/05-sequence-diagram.md) | 如何画时序图——消息类型、组合片段（alt/loop/par）、激活条、交互流程 |
| 6 | [06-package-diagram.md](references/howto/06-package-diagram.md) | 如何画包图——模块组织、命名空间层次、分层架构、依赖管理 |
| 7 | [07-usecase-diagram.md](references/howto/07-usecase-diagram.md) | 如何画用例图——角色、用例、系统边界、include/extend/generalization、用例描述模板 |
| 8 | [08-activity-diagram.md](references/howto/08-activity-diagram.md) | 如何画活动图——业务流程建模、泳道、fork/join 并发、决策节点、控制流 |
| 9 | [09-state-machine-diagram.md](references/howto/09-state-machine-diagram.md) | 如何画状态机图——对象生命周期、状态转换、事件/守卫/动作、组合状态、实现模式 |

### 语法参考（`references/`）

| 文档 | 内容 |
|------|------|
| [plantuml-guide.md](references/plantuml-guide.md) | 架构图的完整 PlantUML 语法参考：所有支持的图表类型、元素类型、关系语法、skinparam 自定义和常见模式 |
| [plantuml-best-practices.md](references/plantuml-best-practices.md) | 布局优化、内容组织、协作规范和按图表类型的布局指南。**Step 4 时必读** |
| [plantuml-official-docs.md](references/plantuml-official-docs.md) | PlantUML 官方文档和高级功能。按需加载用于语法边界情况或不常见的图表类型 |
| [plantuml-engine-behaviors.md](references/plantuml-engine-behaviors.md) | Graphviz 布局引擎行为模式、PlantUML Server 限制和根本性三方权衡（区域边框 vs 角色分布 vs 注释完整性）。按需加载用于复杂布局调试 |

### 源文档（`references/document/`）

UML 理论、PlantUML 工具、建模方法论、GRASP 模式和最佳实践的原始参考材料。按需加载以深入理解设计原则和方法论。

## 质量检查清单

交付最终文档前，验证：
- [ ] 用户绘制意图已完全理解（通过 Step 0 的分析或交互式问答）
- [ ] 所有图片引用内容已提取并映射到 UML 元素（如适用）
- [ ] 所有 PlantUML 源文件（`.puml`）有匹配的 `@startuml` / `@enduml`
- [ ] 每张图已通过 `render-plantuml.sh` 成功渲染为 SVG/PNG
- [ ] SVG 文件是有效的 XML（通过 `file` 命令验证）
- [ ] SVG 文件使用 `viewBox` 而无固定 width/height（确认 `svgDimensionStyle false` 已生效）
- [ ] SVG viewBox 至少在一个轴上 ≥ 3840（确认 `scale 4 + dpi 300` 已生效）
- [ ] PNG 文件尺寸 ≤ 4095×4095（不触发 Server 4096 硬上限）
- [ ] PNG 文件非空白：大图片文件大小 > 100KB（4096×4096 且 <100KB = 空白）
- [ ] 脚本输出 "Rendering Complete" 且无 WARNING
- [ ] HTML 用正确的相对路径引用所有图表图片
- [ ] 每张图使用了正确的 UML 类型
- [ ] 没有图表超过 7 个核心元素（可接受 ≤12；硬上限 15）；过大则拆分
- [ ] 文字说明引用了图表中的具体元素
- [ ] `skinparam` 在所有图表中提供一致的视觉样式（标准文档用单色；需要彩色时省略）
- [ ] `.puml` 源文件包含 `scale 4 + dpi 300`（SVG 质量保证）
- [ ] 别名和标签是人类可读的（非代码标识符）
- [ ] 所有元素名称和关系标签 ≤10 字符；更长的描述使用 `note` 元素
- [ ] 文档有从总览到细节的清晰叙事流
- [ ] 关系标签存在并描述交互方式（如 "uses via HTTP" 而非仅 "uses"）
- [ ] 无孤立元素（每个元素至少有一条关系）
- [ ] HTML 文件在浏览器中正确打开并显示所有图表
