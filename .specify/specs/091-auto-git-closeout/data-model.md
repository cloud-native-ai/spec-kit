# Data Model — Feature 091 Automatic git Close-out

**Feature**: 091-auto-git-closeout | **Date**: 2026-11-09 | **Plan**: [plan.md](plan.md)

This feature stores almost nothing: a declaration lives in a file the project already owns, a receipt is written once
per run, and everything else is a derived sequence that exists only for the duration of one invocation. Six entities,
each naming its **carrier** (the file that holds it) and the validation rules a guard or the executor asserts. Clause
identifiers refer to the four pages under `contracts/`.

## Entities

### E-1 — Close-out declaration（收口声明）

The project-level policy, and the only authorization source for a push.

| Field | Meaning | Carrier |
|-------|---------|---------|
| `closeout` | the strategy value — closed set `commit+merge+push` / `commit+merge` / `commit-only` / `ask`, default `ask` | `.specify/workflow/git.md` managed block, line `- **Closeout**:` |
| `closeout_remotes` | the pushable remotes, comma-separated; empty or absent means "no pushable remote" | same block, line `- **Closeout remotes**:` |
| `model` | the existing `Workflow model` value — **read, never written by this feature** | same block, line `- **Workflow model**:` |
| `remote_roles` | the existing role markings (e.g. the read-only upstream) — **read, never written** | same block, `⚠ Remote roles` line |

Rules: V-1 (both new rows readable), V-2 (value in the closed set), V-3 (default `ask` when the row is absent), V-4 (no
second branch table added by this feature). Relationship: E-1 1—1 E-2 (one declaration yields one sequence).

### E-2 — Workflow model instance（workflow 模型实例）

The declared model, projected to the branch names the sequence will touch.

| Field | Meaning | Carrier |
|-------|---------|---------|
| `kind` | one of `single-branch` / `dual-branch` / `temp-branch` / `three-tier` | E-1 `model` value, projected |
| `trunk` | the branch a temp-branch or single-branch model merges into and pushes | block's branch convention line, projected |
| `daily` / `archive` | the two long-lived branches of a dual-branch model | block, projected |
| `dev` / `pre` / `main` (+ trackings) | the three branches of the three-tier model | block table rows, projected |
| `feature_branch_name` | `NNN-<slug>` for a temp-branch model | block convention + the caller's requirement key |

Rules: V-5 (the model is read, never guessed — the `None yet.` placeholder is a hard stop), V-6 (a projection names only
the branches its own model needs). Relationship: E-2 is derived 1—1 from E-1 and is never stored.

### E-3 — Close-out sequence（收口序列）

The ordered action list the executor derives. Not stored — it is the projection of E-1 × E-2 × the run's intent.

| Field | Meaning |
|-------|---------|
| `stage` | `commit-artifacts` (already done by the previous step) → `commit-records` → `merge` → `push` → `delete-branch` |
| `model_steps` | the model-specific intermediary steps (dual: sync/merge per declared relation; temp: cut short-lived branch, merge back, delete local branch; three-tier: DEV→PRE then PRE→MAIN) |
| `push_targets` | `closeout_remotes` **minus** every remote marked read-only |
| `authorization` | `execute` for `commit+merge+push`; `local-only` for `commit+merge` / `commit-only`; `present-and-report` for `ask` / absent |
| `failure_stage` | set when the line stops; `null` on success |

Rules: V-7 (the sequence is derived, never hardcoded per project), V-8 (a step in the destructive or governance-kept list
stops for confirmation even under `commit+merge+push`), V-9 (`delete-branch` only when the merge actually landed), V-10
(no `--force`; at most `--force-with-lease` behind its confirmation).

### E-4 — Close-out receipt（收口回执）

The one durable artifact a close-out writes, and the answer to FR-028. One file per run, timestamp-named, never rewritten.

| Field | Meaning | Constraint |
|-------|---------|------------|
| `kind` | the literal receipt kind, distinguishing it from the retention engine's `speckit.record-retention.receipt` | must not reuse the retention key |
| `run_id` | the run the receipt belongs to | one receipt per run |
| `commit` | the hash of the records commit this receipt covers | full 40-hex, as printed by `git rev-parse HEAD` |
| `covered[]` | one row per record file the commit carried: `path`, `action` (`included` / `kept` / `handed-to-consumption`) | paths repository-relative; a path MUST NOT appear twice |
| `reader_pointer` | the consuming engine's read rule, **by path/anchor**, never copied text | e.g. the retention engine's own action names |
| `created_at` | ISO-8601 UTC | sort order = creation order |

