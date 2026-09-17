# Quickstart: 面向用户可理解性纪律(Feature 051)

**Date**: 2026-09-17  
**Purpose**: 6 个验证场景,覆盖规格的 5 个 User Story 与 18 条 Success Criteria。

**执行核验声明**(依 `/speckit.plan` 的 Post-Generation Quality Gate):本文件中**每一条可在今天执行的命令都已于 2026-09-17 实跑**,其"期望结果"取自实跑输出而非意图。依赖尚未落地制品的命令按**逐条**标注(不是文件级免责声明)——文件级免责声明会为它未覆盖的命令作保。

**改前基线汇总**(全部实测):

| 量 | 改前实测值 | 改后期望值 |
|---|---|---|
| 门控扫描 `total` | **23** | 23(不变) |
| 门控扫描 `violations` | **0** | 0 |
| `shared/guidelines/*.md` 文件数 | **11** | 12 |
| `templates/instructions-template.md` 的 `## ` 章节数 | **17** | 18 |
| `.specify/instructions.md` 的 `## ` 章节数 | **18** | 19 |
| `templates/constitution-template.md` 原则数 | **11** | 13 |
| `.specify/memory/constitution.md` 原则数 | **14** | 15 |
| 8 个规则真源文件的指针数 | **0 / 8** | 8 / 8(各 1 行) |
| `grep -c "One Source"` 于两个宪章模板文件 | **0 / 0** | 1 / 1 |
| `sync-mirrors.py --check`(全树) | **EXIT=0** | EXIT=0 |
| `regen-command-copies.py --check` | **EXIT=0** | EXIT=0 |
| `pytest tests/contract/ -q` | **24 failed, 1924 passed** | 失败集 ⊆ 基线(见场景 6) |

---

## 场景 1 — 真源文档存在且镜像逐字节相等(US1 / SC-003)

```bash
cd /storage/project/cloud-native-ai/spec-kit
ls -l shared/guidelines/user-facing-comprehension.md .specify/shared/guidelines/user-facing-comprehension.md
cmp shared/guidelines/user-facing-comprehension.md .specify/shared/guidelines/user-facing-comprehension.md && echo "BYTE-IDENTICAL"
ls -1 shared/guidelines/*.md | wc -l
```

**期望**: 两个文件均存在;输出 `BYTE-IDENTICAL`(`cmp` 静默即相等);guideline 文件数 = **12**。

> *本场景的三条命令依赖尚未创建的真源文档,改前实跑会报 `No such file or directory`。改前可实跑的等价基线是 `ls -1 shared/guidelines/*.md | wc -l` → **11**。*

**改前已实跑的镜像基线**(全树,不限于本文件):

```bash
python3 scripts/python/sync-mirrors.py --check
```

**实测输出(EXIT=0)**:
```
ok    templates/ == .specify/templates/ (22 files)
ok    skills/ == .specify/skills/ (489 files)
ok    agents/ == .specify/agents/templates/ (2 files)
ok    scripts/ == .specify/scripts/ (104 files)
ok    shared/ == .specify/shared/ (40 files)
```
另有 18 条非致命 `note  extra file only in mirror:`(17 × `.specify/skills/.migration-backups/layout-int-*/SKILL.md`,1 × `browser-utils/scripts/js/.temp-execution-*.js`)——镜像侧独有文件对非 strict 对只是提示,不影响退出码。⇒ **改前基线全绿**,故本特性可用绝对判据。

---

## 场景 2 — 常驻章节抵达活动指令文件(US1 / FR-003 / FR-038)

```bash
grep -c '^## User-Facing Comprehension' templates/instructions-template.md .specify/templates/instructions-template.md .specify/instructions.md
grep -c '^## ' templates/instructions-template.md
grep -c '^## ' .specify/instructions.md
```

**期望**: 三条 `grep -c '^## User-Facing Comprehension'` 各输出 **1**(两份模板 + 活动指令文件各含且仅含一次);模板章节数 **17 → 18**;活动文件章节数 **18 → 19**(活动文件多出的一个是项目自有的 `## Recurring Operational Lessons`,增量调谐容忍它)。

