# Read-only live-spec audit — batch 4 (7 specs)

**Scope**: 012-skill-home-workdir, 030-summarize-project, 042-goal-team-creation,
056-probe-handler-system, 068-exec-quant-feedback-channel, 078-coaching-skills, 090-re-anchoring.

**Snapshot**: measured read-only at working-tree HEAD `f5ac8e654` (the anchor-layout merge
`6fb8093c4` landed *during* this audit — see the anomaly line at the bottom). No spec or
source file was modified; this file is the only write.

## Method and counting rule

- **Sources scanned**: `requirements.md`, `plan.md`, `tasks.md`, `research.md`, `data-model.md`,
  `quickstart.md`, `verification.md`, `feature-ref.md`, `contracts/**`, `notes/**`.
  Run records (`test-evidence/**`, `checkpoints/**`, `checklists/**`, `baseline-failed.txt`,
  `phase*-current.txt`, `coverage-baseline.txt`) were excluded so historical evidence paths
  do not inflate the result.
- **Counted unit**: distinct literal repository path strings after stripping trailing
  punctuation/slashes. Globs and placeholders (`<name>`, `...`, `*`), illustrative examples
  (`skills/foo`, `skills/my-skill`), prose fragments (`shared/docs`, `tests/evidence`),
  target-project output contracts (`docs/overview.md`, `docs/project-summary/`), sanctioned
  scratch (`.specify/.tmp/**`), and historical/negative records are **not** counted.
- **Buckets**: `alive` = exists now; `archived` = resolves under `.specify/archive/`;
  `moved` = old anchor path whose target exists at the new `.specify/` root after the
  anchor-layout merge (flagged separately, not counted dead); `dead` = no target.
- **Store roots**: engine-owned roots that are created on demand
  (`.specify/memory/feedback/probes/`, `.specify/memory/exec-quant/aggregated/`,
  `.specify/memory/sanitize/`) count as alive when the owning engine constant exists.
- **Guards**: every `tests/**/test_*.py` named by the spec's authored artifacts was checked
  for existence. Spot-checks verify file + symbol/command + behaviour surface.

## Anchor-layout rename (landed mid-audit)

Commit `6fb8093c4` moved the project anchors out of `memory/`:
`.specify/memory/{constitution,features,glossary,register,tools}.md` →
`.specify/{constitution,features,glossary,register,tools}.md`, and feature details became
`.specify/features/<ID>-<slug>.md`. Every `.specify/memory/{constitution,features,glossary,register}.md`
reference below is therefore **moved**, not dead, unless it was already dead for another reason.
The moved detail files still carry their old upstream bodies (012 = Review Command,
030 = History Command, 042 = Interview Mode) — path resolution succeeds, content does not match.

---

## 012-skill-home-workdir

**Counts** (23 refs): 17 alive · 1 archived · 2 moved · 3 dead.

**Broken**
- `contracts/skill-home-workdir-template.openapi.yaml:41,42,162,185` →
  `skills/create-skills/SKILL.md` and `skills/improve-skills/SKILL.md` do not exist. The live
  canonical sources are `skills/external/create-skills/SKILL.md` and
  `skills/external/improve-skills/SKILL.md`; lines 43–44 already name those mirrors, so the
  contract's default edit set fails on 2 of its 5 targets.
- `plan.md:87,174`, `quickstart.md:107`, `contracts/...yaml:12`,
  `tasks.md:20,44,52,62,78,82,89,103,107,112,126,130,137,147,148,248` →
  `tests/contract/test_skill_home_workdir_template.py` is **missing**. No file or symbol by
  that name exists; the nearest live layout guard
  (`tests/contract/test_skill_install_layout_contract.py`) does not mention `SKILL_HOME`.
- **Registry**: `.specify/features.md:21` (row 012) has Spec Path `-`; its Feature Details cell
  `.specify/features/012-skill-home-workdir.md` exists but the body is
  “Feature Detail: Review Command” — wrong feature. The spec's `feature-ref.md` binds Feature
  013, whose row points its Spec Path at `030-summarize-project/requirements.md`, not at 012.
- **Archived**: `contracts/...yaml:9` → `.specify/archive/specs/008-create-skills-skill/contracts/create-skills-workflow.openapi.yaml` (resolves).

**Moved by anchor rename**: `tasks.md:153` `.specify/memory/features/013.md` →
`.specify/features/013-portable-skill-creation.md`; `feature-ref.md` `.specify/memory/features.md`
→ `.specify/features.md`.

