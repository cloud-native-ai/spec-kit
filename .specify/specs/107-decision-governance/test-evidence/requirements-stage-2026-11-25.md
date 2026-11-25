# Requirements Stage Record — 107-decision-governance

- **Stage**: requirements · attempt 1 · 2026-11-25
- **Line / run**: `decision-governance` / `r20261125T134500Z-107a`
- **Baseline commit**: `fbab7a45c` (branch `107-decision-governance`; worktree `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/decision-governance`)
- **Assignment**: create the next numbered requirements spec (107) + its requirements-quality checklist via the requirements workflow, treating `.specify/.tmp/sdd-loop/tmp/decision-governance/brief-requirements.md` (worktree-local copy) as the feature description.
- **Execution class**: direct; no subagents dispatched; no state-spine writes; no user questions; no push.

## Artifacts produced

| Artifact | Path |
|---|---|
| Requirements spec | `.specify/specs/107-decision-governance/requirements.md` |
| Requirements-quality checklist | `.specify/specs/107-decision-governance/checklists/requirements.md` |
| Validator capture (verbatim) | `.specify/specs/107-decision-governance/test-evidence/requirements-validator.txt` |
| Pre-analyze gate capture (verbatim) | `.specify/specs/107-decision-governance/test-evidence/pre-analyze-requirements.json` |
| Decomposition gate capture (verbatim) | `.specify/specs/107-decision-governance/test-evidence/decomposition-requirements.json` |
| Workspace signature (snapshot + clean check) | `.specify/specs/107-decision-governance/test-evidence/workspace-requirements.json` |
| Glossary proposal (proposal-only, not written) | `.specify/specs/107-decision-governance/test-evidence/glossary-proposal.md` |
| This record | `.specify/specs/107-decision-governance/test-evidence/requirements-stage-2026-11-25.md` |

## Concept-owner inventory performed before drafting

Located and read (summary-first) before any drafting; each existing owner keeps its facts and receives a pointer line, never a paraphrase:

| Concept area | Owner located | Relationship in the spec |
|---|---|---|
| Whether to ask / authorization axis / decision gate | `.specify/shared/guidelines/confirmation-gates.md` | pointer; class taxonomy is orthogonal (A-4); no new gate (FR-025) |
| Load-bearing tension record (`T-NNN`, six fields) | `.specify/shared/guidelines/decision-tension.md` | cross-reference only; no field duplication (FR-017) |
| Durable identifier registration (`D-…`) | `.specify/register.md` + instructions § ID Register | sole id index (FR-004, FR-015) |
| Correction vs decision; submission/ruling | `.specify/shared/guidelines/fast-fail.md` | decision universe excludes corrections (A-5); divergence uses fast-fail (FR-020) |
| Role edge / downlink / uplink | `.specify/shared/definitions/superagent-definitions.md` | decision block rides the existing payload channel; seven role fields unchanged (FR-018, FR-019) |
| Stage checkpoints | `.specify/skills/sdd-loop-driver/references/checkpoint-protocol.md` | producer P-04, carrier `<spec-dir>/checkpoints/` |
| Analyze dispositions | `skills/internal/analyze-artifacts/SKILL.md` | producer P-05 and behavior review surface B-04/B-05 |
| Review findings/dispositions | `skills/internal/review-feature-quality/SKILL.md`, `skills/internal/review-sdd-process/SKILL.md`, `shared/workflow/acceptance-hardening.md` § Review Composition | producer P-06 and review surfaces B-01…B-06 |
| Goal / anchor / team decisions | `shared/definitions/goal-definitions.md`, `anchor-definitions.md`, `agent-definitions.md` | producer P-08; archives unchanged |
| Instruction managed sections | `templates/instructions-template.md` (+ generated `.specify/instructions.md`) | new pointer section with byte cap (FR-026, A-13) |

**New concept declared**: there is no existing owner for a general decision-item contract; `shared/definitions/decision-definitions.md` is therefore a new single owner (A-2), not a rewrite of any adjacent owner.

## Baseline measurements (dated; re-measurable at base `fbab7a45c`)

