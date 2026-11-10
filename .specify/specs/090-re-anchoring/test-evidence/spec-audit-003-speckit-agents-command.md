# Spec Audit — 003-speckit-agents-command (batch 1)

Read-only audit of `.specify/archive/specs/003-speckit-agents-command/` against the CURRENT tree.
Audited tree: `master` @ `564a5f5a6` (2026-11-10). No spec/source file was modified; this file is the only write.

## Scope

Artifacts read in full: `requirements.md`, `plan.md`, `tasks.md`, `data-model.md`, `quickstart.md`,
`contracts/agents-command.openapi.yaml`, `checklists/requirements.md`. No `verification.md` / `notes`
file exists in this archive entry.

Classification rule (stated for reproducibility):

- **alive** — the referenced path resolves in the live tree now.
- **archived-elsewhere** — the referenced object exists only under
  `.specify/archive/specs/003-speckit-agents-command/` (applies to spec-relative references that
  resolve inside the archive container).
- **dead** — no target at the stated path. Per the audit instruction, a stale pre-archive live-tree
  form (`.specify/specs/003-speckit-agents-command/...`) is dead even though a preserved copy exists
  under the archive; the preserved copy is named in the finding.

Counting unit: distinct repository path references (glob/pattern forms counted once). Line anchors
list every occurrence.

## Counts

| Class | Count |
|---|---|
| References total (distinct) | **30** |
| alive | **18** |
| archived-elsewhere | **3** |
| dead | **9** (7 stale pre-archive forms with a preserved archive copy; 2 with no target anywhere) |

No reference to `scripts/`, `skills/`, or `shared/` appears in this spec's artifacts.

## Reference inventory

### Alive (18)

| # | Reference | Anchors |
|---|---|---|
| 1 | `.github/agents/` | requirements.md:16,20,23,37,63,71,83,109; plan.md:10; data-model.md:6,64; quickstart.md:34,109 |
| 2 | `.github/agents/<agent-name>.agent.md` (pattern; dir exists) | requirements.md:80 |
| 3 | `.github/agents/<name>.agent.md` (pattern) | requirements.md:106 |
| 4 | `.github/agents/*.agent.md` (pattern) | plan.md:22; tasks.md:24 |
| 5 | `templates/commands/plan.md` | plan.md:6 |
| 6 | `.specify/specs/**` | plan.md:22 |
| 7 | `.specify/memory/**` | plan.md:22 (partial move pending — see below) |
| 8 | `README.md` | plan.md:53 |
| 9 | `docs/**` | plan.md:53 |
| 10 | `.specify/memory/constitution.md` | plan.md:53 (moves pending) |
| 11 | `.specify/memory/features.md` | plan.md:53; tasks.md:100 (moves pending) |
| 12 | `.specify/memory/features/001..019.md` | plan.md:53 — all of 001–019 exist (moves pending) |
| 13 | `src/specify_cli/` | plan.md:99-100 (structure tree) |
| 14 | `templates/commands/agents.md` | plan.md:104; tasks.md:14,46,137 |
| 15 | `.github/prompts/speckit.agents.prompt.md` | plan.md:108; tasks.md:15,24,25,26,27,28,43,44,45,63,64,65,82,83,84,85,136 |
| 16 | `.specify/memory/features/019.md` | plan.md:113; tasks.md:99 (moves pending) |
| 17 | `tests/` | plan.md:121 |
| 18 | `docs/tutorials/quickstart.md` | tasks.md:16 |

### Archived-elsewhere (3)

| # | Reference | Anchors | Resolves to |
|---|---|---|---|
| 19 | `plan.md` (spec-relative) | quickstart.md:13 | `.specify/archive/specs/003-speckit-agents-command/plan.md` |
| 20 | `data-model.md` (spec-relative) | quickstart.md:14 | `.specify/archive/specs/003-speckit-agents-command/data-model.md` |
| 21 | `contracts/agents-command.openapi.yaml` (spec-relative) | quickstart.md:15 | `.specify/archive/specs/003-speckit-agents-command/contracts/agents-command.openapi.yaml` |

### Dead (9)

