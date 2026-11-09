# W3 — Trunk Reconciliation (analyze round 3, 2026-11-09)

**Worker**: W3 of 3, concurrent, read-only except this file.
**Trunk measured**: `/storage/project/cloud-native-ai/spec-kit` on `master` at `738a42fa` (upstream `gitlab/master` merged at `a72138e1`).
**Domain**: trunk overlap assessment. This is **decision input for the user**, not a defect report against the artifacts.

---

## 1. Trunk surface measurements (all read from the tree, not taken on faith)

### 1.1 What exists where

| Surface | State on trunk `738a42fa` | Evidence |
|---|---|---|
| `.specify/anchoring/` | **EXISTS** — 6 slug dirs (`command-logic-as-classified-skills`, `draw-diagram-interactive`, `draw-two-layer-structure`, `post-refactor-mechanism-integrity`, `session-driven-self-improvement`, `skill-layer-install-separation`) | `ls .specify/anchoring` |
| `.specify/goal/` | **ABSENT** — directory renamed away | `ls: cannot access '.specify/goal'` |
| `.specify/teams/` | **EXISTS** — 12 slug dirs + `.gitkeep` | `ls .specify/teams` |
| Archive file name inside anchoring dirs | **still `goal.md`** (6 `goal.md`, 5 `summary.md`, 5 `roster.md`); **no `anchor.md` anywhere** | `find .specify/anchoring -name '*.md' \| sed 's\|.*/\|\|' \| sort \| uniq -c` |
| Spec-local `goal/` dirs | **9** (`085`, `086`, `087`, `088`, `089`, `090`, `091`, `094-goal-team-parallel`, `092-non-disposable`) | `ls -d .specify/specs/*/goal` |
| Spec-local `team/` dirs | **9** (same set) | `ls -d .specify/specs/*/team` |

> **Delta against our own baselines**: our `requirements.md` FR-043 and `plan.md` § Scale record "`.specify/goal/*/goal.md` 6 条、`.specify/teams/*/team.md` 12 条" and "14 real spec-local definitions to migrate (goal 7 / team 7)". The **archive** counts (6 / 12) still hold; the **spec-local** count has grown to **9 / 9**, because `094-goal-team-parallel` itself and `092-non-disposable` added one each after those baselines were taken. This is a stale measurement in our artifacts, not a trunk change.

### 1.2 Which artifact owns each concept today

| Concept | Owner on trunk | Notes |
|---|---|---|
| **Anchoring / spec-scoped Goal / Goal–Team binding** | `.specify/shared/definitions/goal-definitions.md` (byte-identical to `shared/definitions/goal-definitions.md`) | Title is still "Goal Definitions Reference"; § *Scope: Anchoring vs Spec-Scoped Goal* owns the two scopes |
| **Team** | *no dedicated `team-definitions.md`* — deferred to `/speckit.team` + `skills/internal/create-team`; one-line row in `agent-definitions.md:92` | The `goal-definitions.md` § *Terminology Boundaries* table is the nearest existing register |
| **Binding rule** | `goal-definitions.md` § *Goal–Team Binding* — one-way `goal_slug`, **N teams : 1 Goal**, identity-only, no content copy; run-level axis is the **Target**, never the binding | Already landed |
| **Scope-is-not-lifetime rule** | `goal-definitions.md` § *Scope Is Not Lifetime* — "temporary goal" → spec-scoped goal; "global goal" → Anchoring; "temporary team" → team | Already landed |
| **Scope value set (`--scope`)** | `goal-utils.py` `choices=("global","spec","auto")` — **`global`/`spec`/`auto`, unchanged**; live `resolve-scope --scope auto` still errors `scope-ambiguous` naming "global and spec candidates" | Live run below |
| **Engine** | `scripts/python/goal-utils.py` (mirror `.specify/scripts/python/goal-utils.py`), **name unchanged**, 12 actions; `ARCHIVE_DIRNAME = ".specify/anchoring"` at line 59, `DEFINITION_FILENAME = "goal.md"` at line 63 | `--help` |

### 1.3 Live engine reading (executed, not read)

```
$ python3 scripts/python/goal-utils.py --json resolve-scope --scope auto --spec-dir .specify/specs/090-re-anchoring
error: scope-ambiguous: both the global and spec candidates exist
       (.../.specify/anchoring and .../.specify/specs/090-re-anchoring);
       pass --scope global or --scope spec
```

