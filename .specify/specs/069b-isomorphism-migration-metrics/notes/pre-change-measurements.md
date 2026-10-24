# Pre-Change Measurements — 069b（改前基线）

**Captured**: 2026-10-25T01:02+0800（UTC `2026-10-24T17:02:19Z`）· **Branch**: `069b-isomorphism-migration-metrics`
**HEAD**: `4710676297dcdbcaabb72f6dc7882abfae906006`（short `47106762`）
**Owner of this record**: T001（改前基线）——本文件是后续所有「相对基线零新增」判据的分母来源，逐项贴真实输出与捕获时间。
**Not the owner of the failing test names**: 失败名单与计数只由 `notes/test-baseline-contract.txt` 拥有（T003 重采前其冻结值属 069a 采集）；本文件只记录该文件的**在盘状态**，不复述其数字为当前实测。

> 本文件只做观测：T001 不写任何源文件（`.md` / `.py` / 模板 / 镜像）。所有命令在本仓根目录执行，`python3` 为系统解释器；pytest 唯一可用解释器是 `/Users/liuqiming.lqm/project/profiles/.venv/bin/python`。

---

## 1. 镜像与命令副本（Mirror Obligations 的分母）

### 1.1 `sync-mirrors.py --check`

命令与真实输出（2026-10-25T01:00Z 前后，exit 0）：

```
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (396 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (112 files)
ok    shared/ == .specify/shared/ (55 files)
EXIT=0
```

基线判读：六对全部 `ok`，零差异；`scripts/` 112 files、`shared/` 55 files 是两个编辑面所在的投影规模。

### 1.2 `regen-command-copies.py --check`

```
$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
EXIT=0
```

基线判读：命令副本与 `templates/commands/` 同源；本切片不改 `templates/commands/`，收尾时该检查必须继续 `OK`。

### 1.3 两个编辑面的源/镜像字节等同（改前值）

`shasum -a 256` + `cmp`（2026-10-25T01:01Z）：

```
3f9240313e5d7922207c7a725f90fdfdf3e360cf776ba1772630b55afd450b4b  shared/definitions/flow-class-definitions.md
3f9240313e5d7922207c7a725f90fdfdf3e360cf776ba1772630b55afd450b4b  .specify/shared/definitions/flow-class-definitions.md
804eb693b2bd7d12c803f7a671fd4c3767c4aeede9c0963a926dfecaf2056b9e  scripts/python/flow-class-check.py
804eb693b2bd7d12c803f7a671fd4c3767c4aeede9c0963a926dfecaf2056b9e  .specify/scripts/python/flow-class-check.py
owner mirror identical
engine mirror identical
```

---

## 2. 结构面（`docs-utils.py --action validate`）

```
$ python3 skills/external/create-docs/scripts/docs-utils.py --action validate --root .
{
  "violations": [
    {
      "kind": "broken-link",
      "path": "docs/concepts/overview.md",
      "detail": "../../tests/unit/test_qoder_support_matrix.py"
    },
    {
      "kind": "broken-link",
      "path": "docs/concepts/overview.md",
      "detail": "../../tests/integration/test_qoder_refresh.py"
    },
    {
      "kind": "note-frontmatter",
      "path": "docs/notes/type-follows-stage-misclassification.md",
      "detail": "missing: "
    }
  ]
}
EXIT=0
```

基线值：`violations = 3`，kind 集合 = `{broken-link: 2, note-frontmatter: 1}`（均为既有债，本切片不修不掩盖）。判据是**零新增**违规（计数与 kind 集合双维度），不是「全绿」。

---

## 3. 069a 测试基线（`notes/test-baseline-contract.txt` 改前在盘状态）

该文件在 HEAD `47106762` 已跟踪（`git ls-files` 命中），冻结于 `f0df3d0b`（2026-10-25 采集），冻结命令只跑 `tests/contract`。改前头部原文：

