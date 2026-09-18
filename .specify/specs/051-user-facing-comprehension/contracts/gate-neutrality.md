# Contract: gate-neutrality — 门控预算中立性与零新机制契约

**Feature**: 051 面向用户可理解性纪律  
**Guards**: 确认门控计数不变、扫描器零改动、三处新增文本零阻塞模式命中、零新机制  
**Test files**: 本契约的条款**分布在三个测试文件**中,归属逐条列明(此前本行笼统声明 C-2/C-3/C-5/C-6/C-7 全由纪律文档测试承载,而该测试的撰写任务范围并不含它们,导致这 5 条只剩手工 shell 核验、不进 CI):

| 条款 | 承载测试文件 | 说明 |
|---|---|---|
| C-1(a) | `test_user_facing_comprehension_doc.py` | 即该文件的 `discipline-doc` C-16 |
| C-1(b) | `test_user_facing_comprehension_section.py` | 即该文件的 `ambient-section` C-10 |
| C-1(c) | `test_constitution_double_landing.py` | 即该文件的 `constitution-export` **C-13** |
| C-2 | `test_user_facing_comprehension_doc.py` | 实跑扫描器并断言 `total == 23` 且 `violations == []` |
| C-3 | `test_user_facing_comprehension_doc.py` | 断言 `POLICY_DOCS`、`SELF_REL` 字面量与 `len(BLOCKING_PATTERNS) == 17` 均未变 |
| C-4 | —(**撰写指引,不设断言**) | 17 条禁用字面形态清单供撰写期自检;机械断言由 C-1 的三条承担 |
| C-5 | `test_user_facing_comprehension_doc.py` | 枚举本特性新增文件并断言可执行脚本数为 0 |
| C-6 | `test_user_facing_comprehension_doc.py` | 断言三个零改动面自 T001 的 `BASE_SHA` 起无新增/修改。**MUST 用 `git diff --name-only --no-renames --diff-filter=ACMR "$BASE" -- <路径集>` 并断言输出为空,MUST NOT 用 `git diff HEAD`**——CI 洁净检出下工作树恒等于 HEAD,后者无条件空真(见 C-6(a));断言 MUST NOT 按扩展名过滤(见 C-6(b)) |
| C-7 | —(**由既有套件承担**) | 全量契约套件 vs 冻结基线,执行者是 `tasks.md` 的 T057 与 GATE-1,不新写测试 |

**撰写任务的范围义务**:`tasks.md` 的 T003(该文件唯一的撰写任务)MUST 显式承载 C-2、C-3、C-5、C-6 四条,否则它们只存在于本文档而不存在于 CI。  
**Date**: 2026-09-17

本契约是整个特性**最硬的机械约束**。实测门控预算整数余量为 **0**,任何一处新增命中即同时打爆两个既有契约测试。处置方案与取舍见 `research.md` D-2。条款编号 **C-1…C-7**,以本文件为唯一权威;归属见上方表格(C-4 为撰写指引不设断言、C-7 由既有套件承担,故本文件并非每条都对应一个 `test_cN_*` 函数)。

---

## 实测基线(2026-09-17)

```
$ python3 scripts/python/scan-confirmation-gates.py
blocking confirmation gates: 23
  destructive: 13
  governance_kept: 10
violations (reversible gates still blocking): 0
EXIT=0
```

- 冻结基线 `.specify/specs/044-reduce-confirmation-flows/baseline.json:2` → `"total": 93`。
- 上限 `tests/contract/test_confirmation_gates_sweep.py:63-71` 计算 `cap = 93 × 0.25 = 23.25`,`assert total <= cap` ⇒ **最大可通过整数 23**。
- 第二道更严的钉子 `tests/contract/test_proactive_trigger_section.py:288-306` 断言 `total == 23`(**相等**,非 ≤)。
- ⇒ **整数余量 = 0**。Feature 050 的 `.specify/specs/050-proactive-flow-trigger/baseline-gates.json:14-24` 独立记录了同一结论。

## 扫描范围(实测)