`--help` usage line: `[--scope {global,spec,auto}]`; description: *"Anchoring (goal) definition engine — stores goal.md definitions in the .specify/anchoring archive or a spec's goal/ subtree."*

### 1.4 What the rename actually changed vs. what it did not

**Changed** (commit `8edd955d`, "anchor rename W1/W2 + 092 merge W3"):
- the global directory: `.specify/goal/` → `.specify/anchoring/`
- the **wording** in `goal-definitions.md`, the command templates, the engine comments/help text
- the "temporary goal/team" vocabulary in the concept owner → "scope is not lifetime"

**NOT changed** (measured, all still live on trunk):
- the scope **value names** `global` / `spec` — `goal-utils.py` `--scope`, every command template (`templates/commands/goal.md:29,38`, `templates/commands/team.md:35,45,75`), and the live engine all still say `global|spec|auto`
- the archive **file name** — still `goal.md`, never `anchor.md` (the merge note listed `anchor.md` as a *default taken unless redirected*, and it was not taken)
- the **spec-local write path** — `<spec>/goal/<slug>/goal.md` and `<spec>/team/<slug>/team.md` are still written and still exist (9 and 9 on trunk)
- **`sdd-routing-definitions.md:41`** — still carries the paragraph *"**Temporary run-scoped scopes（追加 carve-out）**: … a spec-local **Temporary Goal/Team** MAY … `.specify/goal/**` 与 `.specify/teams/**` 仍是运行与 child line 的 forbidden paths"*. Both the "Temporary" predicate **and** the now-nonexistent `.specify/goal/**` path survive.
- **`framework-map.md:12`** — `| Goals | .specify/goal/<slug>/ | …` — still the old path; `grep -c anchoring framework-map.md` = **0**.
- **`skills/external/sdd-loop-driver/SKILL.md:45`** — still: *"两者都只写 spec-local `goal/` 与 `team/`，全局 `.specify/goal/**`、`.specify/teams/**` 是 forbidden paths"* (our FR-028 names `.specify/skills/sdd-loop-driver/SKILL.md`, a path that does not exist; the real path is `skills/external/...` mirrored at `.specify/skills/sdd-loop-driver/`).
- **`085-re-anchoring`... no — `085-sdd-temporary-goal-team/requirements.md:26,180,194,267`** — FR-013 / FR-024 / SC-008 still specify `.specify/goal` + `.specify/teams` as global and `<spec-dir>/goal` as spec, and `.specify/goal/**` as a forbidden path.
- **`.specify/specs/090-re-anchoring/requirements.md:190,198,248`** — the absorbed ND feature's **ND-FR-046 / ND-FR-051 / RS-005** still say *"复用既有 `085` 的 spec-local Temporary Goal/Team"* and *"MUST 是 `085` 的 spec-local Temporary Team"*. The absorbed feature thus depends on the very predicate the parallel lineage set out to remove.

**Conclusion**: the upstream commit is a **partial** application of the rename map its own merge note proposed. The *directory* and *wording* waves landed (W1/W2 partly, W3 for the ND merge); the *value-name*, *file-name*, *routing*, *framework-map* and *085* waves did not.

---

## 2. Conflict table — our artifact statement vs. the trunk

Numbered rows `X-01 … X-18`. Columns: our statement (path:line + quote) → trunk counterpart (path:line + quote) → verdict.

