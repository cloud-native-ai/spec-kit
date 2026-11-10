# Contract — Digest Role-Edge View (`status-digest.py`)

**Status**: design contract (Feature 095) · Existing digest contract: `.specify/specs/088-speckit-visualization/contracts/status-digest.contract.md` (C-41…C-46, DG-01…DG-07) — this contract **extends** it and MUST NOT contradict it. Owner of the role model: `.specify/shared/definitions/superagent-definitions.md` ([[STR-004]]).

## C-1. One reader, one renderer

`status-digest.py` remains the only digest renderer (FR-029, FR-035). The role view is computed through the role-edge engine's **importable interface** (`contracts/role-edge-engine.contract.md` C-1): exactly one `read_carrier_inputs` call per digest run over the engine's default carrier roots (state / teams / logs / registry), then exactly one `evaluate_role_model` call. That materialization is the digest's single state-read pass — the legacy line entries and the role view both derive from it, and **no carrier root may be read twice**. A second read of any carrier, a second parser or a second renderer is a red defect.

## C-2. Entry fields (FR-029)

Every rendered executor entry carries: `id` (identity), `parent` (parent-edge identity), `roles` (role set; both-roles rendered via the `dual-role` marker), `depth`, `state`, `last_activity` + `age`, `stale`. Table columns and JSON keys share these names; the table may localize labels but MUST NOT invent a second vocabulary.

**Schema by source type** (the merged set is a union, not a re-keying): an entry that originates from a line-registry row keeps its existing keys unchanged (`line_id`, `last_activity_at`, … — C-6) and **gains** `parent` / `roles` / `depth`; an executor row that originates outside the line registry (team member, fan-out child, driver stage) uses the role-view names `id` / `last_activity` for the two fields whose legacy names are line-specific, and states `project_dir` / `branch` / `stage` as `null` where the source type does not carry them. The two field families never mix inside one entry.

## C-3. Bounded output (existing semantics, unchanged)

- Entry cap: the digest's existing cap applies to the merged entry set.
- Truncation: `omitted=<n>` (JSON `omitted`) MUST state the number of entries not shown. Truncation without the declaration is red.
- Empty set: the existing `nothing-running` state (`NOTHING_RUNNING`, exit 3) renders exactly as today — not an empty summary.
- `stale`: the existing stale-bound judgement and its per-row marker/note are reused verbatim.

## C-4. Fan-out shape (FR-031)

One digest read renders a parent row plus one row per child for an N-child fan-out (N=10 in the acceptance fixture); no separate role dashboard or parser.

## C-5. Field provenance

`parent` / `roles` / `depth` come from the role-edge evaluation (same run); `state` / `last_activity` / `stale` keep their existing sources (artifact triplet, status spine, watch model). The digest MUST NOT derive any of these from conversation memory or process scans.

## C-6. JSON shape

Existing keys (`registry_dir`, `generated_at`, `cap`, `stale_bound_seconds`, `entries`, `all_entries`, `omitted`, `profile`, `state_summary`, efficiency block) keep their names and meanings. `entries[]` gain `parent`, `roles`, `depth`; rows that come from the line registry keep `line_id` / `last_activity_at` (C-2 governs which family a row uses). `--format table` remains the default; `--format json` remains available.

## C-7. Guarding tests

`tests/contract/test_status_digest_roles.py`: field presence (table + JSON); `omitted` on truncation; `nothing-running`; fan-out shape; single-reader assertion (no second store read — structural); single-renderer assertion (one render function); mutation: drop any field or add a second renderer → red.

## C-8. Command examples

> **Premises / execution status (per example)**: the role fields do **not exist yet**; the `--action digest` command itself exists and ran today (2026-11-10) on this tree, rendering its current header (generation timestamp with timezone, entry cap, silence threshold, profile, registry directory) and its current six columns; the captured output is in `test-evidence/plan-stage-evidence.md`. The extended-field expectations below are pinned by `tests/contract/test_status_digest_roles.py` (route: contract-test pinning). Premises: role fields are added to `project_entry` and to both formats; the `nothing-running` literal and exit code 3 are unchanged (measured today); fixtures exist under `tests/fixtures/superagent-role/`.

```bash
python3 .specify/scripts/python/status-digest.py --action digest
python3 .specify/scripts/python/status-digest.py --action digest --format json
```

Expected after implementation (pinned by the test, not assumed now): each entry shows `parent`, `roles` and `depth` beside the existing fields; with zero entries the output is the existing `nothing-running` state; with more entries than the cap, `omitted=<n>` appears.
