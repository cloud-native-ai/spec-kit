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

## Recipe 2 — Runner 脚本与派生（Runner & Derivation）——**正证据四件套差异面**

基础 runner 形态（`cd` + `<cli> -w` + `-p "$(cat …)"` + sed 派生）见 `.specify/shared/workflow/external-dispatch-recipes.md` § Recipe 3。本技能差异面——**pid / status / log / heartbeat 正证据四件套**（无人值守长跑的完成判定与存活判定都依赖它们；模型见 `watch-model.md` §2）：

```bash
# /home/<run-user>/run-<line>-<stage>.sh
#!/usr/bin/env bash
set -u
line=<line>; run=<run>; stage=<stage>; sentinel="<STAGE>-DONE"
dir=/home/<run-user>
pidf="$dir/pid-$line-$stage"; status="$dir/status-$line-$stage"
log="$dir/log-$line-$stage.log"; hb="$dir/heartbeat-$line-$stage.log"
meta="$dir/log-$line-$stage.log.meta.jsonl"; prompt_meta="$dir/prompt-$line-$stage.md.meta.json"
runner_pid=$$
write_atomic() { local tmp="$1.tmp.$$"; printf '%s\n' "$2" > "$tmp" && mv "$tmp" "$1"; }
start_ticks=$(awk '{print $22}' "/proc/$$/stat" 2>/dev/null || true)
write_atomic "$pidf" "pid=$runner_pid start=$start_ticks at=$(date +%s) line=$line run=$run stage=$stage event=pid"
printf '{"line_id":"%s","run_id":"%s","stage":"%s","event":"log-start","at":%s}\n' \
  "$line" "$run" "$stage" "$(date +%s)" >> "$meta"

# 心跳随 runner 死亡而退出，避免孤儿心跳伪造存活
( while kill -0 "$runner_pid" 2>/dev/null; do
    write_atomic "$hb" "at=$(date +%s) line=$line run=$run stage=$stage event=heartbeat"
    sleep 30
  done ) &
hb_pid=$!
disown "$hb_pid" 2>/dev/null || true

finish() {
  rc=$1
  trap - EXIT
  kill "$hb_pid" 2>/dev/null || true
  last=$(tail -n 50 "$log" 2>/dev/null | awk 'NF{line=$0} END{print line}' | tr -d '\r' | sed 's/[[:space:]]*$//')
  sent=0; [ "$last" = "$sentinel" ] && sent=1
  write_atomic "$status" "exit=$rc at=$(date +%s) sentinel=$sent line=$line run=$run stage=$stage event=status"
  printf '{"line_id":"%s","run_id":"%s","stage":"%s","event":"log-terminal","at":%s,"sentinel_seen":%s,"exit":%s}\n' \
    "$line" "$run" "$stage" "$(date +%s)" "$sent" "$rc" >> "$meta"
  exit "$rc"
}
trap 'finish $?' EXIT

cd "<project-dir>" || exit 127
"<cli>" -w "<project-dir>" --permission-mode auto -p "$(cat "$dir/prompt-$line-$stage.md")" > "$log" 2>&1
```

要点：

- **退出记录是完成的主事件**：`status-…` 原子写入 `exit=<rc> at=<epoch> sentinel=<0|1>`，并在行尾追加归属信封 `line= run= stage= event=status`；驱动者优先读退出记录，而不是猜测进程状态。
- **PID 文件是存活的唯一权威**：`pid + start ticks` 供 `kill -0`、僵尸检测与 PID 复用校验；PID 行同样携带信封。禁止用 `pgrep -c` 计数推断存活或完成（零匹配陷阱见 `watch-model.md` §7）。
- **归属信封只走旁路**：日志正文零改动；`log-<line>-<stage>.log.meta.jsonl` 在启动与终止各追加一条 JSON（终止条含 `sentinel_seen`/`exit`），`prompt-<line>-<stage>.md.meta.json` 是派发前写入的静态信封。哨兵仍是日志最后一个非空行。
- **心跳只证明 runner 外壳活着**：心跳循环以 `kill -0 "$runner_pid"` 为条件，外壳死亡即停跳；每跳行尾带 `line= run= stage= event=heartbeat`。子代理是否卡死仍由阶段 deadline 判定。
- **日志最后非空行**是哨兵判据；`-p` 缓冲模式下日志在退出前静默属预期，由退出记录提供提前事件。
- 下一阶段 runner 用 `sed` 替换上一阶段 runner 的提示词/哨兵字面量派生——runner 形态跨阶段恒同，避免重复维护整套脚本。