| # | Our statement (path:line) | Trunk counterpart | Verdict |
|---|---|---|---|
| **X-01** | `requirements.md:132` FR-007 — goal/team 唯一写入落点 `.specify/goal/<slug>/` 与 `.specify/teams/<slug>/` | Trunk archive is `.specify/anchoring/<slug>/goal.md` (`goal-definitions.md:163-171`); `.specify/goal/` **does not exist** | **SUPERSEDED** (path renamed under us) |
| **X-02** | `requirements.md:16` plan summary — `archive-scope` closed three rows headed `.specify/goal/<slug>/` | `.specify/anchoring/` | **SUPERSEDED** (same as X-01, plan side) |
| **X-03** | `requirements.md:149` FR-024 — goal 侧唯一 owner 是 `goal-definitions.md` | Same file, byte-identical, **and it now already owns the rename** (§Scope, §Scope Is Not Lifetime, §Storage & Anchoring Archive) | **DUPLICATED** — the owner we name has already done part of our job |
| **X-04** | `requirements.md:150` FR-025 — 封闭三成员 `goal` / `teams` / `auto`; `global` 与 `spec` 一并出域 | `goal-utils.py` `--scope {global,spec,auto}`; every command template; live `resolve-scope` — **`global`/`spec` still the only accepted names** | **STILL DELTA** (our FR is not landed) — but the **member names we chose are now wrong**: `goal`/`teams` name *archive rows*, and the archive row is now called *anchoring*, not *goal* |
| **X-05** | `requirements.md:22` US5 — 「临时 / 全局」 must stop being a classification predicate; SC-008 (`requirements.md:205`) asserts zero hits on the runtime face | `goal-definitions.md:42` § *Scope Is Not Lifetime* **already states the rule**; but `sdd-routing-definitions.md:41`, `driver SKILL.md:45`, `090 requirements.md:190,198,248` **still use "Temporary"** | **PARTIALLY SUPERSEDED** — the concept statement landed; the enforcement surface did not. Our SC-008 would still fail, against *fewer* targets than we believed |
| **X-06** | `requirements.md:152` FR-027 — rewrite `sdd-routing-definitions.md` "Temporary run-scoped scopes" paragraph | Paragraph still present verbatim at `:41`, including the dead path `.specify/goal/**` | **STILL DELTA** (unchanged) |
| **X-07** | `requirements.md:153` FR-028 — rewrite `.specify/skills/sdd-loop-driver/SKILL.md` § Temporary Goal/Team | (a) the named path **does not exist**; real file is `skills/external/sdd-loop-driver/SKILL.md` (mirrored). (b) there is **no § titled "Temporary Goal/Team"**; the content is a one-paragraph *"Goal/Team（085）"* at `:45` | **WRONG POINTER + STILL DELTA** |
| **X-08** | `requirements.md:156` FR-029 — `framework-map.md` Goals/Teams 两行表达新落点 | `framework-map.md:12` still `| Goals | .specify/goal/<slug>/ |`; zero occurrences of "anchoring" | **STILL DELTA** |
| **X-09** | `requirements.md:151` FR-026 — restate terminal-retention / N:1 / terminal-refuses-binding as inferences of the new model | All three **already owned** by `goal-definitions.md` (§Singularity Rule, §Goal–Team Binding, §Storage) | **DUPLICATED** (harmless: our FR only requires citing them) |
| **X-10** | `requirements.md:127` FR-002 — a **new** `binding` record: `owner` / `owner_id` / `origin` on every definition | Trunk has **no `binding` field on any definition**: `grep -l binding .specify/teams/*/team.md` = **0 of 12**; goal.md files carry `status`/`created`/`updated` only; engine has no binding action (`grep -c handoff goal-utils.py` = 0; `binding` hits are the *pre-existing* `goal-binding` check id) | **STILL DELTA** — clean, but it is **additive to a renamed substrate** |
| **X-11** | `requirements.md:136` FR-011 — migration equivalence compares "concept payload", excluding the binding row | No migration action exists in the engine; `migrate` is *"derive a definition from a team's inline goal"*, a different operation | **STILL DELTA** |
| **X-12** | `requirements.md:132` FR-009 / `:135` FR-010 / `:138` FR-012 — idempotent migration into the unified archive, archive-not-delete, receipts under `.specify/archive/goal-team/`, read-only residual probe | `.specify/archive/` contains **only** `spec/`; **no `goal-team/`**; no residual probe; no receipt | **STILL DELTA** |
| **X-13** | `requirements.md:158` FR-034 / `:159` FR-035 — `handoff.md` contract, bidirectional key pair `goal_slug`+`team_slug` ↔ `handoff_ref`, `<spec-dir>/handoff.md` | No `handoff.md` anywhere outside our own artifacts and an unrelated log/test name; `handoff_ref` = **0** outside our `features/094-goal-team-parallel.md:8` | **STILL DELTA** |
| **X-14** | `requirements.md:161` FR-036 — territory expansion from the handoff contract, spec-side three artifacts forced into `territory.forbidden` | `territory` exists on 10 of 12 `team.md` files, but is declared per-team only; no expansion mechanism, no `forbidden`-forcing | **STILL DELTA** (substrate exists) |
| **X-15** | `requirements.md:171` FR-043 / `plan.md:53` — 存量 backlog: archive 6 goal + 12 team resident definitions lack `binding`; 14 spec-local definitions to migrate (goal 7 / team 7) | Archive counts **hold** (6 / 12). Spec-local counts are now **9 / 9**, not 7 / 7 | **STALE MEASUREMENT** in our artifact (not a trunk conflict — our own feature and ND each added one) |
| **X-16** | `requirements.md:26` Overview — "`.specify/goal/` 与 `.specify/teams/` 这两张既有的框架级档案表" | The "两行档案" framing survives; only the goal row's *directory* was renamed. The **three-row archive-scope** model (`goal` / `teams` / `.tmp`) is ours, not trunk's | **PARTIALLY SUPERSEDED** — row 1 renamed, rows 2–3 unchanged |
| **X-17** | `plan.md:213-214` — `skills/internal/create-team/references/conceptual-model.md` gains `binding` + `handoff_ref` | File exists; no `binding` / `handoff_ref` today | **STILL DELTA** (clean) |
| **X-18** | `features.md:101` — our row says "定义统一迁到 `.specify/goal` 与 `.specify/teams`" | The registry row states a path that no longer exists on trunk | **SUPERSEDED** — registry prose is wrong on its face |

