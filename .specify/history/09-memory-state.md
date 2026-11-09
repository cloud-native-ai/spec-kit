# 主题：Memory + State（T5）

范围：并发安全存储、运行判定与 exec-quant、反馈通道、feature registry 与登记纪律、状态证据与指令预算、`.specify` 工作区治理。
覆盖 **44 个** Qoder 会话（2026-10-08 → 2026-11-10）；sid 在文内逐条引用，完整清单见文末。
关联主题：[[07-archive-history-session]]（记录治理）· [[05-agents-skills-tools]]（引擎）· [[06-anchoring-goal-team]]（registry 状态）· [[00-cross-cutting-lessons]]

## 1. 关键决策与理由

- **并发安全存储**：记录类数据一条一文件（`records/<UTC-microsec>-<8rand>.json`、`scores/` 同理），atomic temp+rename；派生索引即读即建、不再持久化；单标量状态一文件（`state/threshold.json` 等，缺失即默认）；legacy 单体 `index.json` 只读回退，首次写时显式迁移并披露 `migrated: true`。**拒绝**"单体 + 合并纪律"——全文件重写正是冲突根因。（`5ea25dfb`、`840faac8`）
- **单一所有者例外**：`trigger/index.json`、`history/.manifest.json`、`teams/<slug>/{items,run-log,STATE}`、feedback `cleanup|migration-log.md`、canonical registries（`features.md`/`register.md`/`glossary.md`）保留为单文件；可变处理状态按 key 拆分。（`840faac8`）
- **运行判定（Run Determination）**：四轴 = token 消耗 / 耗时 / 制品正确性 / 满意度；无源即 `not_evaluated`，绝不以"fine/0/编造数字"填充；`(unit_id, run_id)` 幂等锁、永不自动铸造 run-id；E1 首记录终局；`--user-turn-class` 属于 `settle` 不属于 `determine`；复杂度由调用方声明（封闭域 `complex|simple`），green check 必须逐字声明。（`2337ce96`、`9c57a1ed`、`da741035`、`26ca6503`、`99912504`、`d01a3852`）
- **Exec-quant 通道**：独立 store（不混 feedback store——feedback 只收摩擦）；059 FR-011 的"结构性排除"被 068 取代，改为反馈包一等载荷（caps 1000 records / 16 MiB、确定性顺序、包级来源身份、无绝对路径/凭据、空条目仍可打包）；ingest 用五元 `identity_key` + 独立 `content_hash` + keep-first + `identity_conflicts` + flock；aggregate 追加写 `summaries/`。（`2337ce96`、`4f60c597`、`eedffe8a`、`27383836`）
- **反馈层**：摩擦专用、阈值提示非阻断；通知需要 `should_prompt` **AND** run-determination 路由位；072 以 `kind`/`slice`/`custom:owner/name` 复用同一 store，不建第二引擎；client-metrics 只读，零分母 = `not-evaluated`。（`5ea25dfb`、`75ced50f`、`c218f73c`）
- **Feature registry 纪律**：集成顺序 spec 侧先、registry 后；绑定后才做校验；状态按证据判读、绝不回退；详情文件/index 行数提交前核对（61 行 = header 61）；registry 是 hand-maintained——无引擎、无 guard。（`c6516cb7`、`86dd0ae8`、`62a1b0b1`）
- **ID Register**：所有耐久 ID（D/OI/S/T/F/B/REC）在铸号那一刻登记进 `.specify/memory/register.md`；指针形态（id → 一行含义 → 权威路径 → 状态），不复述决策正文；durable 测试：被跟踪产物引用或仍待决者必须登记。（`9c57a1ed`、`f556a5f4`）
- **状态盘点**：class reading = registry-status × closure-verdict；G5 51/52 产生不了 verdict（输入契约晚于 dated spec），不修状态、不伪造；`block` 永不变成 `completed`（093 线）。（`dd3b7b4e`、`48099f17`）
- **`.specify` 工作区治理**：census 17,931 文件（15,423 ignored，`teams/.work` 15,316 / 272 MB，tracked 2,556）；`.specify/.gitignore` 成为 `.specify` 专属规则的单一 home，`trigger-utils.py` 的 `do_init` 写入该文件而非根 `.gitignore`；瘦身只做 Phase 0（gitignore 治理，无删除）。（`27383836`、`48099f17`）
- **指令预算**：预算 value owner 是 `scripts/bash/generate-instructions.sh`；"最小必要幅度"的 decidable 规则（S+1024 向上取整）只存在于下游（research/contracts/tasks），需求文本未指定 → 082 H-03 判 `downgrade`（bounded、已披露、有缓解）。（`12f9e0ad`、`d01a3852`）

