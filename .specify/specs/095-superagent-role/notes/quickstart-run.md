# Quickstart run — 095 Super Agent Role (T049)

**Run**: `r20261110T055657Z-b095` · **Package**: P6 close-out · **Date**: 2026-11-10 · **Host**: local, single workspace
**Executed by**: the P6 session, at the close-out tree (HEAD `d8843810f` + P6 uncommitted artifacts). Every command below was executed from the repository root; outputs are verbatim.

## Scenario 1 — Ask who is whose super agent

```bash
python3 scripts/python/role-edge-check.py --action query \
  --parent root --child A \
  --state-dir tests/fixtures/superagent-role/root-a-b/state \
  --teams-dir tests/fixtures/superagent-role/root-a-b/teams \
  --logs-dir tests/fixtures/superagent-role/root-a-b/logs \
  --registry-dir tests/fixtures/superagent-role/root-a-b/registry
```

Exit **0**. Output, verbatim:

```json
{
  "schema_version": 1,
  "action": "query",
  "edge_exists": true,
  "edge": {
    "parent": "root",
    "child": "A",
    "attempt": "1",
    "role_declaration": "superagent",
    "dispatch_duty": "granted",
    "depth": 1,
    "source": {
      "carrier": "team-report",
      "path": "tests/fixtures/superagent-role/root-a-b/teams/demo-team/runs/20261110T000000Z-report.md",
      "line": 7
    }
  },
  "parent": {"id": "root", "roles": ["superagent"], "role_set_marker": null, "depth": 0},
  "child": {"id": "A", "roles": ["subagent", "superagent"], "role_set_marker": "dual-role", "depth": 1},
  "violations": []
}
```

Reading: the edge exists and is sourced from the team run-report line; A is a `subagent` and a `superagent` on different edges, expressed by the output-only `role_set_marker = "dual-role"`; no violations. The full model is `--action report` with the same roots (recorded in `test-evidence/role-edge-engine-readings.txt` §3).

## Scenario 2 — See the role view in the existing digest

```bash
python3 .specify/scripts/python/status-digest.py --action digest
```

Exit **0**. Output, verbatim (2026-11-10T14:32:59Z, live workspace):

```text
状态摘要 · 生成于 2026-11-10T14:32:59.505663Z（UTC）· 最多 20 条 · 注册目录 /home/agent/.local/state/spec-kit/lines

执行体                            所属 spec                      父边                    角色        深度  在做什么                         状态                          已执行时间
--------------------------------  -----------------------------  ----------------------  ----------  ----  -------------------------------  ----------------------------  ------------
095-superagent-role-implement-p6  -                              r20261110T055657Z-b095  subagent    1     -                                运行中                        -
—（无存活执行体）                 096-sdd-observer-agent         -                       superagent  0     /speckit.implement: 实现         活跃（静默 39 分）            6 小时 21 分
—（无存活执行体）                 097-speckit-migrate-command    -                       superagent  0     /speckit.implement: 实现         活跃（静默 39 分）            6 小时 21 分
—（无存活执行体）                 098-suite-speed-optimizations  -                       superagent  0     /speckit.implement: 实现         活跃（静默 39 分）            6 小时 21 分
fork(qodercli, pid 3306262)       095-superagent-role            -                       superagent  0     /speckit.implement: 实现（p6）   活跃                          15 分
—（无存活执行体）                 099-speckit-seal               -                       superagent  0     -                                活跃（静默 2 小时 19 分）     2 小时 19 分
—（无存活执行体）                 074-goal-team-sdd-unification  -                       -           -     /speckit.requirements: 需求撰写  已停滞（静默 12 天 22 小时）  13 天 1 小时
```

```bash
python3 .specify/scripts/python/status-digest.py --action digest --format json
```

Exit **0** (124,269 B). Bounded projection of the same read:

```text
top-level keys: ['all_entries', 'cap', 'efficiency', 'entries', 'executors', 'generated_at',
                 'omitted', 'profile', 'registry_dir', 'stale_bound_seconds', 'state_summary', 'workspace']
entries: 7  all_entries: 120  omitted: 0
row: 095-superagent-role-implement-p6 | parent=r20261110T055657Z-b095 | roles=['subagent'] | marker=None | depth=1 | state=running
row: 095-superagent-role            | parent=None                    | roles=['superagent'] | marker=None | depth=0 | state=active
```

Reading: every row carries identity, parent edge, roles, marker and depth beside the existing fields; the stage executor row's parent is the line's spine `run_id`; `omitted` and `nothing-running` semantics were unchanged (the idle-line row and the previously measured exit-3 reading are in `test-evidence/status-digest-roles-readings.txt`).

## Scenario 3 — Grant dispatch duty and carry the injection (payload obligation, no command)

The quickstart declares this scenario as a payload-writing obligation, not a command. Its two observable surfaces were asserted directly:

```bash
python3 - <<'PY'
from pathlib import Path
import re
fx = Path('tests/fixtures/superagent-role/payload/role-transition-complete.md').read_text(encoding='utf-8')
slugs = re.findall(r'^\d+\. `([a-z-]+)`', fx, re.M)
print('nine-item slugs found:', len(slugs), slugs)
fields = Path('tests/fixtures/superagent-role/payload/role-fields.md')
print('role-fields fixture exists:', fields.is_file())
rows = re.findall(r'^\| `([a-z_]+)` \|', fields.read_text(encoding='utf-8'), re.M)
print('seven downlink fields:', len(rows), rows)
skill = Path('skills/internal/run-agent/SKILL.md').read_text(encoding='utf-8')
print('run-agent SKILL carries role-transition:', 'role-transition' in skill)
assert len(slugs) == 9 and 'role-transition' in skill
print('ASSERTION: pass')
PY
```

Output, verbatim:

```text
nine-item slugs found: 9 ['role-activation-scope', 'self-identity-parent-edge', 'downward-obligation-checklist', 'concurrency-budget-ref', 'reporting-path', 'state-carriers-writer-boundary', 'attention-classes-escalation', 'depth-remaining-prohibitions', 'aggregate-return-contract']
role-fields fixture exists: True
seven downlink fields: 7 ['parent_identity', 'child_label', 'role_declaration', 'dispatch_duty', 'depth_position', 'authority_ref', 'return_channel']
run-agent SKILL carries role-transition: True
ASSERTION: pass
```

Reading: the complete-payload fixture carries the literal identifier and the closed nine item-id slugs; the same payload names the seven downlink role fields; the run-agent SKILL declares the obligation. The enforcement half (delete-one blocks via the substring self-check; anti-nesting red) is recorded in `test-evidence/role-transition-readings.txt`.

## Scenario 4 — Verify the harness landing is inside budget

```bash
python3 scripts/python/sync-mirrors.py --write --only templates/instructions-template.md
bash scripts/bash/generate-instructions.sh
```

Exit **0** for both. Generator output (subset, verbatim):

```text
[info] Existing instructions kept as the refresh base (not overwritten).
[info] Instructions size: 38301 B (budget 38400 B, 99 B headroom). Section table, largest first:
| Super Agent (相对逻辑角色)                            | 333    | 333    | 0     | no          | no            |
```

Reading: the template mirror is byte-identical, the live file keeps its refresh base, the size line reports a **positive 99 B headroom** against the 38,400 B budget (the `BUDGET:` computation inside the generator yields `within` and feeds this line; the verdict is pinned by `tests/contract/test_instructions_budget_superagent_section.py` § C-4), and the per-section table carries exactly one row for the new section (333 B, template-equal, no placeholder, not project-owned). A `git status --porcelain` over `.specify/instructions.md` and both template copies after the run is empty — the generator re-run changed no tracked byte.

## Teardown

- The engine and the digest are read-only: no fixture, registry or state file was modified by scenarios 1–2 (their structural read-only pins are part of the contract tests).
- Scenario 4's generator re-run produced no tracked change; its timestamped backup under `.specify/instructions.md-*` is gitignored by `.specify/.gitignore:19`.
- No background process was started; nothing to stop.
