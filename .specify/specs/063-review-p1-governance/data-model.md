# Data Model: Review P1 Governance（评审 P1 治理）

**Spec**: `.specify/specs/063-review-p1-governance/requirements.md` | **Feature**: 063 Review P1 Governance（评审 P1 治理）
**Scope**: design entities for the F1–F8 mechanism fixes. All entities are framework-source artifacts or their governed payloads; no runtime database, no new store (宪法 IX).

## 1. Entities

### E1 — 引用组 Paren Group（F1）

A parenthetical group in a contract clause block that cites FR/SC ids.

| Field | Type | Rule |
|-------|------|------|
| open_delimiter | enum(`(`, `（`) | declared in owner § 4 rule 2 |
| close_delimiter | enum(`)`, `）`) | must pair with the open delimiter's width for nesting |
| nesting | ≤1 level, same width | per owner's existing "一层嵌套" rule |
| wellformed | bool | cross-width pairing or unpaired delimiter ⇒ malformed |

Validation (from FR-001/FR-002): the delimiter charset and same-width nesting MUST be declared in `shared/definitions/contract-clause-definitions.md` § 4 rule 2 (normative owner body); `scripts/python/clause_extract.py` `parentheticals()` implements exactly that charset; a malformed group MUST be reported by the checker and MUST NOT be silently counted as citation or as mention. Self-test samples (≥1 full-width group, ≥1 same-width nested group, ≥1 malformed cross-width case) live in `tests/contract/test_clause_forms.py` — the extractor's existing deterministic self-test home.

### E2 — Coverage Baseline（F1；[[STR-002]]）

A frozen, name-level coverage snapshot for one feature's contract set.

| Field | Type | Rule |
|-------|------|------|
| path | `<spec-dir>/coverage-baseline.txt` | engine default (`BASELINE_NAME`, `--baseline`) |
| producer | `/speckit.tasks` | freeze via `account-clause-coverage.py --freeze > <path>` at the existing re-freeze timing |
| consumer | `/speckit.analyze` | fixed step; re-runs the accountant against the frozen file |
| missing | state | `baseline-missing` MUST surface as a phase-visible problem with remedy (FR-003); a feature without a contract set MUST skip explicitly with a reason, never fabricate an empty baseline |

Relationship: one per feature that has `contracts/`; consumed read-only by analyze; compared with the `comm -13` idiom the accountant already implements.

### E3 — Checklist Gap Disposition（F2）

The accountable answer for one unchecked checklist item tagged `[Gap]`.

| Field | Type | Rule |
|-------|------|------|
| item_id | `CHKnnn` | as authored in `checklists/<file>.md` |
| status | enum(`raised-as-finding`, `dispositioned`) | deterministically checkable marker in the analyze gate report — never free prose |
| marker | string | e.g. `raised-as-finding H-01` or `dispositioned: covered-by <artifact § anchor>` |
| answering stage | string | the later stage that resolved the item's subject |

Validation (FR-005): after an analyze run, no `[Gap]`-tagged unchecked item may be in the state "unchecked + not raised + not dispositioned". Items without a `Gap` tag keep the existing load semantics (no new obligation — Edge Cases).

### E4 — Recheck File（F2）

The append-only per-round answer record for a checklist.

| Field | Type | Rule |
|-------|------|------|
| path | `checklists/recheck-<date>-<topic>.md` | one new file per answering round |
| answered_entry | entry id + the requirement line it answers | every answered entry MUST quote the requirement row it resolves |
| original_checklist | immutable | MUST NOT be refreshed in place; original unchecked rows preserved as history |

