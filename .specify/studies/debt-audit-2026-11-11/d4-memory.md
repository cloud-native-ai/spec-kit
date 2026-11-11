# 债务审计 D4 — memory / history / register / glossary / tools / project / review

**审计角色**：SDD Debt Governor（只读审计 + 治理设计，无执行授权）
**审计日期**：2026-11-11
**范围**：`.specify/memory/`、`.specify/history/`、`.specify/register.md`、`.specify/glossary.md`、`.specify/tools/`、`.specify/tools.md`、`.specify/project/`、`.specify/review/`
**规模读数**：8 个审计对象；memory 1,536 文件 / 11 MiB（du），history 137 文件 / 5,967,578 B，register 76,284 B / 229 数据行，glossary 74,985 B / 180 数据行，tools.md 68,316 B，project 395,785 B，review 211,414 B
**并发读数**：requested=1 / effective=1 / effective_reason=`single-unit`（可表示单元集 = {D4 单一有界审计}，size=1；证据 = 本节范围清单；四个读域是同一报告单元的分区，写入面只有本文件）
**路径口径**：除特别注明外，证据路径相对仓库根；运行时占用量给 `du -sb` 实测字节，分配量另注 `du -sh`。

## 0. 口径

| 口径项 | 定义 |
|---|---|
| 记录类 store | `memory/{session,feedback,exec-quant,evidence,retention,coaching,trigger,renumber,todo,housekeeping,knowledge,tools}`，一文一件者为条目，`backlog.md` / `consume-log.md` / `probe-map.md` 等为登记册类载体 |
| "open" 计数 | register 状态列字面含 open 且不含 closed 的行；另单列状态为 `mixed` 但含 open 项的 1 行 |
| 反馈积压 | 引擎 `feedback-utils.py --action status` 的 `count_since_submission`，不是"未处置条目数" |
| 保留（retention） | `record-retention.py` 的 consume→receipt→retire 通道；`retention/closeout/` 是收口回执（artifact-commit-step.md § The receipt），与保留回执 `retention/receipts/` 是两个相邻家族 |
| 处置词表 | 本报告处置列取非一次性处置集四值 `archive` / `supersede` / `correct` / `exempt`（owner: `shared/definitions/non-disposable-definitions.md` § Disposition Set）；lane 为 SDD 修复 / sanitize 回收 / 保持并立政策。sanitize 五值 `delete/archive/repair/delegate/dismiss` 只在括号内作为执行动作注记；两套词表的桥由该 owner § Disposition Bridge 独占 |
| 判定时点 | 一切读数为 2026-11-11 本次执行时点；mtime 只作增长节奏证据，不作内容正确性证据 |

## 1. 基线逐条复核

状态取值：**confirmed**（读数成立）/ **changed**（读数或判读变化）/ **disproved**（前提不成立）/ **new**（新增发现）。

