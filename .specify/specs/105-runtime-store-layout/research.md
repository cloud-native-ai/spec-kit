# Phase 0 Research — Runtime Store Layout

**Spec**: `requirements.md` · **Date**: 2026-11-25 · **Baseline commit**: `23938f22e`（requirements 实测基线）/ `0cde03ef9`（本阶段起点）
**Method**: every reading below was measured on this worktree on 2026-11-25 and captured under `test-evidence/`; nothing is inherited from prose. Where a reading is a count, the command that produced it is named and its full output was kept.

> Summary-first note: this file is the Phase 0 record other artifacts cite. It intentionally restates measured numbers (a dated record, legitimate duplicate), while the *normative* rules live in `contracts/` and are referenced, not copied.

## R-1 Runtime inventory baseline

| Reading | Command | Result |
|---|---|---|
| Baseline children of `.specify/memory/` | `git ls-tree -d 23938f22e:.specify/memory` | 12: `coaching evidence exec-quant feedback housekeeping knowledge renumber retention session todo tools trigger` |
| Baseline top-level files | `git ls-tree 23938f22e:.specify/memory \| grep -v tree` | none |
| Tracked paths | `git ls-files .specify/memory \| wc -l` | 2,971 |
| Files on disk | `find .specify/memory -type f \| wc -l` | 2,973 (two ignored `.write.lock` files) |
| Size | `du -sh .specify/memory` | 18 M |
| Per-store tracked counts | `git ls-files .specify/memory \| awk -F/ '{print $3}' \| sort \| uniq -c` | exec-quant 1630 · feedback 568 · session 526 · evidence 146 · retention 45 · coaching 26 · tools 10 · knowledge 10 · renumber 4 · todo 3 · housekeeping 2 · trigger 1 |
| Engine-on-demand stores absent in this tree | `ls .specify/memory/{sanitize,migrate,draft}` | all absent — they are engine-created or legacy-only, which matches requirements § Store Inventory rows 9/14/15 |
| Legacy non-store | `ls .specify/memory/git-workflow.md` | absent; requirements row 16 remains a classification, not a current file |
| Ignored runtime files | `git status --short --ignored .specify/memory` | `exec-quant/.write.lock`, `exec-quant/aggregated/.write.lock` |
| `sanitize/` ignore | `git check-ignore -v .specify/memory/sanitize/findings.json` | `.specify/.gitignore:23:memory/sanitize/` |
| telemetry ignore | `git check-ignore -v .specify/memory/trigger/telemetry.jsonl` | `.specify/.gitignore:27:memory/trigger/telemetry.jsonl` |
| `tools/` ignore | `git check-ignore -v .specify/tools/system.json` | `.specify/.gitignore:16:tools/` |

Consequences recorded:

1. The closed inventory is the 12 baseline children + the engine-declared `sanitize/`, `migrate/receipts/` + legacy `draft/` + non-store `git-workflow.md` + the container itself. No other member exists at baseline.
2. `exec-quant` is 55 % of tracked paths; any design that byte-copies stores before moving would add ~18 M / 2.9 k files to the archive. This bears on `contracts/migrate-store-layout.md` M-4 (manifest-first relocation, the 097 `relocate` precedent).
3. `.write.lock` is the only ignored entry inside a live store today; it must be classified as non-content in the migration predicate.

## R-2 Live-reference inventory (measured)

Search key: the retired-root literal `.specify/memory/` plus the bare container literal `.specify/memory` (not followed by a path segment). Counts are occurrences per file.

### R-2.1 Framework-source class (`templates/ skills/ shared/ scripts/ src/`)

`src/`:

| File | Count | Nature |
|---|---|---|
| `src/specify_cli/__init__.py` | 3 | migration receipt path; installer core-asset list; placeholder-seed lookup (plus package `memory/` copy code using joined path parts, R-4) |

`scripts/`:

| File | Count | Nature |
|---|---|---|
| `scripts/python/sanitize-utils.py` | 8 | store paths, legacy-residue constants, material roots, self-exempt prefix |
| `scripts/python/renumber-utils.py` | 4 | store root, memory literal, machine-prefix exemptions |
| `scripts/python/seal-utils.py` | 3 | archive dated trees / dirty paths / scan file set |
| `scripts/python/memory-utils.py` | 3 | `MEMORY_SUBDIR` and layout docstring |
| `scripts/bash/create-new-tools.sh` | 3 | tool-record path, canonical id |
| `scripts/python/trigger-utils.py` | 2 | store path, ignore entry |
| `scripts/python/feedback-utils.py` | 2 | store path, exec-quant payload path |
| `scripts/python/evidence-utils.py` | 2 | evidence store, feedback lane |
| `scripts/python/anchor-layout-migrate.py` | 2 | legacy anchor layout (migration engine) |
| `scripts/python/tools-utils.py` | 1 | canonical layout doc + workspace resolution comment |
| `scripts/python/skills-utils.py` | 1 | tool resource-id prefix |
| `scripts/python/run-determination.py` | 1 | persistence-adapter docstring |
| `scripts/python/exec-quant.py` | 1 | `STORAGE_REL` |
| `scripts/python/concurrency-check.py` | 1 | fourth-source surface list |
| `scripts/python/probe-utils.py` | — | bare `"memory"` join (feedback store); not caught by the literal grep |
| `scripts/python/record-retention.py` | — | bare `"memory"` join (retention store) |
| `scripts/python/role-edge-check.py` | — | `<state-dir>/../memory/exec-quant/records` composition |
| `scripts/python/non-disposable-check.py` | — | regex `.specify/(memory/)?features/` legacy tolerance |

`skills/` (38 files, counts as measured; all are live instructions):

```
sanitize-materials/SKILL.md 13 · summarize-project/references/consistency-rules.md 6
manage-feedback/references/path-a-digest.md 6 · manage-todo/SKILL.md 5 · improve-tools/SKILL.md 5
manage-feedback/SKILL.md 4 · create-tools/SKILL.md 4 · coaching-skills/references/prompt-templates.md 4
manage-feedback/references/path-b-and-probe.md 3 · sdd-project-setup/references/setup-recipes.md 3
sdd-house-keeping/SKILL.md 3 · git-utils/SKILL.md 3 · study-kb/SKILL.md 2 · memory-record/SKILL.md 2
memory-recall/SKILL.md 2 · manage-instructions/SKILL.md 2 · manage-history/SKILL.md 2
collect-evidence/references/evidence-contract.md 2 · sdd-house-keeping/references/maintenance-recipes.md 2
git-utils/references/{instructions-lookup,bootstrap-commands}.md 2 each · draw-diagram/SKILL.md 2
run-interview, improve-agent, create-team, create-plan, create-agent, collect-evidence, code-review,
code-review/scripts/git-delta-review.sh, improve-skills, improve-docs, git-utils/references/{troubleshooting,
health-check-commands}, draw-diagram/references/routing-matrix, create-docs, coaching-skills/SKILL.md,
coaching-skills/data-model.md 1 each
```

Additional source-form (un-prefixed) references that `rewrite_paths` currently normalizes — they MUST be rewritten as part of this feature, not left to the installer:

- `skills/external/sdd-house-keeping/scripts/mechanism-inventory.py` and `skills/external/sdd-project-setup/scripts/mechanism-inventory.py`: `memory/feedback`, `memory/knowledge`, `memory/session` directory probes (FR-018 names these explicitly).
- `shared/workflow/target-resolution.md`: `.specify/` detection accepts `memory/`; after retirement the probe must accept the new stores.
- `skills/internal/debt-audit/SKILL.md`: `memory/knowledge`, `memory/history` read scopes.
- `skills/internal/sanitize-materials/SKILL.md`: legacy layout lane (`memory/features/<NNN>.md`).
- `shared/patterns/self-improvement-pattern.md`: "memory/history" shorthand.

`templates/` (13 files: 11 command/instruction/tool pages + the 2 ignore templates):

```
commands/tools.md 5 · instructions-template.md 4 · tools.md 3 · commands/todo.md 3 · commands/sanitize.md 3
commands/{review,migrate,interview,instructions,improve,feedback}.md 1 each
```

`agents/`:

| File | Count | Nature |
|---|---|---|
| `agents/sdd-debt-governor.agent.md` | 1 | read scope names the memory roots |

Per-tool command copies (`.github/prompts/`, `.claude/commands/`, `.qoder/commands/`, `.opencode/command/`): 36 files carry the literal; all are regenerated from `templates/commands/` by `regen-command-copies.py` and are never hand-edited.

`shared/` (22 files):

```
definitions/tool-definitions.md 5 · workflow/feedback-step.md 4 · patterns/interview-pattern.md 2
definitions/non-disposable-definitions.md 2 · workflow/{tool-reuse-gate,runtime-mode,evidence-step,
artifact-commit-step,agent-configuration,acceptance-hardening}.md 1 each · guidelines/{todo-in-context,
reporting-obligations,critique-and-self-critique,confirmation-gates}.md 1 each · definitions/{subagent-
definitions,self-explanatory-definitions,probe-definitions,derivation-definitions,framework-map}.md 1 each
declarations/facts/{memory-types,non-disposable-review-surface}.yaml 1 each · declarations/exclusions/no-machine-fact.yaml 1
```

### R-2.2 Runtime-guide class

| File | Count | Note |
|---|---|---|
| `.specify/instructions.md` | 5 | feedback docs row; in-package `memory/` note; tool record paths ×3; framework-map highlight |
| `.specify/glossary.md` | 7 entries | `Memory Layer`, `Session(消歧)`, `三捕获机制`, `自省报告`, `Evaluation Form`, `Renumber Lane`, `Coaching Run` |

### R-2.3 Current-docs class (`docs/**` minus dated classes)

| File | Count |
|---|---|
| `docs/reference/commands/sanitize.md` | 7 |
| `docs/reference/commands/feedback.md` | 5 |
| `docs/reference/commands/tools.md` | 4 |
| `docs/reference/skills/memory.md` | 3 |
| `docs/reference/skills/feedback.md` | 3 |
| `docs/reference/commands/migrate.md` | 3 |
| `docs/concepts/spec-driven.md` | 3（两条 already stale: feature registry claimed under memory） |
| `docs/reference/skills/sdd-house-keeping.md` | 2 |
| `docs/reference/commands/todo.md` | 2 |
| `docs/tutorials/installation.md` | 1 |
| `docs/reference/commands/{session,interview,instructions,improve,derive}.md` | 1 each |
| `docs/reference/cli/supported-agent-tools.md` | 1 |
| `docs/reference/agents/command-and-skills.md` | 1 |
| `docs/concepts/{overview,todo-in-context}.md` | 1 each |

Dated candidates measured but **not** rewritten (see R-9): `docs/reference/history/**` (2 files), `docs/decisions/**` (2 files), `docs/archive/03-sdd-workflow-refactor-proposal.md`, `docs/static/reports/081-acceptance-hardening-final.html`, `docs/notes/dot-specify-mechanism-reconciliation.md`.

### R-2.4 Ignore templates

`templates/gitignore-specify-template` and its live copy `.specify/.gitignore` carry `tools/`, `memory/sanitize/`, `memory/trigger/telemetry.jsonl`; `templates/claudeignore-template` and `templates/codexignore-template` carry the release line `!.specify/memory/`. All are byte-identical copies today (measured by `diff -q`).

### R-2.5 Tests

`grep -rl '\.specify/memory' tests/` → **89 files**. Top carriers: `test_record_retention_engine.py` 17, `test_test_entry_guard.py` 9, `test_no_organize_agents_refs.py` 9, `test_workspace_isolation_contract.py` 6, `test_sanitize_engine_contract.py` 6, `test_feedback_introspection_engine.py` 6, `test_feedback_entry_schema.py` 6, `test_memory_utils.py` 5, `test_tools_inventory_ownership.py` 5. Three of these also contain **already-stale anchors** (`.specify/memory/glossary.md`, `.specify/memory/features.md`) that must be repaired to today's real locations while touching them — this is a correction inside the migration surface, not a new decision (constitution VIII: code/tree is truth).

Test classification for the migration (normative rule in `contracts/live-reference-migration.md` L-3):