```
# Contract test baseline (name-level) — 069b
# measured 2026-10-25 at HEAD f0df3d0b (branch 069b-isomorphism-migration-metrics)
# command: SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python bash scripts/bash/run-tests.sh --names-out <out> tests/contract -q --tb=no -p no:cacheprovider
# result: 33 failed, 4277 passed, 5 skipped, 1 warning in 238.53s (0:03:58)
# criterion: zero NEW failing node ids against this list (never "all green").
# owner of the count and the names: THIS FILE only — plan/tasks/verification cite it, never restate numbers.
```

在盘规模：`wc -l` = 40 行（6 行判据/元信息 + 1 空行 + **33 条失败 nodeid**）。T003 会在实现起点按 `tests/contract tests/unit` 两侧重采并重写该文件，本文件不预先复述其数字作为当前实测。

---

## 4. 客户快照 HEAD（SC-002 的冻结样本，复测于 2026-10-25T01:01Z）

命令：逐项目 `git -C <project> rev-parse --short HEAD` / `rev-parse HEAD` / `branch --show-current` / `status --porcelain | wc -l` / `test -f <project>/.specify/shared/definitions/flow-class-definitions.md` 与 `.specify/scripts/python/flow-class-check.py`。

| # | 项目 | short HEAD | 完整 HEAD | 分支 | 脏文件数 | owner 载荷 | engine 载荷 |
|---|------|-----------|-----------|------|---------|-----------|------------|
| 1 | `/Users/liuqiming.lqm/project/kangaroo-xuanji/xuanji-agent` | `3f68b62` | `3f68b621c556ee5a746169e1f8366196aa309825` | `master` | 195 | absent | absent |
| 2 | `/Users/liuqiming.lqm/project/kangaroo-xuanji/xuanji-cli` | `a0c476d` | `a0c476db81cb348f14e6fa421e358d4081afe667` | `xuanji/develop` | 548 | absent | absent |
| 3 | `/Users/liuqiming.lqm/project/kangaroo-xuanji/xuanji-function` | `a2fad18` | `a2fad18cacf135d248ea8ecaa20b11f79f23ebe3` | `main` | 28 | absent | absent |

与 `notes/migration-samples.md` 的冻结表逐值一致（HEAD / 分支 / 脏文件数 / 载荷状态）。三者均**未刷新**：069a 的 owner 与 engine 载荷都不在，快照套件命令见该文件的「2026-10-25 跑测机制更正」节。

---

## 5. Owner 文档现状（`shared/definitions/flow-class-definitions.md`）

命令：`grep -n '^## '` / `grep -c '^## 同构映射'` / `grep -c '^## 不可同构边界'` / `grep -c '069b 承接'` / `grep -n '069b'`：

```
## 判据                    :22
## 命名空间                :73
## 与复杂度轴正交          :80
## 所有权：归框架，客户项目只为自己新增的流程声明 :85
## 逐流程台账              :91
## 类中立清单              :181
## 变更记录                :195
## 消费方指针              :204
```

```
## 同构映射 count: 0
## 不可同构边界 count: 0
069b 承接 total: 12
由 069b 承接: 3
line numbers of 069b mentions: 19 35 48 88 95 103 111 113 114 153 158 163 170
```

基线判读：

- 两个待新增章节（`## 同构映射`、`## 不可同构边界`）**均不存在**（0 命中）。
- `069b 承接` 12 处：`:19`（P2 交接行，T006 删）、`:35`（mixed-oracle 判据里的交接，T011 收）、`:95`（台账说明，T011 收）、`:103/:111/:113/:114/:153/:158/:163/:170`（8 行台账 `notes`，T011 收）；另有 `:48` 一处「归 069b」不含「承接」字样（§ 判据表内），`:88` 一处「由 069b 承接」（P3 § 所有权）。
- `由 069b 承接` 3 处 = `:19` `:35` `:88`（与 tasks § Measured Premises 一致）。

---

## 6. 台账现状（`flow-class-check.py --action check`）

