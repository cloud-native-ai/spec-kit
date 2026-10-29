# Quickstart Run Log — 076-decision-tension-contract

**Owner of this file**: the implementation-stage real-run log for the five quickstart scenarios
of `quickstart.md` (S1–S5). `quickstart.md` is a plan-owned artifact and MUST NOT be rewritten
here; this log only carries the executed commands, their real output and the teardown step.

**Status vocabulary per scenario**: `not-run` / `run-green` / `run-red`. A scenario is
`run-green` only when the command in `quickstart.md` was actually executed against the current
tree and its observed exit code matches the declared one.

**Rendering boundary (read before the S3 rows)**: the analyze channel is a declared detection
*pass*, not a program. Its report for a fixture is rendered as the program verdict under the
channel's own severity mapping (every channel finding is HIGH or absent — `detection-and-severity.md`
§ I declares HIGH-or-0, no advisory tier, no semantic scoring surface). The `/speckit.analyze`
narrative layer was not produced by a full skill run in this segment; no SC assertion depends on
it. This is the same rendering T017 declared for SC-003.

| Scenario | 判据 (criterion) | Status |
|----------|------------------|--------|
| **S1** — 写下第一条张力记录并校验 | `validate-decision-tensions.py --spec <spec-dir>` 在含一条合规记录的夹具上输出 `status: ok`、六项标签各 `pass`、退出码 0 | run-green |
| **S2** — 六个反向输入逐个变红 | 12 次运行：1 合规（退出 0）+ 6 类反向输入（删字段逐字段各 1、`expected_sacrifice: none`、不可判定措辞、重复 `tension_id`、跳号、指向不存在的来源）各退出 1 且命中声明标签 | run-green（12/12） |
| **S3** — 分析阶段拦住三类缺陷 | 四个夹具各运行一次：合规 0 条 HIGH；缺章节 1 条；六字段不全 1 条；代价不可映射 1 条 | run-green（4/4，快照落 `notes/analyze-sc003/S3-*.md`） |
| **S4** — 证伪四元组的接收与六类拒收 | 1 合规载荷退出 0；封闭六拒收原因码各一例退出 1（6/6）；载荷不可读退出 2；四个 `missing-field` 附加样本同原因码；双 `red:` 定点载荷以第一次出现切分得到确定 verdict | run-green（11/11 + 定点夹具） |
| **S5** — 镜像与术语 | `sync-mirrors.py --check` 与 `regen-command-copies.py --check` 相对改动前基线无新增漂移；三棵分发面五个别名各 0 且 A3 清单仍在 | run-green |

## Run records

Real output for every run below, plus the driver that produced it, is archived verbatim in
`test-evidence/quickstart-s1-s5.txt`. Fixtures were built under `~/tmp/076-quickstart/` (outside
the repo) and are rebuilt from the archived driver at any time.

### S1 — first record and its structural check

- **Command**: `python scripts/python/validate-decision-tensions.py --spec .specify/specs/076-decision-tension-contract`
- **Output (verbatim head)**: `spec: …/.specify/specs/076-decision-tension-contract` / `status: ok` /
  six `[label] pass (0)` lines / `scanned: 275 lines, 2 record(s)` / `0 error(s), 0 warning(s)`
- **Exit code**: `0` — matches quickstart's declared `status: ok`, all labels pass, exit 0.
- **Fixture**: the feature's own `plan.md` — it is the first DTR instance (`T-001`, `T-002`), so
  the run is against real content, not a synthetic plan.
- **Teardown**: none needed (read-only run over a tracked file).

### S2 — one compliant fixture plus eleven inverse inputs (12 runs)

| Run | Mutation | Exit | Declared label hit |
|-----|----------|------|--------------------|
| 1 | none (compliant) | 0 | all labels 0 |
| 2 | delete `decision` | 1 | `dtr-record-incomplete` = 1 |
| 3 | delete `antithesis` | 1 | `dtr-record-incomplete` = 1 |
| 4 | delete `binding_constraints` | 1 | `dtr-record-incomplete` = 1 |
| 5 | delete `discriminating_evidence` | 1 | `dtr-record-incomplete` = 1 |
| 6 | delete `expected_sacrifice` | 1 | `dtr-record-incomplete` = 1 |
| 7 | delete `revision_trigger` | 1 | `dtr-record-incomplete` = 1 |
| 8 | `expected_sacrifice: none` | 1 | `dtr-rejected-form` = 1 |
| 9 | undecidable wording in `decision` | 1 | `dtr-rejected-form` = 1 |
| 10 | duplicated `tension_id` | 1 | `dtr-tension-id` = 1 |
| 11 | skipped `tension_id` (`T-001` then `T-003`) | 1 | `dtr-tension-id` = 1 |
| 12 | `expected_sacrifice` → undeclared source | 1 | `expected-sacrifice-unmapped` = 1 |

