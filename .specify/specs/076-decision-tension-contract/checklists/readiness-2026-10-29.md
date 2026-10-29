# Implementation Readiness Checklist: 决策反题与反指标契约（Decision Tension Record）

**Purpose**: 在进入 `/speckit.analyze` 与 `/speckit.implement` 前，逐条审计 26 FR / 8 SC 的**可实现性、可测性与一致性**。本清单是 readiness audit，不是默认的 spec-quality checklist，也不是实现验证；`pass` 只表示该条在 requirements / plan / contracts / tasks 链上已经闭合到可执行，不表示代码已经存在。
**Created**: 2026-10-29
**Feature (Requirement Scope)**: `.specify/specs/076-decision-tension-contract/`（Feature 076，状态 `Planned`）
**Requirements (What)**: `.specify/specs/076-decision-tension-contract/requirements.md`
**Specifications (How, context only)**: `.specify/specs/076-decision-tension-contract/plan.md`、`.specify/specs/076-decision-tension-contract/contracts/`、`.specify/specs/076-decision-tension-contract/tasks.md`

**Checkbox semantics**: `[x]` = **pass**（该条已具备实现与验收条件）；`[ ]` = **fail**（存在缺口，未解决）。失败项只点名将继承缺口的实现面，不就地修复。

**Method**: 只读审计。每条为 question + verdict + traceable anchor + verbatim evidence；`fail` 项附 `Inherits:`（任务 / 契约）与 `Handoff:`。未修改 `requirements.md` / `plan.md` / `data-model.md` / `contracts/` / `tasks.md` / `quickstart.md` / `research.md` / `feature-ref.md`，未声明 `PLAN-EDIT`。

**Intent defaults**: Depth = Standard；Audience = Reviewer；Focus = DTR 六字段/拒绝形态的可判定性 + 四元组 shape-vs-semantic 边界。调用方参数已预答意图，未发起澄清轮。

**Structure check**: `python3 scripts/python/validate-requirements.py .specify/specs/076-decision-tension-contract/requirements.md` → `status: ok`、五项命题全 pass、`scanned: 287 lines, 34 definition rows, 4 shared strings`、`0 error(s), 0 warning(s)`、exit 0。完整输出见 `.specify/specs/076-decision-tension-contract/test-evidence/checklist-stage-checks.md`。

## Summary

| Verdict | Count |
|---------|-------|
| pass | 27 |
| fail | 10 |
| total | 37 |

| Area | Items | pass | fail |
|------|-------|------|------|
| Owner 与承重判据 | CHK001–CHK007 | 6 | 1 |
| 模板锚点与测量绑定 | CHK008–CHK011 | 3 | 1 |
| Analyze 结构通道 | CHK012–CHK016 | 4 | 1 |
| ADR 引用与校验器 | CHK017–CHK024 | 5 | 3 |
| 证伪四元组 | CHK025–CHK032 | 4 | 4 |
| 术语、镜像、闭合面、跨制品映射 | CHK033–CHK037 | 5 | 0 |

## Owner 与承重判据

- [x] CHK001 [Completeness] Does the new owner's opening declare the six-field record shape, admissibility, rejection forms, load-bearing threshold, adjacent-owner boundary and identifier form, and bind every consumer to path reference rather than restatement? — **pass** — [Req §FR-001; Contract C-1/C-8] — Evidence: FR-001 requires "MUST 新建规范 owner `shared/guidelines/decision-tension.md`，并在其开头声明它拥有什么" and "所有消费者（计划模板、分析检测、ADR 模板、契约测试）MUST 以路径引用该文件，MUST NOT 复述其判据表、拒绝清单或门槛表"; T004 and T006 carry both halves.

- [x] CHK002 [Completeness] Is the record field set closed at exactly six fields plus `tension_id`, with the field names and `T-NNN` form fixed verbatim? — **pass** — [Req §FR-002; Contract C-2; Data-model E1] — Evidence: FR-002 enumerates `decision`, `antithesis`, `binding_constraints` (with `pole_a` and `pole_b`), `discriminating_evidence`, `expected_sacrifice`, `revision_trigger` and the identifier `tension_id` as `T-NNN`; data-model E1 fixes the line grammar and "六个字段各出现一次".

