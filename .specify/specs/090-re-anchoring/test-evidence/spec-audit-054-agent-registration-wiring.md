# Spec Audit — 054-agent-registration-wiring (batch 7)

**Date**: 2026-11-10 · **Tree**: `master` @ `564a5f5a6` (read-only audit — no spec/source modified)
**Audited spec**: `.specify/archive/specs/054-agent-registration-wiring/`
**Tree state**: current tree as-is; the `rename-anchors` branch (worktree at `.specify/.tmp/sdd-loop/worktrees/rename-anchors`) is **not** applied — see § Rename-pending references.

## 1. Scope & method

Artifacts audited (16 files): `requirements.md`, `plan.md`, `tasks.md`, `data-model.md`, `verification.md`, `quickstart.md`, `feature-ref.md`, `review.md`, `contracts/` ×4, `notes/` ×3, `checklists/requirements.md`.

Extraction: repo-anchored path tokens (`.specify/ scripts/ skills/ templates/ shared/ docs/ tests/ src/`), dot-tool directories (`.qoder/ .claude/ .github/ .opencode/ .hermes/`), bare `test_*.py` names and `features/*.md`; occurrences via `grep -r`, distinct targets via normalized path. Classification per instruction: **alive** = target exists now; **archived-elsewhere** = resolves inside this archive; **dead** = no target (stale pre-archive `.specify/specs/054-…` counts dead).

## 2. Counts