| # | Reference | Anchors | Now resolves to |
|---|---|---|---|
| 22 | `.specify/specs/003-speckit-agents-command/` | plan.md:81,114; tasks.md:101 | missing; dir preserved at `.specify/archive/specs/003-speckit-agents-command/` |
| 23 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/003-speckit-agents-command/` (absolute dir) | tasks.md:3 | missing; same archive dir |
| 24 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/003-speckit-agents-command/requirements.md` (absolute) | plan.md:3,4; quickstart.md:11 | missing; copy at `.specify/archive/specs/003-speckit-agents-command/requirements.md` |
| 25 | `.specify/specs/003-speckit-agents-command/requirements.md` | tasks.md:98; checklists/requirements.md:5 (link) | missing; same archive copy |
| 26 | `.specify/specs/003-speckit-agents-command/contracts/agents-command.openapi.yaml` | tasks.md:29,47,66,86 | missing; copy at archive `contracts/agents-command.openapi.yaml` |
| 27 | `.specify/specs/003-speckit-agents-command/quickstart.md` | tasks.md:48,49,68,87,88 | missing; copy at archive `quickstart.md` |
| 28 | `.specify/specs/003-speckit-agents-command/data-model.md` | tasks.md:67 | missing; copy at archive `data-model.md` |
| 29 | `research.md` | plan.md:53 ("not present"), plan.md:83 (optional tree) | missing; never created — plan.md:53 itself declares the absence |
| 30 | `.github/agents/python-code-reviewer.agent.md` | quickstart.md:109 | missing; was an unexecuted manual-test expectation (all quickstart statuses still read "Ready for implementation") |

## Broken list

Each item in `path:line -> what it now resolves to (or the missing symbol)` form. Archive-relative
paths are under `.specify/archive/specs/003-speckit-agents-command/`.

1. `plan.md:3` -> `/storage/.../.specify/specs/003-speckit-agents-command/requirements.md` does not exist; now `.specify/archive/specs/003-speckit-agents-command/requirements.md`
2. `plan.md:4` -> same missing absolute requirements path
3. `plan.md:81` -> `.specify/specs/003-speckit-agents-command/` does not exist; now the archive dir
4. `plan.md:83` -> `research.md` (optional Phase 0 output) missing; never created
5. `plan.md:114` -> `.specify/specs/003-speckit-agents-command/` (Documentation tree) does not exist; now the archive dir
6. `tasks.md:3` -> absolute pre-archive spec dir missing; now the archive dir
7. `tasks.md:29,47,66,86` -> `.specify/specs/003-.../contracts/agents-command.openapi.yaml` missing; copy at archive `contracts/agents-command.openapi.yaml`
8. `tasks.md:48,49,68,87,88` -> `.specify/specs/003-.../quickstart.md` missing; copy at archive `quickstart.md`
9. `tasks.md:67` -> `.specify/specs/003-.../data-model.md` missing; copy at archive `data-model.md`
10. `tasks.md:98` -> `.specify/specs/003-.../requirements.md` missing; copy at archive `requirements.md`
11. `tasks.md:101` -> `.specify/specs/003-speckit-agents-command/` does not exist; now the archive dir
12. `quickstart.md:11` -> absolute pre-archive requirements path missing; now the archive copy
13. `checklists/requirements.md:5` -> link target `.specify/specs/003-.../requirements.md` missing; now `.specify/archive/specs/003-speckit-agents-command/requirements.md`
14. `quickstart.md:109` -> `.github/agents/python-code-reviewer.agent.md` missing (no such file anywhere in the tree)
15. `requirements.md:71 (FR-001)` -> current implementation writes `.specify/agents/{templates,instances}/<name>.agent.md` (`templates/commands/agents.md:32`); `.github/agents/<slug>.agent.md` is only a rendered real-file surface (`docs/reference/commands/agents.md:94-98`)
16. `requirements.md:80 (FR-010)` -> current template states "an existing definition is never silently overwritten (reuse-first / refine instead)" (`templates/commands/agents.md:32`) — the opposite of the claimed same-name overwrite
17. `requirements.md:79 (FR-009)` -> no provider whitelist in the current command template; `AGENT_CONFIG` supports claude, copilot, hermes, opencode, qoder, codex (`src/specify_cli/__init__.py:64`) — Qwen Code is not among them
18. `requirements.md:83 (FR-013)` -> auto-create `.github/agents/` is no longer the write path (same canonical-store drift as item 15)

Items 15–18 are superseded behaviour, not lost artifacts: the supersession is recorded in the ledger
target itself (`features/019.md:32` — Feature 014 moved the canonical directory to `.specify/agents/`;
`features.md:28` — Feature 023 redesign).

## Ledger-target check

Ledger row (`.specify/archive/specs/CONSOLIDATION-LEDGER.md:10`):
`003-speckit-agents-command | archive | Feature 019 (spec dir bound by reference, not by its prefix) |
numbering-collision entry; see review-G1`.

- **Archive executed**: `.specify/specs/003-speckit-agents-command/` is absent from the live tree;
  all 7 artifacts (+ `contracts/`, `checklists/`) exist under `.specify/archive/specs/003-speckit-agents-command/`;
  git tracks only the archive copies.
