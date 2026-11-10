# Phase 0 Research — 096-sdd-observer-agent

**Measured**: 2026-11-10, worktree `096-sdd-observer-agent` @ `4494963a8`, CPython 3.11.11, `git version 2.43.5`, `nproc=192`.
Every measurement below was taken during this plan run; commands and their output records live in `test-evidence/plan-baseline-suites.txt`, `test-evidence/plan-gates-baseline.txt` and `test-evidence/plan-mirror-baseline.txt`.

## R-01 — The driver skill has no observer carrier yet, and its H2 set is pinned

Measured: no `observer` token exists in `skills/external/sdd-loop-driver/SKILL.md`; the state-spine program lives in `references/stage-prompts.md` § Stall Handling & State Spine, which names the spine fields but nowhere an observer record section.

Measured constraint: `tests/contract/test_sdd_loop_driver_skill.py` pins the SKILL.md H2 list (`PINNED_H2_SECTIONS`, 14 entries, `test_c3_skill_md_section_set`) and pins nine mirrored files (`MIRROR_FILES`). Adding the observer section as one new H2 therefore requires one **deliberate pin update** in that module (the established form used by 063/070) plus the new reference in `MIRROR_FILES`.

Decision: the observer lifecycle owner is one new SKILL.md H2 (`## SDD Observer（观察者：启动、记录节与收束）`) plus one new reference `references/observer-lifecycle.md`; `references/stage-prompts.md` § 状态脊 gains one pointer line, not a second definition.

## R-02 — The runner already writes machine-readable stage evidence

Measured in `skills/external/sdd-loop-driver/scripts/stage-runner.sh`:
- `pid-<line>-<stage>`: `pid=<n> start=<token> at=<epoch> line=… stage=… event=pid` (line 222)
- `status-<line>-<stage>`: `exit=<rc> at=<epoch> sentinel=<0|1> line=… stage=… event=status …` (line 350)
- `heartbeat-<line>-<stage>`: `at=<epoch> … event=heartbeat` (line 223)
- `log-<line>-<stage>.log`: completion sentinel is the last non-empty line (`<STAGE>-DONE`), anomaly is a last-line `ANOMALY:` (stage-prompts.md § Independent Verification)

Decision: `stage-start` / `stage-end` / `stage-verdict` / `anomaly` / `dispatch` / `retry` are derived from this quartet's envelopes, never from prose. No new file format is introduced.

## R-03 — The visibility triplet and its label convention already exist

Measured: `shared/definitions/subagent-definitions.md` § External Dispatch Visibility Contract point 3 defines `<label>.live.log` / `<label>.jsonl` / `<label>.status`; point 5 fixes the three-segment label convention. `scripts/python/status-digest.py` compiles the convention as `SUPERVISION_LABEL_PATTERN = ^[A-Za-z0-9][A-Za-z0-9._-]*--[A-Za-z0-9._-]+--[A-Za-z0-9._-]+$` and reads `--sub-flow <label>=<triplet-dir>`.

Decision: the observer execution label is `<line_id>--<run_stamp>--observer` — the existing three-segment convention, no fourth segment and no new pattern. Journal entries reference the triplet by runtime pointer; they never copy its content.

## R-04 — The shipped-agent mirror and the fast-fail preset enumeration are pinned

Measured: `sync-mirrors.py` `MIRROR_PAIRS` maps `agents` → `.specify/agents/templates`; `tests/contract/test_fast_fail_discipline.py` `FACTORY_PRESETS` enumerates **17** `agents/*.agent.md` files, asserts the glob equals that tuple (`test_i10`), asserts each carries the byte-identical fast-fail clause, and asserts each has a per-tool rendered copy in four `AGENT_TREES` (`test_i11`, bounded count 19 = 17 + 2 authoring texts).

Measured: `specify render-agents --help` accepts `--ai` over `qoder`, `claude`, `copilot`, `opencode` (render-only entry; delegates to the same pipeline `specify init` uses).

Decision: adding `agents/sdd-observer.agent.md` requires (a) the byte-identical fast-fail clause block, (b) a deliberate `FACTORY_PRESETS` update 17 → 18 (and the bounded count 19 → 20), (c) `sync-mirrors.py --write --only agents`, and (d) `specify render-agents --ai <t>` for the four render tools.

## R-05 — The declaration layer needs a new fact file, and contract.yaml registration is deliberately NOT touched

Measured: `shared/declarations/contract.yaml` owns `fact_kinds` (`threshold` / `closed-set` / `ordered-operator-table` / `mapping` / `record-schema`), `required_fact_keys` and two registration mechanisms (093 top-level keys; 094 `registered_facts` list). `scripts/python/harness-triple-check.py` discovers fact files by directory listing and validates required keys, kind and slug/stem agreement; registration is not a precondition for reading.

Measured constraint: `tests/contract/test_declaration_facts.py` line 452 asserts the contract key set is exactly pre-existing keys ∪ `{registered_facts}` ∪ the eight 093 keys, and line 461 asserts the `registered_facts` rows are exactly the two 094 slugs. Either registration form would force an edit to that closed-set assertion.

Decision: `shared/declarations/facts/journal-format.yaml` (`kind: record-schema`) is added **without** touching `contract.yaml`; the engine reads it through `scripts/python/declaration_reader.py` (which is also the completeness read-point token the harness checker looks for). This keeps the 094 C-86 closed-set pin intact and introduces no second registration mechanism.

