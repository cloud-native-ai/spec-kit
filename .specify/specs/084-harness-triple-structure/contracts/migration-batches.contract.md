# Contract — Migration Batches（首批名单 + 批次切分 + 每批独立可验收）

**Feature**: 084 Harness 三重结构 | **Date**: 2026-11-05
**Status of this roster**: it is the plan-side list deliverable the spec's A9 asks for. It names **what** migrates and
in **which** batch; it deliberately carries **no values** — the values land in the declarations themselves, whose
domains are owned by `contract.yaml`.

## Why this order

Batch order follows blast radius, not tidiness: a drifted threshold or closed set is already producing wrong verdicts
today (batch 1); a mapping or ordered operator table decides accept/reject, so changing it wrongly turns a gate into a
rubber stamp (batch 2); a record schema only changes the shape of what gets recorded (batch 3). Each batch is closed by
its own readings, so a stalled batch leaves the previous ones complete rather than half-migrated.

## Batch 1 — facts already duplicated across faces (drift risk exists today)

- **C-042** Batch 1 is the roster below: nine facts whose value already exists twice — once as an engine constant and
  once as prose in a carrier — so the drift this feature removes is present today rather than hypothetical.
  Each row: slug · kind · the engine side that defines it today · the carrier(s) that re-state it.

| # | `<fact-slug>` | kind | engine side | carrier side |
|---|---------------|------|-------------|--------------|
| 1 | `feedback-prompt-threshold` | threshold | `scripts/python/feedback-utils.py` | `shared/workflow/feedback-step.md` |
| 2 | `evidence-seven-states` | closed-set | `scripts/python/evidence-utils.py` | `skills/internal/collect-evidence/references/evidence-discipline.md`; `shared/guidelines/better-harness.md` § 证据纪律 item 2 |
| 3 | `evidence-lanes` | closed-set | `scripts/python/evidence-utils.py` | `shared/workflow/evidence-step.md`; `skills/internal/collect-evidence/SKILL.md` |
| 4 | `flow-class-classes` | closed-set | `scripts/python/flow-class-check.py` | `shared/definitions/flow-class-definitions.md` |
| 5 | `flow-class-basis` | closed-set | `scripts/python/flow-class-check.py` | `shared/definitions/flow-class-definitions.md` |
| 6 | `flow-class-document-types` | closed-set | `scripts/python/flow-class-check.py` | `shared/definitions/flow-class-definitions.md` |
| 7 | `flow-class-ledger-columns` | ordered-operator-table | `scripts/python/flow-class-check.py` | `shared/definitions/flow-class-definitions.md` |
| 8 | `flow-class-neutral-categories` | closed-set | `scripts/python/flow-class-check.py` | `shared/definitions/flow-class-definitions.md` |
| 9 | `success-criterion-path-values` | closed-set | `scripts/python/validate-requirements.py` **and** `scripts/python/closure-acceptance-check.py` | `shared/workflow/acceptance-hardening.md` § Closure Verdict § Input contract; `templates/commands/requirements.md`; `skills/internal/create-requirements/SKILL.md` |

Row 9 is the 081-sensitive row: the declaration becomes the value's only home, **both** inline tuples are deleted, and
the judgement prose, refusal message, exit-code meaning and member set stay byte-identical. Its closure reading includes
`tests/contract/test_requirements_checker.py` and `tests/contract/test_checker_form.py` at zero new failures and zero
diff (measured at plan time: 40 and 37 collected tests, `research.md` § R7).

- **C-043** Batch 1 is the only batch that must land before the coverage action can exit 0 on the main tree: the
  units in `C-042` are in scope by construction, and until each has a declaration the unit reads `pending` — which is a
  reading, not a failure. The exit-0 criterion therefore reads "zero `[[STR-013]]` findings", never "zero `pending`".
