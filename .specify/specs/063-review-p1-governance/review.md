# Specification-Driven Development (SDD) Process Review Report: Review P1 Governance（评审 P1 治理）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 063 |
| Requirement Key | 063-review-p1-governance |
| Requirement Name | Review P1 Governance（评审 P1 治理） |
| Related Feature | 063 Review P1 Governance（评审 P1 治理） — `.specify/memory/features/063.md`, status **Implemented** |
| Repository | spec-kit (distributed as `specify-cli`) |
| Repository URL | `origin` = `git@github.com:github/spec-kit.git` — this is the **UPSTREAM**, not the fork. The remotes that would hold these commits are `github` = `git@github.com:cloud-native-ai/spec-kit.git`, `gitee` = `git@gitee.com:cloud-native-ai/spec-kit.git`, `gitlab` = `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git`. All three are SSH, none is HTTPS-web-accessible. |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains HEAD` returns empty — HEAD is not on any remote. Cite absolute paths + `git show <sha>:<path>` instead of URLs. |
| Branch | 063-review-p1-governance |
| Commit SHA | a969e3107c862d6ac1d8dd1854edb70da7fc0789 (short: a969e310) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit |
| Review Date | 2026-10-20 |
| Reviewer (Agent) | SDD Executor — fresh-context stage dispatch running `/speckit.review`, delegated to skill `review-sdd-process` (`.specify/skills/internal/review-sdd-process/SKILL.md`) |
| Environment | Linux 5.10.134-15.2.al8.x86_64; bash; Python 3.11.11; pytest 8.4.2; `CWS_LIB_BASH_HOME=/storage/project/cloud-native-tools/cws-lib-bash` resolvable |
| spec-kit Source Snapshot | This repository **is** the spec-kit source (self-hosting; see `.specify/instructions.md` § Two Hats). Packaged version `0.0.22` per `/storage/project/cloud-native-ai/spec-kit/pyproject.toml` line 3. Every `templates/`, `shared/`, `scripts/`, `skills/` path cited below is a framework-source path, not a `.specify/` runtime copy. |

**Path convention used in this report.** Because §0 records the commit as **UNRESOLVABLE**, no remote-web permalink written here would resolve. Every path is therefore given as an absolute path on the checkout that produced this report **and**, in backticks immediately after it, the repo-relative form; a maintainer on any other checkout resolves the relative form against their own repo root. Absolute paths are checkout-local by nature — the relative form is the portable one, and `git show a969e3107c862d6ac1d8dd1854edb70da7fc0789:<relative-path>` recovers the exact bytes on any clone that has the branch.

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 316 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/requirements.md | FR-001..FR-030, SC-001..SC-014, two decision-level clarifications (E1 run-id idempotency; E2 transition ownership) (`requirements.md`) |
| plan.md | 155 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/plan.md | Constitution Check 16/16, feature-level goal mapping F1–F8 → mechanism fixes (`plan.md`) |
| research.md | 55 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/research.md | Phase 0 D-1..D-13 verified decisions, incl. the D-5 generator premise falsified at implement (`research.md`) |
| data-model.md | 208 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/data-model.md | E1..E13 design entities for the mechanism fixes (`data-model.md`) |
| quickstart.md | 103 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/quickstart.md | S0..S10 verification recipes (`quickstart.md`) |
| contracts/template-mechanisms.md | 74 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/contracts/template-mechanisms.md | C-1..C-19 template/checklist/review-loop mechanism clauses (`contracts/template-mechanisms.md`) |
| contracts/engine-face-contract.md | 42 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/contracts/engine-face-contract.md | C-20..C-25 compiled wrap-up face clauses (`contracts/engine-face-contract.md`) |
| contracts/evidence-baseline-contract.md | 30 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/contracts/evidence-baseline-contract.md | C-26..C-30 evidence-binding and baseline pre-flight clauses (`contracts/evidence-baseline-contract.md`) |
| contracts/cross-cutting-constraints.md | 25 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/contracts/cross-cutting-constraints.md | C-31..C-34 sync/baseline cross-cutting constraints (`contracts/cross-cutting-constraints.md`) |
| tasks.md | 401 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/tasks.md | 51 tasks all `[X]`, DoD-1..8, GATE-1..8, 34 green-point claims, two in-line void annotations (`tasks.md`) |
| verification.md | 611 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/verification.md | SC-001..SC-014 all pass, per-US mechanism evidence, GATE/DoD re-verification, void disclosures (`verification.md`) |
| feature-ref.md | 101 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/feature-ref.md | FR→clause map, SC→verification map, deliverable surface (`feature-ref.md`) |
| checklists/requirements.md | 41 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/checklists/requirements.md | 16/16 items checked (`checklists/requirements.md`) |
| checklists/requirements-quality.md | 82 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/checklists/requirements-quality.md | CHK001..CHK040, **0/40 checked**, 11 unchecked items Gap-tagged (`checklists/requirements-quality.md`) |
| coverage-baseline.txt | 497 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/coverage-baseline.txt | First coverage baseline frozen by tasks (F1 mechanism's own deliverable) (`coverage-baseline.txt`) |
| notes/baseline-failed-tests.txt | 63 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/notes/baseline-failed-tests.txt | Frozen name-level failed-test baseline, 63 sorted names (`notes/baseline-failed-tests.txt`) |
| features/063.md | 66 | /storage/project/cloud-native-ai/spec-kit/.specify/memory/features/063.md | Registry detail: status Implemented (`features/063.md`) |
| 062 review report (input) | 528 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/062-humanize-command/review.md | The six P1 + two P2 findings (F1–F8) this feature turns into mechanism fixes (`062-humanize-command/review.md`) |

**Same-author gate status** (owner: `/storage/project/cloud-native-ai/spec-kit/.specify/shared/workflow/objective-analysis-gate.md`, `shared/workflow/objective-analysis-gate.md`). The gate **does not fire**: every artifact in the inventory above was committed between 2026-10-19 20:35 and 2026-10-20 02:42 by nine prior stage dispatches, none of them this reviewer. The P0 independent-validation wave was nevertheless run unconditionally: 1 P0 candidate raised → 1 fresh-context read-only validation subagent (finding + re-derivation commands only, no reviewer reasoning, no sibling findings) → **CONFIRM P0**; downgrade rate **0 of 1** (§ 7).

## 1. Process Execution Timeline

Reconstructed from `git log --grep=063-review-p1-governance` (13 commits, 2026-10-19 20:35 → 2026-10-20 02:42) plus the stage logs under `/tmp/sdd-review-p1/`. Stage order: requirements → clarify → plan → tasks → checklist → analyze → implement (attempt 1 → halt → instructions → attempt 2).

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | 20:35 `/speckit.requirements` — spec + requirements checklist (16/16 checked) land | `a4ee863e` | None |
| 2 | 20:36 anti-vacuity tightening of success criteria | `80bb1340`; requirements validator 0/0 | None |
| 3 | 20:47 `/speckit.clarify` — Feature 063 bound; the two decision-level questions settled (E1 idempotency untouched; E2 `/speckit.review` owns `Implemented → Ready for Review`) | `ea79ceda`; requirements § Clarifications | None |
| 4 | 21:15 `/speckit.plan` — plan + Phase 1 design (4 contracts, 34 clauses); research D-5 freezes the mechanism-owner premise "the live `.specify/instructions.md` receives it via `scripts/bash/generate-instructions.sh`" without executing that mechanism | `2bcee2ac`; `research.md` § D-5 | **Yes** — unverified behavioral premise frozen → **F2** |
| 5 | 21:33 `/speckit.tasks` — 51 tasks, DoD-1..8, GATE-1..8, coverage baseline frozen (first use of the new lane) | `4a1204ba`; DoD-4/GATE-5 written with 「全绿」/「exit 0」 premises over a 10-file contract-test set | **Yes** — the 10-file set already contains 2 frozen baseline failures at the same commit (`notes/baseline-failed-tests.txt` lines 4–5) → **F3** |
| 6 | 21:35 quickstart complexity literal corrected to the engine's argument domain | `2dbe566a`; disclosed as correction-level | None — in-passing repair, disclosed |
| 7 | 21:40 `/speckit.checklist` — 40-item requirements-quality checklist authored, **all rows `- [ ]`**, 11 unchecked items tagged `Gap` | `728ad4ea` | None at authoring time |
| 8 | `/speckit.analyze` — gate CRITICAL 0 / HIGH 0 (5 MEDIUM + 3 LOW); the log itself records the dead checklist lane and predicts its consumption: "checklist 停在 0/40、10 Gap 无消费，**不是 063 需求的质量缺口，而是 F2 缺陷的活实例**——本特性 FR-005..FR-008 正是修它的机制；修复落地后 analyze 将装载并处置这些 Gap。" | `/tmp/sdd-review-p1/log-p1-analyze.log` line 37 (no commit — read-only stage) | **Yes** — gate passed a spec whose own checklist accountability lane was dead, deferring to a mechanism that then never consumed it → **F1**. (Narration says "10 Gap"; mechanical count is 11 — machine count wins.) |
| 9 | 22:38 implement attempt 1 — lands US1 mechanisms + US2 review-loop edits (T018 blocked), then halts **20/51** at the C-12/T018 decision with an explicit ANOMALY line and a closed 4-option disposition set | `bd108d5a`; `/tmp/sdd-review-p1/log-p1-implement-attempt1.log` final line | Yes, external — but the stop itself is the fast-fail discipline working (§ 4) |
| 10 | 00:41 `/speckit.instructions` — user ruling path 1 executed: `REC-` carried into the live ID Register via Action 5; reports 3 pre-existing contract failures (bd108d5a sources not yet compile→regen→synced) and defers two residuals log-only | `a8c3c1f0`; `/tmp/sdd-review-p1/log-p1-instructions.log` line 25: "体量 37415 → 37443 B，超 32768 B 预算 4675 B——…需整全 reconcile 或预算再裁；(2) `## Fact, Correctness & Logic Checks` 落后模板 403 B…留给下次整全刷新" | **Yes** — residuals deferred with no durable carrier → **F7** |
| 11 | 01:04 implement attempt 2 opens — C-12 realignment per the ruling + fixed-order projection of the bd108d5a batch; **also amends `requirements.md`, `plan.md`, `quickstart.md` mid-run**; closes 053's neutrality window reactively | `68e6b43c` (touches requirements.md, plan.md, quickstart.md, tasks.md); commit message: "test_neutrality_budget c12 reconciled by closing 053's window at cb0a190a per its own contract's feature-scoped freeze…disclosed in verification.md" | **Yes** — frozen pre-implement artifacts amended by implement-stage commits with no declared amendment procedure → **F2**; reactive pin closure → **F9** |
| 12 | 01:51 US3 engine-face contract (T023–T028) | `7e738423`; tasks.md rows flip | None |
| 13 | 02:23 US4–US6 evidence/premise contracts + C-25 closure; 2026-10-15 backlog row (line 89) flipped `closed` in the same commit as the recompiled units | `cf8c882e` | None |
| 14 | 02:42 attempt 2 closes — Polish + SC/gates; DoD-4 and GATE-5 judged **void** with cited measurement (Pre-Status-Flip Gate item 6); Feature 063 flipped Implemented. Full suite 21 failed / 4089 passed; `comm -13` vs the frozen 63-name list = **0 NEW**; 42 baseline names had disappeared silently with the mandated mirror syncs | `a969e310`; tasks.md lines 20/26/34 void annotations; verification.md lines 564–567 | **Yes** — the Step-2 checklist exemption gate never fired in either attempt (→ **F1**); baseline shrink unbookkept → **F4**; `post_change_commit=pending` left stale → **F5** |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 1 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 3 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 5 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 1 |
| Command Prompt | 0 |
| Automation / Scripts | 3 |
| Workflow | 4 |
| Documentation | 1 |

