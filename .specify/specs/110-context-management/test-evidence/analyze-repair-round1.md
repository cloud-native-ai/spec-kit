# Analyze Repair — Round 1 (AN-01, AN-04)

**Line**: `context-management` · **Run**: `r20261127T070000Z-110a` · **Stage**: analyze-repair · **Baseline**: `5fbe83302`
**Trigger**: analyze round 1 BLOCKED with 2 HIGH findings (`analyze-round1-findings.jsonl` / `analyze-round1-report.md`).
**Scope**: exactly AN-01 and AN-04; no contract weakened — both causes repaired at their owner surfaces.

## Findings Resolved

- **AN-01 (HIGH)** — resolved: `task-switch` and `stage-boundary` now name **the composer of the current work** (same holder resolution as `task-entry`), so all seven triggers carry composer, scope and evidence; FR-014/C-022/E-7/T028 (and FR-015/C-023/E-8 for the role resolution) agree.
- **AN-04 (HIGH)** — resolved: the no-content-read prohibition is now scoped to **audited sources** (the project context materials a layout row declares); the declaration layer (owner document layout table + four facts) and the `--version` identity source are declared as the engine's only content-read inputs (FR-021), so FR-021/C-012/C-032 no longer contradict FR-022/FR-024/C-034/C-035.

## Adjudications (recorded in requirements.md Assumptions)

| ID | Adjudication | Basis |
|----|--------------|-------|
| **A-18** | Task-scope triggers (`task-switch`, `stage-boundary`) share `task-entry`'s composer: **the composer of the current work** = whichever existing role holds the work item (session or superagent), a holder resolution — not a new role value, depth rule or grant. | Source 093 owner document (`shared/definitions/context-management-definitions.md`) Triggers table + Composer Roles section names exactly this composer in its final form; FR-015's "no new role value" stays intact. |
| **A-19** | The content-read boundary binds **audited sources only**. The engine's content reads are exactly FR-021's declared inputs: the owner document layout table, the four declaration facts (via `declaration_reader`), and the `--version` run-time identity source (nearest `pyproject.toml` via the house helper, C-031). Audited sources remain metadata-only. | Source 093 FR-024 prohibits only raw user text / conversation content; the engine must parse the owner document and facts. Privacy and read-only containment are not weakened — the scope is made decidable. |

## AN-01 — Finding → Resolution → Files Changed

| Locus | Before | After |
|-------|--------|-------|
| `requirements.md` FR-014 | `task-switch` / `stage-boundary` named no composer | both name **当前工作的组合者**; `reentry` composer clarified as 被恢复的会话 |
| `requirements.md` FR-015 | roles = root session / superagent / dispatched executor | adds the current-work composer as a holder resolution; root session acts as the resumed session at `reentry` |
| `requirements.md` US4 描述 / Key Entities | parenthetical and entity list named only two/three roles | task layer composer added to both |
| `requirements.md` A-18 | — | adjudication row added |
| `contracts/matrix-and-triggers.contract.md` C-022 | `task-switch` / `stage-boundary` had no composer | both name **the composer of the current work**; `reentry` names the resumed session in the root-session role |
| `contracts/matrix-and-triggers.contract.md` C-023 | three roles only | adds the current-work composer (holder resolution, no new role value) |
| `data-model.md` E-7 composer row | "root session for baseline-scope triggers; superagent for dispatch edges" | per-trigger mapping covering all seven, including the current-work composer and the resumed session |
| `data-model.md` E-8 | three role rows | adds "the composer of the current work" row |
| `tasks.md` T028 | role enumeration lacked the task-scope composer | enumeration now includes it (T028's "each naming composer, scope and evidence" is now satisfiable from FR-014) |

## AN-04 — Finding → Resolution → Files Changed

| Locus | Before | After |
|-------|--------|-------|
| `requirements.md` FR-021 | required reads stated without declaring them the exemption | adds the declared-input note (owner layout table, four facts, `--version` identity source) |
| `requirements.md` FR-022 | "MUST NOT 读取文档内容" (unscoped) | content reads limited to FR-021's three declared inputs; audited sources MUST NOT be read |
| `requirements.md` FR-024 | "不打开任何文件内容" (unscoped) | audited sources are metadata-only; FR-021 declared inputs are the only content-read surface |
| `requirements.md` Edge Case (path escape) | "不打开任何文件内容" | scoped to audited sources; content reads limited to FR-021 declared inputs |
| `requirements.md` FR-020 (presence) | "绝不打开文件内容" | "绝不打开来源内容（内容读取仅限 FR-021 的声明输入）" |
| `requirements.md` A-12 / A-19 | blanket privacy phrasing / — | A-12 scoped; A-19 adjudication row added |
| `contracts/engine-and-distribution.contract.md` C-032 | parse statement without exemption note | declares the two reads as declared inputs; layout-row sources remain metadata-only |
| `contracts/engine-and-distribution.contract.md` C-034 | "no content reading" (unscoped) | "no content reading of audited sources" + declared inputs allowlist; Red-when scoped |
| `contracts/engine-and-distribution.contract.md` C-035 | "consumes paths, metadata and presence states only" | "only audited sources' …" + declared inputs allowlist; Red-when scoped |
| `contracts/declarations-and-domains.contract.md` C-012 | four-fact read without boundary note | declares owner document + four facts as declared input reads; no-content boundary binds audited sources |
| `data-model.md` E-11 / I-11 | "never opens a file's content" / unscoped consumption | scoped to declared sources / audited sources; declared inputs named |
| `plan.md` PA-1 / T-002 (title, decision, pole_a) | blanket no-content wording | scoped to audited sources with the declared-input allowlist (A-19) |

**Left untouched by design**: `checklists/context-model-2026-11-27.md` (its own note: findings from answering an item belong in the analyze report, not in the checklist); FR-016/C-024 (already scoped to declared sources and their metadata digest).

## Verification Gates (re-run after repair)

| Gate | Command | Verdict | Evidence |
|------|---------|---------|----------|
| Requirements validator | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/110-context-management/requirements.md` | `status: ok` — 0 error / 0 warning; 289 lines, 40 definition rows | `test-evidence/analyze-repair-requirements-validator.txt` |
| Pre-analyze (tasks) | `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/110-context-management --stage tasks --repo .` | `decision=pass errors=0 advisories=159 waived=0` (all advisory: missing-path for planned files, external-clause) | `test-evidence/analyze-repair-pre-analyze-tasks.txt` / `pre-analyze-tasks.json` |
| Tasks validator | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/110-context-management/tasks.md` | `PASS — 0 error(s), 0 warning(s)` | `test-evidence/analyze-repair-tasks-validator.txt` |
| Workspace guard | `python3 .specify/scripts/python/workspace-guard.py --check .specify/specs/110-context-management/test-evidence/workspace-analyze-repair.json --repo .` | `clean` rc=0 | `test-evidence/analyze-repair-workspace-check.txt` |

## Anomalies

未发现异常 — no in-passing repairs were needed beyond the two findings; the known other-run session record (`.specify/session/20261125T140702Z-…-clarify-artifact-…md`, **M**) is attributed and left untouched (never committed, never reverted).