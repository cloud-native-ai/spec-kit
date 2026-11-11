# 债务审计 D6 — 综合报告与差异对比

> **Seat**: SDD Debt Governor（debt-governor）· **Stage**: 债务审计 D6（综合与差异对比）
> **Date**: 2026-11-11 · **Project root**: `/storage/project/cloud-native-ai/spec-kit`
> **Branch / HEAD（综合时点）**: `master` / `c3997b182`（binding 提交已合入；工作树 2 项：`.specify/memory/trigger/index.json` 时间戳更新 + 本审计目录未跟踪）
> **Write surface**: 仅本文件（`.specify/studies/debt-audit-2026-11-11/report.md`）；未删除、移动、归档或改写任何其它项目文件
> **Concurrency reading**: requested=1 / effective=1 / effective_reason=`single-unit`（D6 综合为单席单单元；d1–d5 各自声明的并发读数同为 `single-unit`，五域并行由编排层承担）
> **Anchors**: 输入 = d1–d5 五份已验收域报告；输出 = 本文件；执行授权 = **无**（本报告只登记与设计治理，不执行任何清理）

---

## 0. 输入、方法与时间窗

### 0.1 输入

| 域 | 报告 | 范围 | 规模读数 |
|---|---|---|---|
| d1 | `d1-state-tmp.md` | `.specify/state/` + `.specify/.tmp/` | T1：state 268M / 1,178 文件；.tmp 824M / 57,002 文件 |
| d2 | `d2-specs-early.md` | `.specify/specs/` 001–074（60 目录） | 1,326 文件 / 16.3 MiB |
| d3 | `d3-specs-late.md` | specs 075–099 + `.specify/studies/` + `.specify/archive/` | 24 live 目录 / 2,755 文件 / 64.66 MiB（磁盘） |
| d4 | `d4-memory.md` | memory / history / register / glossary / tools / project / review | memory 1,536 文件 / 11 MiB；history 5,967,578 B；register 229 数据行 |
| d5 | `d5-code-surfaces.md` | scripts / templates / workflow / skills / agents / teams / anchoring / shared / 根层文件 | 引擎读数（sync-mirrors、regen、goal-utils、doc-consistency 等） |

### 0.2 去重与冲突裁决规则（本报告口径）

1. **同路径 + 同事实** → 合并一条，来源列同时标注两侧 ID。
2. **同路径 + 不同事实** → 保留为分项（如 `features.md` 同时承载缺行、坏指针、超长行三类独立缺陷），在事实列注明同路径关系。
3. **跨域读数冲突** → 以域报告的证据为准并注明来源；若综合时点复核推翻域读数，以复核为准并标 `resolved`（例：d5-01 模板漂移）。
4. 域报告之间的**域界**不被本报告改写：每条债项保留其原域的责任 lane。

### 0.3 时间窗与综合时点复核（T2 = 2026-11-11T03:12Z）

| 复核项 | 命令/证据 | 结果 |
|---|---|---|
| 分支与 HEAD | `git branch --show-current` / `git log` | `master` / `c3997b182`；binding 提交已合入 |
| worktree | `git worktree list` | 仅主仓 + `100-seal-slice-archive`（`134daf45f`）；`binding-base` **已移除** |
| 镜像漂移 | `python3 .specify/scripts/python/sync-mirrors.py --check` | **exit=0**；`templates/gitignore-specify-template` 与镜像 **byte-identical**（漂移由 `c3997b182` 修复） |
| state | `find` / `du -sm` | 272M / 1,189 文件（T1 268M/1,178） |
| pid | 逐文件读 `/proc` | 164 个 pid 文件，**0 活 / 164 死**（T1 为 157 死 / 6 活，6 活即审计 lane 与 100 analyze） |
| .tmp | `du -sm` | **650M**（T1 824M；`binding-base` 177M 移除所致） |
| script-interface | `du -sm` / `find -type f` | **10 目录 / ≈135M / 19,197 文件**（d1 时 9 目录 / 129M / 19,174；d5 自己的第 10 个沙箱缩至 312KB 后保留） |
| quarantine-098 / forks | `du -sm` | 274M / 73M（未变） |
| 工作树 | `git status --porcelain` | 2 项：`M .specify/memory/trigger/index.json`（仅 `updated` 时间戳 → 03:03:58Z）+ 未跟踪的本审计目录 |

**时间窗结论**：本报告的所有体量读数是**移动靶**。跨域数字已在表内标注所属时点；凡 T1 与 T2 有出入的，以两值并列。

---

## 1. 债项总登记表

> 处置词汇：ND 四值 `archive` / `supersede` / `correct` / `exempt`（owner: `shared/definitions/non-disposable-definitions.md`）；sanitize 执行动作 `delete / archive / repair / delegate / dismiss` 仅在括号内注记。lane = SDD 修复 / `/speckit.sanitize` 回收 / 保持并立政策 / 机制修复。排序：严重度降序，同级按主证据路径。**状态**：still（仍存在）/ changed（读数或判读变化）/ new（新增发现）/ resolved（已消解）。

### 1.0 汇总

| 严重度 | 条数 | 说明 |
|---|---|---|
| P0 | 1 | 治理守卫红且盲（d3 D3-01）——唯一 P0 |
| P1 | 27 | 结构性：状态真实性、注册表完整性、旧锚、保留政策、记录通道 |
| P2 | 55 | 计划性：布局噪声、命名、备份、陈旧索引、团队治理 |
| resolved | 3 | 模板漂移（d5-01）、binding-base（d1-11）、脏工作树（d1-24） |
| 合计 | 86 | 其中跨域合并 3 组（见 §4.7） |

### 1.1 P0

| ID | 状态 | 类别 | 证据 | 事实 | 严重度 | 处置 | lane | 波 | 来源 |
|---|---|---|---|---|---|---|---|---|---|
| D6-01 | new | 治理守卫红且盲 | `tests/contract/test_spec_feature_binding_integrity.py:49,69`；`.specify/features.md:99`；`specs/099-speckit-seal/baseline-failed.txt:119-120`；`specs/098-suite-speed-optimizations/baseline-failed.txt:122-123` | 实跑 2 failed/6.23s：C-1 报 092 与 048 的 spec 路径悬空；C-2 报 086/088/089/090 但 4 行**存在**——守卫的严格行正则静默跳过 4/92 行（裸 `\|` 或缺闭合 `\|`），既假红又失明；该红被固化进 **8** 份 `baseline-failed.txt`，新破坏不再可见 | P0 | `regenerate`（守卫改整行 schema 校验）+ `correct`（修 4 行与 048/092 路径） | SDD 修复 | W1 | d3 D3-01 |

### 1.2 P1

