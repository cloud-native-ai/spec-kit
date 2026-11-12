---
name: manage-goal
description: Author and manage action-level Goal definitions in the Goal archive — the executable core of `/speckit.goal`. Runs the four modes (create / view / modify / status) through the definition engine: the three-element interview for a new Goal (the practical guidance it gives, at least one verifiable completion condition, identity), the read/write engine grouping with exit-code verdicts, and the single destructive write (emptying the condition set) behind explicit approval. Step-shaped guidance is accepted by design. Every write goes through the engine — the Goal archive is engine-write-only, and this skill never touches the anchor archive or team definitions. Use this when the user mentions ["goal", "行动级目标", "goal definition", "practical guidance", "行动指导", "创建目标", "success condition", "完成条件", "completion condition", "goal view", "goal modify", "goal status", "goal achieved", "goal abandoned", "reopen", "goal-slug", "goal archive"].
classification: internal
skill_id: "<SKILL:.specify/skills/internal/manage-goal/SKILL.md>"
---

# manage-goal

> **Concurrency obligation（执行义务，按指针抵达）**: this skill is an execution body — before the first real action, run the one-shot assessment (class → carrier → partition), default to concurrent execution for two or more independent units, and when serial name a reason code and record the `requested` / `effective` / `effective_reason` reading. Authored text: `shared/definitions/subagent-definitions.md` § The Concurrency Obligation; class table: `shared/declarations/facts/concurrency-class.yaml`; reason codes: `shared/declarations/facts/serial-reason.yaml`; reading fields: `shared/declarations/facts/effective-concurrency.yaml`. This body restates none of their rules.

## Goal

Own and execute the operations behind `/speckit.goal` — the **sole authoring entry** for
action-level Goal definitions in the Goal archive. A **Goal** is an authored fact source
(never a derived artifact): **action-level, short-horizon, executable practical guidance** —
the concrete next moves a run follows, not a project-level end state. This skill owns only
the *operations* (mode semantics, the `create` interview, execution ordering, engine
invocation). The Goal *concept* — composition, identity, the store, the sections, lifecycle
by reference, and its neighbours — is defined once in
`.specify/shared/definitions/goal-definitions.md`. **Link to that document; never restate
it.** Deterministic rules (identity grammar, rendering, lifecycle transitions, change
history) live in `scripts/python/goal-utils.py`. Call the engine; do not re-derive its
judgments in prose.

**Non-negotiable boundary**: no skill, script, or other command may write into the Goal
archive **directly** — the definition engine (`goal-utils.py`) is its sole writing path,
whether driven by `/speckit.goal` or carried as delegated logic behind it.

Canonical extraction source: `templates/commands/goal.md` § Outline. The command template
keeps entry, user-input handling, glossary pre-step, the named refusal of Anchor-only
modes, and the wrap-up lifecycle only.

## Input Contract

- **Intent**: one of `create | view | modify | status`, optionally with a `goal-slug`.
  Mode is inferred from the request and **disclosed with every run**.
- **Ambiguous input resolves to `view`** — which is read-only.
- **Reversibility**: execution proceeds directly for reversible actions
  (可逆动作自动执行，判据：`.specify/shared/guidelines/confirmation-gates.md`) — the single
  destructive write, named in step 4, is the exception.

**The mode table lives here and nowhere else** — this is its single home; the command
template cites it by path and enumerates no second copy.

| Mode | Purpose | Writes |
|------|---------|--------|
| `create` | archive a new action-level Goal | `.specify/goals/<goal-slug>/goal.md` |
| `view` | list the Goal archive, or show one Goal | nothing |
| `modify` | change the guidance narrative or the completion conditions | the same definition file |
| `status` | report lifecycle state, or transition it | the same definition file (`--set` only) |

The store, identity grammar and section layout are owned by
`.specify/shared/definitions/goal-definitions.md`; the lifecycle value set and its
transition discipline are owned by `.specify/shared/definitions/anchor-definitions.md` and
cited from there — this table cites the landing point, never the value domain.

**Action-level only — the seven Anchor modes have no form here.** `targets`, `migrate`,
`migrate-archive` and `coordinate` belong to `/speckit.anchor`; this skill implements none
of them, exposes no Targets surface, performs no migration, and never writes
`.specify/anchoring/**` or any `team.md`. A caller who names one of those modes is refused
by the command (named refusal, exit 2, zero writes); inside this skill the same request is
answered by pointing at `/speckit.anchor` — never by stretching a Goal mode.

