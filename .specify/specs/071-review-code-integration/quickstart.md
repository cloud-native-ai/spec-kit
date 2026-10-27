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
**Premises**: the subcommand is `base`; it accepts `--spec <dir>`, `--since <ref>`, `--trunk <ref>`, `--head <ref>`, `--json`; it prints `base=<sha>`, `head=<sha>`, `base_source=<tier>`; exit `0` on success and `2` when no tier resolves. Expected value for this repository after implementation: `base_source=feature-first-commit`, `base=e57052ef…`, `head=` the `HEAD` read once at run start. Trunk order, used only when the feature-first-commit tier fails: explicit `--trunk` > a resolvable `refs/remotes/origin/HEAD` > an existing `main` > an existing `master` > `not-evaluated`. Head carries no source tier: it is the explicit `--head` or the run-start `HEAD`, fixed for the run, and the range MAY contain commits unrelated to this feature (a strict slice passes the feature's last commit as `--head`).

## Scenario B — A run that produces both conclusions

```text
/speckit.review
```

**Execution status**: PINNED by `tests/contract/test_review_code_composition.py` (template-level assertions; the command itself is a prompt, so the test pins the text, not a live run).
**Premises**: the feature has at least one commit after its `requirements.md` first commit touching a path the code-path predicate counts as code (the predicate's closed default set lives in the skill script; `--code-paths` overrides it); the repository has a resolvable default trunk for the third base tier.

Expected observable result, in order:

1. `review.md` is written first (process segment), then `code-review.md` (code segment).
2. `review.md` § 2.1 carries the closed content list: base and head ids with the base source, renderer mode, the four receipt counts **copied from the receipt block** (changed / judged / skipped / gap), the segment verdict, the gate verdict, the uncommitted-scope disclosure when the tree is dirty, and the record path with this run's archive path ([[STR-009]] on a first run).
3. The two verifiable carriers are that subsection and the bound feature detail's `## Latest Review` review-record entry — the entry gains a line, not a new structured field. The closing summary MAY restate both; it is a presentation and is not a third verifiable artifact.
4. The code severity words (`blocking` … `praise`) appear only in `code-review.md`; the process report shows `P0`/`P1`/`P2` only.

## Scenario C — A feature with no code paths in its delta

```text
/speckit.review
```

**Execution status**: PINNED by `tests/contract/test_review_code_composition.py`.
**Premises**: the feature's committed delta contains no file the code-path predicate counts as code (spec, docs and memory paths are expressly not code paths), **or** the delta is empty (base and head at the same commit, zero changed files — triaged before the receipt runs, so no 0/0/0 receipt can report a clean review of nothing).

Expected: the code segment is recorded as `not-applicable` with the predicate's basis, **no `code-review.md` is created at all** (no empty record either), `review.md` § 2.1 still carries the reason and the verdict, the feature detail entry repeats it, and the process segment's reader-baseline conclusion is unchanged. A `not-evaluated` outcome (unresolvable base, unusable repository) behaves the same way: no record file, reason in the report subsection and the feature detail entry.

## Scenario D — No renderer on the host

```bash
DELTA_BIN=/nonexistent-delta bash skills/internal/code-review/scripts/git-delta-review.sh receipt \
  --review-file .specify/specs/071-review-code-integration/code-review.md \
  --renderer text
```

**Execution status**: PINNED by `tests/contract/test_coverage_receipt.py`, which drives the script with `DELTA_BIN` pointed at a non-existent binary — the substitution the script already supports through its `DELTA_BIN` variable.
**Premises**: `receipt` accepts `--review-file`, `--renderer`, `--since`; the environment has no `delta` on `PATH` in the test process; the record already exists (created by `start`).

Expected: exit `0` when the file sets match, the receipt block written with the text marker, the record's header marker reading [[STR-003]], and no sentence anywhere in the record claiming a rendered review.

**No-TTY case (the one that actually happens)**: the same rule keys on the terminal, not only on the binary. On this host `delta` *is* installed (`/home/agent/.cargo/bin/delta`) and every composed call is made by an agent through a pipe, so:

```bash
bash skills/internal/code-review/scripts/git-delta-review.sh receipt \
  --review-file .specify/specs/071-review-code-integration/code-review.md
```

**Execution status**: PINNED by `tests/contract/test_code_review_skill_contract.py` (the TTY branch does not exist yet, same reason as the block below).
**Premises**: stdout of the test process is not a TTY; `delta` may be present on `PATH`. Expected: the record carries [[STR-003]] and never [[STR-008]] — the rendered marker requires renderer **and** TTY, so an available renderer must not by itself produce a rendered-mode claim.

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

Expected: step 3 exits `0` with `gap_files=0`; after deleting one `file.<NN>.*` line, step 3 exits `1` (coverage gap) and the block is rewritten with `gap_files` equal to the number of unjudged files; restoring the entry returns exit `0`. Two further cases belong to the same drill: replacing a legal skip reason with a value outside the closed set owned by `requirements.md` FR-014 also exits `1` (an unrecognised reason is a gap, not a skip), and an unresolvable base or a missing record exits `2` (cannot evaluate) with no block written — the alphabet is `0` / `1` / `2` with one meaning each, never a fourth code and never `1` for `2`.

## Scenario F — Focused review of an oversized diff

```bash
bash skills/internal/code-review/scripts/git-delta-review.sh receipt \
  --review-file .specify/specs/071-review-code-integration/code-review.md \
  --skip-with-reason "src/legacy/**" --reason size-guard-focus-not-reviewed
```

**Execution status**: PINNED by `tests/contract/test_coverage_receipt.py`.
**Premises**: `receipt` accepts a repeatable skip selector plus its required reason, and the reason MUST be one of the five values of the closed set owned by `requirements.md` FR-014 (`size-guard-focus-not-reviewed` is the focus case; free text is not accepted and would make the run a gap); a skipped entry is legal (exit `0`) and counted in `skipped_files`.

Expected: exit `0`, `skipped_files > 0`, and the segment verdict **not** [[STR-006]] — [[STR-007]] when the current record contains `blocking` entries, otherwise [[STR-002]].

## Scenario G — The gate verdict, from the explicit record only

```bash
bash skills/internal/code-review/scripts/git-delta-review.sh report --summary \
  --file .specify/specs/071-review-code-integration/code-review.md
echo "exit=$?"
```

**Execution status**: PINNED by `tests/contract/test_status_gate_owner.py`.
**Premises**: `report --summary` keeps its current display, gains `--file`, and returns `0` = allow, `1` = the current record contains at least one `blocking` entry, `2` = input error. Omitting `--file` keeps the legacy newest-file selection and labels it as implicit.

Expected: with one `blocking` entry present, exit `1` and the printed reason naming the count. The condition is an existence test over the current record only — there is no "cleared" state — so re-running the code segment and producing a record with zero `blocking` entries makes the same command exit `0`; nothing is "resolved" in place. A waiver is legal only as an explicit user ruling (a user-authored artifact or the user's own ruling, never a driver's confirmation), and without one the unattended disposition is halt-and-report with [[STR-010]] as the named refusal literal.

## Scenario H — Where a finding may and may not go

```text
/speckit.feedback
```

**Execution status**: PINNED by `tests/contract/test_review_feedback_boundary.py`.
**Premises**: the feedback store is the project-local `.specify/memory/feedback/`; the engine's entry key is `(unit_id, run_id)`; all three units (`/speckit.review`, `skill:review-sdd-process`, `skill:code-review`) are already registered in the probe registry, so no wrap-up recompilation is needed.

Expected: a framework friction item (a receipt gap, a missing renderer) is a legal entry; a code defect copied out of `code-review.md` is a violation of the written classification duty; the review command's closing step list is unchanged; nothing is transmitted automatically; and the run leaves three unit records rather than one merged or two truncated ones.

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
