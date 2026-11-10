# Analyze repair dispositions — 096-sdd-observer-agent — r3 — 2026-11-10

- **Round**: analyze 门第二轮失败后的自主修复轮（单写者，无人值守；修复后续跑 analyze 门）
- **Input**: `test-evidence/analyze-merged-round2-2026-11-10.md`（CRITICAL 1 / validated HIGH 3；四行全部经校验波 confirm，见该报告 § Validator evidence boundaries）
- **Scope of this round**: `tasks.md` 的定点修复（四行同指「门 → 行 → 证据」闭合，S7 建议按条配对修复）；证据 = 本文件 + `test-evidence/analyze-repair-gates-r3-2026-11-10.txt`
- **No-reject statement**: 四条待处置全部 confirm 并 fixed，无 reject、无静默丢条。

| Finding | Verdict | Fixed | Anchors (post-repair) | One-line reason |
|---------|---------|-------|-----------------------|-----------------|
| W3-07 (CRITICAL) | confirm → fixed | yes | `tasks.md:30`（GATE-1：`git check-ignore -q .specify/.tmp && mkdir -p .specify/.tmp/096` 前置 + `--names-out .specify/.tmp/096/current-names.txt`，比较命令同路径；文末注明 scratch 停留在受制裁仓库内根 `.specify/.tmp/`，不再提裸系统临时目录） | 门禁文本不再指示任何 MUST 违反：落点改为 `temp-directory-discipline.md` §1 表列受制裁根 `<project>/.specify/.tmp/<purpose>/`，并按 §3 在首次写入前校验 `.gitignore` 忽略（该仓库 `.specify/.gitignore:30` 已含 `.tmp/`，`git check-ignore` 实测命中）；全文件已无裸 `/tmp` 字样。 |
| W3-08 (HIGH) | confirm → fixed | yes | `tasks.md:22`（DoD-6 改为基线指涉式包含性声明）; `tasks.md:37`（GATE-8 补 `<implement-entry-base>..HEAD` 四路径 diff）; `tasks.md:42`（§ Environment Prerequisites 定义 **implement-entry base** = 实现入口 `git rev-parse HEAD`，DoD-6/GATE-8/T032 唯一引用点）; `tasks.md:111`（T004 记录 base sha）; `tasks.md:211`（T032 增基线 diff + 结构不变量） | 三个载体的「unchanged」现在有具名基线参照物（实现入口提交 sha，T004 落盘于 `test-evidence/env-probe.txt`），检查从工作树对索引的裸 `git diff` 改为 `<base>..HEAD` 路径限定 diff（对已提交变更不再失明）；比较单元覆盖 `STAGE_ARTIFACTS` 的双面载体（声明载体 `driver-stage-artifacts.yaml` + `loop-state.py` 内联回退表），T032 另钉结构不变量（mapping stage keys == stage-sequence `statement`；obligations 页保留 `## 十一 · 零新增机制` 标题），满足 closed-set-claims 要件 1/2/4。 |
| W3-09 (HIGH) | confirm → fixed | yes | `tasks.md:24`（DoD-8 点名两条重测行与两个证据落点）; `tasks.md:68`（§ Premises 引言给出落点）; `tasks.md:111`（T004 扩展：11 个计数/token 前提按各自 re-derivation 命令重测，value/delta/command 落 `test-evidence/premises-entry.txt`） | DoD-8 的重测义务现在有真实任务行（T004 覆盖 11 个 count/token 前提、T002 覆盖 3 个 guard-baseline 前提，合计 14/14）与证据落点，无需把 DoD-8 收窄；选择扩展 T004 而非新增 Setup 行，任务总数保持 47（decomposition 读数不变），且 T004 已携带 `[P]`、与 T002/T003 写面互不重叠（parallel-safe 无新告警）。 |
| W3-10 (HIGH) | confirm → fixed | yes | `tasks.md:120`（Foundational Purpose 改为指引句）; `tasks.md:122`（CRITICAL 改为「行级 `[blockedBy:]` 是唯一顺序权威」）; `tasks.md:161`（T014 增 T006：tamper fixture 读取格式事实）; `tasks.md:263`（Phase Dependencies 同口径收敛） | 按指令建议统一为单一顺序权威：`blockedBy` 标签是包内唯一排序权威，Foundational 的「故事行不得先于两者齐备」从规则降为指引，不再与行级标签形成两条互相矛盾的规则；同时给 T014 补齐语义上真实需要的 T006 边（tamper 变体依赖 T006 拥有的封闭事件类集合；校验波亦确认该依赖），T036 仅读 fixture builder 故保留 T007 单边，T018/T023 的其余边由已声明包序承载（wp02/wp03 在 wp01 之后）。 |

**Gate re-runs**（全文见 `test-evidence/analyze-repair-gates-r3-2026-11-10.txt`，HEAD `60c78e773`）：

- `validate-requirements.py` → `status: ok`，0 error / 0 warning，exit 0
- `pre-analyze-check.py --stage requirements` → `decision: pass`，0 error（82 advisory 均为本特性待创建路径），exit 0
- `pre-analyze-check.py --stage plan` → `decision: pass`，0 error，exit 0
- `pre-analyze-check.py --stage tasks` → `decision: pass`，0 error（tasks=47 不变），exit 0
- `decomposition-check.py --mode tasks` → `decision: proceed`（23 FR / 47 tasks，均低于上限 120/160），exit 0
- supporting：`validate-tasks.py` → `0 error(s), 4 warning(s)`，exit 0（4 条警告与上轮完全一致 = 3 green-cross-phase + 1 green-path-divergence，全部仍在 § Green Attribution disclosed-warnings 表内）
- supporting：`account-clause-coverage.py` → `status: ok`、claimed clauses 58、FR 23/23、uncovered beyond baseline 0，exit 0（`[clause-unparsable] 107` 为语料级既有警告，非本轮引入）

**In-passing notes（仅披露）**：

- W3-08 的载体集在 finding 所列三路径外增加了 `shared/declarations/facts/driver-stage-artifacts.yaml`：`STAGE_ARTIFACTS` 映射存在声明载体与引擎内联回退表两个面，比较单元必须同时覆盖，否则两处可各自漂移；四路径均为整文件基线 diff，判据不因覆盖面扩大而含糊。
- W3-09 未触碰 W3-05 后继关系之外的 MEDIUM/LOW 项；本轮其余 MEDIUM/LOW（W3-11…W3-17、W1-*、W2-*）保持原状，交后续轮次。

**Anomaly**: none —— 四条全部处置并留痕，无 reject、无静默丢条；修复后全部门禁 exit 0，可直接续跑 analyze 门。
