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

## 2. 两槽位测试预算（Test Budget）

### 2.1 全量定义与作用域

**全量测试运行** = 以项目规范测试运行器执行、不带路径/测试过滤器的完整套件（本仓 = `bash scripts/bash/run-tests.sh`）。预算以**运行线**为作用域：每线独立台账与独立槽位，多线并行互不共享或消耗。每条运行线恰好两个全量槽位：

| 槽位 | 时点 | 程序 |
|------|------|------|
| `baseline` | implement 起点（首个任务前） | `run-tests.sh --names-out <spec-dir>/baseline-failed.txt`，按名称捕获失败名单 |
| `closure` | `review` 通过之后、合并之前，由驱动或独立校验单元执行 | `run-tests.sh --names-out <spec-dir>/final-failed.txt`，`comm -13` 名称级比较 |

implement 内 MUST NOT 再运行第二次全量套件；其内部回归比较义务由收口槽位承担。槽内重跑记 `in-slot-rerun`，不另开槽。

### 2.2 台账与证据分工

- **E2 台账唯一来源** = 线状态脊的 `<!-- test-budget:begin -->` … `<!-- test-budget:end -->` JSONL 围栏；`<spec-dir>/test-evidence/implement.jsonl` 仅是 E3 传输/证据副本，MUST NOT 作为台账或审计来源。
- 本地拓扑 `spine_write_mode=direct` 由阶段直接追加；远端 `transport` 由执行侧写传输行，驱动在 U4 后合并进状态脊并记 `merge_source`/`merged_at`，合并前不得审计。
- E2 行字段以 `data-model.md` E2 为准（seq / slot / stage / purpose / trigger / at / command / selection_basis / rc / passed / failed / failed_names_path / baseline_compare / evidence_ptr，例外行另带 `exception_reason`，环境失败行带 `environment_evidence`）。
- 缺失 `passed`/`failed` → 审计报 `unknown`，MUST NOT 记为零或补造。

### 2.3 固定选择程序 `targeted-set-v1`

`clarify` / `plan` / `tasks` / `checklist` / `analyze` 与 `review` 只运行定向测试集；选择 MUST 由固定程序 `targeted-set-v1` 执行。算法 owner 是 `contracts/test-budget.md` TB-05；本节是实现载体，二者不一致时以 TB-05 为准。

- **输入**：`stage_base`（阶段起点提交）、`spec_dir`、`changed_paths`（`git diff --name-only --diff-filter=ACMR <stage_base>..HEAD` 与 `git status --porcelain` 的路径并集）、`test_roots` = `tests/unit`、`tests/contract`、`tests/integration`、`tests/scenarios`。
- **(a) 改动路径覆盖**：候选 = `find <test_roots> -type f -name 'test_*.py' | LC_ALL=C sort`；对每个不在 `test_roots` 下的 `changed_path`，选中内容包含该仓库相对路径或其模块 stem（basename 去扩展名）的候选文件（`grep -lF` 固定字符串）。
- **(b) 交付物契约测试**：本特性短名从 `spec_dir` 目录名去掉编号前缀派生；选中内容包含该短名或交付面路径（`skills/external/sdd-loop-driver`、`docs/reference/skills/sdd-loop-driver.md`）的契约/集成测试。
- **(c) 夹具变更**：`changed_path` 在 `test_roots` 下时选中该文件自身；在 `tests/fixtures/` 下时选中内容引用该夹具路径的测试文件。
- **排序与输出**：去重后 `LC_ALL=C sort -u`，每行一个仓库相对测试路径（stdout），供 E3 `selected_paths[]` 原样记录。
- **复现性**：同一 `stage_base` + 同一工作树状态 MUST 产生同一集合；阶段 MUST 记录完整命令、`stage_base`、输出（或摘要 + 哈希）与充分性说明；不同阶段 MUST NOT 使用不同选择命令。
- **空集**：改动了可执行面却得到空集 → `empty-selection-escalated`（扩大同族或按显式例外升级为全量，并记录原因）；仅文档改动 → `not-run-docs-only`。

