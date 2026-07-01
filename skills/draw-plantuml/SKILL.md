---
name: draw-plantuml
description: |
  Draw system architecture diagrams with PlantUML, render to SVG/PNG via PlantUML server, and output as HTML with rendered images.
  Use standard UML semantics (Component, Deployment, Sequence, Class/Package) to describe system architecture.
  Use when the user mentions "架构图", "architecture diagram", "UML图", "plantuml", "系统架构图", "画架构", "设计图", "组件图", "部署图", "时序图", "类图", "包图", "系统设计",
  "流程图", "状态图", "活动图", "用例图", "状态机图", "模块图", "交互图",
  "sequence diagram", "class diagram", "component diagram", "deployment diagram",
  "activity diagram", "state diagram", "use case diagram", "package diagram"
skill_id: "<SKILL:.specify/skills/draw-plantuml/SKILL.md>"
---

# Architecture Diagram Skill

Draw system architecture diagrams using PlantUML syntax and standard UML semantics, render diagrams to SVG/PNG via the PlantUML server, and output as a complete HTML document with rendered diagram images and descriptive text.

## Core Principles

### 1. UML Semantics, Not Free-Form Boxes
Every diagram must follow standard UML diagram types. Avoid ad-hoc "boxes and arrows" — use proper UML elements (components, nodes, lifelines, classes) with correct relationships (dependency, association, realization, etc.).

### 2. Architecture-First Narrative
The markdown text should tell a story: start with system context, then drill into components and their interactions. Diagrams and text complement each other — text explains *why*, diagrams show *what*.

### 3. PlantUML Best Practices
For PlantUML-specific conventions (syntax, styling, element types, relationship notation), see [plantuml-guide.md](references/plantuml-guide.md). For layout optimization, content organization, and collaboration conventions, see [plantuml-best-practices.md](references/plantuml-best-practices.md). Key principles: use `skinparam` for consistent styling, keep diagrams ≤7 core elements (≤15 hard limit), control layout via direction keywords and grouping, use meaningful labels.

## Workflow

This skill is designed to draw UML diagrams based on existing information (user descriptions, code, documents) and add corresponding text explanations. Follow the steps below in order.

### Step 1: Choose Diagram Type

**MUST** first read [01-choose-diagram-type.md](references/howto/01-choose-diagram-type.md) to determine the appropriate UML diagram type(s).

Based on the user's description, identify what they want to express and match it to the right diagram:

- Use the **快速匹配表** (Quick Match Table) to map user keywords → diagram type
- Use the **按开发阶段推荐** (By Development Phase) table if the user mentions a specific phase
- Use the **选择决策流程** (Decision Flow) to narrow down structure vs behavior diagrams

If multiple aspects need to be expressed, select multiple diagram types — each diagram focuses on one perspective.

### Step 2: Follow the How-To Guide

Once the diagram type is determined, **MUST** read and follow the corresponding how-to guide for detailed drawing instructions:

| Diagram Type | How-To Guide |
|-------------|-------------|
| 类图 (Class Diagram) | [02-class-diagram.md](references/howto/02-class-diagram.md) |
| 包图 (Package Diagram) | [06-package-diagram.md](references/howto/06-package-diagram.md) |
| 组件图 (Component Diagram) | [03-component-diagram.md](references/howto/03-component-diagram.md) |
| 部署图 (Deployment Diagram) | [04-deployment-diagram.md](references/howto/04-deployment-diagram.md) |
| 时序图 (Sequence Diagram) | [05-sequence-diagram.md](references/howto/05-sequence-diagram.md) |
| 用例图 (Use Case Diagram) | [07-usecase-diagram.md](references/howto/07-usecase-diagram.md) |
| 活动图 (Activity Diagram) | [08-activity-diagram.md](references/howto/08-activity-diagram.md) |
| 状态机图 (State Machine Diagram) | [09-state-machine-diagram.md](references/howto/09-state-machine-diagram.md) |

Each how-to guide provides:
- **Key elements**: UML elements and their PlantUML syntax
- **Complete examples**: Runnable PlantUML code blocks
- **Modeling steps**: Step-by-step instructions for constructing the diagram
- **Best practices**: Common patterns and pitfalls

For additional PlantUML syntax details, also reference [plantuml-guide.md](references/plantuml-guide.md).