**Guards**: 1 named, 1 missing (`test_skill_home_workdir_template.py`).

**Spot-checks**
1. **PASS** — `templates/commands/skills.md:44,54` carries the `${SKILL_HOME}` / `${SKILL_WORKDIR}` conventions.
2. **PASS** — `diff -q` between `skills/external/{create,improve}-skills/SKILL.md` and their
   `.specify/skills/...` mirrors returns 0 (byte-equivalent).
3. **CAVEAT** — SC-006 “zero residual `SKILL_ROOT`”: `skills/external/improve-skills/SKILL.md:56`
   still contains `${SKILL_ROOT}/X` as a legacy-idiom example. The named guard that would
   distinguish prose mention from live use is missing, so the claim is unverifiable.

**Verdict: BROKEN** — missing guard, stale contract source paths, registry row does not resolve.

---

## 030-summarize-project

**Counts** (33 refs): 15 alive · 0 archived · 3 moved · 15 dead.

**Broken**
- `skills/analysis-project` family (`plan.md:12,14,19,43,76,78`; `quickstart.md:18,38,53`;
  `tasks.md:17,126,167`; `data-model.md:114`; `contracts/visual-reporting-skills.openapi.yaml:99,130`)
  → no `analysis-project` package exists in `skills/external/` or `skills/internal/`, and no
  `.specify/skills` mirror. Workstream WS-B (UML enhancement of `analysis-project`) has no live carrier.
- `skills/draw-plantuml` and `skills/draw-plantuml/SKILL.md` (`plan.md:14,19,43`) → retired on
  2026-10-12 into `skills/external/draw-diagram`; the retirement is guarded by
  `tests/contract/test_no_retired_draw_skill_refs.py`.
- Flat `skills/summarize-project` and `.specify/skills/summarize-project`
  (`plan.md:77`; `data-model.md:98,113`; `contracts/...yaml:15,19,20,25,40,73`) → the live
  package is `skills/internal/summarize-project` and `.specify/skills/internal/summarize-project`.
- `tests/contract/conftest.py` (`tasks.md:46`) → missing. `tests/conftest.py` and the chosen
  `tests/contract/helpers_prompt_assets.py` exist, so the “conftest **or** helpers” alternative
  was satisfied; only the literal path is dead.
- **Guards missing**: `tests/contract/test_analysis_project_uml_assets.py`
  (`quickstart.md:17,26,59`; `plan.md:39,80`; `tasks.md:15,117,127`) and
  `tests/contract/test_create_skills_prompt_assets.py` (`quickstart.md:10`; `plan.md:21,97`).
  `plan.md:21` also cites `test_skill_home_workdir_template.py`, missing per the 012 section.
- **Registry**: `.specify/features.md:39` (row 030) has Spec Path `-`; its Feature Details cell
  `.specify/features/030-summarize-project.md` exists but the body is “Feature Detail: History
  Command”. Row 013's Spec Path does point at this spec's `requirements.md`, but row 013's
  detail is “Skills Command”, not this spec.

**Moved by anchor rename**: `.specify/memory/constitution.md`,
`.specify/memory/features/013.md`, `.specify/memory/features.md`.

**Guards**: 3 named, 2 missing; plus one bare-name precedent
(`test_skill_home_workdir_template.py`) also missing.

**Spot-checks**
1. **PASS** — `skills/internal/summarize-project/SKILL.md:2,6,7` has `name: summarize-project`,
   the mirror `skill_id`, and `classification: internal`.
2. **PASS** — `tests/contract/test_summarize_project_prompt_assets.py:56,63` pins the canonical
   and mirror directories.
3. **FAIL** — the `analysis-project` UML enhancement (second workstream) has neither a skill
   package nor its guard test in the tree; no live replacement was found.

**Verdict: BROKEN** — one whole workstream dangles, two guards missing, registry row does not resolve.

---

## 042-goal-team-creation

**Counts** (51 refs): 43 alive · 0 archived · 2 moved · 6 dead.

**Broken**
- `quickstart.md:59` → `skills/create-team/scripts/verify-territory-disjoint.py` is missing; the
  live script is `skills/internal/create-team/scripts/verify-territory-disjoint.py` (zero-write,
  exit codes 0/2/3/4 documented in its header).
- `.specify/goal` storage (`plan.md:9,17`; `requirements.md:104`; `quickstart.md:18` including
  `.specify/goal/improve-harness/goal.md`) → there is no `.specify/goal/`. The goal archive root
  is `.specify/anchoring/`; `scripts/python/goal-utils.py:71-75` declares
  `ARCHIVE_DIRNAME = ".specify/anchoring"` and calls `SPEC_GOAL_DIRNAME = "goal"` a retired
  migration source only.
