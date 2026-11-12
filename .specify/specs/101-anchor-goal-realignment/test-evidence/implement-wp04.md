# Implement — WP-04 (T048–T060)

- **Unit**: `/speckit.implement` · **run-id**: `r20261112T064607Z-b101`
- **Feature**: `101-anchor-goal-realignment` · **Stage/package**: implement / WP-04 (T048–T060)
- **Base commit**: `9997e91bf` (checkpoint 15, WP-03)
- **Verdict**: **BLOCKED at T057 verification** in the first pass — fast-fail decision (see §4). **Resolved and completed in WP-04b** under the recorded ruling (see §8); T058–T060 executed, residue closed to zero, no definition was hand-edited.

## 1. Commands executed (rc + artifact)

| # | Command | rc | Artifact |
|---|---------|----|----------|
| T048 | live reading of 14 entry definitions + `classification.json` cross-check | 0 | `classification-2026-11-12.md`, `classification-reading-2026-11-12.txt` |
| T049 | `python3 scripts/python/goal-utils.py cleanup --check --classification .specify/specs/101-anchor-goal-realignment/classification.json --json` | 0 | `cleanup-check-2026-11-12.json` / `.stderr` (verdict `ok`; zero writes — store hashes unchanged before/after) |
| T050–T057 | `python3 scripts/python/goal-utils.py cleanup --apply --classification .specify/specs/101-anchor-goal-realignment/classification.json --json` | 0 | `cleanup-apply-2026-11-12.json` / `.stderr` (verdict `ok`) |
| target | `bash scripts/bash/run-tests.sh tests/contract/test_goal_migration.py tests/contract/test_goal_definition.py tests/contract/test_goal_writeset.py -q` | 1 | `implement-wp04-targeted-tests.txt` (3 failed / 53 passed / 1 skipped) |
| residue | deterministic measurement of the applied tree (FM/BODY attribution) | 0 | `post-apply-residue-2026-11-12.txt` |

All engine calls ran P1–P8 inside one apply; every per-phase artifact below is read from that JSON.

## 2. Executed tasks and readings

- **T048 — classification evidence**: 14 entries = **9 anchor / 3 action-goal / 2 obsolete**, matching `classification.json` and the provisional inventory; no re-classification; cross-check 14 entry dirs / 20 teams / 16 bound / 4 unbound.
- **T049 — `cleanup --check`**: rc 0, verdict `ok`, plan render only; store hashes identical before and after (zero writes).
- **T050 — P1 anchor renames + normalization**: 9 × `goal.md` → `anchor.md` (rename step byte-asserted); normalization hits A-N-1 `^# Goal:` = **9**, A-N-2 retired root = **2** (both `094-goal-team-parallel`), A-N-3 = **0**, A-N-4 = **0**; one `anchor-body-receipt.json` per entry; concept digest before == after for all 9.
- **T051 — P2 action-goal migrations**: `088-speckit-visualization`, `091-auto-git-closeout`, `draw-diagram-interactive` → `.specify/goals/<slug>/goal.md`, each with `migration-receipt.json` (`delete_policy: archive-not-delete`, source/target digests equal, mapping `101-mapping-v1`); `088`'s **2** Target statements preserved verbatim under the fixed heading and recorded in the receipt.
- **T052 — P2 obsolete archival**: `085-sdd-temporary-goal-team` (summary absent), `post-refactor-mechanism-integrity` (summary moved) → `.specify/archive/anchoring/<slug>/` with receipts; zero deletions.
- **T053 — R2**: engine `migrate` created Anchor `visualization-skill-selection`; `viz-skill-arena` now binds `anchor_slug: visualization-skill-selection` (resolves).
- **T054 — P4 summary disposition**: moved with definition (`draw-diagram-interactive`, `post-refactor-mechanism-integrity`); 3 anchor-class trees left for regeneration (`command-logic-as-classified-skills`, `session-driven-self-improvement`, `skill-layer-install-separation`).
- **T055 — P5 structural rename**: 16 teams renamed (`rename` 8 / `rename+normalize` 8), `binding-rename-receipt.json` per team; 4 unbound teams byte-identical.
- **T056 — P6 body normalization**: only declared N-rules fired; each rewrite is `{path, line, rule, before, after}` in the team receipt. The single Anchor-only mode pointer (`/speckit.goal targets --add`) was rewritten to `/speckit.anchor` (N-7 → C6 team hit 0).
- **T057 — P7 dispositions**: 6 × R3 `apply` (`lifecycle_state: archived` + binding line removed + `disposition-receipt.json`), plus R2 `viz-skill-arena` `apply` (Anchor created). `091-auto-git-closeout` acted only `binding line removed` (already archived). No `already-satisfied` rows.
- **P8 engine self-checks** (all `ok`): `anchor-store-purity`, `bindings-resolve`, `receipts-complete`, `orphan-summary`.

