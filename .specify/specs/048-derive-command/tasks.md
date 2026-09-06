# Tasks: 推导式架构生成 —— /speckit.derive(Derivation Command)

**Requirement ID**: 048  
**Requirement Key**: 048-derive-command  
**Related Feature**: 049 Derivation Command(推导式架构生成)  
**Input**: Design documents from `.specify/specs/048-derive-command/`  
**Prerequisites**: plan.md(required), requirements.md(required), data-model.md, contracts/(4), quickstart.md, feature-ref.md, checklists/requirements.md

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation"。本需求为混合形态:引擎(runtime code)走 unit / integration / contract 三层;命令模板与概念锚(template-only artifacts)按宪法 §IV "Template-only features" 条款走结构契约测试(content / heading / mirror-parity / 扫描器零命中断言)。

**执行序偏差(如实记录)**: 契约先于实现(4 份 contracts 在引擎之前落地),但 RED 测试与引擎实现的先后被倒置——引擎先落地并以其 44 项端到端驱动验证,pytest 层随后由 `/tmp/derive-staging/e2e_engine.py` 转写。契约驱动这一实质要求满足;严格 RED→GREEN 序未满足,记为本特性的过程偏差。

**Environment Prerequisites**: python3(≥3.8)与 `.venv/bin/python`(含 pytest);本仓 git。**无线上能力依赖用于测试**——`probe-links` 的真实网络路径由 dogfood 运行(T038)验证,任何测试 MUST NOT 触网。

## Definition of Done (DoD)

- DoD-1: 引擎 `scripts/python/derive-utils.py` 按 `contracts/derive-engine.md` 实现:恰 6 个 action(init / validate / moves-list / moves-add / probe-links / stats)、退出码 0/1/2/3/4、`moves.md` 独写、槽位同构去重拒绝、`M-` 项目级单调发放、`probe-links` 离线容错
- DoD-2: 概念锚 `shared/definitions/derivation-definitions.md` 为模型唯一真源,命令模板/引擎 docstring/词汇表/用户文档均引用而不复述;锚与引擎的禁用论证字面量集由漂移测试钉为相等
- DoD-3: 全部自动化测试通过,全套件相对 `baseline-failed.txt`(50 条,名字级)零新增失败
- DoD-4: plan.md Mirror Obligations 七行全部核验:概念锚/probe-definitions/framework-map 三处 `diff -q` 一致、引擎**严格**镜像对一致、4 份工具副本经 regen 传播且 `--check` 零 stale、`sync-mirrors --check` exit 0、`.specify/derive/` 未进 MIRROR_PAIRS
- DoD-5: 登记面同步:probe Object `speckit-derive-wrapup`(internal 72→73)、复杂命令分类 18→19、docs-step 分类 15→16、framework-map 新行、glossary 四个新词条、Tool 记录、`docs/reference/commands/derive.md`
- DoD-6: 门控零回流——`scan-confirmation-gates.py` total 不超过基线 23,violations 为空,新增文件零 BLOCKING 命中
- DoD-7: 本仓 dogfood 运行已执行并如实报告(含真实死链与 403 阻塞来源的落地证据)
- DoD-8: requirements.md 的 SC-001..SC-006 逐条在 verification.md 有状态与证据记录

**DoD Status**: met

## Completion Gate

- GATE-1: 全套件零新增失败 — check: `bash scripts/bash/run-tests.sh --names-out /tmp/048-final.txt` 后 `comm -13 .specify/specs/048-derive-command/baseline-failed.txt /tmp/048-final.txt` 为空
- GATE-2: 镜像义务逐行核验 — check: `diff -q scripts/python/derive-utils.py .specify/scripts/python/derive-utils.py`;`diff -q shared/definitions/derivation-definitions.md .specify/shared/definitions/derivation-definitions.md`;`python3 scripts/python/sync-mirrors.py --check` exit 0
- GATE-3: 无未决任务行 — check: `grep -cE '^- \[[ >]\]' .specify/specs/048-derive-command/tasks.md` 返回 0
- GATE-4: verification.md 覆盖全部 SC — check: 对 requirements.md 的 SC-001..SC-006 逐一 grep verification.md
- GATE-5: 门控治理无回流 — check: `python3 scripts/python/scan-confirmation-gates.py --root . --json` 的 `total` ≤ 23 且 `violations` 为空
- GATE-6: 命令副本零 stale — check: `python3 scripts/python/regen-command-copies.py --check` 输出 OK,4 份 `speckit.derive` 副本存在且携带 AUTO-GENERATED 标记
- GATE-7: probe 注册表对账不扩大 — check: `feedback-utils.py --action probes --validate` exit 0 且 internal = 73;`--reconcile` 错误集恰为既有的 `{skill:git-fleet, skill:git-server-init}`,不含 `/speckit.derive`

