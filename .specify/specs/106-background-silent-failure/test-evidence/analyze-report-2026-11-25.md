# Analyze Report — 106 Background Silent Failure (wave 1)

- **Spec**: `.specify/specs/106-background-silent-failure`
- **Stage**: `analyze` — wave 1 detection (3 read-only workers) + deterministic integration · run `r20261125T113505Z-106a`
- **Date**: 2026-11-25 · **Owner of this merge**: SDD Analyze Integrator (dispatch `background-silent-failure-analyze-integrate`)
- **Inputs**: `test-evidence/analyze-domain-w1.jsonl` (11) · `analyze-domain-w2.jsonl` (10) · `analyze-domain-w3.jsonl` (10) · `.specify/state/validate-wave1.verdicts.json` (12 verdicts) · both `checklists/*.md` (accountability)
- **Merge rule**: sections by domain W1 → W2 → W3, findings by id ascending; cross-worker duplicate ids — first declared wins. Measured: 31 unique ids, 0 collisions, 0 suppressed copies.
- **Pre-validation cap**: 50 findings — 31 delivered, under cap; the remaining candidates are inside the per-domain overflow rows (W1-11, W2-10), not dropped.

## 1. Gate verdict

**gate: FAIL — 10 HIGH, 0 CRITICAL**

The gate is blocked by the 10 validation-confirmed HIGH findings below. Two findings were downgraded by their validators (W1-01 → MEDIUM, W2-02 → LOW); no verdict rejected a finding, so the `## Unvalidated Findings` appendix is empty. Per the skill's severity rule, implementation must not start until the HIGH set is repaired upstream (requirements / plan / data-model / contracts) and re-analyzed.

## 2. Metrics

### 2.1 Findings by category and severity (post-validation, n=31)

| Category | CRITICAL | HIGH | MEDIUM | LOW | Total |
|---|---|---|---|---|---|
| inconsistency | 0 | 7 | 4 | 1 | 12 |
| underspecification | 0 | 2 | 2 | 0 | 4 |
| ambiguity | 0 | 1 | 1 | 2 | 4 |
| coverage | 0 | 0 | 3 | 0 | 3 |
| duplication | 0 | 0 | 1 | 2 | 3 |
| checklist-gap | 0 | 0 | 2 | 0 | 2 |
| overflow | 0 | 0 | 0 | 2 | 2 |
| decision-tension | 0 | 0 | 1 | 0 | 1 |
| **Total** | **0** | **10** | **14** | **7** | **31** |

### 2.2 Severity shift through validation

- Before validation (worker-declared): 0 CRITICAL · 12 HIGH · 13 MEDIUM · 6 LOW
- After validation (this report): 0 CRITICAL · 10 HIGH · 14 MEDIUM · 7 LOW

### 2.3 Validation wave (C/H only)

- Sent: **12** (every CRITICAL/HIGH finding, one fresh-context read-only validator each, disjoint from the detectors)
- confirm: **10** · downgrade: **2** · reject: **0**
- Downgrade rate: **2/12 = 16.7%**
- Evidence-boundary completeness: 12/12 verdicts carry both `evidence_supported` and `evidence_not_supported`; all copied verbatim into §4.
- Downgrades: W1-01 HIGH → MEDIUM; W2-02 HIGH → LOW. The 2/12 rate is inside a tolerable band but is recorded: two HIGH calls rested on one unqualified arrow notation / one disjunctive reading that the validators narrowed.
- MEDIUM/LOW findings (19) were not dispatched, by rule; their severity is the worker-declared one.

### 2.4 Detection passes that ran

- **W1** (requirements + checklists + constitution + glossary): A duplication · B ambiguity · C underspecification · D constitution alignment · E coverage gaps · F inconsistency · G feature relevance & accuracy · I decision tension records · **H checklist accountability**
- **W2** (plan + data-model + 3 contracts + quickstart + research): A · B · C · E · F · G · I
- **W3** (tasks + feature-ref + handoff + coverage-baseline + team + anchor): A · B · C · E · F · G · I
- **Integration (this pass)**: H over both checklist files + deterministic merge + verdict application + the fixed read-only coverage accounting step (§7).
- **Zero-finding floor**: not applicable — the run yielded 31 findings at three severities.
- **Scale**: 41 FR · 9 SC · 4 STR · 14 edge cases · 5 user stories · 37 tasks · 34 contract clauses (3 files) · 9 entities · 12 invariants · 8 quickstart scenarios · 40 checklist items.

## 3. Findings table (merged, post-validation)

