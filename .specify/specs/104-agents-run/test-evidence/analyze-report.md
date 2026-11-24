# Analyze Report — 104-agents-run (`/speckit.agents run`)

- **Spec**: `.specify/specs/104-agents-run`（requirements 24 FR / 7 SC / 8 STR；plan；3 contracts / 35 clauses；tasks 33 rows；2 checklists）
- **Bound Feature**: 019 Agents Command（`Implemented`，no-status-regression）
- **Run**: `r20261124T054500Z-9b2d` · analyze attempt 1 · 2026-11-24 · Round 1（full severity set）
- **Round 2**: `r20261124T054500Z-9b2d` · analyze attempt 2 · 2026-11-24 · incremental re-check after repair commit `b6907ee53` — **0 open findings**; see § Round 2 (incremental re-check) at the end of this file.
- **Mode**: strictly read-only on artifacts. Writes confined to `test-evidence/analyze-report.md`, `test-evidence/analyze.jsonl`, `test-evidence/analyze-findings.jsonl`; the later wrap-up engine entries are the skill's sanctioned bookkeeping exception.
- **Same-author gate**: **not fired** — every analyzed artifact was produced by a prior independent stage session (requirements / clarify / plan / tasks / checklist), not by this session. Detection was direct; no fresh-context detector was dispatched. CRITICAL/HIGH validation used the subagent-unavailable fallback (`validated: direct re-read, subagent unavailable`), as this execution must not dispatch subagents.
- **Verdict (Round 1, superseded by Round 2)**: **2 HIGH / 4 MEDIUM / 0 CRITICAL / 0 LOW** — not ready for `/speckit.implement` until the two HIGH findings are repaired text-level; the MEDIUM findings do not block on their own but should be repaired in the same round.
- **Deterministic gates (full re-run for Round 2)**: `validate-requirements` 0 error / 0 warning · `validate-tasks` 0 error / 1 warning (same adjudicated `green-cross-phase` C-10 vs C-06) · `pre-analyze-check --stage requirements / plan / tasks` all `decision: pass` (errors=0, advisories=57, identical pre-existing set) · `account-clause-coverage` `status: ok` (claimed clauses 35, FR 24/24, 0 beyond baseline) · `validate-decision-tensions` 0 error / 0 warning (0 records, compliant `N/A`) · Feature index 100 = 100 rows. Full table in § Round 2.

## Detection passes run

A duplication · B ambiguity · C underspecification · D constitution alignment · E coverage · F inconsistency（含 closed-set containment claims、cross-clause contradictions）· G feature relevance & accuracy（含 stage-recording duties）· H checklist accountability · I decision tension records（确定性校验器）。

### Deterministic verdicts consumed (read-only)

| Check | Verdict |
|---|---|
| `python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:104-agents-run"` | `flow_class: execution`, `source: declaration`（非表达类）→ 既有门禁集**逐字不变**，零新增阻断项 / 零新增必填章节；本阶段一次读取、复用于全部判定。 |
| `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/104-agents-run` | `status: ok`, exit 0 — claimed clauses **35**, FR **24/24**, `uncovered beyond baseline: 0`; lone warning `clause-unparsable (108)` is a pre-existing corpus-level fact (107 `md-none` named files + 1 parse doubt), not feature-introduced. `--freeze` was NOT passed. |
| `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/104-agents-run --json` | `status: ok`, 0 error / 0 warning; **0 records**, compliant `N/A` with four negated load-bearing triggers; all six labels pass. |
| `python3 scripts/python/validate-tasks.py .specify/specs/104-agents-run/tasks.md` | PASS — 0 error / 1 warning: `green-cross-phase` C-10 at T009 vs C-06 at T017 — the **adjudicated** exception recorded in the tasks report and the 019 registry row. |
| `python3 scripts/python/validate-requirements.py .specify/specs/104-agents-run/requirements.md` | `status: ok` — 0 error / 0 warning, 281 lines, 24 FR + 7 SC, 8 shared strings. |
| Clause namespace / claim partition (scripted) | 35 clause ids unique `C-01…C-35`, no dup, continuous; 35 `[green:]` claims, each clause exactly once, no duplicate claim. |
| Task row count / coverage map (scripted) | 33 task rows; all 24 FRs and all 7 SCs present in the map; 4 unmapped task rows (all process/checkpoint rows, see below). |
| `sync-mirrors.py --check` / `regen-command-copies.py --check` | rc 0 / rc 0 — no pre-existing drift on the pairs this spec touches. |
| 095 inherited-blocker premise | `deferred_tasks=none` / `final_path_deferred=0` confirmed in `.specify/specs/095-superagent-role/verification.md`. |
| Feature index integrity | `Total Features: 100` = 100 rows. |

