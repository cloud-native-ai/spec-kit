# Analyze-Repair Record — 108-team-view-degradation — 2026-11-26

- **Trigger**: analyze gate, round 1 — **2 validator-confirmed HIGH findings** (W1-01, W2-01), recorded verbatim in `test-evidence/analyze-domain-w1.jsonl` / `analyze-domain-w2.jsonl`; the other 16 domain findings (MEDIUM / LOW) are outside the authorized set and remain open by design.
- **Route**: analyze-gate autonomous upstream repair. Authority: the dispatch's two HIGH findings; no user questions (unattended), no dispatch, no implementation, no push.
- **Unit / run**: `skill:analyze-artifacts` · `r20261126T090814Z-108ar` · feature key `108-team-view-degradation` · branch `108-team-view-degradation` (worktree) · stage base commit `eca0f9d88`.
- **Scope discipline**: only live spec artifacts and their records were edited. Dated records (`checklists/requirements-quality-2026-11-26.md`, `checklists/requirements.md`, `checkpoints/**`, `test-evidence/*` from earlier stages, `103-team-view/**`) were **not** rewritten. FR ids (25), SC ids (8), STR ids (3) and all 35 contract clause ids are unchanged; the degradation reason set `{engine-degraded, report-recognition-uncertain}`, the exit-code set `0/2/3/4/5`, the six-group body and the report-naming owner are untouched.
- **Concurrency reading**: requested=1 · effective=not_evaluated · effective_reason=single-unit (one executor, single leaf, no dispatch).

## 1. Finding → change → evidence map

### W1-01 — healthy-predicate `goal` condition contradicted FR-013 (same fact in three drifting copies)

**Resolution**: FR-022 becomes the **single owner** of the healthy predicate; the goal condition is **`goal` absent OR slug-form**; FR-013's named state is scoped to the identity group's degraded cases, encoded as the dispatch's two conditions — **(a)** the value is not a slug form, **(b)** the binding is unreadable (the dispatch's "inline goal / missing binding"). A slug-form `goal` under a readable binding adds no state line and stays healthy (byte-identical). Every duplicate is now a pointer or is aligned.

- `requirements.md:49` (A-10 → pointer: predicate/referent/delta owned by FR-022), `:50` (A-11 → named increments re-enumerated against the completed predicate), `:104` (US3 healthy scenario → pointer), `:140` (FR-013 → (a)/(b) degraded scope + slug+readable adds no line), `:149` (FR-022 → single owner, six conditions), `:184` (SC-004 → pointer), `:236` (clarify answer aligned), `:238` (clarify answer → pointer to FR-022).
- `contracts/presentation.contract.md:12` (C-302 → (a)/(b) trigger, slug+readable adds no line, binding state independent and coexisting).
- `contracts/team-view-program.contract.md:34` (C-107 condition 4 = absent-or-slug; projection-of-FR-022 statement added).
- `contracts/view-labels.contract.md:32` (C-405 row → scoped to degraded cases).
- `data-model.md:82-83` (C8 → `form` field; `state` exactly when inline or binding unreadable).
- `research.md:106` (R-8 aligned), `tasks.md:209` (T015 aligned), `quickstart.md:35-50` (S-1 exercises both `goal` variants).
- **Evidence**: `test-evidence/analyze-repair-resolution-probe.txt` — 16/16 W1-01 probes PASS; `validate-requirements` 0 error / 0 warning.

### W2-01 — C-107's healthy predicate was incomplete vs. what 108 changes, so the empty allowed-delta claim was unscoped

