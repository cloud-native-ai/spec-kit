# ID Register (编号登记册)

> **本文件是什么**:本仓全部**持久编号标识**的唯一索引 —— 每个编号在**诞生的那一刻**在此登记一行:
> 编号 → 一行含义 → **权威路径**(完整陈述所在,本文件不复述其内容) → 状态。
> 规则 owner:`.specify/instructions.md` § ID Register (编号登记) / 模板源 `templates/instructions-template.md` 同名小节。
> **为什么必须有它**:只活在 session 历史、git-ignored 工作区或对话上下文里的编号,对任何后续 session 均不可解读;
> 引用者却当作已知上下文继续推进 —— 这正是本登记要关闭的静默失效。维护方式:手工(与 glossary 同类),无引擎。

| 编号 | 含义(一行) | 权威路径(完整陈述) | 状态 |
|------|------------|--------------------|------|
| D1–D9 | goal `session-driven-self-improvement` 的 9 轮访谈决策:D1 初版 objective(后被 D7 撤回重述)、D2 满意度判定规则、D3/D6 Target 与阶段轴裁定、D4 改点以 feedback 形记录(被 D5/D7 修正为 sensor)、D5 归一问题、D7 终态=双触发 improve 流程、D8 「断言」实为判断逻辑的概念化、D9 四项细节移出 objective 交团队承接 | `.specify/goal/session-driven-self-improvement/goal.md` § History(逐字留存历次取值)+ `.specify/teams/session-driven-self-improvement/team.md`(D9 承接小节);访谈全账本 `.specify/memory/session/2026-10-05-goal-session-driven-self-improvement-interview.md`(**git-ignored**,短 notebook) | closed(D7 撤回 D1、D5/D7 修正 D4 的链条已在 History 留痕) |
| B1–B4 | 四量口径用户裁定(2026-10-06):B1 机制定名「运行判定」;B2 正确性拆两半只做制品正确性;B3 满意度默认接受+窄例外(紧邻未解决红→not-evaluated);B4 `templates/commands/improve.md` 写权归本团队 | `.specify/teams/session-driven-self-improvement/team.md` § 四量口径裁定 | ratified |
| S1–S5 | 本团队 serial 链五阶段:S1 契约设计、S2 引擎实现、S3 被动触发接线、S4 主动触发命令(两次派发累积)、S5 独立验证 | `.specify/teams/session-driven-self-improvement/team.md` DAG 与 Stage 表 | S1/S2 完成;S3 产出已验证未落地;S4 累积 1 落地;S5 未开始 |
| S3b | 追加阶段:批评与自我批评概念文档(SI-3C 落点) | 同上 team.md DAG(critique-concept-author 席位) | completed(2026-10-08) |
| OI-1…OI-9 | S1 设计契约的 9 个开放项,各项自带选项与 decider,禁止静默解决 | `.specify/teams/session-driven-self-improvement/runs/2026-10-06-S1-judgment-contract.md` § Open items(**tracked** 副本;工作区原件在 git-ignored `outputs/`) | 见下逐项 |
| OI-1 | 「绿但无红先行取证」的 verdict 映射:契约选 (a) `not_evaluated/green_unproven`,已实现;备选 (b) `regressed` 为一行映射改动 | 同上 | resolved(用户裁定 (a) 并已实现;`scripts/python/run-determination.py:201` 单点) |
| OI-2 | 判定记录的持久落点:契约选 (a) 经 `memory-utils.py` 落 `.specify/memory/session/`;**实现期发现该路径不可达**(`SCOPES` 封闭、slug 剥除 `/`、reindex 非递归),S3 停等用户裁定 → 即下述 **D-A** | 同上 + `runs/20261007T170045Z-report.md` § 4 | resolved(扁平落点随 S3 落地) |
| OI-3 | token/耗时的绝对目标值(相对比较之外的将来项) | Open items § OI-3 | open,不阻塞(decider:用户经 /speckit.goal modify) |
| OI-4 | 语义正确性作为将来独立轴(本轮明确不设计,不留占位轴) | Open items § OI-4 | open,不阻塞 |
| OI-5 | goal.md 旧术语「判断逻辑」的修正 | Open items § OI-5 | resolved(commit 0206e021 经 /speckit.goal 落地) |
| OI-6 | 是否读 tool-session 的用户动作信号(v1 选不读) | Open items § OI-6 | resolved-for-v1 |
| OI-7 | SI-2 悬空的 `/better-harness` 引用处置 | Open items § OI-7 | open,阻塞 S5 检查单 |
| OI-8 | 比较轴容差带(v1 以结构性手段替代数值容差) | Open items § OI-8 | resolved-for-v1 |
| OI-9 | 引擎的未解决红状态输入面(遥测七键 schema 承载不了,引擎留 `OI9_RED_STATE_INPUT` 隔离缝待裁) | Open items § OI-9 + `runs/20261007T170045Z-report.md` | open,与 S3 落地相关 |
| **D-A** | 【已追认 2026-10-08】= OI-2 的续裁定:落点不可达后怎么走 —— (i) 拓宽 `memory-utils.py` 放开子目录(与该引擎封闭 scope 契约相抵);(ii) 引擎自写子目录(证伪契约 §15,红五道已落地守卫);(iii) 维持今日扁平 session+tag 落点(契约备选 (b) 证据目录并置为另一候选) | `runs/20261007T170045Z-report.md` § 4 + 契约 § Open items OI-2 | resolved-ratified(扁平 session+tag 落点随 S3 落地生效;S3 补丁 :93 即其实现) |
| **D-B** | 【已 void 2026-10-08,前提证伪】引擎与已落地规范文本的两行分歧:`run-determination.py` 的 `green_unproven` 映射(朱印 `:201` 单点) vs 规范文本要求;修法 = 引擎两行 + `tests/contract/test_run_determination_engine.py:1038,1044` 一行 | `runs/20261007T170045Z-report.md` § 4 | resolved-void(SI-3C 证伪:契约 §5.0 值域容纳现行形态;改动会撤销 OI-1 裁定 (a);见收官 run report §1) |
| T-001/T-002/T-003 | goal `command-logic-as-classified-skills` 的三个 Target:T-001 技能内外部标注字段、T-002 技能名称/描述/触发定义、T-003 命令瘦身(命令=入口+委派,细节落技能侧,含「每个技能的输入与产出」子句) | `.specify/goal/command-logic-as-classified-skills/goal.md` § Targets | open(并行团队在执行) |
| SI-0…SI-9 | 自我提升工作流的步骤编号(SI-2 证据限定、SI-3 诊断、**SI-3C 批评后派发**、SI-4 路由、SI-5 落地、SI-6 验证、SI-7 台账、SI-8 对比、SI-9 收束) | `shared/workflow/self-improvement-workflow.md` | active |
| F-A02 | 死信发现:2026-09-11 分流给 improve-skills 的修复从未执行,同一错误主张(per-file 符号链接模型)已从 `skills/create-agent/SKILL.md` 扩散进 `templates/commands/agents.md` | `.specify/memory/feedback/backlog.md`(2026-10-07 行)+ `consume-log.md` | open |
| F-01…F-07 / M-1 / M-2 / D-01 | 自省报告 introspection-20261006T140432Z 的 7 个发现 + 2 个元观察 + `--limit` 截断陷阱;各自分流与处置见报告与 backlog | `.specify/memory/feedback/introspection/introspection-20261006T140432Z.md` + `backlog.md` | mixed(详见 backlog 各行状态) |

