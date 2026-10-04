# Phase 0 Research: 机器可判定的制品命题(Machine-Decidable Artifact Propositions)

**Requirement**: `053-machine-decidable-artifacts` → Feature 053  
**Date**: 2026-10-02  
**Method**: 本文件每条决策都附**实测证据**(命令 + 输出 + 行号),不引用记忆。凡"改前即可实跑"的命令均已于本日实跑;凡依赖尚未创建制品的命令,标注为改前不可实跑并给出改前等价基线。

**工件形态以 052 为准**(最新约定):`research.md` 独立成文、契约用 `**C-N**` 条款形态并逐条标注制品类/行为类、quickstart 场景用 `## 场景 N` 编号、`feature-ref.md` 承担 FR→条款与 SC→度量两张映射表。

**探查方式**:同作者检测已委托。规格由同一 agent 在同一会话写成,故 Phase 0 的代码库探查交给 **3 个**新鲜上下文只读子代理(US1 / US2+US3 / US4+US5 分工),每个简报携快速失败派发注入子句并要求回传显式异常行。**子代理回传的每个承重实测值均由编排者重新导出后才进入本文件**——本轮该纪律抓到 1 项子代理误判与 1 项编排者自身的假测量,见 § 上送与披露。

---

## D-1 条款语法的 owner:新建 `shared/definitions/contract-clause-definitions.md`

**裁定方式**: **经用户裁定**(2026-10-02,`/speckit.plan` Phase 0 一轮批量提问,三选项:一份新 owner 文档(推荐)/ owner 文档 + 新建 contracts 模板 / 由脚本 docstring 拥有)。用户取推荐项。

**裁定**:新建 `shared/definitions/contract-clause-definitions.md` 作为条款语法的**唯一 owner**,声明(a)新契约的规范形态与(b)它只读识别的遗留形态集合。不新建 contracts 模板。

**为何需要裁定**:FR-022 给了两条路,而探查证明第一条实际不可用——全仓**无任何既有 owner**:

```
$ grep -rniE "clause (id|identifier|numbering|syntax)|条款(编号|语法|形态)|C-N (form|syntax|convention)" \
    templates/ shared/ docs/ --include=*.md | grep -v docs/public
(exit 1,无命中)
$ find templates -iname "*contract*" -o -iname "*clause*"
(空)
```

最接近约定的是两处**用法**而非定义:`.specify/specs/052-fast-fail-principle/feature-ref.md:21`「条款引用形态为 `<contract-file> C-N`」与 `templates/requirements-template.md:173` 的示例 `contracts/xxx.md C-N`。`templates/` 顶层 21 个条目中无任何 contracts 模板。

**落点约束(实测)**:`scan-confirmation-gates.py:35` 的 `SCAN_DIRS = ("templates/commands", "skills", "shared")` 含 `shared`,故新 owner 文档从**第一稿起**就在门控扫描面内,而 total 为 **23**、cap = 93 × 0.25 = **23.25**、整数余量 **0**(实跑:`blocking confirmation gates: 23 / destructive: 13 / governance_kept: 10 / violations: 0`)。该文档是**语法定义**,无理由出现 `BLOCKING_PATTERNS`(**17** 条)的任何一条,故以措辞回避即可满足 FR-045。命名从 `shared/definitions/` 既有 **8** 份 `*-definitions.md` 的体例(该目录共 9 个文件,第 9 个 `framework-map.md` 不匹配该模式)。

**被拒方案**:① 同时新建 `templates/contracts-template.md`——对标 tasks 的先例(行形态由 `templates/commands/tasks.md:151-155` 拥有、由 `templates/tasks-template.md` 实例化),但多一个文件、多一行镜像义务、多一份扫描面措辞,而条款语法的消费者是**核算脚本**而不是逐字抄模板的作者;② 由核算脚本的 docstring 拥有——表面最小,但把一个文档约定的 owner 变成脚本,反转了房子的 owner 优先序(语法约定是定义性事实,归 authored doc)。

---

## D-2 `.yaml` 契约:手写两个最小抽取器,不引入 PyYAML

**裁定方式**: **经用户裁定**(同上轮,三选项:手写两个最小抽取器(推荐)/ 全部点名跳过 / 引入 PyYAML 依赖)。用户取推荐项。

**裁定**:为 9 份 OpenAPI 与 1 份结构化断言各写一个**最小行级抽取器**;**任何解析存疑 MUST 回退到 FR-023 的点名跳过**,MUST NOT 猜测。不新增任何运行依赖。

**关键成本事实(实测)**:PyYAML **不是**本仓声明依赖——

```
$ sed -n '/^dependencies/,/^\]/p' pyproject.toml
dependencies = ["typer","rich","httpx[socks]","platformdirs","readchar",
                "truststore>=0.10.4; python_version >= '3.10'"]
$ grep -rn "import yaml\|yaml\." scripts/python/*.py
(无命中——全部 scripts/python/*.py 零 import yaml)
```

它在当前环境可导入(`yaml 6.0.3`)纯属偶然,不是可依赖的事实。房子既有先例是**手写解析**:`gate-check.py:48` 的 `parse_gate(text: str) -> dict[str, list[str]]` 逐行解析 `.specify/gate.yaml`。

**条款全集实测**:逐形态的文件数与条款 id 数由 **`notes/clause-form-census.md` 唯一拥有**,本条**不复写任何数字**。理由不是形式上的:该量随本特性自己的契约落盘与每次编辑而变动,本文件初版曾在此复写一组值,数小时后即被自己追加的两条条款推翻——一个被本文件自己的编辑推翻的数字不该出现在本文件里。需要数值时现场跑该文件内的命令(**MUST 从仓根运行**)。

抽取器取 D-1 的 owner 所声明的形态;OpenAPI 的条款全集 = `paths:` 下的 HTTP 方法键(**文件内无字面 `operations:` 键**,MUST NOT 以该键名作探测条件——这是 FR-028 订正后的实测结论),结构化形 = `^\s+- id:` 的取值。

**被拒方案**:① 全部点名跳过——零解析风险,但 10 份文件永久处于核算之外,与 US3「消灭自陈覆盖率」的主旨相左;② 引入 PyYAML——会是框架的**第一个** YAML 运行依赖,为 45 个条款 id 而加,很可能构成 Principle IX(No Over-Engineering)违例。

---

## D-3 FR-018 覆盖两个命题:条款区间冲突 + 测试路径绿点分歧

**裁定方式**: **经用户裁定**(同上轮,三选项:两者都机械化(推荐)/ 只做规格字面的条款冲突 / 只做测试路径冲突)。用户取推荐项。

**裁定**:FR-018 扩为覆盖 (a) 同条款同区间被两行认领、(b) 同一测试路径出现在两个核验行且两行绿点不同,二者 MUST **分列**报出。

