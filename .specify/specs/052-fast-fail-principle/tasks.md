---
description: "Task list for Feature 052 — 快速失败纪律(Fast Fail)"
---

# Tasks: 快速失败纪律——异常分流而非静默兜底(Fast Fail)

**Requirement ID**: 052
**Requirement Key**: 052-fast-fail-principle
**Related Feature**: 052 快速失败纪律(Fast Fail)(`.specify/memory/features.md`,Status `Planned`)
**Input**: Design documents from `.specify/specs/052-fast-fail-principle/`
**Prerequisites**: plan.md ✓, requirements.md ✓(78 FR / 15 SC / 13 STR), research.md ✓(D-1…D-17), data-model.md ✓(21 实体 / 7 V / 3 S), contracts/ ✓(5 份 / 107 条), quickstart.md ✓(12 场景), feature-ref.md ✓

**Tests Mode**: **ON** — Constitution Principle **IV. Test-First & Contract-Driven Implementation**(`.specify/memory/constitution.md:54`)由确定性关键字扫描命中,故测试任务 MUST 先于对应实现任务。**同时适用 Principle VII 的 template-only 门**(`.specify/memory/constitution.md:98`:「features with no executable runtime code judge Test-First as Partial (justified) — "tests" verify template content, canonical paths, and structure instead」):本特性无可执行运行时代码,故产出的是**结构契约测试**(制品内容 / 标题 / 镜像一致性 / 计数钉子断言),**不是**单元或集成测试——后者无对象可跑。plan.md 的 Constitution Check 已据此把 Principle IV 记为 Partial。

**Organization**: 任务按用户故事分组。本特性是**文档治理类**,故采用 doc-feature 分类法(author-section → mirror-parity → render-verify → refresh-verify),不套用 models/services/endpoints。plan.md › Mirror Obligations 的**每一行**都由一个显式写入任务 + 一个显式核验任务覆盖;共享同一条扇出命令的行可共享写入任务(每阶段一条,不是每行一条),但核验任务 MUST 枚举它覆盖的行。

**测试文件的跨阶段认领(按命令规则显式分区)**:`tests/contract/test_fast_fail_discipline.py` 被 US1 / US5 / US6 三个阶段的核验行认领。为避免"同一文件在两个不同时间点被要求全绿"这一不可满足的对,**每个核验行只对自己点名的条款区间负责**,不声称整个文件转绿:

| 阶段 / 核验行 | 认领的条款区间 | 断言载体 |
|---|---|---|
| Phase 3(US1)· T011 | `discipline-doc.md` C-1…C-17, C-20, C-21(19 条) | `test_fast_fail_discipline.py` 的 `test_c1_*`…`test_c17_*`, `test_c20_*`, `test_c21_*` |
| Phase 4(US2)· T018 | `ambient-section.md` C-1…C-12, C-16…C-18(**15** 条) | 同文件的 `test_a1_*`…`test_a12_*`, `test_a16_*`…`test_a18_*` |
| Phase 5(US3)· T026 | `constitution-export.md` C-1…C-18(18 条) | 同文件的 `test_x1_*`…`test_x18_*` |
| Phase 6(US4)· T037 | `dispatch-injection.md` C-1…C-23, C-26(24 条)+ `ambient-section.md` **C-19**(1 条,共 **25** 条) | 同文件的 `test_i1_*`…`test_i23_*`, `test_i26_*`, `test_a19_*` |
| Phase 6(US4)· **T039** | `dispatch-injection.md` **C-24, C-25**(2 条) | **不由 pytest 承载**:二者是行为类条款(四条变异演练 + 演练取证与制品删净),由 T039 实跑取证到 `notes/red-first-evidence.md` |
| Phase 7(US5)· **T043** | `discipline-doc.md` **C-18, C-19**(2 条) | `test_fast_fail_discipline.py` 的 `test_c18_*`, `test_c19_*`(T042 实现,T043 核验转绿)。T043 的 `-k` 另含 `c20`,那是标记字面量落地后对 **C-20 的附带重跑**(其认领权仍属 Phase 3 的 T011),不构成第二处转绿时点 |
| Phase 8(US6)· T052 | `discipline-doc.md` C-22;`constitution-export.md` C-23;`ambient-section.md` C-13…C-15;`gate-neutrality.md` C-1…C-17(22 条) | `test_fast_fail_discipline.py` 的 `test_c22_*`, `test_x23_*`, `test_a13_*`…`test_a15_*`, `test_g1_*`…`test_g17_*` |
| Phase 8(US6)· **T048 + T049 + T052 + T053** | `constitution-export.md` **C-19…C-23**(5 条) | 跨纪律条款,断言载体分散三处:**C-19** 由 T048 在既有 `test_user_facing_comprehension_doc.py` 新增的类 ⑪ 行断言承载;**C-20** 由 T048 的钉子上调(8→9)承载;**C-21** 由既有 `test_c18a` 承载(T048 核验其仍绿);**C-22** 的四处留痕由 T049 核验;**C-23** 由 T050 在 `test_fast_fail_discipline.py` 新增断言承载,并经 T052 的 `-k` 区间转绿;C-19/C-21 另由 T053 的 quickstart 场景 9 实跑复核 |

**覆盖完整性(生成时机械核算,非声明)**:五份契约共 **107** 条条款;上述核验行认领的条款集合,其**认领权两两不相交**(唯一的交集是 T043 对 C-20 的附带重跑,认领权仍属 T011,已在表中标注),并集为 **107 / 107**,无遗漏、无重复认领、无指向不存在条款的记号。该核算由生成期的机械扫描得出(初版曾漏 `x20`/`x23` 两条并把 C-20 的附带重跑误计为相交,已订正——这正是 DoD-12 与 T058 要治的形态)。Phase 9 的 **T059** 在实现期复核这一核算(命令要求:标记任何在两个核验行中出现、却指向不同转绿时点的测试路径)。

**同一测试文件被多行认领的处置**:`test_fast_fail_discipline.py` 被 T011 / T018 / T026 / T037 / T043 / T052 六行认领,故每行的 `pytest -k` 表达式**只列自己区间的函数**,且 MUST NOT 声称"该文件全绿"——只有 Phase 9 的 GATE-5 才对整个文件作全绿断言。

**⚠️ `-k` token 的尾下划线是载荷性的(实现期实测订正,2026-09-23)**:`pytest -k` 的每个 token 按**子串**匹配测试 id,故裸 `c1` 会同时命中 `test_c10_*`…`test_c19_*`,裸 `c2` 会命中 `test_c20_*`…`test_c22_*`。实测(5 个桩函数 `test_c1_a` / `test_c2_e` / `test_c10_b` / `test_c18_c` / `test_c22_d`):`-k "c1 or c2"` 收集到 **5** 个,`-k "c1_ or c2_"` 收集到 **2** 个。原六行 `-k` 表达式因此会**越界选中后续阶段的条款**——而 T011 / T018 / T026 明确要求 C-18/C-19/C-22、A-13…A-15、X-19…X-23 在各自时点**仍为红**,越界即核验行自身失败。六行已全部改为带尾下划线的 token(机械替换,已复核零残留裸 token)。

⇒ **对 T003 的硬约束**:测试函数名 MUST 形如 `test_<前缀><N>_<描述>`——编号后**紧跟一个下划线**。`test_c1a_guard` 这类形态会使 `c1_` token 失配,从而让对应核验行**空选并恒绿**(一次盲检:命令返回 0,但其输出并不关于它被写来判定的命题)。MUST NOT 为了"整洁"把 `-k` 里的尾下划线去掉。每个核验行 MUST 顺带断言其 `-k` 的**收集数等于该区间条款数**(非零且不相差),否则空选不可被发现。

## Definition of Done (DoD)

- DoD-1: `shared/guidelines/fast-fail.md` 落地,9 个 H2 节齐备,与 `.specify/` 镜像逐字节相等
- DoD-2: `templates/instructions-template.md` 含 `## Fast Fail Discipline` 且位置满足 Token Efficiency < UFC < Fast Fail < Dogfooding 的严格排序;`.specify/instructions.md` 已再生;4 条兼容性符号链接仍为符号链接
- DoD-3: 宪章双落点齐备(模板原则 XIV + 命令 `MUST include` 第 8 条),活动宪章原则 XVI + 版本 1.13.0 + Sync Impact Report,四个既有钉子同批上调为 14 / 16 / 8 / (1,13)
- DoD-4: 注入子句以成对定界符落在真源文档,2 份出厂 Agent 预设 + 团队 Per-Agent Payload 第六字段行 + 两处制作者要求全部就位,副本与拥有者逐字节相等
- DoD-5: `tests/contract/test_fast_fail_discipline.py` 全绿,且既有 `test_constitution_double_landing.py` / `test_user_facing_comprehension_doc.py` / `test_user_facing_comprehension_section.py` / `test_proactive_trigger_section.py` / `test_instructions_section_propagation.py` 全部仍绿
- DoD-6: 门控扫描实跑 `total` 与冻结基线**相等**(23)、`violations` 为 0、`scan-confirmation-gates.py` 与其余五个引擎/脚本 `git diff` 为空
- DoD-7: 镜像判据为**相对**形态且取**集合包含**(不是相等)——`sync-mirrors.py --check` 对 `shared` / `templates` / `skills` 三个 scope 的 DIFF 集合改后 MUST 是 T001 冻结集的**子集**(减少是改善,新增才是漂移);`--only agents` 仍为 `ok`
- DoD-8: 全量契约套件相对冻结的名字级基线**零新增失败**(`comm -13 baseline current` 输出为空)
- DoD-9: `quickstart.md` 的 12 个场景全部实跑,输出追加进 `notes/quickstart-run.md`;4 条变异演练取证齐全且演练制品计数归零
- DoD-10: 类 ⑪ 登记与 C-14 钉子 8→9 落地,且在 plan.md › Feature List Review、feature-ref.md、`features/051.md`、`features/052.md` 四处留痕
- DoD-11: `verification.md` 逐条给出 SC-001…SC-015 的状态;不可得者记 `[~]` 并说明理由,MUST NOT 编造通过率
- DoD-12: 本文件印出的**每一条派生命令都被实跑过**,其数值取自实跑输出(T046 复核);两处双重枚举(封闭处置集、子句长度上限)在各制品间锁步一致(T044 复核)

