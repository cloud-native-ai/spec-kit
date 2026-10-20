# Efficiency Model — sdd-loop-driver 运行效率优化

> 本文件是 Feature 063 四项运行效率优化的**唯一 owner**：快车道（§1）、两槽位测试预算（§2）、plan 只小修约束（§3）、进度可见与驱动解耦（§4）。SKILL.md 与 docs 页只保留摘要与指针；`references/dispatch-recipes.md` 与 `references/stage-prompts.md` 只引用本文件定义的字段、判据与程序，不复写规则。契约钉住落点为 `tests/contract/test_sdd_loop_driver_efficiency.py`。

本文件自带运行时事实：条目只描述驱动在编排层执行的动作与判定；CLI 行为事实由 Feature 064 的 `references/cli/` 档案拥有，本文件只读引用，不复制档案内容。

## 1. 快车道（Fast Lane）

### 1.1 入口与唯一启用形式

- 快车道**仅在 U0 入口声明携带字面量 `fast-lane=opt-in` 时启用**，且该字面量原文写入该线状态脊。这是无人值守运行的唯一启用形式；自然语言声明、规模印象、历史运行推断都不构成启用。
- 交互式用户在场时，驱动可以在七判据实测后提议一次快车道，并把用户采纳的原文写入状态脊；提议不得阻塞运行，等待回答期间按完整链继续。
- 缺少字面量 → `decision=full-chain`，完整链是缺省行为。

### 1.2 裁决点与七项判据

裁决点在 `tasks.md` 已产出、`checklist` 派发之前，由 `scripts/admission-check.py` 以制品实测值判定。七项判据（全部机械判定；任一项无法证明即 fail-closed 判 `full-chain`）：

| id | 判据 | 机械证据 |
|----|------|----------|
| (a) | FR 定义行数 8–30（含端点），任务行数 10–40（含端点） | `requirements.md` 行匹配 `^- **FR-[0-9]{3}**:`（owner: requirements.md FR-003(a)）；`tasks.md` 行匹配 `^- \[[ xX]\] T[0-9]{3}`（窄模式，准入唯一）。SC 行、说明行、分组标题不计入。 |
| (b) | 宪法零改动 | `git diff --name-only <base>..HEAD` 不含 `.specify/memory/constitution.md` |
| (c) | 不新增可执行引擎、CLI 命令/模板、技能、外部依赖、网络服务或模型 API | 引擎/模板/依赖清单路径保守超集扫描 + 新增代码中的网络/模型调用痕迹；`skills/external/` 新增路径视为新技能 |
| (d) | 不涉及安全/隐私敏感面 | 路径或新增行命中认证授权、凭据/密钥、删除/迁移、发布/外传、确认门判据即拒绝 |
| (e) | 单线单分支且无并发线触碰同一交付路径 | `lines.manifest` 恰一条本线记录，分支等于 `--expected-branch` 与当前分支；语法 owner 为 `data-model.md` E1 §「lines.manifest 行语法」 |
| (f) | `clarify` 完成、活动标记为零、Related Feature 已解析 | `requirements.md` 含 `## Clarifications` + `### Session`，无 `[NEEDS CLARIFICATION:`；注册表行与详情文件存在 |
| (g) | 需求质量清单全绿 | `checklists/requirements.md` 至少一项 `- [X]`、零 `- [ ]` |

**窄/宽模式边界**：准入只使用窄任务模式 `^- \[[ xX]\] T[0-9]{3}`。仓库记账使用宽模式 `^- \[[ xX>~]\] T[0-9]{3}`，它会把 `[>]`/`[~]` 行计入，**MUST NOT 用于准入**；两者不得混用。FR/任务区间数值的运行时 owner 是 `admission-check.py` 的 `FR_MIN/FR_MAX/TASK_MIN/TASK_MAX` 常量，契约测试钉住它们；语义 owner 是 `requirements.md` FR-003。

**脚本接口**（`scripts/admission-check.py`，标准库且 Python ≥3.8）：

```text
admission-check.py --project P --base-ref R --requirements F --tasks F \
  --checklists F --entry-evidence F --lines-manifest F --expected-branch B \
  [--json-out F]
```

退出码：`0` = 可录取（`fast-lane`）；`1` = 拒绝（`full-chain`）；`2` = 输入或解析错误。JSON 记录逐条携带 `{id, verdict, evidence}`。

### 1.3 准入记录（E1）

准入记录在 `checklist` 派发前写入状态脊。字段面以 `data-model.md` E1 为准，至少包含：

- `decision`：`fast-lane` | `full-chain`
- `entry_evidence`：入口原文（含 `fast-lane=opt-in`）
- `criteria[]`：七项 `{id, verdict, evidence}`，evidence 非空且可复算
- `measured`：`{fr_count, task_count}`，由制品实测派生，不手抄
- `decided_at`：裁决时间
- `reversion`（可选）：`{trigger, evidence, at}`，录取后判据失效时记录

录取时记录必须携带跳过标记 `checklist=skipped(fast-lane)`（[[STR-003]]）。

### 1.4 下游发布与收口标记

- 裁决结果 MUST 随下游阶段提示词发布（至少 `implement` 与 `review`），使阶段不把缺失的 `checklist` 产物当作缺失的必需门；条件块见 `references/stage-prompts.md` §「Fast Lane Conditional Blocks」。
- 收尾汇总 MUST 携带 `checklist=skipped(fast-lane)` 或等价可见标记。
- 未录取的运行不发布跳过块，`checklist` 照常执行。

### 1.5 失败回退

录取后任一判据失效，或后续阶段发现新事实使判据不再成立（新增引擎/模式/安全面、任务数越界等）时：

1. 驱动 MUST 回退完整链，记录回退触发与证据到状态脊 `reversion` 字段；
2. 在适用位置补派 `checklist`；
3. 若回退发生在 `analyze` 已通过之后，补派 `checklist` 后 MUST 重过 `analyze` 一次，再按完整链继续；
4. 回退 MUST NOT 静默；收尾汇总必须列出回退次数与原因。

### 1.6 analyze / review 不变量

快车道 MUST NOT 改变 `analyze` 的 CRITICAL/HIGH 归零或已处置判据、至多一轮有界回环，也 MUST NOT 改变 `review` 的行为、证据义务与发现分级。快车道只替代 `checklist` 的质量清单步骤；`analyze` 与 `review` 始终必经、判定不削弱。

### 1.7 自应用排除

063 自身的运行 MUST 使用完整阶段链（`checklist`、`analyze`、`review` 均必经），MUST NOT 产生本特性自身的快车道记录。该例外在 requirements FR-010、plan 与收尾证据中可见；它是规格约束，不是对快车道判据的豁免。

### 1.8 契约钉住

FL-01…FL-10 由 `tests/contract/test_sdd_loop_driver_efficiency.py` 的 `test_fl_01…test_fl_10` 钉住；准入行为由 `tests/unit/test_admission_check.py` 覆盖。任何运行 MUST NOT 在缺少 E1 准入记录时声称自己走了快车道。
