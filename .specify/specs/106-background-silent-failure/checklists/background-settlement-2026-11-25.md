# Requirements-Quality Checklist: Background Dispatch Settlement — 后台派发静默退出结算契约（Background Dispatch Settlement）

**Purpose**: 检验 Feature 106 需求文本（41 FR / 9 SC / 4 Shared Strings）的**写作质量**——结算值封闭集与逐值正证据是否可判定、六个后台载体的证据义务是否逐载体具名且 C5 排除是否显式、静默结束后的反应（report / retry / stop）是否非静默且可验收、判定面与变异演练义务是否可转红且行为类不冒充机器覆盖、保留面空允许差异集是否由具名回归承载、加性版本与 legacy 标注/拒绝语义是否闭合、EP-001…EP-005 与边界案例是否落到可判定处置、以及每条 FR / SC 的承载是否可追溯。每条都是对需求文本（或它点名的 owner 行 / plan 前提）的提问，**不是**对实现行为的检验：凡只有跑一遍产品才能回答的条目，本身就是本清单的缺陷。
**Created**: 2026-11-25
**Feature (Requirement Scope)**: `.specify/features/095-superagent-role.md`（Feature 095 Super Agent Role；本规格为 slice 行 106，`.specify/features.md` 行 106 状态 `Planned`，父行保持 `Ready for Review`；本轮位于 `/speckit.implement` 之前，按 Feature Integration Protocol 不发起 `Implemented → Ready for Review` 迁移）
**Requirements (What)**: [../requirements.md](../requirements.md) — 本轮机械读数（2026-11-25，`validate-requirements.py`，逐字输出见 `../test-evidence/checklist-requirements-validator.txt`）：**312 行 / 0 error / 0 warning**；**41 FR**（FR-001…FR-041）、**9 SC**（SC-001…SC-009；final 3 / supporting 6）、**4 Shared Strings**（STR-001…STR-004）、5 个用户故事、14 条 Edge Cases、A-1…A-18（18 条裁定）、4 行 Runtime Stack（RS-001…RS-004）、3 段 Clarifications 会话。
**Specifications (How, context only)**: [../plan.md](../plan.md)（5 条 Execution Premises EP-001…EP-005，含 EP-005 `falsified` → `fallback`；3 条 Decision Tensions T-001…T-003）、[../tasks.md](../tasks.md)（**37** 任务行；34 条款各被认领一次；§ Requirement Coverage Map 41/41）、[../contracts/](../contracts/)（**3 文件 / 34 条款**：C-01…C-12 / C-13…C-24 / C-25…C-34）、[../data-model.md](../data-model.md)（9 实体 E1–E9 / 12 不变量 INV01…INV12）、[../quickstart.md](../quickstart.md)（8 场景 S-0…S-7）——**只**用于暴露需求的缺口、歧义与冲突，**从不**为它们自身打分。
**Readers**: 需要判定「106 的需求是否足以从 checklist 放行进 analyze / implement」的复核者——`/speckit.analyze` 的检测者、`/speckit.implement` 的协调者与后续接手本线的编写者；他们依据本清单、被引用的需求行与 `test-evidence/` 的机读读数取结论。
**Reading scenario**: 复核者打开本文件，决定三件事：(1) 哪几条需求缺陷必须在 analyze / implement 之前修掉；(2) 哪些项可登记为「已裁定、由下游承载」而放行；(3) 哪些项因判据依赖尚未落地的机制而保持 `not_evaluated`。按条末的 `[Req §…]` / `[plan §…]` / `[contracts §…]` 锚回到正文逐字核对。
**Focus / Depth / Audience**: Focus = 阶段简报的八个维度簇（结算语义 / 载体一致性 / 反应义务 / 执行与守卫 / 保留面 / 迁移与 legacy / 依赖、假设与边界 / 可追溯性）；Depth = **Deep**（简报把八维度写成必覆盖集并要求 41 FR + 9 SC 全覆盖，默认 Standard 不足以承载）；Audience = **Reviewer**。阶段简报已使意图明确，技能 §2 的三个意图澄清问题按「已预答」跳过，默认值与升深理由记录于此。
**Detection path**: same-author 条件**不成立**——`requirements.md` / `plan.md` / `tasks.md` 由上一条无人值守 SDD 线内的独立阶段执行体撰写，本执行体未曾撰写所分析的任何制品；按 `.specify/shared/workflow/objective-analysis-gate.md` § When the gate fires 的「制品先于本会话或作者不同」分支，门不触发，未派发 fresh-context 检测代理（本派发亦明令不得再派发代理）。缺口扫描由本执行体直接完成；可机械核对的前提（FR / SC / STR 计数、条款数、任务行数、EP 行数、边界案例数）均以程序读数当场取证，读数见 Notes。

