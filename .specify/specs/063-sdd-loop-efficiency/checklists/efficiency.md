# 需求质量检查清单：063 SDD Loop Efficiency（四项运行效率优化）

**Purpose**: 验证四项运行效率优化（中型特性快车道、两槽位测试预算、plan 只小修约束、stream-json 进度与 nohup 解耦）的需求质量、可判定性、完整性与一致性——需求写作的“单元测试”，不是实现行为验证。
**Created**: 2026-10-20
**Feature (Requirement Scope)**: 063-sdd-loop-efficiency → Feature 058 无人值守 SDD 循环驱动机制（演化特性）
**Requirements (What)**: [requirements.md](../requirements.md)
**Specifications (How, context only)**: [plan.md](../plan.md)、[tasks.md](../tasks.md)、[contracts/](../contracts/)、[data-model.md](../data-model.md)
**Checklist Domain**: efficiency / decidability / completeness / consistency
**Depth**: Standard · **Audience**: Reviewer（框架维护者与无人值守运行操作者）

**Note**: 本清单由 `/speckit.checklist` 生成，判定对象是 **Requirements (What)**；`plan.md` / `tasks.md` / `contracts/` / `data-model.md` 仅用于发现需求缺口、歧义、冲突与溯源问题，不作为被评分的对象。既有 [requirements.md](requirements.md) 质量清单（16/16）保持不变，与本清单互不覆盖。

## 判定口径与证据方法

- **计数由命令派生，不手抄**：FR 定义行 43、SC 定义行 13、任务行 52、Shared Strings 8、验收场景 28、Edge Cases 25、Assumptions 12；既有 `checklists/requirements.md` 为 16/16 全勾选。2026-10-20 tasks-repair-2 收口 CLI-profile 条款后复算；本清单生成时的 6 strings 为 dated 读数。
- **可判定性口径**：每项判定给出文件与行号、字段名、字面量或命令输出；无法从规范文本唯一判定的项判 **FAIL**，不以“看起来合理”代替证据。
- **同作者门**：本清单阶段由具备新鲜上下文的阶段子代理执行；`requirements.md`、`plan.md`、`tasks.md` 由前序阶段生成，本阶段未参与其写作——未触发 `.specify/shared/workflow/objective-analysis-gate.md` 的同作者委派条件。
- **不通过项**：保留为 `[ ]`，逐项记录缺口与建议处置；不为全绿而降低判据。汇总见 § 不通过项汇总。
- **本阶段测试证据（E3）**：`status=not-run-docs-only`；本阶段只新增 `checklists/efficiency.md`，未改可执行面或测试面，改动路径证据即本文件路径。

## 1. 中型特性快车道：准入与回退

- [x] CHK001 - Are the fast-lane's only enabling form, its exact required location, and its disqualifying alternatives all specified as testable text? [Clarity, Req §FR-002; FL-01]
  - 判定依据：PASS — FR-002 要求字面量 `[[STR-006]]` 出现在 U0 入口声明并原文写入状态脊；自然语言声明被明确排除；`[[STR-006]]` 在 Shared Strings 中解析为 `fast-lane=opt-in`（requirements.md:167/288；contracts/fast-lane.md:7；data-model.md:27）。
- [x] CHK002 - Does the requirement anchor the admission decision to a reproducible artifact state (`tasks.md` present, before `checklist` dispatch) and a measured-value basis, rather than to stage-order inference or size impression? [Clarity, Req §FR-003; FL-02]
  - 判定依据：PASS — FR-003 与 FL-02 均把裁决点钉在“`tasks.md` 已产出、`checklist` 派发前”，并要求以制品实测值判定；缺失/不可解析输入由 Edge Cases 与 FL-03 判 `full-chain`（requirements.md:168；contracts/fast-lane.md:8；requirements.md:135）。
- [ ] CHK003 - Is the FR/task counting rule pinned by one unambiguous pattern, such that the requirement's “definition line” cannot be read to include a non-definition line? [Clarity, Req §FR-003(a); FL-03(a)]
  - 判定依据：FAIL — FL-03(a) 的 FR 模式是 `^- **FR-NNN**`（无尾随冒号），而 T010 与实测前提使用 `^- **FR-NNN**:`（含冒号）；契约文本的较宽模式会把形如 `- **FR-001** 说明` 的非定义行计入，两个“机械”计数口径不一致（contracts/fast-lane.md:10；tasks.md:115；tasks.md:319）。
  - 缺口：计数规则的单一权威模式未闭合；需求本身只说“FR 定义数”，未钉住定义行语法。
  - 建议处置：纠正类——把 FL-03(a) 与 T010/实测前提对齐为含冒号的 `^- **FR-NNN**:`，或在契约测试中钉住精确正则；数值区间 8–30 / 10–40 不变。
