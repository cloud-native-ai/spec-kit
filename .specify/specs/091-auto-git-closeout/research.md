# Research — Feature 091 Automatic git Close-out

**Feature**: 091-auto-git-closeout | **Date**: 2026-11-09 | **Plan**: [plan.md](plan.md)

This record answers one question: *what does the tree contain today, and does it support the settled requirements?*
Every reading below was taken on 2026-11-09 against this repository. Counts and paths are the measurements; the design
consequences are stated once, in `plan.md` § Phase 0 and in the contract pages.

## R1 — The insertion point exists and it is the right owner

`shared/workflow/artifact-commit-step.md` (77 lines) exists, is embedded by every artifact-producing command, and its
§ Boundaries carries this sentence verbatim:

```text
- **Not a substitute for pushing.** This step commits locally. Pushing is a
  shared-state action governed by the framework-level git workflow state file
  (`.specify/workflow/git.md`) and requires its own authorization.
```

Consequence: FR-008's revision rewrites this sentence inside its existing owner. The file's § The step already orders
the lifecycle `Feedback → Documentation → (this step before them)`, so the close-out step is inserted **after** the two
record-producing steps, which is exactly the order FR-005 requires.

## R2 — `closeout` does not exist yet (negative fact, measured)

`grep -n "closeout\|close-out\|收口"` over `skills/external/git-utils/SKILL.md`, `skills/external/git-utils/assets/git-workflow-block.md`,
and `.specify/workflow/git.md` returns exactly **one** hit: the block asset's prose "close-out discipline followed by both
human developers and the framework's unattended mechanisms". No operation, no reference, no declaration row exists.
Consequence: FR-009 creates a name; nothing is being wrapped or renamed.

## R3 — The Phase 0 dispatch table needs no change

`SKILL.md` § Phase 0 (`### Phase 0: 调谐作用域判定`) ends with a three-row table keyed on two axes:

| 块已填写 | 有操作参数 | 进入作用域 |
|----------|------------|------------|
| 否 | — | Bootstrap 调谐（Setup） |
| 是 | 否 | 全维度体检（Maintain） |
| 是 | 是 | 定向收敛（Execute） |

`closeout` falls in row 3 and is therefore a peer of operations A–G. Confirm of clarify C-6; no fourth row is added.

## R4 — The command surface needs its own reference, not a bigger `execute-commands.md`

Measured shape of `skills/external/git-utils/references/execute-commands.md` (180 lines): `## 前置校验`, `## 操作 A`
(+A1–A3), `## 操作 B`, `## 操作 C`, `## 操作 D`, `## 操作 F` (+F1–F3), `## 操作 G`. Operations A–C are explicitly
three-tier-only; D–G are model-agnostic. Its first command block begins `git fetch origin`, and `origin` is this repo's
**read-only upstream** (`git remote -v`: `origin  git@github.com:github/spec-kit.git`, while the fork mirrors are
`github` / `gitlab` / `gitee`).

Consequence (design decision R4): the four close-out sequences do **not** belong to a page about three-tier operations.
A new sibling reference `references/closeout-commands.md` holds them and uses the placeholder `<remote>` (substituted
from the declaration) so no remote name is ever hardcoded into the close-out path. `execute-commands.md` gains one
pointer line only.

## R5 — The probe registry admits one Handler with no new Object

`shared/definitions/probe-definitions.md` (325 lines) has `## Handler` and `## HandlerBinding`. The `wrap-up`
lifecycle point is already bound to five handlers with `order` 10 / 15 / 20 / 30 / 40 / 50
(`h-run-determination`, `h-exec-quant`, `h-feedback-record`, `h-threshold-notice`, `h-token-reflection`,
`h-docs-sync-eval`). Handler rows are a six-field closed set (`handler_id`, `kind`, `action`, `mode`, `order`,
`behavior_owner`), and `kind=agent` takes the `##`-level heading of the `behavior_owner` file verbatim.

Consequence: one new `kind=agent` handler, `behavior_owner = shared/workflow/artifact-commit-step.md`, at the next free
order in the `wrap-up` sequence (after the record steps, since the rule is "close-out runs after records"). The rendered
faces are produced by `probe-utils.py --action compile-embeds`; FR-021 forbids hand-writing them.

## R6 — The destructive-action governance is untouched by design

`.specify/shared/guidelines/confirmation-gates.md` owns two closed lists. The destructive list's third bullet is
*"远程推送(push / force-push / 远程分支操作)与写入外部权威源"*; the governance-kept list holds the git-workflow remote
operation gate (`skills/external/git-utils`, "远程推送属破坏性桶"). Current scan: `blocking confirmation gates: 27`
(destructive 20 / governance_kept 7), `violations: 0`.