## Recipe 3 — 脱离模式派发 + 统一监听（Detached Dispatch & Unified Watch，缺省形态）——**nohup 权威落点**

**让子代理在后台自己跑，驱动者用长轮询窗口监听**——派发连接断开不中断子代理，等待期间不消耗模型回合。本形态是 loop-driver 实测独有差异面（analyze H-04 裁定：权威落点在本文件，不迁配方真源）；监听规则本体见 `watch-model.md`，本节只给命令形态：

```bash
# 0) 每主机一次：上传 watcher（与 runner 同一执行身份）
ssh <alias> "cat > /home/<run-user>/watch-target.sh" < <skill-dir>/scripts/watch-target.sh
ssh <alias> "chmod +x /home/<run-user>/watch-target.sh"

# 1) 远端侧脱离派发：nohup 使 runner 脱离 ssh 会话存活；
#    runner 的 stdout/stderr 在 su -c 内层落 runner-log（归属 run-user）；
#    CLI 输出由 runner 内层再重定向到 log
ssh <alias> "nohup su - <run-user> -c 'bash /home/<run-user>/run-<line>-<stage>.sh > /home/<run-user>/runner-log-<line>-<stage>.log 2>&1' < /dev/null > /dev/null 2>&1 &"

# 2) 每个监听窗口：一次 ssh（与 runner 同一执行身份），命中终止判定或窗口到期即返回
#    （工具超时设为 window+30s）
ssh <alias> "su - <run-user> -c 'bash /home/<run-user>/watch-target.sh \
  --label <line> --pid-file /home/<run-user>/pid-<line>-<stage> \
  --status-file /home/<run-user>/status-<line>-<stage> \
  --log /home/<run-user>/log-<line>-<stage>.log \
  --sentinel <STAGE>-DONE --heartbeat /home/<run-user>/heartbeat-<line>-<stage>.log \
  --deadline-epoch <stage_deadline_epoch> --window 200 --interval 3'"
```

要点：

