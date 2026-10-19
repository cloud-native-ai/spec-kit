# Research: sdd-loop-driver 运行效率优化（SDD Loop Efficiency）

**Feature**: 063-sdd-loop-efficiency → Feature 058 无人值守 SDD 循环驱动机制（演化特性）
**Date**: 2026-10-20
**Method**: Phase 0 勘探 = 读取既有承载面（SKILL.md / 三份 references / watch-target.sh / docs 页）、既有 stream-json 先例、契约测试与校验器；基线实测在 2026-10-20 执行并逐条记录。全部为仓内证据，无外部厂商比较。

## 1. 基线实测（可溯源）

| # | 命令 | 实测结果 | 对设计的影响 |
|---|------|----------|--------------|
| B-1 | `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` | **12 passed / 4 failed**（macOS 15.6，bash）：`pid-reuse` 与 `zombie` 因无 `/proc` 判成 RUNNING；`manifest` 因 `sleep 3` 夹具在测试执行时已退出判成 DEAD；`pgrep-zero-match-trap` 在 macOS 上零匹配只输出一个 `0` | 既有自测含平台假设与时序夹具缺陷；FR-033 扩展自测时必须同时修正这些可移植性问题，否则新用例无法在开发平台证明 |
| B-2 | `python3 scripts/python/sync-mirrors.py --check --only skills/external` | 退出码 2，**68 个 DIFF，跨 12 个技能目录**；其中 sdd-loop-driver 3 文件（SKILL.md、references/dispatch-recipes.md、references/watch-model.md），其余为 draw-diagram 36、improve-skills 8、merge-skills 4、git-utils 4、sdd-project-setup 3、create-pages 3、database-utils 2、create-skills 2、think-skills 1、improve-docs 1、document-utils 1。sdd-loop-driver 镜像侧含 `.specify/` 前缀路径，且编译 fingerprint 与源侧不同（不判断哪侧“更新”，fingerprint 不表达新旧） | 既有契约 `test_c12_mirror_byte_identical` / `test_c18_mirror_pair_no_drift` 在基线即红（21 passed / 2 failed；测试函数共 23）。本特性只拥有 sdd-loop-driver 对：实现期用源→镜像同步修复该对，其余 11 个目录的既有漂移不在本特性面，采用「零 NEW drift」相对判据并完整披露 |
| B-3 | `python -m pytest tests/contract/test_sdd_loop_driver_skill.py -q` | **21 passed / 2 failed**（即 B-2 的 C-12/C-18；文件共 23 个测试函数） | 既有 H2 节集合（C-3）与 C-4 的 `sed` 断言当前为绿；本特性若新增 H2 或替换 runner 派生形态，必须有意更新并在 plan/tasks 记录理由（FR-041） |
| B-4 | `bash scripts/bash/run-tests.sh --names-out /tmp/063-names-probe.txt tests/unit/test_ensure_symlink.py -q` | 7 passed；names 文件 0 行；脚本自行输出解释器与条目数 | `--names-out` 接口可直接用于两个全量槽位的名称级差集（`comm -13`），无需新增测试引擎 |
| B-5 | `python3 scripts/python/validate-requirements.py .specify/specs/063-sdd-loop-efficiency/requirements.md` | `status: ok`；301 lines / 56 definition rows / 6 shared strings；0 error / 0 warning（requirements-repair 后实测 313 lines / 8 shared strings，见 `feature-ref.md` 基线记录） | 规格可作为 plan 的权威输入；准入脚本的 FR 计数口径应与该校验器的定义行口径一致 |
| B-6 | `python3 --version` / `python --version` | 3.9.6 / 3.14.6 | 新脚本按 `pyproject.toml` 的 `>=3.8` 编写（不用 3.9+ 专属语法）；pytest 由 `run-tests.sh` 自行解析 |
| B-7 | 检索 `--output-format stream-json` | 既有先例：`skills/internal/create-team/scripts/dispatch.sh` + `stream-filter.py`；形状权威：`.specify/shared/definitions/subagent-definitions.md` § External Dispatch Visibility Contract（事件 `assistant` / `system(init)` / `result`） | 派生规则可复用**事件形状知识**，但 loop-driver 分类为 external、运行时零框架依赖，不能复用内部技能脚本；必须自包含实现并在文中声明「设计期参考、运行时无依赖」 |