## Format: `[ID] [P?] [Story] Description`

`[P]` = 可并行(不同文件、无依赖)。状态标记:`[X]` 已关闭 · `[~]` 延后(附原因)· `[ ]` 未决。

### Task State Sigil (REQUIRED)

每行任务必须以 `- [X]` / `- [~]` / `[ ]` 开头,关闭时不得删除行——延后项保留并写明原因,以便 GATE-3 与状态机判定。

## Phase 1: Setup & Baseline

- [X] **T001** 冻结全套件名字级基线 → `.specify/specs/048-derive-command/baseline-failed.txt`(50 条;047 的 47 条清单**不可**复用,必须本分支自冻)
- [X] **T002** [P] 冻结门控基线 — `scan-confirmation-gates.py --root . --json` → total 23,cap 23.25(93×0.25),**零余量**
- [X] **T003** [P] 冻结 probe 基线 — `--validate` 5 classes / 72 internal,exit 0;`--reconcile` exit 2 且错误恰为 `skill:git-fleet` + `skill:git-server-init`(既有,留档避免误归因)

## Phase 2: Feature Registration

- [X] **T004** 注册 Feature 049 — 手工追加 7 列行至 `.specify/memory/features.md`、手工把表头 `**Total Features**` 48→49、`Last Updated`→2026-09-05;新建 `.specify/memory/features/049.md`。**MUST NOT 运行 `update-feature-index.sh`**(整体重写、输出 6 列丢掉 Spec Path、以目录 slug 与桩文本覆盖手写散文、重置全部 Status,而 `test_c3` 仍然通过——静默损坏)
- [X] **T005** 验注册表计数钉 — `pytest tests/contract/test_registry_completeness.py -q` → 3 passed(49 == 49)

## Phase 3: Requirements

- [X] **T006** `create-new-requirements.sh ... --short-name derive-command --json` → 发号 048、建分支 `048-derive-command`、脚手架 requirements.md
- [X] **T007** 撰写 requirements.md — 4 US(P1×3 + P2×1)、38 FR、6 SC、8 STR、Edge Cases、Out of Scope、Clarifications(6 条,含用户 5 项直接裁定)
- [X] **T008** [P] `checklists/requirements.md` — 需求质量清单
- [X] **T009** [P] `feature-ref.md` — requirement 048 → **新** Feature 049 归属裁定(5 个候选逐一驳回)+ US→FR→产物映射 + 交叉引用 040/041/046/047

## Phase 4: Plan & Design

- [X] **T010** `create-new-plan.sh --json`(**只跑一次**)→ 撰写 plan.md:Technical Context、Constitution Check 14 项(IX ⚠ Partial,三条 Complexity Tracking 论证)、Project Structure、Mirror Obligations 七行、Phase 0 R1–R6 内联、Phase 1 产物汇总(回填)
- [X] **T011** [P] `data-model.md` — 8 节固定序:7 实体 + `## Termination`;`access` 与 `confidence` 两个状态机 + 最小值传播规则;持久化表形与身份文法
- [X] **T012** [P] `contracts/derivation-model.md`(C-1…C-55)— 等级集、锚定规则、C1–C7 与 A1–A14 的**执行机制**、禁用论证字面量集的引擎钉死副本 + 漂移测试、title_mismatch 归一化算法、verification 反编造规则、降级契约
- [X] **T013** [P] `contracts/derive-engine.md`(C-1…C-38)— 六动作 flag 文法、退出码、JSON 信封、`moves.md` 独写、去重拒绝语义、单调发放、`probe-links` 离线容错且任何测试不得触网
- [X] **T014** [P] `contracts/derive-command-template.md`(C-1…C-36)— frontmatter(`short-description` ≤50)、节序(Feedback → Documentation → Handoffs,并说明 `sanitize.md` 倒序为何进不了该清单)、根相对引用 + `rewrite_paths` 升级、零 BLOCKING 命中、降级条款、客户中性
- [X] **T015** [P] `contracts/move-library.md`(C-1…C-43)— 表形与列序、身份文法、去重键、status 2×2 表、投影 vs 复制 + `<!-- projection of moves.md#M-nnn -->` 标记约定、git 跟踪、小文件阈值引用不复述
- [X] **T016** [P] `quickstart.md` — 三个走查(顺利路径 / 死链 + 改标题 / 无线上能力诚实降级)

