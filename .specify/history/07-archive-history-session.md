# 主题：Archive + History + Session（T3）

范围：`/speckit.history` 知识库与非一次性（Non-Disposable）记录治理、归档不删除（archive-not-delete）与巩固评审、会话/驾驶（driver）证据与提交纪律。
覆盖 **41 个** Qoder 会话（2026-10-06 → 2026-11-10）；sid 在文内逐条引用，完整清单见文末。
关联主题：[[04-history-command-origin]]（命令出生证明）· [[06-anchoring-goal-team]]（重命名债）· [[09-memory-state]]（状态证据）· [[00-cross-cutting-lessons]]

## 1. 关键决策与理由

- **History KB 形态**：主题聚合 + 五维度（决策/经验/待办/流程/分歧）+ 增量 manifest（完整 uuid；短 id 不匹配） + 一次性 `.work/` 草稿；重跑只处理新增会话并合并进既有文档。（`db0b0717`、`c8faa376`；参见 [[04-history-command-origin]]）
- **Non-Disposable 机制**：一次盘点 861 个 open entry，五类——`orphan-path` 661 / `renumber-live-binding` 120 / `status-unreadable` 54（53 HIGH + 1 CRITICAL）/ `false-closed-set` 10 / `deferral-marker` 16；处置二分 `correct` / `exempt`。确认粒度是**封闭三值** `group`/`item`/`none-of`——不存在"一次确认 = 全部执行"。（`c8faa376`）
- **四段 seam**：回顾 → 设计 → 用户确认 → 执行；Step A.3 要求 before/after 双快照字节一致（两次内容哈希相同）才可进 Step B；零写证明靠快照而非声明。（`db0b0717`、`c8faa376`）
- **波次纪律**：单波单一类、有界。G2 `false-closed-set` 10/10 原地修正（open 918→908，−10 精确）；G4 9 条活绑定修正、96 条作为 owning-feature registry 绑定保留（重写会伪造当前陈述）；W5 应用 153 条修正（736→599，实际关闭 137）；G1/G5 直接 BLOCKED 而非凑数；G3 736 条全分类后因 live bucket 153 > 150 上界而停手——0 修复、0 声称。（`6f34ad6c`、`1b96db87`、`ca4d659f`、`38ebae8c`）
- **Archive-not-delete**：归档目录 `.specify/archive/specs/` + `CONSOLIDATION-LEDGER.md`（11 个目录：003/007/008/017/022/046/054/066/069a/069b/092）；回滚说明 = `git checkout <sha-before-deletion> -- <path>`——历史就是备份。Consolidation 评审 G1–G9 的 verdict 只有 keep/merge/archive/delete，`delete` 恒为 0。（`48099f17`、`2e79c944`、`61298504`、`e2c7372c`）
- **会话与运行记录**：E-7 证据四段（readings / paths / corpus / dispositions）；run record 一条一文件；closeout 默认 `ask`，一 run 一 receipt，首败即停，不 force-push；`Closeout`/`Closeout remotes` 成为 `.specify/workflow/git.md` 的受管字段。（`48099f17`、`c8faa376`）
- **Watch 模型**：完成只认正证据——exit record → sentinel → PID → heartbeat；静默、消失、`pgrep` 为零都不是完成。状态机 DONE/INCOMPLETE/ANOMALY/FAILED/DEAD/TIMEOUT/NO_SIGNAL/RUNNING，单目的地 U4/U5。阶梯：long-poll 窗口（默认）→ host notification（仅补充，不得结束 driver 会话）→ interval polling；窗口过期返回 RUNNING，只有 stage deadline 才 TIMEOUT；liveness = PID 文件 + `kill -0`，`pgrep` 只作布尔回退；hook 是提前信号不是完成判定；FIFO 用 `read <> fifo`（`read < fifo` 在 open 时即阻塞）。（`34080ca9`、`f2f7adbe`）
- **提交/状态纪律**：pathspec 精确提交（`git commit -m msg -- <paths>`）；state spine 只 append 不 replace；未 push 的 HEAD 使可达性 UNRESOLVABLE——报告用绝对路径 + `git show <sha>:<path>`，不伪造 URL。（`e059c728`、`db0b0717`、`d22e136f`、`f556a5f4`）
- **sdd-* 产物归档**：housekeeping 报告 → `.specify/memory/housekeeping/<UTC>-<mode>.yaml`；driver 本地 brief → `.specify/.tmp/sdd-loop/tmp/<line_id>/`；root YAML `git mv` + guard 测试。（`48099f17`）

