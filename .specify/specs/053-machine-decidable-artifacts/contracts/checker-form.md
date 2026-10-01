# Contract: 检查器的共同形态与证据纪律

**Requirement**: `053-machine-decidable-artifacts` → Feature 053  
**Covers**: FR-001…FR-005(检查器形态与 Program-First 归属)、FR-039…FR-043(机器给出的绿:证据纪律)、FR-046(钉子)、FR-047(镜像安装)  
**Clause form**: `**C-N**` 行首裸粗体(D-1 的 owner 文档将把它声明为规范形之一)。  
**Class labeling**: 每条条款标注 **[制品类]**(断言落盘文本:文件存在、标题恰好一次、定界区间逐字节相等——可由契约测试机械断言)或 **[行为类]**(描述运行期动作,其中无制品可观测者只能由真源文档载明义务 + 评审强制 + 变异演练取证)。该二分取自 `.specify/memory/glossary.md` 已登记的「制品类/行为类条款 (Artifact-Class vs Behavior-Class Clause)」;MUST NOT 声称行为类条款「由守卫覆盖」。

---

## 单一入口与参数形态

**C-1** [制品类] 每个新增检查器 MUST 是 `scripts/python/` 下的单一入口可执行脚本,以被校验制品的路径为位置参数。判据:脚本存在、`main(argv=None) -> int` 可被 `importlib` 载入并直接调用(与 `validate-tasks.py:280` 同形)。(FR-001)

**C-2** [行为类] 检查器 MUST NOT 要求调用方先读入制品内容再自行判断;判定所需的一切 MUST 由脚本自己从路径读取。取证:契约测试以路径为唯一实参调用 `main()` 并断言退出码,不预先注入文本。(FR-001)

**C-3** [制品类] 检查器 MUST 提供 `--json` 旗标(`store_true`),且该旗标与人读输出二者的判定 MUST 一致——同一份制品在两种输出下 MUST 得到同一个 `status` 语义。判据:契约测试对同一制品跑两次并比对。(FR-003)

## Program-First 归属声明

**C-4** [制品类] 每个新增检查器的模块 docstring MUST 以 STR-008 的字面量 `Program-First discipline (shared/guidelines/token-efficiency.md)` 起首其归属段,即**点名 owner 文件**,而不是内联括注。判据:对脚本源 grep 该字面量,命中数 ≥ 1。(FR-002)

**C-5** [制品类] 该 docstring MUST 逐项列出它执行的检查及各自判据,体例为**两空格缩进 + 标签 + ≥2 空格 + 描述**——因为既有钉子从 docstring 抽取标签(`tests/contract/test_validate_tasks_parallel_safety.py:312` 的 `^  ([A-Za-z][A-Za-z-]*)\s{2,}`),偏离该体例会让抽取静默漏项。判据:抽取式对新脚本 docstring 的命中集 == 该脚本的 `EXPECTED_CHECKS`。(FR-002、FR-042、D-5)

**C-6** [行为类] 既有 `goal-utils.py` 的 docstring 用的是**内联括注**形态(`:6-7`),而 FR-002 经 clarify 裁定只辖**新增**检查器,故本特性 MUST NOT 改写它的既有归属声明形态。(FR-002、D-12)

## 机读输出键集

**C-7** [制品类] 新增检查器的 `--json` 输出 MUST 含:被校验制品路径、**逐项检查的 verdict 数组**、error 计数、warning 计数。判据:契约测试断言四个键在场且 verdict 数组长度 == 该脚本的检查项数。(FR-003)

**C-8** [制品类] 人读输出的计数尾行形态 MUST 为 STR-003 `0 error(s), 0 warning(s)`(数字随实况变化,形态不变)。判据:对尾行做正则匹配 `^-?\d+ error\(s\), \d+ warning\(s\)` 的同构式。(FR-003)

**C-9** [制品类] 先例 `validate-tasks.py --json` 只发 `file` / `errors` / `warnings` / `status` 四键、**无**逐项 verdict 数组(`:302-308`);该四键形态 MUST NOT 因本特性被要求迁移。判据:契约测试断言既有四键仍在场,且**不断言**新增数组存在于该脚本。(FR-003、clarify 裁定 4)

## 三种失败形态互相可区分

**C-10** [制品类] 检查器 MUST 对「被校验文件不存在」「被校验文件不可解析」「被校验文件为空或仅含模板骨架」三种情形给出互相可区分的退出码**或** verdict,MUST NOT 混为同一失败形态。(FR-004)

