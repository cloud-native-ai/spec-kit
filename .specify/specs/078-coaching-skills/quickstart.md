# Quickstart: Coaching Skills（教练技能）

**Feature**: 078 | **Plan**: [plan.md](./plan.md) | **Contracts**: [contracts/](./contracts/)

This quickstart has five scenarios. Scenarios 1 and 3 are shell-level verification; scenario 2 is an agent-level workflow (the skill is a prompt contract, not a program); scenario 4 exercises the degraded path; scenario 5 is teardown.

**Reading the verification notes.** Every command block below carries its own `Verification:` line with the premises it rests on. The reasons are per example, not file-wide: this spec's skill does not exist yet, so an example that needs it cannot be run in the plan phase, while an example that only needs an existing engine can be — and was.

---

## Scenario 1 — Wiring verification after implementation

### 1.1 Research a Trainee's class binding is not needed; verify the coach's own binding

```bash
python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "skill:coaching-skills"
```

Expected: `flow_class: execution`, `basis: behavior-oracle`, `source: ledger`, exit 0.

Verification: grammar proven by the pre-rename equivalent, which was executed in this phase —
`--unit-id "skill:think-skills"` returned `execution / behavior-oracle`, exit 0 (recorded in
`test-evidence/stage-plan-baselines.txt`). The new-name run was **not executed**: it requires the
ledger row that implementation adds. Premises: (a) a single ledger row `skill:coaching-skills` exists in
`shared/definitions/flow-class-definitions.md`; (b) the ledger keeps 79 rows (27 commands + 52 skills),
so the row replaces, rather than adds to, the old one.

### 1.2 Ledger and probe registry are internally consistent

```bash
python3 .specify/scripts/python/flow-class-check.py --action check
python3 scripts/python/probe-utils.py --action probes --validate
python3 scripts/python/probe-utils.py --action compile-embeds --check
```

Expected: `matched=79 inventory_units=79, clean`; probe validation exit 0; `75 units, zero drift`.

Verification: the ledger and compile-embeds commands were executed in this phase and returned
`matched=79 inventory_units=79, clean` and `75 units, zero drift`; the unit count does **not** change,
because the engine derives one unit per skill directory (23 command templates carry a `## Wrap-up` face
plus 52 skills = 75 on 2026-10-30) and a rename removes one unit while adding one. Premises: (a) exactly
one probe Object row is renamed; (b) the new skill body carries the compiled `## Wrap-up` block produced
by `--action compile-embeds`.

### 1.3 Derived faces carry no drift and no stale copy

```bash
python3 scripts/python/sync-mirrors.py --check
python3 scripts/python/regen-command-copies.py --check
test ! -e .specify/skills/think-skills
```

Expected: both checks exit 0 (no `DIFF` / `MISS` / `ORPHAN` lines); the third command exits 0.

Verification: both checks were executed in this phase and exited 0 on the pre-change tree, so the
criterion is “no NEW drift”. The third command was **not executed** (the old mirror still exists now).
Premises: (a) `sync-mirrors.py --write` ran after the rename; (b) the stale mirror directory was deleted
explicitly, because `sync-mirrors.py` never removes extras; (c) `regen-command-copies.py` ran after
`templates/commands/skills.md` changed.

### 1.4 Old name survives exactly once

```bash
/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest \
  tests/contract/test_coaching_wiring_contract.py -q
```

Expected: pass. That test is the guard copy: it derives the candidate set at run time (the six mirror
pairs from `MIRROR_PAIRS`, the per-tool copy targets from `regen-command-copies.py`, and A10's residual
hand-edited members pinned inside the test) and asserts the only surviving old-name occurrence is the
`_OBSOLETE_SKILLS` entry. The path list lives in that test, never in this quickstart — requirements
**A10** owns the closed surface and its allowed difference set, and a second prose list is exactly the
duplicate the analyze pass removed.

Verification: **not executed in the plan phase** (the test does not exist yet). Premises: (a) the
historical comment inside the OBSOLETE-ASSET-REGISTRY region is restated without the literal; (b) the
guard copy's A10 residue matches the requirements' closed surface; (c) `git grep -l` outside the
closed surface still finds records under `.specify/specs/**` and the feature registry, which A10/C-6
exclude by reference to A9 — a repo-wide count is a diagnostic, not the verdict.

### 1.5 Zero new blocking confirmation gates (SC-008 third condition)

```bash
BASE=d0f50759   # feature baseline; record the SHA in the evidence before running
git diff "$BASE" -- templates/commands skills shared 'templates/*.md' \
  | grep '^+' | grep -v '^+++' \
  | python3 -c '
import importlib.util, sys
spec = importlib.util.spec_from_file_location("gates", "scripts/python/scan-confirmation-gates.py")
gates = importlib.util.module_from_spec(spec); spec.loader.exec_module(gates)
lines = [line[1:].rstrip("\n") for line in sys.stdin if line.startswith("+")]
hits = [(i, line) for i, line in enumerate(lines, 1) if gates.BLOCKING_RE.search(line)]
print("added_lines=%d blocking_hits=%d" % (len(lines), len(hits)))
for i, line in hits: print("hit %d: %s" % (i, line))
sys.exit(1 if hits else 0)
'
```

Expected: `blocking_hits=0`, exit 0.