One candidate was initially rated P0 and **was confirmed by independent validation** — see § 7 (0 of 1 downgraded; 062's rate was 4 of 4 downgraded).

## 3. Findings (Problems & Improvement Targets)

> Only problems, friction, and improvement targets. Each finding carries a quoted excerpt so it can be judged without opening the source.

### F1 — The implement checklist exemption gate was silently skipped in the founding feature of checklist governance; nothing in the framework can detect a skipped gate whose trigger is live

- **Severity**: P0 `(validated: confirmed by independent read-only subagent)`
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md § Step 2 — Checklist exemption gate (runtime copy: `/storage/project/cloud-native-ai/spec-kit/.specify/skills/internal/implement-feature/SKILL.md`); verified identical at both implement-time commits (728ad4ea, bd108d5a) and at HEAD
- **Evidence** (verbatim quotes):

  Owner text — `.specify/skills/internal/implement-feature/SKILL.md` § Step 2:

  ```
  - If genuinely unresolved items remain: STOP, show table, ask **"Proceed anyway? (yes/no)"**.
    > Gate probe: gate-implement-checklist-waiver — after the user decision, record firing
    > evidence per `.specify/shared/guidelines/confirmation-gates.md` §门控观察协议
    > (non-blocking).
  - If user proceeds: require a waiver recorded in `REQUIREMENTS_DIR/waivers.md` carrying
    all four parts — `Scope`, `Basis`, `Disposition`, `Closed`.
  ```

  Mechanical state at review time (HEAD a969e310), all re-derived independently by the validator:

  ```
  grep -c '^- \[ \]' .specify/specs/063-review-p1-governance/checklists/requirements-quality.md   → 40
  grep -c '^- \[x\]' …requirements-quality.md                                                     → 0
  grep '^- \[ \]' …requirements-quality.md | grep -c 'Gap'                                        → 11
  ls .specify/specs/063-review-p1-governance/checklists/                                          → requirements.md, requirements-quality.md only (no recheck-*)
  test -f .specify/specs/063-review-p1-governance/waivers.md                                      → ABSENT
  ```

  No gate-firing trace exists anywhere: `verification.md`'s only "waiver" hits describe the feature's *deliverables* (fixture drills for `test_review_p1_recheck_waiver.py` and the C-02 waiver-storage decision — `verification.md` line 150: "### C-02 — waiver storage location"), never a Step-2 event; both stage logs contain zero checklist-gate lines; `gate-implement-checklist-waiver` appears only as registration rows (probe map, contracts), never as a firing record. The timeline is unambiguous: the checklist landed 21:40 (728ad4ea) with 40 unchecked items; both implement attempts started after it; the feature was flipped Implemented at 02:42 (a969e310) with zero items answered, zero waivers, zero recheck files. The analyze stage had even predicted the consumption that never happened (§ 1 row 8, quoted in full there).

- **Why it's a problem**: A human-confirmation gate with a live trigger produced no observable event in an unattended run — the three branches (STOP+ask, proceed+waiver, all-complete) all lack a trace, so the record cannot distinguish "gate ran and passed" from "gate never executed". In an unattended dispatch there is no human to answer the STOP prompt, and the just-landed third branch's producer side (recheck files) is wired to no stage's duty, so the only unattended-legal path is one no stage owns producing. Every future unattended feature repeats this silently, and the Pre-Status-Flip Gate plus the new `gate-implement-evidence-binding` trust upstream gates ran — a trust with no detection backstop. The corruption is to the process record: a governed-looking run whose core exemption gate has never once executed, in the very feature whose subject is checklist governance.
- **Proposed fix**: two-part (REC-063-01, REC-063-02). (1) Make gate-execution evidence a mandatory per-run output: implement's wrap-up records one line per Step-2-class gate — `fired` (with probe evidence per the 门控观察协议 the owner text already cites) or `not-triggered` (with the counted trigger) — so a skipped gate becomes visible; a `not-triggered` claim whose trigger mechanically exists is a review-facing red. (2) Wire recheck producers: the analyze gate report's `dispositioned: covered-by <anchor>` markers must land as `checklists/recheck-<date>-<topic>.md` entries (the C-8 form already landed) so "genuinely unresolved" has a real unattended path.

### F2 — plan froze an unverified mechanism-owner premise; its mid-implement falsification forced a halt, a user adjudication, and mid-run amendment of frozen artifacts for which no procedure exists

- **Severity**: P1
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/research.md § D-5 (frozen at `2bcee2ac`); falsified at `bd108d5a`
- **Evidence** (verbatim quotes):

  `research.md` § D-5, the premise as frozen:

  ```
  the live `.specify/instructions.md` receives it via `scripts/bash/generate-instructions.sh` (the canonical generator; hand-editing the runtime copy is forbidden)
  ```

  The attempt-1 halt — `/tmp/sdd-review-p1/log-p1-implement-attempt1.log`, final line:

  ```
  ANOMALY: C-12/T018 要求活动 `.specify/instructions.md` 经 `generate-instructions.sh` 获得 `REC-`，但该生成器只注入缺失章节、从不变更既有章节（由 `test_instructions_section_propagation` C-2 钉住），该变更无法经指定机制落位，需在"改指 `/speckit.instructions`"与"扩展生成器并改其契约"之间裁定。
  ```

  The amendment trail: implement-stage commits touched `requirements.md`, `plan.md`, `quickstart.md` (`bd108d5a` 22:38, `68e6b43c` 01:04) and `tasks.md` four times (T023–T051 rows), realigning C-12/T018/D-T7/quickstart S5/plan mirror row plus a test rename — all after the artifacts were frozen by stages 4–5.

- **Why it's a problem**: research verified the generator's existence and the template's heading, not its propagation *behavior* — even though the additive-only behavior was already pinned by an existing contract test (`test_instructions_section_propagation`), i.e. the falsifying fact was one test-read away at plan time. The halt cost an extra stage dispatch (instructions) plus a user adjudication mid-run. Worse, the recovery required amending frozen pre-implement artifacts from an implement-stage commit, and no artifact declares who may amend what after freeze, with what in-artifact recording — the realignment lives in commit messages and the ruling lives in the session.
- **Proposed fix**: REC-063-03 — plan-stage research premises that assert engine/mechanism behavior MUST carry an executed probe (command + real output) at freeze time; a premise contradicting an existing contract test fails plan's constitution check mechanically. Plus REC-063-01's evidence regime extended: mid-run amendment of a frozen artifact requires a dated amendment note inside the artifact (or a registered ruling row), not only a commit message.

### F3 — Acceptance gates froze premises born-false: 「全绿」/「exit 0」 over a 10-file set that already contained 2 frozen baseline failures at the moment the rows were written

- **Severity**: P1
- **Category**: Automation
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/tasks.md lines 20 (DoD-4) and 34 (GATE-5); baseline `/storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/notes/baseline-failed-tests.txt` lines 4–5 — **same commit** `4a1204ba`
- **Evidence** (verbatim quote, tasks.md line 34, GATE-5):

  ```
  - GATE-5: Contract tests green — check: `python3 -m pytest tests/contract/test_clause_forms.py … exit 0。<!-- void 2026-10-20: 本 gate 的 "exit 0" 前提于 plan 冻结时即已为假——该 10 文件集合含两条冻结基线失败（`test_clause_forms.py::test_the_four_md_forms_never_co_occur_in_one_file`、`test_clause_coverage.py::test_c5_gate_budget_is_unchanged_by_the_owner_document`，`notes/baseline-failed-tests.txt` 行 4–5，2026-10-19 冻结早于本 gate 行）。…判 void 不阻塞翻转（`feature-integration.md` Pre-Status-Flip Gate 第 6 条） -->
  ```

  The two frozen baseline names above are exactly members of the 10-file set; `4a1204ba` (21:33) both wrote the GATE-5 premise and froze the baseline containing the two failures.

- **Why it's a problem**: The tasks generator's validator (`scripts/python/validate-tasks.py`) checks clause shape and green-claim form, never premise truth against the just-frozen baseline — a purely mechanical check (`do any files named in an exit-0/全绿 premise contain a baseline failure name?`) would have rejected the rows at generation time. Instead the falsity surfaced at wrap-up and consumed adjudication effort. The void handling itself was exemplary (measured re-verification `2 failed, 164 passed`, Pre-Status-Flip Gate item 6, disclosed in-line) — the process recovered correctly from a defect the tooling should have prevented.
- **Proposed fix**: REC-063-04 — extend the tasks-stage validator: every DoD/GATE premise naming a command + file set gets a premise-vs-baseline check against `notes/baseline-failed-tests.txt` in the same spec dir; a born-false premise fails generation with the offending names.

### F4 — Frozen failed-test baselines have no shrink-side bookkeeping: 42 of 63 names silently disappeared mid-run, leaving a ghost-laden gate set and unclassified failure mixture

- **Severity**: P1
- **Category**: Automation
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/verification.md lines 219, 564–567; owner of re-freeze timing: `skills/internal/create-tasks/SKILL.md` § Re-freeze timing
- **Evidence** (verbatim quotes):

  `verification.md` lines 564–567:

  ```
  → **0 NEW**. All 21 residual failures are frozen-baseline members; 42 of the 63
  baseline names disappeared with the mandated mirror syncs (pre-existing drift the
  ```

  `verification.md` line 219 (earlier checkpoint):

  ```
  (32 baseline failures disappeared with the mirror sync — disappearances are not
  ```

- **Why it's a problem**: The disappearance is good news handled honestly in prose — but nothing owns it. (a) The frozen gate set remains 63 names until some future feature re-freezes, so "zero NEW" is materially weaker than "only genuinely-known failures fail": 42 ghosts dilute the comparison. (b) Roughly two-thirds of the baseline were mirror-staleness failures, not product defects — the baseline mixed failure classes with no classification, so "63 known failures" overstated the product's red surface from day one. (c) The re-freeze owner (`create-tasks` § Re-freeze timing) declares *when* to re-capture but has no duty to diff against the previous frozen list; disappearances are narrated ad hoc per feature. No corruption: a regression in a cleared test still surfaces as NEW under `comm -13`. This is friction and signal-dilution, not silent breakage — hence P1, not P0.
- **Proposed fix**: REC-063-05 — at every re-freeze: diff both directions against the previous frozen list; each disappeared name classified (mirror-sync clearance / genuine repair / flaky) into a `baseline-cleared.txt` beside the new list; the baseline record states its validity window and predecessor pointer.

### F5 — verification.md's closure fields are hand-filled and went stale in the founding run: `post_change_commit=pending` and `implementation_date` were never closed

- **Severity**: P2
- **Category**: Template
- **Location**: /storage/project/cloud-native-ai/spec-kit/templates/verification-log-template.md (source); instance `/storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/verification.md` lines 18–20
- **Evidence** (verbatim quote, verification.md lines 18–20):

  ```
  implementation_date=2026-10-19
  post_change_commit=pending
  ```

  The run completed 02:42 on 2026-10-20 and the closing commit a969e310 exists — neither field was ever closed.

- **Why it's a problem**: The verification log's own header fields claim a completion commit that is `pending` in the final state of the final commit. A dated record that is never cited as current reality is legitimate under One Source of Truth, but a *pending* marker inside the authoritative completion record is stale-in-waiting — every reader must externally reconstruct which commit actually closed the run.
- **Proposed fix**: REC-063-06 — template marks both fields engine-fillable at the verification-log step (implementation_date = completion date; post_change_commit = the commit closing the run, written by the wrap-up's fixed-order step), or the implement skill's verification step closes them mechanically instead of leaving literals for hand-editing.

### F6 — Observed recipe-literal errors stay committed in quickstart.md: the observation record diverges from the committed artifact it observed

- **Severity**: P2
- **Category**: Documentation
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/specs/063-review-p1-governance/quickstart.md line 74 (S6)
- **Evidence** (verbatim quote, quickstart.md line 74):

  ```
  python3 .specify/scripts/python/run-determination.py --action determine --unit-id x --unit-type y        # missing ≥2 → ONE error listing all
  ```

  As written, argparse's `choices` validation rejects `y` before the engine's aggregate missing-args check runs, so the literal exercises the wrong error path — the imprecision was recorded in the implement run's notes, but the committed quickstart keeps the wrong literal. Same class: S5's clean-clone step (`git clone --quiet . /tmp/s63-clean && test -f /tmp/s63-clean/<a REC target repo-relative path>`) carries an unexpandable placeholder limitation noted in notes, unfixed in the recipe.

- **Why it's a problem**: quickstart.md is the feature's durable verification recipe; future re-runs will trip the same wrong path and, worse, learn that recipe and observation can disagree without consequence — the exact pass-claim-vs-evidence divergence this feature's own C-26..C-28 mechanisms were built to close for verification.md, surviving one artifact over.
- **Proposed fix**: REC-063-07 — the implement verification step gains a correction-class duty: a recipe literal that observation falsified is corrected in the same pass as the observation is recorded (disclosed as correction-level, the established `2dbe566a` precedent), so the committed recipe and the recorded observation never diverge.

### F7 — Stage residuals deferred log-only: the instructions byte-budget overrun recurs across runs with no durable carrier — a dead-letter pattern

- **Severity**: P2
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/memory/feedback/backlog.md line 52 (open since 2026-10-08); instance `/tmp/sdd-review-p1/log-p1-instructions.log` line 25; four identical feedback entries dated 2026-10-14/15
- **Evidence** (verbatim quotes):

  This run's instructions stage, log line 25:

  ```
  - **pending**：(1) 体量 37415 → 37443 B，超 32768 B 预算 4675 B——快照过滤后无 R1/R2 候选（…），需整全 reconcile 或预算再裁；(2) `## Fact, Correctness & Logic Checks` 落后模板 403 B（inherited-premises 条款缺失）——同类仅增量机制的遗留漂移，按部分更新范围留给下次整全刷新；
  ```

  The recurring siblings — four identical feedback entries (e.g. `.specify/memory/feedback/20261015T031340Z-speckit-plan.md` line 23):

  ```
  - instructions 尺寸 33898 B 超 32768 B 预算 1130 B，且 R1/R2 均无合法候选（…）——预算收敛机制对"项目填充型大章节"无解，需用户裁定预算值或章节拆分。
  ```

- **Why it's a problem**: The same residual class (instructions over the 32768 B budget, plus section lag) has now surfaced in at least three separate runs across two weeks, each deferring to "next full refresh" or "user ruling", with the deferral living only in that run's log or feedback store — no register row, no OI- id, no owner. A stage can complete DONE while shipping an unresolved residual nobody is obligated to pick up; the 2026-10-08 backlog row 52 (the adjacent additive-reconcile gap) shows the pattern's half-life: open, unowned, 12 days. Secondary, transient: a permission-classifier interception anomaly was recovered with a Warning-level fallback during this run (recorded in the log; no action needed).
- **Proposed fix**: REC-063-08 — stage wrap-ups land unresolved residuals as `register.md` OI- rows (or feedback-engine backlog rows) **in the same commit** as the stage's closure; a residual without a carrier cannot be part of a DONE verdict. The budget value itself gets one explicit adjudication instead of per-run re-deferral.

### F8 — REC- ids cited as load-bearing by tracked artifacts remain unregistered: the register rule is forward-only in practice

- **Severity**: P2
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/memory/register.md (0 `REC-` rows at review time); citing artifacts `plan.md` line 81, `contracts/template-mechanisms.md` lines 24/28, `tasks.md` lines 101–102
- **Evidence** (verbatim quotes):

  `contracts/template-mechanisms.md` line 24:

  ```
  This lands 061 REC-C5 at its named target (FR-006, SC-004)。
  ```

  `tasks.md` line 101 (T009):

  ```
  - [X] T009 [P] [US1] [blockedBy: T005] 实现 C-8：…（061 REC-C5 落点）。
  ```

  The ambient rule being violated — `.specify/instructions.md` § ID Register:

  ```
  Every durable identifier — a decision (D-…), open item (OI-…), stage (S…), target (T-…), finding (F-…), criterion (B-…), recommendation (`REC-…`) — MUST be recorded in `.specify/memory/register.md` **at the moment the ID is coined**, never left only in session history, a git-ignored workspace, or conversation: an unregistered ID is uninterpretable to any later session, and **citing it as known is the silent-context failure this register closes**.
  ```

  `grep -c "REC-" .specify/memory/register.md` = **0**, while this feature's plan, contracts, and tasks cite `REC-C5`/`REC-C6` as the named targets two mechanisms were built on. 061's 22 `REC-` ids are all unregistered.

- **Why it's a problem**: The ids resolve today only because the 061 report body still exists and names them — the register, the file whose purpose is making ids interpretable without opening reports, cannot interpret the very ids 063 cites as authority. The just-landed same-commit registration duty (C-11, in the review command's Handoff) covers **future** reports only; the existing rule's "anything cited by a tracked artifact … registers" clause already makes 061's cited ids violations, and no stage owns backfilling them. The forward-only seam means the register's completeness silently decays backward in time.
- **Proposed fix**: REC-063-09 — backfill register rows for all cited 061 `REC-` ids (pointer form: id → one-line meaning → `062-humanize-command/review.md` § 5 anchor → status) in the same shape the new duty prescribes; the review-command Handoff row gains a backfill line so each review also registers its predecessors' cited-but-unregistered ids.

### F9 — Cross-feature state pins are amended reactively: open-ended windows redden later features' legitimate edits, and closure rules are invented per incident instead of declared at authoring

- **Severity**: P2
- **Category**: Automation
- **Location**: /storage/project/cloud-native-ai/spec-kit/tests/contract/test_neutrality_budget.py (053's pin, amended by 063 at `68e6b43c`); same pattern: `tests/contract/test_probe_engine_action_sets.py` (056's closed set, amended by 063 C-22)
- **Evidence** (verbatim quotes):

  `test_neutrality_budget.py`, the 063 amendment note:

  ```
  # 2026-10-20 amendment (Feature 063): C-12's freeze is scoped by its own contract to
  # 053's window ("在本特性窗口内逐字不变"), so the window CLOSES at 053's last commit —
  # the original open-ended ``BASE_SHA..HEAD`` form over-reached the clause it pins and
  # reddens on any later feature that legitimately edits the state machine
  ```

  The test's own comment quotes the recurring lesson: "an unanchored window is how 052's GATE-3 went void." The 056 action-set test docstring: "Amended by Feature 063 (C-22, 2026-10-20): … The manifest action joins the engine action closed set; the owner contract (056 contracts/engine-action-sets.md) is updated in the same change."

- **Why it's a problem**: Each amendment is well-documented *after the fact* (dated in-test notes, owning-contract citation, verification.md disclosure — good practice worth keeping), but nothing requires a pin to declare its closure rule **at authoring time**. The consequence is deterministic: an open-ended pin redden's the next feature's legitimate edit, the amendment is invented ad hoc under time pressure, and the same lesson has now re-derived itself across at least three features (052's GATE-3, this amendment, the C-7 precedent the test cites). Combined with F7's carrierless residuals, cross-feature state is maintained by incident response rather than convention.
- **Proposed fix**: REC-063-10 — pin-authoring rule in the tasks/plan owners: a feature-scoped state pin MUST declare, where it is authored, either a closed window or the rule that closes it; amendments to another feature's pin additionally register a dated row (REC-063-08's carrier), so the amendment trail is queryable rather than archaeology.

## 4. What Worked — Preserve (Brief)

- Attempt-1's fast-fail at the C-12 decision point: explicit ANOMALY line, closed 4-option disposition set, 20/51 tasks preserved (`bd108d5a`) — the discipline worked exactly as written.
- Void-with-measurement adjudication: DoD-4/GATE-5's born-false premises judged void with re-measurement (`2 failed, 164 passed`), anchored to Pre-Status-Flip Gate item 6, never silently regraded.
- The frozen 63-name baseline was never relaxed: `comm -13` zero-NEW held through two projection batches and a mirror sync that cleared 42 ghost names.
- 062's governed artifacts untouched throughout — verification.md records git-diff-empty at every checkpoint (FR-029).
- Red-first evidence per red run; contract tests updated alongside the mechanism they pin; 34 green claims with mutation drills.
- The C-12 realignment named every edited file (D-T7 ledger) and renamed the test to match the new owner.
- The review command's Handoff now owns same-commit `REC-` registration (C-11) — this report is the first run under it (§ 5, REC-063-01..10 registered in the same commit).

## 5. spec-kit / SDD Improvement Recommendations

> Grouped by target subsystem. Each names the exact file to change and its source finding(s).

### 5.1 Template Improvements

- **REC-063-06 Engine-fill the verification log's closure fields** — Target: `templates/verification-log-template.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/templates/verification-log-template.md`). Change: mark `implementation_date` and `post_change_commit` as engine-filled at the verification-log step (completion date; closing commit sha) and forbid hand-authored `pending` values from surviving wrap-up. Source: F5. Expected impact: the completion record never ships a stale `pending`; downstream readers resolve the closing commit without archaeology.

### 5.2 Command Prompt Improvements

- **REC-063-01 Mandatory gate-execution evidence on implement's face** — Target: `templates/commands/implement.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/templates/commands/implement.md`), mirrored into the skill at `skills/internal/implement-feature/SKILL.md` § Step 2. Change: each implement run records one evidence line per stop-gate — `fired` (with 门控观察协议 probe evidence) or `not-triggered` (with the counted trigger); a `not-triggered` claim whose trigger mechanically exists is a review-facing red; mid-run amendment of frozen pre-implement artifacts requires a dated in-artifact amendment note. Source: F1, F2. Expected impact: a skipped gate becomes visible instead of silent; the process record becomes falsifiable.

### 5.3 Automation / Script Improvements

- **REC-063-04 Premise-vs-baseline check in the tasks validator** — Target: `scripts/python/validate-tasks.py` (absolute: `/storage/project/cloud-native-ai/spec-kit/scripts/python/validate-tasks.py`). Change: for every DoD/GATE premise naming a command + file set, mechanically check the named files against the spec dir's frozen `notes/baseline-failed-tests.txt`; a premise a frozen baseline already falsifies fails generation with the offending names. Source: F3. Expected impact: born-false acceptance premises die at generation time, not at wrap-up adjudication.
- **REC-063-05 Baseline shrink-side bookkeeping at re-freeze** — Target: `skills/internal/create-tasks/SKILL.md` § Re-freeze timing (absolute: `/storage/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md`), plus a `comm`-based diff step in the freeze procedure. Change: every re-freeze diffs both directions against the previous frozen list; disappeared names are classified (mirror-sync clearance / genuine repair / flaky) into `baseline-cleared.txt`; the baseline record states its validity window and predecessor. Source: F4. Expected impact: gate sets stay ghost-free; failure classes stay separated; "zero NEW" regains its meaning.
- **REC-063-10 Closed-window rule for cross-feature state pins** — Target: `skills/internal/create-tasks/SKILL.md` § Runtime-evidence landing points (absolute: `/storage/project/cloud-native-ai/spec-kit/skills/internal/create-tasks/SKILL.md`). Change: a feature-scoped state pin (window pin, closed set, byte budget) MUST declare its closure rule at authoring; amending another feature's pin registers a dated row per REC-063-08's carrier. Source: F9. Expected impact: legitimate later-feature edits stop reddening ancestor pins; amendments become queryable convention instead of incident archaeology.

### 5.4 Workflow Improvements

- **REC-063-02 Wire recheck-file producers** — Target: `skills/internal/analyze-artifacts/SKILL.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/skills/internal/analyze-artifacts/SKILL.md`) + `skills/internal/create-checklist/SKILL.md` § 5. Change: analyze's `dispositioned: covered-by <anchor>` markers and downstream answers land as `checklists/recheck-<date>-<topic>.md` entries (the C-8 append-only form already landed); each answered entry quotes the requirement line. Source: F1. Expected impact: the Step-2 third branch becomes reachable in unattended runs — the gate's legal proceed path has an owner.
- **REC-063-03 Execution-verified plan premises** — Target: `skills/internal/create-plan/SKILL.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/skills/internal/create-plan/SKILL.md`), Phase 0 research rules. Change: a research decision that asserts engine/mechanism behavior MUST carry an executed probe (command + real output) at freeze time; a premise contradicting an existing contract test fails plan's constitution check. Source: F2. Expected impact: mechanism-owner premises stop being falsified mid-implement; halts like this run's become avoidable at plan time.
- **REC-063-07 Correct falsified recipe literals at observation time** — Target: `skills/internal/implement-feature/SKILL.md` verification-log step (absolute: `/storage/project/cloud-native-ai/spec-kit/skills/internal/implement-feature/SKILL.md`). Change: a quickstart/recipe literal that observation falsified is corrected in the same pass as the observation is recorded (correction-class, disclosed). Source: F6. Expected impact: the committed recipe and the recorded observation never diverge; future re-runs exercise the real path.
- **REC-063-08 Durable carriers for stage residuals** — Target: `skills/internal/manage-instructions/SKILL.md` Action 5 (absolute: `/storage/project/cloud-native-ai/spec-kit/skills/internal/manage-instructions/SKILL.md`) + the wrap-up residual convention in `.specify/shared/workflow/feedback-step.md`. Change: unresolved stage residuals (budget overruns, section lag) land as `register.md` OI- rows or feedback-engine backlog rows in the same commit as stage closure; a DONE verdict with an uncarried residual is non-compliant; the 32768 B budget value gets one explicit adjudication. Source: F7, F9. Expected impact: residuals stop dying in run logs; the recurring budget overrun gets a decision instead of per-run re-deferral.
- **REC-063-09 Backfill cited REC- registrations** — Target: `.specify/memory/register.md` (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/memory/register.md`) + `templates/commands/review.md` Handoff (absolute: `/storage/project/cloud-native-ai/spec-kit/templates/commands/review.md`). Change: backfill pointer rows for all cited 061 `REC-` ids; the Handoff gains a line so each review also registers its predecessors' cited-but-unregistered ids. Source: F8. Expected impact: the ID Register becomes backward-complete; cited ids resolve from the register, not from report archaeology.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | REC-063-01 gate-execution evidence; REC-063-02 recheck producers | `templates/commands/implement.md`, `skills/internal/implement-feature/SKILL.md`, `skills/internal/analyze-artifacts/SKILL.md` | F1 |
| P1 | REC-063-03 executed plan premises | `skills/internal/create-plan/SKILL.md` | F2 |
| P1 | REC-063-04 premise-vs-baseline check | `scripts/python/validate-tasks.py` | F3 |
| P1 | REC-063-05 shrink-side baseline bookkeeping | `skills/internal/create-tasks/SKILL.md` | F4 |
| P2 | REC-063-06 engine-filled closure fields | `templates/verification-log-template.md` | F5 |
| P2 | REC-063-07 fix falsified recipe literals | `skills/internal/implement-feature/SKILL.md` | F6 |
| P2 | REC-063-08 durable residual carriers | `skills/internal/manage-instructions/SKILL.md`, `shared/workflow/feedback-step.md` | F7, F9 |
| P2 | REC-063-09 backfill REC- registrations | `.specify/memory/register.md`, `templates/commands/review.md` | F8 |
| P2 | REC-063-10 closed-window pin rule | `skills/internal/create-tasks/SKILL.md` | F9 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason. (No `external` targets — all ten resolve in-repo.)
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: **one P0 finding (F1) was raised and confirmed**. It was validated by a fresh-context, read-only subagent that received only the finding and the re-derivation commands — never the reviewer's reasoning or sibling findings (gate rule 5 disjointness); all mechanical counts matched exactly (40/0/11/0/ABSENT), the counter-evidence sweep across verification.md, tasks.md, features/063.md, both stage logs, and the checklist itself found no gate-firing record, and the verdict was **CONFIRM P0** (0 of 1 downgraded). The same-author objective-analysis gate did not fire (all artifacts authored by nine prior stage dispatches), but the P0 validation wave was run unconditionally regardless.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.

---

## Registration Note

Per the review command's Handoff (C-11, landed): `REC-063-01` … `REC-063-10` are registered in `.specify/memory/register.md` **in the same commit** as this report, pointer form (id → one-line meaning → this file § 5 anchor → status `open`).