## Phase 5: Concept Anchor

- [X] **T017** 撰写 `shared/definitions/derivation-definitions.md` — 开头声明所有权;四套 schema + Open Question;四级溯源等级;C1–C7;A1–A14;禁用论证集;`## Contradiction Handling`(**不用** `## Resolving a disagreement`);`## Script / Prompt Boundary`(**不用** `## 判定边界`);能力降级;`## Terminology Boundaries`;示例全部槽位化合成(零真实 URL / 标题 / 作者)
- [X] **T017a** 修正锚的四处设计缺陷(由下游契约撰写时暴露):① **跨作用域身份**——`M-` 项目级而 `S-` 主题级,anchor 改用限定形式 `<topic-slug>.S-<nnn>`(循 `<goal-slug>.T-<nnn>` 先例);② 删除无产出路径的枚举值 `access: not-found`、`resolved_via: publisher-index`;③ 补 `paywalled` 与「网络失败 ≠ 死链」(`access: unknown` ⇒ `grade: unverified`)两条协议分支;④ 算子 `status` 由「四值混装」规范为持久二值 `active`/`superseded`,run-relative 的 new/reused/reinforced 改为引擎输出而非库列
- [X] **T017b** 补 `A-<k>` 的跨作用域限定形式 `<topic-slug>.A-<k>`(Plan 跨主题引用元素时需要,与 `S-` 同构)
- [X] **T018** 守卫测试 `tests/contract/test_derivation_definitions.py` — 存在 + 镜像逐字节一致、开头声明所有权、四套 schema + 等级集 + Terminology Boundaries、零 BLOCKING 命中(import 扫描器的 `BLOCKING_RE`)、十二个保留标题零子串命中、零真实 URL、**禁用论证集与引擎常量漂移钉**

## Phase 6: Engine

- [~] **T019** [P] RED `tests/contract/test_derive_engine_contract.py` — **延后原因:执行序倒置**。引擎先落地并以 44 项端到端驱动验证,本测试随后由该驱动转写;契约(C-1…C-38)先于实现,Principle IV 的实质要求满足,严格 RED→GREEN 序未满足(见文首「执行序偏差」)。**交付物已落地并通过**:`tests/contract/test_derive_engine_contract.py` 存在且全绿;延后的只是**次序**,不是产物
- [~] **T020** [P] RED `tests/unit/test_derive_moves.py` — 同上,延后原因同一。**交付物已落地并通过**:`tests/unit/test_derive_moves.py` 存在且全绿;延后的只是**次序**,不是产物
- [~] **T021** [P] RED `tests/unit/test_derive_validate.py` — 同上,延后原因同一。**交付物已落地并通过**:`tests/unit/test_derive_validate.py` 存在且全绿;延后的只是**次序**,不是产物
- [X] **T022** 实现 `scripts/python/derive-utils.py`(stdlib only,六动作,房式对齐 `goal-utils.py` / `sanitize-utils.py`:命名 `EXIT_*` 常量、`--action`/`--workspace-root`/`--format`、`.specify` 镜像 REPO_ROOT 守卫)。**端到端驱动 44/44 通过**:init(含 no-clobber / `--force` / 坏 slug 拒绝)、moves-add 槽位同构去重拒绝并返回既有 id、限定锚点、25 类缺陷逐一命中正确规则编号、stats、exit 3
- [X] **T023** `probe-links` 离线容错 — **由真实环境证明而非仅夹具**:本仓环境 `HTTPS_PROXY=socks5://…`,stdlib urllib 无法穿越,六个 URL 全部失败,引擎返回 `access: unknown` + exit 0 + 不崩溃 + 不伪造 `dead`。任何测试不得触网
- [X] **T024** Tool 记录 `.specify/memory/tools/derive-utils.py.md`(Scope / Description / Resource ID / Invocation & I/O / Parameters / Behavioral Rules / Exit Codes / Environment Applicability `Status: Draft` / Mirror)

## Phase 7: Command Template