- [x] CHK003 [Completeness] Are the admissibility criteria and the rejection forms each specified as a closed set with an explicit "adding an entry is an owner revision" rule? — **pass** — [Req §FR-003/§FR-004; Contract C-3/C-4] — Evidence: FR-003 says "可采纳判据 MUST 是封闭集且四条全满足"; FR-004 says "拒绝形态 MUST 是封闭清单，命中任一条即判该记录不成立"; both close extension through owner revision.

- [ ] CHK004 [Clarity, Measurability] Is a decidable judge named for the semantic admissibility and rejection criteria — straw-man `antithesis`, non-executable or non-binary `discriminating_evidence`, "decision names one pole", and the open-ended "要平衡 / 综合考虑 / 视情况而定 一类" wording — given that `dtr-rejected-form` is implemented only for the `none` literal and the wording list? — **fail** — [Gap, Req §FR-003/§FR-004 vs §FR-013/§FR-016] — Evidence: FR-004 lists "`antithesis` 为稻草人" and "`discriminating_evidence` 不可执行或结果非二值" as rejection forms, while T008 scopes the implementation to "实现不可判定措辞与空极点的拒绝形态"; no task assigns the semantic forms to a named reviewer, and the analyze channel is structural only. — **Inherits**: T004/T008; `contracts/decision-tension-owner.md` C-3/C-4; `contracts/validator.md` C-2/C-4. — **Handoff**: `/speckit.plan`.

- [x] CHK005 [Completeness] Does the load-bearing threshold define the four triggers and the negative boundary (a decision meeting none is not asked for a record and a missing record is not a defect)? — **pass** — [Req §FR-005; Assumption A7; Contract C-5] — Evidence: FR-005 says "承重决策门槛 MUST 为四类触发，任一成立即承重（不可逆 / 跨团队 / 高爆炸半径 / 与宪法原则相关）" and "不满足任一触发的决策 MUST NOT 被要求填写记录，缺失记录 MUST NOT 被判为缺陷"; T006 implements the threshold and boundary.

- [x] CHK006 [Consistency] Are the complexity gate and the four adjacent-owner boundaries specified with a single tie-break and path-only references? — **pass** — [Req §FR-006/§FR-007; Contract C-6/C-7] — Evidence: FR-006 requires the rubric's tie-break "取较高一级，并以承重判据为准"; FR-007 names the four adjacent mechanisms and requires "各以路径引用不复述".

- [x] CHK007 [Consistency] Does the plan's own `## Decision Tensions` instance satisfy the six-field grammar and resolve both `expected_sacrifice` values to declared measurement sources? — **pass** — [Plan §Decision Tensions; Req §FR-002/§FR-010] — Evidence: `### T-001` and `### T-002` are unique and increasing; each carries `decision`, `antithesis`, `binding_constraints` with `pole_a` and `pole_b`, `discriminating_evidence`, `expected_sacrifice`, `revision_trigger`; the values are "SC-004 Source ↓ ..." and "SC-002 Source ↑ ...", each containing exactly one `SC-NNN`.

## 模板锚点与测量绑定

- [x] CHK008 [Clarity] Is the template section's position pinned to a single satisfiable slot by heading-sequence adjacency, with the `N/A` rule and `### T-NNN` carrier also fixed? — **pass** — [Req §FR-008; Contract C-1/C-2] — Evidence: FR-008 requires "`## Constitution Check` 的**直接后继**" and asserts "`## Constitution Check` → `## Decision Tensions` → `## Project Structure` 三者相邻"; the current template order is `## Constitution Check` (line 31) → `## Project Structure` (line 62), so T005 has exactly one insertion point.