**该裁定扩大了 FR-018 的范围,故按 `/speckit.plan` 的上游优先规则先改 `requirements.md` 再填本计划**:FR-018 已改写、US2 已增验收场景 6(正反两向)、`## Clarifications` 已按追加方式记入第 5 条 bullet。FR 仍 48、SC 仍 12,**编号未变故无需重编号**;清单已复验一次(16/16)。

**为何不是编造**:该义务在框架里**已经存在**,只是仍以散文执行——`templates/commands/tasks.md:197` 原文「Add a self-check that flags any test path appearing in two verification rows with different green points」;而 `.specify/memory/glossary.md:134` 已登记的「条款分区 (Clause Partition)」条目本身即写明「生成期 MUST 机械核算分区的并集覆盖全部条款且无幻影记号」。US2 恰好在建它所需的全部解析数据:行级测试路径由既有 `_classify_paths`(`validate-tasks.py:94-112`)抽出,绿点由新 `[green:]` 声明抽出。边际成本 = 一个检查标签 + 一个逆样本 + 一个钉子条目。

---

## D-4 新检查器的名字与落点:`scripts/python/validate-requirements.py`

**裁定**:名字取 `validate-requirements.py`,与既有 `validate-tasks.py` 同形同目录;镜像落 `.specify/scripts/python/`。

**依据(实测)**:标识符冲突检查已在规格现状锚点记录该名字在非 spec、非 memory 的跟踪文件里**零命中**。镜像与打包均自动覆盖:

- `sync-mirrors.py:72-78` 的 `MIRROR_PAIRS` 含 `scripts → .specify/scripts`(`strict_extras=True`);`--only` 接受可重复的仓相对**路径前缀**(`:116-119`,docstring 示例 `:23` 即 `--only scripts/python/feedback-utils.py`),不匹配任一对前缀则 exit 2(`:141-149`);字节比较用 `filecmp.cmp(..., shallow=False)`(`:106`)。
- `pyproject.toml:32-37` 的 `[tool.hatch.build.targets.wheel.force-include]` 把**整个** `scripts` 树映射到 `specify_cli/scripts`,故新脚本自动随包安装(FR-047)。
- 镜像一致性由**引擎级**测试保证,无逐文件枚举:`tests/contract/test_scripts_distribution_parity.py::test_repo_has_no_orphan_or_drifted_scripts`(`:71-87`)跑 `sync-mirrors.py --check` 并断言 exit 0(核心断言 `:79`);`test_scripts_pair_is_strict_about_orphans`(`:39-46`)钉住 `strict_extras=True`;`test_fast_fail_discipline.py:1923` 钉 `len(mod.MIRROR_PAIRS) == 5`。实测 `cmp scripts/python/validate-tasks.py .specify/scripts/python/validate-tasks.py` → BYTE-IDENTICAL。

---

## D-5 检查项标签集:**docstring 就是契约**,不是发出去的消息

**裁定**:新检查器的检查项标签集 MUST 以 `validate-tasks.py` 的 docstring 体例书写,因为既有钉子**从 docstring 派生标签**,而不是从运行输出。

**实测(承重)**:`tests/contract/test_validate_tasks_parallel_safety.py`

```python
:75  EXPECTED_CHECKS = {"row-format","id-unique","blockedBy",
                        "parallel-safe","story-labels","dod-format"}
:312 labels = set(re.findall(r"^  ([A-Za-z][A-Za-z-]*)\s{2,}", doc, re.M))
:314 assert labels == EXPECTED_CHECKS
```

`:312` 的 `doc` 是**模块 docstring**。其体例是:两空格缩进 + 标签 + ≥2 空格 + 描述列(`validate-tasks.py:9-33`)。任何偏离该缩进/间隔的新 docstring 都会让标签集抽取漏项——而漏项表现为「集合变小」,若钉子同时被改小就无人发现。故 FR-042 的标签集钉子 MUST 与 docstring 体例一起被钉。

**新检查器的标签集(派生自 FR-006…FR-011)**:`id-contiguous`(FR-007)、`doc-order`(FR-008)、`ref-resolvable`(FR-009)、`marker-count`(FR-010)、`dup-id`(FR-011)。5 项,每项按 FR-039 各配至少一个逆样本。

**`validate-tasks.py` 侧新增的标签**(US2/D-3):`green-dangling`(FR-016,ERROR)、`green-cross-phase`(FR-017,WARN)、`green-clause-collision`(FR-018(a),WARN)、`green-path-divergence`(FR-018(b),WARN)。既有 6 项 + 新 4 项 = **10** 项,`EXPECTED_CHECKS` 与 docstring MUST 在同一提交内同步扩充(FR-046)。

---

## D-6 新检查器的退出码表:沿用先例的 0/1/2,FR-004 的第三态走 verdict 而非新码

**裁定**:`validate-requirements.py` 的退出码沿用 `validate-tasks.py` 的三档——`0` 无 error(允许 warning)/ `1` ≥1 error / `2` 文件缺失或不可解析或无内容行。FR-004 要求的三种**互相可区分**情形(不存在 / 不可解析 / 为空或仅模板骨架)在 `--json` 的 `status` 与逐项 verdict 上区分,MUST NOT 为此新增第四个退出码。

**依据(实测)**:`validate-tasks.py:295-297` 缺文件 → stderr + `return 2`;`:300` `unparseable = any(e.startswith("0:") for e in errors)`;`:317` `return 2 if unparseable else (1 if errors else 0)`;warning 永不影响退出码。该表被 `test_c5_exit_code_table`(`:346-370`)逐档钉住,含 `:353` 「0 = no errors (warnings allowed)」、`:355-356` 「a warning-only file must still exit 0」、`:362` 「1 = at least one error」、`:364-369` 两个 2 档。

**为何不新增第四码**:FR-004 的原文是「互相可区分的**退出码或 verdict**」,二者择一即可;而 `0/1/2` 已被同目录先例与其钉子占住,新检查器另立四档会让两个同形脚本的退出码语义分叉——正是 D-11 里 `goal-utils` 要避免的那类冲突。"为空或仅模板骨架"以 `status` 的一个独立取值表达(先例只有 `PASS`/`FAIL` 两值,故这是**新增**取值,须在钉子内声明)。

**`--json` 键集**:先例只发 `{"file","errors","warnings","status"}` 四键(`:302-308`),**无逐项 verdict 数组**。FR-003 要求的「逐项检查的 verdict」因此是**新造**形态;经 `/speckit.clarify` 裁定,该要求只辖**新增**检查器,既有 `validate-tasks.py` MUST NOT 因本特性被要求迁移其 JSON。实测风险低:全仓无任何调用方传 `--json`(`templates/commands/tasks.md:76` 只以人读形态调用)。

---

## D-7 `[green:]` 标签会被既有路径分类器误判为**写入目标**(实证,非推断)

**裁定**:US2 MUST **先抽取归属声明、再对残余文本做路径分类**——即在 `_classify_paths` 之前把 `[green: ...]` 的整段从行文本中取出并单独解析。MUST NOT 靠往 `POINTER_GOVERNOR` 里加一个标签前缀来解决。

