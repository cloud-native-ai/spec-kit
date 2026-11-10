# Analyze — Merged Report（096-sdd-observer-agent）

- **Line / Run**: `096-sdd-observer-agent` / `r20261110T081104Z-b096`
- **Stage**: analyze（串行集成者；三路并发检测波 W1/W2/W3 + 合并波）
- **Round**: 1（首轮；`test-evidence/` 下无既有 `analyze-merged-*`，无 rerun delta）
- **Date**: 2026-11-10
- **Authority**: `.specify/skills/internal/analyze-artifacts/SKILL.md` + `references/detection-and-severity.md` + `references/validation-and-report.md`；`.specify/constitution.md`（v1.19.0）
- **Read domain（合并波）**: `requirements.md`、`plan.md`、`tasks.md`、`research.md`、`data-model.md`、`quickstart.md`、`feature-ref.md`、`contracts/`（5 页 58 条款）、`checklists/`（2 份）、`.specify/features.md` 096 行、`.specify/features/096.md`、`coverage-baseline.txt`、`AGENTS.md`、宪法
- **Write surface**: 本文件 + `test-evidence/analyze-{clause-coverage,decision-tensions,validation-wave}.txt` + Wrap-up 记账；未修改任何 spec 制品，未执行任何修复（只读阶段）
- **Merge protocol（确定性归并）**: 分节 W1→W2→W3（本节 + 合并波新行）；各节内按 ID 字典序；跨波重复 ID 检查 **0 条**（`W1-*` / `W2-*` / `W3-*` / `E-*` 前缀互斥），「先声明先得 + 指针」规则本轮无触发。W1/W2/W3 表格按原文逐字保留，不重写、不重评级（C/H 校验结果以「Validation annotations」小节与 § Validation wave 为准）。
- **C/H 校验**: 6 条 CRITICAL/HIGH 候选由 6 个独立只读外部 worker 并行校验（Recipe 7 载体；`qodercli -p`，只读工具白名单 `Read Grep Glob Bash`，`--no-session-persistence`，一节一 finding、互不可见）；波后 `git status --porcelain` 与波前一致（无 validator 写入）。结果：confirm 4 · downgrade 1 · reject 1（降级率 1/6）。

---

## Top summary — C/H count and per-item pointers（不修复）

**CRITICAL: 0**（三波 D pass 均未发现宪法 MUST 冲突；合并波复核一致）

**HIGH（validated，4 条）**：

| ID | Category | Severity（validated） | Anchor（逐条指针） | Fact pointer（一句话） |
|----|----------|----------------------|--------------------|------------------------|
| W1-02 | F inconsistency / acceptance | HIGH（confirm） | `requirements.md:191`; `:197`; `:137`; `:144`; `:146`; `:111` | SC-001/SC-007 的失败线覆盖与缺口披露判据，缺少被 FR 支撑的收束缺口写入义务（约束边界见 § Validation wave） |
| W3-01 | inconsistency（包级顺序） | HIGH（confirm） | `tasks.md:89-100`; `:232`; `:337` | wp01 的 T037 被 wp02 的 T020 阻塞，三种顺序声明无一种能同时成立（静态文档不一致，非已观测死锁） |
| W3-04 | concurrency-safety（项目指令冲突） | HIGH（confirm） | `tasks.md:11`; `:108`; `:369`; `AGENTS.md` § Concurrent Development Safety | 全部 red-first 证据追加到单一 `notes/red-first-evidence.md`，而写入行分属三个可并发执行的包 —— 违反「记录类数据一文一件」MUST |
| E-01 | E coverage / F inconsistency | HIGH（confirm，合并波新发现） | `tasks.md:38`; `:254`; `:354-365`; `contracts/*.md` 页级 `Requirements:` 行 | GATE-9/T047 要求覆盖率脚本退出 0，但 § Green Attribution 刻意保留 4 个未认领条款、且条款体无 FR citation group —— 该完成门按字面无法通过（实测 exit 1） |

**Severity distribution（validated，主表）**: CRITICAL 0 · HIGH 4 · MEDIUM 26 · LOW 8 —— 主表 38 行；另有 1 条 HIGH 被 reject 移入 **Appendix A**（W1-03，不静默丢弃）。检测总量 39 行（≤50 上限，无 overflow）。

**MEDIUM/LOW 不改门**（技能语义）：按 `validation-and-report.md` § Next actions，LOW/MEDIUM only 可继续，建议随对应入口修复。

---

## Validation wave（C/H，独立只读）

- **Carrier**: subprocess 载体（Recipe 7）——每 finding 一个独立 `qodercli` 子进程，只读工具白名单、`--no-session-persistence`；brief 只含 finding（id / category / claim / severity）+ evidence locations，不含检测推理、不含其他 findings；检测者与校验者不相交。
- **Read-only proof**: 波后 `git status --porcelain` 与波前一致——无 validator 写文件；`.specify/.tmp/`（scratch）与 `.specify/agents/execution/logs` 类均为被忽略路径。
- **Downgrade rate**: sent 6 · confirm 4 · downgrade 1 · reject 1 → 降级率 **1/6 ≈ 16.7%**，reject 率 1/6。仅 1 条降级说明检测波总体未系统性高估，但 W1-01 的初评 HIGH 确属传播面误判（见其边界）。

| Finding | Sent | Verdict | Final severity |
|---------|------|---------|----------------|
| W1-01 | HIGH | downgrade | MEDIUM `(validated: downgraded)` |
| W1-02 | HIGH | confirm | HIGH |
| W1-03 | HIGH | reject | — → Appendix A |
| W3-01 | HIGH | confirm | HIGH |
| W3-04 | HIGH | confirm | HIGH |
| E-01 | HIGH | confirm | HIGH |

### Validator evidence boundaries（verbatim）

**W1-01 — verdict: downgrade / proposed_severity: MEDIUM**