- [x] CHK009 [Clarity] Is the template required to carry only a pointer plus the field-name list, with four machine-checkable assertions against copying the owner's tables? — **pass** — [Req §FR-009; Contract C-3] — Evidence: FR-009 says "只引用 owner 的字段名与判据（一条指针加字段清单），MUST NOT 复制 owner 的可采纳判据表、拒绝清单或承重门槛表"; C-3 names the four assertions: section presence, heading-sequence adjacency, pointer path resolves, and no owner table row reproduced.

- [x] CHK010 [Measurability] Does the closed `<SC-NNN> Source <↓|↑>` grammar resolve against every measurement-source entry the requirements declare? — **pass** — [Req §FR-010; Contract C-1/C-2] — Evidence: the requirements declare 8 entries, all of the form "`- **SC-001 Source**: ...`" through "`- **SC-008 Source**: ...`"; FR-010 requires resolution to an entry "以 `**SC-NNN Source**` 起头", and T008 parses the same form.

- [ ] CHK011 [Measurability] Is the metric whose `↓`/`↑` direction is asserted identified and machine-bound for each measurement source, or can both directions parse against the same collection-method entry? — **fail** — [Ambiguity, Req §FR-010 / Clarifications Q4] — Evidence: FR-010 asks for "测量来源标识与变差方向"; Q4 says the token is "指标的变差方向", but the 8 sources are collection methods, for example "SC-001 Source: 夹具计划文件与结构校验器的退出码、报告条目"; the parser checks only that the token is `↓` or `↑` and leaves "阈值或说明自由" unparsed. — **Inherits**: T008; `contracts/measurement-binding.md` C-1/C-2. — **Handoff**: `/speckit.plan`.

## Analyze 结构通道

- [x] CHK012 [Consistency] Is the analyze channel's judged object limited to the current `REQUIREMENTS_DIR/plan.md`, with out-of-scope plans producing no finding and in-scope historical plans not exempt? — **pass** — [Req §FR-011; Contract C-1] — Evidence: FR-011 says "检查范围的被判定对象 MUST 只有一份工件：本轮经前置脚本解析出的 `REQUIREMENTS_DIR` 下的 `plan.md`" and "其他特性目录下的 `plan.md` MUST NOT 被本通道打开"; C-1 repeats that in-scope historical plans are not exempt and out-of-scope plans produce no finding.

- [x] CHK013 [Completeness] Are the three defect classes, the fail-closed missing-section rule, the no-advisory value domain and the missing-measurement-section branch all specified? — **pass** — [Req §FR-011; Contract C-2; SC-002] — Evidence: FR-011 lists (a) missing section or bare `N/A`, (b) incomplete six fields including a single pole, (c) unmapped sacrifice; "三类都判 HIGH"; "该通道 MUST NOT 设 advisory 或降级档"; the requirements-without-measurement-section case branches on record count.

- [ ] CHK014 [Consistency] Is SC-003's "same trivial fixture plus one irreversible decision" state defined precisely enough for a detector forbidden to judge load-bearingness to emit exactly one HIGH — in particular, does the compliant `N/A` section stay or go? — **fail** — [Ambiguity, Req §SC-003 / US4 AS2 vs §FR-011] — Evidence: FR-011 says "检测器 MUST NOT 被要求自行判断计划里是否存在承重决策"; SC-003 says "同一夹具补入一条不可逆决策后复跑恰出现 1 条 HIGH"; US4 AS2 says "同一夹具追加一条不可逆决策（回滚需要迁移），When 复跑 analyze，Then 恰出现 1 条 HIGH（缺张力记录）"; T017 repeats the fixture without stating that the previous compliant `N/A` is removed. — **Inherits**: T017/T018; `contracts/analyze-channel.md` C-2. — **Handoff**: `/speckit.plan`（先钉死夹具状态），随后 `/speckit.tasks`.

- [x] CHK015 [Consistency] Are severity and mechanical adjudication both tied to existing owners — propagation-surface severity and `scripts/python/` verdicts — without new tiers or model scoring? — **pass** — [Req §FR-012/§FR-013; Contract C-3/C-4] — Evidence: FR-012 says "严重度 MUST 采用既有传播面判据 ... MUST NOT 新造严重度等级、评分或成熟度结论"; FR-013 says "可机械判定的部分 MUST 由既有 `scripts/python/` 下的程序执行并输出 verdict，模型只消费 verdict".