**Note**: 由 `/speckit.checklist` 按 `.specify/skills/internal/create-checklist/SKILL.md` 生成，方法论 owner 为 `.specify/shared/guidelines/checklist-methodology.md`，结构模板为 `.specify/templates/checklist-template.md`。勾选一条的唯一依据是**需求文本本身**（或该条目点名的 owner 行 / plan 前提）给出了答案；答「否」产出的是对 `requirements.md` 的 finding，不是一条实现任务。判据落在需求之外（下游文档 / 工具）时登记为**观察**；判据依赖尚未落地的机制时登记为 `not_evaluated`。

## 一、结算值集合与逐值正证据（Settlement semantics）

- [ ] CHK001 - 结算值封闭集是否被逐字写出为七个值、三个语义类（终态 / 非终态 / 检测缺陷），并规定集合外取值被拒绝；两个共享字符串（[[STR-001]] / [[STR-002]]）是否逐字出现且其值表只由唯一 owner 拥有？[Completeness, Req §FR-001, Req §A-3, contracts §C-01]
- [ ] CHK002 - `completed` 是否要求「终端成功记录 **且** 独立核验通过」两件同时成立，并把仅 exit 0、日志末尾好看、父侧期望列为不构成证据；「独立核验」的机制集合是以「例如」举例的开放列表还是封闭枚举，其封闭性由谁拥有、能否判定？[Clarity, Ambiguity, Req §FR-002, Req §Settlement Evidence Matrix, contracts §C-02]
- [ ] CHK003 - `failed` 的正证据是否穷举为非零终端记录、具名失败返回、exit 0 缺完成证据三类，并明确「无输出 / 日志停止增长 / 父侧等待超时」不得读作失败？[Completeness, Req §FR-003, Req §Settlement Evidence Matrix, contracts §C-02]
- [ ] CHK004 - `anomaly` 是否被限定为「显式异常信号 **且** 终端证据」，并规定进程仍活时的异常行只记 observed、该尝试仍为 `running`；`cancelled` 是否被限定为父侧经既有纪律写下的显式取消记录，且进程死亡 / 连接断开 / 提前退出被明确排除？[Clarity, Req §FR-004, Req §FR-008, contracts §C-02, contracts §C-09]
- [ ] CHK005 - `running` 是否要求**结算时刻复核过**的活证据，可接受的活证据（pid 存活且非僵尸/未复用、心跳新鲜、活日志在阈值内增长、返回通道仍开放）是否逐项枚举，陈旧读数被排除；「声明阈值」由谁声明、阈值本身是否被量化？[Clarity, Ambiguity, Measurability, Req §FR-005, Req §Settlement Evidence Matrix]
- [ ] CHK006 - [[STR-001]]（`silent-end`）与 `completed` / `failed` / `running` 的边界是否可测试地钉死（不得折算、不得报成仍在运行），三件同时成立的要求是否写全（起点记录、执行主体消失、四类终态证据缺席）；对无 pid 载体的「声明等待期限」由哪个记录的哪个字段承载、由谁声明？[Clarity, Ambiguity, Req §FR-006, contracts §C-03, data-model §E2, data-model §E3]
- [ ] CHK007 - [[STR-002]]（`unknown`）是否被定义为证据不可读/不可解析的**检测缺陷态而非结束**，要求点名不可读指针，并承担与 [[STR-001]] 相同的「不得声称成功」反应？[Completeness, Req §FR-007, contracts §C-04]
- [ ] CHK008 - 每次尝试的唯一 label、重试即新尝试/新 label、旧证据保留、旧尝试晚到返回不得被当成本次结果消费，是否在需求与 owner 两侧表述一致且无未定义聚合词？[Consistency, Req §FR-009, contracts §C-05]
- [ ] CHK009 - 起点记录（尝试身份、载体、父身份、开始时间、进程载体 pid）是否被要求写入**既有父侧载体**，缺起点记录即 [[STR-002]] 而非 `completed`；返回通道（含七字段角色的 `return_channel`）被声明为子侧发起的上行、其沉默不读作存活或完成，是否同时写明？[Completeness, Clarity, Req §FR-010, contracts §C-06]
- [ ] CHK010 - 「父侧在对外可见的完成报告之前结算它开过的每个尝试」是否被写成可判定顺序，且任一尝试未结算时成功结论不得成立？[Measurability, Req §FR-011, contracts §C-07]

