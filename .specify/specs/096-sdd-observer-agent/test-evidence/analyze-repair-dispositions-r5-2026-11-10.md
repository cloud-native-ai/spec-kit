# Analyze repair dispositions — 096-sdd-observer-agent — r5 — 2026-11-10

- **Round**: analyze 门第四轮失败后的自主修复轮（单写者，无人值守；修复后续跑 analyze 门）
- **Input**: `test-evidence/analyze-merged-r4-2026-11-10.md` §1（W13-17，HIGH；本轮输入面 0 CRITICAL / 1 HIGH）
- **Category quadruple**: `flow_class=execution`；`source=declaration`；`marker=`（空）；`error=`（无）
- **Scope of this round**: W13-17 的完成门记录载体统一 —— `tasks.md` GATE-4（载体 + 披露）、`tasks.md` § Notes（框架链注记）、`.specify/features/096.md` § Status Criteria（核对）；框架级反馈条目 1 条；证据 = 本文件 + `test-evidence/analyze-repair-gates-r5-2026-11-10.txt`
- **No-reject statement**: 唯一待处置项 confirm 并 fixed，无 reject、无静默丢条。

## Decision — 单一可执行载体 `verification.md`（要求 1）

**选择**：方案 A —— 本线统一按框架实施链的 `verification.md` 执行，不用双载体。理由（按可判定性排序）：

1. **唯一机器判据只认 `verification.md`**：`scripts/python/closure-acceptance-check.py:87` 的 `REQUIRED_INPUTS` 含 `verification.md`——缺它即 `EXIT_INPUT`，状态翻转门不可能通过；`templates/commands/implement.md:60` 明言 checker「reads `SC-NNN_status=` rows in `REQUIREMENTS_DIR/verification.md` and nothing else」。
2. **`verification.log` 默认不可提交**：`git check-ignore -v` 实测根 `.gitignore:37` 的 `*.log` 命中该路径（exit 0；同目录 `verification.md` exit 1），且没有任何任务行声明 force-add——双载体方案会让「宪法字面记录」成为未跟踪残件。
3. **条款 owner 同向**：`shared/workflow/acceptance-hardening.md:46`（四条件第 2 条）、`templates/verification-log-template.md`（词汇 owner）、`.specify/features/096.md:49` 均写 `verification.md`；`verification.log` 面只剩 `.specify/constitution.md:223` 的字面与 `shared/guidelines/better-harness.md:27/39` 的示例名。

**披露（行内，与 GATE-4 同处）**：「宪法 VII 的 `verification.log` 字面由框架级统一裁定（反馈已登记：`.specify/memory/feedback/20261110T124821Z-skill-sdd-loop-driver.md`），本线按框架链执行（唯一载体 `verification.md`，即 `templates/verification-log-template.md` 与 `closure-acceptance-check.py` 的输入名）。」

## Disposition

| Finding | Verdict | Fixed | Anchors (post-repair) | One-line reason |
|---------|---------|-------|-----------------------|-----------------|
| W13-17 (HIGH) | confirm → fixed | yes | `tasks.md:33`（GATE-4：两处记录载体改为 `verification.md`；Condition owners 保留宪法 § VII 的 every-SC 语义、不再复述旧字面；行尾追加 Disclosure）; `tasks.md:379`（§ Notes 新增载体注记：框架链唯一输入名 + `.gitignore:37` 排除事实）; `.specify/features/096.md:49`（核对为 `verification.md`，已与所选载体一致，未改）; `.specify/memory/feedback/20261110T124821Z-skill-sdd-loop-driver.md`（新增框架级反馈条目） | 完成门记录载体收敛为 `verification.md`：与 closure checker 的 `REQUIRED_INPUTS`、implement 模板、acceptance-hardening、词汇 owner 及 features 状态标准面一致；`verification.log` 字面按「框架级统一裁定」披露并登记反馈，本线不写该文件（`*.log` 被 `.gitignore` 排除），GATE-4 与状态翻转门不再互斥。 |