| # | 基线断言 | 状态 | 实测读数与判读 |
|---|---|---|---|
| B1 | session 454 / 3.6 MB；95% run-determination；单 run 最多 16 份 | **changed** | 454 文件、内容 2,903,172 B（分配 3.6 MiB）；run-determination 435/454 = **95.8%** 成立；单 `run_id` 最多 **11** 份（`r20261105T074027Z-084a`、`r20261030T081645Z-078a`），269 个 run_id，`(run_id, unit_id)` 重复组 **0**、全文哈希重复 **0**。16 不可复现；每条是独立单元的记录，不是复制 |
| B2 | feedback 464 条积压（阈值 10，10-08 未外发） | **confirmed** | 引擎 `count_since_submission=464`、`total=464`、`threshold=10`、`submitted_at=2026-10-08T14:08:41Z`、`should_prompt=true`；最早条目 2026-10-13，最新 2026-11-10；本地处置 processed 209 / ignored 126 / 空 129；`packages/` 目录不存在 |
| B3 | exec-quant 357 / 1.7 MB | **confirmed + changed** | 357 条记录 + 2 条 score；内容 684,686 B（分配 1.7 MiB）。**新增发现**：357/357 条 `quality.{elapsed_ms,tokens,errors,satisfaction,exit_code}` 全为 `not_evaluated`，0 条含 token 键；见 D4-04 |
| B4 | retention 空转（唯一 plan 11-05 items=0；696/0/696） | **changed** | plan 成立：`20261105T130456214498Z-retention-plan.json` `confirmed=false`、`items=[]`、grace 30、四 store。计数不可逐字复现：当前 `scan/status` 为 **1,270 总数 / 0 eligible / 1,270 blocked(unreceipted)**、receipts 0、ledgers 0；11-05 时点快照约 728（feedback 280 + exec-quant 179 + run-determination 269），696 应为更早/更窄切片。另有 33 个 `closeout/` 回执，属收口家族，不进入保留引擎 |
| B5 | history/.work 125 txt / 5.9 MB | **confirmed** | 125 个 `.txt`，5,859,933 B = history store 的 **98.2%**；全部 mtime 2026-11-10；README:48 自声明"一次性提取草稿（已 git-ignore，可随时删除）" |
| B6 | register 168 open（REC142/D10/F7/OI7/T1/c7；2 路径缺陷） | **confirmed** | 状态列字面 open 167 行（REC 142 / D 10 / F 6 / OI 7 / T 1 / c7 1）+ `mixed` 1 行（F-01…F-07）= 168 open-bearing；路径缺陷 2 处成立（见 D4-08）；150/167 行目标 spec 目录存在，17 行无 spec 路径 |
| B7 | project/ + review/ 3.5 月无消费者 | **confirmed** | project 10 文件 / 395,785 B，全部 2026-07-25/26；review 1 文件 / 211,414 B，2026-07-27；消费者只有 framework-map 声明、技能写入侧与测试路径断言，无读取侧；project 下无 `summary/` 交付目录 |
| B8 | tools.md MCP 快照 2026-02-02 | **confirmed + changed** | 时间戳 `2026-02-02T14:10:45`、count=2、`_source=/root/.vscode-server-insiders/...`（本机不存在）；**新增发现**：该 65,809 B JSON 块已不可解析（`json.loads` 失败于文件第 73 行），文件 68,316 B vs 模板 2,358 B；见 D4-11 |
| B9 | 098 线 memory 证据链缺失（三 store 0 条） | **confirmed** | run-determination 0、exec-quant 0、knowledge 0、feature_id=098 的 feedback 0；仅 1 条顺带提及（`feedback/20261110T104158Z-skill-sdd-loop-driver.md` 的 summary 写 "095-098"）。同期该线有 261 个 `state/098-*` 运行文件、117 个 test-evidence 文件、合并提交 `48e273d73`——缺的是记录层，不是活动 |
| B10 | feature_id 错挂 8 例（097→024、083→082） | **disproved** | 按"slug 数字前缀 ≠ feature_id"机械扫描得 **36** 处表面不一致，逐条核对权威 `Related Feature` 后 **0 处真实错挂**：097→024（14 处）是 `097-speckit-migrate-command/requirements.md:14` 声明的 Feature 024 子规格；066→065（10 处）是归档切片声明 Feature 065；079/080→062（4 处）是重编号前的 humanize-run-output 声明 Feature 062；063/075→058（4 处）声明 Feature 058；083→082（4 处）全部写于 2026-11-05 06:45–07:01，早于同日 clarify 将 083 立为独立 Feature 的落定，属 dated 记录。真实缺陷是**归属缺失**，见 D4-09 |
| B11 | 096–099 新增约 110 条 | **confirmed（量级）** | 跨 store 去重前约 90–110 条：feedback 提及 096:10 / 097:13 / 098:1 / 099:16；run-determination 096:4 / 097:13（feature_id 记 024）/ 098:0 / 099:8；exec-quant 按 run_id 096:9 / 097:13 / 098:0 / 099:16。098 为唯一全空线 |

## 2. 域内存量盘点

