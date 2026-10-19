# Quickstart: Humanize Command（人性化改写命令）

**Feature**: 062 | **验证基准日**: 2026-10-19（基线=实现前实跑留痕）
**执行验证纪律**: 本文件每条命令示例都按 `/speckit.plan` Post-Generation Quality Gate 的 execution-verify 规则处置——已实跑的粘贴真实输出；未实现的示例**逐条**声明免责与前提清单，免责不覆盖未点名的示例。

## S1 — 按工具副本生成面基线（已实跑）

```bash
python3 scripts/python/regen-command-copies.py --check
```

实跑输出（2026-10-19，全量留痕 `notes/baseline-regen-check.txt`）：

```text
OK: all per-tool command copies match the source templates.
```

解读：生成面当前零漂移——本特性新增 `templates/commands/humanize.md` 后，`--check` 的预期形态是「除新增 humanize 副本落位并保持一致外，其余副本零变化」。

## S2 — 镜像对基线（已实跑，相对判据）

```bash
python3 scripts/python/sync-mirrors.py --check
```

实跑输出（2026-10-19，全量留痕 `notes/baseline-mirror-check.txt`，共 209 行 DIFF；构成实测：`skills/internal` 75 文件、`skills/draw-diagram` 36、`scripts/python` 17、`shared/guidelines` 12、`shared/workflow` 11、`shared/definitions` 10（其中第 181 行即本特性**触碰对** `probe-definitions.md`）等）：

```text
DIFF  .specify/shared/workflow/glossary.md
DIFF  .specify/shared/workflow/interview-walkthrough.md
DIFF  .specify/shared/workflow/objective-analysis-gate.md
...（共 209 条）
DIFF  .specify/shared/definitions/probe-definitions.md   ← 第 181 行：本特性触碰对，基线已漂移
DRIFT detected — run: python3 scripts/python/sync-mirrors.py --write
```

解读（两档判据，不得混用）：
- **不触碰对**：209 条既有漂移先于本规格存在，绝对全绿判据不可写；判据取相对形式——零 NEW drift。
- **触碰对**：
  - `skills/external/humanize/` ↔ `.specify/skills/humanize/` 为**新增对**，落位时须字节一致；
  - `shared/definitions/probe-definitions.md` ↔ `.specify/shared/definitions/probe-definitions.md` **基线已漂移**（第 181 行），对已被触碰的对「零 NEW drift」无判别力——实现期判据为特性限定同步（`--only` 该前缀）后**绝对字节一致**，且同步不拖入其他对的变更。

## S3 — Wrap-up 编译面基线（已实跑，相对判据）

```bash
python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check
```

实跑输出（2026-10-19，节选）：

```text
compile-embeds drift in 73 of 73 units (--check; nothing written):
- /speckit.analyze
- /speckit.checklist
- ...
```

解读与判据修正（纠正级，已在 plan § Phase 0 披露）：
- 73/73 全部为「旧指纹渲染」类可再生漂移（引擎语义：recompile 修复），先于本规格存在——「零漂移」绝对判据在本基线上不可通过（2026-10-16 的 060 记录的是 zero drift，其间注册表指纹发生过变化）。
- 单元构成实测（`notes/baseline-compile-check.txt` 逐行）：**73 = 23 个 Complex 命令 + 50 个技能**。humanize 命令按 027 分类规则（(a)(b)(c) 逐条不命中）为 **Simple**——不注册命令单元；技能侧新增 `skill:humanize` 一个单元。实现后总数 = **74**（23 + 51）。
- `--unit` 参数**不限定** compile-embeds 的检查/写入范围（`notes/baseline-compile-unit-no-scope.txt`：传入单单元仍报 73/73，与本行结论同源）。
- 实现期判据取相对形式：新增 `skill-humanize-wrapup` 单元注册后其编译面落位且带当前指纹；本特性对既有 73 个单元的编译面**零新增漂移归因**；`compile-embeds --write` 的全局重写溢出（既有欠账的顺带修复面）不属本特性产物、不并入本特性提交（按 Artifact Commit 纪律作为上游偏差披露）。