- **C-044** Batch 2 — mappings and ordered operator tables (they decide accept/reject). Each row names **both** sides as
  they stand today: the engine side is the constant or read point that step 3 of `C-047` replaces with a read through the
  shared entry (`C-052`…`C-059`), so no row's engine side has to be discovered by `grep` at edit time. `none` is a
  reading, not a gap in the roster: it means the row has **no** engine-side copy today, so step 3 of `C-047` creates the
  read point in the consumer the row names and `C-050`'s `note` records the correction. File:line readings are as
  measured on 2026-11-05; the constant names are the stable part, the line numbers move.

  | `<fact-slug>` | engine side (constant or read point today) | carrier side |
  |--------------|-------------------------------------------|--------------|
  | `expression-gate-faces` | `scripts/python/flow-class-check.py` — `FACES_SECTION_KEYWORD = "六面"` / `FACES_EXPECTED = 6`, the gate owner's § 六面 row-count check | `shared/workflow/expression-gates.md` |
  | `expression-stage-operator-table` | `scripts/python/flow-class-check.py` — the operator-table header tuple `required = ("阶段", GATE_ID_COLUMN, "执行算子", "对应面", "阻断级别")` | `shared/workflow/expression-gates.md` |
  | `analyze-severity-values` | `none` — no engine constant carries the severity scale; the only `severity` domain in code is `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py`'s two-value `error` / `advisory`, a different axis, so this row's read point is created at migration | `templates/commands/analyze.md`; `skills/internal/analyze-artifacts/` (`references/detection-and-severity.md`) |
  | analysis finding-channel set | `none` — the finding classes exist only in the two carriers. The nearest label set in code is `scripts/python/account-clause-coverage.py`'s `clause-uncovered` / `fr-uncovered` channels (its `{"label": …}` rows), a narrower set read there and **not** re-declared by this row | same two carriers |
  | `review-segment-sequence` | `none` — the four-segment sequence is written by the prose carriers; `skills/internal/code-review/scripts/git-delta-review.sh` owns only the code segment's four-value verdict vocabulary (`pass` / `blocked` / `not-applicable` / `not-evaluated`) and does not enumerate the sequence | `templates/review-template.md` |
  | ARC verdict mapping | `scripts/python/closure-acceptance-check.py` — `final_path_counts()` (six status buckets plus the total) and the comparison `verdict` (`"block" if blocking else "accept"`); the template's `[ARC_*]` placeholders are copied from `--json` verbatim, never recomputed | `templates/review-template.md` |
  | `self-improvement-stage-sequence` | `none` — measured: `Bootstrap` / `Operationalize` / `Optimize` appear in no `.py` and no `.sh`; the sequence exists only in the carriers | `shared/workflow/self-improvement-workflow.md`; `shared/definitions/self-improvement-definitions.md`; `skills/internal/self-improvement/` |
  | track-to-executor mapping | `none` — same measurement; no engine maps a track to an executor | same three carriers |
  | `improvement-track-values` | `none` — the improve-\* skill scripts (`skills/external/improve-skills/scripts/redline-check.py`, `skill-shape.py`) carry no track vocabulary | `skills/internal/improve-agent/`, `improve-team/`, `improve-tools/`; `skills/external/improve-docs/`, `improve-skills/` |
  | changed-asset-category mapping | `none` — no engine classifies a changed asset into a category | same five carriers |
  | `driver-stage-sequence` | `skills/external/sdd-loop-driver/scripts/loop-state.py` — the `STAGE_ARTIFACTS` key order: `requirements`, `clarify`, `plan`, `tasks`, `checklist`, `analyze`, `implement`, `review` | `skills/external/sdd-loop-driver/SKILL.md` |
  | `driver-gate-roster` | `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` — the check-name literals at its `add(findings, "<name>", …)` call sites (`dangling-id`, `blocked-by`, `missing-path`, `external-clause`, `duplicate-id`, `count-claim`), plus `STAGES` for the per-stage file requirement | same carrier |
  | `driver-completion-sentinels` | `loop-state.py` — `sentinel_literal()`, which renders `<STAGE>-DONE`, plus the `sentinel` keys in `STATUS_FIELDS` / `LOG_FIELDS` | same carrier |
  | `driver-stage-artifacts` | `loop-state.py` — `STAGE_ARTIFACTS` itself (`artifacts` / `owned_paths` / `commit_required` / `no_change_allowed` per stage), and `IMPLEMENT_CODE_PATHSPEC` for implement's code pathspec | same carrier |

- **C-045** Batch 3 — record schemas (they change evidence shape only). Same two-sided reading as `C-044`; `none` again
  means no engine-side copy exists today.

  | `<fact-slug>` | engine side (constant or read point today) | carrier side |
  |--------------|-------------------------------------------|--------------|
  | `memory-types` | `scripts/python/memory-utils.py` — `SCOPES = ("session", "knowledge")` | the memory skills (`skills/internal/memory-record/`, `memory-recall/`) |
  | `memory-retention-thresholds` | `scripts/python/record-retention.py` — `DEFAULT_GRACE_DAYS = 30` and the `STORES` roster. `memory-utils.py`'s `prune` carries no default of its own (it requires `--max-entries` / `--max-age-days`), which is why the threshold's engine side is the retention engine, not the memory store | same two skills |
  | `history-categories` | `none` — measured: the five category names are in no `.py` and no `.sh`; `scripts/python/history-utils.py` writes the record store without enumerating categories | `skills/internal/manage-history/SKILL.md` |
  | `history-manifest-schema` | `scripts/python/history-utils.py` — `_manifest_path()` (`.manifest.json`), `read_manifest()` / `write_manifest()`, and the `sessions` key set the incremental read builds | `skills/internal/manage-history/` |
  | `probe-class-values` | `scripts/python/probe-utils.py` — `_PROBE_KINDS`, `_CLASS_FIELDS`, `HANDLER_KINDS`, `HANDLER_MODES`, `LIFECYCLE_POINTS`, `BINDING_SCOPES` | `shared/definitions/probe-definitions.md` |
  | `probe-object-binding-map` | `scripts/python/probe-utils.py` — `_OBJECT_FIELDS`, `PROBE_MAP_NAME`, and the catalog heading/entry parsers (`_CATALOG_HEADING`, `_CATALOG_ENTRY_RE`) | `shared/definitions/probe-definitions.md` |
  | `quant-record-schema` | `scripts/python/exec-quant.py` — `SCHEMA_VERSION`, `PROVENANCES`, `UNIT_TYPES`, `RESOLUTIONS`, `AGENT_RESOLUTIONS`, `CONFIG_FIELDS`, `ARG_MANIFEST` | `shared/definitions/probe-definitions.md` |
  | `trigger-state-schema` | `scripts/python/trigger-utils.py` — `SCHEMA_VERSION`, `DEFAULT_CONFIG`, `ACTIONS`, `RESPONSES`, `THRESHOLD_DEFAULT` | `shared/definitions/probe-definitions.md` |
