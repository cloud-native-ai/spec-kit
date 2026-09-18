---
description: "Task list for Feature 051 — 面向用户可理解性纪律(User-Facing Comprehension)"
---

# Tasks: 面向用户可理解性纪律(User-Facing Comprehension)

**Requirement ID**: 051
**Requirement Key**: 051-user-facing-comprehension
**Related Feature**: 051 面向用户可理解性纪律(User-Facing Comprehension)(from `.specify/memory/features.md`,Status = **Planned**)
**Input**: Design documents from `.specify/specs/051-user-facing-comprehension/`
**Prerequisites**: plan.md(required)、requirements.md(required)、research.md(D-1…D-15)、data-model.md(E1…E9 / V1…V4 / S1…S2)、contracts/(5 份;条款编号区间见各文件头部,总数 MUST 派生不手写)、quickstart.md(6 场景)、feature-ref.md(FR → 条款映射)

**Tests Mode**: ON —— `.specify/memory/constitution.md:51` 的 **Principle IV "Test-First & Contract-Driven Implementation"** 含 MUST 级测试要求(由 `grep -nE 'MUST|MANDATORY|NON-NEGOTIABLE|Test-First|TDD|Contract-Driven'` 确定性检出);**但** `:90` 的 `**Workflow Gates (NON-NEGOTIABLE)**` 之下、`:95` 的 **Template-only features** 门同时适用——本特性**零可执行运行时代码**(`src/specify_cli/` 与 `scripts/` 均不改动,FR-033 禁止任何新机制),故本文件发出的是**结构契约测试**(对制品内容、canonical 路径、标题、镜像字节相等的断言),**不是**单元/集成测试(无运行时代码可测)。plan.md 的 Constitution Check 已据此把 Principle IV 判为 **⚠ Partial(正当化)** 并填入 Complexity Tracking。

**Organization**: 任务按 user story 分组。**无 Phase 2 Foundational**——本特性是纯文档/治理特性,无阻塞式前置基础设施,依 tasks 模板 `:168-170` 的显式指引整节省略并重编号。**制品形态为 doc-feature**,故各 story 内采用文档特性分类法(author-section → mirror-parity → render-verify → refresh-verify),**不套用** app 形态的 Models → Services → Endpoints。

## Definition of Done (DoD)

- DoD-1: 真源文档 `shared/guidelines/user-facing-comprehension.md` 七节齐备、内容与 `contracts/discipline-doc.md` 的**全部条款**相符(条款清单与编号以该文件头部声明为准,MUST NOT 在本行枚举区间——区间会随新增条款静默过期,本行此前正因 C-17 的新增而漏改)、且镜像逐字节相等。
- DoD-2: 常驻章节 `## User-Facing Comprehension` 在两份模板各出现且仅一次、抵达 `.specify/instructions.md`、位置在钉死窗口之外、节体 ≤25 行且无 `###`。
- DoD-3: 8 个界面类规则真源文件各含**且仅含一行**指针;3 处内容搬家完成且各自的**保留项**逐字未动(`interview-pattern.md:125-126`、`feedback-step.md:89-90/:113-114/:141`、`project-overview.md:51` 的清单门)。**`feedback-step.md:115` 不属逐字保留项**——C-10 要求其并存措辞收敛权威**上移**,故该行会被改写;原表述 `:113-115` 使本行与 C-10/T036 构成不可满足对(发现项 B-09),已按需求侧真源 FR-019 的 `:113-114` 订正。
- DoD-4: `confirmation-gates.md` 的判据各节(`:7-12`、`:14-21`、`:23-41`、`:43-45`、`:47-52`)**逐字未改写**;`:58-60` 三要素仍由该文件拥有。
- DoD-5: 宪章双落点成立——模板 13 条原则(含 XII = STR-006、XIII = STR-003)、命令 `MUST include` 清单 7 条、活动宪章 15 条且版本 ≥1.12.0 并含 Sync Impact Report;`templates/plan-template.md` **零改动**。
- DoD-6: 确认门控扫描 `total == 23` 且 `violations == []`;`scan-confirmation-gates.py` 的 `POLICY_DOCS`、`SELF_REL`、`BLOCKING_PATTERNS`(17 条)**均未被修改**。
- DoD-7: 零新机制——本特性新增文件中可执行脚本数为 0(新增 `.py` 仅位于 `tests/contract/`);`src/specify_cli/`、`scripts/`、`templates/plan-template.md` 三个零改动面**自 T001 冻结的 `BASE_SHA` 起**无任何新增/修改(命令形态与理由见 GATE-4 与 `gate-neutrality.md` C-6(a)/(b):MUST 用 `--name-only --no-renames --diff-filter=ACMR "$BASE"`、MUST NOT 用 `git diff HEAD`、MUST NOT 按扩展名过滤)。
- DoD-8: 镜像与再生一致——本特性触及的三对经 `sync-mirrors.py --check --only shared --only templates --only skills/summarize-project` 为 EXIT=0、`regen-command-copies.py --check` 为 EXIT=0,且全树相对 T001 冻结的既有漂移**无新增 `MISS`/`DIFF` 行**。判据形态与理由见 GATE-2;**全树绝对 EXIT=0 不是判据**(它会被本特性未触及的在途漂移拖红)。
- DoD-9: 单源扫描内容形态复述数为 **0**(豁免:真源文档自身、机械副本、测试钉死字面量)。
- DoD-10: 全量契约套件失败集 ⊆ `baseline-failed.txt`,**零新增失败 ID**。该文件**以 T001 开工时重新冻结的那份为准**,条数 MUST NOT 在本行手写——本行此前钉死"24 条",而其中 1 条(`test_review_prerequisite_flags_are_supported`)在 `tasks.md` 生成后已**自愈**、另有若干条来自本特性未触及的在途漂移,钉死数字会在每次重冻后立刻过期(承 050 自己记录的"不硬编码字面量"教训)。
- DoD-11: `verification.md` 为 SC-001…SC-018 逐条给出 `SC-NNN_status=pass|deferred`;延后项写明理由。
- DoD-12: 项目中立性——4 个禁用专有名称在真源文档、新常驻章节、两条新宪章原则中命中数为 0。

**DoD Status**: pending

## Completion Gate

