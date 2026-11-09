# Phase 0 Research — Non-Disposable（历史回顾与处置机制）

**Feature**: 092-non-disposable | **Date**: 2026-11-09 | **Spec**: [`requirements.md`](requirements.md)（65 FR / 20 SC，D-1…D-8，A1–A14，OI-1…OI-5）

Every finding below was measured read-only on commit `62f95298` before any design was written. A finding that
records a value also records the command that produced it, so a later reader can re-run it instead of trusting
this page. This file owns **the reasoning**, not the values: an enumeration or a threshold cited here is reached by
pointer to its owner (the owner page, a declaration file, or an engine constant).

## R1 — `/speckit.history` already has exactly one executable core

**Measured.** `templates/commands/history.md` (52 lines) is entry + `## Skill Delegation` + the compiled `## Wrap-up`
+ `## Handoffs`; the six-step workflow and the safety rules live in `skills/internal/manage-history/SKILL.md`
(123 lines). The engines are `scripts/bash/collect-history.sh` (locate / extract / manifest-update) and
`scripts/python/history-utils.py` (`STORE_RESOLVERS`, one per tool; the manifest schema is read from
`shared/declarations/facts/history-manifest-schema.yaml#/statement` through `declaration_reader`).

**Consequence.** The four-stage form (review → design → confirm → execute) is a **seam inside `manage-history`** and
an enumeration line added to the command template's delegation bullet list — not a second command, not a second
skill, not a second store. `manage-history` keeps owning steps 1–6; the new stages are appended as its steps 0/A/B,
so the existing distillation remains reachable at its existing name (FR-043, FR-044, FR-059).

**Rejected alternative.** A sibling skill `non-disposable-review` wired into the same command: it would make
`/speckit.history` have two executable cores, which is the exact defect the feature exists to detect
(`multi-owner`), and it would give the review surface a second scheduling owner.

## R2 — `scripts/python/sanitize-utils.py` is a vocabulary owner, not a host

**Measured.** `CATEGORIES` = 6 items (`stale-residue`, `redundant`, `dead-reference`, `index-inconsistency`,
`broken-symlink`, `mirror-drift`); `DISPOSITIONS` = 5 (`delete`, `archive`, `repair`, `delegate`, `dismiss`);
`STATES` = 3 (`pending`, `resolved`, `dismissed`); `DETECTIONS` = 2 (`programmatic`, `semantic`). `DETECTIONS`'s
first member is spelled **`programmatic`**, not `deterministic` — see R6.

**Consequence.** FR-060 forbids touching those four sets; FR-012 requires two closed mapping tables plus one
adjudication rule inside the owner page. `DETERMINISTIC_CATEGORIES` / `SEMANTIC_CATEGORIES` in the same engine are
its own classification of its own categories and are not a second copy of the review surface's class roster.

**Rejected alternative.** Folding `stale-residue`/`redundant` into the new engine's categories: it would move a
declared owner's criteria into a second place and falsify Feature 047's contract (the `A20` boundary in
`requirements.md` § Boundary and Ownership).

## R3 — the closure verdict already owns the reason vocabulary the status check must reuse

**Measured.** `scripts/python/closure-acceptance-check.py` exposes a seven-member closed `REASON_CODES` set whose
member `status-claims-implemented-but-blocked` is exactly FR-026's required code; `--json` emits `verdict` +
`reasons`; exit codes are 0/1/2 with the "missing input is never `block`" rule. `STATUS_VALUES`, `LADDER_FIELDS`,
`SMOKE_FIELDS` and the `final_path` buckets are read from
`shared/declarations/facts/arc-verdict-mapping.yaml#/statement` and from `FINAL_PATH_*` constants.

**Consequence.** The new engine **invokes** the closure engine as a subprocess and consumes its `--json`; it never
re-implements a verdict (FR-028). The status family of detections is a thin comparison layer: registry claim vs
`verdict`, `verification.md` field presence vs `SMOKE_FIELDS`/`STATUS_VALUES`, closed-set identity arithmetic vs the
recorded bucket counts.

**Measured baseline for the A–H corpus.** `python3 scripts/python/harness-triple-check.py --action verify` today
reports `unclassified-candidate` ×3 (`skills/external/ssh-utils/SKILL.md`, `templates/commands/measure.md`,
`templates/commands/status.md`), exit 1. This is corpus row A-2 (the "declared clean, engine says 3 unclassified"
contradiction) *as it exists on this tree*, and it is the first live demonstration that the detection engine must
read the engine's reading, not the document's claim.

## R4 — the declaration layer is the only legitimate carrier for the review-surface roots

