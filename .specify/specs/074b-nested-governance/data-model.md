# Data Model: 074b-nested-governance

**Requirement → Feature**: `074b-nested-governance` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一

Entities E1–E8; validation rules V-1…V-12; two state machines (report-section composition, containment
verification). Entities owned by earlier features (the team run report, the team ledger item, the Goal
and Target definition, the neutral metadata key map, the line registry entry, the handoff block) are
**referenced by path, never re-specified**: this slice adds a section to one report, one statement to
one authoring baseline, one sentence to one conceptual-model bullet, one section to the instructions
template, one sentence to one guideline, and one test-evidence carrier. Nothing else is stored.

**Numbering convention (disclosed)**: this slice's entity and rule ids are **local** and continuous
(`E1`…`E8`, `V-1`…`V-12`), each carrying the parent entity or rule where one exists. The parent's
`V-1`…`V-29` are not carried with gaps, because only nine of them fall inside this slice and a gapped
set reads as a deletion rather than a projection. `074a` took the opposite decision for its own slice
(all 29 fell inside it, so it kept the parent numbers); the two decisions are consistent with one rule
— one id per one rule set, never two ids for the same text.

**One-declaration rule for this file**: the routing input names, the closed value domains, the verdict
table, the precedence and the reason-code vocabulary are owned by
`shared/definitions/sdd-routing-definitions.md` and MUST NOT be restated here or anywhere else.
V-10 is the mechanical guard, and it is the local projection of the parent's `V-19`.

---

## E1 `## Nested SDD Runs` report section（父 E6）

Owner: `skills/internal/create-team/SKILL.md` § Report contract (amended once, in place).

| 子项 | 规则 |
|------|------|
| 段标题 | 字面量 `[[STR-007]]`，逐字；本切片是该字面量的唯一落点（D-3） |
| 每次调用一行 | outcome（三值之一）+ artifact paths + evidence paths + routing-verdict reference + anomalies |
| 无调用 | MUST 显式声明「本次无嵌套 SDD 调用」，MUST NOT 省略整段 |
| 与既有必填段的关系 | 并列；不合并、不重排、不互相替代（V-3） |
| 写者 | team supervisor（tracked 工件的唯一写者） |

**V-1**: 段标题 MUST 逐字等于 `[[STR-007]]`；同义改写、大小写变化或层级变化均判不合规。
**V-2**: 每行的 outcome MUST 取自三值封闭集；第四值、自由文本或空值一律非法。
**V-3**: 该段与既有必填段并列 —— 既有段的名称、次序与内容义务不变；嵌套段的证据不替代外层运行的验证义务。
**V-4**: 段内引用的每个路径 MUST 在交接时存在；不存在者按缺失记录，MUST NOT 用占位符或「稍后补」替代（父 V-10）。

## E2 Ledger attribution row（父 E8，只读引用）

Reuses the existing team ledger (`items.jsonl`); the attribution field and its `T-<nnn>` grammar are
owned by `skills/internal/create-team/references/summary-mapping.md` and
`shared/definitions/goal-definitions.md` (referenced).

| 事实 | 规则 |
|------|------|
| 写者 | team supervisor，在报告时追加**一行** |
| 何时写 | 该次运行声明了 Target；对 Goal 整体运行则不带归因字段（既有形态，V-6） |
| 禁止 | 新增 Goal 字段、写 Goal 定义文件、由嵌套运行写该行 |

**V-5**: 一次报告的归因行最多一行；两行即判重复归因，MUST NOT 以「补充说明」为由再写一行。
**V-6**: 未声明 Target 的运行 MUST NOT 发明占位 Target；其台账行不带归因字段，这是既有 Goal 整体形态。
**V-7**: 归因 MUST 只经既有台账引用解析；解析出的 Goal 字段集在运行前后 MUST 完全一致（SC-002）。

## E3 SDD-host declaration and responsibility statement（父 E3 增量面）

| 载体 | owner | 本切片增量 |
|------|-------|------------|
| Agent 定义 frontmatter（`sdd-invocation: allowed`） | 中性键集 `src/specify_cli/__init__.py`（`074a` 已注册） | 无（只读引用） |
| Agent 定义职责正文 | 本切片：`skills/internal/run-agent/SKILL.md` § Authoring Baseline | 三条职责陈述的合规规则（V-8） |
| 出厂阶段执行者预设 | `agents/sdd-executor.agent.md` | 负向断言：不得声明该键（V-9） |

**V-8**: 声明 `[[STR-002]]` 的定义 MUST 同时写明三件事：承载驱动、自身不执行阶段命令、止于 review；声明与正文 MUST 一起被读取，只有声明没有三条陈述判不合规。
**V-9**: 阶段执行者能力 MUST NOT 声明 `[[STR-002]]`；该禁令 MUST 对出厂预设断言，MUST NOT 只对约定断言。

## E4 Team Stage vocabulary boundary（父 C-55 / C-66 Stage 面）

| 事实 | owner |
|------|-------|
| team Stage 取值集（`executor` / `evaluator` / `optimizer`） | `skills/internal/create-team/references/conceptual-model.md` |
| SDD 阶段名册 | `skills/external/sdd-loop-driver/SKILL.md`（本切片不复述） |

- 无存储：这是一条**词表边界**，不是新实体。
- 断言面：team Stage 取值集在改动前后逐字不变；新增文本中不出现名册形状的枚举（V-11）。

