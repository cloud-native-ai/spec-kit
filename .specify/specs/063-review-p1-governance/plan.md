# Implementation Plan: Review P1 Governance（评审 P1 治理）

**Branch**: `063-review-p1-governance` | **Date**: 2026-10-19 | **Spec**: `.specify/specs/063-review-p1-governance/requirements.md`
**Requirement → Feature**: `063-review-p1-governance` → Feature 063 Review P1 Governance（评审 P1 治理）
**Input**: Specification from `.specify/specs/063-review-p1-governance/requirements.md` (clarify complete: E1/E2 settled, Feature 063 bound)

## Summary

Turn the six P1 and two P2 findings of the 062-humanize-command process review (`.specify/specs/062-humanize-command/review.md` § 3, F1–F8) into framework-mechanism fixes on the framework-source side (`shared/` `templates/` `skills/` `scripts/` `tests/`), never instance repairs of 062: (F1) declare the citation-group paren charset in its owner and honor both widths in the extractor, wire the clause-coverage lane into `/speckit.analyze` and freeze `coverage-baseline.txt` in `/speckit.tasks`; (F2) make analyze consume checklists (`Gap` items raised or deterministically dispositioned), land the append-only recheck form and the four-part waiver format (061 REC-C5/C6); (F3) give review recommendations a persistent life — same-commit `register.md` registration, `REC-` in the ambient ID Register, a named legal feedback intake, repo-relative-first REC targets, and a `/speckit.review` transition row (E2); (F4) make compiled wrap-up faces executable as written — engine-derived argument manifests, placeholder convention, all-missing-args-at-once engine errors, idempotency untouched (E1), full recompile with the 2026-10-15 backlog row closed; (F5) open the environment-premise carrier list; (F6) bind every `pass` claim to a structured, hash-pinned archived-evidence record checked by a registered gate; (F7) mirror the frozen-baseline re-capture duty onto the implement consumer with four-way drift classification; (F8) require verbatim gate-row quotes in red-first notes. 30 FRs → 34 contract clauses (30 mechanism + 4 cross-cutting) → per-mechanism contract tests with mutation drills; no new subsystems, stores, or dependencies (宪法 IX/XIII).

## Technical Context