- **脱离（detached）优先于前台**：`nohup … &` 让远端进程独立于 ssh 连接存活；派发命令立即返回，驱动者随后发起独立的监听窗口。简化变体（本地 ssh 后台 `ssh … "su - …" > 本地日志 2>&1 &`）仅适用于短阶段且连接稳定时——连接断开会杀掉子代理，故**缺省用脱离形态**。
- **外层三重重定向必须**：`nohup` 任务本体之外再带 `< /dev/null` 并把 ssh 通道的 stdout/stderr 重定向（`> /dev/null 2>&1`）——缺省时后台任务继承 ssh 通道的 stdio，本地 ssh 挂起直到超时（实测 2026-10-16：每次派发白烧一次 2 分钟本地超时，进程虽照常启动但驱动者节拍被打断）。runner 自身的 stdout/stderr 在 `su -c` 内层落 `runner-log`，保证归属 run-user 可读。
- **监听机制阶梯（`watch-model.md` §4）**：长轮询窗口缺省 → 宿主原生通知仅作补充（且不得结束驱动者会话）→ 间隔轮询回退；**禁止**独立 `sleep N` 回合空等。
- **窗口到期 ≠ 阶段超时**：watcher 返回 `RUNNING`（退出码 10）时立即发起下一窗口，不做 agent 侧等待；只有 `TIMEOUT`（阶段 deadline）进入 U5。这条把「监视器零匹配/窗口到期误判超时」与真正的阶段超时分开（2026-10 实测缺陷：`pgrep -c` 零匹配先输出 0 再被 `|| echo 0` 追加第二个 0，导致 clarify 已完成仍被误判超时）。
- **正证据优先**：每轮一次读取退出记录 → PID 存活 → 日志尾行 → 心跳 mtime；进程消失、日志静默、`pgrep` 零匹配都**不是**完成。心跳只证明 runner 外壳活着，与 PID 一起看。
- **多线批查**：一个窗口一次 ssh 检查多条线（`--manifest` 模式），任一线终止即返回全部线快照，**判定仍逐线独立做**；输出只保留判定行与必要证据，哨兵未现且进程存活时无需更多输出。
- **观察面纪律（底稿注解：External Dispatch Visibility Contract，`subagent-definitions.md`）**：禁止**缓冲至退出**式派发——`qodercli -p "<prompt>" > agent.log 2>&1 &` 这种「输出缓冲到进程退出才落盘」的形态让运行期零可见性，是明令禁止的反模式。本机制的观察面是**阶段粒度**（哨兵出现在输出末尾）：`-p` 缓冲意味着阶段结束前日志静默——退出记录与窗口监听等的就是终止事件；若需阶段内进度/卡死检测，把 runner 换成流式输出（`--output-format stream-json`）形态。
- 终止判定 `DONE` / `INCOMPLETE` → 独立校验（见 stage-prompts.md）；其余终止判定 → U5；通过则派发下一阶段（回到 Recipe 1/2/3）。

## Recipe 4 — 阶段链与收尾（Stage Chain & Closure）——编排本体

- 阶段链固定顺序：`requirements → clarify → plan → tasks → checklist → analyze → implement → review`（2026-10-17 修订：纳入 checklist/analyze 质量门——无人值守循环执行完整版流程，日常手动开发常省略的非必须命令一律必经）；每阶段完成哨兵 = 大写阶段名 + `-DONE`（如 `PLAN-DONE`、`CHECKLIST-DONE`、`ANALYZE-DONE`）。尾标是完成的必要条件，充分条件由独立校验补齐。
- **U3→U4 接线**：U3 的终止判定决定去向——`DONE` / `INCOMPLETE` 进 U4 独立校验（`INCOMPLETE` 按伪完成处理）；`ANOMALY` / `FAILED` / `DEAD` / `TIMEOUT` / `NO_SIGNAL` 直接进 U5。U4 通过后才派发下一阶段。
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

- **本地拓扑**：项目在本机时省略 ssh/su，直接以本地项目为工作目录执行 runner；需求上下文先写简报文件（`/tmp/<topic>-sdd-brief.md`），子代理提示词只指示「先完整阅读简报，再执行对应阶段命令」——命令形态见 `.specify/shared/workflow/external-dispatch-recipes.md` § Recipe 5（本配方坍缩为引用）。监听同样走 `watch-target.sh`，只是去掉 ssh/su 层（`watch-model.md` §6）。
- **构建固化变体**：同一主机按角色分线（不同系统用户在各自目录固化不同层），仅经入口参数（执行身份、路径）区分，机制零新增分支——形态见同文件 § Recipe 6。

## Recipe 6 — 线路登记、归属信封与消息入口（064）

**环境级 Line Registry**：同一 OS 用户一份，缺省 `${XDG_STATE_HOME:-$HOME/.local/state}/spec-kit/lines`，`SPECIFY_LINE_REGISTRY_DIR` 可覆盖；每线一个 `<line_id>.json`，同线更新以 `<line_id>.lock` 排他锁串行化，写入为临时文件 + `fsync` + `os.replace` 原子替换。引擎无框架依赖：`scripts/line-registry.py`（Python 3 stdlib-only）。

