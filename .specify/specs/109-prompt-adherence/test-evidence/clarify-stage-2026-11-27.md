# Clarify Stage Evidence — 2026-11-27

Line `prompt-adherence`; run `r20261127T053750Z-109a`; stage `clarify`; baseline `d6111b70c`; branch `109-prompt-adherence` (worktree).

## Mode & target

- **Mode A (post-requirements)** — `plan.md` absent in `.specify/specs/109-prompt-adherence/`; target `.specify/specs/109-prompt-adherence/requirements.md`. Writability confirmed by the landed edits (no root-owned path).
- **Unattended adjudication, no user questions** — the candidate queue was the brief's six scan areas plus the Feature-binding duty the requirements stage deferred (A-2). Every answer stayed inside the recorded adjudications (A-1…A-18), the closed source 092 capability, and measured facts of this tree; no option space was invented.

## Feature binding (lookup evidence)

- **Binding**: **new standalone Feature 109** `Prompt Adherence Evaluation`, `Draft`. Registry lookup: no 109 row existed; max registered row was 108; the features index header and rows were edited together (`Total Features` 104 → 105, 105 counted rows verified by `grep -cE '^\| [0-9]{3} '`).
- **Reuse scan correction (in passing)**: the requirements-stage candidate scan cited sensor owners with numbers that do not resolve in either tree (`069 probe`, `091/059 exec-quant`, `093 feedback`, `080/run-determination`, `106 evidence lanes`). Measured owners in this tree: probe registry/`Wired` → **Feature 056** (`shared/definitions/probe-definitions.md`); exec-quant → **Feature 059** (`scripts/python/exec-quant.py`); feedback store/gate family/red lines → **Feature 028** (`shared/workflow/feedback-step.md`); managed store roots → **Feature 105**; evidence lanes/findings → **Feature 038** (`scripts/python/evidence-utils.py`, `shared/declarations/facts/evidence-lanes.yaml`); run-determination records → engine `scripts/python/run-determination.py` with schema/value domains owned by `shared/workflow/feedback-step.md` § Run Determination. `Related Feature` now names these verified owners; the "no existing adherence-reading mechanism" conclusion is unchanged.
- **Integration duties discharged**: index row 109 (`Draft`, detail pointer, spec path, dated note); detail `.specify/features/109-prompt-adherence.md` created from the template; reverse cross-reference written into `.specify/features/028-feedback-mechanism.md`. Feature 105 has only an index row (legacy entry, no detail file) — per the Feature Integration Protocol its relation is recorded in the new Feature's detail, and no detail file was created for it.
- **No ID coined**: `.specify/register.md` was not touched.

## Six-area adjudication (written back in place; record appended under `## Clarifications` > `### Session 2026-11-27（无人值守 clarify 阶段…）`)

| Brief area | Decision | Where integrated |
|---|---|---|
| 1. Sensor mapping | Six rows stay exactly FR-028; each reads through its owning engine (`load_determinations`, `load_records`, `scan_entries` ×2, `load_index` + `FINDINGS_PROJECTION_FIELDS`, `load_probe_registry`); `measure.py` is a read-only projection over the exec-quant store — no separate row, engine never calls it, its contract stays an FR-007 no-touch; no source sensor is missing in this tree (the only read-surface divergence is the layout reader, A-5/FR-030) | FR-005, Overview, Session rows 1 |
| 2. Reading semantics | Absence four-way derivation (`source-unavailable` / positive cap / `invalid-source` / `no-matching-records` with `not_evaluated`-vs-`Unobserved` split by scope); reading status derivation (`no-data` / `not-found` / `partial` / `complete`, all exit 0) shared by both output forms; half-open window with `open` literal and boundary side; window-zero-records → `no-data`; baseline = default-scope per-run reading dated by its feedback entry, replay by re-run with the reading's declaration-set digest | FR-011, FR-014, FR-015, FR-026, Edge Cases, Session rows 2–4 |
| 3. Coverage map | Catalog add/retire = one owner revision plus the `prompt-adherence-signals.yaml` member edit in the same change; engine changes only when the row's read surface changes; no second mapping table/registry; retired rows' dated records stay replayable; "drift" = definition drift (guard-time, not a runtime output) + instruction drift (blind spot) — no drift metric exists | FR-004, Session rows 4–5 |
| 4. Engine contract | Single documented invocation unchanged; workspace resolution pinned (`--workspace-root` else nearest `.specify/` ancestor; `declaration_reader.find_repo` for owner/declarations; Two Hats boundary with a negative assertion); bounded output, sorted-key JSON and exit-code closure already normative | FR-023, Edge Cases, Session row 6 |
| 5. Distribution | No new registration: init copies the `shared/` and `scripts/` trees (owner doc, five facts, engine arrive); mirror pairs `shared → .specify/shared`, `scripts → .specify/scripts`; no `.specify/.gitignore` rule and no `runtime-store-layout.yaml` change (no new store root); tests/fixtures do not ship | A-6, Session row 7 |
| 6. Tests | Source C-001…C-046 mapped to five guard families (owner / declarations / engine / readonly contract tests + one integration init test); baseline clauses ride the engine audit-replay leg plus the dated entry; C-042 documentation-only; C-037's ambient-section clause stays with the existing full suite; runner `scripts/bash/run-tests.sh`, markers `contract`/`integration`, fixtures `tests/fixtures/prompt-adherence/`, no new runner, no `slow`/`serial` need | FR-024, Session row 8 |

