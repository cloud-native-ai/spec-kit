# Pre-Change Measurements — Feature 071 (implement start, T001)

**Captured**: 2026-10-27, before the first implementation edit of the implement stage (T001), at HEAD `30391ec38ac6de1466254d76febb66cb3ee54710`. Every row carries the real command and its real output; nothing here is quoted from an earlier stage. This note is the **control** T033 (mirror "no NEW drift") and T036 (closure) measure against: the verdict those rows owe is "no NEW drift / no NEW failure", **never** an absolute green, because several controls below already start non-zero.

## PM-1 Toolchain

```text
$ python3 --version
Python 3.11.11

$ python3 -m pytest --version
pytest 8.4.2

$ bash --version | head -1
GNU bash, version 4.4.20(1)-release (x86_64-koji-linux-gnu)

$ git --version
git version 2.43.5
```

## PM-2 Mirror baselines — three `sync-mirrors.py --check` scopes

```text
$ python3 scripts/python/sync-mirrors.py --check --only templates
scope --only: templates
ok    templates/ == .specify/templates/ (22 files)

$ python3 scripts/python/sync-mirrors.py --check --only skills/internal
scope --only: skills/internal
ok    skills/internal/ == .specify/skills/internal/ (136 files)

$ python3 scripts/python/sync-mirrors.py --check --only shared
scope --only: shared
ok    shared/ == .specify/shared/ (55 files)
```

All three `ok`, exit `0`. **Frozen file counts for T033: 22 / 136 / 55.**

## PM-3 Per-tool command copies

```text
$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
```

exit `0`.

## PM-4 Git snapshot

```text
$ git rev-parse HEAD
30391ec38ac6de1466254d76febb66cb3ee54710

$ git status --short
(no output — clean working tree)
```

The tree was clean before this stage's edits, so every measurement above is a genuine pre-change reading.

## PM-5 Five neighbouring suites — re-measured at implement start (per file)

```text
$ python3 -m pytest -q tests/contract/test_expression_compatibility.py   → 16 passed
$ python3 -m pytest -q tests/contract/test_run_skills_wiring.py          → 10 passed
$ python3 -m pytest -q tests/contract/test_migration_distribution.py     → 18 passed
$ python3 -m pytest -q tests/contract/test_flat_internal_skill_migration.py → 6 passed
$ python3 -m pytest -q tests/contract/test_review_p1_review_loop.py      → 10 passed
```

**Five-file total: 16 + 10 + 18 + 6 + 10 = 60 passed**, exit `0` — equal to the plan-stage frozen value (60 passed over the five neighbouring files in `test-evidence/regression-baseline.txt`, taken at base `884e7a86`). No drift between the plan-stage count and the implement-start count.

The five are the suites T035 re-runs plus the file that holds the one pin T030 changes (`tests/contract/test_review_p1_review_loop.py`), which R11 includes deliberately so the pin's pre-change green state is measured rather than assumed.

## PM-6 The separately-tracked expression-face suite

```text
$ python3 -m pytest -q tests/contract/test_expression_gates_doc.py
18 passed
```

**18 passed**, exit `0` — equal to the plan-stage frozen value. This is the count T027 compares against after the skill-body edits.

## PM-7 Existing pinned subjects this feature touches

```text
$ wc -l skills/internal/code-review/scripts/git-delta-review.sh skills/internal/code-review/SKILL.md
512 skills/internal/code-review/scripts/git-delta-review.sh
110 skills/internal/code-review/SKILL.md
```

Both files are unedited at this point (the subcommands T011/T012/T015/T017 add extend this one script entity — C-30).

## T002 companion — the implement-start failing-name baseline (consumed once)

```text
$ bash scripts/bash/run-tests.sh --names-out .specify/specs/071-review-code-integration/baseline-failed.txt
...
===== 26 failed, 5983 passed, 1 skipped, 3 warnings in 298.81s (0:04:58) ======
# failed-name list written: .specify/specs/071-review-code-integration/baseline-failed.txt (26 entries)
```

- **Exit code: 1** (pytest's own result — non-zero **because the repository already carries 26 pre-existing failures**, not because of any edit by this stage: the tree was clean at PM-4 and no source file was touched before this run).
- **26 entries** in the name list, which is the single name-level comparison anchor SC-006 and GATE-5 name. The later verdict is `comm -13 baseline-failed.txt <current failing names>` returning empty — zero **NEW** names — and never "a green suite".
- The failures are concentrated in `tests/unit/test_loop_state_engine.py` (9), plus contract suites unrelated to this feature (`test_clause_forms`, `test_compile_propagation_order`, `test_confirmation_gates_sweep`, `test_evidence_findings_schema`, `test_execution_config_engine`, `test_fast_fail_discipline`, `test_lifecycle_detach_reattach`, `test_mirror_parity_suite`, `test_neutrality_budget`, `test_proactive_trigger_section`, `test_scripts_distribution_parity`, `test_shared_reference_rewrite`, `test_shipped_surface_client_neutrality`, `test_token_efficiency_discipline`, `test_trigger_engine`). All 26 are pre-existing on this host at HEAD `30391ec3`; none names a file this feature edits.
- **Test budget**: this is the one and only full-suite run of the implement stage (the E2 `baseline` slot, `selection_basis=full-suite`). No later row re-captures it; the closure comparison (T036) re-runs the suites and diffs names against this file. The raw run log is kept outside git at `tmp/sdd-loop-071/full-suite-baseline.log`.
