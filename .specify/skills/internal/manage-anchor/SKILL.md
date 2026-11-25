---
name: manage-anchor
description: Author and manage Anchor definitions in the anchor archive — the executable core of `/speckit.anchor`. Runs the seven modes (create / view / modify / targets / migrate / migrate-archive / coordinate) through the definition engine: the four-element interview for a new Anchor (outcome objective, at least one verifiable success criterion, identity, optional Targets), the read/write engine grouping with exit-code verdicts, the single destructive write (criteria --clear) behind explicit approval, Target slice authorization with GD-2/GD-3 shape checks, per-team migration from an inline goal, the one-time move of spec-local legacy trees into the unified archive, and territory re-division proposals across teams bound to one Anchor. Every write goes through the engine — the anchor archive is engine-write-only. Use this when the user mentions ["anchor", "锚点", "项目级目标", "远期目标", "anchor definition", "objective", "成功判据", "success criteria", "targets", "目标切片", "migrate anchor", "锚点迁移", "migrate-archive", "档案迁移", "coordinate", "锚点协调", "anchor archive", "anchor_slug", "anchor achieved", "anchor abandoned"].
classification: internal
skill_id: "<SKILL:.specify/skills/internal/manage-anchor/SKILL.md>"
---

# manage-anchor

> **Concurrency obligation（执行义务，按指针抵达）**: this skill is an execution body — before the first real action, run the one-shot assessment (class → carrier → partition), default to concurrent execution for two or more independent units, and when serial name a reason code and record the `requested` / `effective` / `effective_reason` reading. Authored text: `shared/definitions/subagent-definitions.md` § The Concurrency Obligation; class table: `shared/declarations/facts/concurrency-class.yaml`; reason codes: `shared/declarations/facts/serial-reason.yaml`; reading fields: `shared/declarations/facts/effective-concurrency.yaml`. This body restates none of their rules.

## Goal

Own and execute the operations behind `/speckit.anchor` — the **sole authoring entry** for
anchor definitions in the anchor archive. An **Anchor** is an authored fact source (never a
derived artifact): a project-level, long-horizon end state measured by degree. This skill owns
only the *operations* (mode semantics, the four-element interview, execution ordering, engine
invocation). The anchor *concept* — composition, GD-2/GD-3 shape rules, the three archive
layers, the binding record, lifecycle, Target decomposition, the Anchor–Team binding — is
defined once in `.specify/shared/definitions/anchor-definitions.md`. **Link to that document;
never restate it.** Deterministic rules (identity grammar, three-part structure, lifecycle
table, change history, archive enumeration) live in `scripts/python/goal-utils.py`. Call the
engine; do not re-derive its judgments in prose.

**Non-negotiable boundary**: no skill, script, or other command may write an anchor definition
file **directly** — the definition engine (`goal-utils.py`) is its sole writing path, whether
driven by `/speckit.anchor` or carried as delegated logic behind it. Derived `summary/**`
subtrees are refreshed by the existing summary flow and are outside the definition write face.

Canonical extraction source: `templates/commands/anchor.md` § Outline. The command template
keeps entry, user-input handling, glossary pre-step, the named refusal of Goal-only surfaces,
and the wrap-up lifecycle only.

## Input Contract

- **Intent**: one of `create | view | modify | targets | migrate | migrate-archive |
  coordinate`, optionally with an anchor-slug or team-slug. Mode is inferred from the
  request and **disclosed with every run**.
- **Ambiguous input resolves to `view`** — which is read-only.
- **Reversibility**: execution proceeds directly for reversible actions
  (可逆动作自动执行，判据：`.specify/shared/guidelines/confirmation-gates.md`) — the single
  destructive write, named in step 4, is the exception.

**The mode table lives here and nowhere else** — this is its single home; the command template
cites it by path and enumerates no second copy.

| Mode | Purpose | Writes |
|------|---------|--------|
| `create` | archive a new anchor definition | `.specify/anchoring/<anchor-slug>/anchor.md` |
| `view` | list the anchor archive, or show one Anchor | nothing |
| `modify` | change the objective narrative, success criteria, or lifecycle state | the same definition file |
| `targets` | add / list / transition the Anchor's Targets (run-assignable scope slices) | the same definition file |
| `migrate` | derive an Anchor from a team's inline goal and switch that team to a reference | new `anchor.md` + that `team.md` |
| `migrate-archive` | move spec-local legacy goal/team trees into the unified archive (archive-not-delete; explicit, never implicit) | the two archive layers + receipts and archived trees |
| `coordinate` | propose a territory re-division across the teams bound to one Anchor | nothing until ratified, then each `team.md` |

