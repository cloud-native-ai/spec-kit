# Research & Decisions: SKILL_HOME / SKILL_WORKDIR

**Branch**: `012-skill-home-workdir` | **Date**: 2026-05-30 | **Plan**: [plan.md](plan.md)

This file records the three implementation-level decisions taken in Phase 0 of `/speckit.plan`. The first explicitly resolves the only item the clarify phase deferred to planning (BSD `readlink -f` portability). The other two anchor design choices that affect the template wording.

## Decision 1 — Portable script-self-locate idiom

**Decision**: Use POSIX `cd … && pwd -P` for the normative script-side resolution of `${SKILL_HOME}` and `${SKILL_WORKDIR}`. Do not depend on `readlink -f`, GNU coreutils, or Python 3 in the normative recipe.

**Normative recipe (FR-016)**:

```bash
SKILL_HOME="${SKILL_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd -P)}"
SKILL_WORKDIR="${SKILL_WORKDIR:-$(pwd -P)}"
```

**Why**:
- `pwd -P` is POSIX-defined to print the absolute, symlink-resolved path of the current working directory. Available on every shell we target (stock macOS `/bin/bash` 3.2, GNU `bash`, BusyBox `ash`, Alpine `sh`).
- `${BASH_SOURCE[0]:-$0}` resolves to the script's own path under bash; the `$0` fallback covers POSIX `sh` invocations where `BASH_SOURCE` is unset.
- The `${VAR:-fallback}` parameter expansion preserves any value the agent runtime exports (matches Clarifications Q3 in `requirements.md`).
- No new dependencies — every officially supported AI agent platform already has a POSIX shell.

**Assumption about script depth**: The `/..` segment assumes the conventional Skill layout `${SKILL_HOME}/scripts/<name>.sh`. The template will state this explicitly so authors with deeper script trees know to adjust the `..` count (e.g., `/../..` for `${SKILL_HOME}/scripts/sub/<name>.sh`).

**Alternatives rejected**:

| Alternative | Why rejected |
|-------------|--------------|
| `readlink -f` directly | Not available on BSD macOS without GNU coreutils; the whole motivation for this decision. |
| Python 3 `os.path.realpath` fallback | Adds a hard Python 3 dependency to every Skill shell script — far heavier than the problem. |
| Pure-shell symlink-walking loop | ~10 lines of boilerplate per script; defeats the "single named recipe" goal of FR-003. |
| Require `coreutils` install on macOS | Breaks the "install one Skill, run anywhere" promise of FR-007 / SC-003. |

**Conceptual recipe retained**: The user's original `dirname $(readlink -f SKILL.md)` example remains valid in prose contexts (e.g., when an agent or human is reasoning about the Skill's directory from a known SKILL.md path). The template will mark it as a *conceptual* recipe and direct authors to the FR-016 idiom for actual scripts.

## Decision 2 — Canonical written form vs. computation idioms

**Decision**: `${SKILL_HOME}` and `${SKILL_WORKDIR}` are the canonical written form in every context: SKILL.md prose, code blocks, examples, migration mapping, and prompts. The shell-form computation idioms are normative *examples* of how the variables get values; they do not change the written form.

**Why**:
- Aligns FR-007 (agent-engine-agnostic concepts) and FR-013 (non-shell agents resolve semantically).
- A single written syntax reduces author cognitive load: one symbol, one meaning, regardless of whether a shell will literally expand it or an LLM will substitute it.
- The `${...}` parameter-expansion syntax is recognizable across bash, POSIX `sh`, Make, many template engines, and is unambiguous in prose.

**Consequence for non-shell agents**: When an agent without shell execution reads `${SKILL_HOME}/scripts/init.sh`, it substitutes the Skill's resolved directory semantically. The template will include one explicit sentence to this effect (covers FR-013 and the "Variable expansion in non-bash contexts" edge case).

## Decision 3 — Scope of `CLAUDE.md` / `.specify/instructions.md` edits

**Decision**: No automatic edits to `CLAUDE.md` or `.specify/instructions.md` in this iteration. The contract test will include a grep assertion that no `SKILL_ROOT` reference remains in those two files; if the assertion fails, the task is to remove the stray reference at that point.

**Why**:
- FR-015 requires consistency, not unconditional edits. A grep of the current tree shows `SKILL_ROOT` only in `skills/create-skills/SKILL.md` and its `.specify/skills/create-skills/SKILL.md` mirror — both already in the edit scope.
- The Skills registry rows in `.specify/instructions.md` reference *canonical paths* (e.g., `.specify/skills/create-skills/SKILL.md`), not the variable name. No drift expected.
- Adding speculative edits to top-level instruction files would violate YAGNI (Principle VI).

## Open Items

None. The clarify-phase deferral is resolved (Decision 1), and the two design decisions are recorded. No `NEEDS CLARIFICATION` remains in `plan.md`.
