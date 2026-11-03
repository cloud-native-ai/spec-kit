# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `081-acceptance-hardening` |
| **基准** | `f29b6178789539622fd9b7ee9af811b956cfa909` (`f29b6178`) |
| **目标** | `a8dbb599e0ce2adc98766c517f0a19ac14a7afc0` (`a8dbb599`) |
| **基准来源** | `explicit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming, Liu` |
| **日期** | `2026-11-03T11:06:30Z` |

## 变更概览

```
 .specify/memory/features.md                        |   2 +-
 .specify/memory/features/081.md                    |   2 +-
 .../test-evidence/gate-newline-baseline.txt        |  16 +++
 .../081-acceptance-hardening/head-failed-2.txt     |  39 ++++++
 .specify/specs/081-acceptance-hardening/tasks.md   |  26 ++--
 .../test-evidence/081d-call-sites.txt              | 110 +++++++++++++++++
 .../test-evidence/081d-final-baseline-2.txt        | 131 +++++++++++++++++++++
 .../test-evidence/081d-final-baseline.txt          | 129 ++++++++++++++++++++
 .../test-evidence/081d-gates.txt                   |  79 +++++++++++++
 .../test-evidence/081d-head-failed.txt             |  58 +++++++++
 .../test-evidence/closure-verdict-081d.json        |  38 ++++++
 .../specs/081-acceptance-hardening/verification.md | 105 ++++++-----------
 CHANGELOG.md                                       |  23 ++++
 tests/contract/test_coaching_run_contract.py       |  18 ++-
 tests/contract/test_coaching_wiring_contract.py    |   8 +-
 tests/contract/test_decision_tension_contract.py   |  46 +++++++-
 tests/contract/test_docs_gate_driver.py            |  13 +-
 tests/contract/test_expression_compatibility.py    |  14 +++
 tests/contract/test_expression_gate_wiring.py      |   5 +-
 tests/contract/test_flow_class_ledger.py           |  40 +++++--
 tests/contract/test_humanize_command_surface.py    |  46 +++++++-
 tests/contract/test_ledger_reconciliation.py       |  14 ++-
 tests/contract/test_probe_nonentity_catalog.py     |   4 +-
 tests/contract/test_run_skills_wiring.py           |  12 +-
 tests/contract/test_stage_class_wiring.py          |   8 +-
 25 files changed, 865 insertions(+), 121 deletions(-)
```

---

## Review 意见


### 🟢 [SUGGESTION] tests/contract/test_humanize_command_surface.py (Line 1851)

> Frozen-surface pins re-pointed to fixed historical ranges (WC-14 here; same shape WC-17 line 1905, WC-19 line 1925, and C-13 test_coaching_run_contract.py line 499) stop observing future cross-feature edits to the same shared surfaces; the union of watched windows shrinks with every legitimate re-pointing and no compensating control (a living line-head registry) exists. Disclosed in dated comments and legitimized by this file own WC-18 precedent and the C-8 BASE-is-re-recordable owner rule - recorded as a drift-risk suggestion, not a defect.

<sub>19:06:36</sub>


### ⚪ [NITPICK] skills/external/sdd-loop-driver/scripts/integrate-lines.py (Line 170)

> spec_dir = candidate.parent when the Spec Path cell names a non-directory: a one-component cell naming a nonexistent file directly under the worktree (e.g. requirements.md with no such file) resolves spec_dir to the worktree root itself instead of raising the GateInputError this resolver exists for; a multi-component miss still errors correctly. Same parent-fallback shape in closure-acceptance-check.py _audit_spec_dir.

<sub>19:06:36</sub>


### ❓ [QUESTION] skills/external/sdd-loop-driver/scripts/integrate-lines.py (Line 159)

> The registry the gate reads is the line worktree own copy (worktree / .specify/memory/features.md), not the driver repository registry; at line closure the worktree copy is the natural source, but GW-03 says only "the registry row" without locating the file, so the contract and the code can drift apart on which tree is read.

<sub>19:06:41</sub>


### 👍 [PRAISE] tests/contract/test_decision_tension_contract.py (Line 1061)

> The C-5 containment was tightened, not loosened: the allowed delta is now an exact Counter multiset of paragraph-delta plus the Rounds section, so any third added line still fails; the helper asserts the section exists instead of passing vacuously.

<sub>19:06:42</sub>


