# Concurrency, Isolation & Lifecycle Requirements Quality Checklist: 064

**Purpose**: 在 tasks 之后、analyze/implement 之前，对 Feature 064 的需求文本做一次"需求写作的单元测试"——检查归属零串台、工作区/集成队列确定性、主/子会话生命周期三分支、CLI 档案/probe/feedback、058/061 非回归与 063 单 owner 收口是否可判定、完整、一致，而不是验证实现行为。
**Created**: 2026-10-20
**Feature (Requirement Scope)**: Feature 064 — Subagent 并发归属、CLI 能力档案与生命周期解耦
**Requirements (What)**: [requirements.md](../requirements.md)
**Specifications (How, context only)**: [plan.md](../plan.md) · [tasks.md](../tasks.md) · [data-model.md](../data-model.md) · [contracts/](../contracts/) · [feature-ref.md](../feature-ref.md)
**Distinct from**: `checklists/requirements.md`（plan 前的通用 16 项完整性门）。本文件是该门之后的独立并发/生命周期质量门，不覆盖、不替代既有清单。

**Note**: 本清单只评判**需求与需求承载文本**的质量；引用 plan/tasks/contracts/data-model 仅用于发现需求缺口、歧义、冲突与追溯断点，不对其实现行为打分。

## Verdict Semantics

- `[x]` = **PASS**：按当前文本可判定且证据一致；行下给出证据指针。
- `[ ]` = **FAIL**：存在缺口、歧义或冲突；行下给出证据与移交建议，供 analyze/implement 门处置。
- 每个条目形如"是否……？"并带质量维度与追溯引用。判定只读文本与源码 owner，不运行产品。
- 本清单为逐项判定型：`40` 项、`16` PASS、`24` FAIL。FAIL 不等于执行异常，而是待 analyze/implement 处置的需求质量发现。

**Same-author detection**: 同一作者条件成立（requirements→clarify→plan→tasks 为同一编排代理连续产出）。按 `.specify/shared/workflow/objective-analysis-gate.md`，检测已委托给三个新鲜上下文只读子代理，作用域互不重叠：
- Detector A：requirements.md + data-model.md + feature-ref.md；
- Detector B：contracts/ 六文件 + plan.md + requirements.md（仅引用 FR/SC 正文）；
- Detector C：brief.md + requirements.md + tasks.md + quickstart.md + notes/063-overlap-adjudication.md + 既有 checklists/requirements.md。

验证轮由编排代理对每条引用重新打开到 file:line 核对，不复用检测结论；重复项合并；拒绝/降级 3 条候选（FR-063 豁免清单被重判为 PASS；063 保留 stream-json/nohup 由"双 owner"降为"边界未闭合"；S6 场景正文不作为需求质量条目）。降级率约为 3/27；其余 24 条 FAIL 均有行级证据。

---

## A. 线路身份、Registry、信封与入口（FR-001…FR-017）

- [x] CHK001 — 环境级 Registry 的位置、`SPECIFY_LINE_REGISTRY_DIR` 覆盖、worktree 之外的可发现性、每线原子写、同线排他锁、U0.5/U6 注册注销、失败上送与 stale 显式清理，是否由单一 owner 完整且无冲突地定义？ [Completeness, Req §FR-001…FR-003, FR-007]
  - **Verdict**: PASS — 位置/覆盖/原子写/锁/时点/失败/stale 清理均有对应条款，且 SC-009 给出并发验收。
  - **Evidence**: `requirements.md:190-196`；`contracts/line-registry.md:10-20`；`requirements.md:306`（SC-009）。

- [ ] CHK002 — Registry/Envelope/Profile 的实体字段表是否枚举了 FR 与校验规则要求的全部字段与类型（含 `run_history`、`profile_version`、`at` 的单一时间类型、并发上限使用情况），且无悬空引用？ [Completeness, Req §FR-004, FR-005, FR-029, FR-037]
  - **Verdict**: FAIL — `run_history` 只出现在 V-LR-3，不在 E1 字段表；`profile_version` 只在 E10/CLP-08 使用，E9 未定义；`at` 被写成 epoch seconds，与文件开头 ISO-8601 约定冲突；`resources` 缺 FR-029 要求的并发上限使用情况；E1 存储说明引用未命名的 "R1"。
  - **Evidence**: `data-model.md:51`（run_history）；`data-model.md:15-45`（E1 表，无该字段）；`data-model.md:305` + `contracts/cli-profiles.md:20`（profile_version）；`data-model.md:93` vs `data-model.md:7`（时间类型）；`data-model.md:41` vs `requirements.md:221`（cap usage）；`data-model.md:13`（R1）。
  - **Gate**: 纠正类——analyze 统一实体字段表；若涉及 `qodercli_pid` → `cli_pid` 泛化，保留 D-02 的追溯说明。

- [x] CHK003 — 信封字段与各载体（prompt/status/log/heartbeat/哨兵承载记录/watcher/monitor）是否定义完整，并明确保证不改写日志正文、不位移哨兵最后一行？ [Clarity, Req §FR-008, FR-009]
  - **Verdict**: PASS — EN-01/02/03 给出字段、旁路命名与哨兵保全；V-EN-1 明确日志正文不含信封。
  - **Evidence**: `contracts/line-envelope-and-ingress.md:10-12`；`data-model.md:114`（V-EN-1）。