**Language/Version**: Python ≥3.8 (engine scripts under `scripts/python/`), Markdown (templates/skills/shared), Bash (workflow scripts)
**Primary Dependencies**: pytest (contract/integration markers) via `scripts/bash/run-tests.sh`; existing engines only — `probe-utils.py`, `run-determination.py`, `feedback-utils.py`, `exec-quant.py`, `account-clause-coverage.py`, `clause_extract.py`, `sync-mirrors.py`, `regen-command-copies.py`, `generate-instructions.sh`
**Storage**: file-based project memory and spec artifacts only; **no new store** (REC uses existing `register.md` pointer rows; evidence uses the verification log template; 宪法 IX)
**Testing**: pytest contract tests (each mechanism gets a pin; negative propositions get mutation drills per FR-027); frozen failed-tests baseline: **63 names** (`.specify/specs/063-review-p1-governance/notes/baseline-failed-tests.txt`, captured 2026-10-19 before any change)
**Target Platform**: this repo's framework sources plus their generated runtime copies (`.specify/` via sync/init flows; per-tool command copies via regen)
**Project Type**: framework source (documentation/prompt framework with Python automation); self-hosting client (two hats — all edits land in sources, FR-026)
**Performance Goals**: N/A (governance feature, no runtime performance surface)
**Constraints**: no new external service/network/model API/third-party dependency/background process (FR-028); 062's `requirements.md`/`plan.md`/`tasks.md`/`review.md` frozen as evidence (FR-029); counts/enumerations program-derived or owner-referenced (FR-030); templates/mechanism edits justified through the constitution rows below
**Scale/Scope**: ~23 deliverable framework files, 34 contract clauses in 4 contract files, 11 quickstart scenarios, 13 design entities

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md` v1.13.0, principles I–XVI):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every mechanism edit traces to FR-001..FR-030; traceability in `feature-ref.md` FR→clause map |
| II | Feature-Centric Development | ✅ Pass | Feature 063 bound at clarify; index row + detail exist; this plan advances Draft → Planned only (state machine) |
| III | Intent-Driven Development | ✅ Pass | Design fixes mechanisms (what/why in requirements; contracts state normative behavior before implementation) |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | FR-027 mandates per-mechanism contract tests + mutation drills, sequenced before their subjects in tasks; baseline frozen pre-change |
| V | AI Agent Integration Standards | ✅ Pass | No agent roster/config changes; `AGENT_CONFIG`/`_ASSISTANT_TIERS` untouched |
| VI | Continuous Quality & Observability | ✅ Pass | Faces become executable (运行判定 sensor restored); engines report all missing args at once; root-cause fixes, not symptom patches |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Workflow gates: reuse-first honored (new Feature 063 justified at clarify after 5-candidate scan); no status regression (Draft→Planned forward); template-only gate not needed — feature includes executable code, so IV stands Pass |
| VIII | Code as the Single Source of Truth | ✅ Pass | Arg sets derived from engine parsers (C-22); two requirement premises corrected against code (C-18 note-owner, C-27 GATE-8→Step 9), disclosed in `research.md` D-9/D-10 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | No new subsystem/store/engine/scorer: reuses register.md rows, existing gate-probe mechanism, existing A3 introspection path; the args-manifest action extends existing engines (mandated by FR-030), it does not add infrastructure |
| X | Documentation Naming & Location Conventions | ✅ Pass | No new document names; spec artifacts follow the standard spec-dir layout; all edits stay at registered locations |
| XI | Dogfooding (Self-Application) | ✅ Pass | Every fix lands at the producing mechanism (fix-the-mechanism); two-hats respected — sources edited, runtime copies synced; this feature itself runs the SDD workflow |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses run-tests.sh, sync-mirrors.py, regen-command-copies.py, generate-instructions.sh, probe-utils.py, account-clause-coverage.py; no new helper scripts planned |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Dimension mapping: Change Validation (F1/F6/F7), Reliable Delivery (F4), Learning Capture (F3), Task Understanding (F2/F5/F8); no scoring/maturity machinery added |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | Charset declared once in owner; manifests parser-derived; baseline sets directory-derived; REC row form referenced not restated; register/backlog own their forms |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | Faces gain one placeholder-convention line; engine errors name every missing flag in one message; this plan/quickstart carry their own context with path references |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | Malformed groups reported not silently counted; `undecidable` drift class with no guessing; unevidenced pass = unverified; baseline-missing surfaced with remedy; no silent mirror fallback in the renderer |

**Gates Status**: ✅ All gates pass — no Fail/Partial rows.

**Re-check after Phase 1**: 2026-10-19 — re-scored against the landed design artifacts (`data-model.md`, 4 contract files, `quickstart.md`, `feature-ref.md`, `research.md`) by a fresh-context read-only subagent per the same-author gate (mixed set: requirements authored by a prior dispatch, design authored this session — the self-authored design subset was delegated; see § Same-Author Delegation Record). Constitution verdict: 16/16 rows CONFIRM, 0 overturns. The same delegation's contract audit returned 7 findings; all were repaired in this commit and are recorded with their dispositions in § Delegation findings.

## Same-Author Delegation Record

Condition held for the design subset (plan + Phase 1 artifacts authored by this session). Per `.specify/shared/workflow/objective-analysis-gate.md`, scoring of the Constitution Check rows and the contract-artifact set was delegated to fresh-context read-only subagents (disjoint scopes: (1) constitution-row verdicts vs the landed artifacts; (2) contract-artifact audit — deliberation markers, clause form, citation-group resolution, FR/SC coverage). Result recorded at the Post-Generation Quality Gate below.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/063-review-p1-governance/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output — decisions D-1..D-13 + measured current state (standalone: >50 lines)
├── requirements.md      # /speckit.requirements output (upstream, committed)
├── checklists/          # requirements checklist (upstream)
├── data-model.md        # Phase 1 output — 13 design entities
├── contracts/           # Phase 1 output — 4 files, 34 clauses
├── quickstart.md        # Phase 1 output — 11 scenarios (S0–S10)
├── feature-ref.md       # Phase 1 output — FR/SC maps + deliverables + baselines
├── notes/               # baseline-failed-tests.txt (frozen 2026-10-19, pre-change)
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md     # Implementation output (/speckit.implement command)
```