| ID | Category | Severity | Primary location | Summary | Validation |
|---|---|---|---|---|---|
| W1-01 | inconsistency | **MEDIUM** (validated: downgraded) | `requirements.md:178` | A no-start-record attempt settles `unknown` (FR-010), but the Edge Cases row labels it `legacy/unknown` while FR-034 defines `legacy` by a missing `settlement_version`. | downgrade → MEDIUM (validated: downgraded) |
| W1-02 | inconsistency | HIGH | `requirements.md:171` | Exit 0 with a final `ANOMALY:` line satisfies both FR-003's incomplete-`failed` branch and FR-004's `anomaly` branch; no precedence is stated. | confirm (confirm) |
| W1-03 | inconsistency | HIGH | `requirements.md:52` | A-7 and the glossary require disappearance for `silent-end`, but FR-006 adds a no-pid deadline branch the glossary omits — after A-15 takeover the semantics narrow. | confirm (confirm) |
| W1-04 | underspecification | HIGH | `requirements.md:173` | `running` vs `silent-end` is decided by unnamed "declared threshold" / "declared wait deadline" values with no declarer, field, value domain or default. | confirm (confirm) |
| W1-05 | ambiguity | HIGH | `requirements.md:170` | `completed`'s independent-verification mechanisms are an open "例如" list, so the FR-029 / SC-002 guard has no decidable evidence set. | confirm (confirm) |
| W1-06 | inconsistency | HIGH | `requirements.md:178` | FR-010 / FR-018 require persistent attempt/start records in an unnamed existing carrier while FR-038 / A-6 forbid new storage; the Overview says C4 has no persistent attempt record today. | confirm (confirm) |
| W1-07 | inconsistency | HIGH | `requirements.md:219` | FR-039 / SC-009 require a frozen-total equality check to stay green, but EP-005 measured it red at base (31≠27); no baseline referent or allowed-delta set is named and the containment checklist item stays ticked. | confirm (confirm) |
| W1-08 | underspecification | MEDIUM | `requirements.md:192` | FR-021 delegates the re-ask of a state-less checker to "既有规则" without a named owner or path. | not in C/H wave |
| W1-09 | checklist-gap | MEDIUM | `checklists/background-settlement-2026-11-25.md:74` | CHK037 (Gap): the Runtime Stack premises name EP-001…EP-004, but FR-039 / SC-009 are governed by EP-005, which no requirement clause carries. | not in C/H wave |
| W1-10 | checklist-gap | MEDIUM | `checklists/background-settlement-2026-11-25.md:75` | CHK038 (Gap): the pre-dispatch failure record's carrier, format, owner and settlement disposition are unnamed; unlike other edge cases it lands on no value. | not in C/H wave |
| W1-11 | overflow | LOW | `requirements.md:169` | Overflow: two candidates elided (`running` inside the settle-all gate; FR-037 / FR-038 lacking an SC or measurement source). | not in C/H wave |
| W2-01 | inconsistency | HIGH | `contracts/settlement-contract.contract.md:24` | C-06 settles a no-start-record attempt as `unknown`, while C-04 / INV05 / C-26 define `unknown` only for unreadable or unparseable evidence tied to exit 2. | confirm (confirm) |
| W2-02 | inconsistency | **LOW** (validated: downgraded) | `contracts/carrier-conformance.contract.md:10` | C-13's `DONE → completed` arrow conflicts with the same clause, INV02 and the transition table making E4 a precondition (DONE without E4 = `failed` incomplete). | downgrade → LOW (validated: downgraded) |
| W2-03 | inconsistency | HIGH | `data-model.md:91` | A legacy 5-column row matches `settlement-unrecorded` (exit 1) while INV08 / C-33 forbid legacy records from causing a failing exit; no carve-out is stated. | confirm (confirm) |
| W2-04 | underspecification | HIGH | `contracts/settlement-contract.contract.md:20` | The pid-less running/silent-end split depends on an undeclared wait deadline (and C-15's start grace) with no field, option, default or input source. | confirm (confirm) |
| W2-05 | coverage | MEDIUM | `data-model.md:93` | `anomaly` and `cancelled` have no asserted red path: absent from E7's covers list, C-30's drills and per-carrier fixtures; INV06's negative is untested. | not in C/H wave |
| W2-06 | underspecification | MEDIUM | `data-model.md:54` | E4's `return-record` "declared equivalent" and C-15's "verified return" name no verifier and no resolvable evidence, so C2's `completed` gate rests on an undefined declaration. | not in C/H wave |
| W2-07 | inconsistency | MEDIUM | `data-model.md:126` | INV04 requires a present E2 start record for `silent-end`, but C1 writes no new record and its four-piece is "not duplicated"; `c1-fork` sits in E2's carrier enum with no writer. | not in C/H wave |
| W2-08 | ambiguity | MEDIUM | `contracts/carrier-conformance.contract.md:10` | C-13's `else silent-end` fallback is stated only for TIMEOUT; an unverifiable RUNNING verdict is left undefined although INV03 forbids a stale `running` and INV04 bounds `silent-end`. | not in C/H wave |
| W2-09 | decision-tension | MEDIUM | `plan.md:82` | The C3 7-column header widening touches an exact-header parser with no decision-tension record (no alternative, discriminating evidence or reopening condition, unlike T-002's pattern). | not in C/H wave |
| W2-10 | overflow | LOW | `contracts/enforcement-and-migration.contract.md:22` | Overflow: four elided items — C-28 names three roots (engine has four); 5 vs 4 skill-text edits; exit≠0 + anomaly-line precedence; the unknown rule restated on five surfaces. | not in C/H wave |
| W3-01 | inconsistency | HIGH | `tasks.md:66` | tasks.md allows PLAN-EDIT small edits to plan-owned files while handoff.md / team.md forbid those paths to every seat — mutually exclusive permissions over one object set. | confirm (confirm) |
| W3-02 | coverage | MEDIUM | `feature-ref.md:79` | Delivery surface 35 (the `.specify/glossary.md` `silent-end` proposal) is carried by no task row and checked by no DoD or GATE item. | not in C/H wave |
| W3-03 | coverage | MEDIUM | `handoff.md:50` | C-65's one `writeback/<T-NNN>.yaml` per completed task is produced and verified by no task, DoD or GATE item. | not in C/H wave |
| W3-04 | inconsistency | MEDIUM | `tasks.md:9` | T028 is classified both as a red-first test written before T029 and as a post-implementation regression guard of existing behaviour. | not in C/H wave |
| W3-05 | inconsistency | MEDIUM | `tasks.md:267` | T031's `[blockedBy:]` omits T019 although T019 edits a mirrored skill source, contradicting the cross-story dependency rule. | not in C/H wave |
| W3-06 | duplication | MEDIUM | `teams/106…/team.md:17` | The crew territory (write / forbidden sets) is declared twice — team.md vs handoff.md § Territory — with neither copy naming an owner. | not in C/H wave |
| W3-07 | duplication | LOW | `tasks.md:19` | DoD-3 restates the full 34-clause → task mapping that § Contract Clause → Task Map already owns in table form. | not in C/H wave |
| W3-08 | duplication | LOW | `tasks.md:19` | The 37/41 fr-uncovered fact with its four-FR set is stated three times in tasks.md. | not in C/H wave |
| W3-09 | ambiguity | LOW | `tasks.md:19` | DoD-2 counts 5 skill/report text edits while the delivery surface lists only four skill files. | not in C/H wave |
| W3-10 | ambiguity | LOW | `handoff.md:46` | handoff.md names all nine SCs as acceptance criteria while GATE-4 passes only SC-001/002/004 and T035 records the rest as supporting readings; no criterion says whether a failing supporting SC blocks. | not in C/H wave |

## 4. Findings detail

### 4.1 Domain W1 — requirements, checklists, constitution, glossary (11 findings)

#### W1-01 · inconsistency · MEDIUM (validated: downgraded from HIGH)

- **Claim** (verbatim; `analyze-domain-w1.jsonl:1`): The settlement of an attempt that lacks a start record is assigned two different values — `unknown` by FR-010 but `legacy/unknown` by the Edge Cases row — while FR-034 defines `legacy` by a missing `settlement_version`, not by a missing start record.
- **Propagation surface** (verbatim): judgment-surface verdict selection for attempts lacking a start record, FR-034 legacy marking, and the per-carrier fixtures that assert which value such an attempt receives
- **Locations**: `.specify/specs/106-background-silent-failure/requirements.md:178` · `.specify/specs/106-background-silent-failure/requirements.md:156` · `.specify/specs/106-background-silent-failure/requirements.md:214`
- **Recommendation**: Rewrite the Edge Cases row (requirements.md:156) to one reading — drop `legacy/`, or define it strictly as the FR-034 missing-`settlement_version` mark — and state that a missing start record settles `[[STR-002]]` with no `legacy` implication; align the per-carrier fixtures.
- **Validation**: `downgrade` → `MEDIUM`

  **evidence_supported** (verbatim): requirements.md:178 (FR-010) mandates [[STR-002]] for attempts lacking a start record; requirements.md:294/251 map STR-002 to `unknown`. requirements.md:156 labels the same no-start-record attempt 'legacy/`unknown`', while requirements.md:214 (FR-034) ties the `legacy` mark exclusively to a missing settlement_version [[STR-004]], and requirements.md:307 confirms `legacy` is only an audit/settlement-output mark. The `legacy` term thus carries two coexisting criteria, one of which (missing start record) FR-034 does not define.

  **evidence_not_supported** (verbatim): The claim of 'two different values': `legacy` is outside FR-001's closed verdict set (requirements.md:169) and `unknown` appears in both locations, so the settlement value itself is not contradicted — only the `legacy` labeling criterion is. The Edge Cases phrase also admits a disjunctive reading ('legacy or unknown', the legacy branch covering version-less attempts) that would dissolve the conflict; the finding does not exclude it, and no downstream artifact beyond the cited file was examined to establish an implementer-facing consequence.

#### W1-02 · inconsistency · HIGH (validated: confirm)

- **Claim** (verbatim; `analyze-domain-w1.jsonl:2`): FR-003's third `failed` branch (exit 0 without completion evidence) and FR-004's `anomaly` branch both match a process that exits 0 with a final `ANOMALY:` line, and no clause states which value takes precedence.
- **Propagation surface** (verbatim): classification of the most realistic anomaly fixture (a subagent whose process ends normally after writing its `ANOMALY:` return line), the `failed`/`anomaly` rows of the Settlement Evidence Matrix, and SC-001/SC-002 fixture expectations
- **Locations**: `.specify/specs/106-background-silent-failure/requirements.md:171` · `.specify/specs/106-background-silent-failure/requirements.md:172` · `.specify/specs/106-background-silent-failure/requirements.md:148` · `.specify/specs/106-background-silent-failure/requirements.md:246`
- **Recommendation**: Add one precedence clause in FR-003 / FR-004 or the Settlement Evidence Matrix: an explicit `ANOMALY:` final line on exit 0 settles `anomaly`; the incomplete-`failed` branch applies only when no anomaly marker exists. Mirror the matrix rows.
- **Validation**: `confirm` (severity kept)

  **evidence_supported** (verbatim): requirements.md:171 (FR-003) makes 'exit 0 but missing required completion evidence (incomplete)' positive evidence for failed; requirements.md:172 (FR-004) makes 'last non-empty line starts with ANOMALY:' plus terminal evidence positive evidence for anomaly, and a terminated exit-0 attempt with an ANOMALY final line satisfies both branches on the same observation; requirements.md:148 routes 'exit 0, no sentinel / no completion declaration' to failed(incomplete), which also covers exit 0 with an ANOMALY final line; requirements.md:246 lists both as separate positive-evidence rows in the Settlement Evidence Matrix on overlapping observations with no precedence column or note; adjacent FR-001 (requirements.md:169) requires exactly one settlement value per attempt, making the collision material rather than harmless permissive wording.

  **evidence_not_supported** (verbatim): The blanket negative 'no clause states which value takes precedence' was verified only within the cited Settlement Contract (FR-001–FR-018), the Edge Cases and the Settlement Evidence Matrix; the remainder of requirements.md and any downstream artifacts were not read, so precedence rules outside that scope were not observed. The artifacts show an under-determined overlap (both FRs are permissive 'MUST only hold when' conditions) plus a failed-prescribing edge case, not two explicitly prescriptive clauses naming different values.

#### W1-03 · inconsistency · HIGH (validated: confirm)

- **Claim** (verbatim; `analyze-domain-w1.jsonl:3`): A-7 and the glossary entry define `silent-end` as unconditionally requiring that the executing body has disappeared, while FR-006 adds a no-pid branch in which a passed waiting deadline substitutes for that disappearance test — so the glossary entry that A-15 lets take over the semantics would exclude a path FR-006 requires.
- **Propagation surface** (verbatim): settlement of the no-pid carriers C4/C6, the glossary entry that takes over the semantics after confirmation (A-15), and every silent-end fixture built on a carrier without a pid
- **Locations**: `.specify/specs/106-background-silent-failure/requirements.md:52` · `.specify/specs/106-background-silent-failure/requirements.md:174` · `.specify/specs/106-background-silent-failure/requirements.md:60` · `.specify/glossary.md:208`
- **Recommendation**: Widen A-7 to include the no-pid branch (or qualify it as the pid-bearing case) and align the glossary proposal text (glossary.md:208) before confirmation, since A-15 hands semantic reference to that entry after takeover.
- **Validation**: `confirm` (severity kept)

  **evidence_supported** (verbatim): requirements.md:52 (A-7) states that silent-end requires 尝试已开始 + 执行主体已消失 + 四类终态证据均缺席 to hold simultaneously, with no carrier qualification and no deadline branch, and says 「三件同时成立」. requirements.md:174 (FR-006) defines silent-end for carriers with no pid as 声明等待期限已过、无返回且无活信号, a separate operative test that does not require establishing that the executing body disappeared. requirements.md:60 (A-15) states that the spec definition governs this feature until the glossary entry is confirmed, after which the glossary entry takes over semantic reference. glossary.md:208 (status=proposed, 提案来源: spec 106) defines silent-end via 起点记录 + 执行主体已消失 + 四类终态证据全部缺席 and contains no no-pid/deadline branch, so it is narrower than the spec it cites as its source. Corroboration within the same artifact: requirements.md:250's settlement-evidence matrix already carries the branch 或无 pid 载体的等待期限已过且无返回无活信号, and requirements.md:189 (FR-018) applies the deadline test to C4 native, confirming that the requirements layer does require the branch A-7 and the glossary entry omit.

  **evidence_not_supported** (verbatim): The claim that the glossary entry 'would exclude' the no-pid path after takeover is inferred from A-15's takeover clause; the entry is status=proposed and no confirmation decision or confirmation outcome was observable. The cited semantic owner shared/definitions/superagent-definitions.md § Termination was not read because it is outside the cited locations, so whether that owner already carries the branch is unobserved. The claim does not mention requirements.md:250 or FR-018, which show the requirements artifact as a whole does carry the no-pid branch, so the divergence is confined to A-7's summary and the current glossary proposal rather than to the entire spec. The parenthetical 未覆盖无 pid 的期限分支 in the evidence notes is the finder's annotation, not glossary text; the omission from the glossary is substantiated, but that wording is not present in the artifact. No plan or implementation artifact was observed, so downstream impact is not demonstrated, and whether glossary-utils detect-conflict would flag this semantic narrowing at plan wrap-up was not observed; HIGH rests on the owner-projection argument, not on an observed defect.

#### W1-04 · underspecification · HIGH (validated: confirm)

- **Claim** (verbatim; `analyze-domain-w1.jsonl:4`): FR-005, FR-006 and FR-018 decide the `running` versus `silent-end` boundary from an unnamed declared threshold and an unnamed declared waiting deadline — no declarer, value domain or record field is named — so two implementers can choose different numbers with both readings compliant.
- **Propagation surface** (verbatim): liveness re-check and deadline evaluation in the judgment surface, C4/C6 settlement, and every silent-end fixture whose outcome depends on the threshold value
- **Locations**: `.specify/specs/106-background-silent-failure/requirements.md:173` · `.specify/specs/106-background-silent-failure/requirements.md:174` · `.specify/specs/106-background-silent-failure/requirements.md:189`
- **Recommendation**: Name the declaration surface for both values — declarer, record field or CLI option, default and value domain — in FR-005 / FR-006 / FR-018, and add the deadline field to FR-010's record enumeration.
- **Validation**: `confirm` (severity kept)

  **evidence_supported** (verbatim): requirements.md:173 (FR-005) conditions `running` on 活日志在声明阈值内增长 without naming who declares the threshold or where it lives; requirements.md:174 (FR-006) defines the pid-less-carrier silent-end as 声明等待期限已过、无返回且无活信号, again with no declarer, value or record field; requirements.md:189 (FR-018) settles C4 on 超过声明的等待期限 with the same gap. A whole-file grep of requirements.md for 阈值|期限|宽限|声明 finds no numeric value, declaration point or owner anywhere in the document (line 250's evidence matrix and line 237's C4 row only restate 等待期限/期限), and FR-010 (line 178) enumerates the dispatch-time record fields (尝试身份、载体、父身份、开始时间、pid) with no deadline/threshold field even though it names 期限 as a settlement input. With no binding value and no home for it, the same material event can settle silent-end under one compliant implementation and running/late completed under another, and the FR-028/FR-029 deterministic surface has nothing authoritative to read.

  **evidence_not_supported** (verbatim): The inference that two implementers 'can choose different numbers with both readings compliant' is derived from the observed absence of any value, owner or field, not from a demonstrated contradiction; absence was verified only inside requirements.md — a declaration in plan.md or an existing framework owner (line 153 cites 既有 deadline grace, implying a pre-existing deadline concept) was not examined, so 'no declarer anywhere' exceeds the observed boundary. The claim also folds FR-005 into the silent-end boundary, whereas FR-005 is one of several alternative live-evidence forms and pid-bearing carriers (FR-014/FR-016) settle via pid disappearance/termination records without the deadline; the deadline is decisive mainly for pid-less carriers (FR-006) and C4 (FR-018).

#### W1-05 · ambiguity · HIGH (validated: confirm)

- **Claim** (verbatim; `analyze-domain-w1.jsonl:5`): FR-002 lets `completed` rest on an open for-example list of independent-verification mechanisms with no closure owner, so the guard that must reject a `completed` claim without completion evidence (FR-029, SC-002) has no decidable evidence set.
- **Propagation surface** (verbatim): the completed guard required by FR-029, SC-002's reverse fixture, and completion acceptance for every carrier
- **Locations**: `.specify/specs/106-background-silent-failure/requirements.md:170` · `.specify/specs/106-background-silent-failure/requirements.md:206` · `.specify/specs/106-background-silent-failure/requirements.md:269`
- **Recommendation**: Close the independent-verification mechanism set: replace FR-002's "例如" list with an enumeration whose closure owner is named, or require the named owner to enumerate it, so the FR-029 / SC-002 guard predicate becomes decidable.
- **Validation**: `confirm` (severity kept)

  **evidence_supported** (verbatim): requirements.md:170 (FR-002) makes `completed` require 终端成功记录 AND 独立核验, introducing the verification mechanisms with 例如 (驱动 U4 的产物校验、团队 `## Verification`、五要素上行齐备) — explicitly non-exhaustive; the same open form recurs in the artifact at :245 (Settlement Evidence Matrix `completed` row: 五要素齐备 / U4 / 团队 Verification) and :77 (US1 scenario: 独立核验的指针), so no closure of the mechanism set is stated. FR-029 at :206 requires a red-able guard covering 无完成证据却声称 `completed`; SC-002 at :269 asserts the identical predicate with Path: final. FR-041 at :221 declares closed only 载体清单与结算值集合, leaving the completion-evidence mechanism set outside any closure declaration, and no FR requires the named evidence owner to enumerate or close it, so the guard predicate has no decidable evidence set in the requirements text.

  **evidence_not_supported** (verbatim): 'no closure owner' is stronger than observed: A-3 (:48) and FR-029 (:206) name the revised superagent-definitions § Termination as single owner of 集合与证据要求, and FR-013 (:184) forbids a second evidence matrix — the missing piece is a closure/decidability mandate, not an owner; the owner page itself was not cited or read, so whether it closes the set is unobserved. Also unestablished: that plan/implementation cannot close it — FR-029 defers C2/C4/C6 evidence-input integration to the plan, and carrier FRs (FR-016 :187 '退出 0 但无完成声明 → failed'; FR-018 :189 五要素缺任一 → failed incomplete) constrain completion evidence for some carriers.

#### W1-06 · inconsistency · HIGH (validated: confirm)

- **Claim** (verbatim; `analyze-domain-w1.jsonl:6`): FR-010 and FR-018 require persistent parent-side attempt/start records while FR-038 and A-6 forbid any new storage or registry, and the existing parent-side carrier those records must land in is never named — the Overview states C4 has no persistent attempt record today.
- **Propagation surface** (verbatim): plan architecture for the attempt record (additive carrier versus the forbidden new store), C4 implementation, and the zero-new-mechanism claim that acceptance must verify
- **Locations**: `.specify/specs/106-background-silent-failure/requirements.md:178` · `.specify/specs/106-background-silent-failure/requirements.md:189` · `.specify/specs/106-background-silent-failure/requirements.md:218` · `.specify/specs/106-background-silent-failure/requirements.md:51` · `.specify/specs/106-background-silent-failure/requirements.md:32`
- **Recommendation**: Name the existing parent-side carrier in FR-010 / FR-018, or state explicitly that an additive attempt-record file is permitted under FR-033 and outside FR-038's storage ban; reconcile the Overview's "no persistent attempt record today" with the new obligation.
- **Validation**: `confirm` (severity kept)

  **evidence_supported** (verbatim): requirements.md:178 FR-010 requires recording attempt identity/carrier/parent/start time/pid into an unnamed 既有父侧载体, with missing start record forcing [[STR-002]]; requirements.md:189 FR-018 requires C4 native to leave an attempt record at dispatch with no named destination; requirements.md:218 FR-038 and requirements.md:51 A-6 forbid new storage/registry and define settlement as read-only classification of existing carriers; requirements.md:32 states C4 attempt records exist only in parent-side memory with no persistent started-but-unreturned fact. Adjacent context corroborates: the C4 inventory row (line 237) records '无持久尝试记录' and lists '父侧尝试记录' as the required change; line 156 requires rebuilding attempts after parent death from an '既有持久载体' that is also unnamed; a full-file scan finds no named store for these records.

  **evidence_not_supported** (verbatim): FR-010 does not itself use the word 'persistent' nor explicitly require cross-session survival; that requirement is implied by missing-start→[[STR-002]] at settlement and asserted at uncited Edge Cases line 156. The document shows a load-bearing under-specification/contradiction rather than a formal impossibility: FR-033 permits additive new fields/files, so whether a new C4 attempt-record file constitutes forbidden 'storage' under A-6/FR-038 is itself undefined — that ambiguity is the defect. No plan/tasks or other artifacts were examined (out of scope), so it is unverified whether a downstream artifact names a carrier.

#### W1-07 · inconsistency · HIGH (validated: confirm)

- **Claim** (verbatim; `analyze-domain-w1.jsonl:7`): FR-039 and SC-009 require the scanner's frozen total and equality check to stay green without naming a baseline referent or allowed-delta set, while the feature's own record reports that equality check already red at baseline (live 31 versus frozen 27) and the requirements checklist still ticks the containment-claim item.
- **Propagation surface** (verbatim): SC-009's measurement at implement and review, the honesty of the preservation claim, and any acceptance verdict that repeats stays-green as a met criterion
- **Locations**: `.specify/specs/106-background-silent-failure/requirements.md:219` · `.specify/specs/106-background-silent-failure/requirements.md:276` · `.specify/specs/106-background-silent-failure/checklists/background-settlement-2026-11-25.md:70` · `.specify/specs/106-background-silent-failure/checklists/background-settlement-2026-11-25.md:93` · `.specify/specs/106-background-silent-failure/checklists/requirements.md:18` · `.specify/glossary.md:120`
- **Recommendation**: Give FR-039 / SC-009 an actual baseline referent and a fallback criterion consistent with plan EP-005 (zero new blocking hits on touched files); un-tick or re-scope checklists/requirements.md:18; state that the equality check is red at base and is never claimed green.
- **Validation**: `confirm` (severity kept)

  **evidence_supported** (verbatim): FR-039（requirements.md:219）与 SC-009（requirements.md:276）均要求冻结 total 与相等判定保持绿色，但未点名基线参照物（无具体值、提交或文件），A-12（requirements.md:57）同义；plan.md:185 的 EP-005 将该前提标为 falsified，实测 total 31、相等测试失败 31 != 27，plan.md:187 明言本特性从不声称其为绿，plan.md:216 复述同一事实；checklists/background-settlement-2026-11-25.md:70（CHK036）明写 live 31 ≠ 冻结 27，:93 将其列为待 analyze/review 裁定的观察；checklists/requirements.md:18 仍勾选 [x] containment claims 点名基线参照物与可推导允许差异集；glossary.md:120 记录基线 93 ⇒ cap 23.25 ⇒ 最大整数 23，且 test_proactive_trigger_section.py 对 050 baseline-gates.json 的 frozen total=23 做相等判定（该文件第 14-23 行确为 23），而 test_clause_coverage.py:87、test_wrap_up_wording_gate_safe.py:75-77、test_user_facing_comprehension_doc.py:569 钉 27，证明仓内 '冻结基线值' 存在多个互不一致的钉值。

  **evidence_not_supported** (verbatim): 受只读约束未重跑扫描器，live 31 无法独立复测，仅取自 plan.md EP-005 与 checklist 的转述；'未给出 allowed-delta set' 对 SC-009 的 '新增阻断模式命中数为 0' 而言略宽——该句确为零增量声明，缺参照物的是 total/相等判定部分；glossary.md:120 的 23 与 plan 的 27 是不同钉点/冻结日期（050 baseline-gates.json 2026-09-08 与 067 T025 更新）下的值，二者可先后描述同一扫描器，故应读作 '不存在单一冻结基线参照物'，而非两个数字本身不可能同源；未核对 requirements 清单第 18 行勾选时间是否早于 EP-005 的发现时点。

#### W1-08 · underspecification · MEDIUM

- **Claim** (verbatim; `analyze-domain-w1.jsonl:8`): FR-021 delegates the re-ask of a checker that returns no state to existing rules without a path or owner, so the validation-wave reaction has no identifiable rule to follow.
- **Propagation surface** (verbatim): the re-ask behaviour of analysis fan-out workers and any test asserting that behaviour
- **Locations**: `.specify/specs/106-background-silent-failure/requirements.md:192` · `.specify/specs/106-background-silent-failure/checklists/background-settlement-2026-11-25.md:37`
- **Recommendation**: Replace "按既有规则重问" with a named owner pointer to the re-ask rule, or write the re-ask protocol (attempt bound, escalation) directly into FR-021.
- **Validation**: not dispatched — MEDIUM/LOW skip the C/H wave (skill §7); severity is the worker-declared one.

#### W1-09 · checklist-gap · MEDIUM

- **Claim** (verbatim; `analyze-domain-w1.jsonl:9`): Checklist item CHK037 (Gap) has no requirement-side disposition: the Runtime Stack names only EP-001 through EP-004 as premises, while the checklist reports the plan carries EP-001 through EP-005 with EP-005 governing FR-039/SC-009, and no requirement clause carries EP-005 or a fallback measurement for it.
- **Propagation surface** (verbatim): traceability of FR-039/SC-009 to their governing premise and the plan-stage premise-row completeness CHK037 asks for (not decidable from this read domain)
- **Locations**: `.specify/specs/106-background-silent-failure/checklists/background-settlement-2026-11-25.md:74` · `.specify/specs/106-background-silent-failure/requirements.md:255` · `.specify/specs/106-background-silent-failure/requirements.md:259` · `.specify/specs/106-background-silent-failure/requirements.md:262` · `.specify/specs/106-background-silent-failure/requirements.md:219`
- **Recommendation**: Carry EP-005 (or its fallback measurement) on the requirement side — add it to the Runtime Stack premises row that governs FR-039 / SC-009.
- **Validation**: not dispatched — MEDIUM/LOW skip the C/H wave (skill §7); severity is the worker-declared one.

#### W1-10 · checklist-gap · MEDIUM

- **Claim** (verbatim; `analyze-domain-w1.jsonl:10`): Checklist item CHK038 (Gap) has no requirement-side disposition: the Edge Cases row for pre-dispatch failure names a pre-dispatch failure record but neither its carrier or format nor which owner produces it, so unlike every other edge case it lands on no settlement value and no named record.
- **Propagation surface** (verbatim): reporting of pre-dispatch failures, retry-counter exclusion accounting, and fixtures for the pre-dispatch branch
- **Locations**: `.specify/specs/106-background-silent-failure/checklists/background-settlement-2026-11-25.md:75` · `.specify/specs/106-background-silent-failure/requirements.md:158` · `.specify/specs/106-background-silent-failure/requirements.md:169` · `.specify/specs/106-background-silent-failure/requirements.md:179`
- **Recommendation**: Name the pre-dispatch failure record's carrier, format and producing owner, and state its settlement disposition (no settlement value, excluded from retry count) in the Edge Cases row and FR-001's scope.
- **Validation**: not dispatched — MEDIUM/LOW skip the C/H wave (skill §7); severity is the worker-declared one.

#### W1-11 · overflow · LOW

- **Claim** (verbatim; `analyze-domain-w1.jsonl:11`): Two further candidates were kept out of this file under the approximately-ten-finding budget: (1) `running` counted as one of the seven settlement values (FR-001) versus the same attempts marked 未结算 in reports (FR-027) under FR-011's settle-all gate; (2) FR-037 (documentation values consistent with code, no second copy) and FR-038 (zero-new-machinery ban list) carry no Success Criterion or measurement source.
- **Propagation surface** (verbatim): report-field semantics for running attempts; documentation drift and the zero-new-machinery claim remaining unobservable at acceptance
- **Locations**: `.specify/specs/106-background-silent-failure/requirements.md:169` · `.specify/specs/106-background-silent-failure/requirements.md:179` · `.specify/specs/106-background-silent-failure/requirements.md:201` · `.specify/specs/106-background-silent-failure/requirements.md:217` · `.specify/specs/106-background-silent-failure/requirements.md:218` · `.specify/specs/106-background-silent-failure/requirements.md:280`
- **Recommendation**: Split the overflow candidates into their own rows next round: settle whether `running` is inside FR-001's settle-all gate versus FR-027's 未结算 marking, and give FR-037 / FR-038 a Success Criterion or measurement source.
- **Validation**: not dispatched — MEDIUM/LOW skip the C/H wave (skill §7); severity is the worker-declared one.

### 4.2 Domain W2 — plan, data-model, contracts, quickstart, research (10 findings)

#### W2-01 · inconsistency · HIGH (validated: confirm)

- **Claim** (verbatim; `analyze-domain-w2.jsonl:1`): C-06 settles an attempt that has no start record as `unknown`, while C-02/C-04/INV05/C-26 define `unknown` as produced only from unreadable or unparseable evidence and always tied to exit 2, so one readable absence (a missing record) is forced into the detection-defect refusal path.
- **Propagation surface** (verbatim): engine settle verdict derivation and exit-code semantics, the settlement test matrix, and carriers that can lack a start record (C3 legacy rows, C4 before hand-off)
- **Locations**: `.specify/specs/106-background-silent-failure/contracts/settlement-contract.contract.md:24` · `.specify/specs/106-background-silent-failure/contracts/settlement-contract.contract.md:32` · `.specify/specs/106-background-silent-failure/data-model.md:127` · `.specify/specs/106-background-silent-failure/contracts/enforcement-and-migration.contract.md:14`
- **Recommendation**: Reconcile C-06 with C-04 / INV05: either extend `unknown` to cover readable absences (missing start record) with an explicit exit-code consequence, or give the missing-start case a distinct verdict; align C-26's exit map.
- **Validation**: `confirm` (severity kept)

  **evidence_supported** (verbatim): settlement-contract.contract.md:32 (C-06) requires § Termination to state that an attempt with no start record cannot prove it existed and settles as `unknown`, never `completed`; :24 (C-04) says `unknown` is produced only when evidence is unreadable/unparseable and names the unreadable pointers; :16 (C-02) defines `unknown` as the unreadable/unparseable pointer set; data-model.md:127 (INV05) says `unknown` is produced only from unreadable/unparseable evidence, names the unreadable pointers, and the engine exits 2, never 0; data-model.md:81/95 distinguish E6 `kind: lack` (absence) from `kind: unreadable` and call unreadable evidence the single deterministic exit-2 refusal, with `unknown` not a violation kind; enforcement-and-migration.contract.md:14 (C-26) maps exit 2 to unreadable/unparseable evidence with `unknown` findings and forbids `unknown` as exit 0, and :42 (C-33) calls `unknown`/exit-2 the single deterministic refusal for unreadable evidence; the settlement contract contains only C-01–C-12 and the enforcement contract only C-25–C-34, and no clause reconciles a missing (never-written, hence readable-absent) start record with the only-unreadable-evidence definition, so the cited artifacts do force that absence into the detection-defect/exit-2 path.

  **evidence_not_supported** (verbatim): FR-007/FR-010 source text in requirements.md and the owner page superagent-definitions.md § Termination were not cited and I did not read them, so an owner-level resolution (e.g. redefining 'unreadable' to include an unresolvable start-record pointer) cannot be ruled out; 'always tied to exit 2' is an inference from C-04/INV05's 'only' plus C-26's mapping, since no cited line literally states every `unknown` verdict yields exit 2; no downstream task or test was cited, so whether an implementation reading is already fixed is unobserved; the 'missing pointer = unreadable pointer' reading is a stretch but is not textually excluded by the cited lines.

#### W2-02 · inconsistency · LOW (validated: downgraded from HIGH)

- **Claim** (verbatim; `analyze-domain-w2.jsonl:2`): C-13 states `DONE → completed` as a direct mapping while the same clause and INV02 plus the state-transition table make U4 verification a precondition of `completed` (DONE without E4 is `failed (incomplete)`), giving one C1 attempt two mutually exclusive outcomes.
- **Propagation surface** (verbatim): the C1 verdict-mapping implementation, the `completed` gate, and the C1 mapping fixture
- **Locations**: `.specify/specs/106-background-silent-failure/contracts/carrier-conformance.contract.md:10` · `.specify/specs/106-background-silent-failure/data-model.md:124` · `.specify/specs/106-background-silent-failure/data-model.md:143`
- **Recommendation**: Qualify C-13's arrow notation — `DONE → completed` only with E4, otherwise `failed (incomplete)` — matching INV02 and the state-transition table.
- **Validation**: `downgrade` → `LOW`

  **evidence_supported** (verbatim): carrier-conformance.contract.md:10 (C-13) does contain an unqualified mapping list including `DONE → completed`, immediately followed by the qualifier `DONE remains a candidate that the driver's U4 verification completes; a versioned claim MUST name its U4 evidence pointer`; data-model.md:124 (INV02) requires E3 success and E4 with non-empty resolvable evidence for `completed`, with exit 0 alone not being completion; data-model.md:142-144 shows exit 0 plus sentinel/declaration reaching `completed` only with E4 verified and `failed (incomplete)` with E4 absent; data-model.md:48-58 (E4) states no E4 means a success terminal record settles `failed (incomplete)`, never `completed`.

  **evidence_not_supported** (verbatim): The claim that one C1 attempt is given two mutually exclusive outcomes, and its HIGH severity, are overstated: C-13's own next sentence, E4, INV02 and the state-transition table converge on one final verdict (`failed (incomplete)`) for DONE without E4, so the artifact as a whole leaves only an unqualified arrow-notation tension rather than two licensed outcomes; no task row, pinning test or implementation consequence of the mapping was cited or observed (tasks.md and tests were not inspected).

#### W2-03 · inconsistency · HIGH (validated: confirm)

- **Claim** (verbatim; `analyze-domain-w2.jsonl:3`): A legacy 5-column team report row satisfies E7/C-16's `settlement-unrecorded` predicate (row missing `end_state`/`evidence`) while INV08/C-33 forbid legacy records from causing a failing exit code, leaving the same row either exit 1 (violation) or exit 0 (annotated) under mutually exclusive criteria.
- **Propagation surface** (verbatim): the engine team-report reader, exit codes, every pre-existing 5-column report, and the migration contract's legacy-never-fails guarantee
- **Locations**: `.specify/specs/106-background-silent-failure/data-model.md:91` · `.specify/specs/106-background-silent-failure/contracts/carrier-conformance.contract.md:22` · `.specify/specs/106-background-silent-failure/data-model.md:130` · `.specify/specs/106-background-silent-failure/contracts/enforcement-and-migration.contract.md:42` · `.specify/specs/106-background-silent-failure/quickstart.md:80`
- **Recommendation**: Add an explicit legacy carve-out: a 5-column (version-less) row is annotated `legacy` and neither triggers `settlement-unrecorded` nor exits 1; mirror it in C-16 / INV08 / C-33 and the quickstart scenarios.
- **Validation**: `confirm` (severity kept)

  **evidence_supported** (verbatim): data-model.md:91 (E7) defines settlement-unrecorded as a claim-bearing team-report row missing end_state/evidence; data-model.md:66 places a ## Execution Detail row on E5's team-report-row surface, so a 5-column legacy row matches; carrier-conformance.contract.md:22 (C-16) both requires the legacy 5-column header to parse as legacy and declares a row with empty end_state/evidence settlement-unrecorded, with no legacy carve-out; data-model.md:130 (INV08) and enforcement-and-migration.contract.md:42 (C-33) state records without settlement_version are annotated and MUST NOT cause a failing exit code; quickstart.md:80 pairs settlement-unrecorded (exit 1) with a 5-column legacy report parsing and annotated legacy; enforcement-and-migration.contract.md:12-14 (C-26) maps settlement violations to exit 1 and judged attempts to exit 0, making the two prescribed exit codes incompatible for the same row; quickstart.md:94 (same-document S-4 context) pins a legacy fixture to exit 0.

  **evidence_not_supported** (verbatim): No cited location states an explicit precedence or carve-out for legacy team-report rows (neither that legacy rows are exempt from settlement-unrecorded nor that legacy reports must exit 1); the contradiction is assembled from separate clauses. A charitable reading of C-16 (empty means blank 7-column cells, not absent columns) could reconcile the texts, but that scoping is nowhere written, and E7 plus quickstart say missing. I did not inspect spec.md FR-034/FR-017, role-edge-check.py, or the pinning tests, so actual intended or implemented exit behavior for a legacy team report is unobserved; HIGH is the finding's own severity, not an artifact claim.

#### W2-04 · underspecification · HIGH (validated: confirm)

- **Claim** (verbatim; `analyze-domain-w2.jsonl:4`): The running-versus-silent-end split for pid-less carriers depends on `the declared wait deadline` (C-03/C-17/INV04) and on C-15's `start grace`, but no record field, CLI option, default or input source declares either value, so the engine cannot derive that boundary deterministically.
- **Propagation surface** (verbatim): silent-end derivation for pid-less attempts (C3/C4), engine determinism, and the running/silent-end boundary this feature exists to make decidable
- **Locations**: `.specify/specs/106-background-silent-failure/contracts/settlement-contract.contract.md:20` · `.specify/specs/106-background-silent-failure/contracts/carrier-conformance.contract.md:18` · `.specify/specs/106-background-silent-failure/contracts/carrier-conformance.contract.md:26` · `.specify/specs/106-background-silent-failure/data-model.md:126` · `.specify/specs/106-background-silent-failure/data-model.md:16` · `.specify/specs/106-background-silent-failure/contracts/enforcement-and-migration.contract.md:22`
- **Recommendation**: Declare both boundary inputs — wait deadline and start grace — with source (record field / CLI option / default), value and precedence; extend E2's field table and C-28's closed input list.
- **Validation**: `confirm` (severity kept)

  **evidence_supported** (verbatim): settlement-contract.contract.md:20 (C-03) defines pid-less silent-end as 'the declared wait deadline passed with no return and no live signal' without naming a declaration site; carrier-conformance.contract.md:26 (C-17) likewise uses 'declared wait deadline' for C4; carrier-conformance.contract.md:18 (C-15) uses 'start grace' with no value or source; data-model.md:126 (INV04) and data-model.md:46 both make derivation depend on a deadline with no defined input; data-model.md:19-31 (E2) lists settlement_version/attempt_id/carrier/parent_identity/started_at/pid/pid_start_ticks/contract and no deadline or grace field, and E3 (35-44) and E5 (66-71) add none; enforcement-and-migration.contract.md:22 (C-28) closes the settle input set to existing carriers, additive records and the three existing roots, with no deadline/grace option; a targeted search of the cited contracts/data-model plus plan.md and requirements.md found no default, field, CLI option or input source for either value (plan.md:15 only repeats 'declared deadline'; requirements.md:153 cites only the C1 watcher's existing deadline grace). Because silent-end versus running for pid-less carriers is decided by this undeclared boundary and the engine contract requires deterministic per-attempt derivation (INV10, C-29), the gap is material and unimplementable without inventing a value.

  **evidence_not_supported** (verbatim): The finding attaches C-15's start grace to the pid-less carrier boundary, but C-15 governs C2, which records a pid; the start-grace gap is real yet belongs to C2's 'pid never appeared' branch rather than to pid-less carriers, whose split depends only on the wait deadline. I did not examine pointer-reached downstream texts not among the cited locations (e.g. shared/definitions/superagent-definitions.md § Termination, skills/internal/run-agent/SKILL.md), so I cannot exclude that one of them declares a deadline source or default; a non-cited baseline shows watch-target.sh already carries --start-grace and deadline parameters for C1, so the gap is specific to carriers without that watcher, and no citation establishes whether the feature intends to reuse those defaults. Magnitude of practical impact (which of C3/C4 fail at runtime) was not measurable from the cited artifacts.

#### W2-05 · coverage · MEDIUM

- **Claim** (verbatim; `analyze-domain-w2.jsonl:5`): Two of the seven settlement values, `anomaly` and `cancelled`, have no asserted red path: E7's `settlement-unbacked` covers-list names only completed/running/silent-end, the four C-30 drills omit both, and no test module or quickstart scenario asserts the cancelled derivation or INV06's negative (process death is never cancellation).
- **Propagation surface** (verbatim): the engine test matrix and fixtures; an INV06 inversion (death read as cancellation) could ship with all six new modules green
- **Locations**: `.specify/specs/106-background-silent-failure/data-model.md:93` · `.specify/specs/106-background-silent-failure/data-model.md:128` · `.specify/specs/106-background-silent-failure/contracts/enforcement-and-migration.contract.md:30` · `.specify/specs/106-background-silent-failure/contracts/enforcement-and-migration.contract.md:34` · `.specify/specs/106-background-silent-failure/contracts/settlement-contract.contract.md:16`
- **Recommendation**: Add red-path duties for `anomaly` and `cancelled`: E7 covers-list rows, at least one C-30 drill or C-31 fixture each, and a negative fixture proving INV06 (process death is never cancellation).
- **Validation**: not dispatched — MEDIUM/LOW skip the C/H wave (skill §7); severity is the worker-declared one.

#### W2-06 · underspecification · MEDIUM

- **Claim** (verbatim; `analyze-domain-w2.jsonl:6`): E4's `return-record` mechanism is defined only as `declared equivalent` and C-15 requires a `verified return` without naming the verifier or the resolvable evidence, so C2's `completed` gate can rest on an undefined parent declaration that C-06 also says cannot prove completion.
- **Propagation surface** (verbatim): C2/C4 `completed` derivation, INV02's independent-verification requirement, and the E4 evidence audit
- **Locations**: `.specify/specs/106-background-silent-failure/data-model.md:54` · `.specify/specs/106-background-silent-failure/contracts/carrier-conformance.contract.md:18` · `.specify/specs/106-background-silent-failure/contracts/settlement-contract.contract.md:32` · `.specify/specs/106-background-silent-failure/data-model.md:124`
- **Recommendation**: Define E4's `return-record` mechanism and what "declared equivalent" admits, and name the verifier and the resolvable evidence C-15 requires; tie the definition to INV02.
- **Validation**: not dispatched — MEDIUM/LOW skip the C/H wave (skill §7); severity is the worker-declared one.

#### W2-07 · inconsistency · MEDIUM

- **Claim** (verbatim; `analyze-domain-w2.jsonl:7`): INV04 makes a present E2 start record a precondition of `silent-end`, but E8 and E2 say C1 writes no new record and its four-piece is `not duplicated`, so C1's DEAD/NO_SIGNAL to `silent-end` mapping either fails INV04 as literally written or leaves E2's `c1-fork` carrier value without a writer.
- **Propagation surface** (verbatim): the engine C1 reader, the silent-end precondition check, the E2 carrier enum, and the C1 DEAD/NO_SIGNAL fixtures
- **Locations**: `.specify/specs/106-background-silent-failure/data-model.md:126` · `.specify/specs/106-background-silent-failure/data-model.md:101` · `.specify/specs/106-background-silent-failure/data-model.md:31` · `.specify/specs/106-background-silent-failure/data-model.md:24` · `.specify/specs/106-background-silent-failure/contracts/carrier-conformance.contract.md:10`
- **Recommendation**: Decide the C1 case once: either state that C1's existing four-piece satisfies E2 for `silent-end`, or remove `c1-fork` from E2's carrier enum and qualify INV04's precondition.
- **Validation**: not dispatched — MEDIUM/LOW skip the C/H wave (skill §7); severity is the worker-declared one.

#### W2-08 · ambiguity · MEDIUM

- **Claim** (verbatim; `analyze-domain-w2.jsonl:8`): C-13 states the `else silent-end` fallback only for TIMEOUT and leaves a RUNNING verdict without a settlement-time live check undefined, while INV03 forbids reading it as `running` and INV04 forbids `silent-end` unless the subject is gone or the deadline passed.
- **Propagation surface** (verbatim): the engine C1 verdict mapping and the reverse liveness fixture; an unverifiable RUNNING attempt can be coded either way
- **Locations**: `.specify/specs/106-background-silent-failure/contracts/carrier-conformance.contract.md:10` · `.specify/specs/106-background-silent-failure/data-model.md:125` · `.specify/specs/106-background-silent-failure/data-model.md:126` · `.specify/specs/106-background-silent-failure/quickstart.md:66`
- **Recommendation**: Extend C-13's fallback to RUNNING: an unverifiable RUNNING settles `silent-end` only when disappearance or deadline holds, otherwise `unknown` (or another explicitly named refusal); state the outcome.
- **Validation**: not dispatched — MEDIUM/LOW skip the C/H wave (skill §7); severity is the worker-declared one.

#### W2-09 · decision-tension · MEDIUM

- **Claim** (verbatim; `analyze-domain-w2.jsonl:9`): The C3 7-column header widening touches an engine parser that requires exact header equality, yet no decision-tension record states the alternative T-002 used for C2 (additive sidecar/claim artifact instead of editing a pinned format), its discriminating evidence, or its reopening condition.
- **Propagation surface** (verbatim): the C3 report contract and the engine's accepted-header rule; the rejected alternative and its revision trigger are unavailable to review and to future revision
- **Locations**: `.specify/specs/106-background-silent-failure/plan.md:82` · `.specify/specs/106-background-silent-failure/plan.md:69` · `.specify/specs/106-background-silent-failure/research.md:13` · `.specify/specs/106-background-silent-failure/research.md:30` · `.specify/specs/106-background-silent-failure/contracts/carrier-conformance.contract.md:22`
- **Recommendation**: Record a decision-tension entry for the C3 header widening (alternative: an additive sidecar like T-002; discriminating evidence: the parser's exact-header equality; expected anti-metric; reopening condition), or apply T-002's pattern to C3.
- **Validation**: not dispatched — MEDIUM/LOW skip the C/H wave (skill §7); severity is the worker-declared one.

#### W2-10 · overflow · LOW

- **Claim** (verbatim; `analyze-domain-w2.jsonl:10`): Four lower-severity findings are elided: C-28 enumerates three existing roots while the engine has four (no `--registry-dir`); Scale/Scope says 5 skill/report text edits while the source list holds four SKILL.md rows; the state-transition table gives no precedence for a non-zero exit combined with an explicit anomaly line; and the unknown rule is restated on five surfaces.
- **Propagation surface** (verbatim): engine CLI flag surface; tasks-stage scope accounting; anomaly-versus-failed derivation; post-implementation one-source-of-truth duplication
- **Locations**: `.specify/specs/106-background-silent-failure/contracts/enforcement-and-migration.contract.md:22` · `.specify/specs/106-background-silent-failure/research.md:10` · `.specify/specs/106-background-silent-failure/plan.md:29` · `.specify/specs/106-background-silent-failure/plan.md:129` · `.specify/specs/106-background-silent-failure/data-model.md:139` · `.specify/specs/106-background-silent-failure/contracts/settlement-contract.contract.md:16` · `.specify/specs/106-background-silent-failure/data-model.md:127`
- **Recommendation**: Fold the four elided items into the next round: C-28's root list (add `--registry-dir`), the 5-vs-4 text-edit count, exit≠0 + anomaly-line precedence, and de-duplicate the unknown rule onto one owner surface.
- **Validation**: not dispatched — MEDIUM/LOW skip the C/H wave (skill §7); severity is the worker-declared one.

### 4.3 Domain W3 — tasks, delivery surfaces, handoff, team, anchor (10 findings)

#### W3-01 · inconsistency · HIGH (validated: confirm)

- **Claim** (verbatim; `analyze-domain-w3.jsonl:1`): tasks.md permits disclosed small edits to plan-owned files (plan.md, data-model.md, contracts/, quickstart.md, research.md, feature-ref.md) while handoff.md and team.md forbid those same paths to every crew seat, so two clauses impose mutually exclusive write permissions on one object set.
- **Propagation surface** (verbatim): implement-stage write permissions and C-62 compliance: the crew either edits forbidden design artifacts under a PLAN-EDIT disclosure or halts for a decision; a silent territory breach is possible.
- **Locations**: `.specify/specs/106-background-silent-failure/tasks.md:66` · `.specify/specs/106-background-silent-failure/tasks.md:360` · `.specify/specs/106-background-silent-failure/handoff.md:42` · `.specify/teams/106-background-silent-failure/team.md:62`
- **Recommendation**: Pick one permission regime: add a PLAN-EDIT exception clause to handoff.md / team.md, or remove the PLAN-EDIT allowance from tasks.md and route small edits through the spec side; state precedence explicitly.
- **Validation**: `confirm` (severity kept)

  **evidence_supported** (verbatim): tasks.md:66 classifies plan.md, data-model.md, contracts/, quickstart.md, research.md, feature-ref.md as 'plan-owned 面（仅小修）', and tasks.md:360 permits implementation-driven small edits declared under PLAN-EDIT disclosure, halting only for substantive changes; handoff.md:42 states these same paths MUST stay forbidden to every seat carrying the expansion (C-62) with no PLAN-EDIT exception in the contract (lines 28-43); team.md:62-81 is a team-level territory.forbidden list naming the same six paths, and no seat-level entry (reporter reporting-territory, lines 123-125) removes them; handoff.md:26 and team.md:168-175 make the crew the executor of T001-T037, so the actor executing the tasks is the same actor set the forbidden lists bind, yielding mutually exclusive write permissions over one object set.

  **evidence_not_supported** (verbatim): tasks.md never names the crew, a seat, or the handoff/team contract as the PLAN-EDIT actor and states no precedence, so 'mutually exclusive for the same actor' relies on inferring '实现' = the crew; handoff.md:14 says design authority stays on the spec side (C-64), leaving open a spec-side-only reading; the PLAN-EDIT discipline's own text was not cited and was not read, so whether it routes small edits to the spec side is unobserved.

#### W3-02 · coverage · MEDIUM

- **Claim** (verbatim; `analyze-domain-w3.jsonl:2`): Feature-reference delivery surface 35 (the .specify/glossary.md silent-end proposal) is carried by no task row and checked by no DoD or GATE item.
- **Propagation surface** (verbatim): the silent-end term never reaches the glossary; later readers and commands have no canonical term, and every gate can pass without it.
- **Locations**: `.specify/specs/106-background-silent-failure/feature-ref.md:79` · `.specify/specs/106-background-silent-failure/tasks.md:19` · `.specify/specs/106-background-silent-failure/tasks.md:64`
- **Recommendation**: Add a task row (or DoD / GATE item) for delivery surface 35 (glossary `silent-end` proposal) with its wrap-up disposition.
- **Validation**: not dispatched — MEDIUM/LOW skip the C/H wave (skill §7); severity is the worker-declared one.

#### W3-03 · coverage · MEDIUM

- **Claim** (verbatim; `analyze-domain-w3.jsonl:3`): handoff.md and team.md require one writeback/<T-NNN>.yaml record per completed task (C-65), but tasks.md defines no task, DoD item or GATE check that produces or verifies those records.
- **Propagation surface** (verbatim): a complete T001–T037 run can pass every gate while writing zero writeback records, leaving the handoff contract unfulfilled and invisible to verification.
- **Locations**: `.specify/specs/106-background-silent-failure/handoff.md:50` · `.specify/teams/106-background-silent-failure/team.md:174` · `.specify/specs/106-background-silent-failure/tasks.md:15` · `.specify/specs/106-background-silent-failure/tasks.md:28` · `.specify/specs/106-background-silent-failure/tasks.md:64`
- **Recommendation**: Add a task / DoD / GATE duty that produces and verifies `writeback/<T-NNN>.yaml` records (C-65), or remove the requirement from handoff.md / team.md.
- **Validation**: not dispatched — MEDIUM/LOW skip the C/H wave (skill §7); severity is the worker-declared one.

#### W3-04 · inconsistency · MEDIUM

- **Claim** (verbatim; `analyze-domain-w3.jsonl:4`): T028 is classified both as a red-first test for new legacy/version behaviour written before T029 and as a post-implementation regression guard of existing behaviour, two mutually exclusive classifications that drive different ordering and red-first accounting.
- **Propagation surface** (verbatim): implement ordering and red-first evidence accounting: treating T028 as a regression guard defers it past T029, losing the pre-implementation red that the plan claims; treating it as red-first contradicts the stated migration/regression exception.
- **Locations**: `.specify/specs/106-background-silent-failure/tasks.md:9` · `.specify/specs/106-background-silent-failure/tasks.md:261` · `.specify/specs/106-background-silent-failure/tasks.md:308`
- **Recommendation**: Classify T028 once: either red-first before T029 (and drop it from the regression exception), or a post-implementation regression guard (and move its red-first claim accordingly); reconcile tasks.md:9/261/308.
- **Validation**: not dispatched — MEDIUM/LOW skip the C/H wave (skill §7); severity is the worker-declared one.

#### W3-05 · inconsistency · MEDIUM

- **Claim** (verbatim; `analyze-domain-w3.jsonl:5`): T031 regenerates the skills/internal mirrors but its [blockedBy:] list omits T019, whose edit to skills/internal/run-agent/SKILL.md is a mirrored source, contradicting the rule that cross-story dependencies are carried by [blockedBy:] and that mirrors come after all source edits.
- **Propagation surface** (verbatim): mirror regeneration can legally start before T019 closes, leaving .specify/skills/internal/run-agent/SKILL.md stale and producing a new drift member at GATE-6.
- **Locations**: `.specify/specs/106-background-silent-failure/tasks.md:267` · `.specify/specs/106-background-silent-failure/tasks.md:217` · `.specify/specs/106-background-silent-failure/tasks.md:295` · `.specify/specs/106-background-silent-failure/tasks.md:304`
- **Recommendation**: Add T019 to T031's `[blockedBy:]` list.
- **Validation**: not dispatched — MEDIUM/LOW skip the C/H wave (skill §7); severity is the worker-declared one.

#### W3-06 · duplication · MEDIUM

- **Claim** (verbatim; `analyze-domain-w3.jsonl:6`): The crew's complete write and forbidden path territory is declared twice, in team.md territory.write/forbidden and in handoff.md § Territory, with neither copy naming the other as owner.
- **Propagation surface** (verbatim): crew write permissions can diverge silently between the persisted team definition and the handed-off contract; a seat following one accepts writes the other forbids.
- **Locations**: `.specify/teams/106-background-silent-failure/team.md:17` · `.specify/teams/106-background-silent-failure/team.md:62` · `.specify/specs/106-background-silent-failure/handoff.md:28` · `.specify/specs/106-background-silent-failure/handoff.md:42`
- **Recommendation**: Declare one owner for the territory sets (team.md as the persisted definition) and make the other cite it, or vice versa.
- **Validation**: not dispatched — MEDIUM/LOW skip the C/H wave (skill §7); severity is the worker-declared one.

#### W3-07 · duplication · LOW

- **Claim** (verbatim; `analyze-domain-w3.jsonl:7`): DoD-3 restates the full 34-clause-to-task-row mapping in prose that § Contract Clause → Task Map already owns in table form.
- **Propagation surface** (verbatim): contract-coverage accounting has two copies inside tasks.md; an edit to one leaves a stale mapping a reader may follow.
- **Locations**: `.specify/specs/106-background-silent-failure/tasks.md:19` · `.specify/specs/106-background-silent-failure/tasks.md:124`
- **Recommendation**: Replace DoD-3's prose mapping with a pointer to § Contract Clause → Task Map.
- **Validation**: not dispatched — MEDIUM/LOW skip the C/H wave (skill §7); severity is the worker-declared one.

#### W3-08 · duplication · LOW

- **Claim** (verbatim; `analyze-domain-w3.jsonl:8`): The fr-uncovered accounting fact (37/41 with FR-036, FR-037, FR-039 and FR-040 unclaimed by contracts) is stated three times in tasks.md.
- **Propagation surface** (verbatim): the 37/41 figure and the four-FR set can drift across DoD-3, GATE-3 and Notes, so a reader may cite a stale accounting claim.
- **Locations**: `.specify/specs/106-background-silent-failure/tasks.md:19` · `.specify/specs/106-background-silent-failure/tasks.md:32` · `.specify/specs/106-background-silent-failure/tasks.md:359`
- **Recommendation**: Keep the 37/41 fact in one owner location (accountant output / GATE) and reference it from the other two.
- **Validation**: not dispatched — MEDIUM/LOW skip the C/H wave (skill §7); severity is the worker-declared one.

#### W3-09 · ambiguity · LOW

- **Claim** (verbatim; `analyze-domain-w3.jsonl:9`): DoD-2 counts 「5 处技能/报告文本」 but the feature reference's delivery surface lists only four skill files carrying skill text changes (items 6-9).
- **Propagation surface** (verbatim): DoD-2 closure cannot be satisfied point-by-point against the delivery surface; a fifth skill text may be invented or one surface omitted from verification.
- **Locations**: `.specify/specs/106-background-silent-failure/tasks.md:19` · `.specify/specs/106-background-silent-failure/feature-ref.md:35`
- **Recommendation**: Reconcile the count: name the fifth skill text in DoD-2, or correct 5 → 4 against the delivery surface.
- **Validation**: not dispatched — MEDIUM/LOW skip the C/H wave (skill §7); severity is the worker-declared one.

#### W3-10 · ambiguity · LOW

- **Claim** (verbatim; `analyze-domain-w3.jsonl:10`): handoff.md names all nine SCs as acceptance criteria while GATE-4 requires pass only for final-path SC-001/SC-002/SC-004 and T035 records the remaining SCs as measured supporting readings, so a verifier has no criterion for whether a failing supporting SC blocks acceptance.
- **Propagation surface** (verbatim): acceptance verdict divergence between the crew contract and the driver gate: a compliant run may be rejected, or a supporting-SC failure waved through.
- **Locations**: `.specify/specs/106-background-silent-failure/handoff.md:46` · `.specify/specs/106-background-silent-failure/tasks.md:33` · `.specify/specs/106-background-silent-failure/tasks.md:283`
- **Recommendation**: State whether a failing supporting SC blocks acceptance, aligning handoff.md:46 with GATE-4's final / supporting split.
- **Validation**: not dispatched — MEDIUM/LOW skip the C/H wave (skill §7); severity is the worker-declared one.

## 5. Unvalidated Findings appendix

None. The validation wave returned **0 reject** verdicts, so no finding was moved out of the main table. Rejected rows are the only residents of this appendix by the merge rule; MEDIUM/LOW rows that were never dispatched are not "rejected" and stay in §3/§4 without a validator block.

## 6. Checklist accountability (pass H)

Governed surface: `checklists/*.md` under the spec, items tagged `Gap`, unchecked. Measured by program: `checklists/requirements.md` has 18 checked / 0 unchecked / 0 Gap items; `checklists/background-settlement-2026-11-25.md` has 0 checked / 40 unchecked, of which exactly **2** carry the `Gap` tag in their annotation bracket — CHK037 at line 74 and CHK038 at line 75. (No item uses a literal `[Gap]`-only bracket; the tag appears inside the combined annotation list, matching the checklist Notes' own "`[Ambiguity]` / `[Gap]` 条目" phrasing.)

| Item | State | Disposition marker (machine-checkable) |
|---|---|---|
| CHK037 | unchecked, Gap | `CHK037 disposition: raised-as-finding W1-09` |
| CHK038 | unchecked, Gap | `CHK038 disposition: raised-as-finding W1-10` |

Arithmetic (governed set): unchecked [Gap] items **2** · raised-as-finding **2** · covered-by **0** · unraised **0** · undispositioned **0** → **unchecked + unraised + undispositioned = 0**. This axis does not block the gate.

Non-normative cross-references (the other 38 unchecked items are outside the Gap disposition rule; the checklist's own Notes assign item-answering to analyze/review, and 6 of them are in fact answered by findings this pass): CHK002 → W1-05 · CHK005 → W1-04 · CHK006 → W1-03 + W1-04 · CHK018 → W1-08 · CHK032 → W1-01 · CHK036 → W1-07. The checklist's six named candidate confirmation points (CHK002/005/006/018/032/036/038) are therefore all surfaced as findings; CHK037 adds the seventh (EP-005 premise-carriage) gap.

**Tick-integrity observation**: `checklists/requirements.md:18` ("Stability / containment claims name a baseline referent…") is checked although FR-039 / SC-009 name no baseline referent and EP-005 measured the checked equality red at base — raised as W1-07, not silently accepted.

## 7. Coverage summary (fixed read-only accounting step)

`account-clause-coverage.py --spec-dir .specify/specs/106-background-silent-failure --json` (no `--freeze`; the tasks stage owns the frozen baseline) → `status: uncovered`, exit 1; claimed clauses 34, files scanned 329, clause universe 2452, FR universe 41:

| Lane | Verdict | Reading |
|---|---|---|
| clause-uncovered | pass | 785 uncovered, 0 beyond the frozen baseline |
| fr-uncovered | fail | 37 of 41 FRs cited from clause groups; FR-036 / FR-037 / FR-039 / FR-040 uncited (the fact W3-08 re-states three times) |
| clause-unparsable | fail | 111 corpus files yield no clause id under the owner's forms; 1 declares a positive form (parse doubt, never zero-and-covered) — corpus-wide, not introduced by 106 |
| coverage-baseline-delta | pass | baseline holds 785 names; 785 uncovered items are baseline-internal and do not block |

This is **identical** to the tasks-stage frozen reading captured in `test-evidence/clause-coverage-tasks.txt` — no coverage drift since freeze. The `uncovered` status is inherited structural state (corpus-level unparsable forms + the four deliberately uncited FRs), disclosed here rather than dressed as a green; its one 106-specific component is already finding W3-08.

- Requirements coverage: 41 FR + 9 SC; 34/34 contract clauses claimed by a task row; FR claim rate 37/41 (90.2%).
- Task coverage: 37 task rows; the four contract-uncited FRs must be carried by explicit task-side accounting (their current state is W3-08's subject).

## 8. Feature linkage and constitution alignment

- **Pass G** ran in all three domains over their artifact sets; **0** feature-linkage findings. The feature-reference delivery surface is in scope via W3; its uncarried delivery row 35 is a coverage finding (W3-02), not a linkage defect.
- **Registry status** was not re-read in this integration pass (outside the dispatch read set). The checklist-stage header records row 106 = `Planned`, parent 095 = `Ready for Review`; this read-only stage changes neither.
- **Pass D** ran in W1 only (the constitution sat in the W1 read domain); **0** constitution findings. Consequently the constitution-authority carve-out (CRITICAL, never downgrade) had nothing to act on, and 0 CRITICAL is an evidence-backed reading, not an omission.

## 9. Task-side gaps (not a full unmapped-task sweep)

This integrator did not re-read `tasks.md` whole (the dispatch bounds the read set); the task-side picture comes from the W3 worker's evidence. Four task-side gaps are dimensional, not editorial: W3-02 (un-carried delivery row 35), W3-03 (un-produced C-65 writeback records), W3-04 (T028 double classification), W3-05 (T031 missing `blockedBy: T019`). Each would survive a green clause-coverage and gate run because no gate checks it — that is why they are reported at their stated severities.

## 10. Systemic observations (clusters; no row re-tiered)

1. **"Declared X" without a declaration surface** — W1-04, W2-04, W1-08: boundary values/rules are load-bearing yet have no named declarer, field, value domain or owner pointer. The pattern, not any single instance, is the systemic risk: every downstream fixture inherits an invented number.
2. **Verdict-set boundary collisions** — W1-01, W1-02, W2-01, W2-02, W2-03, W2-07, W2-08: a closed set of seven values repeatedly meets observations that fit two definitions (or one value carrying two criteria). The set is closed; its *mapping* is not.
3. **Legacy semantics assembled from separate clauses** — W1-01, W2-03: no single place states what a version-less or start-record-less attempt settles and exits with; each clause contributes one half.
4. **Governance copies without a declared owner** — W3-06, W3-07, W3-08, plus the tick-integrity note under W1-07: permission sets, clause mappings and accounting facts live on two or more surfaces with no `owner` designation, so they can drift independently.
5. **Obligations with no carrying artifact** — W3-02, W3-03, W1-09, W1-10, W2-05: duties exist in handoff/team/plan/edge-case prose but no task, DoD, GATE or fixture carries them, so a fully green run can still skip them.

## 11. Next actions and remediation

1. **Gate FAIL — do not start `/speckit.implement`.** The 10 HIGH findings must be repaired upstream (requirements / plan / data-model / contracts) and the analysis re-run; the driver owns that bounded repair decision.
2. Repair clusters, in leverage order:
   - **Verdict/definition collisions** — W1-02, W1-03, W2-01, W2-03 (+ the downgraded W1-01, W2-02 still need their wording fix even though they no longer block).
   - **Undeclared inputs** — W1-04, W2-04 (one fix likely closes both: a named declaration surface for threshold / deadline / grace).
   - **Unnamed carrier and evidence closures** — W1-06, W1-05.
   - **False-green preservation claim** — W1-07 (EP-005 fallback wording + checklist tick).
   - **Write-territory contradiction** — W3-01 (one permission regime).
3. After repair, re-run the affected detection domains only (the incremental re-check protocol) and re-validate every new or changed CRITICAL/HIGH.
4. Concrete remediation edits are offered per finding in §4 — **none applied** by this pass; applying them belongs to `/speckit.requirements`, `/speckit.plan` or `/speckit.tasks`.

## 12. Run notes

- **Anomaly**: 未发现异常 — no decision-class anomaly was encountered. Two in-passing corrections, disclosed: (a) the verdicts record lives in git-ignored `.specify/state/`; it was copied verbatim to `test-evidence/validate-wave1.verdicts.json` so the dispatch's "commit the verdicts record" intent is satisfiable without bypassing `.gitignore`; (b) no second correction.
- **Read-only proof for the report itself**: no spec artifact was edited; the only writes are this report, the verdicts copy, the accounting records and the receipt.
- **Worker-disclosed noise**: W2 recorded an incidental grep overshoot outside its domain (tasks.md / checklist lines matched); every cited location is in-domain and the overshoot was not used as analysis input (spine U3 row).
- **Verdict-extraction normalization**: 7 validator outputs carried a literal double-brace layer from the prompt template; the driver normalized the brace layer when extracting all 12 verdicts (serialization-only, no missing fields; spine U3 row). Both notes are carried here so the report does not inherit an unstated process correction.
