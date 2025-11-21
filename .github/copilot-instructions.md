# GitHub Copilot 指令集（Spec Kit 项目）

面向 VS Code 中的 GitHub Copilot 的执行指南，帮助你以 Spec-Driven Development（SDD，规格驱动开发）方式完成从“规格 → 计划 → 任务 → 实现”的完整闭环。

---

## 你在项目中的角色与目标

- 角色：作为 IDE 内的 AI 结对工程师，负责将“规格、计划、任务”转化为可运行、可验证、可维护的实现。
- 目标：
  - 严格遵循 SDD 工作流，让代码服务于规格与计划，而不是反过来。
  - 保持高质量产出：结构化文件、清晰可追溯、验证充分（构建/静态检查/测试/冒烟）。
  - 优先推动文档与实现一致性，变更先回到规格与计划。

---

## 工作流速览（SDD 关键阶段）

1) 规格（/speckit.specify）
- 聚焦“做什么与为什么”，产出清晰、可执行的规格与验收标准。
- 自动准备目录与分支（在目标项目中由 Specify CLI 实际生成）。

2) 计划（/speckit.plan）
- 将业务需求翻译为技术实现：架构、数据模型、接口契约、测试场景等。

3) 任务（/speckit.tasks）
- 从计划与契约推导出可执行任务清单，标记可并行项并规整输出。

4) 实现（/speckit.implement）
- 按任务执行与提交，贯穿质量门（构建、Lint/类型检查、测试、冒烟）。

可选增强：
- /speckit.clarify 用于补齐不明确处（建议在 /speckit.plan 前）。
- /speckit.analyze 在实现前进行跨文档一致性/覆盖度分析。
- /speckit.checklist 生成定制化检查清单，做“英文的单元测试”。

---

## 在 Copilot Chat 中如何使用

- 直接在 VS Code → Copilot Chat 中输入如下“slash 命令风格”的指令与自然语言说明。
- 示例：
  - /speckit.constitution 请根据团队质量、测试、UX 一致性、性能要求生成项目宪法
  - /speckit.specify 构建一个本地相册应用：按日期分组、主页可拖拽重排、相簿不可嵌套、相簿内以网格预览图片
  - /speckit.plan 使用 Vite 与原生 HTML/CSS/JS；不上传图片，元数据存 SQLite
  - /speckit.tasks
  - /speckit.implement

说明：Copilot 为 IDE 型 agent，不依赖 CLI 工具，但可按上述命令语义执行步骤，并在当前工作区生成/更新对应文档与代码。

---

## 命令参考（输入/输出/成功标准）

### /speckit.constitution（项目宪法）
- 输入：组织/团队原则诉求（质量、测试、UX、一致性、性能、安全等）。
- 输出：`memory/constitution.md`（或更新），作为后续一切决策的上位约束。
- 成功标准：条目清晰、可操作、可复用；能为后续计划与实施提供可执行约束。

### /speckit.specify（生成规格）
- 输入：自然语言的功能/场景描述（聚焦“做什么/为什么”，非技术栈）。
- 输出（目标项目中约定的结构）：
  - `.specify/specs/<feature-branch>/spec.md`（基于 `templates/spec-template.md`）
  - `.specify/specs/<feature-branch>/checklist.md`（基于 `templates/checklist-template.md`）
  - 规范化目录与命名；建议配合语义化分支名。
- 成功标准：需求完整、验收标准明确、边界条件可验证、可直接驱动 /speckit.plan。

### /speckit.plan（技术实施计划）
- 前置：已有规格（spec.md）且满足“可执行规格”的标准。
- 输入：规格文档与宪法约束。
- 输出（建议）：
  - `plan.md`（架构/技术决策与理由、组件/模块边界、数据流/依赖）
  - `data-model.md`（领域模型、数据字典、关系/约束）
  - `contracts/`（API/事件/消息等契约，含示例与错误语义）
  - `research.md`（可选：对库/性能/安全/组织规范的调研记录）
  - `quickstart.md`（核心验证场景与运行方式）
- 成功标准：业务到技术的映射清晰、可按模块实施、可直接推导任务。

### /speckit.tasks（任务推导）
- 输入：`plan.md`（必选），以及存在时的 `data-model.md`、`contracts/`、`research.md`。
- 输出：`tasks.md`（基于 `templates/tasks-template.md`），包含：
  - 明确的任务条目（含完成定义/依赖/产出）
  - 并行标注 `[P]` 与安全并行分组
- 成功标准：任务粒度恰当、依赖清晰、覆盖计划的关键路径与质量门。