**Conflict count: 18 rows.** Tally of the verdict column exactly as written above: **3 SUPERSEDED** (X-01, X-02, X-18) · **2 PARTIALLY SUPERSEDED** (X-05, X-16) · **2 DUPLICATED** (X-03, X-09) · **10 STILL DELTA** (X-04, X-06, X-07*, X-08, X-10, X-11, X-12, X-13, X-14, X-17) · **1 STALE MEASUREMENT** (X-15). X-07 carries two verdicts (wrong pointer **and** delta) and is counted once in the delta column, so 3+2+2+10+1 = 18. Per-FR roll-up in §3.

---

## 3. Landed-vs-delta FR accounting (43 FRs)

Judged against **trunk surfaces that exist and are enforced**, not against intent. Categories:

- **L (landed)** — trunk already implements the FR's substance; our FR would only restate it (duplication risk, not work).
- **P (partial)** — trunk landed a component the FR depends on, but not the FR itself.
- **D (delta)** — nothing on trunk implements it; our FR is the only carrier.
- **S (superseded)** — the FR's *statement* is now wrong on its face (names a path/vocabulary trunk removed) and must be rewritten before it can be implemented at all.

| FR | Class | Anchor / evidence |
|---|---|---|
| FR-001 command runs own goals/teams via the same engine | **D** | no `owner`-based command-run path; engine is spec/global only |
| FR-002 `binding` record (`owner`/`owner_id`/`origin`) | **D** | X-10: 0 of 12 team.md carry `binding` |
| FR-003 binding writes only via engine; rewrite action | **D** | engine has no binding action |
| FR-004 definition survives its creating run | **P** | trivially true for archive entries; no mechanism, no test |
| FR-005 closed command-family determination | **D** | `flow-class-classes.yaml` exists (substrate), no goal/team-owning predicate |
| FR-006 reuse `flow-class-*` declarations | **P** | 5 `flow-class-*.yaml` facts exist (X-05 substrate) |
| FR-007 single write home | **S** | X-01: path renamed to `.specify/anchoring/` |
| FR-008 `resolve-scope` drops the spec root | **D** | live reading: `spec` still accepted |
| FR-009 idempotent migration into the unified archive | **D** | no such action; `.specify/archive/` holds only `spec/` |
| FR-010 archive-not-delete + per-entry receipt | **D** | no receipts |
| FR-011 conflict stop on concept payload | **D** | no migration |
| FR-012 read-only residual probe | **D** | none |
| FR-013 contract test: zero second write path | **D** | none |
| FR-014 spec and goal+team are parallel lines | **P** | `goal-definitions.md` §*Goal vs Requirement* already states "no necessary hierarchy" / "no structural link" — the *concept* landed; the *execution* mechanism did not |
| FR-015 attribution only by binding record | **D** | trunk infers by scope (`scope: spec\|global`), i.e. by location |
| FR-016 handoff contract artifact | **D** | X-13: no `handoff.md` |
| FR-017 handoff ownership single-sided | **D** | — |
| FR-018 complexity threshold is a declared value | **D** | no `goal-team-handoff-threshold.yaml` |
| FR-019 spec keeps requirements/tasks/verification | **P** | already true by convention; no mechanism |
| FR-020 verifiable writeback per task | **D** | — |
| FR-021 concurrent lines stay decidable; duplicate slug refused | **D** | engine refuses duplicate *within one scope*, not across the two scopes we collapse |
| FR-022 stop using 临时/全局 as predicates | **P** | X-05: concept rule landed in `goal-definitions.md:42`; 4 enforcement surfaces still carry it |
| FR-023 four dimensions incl. lifecycle | **D** | no `binding` dimension; `lifecycle` exists (goal `status`, team `lifecycle_state`) |
| FR-024 concept owner is the existing definition docs | **L** | `goal-definitions.md` + `create-team/references/conceptual-model.md` are the owners today (X-03) |
| FR-025 scope set `{goal, teams, auto}` | **D** + **S** | not landed, **and** the member names now clash with the renamed archive (X-04) |
| FR-026 three global constraints restated | **L** | all three owned by `goal-definitions.md` (X-09) |
| FR-027 rewrite routing carve-out | **D** | X-06: paragraph intact at `:41` |
| FR-028 rewrite driver protocol + legacy spine keys | **D** + **S** | X-07: wrong path, no such section; `temp_*` keys already absent from the driver (`grep` = 0), so the alias half is moot |
| FR-029 sync `framework-map.md` | **D** | X-08: still `.specify/goal/` |
| FR-030 command-template scope wording as pointer | **P** | templates already defer the path rule to `resolve-scope`; they still name `global\|spec` |
| FR-031 declaration entries for command family + threshold | **P** | `shared/declarations/facts/` substrate landed (24 facts); neither of our two entries exists |
| FR-032 land in framework source, mirror; template neutrality | **P** | mirror discipline exists (`sync-mirrors.py`); our FRs are unattempted |
| FR-033 contract/unit test per decidable assertion | **D** | no such tests |
| FR-034 bidirectional key pair | **D** | X-13: `handoff_ref` = 0 |
| FR-035 `<spec-dir>/handoff.md`, one per spec | **D** | — |
| FR-036 territory as mechanical write refusal | **P** | `territory` on 10/12 team.md; `territory.write` exists; no expansion/no `forbidden` forcing |
| FR-037 `.specify/.tmp/` is not an archive row | **P** | the scratch root exists and is git-ignored; our "third row" framing is ours alone |
| FR-038 writability as a deterministic function of binding | **D** | trunk expresses it as the forbidden-path ban (085 FR-024), i.e. the mechanism FR-038 replaces (X: the ban is still live) |
| FR-039 creation timing by complexity | **D** | — |
| FR-040 command-run creation timing declared per template | **D** | — |
| FR-041 dispose of the 085 tests pinning spec-local paths | **D** | 085 tests untouched and still green |
| FR-042 dry-run migration on real data + evidence | **D** | — |
| FR-043 exhaustive backfill of `binding` on every resident definition | **D** | X-15: 6 + 12 archive residents, none bound |