### Source Code (repository root)

```text
shared/definitions/               # contract-clause-definitions.md (F1 owner), probe-definitions.md (F4 registry, F6 gate row)
shared/workflow/                  # feedback-step.md (F3 entry), feature-integration.md (F3/E2 transition row)
skills/internal/analyze-artifacts/    # checklist load + Gap pass + coverage lane (F1/F2)
skills/internal/create-checklist/     # recheck form (F2, REC-C5)
skills/internal/create-tasks/         # coverage freeze + carriers + re-freeze pointer + red-first quote (F1/F5/F7/F8)
skills/internal/implement-feature/    # Step 2 branches + waiver format + Step 9 gate + pre-flight (F2/F6/F7)
templates/commands/               # analyze.md, review.md, implement.md (command faces for F1/F2/F3/F7)
templates/                        # tasks-template.md, verification-log-template.md, review-template.md, instructions-template.md
scripts/python/                   # clause_extract.py, probe-utils.py, run-determination.py, feedback-utils.py, exec-quant.py
tests/contract/                   # per-mechanism pins + mutation drills (clause forms/coverage, engine face, transition table, mirror guards)
.specify/memory/feedback/backlog.md   # 2026-10-15 row flips closed with the recompile (C-25)
```

**Structure Decision**: extends the existing framework-source layout in place — no new top-level directory, no new file families; the only new artifacts are contract tests under `tests/contract/` and (at implement) the engine args-manifest actions inside existing scripts. Runtime copies are generated, never hand-edited.

### Mirror Obligations *(mandatory — measured baselines below)*

