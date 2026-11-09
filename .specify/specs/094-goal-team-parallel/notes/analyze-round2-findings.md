# Analyze Round 2 — Independent Verification and Verdict (092, 2026-11-09)

Read-only analyze round 2 at main workspace `master@7b3597c2`. Scope: independently verify the 14-item
round-1 repair (`notes/analyze-round1-repair.md`, commit `dae4a26c`), adjudicate the four residual risks
handed to round 2, and run a fresh full pass over requirements / plan / tasks / contracts / checklist.

**Verdict: NOT READY TO IMPLEMENT.** Round 2 finds **1 CRITICAL + 4 HIGH** still open. Two of the four are
re-openings of findings the repair reported *closed*, and the root cause is mechanical and auditable: the repair
commit `dae4a26c` **never touched `plan.md` or `feature-ref.md`** (`git show --stat dae4a26c -- plan.md
feature-ref.md` is empty), while `requirements.md` line 259 asserts that `plan T-004` had been brought into
agreement. The claims were recorded as closed; the artifact edits were not made.

Counting: 1 CRITICAL / 4 HIGH / 4 MEDIUM / 3 LOW. A repair brief is in § 6.

## 1. Closure verification — 14 round-1 rows

Claim checked against the artifact itself, not against the repair prose. "Holds" = the artifact says what the
repair claims; "Does not hold" = the artifact contradicts the claim (counted as a round-2 finding).

| Row | Repair claim | Verified against | Result |
|---|---|---|---|
| C-01 | FR-006 + A9 use `source: ledger` vs `source: default` as the discriminator | `requirements.md` FR-006 (L131), A9 (L303); engine re-measured | **Holds** on requirements; **fails downstream** — see C-2 |
| H-01 | All 111 clauses carry a trailing `(FR-…)` citation group; FR lane 42/42 | `account-clause-coverage.py --corpus-root` → `fr-uncovered pass (0) — 42 of 42`; all 111 clause blocks carry ≥1 group under the owner's grammar | **Holds** (grammar fragility adjudicated in § 3) |
| H-02 | FR-025 is the single owner of `{goal, teams, auto}`; FR-008/A1 point at it | FR-025 (L150) owns it; FR-008 (L133) and A1 (L295) point at FR-025 | **Fails** — `plan.md` T-004 (L132 heading, L134 decision) still says `global` / `auto`; the plan was never edited |
| H-03 | One contiguous A1–A11 block | 11 A-lines, ids A1…A11, no duplicates, one `## Assumptions` section | **Holds** in body; **fails in the section preamble** — see M-2 |
| H-04 | Mis-cites fixed; superseded A1 recorded as superseded | A2 → `FR-006、FR-031`; A3 → `FR-018 / FR-031`; A4 → `FR-024`; superseded A1 recorded verbatim in § Notes (L275) | **Holds** |
| H-05 | T043 `[blockedBy: T015,T054]` in wp03; T054 `[blockedBy: T015,T053]` | `tasks.md` L239 / L269; wp03 = 19 rows (`T016–T027, T043, T049–T054`), wp05 = 16 | **Holds** (19-row ceiling adjudicated in § 3) |
| M-01 | A6 unified to one reading (`085–091`) | A6 L300 states `085–091` 各一对 | **Holds** |
| M-02 | FR-005 `FR-032` → `FR-031`; RS-003 row fixed | FR-005 L130 cites FR-031; RS-003 L179 `FR-031` | **Holds** |
| M-03 | A9 rewritten in `source` terms | A9 L303 | **Holds** |
| M-04 | FR-009 carries the no-lineage prohibition; A11 points at it | **FR-009 (L134) contains no such sentence** — no `谱系` / `lineage` / `MUST NOT 重建`; A11 (L305) and § Notes (L277) both assert FR-009 carries it. A contract does carry it: C-36 (`unified-archive-and-migration.md` L40-42) | **Does not hold as stated** — see M-1 |
| M-05 | FR-041's double A7 citation left intact, recorded in § Notes | FR-041 L166 cites A7 twice; L285 records the decision | **Holds** |
| L-01 | One paragraph after § E stating all 42 FRs register under A | requirements.md § E paragraph L169 | **Holds** |
| L-02 | Stage record refreshed in index row + feature detail | `features.md` 092 row L100; `features/092.md` L36–45 | **Holds** |
| L-03 | Residual: generation name on 8 surfaces, C-107 does not scan `.specify/specs/**` | 8 `team.md` files carry `name: SDD Temporary Team …` (085–092, incl. 088 at `team/team.md`) | **Holds as described** (adjudicated in § 3) |

