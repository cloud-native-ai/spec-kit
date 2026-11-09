# FV2 — final cross-artifact consistency and claim hygiene (analyze round 4, 2026-11-09)

**Worker**: FV2 (final verification, fork verifier). **Tree**: MAIN `/storage/project/cloud-native-ai/spec-kit`,
branch `master`, HEAD `aeadddd2`. Read-only: no edits, no commits, no push, no subagents; this file is the
only write. **Scope**: counts agreement, W2's M-5 sites, registry, team YAML shape, claim hygiene.

## 1. Counts — measured on this tree, 2026-11-09, HEAD `aeadddd2`

| Quantity | Claim | Measured | Verdict |
|---|---|---|---|
| FR | 43 | 43 distinct `FR-NNN` ids; 43 definition rows (`^- \*\*FR-NNN\*\*:`) | PASS |
| SC | 12 | 12 distinct `SC-NNN` ids; 12 definition rows | PASS |
| Clause markers | 113 markers = 113 distinct ids | 30 + 24 + 18 + 20 + 21 = 113 marker lines; 113 distinct; max `C-113`; 0 duplicates; ranges C-1…C-30 / C-31…C-52 + C-112…C-113 / C-53…C-70 / C-71…C-90 / C-91…C-111 | PASS |
| Task rows | 83 (`T001`…`T083`) | 83 `- [ ] TNNN` rows; 83 distinct; contiguous, no gap | PASS |
| Packages | 7 (15+17+19+8+16+6+2 = 83) | every package row's declared count matches its id set; union covers T001–T083 exactly once, 0 id in two packages | PASS |
| FR → clause map | 43/43 | `feature-ref.md` holds 43 distinct FR ids; gate evidence `43 of 43` (`test-evidence/vb-gate-coverage.txt`) | PASS |
| SC → module map | 12/12 | `feature-ref.md` holds 12 distinct SC ids | PASS |
| features.md header | 88 | 88 `^\| NNN` rows; 88 distinct ids; 0 duplicate row ids; header `Total Features: 88` | PASS |
| Serial baseline | 46 ids | `test-evidence/plan-baseline-names.txt`: 46 lines, 46 unique | PASS |
| Checklist | 40 items | 40 items in `checklists/2026-11-09-requirements-quality.md` | PASS |
| Spec-local definitions | probe 9 goal / 8 team = 17; census 9 / 10 = 19 | reproduced exactly; the two one-level team files are `088-speckit-visualization/team/team.md` and `092-non-disposable/team/team.md` (both tracked, both `lifecycle_state: active`); `088-…/fixtures/us1-compliant-fixture/team.md` is a fixture, excluded | PASS |
| Archive | 6 goal / 12 team | `.specify/anchoring/*/goal.md` = 6; `.specify/teams/*/team.md` = 12 | PASS |

Live count claims in the seven files: all agree with the measured table or carry a date/stage label,
**except** `requirements.md:47` and `plan.md:102,104` (findings F1/F2). Sites checked: `plan.md:5,53,63,88,189,191,354,361,372,374`;
`tasks.md:7,30,35,38,47,87-89,96,126,349,478-488`; `feature-ref.md:9,39`; `quickstart.md:27`;
`features.md:101`; `features/094.md:33-49`. Minor description nuance (not a count violation):
`feature-ref.md:39` "two FR cells per row" over 22 rows holds for 21 rows — the 22nd carries one FR
cell (21 rows carrying two FR cells each make 42 entries, and the 22nd row's single cell makes 43
entries in all; the stated 43 / 22 / 43 numbers are exact). Re-expressed 2026-11-10 (history wave
G2): same readings, spelled so the line's leading product is visible to a line-level reader.

## 2. W2's M-5 anomaly — what the three sites now say

