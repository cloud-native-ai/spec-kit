# Contract: goal-based 创建分支(create 面)

**Spec**: [requirements.md](../requirements.md) FR-001..005, FR-010, FR-013, FR-014  
**Surface**: `templates/commands/team.md`(create 路由)× `skills/create-team/{SKILL.md, references/create-mode.md}`  
**Authority**: 概念锚 `shared/definitions/goal-definitions.md`(链接,不复述);行为裁决在 `scripts/python/goal-utils.py`

## C-1 分支识别(确定性,零语义猜测)

- create 模式 MUST 先运行 `python3 scripts/python/goal-utils.py list --json` 获取 archive slug 全集;入参 token 与某 slug **精确匹配**(或为指向其 `goal.md` 的路径)→ 向用户确认"基于已定义 goal <slug> 创建"后进入分支。
- 近似不匹配(大小写/连字符差异)**不构成命中**;无命中 → 走既有自由文本流程,行为与引入前一致(FR-014 零回归)。
- 匹配判定 MUST 由引擎枚举结果驱动,MUST NOT 由 agent 凭记忆断言。

## C-2 定义加载与两类拒绝

- 进入分支后 MUST 经 `parse_goal`(`goal-utils.py`)读取:objective、criteria(含 `None provided.` 缺失态)、status、targets、history,并复述给用户确认。
- **悬空引用**(用户指名但 `list` 无此 slug):输出以 [[STR-003]] 前缀(逐字 `goal 未定义:`)的报错,指向 `/speckit.goal create`;零产物、零写入,MUST NOT 降级为内联 goal 创建。
- **终态 goal**(`achieved`/`abandoned`):显式报出终态并拒绝进入;MUST NOT 创建团队。两类拒绝均不需要用户确认即可执行(它们是停止,不是写入)。

## C-3 分析披露(四要素,建议非门禁)

创建前 MUST 呈现,每项附理由:

1. **维度**:goal 对象所处平面(框架自身/代码库收敛/交付能力运行态/…)——链接概念锚 Goal Dimensions;
2. **判据覆盖**:criteria 逐条列出,或显式声明缺失(`None provided.`,MUST NOT 臆造);
3. **既有 Target**:open/done/dropped 分类清单(复用基线,见 decomposition-proposal 契约 C-4);
4. **可达成性判断**:单团队短期可达成 vs 宽泛需分解——结论 + 依据。

结论是建议:最终单团队/分解路径由用户裁决;用户强行选单团队不被阻止,但裁决留痕于确认预览。

## C-4 成组建队(FR-010, FR-013)

- 分解批准后(或复用基线成立时),每个 open Target 对应一个团队;全部声明同一 `goal_slug`;`focus_target = T-<nnn>`(该团队对应切片)。
- 每个团队的 roster/pattern 派生:MUST 以其 **Target 语句**为输入走既有机制——`python3 skills/create-team/scripts/match-team-preset.py --goal "<Target 语句>" --json`(preset 强匹配推荐复用)+ pattern 决策树(`references/patterns.md`),派生理由入确认预览。
- slug 缺省派生 `<goal-slug>-t<nnn>`(小写、三位零填充,如 `log-split-t003`);MUST 对 `.specify/teams/` 现存目录查重,冲突即改写并回显;用户可在确认门禁改名。
- 确认门禁一次性披露:分支判定、分析结论、路径决策、提议集或复用声明、territory 划分提议(含 verify 脚本 verdict,见 creation-territory-disjoint 契约)。
- 同一 `goal_slug` 下已存在团队(扫描 `.specify/teams/*/team.md` frontmatter)时:MUST 检测并向用户提议复用既有团队或移交 `/speckit.goal coordinate`;MUST NOT 无提示重复建队。

## C-5 落盘与不变量

- 写入面仅限 `team.md`(含 `focus_target` 字段)与其 territory 键;`goal.md` 零写入(见 decomposition-proposal 契约 C-5)。
- 内联 `goal` 字段(如保留)仅为可读性渲染;与定义不一致 MUST 显式报出供裁决——定义权威(`references/goal.md` 既有规则,不改)。
- 未匹配 archive 的 create、未声明 `goal_slug` 的存量团队、run/modify 模式:行为零变化。

## 验证

- 契约测试 `tests/contract/test_goal_team_creation.py`:模板/参考文档子串断言(C-1..C-4 关键句)+ `PER_TOOL_COPIES` 六副本一致性。
- 集成面(实现期):临时 repo root 构造 archive goal → 走 create 编排 → 断言 team.md 产物(`goal_slug`/`focus_target`/territory)与两类拒绝的零产物。