Verification: executed in this phase against `BASE=d0f50759`; all stage edits are under
`.specify/specs/`, outside the scanner's surface, so the reading was `added_lines=0 blocking_hits=0`
(exit 0). The pre-change reading of the same command and the scanner's total baseline (`blocking=27`,
destructive 20 + governance_kept 7, violations 0) are in `test-evidence/gate-newline-baseline.txt`;
this phase's reading is in `test-evidence/plan-fix-newline-gate.txt`. Premises: (a) the pathspec is
the scanner's own `SCAN_DIRS` + `SCAN_ROOT_FILES`, a subset of A10's closed surface, so the surface is
derived from the scanner and not re-listed; (b) `BASE` is the feature baseline commit, not the
previous stage commit, so every feature-added line inside the scan surface is counted.

---

## Verification boundary — FR → clause traceability

The FR → contract mapping is **owned by plan § Phase 1** (one row per FR). This feature declares
`account-clause-coverage.py`'s **FR lane not applicable**: that lane reads each clause block's
citation group, and these contracts deliberately use condition-shaped clauses without citation
groups, so the lane would report zero coverage by construction rather than by a missing mapping. The
clause lane is unaffected. The full statement, its cost and its reopening condition live in plan
§ Phase 1; this quickstart only points at the owner so the exemption is visible at the verification
surface.

---

## Scenario 2 — One coaching loop (agent-level)

This scenario is executed by an agent host, not by a shell. It is the acceptance path for SC-001…SC-005.

```text
User: coaching-skills memory-recall "Summarize what changed in the last three commits of this repo
      and list the files each commit touched."
```

Expected sequence, in this order:

1. `.specify/memory/coaching/<run-id>/expectation.md` exists **before** the first subagent action, with
   `## Outcome Correctness` (first row names the primary deliverable) and `## Process Efficiency`
   (steps magnitude, tool-call profile, retry budget, critical path).
2. One subagent runs `memory-recall` per its own `SKILL.md` and returns the summary; the real Trainee
   output exists.
3. `.specify/memory/coaching/<run-id>/observation.md` has one `## Dispatch` block and a step table whose
   rows each carry a source (`host-event`, `self-report`, or `observation-gap`).
4. `.specify/memory/coaching/<run-id>/deviations.md` has at least one finding per dimension when the
   fixture plants a defect and a slowdown, each citing a step id or artifact path.
5. `.specify/memory/coaching/<run-id>/improvement-plan.md` names a Trainee file and section per entry and
   ends with `## Run Status` carrying `run:` and `optimization:`.

Verification: **not executed in the plan phase** — neither the skill body nor the fixture Trainee exists
yet. Premises: (a) the host dispatches native subagents and exposes their events; where it does not, the
payload's `return-contract` makes `self-report` rows available; (b) the fixture plants one correctness
defect and one efficiency regression so SC-003 is decidable; (c) the run-id directory did not pre-exist.

---

## Scenario 3 — Upgrade a project that still has the old skill

```bash
# in a disposable fixture project that contains .specify/skills/think-skills/ (a real directory)
# and .specify/skills/think-skills-alias -> ../skills/coaching-skills (a user-authored symlink)
specify init --here --force --ai qoder
test ! -e .specify/skills/think-skills        # old entity directory removed
test -L .specify/skills/think-skills-alias    # user symlink preserved
```

Expected: both `test` commands exit 0.

Verification: **not executed in the plan phase** (the `_OBSOLETE_SKILLS` entry does not exist yet).
Premises: (a) `specify` on PATH is a build that contains the new `_OBSOLETE_SKILLS` entry, not the
repo's `.venv` copy; (b) `cleanup_obsolete_framework_assets()` skips symlinks and removes entity
directories — verified by reading the function, not by running it in this phase; (c) the fixture
project is disposable and outside the repository.

---

## Scenario 4 — Degraded path: no `improve-skills`, or no observation

```text
User: coaching-skills memory-recall "List every TODO marker in docs/ with file and line."
# in a fixture where improve-skills is removed from both layers
```

Expected: the Trainee's primary output is still delivered; `## Run Status` shows
`optimization: unavailable` and `run: success` (or `partial` when the Trainee's own criteria are not
met). The verdict ladder is owned by `data-model.md` § RunStatus: optimization status never caps a
completed execution.

```text
User: coaching-skills <trainee> "<work>"   # in a fixture whose subagent returns no log at all
```

Expected: `observation.md` states the total absence of observation, every improvement entry carries
`evidence: none`, and `run: partial`.

Verification: **not executed in the plan phase**. Premises: (a) the fixture removes both source and
mirror of `improve-skills` so “unavailable” is constructible; (b) the run status line is the only place
the two closed values are read.

---

## Scenario 5 — Teardown

```bash
rm -rf .specify/memory/coaching/20261030T101500Z-memory-recall
rm -f .specify/memory/coaching/.optimization-claims/memory-recall
test ! -e .specify/memory/coaching/20261030T101500Z-memory-recall
test ! -e .specify/memory/coaching/.optimization-claims/memory-recall
```

Expected: both `test` commands exit 0 — neither the run directory nor that Trainee's claim survives.

Verification: **not executed in the plan phase** — `.specify/memory/coaching/` does not exist yet.
Premises: (a) the run-id directory name and the Trainee slug are the ones the fixture run produced;
(b) the claim lives in the shared claim store of `data-model.md` § Optimization claim, keyed by Trainee
slug, so removing the run directory does **not** remove it — clearing it is a separate operator step,
taken only after confirming no live run owns it; (c) a fixture run that crashed mid-optimization leaves
a claim behind by design, and this teardown is how it is cleared — the skill itself never removes
another run's claim.
