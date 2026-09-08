# Contract: 触发段形态与全 agent 路径覆盖 (trigger-section)

**Requirement**: `050-proactive-flow-trigger` → Feature 050
**Surfaces under contract**: `templates/instructions-template.md`(新 `## ` 章节)· `.specify/templates/instructions-template.md`(镜像)· `.specify/instructions.md`(再生产物)· `scripts/bash/generate-instructions.sh`(symlink 段)· `src/specify_cli/__init__.py`(`_INSTRUCTIONS_FILE_MAP` 一致性)
**Test file**: `tests/contract/test_proactive_trigger_section.py`
**Clauses**: C-1 … C-12

条款均为结构性、机械可断言。断言风格承 `tests/contract/test_task_complexity_rubric.py`(双表面 + 字节镜像 + 项目中性禁用 token)。

---

| ID | Clause | Assertion |
|----|--------|-----------|
| **C-1** | 章节存在于**两个表面** | `## Proactive Flow Trigger` 标题同时出现在 `templates/instructions-template.md` 与 `.specify/templates/instructions-template.md`;两侧均含指向 `shared/guidelines/proactive-trigger.md` 的指针链接 |
| **C-2** | 字节相同镜像 | `templates/instructions-template.md`.read_bytes() == `.specify/templates/instructions-template.md`.read_bytes() |
| **C-3** | 插入位置满足顺序契约 | 在模板的 `## ` 标题序列中,`## Proactive Flow Trigger` 紧随 `## Documentation Map` 之后、`## Fact, Correctness & Logic Checks (Input Sanity)` 之前(FR-005b「同一趟、合规先行」的结构落点) |
| **C-4** | 摘要 + 指针形态,不承载全文 | 章节正文行数 ≤ 25;且章节内 MUST NOT 出现 `### ` 子标题(additive reconcile 不传播 `###`,寄望子节即等于不投递 — plan.md D-1 推论) |
| **C-5** | **引用不复制**:零流程枚举 | 章节内 `/speckit.` 出现次数 == 0;`skills/` 路径出现次数 == 0;**参数结构示例出现次数 == 0**,检测模式为闭合集:正则 `--[a-z][a-z0-9-]*`(长选项形态)、`\$ARGUMENTS`、`<[a-z-]+>`(占位符形态)三者命中数之和 == 0(FR-002:调用形式由引擎在运行时供给,不由指令文件承载) |
| **C-6** | **零 BLOCKING_PATTERNS 命中** | 对章节文本运行 `scan-confirmation-gates.py` 的 `BLOCKING_RE`,命中数 == 0。该条款与 C-11 共同守住"门控整数余量为 0"(plan.md D-4) |
| **C-7** | 项目中性 | 章节内 MUST NOT 出现任一禁用 token:`spec-kit`、`specify-cli`、`specify_cli`、`Feature 0`、`cloud-native-ai`、`.specify/specs/0`(承 C-9 of `test_task_complexity_rubric.py`;shipped-surface 中性) |
| **C-8** | 受管块标记不得出现在指令模板 | 章节内 MUST NOT 出现 `<!-- ` + `_START -->` / `_END -->` 形态的受管块标记;运行状态留在 `.specify/memory/trigger/`,指令侧只放指针(承 `test_git_workflow_instructions_block.py:33–40` 先例) |
| **C-9** | 章节会被 additive reconcile 传播 | 对一个缺少该章节的 `.specify/instructions.md` 样本运行 `generate-instructions.sh` 后,该章节出现;再次运行**幂等**(章节数不增、块外字节不变);既有非模板章节(如 `## Recurring Operational Lessons`)保留 |
| **C-10** | 全 agent 路径覆盖(FR-003 硬前置)—— **本条款是路径计数的唯一权威** | 计数口径:`_INSTRUCTIONS_FILE_MAP` 有 **6 个 key**,其值去重后为 **5 个不同文件**(`codex` 与 `qoder` 共用 `AGENTS.md`);`generate-instructions.sh` 共创建 **8 条 symlink**(5 个声明文件 + `QODER.md` + 2 条 IDE 侧链接)。其他工件 MUST 引用本条而不复述枚举。断言:在临时根上运行 `generate-instructions.sh` 后 —— ① 5 个声明文件(`CLAUDE.md`、`AGENTS.md`、`HERMES.md`、`.github/copilot-instructions.md`、`.opencode/instructions.md`)全部存在且 `readlink -f` 解析到 `.specify/instructions.md`;② 另 3 条(`QODER.md`、`.qoder/project_rules.md`、`.claude/project_rules.md`)同样存在并解析到同一目标;③ 合计 **8** 条 |
| **C-11** | 门控扫描总数不增 | 全部改动落地后运行 `scan-confirmation-gates.py --summary`,`total` **等于 T002 冻结在 `baseline-gates.json` 的前值**(本契约不硬编码该数字,以免项目侧合法变动时被迫改契约;撰写时实测前值为 23)、`violations` == 0;`tests/contract/test_confirmation_gates_sweep.py` 保持绿(cap = 044 `baseline.json` total × 25%) |
| **C-12** | 声明与生成一致 | `_INSTRUCTIONS_FILE_MAP`(`src/specify_cli/__init__.py`)的每个值都被 `generate-instructions.sh` 实际创建;`_check_instructions` 对 6 个 tool key 全部返回 `pass`(消除当前 hermes/opencode 恒 `fail` 的状态) |

---

## 章节必须承载的语义要点(内容契约,由 C-1…C-8 的形状约束 + `discipline-doc.md` 的全文约束共同钉住)

章节以摘要形式陈述以下五点,每点一行,细节一律指向纪律文档:

1. **每回合评估**:每个用户回合都要判断"当前状态下有哪个流程值得执行";评估本身静默,无适用流程时零用户可见输出。
2. **同一趟、合规先行**:该判断接在本文件 Documentation Map 常驻指令要求的合规检查之后,在同一趟里完成;建议不早于合规检查产出。
3. **证据预算**:默认只用已在上下文中的信息;不足时按纪律文档的升级判据调用引擎的探测形态,不读制品全文。
4. **建议形态**:一行非阻塞提示 = 用途说明 + 引擎给出的确切调用形式;用户可采纳也可忽略,忽略不影响其当前请求。
5. **入口**:状态查询、复位、关闭、调优一律经引擎 `trigger-utils.py`(指针指向纪律文档的 action 表),不引入需要用户记忆的新命令名。

## 禁止出现的表述(实现期硬性清单)

- 任何 `BLOCKING_PATTERNS` 字面量(C-6);尤其 `confirmation gate`、`确认门禁`、`确认门控`、`等待确认`、`等待用户确认`、`after confirmation`、`confirm before`、`stop and confirm`、`interactive confirmation`、`显式用户确认`。提及治理域名时使用路径形式 `shared/guidelines/confirmation-gates.md`(连字符,不匹配 `confirmation gate` 的空格形态)。
- 任何命令名、技能名、参数结构枚举(C-5)。
- 任何项目专属标识(C-7)。
- `### ` 子标题(C-4)。

## 交付顺序约束

C-2 / C-9 / C-10 / C-12 涉及生成脚本与镜像,故实现顺序 MUST 为:改模板 → `sync-mirrors.py --write` 落镜像 → 改 `generate-instructions.sh` 补两条 symlink → `sync-mirrors.py --write` 落脚本镜像 → 在本仓运行 `/speckit.instructions` 使 `.specify/instructions.md` 获得新章节 → 跑 C-1…C-12。颠倒顺序会让 C-9 在真实树上失败。