| Store | 文件 / 条目 | 字节 | 形态判定 |
|---|---|---|---|
| `memory/session/` | 454 文件（435 run-determination） | 2,903,172 | 一文一件；全量 tracked；无重复 |
| `memory/feedback/` | 464 条目 + 9 簿记 + 15 introspection + 2 state | 1,401,892 | 一文一件；`backlog/consume-log/cleanup-log/migration-*/probe-map` 为登记册类（sanctioned）；1 个残留见 D4-14，`last-regression-failed.txt` 已核销（被测试引用的 dated 记录） |
| `memory/exec-quant/` | 357 records + 2 scores + 2 legacy jsonl + 1 lock（ignore） | 899,404 | 一文一件；`records.jsonl`/`scores.jsonl` 是 owner 声明的只读 legacy 回退（最后写 2026-10-21/16），非违规 |
| `memory/evidence/` | 139 文件 / 20 个 run | 1,897,710 | 每 run 一目录、manifest/findings；未发现失效载体 |
| `memory/retention/` | 33 closeout + 1 plan | 102,014 | `receipts/`、`ledger/` 从未生成 |
| `memory/{coaching,trigger,renumber,todo,housekeeping,knowledge,tools}` | 26/2/4/3/2/10/10 | 92,907/80,532/44,738/10,393/10,704/23,603/99,306 | 近期运行产物与状态；`trigger/telemetry.jsonl` 已 ignore，`index.json` 为声明的学习状态 |
| `history/` | 11 主题 + README + manifest | 107,645（不含 .work） | manifest 108 sessions，last_run 2026-11-10；`.work/` 见 D4-12 |
| `project/` + `review/` | 10 + 1 | 395,785 + 211,414 | 见 D4-13 |
| `tools/` | system/shell/project 三 JSON | 271,554 | 机器生成、`.specify/.gitignore` 已 ignore tools/；合规 |

## 3. 债项登记

排序：严重度优先（P0 → P1 → P2），同严重度按主证据路径。**无 P0**。处置取非一次性处置集四值；括号内为 sanitize 执行动作。

### P1（结构性）

| ID | 类别 | 证据路径 | 实测事实 | 严重度 | 处置 | lane |
|---|---|---|---|---|---|---|
| D4-01 | 反馈上报通道停摆 | `.specify/memory/feedback/state/submitted-at.json`；`state/threshold.json`；`memory/feedback/` | 自 2026-10-08 起 34 天未 mark-submitted；464 条 = 阈值的 46.4 倍；129 条从未处置；`packages/` 不存在；活跃日新增 39–137 条。阈值 owner 声明值 10（`shared/declarations/facts/feedback-prompt-threshold.yaml`）与本地 state 一致，非漂移 | P1 | `correct`（恢复消费-打包-记账节奏） | SDD 修复（feedback 流程） |
| D4-02 | 路由欠账未执行 | `.specify/memory/feedback/backlog.md` | 176 行：119 `open` + 40 `**open**` + 7 `open-unverified` = **166 open-bearing**；5 carried-by-spec-053；4 closed；5 行表格结构损坏（4×8 列、1×9 列，未转义 `|`）；最早路由 2026-08-31，按月 Aug 1 / Sep 15 / Oct 120 / Nov 40。闭合规则要求 owner 文件证据，现存行恰是"已路由≠已执行"的堆积 | P1 | `correct`（执行/改派/按证据关闭） | SDD 修复 |
| D4-03 | 保留通道从未运行 | `.specify/memory/retention/plans/20261105T130456214498Z-retention-plan.json`；`.specify/memory/retention/closeout/`（33） | 1,270 条记录（exec-quant 357 + feedback 464 + run-determination 435 + session-note 14）全部 `blocked: unreceipted`；eligible 0、receipts 0、ledgers 0；唯一 plan 未确认且 items 为空；memory 近期增长 6–194 文件/日。33 个 closeout 回执不喂保留引擎（相邻家族，非缺陷） | P1 | `correct`（跑通 distill→plan→apply 并定节奏） | sanitize 回收（retention lane） |
| D4-04 | 量化轴全空 | `.specify/memory/exec-quant/records/`；`memory/session/*run-determination*` | exec-quant 357/357 条 `quality` 五键全 `not_evaluated`，0 条 token 键；仅 2 条 score（均 user-given）。run-determination 435 条：token 435/435、elapsed 423/435、artifact 415/435、satisfaction 360/435 为 `not_evaluated`；qualification 432 qualified / 3 partial。四量自提升回路目前只有结构、没有读数 | P1 | `correct`（接传感器；接不上则按 owner 规则登记带到期日的 `exempt`） | SDD 修复 |
| D4-05 | 整条线记忆缺链 | `.specify/specs/098-suite-speed-optimizations/test-evidence/`（117 文件）；`.specify/state/098-*`（261 文件）；`git log --grep=098` | 098 线经 analyze×3 / review×3 / merge 落地，但 run-determination 0、exec-quant 0、knowledge 0、feature_id=098 feedback 0；absence 与活动量形成结构性缺口（收口不变量"每 run 的记录由恰一个提交承载"在该线无对象） | P1 | `correct`（登记 OI + 日期性对账注记；不伪造记录） | SDD 修复 |
| D4-06 | 红钉未裁 | `.specify/register.md:38`；`tests/contract/test_neutrality_budget.py`；`.specify/specs/053-machine-decidable-artifacts/contracts/neutrality-budget.md` § C-7 | c7 自 2026-10-11 起为红（窗口违规文件 `tests/contract/test_confirmation_gates_sweep.py` 两处合法维护），登记行明写"待 053 流程的刻意重锚/复核裁定，MUST NOT 静默改写"。自 2026-10-11 起因归因更正后至今无裁定 | P1 | `correct`（完成重锚裁定；暂缓则 `exempt`，`expiry_kind=on-review`、`expiry_value=2026-12-11`） | SDD 修复 |

