---
id: "20260804T121655Z-speckit-implement"
unit_id: "/speckit.implement"
unit_type: "command"
run_id: "036-team-summary-implement-20260804T200000Z"
scope: "local"
feature: "036-team-summary"
partial: false
created: "2026-08-04T12:16:55Z"
summary: "执行 036-team-summary 的 Phase 1(Setup)与 Phase 2(Foundational),15/120 任务闭环、105 项待办;两相内零开放任务。达成命令声明目的:按拓扑序、测试先行、逐任务证据闭环推进,并以基线名单证明零回归。"
---

## Review
执行 036-team-summary 的 Phase 1(Setup)与 Phase 2(Foundational),15/120 任务闭环、105 项待办;两相内零开放任务。达成命令声明目的:按拓扑序、测试先行、逐任务证据闭环推进,并以基线名单证明零回归。

预检阶段发现一个**框架级 bug**并按命令要求"exit 3 不得静默继续"处理:命令文档规定的机械写入门禁调用 `python3 .specify/scripts/python/gate-check.py` **永远失败**(exit 3),因为该脚本用 `Path(__file__).parents[2]` 推导 REPO_ROOT——对镜像副本会解析成 `.specify/`,于是去找 `.specify/.specify/gate.yaml`。canonical 副本 `scripts/python/gate-check.py` 解析正确,改用它后 8 条计划写入路径全部返回 allow(exit 0)。已记入 verification.md notes。

其余预检按命令逐项落实:清单 16/16 自动通过;24 个目标目录写权限全部实探可写;用 `git check-ignore` 双向验证忽略规则(goal 交付目录/items.jsonl/夹具/verification.md 全部被 ADMIT,`teams/.work/` 与 `agents/execution/logs/` 正确被忽略)。基线用 canonical runner 以 `--names-out` 采名单而非计数:39 failed / 1108 passed,名单落 baseline-failed.txt。在向 tests/ 与 skills/create-team/ 添文件前先按命令要求 grep 了脆弱计数断言,确认无穷举文件清单类断言。

TDD 严格执行且红-绿可见:三个契约测试文件先写,首轮 6 项结构性断言红(文档尚不存在),补齐 summary-mapping.md 后转绿;最终 69/69 通过。其中两条是高价值的行为断言而非结构断言——直接调用上游 `project-db.py` 证明 ID 文法由 DDL 强制(越界 exit 3),以及证明两团队各自的 `TI-0001` 会撞号、加团队前缀后可装载(把 research E-7 的一次性实测固化成了回归测试)。

回归以名单差集判定:`comm -13` 输出为空,39→39 名单完全一致,passed 1108→1177(+69,恰为新增测试数),零新增失败。镜像:`sync-mirrors --check` exit 0,三份 canonical 与镜像 byte-identical,5 份 per-tool speckit.team 副本均含 goal 目录改动。

两处自身失误已修:一是写 `summary-mapping.md` 时把可采纳执行层路径写成 `{configs,scripts}` 花括号形式,契约测试按 WS-7 逐条查找而红——修文档而非改断言(显式路径更可 grep);二是 `test_goal_slug_is_distinguished_from_team_slug` 用 ±900 字符窗口做邻近性启发式,而 frontmatter schema 与解释性 bullet 本就相隔甚远,导致假红——改为逐行断言,这是断言机制的缺陷而非文档缺陷。

## Optimization Points
- 命令第 6 步明写「run `python3 .specify/scripts/python/gate-check.py <planned-write-paths>`」,但这条**文档化的调用方式必然失败**:`gate-check.py` 用 `Path(__file__).resolve().parents[2]` 推导 REPO_ROOT,对 canonical 副本 `scripts/python/gate-check.py` 正确(→ 仓库根),对命令指定的镜像副本 `.specify/scripts/python/gate-check.py` 却解析为 `.specify/`,于是寻找不存在的 `.specify/.specify/gate.yaml` 并以 exit 3 退出。任何遵循该命令的 agent 都会在预检第一步撞上"gate unreadable",然后要么误判"本项目无门禁"、要么自行绕过——两者都破坏该门禁的意义。修法二选一:(a) 命令改为调用 canonical 路径 `scripts/python/gate-check.py`;(b) 脚本改为向上搜寻含 `.specify/` 的最近祖先目录而非固定 `parents[2]`,使两份副本都可用。建议同时做,并补一条契约测试断言"两份副本都能读到 gate.yaml"。
- 同类隐患值得普查:凡 `scripts/python/*.py` 中用固定 `parents[N]` 推导仓库根的脚本,在 `.specify/` 镜像下都会偏移一层。命令要求"prefer the canonical runner",但没说清"canonical 也指脚本路径本身"。建议在命令中把这条上升为一般规则:**调用被镜像的脚本时一律用 canonical 路径**(`scripts/`、`skills/`),`.specify/` 副本只作为被分发的运行时资产、不作为调用入口。
- 第 4 步的 ignore 校验只要求"确认忽略规则 ADMIT 本次产出路径"(单向)。本次我顺手做了反向校验(该被忽略的确实被忽略),并因此发现自己第一版探针路径写错了形状——用了 per-team 的 `.specify/teams/<slug>/.work/`,而真实约定是 `.specify/teams/.work/<slug>/`,若只做单向校验就会把"探针路径写错"误报成"忽略规则有漏洞"。建议该步明确要求双向:期望产出必须 ADMIT,期望瞬时物必须 IGNORE,且探针路径必须取自技能文档中的真实约定而非凭记忆构造。
- 第 7 步的证据闭环要求很到位,但没有区分"断言失败 = 被测物有问题"与"断言失败 = 断言本身写错了"。本次两次红都属后者(文档用了等价的花括号写法、测试用了脆弱的字符窗口启发式)。若机械照"红了就改被测物"执行,第二次会把正确的文档结构改坏来迁就一个坏断言。建议补一句:测试转红时 MUST 先判定失败归属(被测物 vs 断言),并在进度报告中说明改了哪一侧及理由。
- 第 3 步允许"同会话内产出的工件可从对话上下文消费(经存在性检查)",这条实际省了大量重读。但它与第 5 步"解析 tasks.md"存在张力:tasks.md 在本次运行中被我自己反复改写(勾选状态),从上下文消费就会读到过期的勾选态。本次每次勾选后都用 python 重读并打印 closed/open 计数来规避。建议该条补一句例外:**状态会被本次运行修改的文件(tasks.md)MUST 每次从磁盘重读**,不得从上下文消费。
- token-efficiency: 预检的四类检查(写权限、ignore 双向、gate、基线)各用一条批量命令完成;基线与回归都用 `--names-out` + `comm` 做名单差集而非逐行读输出;勾选状态用 python 正则批改并回打计数,未重读 tasks.md 全文;三份契约测试均未重读被测文档全文,而是让测试自己去读。可改进点:`run-tests.sh` 全量跑一次约 14s、本次跑了 4 次(基线 + 契约批 3 次),其中两次契约批可合并——应在改完文档与测试后一次性跑,而不是每改一处就跑一次。