**Measured.** `shared/declarations/contract.yaml` owns the closed `fact_kinds` (`threshold`, `closed-set`,
`ordered-operator-table`, `mapping`, `record-schema`) and the `required_fact_keys` (`fact`, `kind`, `statement`,
`consumers`, `former_carriers`); `scripts/python/declaration_reader.py` is the one read entry (`load_fact`,
`load_facts`, `find_repo`, `normalize_path`, `absent_label`); `shared/declarations/facts/flow-class-classes.yaml`
is the closest sibling (a `closed-set` whose member order is part of the value).

**Consequence.** FR-037/FR-038 land as one new fact file with `kind: closed-set` whose `statement` is the ten root
names **in the declared order** (order is part of the value: the coverage declaration prints it in that order). The
count is not written a second time — it is `len(statement)`, which is what FR-038 means by "declared once at the
same place". The directory literal MUST NOT appear in any engine, command template or skill (FR-037).

**Rejected alternative.** A `kind: mapping` fact carrying `{roots: [...], count: 10}`: the count would then be a
second statement of a derivable value, and the sibling precedent (`success-criterion-path-values`,
`flow-class-classes`) already fixes `closed-set` as the shape for an ordered member list.

## R5 — the renumber predicate already distinguishes live bindings from history

**Measured.** `scripts/python/renumber-utils.py` implements exactly the split FR-022/FR-023/FR-024 need:
`EXCLUDED_PREFIXES` (`.specify/history/`, `.specify/archive/`, `.specify/specs/.archive/`),
`MACHINE_PREFIXES` (`.specify/memory/{sanitize,retention,renumber}/`), `EVIDENCE_SEGMENTS = {"test-evidence"}` and
`DATED_RE` (`\d{4}-\d{2}-\d{2}|\d{8}` on the file name), plus `_is_machine` / `_is_dated_record` and a
`SCAN_ROOTS` set covering `.specify` and the framework trees.