- [ ] CHK004 — 归属分类的每个取值（`own/foreign/stale-run/unattributed/legacy`）是否都有唯一的消费规则，尤其 `legacy` 是否被限制为不得在活动线 >1 时绕过归属过滤？ [Consistency, Req §FR-014, FR-015, FR-017]
  - **Verdict**: FAIL — 分类是五值封闭集，但 V-EN-3 写"其余三类"（与五值不符）；`legacy` 被定义为"无归属过滤"且可被消费，却不在 FR-014/015/017 中；EN-16 又依赖 legacy 做 058 兼容。若多线环境使用 legacy 调用，零串台保证可被绕过。
  - **Evidence**: `data-model.md:115`（五值），`data-model.md:121`（"其余三类"）；`contracts/line-envelope-and-ingress.md:13-14`（legacy/no-filter），`:28`（EN-16 兼容）；`requirements.md:203-206`。
  - **Gate**: 裁定类——要么禁止多活动线时使用 legacy，要么把 legacy 限定为单线/058 兼容并补一条消费规则。

- [x] CHK005 — 入口决策表是否对 >1 / 1 / 0 条活动线、显式标识、唯一匹配与"回答后仍不唯一"的所有组合给出单一结果？ [Decidability, Req §FR-010, FR-011]
  - **Verdict**: PASS — 活动线定义、标识形态、恰好一次澄清、ambiguous-stop、单线/零线均有单一出口。
  - **Evidence**: `requirements.md:199-200`；`contracts/line-envelope-and-ingress.md:20-24`；`contracts/line-registry.md:36`（resolve-message 决策封闭集）。

- [ ] CHK006 — "澄清不阻塞其他线路"是否有可测量的验收场景或 SC，而不仅是 FR-012 的散文？ [Coverage/Measurability, Req §FR-012]
  - **Verdict**: FAIL — FR-012 与 Edge Case 都要求其他 line 继续推进，但 10 条 SC 无一测量"其他线路未被暂停"；US1 验收场景只查澄清次数与路由；tasks 的 T008/T016 也未具名覆盖。
  - **Evidence**: `requirements.md:201`（FR-012）；`requirements.md:157`（Edge Case）；`requirements.md:298-307`（SC 集合）；`tasks.md:131`（T008），`tasks.md:142`（T016）。
  - **Gate**: 裁定类——为 FR-012 增加验收场景/SC，或明确该保证只约束消息路由、不承诺可观测的并发进度。

- [ ] CHK007 — PID 身份校验是否将 start ticks、cwd 与 branch 三者都定义为必查，并显式批准平台豁免（macOS cwd `unsupported`），而不是用"可用的 cwd/branch 证据"静默降级？ [Clarity/Completeness, Req §FR-013, FR-050]
  - **Verdict**: FAIL — 权威 brief 要求校验 start ticks、cwd 与 branch 三项；FR-013 改为"可用的 cwd/branch 证据"；LC-07 批准 macOS cwd `unsupported` 为唯一豁免，E6 又增加 `skipped`，但 requirements 的 Assumptions 未记录该降级，`skipped` 也未获 LC-07/V-ID-1 授权。
  - **Evidence**: `/tmp/sdd-064/brief.md:51`；`requirements.md:202`（"可用的"）；`contracts/lifecycle-detach-reattach.md:19`（LC-07）；`data-model.md:205-206`（cwd_check 枚举），`data-model.md:214`（V-ID-1）。
  - **Gate**: 裁定类——在 requirements 中批准平台豁免与 `skipped` 语义，或恢复 cwd/branch 必查。

- [ ] CHK008 — Registry 状态模型是否在每个同步点单值化，并与状态脊一致，尤其"全部阶段完成但尚未合并"是 `completed` 还是 `active + merge_ready`？ [Consistency, Req §FR-006, FR-025]
  - **Verdict**: FAIL — 同一 data-model 给出两条互斥迁移：`active --all stages done--> completed` 与 `active --u4 all stages done & merge ready--> active + merge_ready=true`；V-LR-9 又把 `active` 绑定到脊 `running/retrying`、把 `completed/closed` 绑定到 `done`，并允许从 `active` 直接 `closed`。FR-006 只列六个同步点，未规定每点写入哪个状态值。
  - **Evidence**: `data-model.md:68` vs `data-model.md:73`；`data-model.md:57`（V-LR-9）；`data-model.md:70`（active→closed）；`requirements.md:195`（FR-006 六时点）。
  - **Gate**: 裁定类——选定唯一的 pre-merge 状态，并补 U0.5/U2/U3/U4/U5/U6 的状态转移表。

- [ ] CHK009 — 单线兼容（LR-13/NG-07）与"注册失败即停止"（LR-02/LR-11）是否互相兼容，是否明确把注册失败停止排除在"既有 U0–U6 行为不变"之外？ [Consistency, Req §FR-017, FR-068, FR-002]
  - **Verdict**: FAIL — LR-02/LR-11 要求注册失败停止该 line 且不得回退；LR-13/NG-07 又承诺单线"不得因归属机制改变 U0–U6 既有行为"，未给新失败路径留出例外。Edge Case 已批准该停止，文本需要同步。
  - **Evidence**: `contracts/line-registry.md:11`（LR-02），`:20`（LR-11），`:22`（LR-13）；`contracts/non-regression-and-tests.md:15`（NG-07）；`requirements.md:177`（Edge Case）。
  - **Gate**: 纠正类——在 LR-13/NG-07 中显式 carve out 注册失败的停止语义。

