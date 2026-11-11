# Analyze — merged findings report（100-seal-slice-archive）

**Date**: 2026-11-11 | **Branch**: `100-seal-slice-archive` | **Stage**: analyze（无人值守，analyze-gate exception 授权就地修复）
**Artifacts under analysis**: `requirements.md` / `plan.md` / `tasks.md` / `research.md` / `data-model.md` / `quickstart.md` / `feature-ref.md` / `contracts/`（3 页 40 条款）/ `checklists/`（2 文件）/ `.specify/features.md` + `features/099-speckit-seal.md` / `.specify/constitution.md` v1.19.2
**Authority**: `/speckit.analyze` command template + `analyze-artifacts` skill + constitution v1.19.2；flow_class=`execution`（`flow-class-check.py` → source=declaration）。

## 1. Method and evidence

- **Same-author condition**: the chain artifacts were produced by this SDD line in one multi-pass session. Detection was therefore delegated to **5 fresh-context read-only SDD Analysis Workers** (fork carrier: qodercli child processes via `dispatch.sh`, stream-json, `--no-session-persistence`, tools `Read Grep Glob Bash`).
- **Disjoint read domains (file-level, pairwise disjoint)**: W1 requirements+research+closed-set-claims; W2 plan+data-model+quickstart+constitution+decision-tension; W3 3 contracts+tasks; W4 features.md+099 detail+feature-ref+feature-integration; W5 two checklists+checklist-methodology. `READ-DOMAIN-CHECK` in every worker output matched its declaration; no overlap.
- **Validation wave**: **17 unique CRITICAL/HIGH findings** (duplicates across workers merged; worker-local IDs remapped to stable category-prefixed IDs) were each sent to one independent fresh-context validator (17 fork-carrier processes, one wave). Validators received only the finding (id/category/claim/severity/locations), never detection reasoning; detector and validator sets are disjoint. Results: **12 confirm · 3 downgrade · 2 reject**. After the wave, the working tree showed only this stage’s evidence files — no validator wrote.
- **Concurrency reading**: requested=5 / effective=5 / effective_reason=n/a (5 detection workers and 17 validators ran as independent processes).

## 2. Findings and disposition (round 1 → remediation)

| ID | Category | propagation_surface | Final severity | Status | Location(s) | Summary | Fix / disposition |
|----|----------|---------------------|----------------|--------|-------------|---------|-------------------|
| D-02 | D — constitution (I) | plan → feature traceability | CRITICAL | fixed | plan.md:70,82,94,106,118,130 | T-001…T-006 decision 行未携带 FR id；Constitution Check Row I 的「每条设计裁决引用 FR id」不成立。 | 各 decision 行追加 FR id（T-001 FR-002/FR-020；T-002 FR-001/FR-006；T-003 FR-012/014/015；T-004 FR-005/018；T-005 FR-012/013；T-006 FR-019）。 |
| D-03 | D — constitution (IV) | tasks → tests / verification | CRITICAL | fixed | plan.md:20,250-257; tasks.md T024/T027/T029; plan source list | 纯函数/工具无单元测试交付物；Tests 只声明 contract/integration。 | 新增 tests/unit/test_seal_archive_{classify,manifest_math,schema}.py，接入 T024/T027/T029、DoD-3、plan Testing/P3/source 与 feature-ref 交付面。 |
| F-01 | F — inconsistency | contracts / tests / implementation | HIGH | fixed | requirements.md:99-101 | 「部分归档」与「destination-exists」对同一分片双侧状态给出 exit 2 / exit 1 两个相反处置。 | Edge Cases 拆为跨分片混合（exit 2 partial-archive）与同一分片双侧（exit 1 destination-exists）。 |
| F-02 | F — inconsistency | contracts / tests / implementation | HIGH | fixed | requirements.md:120; C-102 ① | FR-006 的前置合取与 FR-007 的 not-applicable 成功冲突。 | FR-006 增加 not-applicable 分流；C-102 ① 同步（按 C-104 以 0 报告）。 |
| F-03 | F — containment | SC-009 evidence; static audit | HIGH | fixed | requirements.md:172; T053 | SC-009 的「仓库中不存在第二套处置词表」在基线即假（sanitize 五值 vs non-disposable 四值）。 | SC-009 与 T053 限定为「本特性新增的」，并点名基线中既有词表按原样保留。 |
| F-07 | F — inconsistency | manifest schema / tests | HIGH | fixed | C-207; C-202/C-203; T016 | C-207 的「所有路径仓库根相对」与 C-203 的 slice-relative files[].path、C-202 的 parent-relative merge_manifest.path 冲突。 | C-207 改为逐字段路径基准清单；T016 引用该逐字段基准。 |
| F-08 | F — inconsistency | tasks / SC-010 evidence | HIGH | fixed | C-116 SC-010; feature-ref; quickstart S-6; plan source | SC-010 首红模块在契约/feature-ref 写 round.py，在 tasks 写 rollback.py。 | C-116/feature-ref/quickstart/plan 统一为 tests/integration/test_seal_archive_rollback.py。 |
| F-09 | F — coverage | SC-007 / SC-008 evidence | HIGH | fixed | tasks.md:148-149; T012/T013/T026 | SC-007/SC-008 的 trace 指向实现行，测试文件作者行未承载算术/运行期用例。 | T012 增加算术与删行变异；T026 增加 runtime 存在/缺席用例；SC trace 改列 T012/T027 与 T013/T026。 |
| F-10 | F — inconsistency | manifest schema / tests | HIGH | fixed | requirements.md:119; C-203; T016 | 同一条目封闭字段集三写不一致（6/7/6，T016 缺 slug）。 | FR-005、T016 统一为 C-203 的七字段；T012 断言七字段键集与两处排序。 |
| F-11 | F — inconsistency | write-surface audit; SC-005 | HIGH | fixed | requirements.md:142 | FR-028 白名单 (b) 未覆盖 .specify/register.md 与 features/<ID>.md 活区。 | FR-028 (b) 改为引用 C-301 live 名册并点名 register/features/glossary/instructions。 |
| F-12 | F — inconsistency | write-surface audit; SC-005 | HIGH | fixed | requirements.md:142 | FR-028 白名单 (a) 只授权父 spec 树内移动，移动源侧在树外。 | FR-028 (a) 改为 `.specify/specs/<slug>` → `<parent>/slices/<slug>` 的纯移动。 |
| B-01 | B — ambiguity | contracts / tests / SC-001 | HIGH | fixed | requirements.md:35,164,177; C-106/C-116; V2; quickstart S-3; tasks DoD-4/T013/T043; feature-ref | `git diff --name-status -M` 缺少比较基；git mv 暂存后该命令读不到重命名对。 | 所有消费者改为 `git diff --name-status -M <pinned_commit>` / `HEAD`，并写明索引写入不改变读数。 |
| C-01 | C — underspecification | contracts / tests | MEDIUM (validated: downgraded) | fixed | requirements.md:120; C-102 | FR-006 五合取项未逐项映射唯一退出码。 | FR-006 与 C-102 写入逐项映射（①→2；②③④→1；⑤双侧→1/皆无→2/跨片→2）。 |
| F-04 | F — containment | SC-005 evidence; T030/T037 | MEDIUM (validated: downgraded) | fixed | requirements.md:132; C-211; T030; data-model E9 | FR-018 的「至少…任何其他路径形态」允许差异集未机械派生。 | 改为清单全文模式扫描 `.specify/specs/<slug>[/…]`；匹配集合=允许差异集，集合外逐字节一致；T030 同步。 |
| F-06 | F — inconsistency | SC-010 evidence; rollback | MEDIUM (validated: downgraded) | fixed | C-110; V14; quickstart S-6; T033 | 回滚完成判据要求「清单记录的 before 值」的 per-carrier sha256，但清单只记行文本与 pinned_commit。 | 判据改为相对 pinned_commit 的树零差异；S-6/C-110 增加 `--staged --worktree` 与索引清理。 |

