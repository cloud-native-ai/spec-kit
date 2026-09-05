<!-- AUTO-GENERATED from templates/commands/docs.md — do not edit; edit the source template, then run scripts/python/regen-command-copies.py -->
## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](.specify/shared/workflow/user-input-protocol.md). Treat as command parameters, not standalone instructions. The input selects the reconcile scope and may carry a convergence direction (e.g. "整理 README"、"激进重组") or a **writing commission** (e.g. "写一份部署教程"、"新增 xxx 的概念文档") that the skill routes to its Authoring Flow.

## Glossary

Consult the project glossary (`.specify/memory/glossary.md`) and apply the protocol in `.specify/shared/workflow/glossary.md`: correct recorded homophone/confusable variants before acting; propose new terms at wrap-up with user confirmation.

## Outline

`/speckit.docs` is the **thin orchestration layer** for every documentation-space operation. It owns only target-declaration coordination, typed-action decomposition, and dispatch order; it never copies engine rules into this command:

- `skills/create-docs/SKILL.md` is the **single source of truth** for the static baseline, Scope Resolution (全量 / 单目标 / 写作 / 扇出 / Bootstrap), structural actions, the Reconcile Loop from [.specify/shared/patterns/reconcile-pattern.md](.specify/shared/patterns/reconcile-pattern.md), the four per-run artifacts (观察快照 / 干跑计划 / 审计日志 / 残差报告), tiered confirmation, Authoring Flow, and `docs-utils.py` automation.
- `skills/improve-docs/SKILL.md` is the **single source of truth** for evidence-backed content improvement of an existing correctly placed document.

### Stage 1 — Establish or load the target structure

The persistent project-specific declaration is `.specify/docs/target-structure.md`; bootstrap it from `.specify/templates/docs-target-structure-template.md`. Its managed region is bounded by `<!-- DOCS_TARGET_STRUCTURE_START -->` and `<!-- DOCS_TARGET_STRUCTURE_END -->`.

1. If the declaration is absent, inspect repository evidence for project shape, audience, current topic inventory, and project-specific extensions. If that evidence is underdetermined, ask one batch of **1–3 necessary questions**; **no declaration or convergence write** happens **before answers arrive**.
2. Present the first declaration and the convergence plan together at the existing **R4** dry-run confirmation. Safe local writes remain 自动执行; move/archive/restructure actions remain **stop-and-confirm**; the formal zone remains 只归档不删除.
3. If a valid declaration exists and the user did not request a reset, reuse it without redesign or timestamp churn.
4. If repository evidence shows **substantive drift**, add a **redesign proposal** to the same R4 plan. The declaration remains byte-identical **before confirmation**.
5. On missing, unpaired, or unparseable markers, stop and request repair or explicit rebuild authorization; never overwrite the whole file. A valid refresh replaces only managed content and preserves all **outside-block bytes**.

### Stage 2 — Diff and decompose typed actions

After Stage 1 yields a confirmed target, compare current state with it **tolerance band first**. A tolerated difference is reported as consistent and **must not become an action**.

Every substantive action row MUST carry: **type**, **target**, **owning skill**, **confirmation tier**, **source**, and execution result; a content action also carries **evidence**. The source is either baseline reconcile or user input. A **content action requires concrete evidence** from deterministic findings, verified staleness, user correction, or feedback; **Unobserved** is not a defect and produces no content action.

Route each action **mechanically** to **exactly one owning skill**:

- **structure** — placement, naming, creation, move, archive, index, frontmatter, or link structure → `create-docs`;
- **content** — accuracy, staleness, completeness, readability, or render-safe prose in an existing correctly placed document → `improve-docs`;
- **user commission** — classify by its actual structure/content effect, then use the same routing rule.

### Stage 3 — Dispatch and report

Dispatch structural actions through one `create-docs` reconcile. Dispatch judgement-based content actions **one document at a time**, **sequential** in severity order; only a single mechanical dimension may use the bounded-batch exception owned by `improve-docs`.

Content dispatch has **no per-run cap** and MUST NOT truncate or silently defer the tail. Before dispatch, **announce the full document count** so the user can **abort before dispatch**. Each document boundary is another abort point: **completed actions stay completed**, while unstarted actions become `pending` in the residual report for the next run.

