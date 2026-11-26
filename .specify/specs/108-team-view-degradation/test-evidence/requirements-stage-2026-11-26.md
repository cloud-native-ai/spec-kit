# Requirements Stage Evidence — 2026-11-26

Line `team-view-degradation`; run `r20261126T071500Z-108a`; stage `requirements`; baseline `54c6efa8c`; branch `108-team-view-degradation` (worktree).

## Scaffold

- `create-new-requirements.sh` derives the next number from spec dirs, `.archive/`, and local/remote branch names in `<NNN>-<slug>` form. The current local branch `108-team-view-degradation` is itself counted, so the script would derive **109** and run `git checkout -b 109-…`, switching the worktree off the line branch.
- Per brief and 107 precedent: manual scaffold from `.specify/templates/requirements-template.md` into `.specify/specs/108-team-view-degradation/requirements.md`, staying on branch 108; the script's template-copy step replicated, only its branch-creation step skipped. Recorded as A-16 in the spec.

## Probes (reproduced against a scratch fixture under `.specify/.tmp/sdd-loop/tmp/team-view-degradation/`)

1. **Stale-latest selection**: a fixture with `20261124T074500Z-report.md` (conforming) plus newer `20261125T121924Z-93cc-stage.md` and `2026-11-25T140000Z-report.md` (non-conforming) renders `运行报告: 已列出（共 N 份…）` from the conforming set only; the non-conforming newer reports land in `未识别（unrecognized）` and can never become latest (`team-view.py` lines 925–941 select from `recognized` only).
2. **Degraded definition**: a fixture with no `binding` block, inline `goal`, a matrix without `agent` column, and missing `items.jsonl` / spine files renders: `绑定（binding）: 不可读（binding-missing: … carries no binding block; …）`, `其它声明键: goal（不可读）`, `名册差异（roster_delta）: 未记录（正文矩阵无 agent 列，两侧名册不可比对）`, missing states for the ledger/spine, exit code **5**.
3. **Partial binding**: `goal-utils.py binding team <slug> --json` returns exit 2 with `binding-missing: … is missing the binding key(s) owner_id, origin; exactly owner / owner_id / origin are required` — the engine already names missing keys; the view only needs to preserve and render that precision plus the repair path.
4. **Live corpus (2026-11-26, baseline `54c6efa8c`)**: `.specify/teams/*/runs/` holds 46 files: 28 conforming to `^\d{8}T\d{6}Z-report\.md$`; 18 non-conforming, of which 16 carry a parseable leading UTC stamp (13 report-style: ISO-dashed `2026-09-17T072239Z-report.md`, fully dashed `2026-08-07T18-30-00Z-report.md`, hour-minute `20261014T1710Z-report.md`; 3 auxiliary: `-verification.md` ×2, `-seat-result.md` ×1) and 2 carry no parseable stamp (`2026-10-07-progress-snapshot.md`, `2026-10-06-S1-judgment-contract.md`).
5. **Live misreporting**: `team-view.py viz-skill-arena` (5 reports, all non-conforming) prints `运行报告: 为空`, `最近报告（latest_report）: 未记录`, and exits **0**; same shape for `draw-two-layer-structure` (7) and `draw-diagram-interactive` (1). This is the in-repo reproduction of the production "latest is not the true latest / history invisible" class.

Scratch fixtures were removed after the probes; nothing under `.specify/teams/` was created or modified.

## Deterministic gates (verbatim outputs)

- `validate-requirements.py .specify/specs/108-team-view-degradation/requirements.md` → exit 0, `status: ok`, 0 errors / 0 warnings, 228 lines, 33 definition rows, 3 shared strings → `test-evidence/requirements-validator.txt`.
- `pre-analyze-check.py --spec-dir .specify/specs/108-team-view-degradation --stage requirements --repo .` → `decision=pass errors=0 advisories=0`, `fr=25 sc=8` → `test-evidence/pre-analyze-requirements.json`.
- `decomposition-check.py --mode plan --requirements .specify/specs/108-team-view-degradation/requirements.md` → `decision=proceed`, `fr_count=25`, `fr_ceiling=120` → `test-evidence/decomposition-requirements.json`.

## Workspace guard (attempt 1 — superseded by attempt 2, disclosed)

- Snapshot taken before authoring: `.specify/.tmp/sdd-loop/tmp/team-view-degradation/workspace-guard-requirements.json`; **no check was recorded at attempt-1 wrap-up and the signature was not persisted into `test-evidence/`**. Attempt 2 remedied this and compared the attempt-1 snapshot against the repair-start state (`clean`, rc 0) — see below.

## Concurrency

- `requested=1`, `effective=not_evaluated`, `effective_reason=single-unit` — one bounded assignment, no independent units to parallelize.

## Repair attempt 2 (2026-11-26T07:25Z)

Attempt 1 ended `REQUIREMENTS-DONE` with a false-completion signature: the spec directory was left untracked, no workspace signature was persisted into `test-evidence/`, and no stage wrap-up records (run determination / exec-quant / feedback / close-out receipt) were written. This repair closes exactly those three gaps; the requirements content is unchanged (no validator error demanded any edit).

- **Workspace signature (post-stage reading; disclosure)**: attempt 1 persisted no signature and recorded no wrap-up check. Attempt 2 wrote `test-evidence/workspace-requirements.json` at 2026-11-26T07:25:10Z and self-checked it immediately: `clean`, rc 0. The attempt-1 unpersisted pre-authoring snapshot (`.specify/.tmp/sdd-loop/tmp/team-view-degradation/workspace-guard-requirements.json`, taken 2026-11-26T07:19Z) also compares against the repair-start state as `clean` (rc 0): branch `108-team-view-degradation`, all 213 refs and the `.specify/specs` listing (including `108-team-view-degradation`) are identical, so the stage created no branch and no spec directory beyond the one it owns. Readings: `test-evidence/workspace-requirements-readings.txt`. The post-artifact-commit signature is `test-evidence/workspace-requirements-postcommit.json` with its own check in `test-evidence/workspace-requirements-postcommit.txt`; its `refs` differ from the pre-commit reading only by this line's own stage commit.
- **Stage commit**: carries the requirements spec, the quality checklist and `test-evidence/` (including this record and the signature).
- **Records**: stage wrap-up for `/speckit.requirements`, run `r20261126T071500Z-108a` — run determination, exec-quant, feedback entry (with threshold notice and token reflection) — plus a stamp-named close-out receipt under `.specify/retention/closeout/` matching `*r20261126T071500Z-108a-requirements.md`; all ride one records commit that follows the stage commit.
- **Post-commit gates**: `validate-requirements.py` (0 error / 0 warning) and `pre-analyze-check.py --stage requirements` (pass) re-run against the committed state; readings in `test-evidence/requirements-validator-postcommit.txt` and `test-evidence/pre-analyze-requirements-postcommit.json`, carried by the records commit.
- **No content change, no push, no spine/registry edit, no Feature status transition** (`Related Feature` stays `Need clarification`; feature 108 unregistered, so the wrap-up records carry the requirement key only, no `--feature-id`).
