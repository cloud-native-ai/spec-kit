# VC — D4 anchoring reconciliation + residuals (analyze round 4, 2026-11-09)

**Worker**: VC, fork verification worker (read-only; this file is the only write).
**Tree**: MAIN `/storage/project/cloud-native-ai/spec-kit`, `master` @ `2c704003`.
**Inputs**: D4 decision (`notes/analyze-round3-findings.md` § Decision sheet), W3 body (`notes/analyze-round3/w3-trunk-reconciliation.md` §1.4, §2–3), R2 ledger residuals (`notes/analyze-round3/repair-r2.md` § Residual risks).
**Method**: every reading below was re-measured on the tree with `grep`/`find`/`ls`/`git cat-file`; no number is taken on faith from the repair ledgers.

---

## 1. THE SPLIT — contracts hit table (mandated)

Measured: `grep -c anchoring .specify/specs/094-goal-team-parallel/contracts/*.md` = **0 in all five pages**.
`grep -n '\.specify/goal' contracts/*.md` = **10 line occurrences / 9 clauses / 4 files**.

| # | file:line | clause | class | verdict |
|---|-----------|--------|-------|---------|
| 1 | `contracts/binding-and-lifecycle.md:61` | C-10 | normative — "`--scope goal` MUST resolve the goal root to `.specify/goal`" | **MUST ALIGN** → `.specify/anchoring` — **HIGH** |
| 2 | `contracts/binding-and-lifecycle.md:75` | C-13 | normative — write target "outside `.specify/goal/<slug>/`" | **MUST ALIGN** — **HIGH** |
| 3 | `contracts/binding-and-lifecycle.md:88` | C-15 | normative — territory prohibition on `.specify/goal/**` | **MUST ALIGN** → `.specify/anchoring/**` — **HIGH** |
| 4 | `contracts/unified-archive-and-migration.md:10` | C-31 | normative — "unified archive MUST be exactly `.specify/goal/<slug>/`" | **MUST ALIGN** — **HIGH** |
| 5 | `contracts/unified-archive-and-migration.md:11` | C-31 | normative — goal definition "lives at `.specify/goal/<slug>/goal.md`" | **MUST ALIGN** — **HIGH** |
| 6 | `contracts/unified-archive-and-migration.md:125` | C-112 | normative (dated measurement embedded) — "Measured 2026-11-09: `.specify/goal/*/goal.md` carries 6" | **ALIGN PATH, keep count 6** — **MEDIUM** |
| 7 | `contracts/handoff-contract.md:36` | C-58 | normative — `goal_slug` "MUST resolve to `.specify/goal/<goal_slug>/goal.md`" | **MUST ALIGN** — **HIGH** |
| 8 | `contracts/handoff-contract.md:42` | C-59 | normative — reverse key "MUST exist" at `.specify/goal/<goal_slug>/goal.md` | **MUST ALIGN** — **HIGH** |
| 9 | `contracts/handoff-contract.md:66` | C-63 | normative — `territory.write` "MUST NOT include `.specify/goal/**`" | **MUST ALIGN** → `.specify/anchoring/**` — **HIGH** |
| 10 | `contracts/owner-rewrites-and-tests.md:57` | C-100 | normative — framework-map Goals row "land only in `.specify/goal/`" | **MUST ALIGN** — **HIGH** |

**Class counts**: normative-and-must-align **9 lines / 8 clauses (HIGH)**; normative-with-dated-measurement **1 line / 1 clause (MEDIUM)**; explanatory/dated-only **0**.

**Why HIGH** (dispatch criterion — "an implementer reading only the contracts would build the removed path"): C-31 defines the migration destination as the removed tree; C-10 resolves `--scope goal` there; C-13 guards it; C-58/C-59 resolve handoff keys there; C-100 writes it into `framework-map.md`; and C-15/C-63 protect a dead tree while leaving `.specify/anchoring/**` **unprotected** (fails open on the real archive). The exposure is live: `tasks.md` carries green tags for every affected clause — `#C-10`, `#C-13`, `#C-15`, `#C-31`, `#C-58`, `#C-59`, `#C-63`, `#C-100`, `#C-112` all appear.

**C-112 note**: the count 6 still holds (`.specify/anchoring/` has 6 slug dirs); only the path is wrong, and it was already wrong on 2026-11-09 (W3 measured `.specify/anchoring/` that day — `.specify/goal/` was absent). This is a live-clause measurement, not a historic record of a pre-rename tree.

