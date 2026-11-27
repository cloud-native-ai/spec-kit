# Plan Stage Evidence — 2026-11-27

Line `context-management`; run `r20261127T070000Z-110a`; stage `plan`; baseline `df4d31ee5` (checkpoint
02); branch `110-context-management` (worktree).

## Source set read (ai-harness 093 design set)

`.ah/specs/093-context-management/` — `plan.md` (35,850 B), `research.md`, `data-model.md`,
`quickstart.md`, five files under `contracts/` (`owner-and-layout`, `declarations-and-domains`,
`matrix-and-triggers`, `engine-and-distribution`, `guards-and-boundaries`), `feature-ref.md`. Every `.ah/`
path was adapted to `.specify/` per requirements A-3; the two registries (`features.md`,
`.specify/register.md`) and the decision archive were **not** written (A-2, PA-13).

## Probes — target carriers and missing sensors (all measured 2026-11-27, this worktree)

1. **Carrier existence**: 46 named carriers probed by `[ -e ]` — all `OK` (superagent/re-anchoring/
   framework-map/harness-triple/script-interface definitions; token-efficiency, confirmation-gates,
   fast-fail, temp-directory, directory-governance, closed-set-claims, bilingual, one-source,
   user-facing-comprehension guidelines; user-input-protocol, acceptance-hardening,
   objective-analysis-gate, glossary workflows; contract.yaml and the facts; declaration_reader,
   sync-mirrors, memory-utils, script_interface_cli, script-interface-check; generate-instructions,
   run-tests; `.specify/` anchors; `src/specify_cli/__init__.py`; tests trees).
2. **Missing sensors (adapted, never fabricated)**: `grep -rn 'Tier G|Tier T|7-component' shared/
   .specify/shared/` → 0 hits (the real payload is the seven-field/four-injection super↔sub protocol);
   `scripts/python/project-context-render.py` and `project_facts.py` absent — the standing
   `## Project Context` block is rendered by `render_agents_for_tool` (`src/specify_cli/__init__.py:648`)
   over `agents/*.agent.md`; no framework owner declares `absent`/`unreachable`/`empty`/`not-evaluated`
   — all five presence tokens are defined once in the new owner document (A-8); no per-slot cap exists —
   the cap/exception owner is `shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First).
3. **Instructions budget**: `wc -c .specify/instructions.md` → 40,170; generator constant
   `INSTRUCTIONS_BUDGET_BYTES=40960` (`scripts/bash/generate-instructions.sh:119`) → headroom 789 B;
   section counts 39 (template) / 40 (live; the live-only `## Recurring Operational Lessons` is preserved
   by the additive reconcile). The ambient section MUST read `within`; no raise, no trim (A-10).
4. **Mirror baseline**: `python3 scripts/python/sync-mirrors.py --check` exit 0 — six pairs byte-identical
   (templates 23, skills/external 439, skills/internal 139, agents 20, scripts 133, shared 117), six
   projections `ok` → `test-evidence/mirror-baseline-plan.txt`.
5. **Declaration layer**: `contract.yaml` carries `required_fact_keys`, five `fact_kinds`, three
   `exit_codes`, the append-only flat registration block (093/105 precedent, lines 64–77) and the richer
   `registered_facts` sequence (094, not needed here); `--action get --fact memory-types` returns the
   parsed closed-set body (statement `session`, `knowledge`).
6. **Fresh-init probe**: `specify init plan-init-probe --ai qoder --no-git --ignore-agent-tools` (installed
   CLI 0.0.22, framework commit `fed513bc`) exit 0 in a sanctioned scratch root, since removed. Fresh tree
   carries `constitution.md`, `features.md`, `features/`, `workflow/git.md`, `tools.md`, `shared/`,
   `agents/`, `scripts/`, `templates/`, `memory/`, `source.json`; lacks `instructions.md`, `glossary.md`,
   `register.md`, `skills.md`, `tools/`, `session/`, `knowledge/`, `state/`, `docs/` and (predating this
   feature) the new owner document, facts and engine. Recorded as RU-2's measured anchor set.
7. **Dependency extraction**: eleven dependency features declared with their real artifacts; the
   extraction set (blocked/deferred/partial status rows + non-empty `deferred_tasks=`) yields 14 records
   across `035` (1), `051` (7), `084` (3), `093` (3), each disposed `not-applicable` with a basis. Feature
   numbers ≠ spec numbers were resolved from each detail's links (055 has no `verification.md`; 105 has no
   per-feature detail file).

