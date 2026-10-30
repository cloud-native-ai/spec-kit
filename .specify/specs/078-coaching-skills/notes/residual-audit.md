# Residual Audit Verdict — Feature 078 (T026)

**Date**: 2026-10-30
**Clause**: `contracts/identity-and-wiring.contract.md` C-6 (residual rule), C-8 (verifiable surface)
**Verdict**: the retired literal survives in exactly one place, the `_OBSOLETE_SKILLS` tuple entry; every other face of the closed wiring surface carries zero live occurrences.

The candidate set is **not** a hand-written list. It is derived at run time by the guard copy
`tests/contract/test_coaching_wiring_contract.py` from three sources:

1. `scripts/python/sync-mirrors.py` → `MIRROR_PAIRS` (source side + mirror side);
2. `scripts/python/regen-command-copies.py` → the per-tool command-copy directories that exist
   (`specify_cli._ASSISTANT_COMMAND_DIRS`, filtered to present directories);
3. A10's residual hand-edited members no generator reaches, pinned as literals inside that test
   (`.qoder/agents`, the compiled `## Wrap-up` face, `.specify/memory/feedback/probe-map.md`,
   plus `templates/commands/skills.md`, `src/specify_cli/__init__.py`, the two authored docs).

`git grep -n` below is **diagnostic side evidence only**; the verdict is the guard test.

## 1. Guard run (the verdict)

Command:

```bash
/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest -q tests/contract/test_coaching_wiring_contract.py
```

Output (verbatim tail; the single red is the C-7 handoff to T027, whose subject is the four
frozen rosters, not a residual occurrence):

```text
...............F.                                                        [100%]
=================================== FAILURES ===================================
______________ test_c7_the_four_frozen_rosters_carry_the_new_name ______________

    def test_c7_the_four_frozen_rosters_carry_the_new_name():
        stale = [
            rel for rel in FROZEN_ROSTERS if NEW not in _read(ROOT / rel)
        ]
>       assert not stale, f"frozen roster(s) still lack the new name: {stale}"
E       AssertionError: frozen roster(s) still lack the new name: ['tests/contract/test_expression_compatibility.py', 'tests/contract/test_migration_distribution.py', 'tests/contract/test_skill_layer_visibility_guards.py', 'tests/contract/test_run_skills_wiring.py']
E       assert not ['tests/contract/test_expression_compatibility.py', 'tests/contract/test_migration_distribution.py', 'tests/contract/test_skill_layer_visibility_guards.py', 'tests/contract/test_run_skills_wiring.py']

tests/contract/test_coaching_wiring_contract.py:412: AssertionError
=========================== short test summary info ============================
FAILED tests/contract/test_coaching_wiring_contract.py::test_c7_the_four_frozen_rosters_carry_the_new_name
1 failed, 16 passed in 1.85s
```

Reading: 16/17 green. The sixteen green legs are C-1 (8/8 coordinates), C-2 (candidate set is
derived, not restated), C-3 (probe compile, mirrors and command copies zero drift), C-4 (entity
directory removed, user symlink kept), C-5 (external classification), C-6 (no live occurrence;
one permitted occurrence; four named faces at zero; old mirror gone), C-8 (verification surface
green). The one red is C-7 — T027's own deliverable — and it is red for a **missing new name**,
not for a surviving old one.

## 2. Candidate faces derived at run time

The guard's own `_candidate_faces()` / `_live_occurrences()` functions were invoked directly
(import the module from its path, no test rewrite) to print the per-face census. The sanctioned
`OBSOLETE-ASSET-REGISTRY` block is stripped before counting, which is why the CLI file reads 0
live occurrences while still holding the one permitted tuple entry.

```text
.claude/commands: files=27 live_occurrences=0
.github/prompts: files=27 live_occurrences=0
.opencode/command: files=27 live_occurrences=0
.qoder/agents: files=7 live_occurrences=0
.qoder/commands: files=27 live_occurrences=0
.specify/agents/templates: files=3 live_occurrences=0
.specify/memory/feedback/probe-map.md: files=1 live_occurrences=0
.specify/scripts: files=117 live_occurrences=0
.specify/shared: files=60 live_occurrences=0
.specify/skills: files=406 live_occurrences=0
.specify/skills/internal: files=136 live_occurrences=0
.specify/templates: files=22 live_occurrences=0
agents: files=3 live_occurrences=0
docs/reference/agents/command-and-skills.md: files=1 live_occurrences=0
docs/tutorials/quickstart.md: files=1 live_occurrences=0
scripts: files=117 live_occurrences=0
shared: files=60 live_occurrences=0
skills/external: files=406 live_occurrences=0
skills/internal: files=136 live_occurrences=0
src/specify_cli/__init__.py: files=1 live_occurrences=0
templates: files=22 live_occurrences=0
templates/commands/skills.md: files=1 live_occurrences=0
faces=22 files_total=1608
```

22 derived faces, 1608 files, zero live occurrences on every one. The duplicate `skills/external`
/ `.specify/skills` pair and the `scripts` / `.specify/scripts` pair are the two sides of their
mirror pairs, counted separately on purpose.

## 3. The four named faces, read directly

Raw occurrence counts (no registry stripping — a stricter reading than the guard's):

```text
.qoder/agents: files=7 occurrences=0 hit_files=[]
.specify/agents/templates: files=3 occurrences=0 hit_files=[]
.specify/shared/definitions: files=12 occurrences=0 hit_files=[]
.specify/memory/feedback/probe-map.md: files=1 occurrences=0 hit_files=[]
src/specify_cli/__init__.py: occurrences=1
  line 892: '    "think-skills",'
```

- `.qoder/agents` — 0. The rendered host agents were re-rendered in T023.
- `.specify/agents/templates` — 0. Mirror of `agents/`.
- `.specify/shared/definitions` — 0. Mirror of `shared/definitions/`; the ledger and probe rows
  name `skill:coaching-skills` / `skill-coaching-skills-wrapup`.
- `.specify/memory/feedback/probe-map.md` — 0. Rebuilt by `probe-utils.py --action map`.
- `src/specify_cli/__init__.py` — exactly 1, and it is the tuple entry itself, inside the
  sanctioned `OBSOLETE-ASSET-REGISTRY` block. That is A10's one permitted difference.

## 4. Diagnostic side evidence (not the verdict)

```bash
git grep -n "think-skills" -- .qoder/agents .specify/agents/templates \
  .specify/shared/definitions .specify/memory/feedback/probe-map.md src/specify_cli/__init__.py
```

```text
src/specify_cli/__init__.py:892:    "think-skills",
```

Same conclusion as the guard: one line, in the cleanup registry. This grep is scoped to the
diagnostic faces above and is deliberately **not** a repo-wide count — SC-006 is scoped to A10,
and a repo-wide `git grep -c` would only count historical records that A9 forbids rewriting.

## 5. History boundary (not in the surface, not rewritten)

Per FR-024 / A9 the following stay as dated records and were not touched:
`.specify/specs/**` other than this feature, `memory/evidence/**`, `features/` of other IDs,
reviews, eval-baseline, and run/feedback records archived under the old `skill:think-skills`
unit id. This feature's own artifacts (`.specify/specs/078-coaching-skills/**`,
`.specify/memory/features/078.md`, the new run/feedback records) are **not** history and are
written under the new name, starting from an empty history.
