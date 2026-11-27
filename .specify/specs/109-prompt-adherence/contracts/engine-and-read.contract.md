# Contract — Engine Interface and Sensor Reads

**Feature**: 109 Prompt Adherence Evaluation（提示遵从度评价）— Spec Kit port of the closed ai-harness spec 092
**Status**: design contract. Script-interface rule owner:
`shared/definitions/script-interface-definitions.md`; store roster:
`shared/declarations/facts/runtime-store-layout.yaml`; declaration reader:
`scripts/python/declaration_reader.py`.

## C-030 — One documented invocation, one read-only engine

**Statement**: the entry is `scripts/python/prompt-adherence.py`
(`.specify/scripts/python/prompt-adherence.py`), a single-file Python-stdlib read-only script. The bare
invocation prints the human-readable per-run reading for the default scope; `--run <run-id>` pins a run
identity; `--since` / `--until` request the longitudinal reading; `--json` emits the machine-readable
form; `--workspace-root PATH` selects the project; `--check-coverage` runs the FR-003 map check. No
`/speckit.*` command or skill wrapper ships in this version.
**Red when**: a second entry point appears; a flag differs; obtaining a reading requires an LLM step or
hand-composed queries.
**Test carrier**: `tests/contract/test_prompt_adherence_engine.py` (CLI surface legs);
`tests/integration/test_prompt_adherence_init.py` (installed-copy entry leg).

**Serves**: (FR-023)

## C-031 — Script interface contract satisfied

**Statement**: the engine answers `-h` and `--help` (identical body) with usage, options, side effects
(`none`) and exit-code meanings; `--version` prints one line `<script-name> <framework-version>` derived
at run time from the nearest `pyproject.toml`; an undeclared option exits 2 before any action, including
after a bare `--`. The four flags act before any read and write nothing.
**Red when**: a required flag content is missing; a version literal lives in the source; an unknown
option reaches an action or exits 0.
**Test carrier**: `tests/contract/test_prompt_adherence_engine.py` (interface legs);
`scripts/python/script-interface-check.py` stays green for the new engine.

**Serves**: (FR-022, FR-023)

## C-032 — Sensor reads use the owning engines' read surfaces; roots derive from the layout fact

**Statement**: each catalog row reads its store through the owning engine's read surface, in process,
never through a second parser: `run-determination.py` `load_determinations`, `exec-quant.py`
`load_records`, `feedback-utils.py` `scan_entries` (metadata only), `probe-utils.py`
`load_probe_registry`, `evidence-utils.py` `load_index` plus the item projection whose field names are
pinned against `evidence-utils.py`'s own constants (`FINDINGS_KIND`, `SCHEMA_VERSION`) and
`run-determination.py`'s `FINDINGS_PROJECTION_FIELDS`. The in-process import pattern follows
`scripts/python/measure.py`. The source store of every non-registry row resolves against the declared
set: the engine reads `shared/declarations/facts/runtime-store-layout.yaml#/statement` through
`declaration_reader.py` (the tree has no `scripts/python/store_layout.py`; the precedent for reading the
layout fact directly is `concurrency-check.py` / `sanitize-utils.py` / `seal-utils.py`), derives each
root as the documented `.specify/<store-name>/` projection of the declared store name (the fact carries
no per-store `root` key), and treats a row naming an undeclared store as a hard error (exit 2). The
engine MUST NOT keep a second root table. The probe row is exempt from the store lookup: it reads a
registry declaration, not a store.
**Red when**: a store's record format is re-implemented; a row bypasses its owning read function where
one exists; the evidence item fields drift from the owning engine without a guard failure; a root outside
the declared projection appears in the engine; a second root table exists.
**Test carrier**: `tests/contract/test_prompt_adherence_declarations.py` (read-point locator legs);
`tests/contract/test_prompt_adherence_engine.py` (seeded-fixture legs over all six stores; undeclared
store rejection).

**Serves**: (FR-005, FR-028, FR-030)

## C-034 — Offline, private, no transmission

**Statement**: the engine makes no network access and performs no automatic transmission; readings
remain in the project. A reading under a socket-blocked interpreter completes normally.
**Red when**: a network module is imported by the engine; a reading requires connectivity; anything is
written outside the terminal streams.
**Test carrier**: `tests/integration/test_prompt_adherence_init.py` (socket-blocked run);
`tests/contract/test_prompt_adherence_engine.py` (import-surface leg).

**Serves**: (FR-021)

## C-036 — Self-location and workspace resolution

**Statement**: the engine resolves the owner document and the declaration layer through
`declaration_reader.find_repo` (framework-source form first, `.specify/` mirror form second), and
resolves the workspace — whose stores it reads — from `--workspace-root`, else by walking the current
directory upward to the nearest ancestor holding `.specify/` (the pattern of
`evidence-utils.py` `resolve_workspace_root`). A copy-level self-location MUST fire only on a literal
`.specify` component of its own resolved path; the negative case (a source-tree copy that must not treat
itself as the installed copy) carries its own assertion.
**Red when**: the engine treats a source-tree copy as the installed copy; a nested tree misdirects the
layer read; the two hats rule in `shared/definitions/dogfooding-definitions.md` § 2.1 is contradicted.
**Test carrier**: `tests/contract/test_prompt_adherence_engine.py` (both-copies legs);
`tests/integration/test_prompt_adherence_init.py`.

**Serves**: (FR-019, FR-020, FR-023)