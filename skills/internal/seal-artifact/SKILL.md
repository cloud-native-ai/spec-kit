---
name: seal-artifact
description: Merge split slices back into the parent spec and seal a reviewed spec at its terminal status — orchestrate the deterministic seal engine (merge-plan, merge-apply, seal), report its verdict verbatim, and never recompute a judgment. Use when the user mentions ["seal", "speckit.seal", "seal the spec", "merge back slices", "merge-back", "finalize the spec", "seal-artifact", "封装 spec", "合并回写", "封存", "终态"].
classification: internal
skill_id: "<SKILL:.specify/skills/internal/seal-artifact/SKILL.md>"
---

# seal-artifact

> **Concurrency obligation（执行义务，按指针抵达）**: this skill is an execution body — before the first real action, run the one-shot assessment (class → carrier → partition), default to concurrent execution for two or more independent units, and when serial name a reason code and record the `requested` / `effective` / `effective_reason` reading. Authored text: `shared/definitions/subagent-definitions.md` § The Concurrency Obligation; class table: `shared/declarations/facts/concurrency-class.yaml`; reason codes: `shared/declarations/facts/serial-reason.yaml`; reading fields: `shared/declarations/facts/effective-concurrency.yaml`. This body restates none of their rules.

## Goal

Take one reviewed spec to its terminal state: merge its split slices back into the parent spec when they exist, then fix the parent at `Sealed` with a receipt. This skill orchestrates the steps and reports what the engine said; every judgment — which directories are slices, which output files merge where, whether a conflict is open, whether the conjunctive seal conditions hold, whether the state faces agree — is computed by the deterministic engine and is never re-derived here.

Owning command: `/speckit.seal`. Engine: `scripts/python/seal-utils.py` (runtime face `.specify/scripts/python/seal-utils.py`). Its action set and exit-code semantics are owned by the engine; read them with `python3 scripts/python/seal-utils.py --help`. The status transition and its conjunctive conditions are owned by `shared/workflow/acceptance-hardening.md` § Feature Status; this skill reaches both owners by path and restates neither.

## Input Contract

- **Target**: the spec directory named by `$ARGUMENTS`, else `REQUIREMENTS_DIR` from the command's declared prerequisite script (`scripts/bash/check-prerequisites.sh --json --paths-only`, fields `REPO_ROOT`, `BRANCH`, `REQUIREMENT_ID`, `REQUIREMENTS_DIR`, `FEATURE_SPEC`, `IMPL_PLAN`, `TASKS`).
- **Repository root**: `REPO_ROOT`; pass it as `--repo` only when the engine would otherwise resolve the wrong root.
- **Action selection**: an explicit `merge-plan` preview or `merge-apply` request in `$ARGUMENTS` narrows the run to that action; the default full run is merge preview → merge apply (when slices exist) → seal.
- **Engine availability**: the engine is stdlib-only and must exist at the framework-source path or its runtime mirror. Absence is a hard failure reported as such — never a reason to judge from prose.

## Workflow

### 1. Preview the merge (read-only)

Run the engine's merge preview against the target:

```bash
python3 scripts/python/seal-utils.py --action merge-plan --spec-dir <spec-dir>
```

This action writes nothing. Read its report as the run's contract:

- **No open conflicts** — the report lists the slice set, the per-output-file actions, the ID maps and the conflict list. A single spec reports no slices; a split parent reports its slices and merge work. Continue.
- **Open conflicts** — the engine exits with its refusal status and names every conflict. Render the report verbatim, name the repair (edit the named inputs, then rerun the preview until the conflict no longer reproduces), and stop. Do not hand-merge a conflict the engine reported as open.
- **Input error** — report the engine's message and stop; do not proceed to a write action.

### 2. Apply the merge (only when the preview shows merge work)

```bash
python3 scripts/python/seal-utils.py --action merge-apply --spec-dir <spec-dir>
```

The engine writes the parent-side merged outputs, `merge-manifest.json` and the slice-side `**Merged into**:` markers, deterministically and idempotently. Report the written paths the engine names. A refused or error exit stops the run before any seal attempt.

### 3. Commit before sealing

The seal judgment refuses on a dirty spec tree, so after a successful apply commit exactly the merge products — the parent spec directory, the slice `requirements.md` markers, and any recorded factory-document resolution — staged by explicit path with a single-line message per `.specify/templates/commit-template.md`. Never `git add -A`, and never fold unrelated work into this commit. A single spec with no merge work needs no such commit; the tree must still be clean.

### 4. Run the seal judgment

```bash
python3 scripts/python/seal-utils.py --action seal --spec-dir <spec-dir>
```

The engine computes the judgment in a read-only phase and only then writes its batch (`seal.md`, the registry row and the feature detail). Report its stdout verbatim and resolve the outcome from the exit status alone:

- **Success** — the spec is `Sealed`, or it already was (the engine reports the idempotent case). Report the receipt path and the status faces it names.
- **Refusal** — the engine lists every unmet condition with its repair path and persists nothing. Render the complete list in the engine's order; do not reduce it, reorder it, or re-judge any line.
- **Error** — an input or environment error (including a state-face contradiction or a failed atomic write) is not a pass and not a refusal to negotiate. Report the engine's message and stop.