### Roll-up

| Class | Count | FRs |
|---|---|---|
| **L — landed** | **2** | FR-024, FR-026 |
| **P — partial (substrate exists, mechanism does not)** | **10** | FR-004, FR-006, FR-014, FR-019, FR-022, FR-030, FR-031, FR-032, FR-036, FR-037 |
| **D — pure delta** | **28** | FR-001, 002, 003, 005, 008, 009, 010, 011, 012, 013, 015, 016, 017, 018, 020, 021, 023, 027, 029, 033, 034, 035, 038, 039, 040, 041, 042, 043 |
| **S — statement superseded as written** | **3** | FR-007 (names the removed `.specify/goal/`), FR-025 (member names clash with the renamed archive), FR-028 (names a nonexistent driver path) |

Partition check: L ∪ P ∪ D ∪ S = **43**, pairwise disjoint, no FR unclassified. (`2 + 10 + 28 + 3 = 43`.)

**Headline**: **2 of 43 FRs (4.7 %) are already landed**; **10 are partial**; **28 are pure delta**; **3 (FR-007, FR-025, FR-028) are superseded as written** and cannot be implemented until rewritten. In other words the parallel lineage landed the **concept statement** (parallelism is not hierarchy, scope is not lifetime, binding is N:1 by identity) but **none of the executable surface** our feature exists to build: no `binding` record, no migration, no residual probe, no handoff contract, no territory expansion, no declaration entries, no tests.

---

## 4. Numbering collision analysis

### 4.1 The two `092` rows on trunk

