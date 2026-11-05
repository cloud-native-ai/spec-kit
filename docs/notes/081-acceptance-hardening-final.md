# 更严格的验收与产物审查：Feature 081 最终成果

**状态**：`Ready for Review`（2026-11-03）
**严格门禁**：`accept`，exit 0，`final_path 2/2 pass`，无 reason
**合并**：`master` @ `506adf88`；特性分支 `081-acceptance-hardening`

## 结论

Feature 081 把 spec-kit 的 `Implemented` 从「任务勾完 + 每条 SC 有一行状态」收紧为「每条 `final` 路径 SC 为 `pass` + 一条确定性最小 smoke 记录在案」，并把「本能力由某仓提供」收紧为 requirements 的运行时栈／依赖所有权表与 plan 的执行前提／继承 blocker 表；review 从「恰好两段」改为**过程 → 产物 → 实现 → 代码四段 + 一次确定性 Acceptance Reality Check**。081a–081d 四个切片全部收口，feature 级读数如下。

| 读数 | 结果 |
|---|---|
| 闭环判定 | `accept`，exit 0，`final_path pass=2 / blocked=0 / deferred=0 / partial=0 / fail=0 / unknown=0 / total=2` |
| 全量测试 | `39 failed / 7134 passed / 7 skipped`；`head − baseline = 0`（0 new），`baseline − head = 0`（0 fixed） |
| final smoke | 同一命令两次 exit 0/0；证据文件 byte-identical |
| 镜像与副本 | `sync-mirrors.py --check` 与 `regen-command-copies.py --check` 均 exit 0 |
| schema guard | `tests/contract/test_acceptance_schema_ownership.py` 9 passed |

39 个失败是既有基线（归其他切片），本特性既未新增也未修复它们；这一区分由 id 级集合差证明，不由「全仓测试」这类聚合词替代。

## 四个切片

| 切片 | 交付 |
|---|---|
| **081a** | `Blocked` 一等状态与四条转移、verification 词表与五字段测量阶梯、`scripts/python/closure-acceptance-check.py`（accept/block + 封闭原因集 + `final_path` 六桶）、smoke 硬条件、implement 调用点 |
| **081b** | Runtime Stack & Dependency Ownership / Execution Premises / Inherited Blockers 三张强制表；四类确定性发现（`runtime-stack-row`、`runtime-contract-incomplete`、`premise-undecided`、`inherited-blocker`）；两个 producer 在**真实 plan 形状**上对拍 |
| **081c** | 四段 review + ARC、`review-feature-quality` 技能、review-template 槽位 `### 2.2`–`### 2.4`、review 调用点；用新组合对自身做 dogfooding 评审 |
| **081d** | `--audit-existing` 零写审计、driver line-state `blocked` + 八项处置、driver closure/merge 调用点（`closure-blocked` 与 `closure-input-error` 分置）、`manage-features` / feature-index 词表、schema-ownership guard、CHANGELOG、feature 级读数与状态落地 |

## Dogfooding 评审

081c 首次用新四段组合评审自身：P0=1（report slot 前言与 findings 表互相否定）、P1=4（analyze round-2 只裁 C/H 且 M/L 残留无机械载体、FR-015 追溯指向错误夹具、severity 定义两套、覆盖率回执无步骤产出）。P0/P1 全部修复后重跑，081d 最终评审 P0=0、P1=3（实现阶段代做 R4R 翻转、SC-009 两处矛盾陈述、detail 当前位过时），三条 P1 亦已修复；ARC 读 `agree`。

## 证据

| 证据 | 位置 |
|---|---|
| 状态脊 | `.specify/state/081-acceptance-hardening.md` |
| 验收日志 | `.specify/specs/081-acceptance-hardening/verification.md` |
| 最终评审 | `.specify/specs/081-acceptance-hardening/review.md` |
| 闭环载荷 | `.specify/specs/081-acceptance-hardening/test-evidence/closure-verdict-081d.json` |
| 基线对照 | `.specify/specs/081-acceptance-hardening/test-evidence/081d-final-baseline-2.txt` |
| 特性登记 | `.specify/memory/features/081.md` |

## 剩余具名缺口（未计 pass）

- **覆盖率车道**：`[fr-uncovered] fail (23)` — 25 条 FR 中仅 2 条从 citation group 引用；已作为具名 remainder 记录，未冒充绿色。补齐需要拥有 `contracts/` 的切片在条款块内引用 FR。
- **39 个既有基线失败**：归其他切片，不在本特性的允许差异集内。

## 可访问入口

- 代码与全部证据：`https://code.alibaba-inc.com/cloud-native-ai/spec-kit`（`master` @ `506adf88`）
- 独立展示版（内网静态托管）：https://xuanji-static.io.alibaba-inc.com/text/367c18340754f4ec38688d4cf3076c303a334c45.html
- 独立展示版源文件：`docs/static/reports/081-acceptance-hardening-final.html`