- [x] CHK010 — 双线验收是否完整列出 FR-016 的四项断言（零串台、恰好一次澄清、foreign 不改变状态、PID 复用/死亡不产生假完成）？ [Completeness, Req §FR-016]
  - **Verdict**: PASS — 四项均在 FR-016 与 EN-15 中；US1 的验收场景逐项对应。
  - **Evidence**: `requirements.md:205`；`contracts/line-envelope-and-ingress.md:27`（EN-15）；`requirements.md:70-75`（US1 AS1–AS4）。

## B. 工作区隔离与确定性集成（FR-018…FR-032）

- [x] CHK011 — 写线 worktree/分支/base_sha、路径归一化、写-写重叠、`created_at` FIFO + `line_id` tie-break、持线者死亡不自动释放、只读/禁止路径，是否都定义为可判定规则？ [Completeness/Decidability, Req §FR-018…FR-021]
  - **Verdict**: PASS — WI-01…WI-08 与 V-OM-1…6 给出路径归一化、重叠、串行化与死亡保留规则。
  - **Evidence**: `requirements.md:210-213`；`contracts/workspace-isolation.md:10-20`；`data-model.md:143-148`。

- [ ] CHK012 — waiting 的晋级条件是否严格等于 FR-021 授权的"持线者完成 U6 合并或显式放弃（或路径拆分）"，没有把"holder closed"当成自动释放？ [Consistency, Req §FR-021]
  - **Verdict**: FAIL — data-model 的迁移写 `waiting --promote--> active (holder closed / explicit release / disjoint)`；FR-021 只授权"U6 合并或显式放弃"，并明确持线者死亡不得自动释放；WI-06 与 FR-021 一致，data-model 是离群副本。
  - **Evidence**: `data-model.md:66`；`requirements.md:213`；`contracts/workspace-isolation.md:18`（WI-06）。
  - **Gate**: 纠正类——把 "holder closed" 限定为"显式放弃后的 closed"，或删除该触发条件。

- [ ] CHK013 — line 本地运行时记录集合是否闭合且无歧义，并与集成归档的单一枚举一致（FR-022 的"等"是否已收敛）？ [Clarity/Completeness, Req §FR-022, FR-023]
  - **Verdict**: FAIL — FR-022 用"feedback/session/exec-quant 等"开放列举；E8 把运行时记录集合封闭为四条路径并声明"唯一枚举"，但仓库还存在 `.specify/memory/evidence/`、`.specify/history/`、`.specify/memory/trigger/` 等运行时存储；两者至少有一处需要收口。
  - **Evidence**: `requirements.md:214`（FR-022）；`data-model.md:250-257`（Runtime-record path set），`:264`（V-AR-4）；`contracts/workspace-isolation.md:24`（WI-09）；本工作树 `.specify/memory/evidence/`、`.specify/history/`、`.specify/memory/trigger/` 均存在。
  - **Gate**: 裁定类——在 requirements 层闭合集合，或明确排除其他存储并给出理由。

- [ ] CHK014 — FR-024（镜像/命令副本每批一次）与 FR-026（逐线"更新 Registry/镜像"）的矛盾是否已在 requirement 文本中消除，而不只是由 WI-14 单点改写？ [Consistency/Conflict, Req §FR-024, FR-026]
  - **Verdict**: FAIL — FR-024 说 MUST 只在集成过程执行一次、MUST NOT 每 line 执行；FR-026 的逐线步骤仍写"更新 Registry/镜像"；US2 AS4 重复同一措辞。WI-14 已把它改写为"每线 Registry + 批次镜像"，但 requirements 正文仍自相矛盾。
  - **Evidence**: `requirements.md:216`（FR-024） vs `requirements.md:218`（FR-026）；`requirements.md:92`（US2 AS4）；`contracts/workspace-isolation.md:29`（WI-14，唯一已修正副本）。
  - **Gate**: 裁定类——修改 FR-026 与 US2 AS4，使之与 FR-024 一致（需求文本裁定，非仅设计注记）。

- [x] CHK015 — 集成队列是否在 FIFO、同时间戳 tie-break、显式拓扑依赖、同层排序与环拒绝上给出确定性定义，并声明重放逐字一致？ [Decidability, Req §FR-025]
  - **Verdict**: PASS — FR-025、WI-13 与 E7 的 V-IQ-1/2 给出完整排序与环拒绝规则。
  - **Evidence**: `requirements.md:217`；`contracts/workspace-isolation.md:28`；`data-model.md:230-231`。

- [x] CHK016 — 逐线集成步骤、失败保留、no-force-push 与清理条件是否完整且不冲突（除 CHK014 的镜像基数冲突外）？ [Completeness, Req §FR-026, FR-027, FR-032]
  - **Verdict**: PASS — 逐线步骤、失败保留、禁止 force push、无 `--force` 清理与未提交工作保留均有对应条款。
  - **Evidence**: `requirements.md:218-219, 224`；`contracts/workspace-isolation.md:29-31`；`contracts/non-regression-and-tests.md:10, 12`。

