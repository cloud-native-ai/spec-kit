# Quickstart Run Record — 109-prompt-adherence

Purpose: record each quickstart scenario's real command output and teardown steps as executed, exactly as written in `quickstart.md`.

Executed 2026-11-27 in the line worktree on branch `109-prompt-adherence`, after the single
mirror projection (T033): engine version `0.0.22` on both copies, declaration-set digest
`093e71f226cc7a14f8c5fe83400943305f0e9654a5915a1edd618f7a2d4c5018`. Every command below was
run from the repository root; no premise in `quickstart.md` was found false (nothing to report to
the plan owner), and the plan-owned quickstart was not rewritten.

## Sensor-read block (re-executed at implementation time)

```bash
python3 .specify/scripts/python/run-determination.py --action history --target /speckit.clarify --limit 2 --json
```

Exit 0; `"counts": {"total": 43, "settled": 11, "unsettled": 32, ...}`; the first record carries
`unit_id: "/speckit.clarify"`, `run_id: "r20261126T071500Z-108a"`, `determined_at:
"2026-11-26T08:19:31Z"` — the plan-time measurement reproduces.

```bash
python3 .specify/scripts/python/exec-quant.py --action list-records --format json --since 2026-11-27
```

Exit 0; a JSON array of records carrying `kind: speckit.exec-quant`, `schema_version: 2`,
`run_id`, `collected_at`.

```bash
python3 .specify/scripts/python/feedback-utils.py --action list --limit 2 --format json
```

Exit 0; `{"count": 2, "matches": [...]}` with frontmatter metadata only (`id`, `run_id`,
`created`, `feature`, `feature_id`, `path`).

```bash
python3 .specify/scripts/python/probe-utils.py --action probes --format json
```

Exit 0; `available: true`, 11 classes, 130 objects, 0 errors (read from the JSON fields).

```bash
python3 .specify/scripts/python/evidence-utils.py --action list --limit 5
```

Exit 0; the existing evidence runs are listed (`runId` `ev-…`, manifest `created`).

```bash
python3 .specify/scripts/python/measure.py --action summary --workspace .
```

Exit 0; per-unit lines over the exec-quant store (the reading engine does not call it and the
catalog gives it no separate row).

```bash
python3 .specify/scripts/python/declaration_reader.py --action get --fact evidence-seven-states
```

Exit 0; the seven-state statement exactly as `shared/declarations/facts/evidence-seven-states.yaml`
declares it (`path: shared/declarations/facts/evidence-seven-states.yaml`).

## Scenario 1 — One honest per-run reading, maintainer (default scope, text)

```bash
python3 .specify/scripts/python/prompt-adherence.py
```

Real output (exit 0):

```text
prompt-adherence reading
reading-format: 1
engine: scripts/python/prompt-adherence.py 0.0.22
declaration-set: 093e71f226cc7a14f8c5fe83400943305f0e9654a5915a1edd618f7a2d4c5018
facts: shared/declarations/facts/prompt-adherence-deviation-classes.yaml, shared/declarations/facts/prompt-adherence-layers.yaml, shared/declarations/facts/prompt-adherence-reading-status.yaml, shared/declarations/facts/prompt-adherence-signals.yaml, shared/declarations/facts/prompt-adherence-strengths.yaml
scope: run r20261127T053750Z-109a-p4-baseline
scope-resolution: most-recent
scope-basis: store=feedback path=.specify/feedback/20261127T074122Z-speckit-implement.md timestamp=2026-11-27T07:41:22Z
status: complete
row run-determination-record layer=host-prompt strength=indirect state=Unobserved reason=no-matching-records source=.specify/session
row exec-quant-record layer=project-rules strength=indirect state=Unobserved reason=no-matching-records source=.specify/exec-quant
row feedback-entry layer=project-rules strength=direct state=Exercised
source feedback-entry store=feedback path=.specify/feedback/20261127T074122Z-speckit-implement.md record=20261127T074122Z-speckit-implement field=run_id
row gate-observation-record layer=project-rules strength=direct state=Unobserved reason=no-matching-records source=.specify/feedback
row evidence-finding layer=project-rules strength=indirect state=Unobserved reason=no-matching-records source=.specify/evidence
row probe-registry-declaration layer=project-rules strength=indirect state=Wired
source probe-registry-declaration store=registry path=.specify/shared/definitions/probe-definitions.md record=registry field=objects
coverage-observable: feedback-entry, probe-registry-declaration
coverage-not-observable: run-determination-record, exec-quant-record, gate-observation-record, evidence-finding
coverage-blind-spots: host-prompt-content, host-rule-surfacing, in-turn-rule-behavior, anomaly-line-persistence, gate-breach-and-silent-skip, instruction-drift-between-reconciles
coverage-records-in-scope: 1
coverage-invalid-records: 19
invalid-source .specify/exec-quant/records.jsonl unknown-schema-version   (19 legacy jsonl records, disclosed not skipped)
```