- [x] CHK004 - Are criteria (b), (c), and (d) each bounded by a conservative, machine-checkable scope (paths/contents) with a fail-closed outcome for undecidable inputs? [Measurability, Req §FR-003(b)-(d); FL-03]
  - 判定依据：PASS — (b) 以 `git diff --name-only <base>..HEAD` 为零判定；FL-03(c)/(d) 以路径/内容扫描 + “保守超集、命中即拒绝”判定；FR-003 与 FL-03 均规定任一判据无法判定即 `full-chain`。具体引擎前缀/依赖清单是 T010 的实现义务，且必须满足保守超集（requirements.md:168；contracts/fast-lane.md:11-13；tasks.md:115）。
- [ ] CHK005 - Is the `lines.manifest` line format (field order, separator, branch field) defined by a normative owner, rather than only by a fixture or quickstart example? [Clarity, Req §FR-003(e); FL-03(e)]
  - 判定依据：FAIL — FL-03(e) 与 E1 只定义路径、恰一行、分支相等，未定义行内字段顺序/分隔符；唯一的具体形态 `012-medium|012-medium` 出现在 T003/T008 与 quickstart，解析器成为唯一权威（contracts/fast-lane.md:14；data-model.md:29；tasks.md:92；quickstart.md:37）。
  - 缺口：准入证据的格式无法仅凭规范文本判定合法性；不同操作者可生成脚本不接受、但文本未禁止的形态。
  - 建议处置：纠正类——在 efficiency-model §1 / FL-03(e) 或 E1 中补一行“字段顺序 + 分隔符 + 分支字段”的行语法；不改 FR-003(e) 的判定语义。
- [x] CHK006 - Does the admission record field set include the decision, verbatim entry evidence, seven per-criterion verdicts with non-empty reproducible evidence, measured counts, and decision time, and is it required before checklist dispatch? [Completeness, Req §FR-004; FL-04]
  - 判定依据：PASS — FR-004 列出 `decision` / `entry_evidence` / 七项判据 `{id, verdict, evidence}` / 实测计数 / `decided_at`；E1 增加 `lines_manifest_ptr` 与可选 `reversion`；FL-04 要求派发前写入并携带 `[[STR-003]]`（requirements.md:169；data-model.md:24-32；contracts/fast-lane.md:18）。
- [x] CHK007 - Are the downstream publication of the skip decision and the single verbatim skip marker specified for both stage prompts and the wrap-up, so a missing checklist is not treated as a missing required gate? [Consistency, Req §FR-005; FL-05]
  - 判定依据：PASS — FR-005/FL-05 要求至少 implement 与 review 提示词携带跳过标记，收尾汇总携带 `checklist=skipped(fast-lane)`；`[[STR-003]]` 解析一致；E6 `fast_lane_marker` 与 E1 V-E1-4 呼应（requirements.md:170；contracts/fast-lane.md:19；data-model.md:157）。
- [x] CHK008 - Does reversion cover every criterion failure and newly discovered fact, and does it define the re-entry order (re-dispatch checklist; re-run analyze once if analyze already passed) and non-silent evidence? [Completeness, Req §FR-006; FL-06]
  - 判定依据：PASS — FR-006 与 FL-06 覆盖“任一判据失效或后续新事实”，要求补派 `checklist`、记录触发与证据，并规定 analyze 已通过时补派后重过 analyze 一次；Edge Cases 覆盖新增引擎/安全面/任务越界（requirements.md:171/136-137；contracts/fast-lane.md:20）。
- [x] CHK009 - Is the self-application exclusion stated and measurable, and does the feature's own measured size (43 FR / 52 tasks) independently place it outside the frozen medium band (8–30 FR / 10–40 tasks)? [Consistency, Req §FR-010; SC-013]
  - 判定依据：PASS — FR-010/SC-013/FL-10/DI-07 均要求 063 自身走完整链且快车道记录为 0；实测本规格 43 FR / 52 任务，均越出中型区间，故即使不看 FR-010，FR-003(a) 也会拒绝快车道（requirements.md:175/264；实测计数；requirements.md:27）。

