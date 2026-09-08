# Tasks: 主动触发机制(Proactive Flow Trigger)

**Requirement ID**: 050
**Requirement Key**: 050-proactive-flow-trigger
**Related Feature**: 050 Proactive Flow Trigger(主动触发机制) — from `.specify/memory/features.md`
**Input**: Design documents from `.specify/specs/050-proactive-flow-trigger/`
**Prerequisites**: plan.md ✅ · requirements.md ✅ · data-model.md ✅ · contracts/(4 份 / **61** 条款,含 analyze 2026-09-08 补强的 trigger-engine C-19…C-23 与 discipline-doc C-8…C-16)✅ · quickstart.md ✅ · feature-ref.md ✅ · research.md ❌(Phase 0 findings 内联于 plan.md D-1…D-10)

**Tests Mode**: **ON** — Constitution Principle IV「Test-First & Contract-Driven Implementation」强制(测试先于实现 Red-Green-Refactor、纯函数必须有单元测试、验收场景转为自动化测试)。**混合型判定**:Principle VII 的 template-only 门(`constitution.md:95`「features with no executable runtime code judge Test-First as Partial」)**只**覆盖本文档/模板制品面(指令章节、纪律文档、种子 JSON → 结构契约测试);`scripts/python/trigger-utils.py` 是**可执行运行时代码**,故 template-only 豁免对其不适用,单元测试与集成测试为强制。

**Organization**: 任务按 user story 分组(US1/US2 = P1 = MVP;US3/US4 = P2),每个 story 可独立实现与测试。

**⚠️ 结构性串行约束(实现前必读)**:`scripts/python/trigger-utils.py` 是**单一文件引擎**(房式约定,承 `feedback-utils.py` / `derive-utils.py` 单文件形态),US2 / US3 / US4 三个故事都要改它 → 这三个故事的**实现任务互相串行**(以 `[blockedBy]` 表达),不得标 `[P]`。测试文件按故事拆分(4 契约 + 1 单元 + 3 集成),故**测试任务跨故事可并行**。

## Definition of Done (DoD)

- DoD-1: 全部 51 项任务为 `[X]` 或带理由的 `[~]`;`grep -cE '^- \[[ >]\]' tasks.md` 返回 0
- DoD-2: 8 个新测试文件全绿,且全套件名字级回归 `comm -13 baseline-failed.txt current` 输出为空(零新增失败)
- DoD-3: 4 份契约的 **61 条款**逐条有对应断言并通过(trigger-section 12 / trigger-engine **23** / seed-derivation 10 / discipline-doc **16**)
- DoD-4: plan.md § Mirror Obligations 表 **7 行**中,**6 行有镜像产物的**全部有显式写任务 + 显式验任务并逐行 diff 通过;**第 6 行(「不改任何命令模板」)按设计无写任务**,其验证形态是 `regen-command-copies.py --check` 保持 exit 0(T047),该行豁免于「写任务」要求(analyze L-05)
- DoD-5: 门控扫描 `total` **等于 T002 冻结的前值**(撰写时实测 23)、`violations` **0**;复杂命令分类 **19**、docs-step **16**、probe internal objects **73** 三者均未变(零扰动承诺)
- DoD-6: quickstart.md **6 场景**真实走查通过,证据留痕于 `verification.md`
- DoD-7: `verification.md` 为 **SC-001…SC-015** 逐条记录 `pass` 或 `deferred`(附因)
- DoD-8: Tool 记录 `.specify/memory/tools/trigger-utils.py.md` 已建,且 `.specify/memory/tools.md` 与 `.specify/tools/*.json` 经 `refresh-tools.sh` **再生**(未手改派生清单)

**DoD Status**: pending   <!-- flip to `green` only when every DoD-N row above is satisfied -->

## Completion Gate

- GATE-1: 全套件零新增失败 — check: `bash scripts/bash/run-tests.sh --names-out /tmp/cur-failed.txt && comm -13 .specify/specs/050-proactive-flow-trigger/baseline-failed.txt /tmp/cur-failed.txt`(输出为空)
- GATE-2: 五对镜像全绿(scripts 对为 STRICT) — check: `python3 scripts/python/sync-mirrors.py --check`(exit 0)
- GATE-3: 命令副本零变动(本特性不改任何命令模板) — check: `python3 scripts/python/regen-command-copies.py --check`(exit 0)
- GATE-4: 门控预算未破(整数余量为 0) — check: `python3 scripts/python/scan-confirmation-gates.py --summary`(total **等于 `baseline-gates.json` 中 T002 冻结的前值** / violations 0)+ `python3 -m pytest tests/contract/test_confirmation_gates_sweep.py -q`(绿)
- GATE-5: 无开放任务行 — check: `grep -cE '^- \[[ >]\]' .specify/specs/050-proactive-flow-trigger/tasks.md`(返回 0)
- GATE-6: 每条 SC 有状态行 — check: `grep -oE 'SC-0[0-9]{2}' .specify/specs/050-proactive-flow-trigger/verification.md | sort -u | wc -l`(返回 15)
- GATE-7: probe 注册表未扰动 — check: `python3 scripts/python/feedback-utils.py --action probes --validate`(exit 0,internal 仍 73)
- GATE-8: 零扰动计数未变 — check: `python3 -m pytest tests/contract/test_feedback_command_classification.py tests/contract/test_docs_step_injection.py -q`(绿,分类 19 / docs-step 16 未改写)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行(不同文件、无未完成依赖)
- **[Story]**: US1 / US2 / US3 / US4;Setup、Foundational、Polish 阶段**不带**故事标签
- **[blockedBy: Txxx,Tyyy]**: 显式依赖标签,列出的任务全部 `[X]` 之前不得开工
- **状态符**: `- [ ]` 开放 · `- [>]` 已认领(多代理运行) · `- [X]` 关闭 · `- [~]` 附因延后

## Path Conventions

框架仓形态(Principle XI「两顶帽子」):**框架源码面** = `templates/`、`shared/`、`scripts/`、`src/specify_cli/`、`tests/`;**本仓客户端运行面** = `.specify/`(经同一 init/refresh 流安装)。本特性所有新增制品都落在**框架源码面**并靠既有 `sync-mirrors.py` / init 拷贝抵达运行面 —— 每个改动前先确认戴的是哪顶帽子(plan.md § Mirror Obligations 逐行列出)。

## Environment Prerequisites

本特性**不需要** docker daemon、可拉取镜像、活动集群或特殊硬件;无网络调用。仅需:

- `python3` ≥ 3.8(`pyproject.toml` 既有下限)与 `pytest`
- POSIX symlink 支持(macOS / Linux)
- 一个可写的临时根(场景 1 的 `specify init` 走查用 `mktemp -d`)

上述由 T002 在生成期实测确认,不留给 `/speckit.implement` 中途发现。

---

## Phase 1: Setup

**Purpose**: 冻结基线、探测环境、预检派生来源 —— 使后续每个"零新增/零变动"承诺都有可比对的前值

- [X] T001 冻结名字级失败基线:运行 `bash scripts/bash/run-tests.sh --names-out .specify/specs/050-proactive-flow-trigger/baseline-failed.txt`,并在该文件首行注释记录条目数与冻结时间(参照 `.specify/specs/049-docs-reconcile/baseline-failed.txt` 的 47 条形态)
- [X] T002 [P] 探测环境前值并落 `.specify/specs/050-proactive-flow-trigger/baseline-gates.json`:`python3 --version`(≥3.8)、`pytest --version`、`python3 scripts/python/sync-mirrors.py --check` 退出码(期望 0)、`python3 scripts/python/scan-confirmation-gates.py --summary` 的 total/violations(期望 23/0)、`python3 scripts/python/regen-command-copies.py --check` 退出码(期望 0)、`python3 scripts/python/feedback-utils.py --action probes --validate` 的 internal objects 数(期望 73)、`docker info` 是否可用(仅记录,本特性不依赖)
- [X] T003 [P] 种子派生来源预检:对 `data-model.md` §命名情境表的 **13** 条 provenance anchor 逐条打开其 `provenance.file`,按 `anchorKind` 定位对应段落(`handoffs` → `## Handoffs` 段;`owning-section` → `anchor` 指名段落),确认被引流程名与逐字引文当前确实出现在该段内;把结果(**13/13** 或失败清单)记入 `.specify/specs/050-proactive-flow-trigger/baseline-gates.json` 的 `seedAnchorsPrecheck` 字段。此为 `seed-derivation.md` C-7 的人工预飞——若某 anchor 在开工前就已陈旧,C-7 的失败与本特性无关,须先分清

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 触发纪律的单一真源文档 —— 指令章节的指针目标、且声明拥有 US2/US3/US4 的行为语义,故阻塞全部故事

**⚠️ CRITICAL**: 本阶段完成前,任何 user story 都不得开工(`discipline-doc.md` §交付顺序约束:先文档 → 镜像 → 测试绿,再写模板章节)

- [X] T004 [P] 编写结构契约测试(RED)`tests/contract/test_proactive_trigger_discipline_doc.py`,断言 `contracts/discipline-doc.md` 的 C-1…C-7:双表面存在 + 字节相同、10 个 `## ` 章节封闭集与顺序、全文零 `BLOCKING_PATTERNS` 命中(从 `scripts/python/scan-confirmation-gates.py` 导入或复刻 `BLOCKING_RE`)、引用不复述(无 confirmation-gates 分类表复制、无种子规则表复制、无信封键集复制)、`## Ownership` 声明归属、项目中性禁用 token、指针可达性不依赖 Documentation Map 行
- [X] T005 撰写 `shared/guidelines/proactive-trigger.md`:恰好 10 个 `## ` 章节且顺序如 `discipline-doc.md` C-2(Ownership / Evaluation Cadence / Evidence Budget & Escalation / Suggestion Shape / Ordering Contract / Promotion & Safety Boundary / Telemetry & Retention / Tuning Protocol / Global Switch / Maintenance Duties);内容按该契约 §各章节必须承载的规范内容 逐节落实;**文案严格照 §文案安全清单 的五处替代表述写**,零 `BLOCKING_PATTERNS` 命中;破坏性判据只以路径引用 `shared/guidelines/confirmation-gates.md`;P1–P5 升级判据表从 `data-model.md` §探测升级判据表 迁入并在此声明为 owner [blockedBy: T004]
- [X] T006 镜像对写 + 验(plan.md Mirror Obligations 第 2 行):运行 `python3 scripts/python/sync-mirrors.py --write`,再 `diff -q shared/guidelines/proactive-trigger.md .specify/shared/guidelines/proactive-trigger.md` 断言字节相同 [blockedBy: T005]
- [X] T007 渲染验证:`python3 -m pytest tests/contract/test_proactive_trigger_discipline_doc.py -q` 转 GREEN;并 `python3 scripts/python/scan-confirmation-gates.py --summary` 确认 total **等于 T002 冻结在 `baseline-gates.json` 的前值**(撰写时实测 23;不硬编码字面量,以免项目侧合法变动时被迫改本文件 —— analyze L-09)、violations **0**(该文档在 `SCAN_DIRS` 的 `shared/` 内且不匹配任何 `GOVERNANCE_PATH_PATTERNS`,故任何命中都会直接破预算) [blockedBy: T006]

**Checkpoint**: 纪律真源就位且文案安全 —— US1 的指针目标存在,US2/US3/US4 的行为语义有了 owner

---

## Phase 3: User Story 1 - 触发点埋设与全 agent 覆盖 (Priority: P1) 🎯 MVP

**Goal**: 主动触发指令段进入 canonical 指令源并经既有 symlink 模型抵达**全部** 6 条受支持 agent 必经路径,同时闭合 `HERMES.md` / `.opencode/instructions.md` 声明却未生成的既有缺口

**Independent Test**: 在干净临时根上 `specify init`,逐条核对 6 个 agent 路径都存在且解析到 `.specify/instructions.md`、都含触发段且语义同源;`/speckit.instructions` 刷新后触发段仍在且自定义章节未被吞;触发段内命令/技能枚举复制计数为 0(quickstart 场景 1)

### Tests for User Story 1 (MANDATORY) ⚠️

- [ ] T008 [P] [US1] 编写结构契约测试(RED)`tests/contract/test_proactive_trigger_section.py`,断言 `contracts/trigger-section.md` 的 C-1…C-12:双表面标题与指针、字节相同镜像、模板 `## ` 序列中的插入位置(紧随 Documentation Map、在 Input Sanity 之前)、正文 ≤25 行且无 `### `、`/speckit.` 与 `skills/` 出现次数为 0、零 `BLOCKING_PATTERNS` 命中、项目中性禁用 token、无受管块标记、additive reconcile 传播且幂等、临时根上 6 条 agent 路径齐备、扫描 total 不增、`_INSTRUCTIONS_FILE_MAP` 与生成侧一致(断言风格承 `tests/contract/test_task_complexity_rubric.py` 的 C-1/C-9/C-10)