**U0.5 注册（首次派发前）**：

```bash
python3 <skill-dir>/scripts/line-registry.py --action register \
  --line-id <line> --run-id <run> --project-dir <project-dir> --repo-root <repo-root> \
  --state active [--write-line --manifest <manifest> --worktree-path <wt> \
  --branch line/<line> --base-sha <sha>] --format json
```

注册失败（目录不可写、JSON 损坏）→ 显式上送并停止该线启动；不得回退到项目内共享路径。

**U6 注销（收尾后）**：`--action deregister --line-id <line> --reason <reason>`；closed 条目保留历史字段，`list --active` 不再返回。

**Watcher 归属参数**：每个监听窗口追加 `--line-id <line> --run-id <run> --registry <registry> --meta <log-…meta.jsonl>`；watcher 只消费 Registry 中登记且 start token 校验通过的 `runner_pid`/`cli_pid`（PID 文件中的未登记 PID 一律 `DEAD pid=unregistered`；登记了 `branch` 时校验 worktree 分支），输出行追加 `line= run= attribution=own|foreign|stale-run|unattributed|legacy`。只有 `own` 事件参与判定；`foreign`/`stale-run`/`unattributed` 只出现在摘要，不改变 verdict、进度或 Registry 状态。未提供归属参数时保持 058 兼容（`attribution=legacy`，无过滤）。

**持 lease 的监听窗口（I-19）**：持有 driver lease 时，`--window` MUST ≤ `ttl_seconds/3`（缺省 ≤200s），或给 watcher 传窗口内续租钩子。watcher 缺省窗口即 200s；显式声明的 lease 用 `--lease-ttl` 钉住上限（超限且无续租钩子 → 立即 usage 失败）：

```bash
... watch-target.sh ... --line-id <line> --run-id <run> --registry <registry> --meta <meta> \
  --lease-ttl 600 --window 200 \
  --lease-renew-cmd "python3 <skill-dir>/scripts/line-registry.py --action lease-renew --line-id <line> --session <session>" \
  --lease-renew-interval 60
```

`lease-renew` 在间隔 > ttl/3 时仍续租（不让活会话自伤），但会写入 `lease-cadence-violation` 历史事件并把 Registry 的 `last_event` 置为该违规。

**消息入口（无标识消息）**：归属判定下沉为确定性动作，驱动只呈现结果：

```bash
python3 <skill-dir>/scripts/line-registry.py --action resolve-message --message "<user message>" [--clarified]
```

- 活动线 = `active|waiting`；0 条 → `no-active`；恰好 1 条且无标识 → `route`；
- ≥2 条且无可识别标识 → `clarify`：**恰好一个问题**并列候选（line_id / project / branch / stage / state）；
- 用户回答仍不唯一（`--clarified`）→ `ambiguous-stop`：列候选并停止，不再问第二个问题；
- 可识别标识 = 显式 `line_id` token，或唯一匹配的 project/repo 路径或分支名。
- **禁止**用 `ps`/`pgrep`/进程名/cwd/环境态推断归属；一次澄清不阻断其他线路。

### U2 派发前查档（CLI Capability Profiles）

- 只读查阅 `references/cli/index.md` 与目标 `<cli>.md`；据此选择超时/脱离形态，**不复制档案内容**。
- 派发记录携带 `profile_id` / `profile_version` / `observed_cli_version`；匹配且无新事实不产生反馈。

## Recipe 7 — 工作区隔离与确定性集成（064）

### Worktree-per-write-line

```bash
git -C <repo> worktree add -b line/<line> <worktree_path> <base_sha>
# 等价形态（在仓库内执行）：git worktree add -b line/<line> <worktree_path> <base_sha>
```