Use the owners' existing confirmation tiers; this orchestration **does not introduce another gate**. Group the residual report by owning skill and list converged, tolerated, pending-human-decision, pending, and “no finding” outcomes. Append the audit log even on **zero convergence**.

`$ARGUMENTS` remains an input to this one reconcile engine; it never creates a separate top-level mode. Additive-input routing is completed below without weakening these invariants.

**Delegation (mandatory)**: load both owning skills. Do NOT inline or re-implement their baseline, scope table, gates, reconcile loop, authoring rules, or content-improvement rules here.

Zone orientation (details in `create-docs`): managed = root entry files + `docs/` tree; read-only = source code, `.specify/specs/`, `.specify/memory/`; skip = compatibility symlinks, generated per-tool copies; archive = `docs/archive/`; run workspace = `.specify/docs/` (never mixed into `docs/`).

## Feedback

At wrap-up (the same lifecycle point where this command prompts for a Git commit), perform an agent self-reflection step (never solicit feedback content from the user), following the canonical convention in `.specify/shared/workflow/feedback-step.md`:

1. **Gate on qualification & completion.** Only proceed if this command reached its wrap-up stage. Skip trivial/no-op runs; for an aborted run use the abort/partial rule below.
2. **Reflect (no user input).** Review this run against `/speckit.docs`'s declared purpose and produce a short review plus ≥1 concrete, command-specific optimization point. If the run was clean, use exactly: `No significant optimization points identified this run.`
3. **Scope guard.** Keep strictly to this command's operation; do NOT produce a global/whole-project assessment (that is `/speckit.review`'s job). Entries are `scope: local`.
4. **Dedup guard.** Use a stable `run_id` (e.g. the reconcile scope + a run timestamp); if a nested skill/command already recorded feedback for this same `(unit_id, run_id)`, the engine no-ops.
5. **Persist** via the engine:
   ```bash
   python3 "${SKILL_WORKDIR:-.}/.specify/scripts/python/feedback-utils.py" --action record \
     --unit-id "/speckit.docs" --unit-type command \
     --run-id "<stable-run-id>" --feature "<feature-key-if-any>" \
     --review "<review prose>" --points-file "<points file>"
   ```
   Probe attribution: the engine resolves the unit to its probe object automatically — the entry inherits kind/slice from the probe registry. External custom units record via `--unit-id custom:<owner>/<name> --unit-type custom-unit`; their entries stay host-project-local and never enter upstream packages.
6. **Consolidated submission prompt(非阻塞).** If the returned `should_prompt` is `true`, append ONE non-blocking line to the wrap-up report inviting submission (point the user to the `/speckit.feedback package` command — the user-facing path; never paste the raw `feedback-utils.py` engine call into the user-facing line); it MUST NOT block the wrap-up flow and MUST NOT trigger any 自动传输 (manual delivery only; `--action mark-submitted` runs only if the user initiates submission). Below threshold, do not prompt.

**Abort / partial-run rule.** If the run failed before wrap-up, either skip recording or record with `--partial` and a `## Review` beginning `**Partial run** — `.

## Documentation

At the same wrap-up point, apply the docs-sync evaluation step per the canonical convention in [.specify/shared/workflow/docs-step.md](.specify/shared/workflow/docs-step.md): assess whether information produced by this run (new capabilities, key decisions, structural changes) needs to be recorded into the project documentation space. Conclude with exactly one of `需记录（目标文档 + 要点）` or `无需记录`; never block wrap-up; incremental judgment only — do NOT trigger a full reconcile sweep from this step.

## Handoffs

**Before running this command**:

- None required. On a project without a `docs/` structure the run resolves to Bootstrap scope.

**After running this command**:

- Address the residual report's pending-human-decision items.
- Invoke `memory-record` to persist notable reconcile decisions.
- If the reconcile changed instructions-facing structure (e.g. documentation map), run `/speckit.instructions` to refresh generated instruction files.
- To publish the space as a static site — or to repair mounts staled by a move — use the `create-pages` skill; presentation is an optional layer this command never scaffolds or builds.