### Premise re-measurements（implement 前树态，与 research / tasks 的测量对照）

`^# /speckit.agents` = **3**（commands ref 三副本）；`capabilities (create / refine)` = **4**（commands 2 / command-and-skills 1 / routing scenario 1）；`create and refine one agent` = **2**（commands ref）；`Generate role-based agents or create custom agents` = **1+1**（installation / quickstart）；`generates the seven role-based workflow agents` = **2**（commands ref）；`argument-hint` 在 `templates/commands/agents.md` = **0**；七字段名在 `skills/internal/run-agent/SKILL.md` = **0**；五个新测试文件 **5/5 ABSENT**；兄弟 `argument-hint` 先例 `team.md:4` / `goal.md:4` / `anchor.md:4` 在位。所有读数与 research B-01…B-07 一致。

### Reference sweep

七个分析产物的全部**全路径**引用均解析成功，唯五处为 implement 才创建的预期路径（`notes/pre-change-measurements.md`、`notes/red-first-evidence.md`、`verification.md`、`test-evidence/mutation-drill.md`、`test-evidence/behavior-class-evidence.md`）。关键 owner 段落全部解析：`superagent-definitions.md` § The super↔sub Protocol / § Role-Transition Injection（九个 item-id slug 逐项）/ § Role Edges / § Visualization & Tracking；`subagent-definitions.md` § Dispatch-Time Governance Obligation（收窄谓词三条件）/ § The Concurrency Obligation；`role-edge-check.py`（`--action report/query`）、`execution-config.py`（`resolve`）、`sdd-route.py`（`--action authorize`）、`exec-quant.py`（`collect-dispatch`）、`status-digest.py`（`ROLE_VIEW_FIELDS = parent/roles/role_set_marker/depth`）均在位。

### Plan constraint

`git diff d6a9f1cbb..HEAD` 对 plan-owned 面（`plan.md` / `data-model.md` / `contracts/` / `quickstart.md` / `research.md` / `feature-ref.md`）**恰为**两处已声明的 `PLAN-EDIT:` 引用级补全（3 insertions / 3 deletions：C-19 +FR-013、C-22 +FR-021、C-35 +FR-024），无条款正文改动 — **compliant**。本 analyze 运行零触碰。