- [X] **T025** 撰写 `templates/commands/derive.md`(187→190 行)— frontmatter `description`(英文,不摘要工作流)+ `short-description` `联网核实权威源，提取思维方式，逐步推导出可溯源架构`(25 字符 ≤50)+ `handoffs`(plan / clarify);**无 `scripts:` 键**(内联引擎调用);节序 User Input → Glossary → Outline(九阶段)→ Behavior Rules → Boundary → **Feedback → Documentation → Handoffs**;根相对引用概念锚并声明引用不复述;零 BLOCKING 命中;降级条款;与 `/speckit.research` 的边界表
- [X] **T025a** 补 Stage 3「探活是佐证,不是落地路径本身」规则 — 由 dogfood 暴露:SOCKS 环境下 `probe-links` 全量 `unknown`,MUST NOT 被当作来源已死的证据,MUST 改用宿主自身抓取工具落地并把该证据写入 `verification`
- [X] **T026** [P] 守卫测试 `tests/contract/test_derive_command_surface.py` — 规范源存在 + frontmatter + `short-description` ≤50、四份副本 + AUTO-GENERATED 标记 + Qoder `description` 一致、引擎镜像逐字节一致、节序与相邻性、`docs-step.md` 引用 + `需记录`/`无需记录`、`feedback-utils.py` 与 `/speckit.derive` unit-id、**零 BLOCKING 命中**(import `BLOCKING_RE`)、降级字面量 `no-online-capability`、与 research 的边界声明、`docs/reference/commands/derive.md` 存在且该目录仍无 `README.md`
- [X] **T027** probe 登记 — `shared/definitions/probe-definitions.md` Objects 表插入 `| speckit-derive-wrapup | command-wrapup | /speckit.derive | wrap-up |`(clarify 与 docs 之间;`d-e-r` < `d-o-c`),与 T025 同批
- [X] **T028** 分类计数 +1 —`tests/contract/test_feedback_command_classification.py` `COMPLEX_COMMANDS` 加 `derive`、断言 18→19、docstring 18→19;`tests/contract/test_docs_step_injection.py` 加 `derive`、断言 15→16。`SIMPLE_COMMANDS` 两处集成副本**不动**(derive 是复杂命令)

## Phase 8: Docs, Map, Glossary

- [X] **T029** [P] `docs/reference/commands/derive.md` — `# /speckit.derive` → When to Use → Syntax → Execution Flow(九阶段)→ Output Artifacts → Boundary: derive vs research → Prerequisites → Next Steps;**不建** `README.md` / `index.md`
- [X] **T030** [P] `shared/definitions/framework-map.md` 加 `.specify/derive/` 行(Notes 指向 `definitions/derivation-definitions.md`);另记观察:该表亦缺 `.specify/goal/` 行(既有缺口,不在本特性顺手修)
- [X] **T031** [P] `.specify/memory/glossary.md` 追加四行(Derivation / Reasoning Move 思维算子 / Provenance Grade 溯源等级 / Derivation Chain 推导链),各指向真源
- [X] **T032** [P] 命令发现面**全量收敛**(不止加 derive 一行)— 四个面此前各自陈旧,单独补一行只会让覆盖更不一致,故按「全量收敛」处理:`docs/tutorials/quickstart.md` 补 5 行(derive 入 Quality Assurance & Research、feedback/sanitize/session 入 Governance & Extension、derive 入 Prerequisites & Next Steps);`docs/tutorials/installation.md` 补 6 行(derive/docs/feedback/interview/sanitize/session);`templates/vscode-settings.json` 的 `chat.promptFilesRecommendations` 13 → **25**(并重排为字典序,保留另两个键);`src/specify_cli/__init__.py` init 后的 `Optional:` 控制台行 10 → **19** 个命令。收敛后**四个面各自缺失命令数均为 0**(以 `templates/commands/*.md` 的 25 个模板为基准逐一核对)。`.vscode/settings.json` 是本仓未跟踪的本地安装产物且已与模板漂移,故**不动**——它由 `specify init` 再生成;`templates/vscode-settings.json` 的镜像经 sync-mirrors 已同步且 `--check` exit 0。quickstart.md 的 Prerequisites & Next Steps 表对更早的命令仍有缺行,属文档空间 reconcile,移交 `/speckit.docs`,本特性不顺手改

## Phase 9: Regeneration

- [X] **T033** `sync-mirrors.py --write` — 扇出 `shared/`(概念锚 + probe-definitions + framework-map)、`scripts/`(**严格对**:引擎源与镜像必须同批)、并委托 `regen-command-copies.py` 生成 4 份工具副本
- [X] **T034** `feedback-utils.py --action map` — 重建 `.specify/memory/feedback/probe-map.md`(派生视图,绝不手改);objects 72→73