```
evidence_supported: requirements.md:142 (FR-011) states entries carry exactly nine information classes and enumerates nine fields; requirements.md:181 (Key Entities) says the same Journal Entry carries eight; checklists/2026-11-10-observer-requirements-quality.md:72 records the 八/九 contradiction (CHK018), and CHK018 at line 36 remains unchecked — so "same artifact, two counts on one closed field set, recorded but unconverged" is substantiated. requirements.md:234 additionally records the clarified decision as nine, confirming :181 is a stale count.
evidence_not_supported: The HIGH severity is not substantiated: no downstream artifact inherits the eight-count — plan.md:14, data-model.md:55/146/155, contracts/journal-format.contract.md:19 and tasks.md:133/135/139 all carry nine fields/columns consistent with FR-011 — so under the analyze-artifacts severity rule (propagation surface `none` → capped at MEDIUM; 071 analyze-report:50 precedent) this is a stale-summary/terminology defect, not a propagating conflicting requirement. I could not observe any current artifact outside requirements.md:181 that states eight.
```

**W1-02 — verdict: confirm**

```
evidence_supported: requirements.md:191 makes failure-line coverage depend on `observer-gap` naming for stages lacking start entries; :197 requires the next observer execution or line close-out to output an `observer-gap` entry naming window start/end; :137 (FR-009) permits a state-spine reason to replace the journal close-out entry; :144 (FR-013) defines gap end by the next execution's first entry, presupposing a subsequent execution and naming no close-out writer; :146 (FR-015) authorizes only the observer Execution to write via the engine; :111 permits no journal at all when the line fails before observer start; and :157 (FR-020) caps the close-out obligation at disclosure satisfied by one recorded reason. Together these substantiate that the failure-line acceptance criteria require journal artifacts no FR obligates anyone to write at close-out.
evidence_not_supported: SC-001:191 does not literally require every stage to be named by `observer-gap` — it is a disjunction with stage-start entries (gap naming is mandatory only for unobserved stages); SC-007:197 says the next observer execution *or* close-out must output the gap entry, so close-out is the fallback, not an unconditional duty. The claim also asserts absence of an FR-backed writing obligation only within requirements.md — whether plan-stage or driver-skill text later assigns a close-out writer was not examined.
```

**W1-03 — verdict: reject（→ Appendix A）**

```
evidence_supported: requirements.md:196 matches the quoted claim verbatim — SC-006 is a containment claim over a machine-produced surface (`/speckit.status` digest field set, empty allowed-delta set "零新增字段、行与小节") anchored to "本特性第一个实现提交之前的一次实测采集"; and requirements.md:206 (SC-006 Source) names only a "前后对比记录（零新增）" with no file path or capture command, so within requirements.md alone the baseline is not pinned to a persisted artifact or spelled-out procedure.
evidence_not_supported: The categorical assertions "无持久位置"、"无复现采集规则"、"验收不可复现" are contradicted by artifacts that pre-date the analysis (tasks.md mtime 17:09; findings 17:28): tasks.md:110 (T003) captures the SC-006 baseline into the fixed path `.specify/specs/096-sdd-observer-agent/test-evidence/digest-fieldset-baseline.txt` via the re-runnable command `python3 scripts/python/status-digest.py --action digest --format json --workspace .` with a declared comparison unit (sorted top-level keys plus `all_entries[]` row keys, timestamps/ages excluded); tasks.md:212 (T033) re-captures with the same command and compares against that file; tasks.md:22 (DoD-6) makes the empty delta against that file a completion gate; plan.md:126 (T-005) names the same baseline-vs-post reading as the binary discriminating evidence; the command and options exist (scripts/python/status-digest.py:2279-2282). Per `.specify/shared/guidelines/closed-set-claims.md` element 1 the baseline referent/acquisition is named, so the claim is not void, and the do-not-flag entry in `.specify/skills/internal/analyze-artifacts/references/detection-and-severity.md` treats a containment claim naming its baseline referent and comparison unit as legitimate — so the HIGH "untestable acceptance criterion" rationale fails. Only the narrow observation that the SC/SC-Source text does not inline the path or command survives, which is a presentational omission, not a non-reproducible acceptance.
```

**W3-01 — verdict: confirm**

```
evidence_supported: tasks.md:93-94 assigns T037 to wp01-journal-core (rows T006–T017, T036–T037) and T020 to wp02-observer-definition (rows T018–T020, T031, T038); wp01's Edge cell "after Setup + Foundational" records no wp02/T020 predecessor. tasks.md:232 records T037 [blockedBy: T020,T036], a hard cross-package dependency from a wp01 row onto a wp02 row, and tasks.md:267-268 confirms the row intent ("US5 … after US2's template (T020)"). tasks.md:100 declares wp01 → wp02 → wp03 → wp04, permits only wp02/wp03 concurrency "after wp01", and names "the one forward edge" as T031→T029, omitting T037→T020; tasks.md:337 repeats the same "wp01 first" strategy. Hence the two narrative orderings cannot be executed literally (wp01 must finish before wp02 begins, yet T037 needs T020), and the Edge column fails to record the wp01←wp02 edge that line 89 says is package-edge territory: the three declarations plus row-level blockedBy are mutually unsatisfiable.
evidence_not_supported: No observed execution deadlock — this is a static document inconsistency, and "按字面执行会死锁" is a derivation, not a recorded event. The Edge column taken alone does not deadlock ("wp02 after T006" permits wp02 to start concurrently with wp01), so "none can hold" holds only at the set level, not as "each of the three is individually impossible." I did not check plan.md or other planning artifacts for an override of this package map; the verdict is bounded to the cited tasks.md locations.
```

**W3-04 — verdict: confirm**