```
$ python3 scripts/python/flow-class-check.py --action check --format json
{
  "action": "check",
  "checked_at": "2026-10-24T17:00:55Z",
  "repo": "/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit",
  "units": 78,
  "inventory": {
    "commands": 27,
    "skills": 51,
    "floors": {
      "commands": 27,
      "skills": 51
    }
  },
  "findings": [],
  "error": null
}
EXIT=0
```

基线判读：`units = 78`（27 命令模板 + 51 技能）、`findings = []`、exit 0。该输出尚无 `coverage` 块与 `red_kind`（本切片 T019 才引入），故此处即为 069a 形态的基线。

---

## 7. 引擎现状（动作集）

```
$ grep -n 'choices=' scripts/python/flow-class-check.py
665:    parser.add_argument("--action", required=True, choices=("check", "lookup"))
672:    parser.add_argument("--format", default="text", choices=("text", "json"))
```

基线判读：只有 `check` / `lookup` 两个动作；`isomorphism` / `delegation` / `faces` 三个动作不存在（T008 / T020 / T021 才新增）。`--action check` 与 `--action lookup` 的既有行为是本切片的零改动面。

---

## 8. 流程单元清单规模（台账分母与 `LEDGER_FLOOR` 的自变量）

```
$ ls templates/commands/*.md | wc -l
27
$ ls -d skills/external/*/ | wc -l
14
$ ls -d skills/internal/*/ | wc -l
37
$ comm -12 <(ls skills/external) <(ls skills/internal)
(空输出)
```

基线判读：技能 14 + 37 = 51，合计 78；`comm -12` 空输出 = 零同名冲突。T019 的解析侧下限 `⌊(27+51)/2⌋ = 39` 由这组清单侧计数推导。

---

## 9. 红先前提前提（8 支新测试与被否决备选路径）

```
$ for f in tests/contract/test_isomorphism_map.py tests/contract/test_ledger_reconciliation.py \
    tests/contract/test_delegation_classes.py tests/contract/test_expression_faces.py \
    tests/contract/test_migration_distribution.py tests/contract/test_measurement_instruments.py \
    tests/unit/test_isomorphism_checker.py tests/unit/test_reconciler_extensions.py; do
    [ -e "$f" ] && echo "PRESENT $f" || echo "ABSENT $f"; done
ABSENT tests/contract/test_isomorphism_map.py
ABSENT tests/contract/test_ledger_reconciliation.py
ABSENT tests/contract/test_delegation_classes.py
ABSENT tests/contract/test_expression_faces.py
ABSENT tests/contract/test_migration_distribution.py
ABSENT tests/contract/test_measurement_instruments.py
ABSENT tests/unit/test_isomorphism_checker.py
ABSENT tests/unit/test_reconciler_extensions.py

$ test -e shared/definitions/isomorphism-map.md && echo PRESENT || echo ABSENT
ABSENT
```

基线判读：8/8 测试文件 ABSENT（红先成立的前提）；被否决备选 `shared/definitions/isomorphism-map.md` 保持 ABSENT（MUST 保持）。

---

## 10. 工作树与提交状态（本切片相关条目）

```
$ git rev-parse HEAD
4710676297dcdbcaabb72f6dc7882abfae906006

$ git status --short | grep -E '069b|flow-class|shared/definitions|scripts/python/flow-class-check'
?? .specify/memory/session/20261024T164126Z-run-determination-speckit-checklist-checklist-069b-20261025t.md

$ git ls-files .specify/specs/069b-isomorphism-migration-metrics | wc -l
17
```

基线判读：

- 本切片规格目录 17 个文件全部已跟踪、无改动；两个编辑面（`shared/definitions/flow-class-definitions.md`、`scripts/python/flow-class-check.py`）与镜像均无改动。
- 唯一命中「069b」的工作树条目是一条**运行期记录**（`.specify/memory/session/…069b…md`，untracked），按提交纪律不提交。
- 全仓工作树共 28 条：6 条已跟踪文件被改（均为 `.specify/memory/session/` 下的既有运行判定记录）+ 22 条 untracked（`.spec-kit/` 1 条、`exec-quant/records/` 7 条、`feedback/` 7 条、`session/` 7 条）——全部属运行期/工具产物，T001–T003 的提交只取本特性基线产物。

