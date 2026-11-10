# Analyze — Merged Report, Round 2（096-sdd-observer-agent）

- **Line / Run**: `096-sdd-observer-agent` / `r20261110T081104Z-b096`
- **Stage**: analyze（串行集成者；第二轮修复后重过门：三路并发检测波 W1/W2/W3 + 合并波 + C/H 独立校验波）
- **Round**: 2（prior report: `test-evidence/analyze-merged-2026-11-10.md`；repair commit: `4808bd3f7`）
- **Date**: 2026-11-10
- **Authority**: `.specify/skills/internal/analyze-artifacts/SKILL.md` + `references/detection-and-severity.md` + `references/validation-and-report.md`；`.specify/constitution.md`（v1.19.0）
- **Read domain（合并波）**: `requirements.md`（全量）、`tasks.md`（全量）、`checklists/`（2 份，`[Gap]` 行复核）、`data-model.md` 与 `contracts/` 的跨波接缝抽读（E-3 / E-8 / E-9 / V-19、lifecycle C-07/C-08/C-09、engine C-09/C-10）、`quickstart.md` 头部、`feature-ref.md` FR 行、`.specify/features.md` 096 行、`.specify/features/096.md`、宪法 XVII、`temp-directory-discipline.md`、`closed-set-claims.md`；plan 域细节以 W2 波读值为准（本轮 `plan.md` 未变）
- **Write surface**: 本文件 + `test-evidence/analyze-{clause-coverage,decision-tensions,validation-wave}-round2.txt` + Wrap-up 记账；未修改任何 spec 制品，未执行任何修复（只读阶段）
- **Merge protocol（确定性归并）**: 分节 W1→W2→W3（本节 + 合并波）；各节内按 ID 字典序；跨波重复 ID 检查 **0 条**（`W1-*` / `W2-*` / `W3-*` 前缀互斥），「先声明先得 + 指针」规则本轮无触发。W1/W2/W3 表格按原文逐字保留，不重写、不重评级（C/H 校验结果以 `(validated: …)` 标注与 § Validation wave 为准）；W3-06 为轮 1 未再检测但实测仍成立的 LOW，按 `(carried over)` 入主表（§ Rounds 的残余义务由合并波承接）。
- **C/H 校验**: 4 条 CRITICAL/HIGH 候选由 4 个独立只读外部 worker 并行校验（Recipe 7 载体；`qodercli -p`，只读工具白名单 `Read Grep Glob Bash`，`--no-session-persistence`，一节一 finding、互不可见、与检测者不相交）；波后 `git status --porcelain` 与波前逐字节一致（无 validator 写入）。结果：**sent 4 · confirm 4 · downgrade 0 · reject 0**（降级率 0/4）。

---

## Top summary — C/H count and per-item pointers（不修复）

**CRITICAL（validated，1 条）**：

| ID | Category | Severity（validated） | Anchor（逐条指针） | Fact pointer（一句话） |
|----|----------|----------------------|--------------------|------------------------|
| W3-07 | 宪法对齐 / 临时目录纪律 | **CRITICAL**（confirm；宪法变体不可降级） | `tasks.md:30`；`temp-directory-discipline.md` §1/§2；`constitution.md` XVII（:375-377） | GATE-1 的检查命令把 scratch 文件写到裸 `/tmp/096-current-names.txt`，临时目录纪律明令禁止裸 `/tmp/...` 且宪法 XVII 把受制裁根集委托给该 owner —— 门禁文本指示了一次 MUST 违反 |

**HIGH（validated，3 条）**：

| ID | Category | Severity（validated） | Anchor（逐条指针） | Fact pointer（一句话） |
|----|----------|----------------------|--------------------|------------------------|
| W3-08 | containment claim 无基线指涉 | **HIGH**（confirm） | `tasks.md:22`（DoD-6）；`tasks.md:37`（GATE-8）；`tasks.md:211`（T032） | 三个载体声明「unmodified/unchanged」，唯一检查是无 commit 参数的裸 `git diff --name-only`（工作树 vs 索引，对已提交变更失明）且无任何基线/哈希指涉 —— 包含性声明 void |
| W3-09 | DoD 前提重测缺口 | **HIGH**（confirm） | `tasks.md:24`（DoD-8）；`tasks.md:66-85`（§ Premises）；`tasks.md:109-112`（T002/T004/T005） | DoD-8 要求 implement 入口重测全部 § Premises 量，但 11 个计数 / token 前提（FR 23 / SC 7 / clauses 58 / fact files 34 / presets 17 / bounded 19 / H2 14 / mirror list 9 / stage sequence 8 / digest tokens 0）无任何重测行或证据落点 |
| W3-10 | 阶段规则与行级阻塞矛盾 | **HIGH**（confirm） | `tasks.md:120`；`:122`；`:161`（T014）；`:163`（T018）；`:186`（T023）；`:231`（T036） | Foundational「任何故事行不得在两者齐备前开始」（CRITICAL）与行级 `[blockedBy:]` 作为包内顺序权威相矛盾：T014/T036 与 T006 同包却只列 T007，可在 T006 未闭合时启动 |

**Severity distribution（validated，主表）**: **CRITICAL 1 · HIGH 3 · MEDIUM 29 · LOW 11 —— 主表 44 行**（≤50 上限，无 overflow）。另有 delta-only 行：resolved 7 · rejected 1（Appendix A，不静默丢弃）· superseded 2（W3-03 → W3-12+W3-14、W3-05 → W3-09）。

**门禁结论须双向陈述（不构成「ready to implement」）**：本轮修复**清零了轮 1 的 HIGH 积压**（W1-02 / W3-01 / W3-04 / E-01 fixed，W1-03 rejected 维持，W1-01 已是 MEDIUM），但**第二轮重扫不清零**——新增 1 CRITICAL + 3 HIGH（W3-07/08/09/10，全部 confirm）。按技能 §9，**CRITICAL 须在 `/speckit.implement` 前处置**；本阶段只读，未修复。

---

## Validation wave（C/H，独立只读）

- **Carrier**: subprocess 载体（Recipe 7）——每 finding 一个独立 `qodercli` 子进程，只读工具白名单、`--no-session-persistence`；brief 只含 finding（id / category / claim / severity）+ evidence locations，不含检测推理、不含其他 findings；检测者（W3 波 worker）与校验者不相交。
- **Read-only proof**: 波后 `git status --porcelain` 与波前逐字节一致（`git-status-pre.txt` / `git-status-post.txt`）；每个 `.status` 记录 `exit=0`。
- **Downgrade rate**: sent 4 · confirm 4 · downgrade 0 · reject 0 → 降级率 **0/4**。检测波本轮未系统性高估；W3-07 为宪法变体，confirm 即锁 CRITICAL。

| Finding | Sent | Verdict | Final severity |
|---------|------|---------|----------------|
| W3-07 | CRITICAL | confirm | CRITICAL |
| W3-08 | HIGH | confirm | HIGH |
| W3-09 | HIGH | confirm | HIGH |
| W3-10 | HIGH | confirm | HIGH |

