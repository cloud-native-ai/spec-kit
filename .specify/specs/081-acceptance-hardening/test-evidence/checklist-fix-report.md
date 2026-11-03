# Checklist-Fix Report — Feature 081, slice 081a

**Stage**: `checklist-fix` (spec-only repair; no implementation code, no template/skill/script source, no `.specify/` mirror touched)
**Branch**: `081-acceptance-hardening` · **Base commit**: `67054707` (checklist stage)
**Input checklist**: `checklists/acceptance-2026-11-03.md` (39 items, 28 PASS / 11 FAIL)
**Fixed**: the 8 clear gaps of the dispatch brief § 1 — CHK004, CHK005, CHK008, CHK024, CHK025, CHK027, CHK035, CHK036
**Deferred to `/speckit.analyze`** (semantic/policy, not repaired — see § 3): CHK012, CHK017, CHK021
**Files changed**: `requirements.md`, `plan.md`, `tasks.md`, `data-model.md`, `contracts/{closure-acceptance-check,state-vocabulary,artifact-schemas,gate-wiring}.contract.md`

---

## 1. The eight fixed gaps

### CHK025 — one canonical spelling for the seven closure reason literals

The literals were spelled three ways (trailing colon in the Shared Strings table, no colon in contract C-09, mixed in plan/tasks prose).

- **Owner established**: `requirements.md` § Shared Strings now carries the seven canonical forms verbatim — `STR-008` `zero-final-path-pass`, `STR-009` `final-path-not-pass: SC-NNN`, `STR-010` `blocked-without-measurement-ladder: SC-NNN`, `STR-011` `runtime-dependency-not-owned: RS-NNN`, `STR-012` `falsified-premise-undecided: EP-NNN`, `STR-013` `inherited-blocker-undisposed: <feature>:<row>`, `STR-014` `status-claims-implemented-but-blocked` (`requirements.md:241-247`).
- **Rule stated once**: the colon is the argument separator, a bare code carries no trailing colon, the argument placeholder may not be rewritten, and no consumer may introduce a second spelling (`requirements.md:254`).
- **Citations aligned**: FR-006 now lists the seven `[[STR-…]]` references without the old "(后接 `SC-NNN`)" glosses (`requirements.md:140`); the three bare-literal US2 scenarios now cite the string IDs (`requirements.md:79`, `:81`, `:82`); contract C-09 lists the seven values with their arguments and points at the Shared Strings owner (`contracts/closure-acceptance-check.contract.md:23`); AS-08 (`contracts/artifact-schemas.contract.md:18`) and GW-05 (`contracts/gate-wiring.contract.md:15`) quote the canonical forms; `plan.md:266` and `tasks.md:110`, `:197`, `:219`, `:233` use the canonical forms; `data-model.md:47`, `:101` drop their duplicate bare codes in favour of the `[[STR-NNN]]` reference.
- **Verification**: a repository-wide grep for the seven literals inside the five artifact families now returns **0** occurrences without an argument, without a trailing colon, and **0** occurrences of the old trailing-colon spellings.

### CHK005 — GATE-5 asserts `Blocked`, not "not Implemented"

- **GATE-5** (`tasks.md:30`) now asserts the registry cell prints exactly ` Blocked `, and states that `Implemented` **and** the pre-slice `Planned` both fail the check — so an untouched registry can no longer pass it.
- **DoD-5** (`tasks.md:19`) is written as a two-carrier value assertion: `.specify/memory/features.md` column 5 **and** `.specify/memory/features/081.md` `**Status**` both read `Blocked`.
- **The missing write now has a row**: `Planned → Blocked` is landed by T020 (`tasks.md:124`), which previously seeded only `verification.md`. Without it the strengthened gate would have been unsatisfiable; FR-003 already authorises exactly this transition for a slice with non-`pass` `final`-path SCs.
- **Contradiction removed**: `Implementation Strategy` step 4 said "Do not advance the feature status"; it now reads "Land the status as `Blocked` (T020) and do not advance it past that" (`tasks.md:176`), and the `## Slice Boundary` consequence bullet says the registry row must read **exactly `Blocked`** (`tasks.md:227`).
- **Template-vocabulary contradiction resolved explicitly**: `templates/feature-index-template.md` was measured (21 lines, `Status` column header only, no value-domain list) to carry no vocabulary at all, while FR-018 names it a vocabulary owner. The resolution is recorded where the obligation lives, not by editing the template (spec-only stage): `contracts/state-vocabulary.contract.md:16` (SV-06) and `tasks.md:235` (081d row) now state that the measured state is header-only and therefore the obligation is to **add** a closed status vocabulary containing `Blocked` — not to insert one value into a list that does not exist. `plan.md:260` (D3 row) carries the same measured fact.

### CHK004 — duplicate `Blocked` transition table removed from `data-model.md`