The archive layers and the scope value set are owned by
`.specify/shared/definitions/anchor-definitions.md` § Archive Layers — this table cites the
landing points, never the value domain. The team side a `migrate` / `coordinate` run touches
lives at `.specify/teams/<slug>/team.md` (team concept:
`skills/internal/create-team/references/conceptual-model.md`).

`targets` is a modify-intent route: Target authorization, listing, and state transitions all
land through this single authoring entry — no other surface writes the `## Targets` section.
Concept: link `.specify/shared/definitions/anchor-definitions.md` (Target Decomposition), never
restate.

**Anchor-only, not Goal-side.** `targets`, `migrate`, `migrate-archive` and `coordinate` have
no action-level Goal form. An action-level Goal definition (`.specify/goals/**`) is never
written by this skill; that store and its four-mode entry belong to `/speckit.goal`. When a
caller actually asks for action-level guidance, hand the request to `/speckit.goal` rather
than stretching an Anchor mode to serve it.

## Workflow

### 1. Resolve context

Run `.specify/scripts/bash/check-prerequisites.sh --json --paths-only` for `REPO_ROOT`.
The anchor archive is `REPO_ROOT/.specify/anchoring/` (archive layers and scope value set:
`.specify/shared/definitions/anchor-definitions.md` § Archive Layers).

### 2. Determine the mode

From the request; state it back to the user.

### 3. Preview → execute

Before any write, show: the mode, the target path, and the exact content to be written
(or the diff for a modify) — then write directly (preview is **disclosure, not a blocking
gate**；事后修改经 `/speckit.anchor` modify). `view` stays read-only.

### 4. Execute via the engine — never hand-write a definition file

The block below fixes only the **read/write grouping**; every action's full flag set and
defaults are owned by `python3 scripts/python/goal-utils.py --help` and are not restated
here.

```bash
# 读组 — zero writes
python3 scripts/python/goal-utils.py list    # anchor archive listing (no `view` action)
python3 scripts/python/goal-utils.py validate <anchor-slug>
python3 scripts/python/goal-utils.py check-statement "<sub-outcome statement>"
python3 scripts/python/goal-utils.py targets <anchor-slug> --list
python3 scripts/python/goal-utils.py targets <anchor-slug> --check "<sub-outcome statement>"
python3 scripts/python/goal-utils.py probe-residual    # spec-local residual reading

# 写组 — mutates the archive through the engine
python3 scripts/python/goal-utils.py create <anchor-slug> --objective "<desired end outcome>"
python3 scripts/python/goal-utils.py objective <anchor-slug> --set "<revised outcome>"
python3 scripts/python/goal-utils.py criteria <anchor-slug> --criterion "<new>"
python3 scripts/python/goal-utils.py status <anchor-slug> --set achieved
python3 scripts/python/goal-utils.py targets <anchor-slug> --add "<sub-outcome statement>"
python3 scripts/python/goal-utils.py targets <anchor-slug> --set done --id T-001
python3 scripts/python/goal-utils.py migrate <team-slug>
python3 scripts/python/goal-utils.py migrate-archive --dry-run   # then --apply
```

Exit codes: `0` ok · `2` input error (rejection) · `3` not found / migration interrupted ·
`4` validation failed / migration conflict · `5` blocked — the action table is the
engine's (`python3 scripts/python/goal-utils.py --help`). A non-zero exit is a **verdict**:
report it, never argue around it.

**破坏性写入**（桶归属见 `.specify/shared/guidelines/confirmation-gates.md` §破坏性动作清单）：`criteria <anchor-slug> --clear` 以空值覆盖既有判据集。引擎对缺参的 `criteria` 调用一律 exit 2——它 MUST NOT 被读成查看入口，也不会静默清空；传 `--clear` 之前 MUST 先取得用户明示批准。其余写入均为可逆动作：直接执行，按执行报告呈现，事后经 `/speckit.anchor` modify 修改。

`create` 另接受两个可选附注——`--title`（可读标题，身份仍是 slug）与 `--boundary`（排除项）：仅在用户自行陈述时携带，MUST NOT 为此发问，step 5 的收集集不因它们扩张。概念见 `.specify/shared/definitions/anchor-definitions.md`。

`targets` notes:

- the engine renders the `## Targets` section (never hand-edit it);
- statements pass the same GD-2/GD-3 shape check at slice scale and must not restate a
  success criterion;
- terminal Anchors are read-only; terminal Target identities are never reused;
- a terminal-state Target reported by a run is a **review bifurcation**: verify by hand —
  if genuinely done, stop; if evidence contradicts, reopen via
  `targets <slug> --set open --id <T-nnn>` and re-issue the run. There is no
  terminal-execution bypass.

### 5. Interview for `create` — exactly four things, nothing else

