# Specification-Driven Development (SDD) Process Review Report: 074a-authorized-routing

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 074a |
| Requirement Key | `074a-authorized-routing` |
| Requirement Name | 授权席位的有界嵌套 SDD 调用与确定性分流 (slice 074a of Feature 074) |
| Related Feature | 074 Goal/Team/Agent 与 SDD 开发流程统一 (slice reuses the Feature 074 row; status stays `Planned`) |
| Repository | spec-kit |
| Repository URL | `(no HTTPS web remote)` — remotes are SSH-only: `git@gitee.com:cloud-native-ai/spec-kit.git`, `git@github.com:cloud-native-ai/spec-kit.git`, `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git`. `origin` is `git@github.com:github/spec-kit.git` — the **upstream**, which does not contain these commits |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains HEAD` is empty (unpushed). Cite absolute paths plus `git show <sha>:<path>` for recovery; no URL citation in this report resolves |
| Branch | `074-goal-team-sdd-unification` |
| Commit SHA | `0024585c4a58af455a19aec218396e8098d05748` (short: `0024585c4`) |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-10-29 |
| Reviewer (Agent) | SDD Executor (fresh dispatch, stage `review`); the record header names `Qiming Liu (John)` as the git author |
| Environment | Linux 5.10.134-15.2.al8.x86_64; Python 3.11.11; pytest 8.4.2; no network, no container runtime; `delta` not exercised (non-TTY agent run ⇒ `renderer: text`) |
| spec-kit Source Snapshot | this repository at `0024585c4` (`pyproject.toml` version `0.0.22`) |

### Same-author condition (objective-analysis gate)

The gate in `.specify/shared/workflow/objective-analysis-gate.md` fires when the artifacts under analysis were produced by the agent now analyzing them **in the current session**. It does **not** fire here: this review is a fresh dispatch that authored none of the artifacts, which were produced by earlier dispatches across 31 slice commits. Independent authorship supplies the fresh context the gate exists to obtain, so detection ran in this context rather than being delegated, and the propagation-surface cap (P1) was **not** applied as a ceiling — each finding's severity is derived from its propagation surface as stated in the row.

The P0-validation pass was unavailable for a structural reason: this environment exposes no subagent dispatch capability. The skill's documented fallback applies, and every P0 candidate row would have carried `(validated: direct re-read, subagent unavailable)`. There are no P0 rows (see §2), so nothing depends on the weaker path.

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 513 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074a-authorized-routing/requirements.md` | 20 FR / 6 SC / 10 STR, parent mapping, D-1…D-3 attribution rulings, three dated clarification sessions |
| plan.md | 359 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074a-authorized-routing/plan.md` | Technical approach, 18-row Constitution Check, mirror obligations, plan-owned scope, one declared Plan Revision |
| tasks.md | 271 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074a-authorized-routing/tasks.md` | 32 rows all `[X]`; 9 gates; measured premises; `[green:]` clause claims |
| verification.md | 248 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074a-authorized-routing/verification.md` | Baseline/implement blocks, six hash-bound evidence rows, gate re-runs, DoD close |
| research.md | 218 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074a-authorized-routing/research.md` | RA1–RA9 rulings with measured anchors and rejected alternatives |
| data-model.md | 258 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074a-authorized-routing/data-model.md` | E1–E9 entities, V-1…V-29 validation rules, 3 state machines |
| quickstart.md | 195 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074a-authorized-routing/quickstart.md` | S1–S7 walkthrough scenarios with per-example disclaimers |
| feature-ref.md | 130 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074a-authorized-routing/feature-ref.md` | Binding, 15-row delivery surface, FR/SC maps, 7 disclosed rulings |
| contracts/hierarchy-and-authorization.md | 153 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074a-authorized-routing/contracts/hierarchy-and-authorization.md` | C-1…C-16 (hierarchy, seats, AND resolution, narrowed predicate) |
| contracts/routing-decision.md | 151 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074a-authorized-routing/contracts/routing-decision.md` | C-17…C-30 (owner document, five inputs, verdict mechanics, exit alphabet, golden table) |
| contracts/nested-invocation.md | 110 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074a-authorized-routing/contracts/nested-invocation.md` | C-31…C-43 (entry form, handoff, line registration, failure handoff, consumer duty) |
| contracts/bootstrap-and-maintenance.md | 52 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074a-authorized-routing/contracts/bootstrap-and-maintenance.md` | C-44…C-47 (invocation kinds, bootstrap path, same predicate, no new machinery) |

Counts above were re-derived in this run, not copied: `FR=20 / SC=6 / STR=10`, `clauses=47`
(16 + 14 + 13 + 4), `tasks [X]=32 / open=0`, and 47 distinct `[green:]` clause targets with none
unclaimed and none double-claimed (the 48th `[green:]` match in `tasks.md` is the legend literal
`<contract>#<clause>`, not a claim).

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | Slice registered under Feature 074 | `939766891` "docs(074-goal-team-sdd-unification): register 074a slice under feature 074" | None — no new Feature row was created, per `requirements.md` § Related Feature |
| 2 | requirements + checklist | `312b37017`, then `c5e4c662a` "qualify parent references for requirements gate" | Minor: the first commit did not satisfy the parent-reference gate and needed a follow-up |
| 3 | clarify | `78e26f0ca` | None |
| 4 | plan + design artifacts | `907d21fbe` (plan, data-model, contracts, quickstart, research, feature-ref) | None |
| 5 | tasks + clause baseline freeze | `a98155404` | None |
| 6 | implementation-readiness checklist | `b8363f89f` | None |
| 7 | analyze-fix round 1 | `8f991f375` "resolve analyze HIGH findings and align contracts" — `plan.md` § Plan Revision records 4 decisions | None — plan re-review was authorized and declared |
| 8 | analyze residuals + **parent-spec edit** | `71954e31a` "reconcile analyze residuals and parent cap" — modifies `.specify/specs/074-goal-team-sdd-unification/requirements.md` (+8/−4) and adopts it as `baseline_commit` | **Yes** — `tasks.md` § Path Conventions marks `.specify/specs/074-goal-team-sdd-unification/**` read-only. See F1 |
| 9 | implement-start baselines (T001–T003) | `d5129efcd`, `08837d1e9` (full baseline run kept in version control) | None |
| 10 | Foundational + US1 + US2 + US3, red-first per row | `febe90509` … `7305ea7b8` — 14 commits, each naming its task ids, each carrying a `notes/red-tNNN.txt` red record | None — story/task-grouped commit discipline held |
| 11 | Polish: mirrors, single-owner audit, structural face, targeted regression | `ff1ef3527`, `a162485f6`, `4f3095225`, `42b105d75` | None — `audit-plan-changes.py` was **not** used; the plan-constraint was measured with an ad-hoc `git diff --stat` over six paths (F1) |
| 12 | quickstart walkthrough, SC evidence, gate re-run | `f1d65142a`, `8e1a41536`, `0024585c4` | Minor: `verification.md` still records `post_change_commit=f1d65142a` although two later commits carry the log's own SC and gate sections (F5) |
| 13 | Review (this run) | `code-review.md` + `review.md` in the slice directory; base `371869045..head 0024585c4`, triage `run` | None |

