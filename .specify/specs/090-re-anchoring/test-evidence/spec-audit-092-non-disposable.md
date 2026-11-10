# Spec Audit — 092-non-disposable (batch 11)

Read-only audit of `.specify/archive/specs/092-non-disposable/` against the CURRENT tree.
Audited tree: `master` @ `6fb8093c4` (2026-11-10). **The tree moved mid-audit** — it started at `564a5f5a6`
and the anchor-layout merge landed during the run; every path below was re-measured on `6fb8093c4`.
No spec or source file was modified; this file is the only write.

## Scope

Artifacts read in full: `requirements.md` (65 FR / 20 SC), `plan.md`, `tasks.md`, `data-model.md`,
`research.md`, `quickstart.md`, `feature-ref.md`, 8 `contracts/*.contract.md`, 5 `notes/*.md`
(`notes/baseline-failed-tests.txt` excluded as raw output), 1 checklist, `team/team.md`,
`goal/092-non-disposable/goal.md`. `test-evidence/` was read only for cross-reference, not audited as claims.

**No `verification.md` exists in this archive entry** — the spec planned one (`plan.md:215`, `tasks.md:320`)
but it was never produced (finding D3 below).

Classification rule (stated for reproducibility):

- **alive** — the literal resolves in the live tree now.
- **archived-elsewhere** — the object survives only under `.specify/archive/specs/092-non-disposable/`;
  the literal is a stale pre-archive form (`.specify/specs/092-non-disposable/...`).
- **dead** — no target at the stated path.

Counting unit: distinct repository path literals (glob patterns counted once). Trailing-slash literals were
checked with `[ -e ]` (bash `compgen -G` falsely matches a nonexistent trailing-slash path); `*` globs were expanded.

Conservative rule: because the spec now lives in the archive, all 17 archived-elsewhere literals are also
**broken links as written**. If the instruction's parenthetical is applied literally (stale pre-archive = dead),
the tally becomes 137 alive / 0 archived-elsewhere / 44 dead. Both readings are given so the count is reproducible.

## Counts

| Class | Count |
|---|---|
| References total (distinct) | **181** |
| alive | **137** |
| archived-elsewhere | **17** |
| dead | **27** |

Dead breakdown: 7 promised-but-never-produced artifacts with no archive copy; 4 stale/defect references
(`.specify/goal/**`, 088 `efficiency-model.md`, 089 old team dir, `.specify/specs/.archive/`); 5 moved by the
anchor-layout merge (`.specify/memory/{constitution,features,glossary,register}.md` and `features/092.md`);
8 by-design/negative/illustrative; 3 placeholder templates.

Pre-archive literal occurrences: **63** across 12 artifacts — 47 inside the 17 archived-elsewhere literals,
16 inside the 7 no-target literals. The anchor-layout merge removes 5 more literals from the live set
(the `.specify/memory/...` forms; their live owners are the `.specify/` root files).

## Reference inventory

### Alive (137)

