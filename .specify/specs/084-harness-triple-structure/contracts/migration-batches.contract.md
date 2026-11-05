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
| 9 | `success-criterion-path-values` | closed-set | `scripts/python/validate-requirements.py` **and** `scripts/python/closure-acceptance-check.py` | `shared/workflow/acceptance-hardening.md` § Closure Verdict § Input contract; `templates/commands/requirements.md`; `skills/internal/create-requirements/SKILL.md`（producing carrier that never restated the value; 069a byte-frozen, not pointed） |

Row 9 is the 081-sensitive row: the declaration becomes the value's only home, **both** inline tuples are deleted, and
the judgement prose, refusal message, exit-code meaning and member set stay byte-identical. Its closure reading includes
`tests/contract/test_requirements_checker.py` and `tests/contract/test_checker_form.py` at zero new failures and zero
diff (measured at plan time: 40 and 37 collected tests, `research.md` § R7).

- **C-043** Batch 1 is the only batch that must land before the coverage action can exit 0 on the main tree: the
  units in `C-042` are in scope by construction, and until each has a declaration the unit reads `pending` — which is a
  reading, not a failure. The exit-0 criterion therefore reads "zero `[[STR-013]]` findings", never "zero `pending`".
- **C-044** Batch 2 — mappings and ordered operator tables (they decide accept/reject). Each row names **both** sides as
  they stand today: the engine side is the constant or read point that step 3 of `C-047` replaces with a read through the
  shared entry (`C-052`…`C-059`), so no row's engine side has to be discovered by `grep` at edit time. **Every row in
  this table has a live engine side today** — that is now a membership condition of the roster, not a coincidence: a fact
  with no engine read point today fails FR-006 (i) on the tree and is not in scope (it is recorded in § Facts outside the
  roster (`no-machine-fact`) below, never migrated for symmetry). File:line readings are as measured on 2026-11-05; the
  constant names are the stable part, the line numbers move.

  | `<fact-slug>` | engine side (constant or read point today) | carrier side |
  |--------------|-------------------------------------------|--------------|
  | `expression-gate-faces` | `scripts/python/flow-class-check.py` — `FACES_SECTION_KEYWORD = "六面"` / `FACES_EXPECTED = 6`, the gate owner's § 六面 row-count check | `shared/workflow/expression-gates.md` |
  | `expression-stage-operator-table` | `scripts/python/flow-class-check.py` — the operator-table header tuple `required = ("阶段", GATE_ID_COLUMN, "执行算子", "对应面", "阻断级别")` | `shared/workflow/expression-gates.md` |
  | ARC verdict mapping | `scripts/python/closure-acceptance-check.py` — `final_path_counts()` (six status buckets plus the total) and the comparison `verdict` (`"block" if blocking else "accept"`); the template's `[ARC_*]` placeholders are copied from `--json` verbatim, never recomputed | `templates/review-template.md`; `templates/commands/review.md` § 2.4 carrier slot |
  | `driver-stage-sequence` | `skills/external/sdd-loop-driver/scripts/loop-state.py` — the `STAGE_ARTIFACTS` key order: `requirements`, `clarify`, `plan`, `tasks`, `checklist`, `analyze`, `implement`, `review` | `skills/external/sdd-loop-driver/SKILL.md` |
  | `driver-gate-roster` | `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` — the check-name literals at its `add(findings, "<name>", …)` call sites (`dangling-id`, `blocked-by`, `missing-path`, `external-clause`, `duplicate-id`, `count-claim`), plus `STAGES` for the per-stage file requirement | same carrier |
  | `driver-completion-sentinels` | `loop-state.py` — `sentinel_literal()`, which renders `<STAGE>-DONE`, plus the `sentinel` keys in `STATUS_FIELDS` / `LOG_FIELDS` | same carrier |
  | `driver-stage-artifacts` | `loop-state.py` — `STAGE_ARTIFACTS` itself (`artifacts` / `owned_paths` / `commit_required` / `no_change_allowed` per stage), and `IMPLEMENT_CODE_PATHSPEC` for implement's code pathspec | same carrier |

- **C-045** Batch 3 — record schemas (they change evidence shape only). Same two-sided reading as `C-044` and the same
  membership condition: every row here has a live engine side today; a record fact that measured `none` on 2026-11-05 is
  recorded in § Facts outside the roster instead of being migrated.

  | `<fact-slug>` | engine side (constant or read point today) | carrier side |
  |--------------|-------------------------------------------|--------------|
  | `memory-types` | `scripts/python/memory-utils.py` — `SCOPES = ("session", "knowledge")` | the memory skills (`skills/internal/memory-record/`, `memory-recall/`) |
  | `memory-retention-thresholds` | `scripts/python/record-retention.py` — `DEFAULT_GRACE_DAYS = 30` and the `STORES` roster. `memory-utils.py`'s `prune` carries no default of its own (it requires `--max-entries` / `--max-age-days`), which is why the threshold's engine side is the retention engine, not the memory store | same two skills |
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

