---
title: "整合方案：K8s 基底 + ADR 机制 + 根目录索引"
created: 2026-07-28
expires: 2026-09-26
status: archived
target: "docs/concepts/documentation-model.md"
tags: [docs, design]
---

> ✅ 已合入 [docs/concepts/documentation-model.md](../concepts/documentation-model.md)（spec 033 / Feature 037 / ADR-0001 落地）

# 整合方案：K8s 基底 + ADR 机制 + 根目录索引

## 整体结构

```
项目根目录/
├── README.md               # 项目入口 → 索引到 docs/ 各区域
├── CONTRIBUTING.md         # 贡献流程入口 → 索引到 docs/contribute/
├── CHANGELOG.md            # 变更日志（自包含，不索引）
├── ARCHITECTURE.md         # 架构总览入口 → 索引到 docs/concepts/ + docs/decisions/
│
└── docs/
    ├── concepts/           # 概念：What & Why（架构、组件、核心抽象）
    │   ├── overview.md
    │   ├── core-abstractions.md
    │   └── ...
    │
    ├── tutorials/          # 教程：端到端学习路径（Learning-oriented）
    │   ├── getting-started.md
    │   └── ...
    │
    ├── tasks/              # 任务：完成特定目标的步骤（Task-oriented）
    │   ├── deploy-to-prod.md
    │   ├── write-a-plugin.md
    │   └── ...
    │
    ├── reference/          # 参考：API、CLI、配置项的精确描述
    │   ├── api.md
    │   ├── cli.md
    │   ├── config-schema.md
    │   └── ...
    │
    ├── decisions/          # ADR：架构决策记录（Why we chose X over Y）
    │   ├── README.md       # ADR 索引 + 模板说明
    │   ├── template.md
    │   ├── 0001-use-xxx.md
    │   ├── 0002-adopt-yyy.md
    │   └── ...
    │
    └── contribute/         # 贡献者指南：开发环境、代码规范、发布流程
        ├── dev-setup.md
        ├── coding-standards.md
        ├── release-process.md
        └── ...
```

---

## 根目录索引文件的职责定义

### README.md — 项目总入口

```markdown
# 项目名称

> 一句话描述项目是什么、解决什么问题。

## 快速开始
→ 见 [docs/tutorials/getting-started.md](docs/tutorials/getting-started.md)

## 文档导航

| 我想... | 去哪里 |
|---------|--------|
| 了解核心概念和设计哲学 | [docs/concepts/](../concepts) |
| 跟着教程上手 | [docs/tutorials/](../tutorials) |
| 完成一个具体任务 | [docs/tasks/](../tasks) |
| 查 API / CLI / 配置项 | [docs/reference/](../reference) |
| 了解某个设计决策的背景 | [docs/decisions/](../decisions) |
| 参与项目开发 | [CONTRIBUTING.md](../../CONTRIBUTING.md) |

## 架构总览
→ 见 [ARCHITECTURE.md](../../ARCHITECTURE.md)
```

**设计意图：** README 是"路标"，不承载实质内容，只做分发。读者 3 秒内能找到自己要去的地方。

---

### ARCHITECTURE.md — 架构总览入口

```markdown
# 架构总览

> 本文是架构文档的入口和摘要。详细内容在 docs/concepts/ 中展开。

## 系统全景图

（一张高层架构图）

## 核心组件

| 组件 | 职责 | 详细文档 |
|------|------|----------|
| ComponentA | ... | [docs/concepts/component-a.md](docs/concepts/component-a.md) |
| ComponentB | ... | [docs/concepts/component-b.md](docs/concepts/component-b.md) |

## 关键设计决策

| 决策 | 状态 | 记录 |
|------|------|------|
| 为什么选择 X 而非 Y | Accepted | [ADR-0001](docs/decisions/0001-use-xxx.md) |
| 为什么采用 Z 架构 | Accepted | [ADR-0002](docs/decisions/0002-adopt-yyy.md) |

## 深入阅读
- 概念详解 → [docs/concepts/](../concepts)
- 决策全量列表 → [docs/decisions/README.md](../decisions/README.md)
```

**设计意图：** ARCHITECTURE.md 是"一页纸架构"，给新人一个全局视图，同时通过链接指向 docs/ 中的深度内容。它和 docs/concepts/ 的关系是**摘要 vs 全文**。

---

### CONTRIBUTING.md — 贡献流程入口

```markdown
# 贡献指南

> 本文是贡献流程的入口。详细的开发文档在 docs/contribute/ 中。

## 快速参与

1. Fork & Clone → [docs/contribute/dev-setup.md](../contribute/dev-setup.md)
2. 了解代码规范 → [docs/contribute/coding-standards.md](docs/contribute/coding-standards.md)
3. 提交 PR → 遵循下方流程

## PR 流程
（简要描述，或链接到详细文档）

## 深入阅读
- 开发环境搭建 → [docs/contribute/dev-setup.md](../contribute/dev-setup.md)
- 发布流程 → [docs/contribute/release-process.md](docs/contribute/release-process.md)
- 架构决策背景 → [docs/decisions/](../decisions)
```