### Implementation for User Story 1

- [ ] T009 [US1] author-section:在 `templates/instructions-template.md` 的 **L23**(Documentation Map 常驻指令 L22 之后、`## Fact, Correctness & Logic Checks (Input Sanity)` L24 之前)插入 `## Proactive Flow Trigger` 章节;正文 ≤25 行、**不含任何 `### ` 子标题**、按 `trigger-section.md` §章节必须承载的语义要点 写五行摘要(每回合评估 / 同一趟合规先行 / 证据预算 / 建议形态 / 引擎入口),细节一律指向 `shared/guidelines/proactive-trigger.md`;**零命令名、零技能名、零参数结构、零项目专属 token、零 BLOCKING 字面量** [blockedBy: T005,T008]
- [ ] T010 [US1] mirror-parity 写 + 验(Mirror Obligations 第 1 行的镜像分量):`python3 scripts/python/sync-mirrors.py --write` 后 `diff -q templates/instructions-template.md .specify/templates/instructions-template.md` 断言字节相同(C-2) [blockedBy: T009]
- [ ] T011 [US1] FR-003 硬前置 —— 在 `scripts/bash/generate-instructions.sh` 的 symlink 段(L187–212 区域)按既有 `ln -sf` 形态补两条:根级 `HERMES.md` → `.specify/instructions.md`,以及 `mkdir -p .opencode` + `.opencode/instructions.md` → `../.specify/instructions.md`;随后 `python3 scripts/python/sync-mirrors.py --write` 落 `.specify/scripts/bash/generate-instructions.sh`(**STRICT 对**)并 `diff -q` 验字节相同(Mirror Obligations 第 4 行) [blockedBy: T008]
- [ ] T012 [US1] refresh-verify:在本仓运行 `bash scripts/bash/generate-instructions.sh`,断言 ① `## Proactive Flow Trigger` 已注入 `.specify/instructions.md`;② 既有非模板章节(如 `## Recurring Operational Lessons`)逐字保留;③ **再跑一次幂等**(章节计数不增、块外字节不变);④ 生成了时间戳备份而非覆盖(C-9 / FR-004) [blockedBy: T010,T011]
- [ ] T013 [US1] render-verify 全 agent 路径:按 `quickstart.md` 场景 1 在 `mktemp -d` 临时根上执行 `specify init --here --ai qoder --force --ignore-agent-tools`,断言 `CLAUDE.md`/`AGENTS.md`/`HERMES.md`/`.github/copilot-instructions.md`/`.opencode/instructions.md` 全部存在且 `readlink -f` 均指向 `.specify/instructions.md`,`.qoder/project_rules.md` 与 `.claude/project_rules.md` 亦在;并断言 `_check_instructions` 对 6 个 tool key 全部返回 `pass`(消除 hermes/opencode 恒 fail)(C-10 / C-12) [blockedBy: T011,T012]
- [ ] T014 [US1] 门禁验证:`python3 -m pytest tests/contract/test_proactive_trigger_section.py tests/contract/test_instructions_section_propagation.py -q` 全绿(新契约 + 既有传播守卫);`python3 scripts/python/scan-confirmation-gates.py --summary` 确认 total **等于 T002 冻结前值**、violations **0**;`python3 -m pytest tests/contract/test_confirmation_gates_sweep.py -q` 绿(C-6 / C-11) [blockedBy: T009,T012]

### Manual Verification for User Story 1

- [ ] T015 [US1] 人工走查 `quickstart.md` 场景 1 全流程并把证据(6 条路径的 readlink 输出、`grep -c` 结果、刷新前后自定义章节 diff)记入 `.specify/specs/050-proactive-flow-trigger/verification.md` 的 SC-001 / SC-002 条目 [blockedBy: T013,T014]

**Checkpoint**: 触发段已抵达全部 agent 必经路径,FR-003 覆盖缺口闭合 —— 但此时尚不产出任何建议(US2 才给引擎),故 US1 单独交付的价值是"能力第一次出现在必读上下文里 + 两个 agent 的审计恒 fail 被修掉"

---

## Phase 4: User Story 2 - 情境评估与流程建议:用户不必记得命令名 (Priority: P1) 🎯 MVP

**Goal**: 引擎按粗信号确定性解析情境身份、匹配规则、给出含**确切可复制调用形式**的非阻塞建议;出厂种子规则集使新项目第一天即有价值;每回合遥测使 SC-011/SC-012 可测

**Independent Test**: 零学习记录的全新项目上 `init` 后 `assess` 即返回正确的生命周期建议(冷启动);连续 20 个无关回合评估静默且探测升级率为 0;`--probe` 时才升级且只回摘要(quickstart 场景 2 + 3)

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T016 [P] [US2] 编写结构契约测试(RED)`tests/contract/test_trigger_seed_derivation.py`,断言 `contracts/seed-derivation.md` 的 C-1…C-10:双表面 + 字节相同、顶层 schema 封闭、规则条目键集(含可选 `notes`)、与学习规则同构、每条携带 `provenance{file,anchor,quote}`、provenance 指向的文件与 `## Handoffs` 段真实存在且 `quote` 为逐字子串、**漂移检出**(顶层 `flow` 值仍出现在来源 Handoffs 段内,失败信息含 ruleId + file + flow)、14 个命名情境全覆盖、`confirmationClass` 与 data-model 分类列逐项一致且不复述判据文档、init 整体拷贝可达
- [ ] T017 [P] [US2] 编写结构契约测试(RED)`tests/contract/test_trigger_engine.py`,断言 `contracts/trigger-engine.md` 的 **C-1…C-23 全部条款**(含 US3/US4 才实现的 C-16…C-18 与 analyze 补强的 C-19…C-23 行为 —— 引擎契约是一份制品,其测试文件一次写全;故事专属的**行为**验证另落各自的集成测试文件以避免同文件串行):stdlib-only、镜像字节相同、9 键 camelCase 信封、`--format`、5 级退出码常量、原子写、workspace-root 优先级、状态不可读降级、**11 项 action 封闭枚举**、**20 个长选项封闭集**(含 analyze 补的 `--compliance-done`)、标识符格式、assess 确定性解析、未传 `--probe` 时零制品文件打开(monkeypatch 计数)、恒写一行遥测、输出摘要有界;**并按该契约末节要求解析 `quickstart.md` 的代码块,逐条校验 action ∈ C-9、长选项 ∈ C-10、标识符满足 C-11**
- [ ] T018 [P] [US2] 编写单元测试(RED)`tests/unit/test_trigger_utils_units.py`,覆盖引擎纯函数(Principle IV「Pure functions/utilities MUST have unit tests」):情境身份解析((stage, signals) → 唯一 situationId / 解析不到)、词表越界 → `EXIT_INVALID`、阈值优先级链四级(显式 > 环境变量 > 存储 > 默认,含非法环境变量值忽略降级)、阈值下限 <2 → `EXIT_USAGE`、遥测行 7 键整形、`snapshot` >200 字符守卫、连续计数递增与重置的纯计算、破坏性豁免判定

