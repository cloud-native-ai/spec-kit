# Research — 111-general-best-practices

**Purpose**: record the measurements this plan stands on and the design points it resolved, so later stages re-measure instead of inheriting claims. Every number below was taken at plan time (2026-11-27, worktree `.specify/.tmp/sdd-loop/worktrees/general-best-practices`, branch `111-general-best-practices`, baseline commit `0419adae5`, stage baseline `f0ddff3e5`) with the command named in its row; the raw probe capture is `test-evidence/plan-probes.txt`.

## M1 — Target absence and collision check (measured)

- `ls shared/best-practices` and `ls .specify/shared/best-practices` → both absent; the port creates both, so no pre-existing content can be overwritten.
- `grep -c 'best-practices'` → `0` in `shared/definitions/framework-map.md`, `.specify/shared/definitions/framework-map.md`, `.specify/instructions.md` and `.specify/glossary.md`; the module and its registration do not exist yet.
- `.specify/features.md` has no row for 111 and `.specify/features/111-general-best-practices.md` is absent; the feature-registration stage is the only writer of those paths (FR-009 exception).

## M2 — Source module inventory (read-only)

- Five documents: `README.md` (38 lines), `programming-languages.md` (5), `system-interfaces.md` (5), `programming-frameworks.md` (5), `programming-tools.md` (8).
- The manifest's only table has three columns (模块 / 文件 / 内容), four data rows (lines 11–14), exactly one relative link per row; the link targets are the four owner files; the literal 封闭集 appears in the “四个模块(封闭集)” heading.
- Three empty categories each carry exactly one italic placeholder line containing 尚无条目 at line 5, and zero `## ` entries; `programming-tools.md` carries the seed heading `## Git clone 的默认协议` (line 5) with 实践 / 反例 / 证据 / 延伸 bullets.
- Residue scan: exactly two README lines carry product-specific text — line 3 (`ai-harness`) and line 33 (`.ah/shared/best-practices/`); zero `/ah.` matches in the five documents. These two lines are the FR-008 adaptation points; everything else ports in substance verbatim (A-8).
- The source spec set is 77 + 53 + 23 + 37 + 31 lines (requirements / plan / tasks / verification / contract); verification records three pass statuses, so the content itself is settled.

## M3 — Accumulation owners present (measured)

- `python3 .specify/scripts/python/feedback-utils.py --help` → action set starts `record,status,list,dispose,mark-submitted,reindex,package,cleanup,upstream,migrate-legacy,introspect-register,args-manifest,ingest-exec-quant,client-metrics`; `record` exists, so the observation half needs no new action.
- `shared/guidelines/knowledge-promotion.md` and `.specify/shared/guidelines/knowledge-promotion.md` exist (4849 bytes each), so the promotion half is reachable by pointer in both the source and the runtime mirror.

## M4 — Distribution path (measured)

- `src/specify_cli/__init__.py` (~lines 2743–2757) copies `resource_path/shared` into `<project>/.specify/shared` with `copy_tree_with_rewrite` whenever the packaged `shared/` exists; any new subdirectory rides this copy with no code change.
- `scripts/python/sync-mirrors.py` line 99 declares the pair `("shared", ".specify/shared", False, set())`; the engine compares and writes the whole directory tree, so the five new documents and the edited map file are covered automatically.
- `tests/contract/test_mirror_parity_suite.py` importlib-loads the engine and derives its parameter table from `MIRROR_PAIRS`; new files in `shared/` join the parameter set without a test edit.

## M5 — Mirror baseline (measured)

- `python3 scripts/python/sync-mirrors.py --check` → rc 0; the `shared` line reads `ok    shared/ == .specify/shared/ (117 files, byte-identical)`. The plan-stage criterion is therefore **no NEW drift** on the `shared` pair, never an absolute “all green” claim over unrelated pairs. The full output is kept at `test-evidence/plan-mirror-check.txt`.

## M6 — Framework map shape and ownership (measured)