### Validator evidence boundaries（verbatim）

**W3-07 — verdict: confirm**

```
evidence_supported: tasks.md:30 contains the bare `/tmp/096-current-names.txt` path twice (the `--names-out` write and the `comm -13` comparison); scripts/bash/run-tests.sh:21-24, :82, :224-228 confirms `--names-out` writes FAILED ids to exactly the given path, so executing GATE-1 creates a file in bare `/tmp`; temp-directory-discipline.md §1 (sanctioned roots only `~/tmp/<project>/<purpose>/` and `.specify/.tmp/<purpose>/`) and §2 (forbids "裸 `/tmp/...`、`/var/tmp/...`") establish the prohibition, and §5 exceptions do not cover a persistent scratch output; constitution.md:375-377 (XVII) makes the sanctioned-root rule a MUST and delegates roots/cleanup/exceptions to that owner document.
evidence_not_supported: The write is prospective — tasks.md instructs the command; the file is created only when an implementer executes GATE-1, and I did not observe any execution. The owner document and XVII are framed around "temporary or scratch directory," while this is a file directly in the OS temp dir; the violation rests on §2's textual ban of the bare-`/tmp` form plus the absence of a §5 exception, which is an interpretive step beyond a literal directory-creation act. No machine guard enforces this instance: scan-temp-usage.py scans only shared/templates/skills/agents/scripts (scripts/python/scan-temp-usage.py:34, :36-39) and skips `.specify`, so the tasks.md text is outside its scope; nothing in the ALLOWLIST covers spec artifacts. I also did not observe any justifying note for this path at the gate, so the "instructs a MUST violation" characterization stands as written.
```

**W3-08 — verdict: confirm**

```
evidence_supported: tasks.md:22 (DoD-6) states reporting-obligations.md, the STAGE_ARTIFACTS mapping and shared/declarations/facts/driver-stage-sequence.yaml "are unmodified" with no baseline named; tasks.md:37 (GATE-8) checks only a bare `git diff --name-only` (no commit arg, working tree vs index, blind to staged/committed changes) naming only two of the three artifacts — STAGE_ARTIFACTS (owner skills/external/sdd-loop-driver/scripts/loop-state.py:211) is unchecked there; tasks.md:211 (T032) asserts the three are "unchanged" without naming a baseline, hash or expected content; no baseline for these carriers is frozen elsewhere in tasks.md (T002/T003/T005 at lines 109-112 cover mirrors, test names, digest field-set, coverage only; base sha c691d658a at line 42 is scoped to environment probes and unreferenced by GATE-8/T032); .specify/shared/guidelines/closed-set-claims.md requires a baseline referent (element 1), lists "无基线参照物的稳定性断言" as a rejection form (line 43), and prescribes HIGH for a void claim carrying a DoD/gate (line 36).
evidence_not_supported: The phrase "the only check is a bare git diff --name-only" is imprecise in coverage — GATE-8's git check covers two of the three artifacts (STAGE_ARTIFACTS has no check at all in GATE-8), and T032 is itself a planned verification surface (a test assertion) though it carries no referent; DoD-6 also holds a separate digest-field-set baseline check unrelated to these carriers. I could not observe whether the eventual T032 implementation would pin a literal content/hash inside the test, and did not evaluate whether any other existing gate or mirror check incidentally detects changes to loop-state.py or the two carrier files.
```

**W3-09 — verdict: confirm**

```
evidence_supported: tasks.md:24 (DoD-8) mandates re-measurement of every § Premises quantity at implement entry with no check command or owner; tasks.md:66-85 lists 14 premises, states "MUST be re-measured at implement entry" (line 68), of which 11 are the count/token rows named in the finding; tasks.md:109-112 shows T002 re-captures only the 3 baseline rows, T004 re-probes only § Environment Prerequisites (tasks.md:40-48), and T005 re-freezes the coverage baseline, which is not a § Premises row; a full read of all 381 lines plus grep for premise/re-measur/DoD-8 found no other row, GATE-1…GATE-9, T047 gate sweep, or evidence sink covering the 11 count/token premises — only notes/pre-change-measurements.md (T002/T005) and test-evidence/env-probe.txt (T004) exist as re-measurement sinks.
evidence_not_supported: The finding's count "T002/T005 re-capture only four baselines" slightly overstates their scope as premises baselines — only three of the four captured values are § Premises rows; T005's coverage baseline is outside the table (no effect on the conclusion). The cited artifacts cannot establish, and the finding does not claim, whether an external mechanism (e.g., /speckit.implement Step 0 or the driver) re-measures these premises outside tasks.md; nothing in tasks.md assigns that duty. I did not measure whether downstream test failures would in practice trip loudly on premise drift (T020/T028 carry literal before→after counts that would be stale under drift), so the practical blast radius of the gap beyond DoD-8 being undischargeable was not observed.
```

**W3-10 — verdict: confirm**

```
evidence_supported: tasks.md:120 ("No story row may start before both exist") and :122 (CRITICAL phase gate) require both T006 and T007 before any story row; T014 (:161) and T036 (:231) are [US2]/[US5] story rows listing only [blockedBy: T007], while :89 declares row-level [blockedBy:] tags the ordering authority inside a package and :54 says only untagged rows follow phase order; T014/T036 are in wp01 alongside T006 (:93), so no package edge supplies the missing T006 dependency and they can start after T007 closes with T006 still open (T018/:163 and T023/:186 are protected by wp02/wp03 package edges, :100). T014's tamper variants depend on the closed event-class set owned by T006 (:124).
evidence_not_supported: No observed instance of early start (static artifact inconsistency only; no run records examined); the row texts of T014/T036 do not explicitly cite journal-format, so functional dependence on T006 is inferred, not stated; whether an executor would apply the CRITICAL gate additively rather than defer to the tag authority cannot be determined from the file (no resolution clause exists either way); HIGH severity is a judgement — the concrete impact is a one-token tag repair limited to two fixture rows.
```

---

## Merged findings

### Wave W1 — requirements + checklists（20 rows；读域 `requirements.md` + `checklists/2026-11-10-observer-requirements-quality.md`）

Round-2 模式：full severity（重判 round-1 + 全量检测）。轮 1 处置：**W1-02 fixed**、**W1-03 rejected（Appendix A 维持，不重报）**；`carried over` = W1-01、W1-04…W1-18（16 条，原 ID 保留）；`new` = W1-19…W1-22（4 条）。本波 C/H = 0，无需校验波（合并波转派 W3 波 C/H 见上）。