The commit history is story/task-grouped throughout (21 of the 31 commits that touch the slice
directory name their task ids; the rest are stage-level), so no working-tree reconstruction fallback
was needed and no timeline claim above is inferred from artifact state.

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 3 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 3 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 0 |
| Automation / Scripts | 2 |
| Workflow | 3 |
| Documentation | 1 |

No P0 findings were raised: every candidate either named a repair already inside the declared scope
(the parent-spec edit is disclosed in the parent file's own dated clarification, so nothing was
concealed), or resolved to a lower tier once its propagation surface was checked. There is no fourth
severity tier in the vocabulary this report uses (`templates/commands/review.md` § Delegation cites
the process skill's `P0`/`P1`/`P2` family and defines no levels of its own), so a caller-side "P3"
request resolves to 0 by construction — every quality-of-life item is a P2 here.

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `371869045d7c86cace67bb49b40b5aa2fd18ceb0` | the resolved diff base |
| Head commit | `0024585c4a58af455a19aec218396e8098d05748` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the resolution tier the code segment reported (`base` subcommand) |
| Renderer mode | `renderer: text` | the code record's header marker |
| Changed / judged / skipped / gap files | 69 / 9 / 60 / 0 | copied field by field from the coverage receipt block (`changed_files` / `judged_files` / `skipped_files` / `gap_files`) |
| Segment verdict | `pass` | one of the four closed values the `code-review` skill owns |
| Gate verdict | `allow` (`blocking_entries=0`; 1 `important` item answered in the record, 2 `suggestion`, 1 `question`, 2 `praise`) | `report --summary --file` exit 0 |
| Reason, when one applies | `none` | mandatory only for `not-applicable` / `not-evaluated` |
| Uncommitted scope | 49 uncommitted paths were excluded from the reviewed object and are concluded over nowhere; the same sentence is written in the record (`code-review.md`, "未提交范围（未评审）" line) | disclosed, never concluded over |
| Record | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074a-authorized-routing/code-review.md` | written because the triage value is `run` |
| Archive | `none` | first run — no earlier record existed to rotate |

The 60 skipped files are all non-code (`*.md`, `.specify/specs/*`, `.specify/memory/*`) or generated
mirrors (`.specify/shared/*`, `.specify/skills/*`, `.specify/scripts/*`, proven byte-identical to
their sources by `cmp` for all seven pairs). Two of those skipped `.md` files are nevertheless
machine inputs of the judged code — `shared/definitions/sdd-routing-definitions.md` is parsed by the
engine at run time, and `skills/external/sdd-loop-driver/references/nested-invocation.md` is the
document the handoff tests read — and both were read as part of this judgement even though the
receipt does not credit them. Findings from that reading are in §3 (F3), not in the code record,
because they are documentation defects rather than code defects.

### 2.2 Classification-honesty audit (the surface T029 designates)

`tasks.md` T029 records that `/speckit.review` is this slice's classification-honesty audit surface:
the routing engine's determinism covers **declared** inputs, so a knowingly misclassified input
(a feature reported as `maintenance`) cannot be caught by the engine, and the audit's conclusion is
recorded here **without writing back into any verdict**.

What was audited, and how. Each of the golden table's 14 rows
(`shared/definitions/sdd-routing-definitions.md` § Golden case table) was checked on three axes:
(i) every declared value lies inside the closed domain its `§ Inputs` row declares; (ii) the
declared value is consistent with the row's own case id and 覆盖的需求面 text; (iii) the expected
verdict/reason pair is what the documented precedence and reason-code order produce. The engine was
then re-run live (`--action golden`, `all_match=True`, 14/14) and one adversarial probe was executed
against the documented limitation.

**Result — no discrepancy found on axes (i) and (iii).** All 14 rows carry in-domain values and
judge to their documented pair. Two rows are deliberately out-of-domain (`G5` `complexity: deep`,
`G14` `reversibility: maybe`), which is the correct shape for the `input-ambiguous` cases and is
what makes the exit-alphabet case meaningful.

**Result — axis (ii) is decidable for 12 rows and *not independently derivable* for 2.** `G2` and
`G7` are the two rows whose declared class is the whole point of the row, and neither carries the
evidence that would let a reader re-derive it:

- `G7-bounded-definition-correction` declares `change_nature: definition-class` with
  `blast_radius: local-bounded-definition-correction` and the rationale
  `只收紧一处定义措辞，语义不变`, expecting `direct`. Membership of `definition-class` is, by
  FR-008, "derivable from the target path without judgement" — but a golden row has no target path,
  so the one predicate that could falsify the declaration cannot be evaluated on the row. The
  rationale is a free-text claim any caller can copy verbatim; it is the escape hatch, and it is
  unguarded by construction.
- `G2-bounded-maintenance` declares `maintenance` ("preserves every existing capability and
  contract") on the same footing: the row states the class, the engine consumes it, and nothing on
  the row distinguishes an honest `maintenance` from a `feature` reported as one.

The probe makes the exposure concrete and reproducible:

```console
$ python3 scripts/python/sdd-route.py --action route --nature maintenance --traceability not-required \
    --blast-radius local --reversibility reversible --complexity standard --format text
verdict:            direct
reason_code:        direct-conditions-all-hold
triggered:          nature-preserves, traceability-not-required, blast-local, reversal-reversible, complexity-low, bounded-correction-recorded
```

A feature-scale change declared as `maintenance` routes to `direct`, by design and with no complaint.
The engine is not at fault — FR-008 assigns the path predicate to the declaration side, and the
requirement itself names `/speckit.review` and the driver's U4 check as the two guards. The audit
finding is therefore about the **guard**, not the verdict: the review surface records the observation
(this subsection), but nothing carries the record forward — no artifact consumes it, and a
`direct` verdict produced from a dishonest declaration leaves no trace that an audit ever looked.
Recommendation REC-5 addresses the cheapest version of this (a required `target_paths` column on
every golden row, so axis (ii) becomes decidable for all 14).

**No verdict was written back.** No requirement, contract, owner-document row or golden expectation
was changed by this audit; `G7` and `G2` keep their documented `direct` verdicts.

## 3. Findings (Problems & Improvement Targets)

### F1 — The slice's declared read-only authority surface was edited from inside the slice loop, and no declaration channel records it

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074a-authorized-routing/tasks.md:66` (the declaration), `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074-goal-team-sdd-unification/requirements.md:247-251,485-489,521-528` (the edit), commit `71954e31a`
- **Propagation surface**: `requirements.md` § Parent Mapping ("父规格仍是权威"), `feature-ref.md` § 5 ruling 1 ("Nothing here contradicts a parent clause"), `verification.md` DoD-8 — three artifacts state a premise this edit changed, and none carries a line about it. Non-empty surface ⇒ no mid-tier cap.
- **Evidence** (verbatim):

  ```
  **禁改面**: `.specify/specs/074-goal-team-sdd-unification/**`（父 spec 与父设计，含其 `tasks.md`，只读）…
  ```

  ```
  baseline_commit=71954e31a1ff58480342209c1d54329a05c30225
  …
  plan_edit_count=0

  > No line of a plan-owned surface was edited in this implement stage. Measured, not asserted:
  > `git diff --stat 71954e31a..HEAD -- plan.md data-model.md contracts/ quickstart.md research.md
  > feature-ref.md` prints nothing. There is therefore no `PLAN-EDIT:` line to declare, and no
  > substantive change to halt on.
  ```

  ```
  $ git show --stat 71954e31a -- .specify/specs/074-goal-team-sdd-unification/requirements.md
   .specify/specs/074-goal-team-sdd-unification/requirements.md | 12 ++++++++----
   1 file changed, 8 insertions(+), 4 deletions(-)
  ```

  The content of the edit is itself correct and declared in place — the parent's own new session
  row reads `Q: 074a 的 B-04 修复删除了每成员并发上限的逃逸口；父规格是否跟随？ → A: 跟随…`. Nothing
  was concealed.

- **Why it's a problem**: the slice's authority premise ("父规格仍是权威，本切片是其投影，不重新设计")
  became bidirectional in `71954e31a`, and the record a reader checks says the opposite. Worse, it
  says it in a form that cannot come out true: `plan_edit_count=0` is measured from
  `baseline_commit=71954e31a`, which **is** the commit that carried the parent edit — so the
  measurement range begins after the event, and no re-run can ever surface it. A green check whose
  baseline is downstream of its own subject is a claim, not evidence. The repository already ships
  the mechanism that would have caught it (`audit-plan-changes.py`, which reports undeclared touches
  and exits 1); this slice did not invoke it and instead hand-listed six paths — a set that by
  construction excludes the parent.
- **Proposed fix**: introduce a `PARENT-EDIT:` (or, generally, `READ-ONLY-EDIT:`) declaration token
  as a sibling of `PLAN-EDIT:` in the implement stage's declaration protocol, and make the
  read-only surface list an explicit `--plan-owned`/`--read-only` input to
  `scripts/external/audit-plan-changes.py`, so the audit reports undeclared touches of *any*
  declared-immutable path. Additionally require the closing task to state the measurement range's
  own commit, so a baseline that sits downstream of the audited event is visible on the face of the
  log.

### F2 — The code-review script's own `--help` still advertises the four-step non-interactive path and never names `capture`

- **Severity**: P1
- **Category**: Automation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/scripts/git-delta-review.sh:1443` (the `NON-INTERACTIVE PATH` block) and the `COMMANDS:` block above it; the command is dispatched at `:1485` and implemented at `:1277`
- **Propagation surface**: every unattended `/speckit.review` run that drives the deterministic path from `--help` instead of from the skill body. Non-empty ⇒ no cap.
- **Evidence** (verbatim, from `git-delta-review.sh help` in this run):

  ```
  COMMANDS:
    diff  … review … note … report … base … triage … start … receipt …

  NON-INTERACTIVE PATH (four steps, in this order — four, never three):
    1. base      resolve the range: base= head= base_source=
    2. start     record creation and rotation (required from the second run on)
    3. note      append opinions (repeatable, one call per opinion)
    4. receipt   coverage receipt and the summary verdict
  ```

  against the skill body it belongs to (`skills/internal/code-review/SKILL.md`):

  ```
  ### 非交互路径（Agent / CI：五步，不是四步）
  …
  5. `capture --review-file <record> --triage <value> [--unit <custom:owner/name>]` — 客户采集…
  > **修订记录（四步 → 五步，C-10）**：… 前序特性的一处闭合枚举（本节步骤枚举）被改写一次
  ```

- **Why it's a problem**: the script is the surface an agent reaches for when it wants the machine
  path, and `--help` is what it reads. It states a closed, emphatic count ("four, never three") that
  the skill has already revised to five, and omits the one step whose whole purpose is to make
  "findings reached the client channel" a mechanically checkable fact. An agent that follows the
  script's own instruction will skip step 5 silently — and will believe it has completed the path,
  because the script told it the path was four steps. This run hit exactly that: `capture` had to be
  discovered in the skill body, and the `--help` block it had already read said it did not exist.
- **Proposed fix**: make the `NON-INTERACTIVE PATH` block and the `COMMANDS:` block derive from a
  single list in the script (one array that both the dispatch and the help render), so a step cannot
  be implemented without appearing in the help. Until then, rewrite the block to five steps and add
  `capture` with its closed five-value outcome set.

### F3 — `pre-analyze-check.py` reports the same unresolvable-path advisory on every run, so each run must hand-adjudicate it

- **Severity**: P1
- **Category**: Automation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/pre-analyze-check.py:268-269`
- **Propagation surface**: every slice whose checklist cites `.specify/memory/`-relative paths — the convention is set by the checklist template and by existing checklists, so the advisory recurs. Non-empty ⇒ no cap.
- **Evidence** (verbatim from `verification.md` § GATE-2, advisory 3):

  ```
  {"check": "missing-path", "severity": "advisory", "path": "checklists/requirements.md", "line": 62,
   "message": "path does not exist under the repo: feedback/20261028T160637Z-speckit-requirements.md"}
  …
  3. `checklists/requirements.md:62` → `feedback/20261028T160637Z-speckit-requirements.md`. The bundle
     **does** exist, at `.specify/memory/feedback/20261028T160637Z-speckit-requirements.md`; the checklist
     cites `.specify/memory/`-relative paths throughout … so this is a resolution-convention artefact rather
     than a missing artifact. The checklist is a dated record from an earlier stage; its citations are left
     byte-identical rather than rewritten in this stage.
  ```

- **Why it's a problem**: the checker resolves a cited path against the repository root only
  (`"path does not exist under the repo: %s"`), while the requirements-stage checklist — a generated
  artifact — cites paths relative to `.specify/memory/`. The result is a permanent, correct-by-
  construction advisory that every stage must re-adjudicate in prose, and the adjudication is
  re-derived each time because the log that carries it belongs to a different slice. That is the
  recurring toll: real advisories sit beside a known-noise one, and the noise has to be re-argued
  every run instead of being silenced once.
- **Proposed fix**: resolve a cited path against both the repo root and `.specify/memory/` (a second
  candidate root is cheap and removes the class of false positive), or — better, per the
  program-first discipline — have the checklist template emit root-relative citations and add a
  regression case here with the pre-existing checklist as its fixture.

### F4 — Two identifier families share the `V-n` prefix inside one slice, so `V-6` means two different rules

- **Severity**: P2
- **Category**: Documentation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/references/nested-invocation.md:23-30` against `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074a-authorized-routing/data-model.md:40-46`
- **Propagation surface**: `none` — no artifact in the slice cites the reference's `V-n` ids by number (the contracts cite E-ids and C-ids; the tests cite the data-model's `V-14`/`V-15`/`V-17`/`V-18`/`V-20`/`V-21`). Mid-tier cap applies, and P2 is below it.
- **Evidence** (verbatim):

  ```
  | V-6 | 裁决缺失，或裁决不是 SDD 值 | `verdict_ref` 必须引用一条**已记录**的路由裁决…
  ```

  ```
  **V-6**: `scope` 超出该席位 territory → 拒绝；并发判定交给既有 line registry，不新增第二套并发机制。
  ```

  The overlap is systematic: reference `V-1` (Goal missing) is data-model `V-3`; reference `V-3`
  (terminal Goal) is data-model `V-4`; reference `V-6` (missing verdict) is data-model `V-7`.

- **Why it's a problem**: an identifier is the reader's pointer into the knowledge network, and here
  one pointer resolves to two rules with an 8-row offset. The new file is the last surface a reader
  reaches, and it re-uses an id space its sibling already owns without saying so — the exact defect
  the project's Grounded Naming and ID-register discipline name. Damage is currently zero (nothing
  cites it), which is precisely why it is cheap to fix now and expensive to fix after `074b` starts
  citing the entry-validation table.
- **Proposed fix**: rename the reference's six rows off the `V-` space (e.g. `EV-1`…`EV-6`, "entry
  validation") and state in its owner line that the slice's validation-rule ids stay with
  `data-model.md`; or cite the data-model ids and keep only the pointer in the reference.

### F5 — `verification.md` advertises a `post_change_commit` that predates the sections it introduces

- **Severity**: P2
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074a-authorized-routing/verification.md:23`
- **Propagation surface**: `none` — the record's own gate section and DoD-8 row are self-contained; the stale value misleads only a reader who tries to resolve the measurements at that commit. Mid-tier cap applies.
- **Evidence** (verbatim):

  ```
  implementation_date=2026-10-29
  post_change_commit=f1d65142ad73433a838a096120f837706ba20644
  ```

  ```
  8e1a41536 docs(074a-authorized-routing): record SC-001..SC-006 with bound evidence … (T031)
  0024585c4 docs(074a-authorized-routing): re-run the four gates green … (T032)
  ```

- **Why it's a problem**: `post_change_commit` reads as "the tree state at which the post-change
  measurements were taken". `f1d65142a` is T030; the SC evidence block was written in the next
  commit and the gate re-runs in the one after that. A reader who checks out the advertised commit
  gets a log whose SC and gate sections do not exist yet, so the value cannot be trusted for the very
  purpose it exists for. The field is not wrong so much as unowned: no task row is responsible for
  advancing it, and the last two rows both edited the file it lives in without touching it.
- **Proposed fix**: rename the field to name what it measures (e.g.
  `measurements_taken_at_commit=`), or require the closing task to advance it and pin it with the
  evidence hashes in the same block — the hashes already bind the *content*, so binding the *commit*
  the same way makes the pair self-checking.

### F6 — A closed task row carries an obligation the next stage discharges, so a fully closed slice still owes a named duty

- **Severity**: P2
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/074a-authorized-routing/tasks.md:199` (T029)
- **Propagation surface**: `none` — the audit outcome lands in this report (§2.2), which is a different stage's artifact by design. Mid-tier cap applies.
- **Evidence** (verbatim):

  ```
  - [X] T029 … 同趟落审计职责——`/speckit.review` 是本切片的分类诚实性审计面（复核每条已声明输入的分类、记录不一致；嵌套运行另加驱动 U4 独立校验），引擎的确定性只覆盖声明输入，故审计结论记入 review 证据而不回写裁决
  ```

  and `tasks.md` DoD-1:

  ```
  - DoD-1: 全部 32 行任务为 `[X]`；若出现 `[~]`，其理由逐条记录在 … `deferred_tasks=`
  ```

- **Why it's a problem**: the row is marked `[X]` at implement close, and DoD-1 then reports the
  slice as fully closed — while the second half of that same row is performed by a later stage that
  had not run. The row is honest in its wording ("designates the audit surface"), but the state
  machine has no way to represent "this row's obligation is discharged downstream", so the tick and
  the obligation disagree. It is the recording-class version of a green check that has not gone red
  yet: the slice's own closure arithmetic cannot tell the two states apart.
- **Proposed fix**: let the task-state vocabulary express a downstream hand-off explicitly (a
  `[>]`-style *claimed-by-another-stage* state, or a `deferred_to_stage=` field per row carried into
  `deferred_tasks=`), and have the tasks template forbid a row whose completing artifact belongs to a
  later stage from closing as `[X]` without that declaration.

## 4. What Worked — Preserve (Brief)

- Hash-bound evidence rows: all six `evidence_sha256` values in `verification.md` re-hash clean in this run (SC-001…SC-006), so every `pass` claim still resolves to the bytes it was made over.
- Mirror discipline: all seven source/mirror pairs are byte-identical (`cmp`), `sync-mirrors.py --check` clean, and no `.specify/` projection was hand-edited.
- Clause accounting: 47 clauses, 47 distinct `[green:]` claims, none unclaimed, none double-claimed — verified independently of the gate script.
- Red-first evidence per task (`notes/red-t005.txt` … `notes/red-t022.txt`), each carrying command, real output and exit code.
- Disclosure culture: `post_change_full_suite_*=not-evaluated` rather than a claimed full run; the same-author condition disclosed in `plan.md`; the GATE-8 pre-close value (`1`) shown beside the post-close value (`0`).
- Analyzed-fix rounds recorded as decisions with reasons (`plan.md` § Plan Revision), including the two contradictory exit alphabets that F-01 reconciled.
- Independent re-run in this review: the five new contract modules plus the pin-change file collect and pass — `115 passed in 2.50s` (86 new cases + 29 pre-existing in the pin file), and `--action golden` returns `14 cases, all_match=True`.

## 5. spec-kit / SDD Improvement Recommendations

> `REC-…` identifiers below are coined here and are **not** registered in
> `.specify/memory/register.md` by this run: the dispatch that commissioned this review scopes the
> commit to `review.md` plus its evidence and forbids staging anything else, so registration is left
> to the driver. Coining without registering is disclosed rather than silently done.

### 5.1 Automation / Script Improvements

- **REC-1 — Declare read-only surfaces and audit them mechanically** — Target: `skills/external/sdd-loop-driver/scripts/audit-plan-changes.py` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/audit-plan-changes.py`) plus `skills/external/sdd-loop-driver/references/stage-prompts.md`. Change: accept a declared read-only surface list beside the plan-owned list, accept a `PARENT-EDIT:`/`READ-ONLY-EDIT:` declaration token, and report any undeclared touch of either list — including a touch that landed *before* the audit baseline, which is the case F1 could not see. Source: F1. Expected impact: an authority surface can no longer move without a declaration line, and a baseline that sits downstream of the event stops being able to hide it.
- **REC-2 — One step list drives both the dispatch and the help** — Target: `skills/internal/code-review/scripts/git-delta-review.sh` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/scripts/git-delta-review.sh`). Change: derive the `COMMANDS:` and `NON-INTERACTIVE PATH` blocks from the same ordered step list the dispatcher uses, so `capture` cannot be implemented without appearing in the help; correct the block to five steps meanwhile. Source: F2. Expected impact: removes a live trap in which the machine path's own documentation teaches a caller to skip its fifth step.
- **REC-3 — Resolve citations against a second candidate root** — Target: `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/pre-analyze-check.py`). Change: when a cited path does not resolve at the repo root, retry it under `.specify/memory/` before emitting `missing-path`; add the existing `checklists/requirements.md` as a regression fixture. Source: F3. Expected impact: retires one permanently-adjudicated advisory per stage per slice, so real advisories are not read beside known noise.

### 5.2 Workflow Improvements

- **REC-4 — Give a downstream-discharged obligation its own state** — Target: `templates/tasks-template.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/templates/tasks-template.md`) and `templates/verification-log-template.md`. Change: add a per-row downstream-hand-off declaration carried into `deferred_tasks=`, and rename `post_change_commit` to a field that names what it measures and requires the closing task to advance it. Source: F5, F6. Expected impact: a fully ticked slice stops implying that every named duty has been discharged, and the commit a measurement block advertises can actually be checked out to find it.

### 5.3 Documentation Improvements

- **REC-5 — Move the entry-validation ids off the `V-` space, and make the golden rows' class decidable** — Targets: `skills/external/sdd-loop-driver/references/nested-invocation.md` (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/references/nested-invocation.md`) and `shared/definitions/sdd-routing-definitions.md` § Golden case table (absolute supplement: `/storage/project/cloud-native-ai/spec-kit/shared/definitions/sdd-routing-definitions.md`). Change: rename the reference's `V-1`…`V-6` rows to a family of their own; add a `target_paths` column to every golden row so that FR-008's path predicate — the only thing that can falsify a `definition-class` declaration — becomes evaluable on the row it is supposed to govern. Source: F4, and §2.2's axis-(ii) result. Expected impact: one id resolves to one rule again, and the escape hatch (`G7`/`G2` declared class) stops being the one part of the golden table a reader must take on faith.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Declare and mechanically audit read-only surfaces (PARENT-EDIT / READ-ONLY-EDIT) | `skills/external/sdd-loop-driver/scripts/audit-plan-changes.py`, `references/stage-prompts.md` | F1 |
| P1 | One ordered step list drives both dispatch and `--help` (five-step path) | `skills/internal/code-review/scripts/git-delta-review.sh` | F2 |
| P1 | Resolve cited paths against `.specify/memory/` before reporting `missing-path` | `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` | F3 |
| P2 | Downstream-hand-off state for task rows; honest `post_change_commit` | `templates/tasks-template.md`, `templates/verification-log-template.md` | F5, F6 |
| P2 | Entry-validation ids off `V-`; `target_paths` column on golden rows | `skills/external/sdd-loop-driver/references/nested-invocation.md`, `shared/definitions/sdd-routing-definitions.md` | F4, §2.2 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; no target needed an `external` marking.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