## 2. 全量测试预算与定向测试

- [x] CHK010 - Are “full test run” (canonical runner, no path/test filters), the per-run-line budget scope, the exactly two slots, and their stage/order/executor all specified without overlap? [Clarity, Req §FR-011; TB-01/TB-02]
  - 判定依据：PASS — FR-011 定义全量 = 规范 runner 且不带路径/测试过滤器，预算以运行线为作用域、恰两个槽位（implement 起点与收口）；TB-01/TB-02 重复同一语义；E2 槽位表给出执行者与顺序（requirements.md:179；contracts/test-budget.md:7-8；data-model.md:70-75）。观测到的 6 次全量是带日期的需求方报告，plan 明确未复测、不据此宣称提速百分比（feature-ref.md:121）。
- [x] CHK011 - Are the baseline slot's pre-first-task anchor and name-level failed list, the prohibition on a second full run inside implement, and the closure slot's post-review/pre-merge name-level diff (`comm -13`) all stated? [Measurability, Req §FR-011/014/015; TB-03/TB-04; SC-004]
  - 判定依据：PASS — TB-03 要求 implement 首个任务前 `--names-out` 采集基线且 implement 内不得第二次全量；TB-04 要求收口 `--names-out` + `comm -13` 名称级差集，禁止仅比较计数；FR-014/FR-015/SC-004 一致；T002、DoD-7、GATE-8 把本特性自身运行钉在“仅 implement 一个槽位”（contracts/test-budget.md:9-10；tasks.md:80/25/41）。
- [ ] CHK012 - Does the targeted-set selection define a single fixed mapping procedure (command or algorithm) that two independent operators would reproduce, rather than only three categories plus a per-stage record of whatever command was used? [Measurability, Req §FR-013; TB-05]
  - 判定依据：FAIL — FR-013/TB-05 定义三条并集并要求“路径/名称映射命令”，但没有规定固定的选择命令或算法；efficiency-model §2.3 被 T020 指派去“发明”选择命令。不同阶段可以各自声称“确定性”却选出不同集合（requirements.md:181；contracts/test-budget.md:11；tasks.md:141）。
  - 缺口：“确定性规则”缺少可复现的执行定义；记录“我用了什么命令”不等同于跨运行可复现。
  - 建议处置：纠正类/设计补全——在 efficiency-model §2.3 定义固定选择命令或算法，并在 TB-05/契约测试中钉住；若确实允许阶段裁量，则应把“充分性判据”写成可复核的判定条件，而不是保留“确定性”的强措辞。
- [x] CHK013 - Are all evidence fields for full and targeted runs enumerated, and is missing evidence mapped to `unknown` rather than zero or a fabricated value? [Completeness, Req §FR-014/017; TB-06/TB-07]
  - 判定依据：PASS — FR-014 列出命令、选择依据、退出码、passed/failed、新增失败、比较基线；E2/E3 字段表逐项展开；FR-017 与 V-E2-3/V-E3-3 明确缺失即 `unknown`，不得记零或补造（requirements.md:182/185；data-model.md:52-68/85-105；contracts/test-budget.md:12-13）。
- [x] CHK014 - Are out-of-slot full runs and in-slot reruns mutually exclusive, with an exception requiring a reason and evidence pointer and appearing in the wrap-up summary? [Clarity, Req §FR-016; TB-08]
  - 判定依据：PASS — FR-016/TB-08 规定槽外全量只能是 `out-of-slot-exception`，必须带原因与证据并在收尾汇总列出；槽内重跑只能记为 `in-slot-rerun`（触发 + 证据），不另开槽；E2 槽位语义与 V-E2-1/V-E2-2 一致（requirements.md:184；contracts/test-budget.md:14；data-model.md:70-82）。
- [x] CHK015 - Is the environment-failure boundary (failure before collecting/executing any test) defined as non-slot-consuming, while any call that actually executed tests consumes a slot? [Clarity, Req §FR-018; TB-09]
  - 判定依据：PASS — FR-018/TB-09 规定收集/执行任何测试前失败（解释器/依赖缺失、收集前错误）记 `environment-failure` 且不消耗槽位；实际执行了测试的调用（含 0 tests collected 的选择失败）消耗槽位；V-E2-4 重复该边界（requirements.md:186；contracts/test-budget.md:15；data-model.md:81）。