## 2. 可复用经验 / 踩坑

- **波次机制坑**：行插入造成锚点级联（049 插入使两条 `orphan-path` 锚点 +8 行）；`entry_id` 丢弃 `.specify/` 前缀——用 baseline 的 `evidence_refs.path`；引擎 C-703 按 `entry_id` 合并同行读数，掩掉同行的第二个 orphan token——这正是 W5 的 16 条残余；`:line` 后缀 token 替换路径但保留后缀；`--freeze` 只打印（需重定向进 baseline 文件）；baseline header 用 repo-relative corpus-root；freeze 只覆盖一个名字，parse-doubt 不是 coverage item；上游 merge 在 freeze 后引入新名字（`8edd955d` 带入 `085#C-014`）。（`ca4d659f`、`63f60627`、`5059aff0`）
- **有界纪律的反面**：live bucket 153 超过 150 上界时，正确动作是"分类完成即停"，不是"顺手修完"；下一波按逐条计划执行。（`38ebae8c`）
- **BLOCKED 是诚实结论**：G5 51/52 无 verdict——checker 的 closure-verdict 输入契约晚于 51 个 dated spec；43 个缺 `**Path**:` 标记（按 C-804 归 `validate-requirements.py`）；17 个需从未做过的 ladder 测量、20 个需新 smoke + 逐 SC 判断——拒绝编造测量阶梯。G1 的豁免机制对 `deferral-marker` 惰性，E-3 fact 形状被 declaration schema 拒（`kind: record` 不在封闭集，exit 2）。（`dd3b7b4e`、`6f34ad6c`）
- **状态/登记矛盾谱**：090 `Implemented` 但 closure `block`；092 叙述"已并入 090"而行尚开；056 header `Planned` vs body/registry/verification `Implemented`（只修 header）；073 仅 requirements 就标 `Implemented`；089 `Implemented` 而 closure-suite 111 失败 vs 34 基线；058 `Implemented` 但 8/9 SC `partial` + T031 deferred；006/009 10/13 任务未勾而 registry 说 Implemented——**证据缺口 ≠ 交付缺口**，判读要分开。（`208e88b8`、`3b8d316b`、`c2287715`、`a3821ef3`、`61298504`）
- **Consolidation 判读**：spec 目录号 ≠ registry 号（020→006、031→032、035→040、045→047…），映射按 spec 路径；git 日期不是陈旧信号（16 个 spec 共享 `c4605da6a` sanitize 提交日期）；registry 行巨大——只解析 ID/status/links；任务计数被 legend 文本污染——锚定行模式。（`61298504`、`c2287715`、`1f5f64d1`）
- **并发写者归因**：同树并发会话写被跟踪的 `.specify/memory/trigger/index.json`（`sman-2`）；嵌套 worktree self-location 陷阱让 repair-wave 套件改写了 trigger index——只判 committed HEAD；`hist-wave1` fork 运行中把 `SKILL.md` 从 `UU` 翻成 `M.`——未触碰、只记录。按 mtime + `git log` 归因后再决定信用/否定。（`dc1d9296`、`644a1597`、`a4475aa8`）
- **`collect-history.sh` 的识别边界**：工具自动识别可返回 null → `QODER_CLI`/`QODER_PID` 判定 + `--tool qoder`；Qoder store 104 pending / ~211 MB，与 claude 纪元 manifest 0 重叠；1.46 MB 的 review JSON 必须程序化 digest，绝不整载。（`db0b0717`、`c8faa376`）
- **`.tmp` worktree 噪声不是活目标**；basename 匹配太噪——用后缀式重定位匹配；被分析工作区的惯例路径不得重写（4 条 `030-summarize-project` 条目指向分析对象的 `docs/overview.md`）。（`38ebae8c`）
- **归档评审的悬空指针**：069b/092 归档后留下规范指针；070 的 review gate 说 closure blocked，verification 却说 unblocked 并在 `ca8040f5` 合并，无记录解决 F1/F2。（`644a1597`、`1f5f64d1`）

