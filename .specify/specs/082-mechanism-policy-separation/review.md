# Specification-Driven Development (SDD) Process Review Report: 082-mechanism-policy-separation

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 082 |
| Requirement Key | 082-mechanism-policy-separation |
| Requirement Name | 元技能治理：机制/策略分离与技能引用归一化（Meta-Skill Governance: Mechanism–Policy Separation & Skill Reference Grammar） |
| Related Feature | 082 (the spec is the bound Feature's only spec) |
| Repository | spec-kit |
| Repository URL | `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git` (SSH-only remote; no HTTPS web form is configured) |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains 875be2c7` is empty, so the commit is unpushed. Cite absolute paths plus `git show 875be2c7:<path>` recovery instructions instead of URLs. |
| Branch | 082-mechanism-policy-separation |
| Commit SHA | 875be2c7f73679a0d1ec108afed1df4e32c8a766 (short: 875be2c7) — the review object's head; the review records commit follows it |
| Repo Root (absolute) | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-11-05 |
| Reviewer (Agent) | Qoder unattended review agent (four segments + Acceptance Reality Check) |
| Environment | macOS 25.6.0 / arm64; bash; Python 3.14.6; pytest 9.2.0; git 2.54.0 (Apple Git-157); Qoder CLI 1.1.83 recorded by SC-002 / SC-004 evidence |
| spec-kit Source Snapshot | this repository at 875be2c7 (self-hosted; the reviewed templates/commands/scripts are its own) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 318 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/082-mechanism-policy-separation/requirements.md` | 30 FR / 9 SC / 11 assumptions / C1–C11; SC paths final×8 + supporting×1 |
| plan.md | 527 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/082-mechanism-policy-separation/plan.md` | D1–D14, T-001…T-004, project structure, scope-update record |
| tasks.md | 331 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/082-mechanism-policy-separation/tasks.md` | 52 dependency-ordered rows, all `[x]` |
| contracts/skill-reference.contract.md | 148 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/082-mechanism-policy-separation/contracts/skill-reference.contract.md` | GR-01…GR-10 + SR-01…SR-06 |
| contracts/guard-and-measurement.contract.md | 172 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/082-mechanism-policy-separation/contracts/guard-and-measurement.contract.md` | GM-01…GM-14 measurement/guard clauses |
| contracts/owner-document.contract.md | 101 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/082-mechanism-policy-separation/contracts/owner-document.contract.md` | OD-01…OD-10 owner-document shape |
| contracts/skill-wiring.contract.md | 81 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/082-mechanism-policy-separation/contracts/skill-wiring.contract.md` | SW-01…SW-08 meta-skill wiring |
| data-model.md | 307 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/082-mechanism-policy-separation/data-model.md` | 10 entities / 34 validation rules / GM-03 allowed set |
| quickstart.md | 282 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/082-mechanism-policy-separation/quickstart.md` | 14 scenarios S1–S14 with run/deferred markers |
| verification.md | 229 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/082-mechanism-policy-separation/verification.md` | SC-001…SC-009 status rows, smoke record, GATE-1…GATE-8 |
| research.md | 216 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/082-mechanism-policy-separation/research.md` | R1–R15 measured readings |
| feature-ref.md | 49 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/082-mechanism-policy-separation/feature-ref.md` | Feature binding + delivery surface |
| checklists/requirements.md | 89 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/082-mechanism-policy-separation/checklists/requirements.md` | requirements-quality checklist |
| checklists/quality-scope-update.md | 153 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/082-mechanism-policy-separation/checklists/quality-scope-update.md` | scope-update checklist |
| test-evidence/ | 80 files | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/082-mechanism-policy-separation/test-evidence/` | stage status, SC readings, final gates, review re-runs |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | `/speckit.requirements` creates the spec and binds Feature 082 | `88f8da14`; `.specify/memory/features.md` row 082 | no |
| 2 | `/speckit.clarify` Mode A, zero questions, A1–A10 ratified | `aaee504c`; `test-evidence/clarify-gates.txt` | Mode A differs from an interactive clarify, by the dispatch |
| 3 | Scope update: the concurrent skill-reference implementation is folded in as capability two | `518466db`, `00641764`; `requirements.md` § Assumptions A11 | scope change mid-feature; ratified by the user |
| 4 | `/speckit.plan` + research, data-model, 4 contracts, quickstart | `58d3dc5b`, `d20ed616`; `plan.md` § Scope Update Record | no |
| 5 | `/speckit.tasks`; 52 rows; `validate-tasks.py` PASS | `5e60c629`; `tasks.md` | no |
| 6 | Checklist + `/speckit.analyze` repair round | `32389f88`, `974db180` | analyze findings repaired before implement |
| 7 | Baseline capture at implement start (E2 full suite 7157P / 24F / 7S) | `bfc18fe5`; `test-evidence/implement-part1-baseline.txt` | the baseline tree already carried the uncommitted concurrent implementation; two coaching tests were red for the *concurrent* rename |
| 8 | Implement Parts 1–7 | `59ca4d36` … `6785e8de` | task-grouped commits; good traceability |
| 9 | Concurrent work lines are absorbed into the same branch and range | `62d1ab5d` (ssh-utils), `1acb97c1` (framework calibration) | the range carries 24 paths with no 082 commit; disclosed, not attributed to 082 |
| 10 | SC-006 / SC-009 measured against a matrix authored from the implementation | `test-evidence/sc-006-2026-11-05.txt`, `sc-009-2026-11-05.txt` | matrix expectation contradicted the owner's rule (c); see F1 |
| 11 | Implement closes `Planned → Implemented` | `6785e8de`; `verification.md` § Feature-level statement | four conditions held on the recorded readings |
| 12 | Review dispatched; process, artifact, implementation, code segments run | this report; `code-review.md` | review found and repaired two P1 code/test defects before the flip |
| 13 | In-review repairs committed | `875be2c7` | mirror collapse, coaching parameter restore, SW-05 carrier, GM-03 text/name |
| 14 | Smoke and targeted set re-run after repairs | `test-evidence/review-smoke-and-targeted.txt` (102 passed, exit 0) | count grew by two tests (SW-05 carrier) |
| 15 | Acceptance Reality Check | `closure-acceptance-check.py --spec-dir .specify/specs/082-mechanism-policy-separation --json` → verdict `accept`, pass 8 / total 8 | agree with the claim |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 4 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 6 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 0 |
| Automation / Scripts | 2 |
| Workflow | 4 |
| Documentation | 4 |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `3ffeb26e4880f134f7a5e220ecbffb869f165632` | the resolved diff base |
| Head commit | `875be2c7f73679a0d1ec108afed1df4e32c8a766` | the code segment's run-start `HEAD` |
| Base source | `feature-first-commit` | the resolution tier the code segment reported (`git-delta-review.sh base --spec`) |
| Renderer mode | `renderer: text` | the code record's header marker |
| Changed / judged / skipped / gap files | 246 / 29 / 217 / 0 | copied field by field from the record's coverage receipt block |
| Segment verdict | `not-evaluated` | 217 non-code/spec/generated/out-of-scope files were skipped with legal reasons; 29 code/test/skill files judged; zero gaps; zero `blocking` entries |
| Gate verdict | `allow` | `git-delta-review.sh report --summary --file code-review.md` exit 0; 2 `important` items answered below; 0 `blocking` |
| Reason, when one applies | skipped files carry one of the five legal reasons (`non-code-file`, `generated`, `out-of-scope-per-explicit-user-ruling`); the code paths themselves were reviewed and carry 7 notes | `code-review.md` receipt block |
| Uncommitted scope | 28 uncommitted paths (runtime records under `.specify/memory/{feedback,session,exec-quant}/`, the `.specify/state/` spine, one stage-status evidence file) are outside the reviewed object and receive no conclusion | the same sentence in `code-review.md` |
| Record | `.specify/specs/082-mechanism-policy-separation/code-review.md` | written because the triage value is `run` |
| Archive | `none` | first code-segment record for this feature |

This subsection carries the verdict and the pointers only: no opinion body, no per-severity item count. The findings themselves live in `code-review.md` and are read there.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | `requirements.md`, `plan.md`, `tasks.md`, `contracts/`, `data-model.md`, `quickstart.md`, `verification.md`, `research.md`, `feature-ref.md`, `checklists/requirements.md`, `test-evidence/` | the stage rules' standard set plus `plan.md` § Project Structure's declared additions |
| Coverage line | 11 / 11 | all eleven expected members exist |
| Missing members | none | - |
| Segment verdict | `pass` | complete; internally consistent after the in-review repairs; one cross-feature rule conflict is carried as a decision (F6) |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P1 | `.specify/specs/082-mechanism-policy-separation/contracts/skill-reference.contract.md` | 122 | none | F6: SR-06's source-path rule and Feature 029's installed-absolute skill-reference rule contradict each other; the feature's consumers now satisfy SR-06 and keep 029 red. Decision recorded; no silent rule change. |
| P2 | `.specify/specs/082-mechanism-policy-separation/feature-ref.md` | 33 | none | F8: the delivery-surface total says 24 while the listed members (3 + 9 + 11 + 1 + the separate test-only helper) sum to 25; the parenthetical also claims the helper is inside the 11 when 6 + 5 = 11 already. |
| P2 | `tests/fixtures/skill-reference/normalization-matrix.json` | 112 | none | F1's artifact face: rows R07/R08 read `dual-layer` for a source-plus-mirror pair; repaired at `875be2c7` and re-measured. |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `3ffeb26e4880f134f7a5e220ecbffb869f165632` | the resolved diff base |
| Head commit | `875be2c7f73679a0d1ec108afed1df4e32c8a766` | the code segment's run-start `HEAD` |
| Base source | `feature-first-commit` | the code skill's `base --spec` tier |
| Smoke command | `env -u PYTHONPATH bash scripts/bash/run-tests.sh -q tests/contract/test_mechanism_policy_owner_doc.py tests/contract/test_mechanism_policy_ownership.py tests/contract/test_mechanism_policy_skill_wiring.py tests/contract/test_mechanism_policy_guard.py tests/contract/test_mechanism_policy_missing_policy.py tests/contract/test_mechanism_policy_decidability.py tests/contract/test_skill_reference_grammar.py tests/contract/test_skill_reference_matrix.py tests/contract/test_skill_reference_consumers.py tests/contract/test_skill_reference_command_surface.py tests/contract/test_skill_reference_failures.py` | recorded verbatim |
| Smoke exit code | 0 | the integer the command returned |
| Smoke evidence path | `.specify/specs/082-mechanism-policy-separation/test-evidence/review-smoke-and-targeted.txt` | exists and non-empty; `102 passed in 42.06s`, exit 0 |
| Scope and regression verdict | pass after repairs: the 082-attributed in-unit set is 10 paths (== GM-03's in-unit allowed set); the two 078 C1 reds are green; the 029 test remains red for exactly the rule conflict in F6; 24 absorbed non-082 paths are disclosed, not attributed to this feature | this segment's own reading of the delta |
| Segment verdict | `pass` | smoke `pass`, scope and regression readings above |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P1 | `tests/contract/skill_reference_matrix.py` | 452 | none | F9: the executable projection returned `failure/dual-layer` for every source-plus-mirror pair; repaired at `875be2c7` (collapse before the layer test) and re-measured (SC-006 30/30). |
| P1 | `skills/external/coaching-skills/SKILL.md` | 21 | none | F10: T032 renamed the 078-owned parameter `trainee-name` to `trainee-reference`, turning both 078 C1 tests red; restored at `875be2c7` and the mirror regenerated. |
| P2 | `skills/external/coaching-skills/data-model.md` | 20 | none | F2's artifact face: the absorbed coaching files and the two 078 reds entered the baseline as "known red", which made a feature-caused change invisible to a name-only red comparison. |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Implemented` | `.specify/memory/features.md` row 082, read before the flip |
| `final_path` record, copied verbatim (7/7) | pass 8 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 8 | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/082-mechanism-policy-separation --json`; never recomputed here |
| Comparison verdict | `agree` | checker `accept` with the claim `Implemented` |
| Failed condition, on refusal | none | - |
| Fixed item, on refusal | none | - |

## 3. Findings (Problems & Improvement Targets)

### F1 — SC-006's matrix was authored from the implementation, so a wrong implementation produced a green final criterion

- **Severity**: P1
- **Category**: Workflow
- **Location**: `tests/fixtures/skill-reference/normalization-matrix.json:112` (R07) and `:450` (R27); `tests/contract/skill_reference_matrix.py:452`
- **Evidence** (verbatim quote):

  ```
  "exercises": "bare name; in the live tree both layers carry it, and § Disambiguation rules (c) says the criterion is the layer — so this closes as dual-layer. ..."
  ```

  against the owner's rule:

  ```
  **(c) Two hits in one layer are one hit; two different layers are two.**
  Example: `improve-skills` present both in the dev canonical tree and in the installed
  mirror → **one** hit. The criterion is the **layer**, not the path literal — comparing path
  literals would read the source directory and its `.specify/` mirror as two.
  ```

- **Why it's a problem**: the fixture's live rows encoded the opposite of the owner's example, so SC-006's `rows=30 matched=30` proved only that the implementation agreed with itself. The same matrix fed SC-009's `dual-layer` case. A self-confirming acceptance test can turn any implementation defect into a passing criterion.
- **Proposed fix**: derive the matrix expectations from the owner text and the ladder, not from a run of the projection; keep a negative case that changes an expectation against the owner. Fixed in this review: `_collapse_mirror_pairs` drops an installed path when its dev-canonical counterpart is a hit (FR-023(c) / V-33), the dual-layer fixture now uses `skills/internal` + `.specify/skills` (a genuine two-layer case), and SC-006/SC-009 were re-measured (`test-evidence/review-sc-006-sc-009.txt`, 30/30 rows, 10 passed).

### F2 — A known-red baseline can hide a feature-caused failure by node-id name alone

- **Severity**: P2
- **Category**: Workflow
- **Location**: `.specify/specs/082-mechanism-policy-separation/verification.md:16` and `baseline-failed.txt:2-3`
- **Evidence** (verbatim quote):

  ```
  tests/contract/test_coaching_run_contract.py::test_c1_inputs_declare_exactly_two_parameters_and_verbatim_work
  tests/contract/test_coaching_wiring_contract.py::test_c1_eight_identity_coordinates_all_hold
  ```

  and the implement-time comparison rule at `verification.md:49-51`:

  ```
  post_change_new_failed_nodeids=0 is the `comm -13` result over node-id **names** against `baseline-failed.txt` (GATE-2), not a count difference.
  ```

- **Why it's a problem**: both node ids were already red at the baseline because the uncommitted concurrent implementation had renamed the parameter; T032 then rewrote the same file and kept the tests red for the same reason. A name-only comparison cannot distinguish "still red for the pre-existing reason" from "still red, and this feature is now the reason". The implement segment could honestly report zero new names and still ship a contract violation.
- **Proposed fix**: when a baseline-red file is edited by the feature, re-run the test against the feature's file and record the failure text, not only the node id; or restore the owner's contract and require the test to go green (what this review did at `875be2c7`). The 078 C1 pair is now green (`test-evidence/review-078-coaching-regression.txt`).

### F3 — GATE-4's allowed-set sentence and the guard's test name still described the pre-absorption eight rows

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/specs/082-mechanism-policy-separation/data-model.md:282` (before repair); `tests/contract/test_mechanism_policy_guard.py:473`
- **Evidence** (verbatim quote, before repair):

  ```
  登记表在**比较单元内**的条目恰为第 1–8 行（**1 条新增 + 7 条改写** ...）
  ```

  and the test name `test_gm03_allowed_set_parses_to_eight_in_unit_rows` whose body asserts `len(inside) == 10`.
- **Why it's a problem**: GM-03 marks rows 19–20 as in-unit, so the sentence and the test name contradicted the table they describe; a future reader could delete or ignore rows 19–20 and still believe the set is eight. GATE-4 disclosed the stale literal but the artifact was not repaired.
- **Proposed fix**: state "rows 1–8 + 19–20 (10)" in the data-model, rename the test to `..._ten_in_unit_rows`, and keep the guard's messages consistent. Fixed in this review (PLAN-EDIT: data-model GM-03 count sentence, non-substantive).

### F4 — SC-002's before/after harness cannot attribute detection to the changed skill

- **Severity**: P2
- **Category**: Workflow
- **Location**: `.specify/specs/082-mechanism-policy-separation/verification.md:130-132`; `test-evidence/sc-002-2026-11-05.txt` § 7
- **Evidence** (verbatim quote):

  ```
  The harness supplies the policy **values** so the flow can proceed, and a capable general model detects both misplaced samples in the before state too, so this reading does **not** establish that the changed skill causes detection.
  ```

- **Why it's a problem**: the criterion's two literal numbers (detection 2/2, false positives 0/2) are met, but the same numbers hold before the change, so the reading cannot distinguish "the new checklist works" from "a capable model always detects these samples". The implement segment disclosed the limitation; the acceptance claim still reads `pass`.
- **Proposed fix**: write effect-measuring criteria as a before/after differential (e.g. a sample that only the new checklist forces, or a weaker host), or mark the criterion `supporting`. For this feature: accept `pass` on the literal numbers with the §7 limitation recorded as residual risk; no second run is expected to separate the two states.

### F5 — SC-005's uninvolved reader answered 13/14; Q-06 shows a boundary sentence with two defensible readings

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/specs/082-mechanism-policy-separation/verification.md:142-149`; owner `shared/definitions/mechanism-policy-definitions.md:326-331` (S-12)
- **Evidence** (verbatim quote):

  ```
  SC-005_value=correct = 13 / 14 (full set size = 14); the one divergence is Q-06, answered `策略` while the owner's key is `待澄清`
  ```

  and S-12's key:

  ```
  答案：待澄清。依据：「重新生成镜像」换掉运行环境仍成立（机制），「写进项目里」随运行环境而变（策略）；两判都成立，须问清「项目」指哪个落点。
  ```

- **Why it's a problem**: a reader can reasonably treat "写进项目里" as a policy statement and answer `策略`; the key requires `待澄清` because both directions hold. The criterion is `supporting`, so the shortfall does not refuse the transition, but the divergence is a documentation ambiguity, not a bad reader.
- **Proposed fix**: keep SC-005 as `partial` (supporting, not blocking); in a follow-up owner revision, sharpen S-12's boundary sentence to say why the mixed sentence closes as `待澄清` rather than by its stronger half. Do not re-run readers until one scores 14/14.

### F6 — Feature 029's installed-absolute skill-reference rule and Feature 082's source-canonical ruling contradict each other

- **Severity**: P1
- **Category**: Documentation
- **Location**: `tests/contract/test_shared_reference_rewrite.py:75-103`; `contracts/skill-reference.contract.md:122-125`; `requirements.md:305` (clarify decision 2)
- **Evidence** (verbatim quote, 029's rule):

  ```
  - Sibling skills live in the two-layer source tree ``skills/{external,internal}/<name>/`` and
    use the installed-absolute form ``.specify/shared/<type>/<f>.md``.
  ```

  against 082's ruling:

  ```
  **source-canonical：消费方引用源路径，镜像只作为生成物存在**
  ```

  and SR-06's guard: `以 .specify/shared/definitions/ 为前缀的引用串零命中`.
- **Why it's a problem**: the five 082 consumers now cite `shared/definitions/skill-reference-definitions.md` (source path), which 029's `test_skills_use_installed_absolute_shared_form` rejects. The test was already red at the baseline with 17 offenders; 082 adds 7 more. A client project that installs the skill tree only has `.specify/shared/`, so the source path is unresolvable from `.specify/skills/` unless the reader resolves "relative to the framework root" — the clarify ruling says it does, but 029's rule says it must not be written that way.
- **Proposed fix**: a framework-level decision, not a silent edit. Options are recorded below; the review does not change either rule.
- **Disposition**: `decision` (fast-fail). The feature's artifacts are consistent with the ratified clarify position; the 029 test remains a known baseline red and the conflict is handed to the user.

#### Decision — 029 shared-reference form vs 082 source-canonical ruling

**Question**: which reference form do the five meta-skill consumers use for the skill-reference owner — the framework-source path (`shared/definitions/skill-reference-definitions.md`) or the installed-absolute path (`.specify/shared/definitions/skill-reference-definitions.md`)?

**Options**

| Option | What changes | Cost / risk | Recommendation |
|--------|--------------|-------------|----------------|
| A. Keep 082's source-canonical ruling and revise 029's rule | 029's test accepts the source form for framework-source definition references (a documented exception or a rule rewrite); the 17 pre-existing offenders can be migrated in one pass | one cross-feature rule change; the 029 guard's "resolvable in a client project" intent must be preserved by a "resolve relative to framework root" statement | **recommended** — the mirror is a generated artifact (FR-028), and `.specify/shared/` does not exist in standalone deployments |
| B. Revert the five consumers to installed-absolute | 082's SR-06, SC-007 and the clarify decision 2 are revised; the consumers cite `.specify/...` | breaks the standalone topology and the "source is truth" rationale; re-opens a ratified clarify answer | not recommended |
| C. Keep both rules and the baseline red | no framework change; the 029 test stays red; 082 ships a consumer form its own framework guard rejects | two contradicting guards persist; every future edit pays the ambiguity | acceptable only as a time-boxed deferral |

### F7 — SW-05's zero-literal carrier was named by the contract but absent from its assigned test module

- **Severity**: P2
- **Category**: Automation
- **Location**: `contracts/guard-and-measurement.contract.md:147`; `tests/contract/test_skill_reference_consumers.py` (before repair)
- **Evidence** (verbatim quote):

  ```
  `coaching-skills` / `run-skills` 在 GM-03 的逐字节断言里**失效** ... 补偿判据是**同一个模块**里的两条断言各占一半：`tests/contract/test_skill_reference_consumers.py`（tasks T027）既持 SW-05 的行形态/字面零命中断言，也持 GM-12 的接线条数断言。
  ```

- **Why it's a problem**: the module held the GM-12 scan but not the SW-05 mechanism/policy-literal scan; GATE-6 was a one-off shell `grep`, so a later edit that leaked a judgement literal into `coaching-skills` or `run-skills` would pass every test. The evidence was true; the mechanised carrier its contract requires was missing.
- **Proposed fix**: add the SW-05 scan to the named module (denominator printed, literal set from the contract, negative case). Fixed in this review: `test_sw05_excluded_members_carry_no_mechanism_policy_literal` + its negative case; the live run reads `scanned=4` and zero hits.

### F8 — The delivery-surface total double-counts the test-only helper

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/specs/082-mechanism-policy-separation/feature-ref.md:27` and `:33`
- **Evidence** (verbatim quote):

  ```
  **合计 24** = 新增 3 + 改写 9 + 新增测试 11 + 矩阵 fixture 1（test-only 辅助 `tests/contract/skill_reference_matrix.py` 已含在「新增测试 11」的口径内，不另计 ...）
  ```

  while the same file lists "机制/策略 6 + 技能引用 5 = 11" and separately names the helper.
- **Why it's a problem**: 6 + 5 already fills the 11, so the helper is a twelfth test file; the listed members sum to 25, not 24. A totals line that does not close on its own items is the same class of defect the review's one-source-of-truth rule targets.
- **Proposed fix**: state 25 and move the helper into its own "+1" item, or state 24 and exclude the helper from the delivery surface explicitly. Not repaired here because the correction touches the plan-owned delivery surface and belongs with the 029 decision's follow-up (the same file already carries the 24 literal).

### F9 — The executable normalization projection returned `dual-layer` for every source-plus-mirror pair

- **Severity**: P1
- **Category**: Automation
- **Location**: `tests/contract/skill_reference_matrix.py:452` (before repair)
- **Evidence** (verbatim quote, a live run before the repair):

  ```
  improve-skills -> failure improve-skills {"failure_class": "dual-layer", "report_items": {"candidate_paths": [".specify/skills/improve-skills/SKILL.md", "skills/external/improve-skills/SKILL.md"], ...}}
  ```

  and `data-model.md` V-33:

  ```
  「同名两处」只在**不同层**时才算两处；dev 规范层与其安装镜像的同名命中算一处（FR-023(c)）。因此 `dual-layer` 断言 MUST 用两个不同层的 fixture 行，不能拿「源 + 镜像」当反例。
  ```

- **Why it's a problem**: in this repository almost every skill exists at both `skills/external/<name>` and its generated mirror `.specify/skills/<name>`; the projection therefore reported the *normal* state as a failure, and the five meta-skills could not resolve their own targets under the executable model. The fixture had codified that behavior.
- **Proposed fix**: collapse mirror pairs before the layer test, keep ladder order when one layer has several hits, and rebuild the dual-layer fixture from two genuinely different layers. Fixed at `875be2c7`; SC-006 30/30 and SC-009 10 passed (`test-evidence/review-sc-006-sc-009.txt`).

### F10 — T032 renamed a 078-owned parameter, breaking both 078 C1 contract tests

- **Severity**: P1
- **Category**: Workflow
- **Location**: `skills/external/coaching-skills/SKILL.md:4` and `:21` (before repair); `tests/contract/test_coaching_run_contract.py:223`; `tests/contract/test_coaching_wiring_contract.py:45`
- **Evidence** (verbatim quote, 082's T032 diff):

  ```
  Invocation: `coaching-skills <trainee-reference|trainee-path> <work>`.
  ```

  against Feature 078's contract:

  ```
  - The skill accepts **exactly two positional parameters**: `<trainee-name|trainee-path>` and `<work>`.
  ```

- **Why it's a problem**: 078 is the owner of the coaching identity/wiring contract; 082's task only said "declare its own parameter", not rename it. The rename made `test_coaching_run_contract::test_c1...` and `test_coaching_wiring_contract::test_c1...` red for a reason unrelated to 078, and the baseline already contained them, so the name-only regression comparison could not see it (F2).
- **Proposed fix**: restore the owner's parameter name in the source and regenerate the mirror; let the 078 tests guard the name. Fixed at `875be2c7`; both tests green (`test-evidence/review-078-coaching-regression.txt`).

#### Code-segment important items — answers

The current `code-review.md` carries two `important` items; the transition rule requires each to be answered.

| Item | Answer | Reason |
|------|--------|--------|
| `tests/contract/skill_reference_matrix.py:371` — the normalization projection was repaired during review; live-tree rows remain tree-state dependent | agree | The mirror-collapse rule is now the owner's (FR-023(c) / V-33) and the live rows exercise the real ladder. The residual fragility is disclosed and covered by the SC-006 re-measurement; a future skill moving between layers must re-run SC-006, as the test docstring already says. |
| `skills/external/coaching-skills/SKILL.md:21` — T032 renamed the 078-owned parameter; restored | agree | 078 owns the parameter name; 082's wiring only needed to declare the parameter and cite the reference owner. The restored name keeps both 078 C1 tests green and the mirror is regenerated from the source. |

## 4. What Worked — Preserve (Brief)

- The task-grouped 082 commit history (`bfc18fe5` … `6785e8de`) makes the per-task timeline reconstructible without artifact-state inference.
- `test_mechanism_policy_guard.py`'s baseline-blob comparison, explicit absorbed-path disclosure and three negative cases are a strong template for closed-set containment claims.
- `test_mechanism_policy_missing_policy.py`'s sha256 + directory-set snapshot (never mtime) is the right shape for a zero-write claim, and its negative case actually injects a write.
- The `decision`-then-options handling of the 029 conflict (instead of a silent rewrite) kept both owners intact while surfacing the choice.
- The ARC program's `final_path` record and the four-condition gate made the status flip mechanical and auditable.

## 5. spec-kit / SDD Improvement Recommendations

### 5.3 Automation / Script Improvements

- **Derive acceptance matrices from the owner, not from the implementation** — Target: `templates/commands/implement.md` and `templates/commands/review.md` (absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/commands/review.md`). Change: when a criterion's carrier is a fixture/expectation table, require the plan/tasks row to name the owner text each expectation is derived from, and require the code segment to check one row against the owner independently. Source: F1, F9. Expected impact: a wrong implementation can no longer make its own criterion green.
- **Give the code-review receipt a code-path scope** — Target: `skills/internal/code-review/scripts/git-delta-review.sh` (absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/code-review/scripts/git-delta-review.sh`). Change: let `receipt` count coverage against the triage's `--code-paths` set (with the non-code files disclosed as out of scope) instead of forcing a `not-evaluated` verdict whenever a spec/generated file is skipped. Source: the 246/29/217 receipt in `code-review.md`. Expected impact: a composed review can still claim a clean code segment without pretending to have read 100 KB spec artifacts.
- **Mechanise the SW-05 compensation scan** — Target: `tests/contract/test_skill_reference_consumers.py` (absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/tests/contract/test_skill_reference_consumers.py`). Change: keep the two added SW-05 tests as the permanent carrier and delete the one-off GATE-6 shell scan from future evidence sets. Source: F7. Expected impact: an excluded member cannot silently acquire a judgement literal.

### 5.4 Workflow Improvements

- **Write effect-measuring criteria as before/after differentials** — Target: `templates/requirements-template.md` (absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/requirements-template.md`). Change: for a criterion whose subject is "flow X now detects Y", require the source sentence to name the before state and the discriminating sample, or mark the criterion `supporting`. Source: F4. Expected impact: SC-002-style readings stop reading green on a property the baseline already had.
- **Baseline capture must label uncommitted concurrent work** — Target: `templates/commands/implement.md` (absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/commands/implement.md`). Change: when the baseline run is taken from a tree carrying uncommitted concurrent changes, record the dirty set beside the baseline and re-check any baseline-red file the feature edits. Source: F2, F10. Expected impact: a feature cannot inherit a red and then change its cause without anyone seeing it.
- **Resolve the 029 vs 082 reference-form conflict** — Target: `tests/contract/test_shared_reference_rewrite.py` (absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/tests/contract/test_shared_reference_rewrite.py`) plus the 029 rule's owner. Change: apply decision option A or B above; do not leave both guards active. Source: F6. Expected impact: one reference form has one owner again.

### 5.5 Documentation Improvements

- **State the mirror-collapse example as a rule, not only as an example** — Target: `shared/definitions/skill-reference-definitions.md` (absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/shared/definitions/skill-reference-definitions.md`). Change: add one sentence to rule (c) that a source path and its generated mirror are one hit and that the executable projection must collapse them before grouping by layer. Source: F1, F9. Expected impact: the next implementer cannot read the two layer names as two hits.
- **Sharpen S-12's boundary sentence** — Target: `shared/definitions/mechanism-policy-definitions.md` (absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/shared/definitions/mechanism-policy-definitions.md`). Change: say why the mixed sentence closes as `待澄清` rather than by its stronger half. Source: F5. Expected impact: SC-005's reader sample stops diverging on Q-06.
- **Make the delivery-surface total close on its own items** — Target: `.specify/specs/082-mechanism-policy-separation/feature-ref.md` (absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/082-mechanism-policy-separation/feature-ref.md`). Change: 25 with the helper as a separate +1, or 24 with the helper explicitly excluded. Source: F8. Expected impact: the count can be recomputed from the list.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Resolve the 029 vs 082 source-vs-installed reference form (decision A/B/C) | `tests/contract/test_shared_reference_rewrite.py` + 029 rule owner | F6 |
| P1 | Derive acceptance matrices from the owner text | `templates/commands/review.md` / implement template | F1, F9 |
| P2 | Effect-measuring criteria as before/after differentials | `templates/requirements-template.md` | F4 |
| P2 | Label uncommitted concurrent work in the baseline | `templates/commands/implement.md` | F2, F10 |
| P2 | Scope the code-review receipt to code paths | `skills/internal/code-review/scripts/git-delta-review.sh` | the 246/29/217 receipt |
| P2 | Keep the SW-05 carrier; retire the one-off GATE-6 scan | `tests/contract/test_skill_reference_consumers.py` | F7 |
| P2 | State the mirror-collapse rule explicitly | `shared/definitions/skill-reference-definitions.md` | F1, F9 |
| P2 | Sharpen S-12 and close the delivery count | owner document + `feature-ref.md` | F5, F8 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason. (No `REC-…` id was coined in this report; the recommendations carry plain titles.)
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No unexpanded placeholder tokens remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: **No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.**

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
