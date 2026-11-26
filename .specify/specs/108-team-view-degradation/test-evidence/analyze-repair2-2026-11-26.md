# Analyze-Repair Round 2 Record — 108-team-view-degradation — 2026-11-26

- **Trigger**: analyze gate, round 2 — **2 validator-confirmed HIGH findings** (R2-108-W1-01, R2-108-W3-01), recorded verbatim in `test-evidence/analyze-domain-w1-r2.jsonl` / `analyze-domain-w3-r2.jsonl`; the other 16 round-2 domain findings (W1-02…W1-06, W2-01…W2-06, W3-02…W3-06; MEDIUM / LOW) are outside the authorized set and remain open by design.
- **Route**: analyze-gate autonomous upstream repair. Authority: the dispatch's two HIGH findings; no user questions (unattended), no dispatch, no implementation, no push.
- **Unit / run**: `skill:analyze-artifacts` · `r20261126T092355Z-108ar2` · feature key `108-team-view-degradation` · branch `108-team-view-degradation` (worktree) · stage base commit `03791736c`.
- **Scope discipline**: only live spec artifacts and their records were edited. Dated records (`checklists/**`, `checkpoints/**`, earlier `test-evidence/*`, `103-team-view/**`) were **not** rewritten. FR ids (25), SC ids (8), STR ids (3), task rows (29) and all 35 contract clause ids are unchanged; the five-form timestamp set, the degradation reason set, the exit-code set `0/2/3/4/5`, the six-group body and the report-naming owner are untouched.
- **Concurrency reading**: requested=1 · effective=not_evaluated · effective_reason=single-unit (one executor, single leaf, no dispatch).

## 1. Finding → change → evidence map

### R2-108-W1-01 — FR-001's five-form closed set contradicted its own decomposition and the Clarifications record

**Resolution**: the enumerated **five forms are the sole closed set**; the sentence now *decomposes exactly those five* instead of describing a date × time cross product. The pairing is: compact date `YYYYMMDD` × compact times `hhmmss` / `hhmm` (2), ISO date `YYYY-MM-DD` × times `hh:mm:ss` / `hh-mm-ss` / `hhmmss` (3) — 5 in total, and "五种之外无其它组合". The three previously ambiguous cross-product shapes (`YYYYMMDD` + `hh:mm:ss`, `YYYYMMDD` + `hh-mm-ss`, `YYYY-MM-DD` + `hhmm`) are therefore outside the set by construction. The Clarifications answer now carries the **same grouping**, names FR-001 as the owner, and no longer restates the 8-way cross product. `contracts/report-recognition.contract.md` C-201, `data-model.md` C2 and `research.md` R-1 already enumerated the same five forms and needed no edit — the drift existed only between the two prose sites.

- `requirements.md:128` (FR-001 → pairing decomposition, "五种之外无其它组合").
- `requirements.md:233` (Clarifications answer → five-form grouping, FR-001 named owner).
- **Evidence**: `analyze-repair2-resolution-probe.txt` — 18/18 W1-01 probes PASS, including a behavioral parser run: all five listed forms parse under the stated rule, the three excluded cross-product shapes do not, all five production-evidence stamps (`20261124T074500Z`, `20261125T121924Z`, `2026-11-25T140000Z`, `2026-08-07T18-30-00Z`, `20261014T1710Z`) parse, and date-only / month-13 / hour-24 / non-Z samples are rejected; `validate-requirements` 0 error / 0 warning.

### R2-108-W3-01 — tasks required producing `verification.md` while both territory contracts forbid it to every crew seat

**Resolution** (established 106/107 pattern): the crew writes `test-evidence/verification-input.md`; `verification.md` is **derived spec-side** from that input and stays forbidden to every seat. The read-before-producer defect is removed independently: T028's baseline is the literal `54c6efa8c` already recorded in DoD-6 / FR-022, not a value read from `verification.md`.