| 常量 | 值 | 对本特性的含义 |
|---|---|---|
| `SCAN_DIRS`(`:35`) | `("templates/commands", "skills", "shared")`,递归 `rglob("*.md")`(`:85`) | **新真源文档在范围内**;`skills/summarize-project/**` 的搬家也在范围内 |
| `SCAN_ROOT_FILES`(`:36`) | `("templates",)`,非递归 `glob("*.md")`(`:94`) | **`templates/instructions-template.md` 与 `templates/constitution-template.md` 都在范围内** |
| `SKIP_DIR_PARTS`(`:37`) | `.specify`、`.claude`、`.qoder`、`.github`、`.opencode`、`__pycache__`、`.archive` | 镜像与 4 棵按工具副本树**不重复计数**;本 spec 目录不被扫描 |
| `SELF_REL`(`:38`) | `shared/guidelines/confirmation-gates.md` | 该文件**整体豁免**计数 ⇒ 编辑它(FR-018 的 `:68` 提升)不影响 `total` |
| `POLICY_DOCS`(`:41-44`) | `shared/patterns/reconcile-pattern.md`、`shared/patterns/interview-pattern.md` | 二者整体豁免 ⇒ 搬家 A 不影响 `total`;**本特性 MUST NOT 扩充此集合**(C-3) |

**关键**:`constitution-template.md` 的路径命中 `GOVERNANCE_PATH_PATTERNS`(`:71-76` 含 `constitution-template`)⇒ 其命中被归类 `governance_kept`,但 **`governance_kept` 仍计入 `total`**,不豁免。故"它在治理路径里所以安全"是**错误**推断。

---

## 条款

**C-1** 三处新增文本对 `BLOCKING_RE` 的命中数 MUST 各为 **0**:
- (a) `shared/guidelines/user-facing-comprehension.md` 全文;
- (b) `templates/instructions-template.md` 的 `## User-Facing Comprehension` 章节体;
- (c) `templates/constitution-template.md` 的两条新原则块(XII 与 XIII)。

测试 MUST 以 `importlib` 内联加载真实扫描器模块并复用其 `BLOCKING_RE`(先例:`test_ask_record_repeat.py:41,106-108`),MUST NOT 在测试内重写一份模式副本——重写副本会在扫描器演进时静默失效。

**C-2** 实跑 `scan-confirmation-gates.py` 后 MUST 满足 `total == 23` 且 `violations == []`。测试 MUST 断言**相等**而非 ≤,与 `test_proactive_trigger_section.py:288-306` 的既有钉子同强度。

**C-3** `scripts/python/scan-confirmation-gates.py` MUST **未被修改**——具体断言 `POLICY_DOCS`(`:41-44`)与 `SELF_REL`(`:38`)的字面内容不变,且 `BLOCKING_PATTERNS`(`:46-64`)的条目数仍为 **17**。

> FR-032 的条件前提("若真源文档为说明违规形态而引用任何命中阻塞模式的措辞")经 D-2 裁定**不成立** ⇒ 不登记 `POLICY_DOCS`,本特性对扫描器**零代码改动**。取舍依据:`POLICY_DOCS` 豁免只能救真源文档,救不了两个模板文件;而把整个 `instructions-template.md` 或 `constitution-template.md` 加进豁免集,会掩盖那 17 个章节 / 11 条原则里的真实门控回流,豁免面过宽。

**C-4** 撰写期自检清单 —— 下列 **17 条**字面形态(实测 `:46-64`)MUST NOT 出现在 C-1 的三处文本中。本条是**撰写指引**,机械断言由 C-1 承担:

`等待用户确认` · `等待确认` · `用户确认后才` · `确认后才(执行|写入|落盘|启动|持久化)` · `显式用户确认` / `explicit user confirmation` · `wait for user confirmation` · `MUST NOT execute before confirmation` · `stop and confirm` · `after user confirmation` / `after confirmation` · `[Cc]onfirm before` · `[Pp]roceed…yes/no`(中间 ≤40 字符) · `preview → confirm → execute`(箭头可为 `→` 或 `->`) · `confirmation gate` / `确认门[禁控]` · `Confirm and persist` / `确认并落盘` / `合并确认` · `Execute on Confirmation` · `interactive confirmation` · `inviting the user to submit collected feedback`

