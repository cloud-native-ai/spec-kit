---
title: ".specify 机制归属对账表(判据对账)"
created: 2026-10-11
expires: 2026-12-10
status: draft
target: ""
tags: [criterion-reconcile, mechanism-audit, dot-specify]
---

# `.specify/` 机制归属对账表

> 服务 Goal `post-refactor-mechanism-integrity` 判据 1(权威定义:`.specify/goal/post-refactor-mechanism-integrity/goal.md`):`.specify/` 下除 `skills/` 外的所有目录与文件均有对应流程/脚本支撑,不存在无机制归属或来由不明的文件。本表为该判据的对账证据。

## 0. 方法与口径

- 枚举命令(实跑,repo root):`find .specify -maxdepth 2 -not -path "*/.work*" -not -path "*/specs/*" | sort`,再按需加深(`memory/`、`shared/`、`agents/` 等已逐一列深)。
- 排除口径:**`skills/` 整面排除**(判据原文「除 skills/ 外」;单列一行记账其归属与排除理由);**`specs/` 按派发口径单行覆盖**(特性流程领域,不逐文件);`.work/` 已被 find 排除(git-ignored 运行工作区,归 /speckit.team 运行面,记入 teams 行)。
- 证据形态:每行至少一个可定位证据(命令模板 / 引擎脚本 / CLI 调用点行号),行号为 2026-10-11 实读。

## 1. 对账表

全表 **33 行 = 32 有主 + 1 排除(`.specify/skills/`,判据原文「除 skills/ 外」)**;缺口为零。

