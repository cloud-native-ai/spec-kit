# Package 2a stage status — 089-script-interface-contract (T012–T019, US4 red-first)

**Scope**: Phase 3 US4's **test band only** (T012–T019). Eight rows, no implementation row.
**Tree**: `/cws_data/cloud-native-ai/spec-kit`, branch `089-script-interface-contract`, parent `5068bf7c`.
**Run**: 2026-11-06, implement stage, package 2a of ~6.

---

## 1. Per-task completion

| Task | Status | Artifact | Red reading (what is missing) |
|---|---|---|---|
| T012 | done | `tests/contract/test_script_interface_contract.py::test_c23_*` | **PASSES today** — the owner page landed in package 1, so C-23 is satisfied; the assertion is the guard for it, not a red-first pair |
| T013 | done | same file, `test_c24_*` (2 rows) | RED — `templates/constitution-template.md` holds 18 numbered principles, none titled `Script Interface Contract (Declared, Zero-Side-Effect)`. Closing owner: **T020** |
| T014 | done | same file, `test_c25_*` (2 rows) | RED — `.specify/memory/constitution.md` holds 19 principles, none titled that; head Sync Impact Report still names the 1.16.0 amendment. Closing owner: **T023** |
| T015 | done | same file, `test_c26_*` | RED — the `- **MUST include**` block holds 11 sub-entries, expected 12. Closing owner: **T021** |
| T016 | done | same file, `test_c27_*` (3 rows) | RED — `## Script Interface Contract` heading count is 0 on both `templates/instructions-template.md` and `.specify/instructions.md`. Closing owners: **T022** (template), **T024** (live reconcile) |
| T017 | done | `tests/contract/test_constitution_double_landing.py` — three pins raised, watchlist 6 → 7, plus a new `test_c10_newest_watchlist_entry_is_caught_by_the_mutation_probe[template|command]` | RED — 7 failures: template 18/19, live 19/20, mandate 11/12, and the new watchlist entry absent from both sides. Closing owners: **T020/T021/T023** |
| T018 | done | `test_c29_*` (3 rows) | RED (partially — see § 4): the four labels are read out of the page successfully (that row passes), but the pointer row and the leak-scan row are red for two different reasons |
| T019 | done | `test_c30_*` (2 rows) | RED — `scripts/python/script-interface-check.py` does not exist. Declared red target of T019's own `[blockedBy: T018,T065]`; closing owner **T032/T045** |

## 2. Commands and readings (this package's own evidence)

| # | Command | Reading |
|---|---|---|
| 1 | `/usr/bin/python3 -m pytest -q tests/contract/test_script_interface_contract.py tests/contract/test_constitution_double_landing.py` | **18 failed, 17 passed**, exit 1 — captured in `T012-T019-red.txt` |
| 2 | same, `test_script_interface_contract.py` alone | 11 failed, 3 passed |
| 3 | same, `test_constitution_double_landing.py` alone | 7 failed, 14 passed |
| 4 | `/usr/bin/python3 .specify/scripts/python/validate-tasks.py .specify/specs/089-script-interface-contract/tasks.md` | `PASS (with warnings)`, **0 error(s), 62 warning(s)** — the pre-package reading, unchanged (the file's Notes record 62 as the adjudicated residue) |
| 5 | `grep -cE '^- \[[ >]\]' tasks.md` | **68** (was 76; eight rows closed) |

## 3. What the new test file asserts, and where each set comes from

The file's design rule is that **nothing it compares against is typed twice**:

- the four help-content labels are grepped out of the owner page's closed-set sentence;
- the classification-steps literal is read from the page's `### 1.4` heading;
- the house shape is the sibling guard's `_check_structure`, imported by path — C-24 says "the
  house shape *already asserted* for every principle in that file", so the owner of that
  judgement is reused rather than re-implemented;
- the exemption-table columns come from C-30's own enumeration (the contract is that owner).

`test_c24_template_principle_points_at_the_owner_and_does_not_copy_its_steps` and
`test_c29_*` therefore run against a list that changes with the page, not with the test.

## 4. Anomalies surfaced (not repaired in place)

- `ANOMALY A-1` — **the banned-literal scan as the clause words it collides with ordinary English
  prose that predates this feature.** Reading the four labels out of the owner page works (the
  derived list is `('usage', 'options', 'side-effects', 'exit-codes')`), but scanning the five
  landing surfaces for those four bare words finds pre-existing hits:
  `templates/constitution-template.md:142,149` (the word *options* inside Principle XI) and
  `templates/instructions-template.md:110,178` / `.specify/instructions.md:122,190` (the word
  *usage* inside the Token Efficiency and Dogfooding sections). No 086 landing produces any of
  them. Two readings exist and this package does not own the choice: (a) the guard must match the
  owner page's *closed-set form* (the label tokens as the page publishes them, not as free-standing
  words); (b) the clause intends a narrower literal set. The guard is written to the clause's
  wording and is red; the discriminating reading is a decision for the row that turns it green
  (T022/T020) or for the clause's owner. Surfaced rather than pre-empted.
- `ANOMALY A-2` — **T019 cannot go green inside Phase 3.** Its `[blockedBy: T018,T065]` names T065,
  a Phase 4 row, so this US4 test row is red against an engine (`script-interface-check.py`,
  T032/T045) that Phase 4 builds. The row is written and closed as a *test* row; its green point
  is Phase 4 by the tasks file's own declaration, not by this package's choice.

## 5. Corrections repaired in passing (disclosed)

- **The owner page's label paragraph is hard-wrapped**, so a line-anchored grep read only 3 of the
  4 labels (`exit-codes` sits on the next line). The extractor now reads the whole paragraph. The
  page is unchanged; the *guard's* matcher was the defect.
- **C-23's "ends with `## Declared Exceptions`"** was first read as "last `##` section in the
  file". The page ends with three apparatus sections after the register. Re-read as what the
  clause enumerates: the register is the **fifth of the five owned items** and closes that block;
  the page's trailing scope disclaimer and consumer tables are not owned items. The assertion now
  states that reading explicitly instead of asserting an order the clause never fixed.
- **The label paragraph's own follow-on clause names the JSON key `labels`**, which the naive
  backtick scrape picked up as a fifth "label". The extractor excludes that one token by name and
  says why.
- **T017's mutation probe was pinned to `DOUBLE_LANDING_WATCHLIST[0]`**, so extending the
  watchlist widened what C-7 asserts without widening what C-10 proves it can catch. A new
  parametrized row proves the newest entry is catchable on both sides. This is the "re-assert that
  the `c10` mutation probe still catches a missing landing" limb of T017's own text.

## 6. Assumptions taken (unattended run — recorded, not asked)

1. **The eight closed rows are closed as *test* rows**, not as green rows. `tasks.md` § Tests says
   the assertion lands before the implementation row that turns it green; a test row that is
   correctly red is a finished test row.
2. **No implementation surface was touched**: `templates/constitution-template.md`,
   `.specify/memory/constitution.md`, `templates/instructions-template.md` and
   `skills/internal/manage-constitution/SKILL.md` are byte-unchanged by this package (package 2b
   owns them). `tests/contract/test_constitution_double_landing.py` is edited only in its three
   count pins, its watchlist tuple, and one added test.
3. **The `[P]` markers on T012/T016 were left as the tasks file has them.** The residue warning is
   the one `tasks.md` § Notes already adjudicates; editing that adjudication is the tasks owner's
   call.
