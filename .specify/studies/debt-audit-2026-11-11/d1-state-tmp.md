# D1 — 运行期区域债务审计（`.specify/state/` 与 `.specify/.tmp/`）

> **Seat**: SDD Debt Governor（debt-governor） · **Date**: 2026-11-11 · **Mode**: read-only audit + governance design
> **Project root**: `/storage/project/cloud-native-ai/spec-kit` · **Assigned branch**: `master`
> **Write surface**: only this file — no project file was deleted, moved, archived or rewritten.
> **Reading timestamps**: T0 = 2026-11-11T02:55Z（10:55 +08）; T1 = 2026-11-11T03:01Z（11:01 +08）. Totals are given at both points where they moved.
> **Concurrency reading** (per 093 / `serial-reason.yaml`): `requested=1 / effective=1 / effective_reason=single-unit` — the dispatch assigned one bounded domain.
> **Anchors**: scope = `state/` + `.tmp/` only; output = this file; execution authorization = **none**.

---

## 0. 覆盖声明与前提校正

**覆盖**（两棵根，均为存在、已 gitignore、零跟踪的观测面）：

| Root | Exists | Files (T1) | Size (T0 → T1) | git tracked | ignore rule |
|---|---|---|---|---|---|
| `.specify/state/` | yes | 1,178 | 263M → **268M** | 0 | `.specify/.gitignore:34` → `state/` |
| `.specify/.tmp/` | yes | 46,954 → **57,002** | 647M → **824M** | 0 | `.specify/.gitignore:30` → `.tmp/` |

`git check-ignore -v` 对两棵根的子文件均命中，`git ls-files` 均为 0：**ignore / tracking 一致，无违规**。

**前提校正（Premise correction）**：

1. 任务书写“分支 master”；实测 `git branch --show-current` = **`debt-audit-harness-binding`**（HEAD `733ac70e8`，与 master 同提交的临时审计分支）。工作树 9 项脏（6 modified + 3 untracked，含 `.specify/skills/internal/debt-audit/`、`skills/internal/debt-audit/`），均为既有审计载体，不是本席产出。
2. `.tmp` 在审计窗口内自 647M 增至 **824M**：新增 `.specify/.tmp/binding-base`（git worktree，10,032 文件 / 177M，创建于 10:59），另 `state/` 增加约 5M（本审计 raw 转录，30 文件 / 4M）。**本报告所有 `.tmp` 组成数据标注 T0/T1。**
3. 任务基线的“registry”经复核 = **环境级行注册表** `~/.local/state/spec-kit/lines/`（非 `.specify/features.md`）。两个注册表分别复核，结论不同，见 §3。

**未评估（显式）**：raw 转录的语义内容（仅尺寸/时间读数）；全量 57k 文件的 hash 分组（仅对 `state/*.md` 与 `.tmp` 根文件做）；复制树内 mtime 为源文件保留时间，不等于创建时间；`/proc/<pid>` 存在性只证明进程存活，不证明身份。

---

## 1. 机械读数

### 1.1 `state/` 按类读数

| 类 | 计数 | 大小 | 说明 |
|---|---|---|---|
| 线脊 `*.md` | 32 | 736K | 27 主线脊 + 4 `*-u5-handoff.md` + 1 无 loop-state 的 `speckit-docs-expression.md` |
| `raw-*.jsonl` | 326 | 201M | 095–100 = 314 / 201M；其余 12 = 本审计 + coaching |
| `log-*.log`（runner stdout） | 163 | **61M** | 唯一有体积的日志类；最大单文件 `raw-099-speckit-seal-plan.jsonl` 7.4M |
| `runner-log-*.log` | 163 | **0** | 全部 0 字节（每次运行仍创建空文件） |
| `heartbeat-*.log` | 163 | 652K | 每次运行一份 |
| `status-*` | 159 | 636K | 156 规范 + 2 `.attempt0` + 1 `.bak-attempt1` |
| `pid-*` | 163 | 652K | 6 活 / 157 死（见 §1.4） |
| `wp/*.json` | 4 | 20K | 088 已关闭特性的 gate 计划 |
| `eval-baseline/` | 2 | 32K | 2026-10-27 的 README + instructions 快照 |
| 其他 | 3 | ~20K | `ts-clarify-start`、`083-*-tests.txt`、`083-loop-state-self-test.txt` |
| **合计** | **1,178** | **268M** | T0 263M |