- The full `From | To | Allowed | Condition` table is gone from `data-model.md` § E-8 and replaced by a **pointer**: the row set is owned by `shared/workflow/acceptance-hardening.md` § Feature Status ([[STR-017]]) and physically carried by `templates/feature-details-template.md` § Canonical Status State Machine (FR-002 / FR-003 / FR-018) (`data-model.md:140`). The two rules the checker reads (V-23, V-24) stay.
- **`contracts/state-vocabulary.contract.md:13` (SV-03)** no longer designates `data-model.md` § E-8 as "the row set"; it points at the owner and states that neither this contract nor `data-model.md` restates the rows.
- **Uniqueness guard extended** (the "do not leave the duplicate unguarded" half of the gap): SC-009 ④ now declares `data-model.md` and `contracts/` **projection surfaces** — exempt from the hit counter, with the exemption itself tested: (a) `data-model.md` must contain **0** transition-table rows, (b) every value-domain literal used in a projection surface must be a member of the owner's exported domain (`requirements.md:209`). The exemption's reason is stated at the top of `data-model.md` (`:5`) and the test carrier is named (`requirements.md:221`).

### CHK024 — `tests/contract/test_acceptance_schema_ownership.py` gets a carrier

The module was cited by two contracts but existed in no inventory and no slice.

- **Plan inventory**: added to `plan.md` § Source Code `tests/` with its purpose and slice (`plan.md:178`), and named in Constitution Check row IV (`plan.md:42`). `test_gate_wiring_081.py` — cited by the same row but likewise absent from the tree listing — was added to the inventory in the same edit (`plan.md:177`).
- **Task-level assignment**: the 081d `## Deferred Slices` row now names the module and its two assertions (`tasks.md:235`), and the FR/SC coverage row for SC-009 names it plus the slice that owns it (`tasks.md:219`).
- **Contract citations kept** (they are now backed): `contracts/artifact-schemas.contract.md:43` and `contracts/gate-wiring.contract.md:47`.
- **Counts kept honest**: `plan.md:29` moves 41→42 source surfaces and tests 14→15 accordingly.

### CHK036 — DoD-6 aligned to the set-level invariant

- `tasks.md:20` now states SC-009 ②'s invariant at set level: `head 失败集 − 基线失败集` empty, `基线失败集 − head 失败集` enumerated as fixed items, comparison unit = failing-test **id set** (never a count, never a byte diff), baseline = `baseline-failed.txt` (39 ids, plan-stage capture).
- The narrower touched-module observation is stated **separately and subordinated**: GATE-1's four modules green "MUST NOT stand in for the set-level invariant", and the closing set-level run is assigned to 081d (which the FR/SC coverage table already assigns FR-023's id-level differencing to). This removes the silent narrowing without inventing a new closing obligation for 081a.

### CHK008 — one form for the ladder field names and the illegal-row trigger

- **Field names**: `SC-NNN_blocked_at`, `SC-NNN_reduced_measurement`, `SC-NNN_reduced_measurement_run`, `SC-NNN_why_reduced_insufficient`, `SC-NNN_unblock` — now used verbatim in `requirements.md:138` (FR-004), `requirements.md:204` (SC-004), `tasks.md:108` (T013), `tasks.md:124` (T020), `data-model.md:47` (V-6), `contracts/state-vocabulary.contract.md:22` (SV-09), `contracts/closure-acceptance-check.contract.md:36` (C-16), `plan.md:258` (D3 row). No unprefixed form remains.
- **Illegal-row trigger**: defined exactly as "`SC-NNN_reduced_measurement` **non-empty** AND `SC-NNN_reduced_measurement_run=no`" (`requirements.md:121`, `:138`, `:204`; `data-model.md:45`; SV-09; C-16; `plan.md:258`), with the semantic "可用/available" wording explicitly retired — the trigger reads *non-empty*, not "available".
- **Fixture inputs** restated in the same vocabulary (`tasks.md:69` T004; `data-model.md:190`).

### CHK035 — implement-step references point at the real steps

Measured in `skills/internal/implement-feature/SKILL.md`: `### Step 8 — Completion validation` (line 249) and `### Step 9 — Pre-Status-Flip Gate and Verification Log` (line 310); the status flip happens in Step 9.

- `tasks.md:102` (T010) — "step 8" → **Step 9 — Pre-Status-Flip Gate and Verification Log** (the step where the status is landed).
- `tasks.md:111` (T016) — "step 8" → **Step 8 — Completion validation** (re-validation at the completion gate) **and Step 9** (status landing, where the checker runs before the flip).
- `plan.md:261` (D3 row) — "steps 8–9" → the two named steps.

### CHK027 — the mixed `final`/`supporting` fixture exists