- [ ] CHK017 — 端口块、缓存/临时目录、并发上限与"并发上限使用情况"的报告字段是否量化到可验收的形态？ [Measurability, Req §FR-028, FR-029]
  - **Verdict**: FAIL — FR-028 只要求"可配置并在派发前检查"；FR-029 要求报告"并发上限使用情况"但未定义字段或口径；E11 给出 cap 缺省 4，E1 的 `resources` 却只有 `{ports, cache_dir, tmp_dir}`，没有 cap usage。
  - **Evidence**: `requirements.md:220-221`；`data-model.md:320`（E11）；`data-model.md:41`（E1 resources）。
  - **Gate**: 纠正类——在资源报告中加入 `active_count`/`cap` 或等价字段，并声明报告时点。

- [ ] CHK018 — 双写线验收条款 WI-21 是否携带 FR-031 的全部五项断言，特别是"运行时/镜像只集成一次"？ [Completeness, Req §FR-031]
  - **Verdict**: FAIL — FR-031 列出五项，WI-21 只列四项，缺"运行时/镜像只集成一次"；T022 已覆盖该项，但契约条款正文是断的。
  - **Evidence**: `requirements.md:223`（FR-031 五项）；`contracts/workspace-isolation.md:39`（WI-21 四项）；`tasks.md:161`（T022 含 runtime/mirror once）。
  - **Gate**: 纠正类——把第五项补入 WI-21，或在 WI-21 中显式引用 FR-031 而不复述。

## C. CLI 能力档案、Probe 与 Feedback（FR-033…FR-045）

- [x] CHK019 — 五份档案、八个维度、单一 schema/知识落点（`references/cli/index.md`）、镜像与 docs 入口是否完整规定？ [Completeness, Req §FR-033, FR-034, FR-042, FR-045]
  - **Verdict**: PASS — 档案集合、八维、单一落点、镜像与 docs 入口均有条款；Probe 细节另见 CHK024。
  - **Evidence**: `requirements.md:228-229, 237, 240`；`contracts/cli-profiles.md:10-16, 31`（CLP-01/02/06/07/16）。

- [ ] CHK020 — "无档案不得派发"是否可判定，且骨架建立后"按安全缺省派发"中的"安全缺省"是否定义并服从 061 的 `CAPABILITY_MATRIX`？ [Ambiguity, Req §FR-033]
  - **Verdict**: FAIL — FR-033 写"MUST NOT 被派发（先建骨架并记录缺口）"，CLP-01 进一步写"再按安全缺省派发"，但"安全缺省"没有定义，也未说明它与 061 矩阵的派发资格如何合成。
  - **Evidence**: `requirements.md:228`；`contracts/cli-profiles.md:10`；`contracts/cli-profiles.md:30`（CLP-15 矩阵权威）。
  - **Gate**: 裁定类——定义"安全缺省"，或明确骨架建立后仍须由矩阵判定资格。

- [x] CHK021 — known/unknown、版本适用性、证据指针与 qodercli 六项初始事实是否完整，且 0/负值超时语义明确记为 unknown 而非猜测？ [Clarity/Measurability, Req §FR-035, FR-036]
  - **Verdict**: PASS — FR-035/036 与 CLP-03/04 覆盖八维、provenance、qodercli 缓冲/超时/600,000 ms/stream-json/日志/detach，0/负值记为 unknown。
  - **Evidence**: `requirements.md:230-231`；`contracts/cli-profiles.md:12-14`。

- [ ] CHK022 — U2/U4/U5 的观测面是否完整（含缓冲行为与"同一次派发多个独立事件各一条反馈"），且写序与 Provenance 的 `feedback_id` 时点自洽？ [Consistency, Req §FR-037…FR-039]
  - **Verdict**: FAIL — CLP-03 要求 Provenance 表含"反馈 id"，CLP-10 却规定先更新 provenance、后记录反馈，写入时 id 尚不存在；CLP-09 的 U4 比对项漏掉 FR-038 的"缓冲"；CLP-10 未承接 FR-039 的"同一次派发内多个独立观测事件各产生一条"。
  - **Evidence**: `contracts/cli-profiles.md:12`（CLP-03），`:21`（CLP-09 无 buffering），`:22`（CLP-10 顺序与单事件）；`requirements.md:233-234`（FR-038/039）。
  - **Gate**: 纠正类——把 `feedback_id` 定义为事后回填或调整写序；补 buffering 与多事件规则。

- [ ] CHK023 — FR-040 的"经既有 feedback 机制记录"是否允许 standalone（无 `.specify/`）跳过引擎调用，若允许该例外是否已在 requirements 中批准？ [Consistency/Assumption, Req §FR-040]
  - **Verdict**: FAIL — FR-040 是无条件 MUST；CLP-11 增加"宿主无 `.specify/` 时按 runtime-mode gate 跳过引擎调用"的例外，requirements 没有对应 Assumption 或例外条款。
  - **Evidence**: `requirements.md:235`（FR-040）；`contracts/cli-profiles.md:23`（CLP-11 standalone 分支）。
  - **Gate**: 裁定类——在 requirements 中批准 standalone 例外，或删除该分支。