### Step 3: Semantic Layout Planning

Before writing PlantUML code, analyze the semantic relationships between components to determine their natural positions. This prevents layout issues by establishing a semantically-grounded spatial arrangement upfront.

#### 3.1 Identify Component Roles

Classify each component:

| Role | Description | Typical Position |
|------|-------------|------------------|
| **Hub (中心端)** | Central component that many others connect to | Center-top |
| **Edge (节点端)** | Components connecting to the hub in 1:many pattern | Below the hub |
| **Peer (对等端)** | Same-level, similar function | Side-by-side (`together {}`) |
| **Entry (入口)** | External access point | Left edge or top |
| **Sink (汇聚端)** | Data destination, storage, external service | Right edge or bottom |
| **External (外部)** | Outside the system boundary | Outside main frame |

#### 3.2 Map Relationships to Layout

| Relationship Pattern | Layout Rule | PlantUML Technique |
|---------------------|-------------|-------------------|
| **1:many (hub-spoke)** | Hub above, edges below | Hub in upper frame; edges in lower frames |
| **Peer (同级)** | Side-by-side | `together {}` block |
| **Chain (链式)** | Sequential flow | Default arrow `-->` |
| **Hierarchical (层次)** | Parent above children | Nested containers |

#### 3.3 Draft Position Map

Sketch a rough position map before writing code. Example for Kubernetes:

```
[External: Users] → [Entry: Ingress → Service]
                              ↓ ClusterIP
[Hub: Control Plane]   [Edge: Node 1]  [Edge: Node 2]  → [Sink: PV]
(Sched, CM → API → etcd) (kubelet, Pod)  (kubelet, Pod)
                              ↓ pull
                       [Sink: Registry]
```

The position map determines: layout direction, element declaration order, `together{}` groupings, and nesting structure.

### Step 4: Draft PlantUML Code

Based on the how-to guide and the user's system information:

1. Identify the key elements (participants/nodes/components/classes/etc.) from the user's description
2. Define the relationships between them (dependencies, messages, transitions, etc.)
3. Write PlantUML code with `@startuml` / `@enduml` wrapping
4. Keep each diagram focused: ≤7 core elements (acceptable ≤12, hard limit 15); split into multiple diagrams if larger
5. **Apply layout best practices**: use direction keywords (`-right->`, `-down->`), group related elements (`together{}`), and declare elements before relationships
6. **Keep labels short (≤10 chars)**: element names and relationship labels must not exceed 10 characters; use `note` elements for supplementary details

For PlantUML syntax details (element types, relationship notation, styling, patterns), reference [plantuml-guide.md](references/plantuml-guide.md). The guide includes a **Quick Syntax Reference by Diagram Type** table covering all 7 diagram types.

**MUST** also follow [plantuml-best-practices.md](references/plantuml-best-practices.md) for:
- Layout optimization (§1): direction control, hidden connections, grouping, spacing
- Content organization (§2): single responsibility, C4 layered splitting, element ordering
- Visual highlighting (§3): **label length ≤10 chars**, note placement, alias readability
- Per-diagram-type layout guidance (§5): recommended direction and layout focus for each UML type

### Step 5: Apply Standard Style

After drafting PlantUML code, **MUST** apply the standard style configuration defined in [plantuml-style.md](references/plantuml-style.md). For each diagram:

1. Insert the **base style block** immediately after `@startuml` (before any diagram content):
   ```plantuml
   skinparam monochrome true
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
   For **class/component/deployment diagrams** only, also add `top to bottom direction` as the first line. Do NOT add it for sequence/activity/state/use-case diagrams.
2. If the diagram contains `actor` elements or is a Use Case Diagram, additionally add:
   ```plantuml
   skinparam actorStyle awesome
   ```
3. Verify placement: all style declarations must appear **after** `@startuml` and **before** any element definitions
4. Verify no conflicts: ensure no duplicate or overriding `skinparam` declarations exist in the diagram body

**注意：** `.puml` 源文件统一使用 `scale 4 + dpi 300`（面向 SVG 最高质量）。PNG 渲染由 `render-plantuml.sh` 脚本**自动计算**合适的 scale/dpi 参数，确保 PNG 输出 ≤ 4095×4095（低于 PlantUML Server 硬上限 4096）。无需手动为 PNG 调整样式。

### Step 6: Write Accompanying Text

For each diagram, prepare the following descriptive content (to be included in the final HTML):
1. **Diagram Title** (will become H2/H3 heading in HTML)
2. **Context**: 1-2 sentences on what this diagram represents and why this type was chosen
3. **PlantUML source**: save the code as `.puml` file for reference and rendering
4. **Explanation**: Key points for each key element and relationship
5. **Design Rationale**: Why this structure/interaction pattern was chosen (if applicable)

### Step 7: Render PlantUML to SVG/PNG

After drafting and styling all PlantUML code, render each diagram into SVG (preferred) and PNG using the rendering script.

**Rendering script:** [scripts/render-plantuml.sh](scripts/render-plantuml.sh)

The script implements **SVG/PNG 双策略渲染**：
- **SVG**：始终使用 `scale 4 + dpi 300`（矢量格式，无尺寸限制，无损缩放）
- **PNG**：自适应计算 scale/dpi，确保输出 ≤ 4095×4095（低于 PlantUML Server 硬上限 4096）
  - 从 SVG viewBox 推算图表实际大小
  - 自动选择最大化质量且不超限的 scale + dpi 组合
  - 渲染后验证 PNG 非空白（文件大小合理性检查）
  - 若检测到空白输出，自动降级重试

**Procedure for each diagram:**
```bash
bash ${SKILL_HOME}/scripts/render-plantuml.sh diagram-01.puml output_dir 01-system-overview
```

**Output files** (in `output_dir`):
- `01-system-overview.puml` — PlantUML source with SVG style block applied (scale 4)
- `01-system-overview.svg` — SVG (preferred, vector, infinitely scalable)
- `01-system-overview.png` — PNG (adaptive resolution, ≤ 4095×4095)

**Verification:**
1. Check the script output reports valid dimensions (SVG viewBox should be ≥ 3840 on at least one axis for medium diagrams)
2. Verify SVG file is valid XML: `file diagram-01.svg` should show "SVG document"
3. Verify PNG file: `file diagram-01.png` should show "PNG image data" with dimensions ≤ 4095 on both axes
4. Verify PNG is not blank: file size should be > 100KB for 4000+ pixel images (blank 4096×4096 ≈ 60KB)
5. Name files descriptively: `{nn}-{short-title}` (e.g., `01-system-overview`)

**Prefer SVG** for scalability and crisp rendering at any zoom level; use PNG when the user explicitly requests it or when the target platform does not support SVG.

**PNG 限制说明：** PlantUML Server 对 PNG 有 4096×4096 硬上限。当图表元素过多（>15）时，PNG 质量可能受限。此时应强制使用 SVG。

### Step 8: Assemble Final HTML Document

Combine all rendered diagrams and text into a **single HTML document** that displays the architecture with embedded SVG/PNG images (not raw PlantUML code).

**HTML Structure:**

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

**Key Rules:**
- Reference SVG/PNG files using **relative paths** (diagrams and HTML in the same output directory)
- Alternatively, if only one diagram exists, embed the SVG content inline in the HTML using `<svg>...</svg>` directly
- Ensure all images have meaningful `alt` attributes
- HTML should be self-contained and viewable by opening the `.html` file directly in a browser

## Output Requirements

- Output as a **single HTML document** (`.html` file) with rendered SVG/PNG diagrams
- Diagrams MUST be rendered via the [render-plantuml.sh](scripts/render-plantuml.sh) script (which calls the PlantUML server internally) — do NOT embed raw PlantUML text in the final output
- SVG/PNG image files saved alongside the HTML in the same output directory
- HTML references images via relative paths (e.g., `<img src="01-overview.svg" />`)
- For single-diagram outputs, inline SVG embedding is acceptable as an alternative
- PlantUML source files (`.puml`) should also be saved for future editing/regeneration
- Text descriptions in HTML semantic elements (headings, paragraphs, lists)
- Default language: follow user's preferred language (Chinese by default for this project)
- Each diagram must have at minimum: a title, a rendered image, and a brief explanation

## Reference Documents

### How-To Guides (`references/howto/`)

Step-by-step guides organized by diagram type and PlantUML syntax. Start here for hands-on drawing:

| # | Document | Content |
|---|----------|---------|
| 1 | [01-choose-diagram-type.md](references/howto/01-choose-diagram-type.md) | How to select the right UML diagram type based on user description, development phase, and system type |
| 2 | [02-class-diagram.md](references/howto/02-class-diagram.md) | How to draw Class Diagrams — class definition, 6 relationship types with PlantUML syntax, packages, GRASP design principles |
| 3 | [03-component-diagram.md](references/howto/03-component-diagram.md) | How to draw Component Diagrams — layered architecture, microservice patterns, interface and dependency modeling |
| 4 | [04-deployment-diagram.md](references/howto/04-deployment-diagram.md) | How to draw Deployment Diagrams — physical topology, Kubernetes, cloud services, node-to-node communication |
| 5 | [05-sequence-diagram.md](references/howto/05-sequence-diagram.md) | How to draw Sequence Diagrams — message types, combined fragments (alt/loop/par), activation bars, interaction flow |
| 6 | [06-package-diagram.md](references/howto/06-package-diagram.md) | How to draw Package Diagrams — module organization, namespace hierarchy, layered architecture, dependency management |
| 7 | [07-usecase-diagram.md](references/howto/07-usecase-diagram.md) | How to draw Use Case Diagrams — actors, use cases, system boundary, include/extend/generalization, use case description template |
| 8 | [08-activity-diagram.md](references/howto/08-activity-diagram.md) | How to draw Activity Diagrams — business process modeling, swimlanes, fork/join for concurrency, decision nodes, control flow |
| 9 | [09-state-machine-diagram.md](references/howto/09-state-machine-diagram.md) | How to draw State Machine Diagrams — object lifecycle, state transitions, events/guards/actions, composite states, implementation patterns |

### Syntax Reference (`references/`)

| Document | Content |
|----------|---------|  
| [plantuml-guide.md](references/plantuml-guide.md) | Complete PlantUML syntax reference for architecture diagrams: all supported diagram types, element types, relationship syntax, skinparam customization, and common patterns |
| [plantuml-best-practices.md](references/plantuml-best-practices.md) | Layout optimization, content organization, collaboration conventions, and per-diagram-type layout guidance. **MUST read during Step 4** |
| [plantuml-official-docs.md](references/plantuml-official-docs.md) | PlantUML official documentation and advanced features. Load on-demand for syntax edge cases or less common diagram types |

### Source Documents (`references/document/`)

Original reference materials on UML theory, PlantUML tools, modeling methodology, GRASP patterns, and best practices. Load on-demand for deeper understanding of design principles and methodology.

## Quality Checklist

Before delivering the final document, verify:
- [ ] All PlantUML source files (`.puml`) have matching `@startuml` / `@enduml`
- [ ] Each diagram has been successfully rendered to SVG/PNG via `render-plantuml.sh`
- [ ] SVG files are valid XML (verified with `file` command)
- [ ] SVG files use `viewBox` without fixed width/height (confirm `svgDimensionStyle false` is active)
- [ ] SVG viewBox ≥ 3840 on at least one axis（confirm `scale 4 + dpi 300` took effect）
- [ ] PNG files dimensions ≤ 4095×4095（不触发 Server 4096 硬上限）
- [ ] PNG files are NOT blank: file size > 100KB for large images（4096×4096 且 <100KB = 空白）
- [ ] PNG output confirmed by script "Rendering Complete" without WARNING
- [ ] HTML references all diagram images with correct relative paths
- [ ] Each diagram uses the correct UML type for its purpose
- [ ] No diagram exceeds 7 core elements (acceptable ≤12; hard limit 15); split if larger
- [ ] Text explanations reference specific elements in the diagram
- [ ] `skinparam` provides consistent visual style across all diagrams
- [ ] `.puml` source contains `scale 4 + dpi 300`（SVG 质量保证）
- [ ] Aliases and labels are human-readable (not code identifiers)
- [ ] All element names and relationship labels ≤10 characters; longer descriptions use `note` elements
- [ ] Document has a clear narrative flow from overview to details
- [ ] Relationship labels are present and describe the interaction (e.g., "uses via HTTP", not just "uses")
- [ ] No orphan elements (every element has at least one relationship)
- [ ] HTML file opens correctly in a browser and displays all diagrams