## 2. 设计决定

### R-1 Runner 打包：单一参数化 `stage-runner.sh`（取代逐阶段 sed 派生）

- **决定**：在 `skills/external/sdd-loop-driver/scripts/` 新增通用 runner 脚本，接收 `--cli/--cli-args/--project-dir/--prompt-file/--sentinel/--line/--stage/--state-dir/--mode auto|stream|buffered`；dispatch-recipes 只展示调用形态与产物路径。逐阶段 `sed` 派生 runner 的做法标注为被取代的旧形态。
- **理由**：runner 是四件套、stream-json、派生、降级与哨兵计算的唯一执行点；把它做成脚本才能被行为测试，避免「配方文本 × 每阶段副本」多重真源。参数化不新增运行时平台（宪法 IX）：生命周期仍等于单阶段。
- **替代方案否决**：继续在配方里用 sed 生成 per-stage runner——无法被 CI 执行、每阶段副本漂移、降级与派生逻辑无法单点测试。
- **契约影响**：既有 C-4 断言 `sed` 为 runner 派生差异面；本特性有意更新该断言为 `stage-runner.sh`（FR-041 允许，理由记录于 plan/tasks）。

### R-2 派生：自包含 `derive-live-log.py` + runner 收口

- **决定**：stream 模式采用 `CLI --output-format stream-json | tee raw.jsonl | python3 derive-live-log.py --out live.log` 的管道；派生进程对非终止事件只写**带前缀的单行进度**，在 EOF 时追加终止 `result` 事件的 `result` 文本（逐字）。runner 在 CLI 退出后做收口：live log 最后非空行 = 哨兵 → `sentinel=1`；否则尝试一次性 `--finish` 从 raw 提取；仍失败 → `sentinel=0` 且 `progress=degraded:<reason>`。CLI 不支持 stream-json（`--help` 无 `--output-format`）或派生运行时缺失（无 python3）→ 启动即选 buffered，记录 [[STR-004]] 与原因。
- **理由**：哨兵必须来自终止结果文本（FR-028）；把 result 文本放在派生输出的最后，watcher 的「最后非空行」判据无需改动。非终止事件内的哨兵字样被前缀行包裹，不可能成为裸哨兵。
- **替代方案否决**：复用 `create-team/scripts/stream-filter.py`——它在 result 事件只打印 `== DONE` 摘要、不输出 result 文本，且属于 internal 技能，违反 external 零运行时依赖。另否决后台 `tail -f` 派生进程：管道天然随 CLI 结束，生命周期更简单。
- **降级不伪完成**：派生失败时 live log 可能为空/不完整；runner 的收口只认「最后非空行 = 哨兵」或成功 `--finish` 提取，不因 raw 有内容或退出码 0 判 DONE。

### R-3 准入：`admission-check.py`（七判据全部机械判定，fail-closed）

- **决定**：脚本按 FR-003(a)–(g) 输出逐条 `pass/fail` 与证据指针；整体 exit 0 仅当全部判据通过。自动判据：**只数 FR 定义行**（不把 SC 计入）与任务行数（区间 owner = FR-003，脚本常量为运行时 owner，契约测试钉住）、clarification 标记为零、需求质量清单全绿、Related Feature 注册可解析、宪法未改动、路径/内容扫描（引擎/模板/技能/依赖清单、安全敏感面、网络/模型 API 痕迹）、`--lines-manifest` 恰一行本线记录且分支匹配。任何解析失败或输入缺失 → fail-closed。
- **理由**：数值区间与文件存在性是固定规则，交给程序（Program-First）；FR-003 要求以可复算制品证据判定，因此**不设自证判据**。`lines-manifest` 是 U0 拓扑声明的导出视图，单线是硬性事实；多线并行的一线不得使用快车道。路径/内容扫描采用**保守超集**（改动既有引擎文件也拒绝），宁可多跑 checklist，不静默降质。
- **替代方案否决**：让驱动凭阅读规格判断或写自证文本——不可复算、不可审计；复用 `.specify/scripts/python/validate-requirements.py`——external 技能不能对框架脚本产生运行时依赖。