- [ ] CHK024 — Probe Object 的 class/unit 落点是否对 external skill 可注册且格式合法（external 要求 `ext-` id 与 `custom:<owner>/<name>` unit）？ [Decidability, Req §FR-040]
  - **Verdict**: FAIL — FR-040 优先 `skill-wrapup` + `skill:sdd-loop-driver`，兜底 `custom:`；但该 skill 的 frontmatter 为 `classification: external`，probe 引擎规定 external Object id 必须以 `ext-` 开头、unit 必须匹配 `^custom:[a-z0-9._/-]+$`。计划中的 `skill-sdd-loop-driver-cli-profile` 无 `ext-` 前缀，research 中的 `custom:skill:sdd-loop-driver` 也不匹配该正则。
  - **Evidence**: `requirements.md:235`；`contracts/cli-profiles.md:24`（CLP-12）；`skills/external/sdd-loop-driver/SKILL.md:5`（classification: external）；`.specify/scripts/python/probe-utils.py:132`（custom unit 正则），`:273`（external id `ext-`），`:285`（external unit 规则）。
  - **Gate**: 裁定类——选定合法 class/unit/id，或明确该 Object 以 internal-class 注册的依据；两种落点都必须能通过 `probes --validate`。

- [x] CHK025 — 档案更新是否明确不改变哨兵、watcher 判定/退出码、确认门、deadline 与测试预算，并保持 061 矩阵为唯一派发资格 owner？ [Consistency, Req §FR-041, FR-043]
  - **Verdict**: PASS — FR-041/043 与 CLP-13/15 明确行为不变与矩阵权威；EN-06/NG-04 保持 058 语义。
  - **Evidence**: `requirements.md:236, 238`；`contracts/cli-profiles.md:25, 30`；`contracts/line-envelope-and-ingress.md:15`；`contracts/non-regression-and-tests.md:12`。

- [ ] CHK026 — 063 收口是否在"保留吞吐策略"与"064 拥有档案/输出形态事实"之间划出单一 owner，且已消除对已删除的 CP-07/CP-08 的活引用与合并前双份契约风险？ [Consistency/Dependencies, Req §FR-044]
  - **Verdict**: FAIL — 裁决记录保留 063 的 stream-json 默认与 E6/E8 字段；CLP-08 又规定 U2 依档案选择输出模式，两者的事实/策略边界未写明。CLP-11/13 仍以 CP-07/CP-08 为活引用，而 CLP-17 要求 063 合并时删除它们；T063 只验证 064 树，不验证 `bcf27c77` 仍持有 provisional 契约。
  - **Evidence**: `notes/063-overlap-adjudication.md:21-23`；`contracts/cli-profiles.md:20`（CLP-08），`:23, 25`（CP-07/08 引用），`:32`（CLP-17 删除）；`tasks.md:237`（T063 仅查 064 树）。
  - **Gate**: 裁定类——写明"档案记录事实、063 决定吞吐默认"的边界，并把 CP-07/08 引用改为指向 064 条款；为合并时的删除建立可验证 owner。

## D. 主/子会话生命周期解耦与重接线（FR-046…FR-059）

- [x] CHK027 — 脱离式执行是否在本地与远端同构地规定独立进程组/会话、stdio 脱离、信号不传播、最小远端字段与驱动侧 Registry？ [Completeness, Req §FR-046, FR-047, FR-058, FR-065]
  - **Verdict**: PASS — LC-01/02/17 与 LR-08 覆盖本地/远端同构、`ssh + su + nohup`、最小远端字段与驱动侧 Registry。
  - **Evidence**: `requirements.md:244-245, 256, 266`；`contracts/lifecycle-detach-reattach.md:10-12, 35`；`contracts/line-registry.md:17`。

- [x] CHK028 — 四件套、CLI 子进程 PID、`(line_id, stage)` 原子 reservation 与第二启动者附着/拒绝是否完整规定？ [Completeness, Req §FR-048, FR-056]
  - **Verdict**: PASS — LC-03/04/15 与 V-SR-1/2/3 给出四件套、CLI 子进程、`O_CREAT|O_EXCL`、attach/refuse 与证据破除。
  - **Evidence**: `requirements.md:246, 254`；`contracts/lifecycle-detach-reattach.md:12-13, 33`；`data-model.md:188-192`。

- [ ] CHK029 — lease 获取、身份校验与 `--once` 快照的顺序是否在 FR-030/FR-049/FR-050 之间单值（"重入先快照"与"校验后快照"是否冲突）？ [Consistency, Req §FR-030, FR-049, FR-050]
  - **Verdict**: FAIL — FR-030 说"重入 MUST 先做一次 `--once` 快照"；FR-050 说取得 lease 并校验身份后"再先做一次 `--once` 快照"；LC-08/V-ID-4 解析为 lease→identity→snapshot，但需求正文仍有两个"先"。
  - **Evidence**: `requirements.md:222`（FR-030），`requirements.md:248`（FR-050）；`contracts/lifecycle-detach-reattach.md:20`（LC-08）；`data-model.md:217`（V-ID-4）。
  - **Gate**: 纠正类——把 FR-030 的"先"限定为"在任何重派/去向决定之前"，并引用 lease/identity 顺序。