Pre-change baselines (2026-10-19): `regen-command-copies.py --check` → **clean** (all per-tool copies match). `sync-mirrors.py --check` → **202 pre-existing DIFF entries** (includes `shared/workflow/feature-integration.md` and `feedback-step.md`, both in this spec's edit set). Criterion: **no NEW drift on any pair**; for the pairs this spec touches, the tasks-stage sync lands source→mirror and thereby clears those pairs' pre-existing drift (mandated runtime landing per FR-026); drift elsewhere is out of scope. `probe-utils.py --action compile-embeds --check` → **74 units, zero drift** pre-change; post-change all units recompile (C-25) and `--check` returns to zero drift.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `templates/commands/analyze.md`, `review.md`, `implement.md` | `.claude/commands/speckit.<stem>.md`; `.qoder/commands/speckit.<stem>.md`; `.opencode/command/speckit.<stem>.md`; `.github/prompts/speckit.<stem>.prompt.md` — via `regen-command-copies.py`; NO `.specify/templates/commands/` mirror (retired) | `regen-command-copies.py --check` vs pre-change clean baseline — no NEW drift; regenerated copies contain the edit |
| `templates/tasks-template.md`, `verification-log-template.md`, `review-template.md` | `.specify/templates/<same>` via `sync-mirrors.py --write --only templates` | `sync-mirrors.py --check --only templates` — no NEW drift vs the 202-entry baseline |
| `templates/instructions-template.md` | `.specify/templates/instructions-template.md` (mirror) + generated `.specify/instructions.md` via `generate-instructions.sh` (symlink set unchanged) | generator run; `grep -n "REC-" .specify/instructions.md` finds the enumeration; `git diff` on the symlinks empty |
| `skills/internal/{analyze-artifacts,create-checklist,create-tasks,implement-feature}/SKILL.md` | `.specify/skills/internal/<same>` via `sync-mirrors.py --write --only skills/internal` | `sync-mirrors.py --check` — no NEW drift on these pairs |
| `shared/definitions/{contract-clause-definitions,probe-definitions}.md`; `shared/workflow/{feedback-step,feature-integration}.md` | `.specify/shared/<same>` via `sync-mirrors.py --write --only shared` (these two workflow pairs already drift pre-change — sync clears them) | `sync-mirrors.py --check` — no NEW drift anywhere; touched pairs byte-identical after write |
| `scripts/python/{clause_extract,probe-utils,run-determination,feedback-utils,exec-quant}.py` | `.specify/scripts/python/<same>` via `sync-mirrors.py --write --only scripts` | `sync-mirrors.py --check` — no NEW drift |
| `shared/definitions/probe-definitions.md` (registry edit) → ALL compiled `## Wrap-up` faces | every `templates/commands/*.md` + every `skills/**/SKILL.md` compiled section, via `probe-utils.py --action compile-embeds` | `compile-embeds --check` zero drift after recompile; `--reconcile` where reconcile guards demand; fixed order compile → regen → sync |

## Complexity Tracking

N/A — Constitution Check has no Fail/Partial rows; no justification table needed.

## Phase 0: Research Review

No standalone research input existed at start; a dedicated exploration pass (Explore subagent sweep + targeted verification reads) produced decisions D-1..D-13 with measured current state — recorded in `research.md` (standalone file; >50-line threshold). Key measured anchors: coverage lane dark (`status: baseline-missing`, 512 errors on 062; only 053 owns a baseline), renderer emits two flags for engine lines, engines fail one missing arg at a time (exit 2), checklist blind spot confirmed (`grep -c checklist` = 0 on the analyze surfaces), register.md holds zero `REC-` rows, transition table lacks the review row, mirror drift = 202 pre-existing DIFF entries, regen copies clean, test baseline = 63 failed / 3954 passed. Two requirement premises were corrected against code (C-18 note-shape owner; C-27 GATE-8→Step 9 anchor) and one label modernized (C-13 "Mode 5"→A3 自省) — all disclosed in `research.md` and at wrap-up. No unresolved unknowns remain; no interview-pattern round was needed (all plan-level decisions are mechanism-derivable, `research.md` D-13).

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | `data-model.md` | 13 entities (E1–E13) + relationships + 3 state-transition sets |
| Contracts | `contracts/` | 4 files: `template-mechanisms.md` (C-1..C-19), `engine-face-contract.md` (C-20..C-25), `evidence-baseline-contract.md` (C-26..C-30), `cross-cutting-constraints.md` (C-31..C-34) — 34 clauses, all `md-bold-closed`, FR-001..FR-030 fully cited |
| Quickstart | `quickstart.md` | 11 scenarios (S0 current-state + S1–S10), every emitted command executed at plan or premise-declared |
| Feature ref | `feature-ref.md` | FR→clause map (30 rows), SC→verification map (14 rows), 23 deliverables, 4 frozen baselines, 3 shared strings |
| Research | `research.md` | 13 decisions (D-1..D-13) with measured evidence |

Counts taken from the landed files (grep/section census at fill time), not pre-written.

## Post-Generation Quality Gate

- **Deliberation-marker scan**: all four Phase 1 artifacts + plan scanned for internal deliberation markers ("Wait —", "Actually,", "I think", self-correction prose); the contract files read as declarative specifications. One narrative footnote retained deliberately: C-18's *Owner-file note* — it is a disclosure of a requirement-premise correction (an obligation under the fast-fail discipline), not leaked reasoning.
- **Execution-verify**: commands emitted into plan/quickstart were either executed during this phase with real output pasted (S0's four runs; the pre-change mirror/regen baselines; `backlog.md` line-89 verification via the exploration pass) or carry per-example premise declarations in `quickstart.md` (S1–S10) naming exactly which facts `/speckit.tasks`/`/speckit.implement` must re-measure — the mechanisms do not exist yet, and a file-level disclaimer would silently vouch for them, so each scenario declares its own premises. The engine-face example in `contracts/engine-face-contract.md` is explicitly labelled a shape target, with the real pin delegated to contract tests (SC-007's verbatim-execution check).
- **Same-author delegation result**: fresh-context read-only subagents scored (1) the 16 Constitution Check rows against the landed artifacts and (2) the contract set (deliberation markers; canonical clause form; `[[STR-NNN]]` resolution; FR/SC coverage completeness). Findings and dispositions are appended below.

### Delegation findings (2026-10-19)

**Scorer (Constitution Check rows vs landed artifacts)**: 16/16 rows CONFIRM, 0 overturns. One process anomaly flagged and repaired in this commit: this plan had asserted the re-check verdict ("verdicts unchanged") above before the findings section existed; § Re-check after Phase 1 now states the verdict only with the delegation record as its evidence.

**Contract auditor (clause form, citation groups, coverage, cross-references)** — 7 findings, all accepted and repaired in this commit:

1. *(high)* All 30 clause markers used the legacy `md-bold-paren` form (`**C-N — label（FR-…）**:`) while the files claimed canonical `md-bold-closed` — verified by the scorer executing `clause_extract.form_of`. **Repaired**: all 30 markers rewritten to `**C-N**: label`; extractor re-run confirms `md-bold-closed` on all four files.
2. *(high)* All 30 clauses cited ZERO FRs — the FR ids sat in label parentheticals (mentions) while the last FR/SC-bearing group of every block was the trailing `(SC-0NN)`; verified by executing the extractor's citation-group rule. 063 would have failed its own C-5/SC-002 coverage gate at implement. **Repaired**: every clause's citation group rebuilt as the trailing `(FR-…, SC-…)` group of its block; label FR groups stripped (E-mixed labels keep their ruling mention, e.g. `（E1 裁决）`).
3. FR-026..FR-029, SC-013, SC-014 were cited by no clause. **Repaired**: new `contracts/cross-cutting-constraints.md` with C-31 (two-hats sync, FR-026/SC-013/SC-014), C-32 (per-mechanism tests + mutation drills, FR-027/SC-013), C-33 (zero new deps/network/daemons, FR-028/SC-013), C-34 (062 artifacts read-only, FR-029/SC-014). Live accountant after repair: `[fr-uncovered] pass (0) — 30 of 30 FRs cited`. Note for `/speckit.tasks`: the four new clauses MUST be claimed in tasks.md (clause-uncovered lane).
4. feature-ref FR-021 row cited C-26 and FR-030 row cited C-7 — C-26 does not carry FR-021 (its red-semantics home is C-28), and C-7's citation group lacked FR-030. **Repaired**: FR-021 row → C-28 only; C-7 and C-29 citation groups extended with FR-030 (both genuinely carry the derived-not-restated duty).
5. quickstart S8 said "three `pass` samples" while listing four. **Repaired**: count corrected to four.
6. data-model E9 carried a spurious `[[STR-003]]-independent` bracket aside (deliberation residue; [[STR-003]] is unrelated to the backlog row). **Repaired**: aside removed.
7. feature-ref STR-001 "Where" column listed C-28, which never references the `gate-implement-evidence-binding` string. **Repaired**: corrected to C-27 + the probe-definitions row.

**Downgrade rate**: 0 of 7 findings downgraded by validation — the auditor's two high findings carried machine evidence (extractor execution), and the scorer's row-by-row check confirmed rather than overturned. Per objective-analysis-gate rule 6 this near-zero downgrade rate is read against the fact that detection did surface 7 real defects: the artifacts were not clean, and the delegation earned its cost.

**Propagation surfaces**: findings 1–2 propagated to all 30 clauses (all repaired in place); finding 3 propagated to coverage accounting and the tasks-phase claim set (disclosed above); findings 4–7 were single-artifact. No downstream artifact outside this spec's Phase 1 set inherited any of the defects.

## Plan integrity gate

- [x] No residual `[UPPER_SNAKE_CASE]` placeholder tokens (self-referential template Note line removed)
- [x] Exactly one top-level `# Implementation Plan:` heading — no duplicated template body
- [x] `**Requirement → Feature**` stamp present (`063-review-p1-governance` → Feature 063)