**按线分布（state 根内文件名匹配）**：

| 线 | 文件 | 大小 | 行注册表状态 |
|---|---|---|---|
| 095-superagent-role | 193 | 49M | closed（11-10 16:04Z） |
| 096-sdd-observer-agent | 247 | 51M | closed（11-10 16:20Z） |
| 097-speckit-migrate-command | 191 | 42M | closed（11-10 16:21Z） |
| 098-suite-speed-optimizations | 261 | 57M | closed（11-10 20:12Z） |
| 099-speckit-seal | 176 | 52M | closed（11-10 19:53Z） |
| 100-seal-slice-archive | 42 | 13M | active |
| 074 / 074b | 2 / 1 | 36K / 12K | stalled / closed |

- **095–099 闭环线残留合计：1,068 文件 / 251M**（其中 raw 190M）。
- 文件日期分布（T0）：`2026-10-27` 1；`10-29` 1；`10-30` 4；`10-31` 1；`11-05` 6；`11-06` 1；`11-07` 3；`11-09` 5；`11-10` 880；`11-11` 270。最老 `speckit-docs-expression.md`（10-27，16 天）。
- 0 字节文件：`state/` 163（全部是 runner-log）；空目录 0。

### 1.2 `.tmp/` 按根读数（T0 → T1）

| 子树 | 文件 | 大小 | 最新日期 | 性质 |
|---|---|---|---|---|
| `quarantine-098/` | 17,216 | 274M | 11-10 / 11-11 | 两棵完整 repo 快照（wp5 8,554/134M；wp7 8,662/141M），**无 manifest** |
| `sdd-loop/worktrees/` | 9,652 | 154M | 11-11 | 仅 `100-seal-slice-archive`（活跃线，已注册 worktree @ `134daf45f`） |
| `sdd-loop/forks/` | 551 | 73M | 11-10 | 56 个 fork 运行包（每包 9 文件：status/raw/prompt/heartbeat/log/pid/runner-log），无 git |
| `sdd-loop/tmp/` | 177 | 760K | 11-11 | 按线 prompt/结果；含 095–099、`101-debt-governor-agent/prompt-requirements.md` |
| `script-interface-*`（9 目录） | 19,174 | 129M | 11-10 | 3 个大沙箱（55M/46M/28M）+ 6 个仅 1 文件的残壳 |
| `binding-base/` | 10,032 | **177M** | 11-11 10:59 | 当前审计的 git worktree（detached `733ac70e8`），T1 新增 |
| 根散文件 | 89 | 16M | 11-10/11-11 | 44×`095-*`、18×`history-*` 等；含当前安全快照 `main-tree-dirty-20261111.tar.gz` 108K |
| 其他小目录 | ~80 | ~3M | 11-05…11-11 | `082-part5` 29、`histw1-scratch` 37、`s094` 0（空）、`repair-078` 1、`analyze-r3` 1、`repair-r1` 2 等 |

- 0 字节文件：`.tmp/` **3,244**；空目录 **943**（几乎全部位于被复制的树内）。
- 根散文件重复组 7 组：6 组含内容（如 `095-mirror-check.txt` ≡ `095-mirror-check2.txt`；3 份 `history-seam-snapshot-*` 相同），1 组为 4 个空文件。
- `quarantine-098/wp7-before-tree` 携带 `.git`，HEAD `dbe948684`；`git cat-file -e` 验证该提交**在主仓可达**（无独有提交），不存在删除丢提交风险。wp5 无 `.git`。

