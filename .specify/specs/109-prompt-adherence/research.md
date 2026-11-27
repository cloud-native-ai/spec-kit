# Research — Prompt Adherence Evaluation（提示遵从度评价）— Spec Kit port

**Spec**: `.specify/specs/109-prompt-adherence/requirements.md`
**Feature**: 109 Prompt Adherence Evaluation（提示遵从度评价）
**Status**: Phase 0 research record (2026-11-27). Findings below were measured against this tree during
this plan run; the behavior authority is the closed source set at
`/storage/project/cloud-native-ai/ai-harness/.ah/specs/092-prompt-adherence/` (plan, research,
data-model, five contract files, quickstart), and integration authority is this tree's owners.

## R-1 — Source-to-target adaptation is complete and verified

The port renames every source surface; no unresolved source naming may ship.

| Source form | Target form | Verified |
|-------------|-------------|----------|
| `.ah/` (paths) | `.specify/` | every path below measured in this tree |
| `/ah.*` (unit ids) | `/speckit.*` | `run-determination.py` accepts `/speckit.<command>` (its `--unit-id` help) |
| `ai-harness` (product) | Spec Kit / `specify` CLI | README + `pyproject.toml` `[project.scripts] specify` |
| `ai-harness init` | `specify init` | `src/specify_cli/__init__.py` init flow |
| `ah.exec-quant` / `ah.evidence-findings` (kind tokens) | `speckit.exec-quant` / `speckit.evidence-findings` | `exec-quant.py:147`; `evidence-utils.py:48` |
| source tool's Python package directory | no path literal in this port; the tree's CLI package is `src/specify_cli` and this feature does not reference it | requirements A-3 mapping rule |
| `scripts/python/store_layout.py` (source-only module) | absent here; the layout fact is read through `declaration_reader.py` (A-5) | `ls scripts/python/store_layout.py` → absent; precedent: `concurrency-check.py:119`, `sanitize-utils.py:40`, `seal-utils.py:52` |

Input surfaces measured present (2026-11-27): `scripts/python/declaration_reader.py`,
`run-determination.py`, `exec-quant.py`, `feedback-utils.py`, `evidence-utils.py`, `probe-utils.py`,
`sync-mirrors.py`, `regen-command-copies.py`, `script-interface-check.py`,
`shared/declarations/facts/runtime-store-layout.yaml`, `quant-record-schema.yaml`,
`evidence-seven-states.yaml`, `shared/workflow/symlink-model.md`, `shared/guidelines/better-harness.md`,
`shared/definitions/dogfooding-definitions.md` (§ 2.1), `shared/definitions/script-interface-definitions.md`,
`scripts/bash/run-tests.sh`, `tests/contract/test_runtime_store_layout.py`. Deliverable paths absent by
design (this feature creates them): `scripts/python/prompt-adherence.py`,
`shared/definitions/prompt-adherence-definitions.md`, the five `shared/declarations/facts/prompt-adherence-*.yaml`
files, the five guard files, `tests/fixtures/prompt-adherence/`.

## R-2 — Six sensor read surfaces exist in process, with the fields the catalog predicates need

| Row | Store | Owning read surface (measured) | Identity | Timestamp |
|-----|-------|--------------------------------|----------|-----------|
| `run-determination-record` | `.specify/session/` (memory-tier entry tagged `run-determination`, fenced JSON body) | `run-determination.py` `load_determinations(workspace_root, unit_id=None)` (`:1170`) | `run_id` | `determined_at` (`:1140-1141`) |
| `exec-quant-record` | `.specify/exec-quant/` (legacy `records.jsonl` + `records/*.json`) | `exec-quant.py` `load_records(workspace_root)` (`:1124`) | `run_id` | `collected_at` |
| `feedback-entry` | `.specify/feedback/*.md` (frontmatter only) | `feedback-utils.py` `scan_entries(workspace_root)` (`:420`) → `entry_meta` (`:538`) | `run_id` | `created` |
| `gate-observation-record` | same feedback store; family = `run_id` prefix `gate:` | same read surface | `run_id` | `created` |
| `evidence-finding` | `.specify/evidence/<run-id>/findings.json` items | `evidence-utils.py` `load_index(root)` (`:138`) (run envelope) | item `runId` | run manifest `created` |
| `probe-registry-declaration` | `.specify/shared/definitions/probe-definitions.md` | `probe-utils.py` `load_probe_registry(workspace_root)` (`:283`) | registry `object_id` | none (declaration, not a record) |

Live readings taken this run (excerpts):

- `python3 .specify/scripts/python/run-determination.py --action history --target /speckit.clarify --limit 2 --json`
  → exit 0, `counts.total=43`, per-record `run_id` (`r20261126T071500Z-108a`) and `determined_at`.
