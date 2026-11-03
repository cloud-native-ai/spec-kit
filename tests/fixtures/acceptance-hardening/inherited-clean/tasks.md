<!-- Fixture case: acceptance-hardening/inherited-clean — see requirements.md for the fixture notice.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     T004 is the task that carries the inherited measurement, and the test path in its description is what makes
     the `task:<T-ID>+test:<path>` carrier resolvable. GATE-1 is the `gate:<GATE-ID>` carrier's target. -->

# Tasks: Acceptance Fixture — inherited-clean

**Requirement Branch**: `900-acceptance-fixture-inherited-clean`

## Phase 1: Setup

- [X] T001 Delivers FR-001: the fixture's runtime capability is in place.
- [X] T002 Records the single smoke command required by FR-002.
- [X] T003 Drives the fixture's main flow once, end to end.

## Phase 2: Inherited Measurement

- [X] T004 Carries the inherited dependency measurement, asserted by tests/contract/test_acceptance_premises.py.

## Completion Gate

- GATE-1: The fixture's single test carrier is green — check: `bash scripts/bash/run-tests.sh tests/contract/test_acceptance_premises.py -q`