### P2（计划性）

| ID | 类别 | 证据路径 | 实测事实 | 严重度 | 处置 | lane |
|---|---|---|---|---|---|---|
| D4-07 | register 无分诊节奏 | `.specify/register.md` | 229 数据行、168 open-bearing；25 行指向已归档切片（REC-069a 14 + REC-069b 11）、31 行指向 Completed/Implemented 特性（REC-084 14 + REC-063 10 + REC-078 7）、72 行指向 live 特性、14 行属其他 REC 家族、25 行为决策/发现类（D/F/OI/T/c7），另 1 行 `mixed`；无周期分诊步骤 | P2 | `correct`（分桶分诊；逐行 close/supersede/exempt） | SDD 修复 |
| D4-08 | register 权威路径断链 | `.specify/register.md:39`（G1）；`:32`（goal 行） | ① G1 权威路径 `.specify/teams/.work/skill-layer-install-separation/S-B/verification.md` 不存在（`teams/.work/` 已清、git-ignored）；② goal 行含义列 `.specify/goal/session-driven-self-improvement/summary/` 不存在，现址 `.specify/anchoring/session-driven-self-improvement/summary/` 存在。其余相对路径经其隐含目录解析全部存在（150/150） | P2 | `correct`（G1 改指 tracked `team.md` forbidden 行 + run report；goal 行改指 anchoring） | SDD 修复 |
| D4-09 | 特性归属覆盖不足 | `.specify/memory/feedback/`；`memory/session/*run-determination*` | feedback feature_id 空 302/464（**65%**）；run-determination feature_id null 207/435（**48%**）。表面错挂 36 处全部为声明绑定或 dated 记录（见 B10），真实缺陷是覆盖，而非错挂 | P2 | `correct`（引擎侧默认/推断归属；不改写 dated 记录） | SDD 修复 |
| D4-10 | 词汇表提议积压 | `.specify/glossary.md:186` 等 | 180 行：112 proposed（**62%**）/ 68 confirmed；origin auto 145 / user 35；66 条 proposed 带需求标签（052×11、050×8、051×6、046×4、069×5…，最老回溯至 046 期）；1 条 user 来源核心术语"机制/策略分离"（083 已实现）仍 proposed；文件 74,985 B；`glossary-utils.py validate` 通过、无结构冲突（空 variant 伪冲突已排除） | P2 | `correct`（按行确认/退役；user 来源术语交用户裁定） | SDD 修复（词汇表维护） |
| D4-11 | tools.md MCP 索引失效 | `.specify/tools.md:30–1998`（JSON 块）；`:73` | 65,809 B JSON 无法解析（第 73 行 `"description": "...(originally in Chinese)"foo/bar\"[CN]\"...` 缺分隔符）；时间戳 2026-02-02、count=2、来源路径属他机；整文件 68,316 B vs 模板 2,358 B。owner `shared/definitions/tool-definitions.md:38` 明示此段手工维护、无生成器 | P2 | `correct`（按当前 MCP 配置修复，或回退为模板 scaffold；二者皆需用户裁定） | SDD 修复（客户端内容；模板 scaffold 不动） |
| D4-12 | history 草稿残留 | `.specify/history/.work/` | 125 txt / 5,859,933 B = history 的 98.2%；全部 2026-11-10；`history-utils.py` 的 extract 只写不删，manifest-update 不清理；README:48 与 manage-history SKILL:189 均声明可随时删除 | P2 | sanitize `delete`（草稿；ND 四值不含 delete，且该目录由 owner 声明为一次性草稿） | sanitize 回收 |
| D4-13 | project/review 陈旧产物 | `.specify/project/`；`.specify/review/master-20260726-205515.md` | 10 文件 / 395,785 B，全部 2026-07-25/26（含 gantt.png 203,452 B、milestones.png 95,519 B）；review 1 文件 / 211,414 B，2026-07-27；无 `summary/` 交付目录；3.5 个月无读取侧；framework-map 已把 project 定为 legacy read-only | P2 | `archive`（archive-not-delete，需用户授权） | sanitize 回收 |
| D4-14 | feedback 簿记残留 | `.specify/memory/feedback/index.json.root-stale-20260907` | 5,448 B 陈旧派生索引（文件名自标 stale；除本报告外仓库 0 引用）；其余 backlog/consume-log/cleanup-log/migration-log/probe-map 均为 sanctioned 簿记（probe-map 由 `probe-utils.py --action map` 重建）。同目录 `last-regression-failed.txt`（9,111 B）经复核被 `tests/unit/test_tier_classification.py:10` 引用为 dated 证据，**核销、不列债** | P2 | `archive` | sanitize 回收 |