---

## 2. Same defect class outside the contracts (live execution surfaces)

`tasks.md`, `quickstart.md`, `feature-ref.md`, `data-model.md` and `team.md` carry the identical old path. None of these is a dated record; all are consumed by the implement/review stages.

| file:line | surface | class | verdict |
|-----------|---------|-------|---------|
| `tasks.md:176` | US1 **Independent Test** — "assert both land under `.specify/goal/<slug>/`" | normative instruction | **MUST ALIGN** — **HIGH** |
| `tasks.md:220` | T037 [US2] — "the archive layout is `.specify/goal/<slug>/goal.md`" | normative instruction | **MUST ALIGN** — **HIGH** |
| `tasks.md:321` | T073 (FR-029) — "Goals and Teams rows name only `.specify/goal/`" | normative instruction | **MUST ALIGN** — **HIGH** |
| `tasks.md:330` | T081 — backfill test over every `.specify/goal/*/goal.md` | normative instruction | **MUST ALIGN** — **HIGH** |
| `tasks.md:400` | 085 disposal row 11 — "goal path moves to `.specify/goal/<slug>/`" | normative instruction | **MUST ALIGN** — **HIGH** |
| `tasks.md:96` | stage-premise measurement command `basename -a .specify/goal/*/` | normative measurement | **ALIGN; count 6/12 holds** — **MEDIUM** |
| `tasks.md:200` | Phase 4 US2 heading "档案统一落 `.specify/goal/`…" | heading | align (cosmetic) — **LOW** |
| `quickstart.md:42` | S-1 expected result — "the definition lands at `.specify/goal/…`" | normative walkthrough | **MUST ALIGN** — **HIGH** |
| `quickstart.md:64` | S-3 expected result — "each definition exists at `.specify/goal/<slug>/goal.md`" | normative walkthrough | **MUST ALIGN** — **HIGH** |
| `quickstart.md:80` | S-5 command `sha256sum .specify/goal/demo-command-goal/goal.md` | normative walkthrough | **MUST ALIGN** — **HIGH** |
| `quickstart.md:82` | S-5 command (re-hash after bind) | normative walkthrough | **MUST ALIGN** — **HIGH** |
| `feature-ref.md:92` | SC-012 row — "every `.specify/goal/*/goal.md` … resident" | normative | **MUST ALIGN** — **HIGH** (contradicts `requirements.md:209` SC-012, which already says `.specify/anchoring/*/goal.md`) |
| `data-model.md:21` | E-1 binding record — "Path `.specify/goal/<slug>/goal.md` (C-31)" | normative design | **MUST ALIGN** — **HIGH** |
| `data-model.md:42` | validation rule — territory "must not include `.specify/goal/**`" (C-15) | normative design | **MUST ALIGN** — **HIGH** |
| `team.md:17` | `territory.write: .specify/goal/**` (live grant; `.specify/anchoring/**` missing) | operational state | **ALIGN or drop** — **MEDIUM** |

**Keep (dated / explanatory — D5, do not rewrite)**: `requirements.md:10` (user Input quote), `:19` (rename fact), `:153` (FR-028 quoting the dying literal as the thing to replace), `:251` (dated Clarification), `:299`/`:304` (dated round-3 Notes) — 6 hits; `plan.md:11,16,47,110,111,134,141,163` (historical / antithesis / rename facts) — 8 hits; `research.md:19,35,88,131` (Phase-0 dated research) — 4 hits; `goal.md:11,15` (goal Objective mirrors the user brief) — 2 hits; `team.md:9,131` (goal/charter text mirroring the brief) — 2 hits; `checkpoints/01–05` goal rows + `01:7` anomaly (stage records) — 6 hits.

**Totals**: 53 `.specify/goal` occurrences in the spec dir → **25 live alignment hits** (10 contracts + 15 non-contract) and **28 dated/explanatory keeps**. The split is **not contract-only**: R2 residual risk 1 under-scoped it.

---

## 3. D4 substance — FR-007 / FR-025 / FR-028 vs W3 §2–3

