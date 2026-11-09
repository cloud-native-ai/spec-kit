# V2B — V3 fix verification + gate rerun (analyze round 3)

**Verifier**: fork worker V2B (read-only; this file and `test-evidence/v2b-*` are the only writes)
**Worktree**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/093-clarify`
**Branch / HEAD**: `093-concurrency-by-default` @ `8c90088c` (repair commit `86b9e43c`, base `780dfa82`)
**Objects under test**: the V3 finding list (`notes/analyze-round2/v3-trunk-reconciliation.md` § 6) against the repair landed in `86b9e43c`, plus a full gate rerun with explicit flags.
**Method**: every fix re-read from the artifact itself; body-integrity claims checked against `git diff 780dfa82..HEAD` on the touched paths; every gate re-executed today (2026-11-09, ~18:09 +08:00) with stdout/stderr and exit codes retained under `test-evidence/v2b-*`.

---

## Part A — V3 finding closure

| id | severity | required state (round-3 criterion) | measured | verdict |
|----|----------|-----------------------------------|----------|---------|
| V3-F1 | MEDIUM | `requirements.md:307` retired path + 持久/临时 lifetime reading now consistent with FR-032 `:185` and the owner page; dated correction is an acceptable closure, a rewritten dated body is not | Body intact (`git diff` shows **no** `-` line for the Q/A). Dated blockquote added directly below at `requirements.md:309`: path `.specify/goal/<slug>/` → renamed by 090 to `.specify/anchoring/<slug>/goal.md`, and the 存档-vs-临时 **lifetime** reading explicitly retired ("scope 不是生存期"). Live FR-032 `:185` reads the same (only 存储位置 distinguishes the two scopes, "MUST NOT 被读成「持久 vs 临时」"). Owner page `shared/definitions/goal-definitions.md:34` — "No 'temporary' property. A scope is not a lifetime"; `:44` maps the retired naming forward | **CLOSED** |
| V3-F3 | MEDIUM | SC-006's reason is `mechanism-not-yet-landed` in `quickstart.md` and checklist CHK043, not "no dispatch tool" | `quickstart.md:115` (live artifact, rewritten in place): "the feature's own concurrency mechanism has not landed yet (the declaration facts, the engine, and the FR-035 runner path), so the run declares serial with `mechanism-not-yet-landed` and records SC-006 as `not_evaluated`. A tool set is a per-run probe (RS-005), never a constant; the earlier 'no dispatch tool' reason was measured false at analyze 2026-11-09 (F-093-012)." CHK043 (`checklists/2026-11-09-requirements-quality.md:80`): reason now `mechanism-not-yet-landed`, marked "校正 2026-11-09, analyze-repair round 2 · V3-F3", verdict stays `not_evaluated` | **CLOSED** |
| V3-F4 | MEDIUM | `research.md:144` R-10 carries a dated correction, body intact | Body intact (`git diff`: only `+` lines). Dated blockquote at `research.md:148-152`: the "no dispatch tool" premise "was itself measured false at analyze (F-093-012)", tool set = per-run probe (RS-005), live reason = `mechanism-not-yet-landed` | **CLOSED** |
| V3-F2 | LOW | `requirements.md:293` path half closed | Same correction note explicitly names "L293 与 L307"; body retained as dated record. FR-001 `:133` current text carries `.specify/anchoring/<slug>/` | **CLOSED** |
| V3-F5 | LOW | CHK001 / CHK027 vocab corrected by dated note, item text retained | CHK001: dated note — "第五个根的现行路径为 `.specify/anchoring/<slug>/`——FR-001 已按 090 更名后的路径书写；本条正文的 `.specify/goal/` 与实测读数 6 保留为 dated record". CHK027: dated note — FR-032 now separates scopes by storage location, lifetime reading retired, global path `.specify/anchoring/<slug>/goal.md`. Both bodies retained | **CLOSED** |
| V3-F6 | LOW | six checkpoint headings annotated, not rewritten | All six checkpoints (`01:9`/`02:11`/`03:15`/`04:14`/`05:19`/`06:15`) keep the heading `## 2. Temporary Goal progress` and carry one identical dated note below it (points at `checkpoint-protocol.md` § 2 "Goal progress"). `git diff 780dfa82..HEAD -- checkpoints/` shows **only `+` lines** — no heading or body line removed | **CLOSED** |
| V3-F7 | LOW | T135 retired adjective fixed, ownership statement unchanged | `tasks.md:308` now: "the spec-local goal layer (a storage scope, not a lifetime — FR-032) stays owned by the earlier goal/team feature" | **CLOSED** |

Supplementary (claimed by the repair ledger, not in the round-3 required list): V3-F9 — both dated notes present in `notes/analyze-findings.md` (disclosure above + § 5 item 6), each stating the measured 03/04/05 vs 01/02 distinction. **CLOSED**.

**Fix-table count: 7 required + 1 supplementary = 8 / 8 closed; 0 open.** No dated body was rewritten; every annotation landed as an appended dated note except the two surfaces the repair declared live (`quickstart.md` S-6) or whose reason the finding itself required replaced (CHK043).

---

## Part B — Gate rerun (explicit flags, 2026-11-09)