**Consequence.** FR-024's "closed enumeration by path and by section position" is satisfied by **declaring this
file the owner of the history-side predicate** and having the new engine import/reference it, not by writing a
second predicate set. The new engine adds only what renumber does not have: the **live-binding** side (which cells
and headers bind the directory's own number) and the "a history record was rewritten" leg.

**Boundary recorded.** `renumber-utils.py` is an existing owner; this feature references it. If implement finds an
APIs gap, the repair belongs to that file's own contract, and the gap is reported — not silently re-implemented.

## R6 — `detection` vocabulary: one word per set, and the sets do not merge

**Measured.** `sanitize-utils.DETECTIONS = ["programmatic", "semantic"]`. `requirements.md` FR-004 says
"`deterministic` / `semantic`（术语与 sanitize 的 `DETECTIONS` 同名同义，按指针引用，不另造词）". The two statements
disagree on the first member's spelling.

**Resolution (recorded, not silent).** The owner page declares the review surface's own two values as
`deterministic` / `semantic`, **and** the bridge table's adjudication rule names `programmatic` as the sanitize
side's spelling of the same axis. Reason: FR-004's *normative* content ("断言对象是文件/行/字段/字面量 → 引擎判定")
is what the engine implements, and the requirements call `deterministic` the word every other FR uses
(`FR-005`, `SC-016`); the parenthetical claims identity with a set whose member is spelled differently. Renaming
the sanitize member is forbidden (FR-060), so the two spellings must coexist as two sets — exactly the D-1
treatment already applied to the disposition vocabularies. This is a **correction, not a decision**: one reading
(the owner page names its own two values and the bridge maps the other side) is fully consistent with every other
FR. It is recorded here and in the owner page's § Disposition Bridge, and disclosed at wrap-up.
See `T-004` for the load-bearing part of the same question (see § Decision Tensions in plan).

**Alternate spelling risk.** A resolver that tries to unify the two literals at implement time would silently
rename a delivered contract's member; that is why the ban is written in the owner page rather than left to review.

## R7 — the expression-compatibility baseline is a closed-set that this feature will touch

**Measured.** `tests/contract/test_expression_compatibility.py` freezes a 74-source hash manifest (25 command
templates + 49 skill sources) at a dated baseline commit and asserts each file's bytes are unchanged unless it is
registered in `ALLOWED_POST_BASELINE_CHANGES` with a `reason` and `markers` (two of which use
`COMPILED_BANNER_ONLY` or `added_markers`). `templates/commands/history.md` and
`skills/internal/manage-history/SKILL.md` are **both** in that manifest.

**Consequence.** Editing the command template and the skill is legal but MUST register itself in that dict with
markers that are **added** by this feature (`added_markers: True`-style two-directional assertion) — a marker that
already existed cannot witness a drift. This is the concrete form of FR-052's "guarded, not free" requirement: the
seam is a change to two frozen files, and the freeze is the guard (`contracts/four-stage-command.contract.md`
C-4xx).

**Rejected alternative.** Adding the review surface as a new command template: a new file is outside the 069a
manifest and the guard's own comment says an allowance entry for it would be vacuous — the guard would prove
nothing about the seam.

## R8 — a second source of "what is a live binding" already exists: `validate-requirements.py`

**Measured.** `scripts/python/validate-requirements.py` runs six deterministic labels over a requirements file
(`id-contiguous`, `doc-order`, `ref-resolvable`, `marker-count`, `dup-id`, `path-marker`) and emits 0 errors /
0 warnings for `092`; `scripts/python/validate-tasks.py` is its tasks-side sibling; `scripts/python/account-clause-coverage.py`
carries `--spec-dir` / `--baseline` / `--freeze` / `--list-named` and is the existing owner of clause coverage.

**Consequence.** The new engine's `renumber-live-binding` check MUST consume these existing readings where they
overlap (an FR id that does not resolve is `ref-resolvable`, not a new finding class) and add only the
characteristically unowned leg: "a **cell or header** in a delivered artifact binds a feature number that differs
from the directory's own number, and that artifact is not a history record". `contracts/detection-categories.contract.md`
carries the per-category owner-of-the-overlap column so that the same physical defect is not reported twice under
two names — the FR-013 rule applied inside this feature.

## R9 — the corpus integrity scan: what A–H actually reaches in `requirements.md`

**Measured (read-only).** FR ids 001–065 contiguous, SC ids 001–020 contiguous, zero dangling `FR-`/`SC-`
references. Two structural facts a reader of `requirements.md` alone cannot see:
- The `A–H Corpus Mapping` table's `档` column is written `I（…）` / `II（…）` **outside** the cell's backticks and
  the table has an extra empty cell between the SC column and the tier column, so a row has 8 pipes' worth of
  cells for a 6-column header. A deterministic reader of that table MUST therefore read the tier from the cell
  text, not from a fixed column index (`contracts/report-schema.contract.md` C-703 / `contracts/detection-categories.contract.md` C-102).
- The `### OI 处置结果（clarify，2026-11-09）` table already routes OI-1…OI-5; OI-4 and OI-5 are deliberately open
  and are *not* this feature's to close (FR-065; `plan.md` § Decision Tensions `T-002`).

**Consequence.** § A–H Corpus Mapping in `plan.md` is the **per-entry expansion** the requirements table promises
to plan/tasks ("逐条的映射 MUST 在 plan / tasks 阶段展开为一行"): one row per corpus entry — A1–A6, B1–B5, C1–C5,
D1–D6, E1–E6, F1–F5, G1–G3, H1–H3 = **35 entries** — each carrying the tier, the detection class and the receiving
carrier. The count is taken from the corpus file's own table rows and list items per section (`A` 6, `B` 5, `C` 4,
`D` 6, `E` 6, `F` 5, `G` 3, `H` 3), not from the section titles.

**Live re-check (read-only, `62f95298`).** Several corpus rows are reproduced by the tree as it stands, which is
what SC-001 asks the engine to do later:
- **A1 still true** — `084/verification.md:70` records `unclassified 0`, and today's
  `harness-triple-check.py --action verify` reports 3 (`skills/external/ssh-utils/SKILL.md`,
  `templates/commands/measure.md`, `templates/commands/status.md`), exit 1.
- **A5 still true** — `085/plan.md` is judged `error` by `validate-decision-tensions.py` (`dtr-rejected-form`).
- **G1/G2 still true** — `tests/contract/test_sdd_loop_driver_reanchor.py:118-119` is the `first_no = "1"` /
  `assert first_no == "1"` tautology.
- **F2 still true** — `scripts/bash/generate-instructions.sh:100` declares `INSTRUCTIONS_BUDGET_BYTES=38400` while
  the reason block immediately above it derives `37888`, and `090/review.md:230-245` already records the
  arithmetic contradiction (the corpus row and the review row are the same defect seen from two features).