## Workflow

### 1. Resolve context

Run `.specify/scripts/bash/check-prerequisites.sh --json --paths-only` for `REPO_ROOT`.
The Goal archive is `REPO_ROOT/.specify/goals/` (store and identity:
`.specify/shared/definitions/goal-definitions.md`).

### 2. Determine the mode

From the request; state it back to the user.

### 3. Preview → execute

Before any write, show: the mode, the target path, and the exact content to be written
(or the diff for a modify) — then write directly (preview is **disclosure, not a blocking
gate**；事后修改经 `/speckit.goal` modify). `view` and a `status` report stay read-only.

### 4. Execute via the engine — never hand-write a definition file

The block below fixes only the **read/write grouping**; every action's full flag set and
defaults are owned by `python3 scripts/python/goal-utils.py --help` and are not restated
here.

```bash
# 读组 — zero writes
python3 scripts/python/goal-utils.py goal-list
python3 scripts/python/goal-utils.py goal-view <goal-slug>
python3 scripts/python/goal-utils.py goal-status <goal-slug>          # report only
python3 scripts/python/goal-utils.py validate <goal-slug> --scope goals
python3 scripts/python/goal-utils.py command-mode --command goal --mode <mode>

# 写组 — mutates the Goal archive through the engine
python3 scripts/python/goal-utils.py goal-create <goal-slug> --guidance "<practical action>" --done "<condition>"
python3 scripts/python/goal-utils.py goal-modify <goal-slug> --guidance "<revised guidance>"
python3 scripts/python/goal-utils.py goal-modify <goal-slug> --done "<replacement condition>"
python3 scripts/python/goal-utils.py goal-status <goal-slug> --set achieved
```

Exit codes: `0` ok · `2` input error (rejection) · `3` not found · `4` validation failed ·
`5` blocked — the action table is the engine's
(`python3 scripts/python/goal-utils.py --help`). A non-zero exit is a **verdict**: report
it, never argue around it.

**破坏性写入**（桶归属见 `.specify/shared/guidelines/confirmation-gates.md` §破坏性动作清单）：`goal-modify <goal-slug> --clear-done` 以空值覆盖既有完成条件集。引擎对缺参的 `goal-modify` 调用一律 exit 2——它 MUST NOT 被读成查看入口，也不会静默清空；传 `--clear-done` 之前 MUST 先取得用户明示批准（`--clear-done` 与 `--done` 同现亦 exit 2）。其余写入均为可逆动作：直接执行，按执行报告呈现，事后经 `/speckit.goal` modify 修改。

### 5. Interview for `create` — exactly three things, nothing else

Ask them per the interview pattern (`.specify/shared/patterns/interview-pattern.md`):
**open** questions carrying their context, no option menus and no recommended answers
(the guidance is the user's to state, not yours to propose), facts looked up rather than
asked, each answer written through before the next round.

1. **the guidance**: the practical action this Goal steers. **Step-shaped text is
   accepted** — a numbered sequence is a legitimate Goal shape here (concept:
   `.specify/shared/definitions/goal-definitions.md`, link, never restate). There is no
   `outcome, not steps` check on a Goal: never press the user to restate guidance as an
   end state, and never import the Anchor shape rules.
2. **completion conditions**: **at least one** verifiable condition — the engine rejects a
   `goal-create` without one (`--done` is repeatable; `goal-create` requires ≥1). Verifiable
   ≠ machine-checkable: a condition whose measurement route is **manual/human review** (a
   named reviewer judging the outcome) is an equally legitimate form. Say so out loud when
   asking, so the user does not withhold a real condition because no program can measure
   it.
3. **the identity**: a `goal-slug` that is also the directory name. Reuse `goal-slug`
   semantics; do not invent a second identifier.

`goal-create` 另接受一个可选附注——`--title`（可读标题，身份仍是 slug）：仅在用户自行陈述时携带，MUST NOT 为此发问，上面的收集集不因它扩张。

### 6. `status <goal-slug>`

Without `--set` this is a **read**: report the current lifecycle state and stop. With
`--set` it transitions within the shared value set; a terminal Goal is **retained** in the
archive, and reopening one (`--set active`) is allowed **only** for a human-owned Goal —
the engine is the executable subject of that rule and rejects anything else. Every
transition appends a history line; nothing is deleted, ever.

### 7. `modify <goal-slug>`

Edit the guidance narrative or replace the completion conditions — the prior values stay
traceable in the definition's `## History`. A replacement condition set goes through
`--done` (repeatable); emptying the set requires `--clear-done` and explicit user approval
(step 4). Never hand-edit the file, and never touch the lifecycle state here — that is
`status`.

## Boundaries

- **Engine-write-only (non-negotiable)**: the definition is **authored**. No derived flow
  may write `goal.md`; no skill, script, or other command may write into the Goal archive
  directly — `goal-utils.py` is its sole writing path.
- **Never the Anchor archive and never teams**: this skill writes
  `.specify/goals/<goal-slug>/goal.md` and nothing else. Team binding and slice
  coordination are always carried by Anchor + Team (`/speckit.anchor`, `/speckit.team`).
- **No Anchor pointer**: a Goal's schema declares no `anchor_ref` (or any Anchor-named
  key) and the engine rejects undeclared keys with exit 2. The only permitted cross
  reference is the source spec directory in the binding record's `origin`.