## 4. feedback 分流方案

分两条独立通道，禁止混算（本地处置 ≠ 外发提交）：

1. **条目分诊（464 条 → 全部有处置）**：209 processed 与 126 ignored 只缺外发记账，不重开；129 条空处置走 `/speckit.feedback` consume（Path A），逐条落 `processed|ignored` + reason，路由结果写入 `backlog.md` 或直接修复。
2. **路由欠账（166 open-bearing 行）**：按闭合规则执行——只有 owner 文件变更（提交或实测缺陷消失）才关闭；`open-unverified` 7 行先复测；5 行损坏表格先修真（转义 `|`），否则任何机器读取都截断。
3. **外发记账（用户决策）**：`package`（产包、保留审计轨迹）或 `mark-submitted`（仅本地复位）二选一；两种都会把计数 464→0。**系统永不自动外发**。
4. **节奏**：以 seal 收口为自然检查点（或每周一次）；阈值 10 与 `should_prompt` 由 owner 声明，本报告不复述取值。目标：`count_since_submission 464→0`；open-bearing `166→0 或逐行 exempt`；损坏行 `5→0`。

## 5. register 分诊方案

| 桶 | 行数 | 内容 | 建议 |
|---|---|---|---|
| A 归档切片 | 25 | REC-069a 14 + REC-069b 11 | 随归档 spec 归档（`archive`），或转入 feedback backlog 继续追踪（`supersede`）；二选一逐批裁定 |
| B 已完成特性 | 31 | REC-084 14 + REC-063 10 + REC-078 7 | 复核是否已被后续机制吸收：已吸收 `supersede` 并注明新载体；仍有效转 backlog；均无证据则 `exempt`（带到期日） |
| C live 特性 | 72 | REC-068/071/072/086/095/098/099、REC-080、REC-074a、REC-079 等 | 保留 open，指定 owner，在下一次 review/seal 关闭；REC-080 的目标 spec 存在但 features.md 无 080 行（注册缺口属 D2 域，见 §8） |
| D 决策/发现 | 25 | D-001/D-001-a、D-1…D-8(092)、F-6/F-7(089)、F-093-*、F-A02、OI-3/4/7/9 + OI-069b/073/082、T-001..003、c7 | 逐行裁定；c7 与 OI-7 优先（c7 红、OI-7 阻塞 S5） |
| E 路径修复（非 open 行） | 2 | D4-08 两行（G1 为 resolved、goal 行为 closed-achieved，不占 open 计数） | 立即 `correct`，不参与分桶 |
| F 其他 REC 家族 | 14 | REC-T1×2、REC-A1/A2、REC-W1/W2/W3/W4、REC-C1、REC-T2、REC-D1 | 并入 B/C 两桶同规则分诊 |