> *`grep -c '^## User-Facing Comprehension' …` 改前实跑输出 `0`(文件不存在时 grep 报 `No such file or directory`)。上表中的 17 / 18 两个章节计数为**改前实跑值**。*

**位置窗口核验**(新章节 MUST 不在被钉死的窗口内):

```bash
grep -n '^## ' templates/instructions-template.md
```

**改前实测章节顺序**: `Project Overview`(3) → `Documentation Map`(8) → `Proactive Flow Trigger`(24) → `Fact, Correctness & Logic Checks (Input Sanity)`(34) → `One Source Of Truth`(49) → `Task Complexity Rubric`(59) → `Token Efficiency Discipline`(65) → `Dogfooding Practice`(73) → `Two Hats`(82) → `Ask, Record, Repeat`(94) → `Tech Stack & Resources`(106) → `Suggested Tooling Scope`(122) → `AI Tool Compatibility`(135) → `Spec Kit Framework Map`(139) → `Spec Kit Runtime & Symlink Model`(145) → `Git Workflow`(151) → `Skills & Tools`(154)。

**期望(改后)**: `## User-Facing Comprehension` 出现在 `Token Efficiency Discipline` 之后、`Dogfooding Practice` 之前;`Documentation Map` → `Proactive Flow Trigger` → `Fact, Correctness & Logic Checks` 三者的相邻关系**不变**。

**悬空指针遍历核验**(FR-038 / SC-017,覆盖全部 guideline 而非只覆盖新文档):

```bash
grep -oE '\.specify/shared/guidelines/[a-z0-9-]+\.md' .specify/instructions.md | sort -u | while read -r p; do
  s="shared/guidelines/$(basename "$p")"
  [ -f "$s" ] && echo "ok   $s" || echo "MISSING  $s"
done
```

**期望**: 全部输出 `ok`,零 `MISSING`。改前实跑该命令对既有 11 份 guideline 全部 `ok`(窗口今天尚未被触发,但**从未受测**——这正是 SC-017 要把它变成受测项的理由)。

---

## 场景 3 — 门控预算不变(US2 / SC-012,本特性最硬的门禁)

```bash
python3 scripts/python/scan-confirmation-gates.py; echo "EXIT=$?"
python3 scripts/python/scan-confirmation-gates.py --baseline .specify/specs/044-reduce-confirmation-flows/baseline.json; echo "EXIT=$?"
```

**改前实测输出**(两次均 EXIT=0):
```
blocking confirmation gates: 23
  destructive: 13
  governance_kept: 10
violations (reversible gates still blocking): 0
```
第二次另含一行 `baseline delta total: -70`。

**期望(改后)**: 三次数字**逐字不变** —— `total 23`、`destructive 13`、`governance_kept 10`、`violations 0`、`EXIT=0`。任何 +1 都会同时打爆 `test_confirmation_gates_sweep.py::test_residual_total_within_sc002_target`(cap = 93 × 0.25 = 23.25)与 `test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged`(钉死 `== 23`)。

**扫描器未被改动的核验**(FR-032 的条件前提不成立 ⇒ 零代码改动):

```bash
git diff --stat HEAD -- scripts/python/scan-confirmation-gates.py src/specify_cli/__init__.py scripts/
python3 - <<'PY'
import importlib.util, pathlib
spec = importlib.util.spec_from_file_location("scg", "scripts/python/scan-confirmation-gates.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print("BLOCKING_PATTERNS:", len(m.BLOCKING_PATTERNS))
print("POLICY_DOCS:", [str(p) for p in m.POLICY_DOCS])
print("SELF_REL:", str(m.SELF_REL))
PY
```

**期望**: `git diff --stat` 输出为空;`BLOCKING_PATTERNS: 17`;`POLICY_DOCS` 恰为 `['shared/patterns/reconcile-pattern.md', 'shared/patterns/interview-pattern.md']`;`SELF_REL` 为 `shared/guidelines/confirmation-gates.md`。