### R-4 测试预算：状态脊内 JSONL 台账 + 阶段证据文件 + 审计脚本

- **决定**：每线状态脊内用 `<!-- test-budget:begin --> … <!-- test-budget:end -->` 围栏承载 JSONL 台账（字段见 data-model E2）；阶段测试证据写入 `<spec-dir>/test-evidence/<stage>.jsonl`。`audit-test-budget.py` 校验：槽位数、槽外例外必须带原因与证据、环境失败不得消耗槽位、缺字段报告 `unknown`、可选扫描阶段日志（`--logs-dir`）发现未入账的全量命令。最终收口由驱动或其派发的独立校验单元执行，使用 `scripts/bash/run-tests.sh --names-out`（或项目声明的规范 runner）+ `comm -13`。`implement` 阶段内不得再跑第二次全量；其内部回归比较义务由收口槽位承担。
- **理由**：台账是机器可审计的结构，不是散文；证据文件把「命令/依据/rc/计数/新增失败/基线」固定为字段；名称级差集保留回归发现能力（仅比计数被明确禁止）。请求方报告的「一次运行 6 次全量」是 dated baseline，本 plan 不复测、不据此宣称提速百分比。
- **替代方案否决**：把台账写进自由格式散文——审计只能靠再读一遍，违反 Program-First；为预算新增数据库/服务——违反 IX 与 FR-035。
- **环境失败边界**：解释器/依赖缺失、pytest 在收集或执行前退出（stderr 证据）→ `environment-failure`，不消耗槽位；已收集并执行（含 0 tests collected 的选择失败）→ 消耗槽位并判证据不足，不得当环境失败。

### R-5 Plan 约束：编排层纪律 + `PLAN-EDIT:` 声明 + `audit-plan-changes.py`

- **决定**：plan U4 通过时，驱动在状态脊登记 `plan_constraint=active since=<commit> at=<ts>`；下游阶段提示词携带只小修块，并要求任何 plan 制品改动在哨兵前回传 `PLAN-EDIT:` 声明行（完整格式由 efficiency-model 单一 owner）。U4 用 `git diff --name-only <stage-base>..HEAD -- <plan-owned paths>` **加** `git status --porcelain`（未提交改动）+ 声明行判定：无触碰=none；有触碰且无声明=undeclared；有声明再按驱动分类 minor/substantive。undeclared/substantive 先判该阶段门失败，再按 FR-022 两分支：修复既有缺陷且不变更已批准范围/架构/数据模型/契约/任务分解 → 派发完整 plan 重审（记录触发）；否则四要素上送。每次实质改动都按其分支处置并留痕；重复回环由既有 stall/retry 纪律兜底，不设人工次数上限。
- **理由**：框架命令内部不改（FR-025 显式排除），驱动是唯一执行点；`audit-plan-changes.py` 把「是否触碰/是否声明」变成确定性输出，语义分类仍由驱动记录依据。按最终 diff 分类，避免「多处小修合并成实质改写」的措辞规避。
- **替代方案否决**：在 plan 命令内部加硬门——超出本特性范围且违反 FR-025；完全不实现——brief 要求显式排除或实现，本特性选择实现编排层可安全实现的部分。
- **显式排除/设计代价**：非驱动手工调用阶段命令不受约束；若后续证明编排层实现不安全，另立特性修订，不得静默扩大范围。

### R-6 脱离：本地补齐 nohup，远端保留 ssh+su+nohup

- **决定**：远端 recipe 保持 `ssh ... "nohup su - <run-user> -c '…' </dev/null >/dev/null 2>&1 &"`；本地 recipe 改为 `nohup bash stage-runner.sh … </dev/null >runner-log… 2>&1 &`（可用时 `setsid` 加强进程组脱离，不作为硬依赖）。派发记录写入 `detached=yes|no`；遗漏 nohup/`</dev/null` → 标记「未脱离」并记录风险，不计为受保护运行。
- **理由**：FR-031 明确 nohup 双拓扑；本地原有直驱形态会在驱动进程退出时被会话终止。setsid 在 macOS 默认不提供，故只作可选增强。
- **替代方案否决**：只在远端脱离——不满足 FR-031 双拓扑；用系统服务/守护进程托管——违反 FR-035。