### 1.3 行注册表（`~/.local/state/spec-kit/lines/`）

- 43 项 = 20 个 line JSON + 21 个 lock（含 `.ownership.lock`）+ `speckit-068-execquant-feedback.lease-history.jsonl` + 1 个旧布局目录 `speckit-068-execquant-feedback/state-spine.md`。
- 20 个 line 条目中 18 个 `state: closed`、1 个 `stalled`（074）、1 个 `active`（100）。
- **孤儿 lock**：`098-suite-speed-optimizations-implement-wp9.lock` 无配对 JSON、无 registry 记录；其余 line lock 为 0 字节 flock 文件，按 `line-registry.py` 的 `a+` 打开语义属于持久文件，不是“持有中的锁”。
- 101 条目 `state: closed`，但其 `spine_path` 指向的 `.specify/state/101-debt-governor-agent.md` **不存在**。

### 1.4 孤儿 pid / status / 哨兵

- pid：163 个，**157 死 / 6 活**；活的 6 个 = 100-analyze（`pid=233737`）+ 本审计 5 个 lane。基线 156 死 → 157 死（一变）。
- `sentinel=0`：**4 个**（基线 4，不变）：`status-096-...-implement-wp02`、`status-098-...-implement-wp1`、`...-wp1b`、`status-098-...-wp9.bak-attempt1`；前三个所属线已 closed，阶段后来重试/关闭。
- 备份式命名：`status-095-...-plan.attempt0`、`status-095-...-tasks.attempt0`、`status-098-...-wp9.bak-attempt1`。

### 1.5 状态脊 × 行注册表 × 特性索引（三处对读）

| 线 | 脊 `spine_state` / stage | 行注册表 | `features.md` | 判定 |
|---|---|---|---|---|
| 074 | running / review（10-29 deadline） | **stalled**（10-28 更新） | Ready for Review | 矛盾 |
| 074b | running / review（mtime 10-29） | **closed**（10-29 07:12Z） | 无行（074 切片） | 矛盾 |
| 081 | running / implement（deadline ≈11-03） | **无条目** | Completed | 矛盾 |
| 086 | running / implement（deadline ≈11-06） | **无条目** | Ready for Review | 矛盾 |
| 092 | running / implement（deadline ≈11-09） | **无条目** | Relocated | 矛盾 |
| 093 | **running** / **stage: closed** | **无条目** | Blocked | 脊自相矛盾 |
| 094 | running / implement（deadline ≈11-09） | **无条目** | Ready for Review | 矛盾 |
| 095 | **active** / review round 2（mtime 11-11 00:03） | **closed**（11-10 16:04Z） | Ready for Review | 矛盾 |
| 096 | **running** / review（mtime 11-11 00:06） | **closed**（11-10 16:20Z） | Ready for Review | 矛盾 |
| 097 | **running** / review-repair-r1（mtime 11-11 00:09） | **closed**（11-10 16:21Z） | **无行** | 矛盾 + 缺行 |
| 098 | **running** / review（mtime 11-11 02:48） | **closed**（11-10 20:12Z） | **无行** | 矛盾 + 缺行 |
| 099 | **running** / requirements（mtime 11-11 02:19） | **closed**（11-10 19:53Z） | Ready for Review | 矛盾 |
| 100 | active / **stage: requirements** | active（last_event=registered） | **无行** | 脊内 stage 与 Stage Records/status 矛盾 |
| 101 | **无脊文件** | closed（spine_path 悬空） | 无行 | 孤儿路径 |

`features.md` 共 92 行；097/098/100 无行；096 的 Feature Details 指向非规范名 `.specify/features/096.md`（其余为 `<ID>-<slug>.md`）。

---

## 2. 基线逐条复核（上午两轮 → 本次）