- `python3 .specify/scripts/python/exec-quant.py --action list-records --format json --since 2026-11-27`
  → exit 0, records carry `kind: speckit.exec-quant`, `schema_version: 2`, `run_id`, `collected_at`.
- `python3 .specify/scripts/python/feedback-utils.py --action list --limit 2 --format json`
  → exit 0, frontmatter metadata only (`id`, `file`, `unit_id`, `unit_type`, `run_id`, `feature`,
  `feature_id`, `created`, `summary`).
- `python3 .specify/scripts/python/evidence-utils.py --action list --limit 5`
  → exit 0, one entry (`runId` `ev-20261113-161502-improve-skills`, manifest `created`, `lanesSummary`).
- `python3 .specify/scripts/python/probe-utils.py --action probes --format json`
  → `available: true`, 11 classes, 130 objects, 0 errors.

In-process import is the house precedent: `scripts/python/measure.py` loads `exec-quant.py` with
`importlib` (`measure.py:28,39,80`) and uses the engine's own read path. The gate family's structured
identity is fixed by `shared/guidelines/confirmation-gates.md:93`
(`--run-id "gate:<gate_id>:<UTC ts>"`); the recorded decision signal lives only in the entry body (prose)
and MUST NOT be read.

**Deviation-class derivations measured in the owning engine**: `run-determination.py` owns
`COMPARISON_VERDICTS` / `CORRECTNESS_VERDICTS` containing `not_evaluated` (`:140-141`) and
`GREEN_UNPROVEN_VERDICT = ("not_evaluated", "green_unproven")` (`:243`); `evidence-utils.py` owns
`FINDINGS_KIND` (`:48`) and `SCHEMA_VERSION = 1` (`:47`); `run-determination.py` owns
`FINDINGS_PROJECTION_FIELDS = ("id", "lane", "evidenceState", "summary", "signals")` (`:210`).

## R-3 — The declaration layer accepts five new closed-set facts without code change

`shared/declarations/contract.yaml` owns `required_fact_keys` (`fact`, `kind`, `statement`, `consumers`,
`former_carriers`; `note` optional) and the closed five-value `fact_kinds`. The reader is
`scripts/python/declaration_reader.py` (`find_repo` `:120`; `load_fact` `:400`); the completeness judge is
`scripts/python/harness-triple-check.py`, whose condition (c) holds when the consumer engine's source
text references `declaration_reader` and the fact slug (`has_read_point` `:166`). A sibling fact of kind
`closed-set` already exists (`evidence-seven-states.yaml`), so the five new facts add data files only.

Observation states get no sixth fact (FR-018): the engine composes the seven-state sequence read by
`evidence-utils.py` with the `not_evaluated` literal owned by `run-determination.py`'s verdict domains.
No value domain is re-spelled.

## R-4 — A machine-parsed authored document is a house precedent, and the owner doc is one by requirement

FR-003 requires the coverage map to be machine-checkable in both directions, so the owner document is a
**registry** by design. Precedent: `scripts/python/probe-utils.py` parses the table registry in
`shared/definitions/probe-definitions.md` (`load_probe_registry`; measured 11 classes / 130 objects / 0
errors on 2026-11-27). The plan therefore fixes the owner document's stable table shapes (catalog,
blind-spot register, coverage map) and pins them with a contract test; the engine validates every cell
against the declaration sets and treats an unknown token as a hard error (exit 2, no reading).

## R-5 — Distribution rides the existing mirror and init flow

`scripts/python/sync-mirrors.py` `MIRROR_PAIRS` (`:93-100`) projects `shared → .specify/shared` and
`scripts → .specify/scripts`; `specify init` copies the `shared/` and `scripts/` trees
(`src/specify_cli/__init__.py:2517-2522` for `scripts`, `:2744-2752` for `shared`). Baselines measured
2026-11-27 before any edit:

- `python3 scripts/python/sync-mirrors.py --check` → exit 0; all six pairs byte-identical
  (templates 23 / skills/external 439 / skills/internal 139 / agents 20 / scripts 133 / shared 117
  files), six projections `ok`.
- `python3 scripts/python/regen-command-copies.py --check` → `OK: all per-tool command copies match the
  source templates`, exit 0.

The implementation-time criterion is **no NEW drift on the pairs this spec touches**, judged against
these baselines — never a pre-written absolute exit code.

## R-6 — Evidence findings carry their own state reading but no SDD run identity

`evidence-utils.py` `load_index` returns run envelopes (`runId`, `target`, `created`, `lanesSummary`,
`file`); finding items live inside `<run-id>/findings.json` and the item projection field set is pinned in
`run-determination.py` (`FINDINGS_PROJECTION_FIELDS`). Evidence runs identify by their own `ev-…`
identity, never by an SDD run id — so in a per-run reading scoped by an SDD identity the evidence row is
honestly unmatched, and the longitudinal window is the cross-store view. No owning function returns
finding items; the engine reads the item fields after `load_index`, with a drift guard pinning the field
names against the owning engine's constants and a seeded fixture.