```
evidence_supported: tasks.md:11 directs all red-first captures into the single `.specify/specs/096-sdd-observer-agent/notes/red-first-evidence.md`; tasks.md:108 (T001) creates exactly that one file with per-run entries inside it; tasks.md:139/162/163/187/232 (T008, T016, T037; T018; T024) append red runs to that same file, and the package map tasks.md:93-95 assigns T008/T016/T037 to wp01, T018 to wp02, T024 to wp03; tasks.md:100 explicitly permits wp02 and wp03 to run concurrently, while tasks.md:98 acknowledges `notes/` is an append-only sink shared by several packages. AGENTS.md:101-108 makes per-entry files a MUST for append-only observations including "evidence" and states the exact test: two simultaneous writers on one path means the layout is wrong. The file is tracked (not git-ignored), so both branch-level and same-worktree agent-flow concurrency apply. The claim as stated is fully supported.
evidence_not_supported: The cited artifacts establish a design-level violation, not an observed one: they show wp02/wp03 MAY run concurrently (permission, not a guaranteed schedule), and no actual merge conflict, lost append or race outcome is recorded anywhere cited. "All red-first evidence" is supported by the global directive at tasks.md:11, but only five rows name the file explicitly, so other captures are covered by the directive rather than by row-level evidence. It is also not shown whether implement-stage dispatch will use separate worktrees/branches or a shared worktree; both fall under the rule's "parallel branches and agent flows" wording, but the actual execution topology is not in evidence. The classification of a human-readable markdown evidence note as a "machine-managed store" is an interpretive step, though the rule's own enumeration of "evidence" supports it.
```

**E-01 — verdict: confirm**