| ID | 状态 | 类别 | 证据 | 事实 | 严重度 | 处置 | lane | 波 | 来源 |
|---|---|---|---|---|---|---|---|---|---|
| D6-02 | still | 状态不可读 | `.specify/state/{096,097,098,099}-*.md` ↔ `~/.local/state/spec-kit/lines/{096,097,098,099}-*.json` | 4 脊 `spine_state: running`；4 注册表 `closed`（11-10 16:20/16:21/20:12/19:53Z）；098 脊 mtime 11-11 02:48 **晚于**关闭 | P1 | `correct`（close-out 同步 + 守卫） | SDD 修复 | W1 | d1 D1-01 |
| D6-03 | still | 状态不可读 | `.specify/state/095-superagent-role.md` ↔ `.../095-superagent-role.json` | 脊 `active` / review round 2（mtime 11-11 00:03）；注册表 `closed` 11-10 16:04Z | P1 | `correct` | SDD 修复 | W1 | d1 D1-02 |
| D6-04 | still | 状态不可读 | `.specify/state/074-goal-team-sdd-unification.md`、`074b-nested-governance.md` ↔ 注册表 JSON | 074 脊 running / 注册表 `stalled`（10-28）；074b 脊 running（10-29 未再动）/ 注册表 `closed` 10-29 07:12Z | P1 | `correct` | SDD 修复 | W1 | d1 D1-03 |
| D6-05 | still | 状态不可读 | `.specify/state/{081,086,092,093,094}-*.md`；行注册表无对应 JSON | 5 脊 running、0 注册表条目；deadline 已过（≈11-03…11-09）；093 脊 `stage: closed` 与 `spine_state: running` 自相矛盾 | P1 | `correct` | SDD 修复 | W1 | d1 D1-04 |
| D6-06 | changed | 状态不可读 | `.specify/state/100-seal-slice-archive.md`；`status-100-*`；注册表 100 JSON | loop-state `stage: requirements` / last_verdict U0，但 Stage Records 已有 clarify+checklist，status 覆盖 5 阶段，analyze pid 在 T1 存活 | P1 | `correct` | SDD 修复 | W1 | d1 D1-05 |
| D6-07 | still | 保留缺口 | `.specify/state/` 中 095–099 全量文件 | 闭环线残留 **1,068 文件 / 251M**（raw 190M）；框架图与目录治理未声明这些 per-run 载体的保留 owner | P1 | `exempt`（on-date 2026-12-11；recheck 2026-11-18）→ 回收 | sanitize retention lane（参数待裁） | W2+W3 | d1 D1-06 |
| D6-08 | new | 治理缺口 | `.specify/state/` 整体 | 目录治理只声明“每线一脊”；实测脊 32 文件 / 736K，其余 1,146 文件 / ~267M 为 runner per-run 产物，无声明内容类与保留规则 | P1 | `correct`（声明内容类 + 保留 owner） | SDD 修复（framework-map / directory-governance） | W3 | d1 D1-07 |
| D6-09 | still | 临时生命周期 | `.specify/.tmp/quarantine-098/` | 17,216 文件 / 274M，两棵 repo 快照；**无 manifest**；wp7 含 `.git`（HEAD `dbe948684` 主仓可达，无独有提交）；含 11-11 文件（晚于 098 关闭） | P1 | `delete`（单批前置确认） | sanitize materials | W2 | d1 D1-08 |
| D6-10 | still | 临时生命周期 + 权限阻断 | `.specify/.tmp/script-interface-*/`（d1：9 目录；T2：10 目录） | d1：129M / 19,174 文件，3 大沙箱 55/46/28M + 6 残壳；T2：≈135M / 19,197；**根因**：`script-interface-check.py` 中止后不清理（`finally: rmtree` 只覆盖正常退出）；`.tmp` 内 **520 个 root 属主条目**，agent 用户无法删除 | P1 | `delete` + 引擎启动清扫（>24h 残留）；root 授权处置 | sanitize + SDD 修复 | W2+W3 | d1 D1-09 + d5 D5-05（合并） |
| D6-11 | still | 临时生命周期 | `.specify/.tmp/sdd-loop/forks/`（56 目录） | 551 文件 / 73M，全为 11-10；每目录 9 文件运行包；无 git；均为已关闭线 scratch | P1 | `delete` | sanitize | W2 | d1 D1-10 |
| D6-12 | still | 注册表可见性 | `.specify/features.md`；`specs/{075,080,097,098}`；`.specify/features/` | 92 行；live spec **075/080/097/098/100 无索引行**；097/098 无详情；切片绑父特性（058/062/024/086），C-2 因父行存在不报红 → 注册表盲区 | P1 | `consolidate`（逐 spec 补行或父详情 + 指针） | SDD 修复 | W1 | d1 D1-12 + d3 D3-02（合并） |
| D6-13 | changed | 注册表坏指针 | `.specify/features.md:57`（行 048）；`archive/specs/046-browser-site-memory/` | 行 048 状态 Relocated，Spec Path 仍写 live 路径；live 目录不存在，spec 只在 archive；按 Spec Path 解析得 ENOENT | P1 | `normalize`（改指 archive 路径或置 `-`） | SDD 修复 | W1 | d2 D2-01 |
| D6-14 | still | 生命周期漂移 | `.specify/features.md:99`；`.specify/features/092-non-disposable.md:6`；`archive/specs/092-non-disposable/`；22 处 live 引用 | 行路径悬空且行文称工件仍在 live；详情 `Status: Planned` vs 行 `Relocated`；090/080/094 的 canonical 工件仍引用旧 live 路径 | P1 | `normalize`（行/详情/引用三处对齐） | SDD 修复 | W1 | d3 D3-03 |
| D6-15 | still | 注册表/状态矛盾 | `.specify/features.md:78`；`specs/069-execution-expression-sdd/requirements.md:6` | 行 069 Implemented 指向 live 父 spec；父只有 requirements.md 且 Status=Draft；交付证据在归档切片 069a/069b | P1 | `normalize`（推进/标注父状态 + 归档切片指针） | SDD 修复 | W1 | d2 D2-03 |
| D6-16 | changed | 旧锚腐烂（001–074） | 443 处 / 182 个规范性文档；热点 `specs/029-glossary-mechanism/plan.md` 12 处、`specs/050-proactive-flow-trigger/{requirements,tasks}.md` 各 10 处 | 规范性文档引用不存在的 `.specify/memory/*`；Top 目标 `memory/features.md` 110、`memory/constitution.md` 103、`memory/glossary.md` 34、`memory/feedback/probes/` 17 | P1 | `normalize`（确定性映射 + 日期性叙述 allowlist） | SDD 修复 | W1 | d2 D2-02 |
| D6-17 | still | 旧锚悬空（075–099 live） | 240 个缺失目标；`specs/082-*/requirements.md`（12）、`090-*/tasks.md`（11）、`089-*/plan.md`（10） | 全区间 3,037 次悬空 / 482 文件；**live canonical 子集 367 次 / 116 文件**；布局引擎 `anchor-layout-migrate.py --action check` → `{clean:true}`（引擎不重写文档内引用） | P1 | `regenerate`（只修 live 工件） | SDD 修复 | W1 | d3 D3-07 |
| D6-18 | still | review 权威碎片化 | `specs/096-*/review*.md`（6）、`097`（4）、`098`（6）、`099`（4）、`081`（8）、`084`（8）、`095`（4）；`093/094 notes/review-*.md`；`089`（0） | 根级 review 族 **65 文件 / 2.58 MiB**；28 个 loose 世代；093/094 评审只在 `notes/`；089 无评审；`driver-stage-artifacts` 只认 `review.md` | P1 | `consolidate`（单一权威政策 + 守卫） | SDD 修复 + sanitize 搬移 | W1 | d3 D3-04 |
| D6-19 | still | checkpoint 协议覆盖不全 | `skills/sdd-loop-driver/references/checkpoint-protocol.md:5`；`specs/096-*`、`099-*`、`097-*/checkpoints/`、`098-*/checkpoints/` | 协议自 085 起存在；**096=0、099=0、097=1/8、098=5/8**；缺失的是历史协作证据，不能事后伪造 | P1 | `normalize`（closure 记录豁免原因 + 协议校验） | SDD 修复 | W1 | d3 D3-05 |
| D6-20 | still | test-evidence 无保留政策 | `shared/declarations/facts/memory-retention-thresholds.yaml:20`；`specs/090-*/test-evidence/`；32 件 >200KB | specs scope apparent 58.40 MiB 中 **44.21 MiB（75.7%）是 test-evidence**；090 单篇 17.90 MiB；31/32 个 >200KB 在 test-evidence；保留引擎 store 闭集不含 spec 证据 | P1 | `keep-with-policy`（先定参数再回收） | SDD 修复（政策）+ sanitize（回收） | W3+W2 | d3 D3-06 |
| D6-21 | still | archive 根分裂且无主 | `shared/definitions/framework-map.md:17`；`.specify/archive/spec/`（8 目录/0.52 MiB/无台账）；`.specify/archive/specs/`（11 目录+台账/2.55 MiB） | framework-map 只声明 `archive/spec/`；`archive/specs/` 在 framework-map / skills / templates / src 中 **0 引用**——违反“无文档含义的目录不得创建”；两套命名同指一类对象 | P1 | `consolidate`（并根 + 台账随迁，或立第二声明层） | SDD 修复 + sanitize 搬移 | W1 | d3 D3-08 |
| D6-22 | still | 反馈上报通道停摆 | `.specify/memory/feedback/state/submitted-at.json`；`state/threshold.json` | 自 2026-10-08 起 **34 天**未 mark-submitted；464 条 = 阈值的 46.4×；129 条从未处置；`packages/` 不存在 | P1 | `correct`（恢复消费-打包-记账节奏） | SDD 修复（feedback 流程） | W1 | d4 D4-01 |
| D6-23 | new | 路由欠账 | `.specify/memory/feedback/backlog.md` | 176 行；**166 open-bearing**（119 `open` + 40 `**open**` + 7 `open-unverified`）；5 行表格损坏；最早路由 2026-08-31；“已路由 ≠ 已执行”堆积 | P1 | `correct`（执行/改派/按证据关闭） | SDD 修复 | W1 | d4 D4-02 |
| D6-24 | changed | 保留通道从未运行 | `.specify/memory/retention/plans/20261105T130456214498Z-retention-plan.json`；`retention/closeout/`（33） | **1,270 条记录全部 `blocked: unreceipted`**；eligible 0、receipts 0、ledgers 0；唯一 plan `confirmed=false`、items=[]；33 个 closeout 回执不喂保留引擎（相邻家族） | P1 | `correct`（跑通 distill→plan→apply 并定节奏） | sanitize（retention lane） | W1+W2 | d4 D4-03 |
| D6-25 | new | 量化轴全空 | `.specify/memory/exec-quant/records/`；`memory/session/*run-determination*` | exec-quant **357/357** 条 `quality` 五键全 `not_evaluated`，0 条 token 键；run-determination 435 条：token 435/435、elapsed 423/435、artifact 415/435、satisfaction 360/435 为 `not_evaluated` | P1 | `correct`（接传感器；接不上则登记带到期日 `exempt`） | SDD 修复 | W1 | d4 D4-04 |
| D6-26 | still | 整线记忆缺链 | `specs/098-suite-speed-optimizations/test-evidence/`（117 文件）；`.specify/state/098-*`（261 文件） | 098 经 analyze×3 / review×3 / merge 落地，但 run-determination 0、exec-quant 0、knowledge 0、feedback 0；缺的是记录层，不是活动 | P1 | `correct`（登记 OI + 日期性对账注记；不伪造） | SDD 修复 | W1 | d4 D4-05 |
| D6-27 | new | 红钉未裁 | `.specify/register.md:38`；`tests/contract/test_neutrality_budget.py`；`specs/053-machine-decidable-artifacts/contracts/neutrality-budget.md` §C-7 | c7 自 2026-10-11 起为红且登记行明写“MUST NOT 静默改写”；至今无裁定 | P1 | `correct`（完成重锚裁定；暂缓则 `exempt` 至 2026-12-11） | SDD 修复 | W1 | d4 D4-06 |
| D6-28 | still | 预算濒临溢出 | `.specify/instructions.md` | 38,301 B / 预算 38,400 B，余 **99 B**；规则要求下一次增节后至少留 1,024 B；超限仅告警不失败 | P1 | `correct`（按 owner 规则压缩，或走文档化 raise） | SDD 修复（`/speckit.instructions`） | W1 | d5 D5-02 |

### 1.3 P2