The default scope resolves the most recent record (the T031 baseline entry) and prints its basis;
each catalog row appears once; the six blind-spot classes are listed; exit 0. The 19
`unknown-schema-version` entries are the repository's legacy `records.jsonl` lines — pre-existing
records laid aside by name, never coerced and never skipped.

## Scenario 2 — Pin a run identity, machine-readable form (maintainer)

```bash
python3 .specify/scripts/python/prompt-adherence.py --run r20261126T071500Z-108a --json
```

Exit 0. Measured reading (the full 13 KB JSON; the structural fields verbatim):

```json
{
  "coverage": {
    "blind_spots": ["host-prompt-content", "host-rule-surfacing", "in-turn-rule-behavior", "anomaly-line-persistence", "gate-breach-and-silent-skip", "instruction-drift-between-reconciles"],
    "invalid_records": 19,
    "not_observable": ["gate-observation-record", "evidence-finding", "probe-registry-declaration"],
    "observable": ["run-determination-record", "exec-quant-record", "feedback-entry"],
    "records_in_scope": 30
  },
  "declaration_set": {"facts": ["shared/declarations/facts/prompt-adherence-deviation-classes.yaml", "shared/declarations/facts/prompt-adherence-layers.yaml", "shared/declarations/facts/prompt-adherence-reading-status.yaml", "shared/declarations/facts/prompt-adherence-signals.yaml", "shared/declarations/facts/prompt-adherence-strengths.yaml"], "version": "093e71f226cc7a14f8c5fe83400943305f0e9654a5915a1edd618f7a2d4c5018"},
  "engine": {"path": "scripts/python/prompt-adherence.py", "version": "0.0.22"},
  "reading_format": 1,
  "scope": {"basis": null, "kind": "run", "resolution": "explicit", "run": "r20261126T071500Z-108a", "window": null},
  "status": "partial"
}
```

Per-row replayed states: `run-determination-record Exercised [axis-regression] (10 sources)`,
`exec-quant-record Exercised (10)`, `feedback-entry Exercised (10)`,
`gate-observation-record not_evaluated / no-matching-records`, `evidence-finding not_evaluated /
no-matching-records`, `probe-registry-declaration not_evaluated / no-matching-records`; duplicates
3. `scope.kind` is `run`, `scope.run` is the pinned identity, status `partial` (records match).
The non-matching identity form:

```bash
python3 .specify/scripts/python/prompt-adherence.py --run r20260101T000000Z-no-such-run --json
```

Exit 0; `status: not-found`.

## Scenario 3 — Longitudinal window (maintainer)

```bash
python3 .specify/scripts/python/prompt-adherence.py --since 2026-11-01 --until 2026-12-01
```

Real output (exit 0):

```text
scope: window [2026-11-01T00:00:00Z, 2026-12-01T00:00:00Z)
scope-resolution: explicit
scope-note: probe-registry-declaration is window-exempt: it evaluates once against current state
status: partial
state-counts run-determination-record Exercised=341
state-counts exec-quant-record Exercised=358
state-counts feedback-entry Exercised=377
state-counts gate-observation-record Exercised=1
state-counts evidence-finding Exercised=2
state-counts probe-registry-declaration none
coverage-records-in-scope: 1079
```

```bash
python3 .specify/scripts/python/prompt-adherence.py --since 2026-11-01 --json
```

Exit 0; `scope.window = {"since": "2026-11-01T00:00:00Z", "until": "open"}` — the omitted bound
prints as the literal `open` and both bounds appear; status `complete`; `records_in_scope` 1079.
No per-project, per-agent or per-user ranking appears.

## Scenario 4 — A fresh client project reads honestly, offline (client project)

A scratch project initialized from this repository's framework sources (the
`copy_local_templates` + `get_resource_path` distribution path, the same one the integration
fixture exercises) under `.specify/.tmp/p4-fresh-project`; both calls ran under a socket-blocked
interpreter.

```bash
# inside the fresh project (no runtime records yet)
python3 .specify/scripts/python/prompt-adherence.py
python3 .specify/scripts/python/prompt-adherence.py --json
```