### R-7 Watcher：只加证据面，不改判定

- **决定**：`watch-target.sh` 增加可选 `--raw-stream PATH`：WATCH 输出附 `stream=<na|absent|growing|idle>`、EVIDENCE 附 raw 路径与字节数；**不参与任何 verdict**。判定表、退出码、窗口/deadline 语义零改动。自测新增：非终止事件哨兵字样不判 DONE、终止 result 事件判 DONE、派生失败不伪完成、脱离 runner 在驱动退出后存活（后两者用文件夹具 + 进程夹具）。
- **理由**：FR-033 要求 watcher 支持 live log 作为哨兵来源并保留 raw 证据；把 raw 成长作为可见性字段足够，不需要改变状态机。既有自测的 4 个平台/时序失败一并修正（B-1），否则新用例无法证明。
- **替代方案否决**：让 watcher 直接读 raw 判哨兵——会破坏「最后非空行 = 哨兵」契约，并把 JSON 信封误判风险引入判定层。

### R-8 契约变更面：新增一个 H2 + 有意更新两条既有断言

- **决定**：SKILL.md 新增 H2 `Efficiency Optimizations（运行效率优化）`（摘要 + 指针，不复述细节），更新 `test_sdd_loop_driver_skill.py` 的 `PINNED_H2_SECTIONS` 与 C-4 的 `sed` 断言；新增 `tests/contract/test_sdd_loop_driver_efficiency.py` 钉住本特性条款。
- **理由**：四项优化是技能面的能力级变化，需要可发现的入口；详情由 `references/efficiency-model.md` 单一承载。既有断言的有意更新必须记录理由（FR-041），不能静默删改。
- **替代方案否决**：把所有内容塞进既有 H2——入口不可发现，且 C-3 虽不用改但语义重心被稀释。

### R-9 文件格式与证据面：不新增存储/服务

- **决定**：baseline/final 失败名单用 `--names-out` 的纯文本（每行一个测试 ID）；台账用状态脊内 JSONL 围栏；阶段证据用 `<spec-dir>/test-evidence/<stage>.jsonl`；准入记录用状态脊内 Markdown 块 + 脚本 JSON 输出。全部是文件，无新目录服务、无新依赖。
- **理由**：FR-017/FR-035 要求证据可审计且不新增常驻服务；JSONL 行级追加与 `comm` 天然可复核。
- **替代方案否决**：SQLite/向量库/外部日志服务——均违反 IX 与 FR-035。

### R-10 本特性的自应用与证据边界

- **决定**：063 自身走完整链，不产生快车道记录；本 plan 由完整 research/design 流程产出。确定性组件（准入、台账、派生、脱离、名称级回归）由 CI 测试证明；LLM 驱动的阶段序列行为由实现期录制的编排演练（dry-run trace）证明，并在 verification.md 如实标注哪些 SC 是自动证据、哪些是录制证据。
- **理由**：driver 本体是提示词手册，不是可单测的调度器；把不可自动化的部分伪装成自动测试才是伪证据（better-harness 证据纪律）。录制 trace + 契约钉住决策表是可复核的诚实上限。

## 3. 明确排除（本特性不做）

- 不修改 `templates/commands/*`、`skills/internal/{implement-feature,review-sdd-process,analyze-artifacts,create-plan}` 等框架命令内部流程；plan 约束与测试预算只在编排层执行。
- 不新增技能、命令、常驻服务、守护进程、外部依赖或模型 API；不引入 `jq` 等新工具。
- 不改变哨兵字面量、watcher 判定状态机、退出码、确认门、独立校验与卡死处置。
- 不自动 push、不自动合并远程分支、不自动外传反馈数据。
- 不把快车道设为缺省，不对大型特性启用，不跳过 analyze/review。

## 4. 未决项

无。FR-003 的中型区间、预算作用域、plan 改动分流、入口字面量均已在 clarify Session 2026-10-20 冻结；本 plan 不重裁。