- **Guards missing**:
  - `tests/contract/test_goal_team_creation.py` (`quickstart.md:5`; `plan.md:86`;
    all four contracts; `tasks.md:70,80,104`; `verification.md:24`).
  - `tests/contract/test_targets_check.py` (`quickstart.md:5`; `plan.md:84`;
    `contracts/decomposition-proposal.contract.md:43`; `tasks.md:32,94,104`) — the live
    equivalent is `tests/contract/test_goal_targets_check.py`.
  - `tests/contract/test_run_target_assignment.py` (`plan.md:18,113`; `verification.md:24`;
    `tasks.md:80,133`) — no same-name file; `tests/contract/test_team_command_routing.py`
    carries some goal-branch assertions and `test_focus_target_resolution.py` covers the
    resolution face.
- **Registry**: `.specify/features.md:51` (row 042) has Spec Path `-`; its Feature Details cell
  `.specify/features/042-goal-team-creation.md` exists but the body is “Feature Detail: Interview
  Mode”. The declared bound row 027 exists, but its Spec Path is
  `.specify/specs/036-team-summary/requirements.md` (a sibling), not this spec.

**Moved by anchor rename**: `.specify/memory/constitution.md`,
`.specify/memory/features/027.md`.

**Guards**: 7 named, 3 missing.

**Spot-checks**
1. **PASS** — `scripts/python/goal-utils.py:22,2680` exposes `targets <slug> --check`.
2. **PASS** — `skills/internal/create-team/scripts/verify-territory-disjoint.py` exists with the
   documented pairwise-overlap verdicts and zero writes.
3. **FAIL** — `plan.md:17` claims the fact source is `.specify/goal/<slug>/goal.md`; the engine
   reads `.specify/anchoring/<slug>/goal.md`. Storage claim and engine disagree.

**Verdict: BROKEN** — goal storage path drift, flat skill path, three missing guards, registry row.

---

## 056-probe-handler-system

**Counts** (73 refs): 67 alive · 0 archived · 4 moved · 2 dead.

**Broken**
- `verification.md:57` → `docs/git-workflow.md` no longer exists; the git-workflow owner is now
  `.specify/workflow/git.md`. The dated disclosure (“file exists”) is no longer true.
- `tasks.md:54` → `.specify/skills/external` does not exist; external skills mirror flat under
  `.specify/skills/<name>/` and internal skills under `.specify/skills/internal/`. The measurement
  command at that line would count 0, not the recorded 11.
- **Not broken, counted alive**: `.specify/memory/feedback/probes/` is the engine-owned external
  probe store (`probe-utils.py:32,270,634-635` creates it on demand);
  `src/specify_cli.generate_commands` is a symbol in `src/specify_cli/__init__.py:1588`, not a module.

**Moved by anchor rename**: `.specify/memory/constitution.md`,
`.specify/memory/features/056.md`, `.specify/memory/features.md`,
`.specify/memory/glossary.md`.

**Registry**: resolves — row `.specify/features.md:64` has
`.specify/features/056-probe-handler-system.md` and
`.specify/specs/056-probe-handler-system/requirements.md`, both existing. Note: the detail body's
`**Status**: Planned` is stale against the row's `Implemented`.

**Guards**: 15 named, 0 missing (compile-embeds, handler-registry, phase-2 bindings, probe action
sets/registry/nonentity catalog, propagation/reconcile, confirmation-gates, feedback step form,
run determination, wrap-up budgets).

**Spot-checks**
1. **PASS** — `scripts/python/probe-utils.py:1427` action closure is
   `probes, map, probe-inject, handlers, compile-embeds`.
2. **PASS** — `shared/definitions/probe-definitions.md:203,235` has `## Handler` and
   `## HandlerBinding`; `tests/contract/test_handler_registry.py:76,80` parses both tables.
3. **PASS** — the external probe store is still `.specify/memory/feedback/probes`
   (`probe-utils.py:32,270,634-635`), matching FR-009's zero-migration claim.

**Verdict: BROKEN** — two dead pointers, both minor/dating drift; guards and registry resolve.

---

## 068-exec-quant-feedback-channel

**Counts** (326 refs): 323 alive · 0 archived · 3 moved · 0 dead.

**Broken**: none.