Ask them per the interview pattern (`.specify/shared/patterns/interview-pattern.md`):
**open** questions carrying their context, no option menus and no recommended answers
(the objective and its slices are the user's to state, not yours to propose), facts looked
up rather than asked, each answer written through before the next round.

1. **the objective**: the desired end *outcome*. If the user describes steps, say so and
   ask for the outcome instead (the engine rejects task lists as GD-2).
2. **success criteria**: **at least one** verifiable condition — a definition carrying zero
   is not an Anchor (concept: `.specify/shared/definitions/anchor-definitions.md` § What an
   Anchor Is, link, never restate). Collect until one exists; never create an Anchor without
   it and never invent one on the user's behalf. Verifiable ≠ machine-checkable: a criterion
   whose measurement route is **manual/human review** (a named reviewer judging the end
   state, recorded by degree) is an equally legitimate form. Say so out loud when asking, so
   the user does not withhold a real criterion because no program can measure it.
3. **the identity**: a slug that is also the directory name. Reuse `anchor_slug` semantics;
   do not invent a second identifier.
4. **Targets** (optional annex — concept: Target Decomposition in
   `.specify/shared/definitions/anchor-definitions.md`, link, never restate): zero or more
   sub-outcome statements under the confirmed objective. Zero is legal — an Anchor without
   Targets is fully valid and this item may be skipped entirely. Each statement must be
   outcome-shaped at slice scale (GD-2), a slice of this objective rather than an
   independent end state (GD-3), and must not restate a success criterion. Collect only
   statements the user states — in this mode you never draft slices on their behalf.

If the objective bundles several objectives the engine rejects it as GD-3 — help the user
split it into separate Anchors, each with its own directory and lifecycle.

**Execution order**: write the definition first (`create`), then land each collected
Target statement through the engine — `targets <anchor-slug> --check "<statement>"` for the
dry-run verdict, `targets <anchor-slug> --add "<statement>"` to authorize; never hand-write
the `## Targets` section. A rejected statement is a verdict: report it, let the user
reword or drop it, and continue with the rest — the already-created Anchor is never rolled
back for a rejected slice.

### 6. `migrate <team-slug>`

Read that team's inline goal, derive an Anchor definition whose objective and criteria are
semantically equivalent, create it, then set the team's `anchor_slug` to the new identity.
**Never** delete the team's inline goal — retention is the user's choice, and migration is
per-team and optional.

### 7. `migrate-archive`

Move the spec-local legacy goal/team trees into the unified archive — both kinds in one
explicit call, archive-not-delete (each source tree is archived, never deleted) and never
invoked implicitly as a side effect of another run. Present the `--dry-run` plan before
`--apply`; a per-definition conflict is a verdict, and an interrupted run is resumed by a
second call rather than restarted. The flags, receipt shape and exit codes are owned by the
engine's action table (`python3 scripts/python/goal-utils.py --help`). `/speckit.sanitize`
offers only the read-only residual reading — never a migration.

### 8. `coordinate <anchor-slug>`

The mechanism detects overlap and **proposes** a re-division with its rationale. It writes
nothing. On the user's ratification, write the agreed territory back into each affected
`team.md` — never into the anchor directory.

## Boundaries

- **Engine-write-only (non-negotiable)**: the definition is **authored**. No derived flow
  may write `anchor.md`; no skill, script, or other command may write into the anchor
  archive directly — `goal-utils.py` is its sole writing path. The summary refresh writes
  only `<anchor-slug>/summary/**`.
- **WD-2 applies**: objective and Target statements state outcomes, not steps; the engine is
  the executable subject of that check.
- The Anchor's object is **unrestricted** — the framework itself, codebase-wide convention
  convergence, runtime outcomes. Never reject an Anchor because no functional requirement in
  this project implements it.
- Criteria are **measured by degree**, not per-clause pass/fail. Never render a criterion as
  a binary checkbox.
- Criteria are **cross-feature** and disjoint from any requirements spec's `SC-xxx`. Never
  copy criteria in either direction.
- `requirements.md` carries no anchor field and an Anchor never enumerates functional
  requirements. The two sit on different planes with no hierarchy.
- A team serves exactly one Anchor at a time (binding concept:
  `.specify/shared/definitions/anchor-definitions.md` § Anchor–Team Binding).
- Terminal Anchors (`achieved` / `abandoned`) stay archived. Deletion is not a lifecycle
  transition.
- This skill **never** writes `.specify/goals/**` and never issues a Goal-side operation;
  action-level guidance is `/speckit.goal`'s surface.

## Command-lifecycle surfaces (kept in `/speckit.anchor`)

Entry argument handling (`.specify/shared/workflow/user-input-protocol.md`), the glossary
pre-step (`.specify/glossary.md`, protocol `.specify/shared/workflow/glossary.md`), the
named refusal of Goal-only surfaces, the `## Wrap-up` lifecycle, and handoffs (team binding
via `/speckit.team`) stay in the command template — they are command lifecycle, not anchor
operations.