### Implementation for User Story 2

- [ ] T019 [US2] 撰写 `templates/proactive-trigger-seed.json`:`schemaVersion` / `generatedFrom`(记派生批次与 commit)/ `situations`(**13** 条,携带 E1 完整形状 `id`/`name`/`stage`/`signals`/`match{stage,signalsAll,signalsAny}`,与 `data-model.md` §受控词表逐项一致)/ `rules`(**13** 条 `r-001`…`r-013` 与 `s01`…`s13` 配对);每条 `provenance` 四键齐备(`file`/`anchorKind`/`anchor`/`quote`),`quote` 从其 `anchorKind` 对应的来源段落**逐字复制**(空白归一,不改写不概括,以 T003 预检结果为准);`owning-section` 类共 2 条(s09 → `shared/workflow/feedback-step.md` §Threshold prompt protocol、s10 → `templates/commands/feedback.md` Mode 表);`confirmationClass` 按 data-model 分类列(`r-006` `/speckit.implement`、`r-011` `/speckit.docs`、`r-013` `/speckit.constitution` 为 `destructive`,其余 `reversible`),`destructive` 条目在 `notes` 说明判据出处(**引用**路径,不复述分类表) [blockedBy: T003,T016]
- [ ] T020 [US2] mirror-parity 写 + 验(Mirror Obligations 第 5 行):`python3 scripts/python/sync-mirrors.py --write` 后 `diff -q templates/proactive-trigger-seed.json .specify/templates/proactive-trigger-seed.json`(C-1) [blockedBy: T019]
- [ ] T021 [US2] 实现 `scripts/python/trigger-utils.py` 骨架:stdlib-only;`envelope()` 返回 9 键 camelCase(`ok`/`action`/`workspaceRoot`/`generatedAt`/`errors[]`/`warnings[]`/`semanticJudgmentPending[]`/`notes[]`/`payload{}`);退出码常量 `EXIT_OK=0`/`EXIT_USAGE=1`/`EXIT_INPUT_ERROR=2`/`EXIT_NOT_FOUND=3`/`EXIT_INVALID=4`;原子写 `.part` + `os.replace`;workspace-root 四级解析;`--action` 11 项封闭枚举;**20** 个长选项封闭集(含 `--compliance-done`);`--format text|json`(默认 json);状态不可读 → 降级 suggest-only + `warnings:["state-unreadable"]` + exit 0(骨架范式照 `scripts/python/derive-utils.py`,**不**照 `feedback-utils.py` 的非原子 `save_index`) [blockedBy: T017,T018]
- [ ] T022 [US2] 在 `scripts/python/trigger-utils.py` 实现 `init` action:从种子建 `.specify/memory/trigger/index.json`(E6 schema,`schemaVersion`/`config{enabled,threshold:3,telemetryWindow:200,probeBudgetPct:20,minSample:5}`/`situations`/`rules`/`events`/`proposals`);**幂等**;已存在 `ruleId` 只刷新 `rationale`/`invocation`,凡 `tuning` 非空者其 `state`/`priority`/`confirmationClass` 以本地为准(V2.3 / seed C-10:用户调优不被种子回退);确保 `telemetry.jsonl` 的 gitignore 条目由引擎自维护(下游项目同样生效) [blockedBy: T019,T021]
- [ ] T023 [US2] 在 `scripts/python/trigger-utils.py` 实现 `assess` action:按 `--stage` + `--signal`(可重复)依 E1.`match` 谓词确定性解析唯一 `situationId`,解析不到 → `payload.suggestion=null` + `payload.reason="no-situation-match"`;命中则按 `priority` 收敛为一条,`payload.suggestion` 含且仅含 `ruleId`/`flow`/`invocation`/`rationale`/`autoExecute`;`payload` 序列化 ≤60 行 / ≤2000 字符;**每次调用向 `telemetry.jsonl` 追加恰好一行**(E4 七键);`suggested=true ∧ complianceDone=false` → 该行照写且 `errors:["ordering-violation"]`;`suggested=false` → `visibleOutput` 恒 false(C-12/C-14/C-15) [blockedBy: T022]
- [ ] T024 [US2] 在 `scripts/python/trigger-utils.py` 实现 `--probe` 升级路径:P1–P5 五个确定性探测(制品存在性 / `NEEDS CLARIFICATION` 与 `Need clarification` **计数** / `[ ]`·`[X]`·`[~]` **计数** / 调 `feedback-utils.py --action status` 取阈值字段 / 指令文件与模板的 `## ` 标题**集合差**),全部只回摘要(单条 ≤200 字符)、MUST NOT 回传制品正文;遥测记 `escalated=true`;未传 `--probe` 时引擎 MUST NOT 打开任何制品文件(C-13 以文件打开计数断言) [blockedBy: T023]
- [ ] T025 [US2] 在 `scripts/python/trigger-utils.py` 实现 `status` 与 `rules` action:`status` ≤30 行,含 `config`、按 `state` 分组的规则计数、`promoted` 清单、待批提议数、遥测行数 vs 窗口、**实测探测升级率 vs `probeBudgetPct` 对比**(SC-011 的读数入口);`rules` 每行 `ruleId/situationId/flow/class/origin/state/consecutive/hits/declined`,`--format json` 给全字段 [blockedBy: T022]
- [ ] T026 [US2] mirror-parity 写 + 验(Mirror Obligations 第 3 行,**STRICT 对**):`python3 scripts/python/sync-mirrors.py --write` 后 `diff -q scripts/python/trigger-utils.py .specify/scripts/python/trigger-utils.py`,并 `python3 scripts/python/sync-mirrors.py --check` 断言 exit 0(mirror-only 会报 ORPHAN 并 exit 2)。**blocker 说明**:T023/T024/T025 都改同一个引擎文件,故三者全部列入 —— 否则合法拓扑序 T022→T025→T026→T023→T024 会在 T024 落地前镜像,留下陈旧 STRICT 镜像(analyze M-02) [blockedBy: T023,T024,T025]
- [ ] T027 [US2] 验证:`python3 -m pytest tests/contract/test_trigger_seed_derivation.py tests/contract/test_trigger_engine.py tests/unit/test_trigger_utils_units.py -q` 全绿 [blockedBy: T020,T024,T026]