## 3. Not executed

- **T058** (regenerate 3 anchor summaries via the existing summary flow), **T059** (P8 evidence + per-team `run-checks`), **T060** (second apply idempotency) — halted at the decision point below. `cleanup --check` was not re-run after apply and a second `--apply` was not executed, because the halt precedes them.

## 4. Blocking finding (fast-fail: decision, not correction)

The applied tree still carries retired-token / stale-path residue that **the declared normalization mechanism (C-46, body-scoped N-1…N-7) cannot reach**, while the feature's own guards require it gone. Measurements: `post-apply-residue-2026-11-12.txt`.

| Class | Count | Where | Why the mechanism cannot reach it |
|-------|------:|-------|-----------------------------------|
| A. retired key `goal_slug` | **2 lines** | `/storage/project/cloud-native-ai/spec-kit/.specify/teams/draw-diagram-interactive/team.md:8` (inside the `goal: >` folded scalar); `.specify/teams/command-logic-as-classified-skills/team.md:72` (inside a `non_path` entry) | both are **frontmatter prose**; N-1 is declared "in body text", and `_map_team_body` only maps text after the `---…---` block |
| B. references to a `goal.md` that no longer exists | **15 lines / 9 teams** (6 FM + 9 BODY) | e.g. `.specify/teams/090-re-anchoring/team.md:137`, `…/094-goal-team-parallel/team.md:136`, `…/skill-layer-install-separation/team.md:124` | the live text already used `.specify/anchoring/<slug>/goal.md`; N-2's match is `.specify/goal/<slug>/goal.md` only, so the file-name half of the mapping never fired after P1/P2 renamed/moved those files |
| C. retired delivery path | **5 lines** | `config.summary.delivery_dir: .specify/goal/<slug>/summary/` in `command-logic-as-classified-skills`, `draw-two-layer-structure`, `post-refactor-mechanism-integrity`, `session-driven-self-improvement`, `skill-layer-install-separation` | N-3 is body-scoped; the frontmatter `delivery_dir` line is never read by the team mapper |

Why this blocks:

- **FR-066 / T066** turns red on class A: "任一活团队定义（frontmatter 或正文…）仍含 `goal_slug`".
- **FR-058** is violated by class C: "任何活页面 MUST NOT 继续把 `.specify/goal/<slug>/summary/` 当交付路径" (all five files are live team definitions, and `lifecycle_state: archived` is not an exemption per FR-061).
- **Class B** leaves 9 live definitions pointing at definition files that P1/P2 renamed or moved (the paths are dead); no FR/guard pattern currently enumerates this form, so it would pass silently.

Adjudication: repairing A/B/C requires either (i) extending the C-46/N-2 match surface (engine + contract amendment, WP-01/WP-02 territory) to the whole team definition — including the anchored path form and the frontmatter `delivery_dir` — or (ii) a recorded decision that these surfaces are out of scope. Both are choices between readings, not a local repair; hand-editing `team.md` is forbidden by the dispatch (engine is the sole definition writer) and would falsify the C-45 byte assertion. **No hand-edit was made.**

## 5. Targeted tests vs E2 baseline (`suite-baseline-entry.txt`)

3 failed / 53 passed / 1 skipped. Name-level comparison:

- `tests/contract/test_goal_migration.py::TestLiveSurfacesAreMigrated::test_no_live_face_file_retains_the_old_path` — **present as FAILED in the E2 baseline** (known red).
- `tests/contract/test_goal_writeset.py::TestInvariantGroups::test_mapping_declares_the_definition_is_not_writable_by_the_refresh`
- `tests/contract/test_goal_writeset.py::TestInvariantGroups::test_mapping_names_each_invariant_group[goal.md]`
  — **not in the E2 baseline**; **pre-existing at base `9997e91bf`**: both assert `goal.md` in `skills/internal/create-team/references/summary-mapping.md`, which WP-03 (`5a091f693`) rewrote to `anchor.md`. That file is unchanged by WP-04 (`git status` shows no non-`.specify/` edits). These two reds are a WP-03/T065-era follow-up, disclosed here and not attributed to this package.

## 6. Post-apply readings (read-only, after the halt decision)

- **Re-run `cleanup --check`** (`cleanup-check-after-apply-2026-11-12.json`): rc 0, verdict `ok`; counts `already-archived: 2`, `already-migrated: 3`, `already-normalized: 9`; teams `already-normalized: 16`; dispositions `already-satisfied: 7`. The engine therefore believes the world is fully converged — the residue in §4 is outside its model, so a second `--apply` would be a no-op and would not repair it.
- **Per-team `run-checks`** (`run-checks-wp04-2026-11-12.txt`, 20 teams): 6 bound teams `ok/false/0` (086, 089, 090, 094, command-logic, viz-skill-arena); 10 teams `no-goal-definition/false/0` (6 R3 + 4 unbound); **4 bound teams `goal-terminal/true/5`** (087-arch-diagram-docs, draw-two-layer-structure, session-driven-self-improvement, skill-layer-install-separation).

### SC-005 deviations (pre-existing, not caused by the apply)

1. `goal_slug` count in live team definitions is **2**, SC-005 requires **0** — the §4 class A residue.
2. SC-005 requires every still-bound team to read `ok/false/0`, but four still-bound teams read `goal-terminal/true/5` because their Anchors were already `achieved` at classification time (087, draw-two-layer, session-driven, skill-layer are the four achieved anchor-class entries). `run-checks` derives that verdict from the Anchor's lifecycle, which P1 did not change, so the reading is baseline behaviour; SC-005's expectation does not cover achieved-but-still-bound teams.

## 7. Disclosures

- No definition (`anchor.md` / `goal.md` / `team.md`) was edited by hand; the engine is the only writer of record in this run.
- No `git mv` / `rm` was used for definitions; every moved/archived entry carries a receipt.
- Protected dated records were not touched (`runs/**`, `.specify/archive/**` pre-existing, `.specify/history/**`, `docs/notes/**`, dated spec dirs, `smoke-081.txt`, `.specify/.specify/`).
- No commit was made and nothing was pushed.

## 8. WP-04b — decision resolved, T058–T060 executed

- **Unit**: `/speckit.implement` · **run-id**: `r20261112T064607Z-b101` · **Package**: implement / WP-04b
- **Ruling applied**: (i) extend the C-46 normalization surface in `scripts/python/goal-utils.py` with **N-8** (frontmatter `goal_slug` → `anchor_slug`), **N-9** (definition-file refs in both `.specify/goal/<slug>/goal.md` and already-anchored `.specify/anchoring/<slug>/goal.md` forms → `anchor.md`), **N-10** (frontmatter `delivery_dir` `.specify/goal/<slug>/summary/` → `.specify/anchoring/<slug>/summary/`); (ii) correct SC-005 for achieved-but-still-bound teams; (iii) complete T058–T060. No lifecycle change; no definition edited by hand.

### 8.1 Residue closure readings (2 / 15 / 5 → 0 / 0 / 0)