| ID | Severity | Pass | Anchor | Fact（一句话事实） | Propagation | Suggested disposition（指针） |
|----|----------|------|--------|--------------------|-------------|------------------------------|
| W1-01 | MEDIUM (carried over) | F inconsistency | `requirements.md:181`; `requirements.md:142`; `checklist.md:36`; `checklist.md:72` | FR-011 规定条目恰好承载九类信息，而 Key Entities 的 Journal Entry 仍称「承载八类信息」，同一制品对同一封闭字段集给出两个计数；round-1 校验波以「下游 plan/data-model/contracts/tasks 均按九类落地、无下游传播」降级 MEDIUM，但缺陷本身未修复。 | `none`（下游已按九类落地，round-1 校验证据） | `/speckit.requirements`（Key Entities 改为九类或引用 FR-011） |
| W1-04 | MEDIUM (carried over) | C underspecification | `requirements.md:129`; `requirements.md:195` | FR-004 以 `line_id` + spec key 派生实例身份，但全文未定义 spec key 的派生来源、唯一性范围与 owner，身份函数不可求值，SC-005 的「两个不同实例身份」缺可判定函数。 | plan 身份模型 / driver 修订 / SC-005 测试 | `/speckit.clarify`（定义 spec key 派生与 owner） |
| W1-05 | MEDIUM (carried over) | C underspecification | `requirements.md:160` | FR-023 规定入口声明键 `observer: on\|off`，但「入口声明」的载体、位置、解析格式与 owner 均未定义，关闭开关无法被实现方无歧义解析。 | driver U0 解析 / plan | `/speckit.clarify`（绑定入口声明载体与解析规则） |
| W1-06 | MEDIUM (carried over) | C underspecification | `requirements.md:145`; `requirements.md:192` | FR-014 要求证据指针携带「留存类别」并在线收束时可解析，SC-002 以「可解析」为判据，但留存类别词表与可解析判定（存在 / 类型 / 版本历史可达）未定义为受拥有的封闭集合，也未覆盖工作树清理后的时点。 | plan checker / 测试夹具 | `/speckit.clarify` + `/speckit.plan`（留存类别封闭词表与可解析判定） |
| W1-07 | MEDIUM (carried over) | F inconsistency | `requirements.md:135`; `requirements.md:136` | FR-007 规定上一执行 `.status` 未结算时 driver MUST NOT 派发下一个，FR-008 又允许失败 / 停滞 / 窗口到期后在阶段边界重启；执行崩溃且未留 `.status` 时既未结算又已结束，两条规则互斥。 | driver 派发逻辑 / plan | `/speckit.clarify`（裁定未结算执行的结算或超时规则） |
| W1-08 | MEDIUM (carried over) | F inconsistency | `requirements.md:128`; `requirements.md:141`; `requirements.md:158` | FR-003 禁止不同线共享 journal、FR-010 按 spec 目录落一份 journal，但全文未排除两条线（含嵌套运行）解析到同一 spec 目录的状态，该状态下路径冲突且「不共享」无法成立。 | plan 路径模型 / 双线夹具 | `/speckit.clarify`（排除或消歧同 spec 双线状态） |
| W1-09 | MEDIUM (carried over) | C underspecification | `requirements.md:144`; `requirements.md:160` | FR-013 未裁决缺口窗口的三种边界：零长度窗口（起止同秒）写入还是抑制、连续多个缺口的起点链、以及 `state=disabled` 无启动时间时的起点回退值。 | plan 缺口写入 / checker / 测试 | `/speckit.clarify`（缺口窗口边界裁决） |
| W1-10 | MEDIUM (carried over) | B ambiguity | `requirements.md:194`; `requirements.md:52` | SC-004(c) 要求 checker 拒绝「自由叙述条目」，但需求层未给出自由叙述的结构定义，反例构造只能回落到 checker 自身判定，存在循环判据风险。 | plan 客观性夹具 / checker | `/speckit.clarify`（自由叙述的结构定义） |
| W1-11 | MEDIUM (carried over) | B ambiguity | `requirements.md:142`; `requirements.md:144` | FR-011 的 `命令` 字段允许「原文或 `-`」，但原文取自哪个载体、字符集 / 长度如何约束均未定义，评价或建议文本可借这个自由文本字段进入条目，与 FR-013 客观性构造冲突。 | plan journal 格式 owner / driver | `/speckit.clarify`（命令字段来源与内容约束） |
| W1-12 | MEDIUM (carried over) | B ambiguity | `requirements.md:144` | FR-013 以「限定为」引出观测输入清单，但未声明该清单是否穷尽，也未指名新增载体的 owner，其他制品引入的 meta 包络是否可读不可判定。 | plan 读域实现 / 定义文本 | `/speckit.clarify` + `/speckit.plan`（封闭清单与扩展 owner） |
| W1-13 | MEDIUM (carried over) | C underspecification | `requirements.md:150`; `requirements.md:88` | FR-016 把写面界定为 journal 与「自身执行运行产物」，但 US4 AS1 的写面审计未定义锁文件 / 游标 / 临时文件的归属，而 FR-007 的单写者协议需要协调状态。 | plan 写面声明 / tasks | `/speckit.plan`（写面枚举与审计规则） |
| W1-14 | MEDIUM (carried over) | E coverage gap | `requirements.md:252` | 「journal MUST NOT 被加入任何阶段 required artifact 集或 `STAGE_ARTIFACTS` 映射」只存在于 Assumptions A12，既无 FR 承载也无带红腿的 SC。 | plan / tasks（红腿） | `/speckit.requirements`（提升为 FR）→ `/speckit.tasks` |
| W1-15 | MEDIUM (carried over) | F inconsistency | `requirements.md:129`; `requirements.md:141`; `requirements.md:234`; `requirements.md:247` | FR-004 与 A7 把身份第四项写作「执行 label」，FR-010 与 clarify 记录写作「实例 label」；journal 跨多次执行只有一份头部，而派发 label 每次执行不同，头部字段语义悬空。 | plan 头部 schema / 模板 | `/speckit.clarify`（头部 label 字段定名与取值） |
| W1-16 | LOW (carried over) | H completeness | `requirements.md:126` | FR-001 的 MUST NOT 覆盖 stage executor / reviewer / reporter 三个席位，但三者没有指向定义 owner 的引用，禁令无法按同一谓词独立核对。 | 定义文本 | `/speckit.requirements`（补 owner 引用） |
| W1-17 | LOW (carried over) | A duplication | `requirements.md:137`; `requirements.md:141`; `requirements.md:144`; `requirements.md:191`; `requirements.md:194`; `requirements.md:197` | FR-009、FR-010、FR-013、SC-001、SC-004、SC-007 在 `[[STR-00N]]` 标记旁同时复制了字面量，违反本制品自设的「用 `[[STR-NNN]]` 代替复制字面量」约定（FR-010 路径语句中的文件名属位置定义，可从宽）。 | requirements 文本 | `/speckit.requirements`（仅保留 token） |
| W1-18 | LOW (carried over) | B ambiguity | `requirements.md:113`; `requirements.md:142` | Edge Cases 称「checker 以文件序判定非递减」但未点名判定对象（序号还是观测时间），与 FR-011 的序号单调递增并列时存在两种读法。 | plan checker | `/speckit.clarify` 或 `/speckit.plan`（点名判定对象） |
| W1-19 | MEDIUM (new) | F inconsistency | `requirements.md:195`; `requirements.md:104`; `requirements.md:135`; `checklist.md:41` | SC-005 与 US5 AS2 把同线第二个并发执行的期望写成「被拒绝或串行化」，而 FR-007 规定 driver MUST NOT 派发且引擎 MUST 以单写者协议拒绝第二 writer；验收判据未收敛为恰一个可观测结果（CHK023）。 | driver 派发 / SC-005 测试 / tasks | `/speckit.requirements`（与 FR-007 对齐为单一可观测结果） |
| W1-20 | MEDIUM (new) | E coverage gap | `requirements.md:133`; `requirements.md:195`; `checklist.md:13` | FR-005 的「唯一机械判据」依赖 `line 已登记` 与 `U2 派发` 两个无 owner 引用的谓词，而 SC-005 只断言「首个 journal 条目早于首个阶段完成条目」，该弱代理无法证明「U2 派发前启动」（CHK001）。 | driver 启动步骤 / SC-005 测试 | `/speckit.requirements`（补谓词 owner 引用与判定动作）+ SC 红腿 |
| W1-21 | MEDIUM (new) | E coverage gap | `requirements.md:134`; `requirements.md:146`; `requirements.md:152`; `requirements.md:153`; `requirements.md:158`; `requirements.md:189` | FR-006（承载模态）、FR-015（脚本接口契约）、FR-018（不发用户可见汇报 / 提问 / 审批）、FR-019（triplet 引用不复制 / 不新造通道）、FR-021（非 SDD 命令与非 SDD team 运行不产生 observer / journal）均无对应 SC 或 Acceptance Scenario 红腿。 | tasks 验收夹具 / contracts | `/speckit.requirements`（补 SC/AS 红腿）→ `/speckit.tasks` |
| W1-22 | MEDIUM (new) | F inconsistency | `requirements.md:191`; `requirements.md:137`; `requirements.md:111` | SC-001 的失败线覆盖判据在「线在 observer 启动前即失败、按 Edge Cases 允许无 journal」分支不可满足（既无阶段开始条目也无 `observer-gap` 条目），判据未引用 FR-009 的无 journal 回退。 | 验收测试 / SC-001 | `/speckit.requirements`（SC-001 增补无 journal 分支回退引用） |