### Manual Verification for User Story 2

- [ ] T028 [US2] 人工走查 `quickstart.md` 场景 2(冷启动首日建议)与场景 3(20 个无关回合静默 + `--probe` 升级),**本任务是 SC-003 / SC-004① / SC-011 / SC-012 / SC-013 / SC-014 的具名产出者**,须交付:① **≥6 种生命周期状态矩阵**的逐状态建议记录与正确性人工判定(SC-003 要求 ≥6 种,`quickstart` 场景 2 只覆盖 1 种,须自行补齐:仅 requirements、requirements 含未决澄清、已澄清未规划、plan 就绪无 tasks、tasks 就绪未实现、feedback 达阈值);② **≥5 个独立会话**对同一构造状态的 `payload.situationId` 一致率(SC-014);③ 场景 3 的 20 回合 `status` 读数 `turns`/`escalationPct`/`visibleOutputCount`(SC-011、SC-004①);④ 词表越界退出码 4 的实测;⑤ 冷启动首日建议(SC-013)。全部记入 `verification.md` 对应 SC 条目 [blockedBy: T027]

**Checkpoint**: **MVP 达成**(US1 + US2)—— 用户不必记得任何命令名即可在第一天得到正确建议;两个 P1 故事合起来构成可独立演示的增量

---

## Phase 5: User Story 3 - 选择记录与阈值晋升:重复确认后自动执行 (Priority: P2)

**Goal**: 记录采纳/拒绝,连续采纳达阈值(默认 3)晋升为免确认自动执行;一次拒绝即重置;**破坏性流程永不晋升**;遥测有界可轮转且轮转不清空学习结果

**Independent Test**: 连续采纳 3 次后第 4 次 `autoExecute=true`;插入一次拒绝则计数归零、晋升不发生;破坏性规则采纳 10 次仍恒不晋升;窗口 50 下制造 60 行遥测后轮转,规则与晋升态 diff 为空(quickstart 场景 4 + 5)

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T029 [P] [US3] 编写集成测试(RED)`tests/integration/test_trigger_promotion.py`:连续 3 次 accepted → `state=promoted` 且 `assess` 返回 `autoExecute=true`;一次 declined → `consecutive=0`、`state` 回落 `active`、`promotion.resetBy` 指向该 eventId;ignored 与 declined 同效但在 `stats` 分列;**破坏性规则连续 10 次 accepted → `promoted` 恒 false、`state` 恒 ≠ promoted、`autoExecute` 恒 false(SC-005 零容忍)**;`reset --rule` 与 `reset --all` 记 `userResetAt`;`config --enabled false` → 建议产出数与自动执行数均为 0 且状态在指令再生后仍生效(SC-009);`--threshold 1` → `EXIT_USAGE` + `errors:["threshold-below-floor"]`
- [ ] T030 [P] [US3] 编写集成测试(RED)`tests/integration/test_trigger_telemetry.py`:`config --window 50` 后制造 60 回合 → `rotate` → `telemetry.jsonl` 行数 ≤50 且 `rules --format json` 轮转前后**逐字节相等**(SC-015 零丢失,判别"计数从原始行重算"的缺陷);`escalationPct` 计算正确;`suggested=false` 的回合 `visibleOutput` 恒 false(SC-011 静默性)

### Implementation for User Story 3

- [ ] T031 [US3] 在 `scripts/python/trigger-utils.py` 实现 `record` action:写 E3 建议事件(`eventId` = `<UTC-compact>-<seq>`、`snapshot` ≤200 字符否则 `EXIT_INVALID`);更新 E2.`stats{hits,accepted,declined,ignored,lastSeen}` 与 E5 晋升态;accepted → `consecutive += 1`,达 `threshold` 且 `confirmationClass == "reversible"` → `state="promoted"`;declined/ignored → `consecutive=0`、`promoted=false`、记 `resetBy`;**破坏性豁免为硬守卫**(C-16/C-17,`confirmationClass` 只读不计算) [blockedBy: T023,T029]
- [ ] T032 [US3] 在 `scripts/python/trigger-utils.py` 实现 `reset` 与 `config` action:`reset --rule <r-nnn>` / `--all` 置 `consecutive=0`、`promoted=false`、记 `userResetAt`(FR-012);`config --enabled|--threshold|--window|--probe-budget|--min-sample` 写 E6.`config`,阈值解析优先级链 **显式 `--threshold` > `SPECKIT_TRIGGER_THRESHOLD` > 存储值 > 默认 3**,非法环境变量值忽略降级,解析结果 <2 → `EXIT_USAGE`(C-18,与 `feedback-utils.py:resolve_threshold` 同构) [blockedBy: T031]
- [ ] T033 [US3] 在 `scripts/python/trigger-utils.py` 实现 `rotate` action 与窗口强制:截断 `telemetry.jsonl` 保留最近 `config.telemetryWindow` 行;**MUST NOT 触及 `index.json`**(晋升计数是 E2 内嵌聚合态,不由原始行重算)(FR-009a / V4.3 / V4.4) [blockedBy: T031,T030]
- [ ] T034 [US3] mirror-parity 写 + 验(Mirror Obligations 第 3 行,STRICT):`python3 scripts/python/sync-mirrors.py --write` + `diff -q` + `--check` exit 0 [blockedBy: T032,T033]
- [ ] T035 [US3] 验证:`python3 -m pytest tests/integration/test_trigger_promotion.py tests/integration/test_trigger_telemetry.py tests/contract/test_trigger_engine.py -q` 全绿(C-16…C-18 由 T017 已写就,此处随实现转绿) [blockedBy: T034]

### Manual Verification for User Story 3

- [ ] T036 [US3] 人工走查 `quickstart.md` 场景 4(晋升 / 拒绝重置 / 破坏性 10 次零晋升 / 复位 / 全局关闭)与场景 5(轮转零丢失),**本任务是 SC-005 / SC-006 / SC-009 / SC-010 / SC-015 的具名产出者**,须交付:① 破坏性规则连续 **10** 次采纳后 `promoted` 恒 false 的实测(SC-005,强于其 ≥5 次下限);② 一次拒绝后计数归零(SC-006①);③ **实际运行 `bash scripts/bash/generate-instructions.sh` 后** diff `.specify/memory/trigger/index.json`,证明再生零丢失(SC-006②,此前无任何任务产出该半边);④ `config --enabled false` 后建议与自动执行均为 0、且再生后仍生效(SC-009);⑤ **三态降级走查**——状态文件缺失 / JSON 损坏 / `schemaVersion` 不兼容,各观察退出码 0 + `warnings:[state-unreadable]` + `payload.degraded=suggest-only` + 会话不中断(SC-010,此前无任何任务产出);⑥ 场景 5 的截断不变量与轮转零丢失 diff(SC-015)。全部记入 `verification.md` [blockedBy: T035]