- [ ] CHK016 - Does the test-evidence completeness metric explicitly treat a fast-lane-skipped `checklist` as not applicable, rather than as missing evidence? [Consistency, Req §SC-005 vs FR-001/FR-012]
  - 判定依据：FAIL — SC-005 要求“每个中间阶段与 review 的测试证据完整率为 100%”，FR-001 允许快车道完全跳过 `checklist`；E3 的 `status` 只有 `ran` / `not-run-docs-only` / `empty-selection-escalated` / `unknown`，没有“已授权的跳过/不适用”状态。收口审计无法区分“合法的快车道跳过”与“证据缺失”（requirements.md:166/180/256；data-model.md:92）。
  - 缺口：快车道与测试证据完整性指标之间缺少显式的 not-applicable 口径。
  - 建议处置：纠正类——在 E3 增加 `not-applicable-skipped-stage`（或等价）状态，或在 SC-005 的分母定义中排除“按准入记录授权的跳过阶段”；不要用 `unknown` 掩盖合法跳过。
- [x] CHK017 - Are the ledger's write point, per-line isolation, and closure audit defined, including a scan of stage logs for full-run commands not entered into the ledger? [Completeness, Req §FR-017; TB-07; V-E2-6]
  - 判定依据：PASS — FR-017 要求台账写入该线状态脊并由驱动在最终收口审计；TB-07 要求 `--logs-dir` 扫描阶段日志中的全量 runner 命令，日志命中但未入账即违规、日志缺失报 `unknown`；FR-011/E8 V-E8-2 要求多线独立台账与槽位（requirements.md:185；contracts/test-budget.md:13；data-model.md:83/200）。

## 3. Plan 阶段「只小修、不重审」约束

- [x] CHK018 - Are the constraint's activation point (plan U4 pass), the six plan-owned paths, and the recorded `activated_at`/`plan_commit` fields consistent across the requirement, data model, contract, and tasks? [Consistency, Req §FR-020/FR-024; PC-01]
  - 判定依据：PASS — FR-020/FR-024、PC-01、E4、T028 均把生效点钉在 plan U4 通过；六个路径 `plan.md`、`data-model.md`、`contracts/`、`quickstart.md`、`research.md`、`feature-ref.md` 逐字一致（requirements.md:191/195；contracts/plan-constraint.md:7；data-model.md:114-117）。
- [x] CHK019 - Are “minor fix” and “substantive change” defined by closed, non-overlapping criteria, and is classification required on the final diff rather than per-edit wording, including accumulated minor edits? [Clarity, Req §FR-020/FR-022; PC-02/PC-03; V-E5-2/V-E5-3]
  - 判定依据：PASS — FR-020 与 PC-02 把 minor 限定为错别字/措辞、断链/引用、格式、行级一致性；PC-03/E5 把 substantive 定义为改变范围、架构、数据模型、契约、FR/SC 或任务分解，并要求按最终 diff 判定；Edge Case 明确多处小修合并后按最终差异判定（requirements.md:155/191-193；contracts/plan-constraint.md:8-9；data-model.md:139-140）。
- [x] CHK020 - Is the `PLAN-EDIT:` declaration token required for every plan-owned touch before the completion sentinel, and is the full declaration format assigned to a single owner? [Clarity, Req §FR-020/FR-021; PC-04]
  - 判定依据：PASS — PC-04 规定任何 plan 制品改动必须在哨兵前的回传中包含 `PLAN-EDIT:` 声明行，并把完整格式的单一 owner 指到 `references/efficiency-model.md` §3.2；E5 `declaration_lines` 与 T028 呼应（contracts/plan-constraint.md:10；data-model.md:132；tasks.md:165）。需求正文使用“未声明”而未复写 token，属于契约层的设计细化，不构成冲突。
- [ ] CHK021 - Are the two post-gate routing branches deterministic, and is the “approved requirement scope / FR / SC baseline” used by branch (a) identified by an artifact and a commit or state? [Ambiguity, Req §FR-022; PC-06; E4]
  - 判定依据：FAIL — FR-022(a)/(b) 与 PC-06 都使用“已批准的需求范围/FR/SC 语义”，但没有定义“已批准”对应的制品与提交/状态；E4 记录了 `plan_commit` 作为约束基线，分流条款却没有把比较对象绑定到它。驱动无法稳定判定走 (a) 还是 (b)（requirements.md:193；contracts/plan-constraint.md:13-14；data-model.md:115）。
  - 缺口：“approved baseline”是分流的关键输入，但未被标识为可复核的制品/提交。
  - 建议处置：裁定类——明确把“已批准基线”绑定到 plan U4 时的 `requirements.md`（可复用 `plan_commit`），并要求分类记录该提交；若意图不是该基线，需要显式说明替代物。
