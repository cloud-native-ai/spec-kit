# Analyze repair dispositions — 096-sdd-observer-agent — r4 — 2026-11-10

- **Round**: analyze 门第三轮失败后的自主修复轮（单写者，无人值守；修复后续跑 analyze 门）
- **Input**: `test-evidence/analyze-merged-r3-2026-11-10.md`（carried C/H = 0；新增 CRITICAL W13-01（宪法 VII 记录面）+ HIGH W2-01（C-09/V-16 可执行性，同面较轮 2 的 W2-04 升档））
- **Category quadruple**: `flow_class=execution`；`source=declaration`；`marker=`（空）；`error=`（无）
- **Scope of this round**: `tasks.md` 记录面按宪法 VII 对齐（W13-01）；`contracts/journal-engine.contract.md` C-07/C-09 与 `data-model.md` V-16 的可执行性收敛（W2-01）；证据 = 本文件 + `test-evidence/analyze-repair-gates-r4-2026-11-10.txt`
- **No-reject statement**: 两条待处置全部 confirm 并 fixed，无 reject、无静默丢条。

| Finding | Verdict | Fixed | Anchors (post-repair) | One-line reason |
|---------|---------|-------|-----------------------|-----------------|
| W13-01 (CRITICAL) | confirm → fixed | yes | `tasks.md:60`（§Task State Sigil：`[~]` 延迟原因改为行内 `<!-- deferred: reason -->`）; `tasks.md:33`（GATE-4：记录载体改为 `verification.log`，判定面改为**每个** SC 均有 `SC-NNN_status=` 状态行，另保留 final-path pass 与 smoke 字段；条件 owner 拆分为宪法 VII〔记录完备 + zero-open 由 GATE-3 承载〕与 `acceptance-hardening.md` § Gates / § Verification Vocabulary〔final-path pass、smoke 字段〕，仍为「本行承载检查、不另立 schema」）; `tasks.md:381`（§Notes：延迟原因同为行内注释） | tasks.md 的完成门与延迟约定现与宪法 VII 逐字对齐（`:223` `verification.log` + every SC；`:224` 行内 `<!-- deferred: reason -->`），三处记录面（GATE-4 / Sigil / Notes）同步无残句；全 spec 的非证据面已无 `verification.md` / `deferred_tasks=` 引用。宪法文本与框架 owner 链（`acceptance-hardening.md:46` 仍写 `verification.md`、`feature-integration.md` Pre-Status-Flip 第 4 项仍要求 `deferred_tasks=`）之间的漂移是本轮之外的框架级宪法修订项，按 finding 的 evidence_not_supported 照实披露、不在本 spec 内稀释。 |
| W2-01 (HIGH) | confirm → fixed | yes | `contracts/journal-engine.contract.md:55`（C-09：`check` 规则集改为 V-1…V-13 与 V-17；明示 V-16 不在其内——追加时拒绝规则、由 `append` 按 C-07 执行，`check` 无执行身份可评）; `contracts/journal-engine.contract.md:43`（C-07：点名为 V-16 的唯一执行点）; `data-model.md:160`（V-16 标注为 append-time 规则、`check` 不评估）; `tasks.md:168`（T017 `check` 实现行同步为 V-1…V-13 与 V-17 + V-16 由 append 承担的说明） | 采用「把 V-16 归回 `append` 并从 `check` 移除」分支：V-16 语义上需要**调用方执行身份**，只读 checker 不持有该输入，声明输入无法弥合；且同页 V-14（并发拒绝）已是「append 时执行、不在 `check` 规则集」的同型先例，收敛后 `check` 的规则集与输入面自洽可执行。C-07/C-09/data-model V-16 三处同步，T017（规则集的实现落点）一并收敛，无残留 `V-16…V-17` / `V-16/V-17` 表述。 |

**In-passing notes（仅披露）**：

- T017 的同步是 W2-01 的必要闭合面而非扩面：该行逐字枚举 `check` 实现的 V 规则集，若只改 C-09 会留下「契约去掉 V-16、任务行仍要求 V-16」的新不一致。
- W13-01 的修复面按 finding 记载含「analyze 之外的独立宪法修订」一环（宪法 `verification.log` vs 框架 owner 链 `verification.md` 的词汇漂移，S1）；本轮按指令只做 tasks.md 侧对齐，框架侧修订保持 open，交框架维护流程处置，不视为本 spec 的残项。
- 本轮未触碰其余 MEDIUM/LOW 项（W13-02…W13-16、W2-02…W2-13 中除 W2-01 外的各行、以及 W1/W3 波既有项），保持原状交后续轮次。

**Gate re-runs**（全文见 `test-evidence/analyze-repair-gates-r4-2026-11-10.txt`，运行于工作树 HEAD `14a7da094` + 未提交修复）：

- `validate-requirements.py` → `status: ok`，6 标签全 pass，0 error / 0 warning（254 行 / 30 定义行 / 3 shared strings），exit 0
- `pre-analyze-check.py --stage requirements` → `decision: pass`，0 error（82 advisory 均为本特性待创建路径），exit 0
- `pre-analyze-check.py --stage plan` → `decision: pass`，0 error（82 advisory 同上），exit 0
- `pre-analyze-check.py --stage tasks` → `decision: pass`，0 error（tasks=47 不变），exit 0
- `decomposition-check.py --mode tasks` → `decision: proceed`（23 FR / 47 tasks，均低于上限 120/160），exit 0
- supporting：`validate-tasks.py` → `0 error(s), 4 warning(s)`，exit 0（4 条警告与 r3 完全一致 = 3 green-cross-phase + 1 green-path-divergence，全部仍在 § Green Attribution disclosed-warnings 表内）
- supporting：`account-clause-coverage.py` → `status: ok`、claimed clauses 58、FR 23/23、uncovered beyond baseline 0，exit 0（`[clause-unparsable] 107` 为语料级既有警告，非本轮引入）

**Anomaly**: none —— 两条全部处置并留痕，无 reject、无静默丢条；修复后全部门禁 exit 0，可直接续跑 analyze 门。