## Findings

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| **F-01** | F — inconsistency（closed-set containment claim） | SC-005 → T014/T029 scope test → implement acceptance | **HIGH** | `requirements.md` SC-005（L228）；`tasks.md` T014（L181）、T029（L232）；`feature-ref.md` § Delivery surface items 20–22（L52–59）；`plan.md` § Project Structure（L99–118） | SC-005 的比较单元写作 `git diff <base>..HEAD --name-status` 的**路径集**，而允许差异集只列产品面五类（模板 / 技能 / docs / tests / 再生成副本）。implement 区间必然还包含 `.specify/specs/104-agents-run/**`（T001/T002/T030/T031/T033 创建的 notes 与 test-evidence 证据）、`verification.md`、Feature 登记编辑与运行记录——均不在允许集内。按字面「补集断言该区间不出现上列之外的路径」读，声明**必然误红**；按「只比较五类产品面」读，则是另一条声明。两种读法各自成立 ⇒ 依 `closed-set-claims.md` 不可判定（void）。 | 把比较单元显式限定为五类产品面并声明流程/证据/登记路径在比较单元之外，或把这些路径类**按类**并入允许差异集；随后重跑该门。属规格/任务文本级回修（SC-005 / T014 / T029），不改实现。 |
| **C-01** | C — underspecification（zero-occurrence class predicate） | docs contract test → T016/T018 → implement | **HIGH** | `contracts/agents-run-docs.contract.md` C-29（L32–34）、header STR-006（L6）；`requirements.md` FR-019（L184）；`research.md` B-05（L13）；现行 `docs/reference/agents/command-and-skills.md:11` | C-29 要求「`[[STR-006]]`-class two-capability statements … MUST appear 0 times」，但该「class」没有成员枚举。实测陈旧句是 `creates or refines **one** agent`（与 STR-006 字面 `create and refine one agent` 不同，且中间夹 markdown 粗体），仅按契约 header 写的测试会**假绿**，FR-019 要求删除的两能力陈述得以存活。FR-019 自身也停在「一类只含两能力的陈述」，C-34 的封闭谓词表未收录该句。 | 在 C-29 中具名实测字面量（或把该谓词加入 C-34 的封闭表，连同 `**one**` 粗体形态），并由 `test_agents_run_docs_contract.py` 钉住。属契约/规格文本级回修。 |
| **B-01** | B — ambiguity（checklist CHK005 raised） | run-agent Input/edge 文本 + `data-model.md` E1 → implementation | MEDIUM | `requirements.md` § Edge Cases（L140）；`data-model.md` E1 Rules（L21）；`checklist` CHK005（L21） | 团队参数边界写作「（如 `--target`）」——参数类是**开放**的，响应「报告属于 `/speckit.team` 并请求澄清」没有被钉住的输出形态（无 STR / 无字面量）。E1 只点名 `--target`。第二个实现可以对其余团队式选项另作处置而仍然「合规」。 | 定义参数类（至少列出当前已知的团队参数封闭集）并把响应形态钉进 run-agent 文本 / E1；或明确声明任何未知选项统一走同一冲突规则并给出具名输出句。 |
| **E-01** | E — coverage gap（checklist CHK014 raised） | contracts → verification → implement | MEDIUM | `requirements.md` FR-023（L191）；`checklist` CHK014（L33）；契约逐条类别标签（command header L4；dispatch C-11…C-22；docs header L4） | FR-023 的两份封闭清单覆盖 13/24 FR；其余 10 条（FR-002/005/006/009/012/013/014/015/021/024）在 FR-023 中没有类别。契约按条款打了类别标签，但 FR-024 的取证路线（唯一入口测试执行）既非行为类也非制品类，且没有任何工件说明「未列入的 FR 按什么规则取证」。 | 写明剩余 FR 的分类规则（例如「未列入行为类清单者按制品类文本钉住，除非另行具名」），并显式给出 FR-024 的取证路线（SC-007 / T032），或扩充 FR-023 的两份清单。 |
| **F-02** | F — inconsistency（blind gate） | tasks GATE-8 → implement completion acceptance | MEDIUM | `tasks.md` GATE-8（L38）；`contracts/agents-run-docs.contract.md` C-34（L52–67）；DoD-6（L22） | GATE-8 声称「陈旧字面量封闭集为空」，但其 grep 只覆盖 C-34 八条谓词中的 4 条：`generate seven`、`generate project-aware role agents`、以及「同行含 `no arguments` 与 `generate`」三条不在检查内。例如 installation 的 "generate seven role-based development workflow agents" 会让 GATE-8 保持绿色。绿色 GATE-8 不构成所称零集的证据（完整检查只在 docs 契约测试里）。 | 让 GATE-8 指向 C-34 谓词集 / docs 契约测试，或把 grep 扩到全部八条谓词。属任务文本级回修。 |
| **G-01** | G — feature metadata / stage record | Feature 019 index row + detail → review / seal stage recording judgment | MEDIUM | `.specify/features.md` 019 行（L28 的 Last Updated 单元格）；`.specify/features/019-agents-command.md` § Latest Review（L16） | 实际到达的最新阶段是 **checklist**（`checklists/run-command-2026-11-24.md` 与 `test-evidence/checklist.jsonl` 已提交），但索引行与详情的最近记录停在 **tasks**，没有 checklist 注记。状态 `Implemented` 依法保持、日期（2026-11-24）同日巧合一致，但阶段记录已陈旧——正确的状态不豁免阶段记录。 | 在 019 索引行 Last Updated 单元格与详情 Latest Review 补 checklist 阶段注记（日期已正确）；不改状态。 |

## Validation（CRITICAL/HIGH only）

- **Sent 2**（F-01, C-01）· **confirmed 2** · **downgraded 0** · **rejected 0** · downgrade rate **0/2**。
- 每条 C/H 行携带 `(validated: direct re-read, subagent unavailable)`。按本执行约束未派发子代理，采用技能 §7 的 fallback（直接证据重读）；证据路径弱于独立子代理，在此披露。