## S4 — 测试基线冻结（已实跑）

```bash
bash scripts/bash/run-tests.sh --names-out .specify/specs/062-humanize-command/notes/baseline-failed-tests.txt
```

实跑输出（2026-10-19，全量日志 `notes/baseline-test-run.txt`——仓库 `*.log` 忽略约定下的可提交形态）：

```text
=========== 71 failed, 3929 passed, 3 warnings in 157.37s (0:02:37) ============
# failed-name list written: .specify/specs/062-humanize-command/notes/baseline-failed-tests.txt (71 entries)
```

解读：71 个失败节点全部为 master 既有欠账（主体为镜像字节一致类，与 S2 的 209 条 DIFF 同源；含 `test_compile_propagation_order` 两项，与 S3 同源）。SC-008 的非回归判据：实现后同命令复跑，`comm -13 notes/baseline-failed-tests.txt <new-list>` 为空（零新增失败节点）；既有失败数允许减少（欠账被顺带修复），不允许增加。

## S5 — 契约条款与 FR 覆盖（已实跑）

```bash
python3 -c "
import sys; sys.path.insert(0,'.specify/scripts/python')
from clause_extract import extract_clauses
total=0
for f in ['command-surface.md','rewrite-behavior.md','tone-input-file.md']:
    p='.specify/specs/062-humanize-command/contracts/'+f
    cs=extract_clauses(p)
    total+=len(cs)
    print(f, len(cs), (cs[0]+'..'+cs[-1]) if cs else 'NONE')
print('TOTAL', total)
"
```

实跑输出（2026-10-19）：

```text
command-surface.md 10 C-1..C-10
rewrite-behavior.md 13 C-11..C-23
tone-input-file.md 11 C-24..C-34
TOTAL 34
```

FR 覆盖自检（`clause_blocks` 逐条款正文检索 FR 引用）实跑输出：

```text
covered: 28 missing: NONE
```

## S6 — 需求规格校验器（已实跑）

```bash
python3 .specify/scripts/python/validate-requirements.py .specify/specs/062-humanize-command/requirements.md
```

实跑输出（2026-10-19）：

```text
status: ok
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] pass (0)
  [marker-count] pass (0)
  [dup-id] pass (0)
scanned: 244 lines, 38 definition rows, 3 shared strings
0 error(s), 0 warning(s)
```

## S7 — 传播次序端到端（实现期场景，逐例免责）

**免责（仅覆盖本场景，不外溢）**: 以下多步管线在命令与技能落盘前**无法执行**——`/speckit.humanize` 尚不存在，`skill-humanize-wrapup` 单元未注册。此免责即本场景对「命令尚不可运行」的全部声明范围；S1–S6 的已实跑示例不在免责内。

**前提清单（实现期须逐项复测而非继承）**:
1. `probe-definitions.md` 接受 `skill-wrapup` 类单元行与 `h-docs-sync-eval` 绑定行（既有 50 个技能同型行在册，2026-10-19 实测形态一致）；humanize 命令为 **Simple**，不注册命令单元（027 分类规则）。源侧编辑落点为框架源 `shared/definitions/probe-definitions.md`（两顶帽子：镜像经步骤 4 同步）。
2. `compile-embeds` 对「目标文件存在 + 单元已注册」的新技能单元会创建其 `## Wrap-up` 节（`_replace_sections` 语义，实现期以落盘结果验证）。
3. `regen-command-copies.py` 从模板源生成 4 个副本（S1 已验证引擎工作正常，新命令副本形态为前提而非实测）。
4. `sync-mirrors.py --write --only <prefix>` 接受可重复的 repo-relative 前缀（`--help` 实测文档形态：`--only scripts/python/feedback-utils.py` 例），特性限定同步不拖入无关漂移。
5. 评估场景 S8 依赖 `tests/fixtures/humanize/` 语料与 `rubric.md`（随实现落盘，本 plan 只定义布局契约）。