- [x] CHK022 - Does the constraint preserve analyze's upstream repair route and re-gate obligation, so the constraint limits re-review cost but not whether a fix happens? [Consistency, Req §FR-023; PC-07]
  - 判定依据：PASS — FR-023/PC-07 明确约束只限制修复规模与重审开销，不取消 analyze 发现回到所属制品修复并重过该门的义务（requirements.md:194；contracts/plan-constraint.md:16）。
- [x] CHK023 - Is the exclusion of framework-command-internal hard enforcement recorded with its accepted design cost (manual invocations unconstrained; a future unsafe finding requires a separate feature)? [Completeness, Req §FR-025; PC-09; DI-09]
  - 判定依据：PASS — FR-025/PC-09/DI-09 把框架命令内部硬执行列为显式排除，记录“非驱动手工调用不受约束”的设计代价，并要求若后续证明不安全则另立特性（requirements.md:196；contracts/plan-constraint.md:18；contracts/delivery-and-invariants.md:15）。
- [x] CHK024 - Is the wrap-up report defined (constraint active or not, plan touches, classification, disposition) and is the active state restored from the state spine after a driver exit? [Completeness, Req §FR-024; PC-08; V-E4-2/V-E4-3]
  - 判定依据：PASS — FR-024/PC-08/E4 V-E4-3 要求收尾汇总报告约束状态、是否发生 plan 改动及分类/处置；E4 V-E4-2 与 Edge Case 要求重入后从状态脊恢复 `active` 与 `activated_at`（requirements.md:195/157；contracts/plan-constraint.md:17；data-model.md:121-122）。
- [x] CHK025 - Is “no silent re-review loop” made auditable for every substantive/undeclared change, with repeated loops bounded by the existing stall/retry discipline rather than an unstated cap? [Measurability, Req §FR-022; PC-06]
  - 判定依据：PASS — FR-022 要求每次实质/未声明改动先判门失败再按两分支处置；PC-06 明确不得因次数跳过分流，重复回环沿用既有 stall/retry 纪律（阶段超时 90 分钟 / 重试上限 2 次），不设人工次数上限（requirements.md:193；contracts/plan-constraint.md:15；skills/external/sdd-loop-driver/SKILL.md:85）。

## 4. 进度可见与驱动会话解耦

- [x] CHK026 - Is the default `--output-format stream-json` invocation specified together with a named raw-stream artifact and raw/stderr separation? [Completeness, Req §FR-026; PD-01]
  - 判定依据：PASS — FR-026 要求默认以 `[[STR-001]]` 调用并完整落盘 raw stream；PD-01 给出 `raw-<line>-<stage>.jsonl` 命名并要求 stderr 单独落 runner-log、不混入 raw；E7 登记 raw 路径与 `derivation`（requirements.md:200；contracts/progress-decoupling.md:7；data-model.md:170-175）。
- [x] CHK027 - Is the live-log derivation specified as incremental (not buffered to exit), with the terminal result text appended at EOF and the last non-empty line exactly the stage sentinel, while non-terminal events cannot satisfy the sentinel? [Clarity, Req §FR-027/FR-028; PD-02/PD-03]
  - 判定依据：PASS — FR-027/FR-028 与 PD-02/PD-03 要求每个有意义事件输出一行、不得缓冲到进程退出、EOF 时追加终止 `result` 文本、最后非空行恰为 `<STAGE>-DONE`，并明确非终止事件/JSON 信封/事件元数据不得满足判定（requirements.md:201-202；contracts/progress-decoupling.md:8-9；data-model.md:178）。
- [x] CHK028 - Are the derivation-failure paths ordered (one-shot `--finish` from raw, then buffered fallback, then INCOMPLETE), with the degradation marker and reason recorded and no fabricated completion or stage failure? [Completeness, Req §FR-030; PD-05; V-E7-2]
  - 判定依据：PASS — FR-030/PD-05/E7 V-E7-2 规定派生失败先 `--finish` 从终止 result 恢复，再考虑 buffered fallback；两者皆无则 `sentinel=0` 按 INCOMPLETE 处理，并记录 `[[STR-004]]` 与原因；降级不得产生伪完成或阶段失败（requirements.md:204；contracts/progress-decoupling.md:11；data-model.md:179）。
