# V3 — trunk reconciliation + the two record corrections

**Verifier**: fork worker V3 (read-only)
**Worktree**: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/093-clarify`
**Branch / HEAD**: `093-concurrency-by-default` @ `c5abfaaa`; master merged at `95e44f3a`
**Objects under test**: 093 artifacts against the merged trunk's rename / re-number state; the F-093-012 correction set; the F-093-004 / T138 ruling; SC-006's stated reason
**Method**: every claim re-measured from the artifacts themselves (`grep -rn`, file reads, `git log` on the touched paths). No artifact was edited; this file is the only write.
**Independence note**: V1 verified the repair ledger's own scoped claims (and its F-093-012 row HOLDS as scoped). This fragment is about the *residual* surface: what the same correction left untouched outside the ledger's five named records.

## 0. Trunk state measured in this worktree

| Fact | Reading |
|---|---|
| `.specify/goal/` | **absent** (`ls` → exit 2) |
| `.specify/anchoring/` | exists, **6** entries: `command-logic-as-classified-skills`, `draw-diagram-interactive`, `draw-two-layer-structure`, `post-refactor-mechanism-integrity`, `session-driven-self-improvement`, `skill-layer-install-separation` |
| Owner page | `shared/definitions/goal-definitions.md:3` declares itself single source of truth; `:31` global scope = Anchoring at `.specify/anchoring/<slug>/goal.md`; `:34` **"No 'temporary' property. A scope is not a lifetime"**; `:44` and `:189` map the retired names forward ("Temporary Goal" / "Temporary Team" → spec-scoped Goal / team); `:180` says the directory rename is the path side of the concept rename |
| Partial rename (confirmed, not repaired by 093) | `scripts/python/goal-utils.py:59` `ARCHIVE_DIRNAME = ".specify/anchoring"`; `:63` `DEFINITION_FILENAME = "goal.md"`; `:146`/`:1339` `--scope` closed set still `global / spec / auto` |
| Checkpoint protocol section name | `skills/sdd-loop-driver/references/checkpoint-protocol.md:19,171` → **"## 2. Goal progress"** (093's checkpoints say "Temporary Goal progress") |
| Feature registry | `features.md` carries **two `092` rows**: row with 092 Non-Disposable (merged into 090, archive pointer) and row with 092 Goal/Team Parallel; 093 is row 093 |

---

## 1. `.specify/goal` and the retired vocabulary — hit table

Scan basis: `grep -rn '\.specify/goal'` over the whole spec dir, plus `grep -rn 'temp_goal_slug|temp_team_slug|temporary goal|Temporary Goal|临时'` over the live artifacts. **`temp_goal_slug` / `temp_team_slug`: zero hits anywhere in 093.**

| # | file:line | what it says | class | verdict |
|---|-----------|--------------|-------|---------|
| H1 | `requirements.md:185` (FR-032 continuation) | "项目级 scope 即**锚点（Anchoring）**，持久化在 `.specify/anchoring/<slug>/goal.md`（该目录自 090 起由 `.specify/goal/` 改名而来）… MUST NOT 被读成「持久 vs 临时」的生存期差异" | aligned | **mechanically aligned by the repair** — old path appears only as a rename gloss; the lifetime rule matches `goal-definitions.md:34` |
| H2 | `requirements.md:293` (Clarifications, requirements session) | A-part: "…`.specify/teams/<slug>/`、**`.specify/goal/<slug>/`**；「枚举根 → 执行体类别」的映射由 [[STR-008]] …" | stale | **still stale (finding V3-F2)** — contradicts `requirements.md:133` FR-001 "goal 定义根 `.specify/anchoring/<slug>/`"; no dated note marks the supersession |
| H3 | `requirements.md:307` (Clarifications, clarify session) | Q names `.specify/goal/<slug>/`; A: "`goal-definitions.md` 声明 goal 持久化在 **`.specify/goal/<slug>/`** … FR-032 因此显式区分「**存档目标**」与「**临时目标**」" | stale + behavioural conflict | **still stale (finding V3-F1)** — the A-part is a normative answer that (a) gives a path the owner page no longer has, and (b) restates the exact 持久-vs-临时 lifetime reading that the live FR-032 (`:185`) forbids and `goal-definitions.md:34/:44` retires. The conflict is **not** recorded as a finding anywhere; repair § 3.1 filed these lines as "dated records" only |
| H4 | `tasks.md:76` (T003) | "`ls -d .specify/anchoring/*/` → **6** (the former `.specify/goal` tree, renamed by 090 and merged 2026-11-09 …)" | aligned | **mechanically aligned** — measured path + historical gloss |
| H5 | `research.md:100` (R-6 table) | "`.specify/anchoring/<slug>/` \| 6 \| anchoring entries (the former `.specify/goal/` tree, renamed by 090 …)" | aligned | **mechanically aligned** |
| H6 | `quickstart.md:41` | "6 `.specify/anchoring` slugs … the anchoring tree was `.specify/goal` before the 090 rename merged on 2026-11-09" | aligned | **mechanically aligned** |
| H7 | `checklists/2026-11-09-requirements-quality.md:16` (CHK001) | "FR-001 逐字给出**五个**枚举根（… `.specify/goal/<slug>/`） … 实测：… `.specify/goal` 6" | stale | **still stale (finding V3-F5)** — dated checklist, no correction note; repair § 3.1 records the exemption but leaves no dated mark in the file |
| H8 | `checklists/2026-11-09-requirements-quality.md:55` (CHK027) | "`.specify/goal/*/` 6 个 … FR-032 逐字区分「存档目标」与「临时目标」" | stale | **still stale (finding V3-F5)** — same as H7, and it repeats the retired lifetime reading |
| H9 | `notes/analyze-repair.md:73,77` | § 3.1 measures the rename and records the partial-rename facts (file still `goal.md`, `--scope` still `global\|spec\|auto`, `register.md` first rows still `.specify/goal/...`) | aligned | **aligned** — the ledger's own account is accurate; `register.md` first rows do still carry `.specify/goal/...` (measured), so the "trunk-side inconsistency recorded, not repaired" statement holds |
| H10 | `test-evidence/v2-pre-analyze-check.txt:2,6,10`; `test-evidence/checklist-readings-2026-11-09.txt:61`; `test-evidence/analyze-repair-gates.txt:1383,1389,1395`; `test-evidence/analyze-repair-gates-attempt1.txt:1378,1384,1390` | old path inside captured gate output | excluded | **dated evidence** — correctly left per repair § 3.1 and the single-run-evidence rule |
| H11 | `checkpoints/01-requirements.md:9`, `02-clarify.md:11`, `03-plan.md:15`, `04-tasks.md:14`, `05-checklist.md:19`, `06-analyze.md:15` | section heading "## 2. **Temporary Goal** progress" | stale vocabulary (dated records) | **still stale (finding V3-F6)** — the shipped protocol now reads "## 2. Goal progress" (`checkpoint-protocol.md:19,171`). Heading-only, no behavioural content; a dated note would be the discipline-consistent fix |
| H12 | `tasks.md:308` (T135) | "… the spec-local **temporary goal layer** stays owned by the earlier goal/team feature (FR-032)" | stale vocabulary | **still stale (finding V3-F7)** — the ownership statement is *correct* under FR-032; only the adjective is retired ("scope is not a lifetime") |
| H13 | `plan.md:106` (T-002 antithesis) | "临时 team 模式 `min(effective_concurrency, 24)` …" | adjacent (trunk-side) | **not a 093 defect** — `goal-definitions.md:189` retires "Temporary Team", but the page 093 cites, `skills/internal/create-team/references/conceptual-model.md:94`, still defines "A **Temporary Team** is a spec-attached, run-scoped team" verbatim. Two trunk owner pages disagree; 093 follows the live page. Observation only |

**Counts**: 13 rows / 28 line-anchors — aligned **6**, stale **11**, adjacent-trunk-side **1**, excluded-dated-evidence **10**.

---

## 2. Duplicate-092 record

**Verdict: RECORDED — no finding.**

| Requirement | Evidence |
|---|---|
| The duplicate fact is recorded | `notes/analyze-repair.md:42` (F-093-019 row) + `:79` (§ 3.2) + `:108`; `register.md:199` (F-093-019, status `recorded`); spine `state/093-concurrency-by-default.md:85` ("F-093-019 NEW (MEDIUM, recorded) duplicate-092 numbering …") |
| Impact on fixture row T090 | `tasks.md:235` T090 carries the in-place disambiguation: "'092' here is **092-goal-team-parallel** (the 6-package plan), not the 092-non-disposable row absorbed into 090 by the 2026-11-09 merge — the numbering collision is recorded as F-093-019" |
| Impact on the reproduction suite name | Stated in the same three places: filename `tests/contract/test_concurrency_reproduction_092.py` is **kept as-is** ("renaming would break every reference"); `plan.md:219`, `quickstart.md:91`, `research.md:188`, `feature-ref.md:47`, `tasks.md:227/331/356` all use that name consistently |
| No renumber performed | Stated and true here: every "092" in 093 still means 092-goal-team-parallel; the naming decision is self-consistent in this tree |

**Forward note (not a finding against this tree)**: the MAIN tree's `29c3aa08` renumbers 092-goal-team-parallel → 094, and `.specify/.tmp/sdd-loop/tmp/renumber-094.sh` deliberately does **not** touch 093. After that renumber, a bare "092" in 093 inverts to the *Non-Disposable archive pointer*, and T090's own disambiguation sentence ("092 here is 092-goal-team-parallel") becomes wrong. The driver's promised T090-naming reconciliation must therefore also sweep `requirements.md:19/87/303`, `plan.md:282/301/385`, `research.md:134/149/183/188`, `quickstart.md:88/91/95`, `feature-ref.md:47/124`, `tasks.md:225/227/235/255/307/331/356` — not only T090's row.

---

## 3. F-093-012 — record by record

Scope tested: the five records that asserted "the executing body holds `Read, Grep, Glob, Bash, Write, Edit` — no dispatch tool" (the set `analyze-findings.md:92` names: "the five checkpoints, `plan.md` and `tasks.md` § Environment Prerequisites" — measured: only checkpoints **03/04/05** carry the tool claim; 01/02 carry no tool-set claim at all, so the five records are `plan.md` + `tasks.md` + 03/04/05), plus every other record that still states the premise.

| Record | State | Evidence |
|---|---|---|
| `plan.md` § Concurrency plan (L336-341) | **corrected** | "…was **measured false at analyze 2026-11-09 (F-093-012)** … a tool set is a per-run probe (RS-005), never a constant. What is genuinely absent is the feature's own mechanism — the declaration facts, the engine, and the fork runner path of FR-035" |
| `plan.md` R-3 (L385) | **corrected** | "The earlier premise 'the host still has no dispatch tool' was measured false at analyze (F-093-012) — the host holds one, and the fixture rests on neither." |
| `tasks.md` § Environment Prerequisites (L44) | **corrected** | "**corrected at analyze 2026-11-09 (F-093-012): the executing body holds a host dispatch tool** … the `mechanism-not-yet-landed` code rides on the feature's own deliverable … not on the host's tool set. Affected phases/tasks: T101 / T103 / T105 and the SC-006 evidence plan (T106 / T110)" — the wrong `T102` pointer is gone |
| `tasks.md` § SC-006 evidence plan (L369) | **corrected** | "the executing body **holds a host dispatch tool** — the earlier 'no Agent/Task tool' reading was wrong … the gap is the missing mechanism, not missing work." |
| `checkpoints/03-plan.md` | **annotated** | dated banner `:3` ("Correction (2026-11-09, analyze-repair · F-093-012) … The body of this dated checkpoint is left as written"); body `:25` intact |
| `checkpoints/04-tasks.md` | **annotated** | dated banner `:3`; bodies `:19`, `:24`, `:57` intact |
| `checkpoints/05-checklist.md` | **annotated** | dated banner `:3`; bodies `:24`, `:30`, `:42` intact |
| `checkpoints/01-requirements.md`, `02-clarify.md` | **n/a** | neither asserts a tool set (measured: zero hits for "Read, Grep", "capability", "工具") |
| `checkpoints/06-analyze.md` | **self-correcting** | `:27` records the measured contradiction and files F-093-012; `:52` restates the SC-006 reason with the disclosure beside it |
| `research.md` R-10 (L144) | **untouched → finding V3-F4** | still reads "Measured: this planning stage ran in one agent with `Read, Grep, Glob, Bash, Write, Edit` — no dispatch tool." This is a **live** plan-stage artifact; the correction set (`analyze-repair.md:35`) lists only `plan.md`, `tasks.md`, `plan.md R-3`, and checkpoints 03/04/05 |
| `quickstart.md` S-6 (L116) | **untouched → finding V3-F3** | "This feature's own run does not satisfy S-6 … the executing **agent has no dispatch tool**, so it declares serial with `mechanism-not-yet-landed`" — the same false premise in a live Phase-1 artifact, and it is the artifact a passer reads to understand S-6 |
| `checklists/2026-11-09-requirements-quality.md` CHK043 (L80) | **untouched → finding V3-F3** | "本线的阶段执行体工具集为 `Read, Grep, Glob, Bash, Write, Edit`（**无派发工具**），机制本身是本特性的交付物" — the file was touched by the repair (header count note), but CHK043's reason was not; no correction note |
| `research.md:183` (R-14) | **acceptable as-is** | "six declared packages, one coordinator, no dispatch tool" describes the *fixture's declared shape* / the 092 record, not this line's executor. Not the corrected premise; no finding |

**Five-record verdict: 2 corrected + 3 annotated = 5/5 handled. Residual: 3 records untouched (2 live, 1 dated checklist).**

---

## 4. F-093-004 / T138 — wording check (no re-adjudication)

| Check | Reading |
|---|---|
| Ruling recorded — findings § 2 | `notes/analyze-findings.md:39-77` § 2: disagreement table, ruler (glossary 绿点归属 → `templates/tasks-template.md:110`), ruling "`[green:]` is a **red-first marker**", corollary "the partition invariant survives, scoped to claimed clauses", and the explicit "093 claims 35 of 92" reading |
| Ruling recorded — register | `register.md:197` — owner named, ruling cited, status `resolved（2026-11-09, analyze）` |
| Ruling recorded — spine | `state/093-concurrency-by-default.md:85` — "F-093-004 [green:] semantics — RESOLVED … the marker reading wins, the partition invariant survives scoped to claimed clauses (093 claims 35 of 92) … fix recorded as implement row T138 … NOT edited in this stage" |
| T138 exists | `tasks.md:311` (Phase 8 Polish; also in `WP2-engine`, `tasks.md:354`; row count 143 confirmed at `tasks.md:419`) |
| T138 framework-source targets | `scripts/python/validate-tasks.py` (rule block ~L44-46 + emitted message ~L501-516 + `--help` banner), `.specify/scripts/python/validate-tasks.py` (mirror, regenerated, never hand-edited), new `tests/contract/test_validate_tasks_green_semantics.py` (red if a totality claim returns; green-partition assertion ≥1 claim / 0 double-claimed / 0 dangling); `templates/tasks-template.md` L110 named as the **owner** (pointer only) — all present |
| Wording consistency | Findings § 2.3's sketch → landed T138 matches sentence for sentence (marker reading, strict-subset allowance, both file targets, test's two arms); T138 additionally folds in F-093-015's dead-owner re-point, exactly as `analyze-repair.md` says F-093-015 was routed. One label delta: the sketch reads "T138 **[US5]**", the landed row carries **no** user-story tag because it sits in Phase 8 (Polish) — correct for the tasks format, not a defect |

**Verdict: PASS (wording only).**

---

## 5. SC-006 — status and stated reason

**Status: `not_evaluated` everywhere it is stated — unchanged, correct.**

| Location | Stated reason | Verdict |
|---|---|---|
| `plan.md:336-342` | "the feature's own mechanism — the declaration facts, the engine, and the fork runner path of FR-035" is absent; `mechanism-not-yet-landed`; no claim of concurrency | **aligned** (mechanism, not host tool) |
| `tasks.md:44` | "the `mechanism-not-yet-landed` code rides on the feature's own deliverable … not on the host's tool set" | **aligned** |
| `tasks.md:365-369` | "what is missing is the feature's own mechanism … not a host tool"; forbids `0`, estimates, and fixtures-as-proof | **aligned** |
| `notes/analyze-findings.md` F-093-011 | "the only thing that closes SC-006 is the feature's own engine running on the feature's own implement run" | **aligned** |
| `checkpoints/03-plan.md:20`, `04-tasks.md:19`, `05-checklist.md:24`, `06-analyze.md:20,52` | body reasons name "no dispatch tool" but each file carries the F-093-012 dated banner / disclosure | **annotated** |
| `quickstart.md:116` | "the executing **agent has no dispatch tool**" — the reason a reader of S-6 is given | **stale reason → finding V3-F3** |
| `checklists/2026-11-09-requirements-quality.md:80` (CHK043) | "（**无派发工具**）" | **stale reason → finding V3-F3** |

`verification.md` does not exist yet (implement-stage artifact); no `SC-006_status=` claim exists anywhere, so nothing fabricates a value.

---

## 6. Findings (verification-local ids — not registered F-093 ids; promote before citing durably)

| id | severity | finding | anchors |
|----|----------|---------|---------|
| V3-F1 | **MEDIUM** | The clarify-session answer states the retired storage path **and** the retired 持久/临时 lifetime reading as normative. It directly contradicts FR-032 in the same file (`:185` "MUST NOT 被读成「持久 vs 临时」") and the trunk owner (`goal-definitions.md:34` "No 'temporary' property", `:44` retired naming). An implementer reading the Q&A instead of FR-032 takes the wrong path (`.specify/goal/` — absent) and the forbidden lifetime model. The repair filed this line as a "dated record" (§ 3.1) but recorded no dated note and no finding | `requirements.md:307` vs `:185`; `goal-definitions.md:34,44` |
| V3-F2 | LOW | The other clarify answer still names `.specify/goal/<slug>/` as the fifth enumeration root, contradicting FR-001 (`:133` `.specify/anchoring/<slug>/`). Path-only, and FR-001 is unambiguous, so a builder fails loudly rather than silently | `requirements.md:293` vs `:133` |
| V3-F3 | **MEDIUM** | SC-006's stated reason still attributes `not_evaluated` to the host's tool set in two surfaces outside the F-093-012 correction set: the live quickstart S-6 (the artifact a passer reads) and the dated checklist's CHK043. Contradicts the corrected reason (`plan.md:336-342`, `tasks.md:44,369`) and makes the ledger's "SC-006 reason aligned" claim over-broad | `quickstart.md:116`; `checklists/2026-11-09-requirements-quality.md:80` |
| V3-F4 | **MEDIUM** | A live plan-stage artifact still states the corrected premise as a measurement: research R-10 "this planning stage ran in one agent … — no dispatch tool". F-093-012's repair list omits `research.md`, so the false constant survives beside its own correction in `plan.md` | `research.md:144` |
| V3-F5 | LOW | The dated checklist still carries `.specify/goal/...` as the fifth root (CHK001) and as the two-layer goal home plus the 临时目标 reading (CHK027). The file was touched by the repair (header count note) but these two items carry no dated correction note | `checklists/2026-11-09-requirements-quality.md:16,55` |
| V3-F6 | LOW | All six dated checkpoints use the retired section name "## 2. Temporary Goal progress"; the shipped protocol reads "## 2. Goal progress". Heading only; rewriting a dated record would be worse than annotating it | `checkpoints/01:9`, `02:11`, `03:15`, `04:14`, `05:19`, `06:15`; `checkpoint-protocol.md:19,171` |
| V3-F7 | LOW | T135 keeps the retired adjective ("the spec-local **temporary goal layer**") while stating the correct ownership under FR-032. Wording only | `tasks.md:308` |
| V3-F9 | LOW | The analyze ledger's own count is imprecise: "The **five checkpoints**, `plan.md` and `tasks.md` § Environment Prerequisites **all assert** … no dispatch tool" and "five consecutive stages asserted 'no dispatch tool'". Measured: only checkpoints 03/04/05 make that assertion; 01/02 record serial execution from a different, still-valid reason ("single read/write package/slice"). Dated record; no verdict depends on it | `notes/analyze-findings.md:92,197` |

Non-findings recorded for completeness: plan.md:106's "临时 team" (the cited framework page still defines the term — trunk-side divergence, observation); research.md:183's "no dispatch tool" (describes the 092/fixture shape, not this line's executor); all `test-evidence/*` old-path captures (dated evidence).

---

## Verdict

- § 1 hit table: **6 aligned / 11 stale / 1 adjacent-trunk-side / 10 excluded-dated-evidence** (28 anchors, 13 rows).
- § 2 duplicate-092: **recorded** — F-093-019 in ledger + register + spine; T090 disambiguated in place; suite name kept and the decision stated. Forward note: the MAIN-tree 092→094 renumber will invert bare "092" references inside 093; the driver's reconciliation must sweep beyond T090.
- § 3 F-093-012: **5/5 named records handled** (2 corrected, 3 annotated with dated notes over intact bodies); **3 residual records untouched** (V3-F3 ×2, V3-F4).
- § 4 F-093-004 / T138: **PASS** — ruling in findings § 2 + register + spine, T138 present with framework-source targets; wording consistent.
- § 5 SC-006: status `not_evaluated` consistent; **reason stale in 2 surfaces**.

V3: FAIL — V3-F1 (MEDIUM: requirements.md:307 retired path + 持久/临时 lifetime reading contradicts FR-032/:185 and goal-definitions.md:34), V3-F3 (MEDIUM: SC-006 reason still "no dispatch tool" in quickstart.md:116 and checklist CHK043), V3-F4 (MEDIUM: research.md:144 R-10 keeps the corrected false premise), V3-F2 / V3-F5 / V3-F6 / V3-F7 / V3-F9 (LOW: stale path in requirements.md:293; stale goal path + vocab in CHK001/CHK027; retired checkpoint heading ×6; retired adjective in T135; ledger's "five checkpoints" count imprecise)
