# Contract: Confirmation Taxonomy(确认分类判据)

**真源**: `shared/guidelines/confirmation-gates.md`(新增,唯一判据来源)
**消费方**: 全部 `templates/commands/*.md`、`skills/*/SKILL.md`、`shared/workflow/*`、`templates/instructions-template.md`(Documentation Map 引用)
**溯源**: FR-001、FR-002、FR-003、FR-007、FR-008、FR-011;澄清会话 2026-08-18

## C-1 两级判据

判据文档 MUST 包含且仅以如下语义定义两级:

1. **破坏性/不可撤销动作** → MUST 保留前置用户确认;
2. **可逆动作** → MUST NOT 以阻塞等待用户确认为执行前置条件;执行后 MUST 按 execution-report-contract 呈现。

## C-2 破坏性动作清单

清单 MUST 保守、可枚举,至少涵盖:

- 删除文件或数据
- 移动/归档既有工件
- 远程推送(push、force-push、远程分支操作)
- 覆盖用户既有内容(含覆盖用户既有权威条目,如 glossary 用户条目冲突写入)

清单扩展 MUST 以判据文档修订形式进行,MUST NOT 分散到各命令模板。

## C-3 治理保留清单

以下门控凭清单保留,不参与可逆性推断:

| 门控 | 所在面 | 保留理由 |
|------|--------|----------|
| 访谈退出门 | interview-pattern / `/speckit.interview` | 确认即产品形态(intrinsic) |
| 宪章不可撤销动作确认 | constitution-template.md | 宪章自身要求 |
| git commit 显式批准 | todo.md / implement.md | 与宿主安全规范对齐(governance-kept) |
| implement gate.yaml CONFIRM 判定 | implement.md | 机械安全门禁 |
| git-workflow 远程操作门控 | skills/git-workflow | push/force 为破坏性桶 |
| tools invoke 预览门控 | tools.md / tool-definitions.md | 任意脚本执行,存疑从严 |

## C-4 存疑从严

无法按 C-1/C-2/C-3 明确归类的动作 MUST 按破坏性处理(保留确认)。判据文档 MUST 含此规则的显式条文。

## C-5 回流约束

判据文档 MUST 含约束条文:新增或修订命令/技能 MUST NOT 引入非破坏性阻塞确认门控;契约测试与门控扫描(gate-scanner-contract)共同执行该约束。

## C-6 接入形态

命令/技能模板 MUST 以单行引用接入判据文档(对齐 Token Efficiency 纪律"引用不复制"),MUST NOT 在模板内复制判据正文。`templates/instructions-template.md` 的 Documentation Map MUST 含指向判据文档的一行,使判据对全部命令 ambient。

## C-7 既有保护清单不动

本契约覆盖的改写 MUST NOT 触碰:feedback.md consume 删除前确认、docs.md 移动/归档/删除分级、session.md 同名覆盖确认、feature.md 状态回退确认、analyze.md 补救批准、continuous 循环分级门控(create-team references)、git-workflow 远程门控。