**实证**(本轮实跑,临时目录已删净、残留计数 0):

```text
# 正样本对照:两行 [P] 写同一路径 → 如期 WARN
- [ ] T001 [P] Write the thing in docs/a.md
- [ ] T002 [P] Write another thing in docs/a.md
WARN 3: parallel-safe: [P] tasks T001 (line 3) and T002 (line 4) both WRITE ['docs/a.md'] …

# 加了 [green:] 标签、两行写入目标本不相同:
- [ ] T001 [P] Write the thing in docs/a.md [green: contracts/x.md#C-1]
- [ ] T002 [P] Write another thing in docs/b.md [green: contracts/x.md#C-2]
WARN 3: parallel-safe: … both WRITE ['contracts/x.md'] …      ← 假告警
```

第二例中 `docs/a.md` 与 `docs/b.md` 本不相同,告警点名的却是**标签内的契约路径**。

**机理**:`PATH_TOKEN`(`:63-65`)的尾字符类不含 `#`,故它在 `[green: contracts/x.md#C-1]` 里匹配出 `contracts/x.md`;`:106-107` 的 `if "[" in tok or "]" in tok: continue` **保护不到它**——被匹配的 token 自身不含方括号,方括号在匹配范围之外;而其前 40 字窗口内无 `POINTER_GOVERNOR`(`:70-75`,一个**刻意封闭**的只读治理词表)命中,故按默认落进 write 集。

**为何选"先抽取再分类"而不是扩治理词表**:`POINTER_GOVERNOR` 的注释明写它是「a closed list of unambiguous read-only **governors**」即治理**词**;`[green:` 是一个标签前缀而非词,塞进去会让该表的语义不再自洽。而 FR-019 要求归属声明与既有行形态检查**正交**——先抽取再分类使正交性成为**构造性质**而不是一个正则特例,同时正好产出 US2 需要的四元组。

**编排者自身的一次探查错误(已订正并披露)**:第一次探针让 T001 **不带** `[P]`,而 `parallel-safe` 只在两个 `[P]` 行之间触发,故误得「无告警」并一度判子代理的推断为假。补上正样本对照后才复现。教训已并入本文件 § 上送与披露。

---

## D-8 「绿点跨阶段」WARN 用单调行序,不用阶段号

**裁定**:FR-017 的跨阶段判定 MUST 用既有的单调行计数 `order`,MUST NOT 依赖阶段序号。

**依据(实测)**:`validate-tasks.py` **没有**数值阶段索引——`PHASE_HEADING`(`:57`)只捕获标题串,`by_phase`(`:236-239`)按**标题字符串**分组。可用的是单调行序 `order`(`:123` 初始化、`:171`/`:181` 递增并存入每条任务),而它**已经**被用于同型判定:`:229-233` 的 `blockedBy` 前向依赖 WARN 正是比较 `order`。故跨阶段绿点是该先例的直接类比,零新机制。

---

## D-9 FR-014 的债务**本身被两个测试钉住**,移除过渡副本 MUST 同轮改测试

**裁定**:US1 落地时移除 `shared/constants/clarify-taxonomy.md` 的过渡期 awk 抽取式与「Until that validator ships」一句,**同一提交内** MUST 改写 `tests/contract/test_clarify_semantic_completeness.py` 的两个测试。

**实测(承重)**:

```python
:311 def test_c4_extraction_is_definition_anchored_and_history_excluded():
:322     block = re.search(r"```bash\n(.*?)```", region, re.S)
:324     assert block, "the interim extraction block is gone from the document-order invariant"
:326     assert r"^- \*\*(FR|SC)-[0-9]+\*\*" in cmd, …
:329     assert "## Clarifications" in cmd, …
:330     assert "load-bearing" in rules, …
:336 def test_c4_shared_implementation_with_the_requirements_validator_is_declared():
:338     assert "shares one implementation" in rules, …
:341     assert "/speckit.requirements" in rules, …
```

`:324` 的断言消息**逐字就是**「the interim extraction block is gone」——即该测试当前把过渡副本的**在场**当作通过条件。FR-014 要求移除它,故这两个测试 MUST 从「断言副本在场」改写为「断言不变量指向新检查器」。

`"Until that validator ships"` 一句**未被钉**(`grep -rn "Until that validator" tests/` → 无命中),可自由移除。被钉的是 `:338`/`:341` 的「shares one implementation」与「/speckit.requirements」两处措辞——它们恰好在 US1 落地后**变成真的**(此前只是声明),故改写方向是把「宣告将来共享」换成「指名现在共享的实现」。

**过渡副本的位置**:`clarify-taxonomy.md:106`(文档序不变量条目起)· `:108-112`(awk 块)· `:114`(两个锚点的理由)。同文件 `:20-22` 的 docstring 已把机器实现指派给「the deterministic requirements validator, a separately scheduled feature」——即本特性。

---

## D-10 覆盖核算:新脚本 + 冻结名字级基线文件

**裁定**:核算脚本取 `scripts/python/account-clause-coverage.py`(单一入口、只读、以被核算 spec 目录为参数);FR-027 裁定产生的基线文件取 `.specify/specs/<key>/coverage-baseline.txt`,形态与 `run-tests.sh --names-out` 的输出同构(每行一个名字、已排序),使比对可以直接用 `comm -13`。

**依据(实测)**:`scripts/bash/run-tests.sh:22-24,29,35-43` 的 `--names-out <file>` 已确立该形态——`:41` `printf '%s\n' "$OUT" | grep "^FAILED" | sed 's/^FAILED //;s/ - .*//' | sort > "$NAMES_OUT"`,`:42` 向 stderr 印 `# failed-name list written: <file> (<N> entries)`,`:43` `exit "$STATUS"`(透传 pytest 自己的码)。该脚本**不**存基线、**不**跑 `comm`;`comm -13` 是文档化的消费者习语(`:23` 注释、`templates/tasks-template.md:80` 的 GATE-1)。核算脚本沿用同一分工:脚本产出**有序名字集**,比对留给 `comm`。

**MUST NOT 抄的比较形态(实测缺陷,已被记录两次)**:`scan-confirmation-gates.py --baseline` 读基线的**顶层** `total`,而冻结值嵌在 `confirmationGates` 下,且其退出码只反映 `violations`——故它作为相等门不可用。该缺陷已记录在 `.specify/memory/constitution.md:14` 的后续 TODO (a) 与 `.specify/specs/052-fast-fail-principle/contracts/gate-neutrality.md` + `verification.md:209`,**上游仍未修**。本特性的核算脚本 MUST NOT 复制该形态。