## Facts outside the roster — `no-machine-fact`（路径 A，2026-11-05）

**What this section is.** The eight facts below were in the `C-044` / `C-045` tables until 2026-11-05. They left the
roster, and this table is where they are recorded. It is not a clause — the clause count stays 59 (`C-001`…`C-059`), and
nothing here adds a value, a domain or a ninth reason.

**Why they left — the reason is `no-machine-fact`（[[STR-006]]）.** FR-006 (i) is evaluated **on today's tree**: 「存在一个
确定性引擎，其判决结果随该取值改变而改变」, and FR-006's own disposition clause reads 「任一不成立即留在原处」. Each row below
measured `none` — no deterministic engine's judgement changes when the value changes. The competing reading ("the read point
is created during migration") is explicitly **not** available to this feature: it would make the criterion vacuous, since
the migration would manufacture its own justification — precisely the mechanism the clarify narrowing A2 removed
(`requirements.md` § Assumptions A2). Authority for the adjudication:
`test-evidence/analyze-report-round2-2026-11-05.md` § R2-02 (HIGH) plus the user's path-A decision of 2026-11-05 recorded in
`.specify/state/084-harness-triple-structure.md` § 用户裁定. All eight keep their carriers as they are: these facts were
never two-faced with an engine, so no pointer is created and no literal is deleted.