`scripts/bash/{collect-history,generate-instructions,run-tests}.sh`; `scripts/python/` and its
`account-clause-coverage.py`, `closure-acceptance-check.py`, `declaration_reader.py`,
`harness-triple-check.py`, `history-utils.py`, `non-disposable-check.py`, `regen-command-copies.py`,
`renumber-utils.py`, `sanitize-utils.py`, `sync-mirrors.py`, `validate-decision-tensions.py`,
`validate-requirements.py`, `validate-tasks.py`;
`shared/declarations/contract.yaml`, `shared/declarations/exclusions/`, `shared/declarations/facts/`,
`shared/declarations/facts/*.yaml`, `arc-verdict-mapping.yaml`, `flow-class-classes.yaml`,
`history-manifest-schema.yaml`, `non-disposable-review-surface.yaml`; `shared/definitions/`,
`shared/definitions/*-definitions.md`, `framework-map.md`, `non-disposable-definitions.md`,
`re-anchoring-definitions.md`, `script-interface-definitions.md`; `shared/guidelines/progress-reporting.md`,
`test-execution-efficiency.md`, `user-facing-comprehension.md`; `shared/workflow/acceptance-hardening.md`,
`feature-integration.md`;
`skills/external/database-utils/scripts/query.py`, `sdd-loop-driver/references/efficiency-model.md`,
`sdd-loop-driver/scripts/`, `sdd-loop-driver/scripts/{decomposition-check,pre-analyze-check}.py`,
`ssh-utils/SKILL.md`; `skills/internal`, `skills/internal/create-team/scripts/validate-roster.py`,
`skills/internal/{manage-constitution,manage-history}/SKILL.md`;
`.specify/agents/templates/`, `.specify/archive/`, `.specify/.gitignore`, `.specify/history/`,
`.specify/instructions.md`, `.specify/memory/`, `.specify/memory/tools/`; `.specify/scripts`, `.specify/scripts/`,
`.specify/scripts/python/`, `.specify/scripts/python/{account-clause-coverage,non-disposable-check,validate-tasks}.py`;
`.specify/shared`, `.specify/shared/`, `.specify/shared/declarations/facts/`,
`.specify/shared/declarations/facts/non-disposable-review-surface.yaml`, `.specify/shared/definitions/`,
`.specify/shared/definitions/{framework-map,non-disposable-definitions}.md`,
`.specify/shared/guidelines/{decision-tension,progress-reporting}.md`,
`.specify/shared/workflow/{execution-topology,self-improvement-workflow}.md`;
`.specify/skills/internal`, `.specify/skills/internal/manage-history/SKILL.md`;
`.specify/specs`, `.specify/specs/`,
`.specify/specs/045-sanitize-command/contracts/sanitize-findings.md`, `.specify/specs/067-*/**`,
`.specify/specs/067-*/contracts/runner-contract.md`, `.specify/specs/069*/**`,
`.specify/specs/077-*/**`, `.specify/specs/079-*/**`, `.specify/specs/080-*/`, `.specify/specs/080-*/**`,
`.specify/specs/080-humanize-run-output/requirements.md`, `.specify/specs/081-*/`, `.specify/specs/081-*/**`,
`.specify/specs/082-*/`, `.specify/specs/082-*/**`, `.specify/specs/083-*/`, `.specify/specs/083-*/**`,
`.specify/specs/084-*/`, `.specify/specs/084-*/**`,
`.specify/specs/084-harness-triple-structure/verification.md`, `.specify/specs/085-*/`,
`.specify/specs/085-sdd-temporary-goal-team/**`,
`.specify/specs/085-sdd-temporary-goal-team/contracts/{concurrency-and-worktrees,temporary-goal-team}.md`,
`.specify/specs/085-sdd-temporary-goal-team/plan.md`, `.specify/specs/086-*/`,
`.specify/specs/086-efficient-test-execution/**`,
`.specify/specs/086-efficient-test-execution/contracts/runner-contract-086.contract.md`,
`.specify/specs/087-*/`, `.specify/specs/087-arch-diagram-docs/**`, `.specify/specs/088-*/`,
`.specify/specs/088-speckit-visualization/**`, `.specify/specs/089-*/`,
`.specify/specs/089-script-interface-contract/**`,
`.specify/specs/089-script-interface-contract/contracts/mirror-projection.contract.md`,
`.specify/specs/089-script-interface-contract/{requirements,tasks,verification}.md`,
`.specify/specs/090-*/`, `.specify/specs/090-re-anchoring/**`, `.specify/state/`,
`.specify/state/092-non-disposable.md`, `.specify/teams/**`, `.specify/templates`, `.specify/templates/`,
`.specify/templates/{feature-details,instructions,tasks,verification-log}-template.md`, `.specify/.tmp/`;
`templates/commands/{history,measure,status}.md`, `templates/{constitution,instructions}-template.md`;
`tests/contract/`, `tests/contract/{test_closure_acceptance_check,test_constitution_double_landing,
test_docs_command_template,test_expression_compatibility,test_fast_fail_discipline,
test_non_disposable_contract,test_run_tests_runner_contract,test_sdd_loop_driver_gates,
test_sdd_loop_driver_reanchor}.py`.

Note: the five `.specify/memory/` anchors moved to the `.specify/` root **during this audit** (merge
`6fb8093c4`); they are now listed under Dead (rows 40–44), not here. `.specify/templates/` is alive as a
directory; the spec's retired subpath is listed under Dead.