| # | 基线项 | 本次读数 | 判定 |
|---|---|---|---|
| 1 | state 261MB / 1,141 文件 | 263M / 1,178（T0）→ 268M（T1） | **changed**（+37 文件；审计 raw + 100 线推进） |
| 2 | raw 314 份 / 199MB | 095–100 仍 314 份；closed 五线 190M + 100 线 11M；总数 326（+12 审计/coaching） | **still**（闭环集合）/ changed（总数） |
| 3 | log 157 份 / 60MB | `log-*.log` **163 / 61M**；另有 runner-log 163 / **0**、heartbeat 163 / 652K | **changed**（+6） |
| 4 | 095–099 闭环线残留 | 1,068 文件 / 251M | **still** |
| 5 | 线 100 活跃（34 状态文件） | 42 文件 / 13M（status 5、pid 6、raw 12、日志 18） | **changed**（线在推进） |
| 6 | 156 dead pid | 163 pid：**157 dead / 6 alive** | **changed**（+1 dead） |
| 7 | 4 个 sentinel=0 | 4 个（3 规范 + 1 `.bak`） | **still** |
| 8 | 孤儿 lock | 21 个 lock；1 个无配对 JSON 的 stage lock（`098-...-wp9`） | **still**（精确化） |
| 9 | 095 active vs closed | 脊 active / 注册表 closed | **still** |
| 10 | 096–099 running vs closed | 四脊 running / 四注册表 closed | **still** |
| 11 | 074 running vs stalled | 脊 running / 注册表 stalled | **still** |
| 12 | 074b running vs closed | 脊 running（10-29 未再动）/ 注册表 closed | **still** |
| 13 | 081/086/092/093/094 running 无 registry | 五脊 running；行注册表 0 条目 | **still** |
| 14 | quarantine-098 274MB/17,216 无 manifest | 274M / 17,216；无 manifest；wp7 含 `.git`（HEAD 主仓可达） | **still**（新增：含 .git） |
| 15 | script-interface-* 9 目录 / 129MB / 19,174 | 完全一致 | **still** |
| 16 | forks 56 / 73MB | 56 目录 / 551 文件 / 73M，均 11-10 | **still** |
| 17 | 根散文件 89 / 16MB | 89 / 16M；7 组重复；含当前安全 tarball | **still** |
| 18 | 101 prompt 残留 | `.tmp/sdd-loop/tmp/101-debt-governor-agent/prompt-requirements.md` 1 / 12K | **still** |
| 19 | worktrees 仅剩 100（153MB） | 100 worktree 9,652 / 154M；**新增** `binding-base` 10,032 / 177M worktree | **changed**（+177M） |

**基线之外的新发现**：097/098 在 `features.md` 缺行；100 脊内 stage 矛盾；101 `spine_path` 悬空；state 内容类未声明（脊仅占 0.3% 文件 / 0.3% 字节）；runner-log 全 0 字节；`096.md` 非规范命名；3,244 零字节 + 943 空目录（复制树内）；`.tmp` 根 7 组重复；`attempt0/.bak` 命名；当前分支与工作树脏。

---

## 3. 债项表（状态 | 类别 | 证据 | 事实 | 严重度 | 处置 | lane）

> 处置词汇：`state/` 属 Non-Disposable 回顾面，用 ND 四值（`archive` / `supersede` / `correct` / `exempt`）；`.tmp/` 不在回顾面，用 sanitize 五值（`delete` / `archive` / `repair` / `delegate` / `dismiss`）。排序：严重度降序，同级按证据路径序。