- [x] CHK016 [Consistency] Is the channel's placement and only-add delta declared with baseline `ac63fe8c`, and is the `SKILL.md` enumeration update pinned for the `I` channel? — **pass** — [Req §FR-014; Contract C-5; Research R-2] — Evidence: FR-014 fixes "基线参照物为本特性基线提交 `ac63fe8c`" and allows "本特性新增的通道小节 + 因新增通道而更新的计数行"; R-2 pins "Eight passes (A–G · I decision tensions) plus one checklist pass (H)"; T011 changes "`## The seven passes`" and the "`SKILL.md` 第 5 步" sentence.

## ADR 引用与校验器

- [x] CHK017 [Completeness] Does the ADR template gain a `tension_id` slot that points without copying and requires an explicit no-record statement? — **pass** — [Req §FR-015; Contract C-1] — Evidence: FR-015 requires a "`tension_id` 引用位" that "MUST NOT 复制记录字段内容" and "当该决策无张力记录时，MUST 显式写明「无承重张力记录」及判定结论"; T020 edits `docs/decisions/template.md` § Alternatives.

- [ ] CHK018 [Measurability] Is there a specified invocation or gate that applies the dangling-`tension_id` check to real ADR files, rather than only to a contract-test fixture? — **fail** — [Gap, Req §FR-015 / SC-006; Contract C-2] — Evidence: FR-015 says an unresolvable reference "MUST 判为断链错误"; C-2 requires "the check MUST be exercised by a contract test over a fixture pair"; T019/T020 implement the test and reuse the index function, but the only CLI (FR-016) reads `<spec-dir>/plan.md` and `<spec-dir>/requirements.md`, not an ADR path. — **Inherits**: T019/T020; `contracts/adr-reference.md` C-2. — **Handoff**: `/speckit.plan`（定义触发面与调用方式）.

- [x] CHK019 [Clarity] Are the validator's invocation, exit codes, closed six labels, human/JSON output shape and `none`-vs-unmapped dedup all fixed? — **pass** — [Req §FR-016; Contract C-1/C-2/C-3] — Evidence: FR-016 fixes `--spec <spec-dir> [--json]`, exit 0/1/2, the six labels, "同一记录同一标签 MUST 只报一条", and "`expected_sacrifice` 恰为 `none` 时只报 `dtr-rejected-form`，不再叠加 `expected-sacrifice-unmapped`".

- [ ] CHK020 [Consistency] Does the six-label set map to the analyze channel's three defect classes without double counting — specifically, when the section is missing, do `dtr-anchor` and `dtr-section-missing` both fail and produce two findings against SC-002's required one HIGH? — **fail** — [Conflict, Req §FR-016 / SC-002] — Evidence: FR-016 calls the six labels "封闭六项，且与 FR-008 锚点、FR-011 三类缺陷一一对应" (six labels mapped to four targets), while `dtr-anchor` is "`^## ` 序列三行相邻" and `dtr-section-missing` is "章节缺失"; a missing section fails both, and no cross-label dedup or precedence rule is defined. — **Inherits**: T007/T010; `contracts/validator.md` C-2; `contracts/analyze-channel.md` C-2. — **Handoff**: `/speckit.plan`.

- [x] CHK021 [Completeness] Are the inverse samples required to live in the contract tests, with a red run per sample, rather than only in prose? — **pass** — [Req §FR-017; Contract C-4] — Evidence: FR-017 says "每一例 MUST 在契约测试中产生一次红运行记录；逆样本 MUST NOT 只写在文档描述里"; T003 constructs the compliant plan plus five inverse inputs in `tmp_path`.

