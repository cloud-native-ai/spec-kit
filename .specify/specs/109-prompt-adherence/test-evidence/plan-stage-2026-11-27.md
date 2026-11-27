# Plan Stage Evidence — 109-prompt-adherence

**Run**: `r20261127T053750Z-109a` · **Stage**: `plan` · **Date**: 2026-11-27
**Worktree**: `.specify/.tmp/sdd-loop/worktrees/prompt-adherence` · **Branch**: `109-prompt-adherence` · **Baseline**: `534688278`

Every section below is a captured reading from this run; nothing is hand-scored. Test execution for this
stage is `not-run-docs-only` (the stage produces documentation artifacts only; the guards it names are
implementation outputs).

## A-1 — Artifacts produced (paths, counts measured after writing)

| Artifact | Path | Count / scope |
|----------|------|---------------|
| Plan | `.specify/specs/109-prompt-adherence/plan.md` | 23-row dynamic Constitution Check; 16 plan assumptions; 8 execution premises; 1 inherited-blockers row; N/A decision-tension form |
| Research | `.specify/specs/109-prompt-adherence/research.md` | 11 findings (R-1…R-11) + 3 residual unknowns (RU-1…RU-3) |
| Data model | `.specify/specs/109-prompt-adherence/data-model.md` | 11 entities (E-1…E-11) + 14 invariants (I-1…I-14) |
| Contracts | `.specify/specs/109-prompt-adherence/contracts/` | 6 files / 39 clauses: owner-and-catalog 7, declarations-and-vocabularies 7, reading-semantics 10, engine-and-read 5, distribution 3, guards-and-boundaries 7 |
| Quickstart | `.specify/specs/109-prompt-adherence/quickstart.md` | 6 scenarios + measured sensor-read block + distribution/suite check block |
| Feature reference | `.specify/specs/109-prompt-adherence/feature-ref.md` | Binding, delivery surface, 30 FR deliveries, 9 SC evidence rows |
| Feature registry | `.specify/features.md`, `.specify/features/109-prompt-adherence.md` | Feature 109 `Draft → Planned` + plan note |

## A-2 — Plan integrity checks (verbatim, `test-evidence/plan-integrity.txt`)

```
== residual UPPER_SNAKE placeholders ==
none
== H1 headings ==
1
== Requirement→Feature stamp ==
1
== template note removed (expect 0) ==
0
== decision-tension records (expect N/A form) ==
0
```

## A-3 — pre-analyze-check.py --stage plan (final run, summary)

```
pre-analyze-check: stage=plan decision=pass errors=0 advisories=103 waived=0
{"fr": 30, "sc": 9, "tasks": 0, "clauses": 39, "files": 13}
```

All 103 advisories are `missing-path` findings naming exactly the ten deliverable path families this
feature creates (owner document and its installed form, the five fact files, the engine and its mirror,
the five guard files, the fixtures directory). No error-class finding exists. Full capture:
`test-evidence/pre-analyze-plan.txt` and `test-evidence/pre-analyze-plan.json`.

## A-4 — validate-decision-tensions.py (verbatim tail, `test-evidence/plan-decision-tensions.txt`)

```
status: ok
scanned: 284 lines, 0 record(s)
channel: value_domain=HIGH-or-0, high=0
0 error(s), 0 warning(s)
EXIT=0
```

## A-5 — validate-requirements.py (unchanged requirements, `test-evidence/plan-validate-requirements.txt`)

```
status: ok
scanned: 310 lines, 39 definition rows, 2 shared strings
0 error(s), 0 warning(s)
EXIT=0
```

## A-6 — Workspace guard (snapshot before remaining gates, check after)

```
python3 scripts/python/workspace-guard.py --snapshot .specify/specs/109-prompt-adherence/test-evidence/workspace-plan.json --repo .
recorded .specify/specs/109-prompt-adherence/test-evidence/workspace-plan.json
EXIT=0

python3 scripts/python/workspace-guard.py --check .specify/specs/109-prompt-adherence/test-evidence/workspace-plan.json --repo .
clean
EXIT=0
```

## A-7 — Mirror and command-copy baselines (measured before the artifact writes)

```
python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (23 files, byte-identical)
ok    skills/external/ == .specify/skills/ (439 files, byte-identical)
ok    skills/internal/ == .specify/skills/internal/ (139 files, byte-identical)
ok    agents/ == .specify/agents/templates/ (20 files, byte-identical)
ok    scripts/ == .specify/scripts/ (133 files, byte-identical)
ok    shared/ == .specify/shared/ (117 files, byte-identical)
EXIT=0

python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
EXIT=0
```

