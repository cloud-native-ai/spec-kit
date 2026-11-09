# 主题：Anchoring → Goal → Team（T2）

范围：goal 档案与目标生命周期、goal/team 相对 SDD 的编排层、临时 Goal/Team、`.specify/goal` → `.specify/anchoring` 重命名及其修复波。
覆盖 **33 个** Qoder 会话（2026-10-06 → 2026-11-10）；sid 在文内逐条引用，完整清单见文末。
关联主题：[[05-agents-skills-tools]]（seat 与派发）· [[07-archive-history-session]]（归档与历史波次）· [[09-memory-state]]（状态与证据）· [[00-cross-cutting-lessons]]

## 1. 关键决策与理由

- **Goal 档案引擎独占写**：`goal-utils.py` 是唯一写路径；`templates/commands/goal.md` 的"No skill may write"改述为"不得**直接**写"，从而解锁 `manage-goal` skill。（`e9450ef0`）
- **Goal 形态**：9 轮访谈收窄为"只建立 improve 流程，不执行改进"；保留"Goal 不分阶段"裁决（零 Targets）；成功标准含一个刻意的人工判断（`achieved`）；判据名为 `运行判定 (Run Determination)`，避开 断言/评估/判据/verdict/信号。（`9c57a1ed`）
- **Target 生命周期封闭**：无 edit 动作——只能 drop + 新 ID，ID 永不复用；唯一合法链路 `dropped→open→done`（`dropped→done` 非法）；`focus_target` 常不设，因为 done target 会让 `run-checks` check 3 阻断后续运行；Boundaries 无引擎动作，create-only。（`7896e937`、`6313ff57`）
- **Team 结构**：serial / parallel / iteration 三种 pattern；Meta supervisor 为唯一 canonical 写者，成员只产 patch；territory 校验只比较**同 `goal_slug`** 团队的 write×write，`forbidden` 不参与差集 → 跨 goal 写竞争与"两写者同持一文件却双绿"不可见，只能靠 `forbidden` 条目人工收窄。（`9c57a1ed`、`7896e937`）
- **Goal/Team 位于 SDD 之上**：授权两层——agent `sdd-invocation` + team `seats`，AND 关系，默认 `forbidden`；路由引擎 `sdd-route.py` 三值 `sdd/direct/adjudicate`，优先级 `adjudicate > sdd > direct`；输入缺失或冲突只裁决为 adjudicate，**绝不默认 direct**；反嵌套收窄而非删除：允许 depth-2 链（team orchestrator → member driver host → stage executor leaf），禁 virtual member 与 SDD-within-SDD；嵌套 SDD 在 review 后交接，merge/push 归外层。（`2b259011`）
- **085 临时 Goal/Team**：置于 `.specify/specs/<NNN>/goal|team/`；Goal 在 requirements U4 后形成、Team 在 clarify+plan U4 后形成；stage roles 替代通用 `sdd-executor`；`agent_concurrency_requested` 默认 24；per-agent worktree + 集成队列；maxTurns 统一（2026-11-05 政策 120→400）。（`d28dbd53`）
- **094 重命名**：全局 store `.specify/goal` → `.specify/anchoring`；spec-local `<spec>/goal/<slug>/goal.md` 与文件名 `goal.md` 不变——只有全局树移动（身份 vs 位置）；引擎 scope 值仍 `global|spec|auto`；dated 记录保值，只对齐活路径与 dated 措辞。（`8f473c19`、`a3a581e2`）
- **Reporter 席位**：可视化特性的 dogfood team 恰有一个 `role: reporter` seat，`validate-roster.py` 退出 0；SC-001 以真实 >90 s 运行（437.97 s）+ 30 s 节奏 20 行报告解除阻塞。（`9857e730`）
- **命名**：team 身份沿用兄弟约定 `SDD Temporary Team <id>`；页面限定 clause id（`handoff-contract#C-53`、`unified-archive-and-migration#C-112`）解决跨页编号。（`03be6910`、`a3a581e2`）

## 2. 可复用经验 / 踩坑

- **重命名债是机器绿债**：审计测得 630 行 / 276 个跟踪文件仍写 `.specify/goal`（LIVE 150）；引擎 `ARCHIVE_DIRNAME = ".specify/anchoring"`（`goal-utils.py:59`）无 legacy fallback。测试与文档一起陈旧时全绿：`test_directory_governance.py` 断言退役根，`framework-map.md:12` 同步陈旧；四个 owner 面（framework-map、non-disposable review surface/definitions、driver SKILL）仍称旧路径。（`ebbbcf14`、`5fea4a1e`、`e2c7372c`）
- **分母必须重测**：派发前提"9+9"来自目录计数（`ls -d specs/*/team`）而非定义文件计数——实树 probe 可见 9+8=17，全量普查 9+10=19（两个 one-level `team/team.md`：088 与 092-non-disposable）；"44 ids"实为 46。（`03be6910`、`37801781`、`cf3fe393`）
- **状态分期**：registry `Planned` 只是过渡前状态；`Planned → Implemented` 必须在 review 记录 Ready-for-Review 之前完成；不存在 `Planned → Ready for Review` 转换。VB-1 缺陷类在集成边界复发：同一 commit 的状态更新没有刷新 registry 行（`features/094.md:66`、`features.md:101` 仍写"进行中"）。（`2a7e498f`、`6d387867`）
- **goal-utils 的盲点**：`criteria` 是 replace 语义（两次调用覆盖第一条）；`validate` 对概念级 MUST 违反保持绿；Target 重述 guard 只做归一化字面比较（改写即盲）；GD-3 只做词法合取——绿 ≠ 证据。（`7896e937`）
- **编号双序列**：spec 目录号与 feature registry 号是两条偏移序列（033→037、080→062 等），不是错配；`092` 双占（`specs/092-non-disposable` 与 goal-team 线的 093/094）→ renumber 到 094 才解开。（`208e88b8`、`48099f17`、`ebbbcf14`）
- **并行线必须 worktree 隔离**：092 的 tasks 提交曾落到 093 分支；提交一律显式 pathspec（宽 `git add` 会卷入 in-flight fork 产物）。（`48099f17`）
- **并发重命名要核实落地**：写出 post-rename id 之前先验证 R1 的并发重命名已落地（113 markers / 113 distinct ids）。（`a3a581e2`）
- **命名/文案陷阱**：Notes 里的 `- **FR-007**` 定义式条目会触发 dup-id gate；`FR-022` 表格行 5 格塞入 4 列表格是真实缺陷而非解析假象（重解析可区分）。（`a3a581e2`、`a07fa138`）