- **Target feature resolves**: `.specify/memory/features/019.md` exists (Status: Implemented); registry
  row `.specify/memory/features.md:28` exists and points to that detail file; the row's spec column points
  to `.specify/specs/023-agent-framework-redesign/requirements.md` (alive) — consistent with 003 being
  bound only by reference.
- **"Bound by reference" holds partially**: `features/019.md:17,27` reference the archived path correctly;
  but `features/019.md:84-89` (Related Specifications block) still carries 6 dead pre-archive paths
  (`.specify/specs/003-speckit-agents-command/...`).
- **Minor**: the note's anchor `review-G1` is findable only in `.specify/history/.work/2e79c944-...txt`,
  not in a surfaced review document.

Conclusion: the ledger row's verdict and target are accurate; the target's own reference block is stale.

## Missing guards

- The 003 artifacts name **no executable contract test or guard file**. The only test surface is the
  manual quickstart (7 checks, all still "Ready for implementation" — never recorded as executed).
- The contract artifact `contracts/agents-command.openapi.yaml` survives in the archive but is referenced
  by no test: `grep -r agents-command tests/` finds only the scenario directory below.
- Nearest live guard for this command: `tests/scenarios/agents-command/single-entry-routing-scenario.md`
  **exists**, but its contract link is **dead** — `:4` points at
  `.specify/specs/.archive/023-agent-framework-redesign/contracts/agents-command-contract.md`; the actual
  file is `.specify/specs/023-agent-framework-redesign/contracts/agents-command-contract.md`.
- So: 0 named guards missing; 1 existing adjacent guard with a dead contract link.

## Three spot-checks (implementation claims vs current tree)

1. **File** — `templates/commands/agents.md` (plan.md:104; tasks.md:14,46,137): **EXISTS** (git-tracked).
   Content check: it is now a delegating router (create → `.specify/skills/internal/create-agent/SKILL.md`,
   run → `run-agent`, refine → `improve-agent`; router lines 31–33), so the file claim holds but the
   authoring rules the spec placed in it have moved into internal skills.
2. **Symbol/command** — `/speckit.agents`: **EXISTS**. Host prompt `.github/prompts/speckit.agents.prompt.md`
   exists; `docs/reference/commands/agents.md` exists; CLI symbols `render_agents`
   (`src/specify_cli/__init__.py:3353`) and `render_agents_for_tool` (`:638`) exist.
3. **Behaviour surface** — **FAILS**. FR-001/FR-009/FR-010/FR-013 no longer describe the implementation:
   canonical store is `.specify/agents/{templates,instances}/`, `.github/agents/` is render output,
   existing definitions are not silently overwritten, and no provider whitelist exists (details in
   Broken items 15–18). This is recorded supersession (Feature 014 per `features/019.md:32`, Feature 023
   per `features.md:28`), not an unexplained regression.

## Anchor-layout rename (pending branch `rename-anchors` @ 8b9030371)

Audited on the current tree (`master`). References that will move:

| Reference | Anchor(s) | New path on the branch |
|---|---|---|
| `.specify/memory/constitution.md` | plan.md:53 | `.specify/constitution.md` |
| `.specify/memory/features.md` | plan.md:53; tasks.md:100 | `.specify/features.md` |
| `.specify/memory/features/001..019.md` | plan.md:53 | `.specify/features/<NNN>-<slug>.md` |
| `.specify/memory/features/019.md` | plan.md:113; tasks.md:99 | `.specify/features/019-agents-command.md` |
| `.specify/memory/**` | plan.md:22 | partial: the five anchors leave `memory/`; session/knowledge/feedback stores stay |

The ledger target's stale block (`features/019.md:84-89`) will break further on that branch.

## Anomaly

**Anomaly**: live guard `tests/scenarios/agents-command/single-entry-routing-scenario.md:4` links to a non-existent `.specify/specs/.archive/023-agent-framework-redesign/contracts/agents-command-contract.md` (actual: `.specify/specs/023-agent-framework-redesign/contracts/agents-command-contract.md`), and ledger-target detail `.specify/memory/features/019.md:84-89` still carries dead pre-archive paths.

## Verdict

**BROKEN** — the spec is fully preserved (no artifact lost) and 21 of 30 references resolve (18 alive,
3 archived-elsewhere), but 9 references are dead at their stated paths (7 stale pre-archive forms,
2 no-target-anywhere), one named-behaviour spot-check (FR-001/FR-009/FR-010/FR-013) contradicts the
current implementation, and the adjacent guard file carries a dead contract link. The ledger row itself
resolves accurately; its target detail file needs its reference block repointed to the archive.

SPEC-AUDIT-1-DONE
