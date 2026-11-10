# Plan-stage evidence — 095-superagent-role（2026-11-10）

Single-run captures from the plan stage. Commands were run from repo root on this tree; readings are copied, not recomputed.

## Environment readings

| Reading | Command | Result |
|---------|---------|--------|
| Interpreter | `python3 --version` | `Python 3.11.11` |
| Requires-python | `pyproject.toml:5` | `requires-python = ">=3.8"` |
| Live instructions size | `wc -c .specify/instructions.md` | `37454` B |
| Template size | `wc -c templates/instructions-template.md` | `32975` B |
| Budget literal | `scripts/bash/generate-instructions.sh:107` | `INSTRUCTIONS_BUDGET_BYTES=38400` → headroom 946 B |
| Engine path absence | `ls scripts/python/role-edge-check.py` | no such file (path free) |
| Mirror-drift baseline | `python3 scripts/python/sync-mirrors.py --check` (DIFF/ORPHAN lines) | `428` |
| Dirty mirrors baseline | `git status --porcelain .specify/shared/` | `100` modified files — pre-existing path-prefix rewrite (`shared/` → `.specify/shared/`), unrelated to this feature |
| Team run report sample | `ls .specify/teams/skill-layer-install-separation/runs/` | three `*-report.md` files |
| Artifact-triplet root | `ls -d .specify/agents/execution/logs` | exists |
| Line-registry store | `ls ~/.local/state/spec-kit/lines` | `*.json` entries present |

## Digest capture (before the role view exists)

Command: `python3 .specify/scripts/python/status-digest.py --action digest` (exit 0)

Header: `状态摘要 · 生成于 2026-11-10T06:32:25.703029Z（UTC）· 最多 20 条 · 静默阈值 15 分钟 · long-run · 注册目录 /home/agent/.local/state/spec-kit/lines`

Columns: 线路 / 状态 / 阶段 / 已静默 / 标记 / 最近步骤与消耗. Rows included `095-superagent-role` (活跃, 已静默 32m34s) and closed lines. Used as the pre-change baseline for `contracts/status-digest-role-view.contract.md`.

## Gate readings

| Gate | Command | Result |
|------|---------|--------|
| Flow class | `python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:095-superagent-role"` | `flow_class: execution`, `source: declaration`, exit 0 |
| Decision tensions | `python3 .specify/scripts/python/validate-decision-tensions.py --spec .specify/specs/095-superagent-role` | first run: 2 × `expected-sacrifice-unmapped` (missing ↓ token) — repaired; second run: `status: ok`, 2 records, 0 errors |
| Plan integrity | placeholder scan / heading count / stamp grep | no `[UPPER_SNAKE]` placeholders; exactly one `# Implementation Plan:` heading; `Requirement → Feature` stamp present |
| Deliberation markers | grep over contracts + plan + data-model + quickstart | 0 hits |

## Same-author detection gate (delegated, fresh-context read-only)

Condition held (requirements → plan chain without a break). Detection split into two disjoint scopes: (A) Constitution Check audit; (B) Post-Generation Quality Gate audit. Findings: 13 total (2 HIGH / 8 MED / 3 LOW). Resolution:

| # | Finding (scope) | Verdict | Repair |
|---|-----------------|---------|--------|
| A1 | "pre-dispatch self-check blocks" overstated as existing (HIGH) | partially refuted + repaired | The substring self-check form exists (`fast-fail.md` § 派发前自检); wording now says the **identifier** is added to the existing form (D-14, XVI row, contract C-3) |
| A2 | `test_superagent_zero_mechanism.py` unowned (HIGH) | accepted | Added to P6 paired verification |
| A3 | data-model duplicated the nine-item pointers + message classes (MED) | accepted | Rewritten as item-id slugs only + pointer to owner; classes pinned by test against owner |
| A4 | `requirements § Readers` citation wrong (LOW) | accepted | Cited as frontmatter fields |
| A5 | "(Feature Integration)" citation wrong (LOW) | accepted | Reworded to name the create-plan step |
| A6 | budget literal restated in harness contract (LOW) | accepted | Removed (C-1, C-4) |
| B1 | 17 Mirror-Obligations Verify commands lack premise/pin (MED) | partially refuted (`--only` exact-file prefix works, measured `sync-mirrors.py:37-38`) + repaired | Verify column rewritten as criterion + named pinning test; per-row premises block added |
| B2 | Phase 1 summary counts prose wrong (MED) | accepted | Reworded (three contract files carry shell examples, not two; runnable-fact list corrected) |
| B3 | generator `within` wording (MED) | accepted | Aligned to `BUDGET:` line + `Instructions size:` log line |
| B4 | C-4 self-contradiction (MED) | accepted | Fixed with A6 |
| B5 | stale-bound `900 s` copied (MED) | accepted | Removed; owner referenced |
| B6 | anti-nesting red lines copied (MED) | accepted | Replaced by pointer in data-model §7 + payload contract C-4 |
| B7 | message-class closure untested (LOW) | accepted | Test ownership added (definitions test pins tokens against owner) |
| B8 | anomaly-suppression signals (LOW) | accepted | This evidence file created; Phase 1 summary drift sentence corrected; digest quote replaced by an accurate description |

Downgrade/rejection rate: 2 of 15 finding lines were refuted on measurement (A1 wording-only; B1's "unregistered pair" premise), 0 HIGH left unaddressed. No finding changed a verdict to Fail/Partial.

## Notes for the tasks stage

- Re-run every command example in `quickstart.md` and the three contract files during implementation; paste outputs here or into per-package evidence files.
- The mirror sync must stay file-scoped (`--only <source path>`); never a tree-wide `--write` (428-line pre-existing drift).
- The three pre-existing-dirty definition mirrors are normalized by the file-scoped sync; disclose in the commit body.