### 5. Report and hand off

State the target, the actions actually run with their exit statuses, the engine output verbatim, the artifacts written, and the next step: archive eligibility through the existing archive lane on success, or the named repairs followed by a rerun on a refusal. The archive admission query itself is the engine's own action and is consumed by the archive lanes (`/speckit.sanitize`, `manage-features`); this skill neither re-implements nor pre-empts it.

## Report

- **Target**: spec directory and repository root.
- **Actions**: each action run (`merge-plan` / `merge-apply` / `seal`), its exit status, and its full output.
- **Artifacts**: every file the engine reported writing; on a refusal, explicitly `none — refusals persist nothing`.
- **Next step**: archive lane, or the refusal list's repairs and the rerun command.

## Behavior Rules

- **The engine judges; this skill reports.** Never compute a slice set, a merge action, a conflict verdict, a seal condition or an admission result in prose.
- **Report refusals in full.** Every unmet condition appears, in the engine's order, with its repair path. Truncating or summarizing the list into fewer items is a defect.
- **Never read an error exit as a pass.** A state-face contradiction, an unreadable acceptance verdict or a failed atomic write is an error class of its own.
- **Do not call the acceptance engine directly.** The seal judgment obtains its closure verdict from `closure-acceptance-check.py` through the seal engine; a second invocation or a hand-rolled reading would be a second source of truth.
- **Read-only records stay read-only.** Review records, code-review records and measurement files are inputs; never edit, re-verdict or downgrade them.
- **Anomalies surface.** A missing engine, an unreadable output or a disagreement between report and tree is reported at the point it appears, following `shared/guidelines/fast-fail.md`.

## Boundaries

- **Archival is not this skill.** Retirement, deletion, moving and the registry's archive-pointer reconcile remain with `/speckit.sanitize`'s archive lane and `manage-features`; this skill implements neither the admission query nor any archive action (owners by pointer: `shared/definitions/non-disposable-definitions.md`, `shared/workflow/feature-integration.md`).
- **Review is not this skill.** `/speckit.review` owns review records and verdicts; the seal run reads them.
- **The command keeps its wiring.** Frontmatter, the User Input Protocol and the wrap-up lifecycle belong to `templates/commands/seal.md`.
- **Four actions, no fifth.** This skill invokes the engine's merge and seal actions only; it adds no move, delete, archive, push or scheduled behavior, and introduces no second state machine, registry or ledger.

## Wrap-up

<!-- AUTO-GENERATED by probe-utils.py --action compile-embeds — truth source: .specify/shared/definitions/probe-definitions.md (## Handler / ## HandlerBinding) — fingerprint: 4682b9e38032 — do not edit; edit the registry, then recompile -->

**Runtime-mode gate.** If `${SKILL_WORKDIR}/.specify/` does not exist, this skill is running in standalone mode (a non–Spec Kit deployment, e.g. a global agent skills directory) — skip this entire Wrap-up step: no engine call, no feedback entry.

1. Run Determination — `python3 .specify/scripts/python/run-determination.py --action determine --unit-id "skill:seal-artifact" --unit-type skill --run-id <RUN_ID> --complexity <COMPLEXITY>`；source args when available: `--session-file <SESSION_FILE> --session-rows <SESSION_ROWS> --tool <TOOL> --proxy-paths <PROXY_PATHS> --token-note <TOKEN_NOTE> --elapsed-ms <ELAPSED_MS> --elapsed-note <ELAPSED_NOTE> --names-current <NAMES_CURRENT> --names-baseline <NAMES_BASELINE> --declared-check <DECLARED_CHECK> --green-check <GREEN_CHECK> --red-first-refs <RED_FIRST_REFS> --collected <COLLECTED> --prev-user-turn-class <PREV_USER_TURN_CLASS> --unresolved-red <UNRESOLVED_RED> --red-source <RED_SOURCE>`
   尖括号为本轮运行时值——代入后照抄执行(占位 = 参数名去 --、转下划线、全大写;渲染集 = 引擎 manifest required + source,身份对已带实值)
2. Exec Quant — `python3 .specify/scripts/python/exec-quant.py --action collect --unit-id "skill:seal-artifact" --unit-type skill`；source args when available: `--run-id <RUN_ID>`
3. Feedback Record — `python3 .specify/scripts/python/feedback-utils.py --action record --unit-id "skill:seal-artifact" --unit-type skill --run-id <RUN_ID> --review <REVIEW> --points <POINTS>`
4. Threshold Notice — `.specify/shared/workflow/feedback-step.md` § "Threshold prompt protocol (canonical semantics for step 6)"
5. Token Reflection — `.specify/shared/workflow/feedback-step.md` § "Reflection procedure (the embedded step points here)"
6. Closeout — `.specify/shared/workflow/artifact-commit-step.md` § "The `## Close-out` step"