- [x] CHK029 - Does the watcher use stream progress only as visibility, with completion still requiring the sentinel plus U4 verification and timeout still produced only by the stage deadline? [Consistency, Req §FR-029; PD-04]
  - 判定依据：PASS — FR-029/PD-04 明确进度行数/增长不得单独产生 DONE 或 TIMEOUT；完成仍须哨兵 + U4 独立校验，超时只由 deadline 产生；既有判定顺序与退出码保持不变（requirements.md:203；contracts/progress-decoupling.md:10）。
- [x] CHK030 - Is `nohup` detachment the default in both local and remote topologies (stdin `/dev/null`, stdout/stderr redirected), and is a non-detached dispatch explicitly marked unprotected with a recorded risk? [Clarity, Req §FR-031; PD-06; V-E6-1]
  - 判定依据：PASS — FR-031/PD-06 要求本地与远端都以 `nohup`、stdin `/dev/null`、stdout/stderr 重定向脱离；远端保留 `ssh + su + nohup`；E6 V-E6-1 规定 `detached=no` 必须标记“未脱离”并记录风险、不得计为受保护运行（requirements.md:205；contracts/progress-decoupling.md:12；data-model.md:161）。
- [x] CHK031 - Is re-entry defined as an `--once` snapshot that verifies completed stages instead of re-dispatching them, and is this consistent with the four-piece evidence set? [Completeness, Req §FR-032; PD-07; V-E8-3]
  - 判定依据：PASS — FR-032/PD-07/E8 V-E8-3 要求新会话用 `--once` 快照接管、已完成阶段只核验不重派，并保持 pid/status/log/heartbeat 四件套与状态脊字段（requirements.md:206；contracts/progress-decoupling.md:13；data-model.md:201）。
- [x] CHK032 - Does the watcher self-test requirement name all four behaviors (non-terminal sentinel ignored, terminal result sentinel recognized, derivation failure not a false completion, detached runner survives driver exit), and is the raw-stream evidence face optional and verdict-neutral? [Coverage, Req §FR-033; PD-08]
  - 判定依据：PASS — FR-033/PD-08 逐项列出四个自测行为；`--raw-stream` 只输出成长/字节证据，不参与任何 verdict；既有平台假设的修正也被要求（requirements.md:207；contracts/progress-decoupling.md:14）。
- [ ] CHK033 - Is the 120-second silence threshold measured from a defined clock and compatible with the ban on fabricated progress lines when the CLI emits no events for longer than 120 seconds? [Conflict, Req §SC-007; Measurement Source]
  - 判定依据：FAIL — SC-007 同时要求“事件到达期间静默间隔不超过 120 秒”和“无事件时伪造进度行数为 0”；Measurement Source 只说“阈值 120 秒按事件到达区间测量”，没有定义计时的起点/终点。若事件间隔超过 120 秒，两条子句无法同时成立，除非伪造进度行（requirements.md:258/271；plan.md:21）。
  - 缺口：120 秒的测量对象（事件→派生行的延迟，还是相邻事件间隔）未定义；无事件时的适用性未说明。
  - 建议处置：裁定类——明确采用“事件到达→派生行出现”的延迟指标，或规定阈值仅在事件存在时计量；同步修改 Measurement Source 与派生测试的断言。
- [x] CHK034 - Are all four optimizations constrained to the orchestration layer, with any framework-command-internal change explicitly excluded or carrying a recorded design decision? [Consistency, Req §FR-019/FR-025/FR-043; TB-10; PC-09; DI-09]
  - 判定依据：PASS — FR-019/FR-025/FR-043、TB-10、PC-09、DI-09 都要求编排层实现；框架命令内部硬执行被列为显式排除；plan 的结论是四项均可在编排层实现（requirements.md:187/196/223；contracts/test-budget.md:16；contracts/delivery-and-invariants.md:15）。

## 5. 跨项一致性、安全不变量与验收证据

