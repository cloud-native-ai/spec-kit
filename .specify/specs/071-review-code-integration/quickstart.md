# Quickstart: exercising the composed review (071)

**Requirement → Feature**: `071-review-code-integration` → Feature 071 Review 命令与代码评审技能的组合与治理
**Scope**: operator-level scenarios for the composed `/speckit.review`. Each command block states its **execution status** and, when it could not be run at plan time, the exact premises it rests on — the flags, id forms, counts, and file locations a later stage must re-measure instead of inheriting.

> **Execution-status convention.** `EXECUTED` = the block was run during this planning stage against the real tool at commit `884e7a86`, and the pasted output is the actual output. `PINNED` = the block exercises a deliverable that this plan only designs; a named contract test pins the same command and its expected result, and the premises below are what that test asserts. Nothing in this file is written from intent alone.

## Scenario A — Resolve the feature-slice base (the rule this feature relies on)

The resolution rule is "explicit > parent of the first commit that added this feature's `requirements.md` > merge base with the default trunk". The instrument behind the middle tier is executed here, because the instrument exists today:

```bash
git log --diff-filter=A --format='%H %ad %s' --date=short -- .specify/specs/071-review-code-integration/requirements.md
git rev-parse 8d18265b^
```

**Execution status**: EXECUTED (2026-10-27).

```text
8d18265baf9d1aa8c4580339946411ddb082735f 2026-10-27 docs(071-review-code-integration): land the review × code-review composition requirements
e57052efa1c16871da4e24a56eabf7402b6fd87e
```

Reading: the feature slice starts at `e57052ef` — the parent of the commit that first added this feature's `requirements.md`. The same command run on an older feature resolves that feature's own freeze point; that is the property the tier exists for.

The tier order exists because the alternatives are measurably wrong **in this repository**:

```bash
git symbolic-ref refs/remotes/origin/HEAD   # → fatal: ref not a symbolic ref
git remote -v                               # origin is the UPSTREAM project, not this work
git merge-base main HEAD                    # → 926836e0… (far behind the feature slice)
```

**Execution status**: EXECUTED (2026-10-27). Premises: `main` exists locally and resolves to the upstream mirror `2dd1ca4f`; `master` is this work's branch at `884e7a86`.

The scripted form of the same rule:

```bash
bash skills/internal/code-review/scripts/git-delta-review.sh base \
  --spec .specify/specs/071-review-code-integration
```

**Execution status**: PINNED by `tests/contract/test_coverage_receipt.py` (the subcommand does not exist yet at plan time).
**Premises**: the subcommand is `base`; it accepts `--spec <dir>`, `--since <ref>`, `--json`; it prints `base=<sha>`, `head=<sha>`, `base_source=<tier>`; exit `0` on success and `2` when no tier resolves. Expected value for this repository after implementation: `base_source=feature-first-commit`, `base=e57052ef…`.

## Scenario B — A run that produces both conclusions

```text
/speckit.review
```

**Execution status**: PINNED by `tests/contract/test_review_code_composition.py` (template-level assertions; the command itself is a prompt, so the test pins the text, not a live run).
**Premises**: the feature has at least one commit after its `requirements.md` first commit touching non-spec files; the repository has a resolvable default trunk for the third base tier.

Expected observable result, in order:

1. `review.md` is written first (process segment), then `code-review.md` (code segment).
2. `review.md` § 2.1 lists base/head ids, base source, renderer mode, receipt counts, segment verdict, gate verdict, record path, archive path (`none` on a first run).
3. The closing summary prints both segments' conclusions.
4. The code severity words (`blocking` … `praise`) appear only in `code-review.md`; the process report shows `P0`/`P1`/`P2` only.

## Scenario C — A feature with no code delta

```text
/speckit.review
```

**Execution status**: PINNED by `tests/contract/test_review_code_composition.py`.
**Premises**: the feature's delta contains no file outside `.specify/specs/<key>/`, or the feature has produced no commit since its requirements first commit.

Expected: the code segment is recorded as `not-applicable` with a basis, no `code-review.md` is written, `review.md` § 2.1 still lists the reason and the verdict, and the process segment's reader-baseline conclusion is unchanged.

## Scenario D — No renderer on the host

```bash
DELTA_BIN=/nonexistent-delta bash skills/internal/code-review/scripts/git-delta-review.sh receipt \
  --review-file .specify/specs/071-review-code-integration/code-review.md \
  --renderer text
```

**Execution status**: PINNED by `tests/contract/test_coverage_receipt.py`, which drives the script with `DELTA_BIN` pointed at a non-existent binary — the substitution the script already supports through its `DELTA_BIN` variable.
**Premises**: `receipt` accepts `--review-file`, `--renderer`, `--since`; the environment has no `delta` on `PATH` in the test process; the record already exists (created by `start`).