- 每条写线一个独立 worktree + 专用分支 `line/<line>`；`worktree_path` / `branch` / `base_sha` 登记进 Registry。
- 缺省 `worktree_path=<repo_parent>/.spec-kit/worktrees/<repo-basename>/<line_id>`；目标已存在或跨文件系统 → 显式失败，不得复用/删除其他 line 的 worktree。
- 一个 worktree 同时只有一个写 line；阶段子代理只在该 worktree 内提交，**不得切换分支、创建/删除 worktree、改写其他 line 的 worktree**。
- 运行时记录（feedback / session / knowledge / exec-quant）写在各自 worktree 内；**阶段提交不提交运行时记录**（路径集合以 `data-model.md` § E8 为唯一枚举；`evidence/`、`history/`、`trigger/` 明确排除）。

### Ownership Manifest 与串行化

```bash
python3 <skill-dir>/scripts/line-registry.py --action ownership-check \
  --line-id <line> --manifest <registry>/manifests/<line>.json --format json
```

- Manifest 是 `owned_paths` / `read_only_paths` / `forbidden_paths` / `integration_depends_on` 的 owner；Registry 的 `owned_paths` 是投影。
- 路径先归一化（相对路径按 `repo_root` 展开、`realpath`、去尾分隔符）再比较；写-写重叠（相等或互相包含）在注册/派发前拒绝或串行化。
- 重叠按当前认领时间 FIFO（Manifest/条目 `claimed_ns`，无则 `created_at` 的 epoch ns；同一时间戳 `line_id` 字典序 tie-break）串行：后到线 `state=waiting`，持 `waiting_reason=ownership-overlap`、`holder_line_id`、`queued_at`。`ownership-check` 重新认领会刷新 `claimed_ns`，因此重认领的线排在既有等待者之后，不能凭旧 `created_at` 抢占。
- `ownership-check` **不再隐式晋升**：冲突消失后 waiting 线保持 waiting 并返回 `promotion_required=true`，只有显式 `promote-waiting` 才能晋级。
- 持线者死亡**不自动释放**：`deregister --reason stale-cleanup` 只把线标记为 `state=stale`（`stale_at`），不关闭、不释放 ownership、不释放 reservation；随后必须经 `release-ownership --reason --evidence-ref` 显式处置（stale → closed）。`promote-waiting` 仅当持线者满足以下之一时才放行：① 当前 Manifest 已由 `release-ownership` 释放（`released_at` + 带 `evidence_ref` 的历史）；② `integration_result.status=merged`（真实存在且可从 trunk HEAD 到达的提交）且已完成 U6 `closed`。仅 `deregister --reason abandoned`（无 release 证据）的 closed 线仍然阻止晋升。
- **任何进入 active 的路径同闸**：`register --state active` 携带重叠 manifest 会被拒绝（exit 3）；`update --state active` 在从 waiting/stalled 等非 active 状态迁移时执行同一冲突扫描，已释放（Manifest `released_at`）的写线必须先 `ownership-check` 重新认领。`ownership-check` 会写入 `claimed_at`/`claimed_ns` 并清除旧的 `released_at`，因此旧的释放历史不能解锁新的占用，重新认领按当前时间排队；`closed/stale/orphaned` 条目不得重新认领。
- **状态一致性**：`closed` 是终态，任何 `update` 不得复活；`update` 进入 active 只允许来自 waiting/stalled。`release-ownership` 对 `active`/`waiting` 线会把它置为 `stalled`（停止写入，等待显式 U5/U6），对 `stale`/`orphaned` 则关闭。`allocate-resources` 只接受 active 线。ownership 影响动作在环境级 `.ownership.lock` 内串行，避免并发注册双赢。
- **路径纪律**：`owned_paths` 在 register/update 写入前归一化（相对路径按 repo_root、realpath、去尾分隔符），活动线新增 owned_paths 走冲突闸门（与 active 线冲突时无条件拒绝）；`update` 不能清空 owned_paths（释放走 `release-ownership`），也不能用投影遮蔽 manifest（路径集变更走 `ownership-check`）。`worktree_path`/`branch`/`base_sha` 设置后不可改写，worktree 必须在 repo_root/project_dir 之外且不是 repo root；`integration-record` 校验 worktree 分支与登记一致。closed/stale/orphaned 线不接受 lease/reserve。
- `integration_result` 只能经 `integration-record` 写入（`update` 不提供该字段）；`merged` 需要真实存在、可从 HEAD 到达且包含该线 worktree HEAD 的提交，写线还必须保留可验证的 worktree（非 git `repo_root` 拒绝 merged）。
- 任何 line 不得写入另一活动 line 的 `read_only_paths` / `forbidden_paths`。

