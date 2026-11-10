# U5 上送件 — 096-sdd-observer-agent（analyze 二轮未清 C/H）

**时间**: 2026-11-10T09:02Z · **线**: `096-sdd-observer-agent` · **run**: `r20261110T081104Z-b096`
**判定**: analyze 门一轮修复回环用尽；第二轮 **CRITICAL 1 / HIGH 3** 经独立只读验证 4/4 confirm → 按规则停线（不可豁免）。

## 1. 发现了什么（均经 fresh-context 验证）

| ID | 严重度 | 一句话 |
|----|--------|--------|
| W3-07 | CRITICAL | GATE-1 检查命令把 scratch 写到裸 `/tmp/096-current-names.txt`，违反临时目录纪律（宪法 XVII 把受制裁根委托给该 owner）——门禁文本本身指示了一次 MUST 违反 |
| W3-08 | HIGH | DoD-6/GATE-8/T032 的「unmodified/unchanged」包含性声明无基线指涉，检查是裸 `git diff --name-only`（对已提交变更失明）→ 声明 void |
| W3-09 | HIGH | DoD-8 要求 implement 入口重测全部 § Premises 量，但 11 个计数/token 前提无重测行与证据落点 |
| W3-10 | HIGH | Foundational「任何故事行不得在两者齐备前开始」与行级 `[blockedBy:]` 包内顺序权威矛盾；T014/T036 可在 T006 未闭合时启动 |

完整事实：`test-evidence/analyze-merged-round2-2026-11-10.md`；验证记录见其 § C/H 校验（sent 4 / confirm 4 / downgrade 0 / reject 0）。

## 2. 为何吃重

- W3-07 是门禁文本与宪法 MUST 的直接冲突；W3-08/W3-09/W3-10 是判据级（可测性、前提重测、顺序权威）问题，修复须动 DoD/GATE/tasks 三处。
- 按门禁规则第二轮仍 C/H 不得豁免。

## 3. 已产生的中间产物

- 分支：`096-sdd-observer-agent`；工作树：`.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent`
- 规格全链：requirements / plan / tasks / checklists / contracts×5 / data-model / quickstart / research / feature-ref
- analyze 证据：findings W{1,2,3}、merged 两轮、repair dispositions/gates、validation 记录
- 状态脊：`.specify/state/096-sdd-observer-agent.md`（stalled）；registry `state=blocked`

## 4. 可选处置

- **A**：人工裁定四条（GATE-1 换受治理临时根 / 包含性声明补基线或改写 / DoD-8 瘦身或补重测行 / 统一包内顺序权威），聚焦修复后授权重开 analyze 门一次。
- **B**：停在 Blocked，优先 098。
- **C**：把 096 缩到「agent 定义 + journal 引擎 + 生命周期契约」本体，DoD 判据随框架级反馈统一处置。

## 附：本线观察到的正向机制行为

- analyze 集成者**自行发起 4 个 fresh-context 只读验证 worker**（Recipe 7 载体），波后 `git status --porcelain` 逐字节一致 —— 090/093 的验证波与只读边界机制按设计工作。
- 修复轮能一次消除 4/4 validated HIGH（round-2 新增的是新面，旧面全 fixed）。

## 5. 用户裁定（访谈 D-096，2026-11-10）

- **按建议修复**：处置 1 CRITICAL + 3 HIGH，随后重开 analyze 门一次（本次为显式授权的门槛例外）。
