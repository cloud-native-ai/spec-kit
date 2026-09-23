# Contract: 门控预算中立 (gate-neutrality)

**Feature**: 052 快速失败纪律(Fast Fail)  
**Guards**: `requirements.md` FR-036…FR-039, FR-064, FR-065, FR-078  
**Test files**: `tests/contract/test_fast_fail_discipline.py`(函数名 `test_gN_*`)、既有 `test_proactive_trigger_section.py:352`、既有 `test_user_facing_comprehension_doc.py:557`、既有 `test_confirmation_gates_sweep.py:162`(三者即 C-10 枚举的钉子集合)  
**Date**: 2026-09-23

条款号在本文件内独立编号;跨文件引用 MUST 写作 `gate-neutrality.md C-N`。

**为何本文件独立成一份**:门控预算的整数余量为 **0**,而本特性的全部新增文本都落在扫描面内。这不是一个附带约束,而是决定本特性能否落地的**硬门禁**——任何一行命中即同时打爆 C-10 枚举的**全部**既有钉子(其数目与形态由 C-10 单点拥有,此处不重抄)。故其条款集中一处,便于实现期逐条核验。

---

## 改前基线(2026-09-23 实测)

**C-1** 改前实跑基线 MUST 被冻结并记录,判据一律写成**相对**形态:

```
$ python3 scripts/python/scan-confirmation-gates.py
blocking confirmation gates: 23
  destructive: 13
  governance_kept: 10
violations (reversible gates still blocking): 0
```

**C-1(a) 上面这段引文 MUST NOT 被复制进任何被扫描的文件。** 实测(以 `importlib` 载入扫描器取真 `BLOCKING_RE` 逐行检验本契约文件):其首行 `blocking confirmation gates: 23` **命中** `confirmation gate` 模式。本文件位于 `.specify/specs/` 下、被 `SKIP_DIR_PARTS` 跳过,故此处引用安全;但 C-14 要求把"已接受代价"写进**真源文档**,而真源文档在 `shared/guidelines/` 下、**在扫描面内**——把这段扫描器输出原样贴进去会使 `total` 由 23 变 24,同时打爆 C-10 枚举的全部钉子。故真源文档载明该代价时 MUST 以**散文**表述(例如"因预算整数余量为零而取设计规避"),MUST NOT 引用扫描器的输出行。同一约束适用于本文件 C-7 逐条列出的 17 个模式字面量。

冻结基线文件 `.specify/specs/050-proactive-flow-trigger/baseline-gates.json`:`"total": 23`、`"destructive": 13`、`"governanceKept": 10`、`"integerHeadroom": 0`、`"cap": 23.25`。

**C-2** 扫描器 MUST **零改动**:`scripts/python/scan-confirmation-gates.py` 的 `POLICY_DOCS`(改前恰 **2** 项:`shared/patterns/reconcile-pattern.md`、`shared/patterns/interview-pattern.md`)、`SELF_REL`(`shared/guidelines/confirmation-gates.md`)、`len(BLOCKING_PATTERNS)`(改前 **17**)三者 MUST 与改前逐字一致。守卫形态为以 `importlib` 载入扫描器后断言这三个值,并断言 `git diff` 对该文件为空。

> **处置取设计规避,不扩大豁免集**(D-8)。房式先例:Feature 050 与 051 均取零命中 + 测试钉死;051 的 `plan.md:36` 明写 `scan-confirmation-gates.py 的 POLICY_DOCS **不修改**`。取舍依据(词汇表 `设计规避` 条):扩大豁免集会掩盖其中真实门控回流,豁免面过宽。

## 零命中的判据与范围

**C-3** 计数单位是**命中的行**,不是文件或门控:`scan()` 逐行 `if not BLOCKING_RE.search(line): continue` 后 `gates.append(…)`。故零命中的判据 MUST 逐行检查,而非逐文件。

**C-4** 扫描面 MUST 覆盖本特性**全部**新增文本(改前实测 `SCAN_DIRS = ("templates/commands", "skills", "shared")`、`SCAN_ROOT_FILES = ("templates",)`):