| ID | 状态 | 类别 | 证据 | 事实 | 严重度 | 处置 | lane | 波 | 来源 |
|---|---|---|---|---|---|---|---|---|---|
| D6-29 | new | 孤儿路径 | `~/.local/state/spec-kit/lines/101-debt-governor-agent.json`；`.specify/.tmp/sdd-loop/tmp/101-debt-governor-agent/prompt-requirements.md` | 注册表 `closed` 但 `spine_path` 指向的 `.specify/state/101-debt-governor-agent.md` **从未存在**；1 个 prompt 残留 12K | P2 | `correct`（去悬空）+ `delete`（prompt） | SDD 修复 + sanitize | W1+W2 | d1 D1-21 |
| D6-30 | new | 非受管命名 | `.specify/state/status-095-...-plan.attempt0`、`...-tasks.attempt0`、`status-098-...-wp9.bak-attempt1` | 机器管理的 state 根内出现 `.attempt0` / `.bak` 备份命名；后者同时携带 `sentinel=0` | P2 | `correct`（对账后移除） | SDD 修复 | W1 | d1 D1-16 |
| D6-31 | still | 孤儿 status | 4 个 `sentinel=0` status（096-wp02、098-wp1、098-wp1b、098-wp9.bak） | 所属线已 closed；阶段后来重试/关闭；哨兵 0 未在收口时对账 | P2 | `correct` | SDD 修复 | W1 | d1 D1-17 |
| D6-32 | changed | 孤儿 pid | `.specify/state/pid-*` | T1：163 个 157 死 / 6 活；**T2：164 个全部死** | P2 | `exempt`（on-date 2026-12-11）→ 随 per-run 回收 | sanitize retention | W2+W3 | d1 D1-18 |
| D6-33 | still | 孤儿 lock | `~/.local/state/spec-kit/lines/*.lock` | 21 个 0 字节 lock；1 个孤儿 stage lock `098-...-wp9.lock`（无配对 JSON） | P2 | `delete`（仅孤儿）/ keep-with-policy（其余） | sanitize + engine note | W2 | d1 D1-19 |
| D6-34 | new | 非受管命名 | `.specify/state/eval-baseline/`（2/32K，10-27）、`wp/`（4/20K，088）、`ts-clarify-start`、`083-*.txt` | 无 per-line 身份的一次性产物混入线脊根；088 已 closed | P2 | `archive` | sanitize（layout/retention） | W2 | d1 D1-20 |
| D6-35 | changed | 详情命名漂移 | `skills/internal/manage-features/SKILL.md:29`；`shared/definitions/framework-map.md:9`；`skills/internal/sanitize-materials/SKILL.md:375-378`；`.specify/features/096.md`；其余 91 个 `<ID>-<slug>.md` | **两名 owner 文本互相冲突**：manage-features/framework-map 声明 `<ID>.md`，sanitize layout lane 声明 `<NNN>-<slug>.md`；实践 91/92 用 slug 形式；`096.md` 是唯一符合 manage-features 文本的文件且行内链接可解析 | P2 | `normalize`（先统一 owner 文本，再决定批量方向） | SDD 修复 | W1 | d1 D1-22 + d3 D3-12（合并；d3 证据翻转 d1 判读） |
| D6-36 | still | 临时生命周期 | `.specify/.tmp` 根：89 文件 / 16M | 无 `<purpose>/` 分组；44×`095-*`、18×`history-*`；7 组重复（6 组含内容、1 组全空）；安全快照 tarball 108K | P2 | `delete`（重复与过期；tarball 留至审计结束） | sanitize | W2 | d1 D1-14 |
| D6-37 | new | 非受管命名 | `.specify/.tmp/s094`（空）、`082-part5`、`repair-078`、`analyze-r3`、`repair-r1`、`history-batches` | ad-hoc 短名 / 无 owner / 无 manifest | P2 | `delete` | sanitize | W2 | d1 D1-15 |
| D6-38 | new | 引用卫生 | 254 个 tracked spec 文件含 `.specify/.tmp` 路径；`095-appendix-check.py` 仅存于 `.tmp` 根（3.5K） | 活 checker 只存在于 scratch；删除 scratch 会使记录的命令不可重放 | P2 | `supersede`（活脚本迁入 `test-evidence/`，旧路径留指针） | SDD 修复 | W1+W2 | d1 D1-13 |
| D6-39 | new | 零字节/空目录 | `.specify/.tmp` 复制树；`.specify/state/runner-log-*` | 3,244 零字节文件 + 943 空目录（复制树内）；state 163 个 0 字节 runner-log（每次运行仍创建） | P2 | `delete`（scratch）/ `repair`（runner 不建空文件） | sanitize + SDD 修复 | W2+W3 | d1 D1-23 |
| D6-40 | still | 详情 stale | `.specify/features/074-goal-team-sdd-unification.md:30`，对照第 6/8 行 | 第 30 行“状态保持 Planned…074b 未实现前不擅自推进”与头部 `Ready for Review` 矛盾；Last Updated 止于 2026-10-29；0 处 2026-11-11 记录 | P2 | `normalize`（追加 dated 记录，不改写 dated 文本） | SDD 修复 | W1 | d2 D2-04 |
| D6-41 | still | 薄记录缺验证 | `specs/001-unify-command-handoffs/`、`006-add-qoder-support/`、`009-claude-code-support/`、`073-record-retention-and-housekeeping/` | 001 只有 plan+requirements；006/009 有 plan/tasks 无 verification；073 只有 requirements；4 个已完成/直实现特性无验证件（历史证据缺口） | P2 | `correct`（注册行加 closure 注记；不回填） | 保持并立政策 | W1 | d2 D2-05 |
| D6-42 | still | 被取代的 live Draft | `specs/012-skill-home-workdir/`、`013-portable-skill-creation/`、`062-humanize-command/` | 012/013 自声明 Feature 013（代表 spec 已是 030）；062 代表已是 080（079 重编号）；三者仍 live、Draft、无 Superseded 标记 | P2 | `archive`（先加取代标记） | sanitize | W1+W2 | d2 D2-06 |
| D6-43 | still | 需求状态字段未治理 | 54/60 `requirements.md` 为 Draft；其中 50 个对应注册行已完成态 | 模板只定义 `Status: Draft`；状态机治理的是 features.md；6 个 spec 自行推进该字段，语义未声明 | P2 | `normalize`（先裁定语义再批量归一） | SDD 修复 | W1 | d2 D2-07 |
| D6-44 | still | 切片关系不可机读 | 14 个目录：012/013/018/024/038/041/042/047/049/062/065a/067/074a/074b | 均为某 Feature 的切片/演化（自声明 Feature ID），但 features.md 单值 Spec Path 列无法表达；无孤儿 spec，缺关系字段 | P2 | `normalize`（增加切片关系列或行内关系句） | SDD 修复 | W1 | d2 D2-08 |
| D6-45 | still | 详情/模式缺口 | `features/` 无 067、065a 详情；`specs/001-*`、`006-*` 的 requirements 无 `**Feature ID**` 行 | 三个可追溯面缺失（067 只在 058 散文、065a 只在 065 行内、001/006 为早期 schema） | P2 | `regenerate`（补详情或显式声明“无详情”） | SDD 修复 | W1 | d2 D2-09 |
| D6-46 | still | 豁免未入册 | `specs/055-conflict-free-stores/requirements.md` | 用户裁定“不走完整 SDD 仪式”写在 spec 内，但 features.md 的 055 行未记录该豁免 | P2 | `correct`（豁免写进注册行） | 保持并立政策 | W1 | d2 D2-10 |
| D6-47 | still | 证据附件无政策 | 72 个根级非标准文件（61 evidence-log、5 machine-artifact、6 authored）；54 个被标准文档引用 | framework map 只列四件标准文档；证据附件承重但无声明式放置/命名政策；移动会打断 54 个引用 | P2 | `keep`（先声明政策；是否迁移待裁） | 保持并立政策 | W1 | d2 D2-11 |
| D6-48 | still | md5 重复（001–074） | 21 组 / 47 个冗余文件；例：`specs/074b-nested-governance/test-evidence/implement-targeted-part{1..4}-failed.txt` | 非空重复均为跨 spec 的 dated evidence 副本；按 non-disposable owner 属允许的日期性重复；债务是体积与检索噪声 | P2 | `keep`（retention 授权后再 dedupe 为指针） | 保持并立政策 | W1 | d2 D2-12 |
| D6-49 | changed | 空输出约定未文档化 | 16 个零字节文件（033、056×5、065a×6、068、071、074a×2） | “空 = 0 failures / 0 errors / 0 names”语义成立（056 verification:35 直接引用）；约定未写入任何 owner；phase4/5/6-current 未被引用 | P2 | `keep`（约定写进证据规范） | 保持并立政策 | W1 | d2 D2-13 |
| D6-50 | still | 损坏相对链接 | `specs/006-add-qoder-support/plan.md:3`、`specs/009-claude-code-support/plan.md:3`、`specs/033-docs-command/tasks.md:86` | 3 处 live 文档坏链（根相对路径在 spec 目录解析为 ENOENT；033 真实文件在 `templates/commands/docs.md`） | P2 | `normalize` | SDD 修复 | W1 | d2 D2-14 |
| D6-51 | still | 超大文件（001–074） | `specs/067-loop-efficiency-hardening/test-evidence/post-test-ids-2026-10-22.txt` 611KB；`baseline-test-ids.txt` 467KB；`specs/052/051 requirements.md` 143KB/128KB | 5 个 >100KB in-scope 文件，集中在测试 node-id 日志与需求正文 | P2 | `keep`（证据保留；需求体积纪律另立） | 保持并立政策 | W1 | d2 D2-15 |
| D6-52 | still | 根级残留与重复（075–099） | `specs/087-*/closure-*.txt`、`088-*/final-failed-r*.txt`、`081-*/tasks-081{a,b,c}.md`、`095-*/observation-appendix.md` | 根文件 323；非标准 73（基线口径 69）；失败/修复日志 41、loose review 28、切片 tasks 3、附录 1；md5 重复 72 组 / 109 副本（0.67 MiB） | P2 | `archive` + `dedupe` | sanitize | W2 | d3 D3-09 |
| D6-53 | changed | 075 旧身份残留 | `specs/075-sdd-loop-efficiency/verification.md:1`、`notes/*`、7 个 `test-evidence/*.jsonl` | 目录与 requirements 已是 075（绑 058），但工件内仍有 5 处 `Feature 063` 与 19 处 `063-sdd-loop-efficiency`（含证据文件名） | P2 | `normalize`（live 工件改 075/058；历史 jsonl 加注） | SDD 修复 | W1 | d3 D3-10 |
| D6-54 | still | 092 编号陷阱残留 | `specs/093-concurrency-by-default/tasks.md:235`；`notes/analyze-repair.md:42` 等 | features.md 已收敛单 092 行，但 093 内 `092-goal-team-parallel` 仍指不存在目录；F-093-019 已登记“不重编号”决定 | P2 | `keep-with-policy`（已登记 dated 决定） | 保持并立政策 | W1 | d3 D3-11 |
| D6-55 | still | 090 快照体量 | `specs/090-re-anchoring/test-evidence/history-{w1..w5}-{before,after}*.json` | 10 个互异 JSON / **15.42 MiB**；单件 gzip ≈0.09 MiB（≈5.6%）；保留 w1-before + w5-after 明文、其余压缩可回收 ≈11.4 MiB | P2 | `archive`（压缩/轮转；参数待裁） | sanitize | W2 | d3 D3-13 |
| D6-56 | still | 超大证据日志（075–099） | `specs/093-*/test-evidence/*suite*.txt`（7）、`095`（3）、`097`（3）、`099`（4）、`094/wp07-closure-suite.out` 等 | 32 件 >200KB 合计 26.23 MiB；多为重复全量套件日志；单件 gzip ≈0.09 MiB | P2 | `keep-with-policy`（final/被 SC 引用者明文；更早压缩） | sanitize | W2 | d3 D3-14 |
| D6-57 | still | 空文件分类未治（075–099） | `specs/078-*/part4-current-failed.txt`；`081-*/closure-verdict.err`；`087-*/closure-*.txt`；`090-*/tmp/tasks-base-failed.txt`；`094-*/repairwave-T079-dryrun.err`；`095-*/review-r2-closure-acceptance.err` | 29 个空文件：21 个应保留（075 夹具 16、088 flag 3、`.gitkeep` 2），8 个是失败运行的空输出 | P2 | `delete`（8 个空输出）/ `keep`（其余） | sanitize | W2 | d3 D3-15 |
| D6-58 | still | 归档内旧路径 | `.specify/archive/spec/**`（123 处 `.specify/specs/`）；`archive/specs/**`（529 处） | 归档工件仍指 live 路径；归档是历史记录，不重写 | P2 | `keep-with-policy`（由台账/摘要承担可解析性） | 保持并立政策 | W1 | d3 D3-16 |
| D6-59 | new | 外部目标依赖 | `.specify/studies/dsh-superagent-prototype-study/target-commit.txt`；`strip-manifest.md:7-12` | 唯一 study 结构合规；target commit 在本仓不可解析，只在外部源仓 `/storage/project/cloud-native-ai/dsh-superagent-prototype` 实测存在 | P2 | `keep-with-policy`（源仓不可得时按 manifest 标 unverified） | 保持并立政策 | W1 | d3 D3-17 |
| D6-60 | new | register 无分诊节奏 | `.specify/register.md` | 229 数据行、168 open-bearing；25 行指归档切片、31 行指已完成特性、72 行指 live、14 行其他 REC 家族、25 行决策/发现 + 1 mixed；无周期分诊步骤 | P2 | `correct`（分桶分诊；逐行 close/supersede/exempt） | SDD 修复 | W1 | d4 D4-07 |
| D6-61 | new | register 权威路径断链 | `.specify/register.md:39`（G1）；`:32`（goal 行） | ① G1 权威路径 `teams/.work/skill-layer-install-separation/S-B/verification.md` 不存在（已清、git-ignored）；② goal 行指向 `.specify/goal/...`，现址为 `.specify/anchoring/...` | P2 | `correct`（G1 改指 tracked team.md + run report；goal 行改指 anchoring） | SDD 修复 | W1 | d4 D4-08 |
| D6-62 | new | 特性归属覆盖不足 | `.specify/memory/feedback/`；`memory/session/*run-determination*` | feedback feature_id 空 **302/464（65%）**；run-determination null **207/435（48%）**；真实缺陷是覆盖，不是错挂（见 §4.2） | P2 | `correct`（引擎侧默认/推断归属；不改写 dated 记录） | SDD 修复 | W3 | d4 D4-09 |
| D6-63 | new | 词汇表提议积压 | `.specify/glossary.md:186` 等 | 180 行：112 proposed（62%）/ 68 confirmed；66 条 proposed 带需求标签；1 条 user 来源核心术语（“机制/策略分离”，083 已实现）仍 proposed；结构校验通过 | P2 | `correct`（按行确认/退役；user 来源交用户裁定） | SDD 修复 | W1 | d4 D4-10 |
| D6-64 | still | tools.md MCP 索引失效 | `.specify/tools.md:30–1998`；`:73` | 65,809 B JSON **不可解析**（第 73 行缺分隔符）；时间戳 2026-02-02、count=2、来源属他机；整文件 68,316 B vs 模板 2,358 B；owner 声明手工维护、无生成器 | P2 | `correct`（按当前 MCP 配置修复，或回退模板 scaffold） | SDD 修复 | W1 | d4 D4-11 |
| D6-65 | still | history 草稿残留 | `.specify/history/.work/` | 125 txt / 5,859,933 B = history store 的 **98.2%**；全部 2026-11-10；owner 声明“可随时删除” | P2 | `delete`（owner 已声明一次性草稿） | sanitize | W2 | d4 D4-12 |
| D6-66 | still | 陈旧产物无消费者 | `.specify/project/`；`.specify/review/master-20260726-205515.md` | 10 文件 / 395,785 B（全部 2026-07-25/26，含 2 张 PNG）；review 1 文件 / 211,414 B；3.5 个月无读取侧；framework-map 已定 legacy read-only | P2 | `archive`（需授权） | sanitize | W2 | d4 D4-13 |
| D6-67 | new | 簿记残留 | `.specify/memory/feedback/index.json.root-stale-20260907` | 5,448 B 陈旧派生索引（文件自标 stale；除报告外 0 引用） | P2 | `archive` | sanitize | W2 | d4 D4-14 |
| D6-68 | new | 报告的语义缺陷 | `.specify/scripts/python/sync-mirrors.py:792-799`（`project_for` :523-566） | projected 行 `: ok` 只表示“投影可计算”，不表示镜像等于投影；漂移时会同屏出现 `DIFF[projected]` 与 `projected[…]: ok`；契约 C-35 只要求点名 kind，测试只钉行格式 | P2 | `correct`（判定改为 `mirror == expected` + 变异腿测试） | SDD 修复 | W1 | d5 D5-03 |
| D6-69 | changed | 零调用脚本 | `scripts/bash/detect-feature-context.sh`、`common-todo.sh`、`implement-plan.sh`、`run-tests-shards.sh`、`scripts/python/skills-utils.py` | **5 个**零调用（基线 4）；`implement-plan.sh:279-284` 调用未定义的 `json_escape`（全仓只有 `json_escape_string`），JSON 模式必失败；`run-tests-shards.sh` 已被 `run-tests.sh -n --dist load` 取代；5 个脚本 11-09/10 仍被 089 守卫改过（死而维护） | P2 | `archive`（先授权；若保留则先修 `json_escape`） | sanitize | W1+W2 | d5 D5-04 |
| D6-70 | still | 单文件超大行 | `.specify/features.md` | 241,145 B；92 数据行 ↔ 92 详情文件（零孤儿）；第 60 行（Feature 051）**14,097 字符**，另有 4 行 >7,000；合并冲突与 token 热点 | P2 | `correct`（行体收敛为一行指针；不改单文件形态） | SDD 修复 | W1 | d5 D5-06 |
| D6-71 | still | 安装基线陈旧 | `.specify/source.json` | `commit=b3da3a2`，落后 HEAD **240** 提交；`stamped_at=20261110T055525Z` | P2 | `correct`（经 `specify init`/迁移重盖章） | SDD 修复 | W1 | d5 D5-07 |
| D6-72 | still | 被跟踪的旧备份 | `.specify/agents/.backups/qoder/*.md` | 15 份 / 68KB，全部被跟踪且全部与当前模板 DIFFERS（旧渲染快照）；版本历史已承担备份职责 | P2 | `archive`（授权后；源侧补 ignore 规则） | sanitize | W2 | d5 D5-08 |
| D6-73 | still | 共享追加式存储（并发热点） | 5 个 `teams/*/items.jsonl` + 3 个 `teams/*/run-log.jsonl` | 8 个被跟踪 jsonl（7 队）；`viz-skill-arena/items.jsonl` 0 B；与 AGENTS「记录类数据一文一件」MUST 冲突 | P2（MUST 级违例，当前休眠、爆炸半径低） | `supersede`（create-team 改逐条文件/派生索引；旧文件归档） | SDD 修复 + sanitize | W1+W2 | d5 D5-09 |
| D6-74 | still | 团队无可用 goal | 4 队无 `goal_slug`（cws-workspace-cluster、draw-plantuml-optimizer、requirement-implement-monitor、summarize-project-optimizer）+ 2 队悬空（demo-seat-dispatch、viz-skill-arena→visualization-skill-selection） | `goal-utils.py run-checks` 对 6 队一致 `no-goal-definition`；6 队全部无法通过运行前置 | P2 | `correct`（`/speckit.goal migrate`）或 `archive`（休眠队退役） | `/speckit.goal` + `/speckit.team` | W1 | d5 D5-10 |
| D6-75 | new | 终态 goal 的壳团队 | `teams/{087-arch-diagram-docs,draw-two-layer-structure,post-refactor-mechanism-integrity,session-driven-self-improvement,skill-layer-install-separation}/team.md` | 5 队对应 goal `achieved`；`run-checks` 判 `goal-terminal` 且 `blocked=true`，团队定义仍在活跃层 | P2 | `archive` 或 `exempt`（理由 + 到期条件） | `/speckit.team` | W1 | d5 D5-11 |
| D6-76 | new | 团队元数据非法 YAML | `.specify/teams/command-logic-as-classified-skills/team.md:74`；`viz-skill-arena/team.md:3` | 两文件 frontmatter 过不了严格 YAML 解析（PyYAML 实测失败）；行扫描式读取器掩盖缺陷 | P2 | `correct`（引号化 / 修流映射） | SDD 修复 | W1 | d5 D5-12 |
| D6-77 | still | 团队定义旧锚 | 090/091/094 三处 archive-tree 锚 + 6 处 `.specify/goal/…` 权威行；共 12 文件 / 36 行 | 活定义在 `.specify/anchoring/<slug>/goal.md`；团队文件仍宣告已不存在的 `.specify/goal/` 或归档树 | P2 | `correct`（指向 anchoring） | SDD 修复 | W1 | d5 D5-13 |
| D6-78 | new | 无消费者的模板 | `.specify/templates/gate-template.yaml`（源 `templates/gate-template.yaml`） | 命令/技能/脚本/src 均 0 引用；唯一提及是历史 Feature 039；活载体是 `.specify/gate.yaml` | P2 | `correct`/`supersede`（接引用或退役） | SDD 修复 | W3 | d5 D5-14 |
| D6-79 | new | 空层与 root 属主 | `.specify/agents/execution/scripts/`（空、root 属主）、`.specify/agents/execution/logs/`（空、root 属主） | framework-map 声明 execution 层含 tracked `configs/` + `scripts/`；实际 scripts 为空（文档称 optional）；两目录 agent 用户不可写；`.tmp` 内 520 个 root 属主条目 | P2 | `correct`（确认 optional 后保留或删层；`chown` 恢复可写） | sanitize / 机制修复 | W3 | d5 D5-15 |
| D6-80 | new | workflow 观察块陈旧 | `.specify/workflow/git.md`（`GIT_OBSERVED_START` 块） | 观察时间 2026-11-10T02:33:38Z，记“1 个非声明分支 `rename-anchors`”；当前本地分支 `master`/`main`/`100-seal-slice-archive`，`rename-anchors` 已不存在 | P2 | `correct`（经 git-utils scope A 重新观察） | git-utils | W1 | d5 D5-16 |
| D6-81 | new | 指令备份残留 | `.specify/instructions.md-*`（7 份） | 252KB：2026-07-11 1 份 + 2026-11-10 6 份；全被 `.specify/.gitignore` 忽略；最新一份与当前文件同尺寸 | P2 | `delete`（保留策略由用户定 0 或 1 份） | sanitize | W2 | d5 D5-17 |
| D6-82 | new | 生成事实与本机不符 | `.specify/instructions.md:254` | 生成物写 `Root Path: /Users/liuqiming.lqm/...`；本仓实际根为 `/storage/project/cloud-native-ai/spec-kit` | P2 | `correct`（本机重渲染，或声明跨主机事实） | SDD 修复 | W1 | d5 D5-18 |
| D6-83 | still | goal/team slug 分歧 | `teams/088-reporting-dogfood/team.md`、`089-script-interface-contract/team.md`、`viz-skill-arena/team.md` | 3 处 goal_slug ≠ team slug；088/089 像有意命名，viz 目标档案缺失（并入 D6-74） | P2 | `correct`（有意分歧写成显式声明） | `/speckit.team` | W1 | d5 D5-19 |

