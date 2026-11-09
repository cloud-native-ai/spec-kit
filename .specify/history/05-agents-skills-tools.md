# 主题：Agent → Skill → Tool 分层与命令-技能委派（T1）

范围：agent 注册与派发、skill 内外部两层、命令薄壳化、probe/handler 编译链、引擎工具治理。
覆盖 **41 个** Qoder 会话（2026-10-05 → 2026-11-10）；sid 在文内逐条引用，完整清单见文末。
关联主题：[[06-anchoring-goal-team]]（目标/团队编排）· [[09-memory-state]]（引擎状态与存储）· [[03-framework-mechanics]]（命令/模板机制）· [[00-cross-cutting-lessons]]

## 1. 关键决策与理由

- **技能两层布局（two-hats layering）**：source 分 `skills/{external,internal}/`；runtime external 扁平注册、internal 嵌套不注册——"不可见 = 不注册为技能"，而非"文件不存在"，目的是遏止客户 agent 技能列表膨胀。判定只看**操作性耦合**（skill 逻辑是否读写 `.specify` runtime/引擎/shared 文档）；`skill_id` 头、standalone runtime-gate、Feedback step 这类样板不计入，否则规则退化为"全部 internal"。（`e9450ef0`、`86dd0ae8`、`8b32d7cd`、`48099f17`）
- **命令薄壳化 + 行为下沉技能**：S0 普查 25 命令（26 减去他线 `improve.md`）→ 20 sink-and-create（1 条件性）/ 5 maintain；25 个命令模板收窄为 frontmatter + 生命周期 + 薄委派（−2,368 行）；`/speckit.goal` 禁令改述为"不得**直接**写，`goal-utils.py` 是唯一写路径"。新技能只在无既有覆盖时创建（`run-skills`/`run-team` 从 team 命令 ~40 行内联提取，要求 behaviour parity、zero loss）；修改面复用 `improve-skills`/`merge-skills`。（`e9450ef0`、`28144a1d`、`8b32d7cd`）
- **Probe/Handler 编译期派发**：1 probe ⇒ N handler；`Probe Class × Object` + `HandlerBinding` + `Handler`（六字段封闭集、`h-` 前缀）；`compile-embeds` 为每单元生成单一 AUTO-GENERATED `## Wrap-up`；零 handler 单元不输出段；micro-probe 保持 code-first，仅以指针条目登记于非实体目录；宿主项目只读。（`06db3fb9`、`4f60c597`、`eedffe8a`、`f2f7adbe`）
- **引擎增补纪律**：新 engine 必须进入 `_ENGINE_SIBLINGS` 显式元组并进 probe registry（4 表行 + 每面孔 +1 行）；动作名避开既有命名（feedback 的 `list` 冲突 → `list-records`）；每个功能型引擎回答 `--help`/`--version`，动作集为封闭清单（`goal-utils` 9→10 加 `run-checks`、`EXIT_BLOCKED=5`；`validate-tasks` 标签 6→10）。（`4f60c597`、`a6a25181`、`eedffe8a`）
- **技能合并必经 `merge-skills`**（用户裁决）：带提交的继承记录 `references/merge-provenance.md` + 冻结基线（`coverage_probe.py --emit-baseline`）+ `provenance_check.py`；清理阶段以"记录已提交"为门，不以 probe 绿为门。六 `draw-*` 合并为 `draw-diagram` 的 `references/types/<engine>/`；四 `git-*` 合并为 `git-workspace`。（`6313ff57`、`e9450ef0`）
- **Agent 注册链**：`create-team` 经 `create-agent` 实例化 seat（放弃 init 安装帧——与 `{{PLACEHOLDER}}` 拒绝冲突，也放弃 `seat_kind` 判别器）；`specify render-agents --ai <tool>` 窄子命令复用既有 renderer（uv/pipx 隔离使 in-script import 不可行，init 重跑过重）。（`e059c728`、`9c57a1ed`）
- **并发载体 = fork 模型**：qodercli 单进程单 CPU；进程内 subagent 在并发下不稳定（宿主重启一次杀掉全部四个、CPU 饱和）→ 一律 fork：`stage-runner.sh` + `qodercli -w <repo> --permission-mode auto -p`（stdin、stream-json、pid/status/heartbeat/live-log、哨兵末行、detached），异构 CLI 用 subprocess。（`48099f17`）
- **测试入口单一化**：一切框架测试经 `scripts/bash/run-tests.sh`（xdist `-n <effective> --dist load`），裸 `python3 -m pytest` 禁止并有 guard 测试；>10 s 的 8 个测试走 opt-in `slow` marker（用户选"保留标记"而非删除）。（`48099f17`）
- **命令复杂度分类**：Simple 命令不承载 `## Wrap-up`/probe 单元，wrap-up 由 skill 侧 handler 承担（`humanize` 首个 skill 侧 `h-docs-sync-eval`）；分类由 027 owner 规则 (a)(b)(c) 判定，登记 73/74 单元 = 23 Complex 命令 + 50 skills。（`544f490f`、`da741035`、`0250abd1`）