| Site | Reading recorded | Verdict |
|---|---|---|
| `plan.md:53` (Scale/Scope) | probe form (`*/goal/*/goal.md`, `*/team/*/team.md`, C-43) goal 9 / team 8 = 17; full census adds two one-level non-conforming team files (both named), goal 9 / team 10 = 19; dated history: plan entry 7 / 7 = 14 (`test-evidence/requirements-baseline-probe.txt`, 2026-11-09), tasks stage 8 / 8 = 16 (tasks.md N-4, 2026-11-09); residual probe is authority | measured + labeled; agrees |
| `plan.md:258` (EP-002) | plan-entry 7 / 7 = 14; tasks-stage 8 / 8; round-4 probe form goal 9 / team 8 = 17; census goal 9 / team 10 = 19 (two files at one-level non-conforming paths, both named); archive 6 goal / 12 team | measured + labeled; agrees |
| `requirements.md:320` (A6) | round-4 re-measure: probe form goal 9 / team 8 = 17; two one-level non-conforming files (both named); full census goal 9 / team 10 = 19; dated history plan 7 / 7 = 14, tasks 8 / 8 = 16; comparative baseline kept | measured + labeled; agrees |

The three sites agree pairwise, and each reading is reproduced on the tree (probe 9/8, census 9/10 with
the fixture excluded; the 7/7 and 8/8 history is backed by the probe file and tasks N-4 respectively).
The requirement — measured and labeled rather than a chosen literal — is met. **PASS.**
The falsified `9 / 9` (= 18) reading still lives at two sites VC did not name: **F1**, **F2**.

## 3. Registry

- `features.md` header `Total Features: 88` = 88 rows = 88 distinct ids — **PASS**.
- `features.md:101` (`| 094 |` row): round-3 closure (`84d8765f`, `2c704003`) + round-4 verdicts
  (VA PASS / VB 4 LOW / VC split, pointing at `notes/analyze-round4/`) + fix-wave state + next-step
  chain (修复集成 + 门复跑 → 终验 → implement 门); FR/SC/clause/task/package numbers match section 1 —
  **PASS**, with one nuance: "锚定修复波次（W1/W2）进行中" is one notch behind the committed fix reports
  (`aeadddd2`); the stated next-step chain is correct and the row self-heals if the driver updates it at
  integration.
- `features/094.md:62-66`: same round-4 facts and same next-step chain; L-03 residual closure recorded
  at `:69-72` — **PASS**, same one-notch nuance.
- `register.md:192` (`C-01…L-03@094`) and `:193` (`R3-H-1…L-5@094`): both rows present verbatim, ranges
  intact, authority paths resolve — intact. **Status-cell drift → F3.**

## 4. Team file — `team/094-goal-team-parallel/team.md`

- Diff vs the fix-wave base is exactly 4 lines: `name` 092→094, `description` 092→094,
  `territory.write` `.specify/goal/**`→`.specify/anchoring/**`, `.specify/memory/features/092.md`→`094.md` —
  matching VC M-4's targets; nothing else moved.
- `yaml.safe_load` parses the front matter: same 16 top-level keys as before the edit; `seats` (9),
  `stage_seats` (tasks 2 / implement 6 / review 4), `members` (8, reporter with its reporting territory),
  `config` untouched — seat/roster semantics intact.
- No parse risk. `.specify/goal|teams` prose remains only at `:9` and `:131` (VC keep-list, mirrors the
  user brief). `slug`, `spec_dir`, `goal_slug`, `lifecycle_state` unchanged.

## 5. Claim hygiene — evidence pointers