1. **Live-target** — the test exercises an engine/store that moves: rewrite to the new root.
2. **Legacy-fixture** — the test constructs a pre-migration workspace on purpose (migrate-097 builders, anchor-layout legacy fixtures, sanitize legacy-residue, upgrade-end-state): keep old literals, confined to an explicit allowlist.
3. **Stale** — the literal names a path that is already wrong today (e.g. `.specify/memory/glossary.md`): repair to the current authoritative path.

## R-3 `specify migrate` anatomy (the transition vehicle)

Measured in `src/specify_cli/__init__.py`:

- `MIGRATE_DIMENSIONS` (line 2830) is the closed five-token tuple `templates-generated, anchor-layout, compat-links, mirror-consistency, migration-residue`; `MigrateItem` validates its `dimension` against it; receipts and the summary iterate it in order.
- `MIGRATE_DISPOSITIONS` is the six-value domain `converged, write, replace, archive, refuse, blocked`; `MIGRATE_MECHANISMS` is `copy, replace, archive, relocate, symlink, anchor-engine, mirror-engine, none`.
- The executor implements `write / replace / archive / relocate / anchor / mirror` mechanisms. `_migrate_execute_relocate` performs `shutil.move` (atomic rename on one filesystem), records `archiveTo = <target>` plus a digest, and appends a `{path, archiveTo, change: "relocated", digest}` archive entry — **no byte copy**. This is the existing, reviewed interpretation of "archive-first for relocation" (097 review r2 accepted it).
- Receipts: one JSON per run at `migrate_receipts_dir()` = `.specify/memory/migrate/receipts/<run-id>.json`, created with `O_EXCL`, `status=running` at apply start, completed at the end; `load_migrate_resume_state` scans receipts and resumes from the *receipt's own recorded* items.
- Outcomes/exit codes: clean 0 / planned 1 / applied 0 / blocked 3 / input error 2.
- Dimension pins that constrain an extension: `tests/contract/test_migrate_engine_contract.py::test_dimension_tokens_and_order_come_from_data_model_e8` and `tests/unit/test_migrate_planner.py::test_dimension_tokens_and_order_come_from_data_model_e8` compare the code tuple **exactly** against 097's `data-model.md` E-8. 097 contract C-1 declares the dimension set closed and says an extension requires revising requirements.
- The current dry-run on this repo (`test-evidence/plan-migrate-dryrun.json`) returns `outcome=planned`, 450 items — **all** `replace` from the pre-existing mirror drift (R-6); zero store items because the layout is still old. This verifies both the command form and the five dimensions' operation before any edit.

Design consequence: the store relocation is a **sixth dimension `store-layout`**, ordered last, reusing the item/executor/receipt machinery. The two 097 dimension-pin tests must be re-pointed to a prefix-preserving guard (the five original tokens remain, in order, as the prefix) with 105's contract as the live extension owner; 097's dated E-8 is not rewritten. Recorded as Decision Tension T-001 in `plan.md`.

## R-4 Installer / refresh anatomy

| Site | Reading | Effect |
|---|---|---|
| Package seed | `memory/` in the source/wheel: `constitution.md`, `features.md`, `session/.gitkeep`, `knowledge/.gitkeep`; `pyproject.toml` force-includes `memory` → `specify_cli/memory` | init copies anchors → `.specify/`, subdirs → `.specify/memory/session|knowledge`; it also creates `.specify/memory/` itself |
| `copy_local_templates` (≈2403–2467) | creates `.specify/memory/`; special-cases the two anchors; copies each seed subdir under memory; skip-and-defers when a legacy anchor exists under memory | must seed `.specify/session/` + `.specify/knowledge/`, never create `.specify/memory`; skip-and-defer for legacy anchors stays but its message must point at `specify migrate` without naming the retired root as a live location (tombstone wording allowed) |
| `migrate_placeholder_dir()` (≈3495) | `resource/memory` used to recognise placeholder anchors | re-point to the seed dir |
| `_CORE_SPECIFY_ASSETS` (line 1157) | includes `.specify/memory` | replace with the two seeded memory tiers |
| `rewrite_paths()` (line 1574) | anchor specials `memory/{constitution,features,glossary,register,tools}.md`, `memory/features/`, and a generic `memory` segment | anchor specials were for the 2026-11-10 anchor move; the generic `memory` segment is now a retired-root literal. Remove all; source files will carry runtime-form `.specify/<store>/` paths |
| `features_dir` (≈5324) | creates `.specify/features` (comment wrongly says "under .specify/memory") | comment repair only |
| `generate-instructions.sh` | appends `.specify/tools/*.json` to the **repo-root** `.gitignore` | unchanged behavior (still correct for the tools split); the framework-owned `.specify/.gitignore` narrows its own `tools/` rule |
| Shared asset packaging | `shared/` force-included in the wheel | a declaration fact placed under `shared/declarations/facts/` is available to the installed CLI and to clients |