- [x] CHK035 - Are confirmation gates, independent verification, and stall handling preserved with no new auto-approval or bypass path? [Consistency, Req §FR-036/FR-037/FR-038; DI-01/DI-02/DI-03]
  - 判定依据：PASS — FR-036/037/038 与 DI-01/02/03 明确 push 仍为破坏性动作、独立校验三件套不变、卡死处置四要素与状态脊先写后动不变；未新增自动批准或绕过路径（requirements.md:213-215；contracts/delivery-and-invariants.md:7-9）。
- [ ] CHK036 - Is the “pre-change frozen baseline” used by SC-010 identified by a path/commit and measured by a procedure that actually captures stall-handling behavior? [Measurability, Req §SC-010; Measurement Source; feature-ref]
  - 判定依据：FAIL — SC-010 要求卡死场景的处置结果与“改动前基线”100% 一致，但 Measurement Source 只写“契约测试与场景夹具对照改动前冻结基线”；feature-ref 把它映射为 implement 起点的名称级测试基线，而名称级测试失败名单并不度量卡死处置行为。基线制品与比较程序均未定义（requirements.md:261/274；feature-ref.md:68）。
  - 缺口：SC-010 的 baseline 是行为基线，却用测试失败名称基线替代；证据链无法证明“100% 一致”。
  - 建议处置：裁定类——定义行为基线的制品（例如在指定提交上录制三类卡死场景的处置结果）与比较程序；或将 SC-010 限定为契约测试断言并如实标注其局限，不得把名称级测试基线冒充行为基线。
- [ ] CHK037 - Is SC-012's “镜像零漂移” scoped consistently with DI-05's “owned mirror pair zero NEW drift” and the plan's disclosed 65 pre-existing DIFFs in 11 other directories? [Conflict, Req §SC-012; DI-05]
  - 判定依据：FAIL — SC-012 写“镜像零漂移”未限定范围；DI-05 把判据限定为“本特性触碰的镜像对零 NEW drift”；plan.md:151 与 T048 明确保留其余 11 个目录的 65 个既有 DIFF。按 SC-012 字面执行全局 `sync-mirrors.py --check` 无法通过（requirements.md:263；contracts/delivery-and-invariants.md:11；plan.md:151；tasks.md:214）。
  - 缺口：验收标准与已记录的设计口径冲突；plan 已在文字上重新解释 SC，但未显式记录该重新解释。
  - 建议处置：裁定类/纠正类——把 SC-012 的镜像子句改为“本特性触碰的镜像对零 drift；相对冻结基线零 NEW drift”，或在规格中记录全局既有漂移的显式例外；不得静默按 plan 的窄口径执行而宣称满足 SC-012。
- [x] CHK038 - Do the six Shared Strings resolve to their declaring rows and verbatim values, and is the Related Feature binding traceable to the registry without creating a new Feature? [Traceability, Req §Shared Strings; Related Feature]
  - 判定依据：PASS — Shared Strings 表 6 行；`[[STR-001]]`…`[[STR-006]]` 的引用计数为 2/2/2/1/1/6，全部可解析；Related Feature 绑定 058，`features.md` 的 058 行为 `Implemented`，未新建 Feature（requirements.md:9-12/281-288；机器计数；`.specify/memory/features.md:66`）。
- [x] CHK039 - Do the explicit exclusions cover the obvious scope creep (large-feature fast lane, default fast lane, skipping analyze/review, auto-push/merge, new services/dependencies/APIs, budget overrun) and does the evidence plan distinguish automated tests, recorded trace, and driver-owned closure without overclaiming? [Coverage, Req §Out of Scope; SC Measurement Sources; plan Complexity Tracking]
  - 判定依据：PASS — Out of Scope 9 条覆盖上述范围蔓延；Measurement Sources 逐 SC 给出证据来源；plan Complexity Tracking 把 LLM 编排序列标为录制 trace、确定性组件标为自动测试；tasks DoD-8 禁止把录制 trace 冒充自动测试；feature-ref SC 表逐条标注证据类别（requirements.md:225-235/266-277；plan.md:163-165；tasks.md:26；feature-ref.md:57-71）。

## 不通过项汇总（供 analyze / implement 门处置）

