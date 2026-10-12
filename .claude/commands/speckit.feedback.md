<!-- AUTO-GENERATED from templates/commands/feedback.md — do not edit; edit the source template, then run scripts/python/regen-command-copies.py -->
## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](.specify/shared/workflow/user-input-protocol.md). Treat as command parameters, not standalone instructions. If empty, run the **Routing flow** below — the command inspects what has accumulated, judges where each item points, and picks the path itself, so no arguments and no keywords are needed. A non-empty argument MAY name a path explicitly (`package` / `打包` short-circuits to Path B), MAY carry an inventory filter (`--slice` / `--kind` / `--disposition` / `--since`), or MAY name a custom unit for probe injection. If the intent is ambiguous or unsupported, report the two paths and request the missing intent (do NOT guess silently).

## Glossary

Consult the project glossary (`.specify/memory/glossary.md`) and apply the protocol in `.specify/shared/workflow/glossary.md`: correct recorded homophone/confusable variants before acting; propose new terms at wrap-up with user confirmation.

## Outline

`/speckit.feedback` is the **single entry point** for every operation on the local feedback store. 一次调用 = 委派 **`manage-feedback`** 技能:技能读取存量、判断各条目指向(先判本仓帽子,再判 `kind`),自行路由到两条执行路径之一,并承载探针注入的显式请求能力 —— 本模板不复述任何路由或执行规则。

**Delegation (mandatory)**: load `.specify/skills/internal/manage-feedback/SKILL.md` and execute per its Routing flow and Behavior Rules, plus its two path references:

- `.specify/skills/internal/manage-feedback/SKILL.md` — 路由判定真源:意图识别(`package` 短路 / 探针注入 / 存量决定)、帽子判定(根级源目录判据,术语见 `.specify/shared/definitions/dogfooding-definitions.md`)、清单盘点(探针总览 + `.specify/memory/feedback/backlog.md` 路由积压)、分类与单向内容精化、双侧非空 / 空范围 / 不可判定条款、行为规则(零网络红线、exit 2 是裁决、路由判定须呈报)。
- `.specify/skills/internal/manage-feedback/references/path-a-digest.md` — **Path A 就地消化**:A1 入站包清点(重投 / 中断 / 孤儿识别)→ A2 抽取与大批量读纪律 → A3 自省(Introspection)→ A4 对账与渠道路由(含 backlog 写入)→ A5 原子清理与 consume-log → A6 本地条目 dispose。
- `.specify/skills/internal/manage-feedback/references/path-b-and-probe.md` — **Path B 打包上送**(status / 过滤汇总 / dispose / package / hat-aware 清理 / mark-submitted)与 **Probe Injection**(仅显式请求)。

引擎 = `.specify/scripts/python/feedback-utils.py`:机制(旗标校验、schema 检查、退出码、排除计数)归引擎,调用编排归技能;二者不一致时以引擎裁决为准。

## Feedback

At wrap-up (the same lifecycle point where this command prompts for a Git commit), run the feedback self-reflection step per the canonical convention in `.specify/shared/workflow/feedback-step.md`: agent self-reflection only — **never** solicit feedback content from the user; skip trivial or no-op runs; keep strictly to this command's scope; persist one entry via `feedback-utils.py --action record --unit-id "/speckit.feedback" --unit-type command`. Non-blocking (非阻塞) and never any 自动传输 — delivery stays manual. That file owns every rule of this step — reflection, scope, dedup, persistence, the submission prompt, the abort and nesting clauses; do not restate any of them here.

## Documentation

At the same wrap-up point as the Feedback step, apply the docs-sync evaluation per the canonical convention in `.specify/shared/workflow/docs-step.md`: assess whether information produced by this run (new capabilities, key decisions, structural changes) needs to be recorded into the project documentation space, and conclude with exactly one of `需记录（目标文档 + 要点）` or `无需记录`. Never block wrap-up; incremental judgment only (no full reconcile sweep); when a move/archive-level change is needed, recommend running `/speckit.docs` instead of executing it here.

## Handoffs

**Before**: none (any Spec Kit project; requires the probe registry installed by `/speckit.instructions`).

**After**: Path A → this project's own improvement channels (`improve-skills` / `improve-agent` / `improve-tools` / `improve-docs`), routed `/speckit.requirements` calls for new-feature findings, and `consume-log.md` recording the batch disposition. Path B → `mark-submitted` if not yet run for the batch, then manual delivery of the zip by the user. § Probe Injection → the client project's own improvement loop, which consumes `list --kind external` findings.