**Dated note (not counted)**: `notes/pre-change-measurements.md:198` records a then-missing
`.specify/skills/internal/study-project/references/uml-visualization-guide.md` mirror (a `sync-mirrors`
DIFF line from the pre-change measurement). It is a historical reading, not a live pointer.

**Moved by anchor rename**: `.specify/memory/constitution.md`,
`.specify/memory/features/068.md`, `.specify/memory/features.md`.

**Registry**: resolves — row `.specify/features.md:75`, details
`.specify/features/068-exec-quant-feedback-channel.md`, Spec Path
`.specify/specs/068-exec-quant-feedback-channel/requirements.md`, all existing; detail status
`Ready for Review` matches the row.

**Guards**: 36 named test files (contract/unit/integration), 0 missing.

**Spot-checks**
1. **PASS** — `scripts/python/exec-quant.py:135,171` exposes the `aggregate` action and
   `AGGREGATED_DIR_NAME = "aggregated"`.
2. **PASS** — `scripts/python/feedback-utils.py:1911-1993` implements `ingest-exec-quant`
   (`--package` required, idempotent dedup, non-writable-store exit 2).
3. **PASS** — `docs/reference/skills/feedback.md:271-277` documents aggregation as a separate
   explicit `exec-quant.py --action aggregate` follow-up, never automatic.

**Verdict: INTACT**.

---

## 078-coaching-skills

**Counts** (122 refs): 118 alive · 0 archived · 4 moved · 0 dead.

**Broken**: none.

**Known advisory (not counted)**: `verification.md:174` records
`.specify/templates/commands/` as absent, an analyze-stage advisory already captured at the time
(the line records the absence rather than asserting a live path). Historical negatives at
`notes/quickstart-run.md:191,193` record the removed `think-skills` package — intentional
post-rename assertions, not dead pointers.

**Moved by anchor rename**: `.specify/memory/constitution.md`,
`.specify/memory/features/078.md`, `.specify/memory/features.md`,
`.specify/memory/register.md`.

**Registry**: path-wise resolves — row `.specify/features.md:87`, details
`.specify/features/078-coaching-skills.md`, Spec Path
`.specify/specs/078-coaching-skills/requirements.md`, all existing. Note: the detail body's
`**Status**: Planned` is stale against the row's `Implemented`.

**Guards**: 9 named, 0 missing (the five coaching contracts — run / expectation / observation /
dispatch / wiring — plus four related guards).

**Spot-checks**
1. **PASS** — `skills/external/coaching-skills/SKILL.md:2,6,7` has `name: coaching-skills`, the
   mirror `skill_id`, and `classification: external`.
2. **PASS** — `tests/contract/test_coaching_wiring_contract.py:61,317` asserts the sole permitted
   live occurrence is in `src/specify_cli/__init__.py`.
3. **PASS** — `diff -rq skills/external/coaching-skills .specify/skills/coaching-skills` is silent
   (mirror byte-equivalent).

**Verdict: INTACT**.

---

## 090-re-anchoring

**Counts** (164 refs): 149 alive · 2 archived · 7 moved · 6 dead.

**Broken**
- `plan.md:298` asserts the 092 slice's artifacts “remain under `.specify/specs/092-non-disposable/`
  and are read **in place**”. They are under `.specify/archive/specs/092-non-disposable/` — the
  asserted location and the “in place” claim are both false now.
- Open tasks still target the removed `.specify/specs/092-non-disposable/` tree:
  - `tasks.md:422,440` → `test-evidence/repair-corpus.md` absent (T119A / T137A); the archive has
    no `repair-corpus.md`.
  - `tasks.md:448` (and T140A/T141A appends) → `test-evidence/shift-092.md` absent (T139A).
  - `tasks.md:462` → `verification.md` absent (T147A); the archive carries no `verification.md`.
  - `tasks.md:468` → `test-evidence/INDEX.md` absent (T153A).
  - `tasks.md:465` → `closure-acceptance-check.py --spec-dir .specify/specs/092-non-disposable`
    (T150A) points at a removed directory.
- `tasks.md:435` → `.specify/specs/089-script-interface-contract/team/086-script-interface-contract/`
  is absent; 089 has no `team/` directory (T132A).
- `contracts/nd-acceptance-readability.contract.md:165` → `team/092-non-disposable/team.md`
  (relative to the 092 tree); the archive has `team/team.md`, not that nested path.
- `contracts/nd-renumber-and-supersede.contract.md:54` → `.specify/specs/.archive/` is absent.
  It is used only as an exclusion prefix, so the effect is benign, but the path has no target.