**C-11** [制品类] 新增检查器的退出码沿用先例三档:`0` 无 error(允许 warning)/ `1` ≥1 error / `2` 文件缺失或不可解析或无内容行;第三态「为空或仅模板骨架」以 `status` 的**第四取值**表达,MUST NOT 为此新增第四个退出码。判据:退出码表钉子逐档断言(含 warn-only → 0),`status` 取值集钉子含第四值。(FR-004、D-6)

**C-12** [行为类] 「为空或仅模板骨架」的判据 MUST 由真源文档载明(哪些占位符形态算骨架),因为它是语义判断而非纯结构判断;其取证为一份只有占位符的最小制品被拒绝而不是 exit 0。(FR-004、边界情形)

## 只读性

**C-13** [制品类] 所有检查器(含既有的)MUST 是只读的:判定只经 stdout 与退出码表达,MUST NOT 修改被校验制品或任何仓内文件。判据:对脚本源做写入点扫描(`write_text|mkdir|open(`),每个命中点 MUST 可归属到一个写动作;新增检查器的命中数 MUST 为 **0**。(FR-005、V-2)

**C-14** [行为类] 只读性的取证 MUST 是一次写入点扫描加一次调用前后的字节校验和对比,MUST NOT 只凭 docstring 自陈「read-only」。(FR-005、V-2)

## 证据纪律:逆样本

**C-15** [行为类] 本特性新增的**每一项**检查 MUST 有逆样本取证:证明被守物真的坏掉时该检查会变红。只展示正常路径的取证不被接受。判据归属:`.specify/shared/guidelines/fast-fail.md` § 判据同样覆盖机器给出的绿。(FR-039)

**C-16** [制品类] 逆样本数 MUST ≥ 新增检查项数,且清单落在本特性 `verification.md`。判据:对清单行数与被钉标签集的新增子集做数量比较。(FR-039、SC-011)

**C-17** [行为类] 逆样本 MUST 建在临时目录,MUST NOT 落在 `.specify/specs/` 下;演练结束后残留计数 MUST 为 **0**,并以一次 `find` 实测取证。(FR-041、SC-011、SC-001 Source)

**C-18** [行为类] SC-001 的命中率判据是 **4/4 且零交叉遮蔽**:四份各只破坏一类命题的副本,各自只报出对应那一类。取证 MUST 逐份贴出被点名的检查项与退出码。(SC-001)

## 证据纪律:反空真哨兵与变异演练

**C-19** [制品类] 凡断言「某集合为空」的检查(未覆盖集、不可解析集、冲突集),MUST 在同处配一条断言**必须非空的伴生量**的检查,使「空因为对」与「空因为盲」可区分。判据:契约测试同时断言空集与伴生量 > 0。(FR-040)

**C-20** [行为类] 凡守卫**负面命题**的检查项(某物不存在 / 未变化 / 未泄漏),其取证 MUST 含一次变异演练:弄坏被守物 → 确认变红 → **精确反向替换**复原 → 确认恢复绿,并复核复原后该文件的差异回到预期形态(`diff -q` 与备份 BYTE-IDENTICAL 是合法形态)。(FR-041)

**C-21** [行为类] 探一个「某检查不会误报」的命题时,MUST 先证明该检查在**正样本**上会报;否则探到的是「检查没被触发」而不是「检查没误报」。依据:本特性 plan 期的一次探针即因漏掉 `[P]` 而误判(见 `research.md` § 编排者自身在本轮查出并订正的缺陷)。(FR-039 的适用细化)

## 钉子

**C-22** [制品类] 检查项集合的钉子 MUST 以**标签集**表达,MUST NOT 以计数表达。判据:钉子源码里出现的是一个集合字面量与一次集合相等断言,而不是一个整数。(FR-042)

**C-23** [制品类] 退出码表 MUST **单独**被钉,不与标签集共用一个断言。判据:两个测试函数分别存在。(FR-042)

**C-24** [制品类] 本特性触及的每个检查器 MUST 在落地时同时具备标签集钉子与退出码表钉子,MUST NOT 留下任何一个零守卫的检查器。(FR-046)