- `shared/definitions/framework-map.md` is the single source of truth for the `.specify/` layout; its layout table is the only table of that kind, with three columns (What / Where / Notes) and sibling `.specify/shared/` rows that append `(framework source: shared/…)` in the Notes cell.
- `.specify/instructions.md` § Spec Kit Framework Map is a pointer to this map (it lists high-level entries and ends with “Full table with per-row notes: `.specify/shared/definitions/framework-map.md`”). No second pointer section is needed or allowed (A-6).
- `shared/guidelines/directory-governance.md` § 3 requires a new directory, or the first directory of a new kind under an existing tree, to be added to its area's map in the same change; the area map for framework layout is `shared/definitions/framework-map.md`.

## M7 — Test stack (measured)

- `scripts/bash/run-tests.sh` is the single test entry; it resolves an interpreter that imports pytest (SPECKIT_PYTHON, `.venv/bin/python`, `python3`, `python`) and forwards test paths and flags to pytest.
- `/usr/local/bin/python3` → pytest 8.4.2 on CPython 3.11.11; the profile `python3` on PATH imports no pytest (`ModuleNotFoundError`). The implement stage MUST pass `SPECKIT_PYTHON=/usr/local/bin/python3` when the runner's resolution order does not reach it.
- `tests/contract/test_general_best_practices.py` is absent; the house marker convention is `pytestmark = pytest.mark.contract` (as in `tests/contract/test_mirror_root_guard.py`).

## M8 — Registry and vocabulary state (measured)

- No Feature 111 row or detail file exists; the requirements stage deliberately bound the feature without registering it (A-3, A-10, A-21), and FR-009 leaves registry rows to a later feature-registration stage.
- `.specify/glossary.md` carries neither proposed term; the clarify stage froze the proposal text and externalized registration (A-21). This plan writes neither file.

## M9 — Containment and accounting baseline (measured)

- `git diff --name-only 0419adae5..HEAD` → 18 paths: 10 under `.specify/specs/111-general-best-practices/`, 2 in `.specify/session/`, 2 in `.specify/feedback/`, 2 per-entry records in `.specify/exec-quant/records/`. All 18 are inside FR-009's declared set; zero out-of-set changes at stage start.
- The run id is `r20261127T071500Z-111a` (state spine) and matches FR-009's record-body predicate.
- A workspace signature was recorded to `test-evidence/workspace-plan.json` before any stage probe (`workspace-guard.py --snapshot`), so a repository-root escape by a probe would be caught by the closing `--check`.

## M10 — Flow class (measured)

- `python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:111-general-best-practices"` → `flow_class: execution`, `source: declaration`, `marker: null`, rc 0. The execution-class gate set is kept unchanged: no expression-class operator rows and no `## Document Structure` section are added.

## M11 — Source specification set (read-only)

- Source 087 carries five FR, three SC, three tasks and five contract clauses, all verified pass; the target does not copy those artifacts — it re-derives the contract face from this repo's machine-decidable shapes (A-15 / A-16 / A-17 / A-18 / A-19) while porting the settled **content** (five documents, seed, mechanism declaration).

## Resolved design points

### R-1 — Five-document shape is the capability

The module ships the manifest plus all four owner files, including the three empty categories. A subset would break the closed set and hollow out the guard (A-2). The top-level file set is closed at five; nested directories are not part of the module.

### R-2 — The manifest table is the single machine-decidable carrier

The closed set is declared in exactly one table: three columns, four data rows, one relative link per row, link-target set equal to the four owner files, plus the literal 封闭集. This makes FR-001 decidable without semantic reading. A second table or an open-ended list would be unparseable and is rejected by C-103.

### R-3 — Entry shape and the placeholder invariant

An entry is a `## ` heading plus `**实践**` and `**反例 / 证据**` bullets, with optional `**延伸**`; promoted entries add `**来源**`. An empty category carries exactly one [[STR-006]] placeholder line and zero entries; the first promotion removes the placeholder in the same change. The guard judges the equivalence, not the delivery count 3 (A-16): freezing the count would make every legitimate promotion force a guard edit.