- `features.md:99` — `| 092 | Non-Disposable（不可一次性处置） | … | Planned | .specify/memory/features/092.md | .specify/specs/092-non-disposable/requirements.md |` — status note says **"merged into 090 … registry row retained as an archive pointer"**.
- `features.md:101` — `| 092 | Goal/Team Parallel（目标/施工队 × spec 并行） | … | Planned | .specify/memory/features/094-goal-team-parallel.md | .specify/specs/094-goal-team-parallel/requirements.md |` — **ours**.

Detail-file split is already in place and is **not** ambiguous:
- `features/092.md` = Non-Disposable (title line `**Feature ID**: 092`)
- `features/094-goal-team-parallel.md` = ours
- plus `features/090.md` which is now the authoritative narrative for ND (`§ Non-Disposable（不可一次性处置，absorbed from 092）`, `:43-61`)

**The collision is visible in the header arithmetic**: `features.md:4` declares `**Total Features**: 87`; the table has **88 rows** and **87 distinct IDs**; `grep -oE '^\| [0-9]{3}' | sort | uniq -d` returns exactly `| 092`. So the duplicate is a machine-detectable defect in the registry today.

### 4.2 House precedent

Two prior renumbers in this repo:

| Commit | What it did | Files touched |
|---|---|---|
| `111d03e0` "chore(088): renumber the visualization feature to 088 (the trunk's 087 is arch-diagram-docs)" | `087` → `088` | `features.md` (2 lines), `features/{087.md => 088.md}` (renamed + 14 lines), `register.md` (22 lines), `measure.py`, `status-digest.py`, `validate-roster.py`, the whole spec dir renamed with in-file identity lines, `coverage-baseline.txt`, `feature-ref.md` |
| `f5d66770` / `70d2bb1e` "renumber the local mechanism-policy feature to 083 after the remote 082 collision" / "record the renumber and final commit identity" | `082` → `083` | detail file, `review.md`, `verification.md` |

The **pattern** is: the *incoming* line yields the number; the registry header count is kept consistent; the spec directory is renamed and identity lines updated; **historical records keep their original text** (the 085 precedent says only the *identity* lines are rewritten, and the renumber note itself records the change).

### 4.3 If our line renumbers to `094`

**MUST change** (live, resolvable):
| Surface | Path today | Work |
|---|---|---|
| Spec directory | `.specify/specs/094-goal-team-parallel/` | rename → `094-goal-team-parallel/` |
| State spine | `.specify/state/094-goal-team-parallel.md` | rename; `slice:` / run_id / `stage_base_commit` lines stay as recorded history |
| Registry row | `features.md:101` | id `092` → `094`; header `Total Features: 87` → `88` is then automatically consistent (88 rows / 88 ids) |
| Feature detail | `.specify/memory/features/094-goal-team-parallel.md` | rename → `094-…md`; in-file id lines |
| Register entries | `register.md:192` (`C-01…L-03@092`), possibly any `D-*` / `REC-*` rows we own | rewrite the `@092` tag and cited paths |
| In-spec identity | `requirements.md:1` title, `:3` branch, `:5`/`plan.md` inputs, `goal/094-goal-team-parallel/goal.md`, `team/094-goal-team-parallel/team.md` (slug + `name:`), `coverage-baseline.txt`, `feature-ref.md`, checkpoints, `quickstart.md` | mechanical rewrite, 45 in-dir references |
| 14 out-of-dir references | `features.md`, `features/094-goal-team-parallel.md`, `register.md`, `.specify/state/094-goal-team-parallel.md`, 3 feedback files, 7 run-determination session files | feedback + session files are **dated records** → see below |

**MUST NOT change** (recorded history / dated evidence):
- historical commit messages (`d03fca61`, `096f825e`, …) — never rewrite history
- `.specify/memory/session/*run-determination*` files and `.specify/memory/feedback/*` files — dated one-file-per-entry records carrying `r20261109T064500Z-092a`; rewriting them would falsify a measurement record
- `test-evidence/*` readings (they quote run ids and paths as measured)
- the ND feature's own `092` (`092-non-disposable`) — it is a *different* feature and its id stays; the archive-pointer row at `features.md:99` stays as is
- the unrelated `092 handoff` notes in `.specify/agents/templates/reporter.agent.md:51`, `.specify/shared/definitions/harness-triple-definitions.md:53`, `.specify/shared/declarations/exclusions/no-harness-asset.yaml:271` — **these refer to a THIRD 092 lineage** (092 A2/A3/D3/D4 handoff items), not to non-disposable and not to us. See anomaly A-02.

