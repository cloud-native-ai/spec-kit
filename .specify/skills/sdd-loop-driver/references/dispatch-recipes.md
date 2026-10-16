# Dispatch Recipes — 五大执行机制命令形态（sdd-loop-driver）

> 本文件是宿主 agent 驱动外部子代理的**操作手册**：全部命令形态自包含可用，不依赖任何框架文档（对撰写底稿的引用仅为溯源注解）。所有路径、用户名、别名均为入口参数占位——机制零硬编码。
>
> **委派化声明（2026-10-16 裁定）**：与配方真源 `.specify/shared/workflow/external-dispatch-recipes.md` 同型的机制段已坍缩为引用；本文件保留 **loop-driver 特有差异面**（心跳机制、脱离形态权威落点、阶段链与收尾编排）与对真源的引用——单一事实落点，重复即漂移。

## Preflight — 前置检查（引用 run-agent 公用承载；U0 与 U1 之间）

> 五族前置检查表与失败处置链已上收至 `skills/internal/run-agent/references/dispatch-preflight.md`（2026-10-16 上收，本表唯一权威落点在彼处）——检查先于 U1 派发；结论（逐项 ok / fail / uncertain）以**每项 ≤3 行摘要**写入该线状态脊的前置检查段。⑤ fail（`.specify/` 缺失/退化）handoff sdd-project-setup（缺失=install、退化=refresh）的软协同语义随表迁移；①②③ fail 停线上送、④ uncertain 列待补清单的处置链同见该文件。

## Recipe 0 — 断点探测（Breakpoint Probe）

派发前探测目标项目当前所处 SDD 阶段，未声明阶段时**必须探测、禁止猜测**。命令形态（三信号：分支名 / 近期提交 / specs 目录）见 `.specify/shared/workflow/external-dispatch-recipes.md` § Recipe 1——本配方坍缩为引用。

两条本技能纪律保留：三信号与终态权威文档路径一起判定续跑阶段，判定结果写入该线状态脊；必须覆盖收尾场景——review 已完成、只剩合并时直接进入收尾配方（Recipe 4）。

## Recipe 1 — 阶段提示词文件（Stage Prompt File）

每阶段把完整指令经 heredoc 写为远端文件（不内联进命令行）。落盘命令形态见 `.specify/shared/workflow/external-dispatch-recipes.md` § Recipe 2——本配方坍缩为引用。

两条本技能纪律保留：提示词三段骨架（背景与权威文档 / 执行要求 / 完成尾标与回传契约）见 `stage-prompts.md`——骨架内容是本技能的编排本体；反嵌套红线义务真源在 run-agent 派发治理（`skills/internal/run-agent/SKILL.md`），派发前自检涵盖本配方。

## Recipe 2 — Runner 脚本与派生（Runner & Derivation）——**心跳差异面**

基础 runner 形态（`cd` + `<cli> -w` + `-p "$(cat …)"` + sed 派生）见 `.specify/shared/workflow/external-dispatch-recipes.md` § Recipe 3。本技能差异面——**心跳文件机制**（无人值守长跑的存活判定依赖）：

```bash
# /home/<run-user>/run-<line>-<stage>.sh
# 心跳：runner 启动即打点，进程活着的确定信号（不依赖 CLI 流式输出）
(while true; do date +%FT%T >> /home/<run-user>/heartbeat-<line>-<stage>.log; sleep 30; done) &
HB=$!
cd <project-dir> && <cli> -w <project-dir> --permission-mode auto -p "$(cat /home/<run-user>/prompt-<line>-<stage>.md)"
rc=$?; kill $HB 2>/dev/null; exit $rc
```

下一阶段 runner 用 `sed` 替换上一阶段 runner 的提示词文件名派生——runner 形态跨阶段恒同，避免重复维护整套脚本。

## Recipe 3 — 脱离模式派发 + 定时间隔检查（Detached Dispatch & Interval Check，缺省形态）——**nohup 权威落点**

**让子代理在后台自己跑，主代理按一定时间间隔检查结果**——派发连接断开不中断子代理。本形态是 loop-driver 实测独有差异面（analyze H-04 裁定：权威落点在本文件，不迁配方真源）：