- `tasks.md:17` (DoD-1 → deferred reasons in `test-evidence/verification-input.md`; `verification.md` derived).
- `tasks.md:24` (DoD-8 → crew-writable close-out input; `verification.md` derived, crew MUST NOT write).
- `tasks.md:33` (GATE-4 → checks the derived `verification.md`, with explicit derivation annotation).
- `tasks.md:58` (task-state sigil → deferred reason in the crew input, derived into `verification.md`).
- `tasks.md:64` (evidence landing points → `test-evidence/verification-input.md`; `verification.md` derived).
- `tasks.md:247` (T028 → `git diff --stat 54c6efa8c..HEAD`; no read from `verification.md`).
- `tasks.md:248` (T029 → assembles `test-evidence/verification-input.md`; derived `verification.md` explicitly forbidden to the crew).
- `tasks.md:250` (Polish checkpoint → crew input directly derivable into `verification.md`).
- `tasks.md:314` (incremental delivery → crew input, spec-side derivation).
- `handoff.md:26` (Task Reference → T029's crew-side deliverable is the input; `verification.md` is never a crew write).
- `handoff.md:35` (forbidden list keeps `verification.md`, with the derivation explanation).
- `team.md:146` (Dynamic Structure → crew input path inside its write territory; `verification.md` derived and forbidden).
- **Evidence**: `analyze-repair2-resolution-probe.txt` — 20/20 W3-01 probes PASS; every remaining `verification.md` mention in tasks.md (8 lines) is derivation-annotated; both territory write grants already cover `test-evidence/**` and keep `verification.md` forbidden (no new write surface); read-only smoke `python3 scripts/python/team-view.py --repo-root . 108-team-view-degradation` → rc 0 (edited `team.md` still parses).

## 2. PLAN-EDIT declarations (plan-owned touches)

**None.** No plan-owned path (`plan.md`, `data-model.md`, `contracts/`, `research.md`, `quickstart.md`, `feature-ref.md`) was touched. W1-01 needed no contract edit because C-201 / C2 / R-1 already carried the five forms; W3-01 lives entirely in `tasks.md`, `handoff.md` and `team.md`. `feature-ref.md` untouched; `plan.md:91`'s output-tree comment already frames `verification.md` as implement-stage output, which the crew-input split does not contradict.

## 3. Invariants held

- FR 25 / SC 8 / STR 3; clause definition rows 9 / 8 / 9 / 9 = 35; task rows 29 and every task status unchanged (`analyze-repair2-resolution-probe.txt`).
- The five-form timestamp set is semantically identical to the pre-repair contracts — only its prose decomposition and the Clarifications restatement changed. The degradation reason set, exit-code set, envelope keys, six-group body, re-emission rule, report-naming owner and `team.md` schema are untouched.
- Crew writability is unchanged: `test-evidence/verification-input.md` lands inside the existing `test-evidence/**` grants; `verification.md` remains forbidden; both territory contracts keep the same write/forbidden lists (one clarifying sentence added each).
- No implementation, no test run, no program edit; `goal-utils.py` and `scripts/python/team-view.py` untouched.

## 4. Deterministic gate readings (verbatim)

- `python3 .specify/scripts/python/validate-requirements.py …/requirements.md` → rc 0, `0 error(s), 0 warning(s)`, `scanned: 239 lines, 33 definition rows, 3 shared strings` (`analyze-repair2-requirements-validator.txt`).
- `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir … --stage {requirements|plan|tasks} --repo .` → all three rc 0, `decision=pass errors=0 advisories=70 waived=0`, summary `fr=25 sc=8 tasks=29 clauses=35 files=13` (`analyze-repair2-pre-analyze-{requirements,plan,tasks}.{txt,json}`).
  - Advisory adjudication: the finding set is **identical to round 1** — same check / path / line / message multiset, zero added, zero removed. Composition: **40 `external-clause`** (the `INV-01…INV-10` invariant ids in `data-model.md`; legacy clause-id shape, same noise as earlier stages) and **30 `missing-path`** (the three planned test files, a red-first premise, plus one driver-owned out-of-worktree state path). Note: round 1's record transcribed this split as 38/32; its JSON already held 40/30 — this record states the measured values.
- `python3 .specify/scripts/python/validate-tasks.py …/tasks.md` → `PASS … — 0 error(s), 0 warning(s)`, rc 0 (`analyze-repair2-tasks-validator.txt`).
- `decomposition-check.py --mode plan --requirements …` → `decision=proceed`, `fr_count=25`, rc 0; `--mode tasks --requirements … --tasks …` → `decision=proceed`, `fr_count=25`, `task_count=29`, rc 0 (`analyze-repair2-decomposition-{plan,tasks}.{txt,json}`).
- Machine resolution probe → `RESULT: ALL PASS (46 pass, 0 fail)` (18 W1-01 + 20 W3-01 + 8 invariant probes; `analyze-repair2-resolution-probe.txt`).

## 5. Deviations and residual risk

1. **Pre-existing untracked analyze evidence carried into the records commit (disclosed)**: `test-evidence/analyze-domain-w{1,2,3}-r2.jsonl` existed untracked before this dispatch (18 round-2 findings: 2 HIGH + 16 MEDIUM/LOW, authored by the analyze-stage validators). This seat did not author or alter them; they are carried into the records commit so the trigger findings cited above are resolved in history. No other untracked file was touched.
2. **Clarifications answer edited in place**: the requirements Clarifications section is a live writeback surface of the clarify protocol (round-1 precedent edited the goal answers there); the fix must reach it because it was one of the two contradicting sites. Dated checklists and checkpoint records stay untouched.
3. **T028 baseline literal**: the baseline is resolved to `54c6efa8c` (already recorded in DoD-6, FR-022 and the Measured Premises table) instead of being read from `verification.md`. `GATE-6`'s `<baseline_commit>` placeholder was left as-is under the same literal — it was not part of the finding.
4. **`team.md` edited under dispatch authority**: the dispatch explicitly authorizes "handoff/team-adjacent text" updates; tasks.md's `.specify/teams/**` read-only clause governs the implement crew, not this analyze-stage repair seat. The edit adds one boundary sentence (106/107 wording) and leaves the write/forbidden lists unchanged.
5. **Open by design**: the 16 non-HIGH round-2 findings remain open; none was authorized. In particular **W3-02** (`coverage-baseline.txt` outside the crew write territory) is adjacent to W3-01 but NOT authorized — T002 and the `coverage-baseline.txt` entry at `tasks.md:64` were deliberately left unchanged.
6. **Registry/spine**: `.specify/features.md`, `.specify/features/027-team-management.md` and the state spine were not edited (driver close-out owns status advances); nothing was pushed.

## 6. Anomaly

- 未发现异常。No decision-class anomaly occurred. The disclosed items above are corrections/interpretations inside the authorized repair scope; no user question was asked, nothing was pushed, and no dated record was rewritten.
