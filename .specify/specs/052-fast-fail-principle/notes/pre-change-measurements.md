# 改前实测基线 (Pre-Change Measurements) — Feature 052

**Frozen by**: T001 (`/speckit.implement` Phase 1 Setup)
**Frozen at**: 2026-09-23
**Purpose**: 本特性所有比对型门禁的比对源。判据一律写成**相对**形态("触及的面上无新增漂移"),故本文件冻结的是**改前的漂移集本身**,不是"全绿"。

---

## ① BASE_SHA(字面值,不写 `HEAD`)

```
BASE_SHA=80a8c1fb0e27c70c797974affb8e88510558da19
branch=052-fast-fail-principle
```

派生命令:`git rev-parse HEAD` · `git rev-parse --abbrev-ref HEAD`

⚠️ 后续一切 `git diff` 比对 MUST 以该字面值为基线。CI 洁净检出下 `git diff HEAD` 恒为空真(空集 ⊆ 空集),用它做"零改动"判据是一次盲检。

---

## ② 镜像既有漂移集(`sync-mirrors.py --check`,逐 scope)

派生命令(逐 scope;⚠️ MUST 用 `rc=$?` 直接取脚本退出码 —— 管道到 `tail` 后 `$?` 是 `tail` 的,本轮实测踩过):

```bash
for s in shared agents templates skills; do
  out=$(python3 scripts/python/sync-mirrors.py --check --only "$s" 2>&1); rc=$?
  printf '%s EXIT=%s DIFF=%s\n' "$s" "$rc" "$(printf '%s\n' "$out" | grep -c '^DIFF')"
done
```

| scope | EXIT | DIFF 条数 | 冻结的 DIFF 集合 |
|---|---|---|---|
| `shared` | **2** | **2** | `.specify/shared/workflow/feedback-step.md`、`.specify/shared/workflow/runtime-mode.md` |
| `agents` | **0** | **0** | `ok    agents/ == .specify/agents/templates/ (2 files)` |
| `templates` | **2** | **2** | `.specify/templates/proactive-trigger-seed.json`、`.specify/templates/skills-template.md` |
| `skills` | **2** | **38** | 见下方完整清单 |

**判据(相对形态)**:改后重跑同一命令,`shared` MUST 仍为**这同 2 条**、`agents` MUST 仍为 `ok`、`templates` MUST 仍为**这同 2 条**、`skills` MUST 仍为**这 38 条的子集或相等**——即**无新增行**。写"EXIT=0 / 全绿"是发运一条在本仓不可通过的判据。

> **规划期缺口订正**:`plan.md` › Mirror Obligations 的基线段只记了 `shared`=2 与 `agents`=ok,**未冻结 `templates` 与 `skills` 两个 scope 的数目**;而 T017 / T024 / T034 都要对这两个 scope 判"无新增漂移"。本文件补冻,判据自此有比对源。

### `--only skills` 的 38 条既有 DIFF(完整清单)

```
.specify/skills/archive-session/SKILL.md
.specify/skills/code-review/SKILL.md
.specify/skills/collect-evidence/SKILL.md
.specify/skills/create-agent/SKILL.md
.specify/skills/create-docs/SKILL.md
.specify/skills/create-pages/SKILL.md
.specify/skills/create-skills/SKILL.md
.specify/skills/create-team/SKILL.md
.specify/skills/create-team/references/operating-loops.md
.specify/skills/create-team/references/summary-mapping.md
.specify/skills/create-team/references/team-presets.md
.specify/skills/create-tools/SKILL.md
.specify/skills/database-utils/SKILL.md
.specify/skills/document-utils/SKILL.md
.specify/skills/draw-d3js/SKILL.md
.specify/skills/draw-diagram/SKILL.md
.specify/skills/draw-drawio/SKILL.md
.specify/skills/draw-echarts/SKILL.md
.specify/skills/draw-excalidraw/SKILL.md
.specify/skills/draw-mermaid/SKILL.md
.specify/skills/draw-plantuml/SKILL.md
.specify/skills/git-fleet/SKILL.md
.specify/skills/git-server-init/SKILL.md
.specify/skills/git-submodule-edit/SKILL.md
.specify/skills/git-workflow/SKILL.md
.specify/skills/improve-agent/SKILL.md
.specify/skills/improve-docs/SKILL.md
.specify/skills/improve-skills/SKILL.md
.specify/skills/improve-skills/references/loop-playbook.md
.specify/skills/improve-team/SKILL.md
.specify/skills/improve-tools/SKILL.md
.specify/skills/manage-agents/SKILL.md
.specify/skills/memory-recall/SKILL.md
.specify/skills/memory-record/SKILL.md
.specify/skills/merge-skills/SKILL.md
.specify/skills/study-project/SKILL.md
.specify/skills/summarize-project/SKILL.md
.specify/skills/think-skills/SKILL.md
```