```bash
# 1) 远端侧脱离派发：nohup 使子代理脱离 ssh 会话存活；日志重定向在 su -c 内层，
#    归属 run-user（外层重定向会以本地身份落盘，run-user 不可 tail）
ssh <alias> "nohup su - <run-user> -c 'bash /home/<run-user>/run-<line>-<stage>.sh > /home/<run-user>/log-<line>-<stage>.log 2>&1' < /dev/null > /dev/null 2>&1 &"
# 2) 主代理按 cadence 主动检查（一次调用合并心跳+日志两路信号，输出 ≤4 行）：
ssh <alias> "tail -1 /home/<run-user>/heartbeat-<line>-<stage>.log; tail -3 /home/<run-user>/log-<line>-<stage>.log"
```

要点：

- **脱离（detached）优先于前台**：`nohup … &` 让远端进程独立于 ssh 连接存活；派发命令立即返回，主代理随后按间隔发起独立的检查连接。简化变体（本地 ssh 后台 `ssh … "su - …" > 本地日志 2>&1 &`）仅适用于短阶段且连接稳定时——连接断开会杀掉子代理，故**缺省用脱离形态**。
- **外层三重重定向必须**：`nohup` 任务本体之外再带 `< /dev/null > /dev/null 2>&1`——缺省时后台任务继承 ssh 通道的 stdio，本地 ssh 挂起直到超时（实测 2026-10-16：每次派发白烧一次 2 分钟本地超时，进程虽照常启动但驱动者节拍被打断）。
- **心跳即存活信号**：阶段日志受 `-p` 缓冲影响在退出前静默，心跳文件是「进程活着」的确定信号；**心跳停跳且进程消失** = 卡死判定信号（单看任一都不是）。
- **cadence 分级（入口可覆盖）**：requirements/clarify/tasks/checklist/analyze 建议 120–240s（checklist/analyze 为轻量分析型质量门）；plan/implement/review 建议 300–600s——长阶段高频轮询只烧驱动者预算不增信息。
- **多线批查**：一次 ssh 调用合并检查多条线（各自 tail 心跳+日志），**判定仍逐线独立做**；检查输出只保留心跳行与日志尾部 ≤4 行/线，哨兵未现且进程存活时无需更多输出。
- **观察面纪律（底稿注解：External Dispatch Visibility Contract，`subagent-definitions.md`）**：禁止**缓冲至退出**式派发——`qodercli -p "<prompt>" > agent.log 2>&1 &` 这种「输出缓冲到进程退出才落盘」的形态让运行期零可见性，是明令禁止的反模式。本机制的观察面是**阶段粒度**（哨兵出现在输出末尾）：`-p` 缓冲意味着阶段结束前日志静默——间隔检查等的就是哨兵行；若需阶段内进度/卡死检测，把 runner 换成流式输出（`--output-format stream-json`）形态。
- 哨兵出现 `<STAGE>-DONE` → 进入独立校验（见 stage-prompts.md）→ 通过则派发下一阶段（回到 Recipe 1/2/3）。

## Recipe 4 — 阶段链与收尾（Stage Chain & Closure）——编排本体

- 阶段链固定顺序：`requirements → clarify → plan → tasks → checklist → analyze → implement → review`（2026-10-17 修订：纳入 checklist/analyze 质量门——无人值守循环执行完整版流程，日常手动开发常省略的非必须命令一律必经）；每阶段完成哨兵 = 大写阶段名 + `-DONE`（如 `PLAN-DONE`、`CHECKLIST-DONE`、`ANALYZE-DONE`）。尾标是完成的必要条件，充分条件由独立校验补齐。
- **质量门编排（checklist / analyze 两门位于 tasks 与 implement 之间）**：
  - **checklist 门**：产物 = `REQUIREMENTS_DIR/checklists/` 新增清单文件；清单项的满足判定不在本门裁决——由 implement 阶段的 checklist 豁免门接管（子代理按 G5 默认纪律自行裁决，waiver 记录进 waivers.md）。
  - **analyze 门**：产物 = findings 报告正文（只读命令，不产新提交）；门判据 = 报告中 CRITICAL/HIGH 发现为零或已处置。
  - **回环规则（两门同构，一轮有界）**：门发现的问题回上游阶段修复（checklist 项失败 → 重派 plan 或 tasks；analyze CRITICAL/HIGH → 重派 requirements/plan/tasks 对应修复）后重过该门，同一门最多回环一轮；第二轮 checklist 仍未过 → 豁免放行并记录进状态脊；第二轮 analyze 仍有 CRITICAL/HIGH → 停线上送（跨产物矛盾带病进 implement 会放大，不可豁免）。