合计：A 25 + B 31 + C 72 + D 25 + F 14 = **167 字面 open**，再加 `mixed` 1 行 = **168 open-bearing**。

分诊出口只有三种：有证据的 `closed`、有承接的 `superseded`、有到期条件的 `exempt`；不接受"看过但不处理"。节奏挂到 seal 收口或 house-keeping，不新建第二登记册。

## 6. 治理计划

顺序：机制修复 → 数据回收 → 结构收敛。每波独立确认门，前一波不绿不启动下一波。

### Wave A — 记录通道修复（机制）

- **范围**：D4-01/02（feedback 分诊与外发记账）、D4-03（retention 首次闭环）、D4-04（量化轴接传感器或登记到期豁免）、D4-05（098 缺口登记）、D4-06/07/08（register 分诊与路径）、D4-10（词汇表确认）、D4-11（MCP 索引修复）。
- **确认门**：feedback 打包/外发与 retention apply 均需用户显式授权（`shared/guidelines/confirmation-gates.md` 破坏性/外发项）；register 与词汇表修改走各自 owner 流程；tools.md 修复走客户端内容修改。
- **可测成果**：`count_since_submission 464→0`；open-bearing backlog `166→0 或逐行 exempt`；retention 产生首个非空 plan 与 receipts>0；run-determination 至少一个轴出现实测值（非 not_evaluated）；098 有 OI 行；register 两处断链 `2→0`；proposed 条目 `112→0 或逐行裁定`；MCP JSON 可解析。
- **中止条件**：外发授权缺失 → 只做本地分诊与记账，不打包；传感器数据不可得 → 按 owner 规则登记 `exempt` 而非编造读数；register 某行正确归属无法唯一确定 → 停在该行，不大批改写。

### Wave B — 数据回收（sanitize）

- **范围**：D4-12（history/.work）、D4-13（project/review 归档）、D4-14（feedback 残留）、D4-03 的 apply（按已确认 plan 退役原始记录）。
- **确认门**：`/speckit.sanitize` dry-run + 用户授权；archive-not-delete（草稿删除除外，owner 已声明可删）；apply 前逐条确认 plan 与保留回执。
- **可测成果**：history 占用 `5,967,578 B → ~107,645 B`（回收 5.86 MB）；project/review 11 文件归档且留下指针；feedback 残留 `1→0`；原始记录退役数 = plan items 数。
- **中止条件**：任一待移动文件仍被 live 文档引用且未同步改写 → 中止该批；plan 为空 → 不 apply。

### Wave C — 结构收敛（计划性）

- **范围**：D4-09（引擎侧归属默认/推断）、分诊节奏落 house-keeping、closeout 与 retention 两组回执的命名说明（只在 owner 文档加指针，不合并机制）。
- **确认门**：SDD 修复批 + 契约测试；不新增 store、不新增登记册。
- **可测成果**：feedback 归属缺失率 `65%→<5%`（新条目口径）；run-determination null 率 `48%→<5%`；每轮 house-keeping 产出 register/backlog 分诊读数。
- **中止条件**：归属推断需要读取用户未授权数据 → 保持 null 并在引擎输出标注，不猜测。