**F-01** — verdict `confirm`；`(validated: direct re-read, subagent unavailable)`
- `evidence_supported`: SC-005（L228）点名基线（implement 阶段提交的父提交）、比较单元（`git diff <base>..HEAD --name-status` 的路径集）、允许差异集的产品面五类与补集断言；T014（L181）/ T029（L232）复用同一 diff；`feature-ref.md` items 20–22（L52–59）与 `plan.md` § Project Structure（L99–118）明确把 spec 目录与 Feature 登记列入交付面。
- `evidence_not_supported`: 没有工件声明 `.specify/specs/104-agents-run/**`、`.specify/features*`、`.specify/memory/**` 在比较单元之外或在允许集之内；本阶段尚无执行证据，字面读法下的误红是**推导**而非实测。

**C-01** — verdict `confirm`；`(validated: direct re-read, subagent unavailable)`
- `evidence_supported`: C-29（L32–34）的零出现类谓词；header（L6）把 STR-006 定义为 `create and refine one agent`；`command-and-skills.md:11` 的实测陈旧句为 `creates or refines **one** agent`；C-34 表（L52–67）未收录该谓词；FR-019（L184）保持「一类」措辞。
- `evidence_not_supported`: 没有工件枚举该类的成员；未来测试是否会断言实测字面量在 implement 前不可观测。

## Checklist H accountability（清单面 H）

来源：`checklists/run-command-2026-11-24.md`（40 条，全部 `- [ ]` 为设计使然，逐条作答属 analyze 职责）；`checklists/requirements.md` 无未勾选 `[Gap]` 项。

- 未勾选 `[Gap]` 项：**3** — CHK005、CHK014、CHK030。
- `CHK005 disposition: raised-as-finding B-01`
- `CHK014 disposition: raised-as-finding E-01`
- `CHK030 disposition: covered-by research.md § R-01`（R-01 保留 copy 1 为基底、删除 copy 2/3 为旧子集；B-01 实测该子集关系；C-23 与 T017 声明同一保留 / 删除规则）
- 可观察计数：`unchecked[Gap]=3`，`raised=2`，`dispositioned=1`，`unraised=0`，`undispositioned=0` ⇒ **`unchecked[Gap] ∧ ¬raised ∧ ¬dispositioned = 0`**（analyze gate 不被阻断项）。

## Coverage Summary

| Metric | Reading |
|---|---|
| FR coverage | **24/24**（`FR claimed: 24` / `FR uncovered: 0`） |
| Clause coverage | **35/35**，每条 `[green:]` 恰一次（C-01…C-35 唯一、无重复认领） |
| Task rows | 33（Setup 1 / US1 8 / US2 3 / US3 3 / US4 8 / US5 3 / Polish 7） |
| SC → tasks | 7/7 SC 出现在映射表 |
| Zero-finding floor sample（已重读） | 全部 **13** 条单任务行 FR：FR-003→T004、FR-004→T005、FR-007→T006、FR-008→T007、FR-009→T007、FR-010→T008、FR-012→T011、FR-016→T013、FR-017→T013、FR-018→T017、FR-019→T018（→ C-01）、FR-023→T031、FR-024→T032；另抽样多行 FR-001（T004/T005/T017/T027）、FR-011（T011/T012）、FR-022（T002/T003/T016/T024/T027/T028/T032）。结论：抽样行均承载其 FR；降级映射仅为上述 findings 所指。 |

## Feature Linkage Summary

| Field | Reading |
|---|---|
| Bound feature | **019 Agents Command**（`Implemented`，no regression） |
| Binding evidence | `requirements.md` § Related Feature（L18）；索引行 019 的 Spec Path → `requirements.md`；详情 § Related Specifications（L84） |
| Confidence | High — 显式绑定 + 索引/详情一致 + 术语匹配 |
| Status duty | 合法保持 `Implemented`（clarify/plan/tasks/checklist 在 implement 之前无状态迁移权） |
| Stage-record duty | **陈旧** — checklist 阶段未记录（G-01） |
| Index integrity | `Total Features: 100` = 100 行 |

## Constitution Alignment

无宪法冲突。`plan.md § Constitution Check` 按序渲染现行 23 条原则（I–XXIII）且全部 Pass；宪法 live roster 恰为 23 个 `###` 原则标题、名称逐一对应。`## Decision Tensions` 为合规 `N/A`（校验器 6/6 pass、0 records、四条承重触发逐条否定）。Principle IV（test-first）由 Tests Mode ON + 红先行承载，两处 migration/regression 形态的例外在 tasks 文本中具名并给出理由。无 CRITICAL 级冲突。