## E5 Routing pointer surface in the project instructions（父 C-56 投影）

| 事实 | value |
|------|-------|
| 载体 | `templates/instructions-template.md` 一个 `## ` 段 → `.specify/instructions.md`（既有生成器） |
| 内容面 | 何时到 owner 路径执行裁决；MUST NOT 出现输入集 / 取值域 / 裁决表 / 理由码词表 / 优先级第二条 |
| 生成方式 | `scripts/bash/generate-instructions.sh` 附加式注入；live 文件不手改 |

**V-10**: 指针面 MUST NOT 复述 owner 的输入集、取值域、裁决表或理由码词表。审计方式：先从落盘 owner 提取实际短语，再以这些短语为查询集对新文本反向计数（`shared/guidelines/one-source-of-truth.md` § Reference, don't copy）——MUST NOT 用「我以为写了的短语」作查询集。
**V-11**: 新增文本 MUST NOT 出现名册形状的 SDD 阶段枚举；阶段名册 owner 唯一（父 C-66，Stage 面）。

## E6 Routing verdict reference（父 E4 的只读消费面，D-2）

| 子项 | 规则 |
|------|------|
| 引用对象 | `074a` 在 Agent 执行证据中记录的那条裁决（输入、裁决、理由码、actor、用户覆盖） |
| 携带形态 | 稳定路径引用；段内不复制输入集、裁决表或理由码词表 |
| 缺记录时 | 记为 missing；外层 MUST NOT 重算、MUST NOT 以调用方叙述替代 |
| 写回 | 无 —— 本切片不产生也不修改裁决 |

**V-12**: 段内出现的裁决 MUST 是引用；任何在本切片内重新计算或改写裁决内容的行为判为越界（父 C-54，report 面）。

## E7 Containment case set（父 C-62 的治理实体）

| 字段 | 规则 |
|------|------|
| `suite_set_id` | 七个具名集合之一：`S1` pre-dispatch governance、`S2` standalone driver entry、`S3` 070 preset、`S4` 064 line/worktree/ownership、`S5` 058 U0–U6、`S6` team suites、`S7` Agent suites |
| `files` | 该集合纳入的文件路径列表（17 个文件，实测） |
| `node_ids` | `pytest --collect-only` 收集到的用例 node id 集合，逐行排序落盘 |
| `baseline_commit` | 冻结时的提交；本切片为 `33269994a` |
| 判据 | post ⊇ pre 且共享 id 裁决不变；**计数比较不合规** |

**Carrier**: `test-evidence/compat-baseline-nodeids.txt`（266 例 / 17 文件 / 7 集合）。它是证据工件，不是新存储：无引擎写它，无查询面消费它。

## E8 Additivity surface set（父 C-61 的四面）

| # | 面 | 既有形态（不得删/改名/改义） | 本切片动作 |
|---|----|------------------------------|------------|
| 1 | 独立 `sdd-loop-driver` 入口契约 | 入口形式、键、退出码、默认解析行为 | 无改动（只读） |
| 2 | Feature 070 阶段团队预设契约 | 预设键、段、入口形式 | 无改动（只读） |
| 3 | Feature 064 线 / 工作树 / 归属契约 | 线注册表字段、工作树形态、归属与集成队列接口 | 无改动（只读） |
| 4 | Feature 058 U0–U6 契约 | 阶段语义、哨兵、独立验证、watcher 判定/退出码、卡死处置、测试预算规则 | 无改动（只读） |

本切片对这四面**只加不改**：报告段是对运行报告的追加，指令指针是对模板的追加，职责陈述与阶段消歧是对既有段的追加，触发句是对既有段的追加。

---

## 状态机 1 — Report-section composition

```text
run starts (existing pattern)
   │  nested invocations declared by authorized seats (074a surface, cited)
   ▼
invocation #k ends → handoff (closed field set, 074a) ── outcome ∉ {completed} ──► row records it verbatim
   │ outcome = completed                                                   │
   ▼                                                                       ▼
row: outcome + artifact paths + evidence paths + verdict reference + anomalies
   │  no invocation at all
   ├──────────────────────────► section states "no nested SDD invocation" explicitly
   ▼
supervisor writes the report (section present, peer of Verification)
   │  Target declared by the run
   ├── yes ──► exactly one ledger item carrying the existing Target reference
   └── no  ──► ledger item without the attribution field (Goal-wide form)
   ▼
outer layer adjudicates integration (never the nested run; no merge, no push)
```

Terminal states of the section: `has rows` / `explicitly none`. There is no "absent" state — E1 V-2
and C-23 make an omitted section a violation, not a third value.

## 状态机 2 — Containment verification

```text
baseline capture (pre-change, at the commit in the verification record)
   │  pytest --collect-only → node-id set per named suite → frozen carrier
   ▼
edit lands (this slice's four diffusion surfaces + the report section)
   │
   ▼
post-change collection (same command, same file list)
   │
   ├── post ⊇ pre for every set ──► shared-id verdicts compared ──► claim satisfied
   │                                                    │
   │                                                    └─ any shared id flips ──► claim failed, named id + verdict
   └── pre \ post non-empty ──► claim failed, dropped ids listed (never "roughly equal")
```

The third element of the parent's state-machine family — the nested-run lifecycle — lives in
`074a`'s data model and in the driver; it is not restated here.