- [ ] CHK030 — lease 的"活会话"与续租节奏是否量化，避免活着但心跳过期的会话被合法夺取？ [Measurability, Req §FR-049]
  - **Verdict**: FAIL — FR-049 只要求活会话不得被夺取；LC-05 只说 `lease-renew` "周期刷新"，没有周期；V-DL-2 把存活定义为 `now < heartbeat_at + ttl`（缺省 600），却没有 requirement 规定续租频率。活会话停止续租后可在证据上被视为过期。
  - **Evidence**: `requirements.md:247`；`contracts/lifecycle-detach-reattach.md:17`（LC-05）；`data-model.md:163`（ttl），`data-model.md:168`（V-DL-2）。
  - **Gate**: 裁定类——量化续租周期/TTL 关系，并说明"活会话"的判据。

- [ ] CHK031 — reattach 的全部结局（running/done/dead 与 orphan/stale/remote-unreachable）是否互斥、穷尽并各有一个明确的 Registry 状态与处置？ [Coverage/Consistency, Req §FR-051…FR-055]
  - **Verdict**: FAIL — running/done/dead 三分支清楚；但 E6 `branch_hint` 有五值；data-model 同时写 identity fail → `stale` 与 U5 → `stalled`，无优先级；V-ID-5 只把 dead/mismatch 送 U5；FR-054 把"Registry 缺失"列为 orphan，却只允许用已登记 PID/线自有证据识别，缺少无 Registry 时的证据入口。
  - **Evidence**: `requirements.md:249-253`；`data-model.md:210`（五值 branch_hint），`:67, 71`（stale/stalled），`:218`（V-ID-5）；`contracts/lifecycle-detach-reattach.md:27, 29`（LC-12/14）。
  - **Gate**: 裁定类——给出五值 → Registry 状态 → 处置的唯一映射，并定义 orphan 的可判定证据集。

- [x] CHK032 — 重复启动防护与 U6 收尾（注销、reservation 释放、证据归档、worktree 保留、无 active 残留）是否完整规定？ [Completeness, Req §FR-056, FR-057]
  - **Verdict**: PASS — FR-056/057、LC-15/16、V-SR-4 与 SC-010 覆盖重复启动、释放、归档、保留与残留检查。
  - **Evidence**: `requirements.md:254-255, 307`；`contracts/lifecycle-detach-reattach.md:33-34`；`data-model.md:191`。

## E. 非回归与边界（FR-060…FR-068）

- [x] CHK033 — no-push、不删未提交工作、迁移不静默丢失是否在所有边界与清理条款中一致陈述？ [Consistency, Req §FR-060…FR-062]
  - **Verdict**: PASS — 三条红线在 FR、WI、LC、NG 中一致；清理均要求合并成功或显式动作。
  - **Evidence**: `requirements.md:261-263`；`contracts/non-regression-and-tests.md:9-11`；`contracts/workspace-isolation.md:30-31`；`contracts/lifecycle-detach-reattach.md:27, 34`。

- [x] CHK034 — 058 的哨兵/判定/退出码与 061 的 `CAPABILITY_MATRIX` 是否以引用方式保留，未被本特性重新定义？ [Consistency, Req §FR-043, FR-063, FR-066]
  - **Verdict**: PASS — EN-06/NG-04 明确判定状态机与退出码零改动；CLP-15 明确矩阵是唯一资格 owner。FR-063 的豁免清单只点名 FR-009/FR-041，表述可再精确，但边界由 EN-06 承载，不构成重新定义。
  - **Evidence**: `requirements.md:264, 267`；`contracts/line-envelope-and-ingress.md:15`；`contracts/non-regression-and-tests.md:12-13`；`contracts/cli-profiles.md:30`。

- [x] CHK035 — 无常驻服务/外部服务/新运行时依赖与跨机器排除/最小远端字段是否有可验收的边界？ [Measurability, Req §FR-064, FR-065]
  - **Verdict**: PASS — FR-064/065 明确 stdlib/bash 复用与跨机器排除；T068 的 stdlib-only 守卫提供可执行证据。FR-065 的追溯断点另见 CHK040。
  - **Evidence**: `requirements.md:265-266`；`contracts/non-regression-and-tests.md:13`；`tasks.md:255`（T068）。

## F. 成功标准、度量与追溯（SC-001…SC-010）

- [ ] CHK036 — SC-009 的 N 是否量化，且并发读保证是否在"写入进行中"而非仅写入后测量？ [Measurability, SC-009, Req §FR-003]
  - **Verdict**: FAIL — SC-009 只写"N 条线路"，N 未定义；度量来源写的是 N 次写入后解析/去重，没有在写入过程中验证"读取方不见半写"，而后者是 FR-003 的核心保证。
  - **Evidence**: `requirements.md:306`（SC-009）；`requirements.md:313`（Source）；`requirements.md:192`（FR-003）。
  - **Gate**: 纠正类——给 N 一个值或范围，并加入写-读交错的断言。

- [ ] CHK037 — SC-004 的"合并结果在重放中差异为 0"是否定义了比较层级（队列顺序、树哈希或提交 SHA），避免不可判定的"结果"？ [Clarity, SC-004]
  - **Verdict**: FAIL — SC-004 与 FR-025 都要求"相同结果"，但没有说明比较队列日志、合并后的树哈希，还是提交 SHA；不同层级对"相同"的判定不同。
  - **Evidence**: `requirements.md:301`（SC-004）；`requirements.md:217`（FR-025）。
  - **Gate**: 纠正类——点名比较制品与层级。