**Cost of the renumber**: 16 files to edit (45 in-dir references move with the directory rename and need only in-file identity rewrite) + 1 dir rename + 2 file renames. This is **cheaper than** the 088 precedent (which touched 3 scripts + the full spec dir).

### 4.4 Counter-evidence for the renumber

The **only** consumer of the number `092` outside our line is feature `093`. Its `feature-ref.md:100-120` adjudicates overlaps with "092" and its `requirements.md:19` calls 092 *"the goal/team parallel model"* while its `:87,89,221,271` call "092" the *6-package defect*. Its `tasks.md:235` names `tests/contract/test_concurrency_reproduction_092.py` as a **filenames-stable** artifact (`SC-005` in `feature-ref.md:45`). Renumbering our line would **not** break 093 (the fixture name refers to the *defect lineage*, which is the 6-package run — a 094-goal-team-parallel execution artifact — so strictly the fixture name and 093's prose both point at us). But 093 is **itself stale** against the trunk: `requirements.md:185` says *"`goal-definitions.md` 声明 goal 持久化在 `.specify/goal/<goal-slug>/`"* — already false. Renumbering is therefore orthogonal to 093's own repair, and 093 must be repaired either way.

---

## 5. Recommendation

### Option A — renumber our line to `094`, re-scope `094-goal-team-parallel` to the delta

**Do**: rename dir / spine / registry row / detail file; keep `092-non-disposable` as the sole `092`; regenerate the requirements' premise set against `.specify/anchoring/` and the landed `goal-definitions.md`; **drop or demote** the 2 landed FRs (FR-024, FR-026) to pointers; **rewrite** the 3 superseded FRs (FR-007 → `.specify/anchoring/`; FR-025 → member names that do not clash with the renamed archive; FR-028 → the real `skills/external/sdd-loop-driver/SKILL.md` path); keep the 28 delta FRs.

- **Pro**: restores a 1:1 id↔feature mapping and fixes the `Total Features` arithmetic; follows the two-times-used house precedent; leaves ND's archive pointer intact; costs 16 edits, cheaper than the 088 precedent; lets the requirements be *re-grounded* on the trunk that now exists rather than patched around it.
- **Con**: one more renumber; 093's fixture name and prose still say "092"; the re-scope is a substantial requirements rewrite (which is required anyway — see below).

### Option B — absorb our line into `090` (like ND)

- **Pro**: matches the single user directive that produced ND's absorption ("one feature now holds both capabilities"); no id arithmetic problem (090 already holds ND); no renumber.
- **Con**: `090-re-anchoring` is **Implemented and closed** (`features.md:98` = `Implemented`); folding a 31-FR delta into a closed feature reopens its closure record, its `verification.md`, its ARC verdict, and — worse — `090`'s own `requirements.md:190,198,248` still depend on the *Temporary* predicate that our FR-022 removes. That is a contradiction **inside one feature**, and the merge note's own W3 evidence (`test-evidence/w3-V2.txt`, cited in commit `8edd955d`) already records ND-merge structural blockers (ND clause heading form, 197-row task graph over the split ceiling, ND cross-references). Adding a second absorption compounds `090`'s existing repair debt.

### Option C — keep both `092` rows with suffixes

- **Pro**: zero renumber cost.
- **Con**: the duplicate is *already* a machine-detectable defect (`Total Features: 87` vs 88 rows, `uniq -d` = `092`); every bare "092" in the repo already has **three** meanings (non-disposable, ours, and the unrelated A2/A3/D3/D4 handoff lineage). Suffixing institutionalises a permanent ambiguity in a registry the constitution designates as a single-owner canonical store. Rejected.

### Recommended: **Option A (renumber to `094`, re-scope to the delta)**

**Discriminating evidence** (why A beats B and C):
1. **Registry integrity is machine-checkable and already red** — `features.md:4` says 87, the table has 88 rows / 87 distinct ids, sole duplicate `092`. Only A makes that check green without touching ND or reopening 090.
2. **090 is closed** (`Implemented`, ARC 4/4 SC pass per its own row) and carries its own repair debt; ND's absorption already produced three recorded structural blockers. B reopens a closed feature and makes its internal contradiction (ND-FR-046/051 need "Temporary Team" while our FR-022/027 remove it) a *same-file* contradiction instead of a cross-feature one. A keeps it cross-feature and therefore adressable.
3. **A is the established pattern, measured twice** (`087→088`, `082→083`), with a known and modest blast radius (16 files; smaller than 088's).
4. **Re-scoping is unavoidable under every option**: 2 of 43 FRs landed, 3 are superseded *as written*, and the spec-local baseline (7/7) is stale against the measured 9/9. The work of rewriting the premise set is not a cost of A — it is required regardless; A is merely the option that lets the rewrite land at a clean identity.

**Cheapest partial alternative if the user rejects renumbering**: take A's *re-scope* work (fix FR-007/FR-025/FR-028, demote FR-024/FR-026, refresh the baseline) and leave the id as `094-goal-team-parallel` — the duplicate row then must be resolved by the user in the registry (ND row is already an archive pointer and *should* carry a non-`092` pointer id, which is the alternative repair the `non-disposable-definitions.md` supersede-and-renumber protocol appears to authorise for the *other* side). That path is strictly more registry surgery than A, not less.

---

## 6. Anomalies (fast-fail disclosure)

- **A-01**: our artifacts record the spec-local definition baseline as **7 goal / 7 team**; trunk measures **9 / 9** (`094-goal-team-parallel` and `092-non-disposable` each added one after the baseline). The archive baseline (6 goal / 12 team) is still correct. Classified as a **stale measurement in our artifact** — a correction the plan/tasks stage owns, **not** repaired here (this worker is read-only by dispatch).
- **A-02**: bare `092` on this trunk denotes **three** distinct things — (a) `092-non-disposable` (merged into 090), (b) `094-goal-team-parallel` (us), (c) an unrelated **"092 handoff A2/A3/D3/D4"** lineage referenced in `.specify/agents/templates/reporter.agent.md:51`, `.specify/shared/definitions/harness-triple-definitions.md:53`, `.specify/shared/declarations/exclusions/no-harness-asset.yaml:271`, `.specify/scripts/python/non-disposable-check.py:2038`, and `goal-utils.py:56,141`. A naive `s/092/094/` sweep would corrupt lineage (c). Surfaced, not repaired.
- **A-03**: the upstream rename is **partial**: `.specify/anchoring/` exists but `goal-definitions.md` still names its file `goal.md`; `--scope` still `global|spec|auto`; `framework-map.md:12`, `sdd-routing-definitions.md:41`, `skills/external/sdd-loop-driver/SKILL.md:45` and `090 requirements.md:190,198,248` all still carry the pre-rename vocabulary. Our FR-027/FR-028/FR-029 therefore remain valid delta — they were **not** superseded, contrary to what the merge note's "W2 docs" wave implies. Surfaced as scoping evidence for the user decision.
- **A-04**: several upstream artifacts were found **empty (0 bytes)** in commit `8edd955d`'s file list (e.g. `.../summary/assets/wbs.png`, `.../goal.md` under `anchoring/team` slug dirs shown as `0` insertions). This worker did **not** verify whether these are known-empty files or truncation, as it is outside W3's trunk-reconciliation domain and outside its read-only mandate to repair. Flagged for the user.

---

## 7. Evidence pointers

- Trunk HEAD: `738a42fa`; upstream merge `a72138e1`; rename+merge commit `8edd955d`
- Registry: `.specify/memory/features.md:4` (Total Features 87), `:98` (090 Implemented), `:99` (092 ND pointer), `:101` (092 ours)
- Concept owner: `.specify/shared/definitions/goal-definitions.md:25-44` (scope), `:163-182` (storage/archive), `:191-197` (binding), `:198-208` (terminology)
- Engine: `scripts/python/goal-utils.py:59` (`ARCHIVE_DIRNAME`), `:63` (`DEFINITION_FILENAME`), `:1340-1354` (`--scope` choices), live `resolve-scope` run 2026-11-09T09:04Z
- Un-migrated surfaces: `.specify/shared/definitions/framework-map.md:12`, `.specify/shared/definitions/sdd-routing-definitions.md:41`, `skills/external/sdd-loop-driver/SKILL.md:45`, `.specify/specs/090-re-anchoring/requirements.md:190,198,248`, `.specify/specs/085-sdd-temporary-goal-team/requirements.md:26,180,194,267`
- Absorbed directive: `.specify/specs/092-non-disposable/notes/refactor-anchoring-merge.md`
- Renumber precedent: `111d03e0`, `70d2bb1e`, `f5d66770`
- Downstream consumer: `.specify/specs/093-concurrency-by-default/{requirements.md:19,87,89,185,221; tasks.md:235; feature-ref.md:45,100-120}` (worktree `093-clarify`)