| # | Gate | Reading (verbatim key lines from `test-evidence/v2b-*`) | EXIT | Ledger claim (`notes/analyze-repair2.md` § 4) | Match |
|---|------|----------------------------------------------------------|------|-----------------------------------------------|-------|
| G1 | `validate-requirements.py requirements.md` | `status: ok`; `[id-contiguous] [doc-order] [ref-resolvable] [marker-count] [dup-id] [path-marker]` all `pass (0)`; `scanned: 337 lines, 47 definition rows, 11 shared strings`; `0 error(s), 0 warning(s)` | 0 | same reading | **MATCH** |
| G2 | `account-clause-coverage.py <spec-dir> --corpus-root <worktree>/.specify/specs` (no `--freeze`) | `status: baseline-missing`; `scanned 319 files: parsed 203 + named-unparseable 116 == 319`; `claimed clauses (this feature): 37`; `[fr-uncovered] pass (0) — 35 of 35 FRs cited from citation groups`; `[clause-uncovered] fail (656)`; `[clause-unparsable] fail (116)`; `[coverage-baseline-delta] fail (656)`; `657 error(s), 1 warning(s)` | 2 | same; baseline file `coverage-baseline.txt` still MISSING | **MATCH** (clause lane red-by-baseline-missing, declared expected state; no baseline created) |
| G3 | `validate-tasks.py tasks.md` | `PASS — 0 error(s), 0 warning(s)` | 0 | PASS 0/0 | **MATCH** (row count 152 confirmed via G6 / G5 / `tasks.md:358,429`) |
| G4 | `validate-decision-tensions.py --spec <spec-dir>` | `status: ok`; all six rules `pass (0)`; `scanned: 466 lines, 5 record(s)`; `0 error(s), 0 warning(s)` | 0 | same | **MATCH** |
| G5 | `pre-analyze-check.py --repo <worktree> --spec-dir .specify/specs/093-concurrency-by-default --stage requirements` / `plan` / `tasks` | all three: `decision=pass errors=0 advisories=112 waived=0`; summary `fr=35, sc=12, tasks=152, clauses=0, files=15`; 112 findings = 110 `missing-path` + 2 `blocked-by`, all `advisory` | 0 ×3 | 112 advisories; `fr=35 / sc=12 / tasks=152`; "one more than the prior run's 111" | **MATCH** — and the 111 baseline is confirmed in `test-evidence/v2-pre-analyze-check.txt` (`advisories": 111`) |
| G6 | `decomposition-check.py --mode tasks --requirements … --tasks …` | `{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 35, "task_count": 152, "fr_ceiling": 120, "task_ceiling": 160}, "reasons": []}` | 0 | same | **MATCH** |

**Ledger-claim comparison summary**: 152 rows — matched (G6 + G5 + `tasks.md:358` "Every one of the 152 rows appears in exactly one package" + `tasks.md:429` round-2 run record). `fr 35 / sc 12` — matched across all three pre-analyze stages. `112 advisories` — matched exactly on all three stages, and the delta vs the prior 111 is real. No gate was weakened, no baseline frozen, no new error introduced since the repair.

**Cross-check of record corrections**: the V3-F1 correction note also names the two verify-side old-path advisories (checklist:16) that explain the 112-vs-111 delta — measured present in the v2b requirements-stage advisory list.

---

## Part C — SC-006 status

| Check | Reading | Verdict |
|-------|---------|---------|
| `verification.md` (implement-stage artifact) | absent (`ls` → exit 2) | correct — nothing can fabricate `SC-NNN_status` |
| Any `SC-006_status=` / status=pass claim | none anywhere; the only pass-shaped formula is `tasks.md:34` GATE-4's **rule definition** ("every `final`-path criterion has `SC-NNN_status=pass`"), not a claim about this stage | no surface claims it passed |
| Live artifacts stating the status | `plan.md:357,438` — deferred / `not_evaluated`; `tasks.md:378,422` — `not_evaluated`, not `0`, not an estimate; `quickstart.md:115` — `not_evaluated`; `research.md:154` — stays `not_evaluated`; CHK043 — `not_evaluated` by design | consistent |
| Dated checkpoints with the old reason in body | `04-tasks.md:21,52,59`, `05-checklist.md:26` still say "no dispatch tool"/"cannot dispatch", but each file carries the F-093-012 dated banner at `:3` (verified); `06-analyze.md:54` restates with the disclosure | annotated dated records — acceptable |
| State spine | `.specify/state/093-concurrency-by-default.md:51` — "SC-006 not_evaluated" | consistent |

**Result: SC-006 stays `not_evaluated` everywhere; no surface claims it passed.**

---

## Observations (non-blocking, disclosed not absorbed)

1. The checklist's header `**Detection path**` line (`checklists/2026-11-09-requirements-quality.md:13`) still states the checklist-producing run's tool set as "不含子代理派发能力". This is a dated description of how the checklist was produced (the file header is a dated producer record, not a claim about SC-006's reason) and sits outside V3-F3's two named surfaces; no correction was added there. Recorded as an observation, not an open item.
2. `checkpoints/04-tasks.md` body still reads "137 task rows" (dated count from the tasks stage); untouched and covered by the same dated-record discipline. Not a finding — the live count 152 is asserted by G5/G6 and `tasks.md:358,429`.
3. V3's forward note on the MAIN-tree 092→094 renumber remains a forward risk outside this worktree; unchanged by this pass.

## Verdict

- Part A: **8/8 closed** (V3-F1, V3-F3, V3-F4 MEDIUM; V3-F2, V3-F5, V3-F6, V3-F7 LOW; V3-F9 supplementary) — 0 open.
- Part B: all six gates rerun; every reading matches the repair ledger's claims (152 rows; fr 35 / sc 12; 112 advisories; G1 337/47/11; G2 657/1 exit 2; G4 466/5; G6 proceed).
- Part C: SC-006 `not_evaluated` everywhere; no pass claim exists.

**V2B: PASS**