**两个高危陷阱**:

1. **`确认门[禁控]`** —— 本纪律必须频繁谈论门控提示。写成 `确认门控` 或 `确认门禁` 即命中。合规写法:**`门控`** / **`门控提示`** / **`前置确认`** / **`门控确认提示`**(其字序为「门-控-确-认」,**不含** `确认门`,安全)。
2. **`classify()` 第 3 条**(`:98-109`)—— 命中 `BLOCKING_RE` 且行内**不含** `执行`/`写入`/`落盘`/`启动`/`继续` 五个中文字面之一、且无破坏性关键词、路径不命中 governance ⇒ 判为 **`reversible`**。这不仅使 `total` +1,还**额外**打爆 `test_confirmation_gates_sweep.py:54-60`(`test_no_reversible_gates_remain_blocking`)并使扫描器在 `--baseline` 下 **exit 2**。本纪律文档必然频繁出现「执行」「写入」,故该路径比单纯计数更易触发 ⇒ 规避是**强制**的。
   注:该 reversible-context 判定**只认那五个中文字面**,英文 `execute` / `execute before` **不算**(`:106`)⇒ 撰写英文反例时不可依赖英文词提供豁免。

**C-5** 本特性新增文件中**可执行脚本数 MUST 为 0**:新增 `.py` 文件 MUST 仅位于 `tests/contract/`;MUST NOT 新增任何行话 lint 引擎、措辞评分器、成熟度报告生成器、跟踪台账或注册表(FR-033 / Principle IX)。

断言方式(**命令形态经实测确定,MUST 逐字采用**):

```bash
# BASE 由 T001 在冻结改前基线时记录为字面 SHA,存于 notes/pre-change-measurements.md
git diff --name-only --no-renames --diff-filter=ACMR "$BASE" -- . | grep -E '\.(py|sh)$' | grep -vE '^tests/contract/' | wc -l
# MUST 输出 0
```

三个要点,缺一个该断言即失效:

1. **MUST 用 `--name-only`,MUST NOT 用 `--stat`**。`--stat` 把每行渲染成 ` path | N ++++`,行尾是 `+` 而非扩展名,且长路径被省略为 `.../name` ⇒ `grep -E '\.(py|sh)$'` **永远零命中**。实测对照(基 `b4fb16cb~1` → `b4fb16cb`,该提交新增了 `scripts/python/validate-tasks.py`):`--stat` 形式零输出 exit 1,`--name-only` 形式正确命中该文件及其镜像;在 6 个提交上循环(共 16 个真实新增 `.py`),`--stat` 形式命中数**恒为 0**。
2. **MUST 含 `--no-renames` 且 filter 含 `R`**,否则 `git mv` 一个既有脚本到新位置会绕过 `--diff-filter=A`。
3. **断言 MUST 以"过滤后计数 == 0"的形式表达**,而不是"命中全部落在 `tests/contract/`"——后者在命中集为空时**空真**,无法区分"没有新增脚本"与"命令什么都没匹配到"。

`BASE` MUST 是 T001 记录的**字面 SHA**,MUST NOT 写 `HEAD~<n>`(n 未定,且随后续提交漂移)。

**C-6** `src/specify_cli/__init__.py` 与 `scripts/`(含 `scripts/bash/generate-instructions.sh`、`scripts/python/sync-mirrors.py`、`scripts/python/regen-command-copies.py`、`scripts/python/feedback-utils.py`)MUST **未被本特性修改**。FR-038 的悬空指针义务落在**文本层**(指针行附获取途径说明 + `ambient-section.md` C-11 的遍历断言),MUST NOT 通过改投递脚本实现——修 `generate-instructions.sh` 使其同步 `shared/` 属另一条 Feature 的归属(规格 Out of Scope)。

