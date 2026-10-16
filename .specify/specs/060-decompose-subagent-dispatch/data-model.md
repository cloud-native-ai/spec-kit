# Data Model: 「驱动子代理」机制的技能化分解与公用化

**Feature**: 060 「驱动子代理」机制的技能化分解与公用化（decompose-subagent-dispatch）
**Spec**: [requirements.md](requirements.md)
**说明**: 本特性交付面为 Markdown 制品（技能体、真源文档、docs 页），无运行时数据库。本数据模型描述制品承载的**信息实体**及其约束——它们是实现契约测试与结构校验时的判定对象。既有概念（Agent Template / Agent Instance / Agent Execution / Subagent 三模态）的定义以真源为唯一权威，本文件只登记本特性**新增或变更的字段面**，不重定义实体本身。

## 实体一览

| # | 实体 | 层 | 承载制品 | 本特性变更 |
|---|------|-----|----------|------------|
| E1 | Agent Template「SDD 执行者」 | Template | `agents/sdd-executor.agent.md`（源）→ `.specify/agents/templates/`（镜像） | 新增 |
| E2 | 阶段职责 Agent Instance | Instance | `.specify/agents/instances/<slug>.agent.md` | 新增（按需创建） |
| E3 | Execution 拓扑声明 | Execution | 内联参数 或 `.specify/agents/execution/configs/<slug>.yaml` | 既有实体扩格 |
| E4 | 派发前置检查记录（Preflight Record） | Execution | 目标线状态脊/派发凭证（随派发落位） | 从两技能上收为 run-agent 承载 |
| E5 | 派发义务集（Obligation Set） | 跨层 | subagent-definitions / fast-fail / external-dispatch-recipes | 组成扩格（反嵌套上收） |
| E6 | 义务平价映射（Parity Map） | 计划产物 | `.specify/specs/060-…/contracts/delegation-parity.md` | 新增（tasks 期成为对账依据） |

## E1 — Agent Template「SDD 执行者」

**定位**: Agent Template 层能力描述——回答"能做什么"；职责无关。

| 字段 | 取值/形态 | 来源约束 |
|------|-----------|----------|
| `name` | `sdd-executor`（渲染为各工具 agent 名） | 既有渲染管线：qoder→`.qoder/agents/sdd-executor.agent.md` 等（`_AGENT_METADATA_MAPPING`） |
| `description` | 能力描述：以项目目录为工作目录、加载项目 `.specify/` 上下文、执行 `/speckit.*` 阶段命令 | FR-003 |
| `capacity-tools` / `skills` / `model-tier` / `run-turn-budget` | 中性词表字段，渲染层按工具转换 | 既有词表（create-agent Authoring Baseline）；`model-tier` 枚举 auto/lite/efficient/performance/ultimate |
| `user-invocable` | `false`（由编排技能委派调用，不作为用户直呼入口） | 与 create-team stage frame 的 executor 同型 |
| 职责字样 | MUST NOT 出现 setup/requirements 等具体职责 | FR-003（模板职责无关） |

**校验规则**:
- V-E1-1: frontmatter 含上述词表字段且职责字样零命中（FR-003；SC-001 的检索判据之一）。
- V-E1-2: **内容判据可复核**——模板全文不出现具体用户名、IP、环境别名、项目路径字面量（分发层判据的机械面；Session 2026-10-16 裁定）。
- V-E1-3: 源文件 `agents/` 与镜像 `.specify/agents/templates/` 字节一致（sync-mirrors 对）。

## E2 — 阶段职责 Agent Instance

**定位**: Instance 层职责描述——回答"为谁做什么"；引用 E1，不复述能力。

| 字段 | 取值/形态 | 来源约束 |
|------|-----------|----------|
| `name` | `<duty>-executor` 形态（如 `sdd-setup-executor`、`sdd-requirements-executor`） | 一实例一职责（FR-005） |
| `capacity-scope` | 指向 E1 模板（引用绑定，非能力复述） | 既有 capacity-scope 键语义 |
| 正文 | 职责绑定说明 + 该职责对模板能力面的具体化引用 | FR-004（复述为零） |

**校验规则**:
- V-E2-1: 实例体对模板能力面的复述为零——能力描述性句子仅经 `capacity-scope` 引用（SC-001 判据）。
- V-E2-2: 同 slug 冲突时 instance 优先（既有 run-agent 解析规则，不变）。
- V-E2-3: 生命周期状态面（FR-016）：`active → retired`；`retired` 制品保留可审计；存在活引用（运行中执行、团队席位、其他实例 `capacity-scope` 引用）时退役 MUST 被拒绝并提示先解引用。

## E3 — Execution 拓扑声明

**定位**: Execution 层运行要素——回答"在哪里怎么跑"；全部入口参数化。

| 要素 | 本地拓扑 | 远端拓扑 | 来源 |
|------|----------|----------|------|
| 项目目录 | `<project-dir>` | `<project-dir>`（远端路径） | FR-006 |
| 子代理 CLI | `<cli>`（qodercli/claude） | `<cli>` | FR-006；A3 不新增 |
| 登录目标 | 无 | `<alias>` 或 IP（ssh） | FR-006 |
| 运行身份 | 当前用户 | `<run-user>`（su/sudo，uid≠0） | FR-006 |
| 输入来源 | 内联提示词 / 简报文件（Recipe 5） | prompt 文件（Recipe 2） | [[STR-006]] 配方 |
| 执行形态 | 前台或后台+轮询 | 脱离派发（nohup）+定间隔轮询——**权威落点=loop-driver 保留差异段**（nohup 形态为其实测独有，analyze H-04 裁定；共性的前台+轮询形态引 [[STR-006]] Recipe 3/4） |