**无既有先例可复用**:`grep -rlniE "uncovered|未覆盖|差集|set difference|coverage" scripts/python/*.py scripts/bash/*.sh` → 只命中 `feedback-utils.py`(反馈存据的覆盖,无关)。真正的前身是**手写**的 `.specify/specs/052-fast-fail-principle/feature-ref.md`(173 行,含 `## FR → 契约条款映射` `:19`、`### 未由契约条款覆盖的 FR(7 条),各有其理由` `:112`、`## SC → 产出与度量映射` `:128`、`## 交付面清单` `:152`);全仓 **30** 份 spec 有 `feature-ref.md`。

---

## D-11 `run-checks`:五项检查全部只存在于 `preview_target_check` 内部,且**无 `--target` 时第①项不可达**

**裁定**:`run-checks` MUST 新增一个薄封装,在无 `--target` 时先经 `resolve_effective_target` 解析有效 target;解析不出 target 时,②③④ 三项 MUST 记 [[STR-004]] `not-evaluated`(它们无判定主体),①⑤ 仍 MUST 被评估(它们只依赖团队与 goal 的绑定关系,不依赖 target)。MUST NOT 为 `run-checks` 重写第二套文法(FR-030)。

**实测**:`goal-utils.py`(1028 行;镜像字节相同)

- 派发:argparse 子命令 `sub = parser.add_subparsers(dest="action", required=True)`(`:800`)+ `main()` 里的 if/elif 链(`:872-992`)。`grep -c "sub.add_parser"` → **9**:create `:802` · validate `:812` · check-statement `:816` · list `:822` · status `:824` · objective `:830` · criteria `:836` · migrate `:846` · targets `:853`。**`run-checks` 未被占用** ✓。
- `preview_target_check(repo_root: Path, team_slug: str, reference: str) -> dict`(`:626-676`):`reference` 是**必需位置参数**,返回 `{goal_slug, identity_kind, verdict, message}`(终态时加 `status`/`statement` `:669`,ok 时加 `target_id` `:675`);docstring `:629` 明写 "Read-only: parses, never writes"。
- `resolve_effective_target(team_md_path: Path, explicit_target: str | None = None) -> dict`(`:679-707`):返回 `{effective, source, declared_focus}`(input-error 时加 `message` `:701`)。
- **二者均无 CLI 入口**:`grep -rn "preview_target_check\|resolve_effective_target" --include=*.py .` 只命中定义处(`:626`、`:679`)、一处 docstring(`:684`)与两个测试文件(`tests/contract/test_focus_target_resolution.py`、`tests/integration/test_run_target_validation.py`)。既有独立记录:`.specify/memory/feedback/introspection/introspection-20260923T120035Z.md:162`。
- **五项检查的现有产出点**(全部只在 `preview_target_check` 内):① goal-binding → `resolve_team_goal_identity`(`:607-620`)判 `goal_slug is None`(`:634-637`,以及 `:654-657` 绑定 slug 无对应文件)→ `no-goal-definition`;② dangling → `:663-667`;③ target-terminal → `:668-674`;④ cross-goal → `_QUALIFIED_TARGET`(`:623`)前缀 ≠ `goal_slug`,`:639-645`;⑤ goal-terminal → `data["status"] in TERMINAL_STATES`(`:55`),`:659-662`。文法失败 → `input-error`(`:646-651`)。
- **无字面量名为 `goal-binding`**:第①项的 verdict 字面量是 `no-goal-definition`。故 `run-checks` 输出里 check 的 `name`(FR-031 的五个名字)与其 `verdict` 字面量是**两个词表**,MUST NOT 混用。
- **零写入已证**:全部写入点 8 处(`:465`/`:466` create_goal、`:487` set_status、`:506` set_objective、`:524` set_criteria、`:569` add_target、`:599` set_target_status、`:756` migrate_team);读动作(validate/list/check-statement/targets --list/--check)只达 `read_text`(`:329`、`:359`、`:614`、`:692`、`:720`),无写入函数在其调用路径上。
- `--json` 已在**共享父解析器**上(`:794`),故置于 action 前后皆可;每个 action 以 `_emit(result, args.json)`(`:1000`)收尾,`_emit`(`:1004-1024`)在 `--json` 下 `json.dumps(..., ensure_ascii=False, indent=2)`。

**该二进制另发第 8 个 verdict 字面量 `rejected`**(`:935` `check-statement`、`:968` `targets --check`,均配 `EXIT_INPUT_ERROR`)。它不在 STR-006 的 7 个字面量内,但**与五项检查无关**,故 STR-006 的「7 个」是 `run-checks` 的词表而非该二进制的全词表——该精度已回写进规格的 STR-006 行,MUST NOT 因本特性删改 `rejected`。

---

## D-12 `run-checks` 的 `--help` 行 MUST 以 `read:` 起首,且既有 roster 钉子 MUST 被扩

**裁定**:新 action 的 help 首词取 `read:`(它是只读动作,FR-034);同一提交内 MUST 把 `tests/contract/test_goal_definition.py` 的硬编码 9 元组扩为 10 元。

**实测**:`test_goal_definition.py:245-257`

```python
def test_help_labels_every_action_read_or_write(capsys):
    for action in ("create","validate","check-statement","list","status",
                   "objective","criteria","migrate","targets"):
        line = next((l for l in out.splitlines() if l.strip().startswith(action+" ")), None)
        assert line, f"--help lost the {action} row"
        assert line.split()[1].startswith(("read","write")), …
```

该元组**不是封闭断言**,故新增 `run-checks` **不会**使它转红——但新 action 会**处于零守卫状态**,正是 FR-046 禁止的形态。实跑 `goal-utils.py --help` 的 choices 行当前为 9 项 `{create,validate,check-statement,list,status,objective,criteria,migrate,targets}`。

`goal-utils.py:16-30` 有一份读/写动作 roster、`:32` 有退出码表(`0 ok | 2 input error | 3 not found | 4 validation failed`)——**二者都 MUST 被 US4 扩充**。其 docstring(`:2-14`)确实声明了 Program-First,但是**内联括注**形态(`:6-7` "Fixed rules belong in a program, not in a model (Constitution Principle XII / token-efficiency Program-First)"),而 `validate-tasks.py:4-6` 是**点名 owner 文件**的形态(`Program-First discipline (shared/guidelines/token-efficiency.md): …`)。STR-008 钉的是后者;FR-002 经 `/speckit.clarify` 裁定只辖**新增**检查器,故 `goal-utils.py` 的既有括注形态 MUST NOT 因本特性被改写。

---

## D-13 `goal-utils` 的退出码表**当前无任何钉子**;要抄的房子形态在 `test_trigger_engine.py`

**裁定**:US4 MUST 为 `goal-utils.py` 新建一张退出码表钉子,形态抄 `tests/contract/test_trigger_engine.py`;MUST NOT 用散落的字面量断言。

**实测**:`grep -rn "goal_utils.EXIT" tests/` → **无命中**(没有任何测试导入这些常量)。退出码目前以散落字面量断言:`test_goal_targets_check.py:136,145,157,163,169,177,186`、`test_goal_migration_path.py:114`。

