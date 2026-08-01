# Contract: 存量审计与创作门槛(audit-and-gates)

**Consumers**: /speckit.implement(审计执行)、contract tests、创作/改进技能

## C-A1 审计范围与产物

- 审计 MUST 覆盖:`templates/commands/*.md` 全部命令模板、`skills/*/SKILL.md` 全部技能、`shared/workflow/*.md` + `shared/guidelines/*.md` 共享文档、`scripts/python/*-utils.py` 引擎摘要能力(以审计时点动态枚举,不硬编码计数)。
- 产物 `audit.md` MUST 落 `.specify/specs/035-token-efficiency/`,行模式见 data-model.md §2(ID/单元/违规纪律/证据/注入量代理/触发频率/严重度/状态)。
- 注入量代理 MUST 为被整读文件的 `wc -l`/`wc -c` 实测值;禁止估算。
- 清单一经冻结(排序定稿)MUST NOT 增删行;整改只改状态列。

## C-A2 top-5 整改规则

- 严重度 = 触发频率 × 注入量的全清单排序;名次 1–5(不足 5 项则全部)状态 MUST 到达 `remediated`,其余 MUST 标 `backlogged`。
- 每个 `remediated` 行 MUST 附前后注入量对比(整改前实测 vs 整改后实测),SC-003 要求下降 ≥ 50%。
- 整改 MUST 落 canonical 源并经 `sync-mirrors.py --write` 扇出;AUTO-GENERATED 副本 MUST NOT 手改。
- 整改后措辞钉扎:每个 remediated 命令模板由 contract 测试断言"违规原句已消失 + 替代摘要级指令存在"(具体字符串对在审计定稿时写入测试)。

## C-A3 创作门槛检查项

以下文件 MUST 含内嵌字面量 `token-efficiency` 的检查项(引用纪律文档路径,不复制定义):

| 文件 | 形式 |
|------|------|
| `skills/create-skills/references/skill-creation-quality-checklist.md` | 检查组:确定性步骤交程序 / 数据访问摘要化 |
| `skills/improve-skills/references/skill-quality-checklist.md` | 同上(改进侧) |
| `skills/create-agent/SKILL.md` | 验证步骤一行检查项 |
| `skills/create-team/SKILL.md` | 交付校验一行检查项 |
| `skills/create-tools/SKILL.md` | 定义校验一行检查项 |

- 各文件镜像(`.specify/skills/...`)MUST 同步一致(`diff -rq`)。
- `templates/skills-template.md` MUST NOT 因本需求新增检查单节(检查项归创作流程,防产物模板膨胀)。

## C-A4 基线纪律

- 动手前 MUST 记录全套 pytest 基线(既有长期失败集与本需求回归区分);完成判定以"零新增失败"为准。