- [ ] CHK022 [Coverage] Do the inverse samples prove every closed field is required and the Edge-Case "skipped `tension_id`" rule is enforced, or does the five-sample set leave both unproven? — **fail** — [Gap, Req §SC-001 / §Edge Cases; Contract C-4] — Evidence: SC-001 lists five reverse inputs including "删任一字段" as one run; Edge Cases adds "重复、跳号或非 `T-NNN` 形态由确定性校验器判错"; T003 lists the same five and does not include a skipped id or one deletion per field. — **Inherits**: T003/T007; `contracts/validator.md` C-4. — **Handoff**: `/speckit.tasks`（补夹具）；若样本数改变，先回 `/speckit.plan`.

- [x] CHK023 [Measurability] Is "zero new mechanism" judged as a before/after set difference over command, dependency and process inventories against `ac63fe8c`? — **pass** — [Req §FR-018 / SC-005; Contract C-1] — Evidence: FR-018 forbids a new `/speckit.*` command, storage, ledger, scheduler, scorer or model call; SC-005 requires the command list to be "逐字相同（允许差异集为空）" and "新增第三方依赖为 0"; T022 collects the two snapshots and writes `scope-set-difference.txt`.

- [x] CHK024 [Measurability] Is SC-001's acceptance observation (one compliant run plus five inverse runs, judged only by exit code and report entries) specified? — **pass** — [Req §SC-001; Contract C-4] — Evidence: SC-001 says "确定性校验器返回 0；五个反向输入 ... 各返回 1。判定只读退出码与报告条目"; T008 targets the six runs; quickstart S1/S2 pin the commands.

## 证伪四元组

- [x] CHK025 [Completeness] Is the quartet a closed four-field form produced before dispatch, replacing the one-line attempt? — **pass** — [Req §FR-019; Contract C-1] — Evidence: FR-019 says "输出形态 MUST 由「一句话加 verdict」升级为封闭四元组：`attempt`、`exit_code`、`observation`、`would_go_red_if`" and "四元组 MUST 在派发前产生，字段集合封闭"; T014 adds the subsection and leaves the old paragraph byte-identical.

- [ ] CHK026 [Consistency] Does the quartet preserve the owner's existing "attempt must be executable" admissibility, given that the checker MUST NOT replay `attempt` and the receiving agent MUST NOT override a zero verdict? — **fail** — [Conflict, Req §FR-020/§FR-021 vs baseline owner §可采纳判据] — Evidence: the existing owner requires "**可执行**——点名一位复核者能直接运行的路径/命令/测试/测量"; FR-021 says "脚本 MUST NOT 重放 `attempt`" and "接收方 agent MUST NOT 反向覆盖判决 ... 额外疑虑只能写成非阻断注记"; T015 checks only the four keys, an integer exit code, the `raw:` prefix and the two `would_go_red_if` halves, so a prose attempt passes. — **Inherits**: T014/T015; `contracts/falsification-quartet.md` C-2/C-3. — **Handoff**: `/speckit.plan`.

- [ ] CHK027 [Clarity, Measurability] Is the "named red signal" half of `would_go_red_if` given a mechanical shape (what token or name counts), or is `tautology` left to an unspecified reading? — **fail** — [Ambiguity, Req §FR-020/§FR-021] — Evidence: FR-020 asks for "具体输入与预期红色结果"; FR-021 requires "被改坏的具名输入（反引号跨度）与具名红色信号，缺任一判 `tautology`"; T015 repeats "具名红色信号" without defining it, and the six reject fixtures only cover a plainly vague sentence. — **Inherits**: T012/T015; `contracts/falsification-quartet.md` C-3. — **Handoff**: `/speckit.plan`.

- [x] CHK028 [Consistency] Is rejection a deterministic program verdict with a closed six-value reason set, no receiver override and no replay of `attempt`? — **pass** — [Req §FR-021; Contract C-3] — Evidence: FR-021 fixes exit 0/1/2, the closed set `missing-field` / `empty-field` / `exit-code-not-integer` / `observation-not-raw` / `tautology` / `input-unreadable`, "接收方 agent MUST NOT 反向覆盖判决", and "脚本 MUST NOT 重放 `attempt`".