| # | 状态 | 类别 | 证据 | 事实 | 严重度 | 处置 | lane |
|---|---|---|---|---|---|---|---|
| D1-01 | still | status-unreadable | `.specify/state/096-sdd-observer-agent.md`、`097-speckit-migrate-command.md`、`098-suite-speed-optimizations.md`、`099-speckit-seal.md` ↔ `~/.local/state/spec-kit/lines/{096,097,098,099}-*.json` | 4 条脊 `spine_state: running`；4 条注册表 `state: closed`（11-10 16:20/16:21/20:12/19:53Z）；098 脊 mtime 11-11 02:48 晚于注册表关闭 | P1 | correct | SDD repair（close-out 同步 + 守卫） |
| D1-02 | still | status-unreadable | `.specify/state/095-superagent-role.md` ↔ `.../095-superagent-role.json` | 脊 `active` / review round 2（mtime 11-11 00:03）；注册表 `closed` 11-10 16:04Z | P1 | correct | SDD repair |
| D1-03 | still | status-unreadable | `.specify/state/074-goal-team-sdd-unification.md`、`074b-nested-governance.md` ↔ 对应注册表 JSON | 074 脊 running / 注册表 `stalled`（updated 10-28）；074b 脊 running（mtime 10-29）/ 注册表 `closed` 10-29 07:12Z | P1 | correct | SDD repair |
| D1-04 | still | status-unreadable | `.specify/state/{081,086,092,093,094}-*.md`；`~/.local/state/spec-kit/lines/` 无对应 JSON | 5 脊 running，0 注册表条目；deadline 已过（≈11-03…11-09）；093 脊 `stage: closed` 与 `spine_state: running` 自相矛盾 | P1 | correct | SDD repair |
| D1-05 | changed | status-unreadable | `.specify/state/100-seal-slice-archive.md`；`status-100-*`；`pid-100-seal-slice-archive-analyze`；注册表 100 JSON | loop-state `stage: requirements` / last_verdict U0，但 Stage Records 已有 clarify + checklist，status 覆盖 requirements/plan/tasks/clarify/checklist，且 analyze pid 233737 存活 | P1 | correct | SDD repair |
| D1-06 | still | retention-gap | `.specify/state/` 中 095–099 全量文件 | 闭环线残留 1,068 文件 / 251M（raw 190M）；框架图与目录治理未声明这些 per-run 载体的保留 owner | P1 | exempt（expiry on-date 2026-12-11；recheck 2026-11-18） | sanitize retention lane（参数待裁） |
| D1-07 | new | governance-gap | `.specify/state/` 整体 | 目录治理只声明“每线一脊（`<line_id>.md`）”；实测脊 32 文件 / 736K，其余 1,146 文件 / ~267M 为 runner per-run 产物，无声明内容类与保留规则 | P1 | correct（声明内容类 + 保留 owner） | SDD repair（framework-map / directory-governance） |
| D1-08 | still | temp-lifecycle | `.specify/.tmp/quarantine-098/` | 17,216 文件 / 274M，两棵 repo 快照；**无 manifest**；wp7 含 `.git`（HEAD `dbe948684` 主仓可达）；含 11-11 日期文件，晚于 098 注册表关闭 | P1 | delete（单批前置确认） | sanitize materials |
| D1-09 | still | temp-lifecycle | `.specify/.tmp/script-interface-*/`（9 目录） | 129M / 19,174 文件；3 个被中断的大沙箱（55M/46M/28M）+ 6 个单文件残壳；095 `closure-suite.txt` 记录其导致 Permission denied 测试噪声 | P1 | delete + 引擎启动清扫 | sanitize + SDD repair |
| D1-10 | still | temp-lifecycle | `.specify/.tmp/sdd-loop/forks/`（56 目录） | 551 文件 / 73M，全为 11-10；每目录 9 文件运行包；无 git；均为已关闭线的 scratch；仅被历史证据文本引用 | P1 | delete | sanitize |
| D1-11 | new | governance-gap | `.specify/.tmp/binding-base/` | 活跃 git worktree（detached `733ac70e8`），10,032 文件 / 177M，11-11 10:59 创建；位于已声明根 `sdd-loop/worktrees/` 之外；使 `.tmp` 在审计中由 647M 增至 824M | P1 | exempt（on-date 2026-11-12；审计结束即移除或迁入 `sdd-loop/worktrees/`） | keep-with-policy（审计载体 owner） |
| D1-12 | new | registry-gap | `.specify/features.md`；`.specify/features/096.md` | 92 行；097/098（均已合并、注册表 closed）无行；100 无行；096 详情指向非规范 `096.md` | P1 | correct | SDD repair |
| D1-13 | new | reference-hygiene | 254 个 tracked spec 文件含 `.specify/.tmp` 路径；`095-appendix-check.py` 仅存于 `.tmp` 根（3.5K） | 活 checker 只存在于 scratch；其余为历史命令记录。删除 scratch 会使记录的命令不可重放 | P2 | supersede（把活脚本迁入 `test-evidence/`，旧路径留指针） | SDD repair |
| D1-14 | still | temp-lifecycle | `.specify/.tmp` 根：89 文件 / 16M | 无 `<purpose>/` 分组；44×`095-*`、18×`history-*`；7 组重复（6 组含内容、1 组全空）；安全快照 tarball 108K | P2 | delete（重复与过期；tarball 留至审计结束） | sanitize |
| D1-15 | new | ungoverned-naming | `.specify/.tmp/s094`（空）、`082-part5`（29/11-05）、`repair-078`、`analyze-r3`、`repair-r1`、`history-batches` | ad-hoc 短名/无 owner/无 manifest；`s094` 为空目录 | P2 | delete | sanitize |
| D1-16 | new | ungoverned-naming | `.specify/state/status-095-...-plan.attempt0`、`...-tasks.attempt0`、`status-098-...-wp9.bak-attempt1` | 机器管理的 state 根内出现 `.attempt0` / `.bak` 备份命名；后者同时携带 `sentinel=0` | P2 | correct（对账后移除） | SDD repair |
| D1-17 | still | orphan-status | 4 个 `sentinel=0` status（096-wp02、098-wp1、098-wp1b、098-wp9.bak） | 所属线已 closed；阶段后来重试/关闭；哨兵 0 未在收口时对账 | P2 | correct | SDD repair |
| D1-18 | changed | orphan-pid | `.specify/state/pid-*` | 163 个：157 死 / 6 活（100 analyze + 本审计 5 lane）；基线 156 死 | P2 | exempt（on-date 2026-12-11）→ 随 per-run 产物回收 | sanitize retention |
| D1-19 | still | orphan-lock | `~/.local/state/spec-kit/lines/*.lock` | 21 个 0 字节 lock；1 个孤儿 stage lock `098-...-wp9.lock`（无 JSON）；其余为 flock 持久文件 | P2 | delete（仅孤儿）/ keep-with-policy（其余） | sanitize + engine note |
| D1-20 | new | ungoverned-naming | `.specify/state/eval-baseline/`（2/32K，10-27）、`wp/`（4/20K，088 gate 计划）、`ts-clarify-start`、`083-*.txt` | 无 per-line 身份的一次性产物混入线脊根；088 已 closed | P2 | archive | sanitize（layout/retention） |
| D1-21 | new | orphan-path | `~/.local/state/spec-kit/lines/101-debt-governor-agent.json`；`.specify/.tmp/sdd-loop/tmp/101-debt-governor-agent/prompt-requirements.md` | 注册表 `closed`，但 `spine_path` 指向的 `.specify/state/101-debt-governor-agent.md` 从未存在；1 个 prompt 残留 12K | P2 | correct（去悬空路径）+ delete（prompt） | SDD repair + sanitize |
| D1-22 | new | ungoverned-naming | `.specify/features/096.md` | 详情文件名 `<ID>.md` 与其余 `<ID>-<slug>.md` 不一致；注册表指向该文件，重命名须成对 | P2 | correct | SDD repair（或 sanitize layout lane） |
| D1-23 | new | zero-byte/empty | `.specify/.tmp` 复制树；`.specify/state/runner-log-*` | 3,244 零字节文件 + 943 空目录（复制树内）；state 163 个 0 字节 runner-log（每次运行仍创建） | P2 | delete（scratch）/ repair（runner 不建空文件） | sanitize + SDD repair |
| D1-24 | new | dirty-worktree | 工作树；`git branch --show-current` | 9 项脏（6 modified + 3 untracked，含 debt-audit 技能）；分支 `debt-audit-harness-binding` 而非 master | P2 | keep-with-policy（审计载体） | 审计 harness owner |
| D1-25 | clean | ignore/tracking | `.specify/.gitignore:30,34`；`git ls-files` | 两棵根均已 ignore，0 跟踪；无 ignore/tracking 违规 | — | keep-with-policy | governance |
| D1-26 | keep | active-worktree | `.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive` | 9,652 文件 / 154M；已注册 worktree @ `134daf45f`；线 100 active | P2 | keep-with-policy | driver lifecycle |

