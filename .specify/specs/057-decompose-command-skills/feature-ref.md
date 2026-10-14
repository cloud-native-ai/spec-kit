# Feature Reference: 057-decompose-command-skills

**Bound Feature**: Feature 057 命令技能化分解补全
**Registry**: `.specify/memory/features.md` 行 057 · Detail: `.specify/memory/features/057.md`
**Spec**: `.specify/specs/057-decompose-command-skills/requirements.md`(Feature ID 057 于 clarify 2026-10-14 裁定新建)

## 本计划到 Feature 的映射

| FR 群 | 计划落点 | Feature 义务 |
|-------|----------|--------------|
| FR-001/002(两新 internal 技能 + 注册例外) | skills/internal/{run-skills,run-team}/SKILL.md;probe 注册表 2 行;templates/skills.md + .specify/skills.md 例外条目 | 技能分类标注约束侧:标注 + 配合 .specify 结构 |
| FR-003…008(run-skills 行为) | run-skills SKILL.md(解析/信任边界/执行/门控)+ contracts/run-skills-wiring.md C-1…C-12 | run 语义入口;尽力检测;降级路径 |
| FR-009…012(run-team 提取与平价) | run-team SKILL.md + team.md 瘦身 + contracts/run-team-parity.md P-1…P-10 | 命令只留入口与委派(goal T-003) |
| FR-013…015(接线核查与封口) | agents.md 核查(C-11)、skills.md 路由 5 行(C-10)、命令模板细节清零(C-5/C-6) | 不新建重复语义技能 |

## 状态推进记录

- **Draft**(2026-10-14,clarify):requirement 澄清完成,checker exit 0,注册表登记(0ed62af3)。
- **Planned**(2026-10-14,本命令):plan.md + Phase 1 产物落盘;Constitution Check 16 原则(IV Partial 已证成);推进依据 = 本文件与 plan.md § Feature Integration。
- Implemented 及以后:归 /speckit.implement(Pre-Status-Flip Gate)。

## 关联 Feature

- 013 Skills Command(skills 面)/ 019 Agents Command(agents 面)/ 027 Team Management(team 面)——被分解命令面的既有 Feature;本 Feature 承接跨面 run 语义补全,不改写其范围记录(反向交叉引用已在其详情文件)。
- Goal `command-logic-as-classified-skills`(T-001/T-003):本 Feature 是其在 agent/team/skills 面的落地实例。