## 2. 可复用经验 / 踩坑

- **compile 顺序固定**：`registry 对同步 → 源侧 compile → regen → feature 作用域 sync`。引擎读 `.specify` 镜像 registry；镜像未重投影时 compile 会产出 `.specify/.specify/...` 并把"绿色"校验变成真空（两处 validate 曾因此为假绿）。（`eedffe8a`、`da741035`、`df0d4308`、`2633f12c`）
- **编译出的 Wrap-up 面孔长期缺引擎参数**（`--run-id`/`--complexity`/`--review`，exit 2），跨 71→74→79 单元反复出现；修复方向是让渲染从引擎 `args-manifest` 读取，而非逐次手补。（`df0a6be3`、`544f490f`、`0250abd1`、`da741035`、`6fbbb89d`）
- **`sync-mirrors --only` 粒度陷阱**：`--only scripts` 是 scope 级，会拖带继承漂移（一次 25 个、后来 108 个）；`--only skills` 对 `skills/internal` 是静默 no-op（对是 `skills/external`/`skills/internal`）。（`27383836`、`2633f12c`、`0f63f87a`）
- **注册/名单类 guard 滞后**：`INTERNAL_SKILLS` 36 vs 实树 38（`run-skills`/`run-team` 无 guard）；扁平 glob `skills/*/SKILL.md` 在两层布局下匹配 0（54 个技能）或制造真空绿。（`bd6dcf6f`、`fe7dafff`、`6313ff57`）
- **宿主派发注册表在会话开始快照**：新渲染的 seat 下一会话才可派发（`dogfood-executor` 先例；`SDD Analysis Worker` 因 `display-color: teal` 被配置加载器拒绝，改 `cyan` 后 24 个 active）；当次用 `general-purpose` 退化并记录虚拟派发。（`e9450ef0`、`9857e730`、`9c57a1ed`）
- **mutation 用删除形态**：子串断言对后缀追加免疫（`seat instantiationz` 仍绿）；先 grep 标记词（`team-scoped` 命中 `team-scope` 的假绿）。（`e059c728`）
- **`render_agents_for_tool` 对未知 tool key 静默返回 `rendered: 0`**（`.github/agents` 的 key 是 `copilot`）——空成功必须当缺陷报告。（`a6a25181`）
- **`cp`/`rm`/`mv` 交互别名静默 no-op 且可能返回成功**；root 属主文件用"临时文件 + 同目录 `mv`"原子替换（rename 只需目录写权限）。（`e059c728`、`a3d3ec0a`、`eedffe8a`、`df0d4308`）
- **测试审计的系统性缺陷**：自指断言（grep 自己引入的字面量）、`or True`、mirror-parity 家族重复、test-about-tests、completed-feature pin、慢构造（真实 worktree 队列、venv 安装、`time.sleep(1.1)`、47 KB 的测试专用 driver 模拟器）。（`5fea4a1e`、`bd6dcf6f`、`dc1d9296`、`fe7dafff`、`a8412de2`）
- **临时目录纪律**：scratch 只允许落在 `.specify/.tmp/` 等受 sanction 根；`$HOME/.cache/`、裸 `/tmp`、repo-root `tmp/` 都被记录并清理。（`9857e730`、`111683d8`、`a9bcef84`）
- **`collect-history.sh` 自动识别可能返回 null** → 用 `QODER_CLI`/`QODER_PID` 判定并显式 `--tool qoder`。（`db0b0717`）

## 3. 未完成 / 待办