**Checkpoint**: US1 + US2 + US3 —— 机制从"提醒"升级为"代办",且安全边界(破坏性永不晋升)已由零容忍测试钉死

---

## Phase 6: User Story 4 - 触发规则的证据驱动优化 (Priority: P2)

**Goal**: 依命中率/拒绝率/误报/漏报产出**附证据**的调优提议,小样本不提议,经用户批准才写回;漏报检测作为"唯一通道无确定性触发"的补偿控制

**Independent Test**: 注入高拒绝率规则与漏报情境的记录历史 → `tune` 识别二者并附指标与样本数;`hits < minSample` 的规则不出现在提议中且被 `notes[]` 具名;批准前规则集零变更;`tune-apply` 后 `tuning.{ratifiedAt,evidenceRef}` 可回查(quickstart 场景 6)

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T037 [P] [US4] 编写集成测试(RED)`tests/integration/test_trigger_tuning.py`:`tune` 的每条提议含证据字段(指标 + 样本数);`stats.hits < minSample` 的规则**不出现**在提议中且被 `notes[]` 具名回显(FR-017 小样本守卫);`tune` 后未 `tune-apply` → 规则集**零变更**(FR-016);`tune-apply --proposal p-001 --reason ...` 后 SM-2 走 `ratified → applied` 且写 `tuning.{ratifiedAt,evidenceRef}`;`record-manual --flow X` 在当回合遥测 `suggested=false` 时产出漏报证据并被下一次 `tune` 消费;需 agent 判断的项出现在 `semanticJudgmentPending[]`

### Implementation for User Story 4

- [ ] T038 [US4] 在 `scripts/python/trigger-utils.py` 实现 `record-manual` action:`--flow` 必填;与当回合遥测的 `suggested` 标志关联,`suggested=false` 时记为**漏报证据**(FR-015;首轮 Q1=A 唯一通道的补偿控制) [blockedBy: T031,T037]
- [ ] T039 [US4] 在 `scripts/python/trigger-utils.py` 实现 `tune` action:确定性聚合命中率 / 拒绝率 / 误报 / 漏报差集(手动调用集 − 已建议集);**小样本守卫** `stats.hits < config.minSample`(默认 5)的规则 MUST NOT 产出提议,被跳过者在 `notes[]` 具名;每条提议含 `proposalId`(`p-nnn`)/ 类型(收紧·抑制·新增)/ 证据(指标 + 样本数);语义判断(该不该采纳、新规则配哪条流程)经 `semanticJudgmentPending[]` 交回 agent(承 `derive-utils.py` 的"确定性交引擎、语义留 agent"分工) [blockedBy: T038]
- [ ] T040 [US4] 在 `scripts/python/trigger-utils.py` 实现 `tune-apply` action:`--proposal <p-nnn>` + `--reason` 必填;SM-2 `ratified → applied`;写 E2.`tuning.{suppressedBy,ratifiedAt,evidenceRef}`;未经该 action 规则集 MUST NOT 变更(FR-016) [blockedBy: T039]
- [ ] T041 [US4] mirror-parity 写 + 验(Mirror Obligations 第 3 行,STRICT):`python3 scripts/python/sync-mirrors.py --write` + `diff -q` + `--check` exit 0 [blockedBy: T040]
- [ ] T042 [US4] 验证:`python3 -m pytest tests/integration/test_trigger_tuning.py tests/contract/test_trigger_engine.py -q` 全绿 [blockedBy: T041]

### Manual Verification for User Story 4

- [ ] T043 [US4] 人工走查 `quickstart.md` 场景 6:6a 漂移检出受控实验(临时改写某 `## Handoffs` 的流程名 → `test_trigger_seed_derivation.py` C-7 失败并指名 ruleId/file/flow → **恢复**,修复方式是同步种子而非放宽测试)+ 6b–6e 漏报证据与调优批准链;证据记入 `verification.md` 的 SC-007 / SC-013 条目 [blockedBy: T042]

**Checkpoint**: 四个故事全部独立可测 —— 机制具备自我收敛能力(证据 → 提议 → 批准 → 写回)

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: 接线义务、零扰动承诺的机械复核、跨故事度量与 Feature 列表复审