- GATE-1: 零新增测试失败 vs 冻结基线 —— check: `python3 -m pytest tests/contract/ -q 2>&1 | grep '^FAILED' | sed -E 's/^FAILED //; s/ - .*$//' | sort > /tmp/cur.txt && comm -13 .specify/specs/051-user-facing-comprehension/baseline-failed.txt /tmp/cur.txt`(输出 MUST 为空)。**`s/ - .*$//` 不可省**:pytest 在 `running_on_ci()`(检查 `CI` / `BUILD_NUMBER`)为真时会给每条 FAILED 行追加 ` - <crash message>`,而 `baseline-failed.txt` 存的是裸 node ID,缺该 sed 会使**整份**基线全部匹配失败、`comm -13` 报出与基线等量的假"新增失败"。本地因每个 node ID ≥88 字符(非 tty 下 `fullwidth=80`、`line_width>74`)恰好抑制了该后缀,故不加 sed 在本地也会通过——这是只在 CI 显形的缺陷
- GATE-2: 本特性触及的镜像对零漂移,且全树**无新增**漂移行 —— check(三段全 MUST 通过):① `python3 scripts/python/sync-mirrors.py --check --only shared --only templates --only skills/summarize-project; echo EXIT=$?` MUST 为 **EXIT=0**(本特性触及的三对;实测该范围今天即 EXIT=0);② `python3 scripts/python/regen-command-copies.py --check; echo EXIT=$?` MUST 为 **EXIT=0**(该命令今天就干净,是名副其实的绝对判据);③ 无新增漂移:`sed -n '/^MIRROR_DRIFT_PREEXISTING_BEGIN$/,/^MIRROR_DRIFT_PREEXISTING_END$/p' .specify/specs/051-user-facing-comprehension/notes/pre-change-measurements.md | grep -E '^(MISS|DIFF)' | sort > /tmp/drift0.txt && python3 scripts/python/sync-mirrors.py --check 2>&1 | grep -E '^(MISS|DIFF)' | sort > /tmp/drift1.txt && comm -13 /tmp/drift0.txt /tmp/drift1.txt` MUST **输出为空**。**MUST NOT 以全树 `--check` 的 EXIT=0 作判据**:实测计划期之后本仓出现 `skills/draw-diagram/` 的在途改动,使全树 `--check` 变为 EXIT=2,与本特性无关;绝对判据要么让本特性被无关状态无限期阻塞,要么(更坏)促使执行者跑裸 `--write` 把别人的在途工作吸收进本特性的提交以"转绿"(见 T050)。判据形态承 **049** 的先例(其 plan 明写"所触及镜像对报 `ok` 且无新增漂移行,而非命令整体 exit 0");既有漂移行集由 T001 冻结
- GATE-3: 确认门控预算未被触碰 —— check: `python3 scripts/python/scan-confirmation-gates.py`(MUST 输出 `blocking confirmation gates: 23` 与 `violations (reversible gates still blocking): 0`)
- GATE-4: 扫描器与零改动面未被修改 —— check: `BASE=$(sed -n 's/^BASE_SHA=//p' .specify/specs/051-user-facing-comprehension/notes/pre-change-measurements.md) && git diff --name-only --no-renames --diff-filter=ACMR "$BASE" -- scripts/ .specify/scripts/ src/specify_cli/ templates/plan-template.md | wc -l`(MUST 输出 `0`)。**MUST 以 T001 冻结的 `BASE_SHA` 为基线、MUST NOT 用 `HEAD`**:`git diff HEAD` 看不见本特性**已提交**的改动(提交纪律要求逐任务提交),且在 CI 洁净检出下工作树恒等于 HEAD ⇒ 该断言**无条件空真**(`gate-neutrality.md` C-6(a))。**MUST 用 `--name-only` 而非 `--stat`**(`--stat` 行尾是 `| N ++++` 且长路径省略为 `.../name`,任何按路径的后续过滤都会零命中)。**MUST NOT 按扩展名过滤**:`templates/plan-template.md` 是 `.md`、`scripts/` 下另有 70 个非 `.py`/`.sh` 受跟踪文件,扩展名过滤会让它们结构性逃逸(C-6(b))。**新增可执行脚本的全仓探测不在此门**,由 GATE-9 承担:`shared/` 与 `skills/` 是本特性的合法改动面,故 MUST NOT 纳入本门的路径集
- GATE-5: 无未闭合任务行 —— check: `grep -cE '^- \[[ >]\]' .specify/specs/051-user-facing-comprehension/tasks.md`(MUST 返回 0)
- GATE-6: 结构校验器通过 —— check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/051-user-facing-comprehension/tasks.md`(MUST exit 0)
- GATE-7: 18 条 SC 逐条有状态 —— check: `grep -cE '^SC-0[0-9]{2}_status=' .specify/specs/051-user-facing-comprehension/verification.md`(MUST 返回 18)
- GATE-8: 8 个规则真源文件各含且仅含一行指针 —— check: `for f in shared/guidelines/confirmation-gates.md shared/workflow/feedback-step.md shared/patterns/interview-pattern.md templates/commands/clarify.md shared/guidelines/requirements-guidelines.md shared/guidelines/proactive-trigger.md skills/summarize-project/references/reporting-playbook.md shared/workflow/glossary.md; do printf '%s  %s\n' "$(grep -c 'shared/guidelines/user-facing-comprehension.md' "$f")" "$f"; done`(8 行 MUST 全部输出 `1`;即 `quickstart.md:133-144` 场景 4 的第一个命令)
- GATE-9: 全仓无新增可执行脚本(FR-033 / SC-011 / `gate-neutrality.md` C-5)—— check: `BASE=$(sed -n 's/^BASE_SHA=//p' .specify/specs/051-user-facing-comprehension/notes/pre-change-measurements.md) && git diff --name-only --no-renames --diff-filter=ACMR "$BASE" -- . | grep -E '\.(py|sh)$' | grep -vE '^tests/contract/' | wc -l`(MUST 输出 `0`)。**MUST 用 `--name-only` 而非 `--stat`**:`--stat` 的行尾是 `| N ++++` 且长路径被省略为 `.../name`,`grep -E '\.(py|sh)$'` 永远零命中——实测在 6 个提交、16 个真实新增 `.py` 上命中数恒为 0。断言取"过滤后计数 == 0"而非"命中全部落在 tests/contract/",否则空结果与通过不可区分

## Environment Prerequisites

本节是探测结论的**唯一落点**(生成期实测,不跨会话缓存)。各 Phase 的前置说明与任务行的 `[~]` 备注 MUST 引用本节,不重述判定。

- **本机工具链**: available —— probe: `command -v python3 pytest bash git grep cmp diff sed awk comm` @ 2026-09-17,全部命中;`python3 --version` = **3.11.11**,`python3 -m pytest --version` = **pytest 8.4.2**。受影响任务:全部(无缺口)。
- **容器运行时 / 镜像仓库 / 实集群 / 特殊硬件**: **不需要** —— 本特性制品全为版本控制下的 Markdown 与 test-side Python;`docker` 虽在 PATH 上但无任何任务依赖它。受影响任务:无。
- **网络**: **不需要** —— `specify init --help` 明写 "Use local templates (GitHub download is no longer supported)";所有校验命令均为本地文件操作。受影响任务:无。
- **已安装 `specify` CLI 与本工作树的关系**: **partial(关键)** —— probe: `python3 -c "import specify_cli; print(specify_cli.__file__)"` @ 2026-09-17 → `/usr/local/lib/python3.11/site-packages/specify_cli/__init__.py`,**不在仓库树内**;`python3 -m pip show specify-cli` → Version **0.0.22**、Location site-packages(**非可编辑安装**)。因 init 使用**已安装包内**的模板,直接在临时目录跑 `specify init` 验证的是 0.0.22 的模板,**不是本特性的改动**。受影响任务:**T034**(quickstart 场景 5c 的下游 bootstrap 演练)。**替代路径**:① 先从本树重装(`python3 -m pip install -e .`)——该动作改动全局 site-packages,属**需先征得用户同意**的操作;② 或以 **T032 + T033 的机械核验**作为导出能力的验收证据,把 T034 记为 `[~]` 延后并在 `verification.md` 写明理由。quickstart.md 场景 5c 已同步订正该前提(原写法"以本仓为安装源"经实测不成立)。
- **镜像全树 `--check` 存在与本特性无关的既有漂移**: **partial(关键)** —— probe: `python3 scripts/python/sync-mirrors.py --check 2>&1 | grep -E '^(MISS|DIFF)'` @ 2026-09-18 → **2 行**:`DIFF .specify/skills/draw-diagram/SKILL.md`、`MISS .specify/skills/draw-diagram/references/self-deploy-render-service.md`。归因已核实:`git status --porcelain skills/draw-diagram/` 显示二者是**未提交的在途改动**(源侧 1 处修改 + 1 个未跟踪文件),mtime 为 2026-09-18 10:48/10:49,**晚于**本特性 2026-09-17 的计划期基线,且两文件对 `user-facing-comprehension` 的命中数均为 **0** ⇒ 与本特性无关。故全树 `--check` 为 **EXIT=2**,而本特性触及范围 `--check --only shared --only templates --only skills/summarize-project` 实测为 **EXIT=0**。受影响任务:**GATE-2 / DoD-8 / T010 / T029 / T051** —— 判据一律取"触及对报 `ok` + 全树相对 T001 冻结集**无新增漂移行**",MUST NOT 取全树绝对 EXIT=0(发现项 B-03);**T050** 的 WRITE 一律 `--only` 范围化、MUST NOT 裸写(裸写会把该在途改动吸收进本特性的提交,即发现项 V-01)。连带影响:`test_scripts_distribution_parity.py::…::test_repo_has_no_orphan_or_drifted_scripts`、`test_trigger_engine.py::test_c2_sync_mirrors_check_clean`、`test_browser_site_exclusions.py::…::test_mirror_check_ignores_site_probe` 三个既有契约测试因断言全树 `--check` 而失败,MUST 纳入 T001 重冻的基线、不得报成本特性回归。该漂移会随对方提交或自行 `--write` 而消失;届时 T001 重冻得空集,判据形态不变。
- **契约套件的既有失败集与目录内基线不一致**: **partial** —— probe: `python3 -m pytest tests/contract/ -q 2>&1 | grep '^FAILED' | sed -E 's/^FAILED //; s/ - .*$//' | sort | wc -l` @ 2026-09-18 → **26**,而本 spec 目录既有的 `baseline-failed.txt` 为 **24** 条(2026-09-17 计划期冻结)。差异已全部定位:① 上一条的 3 个镜像类测试因在途漂移新增失败;② `test_specify_script_paths.py::…::test_review_prerequisite_flags_are_supported` 在 `tasks.md` 生成后**自愈**、由失败转通过(C-7 已预期该条)。⇒ 26 − 3 = 23,与自愈后的数目一致。受影响任务:**T001**(MUST 以实跑重冻 `baseline-failed.txt`,MUST NOT 沿用既有那份)、**GATE-1 / DoD-10 / T057**(判据只有"`comm -13` 输出为空",失败总数 MUST NOT 在任何行预写;发现项 B-04)。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行(不同文件、无未完成依赖)
- **[Story]**: 该任务所属 user story(US1…US5);Setup 与 Polish 阶段**零** `[US` 标记
- **[blockedBy: Txxx,Tyyy]**: 显式依赖;`/speckit.implement` 据此拓扑排序,阻塞项未 `[X]` 前不得开工。仅受阶段顺序约束的任务**省略**该标签
- **任务状态 sigil**: `- [ ]` 未开工 / `- [>]` 已认领(多代理)/ `- [X]` 已闭合 / `- [~]` 已延后(理由记入 `verification.md` 的 `deferred_tasks=`)

---

## Phase 1: Setup

**Purpose**: 冻结改前基线,使后续每一处"计数不变 / 零回归"断言都有可比的实测起点

- [X] T001 **基线冻结(本特性所有比对型门禁的唯一基线来源)**:把改前实测值写入 `.specify/specs/051-user-facing-comprehension/notes/pre-change-measurements.md`,每项附**可复现的再推导命令**。**本行列出的数字是 2026-09-17/18 的实测快照,仅作对照;所有写入值 MUST 取自开工当时的实跑输出,若与快照不符则以实跑为准并把差异记入同一文件**(硬编码的期望值是过期源:本行的套件计数就已在生成后漂移过一次)。需冻结的四组:① **`BASE_SHA=<git rev-parse HEAD 的字面输出>`**——GATE-4 / GATE-9 / T011 / T033 / T055 / T056 全部以该字面 SHA 为比对基线,MUST NOT 用 `HEAD`、`HEAD~<n>` 或 `--stat`(理由见各行);② **测试失败基线**:跑 `python3 -m pytest tests/contract/ -q 2>&1 | grep '^FAILED' | sed -E 's/^FAILED //; s/ - .*$//' | sort` 并把输出**覆写**进 `.specify/specs/051-user-facing-comprehension/baseline-failed.txt`(C-7 明令"开工前 MUST 重新冻结",而 049 与 050 的同一惯例都由各自的 T001 承担;本行此前无承担者),同时记录 failed/passed 计数(快照:24 failed / 1924 passed,**已过期**,实测请以实跑为准);③ **既有镜像漂移基线**:跑 `python3 scripts/python/sync-mirrors.py --check 2>&1 | grep -E '^(MISS|DIFF)' | sort`,把输出写进 `MIRROR_DRIFT_PREEXISTING_BEGIN/END` 标记之间(快照:2 行,均来自本特性未触及的 `skills/draw-diagram/` 在途改动),GATE-2 / DoD-8 / T010 / T029 / T051 以"无新增漂移行"为判据而非全树 EXIT=0;④ 其余结构实测值:门控 `total`=23(`python3 scripts/python/scan-confirmation-gates.py`)、`shared/guidelines/*.md`=11(`ls -1 shared/guidelines/*.md | wc -l`)、`templates/instructions-template.md` 的 `## ` 章节=17 与 `.specify/instructions.md`=18(`grep -c '^## ' <file>`)、`templates/constitution-template.md` 原则=11 与 `.specify/memory/constitution.md` 原则=14(`grep -cE '^### [IVXLC0-9]+\.' <file>`)、命令 `MUST include` 条目=5(`grep -c '\*\*MUST include\*\* a principle for' templates/commands/constitution.md`)、8 个指针目标文件当前指针数=0/8(quickstart 场景 4 的循环)、`BLOCKING_PATTERNS` 条数=17(importlib 加载扫描器后 `len(m.BLOCKING_PATTERNS)`)
- [X] T002 [blockedBy: T001] 核验三个零改动面在开工时干净并把结果追加进 `.specify/specs/051-user-facing-comprehension/notes/pre-change-measurements.md`,作为 Phase 7 T055 的比对起点:`BASE=$(sed -n 's/^BASE_SHA=//p' .specify/specs/051-user-facing-comprehension/notes/pre-change-measurements.md) && git diff --name-only --no-renames --diff-filter=ACMR "$BASE" -- src/specify_cli/ scripts/ templates/plan-template.md | wc -l`(MUST 输出 `0`;`BASE` 即 T001 刚记下的 `BASE_SHA`)。**本行是全特性唯一可以用 `git diff HEAD` 的地方**——开工时 HEAD 就是基线、本特性尚无任何提交,两式等价(`gate-neutrality.md` C-6(c));此处仍统一写成 `"$BASE"` 形态,以免被当作可复制到 T011 / T033 / T055 / GATE-4 的样板(那四处在实现中途运行,用 `HEAD` 即为缺陷)。对应 FR-033 / FR-038 / C-6

---

## Phase 2: User Story 1 - 一条无名规矩获得名字、真源、常驻可见性与守卫 (Priority: P1) 🎯 MVP

**Goal**: 让这条纪律有唯一权威定义点、有名字、被每个 agent 常驻读到、并被契约测试守住——即用户诊断的核心缺口"项目本身没有把它明确的定义出来"

**Independent Test**: 只实现本片即可验证:真源文档存在且七节齐备、镜像逐字节相等、常驻章节在两份模板各一次并抵达活动指令文件、两个新测试文件全绿、项目中立性零泄漏、门控计数不变。交付价值 = 这条纪律从此有唯一真源且被守卫(规格 US1 Independent Test)

### Tests for User Story 1 (MANDATORY — 结构契约测试,red-first)⚠️

- [ ] T003 [P] [US1] 撰写 `tests/contract/test_user_facing_comprehension_doc.py`,实现 `contracts/discipline-doc.md` 的 **C-1…C-18**,**并额外承载 `contracts/gate-neutrality.md` 的 C-2、C-3、C-5、C-6 四条**(该归属由 gate-neutrality 开头的归属表指定;不写进本任务范围则这 4 条只存在于契约文档而不进 CI):独立 `pathlib`+`pytest` 形态、`pytestmark = pytest.mark.contract`、`ROOT = Path(__file__).resolve().parents[2]`、函数名 `test_cN_*` 与条款一一对应;C-16 与 gate-neutrality C-2/C-3 所需的 `BLOCKING_RE`、`POLICY_DOCS`、`SELF_REL`、`BLOCKING_PATTERNS` MUST 以 `importlib` 内联加载真实 `scripts/python/scan-confirmation-gates.py` 复用(先例 `tests/contract/test_ask_record_repeat.py:41,106-108`),MUST NOT 在测试内重写模式副本或硬编码字面量;**Pin Hygiene**:文件路径存在性检查、计数用 `len(...)` 从 glob 派生而非硬编码、版本断言用下限语义 `>=` 而非 `startswith`
- [ ] T004 [P] [US1] 撰写 `tests/contract/test_user_facing_comprehension_section.py`,实现 `contracts/ambient-section.md` 的 **C-1…C-11**;C-11 的悬空指针遍历 MUST 同时覆盖 `templates/instructions-template.md` **与** `.specify/instructions.md` 两个指令面中**全部** `.specify/shared/guidelines/*.md` 指针(实测模板面 7 份、活动面 8 份,两面并不一致——这正是 MUST 遍历两面的理由),MUST NOT 只检查新文档(FR-038 / SC-017);并按 C-11(b) 从 `shared/guidelines/*.md` 派生全集、减去被指向集合,断言余集 **⊆** {`checklist-methodology.md`, `requirements-guidelines.md`, `self-improvement.md`}(子集语义:删指针即失败、补指针不误报),使 11 份 guideline 全部被核算而**不假装**遍历能抵达无指针的 3 份;C-7 的位置窗口断言 MUST 钉死 `## Documentation Map` → `## Proactive Flow Trigger` → `## Fact, Correctness & Logic Checks (Input Sanity)` 三者的相对顺序与相邻关系
- [ ] T005 [US1] [blockedBy: T003,T004] Red-first 取证:运行 `python3 -m pytest tests/contract/test_user_facing_comprehension_doc.py tests/contract/test_user_facing_comprehension_section.py -q`,确认失败原因是**制品缺失**(FileNotFoundError / 标题不存在)而非导入错误或断言写错;把失败计数与首条失败原因记入 `.specify/specs/051-user-facing-comprehension/notes/red-first-evidence.md`

### Implementation for User Story 1

- [ ] T006 [US1] [blockedBy: T005] 撰写真源文档 `shared/guidelines/user-facing-comprehension.md`(STR-002):按 `data-model.md` E1 的字段表落地——前 3–8 行所有权声明(含 MUST-cite / MUST-NOT-copy 与 ambient 指针所在处,`discipline-doc.md` C-4)、紧随的失效陈述(覆盖"解码术语→自信答错"与"翻页找上下文→答另一个问题"两面,C-5)、**七个 H2 节**且节名逐字为 C-6 所列、白名单 ≥5 条含"白名单之外一律违规"(C-9)、黑名单 ≥4 条并指明条目 ② 的实例来源为 `skills/summarize-project/references/reporting-playbook.md` §1.7(C-10,内容由 T046 提升后补全,本任务先留锚定位)、下限 ≥3 项 + 门控类追加项且以路径引用 `confirmation-gates.md:58-60` 三要素(C-11)、上限 ≥3 约束 + ≥2 条裁决顺序 + clarify R2-Q3=A 的已接受代价成文(C-12)、≥2 条机械判问 + 恰好 1 条全局基准读者 + 覆盖协议"声明处生效不回写" + **恰好 1 条消费单元定义并声明就地注解义务按消费单元计而非按会话计**(C-13、E6 的四个字段全数落地;消费单元是白名单 ② 与黑名单 ③ 中"该消费单元内首次出现"限定词的唯一出处,漏写它会把按消费单元计账悄悄退化为按会话计账,FR-008)、11 行界面类表且去重后 8 个路径全部存在(C-14)、范围限制子句(C-8)、**观察约定含 STR-005 字面量与三条红线**(C-17、FR-036;载体可为独立节或范围限制节的子条,C-17 只断言内容存在)、**以及供 8 个文件复用的 canonical 单行指针形态**(一处定义,避免 8 种写法变成 8 个漂移点)。**撰写时 MUST 逐条自检 `contracts/gate-neutrality.md` C-4 的 17 条禁用字面形态与两个高危陷阱**(`确认门[禁控]` 字序;含「执行/写入/落盘/启动/继续」的命中会被判 `reversible` 而额外打爆 sweep 契约),MUST NOT 出现 `确认门控`/`确认门禁` 字样,统一用 `门控`/`门控提示`/`前置确认`/`门控确认提示`;并满足 C-15 项目中立性(4 个禁用专有名称零命中)
- [ ] T007 [US1] [blockedBy: T006] 在 `templates/instructions-template.md` 新增顶级章节 `## User-Facing Comprehension`(STR-004),位置在 `## Token Efficiency Discipline`(改前 `:65-71`)**之后**、`## Dogfooding Practice`(改前 `:73`)**之前**(`ambient-section.md` C-8,且避开 C-7 的钉死窗口);节体按房子形态撰写(一段引出核心主张 + 固定指针短语 "The full discipline is defined in a single source of truth — `.specify/shared/guidelines/user-facing-comprehension.md` (do NOT copy its rules; reference the file) — and binds all commands, skills, and agents:" + 2–5 条子规则要点 + 可选收尾指针行),**≤25 行、无 `###` 子标题、零 `/speckit.` 命令形式与参数形式、不内联真源文档的七个 H2 节名、零 `BLOCKING_RE` 命中、4 个禁用专有名称零命中**;并按 FR-038 在指针行附**获取途径说明**(文档缺失时如何取得),使章节自身在悬空情形下仍告诉读者怎么办
- [ ] T008 [US1] [blockedBy: T007] mirror-parity **WRITE**(覆盖 plan.md Mirror Obligations 表的第 1 行与第 8 行):运行 `python3 scripts/python/sync-mirrors.py --write --only shared --only templates`,落地 `.specify/shared/guidelines/user-facing-comprehension.md` 与 `.specify/templates/instructions-template.md`
- [ ] T009 [US1] [blockedBy: T008] render-verify + refresh-verify:运行 `bash scripts/bash/generate-instructions.sh` 再生 `.specify/instructions.md`(**顺序不可颠倒**——该脚本从 `.specify/templates/` 读模板,故 T008 必须先完成),随后核验:新标题在活动文件中**逐字**出现、模板 `## ` 章节数 17→**18** 且活动文件 18→**19**、C-7 的三章节相邻关系未变、8 条 symlink 别名仍为符号链接而非被替换成普通文件(`ls -l AGENTS.md CLAUDE.md QODER.md HERMES.md .github/copilot-instructions.md .qoder/project_rules.md .claude/project_rules.md .opencode/instructions.md`)

### Verification for User Story 1

- [ ] T010 [US1] [blockedBy: T009] mirror-parity **VERIFY**(显式枚举所覆盖的镜像对,**按文件名而非 Mirror Obligations 表行号**——行号会随该表新增行静默错位,同 T051):`shared/guidelines/user-facing-comprehension.md` 与 `templates/instructions-template.md` 各自的 `.specify/` 侧。对两对各跑 `diff -q`,再跑 `python3 scripts/python/sync-mirrors.py --check --only shared --only templates` 断言 **EXIT=0**,并按 GATE-2 的 ③ 核对全树相对 T001 冻结的既有漂移集**无新增** `MISS`/`DIFF` 行。**MUST NOT 用全树绝对 EXIT=0**:本行原写"改前基线已实测全绿,故此处用绝对判据",而该前提已被本特性**未触及**的 `skills/draw-diagram/` 在途改动推翻(发现项 B-03;判据形态承 049 先例)
- [ ] T011 [US1] [blockedBy: T009] gate-neutrality 核验:`python3 scripts/python/scan-confirmation-gates.py` MUST 输出 `total 23 / destructive 13 / governance_kept 10 / violations 0`;`BASE=$(sed -n 's/^BASE_SHA=//p' .specify/specs/051-user-facing-comprehension/notes/pre-change-measurements.md) && git diff --name-only --no-renames --diff-filter=ACMR "$BASE" -- scripts/python/scan-confirmation-gates.py | wc -l` MUST 输出 `0`(**MUST NOT 用 `HEAD`**:本行在实现中途运行、本特性已有提交,且 CI 洁净检出下 `git diff HEAD` 恒空真,见 `gate-neutrality.md` C-6(a);**MUST NOT 用 `--stat`**:其行尾形态使任何按路径的过滤零命中)(对应 C-2、C-3;本行证明 T006/T007 的设计规避生效)
- [ ] T012 [US1] [blockedBy: T010,T011] 把 US1 负责的条款转绿:运行 T003/T004 两个测试文件,确认 `discipline-doc.md` **C-1…C-18** 与 `ambient-section.md` **C-1…C-11** 全部通过,并确认 T003 额外承载的 `gate-neutrality.md` **C-2、C-3、C-5、C-6** 四条亦通过(C-10 的黑名单实例来源子句在 T046 完成前 MAY 为部分满足,该行须在此注明其完整绿点归 T054)
- [ ] T013 [US1] [blockedBy: T012] 人工 QA:执行 `quickstart.md` **场景 1 与场景 2** 的全部命令并逐项比对期望(两文件存在且 `cmp` 静默、guideline 数=12、三处 `grep -c '^## User-Facing Comprehension'` 各=1、章节数 18/19、悬空指针遍历全 `ok` 零 `MISSING`),把实测输出记入 `.specify/specs/051-user-facing-comprehension/notes/quickstart-run.md`

**Checkpoint**: 纪律有名字、有唯一真源、被每个 agent 常驻读到、被两个测试文件守住;门控预算与零改动面均未受影响。**MVP 达成。**

---

## Phase 3: User Story 2 - 确认提示说人话、带足上下文 (Priority: P1)

**Goal**: 给 13 个治理保留门控的提示加上今天**完全不存在**的措辞义务,并把 `confirmation-gates.md:68` 那条只写给反馈提交提示的最强规则提升为面向全部界面类的一般规则

**Independent Test**: 抽样门控提示套用机械判据;核验 `confirmation-gates.md` 已接入单行头部指针、`:68` 已提升并收敛为指针、判据各节逐字未变、门控计数不变(规格 US2 Independent Test)

### Tests for User Story 2 (MANDATORY — 结构契约测试,red-first)⚠️

- [ ] T014 [US2] 撰写 `tests/contract/test_user_facing_comprehension_pointers.py`,实现 `contracts/surface-pointers.md` 的 **C-1…C-14**;**docstring MUST 记录条款 → Phase 的分区**(本文件被三个 story 的验证行共同认领,依 `/speckit.tasks` 的分区规则避免"同一文件在两个时点被要求全绿"的不可满足对):**US2 = C-2、C-4、C-5**;**US4 = C-10**;**US5 = C-1、C-3、C-6…C-9、C-11…C-14**。C-4 的判据冻结 MUST 用**逐节文本比对**(提取 `:7-12`/`:14-21`/`:23-41`/`:43-45`/`:47-52` 五节全文与冻结字面量比对),MUST NOT 用"包含关键词"的弱断言
- [ ] T015 [US2] 扩展 `tests/contract/test_confirmation_gates_execution_report.py`:新增断言 `shared/guidelines/confirmation-gates.md` 携带指向真源文档的指针(FR-034 补上今天缺失的守卫),并确认既有用例 `:44-46`(只断言 `非阻塞` 与 `自动传输`)**继续通过**
- [ ] T016 [US2] [blockedBy: T014,T015] Red-first 取证:运行两个测试文件,确认**改前真红的子义务**因**制品未改**而失败、且失败原因非导入错误——具体为 **C-2**(`confirmation-gates.md` 头部所有权区尚无指针)与 **T015 新增的指针断言**。**同分区内以下条款在 red-first 时点即为绿,不属取证对象、MUST NOT 被读成"断言写错"**:**C-4**(五个判据节"逐字未改写"——改前本就未改写,该条是冻结断言)、**C-5**(`:58-60` 仍由该文件拥有,且真源文档已由 T006 以路径引用它,两侧改前即成立)。追加记入 `notes/red-first-evidence.md`,逐条写明"红的为什么红、绿的为什么绿"(订正发现项 B-12:本行原把 C-4/C-5 一并列为"因制品未改而失败",而二者改前即绿;本行的判据恰是"确认失败原因是制品未改而非断言写错",于是执行者遇到绿的条款会据此**削弱一个正确的断言**)

### Implementation for User Story 2

- [ ] T017 [US2] [blockedBy: T016] 在 `shared/guidelines/confirmation-gates.md` 的**头部所有权区**(改前 `:3-5`,紧邻既有的"命令模板与技能 MUST 以单行引用接入本文档,MUST NOT 在模板内复制判据正文")加入**一行**指针,用 T006 定义的 canonical 指针形态,声明其覆盖界面类 **①②⑩⑪**;MUST NOT 落在 `:7-52` 的任何判据节内(`surface-pointers.md` C-2),MUST NOT 增成多行
- [ ] T018 [US2] [blockedBy: T017] 执行 FR-018 的提升:把 `confirmation-gates.md:68` 那条**仅限反馈提交提示**的措辞规则收敛为指向真源文档的引用,同时**逐字保留** `非阻塞` 与 `自动传输` 两个字面量(否则 T015 校验的既有用例转红);提升后的一般规则("存在用户视角途径时 MUST NOT 暴露引擎/脚本内部调用形态;无途径时保留标识符但标注为引擎细节")归真源文档的黑名单 ① 与白名单 ③ 所有
- [ ] T019 [US2] [blockedBy: T018] mirror-parity **WRITE + VERIFY**(覆盖 Mirror Obligations 表第 2 行 `shared/guidelines/confirmation-gates.md`):`python3 scripts/python/sync-mirrors.py --write --only shared`,随后 `diff -q shared/guidelines/confirmation-gates.md .specify/shared/guidelines/confirmation-gates.md`

### Verification for User Story 2

- [ ] T020 [US2] [blockedBy: T019] gate-neutrality 核验:`python3 scripts/python/scan-confirmation-gates.py` MUST 仍为 `total 23 / violations 0`。本行的证明点是**特定的**——`confirmation-gates.md` 是扫描器的 `SELF_REL`(`:38`)整体豁免对象,故编辑它**不可能**改变计数;若计数变了,说明改动溢出到了别的被扫文件
- [ ] T021 [US2] [blockedBy: T019] 把 US2 分区转绿:运行 `test_user_facing_comprehension_pointers.py` 与 `test_confirmation_gates_execution_report.py`,确认 **C-2、C-4、C-5** 与 FR-034 新断言全部通过(C-1 的"8 文件各 1 行"此时仍为 1/8,属 US5 的绿点,本行 MUST NOT 要求它绿)
- [ ] T022 [US2] [blockedBy: T021] 人工 QA:执行 `quickstart.md` **场景 4** 的命令,按**本阶段的部分期望**比对——8 行指针计数中 `confirmation-gates.md` = **1**、其余 7 个 = **0**;并核验第二条命令输出的 `interview-pattern.md:125-126` 两规则原文仍在、`非阻塞|自动传输` 命中 ≥1;实测输出追加进 `notes/quickstart-run.md`

**Checkpoint**: 门控面有了措辞义务与守卫;13 个门控提示的**文案本身**尚未逐条评审(归 T059 的人工评审)。

---

## Phase 4: User Story 3 - 下游项目的宪章收到这条原则 (Priority: P1)

**Goal**: 经宪章模板 + 命令 `MUST include` 清单的**双落点**把原则输出到每个下游项目,并同批回流从未抵达下游的 Principle XIV,把这次事故变成双落点守卫的第一个受测样本

**Independent Test**: 机械核验模板 11→13 条原则、命令清单 5→7 条、活动宪章 14→15 条且版本 1.11.0→1.12.0、两个模板文件的 `One Source` 命中 0→1、`plan-template.md` 零改动(规格 US3 Independent Test + quickstart 场景 5a/5b)

### Tests for User Story 3 (MANDATORY — 结构契约测试,red-first)⚠️

- [ ] T023 [US3] 撰写 `tests/contract/test_constitution_double_landing.py`,实现 `contracts/constitution-export.md` 的 **C-1…C-13**(C-13 = 两块新宪章原则各自 `BLOCKING_RE` 命中数为 0,落实 `gate-neutrality.md` C-1(c);此前该子条只有撰写约束与扫描器 `total` 的间接探测,而 `constitution-template.md` 的 governance-path 归类**不豁免于 `total` 计数**,间接探测只能给出 +1 而无法定位是哪一块原则哪一行):含 `DOUBLE_LANDING_WATCHLIST` 常量(初始 = STR-003 与 STR-006 两个**完整标题**)、模板标题集 regex `^### [IVXLC0-9]+\. (.+)$`、命令名称集 regex `\*\*MUST include\*\* a principle for "([^"]+)"`、**集合成员相等**判定(C-7,MUST NOT 用子串包含)、不钉死罗马数字(C-8)、`Code as the Single Source of Truth` 与 STR-006 非同一原则的显式断言(C-9)、以及**变异式有效性抽查**(C-10,以临时副本或 monkeypatch 进行,MUST NOT 修改仓库内真实文件);C-13 的 `BLOCKING_RE` MUST 以 `importlib` 内联加载真实扫描器复用,版本断言用**下限语义** `parsed >= (1, 12)`(Pin Hygiene 规则 1),MUST NOT 用 `startswith("1.12")`
- [ ] T024 [US3] [blockedBy: T023] Red-first 取证:运行 `python3 -m pytest tests/contract/test_constitution_double_landing.py -q`,确认**改前真红的子义务**因两条原则尚不存在而失败——具体为 **C-1…C-7、C-9、C-11、C-12、C-13**(尤其 C-7 的名单两侧均缺、C-13 因原则块不存在而报文件缺失)。**以下两条在 red-first 时点不为红,MUST NOT 列为取证对象**:**C-8** 是关于测试**自身匹配逻辑**的设计规则(不钉死罗马数字字面量),T023 写对即绿,与"制品未改"无关;**C-10** 是变异式有效性抽查,其前提是 C-7 已绿(名单内原则两侧都在,才谈得上"删掉一侧后 MUST 失败"),而改前 STR-006 两侧皆缺(实测 `grep -c "One Source"` 在两个模板文件双双为 0)⇒ 该抽查**改前无从区分**,属"不可测"而非"因制品未改而失败"。追加记入 `notes/red-first-evidence.md`(订正发现项 B-12)

### Implementation for User Story 3

- [ ] T025 [US3] [blockedBy: T024] 在 `templates/constitution-template.md` 的 Principle XI(改前 `:132-141`)之后、`## [SECTION_2_NAME]`(改前 `:143`)之前插入 **`### XII. One Source of Truth (Authority & Reference Discipline)`**(STR-006 回流,FR-028):内容以活动宪章 `.specify/memory/constitution.md:155-163` 的既有原则为蓝本**面向通用下游项目重述**(去掉本仓专有名与本项目专有交叉引用,满足 C-15 同款中立性),结构合规(`constitution-export.md` C-2 的 (a)–(g):冒号结尾主张 / 3–6 条 MUST 要点 / 折行 <100 字符 / 恰好一个空行 / `Rationale:` 段),含锚定 `.specify/shared/guidelines/one-source-of-truth.md` 的要点(C-3)与"不新增机制"的范围限制要点(C-4)
- [ ] T026 [US3] [blockedBy: T025] 在同一插入窗口的 XII 之后插入 **`### XIII. User-Facing Comprehension (No Jargon, With Context)`**(STR-003,FR-024):结构同 C-2 的 (a)–(g),含锚定 STR-001 并写明 "reference it, do not restate it" 的要点(C-3,形态先例 `templates/constitution-template.md:103-106`)与"不新增机制"范围限制要点(C-4,先例 `:110-111`);**零 `BLOCKING_RE` 命中**(`gate-neutrality.md` C-1c——`constitution-template.md` 的 governance-path 归类**不豁免于 `total` 计数**,这是 plan D-2 点名的陷阱)
- [ ] T027 [US3] [blockedBy: T026] 在 `templates/commands/constitution.md` 的 `MUST include` 清单末尾(改前第 5 条 Better-Harness Orientation 结束于 `:125`)与 `:126` 的 Governance 收尾要点之间,新增**两条** `- **MUST include** a principle for "<完整标题>" that mandates:` 条目(标题逐字同 T025/T026),各含一条锚定 `.specify/shared/guidelines/` 真源文档且 "MUST be referenced, not restated" 的子要点(先例 `:118-119`)与一条"不新增机制"子要点(先例 `:124-125`);清单条目数 5→**7**(C-5、C-6)
- [ ] T028 [US3] [blockedBy: T026] 在 `.specify/memory/constitution.md` 的 Principle XIV(改前 `:155-163`)之后新增 **`### XV. User-Facing Comprehension (No Jargon, With Context)`**(它已含 XIV,故只加一条,原则数 14→**15**),把 `**Version**:` 行(改前 `:215`)的 `1.11.0` 改为 **`1.12.0`**(MINOR,依 `templates/commands/constitution.md:66`)并更新 `Last Amended` 为落地日期,并按 `:142-148` 在文件头部**前置** Sync Impact Report(记录版本变更与 bump 类型、新增原则、受影响模板的 ✅/⚠ 状态、后续 TODO)
- [ ] T029 [US3] [blockedBy: T027,T028] mirror-parity **WRITE + VERIFY**(覆盖 `templates/constitution-template.md` 与 `templates/commands/constitution.md` 两个源,**按文件名而非 Mirror Obligations 表行号**):`python3 scripts/python/sync-mirrors.py --write --only templates`,随后对两对镜像各跑 `diff -q`,再跑 `python3 scripts/python/sync-mirrors.py --check --only templates` 断言 **EXIT=0**,并按 GATE-2 的 ③ 核对全树相对 T001 冻结的既有漂移集**无新增** `MISS`/`DIFF` 行(全树绝对 EXIT=0 **不是**判据,理由见 GATE-2 与发现项 B-03)
- [ ] T030 [US3] [blockedBy: T027] 再生 4 棵按工具命令副本树:`python3 scripts/python/regen-command-copies.py`(因 `templates/commands/constitution.md` 改动),随后 `python3 scripts/python/regen-command-copies.py --check` 断言 **EXIT=0**;MUST NOT 手工编辑 `.claude/commands/`、`.github/prompts/`、`.qoder/commands/`、`.opencode/command/` 下的任何副本;MUST NOT 创建 `.specify/templates/commands/`(该镜像对已退役,`sync-mirrors.py:73` 排除 `commands`)

### Verification for User Story 3

- [ ] T031 [US3] [blockedBy: T029] gate-neutrality 核验:`python3 scripts/python/scan-confirmation-gates.py` MUST 仍为 `total 23 / violations 0`。**本行的证明点是特定的**——`constitution-template.md` 的路径命中 `GOVERNANCE_PATH_PATTERNS`(含 `constitution-template`)故其命中被归类 `governance_kept`,但 **`governance_kept` 仍计入 `total`**;若 T026 的原则文案含任一阻塞字面形态,本行会以 +1 暴露它
- [ ] T032 [US3] [blockedBy: T029,T030] 把 US3 的条款转绿:运行 `python3 -m pytest tests/contract/test_constitution_double_landing.py -q`,确认 **C-1…C-13** 全部通过,**含 C-10 的变异式抽查**(人为从任一侧删除名单内一条原则后测试 MUST 失败,且抽查未改动仓库真实文件)与 **C-13 的两块新原则零 `BLOCKING_RE` 命中**
- [ ] T033 [US3] [blockedBy: T028] render-verify FR-026 的动态枚举传导(要求**实测验证而非假定**):`BASE=$(sed -n 's/^BASE_SHA=//p' .specify/specs/051-user-facing-comprehension/notes/pre-change-measurements.md) && git diff --name-only --no-renames --diff-filter=ACMR "$BASE" -- templates/plan-template.md | wc -l` MUST 输出 `0`(**MUST NOT 用 `HEAD`**:本行在实现中途运行、CI 洁净检出下恒空真,见 `gate-neutrality.md` C-6(a);本行是 `templates/plan-template.md` 唯一的专属核验任务,而该面是 `.md`、GATE-9 的扩展名过滤对它结构性不可见,故此处空真即等于该面完全无守卫——C-6(b));`grep -cE '^### [IVXLC0-9]+\.' .specify/memory/constitution.md` MUST 返回 **15**;`grep -c 'User-Facing Comprehension' .specify/memory/constitution.md` MUST ≥1;并核验 `templates/plan-template.md:37` 的 "Do NOT hard-code principle names here" 与 `:38-39` 的动态枚举指令仍在(即传导机制未被本特性改动)
- [ ] T034 [US3] [blockedBy: T032,T033] 人工 QA:执行 `quickstart.md` **场景 5a 与 5b** 的全部命令并逐项比对期望(11→13、14→15、两个模板文件 `One Source` 命中 0→1、`MUST include` 5→7、版本 1.11.0→1.12.0);**场景 5c 的下游 bootstrap 演练见 `## Environment Prerequisites` 第 4 条**——本机 `specify` 为 site-packages 的 0.0.22 非可编辑安装,未从本树重装则 5c 对本特性无证明力;若未获准重装,本行按 `[~]` 延后并在 `verification.md` 的 `deferred_tasks=` 写明理由,以 T033 的机械核验作为 FR-026 的验收证据

**Checkpoint**: 下游项目经既有 init + `/speckit.constitution` 即获得两条原则,并经 `plan` 门控的动态枚举自动生效;Principle XIV 首次抵达下游。

---

## Phase 5: User Story 4 - 反馈流程的对外措辞归入同一纪律 (Priority: P2)

**Goal**: 把今天自成权威、只管反馈的对外措辞规则接入本纪律,使其成为界面类 ③ 上的实例,并把并存措辞的收敛权威从"以本节为准"上移到纪律真源

**Independent Test**: 核验 `feedback-step.md` 已接入单行指针、`:89-90`/`:113-114`/`:141` 三处既有规则保留未删(`:115` 属**改写**项、不在保留集,见 C-10)、阈值提示仍为非阻塞单行且不含引擎原始调用(规格 US4 Independent Test)

### Tests for User Story 4 (MANDATORY — red-first 取证;条款已由 T014 撰写)⚠️

- [ ] T035 [US4] [blockedBy: T014] Red-first 取证:运行 `python3 -m pytest tests/contract/test_user_facing_comprehension_pointers.py -q` 并定位 **C-10** 的失败,确认失败原因是 `feedback-step.md` 尚无指针 / `:115` 权威未上移,而非断言写错;追加记入 `notes/red-first-evidence.md`

### Implementation for User Story 4

- [ ] T036 [US4] [blockedBy: T035] 在 `shared/workflow/feedback-step.md` 的**头部所有权段**(改前 `:1-9`,所有权声明在 `:3`)加入一行指针(用 T006 的 canonical 形态,覆盖界面类 **③**);**逐字保留** `:89-90`、`:113-114`、`:141` 三处既有措辞规则(FR-019 明令保留为实例、MUST NOT 另立第二套规则;**`:115` 不在保留集内**,见下一句);并把 `:115` 的并存措辞收敛权威从"Embedded copies … defer to this section"上移为"以本纪律真源为准"(发现项 B-09 订正:原写 `:113-115`,使"逐字保留"与本句的"改写 `:115`"互斥)。**新增的指针行 MUST NOT 命中任何阻塞字面形态**——该文件在扫描范围内(`SCAN_DIRS` 含 `shared`),且 pattern 17 正是 `inviting the user to submit collected feedback`

### Verification for User Story 4

- [ ] T037 [US4] [blockedBy: T036] mirror-parity **WRITE + VERIFY**(覆盖 Mirror Obligations 表第 6 行 `shared/workflow/feedback-step.md`):`python3 scripts/python/sync-mirrors.py --write --only shared`,随后 `diff -q shared/workflow/feedback-step.md .specify/shared/workflow/feedback-step.md`
- [ ] T038 [US4] [blockedBy: T037] 把 **C-10** 转绿并做 gate-neutrality 核验:`python3 -m pytest tests/contract/test_user_facing_comprehension_pointers.py -q` 中 C-10 MUST 通过(C-1 此时为 2/8,仍属 US5 绿点);`python3 scripts/python/scan-confirmation-gates.py` MUST 仍为 `total 23 / violations 0`——本行专门证明 T036 新增的指针行未命中扫描器
- [ ] T039 [US4] [blockedBy: T038] 人工 QA:重跑 `quickstart.md` **场景 4** 的 8 行指针循环,按本阶段部分期望比对(`confirmation-gates.md` 与 `feedback-step.md` = **1**,其余 6 个 = **0**);并核验 `grep -c 'never paste the raw' shared/workflow/feedback-step.md` ≥1(既有规则保留);实测输出追加进 `notes/quickstart-run.md`

**Checkpoint**: 反馈面的措辞规则归入同一纪律,收敛权威上移;其跨表面传播的机械副本尚未再生(归 T050)。

---

## Phase 6: User Story 5 - 38 处分散措辞收敛为指针,搁浅的实现被提升 (Priority: P2)

**Goal**: 把"改一次许可行话要改 38 个地方"变成"只改 1 个";完成两处内容搬家,使访谈模式的可理解性规则与项目总结技能的内部标识黑名单都归入唯一真源

**Independent Test**: 单源扫描内容形态复述数 38→**0**;8 个文件各含且仅含 1 行指针;`interview-pattern.md:125-126` 两规则原文保留;`reporting-playbook.md:109-113` 已收敛为指针且 `:309` 落盘门禁仍在(规格 US5 Independent Test)

### Tests for User Story 5 (MANDATORY — red-first 取证;条款已由 T014 撰写)⚠️

- [ ] T040 [US5] [blockedBy: T014] Red-first 取证:运行 `python3 -m pytest tests/contract/test_user_facing_comprehension_pointers.py -q`,确认 US5 分区中**改前真红的子义务**因制品未改而失败——具体为 **C-1**(8 个规则真源文件尚无指针行)、**C-6、C-8、C-9**(`interview-pattern.md` 的可理解性规则尚未收敛)、**C-11、C-12、C-13**(`summarize-project` 侧的搬家与单源扫描尚未发生)。**以下三条在 red-first 时点即为绿,MUST NOT 列为取证对象、更 MUST NOT 因"没红"而被当作断言写错去削弱**:**C-3**(8 个文件的 `.specify/` 侧镜像逐字节相等——本行在 T041…T049 **之前**运行,源侧尚未改动,故两侧本就同步)、**C-7**(`interview-pattern.md:125-126` 两条模式特有规则原文保留——改前本就未动,属冻结断言)、**C-14**(4 棵按工具副本树 `--check` 返回 0——实测今天即为 EXIT=0)。追加记入 `notes/red-first-evidence.md`,逐条写明红/绿各自的原因(订正发现项 B-12:本行原写"C-1、C-3、C-6…C-9、C-11…C-14 **全部**因制品未改而失败",把 C-3/C-7/C-14 三条改前即绿者一并列入)

### Implementation for User Story 5(9 个任务互不改同一文件,故全部 [P])

- [ ] T041 [P] [US5] [blockedBy: T040] **搬家 A**:编辑 `shared/patterns/interview-pattern.md` —— 把改前 `:121-124` 的四条可理解性规则(白话优先 / 无未解释缩写或行话 / 就地注解特殊术语 / 绝不假定共享上下文)收敛为**一行**指向真源文档的指针(`:119` 的 `**Comprehension rules (可理解性规则)**` 标题行 MAY 保留作挂载点);**逐字保留** `:125-126` 的两条模式特有规则(每问一决策 / 问 what 不问 whether,C-7 明令 MUST NOT 吞并);把 `:280-281` 两条反模式(`Context-free questions`、`Jargon and bare abbreviations`)收敛为一条指向真源文档黑名单/下限的短引用;并在 `:255` 的**嵌入契约不可丢弃清单**追加"接入本纪律的指针"一项(C-8;实测该清单今天未列 Comprehension rules,不补则宿主收窄时指针可被合法丢弃)。该文件属扫描器 `POLICY_DOCS`,门控预算无风险。**C-1 的一行上限适用于本行的全部三处编辑**:该文件含 STR-002 路径的行数 MUST 恰为 **1**,故 `:280-281` 的短引用与 `:255` 清单的新增项 MUST 以**不含仓库路径**的方式指称本纪律(发现项 B-11:本行原未声明该上限,而 C-1 在 T052 这个全部 US5 并行任务的汇聚点才转红,多出一行路径会在那里才暴露)
- [ ] T042 [P] [US5] [blockedBy: T040] 在 `shared/guidelines/proactive-trigger.md` 的头部"归属不在本文档"要点列表(改前 `:11-15`,已有三条"只以路径引用",其中 `:15` 指向 `confirmation-gates.md`)追加**第四条**指针要点,覆盖界面类 **⑥**;MUST NOT 改写 `:47` 的"一条建议 = 一行非阻塞提示"形态定义(本纪律只引用它作为上下文上限的既有形态)
- [ ] T043 [P] [US5] [blockedBy: T040] 在 `shared/guidelines/requirements-guidelines.md` 加入一行指针,覆盖界面类 **⑤ 与 ⑦**(该文件是两类的共同真源,故一行覆盖两类);插入位取 `## General Guidelines > Quick Rules`(改前 `:97-102`,在 `:101` 旁)或文件头部;并按 plan D-3 的裁定**如实记录类 ⑦ 的真源缺口**——`templates/plan-template.md` 与 `templates/tasks-template.md` 实测零措辞规则,本特性不给它们新增措辞规则。**并按 FR-037 / `discipline-doc` C-18 把类 ⑦ 的读者基准登记为覆盖站点**:该文件 `:24`(`Written for non-technical stakeholders`)与 `:101`(`Written for business stakeholders, not developers`)是类 ⑦ 既有的读者基准声明,登记进真源文档 11 行表的 `reader_baseline_override` 列(**类 ⑦ 一个登记项、两处命中**,C-18(a) 按类计数);同批把 `templates/commands/requirements.md:82`(`Written for business stakeholders`)——类 ⑦ 的**命令侧孪生、`research.md` D-14 从未登记的第 4 处**——按 **C-18(c) 收敛为指针,MUST NOT 登记为第二个覆盖处**(D-3 已裁定 `requirements-guidelines.md` 是类 ⑦ 唯一真源;若登记它则 1 全局 + 3 覆盖 = 4,**SC-018 直接不成立**)
- [ ] T044 [P] [US5] [blockedBy: T040] 编辑 `templates/commands/clarify.md`:把改前 `:70` 的借用段("从 `interview-pattern.md` 只借 **context discipline** 与 fact-vs-decision 拆分")扩展为**同时借"不用行话"半侧**,方式为接入真源文档的单行指针(FR-020);**逐字保留**其既有裁定——封闭式提问、选项表 + Recommended、"deliberately does **not** adopt that pattern's open-question rule"
- [ ] T045 [P] [US5] [blockedBy: T040] 收敛 `templates/commands/interview.md` 的内容形态复述:改前 `:30` 的 Glossary 出向条("A question phrased in codebase jargon gets a confident wrong answer")与 `:153-154` 的 Behavior Rules 两条("Every question carries its own context, in a blockquote" / "No jargon, no unexplained abbreviations … never a bare `DLQ`")改为指向真源文档的指针;MUST NOT 改动该文件的结构性章节(否则 4 棵副本树的再生会产生额外漂移)
- [ ] T046 [P] [US5] [blockedBy: T040] **搬家 B**:把 `skills/summarize-project/references/reporting-playbook.md` §1.7(改前 `:109-113`)的内部标识黑名单(`T1–T5`、`E1–E5`、`RC-*`、`CG-*`、`§编号`、`M-*`、引擎字段名、库/表/列/SQL、脚本名)与读者向改写映射(`unknown-schedule` → 「无计划日期,无法判定延期」)**提升进** `shared/guidelines/user-facing-comprehension.md` 的黑名单节,作为条目 ② 的实例来源(补齐 T006 预留的锚定位);随后把 §1.7 正文收敛为指针,并把 `:309` 的落盘门禁 `- [ ] **读者用语纪律已过**(§1.7)` 重新指向提升后的来源(C-11)。**本任务会再次编辑真源文档**,故 T054 MUST 重跑其契约测试。**按 C-12(a) 的区分规则处置 `:309`**(订正发现项 B-10——C-12 原一面要求"独立黑名单副本数为 0"、一面要求"该行 MUST 保留",而该行字面枚举了七类标识符,二者不可同时满足):保留该清单项本身(勾选框、`§1.7` 引用、"无内部标识渗入"这一断言与"只出现在 `## 元信息` 或技能内部文档"这一限定),把括号内的**七类枚举替换为对真源文档黑名单节的指称**。**并按 C-12(b) / C-1**:该指称 MUST **不含仓库路径**,使该文件含 STR-002 路径的行数恰为 **1**(本行的 §1.7 收敛已占用那一行;发现项 B-11)
- [ ] T047 [P] [US5] [blockedBy: T040] 收敛 `skills/summarize-project/references/project-overview.md`(`:22`、`:38`、`:51`)与 `skills/summarize-project/references/consistency-rules.md`(`:31`)的次级实例面为指针;**MUST 保留** `project-overview.md:51` 的 `- [ ] 无内部黑话;外部读者不读代码也能看懂`(它是该界面类的落盘检查门,不是黑名单定义,C-12);并按 FR-037 把该技能"外部读者"表述登记为类 ⑧ 的**读者基准覆盖**声明处
- [ ] T048 [P] [US5] [blockedBy: T040] 在 `shared/workflow/glossary.md` §1(改前 `:17-28`)加入一行指针,覆盖界面类 **⑨**;插入位取 `:23-24` 的 surface-it 要点旁或节首 `:17`;MUST NOT 改写 `:25-26`(绝不破坏性改写用户输入)与 `:27-28`(歧义从用户)
- [ ] T049 [P] [US5] [blockedBy: T040] 收敛 `docs/reference/` 的 3 处**手写**内容形态复述为指针:`docs/reference/commands/interview.md`(`:65`、`:71-73` 的 `## Question Format` 节、`:126-127` 的保证表两行)、`docs/reference/skills/feedback.md`(`:140-142`)、`docs/reference/commands/requirements.md`(`:63`)。**MUST NOT 触碰 `docs/public/**`**——它是 Hugo 构建产物、`git ls-files docs/public` 为 0、经 `docs/.gitignore` 忽略(证据 `skills/create-pages/references/hugo-site.md:22`),修好手写源后由既有 create-pages 流程重建

### Verification for User Story 5

- [ ] T050 [US5] [blockedBy: T041,T042,T043,T044,T045,T046,T047,T048,T049] mirror-parity **WRITE**(一次覆盖本阶段全部镜像行):`python3 scripts/python/sync-mirrors.py --write --only shared --only templates --only skills/summarize-project`(同步 `shared/` 的 4 个改动文件、`skills/summarize-project/references/` 的 3 个改动文件、`templates/` 的 2 个改动文件),随后 `python3 scripts/python/regen-command-copies.py` 再生 `clarify.md`、`interview.md` 与 `requirements.md`(第二批新增,依 C-18(c))的 4 棵按工具副本树。**MUST 用 `--only` 范围化,MUST NOT 用裸 `--write`**:裸写会把本特性**未触及**的镜像漂移一并吸收进来——实测计划期之后本仓出现 `skills/draw-diagram/` 的在途改动,使全树 `--check` 由 EXIT=0 变 EXIT=2——从而让 GATE-2 / DoD-8 / T010 / T029 / T051 五个门禁**以错误理由转绿**,并把别人的在途工作并入本特性的提交(`049` 的 tasks 明令禁止该动作;T008/T019/T029/T037 均已范围化,本行曾是唯一例外)
- [ ] T051 [US5] [blockedBy: T050] mirror-parity **VERIFY**(显式枚举所覆盖的镜像对,**按文件名而非表行号**——行号会随 Mirror Obligations 表新增行而静默错位,与 DoD-1/派发片段曾有的 `C-1…C-16` 同类):`shared/guidelines/proactive-trigger.md`、`shared/guidelines/requirements-guidelines.md`、`shared/patterns/interview-pattern.md`、`shared/workflow/glossary.md` 的 `.specify/shared/` 侧;`templates/commands/clarify.md`、`interview.md`、`requirements.md` 的 4 棵按工具副本树;`skills/summarize-project/references/` 三份。逐对 `diff -q`,再跑 `python3 scripts/python/sync-mirrors.py --check --only shared --only templates --only skills/summarize-project` 与 `python3 scripts/python/regen-command-copies.py --check`,两者 MUST 均 **EXIT=0**。**MUST 用与 T050 相同的 `--only` 范围**:全树 `--check` 会被本特性未触及的在途漂移(实测 `skills/draw-diagram/` 的 1 处 DIFF + 1 处 MISS)拖成 EXIT=2,与本行要证明的命题无关;全树绝对判据本身的问题另记为发现项 B-03(涉及 GATE-2 / DoD-8 / T010 / T029),不在本行解决
- [ ] T052 [US5] [blockedBy: T051] 把 US5 分区转绿:运行 `python3 -m pytest tests/contract/test_user_facing_comprehension_pointers.py -q`,确认 **C-1**(8 个文件各含且仅含一行指针)、**C-3**、**C-6…C-9**、**C-11…C-14** 全部通过
- [ ] T053 [US5] [blockedBy: T052] 单源扫描(C-13 / SC-003):确认 `shared/` + `templates/` + `skills/` 下以内容形态复述真源文档规则(白名单条件 / 黑名单条件 / 下限项 / 上限约束 / 机械判问 / 七个 H2 节名)的位置数为 **0**,豁免三类合法重复(真源文档自身、机械副本即 `.specify/**` 与 4 棵按工具树与 `docs/public/**`、测试内钉死的字面量常量);把扫描命令与结果记入 `notes/quickstart-run.md`
- [ ] T054 [US5] [blockedBy: T052] 重跑 `python3 -m pytest tests/contract/test_user_facing_comprehension_doc.py -q` 并确认 **C-1…C-18 仍全绿**——T046 的提升编辑了真源文档的黑名单节(补齐 C-10 的实例来源子句),本行是该编辑的回归门,也是 discipline-doc C-10 的**完整绿点**(T012 处只满足其指名子句);同时确认 C-16 的 `BLOCKING_RE` 命中数仍为 **0**、C-17 的观察约定与 STR-005 字面量在提升编辑后仍在,以及 T003 承载的 gate-neutrality C-2/C-3/C-5/C-6 四条仍绿

**Checkpoint**: 38 处措辞收敛为 1 个真源 + 8 行指针;两处搁浅实现全框架可达。

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: 全局门禁复核、SC 逐条落状态、跨 Feature 发现项留痕

- [ ] T055 [blockedBy: T054] gate-neutrality **FINAL** 复核:`python3 scripts/python/scan-confirmation-gates.py` MUST 为 `total 23 / destructive 13 / governance_kept 10 / violations 0`;`BASE=$(sed -n 's/^BASE_SHA=//p' .specify/specs/051-user-facing-comprehension/notes/pre-change-measurements.md) && git diff --name-only --no-renames --diff-filter=ACMR "$BASE" -- src/specify_cli/ scripts/ templates/plan-template.md | wc -l` MUST 输出 `0`(**MUST NOT 用 `HEAD`**:本行在 Phase 7 运行、其前已有 50 余个任务的提交,`git diff HEAD` 对它们全部不可见,且在 CI 洁净检出下工作树恒等于 HEAD ⇒ 断言**无条件空真**,见 `gate-neutrality.md` C-6(a);**MUST NOT 用 `--stat`**,其行尾形态使路径过滤零命中;**MUST NOT 按扩展名过滤**——`templates/plan-template.md` 是 `.md`、`scripts/` 下另有 70 个非 `.py`/`.sh` 受跟踪文件,C-6(b)。本行原写"与 T002 的起点比对"却从未读取 T002 的记录,而 T002 记录的正是空值,等于空比空);以 importlib 加载扫描器确认 `len(BLOCKING_PATTERNS) == 17`、`tuple(str(p) for p in POLICY_DOCS) == ('shared/patterns/reconcile-pattern.md', 'shared/patterns/interview-pattern.md')`、`str(SELF_REL) == 'shared/guidelines/confirmation-gates.md'`(**MUST 用这一内容形态**:实测 `POLICY_DOCS` 是 `PosixPath` **元组**、`SELF_REL` 是 `PosixPath`,与字符串列表直接 `==` 恒为假——T003 撰写 CI 断言时 MUST 复用同一形态,否则该断言恒红,或被"修好"成空断言)(`gate-neutrality.md` C-2、C-3、C-6)
- [ ] T056 [blockedBy: T054] 零新机制核验(FR-033 / SC-011 / DoD-7 / `gate-neutrality.md` C-5):以 T001 记录的 `BASE_SHA` 字面值为基线,运行 `BASE=$(sed -n 's/^BASE_SHA=//p' .specify/specs/051-user-facing-comprehension/notes/pre-change-measurements.md) && git diff --name-only --no-renames --diff-filter=ACMR "$BASE" -- . | grep -E '\.(py|sh)$' | grep -vE '^tests/contract/' | wc -l`,输出 MUST 为 **0**。**MUST 用 `--name-only`,MUST NOT 用 `--stat`**——`--stat` 的行尾是 `| N ++++` 且长路径被省略为 `.../name`,`grep -E '\.(py|sh)$'` 永远零命中(实测:在一个新增了 `scripts/python/validate-tasks.py` 的真实提交上,`--stat` 形式零输出 exit 1、`--name-only` 形式正确命中;6 个提交 16 个真实新增 `.py` 上 `--stat` 命中数恒为 0)。断言 MUST 取"过滤后计数 == 0"而非"命中全部落在 tests/contract/",否则空结果与通过不可区分(即 GATE-9)
- [ ] T057 [blockedBy: T055,T056] 全量契约套件 vs 冻结基线:`python3 -m pytest tests/contract/ -q 2>&1 | tee /tmp/p.txt | tail -3`,随后 `grep '^FAILED' /tmp/p.txt | sed -E 's/^FAILED //; s/ - .*$//' | sort > /tmp/cur.txt && comm -13 .specify/specs/051-user-facing-comprehension/baseline-failed.txt /tmp/cur.txt` MUST **输出为空**(零新增失败 ID)。**`s/ - .*$//` 不可省**:pytest 在 `running_on_ci()`(检查 `CI` / `BUILD_NUMBER`)为真时给每条 FAILED 行追加 ` - <crash message>`,而基线文件存的是裸 node ID,缺该 sed 会使**整份**基线全部失配、`comm -13` 报出与基线等量的假新增(即 GATE-1)。注意 `test_specify_script_paths.py::…::test_review_prerequisite_flags_are_supported` 在本文件存在后应**转为通过**(其 `:90` 断言 `tasks.md` 在输出中),该减少属基线内的自愈、不是回归。**失败总数 MUST NOT 在本行预写**:原钉死"当前失败数预期为 **23**",而 T001 重新冻结基线后该数字由实跑决定(仓库另有来自本特性**未触及**的在途漂移的失败),任何预写值都会在重冻当天过期。判据只有一个——`comm -13` 输出为空,即失败集 ⊆ T001 重冻的 `baseline-failed.txt`
- [ ] T058 [P] [blockedBy: T057] 项目中立性扫描(C-15 / `ambient-section.md` C-9 / SC-010):断言 `spec-kit`、`specify-cli`、`specify_cli`、`cloud-native-ai` 四个禁用名称(大小写不敏感)在真源文档、新常驻章节(两份模板)、两条新宪章原则块中命中数为 **0**;注意本 spec 目录与 `feature-ref.md` **不在**该断言范围内(它们是本仓专属工件,允许出现专有名称)
- [ ] T059 [blockedBy: T057,T058] 执行 `quickstart.md` 的**全部 6 个场景**,把每条命令的实测输出追加进 `notes/quickstart-run.md`,并撰写 `.specify/specs/051-user-facing-comprehension/verification.md`:为 **SC-001…SC-018 逐条**写一行 `SC-NNN_status=pass|deferred`(格式依 `/speckit.implement` 的 Pre-Status-Flip Gate)并附 `SC-NNN_note=`;人工度量项(SC-001、SC-006、SC-007 的长度分布比对)如实记为 `deferred` 并指向 T060/T061
- [ ] T060 [blockedBy: T059] SC-001 人工评审(**`[~]`-eligible**):从 `confirmation-gates.md` 治理保留清单的 **13 个门控**中取样,由**未参与本特性实现的评审者**按真源文档的机械判据逐条判定"能否在不追问术语含义的前提下作出批准/否决决定";发现项中属本特性已触碰文件的违规就地修复,属其他文件的违规记入 `verification.md` 的具名后续项而**不静默改写**。延后理由(若延后):需要一位非实现者评审,单会话内不可得
- [ ] T061 [blockedBy: T059] SC-006 双评审盲测(**`[~]`-eligible**):取样 **≥20 条**面向用户消息(覆盖 **≥5 个**界面类),两位互不沟通的评审者独立套用机械判据,比对结论并计算一致率(目标 ≥90%);把样本清单、两人结论与一致率记入 `verification.md`。延后理由(若延后):同 T060,需两位独立评审者
- [ ] T062 [blockedBy: T059] 把两项**跨 Feature 文档空间发现**记入 `verification.md` 的具名后续项(记录而**不在本特性内修复**):① 确认门控预算(total 23 / cap 23.25 / 余量 0)**没有 owner 文档**——`shared/guidelines/confirmation-gates.md` 99 行无一字提及,该阈值只活在两个契约测试与两份 Feature 索引散文里,建议落进该文档的 `## 回流约束` 节;② `AGENTS.md` 称 `Total Features` 计数"由 `scripts/bash/update-feature-index.sh` 维护"与脚本实际行为矛盾(`:150` 整体 `cat >` 重写、`:164` 表头只 6 列会摧毁 `Spec Path` 列),目标文档 = `templates/instructions-template.md` 的 Feature Index 行及其生成镜像,且应**要么修脚本要么删脚本**
- [ ] T063 [blockedBy: T062] 核验 Feature 记录与最终状态一致:`python3 -m pytest tests/contract/test_spec_feature_binding_integrity.py -q` MUST 全绿;`.specify/memory/features.md` 第 051 行的 Status 单元 MUST 与 `.specify/memory/features/051.md` 头部的 `**Status**:` 一致;索引行数与表头 `**Total Features**` MUST 相等且每行 7 列。**状态推进本身不由本任务执行**——`Planned → Implemented` 由 `/speckit.implement` 的 Pre-Status-Flip Gate 拥有(其 DoD 为 tasks.md 零 `[ ]` 行 **且** verification.md 为每条 SC 给出状态);本任务只在该推进发生后核验记录一致性。索引行与表头计数**一律手工编辑**(MUST NOT 运行 `update-feature-index.sh`,理由见 T062 第 ② 项)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 Setup**: 无依赖,可立即开始。**阻塞全部后续阶段**——T001 冻结的基线是 T011/T020/T031/T038/T055 全部"计数不变"断言的比对起点。
- **无 Phase 2 Foundational**: 本特性是纯文档/治理特性,无阻塞式前置基础设施,依 tasks 模板 `:168-170` 整节省略并重编号。
- **Phase 2 US1(P1,MVP)**: 依赖 Setup。**其 T006(真源文档)是全特性的单一阻塞点**——US2 的指针要指向它、US3 的宪章原则要锚定它的路径、US4/US5 的指针与两处搬家都要引用它。
- **Phase 3 US2 / Phase 4 US3 / Phase 5 US4 / Phase 6 US5**: 四者**均依赖 T006**,但**彼此独立**——各自编辑不同的文件集(见下),故在 T006 完成后可并行(若有人力)。按优先级顺序串行执行时为 US2 → US3 → US4 → US5。
- **Phase 7 Polish**: 依赖全部所需 story 完成(至少 US1;完整 DoD 需 US1–US5 全部完成)。

### 四个 story 之间的文件互斥性(可并行的依据)

| Story | 独占编辑的文件 |
|---|---|
| US2 | `shared/guidelines/confirmation-gates.md`、`tests/contract/test_user_facing_comprehension_pointers.py`(创建)、`tests/contract/test_confirmation_gates_execution_report.py`(扩展) |
| US3 | `templates/constitution-template.md`、`templates/commands/constitution.md`、`.specify/memory/constitution.md`、`tests/contract/test_constitution_double_landing.py`(创建) |
| US4 | `shared/workflow/feedback-step.md` |
| US5 | `shared/patterns/interview-pattern.md`、`shared/guidelines/proactive-trigger.md`、`shared/guidelines/requirements-guidelines.md`、`templates/commands/clarify.md`、`templates/commands/interview.md`、`skills/summarize-project/references/` 三份、`shared/workflow/glossary.md`、`docs/reference/` 三份 |

**两处跨 story 的共享文件**(是并行度的真实上限,已由 `blockedBy` 串行化):
1. `shared/guidelines/user-facing-comprehension.md` —— T006(US1)创建,T046(US5)因搬家 B 的提升再次编辑。故 **US5 MUST 在 US1 之后**;T054 是该二次编辑的回归门。
2. `tests/contract/test_user_facing_comprehension_pointers.py` —— T014(US2)创建并写入全部 C-1…C-14,US4/US5 只**运行**它、不再编辑。这是 `/speckit.tasks` 的分区规则的应用:三个 story 的验证行各自只对自己分区的条款要求转绿(T021 = C-2/C-4/C-5;T038 = C-10;T052 = C-1/C-3/C-6…C-9/C-11…C-14),**不存在两行在不同时点要求同一文件全绿**的不可满足对。

### Within Each User Story(doc-feature 分类法)

1. **tests-first**(结构契约测试)→ red-first 取证(确认失败原因是制品缺失而非断言写错)
2. **author-section**(撰写/编辑文档本体)
3. **mirror-parity WRITE**(一次 fan-out 命令覆盖本阶段全部镜像行)
4. **render-verify / refresh-verify**(实际执行再生路径并检查输出)
5. **mirror-parity VERIFY**(逐对 `diff -q` + 全树 `--check`,显式枚举所覆盖的行)
6. **turn-green**(把本 story 分区的条款转绿)
7. **manual QA**(按 quickstart 场景比对,记录实测输出)

**同批义务的不可颠倒顺序**(T008 → T009):`generate-instructions.sh` 从 `.specify/templates/` 读模板,故 MUST 先 `sync-mirrors.py --write` 再再生指令文件;颠倒则再生结果不含新章节,`ambient-section.md` C-3 失败。

### Parallel Opportunities

- **Phase 1**: 无 `[P]`(T002 依赖 T001 写入同一文件)。
- **Phase 2 US1**: T003 与 T004 可并行(两个不同测试文件)。其余串行(单一文件链 T006 → T007 → T008 → T009)。
- **Phase 3 US2 / Phase 4 US3 / Phase 5 US4**: 各阶段内部以串行为主(同一文件的编辑链 + 镜像再生链)。
- **Phase 6 US5**: **T041–T049 共 9 个任务全部 `[P]`**——9 个任务编辑 9 组互不重叠的文件(见上表 US5 行),是本特性**并行度最高**的一段。其后的 T050(镜像 WRITE)是汇聚点,MUST 等 9 个全部 `[X]`。
- **Phase 7**: T058 标 `[P]`(只读扫描,不写文件);T055/T056/T057 为权威门禁,串行。
- **跨 story 并行**: 在 T006 完成后,US2 / US3 / US4 可由三人并行(文件集互斥);US5 因 T046 编辑真源文档,MUST 在 US1 之后,但与 US2/US3/US4 互不冲突,亦可并行。

---

## Parallel Example: User Story 5(本特性并行度最高的一段)

```bash
# T040 的 red-first 取证完成后,9 个任务可同时开工(9 组互不重叠的文件):
Task: "T041 搬家 A — shared/patterns/interview-pattern.md"
Task: "T042 指针 — shared/guidelines/proactive-trigger.md"
Task: "T043 指针 — shared/guidelines/requirements-guidelines.md"
Task: "T044 借用扩展 — templates/commands/clarify.md"
Task: "T045 收敛 — templates/commands/interview.md"
Task: "T046 搬家 B — skills/summarize-project/references/reporting-playbook.md + 真源文档黑名单节"
Task: "T047 收敛 — skills/summarize-project/references/{project-overview,consistency-rules}.md"
Task: "T048 指针 — shared/workflow/glossary.md"
Task: "T049 收敛 — docs/reference/{commands/interview,skills/feedback,commands/requirements}.md"

# 汇聚点(必须等 9 个全部 [X]):
Task: "T050 mirror-parity WRITE(命令与其 --only 范围以 T050 行为准,勿在此复述)"
```

## Parallel Example: User Story 1

```bash
# 两个测试文件互不相干,可同时撰写。撰写范围以各自任务行为准 —— 本块 MUST NOT 复述条款区间:
# 复述即副本,此处的 "C-1…C-16" 就在 C-17 新增后静默过期(并漏掉 T003 额外承载的
# gate-neutrality 四条),而 T003/T004 行本身是对的。派发时读任务行,不读本块。
Task: "T003 tests/contract/test_user_facing_comprehension_doc.py(范围见 T003 行)"
Task: "T004 tests/contract/test_user_facing_comprehension_section.py(范围见 T004 行)"

# 之后是单一文件链,不可并行:
# T006 真源文档 → T007 常驻章节 → T008 镜像 WRITE → T009 指令再生
```

---

## Implementation Strategy

### MVP First

**MVP 范围 = 仅 User Story 1。** 依 MVP 范围规则判定:本特性有 **3 个 P1** story,但 US1 的 checkpoint **单独即可独立测试且有独立价值**——它交付"这条纪律从此有唯一权威定义点、被每个 agent 常驻读到、被契约测试守住",而这正是用户诊断的核心缺口("项目本身没有把它明确的定义出来")。US2/US3 都是**在 US1 之上加投递面**(门控措辞义务、下游宪章导出),不是 US1 价值的必要组成。故与 Feature 050 的"两个 P1 合起来才构成独立增量"不同,本特性 MVP 取单个 story。

1. 完成 Phase 1 Setup(冻结基线——后续所有"不变"断言的比对起点)
2. 完成 Phase 2 US1(🎯 **MVP**)
3. **STOP and VALIDATE**: 按 US1 的 checkpoint 独立验证(T010 镜像、T011 门控计数、T012 条款全绿、T013 quickstart 场景 1–2)
4. 此时即可交付/演示:纪律有名字、有真源、常驻可见、被守卫

### Incremental Delivery

1. Setup + US1 → **MVP**:纪律被定义且常驻可见
2. \+ US2 → 门控面获得措辞义务;`:68` 的反馈专属规则提升为一般规则;`confirmation-gates.md` 判据各节逐字未变
3. \+ US3 → **跨项目传播**:下游 init + `/speckit.constitution` 即得两条原则,Principle XIV 首次抵达下游,`plan` 门控自动纳入
4. \+ US4 → 反馈面归入同一纪律,收敛权威上移
5. \+ US5 → **38 → 1**:两处搬家完成,单源扫描归零,改一次许可行话只需改一个文件
6. \+ Polish → 全局门禁复核、18 条 SC 逐条落状态、两项跨 Feature 发现留痕

每一步都增加价值且不破坏前序步骤;US2–US5 各自有 `**Checkpoint**` 描述其独立验证方式。

### Parallel Team Strategy

1. 全队共同完成 Phase 1 Setup 与 Phase 2 US1(T006 是全特性单一阻塞点,应最先且由最熟悉房子 guideline 形态的人完成)
2. T006 完成后:
   - 开发者 A:US2(门控面 —— 需要熟悉 `confirmation-gates.md` 的判据冻结边界)
   - 开发者 B:US3(宪章导出 —— 需要熟悉宪章原则结构与双落点)
   - 开发者 C:US4(反馈面 —— 最小的一片,可先完成后转去支援 US5)
   - 开发者 D:US5 的 T041–T049 中除 T046 外的 8 个 `[P]` 任务(可再分给多人)
3. T046 因编辑真源文档,MUST 与 A/B/C 的验证行协调时点(其回归门是 T054)
4. 各 story 独立完成并集成;Phase 7 由一人收口

---

## Notes

- `[P]` = 不同文件、无未完成依赖。US5 的 T041–T049 是本特性唯一的大段并行(9 个任务 / 9 组互斥文件)。
- 每个 story 的 `[Story]` 标签用于溯源;Setup 与 Polish 阶段**零** `[US` 标记(由 `validate-tasks.py` 机械校验)。
- **red-first 取证是本特性的强制环节**(T005/T016/T024/T035/T040):结构契约测试在制品存在前必然失败,但**失败原因必须是制品缺失而非断言写错**——不取证就无法区分"测试正确地红"与"测试本身坏了"。
- **`[~]`-eligible 任务**:T034(下游 bootstrap 演练,受 `## Environment Prerequisites` 第 4 条制约)、T060 与 T061(需非实现者评审)。三者的延后理由与替代路径已在各行写明;延后时 MUST 在 `verification.md` 的 `deferred_tasks=` 记录,并加行内 `<!-- deferred: <reason> -->`。
- **提交纪律**:每完成一个任务或一个逻辑组即提交;镜像 WRITE 与其 VERIFY MUST 在同一批内落地(否则 GATE-2 的 ① 触及对判据会红——注意它已**不再**是全树绝对判据,理由见 GATE-2 与 § Environment Prerequisites)。**正因为逐任务提交,所有零改动面断言 MUST 以 T001 的 `BASE_SHA` 为基线而非 `HEAD`**:`git diff HEAD` 只比较工作树与 HEAD,对本特性**已提交**的改动完全不可见,且在 CI 洁净检出下无条件空真(`gate-neutrality.md` C-6(a))——提交纪律与基线选择是同一件事的两面。
- **门控预算是全特性最脆的约束**:T011/T020/T031/T038/T055 五处复核不是重复劳动——它们各自证明一个**不同**的豁免语义(SELF_REL 整体豁免 / governance-path **不**豁免于 total / 在扫描范围内的 `shared/` 文件新增行不命中)。任何一处 +1 都意味着设计规避失效。
- **禁止手工编辑的目录**:`.specify/**`(镜像)、`.claude/` `.github/` `.qoder/` `.opencode/`(按工具副本)、`docs/public/**`(Hugo 产物)。全部经再生脚本落地。
- **避免**:含糊任务、同文件冲突、破坏 story 独立性的跨 story 依赖。本文件的跨 story 依赖只有两处且都已具名串行化(见 Dependencies 节)。
