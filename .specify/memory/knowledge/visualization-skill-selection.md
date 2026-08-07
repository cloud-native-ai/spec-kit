# 可视化技能选择结论账本

> 跨 cycle 累积的「需求类型 → 最优绘制技能」匹配知识。由 viz-skill-arena 团队每次 cycle 追加。

---

## 2026-08-07 Cycle 1: Substrate 架构图

### 任务类型
Kubernetes 系统架构图（含：组件架构图、部署架构图、Actor 生命周期序列图、Actor 状态机、资源模型分层图）

### 参赛技能
- draw-d3js（力导向图、热力图、状态机）
- draw-echarts（关系图、资源层级图、状态机）
- draw-mermaid（C4 组件图、部署图、序列图、状态机）
- **draw-plantuml ★ 冠军**（Component 图、Deployment 图、Sequence 图）

### 冠军结论
| 字段 | 值 |
|------|-----|
| **推荐技能** | **draw-plantuml** |
| **加权分** | 0.89（≥0.85 采纳线 ✓） |
| **无回退** | ✓（重绘 ≥ R1 自身分） |
| **裁决理由** | PlantUML 原生 UML 语义对系统架构图支持最精确：Component 图五大子系统标注清晰（身份/资源/控制面/节点/网络），Deployment 图含 K8s namespace 结构和协议标注，Sequence 图含完整 5 阶段 27 步请求流。三图信息密度高、语义保真度强、可维护性好。 |

### 各技能评估
| 技能 | 加权分 | 优势 | 不足 |
|------|--------|------|------|
| draw-mermaid | 0.81 | 序列图出色，渲染稳定（SVG/PNG/HTML 三格式） | 系统架构图缺少 UML 原生语义，组件图表达略弱 |
| draw-plantuml | **0.89** | 原生 UML 语义，三图质量均衡，细节丰富 | 部署图节点排版可优化 |
| draw-echarts | 0.72 | 交互式图表，关系图可视化效果好 | 不适合精确架构图，语义不够精确 |
| draw-d3js | 0.75 | 交互式力导向图，适合展示系统关系 | 架构图表达能力有限，可复现性较弱 |

### 本轮技能变更摘要
- 无技能变更被采纳（冠军技能无退化，但首次 cycle 以建立基线为主）

---

## 2026-08-07 Cycle 2: Substrate 架构图（修复 Phase C 后复跑）

### 任务类型
Kubernetes 系统架构图（含：组件架构图、部署架构图、Actor 生命周期序列图、Actor 状态机、资源模型分层图）

### 参赛技能
- draw-d3js（力导向图、热力图、状态机）
- draw-echarts（关系图、资源层级图、状态机）
- draw-mermaid（C4 组件图、部署图、序列图、状态机）
- **draw-plantuml ★ 冠军**（Component 图、Deployment 图、Sequence 图）

### 冠军结论
| 字段 | 值 |
|------|-----|
| **推荐技能** | **draw-plantuml** |
| **加权分** | 0.90（≥0.85 采纳线 ✓，较 cycle 1 的 0.89 提升） |
| **无回退** | ✓（重绘 ≥ R1 自身分 0.86） |
| **裁决理由** | 原生 Component/Deployment/Sequence/State 四种 UML 图型语义最精确；重绘后信息密度进一步提升（部署图含 namespace 与副本形态、序列图含 5 阶段彩色流程与图例、补独立状态机与资源模型图）；.puml 源文件自包含、渲染命令文档化、PNG/SVG/HTML 三格式齐备，可复现性最强。mermaid 序列图出色但组件图为 flowchart 近似；echarts/d3js 以图表近似架构语义，需求契合度不足。 |

### 各技能评估（R2 加权分 vs R1）
| 技能 | R1 | R2 | 采纳 |
|------|-----|-----|------|
| draw-mermaid | 0.73 | 0.87 | ✓ 无回退 |
| draw-plantuml | **0.86** | **0.90** | ✓ 冠军 + 无回退 |
| draw-echarts | 0.70 | 0.76 | ✓ 无回退 |
| draw-d3js | 0.73 | 0.79 | ✓ 无回退 |

### 本轮技能变更摘要（全部合并回 canonical 并同步镜像）
- **draw-mermaid**：组件图 howto 新增「子系统配色 + 图例」与「中心辐射布局」指引（03-component-diagram.md +53 行）；部署图/序列图 howto 增强；render-mermaid.sh 加固
- **draw-plantuml**：01-choose-diagram-type 增补；package-diagram howto +26 行；12-rendering-and-output +25 行；index.md 更新
- **draw-echarts**：echarts-guide.md +153 行（架构图表达指引）；assets/template.html 更新
- **draw-d3js**：SKILL.md 与 d3js-guide.md 更新

### 闭环验证
Phase C 修复后四个技能工作副本均产出变更，全部通过无回退门（R2 ≥ R1），验证「评审 → 技能优化 → 重绘 → 采纳合并」闭环有效。R1 三裁判中 technical 裁判因结构化输出超限失败（2/3 成功，均值计算自动容错）。

---

## 索引
| 日期 | 任务类型 | 冠军技能 | 加权分 |
|------|----------|----------|--------|
| 2026-08-07 | Kubernetes 系统架构图 | draw-plantuml | 0.89 |
| 2026-08-07 | Kubernetes 系统架构图（复跑） | draw-plantuml | 0.90 |