- [ ] T044 [P] 新建 Tool 记录 `.specify/memory/tools/trigger-utils.py.md`(Principle XII 义务;形态照既有 9 条记录:Tool Name / Type `project-script` / Source Identifier `scripts/python/trigger-utils.py` / Tool ID / Aliases / Status / Scope / Description / Invocation & I/O Contract / Parameters 表含 11 个 action);随后运行 `bash scripts/bash/refresh-tools.sh --json` **再生** `.specify/memory/tools.md` 与 `.specify/tools/{system,shell,project}.json`(派生清单禁手改),并断言清单中出现新 Tool [blockedBy: T042]
- [ ] T045 [P] 漂移守卫**活性**证明(防守卫空洞):在临时副本上把某个 `templates/commands/<x>.md` 的 `## Handoffs` 流程名改写,运行 `python3 -m pytest tests/contract/test_trigger_seed_derivation.py -q` 断言**失败**且错误信息同时含 `ruleId`、`provenance.file` 与缺失的 `flow` 值,随后**恢复原文件**并复跑断言绿。记录该受控实验证据(证明 C-7 不是恒真断言)[blockedBy: T016,T019]
- [ ] T046 全套件名字级回归(GATE-1):`bash scripts/bash/run-tests.sh --names-out /tmp/cur-failed.txt` 后 `comm -13 .specify/specs/050-proactive-flow-trigger/baseline-failed.txt /tmp/cur-failed.txt` **输出为空**;同时记录新增通过数 [blockedBy: T027,T035,T042]
- [ ] T047 全树门禁扫(GATE-2/3/4/7):`python3 scripts/python/sync-mirrors.py --check` exit 0;`python3 scripts/python/regen-command-copies.py --check` exit 0(**必须未变** —— 本特性不改任何命令模板);`python3 scripts/python/scan-confirmation-gates.py --summary` total **等于 T002 冻结前值**(撰写时实测 23)/ violations **0**;`python3 -m pytest tests/contract/test_confirmation_gates_sweep.py -q` 绿;`python3 scripts/python/feedback-utils.py --action probes --validate` exit 0 且 internal objects 仍 **73** [blockedBy: T046]
- [ ] T048 零扰动计数复核(GATE-8):`python3 -m pytest tests/contract/test_feedback_command_classification.py tests/contract/test_docs_step_injection.py -q` 绿,且两文件内的 `COMPLEX_COMMANDS`(19)/`SIMPLE_COMMANDS`(4)/docs-step(16)**未被本特性改写**(P-Q1=A 的承诺:不新增命令即不动计数)[blockedBy: T046]
- [ ] T049 [P] 撰写 `.specify/specs/050-proactive-flow-trigger/verification.md`:为 **SC-001…SC-015** 逐条写 `SC-NNN_status=pass|deferred` 行,附 requirements.md § Measurement Sources 指定的证据来源与本次实测读数;`deferred` 项须附因。**本任务汇总他人产出的读数,故必须后于全部产出任务**(analyze M-14:否则 GATE-6 / DoD-7 可能在证据尚未产生时就变绿)[blockedBy: T015,T028,T036,T043,T047,T050]
- [ ] T050 Dogfood 实测(SC-011 / SC-012 的真实读数):在本仓以机制上线后的状态跑 **≥20 个真实回合**,用 `trigger-utils.py --action status` 读出实测 `escalationPct` 并与 `probeBudgetPct=20` 对比、读出无适用流程回合的 `visibleOutputCount`(期望 0)、核对 `complianceDone` 与 `suggested` 的时序(期望零 `ordering-violation`);**本任务另是 SC-008② 与 SC-004② 的具名产出者**:⑦ 记录 dogfood 期间「因建议导致用户当前请求被阻塞或延后」的**事件计数**(期望 0,SC-008②——此前无任何任务产出该读数);⑧ 记录同会话内同一情境重复评估时的**重复建议计数**(期望 0,验证 `trigger-engine.md` C-20 的会话级抑制,SC-004②);⑨ 诚实记录 SC-011 的分母口径局限(`data-model.md` V4.5:遥测无法证明 agent 跳过了某回合的评估,故须附会话侧观察)。全部记入 `verification.md` [blockedBy: T028,T036,T043]
- [ ] T051 实现收尾的 Feature 记录义务(**不推进状态** —— `Planned → Implemented` 由 `/speckit.implement` 持有,受 Principle VII Pre-Status-Flip Gate 约束:零 `[ ]` 任务 + 每条 SC 在 verification 有状态行)。在 `.specify/memory/features/050.md` § Latest Review 追加 implement 阶段实测要点,并在 `.specify/memory/features.md` 050 行 Last Updated 追加 implement 注记(**手工编辑**,禁跑 `update-feature-index.sh`);若 T011 的路径覆盖修复已落地,确认 `features/022.md` 的对应注记仍在(该注记由 tasks 阶段写入)[blockedBy: T049,T050]

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖,可立即开始
- **Foundational (Phase 2)**: 依赖 Setup;**阻塞全部 user story**(纪律文档是指令章节的指针目标,且声明拥有 US2/US3/US4 的行为语义)
- **US1 (Phase 3)**: 依赖 Foundational
- **US2 (Phase 4)**: 依赖 Foundational;**不依赖 US1**(引擎与种子可独立于指令章节实现和测试)—— 但 MVP 需二者同时交付
- **US3 (Phase 5)**: 依赖 US2 的 `assess`/引擎骨架(T023)—— 晋升语义作用于 assess 产出的建议
- **US4 (Phase 6)**: 依赖 US3 的 `record`(T031)—— 调优证据来自建议事件与漏报关联
- **Polish (Phase 7)**: T044 依赖 T042(引擎全部 action 落地后才能写 Tool 记录)、T045 依赖 T016+T019(种子与其测试存在后才能做漂移活性实验)、T049 依赖 T015/T028/T036/T043/T047/T050(它汇总他人产出的读数);T046/T047/T048 依赖各故事的验证任务。**故本阶段不再是"可与故事并行",而是收尾汇聚点**

### User Story Dependencies

- **US1 (P1)**: Foundational 之后即可开工;与其他故事无依赖
- **US2 (P1)**: Foundational 之后即可开工;与 US1 **可并行**(不同文件:US1 改 `templates/instructions-template.md` + `scripts/bash/generate-instructions.sh`,US2 建 `templates/proactive-trigger-seed.json` + `scripts/python/trigger-utils.py` + 测试)
- **US3 (P2)**: 需 US2 的 T023(`assess`);测试任务 T029/T030 可与 US2 实现并行(不同文件)
- **US4 (P2)**: 需 US3 的 T031(`record`);测试任务 T037 可与 US3 实现并行

### 单文件串行链(关键路径)

`scripts/python/trigger-utils.py` 被三个故事共改,故实现任务严格串行:

```
T021 (骨架) → T022 (init) → T023 (assess) → T024 (--probe)
                                  ↓
                            T031 (record) → T032 (reset/config)
                                  ↓              T033 (rotate)
                            T038 (record-manual) → T039 (tune) → T040 (tune-apply)
```

每个故事结束后各有一次 mirror-parity 任务(T026 / T034 / T041),因 STRICT 镜像对要求源与镜像同步落地。

### Within Each User Story

- 测试先写并**必须失败**(RED)再实现(Principle IV Red-Green-Refactor)
- 契约测试 → 单元测试 → 实现 → 镜像 → 验证 → 人工走查
- **例外(迁移/回归型)**:本特性无移植既有行为的测试,故全部测试任务严格 red-first,无需 `[blockedBy: T<impl>]` 反向排序

### Parallel Opportunities

- Phase 1:T002、T003 可与 T001 并行
- Phase 2:T004 独立;T005→T006→T007 串行(同一文件链)
- Phase 3:T008 可与 Phase 2 的实现并行(不同文件);T009/T011 在 T008 之后可并行(不同文件:模板 vs 生成脚本)
- Phase 4:**T016、T017、T018 三个测试文件互不相同,可完全并行**;且可与 Phase 3 的实现并行
- Phase 5:T029、T030 可并行(两个不同集成测试文件),且可与 US2 实现并行
- Phase 6:T037 可与 US3 实现并行
- Phase 7:T044、T045 在各自 blocker 满足后可并行(不同文件);T049 必须最后(它汇总 T015/T028/T036/T043/T047/T050 的读数)
- **跨故事并行的上限**受单文件引擎串行链约束:T021→T023→T031→T038 是关键路径,无法并行化

