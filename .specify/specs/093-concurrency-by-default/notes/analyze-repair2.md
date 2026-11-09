# Analyze-repair — round 2 (093-concurrency-by-default)

**Stage**: analyze-repair round 2 (the stage implied by analyze round 2's FAIL verdicts)
**Branch / worktree**: `093-concurrency-by-default` @ `.specify/.tmp/sdd-loop/worktrees/093-clarify`
**Base commit**: `780dfa82` (the round-2 verdict record; analyze notes at `notes/analyze-round2/`)
**Date**: 2026-11-09
**Inputs**: `notes/analyze-round2/v2-gates-directive.md` (manifest gap), `notes/analyze-round2/v3-trunk-reconciliation.md` (V3-F1…F9), `notes/analyze-repair.md` (round 1), `requirements.md`, `plan.md`, `tasks.md`, `quickstart.md`, `research.md`, `checklists/2026-11-09-requirements-quality.md`, the six checkpoints, and the measured framework surfaces they name.
**Execution shape of this stage**: serial, one executor. The feature's own mechanism has not landed, so this stage's own record is `mechanism-not-yet-landed` ([[STR-010]]) and SC-006 stays `not_evaluated` — no concurrency is claimed. Framework sources were read, never edited: every surface correction is an implement-stage row.

---

## 0. Repair verdict

**PART A (manifest) CLOSED.** The user ruling is now encoded where the structure requires it: the host-internal in-process subagent path is **BANNED** as a concurrency carrier; the only two legal carriers are the **fork form** (same-family `qodercli` child processes through `skills/external/sdd-loop-driver/scripts/stage-runner.sh`) and the **subprocess form** (heterogeneous agents, each carried by an independent child process of its own CLI). FR-035 now states both carriers and the ban (numbering preserved), C-094 matches it, plan.md names all 20 manifest surfaces, and tasks.md carries **T144–T152** — one row set naming every surface path and carrying the ban plus both carriers. V2's 15 previously-missing surfaces are now covered; the 5 already-covered surfaces keep their original rows.

**PART B (V3) CLOSED.** V3-F1 / V3-F3 / V3-F4 (MEDIUM) and V3-F2 / V3-F5 / V3-F6 / V3-F7 / V3-F9 (LOW) each have one recorded correction and a durable anchor. Dated records were annotated, never rewritten; one live artifact (`quickstart.md` S-6) was corrected in place, as were the stale reasons in the dated checklist items (with dated correction markers).

No gate was weakened, no coverage baseline was frozen, and no framework source was edited.

---

## 1. Complete-correction manifest closure (Part A)

**Judgment rule** (same as V2's): a surface is *covered* only when a plan/tasks row names the surface path and carries the correction content — the ban plus the two carriers.

| # | Surface | V2 severity | Plan anchor | Tasks row | Correction content |
|---|---|---|---|---|---|
| 1 | `skills/external/sdd-loop-driver/SKILL.md` | covered | planned-files list | T139, T142 | unchanged (analyze default + fork mechanism) |
| 2 | `.../references/dispatch-recipes.md` | covered | planned-files list | T139, T142 | unchanged |
| 3 | `.../references/watch-model.md` | MEDIUM | planned-files list | **T146** | watch model extended to the local fork carrier; in-process path is not a carrier |
| 4 | `.../references/decomposition-model.md` | covered | planned-files list | T140 | unchanged |
| 5 | `.../references/stage-prompts.md` | MEDIUM | planned-files list | **T146** | two-topology rule becomes fork / subprocess; ban stated |
| 6 | `.../templates/stage-team-preset.md` | covered | planned-files list | T116, T133 | unchanged |
| 7 | `skills/external/sdd-house-keeping/SKILL.md` | HIGH | planned-files list | **T144** | "MUST NOT 启动 qodercli" (~L109/L140/L144) inverted; fork default + subprocess for heterogeneous; in-process BANNED |
| 8 | `skills/external/sdd-house-keeping/references/maintenance-recipes.md` | HIGH | planned-files list | **T144** | H2 Carrier line (~L35) -> fork / subprocess; ban stated |
| 9 | `skills/external/sdd-project-setup/SKILL.md` | HIGH | planned-files list | **T145** | "MUST NOT 启动 qodercli" (~L57/L59/L73/L104) inverted; fork default + subprocess; in-process BANNED |
| 10 | `skills/external/sdd-project-setup/references/setup-recipes.md` | HIGH | planned-files list | **T145** | Carrier paragraph (~L109) -> fork / subprocess; ban stated |
| 11 | `skills/external/coaching-skills/SKILL.md` | MEDIUM | planned-files list | **T147** | "host-native first" (~L276) replaced by fork / subprocess; ban stated |
| 12 | `skills/internal/analyze-artifacts/references/validation-and-report.md` | MEDIUM | planned-files list | **T148** | Dispatch carrier paragraph (~L36) -> the two carriers + ban |
| 13 | `shared/workflow/execution-topology.md` | MEDIUM | planned-files list | **T149** | local carrier bullet (~L33) -> fork / subprocess; ban stated |
| 14 | `shared/workflow/external-dispatch-recipes.md` | MEDIUM | planned-files list | **T150** | SDD boundary (~L18) + Recipe 7 (~L91) -> the two carriers + ban |
| 15 | `shared/definitions/agent-definitions.md` | MEDIUM | planned-files list | **T151** | execution layer names the carrier; in-process ban pinned |
| 16 | `shared/definitions/subagent-definitions.md` | covered | planned-files list | T037, T060, T099, T132 | unchanged |
| 17 | `tests/contract/test_sdd_loop_driver_skill.py` | MEDIUM | planned-files list | **T152** | re-pin the ban + fork/subprocess carriers |
| 18 | `tests/contract/test_sdd_project_setup_skill.py` | MEDIUM | planned-files list | **T152** | same |
| 19 | `tests/contract/test_coaching_run_contract.py` | MEDIUM | planned-files list | **T152** | same |
| 20 | `tests/contract/test_sdd_carrier_contract.py` | MEDIUM | planned-files list | **T152** | same |

Counts: **20 / 20 covered** (was 5 / 20). Rows added: T144–T152 (nine rows; T144/T145/T146 cover two surfaces each, T152 covers four modules).

**Plan-side encoding.** `plan.md` § Source Code (repository root) now lists every one of the 15 previously-omitted surfaces, and a new subsection — `§ The analyze wave and its fork mechanism` → **Complete-correction manifest** — carries the ruling sentence (ban + two carriers) and the closed 20-row table mapping surface → severity → row → correction content. `plan.md` § Scale/Scope was updated to include the dispatch-declaring surfaces and the four re-pinned framework modules.

**Requirement/contract encoding.** FR-035 now reads: independent-child-process form, exactly two legal carriers (FORK same-family default; SUBPROCESS heterogeneous), host-internal in-process fan-out **BANNED** (neither a default nor a degradation option), both carriers falling under FR-005(d)'s external-process branch, and the mechanism owners named for both. C-094 was brought into the same shape in `contracts/high-order-executors.contract.md`. FR numbering is unchanged (FR-001…FR-035); no new clause id was coined.

**Clause attribution note.** T144–T152 carry **no** `[green:]` tag: the tag is the red-first marker for the row that first turns a module or fact green (DoD-1, the F-093-004 ruling), C-094 is already claimed exactly once by T142, and claiming it again would trip `green-clause-collision`. Each new row instead cites `(FR-035, C-094)` in its own text, the same shape T143 already uses.

---

## 2. V3 findings closure (Part B)

| id | severity | fix shape | anchor |
|----|----------|-----------|--------|
| V3-F1 | MEDIUM | **Dated correction appended, body intact**: the clarify Q/A at `requirements.md` L307 (and L293, the path half) keeps its text; a correction blockquote below it states that `.specify/goal/<slug>/` was renamed to `.specify/anchoring/<slug>/goal.md` by 090, and that the 持久/临时 lifetime reading is retired — scope is storage location, not lifetime (FR-032 / `goal-definitions.md`). Alignment target: FR-032 continuation at `requirements.md` L185 | `requirements.md` § Clarifications, correction note after the goal-layer bullet |
| V3-F2 | LOW | same correction note (path-only, L293) | same |
| V3-F3 | MEDIUM | `quickstart.md` S-6 rewritten in place: the reason is now `mechanism-not-yet-landed` (the facts, the engine, the FR-035 runner path), explicitly not the host's tool set; F-093-012 cited. Checklist CHK043's stated reason replaced with the same reading, marked as a dated correction (verdict stays `not_evaluated`; no item was re-scored) | `quickstart.md` § S-6; `checklists/2026-11-09-requirements-quality.md` CHK043 |
| V3-F4 | MEDIUM | **Dated correction appended**: research R-10 keeps its measured paragraph; a correction blockquote records that the "no dispatch tool" premise was measured false at analyze (F-093-012), and the live reason is the missing mechanism | `research.md` § R-10 |
| V3-F5 | LOW | dated correction notes appended to CHK001 (fifth root is `.specify/anchoring/<slug>/`; count 6 unchanged) and CHK027 (storage-scope reading; lifetime reading retired); item texts retained as dated records | `checklists/2026-11-09-requirements-quality.md` CHK001 / CHK027 |
| V3-F6 | LOW | one dated note below each of the six `## 2. Temporary Goal progress` headings: the shipped protocol now reads "Goal progress" (`skills/external/sdd-loop-driver/references/checkpoint-protocol.md` § 2); bodies untouched | `checkpoints/01…06` |
| V3-F7 | LOW | T135 wording fixed in place: "the spec-local goal layer (a storage scope, not a lifetime — FR-032)" — the ownership statement is unchanged | `tasks.md` T135 |
| V3-F9 | LOW | dated correction notes at both "five checkpoints" / "five consecutive stages" claims: measured, checkpoints 03/04/05 carried the tool-set claim; 01/02 recorded serial from a different, valid reason | `notes/analyze-findings.md` § 3 disclosure + § 5 item 6 |

V3's non-findings were left untouched: `plan.md` T-002's "临时 team" (the cited framework page still defines the term — trunk-side divergence), `research.md` R-14 (describes the 092/fixture shape), and every `test-evidence/*` old-path capture (dated evidence).

---

## 3. Verification-local ids and promotion mapping

V3-F1…V3-F9 are **verification-local ids** (`notes/analyze-round2/v3-trunk-reconciliation.md` § 6 declares them "not registered F-093 ids; promote before citing durably"). This repair cites them durably, so the promotion mapping is recorded here and one grouped register row carries them:

| local id | promoted? | durable anchor |
|---|---|---|
| V3-F1 | no new id — closed in place | `requirements.md` correction note; V3-F1 → FR-032 L185 alignment |
| V3-F2 | no new id — closed in place | same note (path half) |
| V3-F3 | no new id — closed in place | `quickstart.md` S-6; checklist CHK043 dated correction |
| V3-F4 | no new id — closed in place | `research.md` R-10 correction note |
| V3-F5 | no new id — closed in place | checklist CHK001 / CHK027 dated corrections |
| V3-F6 | no new id — closed in place | six checkpoint heading notes |
| V3-F7 | no new id — closed in place | `tasks.md` T135 |
| V3-F9 | no new id — closed in place | `notes/analyze-findings.md` two dated corrections |
| V2 manifest gap (15/20) | promoted to implement rows | `tasks.md` T144–T152; `plan.md` manifest table |

Register row: `.specify/memory/register.md` — a single grouped row (`V2/V3@093-analyze-round2`) points here; no new `F-093-*` number was coined because every item closes inside this repair, and coining ids for closed verification notes would bloat the register without a consumer.

---

## 4. Gate readings (post-repair, explicit flags)

Full command lines, stdout/stderr and exit codes are retained under `test-evidence/analyze-repair2-*`.

| # | Gate | Reading | Verdict |
|---|------|---------|---------|
| G1 | `validate-requirements.py requirements.md` | `status: ok` — `[id-contiguous]` `[doc-order]` `[ref-resolvable]` `[marker-count]` `[dup-id]` `[path-marker]` all `pass (0)`; scanned 337 lines, 47 definition rows, 11 shared strings; **0 error / 0 warning**, EXIT 0 | PASS |
| G2 | `account-clause-coverage.py <spec-dir> --corpus-root <worktree>/.specify/specs` (no `--freeze`) | `status: baseline-missing`; **`[fr-uncovered] pass (0)` — 35 of 35 FRs cited from citation groups**; `[clause-uncovered] fail (656)`, `[clause-unparsable] fail (116)`, `[coverage-baseline-delta] fail (656)`; 657 errors / 1 warning, EXIT 2 — the clause lane's declared expected state (no baseline exists; T006 owns it) and the baseline file was **not** created here | PASS on the FR lane; clause lane red-by-baseline-missing, expected |
| G3 | `validate-tasks.py tasks.md` | `PASS — 0 error(s), 0 warning(s)`, EXIT 0 (152 rows; G6 confirms the count) | PASS |
| G4 | `validate-decision-tensions.py --spec <spec-dir>` | `status: ok` — all six rules `pass (0)`; scanned 466 lines, 5 records T-001…T-005; **0 error / 0 warning**, EXIT 0 | PASS |
| G5 | `pre-analyze-check.py --repo <worktree> --spec-dir <spec-dir> --stage requirements` / `plan` / `tasks` | all three `decision=pass`, **0 errors**, 112 advisories (every one a creation-target path or a dated-history path; one more than the prior run's 111 — the new CHK001 correction note repeats the retired `.specify/goal` token), `fr=35 / sc=12 / tasks=152`, EXIT 0 | PASS |
| G6 | `decomposition-check.py --mode tasks --requirements … --tasks …` | `{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 35, "task_count": 152, "fr_ceiling": 120, "task_ceiling": 160}, "reasons": []}`, EXIT 0 | PASS |

Evidence files: `test-evidence/analyze-repair2-validate-requirements.txt`, `…-account-clause-coverage.txt`, `…-validate-tasks.txt`, `…-decision-tensions.txt`, `…-pre-analyze-{requirements,plan,tasks}.txt`, `…-decomposition-tasks.txt`. Every earlier green reading stayed green; no gate was weakened and no baseline was frozen.

---

## 5. Fast-fail decisions in this pass

**Repaired in passing, disclosed** (each is one reading of the already-recorded ruling):
1. C-094 was updated with the same subprocess carrier. The ruling names two carriers; leaving the clause at fork-only would have made the requirement and its contract clause disagree in the same change.
2. `plan.md` § Scale/Scope and the planned-files tree were updated so the manifest enumeration is reachable from the plan's own inventory (V2 noted the plan side omitted the same surfaces).
3. `tasks.md` work-package table and row counts were updated (143 → 152; T144–T151 folded into `WP3-owners`, T152 into `WP4-tests`) so "every row appears in exactly one package" stays true.
4. T135's retired adjective was corrected in place; the ownership statement is unchanged (V3-F7).
5. The checklist CHK043 reason was corrected with a dated correction marker while the verdict `not_evaluated` and the item score stand (the checklist is dated; the correction follows the annotation shape the prior repair used for the header count note, not a re-scoring).

**Refused (surfaced, not absorbed)**:
1. Editing any of the 15 framework surfaces in place — outside the spec dir; the ruling's landing is implement-stage work and is now carried by T144–T152.
2. Rewriting dated records (checkpoint bodies, clarify Q/A, research R-10, analyze-findings items) — dated corrections were appended instead.
3. Running `account-clause-coverage.py --freeze` — the clause lane stays red-by-baseline-missing by design; freezing answers a different question and was refused in both earlier passes.
4. Editing the four framework contract tests now — framework source, and tests are T152's subject.

**Anomaly line**: **ANOMALY: none unreported.** The known residuals are disclosed in § 6, not buried: the framework's own rule text still contradicts the ruling until implement lands T144–T152 (expected — analyze may not edit framework source), and the spine's recorded `execution_topology: local-native-subagents` is this line's runtime topology, not the feature's concurrency mechanism.

---

## 6. Residual risks

- **The old rule still ships until implement.** The 15 surfaces (and the four contract tests pinning them) still read "MUST NOT start qodercli locally" / "host-native first" in the framework. That is the intended state for a repair pass; the rows are named, attributed, and packaged (WP3-owners / WP4-tests). If implement skips them, analyze round 3 must judge the manifest rows, not the framework text.
- **The four contract tests are the drift guard.** Until T152 lands, the suite actively enforces the pre-ruling text. A run of `pytest -m contract` is expected green now; after T152 it must stay green under the inverted assertions. A red after T152 means an unstated old-rule pin survived — treat as a finding, not a flake.
- **Heterogeneous-agent carrier is form-only.** FR-035 / C-094 now state the subprocess carrier's judgement (independent process, intervals, sentinel-or-exit completion); no engine consumes it yet. T143's fork contract does not yet assert the subprocess arm — T152 re-pins the framework tests, and the new clause becomes machine-checkable only when the corresponding test row is added at implement. Recorded rather than pretended.
- **Spine topology field.** `project_config.execution_topology: local-native-subagents` records how this line was run, not the feature's mechanism. It is left unchanged; changing it would falsify the run record.
- **Dated notes are invisible to the blockquote-blind validators** (framework observation, unchanged): the corrections are durable for readers, not machine-scanned. That is acceptable because no gate asserts on them, but a future checker that reads blockquotes would surface new strings.
