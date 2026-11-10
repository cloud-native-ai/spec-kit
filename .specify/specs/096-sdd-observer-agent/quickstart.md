# Quickstart — 096-sdd-observer-agent

Seven walk-through scenarios. Every command is shown with its **premises**; a command whose subject does not exist yet is marked per example and pinned to the contract clause + test module that will assert it, per the Post-Generation Quality Gate's per-example rule. Commands that exist today were executed in this plan run and their readings are in `test-evidence/`.

## S-0 — Inspect the shipped surfaces (runs today)

```bash
ls agents/sdd-observer.agent.md .specify/agents/templates/sdd-observer.agent.md
ls skills/external/sdd-loop-driver/references/observer-lifecycle.md
ls shared/declarations/facts/journal-format.yaml scripts/python/journal-utils.py
```

Premises: these paths are **created by implementation** (see `feature-ref.md`). Until then each `ls` fails — that is the expected reading before the feature lands. Pinned by `tests/contract/test_sdd_observer_agent.py` (role surface) and `tests/contract/test_journal_engine.py` (engine surface).

## S-1 — Enable the observer on a line (driver behavior, template-pinned)

Entry declaration for a driver run:

```text
observer: on          # default; off records state: disabled and must be disclosed
```

Premises: the driver skill text carries the switch and the startup step (`contracts/observer-lifecycle.contract.md` C-01/C-02); the driver is an LLM procedure, so the assertion surface is the SKILL.md text plus the spine fixture — not an executable driver. Pinned by `tests/contract/test_sdd_observer_lifecycle.py`.

Expected reading after implementation: the state spine gains one section

```text
## Observer Record — 2026-11-10T09:00:00Z
- state: started
- line_id: L1
- run_id: R1
- spec: 096-sdd-observer-agent
- instance: sdd-observer-L1
- execution_label: L1--R1--observer
- started_at: 2026-11-10T09:00:00Z
- reason: -
```

## S-2 — Project carrier facts into the journal (engine, fixture-backed)

```bash
python3 scripts/python/journal-utils.py --action append \
  --spec-dir .specify/specs/096-sdd-observer-agent \
  --spine .specify/state/096-sdd-observer-agent.md \
  --state-dir .specify/state \
  --repo . --line-id L1 --run-id R1 \
  --execution-label L1--R1--observer
```

Premises: engine actions and flags as specified in `contracts/journal-engine.contract.md` C-01/C-03; the spine fixture carries the shapes § Execution Premises EP-006 records. Not executable before implementation; pinned by `tests/contract/test_journal_engine.py` (append + idempotency + gap). Expected reading: exit `0`, header written once, one row per newly derivable event, `seq` continuing.

## S-3 — Validate the journal (engine, fixture-backed)

```bash
python3 scripts/python/journal-utils.py --action check \
  --spec-dir .specify/specs/096-sdd-observer-agent --repo .
```

Premises: same as S-2 plus the template's installed journal. Expected reading: exit `0` and a finding-free summary; exit `1` names `file:line` for each rule in `data-model.md` V-1…V-13.

## S-4 — Tamper drills (must turn red)

```bash
# (a) add a tenth column named recommendation to any row  -> exit 1
# (b) replace an event literal with should-improve        -> exit 1
# (c) append a free narrative paragraph to the body       -> exit 1
# (d) point a persistent pointer at a missing path        -> exit 1
# (e) renumber seq 1,2,4                                  -> exit 1
```

Premises: the checker owns these findings (`contracts/journal-format.contract.md` C-06/C-07/C-12; `contracts/journal-engine.contract.md` C-09). Pinned by the five tamper tests in `test_journal_engine.py` (SC-002/SC-004).

## S-5 — Kill the observer mid-line (non-blocking fixture)

Fixture action (pseudo, executed by the test fixture builder):

```text
start observer execution A -> let it append -> kill it (status record: failed)
advance the fixture line through its remaining stub stages
restart observer execution B at the next stage boundary -> append
```

Premises: the fixture builder writes the runner-quartet shapes of R-02; a real kill is replaced by an unsettled/failed status envelope in the fixture. Pinned by `tests/contract/test_sdd_observer_lifecycle.py` (SC-003). Expected reading: the line reaches its terminal stage; the spine carries `state: failed` + reason; the journal carries one `observer-gap` for the uncovered window.

## S-6 — Two parallel lines (isolation fixture)

```text
build two temp project roots, each with its own spec dir + spine + state dir
run append for L1 and L2
```

Premises: fixture builder under `tests/fixtures/sdd-observer/`. Pinned by `test_journal_engine.py` (dual-line isolation). Expected reading: two journals, two instance identities, zero shared paths; a second simultaneous append on one journal exits `3`.

## S-7 — Confirm the boundaries (commands that run today)

```bash
python3 scripts/python/validate-requirements.py .specify/specs/096-sdd-observer-agent/requirements.md
python3 .specify/skills/sdd-loop-driver/scripts/overlap-check.py --spec-dir .specify/specs/096-sdd-observer-agent --repo .
bash scripts/bash/run-tests.sh tests/contract/test_sdd_observer_agent.py tests/contract/test_sdd_observer_lifecycle.py tests/contract/test_journal_engine.py -q
```

Premises: the first two were run in this plan (readings in `test-evidence/plan-gates-baseline.txt`); the third is the post-implementation suite — before implementation it fails on missing modules, which is the expected red-first reading. The digest boundary check is `test_sdd_observer_lifecycle.py` (SC-006 baseline comparison under `test-evidence/`).