Blocker probe: `blocked=True network access is blocked in this interpreter`. Real text output
(exit 0):

```text
prompt-adherence reading
reading-format: 1
engine: .specify/scripts/python/prompt-adherence.py 0.0.22
declaration-set: 2beff0475d4a74de9d3d94259628875f0346b15121e18862dd3a441e44a81c45
facts: shared/declarations/facts/prompt-adherence-deviation-classes.yaml, shared/declarations/facts/prompt-adherence-layers.yaml, shared/declarations/facts/prompt-adherence-reading-status.yaml, shared/declarations/facts/prompt-adherence-signals.yaml, shared/declarations/facts/prompt-adherence-strengths.yaml
scope: run none
scope-resolution: none
status: no-data
row run-determination-record layer=host-prompt strength=indirect state=Unobserved reason=no-matching-records source=.specify/session
row exec-quant-record layer=project-rules strength=indirect state=not_evaluated reason=source-unavailable source=.specify/exec-quant
row feedback-entry layer=project-rules strength=direct state=not_evaluated reason=source-unavailable source=.specify/feedback
row gate-observation-record layer=project-rules strength=direct state=not_evaluated reason=source-unavailable source=.specify/feedback
row evidence-finding layer=project-rules strength=indirect state=not_evaluated reason=source-unavailable source=.specify/evidence
row probe-registry-declaration layer=project-rules strength=indirect state=Wired
source probe-registry-declaration store=registry path=.specify/shared/definitions/probe-definitions.md record=registry field=objects
coverage-observable: probe-registry-declaration
coverage-not-observable: run-determination-record, exec-quant-record, feedback-entry, gate-observation-record, evidence-finding
coverage-blind-spots: host-prompt-content, host-rule-surfacing, in-turn-rule-behavior, anomaly-line-persistence, gate-breach-and-silent-skip, instruction-drift-between-reconciles
coverage-records-in-scope: 0
coverage-invalid-records: 0
```

JSON form: exit 0; `status: no-data`, six observations, six blind-spot classes. The fresh
project's declaration digest is `2beff047…a81c45` — the five fact files' bytes, computed at read
time. No network access occurred and nothing was written under any managed store root.
Teardown: the scratch project and the blocker directory were removed after the capture.

## Scenario 5 — The premise review is machine-checked (maintainer)

```bash
python3 .specify/scripts/python/prompt-adherence.py --check-coverage
python3 .specify/scripts/python/prompt-adherence.py --check-coverage --json
```

Real output of both (exit 0 each):

```text
coverage-map: ok (0 findings)
```

(The doctored-copy and unreadable-owner forms of this check are exercised red at T019/T020 and
recorded in `notes/red-first-evidence.md`.)

## Scenario 6 — Keep a baseline reading through the existing channel (maintainer)

Executed once at T031 (one ordinary entry; re-running the same run id would be recorded as a
duplicate, so the command is not repeated here). Real capture:

```bash
python3 scripts/python/feedback-utils.py --action record \
  --unit-id /speckit.implement --unit-type command \
  --run-id r20261127T053750Z-109a-p4-baseline \
  --feature 109-prompt-adherence --feature-id 109 \
  --review-file .specify/.tmp/p4-baseline-review.md \
  --points-file .specify/.tmp/p4-baseline-points.md
```

```text
{
  "id": "20261127T074122Z-speckit-implement",
  "path": ".specify/feedback/20261127T074122Z-speckit-implement.md",
  "duplicate": false,
  "count_since_submission": 612,
  "threshold": 10,
  "should_prompt": true,
  "migrated": false
}
```

Exit 0; one ordinary feedback entry under `.specify/feedback/`; no new store root, no aggregate,
no query surface; replayable by one engine run against its cited references (T032).

## Check block — distribution and the full suite

```bash
python3 scripts/python/sync-mirrors.py --check
```

Exit 0 — every pair byte-identical (`scripts/ == .specify/scripts/` 134 files, `shared/ ==
.specify/shared/` 123 files, plus the other four pairs), six projections `ok`; no NEW drift on
the pairs this spec touches against `notes/pre-change-measurements.md` (the owner document,
`framework-map.md`, the five facts and the engine were ABSENT/DIFF before the projection and are
byte-identical now).

```bash
python3 scripts/python/regen-command-copies.py --check
```

Exit 0 — `OK: all per-tool command copies match the source templates.` (this spec changes no
`templates/commands/` file).

```bash
bash scripts/bash/run-tests.sh -q
```

Executed once at T038 (slot F-1) — recorded in
`test-evidence/implementation-gates.txt`; not re-run here.