## 二、载体一致性（Carrier conformance）

- [ ] CHK011 - 载体清单是否声明为**封闭**（C1…C6），新载体必须走规格修订、不得静默加入；每个派发入口与派发职责定义是否都指向同一个结算 owner，第二张状态值表 / 第二份证据矩阵 / 载体私有判定副本是否被禁止，叶子执行者模板是否被明确排除在第二套结算逻辑之外？[Completeness, Consistency, Req §FR-012, Req §FR-013, Req §Dispatch Carrier Inventory, contracts §C-22]
- [ ] CHK012 - C1 的处置是否保持四件套与 watcher 判定/退出码/哨兵字面量/`--self-test` 不变，并给出逐 token 映射（DONE / FAILED / ANOMALY / INCOMPLETE / DEAD / NO_SIGNAL / TIMEOUT / RUNNING），其中 DONE 需带 U4 证据指针、TIMEOUT 与 RUNNING 需结算时刻活检查否则归 [[STR-001]]？[Completeness, Req §FR-014, contracts §C-13]
- [ ] CHK013 - C2 的加性起点/终止证据是否逐字段具名（attempt id、carrier、parent、`started_at`、`pid`、`pid_start_ticks`、`settlement_version`；`exit` / `signal` / `ended_at`），TERM/INT/HUP trap 与 SIGKILL 不可捕获是否写明，既有 `.status` 行格式是否逐字保持，五条按证据成立（含 exit 0 无完成声明 → `failed`(incomplete)）的规则是否与证据要求成对？[Completeness, Consistency, Req §FR-015, Req §FR-016, contracts §C-14, contracts §C-15]
- [ ] CHK014 - C3 报告是否被要求为每个被派发席位记录 `end_state`（[[STR-003]]）与证据指针两个**加性列**，legacy 5 列仍被接受，空值记 `settlement-unrecorded`、`completed` 无证据指针记 `settlement-unbacked`，`## Verification` 声明结算覆盖，且席位静默死亡时不得以成功语气收尾？[Completeness, Req §FR-017, contracts §C-16]
- [ ] CHK015 - C4 native 是否被要求派发前写尝试记录、返回时按五要素结算（缺一即 `failed`(incomplete) 且不得消费）、宿主报错即 `failed`、声明的等待期限已过且无返回无活信号即 [[STR-001]]；宿主不提供后台形态时是否显式声明为前台终结、不伪造结算边？[Completeness, Req §FR-018, contracts §C-17]
- [ ] CHK016 - C5 virtual 的排除是否被写成显式规则（不能脱离会话、父侧即执行者、无孤儿边、排除理由、未完成不得报 `completed`），而不是隐含承诺或借口？[Clarity, Req §FR-019, Req §A-4, contracts §C-18]
- [ ] CHK017 - C6 直接外部配方是否被限定为两种形态（合规 runner/wrapper 后台形态，或显式「前台返回即终止」），原先「超时无哨兵＝stall」的含混句是否被替换为逐值处置（无哨兵 + 主体消失/无终止记录 → [[STR-001]]；不可读 → [[STR-002]]；无哨兵但主体仍活 → `running`）？[Clarity, Req §FR-020, contracts §C-19]
- [ ] CHK018 - 只读验证波是否要求对每个校验者结算，缺失状态/结论记 `failed`(incomplete) 并按「既有规则」重问、不得从波次结果静默消失；该「既有规则」是否以具名 owner 指针抵达而不是悬空引用？[Clarity, Req §FR-021, contracts §C-20]
- [ ] CHK019 - observer 是否保持可选（MAY 记录结算事实但不得成为唯一结算载体，无 observer 的线仍必须结算），且不新增 probe class / handler binding 的禁止是否可判定？[Completeness, Req §FR-022, contracts §C-21]

