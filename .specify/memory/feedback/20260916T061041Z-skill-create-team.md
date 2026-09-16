---
id: "20260916T061041Z-skill-create-team"
unit_id: "skill:create-team"
unit_type: "skill"
run_id: "20260916T060815Z-speckit-team-run-draw-two-layer-structure"
scope: "local"
probe: "skill-create-team-wrapup"
kind: "internal"
slice: "skills"
feature: "draw-two-layer-structure"
partial: false
created: "2026-09-16T06:10:41Z"
summary: "run 模式 serial 链首跑:S1-refactor 两次派发均撞 15 轮上限,gate 判 FAIL(六技能只覆盖 1 个),链停在 S1、S2/S3 保持 locked,canonical 零改动。按 failure_strategy retry-once-then-escalate 走完并 escalate。四项机制缺陷:serial stage 粒度与派发预算无对齐要求(根因,16"
---

## Review
run 模式 serial 链首跑:S1-refactor 两次派发均撞 15 轮上限,gate 判 FAIL(六技能只覆盖 1 个),链停在 S1、S2/S3 保持 locked,canonical 零改动。按 failure_strategy retry-once-then-escalate 走完并 escalate。四项机制缺陷:serial stage 粒度与派发预算无对齐要求(根因,162 文件 vs 单次派发实测 1 技能)、verify-territory-disjoint.py 自比较假阳性使 exit-4 规则落盘后不可用、Stage Execution Protocol 无「多次派发累积同一 stage 产物」的说法、run 五项检查依赖的三个引擎函数无 CLI 入口(只能 importlib 手调且首次签名猜错)。实跑成立的部分:Worker/Meta 写权限分离两次派发都守住、territory.forbidden 显式列举有效、交接门拦住假绿。token-efficiency:一次全额子代理预算换来零产物,长 brief 必须要求增量落盘。

## Optimization Points
- # /speckit.team run 优化点（draw-two-layer-structure serial chain，2026-09-16）
- **[根因·stage 粒度] serial stage 的工作量与单次派发预算之间没有任何对齐要求，缺陷只能在运行时暴露。**
- 本次 S1-refactor 覆盖六个技能共 **162 个文件**（mermaid 60 · plantuml 52 · excalidraw 25 ·
- echarts 13 · d3js 9 · draw-diagram 3）。实测单次 Worker 派发在 **15 轮**预算内完成 **1 个技能**
- （mermaid，80 条归属）。S1 需约 5–6 次派发，而 team.md 把它定义为单 stage = 单次派发 →
- Attempt 1 零产物、Attempt 2（brief 收窄到只做 ownership map + 逐技能增量落盘）仍只拿到 1/6，
- quality gate 条款 1「六个技能归属清单齐全」判 FAIL，链在 S1 停住。
- `create-mode.md` 步骤 5（build the pattern config）与 `patterns.md` 的 Serial Chain 段都**没有**
- 要求按受影响文件规模校验 stage 粒度。建议：serial/parallel 的每个 stage 在落盘前对其 `outputs`
- 涉及的目录做一次文件计数，超过单次派发可承载规模即要求拆分（或在 team.md 里显式声明
- 「本 stage 由 N 次派发累积完成」）。这与 AGENTS.md「重构命令/引擎后必须端到端跑真实管线」
- 那条教训同形——静态检查看不出来，一跑就炸。
- **[引擎缺陷] `verify-territory-disjoint.py` 存在自比较假阳性，使 exit-4 规则在落盘后不可用。**
- 命令规定「exit 4（任何 overlap/undecidable）→ 披露争用区、人工改划后重跑或移交
- `/speckit.goal coordinate`，MUST NOT 静默落盘已知重叠」。但校验集定义为
- 「提议团队 ∪ 同 `goal_slug` 既有团队（从磁盘读）」，且**不按 slug 去重**：
- 团队落盘后再拿它自己的 territory 做提议重跑，必然得到
- `{"a": "draw-two-layer-structure", "b": "draw-two-layer-structure", "verdict": "overlap"}` → exit 4。
- 本次即如此（落盘前 `exit 0 / 0 pairs`；改 territory 后重跑 `exit 4 / pairs 1 / overlap 1`，
- contested 列出全部 9 条 write 路径）。照字面执行规则会永久卡死任何已落盘团队的 territory 复核。
- 建议：构造成对比较时跳过 `a.slug == b.slug` 的自比较对（提议与磁盘同 slug 视为同一方，取并集或
- 以提议覆盖），或在输出里把这类对标为 `self` 而非 `overlap`。
- **[协议缺口] serial 的 Stage Execution Protocol 写的是「INVOKE: Spawn subagent」（单数），
- 没有「一个 stage 的产物可由多次派发累积」的说法。**
- 本次 Attempt 2 正是靠增量落盘让第二次派发接续第一次的产物（虽仍不足量），但协议里找不到依据，
- 我只能自行判定这算同一 stage 的重试而非两个 stage。建议在 protocol 里明确：retry 与
- 「多次派发累积同一 stage 产物」是两种不同处置，前者受 `failure_strategy` 约束，
- 后者需在 team.md 显式声明。
- **[引擎暴露缺口] run 模式五项检查所依赖的三个函数没有 CLI 入口。**
- 命令明写「the engine parse of `goal-utils.py`（`parse_goal` / `preview_target_check`）is the single
- source of truth for every judgment below — never re-derive it in prose」，但 `goal-utils.py` 的
- action 只有 create / validate / check-statement / list / status / criteria / migrate / targets，
- **没有**暴露 `resolve_effective_target` 或 `preview_target_check`。我只能用 importlib 加载模块
- 手调函数，且第一次因签名猜错（`resolve_effective_target(team_md_path, explicit_target)` 而非
- `(repo_root, slug, target)`）抛 TypeError。建议增一个 `run-checks <team-slug> [--target <ref>]`
- action，一次输出五项检查的 JSON verdict（含 `{effective, source, declared_focus}` 与 goal 终态判定），
- 让「判定归引擎」这条规矩在 run 路径上真的可执行。
- **[token-efficiency] 一次全额子代理预算换来零产物。**
- Attempt 1 的 brief 覆盖 ownership map + patch-set + sequencing + evaluation-form probe 设计，
- 烧满 15 轮后**零文件落盘**——这是本次可避免的消耗主体（量化口径：1 次完整子代理派发预算，
- 产出 0 字节）。Attempt 2 靠「逐技能增量落盘、最重的先做」把同样预算换成了 1/6 的有效产物，
- 这条经验值得进 create-team 的派发纪律：**长 brief 必须要求增量落盘**，否则轮次耗尽即全损。
- 另：本报告与 progress 文件均由确定性事实（文件计数、gate 逐条判定、git status）支撑，
- 未编造 Token 数值。
- ## 实跑中成立的部分（非问题，供对照）
- **Worker/Meta 写权限分离在两次派发中都成立**：`git status --short skills/ shared/ templates/ .specify/shared/` 全空，
- 子代理没有任何越界写 canonical 的行为。
- **territory.forbidden 的显式列举有效**：pre-flight 收窄 `shared/definitions/**` → 具体文件后，
- `write ∩ forbidden = ∅`，且 S1 的 gate 从不可达变为可达（虽因粒度问题仍未通过）。
- **交接门拦住了不合格的推进**：S1 gate FAIL → S2/S3 保持 locked，没有出现「文件存在/标题齐备就算过」
- 那类假绿。
