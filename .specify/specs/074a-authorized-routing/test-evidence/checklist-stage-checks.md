# Checklist-stage deterministic checks — slice 074a-authorized-routing

**Stage**: checklist（`/speckit.checklist`，`decomposition=single-package`，无子代理派发）
**Slice**: `.specify/specs/074a-authorized-routing/`
**Stage base**: `a98155404`（074a tasks 完成提交）
**Recorded**: 2026-10-29
**Host**: python3（本机 PATH），git

本文件只贴各确定性检查的**真实输出**与偏离裁定；结论不复述到其他产物。

## 0. Test budget record（stage_base=checklist）

**Stage-status row (`status=not-run-docs-only`, 六项缩减字段集 per `.specify/skills/sdd-loop-driver/references/efficiency-model.md`)** — `stage=checklist`, `row_type=stage-status`, `status=not-run-docs-only`, `selection_basis=本阶段零可执行面改动（只新增一份 Markdown 检查单与本证据文件），targeted-set-v1 无新主体`, `changed_paths[]=.specify/specs/074a-authorized-routing/{checklists/readiness-2026-10-29.md,test-evidence/checklist-stage-checks.md}`, `evidence_ptr=.specify/specs/074a-authorized-routing/test-evidence/checklist-stage-checks.md`。运行字段不适用，MUST NOT 报 `unknown`。

本阶段未运行 pytest：判据对象是需求文本，运行测试不产生关于它的信息（checklist-methodology「An item answerable only by running the product is a defect in the checklist」）。

## 1. 入口前提与本阶段的作用域覆盖

```text
$ bash .specify/scripts/bash/check-prerequisites.sh --json
{"REQUIREMENTS_DIR":"/storage/project/cloud-native-ai/spec-kit/.specify/specs/074-goal-team-sdd-unification","REQUIREMENT_ID":"074","FEATURE_ID":"074","FEATURE_NAME":"Goal/Team/Agent 与 SDD 开发流程统一（Unified Goal/Team/Agent Control Hierarchy with SDD Invocation）","AVAILABLE_DOCS":["research.md","data-model.md","contracts/","quickstart.md","checklists/","feature-ref.md"],"MODE":"C","WRITABLE":true}
rc=0
```

- **实测**：前提脚本按分支前缀解析到**父** spec 目录（`074-goal-team-sdd-unification`），与 tasks 阶段同因（分支名 = 父特性名）。
- **显式覆盖**：派发简报要求本阶段显式作用于切片，故 `REQUIREMENTS_DIR` 覆盖为 `.specify/specs/074a-authorized-routing/`。父 spec 的 `requirements.md`、`plan.md`、`tasks.md`、`checklists/` 全程只读，零改动（§ 6 复核）。
- **不覆盖既有检查单**：切片内既有 `checklists/requirements.md`（requirements 阶段产物，10570 字节）未被打开写入、未被改写；本阶段产物是新文件 `checklists/readiness-2026-10-29.md`。

## 2. 判据对象的结构复核（程序导出，非手敲）

```text
$ r=.specify/specs/074a-authorized-routing/requirements.md
$ grep -cE '^\- \*\*FR-[0-9]+\*\*:' $r                                        → 20
$ grep -cE '^\- \*\*SC-[0-9]+\*\*:' $r                                        → 6
$ grep -cE '^\| .STR-[0-9]+. \|' $r                                           → 10
$ grep -cE '^\| .FR-[0-9]+. \|' $r                                            → 20   （Parent Mapping FR 行）
$ grep -cE '^\| .SC-[0-9]+. \|' $r                                            → 6    （Parent Mapping SC 行）
$ grep -cE '^### User Story [0-9]' $r                                         → 3
$ awk '/^\*\*Acceptance Scenarios\*\*/{f=1;next}/^---/{f=0}f&&/^[0-9]+\./' $r | wc -l   → 11   （Given 场景）
$ awk '/^### Edge Cases/{f=1;next}/^## /{f=0}f&&/^- /' $r | wc -l              → 13   （Edge Cases）
$ grep -cE '^\- \*\*A[0-9]+\*\*:' $r                                          → 11   （A1–A7、A9–A12）
```

20 FR / 6 SC / 10 STR / 3 stories / 11 场景 / 13 边界用例 / 11 假设，与 `requirements.md` 头部声明一致；检查单的每条 traceability 锚点都指向这些条目之一。

## 3. 需求校验器（`validate-requirements.py`）

```text
$ python3 .specify/scripts/python/validate-requirements.py .specify/specs/074a-authorized-routing/requirements.md
file: .specify/specs/074a-authorized-routing/requirements.md
status: ok
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] pass (0)
  [marker-count] pass (0)
  [dup-id] pass (0)
scanned: 492 lines, 26 definition rows, 10 shared strings
0 error(s), 0 warning(s)
rc=0
```

五命题全绿只证明**编号与引用自洽**，不证明需求可判定——本阶段 14 条 fail 全部落在校验器不覆盖的语义面（定义缺失、覆盖缺口、包含性声明缺基线），二者不冲突。

## 4. 检查单自身的机械复核

```text
$ f=.specify/specs/074a-authorized-routing/checklists/readiness-2026-10-29.md
$ grep -cE '^- \[[ xX]\] CHK[0-9]{3} ' $f        → 32   （条目总数）
$ grep -cE '^- \[x\] CHK[0-9]{3} ' $f            → 18   （pass）
$ grep -cE '^- \[ \] CHK[0-9]{3} ' $f            → 14   （fail）
$ grep -cE '^  - \*\*fail\*\*' $f                → 14   （每条 fail 一条证据行）
$ grep -cE '^- \[[ xX]\] CHK[0-9]{3} .*\[[A-Za-z].*\]' $f → 32   （带 traceability 锚点）
$ grep -oE 'CHK[0-9]{3}' $f | sort -u | wc -l    → 32   （编号唯一）
first=CHK001 last=CHK032                         （自 CHK001 起连续）
```

- 32 条 ≤ 方法论软上限 40；traceability 32/32 = 100%（下限 80%）。
- 禁用形态扫描：条目一律以 `Do/Is/Are/Does` 提问，`Verify/Test/Confirm/Check` 开头的实现行为条目 0 条。
- 14 条 fail 逐条带 `requirements.md:行号` 证据或 owner 路径，可在不重读本回传的情况下复核。

## 5. 同作者检测与检测方式披露

- 判据对象由 requirements / clarify / plan / tasks 四次派发撰写（`78e26f0ca`、`907d21fbe`、`a98155404`），**非本会话**产物；`objective-analysis-gate.md` § When the gate fires 的触发条件（同会话同作者）不成立。
- 派发简报固定 `decomposition=single-package` 且不派发子代理，故无 fresh-context 检测者被编入。
- 结论：全部 32 条按 `(direct read)` 判定，程序可导出的前提（§ 2、§ 3）以真实运行结果代替断言，不写成未经执行的数字。

## 6. 红线复核

- 父 spec 与父设计（`.specify/specs/074-goal-team-sdd-unification/**`）零改动；父 `checklists/` 未被读取写入。
- 切片既有 `checklists/requirements.md` 零改动（新文件而非覆盖）。
- plan-owned 面（`plan.md` / `data-model.md` / `contracts/**` / `quickstart.md` / `research.md` / `feature-ref.md`）零改动 → 无 `PLAN-EDIT:`。
- `requirements.md` / `tasks.md` 零改动：本阶段只判定、不回修（14 条缺口按命令 Handoffs 交回 `plan`/`tasks` 回环裁决）。
- 未派发子代理；未切换分支；未 push；运行记录与状态脊不入提交。