## 三、反应义务（Reaction obligations）

- [ ] CHK020 - 结算为 [[STR-001]] 或 [[STR-002]] 时的上送是否包含发现内容、为何吃重、已产生的中间产物与可选处置，明确禁止成功语气，并禁止未加诊断就按普通失败原样重派？[Completeness, Req §FR-023, Req §SC-004, contracts §C-08]
- [ ] CHK021 - 重试是否被要求为**新尝试、新 label**、旧证据保留、既有重试上限不变，且对 [[STR-001]] / [[STR-002]] 的重试附具名诊断或用户裁定（fast-fail 区分异常停与普通失败）？[Completeness, Consistency, Req §FR-024, contracts §C-08]
- [ ] CHK022 - 停止 / 终止 / 取消是否被要求遵守既有破坏性动作纪律、watcher 不得杀进程；对活尝试选择「不再等待」时记 `running` + 活证据 + 停止理由而非 [[STR-001]]，是否可判定？[Consistency, Req §FR-025, contracts §C-08]
- [ ] CHK023 - 静默修复的禁止是否以封闭清单给出（不代写终止记录、不补齐缺失返回字段、不改写 `.status`/报告/证据、不删除证据、不把 [[STR-001]]/[[STR-002]] 改写成 `failed`/`completed`、不消费过期返回）？[Completeness, Req §FR-026, contracts §C-08]
- [ ] CHK024 - 父侧成功报告是否要求携带逐尝试结算值与证据指针、仍在跑者标「未结算」，并禁止失败 / 异常 / [[STR-001]] / [[STR-002]] 被聚合语气覆盖？[Completeness, Req §FR-027, contracts §C-07]

## 四、可执行判定、守卫与诚实边界（Enforcement）

- [ ] CHK025 - 判定面是否被定义为一个确定性、只读、零写入/零新存储的判定面，分类表只有一个 owner 且被测试钉住；是否要求接入至少一个能转红的守卫并覆盖六类情形（集合外值 / 无完成证据却声称 `completed` / 无活证据却声称 `running` / 无「消失 + 缺席」证据却声称 [[STR-001]] / 被派发却无结算行 / [[STR-002]] 被当成通过）；它是否只能是 `role-edge-check.py` 的**加性**扩展且 `report` / `query` 输出逐字节不变，第二判定引擎必须先记录「既有 owner 不覆盖」裁定？[Completeness, Consistency, Req §FR-028, Req §FR-029, Req §SC-002, contracts §C-25, contracts §C-26, contracts §C-27]
- [ ] CHK026 - 变异演练是否被定义为四项具名 drill（移除/削弱静默终止检测、活证据要求、让 [[STR-002]] 通过、证据指针要求），每项至少一条测试转红并留证；「未转红即记守卫缺陷、不得软化」是否明写？[Measurability, Req §FR-030, contracts §C-30]
- [ ] CHK027 - 清单内每个后台可脱离载体是否被要求至少一个确定性静默形态测试与一个反向活体夹具（活着的尝试不得误报 [[STR-001]]，长时间无输出但存活保持 `running`），缺测试的载体是否被判缺陷；C5 的排除与 C4 的前台终结分支是否各有断言？[Coverage, Req §FR-031, Req §SC-001, Req §SC-005, Req §SC-008, contracts §C-31]
- [ ] CHK028 - 新测试是否被要求经 `scripts/bash/run-tests.sh` 唯一入口运行、使用确定性夹具/假 CLI/事件文件而非固定等待、同时断言正向与反向、不新增第三个全量槽位，且同一夹具重复运行的结算判定差异为 0？[Measurability, Req §FR-032, Req §SC-007, contracts §C-32]
- [ ] CHK029 - 行为类义务是否以**封闭集合**被点名（FR-005 结算时刻活检查、FR-011 先结算再报告、FR-023 反应上送、FR-025 停止活尝试记录、FR-026 禁止静默修复、FR-027 逐尝试覆盖、FR-017 的成功语气半边、FR-030 的演练执行义务），并明确不得冒充已被机器守卫覆盖？[Clarity, Consistency, Req §FR-041, contracts §C-34]