**双形态与冲突域**（FR-006, Session 2026-10-16）:
- 形态 A：内联参数（调用时给出要素值）；形态 B：执行配置文件（`.specify/agents/execution/configs/<slug>.yaml`，既有 schema：agent/mode/cli/per-dispatch 覆盖/log_dir）。
- **冲突消解**：两形态同给且任一要素值不一致 → 拒收报错并列出冲突字段清单；不静默取舍。
- 拓扑声明与 E2 实例引用正交：同一实例配任意拓扑（SC-002 判据）。

**校验规则**:
- V-E3-1: 远端拓扑四要素（目标/身份/目录/CLI）齐备才可解析；缺项按前置检查失败处置（E4）。
- V-E3-2: 运行身份 uid=0（root）→ fail（既有前置检查族第②族约束）。
- V-E3-3: 冲突域检测先于派发（拒收发生在解析期，不是运行期）。

## E4 — 派发前置检查记录（Preflight Record）

**定位**: 五族检查逐项结论——**上收后由 run-agent 承载**（FR-012 Session 裁定），配方真源与两技能引用。

| 族 | 检查 | 结论域 | fail 处置 |
|----|------|--------|-----------|
| ① | SSH 连通性（本地拓扑跳过） | ok / fail | 停线+上送四要素 |
| ② | 非 root 运行用户 | ok / fail | 停线+上送四要素 |
| ③ | 子代理 CLI 可用性与版本 | ok / fail（版本记录） | 停线+上送四要素 |
| ④ | LLM 配置（model/context/effort） | ok / uncertain | uncertain→列待补清单 |
| ⑤ | spec-kit 框架可用性 | ok / fail | fail→handoff sdd-project-setup（缺失=install、退化=refresh），处置完重跑 |

**唯一落点**：`skills/internal/run-agent/references/dispatch-preflight.md`（新文件，承载表与处置链）——`skills/external/sdd-loop-driver/references/dispatch-recipes.md` 与 `skills/external/sdd-project-setup/references/setup-recipes.md` 的同型表删除并改为引用；`external-dispatch-recipes.md` 维持"只有 how 配方、无检查"的既有边界，不改。

**校验规则**:
- V-E4-1: 全仓检索五族检查表条目原文（`ConnectTimeout`、`id <run-user>`、`--version`、`source.json` 等判据字面量的**成组共现**）在**框架源侧**（`skills/`、`shared/`——排除 `.specify/` 镜像副本）恰 1 处权威落点（SC-003 判据；镜像由 sync-mirrors 保证一致，不计入检索面——analyze M-06 修复）。
- V-E4-2: 结论以每项 ≤3 行摘要写入调用方状态脊，不全文回显（平价保留既有义务）。

## E5 — 派发义务集（Obligation Set）

**组成**（各自真源不变，本特性只做接线与上收）:

| 义务 | 真源 | 本特性动作 |
|------|------|-----------|
| 模态选择（native/virtual/external） | subagent-definitions | 接线说明（run-agent 引用） |
| 可见性契约（stream-json+紧凑化+三元组） | subagent-definitions | 引用不复制 |
| 注入子句+异常回传行+派发前自检 | fast-fail.md | 引用不复制 |
| **反嵌套红线**（子代理提示词不引用驱动/循环技能） | 原 sdd-loop-driver SKILL.md Driver Topology 节 | **上收**为 run-agent 派发义务；原节改为引用+循环视角自检行 |
| 拓扑配方（断点探测/提示词文件/runner/轮询/本地变体） | external-dispatch-recipes | 引用不复制 |

**校验规则**:
- V-E5-1: 经 run-agent 派发的提示词模板（其 references 与正文）中，驱动/循环技能名零命中（SC-004 判据）。
- V-E5-2: sdd-loop-driver SKILL.md 保留编排视角的自检义务行（平价：加载者发现自己是"代为驱动"subagent 时显式异常上报——该行语义保留，落点随上收调整并在平价映射中追溯）。

## E6 — 义务平价映射（Parity Map）

**定位**: 改造验收的对账底册——**唯一权威落点 = `contracts/delegation-parity.md` § P 表（P-01..P-15，嵌套超集形态：既覆盖 FR-011 的九项义务枚举，也含编排本体保留行与更严行）**。本节不复写其行集，仅登记列语义与对账程序（analyze M-02 修复：来源标注订正）。

对账程序（tasks T022 执行）：以 T001 冻结的改造前原文清单为分母，P 表逐行填实"新落点/强度/追溯"三列；实现期发现额外义务按同格式追加行。

**义务枚举下限**（指针——行集以 P 表为唯一承载）：FR-011 列名的九项 + 编排本体保留与更严项，全量见 `contracts/delegation-parity.md` § C-35 节。

## 实体关系

```text
E1 Template (sdd-executor, agents/ 源+镜像)
   └─ capacity-scope 引用 ──▶ E2 Instance ×N (一实例一职责, active/retired)
                                └─ 实例引用 + E3 拓扑声明 ──▶ run-agent 派发
                                                              ├─ E4 Preflight (五族, 上收)
                                                              ├─ E5 Obligations (注入/异常行/反嵌套/可见性)
                                                              └─ E6 Parity Map 对账
```