**Round-1 appendix (validated but not fixed)**: `D-01` (constitution archive-admission scope) — **rejected** by its validator: FR-020 already rules slice archival is not retirement and MUST NOT query `archive-gate`; the constitution’s admission rule is the retirement gate. `F-05` (FR-025 test baseline) — **rejected**: the baseline is pinned by the implement-feature skill owner (`tests/.../baseline-failed.txt` + `comm -13`), and the added FR-025 pointer only cites that owner.

## 3. Coverage summary

| Lane | Reading | Verdict |
|------|---------|---------|
| FR universe | 28 FR | 28/28 cited from tasks citation groups (`account-clause-coverage.py`) |
| SC trace | 10 SC | 10/10 present in SC→row trace |
| Clauses | 40 （C-101…C-116 / C-201…C-212 / C-301…C-312 = 16/12/12） | each claimed by exactly one `[green:]` row; claimed 40 |
| Clause delta | 673 uncovered, 0 beyond frozen baseline | pass |
| Clause unparsable (corpus) | 108 files / 1 parse doubt | phase-visible warning, corpus-wide; not introduced by this feature |
| Single-task rows (zero-finding floor sample) | FR-018/T030, FR-023/T036, FR-026/T044, SC-003/T023, SC-007/T012+T027, SC-008/T013+T026, SC-010/T033 | re-read and verified: each claiming row carries the obligation (after T012/T026 extensions) |

**Coverage note**: the tasks-stage evidence (`test-evidence/tasks-stage-checks.txt`) states “675 lines (6 header + 669 names)” for `coverage-baseline.txt`; the measured baseline is 675 lines = 2 header + 673 names. This is a transcription error in a dated evidence record; the accountant’s measured reading (673/673) is authoritative and the record was not rewritten.

## 4. Feature linkage summary

| Item | Reading | Verdict |
|------|---------|---------|
| Binding | spec `100-seal-slice-archive` → Feature **099 Speckit Seal**（clarify Mode A；C-019 明确延后分片处置） | high confidence |
| Registry row | 099 row status `Ready for Review`; no 100 row; header 92 = 92 rows | consistent |
| Detail file | status/detail link/spec path/Last Updated agree with the row | consistent |
| Stage record | round-1 **G-01**（checklist stage absent from 099 row + detail）→ fixed by dated 2026-11-11 checklist notes in both carriers | fixed |
| Status vocabulary | round-1 **F-15**（features.md Status column re-enumerated a partial set）→ column now points to the owner in `acceptance-hardening.md § Feature Status` | fixed |
| `flow_class` claim | round-1 W4 **F-02** rejected: the declaration row is `requirements.md:6` (`Flow Class: execution`) and `flow-class-check.py` reads it | no change |

No requirement is bound to a wrong or nonexistent Feature; no registry routing defect remains.

## 5. Constitution alignment

Plan Constitution Check: 22/22 principles Pass. Independent round-1 detection raised three constitution-tier findings; validators decided:

- **D-01 CRITICAL — rejected** (see §2 appendix).
- **D-02 CRITICAL — confirmed and fixed** (T-record FR ids).
- **D-03 CRITICAL — confirmed and fixed** (unit-test deliverables).

After remediation, no open constitution conflict remains.

## 6. Unmapped tasks

T001 (baseline capture), T002 (evidence skeleton) and T051 (Feature registry close-out) are process/Setup/Polish rows with no FR/SC anchor; they are recorded as such in the trace note. T003 is now listed under FR-024. No task lacks a declared mapping or a recorded process-row disposition.

## 7. Checklist accountability (H pass)

The dated checklist has 36 unchecked items; 4 are `[Gap]`. Dispositions:

```
CHK021 disposition: raised-as-finding C-03 (FR-022 now requires the unattended decision record in test-evidence/)
CHK022 disposition: covered-by contracts/archive-manifest.contract.md § C-211; plan.md § Disclosed Rulings 2
CHK023 disposition: covered-by 099 merge-back.contract.md § C-019; 099 data-model.md § E14; C-203 now states the pre-existence
CHK025 disposition: raised-as-finding C-04 (RS-P1…RS-P4 premises now defined in requirements.md)
```

Census: unchecked=36（全部条目）, [Gap]=4, unraised=0, undispositioned=0 → `unchecked + unraised + undispositioned = 0` at the gap level. The other 9 fail verdicts are raised as findings (CHK008→C-01, CHK009→F-01, CHK010→B-01, CHK017→C-02, CHK027→F-02, CHK029→F-10, CHK030→F-11, CHK033→B-02, CHK034→F-12). The checklist header 3/7 was corrected to 4/6 and its candidate arithmetic clarified (37−9=28; 28+8=36).

## 8. Systemic observations

- **Requirement prose restating closed sets was the dominant drift source**: the same field set (FR-005 vs C-203 vs T016), the write allowlist (FR-028 vs C-301/C-106) and the exit-code map (FR-006 vs C-102) each existed in multiple hand-written copies. Remediation converted them to owner pointers or single enumerations.
- **`git mv` staging vs comparison base** was a cross-cutting trap: the same unbased `git diff` appeared in requirements, contract, data-model, quickstart, tasks and feature-ref. One definition (comparison base = pinned pre-apply commit) now lands in all consumers.
- **Test attribution** (SC→first-red module→claiming row) was the weakest traceability surface: two SCs had no row actually authoring their tests, and SC-010’s module had drifted. Fixed by test-authoring extensions and trace updates.
- **Hand-maintained summaries** (feature index status vocabulary, checklist candidate arithmetic, tasks-stage baseline count) drift from their owners; the analyze report records the measured readings rather than silently rewriting dated records.

## 9. Metrics

| Metric | Reading |
|--------|---------|
| Total requirements | 28 FR + 10 SC |
| Tasks | 53 rows / 8 work packages |
| Coverage | FR 100% (28/28); SC 100% (10/10); clause claims 40/40 |
| Feature linkage | 099, high confidence |
| Detection workers | 5; read-domain intersections 0 |
| Unique C/H findings validated | 17 |
| Validation verdicts | confirm 12 · downgrade 3 · reject 2 |
| Downgrade rate | 3/17 = 17.6% |
| Reject rate | 2/17 = 11.8% |
| Open CRITICAL / HIGH after remediation (final, round 2) | 0 / 0 |

## 10. Validation appendix (evidence boundaries, verbatim)

> Line numbers below refer to the round-1 pre-remediation snapshot; post-fix locations are in `analyze-dispositions.md`.

### D-01 — reject — same

**evidence_supported**: plan.md:82 (T-002 decision) admits slice archival both when the seal outcome is `Sealed` and when it is a named block; constitution.md:571 states `Sealed` is "the only status admitted to archive" and delegates the value domain and transition owner to acceptance-hardening.md § Feature Status; plan.md:36 (row II) cites only Feature 099's status (`Ready for Review`).

