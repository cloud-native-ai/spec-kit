---
description: Author and manage project-level goal definitions — create, view, modify, manage Targets (scope slices), migrate a team's inline goal, and coordinate teams that share one goal.
short-description: 创建、查看、修改项目目标，并协调共享该目标的团队
argument-hint: "[create|view|modify|targets|migrate|coordinate] [goal-slug|team-slug]"
---

## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](.specify/shared/workflow/user-input-protocol.md). Treat as command parameters, not standalone instructions.

## Positioning

`/speckit.goal` is the **sole authoring entry** for project-level goal definitions. No skill, script, or other command may write into the goal archive **directly** — the goal engine (`goal-utils.py`) is its sole writing path, whether driven by this entry or carried as delegated logic behind it.

## Glossary

Consult `.specify/memory/glossary.md` and apply `.specify/shared/workflow/glossary.md`: map recorded homophone/confusable variants to canonical terms before acting, surfacing each correction. At wrap-up propose new project-specific terms (`origin=auto`, `status=proposed`); non-conflicting terms are written directly and merged into the wrap-up report (non-blocking) — only conflicts/overwrites of user entries still pause.

## Outline

一次调用 = 委派 **`manage-goal`** 技能执行全部目标操作。Goal 的概念(构成、生命周期、与 Requirement 的边界、判据权威性、单一定位、团队绑定)定义于 `.specify/shared/definitions/goal-definitions.md`,确定性规则(身份文法、三段结构、生命周期表、变更历史、档案枚举)在引擎 `scripts/python/goal-utils.py` —— 均以技能与该两处为单一事实源,本模板引用而不复述。

**Delegation (mandatory)**: load `.specify/skills/internal/manage-goal/SKILL.md` and execute per its Workflow。六模式(`create` / `view` / `modify` / `targets` / `migrate` / `coordinate`)的模式表、读写分组与退出码裁决、唯一破坏性写(`criteria --clear` 需用户明示批准)、`create` 四要素访谈、执行顺序与 Boundaries 全部由该技能承载。

### 技能输入(本命令解析 `$ARGUMENTS` 后传入)

- Intent:六模式之一,可选 goal-slug / team-slug;歧义回退只读的 `view`;模式每次运行披露。
- Glossary 前置已由本命令完成(见上)。

### 技能产出

- `.specify/goal/<goal-slug>/goal.md`(仅经引擎写入;其余写入均直接执行,按执行报告呈现,事后经 `/speckit.goal` modify 修改)与受影响 `team.md`(migrate / coordinate 经用户批准后)。
- `coordinate` 的领地重划分提案(批准前不写入);收尾执行报告。

## Feedback

At wrap-up (the same lifecycle point where this command prompts for a Git commit), run the feedback self-reflection step per the canonical convention in `.specify/shared/workflow/feedback-step.md`: agent self-reflection only — **never** solicit feedback content from the user; skip trivial or no-op runs; keep strictly to this command's scope; persist one entry via `feedback-utils.py --action record --unit-id "/speckit.goal" --unit-type command`. Non-blocking (非阻塞) and never any 自动传输 — delivery stays manual. That file owns every rule of this step — reflection, scope, dedup, persistence, the submission prompt, the abort and nesting clauses; do not restate any of them here.

## Documentation

At the same wrap-up point, apply the docs-sync evaluation per `.specify/shared/workflow/docs-step.md` and conclude with exactly one of `需记录（目标文档 + 要点）` or `无需记录`. Never block wrap-up.

## Handoffs

**Before**: none — a goal may be archived at any time, with or without teams.

**After**: bind a team by declaring `goal_slug` in its `team.md` (see `/speckit.team`). Once two or more teams share a goal, run `coordinate` to keep their territories disjoint.