**为什么不是双载体**：双载体要求 `verification.log` 以 force-add 落盘并新增任务行，但该文件对框架链零消费者（checker / review / analyze 只读 `verification.md`），却引入一个被 `.gitignore` 针对的并行记录面；两份记录一旦不一致，机器只读其中一份，与 W13-17 的根因同型。单载体 + 披露 + 反馈是「本线可执行且信息不丢失」的最小形态。

**刻意不改的两处（权威边界）**：

- `.specify/constitution.md:223` 的 `verification.log` 字面：宪法修订是独立治理动作（版本号 + Sync Impact Report），不是本 spec 的修复权域；本轮以反馈条目请求框架级统一裁定。
- 框架源（`shared/guidelines/better-harness.md:27/39` 等）：属框架仓的 source hat，改动须走框架流程；已作为附加证据写入反馈条目。

## Framework feedback entry（要求 2）

- **ID**: `20261110T124821Z-skill-sdd-loop-driver`（path: `.specify/memory/feedback/20261110T124821Z-skill-sdd-loop-driver.md`）
- **Owner**: `skill:sdd-loop-driver`；`unit_type=skill`；`run_id=096-sdd-observer-agent-analyze-repair-r5-20261110`；`feature=096-sdd-observer-agent` / `feature_id=096`；probe 归属 `skill-sdd-loop-driver-cli-profile`（引擎解析，非调用方自设）。
- **三方冲突（条目正文记载）**：宪法 VII（`.specify/constitution.md:223`，`verification.log`）× 根 `.gitignore:37`（`*.log` 默认排除）× 框架实施链（`acceptance-hardening.md:46`、`implement.md:50/58/60`、`closure-acceptance-check.py:87`、`verification-log-template.md`，全部 `verification.md`）；附加证据 `shared/guidelines/better-harness.md:27/39` 仍以 `verification.log` 作示例传感器名。
- **建议裁定**：宪法 VII 字面改为 `verification.md`（与既有机器判据、词汇 owner、实施模板同向），并同步 `better-harness.md:27/39`；若坚持 `.log` 名称，则须同时修订 acceptance-hardening / implement 模板 / closure checker / verification-log-template 并为根 `.gitignore` 加例外——两者取舍已写入条目 Optimization Points。

## In-passing notes（仅披露）

- `.specify/features.md` / `.specify/features/096.md` 均无 `verification.log` 引用；G 面（registry 内容级）无需改动。
- 本轮未触碰其余 24 MEDIUM / 26 LOW 开放项（W13-18、W3-11 等），保持原状交后续轮次。
- `.specify/.tmp/096/feedback-review-r5.md` / `-points-r5.md` 为本次反馈引擎的临时输入，位于受制裁临时根 `.specify/.tmp/`，非交付物。

## Gate re-runs

全文见 `test-evidence/analyze-repair-gates-r5-2026-11-10.txt`（运行于工作树 HEAD `4c34b2c1f` + 未提交修复）：

- `validate-requirements.py` → `status: ok`，6 标签全 pass，0 error / 0 warning（254 行 / 30 定义行 / 3 shared strings），exit 0
- `pre-analyze-check.py --stage requirements` → `decision: pass`，0 error（82 advisory 均为本特性待创建路径），exit 0
- `pre-analyze-check.py --stage plan` → `decision: pass`，0 error（82 advisory 同上），exit 0
- `pre-analyze-check.py --stage tasks` → `decision: pass`，0 error（tasks=47 不变），exit 0
- `decomposition-check.py --mode tasks` → `decision: proceed`（23 FR / 47 tasks，低于上限 120/160），exit 0
- supporting：`validate-tasks.py` → `0 error(s), 4 warning(s)`，exit 0（4 条警告与 r3/r4 完全一致 = 3 green-cross-phase + 1 green-path-divergence，全部仍在 § Green Attribution disclosed-warnings 表内）
- supporting：`account-clause-coverage.py` → `status: ok`、claimed clauses 58、FR 23/23、uncovered beyond baseline 0，exit 0（`[clause-unparsable] 107` 为语料级既有警告，非本轮引入）

**Anomaly**: none —— W13-17 已处置并留痕；框架级反馈条目已落盘；修复后全部 7 项门禁 exit 0，可直接续跑 analyze 门。
