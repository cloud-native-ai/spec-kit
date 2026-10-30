# Pre-change measurements — 079 humanize run output

**Role**: 本文件是全特性「改动前侧」的唯一落点（T001 / T002）。后续任何行引用「改动前」时只指向这里与 `coverage-baseline.txt`；实现期不得回填或刷新本文件的历史读数，只能追加新小节。

- **Measured at**: 2026-10-30T15:41Z（T001 起点；命令逐条真实执行，命令、日期与退出码一并记录）
- **Branch**: `079-humanize-run-output`
- **HEAD**: `c6ac8c99`（上一阶段 implement 起点提交；工作树已有脏文件 `M .specify/memory/session/20261029T101833Z-...md`、`?? baseline-failed.txt`、`?? state/079-humanize-run-output.md`，均非本段产物、不提交不还原）
- **Wiring baseline commit**: `35ff11bc`（A11 发现命令的固定参照物）
- **解释器**: `python3` = `Python 3.9.6`；pytest 走仓库 `.venv`（本文件不重测，基线见 E2）

---

## ① 四组计数（requirements.md）

| 测量 | 命令 | 真实输出 | 退出码 |
|------|------|----------|--------|
| FR 定义行 | `grep -cE '^- \*\*FR-[0-9]{3}\*\*:' .specify/specs/079-humanize-run-output/requirements.md` | `30` | 0 |
| SC 定义行 | `grep -cE '^- \*\*SC-[0-9]{3}\*\*:' .specify/specs/079-humanize-run-output/requirements.md` | `10` | 0 |
| 用户故事数 | `grep -cE '^### User Story' .specify/specs/079-humanize-run-output/requirements.md` | `4` | 0 |
| Shared Strings | `grep -cE '^\| .STR-[0-9]{3}.' .specify/specs/079-humanize-run-output/requirements.md` | `15` | 0 |

## ② 五份契约逐份条款行首计数

命令：`grep -cE '^- \*\*[A-Z]{2}-[0-9]{2}\*\*' .specify/specs/079-humanize-run-output/contracts/*.md`（日期 2026-10-30，退出码 0）

| 契约文件 | 条款定义行 |
|----------|-----------|
| `contracts/content-mode.contract.md` | `10`（CM-01…CM-10） |
| `contracts/execution-dispatch.contract.md` | `21`（EX-01…EX-21） |
| `contracts/invocation-parse.contract.md` | `17`（IP-01…IP-17） |
| `contracts/report-assembly.contract.md` | `20`（RP-01…RP-20） |
| `contracts/wiring-compat.contract.md` | `20`（WC-01…WC-20） |
| **合计** | **`88`** |

## ③ A11 接线面发现（基线提交 `35ff11bc`，无限制）

- **发现命令**：`git grep -l -i humanize 35ff11bc` → **164 命中 / 164 unique paths**（退出码 0）。
- **两个实测陷阱（记录为事实，不是建议）**：
  1. 带 revision 的 `git grep -l` 输出形如 `35ff11bc:<path>`；分类前 MUST 剥掉 `^[0-9a-f]{7,40}:` 前缀，否则每条路径都不匹配任何路径族判据（首次误跑得到 `frozen-verification=164`，已纠正后重跑）。
  2. pinned 文件 `test-evidence/wiring-inventory-baseline.txt` 按 A11 五类**语义分组**排列，不是码点序；`comm` 前 MUST 对两侧做 `LC_ALL=C sort`，否则 328 行全量伪差。排序后比较才有意义。
- **分类结果**（规则 owner = requirements § Wiring Surface — A11 Closed Set，按序求值首个匹配）：

| 类 | 条数 |
|----|------|
| 活源 live-source | `7` |
| 派生副本 derived-copy | `4` |
| 镜像 mirror | `1` |
| dated record | `114` |
| 冻结验证 frozen-verification | `38` |
| 未分类 unclassified | `0` |

- **与 tasks-fix 阶段 pin 的比对**：
  ```
  grep -v '^#' <pin> | sed '/^$/d' | LC_ALL=C sort > /tmp/pin
  LC_ALL=C sort <regenerated class+path> > /tmp/regen
  LC_ALL=C comm -3 /tmp/regen /tmp/pin
  ```
  → **delta_lines = 0**（退出码 0）。pin 是派生记录，不是白名单；本次重算与它完全一致。

## ④ 四条基线（改动前）