- **No targets, no migration, no coordinate**: those are Anchor-side operations and are not
  exposed here.
- **Parallel to SDD, not above it**: spec/plan/tasks carry deliverable design, a Goal
  carries action-level guidance; neither parses the other's identity, and a Goal does not
  enter the control hierarchy, is never bound by a team, and never substitutes for spec
  artifacts.
- **No GD-2 check**: guidance MAY be step-shaped; completion conditions are verifiable and
  are the only shape-checked part (at least one, non-empty).
- Terminal Goals (`achieved` / `abandoned`) stay archived. Deletion is not a lifecycle
  transition.

## Command-lifecycle surfaces (kept in `/speckit.goal`)

Entry argument handling (`.specify/shared/workflow/user-input-protocol.md`), the glossary
pre-step (`.specify/glossary.md`, protocol `.specify/shared/workflow/glossary.md`), the
named refusal of Anchor-only modes, the `## Wrap-up` lifecycle, and handoffs (Anchor + Team
for binding and slices) stay in the command template — they are command lifecycle, not
Goal operations.

## Wrap-up

<!-- AUTO-GENERATED by probe-utils.py --action compile-embeds — truth source: .specify/shared/definitions/probe-definitions.md (## Handler / ## HandlerBinding) — fingerprint: 4682b9e38032 — do not edit; edit the registry, then recompile -->

**Runtime-mode gate.** If `${SKILL_WORKDIR}/.specify/` does not exist, this skill is running in standalone mode (a non–Spec Kit deployment, e.g. a global agent skills directory) — skip this entire Wrap-up step: no engine call, no feedback entry.

1. Run Determination — `python3 .specify/scripts/python/run-determination.py --action determine --unit-id "skill:manage-goal" --unit-type skill --run-id <RUN_ID> --complexity <COMPLEXITY>`；source args when available: `--session-file <SESSION_FILE> --session-rows <SESSION_ROWS> --tool <TOOL> --proxy-paths <PROXY_PATHS> --token-note <TOKEN_NOTE> --elapsed-ms <ELAPSED_MS> --elapsed-note <ELAPSED_NOTE> --names-current <NAMES_CURRENT> --names-baseline <NAMES_BASELINE> --declared-check <DECLARED_CHECK> --green-check <GREEN_CHECK> --red-first-refs <RED_FIRST_REFS> --collected <COLLECTED> --prev-user-turn-class <PREV_USER_TURN_CLASS> --unresolved-red <UNRESOLVED_RED> --red-source <RED_SOURCE>`
   尖括号为本轮运行时值——代入后照抄执行(占位 = 参数名去 --、转下划线、全大写;渲染集 = 引擎 manifest required + source,身份对已带实值)
2. Exec Quant — `python3 .specify/scripts/python/exec-quant.py --action collect --unit-id "skill:manage-goal" --unit-type skill`；source args when available: `--run-id <RUN_ID>`
3. Feedback Record — `python3 .specify/scripts/python/feedback-utils.py --action record --unit-id "skill:manage-goal" --unit-type skill --run-id <RUN_ID> --review <REVIEW> --points <POINTS>`
4. Threshold Notice — `.specify/shared/workflow/feedback-step.md` § "Threshold prompt protocol (canonical semantics for step 6)"
5. Token Reflection — `.specify/shared/workflow/feedback-step.md` § "Reflection procedure (the embedded step points here)"
6. Closeout — `.specify/shared/workflow/artifact-commit-step.md` § "The `## Close-out` step"