> 注:本特性 T030 / T032 会改 `skills/create-team/references/patterns.md` 与 `skills/create-agent/SKILL.md`。前者**不在**上述 38 条内(改前一致),故改后它 MUST 仍不出现;后者**已在**38 条内(改前即漂移),故改后它仍会出现——判据是"DIFF 集合无**新增**成员",不是"该文件从集合里消失"。

### `regen-command-copies.py --check` 既有待再生集

派生命令:`python3 scripts/python/regen-command-copies.py --check 2>&1 | grep -c '^  \.'`
实测:**84** 个文件待再生(首行 `DRIFT detected:`),含 `.github/prompts/*`、`.qoder/commands/*` 等。
**判据(相对)**:改后 `--check` 的待再生集 MUST **无新增**成员;本特性触及的 `speckit.constitution.*` 与 `speckit.agents.*` 副本 MUST 在再生后**离开**该集合。

---

## ③ 结构实测值(逐行携其派生命令)

| # | 前提 | 派生命令 | 实测值 | 改后期望 |
|---|---|---|---|---|
| 1 | `shared/guidelines/` 份数 | `ls -1 shared/guidelines/*.md \| wc -l` | **12** | 13 |
| 2 | `fast-fail.md` 是否已存在 | `test -f shared/guidelines/fast-fail.md && echo yes \|\| echo no` | **no** | yes |
| 3 | 指令模板 `## ` 节数 | `grep -c '^## ' templates/instructions-template.md` | **18** | 19 |
| 4 | 活动指令文件 `## ` 节数 | `grep -c '^## ' .specify/instructions.md` | **19** | 20 |
| 5 | 三个锚点章节行号 | `grep -n '^## Token Efficiency Discipline\|^## User-Facing Comprehension\|^## Dogfooding Practice' templates/instructions-template.md` | **66 / 74 / 86** | 递增,新章节落在 74 与 86 之间 |
| 6 | 宪章模板原则数 | `grep -c '^### [IVX]*\. ' templates/constitution-template.md` | **13** | 14 |
| 7 | 活动宪章原则数 | `grep -c '^### [IVX]*\. ' .specify/memory/constitution.md` | **15** | 16 |
| 8 | 命令 `MUST include` 条目数 | `grep -c 'MUST include' templates/commands/constitution.md` | **7** | 8 |
| 9 | 活动宪章版本 | `grep -oP '^\*\*Version\*\*: \K[0-9.]+' .specify/memory/constitution.md` | **1.12.0** | 1.13.0 |
| 10 | 出厂 Agent 预设份数 | `ls -1 agents/*.agent.md \| wc -l` | **2** | 2(不变) |
| 11 | Per-Agent Payload 字段行数 | `awk '/^Per-Agent Payload:/,/^Context Isolation Rules:/' skills/create-team/references/patterns.md \| grep -c '^| \`'` | **5** | 6 |
| 12 | UFC 类表规则真源路径数(去重) | 见下方脚本(口径同 `test_user_facing_comprehension_doc.py:394-397`) | **8**(8 个路径逐个 `is_file()` 为 True) | 9 |
| 13 | 门控扫描 `total` | `python3 scripts/python/scan-confirmation-gates.py \| head -1` | **blocking confirmation gates: 23**(destructive 13 / governance_kept 10) | 23(相等) |
| 14 | `BLOCKING_PATTERNS` / `POLICY_DOCS` / `SELF_REL` | importlib 载入取真(见下方脚本) | **17 / 2 / `shared/guidelines/confirmation-gates.md`** | 逐字不变 |
| 15 | 双落点四钉 | `grep -oE '(TEMPLATE_COUNT\|LIVE_COUNT\|COMMAND_COUNT) = [0-9]+\|MIN_VERSION = \([0-9, ]+\)' tests/contract/test_constitution_double_landing.py` | **13 / 15 / 7 / (1, 12)** | 14 / 16 / 8 / (1, 13) |
| 16 | UFC C-14 钉子 | `grep -o 'len(deduped) == [0-9]*' tests/contract/test_user_facing_comprehension_doc.py` | **8** | 9 |
| 17 | UFC C-18a override 上限 | `grep -o '<= 2' tests/contract/test_user_facing_comprehension_doc.py` | **2** | 2(不变) |
| 18 | 按工具命令树(4 棵) | `for d in .claude/commands .github/prompts .qoder/commands .opencode/command; do ls -1 "$d" \| wc -l; done` | **25 / 25 / 25 / 25** | 各 25(不变) |
| 19 | 按工具 agent 树 | `for d in .claude/agents .qoder/agents .github/agents .opencode/agent; do ls -1 "$d" 2>/dev/null \| wc -l; done` | **2 / 2 / 2 / 0** ⚠️ 见下方订正 | 四棵各 2 |

