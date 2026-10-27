# Requirements Quality Checklist: Review × Code-Review Composition (071)

**Purpose**: Post-tasks requirements-quality gate for Feature 071 — a "unit test for requirements writing" covering the risky surfaces this stage is chartered to probe: two-segment orchestration and failure propagation, the three applicability values, diff-base resolution, the coverage receipt's closed field set and exit codes, renderer-absence degradation, severity non-mapping with a single gate owner, the feedback boundary and the zero-new-wrap-up invariant, protection of existing contract assertions, and the two-hats sync surface. It validates the *requirement text*, not implementation behaviour.
**Created**: 2026-10-27
**Feature (Requirement Scope)**: Feature 071 — Review 命令与代码评审技能的组合与治理（Review × Code-Review Composition）
**Requirements (What)**: [requirements.md](../requirements.md)
**Specifications (How, context only)**: [plan.md](../plan.md) · [tasks.md](../tasks.md) · [data-model.md](../data-model.md) · [contracts/](../contracts/) · [research.md](../research.md) · [quickstart.md](../quickstart.md) · [feature-ref.md](../feature-ref.md)
**Distinct from**: `checklists/requirements.md` (the requirements-stage pre-plan completeness gate, 16 rows). This file is the post-tasks requirements-quality gate; it neither replaces nor re-checks that file's generic rows.

**Note**: plan, tasks, contracts, data model, research, and quickstart are cited only to expose requirement gaps, ambiguities, conflicts, and traceability breaks — never to grade the plan or the tasks, and never as an answer source. No item is answered by running the product; no upstream artifact is edited by this stage.

## Verdict Semantics

- `[x]` = **PASS** — the requirement text (including its Assumptions, Clarifications, Edge Cases, and named owner references) fixes the decision or names an owner so two readers reach the same verdict; an evidence pointer is given.
- `[ ]` = **FAIL** — a gap, ambiguity, conflict, or untraceable delegation remains; an evidence pointer and an analyze disposition are given.
- Every item is a question carrying a quality dimension and a requirement/SC or gap reference. `[Gap]`, `[Ambiguity]`, `[Conflict]`, `[Assumption]` mark items whose traceability is itself a missing or conflicting requirement.
- This is a judged checklist: **40 items — 13 PASS / 27 FAIL**. A FAIL is a requirements-quality finding handed to `analyze`, not a stage-run anomaly and not an instruction to edit upstream artifacts in this stage.
- Depth: Standard · Audience: Reviewer · Focus: the two clusters the stage brief names — (a) orchestration/failure propagation, applicability triage, base resolution, receipt grammar and verdict derivation; (b) the governance surfaces — single gate owner, feedback boundary, contract-assertion protection, two-hats sync. The stage brief fixes scope, risk, and depth, so the skill's intent-clarification round is not run in unattended mode.

**Same-author detection** (per `.specify/shared/workflow/objective-analysis-gate.md`): the `requirements → clarify → plan → tasks` set was written by earlier stage subagents in prior sessions, so the gate's literal same-session trigger does not fire; independent authorship across sessions already supplied cross-session freshness. This run exposes **no subagent dispatch capability** (no dispatch tool is available in the execution environment), so the delegated detection pass of rule 3 could not run. Detection was therefore a bounded direct read of `requirements.md` with `plan.md`, `tasks.md`, `data-model.md`, `contracts/`, `research.md`, and the live framework sources opened only to expose requirement gaps, and every FAIL row carries `(detected: direct read, subagent unavailable)` per rule 7 so the weaker evidence path stays visible. The downgrade rate rule 6 asks for cannot be computed on a non-delegated pass; that absence is recorded rather than papered over.

---

## A. Segment Orchestration & Failure Propagation (FR-001, FR-002, FR-019)

- [ ] CHK001 — When the process segment aborts before writing `review.md`, is it specified which artifact carries the code segment's subsection, and who is authorized to write it, given that the command template "MUST NOT inline either skill's methodology" (C-4) and the process report's structure is owned by `review-sdd-process`? [Gap, Req §FR-002, FR-010, FR-011]
  - **Verdict**: FAIL — FR-002 forbids suppressing the code segment and requires each conclusion "独立呈现", but the process report (`review.md`) is only ever produced by a process segment that by hypothesis failed. The data model resolves it structurally (`process-not-evaluated → code-triage`, E1) without naming an author, and C-5 requires the process segment to be recorded as `not-evaluated` in a report that may not exist. Two readers diverge: one has the command create a minimal report, the other lets the code record stand alone and reports only in the closing summary. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:118`; `requirements.md:109` (Edge Case 过程段中止或报错); `requirements.md:135`; `requirements.md:136`; `contracts/command-orchestration.md:14` (C-4); `contracts/command-orchestration.md:16` (C-5); `data-model.md:34` (E1 transitions); `data-model.md:36` (V1 requires both conclusions to exist as values).
  - **Disposition**: Decision — analyze must name the carrier and its author for the abort case (command-created minimal report vs record-only), or state that the run-level state lives outside `review.md` and say where.

- [ ] CHK002 — Is "收尾摘要" (closing summary) defined as an artifact surface, and is a run-level conclusion status carried anywhere, so that FR-002's "MUST NOT present the whole run as a completed review" and FR-019's "closing summary plus feature detail MUST present both conclusions" are verifiable rather than statements about a transient console message? [Ambiguity, Req §FR-002, FR-019, SC-001]
  - **Verdict**: FAIL — Key Entities calls the closing summary a component of the review run, FR-019 makes it a MUST surface, and C-14/C-53 add obligations to it, yet no requirement says what artifact holds it, what form it takes, or how a deterministic check reads it. SC-001 anchors the same disclosure duty on the process report instead ("同一份过程报告内"), so the two rows choose different carriers for one fact. A transient chat message cannot be re-verified after the run and cannot be asserted by a contract test. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:150`; `requirements.md:169` (评审运行 includes 一个收尾摘要); `requirements.md:118`; `requirements.md:180` (SC-001 anchors on the report); `requirements.md:108` (Edge Case 两段同时缺环境); `contracts/command-orchestration.md:34` (C-14); `contracts/status-gate-ownership.md:24` (C-53); `data-model.md:34`.
  - **Disposition**: Decision — analyze must fix one carrier (report section, record, or a declared out-of-verification transcript), reconcile FR-019 with SC-001, and say whether a run-level status literal exists.