- [ ] CHK029 [Consistency] Do SC-004's six invalid payloads and FR-021's six rejection reasons describe the same test set? — **fail** — [Conflict, Req §SC-004 vs §FR-021] — Evidence: SC-004's six are "四字段各缺一、`observation` 为转述、反空真条件为空真"; FR-021's six are the reason codes `missing-field` / `empty-field` / `exit-code-not-integer` / `observation-not-raw` / `tautology` / `input-unreadable`; T012 follows the reason-code set, so SC-004's four missing-field variants and the `empty-field` / `exit-code-not-integer` / `input-unreadable` reasons cannot both be the same 6/6. — **Inherits**: T012/T015; `contracts/falsification-quartet.md` C-3. — **Handoff**: `/speckit.plan`（对齐 SC-004），随后 `/speckit.tasks`.

- [x] CHK030 [Consistency] Are the quartet's carrier and the SI-3C pointer obligation both fixed without a second definition or a new store? — **pass** — [Req §FR-022/§FR-023; Contract C-4/C-5] — Evidence: FR-022 keeps the carrier at "SI-4 派发载荷、SI-7 intervention 记录" and forbids a new ledger, store, probe or score; FR-023 requires SI-3C to keep "步骤摘要与指向 owner 的指针" and the test to assert "workflow 无第二份定义"; the current SI-3C already reads "this step references that owner and MUST NOT restate its rules."

- [ ] CHK031 [Completeness] Does any task own publishing the disclosed shape-vs-semantic limitations — a forgeable `raw:` prefix and a `tautology` check that cannot prove the red result — on the owner or workflow surface? — **fail** — [Gap, Req §Clarifications Q5; Contract C-2/C-3] — Evidence: Q5 records "标记可被伪造（伪造由复核者发现，属非阻断注记，不进判决）" and "它管不到「输入改坏了却不会变红」这层真实性（那属 SI-6 与复核者）"; T014 describes "`raw:` 代理、反空真两半条件" and T016 only points to the owner; neither task requires the limitation to be stated where consumers read the rule. — **Inherits**: T014/T016; `contracts/falsification-quartet.md` C-2/C-3. — **Handoff**: `/speckit.plan`.

- [x] CHK032 [Measurability] Is SC-002 measurable with four fixtures and the required 0/1/1/1 HIGH counts? — **pass** — [Req §SC-002; Contract C-2] — Evidence: SC-002 says "对三类缺陷各报 1 条 HIGH ... 对合规计划三类各 0 条 ... 四类夹具各运行一次即可判定"; quickstart S3 gives the four fixtures and counts; T009/T010 target the channel.

## 术语、镜像、闭合面、跨制品映射

- [x] CHK033 [Consistency] Is terminology compliance guarded at zero hits on all three distribution trees with a positive control that the A3 alias list still exists? — **pass** — [Req §FR-024; Assumption A3; SC-007; Contract C-2] — Evidence: FR-024 forbids the A3 aliases in "`shared/`、`templates/`、`skills/`"; T021 scenario F asserts zero hits and "正控断言 `requirements.md` § Assumptions A3 的别名清单仍存在"; the current tree measures 0 for each of "矛盾论、主要矛盾、矛盾的主要方面、对抗性矛盾、矛盾转化条件", while A3 still lists them.

- [x] CHK034 [Consistency] Does the seven-row mirror table match the tasks' single sync-and-verify row, with the per-tool command-copy surface empty? — **pass** — [Req §FR-025; Contract C-3; Plan §Mirror Obligations; tasks §Mirror Obligations] — Evidence: FR-025 has 7 numbered rows; tasks states "**T024 是唯一的同步与验证行**" and T024 says "逐对陈述七行镜像对"; `templates/commands/**` is not touched, so `regen-command-copies.py` gains no copy.

- [x] CHK035 [Consistency] Are the two touched closed-set owners handled as only-add against `ac63fe8c`, with item counts not below baseline? — **pass** — [Req §FR-026 / SC-008; Contract C-4] — Evidence: FR-026 fixes the baseline, allows only "本特性新增的段落", requires "删除或改写行数为 0", and keeps "拒绝形态、边界声明、消费者清单的条目数不小于基线"; T021/T025 enumerate the diff and counts.