```
evidence_supported: GATE-9 (tasks.md:38) and T047 (tasks.md:254) require `account-clause-coverage.py` exit 0 with 0 uncovered names beyond `coverage-baseline.txt`. § Green Attribution (tasks.md:354-363) deliberately leaves exactly four clauses unclaimed (`observer-role.contract.md#C-01`, `observer-verification.contract.md#C-03`, `#C-05`, `#C-07`), and those names never appear as `[green:]` claims elsewhere in tasks.md. The re-run accountant exits 1 and prints exactly those four names as `BEYOND-BASELINE`; the baseline header (coverage-baseline.txt:2) and the script's freeze logic (account-clause-coverage.py:311-313) show this spec's own clauses can never be baseline-exempted. All five contract pages cite FRs only on the page-level `Requirements:` line (line 3), clause bodies carry zero `(FR-nnn)` parentheticals, and `clause_citations` over the five files yields 0 FR-bearing groups across 58 clauses; the accountant reports 0 of 23 FRs claimed, a blocking condition independent of the clause lane (account-clause-coverage.py:357). Thus, on the artifacts as checked out, GATE-9/T047 cannot pass.
evidence_not_supported: The claim does not name a repair row, and none exists — tasks.md contains no task that would add FR citation groups to clause bodies (T005 re-freezes a baseline that excludes this spec; T047 is the gate itself), so the confirmation covers the current artifact set only; whether a future revision of tasks.md or the five contracts could make the gate pass is outside the cited evidence. The run also fails an additional `clause-unparsable` check (107 named files, 1 positive-form parse doubt) and emits 1 warning, which the claim does not mention and which are not needed for its conclusion.
```

---

## Merged findings

### Wave W1 — requirements + checklists（18 rows；读域 `requirements.md` + `checklists/2026-11-10-observer-requirements-quality.md`）

Passes: A/B/C/D/F/G(名称级)/H；E（跨制品覆盖）与 I（decision tension）延期至合并波。Severity basis：每行记录 propagation surface，无 `none` 行（W1-01 的 `none` 判定由校验波更正，见上）。

| ID | Severity | Pass | Anchor | Fact（一句话事实） | Propagation | Suggested disposition（指针） |
|----|----------|------|--------|--------------------|-------------|------------------------------|
| W1-01 | MEDIUM `(validated: downgraded)` | F inconsistency | `requirements.md:181`; `requirements.md:142`; `checklist.md:72` | FR-011 规定条目恰好承载九类信息，而 Key Entities 的 Journal Entry 定义称「承载八类信息」；同一制品对同一封闭字段集给出两个计数，清单已记录该矛盾但未收敛。 | none（计划 / 数据模型 / 契约 / 任务均为九类，实测） | `/speckit.requirements`（Key Entities 改为九类并引用 FR-011） |
| W1-02 | HIGH `(validated: confirm)` | F inconsistency / acceptance | `requirements.md:191`; `requirements.md:197`; `requirements.md:137`; `requirements.md:144`; `requirements.md:146`; `requirements.md:111` | SC-001 的失败线判据要求「每阶段被 `observer-gap` 点名」、SC-007 要求线收束必须输出 `observer-gap` 条目，但 FR-009 允许以状态脊原因替代 journal 收尾，FR-013/FR-015 未指名收束时缺口条目的写入者，且 Edge Cases 允许 observer 启动前失败时无 journal——失败线的覆盖判据缺少被 FR 支撑的写入义务。 | plan 收束设计 / tasks / 验收测试 | `/speckit.clarify`（指名收束缺口写入者，或改写 SC-001/SC-007 与 FR-009 对齐） |
| W1-03 | ~~HIGH~~ → Appendix A（reject） | F containment claim | `requirements.md:196`; `requirements.md:206` | SC-006 以「本特性第一个实现提交之前的一次实测采集」为基线断言字段集零增量，但该基线无持久位置、无复现采集规则，属缺少具名基线指涉的 containment claim，验收不可复现。 | — | 见 Appendix A（下游 T003/T033/DoD-6/plan T-005 已具名基线与采集命令，校验判定 reject） |
| W1-04 | MEDIUM | C underspecification | `requirements.md:129` | FR-004 以 `line_id + spec key` 派生实例身份，但全文未定义 spec key 的派生来源与唯一性范围，身份函数不可求值，SC-005 的「两个不同实例身份」缺少可判定的身份函数。 | plan 身份模型 / driver 修订 / 测试 | `/speckit.clarify`（定义 spec key 的派生与 owner） |
| W1-05 | MEDIUM | C underspecification | `requirements.md:160` | FR-023 规定入口声明键 `observer: on|off`，但「入口声明」的载体、位置、解析格式与 owner 均未定义，关闭开关无法被实现方无歧义解析。 | driver U0 解析 / plan | `/speckit.clarify`（绑定入口声明载体与解析规则） |
| W1-06 | MEDIUM | C underspecification | `requirements.md:145`; `requirements.md:192` | FR-014 要求证据指针携带「留存类别」并在线收束时可解析，SC-002 以「可解析」为验收判据，但留存类别词表与「可解析」的判定（存在 / 类型 / 版本历史可达）未定义为封闭集合，且未覆盖工作树清理后的时点。 | plan checker / 测试夹具 | `/speckit.clarify`（留存类别封闭词表 + 可解析判定） |
| W1-07 | MEDIUM | F inconsistency | `requirements.md:135`; `requirements.md:136` | FR-007 规定上一执行 `.status` 未结算时 driver MUST NOT 派发下一个，FR-008 又允许失败 / 停滞 / 窗口到期后在阶段边界重启；执行崩溃且未留下 `.status` 时既未结算又已结束，两条规则互斥，重启路径被串行规则封死。 | driver 派发逻辑 / plan | `/speckit.clarify`（裁定未结算执行的结算或超时规则） |
| W1-08 | MEDIUM | F inconsistency | `requirements.md:128`; `requirements.md:141`; `requirements.md:158` | FR-003 禁止不同线共享 journal、FR-010 按 spec 目录落一份 journal，但 FR-021 未排除两条线（含嵌套运行）解析到同一 spec 目录的情形，该状态下路径冲突且「不共享」无法成立。 | plan 路径模型 / 双线夹具 | `/speckit.clarify`（排除或消歧同 spec 双线状态） |
| W1-09 | MEDIUM | C underspecification | `requirements.md:144`; `requirements.md:160` | FR-013 的缺口窗口推导未裁决三种边界：零长度窗口（起止同秒）写入还是抑制、连续多个缺口的起点链、以及 `state=disabled` 无启动时间时的起点回退值。 | plan 缺口写入 / checker / 测试 | `/speckit.clarify`（缺口窗口边界裁决） |
| W1-10 | MEDIUM | B ambiguity | `requirements.md:194`; `requirements.md:52` | SC-004(c) 要求 checker 拒绝「自由叙述条目」，但需求层未给出「自由叙述」的结构定义，反例构造只能回落到 checker 自身判定，存在循环判据风险。 | plan 客观性夹具 / checker | `/speckit.clarify`（自由叙述的结构定义） |
| W1-11 | MEDIUM | B ambiguity | `requirements.md:142`; `requirements.md:144` | FR-011 的 `命令` 字段允许「原文或 `-`」，但原文取自哪个载体、字符集 / 长度如何约束均未定义，评价或建议文本可借这个自由文本字段进入条目，与 FR-013 的客观性构造冲突。 | plan journal 格式 owner / driver | `/speckit.clarify`（命令字段的来源与内容约束） |
| W1-12 | MEDIUM | B ambiguity | `requirements.md:144` | FR-013 以「限定为」引出观测输入清单，但未声明该清单是否穷尽、也未指名新增载体的 owner，其他制品引入的 meta 包络是否可读不可判定。 | plan 读域实现 / 定义文本 | `/speckit.clarify` + `/speckit.plan`（封闭清单与扩展 owner） |
| W1-13 | MEDIUM | C underspecification | `requirements.md:150`; `requirements.md:88` | FR-016 把写面界定为 journal 与「自身执行运行产物」（按既有布局引用），但 US4 AS1 要求审计实际写面时，锁文件 / 游标 / 临时文件是否计入写面没有测量规则，单写者协议所需锁文件的位置也未裁定。 | plan 写面声明 / tasks | `/speckit.plan`（写面枚举与审计规则） |
| W1-14 | MEDIUM | E coverage gap | `requirements.md:252` | 「journal MUST NOT 被加入任何阶段 required artifact 集或 `STAGE_ARTIFACTS` 映射」只存在于 Assumptions A12，既无 FR 承载也无带红腿的 SC，规范义务挂在假设上。 | plan / tasks（红腿） | `/speckit.requirements`（提升为 FR）→ `/speckit.tasks` |
| W1-15 | MEDIUM | F inconsistency | `requirements.md:129`; `requirements.md:141`; `requirements.md:234` | FR-004 说身份四元组以「执行 label」记入 journal 头部，FR-010 与 clarify 记录却写「实例 label」；journal 跨多次执行只有一份头部，而派发 label 每次执行不同，头部字段语义悬空。 | plan 头部 schema / 模板 | `/speckit.clarify`（头部 label 字段定名与取值） |
| W1-16 | LOW | H completeness | `requirements.md:126` | FR-001 的 MUST NOT 覆盖 stage executor / reviewer / reporter 三个席位，但这三个角色面没有指向定义 owner 的引用，三条禁令无法按同一谓词独立核对。 | 定义文本 | `/speckit.requirements`（补 owner 引用） |
| W1-17 | LOW | A duplication | `requirements.md:141`; `requirements.md:144`; `requirements.md:191`; `requirements.md:194`; `requirements.md:197`; `requirements.md:217` | FR-010、FR-013、SC-001、SC-004、SC-007 在 `[[STR-00N]]` 标记旁同时复制了字面量，违反本制品自设的「用 `[[STR-NNN]]` 代替复制字面量」约定。 | requirements 文本 | `/speckit.requirements`（仅保留 token） |
| W1-18 | LOW | B ambiguity | `requirements.md:113`; `requirements.md:142` | Edge Cases 称「checker 以文件序判定非递减」但未点名判定对象（序号还是观测时间），而 FR-011 要求序号单调递增，checker 判定谓词存在两种读法。 | plan checker | `/speckit.clarify` 或 `/speckit.plan`（点名判定对象） |

**Checklist Accountability（W1 处置，机器可读行）**

| CHK | Anchor | Disposition |
|-----|--------|-------------|
| CHK002 | `checklist.md:14` | raised-as-finding W1-04 |
| CHK003 | `checklist.md:15` | raised-as-finding W1-05 |
| CHK004 | `checklist.md:16` | raised-as-finding W1-13 |
| CHK005 | `checklist.md:17` | raised-as-finding W1-06 |
| CHK008 | `checklist.md:20` | covered-by requirements.md § FR-001 |
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

`unchecked[Gap]=7 · raised=6 · covered-by=1 · unraised=0 · undispositioned=0` → 阻断计数 **0**。未带 `[Gap]` 的其余 31 个未勾选项属质量问句，其材料性缺陷已由 W1-01…W1-18 按锚点吸收（如 CHK011→W1-07、CHK013→W1-11、CHK014→W1-10、CHK017/CHK019→W1-09、CHK020/CHK021→W1-08、CHK027→W1-03〔reject，见附录〕、CHK038→W1-04）；其余项在 requirements 文本中已有可引用答复，不另立 finding。

### Wave W2 — plan block（14 rows；读域 `plan.md`、`data-model.md`、`quickstart.md`、`feature-ref.md`、`research.md`、`contracts/` 5 页）

Same-author gate 不适用（制品由前序阶段会话产出，本波 fresh context）。Total: 14 findings — CRITICAL 0 · HIGH 0 · MEDIUM 10 · LOW 4。无制品修改。

| ID | Severity | Anchor | Fact (one sentence) | Suggested attribution |
|----|----------|--------|---------------------|-----------------------|
| W2-01 | MEDIUM | `quickstart.md:3` (cf. `plan.md:31`, `plan.md:139`, `plan.md:236`) | `quickstart.md` announces "Seven walk-through scenarios" but contains S-0…S-7 (eight sections), while `plan.md` counts 8 scenarios (S-0…S-7) in three places. | `/speckit.plan` — `quickstart.md`（对齐计数，或将 S-0 明确为 pre-check 不计入 scenario） |
| W2-02 | MEDIUM | `data-model.md:36` vs `data-model.md:127` | E-3 declares execution states `started → settled \| failed` and says they are recorded in the E-9 spine section, but E-9's closed `state` domain is `started \| failed \| disabled \| closed` — `settled` has no spine representation, so a non-terminal settled execution's spine record is undefined. | `/speckit.plan` — data-model E-3/E-9（补 `settled` 值，或明确映射到 `closed`/triplet `.status`） |
| W2-03 | MEDIUM | `data-model.md:137` vs `contracts/observer-lifecycle.contract.md:49` | On final-execution failure, E-9 says the driver writes `state=closed` (with the reason) after the final execution fails, while lifecycle C-08 says the driver records `state: failed` plus the reason — the terminal spine state is contradictory. | `/speckit.plan` — E-9 与 lifecycle C-08（择一终态规则；若 closed 覆盖 failed，须写明顺序） |
| W2-04 | MEDIUM | `contracts/journal-engine.contract.md:39` (cf. `:31`, `data-model.md:160-161`, `quickstart.md:59`) | `check` is required to validate V-16/V-17, but V-16 is an append-time execution-label identity refusal (C-07) and `check` receives only `--spec-dir`/`--repo` — no execution label or spine input — so V-16 cannot be discharged as written; `quickstart.md` S-3 repeats the V-1…V-13-only reading. | `/speckit.plan` — journal-engine C-09 与 V-16/V-17 归属（V-16 归 append；check 补 spine 输入或移除 V-17） |
| W2-05 | MEDIUM | `feature-ref.md:18-40` (cf. `:75`, `:77`) | The Delivered paths table's FR column never cites FR-019 or FR-021, although the FR → Contract map lists both, so 2 of 23 FRs have no delivered-path attribution. | `/speckit.plan` — feature-ref delivered-paths 表（补行归属，或注明经哪一行间接交付） |
| W2-06 | MEDIUM | `plan.md:248` (cf. `plan.md:243-245`, `feature-ref.md:33`, `:37`, `quickstart.md:83`) | WP-3's `test_sdd_observer_lifecycle.py` needs the start-failure / mid-run-kill failure builder that WP-1 owns in `tests/fixtures/sdd-observer/`, but the dependency note claims only pairwise write-domain disjointness and states no WP-1 → WP-3 ordering. | `/speckit.tasks` — 在 tasks.md 记录该 fixture 依赖（并修正 plan 的依赖句） |
| W2-07 | MEDIUM | `data-model.md:80-99` (E-6) + `contracts/journal-engine.contract.md:19`, `:23` | E-6 names each event's primary carrier but no rule maps carrier fields to the nine entry columns per event class, and C-05's "natural keys" for the idempotency identity are undefined — the claimed deterministic projection is not decidable from the read-domain artifacts. | `/speckit.plan` — data-model E-6 / journal-engine C-04/C-05（补 per-event 投影表并定义 identity keys） |
| W2-08 | MEDIUM | `data-model.md:163` (cf. `contracts/observer-lifecycle.contract.md:37`, `plan.md:76-84`, `contracts/observer-verification.contract.md:23`) | V-19 claims two parallel lines' journals "never share a path", but the path is derived from the spec key and the dual-line fixture uses two distinct spec dirs — the plan only excludes same-spec two-line work by T-001 decision, a precondition V-19/C-05 and the fixture do not state. | `/speckit.plan` — V-19 / lifecycle C-05 / observer-verification C-05（写明 distinct-spec 前提，或补 same-spec 判定） |
| W2-09 | MEDIUM | `plan.md:56` | Constitution Check row XV's evidence claims the quickstart "defines journal / observer / gap at first use", but `quickstart.md` contains no such definitions — the terms are used bare in S-1/S-2/S-5. | `/speckit.plan` — `quickstart.md`（补 first-use 定义）或修正 row XV 证据 |
| W2-14 | MEDIUM | `data-model.md:116` (E-8) + `contracts/journal-engine.contract.md:35` (C-08) | E-8 defines a gap window start from "the spine observer record section's `started_at`" when no entry exists, but C-08 only appends a gap when a previous entry exists and does not say which spine section's `started_at` to use — the start-failure/no-entry gap is unreachable or ambiguous. | `/speckit.plan` — E-8/C-08（补 no-entry 分支并消歧 spine section） |
| W2-10 | LOW | `plan.md:42` | Row I's evidence says "Every contract clause cites an FR", but the five contract pages cite FRs only in their page-level `Requirements:` lines; no individual C-NN clause body carries an FR reference. | `/speckit.plan` — 将 row I 证据改写为 page-level scope，或补 per-clause FR tag |
| W2-11 | LOW | `plan.md:47` | Row VI's evidence says every row carries a "resolvable pointer", but E-7 permits runtime pointers to cleaned-up files and E-6 gives `observer-error` `min_persistent: 0` — a row may carry only a runtime pointer that no longer resolves. | `/speckit.plan` — 改写 row VI 证据（persistent 指针须解析；runtime 指针仅标记） |
| W2-12 | LOW | `data-model.md:33` (cf. `research.md:28`, `quickstart.md:34`, `plan.md:195`) | The observer execution label's middle segment is named `run_stamp` in the data model and research, `run` in plan EP-007, and shown as the run id (`R1`) in the quickstart, with no mapping rule between the three names. | `/speckit.plan` — data-model E-3 / research R-03（统一 token 名并定义，示例对齐） |
| W2-13 | LOW | `contracts/journal-engine.contract.md:15` | C-03 calls `--settle` / `--final` "mutually exclusive semantics" but never states whether the flags may be combined or whether `--final` alone implies the `observer-settle` write it describes. | `/speckit.plan` — journal-engine C-03（写明互斥规则与 `--final` 单独语义） |

### Wave W3 — tasks.md（6 rows；读域仅 `tasks.md`）

W3-01、W3-04 的 HIGH 由校验波确认（见上）；本波未自证。

| ID | Category | Severity | Anchor | 一句话事实 | 建议归属（指针） |
|----|----------|----------|--------|------------|------------------|
| W3-01 | inconsistency（包级顺序） | HIGH `(validated: confirm)` | `.specify/specs/096-sdd-observer-agent/tasks.md:89-100,232,337` | 包序声明 wp01 先于 wp02，但 wp01 内的 T037 被 wp02 内的 T020 阻塞，且 package 表 Edge 列未记这条反向边，三种顺序声明（Edge 列 / Declared integration order / Parallel Team Strategy）无一种能同时成立，按字面执行会死锁。 | `tasks.md` § Package Map / § Declared integration order / § Parallel Team Strategy（经 `/speckit.tasks` 收敛；优先复核 T037 的 blocker 或其包归属） |
| W3-02 | inconsistency（写域领地） | MEDIUM | `.specify/specs/096-sdd-observer-agent/tasks.md:93,95,98,186` | T023 属 wp03，却写 `tests/fixtures/sdd-observer/failure_builder.py`——该路径位于 wp01 声明的 owned 目录内、且不在 wp03 的 write domain 中，与 § Package Map 的互斥领地声明不符。 | `tasks.md` § Package Map（wp03 写域补路径，或 T023 改归 wp01） |
| W3-03 | inconsistency（并行标记） | MEDIUM | `.specify/specs/096-sdd-observer-agent/tasks.md:111,124,163,193,288-293` | § Parallel Opportunities / Parallel Example 宣称 T006、T018、T027 可并行（并称 T004 在 T001 之后），但对应行分别是无 `[P]`、无 `[P]`、`blockedBy: T026`、无 blocker，指引与行级标记相互矛盾。 | `tasks.md` 对应任务行的 `[P]` / `[blockedBy:]` 标记，或 § Parallel Opportunities 文本 |
| W3-04 | concurrency-safety（项目指令冲突） | HIGH `(validated: confirm)` | `.specify/specs/096-sdd-observer-agent/tasks.md:11,108,369` | 所有 red-first 证据都追加到单一 `notes/red-first-evidence.md`，而写入行分属 wp01、wp02、wp03 且 wp02/wp03 被允许并发执行，违反 `AGENTS.md` § Concurrent Development Safety 的“记录类数据一文一件、不得共享可变聚合”MUST。 | T001（落地路径改为每条记录一文件，或按包/时间戳分文件）；本波只读，不修复 |
| W3-05 | coverage-gap（DoD） | MEDIUM | `.specify/specs/096-sdd-observer-agent/tasks.md:24,66-85,109-111` | DoD-8 要求 § Premises 的 14 个生成期量在 implement entry 全部重测，但无任何任务行承担该重测（T002 只重取三个测试基线，T004 只重探环境），DoD 与任务覆盖之间存在缺口。 | DoD-8 / Setup 行 T002–T004（补一条 premise 重测行或把 DoD-8 的 owner 显式落到 implement Step 0） |
| W3-06 | underspecification（可追溯性） | LOW | `.specify/specs/096-sdd-observer-agent/tasks.md:168` | T017 只枚举 data-model 的 V-1…V-13 与 V-16/V-17，V-14、V-15、V-18、V-19、V-20 在 tasks.md 全文无任何归属行，五条规则的覆盖不可追溯。 | T017 的检查范围，或 data-model → task 映射（本波读域不含 data-model.md，需聚合波对照确认） |

W3 机器核对摘要（原文）：任务行 47 条（T001–T047 唯一）；`[blockedBy:]` 0 未知目标 / 0 自环，行级依赖图无环；`[green:]` 54 条、0 碰撞（与 header 的 58 子句 − 4 条已披露未认领相符）；包分区 14+5+10+13=42 打包行 + 5 Setup 行 = 47；跨包行级依赖 T031←T029、T032←T020、T037←T020、T018←T006、T033←T003；FR 23/23、SC 7/7 文本覆盖。

### Merge wave — cross-artifact serial pass（requirements ↔ plan ↔ tasks ↔ contracts；1 条新 finding）

| ID | Category | Severity | Anchor | Fact（一句话事实） | Suggested disposition（指针） |
|----|----------|----------|--------|--------------------|------------------------------|
| E-01 | E coverage / F inconsistency | HIGH `(validated: confirm)` | `tasks.md:38`（GATE-9）; `tasks.md:254`（T047）; `tasks.md:354-365`（§ Green Attribution）; `contracts/*.md` 页级 `Requirements:` 行 | GATE-9/T047 要求 `account-clause-coverage.py` 退出 0 且 baseline 之外 0 个未覆盖名称，但 § Green Attribution 刻意保留 4 个未认领条款（`observer-role#C-01`、`observer-verification#C-03/C-05/C-07`），且五份契约仅在页级引用 FR、条款体无 citation group —— 实测脚本 exit 1（4 beyond baseline、FR 0/23），该完成门按字面无法通过。 | `/speckit.tasks`（GATE-9/T047 对齐 § Green Attribution 的 4 条披露，或把 4 条纳入 `[green:]` 认领）+ `/speckit.plan`（补 per-clause FR citation group 或调整该 lane 预期） |

**固定步（技能 §3，read-only）判定——phase-visible**：

- `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/096-sdd-observer-agent --corpus-root .specify/specs` → `status: uncovered`，**exit 1**（证据：`test-evidence/analyze-clause-coverage.txt`）。读值：claimed clauses 54；baseline 640 names；`[clause-uncovered]` 644 未覆盖、其中 **4 条 beyond baseline**（即 § Green Attribution 的 4 条披露未认领条款）；`[fr-uncovered]` **0 of 23** FRs cited from citation groups（五页仅页级引用，机械印证 W2-10，并构成 E-01 的第二条 blocking lane）；`[clause-unparsable]` 107 个既有语料文件无 clause id（1 个 positive-form parse doubt，语料级条件，非 096 特有）；`[coverage-baseline-delta]` 640 baseline-internal 不阻塞。技能要求该未通过状态必须 phase-visible 并带补救指针——已由 E-01 承接；本阶段不修复。
- `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/096-sdd-observer-agent` → `status: ok`，6 个 label 全 pass（0），5 records，0 error / 0 warning，`high=0`（证据：`test-evidence/analyze-decision-tensions.txt`）。I pass 无 finding。

**跨制品复核注记（对既有行，不改变其评级）**：

1. **W1-02**（validator 边界：只判 requirements.md；下游写入者未检查）——合并波补查：lifecycle C-08 指定最终 observer 执行以 `--final` 追加 `line-terminal` + `observer-settle`，C-10 定义缺口行窗口；失败的收束路径仍有「启动失败 / 无 journal」空档，与 finding 描述一致；不改变 confirm 评级。
2. **W1-03**（reject）——合并波独立复核与 validator 一致：T003/T033/DoD-6/plan T-005 已把基线落到 `test-evidence/digest-fieldset-baseline.txt` 并给出可复跑命令与比较单元；requirements 文本未内联路径仅是表述性省略。
3. **W3-06**（LOW，需聚合波对照）——合并波对照 data-model：V-14→T011（引擎单写者）/T037（exit-3 断言）；V-19→T036/T037（双线夹具与隔离断言）；V-18→T031/T019（写面断言）；V-20→T006/T017（封闭集读声明）；V-15→T024 断言键集，但「unknown keys are a spine-side finding」这一句没有实现行承接——W3-06 的追溯性缺口成立，范围收窄为 V-15 的第二句 + 五条规则的显式归属缺失。
4. **W3-01**（confirm）——合并波补记：wp02↔wp03 亦互锁（T031←T029 与 T032←T020，lines 210/211），故「wp02 与 wp03 MAY run concurrently」同样不可成立；属同一 package-map 缺陷（锚点 100 已覆盖），不另立新行。
5. **W2-06 / W3-02**——同一 `tests/fixtures/sdd-observer/` 领地面（plan 的 WP 依赖句 vs tasks 的 wp03 写域），两行分别锚定 plan 与 tasks，保留双行。
6. **W2-10 / E-01**——固定步的 `fr-uncovered 0/23` 是 W2-10（页级 FR 引用）的机械后果，并在 E-01 中成为第二 blocking lane。

---

## Cross-artifact consistency（合并波一致性总账）

### Coverage Summary

| 量 | 读值 | 来源 / 判定 |
|----|------|-------------|
| FR 定义 / SC 定义 | 23 / 7 | requirements.md 定义行（任务阶复测一致） |
| FR → 任务文本覆盖 | 23/23 | W3 机器核对（tasks.md 文本） |
| SC → row trace | 7/7 | tasks.md § SC → row trace 七行齐全 |
| 契约条款 | 58 = 13+13+12+10+10 | 五页 `^## C-` 标题；与 plan/feature-ref/tasks 三处计数一致 |
| `[green:]` 认领 | 54/58；4 条披露未认领 | tasks.md § Green Attribution；4 条 = 会计口径的 beyond-baseline（E-01） |
| FR citation groups | **0/23** | 固定步读值；五页仅页级 `Requirements:` 引用（W2-10 的机械证据） |
| data-model 规则 → 任务 | V-1…V-13/V-16/V-17 → T017；V-14→T011/T037；V-15→T024（第二句无承接）；V-18→T031；V-19→T036/T037；V-20→T006/T017 | 合并波对照（W3-06 收窄） |
| 任务行 / 包 | 47 行、4 包、无缺号重号、行级无环 | W3 机器核对 |
| 未映射任务 | 0 | 47 行全部落在 story/package 归属 |
| 扫描语料 | 291 文件（解析 184 + named-unparseable 107） | 固定步；107 为语料级既有条件 |

### Feature Linkage Summary（G）

- **名称级（W1）**：`Related Feature` 声明 Feature ID `096` 与名称「SDD 专用观察者与线级观察记录（sdd-observer）」，与清单页眉主题一致；`.specify/features.md` 096 行与 `.specify/features/096.md` 均存在。
- **内容级 / 阶段记录义务（合并波）**：索引行 Status `Planned`、Last Updated `2026-11-10`、备注记录 plan 阶段落册；详情文件 Status `Planned`、Last Updated `2026-11-10`。`/speckit.tasks` 的声明转场为「Maintain `Planned`」，同日日期即当前值；implement 阶段刷新由 T044 承接。**无 finding**（名称级 + 内容级均无 index/detail 漂移）。

### Constitution Alignment（D）

- 三波均 0 CRITICAL；plan 的 22 项 Constitution Check 全 Pass；合并波复核未发现宪法 MUST 冲突。
- **W3-04 的层级**：违反的是 `AGENTS.md` § Concurrent Development Safety（项目指令级 MUST），不是宪法原则——故高危但非 CRITICAL。
- 证据面弱化（非冲突）：plan rows I / VI / XV 的证据陈述超出制品实况 → W2-10 / W2-11 / W2-09（LOW/MEDIUM）。

### Checklist accountability（H，全量）

- `checklists/requirements.md`：12/12 已勾选，0 个未勾选 `[Gap]`。
- `checklists/2026-11-10-observer-requirements-quality.md`：38 项全部未勾选；`[Gap]` 7 项 = raised 6 + covered-by 1，`unraised=0 · undispositioned=0` → 阻断 **0**（明细见 W1 节）。
- 合计：`unchecked[Gap]=7 · 阻断=0`。

### Decision Tensions（I pass）

- 判定对象仅 `plan.md`：`## Decision Tensions` 在场、锚点正确、5 条记录（T-001…T-005）字段完整、cost 可映射；确定性程序 6 label 全 pass。**无 finding**。

### Unmapped Tasks / Do-not-flag 复核

- 未映射任务 0；W2 的 duplication pass 判定 format facts 的重复属合法信息面（owner 持有拼写），不立 finding；`checklists/requirements.md` 的 245 行读值与当前 253 行的差异属带日期的阶段记录（clarify 前测量），按噪音控制不立 finding。

---

## Systemic observations（聚合观察，不提升任何单行评级）

- **S1 — 同 spec 双线前提缺口（W1-08, W2-08；旁涉 plan T-001 判别证据）**：三处从不同制品指向同一未言明前提——「两条线解析到同一 spec 目录」不属支持状态，但 V-19 / lifecycle C-05 / 双线夹具 / FR-021 均未把它写成显式前提或判定。
- **S2 — 状态词汇漂移（W2-02, W2-03, W1-15, W2-12）**：`settled` 无 spine 表示、`closed` vs `failed` 终态互斥未裁决、实例 label vs 执行 label、`run_stamp`/`run`/`R1` 三名并存——同一状态面在 data-model / 契约 / 需求 / 快速开始四处的词汇未收敛。
- **S3 — 验收判据与 FR 义务的间隙（W1-02, W1-03〔reject〕, W1-10）**：SC 层提出可判定结果，而写入义务 / 结构定义落在需求之外；W1-03 被下游制品驳回，W1-02 被确认——同一模式的两个不同结局说明「需求文本单独自足」不是本规格的稳定属性。
- **S4 — 包级并发与共享写面（W3-01, W3-02, W3-03, W3-04, W2-06）**：package map、行级 `[P]`/`[blockedBy:]`、并行叙事与共享 append-only sink 四处对「谁并发、写哪里」给出互不相容的声明——implement 派发前必须收敛，否则字面执行即死锁/冲突。
- **S5 — Constitution Check 证据面弱于声明（W2-09, W2-10, W2-11）**：三行证据把「页级引用」写成「逐条引用」等；不影响 Pass 结论，但削弱门禁的证据质量。
- **S6 — 覆盖门与披露的自我矛盾（E-01 + fr citation lane）**：确定性会计为红，而 tasks 文档把红声明为可接受——完成门与披露制度在同一文件内冲突。

---

## Metrics

- **检测**: findings 39（W1 18 · W2 14 · W3 6 · 合并波 1）；上限 50 内，无 overflow。
- **评级（validated，主表）**: CRITICAL 0 · **HIGH 4** · MEDIUM 26 · LOW 8；主表 38 行；Appendix A 1 行（W1-03，reject）。
- **校验波**: sent 6 · confirm 4 · downgrade 1 · reject 1；降级率 1/6 ≈ 16.7%，reject 率 1/6 ≈ 16.7%。
- **覆盖**: FR 23/23 任务文本覆盖；FR citation 0/23（fixed-step）；clauses 54/58 claimed（4 披露未认领）；SC 7/7。
- **制品修改数**: 0；修复动作: 0（只读阶段）。
- **H pass**: `[Gap]` 7/7 处置，阻断 0。

## Rerun delta

- **Round 1**：本特性此前无 merge report、无 analyze findings（W1 记录 `test-evidence/` 无既有 `analyze-findings-W1*`）。`Resolved Since Last Run` 与 `New Since Last Run` 不适用；本节不虚构 delta。
- 后续 rerun（修复后）以本文件 ID 为基线（`W1-*` / `W2-*` / `W3-*` / `E-*` 全量保留，W1-03 在附录中保留其 ID）。

---

## Appendix A — Rejected findings（校验拒绝；不静默丢弃）

| ID | 原 Severity | Verdict | 保留理由 |
|----|-------------|---------|----------|
| W1-03 | HIGH | reject | 下游制品（`tasks.md:110` T003、`:212` T033、`:22` DoD-6、`plan.md:126` T-005）已把 SC-006 基线落到具名持久路径 `test-evidence/digest-fieldset-baseline.txt`，并给出可复跑采集命令与比较单元；requirements 文本未内联路径属表述性省略。两份证据边界原文见 § Validation wave「W1-03」块。 |

## Anomaly

`ANOMALY: none` —— 无未处置异常；无 in-passing repair（只读阶段，未触碰制品）。固定步的 `status: uncovered` 是按技能要求 phase-visible 的报告项（已由 E-01 承接），不是被静默吸收的异常。