## Deterministic gates (verbatim outputs)

- `pre-analyze-check.py --spec-dir .specify/specs/110-context-management --stage plan --repo .` →
  `decision=pass errors=0 advisories=124 waived=0`, summary `fr=29 sc=11 clauses=39 files=12` →
  `test-evidence/pre-analyze-plan.txt` + `.json`. The 124 advisories are 115 `missing-path` on not-yet-
  created deliverable paths (owner document, four facts, engine, five test files, fixtures) plus the known
  absence `.specify/state/` and the deferred detail `.specify/features/110-context-management.md`, and 9
  `external-clause` notices on the plan's own `PA-NN` assumption labels (advisory namespace notices).
- `decomposition-check.py --mode plan --requirements .specify/specs/110-context-management/requirements.md`
  → `decision=proceed`, `fr_count=29`, `fr_ceiling=120` → `test-evidence/decomposition-plan.txt`.
- `doc-consistency-check.py --action structure --spec-dir .specify/specs/110-context-management` →
  `class=execution source=declaration`, `status: not-applicable`, `two-way: not-run` →
  `test-evidence/doc-consistency-plan.txt` (the structural chapter gate applies to expression-class lines
  only; the plan carries no `## Document Structure` section by design).
- **Plan integrity**: exactly one `# Implementation Plan:` heading (line 1); `**Requirement → Feature**`
  stamp present (line 4); zero residual `[UPPER_SNAKE_CASE]` placeholders; the template's self-referential
  note line is removed.

## Corrections disclosed (in-passing; not anomalies)

1. The first gate run failed with 9 `dangling-id` errors: the plan and research cited the instructions-
   propagation test's own clause names (`C-1`/`C-2` and `C-10`/`C-11`/`C-14`), which the gate reads as
   this spec's contract ids (`C-001`…`C-046`). Reworded to prose descriptions of those legs; re-run is
   `decision=pass errors=0`.
2. One path slip in `quickstart.md` — `.specify/memory/tools/` corrected to `.specify/tools/` per A-3's
   recorded mapping (`.ah/memory/tools/` → `.specify/tools/`).

## Workspace guard

- Snapshot `test-evidence/workspace-plan.json`: branch `110-context-management`, 215 refs, 92 spec
  directories. Compared with `workspace-requirements.json`: branch identical, refs added/removed = none,
  spec directories added/removed = none.
- `test-evidence/workspace-plan-check.txt` records the raw `git status --short` and the attribution: the
  `20261125T140702Z…clarify-artifact…` record stays an untouched other-run modification; the
  `20261125T173624Z…create-plan…107c…` record was **settled by this stage's own determination call**
  (07:48:47Z) and is committed with the accounting records.

## Concurrency

- `requested=1`; `effective=not_evaluated`; `effective_reason=single-unit` — one bounded assignment, no
  independent units, and the stage forbids dispatching other agents.

## Wrap-up accounting

- `run-determination.py --action determine --unit-id "skill:create-plan" --run-id
  r20261127T070000Z-110a --complexity complex --feature 110-context-management` (elapsed 835,000 ms
  measured from the spine's `stage_started_at`) → `test-evidence/plan-run-determination.txt`; record
  `.specify/session/20261127T074847Z-run-determination-skill-create-plan-r20261127t070000z-110a.md`.
- `exec-quant.py --action collect` → `test-evidence/plan-exec-quant.txt`; record
  `.specify/exec-quant/records/20261127T074850335988Z-00b03532.json`.
- `feedback-utils.py --action record` → `test-evidence/plan-feedback-record.txt`; record
  `.specify/feedback/20261127T074856Z-skill-create-plan.md`. Threshold notice: `count_since_submission=605`
  ≥ threshold 10, `should_prompt=true` — surfaced as a non-blocking notice only; nothing transmitted.
- **No test run was warranted** for this stage: the run produced design artifacts only (no executable
  change, no test file authored here); the gate program and the read-only mirror check are the executable
  evidence, both captured above.

## Anomaly line

`未发现异常` — no anomaly; two in-passing corrections and one record-settlement side effect are disclosed
above.