# Quickstart Runs — Feature 063

## S1 — medium fixture admitted

- Preparation: quickstart §准备 (`git init`, base commit, branch `012-medium`).
- Command: `python3 skills/external/sdd-loop-driver/scripts/admission-check.py --project "$FIXTURE" --base-ref "$BASE" --expected-branch 012-medium --requirements ... --tasks ... --checklists ... --entry-evidence ... --lines-manifest ... --json-out /tmp/063-admission.json`
- Exit: `0`
- JSON: `decision=fast-lane`, `measured.fr_count=12`, `measured.task_count=25`, seven criteria all `pass`, `checklist=skipped(fast-lane)`.
- Re-run after the mutation drill: same result (`0`, `fast-lane`, 12/25).

## S2 — large fixture refused fail-closed

- Command: the S1 form with `$FIXTURE_LARGE`, `--expected-branch 013-large`.
- Exit: `1`
- JSON: `decision=full-chain`, `measured.task_count=60`, criterion `a` = `fail`.
- Re-run after the mutation drill: same result (`1`, `full-chain`, 12/60).

## S3 — pending (US2)

## S4 — pending (US4)

## S5 — pending (US4)

## S6 — pending (US3)

## S7 — pending (US5, recorded dry-run decision trace; non-CI)
