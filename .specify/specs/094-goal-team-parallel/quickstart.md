# Quickstart — Feature 094

Nine walks. S-0 is preflight and must run first; S-1…S-8 each start from a state S-0 produces. Every command runs from
the repository root. Paths are repo-relative here because the reader runs them here; the evidence records the absolute
path each reading was taken from.

Two premise notes apply to the whole page: (a) the engine actions named below (`bind`, `binding`, `migrate-archive`,
`probe-residual`, `handoff-decision`, `create`) do not exist until `/speckit.implement` lands them, so their examples
are pinned by the contract suite rather than run in this stage; (b) the fixture trees live under the sanctioned
`.specify/.tmp/` root and are removed by the walk's own teardown.

## S-0 — Preflight

```bash
python3 --version                                   # premise: >= 3.8 (host measured 3.11.11)
python3 -m pytest --version
python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:094-goal-team-parallel"
bash scripts/bash/run-tests.sh --names-out /tmp/baseline-names.txt -q
```

Expected: the lookup prints `flow_class: execution` and exits 0; the collected serial failing set is written out. That
set — not a parallel-mode count — is the GATE-1 comparison surface for every later reading.

Three measured cautions, all taken this stage. `run-tests.sh` writes ids **without** their directory (a file under
`tests/contract/` appears as a bare `test_*.py::…`), so compare against a list produced by a plain
`pytest -q | grep '^FAILED'`. The script also leaves an output file beside its target, which is why the target above is a
temp path. And its default is parallel: the parallel reading and the serial reading of this tree agree on 46 ids each but
differ by one swapped pair, so the comparison is name-level against the serial list and that pair is carried as a known
edge rather than read as a regression.

## S-1 — A command run owns a goal and a team

```bash
# fixture: a spec directory with no goal/ or team/ subdirectory
mkdir -p .specify/.tmp/s094/s1/.specify/specs/900-fixture
cd .specify/.tmp/s094/s1
python3 ../../../../scripts/python/goal-utils.py create demo-command-goal \
  --objective "the feedback bundle is triaged and answered" --scope goal
python3 ../../../../scripts/python/goal-utils.py binding goal demo-command-goal --json
```

Expected: the definition lands at `.specify/goal/demo-command-goal/goal.md`; `binding` reports `owner`,
`owner_id`, `origin`; `.specify/specs/` gains **no** goal/team path (SC-001). Writing with `--scope spec` exits 2 with
`invalid choice` (C-9).

## S-2 — Migration dry run on the real tree

```bash
python3 scripts/python/goal-utils.py probe-residual --json > .specify/specs/094-goal-team-parallel/test-evidence/residual-before.json
python3 scripts/python/goal-utils.py migrate-archive --dry-run --json > .specify/specs/094-goal-team-parallel/test-evidence/migration-dryrun.json
```

Expected: the dry run prints one decision per definition and creates **no** `.specify/archive/goal-team/` directory
(C-42). The residual reading is compared against `test-evidence/requirements-baseline-probe.txt`.

## S-3 — Migration applied

```bash
python3 scripts/python/goal-utils.py migrate-archive --apply --json > .specify/specs/094-goal-team-parallel/test-evidence/migration-applied.json
python3 scripts/python/goal-utils.py probe-residual --json
ls .specify/archive/goal-team/receipts/
```

Expected: each definition exists at `.specify/goal/<slug>/goal.md` / `.specify/teams/<slug>/team.md`; residual count is
zero; one receipt per definition carries `delete_policy: archive-not-delete`; every source tree is still readable under
`trees/` (SC-003, C-37).

## S-4 — Idempotency and conflict

```bash
python3 scripts/python/goal-utils.py migrate-archive --apply --json   # second run
```

Expected: zero writes, `result: noop` per definition, exit 0 (SC-004). A fixture whose target slug exists with a
different Objective exits 4 and names both candidate paths (C-40).

## S-5 — Rebind without touching the rest of the file

```bash
sha256sum .specify/goal/demo-command-goal/goal.md
python3 scripts/python/goal-utils.py bind goal demo-command-goal --owner sdd-run --owner-id r20261110T010000Z-900a
sha256sum .specify/goal/demo-command-goal/goal.md
python3 scripts/python/goal-utils.py binding goal demo-command-goal --json
```

Expected: ownership changes; the file-minus-binding hash is unchanged (SC-009, C-6). Once a team binds the goal, a
non-`human` write exits 2 naming the team (C-14).

## S-6 — Handoff on a complex spec

```bash
python3 scripts/python/goal-utils.py handoff-decision --tasks .specify/specs/094-goal-team-parallel/tasks.md --json
```

Expected: `direct` or `handoff` plus the measured task count and the declared threshold. In `handoff` mode the `tasks`
stage writes `<spec-dir>/handoff.md` whose `goal_slug`/`team_slug` resolve and whose reverse `handoff_ref` values point
back at the same file (SC-006). At or below the threshold no contract is forced (C-79 boundary `exclusive`).

## S-7 — The crew cannot rewrite the task table

```bash
python3 skills/internal/create-team/scripts/territory-check.py \
  --team .specify/teams/demo-crew/team.md \
  --path .specify/specs/094-goal-team-parallel/tasks.md
```

Expected: refused, non-zero exit, refusal text naming the path and the seat (SC-007, C-62). The named engine entry
point is fixed by `contracts/handoff-contract.md` C-62; the fixture command above is illustrative until
`/speckit.implement` lands the action. The spec side then reads `<spec-dir>/writeback/<T-NNN>.yaml` — one record per
completed task — and marks the task itself (C-65…C-67).

## S-8 — Residual probe after everything

```bash
python3 scripts/python/goal-utils.py probe-residual --json
ls .specify/archive/goal-team/trees/
```

Expected: zero residual; the archived trees are enumerable and no receipt lacks its `archived_path`.

## Teardown

```bash
rm -rf .specify/.tmp/s094
```

Expected: the fixture root is gone; `git status --short` shows no fixture path. Teardown runs after the last walk that
uses the fixtures, and before the closure suite — worktrees and fixtures under `.specify/.tmp/` are the duplicate-repo
trap measured in the execution-lessons record (`notes/execution-lessons-2026-11-09.md`).
