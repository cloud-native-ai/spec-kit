<!-- AUTO-GENERATED from templates/commands/sanitize.md — do not edit; edit the source template, then run scripts/python/regen-command-copies.py -->
## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](.specify/shared/workflow/user-input-protocol.md). Treat as command parameters, not standalone instructions. 可选参数:`--roots <csv>`(限定资料根子集,部分扫描不自动收敛)、`check`(仅检查,不进入清理提示)。

## Glossary

Consult the project glossary (`.specify/memory/glossary.md`) and apply the protocol in `.specify/shared/workflow/glossary.md`: correct recorded homophone/confusable variants before acting; propose new terms at wrap-up with user confirmation.

## Delegation

框架资料卫生治理的完整执行流:检测过期残留与冗余、运行确定性正确性检查、持久化 pending 发现,经用户确认后按两级判据清理并出具执行报告。整个七阶段流程(Preflight → Collect → Judge → Present → Confirm → Apply → Wrap-up)与行为红线均委派给一个 internal 技能;本命令只保留入口、参数解析与收尾生命周期。

- **Skill**: `sanitize-materials` — runtime path `.specify/skills/internal/sanitize-materials/SKILL.md`(引擎:`.specify/scripts/python/sanitize-utils.py`,发现 schema/合并语义/门控判据以引擎输出与 `--help` 为准)。
- **Inputs**: `$ARGUMENTS` 解析出的参数(见上;`--roots` 部分扫描不自动收敛,`check` 止于 Present 不进入 Confirm);glossary 锚定先行。
- **Outputs**: 发现台账与清理计划(`.specify/memory/sanitize/`);用户确认破坏性计划后为已执行清理 + 三要素执行报告(执行内容 / 变更工件 / 修改途径)。

## Feedback

At wrap-up (the same lifecycle point where this command prompts for a Git commit), run the feedback self-reflection step per the canonical convention in `.specify/shared/workflow/feedback-step.md`: agent self-reflection only — **never** solicit feedback content from the user; skip trivial or no-op runs; keep strictly to this command's scope; persist one entry via `feedback-utils.py --action record --unit-id "/speckit.sanitize" --unit-type command`. Non-blocking (非阻塞) and never any 自动传输 — delivery stays manual. That file owns every rule of this step — reflection, scope, dedup, persistence, the submission prompt, the abort and nesting clauses; do not restate any of them here.

## Documentation

At the same wrap-up point as the Feedback step, apply the docs-sync evaluation per the canonical convention in `.specify/shared/workflow/docs-step.md`: assess whether this run produced information needing entry into the documentation space, and conclude with exactly one of `需记录(目标文档 + 要点)` or `无需记录`. Never block wrap-up; incremental judgment only.

## Handoffs

**Before**: 无前置(手动按需运行)。

**After**: delegate 项按分诊建议移交 `/speckit.docs` / `/speckit.instructions` / sync-mirrors;台账 pending 项可留待下次运行收敛。