| Class | Distinct targets | Occurrences |
|---|---|---|
| alive | 90 | 352 |
| archived-elsewhere (spec's own sibling artifacts) | 16 | ~20 |
| dead | 11 | 27 |
| **Total** | **117** | **≈379** (2 prose false-positive tokens excluded) |

Dead breakdown (27 occurrences): pre-archive spec-dir paths 16 · pre-`internal/` skill-layout paths 10 · removed feedback index 1.

## 3. Broken list

### 3.1 Dead references inside the archived artifacts

Pre-archive path form `.specify/specs/054-agent-registration-wiring/…` (target now only at `.specify/archive/specs/054-agent-registration-wiring/…`):

| Ref | Now resolves to |
|---|---|
| `plan.md:5` → `.specify/specs/054-…/requirements.md` | missing; actual `archive/specs/054-…/requirements.md` |
| `plan.md:78` → `.specify/specs/054-…/` | missing (archive path exists) |
| `tasks.md:6` → `.specify/specs/054-…/` | missing (archive path exists) |
| `tasks.md:15` → `.specify/specs/054-…/requirements.md` | missing (archive path exists) |
| `tasks.md:26` → `.specify/specs/054-…/baseline-failed.txt` (GATE-1 command) | missing; file exists only in archive |
| `tasks.md:28` → `.specify/specs/054-…/tasks.md` (GATE-3 command) | missing; file exists only in archive |
| `tasks.md:29` → `.specify/specs/054-…/verification.md` (GATE-4 command) | missing; file exists only in archive |
| `tasks.md:56` → `.specify/specs/054-…/notes/` (T001) | missing; archive `notes/` exists |
| `tasks.md:57` → `.specify/specs/054-…/baseline-failed.txt` (T002) | missing; archive copy exists |
| `feature-ref.md:3` → `.specify/specs/054-…/requirements.md` | missing; archive path exists |
| `review.md:17,30,58,65,79` → absolute `.specify/specs/054-…/…` | missing (dated 2026-10-08 citations; `git show d58a600e:<path>` still valid historically) |
| `notes/pre-change-measurements.md:7` → `.specify/specs/054-…/baseline-failed.txt` | missing; archive copy exists |

Pre-`internal/` skill layout (`skills/create-agent/…`, now `skills/internal/create-agent/…`):

| Ref | Now resolves to |
|---|---|
| `quickstart.md:42` → `skills/create-agent/` | missing → `skills/internal/create-agent/` |
| `review.md:93` → `skills/create-agent/SKILL.md:108` | missing → `skills/internal/create-agent/SKILL.md` (F6's line-108 dialect text is gone) |
| `notes/quickstart-run.md:15,17,24,25,29,30` → `skills/create-agent/SKILL.md` | missing → `skills/internal/create-agent/SKILL.md` |
| `notes/quickstart-run.md:26,31` → `.specify/skills/create-agent/SKILL.md` | missing → `.specify/skills/internal/create-agent/SKILL.md` |

Removed store:

| Ref | Now resolves to |
|---|---|
| `review.md:134` → `.specify/memory/feedback/index.json` | missing — the feedback store is per-entry files; no `index.json` |

### 3.2 Archive-move side effects in the LIVE tree (most consequential)

The move was not swept through the files that point at the spec:

| Ref | Now resolves to |
|---|---|
| `.specify/memory/features/044.md:56` — "Bound requirement (continuation)" | dead `.specify/specs/054-…/requirements.md`; the same file's `:72` correctly uses the archive path (self-inconsistent) |
| `.specify/agents/instances/dogfood-executor.agent.md:35` | dead `.specify/specs/054-…/requirements.md` (the 054 SC-002 demo seat) |
| `.qoder/agents/dogfood-executor.agent.md:31` | same dead path (rendered copy) |
| `.claude/agents/dogfood-executor.md:29` | same dead path (rendered copy) |
| `.github/agents/dogfood-executor.agent.md:31` | same dead path (rendered copy) |
| `.opencode/agents/dogfood-executor.md:29` | same dead path (rendered copy) |

### 3.3 Line-anchor drift (paths alive, cited anchors moved)

| Spec anchor | Now resolves to |
|---|---|
| `src/specify_cli/__init__.py:310` (load_project_agent_definitions) | `:327` |
| `src/specify_cli/__init__.py:615` (render_agents_for_tool) | `:638` |
| `src/specify_cli/__init__.py:2283` (init call site) | `:2599` (init) / `:3376` (render-agents) |
| `src/specify_cli/__init__.py:2653` (init) / `:2993` (check) | `:2970` / `:3309`–`:3310`; `render_agents` at `:3353` |
| `src/specify_cli/__init__.py:119-148` (key set) | `:119-154`; `role-scope` `:139` → `:147`, `team-scope` → `:149` |
| `src/specify_cli/__init__.py:151-164` (Qoder dialect keys) / review `:154-167` | `:168-182` (`FORBIDDEN_AGENT_METADATA_KEYS`) |
| `:273-279` (unknown-key reject) / `:296-307` (placeholder reject) | `:290-295` / `:313-324` |
| `src/specify_cli/__init__.py:544` (manifest) | `:567` (`_AGENT_MANIFEST_NAME`) |
| `templates/commands/agents.md:25` (STR-001) | literal absent (pass); `:25` now delegation prose |
| `templates/commands/agents.md:72` (capacity dispatch claim) | file is 43 lines; claim now at `skills/internal/run-agent/SKILL.md:87` |
| `templates/commands/team.md:45,52` (modify route) | modify route now `:43` (and capability row `:68`); `:45`/`:52` are other list items |
| `skills/internal/create-agent/SKILL.md:122/:127` (retired teaching) | corrected text now `:142`/`:147`; `:52-53` → `:52-54`, `:111` → `:114` |
| `skills/internal/create-team/SKILL.md:27-32` (6-step flow) | 7-step flow now `:41-48` |
| `skills/internal/create-team/references/create-mode.md:128` (schema note) | moved/extended to `:157` |
| `test_fast_fail_discipline.py:795-814` (drill precedent) | content moved (file evolved; A14 block at `:843`) |

Additional behaviour-surface drift (not a missing file): FR-001's literal subject `templates/commands/agents.md` no longer teaches the render model — a later "S3 command thinning" moved that teaching to `skills/internal/create-agent/SKILL.md`, and `tests/contract/test_teaching_surfaces.py:71-76` was deliberately re-pointed to the skill with that comment. The guard follows the content; the archived FR-001 wording no longer matches its named surface.

## 4. Ledger-target check (`.specify/archive/specs/CONSOLIDATION-LEDGER.md`)

Row (line 23): `| 054-agent-registration-wiring | merge | 040-agent-metadata-portability (Feature 044 child) | review-G2 |`

| Check | Result |
|---|---|
| Target spec dir `.specify/specs/040-agent-metadata-portability/` | **resolves** (alive, `requirements.md` present, Status Draft) |
| Target feature lineage "Feature 044 child" | **resolves** — `.specify/memory/features/044.md:71-72` binds spec 040 and spec 054; `Last Updated` records the 054 implementation |
| Registry row 044 (`.specify/memory/features.md`) | **resolves** (row 044 present) |
| Ledger row accurate? | **NO** — see below |

Ledger defects:
1. **Row is outside the table.** Line 23 sits after the blank line and the two prose lines (21 `Deferred:`, 22 `Not executed:`); it will not render as part of the table and is easy to miss.
2. **Verdict/state mismatch.** Verdict says `merge`, but the spec directory was moved whole into `.specify/archive/specs/` and carries no merge note (contrast 092's "absorbed into 090-re-anchoring (merge note § W3)"); `.specify/specs/040-agent-metadata-portability/` contains zero mentions of 054.
3. **Target label conflates namespaces.** `040-agent-metadata-portability` is a spec-dir slug under Feature 044; read as a Feature ID, registry row 040 is **Token Efficiency Discipline** — a different feature. The label should say "spec 040 (Feature 044)".
4. **`review-G2` is unregistered.** `.specify/memory/register.md` has no `review-G*` entry; the cited authority is unresolvable.
5. **Target feature's own detail file is stale.** `.specify/memory/features/044.md:56` points at the pre-archive path while `:72` uses the archive path (see § 3.2).

## 5. Missing guard files

**None.** All five contract-test files named by the spec exist and carry their guard functions:

| Guard file | Status |
|---|---|
| `tests/contract/test_render_trigger_cli.py` | alive (9 collected; C-1..C-5 + seat C-1/C-2) |
| `tests/contract/test_teaching_surfaces.py` | alive (11 collected via parametrization; C-1..C-4 + seat C-3) |
| `tests/contract/test_seat_instantiation_flow.py` | alive (6; C-4..C-9 + modify-backfill C-1/C-2/C-8) |
| `tests/contract/test_agent_surface_docs.py` | alive (5; C-5..C-8) |
| `tests/contract/test_agent_chain_guards.py` | alive (4; C-9/C-10) |

Suite arithmetic still 9+11+6+5+4 = **35**. Precedent guards named in the plan also alive: `test_shipped_surface_client_neutrality.py` (`BANNED_PATTERNS`:30, `KNOWN_DEBT`:37), `test_fast_fail_discipline.py`, `test_team_command_routing.py` (modify→improve-team assertion at `:107`).

## 6. Three implementation spot-checks

| # | Spec claim | Current-tree evidence | Verdict |
|---|---|---|---|
| 1 | Narrow CLI trigger `specify render-agents --ai <tool>` delegating to the existing renderer, `--ai` required, annotated/unknown tools rejected with legal values | `src/specify_cli/__init__.py:3353` `def render_agents`; `:3376` delegates `render_agents_for_tool` (`:638`); non-render tools raise `BadParameter` listing legal values at `:3365-3372` | **HOLDS** (anchor drift only) |
| 2 | `team-scope` is a framework-only neutral key, accepted by the validator, never rendered | `src/specify_cli/__init__.py:149` `"team-scope": (None, None, False)`; framework key set `:162`; not in `_AGENT_METADATA_MAPPING` render fields; guard `test_seat_c1_team_scope_not_rendered` (`tests/contract/test_render_trigger_cli.py:135`) | **HOLDS** |
| 3 | "Host Registration Surface" defined in its owner doc; Qoder IDE/CLI shared-path documented with provenance; create-team instantiates + triggers rendering | `shared/definitions/agent-definitions.md:98` owner section + Seat Instance taxonomy `:102`; `shared/workflow/symlink-model.md:11` and `docs/reference/cli/supported-agent-tools.md:37` (both provenance URLs + 2026-10-08); `skills/internal/create-team/SKILL.md:44,48`; schema note `references/create-mode.md:157` | **HOLDS** |

## 7. Rename-pending references (will move)

`rename-anchors` worktree already carries `.specify/features/`, `.specify/features.md`, `.specify/constitution.md`, `.specify/anchoring/`, `.specify/history/`; `memory/` retains only working stores (feedback, todo, tools, session, …). Refs in this spec that will move:

| Current ref | Will become |
|---|---|
| `.specify/memory/features/044.md` (`feature-ref.md:4`) | `.specify/features/044.md` |
| `features/044.md`, `features.md` (`feature-ref.md:30-31`, `tasks.md:157`) | `.specify/features/044.md`, `.specify/features.md` |
| `.specify/memory/constitution.md` (`plan.md:35`) | `.specify/constitution.md` |
| `.specify/memory/feedback/backlog.md` (`requirements.md:6`) | unchanged (stays under `.specify/memory/feedback/`) |

## 8. Verdict

**BROKEN** — counts: 117 distinct reference targets (90 alive / 16 archived-elsewhere / 11 dead; 27 dead occurrences in-artifact), plus 6 archive-move side effects in the live tree, plus an inaccurate ledger row.

Highest-impact repairs (not performed — read-only audit):
1. Sweep `.specify/memory/features/044.md:56` and the dogfood-executor seat instance + 4 rendered copies to the archive path.
2. Move/renumber the 054 ledger row into the table, change `merge` → `archive` (or add a merge note), relabel the target as "spec 040 (Feature 044)", and register `review-G2`.
3. Replace pre-archive + pre-`internal/` paths in the archived artifacts if they are expected to be re-run (GATE commands in `tasks.md` will fail as written).

**Anomaly**: the archive move left live references pointing at the dead pre-archive path — `.specify/memory/features/044.md:56` and the `dogfood-executor` seat definition (1 instance + 4 rendered copies) — and the ledger row that authorized the move is malformed (outside the table) with an unregistered `review-G2` citation; no anomalies were repaired in this read-only pass.

SPEC-AUDIT-7-DONE
