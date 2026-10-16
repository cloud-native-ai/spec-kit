# Dispatch Recipes — 五大执行机制命令形态（sdd-loop-driver）

> 本文件是宿主 agent 驱动外部子代理的**操作手册**：全部命令形态自包含可用，不依赖任何框架文档（对撰写底稿的引用仅为溯源注解）。所有路径、用户名、别名均为入口参数占位——机制零硬编码。

## Preflight — 前置检查（本技能独立运行所必需；U0 与 U1 之间）

> 五族前置检查是机制能否正确运行的先决条件，**由本技能自持**（与 sdd-project-setup 各自独立、互不强依赖）。任一项无法自动核验或核验结果不确定时，停在前置阶段、提示用户补充或按失败分类处置。检查结论（逐项 ok / fail / uncertain）以**每项 ≤3 行摘要**写入该线状态脊的前置检查段。

| # | 检查 | 命令形态 | 判定 |
|---|------|----------|------|
| ① | SSH 连通性（**本地拓扑跳过**） | `ssh -o ConnectTimeout=5 -o BatchMode=yes <alias> true` | 限时内 0 = ok；超时/拒绝 = fail |
| ② | 非 root 运行用户存在性 | `ssh <alias> "id <run-user>"` | uid≠0 = ok；不存在或 uid=0 = fail |
| ③ | 子代理 CLI 可用性与版本 | `ssh <alias> "su - <run-user> -c '<cli> --version'"` | 版本串 = ok（记录进状态脊）；不在 PATH = fail |
| ④ | 大语言模型配置 | 经宿主 CLI 配置面核验 model/context/effort 三项 | 齐备可读 = ok；不可读 = **uncertain → 列待补清单**（形态因 CLI 而异，不猜测） |
| ⑤ | spec-kit 框架可用性（目标项目侧） | `ssh <alias> "cd <project-dir> && test -d .specify && test -f .specify/memory/constitution.md && cat .specify/source.json 2>/dev/null"` | 在位 = ok；缺失/退化 = **fail → handoff sdd-project-setup**（见下） |

**失败处置的软协同**：⑤ fail（`.specify/` 缺失或宪法不在位）时，**handoff 给 sdd-project-setup 技能**处置（缺失=install 模式、退化=refresh 模式）——本技能不执行框架初始化；处置完成回本循环重跑 preflight。①②③ fail 停线并按上送件四要素报告；④ uncertain 列出待用户补充的信息清单。与 sdd-project-setup 的完整边界见其 setup-recipes.md「软协同契约」。

## Recipe 0 — 断点探测（Breakpoint Probe）

派发前探测目标项目当前所处 SDD 阶段，未声明阶段时**必须探测、禁止猜测**：

```bash
ssh <alias> "cd <project-dir> && git branch --show-current; git log --oneline -3; ls .specify/specs/ 2>/dev/null"
```

三信号（分支名 / 近期提交 / specs 目录）与终态权威文档路径一起判定续跑阶段。判定结果写入该线状态脊。必须覆盖收尾场景：review 已完成、只剩合并——此时直接进入收尾配方。

## Recipe 1 — 阶段提示词文件（Stage Prompt File）

每阶段把完整指令经 heredoc 写为远端文件（不内联进命令行）：

```bash
ssh <alias> "cat > /home/<run-user>/prompt-<line>-<stage>.md" <<'EOF'
<prompt body>
EOF
```

提示词三段骨架（背景与权威文档 / 执行要求 / 完成尾标与回传契约）见 `stage-prompts.md`——本配方只管落盘。**红线：提示词体不得引用本技能（sdd-loop-driver）或任何驱动/循环机制**——子代理只执行阶段命令，不加载技能、不感知循环（反嵌套拓扑见 SKILL.md「Driver Topology」节）。

## Recipe 2 — Runner 脚本与派生（Runner & Derivation）

```bash
# /home/<run-user>/run-<line>-<stage>.sh
# 心跳：runner 启动即打点，进程活着的确定信号（不依赖 CLI 流式输出）
(while true; do date +%FT%T >> /home/<run-user>/heartbeat-<line>-<stage>.log; sleep 30; done) &
HB=$!
cd <project-dir> && <cli> -w <project-dir> --permission-mode auto -p "$(cat /home/<run-user>/prompt-<line>-<stage>.md)"
rc=$?; kill $HB 2>/dev/null; exit $rc
```

下一阶段 runner 用 `sed` 替换上一阶段 runner 的提示词文件名派生——runner 形态跨阶段恒同，避免重复维护整套脚本。

## Recipe 3 — 脱离模式派发 + 定时间隔检查（Detached Dispatch & Interval Check，缺省形态）

**让子代理在后台自己跑，主代理按一定时间间隔检查结果**——派发连接断开不中断子代理：

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
- **cadence 分级（入口可覆盖）**：requirements/clarify/tasks 建议 120–240s；plan/implement/review 建议 300–600s——长阶段高频轮询只烧驱动者预算不增信息。
- **多线批查**：一次 ssh 调用合并检查多条线（各自 tail 心跳+日志），**判定仍逐线独立做**；检查输出只保留心跳行与日志尾部 ≤4 行/线，哨兵未现且进程存活时无需更多输出。
- **观察面纪律（底稿注解：External Dispatch Visibility Contract，`subagent-definitions.md`）**：禁止**缓冲至退出**式派发——`qodercli -p "<prompt>" > agent.log 2>&1 &` 这种「输出缓冲到进程退出才落盘」的形态让运行期零可见性，是明令禁止的反模式。本机制的观察面是**阶段粒度**（哨兵出现在输出末尾）：`-p` 缓冲意味着阶段结束前日志静默——间隔检查等的就是哨兵行；若需阶段内进度/卡死检测，把 runner 换成流式输出（`--output-format stream-json`）形态。
- 哨兵出现 `<STAGE>-DONE` → 进入独立校验（见 stage-prompts.md）→ 通过则派发下一阶段（回到 Recipe 1/2/3）。

## Recipe 4 — 阶段链与收尾（Stage Chain & Closure）

- 阶段链固定顺序：`requirements → clarify → plan → tasks → implement → review`；每阶段完成哨兵 = 大写阶段名 + `-DONE`（如 `PLAN-DONE`）。尾标是完成的必要条件，充分条件由独立校验补齐。
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

- **本地拓扑**：项目在本机时省略 ssh/su，直接以本地项目为工作目录执行 runner；需求上下文先写简报文件（`/tmp/<topic>-sdd-brief.md`），子代理提示词只指示「先完整阅读简报，再执行对应阶段命令」。
- **构建固化变体**：同一主机按角色分线（不同系统用户在各自目录固化不同层），仅经入口参数（执行身份、路径）区分，机制零新增分支。

## Boundary

- 远端不可达 / 凭证失效 / 子代理 CLI 不在执行身份路径：派发前预检拦截并给修复动作，不裸报错弃线。
- 目标项目无 `.specify/`：报告停线，不自动初始化。
- 断点无法判定：停线上送用户裁定，不猜起步阶段。
- 撰写底稿注解：本文件操作要点撰写时取材于 shared 层 `external-dispatch-recipes.md` 与 `unattended-loop-pattern.md` 底稿；运行时零依赖。