Consequence: `T-002` refuses to widen either list; the standing authorization is a *value in the state file*, and the
executor's own resolution reads it. SC-004's baseline is the 27 reading taken today.

## R7 — An existing test pins the gate total by equality (`F-2`)

`tests/contract/test_wrap_up_wording_gate_safe.py` lines 74–77:

```python
# stale-pin update (067 T025, 2026-10-22): owner fact = live scan total, 23 -> 27
assert int(m_total.group(1)) == 27, (
    f"gate budget moved: {m_total.group(1)} != 27 — the compiled sections changed "
```

Consequence: this feature's SC-004 / SC-008 guards MUST compare **by name over the set of gates** (baseline captured in
the same run) and MUST NOT introduce a second equality constant. If a later feature moves the total, that pin's owner
re-rules first — recorded as a task constraint, not edited from a plan stage.

## R8 — "Receipt" already means something else in this tree; the new receipt must borrow its *shape*, not its key

`scripts/python/record-retention.py` implements *"records consume -> receipt -> retire"*: one receipt per consumed raw
record, at `.specify/memory/retention/receipts/<stamp>-<entry_hash(store, entry_id)>.json`, keyed `(store, entry_id)`,
with a 30-day grace window before a record file is retired (`RETENTION_REL = .specify/memory/retention`).

The close-out receipt's subject is different: *which record files this run's commit covers, and under which commit*.
Reusing the retention key would collide with the retirement lane's `(store, entry_id)` identity and invite double-writes.

Consequence (design decision R8): a separate directory, `one file per run`, timestamp-named, carrying the covered paths,
each path's action (`included` / `kept` / `handed-to-consumption`), the covering commit hash, and a **pointer** to the
consuming engine's read rule (never a copy of it). Store layout is `data-model.md` § E-4.

## R9 — The git skill's reference examples contradict this repo's remote roles (`F-1`)

`execute-commands.md` `## 前置校验` starts with `git fetch origin`; the operation-A push strategy text pushes `origin`.
In this repo `origin` is the **read-only upstream**, and the framework instructs pushing the fork mirrors instead.
This is pre-existing and out of a plan stage's territory to rewrite wholesale.

Consequence: the close-out path introduces **no remote literal** and resolves every push target from the declaration
plus the role check (FR-002 / FR-013). The pre-existing example lines are reported as an upstream deviation in the
close-out report when they are touched by a run, and are otherwise left alone. Disposition recorded in
`feature-ref.md` § Disclosed rulings.

## R10 — The instructions surface already names close-out; only a pointer is admissible

Measured: the `## Git Workflow` section of `templates/instructions-template.md` and `.specify/instructions.md` are
**byte-identical** (`diff` of the extracted sections is empty), and both already say *"unattended mechanisms (SDD driver,
house-keeping, feedback digest, close-out) commit, merge and push on a cadence"*.

Consequence: FR-022's "at most one pointer line" is close to unnecessary. The plan's default is **no edit** to the
template; the delivery row stays contingent (row 8 of `feature-ref.md`) and implement adds a pointer only if it finds
that a reader following the section cannot reach the step. This is the smallest change that satisfies the FR.

## R11 — Deployment surface: the block's two rows reach new projects through the asset, not through this repo's file

`assets/git-workflow-block.md` is the whole-file template (it carries `<MODEL>`, `<MODEL_SPECIFIC_LINES>`, `<DATE>` and
the marker comments), while `.specify/workflow/git.md` is this project's filled instance. Measured: the asset's prose
already says the block holds the "close-out discipline", but it carries no fillable close-out row.

Consequence (FR-004): both rows land in the asset as placeholders (so a new project's Bootstrap offers them) **and** in
this repo's instance with this project's values (`Closeout: commit+merge+push`, `Closeout remotes: github, gitlab, gitee`).
The asset MUST keep the markers byte-exact — an existing contract test checks them
(`test_git_workflow_instructions_block.py::test_block_asset_is_a_full_file_template`).

## R12 — Verification surface: what a guard can read without running git

Three quarters of the feature is text; the fourth is behavior. The guard module therefore splits into two shapes:

- **Structural reads** (fast, no subprocess): declaration rows and value domain, the four model sequences present in
  the new reference, the commit-step owner's step + three forks + revised push boundary, the pointer from each
  unattended mechanism, the absence of a second branch table, and the SC-004/SC-008 closed-set claims.
- **Fixture executions** (subprocess `git` in a temp root): one repo + one local bare remote per model, asserting end
  state (`branch --list`, `rev-parse <branch>`, `ls-remote`), plus the two failure fixtures (push rejected, merge
  conflict) and the two wrap-up forks (read-only run, artifacts-without-records).

Measured baseline that makes "no NEW failure" meaningful: the three contract modules this plan's clauses touch report
`835 passed` on an untouched tree (`test-evidence/plan-gates.txt` § 4).