房子已有的正确形态:`test_trigger_engine.py:48` `EXIT_CODES = {…}` + `:292` 循环逐 action 校验 + `:395` `assert sorted(action.choices) == sorted(ACTIONS)`(**封闭** roster 断言)。`test_trigger_engine.py` 与 `test_goal_definition.py` 的差别正在这里:前者封闭、后者不封闭。

**退出码取值(经 `/speckit.clarify` 裁定)**:`goal-utils.py:44-47` 的 `EXIT_OK = 0 / EXIT_INPUT_ERROR = 2 / EXIT_NOT_FOUND = 3 / EXIT_INVALID = 4` **原义全部沿用**,`blocked` 取 **5**。实测 `grep -rn "EXIT_[A-Z_]* = 5" scripts/python/` → 无命中;`5` 在 `scripts/python/` 全目录空闲。码 `1` 在 goal-utils 里未使用(同胞 `derive-utils.py:46`/`trigger-utils.py:43` 有 `EXIT_USAGE = 1`,goal-utils 没有),故 argparse 的用法失败(`parser.error` `:992`)当前落 exit **2**,与动作体内的 `EXIT_INPUT_ERROR` **不可区分**——这是**既有**冲突,本特性 MUST NOT 顺手改它(超出声明范围),但 MUST 在契约里写明 `run-checks` 不依赖该区分。既有调用方 `templates/commands/team.md:96,98` 只按 0/2 分支,不受影响。

---

## D-14 US5 的指代形语法:`[subjects: <glob>]`,冲突判据取「与花括号展开同现」

**裁定**:判据主体指代形取 `[subjects: <glob>]`(例:`[subjects: skills/draw-*/SKILL.md]`),glob 相对仓根、在**解析那一刻**导出成员集。FR-037 的冲突判据取:同一判据行内 `[subjects:]` 与**花括号展开记号** `\{[^}]*,[^}]*\}` 同现即报冲突。

**依据**:房子既有的行内方括号标签族——`[P]`、`[US<n>]`、`[blockedBy: …]`(`validate-tasks.py:54-61`)、US2 新增的 `[green: …]`(STR-001)、`requirements-template.md:173-176` 的 `[[STR-NNN]]`。方括号标签是可解析面的既有惯例,不引入新记号族。

**为何冲突判据取花括号展开**:FR-037 要求「同时使用指代形与成员枚举」报冲突,而**自由散文里的枚举不可机械判定**。实测本仓唯一真实的枚举型判据正是花括号展开形态——`.specify/goal/draw-two-layer-structure/goal.md:15`「七个绘图技能(draw-diagram 与 draw-{d3js,drawio,echarts,excalidraw,mermaid,plantuml})…」,其 `## History` 直接证明了 US5 要消灭的脆弱性:同一条判据随成员集变化被反复改写(`:36` 前值「六个绘图技能(draw-diagram 与 draw-{d3js,echarts,excalidraw,mermaid,plantuml})」、`:37` 前值「七个绘图技能(… drawio …)」)。故花括号展开是**实测到的**枚举形态,不是猜测。

**诚实声明的边界**:不带花括号的散文枚举(如「所有绘图技能」)与 `[subjects:]` 同现时**检不出**。这是可判定性的边界,记进契约,MUST NOT 声称覆盖了它。

**无既有形式可沿用(实测)**:`grep -n "glob\|\*/\|directory-reference\|<dir>\|rglob\|iterdir" shared/definitions/goal-definitions.md` → 无命中;该文件唯一的路径形态是存储位置(`:109-111`、`:46`、`:135`),从不作判据主体。`goal-utils.py` 里唯一的 `iterdir` 是归档枚举(`:765`)。

**该文件是概念 owner 而非被解析对象**:`goal-definitions.md`(137 行;镜像 `diff -q` 相同)不被任何程序解析,只被链接。程序化触点:`goal-utils.py:13`(仅 docstring 引用)、`test_goal_targets_engine.py:296` `AUTHORITY = ".specify/shared/definitions/goal-definitions.md"` + `:357` 断言、`test_confirmation_gates_sweep.py:169`(在门控扫描文件集内)、`test_goal_reference.py:150`。散文消费者 20 处(`grep -rl "goal-definitions" … | wc -l` → 20),含 `templates/commands/goal.md:19,75,82`、`templates/commands/team.md:89`、`docs/reference/commands/{goal,team}.md`。**故 US5 在该文件里增形式是新增一节,不改既有语义**;FR-038 的向后兼容由 SC-010 的名字级比对守住。

**运行期实况**:`.specify/goal/` 下**只有 1 个** goal(`draw-two-layer-structure/goal.md`,4337 B);`.specify/teams/` 下 6 个团队目录 + `.work/` + `.gitkeep`。只有 `draw-two-layer-structure` 与一个 goal 定义绑定。故 SC-010「对仓内**全部**既有 goal 定义跑一次解析」的当前全集就是 **1** 份——该数太小以致"名字级比对为空"近乎空真,MUST 配 FR-040 的反空真哨兵(至少断言被扫描的 goal 定义数 ≥ 1 且解析器确实产出了成员集)。

---

## D-15 US5 有**第二个**解析器,它刻意不 import

**裁定**:US5 MUST 在契约里显式处置 `skills/create-team/scripts/build-summary-input.py` 的本地解析器:要么让它同样理解指代形,要么显式声明它不理解并记录后果。MUST NOT 沉默。

**实测**:该文件 `:354-391` 自行解析 goal 判据,且 `:356-360` 明写这是**刻意**的——"This parses locally rather than importing `scripts/python/goal-utils.py` … cross-tree import breaks once installed"。它是 `skills/` 树内的脚本,安装后与 `scripts/python/` 不同树,故 import 会断。

**后果**:若指代形只被 `goal-utils.py` 理解,则 create-team 的摘要输入会对含指代形的判据给出不一致的解释。该文件另有自己的退出码表(`:41` `EXIT_OK, EXIT_INPUT_ERROR, EXIT_NO_MATERIAL = 0, 2, 3`、`:44` `EXIT_SERIALIZED = 4`),其 `3`/`4` 与 `goal-utils` 的 `EXIT_NOT_FOUND`/`EXIT_INVALID` **语义相左**——即仓内已有**第五套**退出码约定(见 § 上送与披露 A-3)。

---

## D-16 门控预算:零整数余量,**17** 条阻塞模式,9 个断言点 + 4 个元钉子

**裁定**:本特性对门控预算的处置取**设计规避**(零命中 + 扫描器零改动 + total 与冻结基线相等),与 052 同策。任何新增措辞 MUST 逐条对 `BLOCKING_RE` 实跑核验为 0 命中后才落盘。