- [ ] CHK038 — SC-002/SC-003/SC-005 是否覆盖 FR-010 的 ambiguous-stop、stale-run/unattributed、orphan/stalled/remote-unreachable 以及完整路由分母？ [Coverage/Consistency, SC-002, SC-003, SC-005]
  - **Verdict**: FAIL — SC-002 要求"回答后路由正确率 100%"，未说明 FR-010 的 ambiguous-stop 是正确结果还是分母外；SC-003 只度量 foreign，未覆盖 stale-run/unattributed；SC-005 只覆盖 running/done/dead，FR-054/055 的 orphan/stalled/remote-unreachable 没有 SC。
  - **Evidence**: `requirements.md:299-302`；`requirements.md:199`（FR-010 ambiguous-stop）；`requirements.md:203-204`（stale-run/unattributed）；`requirements.md:252-253`（FR-054/055）。
  - **Gate**: 裁定类——补测量条款，并明确 ambiguous-stop 的计分方式。

- [ ] CHK039 — 每条 SC 的证据计划是否保留其完整度量元组（SC-001 双方完成判定正确率、SC-002 路由正确率、SC-006 无新事实时零反馈）？ [Traceability, SC-001, SC-002, SC-006]
  - **Verdict**: FAIL — feature-ref 的 SC-001 只写"事件归属差异清单为空"，漏掉"两条线路各自完成判定正确率 100%"；SC-002 只写澄清次数与零进程扫描，漏掉路由正确率；SC-006 只写模拟差异恰好 1 条，漏掉"无新事实时新增反馈为 0 条"。
  - **Evidence**: `feature-ref.md:57-58, 62`；`requirements.md:298-299, 303`。
  - **Gate**: 纠正类——把被删的度量分量补回证据计划。

- [ ] CHK040 — 68/68 FR 与 98/98 契约条款的覆盖声明是否由条款正文与具名任务共同支撑，特别是 FR-062/NG-03、FR-065、FR-012/EN-13、FR-031/WI-21？ [Traceability/Coverage, Req §FR-001…FR-068]
  - **Verdict**: FAIL — feature-ref 声称 68/68，但 NG 的追溯行把 NG-01…NG-09 映射到 FR-060…FR-066，实际没有任何 NG 条款承载 FR-065（grep 0）；NG-03 在 T068 的守卫清单中没有任务；T008/T016 未具名覆盖 FR-012/EN-13；WI-21 漏 FR-031 的"运行时/镜像只集成一次"；FR-065 仅由 LR-08/LC-17 承载。
  - **Evidence**: `feature-ref.md:44-51`；`contracts/non-regression-and-tests.md:61`（NG 追溯行），`:11`（NG-03）；`tasks.md:255`（T068 未列 NG-03）；`contracts/workspace-isolation.md:39`（WI-21）；`contracts/line-registry.md:17` 与 `contracts/lifecycle-detach-reattach.md:35`（FR-065）。
  - **Gate**: 裁定类/纠正类——修复追溯行，补 NG-03、FR-012/EN-13 的具名任务与 WI-21 的第五项。

---

## Coverage Map (68 FR / 10 SC)

| Requirement range | Checklist items |
|-------------------|-----------------|
| FR-001…FR-007 | CHK001, CHK002, CHK007, CHK008 |
| FR-008…FR-017 | CHK003, CHK004, CHK005, CHK006, CHK007, CHK009, CHK010 |
| FR-018…FR-032 | CHK011…CHK018 |
| FR-033…FR-045 | CHK019…CHK026 |
| FR-046…FR-059 | CHK027…CHK032 |
| FR-060…FR-068 | CHK009, CHK033, CHK034, CHK035, CHK040 |

| Success criterion | Checklist items |
|------------------|-----------------|
| SC-001 | CHK004, CHK010, CHK039 |
| SC-002 | CHK005, CHK006, CHK038, CHK039 |
| SC-003 | CHK004, CHK038 |
| SC-004 | CHK015, CHK037 |
| SC-005 | CHK031, CHK038 |
| SC-006 | CHK021, CHK023, CHK039 |
| SC-007 | CHK033, CHK034, CHK035 |
| SC-008 | CHK010, CHK018, CHK040 |
| SC-009 | CHK001, CHK036 |
| SC-010 | CHK032, CHK040 |

### FR → CHK Index (all 68 explicitly named)

