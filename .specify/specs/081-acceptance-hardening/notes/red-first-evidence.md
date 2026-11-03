# Red-First Evidence — Feature 081, slice 081a (implement stage)

**Opened**: 2026-11-03 at implement part 1 (T001), HEAD `f9f6d4f3`, branch `081-acceptance-hardening`.
**Owner of the obligation**: `tasks.md` § Definition of Done **DoD-2** and `## Format` § Tests Mode note —
each of the four 081a contract modules is authored *before* the row implementing its subject closes, and its
failing run is recorded here with **command line, real output, exit code and failing count**.

**Status of this file**: the four sections in § 1 are *scaffolding opened by T001 and filled by their own rows* —
T007, T008, T009, T010 write the red run; T011–T016 write the red→green transition. § 2 is filled once, at slice
close, by T022. **No section may be read as covered while it still reads `pending`**: nothing here is a claim
until it carries a real command, a real exit code and a real failing count.

## 1. The four 081a contract modules

| # | Test module | Contract clauses it pins | Red run written by | Subject that must be able to break |
|---|---|---|---|---|
| 1 | `tests/contract/test_closure_acceptance_check.py` | `contracts/closure-acceptance-check.contract.md` C-01…C-09, C-13…C-16 | T007 | `scripts/python/closure-acceptance-check.py` — verdict, closed reason set, exit-code tri-state, `final_path` counts, the seven fixtures |
| 2 | `tests/contract/test_requirements_checker.py` (extension) | `contracts/artifact-schemas.contract.md` AS-01…AS-04 | T008 | the sixth `path-marker` check label in `scripts/python/validate-requirements.py` |
| 3 | `tests/contract/test_acceptance_state_machine.py` | `contracts/state-vocabulary.contract.md` SV-03…SV-11 | T009 | `templates/feature-details-template.md` § Canonical Status State Machine and `templates/verification-log-template.md` |
| 4 | `tests/contract/test_gate_wiring_081.py` | `contracts/gate-wiring.contract.md` GW-01, GW-04 | T010 | the implement call site in `skills/internal/implement-feature/SKILL.md` Step 9 and `shared/workflow/feature-integration.md` § Pre-Status-Flip Gate |

### 1.1 `tests/contract/test_closure_acceptance_check.py` — **pending (written by T007)**

- Command line: `bash scripts/bash/run-tests.sh tests/contract/test_closure_acceptance_check.py -q`
- Real output: pending
- Exit status / failing count: pending

### 1.2 `tests/contract/test_requirements_checker.py` — `path-marker` cases — **pending (written by T008)**

- Command line: `bash scripts/bash/run-tests.sh tests/contract/test_requirements_checker.py -q`
- Real output: pending
- Exit status / failing count: pending

### 1.3 `tests/contract/test_acceptance_state_machine.py` — **pending (written by T009)**

- Command line: `bash scripts/bash/run-tests.sh tests/contract/test_acceptance_state_machine.py -q`
- Real output: pending
- Exit status / failing count: pending

### 1.4 `tests/contract/test_gate_wiring_081.py` — **pending (written by T010)**

- Command line: `bash scripts/bash/run-tests.sh tests/contract/test_gate_wiring_081.py -q`
- Real output: pending
- Exit status / failing count: pending

### 1.5 Absence check recorded at T001 (the state a red run requires)

```text
$ for f in tests/contract/test_closure_acceptance_check.py \
           tests/contract/test_requirements_checker.py \
           tests/contract/test_acceptance_state_machine.py \
           tests/contract/test_gate_wiring_081.py \
           tests/integration/test_acceptance_smoke.py; do
    if [ -f "$f" ]; then echo "PRESENT $f"; else echo "ABSENT  $f"; fi
  done
ABSENT  tests/contract/test_closure_acceptance_check.py
PRESENT tests/contract/test_requirements_checker.py
ABSENT  tests/contract/test_acceptance_state_machine.py
ABSENT  tests/contract/test_gate_wiring_081.py
ABSENT  tests/integration/test_acceptance_smoke.py
```

`test_requirements_checker.py` is the one **extension** module (five labels exist today, the sixth `path-marker`
label does not), so its red run is a new failing case inside an existing file rather than an absent file.

## 2. Slice-close set-level comparison (GATE-7 / DoD-6) — **pending (written by T022)**

Not re-derived here: the baseline side is the plan-stage capture, recorded by pointer in
`notes/pre-change-measurements.md`. T022 re-reads the two runner pins, runs the full suite once with
`--names-out`, and lands both set differences plus the two pin readings in this section:

- `head 失败集 − 基线失败集`: pending
- `基线失败集 − head 失败集`: pending
- pin re-read (`pytest --version` / `git --version`) vs `test-evidence/plan-runner-pins.txt`: pending
- exit status of the full-suite run: pending