**Checklist Accountability（W1 处置，机器可读行）**

清单 `checklist.md` 共 38 项、仍全部未勾选；`[Gap]` 标签 7 项逐项处置如下（本轮复核仍成立）。

| CHK | Anchor | Disposition |
|-----|--------|-------------|
| CHK002 | `checklist.md:14` | raised-as-finding W1-04 |
| CHK003 | `checklist.md:15` | raised-as-finding W1-05 |
| CHK004 | `checklist.md:16` | raised-as-finding W1-13 |
| CHK005 | `checklist.md:17` | raised-as-finding W1-06 |
| CHK008 | `checklist.md:20` | covered-by requirements.md § FR-001（`agents/sdd-observer.agent.md` 模板即角色面单一 owner） |
| CHK009 | `checklist.md:21` | raised-as-finding W1-16 |
| CHK036 | `checklist.md:63` | raised-as-finding W1-14 |

```
CHK002 disposition: raised-as-finding W1-04
CHK003 disposition: raised-as-finding W1-05
CHK004 disposition: raised-as-finding W1-13
CHK005 disposition: raised-as-finding W1-06
CHK008 disposition: covered-by requirements.md § FR-001
CHK009 disposition: raised-as-finding W1-16
CHK036 disposition: raised-as-finding W1-14
```

`unchecked[Gap]=7 · raised=6 · covered-by=1 · unraised=0 · undispositioned=0` → 阻断计数 **0**。非 `[Gap]` 项中本轮新吸收：CHK001→W1-20、CHK018→W1-01、CHK023→W1-19；其余材料性缺陷由既有 finding 按锚点吸收（CHK011→W1-07、CHK013→W1-11、CHK014→W1-10、CHK017/CHK019→W1-09、CHK020/CHK021→W1-08、CHK027→W1-03〔rejected，下游具名基线〕）；剩余项在需求文本中已有可引用答复，不另立 finding。

### Wave W2 — plan block（12 rows；读域 `plan.md`、`data-model.md`、`quickstart.md`、`feature-ref.md`、`research.md`、`contracts/` 5 页）

Round-2 模式：full severity 重判。轮 1 处置：**W2-06 fixed**、**W2-10 fixed**（修复轮 E-01 落地的条款级 FR 引用使 `plan.md:42` row I 证据事实上成立）；`carried over` = W2-01…W2-05、W2-07…W2-09、W2-11…W2-14（12 条）。本波全量重扫 **new = 0**：五页 58/58 条款体现均载条款级 FR citation group，且每页条款 group 的并集等于该页 `Requirements:` 行、无越页引用 —— 修复未引入新不一致。本波 C/H = 0。