**C-6(a) 比对基线 MUST 是 T001 冻结的 `BASE_SHA` 字面值,MUST NOT 是 `HEAD`**(发现项 B-02):`git diff HEAD` 比较工作树与 HEAD,而 `tasks.md` 的提交纪律要求"每完成一个任务或一个逻辑组即提交",故本特性**自己已提交**的改动对该形式不可见。更严重的是**在 CI 里它无条件空真**:CI 检出是干净的,工作树恒等于 HEAD,于是"断言 `git diff HEAD -- <路径>` 为空"的 pytest 用例**永远通过**、不论本特性改了什么——这正是本仓 `AGENTS.md` 点名的最差缺陷形态(看着绿的假通过)。实测对照:`git diff --stat HEAD -- scripts/` 输出为空,而 `git diff --name-only HEAD~20 HEAD -- scripts/` 列出 3 个文件。C-5 已就其自身命令规定了同一约束("`BASE` MUST 是字面 SHA,MUST NOT 写 `HEAD~<n>`);C-6 此前**未规定任何基线**,是本契约内部的不一致。

**C-6(b) 断言 MUST 覆盖路径集下的全部文件类型,MUST NOT 按扩展名过滤**:`templates/plan-template.md` 是 `.md`,而 GATE-9 的探针按 `\.(py|sh)$` 过滤,故 GATE-9 对该面**结构性不可见**;`scripts/` 下另有 **70** 个非 `.py`/`.sh` 的受跟踪文件(实测 67 个 `.mjs` 位于 `scripts/js/better-harness/`,加 `LICENSE`、`UPSTREAM.md`、1 个 `.json`),同样落在扩展名过滤之外。零改动面的命题是"该路径集下**任何**新增/修改/重命名为空",与 GATE-9 的"全仓无可执行脚本新增"是两个不同命题,分别由 **GATE-4** 与 **GATE-9** 承担;故 MUST NOT 靠扩大 GATE-9 的扩展名过滤来补 C-6——那会让一个门承担两个命题、且仍漏掉 `.md`。

**C-6(c) 唯一合法的 `HEAD` 相对用法**:T002 在**开工时**核验三个面干净,此刻 HEAD 即基线(`BASE_SHA` 刚由 T001 记下、本特性尚无任何提交),`git diff HEAD` 与 `git diff "$BASE"` 等价。除此一处外,任何 `HEAD` 相对的零改动断言都是缺陷。

**C-7** 既有测试基线 MUST 不恶化。实现期门禁:失败集 ⊆ 049 冻结基线(`.specify/specs/049-docs-reconcile/baseline-failed.txt`,47 条)∪ {`test_specify_script_paths.py::TestSpecifyScriptPaths::test_review_prerequisite_flags_are_supported`}。后者因本分支尚无 `tasks.md` 而失败(`check-prerequisites.sh:248-250` 只在文件存在时才把 `tasks.md` 放进 `AVAILABLE_DOCS`),`/speckit.tasks` 后自愈,**无需改任何源码**。任何**新增**失败 ID 即本特性引入的回归。开工前 MUST 重新冻结一份 `baseline-failed.txt` 到本 spec 目录(承 049/050 惯例),**执行者是 `tasks.md` 的 T001**——本条此前只声明义务而未指派承担者,而 049 与 050 的同一惯例都由各自的 T001 承担(发现项 B-04)。冻结集 MUST 取自开工当时的实跑输出,不得沿用本 spec 目录里既有的那份:实测 `test_specify_script_paths.py::…::test_review_prerequisite_flags_are_supported` 在 `tasks.md` 生成后**已自愈**(24 条实为 23 条),且仓库另有来自本特性未触及的在途漂移的失败,这些 MUST 一并纳入冻结集,而不是留给 GATE-1 报成"新增失败"。

---

## 条款 → FR / SC 映射

| 条款 | FR | SC |
|---|---|---|
| C-1, C-2, C-4 | FR-032 | SC-012 |
| C-3 | FR-032 | SC-012 |
| C-5 | FR-033 | SC-011 |
| C-6 | FR-038 | SC-017 |
| C-7 | FR-029 | SC-016 |
