# Contract: 中立性、预算中立与不新增机制

**Requirement**: `053-machine-decidable-artifacts` → Feature 053  
**Covers**: FR-044(模板中立)、FR-045(门控预算)、FR-048(不新增机制)  
**Clause form**: `**C-N**` 行首裸粗体。  
**Class labeling**: 同 `contracts/checker-form.md`([制品类] / [行为类])。

---

## 模板中立

**C-1** [制品类] `templates/` 下新增的一切内容 MUST 项目中立:MUST NOT 含 `spec-kit` / `specify-cli` / `specify_cli` / `cloud-native-ai` 一类本仓专名。判据:对本特性在 `templates/` 下的**新增内容**做专名 grep,命中数为 **0**;SC-012 把它与门控 total、名字级基线并列为三项。(FR-044、SC-012)

**C-2** [制品类] 本特性在 `templates/` 下的落点为两处:`templates/tasks-template.md`(FR-015 的归属声明面)与 `templates/commands/{requirements,tasks}.md`(FR-012 与 US2 的接线)。二者 MUST 同受 C-1 约束;判据逐文件给出而不是合并计数。(FR-044、D-17)

**C-3** [行为类] 契约与脚本内的**举例**若必须指名一份真实制品(如 C-11 的 `013-portable-skill-creation` 契约、`031-task-complexity-rubric` 的括注形实例),该举例 MUST 落在 `.specify/specs/053-…/contracts/` 或 `scripts/` 的注释里,**MUST NOT** 落在 `templates/` 下——spec 目录是本仓私有的,模板是出厂的。(FR-044、FR-021)

## 门控预算中立

**C-4** [制品类] 本特性落地后 `scripts/python/scan-confirmation-gates.py --summary` 的 total MUST 仍为 **23**、violations MUST 为 **0**。改前实测(本轮实跑):`blocking confirmation gates: 23 / destructive: 13 / governance_kept: 10 / violations (reversible gates still blocking): 0`。(FR-045、SC-012)

**C-5** [制品类] 整数余量为 **0**:cap = `baseline["total"] * 0.25` = 93 × 0.25 = **23.25**(基线 `.specify/specs/044-reduce-confirmation-flows/baseline.json:2` 的 `"total": 93`),故 total 只能 ≤ 23。任何新增措辞若使 total 变为 **24** 即为违例,没有「加一条再调 cap」的余地。(FR-045、边界情形)

**C-6** [制品类] 上限由**三种形态**的断言钉住,合计 **9** 个断言站点另有 **4** 个元钉子:① 硬编码字面量 `test_user_facing_comprehension_doc.py:576` `assert payload["total"] == 23`;② 与冻结基线相等 `test_proactive_trigger_section.py:352` `assert payload["total"] == frozen["total"]`(冻结值 `.specify/specs/050-proactive-flow-trigger/baseline-gates.json:15`);③ 派生上限 `test_confirmation_gates_sweep.py:161-162`。另有 `test_fast_fail_discipline.py:1654, 1801, 1821, 1822, 1830` 五个站点,以及 `:1809-1820` 的 4 个元钉子——它们**正则匹配上述三个站点的源码文本**(`assert re.search(r'payload\["total"\] == 23', ufc)` 等),故改动任一钉子的措辞即打红一个元钉子。(FR-045、D-16)

**C-7** [行为类] 唯一合法的满足路径是**措辞设计回避命中**:MUST NOT 放宽被扫描文档集(`SCAN_DIRS` / `SCAN_ROOT_FILES` / `POLICY_DOCS`)、MUST NOT 调高上限、MUST NOT 修改任何基线数据、MUST NOT 改写钉子的措辞(会打红元钉子)。(FR-045)

**C-8** [制品类] 暴露面实测:`SCAN_DIRS = ("templates/commands", "skills", "shared")`(`:35`)与 `SCAN_ROOT_FILES = ("templates",)`(`:36`,glob `templates/*.md` 的非目录项,`:90-95`)意味着本特性触及的以下落点**全部在扫描面内**——`shared/definitions/contract-clause-definitions.md`(新建)、`shared/definitions/goal-definitions.md`、`shared/guidelines/requirements-guidelines.md`、`shared/constants/clarify-taxonomy.md`、`templates/tasks-template.md`、`templates/commands/requirements.md`、`templates/commands/tasks.md`。`SKIP_DIR_PARTS`(`:37`)含 `.specify`,故本 spec 目录下的契约文件**不在**扫描面内。(FR-045、D-16)