| ID | Severity | Anchor | Fact (one sentence) | Suggested attribution |
|----|----------|--------|---------------------|-----------------------|
| W2-01 | MEDIUM (carried over) | `quickstart.md:3` vs `quickstart.md:5`/`:94`；`plan.md:31`、`:139`、`:236` | quickstart 首行宣布 "Seven walk-through scenarios"，但文件含 S-0…S-7（八节），而 plan 三处均计 8 个场景（S-0…S-7）。 | `/speckit.plan` — `quickstart.md` 开头（对齐计数，或声明 S-0 为 pre-check 不计入 scenario） |
| W2-02 | MEDIUM (carried over) | `data-model.md:36` vs `data-model.md:127` | E-3 声明执行状态 `started → settled \| failed` 并称记入 E-9 spine 节，但 E-9 的封闭 `state` 域为 `started \| failed \| disabled \| closed` —— `settled` 无 spine 表示。 | `/speckit.plan` — data-model E-3/E-9（补 `settled` 值，或明确映射到 E-3 状态机里的非 spine 语义） |
| W2-03 | MEDIUM (carried over) | `data-model.md:137` vs `contracts/observer-lifecycle.contract.md:63`（cf. `contracts/observer-verification.contract.md:19`） | 终态失败时 E-9 说 driver 写 `state=closed`（带原因），C-08 说 driver 记 `state: failed` 加原因；反向地，终态成功时 C-08 又未点名 E-9 要求的 spine `closed` 写入 —— 两个终态分支都没有一致的 spine 规则。 | `/speckit.plan` — E-9 与 lifecycle C-08（为成功/失败各写一条唯一终态规则） |
| W2-04 | MEDIUM (carried over) | `contracts/journal-engine.contract.md:55` vs `data-model.md:160-161`、`quickstart.md:59` | C-09 要求 `check` 校验 V-16/V-17，但 V-16 是 append 时的身份拒绝（需 execution label 与 spine），而 `check` 只有 `--spec-dir`/`--repo` —— V-16 按字面不可执行；quickstart S-3 重复 V-1…V-13-only 读法。 | `/speckit.plan` — journal-engine C-09 与 V-16/V-17 归属（V-16 归 append；check 补 spine 输入或从清单移除 V-17） |
| W2-05 | MEDIUM (carried over) | `feature-ref.md:22-40`（cf. `:75`、`:77`） | Delivered paths 表的 FR 列从未引用 FR-019 或 FR-021（两者在 FR → Contract map 有归属），23 个 FR 中 2 个无交付路径归属。 | `/speckit.plan` — feature-ref delivered-paths 表（补行归属或注明经哪一行间接交付） |
| W2-07 | MEDIUM (carried over) | `data-model.md:82-97`（E-6）+ `contracts/journal-engine.contract.md:31` | E-6 只给每事件的主载体，无「载体字段 → 九列」的 per-event 投影规则；C-05 的 idempotency「natural keys」未定义 —— 确定性投影与幂等 append 在读域内不可判定。 | `/speckit.plan` — data-model E-6 / engine C-04/C-05（补 per-event 投影表并定义 identity keys） |
| W2-08 | MEDIUM (carried over) | `data-model.md:163`（V-19）；`contracts/observer-lifecycle.contract.md:45`；`contracts/observer-verification.contract.md:31`；`plan.md:81` | V-19 声称两条并行线的 journal "never share a path"，但路径由 spec key 派生、双线 fixture 用的是两个不同 spec 目录；same-spec 两线仅由 T-001 决策记录排除，V-19 与两处 C-05 均未写明该前提。 | `/speckit.plan` — V-19 / lifecycle C-05 / verification C-05（写明 distinct-spec 前提，或补 same-spec 判定） |
| W2-09 | MEDIUM (carried over) | `plan.md:56` vs `quickstart.md:15-83` | Constitution Check row XV 的证据声称 quickstart "defines journal / observer / gap at first use"，但 quickstart 无这些定义 —— 术语在 S-1/S-2/S-5 裸用。 | `/speckit.plan` — `quickstart.md`（补首次使用定义）或修正 row XV 证据 |
| W2-14 | MEDIUM (carried over, narrowed) | `data-model.md:116`（E-8）+ `contracts/journal-engine.contract.md:49`（C-08）+ `contracts/journal-format.contract.md:61`（C-10） | C-10 已给 no-entry 时的窗口起点回退，但 engine C-08 的触发仍要求 previous entry（"if the previous entry's `observed_at` is earlier than the spine record's `started_at`"），且 "the spine record" 未指明取哪一节（latest vs 该执行自己的启动节）—— start-failure/no-entry 缺口在引擎契约层不可达或歧义。 | `/speckit.plan` — E-8 / engine C-08（补 no-entry 分支并消歧 spine 节） |
| W2-11 | LOW (carried over) | `plan.md:47` vs `data-model.md:110`（E-7）+ `data-model.md:97`（`observer-error` `min_persistent: 0`） | Row VI 证据称每行都有 "resolvable pointer"，但 E-7 允许指向已清理文件的 runtime 指针、`observer-error` 允许零 persistent —— 一行可以只带一个不再解析的 runtime 指针。 | `/speckit.plan` — 改写 row VI 证据（persistent 指针须解析；runtime 指针仅标记） |
| W2-12 | LOW (carried over) | `data-model.md:33`（cf. `research.md:28`、`plan.md:195`、`quickstart.md:34`） | 执行 label 中段在 data-model/research 叫 `run_stamp`、在 plan EP-007 叫 `run`、在 quickstart 示例中显示为 run id（`R1`），三者无映射规则。 | `/speckit.plan` — data-model E-3 / research R-03（统一 token 名并定义，示例对齐） |
| W2-13 | LOW (carried over, narrowed) | `contracts/journal-engine.contract.md:19` | C-03 以 "mutually exclusive semantics" 命名 `--settle` / `--final`（且已写明 `--final` 追加 `observer-settle`），但从未说明两 flag 能否同次出现、非法组合落到哪个退出码 —— 组合规则仍未决。 | `/speckit.plan` — journal-engine C-03（写明互斥/组合规则与退出码） |

### Wave W3 — tasks.md（12 rows：W3-06 carried + W3-07…W3-17；读域仅 `tasks.md`）

`W3-06` 为轮 1 LOW、本轮未被 W3 worker 重报但合并波实测仍成立（`:168` 原文未变），按 `carried over` 入表；`W3-07…W3-17` 为本轮新增（ID 续接轮 1，避免与归并报告 W3-01…W3-06 冲突）。W3-07/08/09/10 的 C/H 由校验波 confirm（见上）。本波确定性检查读数：`validate-tasks.py` → `0 error(s), 4 warning(s)`（4 条均出现在 § Green Attribution 披露表，exit 0）；`account-clause-coverage.py` → `status: ok`（58/58 claimed、FR 23/23、beyond-baseline 0，exit 0）；`pre-analyze-check.py --stage tasks` → `decision: pass`（errors=0，advisories=82 均为本特性待创建路径，非 strict 不阻断）。