- Decision-adjacent owner sizes: `confirmation-gates.md` 149 lines, `decision-tension.md` 116, `fast-fail.md` 308, `superagent-definitions.md` 126, `register.md` 253.
- Existing decision-like records: 101 `### T-NNN` records across spec plans; 125 checkpoint files; 43 run reports; register decision-family rows (`D1–D9`, `D-A`, `D-B`, `D-001`, …).
- The two production rules are absent from both `templates/instructions-template.md` and `.specify/instructions.md` (grep for 完整名称 / 同名冲突 / region id: zero hits on the instruction surface).
- `.specify/glossary.md` has no Decision entry.
- No decision-item contract, record shape or transmission contract owner exists.

## Deterministic gate results

| Gate | Command | Verdict |
|---|---|---|
| Requirements validator | `validate-requirements.py .specify/specs/107-decision-governance/requirements.md` | `status: ok`, 0 error / 0 warning, 387 lines, 40 definition rows (30 FR + 10 SC), 9 shared strings, exit 0 — first run, no repair iteration |
| Pre-analyze gate | `pre-analyze-check.py --spec-dir .specify/specs/107-decision-governance --stage requirements --repo <worktree>` | `decision=pass errors=0 advisories=2 waived=0`, summary `fr=30 sc=10`; both advisories are `missing-path` naming `shared/definitions/decision-definitions.md` — the new owner page this feature creates (expected creation target) |
| Decomposition gate | `decomposition-check.py --mode plan --requirements .specify/specs/107-decision-governance/requirements.md` | `decision=proceed`, `fr_count=30`, `fr_ceiling=120`, rc 0 |
| Workspace signature | `workspace-guard.py --snapshot …` then `--check …` | snapshot recorded; check `clean`, rc 0 |
| Quality checklist | `.specify/specs/107-decision-governance/checklists/requirements.md` | 16/16 pass; no iteration consumed |

## Adjudications carried into the spec

- **Owner**: one new page `shared/definitions/decision-definitions.md`; adjacent owners keep their facts and gain pointer lines (A-2, FR-001, FR-002).
- **Archive**: archive-as-projection over a closed Decision Producer Inventory; `register` remains the sole id index; no second registry/store (A-3, FR-003, FR-004).
- **Classes**: decided by the holder — `human-interactive` (human) vs `ai-autonomous` (agent without a user); orthogonal to the confirmation-gate authorization axis (A-4, FR-006).
- **Text minimum bar**: full names; full resource location on possible same-name conflicts (business resource group + region id as the minimum pair); both land in the owner page **and** the instruction template, plus templates/guards/review (A-8, FR-007, FR-010).
- **Options**: closed enumerable set with label/consequences/reversibility/default/evidence; `other` only with a defined path; degenerate sets declare `forced` (FR-012).
- **Record**: closed field set (`decision_id`, `decision_class`, context, options, chosen option, rationale, evidence pointers, actor, timestamps, `transmission_status`); `D-NNN` per carrier registered at creation; reconstructable from archive + register alone; load-bearing decisions cross-reference `T-NNN` without duplicating the six fields (FR-014…FR-017).
- **Transmission**: decision block in the existing dispatch payload channel; seven role fields and four injections unchanged; acknowledgment + `implementation_receipt`; no silent re-decision; decision → dispatch → receipt audit chain (A-7, FR-018…FR-021).
- **Enforcement**: closed machine-decidable roster M-01…M-08 with reverse samples, behavior roster B-01…B-06 with named review surfaces; no machine claim for behavior rules (A-9, FR-022…FR-024).
- **Landing**: framework sources + instruction section + mirrors/per-tool copies + client init/refresh; new-only records, legacy readable, no dated-record rewrite; incompatible changes closed by migrate or deterministic refusal (A-10, FR-026…FR-029).
- **Glossary**: proposal-only, not written (A-11, FR-005; `glossary-proposal.md`).
- **Feature binding**: deferred to `/speckit.clarify`; `Related Feature` remains `Need clarification` (A-12).

## Deviations (disclosed)