**设计意图：** CONTRIBUTING.md 是 GitHub 约定的标准文件（PR 页面会自动展示），所以它必须是自包含的"够用"文档，同时链接到 docs/contribute/ 中的深度内容。

---

### CHANGELOG.md — 自包含，不做索引

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
### Added
- ...

## [1.2.0] - 2026-07-01
### Changed
- ...
```

**设计意图：** CHANGELOG 是时间线文档，天然自包含，不需要索引到 docs/。但可以在条目中引用相关的 ADR 编号（如 `See ADR-0003`）。

---

## docs/ 内部各目录的定位

| 目录 | 回答的问题 | 读者 | 写作风格 |
|------|-----------|------|----------|
| `concepts/` | What is it? Why does it exist? | 想理解系统的开发者 | 解释性、叙述性 |
| `tutorials/` | How do I get started? | 第一次接触的用户 | 手把手、线性、有明确终点 |
| `tasks/` | How do I accomplish X? | 有具体目标的用户 | 步骤式、可跳读、面向任务 |
| `reference/` | What are the exact specs? | 需要精确信息的任何人 | 结构化、完整、无叙述 |
| `decisions/` | Why did we choose X over Y? | 开发者、未来的维护者 | 论证式、有替代方案对比 |
| `contribute/` | How do I work on this project? | 贡献者 | 流程式、操作性 |

---

## ADR 模板（docs/decisions/template.md）

```markdown
# ADR-NNNN: 标题

- **状态：** Proposed | Accepted | Deprecated | Superseded by ADR-XXXX
- **日期：** YYYY-MM-DD
- **决策者：** @person1, @person2

## 背景（Context）
什么问题/约束促使我们做这个决策？

## 决策（Decision）
我们选择了什么？

## 替代方案（Alternatives）
考虑过哪些其他方案？为什么没选？

## 后果（Consequences）
这个决策带来的正面和负面影响是什么？
```

---

## 根目录文件与 docs/ 的关系模型

```
根目录文件 = 入口 + 摘要 + 索引（薄层）
docs/ 目录 = 完整内容（厚层）

README.md          ──索引──→  docs/ 全部
ARCHITECTURE.md    ──摘要──→  docs/concepts/ + docs/decisions/
CONTRIBUTING.md    ──摘要──→  docs/contribute/
CHANGELOG.md       ──自包含──  （不索引，但可引用 ADR 编号）
```

**核心原则：根目录文件永远不超过一屏。** 如果某个根目录文件开始膨胀，说明内容应该下沉到 docs/ 中，根目录只保留摘要和链接。

---

## 文档生命周期与流转

```
新想法/调研 ──→ docs/decisions/ (Proposed)
                    │
                    ▼ Accepted
              docs/concepts/ 或 docs/reference/ 中体现设计
                    │
                    ▼ 用户需要操作指导
              docs/tasks/ 或 docs/tutorials/ 中编写操作文档
                    │
                    ▼ 项目演进，决策过时
              docs/decisions/ 中标记 Deprecated / Superseded
```

---

## 与之前三目录方案的对比

| 维度 | 你的原始方案 (manual/contributing/notes) | 整合方案 |
|------|----------------------------------------|----------|
| 分类粒度 | 3 个目录，按读者分 | 6 个目录，按文档类型分 |
| 认知负担 | 极低 | 中等（但有根目录索引降低负担） |
| 适用规模 | 小型项目（<20 篇文档） | 中型项目（20-200 篇） |
| 决策可追溯 | 无专门位置 | ADR 专门目录 |
| 临时文档 | notes/ 兜底 | 无专门兜底（见下方补充） |

### 关于"临时文档"的处理

整合方案中没有 `notes/` 目录。如果你仍然需要这个兜底，有两种选择：

**选项 A：保留 notes/ 作为第七个目录**
```
docs/notes/    # 草稿、调研、临时记录，无稳定性保证
```

**选项 B：用 ADR 的 Proposed 状态替代**
- 不成熟的想法 → 写一个 `Proposed` 状态的 ADR
- 调研笔记 → 放在对应 ADR 的"背景"部分
- 好处：所有临时内容都有明确的"毕业"路径（Proposed → Accepted → 内容沉淀到 concepts/tasks）

我个人倾向 **选项 B**，因为它强制每个临时文档都有一个"归宿目标"，避免 notes/ 变成垃圾场。但如果团队纪律性不够强，选项 A 更务实。