| Pointer family | Check | Verdict |
|---|---|---|
| M-5 pointers (EP-002/A6/Scale-Scope → `test-evidence/requirements-baseline-probe.txt`, tasks.md N-4) | files exist; contents match (7/7; 8/8) | PASS |
| W1 fix notes → `analyze-repair2-gates-requirements.txt` (`43 of 43`), `pre-analyze-tasks-analyze-repair.json` (`fr 42 / sc 11 / tasks 80`, `decision: pass`, `checked_at 2026-11-09T08:20:54Z`), `coverage-tasks.txt` (`16 of 42`) | exist; content matches the claims | PASS |
| W2 fix notes → `requirements-baseline-probe.txt`, `notes/analyze-round3/w3-trunk-reconciliation.md`, `va/vb/vc` round-4 notes, `notes/analyze-round4/` | all exist | PASS |
| M-2 heading `Goal/Team（085）` | exists at `skills/external/sdd-loop-driver/SKILL.md:45` | PASS |
| M-8 premise command (`tasks.md:96`) | `.specify/anchoring` form; 6 / 12 reproduces | PASS |
| W1 anchoring count (10 lines) | measured 3 + 3 + 1 + 3 = 10 (binding 3, handoff 3, owner-rewrites 1, archive 3; command-family 0) | PASS |
| Round-4 fix notes (`fix-w1.md`, `fix-w2.md`) | present, committed in `aeadddd2`; internal claims spot-checked above | PASS |
| Identity residue `092` | only `requirements.md:262` (dated Clarifications quote, D5 keep) | PASS |
| `.specify/goal` residue | only `team.md:9,131` (keep-list); 0 live hits in quickstart/feature-ref/data-model/contracts/tasks | PASS |
| All `notes/…` + `test-evidence/…` paths cited in the seven artifacts + both fix notes | resolve, except 4 planned implement-stage deliverables (`notes/closure-readings.md`, `test-evidence/migration-applied.json`, `migration-dryrun.txt`, `residual-after.txt` — T079/T080/S7 outputs, not evidence-of-record pointers) | PASS |
| `requirements.md:47` → "见 plan EP-002" for a 9 / 9 reading | pointer resolves but EP-002 no longer states 9 / 9 (it states 17 / 19) — content mismatch | **F1** |

## Findings

- **FV2-F1 (MEDIUM)** — `requirements.md:47` (US2 body): "plan-entry 读数 goal 7 / team 7 见 A6，
  2026-11-09 round-3 复测 **goal 9 / team 9** 见 plan EP-002". This is the falsified directory-root reading
  W2 declared superseded, stated as a live pointer; EP-002 now records probe 9/8 = 17 / census 9/10 = 19, so
  the pointer's content no longer matches. Fix: state the 17 (or 19) reading, or drop the inline copy and
  keep the pointer to A6 / EP-002 as the single owner of the count.
- **FV2-F2 (MEDIUM)** — `plan.md:102` (T-001 `pole_b`) and `plan.md:104` (T-001 `expected_sacrifice`):
  "2026-11-09 复测 **18 条**" — the superseded 18 = 9 / 9 record, which matches neither measured shape
  (probe 17 / census 19) and is presented as the latest re-measurement in live decision-tension fields
  (not a dated session record, so D5 does not cover it). Fix: state the probe reading (17, census 19) or
  label the 18 as superseded at both sites.
- **FV2-F3 (LOW)** — `register.md:193` (`R3-H-1…L-5@094`) status cell still reads
  "open（repair round 3 running）" although repair round 3 closed at `84d8765f` (features.md:101 /
  features/094.md:60 both say 收口; all six gates green). The row's summary also names only L-1…L-4 while
  its id range reaches L-5. `register.md:192` (`C-01…L-03@094`) still ends "/L-03 残余" although
  `features/094.md:69` records L-03 closed by the round-4 fix wave. Rows are structurally intact and their
  authorities resolve; only the status cells drift. Fix: status cells to closed with the closing commit,
  and name L-5 in the range summary.

Non-failing nuisances: `features.md:101` / `features/094.md:66` say the fix wave is "进行中" while both
fix reports are committed (`aeadddd2`) — one notch behind; the next-step chain they state is correct.
`feature-ref.md:39` "two FR cells per row" holds for 21 of 22 rows (counts exact).

## Verdict

**FV2: FAIL — FV2-F1 `requirements.md:47` stale 9/9 pointer (EP-002 no longer says it) · FV2-F2 `plan.md:102,104` superseded 18 in live T-001 fields · FV2-F3 `register.md:192-193` status-cell drift.**
All headline counts, the three M-5 sites, the registry header/rows, the team YAML shape and every other
evidence pointer checked are sound.
