# Phase 0 Research: 072-client-self-improvement

**Requirement → Feature**: `072-client-self-improvement` → Feature 072 客户项目的持续反馈与自我提升（Client-Project Feedback & Self-Improvement）

本节是 `/speckit.plan` Phase 0 的独立研究报告（>50 行、含对既有引擎实测）。所有结论均来自对本仓代码的实测引用；每条决策给出被否决的替代读法。探测时间 2026-10-27，基线提交 `8ab5e5a9` 线（HEAD `dce7790c`）。

## R1 — 采集步骤的载体：脚本子命令，而不是技能正文里的引擎调用

**裁决**：代码段非交互路径的第五步落地为 `skills/internal/code-review/scripts/git-delta-review.sh` 的新子命令 `capture --review-file <record> --triage <value> [--unit <custom:owner/name>]`，由它完成武装态解析、计数抄录、引擎落盘与披露行输出的全部确定性工作。

**实测依据**：非交互路径现有四步（`skills/internal/code-review/SKILL.md` § 非交互路径）各由一个确定性子命令承担（`base` / `start` / `note` / `receipt` + `report --summary`）；引擎侧 `feedback-utils.py --action record` 的幂等键是 `(unit_id, run_id)`（源码 783–793 行：`existing = next(e for e in entries if unit_id and run_id match)`），重复记录返回 `duplicate: True` 而不新增文件。

**被否决**：(a) 由技能正文写出 `feedback-utils.py` 调用序列——组装的指针载荷与退出码映射散在散文里，"发现必须进入通道"不再是机械可核验事实；(b) 新引擎——简报红线禁止；(c) 在 `receipt` 子命令内顺带采集——回执是 071 冻结面（退出码字母表与字段块封闭），叠加采集会让"采集失败"与"回执缺口"共用一个退出码，违背 FR-009 的披露闭集。

## R2 — 运行标识：记录头日期戳，而不是收尾运行判定 id

**裁决**：指针条目里的「本次运行的标识」= 代码段记录头的 `日期` 字段值（ISO-8601 UTC 秒级，与归档文件名 `code-review-<stamp>.md` 同源），测试可用 `REVIEW_RUN_TIMESTAMP` 环境变量固定（`git-delta-review.sh:529` 实测存在该覆盖点）。

**理由**：第五步执行时收尾尚未发生，运行判定 run id 还不存在；记录戳在 `start` 时生成、全程不变、天然与记录 1:1，同一 run 重复采集的幂等性因此落到引擎已有的 `(unit, run)` 键上。SC-001 的"按运行标识过滤"用 `list --format json` 的 `run_id` 字段完成。

## R3 — 计数来源：`report --summary` 新增可选 `--format json`，既有文本形态与退出码字母表不动

**裁决**：FR-007 要求计数"逐项抄自既有汇总命令输出"。现有 `report --summary` 的文本输出带严重度图标（`printf "%s %-12s %s" icon [sev] count`），机读脆弱；本设计为 `report` 增加**可选** `--format json`，输出 `record` / `counts{六项}` / `blocking_entries` / `gate`，退出码字母表 0/1/2 原义不变，既有文本输出逐字不动。

**被否决**：(a) 解析带图标的文本——图标集漂移即静默错计数；(b) 由 `capture` 直接重数记录文件——违反 FR-007「MUST NOT 由人或代理另行清点」，且与汇总命令形成第二计数源；(c) 用回执的文件级计数——FR-025 明确捕获计数取意见级计数，不依赖回执的"非代码/未评审"区分。

## R4 — 武装态解析：探针注册表的外部对象计数，注册表缺失即 fail closed

**裁决**：`capture` 调用 `probe-utils.py --action probes --format json`（实测输出含 `available` 与 external 对象数组；外部对象校验规则在 `probe-utils.py:270–286`：`object_id` 以 `ext-` 开头、`class kind=external`、`unit` 匹配 `custom:<owner>/<name>`）。解析顺序：显式 `--unit` > 唯一外部探针对象 > 其余。注册表不可用 → `client-channel-unarmed`，且不调用 record（实测 `feedback-utils.py` 在注册表缺失时会写无 `kind`/`slice` 的遗留条目——这正是需求 Edge Case 点名的随包上送泄漏路径，所以 fail closed 必须发生在调用 record 之前）。