| Check | Evidence | Verdict |
|-------|----------|---------|
| Recorded rationale exists | `plan.md:132–142` **T-004** carries the full decision-tension shape (decision / antithesis "keep `global`+`auto`" / two poles / discriminating evidence / expected sacrifice / **two** revision triggers incl. the member-name↔directory reopening condition); `requirements.md:297–306` round-3 Notes; `requirements.md:315` A1. The **rejected** antithesis (rename member to `anchoring`) is recorded — see Notes bullet | **PASS** |
| Engine's current scope values stated as a fact, not redefined | FR-025 (`requirements.md:150`): "现值仍为 `global|spec|auto`，这是本特性要改写的事实起点，不是本条的退让"; T-004 same. Verified on the tree: `scripts/python/goal-utils.py:1339` `choices=("global", "spec", "auto")`, `:146` guard | **PASS** |
| Spec-local store path unchanged | `goal-utils.py:61` `SPEC_GOAL_DIRNAME = "goal"` with the explicit comment at `:56–58` ("deliberately still `goal` … unchanged this round"); FR-007 names `<spec>/goal/<slug>/goal.md` as **migration source only**; C-43 probe glob unchanged | **PASS** |
| FR-007 re-scoped to `.specify/anchoring/<slug>/goal.md` + `.specify/teams/<slug>/team.md` | `requirements.md:132`; matches D4 vocabulary | **PASS** |
| FR-025 closed set `goal` / `teams` / `auto` with member-naming ruling | `requirements.md:150`; C-9 (`binding-and-lifecycle.md:56–58`) is the same value set; T-004 links FR-025 ↔ T-004 ↔ C-9 | **PASS** |
| FR-028 pointer corrected | `requirements.md:153` names `skills/external/sdd-loop-driver/SKILL.md` § `Goal/Team（085）` + `references/checkpoint-protocol.md`; both exist; the "读方须两者都认" sentence exists at `SKILL.md:45` (alias obligation is live, not moot) | **PASS** |
| No silently redefined value domain | Old values stated as fact, new set declared with antithesis and revision trigger | **PASS** |

**One D4 defect at the contract layer**: `contracts/owner-rewrites-and-tests.md:22` (C-93) still says the SKILL's "§ **Temporary Goal/Team** MUST be retitled" — that section title does not exist on the tree (real heading: `Goal/Team（085）`, `SKILL.md:45`). This is exactly the W3 X-07 dead pointer FR-028 corrected; the contract projection did not follow. **MEDIUM**, fix C-93 to name `Goal/Team（085）`.

---

## 4. Residuals

### R-2 `features.md` header — **live claim, stale by one**
`features.md:4` `**Total Features**: 87`; the table has **88 rows / 88 distinct ids** after the renumber (`grep -cE '^\| [0-9]{3}'` = 88; `sort -u | wc -l` = 88). The header is a current-state declaration at the top of the canonical registry, not a dated record (W3 §4.3 expected 88 after the renumber). **MEDIUM** — fix `features.md:4` → `**Total Features**: 88`.

### L-03 `team/094-goal-team-parallel/team.md` — **live operational state, not dated**
The file is the active run team (`lifecycle_state: active`, consumed by `run-team`); its identity/territory lines are live:
- `:2` `name: SDD Temporary Team 092` — **live, stale id**
- `:4` `description: … for Feature 092` — live, stale id
- `:17` `territory.write: .specify/goal/**` — live grant on a dead path; `.specify/anchoring/**` absent
- `:37` `territory.write: .specify/memory/features/092.md` — grants **ND's** detail file; ours is `features/094.md`

(`:9`/`:131` goal/charter text mirror the user brief — dated content, keep.)
**MEDIUM** — fix targets as listed.

### L-2 EP-002 denominator — **canonical rule stated, recorded reading falsified**
The plan states one canonical **rule** ("the count is the probe's reading, not a frozen constant"; "the residual probe remains the authority") — that part is sound. But the recorded repair-stage reading is wrong in the other direction:
- probe-visible per C-43 (`*/goal/*/goal.md`, `*/team/*/team.md`) = **9 goal + 8 team = 17**
- all definition files = **9 goal + 10 team = 19** (8 two-level + **2** one-level: `088-speckit-visualization/team/team.md`, `092-non-disposable/team/team.md`; both tracked, both `lifecycle_state: active`, 088's present at R2's base `abfc12d1` via `git cat-file -e`)
- `plan.md:53` / `plan.md:258` (EP-002) / `requirements.md:320` (A6) say **18 = goal 9 / team 9**, "**one** non-conforming" — the team total is 10, not 9, and there are **two** one-level files, not one.