**P0：无。** 未发现不可逆的数据丢失风险：隔离树与 fork 均无独有 git 提交；state/tmp 全部被忽略、零跟踪。

---

## 4. 建议保留策略（Retention Policy Proposal）

### 4.1 `state/`（长期归档面）

| 载体 | 策略 |
|---|---|
| `<line_id>.md` 线脊 | **永久**，每线一件；关闭时脊必须置终态并与行注册表、`features.md` 同批对账；关闭后不可再改 |
| `raw-*.jsonl` / `status-*` / `pid-*` / `heartbeat-*` / `log-*` / `runner-log-*` | **活跃线保留 + 终态后 30 天**；到期后：被 tracked 证据引用 → `archive`（迁入 `.specify/archive/state/<line_id>/` 并留指针）；未被引用 → 经 retention-lane receipt 回收（与 073 的 consume→receipt→retire 同构；不新建引擎） |
| `runner-log-*.log` | 0 字节不再创建；已有 0 字节立即随 per-run 回收 |
| 备份后缀 | 禁止 `.attempt*` / `.bak*` / `.old`；需要证据时进 `test-evidence/` |
| 一次性产物（`eval-baseline/`、`wp/`、`ts-*`、`083-*.txt`） | 不得置于线脊根；登记归属或 `archive` |

