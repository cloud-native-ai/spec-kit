# Plan Stage Record — 107-decision-governance

- **Stage**: plan · attempt 1 · 2026-11-25
- **Line / run**: `decision-governance` / `r20261125T134500Z-107a`
- **Baseline commit**: `08b59695c` (branch `107-decision-governance`; worktree `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/decision-governance`)
- **Assignment**: execute the plan workflow (`skills/internal/create-plan/SKILL.md`, `/speckit.plan`) for spec 107 — full plan set (`plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, `feature-ref.md`), Constitution Check, Decision Tensions, Execution Premises, the nine design obligations of the brief, deterministic gates and the stage wrap-up accounting.
- **Execution class**: direct; no subagents dispatched; no user questions; no state-spine writes; no push.
- **Concurrency reading**: `requested=1`, `effective=not_evaluated`, `effective_reason=single-unit` (a single bounded unit has no dispatch/settle interval pair to measure; `single-unit` is a member of `shared/declarations/facts/serial-reason.yaml`).

## Phase 0 — measured before any design claim

`research.md` carries the full table (M-1…M-16). Key readings: no decision owner page exists; instruction template has 38 top-level sections and none names decisions; live instructions 38,894 B vs budget 38,912 B with `over` firing at `size >= budget` (17 admissible bytes); generator reconciles whole sections only; mirror pairs measured from `MIRROR_PAIRS`; mirror and copy checks rc 0 baselines; gate scanner 31 blocking gates / 0 violations; legacy corpus 101 `T-NNN` headings / 127 checkpoints / 43 run reports; 39 pre-existing `### D-…` headings in one/two-digit forms and **zero** three-digit record-form headings.

## Design obligations of the brief — how each was resolved

| # | Obligation | Resolution (artifact) |
|---|------------|----------------------|
| 1 | Decision record contract, one owner, no second store | R-1 + R-2 in `research.md`; owner-page section plan; `contracts/archive-and-audit.contract.md` C-201…C-208; field closure = FR-014's ten + two conditional identity fields (`same_name_conflict`/`resource_locator`) + `superseded_by`; register stays the sole id index |
| 2 | Per-class text and option specification | `contracts/text-and-options.contract.md` C-101…C-109; options closed with five elements, `other` path, `forced` |
| 3 | Transmission and implementation | `contracts/transmission-and-implementation.contract.md` C-301…C-308; decision block in the existing payload (seven role fields + four injections unchanged); ack + `implementation_receipt`; silent re-decision = explicit anomaly |
| 4 | Archive and audit | `contracts/archive-and-audit.contract.md` C-201…C-208; reconstructability from register + carriers; legacy read-only |
| 5 | M/B enforcement boundary | `contracts/enforcement-boundary.contract.md` C-401…C-407; M-01…M-08 with one judge action and a reverse sample each; B-01…B-06 named surfaces, no machine claim |
| 6 | Landing and two hats | `plan.md` § Project Structure (21 source files) + § Mirror Obligations (every pair and generated copy listed; `docs/` explicitly not shipped) |
| 7 | Data model and contracts | `data-model.md` (9 entities, 14 invariants, one state domain) + 5 contracts |
| 8 | Tests and gates | red-first fixture directories named per M rule; single test entry; targeted set only in this stage |
| 9 | Tensions and premises | 3 `T-NNN` records (T-001 budget/section form; T-002 record grammar; T-003 checker engine) + EP-001…EP-007 (EP-005 falsified with `resolve-in-scope`) |

## Preserved invariants

- **Closed Decision Producer Inventory**: P-01…P-12 unchanged; the plan maps each to its existing carrier and adds no producer.
- **Two decision classes**: `human-interactive` / `ai-autonomous`, by holder (A-4); no third class.
- **M/B boundary**: 8 machine rules / 6 behavior rules exactly as the requirements table; no machine claim on B rules.
- **Legacy rules**: new shape binds only post-landing records; old records readable, `legacy`, zero rewrite; BC-01…BC-06 closed inventory with per-row behavior + test.
- **No second store**: the owner page, carriers and register only; the checker is read-only.
- **Instruction rules**: no command template changed; no new blocking gate; budget ruling recorded (T-001) rather than silently absorbed.
- **Spec shape**: 30 FR / 10 SC / 9 Shared Strings unchanged; `Flow Class: execution` unchanged.
- **This plan's own load-bearing decisions** use the existing `T-NNN` carrier (the `D-NNN` contract binds only post-landing records, A-10); the plan contains no `D-` record block and is not retroactively judged.

## Deterministic gates (all captured under `test-evidence/`)

| Gate | Command | Verdict |
|------|---------|---------|
| Pre-analyze (plan) | `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/107-decision-governance --stage plan --repo <worktree>` | `decision=pass errors=0 advisories=67 waived=0` (34 `external-clause` on the spec-local `BC-NN` ids — the checker reads them as contract-clause references in an external namespace; 33 `missing-path` on the not-yet-created deliverables) — `test-evidence/pre-analyze-plan.txt` |
| Decision-tension validator | `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/107-decision-governance` | `status: ok`, 0 error / 0 warning, 3 records, 217 lines — `test-evidence/validate-decision-tensions.txt` |
| Plan integrity | residual `[UPPER_SNAKE]` tokens / `# Implementation Plan:` count / `Requirement → Feature` stamp / template note removed | none / 1 / 1 / removed — `test-evidence/plan-integrity.txt` |
| Post-generation quality gate | deliberation-marker scan + execution-verify of emitted command examples | markers none; examples executed (39 legacy headings / 0 record-form / 0 base-corpus diffs / sync-mirrors rc 0 / regen-copies rc 0 / gate scan 0 violations) — `test-evidence/post-generation-quality-gate.txt` |
| Mirror baseline | `python3 scripts/python/sync-mirrors.py --check` | rc 0, 6 pairs ok, zero DIFF — `test-evidence/sync-mirrors-baseline.txt` |
| Copy baseline | `python3 scripts/python/regen-command-copies.py --check` | rc 0 — `test-evidence/regen-copies-baseline.txt` |
| Gate baseline | `python3 scripts/python/scan-confirmation-gates.py` | 31 blocking gates (23/7/1), 0 violations — `test-evidence/scan-confirmation-gates-baseline.txt` |
| Workspace signature | `workspace-guard.py --snapshot` … `--check` | before `recorded`; after `status: clean`, `changed: []`, rc 0 (no ref or spec-set drift) — `test-evidence/workspace-plan-before.json`, `workspace-plan-after.json` |
| Overlap (post-plan reading) | `python3 skills/external/sdd-loop-driver/scripts/overlap-check.py --spec-dir … --repo <worktree>` | `decision=overlap overlaps=117`, all against long-completed features; disposition recorded in `feature-ref.md` § 3 (existing owner retained; pointer-only/additive; new files have no prior owner) — `test-evidence/overlap-post-plan.txt` |

## Test budget (E3)

- **Program**: `targeted-set-v1` (TB-05) with `stage_base=08b59695c`.
- **Input**: 14 changed paths (`git diff --name-only --diff-filter=ACMR 08b59695c..HEAD` ∪ `git status --porcelain`), all documentation under `.specify/specs/107-decision-governance/`; **0 executable or test paths changed**.
- **Selection output**: the fixed program was executed and its raw output retained — 380 (a) stem/path candidates, 388 after delivery-surface matching. The set is dominated by generic module stems (`plan`, `research`, `quickstart`, …) matching test file contents; it is informational only because no executable surface changed.
- **Status**: `not-run-docs-only` (TB-06 docs-only clause), six reduced fields recorded in `test-evidence/plan.jsonl`. No full suite, no slot consumed.
- **Observation for the feedback flow** (`token-efficiency`): the TB-05 stem rule is noisy on docs-only stages — a docs-only fast path or an extension filter would avoid computing/reading a 388-candidate set when zero executable paths changed.

## Deviations and corrections (disclosed)

1. **No writability pre-probe**: unlike the requirements/clarify stages, no `test -w` probe was run before the first write; all writes succeeded and the workspace guard stayed clean. Disclosed as a process gap, not repaired retroactively.
2. **Legacy-count first reading was wrong**: an initial grep (`^### D-[0-9]`) was read as "39 two-digit headings". The refined measurement shows **39 pre-existing `### D-…` headings in one/two-digit forms and 0 three-digit record-form headings**; the discriminator was kept and the wording corrected in `research.md`, `data-model.md`, `contracts/archive-and-audit.contract.md` and `quickstart.md`. Exactly one reading is consistent with the recorded intent (legacy corpus untouched); repaired in passing and disclosed here.
3. **`external-clause` advisories on `BC-NN`** (34): the pre-analyze heuristic reads `BC-NN` as a foreign-namespace contract clause; these are the requirements spec's own backward-incompatible change ids, adopted verbatim per FR-029. Advisory only; `--strict` was not requested and no waiver was filed.
4. **Same-author scoring was not delegated**: the plan tool is unavailable to this dispatch (role: no dispatch), so the Constitution Check and the post-generation gate were scored by direct bounded reads and marked in this record rather than by fresh-context subagents (objective-analysis-gate § 7 fallback).
5. **Scaffold**: `create-new-plan.sh --json` resolved the current branch's spec dir correctly (unlike the requirements-stage numbering trap); no manual scaffold was needed.
6. **Feature integration**: the row and detail advance `Draft → Planned`; `Total Features` unchanged (102); no new Feature, merge or deprecation.

## Evidence pointers

- Plan set: `plan.md`, `research.md`, `data-model.md`, `contracts/` (5), `quickstart.md`, `feature-ref.md`
- Registry: `.specify/features.md` (row 107 → Planned), `.specify/features/107-decision-governance.md` (Planned + Latest Review), `.specify/register.md` (T-019…T-021)
- Evidence: `test-evidence/{plan-targeted-set.txt, plan.jsonl, pre-analyze-plan.txt, validate-decision-tensions.txt, plan-integrity.txt, post-generation-quality-gate.txt, sync-mirrors-baseline.txt, regen-copies-baseline.txt, scan-confirmation-gates-baseline.txt, overlap-post-plan.txt, workspace-plan-before.json, workspace-plan-after.json, glossary-proposal-plan-2026-11-25.md}`

## Anomaly line

未发现异常。Three corrections are disclosed rather than surfaced: the initial legacy-count wording (repaired in four files), the advisories on `BC-NN` ids (heuristic false positives, advisory only), and the overlap reading (adjudicated by FR-002's pointer-only architecture and recorded). No destructive action, no dirty-file touch, no state-spine write, no push.

## Re-anchoring record

- After brief + role template + authority artifacts: `on-track`.
- After Phase 0 measurements (budget headroom, whole-section reconcile, zero record-form legacy): `on-track`.
- After the first tension validation and pre-analyze: `on-track`.
- After the legacy-count correction: `correction-applied` (disclosed, one reading).
- After the post-plan overlap reading and adjudication: `on-track`.

## Wrap-up accounting

- **Run Determination**: `run-determination.py --action determine --unit-id skill:create-plan --unit-type skill --run-id r20261125T134500Z-107a --complexity complex --feature 107-decision-governance --feature-id 107 --prev-user-turn-class no_user_input --elapsed-ms <measured> --elapsed-note <basis> --declared-check <the three plan gates> --green-check 3/3` → record path and axes recorded in the close-out receipt.
- **Exec Quant**: `exec-quant.py --action collect --unit-id skill:create-plan --unit-type skill --run-id r20261125T134500Z-107a`.
- **Feedback Record**: `feedback-utils.py --action record --unit-id skill:create-plan --unit-type skill --run-id r20261125T134500Z-107a --feature 107-decision-governance --feature-id 107` (review + points below).
- **Points**: (1) `token-efficiency` — TB-05's stem rule is noisy on docs-only stages (388 candidates computed for zero executable changes); a docs-only fast path is the optimization candidate. (2) `token-efficiency` — batch the pre-analyze runs after the last artifact edit (the mirror-table and legacy-count corrections forced two re-runs).
- **Threshold Notice / Token Reflection / Docs Sync Eval / Closeout**: per the owners named in the command's Wrap-up block; close-out receipt under `.specify/retention/closeout/`.