## 7. 裁决点（封闭问题，未自答）

- **Q1（反馈外发）**：(A) `package` 产包并人工外发；(B) 仅 `mark-submitted` 本地复位；(C) 本轮不动，只做条目分诊。
- **Q2（保留参数）**：是否按现状（grace 30、四 store）批准首次 distill→plan？(A) 是；(B) 改 store 集/grace 后再跑；(C) 暂不跑，登记带到期日的豁免。
- **Q3（history/.work）**：(A) 立即删除 125 个草稿；(B) 保留到下一次 history 运行后统一删。
- **Q4（project/review）**：(A) 归档 11 个陈旧产物并留指针；(B) 保留并声明为历史证据（`exempt` + 复核日）。
- **Q5（归档特性 REC）**：(A) 随 spec 归档；(B) 转入 feedback backlog；(C) 逐行 `exempt` 到 2026-12-31。
- **Q6（tools.md MCP 索引）**：(A) 用当前 MCP 配置修复；(B) 回退为模板 scaffold（丢弃本机快照）；(C) `exempt` 并标记"仅供参考"。
- **Q7（098 缺口）**：(A) 只登记 OI + 对账注记；(B) 允许按引擎从现有 state/test-evidence 派生可验证记录（不伪造时间戳）。
- **Q8（c7）**：(A) 立即完成 053 重锚裁定；(B) `exempt` 至 2026-12-11 并保持红可见。

## 8. 边界、异常与未验证项

- **写入边界**：本次未删除、移动、归档或改写任何项目文件；唯一写入为本报告（`studies/debt-audit-2026-11-11/d4-memory.md`）。未执行 git 写操作、未调用任何写模式引擎。
- **快速失败**：无阻塞性异常上抛；四处判读纠正在审计途中完成并已写入正文——① B10 的"feature_id 错挂 8 例"被权威 `Related Feature` 声明**证伪**（36 处表面不一致 → 0 处真实错挂）；② 097 的 run-determination 记录初扫按 feature_id=097 得 0，复核文件名/JSON 后确认存在 13 处（feature_id 记 024，属声明绑定），未按"整线缺链"升级；③ `probe-map.md` 初判"生成器已死"，经 `probe-utils.py --action map` 复核后撤回；④ "单 run 最多 16 份"不可复现（实测 11）。
- **跨域不越界**：features.md 的 097/098/080 缺行属 D2 注册表域；`.specify/state/098-*` 运行态属 D1 域；`archive/spec` 与 `archive/specs` 双命名属 D3 域。本报告只引用它们作证据。
- **未验证项**：① 基线 696 无法逐字复现（已给 11-05 快照 ~728 与三种口径）；② `.specify/tools.md` 的 MCP 快照未与当前机器实际 MCP 配置比对（Q6 裁定所需）；③ 098 的历史记录能否从 state/test-evidence 无损派生未验证（Q7）；④ feedback 129 条空处置条目中哪些可由现有 backlog 行覆盖未逐条匹配（分诊执行时确定）。
- **跨域机械读数（仅作上下文，不计入 D4 债项）**：`non-disposable-check.py` 全根扫描报 1,478 条目、1,477 open、1 unevaluated（candidates 3,166），集中在 `specs/`、`archive/`、`derive/`、`goal/`、`teams/`；本 D4 四根（memory/history/project/review）在该引擎的条目为 0。该读数供全局治理排序参考，不改变本报告的域界。

ANOMALY: 基线 B10 前提不成立——"feature_id 错挂 8 例（097→024、083→082）"经 `Related Feature` 权威声明与 dated 边界复核后为 0 处真实错挂；真实缺陷转为归属覆盖不足（feedback 65% / run-determination 48% 为空），见 D4-09。

DEBT-DONE