| 新增文本 | 所在路径 | 是否被扫描 |
|---|---|---|
| 真源文档 | `shared/guidelines/fast-fail.md` | **是**(`shared` 的 rglob) |
| 常驻章节 | `templates/instructions-template.md` | **是**(根级 `templates/*.md`) |
| 宪章原则 XIV | `templates/constitution-template.md` | **是**(同上;且路径含 `constitution-template` ⇒ 命中归 `governance_kept`,**仍计入 total**) |
| 命令 `MUST include` 条目 | `templates/commands/constitution.md` | **是** |
| 通道二命令侧落点 | `templates/commands/agents.md` | **是** |
| 通道二技能侧落点 | `skills/create-agent/SKILL.md` | **是** |
| 通道三落点 | `skills/create-team/references/patterns.md` | **是** |
| 派发期义务节 | `shared/definitions/subagent-definitions.md` | **是** |
| 出厂预设子句副本 | `agents/*.agent.md` | 否(`agents/` 不在 `SCAN_DIRS`)——但会经镜像与按工具树扩散,故仍按零命中写作 |
| 本 spec 目录制品 | `.specify/specs/052-fast-fail-principle/*` | **否**(`SKIP_DIR_PARTS` 含 `.specify`)⇒ 本规格与 `contracts/` 可自由使用「确认门控治理」等命中词 |

**C-5** `SKIP_DIR_PARTS` 含 `.specify`(`:37`),故 `.specify/shared/` 下的镜像副本 MUST NOT 被重复计数;但也因此**镜像副本不是豁免区**——源文件命中即计数,镜像只是不额外加一。

## 两类必踩陷阱

**C-6** **相邻纪律的中文名**:阻塞模式含 `confirmation gate|确认门[禁控]`,而「确认门控治理」逐字命中 `确认门[禁控]`。故真源文档、常驻章节、宪章原则与命令条目 MUST 以**路径**(`shared/guidelines/confirmation-gates.md`)指称该相邻纪律,MUST NOT 写出其中文名。路径中的 `confirmation-gates` 带连字符,**不命中**空格形态 `confirmation gate`。

**C-7** **停止语义**:表达"停在异常点并交用户裁定"时 MUST 用不命中等价表述。MUST NOT 使用的形态(取自改前实测的 17 条模式):`等待用户确认`、`等待确认`、`用户确认后才`、`确认后才(执行|写入|落盘|启动|持久化)`、`显式用户确认` / `explicit user confirmation`、`wait for user confirmation`、`MUST NOT execute before confirmation`、`stop and confirm`、`after user confirmation` / `after confirmation`、`[Cc]onfirm before`、`[Pp]roceed…yes/no`、`preview → confirm → execute`、`confirmation gate` / `确认门[禁控]`、`Confirm and persist` / `确认并落盘` / `合并确认`、`Execute on Confirmation`、`interactive confirmation`、`inviting the user to submit collected feedback`。

**C-8** 反空真哨兵:C-6 与 C-7 都是"命中集为空"型断言,故 MUST 各配一条伴生非空断言——断言被检文本本身非空(例如新增行数 ≥ 1),使"零命中因为措辞干净"与"零命中因为根本没检到文本"可区分。

## 相等判据与钉子集合

**C-9** 变更后实跑扫描器 MUST 满足 `total` 与冻结基线**相等**(而非 ≤)且 `violations` 为空。

**C-10** 本文件下方这张表是"`total` 被哪些既有断言钉住"的**唯一拥有者**;其余制品 MUST 以指针援引本条,MUST NOT 另行重抄钉子数目(否则数目每变一次就要改 N 处)。表中每一行都是一处独立的红:`total` 任何 +1 会**同时**打爆全部三行。

| # | 钉子 | 位置 | 形态 | 若日后需合法 +1,各自的解除路径 |
|---|---|---|---|---|
| 一 | 硬编码相等 | `tests/contract/test_user_facing_comprehension_doc.py:557` | `assert payload["total"] == 23`(字面量) | 改该测试的字面量 |
| 二 | 对冻结基线相等 | `tests/contract/test_proactive_trigger_section.py:352` | `assert payload["total"] == frozen["total"]`,`frozen` 取自 `.specify/specs/050-proactive-flow-trigger/baseline-gates.json`;断言消息自陈 `the integer headroom on the budget is 0` | 重冻该 JSON(C-11 禁止本特性这么做) |
| 三 | 上限(cap) | `tests/contract/test_confirmation_gates_sweep.py:162` | `assert payload["total"] <= cap`,`cap = baseline["total"] * 0.25`,`baseline` 取自 `.specify/specs/044-reduce-confirmation-flows/baseline.json`(`total: 93` ⇒ `cap = 23.25` ⇒ 可通过的最大整数为 **23**) | 改 044 的基线(与本特性无关的第三方制品) |