Design consequence: rename the package seed root `memory/` → `seed/` (grounded in the requirements' own "种子布局" vocabulary), carrying the two anchors + two tier directories. This removes `memory` as any directory name in the shipped asset tree and makes FR-017 mechanical. Recorded as Decision Tension T-002.

## R-5 Ignore surfaces

- Framework owner: `templates/gitignore-specify-template` → installed `.specify/.gitignore`; measured byte-identical.
- Required changes: `tools/` → `tools/*.json`（记录 `tools/*.md` 受跟踪）; `memory/sanitize/` → `sanitize/`; `memory/trigger/telemetry.jsonl` → `trigger/telemetry.jsonl`; comment "canonical definitions live in memory/tools/" → `.specify/tools/`.
- `templates/{claude,codex}ignore-template`: `!.specify/memory/` must be replaced by release lines for the new top-level stores (the previous line released everything that lived under memory; the new set is the union of the 14 store roots). The `.github/copilot` ignore surface, if any, is generated elsewhere; measured only the two templates above carry the release line.
- The repo-root `.gitignore` already carries `.specify/tools/*.json` (generated by `generate-instructions.sh` line 119); no root-level store rule exists or is needed.

## R-6 Mirror surfaces and the measured baseline drift

- `sync-mirrors.py MIRROR_PAIRS`: `templates/`, `skills/external`, `skills/internal`, `agents`, `scripts` (strict extras), `shared`.
- Baseline measured **before any edit** (typer-capable interpreter `/usr/local/bin/python3`): `sync-mirrors.py --check` → rc 2, **450 DIFF** (templates 0, skills 262, shared 103, scripts 65 = 59 plain + 6 projected, agents 20), 0 MISS, 0 ORPHAN. The differences are the `.specify/`-prefixed runtime form already present in the mirrors versus the source-form sources; `--write` copies source bytes and therefore converges them. Full output kept at `test-evidence/sync-mirrors-baseline.txt`. Running the same check with the profile `python3` additionally fails the regen subprocess for lack of `typer`; that is an interpreter fact, not a tree fact.
- `regen-command-copies.py --check` → rc 0 (`OK: all per-tool command copies match the source templates`) when run with a typer-capable interpreter.
- Project lesson `docs/reference/history/00-cross-cutting-lessons.md` line 154 is authoritative here: pre-existing drift means the criterion MUST be "no NEW drift members on the touched surface", never a count equality; syncing a scope may cure unrelated drift.
- Consequence for SC-007: the absolute "both checks rc 0" reading is not achievable at baseline without converging the 450 members. The plan adopts the measured reading — the feature's mirror WP converges the touched scopes and records the resulting member-set delta; the absolute rc-0 goal is reported honestly against the baseline. Recorded as Decision Tension T-003.

## R-7 Memory system and injection surfaces

- `memory-utils.py`: `MEMORY_SUBDIR = .specify/memory`; `scope_dir()` = `memory_root()/scope`; the scope set comes from `shared/declarations/facts/memory-types.yaml` (`session`, `knowledge`) and is not renamed. Entry format, index-as-derived, prune/reindex semantics are independent of the root.
- `run-determination.py`: persists through `memory-utils.py` (`OI2_PERSISTENCE_ADAPTER = "memory-utils-session"`), reads the same index for `--action history`; the only literal is a docstring. No schema change needed.
- `memory-record` / `memory-recall`: engine-relative invocations, store paths named in description + References sections.
- Dispatch contract: `shared/definitions/subagent-definitions.md` owns the seven-field downlink, four injections and five-element uplink; its only memory literal is the Tool-record row (line 201). `memory-recall` is a declared retrieval source. Nothing in the contract names a store root beyond that; the change is confined to source paths.
- `run-role-edge` / `role-edge-check.py` reads exec-quant records under a sibling `memory/` path — a live path composition, updated.
- Boundary evidence available: memory recall scans only the two scopes; `evidence-utils.py` feedback lane and `probe-utils.py` read the feedback store directly. That separation makes the FR-008 reverse fixture (runtime-store text not recalled as memory) mechanically assertable.

## R-8 Tools domain (A-5)

- Current split: definitions at `.specify/memory/tools/*.md` (10 records, tracked); generated inventories at `.specify/tools/{system,shell,project}.json` (absent in this tree; root `.gitignore` ignores them).
- Live consumers of the record path: `tools-utils.py` (canonical layout + workspace-root resolver), `skills-utils.py` (tool resource id prefix `<TOOL:.specify/memory/tools/...>`), `create-new-tools.sh`, `templates/tools.md`, `templates/commands/tools.md`, `shared/definitions/tool-definitions.md`, `shared/workflow/tool-reuse-gate.md`, `templates/instructions-template.md`, `docs/reference/{commands/tools,cli/supported-agent-tools}.md`, plus the `create-tools` / `improve-tools` skills.
- The sanitize legacy check `legacy-tools-registry` currently flags `.specify/tools` as obsolete when `.specify/memory/tools` exists — **the inverse of the target semantics**. It must be removed (its repair pointer becomes wrong), and the `MATERIAL_ROOTS` entry renamed from a legacy registry to the tools domain.
- `.specify/tools.md` is the guide file at the `.specify/` root; it is not a directory and does not collide.

## R-9 Cross-store consumers and the dated-record boundary

Files that hardcode a *set* of runtime roots (not one store):

| Consumer | Current set | Target |
|---|---|---|
| `sanitize-utils.py` `MATERIAL_ROOTS` / `SELF_EXEMPT_PREFIX` / reference-material scan | memory/todo, memory/draft, memory/*.md, memory/sanitize, memory/renumber | new roots; legacy old-root entries stay only in the residue scanner |
| `renumber-utils.py` `EXCLUDED_PREFIXES` / `MACHINE_PREFIXES` | memory/sanitize, memory/retention, memory/renumber | sanitize, retention, renumber |
| `seal-utils.py` `ARCHIVE_DATED_TREES` / dirty paths / scan files | `.specify/memory/`, `.specify/history/` | the new runtime store roots + `.specify/history` |
| `concurrency-check.py` `FOURTH_SOURCE_SURFACES` | `.specify/memory` | the new runtime guides/stores |
| `non-disposable-review-surface.yaml` | 11 roots incl. `.specify/memory` | replace memory with the store roots (its own fact; guarded against the store declaration) |
| `non-disposable-definitions.md` | tree list + `MACHINE_PREFIXES` | same |
| `probe-utils.py`, `record-retention.py`, `role-edge-check.py`, `evidence-utils.py`, `feedback-utils.py` | one store each | new root |

Because these surfaces hold a *set*, a single machine-readable declaration is the only non-drifting owner: `shared/declarations/facts/runtime-store-layout.yaml` (kind `mapping`), read through `declaration_reader.py` by the six enumerating consumers (sanitize, renumber, seal, concurrency-check, migrate, init); the non-disposable review surface keeps its own closed-set fact and is guarded for membership equality instead of reading the declaration. A consumer that cannot read the declaration degrades with the reader's `owner-unavailable` label, never silently. The declaration holds store names + lifecycle + owner + non-content predicates; paths are projections (`.specify/<name>`, legacy `.specify/memory/<name>`) so the layout stays a fact, not a literal list. The framework map remains the human map and is guarded against the same declaration.

Dated-record boundary measured:

- Explicitly excluded by SC-006: `docs/reference/history/**`, `docs/decisions/**`.
- `docs/archive/03-sdd-workflow-refactor-proposal.md`（归档提议）, `docs/static/reports/081-acceptance-hardening-final.html`（冻结验收报告）, and `docs/notes/dot-specify-mechanism-reconciliation.md`（frontmatter `created: 2026-10-11, status: draft`，对账快照）are dated artifacts by the documentation model (`docs/concepts/documentation-model.md`: formal dirs are append/archive-only, `notes/` is flow-through with a lifecycle). They are **not rewritten**; the SC-006 guard declares them as the dated-record class extension. Recorded as Decision Tension T-004. All other live docs are rewritten.

## R-10 Test posture and environment facts

- Test entry is `scripts/bash/run-tests.sh`; it resolves an interpreter via `SPECKIT_PYTHON` → `repo/.venv/bin/python` → `python3` → `python`.
- This environment: `.venv/bin/python` has `typer 0.29.2` but **no pytest**; `python3` resolves to a profile venv with neither; `/usr/local/bin/python3` has `pytest 8.4.2` + `typer 0.19.2`. Evidence runs therefore use `SPECKIT_PYTHON=/usr/local/bin/python3`. This is an environment fact, not a framework defect; recorded in `Execution Premises` EP-006.
- Baseline proof the entry works (full output in `test-evidence/plan-baseline-memory-tests.txt`): `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_memory_utils.py -q` → `15 passed in 6.48s`, rc 0, mode=parallel.
- `regen-command-copies.py --check` needs a typer-capable interpreter; run with `/usr/local/bin/python3` → rc 0.
- The full-suite name-level baseline is a `/speckit.implement` duty (one expensive run, captured in full per the single-run evidence discipline); this plan defines it as the comparison reference, not as a plan-stage measurement.

## R-11 `specify migrate` pre-edit dry-run (measured)

Command (verified working form; the package has no `__main__`, so the entry is the console function):

```bash
PYTHONPATH=src /usr/local/bin/python3 -c "from specify_cli import main; main()" migrate --workspace . --format json
```

Reading on 2026-11-25 (full payload `test-evidence/plan-migrate-dryrun.json`): rc 1, `outcome=planned`, `workspaceKind=framework-source`, `summary.total=450`, `byDimension={templates-generated:282, anchor-layout:0, compat-links:0, mirror-consistency:168, migration-residue:0}`, `byDisposition={replace:450}`; one static pointer; dry-run left the tree untouched (`git status` unchanged apart from this spec's new files). This confirms (a) the command form the quickstart will cite, (b) the mirror drift is the only pre-existing plan content, and (c) zero store-layout items exist before the feature.

## R-12 Unresolved questions and how they are settled

| Question | Settlement | Where |
|---|---|---|
| How to extend a closed dimension set owned by a dated record? | Sixth dimension `store-layout`, last; 097's five stay as an ordered prefix; live pin re-pointed; dated E-8 untouched | T-001, M-1 |
| Keep or rename the package seed directory `memory/`? | Rename to `seed/` (grounded in "种子布局") | T-002, C-7 |
| How to satisfy SC-007 when 450 pre-existing mirror diffs exist? | Measured-relative reading; converge touched scopes; report member-set delta and absolute state honestly | T-003, L-6 |
| Are `docs/archive|static|notes` rewrite targets? | No — dated artifacts; guard class extension with basis | T-004, L-4 |
| Byte-copy archive vs recorded move for 2,971 files? | Recorded move (097 `relocate` precedent): pre-move manifest + digest + from→to + recover; no byte duplication | T-005, M-4 |
| Per-consumer store lists vs one declaration? | One `runtime-store-layout` mapping fact + reader; consumers degrade explicitly | T-006, C-6 |

## R-13 Files this research touched

Read-only: all files named above; no product file was edited. Created: this file and `test-evidence/plan-migrate-dryrun.json`, `plan-baseline-memory-tests.txt`, `plan-baseline-migrate-tests.txt`, `sync-mirrors-baseline.txt`, `plan-gates.txt`, `plan-workspace-status.txt`, `pre-analyze-plan.json`. Workspace guard: `git status --short` shows only this spec's new files plus the plan-stage feature-registry updates (see `test-evidence/plan-workspace-status.txt`).