- **F1 is stale as stated** — the corpus names `40` / `60` / `80` / `30` / `120` / `160` as six live ceiling
  values. Measured: the **value owner** is `decomposition-check.py`'s `FR_CEILING = 120` / `TASK_CEILING = 160`,
  pinned equal to `admission-check.py`'s `FR_MAX` / `TASK_MAX` by `tests/contract/test_sdd_loop_driver_gates.py:67-68`,
  and `skills/external/sdd-loop-driver/references/efficiency-model.md:300` already states that owner correctly. The
  stale occurrences are **dated records and delivered spec bodies** that quoted a then-current value (`080/tasks.md`
  "40", `077` / `079` / `069b` "40", `069/notes/decomposition-gate.md` "30/40", `082/features` "60", `082` state "60").
  So F1's live form is not "six conflicting live owners" but "one owner plus `stale-constant` hits in history
  records" — and by FR-020's own rule a dated record is *legitimate* repetition. F1 is therefore **档 II** with a
  narrowed shape: the only in-scope part is that the four live-value rows above the rule are neither history nor
  owner, which the `stale-constant` check must classify rather than the repair lane rewriting them.
  Recorded as a correction to the corpus reading, disclosed at wrap-up; the corpus file itself is a dated record
  and is not edited (FR-058 / `A14`).

## R10 — the review surface's actual size, re-measured at this stage

**Measured.** `for d in archive derive goal history memory project review specs state teams; do find .specify/$d -type f | wc -l; done`
on `62f95298`: `archive 66 / derive 2 / goal 55 / history 7 / memory 1216 / project 10 / review 1 / specs 2899 / state 27 / teams 74`
= **4357** files. Clarify measured 4352 on the same roots; requirements measured 4345. The delta is this line's own
record writes (`memory` +3, `specs` +2 since clarify). SC-014 treats the reading as a reference, not a threshold,
and the three readings are themselves the evidence that a hand-written count would have drifted within one stage.

**Consequence.** `4,357` is above a single agent's context budget by three orders of magnitude, so the shard
partition is not an optimisation — it is a precondition for the review to be able to say anything at all (US8).
The deterministic engine's coverage declaration is what makes the number checkable without reading the files.

## R11 — the confirm gate that already exists in the same family: `sanitize-utils.py apply`

**Measured.** `cmd_apply` refuses unless the plan file carries `"confirmed": true`, validates each row's
`disposition` against an applyable subset (`delegate` items are recommendations, not plan rows), and never deletes
a non-empty directory by design (`check_legacy_install_residue`).

**Consequence.** The four-stage seam's confirmation surface follows a **proven sibling** instead of inventing one:
a closed confirmation vocabulary in the owner page (`group` / `item` / `none-of`), a
`.specify/.tmp/`-hosted plan document carried only for the duration of the confirm stage and deleted by the
execute stage (FR-031), and a `confirmed` flag the execute stage refuses without. The
`archive` disposition adopts `git mv` semantics and the `correct`/`supersede` marking changes are per-file
reversible; **no disposition deletes** (FR-034, FR-058).

## R12 — the gates this stage must run, and what each one actually reads

| Gate | Invocation | What it reads |
|------|-----------|---------------|
| plan entry | `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --stage plan --spec-dir .specify/specs/092-non-disposable --repo .` | this spec's artifacts + the section shapes the stage owes |
| decomposition | `python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode plan --requirements .specify/specs/092-non-disposable/requirements.md` | `^- \*\*FR-NNN\*\*:` rows vs the FR ceiling (measured 65 ≤ 120) |
| decision tensions | `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/092-non-disposable --json` | one record per `### T-NNN` heading under `## Decision Tensions`, six fields, `expected_sacrifice` bound to exactly one `**SC-NNN Source**` entry in `requirements.md` § Measurement Sources |

`decomposition-check.py` measures **the requirements artifact only**; it has no argument for a package plan.
Therefore this plan's implement-side package proposal (§ Implement Package Proposal) is a design deliverable for
`/speckit.tasks` and is **not** an input to that gate — the gate's `proceed` reading answers exactly one question
(the FR ceiling), and reading it as an approval of the package partition would be a green check claimed as proof
of something it never examined.

## R13 — the corpus can be reproduced now, so the engine has a fixture set before it exists

**Measured (read-only).** Two of the eight detection classes have a live hit that can be turned into a fixture
without waiting for the engine: `status-unreadable` (the `harness-triple-check` divergence in R9) and
`stale-constant` (the `generate-instructions.sh` budget block in R9). The other classes have a **described**
instance in the corpus but the copy that would carry it is not assembled yet.

**Consequence.** `quickstart.md` scenario 1 is written against the tree as it stands (a real reproduction, not a
synthetic one), and every other scenario names the minimal mutation it needs. A quickstart that only ever ran on
synthesised fixtures would prove the engine can be made to fire, never that it fires on the defect the feature was
written for.
