# Research: Review × Code-Review Composition (071)

**Requirement → Feature**: `071-review-code-integration` → Feature 071 Review 命令与代码评审技能的组合与治理
**Date**: 2026-10-27
**Method**: every premise below was re-measured against this repository at commit `884e7a86` (working tree clean) before it was used in a design decision. Where a decision rests on a command, the command and its real output are quoted. No premise is carried over from the requirements document without re-measurement.

## R1 — Composition shape: sequential segments, process first, no merged severity

**Decision**: `/speckit.review` runs exactly two segments in fixed order — process segment (`review-sdd-process`) first and unconditional, code segment (`code-review`) second — and the two conclusions are never merged into one severity system or one score.

**Evidence measured**:

- `templates/commands/review.md` (53 lines) delegates only to `review-sdd-process`; its `## Delegation` paragraph says the report reviews "the SDD process that produced the feature …, never the code it produced".
- `skills/internal/review-sdd-process/SKILL.md` `description` states "This skill has no overlap with the code-review skill, which reviews code diffs/PRs"; `## Boundaries` repeats "No overlap — keep the two separate even though both say \"review\"".
- `grep -rn "code-review" templates/ docs/reference/commands/` returns nothing: no command template references the skill today.

**Alternatives rejected**: parallel segments (no benefit on a serial artifact chain; two writers into one feature directory), a single merged report (forces one severity table, violating FR-007/FR-001), a mode parameter (creates a path where the process segment can be skipped, contradicting the 100%-call-rate gate that `shared/definitions/flow-class-definitions.md` records for the `review` face).

**Consequence for the "no overlap" wording**: after composition that sentence is false, so it is rewritten into "distinct judgment objects, composed by the command" (FR-025) rather than left standing.

## R2 — Review object and base resolution, with the failure mode measured on this repo

**Decision**: the code segment's object is this feature slice's committed delta. Resolution order: explicit caller value > parent of the first commit that added this feature's `requirements.md` > merge base with the repository default trunk. The rule is implemented in the skill's script and is parameter-overridable.

**Measured on this repository** (the three facts that make the order non-arbitrary):

```text
$ git log --diff-filter=A --format='%H %ad %s' --date=short -- .specify/specs/071-review-code-integration/requirements.md
8d18265baf9d1aa8c4580339946411ddb082735f 2026-10-27 docs(071-review-code-integration): land the review × code-review composition requirements

$ git rev-parse 8d18265b^        # e57052ef — the feature-slice base
e57052efa1c16871da4e24a56eabf7402b6fd87e

$ git symbolic-ref refs/remotes/origin/HEAD
fatal: ref not a symbolic ref

$ git remote -v
origin  git@github.com:github/spec-kit.git (fetch)      # upstream, not this work
github  git@github.com:cloud-native-ai/spec-kit.git (fetch)
gitee / gitlab …                                        # three more remotes

$ git rev-parse main; git rev-parse --short master; git merge-base main HEAD
2dd1ca4f…      884e7a86      926836e0…
```

Three readings follow from that output:

1. `refs/remotes/origin/HEAD` does not exist here, and in this clone `origin` is the UPSTREAM project. A rule that starts from `origin/HEAD` finds nothing; a rule that falls back to a local branch named `main` resolves to `2dd1ca4f` whose merge base with HEAD is `926836e0` — a base far behind the feature slice, which would fold months of unrelated history into every review. The base therefore cannot default to a branch name.
2. The first-commit instrument already exists in this repository's governance and is the one 069b contract C-1 pins for the requirements first commit (`git log --diff-filter=A`, never `git log -1`). Reusing it means the code segment and the wall-clock baseline measure the same freeze point.
3. The script's own default is the wrong default for this job: `git-delta-review.sh` sets `GIT_BASE="${GIT_BASE:-main}"` (line 22), so the composed path must pass the resolved base explicitly instead of relying on it (FR-004 in the requirements forbids the built-in default).