### 1.4 已消解（resolved）

| ID | 状态 | 类别 | 证据 | 事实 | 严重度 | 处置 | lane | 来源 |
|---|---|---|---|---|---|---|---|---|
| D6-84 | resolved | 镜像漂移 | `.specify/templates/gitignore-specify-template` | d5 读数时缺 `state/` 块、`sync-mirrors --check` exit=2；**综合复核：`c3997b182` 已补 4 行，源与镜像 byte-identical，`--check` exit=0** | — | 已完成（无需动作） | 机制修复 | d5 D5-01 |
| D6-85 | resolved | 审计载体 | `.specify/.tmp/binding-base/`（d1 读数 177M / 10,032 文件） | **综合复核：worktree 已移除**（`git worktree list` 仅主仓 + 100）；`.tmp` 824M→650M | — | 已完成 | 审计 harness owner | d1 D1-11 |
| D6-86 | resolved | 脏工作树 | 工作树；分支 | d1 读数时 9 项脏、分支 `debt-audit-harness-binding`；**综合复核：master / `c3997b182`，工作树 2 项（trigger 时间戳 + 本审计目录）** | — | 已完成（trigger 变动属引擎状态） | 审计 harness owner | d1 D1-24 |

### 1.5 健康项（不列债）

- d1：state/.tmp 均被 ignore、零跟踪（`git check-ignore` 全命中）；quarantine 无独有 git 提交；worktree 100 是已注册活跃载体。P0 数据丢失风险：无。
- d2：无孤儿 spec；54 个根级附件被标准文档引用（承重证据）；56 verification 的第 35 行把零字节证据读作“0 failures”的语义合法。
- d3：24/24 spec 四件套齐备；096–099 verification+review 齐备；features.md 92 行 = 头部 `Total Features`；archive 台账覆盖 11 目录；studies 结构合规；无断裂符号链接。
- d4：session 454 条一文一件、`(run_id, unit_id)` 重复 0、全文哈希重复 0；`records.jsonl`/`scores.jsonl` 为 owner 声明的只读 legacy 回退；`last-regression-failed.txt` 经复核被测试引用，核销。
- d5：`.render-manifest.json` 88 条 = 22 agent × 4 宿主，sha256 全匹配；`regen-command-copies --check` exit=0（31⇄31）；`goal-utils validate` 14/14；`doc-consistency-check --faces duplicate` 对 75 个 shared 文件 pass。