| # | 目录/文件面 | 支撑机制(流程/命令/技能/引擎) | 证据(路径或调用点) | 判定 |
|---|---|---|---|---|
| 1 | `.specify/instructions.md` | `/speckit.instructions` 命令,经生成脚本产出 | `scripts/bash/generate-instructions.sh:29`(TARGET_FILE);命令模板 `templates/commands/instructions.md` | 有主 |
| 2 | `.specify/instructions.md-<时间戳>` 备份族(26 份) | 同一命令的带时间戳备份历史;根 `.gitignore` 持其排除 pattern | `scripts/bash/generate-instructions.sh:190,201,292` | 有主 |
| 3 | `.specify/skills.md` | `/speckit.instructions` create-if-absent(源 `.specify/templates/skills.md`,既有副本永不覆盖) | `templates/commands/instructions.md:112` | 有主 |
| 4 | `.specify/tools.md` | 同上(源 `.specify/templates/tools.md`) | `templates/commands/instructions.md:112` | 有主 |
| 5 | `.specify/tools/`(`system.json` / `shell.json` / `project.json`) | 工具发现清单(discovery inventories):`refresh-tools.sh` 引擎产出、canonical caller `generate-instructions.sh` 重定向写入,机器生成、禁手改;根 `.gitignore` 持排除 pattern(运行时生成物,不随 git) | `scripts/bash/refresh-tools.sh:60` + 根 `.gitignore:46` + `shared/definitions/tool-definitions.md:36` + `tests/contract/test_tools_inventory_ownership.py:38` | 有主 |
| 6 | `.specify/source.json` | CLI init 提交戳(feature 043:framework/commit/stamped_at) | `src/specify_cli/__init__.py:588-602` | 有主 |
| 7 | `.specify/gate.yaml` | 确认门机械写门:`gate-check.py` 引擎读取,`/speckit.implement` 消费;模板 `templates/gate-template.yaml` | `scripts/python/gate-check.py:45`(GATE_FILE)+ `templates/commands/implement.md:51` | 有主 |
| 8 | `.specify/.gitignore` | CLI 安装自 `templates/gitignore-specify-template` | `src/specify_cli/__init__.py:2357-2361` | 有主 |
| 9 | `.specify/memory/constitution.md` | `/speckit.constitution` | `templates/commands/constitution.md` + `templates/constitution-template.md` | 有主 |
| 10 | `.specify/memory/features.md` + `features/<NNN>.md`(54 份) | 特性集成工作流(索引手工维护,记录义务归该流程) | `.specify/shared/workflow/feature-integration.md` + `templates/feature-index-template.md` + `templates/feature-details-template.md` | 有主 |
| 11 | `.specify/memory/glossary.md` | 词汇协议流程 + glossary-utils 引擎 | `.specify/shared/workflow/glossary.md` + `scripts/python/glossary-utils.py` | 有主 |
| 12 | `.specify/memory/register.md` | ID 登记纪律(指令面携带并强制) | `templates/instructions-template.md:147` | 有主 |
| 13 | `.specify/memory/tools.md` | 手工维护的工具系统指南(refresh 脚本显式声明不产出它) | `scripts/bash/refresh-tools.sh:62` | 有主 |
| 14 | `.specify/memory/tools/<name>.md`(10 份) | `create-tools` / `improve-tools` 技能 + tools-utils 引擎 | `skills/internal/create-tools/SKILL.md` + `scripts/python/tools-utils.py` | 有主 |
| 15 | `.specify/memory/session/`(11 份 md) | memory-utils 短期存储 + run-determination 运行判定记录 | `scripts/python/memory-utils.py:10` + `scripts/python/run-determination.py` | 有主 |
| 16 | `.specify/memory/knowledge/`(7 份 md) | memory-utils 长期蒸馏存储 | `scripts/python/memory-utils.py:11` | 有主 |
| 17 | `.specify/memory/feedback/`(50 份 md) | feedback-utils 反馈库;`probe-map.md` 为 `--action map` 派生物(禁手编) | `scripts/python/feedback-utils.py:11` | 有主 |
| 18 | `.specify/memory/evidence/`(17 个 `ev-*` 运行目录 + `index.json`) | `collect-evidence` 技能(内部)+ evidence-utils 索引 | `scripts/python/evidence-utils.py:76`。**注**:并发外来会话(ev-20261011-132006-merge-skills,归因见 S2 报告 §6)正在写其中 `ev-20261011-132006-merge-skills/`,本对账未触碰 | 有主 |
| 19 | `.specify/memory/sanitize/`(findings.json + cleanup-plan.json) | sanitize-utils 引擎(`/speckit.sanitize`) | `scripts/python/sanitize-utils.py` | 有主 |
| 20 | `.specify/memory/trigger/`(index.json + telemetry.jsonl) | trigger-utils 引擎(建议流状态 + 遥测留存窗) | `scripts/python/trigger-utils.py` | 有主 |
| 21 | `.specify/goal/<slug>/`(5 个 goal.md + `summary/`) | `/speckit.goal` + goal-utils 引擎;summary/ 由阶段边界刷新 | `templates/commands/goal.md` + `scripts/python/goal-utils.py:55` | 有主 |
| 22 | `.specify/teams/<slug>/`(10 个 team.md + `.gitkeep`)+ `.work/` | `/speckit.team`;`.work/` 为 git-ignored 运行工作区;`.gitkeep` 由安装显式保留 | `templates/commands/team.md:23` + `src/specify_cli/__init__.py:2087` | 有主 |
| 23 | `.specify/specs/<ID>-<slug>/`(46 个特性目录) | 特性流程(`/speckit.specify`→plan→tasks→implement);目录由部署脚本建立 | `scripts/bash/create-new-requirements.sh:134`(SPECS_DIR) | 有主(单行覆盖,不逐文件) |
| 24 | `.specify/archive/spec/`(8 个归档特性) | `/speckit.sanitize` 的 `archive-spec` 处置位 | `scripts/python/sanitize-utils.py:51,60` | 有主 |
| 25 | `.specify/derive/`(`moves.md` + `rest-architecture/derive.md`) | `/speckit.derive` + derive-utils 引擎(变更档案与算子库) | `templates/commands/derive.md:155,171` + `scripts/python/derive-utils.py:57` | 有主 |
| 26 | `.specify/project/`(project.md + gantt/wbs/milestones 各 puml/svg/png) | `manage-project` 技能历史产物(dogfooding 基线)→ 该技能重构为 `summarize-project`,现为只读呈现的信息源 | `.specify/project/project.md` 头注(文件自述来由)+ `skills/internal/summarize-project/SKILL.md` | 有主(来由由文件头注显式声明) |
| 27 | `.specify/review/master-<branch>-<ts>.md` | `code-review` 技能归档报告 | `skills/internal/code-review/SKILL.md:62,83` | 有主 |
| 28 | `.specify/history/`(README.md + `.manifest.json` + `00-05` 主题文档) | `/speckit.history` 蒸馏 + history-utils 增量清单 | `templates/commands/history.md:87` + `scripts/python/history-utils.py:208-209` | 有主 |
| 29 | `.specify/scripts/`(bash 14 / python 22 / js 1) | CLI 安装自源 `scripts/`(resource 段拷贝;仓内两态见 AGENTS.md「Two Hats」) | `src/specify_cli/__init__.py:1512`(memory/scripts/templates/shared 段) | 有主 |
| 30 | `.specify/shared/`(constants 3 / definitions 10 / guidelines 15 / patterns 4 / workflow 14) | CLI 拷贝 shared 目录(源 `shared/`) | `src/specify_cli/__init__.py:2423-2432` | 有主 |
| 31 | `.specify/templates/`(21 文件;无 `commands/` 子目录) | CLI 安装模板投影(源 `templates/`);`commands/` 镜像已退役——退役清单与「不再随行」语义在 `_OBSOLETE_COMMANDS`/`_OBSOLETE_TEMPLATES`,现行命令副本归 `regen-command-copies.py` 四副本树 | `src/specify_cli/__init__.py:899-911,1118` + `scripts/python/regen-command-copies.py:5-6` | 有主(退役面零残留) |
| 32 | `.specify/agents/`(`templates/` + `instances/` + `execution/` + `.render-manifest.json`) | agent 三层 taxonomy:templates 由 sync-mirrors 投影(源 `agents/`)、instances/execution 项目本地、渲染清单由 CLI 写 | `.specify/shared/definitions/agent-definitions.md:11,40` + `src/specify_cli/__init__.py:547`(`_AGENT_MANIFEST_NAME`) | 有主 |
| 33 | `.specify/skills/`(17 external + `internal/` 15 + `.gitkeep`) | **判据显式排除面**;技能系统两层投影(sync-mirrors 层映射,源 `skills/{internal,external}`) | `scripts/python/sync-mirrors.py`。**注**:并发外来会话正在改 `merge-skills`(源 + 镜像),本对账未触碰(归因同 17 行) | 排除(判据原文「除 skills/ 外」) |