## Unmapped Tasks

四条任务行不在 Requirement Coverage Map 中，均为流程 / 检查点行，不是未被覆盖的需求：T001（implement 起点基线与证据落点，即 SC-005 的基线）、T015（US3 转绿与结构审计取证）、T026（US5 转绿检查点）、T033（quickstart S-0 实跑记录）。

## Systemic Observations

1. `validate-tasks` 的 `green-cross-phase` WARN（T009 的 C-10 先于 T017 的 C-06）是**已裁定**例外：C-06 的第三面（docs Syntax）只能在 T017 转绿，T009 的允许残余失败集已点名 C-06；tasks 报告与 019 行均有记录。非 finding。
2. 行为类 / 制品类二分在 FR-023、C-22、`data-model.md` E5/E6、tasks T031 与 quickstart S-7 之间一致（7 条款 / 6 FR），没有任何测试文本声称覆盖运行期行为。
3. 共享字符串引用形态（低信号）：`tasks.md` 对 STR 使用裸 `STR-NNN` 且在 T004/T005 复制了 STR-001 字面量，而 requirements 的 citation convention 要求 `[[STR-NNN]]`；全部 `[[STR-]]` 引用均可解析，且混用形态与兄弟规格一致 — 记为观察，不判 finding。
4. plan-owned 面合规：`d6a9f1cbb..HEAD` 内恰为两处已声明的 `PLAN-EDIT:`（3+/3−），无条款正文改动；本 analyze 零触碰。
5. implement 前树态与 research / tasks 的测量前提逐项吻合（三副本、无 argument-hint、run-agent 零七字段、五测试缺位、生成器 rc 0）；规格链描述的是**变更后**目标态，现状不是不一致。
6. 需求级覆盖的一点弱映射（观察，不升级为 finding）：FR-013 的「同 Instance 多次执行彼此隔离 / 不改定义」由 `data-model.md` E2 Rules 与 run-agent 既有 Run Mode 首段承载，而非 C-19 的引用括号本身；T006/T009 是边界行，不是该句的直接钉住者。现有设计面足以覆盖，记录以免读者把引用当成文本断言。

## Metrics

- Total FR **24** · Tasks **33** · Coverage **100%**（FR 24/24；clauses 35/35）· Feature linkage **100%**（1 需求 / 1 Feature，高置信）
- Ambiguity **1**（B-01）· Underspecification **1**（C-01）· Coverage **1**（E-01）· Inconsistency **2**（F-01, F-02）· Duplication **0** · Feature metadata **1**（G-01）
- CRITICAL **0** · HIGH **2** · MEDIUM **4** · LOW **0** · Findings **6**
- Validation: sent **2** / confirmed **2** / downgraded **0** / rejected **0**（direct re-read fallback）

## Rerun delta

本需求**首次** analyze 运行 — `test-evidence/` 无先前报告，用户亦未提供。六条均为 **New Since Last Run**；无 carried-over / resolved 行，因而不存在「已清空的旧集」与「干净重跑」被混同的问题。

## Next actions

1. **先行文本级回修两条 HIGH**（F-01、C-01），随后重跑 `/speckit.analyze`（Round 2）再进入 `/speckit.implement`。HIGH 未清不进入 implement 门。
2. MEDIUM 可同轮处理：B-01（团队参数类与响应形态）、E-01（FR-023 分类规则 + FR-024 路线）、F-02（GATE-8 指向 C-34 / 契约测试）、G-01（Feature 登记补 checklist 注记）。
3. 本运行未修改任何制品；回修应经 `/speckit.requirements`、`/speckit.plan`、`/speckit.tasks` 或用户批准的文本编辑执行。

## Evidence pointers

- 本文件：`.specify/specs/104-agents-run/test-evidence/analyze-report.md`
- E3：`.specify/specs/104-agents-run/test-evidence/analyze.jsonl`（恰一条 `stage-status`，六项缩减字段）
- 结构化发现：`.specify/specs/104-agents-run/test-evidence/analyze-findings.jsonl`
- 确定性命令与其裁决见上文 § Deterministic verdicts；完整输出按 single-run evidence discipline 留在会话记录中。

---

## Round 2 — Incremental re-check (2026-11-24, after repair commit `b6907ee53`)

