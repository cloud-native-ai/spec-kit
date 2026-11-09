# Implementation Plan: 浏览器站点记忆与分级自动化(browser-utils Site Memory)

**Branch**: `[046-browser-site-memory]` | **Date**: 2026-08-24 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `046-browser-site-memory` → Feature 048 Browser Utils Skill
**Input**: Specification from `.specify/specs/046-browser-site-memory/requirements.md`

## Summary

为 browser-utils 技能建设站点记忆机制:以 domain(host:port)为 key 的 `site/<host>/` 记忆目录、四态状态机(exploration → optimization → validation → sealed,失败回退 optimization)、探索期全量留痕(DOM 操作 + 底层网络请求,敏感字段脱敏)、优化期蒸馏请求级步骤集(Request Recipe)、验证期端到端验证与固化/回退。状态判定与格式校验遵循程序优先,落在一个 stdlib-only 引擎 `skills/browser-utils/scripts/site-memory.py`;记录与状态文件为 agent 中立的 JSON/JSONL,三个 Tier 均可读写。SKILL.md 增加"站点记忆与双方向路由"入口段(契约级),机制细节进 `references/site-memory.md`、请求级模式进 `references/request-level-patterns.md`。框架侧按 FR-003 收口分发边界:`.gitignore` 排除、sync-mirrors skills 对排除 `site` 分量、wheel 经 `src/hatch_build.py` 舞台拷贝排除(实证:hatchling `exclude` 对 force-include 不生效,见 research.md R2)。

## Technical Context