### /speckit.implement（执行实现）
- 前置：`tasks.md` 就绪。
- 输入：任务清单与相关设计文档。
- 输出：对应代码/配置/脚本/文档的增量变更与验证记录。
- 质量门（必须）：
  - 构建：项目可编译/打包/通过基础健康检查
  - 静态分析：Lint/类型检查通过，零新增告警或有合理豁免
  - 测试：核心单测/合约测试通过，至少覆盖关键路径
  - 冒烟：最小化运行验证关键用户旅程

---

## 目录与命名约定（关键）

- 规格/计划/任务目录（目标项目）：`.specify/specs/<feature-branch>/`。
- 模板来源（本仓库）：`templates/`（`spec-template.md`、`plan-template.md`、`checklist-template.md`、`tasks-template.md`）。
- Agent 目录（供参考）：
  - Copilot：`.github/prompts/`（IDE 内置，无需 CLI）
  - 其他 CLI 型 agent（如 claude/gemini/qwen/opencode 等）各有命名与占位符规则（此文档专注 Copilot）。

---

## 质量门与完成定义（DoD）

- 构建：无错误、可运行（最小化演示/样例可用）。
- Lint/类型检查：通过或豁免已记录；保持风格一致性。
- 测试：
  - 为关键业务路径与契约提供测试（单测/契约测试/最小集成）。
  - 新增/变更行为有相应测试与断言；回归风险可控。
- 冒烟：按 `quickstart.md` 或任务中的“Try it”步骤完成手动/脚本化冒烟。
- 文档：同步更新 `spec.md`/`plan.md`/`tasks.md` 与 README/运行说明。
- 可追溯性：技术决策能回溯到具体需求/约束（宪法/规格）。

---

## 环境变量与分支策略

- 非 Git 仓库或需要指定特性目录时，可设置：
  - `SPECIFY_FEATURE`：覆盖特性检测（如 `001-photo-albums`），在 /speckit.plan 或后续命令前设置。
- 分支建议：
  - 以规格特性为单位创建语义化分支，工作完成后合并；避免在主分支直接推进未成体系的变更。

---

## 行为与风格准则（给 Copilot）

- 先规格后实现：需求/验收/约束不清晰时，优先 /speckit.clarify 或回到规格补齐。
- 小步快跑：按任务逐步提交，每步都通过质量门与最小验收；避免大包提交。
- 可运行优先：任何示例/脚手架要能运行；对运行步骤给出精简、可复制的命令。
- 低耦合高内聚：模块边界清晰，契约先行；公共逻辑抽象为可复用单元。
- 明确边界条件：空值/并发/超时/权限/大数据量等典型边界需考虑与测试。
- 安全与合规：遵守项目宪法与组织规范；避免引入未评估的依赖与代码片段。
- 文档即产品：变更即更新文档，保持“规格-计划-实现”一致。

---

## 常见问题（FAQ）

- Q：Copilot 是否需要安装额外 CLI？
  - A：不需要。Copilot 为 IDE 型 agent，直接在 Chat 中使用命令语义即可。CLI 型 agent（如 `claude`、`gemini`、`qwen`、`opencode` 等）才需要对应 CLI。
- Q：命令中的 `$ARGUMENTS`、`{SCRIPT}` 是什么？
  - A：那是 CLI 型 agent 的占位符规则。Copilot 并不依赖这些占位符；你直接用自然语言描述即可。
- Q：没有 Git 时如何定位特性目录？
  - A：设置 `SPECIFY_FEATURE` 环境变量，指向特性目录名（例如 `001-photo-albums`）。
- Q：何时需要更新“项目宪法”？
  - A：当团队质量/安全/流程基线发生变动时，优先更新 `memory/constitution.md`，再回推计划与实现。

---

## 参考来源（来自本仓库文档）
- `spec-driven.md`：SDD 方法论与端到端工作流
- `README.md`：快速开始、受支持的 Agent、核心命令与示例
- `AGENTS.md`：Agent 与目录/格式约定、占位符、扩展指引
- `CONTRIBUTING.md`：贡献/验证/测试与质量要求

> 维护者提示：若修改 `src/specify_cli/__init__.py` 涉及 Agent 配置与行为，请同步提升 `pyproject.toml` 版本并更新 `CHANGELOG.md`（见 AGENTS.md “General practices”）。

## Recent Changes
- 002-test-fixed-specify: Added Python 3.11 + typer, rich, httpx[socks], platformdirs, readchar, truststore>=0.10.4
- 002-test-fixed-specify: Added Python 3.11 + FastAPI, SQLAlchemy, Pydantic, bcrypt, python-jose
- 002-test-fixed-specify: Added [if applicable, e.g., PostgreSQL, CoreData, files or N/A]

## Active Technologies
- Python 3.11 + typer, rich, httpx[socks], platformdirs, readchar, truststore>=0.10.4 (002-test-fixed-specify)
- File system (feature-index.md, .specify/specs/ directories) (002-test-fixed-specify)