**C-25** [制品类] 既有 `validate-tasks.py` 的两处钉子(`EXPECTED_CHECKS` `:75-82` 由 `:314` 断言、`test_c5_exit_code_table` `:346`)均已存在,故对它的义务是**在新增检查项的同一提交内扩充这两个钉子**,不是从零补钉;扩充后标签集为既有 6 项 + 新增 4 项 = **10** 项。(FR-046、D-5)

**C-26** [制品类] `goal-utils.py` 的退出码表**当前无任何钉子**(实测 `grep -rn "goal_utils.EXIT" tests/` 无命中,退出码只以散落字面量断言),故 US4 MUST 为它新建一张表钉子,形态抄 `tests/contract/test_trigger_engine.py:48` 的 `EXIT_CODES = {…}` + `:292` 逐 action 循环 + `:395` 的**封闭** roster 断言。(FR-046、D-13)

**C-27** [制品类] `tests/contract/test_goal_definition.py:245-257` 的 action roster 是一个**硬编码 9 元组且非封闭断言**,故新增 `run-checks` 不会使它转红、但会让新 action 处于零守卫状态;US4 MUST 在同一提交内把该元组扩为 10 元。(FR-046、D-12)

**C-28** [制品类] 新 action 的 `--help` 行 MUST 以 `read:` 或 `write:` 起首(既有约定,由上述测试的 `line.split()[1].startswith(("read","write"))` 强制);`run-checks` 是只读动作,故取 `read:`。(FR-034、D-12)

## 可运行性与镜像安装

**C-29** [行为类] 每个检查器 MUST 至少对一份**真实存在**的仓内制品只读地跑通一次并留下真实输出,作为它可运行的证据;「能编译」不构成「能启动」的证据。(FR-043)

**C-30** [制品类] 检查器 MUST 随包安装到运行时镜像:`pyproject.toml:32-37` 的 `[tool.hatch.build.targets.wheel.force-include]` 把整个 `scripts` 树映射到 `specify_cli/scripts`,故新脚本自动随包;判据为该映射行仍在场且新脚本位于 `scripts/python/` 下。(FR-047)

**C-31** [制品类] 检查器 MUST 被镜像同步的一致性检查覆盖(与 `validate-tasks.py` 同待遇):`sync-mirrors.py:72-78` 的 `MIRROR_PAIRS` 含 `scripts → .specify/scripts`(`strict_extras=True`),一致性由 `tests/contract/test_scripts_distribution_parity.py::test_repo_has_no_orphan_or_drifted_scripts`(`:71-87`)在引擎级保证,无逐文件枚举。(FR-047、D-4)

**C-32** [行为类] 镜像核验判据 MUST **逐对**给出,而不是一律取相对形或一律取绝对形。改前实测(2026-10-02,逐对跑 `sync-mirrors.py --check --only <path>` 并取真实退出码):`scripts/python` → **EXIT=2**(既有 `.specify/scripts/python/trigger-utils.py` DIFF,先于本特性存在)故该对 MUST 取**相对形**「无**新增**漂移」;`shared/definitions`、`shared/guidelines`、`shared/constants`、`templates/tasks-template.md`、`templates/commands` 五对均 **EXIT=0 `ok`**,故取绝对形即可通过。`regen-command-copies.py --check` 改前为 **EXIT=0**(「OK: all per-tool command copies match the source templates.」),故逐工具副本亦取绝对形。**全树** `--check` 为 EXIT=2(既有 `skills/` 两处 DIFF + 上述 `trigger-utils.py`),故 MUST NOT 用全树绝对判据。测量时 MUST 用 `PIPESTATUS` 或不经管道取码——经 `| tail` 会把退出码换成 `tail` 的。(FR-047、D-17)

**C-33** [行为类] 新增检查器的 verdict 消息**词汇**(不只是 C-8 钉住的数字尾行形态)MUST 受 `.specify/shared/guidelines/user-facing-comprehension.md` 约束:消息 MUST 能被一个未参与该次运行的读者据以行动,故 MUST 点名**哪个文件的哪一行**、**违反了哪条规则**、以及**下一步该做什么**;MUST NOT 只用内部标签(如裸印 `green-path-divergence`)充作解释。判据归属:该纪律的界类封闭集已含 **⑪ 失败如实报告**,检查器的输出属该类,故本特性 MUST NOT 向其封闭集新增类别(与 052 对同一集合的处置一致)。取证形态为对每条新消息各给一个真实样本并逐条核其可行动性——属行为类,由真源文档载明义务 + 评审强制,MUST NOT 声称由守卫覆盖。(Principle XV、FR-003)