### Integration Protocol（单一协调者）

1. `integration-plan`：输入 `state=completed` 且 `merge_ready=true` 的条目 + 各线 `integration_depends_on`；拓扑分层，同层按 `(ready_for_merge_at, line_id)`，重放逐字相同；环 → 显式拒绝。
2. 逐线序列由可执行执行器完成（`scripts/integrate-lines.py`；stdout 输出 JSON 摘要，含每线状态与 `archive_calls`/`mirror_calls` 计数）：

   ```bash
   python3 <skill-dir>/scripts/integrate-lines.py \
     --repo <repo> --trunk <trunk> --registry <registry> --archive <archive-dir> \
     [--gate-cmd "<完整质量门命令>"] [--mirror-cmd "python3 scripts/python/sync-mirrors.py --write ..."] \
     [--lines <line>[,<line>...]]
   ```

   执行器按顺序执行：`git -C <worktree> rebase <trunk>` → 质量门 → `git -C <repo> merge --ff-only <rebased-sha>` → `integration-record --result merged --commit` → `archive-runtime`（移除 worktree 之前，冲突保留双方） → `git worktree remove <worktree>`（仅 merged，**无 `--force`**）。仓库必须已检出 trunk；执行器**不切换分支**，不满足时显式失败。
3. 任一步失败：`integration-record --result failed --reason …`，**保留 worktree 与证据**，继续下一条；该 line 的 U6 不自动执行。
4. **每批一次**：全部条目处置后执行器调用一次 `--mirror-cmd`（`sync-mirrors.py` 与命令副本再生成）；镜像/命令副本不在逐线序列中，**不得每 line 执行**。
5. 不 force push、不绕过确认门；push 仍是显式授权动作。MUST NOT force push。

### 构建/测试隔离

- 每线独立端口块（缺省 39000 + 20/线）、缓存目录与临时目录；或只读共享缓存。不得写共享路径、不得启动全局服务。
- 并发上限可配置（缺省 4，`SPECIFY_LINE_CONCURRENCY_CAP` 覆盖），派发前检查；超限线 `state=waiting`（`waiting_reason=concurrency-cap`）。
- 每条线报告端口、缓存/临时路径与上限使用情况。

### 崩溃与重入

- 恢复证据 = worktree + 状态脊 + Registry；stale lock **先验证持有者**再处置，不盲目删除。
- 重入先做一次 `--once` 快照，再决定派发/校验/恢复窗口。

### 脱离式 runner、reservation 与 lease（064）

**本地脱离**（`setsid` 可用时优先；本机 macOS 无 `setsid` 时用 `nohup + disown`）：