**Closure tally: 11 of 14 rows hold, 1 partial (H-03 body yes / preamble no), 2 do not hold (H-02, M-04).**

## 2. Findings by severity

### CRITICAL

**C-2 — Contract C-71 states the predicate C-01 proved undecidable, and contradicts FR-006/A9/C-72.**
`contracts/command-family-and-declarations.md` L11 still reads: "the command's carrier exists **and**
`flow-class-check.py --action lookup … exits 0 with a registered class**". Round 1 C-01 established, and round 2
re-measured, that this admits the wrong answer:

```
/speckit.feedback            flow_class=execution source=ledger  exit 0
/speckit.nonexistentcommand  flow_class=execution source=default exit 0
```

`/speckit.nonexistentcommand` satisfies C-71's predicate (carrier-absent is not in the predicate; exit 0 holds;
`execution` is a registered class) yet FR-006 and A9 say it MUST NOT be in the family, and C-72 says the lookup's
exit codes are the *only* inputs and that a carrier-absent command is not in the family. An implementer following
C-71 builds the defect round 1 was raised to prevent, and C-72's guard test would fail against C-71's predicate.
No contract clause anywhere names the `source` field (`grep -c ledger contracts/*.md` = 0 across all five pages) —
C-01's repair stopped at `requirements.md` and never reached the conformance layer that `feature-ref.md` names as
the conformance owner. Evidence: `test-evidence/analyze-round2-engine-measurements.txt` § 1–2.

Why CRITICAL and not HIGH: the contract layer is the implementer's instruction set, and this clause directs the
wrong predicate with a green-looking example. It also voids the SC-008 measurement surface (`test_command_family`
/ family closed-set) for the case the feature exists to handle.

### HIGH

**H-2 — `feature-ref.md`'s FR → contract-clause map is stale for 36 of 42 rows.**
`feature-ref.md` L18–34 map each FR to clause ids. Checked against the citation groups the repair itself installed
(the authoritative reverse map), **only 6 of 42 rows name a clause that cites that FR**; the other 36 name a
clause in the right contract file but that does not cite the FR at all. The offsets are not a uniform shift
(−58 … +53), so this is a map authored against an earlier clause layout and never regenerated — not a renumbering
that can be corrected by arithmetic. Examples: FR-005 (command family) → "binding-and-lifecycle C-18, C-19" (a
team-lifecycle clause; the real clauses are C-71/C-72/C-75); FR-014 (peer lines) → "C-11, C-12" (scope resolution;
real: C-25); FR-021 (duplicate slug refusal) → "C-17" (goal lifecycle; real: C-27); FR-022 (temporary/global ban) →
"command-family… C-77…C-80" (declaration facts; real: C-105/C-107/C-108). `plan.md` L63 and L374 both certify this
map as "42/42", so the plan's Constitution Check row I rests on a reading that does not hold. `feature-ref.md` is
the published view of the citation rule (`contract-clause-definitions.md` § 7 names it a consumer), and an
implementer using it lands on the wrong test. Evidence: computed reverse map over `contracts/*.md`.

**H-3 — C-1 requires a binding record on *every* goal/team definition, but 18 existing archive residents have none and no FR, clause or task owns their backfill.**
`contracts/binding-and-lifecycle.md` L14-16: "A goal definition and a team definition MUST each carry exactly one
binding record … A definition without a complete binding record MUST be rejected as uninterpretable (exit 2,
`binding-missing`)." Measured on this tree:

```
.specify/goal/*/goal.md  : 6 definitions, binding present: 0
.specify/teams/*/team.md : 12 definitions, binding present: 0
```

These are the *unified archive*, i.e. the post-feature landing zone — and they predate the feature. The migration
subject is the 8+8 **spec-local** definitions (FR-009 / C-35 source scope), and plan EP-002 explicitly verifies
that the two sets do not collide in slug, so migration neither creates nor touches these 18. Once C-1's
`binding-missing` rejection is implemented, every one of these 18 definitions becomes unreadable by the engine. No
FR, clause or task row owns a backfill: `grep -n "backfill\|既有定义.*绑定"` over requirements / contracts / tasks
returns nothing, and T005 only *authors the reader*. This is an unstated assumption of the highest blast radius in
the feature (it would break `/speckit.goal`, `/speckit.team`, `run-team` and the driver on the current tree), and
it is exactly the class of gap the closed-set/decidable-claim discipline is meant to catch.

**H-4 — The prescribed lookup invocation `--unit-id command:<name>` is not in the engine's unit-id grammar.**
C-71, C-72, C-74 and task T020 all prescribe `flow-class-check.py --action lookup --unit-id command:<command>`.
The engine's `UNIT_ID_RE` is `^(?:/speckit\.[a-z0-9][a-z0-9-]*|skill:[a-z0-9][a-z0-9-]*)$`, and the documented
form is `/speckit.<stem>` or `skill:<dir>`; `command:feedback` is rejected as `invalid-unit-id`, exit 2. The
consequence interacts with C-2: under C-71's predicate "exits 0", every command would be *out* of the family
because the lookup always exits 2 on the malformed id — the opposite of the intended reading and a silent
family-wide denial. Requirement FR-006 itself says "复用既有的类别读取入口" without naming a unit-id form, so the
requirement is satisfiable; the error is introduced at the contract and task layer. Fix: use
`--unit-id /speckit.<command>`. Evidence: measurements file § 3.

**H-5 — The repair note records a closure that the artifacts do not contain (H-02 / M-04), and the requirement text repeats the false claim.**
Two rows are reported closed with named edit sites that were never edited:

- H-02: the repair says "契约 C-9、`features/092.md`、plan T-004 与 quickstart 的 `--scope goal` 均已一致,本阶段只改
  FR-008 / FR-025 / 假设 A1 三处正文" (`notes/analyze-round1-repair.md` and requirements.md L259). `requirements.md` L259
  also states "Plan T-004 … 写 `{global, auto}`" as the *prior* state and implies it is now aligned. It is not:
  `plan.md` L132 (`### T-004 — 引擎作用域取值收窄为 `global` / `auto`…`) and L134 (`只保留 `global` / `auto``) are
  unchanged, and `git show --stat dae4a26c -- plan.md` is empty. The T-004 decision record — the one document the
  DoD names as the design owner and the tension record that `validate-decision-tensions.py` validates — still
  carries the rejected reading, with its `antithesis` and `discriminating_evidence` written against `global`.
- M-04: A11 (L305) and § Notes (L277) both say "该禁令的规范面由 FR-009 承载"; FR-009 (L134) has no such clause. The
  prohibition *is* carried (C-36), so the substantive gap CHK007 raised is closed at the contract layer — but the
  pointer is false, and a reader following it finds nothing.

Why HIGH: the artifacts that a verifier reads to decide "can we implement" and that the next stage inherits now
contain a false statement of their own state, and one of them (T-004) is the load-bearing decision record for the
largest semantic change in the feature.

### MEDIUM

**M-2 — The `## Assumptions` section preamble contradicts its own body.** L291 reads "`A1`–`A8` only; `A9`–`A11`
are the clarify-stage additions that follow" and describes "Two blocks had accumulated here". After the H-03 merge
there is one block of A1…A11 in a single contiguous list; the sentence describes a two-block history that no longer
exists and draws a boundary (A8/A9) that the body does not have. Exactly one reading is consistent with the
recorded intent (the H-03 merge, verified in the body), so this is an in-passing correction — see § 5.

**M-3 — The engine's default scope and two of its guidance strings recommend values FR-025 deletes.**
`goal-utils.py` L1416 defaults `requested_scope = "auto" if args.action == "resolve-scope" else "global"`, and
L166 / L1418 emit `pass --scope global or --scope spec`. After FR-008/FR-025 both suggested values are invalid.
T013 owns narrowing `choices=` and T014 owns `resolve_scope`, but neither names the default literal nor the two
message strings, and no FR states that in-engine guidance text MUST stay inside the declared domain. An implementer
who follows T013/T014 literally leaves the engine printing instructions that its own parser now rejects.

**M-4 — CHK030's gap is still open in substance: FR-006 delegates the closed-set ruling to an Assumption.**
FR-006 ends "〔未声明类别的命令不入族见假设 A9〕" and no FR sentence carries "未声明 = 不入族" (`grep -n 不入族
requirements.md` hits only FR-006's pointer, § Notes and A9). The checklist row CHK030 was raised precisely because
this ruling sits only in an Assumption; the repair strengthened A9's *content* but did not promote the rule to the
FR layer, so the checklist finding is not closed by its own criterion. Low blast radius (A9 is now unambiguous) but
it is a checklist fail row with no closure record.

**M-5 — The checklist's 8 fail rows are all still `fail` in the file; 7 are closed in fact, CHK007 is open and
carries a false premise.** The checklist explicitly does not self-refresh (L78), so stale `fail` markers are
expected; but no recheck file exists and the analyze stage is the owner of that transition. Worse, CHK007 asserts
"`## Functional Requirements` 中没有任何一条 FR 承载…" — true — and the repair answered it by moving the prohibition
into a *contract* (C-36) while simultaneously writing two false pointers to FR-009 (H-5). A recheck would mark
CHK007 closed-by-contract and clear the false pointers.

### LOW

**L-4 — 088's `team/team.md` declares `name: SDD Temporary Team 087` under `slug: 088-speckit-visualization`.**
A pre-existing generation defect (not introduced by 092), but it is one of the 8 surfaces residual L-03 counts, and
it weakens "8 surfaces" as a uniform class — one of them carries a *wrong number* as well as the retired name.

**L-5 — `feature-ref.md` discloses "Clarifications Q1–Q12" while requirements now carries Q1–Q12 plus a Q13 and the
analyze-repair session.** Minor bookkeeping drift in the same file as H-2.

**L-6 — `notes/analyze-round1-repair.md` § 2 lists gate readings as "(stdout, this slice)" for three rows instead of
naming an evidence path**, while the deliverable convention is a retained file under `test-evidence/`. Round 2
re-ran and retained all of them, so evidence now exists; the note's pointers remain unfilled.

## 3. Residual-risk adjudications (the four handed to round 2)

### (a) L-03 — "Temporary Team" generation name on 8 surfaces — **does not block implement; an implement-stage question, with one correction to the framing.**

Verified: 8 `team.md` files carry `name: SDD Temporary Team <NNN>` (085, 086, 087, 088, 089, 090, 091, 092 — 088's
is at `team/team.md` rather than `team/<slug>/team.md`, and it says "Team 087" — L-4). C-107's scan surface is
`shared/`, `skills/`, `scripts/`, `templates/`, `src/` and genuinely excludes `.specify/specs/**`, so no gate sees
these. Adjudication: **not a spec defect and not an implement blocker**, for a reason the repair note did not give:
the `name:` field is free text (`create-team/references/create-mode.md` L57 `name: <display name>`), and no template
or generator emits the string (`grep -rn "SDD Temporary Team" skills/ shared/ templates/` = 0 hits). So nothing in
the feature will *re-create* these names; rewriting them is an optional data edit. Two refinements belong to
implement, and neither is a requirements change:

1. The *classification wording* that C-107 does scan is in scope and already owned: `conceptual-model.md`
   ("Temporary (Run-Scoped) Team"), `goal-definitions.md`, `sdd-routing-definitions.md` — 5 hits across 3
   runtime-surface files, all covered by T068 / T067 / T044. Note this contradicts a claim in the repair note: it
   says C-107's surface "不含 `.specify/specs/**`" as if the concept were unscanned; the concept *is* scanned via
   the `skills/` mirror (`skills/internal/create-team/references/conceptual-model.md` exists and is byte-identical
   to the `.specify/` copy), so the gap is narrower than stated — only the free-text `name:` values are unscanned.
2. If implement does rewrite the 8 names, it must also fix 088's wrong number (L-4), or the "uniform 8-surface"
   framing stays false.

### (b) H-01 grammar dependence — **real, bounded, and not a blocker; the gate is sensitive, the blind spot is narrow.**

Two things were measured rather than reasoned about. First, the gate **is** sensitive: deleting every FR-005
citation drives `fr-uncovered` to `fail (1) — 41 of 42`, so the lane is not green-by-construction. Second, the
fragility named in the residual is real: appending a trailing non-FR parenthetical after C-1's citation group left
the run at `pass (0) — 42 of 42`, because the owner's grammar defines the citing position as the block's **last**
FR-bearing group and C-1's citation was masked — though in that particular probe no FR lost coverage because C-2..C-4
carry the same group. So the failure mode is: a clause that *uniquely* cites an FR, edited to end with an unrelated
parenthetical, drops that FR from the lane and the count still passes if another clause covers the FR. Adjudication:
**accept as a documented fragility, not a blocker.** The mitigation is a one-line guard the implementation already
has a home for: assert per-clause that the last group is FR-bearing (the FR lane's `fr-uncovered` checks FR→clause
reachability, not clause→group shape). Recorded here so the implement stage does not inherit it silently.

### (c) H-05 wp03 at 19 rows against the plan's 16-row target — **accept; no split required.**

The 16-row figure is a *target* in `plan.md` L331 ("per-package ceiling 16 rows, never 60+ in one executor") and
`decomposition-model.md` § 13, with the hard gate being the 6-slot cap. Verified: wp03 = 19 (`T016–T027, T043,
T049–T054`), wp05 = 16, wp01 = 15, wp02 = 14, wp04 = 8, wp06 = 6, wp07 = 2 — 80 rows, one row per ID, no
double-assignment (computed from the declared ranges; only T043 carries an explicit `[owner:]` tag). The tasks note
already discloses the composition and argues the extra rows are test-authoring, not source writes. Adjudication:
**19 is accepted.** Splitting wp03 would either re-open the H-05 defect (moving T043 back to a package with no edge
on its blocker) or shave the package below a coherent unit; the ceiling's purpose is executor cost, and 19 rows
over one package's four disjoint engine sections plus tests stays inside it. This is a recorded acceptance, not an
oversight — but it should be recorded *in the plan*, not only in tasks.md § Notes, because the plan is where the
ceiling is declared.

### (d) FR-025 removes `spec` from the scope domain while `goal-utils.py` and 085–091 carry spec-scoped data — **migration rows own the data; they do NOT own the code.** 

The data side is covered and I confirm it: the migration subject is the 8 goal / 8 team spec-local definitions
(C-35 / FR-009), receipts carry `source_spec` (C-33), `origin` is set from the source spec basename (C-36), and
conflict comparison excludes the binding rows so a migrated file is not "non-equivalent to itself" (C-40 / FR-011).
plan EP-002 verifies the two trees' slugs do not collide. T079 runs the real-data sequence with retained readings.

The **code** side is the gap, and it is M-3: `goal-utils.py` still holds 7 hardcoded `"global"` literals
(`resolve_scope` default parameter L120, membership tuple L127, `Scope("global", …)` at L155/L169, the argparse
`choices` tuple L1312, the runtime default L1416) and two user-facing strings (L166, L1418) that recommend
`--scope global`/`--scope spec`. T013 (choices) and T014 (`resolve_scope` + Scope object) cover most of the
literals; the default at L1416 and the two strings at L166/L1418 are covered by neither. So the answer to (d) is:
**the migration rows own the data, and they were never meant to own the code — but the code sweep has three
unowned items that must be added.** This is filed as M-3, not as a new CRITICAL, because it is local and additive.

## 4. Fresh full pass — requirements / plan / tasks / contracts / checklist

Checked: duplication, ambiguity, underspecification, internal inconsistency, unstated assumptions, coverage
(FR→task→SC→evidence), constitution conflicts.

| Axis | Reading |
|---|---|
| FR count / contiguity | 42, `FR-001…FR-042` contiguous, no gaps, no duplicates (`validate-requirements` `id-contiguous` / `dup-id` pass) |
| SC count | 11 (`SC-001…SC-011`), each with a `Path:` and a Measurement Source |
| FR → task | 42 of 42 FRs cited from at least one task row (computed over the 80 rows) |
| SC → task | 11 of 11 SCs cited from at least one task row |
| FR → clause (citation groups) | 42 of 42 reachable; every FR cited by ≥1 clause |
| FR → clause (`feature-ref.md` map) | **6 of 42 correct** — H-2 |
| Clause count / contiguity | 111 clauses, `C-1…C-111` contiguous across 5 pages, no id shared between pages |
| Clause → citation group | 111 of 111 blocks carry ≥1 FR-bearing group |
| Cross-contract duplication | 0 near-duplicate normative sentences across pages |
| Task partition | 80 rows / 7 packages, ranges cover 78 + wp07's 2, no double assignment, write domains disjoint by declaration |
| Forward dependency | 1 (`T043 → T054`) — disclosed in tasks § Notes / Package Map / DO NOT-2, intentional |
| Decision tensions | 7 records, all fields present, `validate-decision-tensions` ok — but **T-004 records the rejected reading** (H-2/H-5) |
| Unstated assumptions | the 18 pre-existing archive residents (H-3) |
| Constitution conflicts | none new; row I's "42/42" certification rests on the stale map (H-2) |

Two checks I could not make green and did not paper over: the `feature-ref.md` map (H-2) and T-004's decision text
(H-2/H-5) are the two places where a machine gate is green and the artifact is wrong. Neither the map nor the
decision record is covered by any re-derivable gate — `validate-decision-tensions.py` checks field presence and
tension-id linkage, not that the decision matches the FR it points at, and nothing parses `feature-ref.md`'s table.
That is the structural reason these two slipped through round 1's repair and round 1's own gates.

## 5. In-passing corrections applied (each: exactly one reading consistent with recorded intent)

Per the round-2 brief, only MEDIUM/LOW corrections with a single consistent reading were applied; C/H findings are
surfaced, not fixed.

1. **M-2 — `## Assumptions` preamble.** Replaced the stale "`A1`–`A8` only; `A9`–`A11` … follow / Two blocks had
   accumulated" sentence with a statement that matches the merged body (one contiguous A1–A11 block, merge rule and
   the two diffs recorded in § Notes). One reading: the H-03 merge is verified in the body, and the Notes section
   already records the diffs; the preamble was the only place still describing the two-block state.
   Before: "`A1`–`A8` only; `A9`–`A11` are the clarify-stage additions that follow. Two blocks had accumulated
   here …" / After: a four-line preamble stating one contiguous `A1`–`A11` block (11 lines, no duplicate ids, no
   sub-blocks), that `A9`–`A11` are clarify-stage additions *within the same block*, and that the merge happened
   2026-11-09 with its two diffs recorded in § Notes. `validate-requirements.py` re-run after the edit:
   `status: ok`, 0 error / 0 warning, 307 lines (was 306).

No other in-passing correction was made. In particular I did **not** touch `plan.md`, `feature-ref.md`, the
contracts, `tasks.md`, or T-004: the correct value for T-004 is a decision among recorded readings (its antithesis
and discriminating evidence are written against `global`), and re-authoring a decision record is a decision, not a
correction — fast-fail says halt and surface, so H-2/H-5 are reported instead.

## 6. Repair brief (round 2 does not fix C/H)

Order matters: 1 and 4 are one edit; 2 depends on nothing; 3 is a requirements-layer decision that should be made
before 1 lands, because C-1's rejection is what makes the 18 residents unreadable.

1. **C-2 — rewrite C-71's predicate.** Replace "exits 0 with a registered class" with the `source` discriminator as
   FR-006 states it (in family ⇔ `source: ledger`; `source: default` ⇒ not in family, `marker: 未声明·按默认`), and
   align C-72's "only inputs" sentence with it. Add the `source` field to at least one clause so the conformance
   layer carries the discriminator at all. Then re-check `feature-ref.md`'s FR-005/FR-006 rows (couples to 2).
2. **H-2 — regenerate `feature-ref.md`'s FR→clause map** from the citation groups (the same reading the FR lane
   uses), or delete the map and keep the reverse direction as machine-generated. Update `plan.md` L63 and L374,
   which certify it as "42/42".
3. **H-3 — decide the backfill, and record the decision.** Either (a) add an FR + clause + task that backfills
   `owner` / `owner_id` / `origin` on the 6 goals and 12 teams already in `.specify/goal` and `.specify/teams`
   (their owner is most plausibly `human`, `origin: null`, but that is a *decision* and must be recorded, not
   assumed), or (b) scope C-1's rejection to definitions created or migrated by this feature and state explicitly
   that pre-existing residents are read-compatible. Either way the choice must be visible in requirements, because
   it decides whether the feature lands on a working engine or a broken one.
4. **H-4 — fix the unit-id form** in C-71, C-72, C-74 and T020 from `command:<command>` to `/speckit.<command>`,
   and state the accepted grammar so it is not re-guessed.
5. **H-5 — correct the two false pointers and the repair note's closure claim.** Either edit `plan.md` T-004 to the
   `goal`/`teams`/`auto` reading (re-authoring its antithesis / discriminating evidence against the new member set)
   or record in T-004 why the plan-level record intentionally keeps the pre-H-02 wording; and either move the
   no-lineage prohibition into FR-009 or change A11 / § Notes to point at C-36. Re-state requirements L259's
   "plan T-004 已一致" to match whatever is true after the edit.
6. **M-3 — add three unowned code items** to T013/T014: the runtime default at `goal-utils.py` L1416, and the two
   guidance strings at L166 / L1418.
7. **M-4 / M-5 — promote the "unregistered ⇒ not in family" ruling into FR-006's own sentence** (or record why the
   Assumption placement is accepted), and write a `recheck-<date>-assumptions.md` that closes CHK007/CHK013/
   CHK014/CHK017/CHK028/CHK030/CHK036/CHK038 with pointers to where each was answered.
8. **Close the structural blind spot in § 4**: nothing re-derives `feature-ref.md`'s map or checks that a decision
   record's decision matches the FR it names; until something does, both H-2 and H-5 can recur silently.

## 7. Gate readings (all re-run this round; evidence retained)

| Gate | Command | Reading | Evidence |
|---|---|---|---|
| requirements structure | `validate-requirements.py …/requirements.md` | `status: ok`, 0 error / 0 warning, 306 lines / 53 definition rows | `analyze-round2-validate-requirements.json`, `analyze-round2-gates.txt` |
| clause / FR coverage | `account-clause-coverage.py … --corpus-root …/.specify/specs` | `status: ok`; `fr-uncovered pass (0) — 42 of 42`; 0 uncovered beyond the 598-name baseline | `analyze-round2-coverage.json`, `analyze-round2-gates.txt` |
| tasks structure | `validate-tasks.py …/tasks.md` | `PASS (with warnings)` — 0 error, 1 warning (`T043 → T054` forward dependency, disclosed) | `analyze-round2-validate-tasks.json`, `analyze-round2-gates.txt` |
| decision tensions | `validate-decision-tensions.py --spec …` | `status: ok`, 7 records, 0 error / 0 warning | `analyze-round2-gates.txt` |
| pre-analyze ×3 | `pre-analyze-check.py --repo … --spec-dir … --stage {requirements,plan,tasks}` | all `decision: pass`, errors 0, advisories 86, fr 42, sc 11, tasks 80 | `analyze-round2-precheck.txt` |
| decomposition | `decomposition-check.py --mode tasks --requirements … --tasks …` | `proceed` — fr=42 (ceiling 120), tasks=80 (ceiling 160) | `analyze-round2-precheck.txt` |
| engine measurements | see file | C-01 discriminator, C-71 contradiction, unit-id grammar, archive residents, repair-commit scope | `analyze-round2-engine-measurements.txt` |
| coverage without `--corpus-root` | `account-clause-coverage.py …` | `status: ok` this round (the driver's 57-false-name reading is cwd-dependent; retained for the record) | `analyze-round2-coverage-no-corpus-root.txt` |

All six mandated gates are green. **Every one of them is green while C-2, H-2, H-3, H-4 and H-5 are open** — which
is the round-2 headline: the gate set verifies structure, counts and field presence, and none of them reads whether
a contract clause agrees with its FR, whether a published map resolves, or whether a REQUIRED field is
unsatisfiable on the live tree.

## 8. Verdict

**NOT READY TO IMPLEMENT** — 1 CRITICAL + 4 HIGH open. The round-1 repair closed 11 of 14 rows cleanly and the
six gates are green, but two closures were recorded without their edits (`dae4a26c` never touched `plan.md` or
`feature-ref.md`), one was closed at the wrong layer (C-01 stopped at requirements while the contracts still carry
the refuted predicate), and one requirement (C-1) is unsatisfiable on the repository as it stands. Repair per § 6,
then re-run analyze round 2 over the affected artifacts (requirements, plan, contracts, feature-ref, tasks) — the
gates will not catch these on their own.
