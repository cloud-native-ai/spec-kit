# Plan Stage Evidence — 2026-11-26

Line `team-view-degradation`; run `r20261126T071500Z-108a`; stage `plan`; attempt 1; base commit `4e5b8a11d`; branch `108-team-view-degradation` (worktree). Terminal authority: requirements + clarifications, constitution v1.20.0, instructions.

## Setup

- `bash scripts/bash/create-new-plan.sh --json` → exit 0, copied `.specify/templates/plan-template.md` to the spec's `plan.md`; JSON reported `FEATURE_SPEC` / `IMPL_PLAN` / `SPECS_DIR` / `BRANCH=108-team-view-degradation` / `HAS_GIT=true`.
- The template was filled in place (one `# Implementation Plan:` heading, the Requirement → Feature stamp, zero residual `[UPPER_SNAKE]` placeholders, the self-referential Note line removed). Plan integrity re-checked after every edit batch.

## Phase 0 measurements (research.md M1–M8)

All measurements were taken in this worktree on 2026-11-26; probe fixture trees were created under the sanctioned scratch root `.specify/.tmp/sdd-loop/tmp/team-view-degradation/plan-probe/`.

1. **Corpus** — 46 run files: 41 reports (28 compact-conforming + 13 report-style non-conforming), 3 auxiliary, 2 residue; zero 4-hex names in-repo.
2. **Current misreporting** — `viz-skill-arena` / `draw-two-layer-structure` / `draw-diagram-interactive` render `运行报告: 为空` and `最近报告: 未记录` at exit 0; the `未识别` line is unbounded.
3. **Degraded definition probe** — missing binding → engine exit 2 with the verbatim `binding-missing: … carries no binding block …`; view exit 5; `roster_delta: 未记录`; goal rendered only as a declared key; no repair pointer.
4. **Healthy fixture + baseline program** — `git show 54c6efa8c:scripts/python/team-view.py` materialized beside copies of `script_interface_cli.py` and `goal-utils.py`; baseline and current programs both exit 0 with stdout diff lines = 0 on the same healthy fixture; fixture snapshot unchanged (3 files); `git cat-file -e 54c6efa8c` ok; baseline blob sha256 == current file (`81fad3f9…`).
5. **Residue-only probe** — `运行报告: 为空`, latest `未记录`, exit 0 (the presentation FR-005 fixes).
6. **Toolchain** — `sync-mirrors.py --check` rc 0 zero DIFF; `regen-command-copies.py --check` rc 0; `pytest` 8.4.2 only under `/usr/local/bin/python3`.

## Deterministic gates (verbatim outputs)

- `pre-analyze-check.py --spec-dir .specify/specs/108-team-view-degradation --stage plan --repo .` → `decision=pass errors=0 advisories=48 waived=0`, `fr=25 sc=8 clauses=35` (`pre-analyze-plan.txt` / `.json`). Advisory composition: 36 `external-clause` (the `INV-NN` invariant ids in `data-model.md` are read by the legacy clause-form detector as an external namespace — the same noise 103's plan recorded) + 12 `missing-path` (the three planned test files do not exist before implement).
- `validate-decision-tensions.py --spec .specify/specs/108-team-view-degradation` → `status: ok`, 0 error / 0 warning, 0 records (N/A with one line per trigger) (`plan-decision-tensions.txt`).
- `decomposition-check.py --mode plan --requirements .../requirements.md` → `decision=proceed`, `fr_count=25`, ceiling 120 (`decomposition-plan.json`).
- `doc-consistency-check.py --action structure --spec-dir ...` → `status: not-applicable`, `two-way: not-run` (execution class), exit 0 (`plan-gates.txt`).
- `flow-class-check.py --action lookup --unit-id "spec:108-team-view-degradation"` → `flow_class: execution`, exit 0 (`plan-gates.txt`).
- Mirror baselines: `sync-mirrors.py --check` rc 0 (all pairs byte-identical), `regen-command-copies.py --check` rc 0 (`sync-mirrors-baseline.txt`).

## Two in-passing corrections (disclosed)

1. The first `pre-analyze --stage plan` run exited 2 as an **input error**: an EP-005 table cell contained a literal `|` inside a backticked regex, which split the row and made `Status` unparsable. Repaired in passing by rewording the cell (no claim changed); the gate then ran clean.
2. Two files referenced 103's program-contract clause ids (`C-28`…`C-34`) as `C-NN` tokens; the gate resolves clause ids only inside the 108 spec, so they were dangling. Repaired in passing by describing the superseded 103 clauses without clause ids (semantics unchanged).

Both are RP-1-class corrections (one reading consistent with the recorded intent, local, reversible, no downstream premise touched).

## Feature Integration

- `.specify/features.md`: slice row `108` status `Draft → Planned`; its Last Updated cell gains the plan-stage note (design set landed, gates, parent status unchanged).
- `.specify/features/027-team-management.md`: dated plan entry added under § Latest Review; parent status untouched (`Ready for Review`, no status regression).
- `.specify/register.md` and the state spine are untouched (the stage brief's "registry" boundary, interpreted per the line's clarify adjudication). No new durable identifier was coined (plan-local `T-` ids are unused — Decision Tensions is N/A).

## Test budget (E3 stage-status row, reduced field set — docs-only stage)

| Field | Value |
|-------|-------|
| stage | `plan` |
| row_type | `stage-status` |
| status | `not-run-docs-only` |
| selection_basis | this stage changed only Markdown design artifacts (plan set, feature index/detail); no executable surface changed; targeted selection would be empty |
| changed_paths | `.specify/specs/108-team-view-degradation/{plan.md,research.md,data-model.md,quickstart.md,feature-ref.md,contracts/*}`, `.specify/features.md`, `.specify/features/027-team-management.md`, `test-evidence/*` |
| evidence_ptr | this file; `pre-analyze-plan.json`; `sync-mirrors-baseline.txt` |

Command / rc / counts / new-failures / comparison baseline are not applicable to a docs-only stage and are not reported as `unknown`.

## Concurrency

`requested=1`, `effective=not_evaluated`, `effective_reason=single-unit` — one bounded assignment; the plan authoring is one indivisible unit with no independent file-disjoint work package worth a second carrier.

## Workspace guard

- Pre-authoring snapshot: `.specify/.tmp/sdd-loop/tmp/team-view-degradation/workspace-guard-plan.json` (branch `108-team-view-degradation`, 213 refs, `.specify/specs` listing incl. `108-team-view-degradation`).
- Post-authoring check: `workspace-guard.py --check … --repo .` → `{"status": "clean", "changed": []}`, rc 0 (`workspace-plan.json`, `workspace-plan-readings.txt`). No branch created, no spec directory added beyond this feature's own.

## Re-anchoring record

- T0 after setup, after Phase 0, after Phase 1 and before wrap-up: rules reloaded (unattended / no user questions / no push / no state-spine or `.specify/register.md` edit / single engine / healthy byte-fidelity / closed sets); five direction questions answered; verdict each time: `on-track`.

## Anomalies

- No anomaly requiring adjudication. The two in-passing corrections above are disclosed. No user question was asked; nothing was pushed; the state spine, `.specify/register.md` and all dated records (including the 103 spec artifacts) were left untouched.