**实测**:`scan-confirmation-gates.py` 的 `SCAN_DIRS = ("templates/commands","skills","shared")` `:35`;`SCAN_ROOT_FILES = ("templates",)` `:36`(glob `templates/*.md` 非目录项,`:90-95`);`SKIP_DIR_PARTS = {".specify",".claude",".qoder",".github",".opencode","__pycache__",".archive"}` `:37`;`SELF_REL = Path("shared/guidelines/confirmation-gates.md")` `:38`;`POLICY_DOCS` 2 项 `:41-44`;`BLOCKING_PATTERNS` **17** 条 `:46-64`;`BLOCKING_RE` `:65`。实跑:`blocking confirmation gates: 23 / destructive: 13 / governance_kept: 10 / violations: 0`。镜像 `.specify/scripts/python/scan-confirmation-gates.py` 相同。

**暴露面**:`templates/tasks-template.md` 经 `SCAN_ROOT_FILES` **在扫描面内**(US2 要改它),`shared/` 全树在扫描面内(US1 要改 `requirements-guidelines.md`、FR-014 要改 `clarify-taxonomy.md`、D-1 要新建 owner 文档),`templates/commands/` 在扫描面内(US1/US2 要改 `requirements.md`、`tasks.md` 两个命令模板)。整数余量为 **0**。

**钉子的真实规模(订正子代理的"三处"表述)**:「三处不同形态」对**形态**成立、对**站点**不成立。三种形态:① 硬编码字面量 `test_user_facing_comprehension_doc.py:576` `assert payload["total"] == 23`;② 与冻结基线相等 `test_proactive_trigger_section.py:352` `assert payload["total"] == frozen["total"]`(冻结值 `.specify/specs/050-proactive-flow-trigger/baseline-gates.json:15` `"total": 23`);③ 派生上限 `test_confirmation_gates_sweep.py:161-162` `cap = baseline["total"] * 0.25` / `assert payload["total"] <= cap`(基线 `.specify/specs/044-reduce-confirmation-flows/baseline.json:2` `"total": 93` → 23.25)。

另有 `test_fast_fail_discipline.py` 的 5 个站点:`:1654` `assert frozen["total"] == 23`、`:1801`(形态②的副本)、`:1821` `…["confirmationGates"]["total"] == 23`、`:1822` sweep 源 `== 93`、`:1830` `assert (gate["total"], gate["destructive"], gate["governanceKept"]) == (23, 13, 10)`;以及 `:1809-1820` 的 **4 个元钉子**,它们**正则匹配上述三个形态站点的源码文本**(`assert re.search(r'payload\["total"\] == 23', ufc)` 等)——**改动任一钉子的措辞就会打红一个元钉子**。合计 9 个断言站点 + 4 个元钉子。

---

## D-17 镜像义务清单:**唯一拥有者是 `plan.md` § Mirror Obligations**

**裁定**:镜像义务表**不在本文件复写**。其唯一拥有者是 `plan.md` § Mirror Obligations(12 行,逐对给出改前实测退出码与判据形态);本条只记录 Phase 0 得到的、支撑那张表的**机制事实**。

**为何改为引用而不是两处各留一份**:初版本文件曾有一份 11 行的镜像表,与 `plan.md` 的 12 行**已经分叉**(前者漏了 `templates/commands/team.md` ↔ 4 个逐工具副本那一对),而它自称是「供 tasks 展开为成对任务」的输入——一份分叉的表会让 `tasks.md` 少排一对写入+核验任务,并在实现后把 `regen-command-copies.py --check` 打红。这正是唯一真源纪律要防止的形态:改一个事实需要改两个文件,就已经破了。

**支撑该表的机制事实(实测)**

- `sync-mirrors.py:72-78` 的 `MIRROR_PAIRS` 共 **5** 对:`templates → .specify/templates`(**排除** `commands`)、`skills → .specify/skills`(排除 `site`)、`agents → .specify/agents/templates`、`scripts → .specify/scripts`(`strict_extras=True`)、`shared → .specify/shared`。`test_fast_fail_discipline.py:1923` 钉 `len(mod.MIRROR_PAIRS) == 5`。
- `--only` 接受**可重复的仓相对路径前缀**(`:116-119`,docstring 示例 `:23` 即 `--only scripts/python/feedback-utils.py`);不匹配任一对前缀或 `templates/commands/` 则 exit 2(`:141-149`);除非目标是 `templates/commands`,否则跳过 regen 委托(`:204-206`)。字节比较用 `filecmp.cmp(..., shallow=False)`(`:106`)。
- `templates/commands/` **无 `.specify/` 镜像**(该对已退役),命令模板只经 `regen-command-copies.py` 扇出到 **4** 个逐工具副本目录。
- 一致性由**引擎级**测试保证、无逐文件枚举:`tests/contract/test_scripts_distribution_parity.py::test_repo_has_no_orphan_or_drifted_scripts`(`:71-87`)跑 `sync-mirrors.py --check` 并断言 exit 0(核心断言 `:79`);`test_scripts_pair_is_strict_about_orphans`(`:39-46`)钉 `strict_extras=True`;`test_trigger_engine.py:220-225` 有一份重复的全局检查。
- 打包:`pyproject.toml:32-37` 的 `[tool.hatch.build.targets.wheel.force-include]` 把整个 `scripts` 树映射到 `specify_cli/scripts`,故新脚本自动随包(`skills` 刻意不在其中,由 `src/hatch_build.py:23-24,38-39` 分级)。
- 逐对改前实测退出码与「哪几对需要相对判据、哪几对可用绝对判据」见 `plan.md` § Mirror Obligations 的 Verify 列;其中包含一处对 052 期旧结论的订正(`regen-command-copies.py --check` 已从「大量待再生」变为 **EXIT=0** 全清)与一处测量陷阱(经 `| tail` 取 `$?` 得到的是 `tail` 的码)。

## D-18 尚未创建制品的核验策略(执行核验规则)

**裁定**:凡本阶段写进任一制品的可执行命令示例,分两类处置——

1. **改前即可实跑的**(对既有脚本、既有制品的只读命令):本阶段**已实跑**,真实输出已粘贴。本文件内所有 `grep`/`sed`/`find`/`python3` 命令与 `validate-tasks.py`、`goal-utils.py --help`、`scan-confirmation-gates.py --summary` 的调用均属此类。
2. **依赖尚未创建制品的**(对 `validate-requirements.py`、`account-clause-coverage.py`、`run-checks`、owner 文档的调用):**改前不可实跑**,逐例标注其**所依赖的前提**(假定的旗标、ID 形态、计数、文件位置、工具行为),使 `/speckit.tasks` 与 `/speckit.implement` 知道该**重测**哪些事实而不是继承它们。文件级免责声明 MUST NOT 用来兜住未逐个标注的示例。

**依据**:`/speckit.plan` 的 Post-Generation Quality Gate 明文规定「A **file-level** disclaimer … does NOT discharge this rule for the examples it does not cover」且「A disclaimer MUST also list the premises that example rests on」。052 plan 期曾因此查出 3 处「印了派生命令或数字却没实跑」的同类缺陷,本特性 MUST NOT 重蹈。