| Step | Command | rc | Artifact |
|------|---------|----|----------|
| check (pre-apply) | `python3 scripts/python/goal-utils.py cleanup --check --classification .specify/specs/101-anchor-goal-realignment/classification.json --json` | 0 | `cleanup-check-wp04b-2026-11-12.json` |
| apply | same with `--apply` | 0 | `cleanup-apply-wp04b-2026-11-12.json` (verdict `ok`, 4/4 self-checks) |
| check (post-apply) | same with `--check` | 0 | `cleanup-check-after-apply-wp04b-2026-11-12.json` (`ok`) |
| residue re-measure | FM/BODY attribution scan over 20 `team.md` | 0 | `post-apply-residue-wp04b-2026-11-12.txt` → `{A_goal_slug: 0, B_stale_definition_ref: 0, C_retired_delivery_dir: 0}` |
| residue re-measure after T058 | same scan (class B excludes the live `.specify/goals/` store) | 0 | `post-apply-residue-wp04b-t058-2026-11-12.txt` → `0 / 0 / 0` |

Per-line receipts: every rewritten team carries `binding-rename-receipt.json` with `{path, line, rule, before, after}` rows (`N-8` 2 rows, `N-9` 15 rows, `N-10` 5 rows). Purity/bindings/receipts/orphan-summary all `ok`.

### 8.2 SC-005 correction

`requirements.md` / `plan.md` / `contracts/migration-cleanup.contract.md` now state two verdict bands: non-achieved bound teams read `ok` / `false` / `0`; a bound team whose Anchor is already `achieved` reads `goal-terminal` / `true` / `5` (087-arch-diagram-docs, draw-two-layer-structure, session-driven-self-improvement, skill-layer-install-separation). The reading follows unchanged Anchor lifecycle; the rebaseline/PLAN-EDIT records are in `notes/wp04-decision-resolution.md`.

### 8.3 T058 — three anchor summaries regenerated through the existing summary flow