Post-artifact re-run: both exit 0 (this stage changes no mirrored file; the criterion stays "no NEW
drift on the touched pairs").

## A-8 — Sensor read surfaces (executed at plan time)

```
python3 .specify/scripts/python/run-determination.py --action history --target /speckit.clarify --limit 2 --json
→ exit 0; counts.total=43; record run_id r20261126T071500Z-108a; determined_at 2026-11-26T08:19:31Z

python3 .specify/scripts/python/exec-quant.py --action list-records --format json --since 2026-11-27
→ exit 0; records carry kind speckit.exec-quant, schema_version 2, run_id, collected_at

python3 .specify/scripts/python/feedback-utils.py --action list --limit 2 --format json
→ exit 0; {"count": 2, ...}; frontmatter metadata only (id/run_id/created/feature/feature_id/file)

python3 .specify/scripts/python/evidence-utils.py --action list --limit 5
→ exit 0; one entry (runId ev-20261113-161502-improve-skills, manifest created, lanesSummary)

python3 .specify/scripts/python/probe-utils.py --action probes --format json
→ available true; classes 11, objects 130, errors 0

python3 .specify/scripts/python/measure.py --action summary --workspace .
→ exit 0; read=545, 27 figures measurable (projection over the exec-quant store)

python3 .specify/scripts/python/declaration_reader.py --action get --fact evidence-seven-states
→ exit 0; the seven-state statement body as declared
```

Read-API pointers: `run-determination.py` `load_determinations` :1170, `FINDINGS_PROJECTION_FIELDS` :210,
`GREEN_UNPROVEN_VERDICT` :243; `exec-quant.py` `load_records` :1124, `KIND` :147; `feedback-utils.py`
`scan_entries` :420, `entry_meta` :538; `evidence-utils.py` `load_index` :138, `FINDINGS_KIND` :48,
`SCHEMA_VERSION` :47; `probe-utils.py` `load_probe_registry` :283, `PROBE_DEFS_REL` :202;
`confirmation-gates.md` :93.

## A-9 — Runtime store layout fact (A-5 adaptation)

```
declaration_reader.load_fact(<repo>, "runtime-store-layout")["body"]["statement"]
→ store count: 14
→ names: coaching,evidence,exec-quant,feedback,housekeeping,knowledge,migrate,renumber,retention,sanitize,session,todo,tools,trigger
→ any per-store `root` key: False
→ sensor stores present: session, knowledge, feedback, evidence, exec-quant
```

Roots are the documented `.specify/<store-name>/` projections; the engine holds no second root table.

## A-10 — Flow-class reading

Dispatch quartet: `flow_class=execution; source=declaration; marker=; error=-`.
Local lookup: `flow-class-check.py --action lookup --unit-id "spec:109-prompt-adherence"` →
`flow_class: execution`, `flow_type: -`, `source: declaration`, `marker: null`, `neutral: false`.

## A-11 — Plan-stage concurrency record

`requested=1`; `effective=not_evaluated`; `effective_reason=single-unit`. Units enumerated before the
shape: research; plan.md; data-model.md; six contract files; quickstart.md; feature-ref.md; Feature
Integration edit; gate runs and records. The representable unit set has size 1 (the assignment forbids
dispatching agents; the driver partitioned the stage as one serial work package — checkpoint 02 § 4).
Reason code `single-unit` read from `shared/declarations/facts/serial-reason.yaml`; no dispatch intervals
were produced.

## A-12 — Registry posture (disclosure)

Feature Integration performed as the plan stage's mandated duty: `.specify/features.md` row 109 advanced
`Draft → Planned` with a plan note, and `.specify/features/109-prompt-adherence.md` carries `Status:
Planned` with the plan entry. The stage brief's "spine/registry" boundary is read as the driver state
spine and `.specify/register.md` — both untouched; this plan coins no new durable identifier (decision
tensions are recorded as N/A with the upstream records consumed by reference). Precedent: 106 and 108
plan executors updated the feature index/detail in their plan commits.

## A-13 — Same-author scoring (disclosure)

The create-plan same-author gate would delegate scoring to fresh-context subagents; the executor role
forbids dispatching other agents, so the Constitution Check and the Post-Generation review are a
disclosed direct self-read (the gate's fallback path), recorded per row in `plan.md` (PA6).

## A-14 — In-passing corrections (disclosed)

1. Draft plan-assumption ids `PA-10`…`PA-16` matched the gate's external-contract-clause pattern
   (`[A-Z]{2,4}-\d{2}`) and produced seven false `external-clause` advisories; renamed to `PA10`…`PA16`
   (local, reversible; the advisory class disappeared on re-run).
2. A backticked dead path literal naming the source tool's Python package directory produced a
   `missing-path` advisory; reworded to a description with no dead path (the requirements stage's A-3
   already states this mapping without a literal).
3. The feature-index row edit initially dropped one inter-cell space; repaired in place before commit.

## A-15 — Test execution

`not-run-docs-only` — this stage adds and changes documentation artifacts only. The guards the plan
names are authored at implementation time (contract C-040); the implement stage captures the suite
baseline once through `scripts/bash/run-tests.sh`.

## Anomaly line

未发现异常（in-passing corrections disclosed in A-14）。