**基线冻结策略**:三组基线在实现开工时冻结并落盘本特性目录——① 全量测试的**名字级**失败集(`run-tests.sh --names-out`,SC-012);② 门控 total(`scan-confirmation-gates.py --summary`,SC-012 / FR-045);③ 覆盖核算的**未覆盖项名字集**(D-10,FR-027)。改前实测参考值:测试 **65 failed / 2927 passed / 2 skipped**(名字集与 052 冻结基线 md5 相同)、门控 total **23** / violations **0**。

---

## 上送与披露

### 本轮子代理回传的显式异常行(逐条处置)

- **A-1**(`shared/constants/clarify-taxonomy.md:95,104`):该处记录 `checklists/requirements.md`「carries derived counts (how many FR / SC / STR / Entity / Story rows)」且「the full count set」的 owner 是 `shared/guidelines/requirements-guidelines.md` § Create Spec Quality Checklist——但**该 owner 节(`:9-48`)不定义任何计数字段**,实测其为一个固定 16 项清单、无派生计数位。**处置:上送,未就地修**。这是一个 owner 指针悬挂,两种读法都成立(要么该节应定义计数集,要么指针应改指别处),属**裁定**;且它不在 053 的声明范围内。它对本特性的影响已如实记入:US1 的检查器**无法**从被声明的 owner 派生计数集,故 FR-013 的落点改为在 § Validation Process 写明「计数由检查器派生」,而不假称既有 owner 已定义计数。
- **A-2**(`.specify/memory/features.md:36` vs `templates/commands/team.md:127`):两处对 goal **摘要存据目录**的记录互相冲突,且二者都未落盘(实测:前一条所指的目录不存在,`find .specify -maxdepth 4 -type d -name summary` → 空)。**本条刻意不复现任何一侧的路径字面量**:其中一侧正是 `tests/contract/test_goal_migration.py:19` 的 `OLD_PATH_NEEDLE` 禁止出现在任何 live-face 文件里的迁移前旧路径,而该守卫的豁免集(`HISTORICAL_PREFIXES` `:40`、`GUARD_FILES` `:55`)不覆盖 spec 制品——**复现它会让本文件自己成为该守卫的一个 offender**。本轮实测到了这一点:初版把两侧路径都抄了进来,`test_no_live_face_file_retains_the_old_path` 随即转红并逐字点名本文件;改为只给坐标后转绿。需要具体路径时按上面两个坐标去读原文。**处置:上送,未就地修**——需裁定哪条是真源,且超出 053 范围。对本特性无影响(053 不触及摘要存据)。
  **可推广的一类(举一反三)**:凡「某字面量禁止出现」型守卫,都会被一份**为了报告它而引用它**的文档打红——与 clarify 轮那个「为描述不可解析引用而裸写 `[[STR-014]]`,于是它自己成了一个不可解析引用」是同一类。判据:**报告一个被禁形态时 MUST 给坐标而不是给实例**;若确需实例, MUST 先确认该守卫的豁免集覆盖本文件,否则先扩豁免集(属上游裁定)或改为坐标引用。
- **A-3**(`scan-confirmation-gates.py --baseline` 的比较形态):读基线**顶层** `total` 而冻结值嵌在 `confirmationGates` 下,退出码只反映 `violations`,故作为相等门不可用。已被记录两次(`constitution.md:14` 后续 TODO (a);052 的 `contracts/gate-neutrality.md` + `verification.md:209`)而**上游仍未修**。**处置:已记入 D-10 作为本特性的 MUST NOT**,不就地修上游。
- **A-4**(子代理对 `.yaml` 形态的误判):探查子代理报「10 份 `.yaml` 全部是 OpenAPI」且判据为「无字面 `operations:` 键」。**编排者重导后证伪**:实为 9 份 OpenAPI + 1 份 `assertions[].id` 结构化断言(文件名恰为 `.openapi.yaml`),而 OpenAPI 的 operation 是 `paths:` 下的 HTTP 方法键、本就不是一个字面键名。**处置:已订正**,并回写进规格 FR-028(MUST NOT 以 `operations:` 键名作探测条件)。
- **A-5**(子代理对「三处钉子」的表述):形态数 3 正确、站点数不止 3。**处置:已订正**为 9 个断言站点 + 4 个元钉子,见 D-16。
- **A-6**(`goal-utils.py` 的第 8 个 verdict 字面量 `rejected`):不在 STR-006 的 7 个字面量内。**处置:已订正**——经实测确认 `rejected` 只由 `check-statement`/`targets --check` 发出、与五项检查无关,故 STR-006 的「7 个」是 `run-checks` 的词表而非该二进制的全词表;该精度已回写进规格 STR-006 行,MUST NOT 因本特性删改 `rejected`。
- **A-7**(FR 侧有没有一份基线 — 2026-10-03 第二轮 `/speckit.analyze` 的校验波提出,登记而未裁定):C-21 冻结的名字集按 `contracts/*` 的**条款名**建键,故它天然只承载条款侧;而 T025 要求「两侧都 empty-beyond-baseline」、FR-027 § 基线面 也只写了条款侧。于是既有 spec 的 **FR 欠账没有豁免通道**。实测(本轮自己跑的,不继承子代理的数;抽取按 C-2 的三条规则:块边界 + 引用组 + 区间展开):44 个 spec 目录都声明了 FR,FR 定义行合计 **812** 条;其中 **38** 个目录的契约里**没有任何引用组提到 FR**(即 FR 侧全集几乎全部未覆盖,按 FR-026 的新读法会永久报红)。**两种读法都成立、都需要一个新决定**:① 给 FR 侧另立一份以 `<spec 目录>/FR-nnn` 限名的基线(代价:要与 FR-027 首句「MUST NOT 要求改造既有 spec 的契约文件」并存,并给 C-21/C-23 加一个第二名单);② 把 FR 侧核算限定在 `--spec-dir` 指定的单个 spec 内、并从 T025 的措辞里去掉「beyond-baseline」(代价:FR 侧从此没有跨仓欠账视图)。**处置:上送**——本特性不在 analyze 阶段发明未记录的意图;`data-model.md` E-3c 的 `universe` 字段已就地标注此未决点。**(2026-10-04 US3 实现期的落点披露,不是裁定)**:`account-clause-coverage.py` 的 FR 侧按**读法 ②** 落地——全集取 `--spec-dir` 那一份 `requirements.md` 的 FR 定义行,被认领子集取该 spec 自己契约的条款引用组,因此 FR 侧**没有**跨仓欠账视图、也**没有**第二份基线。选 ② 不是在这里发明意图:FR-026 写的是「`requirements.md` 的 FR 定义行」(单数、本 spec 的)、C-18 写的是「FR 侧的 verdict 与任务行无关」、GATE-8 举的实测是「本特性自己的 48 条 FR 全部已被引用组引到」,三处都已预设 FR 侧按单 spec 取全集;读法 ① 要求的第二名单在任何下游制品里都没有落点。故 ① 仍是**可加**的未决项(加上它不会推翻 ②,只会多一个跨仓视图与一份新基线),上送状态不变。
- **A-8**(OpenAPI 形态的条款 id 不唯一 — 2026-10-04 US3 实现期由实跑发现,登记而未裁定):owner 文档声明 `yaml-openapi` 的「条款 = `paths:` 下的 HTTP 方法键」,而**一个文件可以在多个 path 下声明同一个方法**,故方法键在文件内**不是唯一标识**。实测(全仓 `.specify/specs/*/contracts/*`,以 `clause_extract.py` 重导):抽出 id 合计 **689**,而按 `<spec>/<契约>#<条款 id>` 建**名字集**只得 **665**,**24** 个 operation 与同文件的另一个共用一个名字,分布在 **8** 份 OpenAPI 契约里(最多的一份 5 个 `get` 共用一个名字)。后果:覆盖核算的分母比 id 数小 24,而一条 `[green: …#post]` 认领会一次覆盖该文件的全部 `post` operation。**两种读法都成立、都需要一个新决定**:① 把该形态的条款 id 限定为 `<path>.<method>`(唯一,但改的是 owner 声明的**语法**,并要同步 `test_clause_forms.py` 里「id 属于七个方法名之一」那条断言与普查的逐形态 id 语义);② 保持方法键为 id、由核算器对重复名加**出现序号**消歧(不改 owner 语法,但序号不携带语义,且 `[green:]` 认领面无法据此精确指认一个 operation)。**处置:上送,并在实现期就地做了不掩盖的那一半**——核算器**同时印出** id 数与去重后的名字数,并在二者不等时印一行说明其成因与归属(判据由 `tests/contract/test_clause_coverage.py::test_c7b_ids_that_collapse_into_one_name_are_reported_never_absorbed` 钉住,用一份含两个 `post` 的最小 OpenAPI 制品取证)。理由:选择 id 语法是 owner 文档的权限,一次核算运行 MUST NOT 悄悄替它决定;但让分母**静默**少 24 恰是 FR-025 要消灭的「空因为盲」下沉到条款标识这一层,故先把差值变成印出的事实。基线在头部记录抽取规则版本(C-23),正是为了将来选定 ① 或 ② 之后可以重冻而不与旧基线混比。