- [x] CHK036 [Traceability] Is every FR and SC mapped to at least one task, and is every one of the 34 contract clauses claimed by exactly one task row? — **pass** — [tasks §Requirement Coverage Map / §Clause Partition; DoD-2] — Evidence: the coverage map lists FR-001 through FR-026 and SC-001 through SC-008; the partition sums "8 + 3 + 4 + 3 + 5 + 5 + 2 + 4 = 34" with 15 claim rows; `account-clause-coverage.py` reports "claimed clauses (this feature): 34", "uncovered beyond baseline: 0", "FR claimed: 26", "status: ok".

- [x] CHK037 [Consistency] Do the declared counts (26 FR / 8 SC / 5 user stories / 4 shared strings / 8 measurement sources) match the actual file and the deterministic checker? — **pass** — [Req §Functional Requirements / §Success Criteria / §Shared Strings / §Measurement Sources] — Evidence: `validate-requirements.py` reports "status: ok", "scanned: 287 lines, 34 definition rows, 4 shared strings", "0 error(s), 0 warning(s)"; direct greps return 26 FR, 8 SC, 5 user stories, 4 STR rows and 8 `**SC-NNN Source**` entries.

## Failures and Handoffs

| CHK | One-line fact | Inherits | Handoff |
|-----|---------------|----------|---------|
| CHK004 | Semantic admissibility/rejection forms (straw-man antithesis, non-executable/non-binary evidence) have no named judge; T008 implements only `none` and wording cases. | T004/T008; `contracts/decision-tension-owner.md` C-3/C-4; `contracts/validator.md` C-2/C-4 | `/speckit.plan` |
| CHK011 | `expected_sacrifice` direction token is parsed but the metric whose direction is asserted is not identified or machine-bound; both `↓` and `↑` parse for the same collection-method source. | T008; `contracts/measurement-binding.md` C-1/C-2 | `/speckit.plan` |
| CHK014 | SC-003's post-add fixture does not state whether the compliant `N/A` stays; a structural detector forbidden to judge load-bearingness cannot emit the required 1 HIGH if it stays. | T017/T018; `contracts/analyze-channel.md` C-2 | `/speckit.plan`, then `/speckit.tasks` |
| CHK018 | No invocation or gate applies the dangling-`tension_id` check to real ADR files; only a contract-test fixture exercises it. | T019/T020; `contracts/adr-reference.md` C-2 | `/speckit.plan` |
| CHK020 | A missing section fails both `dtr-anchor` and `dtr-section-missing`; no cross-label dedup/precedence maps this to SC-002's single HIGH. | T007/T010; `contracts/validator.md` C-2; `contracts/analyze-channel.md` C-2 | `/speckit.plan` |
| CHK022 | Five inverse samples do not prove every one of the six field deletions or the Edge-Case skipped-`tension_id` rule. | T003/T007; `contracts/validator.md` C-4 | `/speckit.tasks`; if sample count changes, `/speckit.plan` |
| CHK026 | The existing "attempt must be executable" admissibility is unenforced: the checker never replays `attempt`, and the receiver cannot override a passing verdict. | T014/T015; `contracts/falsification-quartet.md` C-2/C-3 | `/speckit.plan` |
| CHK027 | The "named red signal" half of `would_go_red_if` has no mechanical shape; `tautology` is underdetermined. | T012/T015; `contracts/falsification-quartet.md` C-3 | `/speckit.plan` |
| CHK029 | SC-004's six invalid payloads (four missing-field variants + paraphrase + tautology) differ from FR-021/T012's six reason codes. | T012/T015; `contracts/falsification-quartet.md` C-3 | `/speckit.plan`, then `/speckit.tasks` |
| CHK031 | The disclosed shape-vs-semantic limitations (forgeable `raw:`, unprovable red result) are recorded only in the spec's Clarifications, with no task to publish them on the owner/workflow surface. | T014/T016; `contracts/falsification-quartet.md` C-2/C-3 | `/speckit.plan` |