- **合并收尾（git 状态判定，不设哨兵）**：review 后合并回 main——判定条件为特性分支的提交已包含于集成分支、且工作树无该分支的未合并/冲突残留；两项齐备即该线合并完成。push 与远程分支操作缺省不执行（确认门控破坏性动作；仅入口显式授权时先推后合）。
- **脏树合并变体（实测配方）**：工作树存在与集成分支冲突的既有脏文件、`git checkout main` 被终止时，不动工作树——`git push . HEAD:main` 快进本地 main 引用，再 `git push origin HEAD:main` 推远端；工作树留在特性分支无害，重入只认状态脊。
- **分支清理（branch hygiene，合并后的收尾步）**：合并并推送后，删除本特性的特性分支——本地用 `git branch -d`（安全删除，未合并自动拒删），远端先 `git merge-base --is-ancestor origin/<branch> main` 验证祖先关系再 `git push origin --delete`；判定 NOT-MERGED 的分支保留并登记进收尾汇总，不强删。该线历史上的遗留分支同规则一并巡检（实测定级示例见 2026-10-15 xuanji-doc：6 条规格/验证分支 + 1 条已并入的 kb-v41-phase-t 时代分支，全部验证祖先后删除，终态仅存 main）。
- **P0 前置门**：同线上一特性 review 的 P0 发现未修复或未显式豁免前，禁止派发该线下一特性规格的 requirements（P0 语义 = fix before next spec；豁免记录进状态脊）。
- **工作树归档清扫（archive-or-ignore，合并的前置门）**：合并前驱动者必须把该线工作树残留逐文件（或逐聚类）归类处置，确保「代码全部归档合并到主干并推送上游」可判定：
  1. 本线特性产物 → 应已随阶段提交，漏网的补入对应阶段提交或单独补提交；
  2. 运行记录（feedback / session / knowledge / glossary / 登记表等 SDD 运行副产物）→ 归档提交（`chore(archive): …`）；
  3. 机器状态打点（索引器/构建器对内容库的批量标记，抽样 diff 确认为状态字段而非内容改动）→ 归档提交（`chore(index): …`，注明运行来源与时间）；
  4. 构建缓存/派生产物 → 追加 `.gitignore` 并提交忽略规则；
  5. 他线隔离项（并发隔离声明列出的路径）→ 保留不动，逐项登记进收尾汇总。
  判定：分类提交后 `git status --porcelain` 为空（或仅剩第 5 类），工作树归零才进入合并；实测定级示例见 2026-10-15 xuanji-doc 归档（5416 索引打点 + 11 运行记录 + 9 框架刷新 + 1 gitignore，四提交归零）。
- **逐线强制与时序（实测教训 2026-10-15 xuanji-robot 漏扫）**：多线并行时归档清扫**逐线各执行一遍**——驱动者不得因「一条线已扫」而推断全线干净；时序固定为「末阶段提交完成 → 归档清扫（含清扫产生的归档提交）→ 合并 → 推送 → 该线状态脊记录归零判定」；收尾汇总**每线必须携带工作树归档判定字段**（归零 / 残留 N 项+分类），缺该字段的线视为未收束——用清单字段强制可见，不依赖驱动者记忆。
- 全部线收束后向用户出**收尾汇总**：逐线终态阶段、合并结果、**工作树归档判定（归零 / 残留 N 项+分类）**、遗留异常与证据指针。

## Recipe 5 — 本地拓扑与变体

- **本地拓扑**：项目在本机时省略 ssh/su，直接以本地项目为工作目录执行 runner；需求上下文先写简报文件（`/tmp/<topic>-sdd-brief.md`），子代理提示词只指示「先完整阅读简报，再执行对应阶段命令」——命令形态见 `.specify/shared/workflow/external-dispatch-recipes.md` § Recipe 5（本配方坍缩为引用）。
- **构建固化变体**：同一主机按角色分线（不同系统用户在各自目录固化不同层），仅经入口参数（执行身份、路径）区分，机制零新增分支——形态见同文件 § Recipe 6。

## Boundary

- 远端不可达 / 凭证失效 / 子代理 CLI 不在执行身份路径：前置检查（run-agent dispatch-preflight.md）拦截并给修复动作，不裸报错弃线。
- 目标项目无 `.specify/`：报告停线，不自动初始化。
- 断点无法判定：停线上送用户裁定，不猜起步阶段。
- 撰写底稿注解：本文件操作要点撰写时取材于 shared 层 `external-dispatch-recipes.md` 与 `unattended-loop-pattern.md` 底稿；运行时零依赖。同型机制段已按 2026-10-16 委派化裁定坍缩为引用（Preflight→run-agent、R0/R1/R5→配方真源），保留面=心跳/脱离形态权威落点/阶段链收尾。
