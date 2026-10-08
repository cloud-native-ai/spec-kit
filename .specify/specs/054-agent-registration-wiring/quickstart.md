# Quickstart — 054-agent-registration-wiring

三个场景,按使用频率排序。**逐示例执行披露**:本特性落地前,涉及新子命令与新流程步的示例**均不可执行**——每条此类示例自带「未实现」免责 + 前提清单(所依赖的旗标、形态、位置,供 /speckit.tasks 与 /speckit.implement 复测);今日已可执行的示例标注「实测」并粘贴真实输出。前提变更时以契约为准,不以本文措辞为准。

## Scenario 1: 建一个引用 stage 帧的团队,席位直达宿主注册面

**未实现**(依赖:`seat-instantiation.md` C-4..C-8 落地 + `render-trigger-cli.md` 子命令实现)。

步骤(实现后):

1. `/speckit.team create <slug> <goal>` —— 建队流程在 roster 步之后**自动**为每个引用 stage 帧的席位走 create-agent 委托实例化。前提:实例落 `.specify/agents/instances/<slug>.agent.md`,frontmatter 含 `team-scope: <team-slug>`,占位符全解析。
2. 建队流程终点**自动**执行渲染触发(对当前宿主工具)。前提:`specify render-agents --ai <tool>` 已实现,`--ai` 值为当前工具(qoder/claude/copilot/opencode 之一)。
3. 验证席位已上注册面。前提(以 qoder 为例):`ls .qoder/agents/` 含席位文件,frontmatter `name`/`tools`/`maxTurns` 由中性键渲染而来。

预期(实现后,依契约 seat-instantiation C-8):流程报告含 stats 摘要;数值以实跑为准,本文不预写。

## Scenario 2: 存量团队经一次 modify 补齐席位(opt-in 回填)

**未实现**(依赖:`modify-backfill.md` 落地 + 渲染命令实现)。

步骤(实现后):`/speckit.team modify <既有团队>` —— modify 流程对缺失席位补实例化并执行渲染触发;报告区分「既有席位 / 本次补齐席位 / 渲染 stats」。前提:未被 modify 触及的团队不受影响(FR-014);冲突披露不覆写。

## Scenario 3: 核验接线与镜像面(今日即可执行的部分)

**实测**(2026-10-08,本仓):

```text
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/ == .specify/skills/ (455 files)
ok    agents/ == .specify/agents/templates/ (2 files)
ok    scripts/ == .specify/scripts/ (107 files)
ok    shared/ == .specify/shared/ (46 files)
(exit 0)
```

实现后的核验(前提:守卫测试 `teaching-and-guards.md` C-4、C-9..C-11 已落地):

```text
$ python3 -m pytest tests/contract/ -k "agent_registration"   # 守卫名以 tasks 阶段定形为准
$ grep -rn "[[STR-001]]" templates/commands/ skills/create-agent/ .qoder/commands/ .claude/commands/ .github/prompts/ .opencode/command/
```

(`[[STR-001]]` 为引用形态——实际执行时以 spec Shared Strings 表中的 verbatim 值代入,连同 SKILL.md 的两条专属退役措辞一起检索。)

前提与预期:退役字面**今日**在 `templates/commands/agents.md:25`、`.qoder/commands/speckit.agents.md:19` 及 SKILL.md :122/:127 有命中(实测;源与副本同步携带);实现后 C-4 守卫断言零命中(该预期由契约测试钉住,非本文口头声明)。pytest 的 `-k` 选择串以 tasks 阶段实际落地的测试命名为准,本文不预写测试文件名。