**Resolution**: the predicate now covers **every dimension 108 changes**: the goal condition (above), **zero auxiliary artifacts** (so C-205's line never fires), **`items.jsonl` present, readable, ≥ 1 line** (so C-304's consequences never fire), and **all three continuous-spine files present** (so C-305's applicability forms never fire). The empty allowed-delta set is scoped **exclusively** to predicate-satisfying inputs, and degraded inputs carry the named correction increments. The auxiliary-line emission boundary is stated at its owner so the claim is satisfiable; the plan-time M4 fixture is disqualified as a healthy fixture and S-1/T020 are re-pointed at a completed-predicate fixture.

- `requirements.md:149` (FR-022 conditions (2) zero auxiliary / zero residue, (5) ledger in place, (6) spine all present; empty delta scoped; non-predicate fixtures MUST NOT masquerade as healthy).
- `contracts/team-view-program.contract.md:34` (C-107 six conditions item-for-item; "empty for predicate-satisfying inputs only"; explicit rejection of ledger-less / spine-less / auxiliary-bearing fixtures as evidence).
- `contracts/report-recognition.contract.md:24` (C-205 → auxiliary line emitted only when ≥ 1 auxiliary artifact; zero adds no line).
- `plan.md:124` (EP-003 → completed predicate + plan-probe scope disclosed), `research.md:42` (M4 amendment: the builder-default fixture is not a healthy fixture; S-1 re-takes the reading).
- `quickstart.md:35-50` (S-1 fixture = completed predicate, ledger + three spine files + both goal variants), `tasks.md:227` (T020 aligned).
- **Evidence**: `analyze-repair-resolution-probe.txt` — 13/13 W2-01 probes PASS; `pre-analyze-check` requirements/plan/tasks `decision=pass errors=0`.

## 2. PLAN-EDIT declarations (plan-owned touches, classification = minor)

`tasks.md` § Path Conventions designates `{plan.md, data-model.md, contracts/, research.md, quickstart.md, feature-ref.md}` as plan-owned ("仅小修须 `PLAN-EDIT:` 声明"). This repair touched those paths only as analyze-driven defect fixes; no semantic redesign, no clause added or removed.

| Path | Classification | What changed |
|------|----------------|--------------|
| `contracts/team-view-program.contract.md` | minor | C-107 rewritten: completed predicate, scoped empty delta, projection-of-FR-022 statement |
| `contracts/presentation.contract.md` | minor | C-302 rescoped to the (a)/(b) degraded trigger |
| `contracts/report-recognition.contract.md` | minor | C-205 gains the auxiliary-line emission boundary |
| `contracts/view-labels.contract.md` | minor | C-405 `goal` row scoped to degraded cases |
| `data-model.md` | minor | C8 gains `form`; `state` rule made disjunctive |
| `plan.md` | minor | EP-003 predicate completed + plan-probe scope disclosed |
| `research.md` | minor | R-8 aligned; M4 dated amendment (fixture no longer healthy) |
| `quickstart.md` | minor | S-1 fixture/expected reading completed (both goal variants, ledger, spine) |

Additionally: `requirements.md` (spec-owned; 8 sites), `tasks.md` (tasks-owned; T015/T020). `feature-ref.md` untouched (no duplicate).

## 3. Invariants held

- FR 25 / SC 8 / STR 3 unchanged; clause definition rows 9 / 8 / 9 / 9 = 35 unchanged (`analyze-repair-resolution-probe.txt`).
- Degradation reason set, exit-code set, envelope keys, six-group body, re-emission rule, report-naming owner and `team.md` schema untouched.
- Healthy byte-identical preservation retained and strengthened (predicate now sufficient for a zero delta); `goal:<slug>` under a readable binding is explicitly healthy and adds no line.
- No implementation, no test, no program edit; `goal-utils.py` untouched.

## 4. Deterministic gate readings (verbatim)

- `python3 .specify/scripts/python/validate-requirements.py …/requirements.md` → rc 0, `0 error(s), 0 warning(s)`, 239 lines / 33 definition rows / 3 shared strings (`analyze-repair-requirements-validator.txt`).
- `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir … --stage {requirements|plan|tasks} --repo .` → all three rc 0, `decision=pass errors=0 advisories=70 waived=0`, summary `fr=25 sc=8 tasks=29 clauses=35 files=13` (`analyze-repair-pre-analyze-{requirements,plan,tasks}.{txt,json}`).
  - Advisory adjudication (all pre-existing classes, none introduced): **38 `external-clause`** — the `INV-01…INV-10` invariant ids in `data-model.md` and their references in the dated checklist match the legacy clause-id shape (same noise recorded at plan/tasks stages); **32 `missing-path`** — the three planned test files (red-first premise), four contract/quickstart/feature-ref header references to them, and one driver-owned out-of-worktree path `.specify/state/u4-team-view-degradation-plan.txt`. No new advisory class or touched-file hit was introduced by this repair.
- `python3 .specify/scripts/python/validate-tasks.py …/tasks.md` → `PASS … — 0 error(s), 0 warning(s)`, rc 0 (`analyze-repair-tasks-validator.txt`).
- `decomposition-check.py --mode plan --requirements …` → `decision=proceed`, `fr_count=25`, rc 0; `--mode tasks --requirements … --tasks …` → `decision=proceed`, `fr_count=25`, `task_count=29`, rc 0 (`analyze-repair-decomposition-{plan,tasks}.{txt,json}`).
- Machine resolution probe → `RESULT: ALL PASS` (16 W1-01 + 13 W2-01 + 5 invariant probes; `analyze-repair-resolution-probe.txt`).

## 5. Deviations and residual risk

1. **Pre-existing untracked analyze evidence carried into the records commit (disclosed)**: `test-evidence/analyze-domain-w{1,2,3}.jsonl` existed untracked before this dispatch (18 findings: 2 HIGH + 16 MEDIUM/LOW, authored by the analyze-stage validators). This seat did not author or alter them; they are carried into the records commit so the trigger findings cited above are resolved in history. No other untracked file was touched.
2. **Dispatch parenthetical encoded literally**: "degraded cases only (inline goal / missing binding)" is written as the disjunction (a) non-slug value OR (b) unreadable binding, scoped to declared `goal` keys. The healthy claim is unaffected because predicate condition (1) requires a complete binding, so no predicate-satisfying input can hit (b).
3. **The completed predicate is narrower than the old one** by design: a builder-default fixture with no ledger and no spine (research M4) is no longer "healthy"; it is a degraded input under C-304/C-305. S-1 and T020 now require the completed-predicate fixture (ledger + three spine files + both goal variants). This is the W2-01 fix, not a regression.
4. **Dated records not rewritten**: `checklists/requirements-quality-2026-11-26.md` CHK030 (and CHK017/CHK028) posed the questions this repair answers; the checklist keeps its dated status. `checklists/requirements.md:42` likewise stays as the requirements-stage record.
5. **Open by design**: the 16 non-HIGH domain findings (W1-02…W1-06, W2-02…W2-06, W3-01…W3-06) remain open; none was authorized for this round.
6. **Registry/spine**: `.specify/features.md`, `.specify/features/027-team-management.md` and the state spine were not edited (driver close-out owns status advances).

## 6. Anomaly

- 未发现异常。No decision-class anomaly occurred. The three disclosed items above are corrections/interpretations inside the authorized repair scope; no user question was asked, nothing was pushed, and no dated record was rewritten.