- **Mode**: incremental per the analyze-artifacts skill § Rounds / Incremental re-check protocol. Re-check scope = the six Round 1 repair loci plus their one-hop neighbors; untouched domains reused by declared hash (below). Artifacts strictly read-only; writes confined to the three evidence files.
- **Validator independence**: every CRITICAL/HIGH closure in this round carries `(validated: direct re-read, subagent unavailable)` — no subagent was dispatched in this execution (dispatch constraint), so the weaker direct-re-read path is disclosed verbatim.
- **Verdict**: **0 CRITICAL / 0 HIGH / 0 MEDIUM / 0 LOW open** — all six Round 1 findings `fixed` with evidence; no new findings; the analyze gate is **clear** and `/speckit.implement` may proceed.

### Round record — touched loci

| Round 1 locus | Repair in `b6907ee53` | Round 2 reading |
|---|---|---|
| `requirements.md` SC-005 (L228) | comparison unit restricted to the five product-face roots; process/evidence/registry paths declared outside it | five-element closed-set form re-read and satisfied: baseline referent (implement parent commit), per-class comparison unit, mechanically derived allowed-delta set, both complement and structural-invariant sides, no undefined aggregate term. The literal reading no longer turns false by construction |
| `requirements.md` FR-019 (L184) | two-capability statement class closed to exactly two forms (STR-006 verbatim + measured bold variant) | aligned with C-29/C-34; the bold variant occurs once at `docs/reference/agents/command-and-skills.md:11` and STR-006 verbatim 0 times there — measured, not assumed |
| `requirements.md` FR-023 (L191) | default classification rule for unlisted FRs + named FR-024 evidence route | nine named default text/structure faces (FR-002/005/006/009/012/013/014/015/021) plus the FR-024 route to the `run-tests.sh` baseline diff (SC-007 / T032); every FR other than FR-023 itself (the rule) now has a classification or a named exception |
| `requirements.md` § Edge Cases (L140) | team-parameter class closed by owner reference + named conflict sentence | class members verified in `templates/commands/team.md` (`--target` L4/L36/L46; `--scope` + `--spec-dir` L39); the sentence `team parameter not accepted by run: <option>` is identical in the FR text, `data-model.md` E1 and T013 |
| `contracts/agents-run-docs.contract.md` C-29 (L34) / C-34 (L52–68) | C-29 closed to two named literal forms; C-34 gains the bold-variant row (Before 1 → After 0) | both forms are decidable zero-occurrence predicates over named literals; the C-34 table stays the sole owner of the predicate set; the contract's dated "measured once" record matches the tree |
| `tasks.md` T014 (L181) / T029 (L232) | diff wording limited to the SC-005 five roots; process/evidence/registry paths excluded from the complement assertion | consistent with SC-005; no residual complement phrasing remains anywhere else (`quickstart.md` / `plan.md` / contracts carry none) |
| `tasks.md` GATE-8 (L38) | gate now runs the docs contract test through the unique entry; subset greps explicitly forbidden | the check is the C-34 full-table assertion; T016 (L196) / T023 (L206) say "C-34 全表" instead of copying a predicate count |
| `tasks.md` T013 (L180) | team-option disposal duty added to the run-agent edit | carries the same closed class + named sentence as the implement-side carrier |
| `data-model.md` E1 Rules (L21) | team-option class + named conflict sentence | matches the requirements edge case; "option position" is bounded by E1's `task_text = The remainder` rule |
| `.specify/features.md` 019 row (L28) / `.specify/features/019-agents-command.md` § Latest Review (L16) | checklist-stage note added to both; status held | the latest stage actually reached (checklist) is now recorded in both surfaces; status `Implemented` lawfully unchanged |

**One-hop neighbors re-read**: SC-005 → `feature-ref.md` § Delivery surface items 20–22 (L52–59; delivery-surface list, carries no containment claim) and `plan.md` § Project Structure (L99–118; same, no containment claim); C-29/C-34 → T016 (L196) / T018 (L201) and the `tests/contract/test_agents_run_docs_contract.py` name in T016 / GATE-8; FR-019 → `research.md` B-05 (L13; carries the same bold literal, no drift); E1 → `skills/internal/run-agent/SKILL.md` (no team-parameter text yet — correctly an implement duty via T013, no contradiction today).

### Reused domains（declared, never silent — sha256 verified against the dispatch payload)

