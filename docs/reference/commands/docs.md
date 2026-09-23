# /speckit.docs

Reconcile the project documentation space by deciding **what to write** and **where each document belongs**, then dispatching work to the owning documentation skills.

> Architecture: `/speckit.docs` is a thin three-stage orchestration layer. Static structure and structural actions are owned by `.specify/skills/create-docs/SKILL.md`; evidence-backed content changes are owned by `.specify/skills/improve-docs/SKILL.md`. Reconcile semantics remain authoritative in `.specify/shared/patterns/reconcile-pattern.md`.

## When to Use

- Establish or refresh the project's intended documentation structure.
- Converge misplaced, unindexed, stale, incomplete, or contradictory documentation.
- Write a new document from a user commission while baseline reconciliation still runs.
- Route existing-document content fixes without creating a competing copy.
- Maintain the notes lifecycle or hand off optional site publishing.

## Syntax

```text
/speckit.docs                    # full reconcile
/speckit.docs <path-or-target>   # directional reconcile for one target
/speckit.docs <raw material>     # fan-out intake
/speckit.docs <writing request>  # baseline reconcile plus additional writing action
```

`/speckit.docs` is a chat instruction, not a terminal command.

## The Two Core Decisions

### 1. What to write

A writing action starts with a content plan containing five inputs:

- target reader;
- current task context;
- this run's user input;
- verified repository evidence;
- explicit writing boundary.

Missing decisive context is clarified before writing. Generic filler, taste, and unverified assumptions are not evidence.

### 2. Where it lives

The command searches for an existing canonical owner of the topic before creating anything. If coverage already exists, the action updates that document through `improve-docs`; otherwise, it selects exactly one canonical home through `create-docs` using the confirmed target structure and local conventions.

This owner-first rule prevents scattered near-duplicates and contradictory copies.

## Desired-State Layering

- **Static baseline**: owned only by `.specify/skills/create-docs/SKILL.md` § Desired-State Baseline. Open that owner for operative naming, taxonomy, lifecycle, and threshold rules; this reference does not copy them.
- **Project layer**: persisted in `.specify/docs/target-structure.md` as the **Target structure declaration**. It records project shape, readers, project-specific extensions, topic placement, and fixed discovery routes.
- **Run layer**: the current repository state plus this run's input and evidence.

The target declaration uses `templates/docs-target-structure-template.md` and preserves bytes outside its managed block.

## Three-Stage Execution Flow

1. **Establish or load the target**: create the declaration once, ask at most three necessary questions when evidence is insufficient, reuse it without churn, and propose evidence-backed redesign when project reality changes.
2. **Diff and decompose**: apply the tolerance band first, then emit typed actions carrying target, owner, evidence/source, and confirmation tier.
3. **Dispatch and report**: route structure to `create-docs`, content to `improve-docs`, preserve existing confirmation tiers, audit every run, and group residuals by owner.

User input is additional: baseline reconciliation always runs. Directional instructions affect current priorities; structural changes update the target only through the existing dry-run plan.

## Fixed Discovery Paths

Every created or moved canonical document updates the nearest human index and any required root entry in the same run.

When a canonical path belongs in Agent project knowledge, `/speckit.docs` dispatches `/speckit.instructions` to refresh `.specify/instructions.md` § Documentation Map and verifies that the row resolves. Generated compatibility instruction aliases are never edited directly.

The resulting residual report states both lookup routes:

- **Human**: canonical root or directory index → document.
- **Agent**: project instruction file → Documentation Map → document.

## Content Fan-Out and Abort

Evidence-backed content actions run one document at a time in sequence. There is **no per-run cap** and no silent truncation. Before dispatch, the command announces the full document count; the user may abort before dispatch or between documents. Completed actions remain complete, while unstarted actions are reported as pending for the next run.

## Deterministic Engine

```bash
python3 .specify/scripts/python/docs-utils.py --action scan --root .
python3 .specify/scripts/python/docs-utils.py --action expire --root .
python3 .specify/scripts/python/docs-utils.py --action clean [--yes] --root .
python3 .specify/scripts/python/docs-utils.py --action archive-check --root .
python3 .specify/scripts/python/docs-utils.py --action stats --root .
python3 .specify/scripts/python/docs-utils.py --action validate --root . [--allow-special NAME ...]
python3 .specify/scripts/python/docs-utils.py --action audit --root . --scope <s> --summary <text>
```

The engine supplies deterministic findings and audit output. It does not own or rewrite the target declaration.

## Static Site

Presentation and publishing remain optional and are owned by `create-pages`. Site requests are handed off rather than becoming documentation-space reconcile actions.

## Output Artifacts

| Artifact | Location | Lifecycle |
|----------|----------|-----------|
| Target structure declaration | `.specify/docs/target-structure.md` | cross-run, confirmed project contract |
| Observation snapshot | inline | per run |
| Dry-run plan | `.specify/docs/plans/` | per run when a confirmable action exists |
| Audit log | `.specify/docs/audit/` | every run, including no-op |
| Residual report | inline | per run |

## Tool Support

The canonical command template is distributed through the standard command-generation path to the supported AI agent CLIs present in the project.

## Related

- Structure and authoring owner: `.specify/skills/create-docs/SKILL.md`
- Existing-content owner: `.specify/skills/improve-docs/SKILL.md`
- Optional publishing owner: `.specify/skills/create-pages/SKILL.md`
- Reconcile pattern: `.specify/shared/patterns/reconcile-pattern.md`
- Instructions refresh command: `/speckit.instructions`
- Deterministic engine contract: `.specify/specs/033-docs-command/contracts/docs-utils-cli.md`
