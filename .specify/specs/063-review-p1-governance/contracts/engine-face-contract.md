# Contracts: Compiled Wrap-up Face & Engine Arguments（F4）

**Spec**: `.specify/specs/063-review-p1-governance/requirements.md`
**Convention**: canonical clause form (`**C-N**` md-bold-closed) per `shared/definitions/contract-clause-definitions.md` § 3. Shared strings cited as [[STR-NNN]] per the requirements' table.

> Owner anchors (current code, verified 2026-10-19): renderer `scripts/python/probe-utils.py` `_render_call_line()` (engine line today emits only `--unit-id`/`--unit-type`); validations `scripts/python/run-determination.py` `action_determine()` (sequential one-at-a-time `InputError`s) and `scripts/python/feedback-utils.py` `action_record()` (sequential `FeedbackError`s); registry truth source `shared/definitions/probe-definitions.md` § Handler (columns `handler_id|kind|action|mode|order|behavior_owner`) and § HandlerBinding. Current engine-line parser `_CALL_ENGINE_RE` extracts `(owner, action)` — extended lines keep matching because the regex anchors on the `python3 <owner> --action <action>` prefix.

## Placeholder convention (declared once)

**C-20**: 占位约定 the compile-embeds renderer MUST render, for every `kind=engine` handler line, the action's full required-argument set plus its declared source arguments, with run-scoped values carried as angle-bracket placeholders (e.g. `--run-id <RUN_ID>`, `--complexity <COMPLEXITY>`, `--review <REVIEW>`). The convention — placeholder syntax, the substitution rule ("尖括号为本轮运行时值，代入后照抄执行"), and the rendered-set membership — MUST be declared in the registry (`shared/definitions/probe-definitions.md` § Handler note), not per command hand-written; the rendered `## Wrap-up` section carries the one convention line when any of its engine lines contains a placeholder. The face for `run-determination determine` MUST include at least the required set (`--run-id`, `--complexity`) and the source exemplars (`--session-file`, `--session-rows`, `--tool`, `--declared-check`, `--green-check`) (FR-014, SC-007)。

**C-21**: 拒收参数不渲染 an argument the engine action does not accept MUST NOT be rendered. The rendered set per (engine, action) is exactly the engine's own manifest (C-22); the renderer MUST NOT hold a hand-written argument table (FR-030). Verification: a contract test renders a fixture manifest and asserts a non-accepted flag never appears (FR-014, SC-007)。

**C-22**: 参数集合由引擎派生 each wrap-up engine (`run-determination.py`, `feedback-utils.py`, `exec-quant.py`) MUST expose a machine-readable argument manifest for its actions (e.g. a `--action args-manifest` emitting JSON `{action: {required: [...], source: [...]}}`), BUILT FROM THE ENGINE'S OWN PARSER so the parser stays the single source of truth. `probe-utils.py --action compile-embeds` MUST obtain each handler's manifest from its engine at compile time; an engine/action pair with no manifest MUST fail the compile loudly (registry/engine divergence is a fast-fail surface, never a silent unit-id-only fallback). The manifest action joins the engine action closed set (`contracts/engine-action-sets.md` + `tests/contract/test_probe_engine_action_sets.py` updated in the same change) (FR-014, FR-030, SC-007)。

## Engine error & idempotency semantics

**C-23**: 缺参一次全列 `run-determination.py` (`--action determine`) and `feedback-utils.py` (`--action record`) MUST report ALL missing required arguments in ONE error message (single `InputError`/`FeedbackError` listing every missing flag), replacing the sequential one-at-a-time checks at `run-determination.py:1390-1397` and `feedback-utils.py:716-728`. The input-error exit code convention stays: 2 for both engines. A call missing ≥2 required args yields exactly one error naming all of them (FR-015, SC-008)。

**C-24**: 幂等语义不变（E1 裁决） the `(unit_id, run_id)` idempotency at `run-determination.py:1410-1413` MUST remain byte-for-byte in behavior: a re-run with an existing key returns `{"duplicate": true, ...}` with exit 0; the engine MUST NOT mint, derive, or substitute a run-id under any circumstance; a caller-side re-measurement under a new run-id is a caller decision recorded in that caller's run evidence. feedback-utils' duplicate no-op (`action_record` existing-entry branch) is likewise unchanged. Verification: a mutation-style contract test asserts the duplicate path and asserts no engine code path writes a record with a run-id it generated (FR-017, SC-008)。

**C-25**: 全单元重编译与收口 after the renderer/registry changes land, ALL compiled units MUST be recompiled via `probe-utils.py --action compile-embeds`; `--action compile-embeds --check` MUST report zero drift; `--reconcile` closes reconcile-guard surfaces where applicable (compile → regen → sync fixed order per the probe system's compile protocol). The `backlog.md` row dated 2026-10-15 (the compiled-face missing-args row, route `direct-fix`, status `open`) MUST flip to `closed` in the same commit as the recompiled units, with the check output as evidence (FR-016, SC-007)。

## Face shape (informative example of the contracted output)

```text
1. Run Determination — `python3 scripts/python/run-determination.py --action determine --unit-id "/speckit.review" --unit-type command --run-id <RUN_ID> --complexity <COMPLEXITY>`；source args when available: `--session-file <PATH> --tool <NAME> --declared-check <CLAUSE> --green-check <CLAUSE>`
   <占位约定行：尖括号为本轮运行时值——代入后照抄执行>
```

*This block is the clause C-20 shape target, not a verbatim render commitment; the exact flags rendered are the engines' manifests at compile time (C-22). The final rendered text is pinned by contract tests at implement (SC-007's verbatim-execution check runs against the real compiled faces, not this example).*

## Traceability

| Clause | Finding | FR | SC | Primary artifact |
|--------|---------|----|----|------------------|
| C-20 | F4 | FR-014 | SC-007 | scripts/python/probe-utils.py + shared/definitions/probe-definitions.md |
| C-21 | F4 | FR-014 | SC-007 | scripts/python/probe-utils.py |
| C-22 | F4 | FR-014/FR-030 | SC-007 | run-determination.py + feedback-utils.py + exec-quant.py + probe-utils.py |
| C-23 | F4 | FR-015 | SC-008 | run-determination.py + feedback-utils.py |
| C-24 | F4/E1 | FR-017 | SC-008 | run-determination.py + feedback-utils.py |
| C-25 | F4 | FR-016 | SC-007 | all compiled units + .specify/memory/feedback/backlog.md |