> ⚠️ **第 19 行的路径写错了,冻结值本身如实保留(它是当时那条命令的真实输出)**:第四个路径应为**复数** `.opencode/agents`,它改前即有 **2** 个受跟踪副本,故按工具 agent 树是**四棵**而非三棵。写错的后果不是"少数了一棵树"这么轻:T034 会据它少渲染一棵,而 `.github/agents` 的渲染键是 `copilot`(不是 `github`),`render_agents_for_tool` 对未知键**静默返回 `rendered: 0`**——两处叠加会让"渲染已执行"与"副本已更新"脱节,而命令都返回成功。实现期已实测四棵各 2 条目、8 个副本全部携一份字节相等的注入子句。
| 20 | 指令兼容性符号链接 | `for f in AGENTS.md CLAUDE.md QODER.md .github/copilot-instructions.md; do test -L "$f"; done` | **4** 条,均为 symlink(前三 → `.specify/instructions.md`,第四 → `../.specify/instructions.md`) | 仍为 4 条 symlink |
| 21 | 活动指令文件字节 / 预算 | `wc -c < .specify/instructions.md`;`sed -n '38p' scripts/bash/generate-instructions.sh` | **28168 / 32768**(余量 **4600**) | ≤ 32768 |
| 22 | 规格与契约规模 | `grep -c` 系列(见下) | FR **78** / SC **15** / STR **13** / 条款 **107** / quickstart 场景 **12** / data-model `## E` **19**、V **7**、S **3** | 条款仍 **107**(本文件的实现期订正只增子项,不增条款号) |

### 第 9 行的命令形态警告(本轮实测踩过)

裸 `grep -o '1\.[0-9]*\.[0-9]*' .specify/memory/constitution.md | head -1` 会命中 Sync Impact Report 的 `Version change: 1.11.0 →` 行而得 **1.11.0**(错);MUST 用锚定形态 `grep -oP '^\*\*Version\*\*: \K[0-9.]+'` 得 **1.12.0**(对)。

### 第 22 行的两个命令形态警告(本轮实测踩过)

- quickstart 场景数 MUST 用 `grep -c '^## 场景 [0-9]'`(得 **12**);`grep -c '^## 场景'` 会连 `## 场景覆盖表` 一起匹配(得 **13**,错)。
- data-model 实体标题是 `## E1`…**二级**标题,故用 `grep -c '^## E'`(得 **19**);`grep -c '^### E'` 得 **0**(错)。19 个标题覆盖 21 个实体(`## E5a / E5b` 与 `## E19a / E19b` 各为一对)。

### 第 12 / 14 行的取真脚本