### Archived-elsewhere (17)

Every row is a stale pre-archive literal; the preserved copy is at the same relative path under
`.specify/archive/specs/092-non-disposable/`.

| # | Literal | Anchors |
|---|---|---|
| 1 | `.specify/specs/092-non-disposable` | requirements.md:26; team/team.md:20 |
| 2 | `.specify/specs/092-non-disposable/` | requirements.md:26 |
| 3 | `.specify/specs/092-non-disposable/**` | team/team.md:20 |
| 4 | `.specify/specs/092-non-disposable/checkpoints/` | team/team.md:147 |
| 5 | `.specify/specs/092-non-disposable/checkpoints/**` | team/team.md:147 |
| 6 | `.specify/specs/092-non-disposable/coverage-baseline.txt` | plan.md:216; tasks.md:123 |
| 7 | `.specify/specs/092-non-disposable/goal/092-non-disposable/goal.md` | team/team.md:181 |
| 8 | `.specify/specs/092-non-disposable/notes/` | requirements.md:26 |
| 9 | `.specify/specs/092-non-disposable/notes/input-review-080-090.md` | requirements.md:26,399; plan.md:5; notes/measurement-corpus.md:3 |
| 10 | `.specify/specs/092-non-disposable/notes/measurement-corpus.md` | tasks.md:122 |
| 11 | `.specify/specs/092-non-disposable/notes/pre-change-measurements.md` | tasks.md:118 |
| 12 | `.specify/specs/092-non-disposable/notes/quickstart-run.md` | tasks.md:157,166,190 |
| 13 | `.specify/specs/092-non-disposable/requirements.md` | requirements.md:397 |
| 14 | `.specify/specs/092-non-disposable/tasks.md` | tasks.md:29 |
| 15 | `.specify/specs/092-non-disposable/test-evidence/` | requirements.md:246; contracts/four-stage-command.contract.md:90 |
| 16 | `.specify/specs/092-non-disposable/test-evidence/**` | team/team.md:147 |
| 17 | `.specify/specs/092-non-disposable/test-evidence/tasks-gates.txt` | tasks.md:321,322 |

### Dead (27)