## 2. 缺口处置

**缺口为零**:上表共 **33 行**(32 行判定「有主」+ 1 行判据排除面),每行均携带至少一个可定位证据路径;未发现无机制归属或来由不明的目录/文件。

补充观察(非缺口,仅记账):

- 行 2 的 26 份备份为生成脚本的**有意备份历史**(非泄漏),根 `.gitignore` 已持排除 pattern;如需瘦身属清理动作,不属判据面。
- 行 26 的 `.specify/project/` 平铺图表形态是**旧版交付**(manage-project 时代),现技能 `summarize-project` 的交付目录为 `.specify/project/summary/` 形态;来由与现状由 `project.md` 头注自述,信息源角色不变,无需本轮处置;下次运行该技能自然刷新。
- 行 32 的 `execution/{configs,logs,scripts}` 当前为空目录,为 taxonomy 预留的执行层工件位(agent-definitions.md:11),非孤儿目录。

## 3. 并发会话边界

本轮对账窗口内,外来会话(ev-20261011-132006-merge-skills)在编辑 `skills/external/merge-skills/**`、其 `.specify/skills/` 镜像与 `.specify/memory/evidence/**`(归因与「非缺陷」裁定见 `.specify/teams/.work/post-refactor-mechanism-integrity/S2/verification.md` §6)。本对账对上述文件**只读、未触碰**;表内 18/33 两行已如实记账。

## 4. 验证记录

- 表成后自读复核:33 行逐行有证据列;总数与缺口声明一致(32 有主 / 1 排除 / 0 缺口;2026-10-11 返工重述,见文末返工记录)。
- 本 note 写面仅 `docs/notes/dot-specify-mechanism-reconciliation.md`;`git status --short -- docs/` 应只新增/变更本文件与 `consumer-upgrade-migration-plan.md`(见该文档 §3/§9 更新)。

## 返工记录(2026-10-11)

S3 交接验证门 REJECT 后的定点返工(独立验证者判定表仅两项 D1/N1,其余全绿;goal 判据本体经验证者自行重推导已通过,本轮仅修此两项、修完即停):

- **D1(缺行)**:顶层 `.specify/tools/`(实含 `system.json` / `shell.json` / `project.json`,`ls -A` 复核)原表缺行。已补为第 5 行,紧邻 `.specify/tools.md`(沿用表内伴随面相邻模式,同行 2 之于行 1)。四条证据均先实读、后引用:`scripts/bash/refresh-tools.sh:60`(canonical caller `generate-instructions.sh` 将引擎 stdout 重定向写入 `.specify/tools/{system,shell,project}.json`)、根 `.gitignore:46`(`.specify/tools/` 排除 pattern)、`shared/definitions/tool-definitions.md:36`(discovery inventories 机器生成、禁手改)、`tests/contract/test_tools_inventory_ownership.py:38`(`INVENTORIES` 常量)。判定「有主」。
- **N1(计数)**:`.specify/templates/` 行「22 文件」与实跑 `ls .specify/templates | wc -l` = **21** 不符(`ls -A` 同为 21,无隐藏件),已改 21;该行随补行移位为第 31 行。
- 计数整体重述:全表 **33 行 = 32 有主 + 1 排除(`skills/`)**;缺口仍为零。原第 5–32 行顺次移位为第 6–33 行;表内行号引用(§2 行 25→26、行 31→32;§3 17/32→18/33)已同步。
- 本轮 `docs/` 写面仍仅本 note;`consumer-upgrade-migration-plan.md` 本轮未触碰(其 §3/§9 为 S3 原轮已验证面),另写 `S3/manifest.md`(fix note + 异常行,原内容保留)。