Pipeline per slug (no hand-edit of definitions; every enrichment step recorded in the form's `inferred_fields`):

1. `python3 skills/internal/create-team/scripts/build-summary-input.py --goal <slug> --repo-root . --json` → `data/project-input.yaml` + `roster.md` (`t058-build-<slug>.json`).
2. Traceable enrichment merge from the prior committed form + the live `anchor.md` (full criterion/Target names, phase names, item actual dates/owners/deps, milestone anchor/date/evidence) → 33 changes (command-logic) / 1 (session-driven) / 6 + 5 phase names + 4 source normalizations (skill-layer), each appended to `inferred_fields` (`t058-form-enrichment.json`).
3. `project-db.py --load` (rebuild; `--update` is forbidden by `summary-mapping.md` §10) → `t058-db-load-<slug>.json`; `--check` ok.
4. `progress-engine.py --baseline <D0>` → `data/engine-out.json` (`t058-engine-<slug>.txt`).
5. `validate-project-input.py --emit-json` → `data/input-validation.json`; `project-db.py --export-json` where `data/engine-input.json` was retained.
6. Author `summary.md` (5-layer structure, Anchor terminology, zero retired paths), rewrite `assets/wbs.puml`, render `wbs.svg`/`wbs.png`.
7. Gate: `check-coherence.py` FAIL=0 on all three (one WARN on command-logic: CG-ID `123`, the literal contract-test count inside an item name — disclosed false positive); `verify-chart-data.py` “全部通过” on all three.

Engine readings (baseline = generation date):

| slug | baseline | phases | work items | status | milestones | people coverage | closure |
|------|----------|-------:|-----------:|--------|-----------:|-----------------|---------|
| command-logic-as-classified-skills | 2026-10-12 | 5 (all completed, 100%) | 5 (all completed; actual 2026-10-09 / 2026-10-12) | completed 10 / 0 / 0 | 1/1 achieved (2026-10-12, anchored TI-0005) | 5/11 = 45.5% | 5 − 0 − 0 = 5 |
| session-driven-self-improvement | 2026-10-08 | 5 (unknown) | 5 (unknown, no dates) | unknown 10 | 0/0/0, 2 unknown-schedule | 0/12 = 0.0% | 5 − 0 − 0 = 5 |
| skill-layer-install-separation | 2026-10-11 | 5 (all completed) | 6 (all completed) | completed 11 / 0 / 0 | 0/0/0, 6 unknown-schedule | 0/17 = 0.0% | 6 − 0 − 0 = 6 |

No gantt rendered in any tree (`has_planned_dates: false`); milestone views not standalone (no date anchors / below the count threshold).

Content deltas (disclosed, not silently dropped): command-logic no longer derives the S-layer work item `TIX-d3aa82b0` nor the four feature rows `F-001..F-004` — their only provenance was the git-ignored `.specify/teams/.work/.../progress.md`, which the tracked form does not ingest; the S-layer remainder was completed by `skill-layer-install-separation` and is recorded in that anchor's own summary. Builder residuals left untouched (WP-01 territory) and disclosed: the `targets.goal_slug` key in two forms, `roster.md`'s “Goal roster” heading, and the builder-emitted legacy milestone source (normalized in the skill-layer form with provenance, not in the builder).

### 8.4 T059 — P8 self-checks + per-team `run-checks`

- P8: `anchor-store-purity`, `bindings-resolve`, `receipts-complete`, `orphan-summary` = all `ok` (in `cleanup-check-after-apply-wp04b-2026-11-12.json`).
- `run-checks` for 20 teams (`t059-run-checks-wp04b-2026-11-12.json`): **6** `ok/false/0` (086, 089, 090, 094, command-logic, viz-skill-arena); **4** `goal-terminal/true/5` (087, draw-two-layer, session-driven, skill-layer); **10** `no-goal-definition/false/0`.

### 8.5 T060 — second-apply idempotency

`cleanup-apply-2-wp04b-2026-11-12.json`: same `--apply`, **0 non-noop decisions**, counts `already-archived 2 / already-migrated 3 / already-normalized 9`, dispositions `already-satisfied 7`. A verification third apply (`t060-apply3-wp04b-2026-11-12.json`) over a 185-file SHA-256 manifest changed **0 paths** (`t060-idempotency-wp04b-2026-11-12.json`: `hashes_identical: true`).

### 8.6 Targeted tests and wrap-up engines

- `bash scripts/bash/run-tests.sh tests/contract/test_goal_migration.py tests/contract/test_goal_definition.py tests/contract/test_goal_writeset.py tests/contract/test_run_checks.py -q` → **4 failed / 85 passed / 1 skipped** (`implement-wp04b-targeted-tests.txt`). Name-level: `test_goal_migration…no_live_face_file_retains_the_old_path` and `test_run_checks…test_c1_the_action_exists_and_the_roster_grew_by_exactly_one` are both in the recorded baseline red list (`suite-baseline-entry.txt`); the two `test_goal_writeset` invariant-group tests are pre-existing at base `9997e91bf` because WP-03 (`5a091f693`) rewrote `summary-mapping.md` to `anchor.md` (that file is unmodified in this package). No new failure outside the baseline.
- Wrap-up engines (`wrap-up-engines-wp04b-2026-11-12.json`), all on `(skill:implement-feature, r20261112T064607Z-b101)`: `run-determination.py determine` → persisted (`…20261112T121621Z…`), four axes `not_evaluated` (sources unavailable), `qualified`; `exec-quant.py collect` → one record; `feedback-utils.py record` → `20261112T121643Z-skill-implement-feature`, `count_since_submission` 483, `should_prompt` true. Each engine re-run reports `duplicate: true` / “no second row written” — dedupe confirmed on the real run id; no synthetic id was invented and the review text lives in the feedback record and this evidence.
- Mirror sync: `python3 scripts/python/sync-mirrors.py --write` then `--check` → rc 0, all mirrors byte-identical (including `scripts/ == .specify/scripts/`, 129 files).

### 8.7 Disclosures (WP-04b)

- No definition was hand-edited; the engine remained the only writer for team definitions and every moved/archived entry carries a receipt.
- Protected dated records untouched (`runs/**`, pre-existing `.specify/archive/**`, `.specify/history/**`, `docs/notes/**`, dated spec dirs, `smoke-081.txt`, `.specify/.specify/`).
- Temp scratch confined to `.specify/.tmp/`; no commit, no push in this package's execution (commit made only at stage integration).