> *上面 `importlib` 片段中的 `BLOCKING_PATTERNS` 条数 **17** 是本轮实测值(需求阶段误记为 18,已订正)。该片段本身在改前即可实跑。*

---

## 场景 4 — 8 行指针接入 11 类界面(US2 / US4 / US5 / SC-004)

```bash
for f in shared/guidelines/confirmation-gates.md \
         shared/workflow/feedback-step.md \
         shared/patterns/interview-pattern.md \
         templates/commands/clarify.md \
         shared/guidelines/requirements-guidelines.md \
         shared/guidelines/proactive-trigger.md \
         skills/summarize-project/references/reporting-playbook.md \
         shared/workflow/glossary.md; do
  printf '%s  %s\n' "$(grep -c 'shared/guidelines/user-facing-comprehension.md' "$f")" "$f"
done
```

**改前实测输出**(8 行全为 0):
```
0  shared/guidelines/confirmation-gates.md
0  shared/workflow/feedback-step.md
0  shared/patterns/interview-pattern.md
0  templates/commands/clarify.md
0  shared/guidelines/requirements-guidelines.md
0  shared/guidelines/proactive-trigger.md
0  skills/summarize-project/references/reporting-playbook.md
0  shared/workflow/glossary.md
```

**期望(改后)**: 8 行全为 **1**(每文件含且仅含一行指针;SC-004 的"各含且仅含一行")。

**判据冻结与保留项核验**(FR-017 / FR-019 / FR-021):

```bash
grep -c '非阻塞\|自动传输' shared/guidelines/confirmation-gates.md
sed -n '125,126p' shared/patterns/interview-pattern.md
grep -c 'never paste the raw' shared/workflow/feedback-step.md
grep -c '读者用语纪律' skills/summarize-project/references/reporting-playbook.md
```

**期望**: 第 1 条 ≥1(`:68` 收敛后 MUST 仍含 `非阻塞` 与 `自动传输` 两个字面量,否则既有 `test_confirmation_gates_execution_report.py:44-46` 转红);第 2 条输出 `interview-pattern.md:125-126` 的两条模式特有规则**原文**(每问一决策 / 问 what 不问 whether);第 3 条 ≥1(`feedback-step.md` 既有规则保留未删);第 4 条 ≥1(`:309` 落盘门禁仍在,尽管 §1.7 正文已收敛为指针)。

---

## 场景 5 — 下游双落点导出(US3 / SC-005 / SC-015)

**5a. 机械核验(可在 shell 执行)**

```bash
grep -cE '^### [IVXLC0-9]+\.' templates/constitution-template.md
grep -cE '^### [IVXLC0-9]+\.' .specify/memory/constitution.md
grep -c 'One Source' templates/constitution-template.md templates/commands/constitution.md
grep -c '\*\*MUST include\*\* a principle for' templates/commands/constitution.md
grep -n '\*\*Version\*\*' .specify/memory/constitution.md
```

**改前实测输出**:
```
11
14
templates/constitution-template.md:0
templates/commands/constitution.md:0
5
215:**Version**: 1.11.0 | **Ratified**: 2026-01-30 | **Last Amended**: 2026-08-31
```

**期望(改后)**: `11 → **13**`;`14 → **15**`;两个模板文件的 `One Source` 命中各 `0 → **1**`(STR-006 回流,闭合"无下游项目收到它"的缺口);`MUST include` 条目 `5 → **7**`;版本行 `1.11.0 → **1.12.0**`(MINOR,依 `templates/commands/constitution.md:66`)且 `Last Amended` 更新为落地日期。

**5b. 动态枚举传导(FR-026 要求实测验证,不靠假定)**

```bash
grep -n 'Do NOT hard-code principle names' templates/plan-template.md
grep -nE '^### <roman-or-arabic-numeral>|roman-or-arabic-numeral' templates/plan-template.md
```

**期望**: 两条均命中(`plan-template.md:37` 与 `:38-39`)⇒ Constitution Check 门控按 `### <numeral>. <name>` **动态枚举**,故 `plan-template.md` **零改动**即自动纳入两条新原则;`git diff --stat HEAD -- templates/plan-template.md` MUST 输出为空。

