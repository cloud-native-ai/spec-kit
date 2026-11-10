# U5 上送件 — 095-superagent-role（analyze 门二轮未清 HIGH）

**时间**: 2026-11-10T08:18Z · **线**: `095-superagent-role` · **run**: `r20261110T055657Z-b095`
**判定**: analyze 门一轮修复回环已用尽；第二轮仍 **CRITICAL 0 / HIGH 4** → 按规则停线（不可豁免，带病进 implement 会放大）。

## 1. 发现了什么（四条 HIGH，锚点见归并报告）

| ID | 一句话 |
|----|--------|
| W1-30 | `dual-role` 字面量双语义：集合形态机读标记（STR-002 / Key Entities / SC-001）与「已授予派发职责」声明值（FR-005）冲突，契约无法仅凭 token 判别 |
| W1-31 | SC-009 要求四类治理契约测试「全绿」，FR-036 完成门为「相对基线零新增失败 + 既有红豁免」；若基线含这四类红则两条不可同时满足 |
| W1-32 | W1-04 修复未扫全：SC-001 Source 与 US1 故事仍写「违例三类」，与 FR-005/US1 AS3/SC-001 的四类矛盾 |
| W2-13 | `unbacked-role-claim` 不可达或双重判红：载体声明域封闭为 `subagent | dual-role`，而该违例要求声明 `superagent`；C-9 又把已知表内未知值判 malformed → exit 2 |

完整事实与证据：`.specify/specs/095-superagent-role/test-evidence/analyze-merged-round2-2026-11-10.md` §0（44 行全表；MEDIUM 28 / LOW 12 一并呈报）。

## 2. 为何吃重

- 四条都跨制品且触及**语义裁定**（一个 token 的两种含义、两条完成门的取舍、四类违例的封闭集、一个违例的可达性），不是措辞修补；每条都要求 requirements ↔ contracts ↔ data-model ↔ tasks 同步改，改错一处会引入新矛盾。
- 规则门槛：analyze 门「同一门最多回环一轮」，第二轮仍 C/H 时**禁止豁免**——继续回环会违反门禁纪律，故停线而非第三轮。
- 多线并行背景：095 与三条新线（096/097/098）同时推进；095 的语义裁定需要人工口径，继续自动驾驶的边际收益低。

## 3. 已产生的中间产物（逐项可定位）

- 分支：`095-superagent-role`（HEAD `d5a372d45`）；工作树：主仓共享树（未建独立 worktree）
- 规格：`.specify/specs/095-superagent-role/{requirements.md, plan.md, tasks.md, data-model.md, quickstart.md, feature-ref.md, contracts/*, checklists/requirements-quality-2026-11-10.md}`
- 检查点：`checkpoints/01-requirements.md` … `05-checklist.md`
- 分析证据：`test-evidence/analyze-findings-W{1,2,3}.md`、`analyze-merged-2026-11-10.md`、`analyze-repair-dispositions-2026-11-10.md`、`analyze-repair-gates-2026-11-10.txt`、`analyze-findings-round2-W{1,2,3}.md`、`analyze-merged-round2-2026-11-10.md`
- 运行记录：各阶段 run records / receipts 已提交在分支上
- 状态脊：`.specify/state/095-superagent-role.md`（stalled；含全部框架观察 FO-095-01…09）
- Line registry：095 条目 `state=blocked`（reason 已记）

## 4. 可选处置

- **A（推荐）**：人工裁定四条 HIGH 的口径（dual-role 唯一语义、完成门唯一判据、四类违例封闭集、unbacked-role-claim 可达性），落一次聚焦修复后**重开 analyze 门一次**（需你显式授权突破「一轮」上限，作为有记录的裁定）。
- **B**：095 停在 Blocked，先让 096/097/098 三条线推进；095 择日带口径重启。
- **C**：若判定 095 目标可由后续特性覆盖（如 sdd-observer 需要 095 的角色模型），可将 095 归档并在 096 中吸收其定义。

## 5. 用户裁定（访谈 D-095，2026-11-10）

- **重启该线**。重启的具体形态（从哪个阶段、修复范围、是否授权重开 analyze 门一次）见访谈第 2 轮 D-095-R 的裁定。

- 补充裁定（D-095-R）：授权按建议修复 4 条 HIGH 并重开 analyze 一次；同时确立规则「无人值守 SDD 的 analyze 门自主修复续环，不中断等待用户确认」，写入用户决策判定门（confirmation-gates）并约束今后所有 analyze 门。
