# Profiles 仓库反馈批次（12 条，2026-07-31 → 2026-08-05）

> **处置(2026-08-12)**:外部项目(profiles 仓库)反馈批次,单元(dingtalk-follow-up/aliyun-workspace 等技能)均不存在于本仓库,且引用 zip 缺失——在本仓库不可处置,归档留痕;如需处理请在 profiles 仓库执行。

**来源项目**: /Users/liuqiming.lqm/project/profiles
**打包文件**: [feedback-20260805T055914Z.zip](./feedback-20260805T055914Z.zip)（12 条条目 + MANIFEST.md）
**上次提交**: 2026-07-31T08:40:05Z
**上游 commit**: 127753962c10553206b779ffefed8c7723e01686

## 条目清单

| 条目 | 单元 |
|------|------|
| 20260801T121416Z-skill-draw-plantuml | skill:draw-plantuml |
| 20260801T151159Z-skill-improve-skills | skill:improve-skills |
| 20260801T152754Z-skill-improve-skills | skill:improve-skills |
| 20260801T154343Z-skill-dingtalk-follow-up | skill:dingtalk-follow-up |
| 20260801T162013Z-skill-dingtalk-follow-up | skill:dingtalk-follow-up |
| 20260804T173817Z-skill-create-skills | skill:create-skills |
| 20260805T022547Z-skill-create-skills | skill:create-skills |
| 20260805T022957Z-skill-improve-skills | skill:improve-skills |
| 20260805T024400Z-skill-improve-skills | skill:improve-skills |
| 20260805T053815Z-speckit-instructions | /speckit.instructions |
| 20260805T055700Z-skill-improve-skills | skill:improve-skills |
| 20260805T055700Z-skill-aliyun-workspace | skill:aliyun-workspace |

## 高信号要点

- **improve-skills**（5 条）：批量合入类改进缺少确定性脚本（--help 分域采集重复手工劳动）等
- **dingtalk-follow-up**（2 条）：事项跟踪执行中的优化点
- **aliyun-workspace**：cws-lib-python 四级命令全覆盖重构（venv 入口、FC env 约束）
- 详见各条目 Markdown 与 MANIFEST.md

> 提交方式：在 cloud-native-ai/spec-kit 仓库将本目录内容纳入 MR 或 issue 附件。

## 处理结果（2026-08-06，improve-skills 批量模式，两轮处理）

- **spec-kit 仓内落地（3 个技能，10 项）**：
  - draw-plantuml（1 条 5 点）：render-plantuml.sh 修复彩色标记循环陷阱（保留 `monochrome false`）+ 新增 `PLANTUML_SERVER_FALLBACKS` 公网回退与显式 UA，均经真实渲染验证；语法三规则（stereotype/颜色顺序、`~` 转义、frame 嵌套版本敏感）经实测后落 syntax-reference.md / 04-deployment-diagram.md / 12-rendering-and-output.md。
  - create-skills（2 条）：Step 6 无 `tests/contract` 项目的回退路径；Step 5 注册表插入锚点规则。
  - improve-skills（3 点）：Step 3 新增事实核查门（委托能力面 / 数据表事实源 / 覆盖分级核对），GREEN subagent 验证通过。
- **profiles 侧落地（用户确认为框架方直接处理）**：
  - dingtalk-follow-up（~/.qoder/skills，standalone）：S5 增加「本期无变化事项跳过写盘」规则；旧路径 grep 收尾验证通过（两处残留均为有意保留）；pipefail 修复已在位。
  - aliyun-workspace（profiles/.specify/skills，硬链接同步 ~/.qoder/skills）：沉淀 `scripts/dump-help-by-domain.sh`（--list/--dump 分前缀采集，实测 151 条命令）+ SKILL.md 新增「技能维护（上游合入新命令）」节；skills-utils validate 通过。
- **延迟项台账**：4 项需真实运行验证的条目（dingtalk-meeting 会后链路/改期会议室联动、dingtalk-follow-up L2 KQL 与 S0 门控交互、S5 跳过写盘生效性）连同解锁证据条件记入 profiles session memory（`20260805T184107Z-batch-12-deferred-...`）。
- **无操作项**：aliyun-workspace 与 /speckit.instructions 两条无优化点。
- **验证**：spec-kit 全量测试失败集与基线 diff 一致（42 条既有失败，零回归）；sync-mirrors 镜像字节一致。
