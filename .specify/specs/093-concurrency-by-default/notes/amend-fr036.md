# Amendment ledger — FR-036 (test entry = the xdist runner only)

**Date**: 2026-11-09
**Directive (user, 2026-11-09)**: 「the spec-kit test framework MUST enforce the pytest-xdist runner as the ONLY
test entry. Every test execution in framework artifacts must go through `scripts/bash/run-tests.sh` (its default
is `-n <effective> --dist load`); raw `python3 -m pytest` / `pytest` invocations are forbidden because
full-suite single-process runs slow every SDD run. The rule is enforced by a guard test.」
**Routing verdict**: `sdd-capability-or-contract-change` (2026-11-09T11:14:16Z; rule owner
`.specify/shared/definitions/sdd-routing-definitions.md` § Verdict table) — a framework capability/contract
change, so it rides the SDD artifact chain rather than a direct edit.
**Execution**: serial, one executor; `mechanism-not-yet-landed` (the FR-035 fork mechanism is not landed in this
line), so no concurrency is claimed for this amendment run.

## 1. What changed, where

| Artifact | Change |
|---|---|
| `requirements.md` | **FR-036** added contiguously after FR-035 (rule, runner path/arg pass-through, two exemption classes, guard judgment + EXACT allowlist); Clarifications gains **Session 2026-11-09 (amend · 用户裁定：测试入口唯一化)** quoting the directive and the routing verdict; live FR-count claims updated `FR-001…FR-035` → `FR-001…FR-036` (Reading scenario, FR-030). |
| `plan.md` | New bounded section **§ Test-entry enforcement** (rule statement surfaces + guard test + allowlist; explicitly *not* a decision tension — the user ruling fixes the choice, 086's runner contract is consumed unchanged); FR-count claims 35→36 (Input, Scale/Scope, Constitution row I, artifact inventory, gate record); test-module count 10→11 (contract modules where the basis was contract-only; new-test-module lines get +1); guard module added to the Phase-1 file tree. |
| `tasks.md` | Rows **T156–T159** added under Phase 8 (Polish): T156 instructions template + live-instructions refresh, T157 driver dispatch surfaces (test-entry sentences only; 094 wp05 convergence is serialized by the driver), T158 executor guidance in MUST form + the measured raw-pytest sweep, T159 the guard contract test with the EXACT allowlist and red-first evidence. Package Map updated: `WP3-owners` 27→30 (T156–T158), `WP4-tests` 37→38 (T159), **total 155→159**; write domains extended for the new files (WP3 gains `templates/instructions-template.md`, `skills/internal/implement-feature/SKILL.md`, `skills/external/create-skills/SKILL.md`, `skills/external/merge-skills/references/decommission-and-wiring.md`, `shared/definitions/non-disposable-definitions.md`, `docs/reference/history/00-cross-cutting-lessons.md`, `.specify/instructions.md` (flow-refreshed); WP4 gains `tests/contract/test_test_entry_guard.py`). DoD-1 FR range 35→36; DoD-3 contract-module count 9→10; test-module count claims 10→11; a dated Validator-adjudication bullet records this run. |
| `feature-ref.md` | Delivery map gains the **FR-036** row (declared no-contract-clause exception: enforcement is the guard test); count 35/35 → 36/36; authority line 35 FR → 36 FR and 2 → 3 dated user rulings; overlap-section measured claim "ten test modules" → "eleven test modules". |
| `.specify/memory/register.md` | One grouped row **`FR-036@093`** — pointer shape only: meaning → authority (`requirements.md` § Clarifications + FR-036; plan § Test-entry enforcement; tasks T156–T159) → `open (pending implement)`. |
| `.specify/state/093-concurrency-by-default.md` | `last_verdict` = amendment result; `next_action` = dispatch analyze-lite verification of the amendment, then resume implement waves; new `amendments:` block (directive + routing verdict + landing + allowlist owner + coordination notes); a dated `gates:` line with the readings below. |
| `test-evidence/amend-fr036-*.txt` | The five gate readings of this run (command line, ISO date, complete output, exit code). |

No framework source was edited (`skills/`, `templates/`, `agents/`, `shared/`, `scripts/`, `docs/` untouched);
no push; all writes are inside this worktree.

## 2. Gate readings (all green)

| Gate | Reading | Evidence |
|---|---|---|
| `validate-requirements.py` | status ok — 0 error / 0 warning; 345 lines, **48 definition rows**, 11 shared strings | `test-evidence/amend-fr036-validate-requirements.txt` |
| `validate-tasks.py` | PASS — 0 error / 0 warning over **159 rows** | `test-evidence/amend-fr036-validate-tasks.txt` |
| `pre-analyze-check --stage requirements` | decision=pass — 0 errors / 83 advisories (all creation-target or dated-history paths), fr=36 sc=12 tasks=159 | `test-evidence/amend-fr036-pre-analyze-requirements.txt` |
| `pre-analyze-check --stage plan` | decision=pass — 0 errors / 83 advisories, fr=36 sc=12 tasks=159 | `test-evidence/amend-fr036-pre-analyze-plan.txt` |
| `pre-analyze-check --stage tasks` | decision=pass — 0 errors / 83 advisories, fr=36 sc=12 tasks=159 | `test-evidence/amend-fr036-pre-analyze-tasks.txt` |
| `validate-decision-tensions.py` | status ok — 0 error / 0 warning, 5 records (T-001…T-005); no tension added | `test-evidence/amend-fr036-decision-tensions.txt` |
| `decomposition-check --mode tasks` | proceed — 36 FR / **159 tasks**, ceilings 120 / 160 | `test-evidence/amend-fr036-decomposition-tasks.txt` |

## 3. In-passing corrections (directive vs measurement)

1. **Row total**: the directive states `total 158`; the directive's own per-package deltas are +3 (`WP3-owners`
   27→30) and +1 (`WP4-tests` 37→38) against a measured 155-row base, so the consistent total is **159**
   (partition 16+26+30+38+49). 158 is arithmetically unreachable without removing a row. Corrected to the
   measured value; the ceiling check still passes (159 ≤ 160, one slot of headroom).