---

## 2. 分波治理方案（机制先修 → 数据回收 → 结构收敛）

> 原则：每波独立确认门，前一波不绿不启动下一波；W2 只要一次前置批量授权；不新建扫描器 / 债务注册表 / 保留规则引擎——W2 全部走既有 `sanitize-utils.py` 与 retention lane，W1/W3 走 SDD 修复。

### W1 — 机制修复（SDD lane；可逆编辑，无删除）

**范围**：登记表中波次含 W1 的全部条目（D6-01…D6-06、D6-12…D6-19、D6-21、D6-22…D6-28、D6-29…D6-31、D6-35、D6-38、D6-40…D6-46、D6-48…D6-51、D6-58、D6-60…D6-61、D6-63…D6-64、D6-68、D6-70、D6-71、D6-73…D6-78、D6-80、D6-82、D6-83）的机制部分，以登记表的波次列为准。

**关键动作组**：
1. **状态真实性**：close-out 作为一步执行——脊置终态 + 行注册表 `closed` + `features.md` 行同步 + lease 清空；修 100 loop-state；清理/归档 074/074b/081/086/092/093/094 过时脊；移除 101 悬空 `spine_path`。
2. **守卫修复**：`test_spec_feature_binding_integrity.py` 改整行 schema 校验（裸 `\|`/缺闭合即失败，禁止静默跳过），修 086/088/089/090 四行与 048/092 两路径；建立“红守卫写入基线必须带登记行”规则。
3. **注册表**：补 075/080/097/098/100 行或父详情指针；裁定 048/092 路径形态；069 父状态；096.md 命名（先统一 owner 文本）。
4. **政策落盘**：state 内容类（framework-map/directory-governance）；review 两文件根模型 + `review-archive/`；checkpoint closure 校验/豁免字段；test-evidence 保留参数；根级证据附件政策。
5. **记录通道**：feedback 分诊 464 条 + backlog 166 open-bearing 按证据收口；retention 首个非空 plan 与 receipts；exec-quant 接传感器或登记带到期 `exempt`；register 分桶分诊 + 两处断链；glossary 按行确认；tools.md MCP 修复。
6. **文档与工具面**：instructions 压缩至 ≥1,024 B 余量（或 raise 记录）；本机根路径修正；source.json 重盖章；sync-mirrors projected 判定 + 变异腿测试；零调用脚本裁决；团队/goal YAML、旧锚、slug 声明；workflow 观察块重观察；features.md 行体收敛。
7. **旧锚归一**：001–074 规范性文档 443 处与 075–099 live canonical 367 处按确定性映射分批修，日期性证据叙述进 allowlist；以只读链接检查器作完成门。

**确认门**：SDD 流程自身的 plan → review 门；注册表逐行 diff 呈现（治理保留清单）；外发/打包动作需用户显式授权；框架文档修改走 SDD。

**可度量结果**：binding 两测试绿（2 failed → 0）；不可解析行 0；脊/注册表/features 矛盾 0（D1 §1.5 的 14 行矛盾/悬空全部收口）；缺行 0（或逐行声明）；`count_since_submission 464 → 0`；open-bearing backlog `166 → 0 或逐行 exempt`；retention receipts > 0；register 断链 `2 → 0`；`instructions ≤ 37,376 B` 或 raise 记录落盘；`source.json` 落后 0；sync 检查保持 exit=0。

**中止条件**：某线实际仍在运行 → 停在异常点并报告；任一行的正确代表 spec 无法从自声明 + 状态唯一确定 → 交裁决；外发授权缺失 → 只做本地分诊；owner 文档互相冲突 → 升级裁定，不擅自统一；压缩引入语义丢失 → 停。

### W2 — 数据回收（`/speckit.sanitize` lane；破坏性门：一次前置批量确认）

**范围（按当前读数）**：