## 五、保留面与兼容（Preservation）

- [ ] CHK030 - 保留面是否以「空允许差异集」表述，并同时给出基线参照物（`fbab7a45c`）、比较单元（watcher 判定 token / 退出码 / 哨兵字面量三集合）、允许集来源、补集断言（成员差集为空）与无未定义聚合词；[[SC-003]] 的抽取输入是否逐项点名（脚本 + `--help` + `--self-test` 输出）且 `--self-test` 通过率可判定？[Measurability, Req §FR-033, Req §SC-003, contracts §C-23]
- [ ] CHK031 - 新增字段/文件是否一律要求**加性**，既有 `.status` 行格式、五要素上行、七字段下行、确认纪律冻结预算与两槽位测试预算是否逐项声明保持不变；是否存在把「保持不变」写成可机械判定的出现规则（而非形容词）？[Clarity, Consistency, Req §FR-033, Req §A-9, contracts §C-23]

## 六、迁移、legacy 与分发（Migration / legacy）

- [ ] CHK032 - 新格式记录是否以加性字段 `settlement_version`（[[STR-004]]）声明契约版本且不改既有行格式，无版本记录是否在结算判定/审计输出中标 `legacy`、不计合规、不被改写、且标注本身不产生失败退出码；边界案例把「缺起点记录」写成 `legacy/unknown` 的读法，是否与 FR-010 的单一读法（[[STR-002]]）和 FR-034 的 legacy 定义（缺版本）一致，是否需要消歧？[Clarity, Ambiguity, Consistency, Req §FR-034, Req §SC-006, Req §Edge Cases, contracts §C-10, contracts §C-33]
- [ ] CHK033 - 任何对既有路径/文件/字段/状态行契约的不兼容变更是否被要求附带迁移路径或确定性拒绝并附测试、且禁止静默混合态；本特性的不兼容变更清点是否显式声明为**空集**，使「每个不兼容变更…」的全称断言退化为可判定的空真而不是悬空承诺？[Measurability, Req §FR-035, contracts §C-33]
- [ ] CHK034 - 两顶帽子是否写明（改动落框架源与模板；`.specify/` 镜像经既有同步/安装流程再生、不手改；客户项目经 init/refresh 获得同一契约），文档更新是否被要求落在唯一 owner 章节、引用它的技能/命令与 `docs/reference/` 页面，且值受「与代码一致、禁止复制第二份集合/映射」约束？[Completeness, Consistency, Req §FR-036, Req §FR-037, Req §A-11]

## 七、范围封闭、非目标与确认纪律（Scope / non-goals）

- [ ] CHK035 - 零新增机制是否以可判定的禁止项表述（不新增调度器、守护进程、队列、注册表、通知通道、存储或 child list；复用既有载体与判定面；observer 保持可选），非目标是否显式且可检验（不自动 kill/stop、不推送/合并/删除分支/改写远端、不删除证据、不改 SDD 阶段语义与授权、不回溯改写历史报告/规格）？[Clarity, Req §FR-038, Req §FR-040, Req §A-13, contracts §C-24]
- [ ] CHK036 - FR-039 与 [[SC-009]] 的「冻结 total 保持基线值且相等判定保持绿色」是否点名了一个**实际为绿**的基线参照物；当 EP-005 已实测该相等判定在基线即为红（live 31 ≠ 冻结 27）时，需求文本是否给出替代判据（触及文件零新增命中）作为操作口径，而不是留下一个基线已红却被声称可保持绿的验收条款？[Consistency, Measurability, Req §FR-039, Req §SC-009, plan §Execution Premises, plan §EP-005 fallback]