## Gates (verbatim captures)

- `validate-requirements.py .specify/specs/109-prompt-adherence/requirements.md` → exit 0, `status: ok`, **0 error / 0 warning**, `[id-contiguous|doc-order|ref-resolvable|marker-count|dup-id|path-marker]` all pass, scanned **310 lines, 39 definition rows, 2 shared strings** → `test-evidence/clarify-validator.txt`.
- Only this stage's own check was run. Driver-owned gates (`overlap-check`, `pre-analyze-check`, workspace guard) were deliberately not executed; the overlap-relevant boundary is recorded below.

## Derived-count revisit

- No FR / SC / STR addition, removal or renumbering: live counts stay **30 FR (FR-001…FR-030) / 9 SC (SC-001…SC-009) / 2 STR**, 39 definition rows. No renumbering map and no checklist count correction are due; the checklist gained one appended clarify note recording the new line reading (310) next to the requirements-stage reading (296), which stays as dated history.

## Overlap-relevant boundaries (for the driver)

- **Artifact paths written by this stage**: `.specify/specs/109-prompt-adherence/requirements.md`; `.specify/specs/109-prompt-adherence/checklists/requirements.md` (appended note); `.specify/specs/109-prompt-adherence/test-evidence/clarify-stage-2026-11-27.md`; `.specify/specs/109-prompt-adherence/test-evidence/clarify-validator.txt`; protocol-mandated registry paths `.specify/features.md`, `.specify/features/109-prompt-adherence.md` (new), `.specify/features/028-feedback-mechanism.md` (one reverse line).
- **Deliberately untouched**: existing engines (`scripts/`), shared definitions/declarations (`shared/`), runtime store layout (105), decision governance (107), templates, `.specify/instructions.md`, `.specify/register.md` (no ID coined), the driver state spine (`.specify/state/`), the main tree.
- **Records this run produces** (single records commit, per-entry files, run-named): one `.specify/session/` run-determination entry, one `.specify/exec-quant/records/*.json`, one `.specify/feedback/*.md`, one `.specify/retention/closeout/*.md` receipt — distinct paths, no shared aggregate.
- **No push**; branch stays `109-prompt-adherence`.

## Concurrency

- `requested=1`, `effective=not_evaluated`, `effective_reason=single-unit` — one bounded assignment; the six scan areas are not independent units (they share one artifact and one integration pass).

## Corrections applied in passing (disclosed)

1. **Candidate sensor-owner references**: five of the six owner references in `Related Feature` did not resolve to the named capability in this tree (see the lookup evidence above); corrected to measured Feature IDs/paths. Exactly one protocol-consistent reading (verified owners), no option space.
2. **measure-report wording**: the Overview named "exec-quant 记录与 measure 报告的读取面" as if two sensors existed; `measure.py` is a read-only projection over the same store — clarified without changing the catalog.
3. **Feature 105 legacy entry**: the taxonomy's create-branch reverse cross-reference presumes a neighbour detail file; Feature 105 has only an index row, so per the protocol's legacy-entry rule the relation lives in the new Feature's detail instead of a created detail file.

## Anomalies

未发现异常 — no state required adjudication at this layer; the three items above are corrections applied in passing, not open decisions.