## Phase 10: Integration, Dogfood & Close-out

- [X] **T035** [P] `tests/integration/test_derive_us1.py` — 四类语料 fixture(活链 primary / 存档救回的改标题 / community 清单体 / 死链不可救):等级与 access 符合协议、title_mismatch 仅改标题那条为真且为脚本算出、死链入 `## Unverifiable Sources` 带理由、零步骤锚定 community/unverified
- [X] **T036** [P] `tests/integration/test_derive_us2.py` — 同主题两次顺序运行:第二次复用第一次的 `M-`、仅追加 genuinely new、库中重复 `move_id` 与重复归一化 `inference_form` 均为 0
- [X] **T037** [P] `tests/integration/test_derive_us3.py` — 端到端 init→ground→moves→chain→architecture→`validate` exit 0(A 检查全绿 + `semanticChecksPending` 非空);损坏 fixture → exit 4;**降级路径** exit 0 且 `## Derived Architecture` 为空,而带步骤的降级产物 → exit 4
- [X] **T038** **Dogfood(本仓真实运行)** — 对用户 handed-in 的六条 REST/Web 架构文献真实联网核实。结果:仅 1/6 落地(kegel.com/c10k.html,live,primary,正文实读);S-003 与 S-005 **404 且无存档快照**(S-005 是清单未披露的缺陷——它把该链接作为「权威规范依据」推荐并给了 ⭐⭐);S-001/S-002/S-006 **403 阻塞**。产出 `.specify/derive/rest-architecture/derive.md`(6 来源 / 1 算子 / 1 步骤 / 1 元素 / 1 未决问题 / 终止条件 b)+ `moves.md`(M-001,限定锚点 `rest-architecture.S-004`)。`validate` **exit 0**,A1–A10 与 A12/A13 全绿,2 条诚实 warning,A11/A14 由 agent 显式背书
- [X] **T038a** dogfood 驱动的引擎修订 — `probe-links` 增加 SOCKS 代理预检 `detect_socks_proxy()`,输出 `proxyWarning` 指名环境变量并说明「unknown ≠ 已死」;stdlib urllib 无 SOCKS 支持而本仓 runtime 正依赖 `httpx[socks]`,故这不是边缘情形而是本项目的常态环境
- [X] **T038b** dogfood 驱动的引擎修订 — `## Termination` 的声明值与实际计数分歧(`step-count-diverges` / `budget-declaration-diverges`)定为 **warning** 而非 error:声明行是文档,引擎计数才是权威,真实预算超限已由 `step-budget-exceeded`(error)独立覆盖
- [X] **T039** 收尾 — features.md 行 049 `Draft`→`Implemented` + provenance 注记、`features/049.md` Status Tracking、`verification.md` 覆盖 SC-001..SC-006

## Phase 11: 契约—实现收敛(实现期纠偏)

首轮引擎按口头规格落地并通过 44 项驱动后,独立撰写的契约暴露出接口实质性分歧。判定为**契约更严也更好**(且 camelCase 与本仓 `sanitize-utils.py` 房式一致:`semanticCandidates` / `evidencePack`),故重写引擎去符合契约,而非弱化契约迁就实现。若当时让测试直接对着实现写,会得到一套全绿、而契约沦为装饰的结果。

