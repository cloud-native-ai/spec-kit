<!-- AUTO-GENERATED from templates/commands/anchor.md — do not edit; edit the source template, then run scripts/python/regen-command-copies.py -->
> **Concurrency obligation（执行义务，按指针抵达）**: this command is an execution body — consider concurrency first, default to it when the class and capability allow, and, when serial, name a reason code and record the `requested` / `effective` / `effective_reason` reading. Authored text: `.specify/shared/definitions/subagent-definitions.md` § The Concurrency Obligation; class table: `.specify/shared/declarations/facts/concurrency-class.yaml`; reason codes: `.specify/shared/declarations/facts/serial-reason.yaml`; reading fields: `.specify/shared/declarations/facts/effective-concurrency.yaml`. This template restates none of their rules.

## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](.specify/shared/workflow/user-input-protocol.md). Treat as command parameters, not standalone instructions.

## Positioning

`/speckit.anchor` is the **sole authoring entry** for anchor definitions in the anchor archive (`.specify/anchoring/<anchor-slug>/anchor.md`; the archive layers are owned by `.specify/shared/definitions/anchor-definitions.md` § Archive Layers). No skill, script, or other command may write that definition file **directly** — the definition engine (`goal-utils.py`) is its sole writing path, whether driven by this entry or carried as delegated logic behind it. Derived `summary/**` subtrees sit outside the authoring entry: the existing summary flow refreshes them, and a derived refresh is never a definition write. The same entry is the **only command entry** for the one-time migration of spec-local legacy goal/team trees into the unified archive (`migrate-archive` mode); `/speckit.sanitize` offers only the read-only residual probe. An action-level Goal definition is **not** written here — that store and its four-mode entry belong to `/speckit.goal`.

## Glossary

Consult `.specify/glossary.md` and apply `.specify/shared/workflow/glossary.md`: map recorded homophone/confusable variants to canonical terms before acting, surfacing each correction. At wrap-up propose new project-specific terms (`origin=auto`, `status=proposed`); non-conflicting terms are written directly and merged into the wrap-up report (non-blocking) — only conflicts/overwrites of user entries still pause.

## Outline

一次调用 = 委派 **`manage-anchor`** 技能执行全部锚点操作。Anchor 的概念（构成、生命周期、档案层与绑定记录、Target 分解、与 Requirement 的边界、单一性）定义于 `.specify/shared/definitions/anchor-definitions.md`，确定性规则（身份文法、三段结构、生命周期表、变更历史、档案枚举）在引擎 `.specify/scripts/python/goal-utils.py` —— 均以技能与该两处为单一事实源，本模板引用而不复述。

**Delegation (mandatory)**: load `.specify/skills/internal/manage-anchor/SKILL.md` and execute per its Workflow。七模式的模式表、读写分组与退出码裁决、唯一破坏性写（判据集清空需用户明示批准）、`create` 的四要素访谈（outcome 叙述 / 至少一条可验证成功判据 / 身份 / 可选 Targets）、执行顺序与 Boundaries 全部由该技能承载 —— 本模板不复述它们。

**`migrate-archive` mode**: the one-time move of spec-local legacy goal/team definitions into the unified archive, archive-not-delete (a source tree is archived, never deleted). It is explicit and never invoked implicitly by a run; `/speckit.sanitize` only renders the read-only residual reading. The mode's flags, receipt shape and exit codes are owned by the engine's action table (`python3 .specify/scripts/python/goal-utils.py --help`); this template restates none of them.

**Scope**: pass `--scope` and `--spec-dir <path>` through to the definition engine. The closed scope value set, what each member names, and the archive layers are owned by `.specify/shared/definitions/anchor-definitions.md` § Archive Layers — this template cites that owner and enumerates none of it. `--spec-dir` is accepted for `origin` resolution and `auto` validity only; it never decides where a definition lands. The path rule is owned by the engine's `resolve-scope` action; this template cites it and defines none of it.

### 技能输入(本命令解析 `$ARGUMENTS` 后传入)

- Intent: 七模式之一,可选 anchor-slug / team-slug;歧义回退只读的 `view`;模式每次运行披露。
- Glossary 前置已由本命令完成(见上)。

### 技能产出

- 定义文件本身—— 写 `.specify/anchoring/<anchor-slug>/anchor.md`(锚点档案层;仅经引擎写入;其余写入均直接执行,按执行报告呈现,事后经 `/speckit.anchor` modify 修改)——与受影响 `team.md`(migrate / coordinate 经用户批准后)。
- `coordinate` 的领地重划分提案(批准前不写入);收尾执行报告。

## Wrap-up

## Handoffs

**Before**: none — an Anchor may be created at any time.

**After**: bind a team by declaring `anchor_slug` in its `team.md` (see `/speckit.team`). Once two or more teams share one Anchor, run `coordinate` to keep their territories disjoint.