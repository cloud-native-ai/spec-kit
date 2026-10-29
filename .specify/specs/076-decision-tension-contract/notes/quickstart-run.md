# Quickstart Run Log — 076-decision-tension-contract

**Owner of this file**: the implementation-stage real-run log for the five quickstart scenarios
of `quickstart.md` (S1–S5). `quickstart.md` is a plan-owned artifact and MUST NOT be rewritten
here; this log only carries the executed commands, their real output and the teardown step.

**Status vocabulary per scenario**: `not-run` / `run-green` / `run-red`. A scenario is
`run-green` only when the command in `quickstart.md` was actually executed against the current
tree and its observed exit code matches the declared one.

| Scenario | 判据 (criterion) | Status |
|----------|------------------|--------|
| **S1** — 写下第一条张力记录并校验 | `validate-decision-tensions.py --spec <spec-dir>` 在含一条合规记录的夹具上输出 `status: ok`、六项标签各 `pass`、退出码 0 | not-run |
| **S2** — 六个反向输入逐个变红 | 12 次运行：1 合规（退出 0）+ 6 类反向输入（删字段逐字段各 1、`expected_sacrifice: none`、不可判定措辞、重复 `tension_id`、跳号、指向不存在的来源）各退出 1 且命中声明标签 | not-run |
| **S3** — 分析阶段拦住三类缺陷 | 四个夹具各运行一次：合规 0 条 HIGH；缺章节 1 条；六字段不全 1 条；代价不可映射 1 条 | not-run |
| **S4** — 证伪四元组的接收与六类拒收 | 1 合规载荷退出 0；封闭六拒收原因码各一例退出 1（6/6）；载荷不可读退出 2；四个 `missing-field` 附加样本同原因码；双 `red:` 定点载荷以第一次出现切分得到确定 verdict | not-run |
| **S5** — 镜像与术语 | `sync-mirrors.py --check` 与 `regen-command-copies.py --check` 相对改动前基线无新增漂移；三棵分发面五个别名各 0 且 A3 清单仍在 | not-run |

## Run records

_Empty at segment start. Each executed scenario appends: command / real output / exit code /
criterion verdict / teardown step._
