# Implement report — wp04b (094-goal-team-parallel)

Package: the follow-up fork for wp04's blocked rows **T055 / T057 / T058**, plus the
engine half of **T061** that turned the one known red green. Tree:
`/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/094-wp04b`
(branch `094-wp04b`, base `f4e9ae4c1` — master with wp01…wp05). Date: 2026-11-09.
No push, no subagents, no additional worktrees, no merge, no `--force`.

Write domain used — the dispatch's expansion: `tests/contract/test_declaration_facts.py`,
`scripts/python/goal-utils.py`, `shared/declarations/contract.yaml` (inspected, no change
needed), the handoff template surface, the wp04 test modules (read-only), plus this
package's `notes/` and `test-evidence/` outputs. Mirror projection is included per the
dispatch's `sync-mirrors` step.

## Per-row closure

| Row | Status | Evidence |
|-----|--------|----------|
| T055 | **closed** — `test_the_threshold_literal_exists_only_in_its_fact_file` scans the three surfaces the row names (the engine, driver sentences, command templates) for the *declared* threshold number, read from its fact file, in a threshold sentence; the scan is empty, and the fact file still owns the number. | `test-evidence/wp04b-T055-guard.txt` (1 passed) |
| T057 | **closed** — `test_a_fact_in_another_grammar_is_refused_at_load` drives three refusal paths and a restore control: a fact file written outside the subset grammar refuses at load (`owner-unavailable`, detail names the grammar breach); a fact registered under `yaml/v0` refuses as `declaration-invalid` naming both grammars (both consumers); a registration whose `value_domain` disagrees with what the consumer implements refuses naming both domains (both facts). The engine half pre-existed (wp05's T084/T085 `_registration_problem`); the guard proves it behaviourally instead of asserting a text copy. | `wp04b-T057-guard.txt` (1 passed) |
| T058 | **closed** — `test_registration_is_additive_and_both_consumers_are_in_scope` asserts the additive shape (`registered_facts` is the one new top-level key, appended last, one row per fact) and the consumer scope: every declared consumer exists and lives in `goal-utils.py` / `create-team`; the skill invokes both actions; `flow-class-check.py`, `run-stage.sh`, `stage-runner.sh` name neither fact. The registration pre-existed (wp03/T056). | `wp04b-T058-guard.txt` (1 passed) |
| T061 | **closed** — the engine action `handoff-ref --handoff <path>` now exists in `goal-utils.py`: `goal_slug`/`team_slug` are read from the contract's frontmatter and must each resolve to `.specify/anchoring/<slug>/goal.md` / `.specify/teams/<slug>/team.md`; an unresolvable key raises `handoff-dangling-key` (exit 2) naming the key and value; once both resolve, exactly one `handoff_ref: <repo-relative path>` line is inserted into each definition and every other line is byte-identical (idempotent on a second run). | `wp04b-T061-red-before-engine.txt` (red), `wp04b-T061-green.txt` (green) |

Rows this fork did **not** re-open: T049/T050/T056/T059/T060/T062 stay green in the
three-module and neighbourhood runs below. `shared/declarations/contract.yaml` needed no
change — both facts were already registered with `declaration-subset/v1` and their value
domains, and the T058 guard confirms the registration stayed additive.

## Test readings

TEST ENTRY: every run below went through `bash scripts/bash/run-tests.sh … -q`
(pytest-xdist defaults); no raw pytest invocation was used for evidence.

- **Red first** — the pinned guard `test_a_dangling_handoff_key_is_refused_at_creation`
  failed on `error: unrecognized option: --handoff`, 1 failed / exit 1
  (`wp04b-T061-red-before-engine.txt`).
- **Per-row greens** — T055, T057, T058, T061: 1 passed each, exit 0
  (`wp04b-T0{55,57,58}-guard.txt`, `wp04b-T061-green.txt`).
- **The three package modules** — `test_handoff_contract.py`, `test_handoff_territory.py`,
  `test_declaration_facts.py`: **16 passed**, exit 0 (`wp04b-three-modules-green.txt`).
- **wp04 neighbourhood** — the three modules plus `test_command_family.py`,
  `test_parallel_lines.py` (contract + integration), `test_team_territory.py`,
  `test_territory_containment.py`, `test_overlap_verdicts.py`: **51 passed**, exit 0
  (`wp04b-neighbourhood.txt`).
- **Engine regression (17 goal-utils-referencing modules)** — 12 failed, 562 passed,
  1 skipped. Name-level diff against a `git archive HEAD` copy of the tree: **the only
  worktree-only failure is `test_script_interface_contract.py::test_c20…`**, caused by
  the newly projected mirror file being untracked at measurement time (the checker's
  `candidate-not-collected` finding; the file is tracked by this commit). **11 failures
  are common with the baseline copy** (`--scope spec|global` closed-set drift, the
  goal-definitions rewrite budget, the run-checks roster, the nested-run report) and
  **four baseline-only failures are `.git`-absent artifacts** of the copy.
  `wp04b-engine-regression.txt`.
- **validate-tasks** — 85 rows, **0 errors**, 1 warning (the recorded forward `blockedBy`
  T043→T054); `wp04b-validate-tasks.txt`.
- **Mirrors** — `sync-mirrors.py --write` projected `scripts/python/goal-utils.py` and the
  two wp04 MISS files (`handoff-contract-template.md`, `territory-check.py`);
  `--check` then reports every layer byte-identical, exit 0;
  `regen-command-copies.py --check` exit 0 (`wp04b-mirror-check.txt`).
- **Script interface** — `goal-utils.py --version` exit 0, `handoff-ref --help` exit 0,
  `handoff-ref --bogus` exit 2 (`wp04b-script-interface.txt`).

## Artifacts delivered

- `scripts/python/goal-utils.py` — new `handoff-ref --handoff <path>` action
  (`handoff_ref()`, `_with_handoff_ref()`, `_run_handoff_action()`), its `--handoff`
  guard registration, subparser, header entry and human rendering; mirrors projected.
- `tests/contract/test_declaration_facts.py` — the three row guards above; module
  docstring now lists T055/T057/T058.
- `.specify/skills/internal/create-team/references/handoff-contract-template.md`,
  `.specify/skills/internal/create-team/scripts/territory-check.py` — wp04's pending
  mirror projection, completed here per the dispatch's sync step.

## Commits

Committed explicitly by path (never `git add -A`); one commit, no push:

- `fix(094-wp04b): close the blocked handoff rows T055/T057/T058` — the engine, the
  declaration test module, the two wp04 mirrors, this note and the `wp04b-*` evidence.

## Residual risks and disclosed boundaries

1. **The entry name is still the test's pin.** No contract clause fixes `handoff-ref`;
   the test (and now the engine) agree on it, so renaming later is a one-test plus
   one-engine edit — the same disclosure wp04 made. C-59 owns the behaviour, not the name.
2. **T055's scan is scoped to the row's three surfaces** (engine, driver sentences,
   command templates). A wider scan over all of `skills/` produced two real false
   positives at measurement time — a PlantUML how-to containing `错误率阈值` next to an IP
   address, and an `improve-skills` table whose exit code is `10` — so third-party skills
   are excluded; the create-team handoff template was checked separately and cites no
   threshold. `skills/external/sdd-loop-driver/templates/stage-team-preset.md` carries
   the packaging target `~10 tasks per package`, a different fact with its own owner;
   the guard's predicate (threshold vocabulary on the same line as the number) does not
   conflate the two.
3. **The pre-existing 11-failure set is untouched** and not attributable to this fork
   (identical node ids fail on the `git archive HEAD` copy). The `.git`-less baseline
   copy cannot produce a `git ls-files` view, which is why it shows four extra
   projection-scenario failures.
4. **`handoff-ref` ignores `--scope`** like `probe-residual`/`migrate-archive`: it
   addresses both archive layers directly and returns before scope resolution. The
   shared flag therefore appears in its `--help` without effect — the existing
   precedence trap recorded at `main()` (spec 053 research A-9), not a new one.
5. **Fast-fail accounting.** The dispatch described the known red as the
   T055/T057/T058 gap; it is in fact T061's engine gap. T055/T057/T058 were guard-only
   rows whose implementation halves had already landed in wp03/wp05, so their guards
   passed on first write — recorded rather than dressed up as a red-first cycle. No
   anomaly was patched over: the one behaviour bug found during implementation (the
   team file was probed as `goal.md`) was caught by the pinned test and fixed in the
   engine, not in the test.
