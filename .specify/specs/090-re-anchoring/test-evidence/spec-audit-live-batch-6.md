# Spec audit — live batch 6 (7 specs)

- **Date**: 2026-11-10
- **Tree audited**: `/storage/project/cloud-native-ai/spec-kit` (MAIN working tree, read-only). No spec or source file was modified by this audit; the only write is this findings file. No test suite was executed (the audit is static: filesystem existence checks, file reads, `grep`/`cmp`/`git` reads).
- **Tree movement during the audit**: the audit began at `564a5f5a6`; while it ran, master advanced to `6fb8093c4` (`merge(layout): move the project anchors out of memory/`), then to `cff62e51e` (concurrency pointer on 111 SKILL.md files; no referenced path was created or deleted). The anchor rename announced as *pending* in the audit instruction **landed mid-audit**. Counts below are the **end state after `6fb8093c4`**; the `cff62e51e` follow-up only shifted line numbers inside a few skill bodies (re-measured for the citations below) and does not change any path classification. References that were alive at start and are now dead solely because of the rename merge are marked **moved** and reported separately from spec-owned defects.
- **Specs audited**: `016-refactor-tools-command`, `032-dogfooding-practice`, `044-reduce-confirmation-flows`, `058-sdd-loop-driver`, `070-subagent-task-teams`, `080-humanize-run-output`, `093-concurrency-by-default`.

## Method

**Artifact set counted**: `requirements.md`, `plan.md`, `tasks.md`, `data-model.md`, `quickstart.md`, `verification.md`, `research.md`, `feature-ref.md`, `contracts/*`, `notes/*`. `checklists/`, `review.md`, `baseline-failed.txt`, `baseline.json`, `baseline-gates.md` and `test-evidence/` were scanned supplementarily but are excluded from the counted census (several are dated baselines or evidence records, not live pointers).

**Extraction**: every token beginning `.specify/`, `scripts/`, `skills/`, `templates/`, `shared/`, `tests/`, `src/` or `docs/` was extracted with its file:line anchor, stripped of line suffixes and fragments, and de-duplicated per spec. Generic placeholders (`<ID>`, `<slug>`, `*`) were resolved against their parent directory.

**Classification**:

- **alive** — the target path exists in the current tree.
- **archived-elsewhere** — the target is absent but the same artifact exists under `.specify/archive/`.
- **dead** — no target exists; a pointer at a pre-consolidation path counts as dead.
- **moved** — a dead reference whose only cause is the anchor rename (`memory/` → `.specify/` root). Counted in `dead`, reported separately, and **not sufficient by itself** to make a spec BROKEN (the rename was declared in advance and is the subject of spec 090).
- **illustrative** — scenario/example paths (quickstart examples, fixture write domains, generic `test_x.py`). Listed for completeness; not spec-owned breakage.
- **prose false positive** — a path-like string in running text (e.g. “在 tests/scripts/templates 零既有断言”). Excluded from the census.

**Verdict rule**: **BROKEN** iff at least one spec-owned broken item exists — a dead non-rename pointer, a named guard file missing, a named guard that now reads a dead anchor, or a registry defect. **INTACT** otherwise; rename-moved references are flagged but do not flip the verdict.

## Batch summary

| Spec | refs | alive | archived | dead | verdict |
|---|---:|---:|---:|---:|---|
| 016-refactor-tools-command | 29 | 20 | 0 | 9 (3 moved) | **BROKEN** |
| 032-dogfooding-practice | 22 | 18 | 0 | 4 (3 moved) | **BROKEN** |
| 044-reduce-confirmation-flows | 58 | 51 | 0 | 7 (3 moved) | **BROKEN** |
| 058-sdd-loop-driver | 54 | 48 | 0 | 6 (3 moved) | **BROKEN** |
| 070-subagent-task-teams | 84 | 81 | 0 | 3 (3 moved) | **INTACT** |
| 080-humanize-run-output | 134 | 109 | 1 | 24 (4 moved) | **BROKEN** |
| 093-concurrency-by-default | 319 | 272 | 0 | 47 (9 moved) | **BROKEN** |
| **Batch total** | **700** | **599** | **1** | **100 (28 moved)** | 6 BROKEN / 1 INTACT |

Note: spec number ≠ Feature ID for three specs — spec `032-dogfooding-practice` is Feature **036**, spec `044-reduce-confirmation-flows` is Feature **046**, spec `080-humanize-run-output` is Feature **062**. The registry checks below use the row whose **Spec Path** cell names the spec, not the row number.

---

## 016-refactor-tools-command

### Census

**29 distinct references → 20 alive / 0 archived / 9 dead** (3 moved, 3 missing named guards, 3 illustrative quickstart examples).

### Broken list

Moved by the anchor rename (target exists under the new root):

- `.specify/specs/016-refactor-tools-command/plan.md:26` → `.specify/memory/constitution.md` missing; now `.specify/constitution.md`
- `.specify/specs/016-refactor-tools-command/tasks.md:5` → `.specify/memory/features.md` missing; now `.specify/features.md`
- `.specify/specs/016-refactor-tools-command/tasks.md:158` → `.specify/memory/features/016.md` missing; now `.specify/features/016-refactor-tools-command.md`

Named guards that do not exist (tasks are checked `[X]`):

