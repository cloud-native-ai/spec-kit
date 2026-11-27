# Quickstart — Prompt Adherence Evaluation（提示遵从度评价）

The mechanism's documented single invocation is one read-only script:
`python3 .specify/scripts/python/prompt-adherence.py` (framework source
`scripts/python/prompt-adherence.py`). The engine is an implementation output of this feature, so every
example that invokes it is **pinned by a contract test** and lists its premises; examples over the
existing sensors were executed at plan time (2026-11-27) and their measured output is quoted below.
Full captures live at `test-evidence/plan-stage-2026-11-27.md`.

## Sensor read surfaces (executed at plan time)

The reading consumes only these existing stores. Each command below was executed on this tree; the
excerpts are measured output.

```bash
python3 .specify/scripts/python/run-determination.py --action history --target /speckit.clarify --limit 2 --json
```

Measured: exit 0; `"counts": {"total": 43, ...}`; per-record `run_id`
(`r20261126T071500Z-108a`) and `determined_at`.

```bash
python3 .specify/scripts/python/exec-quant.py --action list-records --format json --since 2026-11-27
```

Measured: exit 0; a JSON array of records carrying `kind: speckit.exec-quant`, `schema_version: 2`,
`run_id`, `collected_at`.

```bash
python3 .specify/scripts/python/feedback-utils.py --action list --limit 2 --format json
```

Measured: exit 0; `{"count": 2, "matches": [...]}` with frontmatter metadata only (`id`, `run_id`,
`created`, `feature`, `feature_id`, `path`).

```bash
python3 .specify/scripts/python/probe-utils.py --action probes --format json
```

Measured: `available: true`, 11 classes, 130 objects, 0 errors — exit 0.

```bash
python3 .specify/scripts/python/evidence-utils.py --action list --limit 5
```

Measured: exit 0; one entry (`runId` `ev-20261113-161502-improve-skills`, manifest `created`,
`lanesSummary`).

```bash
python3 .specify/scripts/python/measure.py --action summary --workspace .
```

Measured: per-unit lines over the exec-quant store (`read=545`, `27 figures measurable`) — exit 0. This
is a read-only projection over the same store; the adherence engine does not call it and the catalog
gives it no separate row.

```bash
python3 .specify/scripts/python/declaration_reader.py --action get --fact evidence-seven-states
```

Measured: the seven-state statement exactly as `shared/declarations/facts/evidence-seven-states.yaml`
declares it — exit 0.

## Scenario 1 — One honest per-run reading, maintainer (default scope, text)

```bash
python3 .specify/scripts/python/prompt-adherence.py
```

Expected: the human-readable per-run reading for the most recent run identity observed across the
catalog, with the resolved identity and its basis printed in the scope line, one line per catalog row
(layer, strength, state, classes, reason, sources), the coverage section with all six blind-spot
classes, and exit 0.

> *Not executed at plan time — the engine is an implementation output of this feature. Pinned by
> `tests/contract/test_prompt_adherence_engine.py` (default-scope and fixture-reading legs). Premises:
> engine path `scripts/python/prompt-adherence.py` mirrored to `.specify/scripts/python/prompt-adherence.py`;
> default workspace resolved from the current directory upward to the nearest ancestor holding
> `.specify/`; six catalog rows and their order as the owner document declares; exit 0 whenever a
> reading is emitted.*

## Scenario 2 — Pin a run identity, machine-readable form (maintainer)

```bash
python3 .specify/scripts/python/prompt-adherence.py --run r20261126T071500Z-108a --json
```

Expected: a JSON reading whose `scope.kind` is `run`, `scope.run` is the pinned identity, `status` is
`complete` or `partial` (never `not-found` when records match), and whose `observations` array carries
exactly one entry per catalog row. A non-matching identity yields `status: not-found` and still exits 0.

> *Not executed at plan time. Pinned by `tests/contract/test_prompt_adherence_engine.py` (`--run` pin,
> `not-found`, and JSON-shape legs). Premises: `--run` flag; `--json` flag; the six-row observation
> array; `status` closed set `complete` / `partial` / `no-data` / `not-found`; exit 0 for emitted
> readings including `not-found`.*

## Scenario 3 — Longitudinal window (maintainer)

```bash
python3 .specify/scripts/python/prompt-adherence.py --since 2026-11-01 --until 2026-12-01
python3 .specify/scripts/python/prompt-adherence.py --since 2026-11-01 --json
```

Expected: the window `[2026-11-01, 2026-12-01)` (the second call prints the omitted bound as the literal
`open`), per-row counts by evidence state plus the coverage line, and no per-project, per-agent or
per-user ranking.