## Coverage Matrix

### Functional Requirements

| FR | CHK | FR | CHK |
|----|-----|----|-----|
| FR-001 | CHK001 | FR-014 | CHK016 |
| FR-002 | CHK002, CHK007 | FR-015 | CHK017, CHK018 |
| FR-003 | CHK003, CHK004 | FR-016 | CHK019, CHK020 |
| FR-004 | CHK003, CHK004 | FR-017 | CHK021, CHK022 |
| FR-005 | CHK005 | FR-018 | CHK023 |
| FR-006 | CHK006 | FR-019 | CHK025 |
| FR-007 | CHK006 | FR-020 | CHK026, CHK027 |
| FR-008 | CHK008 | FR-021 | CHK027, CHK028, CHK029 |
| FR-009 | CHK009 | FR-022 | CHK030 |
| FR-010 | CHK010, CHK011 | FR-023 | CHK030 |
| FR-011 | CHK012, CHK013, CHK014 | FR-024 | CHK033 |
| FR-012 | CHK015 | FR-025 | CHK034 |
| FR-013 | CHK015 | FR-026 | CHK035 |

### Success Criteria

| SC | CHK |
|----|-----|
| SC-001 | CHK022, CHK024 |
| SC-002 | CHK013, CHK032 |
| SC-003 | CHK014 |
| SC-004 | CHK029 |
| SC-005 | CHK023 |
| SC-006 | CHK017, CHK018 |
| SC-007 | CHK033 |
| SC-008 | CHK035 |

## Notes

- **This is a new dated file**, not a refresh of `checklists/requirements.md`; the earlier requirements-quality checklist remains as history. No plan-owned artifact was edited, so no `PLAN-EDIT` declaration is required or made.
- **Pass does not mean implemented**: the two validators, the owner file and the three test files are absent at this stage (`shared/guidelines/decision-tension.md`, `scripts/python/validate-decision-tensions.py`, `scripts/python/validate-falsification-quartet.py`, and the three `tests/contract/test_*.py` paths). The checklist judges whether the specification chain is sufficient to build and verify them.
- **Plan as first fixture**: `plan.md` § Decision Tensions is a hand-written pilot (`T-001`, `T-002`), not proof that the validator exists. Its records already use the future grammar, which is why CHK007 passes while the validator is still absent.
- **Channel letter**: the new channel is `I` because `H` is already the checklist-accountability pass in `skills/internal/analyze-artifacts/SKILL.md`; research R-2 pins the post-change sentence as "Eight passes (A–G · I decision tensions) plus one checklist pass (H)".
- **Line-count drift is a dated record, not a derived-count failure**: the requirements-stage evidence `test-evidence/validate-requirements.txt` records `scanned: 255 lines`; the current run records `287 lines` after the clarify round added prose. The definition counts are unchanged at 34 rows / 4 shared strings, so no FR / SC / STR count was stale.
- **No severity tiers**: in keeping with the checklist methodology, failures are prioritized by handoff target and impact, not by an invented severity scale.
- **Zero-modification evidence**: before writing this file the working tree was clean; after writing, only `checklists/readiness-2026-10-29.md` and `test-evidence/checklist-stage-checks.md` are new. The evidence file records the exact status.

## Report

- **Output path**: `.specify/specs/076-decision-tension-contract/checklists/readiness-2026-10-29.md`
- **Item count**: 37 (soft cap 40)
- **Verdict distribution**: 27 pass / 10 fail
- **Traceability**: 37/37 items carry a requirement, plan, contract, gap, ambiguity or assumption anchor (100%, above the 80% minimum)
- **Focus areas**: DTR six-field and rejection-form decidability; `expected_sacrifice` grammar coverage and direction semantics; shape-vs-semantic limitation ownership; mirror-pair/task consistency; terminology guard; zero-new-mechanism set difference
- **Depth level**: Standard
- **User-specified items incorporated**: all six special checks from the caller (DTR decidability, measurement-source grammar, quartet limitation task, seven-row mirror consistency, terminology guard, zero-new-mechanism set difference)