| goal.session-driven-self-improvement | goal 于 2026-10-08 经 `goal-utils.py status --set achieved` 收官(用户收官指令 = 判据 2 的人工判定;判据 1 证据见收官 report §5);终态 summary 交付 `.specify/goal/session-driven-self-improvement/summary/` | `.specify/goal/session-driven-self-improvement/goal.md` + `runs/20261008T090000Z-report.md` | closed-achieved |
| S0-command-census / S1-extract-annotate / S2a-contract-conformance / S2b-structure-alignment / S3-command-thinning | 团队 command-logic-as-classified-skills 的 serial 五阶段(S0 命令普查裁定、S1 提炼建技能+标注、S2a 契约齐备、S2b 结构对齐、S3 命令瘦身);S0 完成证据含 25 行裁定(20 新建/5 维持) | `.specify/teams/command-logic-as-classified-skills/team.md` § Dynamic Structure;S0 报告 `runs/20261009T032057Z-report.md` | S0 completed(2026-10-09 run);S1–S3 pending |
| goal.skill-layer-install-separation | S-layer 剩余工作的收编目标：技能内外分层与安装分流落地（源树双层重家、技能对去 .specify 化、镜像/安装/打包两层映射、测试守卫与运行时刷新）；2026-10-09 经用户指令由 command-logic-as-classified-skills 的 run-2 扩展切片剩余批次转换而来；判据 2 条 | `.specify/goal/skill-layer-install-separation/goal.md` | **executed-complete**（2026-10-11:五阶段+收尾闭合全交付并验证,判据 2/2 终验;goal 未正式收官——待用户经 `/speckit.goal`;targets T-001..T-004 的 authored 状态仍在 goal.md） |
| S-A-skill-pair-decouple / S-B-rehome-and-refs / S-C-toolchain-split / S-D-tests-and-guards / S-E-runtime-refresh | 团队 skill-layer-install-separation 的 serial 五阶段链；阶段内以 native subagent **并发派发**（用户 2026-10-09 硬要求）；承接旧团队 B2c/B2e/B3–B7 | `.specify/teams/skill-layer-install-separation/team.md` § Dynamic Structure | **completed**（2026-10-09~11:五阶段全部完成并逐门验证;见 `runs/20261009T181458Z-report.md` 与 `runs/20261011T021003Z-report.md`） |
| goal.post-refactor-mechanism-integrity | 重构后机制完整性目标:大规模重构后原机制不破坏、功能正常;判据 1 条(`.specify/` 除 `skills/` 外全部目录与文件均有流程/脚本支撑,无无主文件);T-001 = 客户项目旧 `.specify` 经新版 `specify init` 升级后仍正常运转(= 已设计迁移方案的 F1–F3 工作容器) | `.specify/goal/post-refactor-mechanism-integrity/goal.md` | active(2026-10-11 创建;见下行团队) |
| team.post-refactor-mechanism-integrity / S1-fix-and-regression / S2-upgrade-sim-verify / S3-criterion-reconcile | 团队 post-refactor-mechanism-integrity 的 serial 三阶段链(S1 修复 F1–F3 与端态回归测试、S2 升级仿真独立验证、S3 判据对账与收口);goal 同名绑定,T-001 唯一 Target(单团队路径,不设 focus_target) | `.specify/teams/post-refactor-mechanism-integrity/team.md`;run report `runs/20261011T144202Z-report.md` | **completed**(2026-10-11:三阶段全过;S3 门 REJECT→返工→复检 PASS;判据 1 独立重推 PASS;T-001 pending_approval 待人工裁定) |
| **c7** | 053 中立性契约 C-7 的窗口钉子用例（`test_neutrality_budget.py::test_c7…`）：六文件在 `BASE_SHA..HEAD` 窗口内不得变动（防预算计量篡改）；**当前为红**——窗口违规文件仅 `tests/contract/test_confirmation_gates_sweep.py`，两处已提交改动均为合法维护（09bd40a9 增运行判定守卫块；cb483a1b 随 git-workspace 合并改 KEEP_LIST 路径），非预算篡改。**归因更正(2026-10-11)**：此前两份 run report 所记「先存基线失败、非本目标」仅对 A/B 口径成立，红自 09bd40a9 起且含本创议自身提交——以本行为准 | `tests/contract/test_neutrality_budget.py` + `.specify/specs/053-machine-decidable-artifacts/contracts/neutrality-budget.md` § C-7 + `notes/pre-change-measurements.md` § 1（锚点） | open——待 053 流程的**刻意重锚/复核裁定**（MUST NOT 静默改写六文件清单或锚点） |
| **G1** | skill-layer S-B governance finding：forbidden 面（`skills/self-improvement/**`、`templates/commands/improve.md`）迁移触碰无 pre-ruling → 由唯一 Meta 依条款自带 remedy 执行 modify 裁定（分层迁移面纳入授权；内容级改动仍需裁定），事后追认并披露 | `.specify/teams/skill-layer-install-separation/team.md` forbidden 修订行（tracked）；完整判定见工作区 `.specify/teams/.work/skill-layer-install-separation/S-B/verification.md`（git-ignored） | resolved-ratified（2026-10-09） |
| **T1** | S-C→S-D 转交张力（**发现标签，非 Target**——与 T-… 轴冲突,以本行消歧）：`templates/commands/clarify.md` frontmatter `skills:[study-project]` 属命令面「对内部技能按名引用」的最后一处 | `runs/20261011T021003Z-report.md` § Result Summary；判定见工作区 `S-D/verification.md`（git-ignored） | resolved（2026-10-11：条目删除 + regen 四副本；「按名→按路径」闭合归零） |
| REC-063-01 | 实现停止门执行证据义务：每次 implement 对每个 stop-gate 记录 `fired`（带门控观察协议证据）或 `not-triggered`（带触发计数），`not-triggered` 与机械在场的触发共存即评审红；冻结制品的运行中修订须带日期内嵌修订注记 | `.specify/specs/063-review-p1-governance/review.md` § 5.2（F1/F2） | open |
| REC-063-02 | 接通 recheck 文件生产者：analyze 的 `dispositioned: covered-by` 标记与下游回答按 C-8 append-only 形态落 `checklists/recheck-<date>-<topic>.md`，每条引用所答 requirement 行 | `.specify/specs/063-review-p1-governance/review.md` § 5.4（F1） | open |
| REC-063-03 | 计划前提执行验证：research 断言引擎/机制行为须带已执行探针（命令+真实输出）；与既有契约测试矛盾的前提在 plan 宪法检查即失败 | `.specify/specs/063-review-p1-governance/review.md` § 5.4（F2） | open |
| REC-063-04 | tasks 校验器前提-基线机械检查：DoD/GATE 前提点名的文件集对冻结失败基线比对，出生即假的前提在生成期失败并列出违规名 | `.specify/specs/063-review-p1-governance/review.md` § 5.3（F3） | open |
| REC-063-05 | 基线收缩侧记账：每次 re-freeze 对上一份冻结清单双向 diff，消失名分类（镜像同步清除/真实修复/抖动）落 `baseline-cleared.txt`，基线记录声明有效窗口与前任指针 | `.specify/specs/063-review-p1-governance/review.md` § 5.3（F4） | open |
| REC-063-06 | verification 日志闭合字段引擎化：`implementation_date`/`post_change_commit` 由验证日志步骤机械填写，`pending` 值不得存活到 wrap-up | `.specify/specs/063-review-p1-governance/review.md` § 5.1（F5） | open |
| REC-063-07 | 观察时修正被证伪的 recipe 字面量：implement 验证步骤同趟修正 quickstart 等已提交 recipe（correction-class，披露） | `.specify/specs/063-review-p1-governance/review.md` § 5.4（F6） | open |
| REC-063-08 | 阶段残留持久载体：未解决残留随阶段收尾**同提交**落 register OI- 行或 feedback backlog 行，带无载体残留的 DONE 不合规；32768 B 预算值做一次显式裁定 | `.specify/specs/063-review-p1-governance/review.md` § 5.4（F7/F9） | open |
| REC-063-09 | 被引 REC- 补登记：为 061 全部被引用 `REC-` id 补 pointer 行；review Handoff 增补「同趟登记前辈被引未登记 id」义务 | `.specify/specs/063-review-p1-governance/review.md` § 5.4（F8） | open |
| REC-063-10 | 跨特性状态钉封闭窗口规则：特性域状态钉（窗口钉/封闭集/字节预算）**创作时**必须声明封闭规则；修订他特性之钉须按 REC-063-08 载体登记日期行 | `.specify/specs/063-review-p1-governance/review.md` § 5.3（F9） | open |
| REC-068-01 | plan 门增契约条款形态检查：pre-analyze-check 在 stage≥plan 时对 contracts/* 跑 clause_extract.form_of()，md-none 或零条款即 error（或 plan U4 逐契约跑 clause_extract） | `.specify/specs/068-exec-quant-feedback-channel/review.md` § 5.3 REC-068-01（F1） | open |
| REC-068-02 | audit-test-budget 分母按 stage-check 收敛：`--stage-check <stage>` 只要求 ≤stage 的 stage-status 完备（或显式 --allow-future-stages），implement 期审计可按构造 exit 0 | `.specify/specs/068-exec-quant-feedback-channel/review.md` § 5.3 REC-068-02（F2） | open |
| REC-068-03 | TDD 重段预算按测试写作/实现边界拆分（或按任务行×实测回合数定段预算），替代再次上调阶段级常数 | `.specify/specs/068-exec-quant-feedback-channel/review.md` § 5.4 REC-068-03（F3） | open |
| REC-068-04 | 镜像同步任务行开最小 `--only` 文件/对前缀处方（能力已在 sync-mirrors.py）；伴生 REC-068-04a = --write 打印前缀外附带重写计数 | `.specify/specs/068-exec-quant-feedback-channel/review.md` § 5.4 REC-068-04（F4） | open |
| REC-068-05 | analyze 修复同步清单须枚举耐久注册表面（features/<ID>.md、features.md）并以 grep 复核修正事实零漏改 | `.specify/specs/068-exec-quant-feedback-channel/review.md` § 5.4 REC-068-05（F5） | open |
| REC-068-06 | 实现段跨特性钉修订归属规则：欠账钉修订须在产生段内同段补齐、提交点名钉+裁决需求行、按 REC-063-10 登记日期行 | `.specify/specs/068-exec-quant-feedback-channel/review.md` § 5.4 REC-068-06（F6） | open |
| REC-068-07 | pre-analyze-check 的 SKIP_HEADING 历史跳过改为日期/记录标记门控，替代裸「修订」子串 | `.specify/specs/068-exec-quant-feedback-channel/review.md` § 5.3 REC-068-07（F7） | open |
| REC-068-08 | coverage-baseline 单一所有者与单一执行点：tasks 阶段 U4 冻结（撤销 implement 期 T002）或 GATE-7 断言显式延期并指向 implement 任务 | `.specify/specs/068-exec-quant-feedback-channel/review.md` § 5.4 REC-068-08（F8） | open |
| REC-068-09 | verification Run 头 branch 字段机械捕获（`git branch --show-current`），禁止继承 trunk 声明 | `.specify/specs/068-exec-quant-feedback-channel/review.md` § 5.4 REC-068-09（F9） | open |
| REC-068-10 | requirements 模板 Status 字段退役或指针化（所有者 = features.md），消除保证过期的第二份状态副本 | `.specify/specs/068-exec-quant-feedback-channel/review.md` § 5.1 REC-068-10（F10） | open |
| REC-068-11 | 无人值守线 wrap-up 引擎步骤归属一次裁定（executor 或 orchestrator）并注记命令模板，取代逐阶段偏离披露 | `.specify/specs/068-exec-quant-feedback-channel/review.md` § 5.4 REC-068-11（F11） | open |
| REC-069a-01 | verification 模板：分母为运行时事件的 SC，`pass` 必须有至少一条运行期观测；否则只能 `partial`/`deferred` + reason | `.specify/specs/069a-flow-classification-docs-gates/review.md` § 5.1 REC-069a-01（F4/F9） | open |
| REC-069a-02 | checklist 模板：out-of-slice 项保持 `[ ]` + disposition；闭合汇总由标记派生（`n([x]) + n([ ]) = total`） | `.specify/specs/069a-flow-classification-docs-gates/review.md` § 5.1 REC-069a-02（F5） | open |
| REC-069a-03 | 接线命令必须带完整范围与 strict：`--path <doc>… [--spec-dir …] --strict`，命令模板与 create-docs R6 同改 | `.specify/specs/069a-flow-classification-docs-gates/review.md` § 5.2 REC-069a-03（F1/F7） | open |
| REC-069a-04 | 两顶帽子下的根解析：脚本位于 `.specify/` 时优先 payload 根，OWNER/DELEGATE 双根候选；新增「执行模板所写命令原文」的契约测试 | `.specify/specs/069a-flow-classification-docs-gates/review.md` § 5.3 REC-069a-04（F1/F2） | open |
| REC-069a-05 | `lookup` 不得回传域外取值：值非法/重复行/行冲突时降级默认类 + 可见标签 + 退出 2 | `.specify/specs/069a-flow-classification-docs-gates/review.md` § 5.3 REC-069a-05（F3） | open |
| REC-069a-06 | 客户端形态的 `check` 要么有真实扫描面与通过态，要么不随包下发（与 069b 交接） | `.specify/specs/069a-flow-classification-docs-gates/review.md` § 5.3 REC-069a-06（F14） | open |
| REC-069a-07 | 切片投影：「逐字沿用」仅在两文本逐字相等时允许；切片补强须用 `slice-strengthened` + 切片锚，或同步父规格 | `.specify/specs/069a-flow-classification-docs-gates/review.md` § 5.4 REC-069a-07（F6） | open |
| REC-069a-08 | 基线仪器前置：冻结时同时冻结枚举单元集与预期检查次数；不可分离则开工前记 `not-evaluated` | `.specify/specs/069a-flow-classification-docs-gates/review.md` § 5.4 REC-069a-08（F8） | open |
| REC-069a-09 | Feature 状态不得由单个切片推进：切片感知状态（`Implemented k/n` 或 Partially Implemented） | `.specify/specs/069a-flow-classification-docs-gates/review.md` § 5.4 REC-069a-09（F10） | open |
| REC-069a-10 | 作者自裁 checklist 需一次独立复核：同一 agent 同时写需求并裁定 ≥N 条清单项时，实现前派一次 fresh-context 只读复核 | `.specify/specs/069a-flow-classification-docs-gates/review.md` § 5.4 REC-069a-10（时间线 6 / F5 / F6） | open |
| REC-069a-11 | 事实一致性门禁补 owner↔owner 面（或在 C-2 写明排除理由）；`expression-gates.md` § 事实一致性 收敛为指针 | `.specify/specs/069a-flow-classification-docs-gates/review.md` § 5.4 REC-069a-11（F12） | open |
| REC-069a-12 | reader 面覆盖 FR-019 所称对象类（S1 形式产物），或收窄 FR-019 的对象清单 | `.specify/specs/069a-flow-classification-docs-gates/review.md` § 5.4 REC-069a-12（F13） | open |
| REC-069a-13 | 冻结基线的数字只留指针：plan/tasks/C-7 不重述失败计数，计数归 `notes/test-baseline-contract.txt` | `.specify/specs/069a-flow-classification-docs-gates/review.md` § 5.5 REC-069a-13（F11） | open |
| REC-069a-14 | 调用点表区分「命令执行的面」与「流程执行的面」：六面归表达类流程，W1 行只登记命令可执行的四面 + 评审指针 | `.specify/specs/069a-flow-classification-docs-gates/review.md` § 5.4 REC-069a-14（F15） | open |
| REC-069b-01 | Success Criteria 必须带 falsifier（必须变红的变异），不能只有 measurement source | `.specify/specs/069b-isomorphism-migration-metrics/review.md` § 5.1 REC-069b-01（F1） | open |
| REC-069b-02 | 验证记录的值域须机器可解析：`*_commit=` 只接受 SHA 或 `null` + reason | `.specify/specs/069b-isomorphism-migration-metrics/review.md` § 5.1 REC-069b-02（F7） | open |
| REC-069b-03 | Feature 索引 `Last Updated` 只作指针（日期 + 切片状态 + 详情链接），不追加叙事 | `.specify/specs/069b-isomorphism-migration-metrics/review.md` § 5.1 REC-069b-03（F11） | open |
| REC-069b-04 | 需独立判定者的 SC 必须在 plan 阶段就有执行载体（任务行或带 owner 的 deferred） | `.specify/specs/069b-isomorphism-migration-metrics/review.md` § 5.1 REC-069b-04（F10） | open |
| REC-069b-05 | 提交门须 diff 校验 tasks/plan 声明的禁改面，未登记的范围扩张必须补任务行 | `.specify/specs/069b-isomorphism-migration-metrics/review.md` § 5.2 REC-069b-05（F2） | open |
| REC-069b-06 | SC 与其契约的测量主体集必须一致；收窄须同批改 SC 文本 | `.specify/specs/069b-isomorphism-migration-metrics/review.md` § 5.2 REC-069b-06（F4） | open |
| REC-069b-07 | 状态推进按 owner 协议执行；任务行不得写「状态翻转归别的 owner」 | `.specify/specs/069b-isomorphism-migration-metrics/review.md` § 5.2 REC-069b-07（F3） | open |
| REC-069b-08 | 仪器-对象适配在 plan 期校验：通道看不到对象即不得入基线表；`/speckit.analyze` 须写运行判定记录 | `.specify/specs/069b-isomorphism-migration-metrics/review.md` § 5.3 REC-069b-08（F6） | open |
| REC-069b-09 | 迁移快照须至少一个刷新后执行 `.specify` 载荷的冒烟，并记录样本代表性 | `.specify/specs/069b-isomorphism-migration-metrics/review.md` § 5.4 REC-069b-09（F5/F12） | open |
| REC-069b-10 | 冻结样本时同时冻结运行环境契约（解释器/PYTHONPATH/变量/node 集），冻结时先冒烟 | `.specify/specs/069b-isomorphism-migration-metrics/review.md` § 5.4 REC-069b-10（F8） | open |
| REC-069b-11 | implement 收口须对账 checklist 的 `verify-in-implementation` 开放项（关闭或转交） | `.specify/specs/069b-isomorphism-migration-metrics/review.md` § 5.4 REC-069b-11（F9） | open |
| OI-069b-01 | 客户侧分类副本的「漂移检查」没有 owner 与仪器（FR-008 只覆盖框架源 ↔ 镜像）；069b 的 CHK025 因此判 `out-of-slice` 并保持 `[ ]`，不冒充完成 | `.specify/specs/069b-isomorphism-migration-metrics/checklists/isomorphism-migration-metrics.md` CHK025 + 同切片 `verification.md` § Checklist 收口对账 | open（owner = 后续修订 FR-008 的特性，尚未立项；解除条件 = 为该检查指定 owner 与仪器，或明确豁免） |
| REC-071-01 | `receipt` 从它拿到的那份记录头部继承 `base`/`head`，不再自解析区间；文档化四步在此之前必须带 `--spec <feature-dir>`，并以一条契约测试同时钉住文档行与头部字符串 | `.specify/specs/071-review-code-integration/review.md` § 5.3 REC-071-01（F1） | open |
| REC-071-02 | trunk 档从真正包含 `HEAD` 的远端解析（或本地默认分支），不再无条件信任 `refs/remotes/origin/HEAD`——本仓 `origin` 是上游 fork，该档解析到落后 1180 提交的上游 merge commit；同批修 FR-004 第二档并加 decoy-origin 夹具测试 | `.specify/specs/071-review-code-integration/review.md` § 5.3 REC-071-02（F2） | open |
| REC-071-03 | 阶段收口的状态一致性检查：`features.md` 状态 vs `tasks.md` 开放行 / `verification.md` SC 行 / 最新评审记录，不一致即失败；由 implement 收口步骤调用 | `.specify/specs/071-review-code-integration/review.md` § 5.4 REC-071-03（F4） | open |
| REC-071-04 | `test-evidence/implement-stage-status.jsonl` 要么给它一个读者（一段一行，缺行即红），要么退役；无读者的存储只会静默积洞 | `.specify/specs/071-review-code-integration/review.md` § 5.3 REC-071-04（F6） | open |
| REC-071-05 | 覆盖率回执须区分「不是代码」与「没评审」：收窄为代码路径子集 + 非代码余量单列披露，或新增 `not-code` 逐文件裁决（既不计覆盖信用也不作废通过）；保持 C-74 单一计数来源不变 | `.specify/specs/071-review-code-integration/review.md` § 5.4 REC-071-05（F3） | open |
| REC-071-06 | 每条 Success Criterion 标注评估它的阶段：SC-001 拆为 implement 可判定的两载体相等性 + review 阶段的可组合运行观测；验证日志模板增一列 | `.specify/specs/071-review-code-integration/review.md` § 5.4 REC-071-06（F7） | open |
| REC-071-07 | quickstart 的字面选择器必须在写入时对仓库校验（F 的 `src/legacy/**` 在本仓匹配为空，字面命令给出与预期相反的 `verdict=pass`） | `.specify/specs/071-review-code-integration/review.md` § 5.5 REC-071-07（F5） | open |
| REC-071-08 | 技能正文不重述脚本强制的阈值：`>400` / `>800` 只留在 `size_guard`，`SKILL.md` 改为指路 | `.specify/specs/071-review-code-integration/review.md` § 5.5 REC-071-08（F8） | open |
