# Specification-Driven Development (SDD) Process Review Report: 客户项目的持续反馈与自我提升（Client-Project Feedback & Self-Improvement）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 072 |
| Requirement Key | 072-client-self-improvement |
| Requirement Name | 客户项目的持续反馈与自我提升（Client-Project Feedback & Self-Improvement） |
| Related Feature | 072 客户项目的持续反馈与自我提升（Client-Project Feedback & Self-Improvement） |
| Repository | spec-kit |
| Repository URL | `(no single resolving remote)` — remotes: `origin`=github/spec-kit (upstream fork), `github`/`gitee`/`gitlab`=cloud-native-ai/spec-kit |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty (HEAD unpushed on every remote) — cite absolute paths + `git show <sha>:<path>` instead of URLs |
| Branch | master |
| Commit SHA | `5336c0574ab6de641cc7a99e31c005d91eaeecec` (short: `5336c057`) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit |
| Review Date | 2026-10-27 |
| Reviewer (Agent) | SDD Executor — unattended review-stage dispatch (fresh isolated execution; artifacts under review were produced by prior stage dispatches, so the same-author gate's delegation condition does not bind this run; P0 independent validation had zero findings to validate — see §7) |
| Environment | linux; bash 4.4.20; git 2.43.5; python 3.11.11; pytest 8.4.2 |
| spec-kit Source Snapshot | self-hosting repository — the reviewed templates/skills/scripts are this tree itself @ `5336c057` |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 316 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/072-client-self-improvement/requirements.md | 29 FR / 7 SC / 6 user stories / 10 Shared Strings; Q1–Q10 + 5 clarify adjudications |
| plan.md | 151 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/072-client-self-improvement/plan.md | Technical approach, constitution check (16 Pass), mirror obligations, design-artifact summary |
| tasks.md | 365 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/072-client-self-improvement/tasks.md | 29 tasks T001–T029, Tests Mode ON, 62 clauses claimed, 7 completion gates |
| research.md | 69 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/072-client-self-improvement/research.md | R1–R12 rulings with measured evidence and rejected alternatives |
| data-model.md | 162 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/072-client-self-improvement/data-model.md | E1–E10 entities, V1–V33 validation rules, 2 state transitions |
| contracts/ | 6 files | /storage/project/cloud-native-ai/spec-kit/.specify/specs/072-client-self-improvement/contracts/ | C-1…C-62, all `md-bold-closed` |
| quickstart.md | 97 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/072-client-self-improvement/quickstart.md | S1–S8 scenarios (S1–S2 live at plan time; S3–S8 executed at T028) |
| feature-ref.md | 76 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/072-client-self-improvement/feature-ref.md | Binding, delivery surface, FR/SC coverage, 7 disclosed rulings |
| verification.md | 110 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/072-client-self-improvement/verification.md | SC-001…SC-007 status rows + evidence bindings |
| checklists/ | 2 files | /storage/project/cloud-native-ai/spec-kit/.specify/specs/072-client-self-improvement/checklists/ | requirements quality checklist + client-feedback-loop checklist |
| notes/ | 4 files | /storage/project/cloud-native-ai/spec-kit/.specify/specs/072-client-self-improvement/notes/ | red-first evidence, pre-change measurements, C-61 plan, quickstart S3–S8 run log |
| test-evidence/ | 26 files | /storage/project/cloud-native-ai/spec-kit/.specify/specs/072-client-self-improvement/test-evidence/ | per-stage gate outputs, targeted-run captures, mirror checks |

## 1. Process Execution Timeline

Reconstructed from `git log --oneline 8ab5e5a9..5336c057` (16 commits) plus the stage evidence files. The chain followed the prescribed requirements → clarify → plan → tasks → checklist → analyze → implement → review flow with the deviations annotated below; all deviations except the two requirements-stage ones (rows 1–2) were discovered from commit traces and evidence files, not assumed.

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements landed, Feature 072 bound | `ff0b31e2` | Yes — binding moved from clarify to requirements (brief-directed; recorded as Assumption A2 in requirements.md) |
| 2 | spec created on `master`, branch switch suppressed | requirements.md A1 | Yes — scaffold branch action suppressed by unattended stage rule; recorded |
| 3 | clarify: 5 adjudications bound back into requirements | `7a222205`, `fc3fa67d` | None |
| 4 | plan + constitution check (16 Pass, same-author fallback disclosed) | `6dca65a5`, plan.md § Constitution Check | None (fallback disclosed per gate) |
| 5 | tasks (29 rows, red-first plan, 62 clauses claimed) | `e39afe8c` | None |
| 6 | checklist + analyze; analyze report landed, feature held at Planned | `7d225480`, `fe089338`, test-evidence/analyze-report.md | None |
| 7 | implement part 1: evidence slots + E2 failed-name baseline (26 names) | `b5a20115`, baseline-failed.txt | None |
| 8 | **(a) disclosure — pre-existing engine defect found & fixed in passing**: probe registry non-entity catalog reachability only recognized the framework-source face, guaranteeing `probe-inject` failure in real client layouts (C-58 blind branch) | `ac98d354` (fix), notes/pre-change-measurements.md §8, tests/contract/test_probe_nonentity_catalog.py (+50 incl. negative test `test_catalog_unreachable_when_both_faces_missing`) | Correction-class repair under Fast Fail; disclosed, not a deviation. Review verdict: **accepted** — two-face doctrine matches `_engine_script`, negative test guards both-missing; targeted suite re-verified green this run |
| 9 | US1–US6 + Polish landed across 7 story commits | `5db467dd`…`f9236052` | None — story-grouped commits, per-task traces in test-evidence/implement-stage-status.jsonl |
| 10 | part 7 guard sweep found 4 neutrality violations written by the feature itself on distribution faces; neutralized + mirrors re-synced (C-57) | `64afd34d`, test-evidence/part7-us6-guard-sweep.txt | Correction-class; disclosed in features/072.md |
| 11 | **(c) disclosure — C-61 compatibility plan**: two frozen 071/069-era assertions collided with 072's plan-authorized edit surface; resolved via written plan + non-precedential declaration | notes/compatibility-plan-c61.md, `64afd34d` | Handled by the contract's own escape clause; review verdict: **accepted as one-off, non-precedential** — and its root cause is filed here as F1 |
| 12 | **(e) disclosure — quickstart S3–S8 executed for real** in six one-shot client fixtures (armed capture chain, idempotent re-capture, three named unarmed disclosures hit for real, package `excluded_external=1`, fail-closed run-determination `persisted=false` with zero tree change) | notes/quickstart-run.md (737 lines), `f9236052` T028 | None — plan-owned quickstart.md deliberately not rewritten (no PLAN-EDIT; assumption recorded in the note's header). No partial outstanding |
| 13 | **(b) disclosure — part 8b post-close correction**: C-56 guard whitelist covered only `.specify/skills/internal/`, omitting other generator-produced skill mirrors; surfaced when the lawful loop-playbook sync landed | `5336c057`, test-evidence/part8b-guard-sweep-correction.txt | Correction-class post-close fix; review verdict: **accepted** — root cause filed here as F2 |
| 14 | **(d) disclosure — two failing tests attributed**: `test_shipped_surface_client_neutrality` / `test_neutrality_budget` (T029: 588 passed / 2 failed) | baseline-failed.txt lines 11+15; part8-final-targeted-run.txt | Pre-existing debt (064/066/067/070 era, recorded in features/072.md part-7 entry); review-stage re-run of the six new suites + adjacent guards: 112 tests, all green — attribution confirmed, **not this feature's defect, out of scope here** |
| 15 | review (this run): process segment + code segment (triage `run`, base `8ab5e5a9` feature-first-commit, head `5336c057`) | code-review.md, review.md | None |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 1 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 3 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 1 |
| Command Prompt | 0 |
| Automation / Scripts | 2 |
| Workflow | 1 |
| Documentation | 0 |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `8ab5e5a97090ce76b39ec87aeeb788f3170ed9e3` (`8ab5e5a9`) | the resolved diff base (`base --spec` tier `feature-first-commit`; the receipt was pinned with explicit `--since/--head` to avoid the script's `GIT_BASE` default drift) |
| Head commit | `5336c0574ab6de641cc7a99e31c005d91eaeecec` (`5336c057`) | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the resolution tier the code segment's `base` step reported |
| Renderer mode | `renderer: text` | the code record's header marker (non-interactive run; the two-condition rule selects text without a TTY) |
| Changed / judged / skipped / gap files | 111 / 28 / 83 / 0 | copied field by field from the coverage receipt block |
| Segment verdict | `not-evaluated` | one of the four closed values the `code-review` skill owns |
| Gate verdict | `allow` (exit 0 — 0 `blocking`, 0 `important`, 1 `suggestion` / 1 `question` / 1 `praise`) | the merge-gate verdict source; the refusing literal `blocking-unresolved` was not produced |
| Reason, when one applies | `skipped_files` = 83 > 0, so the segment verdict MUST NOT be `pass` (coverage-receipt C-37): the 83 are the delta's spec artifacts, memory records, and generator-produced mirrors, each carrying a legal reason (`non-code-file` / `generated`); a legal skip earns no coverage credit | mandatory reason for a `not-evaluated` result |
| Uncommitted scope | none — the run's own record file is excluded from the uncommitted-scope check by design (`uncommitted_scope()` filters `code-review*.md`), and every other path was clean at receipt time; no conclusion was issued over uncommitted scope | disclosed, never concluded over; the same sentence lives in `/storage/project/cloud-native-ai/spec-kit/.specify/specs/072-client-self-improvement/code-review.md` |
| Record | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/072-client-self-improvement/code-review.md` | written because the triage value was `run` |
| Archive | `none` | this run's archive path; `none` on a first run |

Client capture (the code segment's fifth step) ran and answered with the framework-hat skip line — `capture: skipped hat=framework basis=root owns framework source directories …` — naming the hat verdict as its basis, not one of the five closed tokens, zero entries, exit 0. This is the designed behavior for a framework-hat repository; the client-hat capture path itself was exercised for real at T028 (timeline row 12).

This subsection carries the verdict and the pointers only: no opinion body, no per-severity item count. The findings themselves live in the record and are read there.

## 3. Findings (Problems & Improvement Targets)

### F1 — Frozen guard assertions have no declared channel for plan-authorized drift; every lawful edit pays an ad-hoc compatibility plan

- **Severity**: P1
- **Category**: Automation
- **Location**: `tests/contract/test_dogfooding_practice.py` (FEEDBACK_ENGINE_ACTIONS pin); `tests/contract/test_expression_compatibility.py` (ALLOWED_POST_BASELINE_CHANGES frozen hashes); absolute: /storage/project/cloud-native-ai/spec-kit/tests/contract/test_expression_compatibility.py
- **Evidence** (verbatim quote, from `notes/compatibility-plan-c61.md`):

  > 守护网定向运行首次覆盖 `test_dogfooding_practice::test_c4_engine_action_set_unchanged` 与 `test_expression_compatibility::test_c5_non_wiring_files_keep_their_frozen_hashes`，发现两条 071/069 时代冻结断言与 072 计划授权编辑面（C-56/C-62）正面冲突

  and the after-the-fact amendment it required (from `test_expression_compatibility.py`):

  > Compatibility plan + non-precedential declaration: .specify/specs/072-client-self-improvement/notes/compatibility-plan-c61.md and .specify/memory/features/072.md. Each drift is pinned by a Feature 072 contract suite, cited per entry; this records the drift, it does not authorize any other.

- **Why it's a problem**: The pins are one-directional tripwires with no machine-readable way to declare drift *before* it happens. A feature whose plan lawfully authorizes editing a pinned surface discovers the collision only at guard-run time, then must hand-author a compatibility plan and amend the pin — 072 paid this cost twice in one implement. The escape hatch is prompt-level ("不为例外先例"), not mechanical, so nothing stops a third feature from citing C-61 as precedent.
- **Proposed fix**: Add a declared-drift registry (one file, e.g. `tests/contract/declared-drift.md` or a frontmatter block the two guards read): a plan may append a row naming `{guard, file, markers, plan-path, feature}` in the *same batch* as its edits, and the guards accept exactly the declared rows while failing on anything undeclared. The compatibility plan becomes the workflow narrative around a mechanical channel, not a substitute for one.

### F2 — C-56's mirror whitelist hardcoded one generator subtree instead of the generator's own pair list; surfaced as a post-close commit

- **Severity**: P2
- **Category**: Automation
- **Location**: `tests/contract/test_client_guard_sweep.py` (C-56 edit-surface whitelist); absolute: /storage/project/cloud-native-ai/spec-kit/tests/contract/test_client_guard_sweep.py
- **Evidence** (verbatim quote, from commit `5336c057`'s message):

  > `test_c56_changed_paths_stay_on_the_declared_edit_surface` whitelisted only `.specify/skills/internal/`, omitting the other skill mirrors produced by the same sync-mirrors.py generator; part 8's lawful --write of the pre-existing loop-playbook.md drift made the regenerated mirror an offender.

- **Why it's a problem**: The guard enumerates *some* of the paths `sync-mirrors.py` produces, so a lawful generator run can manufacture a violation the guard was supposed to police — discovered only after the mirror write landed, costing a separate 8b commit. The enumeration and the generator's truth source (`MIRROR_PAIRS`) are two lists that drift.
- **Proposed fix**: Derive the mirror half of the C-56 whitelist from `scripts/python/sync-mirrors.py`'s MIRROR_PAIRS at test time (import or subprocess), keeping only the non-mirror declarations literal. One list, owned by the generator.

### F3 — The feedback command template's Path A bullet grew from pointer shape into content shape, triplicating the carrier closure

- **Severity**: P2
- **Category**: Template
- **Location**: `templates/commands/feedback.md` (Path A delegation bullet); absolute: /storage/project/cloud-native-ai/spec-kit/templates/commands/feedback.md
- **Evidence** (verbatim quote, the current bullet):

  > A4 对账与渠道路由(含 backlog 写入;客户条目载体指派闭集恰三——todo Park 默认 / 新需求规格 / 改进循环主体,一条目一载体、无第四载体,undecided 呈报留待下次消化、不静默丢弃;消化呈报三项事实:本次帽子与武装态(armed state)及解析方式、两侧条目数与处置、四条循环度量读数指针……)

  The same facts already live in `skills/internal/manage-feedback/references/path-a-digest.md` § A4a/A4b (the owner) and `docs/reference/commands/feedback.md` (the reader surface).
- **Why it's a problem**: The one-source-of-truth discipline allows repetition in pointer shape only; this bullet now restates the carrier closure and the three report facts in content shape on a third surface. The next carrier/metrics wording change must be hand-synced across three files, and the template is the one no test pins word-for-word.
- **Proposed fix**: Trim the template bullet back to a pointer ("A4 additionally assigns each digested client entry exactly one carrier from a closed set of three and reports the digest facts — see `references/path-a-digest.md` § A4a/A4b"), leaving the enumeration to the owner document.

### F4 — Plan-constraint freeze left the requirements header status stale through implement and review

- **Severity**: P2
- **Category**: Workflow
- **Location**: `.specify/specs/072-client-self-improvement/requirements.md` line 5 vs `tasks.md` DoD-6; absolute: /storage/project/cloud-native-ai/spec-kit/.specify/specs/072-client-self-improvement/requirements.md
- **Evidence** (verbatim quotes):

  > `**Status**: Draft` (requirements.md line 5, as of HEAD `5336c057`)

  > DoD-6: plan 约束激活期间,任何 plan 属主制品(plan.md / requirements.md / …)不得重写 (tasks.md)

- **Why it's a problem**: With the plan constraint active, implement lawfully could not touch plan-owned files — so the spec header still says `Draft` while the feature detail and registry say `Implemented`. No machine reader consults the header, but a human opening the spec is misled, and every future plan-constrained feature inherits the stale header.
- **Proposed fix**: Add one reconciliation line to the review (or implement close-out) stage protocol: a header-status reconcile of plan-owned spec files is permitted during plan constraint (it is bookkeeping, not a plan rewrite), or the scaffold/template drops the per-file status header in favor of the registry as the only status surface.

## 4. What Worked — Preserve (Brief)

- Story-grouped implement commits with per-task evidence slots (`test-evidence/implement-stage-status.jsonl`) made this review's timeline reconstruction a `git log` read, not an archaeology dig.
- Red-first four-field records (`notes/red-first-evidence.md`) plus the frozen T002 failed-name baseline turned "no new failures" into a mechanical `comm` comparison instead of an impression.
- The two-hat fixture (`tests/fixtures/client_project.py`) — bidirectionally drivable hat predicate, refuses to build inside the framework tree, engine facts only from machine-readable probe output — is the honest-verification shape FR-029 demanded; later client-facing features should copy it, not reinvent it.
- In-run corrections (probe catalog two-face fix, C-57 self-neutrality sweep, C-61 plan) were disclosed at the site and in the feature detail as they happened — the fast-fail discipline worked as designed.
- Guard sweeps that count assertions (`def test_` regex, action-set pins both directions) caught real violations the feature itself introduced (rows 10–11, 13) before any human read the faces.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **Trim the feedback template's Path A bullet to pointer shape** — Target: `templates/commands/feedback.md` (absolute supplement: /storage/project/cloud-native-ai/spec-kit/templates/commands/feedback.md). Change: replace the inlined carrier closure and report-facts enumeration with a one-line pointer to `references/path-a-digest.md` § A4a/A4b. Source: F3. Expected impact: the carrier closure has one content owner again.

### 5.2 Command Prompt Improvements

- **Declared-drift channel for frozen guard pins** — Target: `templates/commands/plan.md` (absolute supplement: /storage/project/cloud-native-ai/spec-kit/templates/commands/plan.md). Change: document that a plan authorizing edits to a pinned surface MUST append a declared-drift row (guard name, file, markers, plan path) in the same batch, pointing at the registry file F1 introduces. Source: F1. Expected impact: compatibility plans stop being one-off escape hatches and become workflow narratives around a mechanical check.

### 5.3 Automation / Script Improvements

- **Mechanical declared-drift registry read by the frozen guards** — Target: `tests/contract/test_expression_compatibility.py` and `tests/contract/test_dogfooding_practice.py` (absolute supplements under /storage/project/cloud-native-ai/spec-kit/tests/contract/). Change: introduce the registry file and make both guards accept exactly declared rows while still failing on undeclared drift; the existing ALLOWED_POST_BASELINE_CHANGES mechanism migrates into it. Source: F1. Expected impact: lawful plan-authorized drift lands in one commit with zero red intermediary.
- **Derive C-56's mirror whitelist from sync-mirrors MIRROR_PAIRS** — Target: `tests/contract/test_client_guard_sweep.py` (absolute supplement: /storage/project/cloud-native-ai/spec-kit/tests/contract/test_client_guard_sweep.py). Change: compute the `.specify/skills/`+`.specify/shared/` portion of the edit-surface whitelist from `scripts/python/sync-mirrors.py` MIRROR_PAIRS at test time. Source: F2. Expected impact: lawful generator writes can no longer manufacture guard violations.

### 5.4 Workflow Improvements

- **Spec-header status reconcile under plan constraint** — Target: `templates/commands/implement.md` close-out (or `templates/commands/review.md` close-out) (absolute supplements under /storage/project/cloud-native-ai/spec-kit/templates/commands/). Change: one bookkeeping line reconciling the spec header status of plan-owned files (or retiring the header field to the registry). Source: F4. Expected impact: no more permanently-`Draft` headers on Implemented features.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Declared-drift channel for frozen guard pins (mechanical registry + plan-template rule) | `tests/contract/` + `templates/commands/plan.md` | F1 |
| P2 | Derive C-56 mirror whitelist from MIRROR_PAIRS | `tests/contract/test_client_guard_sweep.py` | F2 |
| P2 | Trim feedback template Path A bullet to pointer shape | `templates/commands/feedback.md` | F3 |
| P2 | Spec-header status reconcile under plan constraint | `templates/commands/implement.md` / `review.md` close-out | F4 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