## 3. 未完成 / 待办

- **W5 的 16 条同行残余**：引擎按 entry_id 合并所致，已点名保留开放。（`ca4d659f`）
- **96 条 owning-feature registry 绑定**：合法当前陈述，保留开放并带逐条证据；引擎过度近似（96/105）作为框架观察记录。（`1b96db87`）
- **G1/G5 机制修复**：豁免通道接线（`non-disposable-definitions.md` § Exemption vs 引擎）、E-3 fact 与 declaration schema 对齐、G5 的 closure-verdict 输入契约或 51-spec schema 迁移——都需要机制决策，不是执行者。（`6f34ad6c`、`dd3b7b4e`）
- **090/092 裁决与 092 清理**；`features/001.md`/`003.md` header 修复；057 的 goal 路径刷新。
- **closeout 未执行**：策略 `ask`，序列展示后等用户；多数波次 commit 未 push（push 是独立显式动作）。

## 4. 关键交互流程

- **`/speckit.history` 六步**：识别工具与项目 → `collect-history.sh` 提取干净会话 → 逐会话五维提炼（大者并行 subagent）→ 主题聚合合并 → manifest 更新 → 报告。本文件所在的五线程聚合就是该命令的一次执行。（`db0b0717`；[[04-history-command-origin]]）
- **治理波次模板**：fresh baseline JSON → 分类（引擎谓词 + 人工判读）→ 有界修正 → after JSON → E-7 四段证据 → 哨兵；`not_closed.open` 的前后差必须等于实际关闭数（G2 −10、G4 −9、W5 −137）。（`6f34ad6c`、`1b96db87`、`ca4d659f`）
- **Consolidation 评审**：inventory → registry/证据/详情三角 → 陈旧扫描 → 逐条 verdict 表 → `REV-G*-DONE`；只读，动作留给后续。（`61298504`、`e2c7372c`、`c2287715`、`2e79c944`、`3b8d316b`）
- **Driver/watcher/closeout**：U0–U6 → `watch-target.sh`（`--once`/`--self-test` 16 例、4/4 e2e mock、55 契约测试）→ 完成证据链 → closeout receipt。（`34080ca9`、`f2f7adbe`、`48099f17`）
- **sdd 产物治理**：报告/简报改道受管目录 + guard 测试 + root YAML `git mv`。（`48099f17`）

## 5. 用户 ↔ 模型分歧点

- 检测器发现 wrap-up 提交污染（`git add <paths> && git commit` 提交整个 index，`09bd40a9` 吞入 52 个外部暂存文件），用户裁决"一起提交"保留原样。（`e059c728`）
- 用户要求 `tmp/` 的根因解释；模型迁移到 `~/tmp/spec-kit/legacy-root-tmp-2026-10-28/` 但不删除，并在新纪律里禁止 repo-root tmp。（`c218f73c`）
- 历史完整性压力下，模型宁可 G1/G5 BLOCKED 也不把未测量的条目写成已修复；`none-of` 的旧裁决被继承而非重问。（`6f34ad6c`、`dd3b7b4e`、`db0b0717`）
- push 始终是用户显式动作：多数 session 结束时 commit 未推送，`origin` 只读（upstream github/spec-kit）。（`28144a1d`、`e059c728`、`2b259011`）
- 用户追问"是否按 SDD 流程"后，模型把"流程不可替换"写进入口 guard（跨线程，见 [[05-agents-skills-tools]]）。（`34080ca9`）

## 覆盖 sid（41）

`03be6910` `08e0989e` `0f63f87a` `1b96db87` `1f5f64d1` `208e88b8` `2a7e498f` `2e79c944` `302477d1` `34080ca9` `38ebae8c` `3b8d316b` `46290991` `48099f17` `544f490f` `5ea25dfb` `61298504` `62a1b0b1` `6f34ad6c` `7896e937` `840faac8` `86dd0ae8` `8ac9bcc5` `8f473c19` `99912504` `a3821ef3` `a3d3ec0a` `b15cd656` `c218f73c` `c2287715` `c8faa376` `ca4d659f` `cf3fe393` `d01a3852` `d22e136f` `d28dbd53` `db0b0717` `dd3b7b4e` `df0a6be3` `e059c728` `e2c7372c`