| FR | Checklist items | Primary concern |
|----|-----------------|-----------------|
| FR-001, FR-002, FR-003, FR-007 | CHK001, CHK036 | Registry location/atomicity/concurrent read/stale |
| FR-004, FR-005 | CHK002 | id lifecycle/field schema |
| FR-006 | CHK008 | state sync |
| FR-008, FR-009 | CHK003 | envelope/sentinel |
| FR-010, FR-011 | CHK005 | ingress decision table |
| FR-012 | CHK006 | non-blocking clarification |
| FR-013 | CHK007 | PID identity |
| FR-014, FR-015 | CHK004, CHK038 | attribution classes |
| FR-016 | CHK010 | two-line acceptance |
| FR-017 | CHK004, CHK009 | single-line/legacy compatibility |
| FR-018, FR-019, FR-020, FR-021 | CHK011, CHK012 | worktree/ownership |
| FR-022, FR-023 | CHK013 | runtime records/archive |
| FR-024, FR-026 | CHK014, CHK016 | mirror cardinality/integration |
| FR-025 | CHK008, CHK015 | queue determinism |
| FR-027, FR-032 | CHK016 | push/cleanup |
| FR-028, FR-029 | CHK002, CHK017 | resources/reporting |
| FR-030 | CHK029 | re-entry order |
| FR-031 | CHK018, CHK040 | two-write acceptance |
| FR-033, FR-034 | CHK019, CHK020 | profile set/dimensions |
| FR-035, FR-036 | CHK021 | provenance/qodercli facts |
| FR-037, FR-038, FR-039 | CHK022 | observation surfaces/write order |
| FR-040 | CHK023, CHK024 | feedback/probe |
| FR-041, FR-043 | CHK025, CHK034 | non-interference/matrix |
| FR-042, FR-045 | CHK019 | delivery/mirror/docs |
| FR-044 | CHK026 | 063 single owner |
| FR-046, FR-047, FR-048 | CHK027, CHK028 | detach/four-piece/reservation |
| FR-049, FR-050 | CHK029, CHK030 | lease/identity/snapshot |
| FR-051, FR-052, FR-053, FR-054, FR-055 | CHK031, CHK038 | reattach outcomes |
| FR-056, FR-057 | CHK028, CHK032 | reservation/U6 closure |
| FR-058, FR-059 | CHK027, CHK031 | remote isomorphism/acceptance |
| FR-060, FR-061, FR-062 | CHK033 | no-push/no-deletion/no-loss |
| FR-063, FR-066 | CHK034 | 058/061 preservation |
| FR-064, FR-065 | CHK035, CHK040 | no-daemon/cross-machine |
| FR-067, FR-068 | CHK009, CHK040 | tests/single-line |

All 68 FR and all 10 SC appear in at least one item; the mapping is collective, not one-item-per-FR.

## Failing Items — Gate Hand-off

24 failing items are recorded for analyze/implement disposition. None was repaired in this phase (requirements/plan/tasks/contracts/data-model/feature-ref/quickstart were not modified).

**Decision-class (analyze/requirements adjudication required)**

- CHK004 — `legacy` 分类的消费规则与多线禁用边界。
- CHK007 — cwd/branch 必查 vs macOS `unsupported`/`skipped` 豁免的批准。
- CHK008 — pre-merge 状态与六同步点的单一状态映射。
- CHK012 — waiting 晋级是否允许 "holder closed"。
- CHK013 — line 本地运行时记录集合的闭合范围。
- CHK014 — FR-024 与 FR-026/US2 AS4 的镜像基数冲突。
- CHK020 — "安全缺省派发"的定义与 061 矩阵合成。
- CHK023 — standalone feedback 跳过的 requirements 批准。
- CHK024 — external skill 的 Probe Object class/unit/id 合法性。
- CHK026 — 063 保留吞吐策略与 064 档案事实的 owner 边界、CP-07/08 活引用。
- CHK030 — lease 续租节奏与活会话判据。
- CHK031 — 五值 reattach 结局到 Registry 状态/处置的唯一映射与 orphan 证据集。
- CHK038 — ambiguous-stop、stale-run/unattributed、orphan/stalled/remote 的 SC 覆盖。
- CHK040 — 68/68 与 98/98 追溯声明的裁定与补齐。

**Correction-class (one consistent reading; fix locally and disclose)**

- CHK002 — 实体字段表补齐 `run_history`、`profile_version`、`at` 类型、cap usage；消除 "R1" 悬空引用。
- CHK006 — 为 FR-012 增加验收场景/SC，或收窄其表述。
- CHK009 — LR-13/NG-07 carve out 注册失败停止。
- CHK017 — 资源报告加入 cap usage 字段与报告时点。
- CHK018 — WI-21 补 FR-031 第五项。
- CHK022 — Provenance `feedback_id` 时点、buffering 比对、多事件反馈规则。
- CHK029 — FR-030 的 "先" 限定为"任何去向决定之前"。
- CHK036 — SC-009 的 N 与写-读交错断言。
- CHK037 — SC-004 的比较层级。
- CHK039 — feature-ref 的 SC 度量元组补全。

## Validation Record

- **Checklist result**: 40 items — 16 PASS / 24 FAIL. FAILs are requirement-quality findings, not run anomalies.
- **Traceability**: 40/40 items carry a requirement/SC reference or a `[Gap]/[Ambiguity]/[Conflict]/[Assumption]` marker (100%, above the 80% floor).
- **Upstream validators (post-write run)**: see the run record appended at the end of this phase; `validate-requirements.py` and `validate-tasks.py` must both remain exit 0.
- **Upstream files untouched**: requirements.md, plan.md, tasks.md, contracts/, data-model.md, feature-ref.md, quickstart.md were read only. This file is new; `checklists/requirements.md` is unchanged.
- **No implementation testing**: no product behavior was run; all verdicts are textual/traceability judgments against file:line evidence.
- **Same-author gate**: detection delegated to three fresh-context read-only subagents with disjoint scopes; validation re-opened every cited line; 3 detector candidates were reclassified/merged before landing (see the note above).