```bash
# 1) 派发前：原子 reservation 防重复启动；内容含 run_id、启动 PID、start token
python3 <skill-dir>/scripts/line-registry.py --action reserve --line-id <line> --stage <stage> \
  --run-id <run> --pid <launcher-pid> --start-token <launcher-token> --format json
# 已有 reservation：同 run_id 且 PID 身份有效 → attach；否则拒绝，绝不启动第二个同阶段进程
# reservation 的 pid = launch 方（launcher/runner 外壳）的启动身份；runner 启动后只更新 Registry 的 runner_pid，不重写 reservation

# 2) 脱离启动：交付的 runner 脚本 + 独立进程组/会话 + stdio 与主会话脱离
#    run-stage.sh 负责写四件套（PID + start token、原子 status、log、heartbeat）、
#    以 nohup 启动 CLI 子进程、wait 并按哨兵写终态；registry 更新失败时写 ANOMALY 并终止。
if command -v setsid >/dev/null 2>&1; then
  setsid nohup bash <skill-dir>/scripts/run-stage.sh \
    --line-id <line> --run-id <run> --stage <stage> --registry <registry> \
    --worktree <worktree> --prompt <prompt> \
    --pid-file <pidf> --status-file <status> --log <log> --heartbeat <heartbeat> \
    --sentinel <STAGE>-DONE --engine <skill-dir>/scripts/line-registry.py \
    --command "<cli> ..." \
    > <runner-log> 2>&1 < /dev/null &
else
  nohup bash <skill-dir>/scripts/run-stage.sh \
    --line-id <line> --run-id <run> --stage <stage> --registry <registry> \
    --worktree <worktree> --prompt <prompt> \
    --pid-file <pidf> --status-file <status> --log <log> --heartbeat <heartbeat> \
    --sentinel <STAGE>-DONE --engine <skill-dir>/scripts/line-registry.py \
    --command "<cli> ..." \
    > <runner-log> 2>&1 < /dev/null &
  disown
fi

# 3) runner 行为（由 run-stage.sh 实现，勿在调用方重复）：
#    nohup bash -c "<cli> ..." >> <log> 2>&1 &  →  pid 文件记录 cli_pid + start token
#    Registry update --runner-pid/--runner-start-token/--cli-pid/--cli-start-token
#    wait cli_pid；按 log 最后非空行与 --sentinel 写原子 status（exit/sentinel）
```

- 主会话进程/会话终止信号 MUST NOT 传播到子代理；stdio 一律重定向到日志或 `/dev/null`。
- runner 启动时写四件套（PID + start token、原子 status、log、heartbeat）并在 Registry 登记 `runner_pid` / `cli_pid` 与各自 start token。
- 远端拓扑同构：`ssh <alias> "nohup su - <run-user> -c 'bash <runner> …' < /dev/null > /dev/null 2>&1 &"`；Registry 仍在驱动侧，字段与本地相同，仅增加 `remote.alias` / `remote.run_user` / `remote.remote_root`。
- **driver lease**：会话接管一条 line 前 `lease-acquire`（`O_CREAT|O_EXCL`）；活持有者 → exit 3；过期 lease 先验证证据再 `lease-break --reason --evidence-ref`；PID 活 + token 匹配 + 心跳过期 = `suspected-alive`，只允许 `--override` 破除。持有者以 ≤ `ttl_seconds/3`（缺省 ≤200s）续租，并在 U2/U3/U4/U5 各续租一次；watch window 遵守 Recipe 6 的窗口上限或续租钩子。
- **重接线**：`lease-acquire` → `verify-identity`（runner/cli start token、cwd、branch）→ `watch-target.sh --once` → 三分支；不依赖会话记忆或宽泛进程扫描。

## Boundary

- 远端不可达 / 凭证失效 / 子代理 CLI 不在执行身份路径：前置检查（run-agent dispatch-preflight.md）拦截并给修复动作，不裸报错弃线。
- 目标项目无 `.specify/`：报告停线，不自动初始化。
- 断点无法判定：停线上送用户裁定，不猜起步阶段。
- 撰写底稿注解：本文件操作要点撰写时取材于 shared 层 `external-dispatch-recipes.md` 与 `unattended-loop-pattern.md` 底稿；运行时零依赖。同型机制段已按 2026-10-16 委派化裁定坍缩为引用（Preflight→run-agent、R0/R1/R5→配方真源），保留面=心跳/脱离形态权威落点/阶段链收尾。
