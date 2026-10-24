# Contract: 文档一致性检查器（Doc-Consistency Checker）

**Feature**: 069a（父 069） | **File scope**: `scripts/python/doc-consistency-check.py` | **FR served**: FR-019、FR-020、FR-021、FR-022、SC-007

- **C-1** 命令面

```text
python3 scripts/python/doc-consistency-check.py --action verify \
  [--spec-dir <spec dir>] [--path <doc>]... \
  [--faces reader,evidence,duplicate,count] [--strict] [--format text|json] [--json-out <file>]
```

`--faces` 缺省为 `reader,evidence,duplicate,count`；未知面名 → 退出码 2。
`--spec-dir` 与 `--path` 至少给一个；两者都缺 → 退出码 2（不接受"什么都没检查所以通过"）。
只读：MUST NOT 修改被检查文件、MUST NOT 写除 `--json-out` 之外的任何文件。

- **C-2** 检查范围（三集合）

| 集合 | 内容 | 用途 |
|------|------|------|
| S1 形式产物 | `--spec-dir` 下的 `requirements.md` / `plan.md` / `tasks.md` / `data-model.md` / `research.md` / `quickstart.md` / `feature-ref.md` / `contracts/**` / `checklists/**` | evidence / duplicate / count |
| S2 显式文档 | 每个 `--path` | reader / evidence / duplicate |
| S3 判据 owner | 六面 owner 的固定路径表（内部常量，路径形态，不含判据正文） | duplicate 的对照侧 |

**排除（三集合共同）**：`notes/`、`review.md`、`verification.md`（dated record，不是当前现实）；`.specify/` 镜像侧文件；围栏代码块内行；表格分隔行；纯链接行；长度 < 24 字符的行；纯日期/版本行。
排除项 MUST 是闭集并写进实现常量；新增排除项属契约变更。

- **C-3** `evidence` 面规则

| 规则 | 判据 | 级别 |
|------|------|------|
| `grade-asof-unpaired` | 一行出现证据等级或 `as-of` 任一，另一项缺失 | blocking |
| `as-of-malformed` | `as-of` 值不匹配 `YYYY-MM-DD` | blocking |
| `as-of-stale` | `as-of` 早于该文件最后一次提交日期（`git log -1 --format=%cs -- <path>`） | blocking |
| `grade-invalid` | 等级不在封闭三值 `实测` / `推断` / `引用` | blocking |

证据等级与 `as-of` 的语义归 `expression-gate-operators.md` C-5；本面只做语法与配对判定，MUST NOT 重新定义取值。
`as-of-stale` 在非 git 环境或该文件无提交历史时 MUST 输出 `not-evaluated`（附 `reason`），MUST NOT 判为通过。

- **C-4** `reader` 面规则

每个 S2 文档 MUST 在前 40 个非空行内同时含 `**Readers**:` 与 `**Reading scenario**:` 且值非空；否则 `reader-declaration-missing`（blocking）。
`--path` 缺省时该面输出 `not-applicable`（显式），不判通过、不判失败。

- **C-5** `duplicate` 面规则

对 S1 ∪ S2 ∪ S3 做**跨文件**归一化行比对：

1. 归一化：去行首列表/引用前缀、压连续空白、去行尾标点、大小写折叠（仅 ASCII）。
2. 命中条件：归一化后**完全相等**且长度 ≥ 24 字符；或 `difflib.SequenceMatcher(None, a, b).ratio() >= 0.90` 且长度 ≥ 40 字符。
3. 同一归一化行出现在 **≥ 2 个不同文件** → 一条 `duplicate-fact`，`path/line` 取字典序首处，`counterpart` 取第二处。
4. 同一文件内重复不报（不是跨处手写）。

`fix_direction` 恒为「改为对唯一 owner 的引用」。本面 MUST NOT 试图改写文本、MUST NOT 推荐「改措辞使其一致」。

- **C-6** `count` 面规则（委派，不重写）

`count` 面 MUST 委派给 `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py`（或其 `.specify/skills/` 镜像），以 `--spec-dir --stage <plan|tasks> --json-out` 形式调用，把其 `count` 类 finding 映射为 `count-mismatch`。
本检查器 MUST NOT 自行实现「FR/SC/任务计数与定义数比对」的规则（同一规则两个实现必然漂移）。
委派目标不存在、不可执行或返回码 2 时，输出 `count_check: {"status": "not-run", "reason": ...}`：
`--strict` 下该状态计为失败；非 strict 下计为 `not-evaluated`（不是通过）。

- **C-7** 输出形态

`--format json` MUST 输出：

```json
{
  "action": "verify",
  "checked_at": "2026-10-24T12:00:00Z",
  "scope": {"spec_dir": "...", "paths": ["..."], "files_scanned": 7},
  "faces": {"reader": "pass|fail|not-applicable", "evidence": "...", "duplicate": "...", "count": "..."},
  "findings": [{"face": "duplicate", "rule": "duplicate-fact", "path": "...", "line": 12,
                "snippet": "...", "counterpart": "...", "fix_direction": "..."}],
  "count_check": {"status": "delegated|not-run", "reason": null}
}
```

`findings[]` 的字段集合由 `data-model.md` E7 拥有；本契约不新增字段。

- **C-8** 退出码

| 码 | 含义 |
|----|------|
| 0 | 零 finding；`not-evaluated` 条目允许存在但必须出现在输出里 |
| 1 | 至少一条 finding；或 `--strict` 且存在任一 `not-evaluated`（含 `count_check.status = not-run`） |
| 2 | 输入或解析错误（无范围、未知面、owner 路径不可解析、无法读取文件） |

MUST NOT 以 0 退出同时携带 finding。
`not-evaluated` 的语义是「本项没有被评估」，不是「本项通过」：非 strict 下它不改变退出码，但 MUST 以独立字段出现（`as-of-stale` 见 C-3，`count` 见 C-6）；strict 下它一律升级为退出码 1。

- **C-9** 自检样例（route a，本阶段已执行）

本契约的三条规则在实现期 MUST 由 `tests/contract/test_doc_consistency_checker.py` 的夹具覆盖，且夹具 MUST 包含 SC-007 的三类注入各一例：

| 注入 | 期望 finding |
|------|--------------|
| 把一处引用改写成 owner 原文副本 | `duplicate` / `duplicate-fact`，两侧定位 |
| 把一处 `as-of` 改成更早的日期 | `evidence` / `as-of-stale` |
| 把一处派生计数改成手打且与定义数不符 | `count` / `count-mismatch`（经委派） |

漏报数 MUST 为 0；多报（排除项误报）也 MUST 为 0，二者分别断言。

- **C-10** 调用点

本检查器由下列入口调用（接线封闭集见 `flow-class-ledger.md` C-15；调用点表见 `expression-gate-operators.md` C-14）：

| 调用点 | 时点 | 调用形态 |
|--------|------|----------|
| `/speckit.docs`（W1） | 分派前解析类别之后、收敛/写作判定之前 | `--path <每个受触文档>`；规格面存在时另加 `--spec-dir <spec dir>` |
| `skill:create-docs`（W3） | Reconcile Loop R6 verify 与 Authoring Flow R6 验证 | 同一形态；命令侧已执行时复用其输出，不重复执行 |

规则：
- 检查器 MUST NOT 读取流程类别；「要不要跑」由调用点按类别决定，检查器只负责执行被点名面。
- 其他命令模板与技能 MUST NOT 调用本检查器（接线封闭）。
- 调用点缺席（引擎或 owner 未刷新）时，调用方 MUST 显式跳过并标注，MUST NOT 以「没跑 = 通过」呈现。