| 目标 | 体量 | 动作 |
|---|---|---|
| `.tmp/quarantine-098` | 274M / 17,216 文件 | delete（无 manifest；含 `.git` 但 HEAD 主仓可达） |
| `.tmp/script-interface-*`（10 目录） | ≈135M / 19,197 文件 | delete（先解决 520 个 root 属主条目） |
| `.tmp/sdd-loop/forks`（56） | 73M / 551 文件 | delete |
| `.tmp` 根散文件 + 短名目录 | ≈16M + ≈3M | delete（保留安全 tarball 至审计结束） |
| `.tmp/sdd-loop/tmp` 关闭线残留 | ≈1M | delete |
| `state/` 095–099 per-run 产物 | 251M / 1,068 文件 | 按保留参数：receipt 回收（推荐）或 archive |
| `state/` 孤儿 pid / sentinel / attempt 备份 | 随 per-run | delete |
| `history/.work` | 5.86MB / 125 文件 | delete（owner 声明可删） |
| `project/` + `review/` | 0.58MB / 11 文件 | archive |
| `specs/090` 快照 | 15.42 MiB → ≈4 MiB | 压缩/轮转 |
| 32 件 >200KB 证据日志 | 26.23 MiB 的大部分 | 压缩（final/被 SC 引用者明文） |
| 109 个重复副本 + 8 个空输出 | 0.67 MiB / 117 文件 | dedupe / delete |
| pyc | 137 个 / 9.68MB | delete |
| 指令备份 / `.backups` / 残留索引 | 252KB + 68KB + 5KB | delete / archive |

**确认门**：`/speckit.sanitize` dry-run 计划 + 用户对 §3 Q1 的一次性授权；archive-not-delete 为缺省；任何被 live 文档引用的文件先改写引用再移动。

**可度量结果**：`.tmp 650M → ≤ ~165M`、文件数 ≈47k → ≤ ~11k；state 272M → ≤ ~20M（脊 + 活跃线 + 30 天窗口）；reclaimed ≥ ~500M（.tmp）+ ≥ ~250M（state，待参数）；`.work 98.2% → 0`；pyc 0；8 个 tracked jsonl 退出跟踪面。

**中止条件**：任一目标含不可达 git 对象或被活跃证据引用 → 跳过该项；root 属主阻挡 → 上报并等待授权；删除会打断未改写的引用 → 中止该批；plan 为空 → 不 apply。

### W3 — 结构收敛（SDD lane）

**范围**：D6-07、D6-08、D6-10、D6-20、D6-32、D6-39、D6-62、D6-78、D6-79 的结构面，以及 W1 政策落地后的周期性验证。

**关键动作**：framework-map / directory-governance 声明 state 内容类与 `.tmp` 子根；`script-interface-check.py` 启动时清扫 >24h 残留沙箱；runner 停止创建 0 字节日志；close-out 守卫固化；state 30 天保留窗口 + receipt；create-team 逐条文件存储（并发测试：两分支同队不同路径）；`gate-template.yaml` 取舍；execution 空层与属主收敛；归属推断默认（feedback/run-determination）。

**确认门**：框架编辑走 SDD + 契约测试；不新增 store / 登记册。

**可度量结果**：连续两条线后同类债不复发（close-out 矛盾、script-interface 残留、0 字节日志各 0 复发）；0 个“无文档含义”目录；0 个 RfR spec 缺当前 `review.md`；live canonical 工件 0 悬空 `.specify/memory/*`；feedback 归属缺失 `65% → <5%`、run-determination null `48% → <5%`（新条目口径）。

**中止条件**：owner 文档冲突 → 升级裁定；需要改写 dated 历史记录 → 停止；归属推断需读取未授权数据 → 保持 null。

---

## 3. 待用户裁决点（封闭问题，本席未自答）

| # | 问题 | 选项 | 建议 | 阻塞波 |
|---|---|---|---|---|
| Q1 | **W2 批量回收授权**：是否批准删除/归档上表过期 scratch 与按参数回收 state 记录？ | (A) 批准（dry-run 先行） / (B) 仅压缩与搬移不删除 / (C) 不授权 | A | W2 |
| Q2 | **反馈外发**：464 条积压如何记账？ | (A) `package` 产包并人工外发 / (B) 仅 `mark-submitted` 本地复位 / (C) 只做条目分诊 | 有外发通道选 A；否则 B（两者都把计数复位） | W1 |
| Q3 | **state 保留方式**：per-run 产物被引用时？ | (A) `archive` 迁入 tracked（git +251M） / (B) retention receipt 回收（推荐） | B | W3 |
| Q4 | **state 保留参数**：线终态后 30 天回收是否采用？ | (A) 采用 / (B) 改用其他窗口 | A | W3 |
| Q5 | **test-evidence 保留参数**：090 快照与 >200KB 日志？ | (A) 最新 baseline+final 明文、更早压缩、30 天宽限 / (B) 每 spec 明文上限 5 MiB / (C) 只压缩不设上限 | A | W2 |
| Q6 | **history/.work**：125 个草稿何时删？ | (A) 立即 / (B) 下一次 history 运行后统一删 | A | W2 |
| Q7 | **project/review 陈旧产物**： | (A) 归档并留指针 / (B) 声明为历史证据（exempt + 复核日） | A | W2 |
| Q8 | **行 048/092 路径形态**： | (A) 改指 `archive/specs/…`（可解析） / (B) 置 `-` + 台账指针 | A | W1 |
| Q9 | **补齐缺行模型**：075/080/097/098/100？ | (A) 各补一行挂父特性 / (B) 只写父特性详情 + 指针 | A | W1 |
| Q10 | **详情命名**：`096.md` 与 91 个 slug 形式？ | (A) 以实践为准（owner 文本改 `<ID>-<slug>.md`，重命名 096.md） / (B) 以 owner 文本为准（91 个改为 `<ID>.md`） | A（并修 sanitize owner 文本） | W1 |
| Q11 | **069 父 spec**： | (A) 保留 live 索引并标注 Draft/归档切片 / (B) 另选代表并改行 069 | A | W1 |
| Q12 | **需求 Status 字段**： | (A) 冻结于撰写（注册行权威） / (B) 跟随 Feature 批量推进 50 个 | A | W1 |
| Q13 | **被取代 live Draft 012/013/062**： | (A) 加 Superseded 标记后归档 / (B) 保留 live 并标记 | A | W1+W2 |
| Q14 | **零调用脚本（5 个）**： | (A) archive（可逆） / (B) 保留 + 补文档 + 修 `json_escape` | A | W1+W2 |
| Q15 | **团队治理**：6 无 goal 队 + 5 壳队？ | (A) 有运行的 migrate、休眠的 archive / (B) 全部 migrate / (C) 全部 archive | A | W1 |
| Q16 | **instructions 预算**： | (A) 压缩至 ≥1,024 B 余量 / (B) 调高预算（按 owner 规则给出仍 ≥1,024 B 余量的值） | A | W1 |
| Q17 | **source.json**： | (A) 现在经 `specify init`/迁移刷新 / (B) 等下一次窗口 | A | W1 |
| Q18 | **tools.md MCP 索引**： | (A) 用当前 MCP 配置修复 / (B) 回退为模板 scaffold / (C) exempt 并标“仅供参考” | A（无配置则 B） | W1 |
| Q19 | **gate-template.yaml**： | (A) 接上流程引用 / (B) 退役 | B | W3 |
| Q20 | **c7 红钉**： | (A) 立即完成 053 重锚裁定 / (B) exempt 至 2026-12-11 并保持红可见 | A | W1 |
| Q21 | **098 记录缺口**： | (A) 只登记 OI + 对账注记 / (B) 从现有 state/test-evidence 派生可验证记录 | A（不伪造时间戳） | W1 |
| Q22 | **review 权威政策**：是否采用“根级只保留 `review.md` + `code-review.md`，其余入 `review-archive/`”？ | (A) 采用 / (B) 保留根级 + `Superseded-by` 头 | A | W1 |
| Q23 | **根属主清理**：520 个 `.tmp` root 属主条目与 2 个 execution 目录需 root/授权处置 | (A) 提供 root 处置窗口 / (B) 保持现状并登记 | A | W2 |
| Q24 | **W1 是否现在启动**：是否立即发起 SDD 修复批次？ | (A) 是 / (B) 先做别的 | A | — |

---

## 4. 差异对比专章（vs general-purpose 盘点轮）

**对照对象**：2026-11-11 上午第二次盘点，6 个 general-purpose 代理，master 读数（下称 R1）。**判定词汇**：`一致` = R1 读数成立；`精化` = 成立但读数/口径被修正；`新增` = 域报告新发现；`被推翻` = 前提不成立（给证据）。

### 4.1 state / .tmp 组

| R1 基线项 | R1 读数 | 第二轮实测 | 判定 | 来源 |
|---|---|---|---|---|
| state 体量 | 261MB / 1,141 文件 | T0 263M / 1,178 → T1 268M → T2 272M / 1,189；+37 文件来自审计 raw 与 100 线推进 | **精化**（移动靶） | d1 B1 |
| raw | 314 份 / 199MB | 095–100 闭环集合仍 **314 份**；总数 326（+12 审计/coaching） | **精化**（闭环集合一致，总数变化） | d1 §1.1 |
| log | 157 份 / 60MB | `log-*` **163 / 61M**；另有 runner-log 163 / **全 0 字节**、heartbeat 163 / 652K | **精化** | d1 B3 |
| spine 与 registry 矛盾 | 095 active/closed；096–099 running/closed；074 running/stalled；074b running/closed；081/086/092/093/094 running 无 registry | **全部成立**；新增 093 脊自相矛盾、100 脊内 stage 矛盾、101 `spine_path` 悬空；前提纠正：基线所谓 registry 经复核为**环境级行注册表**（`~/.local/state/spec-kit/lines/`），与 `features.md` 是两个注册表 | **一致 + 新增** | d1 §1.5 |
| 死 pid | 156 | T1 163 个 157 死 / 6 活；T2 164 个全死（6 活即审计自身与 100 analyze） | **精化** | d1 B6 / T2 复核 |
| sentinel=0 | 4 | 4 个（3 规范 + 1 `.bak`），所属线已 closed | **一致**（精确化） | d1 B7 |
| quarantine-098 | 274MB 无 manifest | 274M / 17,216 文件；无 manifest；**新增**：wp7 含 `.git`（HEAD 主仓可达，无独有提交）、含 11-11 文件晚于关闭 | **一致 + 新增** | d1 B14 |
| script-interface-* | 9 目录 / 129MB | d1：9 / 129M / 19,174；T2：10 / ≈135M / 19,197；**新增根因**：中止的 checker 不清理（`finally` 只覆盖正常退出）+ **520 个 root 属主条目阻断清理** + 审计期间新沙箱曾达 2.7GB（缩至 312KB） | **精化 + 新增** | d1 B15 + d5 D5-05/ANOMALY |
| forks | 56 / 73MB | 56 目录 / 551 文件 / 73M，全为 11-10，无 git | **一致** | d1 B16 |
| 根散文件 | 89 / 16MB | 89 / 16M；7 组重复（6 组含内容）；含安全快照 tarball 108K | **一致 + 新增** | d1 B17 |
| 101 残留 prompt | 有 | `.tmp/sdd-loop/tmp/101-debt-governor-agent/prompt-requirements.md` 12K；**新增**：注册表 101 条 `spine_path` 指向从未存在的脊 | **一致 + 新增** | d1 B18 / D1-21 |