- **Moved-anchor open tasks**: `tasks.md:466` `.specify/memory/features.md` and
  `tasks.md:467` `.specify/memory/features/092.md` → now `.specify/features.md` and
  `.specify/features/092-non-disposable.md`.
- **Correctly migrated already**: `tasks.md:148,149` use
  `.specify/archive/specs/092-non-disposable/test-evidence/tasks-gates.txt` (alive), so the 092
  evidence migration is partial, not absent.

**Moved by anchor rename**: `.specify/memory/constitution.md`,
`.specify/memory/features/089.md`, `.specify/memory/features/090.md`,
`.specify/memory/features/092.md`, `.specify/memory/features.md`,
`.specify/memory/glossary.md`, `.specify/memory/register.md`.

**Registry**: resolves — row `.specify/features.md:98`, details
`.specify/features/090-re-anchoring.md`, Spec Path
`.specify/specs/090-re-anchoring/requirements.md`, all existing.

**Guards**: the guard contract names two owned guards
(`tests/contract/test_reanchoring_contract.py`, `tests/contract/test_sdd_loop_driver_reanchor.py`)
plus two related ones (`test_constitution_double_landing.py`, `test_fast_fail_discipline.py`);
the Non-Disposable guard `tests/contract/test_non_disposable_contract.py` also exists. 0 missing.

**Spot-checks**
1. **PASS** — `scripts/python/non-disposable-check.py:59-70` imports only stdlib
   (argparse/datetime/hashlib/json/re/subprocess/sys/pathlib); `--json` / `--version` are declared,
   and no write-mode open/`write_text` was found (read-only engine).
2. **PASS** — `shared/definitions/re-anchoring-definitions.md:51-57` defines the T0/T1/T2 reload tiers
   and their firing conditions.
3. **PASS** — `skills/external/sdd-loop-driver/references/checkpoint-protocol.md:63,195` defines the
   three-value verdict `on-track` / `correction-applied` / `decision-needed`.

**Verdict: BROKEN** — the 092 slice's “read in place” claim and six open-task/write targets point
at a tree that is now archived.

---

## Batch summary

| spec | refs | alive | archived | moved | dead | verdict |
|------|-----:|------:|---------:|------:|-----:|---------|
| 012-skill-home-workdir | 23 | 17 | 1 | 2 | 3 | **BROKEN** |
| 030-summarize-project | 33 | 15 | 0 | 3 | 15 | **BROKEN** |
| 042-goal-team-creation | 51 | 43 | 0 | 2 | 6 | **BROKEN** |
| 056-probe-handler-system | 73 | 67 | 0 | 4 | 2 | **BROKEN** |
| 068-exec-quant-feedback-channel | 326 | 323 | 0 | 3 | 0 | **INTACT** |
| 078-coaching-skills | 122 | 118 | 0 | 4 | 0 | **INTACT** |
| 090-re-anchoring | 164 | 149 | 2 | 7 | 6 | **BROKEN** |

`moved` is an added column for the anchor-layout rename: those paths left
`.specify/memory/` during the audit and resolve at the new `.specify/` root, so they are flagged
rather than counted dead. `refs = alive + archived + moved + dead`.

**Cross-cutting observations**
- The registry rows for 012, 030 and 042 have `Spec Path = -`. Their Feature Details cells now
  resolve (post-rename), but all three detail bodies describe upstream features (Review /
  History / Interview) rather than the local specs. The bound-feature rows (013, 013, 027) do not
  point at these specs either, except row 013's Spec Path which points at 030.
- 056 and 078 have stale detail statuses (`Planned`) against registry rows that say `Implemented`.
- The missing-guard cluster is concentrated in 012/030/042: the named structural tests were
  either never landed (`test_skill_home_workdir_template.py`, `test_goal_team_creation.py`) or
  were renamed (`test_goal_targets_check.py`) without updating the spec references.
- The anchor-layout merge moved files but did not rewrite spec references or feature-detail
  bodies; the `.specify/memory/*` references in all seven specs are now stale pointers to the
  new root.

ANOMALY: the anchor-layout merge `6fb8093c4` landed in the working tree mid-audit — `.specify/memory/{constitution,features,glossary,register,tools}.md` are gone, the moved feature-detail bodies still describe the old upstream features (012=Review, 030=History, 042=Interview), and AGENTS.md documents `.specify/features/<ID>.md` while the tree uses `.specify/features/<ID>-<slug>.md`.

SPEC-AUDIT-LIVE-4-DONE
