# Contract: `run-checks` 的调用契约(US4)

**Requirement**: `053-machine-decidable-artifacts` → Feature 053  
**Covers**: FR-029…FR-034  
**Subject**: `scripts/python/goal-utils.py`(既有二进制,新增一个 action)  
**Clause form**: `**C-N**` 行首裸粗体。  
**Class labeling**: 同 `contracts/checker-form.md`([制品类] / [行为类])。

---

## action 的存在与只读性

**C-1** [制品类] `goal-utils.py` MUST 增一个名为 STR-005 `run-checks` 的 action。判据:`goal-utils.py --help` 的 choices 行由实测的 9 项 `{create,validate,check-statement,list,status,objective,criteria,migrate,targets}` 变为 **10** 项且含 `run-checks`;该名字在改前**未被占用**(`grep -c "sub.add_parser"` → 9)。(FR-029)

**C-2** [制品类] 该 action MUST 一次调用输出团队 run 前置**五项**检查的 verdict;五项的 `name` 为 goal-binding / dangling / target-terminal / cross-goal / goal-terminal。判据:`--json` 输出的 `checks` 数组长度为 **5**,五项 `name` 集合相等。(FR-029、FR-031)

**C-3** [制品类] 该 action MUST **零写入**:任何一次调用都 MUST NOT 修改 `.specify/goal/` 或 `.specify/teams/` 下的任何文件。判据:调用前后两个目录的**字节校验和**相等(SC-007 Source 的取证形态);既有只读动作的写入点扫描已证读路径不达任何写入函数(8 个写入点 `:465`/`:466`/`:487`/`:506`/`:524`/`:569`/`:599`/`:756` 全在写动作上)。(FR-034)

**C-4** [制品类] 该 action 的 `--help` 行 MUST 以 `read:` 起首。判据:`tests/contract/test_goal_definition.py:245-257` 的 `line.split()[1].startswith(("read","write"))` 对 `run-checks` 成立。(FR-034、D-12)

## 复用既有解析,不重写第二套文法

**C-5** [制品类] 该 action MUST 复用既有的内部解析函数而**不重写第二套文法**。判据:五项检查的 verdict 全部由既有代码路径产出——① goal-binding → `resolve_team_goal_identity`(`:607-620`)判 `goal_slug is None`(`:634-637`,及 `:654-657` 绑定 slug 无对应文件);② dangling → `:663-667`;③ target-terminal → `:668-674`;④ cross-goal → `_QUALIFIED_TARGET`(`:623`)前缀比较,`:639-645`;⑤ goal-terminal → `data["status"] in TERMINAL_STATES`(`:55`),`:659-662`;文法失败 → `input-error`(`:646-651`)。全部位于 `preview_target_check`(`:626-676`)内。(FR-030、D-11)

**C-6** [制品类] 无 `--target` 时 MUST 先经 `resolve_effective_target`(`:679-707`,返回 `{effective, source, declared_focus}`)解析有效 target 再执行五项检查,并把解析结果(有效值、来源、声明的 focus)写进输出的 `resolution` 字段。判据:`--json` 输出含 `resolution` 且其三个子键在场。(FR-030、FR-031)

**C-7** [行为类] `preview_target_check(repo_root, team_slug, reference)` 的 `reference` 是**必需位置参数**,故第①项检查在无 `--target` 时**不可达**;实现 MUST 新增一个薄封装,在无 target 时:②③④ 记 STR-004 `not-evaluated`(无判定主体),①⑤ **仍被评估**(只依赖团队与 goal 的绑定关系)。MUST NOT 为了少写封装而让①也记 `not-evaluated`。(FR-030、FR-032、D-11)

**C-8** [制品类] `preview_target_check` 与 `resolve_effective_target` 二者**当前均无 CLI 入口**(实测 `grep -rn "preview_target_check\|resolve_effective_target" --include=*.py .` 只命中定义处 `:626`/`:679`、一处 docstring `:684` 与两个测试文件),故本 action 是它们的首个 CLI 暴露面;既有独立记录见 `.specify/memory/feedback/introspection/introspection-20260923T120035Z.md:162`。(FR-030)

## 输出字段

**C-9** [制品类] 机读输出的每条 check MUST 含 `id`(1..5)、`name`(C-2 的五个名字之一)、`verdict`、`message`;顶层 MUST 含 `team_slug`、`goal_slug`、`identity_kind`、`resolution`、`checks`、`verdict`、`blocked`。判据:契约测试对键集做集合相等断言。(FR-031)