- [ ] CHK003 — Does a `not-applicable` (or `not-evaluated`) code segment still write the code-segment record file, i.e. does FR-010's "代码段记录 MUST 写成特性目录内的独立文件" bind on a segment that judged nothing? [Ambiguity, Req §FR-003, FR-010, SC-005]
  - **Verdict**: FAIL — FR-010 states the record duty unconditionally and US1's first acceptance scenario only describes the `run` case; the data model reaches the opposite conclusion in E1's `artifacts` field ("`code-review.md` unless the code segment is `not-applicable`"), and C-39 says a segment that produced nothing is `not-evaluated` with a reason — which needs a home. So the reader who follows FR-010 literally writes a record that no design surface expects. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:119`; `requirements.md:135`; `requirements.md:27` (acceptance scenario 1 covers only the delta case); `requirements.md:99`; `data-model.md:32` (E1 `artifacts`); `contracts/coverage-receipt.md:24` (C-39); `contracts/status-gate-ownership.md:22` (C-52, three disclosure places, none of them the record).
  - **Disposition**: Decision — state whether the non-`run` triage values write the record (and with what minimum content) or explicitly exempt FR-010's file duty for them.

- [x] CHK004 — Is the no-merge rule stated as an artifact-level prohibition (no field, table, or score may store a cross-vocabulary value) rather than only as a behavioural preference? [Clarity, Req §FR-001, FR-007]
  - **Verdict**: PASS — FR-001 forbids merging the two conclusions into one severity system or score, FR-007 forbids any numeric conversion table, mapping matrix, or unified score, and the prohibition is closed at the storage layer: E3 V5 states no field exists that stores a mapped or weighted value, C-50 forbids any artifact providing a place to store one, and Q3 records the single directional gate relation as the only link between the vocabularies.
  - **Evidence**: `requirements.md:117`; `requirements.md:129`; `requirements.md:215` (Q3); `contracts/command-orchestration.md:10` (C-2); `contracts/status-gate-ownership.md:18` (C-50); `data-model.md:61` (V5).

- [x] CHK005 — Is the process segment's unconditional duty stated with a closed exemption list, so an implementer cannot invent a fourth reason to skip it? [Completeness, Req §FR-002]
  - **Verdict**: PASS — FR-002 enumerates the three candidate exemptions the brief raised (execution/expression class, command parameters, absent code delta) and forbids each; C-3 adds the fourth possible reading (an earlier segment's outcome) which follows from the fixed order anyway; V4 states no field of E1 or E4 may be read as an exemption, and Q1 records why parallel or mode-selected variants were rejected.
  - **Evidence**: `requirements.md:118`; `requirements.md:213` (Q1); `contracts/command-orchestration.md:12` (C-3); `data-model.md:49` (V4).

## B. Applicability Triage, Review Object & Diff Base (FR-003…FR-006)

- [ ] CHK006 — Is the first applicability value pinned as a verbatim literal, given that its two siblings are pinned in Shared Strings and the contract fixes it as `run`? [Gap, Req §FR-003, Shared Strings]
  - **Verdict**: FAIL — FR-003 closes the triage set at three values but names the first only in prose ("存在本特性已提交代码 delta 则运行"), while `not-applicable` and `not-evaluated` are pinned as STR-001/STR-002 and consumed verbatim by contracts and tests. The contract writes `run` (§C-6), the data model writes `run` (§E4), and T004 pins "the three applicability values" — so a test-consumed literal exists with no Shared Strings row and no `[[STR-NNN]]`-style citation convention covering it. This is the same defect class as CHK015. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:119`; `requirements.md:200` (Shared Strings table, STR-001…STR-004); `requirements.md:207` (citation convention); `contracts/command-orchestration.md:18` (C-6); `data-model.md:68` (E4 `value`); `tasks.md:207` (T004).
  - **Disposition**: Correction — pin the first value as a Shared Strings row and cite it as `[[STR-NNN]]` wherever the triage set is enumerated.

- [ ] CHK007 — Is "已提交代码 delta" bounded by a file-class rule, so a feature whose committed delta contains only `requirements.md`/`plan.md`/`docs/` files resolves to one triage value rather than two? [Ambiguity, Req §FR-003, FR-004]
  - **Verdict**: FAIL — the triage basis admits two facts, "the feature produces no code deliverable" and "the feature has no committed code delta" (E4), but nothing defines which changed paths count as code. A docs-only feature with a non-empty committed delta satisfies neither fact unambiguously, and the base tiers will happily resolve a range for it; conversely this very feature's delta is `templates/`, `skills/`, `docs/`, `tests/` — a mix that no rule sorts. Two readers reach different triage values on the same repository state. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:119`; `requirements.md:99` (Edge Case 特性没有代码产出); `requirements.md:123`; `requirements.md:125`; `data-model.md:69` (E4 `basis` two facts); `contracts/command-orchestration.md:20` (C-7); `plan.md:169`.
  - **Disposition**: Decision — define the code-path predicate (or delegate it to a named owner) so the triage basis is mechanically decidable.

- [ ] CHK008 — Is the end of the reviewed slice (the head commit) specified anywhere with the same rigour as its base, so "本特性切片的已提交代码 delta" cannot silently absorb commits that belong to other work? [Gap, Req §FR-004, FR-005, FR-011]
  - **Verdict**: FAIL — the base gets three ordered tiers and a reproducibility rule, while the head is never mentioned: FR-004 says only that the object is the feature slice's committed delta, FR-005 speaks of the working tree, and FR-011 requires the report to record "基准与目标的提交标识" — a required field whose resolution rule no requirement states. The design then supplies `HEAD unless overridden` (E5) and a `GIT_HEAD`-style override outside any requirement. On a shared trunk (this line runs on `master`), `HEAD` legitimately contains other features' commits, so "the feature slice" and "base..HEAD" can be different objects. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:123`; `requirements.md:124`; `requirements.md:136`; `requirements.md:174` (特性切片基准 defines only the base); `data-model.md:82` (E5 `head_sha`); `contracts/code-review-skill.md:10` (C-18 covers base tiers only); `plan.md:147`.
  - **Disposition**: Decision — fix the head rule (fixed at `HEAD` at run start, overridable, or bounded by the slice) and state whether "the feature slice" can be a strict subset of base..HEAD.

- [ ] CHK009 — Is "仓库默认主干" (the repository's default trunk) identified by a rule, rather than left as a name the resolver must guess? [Ambiguity, Req §FR-004]
  - **Verdict**: FAIL — the third base tier is "the merge base with the repository's default trunk" and the Edge Case only forbids depending on the script's built-in default; neither states how the trunk is determined when `refs/remotes/origin/HEAD` is absent, when `origin` points at an unrelated upstream, or when both `main` and `master` exist with one stale. The plan measures exactly that shape in this repository (no `origin/HEAD`, `origin` = upstream, local `main` months behind `master`), so the ambiguity is live rather than theoretical: two resolvers pick different bases and therefore review different slices while both claiming tier 3. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:123`; `requirements.md:102` (Edge Case 主干叫 master); `requirements.md:125`; `contracts/code-review-skill.md:10` (C-18); `data-model.md:86` (V9); `plan.md:147`; `research.md` § R2.
  - **Disposition**: Decision — name the trunk-identification rule (or an explicit caller parameter with a stated fallback order) inside FR-004.