管线步骤（固定次序：注册 → 编译 → regen → sync，AGENTS.md Probe System 行）：

```bash
# 1) 编辑框架源（两顶帽子——全部改源侧，镜像由步骤 4 承载）：
#    shared/definitions/probe-definitions.md  加入 skill-humanize-wrapup 单元行 + h-docs-sync-eval 绑定行（命令侧零单元）
#    templates/commands/humanize.md           新命令模板（薄入口，Simple：无 Wrap-up、无 probe 单元）
#    skills/external/humanize/SKILL.md        执行技能（含待编译的 Wrap-up 骨架或由步骤 2 创建）
# 2) 编译 Wrap-up 面（全局写入；溢出面按 S3 判据处置）
python3 .specify/scripts/python/probe-utils.py --action compile-embeds
# 3) 生成按工具副本
python3 scripts/python/regen-command-copies.py
# 4) 特性限定镜像同步（--only 可重复；模板→副本委派仅在前缀命中 templates/commands/ 时触发，本步前缀不命中故由步骤 3 承载）
python3 scripts/python/sync-mirrors.py --write --only skills/external/humanize --only shared/definitions/probe-definitions.md
# 5) 复核（相对判据见 S1–S3；证据逐单元隔离）
python3 scripts/python/regen-command-copies.py --check
python3 scripts/python/sync-mirrors.py --check | grep -E 'humanize|probe-definitions' || echo "touched pairs: zero DIFF"
python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check
```

**证据逐单元隔离（S7 复核面的判定形态）**:
- `compile-embeds --check` 的全局输出按单元逐行留存——本特性证据只取两条：`skill:humanize` **不出现**于 drift 名单（新单元已编译到当前指纹），以及「当前 drift 名单相对基线 `notes/baseline-compile-check.txt` 的**新增集合为空**（`comm -13 <基线单元名> <当前单元名>`）」（既有漂移允许被顺带修复而减少，不允许新增归因）。
- `sync-mirrors --check` 只取 `humanize` 与 `probe-definitions` 两个触碰对的行（期望零命中）；`skills/external/humanize` 为新增对，落位后须字节一致。
- 测试套件证据只取 `comm -13 notes/baseline-failed-tests.txt <新名单>`（零新增失败节点），不因既有欠账减少而放宽。

**Teardown**: 本管线无清理步骤——`sync-mirrors --write --only <pair>` 为幂等同步，无状态残留；步骤 2 的全局溢出面的处置（提交或还原）按 S3 判据与 Artifact Commit 纪律执行，不属于「残留待清理」状态。若引擎动作参数前提不成立（如 `--only` 不接受该路径形态），实现期须先查引擎 `--help` 再执行，不得在报错后猜测参数。

## S8 — 改写行为评估（实现期场景，逐例免责）

**免责（仅覆盖本场景）**: 四维度改写行为、语气矩阵、文件安全行为在命令落盘前无法运行。以下为验证形态声明，非可执行命令。

**前提清单**: S7 的管线已完成（命令可被宿主加载）；E8 语料与 `rubric.md` 已落盘；两位独立评审可用。

验证形态（对 E8 语料逐样本）：
1. 内联样本：按 `rubric.md` 量规由两位独立评审独立判定四维度（C-11..C-15）；受保护内容由确定性差异脚本比对（C-16、C-17；改变数=0、编造数=0）。
2. 文件样本：临时目录内执行，运行前后逐字节哈希比对源文件与未获确认的输出目标（C-30、C-31）；测试自身的临时目录清理步骤同样纳入验证（teardown 与 setup 同标准）。
3. 长文档样本：章节对应性与完整性报告检查（C-20；SC-006）。
4. 全部记录落 `verification.md`（/speckit.implement 产出）。