Expected: exit `0` when the file sets match, the receipt block written with `renderer=text`, the record's marker reading `renderer: text`, and no sentence anywhere in the record claiming a rendered review.

## Scenario E — Gap drill (red first, then green)

```bash
# 1. create/replace the record, capture the current delta's files
bash skills/internal/code-review/scripts/git-delta-review.sh start \
  --spec .specify/specs/071-review-code-integration
# 2. judge every file (repeated per file)
bash skills/internal/code-review/scripts/git-delta-review.sh note \
  --review-file .specify/specs/071-review-code-integration/code-review.md \
  -s suggestion -f templates/commands/review.md -c "example opinion"
# 3. write the receipt
bash skills/internal/code-review/scripts/git-delta-review.sh receipt \
  --review-file .specify/specs/071-review-code-integration/code-review.md
# 4. remove one per-file entry by hand, then re-run step 3 → must go red
```

**Execution status**: PINNED by `tests/contract/test_coverage_receipt.py`, which performs the remove-one-entry step in a temporary git repository.
**Premises**: the temporary repository has two commits and a resolvable base; `start` writes the header and (on a second run) archives the previous record; `receipt` exits `0`/`1`/`2` per `contracts/coverage-receipt.md`; the `note` subcommand already exists and keeps its six-level validation.

Expected: step 3 exits `0` with `gap_files=0`; after deleting one `file.<NN>.*` line, step 3 exits `1` and the block is rewritten with `gap_files` equal to the number of unjudged files; restoring the entry returns exit `0`.

## Scenario F — Focused review of an oversized diff

```bash
bash skills/internal/code-review/scripts/git-delta-review.sh receipt \
  --review-file .specify/specs/071-review-code-integration/code-review.md \
  --skip-with-reason "src/legacy/**" --reason "size guard: focused pass"
```

**Execution status**: PINNED by `tests/contract/test_coverage_receipt.py`.
**Premises**: `receipt` accepts a repeatable skip selector plus its required reason; a skipped entry is legal (exit `0`) and counted in `skipped_files`.

Expected: exit `0`, `skipped_files > 0`, and the segment verdict **not** `pass` — `blocked` when unresolved `blocking` items exist, otherwise `not-evaluated`.

## Scenario G — The gate verdict, from the explicit record only

```bash
bash skills/internal/code-review/scripts/git-delta-review.sh report --summary \
  --file .specify/specs/071-review-code-integration/code-review.md
echo "exit=$?"
```

**Execution status**: PINNED by `tests/contract/test_status_gate_owner.py`.
**Premises**: `report --summary` keeps its current display, gains `--file`, and returns `0` = allow, `1` = an unresolved `blocking` item exists, `2` = input error. Omitting `--file` keeps the legacy newest-file selection and labels it as implicit.

Expected: with one `blocking` entry present, exit `1` and the printed reason naming the count; after the entry is resolved (or explicitly waived by the user and recorded), exit `0`.

## Scenario H — Where a finding may and may not go

```text
/speckit.feedback
```

**Execution status**: PINNED by `tests/contract/test_review_feedback_boundary.py`.
**Premises**: the feedback store is the project-local `.specify/memory/feedback/`; the engine's entry key is `(unit_id, run_id)`; both units (`/speckit.review` and `skill:code-review`) are already registered in the probe registry, so no wrap-up recompilation is needed.

Expected: a framework friction item (a receipt gap, a missing renderer) is a legal entry; a code defect copied out of `code-review.md` is a violation of the written classification duty; the review command's closing step list is unchanged; nothing is transmitted automatically.

## Regression commands (run before and after the change)

```bash
python3 -m pytest tests/contract/test_expression_gates_doc.py -q
python3 -m pytest tests/contract/test_expression_compatibility.py tests/contract/test_run_skills_wiring.py \
  tests/contract/test_migration_distribution.py tests/contract/test_flat_internal_skill_migration.py \
  tests/contract/test_review_p1_review_loop.py -q
python3 scripts/python/sync-mirrors.py --check --only templates
python3 scripts/python/sync-mirrors.py --check --only skills/internal
python3 scripts/python/sync-mirrors.py --check --only shared
python3 scripts/python/regen-command-copies.py --check
```

**Execution status**: EXECUTED (2026-10-27) on the pre-change tree; output recorded in `test-evidence/regression-baseline.txt`.
**Measured results to compare against**: 18 passed; 60 passed over the five files; `ok templates/ (22 files)`; `ok skills/internal/ (136 files)`; `ok shared/ (55 files)`; `OK: all per-tool command copies match the source templates.` The implementation criterion is **no NEW failure and no NEW drift**, not a green run — the counts above are the measurement, and a later run is compared against them by name.