- **New task** `T021` (`tasks.md:70`, `[P]`, Phase 1) authors three path-mix fixtures: `mixed-path/` (one failing `final` beside a passing one, plus one non-`pass` `supporting`), `expr-supporting-only/` (an `expression` feature not forced to invent a `final` SC) and `execution-without-final/` (an `execution` feature with zero `final`-path SC fails).
- **Expectations recorded** in `data-model.md:192-194` and in the plan's fixture list (`plan.md:251`), which also picks up the previously unlisted `smoke-mutation`.
- **Asserting test**: `T007` now asserts `mixed-path` → `final-path-not-pass: SC-NNN` naming the failing SC and **not** `zero-final-path-pass`, plus the `expr-supporting-only` exemption (`tasks.md:99`); its `[blockedBy:]` gains `T003,T004,T021` — the fixtures it reads (`tasks.md:99`, `:149`).
- **One clause added so the fixture is assertable**: `data-model.md:80` (V-11) now states that for an `expression`-class feature the `final`-path rule is vacuous, so no `final`-path reason is emitted when there is no `final` SC. This is the mechanical reading of FR-001 ("`expression` 类特性不受该下限约束") + Edge Case "只有 supporting SC 的表达类特性"; without it the second half of the brief's rule had no parser-level statement.
- **Ceiling**: task rows 20 → 21 (≤ 40).

---

## 2. Gate outputs (verbatim)

`python3 scripts/python/validate-requirements.py .specify/specs/081-acceptance-hardening/requirements.md`

```
file: .specify/specs/081-acceptance-hardening/requirements.md
status: ok
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] pass (0)
  [marker-count] pass (0)
  [dup-id] pass (0)
scanned: 270 lines, 34 definition rows, 17 shared strings
0 error(s), 0 warning(s)
EXIT=0
```

`python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/081-acceptance-hardening --stage tasks`

```
pre-analyze-check: stage=tasks decision=pass errors=0 advisories=0 waived=0
{"stage": "tasks", "decision": "pass", "findings": [], "summary": {"errors": 0, "advisories": 0, "waived": 0, "fr": 25, "sc": 9, "tasks": 21, "clauses": 66, "files": 14}, "checked_at": "2026-11-03T00:00:52Z"}
EXIT=0
```

Targeted structural checks run by hand (no suite run, per the brief):

- the 9 SC definition lines each carry exactly one `**Path**` marker and it is the line's last token (9/9);
- the seven closure reason literals appear 0 times without their argument and 0 times in the retired trailing-colon spelling;
- the five ladder field names appear 0 times without the `SC-NNN_` prefix.

---

## 3. Deferred to `/speckit.analyze` (no policy invented)

| CHK | Open question | Where it lands | Why it was not repaired here |
|---|---|---|---|
| **CHK012** | Whether a pin that is a transcript of one machine's `--version` output satisfies FR-009 (`commit` / `digest` / `version`), and what invalidates it (venv rebuild / machine change) and which gate detects that | `requirements.md:189-190` (RS-002 / RS-003 Pin cells), `plan.md:306` (D8), `test-evidence/plan-runner-pins.txt` | Answering it decides *what a pin is* — two defensible readings (a recorded observation vs a declared repository value) and no artifact records which one is intended |
| **CHK017** | What obligation the `inherited` disposition imposes (what is inherited, with what evidence); `plan.md:229-232` currently uses a meaning no owner declares | `requirements.md:148` (FR-011), `contracts/artifact-schemas.contract.md:23` (AS-10), `plan.md:229-232` | Defining the obligation is new policy for a three-value closed set; the requirements only fix the literals |
| **CHK021** | Whether the artifact-review denominator is "artifacts that exist" or "artifacts that must exist for this stage" — i.e. whether a missing-but-expected artifact is a finding or a silent skip | `requirements.md:25`, `:206` (SC-006), `contracts/review-composition.contract.md:16` (RC-06) | It changes the artifact segment's coverage semantics (and SC-006's measurement), which is a scoping decision, not a repair |

---

## 4. Corrections made in passing (disclosed)

Each is a single-reading repair of an internal inconsistency the eight fixes touched; none changes an FR/SC number, deletes a requirement, or alters the slice boundary.

1. **`plan.md:60`** cited `data-model.md` § "F1–F9", a section that does not exist; corrected to § Fixture set while the fixture list was extended.
2. **`plan.md:42` / `:177`** — `test_gate_wiring_081.py` was cited as a red-first contract test but was missing from the plan's `tests/` tree listing; added (CHK024's inventory-completeness fix applied to the sibling case it exposed).
3. **`tasks.md:99` (T007)** had no `[blockedBy:]` although it reads fixtures authored by T003/T004; the edges were added together with the new T021 edge.
4. **`plan.md:29`** surface counts recomputed for the added guard module (41→42, tests 14→15).

---

## 5. Assumptions

- **A-1**: `Planned → Blocked` is the transition the slice must land (FR-003 + DoD-5 + `## Slice Boundary`); T020 is the row that performs it because it is the row that already writes the slice's closing state. No new policy was needed — the write was simply absent.
- **A-2**: The `Blocked` row set's schema owner is `shared/workflow/acceptance-hardening.md` § Feature Status ([[STR-017]], FR-022/A7/D1) and its physical carrier is `templates/feature-details-template.md` § Canonical Status State Machine (FR-002/FR-003/FR-018). Both statements were already in the artifacts; the repair only removed the third (duplicate) location.
- **A-3**: The `expression`-class exemption in V-11 is a restatement of FR-001 + the existing Edge Case, not a new rule; it was added because the new fixture asserts it and no parser-level clause existed.