- [ ] CHK010 — Does the receipt's mechanical verdict conjunction apply when the resolved delta is empty (base == head, zero changed files), where the triage rule and the conjunction give opposite answers? [Consistency, Req §FR-003, FR-014, FR-015]
  - **Verdict**: FAIL — FR-003 records `not-applicable` for "无已提交 delta", while FR-014 states the verdict conjunction absolutely: a zero-file delta yields `gap_files = 0`, `skipped_files = 0`, no `blocking` — and therefore `pass`, which would report a review of nothing as a clean result and directly contradicts FR-015's evidence rule. C-38's conjunction carries no state precondition, and only V20 ("`not-applicable` is reachable only through E4") keeps the two rules apart, at the data-model layer rather than in the requirement. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:119`; `requirements.md:142`; `requirements.md:143`; `requirements.md:181` (SC-002); `contracts/coverage-receipt.md:22` (C-38); `data-model.md:147` (E9 table, `0/0/0 → pass`); `data-model.md:156` (V20).
  - **Disposition**: Correction — scope FR-014's conjunction to `triage = run` with a non-empty changed-file set, and state that an empty delta is triaged before the receipt runs.

- [ ] CHK011 — Is the uncommitted-scope disclosure given a slot in FR-011's otherwise closed content list, and do the requirements agree with the design on which artifact carries it? [Conflict, Req §FR-005, FR-011]
  - **Verdict**: FAIL — FR-005 requires that "报告 MUST 显式披露未评审范围"; FR-011 closes the code subsection's content at seven items, none of which is the uncommitted scope; the design then splits the duty: C-44 puts it in the code record, E4's `worktree_uncommitted` says "the report discloses the unreviewed scope". Because FR-011 declares its list closed ("只承载"), a reader honouring FR-005 inside `review.md` breaks FR-011, and a reader honouring FR-011 leaves only the record — the artifact SC-001's one-file reader never opens. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:124`; `requirements.md:136`; `requirements.md:44` (US2 acceptance scenario 2 says "报告显式披露"); `contracts/coverage-receipt.md:34` (C-44 places it in the record); `contracts/command-orchestration.md:24` (C-9's closed list); `data-model.md:72` (E4).
  - **Disposition**: Correction — add the uncommitted-scope disclosure to FR-011's enumerated content and align C-9/C-44/E4 on one carrier (or state that the disclosure lives in both by design).

- [x] CHK012 — Is the base-resolution failure path closed, so no reader can substitute a guess or a branch default for an unresolvable base? [Coverage, Req §FR-006, FR-003]
  - **Verdict**: PASS — FR-006 requires `not-evaluated` plus a reproducible command and the failure reason, explicitly forbids a guessed base and a "close enough commit", FR-004 forbids the script's built-in default, and C-20 repeats the no-fallback rule including the branch-name case; V11 makes it the only legal outcome. The environment-failure value in FR-003 gives the same failure a second, consistent home.
  - **Evidence**: `requirements.md:125`; `requirements.md:119`; `requirements.md:101` (Edge Case 首次提交缺失); `contracts/code-review-skill.md:14` (C-20); `contracts/coverage-receipt.md:16` (C-35); `data-model.md:88` (V11).

## C. Coverage Receipt, Exit Codes & Evidence Form (FR-013, FR-014, FR-015)

- [ ] CHK013 — Is the receipt command's exit-code alphabet closed, and is "cannot evaluate" distinguishable from "gap" by a rule the requirements own, rather than only by a contract clause? [Gap, Req §FR-014, SC-002]
  - **Verdict**: FAIL — FR-014 requires "非零退出码" for a gap and zero for a clean set, and SC-002 measures the same thing; the design then introduces a second non-zero meaning (exit `2` for an unresolvable range, a missing record, or an unusable repository — C-35, E10's third code), so a contract test asserting `2` has no requirement row authorizing a distinct code. A reader implementing FR-014 literally may emit `2` for a gap or `1` for an unusable state, and both remain traceable to the requirement text while contradicting the pinned contract. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:142`; `requirements.md:181` (SC-002); `requirements.md:125`; `contracts/coverage-receipt.md:14` (C-34); `contracts/coverage-receipt.md:16` (C-35); `data-model.md:165` (E10 codes); `tasks.md:257` (T015 asserts three codes).
  - **Disposition**: Correction — state the closed exit-code set and each code's meaning in FR-014 (gap vs cannot-evaluate), so the third code is requirement-traceable.

- [ ] CHK014 — Are the legal grounds for a "带理由跳过" (reasoned skip) bounded, or may any free-text reason discharge the per-file verdict while keeping exit `0`? [Ambiguity, Req §FR-014]
  - **Verdict**: FAIL — FR-014 accepts a skip as a legal verdict with a reason and only the Edge Case names the intended grounds (a focus pass after the size guard); the design leaves the field as free text with no enumerated classes. A run may therefore record 50 files as skipped with a placeholder reason, exit `0`, and still satisfy FR-014's letter — the verdict conjunction keeps it out of `pass`, so the anti-pretense property survives, but the "reasoned" qualifier carries no obligation a reader can test, and SC-002's focused-pass sample only exercises one ground. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:142`; `requirements.md:104` (Edge Case 体量守门); `requirements.md:181` (SC-002); `data-model.md:136` (E8 `reason` = free text); `contracts/coverage-receipt.md:18` (C-36).
  - **Disposition**: Decision — enumerate the recognized skip grounds (or delegate the ground set to a named owner) and say whether an unrecognized reason is legal.

- [ ] CHK015 — Are the four segment-verdict values pinned as verbatim literals, given that only two of them appear in Shared Strings while tests and contracts consume all four? [Gap, Req §Key Entities 段裁决, FR-011, FR-014]
  - **Verdict**: FAIL — Key Entities closes the verdict set at four values but writes them in prose (通过 / 存在未清除阻断 / 不适用 / 不可评估); STR-001/STR-002 pin only the last two, and the contract fixes `pass` and `blocked` (§C-39), which the data model's derivation table and every test then consume. So the two values that carry the gate's outcome are the two that no Shared Strings row pins — the same defect class as CHK006, and the one that a relabelling request (FR-007) would most easily exploit. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:173` (Key Entities 段裁决); `requirements.md:200` (Shared Strings); `requirements.md:142`; `requirements.md:136`; `contracts/coverage-receipt.md:24` (C-39); `data-model.md:143-153` (E9 set and derivation).
  - **Disposition**: Correction — pin `pass` and `blocked` as Shared Strings rows and cite them as `[[STR-NNN]]` wherever the verdict set is closed.

- [ ] CHK016 — Is SC-003's "全文不出现声称完成渲染式评审的表述" made measurable by a phrase class or a forbidden-literal set the criterion owns? [Measurability, Req §SC-003, FR-013]
  - **Verdict**: FAIL — FR-013 and C-23 state the anti-pretense prohibition well, but SC-003 is the acceptance criterion and quantifies it only as "any statement claiming a rendered/visual review". Neither the requirement nor the measurement-source row enumerates the phrases a check would search for, so the criterion can be satisfied by scanning for whatever word the implementer chooses — a green that would not go red when a claiming sentence is added in different wording. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:182` (SC-003); `requirements.md:192` (SC-003 Source, "检索文本模式标记与禁用表述"); `requirements.md:141`; `contracts/code-review-skill.md:20` (C-23); `quickstart.md` scenario D.
  - **Disposition**: Decision — fix the forbidden-phrase class (or a closed literal list) inside SC-003 or name the owner that holds it.

- [ ] CHK017 — Is the rule that selects rendered versus text mode stated beyond bare renderer availability, including the non-TTY / agent path FR-021 targets, and is the rendered-mode marker literal pinned as its text counterpart is? [Ambiguity, Req §FR-013, FR-021]
  - **Verdict**: FAIL — FR-013 says rendered mode is the default "whenever the renderer is available", and FR-024 repeats it for the human path; nothing conditions the choice on an interactive terminal, which is precisely the environment the composition targets. A run with `delta` on `PATH` and no TTY would then carry a rendered-mode marker while no visual review ever happened — the state C-23 forbids in words. The rendered literal itself (`renderer: delta`) exists only in the data model, while its text sibling is pinned as STR-003. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:141`; `requirements.md:158`; `requirements.md:103` (Edge Case 交互输入); `requirements.md:155`; `requirements.md:204` (STR-003 = text form only); `data-model.md:99` (both marker literals); `contracts/code-review-skill.md:18` (C-22).
  - **Disposition**: Decision — state the mode-selection rule (availability plus path kind, or availability alone with the marker's meaning defined) and pin the rendered literal.

- [ ] CHK018 — Are the two senses of "覆盖率" separated in the requirement text, given that one is the artifact the code segment must produce and the other is the judgement object the review face must never reuse? [Ambiguity, Req §FR-014, FR-027, SC-005]
  - **Verdict**: FAIL — FR-014 names the evidence artifact a "覆盖率回执" while FR-027 forbids the expression-class review face from reusing code review's judgement objects "(编译、测试、覆盖率)". The same word therefore appears as a required deliverable and as a prohibited object, with no disambiguating clause in the requirements; the separation exists only in the contract (C-63). A reader could reasonably conclude the new receipt is itself the reuse FR-027 forbids. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:142`; `requirements.md:164`; `requirements.md:172`; `contracts/feedback-and-boundaries.md:24` (C-63); `data-model.md:121`; `tasks.md:305` (T027).
  - **Disposition**: Correction — add one clause stating that the receipt counts reviewed files, never test or compile coverage, and that FR-027's prohibition is about the latter.

- [x] CHK019 — Is the "sole evidence form" rule stated as a closed list of substitutes, including the prohibition on inferring a review from the existence of tool output? [Completeness, Req §FR-015]
  - **Verdict**: PASS — FR-015 makes the coverage receipt the only evidence form and names three substitutes explicitly (a diff overview, a changed-file listing, a small changed-line count) plus the tool-output inference that the brief flagged as the real hazard; C-25 repeats the list without widening it, and Q5 records the "不冒充" reasoning that replaces the old renderer-stop clause.
  - **Evidence**: `requirements.md:143`; `requirements.md:217` (Q5); `contracts/code-review-skill.md:24` (C-25); `requirements.md:172` (Key Entities 覆盖率回执).

## D. Severity Separation & the Single Gate Owner (FR-007, FR-008, FR-009)

- [ ] CHK020 — Is "未清除的 `blocking`" defined mechanically — what makes a `blocking` item cleared — given that the whole gate and the receipt's verdict conjunction both count it? [Gap, Req §FR-008, FR-014, SC-004]
  - **Verdict**: FAIL — FR-008 blocks on "未清除" items and FR-014 / C-38 read "无未清除 `blocking`" as one of three verdict signals; the requirement set never says how an item becomes cleared (deleted from the record, annotated, or reclassified), and the existing instrument counts every `blocking` line present in a record (`git-delta-review.sh` `report --summary` sums by severity). So the "cleared" state that SC-004's second run depends on has no representation in any artifact the requirements describe — SC-004 asks a deterministic check to observe a transition whose target state is undefined. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:130`; `requirements.md:142`; `requirements.md:183` (SC-004, "清除后同一转换通过"); `skills/internal/code-review/scripts/git-delta-review.sh:442-455` (presence-based count); `skills/internal/code-review/SKILL.md:55`; `contracts/status-gate-ownership.md:10` (C-46); `data-model.md:147` (E9 `unresolved blocking` column).
  - **Disposition**: Decision — define the clearing convention (or redefine the condition as presence-based and drop the word "未清除"), and align SC-004's two runs with it.

- [ ] CHK021 — Does the requirement resolve the interaction between "the gate is a property of the transition, so every initiator cites it" and the workflow order in which `/speckit.checklist` runs before `/speckit.review` has produced any code-segment evidence? [Conflict, Req §FR-008]
  - **Verdict**: FAIL — FR-008 makes every initiating path, explicitly including `/speckit.checklist`'s same-named row, cite the owner row, and the owner row (once amended) requires review evidence produced and no unresolved `blocking` in the code segment. But the SDD chain runs checklist before implement and therefore before review, and the integration protocol's own annotation scopes the checklist row to "applies only when the checklist runs after implement". Two readings survive: the checklist's transition becomes unavailable until a review ran, or the checkbox row keeps its conditional scope and the "every initiator" clause is advisory for it. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:130`; `requirements.md:230` (clarify adjudication of the single checkpoint); `contracts/status-gate-ownership.md:14` (C-48); `shared/workflow/feature-integration.md:37` (checklist row and its annotation); `shared/workflow/feature-integration.md:38` (review row); `templates/feature-details-template.md:71`; `tasks.md:281` (T021 converges both rows).
  - **Disposition**: Decision — state whether the checklist row is a true initiator under the new conditions or an explicitly conditional one, and what the checklist stage does when the code segment has not run.

- [ ] CHK022 — Is "explicit user ruling" defined for the unattended path the specification declares as its primary call shape, where no user is present to rule? [Ambiguity, Req §FR-009, Assumption A4]
  - **Verdict**: FAIL — FR-009 accepts a waiver only from an explicit user ruling and forbids the agent from downgrading, excluding, or merging a `blocking` item; A4 declares the agent the main caller. The combination is determinate for the agent (no waiver) but leaves the run's disposition undefined: the requirements never say what an unattended run records or hands back when an unresolved `blocking` makes the transition impossible, nor whether a driver-level confirmation counts as "explicit user ruling" (a driver is an agent, not a user). The Edge Case names only the human-asked case. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:131`; `requirements.md:106` (Edge Case 用户明确要求先合入); `requirements.md:239` (A4); `requirements.md:183` (SC-004); `contracts/status-gate-ownership.md:20` (C-51); `data-model.md:168` (V22).
  - **Disposition**: Decision — state the unattended disposition (halt-and-report with a named reason, or a defined waiver authority) and whether a driver confirmation qualifies.

- [x] CHK023 — Is the `Implemented → Ready for Review` criterion owned by exactly one declared owner, with the duplicate summary wording converged to a reference rather than reworded? [Clarity, Req §FR-008]
  - **Verdict**: PASS — FR-008 names `templates/feature-details-template.md` § Canonical Status State Machine as the owner, requires the integration protocol's summary row to become a reference, and forbids a second criteria wording; C-45/C-47/C-48 bind that owner and both initiators, and the two disagreeing rows the requirement was written against are still visible today (owner row: deferred tasks plus review evidence; protocol row: `review.md` committed plus deferred items) — so the requirement is measurably a change and the direction is unambiguous.
  - **Evidence**: `requirements.md:130`; `requirements.md:232` (clarify recheck of the owner quotation); `templates/feature-details-template.md:71`; `shared/workflow/feature-integration.md:37-38`; `contracts/status-gate-ownership.md:8` (C-45), `:12` (C-47), `:14` (C-48).

- [x] CHK024 — Does the requirement fix what happens at the two undecided edges of the gate — an `important`-only record, and a refused transition — including where each fact is disclosed? [Completeness, Req §FR-008, FR-009]
  - **Verdict**: PASS — `important` allows the transition but requires a per-item answer while the four lower levels never block (FR-008, C-49); a refusal leaves the status at `Implemented` with a reason naming the failed condition (clarify adjudication, C-53); a waiver is recorded in the report and the feature detail (FR-009, C-51); and `not-applicable`/`not-evaluated` are disclosed in three named places (C-52) rather than being silently non-blocking. The single-checkpoint timing is also fixed (after both artifacts, C-54), which is what makes "refused" well-defined.
  - **Evidence**: `requirements.md:130`; `requirements.md:230`; `contracts/status-gate-ownership.md:16` (C-49), `:22` (C-52), `:24` (C-53), `:26` (C-54); `data-model.md:168` (V22).

## E. Feedback Boundary & Wrap-Up Invariants (FR-016…FR-020)

- [ ] CHK025 — Is the unit census of one composed run stated, given that the run nests three separately-registered units (the command, the process skill, the code-review skill) while the nested-execution clause speaks of "两个单元"? [Gap, Req §FR-018, Key Entities 评审运行]
  - **Verdict**: FAIL — FR-018 says "命令与技能两个单元 MUST 各自完成自己的收尾记录", and E12 fixes exactly two `unit_id` values (`/speckit.review`, `skill:code-review`) — but the composed run also invokes `review-sdd-process`, whose own compiled wrap-up records under `skill:review-sdd-process`, a third unit. Two readings follow: the clause is scope-limited to the newly composed pair (three units actually record), or the run is expected to produce exactly two records (the process skill's own duty is dropped) — the second contradicts FR-016's "no step removed" spirit and FR-020's preservation clause. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:149`; `requirements.md:169`; `requirements.md:147`; `requirements.md:151`; `data-model.md:185` (E12 two `unit_id` values); `skills/internal/review-sdd-process/SKILL.md:186` (its own `unit_id`); `skills/internal/code-review/SKILL.md:105`; `templates/commands/review.md:41` (command unit).
  - **Disposition**: Decision — state the per-run unit census and scope FR-018's pairing explicitly, so neither the process skill's record nor the two new records is lost.

- [ ] CHK026 — Is the "framework friction in, code defect out" classification decidable when the feature under review *is* the framework, i.e. when a code defect in `skills/`, `templates/`, or `scripts/` is literally framework friction? [Ambiguity, Req §FR-017, SC-007]
  - **Verdict**: FAIL — FR-017 sends framework friction to the store and keeps code defects in the record, and SC-007 builds its two samples on that split. But this repository is both framework source and a client project (two hats), so a `blocking` defect found in `git-delta-review.sh` is a framework defect and a code defect at once; neither the requirement nor the contract states which classification wins, and SC-007's constructed sample is silent on it. In this line's own review stage the code segment will judge framework sources, so the ambiguous case is the default case, not an exotic one. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:148`; `requirements.md:186` (SC-007); `requirements.md:218` (Q6, three optimizations); `contracts/feedback-and-boundaries.md:10` (C-56); `contracts/feedback-and-boundaries.md:12` (C-57); `plan.md:229` (R-07); `AGENTS.md` § Two Hats: Framework Source vs Client Runtime.
  - **Disposition**: Decision — state the precedence for a self-hosting review (either "the record only, with the environment friction still posted" or an explicit two-entry rule) and add the case to SC-007's sample set.

- [x] CHK027 — Is the unchanged wrap-up step set stated enumerably, so "no new closing step" is checkable against a published face? [Measurability, Req §FR-016]
  - **Verdict**: PASS — FR-016 enumerates the six steps and forbids new steps, side channels, and a second record type; the published compiled face of `templates/commands/review.md` carries exactly those six numbered steps today, so a comparison has both sides; C-55 repeats the set and forbids editing the compiled face, and the tasks place the new wording outside that face.
  - **Evidence**: `requirements.md:147`; `templates/commands/review.md:41-47` (six steps, measured 2026-10-27); `contracts/feedback-and-boundaries.md:8` (C-55); `tasks.md:303` (T025 writes outside the compiled face).

- [x] CHK028 — Is the no-new-store / zero-transmission invariant stated as a closed prohibition list rather than a general aspiration? [Completeness, Req §FR-020]
  - **Verdict**: PASS — FR-020 preserves five named mechanisms (same-commit registration, introspection as the legal global entry, zero automatic transmission, user-optional feedback, one unit per entry) and forbids three specific additions (an intake store, a second aggregation, any upload path); C-60/C-61 restate the preserved set and the forbidden set without widening either, and V26 makes it a storage rule. Q6 records the same five invariants as the adjudicated answer.
  - **Evidence**: `requirements.md:151`; `requirements.md:218` (Q6); `contracts/feedback-and-boundaries.md:18` (C-60), `:20` (C-61); `data-model.md:191` (V26).

- [x] CHK029 — Is the classification duty located in named surfaces, so that posting a code defect as feedback is a detectable rule violation rather than a matter of taste? [Measurability, Req §FR-017, SC-007]
  - **Verdict**: PASS — SC-007 states the testability requirement itself ("分类义务在命令模板与技能文案中可检出"), C-57 fixes the same two surfaces, and the tasks land the wording in exactly those two files rather than in the compiled wrap-up face. The two constructed samples are also named in SC-007's measurement source, so the criterion has both a subject and an oracle.
  - **Evidence**: `requirements.md:186` (SC-007); `requirements.md:196` (SC-007 Source); `contracts/feedback-and-boundaries.md:12` (C-57); `tasks.md:303` (T025), `tasks.md:304` (T026).

## F. Artifact Placement & Record Lifecycle (FR-010, FR-012)

- [ ] CHK030 — Is "特性详情的评审记录行" a referent that exists in the owner template, and does any requirement authorize changing that template's shape to create one? [Ambiguity, Req §FR-012]
  - **Verdict**: FAIL — FR-012 requires the code record to be cited from "the feature detail's review-record row"; the feature-detail owner template has a `## Latest Review` section holding narrative entries and a `[FEATURE_LATEST_REVIEW_SUMMARY]` placeholder — no row, and no structured field for an artifact path. The plan's delivery surface edits only the state-machine row of that template, so a reader who needs a row must add one without authorization, and a reader who reads "row" loosely writes a bullet. SC-005's feature-side reachability then depends on which reading won. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:137`; `requirements.md:150`; `templates/feature-details-template.md:19` (`## Latest Review`); `templates/feature-details-template.md:90` (`[FEATURE_LATEST_REVIEW_SUMMARY]` placeholder); `data-model.md:105` (V13 uses the same phrase); `plan.md:91` (the only template edit listed is the state-machine row); `contracts/command-orchestration.md:32` (C-13).
  - **Disposition**: Decision — name the exact surface (the `## Latest Review` entry, or a new authorized row) and state whether the template gains a structured field.

- [ ] CHK031 — Are the archive file's name format, its collision behaviour, and the first-run value of the archive field all fixed, so a re-run in the same second cannot leave the code segment without a record? [Clarity, Req §FR-010, FR-011]
  - **Verdict**: FAIL — FR-010 defines the archive as "[[STR-004]] 去扩展名 + `-<运行时间戳>.md`" without fixing the timestamp's resolution or format; the design picks `YYYYMMDD-HHMMSS` and then forbids overwriting an existing archive (exit `2`), which means two runs inside one second collide and the later run cannot write its record at all — a state no requirement covers, in the very repeated-run Edge Case the requirement does address. FR-011 also requires the report to carry "本次归档件路径" unconditionally, while the first run has none and the design's answer is a bare `none`, which no Shared Strings row pins. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:135`; `requirements.md:136`; `requirements.md:105` (Edge Case 同一次 review 被重跑); `data-model.md:175` (E11 path form); `data-model.md:104` (V12 exit 2 on an existing archive); `data-model.md:179` (V24); `contracts/command-orchestration.md:30` (C-12).
  - **Disposition**: Correction — pin the timestamp format and its resolution, state the collision disposition (sub-second suffix, replace, or a recorded `not-evaluated`), and pin the first-run archive field value.

- [x] CHK032 — Is the two-artifact rule stated so that neither file can absorb the other, and is the record's exclusion from downstream consumption complete? [Consistency, Req §FR-010, FR-012]
  - **Verdict**: PASS — FR-010 forbids mutual overwrite and a shared severity summary table, FR-011 closes the report subsection to pointers and counts, and FR-012 keeps the record out of the available-documents list and out of plan/tasks input while requiring feature-side reachability. C-11/C-13 repeat the rule without opening a second path, and V13 makes the exclusion a validation rule rather than an aspiration.
  - **Evidence**: `requirements.md:135`; `requirements.md:136`; `requirements.md:137`; `contracts/command-orchestration.md:28` (C-11), `:32` (C-13); `data-model.md:105` (V13); `data-model.md:207` (V27).

## G. Contract-Assertion Protection, Tests & Two-Hats Sync (FR-027, FR-028)

- [ ] CHK033 — Does FR-027's absolute prohibition ("existing contract assertions MUST NOT be deleted or weakened") authorize the one intentional pin change the design discloses, and does any requirement state the rule a changed pin must satisfy? [Conflict, Req §FR-027, FR-028]
  - **Verdict**: FAIL — FR-027 admits no exception, yet the design removes an existing assertion's subject (`test_review_p1_review_loop.py::test_c15_review_owns_the_ready_for_review_transition` stops requiring the duplicated criteria wording) and relies on a replacement-assertion rule ("keeps its subject, adds the owner path, adds a negative assertion, net assertions rise") that exists only in the contract and in the tasks' DoD row. Judged by FR-027's own words, the change is a weakening; judged by the design, it is a replacement. Analyze has to authorize one reading, because the implementation cannot satisfy both. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:164`; `requirements.md:165`; `contracts/feedback-and-boundaries.md:26` (C-64); `contracts/tests-and-docs-sync.md:12` (C-67); `plan.md:13`; `plan.md:225` (R-03); `tasks.md:21` (DoD-4); `tasks.md:317` (T030); `research.md` § R5.
  - **Disposition**: Decision — either authorize the one pin change in FR-027 with its replacement rule, or forbid it and converge the wording another way.

- [ ] CHK034 — Does FR-028 or SC-006 require that a new contract test would turn red when its subject breaks, or only that six groups exist and the suite gains no failures? [Gap, Req §FR-028, SC-006]
  - **Verdict**: FAIL — FR-028 requires deterministic coverage of six behaviours and SC-006 counts groups and compares failing names; neither states the falsifiability obligation, so a group of assertion-free or trivially true tests satisfies both rows. The obligation does exist one layer down (C-66's "a group that would stay green when its subject breaks is not coverage") and the tasks carry a red-first evidence sink, but a requirement-level reader can build all six groups green and never red and remain compliant — the exact "a green check is a claim, not evidence" defect the framework's own Fast Fail discipline names. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:165`; `requirements.md:185` (SC-006); `contracts/tests-and-docs-sync.md:10` (C-66); `tasks.md:316` (T029 records a non-reddening group as a fast-fail finding); `.specify/shared/guidelines/fast-fail.md` § 机器给出的绿同样受判据约束.
  - **Disposition**: Correction — add the red-first obligation to FR-028 and let SC-006 measure it (a recorded failing run per group), consistent with C-66.

- [ ] CHK035 — Is SC-006's name-level comparison anchored to a named baseline instant and artifact, or can "新增失败数为零" be measured against any convenient snapshot? [Ambiguity, Req §SC-006]
  - **Verdict**: FAIL — SC-006 says the full suite is compared by name with zero new failures, but names neither the baseline's capture point nor its artifact. The design supplies both (an implement-start name list written once, plus the tasks' gate that compares against it), so the criterion is implementable only by adopting a design decision the requirement never made — and this repository's own recurring lesson about test baselines makes an unanchored comparison a live rework risk rather than a stylistic one. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:185` (SC-006); `requirements.md:195` (SC-006 Source); `tasks.md:114` (E2 baseline slot); `tasks.md:181` (T002); `tasks.md:34` (GATE-5 form); `plan.md:22`.
  - **Disposition**: Correction — name the baseline instant (implement start) and its artifact in SC-006's source row.

- [ ] CHK036 — Does FR-028 give the mirror obligation an acceptance criterion, or only a mechanism ("projections are produced by the generators")? [Measurability, Req §FR-028]
  - **Verdict**: FAIL — FR-028 requires runtime projections to be produced by the existing regenerator and synchronizer and forbids hand-editing, but states no verdict rule: no baseline measurement, no "no NEW drift" criterion, and no statement of what counts as satisfied. The design supplies the criterion and the measured baselines (22 / 136 / 55 files plus per-tool copies), and the plan owns the per-pair table — so the requirement's own acceptance surface is a mechanism, and a run that edits a projection by hand and then re-runs the generator would satisfy the letter while losing the direction rule's purpose. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:165`; `contracts/tests-and-docs-sync.md:18` (C-70, "no NEW drift" + baselines); `plan.md:123` (measured baselines); `plan.md:127-134` (per-pair table); `tasks.md:47` (mirror baselines), `tasks.md:320` (T033).
  - **Disposition**: Correction — add the acceptance criterion (no NEW drift against a pre-edit measurement) to FR-028 and point at the plan's owner for the per-pair table.

- [x] CHK037 — Are the six coverage groups and the framework-source-only edit rule both stated so each is checkable without inventing a seventh obligation? [Completeness, Req §FR-028]
  - **Verdict**: PASS — FR-028 enumerates six groups that map one-to-one onto C-65's list (segments and order, three triage values, gate conditions, receipt non-zero exit, base resolution, docs/template isomorphism), names the three documentation surfaces, and fixes the framework source as the only edit surface; C-69 repeats the surface set (including `scripts/` only when a shared asset is touched) and the tasks keep `docs/` and `tests/` outside the mirror table.
  - **Evidence**: `requirements.md:165`; `contracts/tests-and-docs-sync.md:8` (C-65), `:16` (C-69); `plan.md:117`; `tasks.md:122`.

## H. The Code-Review Skill's Own Scope (FR-021…FR-026)

- [ ] CHK038 — Does FR-021's enumeration of the fully non-interactive path close every write the composed run must perform, including creating the record header and rotating a previous record? [Gap, Req §FR-021, FR-010]
  - **Verdict**: FAIL — FR-021 names three steps ("回执 + 意见落盘 + 汇总裁决"), while the composition needs four deterministic operations: base resolution, record creation with rotation, opinion capture, and the receipt/verdict. The omitted one is the record writer — the very step FR-010 makes mandatory on every re-run. A reader taking FR-021's parenthetical as exhaustive can leave record creation to the agent or to an interactive prompt and still be compliant, which breaks the unattended premise (A4) on the second run of any feature. (detected: direct read, subagent unavailable)
  - **Evidence**: `requirements.md:155`; `requirements.md:135`; `requirements.md:239` (A4); `contracts/code-review-skill.md:8` (C-17 lists four steps); `plan.md:176` (`start` subcommand); `data-model.md:94` (E6 written by `start`); `tasks.md:236` (T012).
  - **Disposition**: Correction — add record creation-and-rotation to FR-021's enumeration, consistent with C-17 and FR-010.

- [x] CHK039 — Are the skill's new deterministic obligations (scripted, overridable, repeatable base resolution; one verdict source taking the record path explicitly) stated so that satisfying one cannot break the other two preserved behaviours (the interactive path and its severity validation)? [Consistency, Req §FR-022, FR-023, FR-024]
  - **Verdict**: PASS — FR-022 puts base resolution in the script with a parameter override and a same-state determinism rule; FR-023 keeps the merge-gate verdict in the same script, requires exactly one verdict source and an explicit record path, and states the concrete false-green it prevents (a process report read as the code record); FR-024 preserves the interactive path, the rendered default, the per-file order, and the six-level validation. The three rows address different script surfaces, and the one place they could collide — the rendered default — is captured separately at CHK017.
  - **Evidence**: `requirements.md:156`; `requirements.md:157`; `requirements.md:158`; `contracts/code-review-skill.md:10` (C-18), `:26` (C-27), `:30` (C-28); `data-model.md:86` (V9), `:167` (V21).

- [x] CHK040 — Are the sister-skill boundary and the closed delivery surface both stated as decidable properties rather than as intentions? [Clarity, Req §FR-025, FR-026]
  - **Verdict**: PASS — FR-025 states precisely what each skill must declare (its own judgment object plus the composed relation) and names the sentence that must not survive, which makes the boundary checkable in the two skill bodies; FR-026 confines every new capability to the existing script entity and closes the delivery surface against new engines, resident processes, external services, and dependencies — repeated for commands, skills, agents, and rosters in C-72/C-73, so a scope sweep has an oracle.
  - **Evidence**: `requirements.md:159`; `requirements.md:160`; `contracts/code-review-skill.md:32` (C-29), `:34` (C-30); `contracts/tests-and-docs-sync.md:22` (C-72), `:24` (C-73); `plan.md:249`.

---

## Traceability Matrix

Every one of the 28 FR and all 7 SC appear in at least one item; the mapping is collective, not one-item-per-requirement.

| Requirement | Items | Aspect |
|-------------|-------|--------|
| FR-001 | CHK004 | fixed order / no merged vocabulary at artifact level |
| FR-002 | CHK001, CHK002, CHK005 | abort carrier, run-level status, unconditional duty |
| FR-003 | CHK003, CHK006, CHK007, CHK010, CHK012 | non-`run` record duty, `run` literal, code-delta class, empty delta, failure value |
| FR-004 | CHK007, CHK008, CHK009 | review object, head boundary, default trunk |
| FR-005 | CHK008, CHK011 | object boundary, uncommitted disclosure slot |
| FR-006 | CHK012 | unresolvable base, no guess |
| FR-007 | CHK004 | non-mapping, artifact-level prohibition |
| FR-008 | CHK020, CHK021, CHK023, CHK024 | clearing rule, checklist initiator, single owner, gate edges |
| FR-009 | CHK022, CHK024 | unattended waiver, waiver recording |
| FR-010 | CHK001, CHK003, CHK031, CHK032, CHK038 | artifact duties, non-`run` case, archive, non-overlap, record writer |
| FR-011 | CHK002, CHK008, CHK011, CHK015, CHK032 | subsection content, head id, disclosure slot, verdict literals, closedness |
| FR-012 | CHK030, CHK032 | feature-side referent, downstream exclusion |
| FR-013 | CHK016, CHK017 | anti-pretense measurability, mode selection |
| FR-014 | CHK010, CHK013, CHK014, CHK015, CHK018, CHK020 | conjunction scope, exit alphabet, skip grounds, verdict literals, vocab clash, blocking clearing |
| FR-015 | CHK010, CHK019 | evidence rule vs empty set, substitute list |
| FR-016 | CHK027 | unchanged wrap-up set |
| FR-017 | CHK026, CHK029 | classification decidable, two surfaces |
| FR-018 | CHK025 | nested unit census |
| FR-019 | CHK002 | closing-summary carrier |
| FR-020 | CHK028, CHK029 | closed prohibition list, duty surfaced |
| FR-021 | CHK038 | non-interactive path closure |
| FR-022 | CHK039 | scripted, overridable, repeatable base |
| FR-023 | CHK039 | single verdict source, explicit input |
| FR-024 | CHK039 | preserved interactive path |
| FR-025 | CHK040 | decidable boundary |
| FR-026 | CHK040 | closed delivery surface |
| FR-027 | CHK018, CHK033 | vocabulary separation, pin change authorization |
| FR-028 | CHK033, CHK034, CHK036, CHK037 | pin rule, falsifiability, mirror criterion, six groups + edit surface |
| SC-001 | CHK002 | one-file readability vs closing-summary carrier |
| SC-002 | CHK013, CHK014 | exit codes, focused-pass skip |
| SC-003 | CHK016, CHK017 | forbidden-phrase measurability, mode marker |
| SC-004 | CHK020, CHK021 | clearing, transition availability |
| SC-005 | CHK003, CHK018 | non-`run` record, reader-baseline separation |
| SC-006 | CHK034, CHK035, CHK037 | falsifiability, baseline anchor, group set |
| SC-007 | CHK026, CHK029 | self-hosting precedence, detectable duty |

**Surface coverage**: FR-001…FR-028 → all 28 referenced; SC-001…SC-007 → all 7 referenced. Shared Strings: STR-001/STR-002 → CHK006, CHK015; STR-003 → CHK017; STR-004 → CHK031. Contracts cited as gap sources: C-1…C-73 (all six files). Edge Cases cited: 特性无代码产出 (CHK003, CHK007), 主干命名 (CHK009), 交互输入 (CHK017), 体量守门 (CHK014), 重跑 (CHK031), blocking 先合入 (CHK022), 过程段中止 (CHK001), 两段同时缺 (CHK002). Assumptions cited: A4 (CHK022, CHK038). Clarifications cited: Q1 (CHK005), Q3 (CHK004), Q5 (CHK019), Q6 (CHK026, CHK028), the 2026-10-27 session (CHK002, CHK010, CHK021, CHK023, CHK024).

## Failing Items — Gate Hand-off

27 failing items are recorded for `analyze` disposition. None was repaired in this stage: `requirements.md`, `plan.md`, `tasks.md`, `data-model.md`, `contracts/`, `research.md`, `quickstart.md`, and `feature-ref.md` were read-only, and this file is new beside the untouched `checklists/requirements.md`.

**Decision-class (analyze / requirements adjudication required — two or more readings survive)**

- CHK001 — who writes `review.md` (or which artifact carries the code subsection) when the process segment aborted.
- CHK002 — the closing summary's carrier and the existence of a run-level conclusion status; reconcile FR-019 with SC-001.
- CHK003 — whether a `not-applicable` code segment writes the record file.
- CHK007 — the code-path predicate behind "committed code delta".
- CHK008 — the head/end boundary of the reviewed slice.
- CHK009 — the trunk-identification rule behind base tier 3.
- CHK014 — the recognized grounds for a reasoned skip.
- CHK016 — the forbidden-phrase class that makes SC-003 measurable.
- CHK017 — the rendered/text mode selection rule (availability alone vs interactive-terminal condition) and the rendered literal.
- CHK020 — what makes a `blocking` item "cleared", and SC-004's target state.
- CHK021 — whether `/speckit.checklist` is a full initiator under the new gate conditions, given it runs before review.
- CHK022 — the unattended disposition when a `blocking` makes the transition impossible.
- CHK025 — the per-run unit census (two or three closing records).
- CHK026 — classification precedence when the reviewed code *is* the framework.
- CHK030 — the "特性详情的评审记录行" referent, and whether the template's shape changes.
- CHK033 — authorization for the one intentional pin change and the replacement-assertion rule.

**Correction-class (one reading consistent with the recorded intent; fix locally and disclose)**

- CHK006 — pin the `run` literal in Shared Strings and cite it.
- CHK010 — scope FR-014's verdict conjunction to `triage = run` with a non-empty changed set.
- CHK011 — give the uncommitted-scope disclosure a slot in FR-011 and align C-9/C-44/E4 on one carrier.
- CHK013 — close the receipt exit-code alphabet in FR-014 (gap vs cannot-evaluate).
- CHK015 — pin `pass` and `blocked` in Shared Strings.
- CHK018 — state the two senses of "覆盖率" and that the receipt is never reader-baseline evidence.
- CHK031 — pin the archive timestamp format, the same-second collision disposition, and the first-run archive value.
- CHK034 — add the red-first obligation to FR-028 and let SC-006 measure it.
- CHK035 — anchor SC-006's name comparison to the implement-start baseline artifact.
- CHK036 — add the "no NEW drift" acceptance criterion to FR-028's mirror obligation.
- CHK038 — add record creation-and-rotation to FR-021's non-interactive enumeration.

## Validation Record

- **Checklist result**: 40 items — 13 PASS / 27 FAIL. FAILs are requirements-quality findings, not stage-run anomalies, and no upstream artifact was edited to close one.
- **Structure**: CHK001…CHK040 contiguous and unique; 40/40 items carry a quality dimension plus at least one `FR-`/`SC-` reference (100%, above the 80% floor); 28/28 FR and 7/7 SC appear in the matrix; 27 dispositions for 27 FAILs; per-item Verdict, Evidence, and (for FAILs) Disposition blocks present. Deterministic check output: `test-evidence/validate-checklist.txt`.
- **Detection path**: bounded direct read with no subagent dispatch available in this environment; every FAIL row carries `(detected: direct read, subagent unavailable)` per `objective-analysis-gate.md` rule 7. No downgrade rate is reported because detection was not delegated (rule 6 cannot be satisfied on a non-delegated pass, and the gap is recorded rather than estimated).
- **Upstream validators (post-write, read-only)**: `python3 scripts/python/validate-requirements.py .specify/specs/071-review-code-integration/requirements.md` and `python3 scripts/python/validate-tasks.py .specify/specs/071-review-code-integration/tasks.md` were re-run after this file landed; both results are recorded in the same evidence note. `git status --porcelain` and `git diff --stat` over the plan-owned artifacts confirm no plan edit was made, so no `PLAN-EDIT:` declaration was required.
- **Feature integration**: Feature 071 stays **Planned**. No lifecycle transition is performed by this stage — the feature is not `Implemented`, so `/speckit.checklist`'s `Implemented → Ready for Review` row does not apply here (and CHK021 records that the row's own applicability under FR-008 is an open question for analyze).
- **Test budget**: documentation-only stage. No test run, no full suite, no baseline capture; the implement-start (E2) and closure slots are untouched. The E3 stage-status row is `test-evidence/checklist.jsonl` with `status=not-run-docs-only`.
- **No implementation testing**: no product behaviour was executed; every verdict is a textual/judged reading of the requirement text against the cited files.
