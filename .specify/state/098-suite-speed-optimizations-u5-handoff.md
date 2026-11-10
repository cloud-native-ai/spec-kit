# U5 上送件 — 098-suite-speed-optimizations（analyze 二轮未清 CRITICAL）

**时间**: 2026-11-10T09:20Z · **线**: `098-suite-speed-optimizations` · **run**: `r20261110T081104Z-b098`
**判定**: analyze 门一轮修复回环用尽；第二轮新增 **CRITICAL 1**（W1-01，validated，宪法冲突不可降级）、HIGH 0 → 按规则停线。

## 1. 发现了什么

| ID | 严重度 | 一句话 |
|----|--------|--------|
| W1-01 | **CRITICAL** | FR-007 的缺省档以 `slow` 标记排除换取更快运行，而 SC-004 又以「缺省档墙钟 ≤ 全量基线 50%」为 final 验收——正是宪法 XX / `test-execution-efficiency.md` L74/L93 明令禁止的「以标记排除换取数字下降」；修复后的 FR-021「MUST NOT 以该清单兑现任何 SC」与其自相矛盾 |

完整事实：`test-evidence/analyze-merged-round2-2026-11-10.md` §0（validation: direct re-read, validated/open）。
另：round-1 的 1C+7H 已全部 fixed 并经复核；round-2 在 requirements 域新发现此条，并带出任务域 9 条修复引入/未收敛的 MEDIUM/LOW。

## 2. 为何吃重

- 该 CRITICAL 是**目标定义级**冲突：提速目标（SC-004 的 50%）与覆盖保持纪律（宪法 XX）在需求层不可同时成立，必须重定成功判据（例如把 50% 目标限定在 `not slow` 选择内、或以墙钟/门数分离表述），不是措辞修补。
- 按门禁规则第二轮仍 C/H 不得豁免。

## 3. 已产生的中间产物

- 分支：`098-suite-speed-optimizations`；工作树：`.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations`
- 规格全链：requirements / plan / tasks / checklists / contracts×6 / data-model / quickstart
- analyze 证据：findings 两轮、merged 两轮、repair dispositions/gates
- 状态脊：`.specify/state/098-suite-speed-optimizations.md`（stalled）；registry 将置 blocked

## 4. 可选处置

- **A**：人工重定 SC-004 判据（把「≤50% 全量基线」改为「≤50% 同选择集基线」或按档位分离），随后授权重开 analyze 门一次。
- **B**：拆成两个特性（xdist/marker 档位机制 ← 与 缓存/去 sleep/直调 提速），分别验收。
- **C**：停在 Blocked，待框架级反馈（analyze 门判据摩擦）统一处置后再启。

## 5. 用户裁定（访谈 D-098，2026-11-10）

- **按建议修复**：重定 SC-004 判据使其与覆盖保持纪律相容，随后重开 analyze 门一次。