```python
# 第 12 行:UFC 类表"规则真源文件"列去重路径数
import re, pathlib
t = pathlib.Path('shared/guidelines/user-facing-comprehension.md').read_text(encoding='utf-8')
paths = set()
for l in t.splitlines():
    if not l.startswith('|'): continue
    cols = [c.strip() for c in l.strip().strip('|').split('|')]
    if len(cols) < 4: continue
    for m in re.findall(r'`([^`]+\.md)`', cols[-2]): paths.add(m)
print(len(paths))            # -> 8
# 并逐个 pathlib.Path(p).is_file() 核验(pin hygiene 规则 2:表面文件清单 MUST 真实)

# 第 14 行:扫描器内部常量(importlib 取真,不重抄)
import importlib.util
spec = importlib.util.spec_from_file_location('s', 'scripts/python/scan-confirmation-gates.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(len(m.BLOCKING_PATTERNS), len(m.POLICY_DOCS), m.SELF_REL)   # -> 17 2 shared/guidelines/confirmation-gates.md
```

---

## ④ 门控基线与钉子集合

### 扫描器实跑

```
$ python3 scripts/python/scan-confirmation-gates.py | head -3
blocking confirmation gates: 23
  destructive: 13
  governance_kept: 10
scan-exit=0
```

冻结基线文件 `.specify/specs/050-proactive-flow-trigger/baseline-gates.json` 的 `confirmationGates` 节:
`total: 23` · `destructive: 13` · `governanceKept: 10` · `violations: 0` · `integerHeadroom: 0` · `cap: 23.25` · `capSource: .specify/specs/044-reduce-confirmation-flows/baseline.json (total 93) x 0.25`

### 钉住 `total` 的既有断言(**三处**,形态互不相同)

**唯一拥有者是 `contracts/gate-neutrality.md` C-10**;此处按 T001 的冻结义务记录实测位置与形态,不作为第二定义点。

| # | 位置 | 形态 | 改前状态 |
|---|---|---|---|
| 一 | `tests/contract/test_user_facing_comprehension_doc.py:557` | `assert payload["total"] == 23`(硬编码字面量) | 绿 |
| 二 | `tests/contract/test_proactive_trigger_section.py:352` | `assert payload["total"] == frozen["total"]`,`frozen` 取自 050 的 `baseline-gates.json` | 绿 |
| 三 | `tests/contract/test_confirmation_gates_sweep.py:162` | `assert payload["total"] <= cap`,`cap = baseline["total"] * 0.25`,`baseline` 取自 `.specify/specs/044-reduce-confirmation-flows/baseline.json`(`total: 93` ⇒ `cap = 23.25`) | 绿(`40 passed in 0.57s`) |

**已排除的第四处候选**:`tests/contract/test_scan_confirmation_gates.py:79` 的 `assert payload["total"] == 2` 是 **fixture 作用域**(`run_scanner("--root", str(tree))`,`tree` 为 `tmp_path`),与本特性新增文本无关,故**不是**钉子。把它算进去会造成一次错误的红归因。

> **实现期订正(记录根因)**:规划期各制品把该集合记为"两处 / 双重钉子"。第三处是**派生上限**形态,`grep '== 23'` 找不到它——按字面量搜索一个以不等式表达的约束,是本特性自己要点名的失效形态(盲检:检查返回绿,但其输出并不关于它被写来判定的命题)。已按 One Source of Truth 把 7 处重抄的数目改为指向 C-10 的指针,并把 `test_confirmation_gates_sweep.py` 补入 GATE-5 的运行集。

### 引擎与脚本零改动面(GATE-3 的比对源)

```bash
git diff --stat 80a8c1fb0e27c70c797974affb8e88510558da19 -- scripts/ src/specify_cli/ skills/create-team/scripts/ templates/plan-template.md
```
改前实测:**空**。改后 MUST 仍为空。

---

## ⑤ 名字级测试基线(T002)

派生命令:
```bash
bash scripts/bash/run-tests.sh --names-out .specify/specs/052-fast-fail-principle/baseline-failed.txt
```

实跑结果 @ 2026-09-23:

```
====== 76 failed, 2684 passed, 2 skipped, 3 warnings in 98.51s (0:01:38) ======
# failed-name list written: .specify/specs/052-fast-fail-principle/baseline-failed.txt (76 entries)
RUNNER_EXIT=1
```

| 项 | 值 |
|---|---|
| `baseline-failed.txt` 行数 | **76** |
| `sort -u` 后行数 | **76**(无重复,满足 `comm` 对输入已排序去重的要求) |
| runner 退出码 | **1**(pytest 自身的结果;runner 正确透传,未 fail-open) |
| runner 解释器探测 | **通过**——`run-tests.sh` 的 `resolve_python` 找到带 pytest 的解释器并跑出了 2762 个用例,故这是一份**真实基线**,不是"收集失败 ⇒ 空基线"的探针失败 |

**判据口径(MUST 按此判,不按条数)**:回归判据是

```bash
comm -13 .specify/specs/052-fast-fail-principle/baseline-failed.txt \
         .specify/specs/052-fast-fail-principle/current-failed.txt
```

**输出为空**,而**不是**"失败条数相等"。条数相等时失败集合仍可能已换手(旧的一处修好、新的一处坏掉,数目不变)——那是用计数掩盖了集合变化,属本特性要点名的盲检形态。

> **与 050 基线的差异(记录,不据此行动)**:`.specify/specs/050-proactive-flow-trigger/baseline-gates.json` 的 `testBaseline` 记的是 `failed: 43 / passed: 2496`。本轮实测 `76 / 2684`。差异来自 050 冻结之后进入本仓的既有失败(与 Feature 052 无关,本特性在 T002 之前未改动任何被扫描面)。这正是"每个特性冻结自己的基线"的理由——050 的文件自己也这么记(`049 baseline was 47; 5 pre-existing failures since fixed — this feature freezes its own`)。故本特性 MUST NOT 以 43 为判据,也 MUST NOT 去"修"这 76 条。
>
> 其中一条与本特性的再生面直接相关,预先点名以免实现期误归因:`tests/contract/test_user_facing_comprehension_pointers.py::test_c14_per_tool_copies_regenerated_and_retired_mirror_absent` —— 它因 `regen-command-copies.py --check` 的 **84** 项既有待再生漂移而红(见 ② 末),改前即红。T017 / T024 / T035 再生后它可能转绿(那会是**减少**,`comm -13` 不报),但 MUST NOT 因它而把判据改成"条数下降"。

---

## 环境探测(承 tasks.md › Environment Prerequisites,不重述结论)

python3 **3.11.11** · pytest **8.4.2** · bash 4.4.20 · git 2.43.5 · diffutils 3.6 · GNU Awk 4.2.1 · GNU sed 4.5 · GNU grep 3.1 · coreutils 8.30 — 均 @ 2026-09-23 实探。容器/集群/网络:**not required**。`specify` CLI 下游 bootstrap:**partial**(site-packages 非可编辑安装,同 Feature 051 的 T034 限制)。

## 可写性预探针(命令步骤 4)

`plan.md` 源码树与 Mirror Obligations 各行点名的 **25** 个目录逐个 touch-test:**全部 OK**,零 ENOENT、零 EACCES。
gitignore 准入:本运行预期写出的 9 个产物路径(`notes/*.md` ×4、`baseline-failed.txt`、`current-failed.txt`、`verification.md`、`shared/guidelines/fast-fail.md`、`tests/contract/test_fast_fail_discipline.py`)逐个 `git check-ignore -q` → **全部 admitted**;`implement-loop.local.md` → **ignored**(正确;长跑模式未激活)。

## 机械写入门禁(`.specify/gate.yaml`)

`.specify/gate.yaml` **存在**,故每个阶段的编辑前 MUST 跑 `gate-check.py` 并把判定回显。

- Phase 1 计划写入路径 ×2 → `allow` ×2,**GATE_EXIT=0**。
- ⚠️ **已预见的 CONFIRM**:`confirm:` 清单含 `.specify/memory/constitution.md`,即 **T022 的写入目标**。Phase 5 将返回 exit 1,届时 MUST 先取得用户明确同意再写,不得自行绕过。
