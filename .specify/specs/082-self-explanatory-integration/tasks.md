# Tasks: Self-Explanatory Framework Integration（不言自明的框架集成）

**Requirement ID**: 082
**Requirement Key**: `082-self-explanatory-integration`
**Related Feature**: 082 Self-Explanatory Framework Integration（不言自明的框架集成）
**Input**: Design documents from `.specify/specs/082-self-explanatory-integration/`
**Prerequisites**: plan.md (required), requirements.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md, feature-ref.md

**Tests Mode**: ON（宪章 Principle IV "Test-First & Contract-Driven Implementation" 是 MUST 级原则:"Write or update tests BEFORE implementing new behavior"）**叠加 template-only 门**（Principle VII Workflow Gates「Template-only features」判定 Test-First 为 Partial(justified):本特性无运行时代码,守卫对象是模板/宪章/镜像的**内容、标题集合与字节相等**）。因此本文件的测试行全部是**结构契约测试**,不存在单元/集成测试行。

**Tests**: 每个用户故事阶段先出契约测试行(Red),后出制品行(Green);两者共用同一个测试文件,故测试文件的改写按**条款分区**(`[green:]` 归属)分派,不做「每故事一份新文件」——见 § Dependencies 的 clause partition 说明。迁移/回归例外也适用:`test_constitution_double_landing.py` 的计数常量(T002)与既有机制套件(T027)只能在其被测对象更新后转绿,故带 `[blockedBy:]` 排在实现之后。

**Organization**: 按 user story 分阶段;三个 P1 故事构成 MVP 集(仅其一不足以形成可交付增量:原则落点没有镜像就指向不存在的路径,镜像没有 `specify init` 就到不了客户项目)。

## Definition of Done (DoD)

- DoD-1: 宪章模板、宪章生成器必含清单与 live 宪章三处都携带 `STR-001`,且 live 宪章版本已推进
- DoD-2: instructions 模板与 live 文件都携带 `STR-001` 小节,小节只含摘要 + 运行时指针,预算报告为 `within`
- DoD-3: 三份 owner 文档的源/镜像逐字节一致,`sync-mirrors.py --check` 退出 0,`regen-command-copies.py --check` 无变化
- DoD-4: 四类守卫套件在真实树上全绿,且每个新守卫都有一条变异腿能证明它会红
- DoD-5: `docs/concepts/self-explanatory.md` 保持指针页形态,其引用的路径两侧可解析
- DoD-6: glossary 登记 `STR-003`（`origin=auto` / `status=proposed`）,退役名只作变体
- DoD-7: 本特性未触碰任何 plan-owned 制品（`plan.md` / `research.md` / `data-model.md` / `contracts/` / `quickstart.md` / `feature-ref.md`）,也未接线 `/speckit.improve`（`OI-082-01`）

**DoD Status**: pending

## Completion Gate

- GATE-1: 四类守卫套件全绿、无新增失败节点 — check: `python3 -m pytest tests/contract/test_constitution_double_landing.py tests/contract/test_instructions_section_propagation.py tests/contract/test_glossary_mechanism.py -q` 退出 0,且与失败节点基线做名字级比对(`comm -13 <baseline> <current>` 为空;唯一允许的既有红是 `tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged`,见 plan EP-003)
- GATE-2: plan.md § Mirror Obligations 的每一行都已核验 — check: `python3 scripts/python/sync-mirrors.py --check` 退出 0 且输出 `shared/ == .specify/shared/` 为 `ok`;`cmp` 判定 6 对源/镜像相同;`python3 scripts/python/regen-command-copies.py --check` 输出 `OK:`
- GATE-3: 无 `[ ]` / `[>]` 任务行残留 — check: `grep -cE '^- \[[ >]\]' .specify/specs/082-self-explanatory-integration/tasks.md` 返回 0
- GATE-4: 每条 `final` 路径成功判据为 `pass` 且 smoke 记录在场 — check: 在 `verification.md` 中,`**Path**: final` 的每条判据都有 `SC-NNN_status=pass`,且 `smoke_command=`、`smoke_exit_code=0`、`smoke_evidence_path=`(路径存在且非空)三者齐备。条件集 owner:`shared/workflow/acceptance-hardening.md` § Gates — 本行只承载检查,不复述判据

## Environment Prerequisites

- Python 3 (`>=3.8`,实测 3.11.11) — available — probe: `python3 --version` @ 2026-11-05;affected phases/tasks: 所有 `pytest` / 镜像 / 扫描器行
- pytest (实测 8.4.2) — available — probe: `python3 -m pytest --version` @ 2026-11-05;affected phases/tasks: 全部验证段
- `specify` 入口 (`/usr/local/bin/specify`) — partial — probe: `command -v specify` + `specify init --help` @ 2026-11-05;affected phases/tasks: T036。**已安装的是已发布的 CLI,其打包资源早于本特性**,故临时目录 `specify init` 只会证明「拷贝路径与 `.specify/shared/` 落地目录可用」,不会产出三份新文档;完整分发判据必须等一个携带三份文档的构建(`pip install -e .` 后重跑同一条命令),T036 的 Notes 写明该替代读法
- git (实测 2.43.5) — available — probe: `git --version` @ 2026-11-05;affected phases/tasks: 基线快照、提交与 `git show HEAD:` 版本比对
- 网络 / 容器运行时 / 活集群 / 特殊硬件 — not-required — probe: 本特性全部操作是本地文件、本地进程与本地 git @ 2026-11-05

