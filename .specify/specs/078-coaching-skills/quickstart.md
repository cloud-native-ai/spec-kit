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
git grep -n "think-skills" -- \
  skills/external/coaching-skills skills/internal/run-skills/SKILL.md \
  templates/commands/skills.md agents/skill-verifier.agent.md agents/structure-adjuster.agent.md \
  skills/internal/create-agent/templates shared/definitions src/specify_cli/__init__.py \
  docs/reference/agents/command-and-skills.md docs/tutorials/quickstart.md \
  tests/contract .specify/skills
```

Expected: one hit — the `_OBSOLETE_SKILLS` tuple entry in `src/specify_cli/__init__.py`.

Verification: **not executed for the post-rename state** (it would find the pre-rename tree). Premises:
(a) the historical comment inside the OBSOLETE-ASSET-REGISTRY region is restated without the literal;
(b) every listed path is part of the closed surface defined by `contracts/identity-and-wiring.contract.md`
C-2/C-3, and historical records outside that list are intentionally excluded.

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
`optimization: unavailable` and `run: success` (or `partial` when the Trainee's own criteria are not met).

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
test ! -e .specify/memory/coaching/20261030T101500Z-memory-recall
```

Expected: the second command exits 0; no `.optimization-claim` file survives under
`.specify/memory/coaching/`.

Verification: **not executed in the plan phase** — `.specify/memory/coaching/` does not exist yet.
Premises: (a) the run-id directory name is the one the fixture run produced; (b) the claim file lives
inside that directory, so removing the directory removes the claim; (c) a fixture run that crashed
mid-optimization leaves a claim behind by design, and this teardown is how it is cleared — the skill
itself never removes another run's claim.