## 八、依赖、假设与边界覆盖（Dependencies / assumptions / edge cases）

- [ ] CHK037 - EP-001…EP-005 是否逐行具备 Evidence / Status / Decision 三要素且互不矛盾；EP-005 的 `falsified` → `fallback` 是否给出可复核的替代测量（按文件命中数不增长）并明确「既有红如实上报、不声称绿」，使依赖该前提的 FR-039 / SC-009 不被读成已满足？[Assumption, Gap, plan §Execution Premises]
- [ ] CHK038 - 边界案例是否逐条落到可判定的结算值与反应，而非仅描述现象——至少覆盖 SIGKILL / 宿主丢失与父代理自身死亡（含交接被遗弃后凭持久载体重建）/ pid 复用与僵尸 / 期限后晚完成 / 存活但长时间无输出 / 证据不可读 / 派发前失败的记录形态与结算值 / 多子执行体聚合 / observer 不在场 / 宿主不提供后台 native / 并发重试；其中「派发前失败」是否点名了它产出的记录形态与所属结算值（既不 `silent-end` 也不进重试计数）？[Coverage, Gap, Req §Edge Cases, Req §FR-005, Req §FR-006, Req §FR-016, Req §FR-018]
- [ ] CHK039 - 18 条假设裁定（A-1…A-18）是否非阻塞且与其喂给的 FR 成对，A-15 的词汇表提议通道是否被声明为不阻塞验收；4 行 Runtime Stack（RS-001…RS-004）是否各具 Owner / Pin / Contract / Premises（EP-001…EP-004）且「零新增第三方依赖」可被机械判定？[Assumption, Dependency, Req §Assumptions & Decisions, Req §Runtime Stack]

## 九、可追溯性与可测量性（Traceability & measurability）

- [ ] CHK040 - 每条 FR 是否都有承载面（contracts / tasks / Requirement Coverage Map），每条 SC 是否都有具名测量来源与 final / supporting 路径，尤其 final 路径的 SC-001 / SC-002 / SC-004 是否各有可复现的源；未被任何契约条款引用的 FR-036 / FR-037 / FR-039 / FR-040 是否在任务侧有显式会计面而非静默缺口；所有 `[[STR-NNN]]` 引用是否可解析到 Shared Strings 行且正文不存在未登记的重复字面量？[Traceability, Consistency, Req §SC-001…SC-009, Req §Shared Strings, Req §Measurement Sources, tasks §Requirement Coverage Map]

## Notes