## 2. 可复用经验 / 踩坑

- **register 无引擎无 guard → 静默漏登**：被引用的 061 REC id 从未有行；"reference⇒registration" guard 仅提案；`register.md` 原本 0 条 REC 行。（`86dd0ae8`、`f556a5f4`）
- **Registry 陈旧复发**：062 行保留 round-1 计数（34/28/10/27 vs 35/29/11/30）未随修订；094 同 commit 的状态更新没刷新 registry 行（VB-1 在集成边界复发）；`features.md` 巨大——只做定向读；`Total Features` 与行数需程序核对（87→88）。（`aaf1fee4`、`6d387867`、`03be6910`、`61298504`）
- **基线纪律**：冻结失败**名集**而非总数；re-freeze 必须记账（063 一次 63→21 留下 42 个 ghost name 未记录）；基线可被自身编辑污染（worker 引擎改动卷入背景基线 → 停掉、按 HEAD 重捕）；pre-existing 归因需在旧 worktree 复现（`aafbf5a8` 的 8 个代表失败）。（`1b96db87`、`f556a5f4`、`5a429557`、`d28dbd53`）
- **状态矛盾谱**：056 header `Planned` vs body/registry `Implemented`；073 仅 requirements 标 `Implemented`；089 `Implemented` vs 111 失败/34 基线；058 `Implemented` + 8/9 SC `partial`；090 `Implemented` vs closure `block`；062 详情行要求 Ready-for-Review 而 `feature-integration.md` 无 review 行——status-unreadable 是一个**类**，不是单点。（`3b8d316b`、`c2287715`、`a3821ef3`、`208e88b8`、`d22e136f`、`dd3b7b4e`）
- **引擎语义细节**：run-determination 拒绝重复 run-id（先 settle 旧记录再 determine）；feedback 需重复 `--points` 与 `--review` 正文；`artifact_correctness: not_evaluated (no_baseline)` 是诚实结果；simple-unit 的 run-determination 记 `skipped`；feedback `list --disposition open` 默认 `--limit 5`（全量 open = 136，需 `--limit 0`）。（`111683d8`、`26940d66`、`be645516`、`a9bcef84`、`0f63f87a`）
- **存储并发残留**：跨分支同秒同 unit 记录碰撞登记为 Known Residual（≤ status quo）；嵌套 worktree self-location 陷阱让套件改写 `trigger/index.json`——只判 committed HEAD。（`5ea25dfb`、`644a1597`）
- **`_ENGINE_SIBLINGS` 与 mirror**：引擎/测试读 `.specify` 镜像；晚到的 `.part` 清理改动若未同步镜像会产生 4 个失败。（`5ea25dfb`、`4f60c597`）
- **预算/仓库门槛**：neutrality-budget gate 在 clean HEAD 时零余量（26 基线）；`instructions.md` 33898 B 超 32768 预算且无合法 R1/R2 候选 → 挂起而不是硬改。（`840faac8`、`a3d3ec0a`、`d01a3852`）
- **临时目录与记录卫生**：captured output 不得落裸 `/tmp`；记录后即删；scratch 只在 sanction 根。（`a9bcef84`、`9857e730`）