## R-06 — The script interface contract has one helper both halves already use

Measured: `scripts/python/record-retention.py` (lines 1141–1162) imports `configure_parser` / `guard_argv` from `script_interface_cli.py`, with an ImportError fallback so a copied engine still runs; `scripts/python/script_interface_cli.py` resolves `<script-name> <version>` from the nearest `pyproject.toml` at run time.

Decision: the new engine follows the same wiring: `guard_argv(argv, declared=[...])` before any action; `--version` and `--help` answer with zero side effects; undeclared options exit non-zero before the action.

## R-07 — The state spine is prose today; the observer record section must be a fixed shape

Measured: `references/stage-prompts.md` § 状态脊 lists the spine's fields (U0 declaration, line label, current stage, attempts, breakpoint verdict, evidence pointers, stall state, watch fields) as bullet prose. The clarified requirements pin the observer record section's keys (`state` ∈ `started|failed|disabled|closed`, instance, execution label, reason) and its writer (the driver, append-only).

Decision: the observer record section is a fixed-key markdown section owned by the new SKILL.md H2; the journal engine reads only that section plus two narrow prose grammars (`## Stage Record — <stage>` + `- outcome: <value>`; `卡死状态` = `stalled`; `attempts: <n>`), all of which the driver already writes or is instructed to keep. Unparseable prose yields **no event** (never an inferred one).

## R-08 — The digest boundary can be measured without editing the digest

Measured: `scripts/python/status-digest.py` contains no `observer` / `journal` token; its supervision projection consumes the existing `--sub-flow LABEL=TRIPLET_DIR` form and the three-suffix triplet. Its three actions and exit codes are contract-owned (C-41/C-45).

Decision: this feature does not modify `status-digest.py`. SC-006's zero-delta evidence is (a) a field-set baseline captured before the first implementation commit, stored under `test-evidence/`, (b) a contract test asserting the digest source carries no observer-specific token, and (c) the driver using only the existing `--sub-flow` semantics.

## R-09 — `overlap-check` on a freshly copied plan template is polluted by template examples

Measured: `overlap-check.py --spec-dir … --repo .` returns `decision=overlap`, 55 overlaps, and its `current_paths` include `templates/commands/x.md` and `scripts/python/doc-consistency-check.py` — both are **example paths inside the copied plan template**, not deliverables of this feature. All reported relations are `same-path` against completed lines or `nested-path` against broad directories.

Decision: `feature-ref.md` § Overlap adjudication records the real file-level delivery surface and adjudicates every reported relation as (a) template-example artifact, (b) requirements-side citation, or (c) framework-wide reference; no active line shares a delivered file. The raw reading stays in `test-evidence/plan-gates-baseline.txt` as the measurement, not as the verdict.

## R-10 — The feature registry has no 096 row

Measured: `.specify/features.md` header says `Total Features: 89`; the highest row is 094; no `096` or `sdd-observer` row exists. `.specify/features/` has no `096.md`.

Decision: Feature Integration creates the row and the detail page and lands status `Planned` (never `Implemented`), and raises the header count to 90.

## R-11 — Gate baselines measured before this plan's artifacts land

Measured (`test-evidence/plan-gates-baseline.txt`):
- `validate-requirements.py` → `0 error(s), 0 warning(s)`, 254 lines / 30 definition rows / 3 shared strings
- `decomposition-check.py --mode plan` → `{"decision": "proceed", "fr_count": 23}` (ceiling 120)
- `overlap-check.py` → see R-09
Measured (`test-evidence/plan-baseline-suites.txt`): `tests/contract/test_sdd_loop_driver_skill.py` → `25 passed`; `test_fast_fail_discipline.py -k "i10 or i11"` → `2 passed`; mirror `--check` → all pairs `ok`, exit 0 (`test-evidence/plan-mirror-baseline.txt`).

Decision: every implement-time criterion is **no NEW failure / no NEW drift** against these readings, never an absolute "all green" that predates the feature.

## R-12 — `journal` is a new name in the runtime tree

Measured: `grep -rl journal` over the tree (excluding this spec and the worktree temp dir) hits only `.specify/glossary.md` (the three clarify-registered terms) and two feedback records. No `journal` engine, command, or skill exists.

Decision: the new names are `journal.md` (STR-001), `sdd-observer` (STR-002), `observer-gap` (STR-003) plus `scripts/python/journal-utils.py` (engine) and `references/observer-lifecycle.md` (driver reference). Naming follows the existing siblings (`memory-utils.py`, `history-utils.py`, `feedback-utils.py`).

## R-13 — The journal engine's single-writer protocol needs no second file

Measured: the spec directory is a plain directory; no existing lock convention exists there. `fcntl` is available in the stdlib on this host; the framework's documented platforms are Linux/macOS.

Decision: the single-writer protocol is a non-blocking `flock` on `journal.md` itself (no lock file, no second store). A second concurrent writer exits `3` with the label `concurrent-writer-refused`. This keeps the observer's write surface exactly "journal + own execution artifacts" (FR-016).

## R-14 — The same-author detection gate does not fire for this plan run

Measured condition: `requirements.md` and its clarify addendum were authored in earlier stage sessions (recorded in the state spine's stage records), not by this session. The gate (`shared/workflow/objective-analysis-gate.md`) does not fire when the artifacts predate the session.

Decision: the Constitution Check and the Post-Generation Quality Gate are performed directly; the plan records this condition and does not claim a delegated review it did not run.