## R-7 — Feedback store metadata is readable without touching prose

`feedback-utils.py` `scan_entries(workspace_root)` derives the entry list from frontmatter only
(`entry_meta`: `id`, `file`, `unit_id`, `unit_type`, `run_id`, `probe`, `kind`, `slice`, `feature`,
`feature_id`, `disposition`, `introspection_ref`, `disposition_reason`, `partial`, `created`, `summary`).
Gate observation entries are ordinary entries whose `run_id` begins `gate:`. The reading uses this
metadata surface only; entry bodies (review prose, points) never enter an output.

## R-8 — The containment oracle is computable from the declared store roster (adapted, A-5)

`shared/declarations/facts/runtime-store-layout.yaml#/statement` declares 14 stores and carries **no
per-store `root` key** (measured through `declaration_reader.load_fact`: `statement.stores` count 14;
`sorted(names)` = `coaching, evidence, exec-quant, feedback, housekeeping, knowledge, migrate, renumber,
retention, sanitize, session, todo, tools, trigger`; `any("root" in v)` = false). The roots are the
documented `.specify/<store-name>/` projections. A hash manifest over those roots (repo-relative sorted
paths + SHA-256 of bytes, interpreter bytecode caches excluded) is a decidable before/after oracle for
the read-only claim (SC-002 / FR-024); the existing `tests/contract/test_runtime_store_layout.py` owns
the roster-side guard.

## R-9 — The script interface contract and the exit-code house table

`shared/definitions/script-interface-definitions.md` § 1.0 places read-only scripts in the
`optional-read-only` class (`--help` / `--version` recommended); FR-023 elevates this engine to the full
contract, and its checker is `scripts/python/script-interface-check.py` (`--files` selects the engine).
The house exit domain (`0` ok / `1` finding / `2` input error) is carried by
`shared/declarations/contract.yaml` `exit_codes` and by the engines' `EXIT_*` constants. Design: exit
`0` whenever a reading is emitted (including `no-data` and `not-found`) and when the coverage check is
clean; exit `1` when `--check-coverage` reports map findings; exit `2` when no reading can be produced
(unusable declaration layer or owner document, unknown token, undeclared store name, invalid arguments,
`--run` combined with a window).

## R-10 — Same-author scoring fallback, baseline channel and wrap-up accounting

The create-plan same-author gate would delegate plan scoring to fresh-context read-only subagents; this
stage's assignment forbids dispatching other agents (the executor role's "do not dispatch" boundary), so
the Constitution Check and the Post-Generation review are a disclosed direct self-read (the gate's
fallback path), recorded per row in `plan.md`.

Baseline channel: the first dated baseline reading (FR-026) lands as **one feedback entry** through
`feedback-utils.py --action record` at implementation time, under the implementing stage's unit and run,
carrying the reading's status, per-row states, the declaration-set digest and source references. Replay
is one engine run against the cited references; nothing becomes a new aggregate. The call shape was
measured at plan time by this stage's own wrap-up records (feedback entry with `feature` /
`feature_id`; run-determination record; exec-quant record).

## R-11 — Test entry, markers and plan-stage evidence discipline

`pyproject.toml` declares the `contract` and `integration` markers (`:57-59`); the test entry is
`scripts/bash/run-tests.sh` (parallel default `-n <effective> --dist load`; `SPECKIT_PYTHON` ladder
`:61-73`). The plan stage is docs-only and records `not-run-docs-only` in its stage record; the
implement stage captures the full-suite baseline once (contract C-040) and judges new failures by name.

## Re-measure list (for `/speckit.tasks` and `/speckit.implement`)

- Declared store roster: 14 stores, no `root` key (R-8) — re-read through `declaration_reader` before
  writing the containment guard.
- Probe registry counts: 11 classes / 130 objects / 0 errors (R-2) — the owner-doc guard should not pin
  these numbers; they belong to `probe-utils.py`'s own guard.
- Mirror baselines: `sync-mirrors.py --check` exit 0 and `regen-command-copies.py --check` exit 0 (R-5).
- `SPECKIT_PYTHON` resolution on the executing host (R-11).
- The six read surfaces' function names and record fields (R-2) — a drift red is a finding about the
  owning engine, not a licence to re-parse.

## Residual unknowns (tracked, not blocking)

- **RU-1** — A future owner-sanctioned persistence change could make instruction-reconcile observations
  a catalog row; today it stays a blind spot (FR-028/FR-029).
- **RU-2** — Whether the host product's own prompt surfaces ever become observable is outside this
  framework's authority (blind spot `host-prompt-content`); no design work is planned here.
- **RU-3** — A composite adherence score remains forbidden (requirements A-11, FR-025); reopening requires
  a new decision and spec, not an edit.