**5c. 端到端下游演练(agent 驱动,非 shell 管线)**

> *本子场景**无法**作为一条 shell 管线执行:`/speckit.constitution` 与 `/speckit.plan` 是聊天指令而非终端命令(见 `AGENTS.md` 的 "`/speckit.*` commands are chat instructions, not terminal commands")。以下步骤 MUST 由 agent 在一个临时目录中逐步驱动,每步的判定点已给出可实跑的 shell 核验命令。本文件不对 `specify init` 的副作用(例如是否创建指令文件符号链接)作任何断言——该行为未经本轮实测。*

> **环境前提(2026-09-17 实测,tasks 阶段探测)**:本机 `specify` 为 `/usr/local/bin/specify`,版本 **0.0.22**,安装在 `/usr/local/lib/python3.11/site-packages/specify_cli/__init__.py`——**不是本工作树的可编辑安装**(`python3 -c "import specify_cli; print(specify_cli.__file__)"` 的路径不在仓库内)。而 `specify init --help` 明写"Use local templates (GitHub download is no longer supported)",即 init 用的是**已安装包内**的模板。⇒ 直接跑本子场景验证的是 0.0.22 的模板,**不是本特性的改动**。要让本子场景有效,MUST 先从本树重装(`python3 -m pip install -e .` 或 `pip install .`);该动作会改动全局 site-packages 安装,属**需先征得同意**的操作。替代路径:以 **5a + 5b 的机械核验**作为本特性导出能力的验收证据,把 5c 记为 `[~]` 延后并在 `verification.md` 写明理由。

1. 在仓库外建临时目录;**先按上面的环境前提从本树重装 CLI**(`python3 -m pip install -e .`,会改动全局 site-packages,需先征得同意),再执行 `specify init`(安装形态依 `docs/tutorials/installation.md`)。**未重装则本子场景验证的是已发布的 0.0.22 模板,对本特性无证明力。**
2. 核验真源文档已随 init 抵达:`ls <tmp>/.specify/shared/guidelines/user-facing-comprehension.md`。
3. 由 agent 执行 `/speckit.constitution`。核验:`grep -c 'User-Facing Comprehension' <tmp>/.specify/memory/constitution.md` → **≥1**;`grep -c 'One Source of Truth (Authority & Reference Discipline)' <tmp>/.specify/memory/constitution.md` → **≥1**;`grep -n '\*\*Version\*\*' <tmp>/.specify/memory/constitution.md` 的版本符合 `x.y.z.ddd` 且文件头部含 Sync Impact Report。
4. 由 agent 执行 `/speckit.plan` 至 Constitution Check 一节。核验:该表行数 == `grep -cE '^### [IVXLC0-9]+\.' <tmp>/.specify/memory/constitution.md`,且表中含两条新原则各一行。
5. 反向核验拒绝路径:若该项目判定某原则与其领域无关而依 `templates/commands/constitution.md:40-41` 拒绝,则该拒绝 MUST 出现在 Sync Impact Report 中(`grep -c 'Sync Impact Report' <tmp>/.specify/memory/constitution.md` → ≥1),MUST NOT 静默丢弃。

---

## 场景 6 — 收敛、镜像与测试基线(US5 / SC-003 / SC-016)

**6a. 单源扫描(38 处内容形态复述 → 0)**

```bash
python3 -m pytest tests/contract/test_user_facing_comprehension_doc.py \
                   tests/contract/test_user_facing_comprehension_section.py \
                   tests/contract/test_user_facing_comprehension_pointers.py \
                   tests/contract/test_constitution_double_landing.py -q
```

**期望**: 全部通过。其中 `surface-pointers.md` C-13 的单源扫描断言 `shared/` + `templates/` + `skills/` 下内容形态复述数为 **0**(豁免:真源文档自身、机械副本、测试钉死字面量)。

> *这四个测试文件由本特性新建,改前不存在,故改前实跑报 `file or directory not found`。*

**6b. 既有测试扩展(FR-034)**

```bash
python3 -m pytest tests/contract/test_confirmation_gates_execution_report.py -q
```