### 4.2 specs 001–074 组（d2）

| R1 基线项 | 第二轮实测 | 判定 | 来源 |
|---|---|---|---|
| 缺 verification 9 | 计数精确成立（001/006/009/012/013/055/065/069/073）；处置分四类：已完成直实现的证据缺口、被 030 代表取代、055 用户裁定轻量、065 未到阶段、069 验证在归档切片 | **一致 + 精化** | d2 B1 |
| 缺 tasks 5 | 精确成立（001/055/065/069/073） | **一致** | d2 B2 |
| 空文件 16 | 计数成立，**判读翻转**：16 个全部是“空输出”语义（空=0 failures，056 verification:35 直接引用）；无数据损坏，债务是约定未文档化 | **一致 + 精化** | d2 B3 |
| md5 重复 21 组 | 21 组成立；47 个冗余 in-scope 文件；全 specs 树 93 组；非空重复均为跨 spec dated evidence | **一致 + 精化** | d2 B5 |
| 旧锚 680 处 / 277 文件 | 全量提及 3,040 / 400；dangling 935 / 329；**排除 074 三目录后 685 / 289**（最接近基线 +5/+12）；规范性文档子集 443 / 182 | **精化**（基线读的是 dangling 子集） | d2 B6 |
| 069a/069b archive + 注册表指 live Draft | 成立；`features/069-*.md:119` 记 2026-11-09 consolidation；父 spec 只有 requirements.md 且 Status=Draft | **一致** | d2 B7 |
| 注册表漂移 | **部分前提翻转**：006/009/012/013/065a/067 是双命名空间/自声明设计，非数据损坏；真缺陷另列：048 行坏指针（P1）、14 个切片目录无机器可读关系（P2）、50 个 Draft/状态矛盾（P2） | **精化（含被推翻子项）** | d2 B8 |
| 074a/074b 待归档 | 合并已应用（`merge-manifest.json`，seal-utils 0.0.22，`merge=merged`，slices `pending-review`，提交 `8460536ca`）；074a 32/32、074b 26/26、父 58/58 全 `[X]`；归档未发生 | **一致 + 精化** | d2 B9 |

### 4.3 specs 075–099 组（d3）

| R1 基线项 | 第二轮实测 | 判定 | 来源 |
|---|---|---|---|
| 64.7MB | 磁盘 64.66 MiB（67,805,184 B）；apparent 58.40 MiB | **一致**（口径=du MiB） | d3 #1 |
| >200KB 32 件 | 32 件 / 26.23 MiB；31 在 `test-evidence/`、1 在 `notes/`（098 pre-change 966,830 B） | **一致** | d3 #3 |
| md5 重复 72 组 / 109 冗余 | 成立；浪费仅 0.67 MiB——**件数问题，不是空间问题** | **一致 + 精化** | d3 #4 |
| 旧锚 30,739（090 快照 25,349） | **逐字复现**：全区间 30,739；090 `history-*.json` 25,349；其余 spec 4,339 | **一致** | d3 #7 |
| 097/098 无注册行与详情 | 成立，并扩展：075/080 同缺；100 亦缺行（d1） | **一致（扩展）** | d3 #10 + d1 D1-12 |
| 096 详情名与 slug 不符 | **被推翻**：owner 文本（`manage-features/SKILL.md:29`、`framework-map.md:9`）声明 `<ID>.md`；`096.md` 是**唯一符合 owner 文本**的文件；91/92 个 `<ID>-<slug>.md` 才是实践偏离；且 sanitize layout lane 的 owner 文本与实践一致、与另两名 owner 冲突 | **被推翻**（前提翻转 + owner 冲突） | d3 D3-12 |
| 075/080 同缺 | 成立：两目录 live、无行、无详情；Feature ID 分别绑 058/062 | **一致** | d3 #12 |
| archive 两套命名 | 成立：`archive/spec/` 8 目录 0.52 MiB 无本地台账；`archive/specs/` 11 目录 + 台账 2.55 MiB；后者在 framework-map / skills / templates / src **0 引用** | **一致 + 新增**（目录治理违例） | d3 D3-08 |

### 4.4 memory 组（d4）

| R1 基线项 | 第二轮实测 | 判定 | 来源 |
|---|---|---|---|
| session 454 / 3.6MB；95% run-determination；单 run 最多 16 | 454 / 内容 2,903,172 B；run-determination 435/454 = **95.8%**；单 run 最多 **11**（16 不可复现）；269 个 run_id；`(run_id, unit_id)` 重复 0、全文哈希重复 0 | **精化 + 被推翻（16）** | d4 B1 |
| feedback 464 积压 | 确认：`count_since_submission=464`、threshold=10、46.4×、2026-10-08 后 34 天未外发、129 条空处置、`packages/` 不存在 | **一致** | d4 B2 |
| exec-quant 357 | 确认 357 + 2 scores；**新增**：357/357 `quality` 五键全 `not_evaluated`，0 条 token 键 | **一致 + 新增** | d4 B3/D4-04 |
| retention 空转 696/0/696 | 空转成立；**696 不可逐字复现**：当前 1,270 总数 / 0 eligible / 1,270 blocked；11-05 快照约 728；唯一 plan `confirmed=false`、items=[] | **精化（读数不可复现）** | d4 B4 |
| history/.work 5.9MB | 125 txt / 5,859,933 B = history 的 98.2%；全部 11-10；owner 声明可删 | **一致** | d4 B5 |
| register 168 open | 167 字面 open + 1 `mixed` = 168 open-bearing；2 处路径缺陷成立 | **一致** | d4 B6 |
| project/+review/ 无消费者 | 10 文件 / 395,785 B（7 月）+ 1 文件 / 211,414 B（7 月）；3.5 个月无读取侧 | **一致** | d4 B7 |
| tools.md MCP 快照 2026-02-02 | 确认；**新增**：65,809 B JSON 在第 73 行不可解析；整文件 68,316 B vs 模板 2,358 B | **一致 + 新增** | d4 B8/D4-11 |
| 098 memory 证据链缺失 | 确认：run-determination / exec-quant / knowledge / feedback 均 0；对照 261 个 state 文件、117 个 test-evidence、合并 `48e273d73` | **一致** | d4 B9 |
| feature_id 错挂 8 例（097→024、083→082） | **被推翻**：机械扫描 36 处表面不一致，逐条核对权威 `Related Feature` 后 **0 处真实错挂**（097→024 是声明的子规格；066→065 是归档切片声明；079/080→062 是重编号前声明；063/075→058；083→082 是 dated 记录）。真实缺陷是归属覆盖：feedback 65% 空、run-determination 48% null | **被推翻**（真实缺陷转为 D6-62） | d4 B10/D4-09 |

### 4.5 scripts / 根层组（d5）

| R1 基线项 | 第二轮实测 | 判定 | 来源 |
|---|---|---|---|
| sync-mirrors exit=2；gitignore 模板缺 `state/` 块（注明已由 harness 绑定提交修复，请复核） | **复核：已修复**。d5 读数时确有 1 处 DIFF；`c3997b182` 的合并内容包含 `.specify/templates/gitignore-specify-template` +4 行；T2 实测源/镜像 byte-identical、`--check` **exit=0**、`--only scripts` exit=0 | **一致（当时）+ 现已 resolved** | d5 B1 + §0.3 |
| 4 个死脚本 | **修正为 5 个零调用**：`detect-feature-context.sh`、`skills-utils.py`、`common-todo.sh`、`implement-plan.sh`、`run-tests-shards.sh`；`implement-plan.sh` 调用未定义的 `json_escape`；5 个脚本死而维护（089 守卫仍在改） | **精化（4→5）** | d5 B3/D5-04 |
| pyc 131 / 9.6MB | **137 / 9.68MB**（.tmp 内 119、非 .tmp 18）；审计自身的只读引擎会新增 pyc，是移动靶 | **精化** | d5 B4 |
| features.md 241KB / 125 行 / 最长 14,097 | **精确成立**；第 60 行（051）14,097 字符；另有 4 行 >7,000；92 数据行 ↔ 92 详情文件，双向零孤儿 | **一致 + 新增（行级）** | d5 B5 |
| instructions 38,301B（余 99B） | 确认；预算 38,400；超限仅告警（恒 exit 0）；**新增**：根路径写的是 `/Users/liuqiming.lqm/...`，本机为 `/storage/...` | **一致 + 新增** | d5 B6/D5-18 |
| source.json 落后 240 提交 | 确认：stamp `b3da3a2`（11-10 13:42 +0800），240 = 11-10 188 + 11-11 52 | **一致** | d5 B7 |
| 渲染一致 | 确认：manifest 88/88 sha256 全匹配；regen 31⇄31 exit=0；skills **18 external / 40 internal**（基线 39，099 的 seal-artifact 已计入） | **一致 + 精化（39→40）** | d5 B8/B9 |
| `.backups` 15 份被跟踪 | 确认：15 个 `.md` / 68KB，全部 DIFFERS 于当前模板 | **一致** | d5 B11 |
| 8 个受跟踪 jsonl（7 队） | 确认；`viz-skill-arena/items.jsonl` 0 B；与「记录类数据一文一件」MUST 冲突（休眠队、爆炸半径低） | **一致 + 新增（规则定性）** | d5 B12/D5-09 |
| 4 队无 goal、2 goal_slug 无档案 | 确认 + 扩展：`run-checks` 对 6 队一致 `no-goal-definition`；**新增** 5 个 achieved-goal 壳团队（`goal-terminal` 且 blocked） | **一致 + 新增** | d5 B13/D5-11 |
| 3 处名称漂移 | 确认（088-reporting-dogfood→088-speckit-visualization；089-script-interface-contract→script-interface-contract；viz-skill-arena→visualization-skill-selection） | **一致** | d5 B14 |
| shared 1 条重复行 | **未复现为缺陷**：`doc-consistency-check --faces duplicate` 对 75 个 shared 文件判 pass、0 findings；唯一重复正文行是 clarify-taxonomy 的 3 个 Mode 模板行 | **被推翻（unverified，不立债）** | d5 B16 |