**Alternatives rejected**: `HEAD~N` (N is unknowable); "the whole branch" (`main..HEAD` on this repo spans the upstream mirror); working-tree diff (excluded by FR-005 and by the fact that the review's object must be reproducible from commits).

## R3 — Renderer absence: replace the stop clause, keep the anti-pretense rule

**Decision**: a missing `delta` no longer stops the code segment. The segment completes in text mode, the record marks the mode, and the coverage receipt becomes the substitute evidence for "the whole diff was read". The old clause is *rewritten*, not deleted: the skill keeps one statement naming the replaced clause, the substitute evidence form, and the reason.

**Measured on this host**: `command -v delta` → `/home/agent/.cargo/bin/delta`, so the text-mode path cannot be exercised live here without manipulating `PATH`; the contract test therefore builds the text-mode assertion by driving the script with `DELTA_BIN` pointed at a non-existent binary (a deterministic substitution the script already supports through its `DELTA_BIN` variable).

**Skill surfaces carrying the old clause today** (all three must move together, FR-013):

| Surface | Current wording |
|---------|-----------------|
| `SKILL.md` § Strict Requirements | "**环境缺失即停**：delta 缺失时报错 + 安装指引，停止执行；不自动安装、不降级为 `git diff` 裸输出冒充已审查。" |
| `SKILL.md` § Phase 0 step 3 | "确认 delta 可用：`command -v delta`。缺失时**报错并给出安装命令后停止**" |
| `SKILL.md` § Overview / § Resources | `note`/`report` as the only delta-free subcommands |

**Why not keep "stop"**: in an unattended run the segment must still produce a judgement; stopping yields no conclusion at all, which is worse than a labelled text-mode conclusion — provided nothing claims a rendered review happened. The anti-pretense rule is what the constraint was protecting, and it survives verbatim in the new clause.

## R4 — Coverage receipt: carrier, closed field set, exit codes

**Decision**: the receipt is one delimited block inside `code-review.md`, `name=value` per line, written by a new subcommand of the existing script. Exit codes: `0` = file sets equal and every changed file judged (reasoned skips included), `1` = gap, `2` = input/base error.

**Why the block and not a JSON sidecar**: the feature's own constraint set forbids a second artifact file (FR-014) and forbids a second artifact chain entry (FR-012). The block keeps one artifact and still parses mechanically: the delimiters are HTML comments, so a Markdown renderer hides it, while a contract test reads it with a two-line split.

**Why exit `1` for a gap and `2` for input error**: this repository's deterministic gates already use that pair (`skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` documents `0 = pass, 1 = fail, 2 = input or parse error`). Reusing the convention means a caller can branch without reading a new vocabulary.

**Gap vs skip, measured consequence**: a "skip everything except one file" run would otherwise exit 0 and could be presented as a pass while 49 changed files were never read. The decision therefore splits the two: a skip is not a gap (exit still 0) but it is not coverage credit either, so a non-zero skip count forbids a `pass` verdict (FR-014, clarified 2026-10-27).

**Design refinement DR1 (disclosed)**: two literals describe the same mode — the record's marker must be the requirements' Shared String `renderer: text` (STR-003), while the receipt block's field must be `renderer=text` to keep the block uniformly `name=value`. Rather than let two hand-written copies drift, both are written by the same subcommand in one write pass and a contract test asserts equality. This is a machine-regenerated projection (Constitution XIV, second legitimate duplicate class), not a second owner.

## R5 — Gate ownership: converge the copy and disclose one pin change

**Decision**: the normative statement of the `Implemented → Ready for Review` gate moves to (stays at) `templates/feature-details-template.md` § Canonical Status State Machine; the duplicate summary row in `shared/workflow/feature-integration.md` § Status State Machine becomes a reference.

**Measured state of the two copies**:

| Owner candidate | Current row text |
|-----------------|------------------|
| `templates/feature-details-template.md:71` | `| Implemented | Ready for Review | /speckit.review (or human) | All deferred ([~]) tasks are resolved or explicitly waived, and review evidence has been produced. |` |
| `shared/workflow/feature-integration.md:38` | `| /speckit.review | Implemented → Ready for Review | review.md committed AND every deferred item resolved or waived |` |

The two disagree on wording and on strictness ("review.md committed" is not in the owner; the owner's "review evidence" is not in the copy). The section in `feature-details-template.md` declares itself "the authoritative transition table cited by `/speckit.feature`, `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`", so it is the owner by declaration.

**The conflict this decision creates, measured**: `tests/contract/test_review_p1_review_loop.py::test_c15_review_owns_the_ready_for_review_transition` asserts, over the `feature-integration.md` table:

```python
assert "| `/speckit.review` | `Implemented → Ready for Review` |" in table
assert "review.md committed" in table
assert re.search(r"deferred item resolved or waived", table)
```

Converging the row to a reference removes both literals, so that test goes red. Three options were considered:

1. **Keep the literals and add a pointer.** Rejected: leaves the second criteria wording in place, which the requirement forbids and which is exactly the drift the two copies already show.
2. **Delete the test.** Rejected: deleting an existing assertion is the weakening the requirements forbid (FR-027).
3. **Update the pin to the reference form and add a negative assertion.** Adopted. The test keeps its subject (the `/speckit.review` row exists and the command owns that transition), stops asserting the duplicated wording, and gains an assertion of the owner's path plus an assertion that the duplicated wording is *gone* — so the drift that motivated the requirement now turns the test red. Net assertion count goes up, not down. This is the one intentional pin change of the feature and it is disclosed here, in `plan.md` § Risks (R-03), and in `feature-ref.md`.

**Why the checklist row is in scope**: `shared/workflow/feature-integration.md` gives `/speckit.checklist` the same `Implemented → Ready for Review` transition. Because the requirement places the criterion on the transition rather than on one command, both initiators cite the same owner row (FR-008, clarified 2026-10-27). The existing annotation "applies only when the checklist runs after implement" stays (a contract test pins it).

## R6 — Record naming and rotation

**Decision**: the code segment record is always `code-review.md` (STR-004) — the latest run — and a re-run first archives the previous file as `code-review-<run timestamp>.md` in the same directory.

**Measured conflict this resolves**: the requirements fix the filename literal (Shared Strings) *and* demand that a re-run not overwrite the previous record. Both are satisfiable only with the stable name plus an archive step; a pure timestamp name would break the literal reference that contracts and tests use, and a pure overwrite would lose history.

**Collision consequence measured**: the archive suffix uses the run timestamp `YYYYMMDD-HHMMSS`, the form the script already uses for `review_file_path()` (line 99–103 of `git-delta-review.sh`). Two runs launched inside the same second would collide; the archive step therefore refuses to overwrite an existing archive and exits 2 instead of silently losing a record.

## R7 — Non-interactive path, and what "non-interactive" costs

**Decision**: a fully non-interactive path exists as script subcommands — record creation/rotation, opinion capture (`note`), coverage receipt (`receipt`), verdict (`report --summary --file`). The interactive `review` subcommand stays as the human path, rendered when `delta` is present.

**Measured state**: `review --yes` already suppresses prompts (`INTERACTIVE=false`), but `cmd_review` calls `need_delta` unconditionally, so the "non-interactive" flag is unusable in a delta-less environment. Separately, `note` already runs without delta, and `report` already runs without delta. The gap is therefore narrow: the record must be creatable and the receipt computable without delta and without a TTY.

**Measured defect inherited from the clarify run (F-obs 2)**: `cmd_note` and `cmd_report` both select their target as `ls -t "$REVIEW_DIR"/*.md | head -1`. Pointing `REVIEW_DIR` at a feature directory (what the composition needs) means `review.md` and `code-review.md` compete for "newest", and `report --summary` would happily read the process report, find zero `blocking` headings, and print a green gate. The composed path therefore always passes the record path explicitly, and the verdict subcommand treats an omitted path as a legacy selection it labels as such.

## R8 — Where the code-segment section goes in the process report template

**Decision**: a subsection `### 2.1` under § 2 Findings Summary, not a new top-level section.

**Measured reason**: `tests/contract/test_review_p1_review_loop.py` parses `templates/review-template.md` by section numbers (`_section(body, r"## 5\.", r"## 6\.")` for the recommendations and roadmap sections). Inserting a new top-level numbered section renumbers § 5 and § 6 and turns that test red for a reason unrelated to its subject. A subsection keeps every existing section number stable, so the existing pin keeps meaning what it meant, and the new content is still in the report a reader opens first.

**Content limit**: base/head ids and base source, renderer mode, receipt counts (changed / judged / skipped / gap), segment verdict, gate verdict, `not-applicable`/`not-evaluated` reason, the record path, and this run's archive path. Opinion bodies are not copied (FR-011) — the subsection is a pointer with a verdict, which is the same shape the review report already uses for external targets.

## R9 — Feedback boundary: two units, one key, no new store

**Decision**: the nested run records two entries — command unit `/speckit.review` and skill unit `skill:code-review` — each at its own wrap-up, keyed by `(unit_id, run_id)`. Only framework friction is posted; code defects stay in the record.

**Measured state**: both units are already registered in the probe registry (`shared/definitions/probe-definitions.md` lines 78 and 87: `speckit-review-wrapup` and `skill-code-review-wrapup`), so the closing faces exist and this feature adds no step (FR-016). `shared/workflow/feedback-step.md` § Mechanism boundary already draws the SDD-flow vs framework-feedback line, and § Dedup guard keys on `(unit_id, run_id)`, so two units in one run do not collide and neither has to be suppressed (FR-018).

**Why the classification duty must be written down rather than assumed**: before this feature, the review command had no path that produced a *code* finding, so "a defect found during review is framework friction" was economically true. After composition the same run produces both kinds, and the cheapest wrong move — posting the code defect to the feedback store — becomes the default. The requirement's FR-017 turns that into a written rule in two surfaces (command template and skill text), which is what makes SC-007's sample detectable.

## R10 — Two hats, mirrors, and the measured baselines

**Decision**: framework sources are the only edit surface; every projected copy is produced by the existing generators.

**Measured baselines, taken before any edit of this feature** (all clean, so the acceptance criterion is "no NEW drift"):

```text
$ python3 scripts/python/sync-mirrors.py --check --only templates
ok    templates/ == .specify/templates/ (22 files)
$ python3 scripts/python/sync-mirrors.py --check --only skills/internal
ok    skills/internal/ == .specify/skills/internal/ (136 files)
$ python3 scripts/python/sync-mirrors.py --check --only shared
ok    shared/ == .specify/shared/ (55 files)
$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
```

**Projected copies this feature touches**:

| Source | Projection | Generator |
|--------|-----------|-----------|
| `templates/commands/review.md` | `.claude/commands/speckit.review.md`, `.github/prompts/speckit.review.prompt.md`, `.qoder/commands/speckit.review.md`, `.opencode/command/speckit.review.md` | `regen-command-copies.py` (the retired runtime command-template mirror is not a target) |
| `templates/review-template.md`, `templates/feature-details-template.md` | `.specify/templates/…` | `sync-mirrors.py` |
| `skills/internal/code-review/**`, `skills/internal/review-sdd-process/SKILL.md` | `.specify/skills/internal/…` | `sync-mirrors.py` |
| `shared/workflow/feature-integration.md` | `.specify/shared/workflow/…` | `sync-mirrors.py` |
| `docs/`, `tests/` | none | — |

**Probe registry**: unchanged. The two wrap-up faces this feature relies on are already registered (see R9); no registry edit, therefore no `compile-embeds` run and no risk of hand-editing a compiled face.

## R11 — Test strategy, including the one disclosed pin change

**Decision**: six new deterministic contract assertions groups (one per FR-028 item) plus one intentional pin update. Nothing is deleted.

**Measured baseline of the neighbouring suites** (run before any edit):

```text
tests/contract/test_expression_gates_doc.py            18 passed
tests/contract/test_expression_compatibility.py
tests/contract/test_run_skills_wiring.py
tests/contract/test_migration_distribution.py
tests/contract/test_flat_internal_skill_migration.py
tests/contract/test_review_p1_review_loop.py           60 passed (5 files)
```

The fifth file is included deliberately: it holds the pin this feature changes, so its pre-change green state is part of the measurement rather than an assumption (`test-evidence/regression-baseline.txt`).

**Assertions that constrain this design, read from the tests themselves**:

- `test_expression_gates_doc.py::test_c08_review_judges_reader_baseline_in_analyze_and_review` requires the review face at both `analyze` and `review`, names `review-sdd-process` and `review-template.md`, requires the reader-baseline wording, and forbids the review face from reusing the code-review object (`编译|测试|覆盖率`). None of that is edited; the new code segment is an additional segment, and a contract clause states that the receipt's coverage counts *reviewed files*, never test or compile coverage, so the two objects cannot be confused by a later reader.
- `test_expression_compatibility.py` freezes 51 layer-qualified skill units and `test_migration_distribution.py` freezes 27 commands / 51 skills. This feature adds neither a command nor a skill; both baselines stay untouched.
- `test_flat_internal_skill_migration.py` and `test_run_skills_wiring.py` pin the nested-skill layout and the wiring surface; the new subcommands live inside the existing script entity, so no new wiring site exists for them to miss.

**Red-first**: each new test is written against the not-yet-changed surfaces and recorded failing before the edit; a test whose subject can break without it going red is not counted as coverage.

## R12 — Same-author analysis gate: unavailability, disclosed

**Decision**: the Constitution Check table and the Post-Generation Quality Gate in this run are self-scored, and that fact is disclosed per the fallback rule of `shared/workflow/objective-analysis-gate.md` § 7.

**Measured condition**: this planning run scores design artifacts it wrote minutes ago in the same session (`requirements.md` came from an earlier independent stage subagent, but `plan.md`, `research.md`, `data-model.md` and `contracts/` are all authored here). The gate's rule 1 requires delegating detection to fresh-context read-only subagents. **This execution environment exposes no subagent dispatch capability** (the available tool set is file read/write/edit, shell, glob and grep — there is no Agent/Task dispatch), so dispatch cannot fail twice; it cannot be attempted at all.

**Handling**: rather than let the fallback pass silently, every Constitution Check row carries the marker `(direct read, subagent unavailable)` and this section records the weaker evidence path, per rule 7's requirement that the fallback stay visible to the reader. The mitigation available without a subagent is mechanical: the checks that can be program-derived are *actually run* (`pre-analyze-check.py --stage plan`, `clause_extract.py`, `sync-mirrors.py --check`, the neighbouring contract suites), so the self-scored part is limited to the prose-level compliance evidence.

## R13 — Housekeeping decisions inside the fixed scope

**Decision**: Feature 071 advances `Draft → Planned`; no new Feature row is created; the specification path is unchanged; the feature detail gains the plan-stage record.

**Measured reason**: `tests/contract/test_migration_distribution.py` freezes the command and skill rosters, and `shared/workflow/feature-integration.md` § Feature Binding Rules forbids duplicate Feature IDs. The binding already exists (row 071 in `.specify/memory/features.md`, detail `.specify/memory/features/071.md`), so this stage only advances status and records the plan's key changes.

**Deviation recorded**: the plan setup script (`scripts/bash/create-new-plan.sh`) derives the spec directory by numeric prefix when the branch carries no numeric prefix, so it resolved `071-review-code-integration` and copied the template without switching branches. No branch was created or switched, consistent with the unattended-stage rule already recorded in the requirements' Assumptions (A1).

## R14 — Explicit non-decisions (so the next phase does not re-litigate them)

- **No second verdict source**: the merge gate keeps coming from the skill's script; the command never recomputes it (FR-023).
- **No receipt sidecar file**: the block lives inside the record (FR-014).
- **No new id family for code findings**: severity + file/line stays the locating form (requirements A6); only framework recommendations use the `REC-…` family.
- **No edit to `shared/workflow/expression-gates.md`**: the expression review face is unchanged by design; its contract test is left as the guard and re-run as evidence rather than re-worded.
- **No change to `docs/reference/commands/checklist.md`**: the checklist's transition row now points at the owner through `feature-integration.md`; the checklist command page never restated the criteria.
