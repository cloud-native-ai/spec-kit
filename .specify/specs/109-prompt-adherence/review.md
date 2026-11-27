# Specification-Driven Development (SDD) Process Review Report: Prompt Adherence Evaluation（提示遵从度评价）— 109-prompt-adherence

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap or a review finding, it does not belong here.

## Segment Verdicts (one composed run, fixed order)

| Order | Segment | Verdict | Findings (own vocabulary) |
|-------|---------|---------|---------------------------|
| 1 | process | **pass** | 0 P0 · 1 P1 · 2 P2 |
| 2 | artifact | **pass** | 0 P0 · 0 P1 · 1 P2 |
| 3 | implementation | **pass** | none |
| 4 | code | **not-evaluated** (0 coverage gap; 0 blocking; gate `allow`) | 0 blocking · 0 important · 2 suggestion · 1 question · 1 praise |
| — | Acceptance Reality Check | **agree** (`final_path` pass 8 / total 8; four completion conditions true) | — |
| — | **Consolidated review verdict** | **accept** | **blocking findings: 0** |

Status transition: Feature 109 `Implemented → Ready for Review` — allowed under the review gate (review evidence exists; the current `code-review.md` carries no blocking entry; no `final`-path criterion sits in `blocked` / `deferred` / `fail`).

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 109 |
| Requirement Key | 109-prompt-adherence |
| Requirement Name | Prompt Adherence Evaluation（提示遵从度评价） |
| Related Feature | 109 Prompt Adherence Evaluation（提示遵从度评价） |
| Repository | spec-kit (`specify-cli`, framework version 0.0.22 as answered by the engine's `--version`) |
| Repository URL | `(no single resolvable URL for this commit)` — four remotes exist: `gitee` git@gitee.com:cloud-native-ai/spec-kit.git, `github` git@github.com:cloud-native-ai/spec-kit.git, `gitlab` git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git, and `origin` **which is the UPSTREAM** git@github.com:github/spec-kit.git |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty — the commit is unpushed. Every citation below is repo-relative plus this worktree's absolute path; recover any file with `git show 25e8b3eacd24407efbf6a306e2f0f8ed79b1279d:<repo-relative-path>` |
| Branch | 109-prompt-adherence (git worktree `.specify/.tmp/sdd-loop/worktrees/prompt-adherence`; main tree stays on `master`) |
| Commit SHA | 25e8b3eacd24407efbf6a306e2f0f8ed79b1279d (short: 25e8b3eac) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/prompt-adherence |
| Review Date | 2026-11-27 |
| Reviewer (Agent) | SDD Review Coordinator (fresh-context subagent; the four segments and ARC executed in one consolidation pass — no segment was produced by the implement executor) |
| Environment | Linux x86_64; bash; Python 3.11.11 at `/usr/local/bin/python3` (pytest 8.4.2 via `scripts/bash/run-tests.sh`); git 2.43.5; `specify_cli` not installed in the review shell — the engine's own `--version` answers `prompt-adherence.py 0.0.22` |
| spec-kit Source Snapshot | this repository itself @ 25e8b3eac (dogfooding: framework sources and the client runtime live in one tree) |

**Baseline note (transparent):** the dispatch brief names `d3c0d5e22` (implement closure) as the stage baseline, while the line spine records `stage_base_commit: 25e8b3eac` (checkpoint 07, one spec-only commit later — it adds only `checkpoints/07-implement.md`). Both facts are recorded here; the judged product delta resolves by the code skill's own base route to `0419adae5..25e8b3eac`.

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 309 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/prompt-adherence/.specify/specs/109-prompt-adherence/requirements.md | 30 FR / 9 SC, 18 adjudicated assumptions, clarifications of 2026-11-27 |
| plan.md | 283 | …/109-prompt-adherence/plan.md | 23-row Constitution Check, 8 execution premises, 1 inherited-blockers disposition, PA1–PA16 |
| tasks.md | 354 | …/109-prompt-adherence/tasks.md | 39 rows T001–T039, all closed; tests mode ON; FR/SC/clause coverage maps |
| data-model.md | 205 | …/109-prompt-adherence/data-model.md | 11 entities E-1…E-11 + 14 invariants I-1…I-14 |
| contracts/ (6 files) | 633 | …/109-prompt-adherence/contracts/ | 39 clauses C-001…C-046 across owner, declarations, reading, engine, distribution, guards |
| quickstart.md | 199 | …/109-prompt-adherence/quickstart.md | 6 scenarios + measured sensor reads + distribution/suite checks |
| research.md | 189 | …/109-prompt-adherence/research.md | R-1…R-11 + RU-1…RU-3 |
| feature-ref.md | 98 | …/109-prompt-adherence/feature-ref.md | 30 FR / 9 SC delivery maps and integration authority |
| verification.md | 79 | …/109-prompt-adherence/verification.md | SC-001…SC-009 status rows (8 final / 1 supporting), smoke triple, baseline and gates |
| checklists/ (2 files) | 173 | …/109-prompt-adherence/checklists/ | requirements validation + 40-item quality checklist |
| test-evidence/ (~30 files) | — | …/109-prompt-adherence/test-evidence/ | gate captures, red-first/green runs, boundary readings, workspace signatures |
| review.md / code-review.md | — | …/109-prompt-adherence/ | this report and the code-segment record |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | Line entry, U0/U1 probe (worktree on `109-prompt-adherence`, base `0419adae5`; spec max 108; breakpoint `requirements`) | spine `/storage/project/cloud-native-ai/spec-kit/.specify/state/prompt-adherence.md` § U0/U1 | no |
| 2 | requirements attempt 1 pass; manual scaffold from the requirements template | commits `4237ca1cd`, `9ffb0d6f3`; `test-evidence/requirements-stage-2026-11-27.md` § Scaffold deviation (A-13); validator 0 error / 0 warning, 296 lines | **yes — manual scaffold** (finding F1) |
| 3 | clarify pass; 14 Q rows integrated; Feature 109 registered `Draft`; `overlap-check` clear | commits `e7a155bb4`, `534688278` | no |
| 4 | plan pass; 6 contracts / 39 clauses / 11 entities + 14 invariants; Draft → Planned; in-passing corrections PA10–PA16 disclosed | commits `cf7eb0071`, `34f2c7492`; `test-evidence/plan-stage-2026-11-27.md` | no |
| 5 | tasks pass; 39 rows, tests mode ON, clause coverage 39/39; a `/tmp` probe file created and deleted (temp-discipline deviation, disclosed) | commits `b41e6c9b9`, `7e32ea372`; spine U4 tasks | minor — disclosed in passing, repaired |
| 6 | checklist pass; `pre-analyze-check --stage checklist` rejects the stage (exit 2) and the run records a "tool-coverage fact" | commits `0a4da72dc`, `127fb2134`, `949cb3631`, `60d3f6840`; `test-evidence/pre-analyze-checklist.txt` | **yes — gate not runnable for this stage** (finding F2) |
| 7 | analyze pass; 20 findings (0 C / 0 H / 13 M / 7 L) → gate pass; implement declared as 4 serial packages (`write-conflict`) | commit `3a4ee4dc2`; `test-evidence/analyze-round1-report.md` | no |
| 8 | implement P1–P4; implement-entry baseline 222 failed names; five guard files authored red-first and closed green; per-package commits | `ef0639b8e`, `09a55c5af`, `009e28b37`, `4df05c1b4`, `12c281ad9`, `21cab972e`, `b7661f617` | no |
| 9 | First F-1 full-suite reading: exactly one NEW failed name (bilingual-literal consumer registration) → guard-owner registration → slot re-read; second reading 222 failed / 10361 passed / 3 skipped, zero NEW names | commit `1321bb609`; `notes/red-first-evidence.md` § T038; `test-evidence/implementation-gates.txt` § GATE-1 | **yes — a full-suite re-read paid for an authoring-time miss** (finding F3) |
| 10 | Implement closure: smoke pass, closure-acceptance `accept` (final_path 8/8), flip to `Implemented`, checkpoint 07 | commit `d3c0d5e22`, checkpoint `25e8b3eac`; `checkpoints/07-implement.md` | no |
| 11 | Review dispatch (this run): four segments + ARC; code segment `base` resolves `0419adae5` (`feature-first-commit`), head fixed at `25e8b3eac`; live smoke re-run `77 passed in 7.70s`, exit 0 | this report; `code-review.md`; spine § U2 review | no |
| 12 | Code segment non-interactive path: `start` (renderer text) → 4 `note` entries → `receipt` (182 changed / 19 judged / 163 legally skipped / 0 gap) → `report` gate `allow` → `capture` skipped (framework hat) | `code-review.md` receipt block and capture line | no |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 1 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 3 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 0 |
| Automation / Scripts | 2 |
| Workflow | 0 |
| Documentation | 2 |

(The counts aggregate the process, artifact and implementation segments — the three consumers of the `P0`/`P1`/`P2` family. The code segment's six-level vocabulary is counted in §2.1 and never mapped onto this table.)

**P0 validation**: No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `0419adae5e6e0e208ad6bcb443e45be8d266f04a` | the resolved diff base |
| Head commit | `25e8b3eacd24407efbf6a306e2f0f8ed79b1279d` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the resolution tier `git-delta-review.sh base` reported |
| Renderer mode | `text` | the code record's header marker (`renderer: text`) |
| Changed / judged / skipped / gap files | 182 / 19 / 163 / 0 | copied field by field from the record's coverage receipt block |
| Lines added / deleted (judged surface) | 4846 / 2 | the record's receipt block |
| Segment verdict | `not-evaluated` | skip is legal but never coverage credit (163 legal skips; 0 gap; 0 blocking) |
| Gate verdict | `allow` | `report --summary --file …` exit 0 — 0 blocking, 0 important |
| Reason, when one applies | 163 files skipped with legal reasons: `non-code-file` for spec artifacts/checkpoints/evidence/fixtures, `generated` for mirrors and machine-written run records; 19 product files judged; 0 gaps | receipt `file.*.reason=` entries |
| Uncommitted scope | none at receipt time (the receipt's own filter excludes the code-review record itself); this report, the status flip and the wrap-up records are written after receipt and are included in the review-stage commit | receipt; `git status` |
| Record | `.specify/specs/109-prompt-adherence/code-review.md` | written by `start`; notes, receipt block and capture line appended by the deterministic path |
| Archive | `none` | `start` output (first run) |

The code record's finding entries (read there, not restated here): 2 `suggestion` (one on the `--check-coverage` action's hard dependency on two sibling engine modules, `scripts/python/prompt-adherence.py:1227`; one on the exec-quant citation path binding, `:789`), 1 `question` (`--json` ignored with `--check-coverage`, `:1572`), 1 `praise` (the read-only containment guard, `tests/contract/test_prompt_adherence_readonly.py`).

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | `requirements.md`, `plan.md`, `tasks.md`, `contracts/` (6 files), `data-model.md`, `quickstart.md`, `verification.md`, `research.md`, `feature-ref.md`, `checklists/`, `test-evidence/` — 11 members | derived per slice from the stage rules and `plan.md` § Project Structure (`plan.md:163–197`) |
| Coverage line | 11 / 11 | every expected member is present on disk |
| Missing members | none | — |
| Segment verdict | `pass` | — |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P2 | `.specify/specs/109-prompt-adherence/plan.md` | 34 | — | The plan/requirements/contract all claim "no `runtime-store-layout.yaml` change", but the delta adds one `consumers` entry; disclosed only in `test-evidence/boundary-readings.txt` — see F4 |

Dimension readings (each dimension answered, not narrated):

1. **Completeness** — 11/11 expected members present; every member carries its template's required sections (plan's premises/inherited-blockers tables, verification's SC rows and smoke triple, contracts' `Serves` lines).
2. **Internal consistency** — FR=30 and SC=9 agree across requirements / plan / tasks / feature detail; clauses 7+7+10+5+3+7=39 agree across plan and tasks; the catalog's six rows, six blind spots, twelve assumed behaviors and the four closed-set sizes agree between the owner document and the five facts. One inconsistency found (F4).
3. **Traceability** — every FR-001…FR-030 names at least one task row (tasks.md § Requirement Coverage Map); every SC-001…SC-009 names evidence rows and every `final` criterion carries a `pass` status row in `verification.md`; the SC-to-test mapping is registered in `feature-ref.md`; the closure checker independently confirms 39/39 closed rows and 8/8 final pass.
4. **Dependency and premise ownership** — EP-001…EP-008 each name their evidence and status (`plan.md:220–234`); the inherited-blockers table carries one `not-applicable` row with its measured basis; borrowed facts (store roster, seven-state domain, gate-family prefix) are reached by path, not restated.
5. **Acceptance honesty** — every `pass` row cites the command and the tree it was read on; the F-1 replacement reading is disclosed with its cause and repair; SC-009 is marked `supporting`, not counted in `final_path`; no red-first claim lacks a recorded red run (`notes/red-first-evidence.md` § T010/T025/T027/T029).

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `0419adae5e6e0e208ad6bcb443e45be8d266f04a` | the resolved diff base (`feature-first-commit`) |
| Head commit | `25e8b3eacd24407efbf6a306e2f0f8ed79b1279d` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | `git-delta-review.sh base` |
| Smoke command | `env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_prompt_adherence_engine.py tests/contract/test_prompt_adherence_owner.py tests/contract/test_prompt_adherence_declarations.py tests/contract/test_prompt_adherence_readonly.py tests/integration/test_prompt_adherence_init.py -q` | recorded verbatim in `verification.md` |
| Smoke exit code | 0 (recorded run); independently re-run by this review: 0 — `77 passed in 7.70s` | `test-evidence/smoke-run.txt`; this review's own run |
| Smoke evidence path | `.specify/specs/109-prompt-adherence/test-evidence/smoke-run.txt` (exists, non-empty) | verification.md |
| Scope and regression verdict | scope clean — every judged hunk serves a task row; the one guard-forced `runtime-store-layout.yaml` consumer line and the bilingual whitelist registration are disclosed (the latter also its own finding, F3/F4). Regression re-measured — smoke green on the reviewed tree; `sync-mirrors.py --check` exit 0 (scripts 134 / shared 123 files byte-identical); `regen-command-copies.py --check` exit 0; engine and owner source/mirror copies byte-identical; recorded F-1 shows zero NEW failed names against the 222-name implement-entry baseline | this review's runs; `test-evidence/implementation-gates.txt` § GATE-1 |
| Segment verdict | `pass` | — |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| — | — | — | — | none |

The closure checker's `final_path` record is quoted, never judged: `accept`, all four completion conditions true (see §2.4).

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Implemented` | `.specify/features.md` row 109, copied by the checker |
| `final_path` record, copied verbatim (7/7) | pass 8 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 8 | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/109-prompt-adherence --json` (exit 0) |
| Comparison verdict | `agree` | the claim survives its own counts |
| Failed condition, on refusal | none | — |
| Fixed item, on refusal | none | — |

The checker also reports `no_open_rows: true`, `status_row_per_criterion: true`, `every_final_path_pass: true`, `smoke_record_pass: true` (one smoke record; exit 0; evidence exists), `tasks.closed=39`.

## 3. Findings (Problems & Improvement Targets)

### F1 — `create-new-requirements.sh` self-counts the current branch and forces a manual requirements scaffold

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `scripts/bash/create-new-requirements.sh` (absolute: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/prompt-adherence/scripts/bash/create-new-requirements.sh`), candidate enumeration around lines 352–387
- **Evidence** (verbatim; the record of this script's effect):

  ```
  当前工作树已处于分支 `109-prompt-adherence`，`create-new-requirements.sh` 会把该分支计入编号空间并派生 110 且新建分支，与本线「停留在既有分支、编号 109」冲突；按 108 A-16 先例，本阶段**手工**从 `.specify/templates/requirements-template.md` 脚手架到 `.specify/specs/109-prompt-adherence/requirements.md`，脚本的模板拷贝步骤等价复刻，仅跳过其编号派生与建分支步骤。
  ```

  and the script's own candidate scan:

  ```
      # Local branches: top-level form only (any slash → not spec numbering).
      while IFS= read -r branch; do
          [ -n "$branch" ] || continue
          case "$branch" in */*) continue ;; esac
          consider_number_candidate "$branch"
      done < <(git branch --format='%(refname:short)' 2>/dev/null)
  ```

- **Why it's a problem**: an SDD line that starts on an already-checked-out feature branch cannot use the creator: the current branch is itself a numbering candidate, so the script derives the NEXT number and would create a second branch. This is the **second recorded occurrence** (Feature 108 A-16 is the cited precedent), so every line running the SDD driver in a worktree pays a manual scaffold and hand-verifies template fidelity.
- **Proposed fix**: give `create-new-requirements.sh` an explicit in-place mode (`--feature-id <NNN>` / `--branch <name>`: scaffold the spec dir on the current branch, skip number derivation and branch creation) and name that mode in the requirements stage brief. Record the current behavior in the script's help so the escape is discoverable.

### F2 — the pre-analyze gate has no `checklist` stage, so a checklist line records a dead gate call

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: `.specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py:1340` with the stage matrix at `shared/declarations/facts/driver-gate-roster.yaml:23–32`
- **Evidence** (verbatim CLI output and declaration):

  ```
  pre-analyze-check.py: error: argument --stage: invalid choice: 'checklist' (choose from 'requirements', 'plan', 'tasks')
  ```

  ```
    stages:
      requirements:
        - requirements.md
      plan:
        - requirements.md
        - plan.md
      tasks:
        - requirements.md
        - plan.md
        - tasks.md
  ```

- **Why it's a problem**: the stage matrix is declared (good), but the checklist stage is not in it and nothing in the driver's stage vocabulary says "checklist runs no pre-analyze gate". The stage executor attempted the gate, got exit 2, and had to record a "tool-coverage fact" — one wasted step and one more bespoke note per checklist run. A reader cannot tell an intentional absence from an uncovered stage.
- **Proposed fix**: either add a `checklist` row to `driver-gate-roster.yaml` (its input list is `requirements.md`, `plan.md`, `tasks.md`, `checklists/requirements.md`) or state the intentional absence explicitly in the driver's stage table/help, so no checklist run re-derives it.

### F3 — a new owner document's Shared-Strings registration is only discovered by the F-1 full-suite reading

- **Severity**: P2
- **Category**: Documentation
- **Location**: `shared/guidelines/bilingual-expression.md:7` (the obligation) and the implement stage's guard roster where it is not surfaced (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/prompt-adherence/shared/guidelines/bilingual-expression.md`)
- **Evidence** (verbatim from `notes/red-first-evidence.md` § T038):

  ```
  The first F-1 full-suite reading on the feat tree produced exactly one NEW failed name against the
  222-name baseline:

  tests/contract/test_bilingual_expression.py::test_drift_str_literal_unique_consumers
  ```

  and the guideline's own rule:

  ```
  **Shared Strings 维护协议（C-03）**：…各字面量的唯一消费点由契约测试的漂移守卫（`tests/contract/test_bilingual_expression.py`）核验，新增消费方 MUST 先改守卫白名单再落字。
  ```

- **Why it's a problem**: the rule is stated in its owner, but nothing in the implement stage's authoring flow surfaces it when a new `shared/definitions/` owner document is written. The miss was caught only by the one full-suite reading — and the fix forced a second full-suite reading of the whole suite (76 s each) because the slot's rule requires re-taking the reading after a test-affecting edit. The process recovered honestly (registration, not suppression), but the toll is recurring for every new owner document that cites the owner path.
- **Proposed fix**: add the registration step ("a new `shared/definitions/` document citing the Shared Strings owner registers its path in the drift guard's whitelist in the same change") to the implement stage's authoring checklist / guard roster and to the owner-document template's checklist, so the first full-suite reading is not the discovery point.

### F4 — three artifacts claim the store-layout fact is unmodified, but the delta adds a consumer line

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/specs/109-prompt-adherence/plan.md:34`, `.specify/specs/109-prompt-adherence/requirements.md:44` (A-6), `.specify/specs/109-prompt-adherence/contracts/distribution.contract.md:17`
- **Evidence** (verbatim claims, then the delta):

  ```
  **Constraints**: … no `.specify/.gitignore` rule and no `runtime-store-layout.yaml` change; no decision-governance alignment (107 stays independent)
  ```

  ```
  | **A-6** | **不新增运行期存储**：读取全部读时派生，不新增 store root、记录类型、采集点或 schema；`runtime-store-layout.yaml` 不被本特性修改，因其无新运行期目录，…
  ```

  ```
  +  - scripts/python/prompt-adherence.py
  ```

  The change is disclosed in the evidence, not in the artifacts:

  ```
  `test_declaration_equals_inventory_and_consumer_sets` required
  `shared/declarations/facts/runtime-store-layout.yaml`'s declared consumer set to name the new
  reader (the fact's own owner invariant: the list is exactly the code files that read the fact)
  ```

- **Why it's a problem**: the consumer registration is legitimate and guard-forced, but the artifact set still asserts a fact the delta falsifies. This is the one place where a reader of the plan/contract/requirements gets a claim that the tree contradicts — exactly the internal-consistency failure mode One Source of Truth is meant to prevent. The evidence file carries the truth; the artifacts do not point at it.
- **Proposed fix**: amend the three sites to the precise fact — "no store-set / layout change; the existing consumer guard requires `scripts/python/prompt-adherence.py` to be named in `runtime-store-layout.yaml`'s `consumers` list (registered in the same change)" — or replace the claim with a pointer to the boundary reading that records the registration.

## 4. What Worked — Preserve (Brief)

- **Deterministic gates between stages**: every stage closed on a named script verdict (`validate-requirements`, `pre-analyze`, `validate-tasks`, `decomposition-check`), with the raw output kept in `test-evidence/`.
- **Red-first guard discipline**: five guard files authored before the engine (T010/T017/T019/T023/T024) with named "engine absent" failure messages, and the readonly guard proves its own comparator can go red.
- **Honest F-1 replacement**: the one NEW failed name was repaired through the guard owner's declared registration, and the whole-suite reading was re-taken and replaced — not suppressed.
- **ARC-first design**: the closure checker's `final_path` record (8/8 final pass) was produced by the implement stage before the status flip, so this review only confirms agreement.
- **Composed-review non-interactive path**: `base`/`start`/`note`/`receipt`/`report`/`capture` gave a reproducible 182/19/163/0 receipt and a `blocking`-only gate without hand-written counts.
- **Distribution verified twice**: mirror parity (`sync-mirrors.py --check`, 134 + 123 files), command-copy parity, and a fresh-init fixture; this review re-ran the parity checks and they stayed green.

## 5. spec-kit / SDD Improvement Recommendations

### 5.3 Automation / Script Improvements

- **REC-A1 — in-place requirements scaffold** — Target: `scripts/bash/create-new-requirements.sh` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/prompt-adherence/scripts/bash/create-new-requirements.sh`). Change: add an explicit `--feature-id/--branch` in-place mode that scaffolds `requirements.md` on the current branch without number derivation or branch creation, and name it in the requirements stage brief. Source: F1. Expected impact: removes the per-line manual scaffold and its template-fidelity hand-check (second occurrence after 108 A-16).
- **REC-A2 — declare the checklist stage's gate posture** — Target: `shared/declarations/facts/driver-gate-roster.yaml` (stage matrix) and `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` (`--stage` choices derive from it). Change: either add a `checklist` row or record the intentional absence in the driver's stage table. Source: F2. Expected impact: one less dead gate call and one less bespoke note per checklist run.

### 5.5 Documentation Improvements

- **REC-D1 — surface the Shared-Strings registration at authoring time** — Target: `skills/internal/implement-feature/SKILL.md` (guard roster) plus the owner-document authoring checklist (absolute supplement under the worktree root). Change: name the drift-guard whitelist registration whenever a new `shared/definitions/` document cites `shared/guidelines/bilingual-expression.md`. Source: F3. Expected impact: avoids one full-suite re-read per new owner document (76 s at the current suite size) and removes a late surprise.
- **REC-D2 — make the store-layout claim match the delta** — Target: `.specify/specs/109-prompt-adherence/plan.md:34`, `requirements.md:44`, `contracts/distribution.contract.md:17`. Change: state "no store-set/layout change; a consumer-registration line is added and required by the existing consumer guard" or point at `test-evidence/boundary-readings.txt`. Source: F4. Expected impact: removes the only claim in the artifact set that the tree contradicts.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | REC-A1 — in-place requirements scaffold | `scripts/bash/create-new-requirements.sh` | F1 |
| P2 | REC-A2 — declare the checklist stage's gate posture | `shared/declarations/facts/driver-gate-roster.yaml` + `pre-analyze-check.py` | F2 |
| P2 | REC-D1 — surface the Shared-Strings registration at authoring time | `skills/internal/implement-feature/SKILL.md` | F3 |
| P2 | REC-D2 — make the store-layout claim match the delta | spec `plan.md` / `requirements.md` / `contracts/distribution.contract.md` | F4 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly. No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.