### 2.4 E3 证据字段与完整性

每次定向运行记录：命令、选择依据、所选路径 `selected_paths[]`、充分性 `sufficiency`、rc、passed/failed、新增失败 `new_failures[]`、比较基线。每个**适用阶段**（`clarify` / `plan` / `tasks` / `checklist` / `analyze` / `review`）恰有一条 `row_type=stage-status` 行；整阶段缺行计入完整性分母，MUST NOT 静默缩小分母。

- `not-run-docs-only` 按**六项缩减字段集**判完整：`stage`、`row_type=stage-status`、`status`、`selection_basis`、`changed_paths[]`、`evidence_ptr`；运行字段不适用，MUST NOT 报 `unknown`。
- 快车道按 §1 授权跳过 `checklist` 时，该阶段记 `not-applicable-skipped-stage`（[[STR-008]]），以 E1 准入记录 + [[STR-003]] 为联结证据；MUST NOT 记为 `unknown`，MUST NOT 计入完整性分母。
- `unknown` 只用于证据缺失；收口审计输出 `stages=N complete=N`（N = 适用阶段总数，含文档型阶段）。

### 2.5 审计、例外与修复

`scripts/audit-test-budget.py --spine "$STATE_SPINE" --spec-dir <spec-dir> [--logs-dir <dir>] [--stage-check implement|closure]`：

- 校验两槽位、第三槽位拒绝、`in-slot-rerun` 只能出现在 `closure` 之后、`out-of-slot-exception` 必带原因与证据、`environment-failure` 不消耗槽位、closure 必须是名称级差集。
- `--logs-dir` 扫描阶段日志中的全量 runner 命令：日志中出现但台账未入账 → 违规；日志缺失 → `unknown`，MUST NOT 当零。
- `--stage-check implement` 只要求 baseline 恰 1 且允许 closure 未写入；`--stage-check closure` 要求 baseline 与 closure 各 1。
- 摘要 MUST 输出 `slots=baseline:N closure:N reruns=N exceptions=N unknown:N environment_failures=N` 与 `stages=N complete=N`。

**槽外例外与槽内重跑**：任何槽外全量 MUST 以 `out-of-slot-exception` 形式出现，带原因与证据，收尾汇总列出次数与原因。收口因修复新失败而重跑同一套件记 `in-slot-rerun`（含触发与证据），不另开槽；MUST NOT 静默超预算。**环境失败**：收集/执行任何测试前即失败（解释器或依赖缺失、收集前错误）记 `environment-failure`，不消耗槽位并附证据；实际执行了测试的调用（含 0 tests collected 的选择失败）消耗槽位。

**收口归属**：implement 只消耗 `baseline` 槽位；`closure` 由驱动在 `review` 通过之后、合并之前写入同一状态脊。closure 修复重入携带 `baseline_slot=skip(closure-repair)`，不再消耗 baseline。

### 2.6 编排层实现

本预算 MUST 在编排层实现（阶段提示词 + 状态脊台账 + 收口审计），MUST NOT 依赖修改框架命令内部流程。`STATE_SPINE_PATH`、`EVIDENCE_DIR`、`SPINE_WRITE_MODE=direct|transport` 由阶段提示词骨架统一携带；缺失 `STATE_SPINE_PATH` → 派发前快速失败（`ANOMALY:`），MUST NOT 另建第二份台账。

### 2.7 契约钉住

TB-01…TB-10 由 `tests/contract/test_sdd_loop_driver_efficiency.py` 的 `test_tb_01…test_tb_10` 钉住；审计行为由 `tests/unit/test_audit_test_budget.py` 覆盖；名称级回归由 `tests/integration/test_sdd_loop_efficiency_regression.py` 覆盖。
