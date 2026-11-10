# Pre-change measurements — Feature 097 (/speckit.migrate 一次性迁移收尾命令)

**Capture date**: 2026-11-10 (implement entry, worktree `.specify/.tmp/sdd-loop/worktrees/097-speckit-migrate-command`)
**Capture point**: before any implement-stage framework-source write on this line
**Owner of the baseline form**: `/speckit.implement` step 6 `**Test runs**` bullet — this file only points at it and never restates its form (name-level baseline via `--names-out`, comparison via `comm -13`).

**Premise re-measurement rule** (tasks.md § Notes): every quantity below is re-captured at implement entry; a differing re-capture replaces the cited value rather than keeping the stale one.

本文件由 Setup 包（T001–T004）建立并追加，append-only：后续包只在对应小节追加读数，不另造落点。

## T002 — 命令面基线重捕获

- 捕获时间: 2026-11-10T12:43:10Z（实现入口实测，本工作树）
- 判据: 逐条粘贴真实输出与退出码；与 tasks.md § Premises measured at generation time 对照，不一致则以本次重捕获替换（本次七项全部一致，无替换）。

| # | 命令（逐字） | 真实输出 | 退出码 | 对 premises |
|---|---|---|---|---|
| 1 | `ls templates/commands/*.md \| wc -l` | `29` | 0 | 29 一致 |
| 2 | `ls .github/prompts/*.prompt.md \| wc -l` | `29` | 0 | 29 一致 |
| 3 | `ls .claude/commands/speckit.*.md \| wc -l` | `29` | 0 | 29 一致 |
| 4 | `ls .qoder/commands/speckit.*.md \| wc -l` | `29` | 0 | 29 一致 |
| 5 | `ls .opencode/command/speckit.*.md \| wc -l` | `29` | 0 | 29 一致 |
| 6 | `ls docs/reference/commands/*.md \| wc -l` | `27` | 0 | 27 一致 |
| 7 | `grep -n "assert len(COMMAND_BASELINE)" tests/contract/test_migration_distribution.py` | `127:assert len(COMMAND_BASELINE) == 29` | 0 | 行 127、`== 29` 一致 |

**备注（naive form 陷阱，来自 tasks.md premises 表述）**: 裸 `ls <dir> | wc -l` 会计入非 `.md`/非 `speckit.*` 条目；上表一律使用带 glob 的形态，单位正确。

---

## T004 — 契约覆盖基线冻结读数（implement 入口首次全树会计）

- 捕获时间: 2026-11-10T12:44Z 左右（实现入口，本工作树）
- 冻结命令（逐字）:

```bash
python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/097-speckit-migrate-command --freeze > .specify/specs/097-speckit-migrate-command/coverage-baseline.txt
```

- 冻结退出码: `0`；冻结产物: `.specify/specs/097-speckit-migrate-command/coverage-baseline.txt`，`642` 行 = 2 行头 + `640` 个名字（与生成期 premises 的 640 名一致）。
- 头部差异（重捕获替换 stale 值，tasks.md § Notes「Premise re-measurement」）: `base-sha` 由 `96df5d2f56b8` 更新为当前 HEAD `4194e0ebb0c2`；其余头部字段（frozen-from / owner-forms / files 286 = parsed 179 + named 107）逐字不变，名字集合逐行相同。这是 implement 入口的首次全树会计，取代生成期读数。

### live 会计读数（同一时点，`--spec-dir` 非冻结运行）

命令（逐字）:

```bash
python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/097-speckit-migrate-command
```

- 退出码: `1`（`status: uncovered`，属阶段待办状态，非门禁失败）；完整输出: `test-evidence/implement-entry-coverage-live.txt`。
- 决定性读数（逐字）:

```text
[clause-uncovered] fail (644) — 644 uncovered, 4 beyond the frozen baseline
[fr-uncovered] fail (21) — 4 of 25 FRs cited from citation groups
[clause-unparsable] fail (108) — 108 files yield no clause id under the owner's forms; 1 of them declare a positive form, which is parse doubt and is never read as zero-and-covered
[coverage-baseline-delta] fail (4) — baseline holds 640 names; 640 uncovered items are baseline-internal and do not block
25 error(s), 1 warning(s)
```

- `4 beyond the frozen baseline` 逐名（`--json` 的 `uncovered_beyond_baseline` 字段，逐字）:

```text
097-speckit-migrate-command/contracts/migrate-cli.md#C-6
097-speckit-migrate-command/contracts/migrate-cli.md#C-7
097-speckit-migrate-command/contracts/migrate-engine.md#C-5
097-speckit-migrate-command/contracts/migrate-engine.md#C-8
```

  这 4 条正是 tasks.md § Notes「strict-subset green partition」披露的未认领条款（migrate-cli C-6/C-7、migrate-engine C-5/C-8），与披露逐条吻合；`4 of 25 FRs cited from citation groups` 同为该 Notes 披露的 contracts 侧引用组缺口（21/25 不可由 citation groups 读出），本阶段不设门、不改 contracts。

### implement 入口失败测试名列表（指针，不重述形式）

- 形式与路径所有者: `/speckit.implement` step 6 `**Test runs**` bullet（`--names-out <spec-dir>/baseline-failed.txt`，比较面 `comm -13`）。
- 本次入口捕获命令（逐字）:

```bash
bash scripts/bash/run-tests.sh --names-out .specify/specs/097-speckit-migrate-command/baseline-failed.txt -q
```

- 结果: 退出码 `1`（pytest failures）；`278 failed, 8262 passed, 2 skipped, 576 warnings in 43.58s`（parallel pass），serial 补跑 `1 passed, 8542 deselected in 18.88s`（`passes=2` 合成一份名单）；runner 落款 `# failed-name list written: .specify/specs/097-speckit-migrate-command/baseline-failed.txt (278 entries) passes=2`。
- 名单文件: `.specify/specs/097-speckit-migrate-command/baseline-failed.txt`（278 条，sorted/dedup）；全量输出记录: `test-evidence/implement-entry-baseline-suite.txt`。
- 说明: 该 278 条为入口既有红（本工作树基线状态），后续回归以名字级 `comm -13 baseline current` 证明零新增；名单形式与重跑义务归上一条 bullet，本文件只记读数与指针。