| # | Literal | Anchors | Now resolves to |
|---|---|---|---|
| 18 | `.specify/specs/092-non-disposable/verification.md` | plan.md:215,322; tasks.md:42,320 | missing everywhere; never produced (T147 open) |
| 19 | `.specify/specs/092-non-disposable/test-evidence/INDEX.md` | tasks.md:326 | missing; never produced (T153 open) |
| 20 | `.specify/specs/092-non-disposable/test-evidence/repair-corpus.md` | tasks.md:268,286 | missing; never produced (T119/T137 open) |
| 21 | `.specify/specs/092-non-disposable/test-evidence/shift-092.md` | tasks.md:300,301,302,303,307 | missing; never produced (T139–T142/T146 open) |
| 22 | `.specify/specs/092-non-disposable/test-evidence/repair-*.md` | feature-ref.md:44 | missing (planned "NEW at execution time") |
| 23 | `.specify/specs/092-non-disposable/test-evidence/reporter-092-non-disposable.live.log` | team/team.md:148,251 | missing; no archive copy |
| 24 | `.specify/specs/092-non-disposable/team/092-non-disposable/runs/**` | team/team.md:147 | missing; archive holds only `team/team.md` |
| 25 | `.specify/goal/**` | team/team.md:48,269 | missing; global archive renamed to `.specify/anchoring/` (63 files) |
| 26 | `.specify/specs/088-*/efficiency-model.md` | tasks.md:278 (T129) | missing; 088 has no such file; live owner spelling is `skills/external/sdd-loop-driver/references/efficiency-model.md` |
| 27 | `.specify/specs/089-script-interface-contract/team/086-script-interface-contract/` | plan.md:413 (C3); tasks.md:281 (T132) | missing; repair landed — team now `.specify/teams/089-script-interface-contract/team.md` (`name: SDD Temporary Team 089`) |
| 28 | `.specify/specs/.archive/` | research.md:81; contracts/renumber-and-supersede.contract.md:54 | directory missing; the prefix constant remains live in `scripts/python/renumber-utils.py:59` and `scripts/python/sanitize-utils.py:317` |
| 29 | `.specify/templates/commands/` | plan.md:241; feature-ref.md:35 | missing; explicitly declared **retired** (`scripts/python/sync-mirrors.py:18-19`) |
| 30 | `.specify/skills/external/` | plan.md:379,435; requirements.md:414 | missing; explicitly the named `orphan-path` defect H1 ("a directory that never existed") |
| 31 | `.specify/.tmp/086-*` | requirements.md:414 | missing; registered exclusion (legitimate historical path) |
| 32 | `.specify/memory/sanitize/findings.json` | requirements.md:246; tasks.md:185; contracts/four-stage-command.contract.md:92 | missing; explicitly a **prohibited** evidence destination |
| 33 | `.specify/history/.work/a.txt` | plan.md:263 | missing; illustrative ignore-leg scratch (EP-008), verified ignored by `.specify/.gitignore:6` |
| 34 | `.specify/history/.work/probe` | quickstart.md:181 | missing; illustrative counterfactual |
| 35 | `.specify/.tmp/x.tmp` | plan.md:263 | missing; illustrative ignore-leg scratch (`.gitignore:30`) |
| 36 | `.specify/.tmp/probe` | quickstart.md:179; notes/quickstart-run.md:50 | missing; illustrative counterfactual |
| 37 | `.specify/.tmp/<plan>` | quickstart.md:197 | placeholder template |
| 38 | `.specify/specs/<NNN-slug>/team/team.md` | tasks.md:276 | placeholder template |
| 39 | `.specify/specs/<spec-dir>/test-evidence/` | requirements.md:246; plan.md:41; tasks.md:185; feature-ref.md:65; contracts/four-stage-command.contract.md:89 | placeholder template |
| 40 | `.specify/memory/constitution.md` | requirements.md:388; plan.md:53; feature-ref.md:48; notes/pre-change-measurements.md:47,84 | **moved mid-audit** to `.specify/constitution.md` |
| 41 | `.specify/memory/features.md` | requirements.md:295; plan.md:201,378,493; tasks.md:10 | **moved** to `.specify/features.md` |
| 42 | `.specify/memory/features/092.md` | requirements.md:295; plan.md:58,202,315,493 | **moved** to `.specify/features/092-non-disposable.md` |
| 43 | `.specify/memory/glossary.md` | requirements.md:294; plan.md:200,492; tasks.md:116; feature-ref.md:38 | **moved** to `.specify/glossary.md` |
| 44 | `.specify/memory/register.md` | requirements.md:298; plan.md:203,455,462,496 | **moved** to `.specify/register.md` |

## Broken list

`path:line -> what it now resolves to (or the missing symbol)`. Archive-relative paths are under
`.specify/archive/specs/092-non-disposable/`.

**Dead — promised artifacts never produced (9)**