Form owner: `skills/internal/create-checklist/SKILL.md` § 5 Generate (061 REC-C5's named target). Consumer: `skills/internal/implement-feature/SKILL.md` § Step 2 third branch (FR-007).

### E5 — Waiver Record（F2）

A four-part closure record for an item that remains genuinely unresolved at implement.

| Field | Rule |
|-------|------|
| `Scope` | which checklist/file/items the waiver covers |
| `Basis` | why the item cannot be answered now |
| `Disposition` | what happens to it (who owns the follow-up, where) |
| `Closed` | what solved it — a waiver without a closing statement stays open-ended |

Format owner: `skills/internal/implement-feature/SKILL.md` § Step 2 (061 REC-C6's named target, same face as FR-007). A waiver missing any part is non-compliant and MUST NOT be treated as closed evidence (Edge Cases).

### E6 — Recommendation（REC-）（F3；[[STR-003]]）

A durable review-recommendation identifier.

| Field | Type | Rule |
|-------|------|------|
| id | `REC-<suffix>` | coined by the review stage |
| meaning | one line | pointer shape only — no body restatement (One Source of Truth) |
| anchor | report path + section | repo-relative primary form |
| status | enum | e.g. `open` / `landed` / `rejected` |
| storage | `.specify/memory/register.md` | existing pointer-row form; no new store (宪法 IX/XIII) |

Validation (FR-009): every `REC-` id coined in a review report is registered in the same commit; a review with zero `REC-` adds zero rows (no fabricated ids — Edge Cases).

### E7 — Transition Row（F3/E2）

One command's owned lifecycle transition in `shared/workflow/feature-integration.md`.

| Field | Rule |
|-------|------|
| command | one row per command — "each command owns exactly one transition" stays true |
| new row | `/speckit.review` → `Implemented → Ready for Review`, condition "`review.md` 已提交且每个延期项已解决或豁免" |
| annotated row | `/speckit.checklist` keeps its row, annotated "applies only when the checklist runs after implement" |

### E8 — Args Manifest（F4）

Per engine action, the machine-derived argument contract the compiled face renders.

| Field | Type | Rule |
|-------|------|------|
| engine | `run-determination.py` / `feedback-utils.py` / `exec-quant.py` | Handler `behavior_owner` set |
| action | e.g. `determine` / `record` / `collect` | Handler `action` set |
| required | list of flags | MUST equal the engine parser's required set (FR-030: derived from the parser, never hand-written) |
| source | list of flags | the measurement-source args the action accepts (e.g. `--session-file`, `--session-rows`, `--tool`, `--declared-check`, `--green-check`) |
| rejected | complement | args the action does not accept MUST NOT be rendered (FR-014) |

State: derived at compile time by `probe-utils.py --action compile-embeds`; a handler whose engine/action yields no manifest MUST fail the compile loudly (registry/engine divergence is a fast-fail surface, not a silent skip).

### E9 — Compiled Wrap-up Face（F4）

The AUTO-GENERATED `## Wrap-up` section of one unit.

| Field | Rule |
|-------|------|
| engine lines | carry the full required-arg set + source args from E8, with run-scoped values as `<…>` placeholders |
| convention line | one rendered line stating that `<…>` holds this run's runtime values (substitute and execute) — part of the deterministic section output |
| fingerprint | unchanged mechanism (sha256[:12] of the registry projection); a renderer change drifts all units until recompiled |

Validation (FR-016): after the fix, all units recompiled, `--check` zero drift, `--reconcile` where applicable, and the 2026-10-15 `backlog.md` row (line 89) flipped `closed` in the same commit. Idempotency: `(unit_id, run_id)` duplicate semantics unchanged; the engine MUST NOT mint run-ids (FR-017).

### E10 — Evidence Record（F6）

The mechanical counterpart of a `pass` claim in `verification.md`.

| Field | Type | Rule |
|-------|------|------|
| sample_id | string | evaluation sample identifier |
| evidence_path | repo-relative path | archived artifact produced by actually running the sample |
| evidence_sha256 | hex | SHA-256 of the archived file bytes — algorithm declared in the template (plan-level decision, per requirements Out of Scope) |
| verdict | enum | template's SC status vocabulary owner |

Placement: a new section between `# -- /speckit.implement results --` and `# -- Success Criteria evaluation --` in `templates/verification-log-template.md`. Validation (FR-019/FR-021): a `pass` verdict MUST carry a complete row; a pass without one is `unverified` and MUST NOT be cited as passing evidence.

### E11 — Evidence-Binding Gate Row（F6；[[STR-001]]）

A command-gate registration in `shared/definitions/probe-definitions.md`.

| Field | Value |
|-------|-------|
| object_id | `gate-implement-evidence-binding` |
| class_id | `command-gate` |
| unit | `/speckit.implement` |
| check | for every sample recorded `pass`: archived artifact exists, is non-empty, and its computed SHA-256 equals the recorded hash; missing/empty/mismatch ⇒ red |
| consumption | existing gate-probe mechanism only (no new subsystem); referenced from `skills/internal/implement-feature/SKILL.md` at the verification-log step (Step 9) |

Samples with a verdict other than `pass` are exempt from the binding duty (only `pass` claims carry it — requirements Acceptance Scenario 3).

### E12 — Frozen Baseline（F7, general）

A name-level frozen measurement with a consumer-side re-capture duty.

| Field | Rule |
|-------|------|
| set | derived from the spec directory at pre-flight time (globs over `<spec-dir>/baseline-*` and `<spec-dir>/notes/baseline-*`, plus the E2 coverage baseline) — never a hand-written count (FR-030) |
| pre-flight | `/speckit.implement` re-captures each entry before starting; differing values written back into the citing row |
| drift classification | `upstream repair` / `inherited` / `attributable to this feature` / `undecidable`, via `git log` provenance, BEFORE any drift verdict; `undecidable` MUST be explicit — no guessing (FR-022) |
| missing file | treated as first-capture with provenance recorded, never as zero-drift (Edge Cases) |

### E13 — Mechanism Fix Record（cross-cutting）

The execution unit of this feature: finding → owner artifact → contract test → acceptance scenario. Not a new persistent id system — the mapping lives in `feature-ref.md` (FR→clause map, SC→verification map).

## 2. Relationships

```text
E1 Paren Group ──declares──▶ contract-clause-definitions.md § 4 rule 2 (owner)
E1 ──implemented-by──▶ clause_extract.py parentheticals()
E2 Coverage Baseline ──frozen-by──▶ /speckit.tasks (--freeze)
E2 ──consumed-by──▶ /speckit.analyze (fixed step, C-5)
E3 Gap Disposition ──emitted-by──▶ /speckit.analyze gate report
E4 Recheck File ──answers──▶ checklist item ──consumed-by──▶ implement Step 2 branch 3
E5 Waiver ──format-owned-by──▶ implement Step 2
E6 REC- ──registered-in──▶ register.md (same commit as the report)
E7 Transition Row ──owned-by──▶ feature-integration.md table
E8 Args Manifest ──derived-from──▶ engine parser ──rendered-into──▶ E9 Compiled Face
E10 Evidence Record ──checked-by──▶ E11 Gate Row ──fired-at──▶ implement Step 9
E12 Frozen Baseline ──produced-by──▶ /speckit.tasks ──re-captured-by──▶ implement pre-flight
E13 Mechanism Fix Record ──indexes──▶ E1–E12 (traceability in feature-ref.md)
```

## 3. State Transitions

### Feature status state machine (E7 consequence)

Existing transitions unchanged except ownership annotation:

| Command | Transition | Condition |
|---------|-----------|-----------|
| `/speckit.requirements` | (none) → `Draft` | binding only |
| `/speckit.plan` | `Draft → Planned` | MUST NOT land `Implemented` |
| `/speckit.tasks` | maintain `Planned` | unchanged |
| `/speckit.implement` | `Planned → Implemented` | Pre-Status-Flip Gate |
| `/speckit.checklist` | `Implemented → Ready for Review` | only when run after implement (newly annotated) |
| `/speckit.review` *(new)* | `Implemented → Ready for Review` | `review.md` committed AND every deferred item resolved or waived |

### E2 Coverage Baseline lifecycle

`unfrozen` →(tasks, first full-tree accounting)→ `frozen` →(analyze, compare)→ `clean` | `delta-classified`; `baseline-missing` is a surfaced problem state with remedy, never a silent pass.

### E4 Recheck lifecycle

`authored (unchecked, Gap)` →(analyze)→ `raised-as-finding` | `dispositioned` →(downstream stage)→ `answered (recheck file)`; the original checklist row is never flipped in place.

## 4. Non-entities (explicitly out of model)

- No new feedback store, REC database, scoring system, tracking engine, or maturity report (宪法 IX/XIII; requirements Out of Scope).
- No modification to 062 artifacts — they are evidence inputs (FR-029), not model subjects.