**C-9** [制品类] 措辞回避的判据是 `BLOCKING_PATTERNS`(`:46-64`,实测 **17** 条)与 `BLOCKING_RE`(`:65`):每个在扫描面内落盘的新增/修改文件 MUST 逐条对 `BLOCKING_RE` 实跑核验为 **0** 命中后才算落地。判据:核验命令与输出记入本特性 `verification.md`。(FR-045)(2026-10-03 订正:此处曾印 **18** 条——该数在本仓已被订正过两次(`051` 记录 18→17、`052` 全程用 17、且有测试断言 `== 17`),而 `plan.md` § 第三轮缺陷清单第 2 项声称「7 个位置已全部订正」,本契约正是那 7 个位置里唯一漏改的一处,故此处不只是数字错、还证伪了一条完成性声明。AST `literal_eval` 实测:`len(BLOCKING_PATTERNS) == 17`。)

**C-10** [行为类] 扫描器本身 MUST 在本特性窗口内**零改动**。判据:对 `scripts/python/scan-confirmation-gates.py` 与其镜像做 `git diff`,窗口内为空(与 052 的同名判据同形)。(FR-045)

## 不新增机制

**C-11** [制品类] 本特性 MUST NOT 新增任何门控停等点。判据:对本特性触及的全部文件做 `BLOCKING_RE` 核验为 0 命中(与 C-9 同一取证,不同命题:C-9 守预算,C-11 守「不新增停等」)。(FR-048)

**C-12** [制品类] 本特性 MUST NOT 改变 `/speckit.*` 的阶段划分或状态机。判据:`shared/workflow/feature-integration.md` § Status State Machine 的命令→迁移表在本特性窗口内**逐字不变**(`git diff` 为空);`templates/feature-details-template.md` § Canonical Status State Machine 同。(FR-048)

**C-13** [制品类] 本特性 MUST NOT 引入守护进程或文件监听。判据:新增脚本源内对 `watchdog` / `inotify` / `while True` + `sleep` 一类轮询形态的 grep 命中数为 **0**;全部新增脚本 MUST 是「一次调用、一次输出、退出」的形态。(FR-048)

**C-14** [制品类] 检查器只由**两条**通道触发:由一个 `/speckit.*` 命令在其既有步骤内调用,或由测试直接调用。该枚举与 A-2 是同一封闭集;MUST NOT 接入 CI 或任何其它自动触发面——实测本仓当前无任何 CI 配置(`.github/workflows/` 不存在),故 CI 不是一个可用通道。(FR-048、A-2)

**C-15** [行为类] FR-012 与 FR-013 的接线 MUST 落在**既有步骤内**,MUST NOT 为检查器新造一个命令阶段:实测 `/speckit.requirements` 的验证步骤当前为 `templates/commands/requirements.md` step 7(`:62-66`),US1 在该步骤内增调用;`/speckit.tasks` 的结构校验当前为 `templates/commands/tasks.md` step 5(`:76`),US2 沿用该步骤而不新增。(FR-012、FR-048)

## 名字级基线

**C-16** [制品类] 全量测试 MUST 相对**开工时冻结的名字级基线**比对,新增失败集为空。基线用 `run-tests.sh --names-out <file>` 采集(实测该旗标位于 `scripts/bash/run-tests.sh:22-24,29,35-43`:`:41` 以 `grep "^FAILED" | sed 's/^FAILED //;s/ - .*//' | sort` 写文件,`:42` 向 stderr 印 `# failed-name list written: <file> (<N> entries)`,`:43` 透传 pytest 退出码),记入本特性目录。(SC-012、D-10)

**C-17** [行为类] 该脚本**不**存基线、**不**跑 `comm`;`comm -13` 是文档化的消费者习语(`:23` 注释、`templates/tasks-template.md:80` 的 GATE-1)。故本特性的三组基线(测试名字集 / 门控 total / 未覆盖项名字集)MUST 各自落盘并各自用 `comm` 或等价集合比较消费,MUST NOT 假称引擎会代劳。(SC-012、FR-027、D-10)

**C-18** [制品类] 计数比较 MUST NOT 作为判据:SC-010 与 SC-012 均明文「按名字比对而非按计数」。判据:本特性全部三组基线的核验命令里出现 `comm -13`(或等价的集合差),MUST NOT 出现两个整数的相等/相减断言作为**唯一**判据。(SC-005、SC-010、SC-012、V-11)

**C-19** [行为类] 改前参考基线(本轮实跑,非实现期冻结值):全量测试 **65 failed / 2927 passed / 2 skipped**,其名字集与 052 冻结基线 **md5 相同**(`02177c0e6e5961c880f73d932007df92`),即这 65 项是先于本特性存在的镜像漂移一类既有失败;门控 total **23** / violations **0**。实现开工时 MUST 重新冻结,MUST NOT 直接沿用本行数字。(SC-012、D-18)