Neither 16 nor 18 matches the tree. **MEDIUM** — fix `plan.md:53`, `plan.md:258`, `requirements.md:320`; state the probe reading (17) as the canonical number and record two one-level files.

---

## 5. Duplicate-092 handling

| Check | Evidence | Verdict |
|-------|----------|---------|
| ND archive pointer keeps `092` | `features.md:99` row `092` Non-Disposable with the archive-pointer note; `features/092.md`, `specs/092-non-disposable/`, `state/092-non-disposable.md` intact | **PASS** |
| No bare-token sweep damage to clause ids | `C-92` intact at `owner-rewrites-and-tests.md:15`; green tag `#C-92` intact at `tasks.md:324`; `feature-ref.md:17,20,21` reference C-92; **no** zero-padded `C-092` form exists; `C-94` is a distinct real clause (no duplication). `goal-utils.py:56,141` `092` lineage comments intact; `test-evidence/*` keeps measured `.specify/specs/092-goal-team-parallel` paths (dated evidence, must keep) | **PASS** |
| Our line `094` everywhere live | **NO** — live residues: `requirements.md:14` `**Feature ID**: 092` (branch line `:3` says 094 — internal contradiction); `tasks.md:3` `**Requirement ID**: 092`; `tasks.md:5` `**Related Feature**: 092 …`; `tasks.md:472` "next minor release after 092" (live version-point ruling); `tasks.md:143`/`:490` `.specify/.tmp/s092`; `tasks.md:491` "pre-092 protocol"; `data-model.md:1` / `research.md:1` titles `Feature 092`; `team.md:2,4` | **FAIL** |
| Dated records correctly kept | `checkpoints/01–05` (incl. `01:7`, `01:35`, `03:20,33`), `checklists/2026-11-09-…`, `notes/*`, `test-evidence/*`, `research.md:45` run id `…-092a` | **PASS** |

**Severity**: identity lines in `requirements.md:14` + `tasks.md:3,5` = **MEDIUM** (primary spec + task list carry a foreign feature id while their own key/branch lines say 094); `tasks.md:472` version point = **MEDIUM** (after the renumber "092" denotes ND); `tasks.md:143,490,491` fixture/context tokens = **LOW**; `data-model.md:1`, `research.md:1` titles = **LOW**.

---

## 6. Verdict

**VC: FAIL** — H-1 contracts split (8 clauses / 9 lines) · H-2 tasks.md split (5 instruction rows) · H-3 quickstart.md split (4 executable lines) · H-4 feature-ref SC-012 split (1 row) · H-5 data-model split (2 design rules) · M-1 C-112 path · M-2 C-93 dead section title · M-3 features.md header 87 vs 88 · M-4 team.md live residues · M-5 EP-002/A6 denominator · M-6 identity residues (`requirements.md:14`, `tasks.md:3,5`) · M-7 `tasks.md:472` version point · M-8 `tasks.md:96` premise command · L-1 `tasks.md:143,490,491` · L-2 `data-model.md:1`/`research.md:1` titles · L-3 `tasks.md:200` heading.

**Counts**: HIGH 5 findings / 21 line-hits · MEDIUM 8 findings / 15 line-hits · LOW 3 findings / 6 line-hits. Keep-as-dated: 28 occurrences across 7 files.

**Fix targets (exact)**
- H-1: `contracts/binding-and-lifecycle.md:61,75,88` · `contracts/unified-archive-and-migration.md:10,11` · `contracts/handoff-contract.md:36,42,66` · `contracts/owner-rewrites-and-tests.md:57` — `.specify/goal` → `.specify/anchoring`
- H-2: `tasks.md:176,220,321,330,400`
- H-3: `quickstart.md:42,64,80,82`
- H-4: `feature-ref.md:92`
- H-5: `data-model.md:21,42`
- M-1: `contracts/unified-archive-and-migration.md:125` (keep 6)
- M-2: `contracts/owner-rewrites-and-tests.md:22` (→ `Goal/Team（085）`)
- M-3: `.specify/memory/features.md:4` (→ 88)
- M-4: `team/094-goal-team-parallel/team.md:2,4,17,37`
- M-5: `plan.md:53`, `plan.md:258`, `requirements.md:320`
- M-6: `requirements.md:14`; `tasks.md:3,5`
- M-7: `tasks.md:472`
- M-8: `tasks.md:96`
- L-1: `tasks.md:143,490,491`
- L-2: `data-model.md:1`; `research.md:1`
- L-3: `tasks.md:200`