| ID | Severity | Anchor | Fact（一句话事实） | Suggested ownership（指针） |
|----|----------|--------|--------------------|------------------------------|
| W3-06 | LOW (carried over) | `tasks.md:168`（cf. 全文 V-rule 检索） | T017 只枚举 data-model 的 V-1…V-13 与 V-16/V-17，V-14、V-15、V-18、V-19、V-20 在 tasks.md 全文无任何归属行（本轮实测 :168 原文未变）。 | tasks stage — T017 检查范围，或补 data-model → task 归属行（合并波对照：V-14→T011/T037、V-18→T031/T019、V-19→T036/T037、V-20→T006/T017；V-15→T024 仅第一句承接） |
| W3-07 | **CRITICAL** (validated: confirm) | `tasks.md:30` | GATE-1's check writes the scratch file `/tmp/096-current-names.txt`, while `.specify/shared/guidelines/temp-directory-discipline.md:19` explicitly forbids bare `/tmp/...` and Constitution XVII delegates that closed set to the owner — the gate instructs a MUST violation. | tasks stage: replace with `.specify/.tmp/096/current-names.txt` (matched by `.specify/.gitignore` `.tmp/`) or `~/tmp/096/...`; then re-run GATE-1. |
| W3-08 | **HIGH** (validated: confirm) | `tasks.md:22`, `tasks.md:37`, `tasks.md:211` | DoD-6/GATE-8/T032 claim `reporting-obligations.md`, `STAGE_ARTIFACTS` and `driver-stage-sequence.yaml` are “unmodified/unchanged”, but the only check is a bare `git diff --name-only` (working tree vs index, blind to committed changes) and T032 names no baseline or hash — the containment claim is void for lack of a baseline referent. | tasks stage: pin the implement-entry commit and compare `git diff --name-only <base>...HEAD -- <three paths>`, plus a content-shape/hash assertion in the boundary test. |
| W3-09 | **HIGH** (validated: confirm) | `tasks.md:24`, `tasks.md:66-85`, `tasks.md:111` | DoD-8 requires every § Premises quantity to be re-measured at implement entry, but the only re-measurement row (T004) covers § Environment Prerequisites and T002/T005 re-capture only four baselines; the counts FR 23 / SC 7 / clauses 58 / fact files 34 / presets 17 / bounded 19 / H2 14 / mirror list 9 / stage sequence 8 / digest tokens 0 have no re-measurement row or evidence path. | tasks stage: extend T004 (or add a Setup row) to run each § Premises re-derivation command and record readings/deltas under `notes/pre-change-measurements.md` or `test-evidence/premises-entry.txt`. |
| W3-10 | **HIGH** (validated: confirm) | `tasks.md:120`, `tasks.md:122`, `tasks.md:161`, `tasks.md:163`, `tasks.md:186`, `tasks.md:231` | The Foundational phase says “no story row may start before both [T006 and T007] exist” (CRITICAL), but T014/T018/T023/T036 each list only one of T006/T007 in `[blockedBy:]`; since row-level tags are declared the ordering authority inside a package, T014/T036 can start before T006 is closed. | tasks stage: add both foundational rows to each story-row blocker set, or qualify the blanket phase rule and explain the intentional partial dependency. |
| W3-11 | MEDIUM (new) | `tasks.md:348`, `tasks.md:351`, `tasks.md:353`, `tasks.md:169`, `tasks.md:187`, `tasks.md:254` | The SC → row trace disagrees with the row citation groups: SC-001 omits T047 (row cites SC-001), SC-004 includes T019 (row cites no SC-004), and SC-006 omits T024 (row cites SC-006). | tasks stage: reconcile the § SC → row trace with each row's parenthetical citation group (or correct the row citations). |
| W3-12 | MEDIUM (new) | `tasks.md:291`, `tasks.md:193` | § Parallel Opportunities says T026 and T027 “run in parallel after T025”, but T027 carries `[blockedBy: T026]`, so the pair cannot start together. | tasks stage: remove T026 from T027's blocker set if the pointer does not depend on the reference file, or delete the parallel claim. |
| W3-13 | MEDIUM (new) | `tasks.md:284`, `tasks.md:319-323`, `tasks.md:96-100` | § Within Each User Story says “Story complete before moving to the next priority” and the MVP order is US1 → US2 → US3, but US2's slice-green/evidence rows T021–T022 sit in `wp04-release-and-evidence`, which executes after `wp03-driver-lifecycle` (US3/US4/US5). | tasks stage: move T021–T022 into wp03 (they only need T017/T020) or qualify the story-completion rule for package dispatch. |
| W3-14 | LOW (new) | `tasks.md:289-292`, `tasks.md:303-310`, `tasks.md:111`, `tasks.md:124`, `tasks.md:163`, `tasks.md:210-211` | The `[P]` marker set disagrees with the parallel statements: T006, T018, T031 and T032 are named as parallel in § Parallel Opportunities / the Parallel Example but lack `[P]`, and T004 is `[P]` without the `[blockedBy: T001]` edge that “after T001” implies. | tasks stage: add `[P]` where the section already schedules the rows in parallel, and add the T001 blocker to T004 (or drop the “after T001” wording). |
| W3-15 | LOW (new) | `tasks.md:372` (cf. `validate-tasks.py` WARN at `tasks.md:162`) | The disclosed-warnings row for T016→T024 explains the inversion as “C-03 before C-04”, but the validator's actual pair is T016 C-07 → T024 C-03 (the adjacent C-03/C-04 inversion is T014→T024, not T016). | tasks stage: correct the rationale to the actual clause pair, or re-state the pair as T014→T024 if that is the intended inversion. |
| W3-16 | LOW (new) | `tasks.md:11`, `tasks.md:98`, `tasks.md:108`, `tasks.md:252` | The evidence-layout prose says “execution readings land in test-evidence/” and “every other evidence file is written by rows of exactly one package”, but T002/T005 write `notes/pre-change-measurements.md` and T045 writes `notes/quickstart-run.md`, which T001 (Setup) created — a second package touches that path. | tasks stage: qualify the prose to the actual landing points (notes vs test-evidence) and include `quickstart-run.md` in the Setup/write-domain exception. |
| W3-17 | LOW (new) | `tasks.md:191`, `tasks.md:194` | T025 authors the new driver H2 without stating its position, while T028 pins it “immediately before the compiled Wrap-up section”; an executor following T025 alone can place it elsewhere and fail the T028 pin. | tasks stage: state the H2's required position in T025 (last H2 before `Wrap-up`). |

**Round-1 W3 residue/delta（合并波承接，W3 worker 读域不含轮 1 findings 文件）**

| Prior ID | R1 severity | R2 status | Evidence | Handling |
|----------|-------------|-----------|----------|----------|
| W3-01 | HIGH | **fixed** | `tasks.md:89-100` 包图重切为严格串行链 wp01→wp02→wp03→wp04；跨包行边全部指向更早包（T037 已移入 wp02）；`validate-tasks.py` 0 error | closed（repair commit `4808bd3f7`） |
| W3-02 | MEDIUM | **fixed** | `tasks.md:95` wp03 写域显式包含 `tests/fixtures/sdd-observer/failure_builder.py`（T023） | closed |
| W3-03 | MEDIUM | **open — superseded** | [P]/blocker 与并行叙事的三处矛盾仍在，但已按面重述为 **W3-12**（T026/T027）与 **W3-14**（T006/T018/T031/T032 缺 `[P]`、T004 缺 blocker） | 后继承接，不另立旧 ID 行 |
| W3-04 | HIGH | **fixed** | `tasks.md:11`/`:108`/`:98` 已改为按包一文一件（`notes/red-first-evidence-wp01/02/03.md`） | closed |
| W3-05 | MEDIUM | **open — superseded** | DoD-8 重测缺口仍在并扩大为 11 个计数 / token 前提，重述为 **W3-09**（HIGH，已 confirm） | 后继承接 |
| W3-06 | LOW | **open — carried over** | `tasks.md:168` 原文未变；V-14/15/18/19/20 仍无显式归属行 | 入主表（carried over） |

### Merge wave — cross-artifact serial pass（requirements ↔ plan ↔ tasks ↔ contracts；**0 条新 finding**）

**固定步（技能 §3，read-only）判定——phase-visible**：

- `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/096-sdd-observer-agent --corpus-root .specify/specs` → **`status: ok`，exit 0**（证据：`test-evidence/analyze-clause-coverage-round2.txt`）。读值：claimed clauses **58**；baseline 640 names，0 beyond baseline；`[fr-uncovered]` **23/23** FRs cited from citation groups；`[clause-unparsable]` 107 个既有语料文件无 clause id（1 个 positive-form parse doubt，语料级既有条件，非 096 特有，其余检查全 pass）；0 error / 1 warning。轮 1 的两条 blocking lane（4 beyond baseline + FR 0/23）均已清零 → **E-01 关闭**。
- `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/096-sdd-observer-agent` → **`status: ok`**，6 个 label 全 pass（0），5 records，0 error / 0 warning，`high=0`（证据：`test-evidence/analyze-decision-tensions-round2.txt`）。I pass 无 finding。

**跨波一致性复核注记（对既有行，不改变其评级）**：