| Path | sha256 | Match |
|---|---|---|
| `plan.md` | `982cfb9c6c84a83e1fef92982543b0bcb5921922d898c12f2d9df188732e9930` | ✓ |
| `research.md` | `ce079805df3cdccc4c2b680b55c2e50458a8f29450e151351358f851c7788d13` | ✓ |
| `quickstart.md` | `14b9dc9d96e1c4ccbd06594146b4a0235439ff2a96ee5ce9ee2a41c8d8135672` | ✓ |
| `feature-ref.md` | `8cb5c433d93cef7ac37235b9a68aac3a3dbe7ec8f6469cf8b93c546fe6a3162f` | ✓ |
| `contracts/agents-run-command.contract.md` | `0013ef7083a9a907e471d429adeecb4ce00a112ec063e86483b46ad7b9f784e2` | ✓ |
| `contracts/agents-run-dispatch.contract.md` | `e4231d2fcf4c3c74b85f3b5837abbed7b2601b18ca2a14b490e543f15163d449` | ✓ |
| `checklists/requirements.md` | `88bacf2b216b94ddedd116d99d1e780f5dff545728b3e16edd4c200cc214e6b1` | ✓ |
| `checklists/run-command-2026-11-24.md` | `b573691e463956ca705461adaa57c5acd980f8b62b3b306890df8b252fe76dde` | ✓ |

Plan-owned surface check: `git diff d6a9f1cbb..HEAD -- plan.md data-model.md contracts/ quickstart.md research.md feature-ref.md` shows exactly the three tasks-stage citation PLAN-EDITs (C-19 +FR-013, C-22 +FR-021, C-35 +FR-024) plus the two repair-round `PLAN-EDIT` declarations in `analyze-repair.txt` (docs contract C-29 literal + C-34 row; data-model E1 rule) — 6 insertions / 5 deletions, no clause-body change elsewhere; `plan.md` / `research.md` / `quickstart.md` / `feature-ref.md` byte-identical since `d6a9f1cbb`.

### Per-finding dispositions (Round 2)

| ID | Round 1 severity | Disposition | Closing evidence |
|---|---|---|---|
| **F-01** | HIGH | **fixed** | `requirements.md` SC-005 (L228) five-root comparison unit + outside-path declaration; `tasks.md` T014 (L181) / T029 (L232) same unit; closed-set five-element form re-read. `(validated: direct re-read, subagent unavailable)` |
| **C-01** | HIGH | **fixed** | `contracts/agents-run-docs.contract.md` C-29 (L34) two-literal closed set + C-34 row (L60, Before 1 → After 0); `requirements.md` FR-019 (L184) aligned; measured bold variant = 1 at `command-and-skills.md:11`, STR-006 verbatim = 0 there. `(validated: direct re-read, subagent unavailable)` |
| **B-01** | MEDIUM | **fixed** | `requirements.md` § Edge Cases (L140) closed class + named sentence; `data-model.md` E1 (L21) same; T013 (L180) implement carrier; team.md members verified |
| **E-01** | MEDIUM | **fixed** | `requirements.md` FR-023 (L191) default rule (9 named faces) + FR-024 named exception route |
| **F-02** | MEDIUM | **fixed** | `tasks.md` GATE-8 (L38) now the docs contract test through the unique entry; C-34 remains the sole predicate owner; T016 / T023 reference the full table |
| **G-01** | MEDIUM | **fixed** | `.specify/features.md` 019 row (L28) and detail § Latest Review (L16) carry the checklist-stage note; status held |

### Delta since Round 1

- **Resolved Since Last Run**: 6 — F-01, C-01, B-01, E-01, F-02, G-01, each with artifact + location evidence in the tables above.
- **New Since Last Run**: 0 — no finding introduced by the repair itself.
- **Carried over**: 0.
- The cleared backlog (six closures) and the clean rerun (zero new/carried findings under the incremental scope, plus the full-run deterministic gates below) are stated separately, not merged into one claim.

### Deterministic gates — full-run backstop after the repair