- [X] **T022a** 引擎重写至契约形态 — 固定信封(`ok` / `action` / `workspaceRoot` / `generatedAt` / `errors[]` / `warnings[]` / `semanticChecksPending[]` / `notes[]` / `payload{}`)、`--slug` 取代 `--topic`、移除 `--timeout`(改为常量 `PROBE_TIMEOUT_SECONDS = 10`)、camelCase payload、`--force` 留 `.bak` 并报 `clobbered` / `backupPath`、`moves-add` 输入加 `intent` 四值、原子写(`.part` + `os.replace`)、**单一传输缝 `_http_get`**(这是「任何测试不得触网」可被机械断言的前提)、`.specify` 镜像 `REPO_ROOT` 守卫、audit 结果由 `errors[]` 派生并按 `(rule, locator)` 去重
- [X] **T022b** 修复**不可达死码** — `BARE_ATTESTATIONS` 的每个成员都不足 16 码点,故契约 C-31 原定的「长度检查在前」会让 `verification-bare-attestation` 永不可达,而它恰是信息量更大的那一个诊断。改为先判裸断言、再判长度下限,两道硬检各自可达;契约 C-31 同步修订并写明理由
- [X] **T022c** 修复 `byAccess` 破坏完整枚举 — `access` 含参数化成员 `wayback:<ts>`,按原值 tally 会把每个快照时间戳变成独立键,使 C-19 的「键集恒为完整枚举」当场失效(SC-001/SC-002 依赖它免探形状直接断言)。引入 `ACCESS_BUCKETS` + `access_bucket()` 归并为 `wayback`
- [X] **T022d** 端到端驱动重跑至全绿 — **102 项检查 ALL GREEN**,其中 41 类违例逐一断言 exit 4 与预期 error code;另覆盖信封键集、`--slug`/`--file` 互斥、`--max-steps 0` 拒绝、init no-clobber 与 `.bak`、warning 集封闭性(恒 ⊆ 六元集)、`probe-links` 离线容错(不可达主机 → `access: unknown`、exit 0、`online=false`、`degraded=true`)、降级产物 exit 0 而「降级却带步骤」exit 4
- [X] **T015a** 契约勘误三处 — ① **C-25 与 C-38 联立不可满足**:被未决问题阻塞的元素若其步骤全为 `derived`,则「confidence 等于最小秩」与「须为 provisional / contested」无解;该矛盾只在动手构造合法 fixture 时暴露,两份契约分别读都无懈可击。裁定不给任一条开例外,改为「问题所依附的步骤本身 MUST 为 provisional」,经最小值传播二者同时成立,已写入 C-25;② FR-005(每个 `unverified` 来源须记入 `## Unverifiable Sources`)原先**无任何 error code 归属**,A2 映射集只有 `premise-grade-ineligible`,补 `unverified-source-unrecorded`;③ C7 的「少于 2 行」下限**不可满足**(记录形态是单行 `- derivation: <value>` 字段),契约表与 C-13 同步修订为仅保留 40 码点下限并写明恢复条件
- [X] **T007a** STR-001 值单元格去标签前缀 — *Value (verbatim)* 列原携带 `封闭禁用论证字面量集:`,致首元素解析为「标签+字面量」,三方漂移守卫(概念锚 §Banned Justifications / 引擎 `BANNED_JUSTIFICATIONS` / requirements STR-001)不成立;前缀移入 *Consumed by* 列、值列保持逐字,三处 15 条实测集合相等
- [X] **T025b** 命令模板同步契约化 CLI — `--topic` → `--slug`(3 处);Stage 4 补 `moves-add` 输入形态(`{"moves": [...]}` + camelCase + `intent` 四值 + 全有或全无)与**限定锚点强制**(裸 `S-<nnn>` 被拒,因 `moves-add` 不携带 topic 无从限定,而写进库的裸形式会在下次 `validate` 触发 `anchor-form`);Stage 7 补**两趟自审**机制(`validate` 零写入,12 行引擎结果须与派生值逐字相等,故须先取 `payload.audit.engine` 派生值、由 agent 誊写进表、再重跑收敛;「誊写引擎给出的值」与「自己判一个值填进去」是两件事,后者是 C-20 禁止的手写)
- [X] **T038c** dogfood 重跑至契约形态 — 重建 `.specify/derive/`(旧库由前版引擎写入,列分隔与锚点形态已变),重跑 init → moves-add(`intent: new`、限定锚点 `rest-architecture.S-004`)→ 誊写自审 → `validate`:**exit 0、errors 0、warnings 5**(全为 `unresolved-title`,属封闭六元集),`byAccess={live:1, wayback:0, dead:2, paywalled:0, unknown:3}`,`audit.semantic={A11: attested, A14: attested}`

## Dependencies & Execution Order

### Phase Dependencies

P1 → P2 → P3 → P4;P5 与 P4 并行并闸住 P6–P8;P6 → P7 → P8 → P9 → P10。

### Critical Path

T001 → T004 → T006 → T007 → T010 → {T011–T015} → T016 → T022 → T025 → T027/T028 → T033 → T034 → T038 → T039。

### 并行实际用法

T008/T009、T011–T015、T018/T026/T029–T031、T019–T021/T035–T037 各以并行批次执行。并行撰写下游契约时暴露了概念锚的四处设计缺陷(T017a),其中跨作用域身份缺陷若未在实现前修掉,会让算子库的 `anchor` 从第二个主题起全部不可解析——这是本特性最有价值的一次漂移检查。