### 4.2 `.tmp/`（scratch 面）

| 载体 | 策略 |
|---|---|
| 一般 scratch | 生命周期 = 工作项；无引用者**硬上限 7 天** |
| `quarantine-*/` 类快照 | 必须有 manifest（源提交 + 目的 + owner + 到期日）；上限 14 天；含 `.git` 时须先证明 HEAD 在主仓可达 |
| `script-interface-*` 沙箱 | 引擎启动时清扫 >24h 的残留（现有 `finally: rmtree` 只覆盖正常退出） |
| `sdd-loop/forks/` | 随线关闭移除；不在 `.tmp` 保留第二份运行证据 |
| `sdd-loop/tmp/<line>/` | 随线关闭移除 |
| 根散文件 | 禁止；必须落在 `.tmp/<purpose>/` 下 |
| 临时 worktree（如 `binding-base`） | 必须位于 `.tmp/sdd-loop/worktrees/` 或审计结束时移除 |

### 4.3 注册表与锁

- 线关闭时：`state` → `closed`，脊 → 终态，`lease` → null，`features.md` 行同步；close-out 作为**一步**执行并由守卫断言（否则本报告的 D1-01…D1-05 会复发）。
- `*.lock` 为 flock 持久文件，可保留；**stage 级 lock 必须有配对运行记录**，否则视为孤儿并清除。

---

## 5. 治理计划（分波次，先机制、后数据、再结构）