**C-10** [制品类] check 的 `name` 与其 `verdict` 是**两个字段、两种角色**——`name` 说明「跑的是哪一项检查」,`verdict` 说明「该项得出什么结论」——MUST NOT 互相替代。**实测(订正)**:二者**并非**互斥集合,五项 `name` 里有 **4** 个同时也是 `goal-utils.py` 发出的 verdict 字面量(`dangling` `:665`、`target-terminal` `:669`、`cross-goal` `:643`、`goal-terminal` `:660`),只有 `goal-binding` 是纯 name(其 verdict 为 `no-goal-definition`)。故判据 MUST NOT 写成「两个集合交集为空」——那在当前源码下**不可满足**,照它写的测试一落地即红。可判定的判据取两条:(a) 至少存在一项检查,其 `name` **不属于** verdict 词表(实测即 `goal-binding`),证明两个字段不可互换;(b) 每项检查的 `name` → **可能 verdict 集**的映射被逐项钉住(依 D-11 的五个产出点),使「name 恰是该检查的某个 verdict」这一巧合不被误当作可依赖的不变量。(FR-031、FR-032、V-9)

**C-11** [制品类] `--json` MUST 已由**共享父解析器**提供(`:794`),故置于 action 前后皆可;每个 action 以 `_emit(result, args.json)`(`:1000`)收尾,`_emit`(`:1004-1024`)在 `--json` 下 `json.dumps(..., ensure_ascii=False, indent=2)`。新 action MUST 沿用同一路径,MUST NOT 自行 `print(json.dumps(...))`。(FR-031)

## verdict 词表

**C-12** [制品类] 单项检查的 verdict MUST 沿用既有词表 STR-006 的 7 个字面量 `ok` / `no-goal-definition` / `dangling` / `target-terminal` / `cross-goal` / `goal-terminal` / `input-error`(7 个已逐个实测命中 `goal-utils.py`)。判据:五项 verdict 的取值集 ⊆ 该 7 项 ∪ {`not-evaluated`}。(FR-032)

**C-13** [制品类] 因前置条件不成立而被短路的检查 MUST 记 STR-004 `not-evaluated`,MUST NOT 记 `ok`——一个未被评估的检查报绿正是本特性要消灭的形态。判据:构造一个使某项前置条件不成立的团队,该条 verdict 为 `not-evaluated` 且其余四条仍被评估(SC-008)。(FR-032、SC-008)

**C-14** [制品类] STR-004 `not-evaluated` 是**新造字面量**(实测在 `goal-utils.py` 零命中),故该二进制对 `run-checks` 而言的有效词表是 STR-006 ∪ {STR-004}。判据:新字面量以模块级常量或等价单点定义出现,MUST NOT 在多处散写字面量。(FR-032、clarify 轮订正)

**C-15** [制品类] 该二进制**另发**第 8 个字面量 `rejected`(`:935` `check-statement`、`:968` `targets --check`,均配 `EXIT_INPUT_ERROR`),它与五项检查无关,MUST NOT 因本特性被删改。判据:改动前后对 `rejected` 的命中数不变。(A-6、D-11)

**C-16** [行为类] 五项里有一项**自身抛异常**时,MUST 把该条记为 `not-evaluated` 并**继续评估其余四项**,MUST NOT 让一项异常吞掉整份 verdict。判据:注入一个使某项抛异常的团队定义,输出的 `checks` 数组长度仍为 **5** 且其余四项 verdict 非 `not-evaluated`。(边界情形)

## 退出码

**C-17** [制品类] 退出码 MUST 按 STR-007 `0=ok / 2=input-error / 3=not-found / 4=invalid / 5=blocked` 分档,即**沿用 `goal-utils.py:44-47` 既有 `EXIT_OK=0 / EXIT_INPUT_ERROR=2 / EXIT_NOT_FOUND=3 / EXIT_INVALID=4` 四码的原义**,只为 `blocked` 取下一个空闲码 **5**。判据:`grep -rn "EXIT_[A-Z_]* = 5" scripts/python/` 改前无命中(实测空闲);改后该二进制新增 `EXIT_BLOCKED = 5` 且既有四常量的值**逐字不变**。(FR-033、clarify 裁定 2、D-13)

**C-18** [制品类] 「检查判为阻塞」与「输入不合法」与「定义不可解析」三档 MUST 互相可区分。判据:三个逆样本各自得到 5 / 2 / 4。(FR-033)

**C-19** [制品类] MUST NOT 让同一个码在同一脚本里按 action 而有两种含义。判据:新增常量后,该二进制的退出码表仍是一个**全 action 共享**的单射(码 → 含义),不存在按 action 分叉的映射。(FR-033)

