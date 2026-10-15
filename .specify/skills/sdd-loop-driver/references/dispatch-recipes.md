# Dispatch Recipes — 五大执行机制命令形态（sdd-loop-driver）

> 本文件是宿主 agent 驱动外部子代理的**操作手册**：全部命令形态自包含可用，不依赖任何框架文档（对撰写底稿的引用仅为溯源注解）。所有路径、用户名、别名均为入口参数占位——机制零硬编码。

## Preflight — 前置检查（真正流程执行之前，U0 与 U1 之间）

> 五族前置检查是机制能否正确运行的先决条件；任一项无法自动核验或核验结果不确定时，**停在前置阶段、提示用户补充**该信息，MUST NOT 猜测续跑。检查结论（逐项 ok / fail / uncertain）写入该线状态脊的**前置检查段**，失败项附修复动作。

| # | 检查 | 命令形态 | 判定 |
|---|------|----------|------|
| ① | SSH 连通性（**本地拓扑跳过**） | `ssh -o ConnectTimeout=5 -o BatchMode=yes <alias> true` | 限时内返回 0 = ok；超时/拒绝 = fail（附修复：网络/凭证/别名） |
| ② | 非 root 运行用户存在性 | `ssh <alias> "id <run-user>"` | 输出含 `uid=` 且 `uid=<n>` 中 n ≠ 0 = ok；用户不存在或 uid=0 = fail（root 不能作为运行身份） |
| ③ | 子代理 CLI 可用性与版本 | `ssh <alias> "su - <run-user> -c '<cli> --version'"` | 版本串输出 = ok（记录版本号进状态脊）；命令不存在/不在执行身份 PATH = fail |
| ④ | 大语言模型配置 | 经宿主 CLI 配置面核验：模型（model）、context size、effort 三项当前生效值 | 三项齐备且可读 = ok（记录进状态脊）；配置面不可读或项缺失 = **uncertain → 提示用户补充**（形态因 CLI 而异，不猜测） |
| ⑤ | spec-kit 框架可用性（目标项目侧） | `ssh <alias> "cd <project-dir> && test -d .specify && test -f .specify/memory/constitution.md && cat .specify/source.json 2>/dev/null"` | `.specify/` 存在且宪法在位 = 初始化 ok；`source.json` 提供框架版本 provenance（缺失 = 版本未知，报告）；未安装/未初始化 = fail（对应边界：不自动初始化，停线上送） |

程序：五项逐条执行 → 结论（ok / fail / uncertain + 证据）写入状态脊前置检查段 → 全 ok 才进入 Recipe 0；存在 fail = 停线并按上送件四要素报告；存在 uncertain = 停线并列出**待用户补充的信息清单**，用户补充后重入前置检查。

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

提示词三段骨架（背景与权威文档 / 执行要求 / 完成尾标与回传契约）见 `stage-prompts.md`——本配方只管落盘。

## Recipe 2 — Runner 脚本与派生（Runner & Derivation）

```bash
# /home/<run-user>/run-<line>-<stage>.sh
cd <project-dir> && <cli> -w <project-dir> --permission-mode auto -p "$(cat /home/<run-user>/prompt-<line>-<stage>.md)"
```

下一阶段 runner 用 `sed` 替换上一阶段 runner 的提示词文件名派生——runner 形态跨阶段恒同，避免重复维护整套脚本。

## Recipe 3 — 脱离模式派发 + 定时间隔检查（Detached Dispatch & Interval Check，缺省形态）

**让子代理在后台自己跑，主代理按一定时间间隔检查结果**——派发连接断开不中断子代理：

```bash
# 1) 远端侧脱离派发：nohup 使子代理脱离 ssh 会话存活，日志落远端
ssh <alias> "nohup su - <run-user> -c 'bash /home/<run-user>/run-<line>-<stage>.sh' \
  > /home/<run-user>/log-<line>-<stage>.log 2>&1 &"
# 2) 主代理按定时间隔检查（间隔 = cadence 参数，缺省建议 60s，可入口覆盖）：
ssh <alias> "tail -20 /home/<run-user>/log-<line>-<stage>.log"
```

要点：

- **脱离（detached）优先于前台**：`nohup … &` 让远端进程独立于 ssh 连接存活；派发命令立即返回，主代理随后按间隔发起独立的检查连接。简化变体（本地 ssh 后台 `ssh … "su - …" > 本地日志 2>&1 &`）仅适用于短阶段且连接稳定时——连接断开会杀掉子代理，故**缺省用脱离形态**。
- **一线一连接（检查时）**：每条线的检查各自独立发起；多线并行互不串扰。
- **观察面纪律（底稿注解：External Dispatch Visibility Contract，`subagent-definitions.md`）**：禁止**缓冲至退出**式派发——`qodercli -p "<prompt>" > agent.log 2>&1 &` 这种「输出缓冲到进程退出才落盘」的形态让运行期零可见性，是明令禁止的反模式。本机制的观察面是**阶段粒度**（哨兵出现在输出末尾）：`-p` 缓冲意味着阶段结束前日志静默——间隔检查等的就是哨兵行；若需阶段内进度/卡死检测，把 runner 换成流式输出（`--output-format stream-json`）形态。
- 哨兵出现 `<STAGE>-DONE` → 进入独立校验（见 stage-prompts.md）→ 通过则派发下一阶段（回到 Recipe 1/2/3）。

## Recipe 4 — 阶段链与收尾（Stage Chain & Closure）

- 阶段链固定顺序：`requirements → clarify → plan → tasks → implement → review`；每阶段完成哨兵 = 大写阶段名 + `-DONE`（如 `PLAN-DONE`）。尾标是完成的必要条件，充分条件由独立校验补齐。
- **合并收尾（git 状态判定，不设哨兵）**：review 后合并回 main——判定条件为特性分支的提交已包含于集成分支、且工作树无该分支的未合并/冲突残留；两项齐备即该线合并完成。push 与远程分支操作缺省不执行（确认门控破坏性动作；仅入口显式授权时先推后合）。
- 全部线收束后向用户出**收尾汇总**：逐线终态阶段、合并结果、遗留异常与证据指针。

## Recipe 5 — 本地拓扑与变体

- **本地拓扑**：项目在本机时省略 ssh/su，直接以本地项目为工作目录执行 runner；需求上下文先写简报文件（`/tmp/<topic>-sdd-brief.md`），子代理提示词只指示「先完整阅读简报，再执行对应阶段命令」。
- **构建固化变体**：同一主机按角色分线（不同系统用户在各自目录固化不同层），仅经入口参数（执行身份、路径）区分，机制零新增分支。

## Boundary

- 远端不可达 / 凭证失效 / 子代理 CLI 不在执行身份路径：派发前预检拦截并给修复动作，不裸报错弃线。
- 目标项目无 `.specify/`：报告停线，不自动初始化。
- 断点无法判定：停线上送用户裁定，不猜起步阶段。
- 撰写底稿注解：本文件操作要点撰写时取材于 shared 层 `external-dispatch-recipes.md` 与 `unattended-loop-pattern.md` 底稿；运行时零依赖。