**DoD Status**: pending

## Completion Gate

每项 MUST 由 `/speckit.implement` 对着**当前树**重跑其检查命令并读输出后才算满足;全部任务 `[X]` 本身不被信任。

- GATE-1: 契约套件零新增失败 — check: `bash scripts/bash/run-tests.sh --names-out .specify/specs/052-fast-fail-principle/current-failed.txt` 后 `comm -13 .specify/specs/052-fast-fail-principle/baseline-failed.txt .specify/specs/052-fast-fail-principle/current-failed.txt` 输出为空
- GATE-2: 门控预算中立(**相等判据 MUST 直接比较,MUST NOT 依赖 `--baseline` 的退出码**)— check: 执行 `quickstart.md` 场景 4 第二段的可跑脚本——它从 `.specify/specs/050-proactive-flow-trigger/baseline-gates.json` 的 `confirmationGates.total` 取 `frozen`,从 `scan-confirmation-gates.py --json` 取 `payload`,断言 `payload["total"] == frozen` 且 `len(payload["violations"]) == 0` 并输出 `TOTAL-EQUAL`;并另跑 `python3 scripts/python/scan-confirmation-gates.py | head -1` 断言输出 `blocking confirmation gates: 23`。 ⚠️ **`--baseline` 旗标不可用作相等判据(实现期变异演练实证)**:① 它读基线文件的**顶层** `total` 键,而 050 基线把该值嵌在 `confirmationGates` 下,故 `baseline delta total` 恒为 `+23`(与 0 相比);② 其退出码为 `if args.baseline and violations: return 2`,**只反映 violations、完全不反映 total**。演练:把冻结值改为 99 后 `--baseline` 仍 `EXIT=0`,而直接比较正确变红。这两个缺陷属上游(`scripts/` 在零改动面内,GATE-3 机械核验),MUST 单独上报,MUST NOT 改写扫描器
- GATE-3: 引擎与脚本零改动 — check: `git diff --stat -- scripts/ src/specify_cli/ skills/create-team/scripts/ templates/plan-template.md` 输出为空
- GATE-4: 镜像相对判据(**集合包含**形态,MUST NOT 写成相等)— check: 对 `shared` / `templates` / `skills` / `agents` 四个 scope 各跑 `python3 scripts/python/sync-mirrors.py --check --only <scope>`,其 `DIFF` 集合 MUST 是 T001 冻结集的**子集**(减少是改善,新增才是漂移);`--only agents` MUST 输出含 `ok`。⚠️ 原写法是"`--only shared` 的 DIFF 行数等于 2",实现期证伪:`sync-mirrors.py --write --only shared` 会同步**整个 scope**,连带治好该 scope 的既有漂移(实测 2 → 0),于是"漂移变少"反而使相等判据失败。判据的意图是"无新增",故 MUST 用子集形态
- GATE-5: 新守卫与全部被上调/被钉住的既有守卫全绿 — check: `python3 -m pytest tests/contract/test_fast_fail_discipline.py tests/contract/test_constitution_double_landing.py tests/contract/test_user_facing_comprehension_doc.py tests/contract/test_user_facing_comprehension_section.py tests/contract/test_proactive_trigger_section.py tests/contract/test_instructions_section_propagation.py tests/contract/test_confirmation_gates_sweep.py -q`(末项是实现期补入的第三处 `total` 钉子,见 `contracts/gate-neutrality.md` C-10 第三行)
- GATE-6: 真源文档与镜像逐字节相等 — check: `cmp shared/guidelines/fast-fail.md .specify/shared/guidelines/fast-fail.md && echo BYTE-IDENTICAL`
- GATE-7: 无残留未完成任务 — check: `grep -cE '^- \[[ >]\]' .specify/specs/052-fast-fail-principle/tasks.md` 返回 0
- GATE-8: verification.md 覆盖全部 SC — check: `for n in $(seq -w 1 15); do grep -q "SC-0$n\|SC-$n" .specify/specs/052-fast-fail-principle/verification.md || echo "MISSING SC-$n"; done` 输出为空
- GATE-9: 结构校验器通过 — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/052-fast-fail-principle/tasks.md; echo EXIT=$?` 期望 `EXIT=0`

## Environment Prerequisites

本节是所有探测结论的**唯一落点**(2026-09-23 本轮生成时实测,不跨会话缓存)。各阶段的前置说明与 `[~]` 备注 MUST 引用本节,MUST NOT 复述结论。

- python3 / pytest: **available** — probe: `python3 --version` → `Python 3.11.11`;`python3 -c "import pytest;print(pytest.__version__)"` → `8.4.2` @ 2026-09-23;affected: 全部阶段
- bash / git / cmp / awk / sed / grep / comm: **available** — probe: `command -v` 逐个 @ 2026-09-23( GNU bash 4.4.20 / git 2.43.5 / diffutils 3.6 / GNU Awk 4.2.1 / GNU sed 4.5 / GNU grep 3.1 / coreutils 8.30);affected: 全部阶段
- 本项目的六个引擎与脚本: **available 且支持本清单引用的全部旗标** — probe: `run-tests.sh` 支持 `--names-out`(`:22,:29`)、`sync-mirrors.py` 支持 `--only PATH`、`regen-command-copies.py` 支持 `--check`、`scan-confirmation-gates.py` 支持 `--baseline`(`:154`)、`validate-tasks.py` 与 `feedback-utils.py` 存在 @ 2026-09-23;affected: GATE-1…GATE-9、T001、T019、T028
- 容器运行时 / 可拉取镜像 / 活动集群 / 网络: **not required** — 本特性只改文档制品与测试,无构建或冒烟目标;`docker` 虽 present 但无任何任务依赖它 @ 2026-09-23;affected: none
- `specify` CLI 的下游 bootstrap 演练: **partial** — 本机 `specify` 为 site-packages 下的非可编辑安装,`specify init` 渲染的是安装包模板而非本树(Feature 051 的 T034 已记录同一限制,其 `features/051.md` 记为 `[~]`)。故本清单**不含**下游 bootstrap 场景;FR-033 的"下游 plan 门控自动多一行"由 T020 的机械核验(渲染枚举逻辑并数行)承担,不依赖真实 init @ 2026-09-23;affected: T020
- **跨制品环境断言核对**(命令要求):已 grep 本特性的兄弟制品,无与上述探测矛盾的陈旧环境声明;`quickstart.md` 的 25 行改前基线于 2026-09-23 全部复现(委托复核 22 条命令覆盖 25 行,零冲突)

## 生成时前提重测(Premise verification)

任务行内嵌的一切计数前提于**本轮生成时**重测,重测命令与结果如下(命令一并印出,使实现者能复跑而不是信任数字):

| 前提 | 重测命令 | 实测值 |
|---|---|---|
| `shared/guidelines/` 份数 | `ls -1 shared/guidelines/*.md \| wc -l` | **12** → 改后 13 |
| `fast-fail.md` 是否已存在 | `test -f shared/guidelines/fast-fail.md && echo yes` | **no**(待创建) |
| 指令模板 / 活动文件 `## ` 节数 | `grep -c '^## ' <file>` | **18 / 19** → 改后 19 / 20 |
| 三个锚点章节行号 | `grep -n '^## Token Efficiency Discipline\|^## User-Facing Comprehension\|^## Dogfooding Practice' templates/instructions-template.md` | **66 / 74 / 86** |
| 宪章模板 / 活动宪章原则数 | `grep -c '^### [IVX]*\. ' <file>` | **13 / 15** → 改后 14 / 16 |
| 命令 `MUST include` 条目数 | `grep -c 'MUST include' templates/commands/constitution.md` | **7** → 改后 8 |
| 活动宪章版本 | `grep -oP '^\*\*Version\*\*: \K[0-9.]+' .specify/memory/constitution.md` | **1.12.0** → 改后 1.13.0。⚠️ MUST 用锚定 `^\*\*Version\*\*` 的形态:裸 `grep -o '1\.[0-9]*\.[0-9]*' \| head -1` 会命中 Sync Impact Report 的 `Version change: 1.11.0 →` 行而得 **1.11.0**(本轮实测踩过) |
| 出厂 Agent 预设份数 | `ls -1 agents/*.agent.md \| wc -l` | **2** |
| Per-Agent Payload 字段行数 | `awk '/^Per-Agent Payload:/,/^Context Isolation Rules:/' skills/create-team/references/patterns.md \| grep -c '^| \`'` | **5** → 改后 6 |
| UFC 类表去重规则真源路径数 | 按**规则真源列**解析(口径同 `test_user_facing_comprehension_doc.py:394-397`) | **8** → 改后 9。⚠️ 按整行解析得 9(改前)/10(改后),口径不可混用;8 个路径已逐个 `is_file()` 核验存在(pin hygiene 规则 2) |
| 门控扫描 total / BLOCKING_PATTERNS / POLICY_DOCS | `python3 scripts/python/scan-confirmation-gates.py`;importlib 载入取真 | **23 / 17 / 2** |
| 双落点四钉 | `grep -oE '(TEMPLATE_COUNT\|LIVE_COUNT\|COMMAND_COUNT) = [0-9]+\|MIN_VERSION = \([0-9, ]+\)' tests/contract/test_constitution_double_landing.py` | **13 / 15 / 7 / (1, 12)** → 改后 14 / 16 / 8 / (1, 13) |
| UFC C-14 / C-18a 钉子 | `grep -o 'len(deduped) == [0-9]*' …doc.py`;`grep -o '<= 2' …doc.py` | **8** → 改后 9;override 上限 **2**(不受本特性影响,类 ⑪ 的该列为 `—`) |
| 按工具命令树 / agent 树 | `ls -1 <dir> \| wc -l` | 命令树 4 × **25**;agent 树 `.claude`=2 `.qoder`=2 `.github`=2 `.opencode`=**0** |
| 指令兼容性符号链接 | `test -L <f>` | **4** 条(AGENTS.md / CLAUDE.md / QODER.md / .github/copilot-instructions.md) |
| 活动指令文件字节 / 预算 | `wc -c < .specify/instructions.md`;`generate-instructions.sh:38` | **28168 / 32768**(余量 4600) |
| 镜像基线(`--only shared` / `--only agents`) | `python3 scripts/python/sync-mirrors.py --check --only shared` | **恰 2 条 DIFF**(`feedback-step.md`、`runtime-mode.md`),EXIT=2;agents 为 `ok (2 files)` |
| 规格与契约规模 | `grep -c` 系列 | FR **78** / SC **15** / STR **13**;条款 **107**;quickstart 场景 **12**(`grep -c '^## 场景 [0-9]'`,MUST 带 `[0-9]`,否则匹配 `## 场景覆盖表` 得 13);data-model E **19** / V **7** / S **3** |

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行(**不同文件**、无未完成依赖)。同一文件上的任务 MUST NOT 标 `[P]`——本特性大量任务编辑同一份真源文档,故 `[P]` 只出现在跨文件处。
- **[Story]**: US1…US6,仅用户故事阶段的任务携带;Setup / Foundational / Polish 阶段 MUST 零 `[US` 标记。
- **[blockedBy: Txxx,Tyyy]**: 显式依赖,列出的任务全部 `[X]` 之前 MUST NOT 开工。
- 任务状态 sigil:`[ ]` 未开始 · `[>]` 已认领(多代理) · `[X]` 已完成 · `[~]` 已移交(理由记入 `verification.md` 的 `deferred_tasks=`)。

## Path Conventions

代码生成器/框架形态:`shared/`(纪律真源)、`templates/`(模板与命令)、`skills/`、`agents/`、`tests/contract/`、`scripts/`(**本特性零改动**)、`src/specify_cli/`(**零改动**)。`.specify/` 与四棵按工具树**一律由引擎再生,MUST NOT 手改**。

---

## Phase 1: Setup(基线冻结)

**目的**: 把本特性所有比对型门禁的基线在开工前一次冻结,承 Feature 049/050/051 的惯例(它们都由各自 T001 承担)。基线冻结 MUST 先于任何编辑,否则"改前/改后"无从比较。

- [X] T001 冻结四组基线到 `.specify/specs/052-fast-fail-principle/notes/pre-change-measurements.md`:① `BASE_SHA=$(git rev-parse HEAD)` 的字面值(不写 `HEAD`,CI 洁净检出下 `git diff HEAD` 恒空真);② 镜像既有漂移集(`sync-mirrors.py --check --only shared|agents|templates|skills` 的逐对输出);③ 结构实测值(上文"生成时前提重测"表的每一行,连同其命令);④ 门控基线(total 23 / BLOCKING_PATTERNS 17 / POLICY_DOCS 2 / 四钉 13·15·7·(1,12) / UFC C-14 8)
- [X] T002 [blockedBy: T001] 冻结名字级测试基线:`bash scripts/bash/run-tests.sh --names-out .specify/specs/052-fast-fail-principle/baseline-failed.txt`,并在 `notes/pre-change-measurements.md` 记录该文件的行数与"判据是 `comm -13` 输出为空,不是失败条数相等"这一口径(名字级基线:条数相等时失败集合仍可能已换手)

## Phase 2: Foundational(阻塞性前置)

**目的**: 先建守卫骨架并取 red-first 证据,使后续每个阶段的"转绿"都有意义。本阶段 MUST 在全部用户故事之前完成。

- [X] T003 [blockedBy: T002] 创建 `tests/contract/test_fast_fail_discipline.py`:模块常量区(`ROOT = Path(__file__).resolve().parents[2]`、`DOC`、`DOC_MIRROR`、`INSTR`、`INSTR_LIVE`、`DOC_NAME = "fast-fail.md"`、`AMBIENT_HEADING = "## Fast Fail Discipline"`、`AMBIENT_POINTER = ".specify/shared/guidelines/fast-fail.md"`、`SECTION_HEADINGS` 九元组、`FORBIDDEN_NAMES` 四元组、`MARKER_OBS/MARKER_CLAUSE/MARKER_RETURN/MARKER_CLEAN` 四个字面量常量、`CLAUSE_BEGIN/CLAUSE_END` 定界符常量、以 importlib 载入 `scripts/python/scan-confirmation-gates.py` 取 `BLOCKING_RE`),并实现 `test_c20_marker_literals_are_mutually_disjoint`(纯字符串运算,**red-first 期即可绿**)+ 其余条款的函数骨架(每个以 `_text(<该条款主制品>)` 起头,使缺失制品报 FileNotFoundError 而不是断言写错;制品已存在者由第二行 `_unimplemented()` 显式失败,故**骨架永不绿**)。〔实现期订正:原行写的常量名是 `INSTR_MIRROR`,已改为 `INSTR_LIVE` —— `.specify/instructions.md` 由 `generate-instructions.sh` **再生**而非镜像同步(D-17 / FR-077 的实测依据),把它叫 mirror 正是本特性要纠正的那个假承诺,守卫的词汇 MUST NOT 编码它〕
- [X] T004 [blockedBy: T003] 取 red-first 证据到 `.specify/specs/052-fast-fail-principle/notes/red-first-evidence.md`:实跑 `python3 -m pytest tests/contract/test_fast_fail_discipline.py -q`,记录 failed/passed 计数并**逐条分类失败原因**(制品缺失 / 标题不存在 / 断言不成立),并对**改前即绿**的条款逐条写明为何绿(否则执行者会据"红的才正常"去削弱一个本来正确的断言——Feature 051 的 B-12 教训)

## Phase 3: User Story 1 - 执行中发现异常时按可判定判据分流 (Priority: P1) 🎯 MVP

**Story Goal**: 真源文档落地,携二值分流判据、机械测试、爆炸半径可判定定义、以及两份封闭清单(其条目取自本仓已实测失效),使"顺手修复 vs 快速失败"成为可复现的判定而非印象。

**Independent Test**: 只完成本阶段即可独立验收——`shared/guidelines/fast-fail.md` 存在且镜像逐字节相等;9 个 H2 节齐备;`discipline-doc.md` C-1…C-17、C-20、C-21 转绿;`quickstart.md` 场景 1 与场景 7 的改后判据可实跑。不依赖常驻章节、宪章导出、派发注入或生长闭环。

### Tests for User Story 1

- [X] T005 [US1] [blockedBy: T004] 在 `tests/contract/test_fast_fail_discipline.py` 中实现 `discipline-doc.md` C-1…C-17、C-21 的断言体(存在性、镜像字节相等、改名守卫 + 其反空真哨兵、前 8 行所有权三要素、前 20 行失效陈述双侧覆盖、canonical 指针行恰好一行且声明类 ⑪、9 节封闭元组、RFC-2119 关键词、双语 H1、判据节七项((a)…(g),其中 (f) 上送极优先与 (g) 两振升级 MUST 各自独立可定位且 MUST NOT 与 (d) 的"判据优先于清单命中"共用一处文本、(g) MUST 断言 `(发现点, 被证伪的预期)` 认定键在场)、爆炸半径可判定定义、STR-006 与两条手法援引、两份清单条目语法与封闭性、FF-2…FF-8 七项逐项可定位 + 其反空真哨兵、委托而非复制、上送件四要素与封闭处置集与类 ⑪ 归属与 STR-013 与粒度引用、项目中立);本行**只对该区间负责**,C-18/C-19/C-22 属后续阶段

### Implementation for User Story 1

- [X] T006 [US1] [blockedBy: T005] 创建 `shared/guidelines/fast-fail.md` 的骨架:双语 H1(含 `快速失败` 与 `Fast Fail`)、前 8 行所有权三要素(owns 什么 / `templates/instructions-template.md` 的 `## Fast Fail Discipline` 章节以指针引用 / 消费者 MUST 引用而 MUST NOT 复制)、前 20 行失效陈述(点名**静默兜底**并覆盖"就地修平+用户看不见"与"下游当已验证前提引用"两侧)、头部所有权区恰好一行 canonical 指针(指向 `.specify/shared/guidelines/user-facing-comprehension.md`、括号内声明覆盖界面类 ⑪、MUST NOT 落在任何判据节内部),以及**全部 9 个 H2 节标题**(节名逐字取 `discipline-doc.md` C-7 的封闭元组,使 C-7 在本阶段即可绿)
- [X] T007 [US1] [blockedBy: T006] 填写 `shared/guidelines/fast-fail.md` 的 `## 分流判据` 节:二值判据(纠正 vs 裁定,无第三值、无"尽量少停"中间档)、FR-010 的四条必要条件、机械测试 STR-005 与 STR-006 各恰好一次、FR-070 的"判据优先于清单命中"顺序声明、FR-012 存疑从严(以路径指称 `shared/guidelines/confirmation-gates.md`,MUST NOT 写其中文名)、FR-013 上送极优先、FR-014 两振升级、以及 FR-073 的爆炸半径可判定定义(集合包含判定:本次修复触及的工件集合是否超出当前动作的声明范围;声明范围来源按 territory → plan 源码树/镜像义务行 → 命令产出声明 的优先级,皆无则为当前文件)
- [X] T008 [US1] [blockedBy: T007] 填写 `shared/guidelines/fast-fail.md` 的 `## Fast Fail List(快速失败清单)` 与 `## In-Passing Repair List(顺手修复清单)` 两节:标题字面量逐字取 STR-011 与 STR-012(**唯一拥有者是 `requirements.md` 的 Shared Strings 表**;`discipline-doc.md` C-7 的封闭元组与 `research.md` D-10 已于实现期订正为引用该拥有者,三者 MUST 逐字一致,T003 的 `SECTION_HEADINGS` 常量据此取值);条目语法固定为 `- **FF-n <类名>** — 判据:<一句> | 实证:<路径或小节>`(修复侧用 `RP-n`);FF 侧 ≥9 条且 `FF-2`…`FF-5` 逐条对应盲检四成因、`FF-6`…`FF-8` 逐条对应 `git diff` 三形态,实证列以路径引用 `docs/reference/history/00-cross-cutting-lessons.md` 的对应小节而 MUST NOT 复述其正文;RP 侧 ≥6 条;两节各声明封闭性(扩展只经修订本文档);"仅不可撤销动作方可通过"一条以路径委托门控治理纪律
- [X] T009 [US1] [blockedBy: T008] 填写 `shared/guidelines/fast-fail.md` 的 `## 上送件与披露` 节:四要素、封闭处置集四项(`按建议处置` / `改为顺手修复并继续` / `照原样继续` / `终止本次运行`,并声明扩展只经修订本文档)、界面类归属 ⑪ 失败如实报告(并写明排除 ① 的实质理由)、干净运行显式陈述义务(含 STR-013 字面量)、以指针引用执行报告的粒度规则而不复述其三要素
- [X] T010 [US1] [blockedBy: T009] 同步镜像并核验:`python3 scripts/python/sync-mirrors.py --write --only shared`,随后 `cmp shared/guidelines/fast-fail.md .specify/shared/guidelines/fast-fail.md && echo BYTE-IDENTICAL`;并核验 `--check --only shared` 的 DIFF 集是 T001 冻结集的**子集**(集合包含判据,见 GATE-4 与 DoD-7)。〔实现期实测:`--write --only shared` 同步的是**整个 scope**,一次写出 3 个文件——本特性的 `fast-fail.md`(MISS → 新建)连同两条既有漂移(`workflow/feedback-step.md`、`workflow/runtime-mode.md`)一并治好,故 DIFF 集由 2 条降为 **0** 条。两个被连带治好的文件其**源**(`shared/workflow/`)`git diff` 为空、方向是源 → 镜像、镜像改后与源逐字节相等,即它们是**陈旧的生成副本**而非有人在镜像里编辑,故治好是正确结果;但其 84 增 / 37 删落在 Feature 052 声明范围之外,MUST 单独成一个提交以保持本特性提交的原子性。原判据写成"等于 2 条",使一次改善反而判为失败——已按 GATE-4 改为子集形态〕
- [X] T011 [US1] [blockedBy: T010] 核验 US1 分区转绿:`python3 -m pytest tests/contract/test_fast_fail_discipline.py -q -k "c1_ or c2_ or c3_ or c4_ or c5_ or c6_ or c7_ or c8_ or c9_ or c10_ or c11_ or c12_ or c13_ or c14_ or c15_ or c16_ or c17_ or c20_ or c21_"`,期望该区间全绿且 C-18/C-19/C-22 仍红(它们属后续阶段,本行 MUST NOT 要求其转绿)
- [X] T012 [US1] [blockedBy: T011] 实跑 `quickstart.md` 场景 1 与场景 7 的**改后**命令并把输出追加进 `.specify/specs/052-fast-fail-principle/notes/quickstart-run.md`:场景 1 期望份数 **13** 且 `BYTE-IDENTICAL`;场景 7 期望两条计数**相等**且 `FF-2`…`FF-8` 各 **1**
- [X] T013 [US1] [blockedBy: T012] SC-001 双评审者一致性取样:构造 ≥10 个异常场景(清单命中与未命中各半,取自 `00-cross-cutting-lessons.md` §十二–§十四 的已实测案例 + 构造的未命中案例),派发**两个互不共享上下文的只读子代理**独立判定,逐场景对照表落盘 `notes/sc001-dual-review.md`;若二者结论不一致,MUST 记为**判据缺陷**并回写 T007 的判据文本,而不是判为"两位都对";若独立评审者在本会话不可得,记 `[~]` 并说明(051 对同类 SC 的先例),MUST NOT 编造通过率

## Phase 4: User Story 2 - 纪律获得名字、唯一真源、常驻可见性与防漂移守卫 (Priority: P1)

**Story Goal**: 常驻顶级章节落地并抵达所有已初始化项目,既有分散实例点位收敛为指针,使 US1 的判据在每个会话里够得着且不各自漂移。

**Independent Test**: 只完成本阶段即可独立验收——`## Fast Fail Discipline` 在模板与活动文件中各出现且仅出现一次、位置合法、不内联真源文档节名;8 个既有实例点位各含且仅含一行指针而正文逐字未变;`ambient-section.md` C-1…C-12 转绿;`quickstart.md` 场景 2 改后判据可实跑。

### Implementation for User Story 2

- [X] T014 [P] [US2] [blockedBy: T010] 在 `templates/instructions-template.md` 的 `## User-Facing Comprehension` 与 `## Dogfooding Practice` 之间插入新的顶级章节 `## Fast Fail Discipline`:沿用既有纪律章节的固定引导句式(`The full discipline is defined in a single source of truth — ` + 反引号路径 `.specify/shared/guidelines/fast-fail.md` + `(do NOT copy its rules; reference the file) — and binds all commands, skills, and agents:`)+ 若干摘要要点 + 一行指针;MUST NOT 内联真源文档的任何 H2 节名;MUST NOT 含引擎调用形态(裸 `--action` 旗标 / `$ARGUMENTS` / `<占位符>`)、`/speckit.` 命令形态、或四个项目专名;逐行 MUST NOT 命中 `BLOCKING_RE`;并**实测新增字节数**,确认活动文件再生后仍在 32768 预算内(改前 28168,余量 4600)
- [X] T015 [P] [US2] [blockedBy: T010] 把 FR-029 点名的 8 个既有实例点位各加**一行**指向 `.specify/shared/guidelines/fast-fail.md` 的指针,正文逐字不动:`templates/commands/implement.md`(可写性预探针、任务前提证伪回写、门禁判定不得绕、非并行失败即停、两振停滞升级)、`templates/commands/todo.md`、`templates/commands/analyze.md`、`templates/commands/docs.md`(两处)、`templates/commands/clarify.md`(两处)、`templates/commands/interview.md`、`skills/create-team/references/create-mode.md`、`skills/draw-diagram/SKILL.md`;指针措辞 MUST 逐行零命中 `BLOCKING_RE`(这些文件都在扫描面内)
- [X] T016 [US2] [blockedBy: T014,T015] 在 `tests/contract/test_fast_fail_discipline.py` 中实现 `ambient-section.md` C-1…C-12、C-16…C-19 的断言体(**C-19 的转绿时点归 Phase 6 的 T037**,因其断言对象——真源文档"通道一不可测"的自陈——由 T028 在 Phase 6 才落地;本行只实现其断言体,不要求其转绿)(函数前缀 `test_aN_*`):章节各出现且仅出现一次、指针恰好一行 + 其反空真哨兵、四章节严格排序、三节连续窗口未受扰、章节数 18→19 与 19→20、不内联节名、房式引导句式、无引擎形态、项目中立、无 `/speckit.` 形态、8 个点位各含且仅含一行指针 + 其反空真哨兵、余集断言(除点名点位与本特性落点外 `shared/`+`templates/` 无第二处判据复述)、以及"通道一不可测"的自陈在场
- [X] T017 [US2] [blockedBy: T016] 再生与同步(顺序不可颠倒):先 `python3 scripts/python/sync-mirrors.py --write --only templates --only skills`,再 `python3 scripts/python/regen-command-copies.py`,最后 `bash scripts/bash/generate-instructions.sh`;随后核验 4 条兼容性符号链接仍为符号链接(`for f in AGENTS.md CLAUDE.md QODER.md .github/copilot-instructions.md; do test -L $f; done`)、活动文件 `## ` 节数为 **20**、`regen-command-copies.py --check` 相对 T001 冻结集**无新增**待再生项、`sync-mirrors.py --check --only templates` 与 `--only skills` 相对冻结集**无新增**漂移
- [X] T018 [US2] [blockedBy: T017] 核验 US2 分区转绿:`python3 -m pytest tests/contract/test_fast_fail_discipline.py -q -k "a1_ or a2_ or a3_ or a4_ or a5_ or a6_ or a7_ or a8_ or a9_ or a10_ or a11_ or a12_ or a16_ or a17_ or a18_"` + 既有位置钉子 `python3 -m pytest tests/contract/test_user_facing_comprehension_section.py tests/contract/test_instructions_section_propagation.py tests/contract/test_proactive_trigger_section.py -q` 全绿
- [X] T019 [US2] [blockedBy: T018] 实跑 `quickstart.md` 场景 2 的**改后**命令并追加输出到 `notes/quickstart-run.md`:期望两处各 **1**、四标题行号严格递增且 Fast Fail 落在 UFC 与 Dogfooding 之间、节数 **19 / 20**、指针行 **1**

## Phase 5: User Story 3 - 下游项目的宪章收到这条原则并在 plan 门控里被逐条枚举 (Priority: P1)

**Story Goal**: 经宪章模板原则 XIV + 宪章命令 `MUST include` 第 8 条的**双落点**导出,使每个下游项目 bootstrap 即得,并因其 plan 模板动态枚举而自动进入门控。

**Independent Test**: 只完成本阶段即可独立验收——模板原则数 13→14、活动宪章 15→16、命令条目 7→8、版本 1.12.0→1.13.0、四钉同批上调、`plan-template.md` 零改动而渲染出的门控行数 15→16;`constitution-export.md` C-1…C-18 转绿;`quickstart.md` 场景 3 改后判据可实跑。

### Implementation for User Story 3

- [X] T020 [P] [US3] [blockedBy: T010] 在 `templates/constitution-template.md` 的 `### XIII.` 块之后、`## [SECTION_2_NAME]` 之前插入 `### XIV. Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest)`,结构逐字对齐既有块:以冒号结尾的主张句 → 携 MUST / MUST NOT 的 `- ` 要点(含一条以路径援引 `shared/guidelines/fast-fail.md` 的指针要点,写明消费者 MUST 引用而 MUST NOT 复述;含一条点名拒绝四类机制的不新增机制要点)→ 恰好一个空行 → `Rationale:` 段;每行硬折行 **< 100 字符**;MUST NOT 复述判据、清单条目或注入子句正文;逐行零命中 `BLOCKING_RE`;项目中立
- [X] T021 [P] [US3] [blockedBy: T010] 在 `templates/commands/constitution.md` 的 `MUST include` 清单末尾(`:149` 的 Governance 收尾项之前)新增第 8 条,引号内标题与 T020 **逐字一致**;逐行零命中 `BLOCKING_RE`
- [X] T022 [US3] [blockedBy: T020] 在 `.specify/memory/constitution.md` 的 `### XV.` 块之后新增 `### XVI. Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest)`(结构同 T020);把 `**Version**:` 行由 `1.12.0` 改为 **`1.13.0`** 并更新 `**Last Amended**`;在文件顶部**前置**一份 Sync Impact Report HTML 注释块,形态对齐既有块(`Version change:` 行注明 MINOR 与新增原则、Added / Modified / Removed、`Templates requiring updates:` 逐项 ✅/⚠、`Follow-up TODOs:`、`Preserved by design:`)。⚠️ 核验版本时 MUST 用 `grep -oP '^\*\*Version\*\*: \K[0-9.]+'`,裸 grep 会命中 Sync Impact Report 的 `Version change:` 行(见"生成时前提重测")
- [X] T023 [US3] [blockedBy: T020,T021,T022] 上调 `tests/contract/test_constitution_double_landing.py` 的四个钉子:`TEMPLATE_COUNT` 13→**14**、`LIVE_COUNT` 15→**16**、`COMMAND_COUNT` 7→**8**、`MIN_VERSION` `(1, 12)`→**`(1, 13)`**,并把 STR-004 的标题增入 `DOUBLE_LANDING_WATCHLIST`(改前 2 项 → 3 项);提交说明 MUST 写明"MIN_VERSION 是下限语义,1.13.0 本就通过;上调是为把下限推到本特性之后"(pin hygiene 规则 1)
- [X] T024 [US3] [blockedBy: T021] 再生与同步:`python3 scripts/python/sync-mirrors.py --write --only templates` 后 `python3 scripts/python/regen-command-copies.py`;核验 4 棵按工具命令树(改前各 **25** 文件)的 `speckit.constitution.*` 副本各含新条目、`regen-command-copies.py --check` 相对冻结集无新增待再生项
- [X] T025 [US3] [blockedBy: T023,T024] 在 `tests/contract/test_fast_fail_discipline.py` 中实现 `constitution-export.md` C-1…C-18 的断言体(函数前缀 `test_xN_*`):双落点标题两侧逐字一致 + 缺一即红 + 变异演练(从任一侧删标题都能红,双向带反空真哨兵)、活动宪章原则与版本与 Sync Impact Report、原则块结构与 <100 折行与指针要点与不新增机制要点与中立性、四钉上调后的相等断言、`plan-template.md` 零改动 + 其动态枚举指令文本仍在场的反空真哨兵、以及渲染枚举逻辑使门控行数 15→**16**
- [X] T026 [US3] [blockedBy: T025] 核验 US3 分区转绿:`python3 -m pytest tests/contract/test_fast_fail_discipline.py -q -k "x1_ or x2_ or x3_ or x4_ or x5_ or x6_ or x7_ or x8_ or x9_ or x10_ or x11_ or x12_ or x13_ or x14_ or x15_ or x16_ or x17_ or x18_"` + `python3 -m pytest tests/contract/test_constitution_double_landing.py -q` 全绿;并核验 `git diff --stat -- templates/plan-template.md` **为空**
- [X] T027 [US3] [blockedBy: T026] 实跑 `quickstart.md` 场景 3 的**改后**命令并追加输出到 `notes/quickstart-run.md`:期望 **14 / 16 / 8 / 1.13.0**、双落点标题各 **1**、超长行 **0**、pytest 全绿

## Phase 6: User Story 4 - 子代理在启动那一刻就带上规则 (Priority: P1)

**Story Goal**: 注入子句以成对定界符单点落于真源文档,经三条通道抵达子代理;派发前自检与回传显式异常行两个控制点就位,使"启动后不受控"的执行体在派发前与回传时都可治理。

**Independent Test**: 只完成本阶段即可独立验收——真源文档含恰好一对定界符且区间内文本 ≤10 行/≤1200 字节、逐行零命中、承载三项必备内容;2 份出厂预设与团队载荷第六字段行与两处制作者要求全部就位且副本与拥有者逐字节相等;`dispatch-injection.md` C-1…C-23 转绿;`quickstart.md` 场景 5、6、10、11、12 可实跑。

### Implementation for User Story 4

- [ ] T028 [US4] [blockedBy: T009] 在 `shared/guidelines/fast-fail.md` 填写 `## 子代理派发注入` 节:派发期义务(与既有外部派发可见性契约并列,声明分工——它拥有"是否可观测"、本节拥有"是否受治理",MUST NOT 复述其 5 条义务)、**成对定界符包围的注入子句拥有者字面量**(`<!-- fast-fail-clause:begin -->` … `<!-- fast-fail-clause:end -->`,区间内 MUST 含 `fast-fail-clause` 标识、二值判据、"停在本层并回抛编排者"义务、行首 `ANOMALY:` 前缀判据;MAY 附真源文档路径但 MUST NOT 以路径替代前三项;≤10 行且 ≤1200 字节;逐行零命中 `BLOCKING_RE`)、三条通道及其**不互斥**声明、派发前自检与时点分流、回传显式异常行与缺行即不完整、异常停不计入既有**全部**失败规则(点名两振停滞、连续两次派发失败即降级、非并行失败即停)、上送件所有权分层、三模式同等成立且 virtual 不豁免、调用方内容义务而非包装器行为、派发链逐跳重新注入、子句优先于 Agent 定义正文且冲突本身回抛
- [ ] T029 [P] [US4] [blockedBy: T028] 在 `shared/definitions/subagent-definitions.md` 新增一节派发期注入义务,与既有 `## External Dispatch Visibility Contract` **并列**;该既有节的 5 条编号义务与 `**Reference implementation**:` 行 MUST 逐字未变;新节 MUST 以路径指称真源文档、逐行零命中 `BLOCKING_RE`
- [ ] T030 [P] [US4] [blockedBy: T028] 在 `skills/create-team/references/patterns.md` 的 Per-Agent Payload 表(改前 5 个字段行)新增第 6 行 `fast_fail_clause`,内容规则指向真源文档的拥有者字面量;紧随其后的 Context Isolation Rules 四条 MUST 逐字未变;逐行零命中 `BLOCKING_RE`
- [ ] T031 [P] [US4] [blockedBy: T028] 在 `templates/commands/agents.md` 的 `### Run Mode (subagent dispatch)` 节增加一条注入义务(指向真源文档);该节既有的 4 步序列与 `**Scope boundary**` 段 MUST 逐字未变;逐行零命中 `BLOCKING_RE`
- [ ] T032 [P] [US4] [blockedBy: T028] 在 `skills/create-agent/SKILL.md` 的创作契约增加一条"注入子句 MUST 在场"要求;既有的"六个必备正文节"与"`## Self-Improvement Contract` 恰好一次"要求 MUST 逐字未变;逐行零命中 `BLOCKING_RE`
- [ ] T033 [US4] [blockedBy: T028] 把拥有者字面量(含定界符)逐字节插入 `agents/skill-verifier.agent.md` 与 `agents/structure-adjuster.agent.md`(改前实测恰 **2** 份),各含**恰好一对**定界符
- [ ] T034 [US4] [blockedBy: T029,T030,T032,T033] 同步镜像与渲染:`python3 scripts/python/sync-mirrors.py --write --only shared --only skills --only agents`,随后按既有渲染路径再生三棵按工具 agent 树(`.claude/agents`、`.qoder/agents`、`.github/agents`,改前各 2 条目;`.opencode/agent` 改前为 0);核验 `--check --only agents` 仍为 `ok (2 files)`、`--check --only shared` 与 `--only skills` 相对冻结集无新增漂移
- [ ] T035 [US4] [blockedBy: T031,T034] 再生按工具命令副本:`python3 scripts/python/regen-command-copies.py`;核验 4 棵树的 `speckit.agents.*` 副本含新义务、`--check` 相对冻结集无新增待再生项
- [ ] T036 [US4] [blockedBy: T035] 在 `tests/contract/test_fast_fail_discipline.py` 中实现 `dispatch-injection.md` C-1…C-23、C-26 的断言体(函数前缀 `test_iN_*`):定界符恰好一对且区间非空、子句标识在场、三项必备内容各自独立断言(不因路径在场而短路)、≤10 行且 ≤1200 字节、逐行零命中(正则以 importlib 取真) + C-5/C-6 各自的反空真哨兵、通道二两处制作者要求 + 2 份预设的字节相等 + **有界集合**断言(MUST NOT 枚举 `.specify/agents/instances/`)、通道三第六字段行、通道一落点规定与不互斥声明、派发期义务节与既有 5 条逐字未变、派发前自检与时点分流、回传异常行与缺行即不完整、异常停排除三条既有失败规则、三模式与调用方义务与包装器零改动、逐跳与裁决顺序、通道一不可测的自陈在场
- [ ] T037 [US4] [blockedBy: T036] 核验 US4 分区转绿:`python3 -m pytest tests/contract/test_fast_fail_discipline.py -q -k "i1_ or i2_ or i3_ or i4_ or i5_ or i6_ or i7_ or i8_ or i9_ or i10_ or i11_ or i12_ or i13_ or i14_ or i15_ or i16_ or i17_ or i18_ or i19_ or i20_ or i21_ or i22_ or i23_ or i26_ or a19_"` 全绿
- [ ] T038 [US4] [blockedBy: T037] 实跑 `quickstart.md` 场景 5 的**改后**命令并追加输出到 `notes/quickstart-run.md`:期望拥有者定界符 **1** 对、两份预设各 **1** 对、`owner lines/bytes` ≤ **10 / 1200**、两行 `byte-identical: True`、载荷字段行 **6**、`MIRROR-OK`
- [ ] T039 [US4] [blockedBy: T038] 执行 4 条变异演练并把取证追加进 `notes/red-first-evidence.md`(quickstart 场景 6 / 10 / 11 / 12):场景 6 从**拥有者**取子句写入模拟 outgoing 提示后走"≥1 → 0 → restored 且 ≥1 → 目录不存在"四步;场景 10 断言四种回传分类为 anomaly-halt / clean / incomplete / 行内提及不误判为异常停,且 `doc carries the rule: True`;场景 11 断言 `next action: surface-to-user | allowed: True | forbidden: False` 且真源文档点名"两振/派发失败/非并行"三者;场景 12 断言三行为 True / False / False 且 `doc owns the literal: True`。**每条演练的临时制品 MUST 删净并复核计数归零**

## Phase 7: User Story 5 - 两份清单随使用双向生长 (Priority: P2)

**Story Goal**: 观察闭环就位——标记可检索、双向生长规则与留痕要求落地、过度触发三数可导出,使判据长期有效而不是单向棘轮。

**Independent Test**: 只完成本阶段即可独立验收——`discipline-doc.md` C-18/C-19 转绿;`quickstart.md` 场景 8 在一次性 workspace 中实跑通过且真实存据未被污染;三个数可由既有存据导出。

### Implementation for User Story 5

- [ ] T040 [US5] [blockedBy: T028] 在 `shared/guidelines/fast-fail.md` 填写 `## 生长闭环` 节:观察标记字面量 `[fast-fail]`(带方括号定界)与检索形态、两条红线(干净运行 MUST NOT 追加空洞观察条目、MUST NOT 编造数值)、**双向**生长规则(升级与降级证据资格对称;≥2 次独立观察或 1 次用户直接纠正;以修订本文档的形式;移动后原处措辞收敛为指针)、留痕要求(指向反馈条目 ID / 提交 / 会话原话)、MUST NOT 静默调参、以指针引用既有 probe 与自省入口(不声明新增 probe 类/对象或自省流程)、以及 SC-015 三个数(快速失败率 / 用户推翻率 / 清单净生长方向)与"由既有存据导出、MUST NOT 新增计数器或台账"的声明;并载明上送件**自身携标记**使观察不依赖运行活到收尾
- [ ] T041 [US5] [blockedBy: T040] 同步镜像:`python3 scripts/python/sync-mirrors.py --write --only shared`,核验 `cmp` 逐字节相等且 `--check --only shared` 的 DIFF 集是 T001 冻结集的**子集**(集合包含判据,见 GATE-4;`--write --only shared` 会同步整个 scope,故实测该集已由 2 条降为 0 条)
- [ ] T042 [US5] [blockedBy: T041] 在 `tests/contract/test_fast_fail_discipline.py` 中实现 `discipline-doc.md` C-18、C-19 的断言体(`test_c18_*`、`test_c19_*`):标记字面量在场、两条红线、双向规则(断言文本同时含升级与降级两侧且不只有单向通道)、留痕、禁止静默调参、以指针引用 probe 与自省入口、三个数与其零新增机制声明;并**断言生长闭环侧使用的是独立键 `(发现点, 被证伪的预期)` 二元组**——它 MUST 含发现点,与 `test_c10` 断言的复发键(不含发现点)构成一对**互不替代**的守卫;二者任一侧被合并回单键都必须变红(2026-09-23 用户裁定的回归路径,见 T063);并核验 T005 已实现的 C-20 仍绿(标记字面量改动后互斥性 MUST 重新成立)
- [ ] T043 [US5] [blockedBy: T042] 核验 US5 分区转绿:`python3 -m pytest tests/contract/test_fast_fail_discipline.py -q -k "c18_ or c19_ or c20_"`(C-20 一并复核,因标记字面量在 T040 落地后互斥性 MUST 重新成立),期望全绿;随后实跑 `quickstart.md` 场景 8:在 `--workspace-root /tmp/ffdrill` 一次性根内 record → list 得 `count ≥ 1`,随后断言**真实存据仍为 `count: 0`**(反空真哨兵),`rm -rf` 后目录不存在。⚠️ MUST NOT 用 `--action cleanup` 清理未打包条目(该 action 要求 `--package`,`feedback-utils.py:1389` 会抛 `FeedbackError`);`--action dispose` 亦不适用(只翻元数据、不删文件)

## Phase 8: User Story 6 - 边界落位、既有实例收敛与门控预算中立 (Priority: P2)

**Story Goal**: 与五条相邻纪律的边界显式落位、冲突裁决顺序成文、范围限制与已接受代价写进真源文档,并以设计规避使门控预算 total 保持相等。

**Independent Test**: 只完成本阶段即可独立验收——真源文档 9 节全部填实;类 ⑪ 登记与 C-14 钉子 8→9 落地;扫描器实跑 total 仍为 23、violations 0、扫描器与五个引擎 `git diff` 为空;`gate-neutrality.md` C-1…C-17 与 `ambient-section.md` C-13…C-15、`discipline-doc.md` C-22 转绿。

### Implementation for User Story 6

- [ ] T044 [US6] [blockedBy: T040] 在 `shared/guidelines/fast-fail.md` 填写 `## 与相邻纪律的边界` 节:五处边界各写明"对方拥有什么 / 本纪律拥有什么 / MUST NOT 重定义什么"——门控治理(以**路径** `shared/guidelines/confirmation-gates.md` 指称,MUST NOT 写其中文名「确认门控治理」,因该词逐字命中 `确认门[禁控]`)、输入健全性检查、同作者检测委托(含子代理内异常 MUST 上抛、降级 MUST 标注)、自我提升治理(引用其证据资格判据)、问一次记下来(引用"同一个问题不需要问第二遍",故上送前 MUST 先检索既往裁定)
- [ ] T045 [US6] [blockedBy: T044] 在 `shared/guidelines/fast-fail.md` 填写 `## 冲突裁决顺序` 节:清单 vs 判据(判据优先)、子句 vs Agent 定义正文(框架级优先且冲突本身回抛)、既有实例点位 vs 新判据、并发异常(合并还是逐条、第二处异常在第一处待裁定期间出现时的处置)、裁定 ping-pong 上限(超限升级)、跨会话既有裁定的检索、真源文档自身出现异常时 MUST 上送而 MUST NOT 择一执行
- [ ] T046 [US6] [blockedBy: T045] 在 `shared/guidelines/fast-fail.md` 填写 `## 范围限制` 节:点名拒绝的四类机制(异常检测引擎 / 分流评分器 / 成熟度报告 / 台账或注册表)、不新增 probe 类或对象、不新增面向用户界面类、观察约定(标记 + 三条红线),以及 **FR-078 要求的已接受代价**——因门控预算整数余量为 0 而取设计规避,本纪律措辞从此永久受制于一个无关扫描器的 17 条模式。⚠️ 该代价 MUST 以**散文**表述,MUST NOT 粘贴扫描器的输出行(`blocking confirmation gates: 23` 自身命中 `confirmation gate` 模式,贴进扫描面内的本文档会使 total +1 并打爆 `contracts/gate-neutrality.md` C-10 枚举的**全部**钉子)
- [ ] T047 [US6] [blockedBy: T046] 同步镜像:`python3 scripts/python/sync-mirrors.py --write --only shared`,核验 `cmp` 逐字节相等、9 个 H2 节全部非空、DIFF 集是冻结集的**子集**(集合包含判据,见 GATE-4)
- [ ] T048 [P] [US6] [blockedBy: T028] 在 `shared/guidelines/user-facing-comprehension.md` 的界面类映射表中,把类 **⑪ 失败如实报告** 的「规则真源文件」列由单一路径改为同时含 `shared/guidelines/confirmation-gates.md` 与 `shared/guidelines/fast-fail.md`(该列已支持多文件,类 ⑤ 就列了两个);`reader_baseline_override` 列 MUST 保持 `—` 不变;并在 `tests/contract/test_user_facing_comprehension_doc.py` 中把 `:400` 的 `len(deduped) == 8` 上调为 **9**(改前实测该表 11 行、按规则真源列去重得 8 且 8 个路径均存在),**同时新增一条断言**:类 ⑪ 行的规则真源列含 `shared/guidelines/fast-fail.md`(该断言即 `constitution-export.md` **C-19** 的载体;C-20 由同一次钉子上调承载;C-21 由既有 `test_c18a_override_registry_has_at_most_two_entries` 承载,本行只须核验其仍绿)
- [ ] T049 [US6] [blockedBy: T048] 同步 UFC 镜像并在**四处**留痕该跨纪律改动:`python3 scripts/python/sync-mirrors.py --write --only shared` 后核验 `cmp`;留痕于 plan.md › Feature List Review(已在)、feature-ref.md(已在)、`features/051.md`(已在)、`features/052.md`(已在)——本行核验四处均在场且表述一致,MUST NOT 默默发生
- [ ] T050 [US6] [blockedBy: T047,T049] 在 `tests/contract/test_fast_fail_discipline.py` 中实现 `discipline-doc.md` C-22、`constitution-export.md` **C-23**(上送件四要素内容下限归本纪律、类 ⑪ 措辞与上下文规则仍归既有拥有者——断言真源文档载明该分工)、`ambient-section.md` C-13…C-15、`gate-neutrality.md` C-1…C-17 的断言体(前缀 `test_c22_*`、`test_a13_*`…`test_a15_*`、`test_gN_*`):范围限制子句点名四类机制 + 已接受代价在场、恢复路径指名真实的 CLI 资产复制且 MUST NOT 含"刷新指令即恢复镜像"句式(**负面命题,须配变异演练**)、扫描器三个值逐字不变(`POLICY_DOCS` 2 / `SELF_REL` / `BLOCKING_PATTERNS` 17)、total 与冻结基线相等且 violations 空、**C-10 表三行钉子各自可独立定位到真实断言**(C-10(a) 反空真哨兵:分别断言 `test_user_facing_comprehension_doc.py` 含 `== 23` 字面量、`test_proactive_trigger_section.py` 含 `== frozen["total"]`、`test_confirmation_gates_sweep.py` 含 `<= cap`;MUST NOT 写成"至少一处存在",否则第三行被删时守卫仍绿)、本特性全部新增文本逐行零命中 + 其反空真哨兵、六个引擎与脚本路径 `git diff` 为空 + 其反空真哨兵、`MIRROR_PAIRS` 未变
- [ ] T051 [US6] [blockedBy: T050] 执行 C-15 的变异演练并取证到 `notes/red-first-evidence.md`:临时把"刷新项目指令即连同其镜像副本一并恢复"句式插入常驻章节 → 断言变红 → 移除 → 断言恢复绿;演练改动 MUST 复原并复核 `git diff` 对该文件为空
- [ ] T052 [US6] [blockedBy: T050,T051] 核验 US6 分区转绿(含跨纪律条款 `constitution-export.md` C-19…C-23:其断言载体是**既有**的 `tests/contract/test_user_facing_comprehension_doc.py`,C-14 钉子 8→9 即 C-20 的实现;C-22 的四处留痕由 T049 核验、C-19/C-21 由 T053 的 quickstart 场景 9 实跑核验):`python3 -m pytest tests/contract/test_fast_fail_discipline.py -q -k "c22_ or x23_ or a13_ or a14_ or a15_ or g1_ or g2_ or g3_ or g4_ or g5_ or g6_ or g7_ or g8_ or g9_ or g10_ or g11_ or g12_ or g13_ or g14_ or g15_ or g16_ or g17_"` + `python3 -m pytest tests/contract/test_user_facing_comprehension_doc.py -q` 全绿(含上调后的 C-14 = 9 与未受影响的 C-18a 上限 2)
- [ ] T053 [US6] [blockedBy: T052] 实跑 `quickstart.md` 场景 4 与场景 9 的**改后**命令并追加输出到 `notes/quickstart-run.md`:场景 4 期望 total 仍 **23**、`--baseline` 的 `EXIT=0`、扫描器 `git diff --stat` 为空、`test_c11_gate_scan_total_unchanged` passed;场景 9 期望类 ⑪ 行同时含两个路径、钉子为 **9**、`fast-fail.md` 在该文件命中 **1**、override 列仍为 `—`

## Phase 9: Polish & Cross-Cutting Concerns

- [ ] T054 [blockedBy: T013,T019,T027,T039,T043,T053] 实跑 `quickstart.md` 的**全部 12 个场景**(改前基线部分与改后判据部分),把逐场景输出追加进 `notes/quickstart-run.md`;凡改后判据在本轮不可实跑者,如实记录其改前等价基线并标注原因,MUST NOT 留下未标注的空期望
- [ ] T055 [blockedBy: T054] 全量契约套件名字级回归:`bash scripts/bash/run-tests.sh --names-out .specify/specs/052-fast-fail-principle/current-failed.txt` 后 `comm -13 .specify/specs/052-fast-fail-principle/baseline-failed.txt .specify/specs/052-fast-fail-principle/current-failed.txt`,期望输出**为空**(判据是名字集合,不是失败条数——条数相等时失败集合仍可能已换手)
- [ ] T056 [blockedBy: T055] 撰写 `.specify/specs/052-fast-fail-principle/verification.md`:逐条给出 SC-001…SC-015 的状态与取证位置;不可得者记 `[~]` 并写明理由(SC-001 与 SC-008 要求未参与本特性实现的评审者;SC-013 子代理侧与 SC-015 为度量而非门禁);并记 `deferred_tasks=`
- [ ] T057 [blockedBy: T056] **锁步一致性核验**(plan.md 的遗留义务 ②):封闭处置集四项与子句长度上限(≤10 行 / ≤1200 字节)各有两处全文枚举——处置集在 `data-model.md` E6 与 `contracts/discipline-doc.md` C-17(b),上限在 `data-model.md` E12 与 `contracts/dispatch-injection.md` C-5;逐对比对四处取值一致,并核验真源文档落地后与之一致;任一不一致 MUST 就地订正为单点拥有 + 指针
- [ ] T058 [blockedBy: T057] **派生命令审计**(plan.md 的遗留义务 ③,本轮已查出 3 处同类缺陷):把本特性全部制品(plan.md、research.md、data-model.md、quickstart.md、feature-ref.md、contracts/×5、tasks.md)中印出的每一条派生命令逐条实跑,核对其输出与文中所印数值相符;凡模式可能过宽者(如 `grep -c '^## 场景'` 会匹配 `## 场景覆盖表`、裸 `grep -o '1\.[0-9]*\.[0-9]*'` 会命中 Sync Impact Report)MUST 订正命令本身而不只是订正数字
- [ ] T059 [blockedBy: T058] **测试路径认领自检**(命令要求):扫描本文件全部核验行,标记任何在两个核验行中出现、却指向不同转绿时点的测试路径;`tests/contract/test_fast_fail_discipline.py` 被 Phase 3 / 7 / 8 三处认领,故核验三行的 `-k` 条款区间**互不相交且并集覆盖全部条款**,无区间被两行同时要求转绿
- [ ] T060 [blockedBy: T059] 对着**当前树**重跑 GATE-1…GATE-9 全部九项,逐条记录命令、实际输出与判定到 `verification.md`;任一项不满足 MUST 就地修复后重跑,连续三次重跑无新进展则停止并上送(MUST NOT 继续重试)
- [ ] T061 [blockedBy: T060] Feature 列表复审:确认本特性**未暴露新 Feature、未使既有 Feature 失效**;把实现期的关键变更与跨 Feature 交付效应(对 051 的类 ⑪ 登记与 C-14 上调)记入 `.specify/memory/features/052.md` 的 Latest Review;核验 `.specify/memory/features.md` 索引行的 Spec Path 未变、Status 仍为 `Planned`(推进到 `Implemented` 归 `/speckit.implement`,本命令 MUST NOT 落该状态)
- [ ] T062 [blockedBy: T061] 把实现期查出的**自身缺陷**与推广教训追加进 `docs/reference/history/00-cross-cutting-lessons.md` 的相应小节(若有新形态),或如实记录"无新形态";MUST NOT 为了让本行有产出而发明教训

### 实现期中途用户裁定落地(追加,不重编号)

- [X] T063 [blockedBy: T013] 落地 2026-09-23 用户对 **FR-014 同一性键**的裁定(甲案:拆成两个键),并重跑 S9 双评审复核。裁定原文与理由已逐字追加进 `requirements.md` › `## Clarifications` › `### Session 2026-09-23`(append-only,行数 12 → 13 已核验)。级联改动五处:`requirements.md`(FR-014 复发键 / FR-044 独立键 / Key Entities › 异常)、`data-model.md` E2、`contracts/discipline-doc.md` C-10(g)、真源文档 `### 三条裁决顺序` 的两振升级条、`test_c10` 断言体;另扩 T042 使 `test_c18` 断言独立键含发现点。**新守卫 MUST 非空真**:已做变异演练——把真源文档的「不含发现点」改为「含发现点」(即模拟两键被合并回去)→ `test_c10` 变红并印出回归路径说明 → 复原 → 恢复绿,镜像复核逐字节相等。**复核义务**:以同一份 12 场景表重跑 SC-001 双评审,要求 S9 的**规则级**依据由「退回存疑从严」变为「直接命中两振升级」,规则级一致率由 11/12 升到 **12/12**;两次结果 MUST 并列记入 `notes/sc001-dual-review.md`,MUST NOT 覆盖首轮记录

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1(Setup)** → 无依赖;MUST 先于一切(基线冻结必须在任何编辑之前)
- **Phase 2(Foundational)** → 依赖 Phase 1;**阻塞全部用户故事**(守卫骨架与 red-first 证据是后续"转绿"有意义的前提)
- **Phase 3(US1,P1)** → 依赖 Phase 2。**MVP 边界**:US1 单独交付即已消除"静默兜底"这一失效
- **Phase 4(US2,P1)** → 依赖 Phase 3 的 T010(镜像已同步,常驻章节的指针才不悬空)
- **Phase 5(US3,P1)** → 依赖 Phase 3 的 T010;与 Phase 4 **可并行**(编辑不同文件)
- **Phase 6(US4,P1)** → 依赖 Phase 3 的 T009(真源文档已有前四节,才可在其中增第五节)
- **Phase 7(US5,P2)** → 依赖 Phase 6 的 T028(生长闭环节须在派发注入节之后填,同一文件顺序编辑)
- **Phase 8(US6,P2)** → 依赖 Phase 7 的 T040(边界与范围限制节是同一文件的最后三节)
- **Phase 9(Polish)** → 依赖全部前序阶段

### User Story Dependencies

- US1 是**唯一被其他故事依赖**的:它创建真源文档这一共享载体。US2/US3/US4/US5/US6 都依赖 T010(文档存在且镜像已同步)。
- US2 与 US3 互不依赖,可并行(不同文件:指令模板 vs 宪章模板/命令/活动宪章)。
- US4 → US5 → US6 **在同一份文件上顺序编辑**(`shared/guidelines/fast-fail.md` 的第 5、6、7-9 节),故三者串行;这是文件级争用,不是逻辑依赖。
- US3 与 US4/US5/US6 无依赖,若人力允许可与它们并行。

### Within Each User Story

author-section(写制品)→ mirror-parity(同步镜像并核验字节相等)→ render-verify(再生/渲染并核验输出)→ 分区核验(只对本行点名的条款区间负责)→ quickstart 场景实跑 → 变异演练取证(仅负面命题)。

### Parallel Opportunities

- **Phase 4 内**:T014(指令模板)与 T015(8 个实例点位)编辑不同文件,可并行。
- **Phase 5 内**:T020(宪章模板)与 T021(宪章命令)编辑不同文件,可并行。
- **Phase 6 内**:T029 / T030 / T031 / T032 分别编辑 `subagent-definitions.md`、`patterns.md`、`agents.md`、`create-agent/SKILL.md`,四个不同文件,可并行;T028 与 T033 编辑不同文件但 T033 依赖 T028 的拥有者字面量,故串行。
- **Phase 8 内**:T048(UFC 文档 + 其测试)与 T044–T046(真源文档)编辑不同文件,可并行。
- **跨阶段**:Phase 4 与 Phase 5 可整体并行。
- **MUST NOT 并行**:任何两个编辑 `shared/guidelines/fast-fail.md` 的任务(T006–T009、T028、T040、T044–T046);任何两个编辑 `tests/contract/test_fast_fail_discipline.py` 的任务(T003、T005、T016、T025、T036、T042、T050)。

## Parallel Example: User Story 4

```bash
# T028 完成(拥有者字面量就位)后,四个不同文件的落点可并行:
# 派发 A: T029 shared/definitions/subagent-definitions.md
# 派发 B: T030 skills/create-team/references/patterns.md
# 派发 C: T031 templates/commands/agents.md
# 派发 D: T032 skills/create-agent/SKILL.md
# 四者汇合后再走 T033(agents/ 两份预设)→ T034(镜像与渲染)→ T035(命令副本再生)
```

> 派发这四个子代理时 MUST 履行本特性正在规定的注入义务:派发前自检 outgoing 提示含 `fast-fail-clause` 标识,并要求回传含显式异常行。

## Implementation Strategy

### MVP First

**MVP = Phase 1 + Phase 2 + Phase 3(US1)**。交付物是真源文档及其前三节(判据 + 两份清单 + 上送件与披露)与镜像,以及 `discipline-doc.md` C-1…C-17、C-20、C-21 的守卫。这已消除本特性要治理的核心失效:异常有了可判定的分流判据与两份封闭清单,而不再取决于它恰好在哪个流程里被发现。

MVP 之后按 P1 → P2 增量:US2(可达性与防漂移)→ US3(下游导出)→ US4(派发注入)→ US5(生长闭环)→ US6(边界与门控中立)。US2 与 US3 可并行以缩短关键路径。

### 三条贯穿全程的纪律(承 plan.md 的遗留义务)

1. **计数一律由实跑的派生命令得出**,MUST NOT 沿用记忆或上一轮的值;命令的正则 MUST 核验不会匹配非目标行(T058 复核)。本轮上游已查出 3 处同类缺陷。
2. **两处双重枚举锁步编辑**(T057):封闭处置集与子句长度上限各有两处全文枚举,改一处 MUST 同批改另一处。
3. **相对判据而非绝对判据**(DoD-7、GATE-4):镜像与副本的既有漂移先于本特性存在,故判据一律为"触及的面上无**新增**漂移";写"全绿 / EXIT=0"会发运一条在本仓不可通过的判据。

## Notes

- **提交纪律**:逐任务或逐阶段提交,MUST 以 T001 冻结的 `BASE_SHA` 字面值为比对基线而非 `HEAD`(CI 洁净检出下 `git diff HEAD` 恒空真)。
- **`[~]` 候选**:T013(SC-001 双评审者)与 T056 中依赖 SC-008 读者测试的部分,要求未参与本特性实现的评审者;单会话不可得时记 `[~]` 并在 `verification.md` 的 `deferred_tasks=` 说明,MUST NOT 编造通过率(先例:Feature 051 的 T060/T061)。
- **本特性零改动的路径**:`scripts/`、`src/specify_cli/`、`templates/plan-template.md`、`skills/create-team/scripts/dispatch.sh` 及其流过滤脚本、`scan-confirmation-gates.py`(含 `POLICY_DOCS` / `SELF_REL` / `BLOCKING_PATTERNS`)。GATE-3 对此机械核验。
- **门控中立是逐行判据**:本特性全部新增文本落在扫描面内(`shared/`、根级 `templates/*.md`、`templates/commands/`、`skills/`),任何一行命中 17 条模式即 total +1,同时打爆 `contracts/gate-neutrality.md` C-10 枚举的**全部**既有钉子(实现期实测为三处,形态互不相同:硬编码字面量 / 对冻结基线相等 / 由 Feature 044 基线派生的 `cap = 23.25` 上限——第三处 grep `== 23` 找不到,规划期因此漏计)。每个 author-section 任务都已把"逐行零命中"写进要求;T050 的 GATE 侧再做一次全量核验,GATE-5 已补入第三处钉子所在的 `test_confirmation_gates_sweep.py`。
- **关于 `validate-tasks.py` 的唯一 WARN(T014 / T015 并行安全)**:该警告是**误报,已核实并在报告说明**,MUST NOT 据此把两行串行化。校验器从任务行中提取一切被提及的路径,而这两行都把 `.specify/shared/guidelines/fast-fail.md` 作为**指针目标**提及,并非写入目标:T014 写 `templates/instructions-template.md`,T015 写 8 个命令/技能文件。两者写入集**不相交**,`[P]` 合法。消除该警告需要把指针目标从行文中删去或改写为间接指称——那是**为迁就校验器启发式而削弱制品精度**,与本特性 FR-064("MUST NOT 为规避门禁而改写语义")同一取向,故不取。