**evidence_not_supported**: The claim that plan/requirements contain no ruling scoping archive admission to the retirement lane or placing slice archival outside it — contradicted by requirements.md:134 (FR-020: slice archival MUST NOT be retirement archival; destination confined to `<parent>/slices/`; MUST NOT write/query `.specify/archive/`; MUST NOT query `archive-gate`; independent-spec retirement remains with `/speckit.sanitize`'s archive lane), requirements.md:25, requirements.md:82, requirements.md:207 (same ruling restated), and plan.md:70 (T-001: "不写 `.specify/archive/`、不查 `archive-gate`"). The admission rule constitution.md:571 points to is a feature-status gate owned by `archive-gate` (acceptance-hardening.md:70-72; seal-utils.py:2867-2875 operates on a spec status pair), and slice directories carry no feature status, so the claimed constitutional conflict does not arise; plan.md:36 is the Principle-II check row, not the ruling surface for the Feature Governance clause. Could not observe any artifact asserting that slice archival writes `.specify/archive/` or queries `archive-gate`.
READ-DOMAIN-CHECK: .specify/specs/100-seal-slice-archive/plan.md:24-94; .specify/specs/100-seal-slice-archive/requirements.md:1-145,168,207; .specify/constitution.md:555-584; .specify/shared/workflow/acceptance-hardening.md:55-89; .specify/shared/definitions/non-disposable-definitions.md (grep hits: 168,281,328,340-372,400,410,470,668); .specify/scripts/python/seal-utils.py:2840-2909
VALIDATOR-DONE

### D-02 — confirm — same

**evidence_supported**: Constitution I states "Every technical decision MUST trace back to specific requirements in the specification" (`.specify/constitution.md:183`, within the § I block at 179-186). plan.md:35 marks row I ✅ Pass on the evidence "每条设计裁决引用 FR id；`feature-ref.md` § Delivery map 覆盖 28/28 FR；074 回合由 FR-025/FR-026/SC-001 直接规定", and plan.md:37 identifies the plan's decisions as "六条承重取舍记为 T-001…T-006". The `decision` fields of all six records carry no FR id — plan.md:70 (T-001), :82 (T-002), :94 (T-003), :106 (T-004), :118 (T-005), :130 (T-006) — and T-001/T-002/T-003/T-005 contain no FR reference anywhere in their ranges (plan.md:68-78, 80-90, 92-102, 116-126); the only FR ids in § Decision Tensions appear inside `pole_a`: FR-018 at plan.md:109 (T-004) and FR-019 at plan.md:133 (T-006). feature-ref.md:15-48 is a generated FR-001…FR-028 → contract-clause table (generator note at feature-ref.md:50), so it establishes 28/28 FR coverage by contract clauses, not a decision → FR mapping; a repository-wide search of plan.md finds FR ids only at lines 35, 51, 109, 133, 231-234, i.e. no section supplies the per-decision citations row I claims.

**evidence_not_supported**: The blanket phrasing "T-001…T-005 decisions without FR ids" is over-broad if read at entry level: T-004 does cite FR-018, inside `pole_a` (plan.md:109), so 4 of 6 records (T-001/T-002/T-003/T-005) carry no FR id at all while two (T-004, T-006) carry exactly one, each only in `pole_a`. The claim's contrast singling out T-006's FR-019 while omitting T-004's FR-018 understates that pattern. Also unestablished from the cited locations: whether the six decisions are substantively untraceable — i.e. whether `requirements.md` FRs actually correspond to each decision; the artifacts observed support only the absence of explicit FR citations in plan.md and the unsupported "每条…" gate evidence, not the impossibility of retrospective mapping.
READ-DOMAIN-CHECK: .specify/constitution.md:165-199; .specify/specs/100-seal-slice-archive/plan.md (lines 20-150 read in full, plus FR-id grep across the whole file; wc -l = 276); .specify/specs/100-seal-slice-archive/feature-ref.md:1-60; skills/internal/analyze-artifacts/references/detection-and-severity.md:1-160 (severity taxonomy); .specify/shared/workflow/objective-analysis-gate.md (full)
VALIDATOR-DONE

### D-03 — confirm — CRITICAL

**evidence_supported**: `.specify/constitution.md:206-213` — Principle IV is MUST-level and line 209 states "Pure functions/utilities MUST have unit tests", with line 211 assigning contract/integration tests a separate scope (cross-service/external APIs). `.specify/specs/100-seal-slice-archive/plan.md:20` declares testing as "pytest（`contract` / `integration` 标记）" only. `plan.md:248-253` (P1–P4) names only `tests/contract/test_seal_engine_contract.py`, `tests/contract/test_seal_boundaries.py`, `tests/contract/test_seal_merge_plan.py`, `tests/integration/test_seal_merge_determinism.py`, `tests/integration/test_seal_074_round.py`, `tests/contract/test_seal_archive_plan.py`, `tests/contract/test_seal_archive_manifest.py`, `tests/contract/test_seal_archive_apply.py`, `tests/integration/test_seal_archive_idempotency.py` — all contract or integration; P5–P8 (plan.md:254-257) name no unit module either. `tasks.md:227-234` adds the deterministic helpers — path/line/section classifier (T024), closure arithmetic and digest (T027), single schema validator (T029), C-034 digest recompute (T030). A full scan of `tasks.md` test paths (lines 34–359) yields only `tests/contract` and `tests/integration`; no `tests/unit/` path appears anywhere in the file. `plan.md:38` nevertheless records Principle IV as Pass, so the plan asserts compliance while planning no unit-test deliverable.

**evidence_not_supported**: The characterization of the four named helpers as "pure functions/utilities" under Principle IV is an interpretive step — the constitution does not define that term and nowhere states that function-level tests inside contract modules cannot satisfy line 209; the artifacts therefore establish "no unit-test category/module is planned", not that the helpers are untested in principle. The test modules do not yet exist, so their future contents (whether they would include function-level red-first cases) are unobservable. CRITICAL is a severity classification, not a fact recorded in the cited artifacts; a reader could argue the contract/integration tests indirectly exercise these helpers and cap the practical consequence at a granularity/localization gap rather than a gate failure.
READ-DOMAIN-CHECK: .specify/constitution.md (lines 195-229); .specify/specs/100-seal-slice-archive/plan.md (lines 1-40, 235-269); .specify/specs/100-seal-slice-archive/tasks.md (lines 210-259); grep of `.specify/specs/100-seal-slice-archive/` for "unit" and of tasks.md for `tests/(unit|contract|integration)`
VALIDATOR-DONE

### F-01 — confirm — same

**evidence_supported**: requirements.md:99 states "同一分片两端同时存在：按输入缺陷退出 `2`" as part of the 部分归档 edge case; requirements.md:100 assigns the same presence condition ("目标目录已存在且源也存在") to `destination-exists` 拒绝（退出 `1`）— the two adjacent bullets give one physical state two incompatible exit codes and reason classes. requirements.md:41 (US1 AS-3) describes the identical state "一个分片目录仍留在源位置而同名目标已存在于 slices/" but only says "以具名理由拒绝，两个目录都不被改动", specifying no exit code, so it does not disambiguate. The ambiguity is normative, not editorial: requirements.md:120 (FR-006) requires "每个分片在源与目标中恰好存在一侧。任一不成立 MUST 拒绝或按输入缺陷退出" — leaving "拒绝" vs "输入缺陷" as alternatives — and FR-008 (requirements.md:122) fixes the closed exit set as 0/1/2 without mapping this state. Downstream, contracts/archive-actions.contract.md:20 (C-103) lists both `destination-exists` (exit 1) and `partial-archive` (exit 2) as distinct closed reasons, and archive-actions.contract.md:14 (C-102 ⑤) repeats the same "拒绝（1）或按输入缺陷退出（2）", so the overlap is not resolved there either.

**evidence_not_supported**: The cited locations do not by themselves demonstrate test or implementation impact — no tests or engine code were read, so both are inferred from the exit-code contract, not observed. Whether an implementer can disambiguate 99 vs 100 by any unstated differentiator (cause of the pre-existing destination, content, manifest registration) is not observable — neither bullet mentions cause or content, so the reading that they are the same state is an interpretation, though it is the only one the text supports. The claim also omits that requirements.md:120 and contract C-102 ⑤ were already permissive ("拒绝或…退出 2"), which widens the defect beyond the two edge bullets rather than narrowing it.
READ-DOMAIN-CHECK: .specify/specs/100-seal-slice-archive/requirements.md (lines 30-114, plus grep hits); .specify/specs/100-seal-slice-archive/contracts/archive-actions.contract.md (lines 16-37, plus grep hits); grep survey of .specify/specs/100-seal-slice-archive/contracts/ (reference-classification.contract.md, archive-manifest.contract.md hits only); directory listing of .specify/specs/100-seal-slice-archive/
VALIDATOR-DONE
```

### F-02 — confirm — same

**evidence_supported**: FR-006 requires the conjunct "合并清单存在且 `merge.status` 为已完成" and states "任一不成立 MUST 拒绝或按输入缺陷退出" (requirements.md:120); FR-007 requires an empty slice set to exit `0` and report `not-applicable` with basis (requirements.md:121); research.md:64 records `merge.status` as bivalent, `merged` or `not-applicable` (empty slice set, with `basis`); Clarification Q1 explicitly routes `merge.status == "not-applicable"` to exit `0` per FR-007 (requirements.md:213). Since `not-applicable` is not "已完成"/`merged`, the empty-set case fails FR-006's conjunction, and only Q1 carves it out — the FR-006 text contains no such exception.

**evidence_not_supported**: requirements.md:204 is the earlier session's trigger/`Sealed` Q, not the empty-set carve-out (that is :213), so that cited line does not itself substantiate "only Clarification Q1"; no artifact states the conflict in words — it is derived by combining FR-006's conjunct with research.md:64's bivalent domain; contracts/tests/implementation were not read, so the propagation surface is projected from the FR text rather than observed.
READ-DOMAIN-CHECK: .specify/specs/100-seal-slice-archive/requirements.md:95-234; .specify/specs/100-seal-slice-archive/research.md:40-89
VALIDATOR-DONE

### F-03 — confirm — HIGH

**evidence_supported**: FR-027 at `.specify/specs/100-seal-slice-archive/requirements.md:141` is explicitly scoped: "仓库 MUST NOT **因本特性新增**第二套处置词表、第二个归档引擎……", while SC-009 at `.specify/specs/100-seal-slice-archive/requirements.md:172` states without any baseline qualifier: "仓库中不存在第二套处置词表、第二个归档引擎或第二份按 spec 的归档清单". The baseline premise is substantiated: `.specify/specs/100-seal-slice-archive/research.md:29` records that sanitize's disposition set is five values and "与 non-disposable 四值是两套封闭集", and `research.md:26-31` records the sanitize archive lane (`archive-gate`, apply writing `.specify/archive/<rel>`, `ARCHIVE_REL`). Primary sources confirm the two closed sets: `scripts/python/sanitize-utils.py:35` (`DISPOSITIONS = ["delete","archive","repair","delegate","dismiss"]`) and `.specify/shared/definitions/non-disposable-definitions.md:275-292` (closed four-value set with a single owner); `research.md:17` even states "两套词表互不合并". So SC-009's unqualified "仓库中不存在第二套处置词表" is false at baseline, whereas FR-027's qualified form is satisfiable.

**evidence_not_supported**: The cited artifacts do not characterize the baseline sanitize archive lane as an "归档引擎"/engine — `research.md:22-33` and `requirements.md:134` call it a "归档 lane" — so the "第二个归档引擎" half of the claim rests on a looser reading than the two-vocabularies half. "Can never pass" holds only for SC-009 as literally worded; a baseline-relative or duplicate-detection implementation could satisfy the intent, but that would implement FR-027's qualifier rather than SC-009's text. No test run was performed; the baseline contradiction is established by artifact reading, not by observing a red audit.
READ-DOMAIN-CHECK: .specify/specs/100-seal-slice-archive/requirements.md (lines 120-189), .specify/specs/100-seal-slice-archive/research.md (lines 1-60), scripts/python/sanitize-utils.py (lines 28-41), .specify/shared/definitions/non-disposable-definitions.md (lines 272-295)
VALIDATOR-DONE

### F-04 — downgrade — MEDIUM

**evidence_supported**: requirements.md:132 (FR-018) does limit the merge-manifest update to "路径字段（至少 `slices[].carrier_tasks`、`dispositions[].evidence[]`、`artifacts[].pointer.paths[]` 与任何其他路径形态的值）" and does keep "合并结论、计数、冲突、ID 映射与分片顺序" unchanged; requirements.md:90 (US4 AS-1) does say "变化的只有路径字段、摘要、归档清单与被移动的目录"; requirements.md:168 (SC-005) does say "合并结论/计数/冲突不变", and requirements.md:181 makes the evidence an archive-before/after state snapshot. The propagation is real: tasks.md:233 (T030) restates the same shape predicate ("只改 `.specify/specs/<slug>[/…]` 形态的字符串值 … 及任何同形值") and tasks.md:251 (T037) asserts "除路径字段、摘要、归档清单与被移动目录外零变化"; no cited line defines a guard that mechanically asserts the delta set.

**evidence_not_supported**: "undefined aggregate 'path-shaped'" is contradicted by the cited contract: archive-manifest.contract.md:87 (C-211) defines the allowed delta as "字符串值中形如 `.specify/specs/<slug>[/…]` 的路径形态值（至少覆盖 … 与任何同形值）" — a shape predicate, so a derivation exists and the set is not left open-ended by the "至少" list. "No derivation" and "not mechanically derivable" are therefore overstated; what is actually missing is formal matching semantics (whole-value vs substring, `<slug>` grammar) and an explicit delta guard. "The complement assertion has no defined unit" is not established within the cited boundary: SC-005 names only 合并结论/计数/冲突 without units, but those may be defined by 099's merge-manifest owner (I did not read that schema in full). Also, SC-005 does not assert the full positive "only path fields changed" claim — it asserts three invariants plus no deletion/push/goal-team/`.specify/archive/` writes; the full positive delta is US4 AS-1. Bounded ambiguity in requirement-text precision and guard shape, with C-211 and T030 supplying an implementable predicate, supports MEDIUM rather than HIGH.
READ-DOMAIN-CHECK: .specify/specs/100-seal-slice-archive/requirements.md (lines 70–208); .specify/specs/100-seal-slice-archive/contracts/archive-manifest.contract.md (lines 60–96); .specify/specs/100-seal-slice-archive/tasks.md (grep hits at lines 23, 41, 126, 128, 146, 233, 234, 251); .specify/specs/100-seal-slice-archive/checklists/2026-11-11-requirements-quality.md (header and lines 41, 53); .specify/specs/099-speckit-seal/contracts/merge-back.contract.md (grep only, no unit definition found); verification.md confirmed absent
VALIDATOR-DONE
```

### F-05 — reject — same

**evidence_supported**: FR-025 at .specify/specs/100-seal-slice-archive/requirements.md:139 does require "全量测试 MUST 零新增红（按失败 node-id 名单比对，既有红不修不掩）"; tasks.md:75 and tasks.md:278 do define the comparison as `--names-out` capture plus `comm -13` against an implement-entry baseline owned by `/speckit.implement` step 6's `**Test runs**` bullet, with reading paths `test-evidence/final-failed.txt` and `test-evidence/final-suite.txt`.

**evidence_not_supported**: The assertion that the baseline is "never pinned (no commit, run record or artifact path)" is contradicted by the live owner chain the cited gate points at: `.specify/skills/internal/implement-feature/SKILL.md:181-189` (Step 6 "Implement feature", heading at :119) pins the artifact path convention `--names-out <spec-dir>/baseline-failed.txt` and the `comm -13 baseline current` form; the framework source `skills/internal/implement-feature/SKILL.md:188-189` carries the same text; `templates/commands/implement.md:44,48` delegates the command to that skill; `plan.md:20` pins the capture point as "实现入口实测并记名"; `templates/commands/implement.md:47` derives the set from `<spec-dir>/baseline-*` and treats a missing baseline as a first capture with provenance, never zero drift. I could not observe a concrete `baseline-failed.txt`, baseline commit or run record in spec 100, but implementation has not started and that is the defined pre-implementation state, not an unpinned requirement. Additionally, SC-001 (.specify/specs/100-seal-slice-archive/requirements.md:164, sources at :177) contains no full-suite zero-new-red clause, so the "SC-001 verification" propagation surface is unsupported.
READ-DOMAIN-CHECK: .specify/specs/100-seal-slice-archive/requirements.md (125-154, 164, 177); .specify/specs/100-seal-slice-archive/tasks.md (60-89, 265-294); .specify/specs/100-seal-slice-archive/plan.md:20; .specify/specs/100-seal-slice-archive/checklists/2026-11-11-requirements-quality.md:28; .specify/skills/internal/implement-feature/SKILL.md (42-57, 119, 175-208); skills/internal/implement-feature/SKILL.md (188-189); templates/commands/implement.md (44-72); directory listings of .specify/specs/100-seal-slice-archive/{,notes,test-evidence}
VALIDATOR-DONE
```

### C-01 — downgrade — MEDIUM

**evidence_supported**: requirements.md:120 (FR-006) lists the five conjunctive preconditions and says only "任一不成立 MUST 拒绝或按输入缺陷退出" with no per-conjunct exit code or reason. contracts/archive-actions.contract.md:14 (C-102) repeats conjuncts ①–⑤ and states only the disjunction "任一不成立 MUST 拒绝（`1`）或按输入缺陷退出（`2`）" — no conjunct→code/reason mapping. contracts/archive-actions.contract.md:20 (C-103) partitions the closed reason vocabulary by exit code (refusal: destination-exists, dirty-spec-tree, conflict-open, slice-unclosed, unresolved-references, unclassified-reference; error: merge-manifest-missing, merge-manifest-invalid, slice-missing, partial-archive, archive-drift, archive-manifest-invalid, not-a-git-tree, mirror-copy, write-failed) but never binds a reason to a conjunct. requirements.md:99-101 additionally assign conflicting dispositions to the same both-sides case (line 99 routes it to exit 2 "部分归档"; line 100 routes it to `destination-exists` exit 1; line 101 gives `slice-missing` exit 2 for both-absent).

**evidence_not_supported**: The consequence "two implementers can derive different exit codes for the same condition and FR-024 tests cannot pin one" is not supported by the full artifact set: plan.md:230 (Disclosed Ruling #1) resolves the layering (same-slice both sides → destination-exists exit 1; cross-slice partial or both-absent → exit 2), data-model.md:130 (V3) states both assignments, and tasks.md:194 (T010) requires a contract test pinning that layering. Conjuncts ②/③ are near-uniquely determined by C-103's reason names and exit partition (contract:20), and ④ is pinned by 099 records-and-boundaries.contract.md:63-67 (C-039 `dirty-spec-tree` refusal) with seal-engine.contract.md:14-18 (exit 1 = precondition refusal). I could not observe the `merge.status` value domain for a parseable manifest whose status is neither "merged" nor "not-applicable", so reachability of that residual conjunct-① ambiguity is unverified.
READ-DOMAIN-CHECK: .specify/specs/100-seal-slice-archive/requirements.md; .specify/specs/100-seal-slice-archive/contracts/archive-actions.contract.md; .specify/specs/100-seal-slice-archive/plan.md; .specify/specs/100-seal-slice-archive/data-model.md (grep+excerpt); .specify/specs/100-seal-slice-archive/tasks.md (grep); .specify/specs/100-seal-slice-archive/checklists/2026-11-11-requirements-quality.md (grep); .specify/specs/099-speckit-seal/contracts/seal-engine.contract.md; .specify/specs/099-speckit-seal/contracts/records-and-boundaries.contract.md (grep excerpt); .specify/specs/099-speckit-seal/contracts/merge-back.contract.md (grep)
VALIDATOR-DONE

### B-01 — confirm — HIGH (same)

**evidence_supported**: requirements.md:35 (US1 Independent Test) and requirements.md:177 (SC-001 Source) pin the plain `git diff --name-status -M` form with no comparison base and no staging step; requirements.md:164 makes SC-001 (Path: final) depend on rename pairs with zero pure deletions. contracts/archive-actions.contract.md:36-40 (C-106) mandates `git mv` semantics and MUST-level rename pairs under `git diff --name-status -M`, never pure deletion, and line 102 maps SC-001 to the same plain command. data-model.md:129 (V2) is the same form. quickstart.md:92-95 (S-3) runs the plain command after `archive-apply` and before the archive-batch commit, expecting `R` per file and zero `D`. tasks.md:63 (DoD-4), tasks.md:197 (T013), tasks.md:268 (T043) repeat the plain form, and tasks.md:188 (US1 Independent Test) likewise. A directory-wide search found no `--cached`, `diff HEAD`, or base-commit qualifier in any spec artifact; `git mv` updates the index, so the default worktree-vs-index diff shows no rename pairs, and quickstart's diff runs exactly while the move is staged. checklists/2026-11-11-requirements-quality.md:26 (CHK010) independently records the same base/staging gap as **fail**.

**evidence_not_supported**: requirements.md:164 alone says "git 变更视图" generically rather than literally the plain command; the plain form is pinned by its Measurement Source at requirements.md:177 — the claim's substance still holds but line 164 by itself does not assert it. I did not execute a live git reproduction (validator is read-only, no files written); the staging premise is standard git behavior, corroborated by CHK010. No cited artifact records the implementation's actual staging choice; however, under the plain form neither an unstaged move (only `D` rows for old paths, untracked new paths absent from `git diff`) nor a staged move (empty output) yields per-file `R` pairs, so the unobservability conclusion does not depend on that choice.
READ-DOMAIN-CHECK: .specify/specs/100-seal-slice-archive/requirements.md; .specify/specs/100-seal-slice-archive/contracts/archive-actions.contract.md; .specify/specs/100-seal-slice-archive/data-model.md; .specify/specs/100-seal-slice-archive/quickstart.md; .specify/specs/100-seal-slice-archive/tasks.md; .specify/specs/100-seal-slice-archive/checklists/2026-11-11-requirements-quality.md; directory-wide grep over .specify/specs/100-seal-slice-archive/*.md (surfaced plan.md:18,213 and feature-ref.md:77)
VALIDATOR-DONE

### F-06 — downgrade — MEDIUM

**evidence_supported**: C-110 (contracts/archive-actions.contract.md:62), V14 (data-model.md:141) and quickstart S-6 (quickstart.md:153) all set the completion criterion as "父 spec、分片与全部 live 载体的 sha256 等于清单记录的 before 值". The manifest's closed field set records whole-file sha256 only in slices[].files[] (contracts/archive-manifest.contract.md:39; data-model.md:67); references.rows[].before is 命中整行原文 and references.runtime[].updates[].before is also line text (contracts/archive-manifest.contract.md:45,51; data-model.md:78,88); pinned_commit is a 40-hex commit id (contracts/archive-manifest.contract.md:22,63) and merge_manifest.digest_before/after are sha256 digests of the merge manifest alone (contracts/archive-manifest.contract.md:27,87; data-model.md:53,111). No top-level or row-level field carries a per-carrier content hash (contracts/archive-manifest.contract.md:14-31,57), so the literal comparison "carrier sha256 == manifest-recorded before value" lacks a recorded operand for the parent spec and live carriers.

**evidence_not_supported**: The blanket "cannot be computed from the manifest as specified" overstates impact: the manifest records pinned_commit plus each carrier path (references.rows[].carrier, contracts/archive-manifest.contract.md:45), so pre-archive bytes of versioned carriers and the parent-spec tree are reconstructable via git, and slice content hashes are already recorded (slices[].files[].sha256). SC-010's own declared Source is a fixture before/after tree-hash comparison (requirements.md:186; contracts/archive-actions.contract.md:111), and FR-011 requires only per-slice file hashes plus per-reference before/after (requirements.md:125), not per-carrier whole-file hashes; whether runtime state carriers fall inside "全部 live 载体" is also not established. The surviving defect is a mis-stated normative completion criterion in three artifacts — real and needing wording repair, but it does not block a computable SC-010 oracle, so MEDIUM rather than HIGH.
READ-DOMAIN-CHECK: .specify/specs/100-seal-slice-archive/contracts/archive-actions.contract.md (1-120); .specify/specs/100-seal-slice-archive/data-model.md (1-180); .specify/specs/100-seal-slice-archive/quickstart.md (100-199); .specify/specs/100-seal-slice-archive/contracts/archive-manifest.contract.md (10-79 + grep); .specify/specs/100-seal-slice-archive/requirements.md (grep-selected lines 9, 80-91, 118-125, 138, 150, 169-186, 215-216)
VALIDATOR-DONE

### F-07 — confirm — HIGH

**evidence_supported**: `.specify/specs/100-seal-slice-archive/contracts/archive-manifest.contract.md:63` (C-207) states "清单中所有路径 MUST 是仓库根相对 POSIX 字符串" — a universal MUST over every path value in the manifest; `.specify/specs/100-seal-slice-archive/contracts/archive-manifest.contract.md:39` (C-203) defines `files` as `[{path, sha256}]` with "`path` 是该分片目录内相对 POSIX 路径" (slice-directory-relative), which is not repo-root-relative; `.specify/specs/100-seal-slice-archive/contracts/archive-manifest.contract.md:27` (C-202) fixes the literal `"merge_manifest": {"path": "merge-manifest.json", ...}`, a value relative to the manifest's own (parent-spec) directory, which under a repo-root-relative reading would wrongly denote `<repo-root>/merge-manifest.json`; `.specify/specs/100-seal-slice-archive/tasks.md:203` (T016) requires "逐片条目（…`files[{path,sha256}]`…）" together with "仓库根相对 POSIX 路径", restating the universal rule over the same emitted slice-relative field; `.specify/specs/100-seal-slice-archive/data-model.md:47,64` mark `spec_path`/`from`/`to` as repo-root-relative while `.specify/specs/100-seal-slice-archive/data-model.md:67` marks `files[].path` as "分片目录内" relative, confirming two path conventions are intended and C-207's universal wording is unsatisfiable against the very key set its own contract page defines.

**evidence_not_supported**: The finding's propagation to actual tests and implementation is prospective only — `tasks.md:196` (T012) and `tasks.md:203` (T016) are unchecked, and no `scripts/python/seal-utils.py` behavior, emitted manifest, or failing test was observed; the "no single convention satisfies both clauses" conclusion is a textual/logical inference from the cited clauses (no qualifier scoping C-207 to manifest-level paths exists anywhere in the contract or the read data-model section), not an observed runtime defect; severity HIGH is a review-stage judgement, not a measured field effect.
READ-DOMAIN-CHECK: .specify/specs/100-seal-slice-archive/contracts/archive-manifest.contract.md (full, lines 1-96); .specify/specs/100-seal-slice-archive/tasks.md (lines 190-219, plus grep hit at 103); .specify/specs/100-seal-slice-archive/data-model.md (lines 38-82); directory-wide grep for "仓库根相对|分片目录内相对|相对 POSIX" under .specify/specs/100-seal-slice-archive
VALIDATOR-DONE

### F-08 — confirm — HIGH

**evidence_supported**: C-116's SC→首红模块 table names `tests/integration/test_seal_archive_round.py`（rollback） for SC-010 at contracts/archive-actions.contract.md:111 (clause at :96), and a grep of that contract finds no revised C-116 or any mention of `test_seal_archive_rollback.py`. tasks.md:151 traces SC-010 to T033 with `tests/integration/test_seal_archive_rollback.py`（见 § Notes 裁定 1）; tasks.md:247 (T033) writes that same rollback file; tasks.md:67 (DoD-8 Check) runs `tests/contract/test_seal_boundaries.py tests/integration/test_seal_archive_rollback.py`; tasks.md:359 (Notes 1) explicitly states C-116 writes round.py（含 rollback）and that this stage places rollback assertions in an independent file, i.e. it acknowledges the mapping is being changed while C-116 itself is not revised.

**evidence_not_supported**: verification.md does not exist yet in this spec directory, so an already-materialized conflict in verification records is not observable; the propagation into verification is prospective. The claim does not address the stated rationale for the divergence (green-path-divergence between T018/C-107 and T033/C-110 on one path), which is recorded at tasks.md:359 but does not amend the clause owner.
READ-DOMAIN-CHECK: .specify/specs/100-seal-slice-archive/contracts/archive-actions.contract.md (lines 80-129, grep rollback|C-116|SC-010); .specify/specs/100-seal-slice-archive/tasks.md (lines 55-84, 142-166, 240-259, 350-364); .specify/specs/100-seal-slice-archive/verification.md (attempted, absent)
VALIDATOR-DONE
```

### F-09 — confirm — same

**evidence_supported**: tasks.md:148 maps SC-007 to task row T027 with module `tests/contract/test_seal_archive_manifest.py`; tasks.md:149 maps SC-008 to T026 with `tests/contract/test_seal_archive_apply.py`（runtime 夹具）. T027 (tasks.md:230) is an engine-implementation row ("补齐 `checks` 与摘要记账…三组闭环算术成立…`digest` 覆盖完整文档…`pinned_commit`"), carrying only `[green: ...C-206/C-207]` and naming no test file; T026 (tasks.md:229) is likewise implementation ("实现引用台账与运行期载体…"). T012 (tasks.md:196) is the row that authors `test_seal_archive_manifest.py`, and its scope is key sets, serialization, digest algorithm, path hygiene and plan byte-determinism — no closure-arithmetic recomputation and no delete-row mutation. T013 (tasks.md:197) authors `test_seal_archive_apply.py` with pure-move, read-only recompute, `already-archived`, zero-persistence and non-git-tree cases — no runtime present/absent cases and no absent→blocked mutation. T022 (tasks.md:222) only creates the `runtime-present/` fixture; scanning all rows T023–T053 (tasks.md:223-285) no row names that fixture or authors a runtime test; T031 (tasks.md:234) extends the manifest test only for `schema_version` discipline, and T049/T050 (tasks.md:281-282) produce trace/verification records from existing evidence without authoring tests. Contract C-116 (contracts/archive-actions.contract.md:108) requires SC-007 evidence as "三组闭环算术复算；删行变异转红" in `test_seal_archive_manifest.py`, and (contracts/archive-actions.contract.md:109) SC-008 evidence as "存在/缺席两类；缺席转阻断变异转红" in `test_seal_archive_apply.py`（runtime 夹具）— neither required form is written by any task row.

**evidence_not_supported**: Nothing in the claim exceeds what the cited task and contract text substantiates; the only limits are observational — plan.md and any on-disk test bodies were not read because the claim is about the task-to-SC trace, and the cited locations do not enumerate what the "three closure-arithmetic groups" are (only that T027 asserts them as implementation behavior). The claim's "no row writing the SC-008 test" holds for tasks.md as read in full (T001–T053); an artifact outside tasks.md assigning that work elsewhere was not observed.
READ-DOMAIN-CHECK: .specify/specs/100-seal-slice-archive/tasks.md:130-364; .specify/specs/100-seal-slice-archive/contracts/archive-actions.contract.md:85-113
VALIDATOR-DONE

### F-10 — confirm — HIGH

**evidence_supported**: requirements.md:119 (FR-005) enumerates the per-slice tuple as `{slug, from, to, file_count, files[{path, sha256}], merged_into_pointer}` — six fields, no `order`; archive-manifest.contract.md:4 declares the contract page owns the top-level and nested field **closed sets**, and archive-manifest.contract.md:37-41 (C-203) declares `slices[]` elements "恰含" seven fields `slug`、`from`、`to`、`order`、`file_count`、`files`、`merged_into_pointer`, deriving `from`/`to` from `slug` and ordering by `order`; tasks.md:203 (T016) enumerates `from`/`to`/`order`/`file_count`/`files[{path,sha256}]`/`merged_into_pointer` — six fields, `order` present, `slug` absent — while carrying the `[green: ...#C-203]` anchor, and grep of tasks.md for `C-203` returns only line 203, so T016 is the sole green-claiming row and its carried enumeration conflicts with the owner it must satisfy. FR-023 (requirements.md:137) corroborates that the manifest schema is owned by this contract page.

**evidence_not_supported**: FR-005's tuple sits inside a "closed set MUST cover …" clause with a separate "分片顺序与顺序依据" coverage item, so reading it as itself a standalone closed-set declaration is interpretive — the literal six-field omission of `order` is observed, but the cited line does not literally label that tuple the closed set; no implementation or test file was read, so the downstream effect (an emitted manifest lacking `slug`) was not observed. Severity is not overstated: the omitted field is the slice identity from which C-203 derives `from`/`to` and by which FR-019 slice discovery would match archived slices.
READ-DOMAIN-CHECK: .specify/specs/100-seal-slice-archive/requirements.md (lines 100-139); .specify/specs/100-seal-slice-archive/contracts/archive-manifest.contract.md (lines 1-64); .specify/specs/100-seal-slice-archive/tasks.md (lines 190-219); grep `C-203` over .specify/specs/100-seal-slice-archive/tasks.md
VALIDATOR-DONE

### F-11 — confirm — HIGH

**evidence_supported**: requirements.md:127 (FR-013) mandates that live references be rewritten in the same apply batch and puts `.specify/register.md` 的推荐行 and 特性详情的活指针区 inside the mandatory carrier floor; contracts/reference-classification.contract.md:41 (C-303, the cited line range 39-43) declares `.specify/register.md` and `.specify/features/<ID>.md`'s `## Related Specifications/Requirements` as live carriers, and C-301's table at reference-classification.contract.md:14,16 classifies them live / mixed-live. requirements.md:142 (FR-028) closes the write surface: allowed writes are (a) slice moves, (b) 父 spec 的活引用文件、归档清单与 merge-manifest.json 路径字段, (c) 契约声明的框架 owner 文档与镜像、测试文件, (d) runtime state; it adds "MUST NOT 写声明集合之外的路径" and "静态审计以引擎写路径白名单为准，白名单外的写路径出现时审计测试 MUST 转红". The contract itself separates `.specify/specs/<parent>/` (C-301:12), `.specify/register.md` (C-301:14) and `.specify/features/<ID>.md` (C-301:16) as distinct scan roots, and identifies the framework source/mirror class as `shared/**` + `.specify/shared/**` (C-301:19), so neither registry file is a "父 spec 的活引用文件" nor a "框架 owner 文档与镜像"; requirements.md:168 and :181 make the write-surface static audit part of SC-005 evidence, so the two required live carriers fall outside the audited whitelist exactly as claimed.

**evidence_not_supported**: The live-carrier roster at the cited lines 39-43 is C-303, not C-301 (minor label error; C-301's own rows at :14,:16 still support the classification, and :39-43 clearly support "live carriers"). "The allowlist that SC-005 audits" slightly conflates SC-005's own wording (deletion/status-write injections turn red, requirements.md:168) with FR-028's statement that the static audit is whitelist-based (:142) plus SC-005's evidence line (:181); the audit linkage is real but indirect. I did not observe any clause adding the two registry files to a writable set: archive-actions.contract.md:4 claims ownership of 写面白名单 but its clauses (C-106 pure move, C-108 "活引用改写" without carriers) enumerate no registry path, and 099 seal-engine.contract.md:63-69 (C-008) covers only the pre-existing seal write surface. I did not verify, per-tree, that the 074 round actually contains live hits in both carriers; the contradiction is normative (required-capability vs closed allowlist), not a measured hit count.
READ-DOMAIN-CHECK: .specify/specs/100-seal-slice-archive/requirements.md (110-159, 160-181, 200-229); .specify/specs/100-seal-slice-archive/contracts/reference-classification.contract.md (1-80); .specify/specs/100-seal-slice-archive/contracts/archive-actions.contract.md (1-114); .specify/specs/099-speckit-seal/contracts/seal-engine.contract.md (1-90); directory listing of .specify/specs/100-seal-slice-archive/contracts/
VALIDATOR-DONE
```

### F-12 — confirm — HIGH

**evidence_supported**: FR-028 clause (a) is verbatim "分片目录在父 spec 树内的移动", and the same sentence makes that whitelist the audit criterion: "静态审计以引擎写路径白名单为准，白名单外的写路径出现时审计测试 MUST 转红" (`.specify/specs/100-seal-slice-archive/requirements.md:142`). The spec places the move source outside the parent spec tree: `.specify/specs/100-seal-slice-archive/requirements.md:8` ("从 `.specify/specs/` 同级目录移入父 spec 的 `slices/`"), `:21` (074a/074b are siblings under `.specify/specs/`), `data-model.md:32-33` (`source` = `.specify/specs/<slug>`; `destination` = `.specify/specs/<parent>/slices/<slug>`), `contracts/archive-manifest.contract.md:39` (`from = .specify/specs/<slug>`; `to = <spec_path>/slices/<slug>`), and the reverse move `git mv <spec_path>/slices/<slug> .specify/specs/<slug>` (`contracts/archive-actions.contract.md:62`). FR-002 fixes only the destination `<父 spec 目录>/slices/<原分片目录名>/` (`requirements.md:116`). SC-005 consumes the static audit as evidence (`requirements.md:168,181`; `contracts/archive-actions.contract.md:106`). Hence `.specify/specs/<slug>` is outside `.specify/specs/<parent>/`, and clause (a) — read as movement within the parent tree — does not name the source side.

**evidence_not_supported**: (1) `requirements.md:116` (FR-002) states only the destination, not the `.specify/specs/<slug>` source; that half comes from `requirements.md:8,21`, `data-model.md:32-33` and `archive-manifest.contract.md:39`, so "FR-002 defines the move pair" is imprecise at the cited line. (2) `contracts/archive-actions.contract.md:36-40` (C-106) establishes pure move/rename with zero pure deletion but does not state the source location. (3) SC-005's own text (`requirements.md:168`) does not name the write-path whitelist; "sole basis" is inferred from FR-028:142 and the SC-005 Source line (`requirements.md:181`). (4) No audit implementation or test output was observed, so "the audit would red on the legal move" is a consequence of the literal reading, not a measured result; the same clause could also be implemented destination-only, which would let the source-side change pass without an explicit authorization.
READ-DOMAIN-CHECK: `.specify/specs/100-seal-slice-archive/requirements.md` (read 100-159; grep hits 8,21,86,92,116,137,142,164,168,181); `.specify/specs/100-seal-slice-archive/contracts/archive-actions.contract.md` (read 1-119; grep); `.specify/specs/099-speckit-seal/contracts/seal-engine.contract.md` (grep C-001/C-008 regions); grep-observed only: `.specify/specs/100-seal-slice-archive/data-model.md:32-33`, `.specify/specs/100-seal-slice-archive/contracts/archive-manifest.contract.md:39`, `.specify/specs/100-seal-slice-archive/checklists/2026-11-11-requirements-quality.md:56`
VALIDATOR-DONE

## 11. Remediation disposition records

All fixes are text-level artifact edits applied by this unattended analyze run under the Analyze-gate exception. Each fix was re-checked by the round-2 deterministic gates and the round-2 detection wave; no engine/implementation change was made. Detailed locations: see `analyze-dispositions.md`.

## 12. Round-2 rerun delta

**Round-2 wave**: 5 fresh workers over disjoint domains (R1 requirements; R2 two contracts; R3 ref-classification+tasks; R4 plan/data-model/quickstart; R5 feature-ref/checklists/registry/constitution). R2 hit its output-token limit on the first attempt; it was retried as two smaller fresh workers (R2a archive-actions, R2b archive-manifest), preserving independent detection. Every worker's `READ-DOMAIN-CHECK` matched its declaration.

**Resolved since round 1**: all 16 fixed round-1 findings were re-read and marked RESOLVED by the round-2 workers (D-02, D-03, F-01, F-02, F-03, F-04, F-06, F-07, F-08, F-09, F-10, F-11, F-12, C-01, B-01, plus C-02/C-03/C-04/B-02/B-03/B-04/B-05/B-06/B-07/C-05/C-06/C-08/C-09/C-10/C-11/C-12/F-19…F-34/E-01/G-01/F-15/F-16/F-17/W5-F-02/W5-F-03/I-01/I-02 and the A-02/E-01 trace items). The two rejected round-1 findings (D-01, F-05) remain rejected with the validators' evidence boundaries.

**New since round 1 (round-2 detection; repaired in the same pass)**:
| ID | Severity | New defect | Fix |
|----|----------|-----------|-----|
| R1/N-01 | HIGH | RS-002 joint acceptance "全绿且零新增红" conflicts with FR-025's pinned-baseline set difference | RS-002 now states the set-difference criterion; pre-existing red is explicitly not repaired/masked |
| R1/F-01 (reopened) | HIGH | FR-006 ⑤ "each slice on exactly one side" is satisfied by cross-slice mixing, so the conjunction admits an apply the Edge Case forbids | ⑤ now requires all slices on the **same** side; cross-slice mixing and all-at-destination-without-manifest map to `partial-archive` / `archive-drift` exit 2 (FR-006, C-102) |
| R1/F-04 | HIGH | FR-018's complement clause "values outside the matched set byte-identical" includes the recomputed `digest` | complement now exempts `digest` (recomputed per C-034); C-211/T030 aligned |
| R1/N-04 | HIGH | SC-005 "no push" had no oracle; the write-path audit cannot observe an external subprocess | T034 now audits the engine external-command allowlist (`git mv`/`status`/`diff`/`rev-parse`; `push` absent) and injects a `git push` mutation |
| R3/B-02 | HIGH | C-311 identity constant vs F3 was unsatisfiable on `assert make(".specify/specs/<slug>") == "<slug>"` | C-302 F3 now requires the slug literal to be part of a path-construction expression; identity comparison literals are excluded; F1 beats F3 |
| R3/RC-N01 | HIGH | F1/F2 lacked token boundaries; absolute paths and `../<slug>` matched; cross-line forms were undetectable | F1/F2 now carry explicit left/right boundaries and `<slug> ∈ manifest slices`; cross-line/absolute carriers with a slug literal and no line-level form are `unclassified-reference` |
| R3/RC-N02 | HIGH | "all rename pairs" was asserted over the whole batch, which also adds the manifest and modifies merge/live carriers | rename assertion scoped to the moved-slice path set; declared A/M set asserted separately; global zero D (C-106, SC-001, V2, T013/T043/DoD-4, feature-ref) |
| R3/RC-N03 | HIGH | one `reference-matrix/` fixture was both the clean apply case and the unclassified-blocking case | split into clean `reference-matrix/` and `reference-matrix-unclassified/` (T022, US2 IT, T023) |
| R3/F-11-F-12 | HIGH | no row asserted the C-303 parent `seal.md` non-rewrite prohibition | T022/T024 carry a `seal.md`-bearing fixture with a byte-identity assertion; DoD-8 and T037 include `seal.md` byte-identity; FR-028 trace adds T024 |
| R4/N-02 | HIGH | four decision-tension records let the chosen design satisfy both poles (criterion 3 inadmissible) | all six `pole_b` constraints rewritten to the value the chosen design actually sacrifices (single archive root, unarchived seal tree, zero-jump readers, single-file reading, any-form migration, zero-new discovery); expected sacrifices aligned |
| R4/N-03 | HIGH | round/rollback test files and the rollback fixture had no file-level write domain owner | plan P4 owns `test_seal_archive_round.py`; P7 owns `test_seal_archive_rollback.py`; P8 records the rollback replay (clean-pair) and concurrent fixture |
| R5/N-01 | HIGH | the requirements-stage checklist annotation claimed repairs while citing no analyze receipt | annotation now cites `analyze-merged-2026-11-11.md` + `analyze-dispositions.md`; registry row/detail carry the dated analyze note |
| R2a/N-01 | HIGH | "unique exit code" undecidable when conditions of different classes co-fail; no evaluation order; unevaluable conditions undefined | C-102 now fixes the order (already-archived first; error class 2 over refusal 1; numbered order) and reports blocked conditions as `not-evaluated (blocked-by …)` |
| R2a/N-02 | HIGH | C-110 deleted the manifest before step ④ used it; `git diff` ignores the untracked manifest | rollback plan loaded before deletion; manifest removed last; criterion adds `git status --porcelain` (untracked included) |
| R2a/N-03 | HIGH | C-102 ④ dirty check did not cover live carriers outside parent/slices; C-110 whole-file restore could clobber out-of-flow edits | ④ now includes the C-301 live roster; whole-file restore is only within the in-flow carrier set |
| R2a/N-04/N-05 | MEDIUM | merge-manifest digest not exempt; manifest-absent fallback could read archived slices as "no slices" | digest exempted in ④; fallback only when `<parent>/slices/` is absent/empty, otherwise exit 2 |
| R2b/R2-01 | HIGH | C-210 `from` prefix mapping had no segment boundary, longest-match or uniqueness rule | C-210 now requires segment-boundary matching, longest `from`, and a unique mapping (ambiguity exits 2) |
| R2b/R2-02…R2-06 | MEDIUM | C-206 exit-code disjunction; C-209 "本节" referent; top-level-only rejection; `order`/counter types; C-211 match granularity | exit pinned to 2 (`archive-manifest-invalid`); C-209 cites C-202–C-206; per-level rejection stated; `order` 1-based contiguous unique int and counters int; whole-value/segment-boundary/single-replacement matching |
| R1/N-02…N-09, R3/RC-N04…N09, R3/C-11, R3/F-19, R4/N-01, R4/N-04, R4/F-22, R5/N-02…N-04 | MEDIUM/LOW | field-name drift (`relative_path`), SC-001/SC-002 reading windows, runtime zero-hit binary, plan package counts/write targets, T003 `[P]`+blockedBy contradiction, scan-root overlap, merge-manifest hit domain, DoD-8 "状态写", F1 slug roster, T027 path basis, tension_id body lines, S-6 pathspec, state-machine rows, checklist owner pointer, checklist arithmetic, feature-ref owner-page count | all repaired as listed in `analyze-dispositions.md` |

**Round-3 verification sample**: `V1-requirements` — all round-1/R1 findings RESOLVED; one new HIGH (FR-006's inline exit-2 reason list looked exhaustive but omitted owner-mapped reasons) — fixed by replacing the inline enumeration with a C-102/C-103 owner pointer. `V2-actions` — clean (all R2a findings RESOLVED, no new findings). `V2b-refclass` — one new HIGH (the carrier-level catch-all would flag the contract's own post-apply rewrite outputs/identity constants, breaking idempotence) — fixed by narrowing the catch-all to source-path occurrences and exempting archived paths/identity bare-slugs. `V3-plan-tasks` — all prior findings RESOLVED; four new HIGHs (S-6 criterion used `to` paths after the inverse move; `seal.md` ban unqualified vs template edits; plan package anchors vs green ownership; plan write targets without task rows) — all fixed. **Round-3 new C/H total: 6, all repaired.**

**Round-2 residue (open, non-blocking)**:
- **A-01** (MEDIUM, deferred): contract determinism duplication (C-109 vs C-208; C-201 vs C-111; C-105 vs C-111) — one-owner-per-property cleanup, no execution dependency.
- **R1/N-03** (MEDIUM, deferred): requirements-level field/reason enumerations coexist with the contract owners (FR-005/FR-006 vs C-203/C-103). The copies are currently aligned and machine-checked; a future one-source cleanup should collapse them. Accepted as layered coverage for this feature, recorded rather than hidden.
- **Dated evidence note** (not a finding): `test-evidence/tasks-stage-checks.txt` baseline line/header count transcription; the dated record is preserved and the accountant's measured reading is authoritative.

**Round-2 gate readings**: pre-analyze plan/tasks pass (errors=0, advisories=2 intentional placeholders); validate-requirements 0/0; validate-tasks 0/0; decomposition proceed (28 FR / 53 tasks); decision-tensions 6 records / 0 error / high=0; coverage claimed 40 / FR 28/28 / 0 beyond baseline; unparsable corpus lane unchanged (108 files, 1 parse doubt).

**Final verdict**: **0 open CRITICAL / 0 open HIGH**. The round-1 validated set is closed (15 repaired, 2 rejected with evidence); the round-2 and round-3 new C/H (16 + 6) were detected by independent fresh-context workers, repaired in the same pass, and re-checked by the deterministic gates and targeted re-reads. `/speckit.implement` may proceed.

## 13. Next actions

- CRITICAL/HIGH open count is 0 after remediation: `/speckit.implement` may proceed.
- Deferred residue (MEDIUM/LOW, non-blocking): contract-level determinism duplicates (A-01), the layered requirements-level enumerations (R1/N-03), and the dated tasks-stage baseline transcription note; all are recorded, not fixed.
- At implementation entry, re-probe the environment and capture the baseline failing node-id list (owner: implement-feature step 6).