## R5 — 显式单元参数的字面量：`--client-unit <custom:owner/name>`

**裁决**：评审命令的可选参数字面量为 `--client-unit`，值语法封闭为 `custom:<owner>/<name>`（与引擎 `_CUSTOM_UNIT_RE` 一致）。命令模板只做透传，语义全在 `capture` 一个 owner。畸形值（不满足 `custom:` 语法）→ `capture` 输出具名 skip 行（写明期望值语法）、零条目、退出 0——第五步永不阻断评审运行（FR-008）；参数校验不前置到命令模板，避免第二处校验面漂移。

## R6 — 框架帽披露的文本形态：帽子依据句，不混入五值闭集

**裁决**：需求把客户端通道状态的披露闭集封在五个字面量（STR-003/004/007/009/010）内；「框架项目（含 vendored 框架源的客户仓）」不是通道状态而是帽子判定结果。`capture` 在框架帽下输出 `client-capture: skipped: <帽子依据句>`（引用两顶帽子 owner 判据），永不写条目（US6 验收场景 3）。该形态不属于五值闭集、也 MUST NOT 伪装成五值之一——闭集只在帽子=客户项目时生效。这是对需求 Edge Case「MUST 明确说明本次未采集及其依据」的落法，记为计划级裁决（语义已由 FR-001/Edge Cases 固定，此处只定文本形态）。

## R7 — 四条度量：既有引擎上的一个只读新动作（Program-First）

**裁决**：度量由 `feedback-utils.py` 新增只读动作 `--action client-metrics [--unit <custom:...>]` 计算，每次呈报即读即建，输出 JSON（每指标 `status: evaluated|not-evaluated`、`numerator`、`denominator`、`reason`，重复率带 `proxy: true`），无写盘。

**被否决**：(a) 由代理从 `list --format json` 输出推导——违反 Token Efficiency 的 Program-First（可固定的规则推导必须落在程序里）；(b) 独立新脚本——第二个引擎面，且需自行处理 store 路径解析；(c) 并入 `status` 动作——status 是存量形态，混入四指标会破坏其既有契约测试。

**四条指标的确定性口径**（实现期不得再发明）：
1. **捕获覆盖率** = 已有对应外部条目的代码段记录运行戳去重数 / 代码段记录运行戳总数。分母口径：只统计「通道武装之后」的记录——以该单元（或全部外部单元）最早一条外部条目的 `created` 戳为界，早于该界的记录排除且不补造（FR-020 不回填的机械落法）；排除数在输出里披露。
2. **进入回路比例** = 已被指派载体的外部条目数 / 外部条目总数（载体指派以路由台账 backlog 行的 `carried-by-*` 形态为准）。
3. **闭环比例** = 有 owner 文件变更证据的外部条目数 / 外部条目总数。闭环证据的机械定义：backlog 行形态为 `carried-by-spec-*`（或对应 todo/improve 载体行）且其指名的 owner 文件存在、其 mtime 晚于条目 `created`；`--action dispose` 的 `processed`/`ignored` 只是本地元数据，`open-unverified` 行 MUST 先复测——这两条是「路由≠完成」的具名锚点（FR-021），处置标记 MUST NOT 被当作闭环证据。
4. **重复发现率**（粗代理） = 其记录内任一 `(文件, 严重度)` 对在该单元更早条目的记录里已出现的外部条目数 / 外部条目总数。(文件,严重度) 对从条目所指记录的正文确定性抽取；指针条目本身不带文件明细（FR-007 的封闭字段集），所以该指标读的是条目所指的记录——这是指针形态下唯一诚实的复算方式。所指记录不可读的条目从分子分母同时排除并在输出里给出 `excluded` 计数与原因（FR-023「不省略该行」的落法：行在，口径披露）。

## R8 — 客户项目夹具：临时 git 仓 + 框架安装出的最小 `.specify/`，五组行为各一份确定性检查