1. **W1-08 ↔ W2-08（同 spec 双线前提）**：需求域（FR-003/FR-010/FR-021 未排除同 spec 双线）与 plan 域（V-19 / lifecycle C-05 / verification C-05 未写 distinct-spec 前提，仅 T-001 决策记录排除）指向同一未言明前提；两行均 open，保留双行（S1）。
2. **W1-15 ↔ W2-12（label 词汇）**：需求写作「执行 label / 实例 label」两读，plan 域 `run_stamp`/`run`/`R1` 三名并存；同一状态面词汇未收敛，两行均 open（S2）。
3. **W1-09 ↔ W2-14（缺口窗口边界）**：需求未裁决零长度窗口 / 连续缺口起点链 / disabled 起点回退；plan 引擎 C-08 的 no-entry 分支与 spine 节消歧仍未决；两行均 open，互证同一 lifecycle 面。
4. **W2-04 ↔ T017**：tasks 明确把 V-16/V-17 纳入 `check` 实现行（`tasks.md:168`），说明契约层的歧义读法已被下游采用——W2-04 的传播面已现实化，需在 plan 层收敛。
5. **W1-19 / W1-20 ↔ T037/T038**：tasks 只操作化「拒绝」分支（T037 的 second-writer exit-3）与弱代理（首行早于阶段完成），未实现「串行化」分支，也未证明「U2 派发前启动」——跨波证据支持 W1-19/W1-20 的收敛诉求。
6. **W1-21 ↔ tasks 红腿**：FR-018/019 由 T031/T032 的结构断言承接、FR-015 由 GATE-6/T009 承接、FR-021 由 T025 文本引用但无测试行；需求层 SC 缺失仍成立（W1-21），tasks 层仅有部分实质腿。
7. **W1-14 ↔ T032/T047**：A12 的「journal 不进阶段产物表」现有任务级红腿（T032 断言、T047 的 journal-format C-13 边界），但需求层仍无 FR 承载——W1-14 的规范义务缺口保持 MEDIUM。
8. **W2-01 ↔ quickstart/tasks 计数**：`quickstart.md:3` 称 "Seven"，章节实为 S-0…S-7（八节），`tasks.md:7`/T045 与 `plan.md` 三处均按八节——全局读法下 quickstart 头部是唯一离群点，支持 W2-01 的归属（`/speckit.plan`）。
9. **W3-11 ↔ requirements SC 文本**：SC → row trace 与行级 citation 的三处不一致为 tasks 内部记账问题；需求层 SC-001/SC-004/SC-006 文本本身不构成冲突，修复归属在 tasks。

**结论**：合并波未发现超出三波读域的新 CRITICAL/HIGH/MEDIUM/LOW finding（0 条），故不触发第二轮校验派发；跨制品一致性总账见下节。

---

## Cross-artifact consistency（合并波一致性总账）

### Coverage Summary

| 量 | 读值 | 来源 / 判定 |
|----|------|-------------|
| FR 定义 / SC 定义 | 23 / 7 | requirements.md 定义行 |
| FR → 任务文本覆盖 | 23/23 | W2/W3 复核（tasks.md 文本） |
| FR citation groups（条款体） | **23/23** | 固定步读值；轮 1 为 0/23 → **E-01 已关闭** |
| 契约条款 | 58 = 13+13+12+10+10 | 五页 `^## C-` 标题；与 plan / feature-ref / tasks 三处计数一致 |
| `[green:]` 认领 | **58/58 恰一次** | `validate-tasks.py` 0 `green-dangling` / 0 `green-clause-collision` |
| SC → row trace | 7/7 行齐全；3 处与行级 citation 不一致（SC-001 缺 T047、SC-004 多 T019、SC-006 缺 T024） | W3-11（open） |
| data-model 规则 → 任务 | V-1…V-13/V-16/V-17 → T017；V-14→T011/T037；V-19→T036/T037；V-18→T031/T019；V-20→T006/T017；V-15→T024（第二句无承接） | 合并波对照（W3-06 carried） |
| 任务行 / 包 | 47 行、4 包、分区 13+5+9+15=42+5；无缺号重号；行级无环 | W3 机器核对 |
| 覆盖门可执行性 | GATE-9/T047 现可过（fixed-step exit 0） | `analyze-clause-coverage-round2.txt` |
| 扫描语料 | 291 文件（解析 184 + named-unparseable 107） | 固定步；107 为语料级既有条件 |

### Feature Linkage Summary（G）

- **名称级（W1）**：`Related Feature` 声明 Feature ID `096` 与名称「SDD 专用观察者与线级观察记录（sdd-observer）」，与清单页眉一致；`.specify/features.md` 096 行与 `.specify/features/096.md` 均存在。
- **内容级 / 阶段记录义务（合并波）**：索引行 Status `Planned`、Last Updated `2026-11-10`、备注记录 plan 阶段落册（22 项宪法全 Pass、R-01–R-14、10 实体/20 规则、5 contracts/58 条款、8 场景、19 交付行）；详情文件 Status `Planned`、Last Updated `2026-11-10`。tasks 阶段的转场为「Maintain `Planned`」，同日日期即当前值；implement 阶段刷新由 T044 承接。**无 finding**（名称级 + 内容级均无 index/detail 漂移；日粒度下无可见滞后）。

### Constitution Alignment（D）

- **CRITICAL 1 条**：W3-07（Tasks 的 GATE-1 指示裸 `/tmp` 写入，违反宪法 XVII 所委托的临时目录纪律）。按技能 Constitution Authority，该 finding 不适用降级；校验波 confirm。
- 其余三波 D pass 均未发现宪法 MUST 冲突：W1 波 0；W2 波 0（rows I/VI/XV 为证据面弱化，非冲突）；W3 波其余 0。W1 round-2 复核 A5（journal 单文件 vs 并发纪律）、A10（Test-First Partial）、A12 均非宪法冲突。
- 层级提示：W3-10 为 tasks 内部规则矛盾（非宪法）；W3-08 的判级依据是 closed-set-claims 处置条（DoD/门承载 → HIGH），非宪法冲突。

### Checklist accountability（H，全量）

- `checklists/requirements.md`：12/12 已勾选，0 个未勾选 `[Gap]`。
- `checklists/2026-11-10-observer-requirements-quality.md`：38 项全部未勾选；`[Gap]` 7 项 = raised 6 + covered-by 1，`unraised=0 · undispositioned=0` → 阻断 **0**（明细见 W1 节）。
- 合计：`unchecked[Gap]=7 · 阻断=0`。

### Decision Tensions（I pass）

- 判定对象仅 `plan.md`：`## Decision Tensions` 在场、锚点正确、5 条记录（T-001…T-005）字段完整、cost 可映射；确定性程序 6 label 全 pass、0 error / 0 warning。**无 finding**。

### Unmapped Tasks / Do-not-flag 复核

- 未映射任务 0；47 行全部落在 story/package 归属。
- W2 的 duplication pass 判定 format facts 的重复属合法信息面（owner 持有拼写），不立 finding；`checklists/requirements.md` 的 245 行读值与当前 253 行的差异属带日期的阶段记录（clarify 前测量），按噪音控制不立 finding。
- `validate-tasks.py` 的 4 条 warning 均已在 § Green Attribution 披露；其中 T016→T024 的披露理由与实际子句对不符，已按 W3-15 立 LOW，不另作噪音豁免。

