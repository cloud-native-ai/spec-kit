# Spec Kit Framework Map

Single source of truth for the `.specify/` layout map. Referenced from the `## Spec Kit Framework Map` summary in `.specify/instructions.md` — keep that summary a pointer; the table lives here.

This is a **map, not a manual**: it tells you *what* exists and *where* it lives; the *how* belongs to the documents each row points to. The framework state lives under `.specify/`:

| What | Where | Notes (what lives there — not how to use it) |
|------|-------|-----------------------------------------------|
| Project memory | `.specify/memory/` | constitution, features index + `features/<ID>.md`, glossary, register, `tools/` records, feedback store, `coaching/` (coaching-run products, one artifact per file under `<run-id>/`), `housekeeping/` (sdd-house-keeping run reports, one YAML per run), `session/` + `knowledge/` (memory-as-files), `evidence/` (evidence runs), `exec-quant/` (run measurements), `retention/` (record consume→receipt→retire summaries, receipts, plans, ledgers), `trigger/` (proactive-flow state), `sanitize/` (findings cache) |
| Long-lived runtime state | `.specify/state/` | per-entry state kept across sessions (never one shared aggregate); e.g. SDD loop-driver line spines — owner: `shared/guidelines/directory-governance.md` §5 |
| Temporary workspace | `.specify/.tmp/` | git-ignored scratch, cleaned at work-item end; e.g. `.specify/.tmp/sdd-loop/` (worktrees, cache, tmp) — owner: `shared/guidelines/temp-directory-discipline.md` |
| Goals | `.specify/goal/<slug>/` | goal definitions plus per-goal `summary/`; owner: `/speckit.goal` + `goal-utils.py` |
| History knowledge base | `.specify/history/` | distilled, theme-aggregated conversation knowledge; owner: `/speckit.history` + `history-utils.py` |
| Review reports | `.specify/review/` | archived code-review reports; owner: the `code-review` skill |
| Project summary | `.specify/project/` | `summary/` delivery directory plus legacy manage-project artifacts (read-only); owner: the `summarize-project` skill |
| Spec archive | `.specify/archive/spec/` | archived feature specs; owner: `/speckit.sanitize`'s archive-spec disposition |
| Artifact templates | `.specify/templates/` | requirements/plan/tasks templates rendered by `/speckit.*` |
| Automation scripts | `.specify/scripts/` | bash/python engines invoked by commands and skills |
| Installed skills | `.specify/skills/` | one directory per skill (`SKILL.md` + references/ + scripts/) |
| Skills system guide | `.specify/skills.md` | how skills are discovered and created — no registry |
| Tools system guide | `.specify/tools.md` | how tools are recorded and discovered — no registry |
| Git workflow state | `.specify/workflow/git.md` | framework-level git workflow: branch-role managed block (the `.specify/workflow/` directory holds workflow state files), machine-maintained by the `git-utils` skill |
| **Agent Templates** | `.specify/agents/templates/` | capability descriptions — shipped role set installed by `specify init`; each `.agent.md` is self-contained |
| **Agent Instances** | `.specify/agents/instances/` | responsibility-bound agents authored in this project; reference a Template |
| **Agent Execution** | `.specify/agents/execution/` | dispatch `configs/` + `scripts/` (tracked); runtime `logs/` (gitignored, never committed) |
| Teams | `.specify/teams/<slug>/` | team definitions + `runs/` reports; run intermediates in git-ignored `.work/` |
| Derivations | `.specify/derive/` | one derivation archive per topic (`<topic-slug>/derive.md`) plus the project-level reasoning-move library `moves.md` (engine-written, accumulating); record semantics in `definitions/derivation-definitions.md` |
| Shared definitions & conventions | `.specify/shared/` | canonical concept docs — e.g. agent taxonomy (`definitions/agent-definitions.md`), subagent modes (`definitions/subagent-definitions.md`), tool definitions, workflow conventions; two meta-skill owners (`definitions/mechanism-policy-definitions.md`, `definitions/skill-reference-definitions.md`) |
| Declaration layer contract | `.specify/shared/declarations/contract.yaml` | value domains the declaration layer is read through — schema and subset ids, five fact kinds, two completeness states, three exclusion reasons, three exit codes, required key sets, gate call sites; the discipline itself is `definitions/harness-triple-definitions.md` (framework source: `shared/declarations/`) |
| Declaration facts | `.specify/shared/declarations/facts/` | one fact per file, one file per fact — `<fact-slug>.yaml`, the path IS the identity; no index, no manifest, no cache (framework source: `shared/declarations/facts/`) |
| Declaration exclusions | `.specify/shared/declarations/exclusions/` | one file per exclusion reason (`<reason>.yaml`), each row carrying `unit` / `carrier` / `anchor`; rows are appended, never reordered (framework source: `shared/declarations/exclusions/`) |
| Feature specs | `.specify/specs/<ID>-<slug>/` | requirements / plan / tasks / verification per feature |
| Canonical AI instructions | `.specify/instructions.md` | single source of truth for project-level AI instructions; per-tool files are symlinks (see `workflow/symlink-model.md`) |
| [Other project-specific location] | [Path] | [What lives there] |

> Agent layer taxonomy (Template → Instance → Execution) is defined once in `.specify/shared/definitions/agent-definitions.md` — consult it before creating/refining/running agents.
>
> Self-Improvement terminology is defined once in `.specify/shared/definitions/self-improvement-definitions.md`; policy, reusable structure, and execution order live respectively under `guidelines/`, `patterns/`, and `workflow/`.