Rules: V-11 (written once — a second close-out of the same run creates a new file, never an edit), V-12 (a record file
appears in at most one receipt's `covered[]` for a given commit), V-13 (the receipt itself is committed in the same
commit it names, so the commit is self-describing). Carrier: a timestamp-named file under the close-out receipt
directory — the directory path is a `tasks` decision against the sanctioned record root, and the layout rule (one file
per run) is the binding constraint, not the literal name.

### E-5 — Close-out report（收口报告）

The run-visible outcome. Not a file: a section of the run's report whose required fields are specified.

| Field | Meaning |
|-------|---------|
| `receipt` | path of E-4, or `none` with the reason (read-only run; no records) |
| `records_commit` | the hash, or `not-created` with the reason |
| `merge` | `already-current` / `merged <sha>` / `skipped (<why>)` |
| `push[]` | one row per target: `remote`, `branch`, `result` (`pushed` / `absent` / `rejected` / `skipped (<why>)`) |
| `deviation[]` | other lines' dirty files, by path, reported and never swept in |
| `failure` | `null`, or `{stage, command}` — the exact command handed back, verbatim |

Rules: V-14 (every field present; an unrun step says so instead of being omitted — FR-007 / SC-007). Relationship:
E-5 1—1 E-4 or 1—0 (a read-only run has a report and no receipt).

### E-6 — Fixture repo + fake remote（夹具仓库与假远端）

The verification carrier.

| Field | Meaning |
|-------|---------|
| `model` | which of the four the fixture declares |
| `bare_remote` | a local bare repository acting as `origin`-equivalent, on the filesystem, no network |
| `seed` | the initial branch set + one artifact commit, so the close-out has something to close |
| `assertions` | end-state checks: `branch --list`, `rev-parse <branch>`, `ls-remote <remote>`, commit authorship |

Rules: created under `tempfile.TemporaryDirectory()` (A10), torn down by the fixture; two independent writers never
share a path because each test gets its own root.

## Validation rules

| ID | Rule | Enforced by |
|----|------|-------------|
| V-1 | Both declaration rows are readable from the managed block | `closeout-declaration.contract.md` C-1; `test_git_closeout_contract.py` |
| V-2 | The strategy value is inside the four-value closed set | C-1; SC-002's mutation (illegal value ⇒ red) |
| V-3 | A missing `Closeout` row behaves as `ask` | C-1, C-5 |
| V-4 | The block gains no second branch table | C-2; SC-004 negative structural assertion |
| V-5 | The model is read, never guessed; the `None yet.` placeholder is a hard stop | `closeout-executor.contract.md` C-2 |
| V-6 | A model projection names only its own branches | C-2, C-3 |
| V-7 | The sequence is derived from the declaration, not hardcoded per project | C-3; SC-001's four fixtures |
| V-8 | A confirmation-gate action stops even under `commit+merge+push` | C-5; `closeout-lifecycle.contract.md` C-6 |
| V-9 | The short-lived branch is deleted only after a landed merge | `closeout-executor.contract.md` C-4; SC-001 fixture 3 |
| V-10 | No `--force`; `--force-with-lease` only behind its confirmation | C-4; SC-003's rejection fixture |
| V-11 | The receipt is write-once | `closeout-lifecycle.contract.md` C-3 |
| V-12 | A record path appears in at most one receipt for a commit | C-3 |
| V-13 | The receipt is committed in the commit it names | C-3 |
| V-14 | Every report field is present; an unrun step is stated, not omitted | `closeout-lifecycle.contract.md` C-4; SC-007 |

## State transitions

One run, one close-out, four terminal states:

```text
run ends (artifacts committed)
   ├─ read-only, no artifacts, no records ──► skipped-and-stated        (no receipt, no empty commit)
   ├─ artifacts, no records ─────────────────► merge+push executed      (report says "no records commit")
   ├─ records produced ──────────────────────► receipt written ──► commit ──► merge ──► push ──► done
   └─ any stage fails ───────────────────────► stopped-at-first-failure
                                                 (report: stage + exact command; NO retry, NO force)
```

`ask` / absent strategy is not a fifth state: the sequence is derived and **presented**, and the run ends
`presented-and-waited` without executing — a report, never a block (clarify C-3 / A7).

## What this model deliberately does not contain

No branch registry, no aggregate receipt index, no retry state, no scheduler state, no second store. E-1 and E-2 are
projections of the file the skill already owns; E-3 is per-invocation; E-4 is one file per run; E-5 is report text;
E-6 exists only inside a test's temp root.