> *Not executed at plan time. Pinned by `tests/contract/test_prompt_adherence_engine.py`
> (half-open boundary fixture on an exact record timestamp; `open` literal; counts-only legs).
> Premises: `--since` / `--until` accept `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SSZ` (UTC); the window
> compares against each record's own declared timestamp field; a probe-registry row evaluates once
> against current state and is marked window-exempt.*

## Scenario 4 — A fresh client project reads honestly, offline (client project)

```bash
# inside a project initialized by `specify init` (no runtime records yet)
python3 .specify/scripts/python/prompt-adherence.py
python3 .specify/scripts/python/prompt-adherence.py --json
```

Expected text: the reading completes with explicit `not_evaluated` and `Unobserved` lines with
per-store reasons, every catalog row present, the six blind-spot classes listed, and exit 0. Expected
JSON: `status` is `no-data` (no scope record exists) or `partial` when a default scope resolves but rows
stay unobserved; `observations` carries six entries; `coverage.blind_spots` lists six classes. No
network access occurs and nothing is written under any managed store root.

> *Not executed at plan time. Pinned by `tests/integration/test_prompt_adherence_init.py` (fresh init
> fixture, socket-blocked interpreter, zero-write check) and
> `tests/contract/test_prompt_adherence_readonly.py`. Premises: `specify init` copies the `shared/` and
> `scripts/` trees (`src/specify_cli/__init__.py`); the fresh project's `probe-definitions.md` ships
> with init and is non-empty, so the probe row reads `Wired` or `Unobserved` rather than
> `not_evaluated`; the engine works with absent stores; exit 0 distinguishes "ran with no data" from an
> error (exit 2). The `specify init` step itself is exercised by that integration fixture, not by this
> document.*

## Scenario 5 — The premise review is machine-checked (maintainer)

```bash
python3 .specify/scripts/python/prompt-adherence.py --check-coverage
python3 .specify/scripts/python/prompt-adherence.py --check-coverage --json
```

Expected: exit 0 with zero findings — every assumed behavior maps to exactly one sensor-or-blind-spot
entry, every sensor entry resolves to a catalog row id, every catalog row is cited by at least one
assumed behavior. A doctored owner-document copy exits 1 with the sorted finding list; an unreadable
owner document exits 2.

> *Not executed at plan time. Pinned by `tests/contract/test_prompt_adherence_engine.py`
> (`--check-coverage` clean and doctored-map legs) and `tests/contract/test_prompt_adherence_owner.py`.
> Premises: the owner document's coverage-map table shape (assumed behavior, statement, target kind,
> target); exit 1 on findings and exit 2 on an unreadable owner document.*

## Scenario 6 — Keep a baseline reading through the existing channel (maintainer)

```bash
python3 .specify/scripts/python/feedback-utils.py --action record \
  --unit-id "/speckit.implement" --unit-type command \
  --run-id "<implement-run-id>" --feature "109-prompt-adherence" --feature-id "109" \
  --review "<reading status, per-row states, declaration-set digest, source references>" \
  --points-file "<points file>"
```

Expected: one ordinary feedback entry under `.specify/feedback/`; no new store root, no aggregate, no
query surface; replayable by one engine run against its cited references.

> *The call shape was measured at plan time by this stage's own wrap-up records (a feedback entry
> carrying `feature` and `feature_id`, one run-determination record, one exec-quant record); the
> baseline entry itself is an implementation output. Pinned by the audit-replay leg of
> `tests/contract/test_prompt_adherence_engine.py`. Premises: `--action record` requires a framework
> unit id (`/speckit.*` or `skill:*`); the entry is one Markdown file with frontmatter; the reading's
> source references are repo-relative paths.*

## Check block — distribution and the full suite

```bash
python3 scripts/python/sync-mirrors.py --check
```

Measured 2026-11-27 (plan stage): exit 0 — all six pairs byte-identical, six projections `ok`. The
implementation-time criterion is no NEW drift on the pairs this spec touches.

```bash
python3 scripts/python/regen-command-copies.py --check
```

Measured 2026-11-27: exit 0 (`OK: all per-tool command copies match the source templates`). This spec
changes no `templates/commands/` file.

```bash
bash scripts/bash/run-tests.sh -q
```

Expected at implementation time: no new failures against the implement-stage baseline; the five new
guards green through the project runner.

> *Not executed at plan time (the guards do not exist yet). Pinned by the implement stage's baseline
> capture and the guard roster (contract C-040). Premises: the project test entry is
> `scripts/bash/run-tests.sh`; the five guard files are named in contract C-040; the `contract` and
> `integration` markers are declared in `pyproject.toml`.*