2. **Story labels**: the directive asks for "story labels" on T156–T159, but these rows land in **Phase 8
   (Polish)**, a non-story phase; `validate-tasks.py` rule `story-labels` requires non-story phases to carry no
   `[USn]` marker (every existing Phase-8 row, including T139–T155, is unlabeled). The rows follow the
   established shape; story assignment stays visible in the Package Map (`WP3-owners` / `WP4-tests`). Adding
   labels would have turned the mandated 0/0 gate red.

## 4. Residuals and obligations carried forward

- **No contract clause for FR-036**: the user ruling names the guard test as the enforcement. `feature-ref.md`
  records this as a declared exception; `account-clause-coverage.py`'s FR lane (citation groups) will report
  FR-036 uncovered by design until an owner revises that ruling. The guard test (T159) is its contract-level
  evidence per FR-030.
- **Guard allowlist is exactly four entries** (runner itself, `tests/fixtures/**`, dated records, feature spec
  trees). Raw-pytest mentions measured 2026-11-09 outside the allowlist and inside the scan set — the T158 sweep:
  `skills/internal/implement-feature/SKILL.md` (~L178–L180, ~L193), `skills/external/create-skills/SKILL.md`
  (~L167–L168), `skills/external/merge-skills/references/decommission-and-wiring.md` (~L73),
  `shared/definitions/non-disposable-definitions.md` (~L704), `docs/reference/history/00-cross-cutting-lessons.md`
  (~L57, ~L95). The guard cannot be green until these are reworded; they are inside T158's scope.
- **Live instructions refresh**: `templates/instructions-template.md` is the framework source (mirror
  `.specify/templates/instructions-template.md` regenerated by `sync-mirrors.py`, release row T130). The live
  `.specify/instructions.md` is refreshed by the instructions flow (`/speckit.instructions` →
  `skills/internal/manage-instructions/SKILL.md`) — never hand-edited; T156 carries that evidence. No separate
  WP5 row was added: the instruction refresh is T156's completion evidence and the mirror parity is T130's.
- **094 concurrency**: T157 adds only the test-entry sentences to `skills/external/sdd-loop-driver/references/
  dispatch-recipes.md`; 094's wp05 also edits that file, so the driver serializes the two write lines (recorded
  in the Package Map dependency note and the spine `amendments:` block).
- **Analyze-lite is next**: this amendment was self-verified (U4) by its writer; the state spine routes the next
  turn to an independent analyze-lite verification before implement waves resume.