- **Every defect run reports exactly one finding** (`total findings 1`), so the cross-label
  precedence holds in the real CLI rather than only in unit assertions.
- **Teardown**: `rm -rf ~/tmp/076-quickstart` (fixtures outside the repo).

### S3 — four fixtures, one analyze-channel report each (SC-002)

| Fixture | Exit | HIGH | Snapshot |
|---------|------|------|----------|
| compliant record | 0 | 0 | `notes/analyze-sc003/S3-compliant.md` |
| `## Decision Tensions` section absent | 1 | 1 | `notes/analyze-sc003/S3-section-missing.md` |
| record missing `revision_trigger` | 1 | 1 | `notes/analyze-sc003/S3-record-incomplete.md` |
| `expected_sacrifice` → undeclared source | 1 | 1 | `notes/analyze-sc003/S3-cost-unmapped.md` |

- **Exit code**: 0 / 1 / 1 / 1 — the four runs match the declared HIGH counts 0 / 1 / 1 / 1.
- The missing-section fixture is reported, **not skipped** (the fail-closed half of SC-002).
- **Teardown**: fixtures removed with the workspace dir; the four snapshots stay (they are the
  SC-002 evidence slot).

### SC-003 triple (re-run under T026)

`pytest -q tests/contract/test_decision_tension_contract.py -k "d1 or d2 or d3"` → `3 passed`,
exit 0, and the three snapshots re-rendered deterministically:

- `D-1-compliant-na.md` → `HIGH findings: 0`
- `D-2-section-removed.md` → `HIGH findings: 1`
- `D-3-compliant-record.md` → `HIGH findings: 0`

### S4 — quartet accepted once, six reason codes each rejected once (11 runs + pinpoint)

| Run | Payload | Exit | Reason |
|-----|---------|------|--------|
| 1 | compliant (four keys, `raw:` observation, `red:` split with a span on each half) | 0 | accepted |
| 2 | both `attempt` and `exit_code` absent (the 6/6 `missing-field` primary) | 1 | `missing-field` |
| 3 | `attempt` absent (additional sample) | 1 | `missing-field` |
| 4 | `exit_code` absent (additional sample) | 1 | `missing-field` |
| 5 | `observation` absent (additional sample) | 1 | `missing-field` |
| 6 | `would_go_red_if` absent (additional sample) | 1 | `missing-field` |
| 7 | `attempt:` present with a blank value | 1 | `empty-field` |
| 8 | `exit_code: ok` | 1 | `exit-code-not-integer` |
| 9 | `observation` without the `raw:` marker | 1 | `observation-not-raw` |
| 10 | `would_go_red_if: 若实现有误就会失败` (no `red:` marker) | 1 | `tautology` |
| 11 | path that does not exist | 2 | `input-unreadable` |
| (pinpoint) | two `red:` markers: first split keeps a span on both halves, second split would leave the signal half empty | 0 | accepted — the split point is the FIRST occurrence |

- **Exit codes 0 / 1 / 2 are all covered**; rejection rate is 6/6 on the closed reason set.
- **Teardown**: payloads lived in `~/tmp/076-quickstart/`, removed with the workspace dir.

### S5 — mirrors and terminology

- `python scripts/python/sync-mirrors.py --check` → exit 0, six pairs `ok`
  (templates 22 / skills/external 406 / skills/internal 136 / agents 3 / scripts 117 / shared 60).
- `python scripts/python/regen-command-copies.py --check` → exit 0, `OK: all per-tool command
  copies match the source templates.`
- Judged against the pre-change baseline rather than the bare exit code: no pair gained a DIFF
  line (details and per-pair byte comparison in `test-evidence/sync-mirrors-check-after.txt`).
- Terminology: five aliases × three trees = 0, A3 list still present
  (`test-evidence/terminology-counts-after.txt`).
- **Teardown**: none (read-only commands).