1. `plan.md:215` -> `.specify/specs/092-non-disposable/verification.md` missing; no `verification.md` anywhere for 092 (090's belongs to 090)
2. `plan.md:322` -> same missing `verification.md` (P8 deliverable)
3. `tasks.md:42` -> GATE-4 reads a smoke record "in `.specify/specs/092-non-disposable/verification.md`"; file absent
4. `tasks.md:326` -> `.specify/specs/092-non-disposable/test-evidence/INDEX.md` missing; no archive copy
5. `tasks.md:268,286` -> `.specify/specs/092-non-disposable/test-evidence/repair-corpus.md` missing; no archive copy
6. `tasks.md:300-303,307` -> `.specify/specs/092-non-disposable/test-evidence/shift-092.md` missing; no archive copy
7. `feature-ref.md:44` -> `.specify/specs/092-non-disposable/test-evidence/repair-*.md` missing (planned but never written)
8. `team/team.md:148,251` -> `.specify/specs/092-non-disposable/test-evidence/reporter-092-non-disposable.live.log` missing
9. `team/team.md:147` -> `.specify/specs/092-non-disposable/team/092-non-disposable/runs/**` missing; archive keeps only `team/team.md`

**Dead — renamed / defect references (4)**

10. `team/team.md:48,269` -> `.specify/goal/**` missing; renamed to `.specify/anchoring/**` (63 files) by the 2026-11-09 goal→anchoring rename
11. `tasks.md:278` (T129) -> `.specify/specs/088-*/efficiency-model.md` missing; the live file is `skills/external/sdd-loop-driver/references/efficiency-model.md`
12. `plan.md:413`; `tasks.md:281` -> `.specify/specs/089-script-interface-contract/team/086-script-interface-contract/` missing; repair landed at `.specify/teams/089-script-interface-contract/team.md`
13. `research.md:81`; `contracts/renumber-and-supersede.contract.md:54` -> `.specify/specs/.archive/` directory missing; the `EXCLUDED_PREFIXES` constant still lives at `scripts/python/renumber-utils.py:59`

**Dead — by-design / negative / illustrative (8)**

14. `plan.md:241`; `feature-ref.md:35` -> `.specify/templates/commands/` retired by design (`scripts/python/sync-mirrors.py:18-19`)
15. `plan.md:379,435`; `requirements.md:414` -> `.specify/skills/external/` is the named defect H1, not a target
16. `requirements.md:414` -> `.specify/.tmp/086-*` registered exclusion
17. `requirements.md:246`; `tasks.md:185`; `contracts/four-stage-command.contract.md:92` -> `.specify/memory/sanitize/findings.json` prohibited destination
18. `plan.md:263` -> `.specify/history/.work/a.txt` and `.specify/.tmp/x.tmp` illustrative ignore legs
19. `quickstart.md:181`; `quickstart.md:179`; `notes/quickstart-run.md:50` -> `.specify/history/.work/probe` / `.specify/.tmp/probe` counterfactual examples
20. `quickstart.md:197`; `tasks.md:276`; `requirements.md:246` -> `<plan>` / `<NNN-slug>` / `<spec-dir>` placeholders

**Dead — moved by the anchor-layout merge (5, landed mid-audit at `6fb8093c4`)**

21. `requirements.md:388`; `plan.md:53`; `feature-ref.md:48`; `notes/pre-change-measurements.md:47,84` -> `.specify/memory/constitution.md` missing; now `.specify/constitution.md`
22. `requirements.md:295`; `plan.md:201,378,493`; `tasks.md:10` -> `.specify/memory/features.md` missing; now `.specify/features.md`
23. `requirements.md:295`; `plan.md:58,202,315,493` -> `.specify/memory/features/092.md` missing; now `.specify/features/092-non-disposable.md`
24. `requirements.md:294`; `plan.md:200,492`; `tasks.md:116`; `feature-ref.md:38` -> `.specify/memory/glossary.md` missing; now `.specify/glossary.md`
25. `requirements.md:298`; `plan.md:203,455,462,496` -> `.specify/memory/register.md` missing; now `.specify/register.md`

**Stale pre-archive literals (17 distinct, 47 occurrences, 63 total occurrences including the dead 16)**

Each resolves only under `.specify/archive/specs/092-non-disposable/`. Representative anchors:
`requirements.md:26,397,399`; `plan.md:5,216`; `tasks.md:29,118,122,123,157,166,190,321,322`;
`research.md:217`; `quickstart.md:181`; `feature-ref.md:44`; `contracts/four-stage-command.contract.md:90`;
`notes/measurement-corpus.md:3`; `team/team.md:20,147,181`. Full literal-by-literal anchors are in the
Archived-elsewhere table above.

**Live-tree downstream breaks (recorded from the ledger-target check, not archive-internal)**

26. `.specify/features.md:99` -> 092 registry row's spec-path column still `.specify/specs/092-non-disposable/requirements.md` (dead); its notes text "artifacts remain under `.specify/specs/092-non-disposable/`" is false (they are under `.specify/archive/specs/092-non-disposable/`)
27. `.specify/features/092-non-disposable.md:6` -> `Status: Planned`, contradicting registry `Relocated`; `:59,:76,:80` still carry pre-archive paths (incl. the never-existing `team/092-non-disposable/team.md`)
28. `.specify/specs/090-re-anchoring/plan.md:298` -> claims 092 artifacts live at `.specify/specs/092-non-disposable/` and are "read **in place**", contradicting the archive and `090/tasks.md:260`
29. `.specify/specs/090-re-anchoring/tasks.md:422,440,455,462,468` -> five open merged rows (T119A/T137A/T146A/T147A/T153A) still write to `.specify/specs/092-non-disposable/...`
30. `.specify/archive/specs/CONSOLIDATION-LEDGER.md:17` -> `review-G3/G8` cannot be resolved to any review record file; the ids occur only in the ledger itself and in `090/test-evidence/history-distill-batch-3.md`

## Ledger-target check

Ledger row (`.specify/archive/specs/CONSOLIDATION-LEDGER.md:17`):
`092-non-disposable | merge | absorbed into 090-re-anchoring (merge note § W3) | review-G3/G8`.

- **Target feature resolves**: `.specify/features.md:98` holds the 090 row (`Implemented`), pointing to
  `.specify/features/090-re-anchoring.md` and `.specify/specs/090-re-anchoring/requirements.md` — both alive.
- **Merged content is present**: `090/requirements.md:102` (`## Non-Disposable (092) — merged`) and `:299`
  (A–H corpus mapping); `090/tasks.md:258-260` appends T001A…T158A in the same states; 8 merged pages
  `090/contracts/nd-*.contract.md` exist; 46 `092-*` evidence files are copied into `090/test-evidence/`.
- **"merge note § W3"**: the merge note is `.specify/archive/specs/092-non-disposable/notes/refactor-anchoring-merge.md`
  (Execution waves, item 3) plus `090/test-evidence/w3-M1..M4`. There is no literal `§ W3` heading — the
  reference resolves by wave numbering, not by anchor.
- **Registry row accuracy**: status `Relocated` is consistent with a merge/archive pointer, but the row's
  spec-path column is dead and its "artifacts remain under `.specify/specs/092-non-disposable/`" note is false.
  The detail page `.specify/features/092-non-disposable.md:6` still says `Planned`.
- **Recorded but unresolved at merge time**: `090/tasks.md:264` disclosed that the `nd-*` contract pages were
  absent and all 62 green claims were `green-dangling`; they are present now, so that caveat is stale
  (a dated record, correctly not rewritten).
- **Review ids**: `review-G3/G8` are unbacked by any file (see item 30).

Conclusion: the ledger's verdict and target **resolve**, and the 090 side is substantively complete; the 092
registry row and the 090 plan's "read in place" sentence are **inaccurate**, and the review-id column is unbacked.

## Missing guards

Named guard files — all exist; **none missing**:

- `tests/contract/test_non_disposable_contract.py` (46 `test_*` functions, mutation-leg harness)
- `tests/contract/test_non_disposable_check.py` (named as the "existing guard suite" face)
- `tests/contract/test_non_disposable_seam.py`, `test_non_disposable_seam_bypass.py`
- `tests/contract/test_expression_compatibility.py`, `test_closure_acceptance_check.py`,
  `test_sdd_loop_driver_reanchor.py`, `test_run_tests_runner_contract.py`, `test_docs_command_template.py`,
  `test_fast_fail_discipline.py`, `test_constitution_double_landing.py`, `test_sdd_loop_driver_gates.py`
- Fixture corpora `tests/fixtures/non-disposable/corpus-{a1,a2,b,c,clean,d,def,e,f2,g}` exist.

**Coverage gap (not a missing file)**: no guard asserts that the declared review roots resolve on the real
tree. `tests/contract/test_non_disposable_contract.py:66` names the fact, and `:244` only checks that the
fact file exists; the engine's `--roots` exits 0 while printing `present=False`. See spot-check 3.

## Three spot-checks (implementation claims vs current tree)

1. **File** — `scripts/python/non-disposable-check.py` (plan's deterministic engine) and its
   `.specify/scripts/` mirror: **EXISTS**, 103,245 bytes each, `--version` → `non-disposable-check.py 0.0.22`.
2. **Symbol/command** — the declared CLI surface: **EXISTS**. `--help` declares exactly `--root`, `--json`,
   `--scope`, `--roots`, `--emit-categories`, `--declaration`, `-h/--help`, `--version` (C-604 eight-row
   surface), exit codes 0/1/2. `--emit-categories` prints exactly the closed eight:
   `superseded-live, multi-owner, orphan-path, renumber-live-binding, status-unreadable, false-closed-set,
   stale-constant, deferral-marker`.
3. **Behaviour surface** — `shared/declarations/facts/non-disposable-review-surface.yaml`: **FAILS**.
   `:10` claims "ten roots, all present"; `:17` declares `.specify/goal`, which is absent now
   (`--roots` → `present=False`, exit 0), while `.specify/anchoring/` (63 files) is outside the declared
   ten-root closed set. The goal→anchoring rename landed upstream without re-measuring this fact. The
   anchor-layout merge then moved `.specify/{constitution,features,glossary,register}.md` out of the declared
   `.specify/memory` root, so the four anchors are now **outside the review surface entirely** — the fact was
   not re-measured for that rename either.

## Anchor-layout rename — LANDED mid-audit (`6fb8093c4`)

The rename landed during this run; the five former references are now **dead** (Broken list items 21–25):

| Reference (now dead) | Anchor(s) | Live owner now |
|---|---|---|
| `.specify/memory/constitution.md` | requirements.md:388; plan.md:53; feature-ref.md:48; notes/pre-change-measurements.md:47,84 | `.specify/constitution.md` |
| `.specify/memory/features.md` | requirements.md:295; plan.md:201,378,493; tasks.md:10 | `.specify/features.md` |
| `.specify/memory/features/092.md` | requirements.md:295; plan.md:58,202,315,493 | `.specify/features/092-non-disposable.md` |
| `.specify/memory/glossary.md` | requirements.md:294; plan.md:200,492; tasks.md:116; feature-ref.md:38 | `.specify/glossary.md` |
| `.specify/memory/register.md` | requirements.md:298; plan.md:203,455,462,496 | `.specify/register.md` |

`.specify/memory/` and `.specify/memory/tools/` stay (the merge keeps the stores; only the five anchors left).
The same merge updated the live guard's `SEVEN_FACES` (`tests/contract/test_non_disposable_contract.py:245,246,249`)
and its detail line (`:259`) to the root spellings, so that guard is consistent again; the review-surface fact
(`non-disposable-review-surface.yaml`) was **not** updated and still misses the moved anchors (spot-check 3).

## Anomaly

**Anomaly**: (1) the audited tree moved mid-run — `564a5f5a6` → `6fb8093c4` (anchor-layout merge); all five
memory anchors moved and every finding was re-measured on the new HEAD. (2) The spec's own declared behaviour
surface is stale on the live tree — `shared/declarations/facts/non-disposable-review-surface.yaml:17` still declares
`.specify/goal` (renamed to `.specify/anchoring`; 63 files outside the closed set) and no longer covers the four
anchors moved to the `.specify/` root; the engine reports `present=False` but exits 0, and no guard asserts the real
roots resolve. No spec/source file was modified and this file is the only write.

## Verdict

**BROKEN**. The archive is complete for what was written (no artifact lost), and 137 of 181 path literals resolve,
but:

- 17 pre-archive literals (47 occurrences; 63 including dead forms) are broken links as written even though the
  objects survive in the archive;
- 7 artifacts the spec promised were never produced (`verification.md`, `test-evidence/INDEX.md`,
  `repair-corpus.md`, `shift-092.md`, `repair-*.md`, the reporter live log, the team `runs/` tree) — their producing
  rows are still open in the 090 merged slice;
- one spot-checked behaviour surface fails: the declared review roots no longer resolve (`.specify/goal` →
  `.specify/anchoring`), the moved `.specify/` anchors are outside the surface, and the guard suite does not catch it;
- 5 more literals went dead during the audit when the anchor-layout merge landed
  (`.specify/memory/{constitution,features,glossary,register}.md`, `features/092.md`);
- the ledger target resolves and the merge is substantively landed, but the 092 registry row's spec path and
  "artifacts remain" note are inaccurate, its detail page still reads `Planned`, and `review-G3/G8` are unbacked.

SPEC-AUDIT-11-DONE