**裁决**（FR-029/SC-006 的落法）：pytest `tmp_path` 夹具构造：(1) 临时 git 仓（`git init` + 用户配置）；(2) 从本仓复制最小 `.specify/` 运行时——`scripts/python/` 的既有引擎（`feedback-utils.py` / `probe-utils.py` / `run-determination.py` / `evidence-utils.py`）、`shared/definitions/probe-definitions.md`、`memory/feedback/` 目录，**根级不存在** `templates` / `skills` / `shared` / `scripts` / `src/specify_cli` 五目录 → 帽子判定走客户分支；(3) 引擎以绝对路径 + `--workspace-root <fixture>` 调用；评审脚本以 cwd=<fixture> 调用。先例已存在：`tests/contract/test_feedback_probe_registry.py:42–65` 的 `_workspace` / `_external_probe` / `_embed_workspace` 同款构造。**框架帽孪生夹具**：同一构造 + 根级建五个空目录（帽子谓词只测目录归属，空目录即满足），证明同一流程在框架仓走另一分支、不产生任何外部条目（US6 验收场景 3 的确定性覆盖）。五组行为 → 五个测试文件：`test_client_capture.py`、`test_client_armed_state.py`、`test_client_package_exclusion.py`、`test_client_improve_loop.py`、`test_client_metrics.py`，各做一次记录在案的红先行运行（命令行、退出码、失败计数）。

## R9 — 消化与载体的落点：Path A 引用文档 + 命令模板，不新增消费路径

**实测**：`manage-feedback` 路由表已把 `kind: external` → Path A、Path B 打包侧引擎无条件排除外部条目并只报 `excluded_external` 计数（`feedback-utils.py:1871–1892` 实测）。本特性在 `references/path-a-digest.md` 的 A4（渠道路由/backlog 写入）处增加：每条被消化外部条目恰好指派一个后续载体（闭集三值：todo Park 模式 / 新需求规格 / 改进循环主体；Park 为默认落点），指派写入 backlog 行并在呈报里列出；呈报增加三项既有事实（帽子+武装态及解析路径、两侧条目数与处置、四条度量读数）。载体边界与存放位置引用各自 owner（todo-in-context 指南、requirements 流程、自我提升流程），不复制。

## R10 — 改进循环的落点：workflow 的一处观察源规则 + 一处披露字面量

**实测**：`templates/commands/improve.md` 已承认 `custom:<owner>/<name>` 目标按解析后实体路由；`run-determination.py:1228–1246` 的持久化适配器对 `custom:` 单元返回 `persisted: False` + reason（来源契约只接受命令/技能两种形态），且 `tests/contract/test_run_determination_engine.py:1393` 已钉住"custom 单元如实报告而非丢弃"。本设计在 `shared/workflow/self-improvement-workflow.md` 的 SI-1 观察源处增加一条规则：`custom:` 主体的 why 段以「客户通道条目（该单元的外部条目）+ 既有证据车道」为观察源，并明写披露句「运行判定历史未评估」及引擎给出的 reason；MUST NOT 发明来源字符串、MUST NOT 伪造历史。来源契约的加宽是运行判定引擎 owner 的动作，超出本特性范围（FR-015 原文）。

## R11 — Dogfooding Loop B 配方改写的位置与边界

**实测**：`shared/guidelines/dogfooding.md` 第 22 行仍是旧配方 `--unit-id "skill:<scenario-name>"`。按 FR-003 + A7，实现期把该处改写为 `custom:<owner>/<name>`（unit-type `custom-unit`）并给一句理由（`skill:` 词族在客户项目里要么无探针对象被拒、要么被解析为框架内部单元而随包上送）；Loop B 其余行（memory/history/review/任务记录的定位、advisory 性质、反模式清单）逐字不动。改框架源，`shared/` 镜像由 `sync-mirrors.py` 落位。

## R12 — 同步面基线（漂移预算）

**实测**（2026-10-27）：`sync-mirrors.py --check` 报告 1 处**既有**漂移 `.specify/skills/improve-skills/references/loop-playbook.md`（宪法 Sync Impact Report 记录的遗留分歧，与本特性无关）；`regen-command-copies.py --check` 全绿。本特性的通过判据 = **本特性触及的镜像对无新增漂移**（不预设绝对全绿）。
