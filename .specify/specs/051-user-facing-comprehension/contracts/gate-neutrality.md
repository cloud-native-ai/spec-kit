# Contract: gate-neutrality — 门控预算中立性与零新机制契约

**Feature**: 051 面向用户可理解性纪律  
**Guards**: 确认门控计数不变、扫描器零改动、三处新增文本零阻塞模式命中、零新机制  
**Test files**: 条款分布于 `test_user_facing_comprehension_doc.py`(C-1、C-4 的文档侧)与 `test_user_facing_comprehension_section.py`(C-1、C-4 的章节侧);C-2、C-3、C-5、C-6、C-7 由 `test_user_facing_comprehension_doc.py` 承载  
**Date**: 2026-09-17

本契约是整个特性**最硬的机械约束**。实测门控预算整数余量为 **0**,任何一处新增命中即同时打爆两个既有契约测试。处置方案与取舍见 `research.md` D-2。

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

**C-5** 本特性新增文件中**可执行脚本数 MUST 为 0**:新增 `.py` 文件 MUST 仅位于 `tests/contract/`;MUST NOT 新增任何行话 lint 引擎、措辞评分器、成熟度报告生成器、跟踪台账或注册表(FR-033 / Principle IX)。断言方式:枚举本特性新增文件路径,断言其中可执行脚本(非 `tests/` 下的 `.py`、任何 `.sh`)数量为 0。

**C-6** `src/specify_cli/__init__.py` 与 `scripts/`(含 `scripts/bash/generate-instructions.sh`、`scripts/python/sync-mirrors.py`、`scripts/python/regen-command-copies.py`、`scripts/python/feedback-utils.py`)MUST **未被本特性修改**。FR-038 的悬空指针义务落在**文本层**(指针行附获取途径说明 + `ambient-section.md` C-11 的遍历断言),MUST NOT 通过改投递脚本实现——修 `generate-instructions.sh` 使其同步 `shared/` 属另一条 Feature 的归属(规格 Out of Scope)。

**C-7** 既有测试基线 MUST 不恶化。实现期门禁:失败集 ⊆ 049 冻结基线(`.specify/specs/049-docs-reconcile/baseline-failed.txt`,47 条)∪ {`test_specify_script_paths.py::TestSpecifyScriptPaths::test_review_prerequisite_flags_are_supported`}。后者因本分支尚无 `tasks.md` 而失败(`check-prerequisites.sh:248-250` 只在文件存在时才把 `tasks.md` 放进 `AVAILABLE_DOCS`),`/speckit.tasks` 后自愈,**无需改任何源码**。任何**新增**失败 ID 即本特性引入的回归。开工前 MUST 重新冻结一份 `baseline-failed.txt` 到本 spec 目录(承 049/050 惯例)。

---

## 条款 → FR / SC 映射

| 条款 | FR | SC |
|---|---|---|
| C-1, C-2, C-4 | FR-032 | SC-012 |
| C-3 | FR-032 | SC-012 |
| C-5 | FR-033 | SC-011 |
| C-6 | FR-038 | SC-017 |
| C-7 | FR-029 | SC-016 |