## 3. 未完成 / 待办

- **Registry 修复队列**：001/003 header、057 路径刷新、062 计数、094 行、090/092 裁决；006/009 未勾任务与实现状态对齐。
- **G1/G5 机制**：豁免通道接线、E-3 fact 与 declaration schema、C-804 决策或 51-spec schema 迁移。
- **指令预算**：`instructions.md` 超预算的 R1/R2 裁决未决；`## Fact, Correctness & Logic Checks` 落后模板 403 B（当时读数）。
- **`OI-082-01`** `/speckit.improve` 接线；反馈 backlog（多次读到 131/174/379/382 等不同时点读数）与审计 backlog 由 owner 排期。
- **closeout**：策略 `ask`，记录留在未提交状态等用户决定；多数 commit 未 push。

## 4. 关键交互流程

- **特性状态记录链**：requirements 校验 → registry 绑定（spec 侧先行）→ 阶段记录 → closure → registry 状态翻转；每一步都留程序可读证据。（`c6516cb7`、`99912504`、`2a7e498f`）
- **wrap-up 引擎链**：run-determination（四轴）→ exec-quant 记录 → feedback 记录或跳过；阈值提示按 `should_prompt` AND 路由位判定；记录失败要显式声明而不是吞掉。（`75ced50f`、`4f60c597`、`eedffe8a`、`a3d3ec0a`）
- **波次状态证据**：before/after JSON 字节一致（零写证明）或差值等于实际关闭数（G2/G4/W5）；E-7 四段随行。（`c8faa376`、`6f34ad6c`、`ca4d659f`）
- **Closeout**：policy `ask` → 展示序列 → 用户决定 → 一 receipt；`origin` 排除（只读 upstream），目标 github/gitlab/gitee。（`48099f17`、`a9bcef84`、`af6d3fc1`）
- **Coaching/status**：`status-digest.py` exit 0；exit 3 = "nothing-running" 是正确答案；digest header 缺解析后的 registry 目录是已知缺陷。（`af6d3fc1`、`a9bcef84`）

## 5. 用户 ↔ 模型分歧点

- 用户授权框架阈值变更（082 任务上限 40→60、`TASK_CEILING`/`TASK_MAX`）而不拆分；模型披露 D10(x)SHOULD vs D14 的张力后执行。（`0f63f87a`）
- 用户要求 `tmp/` 根因；模型迁移不删除，并把"禁止 repo-root tmp、scratch 进 `.specify/.tmp/`"写入纪律。（`c218f73c`）
- 用户把 `.specify` 瘦身限定为 Phase 0（gitignore 治理、无删除），模型按范围执行。（`27383836`）
- 复杂度认知差：模型初判 Complex，自纠为 Simple 并保留披露。（`544f490f`）
- 诚实优先成为稳定模式：无基线不造基线（`artifact_correctness: not_evaluated`）、无测量不写已修（G1/G5 BLOCKED）、`block` 不改写为完成。（`be645516`、`6f34ad6c`、`48099f17`）

## 覆盖 sid（44）

`04e3f86b` `09e7b15b` `0f63f87a` `111683d8` `1f5f64d1` `208e88b8` `2337ce96` `26940d66` `26ca6503` `27383836` `302477d1` `46290991` `48099f17` `4f60c597` `5ea25dfb` `61298504` `644a1597` `6d387867` `6f34ad6c` `6fbbb89d` `840faac8` `866a72f0` `86dd0ae8` `8ac9bcc5` `8b32d7cd` `9857e730` `99912504` `9c57a1ed` `a3821ef3` `a3d3ec0a` `a9bcef84` `aaf1fee4` `af6d3fc1` `c218f73c` `c6516cb7` `c8faa376` `cf3fe393` `d01a3852` `da741035` `db0b0717` `dd3b7b4e` `df0d4308` `f3930139` `f556a5f4`