**期望**: 通过。该文件被扩展以断言 `confirmation-gates.md` 携带指针(其既有用例 `:44-46` 只断言 `非阻塞` 与 `自动传输`,不含 `用户视角途径` 子句——这正是 FR-034 要补的守卫缺口)。

**6c. 镜像与再生**

```bash
python3 scripts/python/sync-mirrors.py --check; echo "EXIT=$?"
python3 scripts/python/regen-command-copies.py --check; echo "EXIT=$?"
```

**改前实测**: 两者均 **EXIT=0**(`sync-mirrors` 输出见场景 1;`regen-command-copies` 输出 `OK: all per-tool command copies match the source templates.`)。

**期望(改后)**: 两者仍 **EXIT=0**。这要求实现同批完成:`sync-mirrors.py --write`(同步 `.specify/shared/`、`.specify/templates/`、`.specify/skills/`)与 `regen-command-copies.py`(再生 4 棵按工具命令树)。`tests/contract/test_scripts_distribution_parity.py:71-87` 对**全树**跑该检查并断言 `returncode == 0`,故任何一处镜像缺失都使 CI 红。

**6d. 全量契约套件与失败基线**

```bash
python3 -m pytest tests/contract/ -q 2>&1 | tail -3
```

**改前实测**: `24 failed, 1924 passed in 38.28s`。

**期望(改后)**: 失败集 ⊆ {049 冻结基线 47 条} ∪ {`test_specify_script_paths.py::TestSpecifyScriptPaths::test_review_prerequisite_flags_are_supported`}。后者因本分支尚无 `tasks.md` 而失败(`check-prerequisites.sh:248-250` 只在文件存在时才把 `tasks.md` 放进 `AVAILABLE_DOCS`),`/speckit.tasks` 生成后**自愈,无需改任何源码**。任何**新增**失败 ID 即本特性引入的回归。

**6e. 文档空间(手写源收敛,生成物不手改)**

```bash
grep -c 'plain-language title\|Plain language, your vocabulary' docs/reference/commands/interview.md
grep -c 'never the raw engine path' docs/reference/skills/feedback.md
grep -c 'business stakeholders, not developers' docs/reference/commands/requirements.md
git ls-files docs/public | wc -l
```

**期望**: 前三条在收敛后降为指针形态(计数下降,具体值由实现期测定并记入 `verification.md`);第四条实测为 **0** —— `docs/public/**` 是 Hugo 构建产物、未被 git 跟踪(经 `docs/.gitignore` 忽略;证据 `skills/create-pages/references/hugo-site.md:22` "Never committed, never documentation"),故 MUST NOT 手工编辑,修好手写源后由既有 create-pages 流程重建。

---

## 场景 → SC 覆盖对照

| 场景 | 覆盖的 Success Criteria |
|---|---|
| 1 | SC-003(真源 1 份)、SC-010(中立性,由 C-15 断言) |
| 2 | SC-009(常驻章节守卫)、SC-017(悬空指针遍历) |
| 3 | SC-012(门控计数不变)、SC-011(零新机制) |
| 4 | SC-004(8/8 指针)、SC-013(`:68` 提升后获断言)、SC-016(搬家零回归) |
| 5 | SC-005(下游双落点 + 动态枚举)、SC-015(观察名单守卫) |
| 6 | SC-003(38 → 0)、SC-014(黑名单提升)、SC-016(既有基线不恶化) |

**不由 shell 场景覆盖、需人工评审的 SC**:SC-001(门控提示抽样,需未参与实现的评审者)、SC-002(引擎调用形态泄漏,由 C-13 单源扫描 + 人工抽样双轨)、SC-006(双评审者一致率 ≥90%,需 ≥20 条样本盲测)、SC-007(建议行零膨胀,改前后长度分布比对)、SC-008(裁决顺序齐备,由 C-12 断言 + 人工确认无空白类)、SC-018(读者基准声明总数 ≤3,由 C-13 断言)。这六条的度量方法记在规格 `### Measurement Sources & Collection Methods`,实现期结果落 `verification.md`。