### R-4 — Seed content and the exact adaptation points

The seed ports in substance: default HTTPS clone URL; a special repository requiring HTTP (or SSH) MUST be flagged with protocol and credential requirement; the `~/.git-credentials` HTTP-credential vs HTTPS-clone mismatch counter-example; the SSH extension. Adaptation is confined to the manifest's two residue lines (M2): `ai-harness` → `Spec Kit` and `.ah/shared/best-practices/` → `.specify/shared/best-practices/`, plus the ownership line `Feature 040` → `Feature 111`. No `/ah.*` reference exists in the source documents, so that mapping is a guard condition only (FR-008).

### R-5 — Accumulation by pointer with a separable traceability form

Observation form: the existing feedback `record` action with notes carrying [[STR-001]] plus one owner-file stem — no new field, action or store. Promotion: only when general (recurrence or one explicit user correction), following `knowledge-promotion.md`; the observation record is not rewritten. Traceability: the promoted entry's `**来源**` bullet names at least one of feedback entry ID / ≥7-hex commit / quoted session utterance and states the generality basis. The seed is exempt (A-17).

### R-6 — Distribution reuse, zero code change

The two existing channels cover any new `shared/` subdirectory (M4). Writing CLI, packaging or ignore rules would be over-engineering (A-5) and is excluded by FR-006. The mirror is regenerated by the engine's write mode in the same change; byte identity is adjudicated only by the existing parity suite.

### R-7 — Registration row shape

One row in the map's single layout table, adjacent to the `.specify/shared/` rows: Where = `.specify/shared/best-practices/`; Notes = Feature 111 + `README.md` pointer + `(framework source: shared/best-practices/)`. Exactly one such row in the source table and one in the mirror table. Instructions stays a pointer (A-6, A-19).

### R-8 — Guard design boundaries

Six legs (a)–(f) exactly as FR-007; `pytest.mark.contract`; runner-only execution; red-first record required. The guard must not duplicate the mirror comparison (owned by the parity suite), must not freeze the placeholder count, and must not claim to judge entry truth (A-16, A-18). The only mechanical second-mechanism reading is the absence of `best-practices*.py` under `scripts/python/`; textual claims are review's.

### R-9 — Containment and accounting predicate

FR-009 is the single owner of the changed-path set and the residual procedure; this plan only cites it. Stage writes are limited to this feature's spec artifacts plus per-entry accounting files whose bodies carry the feature key or run id; aggregate/index files are never rewritten (A-20).

### R-10 — Registry and vocabulary are deferred, not dropped

This stage edits neither `.specify/features.md` / `.specify/features/111-*.md` nor `.specify/glossary.md`. The registry row and the `Draft → Planned` advance belong to the later feature-registration stage (FR-009's sole exception); the glossary candidates remain frozen proposal text whose registration needs an FR-009 revision first (A-21). The deviation from create-plan's Feature Integration is disclosed in `feature-ref.md` and the stage record.

## Re-measure list for `/speckit.tasks` / `/speckit.implement`

1. Source residue lines (M2) — confirm the manifest still has exactly the two adaptation points before porting; a third residue line changes the FR-008 edit list.
2. `sync-mirrors.py --check` (M5) — re-take the "no NEW drift" baseline immediately before the write-mode regeneration.
3. `feedback-utils.py --help` action set and `knowledge-promotion.md` presence (M3) — the guard's leg (d) asserts both; re-read before writing the guard.
4. `/usr/local/bin/python3` pytest availability (M7) — required by the runner on this host.
5. Framework-map sibling row style (M6) — re-read the adjacent `.specify/shared/` rows before writing the registration row.
6. Baseline commit and run id (M9, FR-009) — re-check `git cat-file -e 0419adae5` and the spine's run id before the containment reading.