---

## Parallel Example: User Story 2

```bash
# 三个测试文件互不相同,可同时开工(RED):
Task: "编写 tests/contract/test_trigger_seed_derivation.py(C-1…C-10)"     # T016
Task: "编写 tests/contract/test_trigger_engine.py(C-1…C-18 + quickstart 解析)" # T017
Task: "编写 tests/unit/test_trigger_utils_units.py(引擎纯函数)"            # T018

# 同时,US1 的实现可在另一条线上推进(不同文件):
Task: "在 templates/instructions-template.md L23 插入触发章节"              # T009
Task: "在 scripts/bash/generate-instructions.sh 补 HERMES.md 与 .opencode 两条 symlink" # T011
```

## Parallel Example: User Story 3

```bash
# 两个集成测试文件互不相同,可同时开工(RED),且可与 US2 的实现并行:
Task: "编写 tests/integration/test_trigger_promotion.py"    # T029
Task: "编写 tests/integration/test_trigger_telemetry.py"    # T030
```

---

## Implementation Strategy

### MVP First

**MVP 范围 = US1 + US2(两个 P1 故事)**。依 tasks 模板的 MVP 范围规则:本特性有两个 P1 故事,且**只有二者合起来才构成独立有价值的增量** —— US1 单独交付只是"指令文件里多了一段不产出任何建议的文字",US2 单独交付则"引擎能算但没有常驻位置去触发它"(用户仍须自己记得去调用,正是本特性要消除的负担)。故 MVP 覆盖全部 P1。

1. 完成 Phase 1: Setup(冻结基线 + 探测前值 + 种子来源预检)
2. 完成 Phase 2: Foundational(**关键** —— 纪律文档阻塞全部故事)
3. 完成 MVP 故事集:Phase 3(US1)+ Phase 4(US2),二者**可并行**(不同文件)
4. **STOP and VALIDATE**:按各自 Checkpoint 独立测试 —— US1 走 quickstart 场景 1(6 条 agent 路径 + 刷新幂等),US2 走场景 2 + 3(冷启动首日建议 + 20 回合静默与升级率)
5. 此时即可交付/演示:用户不必记得任何命令名就能在第一天得到正确建议

### Incremental Delivery

1. Setup + Foundational → 纪律真源就位
2. \+ US1 → 触发段抵达全部 agent 必经路径,FR-003 覆盖缺口闭合(独立价值:两个 agent 的审计恒 fail 被修掉)
3. \+ US2 → **MVP**:冷启动即有建议,心智负担直接下降
4. \+ US3 → 阈值晋升,机制从"提醒"升级为"代办"(独立价值:重复流程零确认;安全边界由零容忍测试钉死)
5. \+ US4 → 证据驱动调优,机制自我收敛(独立价值:噪声规则可抑制、漏报可补齐)
6. \+ Polish → 接线义务闭合、零扰动承诺机械复核、SC 逐条留证

### Parallel Team Strategy

1. 全队共同完成 Setup + Foundational
2. Foundational 完成后:
   - 开发者 A:US1(指令章节 + 生成脚本 + 路径覆盖)
   - 开发者 B:US2 的**测试三件**(T016/T017/T018,三个不同文件可再细分)
3. US2 测试就位后,引擎实现(T021→T024)因**单文件串行**只能由一人推进 —— 这是本特性并行度的硬上限
4. 引擎 `assess` 落地后:开发者 A 接 US3 测试(T029/T030),开发者 B 接 US3 实现链(T031→T033)
5. US4 同法:测试(T037)与实现(T038→T040)分人
6. Polish 阶段:T044(Tool 记录)与 T045(漂移活性实验)可分人并行;**T049(verification.md)必须最后**,因它汇总各故事走查与 T047/T050 的读数

---

## Notes

- `[P]` = 不同文件、无未完成依赖。**单文件引擎链上的任务一律不标 `[P]`**(T021→T024、T031→T033、T038→T040 及其间的 mirror 任务)
- 每个 story 可独立完成与测试;Checkpoint 处停下即可独立验证
- 实现前确认测试**先失败**;契约测试的 RED 状态本身就是"契约尚未被满足"的证据
- **门控预算余量为 0**:T005(纪律文档)与 T009(指令章节)是全计划**最易失败**的两处 —— 文案天然是"建议/确认/询问"语义,任一 `BLOCKING_PATTERNS` 字面量都会把扫描 total 推过 23.25 上限并打爆 `test_confirmation_gates_sweep.py`。两处都必须照 `contracts/discipline-doc.md` §文案安全清单 的五处替代表述写,落地后立即跑 T007 / T014 的扫描复核
- **Pin hygiene**(测试编写规则,承 `/speckit.tasks` 约定):① 版本断言用下限语义(`parsed >= (3, 8)`),禁 `startswith("3.8")`;② 测试 fixture 里列出的每个文件路径都在编写时存在性核验过(本文件 GATE 与 T002 的命令清单已逐一 existence-check:13/13 存在);③ 计数只在**计数本身即契约**时硬编码 —— 本特性中 门控 total(以 T002 冻结值为准,撰写时实测 23)、19/16(命令分类)、73(probe internal)、**13**(命名情境)、**12**(信号枚举)、11(action 枚举)、**20**(flag 封闭集)、**61**(契约条款)都属此类,改动其population 的任务必须同批更新对应断言;其余一律用 `len(...)` 从 glob 派生
- **两顶帽子**(Principle XI):T009/T011/T019/T021 改的是**框架源码面**(`templates/`、`scripts/`、`shared/`),靠 `sync-mirrors.py` 与 init 拷贝抵达运行面;T012 的 refresh-verify 改的是**本仓客户端运行面**(`.specify/instructions.md`)。任何"直接手改 `.specify/` 运行副本"的诱惑都是 instance fix,不会抵达下游项目
- **延后纪律**:优先 `[~]` + `<!-- deferred: reason -->` 而非留 `[ ]`。可预见的 `[~]` 候选:SC-003 的建议准确率(需 ≥6 种真实状态样本 + 人工判定,单次运行内可能只能覆盖部分)、SC-008 的"阻塞/延后事件计数"(需长期采用观察)、T050 的 ≥20 真实回合 dogfood(若会话长度不足)。三者都在 `verification.md` 记 `deferred` 并附因,不阻塞 GATE-5
- 每完成一个任务或一个逻辑组即提交;任何 Checkpoint 处都可停下独立验证故事
