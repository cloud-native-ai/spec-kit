---
status: active
created: 2026-10-04
updated: 2026-10-05
---

# Goal: command-logic-as-classified-skills

## Objective

spec-kit 的命令核心逻辑尽可能由技能承载 —— 命令模板只保留入口与委派,可执行的核心逻辑落在 skills/ 下的技能里;每个技能的元数据都带 internal 或 external 标注,标注如实表达它与 spec-kit 的依赖关系(internal:只服务 spec-kit 框架自身逻辑;external:与 spec-kit 无依赖,任何项目皆可直接使用),使后续按标注分流的处理有据可依。

## Success Criteria

1. command 中只包含该调用哪些 skill 以及如何调用 skill,不包含具体的实现细节,所有的细节都在 skill 中

## Boundaries

- 不包含依据 internal / external 标注进行的任何差异化处理 —— 用户明示留待后续;本目标只到「标注存在于技能元数据中」为止。

## Targets

| ID | Target | Status |
|----|--------|--------|
| T-001 | 将逻辑和机制抽象成各种各样的技能,并且使用internal和external进行标注 | open |
| T-002 | 每个技能都有明确的名称,描述和触发定义,另外internal技能需要配合.specify目录结构, external技能不应该依赖.specify目录结构 | open |
| T-003 | templates/commands/*.md 中的命令进行更高层次的建模,他们只需要记录该调用哪些技能以及每个技能的输入和产出,所有的实现细节都落入技能中 | open |

## History

- 2026-10-04 — created.
- 2026-10-05 target T-001 added: 将逻辑和机制抽象成各种各样的技能,并且使用internal和external进行标注
- 2026-10-05 target T-002 added: 每个技能都有明确的名称,描述和触发定义,另外internal技能需要配合.specify目录结构, external技能不应该依赖.specify目录结构
- 2026-10-05 target T-003 added: templates/commands/*.md 中的命令进行更高层次的建模,他们只需要记录该调用哪些技能以及每个技能的输入和产出,所有的实现细节都落入技能中
- 2026-10-05 — criteria changed; prior value: None provided.