- `.specify/specs/016-refactor-tools-command/tasks.md:65,205` → `tests/contract/test_tools_discover_draft.py` missing. Coverage survives: `tests/contract/test_tools_define.py` header states it carries T015 (`DiscoveryDraft.to_record()`).
- `.specify/specs/016-refactor-tools-command/tasks.md:89` → `tests/contract/test_tools_modify.py` missing. Coverage survives: `tests/contract/test_tools_view.py` header states it carries T023/T035/T036.
- `.specify/specs/016-refactor-tools-command/tasks.md:110` → `tests/contract/test_tools_preview.py` missing; **no successor**. `grep` finds no test asserting `resolved_command`, `resolved_parameters`, `expected_output_shape` or `confirmation_prompt`; only the template-wording test `tests/contract/test_tools_command_routing.py:62` covers the preview→confirm→execute gate. This is a genuine coverage gap for T028.

Illustrative quickstart paths (not breakage; the quickstart's Scenario 1/3 deliberately creates them):

- `.specify/specs/016-refactor-tools-command/quickstart.md:13,17,61` → `scripts/bash/build-docs.sh` absent (the user-supplied example source, never a repository file)
- `.specify/specs/016-refactor-tools-command/quickstart.md:22,26` → `.specify/memory/tools/build-docs.md` absent (Scenario 1 expected output)
- `.specify/specs/016-refactor-tools-command/quickstart.md:41,54` → `.specify/memory/tools/jq.md` absent (Scenario 3 expected output). The live tools directory is `.specify/memory/tools/` and contains ten real records (e.g. `feedback-utils.py.md`), but neither example record.

### Guards

| Named guard | Status |
|---|---|
| `tests/contract/test_tools_define.py` | present (13 tests) |
| `tests/contract/test_tools_view.py` | present (6 tests) |
| `tests/contract/test_tools_invoke.py` | present (3 tests) |
| `tests/integration/test_tools_definition_flow.py` | present |
| `tests/integration/test_tools_invoke_flow.py` | present |
| `tests/integration/test_tools_modify_flow.py` | present |
| `tests/contract/test_tools_discover_draft.py` | **missing** (coverage folded) |
| `tests/contract/test_tools_modify.py` | **missing** (coverage folded) |
| `tests/contract/test_tools_preview.py` | **missing, no successor** |

Adjacent guard broken by the rename (not named by this spec, but it guards the same command surface): `tests/contract/test_tools_command_routing.py:153` reads `.specify/memory/constitution.md` with `.read_text()` → `FileNotFoundError`; the live file is `.specify/constitution.md`.

### Registry

Row `016` at `.specify/features.md:25`: Status `Implemented`; Feature Details `.specify/features/016-refactor-tools-command.md` exists and is titled “Tools Command”; Spec Path `.specify/specs/016-refactor-tools-command/requirements.md` exists. **Resolves.**

### Three implementation claims — spot checks

1. **File claim** (`plan.md` structure / tasks T002–T004): `scripts/bash/create-new-tools.sh` and `scripts/bash/refresh-tools.sh` exist. `create-new-tools.sh` declares `--action find|create|list` (usage lines 105–123) and covers discovery-assisted creation (discovery handling from line 630); `refresh-tools.sh` lists system/shell/project tool sources. **Holds.**
2. **Symbol claim** (`data-model.md`, tasks T005+): `scripts/python/tools-utils.py` defines `ToolRecord` (:105), `DiscoveryDraft` (:174), `save_record` (:280) and `load_record` (:450); the `.specify/scripts/python/tools-utils.py` mirror is byte-identical (`cmp` clean). **Holds.**
3. **Behaviour claim** (`contracts/tools-command.openapi.yaml`, quickstart): `templates/commands/tools.md:37-41` routes `define | modify | view | list | invoke`, and `:82-92` documents the `preview → confirm → execute` gate; `tests/contract/test_tools_command_routing.py:62` asserts that wording. **Holds**, but the preview contract itself is not independently tested (see above).

### Verdict

**BROKEN.** Three tasks marked `[X]` name test files that do not exist; two were folded into surviving files, but `test_tools_preview.py` has no successor. Three live references were moved by the anchor rename. The tools implementation itself is present and the two named implementation scripts and symbols hold.

---

## 032-dogfooding-practice (Feature 036)

### Census

**22 distinct references → 18 alive / 0 archived / 4 dead** (3 moved, 1 stale documentation-layout path).

### Broken list

Moved by the anchor rename:

- `.specify/specs/032-dogfooding-practice/contracts/dogfooding-artifacts.md:9`
- `.specify/specs/032-dogfooding-practice/data-model.md:21`
- `.specify/specs/032-dogfooding-practice/plan.md:33`
- `.specify/specs/032-dogfooding-practice/plan.md:87`
- `.specify/specs/032-dogfooding-practice/tasks.md:35`
- `.specify/specs/032-dogfooding-practice/tasks.md:70`
  → `.specify/memory/constitution.md` missing; now `.specify/constitution.md`
- `.specify/specs/032-dogfooding-practice/tasks.md:5` → `.specify/memory/features.md` missing; now `.specify/features.md`
- `.specify/specs/032-dogfooding-practice/feature-ref.md:4` → `.specify/memory/features/036.md` missing; now `.specify/features/036-team-summary.md` (filename slug defect, see Registry)

Stale pointer (spec-owned):

- `.specify/specs/032-dogfooding-practice/plan.md:91` → `docs/skills/feedback.md` missing; the docs tree was restructured and the live page is `docs/reference/skills/feedback.md` (also referenced alive at `plan.md` elsewhere in the same map). The Feature 036 detail repeats the stale path at `.specify/features/036-team-summary.md:16,23`.

### Guards

| Named guard | Status |
|---|---|
| `tests/contract/test_dogfooding_practice.py` | present (21 tests) |

The guard was updated for the rename (`CONSTITUTION = ROOT / ".specify" / "constitution.md"` at `test_dogfooding_practice.py:17`) and still asserts Principle XI, the template summary+pointer, the one-source doc and the “no new machinery” invariant. **No missing guard.**

### Registry

Row `036` at `.specify/features.md:45`: Status `Ready for Review`; Feature Details `.specify/features/036-team-summary.md` exists and its body is titled “Feature Detail: Dogfooding Practice / Feature ID 036”; Spec Path `.specify/specs/032-dogfooding-practice/requirements.md` exists. **Resolves, with a slug defect**: the filename `036-team-summary` belongs to the unrelated spec `.specify/specs/036-team-summary/` (bound to Feature 027), not to Feature 036; the content is correct but the cell's slug is misleading. The paired row 027 has the same cross-wiring (`.specify/features/027-feedback-mechanism.md` contains Feature 027 Team Management), so this is a systematic detail-file naming problem, not a one-off.

### Three implementation claims — spot checks

1. **File claim** (`plan.md` delivery list): `.specify/constitution.md:255` carries `### XI. Dogfooding (Self-Application)`; `templates/instructions-template.md:191` carries `## Dogfooding Practice`, and the `.specify/templates/` mirror is byte-identical. **Holds.**
2. **Single-source claim** (`contracts/dogfooding-artifacts.md` C-2/C-4): `shared/guidelines/dogfooding.md` and `.specify/shared/guidelines/dogfooding.md` both exist; the template carries a summary+pointer, and the guard reads the same paths. **Holds.**
3. **Behaviour claim** (`tasks` T004/T011, SC-002/SC-004): the guard asserts C-1…C-7 including the no-new-machinery comparison; `verification.md` records all four SCs as `pass`. **Holds.**

### Verdict

**BROKEN** — narrowly. One spec-owned stale documentation path (`docs/skills/feedback.md`) plus three rename-moved references; the registry cell resolves but its file slug is wrong. The implementation, mirrors and the named guard are intact.

---

## 044-reduce-confirmation-flows (Feature 046)

### Census

**58 distinct references → 51 alive / 0 archived / 7 dead** (3 moved, 1 stale skill path, 3 stale guard names whose coverage was merged).

### Broken list

Moved by the anchor rename:

- `.specify/specs/044-reduce-confirmation-flows/plan.md:27` → `.specify/memory/constitution.md` missing; now `.specify/constitution.md`
- `.specify/specs/044-reduce-confirmation-flows/feature-ref.md:5`, `tasks.md:5` → `.specify/memory/features.md` missing; now `.specify/features.md`
- `.specify/specs/044-reduce-confirmation-flows/feature-ref.md:4` → `.specify/memory/features/046.md` missing; now `.specify/features/046-confirmation-gate-governance.md`

Stale skill pointer (spec-owned):

- `.specify/specs/044-reduce-confirmation-flows/contracts/confirmation-taxonomy-contract.md:35` → `skills/git-workflow` missing. The skill was merged into `skills/external/git-utils/`, and the current taxonomy document already names `skills/external/git-utils` at `shared/guidelines/confirmation-gates.md:35`.

Named guards that do not exist (all three merged, no coverage loss):

- `.specify/specs/044-reduce-confirmation-flows/tasks.md:55` → `tests/contract/test_confirmation_gates_taxonomy.py` missing; merged into `tests/contract/test_confirmation_gates_sweep.py` (“was test_confirmation_gates_taxonomy.py”, file header lines 8–10).
- `.specify/specs/044-reduce-confirmation-flows/tasks.md:76` → `tests/contract/test_confirmation_gates_team_flow.py` missing; merged into the same file (header line 13).
- `.specify/specs/044-reduce-confirmation-flows/tasks.md:127` → `tests/contract/test_confirmation_gates_execution_report.py` missing; merged into the same file (header line 11).

### Guards

| Named guard | Status |
|---|---|
| `tests/contract/test_scan_confirmation_gates.py` | present (7 tests) |
| `tests/contract/test_confirmation_gates_sweep.py` | present (20 tests; explicitly owns the three merged files' assertions) |
| `tests/contract/test_confirmation_gates_taxonomy.py` | **missing (merged)** |
| `tests/contract/test_confirmation_gates_team_flow.py` | **missing (merged)** |
| `tests/contract/test_confirmation_gates_execution_report.py` | **missing (merged)** |

No named guard reads an old anchor path.

### Registry

Row `046` at `.specify/features.md:55`: Status `Implemented`; Feature Details `.specify/features/046-confirmation-gate-governance.md` exists and is titled “Confirmation Gate Governance”; Spec Path `.specify/specs/044-reduce-confirmation-flows/requirements.md` exists. **Resolves.**

### Three implementation claims — spot checks

1. **File claim** (`plan.md` / contract C-1): `scripts/python/scan-confirmation-gates.py` and `.specify/scripts/python/scan-confirmation-gates.py` exist and are byte-identical; `shared/guidelines/confirmation-gates.md` and its `.specify/shared/` mirror are byte-identical. **Holds.**
2. **Symbol claim** (`contracts/gate-scanner-contract.md`): `scripts/python/scan-confirmation-gates.py:65` defines `BLOCKING_RE`, `:98` defines `classify()` with `governance_kept` / `destructive` / 「存疑从严」 branches. **Holds.**
3. **Behaviour claim** (`quickstart`, contract C-7): the scanner contract test drives the output schema, exclusions, deterministic classification, doubtful→destructive and exit code 2; `test_confirmation_gates_sweep.py` drives the real scanner and pins the protected keep list. **Holds.**

### Verdict

**BROKEN.** One stale skill path (`skills/git-workflow`) and three stale guard filenames; the guard coverage itself survives in `test_confirmation_gates_sweep.py`. The implementation, scanner and taxonomy mirrors are intact.

---

## 058-sdd-loop-driver

### Census

**56 extracted; 2 are prose false positives** (`templates/src/scripts` at `tasks.md:18`, `tests/scripts/templates` at `plan.md:116` — both are running-text lists, not paths). **54 path references → 48 alive / 0 archived / 6 dead** (3 moved, 3 stale `git-workspace` paths).

### Broken list

Moved by the anchor rename:

- `.specify/specs/058-sdd-loop-driver/plan.md:27` → `.specify/memory/constitution.md` missing; now `.specify/constitution.md`
- `.specify/specs/058-sdd-loop-driver/feature-ref.md:5` → `.specify/memory/features.md` missing; now `.specify/features.md`
- `.specify/specs/058-sdd-loop-driver/feature-ref.md:5` → `.specify/memory/features/058.md` missing; now `.specify/features/058-sdd-loop-driver.md`

Stale pre-merge skill pointers (spec-owned):

- `.specify/specs/058-sdd-loop-driver/plan.md:13` → `skills/external/git-workspace/SKILL.md` missing; `git-workspace` was merged into `git-utils` (`skills/external/git-utils/SKILL.md` states it merges the former four skills).
- `.specify/specs/058-sdd-loop-driver/quickstart.md:16` → `.specify/skills/git-workspace/SKILL.md` missing; now part of `.specify/skills/git-utils/`.
- `.specify/specs/058-sdd-loop-driver/quickstart.md:17` → `.specify/skills/git-workspace/scripts/git_fleet.py` missing; now part of `.specify/skills/git-utils/`.
  The quickstart block is a dated baseline (`DIFF … DRIFT detected`) captured before the merge; it is evidence, not a live instruction, but it no longer reproduces.

### Guards

| Named guard | Status |
|---|---|
| `tests/contract/test_sdd_loop_driver_skill.py` | present (C-1…C-13 + C-14…C-19; mirror comparisons) |
| `tests/contract/test_run_skills_wiring.py` | present |

No named guard reads an old anchor path. `skills/external/sdd-loop-driver/` and `.specify/skills/sdd-loop-driver/` are byte-identical (`diff -rq` clean).

### Registry

Row `058` at `.specify/features.md:66`: Status `Implemented`; Feature Details `.specify/features/058-sdd-loop-driver.md` exists and is titled “无人值守 SDD 循环驱动机制”; Spec Path `.specify/specs/058-sdd-loop-driver/requirements.md` exists. **Resolves.**

### Three implementation claims — spot checks

1. **File claim** (`plan.md` structure): `skills/external/sdd-loop-driver/` contains `SKILL.md`, `references/`, `templates/` and `scripts/`; the `.specify/skills/sdd-loop-driver/` mirror is identical. **Holds.**
2. **Symbol/command claim** (frontmatter + driver contract): `skills/external/sdd-loop-driver/SKILL.md:4` carries `skill_id: "<SKILL:.specify/skills/sdd-loop-driver/SKILL.md>"` and `classification: external`; the stage sequence and completion sentinels are owned by `shared/declarations/facts/driver-stage-sequence.yaml` and `driver-completion-sentinels.yaml`, both present. **Holds.**
3. **Behaviour claim** (`contracts/skill-structure.md` C-1…C-13, `contracts/distribution-and-docs.md` C-14…C-19): the guard file exists and asserts the clause set, mirror identity and roster wiring. **Holds.**

### Verdict

**BROKEN.** Three stale `git-workspace` pointers in a plan and a dated quickstart baseline; three live references were moved by the anchor rename. The skill, its mirror and both named guards are intact.

---

## 070-subagent-task-teams

### Census

**87 extracted; 3 are prose/illustrative** (`docs/skills` in “feedback docs/skills” at `notes/clarify-decisions.md:512`; `tests/design` meaning a design review round at `notes/analyze-repair.md:95`; `src/generated/` as a fixture write domain at `notes/red-first-evidence.md:177`). **84 path references → 81 alive / 0 archived / 3 dead** — all 3 moved by the anchor rename.

### Broken list

Moved by the anchor rename (no spec-owned dead pointer):

- `.specify/specs/070-subagent-task-teams/plan.md:31` → `.specify/memory/constitution.md` missing; now `.specify/constitution.md`
- `.specify/specs/070-subagent-task-teams/feature-ref.md:13`, `tasks.md:174` → `.specify/memory/features.md` missing; now `.specify/features.md`
- `.specify/specs/070-subagent-task-teams/feature-ref.md:14`, `tasks.md:174` → `.specify/memory/features/070.md` missing; now `.specify/features/070-subagent-task-teams.md`

No missing named guard, no dead implementation pointer, no failed spot check.

### Guards

| Named guard | Status |
|---|---|
| `tests/contract/test_sdd_loop_driver_wp_gate.py` | present (11 tests) |
| `tests/contract/test_sdd_loop_driver_wp_model.py` | present (25 tests) |
| `tests/contract/test_sdd_loop_driver_wp_preset.py` | present (14 tests) |
| `tests/contract/test_sdd_loop_driver_wp_coordination.py` | present (51 tests) |
| `tests/contract/test_sdd_loop_driver_gates.py` | present (7 tests) |
| `tests/contract/test_non_regression_070.py` | present (10 tests) |
| `tests/contract/test_wp_mutation_drills.py` | present (4 tests) |
| `tests/contract/test_clause_forms.py` | present (32 tests) |
| `tests/contract/test_execution_config_engine.py` | present (class-based; 0 `def test_` lines) |
| `tests/contract/test_lifecycle_detach_reattach.py` | present (17 tests) |
| `tests/unit/test_decomposition_check.py` | present (9 tests) |
| `tests/unit/test_overlap_check.py` | present (9 tests) |
| `tests/unit/test_pre_analyze_check.py` | present (15 tests) |
| `tests/unit/test_wp_gate.py` | present (67 tests) |
| `tests/unit/test_wp_report.py` | present (19 tests) |

No named guard reads an old anchor path.

### Registry

Row `070` at `.specify/features.md:76`: Status `Implemented`; Feature Details `.specify/features/070-subagent-task-teams.md` exists and is titled “驱动子代理的任务拆解与配合机制”; Spec Path `.specify/specs/070-subagent-task-teams/requirements.md` exists. **Resolves.**

### Three implementation claims — spot checks

1. **File claim** (`plan.md` structure): `skills/external/sdd-loop-driver/scripts/wp-gate.py`, `wp-report.py`, `decomposition-check.py`, `pre-analyze-check.py` and `stage-runner.sh` exist; `wp-gate.py` and `wp-report.py` are byte-identical to their `.specify/skills/` mirrors. **Holds.**
2. **Symbol/command claim** (`contracts/wp-gate.md`, `quickstart` Scenario B): `wp-gate.py` emits `cycle` (:665), `orphan-output` (:730), `write-write-unordered` (:1236) and `path-overlap` (:1245); `decomposition-check.py` declares `--mode plan|tasks` (:96) and returns `decision: proceed` when no split reason exists (:81, :114). **Holds.**
3. **Behaviour claim** (`tasks` T036, verification): the contract and unit inventories above exist and the mutation-drill file records control+mutant red runs. **Holds.**

### Verdict

**INTACT.** The only three dead references are anchor-rename moves (`memory/constitution.md`, `memory/features.md`, `memory/features/070.md`); no spec-owned stale pointer, no missing guard, and all three spot checks hold. Flag the three references for the rename migration.

---

## 080-humanize-run-output (Feature 062)

### Census

**134 distinct references → 109 alive / 1 archived / 24 dead** (4 moved, 13 renamed skill paths, 6 run-dir paths, 1 state-file renumber). One further reference is an abbreviated path whose full file exists and is counted alive (see below).

### Broken list

**Moved by the anchor rename (4 distinct):**

- `.specify/memory/constitution.md` — `data-model.md:149`, `notes/report-sample.md:22`, `plan.md:38,40` → now `.specify/constitution.md`
- `.specify/memory/features.md` — `contracts/wiring-compat.contract.md:31`, `data-model.md:151`, `feature-ref.md:16`, `notes/quickstart-run.md:298`, `notes/report-sample.md:22`, `plan.md:142`, `requirements.md:217`, `tasks.md:293`, `verification.md:286` → now `.specify/features.md`
- `.specify/memory/features/062.md` — `contracts/wiring-compat.contract.md:31`, `feature-ref.md:15`, `notes/quickstart-run.md:299`, `plan.md:141`, `requirements.md:217`, `tasks.md:293` → now `.specify/features/062-humanize-command.md`
- `.specify/memory/glossary.md` — `data-model.md:150`, `notes/report-sample.md:22` → now `.specify/glossary.md`

**Skill rename `humanize` → `humanize-conclusion` (13 distinct):**

- `.specify/skills/humanize/` — `contracts/wiring-compat.contract.md:21`, `plan.md:137`, `tasks.md:291` → now `.specify/skills/humanize-conclusion/`
- `.specify/skills/humanize/**` — `requirements.md:219`
- `.specify/skills/humanize/SKILL.md` — `contracts/wiring-compat.contract.md:14`, `notes/quickstart-run.md:301`, `plan.md:159`
- `.specify/skills/humanize/references/` — `notes/quickstart-run.md:307`
- `.specify/skills/humanize/references/*.md` — `plan.md:159`
- `skills/external/humanize/` — `contracts/wiring-compat.contract.md:21` → now `skills/external/humanize-conclusion/`
- `skills/external/humanize/**` — `requirements.md:217,219`, `tasks.md:169`, `verification.md:286`
- `skills/external/humanize/SKILL.md` — `notes/pre-change-measurements.md:71`, `notes/quickstart-run.md:303`, `notes/red-first-evidence.md:13`, `plan.md:130`, `quickstart.md:31`, `tasks.md:74,190,201,291`
- `skills/external/humanize/references` — `tasks.md:78`
- `skills/external/humanize/references/` — `plan.md:131`, `tasks.md:78,175`
- `skills/external/humanize/references/*.md` — `plan.md:159`
- `skills/external/humanize/references/report-shape.md` — `notes/red-first-evidence.md:77`
- `skills/external/humanize/references/run-mode.md` — `notes/quickstart-run.md:304`, `notes/red-first-evidence.md:14,123`
  All targets survive under `humanize-conclusion`: `SKILL.md`, `references/run-mode.md` and `references/report-shape.md` exist in both `skills/external/humanize-conclusion/` and its `.specify/` mirror.

**Run-directory drift (6 distinct):** the spec's `.specify/.tmp/humanize/` tree was superseded by `.specify/.tmp/humanize-conclusion/` (`skills/external/humanize-conclusion/SKILL.md:68`):

- `.specify/.tmp/humanize/` — 11 occurrences across `notes/quickstart-run.md:190,287,313`, `plan.md:91`, `quickstart.md:169`, `tasks.md:26,303,371`, `verification.md:127,131,250`
- `.specify/.tmp/humanize/<run_id>.run` — `data-model.md:103`, `plan.md:16,26,86`, `requirements.md:157`, `tasks.md:269`
- `.specify/.tmp/humanize/20261031T001000Z-s10001.run` — `notes/quickstart-run.md:29`
- `.specify/.tmp/humanize/no-such-dir/report.md` — `notes/quickstart-run.md:269`
- `.specify/.tmp/humanize/no-such-dir/.report.tmp` — `notes/quickstart-run.md:275,276`
- `.specify/.tmp/humanize/x.run` — `notes/pre-change-measurements.md:89` (twice), `tasks.md:48,190`

**State-file renumber (1):**

- `.specify/specs/080-humanize-run-output/notes/quickstart-run.md:310` → `.specify/state/080-humanize-run-output.md` missing; the actual state spine is `.specify/state/079-humanize-run-output.md` (slice `079`).

**Archived-elsewhere (1):**

- `.specify/specs/080-humanize-run-output/verification.md:21` → `.specify/specs/092-non-disposable/test-evidence/u08-report.txt` missing; the copy is at `.specify/archive/specs/092-non-disposable/test-evidence/u08-report.txt`.

**Abbreviated but alive (not dead):**

- `.specify/specs/080-humanize-run-output/notes/pre-change-measurements.md:7` → `.specify/memory/session/20261029T101833Z-...md` is a truncated reference; the full file `.specify/memory/session/20261029T101833Z-run-determination-speckit-checklist-r20261029t172918z-076a-c.md` exists.

**Supplementary (outside the counted census):** `review.md:65,90,93,272` records that `.specify/specs/080-humanize-run-output/code-review.md` was never produced; the review self-discloses the missing code-review segment (F9), so this is a recorded gap rather than a silent broken link.

### Guards

All named guard and fixture files exist, including `tests/contract/test_humanize_command_surface.py` (101 tests), `tests/fixtures/humanize/run/` with its scenario directories, `tests/integration/test_expression_line_pilot.py`, `tests/contract/test_stage_class_wiring.py`, and the expression/flow-class/feedback guards. **No missing guard file.**

However, the primary named guard is **statically broken by the anchor rename**:

- `tests/contract/test_humanize_command_surface.py:64` → `REGISTRY = REPO_ROOT / ".specify" / "memory" / "features.md"` (missing)
- `tests/contract/test_humanize_command_surface.py:65` → `FEATURE_DETAILS = REPO_ROOT / ".specify" / "memory" / "features" / "062.md"` (missing)
  Assertions at `:218-220` call `.is_file()` on both and will fail deterministically; `:1758` reads `FEATURE_DETAILS`. Live targets are `.specify/features.md` and `.specify/features/062-humanize-command.md`.

### Registry

Row `062` at `.specify/features.md:70`: Status `Implemented`; Feature Details `.specify/features/062-humanize-command.md` exists and is titled “Humanize Command”; Spec Path `.specify/specs/080-humanize-run-output/requirements.md` exists. **Resolves.**

### Three implementation claims — spot checks

1. **File claim** (`plan.md` / `contracts/wiring-compat.contract.md` WC-12): the skill is now `humanize-conclusion`; `skills/external/humanize-conclusion/SKILL.md`, `references/run-mode.md` and `references/report-shape.md` exist, and the `.specify/` mirror is identical. **Holds under the rename**; the spec's `humanize` path is dead.
2. **Command claim** (`templates/commands/humanize.md`): the template states run mode is the default (execute one instruction → five-section report) and content mode requires `--file`/`--inline`; the guard carries 101 IP/EX/RP/WC tests. **Holds.**
3. **Behaviour surface claim** (`data-model.md` E2/E5, `SKILL.md`): the run-dir is `.specify/.tmp/humanize-conclusion/` (SKILL.md:68), not the spec's `.specify/.tmp/humanize/`; the five-section report and run-mode references exist. **Holds with drift** — the run-dir naming changed after the spec was written.

### Verdict

**BROKEN.** The feature's primary contract guard now reads two dead anchor paths and will fail; the skill surface was renamed (`humanize` → `humanize-conclusion`), the run-directory was renamed, and the state spine uses slice `079`. The implementation exists and the three spot checks hold under the renamed paths.

---

## 093-concurrency-by-default

### Census

**322 extracted; 3 are illustrative** (`src/generated/` and `src/generated/wp02.md` as fixture write domains at `notes/engine-fix.md:39,86`; `tests/contract/test_x.py` as a generic runner example at `requirements.md:196`). **319 path references → 272 alive / 0 archived / 47 dead** (9 moved, 3 goal-tree renames, 2 retired-path mentions, 3 pre-consolidation pointers, 1 wrong-layer guard pointer, 1 missing evidence file, 1 renumbered spec pointer, 27 ephemeral run/worktree paths).

### Broken list

**Moved by the anchor rename (9 distinct):**

- `.specify/memory/constitution.md` — `plan.md:58`, `research.md:5`, `notes/analyze-findings.md:7` → `.specify/constitution.md`
- `.specify/memory/features.md` — 6 occurrences, e.g. `notes/review-arc.md:11,20,72`, `notes/review-process-artifacts.md:227` → `.specify/features.md`
- `.specify/memory/features/064.md` — `plan.md:290` → `.specify/features/064-subagent-concurrency.md`
- `.specify/memory/features/070.md` — `plan.md:291` → `.specify/features/070-subagent-task-teams.md`
- `.specify/memory/features/086.md` — `plan.md:292` → `.specify/features/086-efficient-test-execution.md`
- `.specify/memory/features/092.md` — `plan.md:293` → current `092` is `.specify/features/092-non-disposable.md`; the goal/team spec the plan means was renumbered to **094** (`.specify/features/094-goal-team-parallel.md`)
- `.specify/memory/features/093.md` — 8 occurrences, e.g. `plan.md:63`, `feature-ref.md:6`, `notes/serial-baseline.md:20` → `.specify/features/093-concurrency-by-default.md`
- `.specify/memory/glossary.md` — `notes/analyze-findings.md:49` → `.specify/glossary.md`
- `.specify/memory/register.md` — 12 occurrences, e.g. `requirements.md:335`, `notes/amend-fr036.md:22`, `notes/review-process-artifacts.md:187` → `.specify/register.md`

**Goal-tree rename (3 distinct, disclosed):** `.specify/goal` / `.specify/goal/` / `.specify/goal/<slug>/` — 14 occurrences across `requirements.md:185,295,309`, `tasks.md:76`, `notes/analyze-repair.md:73,77`, `notes/analyze-repair2.md:63,106`, `notes/analyze-lite-fr036.md:50`. The current root is `.specify/anchoring/<slug>/goal.md`; `requirements.md:307` carries an explicit erratum and `tasks.md:76` names the former tree in a measurement note. Treated as disclosed historical mentions, not silent drift.

**Retired-path mentions (2 distinct, intentional):** `.specify/templates/commands/` — `plan.md:261`, `contracts/existing-semantics-disposal.contract.md:45`, `notes/analyze-findings.md:169`, `notes/implement-wp5.md:56`; and `.specify/templates/commands/tasks.md` — `notes/analyze-findings.md:169`. The plan says “NO `.specify/templates/commands/` mirror (retired)” and contract C-090 forbids reviving it; these are retirement statements, not live pointers.

**Pre-consolidation pointers (3 distinct):**

- `.specify/specs/093-concurrency-by-default/notes/analyze-repair3.md:14,26` → `scripts/stage-runner.sh` missing; live at `skills/external/sdd-loop-driver/scripts/stage-runner.sh` (and the `.specify/` mirror).
- `.specify/specs/093-concurrency-by-default/research.md:7`, `notes/review-implementation-code.md:114` → `scripts/wp-gate.py` missing; live at `skills/external/sdd-loop-driver/scripts/wp-gate.py`.
- `.specify/specs/093-concurrency-by-default/research.md:7`, `notes/review-implementation-code.md:114` → `templates/stage-team-preset.md` missing; live at `skills/external/sdd-loop-driver/templates/stage-team-preset.md`.

**Wrong-layer guard pointer (1):**

- `.specify/specs/093-concurrency-by-default/notes/review-implementation-code.md:72,87` → `tests/contract/test_concurrency_check_engine.py` missing; the module is `tests/unit/test_concurrency_check_engine.py`. The spec's own review records this as broken evidence pointer C-2 (`:87-88`: “no such file exists (the module is tests/unit/test_concurrency_check_engine.py)”).

**Missing evidence file (1):**

- `.specify/specs/093-concurrency-by-default/tasks.md:31` → `test-evidence/suite-after-implement.txt` missing. Related retained readings: `test-evidence/wp5-gate1-comparison.txt`, `wp5-suite-final.txt`, `wp5-suite-pre.txt`, `suite-baseline-093*.txt`.

**Renumbered spec pointer (1):**

- `.specify/specs/093-concurrency-by-default/plan.md:293` → `.specify/specs/092-goal-team-parallel/verification.md` missing; the goal/team parallel spec is now `.specify/specs/094-goal-team-parallel/` (`094` was created 2026-11-09 redefining 085).

**Ephemeral run/worktree paths (27 distinct):** the `.specify/.tmp/sdd-loop/worktrees/093-*` worktrees (`093-clarify`, `-enginefix`, `-review`, `-wp2`…`-wp5`) and the `.specify/.tmp/wp5/quickstart/*` case files, plus `.specify/.tmp/sdd-loop/tmp/concurrency-by-default/design.md`. Only `rename-anchors` remains under `.specify/.tmp/sdd-loop/worktrees/`; these are dated evidence pointers to removed temp trees.

### Guards

The concurrency contract/unit guards exist: `tests/contract/test_concurrency_class_table.py`, `test_concurrency_declarations.py`, `test_concurrency_dispatch_capability.py`, `test_concurrency_disposal.py`, `test_concurrency_high_order.py`, `test_concurrency_real_run_evidence.py`, `test_concurrency_reproduction_092.py`, `test_concurrency_serial_reason.py`, `test_concurrency_units.py`, `tests/unit/test_concurrency_check_engine.py`, plus the WP guards shared with 070. The only named guard path that does not exist is the `tests/contract/` layer of `test_concurrency_check_engine.py` (module lives under `tests/unit/`; self-disclosed). The re-pinned cross-feature guard `tests/contract/test_humanize_command_surface.py` has the old-anchor defect described under 080 (`:64-65`).

### Registry

Row `102` at `.specify/features.md:102`: Status `Blocked`; Feature Details `.specify/features/093-concurrency-by-default.md` exists; Spec Path `.specify/specs/093-concurrency-by-default/requirements.md` exists. **Resolves**, but the detail file says “36 FR / 12 SC” at `.specify/features/093-concurrency-by-default.md:60` while `requirements.md` records the FR count as **33** (the clarify number-change notice in requirements and the registry notes both record 36 → 33). Minor detail-file drift.

### Three implementation claims — spot checks

1. **File claim** (`plan.md` / tasks T004–T005): `scripts/python/concurrency-check.py` (70,626 bytes) and `.specify/scripts/python/concurrency-check.py` are byte-identical; the eight fact files (`concurrency-class`, `serial-reason`, `effective-concurrency`, `concurrency-slot-and-reserve`, `decomposition-coverage`, `executor-enumeration-roots`, `concurrency-contract`, `coordinator-dispatch-verdict`) exist under `shared/declarations/facts/`. **Holds.**
2. **Symbol/command claim** (`contracts/judgement-engine.contract.md` C-020): `scripts/python/concurrency-check.py:69` declares the closed action set `classify / serial-reason / reading / coverage / capability`; `tests/unit/test_concurrency_check_engine.py` pins the set, the `--record` requirement and the exit-code grammar. **Holds.**
3. **Behaviour claim** (`tasks` T152 / SC-008): the concurrency contract and unit guards exist, the engine emits `decision=pass` readings, and the spec's own review records the test-layer pointer error. **Holds**, with the guard-layer pointer defect above.

### Verdict

**BROKEN.** Three pre-consolidation pointers (`scripts/stage-runner.sh`, `scripts/wp-gate.py`, `templates/stage-team-preset.md`), one wrong-layer guard pointer (self-disclosed), one missing evidence file, one renumbered spec pointer, 27 dead ephemeral evidence paths, and nine rename-moved anchors. The engine, fact declarations and concurrency guards are present and the three spot checks hold.

---

## Batch-wide observations

### 1. The anchor rename landed mid-audit

Master moved from `564a5f5a6` to `6fb8093c4` during the audit. The merge moved `.specify/memory/{constitution,features,glossary,register,tools}.md` to `.specify/` root and `.specify/memory/features/*.md` to `.specify/features/<NNN>-<slug>.md`. It did **not** move `.specify/memory/{feedback,session,tools/,knowledge,evidence,...}`. Every spec in this batch has at least one such moved reference — 28 distinct across the batch; for 070 these are its **only** dead references:

| Spec | Moved refs | Post-rename targets |
|---|---:|---|
| 016 | 3 | `.specify/constitution.md`, `.specify/features.md`, `.specify/features/016-refactor-tools-command.md` |
| 032 | 3 | `.specify/constitution.md`, `.specify/features.md`, `.specify/features/036-team-summary.md` |
| 044 | 3 | `.specify/constitution.md`, `.specify/features.md`, `.specify/features/046-confirmation-gate-governance.md` |
| 058 | 3 | `.specify/constitution.md`, `.specify/features.md`, `.specify/features/058-sdd-loop-driver.md` |
| 070 | 3 | `.specify/constitution.md`, `.specify/features.md`, `.specify/features/070-subagent-task-teams.md` |
| 080 | 4 | `.specify/constitution.md`, `.specify/features.md`, `.specify/features/062-humanize-command.md`, `.specify/glossary.md` |
| 093 | 9 | plus `.specify/features/{064,070,086,092,093}.md`, `.specify/glossary.md`, `.specify/register.md` |

### 2. Framework guards still read the old anchors

The rename also left guards on the removed paths. Named by this batch:

- `tests/contract/test_humanize_command_surface.py:64-65` — named by 080 and re-pinned by 093; reads `.specify/memory/features.md` and `.specify/memory/features/062.md`; assertions at `:218-220` will fail.
- `tests/contract/test_tools_command_routing.py:153` — guards the 016 command surface; reads `.specify/memory/constitution.md`.

Outside the batch's named guards but same failure class (found while checking): `tests/contract/test_fast_fail_discipline.py:61` (`CONST_LIVE = .specify/memory/constitution.md`), `tests/contract/test_one_source_of_truth.py:24`, and `tests/contract/test_problem_solving_naming.py:23` all read removed paths. Two further hits are **not** file reads and should not be counted as breakage: `tests/contract/test_shipped_surface_client_neutrality.py:34` is a placeholder-rejection regex (`.specify/memory/features/\d{3}`), and `tests/contract/test_gate_wiring_081.py:517` embeds the old path in a fixture registry row string. These are migration work for 090, not spec-owned defects of batch 6.

### 3. Registry detail-file slug defect (Feature 036)

`.specify/features.md:45` (Feature 036 Dogfooding Practice) points to `.specify/features/036-team-summary.md`. The file's content is correct (`# Feature Detail: Dogfooding Practice`, `Feature ID: 036`), but the filename slug belongs to the separate spec `.specify/specs/036-team-summary/` (a requirement bound to Feature 027). The paired row 027 has the inverse cross-wiring (`.specify/features/027-feedback-mechanism.md` contains Feature 027 Team Management), so the rename's detail-file naming map is inconsistent; both cells resolve by ID but the slugs are wrong.

### 4. Self-disclosed / dated defects

- 080 `review.md:65,90,93,272` explicitly records that `code-review.md` was never produced (F9) — a known gap, not a silent break.
- 093 `notes/review-implementation-code.md:87-88` explicitly records the `tests/contract` vs `tests/unit` layer error for `test_concurrency_check_engine.py`.
- 093 `requirements.md:307` explicitly corrects the `.specify/goal` → `.specify/anchoring` rename; the dated occurrences remain in the Clarifications and checklist records.
- 044 `baseline.json` and 080/093 `baseline-*`/`test-evidence/*` contain many historical paths; they are dated records and were excluded from the counted census.

**Anomaly**: the `memory/` → `.specify/` anchor rename merged into master mid-audit (`6fb8093c4`), turning 28 previously-live references in this batch dead and leaving at least two named guards reading removed paths (`tests/contract/test_humanize_command_surface.py:64-65`, `tests/contract/test_tools_command_routing.py:153`); separately, Feature 036's detail cell resolves to `036-team-summary.md` — correct content, wrong slug.

SPEC-AUDIT-LIVE-6-DONE