---

## Systemic observations（聚合观察，不提升任何单行评级）

- **S1 — 同 spec 双线前提缺口（W1-08, W2-08）**：需求与 plan/契约两侧仍未把「两条线解析到同一 spec 目录」写成显式前提或判定；状态同轮 1，**open**。
- **S2 — 状态词汇漂移（W2-02, W2-03, W1-15, W2-12）**：`settled` 无 spine 表示、`closed` vs `failed` 终态互斥未裁决、实例 label vs 执行 label、`run_stamp`/`run`/`R1` 三名并存——同一状态面词汇未收敛；**open**。
- **S3 — 验收判据与 FR 义务的间隙（W1-10, W1-19, W1-20, W1-21, W1-22；W1-02 已修复）**：轮 1 的 SC-001/SC-007 收束义务缺口已由修复关闭，但 SC-004(c) 定义、SC-005 二读、FR-005 谓词与 FR-006/015/018/019/021 红腿仍在需求层悬空；**re-formed**。
- **S4 — 包级并发与共享写面（W3-10, W3-12, W3-13, W3-14；W3-01/W3-02/W3-04/W2-06 已修复）**：轮 1 的包序死锁与共享 append-only sink 已关闭；剩余为 Foundational 阶段规则与行级 blocker 的局部矛盾、并行叙事与 `[P]` 标记漂移、US2 slice 行跨界包顺序；**narrowed, open**。
- **S5 — Constitution Check 证据面弱于声明（W2-09, W2-11；W2-10 已修复）**：per-clause FR 引用落地后 row I 证据已成立；rows VI / XV 仍超实况；**narrowed**。
- **S6 — 覆盖门与披露的自我矛盾（E-01）**：58/58 认领 + 条款级 FR 引用落地后，GATE-9/T047 按字面可通过；**resolved this round**。
- **S7 — 门禁文本的可执行性缺口（W3-07, W3-08, W3-09）**：本轮三行同指一个模式——tasks 的完成门自身不可执行或不可判定：GATE-1 越出临时目录纪律（CRITICAL）、DoD-6/GATE-8/T032 的包含性声明无基线指涉（HIGH）、DoD-8 无对应重测行（HIGH）。门禁文本与任务集之间的证据闭合是同一弱面；修复应按「门 → 行 → 证据」逐条配对，而非单点补丁。

---

## Metrics

- **检测**: 主表 findings 44（W1 20 · W2 12 · W3 12）；delta-only：fixed 7 · rejected 1（Appendix A）· superseded 2；上限 50 内，无 overflow。
- **评级（validated，主表）**: **CRITICAL 1 · HIGH 3 · MEDIUM 29 · LOW 11**；44 行。
- **校验波**: sent 4 · confirm 4 · downgrade 0 · reject 0；降级率 0/4，reject 率 0/4。
- **覆盖**: FR 23/23 任务文本覆盖；FR citation **23/23**（fixed-step）；clauses **58/58** claimed；SC 7/7 row trace（3 处 trace 不一致，W3-11）。
- **制品修改数**: 0；修复动作: 0（只读阶段）。
- **H pass**: `[Gap]` 7/7 处置，阻断 0。

## Rerun delta

**Resolved Since Last Run（7 条，逐条证据）**：

| Prior ID | R1 severity | Evidence that closed it |
|----------|-------------|--------------------------|
| W1-02 | HIGH | `requirements.md:137`（FR-009 终态收束写入义务）/:144（FR-013 窗口终点）/`:157`（FR-020 披露与写入互不替代）/SC-001 `:191`/SC-007 `:197`，与 lifecycle C-08（`:63-66`）对齐；W1 round-2 复核 fixed |
| W2-06 | MEDIUM | `tasks.md:87-100` Package Map 严格串行 wp01→wp02→wp03→wp04，WP-1 → WP-3 fixture 依赖落实为串行链（`plan.md:248` 措辞保持旧文，已披露、无下游影响） |
| W2-10 | LOW | 五页 58/58 条款体均载条款级 FR citation group（修复轮 E-01），`plan.md:42` row I 证据事实上成立 |
| W3-01 | HIGH | 包图重切：T037→wp02、T031/T032→wp04；跨包行边全部向后；`validate-tasks.py` 0 error |
| W3-02 | MEDIUM | `tasks.md:95` wp03 写域显式包含 `tests/fixtures/sdd-observer/failure_builder.py` |
| W3-04 | HIGH | `tasks.md:11`/`:108`/`:98`：red-first 证据按包一文一件（`notes/red-first-evidence-wp01/02/03.md`） |
| E-01 | HIGH | 固定步 `account-clause-coverage.py` → `status: ok` exit 0：58/58 claimed、FR 23/23、beyond-baseline 0（`test-evidence/analyze-clause-coverage-round2.txt`） |

**New Since Last Run（15 条）**：W1-19、W1-20、W1-21、W1-22；W3-07、W3-08、W3-09、W3-10、W3-11、W3-12、W3-13、W3-14、W3-15、W3-16、W3-17。

**Superseded（2 条，开放面由后继 ID 承接）**：W3-03 → W3-12 + W3-14；W3-05 → W3-09。

**Carried over（29 条，原 ID 保留）**：W1-01、W1-04…W1-18（16）；W2-01…W2-05、W2-07…W2-09、W2-11…W2-14（12）；W3-06（1）。

**Headline（双向陈述）**：轮 1 的 4 条 HIGH + 1 条被拒 + 1 条降级积压已全部处置（4 fixed / 1 rejected / 0 遗留 HIGH）；但本轮重扫**不是 clean rerun**——新增 1 CRITICAL + 3 HIGH 全部 confirm。**「清空的旧账」与「干净的重跑」是不同声明，本报告两者分列**。

---

## Appendix A — Rejected findings（轮 1 校验拒绝；维持，不静默丢弃）

| ID | 原 Severity | Verdict | 保留理由 |
|----|-------------|---------|----------|
| W1-03 | HIGH | reject（轮 1 校验波） | 下游制品（`tasks.md:110` T003、`:212` T033、`:22` DoD-6、`plan.md:126` T-005）已把 SC-006 基线落到具名持久路径 `test-evidence/digest-fieldset-baseline.txt`，并给出可复跑采集命令与比较单元；requirements 文本未内联路径属表述性省略。W1 round-2 复核维持 rejected、不重报。原始证据边界见 `test-evidence/analyze-validation-wave.txt`「W1-03」块。 |

## Anomaly

`ANOMALY: none` —— 无未处置异常；无 in-passing repair（只读阶段，未触碰制品）。固定步本轮 `status: ok`（轮 1 的 phase-visible `uncovered` 已由修复关闭）；`[clause-unparsable] 107` 为语料级既有条件，已在固定步输出中照实呈现，非静默吸收。C/H finding 仍在（W3-07/08/09/10），按任务要求照常出报告、不修复。