| Gate | Command | Verdict |
|---|---|---|
| G-REQ | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/104-agents-run/requirements.md` | `status: ok` — 0 error / 0 warning; 281 lines / 31 definition rows / 8 shared strings |
| G-TASKS | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/104-agents-run/tasks.md` | PASS (with warnings) — 0 error / 1 warning: the same adjudicated `green-cross-phase` C-10 (T009) vs C-06 (T017) |
| G-PRE-REQ / PLAN / TASKS | `.qoder/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/104-agents-run --stage {requirements,plan,tasks} --repo .` | `decision: pass`, errors=0, advisories=57 each — identical to the pre-repair readings, all pre-existing (five pending test files + data-model INV ids) |
| G-COV | `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/104-agents-run` | `status: ok` — claimed clauses 35, FR 24/24, 0 beyond baseline; pre-existing `clause-unparsable (108)` unchanged |
| G-DTR | `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/104-agents-run --json` | 0 error / 0 warning; 0 records; compliant `N/A`, six labels pass |
| G-INDEX | `Total Features` vs row count | 100 = 100 — holds |

No gate is red; no red leg needs a full re-run to explain.

### Full re-run trigger evaluation

- Declared domains touched: 6 of 14 (requirements / docs contract / tasks / data-model / features index / feature detail) — not more than half → incremental stands.
- Contract surfaces: only 1 of 3 contract files changed (`agents-run-docs.contract.md`); the other two are byte-identical to the payload hashes → the "all three artifact classes" trigger does not fire.
- Finding taxonomy and clause-id map unchanged (C-01…C-35; C-34 gained a table row, no clause id added, removed or renumbered).
- No open CRITICAL/HIGH remains after this round → mandatory full re-run not triggered.

### C/H conclusions (validation)

- New CRITICAL/HIGH findings in Round 2: **0** — no validation-wave targets were produced.
- Closure of the two Round 1 HIGH findings re-read directly (F-01 five-element form + one-hop neighbors; C-01 two-literal closed set + measured occurrence), both marked `(validated: direct re-read, subagent unavailable)`.
- Downgrade / reject rate: not applicable — zero findings were sent to an external validator wave.

### Zero-finding floor — sample re-read

- All **13** single-task FR anchor rows read in the current tree: FR-003→T004, FR-004→T005, FR-007→T006, FR-008→T007, FR-009→T007, FR-010→T008, FR-012→T011, FR-016→T013, FR-017→T013, FR-018→T017, FR-019→T018, FR-023→T031, FR-024→T032 — every row still carries its FR, including the repaired FR-019 / FR-023 / FR-024 neighborhoods.
- Multi-row samples: FR-001 (T004 / T005 / T017 / T027) and FR-022 (T002 / T003 / T016 / T024 / T027 / T028 / T032) — anchor lines spot-read; the remainder verified against the unchanged coverage map, since the repair diff's hunk set (T001 / T013 / T014 / T016 / T023 / T029 / GATE-8 / US4 Independent Test, 8 hunks = 16 changed lines) touches no other row.
- Outcome: no silently unmapped row; coverage map unchanged by the repair.

### Checklist accountability (H — reused domain)

`checklists/run-command-2026-11-24.md` and `checklists/requirements.md` are byte-identical to Round 1 (hashes above). The Round 1 dispositions stand: `CHK005 raised-as-finding B-01`, `CHK014 raised-as-finding E-01`, `CHK030 covered-by research.md § R-01`; therefore `unchecked[Gap] ∧ ¬raised ∧ ¬dispositioned = 0` still holds.

### Round 2 observations (non-findings)

1. **C-29 flow-face watch point**: `command-and-skills.md:38` currently reports the ambiguity as `(create / refine)` and `:49` says "two skills". C-29's five items cover both through "cover run in its routing flow" and "three skills", but only the three-skill item names its literal explicitly; a test authored strictly from the item list should also pin the routing-flow ambiguity sentence. Recorded as an implementation watch point, not a finding — the repaired zero-occurrence class and the three-skill statement are explicit and decidable.
2. **"option position" is a referenced boundary, not a defined term**: E1's `task_text = The remainder` rule makes the option/task boundary mechanically derivable, and the requirements exclude task text from option parsing consistently. No action.
3. **E3 held at exactly one `stage-status` row**: the existing row was updated in place (`selection_basis` / `evidence_ptr` now name Round 2); no second row was added.

### Round 2 next action

Gate is clear — proceed to `/speckit.implement`; the implement entry re-runs the docs gate through `scripts/bash/run-tests.sh` as GATE-8 now demands. This round modified no artifact.

### Round 2 evidence pointers

- This section + the three `test-evidence/analyze-*` files; repair diff `git show b6907ee53`; plan-owned diff `git diff d6a9f1cbb..HEAD -- <plan-owned paths>`; the six deterministic gate commands above (full output per single-run evidence discipline in the session record).