- **C-046** A batch is **independently acceptable**: closing batch k requires only batch k's rows to satisfy the
  per-fact procedure below, plus "zero new failures" on the existing gate tests. Nothing in batch k depends on batch k+1,
  and an unfinished batch k+1 MUST NOT be reported as a failure of batch k.
- **C-047** Per-fact procedure (identical for all three batches, in this order): (1) pick the value by the authority
  order owned by `shared/definitions/harness-triple-definitions.md`, recording a correction in `note` when the faces had
  already drifted; (2) write `facts/<fact-slug>.yaml`; (3) replace the engine's inline constant with a call through the
  shared read entry; (4) replace the carrier's value restatement with a pointer (`<path>#/<key-path>`); (5) fill
  `former_carriers` with every carrier that used to spell the literal; (6) run `verify` plus the batch readings below and
  record them in the evidence directory.
- **C-048** Per-batch acceptance, five readings, each mechanical: (a) every fact of the batch has exactly one declaration
  passing subset + required keys; (b) the carrier side has zero `duplicate-fact` hits for that fact; (c) the engine
  reaches the value through the shared read entry and its inline constant is gone (`grep` for the literal returns only
  the declaration); (d) `coverage` on the migrated tree reports zero `[[STR-013]]` and zero `[[STR-011]]` for the batch's
  units, while unmigrated units stay `pending` without turning red; (e) the existing gate tests show zero new failures.
- **C-049** Compatibility is bounded: while a fact is unmigrated its engine may read its inline value, but the output
  line MUST carry the `[[STR-014]]` label; once the declaration exists the inline value MUST be deleted (no double read).
  At feature closure the in-scope set has zero `pending` (`SC-002`), so the compatibility path cannot outlive this feature.
- **C-050** A fact whose faces disagree is **not** resolved by picking a side silently: the batch procedure takes the
  authority-ordered value and the declaration's `note` records which face was corrected. A batch row that cannot name
  the corrected face is incomplete, not "close enough".
- **C-051** Nothing in this contract authorises a change to a frozen gate's criteria or exit codes. If a batch row
  cannot be migrated without such a change, the row stops and returns to the spec — it does not get a local exception.

## Verification (route (b), per reading)

Every reading above is measured at implement time, not now: the declarations do not exist on this branch. Premises to
re-measure rather than inherit:

| Reading | Command shape | Premise |
|---------|---------------|---------|
| fidelity to today's faces | `grep -n "DEFAULT_THRESHOLD\|SEVEN_STATES\|LANE_NAMES\|CLASS_VALUES\|BASIS_VALUES\|FLOW_TYPE_VALUES\|REQUIRED_LEDGER_COLUMNS\|NEUTRAL_CATEGORIES\|PATH_VALUES" scripts/python/*.py` | the file:line readings in `research.md` § R5 are from this branch at `171c2ff8`; re-read before editing, they move |
| residual literals (b) | `python3 scripts/python/doc-consistency-check.py --action verify --faces duplicate --spec-dir .specify/specs/084-harness-triple-structure` | runs today (measured: duplicate pass, zero findings) and reuses `duplicate-fact`; it reads `--spec-dir` formal files, so the carriers it can judge are the spec's, not the whole repo — the whole-repo reading is the checker's own `verify` action |
| zero new failures (e) | `bash scripts/bash/run-tests.sh --names-out <file> -q` then an id-level difference against the implement-start baseline | the runner resolves `python3` (measured); the baseline is taken at implement start, not inherited from this plan |
| the 081 acceptance files are untouched | `git diff --stat 171c2ff8 -- tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py` | empty output is the pass criterion; collected counts today are 40 and 37 |
