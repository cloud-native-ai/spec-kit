# Requirements Stage Evidence — 2026-11-27

Line `context-management`; run `r20261127T070000Z-110a`; stage `requirements`; baseline `0419adae5`; branch `110-context-management` (worktree).

## Source set read in full (ai-harness 093)

`.ah/specs/093-context-management/requirements.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `verification.md`, `feature-ref.md`, `tasks.md`, `contracts/` (5 files), `checklists/` (2 files); framework files: `scripts/python/context-audit.py`, `shared/definitions/context-management-definitions.md`, the four `shared/declarations/facts/context-*.yaml`, the five guard modules, `templates/instructions-template.md` (093's section), `shared/definitions/framework-map.md` rows. `templates/tasks-template.md` verified **not edited by 093** (the DoD-7 note there is a premise disclosure, not a port target).

## Scaffold (A-16, disclosed)

- `create-new-requirements.sh` derives the next number from spec dirs, `.archive/`, and local/remote branch names in `<NNN>-<slug>` form; the current local branch `110-context-management` is itself counted, so the script would derive **111** and run `git checkout -b`, switching the worktree off the line branch.
- Per 107/108 precedent: manual scaffold from `.specify/templates/requirements-template.md` into `.specify/specs/110-context-management/requirements.md`, staying on branch 110; the script's template-copy step replicated, only its branch-creation step skipped. Recorded as A-16 in the spec.

## Probes — target surfaces and missing sensors (2026-11-27, this worktree)

1. **Instructions budget headroom**: `wc -c .specify/instructions.md` → `40170`; `grep -n 'INSTRUCTIONS_BUDGET_BYTES=' scripts/bash/generate-instructions.sh` → `119:INSTRUCTIONS_BUDGET_BYTES=40960`; headroom ≈ **790 B**. Section counts: `grep -c '^## ' templates/instructions-template.md` → `39`, live `.specify/instructions.md` → `40` (the live-only `## Recurring Operational Lessons` is preserved because the generator reconciles additively). The ambient section therefore ships only if the final `BUDGET:` line reads `within` (A-10).
2. **Missing sensor — 7-component package**: `grep -rn 'Tier G\|Tier T\|7-component' shared/ .specify/shared/` → **0 hits**. The real dispatch surface is `shared/definitions/superagent-definitions.md` § The super↔sub Protocol (seven role fields, four injections, uplink, settlement); FR-017/A-15 map only onto it.
3. **Missing sensor — project-context renderer**: `ls scripts/python/project-context-render.py scripts/python/project_facts.py` → both absent; the standing `## Project Context` block is produced by the agent render path in `src/specify_cli/__init__.py` (`render_agents_for_tool`), so the terminology boundary and RS-003 name that owner (A-3a).
4. **Missing sensor — absence vocabulary**: `grep -rn 'unreachable' shared/` finds only unrelated prose; `not-evaluated` appears only as a report rendering marker in `shared/guidelines/reporting-obligations.md`. No framework owner declares `absent` / `unreachable` / `empty` / `not-evaluated`, so the presence vocabulary is defined once in the new owner document (A-8); `Unobserved` still reaches `shared/declarations/facts/evidence-seven-states.yaml#/statement`.
5. **Missing sensor — per-slot caps**: the superagent protocol declares no per-slot cap; the real token economy owner is `shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First), cited by every bounded/content-bearing row (A-7).
6. **Mirror pairs**: `scripts/python/sync-mirrors.py` `MIRROR_PAIRS` = `templates → .specify/templates`, `skills/external → .specify/skills`, `skills/internal → .specify/skills/internal`, `agents → .specify/agents/templates`, `scripts → .specify/scripts` (strict extras), `shared → .specify/shared`. `specify init` copies the `scripts/`, `templates/`, `shared/` trees into a project's `.specify/` (measured in `src/specify_cli/__init__.py`).
7. **Declaration layer registration**: `shared/declarations/contract.yaml` carries `required_fact_keys` (fact / kind / statement / consumers / former_carriers), the closed `fact_kinds`, the three `exit_codes`, an append-only flat registration block (093/105 precedent), and the richer `registered_facts` sequence used only where extra `statement_keys` are required (094). The four context facts need no extra keys, so the flat append-only form is the chosen registration shape (A-6).
8. **Target paths verified present**: `.specify/constitution.md`, `.specify/instructions.md`, `.specify/glossary.md`, `.specify/features.md`, `.specify/features/`, `.specify/register.md`, `.specify/skills/` + `.specify/skills.md`, `.specify/tools/` + `.specify/tools.md`, `.specify/agents/templates/`, `.specify/agents/instances/`, `.specify/session/`, `.specify/knowledge/`, `.specify/workflow/git.md`, `.specify/shared/` (incl. `definitions/framework-map.md`, `guidelines/directory-governance.md`, `declarations/facts/runtime-store-layout.yaml`, `workflow/user-input-protocol.md`, `workflow/glossary.md`), `shared/declarations/contract.yaml`, `scripts/python/{declaration_reader,memory-utils,sync-mirrors,script-interface-check}.py`, `scripts/bash/{run-tests.sh,generate-instructions.sh}`, `docs/` + `docs/concepts/documentation-model.md`, `src/specify_cli/__init__.py`. `.specify/state/` is absent in this worktree (runtime state lives in the main tree's `.specify/state/`); the layout's `task-delta` row keeps it as a standing witness and its absence reads an absence token with a reason (FR-020).

## Deterministic gates (verbatim outputs)

- `validate-requirements.py .specify/specs/110-context-management/requirements.md` → exit 0, `status: ok`, `0 error(s), 0 warning(s)`, **283 lines, 40 definition rows, 6 shared strings**; all six labels pass → `test-evidence/requirements-validator.txt`.
- `pre-analyze-check.py --spec-dir .specify/specs/110-context-management --stage requirements --repo .` → `decision=pass errors=0 advisories=14 waived=0`, summary `fr=29 sc=11` → `test-evidence/pre-analyze-requirements.txt` + `.json`. The 14 advisories are all `missing-path` on not-yet-created deliverable paths (`shared/definitions/context-management-definitions.md`, its installed mirror, `.specify/scripts/python/context-audit.py`, `tests/fixtures/context-management/`) and on the standing witness `.specify/state/` (9 mentions in `requirements.md`; the checklist adds 5); each deliverable disappears at implement and the witness reads honestly by design.
- `decomposition-check.py --mode plan --requirements .specify/specs/110-context-management/requirements.md` → `decision=proceed`, `fr_count=29`, `fr_ceiling=120` → `test-evidence/decomposition-requirements.txt` + `.json`.

## Workspace guard

- Snapshot recorded before authoring: `test-evidence/workspace-requirements.json`; immediate self-check `clean` (rc 0). Final check recorded in `test-evidence/workspace-requirements-check.txt` (branch `110-context-management`, refs and `.specify/specs` listing unchanged apart from this line's own spec directory, which the snapshot already contains).

## Concurrency

- `requested=1`; `effective=not_evaluated`; `effective_reason=single-unit` — one bounded assignment, no independent units to parallelize.

## Wrap-up accounting

- Run determination, exec-quant and feedback record for the requirements stage (unit `skill:create-requirements`, `--feature 110-context-management`) — records land under `.specify/session/` and `.specify/feedback/` and are referenced by the stage records commit.