| `<fact-slug>` | batch | unit (the candidate carrier whose roster row drops) | carrier side (keeps the literal) | anchor (in-tree evidence of no engine read point) |
|---------------|-------|--------------------------------------------|----------------------------------|---------------------------------------------------|
| `analyze-severity-values` | 2 | `templates/commands/analyze.md`; `skills/internal/analyze-artifacts/SKILL.md` | `skills/internal/analyze-artifacts/references/detection-and-severity.md` § Severity assignment; the severity column of `templates/commands/analyze.md` § Wrap-up | no `.py` carries the severity scale: `grep -rn "CRITICAL\|severity" scripts/python/*.py` returns verdict-producing consumers only, and `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py`'s two-value `error` / `advisory` is a different axis, not this scale |
| analysis finding-channel set | 2 | same two units | same carriers (§ The eight passes) | the finding classes exist only in the two carriers; the nearest label set in code is `scripts/python/account-clause-coverage.py`'s `clause-uncovered` / `fr-uncovered` channels (`{"label": …}` rows), a **narrower** set read there and not this row's |
| `review-segment-sequence` | 2 | `templates/commands/review.md`; `skills/internal/review-sdd-process/SKILL.md`（两个单元仍 in-scope，理由见下：ARC 判定留在 `C-044`） | `templates/review-template.md` § 2.1–2.4; `shared/workflow/acceptance-hardening.md` § Review Composition (the order's owner) | `skills/internal/code-review/scripts/git-delta-review.sh` owns only the code segment's four-value verdict vocabulary (`pass` / `blocked` / `not-applicable` / `not-evaluated`) and enumerates no sequence; no engine reads a segment order |
| `self-improvement-stage-sequence` | 2 | `skills/internal/self-improvement/SKILL.md` | `shared/workflow/self-improvement-workflow.md` § Standard Flow (SI-0…SI-7); `shared/definitions/self-improvement-definitions.md` § Self-Improvement Loop | `Bootstrap` / `Operationalize` / `Optimize` appear in no `.py` and no `.sh` (measured 2026-11-05) |
| track-to-executor mapping | 2 | `skills/internal/self-improvement/SKILL.md` | same two prose carriers (§ SI-4 Route to the Canonical Improver) | same measurement; no engine maps a track to an executor |
| `improvement-track-values` | 2 | `skills/internal/improve-agent/SKILL.md`; `improve-team/SKILL.md`; `improve-tools/SKILL.md`; `skills/external/improve-docs/SKILL.md`; `improve-skills/SKILL.md` | those five carriers' § Target Classification | the improve-\* skill scripts (`skills/external/improve-skills/scripts/redline-check.py`, `skill-shape.py`) carry no track vocabulary |
| changed-asset-category mapping | 2 | same five units | same five carriers | no engine classifies a changed asset into a category |
| `history-categories` | 3 | `skills/internal/manage-history/SKILL.md`（该单元仍 in-scope，理由见下：`history-manifest-schema` 留在 `C-045`） | `skills/internal/manage-history/SKILL.md` § Step 3 Distill / § Step 4 Theme Aggregation | the five category names are in no `.py` and no `.sh`; `scripts/python/history-utils.py` writes the record store and its manifest without enumerating categories |

**Fact rows and unit rows are two different quantities — never converted into one another.** The file the implement stage
writes is `shared/declarations/exclusions/no-machine-fact.yaml`, whose rows are `unit` / `carrier` / `anchor` keys
(`requirements.md` FR-005, `data-model.md` E-2). Two rules decide the row count, and both are the model's, not this table's:

1. **An exclusion row is owed by a unit**（FR-002）, and a unit is **never** both declared and excluded（`data-model.md` E-2
   **R-4**: exactly one disposition per unit; E-5 resolves a contradictory pair to a *finding*, never to file order）.
2. **`carrier` is what the unit does reach** — the deterministic engine its text actually calls — not the markdown that
   carries the fact. That engine is located by `grep` when the row is written; this table does not pre-assert it.

Measured against those two rules on 2026-11-05, the eight facts above land on **eight excluded units** — two for the analyze
pair, one for the self-improvement pair, five for the improve pair — so `no-machine-fact.yaml` carries **8 rows**. The
remaining **two facts contribute no row**: `review-segment-sequence` and `history-categories` sit on a unit group that keeps
an in-scope fact (`ARC verdict mapping` in `C-044`; `history-manifest-schema` in `C-045`), so those units stay in scope and
a `no-machine-fact` row for them would be the one state R-4 forbids. Their removal is recorded **here** and in
`.specify/memory/features/084.md` § Latest Review — an absent migration, not a silent deletion.

**The counts are readings, not commitments.** 8 facts / 8 units is a 2026-11-05 measurement on the tree at `d23490c3`. The
implement stage re-runs screen S and the anchor greps before writing the file and records the count it measured; a unit that
the screen no longer yields is dropped from the file, and a fact whose anchor grep returns a live engine read point moves
**back** into `C-044` / `C-045` rather than staying excluded.

**候选屏幕的其余单元由 `exclusions/` 的逐行记录处置；覆盖动作的零未分类即判决**（T032，2026-11-05，implement part 6）。This
section owns one thing only — which facts left the roster and why. The disposition record of every other candidate the screen
yields is owned by `shared/declarations/exclusions/<reason>.yaml`, one row per unit (`requirements.md` FR-002 / FR-005,
`data-model.md` E-2); this file MUST NOT restate that list, because the two exclusion files are its single source and a copy
here would drift silently. The verdict is a reading of the tree, not a clause: `harness-triple-check.py --action coverage`
reports `unclassified: 0` with `findings: 0`, and `--action verify` reports zero `exclusion-anchor-unresolvable` and no unit
named by two rows. A unit that later gains a machine-consumed fact moves back into `C-044` / `C-045` by that same reading.

## Verification (route (b), per reading)

Every reading above is measured at implement time, not now: the declarations do not exist on this branch. Premises to
re-measure rather than inherit:

| Reading | Command shape | Premise |
|---------|---------------|---------|
| fidelity to today's faces | `grep -n "DEFAULT_THRESHOLD\|SEVEN_STATES\|LANE_NAMES\|CLASS_VALUES\|BASIS_VALUES\|FLOW_TYPE_VALUES\|REQUIRED_LEDGER_COLUMNS\|NEUTRAL_CATEGORIES\|PATH_VALUES" scripts/python/*.py` | the file:line readings in `research.md` § R5 are from this branch at `171c2ff8`; re-read before editing, they move |
| residual literals (b) | `python3 scripts/python/doc-consistency-check.py --action verify --faces duplicate --spec-dir .specify/specs/084-harness-triple-structure` | runs today (measured: duplicate pass, zero findings) and reuses `duplicate-fact`; it reads `--spec-dir` formal files, so the carriers it can judge are the spec's, not the whole repo — the whole-repo reading is the checker's own `verify` action |
| zero new failures (e) | `bash scripts/bash/run-tests.sh --names-out <file> -q` then an id-level difference against the implement-start baseline | the runner resolves `python3` (measured); the baseline is taken at implement start, not inherited from this plan |
| the excluded facts still have no engine read point | the anchor `grep` in each row of § Facts outside the roster, plus `grep -rln "Bootstrap\|Operationalize\|Optimize" --include=*.py --include=*.sh scripts/ skills/` | today's readings are in that table's anchor column (all zero hits); the exclusion file may be written only after a re-run, and a hit moves that row back into `C-044` / `C-045` instead of being excluded |
| the 081 acceptance files are untouched | `git diff --stat 171c2ff8 -- tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py` | empty output is the pass criterion; collected counts today are 40 and 37 |