- **Wrap-up 编译参数生成源**未修（063 F4 谱系；多次以手工参数绕行）。
- **注册与文档漂移**：`feedback-utils.py --action probes` 已迁 `probe-utils.py`，registry 行 028 与 `features/028.md` 仍教旧动作；`INTERNAL_SKILLS` 36→38；`058` 声称的 `sdd-executor` 表面已不存在。
- **REC 积压**：REC-071-*/REC-072-*、REC-A1（per-tool renderer `rewrite_paths` 与 test_i11）、REC-W1/W4 等已登记未执行。
- **sdd-* 产物治理**：housekeeping 报告落 `.specify/memory/housekeeping/<UTC>-<mode>.yaml`、driver 本地 brief 落 `.specify/.tmp/sdd-loop/tmp/<line_id>/`，root YAML 已 `git mv`；旧表面待清。
- **技能分类迁移**：`archive-session`/`code-review`/`manage-agents`/`study-project` 暂列 internal；`study-code` 已 internal→external，references 与发现面待跟进。

## 4. 关键交互流程

- **命令普查 → 分层落地**：census(S0) → 分类 v2（32 实体：internal 15 / external 17）→ S1 技能包（20/20）→ S2 判分/补丁（46/46、8 patches）→ S3 薄壳化 → mirror sync/regen → 123 个契约失败重指向而非弱化。（`e9450ef0`、`8b32d7cd`）
- **Probe 系统落地**：回顾 → 1⇒N 设计 → 用户"使用3 走完成SDD流程" → requirements→clarify(Q1–Q6)→plan→tasks→implement（38/38，跨 3 次 compaction）。（`06db3fb9`）
- **新引擎/记录通道**：requirements（挂接既有 wrap-up handler，零新模板面）→ plan → tasks（red-first）→ implement → closure；`exec-quant`/`feedback package`/`measure`/`status-digest` 均此形态。（`4f60c597`、`eedffe8a`、`27383836`、`9857e730`）
- **Trainee/coaching 运行**：`/speckit.status`、`/speckit.history` 作为 Trainee 由单 subagent 执行，主会话记录偏差；executor kind 双名单解析，跨类歧义 fail closed。（`af6d3fc1`、`a9bcef84`、`48099f17`）
- **并发批派发**：team run → 4×5 并行 skill-author 批 → 独立 contract-checker 门 → Meta 落地 + sync/regen。（`8b32d7cd`）

## 5. 用户 ↔ 模型分歧点

- 用户裁决"git-* 合并必须经 merge-skills 技能"、"不可见 = 不注册为技能"——模型无异议，直接改设计。（`28144a1d`、`e9450ef0`）
- 用户推翻"critique 单独建 spec"（"适合当前的goal高度契合"）→ 作为 goal 的组件落地。（`9c57a1ed`）
- 用户前提被证伪：`docs/git-workflow.md` 声称不存在（实际存在、mode 600）；"单分支开发"与实际 trunk+短分支不符 → 菜单术语改名"临时分支"。（`06db3fb9`）
- 用户以框架阈值变更替代拆分（082 任务上限 40→60），模型记录张力并执行。（`0f63f87a`）
- 用户质问"为什么没有按照sdd流程进行"——模型跳 U0–U6 直接编辑；根因是缺入口路由 guard，已写入 skill（U0 声明 + Hard Requirement 7）。（`34080ca9`）
- 用户选 `slow` 标记而非删除 >10 s 测试；`/speckit.feedback console` 被模型读作 consume 的 near-miss 并披露。（`48099f17`、`a3d3ec0a`）

## 覆盖 sid（41）

`0250abd1` `04e3f86b` `06db3fb9` `09e7b15b` `0f63f87a` `111683d8` `27383836` `28144a1d` `34080ca9` `3b8d316b` `3e8cf04f` `46290991` `48099f17` `4c000af3` `4f60c597` `544f490f` `5ea25dfb` `5fea4a1e` `6313ff57` `644a1597` `6b6a829d` `6fbbb89d` `7896e937` `825aa3a5` `86dd0ae8` `8b32d7cd` `9857e730` `9c57a1ed` `a3d3ec0a` `a4475aa8` `a6a25181` `af6d3fc1` `c218f73c` `d01a3852` `da741035` `df0d4308` `e059c728` `e9450ef0` `eedffe8a` `f2f7adbe` `fe7dafff`