<!-- coverage-receipt:begin -->
receipt_version=1
base=f29b6178789539622fd9b7ee9af811b956cfa909
head=a8dbb599e0ce2adc98766c517f0a19ac14a7afc0
base_source=explicit
renderer=text
changed_files=25
judged_files=25
skipped_files=0
gap_files=0
lines_added=865
lines_deleted=121
file.01.path=.specify/memory/features.md
file.01.verdict=reviewed
file.02.path=.specify/memory/features/081.md
file.02.verdict=reviewed
file.03.path=.specify/specs/080-humanize-run-output/test-evidence/gate-newline-baseline.txt
file.03.verdict=reviewed
file.04.path=.specify/specs/081-acceptance-hardening/head-failed-2.txt
file.04.verdict=reviewed
file.05.path=.specify/specs/081-acceptance-hardening/tasks.md
file.05.verdict=reviewed
file.06.path=.specify/specs/081-acceptance-hardening/test-evidence/081d-call-sites.txt
file.06.verdict=reviewed
file.07.path=.specify/specs/081-acceptance-hardening/test-evidence/081d-final-baseline-2.txt
file.07.verdict=reviewed
file.08.path=.specify/specs/081-acceptance-hardening/test-evidence/081d-final-baseline.txt
file.08.verdict=reviewed
file.09.path=.specify/specs/081-acceptance-hardening/test-evidence/081d-gates.txt
file.09.verdict=reviewed
file.10.path=.specify/specs/081-acceptance-hardening/test-evidence/081d-head-failed.txt
file.10.verdict=reviewed
file.11.path=.specify/specs/081-acceptance-hardening/test-evidence/closure-verdict-081d.json
file.11.verdict=reviewed
file.12.path=.specify/specs/081-acceptance-hardening/verification.md
file.12.verdict=reviewed
file.13.path=CHANGELOG.md
file.13.verdict=reviewed
file.14.path=tests/contract/test_coaching_run_contract.py
file.14.verdict=reviewed
file.15.path=tests/contract/test_coaching_wiring_contract.py
file.15.verdict=reviewed
file.16.path=tests/contract/test_decision_tension_contract.py
file.16.verdict=reviewed
file.17.path=tests/contract/test_docs_gate_driver.py
file.17.verdict=reviewed
file.18.path=tests/contract/test_expression_compatibility.py
file.18.verdict=reviewed
file.19.path=tests/contract/test_expression_gate_wiring.py
file.19.verdict=reviewed
file.20.path=tests/contract/test_flow_class_ledger.py
file.20.verdict=reviewed
file.21.path=tests/contract/test_humanize_command_surface.py
file.21.verdict=reviewed
file.22.path=tests/contract/test_ledger_reconciliation.py
file.22.verdict=reviewed
file.23.path=tests/contract/test_probe_nonentity_catalog.py
file.23.verdict=reviewed
file.24.path=tests/contract/test_run_skills_wiring.py
file.24.verdict=reviewed
file.25.path=tests/contract/test_stage_class_wiring.py
file.25.verdict=reviewed
<!-- coverage-receipt:end -->

## Scope notes (this run)

- **Range reading, disclosed**: the dispatch names the range `54ad418d..a8dbb599` ("the reconciliation
  to the feature close"). Read strictly (`--since 54ad418d`) the delta is 10 files — feature registry,
  feature detail, `tasks.md` ticks, evidence files, `verification.md`, `CHANGELOG.md` — and the
  deterministic triage answers `not-applicable` (`no code deliverable: the committed delta contains no
  code path`). The dispatch's parenthetical makes the reconciliation itself judged material, so this
  record reviews the inclusive span `f29b6178..a8dbb599` (commits `54ad418d` + `a8dbb599`, 25 files,
  12 code paths): `triage --since f29b6178 --head a8dbb599` → `triage=run`. Both commands are
  reproducible verbatim. The three earlier 081d implementation commits (`8ceaeb7a`, `fc6811c6`,
  `f29b6178`) were read as context per the dispatch and are judged in the implementation segment
  against requirements/tasks; the two context-commit surfaces this record's findings touch
  (`integrate-lines.py`) are located in `fc6811c6`'s files as they read at `a8dbb599`.
- **Uncommitted scope**: `git status --porcelain` was 0 lines at run start. This run's own writes are
  this record and `review.md`. The smoke re-run (`bash scripts/bash/run-tests.sh
  tests/integration/test_acceptance_smoke.py -q`, exit 0) refreshed
  `.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt` byte-identically — porcelain
  stayed 0 after it. No unreviewed working-tree scope exists; no pass conclusion is issued over
  anything but the range above.
- **Client capture**: not run — this repository is the framework source itself (framework hat), so the
  capture step's first trigger condition fails by the hat verdict, not by one of the five tokens.
- **Gate**: `report --summary --file <this record>` → `gate=allow`, exit 0 (0 `blocking`, 0
  `important`).