**A13 boundary**: 本节只记录**任务生成期的探针结论**;plot-stage 的加载前提归 `plan.md` § Execution Premises(EP-001…EP-004),不从其他特性继承任何记录。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行(写目标不同、无未完成任务依赖)
- **[Story]**: 所属用户故事(US1…US4)
- **[blockedBy: T001,T002]**: 显式依赖;`/speckit.implement` 按拓扑序执行,未满足则拒绝开工
- **[green: <contract>#<clause>]**: 本行是让该契约条款转绿的**唯一**认领行;本特性 34 条条款(C-1…C-34)被恰好认领一次

## Path Conventions

仓库根相对路径;spec 目录 `.specify/specs/082-self-explanatory-integration/`。本特性无 `src/` 交付物。

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 冻结阶段基线,并把本阶段要产出的运行期证据落点建好。本特性没有需要初始化的项目骨架(仓库已是框架源),故 Setup 只承担「先量后改」的前提复位。

- [X] T001 [P] 在 `.specify/specs/082-self-explanatory-integration/notes/` 建目录并冻结运行期证据落点(red-first-evidence / quickstart-run / pre-change-measurements 三个空占位不预写内容),该目录是后续证据行的固定落点 [green: contracts/mirror-distribution.contract.md#C-23]
- [X] T002 [P] 重取改动前基线并写入 `.specify/specs/082-self-explanatory-integration/notes/pre-change-measurements.md`: `wc -c .specify/instructions.md`(实测 32739)、`grep -n '^INSTRUCTIONS_BUDGET_BYTES=' scripts/bash/generate-instructions.sh`(实测 `38:INSTRUCTIONS_BUDGET_BYTES=32768`)、`grep -cE '^### [IVXLC0-9]+\. ' templates/constitution-template.md .specify/memory/constitution.md`(实测 17 / 18)、live 宪章版本行与 `python3 scripts/python/scan-confirmation-gates.py --json` 的 `total`(实测 27),每条附命令、输出与 2026-11-05 日期
- [X] T003 冻结条款覆盖基线: `python3 scripts/python/account-clause-coverage.py .specify/specs/082-self-explanatory-integration --freeze > .specify/specs/082-self-explanatory-integration/coverage-baseline.txt` [green: contracts/constitution-double-landing.contract.md#C-9]

**Checkpoint**: 基线已冻结;后续任一「改动前/改动后」断言都可对照本阶段的三份记录。

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 本特性的三条阻塞前提——(a) 三份 owner 文档必须已在框架源中存在(T004 是只读复核,不是新建),(b) `sync-mirrors.py` 的镜像引擎枚举 `shared` 对(校验入口可用),(c) 守卫套件的加载/断言辅助函数在真实树上可用。三者任一不成立,所有用户故事都无从落地。

**⚠️ CRITICAL**: 本阶段完成前不得开始任何用户故事。

- [X] T004 只读复核三份 owner 文档在框架源中存在且非空(实测 `shared/definitions/self-explanatory-definitions.md` 4508 B / 7 个 `## ` 标题;`shared/guidelines/self-explanatory.md` 6271 B / 10 个;`shared/workflow/best-practice-optimization.md` 4613 B / 8 个),并把三条 `ls -l` 输出写入 `notes/pre-change-measurements.md`;内容不在本特性范围,缺失即上送而非新建。指向: `shared/definitions/self-explanatory-definitions.md` [green: contracts/mirror-distribution.contract.md#C-22]
- [X] T005 复核镜像引擎的枚举形态(与 T004 写同一个 `notes/pre-change-measurements.md`,故不带 [P]) `python3 scripts/python/sync-mirrors.py --check`(实测退出 0,`shared/ == .specify/shared/` 为 `ok`、65 文件)并把输出粘入 `notes/pre-change-measurements.md`;同时记录 `shared` 对是**非 strict** 对(镜像独有文件只报 note,见 plan § Mirror Obligations fact 1) [green: contracts/mirror-distribution.contract.md#C-25]
- [X] T006 [blockedBy: T001] Red-first 取证：先创建 `tests/contract/test_self_explanatory_constitution.py` 的最小断言（模板标题集合含 `Self-Explanatory Structure (不言自明)`），运行 `python3 -m pytest tests/contract/test_self_explanatory_constitution.py -q`，确认它因标题尚不存在而失败；把命令、真实失败输出与退出码写入 `.specify/specs/082-self-explanatory-integration/notes/red-first-evidence.md`。不得把既有 `test_constitution_double_landing.py` / `test_instructions_section_propagation.py` 的通过当作红旗——它们不引用 STR-001。 [green: contracts/constitution-double-landing.contract.md#C-1]

**Checkpoint**: 前提齐备且红旗取证已留痕;可以并行开工 P1 的三个故事(镜像、宪章、instructions 互不写同一文件)。

---

## Phase 3: User Story 1 - 宪章生成后，原则自动出现在框架与客户项目 (Priority: P1) 🎯 MVP

**Goal**: `STR-001` 落在**三个表面**——宪章模板、宪章生成器的必含清单、live 宪章——并由一条能红的守卫钉住。

**Independent Test**: 在临时副本中删掉模板里的原则块,运行 `test_c10_removing_a_watchlist_principle_breaks_c7`(经参数化指向副本)断言转红;在真实树上同一组测试全绿。

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: 先写测试、确认它红,再改制品**。C-1/C-3/C-4 的断言写在一个新模块里,避免改写既有文件的加载期常量(C-5/C-7/C-8/C-9 的计数常量在 T016 才动)。

- [X] T007 [P] [US1] 扩展 T006 已创建的 `tests/contract/test_self_explanatory_constitution.py`,实现 C-1/C-3/C-4:模板标题集合含 `STR-001`、标题匹配器对合成名册(一个本仓从未用过的罗马数字)仍命中、任何测试/模板行不钉具体数字 [green: contracts/constitution-double-landing.contract.md#C-3]
- [X] T008 [P] [US1] 在同一新模块实现 C-2/C-6 的结构检查器:claim 句以冒号结尾、3–6 条含 `MUST` 的逻辑 bullet、物理行 < 100 字符、`Rationale:` 前恰好一个空行且 1–4 句、五条内容义务逐条命中、正文含 `STR-004` 且声明「引用不复述」、框架源路径 `STR-002` 仅作 owner 位置出现 [green: contracts/constitution-double-landing.contract.md#C-6]
- [X] T009 [P] [US1] 在同一新模块实现 C-7 的双侧集合判定:每个观察名单标题同时在模板标题集与生成器必含名单的名字集里(集合成员、非子串) [green: contracts/constitution-double-landing.contract.md#C-7]
- [X] T010 [P] [US1] 在同一新模块实现 C-20 的否定断言:从 `shared/definitions/self-explanatory-definitions.md` 与 `.specify/shared/definitions/self-explanatory-definitions.md` 两侧解析 owner 的 `##` 标题,断言其中**没有一条**出现在 `templates/constitution-template.md` 或 `templates/instructions-template.md` 内;同时实现 C-21 的摘要上限(小节正文剥离指针行后按房式句界计数 ≤ 2 句)——两条条款同属「reference, not copy」的机器可判形态,且同为单一新模块内的读断言,故由本行一并认领 [green: contracts/mirror-distribution.contract.md#C-20] [green: contracts/mirror-distribution.contract.md#C-21]

### Implementation for User Story 1

- [X] T011 [US1] [blockedBy: T008] 在 `templates/constitution-template.md` 的下一个可用编号处新增标题 `Self-Explanatory Structure (不言自明)` 的原则:五条内容义务各一条 bullet、正文指向 `.specify/shared/definitions/self-explanatory-definitions.md` 并要求「引用不复述」、带「不得引入新机具」上限句;硬换行 < 100 字符、`Rationale:` 段落 1–4 句 [green: contracts/constitution-double-landing.contract.md#C-2]
- [X] T012 [US1] [blockedBy: T011] 校验该原则块对确认门控扫描器的编译模式零命中: `python3 -c` 加载 `scripts/python/scan-confirmation-gates.py` 的 `BLOCKING_RE` 对块内逐行 `finditer`,输出 `hits: []` 写入 `notes/pre-change-measurements.md`;命中即改写措辞,**不得**改扫描器或它的冻结基线 [green: contracts/constitution-double-landing.contract.md#C-8]
- [X] T013 [US1] [blockedBy: T011] 在 `skills/internal/manage-constitution/SKILL.md` 的 `- **MUST include**` 块内新增子条目 `  - **Self-Explanatory Structure (不言自明)** — …`,带真源锚点(`.specify/shared/definitions/self-explanatory-definitions.md`)与「引用不复述」从句;不带第二份原则清单,命令模板保持委派形态 [green: contracts/constitution-double-landing.contract.md#C-5]
- [X] T014 [US1] [blockedBy: T013] 同步镜像 `python3 scripts/python/sync-mirrors.py --write --only templates --only skills`(或全量 `--write` 后复查),使 `.specify/templates/constitution-template.md` 与 `.specify/skills/internal/manage-constitution/SKILL.md` 与本阶段源文件逐字节一致;本行不提交,提交在 T039 [green: contracts/mirror-distribution.contract.md#C-24]
- [X] T015 [US1] [blockedBy: T014] 运行 US1 守卫的 US1 子集确认转绿: `python3 -m pytest tests/contract/test_self_explanatory_constitution.py -q -k 'not c21'`（C-21 的 instructions 小节要到 T022 才存在；该条的红/绿配对归 T024/T051，不在本行的 US1 子集里）；把该次输出与 T006 的红旗记录成对写入 `notes/red-first-evidence.md`
- [X] T016 [US1] [blockedBy: T015] 扩展既有守卫 `tests/contract/test_constitution_double_landing.py`:把 `Self-Explanatory Structure (不言自明)` 追加为 `DOUBLE_LANDING_WATCHLIST` 的最后一项,并把 `TEMPLATE_COUNT` 17→18、`LIVE_COUNT` 18→19、`COMMAND_COUNT` 10→11 各 +1,每条注记同步写上改动来源;保持「数值不参与标题匹配」的既有形态 [blockedBy: T011,T013] [green: contracts/constitution-double-landing.contract.md#C-9]
- [X] T017 [US1] [blockedBy: T016] live 宪章落点:按 `skills/internal/manage-constitution/SKILL.md` 的模板引导路径在 `.specify/memory/constitution.md` 的下一个可用编号处新增同一原则(从**模板**取标题与正文,编号取 live 自身)、把 `**Version**:` 按 MINOR 推进,并在文件顶部前置 Sync Impact Report(HTML 注释、写明版本箭头、点名本次新增原则、记录必含清单条目数与确认门控 total 不变) [green: contracts/constitution-double-landing.contract.md#C-4]
- [X] T018 [US1] [blockedBy: T017] 变异腿 M-1/M-2:在 `mktemp -d` 副本上分别删除模板原则块与必含清单子条目,断言 C-3/C-7 的对应成员判定转 `False`、并断言真实文件未被触碰(输出写入 `notes/red-first-evidence.md`) [green: contracts/constitution-double-landing.contract.md#C-1]

**Checkpoint**: US1 可独立验收——三表面同标题、live 版本已推进、两条变异腿都能红。

---

## Phase 4: User Story 2 - instructions 输出后，代理能看见规则并到达 owner (Priority: P1) 🎯 MVP

**Goal**: 模板与 live instructions 都携带常驻小节 `## Self-Explanatory Structure (不言自明)`,小节只放摘要 + 运行时指针,预算常量按最小必要幅度上调并记录理由。

**Independent Test**: 在临时夹具(已有自定义 live instructions)上运行 `scripts/bash/generate-instructions.sh`,断言小节被增量注入、既有内容字节不变、第二次运行零注入。

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T019 [P] [US2] 在 `tests/contract/test_instructions_section_propagation.py` 新增 C-10/C-11 断言:模板含顶层 `## Self-Explanatory Structure (不言自明)` 且正文含 `.specify/shared/definitions/self-explanatory-definitions.md`；句数上限由 T010 的 C-21 断言，本行不重复实现 [green: contracts/instructions-propagation.contract.md#C-11]
- [ ] T020 [P] [US2] 在同一文件新增 C-14 模板侧变异断言:**不读 live 文件**,仅断言模板与生成器 reconcile 输入(渲染后的模板文本)含该标题;并在末尾断言真实模板仍携带该标题(反空真哨兵) [green: contracts/instructions-propagation.contract.md#C-14]
- [ ] T021 [P] [US2] 在 `tests/contract/test_instructions_size_budget.py` 增一条从 `scripts/bash/generate-instructions.sh` 读取常量、断言 `.specify/instructions.md` 尺寸 `<= 常量 - 1` 的派生断言(不硬编码常量值、不复制理由) [green: contracts/instructions-propagation.contract.md#C-17]

### Implementation for User Story 2

- [ ] T022 [US2] [blockedBy: T019] 在 `templates/instructions-template.md` 新增小节 `## Self-Explanatory Structure (不言自明)`,位置在 `## Grounded Naming` 之后、`## Bilingual Expression (双语表述)` 之前(既有小节零重排),正文 = ≤ 2 句摘要 + 指向 `.specify/shared/definitions/self-explanatory-definitions.md` 的指针行 [green: contracts/instructions-propagation.contract.md#C-10]
- [ ] T023 [US2] [blockedBy: T022] 上调 `scripts/bash/generate-instructions.sh` 的 `INSTRUCTIONS_BUDGET_BYTES`:取「1024 的整数倍、且至少留 1024 B 余量」的最小值(实测 live 32739 B + 新小节后复测),在常量上方注释里写旧值、新值、本次实测尺寸与理由(本小节),并按 plan T-001 记录规则;不得删改任何既有小节腾空间 [green: contracts/instructions-propagation.contract.md#C-18]
- [ ] T024 [US2] [blockedBy: T023] 用同一变更重建 live 落点: `bash scripts/bash/generate-instructions.sh`,读 `Injected` / `Instructions size` / `BUDGET` 行(必须为 `within`),把整条输出与 `wc -c` 结果写入 `notes/quickstart-run.md`;再跑一次确认幂等(`Section reconcile: live instructions already carry all template sections.`)；随后运行 `python3 -m pytest tests/contract/test_self_explanatory_constitution.py -q -k c21` 确认 C-21 转绿，把命令、输出与退出码写入 `notes/red-first-evidence.md`（作为 C-21 的红/绿配对） [green: contracts/instructions-propagation.contract.md#C-15]
- [ ] T025 [US2] [blockedBy: T024] 断言兼容链接仍是链接:`test -L CLAUDE.md && test -L QODER.md && test -L AGENTS.md`,并读 `readlink` 目标解析到 `.specify/instructions.md`;把四条命令与输出写入 `notes/pre-change-measurements.md`;若任一被改写为副本即停下上送,不得手建链接 [green: contracts/instructions-propagation.contract.md#C-16]
- [ ] T026 [US2] [blockedBy: T024] 同步镜像 `python3 scripts/python/sync-mirrors.py --write --only templates --only scripts`,使 `.specify/templates/instructions-template.md` 与 `.specify/scripts/bash/generate-instructions.sh` 与源逐字节一致 [green: contracts/instructions-propagation.contract.md#C-13]
- [ ] T027 [US2] [blockedBy: T026] 变异腿 M-3/M-4:在 `mktemp -d` 副本上删除模板小节并断言 C-14 的模板侧断言转红(仅对副本运行);再在无小节的夹具上运行生成器并断言零注入,随后断言真实模板仍含该标题 [green: contracts/instructions-propagation.contract.md#C-12]
- [ ] T028 [US2] [blockedBy: T008] C-19 落点:检查 `templates/instructions-template.md` § Documentation Map 是否需要为 owner 增行——增行则指向 `.specify/shared/definitions/self-explanatory-definitions.md`,不增则把「不增行、owner 经小节指针可达」这一决定写入 `.specify/specs/082-self-explanatory-integration/test-evidence/tasks-stage-premises.md` 的追加节 [green: contracts/instructions-propagation.contract.md#C-19]

**Checkpoint**: US2 可独立验收——模板/live 双落点、预算 `within`、注入幂等、链接未变、模板侧变异能红。

---

## Phase 5: User Story 3 - shared owner 被镜像并随 init 分发 (Priority: P1) 🎯 MVP

**Goal**: 三份 owner 文档的源/镜像逐字节一致,`--check` 退出 0,且只存在于镜像的文件永不被当作已分发。

**Independent Test**: 临时目录 `specify init` 后列出 `.specify/shared/` 下三处路径;临时副本中改一个字节让镜像漂移,断言参数化 parity 用例转红并点名 source→mirror 对。

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T029 [US3] 在 `tests/contract/test_self_explanatory_distribution.py` 新建模块实现 C-26 的分发表：在临时目录创建 venv，执行 `python3 -m venv .venv && . .venv/bin/activate && python3 -m pip install -e "$(git rev-parse --show-toplevel)"`（记录命令与退出码），再执行 `specify init --here --ai claude --no-git --skip-tls`，逐条列出三处 `.specify/shared/...` 路径并报告每条的在场；任何一条缺失即失败。不得使用已发布 CLI 的陈旧资源作为豁免；若 venv/editable install 不可用，返回 `ANOMALY: <一句话事实>`。 [green: contracts/mirror-distribution.contract.md#C-26]

### Implementation for User Story 3

- [ ] T030 [US3] [blockedBy: T004] 确认三份源文档以**新文件**身份进入版本控制: `git add shared/definitions/self-explanatory-definitions.md shared/guidelines/self-explanatory.md shared/workflow/best-practice-optimization.md` 后 `git status --short` 应显示三个 `A`;不得把「`.specify/shared/` 下已存在」读作已分发,也不得把 mtime 相同当作「未写入」的证据 [green: contracts/mirror-distribution.contract.md#C-28]
- [ ] T031 [US3] [blockedBy: T030] 运行镜像引擎写入三份镜像: `python3 scripts/python/sync-mirrors.py --write --only shared`,随后 `python3 scripts/python/sync-mirrors.py --check` 必须退出 0 且 `shared/ == .specify/shared/` 为 `ok`(实测基线 65 文件,本阶段后应为 68);把两次输出写入 `notes/pre-change-measurements.md` [blockedBy: T005] [green: contracts/mirror-distribution.contract.md#C-23]
- [ ] T032 [US3] [blockedBy: T031] 逐对字节比对:`cmp shared/definitions/self-explanatory-definitions.md .specify/shared/definitions/self-explanatory-definitions.md` 与另两对,三条命令退出码全 0;把命令与退出码追加到 `notes/quickstart-run.md` [green: contracts/mirror-distribution.contract.md#C-22]
- [ ] T033 [US3] [blockedBy: T031] 补齐 in-scope 行 RS-004 的接口来源(承载 FR-007):让三份文档进入分发输入(框架源 `shared/` 树即 `specify init` 的拷贝源,见 `src/specify_cli/__init__.py` 的 shared 拷贝段);以 `python3 -c "import specify_cli, os; print(os.path.dirname(specify_cli.__file__))"` 确认资源树位置,并记录「源树必须有、镜像独有不算数」这一判据的复算命令;本行不新增任何拷贝逻辑,只确认既有拷贝段覆盖三份新文件 [green: contracts/mirror-distribution.contract.md#C-28]
- [ ] T034 [US3] 把 docs 链接守卫放在 `tests/contract/test_self_explanatory_distribution.py` 内(与 T029 同一新文件,故不带 [P])实现 C-27:从 `docs/concepts/self-explanatory.md` 提取所有行内代码里的仓相对 `.md` 路径,断言每条在源树**与**其镜像树中存在;`docs/` 页面自身按显式允许清单只判源树,允许清单每条带一行理由;不引入独立链接检查引擎 [green: contracts/mirror-distribution.contract.md#C-27]
- [ ] T035 [P] [US3] 只读复核 `docs/concepts/self-explanatory.md` 的指针页形态:确认它指向 `shared/definitions/self-explanatory-definitions.md`、`shared/guidelines/self-explanatory.md` 与 `shared/workflow/best-practice-optimization.md`,不复制 owner 正文;需要补的只是一行退役名史注(`望文生义` 仅作变体);复核结果(是否需补该行、以及该行内容)写入 `notes/pre-change-measurements.md`,本行不改写该页:确认它指向 `shared/definitions/self-explanatory-definitions.md`、`shared/guidelines/self-explanatory.md` 与 `shared/workflow/best-practice-optimization.md`,不复制 owner 正文;需要补的只是一行退役名史注(`望文生义` 仅作变体) [green: contracts/mirror-distribution.contract.md#C-28]
- [ ] T036 [US3] 记录分发探针结论并给出替代读法:在 `notes/quickstart-run.md` 写下 2026-11-05 的 `specify init` 实测输出(临时目录出现 `.specify/shared/` 落地目录但三份文档缺席,因已安装 CLI 的资源早于本特性),并写明完整判据须在 `pip install -e .` 之后重跑;若临时目录里 `.specify/shared/` 落地目录本身缺席则停下上送(见 § Environment Prerequisites)
- [ ] T037 [US3] [blockedBy: T032] 变异腿 M-5:在 `mktemp -d` 的镜像树副本上改一字节,用引擎的 `compare_pair` 比对并断言报告 DIFF 且消息含 source→mirror 对;随后断言真实镜像树未被改动 [green: contracts/mirror-distribution.contract.md#C-24]
- [ ] T038 [US3] [blockedBy: T034] 变异腿 M-6:在 docs 页副本上删掉 `shared/definitions/self-explanatory-definitions.md` 这条行内路径,运行链接守卫对副本并断言 C-27 的路径提取→存在断言转红;真实页未被改动 [green: contracts/mirror-distribution.contract.md#C-28]

**Checkpoint**: US3 可独立验收——引擎退出 0、三对字节相同、分发判据有记录的可复算命令、两条变异腿都能红。

---

## Phase 6: User Story 4 - 测试与词汇表把集成钉住 (Priority: P2)

**Goal**: glossary 登记 `STR-003`(旧名仅作变体、状态 `proposed`),并把「镜像只跑一部分」的风险钉住:既有的参数化 parity 套件确实覆盖了三份新文档,且既有机制套件全绿。

**Independent Test**: 真实树上跑 `tests/contract/test_glossary_mechanism.py` 与 `tests/contract/test_mirror_parity_suite.py -k 'self-explanatory or best-practice-optimization'`,前者绿、后者恰好选中三个参数且绿。

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T039 [P] [US4] 在 `tests/contract/test_self_explanatory_glossary.py` 实现 C-29 的条目断言:恰好一条 canonical 为 `不言自明 (Self-explanatory)` 且该行 `origin=auto`、`status=proposed` [green: contracts/glossary-integration.contract.md#C-29]
- [ ] T053 [P] [US4] 在同一新模块实现 C-34 的命名一致性断言:`STR-001` 与 `STR-003` 的共享片段(去掉括号语言后的主体)一致,且本特性新增的任一文档不引入第三种形态(如 `Self-explanatory Structures`、或把 `望文生义` 当作现名)(C-20 的同一形态由 T010 认领,本行只认领命名面) [green: contracts/glossary-integration.contract.md#C-34]
- [ ] T040 [P] [US4] 在同一模块实现 C-30 的按行解析断言:逐行解析 store 表格,断言不存在第二行把 `望文生义` 或 canonical 串放在 canonical 列;并断言 `glossary-utils.py --action validate` 退出 0 [green: contracts/glossary-integration.contract.md#C-30]
- [ ] T041 [P] [US4] 在同一模块实现 C-32:该行 meaning 单元格含一条仓相对路径,断言该路径存在(概念 owner 可达) [green: contracts/glossary-integration.contract.md#C-32]
- [ ] T042 [P] [US4] 在同一模块实现 C-22/C-24 的参数化复核断言:从 `MIRROR_PAIRS` 派生的参数表必须含有三份新文档对应的三个参数(参数 id 含三处路径),缺失即失败——本行**不新建**第二份对表,只断言引擎枚举已覆盖;该断言与 C-26 同属「新文档确实进入镜像与分发枚举」这一命题,由同一模块承载,故与 T029 共同认领 C-26(两条断言一对一) [green: contracts/glossary-integration.contract.md#C-29]

### Implementation for User Story 4

- [ ] T043 [US4] [blockedBy: T039] 经引擎登记词条: `python3 scripts/python/glossary-utils.py --action add --canonical "不言自明 (Self-explanatory)" --variants "望文生义" --meaning "<摘要 + 真源路径 shared/definitions/self-explanatory-definitions.md>" --origin auto --status proposed`;登记前先跑 `--action detect-conflict` 并把结果留痕;MUST NOT 手工编辑表格 [green: contracts/glossary-integration.contract.md#C-31]
- [ ] T044 [US4] [blockedBy: T043] 确认状态不被流程推进:断言该行 `status` 仍为 `proposed`,并在 `notes/pre-change-measurements.md` 记一行「提升属用户动作(data-model T-B / 需求 A6),本特性不改写」 [green: contracts/glossary-integration.contract.md#C-33]
- [ ] T045 [US4] [blockedBy: T043] 断言既有机制套件未受影响且未改动: `git diff --stat tests/contract/test_glossary_mechanism.py` 必须为空,`python3 -m pytest tests/contract/test_glossary_mechanism.py -q` 退出 0 [green: contracts/glossary-integration.contract.md#C-31]
- [ ] T046 [US4] [blockedBy: T030] 确认 `/speckit.improve` 未被接线:`git diff --stat templates/commands/improve.md` 为空,且 `grep -c 'best-practice-optimization' templates/commands/improve.md` 为 0;把两条命令与输出写入 `notes/pre-change-measurements.md`;该工作在 `OI-082-01` 名下,任何验收不得把「文档已镜像」读作「命令已接线」 [green: contracts/mirror-distribution.contract.md#C-28]

**Checkpoint**: US4 可独立验收——词条可检索、旧名非第二 canonical、parity 参数覆盖三份新文档、既有机制套件绿。

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: 三故事合流后的整体核对:名称一致、镜像总表、成本与结构、以及 Feature 索引。

- [ ] T047 [P] 名称一致性终检: `grep -cF 'Self-Explanatory Structure (不言自明)' templates/constitution-template.md templates/instructions-template.md .specify/memory/constitution.md .specify/instructions.md` 逐文件各 ≥ 1,且 `grep -cF '.specify/shared/definitions/self-explanatory-definitions.md'` 在每个客户端面向输出 ≥ 1;输出写入 `notes/quickstart-run.md`
- [ ] T048 [blockedBy: T014,T026,T031] 镜像总表核对: 逐行对照 plan.md § Mirror Obligations 的十行,`python3 scripts/python/sync-mirrors.py --check` 退出 0;`python3 scripts/python/regen-command-copies.py --check` 打印 `OK: all per-tool command copies match the source templates.`(本特性未改 `templates/commands/`,这条是未变面断言)
- [ ] T049 [blockedBy: T012,T024] 成本与结构终检: `bash scripts/bash/generate-instructions.sh` 的 `BUDGET` 行为 `within`,并把「旧值 → 新值 / 本次实测尺寸 / 理由」三件套写进同一提交的提交说明(plan T-001、C-18);`python3 scripts/python/scan-confirmation-gates.py --json` 的 `total` 仍为 27(与 T002 基线相同)→ 本特性零新增门控命中
- [ ] T050 [blockedBy: T047] Feature 索引同步: `.specify/memory/features/082.md` § Latest Review 追加 tasks 阶段条目(行数统计、`validate-tasks.py` 结论、条款认领数),`.specify/memory/features.md` 的 082 行状态**保持 `Planned`**(`Implemented` 属 `/speckit.implement`)
- [ ] T051 [blockedBy: T006] 红旗取证收尾: 把 T006 的红、T015/T024/T031/T043 的绿成对整理进 `notes/red-first-evidence.md`,每条含命令、真实输出与退出码;缺任一配对即视为该守卫未被证明有效
- [ ] T052 结构校验终检: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/082-self-explanatory-integration/tasks.md` 退出 0;并跑 § Completion Gate 的 GATE-1…GATE-4 四条检查,把四条命令与输出写入 `notes/quickstart-run.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖,可立即开始
- **Foundational (Phase 2)**: 依赖 Setup;**阻塞全部用户故事**
- **User Stories (Phase 3–6)**: 均依赖 Foundational;三个 P1 故事写目标互不相同(宪章三表面 / instructions 两表面+生成器 / shared 镜像与 docs),可并行;US4(P2)可在三个 P1 之后或与 T030 完成后的镜像工作并行
- **Polish (Phase 7)**: 依赖全部用户故事完成

### User Story Dependencies

- **US1 (P1)**: Foundational 之后即可;不依赖其它故事。T017(live 宪章)必须先有 T011(模板原则)——同一标题,不是同一文件
- **US2 (P1)**: Foundational 之后即可;与 US1 无共享写目标(除 `templates/instructions-template.md` 由 T010 只读、T022 写,已用 blockedBy 排序)
- **US3 (P1)**: Foundational 之后即可;T030 的 `git add` 与 T031 的 `--write` 是同一文件的先写后验关系,故串行
- **US4 (P2)**: T042 需要 T031 的镜像已就绪;T046 需要 T030 已完成。其余行与三 P1 无共享写目标
- **模板/命令列表的同文件约束**: `templates/instructions-template.md` 被 T010(只读)、T022(写小节)与 T004(路径)引用,T010 不写该文件,故不构成并发写冲突

### Within Each User Story

- 测试先写并**确认红**(T006 已把红旗机制留下),再动手制品
- 新断言写进**新模块**直到该故事最后一步,避免改写既有文件的加载期常量造成跨故事串行
- 计数常量的更新(T016)只在该故事的模板与必含清单都落地后做——它是 TDD 的迁移/回归例外
- 每个故事以一次 checkpoint 自查收尾

### Parallel Opportunities

- Setup:T001 与 T002 可并行(不同文件)
- Foundational:T004 与 T005 **不并行**——两者都写 `notes/pre-change-measurements.md`(T004 的 `ls -l`、T005 的引擎输出),按序号串行
- US1:T007、T008、T009、T010 四行同属新建的 `tests/contract/test_self_explanatory_constitution.py`,故不带 `[P]`,按序号串行;它们仍可全部先于实现行(T011 起)完成
- US2 与 US3 与 US1 三故事之间可并行(写目标互不相交)
- US4:T039、T053、T040…T042 同属一个新模块,按序号串行;T035(只读复核,写 `notes/`)可与 T031 并行,T034 与 T029 同属新文件故不并行

### Adjudicated validator warnings (generated 2026-11-05)

`validate-tasks.py` exits 0 with 32 warnings. Each class is adjudicated by the rows' actual write
targets and scope — never by deleting a cited path from a row:

- **`green-cross-phase` (18) — accepted, partitioned by story.** Each contract's clauses are claimed
  in the order the delivering story fixes them: `constitution-double-landing.contract.md` runs
  C-1/3/4 (test module) → C-2/C-6 → C-8 → C-5 → C-9 → C-4 …; `mirror-distribution.contract.md` is
  claimed across US1 (C-24) → US3 (C-28, C-23, C-22, C-27) → US4 (C-26); the instructions contract
  runs C-21/C-14/C-17 (test rows) → C-10 → C-18 → C-15 → C-16 → C-13 → C-12 → C-19. The clause
  ordinals therefore do not follow row order *inside a file* — that is the partition, not a defect:
  each `[green:]` row is the row that turns that clause green within its own phase, and the
  implementer reads attribution per row.
- **`green-clause-collision` (11) — accepted; each collision is a different assertion on the same
  clause by rows that own different files.** Pairs: C-26 in T029 (`specify init` on an installed CLI)
  and T042 (`MIRROR_PAIRS` enumeration); C-29 in T039 (entry fields) and T042 (parameter presence);
  C-31 in T043 (the write) and T045 (the unchanged-suite assert); C-1 in T006 (the Red capture) and
  T007; C-22 in T004 (existence) and T032 (byte identity); C-24 in T014 (mirror write) and T037
  (mutation leg); C-28 in T030, T033, T035, T038, T046 (five distinct FR-007 / C-27 / "distribution is
  not wiring" faces).
- **`green-path-divergence` (3) — accepted, and sequenced.** T006 captures the Red baseline into the
  two existing suites (it turns nothing green), while T016 and T019 each own one clause group of one
  of them; T029 and T034 both write the new distribution module by design. In every pair the rows'
  own `[blockedBy:]` tags fix the order, which is the remedy the warning text names.

> [P] 裁决说明:`validate-tasks.py` 的 `parallel-safe` 检查只看同阶段同文件的**写**目标。T007–T010 共享一个新建测试文件,故该组会被机器判为同文件写——执行时的顺序即序号顺序,不并行;这与上一条「可先于实现开始」的语义不冲突。T014/T026/T031 各自 `--write` 不同目录,互不冲突。

## Parallel Example: User Story 1

```bash
# 先写四条断言(同一个新模块,按序号顺序执行):
python3 -m pytest tests/contract/test_self_explanatory_constitution.py -q   # 预期红

# 再落三个表面的制品:
#   1) templates/constitution-template.md 新增原则
#   2) skills/internal/manage-constitution/SKILL.md 新增必含子条目
#   3) .specify/memory/constitution.md 经模板引导路径新增 + 版本推进 + Sync Impact Report
```

## Implementation Strategy

### MVP First

**MVP scope rule**: MVP = **三个同优先级 P1 故事的全部**(US1 + US2 + US3)。只做其一不构成可交付增量:原则与 instructions 里的指针若没有镜像就是悬空指针(镜像必须同时随源进入版本控制),而镜像若不被 `specify init` 分发就到不了任何客户项目(需求 US3 的 Why this priority 已写明这一依赖)。US4(P2)是回归防线,不属 MVP,但它是 DoD-4 的组成部分。

1. 完成 Phase 1(基线冻结)与 Phase 2(前提复核 + 红旗取证)
2. 完成 US1 + US2 + US3 三个 checkpoint
3. **STOP and VALIDATE**:逐故事跑各自 Independent Test,再跑 § Completion Gate 的 GATE-1…GATE-3
4. 完成 US4 与 Phase 7,最后跑 GATE-4(closure 阶段才有 `verification.md`,此处只记录它尚未可跑)

### Incremental Delivery

1. Setup + Foundational → 基线可对照、红旗已留痕
2. US1 → 三表面同标题,live 版本推进 → 独立验收
3. US2 → 双落点 + 预算 `within` → 独立验收
4. US3 → 镜像逐字节 + 分发判据 → 独立验收
5. US4 → glossary 与覆盖复核 → 独立验收
6. Polish → 名称一致性、镜像总表、成本三件套、Feature 索引

---

## Notes

- 本文件的每个 `[green:]` 认领都满足:合同路径相对本文件目录可解析、条款 id 在该合同内存在、同一合同内条款序号随行序单调递增(条款按故事分组认领,故事即分区)
- 计数类前提均已在本轮实测并把命令与输出写入 `test-evidence/tasks-stage-premises.md`;未执行的复算命令不得作为结论
- 镜像判据是 **keep**,不是 **reach**:三份镜像在任务开始时已存在且 `cmp` 相同,义务是「后续编辑不得让 `MISS`/`DIFF` 重现」
- 既有红 `tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged` 属 Feature 050 的冻结基线(plan EP-003,`Decision: fallback`),本特性不修、不掩,每次定向运行都点名
- `/speckit.improve` 接线不在本特性(`OI-082-01`);本文件没有任何行把「文档已镜像」写成「命令已接线」