- **勾选与判读**：`[x]` 表示该问题已依据需求文本（或点名的 owner 行 / plan 前提）得到回答；答「否」即对 `requirements.md` 的 finding，不是一条实现任务。本阶段交付的是清单器械，逐条作答属于 analyze / review 的判定职责。
- **计数与追溯**：共 **40 条**，CHK001…CHK040；**40/40** 携带至少一个追溯锚（`[Req §…]` / `[plan §…]` / `[contracts §C-NN]` / `[tasks §…]` / `[data-model §…]`），满足 ≥80% 下限；soft cap 40 未超出；CHK 编号唯一且顺序连续；零 `Verify` / `Test` / `Confirm` / `Check` 开头的实现检验式条目。
- **维度覆盖（简报八项 → 章节）**：Settlement semantics → §一（CHK001…CHK010，10 条）；Carrier conformance（C1/C2/C3/C4/C6 在范围内、C5 显式排除、逐载体证据义务）→ §二（CHK011…CHK019，9 条）；Reaction obligations → §三（CHK020…CHK024，5 条）；Enforcement（钉住测试 / 红先 / 变异演练 / 行为类边界）→ §四（CHK025…CHK029，5 条）；Preservation（空允许差异集 + 加性）→ §五（CHK030…CHK031，2 条）；Migration / legacy → §六（CHK032…CHK034，3 条）；Dependency / assumptions / edge cases → §七–§八（CHK035…CHK039，5 条）；Traceability → §九（CHK040，1 条）。
- **FR 覆盖（41/41，每条至少一次）**：FR-001→CHK001；FR-002→CHK002；FR-003→CHK003；FR-004→CHK004；FR-005→CHK005；FR-006→CHK006；FR-007→CHK007；FR-008→CHK004；FR-009→CHK008；FR-010→CHK009；FR-011→CHK010；FR-012→CHK011；FR-013→CHK011；FR-014→CHK012；FR-015→CHK013；FR-016→CHK013；FR-017→CHK014；FR-018→CHK015；FR-019→CHK016；FR-020→CHK017；FR-021→CHK018；FR-022→CHK019；FR-023→CHK020；FR-024→CHK021；FR-025→CHK022；FR-026→CHK023；FR-027→CHK024；FR-028→CHK025；FR-029→CHK025；FR-030→CHK026；FR-031→CHK027；FR-032→CHK028；FR-033→CHK030、CHK031；FR-034→CHK032；FR-035→CHK033；FR-036→CHK034；FR-037→CHK034；FR-038→CHK035；FR-039→CHK036；FR-040→CHK035；FR-041→CHK029。
- **SC 覆盖（9/9，每条至少一次）**：SC-001→CHK027；SC-002→CHK025；SC-003→CHK030；SC-004→CHK020；SC-005→CHK027；SC-006→CHK032；SC-007→CHK028；SC-008→CHK027；SC-009→CHK036。
- **机械读数**（2026-11-25，逐字输出见 `../test-evidence/checklist-requirements-validator.txt` 与 `../test-evidence/checklist-artifact-counts.txt`）：`validate-requirements.py` → `status: ok`，0 error / 0 warning，**312 行 / 50 definition rows（41 FR + 9 SC）/ 4 shared strings**；程序计数：A 行 **18**、用户故事 **5**、边界案例 **14**、契约 **3 文件 / 34 条款**、任务行 **37**、EP 行 **5**、RS 行 **4**、SC `final` 标注 **3**（SC-001 / SC-002 / SC-004）、quickstart 场景 **8**、data-model 实体 **9** / 不变量 **12**；`.specify/features.md` 行 106 状态 **Planned**（父行 095 保持 `Ready for Review`）。
- **same-author 检测门**：不成立（见 Detection path）；未派发 fresh-context 检测代理，检测路径如实记录于此，不以委托路径冒充直接读。
- **本阶段无 plan-owned 改动**：本文件位于 `checklists/`，`plan.md` / `data-model.md` / `contracts/` / `quickstart.md` / `research.md` / `feature-ref.md` 未被触碰，故无 `PLAN-EDIT:` 声明。
- **新增而非覆盖**：本文件为 checklist 阶段**新增**清单；requirements 阶段产出的 `checklists/requirements.md` 保持原样，未被覆盖、未刷新。
- **待下游裁定的观察（不阻塞本阶段）**：本清单的 `[Ambiguity]` / `[Gap]` 条目指出的候选确认点——「声明等待期限」与「声明阈值」的 owner/字段（CHK005 / CHK006）、`completed` 独立核验机制的开放/封闭性（CHK002）、验证波「既有规则」的 owner 指针（CHK018）、边界案例 `legacy/unknown` 读法与 FR-010 的消歧（CHK032）、FR-039 / SC-009 基线已红与 EP-005 fallback 的口径（CHK036）、派发前失败记录的形态与结算值（CHK038）——由 `/speckit.analyze` 或实现阶段按判据取证，不在本阶段预先裁定。
- **Feature 状态**：本轮位于 `/speckit.implement` 之前，按 Feature Integration Protocol，checklist 不发起 `Implemented → Ready for Review` 迁移，仅产出清单。
