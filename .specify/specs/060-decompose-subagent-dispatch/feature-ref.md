# Feature Reference: 060 「驱动子代理」机制的技能化分解与公用化

**Feature ID**: 060 | **Feature Name**: 「驱动子代理」机制的技能化分解与公用化（decompose-subagent-dispatch）
**Requirement**: `.specify/specs/060-decompose-subagent-dispatch/requirements.md`（Requirement → Feature 绑定：本规格 ↔ Feature 060 自身，1:1）
**Status at plan time**: Draft → Planned（本 plan 落盘后推进）

## FR → 设计映射

| FR | 条款 | 主要设计落点 | 契约 |
|----|------|--------------|------|
| FR-001 | C-1/C-2/C-3 | agent-definitions.md 接线段（引用不复制） | concept-and-sources.md |
| FR-002 | C-7/C-8 | 层界三行判定 + 越层禁令 | concept-and-sources.md |
| FR-003 | C-9/C-10/C-11/C-14 | agents/sdd-executor.agent.md + 内容判据入 create-agent | skill-enhancements.md |
| FR-004 | C-12 | 多职责实例化说明（capacity-scope 引用） | skill-enhancements.md |
| FR-005 | C-12 | 一实例一职责 + 演进分流 | skill-enhancements.md |
| FR-006 | C-15/C-16, C-4 | 拓扑声明输入形态 + 冲突拒收 | skill-enhancements.md, concept-and-sources.md |
| FR-007 | C-21 | 既有模态/可见性/注入规则零改写 | skill-enhancements.md |
| FR-008 | C-19 | 配方引用不复制 | skill-enhancements.md |
| FR-009 | C-20, C-6, C-26 | 反嵌套上收为公用派发义务 | skill-enhancements.md 等 |
| FR-010 | C-29/C-32 | 两技能委派说明段（057 瘦身先例） | delegation-parity.md |
| FR-011 | C-35, C-34 | 义务平价映射 15 行下限 + 自足可加载 | delegation-parity.md |
| FR-012 | C-17/C-18, C-27/C-30/C-31 | 前置检查+处置链→run-agent；形态/配方→STR-006（Session 2026-10-16 裁定，plan 不重裁） | skill-enhancements.md, delegation-parity.md |
| FR-013 | C-2, C-28/C-29/C-31 | 编排本体保留清单 | concept-and-sources.md, delegation-parity.md |
| FR-014 | C-22/C-23 | 执行证据输入形态 + Self-Improvement 边界不动 | skill-enhancements.md |
| FR-015 | C-33, C-21 | 外部行为零变更（frontmatter/认领/team 体系零改动） | delegation-parity.md |
| FR-016 | C-13 | 退役规则（retired 保留、先解引用） | skill-enhancements.md |

## SC → 验证映射

| SC | 验证方式 | 证据落点 |
|----|----------|----------|
| SC-001 | 实例检索（capacity-scope 引用 + 复述零命中 grep） | verification.md（实现期） |
| SC-002 | 本地实跑 + 远端命令形态审计 + E1/E2 制品 diff 空 | verification.md |
| SC-003 | quickstart S2 三组检索复测（成组共现判据防误中） + P 表逐行对账 | quickstart S2 + contracts/delegation-parity.md P 节 |
| SC-004 | 端到端派发回传三条件 + 子代理输入反嵌套检索 | verification.md |
| SC-005 | pytest 全量 name-level 对比（基线：13 failed，均为 master 既有欠账——2026-10-16 实测） | verification.md |
| SC-006 | 三层词条 owner 检索（agent-definitions + subagent-definitions 之外零定义正文） | verification.md |

## 交付面清单（实现期按此对账）

```text
agents/sdd-executor.agent.md                                    # 新增：SDD 执行者能力模板（源）
skills/internal/create-agent/SKILL.md                           # 增强：内容判据 + 多职责实例化 + 退役生命周期
skills/internal/run-agent/SKILL.md                              # 增强：拓扑声明输入 + 冲突拒收 + 反嵌套义务 + 前置检查接线
skills/internal/run-agent/references/dispatch-preflight.md      # 新增：五族前置检查表 + 失败处置链（上收落点）
skills/internal/improve-agent/SKILL.md                          # 增强：执行证据输入形态
skills/external/sdd-loop-driver/SKILL.md                        # 委派化：Driver Topology 改引用+自检行、HR-6 同步
skills/external/sdd-loop-driver/references/dispatch-recipes.md  # 委派化：Preflight 清零引用、配方段坍缩引用
skills/external/sdd-loop-driver/references/stage-prompts.md     # 委派化：机制红线改引用（骨架内容保留）
skills/external/sdd-project-setup/references/setup-recipes.md   # 委派化：S4 检查表清零引用、远端形态引用
.specify/shared/definitions/agent-definitions.md                # 扩格：驱动子代理接线段 + 层界判定
.specify/shared/definitions/subagent-definitions.md             # 扩格：拓扑声明段 + 反嵌套引用
docs/reference/skills/sdd-loop-driver.md                        # 更新：委派化后的机制归属说明
docs/reference/skills/sdd-project-setup.md                      # 更新：同上
tests/contract/test_agent_dispatch_mechanism.py                 # 新增：S/A/R/I/X/D 条款契约测试
```

**不触碰**（C-33 边界）：`.specify/shared/workflow/external-dispatch-recipes.md`（配方正文零改动——已拥有"how"，不接收检查表）、`/speckit.team` 与 create-team 体系、各 `/speckit.*` 命令模板、两技能 frontmatter 与 probe-registry 认领。

## 基线记录（2026-10-16 实测，实现期相对判据的参照）

- sync-mirrors --check：skills/internal(135) / agents(2) / scripts(108) / shared(49) / skills(external↔flat) 全 ok；**既有漂移 1 条**：`.specify/templates/instructions-template.md` DIFF（与本特性无关，不属本特性修复面）
- regen-command-copies --check：OK
- compile-embeds --check：73 units, zero drift
- contract suite：2854 passed / 13 failed（名字级基线见 /speckit.requirements 前实测，全部为 master 既有欠账）
- 可见性计数：external 13 / internal 37（test_skill_layer_visibility_guards 钉住值）