### 4.6 两轮方法差异

| 维度 | R1（general-purpose ×6） | R2（debt-governor ×5 域 + D6 综合） |
|---|---|---|
| **证据密度** | 汇总级读数：数量、体量、断言；未逐条附测量命令与口径 | 每条发现 = 路径 + 实测数值 + 测量工具；双时点（d1 T0/T1）、双口径（d3 du vs apparent）、引擎退出码表（d5）；同路径冲突逐条裁决 |
| **前提修正数** | 摘要未披露；结论以读数呈现 | **15 处**判读纠正：d1 3（分支/增长窗/registry 双义）、d2 3（空文件语义/142 不可复现/漂移再判读）、d3 1（096 命名翻转）、d4 4（错挂证伪/097 记录存在/probe-map 存活/16→11）、d5 4（4→5 死脚本/131→137 pyc/39→40 skills/重复行不成立）；另 2 处“读数不可逐字复现”（retention 696、残名 142） |
| **域划分** | 6 个 general-purpose 代理，按任务分组 | 5 个**互斥读域**（state+tmp；specs 001–074；specs 075–099+studies+archive；memory/history/register；scripts/templates/skills/agents/teams/anchoring/shared/根文件），统一处置词表与证据纪律；第 6 席做综合与冲突裁决（本报告） |
| **异常披露** | 摘要未附异常行 | 结构化 `ANOMALY` 行：d1 ×3（分支不符、读数迁移、098 关闭后仍在工作）、d4 ×1（B10 证伪）、d5 ×1（沙箱泄漏 + root 属主）；d2/d3 明示“无异常”并披露途中判读纠正；d5 另披露一次自行清理（其 2.7GB 沙箱→312KB，余下 root 属主不可删） |
| **读数分支** | master | 审计分支 `debt-audit-harness-binding`（HEAD `733ac70e8`，d1 异常#1），**现已合并入 master `c3997b182`**；该合并同时修复了 D5-01，故 R2 窗口内出现了“自己的发现被同窗修复”的现象 |
| **可执行性** | 清单式结论 | 每条债项带处置、lane、波次；每波带可度量结果与中止条件；24 个封闭裁决点 |

### 4.7 同路径冲突与合并记录

| 路径 | 冲突 | 裁决 | 依据 |
|---|---|---|---|
| `.specify/templates/gitignore-specify-template` | d5：缺 `state/` 块（exit=2）；T2 实测全绿 | **resolved**（D6-84） | `c3997b182` 合并内容 + `sync-mirrors.py --check` exit=0 + `diff -q` IDENTICAL |
| `.specify/features/096.md` | d1：非规范命名；d3：owner 文本与实践相反、两名 owner 冲突 | 采信 d3（D6-35），d1 原判读作废但保留来源 | `manage-features/SKILL.md:29` + `framework-map.md:9` vs `sanitize-materials/SKILL.md:375-378` |
| `.specify/.tmp/script-interface-*` | d1：9 目录 / 129M；d5：第 10 个沙箱 + root 属主 + 根因 | 合并（D6-10），两时点读数并列 | d1 §1.2 + d5 §2/§5 |
| `.specify/features.md` 缺行 | d1：097/098/100；d3：075/080/097/098 | 合并（D6-12），取并集 5 个 live spec | d1 D1-12 + d3 #10/D3-02 |

---

## 5. 覆盖与缺口

### 5.1 五域覆盖声明与未评估项

| 域 | 覆盖（已声明） | 显式未评估 |
|---|---|---|
| d1 | `state/` 两棵根的存在性、计数、体量、ignore/tracking 一致性、线分布、pid/status/sentinel、行注册表、脊×注册表×features 三处对读 | raw 转录语义；复制树内 mtime≠创建时间；57k 文件全量 hash 分组（仅小集合）；`/proc` 存在性≠进程身份；095 suite 噪声未重跑（引用自 verification） |
| d2 | specs 001–074 共 60 目录的全文档集、根级非标准文件、空文件、md5、旧锚、注册表行、切片关系、链接、体量 | 基线“142 残名”不可逐字复现（现测 143，备选口径 141）；无其它未验证项 |
| d3 | specs 075–099、studies、archive；24/24 四件套健康项；review 族、checkpoint、证据体量、archive 双根、旧锚 | study target 只在外部队列源仓可验证；archive 内旧路径不重写（保持政策）；live 引用的语义未逐条重跑（只做链接/路径解析） |
| d4 | memory 12 个 store、history、register、glossary、tools、project、review；引擎读数（feedback-utils、record-retention、non-disposable-check 上下文） | 696 不可逐字复现；tools.md 未与当前机器 MCP 配置比对；098 记录能否从 state/test-evidence 无损派生未验证；129 条空处置与 backlog 未逐条匹配 |
| d5 | 9 个代码面 + 5 个根层文件；引擎退出码；goal/team 前置检查；镜像/再生成/渲染一致性 | `specs/**`、`memory/**` 等其它域数据；B16 shared 重复行按 `unverified` 保留；`.tmp` 总量归 d1 计量（d5 只认领沙箱与 root 属主） |

### 5.2 全局覆盖缺口（任何域都未审计的面）

1. `docs/` 文档树（内容准确性、链接、站构建）——不在五域范围。
2. `tests/` 全量（仅 d3 实跑了 1 个契约测试；测试有效性、重复、慢测试未审计）。
3. `src/specify_cli/` 源码（仅作为 `source.json` 消费者被提及）。
4. 框架源与安装副本的**内容**审计：`scripts/`、`templates/`、`skills/`、`agents/` 源侧只做了镜像一致性，未做逐文件内容审计（镜像一致 ≠ 两侧都正确）。
5. 宿主侧目录 `.claude/`、`.qoder/`、`.github/`、`.opencode/` 的陈旧文件（只验证了 88 个受管渲染目标）。
6. 根 `feedback/` 入站 bundle 目录、根 `memory/`（包内默认 memory）未被任何域认领。
7. `.specify/derive/`、`.specify/goal/`（已不存在但被引用）、`teams/.work/`（已清空）只作为证据被提及，未系统审计。
8. 仓库根工程文件（`pyproject.toml`、CI 配置等）与 `.specify/.gitignore` 的规则完备性（只验证了 state/.tmp 两棵根的命中）。

### 5.3 读数时间窗注意

1. **d1 的 T0/T1**：T0 = 02:55Z、T1 = 03:01Z；d1 所有 `.tmp` 组成数据按两时点标注。
2. **binding-base worktree 已移除**：d1 读数时的 177M / 10,032 文件已在 T2 前移除；`.tmp` 从 824M 回落到 650M。d1-11 因此 resolved。
3. **binding 提交已合入 master `c3997b182`**：分支 `debt-audit-harness-binding` 不再存在；该合并包含 `.specify/templates/gitignore-specify-template` 的修复，`sync-mirrors --check` 现为 exit=0。
4. **其它漂移**：state 268M→272M、1,178→1,189 文件；pid 163→164（全死）；script-interface 9→10 目录、19,174→19,197 文件；worktree 100 仍在 `134daf45f`。
5. **工作树**：2 项——`.specify/memory/trigger/index.json` 仅 `updated` 时间戳变更（引擎状态，非内容缺陷）；本审计目录未跟踪。
6. **口径差异**：d3 的 MB = du MiB，与 d1/d4 的 du 读数同口径；d4 另给内容字节（`du -sb`）。跨域加总只作量级参考，不作精确预算。

---

## 6. 边界与未验证项

- 本报告只读：未删除、未移动、未归档、未改写任何项目文件；唯一写入为本文件。未执行 git 写操作。
- 本报告不重跑五域的耗时测量；T2 仅做 §0.3 的 9 项点复核（分支/worktree/镜像/state/pid/.tmp/沙箱/quarantine-forks/工作树）。
- 债项严重度沿用域报告的分类并注明来源；唯一跨域升级为 D3-01（P0）与两处合并（D6-10/D6-12），均在表内标注。
- 未验证项：d4 的 696 口径、d2 的 142 残名、d5 的 shared 重复行、098 记录的可派生性、tools.md 与当前 MCP 配置的差异——均按 `unverified` 保留，不升级为事实。
- 本席不代答裁决；§3 的 24 个问题是本报告交给用户的全部决策面。

ANOMALY: none — 综合阶段未发现越出 d1–d5 已披露范围的新异常。两处预期内状态变化（`trigger/index.json` 时间戳更新、`binding-base` worktree 移除）已记入 §5.3；d5 的 root 属主阻断属已披露异常（d5 ANOMALY），其处置需 root 授权，已列入 Q23。

DEBT-DONE