1. **Brief path resolution**: the assignment named `.specify/.tmp/sdd-loop/tmp/decision-governance/brief-requirements.md` relative to the main repository; that path does not exist there. Exactly one consistent reading was available — the brief is materialized inside this worktree at the same relative path — so it was read there. Correction, not a decision.
2. **Scaffold deviation (anticipated by the brief)**: `create-new-requirements.sh` derives the next number from spec dirs, archived specs and local/remote branch names. Because the current line branch `107-decision-governance` is itself a `<NNN>-<slug>` branch, the script would compute `108` and create a **second** branch — contradicting the brief's mandate (spec number MUST be 107; do not create a second branch; proceed on the current branch and record the deviation). The script was therefore not executed; its template-copy step was replicated manually from `.specify/templates/requirements-template.md` (byte-identical to `templates/requirements-template.md`). The spec branch header, directory and input description are the only script outputs consumed. Recorded in the spec Clarifications as well.
3. **No user questions**: by assignment (unattended); all adjudications are recorded under the spec's Assumptions/Clarifications.

No destructive action, no dirty-file touch, no state-spine write, no push.

## Concurrency reading

- `requested=1` · `effective=not_evaluated` (settled by the orchestrator) · `effective_reason=single-unit`.
- Single leaf execution; no dispatch, no fan-out.

## Anomaly line

- 未发现异常。No in-passing repair was needed beyond the brief-path resolution above (disclosed as a deviation, not an anomaly).

## Re-anchoring record

- After reading brief + role: `on-track`.
- After concept-owner inventory: `on-track`.
- After manual scaffold deviation: `correction-applied` (disclosed; one reading consistent with the brief).
- After validator first-run green: `on-track`.
- After pre-analyze/decomposition/workspace gates: `on-track`.

## Wrap-up accounting

- **Run Determination**: `run-determination.py --action determine --unit-id /speckit.requirements --run-id r20261125T134500Z-107a --complexity complex --feature 107-decision-governance` → record `persisted: .specify/session/20261125T135914Z-run-determination-speckit-requirements-r20261125t134500z-107.md`; axes: token `not_evaluated` (source unavailable), elapsed `improved` (measured 498,000 ms from brief mtime to wrap-up), artifact correctness `not_evaluated` (no declared checks / this stage ran gates, not tests), satisfaction `not_evaluated` (pending next turn); `trigger_feedback: false`; `change_point: cp-r20261125T134500Z-107a clean=false findings=3` (all three are not-evaluated axes, disclosed rather than fabricated).
- **Exec Quant**: `exec-quant.py --action collect` → `.specify/exec-quant/records/20261125T135920685209Z-dd809ed0.json`.
- **Feedback Record**: `feedback-utils.py --action record --unit-id /speckit.requirements --unit-type command --run-id r20261125T134500Z-107a --feature 107-decision-governance` → entry `20261125T135929Z-speckit-requirements` at `.specify/feedback/20261125T135929Z-speckit-requirements.md`; `duplicate: false`.
- **Threshold Notice**: `should_prompt: true` (count_since_submission 556, threshold 10). One non-blocking notice is included in the report below; nothing is transmitted automatically and the wrap-up does not wait.
- **Token Reflection**: reflected in the feedback entry: one stable `token-efficiency` optimization point (a deterministic decision producer/carrier inventory engine to replace overlapping greps/reads) and one dedup/reuse point (a combined requirements-stage gate entry). No fabricated token count.
- **Close-out**: see the close-out receipt under `.specify/retention/closeout/` for the records commit; merge and push are not run by this dispatch (stage integration and push authorization belong to the driver).

## Threshold notice (non-blocking, one time)

The local feedback store has accumulated enough entries for its periodic submission check (556 since the last reset, threshold 10). Options, to be chosen whenever convenient — ignoring this never affects the current request:

1. Let the feedback command judge: run `/speckit.feedback` with no argument; it reads the store, decides which hat this repo wears, and routes the entries itself.
2. Skip this time: do nothing; the prompt reappears only after more entries accumulate.
3. Stop prompting: raise the threshold (e.g. `SPECKIT_FEEDBACK_THRESHOLD`), so feedback keeps recording but stops prompting.

Nothing is sent automatically; delivery, if any, stays a manual action.