| CHK | 质量问题 | 证据 | 建议处置 |
|-----|----------|------|----------|
| CHK003 | FR 计数模式在契约与任务/实测前提之间不一致（无冒号 vs 有冒号） | `contracts/fast-lane.md:10`；`tasks.md:115/319` | 纠正类：对齐为 `^- **FR-NNN**:` 或在契约测试钉住精确正则 |
| CHK005 | `lines.manifest` 行语法没有规范 owner，仅存在于夹具/quickstart 示例 | `contracts/fast-lane.md:14`；`data-model.md:29`；`tasks.md:92`；`quickstart.md:37` | 纠正类：在 efficiency-model §1 / FL-03(e) / E1 补行语法 |
| CHK012 | 定向测试集缺少固定选择命令/算法，“确定性”不可跨操作者复现 | `requirements.md:181`；`contracts/test-budget.md:11`；`tasks.md:141` | 纠正类/设计补全：在 efficiency-model §2.3 定义并钉住固定选择程序 |
| CHK016 | 快车道跳过 checklist 与 SC-005 的 100% 证据完整率缺少 not-applicable 口径 | `requirements.md:166/180/256`；`data-model.md:92` | 纠正类：增加 `not-applicable-skipped-stage` 或在 SC-005 分母中排除授权跳过 |
| CHK021 | FR-022 的“已批准需求基线”没有绑定到具体制品/提交，两分支分流不可判定 | `requirements.md:193`；`contracts/plan-constraint.md:13-14`；`data-model.md:115` | 裁定类：明确绑定 plan U4 的 requirements 基线（可复用 `plan_commit`） |
| CHK033 | SC-007 的 120 秒静默阈值与“禁止伪造进度行”在事件稀疏时冲突，计时对象未定义 | `requirements.md:258/271`；`plan.md:21` | 裁定类：定义 event→derived-line 延迟或明确阈值的适用条件 |
| CHK036 | SC-010 的“改动前基线”未定义，且被错误映射为名称级测试失败基线 | `requirements.md:261/274`；`feature-ref.md:68` | 裁定类：定义行为基线制品与比较程序，或显式限定 SC-010 的证据形态 |
| CHK037 | SC-012 的“镜像零漂移”与 DI-05 的“本对零 NEW drift”及既有 65 DIFF 冲突 | `requirements.md:263`；`contracts/delivery-and-invariants.md:11`；`plan.md:151`；`tasks.md:214` | 裁定类/纠正类：收窄 SC-012 措辞或记录全局既有漂移的显式例外 |

## 检查结论

- **Item count**: 39（CHK001–CHK039，连续无缺号）。
- **Result**: 31 pass / 8 not pass（CHK003、CHK005、CHK012、CHK016、CHK021、CHK033、CHK036、CHK037）。
- **Traceability**: 39/39 项携带 `[Req §…]`、`[Gap]`、`[Ambiguity]` 或 `[Conflict]` 引用（100%，高于 ≥80% 的最低要求）。
- **Scope**: 覆盖四项优化的准入、预算、plan 约束、进度/解耦、跨项不变量与验收证据；未改写既有 `checklists/requirements.md`（仍为 16/16），未修改 `requirements.md` / `plan.md` / `tasks.md` / `contracts/` / `data-model.md`。
- **Not-pass handling**: 8 项均为记录项，未通过降低判据或勾选放行；供 `/speckit.analyze` 与 `/speckit.implement` 门按 § 不通过项汇总处置。其中 CHK003/CHK005/CHK012/CHK016 属于可对齐的纠正类；CHK021/CHK033/CHK036/CHK037 需要明确测量/基线口径（裁定类）。
- **Validation**: 见本阶段回传；item 计数、ID 连续性、勾选数与 traceability 由脚本复算，不手抄。

## Notes

- 复选清单项时使用 `[x]`；未通过项保留 `[ ]` 并就地记录缺口，不要为了全绿而删除或放宽判据。
- `plan.md` / `tasks.md` / `contracts/` 只作为缺口发现上下文；本清单不评价其实现质量。
- 本阶段测试证据：`status=not-run-docs-only`，改动集仅 `checklists/efficiency.md`，无可执行/测试面改动。
- 同作者门未触发：本清单由新鲜上下文的 checklist 阶段子代理生成，前序 requirements/plan/tasks 由其他阶段生成。
- 2026-10-20 tasks-repair-2：063 的临时 CLI-profile 范围已按 Feature 064 的 `notes/063-overlap-adjudication.md` 迁出；本清单的 39 项判定对象仍为四项效率优化，不受影响，未新增或删除检查项。当前计数为 43 FR / 13 SC / 8 Shared Strings。