| 测量 | 命令 | 真实输出 | 退出码 |
|------|------|----------|--------|
| 命令副本 | `python3 scripts/python/regen-command-copies.py --check` | `OK: all per-tool command copies match the source templates.` | 0 |
| 镜像 | `python3 scripts/python/sync-mirrors.py --check` | `ok templates/ == .specify/templates/ (22 files)` / `ok skills/external/ == .specify/skills/ (406 files)` / `ok skills/internal/ == .specify/skills/internal/ (136 files)` / `ok agents/ == .specify/agents/templates/ (3 files)` / `ok scripts/ == .specify/scripts/ (117 files)` / `ok shared/ == .specify/shared/ (60 files)` | 0 |
| 编译面 | `python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` | `compile-embeds --check: 75 units, zero drift` | 0 |
| 门禁 | `python3 scripts/python/scan-confirmation-gates.py --summary` | `blocking confirmation gates: 27` / `destructive: 20` / `governance_kept: 7` / `violations (reversible gates still blocking): 0` | 0 |

## ⑤ 技能正文预算（改动前）

命令：`python3 skills/external/improve-skills/scripts/skill-shape.py skills/external/humanize/SKILL.md`（退出码 0）

```
判定        pass
正文估算     ≈4090 tokens 可控 / 预算 5000（123 行）
最大章节     Workflow
发现：
  ! [oversized-section] Workflow=59行（单章节建议上限 40 行）
  ! [flags-outside-contract] 38 个具体 CLI flag 出现在非约束章节
```

判据：T003 改完必须仍为 `pass` 且正文 ≤ 5000 tokens；新增细则落 `references/`，不塞正文。

## ⑥ 夹具与临时根（改动前）

| 测量 | 命令 | 真实输出 | 退出码 |
|------|------|----------|--------|
| 历史语料未改写 | `git diff --stat 35ff11bc -- tests/fixtures/humanize` | 空输出 | 0 |
| 受制裁临时根已匹配 | `git check-ignore -v .specify/.tmp/humanize/x.run` | `.specify/.gitignore:30:.tmp/	.specify/.tmp/humanize/x.run` | 0 |

`tests/fixtures/humanize/run/` 在本次读数时**尚不存在**（由 T004 建）；既有语料 `files/`、`inline/`、`selftest/`、`tone/`、`README.md`、`rubric.md`、`diff_protected.py` 保持逐字节不变（WC-15）。

---

# T002 — 冻结条款覆盖基线复核（2026-10-30T15:47Z）

**基线文件**：`.specify/specs/079-humanize-run-output/coverage-baseline.txt`（497 行 = 2 行头 + 495 个冻结 UNCOVERED 名；头记录 `base-sha 70dd9e78`、`files: 234`）。本小节只**复核**，MUST NOT 重写基线（未使用 `--freeze`）。

**命令**（退出码 1 —— 该工具在「有未覆盖项」时按设计返回 1，不是本阶段异常）：
```
python3 scripts/python/account-clause-coverage.py .specify/specs/079-humanize-run-output
```

**真实读数**：

| 读数 | 值 |
|------|-----|
| `claimed clauses (this feature)` | `0` |
| `baseline` | `coverage-baseline.txt (495 names)` |
| `baseline-internal existing uncovered` | `495` |
| `uncovered beyond baseline`（相对冻结基线的漂移） | `0` |
| `UNCOVERED` 中属于本特性的条数 | `0`（495 条全部为基线内部既有项） |
| `FR uncovered` | `30`（`0 of 30 FRs cited from citation groups`） |
| `scanned files` / `clause universe` / `FR universe` | `239` / `1464` / `30` |
| 工具自评 | `[clause-uncovered] pass (495)`、`[coverage-baseline-delta] pass (0)`、`[fr-uncovered] fail (30)`、`status: uncovered` |

**差值结论**：相对冻结基线，条款车道 **delta = 0**（无新增、无消失）；FR 车道 **0/30**，与本特性在 tasks 阶段的记录一致，无漂移，无需交 `/speckit/analyze` 裁定。

**为什么条款车道看不见本特性的 88 条**（同一命令的 `--list-named` 实测）：
```
python3 scripts/python/account-clause-coverage.py .specify/specs/079-humanize-run-output --list-named
  NAMED: 079-humanize-run-output/contracts/content-mode.contract.md
  NAMED: 079-humanize-run-output/contracts/execution-dispatch.contract.md
  NAMED: 079-humanize-run-output/contracts/invocation-parse.contract.md
  NAMED: 079-humanize-run-output/contracts/report-assembly.contract.md
  NAMED: 079-humanize-run-output/contracts/wiring-compat.contract.md
```
五份契约在 `clause_extract.py` / owner forms 下均判 `md-none`（命名但不可解析，0 clauses）：`IP` / `EX` / `RP` / `CM` / `WC` 两字母命名空间不在 `C-<n>` 形态集内。故条款车道看不见这 88 条，覆盖由 `tasks.md` § Contract Coverage Map 的人工指派 + T036 的 `test_wc12_clause_test_map_is_total` 机器核对承担，**不靠基座豁免**。把 88 条改名为 `C-<n>` 属 plan 属主制品变更，本阶段不做。