## 3. 未完成 / 待办

- **活契约仍写 `.specify/goal`**：C-10/C-13/C-15/C-31/C-58/C-59/C-66 与 `owner-rewrites:57`；R2 声称已清但树中另有 15+ 处 live 命中（HIGH×5）；`tasks.md` T037/T073/T081、quickstart、data-model 仍规定旧路径。（`a3a581e2`、`37801781`、`cf3fe393`）
- **090/092 裁决**：registry 090 `Implemented` 且声称吸收 092，而树中 092 仍有 116 个开行、62 个不可解析 ND 条款、197 行任务图超过 160 上限——正是 Non-Disposable 要检测的状态/判定矛盾；G5 `status-unreadable` 0/52 BLOCKED。（`208e88b8`、`dd3b7b4e`）
- **G1 豁免通道未接线**：`_exemptions` 只在 `class_status_unreadable` 消费，`class_deferral_marker` 从不读取；E-3 fact 形状被 declaration schema 拒绝（exit 2）。（`6f34ad6c`）
- **`create→bind` 不可达**：bind 需要已存在的绑定（经验复现），create 路径无法到达。（`644a1597`）
- **`boundary` 引擎动作缺失**（Boundaries create-only）；093 线 Blocked（SC-006 `not_evaluated`，closure block；block 永不变成 completed）。
- **`verify-territory-disjoint` 的 forbidden 盲区**只靠人工狭窄化，无机器解法。（`9c57a1ed`）

## 4. 关键交互流程

- **Goal 访谈 → 团队 → achieved**：访谈（D1↩D7，9 轮）→ goal create → team create（serial 5 席）→ 中间停摆（B1–B4）→ S1 契约 → S2 引擎 → S3b critique 文档 → S4 thin shell → S5 verifier → `goal-utils` 置 `achieved`。（`9c57a1ed`）
- **goal ↔ team ↔ command-logic 转换**：`/speckit.team run` → S0 census → S1 硬停 + decision brief → Q1–Q3 裁决 → 分层设计 → "转换为goal和team, 并发处理" → 新 goal + team → smoke test。（`e9450ef0`、`7896e937`）
- **094 修复波**：分类（630 行）→ 逐页 clause id（113/113）→ W1 writer（9 条活规范行对齐）→ W2 repair（分母重测）→ VA/FV/VC/FV2 独立验证 → 集成。每个验证器只回自己读到的证据，FAIL 就 FAIL。（`8f473c19`、`63f60627`、`03be6910`、`866a72f0`、`6d387867`、`37801781`、`a07fa138`）
- **SDD 路由**：`sdd-route.py` 裁决（`sdd-capability-or-contract-change` 等）→ driver U0–U6 → stage dispatch；团队 run 的分支决策由 `goal-utils.py list --json` 引擎驱动，披露而不设门。（`d28dbd53`、`75ced50f`）

## 5. 用户 ↔ 模型分歧点

- 用户"SDD 启动即建 team"与 074"SDD 不得自建 Goal/Team"直接冲突 → 模型把约束摊开，用户选择 spec-local 临时 goal/team。（`d28dbd53`）
- 远程仓库已占 Feature 084 → 本地 renumber 为 085；本地 087 撞远程 → 改 088；092 双占 → 094（trunk 拥有 092）——用户裁决，模型执行。（`d28dbd53`、`9857e730`、`48099f17`）
- 用户"更新代码再合并推送"：模型按声明 git 流合并两个远程 commit，唯一冲突 `glossary.md` 双方保留。（`2b259011`）
- 模型两次误判（S1⊂S3、目标排除注释）在用户证据下撤回；预测的重述拒绝被测量推翻。（`7896e937`）
- 记录约束（goal boundary 排除差异化处理、team territory 漏 `src/specify_cli/`）与新需求相撞 → 模型在写前停下，用户裁决。（`e9450ef0`）
- 团队合并请求倒转了两层设计与已 dropped 的 T-001 → 模型停止等用户裁决，而非自行假设。（`6313ff57`）

## 覆盖 sid（33）

`03be6910` `208e88b8` `28144a1d` `2b259011` `2e79c944` `37801781` `3b8d316b` `3db3e58c` `48099f17` `5059aff0` `5a429557` `6313ff57` `63f60627` `644a1597` `6d387867` `70806e65` `75ced50f` `7896e937` `866a72f0` `86dd0ae8` `8b32d7cd` `8f473c19` `9857e730` `9c57a1ed` `a07fa138` `a3a581e2` `b3bf67dc` `bd6dcf6f` `cf3fe393` `d28dbd53` `e2c7372c` `e9450ef0` `ebbbcf14`