**C-20** [行为类] 既有调用方 `templates/commands/team.md:96,98` 只按 0 / 2 分支(`MUST 已通过(exit 0)`、`MUST NOT 以 exit-2 状态进入批准呈现`、`exit 2 的拒绝被原样上报`),故 C-17 的取值 MUST NOT 改动 0 与 2 的语义;落地后 MUST 复核该两处分支仍成立。(FR-033)

**C-21** [行为类] 该二进制**没有** `EXIT_USAGE = 1`(同胞 `derive-utils.py:46`、`trigger-utils.py:43` 有),故 argparse 的用法失败(`parser.error` `:992`)当前落 exit **2**,与动作体内的 `EXIT_INPUT_ERROR` **不可区分**。这是**既有**冲突,本特性 MUST NOT 顺手改它(超出声明范围),但 MUST 在实现处注明 `run-checks` 不依赖该区分。(D-13)

## 钉子

**C-22** [制品类] `goal-utils.py` 的退出码表**当前无任何钉子**(实测 `grep -rn "goal_utils.EXIT" tests/` 无命中;退出码只以散落字面量断言于 `test_goal_targets_check.py:136,145,157,163,169,177,186` 与 `test_goal_migration_path.py:114`),故 US4 MUST 新建一张表钉子,形态抄 `tests/contract/test_trigger_engine.py:48` 的 `EXIT_CODES = {…}` + `:292` 逐 action 循环 + `:395` 的**封闭** roster 断言。(FR-046、D-13)

**C-23** [制品类] `tests/contract/test_goal_definition.py:245-257` 的 action roster 是一个**硬编码 9 元组且非封闭断言**,故新增 `run-checks` **不会**使它转红、但会让新 action 处于零守卫状态;US4 MUST 在同一提交内把该元组扩为 **10** 元。(FR-046、D-12)

**C-24** [制品类] `goal-utils.py:16-30` 的读/写动作 roster 与 `:32` 的退出码表(`0 ok | 2 input error | 3 not found | 4 validation failed`)MUST 在同一提交内被扩充以含 `run-checks` 与码 5;二者都是 docstring 内的**制品**,故属制品类断言。(FR-046、D-12)

**C-25** [行为类] 该 docstring 的 Program-First 归属是**内联括注**形态(`:6-7` "Fixed rules belong in a program, not in a model (Constitution Principle XII / token-efficiency Program-First)"),而 FR-002 经 clarify 裁定只辖**新增**检查器,故 MUST NOT 因本特性把它改写成 `validate-tasks.py:4-6` 的点名 owner 形态。(D-12)

## 文档接线

**C-26** [行为类] `templates/commands/team.md:114-119` 当前把五项检查描述为一个有序 1→5 序列并声明「the engine parse of `scripts/python/goal-utils.py`(`parse_goal` / `preview_target_check`)is the single source of truth for every judgment below」,但**全段无任何 CLI 调用行**——代理必须自行拼装调用(该缺口已记录于 `.specify/memory/feedback/backlog.md:36`)。US4 落地后该处 MUST 增一行 `run-checks` 的调用形式,MUST NOT 保留「靠代理自行拼装」的形态。(FR-029)

**C-27** [制品类] 描述同五项检查的其余散文面 MUST 与新增的调用形式一致,不得留下第二套判据:`skills/create-team/references/execution-guide.md:27,30`、`skills/create-team/references/goal.md:45`、`docs/reference/commands/team.md:68,70`,以及 `team.md` 的 4 个逐工具副本(`.claude/commands/speckit.team.md:105`、`.github/prompts/speckit.team.prompt.md:105`、`.opencode/command/speckit.team.md:105`、`.qoder/commands/speckit.team.md:108`)。判据:逐工具副本经 `regen-command-copies.py` 再生后与源一致。(FR-029、D-17)

**C-28** [行为类] SC-007 的取证实验 MUST 在临时仓库副本里做,真实 goal 与团队定义 MUST NOT 被改动;若只能在真实树上验证,则 MUST 只跑只读路径并记录 C-3 的校验和不变作为证据。实测约束:`.specify/goal/` 下**只有 1 个** goal(`draw-two-layer-structure`),`.specify/teams/` 下 6 个团队目录,只有前者与一个 goal 定义绑定——故「对一个 goal 已终态的真实团队跑」这一支可能**无真实样本可用**,此时 MUST 记为不可得并说明, MUST NOT 编造。(SC-007、SC-007 Source、D-14)