三行的**形态互不相同**(字面量 / 冻结基线相等 / 派生上限),这一点是实质信息而非细节:它意味着一次合法的 +1 需要同时动三个互不相干的表面,其中一个是别的特性的基线文件。FR-078 记录的"已接受代价"因此比"措辞受制于一个扫描器"更重——它还受制于三处彼此独立的钉子。

**C-10(a)** 反空真哨兵:C-10 的三行 MUST 各自可独立定位到真实断言。守卫 MUST 以 `grep` 或 AST 断言三个位置各自存在其形态特征(`== 23` 字面量 / `== frozen["total"]` / `<= cap`),MUST NOT 只断言"至少一处存在"——否则第三行被删掉时守卫仍绿,而预算实际上已松了一档。

**C-11** 本特性 MUST NOT 修改 C-10 表中的任何一处钉子,亦 MUST NOT 重冻 `.specify/specs/050-proactive-flow-trigger/baseline-gates.json`(钉子二的比对源)或 `.specify/specs/044-reduce-confirmation-flows/baseline.json`(钉子三的上限来源)。重冻基线会把"预算被本特性突破"伪装成"预算本来就是这个数",即一次以错误理由转绿的门禁。

## 规避改写的约束

**C-12** 为规避扫描器而做的改写 MUST 限于**措辞**;MUST NOT 通过改写清单条目或边界规则的**语义**来达成零命中(FR-064)。语义漂移是本特性唯一没有守卫的修改路径。

**C-13** 任何因规避而发生的措辞改写 MUST:(a) 触发 SC-001 的双评审者一致性复跑,与"清单每次移动后复跑"同等对待;(b) 在真源文档的修订记录中留痕,注明规避的是哪一个模式(FR-065)。

## 已接受代价的显式记录

**C-14** 真源文档的范围限制节 MUST 载明**已接受的代价**:因余量为 0 而取设计规避,本纪律的措辞从此**永久受制于一个与本纪律无关的扫描器的模式清单**——日后每次修订真源文档都要先躲开那 17 条模式(FR-078)。

**C-15** 该代价 MUST NOT 只记在本 spec 或 `plan.md` 里:它是真源文档的一部分,因为只有在那里,下一次修订它的人才会读到。一条未被写下的代价会在下一次修订时被当作"莫名其妙的约束"而被绕过。

## 其他引擎零改动

**C-16** 下列既有引擎与脚本 MUST **零改动**:`scripts/python/sync-mirrors.py`、`scripts/python/regen-command-copies.py`、`scripts/bash/generate-instructions.sh`、`scripts/python/feedback-utils.py`、`skills/create-team/scripts/dispatch.sh` 及其流过滤脚本、`src/specify_cli/__init__.py`。守卫形态为 `git diff` 对这六个路径为空,并配反空真哨兵(断言这些路径在改前确实存在且非空)。

**C-17** 镜像与按工具副本 MUST 由既有引擎产出,MUST NOT 手工编辑;`sync-mirrors.py` 的 `MIRROR_PAIRS` MUST 不变(改前实测五对:`templates`(排除 `commands`)、`skills`(排除 `site`)、`agents`→`.specify/agents/templates`、`scripts`、`shared`,其中 `shared` 与 `scripts` 为全树 rglob、无 manifest,故新增 `shared/guidelines/fast-fail.md` 自动被拾取)。

---

## 条款 → FR / SC 映射

| 条款 | FR | SC | 备注 |
|---|---|---|---|
| C-1 | FR-038 | SC-005 | 相对判据,基线冻结 |
| C-2 | FR-037 | SC-005 | 设计规避,三个值逐字不变 |
| C-3, C-4, C-5 | FR-036 | SC-005 | 逐行判据 + 封闭扫描面枚举 |
| C-6, C-7, C-8 | FR-036 | SC-005 | 两类陷阱 + 反空真哨兵 |
| C-9, C-10, C-10(a), C-11 | FR-038 | SC-005 | 相等而非 ≤;钉子集合的数目与形态由 C-10 单点拥有、C-10(a) 是其反空真哨兵;禁止重冻两个基线文件 |
| C-12, C-13 | FR-064, FR-065 | SC-001 | 语义漂移是唯一无守卫路径 |
| C-14, C-15 | FR-078 | — | 代价 MUST 写在真源文档里 |
| C-16, C-17 | FR-039, FR-058 | SC-005 | 六路径零改动 + 镜像由引擎产出 |