### 编排者自身在本轮查出并订正的缺陷

- **规格印出的条款形态分布为假**。`/speckit.clarify` 轮(同日)印「可解析面 31 / 110、其余 79 份 `.md` 无任何机器可抽取形态」。重新分类后实测为**可解析 57 / 110、残余 53 份**:`## C-N` 标题形(**25** 份、141 个 id)与 `**C-N (标签)**` 括注形(**1** 份、10 个 id)同样机器可抽取,而原测量只认闭合粗体。79 = 100 − 21,即「`.md` 中不含闭合粗体者」,并非「无任何机器可抽取形态者」。已按**追加**方式订正规格(FR-022、FR-023、SC-006 Source、现状锚点行、`## Clarifications` 第 3 条加日期化注解而决定原文不动),并同步订正清单、`features/053.md`、`features.md` 的 053 行;取证落盘 `notes/clause-form-census.md`。**该假数曾出现在提交给用户的一个裁定问题的框定语里**;裁定本身不受影响(残余量级 79 → 53 不改变「不产生永久豁免清单」这一取舍理由),但已如实披露。
- **一次探针设计错误**。D-7 的第一次探针让 T001 不带 `[P]`,而 `parallel-safe` 只在两个 `[P]` 行之间触发,故误得「无告警」并一度判子代理的推断为假。补正样本对照后复现了假告警。**教训:探一个"某检查不会误报"的命题,必须先证明该检查在正样本上会报**——否则探到的是检查没被触发,不是检查没误报。这与 FR-040 的反空真哨兵是同一纪律的两个方向。
- **第五种条款形态由该次重测才暴露**:`.specify/specs/031-task-complexity-rubric/contracts/rubric-section.md` 用 `- **C-1 (heading)**`,闭合 `**` 在括注之后,故 `\*\*C-\d+(?:\.\d+)*\*\*` 不命中而 `\*\*C-\d+` 命中。任何只写闭合粗体正则的抽取器会静默漏掉这 10 条条款——正是 FR-025 要区分的「空因为盲」在**单形态**粒度上的形态。已记入 `notes/clause-form-census.md`。

### 一条本轮踩到三次的形态陷阱:命令的 cwd 前提 MUST 与命令同处一行

同一个 run 内三次因 cwd 而得到错值:① `notes/clause-form-census.md` 的普查命令是**仓根相对**,从 spec 目录跑会**静默返回 `(0, 0)`** 而不报错;② `plan.md` 的 Contracts 行把两条 **spec 目录相对**的命令标注成「MUST 从仓根跑」,方向反了;③ 编排者复核时又一次从 spec 目录跑仓根相对路径而得 `FileNotFoundError`。

**可推广的判据**:一条印在制品里的命令,若其路径是相对的,则该命令的**cwd 前提与命令本身是不可分割的一条信息**——分开写就等于让下一个读者去猜,而猜错时**有两种失效形态**:报错(可见)与静默给出 `0`/空(不可见)。后者危险得多,因为 `0` 看起来像一个合法测量值。
**规则**:制品内每条相对路径命令 MUST 在同一行或紧邻行注明 cwd;凡「合法值可能就是 0 或空」的命令,MUST 另配一个证明该命令**确实扫到了东西**的伴生量(与本特性 FR-040 的反空真哨兵是同一条纪律,只是对象从「集合为空」换成「命令没跑对地方」)。

### 范围外、记入 Feature 详情而不纳入本计划的欠账

1. **退出码表在仓内无 owner**:`derive-utils.py` / `goal-utils.py` / `interview-utils.py` / `trigger-utils.py` 四个脚本各自重复定义同一张 `EXIT_OK=0 / [EXIT_USAGE=1] / EXIT_INPUT_ERROR=2 / EXIT_NOT_FOUND=3 / EXIT_INVALID=4`,而 `shared/`、`templates/`、`docs/` 三处对该表的命中数为 **0**;`skills/create-team/scripts/build-summary-input.py` 另有第五套(`3=NO_MATERIAL / 4=SERIALIZED`)且 3/4 语义相左。本特性只在 D-13 局部回避冲突。
2. **`Consumed by` 列的反向检查全仓无守卫**:`/speckit.clarify` 轮实测该列有 7 处「点名了却未引用」,而模板的引用公约只保证**正向**可解析。US1 的检查器是它最自然的落点,但未纳入 FR 以免扩大范围。
3. **无任何机器可辨条款形态的 `.md` 契约**:本特性以冻结名字级基线留档可见,收敛机制不在范围内;其规模随 owner 声明的覆盖面而变,两个端值的当前实测由 `notes/clause-form-census.md` 拥有(本条不复写)。