**Language/Version**: Python ≥ 3.8(引擎,stdlib-only,与框架引擎惯例一致);JavaScript/Node(Tier 2 Playwright 留痕钩子,复用既有 scripts/js 运行器)
**Primary Dependencies**: 无新增运行时依赖;Playwright(既有)、hatchling(构建期,既有)
**Storage**: 本地文件 —— `skills/browser-utils/site/<host:port>/` 下 JSON/JSONL(state.json / records/*.jsonl / recipe.json / validation/*.json);spec-kit 仓 gitignore 排除,运行时数据由调用方项目归档
**Testing**: pytest 契约测试 `tests/contract/test_browser_site_memory.py`(状态机迁移、脱敏强制、gitignore/镜像/wheel 排除);现有套件回归基线先行
**Target Platform**: 调用方项目内任意 agent 运行时(Tier 1/2/3);引擎为 CLI 子进程形态,agent 中立
**Project Type**: 框架内技能增强(单仓;技能源 + 镜像 + 构建钩子 + 契约测试)
**Performance Goals**: N/A(本地文件读写,量级为单站点数十条记录)
**Constraints**: 引擎 stdlib-only;SKILL.md 保持契约级(细节进 references/,受 skill-shape 门约束);记录脱敏为写入时强制而非事后扫描
**Scale/Scope**: 1 个引擎 + 2 个 references + SKILL.md 路由段 + 3 处框架分发收口(.gitignore / sync-mirrors / hatch_build)+ 契约测试

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 需求 046 requirements.md(4 US / 10 FR / 5 SC)先行,本计划由其驱动 |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 048(clarify 裁定新建),feature-ref.md 记录映射 |
| III | Intent-Driven Development | ✅ Pass | FR 均为 WHAT/WHY;引擎 CLI 与文件格式为实现契约,不进需求层 |
| IV | Test-First & Contract-Driven Implementation (NON-NEGOTIABLE) | ✅ Pass | contracts/ 三份契约先行;tests/contract/test_browser_site_memory.py 覆盖状态机/脱敏/分发排除 |
| V | AI Agent Integration Standards | ✅ Pass | 分层判定纯能力导向(FR-001);记录格式 agent 中立,三 Tier 可读写(FR-009) |
| VI | Continuous Quality & Observability | ✅ Pass | 引擎 JSON 输出信封;状态变更历史附证据引用(FR-009);skill-shape 门约束 SKILL.md |
| VII | Specification-Plan-Task-Implementation Workflow (MANDATORY) | ✅ Pass | 本计划为标准流程 Phase 1 产物;tasks 由 /speckit.tasks 生成 |
| VIII | Code as the Single Source of Truth | ✅ Pass | 技能源 `skills/browser-utils/` 为唯一真源,镜像经 sync-mirrors 校验;site/ 排除分量同步进 MIRROR_PAIRS |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 零新增运行时依赖;引擎为 FR-009 程序优先的直接要求;复用 sync-mirrors/hatch_build/.gitignore 既有机制,无新子系统 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 机制细节进技能 references/(小写连字符),docs 树不动;docs-step 在 wrap-up 评估 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 记忆数据本地产出归调用方;技能自身即本仓可用资产,g.aliyun-inc.com 为首个真实 dogfood 场景 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用 scripts/js Playwright 运行器、scripts/bridge evaluate 通道(R1);引擎形态沿用 feedback/sanitize-utils 惯例(R4) |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 站点记忆 = Controlled Execution(固化流程)+ Learning Capture(留痕→蒸馏→验证飞轮)双维度强化 |

**Gates Status**: ✅ All gates pass

**Re-check after Phase 1**: 2026-08-24 — 设计产物(data-model / 3 contracts / quickstart / feature-ref)落盘后复核,13 项全 Pass,无 Complexity Tracking 条目;复核结论与原表一致,未引入新依赖或新子系统。

## Phase 0: Research Review

独立 `research.md` 已产出,五项结论全部进入设计:

- **R1 请求级方向已 PoC 验证**(页面上下文 fetch 继承会话;Tier 3 经既有 bridge evaluate 具备同等通道)→ 请求级方向不需要新建桥接设施,只需模式文档 + 记忆机制。
- **R2 hatchling `exclude` 对 force-include 不生效**(实证)→ wheel 排除落在 `src/hatch_build.py` 舞台拷贝,契约测试闭环验证。
- **R3 sync-mirrors `exclude_parts` 先例**(templates 对排除 commands)→ skills 对加 `"site"` 分量。
- **R4 引擎惯例**(stdlib-only / --action / JSON 信封)→ site-memory.py 沿用。
- **R5 复用面盘点** → scripts/js 运行器、bridge、三份既有 references 全部复用。

无遗留 NEEDS CLARIFICATION;技术上下文全部由实证与研究填充。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/046-browser-site-memory/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (R1 PoC / R2 hatchling 实证 / R3-R5 惯例与复用)
├── data-model.md        # Phase 1 output — 4 实体 + 状态机
├── quickstart.md        # Phase 1 output — 3 走查
├── contracts/           # Phase 1 output — 引擎 CLI / 文件格式 / 分发排除
├── feature-ref.md       # Phase 1 output — 需求 046 → Feature 048 映射
├── checklists/          # 需求质量检查清单(已存在)
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

### Source Code (repository root)

```text
skills/browser-utils/                      # 技能源(SKILL.md 加路由段;新增 scripts/site-memory.py、references/site-memory.md、references/request-level-patterns.md)
.specify/skills/browser-utils/             # 上述技能源的镜像(sync-mirrors skills 对,排除 site 分量后保持字节一致)
.gitignore                                 # 新增 skills/browser-utils/site/ 与 .specify/skills/browser-utils/site/ 排除
.specify/scripts/python/sync-mirrors.py    # skills 对 exclude_parts 增加 "site"(脚本源 scripts/python/ 同改)
scripts/python/sync-mirrors.py             # sync-mirrors 的源(strict 镜像对)
pyproject.toml                             # 移除 wheel force-include 静态 "skills" 行(移交构建钩子舞台拷贝)
src/hatch_build.py                         # initialize 增加 skills 舞台拷贝(剔除 site/ 分量)并注册 build_data force_include
tests/contract/test_browser_site_memory.py # 状态机/脱敏/格式契约测试(引擎 + formats 契约)
tests/contract/test_browser_site_exclusions.py # 分发排除三收口契约测试(framework-exclusions 契约)
```

**Structure Decision**: 扩展既有"框架源 + 镜像"布局——不改变任何顶层目录;技能能力增量落在技能自有目录(引擎进 `scripts/`,细节进 `references/`),框架级分发边界收口落在既有三处机制(.gitignore / sync-mirrors / hatch_build),契约测试落在 tests/contract/ 惯例位置。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `skills/browser-utils/SKILL.md` 及技能内新增/修改文件 | `.specify/skills/browser-utils/**`(site/ 除外) | `python3 .specify/scripts/python/sync-mirrors.py --check`(skills 对) |
| `scripts/python/sync-mirrors.py` | `.specify/scripts/python/sync-mirrors.py` | `diff -q`(strict 对)+ sync-mirrors --check 自举 |
| `.gitignore` / `pyproject.toml` / `src/hatch_build.py` / `tests/contract/test_browser_site_memory.py` | 无镜像(单一副本) | N/A |

## Complexity Tracking

N/A — Constitution Check 13 项全 Pass,无豁免条目。