---

## 11. 基线所有权索引（后续任务只引用，不复制数值）

| 基线面 | 所有者文件 | 本文件角色 |
|--------|-----------|-----------|
| 镜像六对与命令副本 | 本文件 § 1（T024 / GATE-5 对照） | 分母 |
| 结构面 violations（3 / 两类） | 本文件 § 2（T025 / GATE-7 对照） | 分母 |
| 契约+单元失败 nodeid 名单 | `notes/test-baseline-contract.txt` | 只记在盘状态（§ 3），T003 重采 |
| 条款覆盖基线（uncovered 名单） | `coverage-baseline.txt` | 本文件不记数值（T002 负责重采） |
| 客户快照 HEAD / 载荷 | `notes/migration-samples.md`（冻结表）+ 本文件 § 4（复测） | 分母 |
| owner 文档 / 台账 / 引擎形态 | 本文件 § 5–§ 7 | 分母 |

---

## 12. T003 重采的名单差值（2026-10-25T01:12Z）

重采命令（两侧都采，与 GATE-4 / T026 的比对范围一致）：

```
SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python \
  bash scripts/bash/run-tests.sh --names-out ~/tmp/069b-names-contract.txt \
  tests/contract tests/unit -q --tb=no -p no:cacheprovider
# result: 33 failed, 5091 passed, 5 skipped, 4 warnings in 392.31s (0:06:32)
# runner banner: # test runner: /Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/contract tests/unit -q --tb=no -p no:cacheprovider
# failed-name list written: /Users/liuqiming.lqm/tmp/069b-names-contract.txt (33 entries)
# EXIT=1（pytest 自身失败状态；基线采集非「测试全绿」判据）
```

与文件内冻结名单（改前 33 条）的差值：

```
comm -13 <frozen> <re-measured>  → 0 条（零新增失败名）
comm -23 <frozen> <re-measured>  → 0 条（零消失/零修复）
计数：frozen 33 / re-measured 33
```

**diff: empty**——重采名单与 069a 阶段冻结名单逐名相同，无需在基线文件里追加迁移注记。`notes/test-baseline-contract.txt` 已按重采结果重写头部（HEAD `47106762`、日期 `2026-10-25`、命令扩到 `tests/contract tests/unit`、结果行 `33 failed, 5091 passed, 5 skipped, 4 warnings in 392.31s`），判据行与 owner 行原样保留。

---

## 13. T002 条款覆盖基线重采核对（程序性记录，2026-10-25T01:03Z）

命令（先落临时文件，核对通过后才替换在盘基线，避免失败时截断唯一对照物）：

```
python3 .specify/scripts/python/account-clause-coverage.py \
  .specify/specs/069b-isomorphism-migration-metrics --freeze > ~/tmp/069b-coverage-baseline.txt
# EXIT=0，497 行（2 行头 + 495 条基线名）
```

核对结果（全部按任务行的四项判据）：

| 判据 | 实测 |
|------|------|
| 头部含 `frozen-from:` | 命中 1 次 |
| 头部含 `excluding 069b-isomorphism-migration-metrics` | 命中 1 次 |
| 基线正文不含本切片 51 条 `C-N` 名 | 前缀 `069b-isomorphism-migration-metrics/` 命中 0；逐名核对 `clauses_expected=51 / names_in_baseline=0` |
| 与在盘基线对比 | 仅头部 `base-sha` 由 `9bfe53dec41c` 变为 `4710676297dc`（实现起点 HEAD），正文名单 `comm -3` = 0 行 |

替换后在盘基线重跑核算（无 `--freeze`）：

```
claimed clauses (this feature): 51
baseline: .specify/specs/069b-isomorphism-migration-metrics/coverage-baseline.txt (495 names)
uncovered beyond baseline: 0
FR universe: 14 / FR claimed: 14 / FR uncovered: 0
status: ok   EXIT=0
```