| 波次 | 内容 | 确认门 | 可测结果 | 中止条件 |
|---|---|---|---|---|
| **W1 机制修复**（SDD） | close-out 对账脊/注册表/features；修 100 loop-state；清理/归档 074/074b/081/086/092/093/094 过时脊；补 097/098/100 行；移除 attempt/bak；重命名 `096.md`；移除 101 悬空 spine_path | 可逆编辑自动执行 + 事后报告 | 脊/注册表矛盾 = 0；缺行 = 0；歧义命名 = 0 | 某线实际仍在运行 → 停在异常点并报告 |
| **W2 数据回收**（sanitize） | 批量删除过期 scratch：`quarantine-098`（274M）、`script-interface-*`（129M）、forks（73M）、根散文件（~16M）、关闭线 `sdd-loop/tmp` 与小目录（~1M）≈ **493M / ~37k 文件** | **一次前置批量确认**（破坏性桶） | `.tmp` ≤ ~330M（binding-base 177 + worktree 100 154 + 当前审计）；文件 ≤ ~20k | 任一目标含不可达 git 对象或被活跃证据引用 → 跳过该项 |
| **W3 状态回收**（policy + retention） | 按 §4.1 落地 30 天窗口；被引用者 archive、其余凭 receipt 回收 | 保留参数裁定 + 确认 | `state` 收敛到 ~20M 量级（脊 + 活跃线 + 30 天窗口） | 无 receipt 的记录 → 一律保留 |
| **W4 结构收敛**（SDD） | 在 `framework-map.md` / `directory-governance.md` 声明 state 内容类与 `.tmp` 子根；加 script-interface 启动清扫；runner 停止创建空日志；用既有引擎做周期确定性扫描 | 框架编辑走 SDD | 连续两条线后同类债不复发 | owner 文档冲突 → 升级裁定 |

**不做的事**：不新建扫描器 / 债务注册表 / 保留规则引擎；W2/W3 全部通过既有 `sanitize-utils.py` 与 retention lane；W1/W4 全部走 SDD 修复。

---

## 6. 裁决点（需要用户决定；本席不代答）

1. **W2 批量删除授权**：是否批准删除上述 ~493M / ~37k 文件的过期 scratch（`quarantine-098`、`script-interface-*`、forks、根散文件、关闭线 `sdd-loop/tmp`）？
2. **state 保留参数**：per-run 产物在“线终态后 30 天”回收是否采用？（建议：采用）
3. **state 回收方式**：被引用的 per-run 产物选 `archive`（迁入 tracked `.specify/archive/`，git +251M）还是 retention receipt 回收（推荐，避免 git 膨胀）？
4. **W1 现在执行？** 是否立即启动 SDD 修复，做 close-out 对账（脊/注册表/features）并为 097/098/100 补行？
5. **`binding-base` 去向**：审计结束即移除（推荐）还是迁入 `.specify/.tmp/sdd-loop/worktrees/`？

---

## 7. 边界与未评估

- 本报告只读：未删除、未移动、未归档、未改写任何项目文件（唯一写入为本文件）。
- raw 转录语义未读；复制树内 mtime 为保留时间；hash 分组只覆盖小集合。
- `alive` 判定仅基于 `/proc/<pid>` 存在；未验证 100-analyze 进程身份。
- 095 的 suite 噪声归因引用自该特性 `verification.md` / `closure-suite.txt`，未重跑测试。
- 行注册表与 `features.md` 是两个不同注册表；本报告分别陈述，不互相代替。

---

ANOMALY: 任务书声明分支 `master`，实测工作树在 `debt-audit-harness-binding`（HEAD `733ac70e8`），且有 9 项既有脏改动（含未跟踪的 debt-audit 技能目录）；本报告的全部读数取自该分支。
ANOMALY: 审计期间读数发生迁移：`.tmp` 新增 `binding-base` 工作树 177M/10,032 文件（10:59 创建），state 增加约 5M 审计 raw；报告以 T0/T1 双时点标注。
ANOMALY: 098 行注册表于 2026-11-10T20:12Z 记为 closed，但其脊在 11-11 02:48 仍被更新、`quarantine-098` 内存在 11-11 日期文件，且 review round 3 在关闭后继续——“已关闭”与后续工作并存。
DEBT-DONE
