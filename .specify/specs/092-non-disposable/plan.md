# Implementation Plan: Non-Disposable（不可一次性处置）

**Branch**: `master` | **Date**: 2026-11-09 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `092-non-disposable` → Feature 092 Non-Disposable（不可一次性处置）
**Input**: Specification from `.specify/specs/092-non-disposable/requirements.md`（65 FR / 20 SC；clarify 2026-11-09 裁定 D-1…D-8；validate corpus `.specify/specs/092-non-disposable/notes/input-review-080-090.md`）

## Summary

这条特性把「过期 / 无用 / 延期」从一种**沉默的默认状态**变成**必须被处置的状态**，并把
`/speckit.history` 从「把会话蒸馏成主题文档」升级为「**回顾 → 设计 → 用户确认 → 执行**」。

```text
回顾 (review)   —— 只读 HEAD 工作树的十个 .specify/ 历史目录（声明式根集合；不读 git 历史）
    |              确定性面 = 新只读引擎；语义面 = 既有 085 spec-local team 的大并发 subagent
    v
报告 (NDR)      —— 每条：位置 / 类别 / detection / 证据引用 / 严重度 / 状态 / 建议处置
    |
设计 (design)   —— 逐条拟处置、影响路径、可逆性；一次确认请求结束该段（零写盘）
    |
确认 (confirm)  —— group / item / none-of（缺省 group）；未确认项 = unconfirmed，可见、不计闭合、不自动重试
    |
执行 (execute)  —— 修复 lane：按确认分组落盘，组边界一次证据；archive-not-delete；四段证据入 test-evidence/
```

**七面落地，零新增原则**（D-2）：owner 页（新）· 声明层事实（新）· 术语表四条 · 特性注册表行与详情 · 既有
`pytest -m contract` 守卫（含变异腿）· 三份历史面**指针**（各一行）· `register.md` 决定条目。两条宪法计数 pin
保持原值，MUST NOT 新增常驻顶级 `##` 章节。

**复用而非新建**（FR-059）：唯一 history 入口（`manage-history` + `templates/commands/history.md`）、唯一蒸馏
存储（`.specify/history/`）、`sanitize-utils.py` 四封闭集（逐字不变）、`closure-acceptance-check.py` 的裁决与
reason code、`renumber-utils.py` 的活绑定/历史记录判据、`shared/declarations/facts/` 声明层、085 的 spec-local
team 与并发。新增只有三件：一个只读引擎、一个事实声明文件、一个 owner 页。

**验证底座**是 A–H 语料：35 条逐条落表（档 I / 档 II），引擎 MUST 在本树复现这些发现，修复 lane 跑完后档 I
项按名归零，档 II 项转为一条可复核的 shift 清单。

## Technical Context

**Language/Version**: Python `>=3.8`（`pyproject.toml:5`；实测解释器 `/usr/bin/python3` = CPython 3.11.0rc1）承载新只读引擎与契约守卫；Markdown 承载 owner 页、契约、命令模板与技能。
**Primary Dependencies**: 零新增。新引擎只用 stdlib（`argparse` / `json` / `re` / `pathlib` / `hashlib` / `subprocess`），并复用既有同目录模块 `declaration_reader.py`（声明层唯一读入口）与 `renumber-utils.py` 的判据函数。
**Storage**: **零新存储**。回顾段与方案段零写盘；确认段若需落盘一份方案，落 `.specify/.tmp/`（git-ignored）并由执行段删除；执行段证据落 `.specify/specs/<spec-dir>/test-evidence/`，**一次运行一个文件**（Concurrent Development Safety）。`.specify/history/` 仍是唯一蒸馏存储且本特性只读它（FR-044）。
**Testing**: `pytest -m contract` 内的新增守卫文件（FR-062），不新增门禁步骤；每类检出至少一条**变异腿**（把被守物弄坏后断言转红），因为「不会变红的绿不是证据」。
**Target Platform**: 任何加载该框架的主机（Markdown 面随 `specify init` 分发；引擎与守卫需 CPython ≥3.8 与 git CLI，后者只用于 `git mv` 语义与零写盘快照）。
**Project Type**: SDD 框架自宿仓库（`shared/` + `templates/` + `skills/` + `scripts/` + `tests/` 为本仓 `.specify/` 的源）。
**Performance Goals**: 回顾面本阶段实测 **4,357** 个文件（R10）。目标不是吞吐而是**可完成性与确定性**：引擎单次全量扫描在数十秒量级（纯 stdlib 目录遍历 + 正则，无网络、无模型），语义面交给分片 subagent；同树不同并发度 MUST 得到按名相同的条目集合（FR-049），所以并发只影响墙钟。
**Constraints**: 只读引擎零写盘、退出码 0/1/2 三值；`sanitize-utils.py` 四个封闭集逐字不变；不新增第二个 history 入口 / 第二套存储 / 第二套调度；不删任何文件（`archive-not-delete`）；回顾不读 git 历史；宪法两条计数 pin 与 `sanitize-utils.py` 字面是 closed-set 的「被守物」，突变即红。
**Scale/Scope**: 65 FR / 20 SC / 35 条 A–H 语料 / 8 个检出类别 / 7 个落点 / 7 条契约；新增 3 个源文件（引擎、声明、owner 页）+ 1 个契约守卫文件，改动 6 个既有面（命令模板、技能、术语表、注册表 + 详情、register、三处指针）。

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Rendered by enumerating every `### <numeral>. <name>` heading of `.specify/memory/constitution.md` (v1.19.0, 22 principles), in file order. The feature deliberately adds **no** principle (D-2), so the roster below is the whole roster and none of its rows is this feature's own.

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every design element cites an FR: engine → FR-010/011/039/061, seam → FR-029…FR-045, landing → FR-063. `contracts/` carries a per-clause FR citation group, not a header-only mapping. |
| II | Feature-Centric Development | ✅ Pass | FR-063 落点 4: registry row + `.specify/memory/features/092.md` land in the same batch; status moves Draft → Planned at this stage (no regression: 092 has no Implemented history). |
| III | Intent-Driven Development | ✅ Pass | The user's four-stage form, the ten-root review surface and the "no deferral" rule are recorded verbatim in the state spine's `goal_verbatim` and mapped one-to-one in § Summary; `T-001`/`T-002` keep the two places where "what" and "how" could drift apart. |
| IV | Test-First & Contract-Driven Implementation | ⚠ Partial — see Complexity Tracking | FR-062 lands the guards in the existing `pytest -m contract` set with a mutation leg per closed set, but the guards can only be written after the engine exists (the engine *is* the subject). Row 1 of Complexity Tracking. |
| V | AI Agent Integration Standards | ✅ Pass | No new agent CLI, no new provider, no change to `AGENT_CONFIG` / `_ASSISTANT_TIERS`. The semantic face runs on the existing native-subagent path. |
| VI | Continuous Quality & Observability | ✅ Pass | Exit codes 0/1/2 + `--json` give the engine one observable surface; every repair carries before/after readings; no symptom suppression — `unevaluated` is a visible non-clean state rather than a pass (FR-005). |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | This plan is the stage artifact; FR/SC counts are read from the artifacts (65/20), never attested; `/speckit.tasks` follows with the package proposal below. |
| VIII | Code as the Single Source of Truth | ✅ Pass | The status check consumes `closure-acceptance-check.py`'s verdict, not a document's claim (FR-026/FR-028); the ceilings question in R9 is settled by reading the engine constants, not the specs that quote them. |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | Three new files, zero new directory, zero new daemon/scheduler/registry/scorer; the engine is a single stdlib script beside `sanitize-utils.py`. `T-001` records the rejected alternative of a hosted review service. |
| X | Documentation Naming & Location Conventions | ✅ Pass | `shared/definitions/non-disposable-definitions.md`, `shared/declarations/facts/non-disposable-review-surface.yaml`, `scripts/python/non-disposable-check.py` — lowercase kebab, path-is-semantic, no reserved ALL-CAPS name, no nested README. |
| XI | Dogfooding (Self-Application) | ✅ Pass | This feature is a *mechanism* fix (its own subject); instance-side patches are banned by FR-058/FR-054. Two hats named: the engine and owner page land in the framework sources (`shared/`, `scripts/`), the runtime copies are produced by `sync-mirrors.py` and never hand-edited. |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | No `.specify/memory/tools/` record covers "find stale carriers"; a new engine is the expected outcome, and it reuses `declaration_reader` / `renumber-utils` / `closure-acceptance-check` instead of re-deriving their judgements (R5, R8, R3). |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | The review surface strengthens *Learning Capture* and *Change Validation* by naming the harness file that fails them today; the evidence discipline is kept (`configured ≠ used`), and no new scoring system is introduced. |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | This feature *is* the discipline's enforcement: FR-001 names the owner page, FR-018…FR-021 detect multi-owner, and the plan's own § Fact Owners names one owner per fact; nothing in the delivery restates the disposition tables. |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | The report and the design segment are written for the baseline reader of `shared/guidelines/user-facing-comprehension.md`; § Human-Facing Output Shape in `data-model.md` fixes the four questions a reader must be able to answer. |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | The stage surfaced three corrections (R6 spelling, R9 F1 shape, D-id registration) and one open decision pair (OI-4 / OI-5) instead of smoothing them; the engine's `unevaluated` state is the same discipline in machine form. |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | Zero new directory. The declaration lands in an existing registered directory; the only temp write goes to `.specify/.tmp/`, already git-ignored and owned by `temp-directory-discipline.md`. |
| XVIII | Grounded Naming | ✅ Pass | Every name is taken from the user's words or the closest sibling: `non-disposable-check.py` (sibling `sanitize-utils.py`), `non-disposable-definitions.md` (sibling `*-definitions.md`), fact slug `non-disposable-review-surface` (sibling `flow-class-classes`); no invented vocabulary — `deterministic`/`semantic` and the four dispositions come from requirements. |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | A report entry carries location, class, evidence and disposition in one place so a reader can act without opening another file; the coverage declaration answers "what was scanned" at the entry point instead of leaving it to inference. |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | The new guards are pure-file assertions with no subprocess except the engine itself (measured runs, no daemon); the engine is invoked once per scenario group, not once per assertion. No selection is shrunk to buy speed. |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | FR-061 + FR-010: the new engine answers `-h`/`--help`/`--version`, rejects undeclared options with exit 2, and writes nothing in any mode; `contracts/detection-engine-cli.contract.md` makes those the guarded clauses. |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | § Execution Premises carries the premises; the stage's own U4 runs the checkpoint protocol's fifth part; the driver's five-question audit is a statement, never an approval request. |

**Gates Status**: ⚠ One Partial row (IV) with a matching Complexity Tracking entry; no ❌ Fail.

**Re-check after Phase 1** (2026-11-09, after `data-model.md` / `contracts/` (7 files, 54 clauses) / `quickstart.md` (10 scenarios) / `feature-ref.md` landed, and after all three gate readings were taken — `test-evidence/plan-gates.txt`): the table was re-read against the Phase 1 artifacts and no row moved. Principle IV stays ⚠ Partial for the same single reason — the guards are implement-side deliverables (`SC-005`…`SC-019`), and a plan cannot claim a guard it has not landed. Row XIV was re-read against `data-model.md` § Fact Owners and stays ✅: every fact the plan names has exactly one owner row and no second statement.

## Decision Tensions

*Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing threshold: `.specify/shared/guidelines/decision-tension.md` — one pointer, read from the repository root. This section lists the field names and points at that file; it MUST NOT restate the criteria table, the rejection list or the threshold table.*

Fields: `decision`, `antithesis`, `binding_constraints` (with `pole_a` and `pole_b`), `discriminating_evidence`, `expected_sacrifice`, `revision_trigger`; record identifier `tension_id` (`T-NNN`).

### T-001 — 检出引擎是本地只读脚本，而不是常驻的回顾服务

- **decision**: 回顾的确定性面落成 `scripts/python/non-disposable-check.py` 一个 stdlib 只读单文件引擎（退出码 0/1/2、`--json`、`--scope` 分片），每次跑完即退出，无状态、无缓存、无守护进程。
- **antithesis**: 建一个常驻的回顾服务（索引化 `.specify/` 的历史目录、增量更新、查询接口），让报告成为可挂载的观测面；当树规模增长到单次遍历无法在一分钟内完成、且多个团队需要共享同一份带索引的报告时它更优——查询是瞬时的，且跨运行可比较。
- **binding_constraints**:
  - pole_a: 本特性 MUST NOT 引入第二套存储、第二套调度或守护进程（FR-059 / FR-044 / 宪法 IX）；任何需要被持续保存的结论都已有 owner（报告、证据文件、`.specify/history/`），再建索引就是第二个真相。
  - pole_b: 回顾 MUST 对一棵已经前行很多特性的树仍然**能跑完**，且「跑了多少」可被核对（FR-011 覆盖声明）；一个需要预建索引才有结论的机制，在第一次运行时就无法回答「查了什么」。
- **discriminating_evidence**: 在一棵 `scripts/python/non-disposable-check.py` 从未运行过的干净副本上直接跑一次全量扫描，测墙钟；结果二值——墙钟在单次会话的可接受等待内完成（是／否）。为「是」则常驻索引的收益不足以支付它的存储与失效成本；为「否」则本决策重开。
- **expected_sacrifice**: SC-014 Source ↓ 覆盖声明的候选计数每次都要重新遍历树，无法跨运行复用；本阶段实测 4,357 个文件的全量遍历因此是可重复但不可加速的开销。
- **revision_trigger**: 连续两次实测单次全量扫描墙钟超过 5 分钟，或出现 ≥2 次「需要跨运行比较同一路径的历史报告」→ 重开，评估在 `.specify/.tmp/` 下建一次性索引（MUST NOT 落成被追踪路径或第二套存储）。

### T-002 — 宪法原则的落点由原话判定为「不新增」，缺口以持久 OI 承接

- **decision**: 本特性 MUST NOT 新增宪法原则、MUST NOT 改动模板与本仓宪法的原则名单（FR-063 / D-2）；规范力来自 owner 页 + 方案确认门，缺口作为 OI-4 长期开放并上报。
- **antithesis**: 把「遗留载体必须被处置」补成一条宪法原则（模板 `XXIII` / 现网 `XXIII`，按既有五处落点 + 三计数 pin + Sync Impact Report 同批落地）；当这条规范必须**压过**任何局部判断（例如当某条正文的作者认为「这条还有用」时，读者仍然无条件地必须处置它）时它更优——只能靠 MUST 级的治理面提供，owner 页提供不了。
- **binding_constraints**:
  - pole_a: 本阶段 MUST NOT 推定一个原话未记载的范围扩展（`direction_contract.goal_verbatim` 逐字无「宪法 / 模板 / 指令面」字样）；宪法修订是用户保留的判定权，plan MUST NOT 代行。
  - pole_b: 缺口 MUST 在上报面持续可见，MUST NOT 因为不落原则就被读成「没有缺口」；OI-4 与 OI-5 两条 MUST 保持 open 并在本 spec 的 Open Items / register 中可查。
- **discriminating_evidence**: 取用户的一轮新指令，检查其中是否出现指向治理面的显式要求（例如「成为一条原则」或指名宪法/模板）；结果二值——出现（是／否）。为「是」则本决策的「不新增」前提被推翻并重开；为「否」则 owner 页 + 确认门是当前规范力的正确上限。
- **expected_sacrifice**: SC-011 Source ↓ 七面核对里没有一条宪法计数位移可被本特性断言，「机制存在」与「机制有宪法级强制力」之间的差距因此只能靠 OI-4 的文字承担。
- **revision_trigger**: 用户以任何形式裁定补一条原则（OI-4 关闭），或出现 ≥2 次「owner 页写明必须处置、但被以『作者认为还有用』为由绕过」→ 按 FR-065 的完整 MINOR 流程重开，本特性此前不预写的条号与 pin 值届时实测。

### T-003 — 确定性面与语义面的分界由「读物能否被程序读出」决定，分界处的降级必须是 `unevaluated`

- **decision**: 一个检出条目的 `detection` 只由断言对象决定（文件/行/字段/字面量/计数/路径/可解析引用 → `deterministic`；只有理解自然语言含义才成立的断言 → `semantic`）；任一侧不可判定时落 `unevaluated` 并计入未闭合，MUST NOT 降级为「无检出」。
- **antithesis**: 让大并发 subagent 承担全部分面（含结构性命题），把这些命题交给模型在完整文件上下文中一次判完；当结构性命题的判据本身只在自然语言里成立（例如「这一段的措辞是否仍与它声称引用的 owner 一致」）时它更优——同一套判据不需要为机器与模型各写一遍。
- **binding_constraints**:
  - pole_a: 一个自称确定性的条目 MUST 可被程序复算（FR-004）；把「命中关键词」冒充「判定为过期」会把误判源注入报告，且这类条目无法独立复核（Edge Case「语义判定被裁成确定性命中」）。
  - pole_b: `semantic` 条目 MUST 携带两处路径 + 行号（FR-004 / FR-048），且 subagent 返回不合规时该片 MUST 可见为未评估；否则「大并发」只是把不确定性放大到不可见。
- **discriminating_evidence**: 把同一个语义命题分别在 (a) 确定性引擎的关键词/结构判据下与 (b) 一位复核者按两处引用逐条复核下判一次；结果二值——两者 verdict 一致率 100%（是／否）。为「是」说明该命题其实可判定、应迁到确定性面；为「否」说明它必须留在语义面并携带引用。
- **expected_sacrifice**: SC-016 Source ↓ 每一条语义条目都要带两条可解析引用，报告体积与复核成本因此高于「只给结论」的形态；分界处一旦判错，代价是条目在两侧来回搬家。
- **revision_trigger**: 出现 ≥2 次「同一命题被两侧判出相反 verdict 且两侧都自认为合规」→ 重开，把该命题的判据改写为 owner 页的一条可判定定义，或明确把它降级为 `unevaluated` 常态。

### T-004 — 处置词汇两套共存不合并，映射表与裁决规则写一次

- **decision**: Non-Disposable 处置集 `archive/supersede/correct/exempt` 与 `sanitize-utils.py` 的 `DISPOSITIONS` 保持两个各自封闭、互不合并的集合（FR-012 / D-1 / OI-2）；两者之间只通过 owner 页「处置映射」一节的两张封闭表（逐值映射表 + 不可映射项表）和一条裁决规则（检出来源引擎决定处置词汇）发生关系。
- **antithesis**: 合并成一套词汇（把 `supersede` / `correct` / `exempt` 并入 sanitize 的 `DISPOSITIONS`，或反向把 `delete` / `dismiss` 并入本特性），让「处置」在全框架只有一个词表；当用户阅读一次回顾报告、不希望同一件事在两处有不同名字时它更优——词汇负担减半。
- **binding_constraints**:
  - pole_a: 合并 MUST NOT 改写 Feature 047 已交付的封闭集与台账（FR-060 逐字不变）；`delete` 与 `exempt` 的语义在本特性里分别是**禁止**与**必须有到期条件**，把它们塞进同一个集合会让「材料卫生可删除」与「历史证据不可删除」这对相反的约束共用一个词。
  - pole_b: 两套词汇 MUST NOT 变成互不知情（A9 / OI-2）：4 × 5 的笛卡尔积每一对 MUST 命中某一张表（SC-015），且同一候选 MUST NOT 被两个引擎各处置一次。
- **discriminating_evidence**: 取一个既被材料卫生引擎报为候选、又被本特性判为过期的具体条目，让两个引擎各跑一次；结果二值——两条报告是否指向同一次处置（是／否）。为「是」说明裁决规则未生效、需要重开；为「否」说明共存形态成立。
- **expected_sacrifice**: SC-015 Source ↓ 维护者每新增一个处置值就要同时维护两张表并在两个引擎里各接一次，成本高于单一词表；两张表的一致性只有一条契约测试在守。
- **revision_trigger**: 出现 ≥2 次「同一候选被两个引擎各处置一次」的实测（SC-015 变异腿判绿而不是判红）→ 重开，改为单一词表并要求一次 MINOR 级契约修订；或出现 ≥3 对「既不命中逐值表也不命中不可映射项表」的第三态 → 重开表的封闭性。

### T-005 — A–H 逐条落表分档，按类别判据而非按发现的心情

- **decision**: A–H 的 35 条按 FR-056 的类别判据分两档（档 I 机制缺失 → 本特性交付机器 + 首轮修复并在本特性内归零；档 II 某条既有特性的正文陈述错误 → 只交付检出 + shift 清单 + 一条移交标记），逐条落表见 § A–H Corpus Mapping (per-entry)。
- **antithesis**: 全部由本特性一次修完（档 I 全覆盖：把 081 / 083 / 084 / 086 / 088 / 089 / 090 的正文一并改到位），让「驱动到零」在字面上成立；当这棵树上没有别人依赖那些正文、也没有别的特性线会同时改它们时它更优——一次收口，不需要移交协议。
- **binding_constraints**:
  - pole_a: 档 II 项 MUST NOT 在本特性的实现里被直接改写（FR-056 / FR-045）：`/speckit.history` 不是批量改写他人已交付正文的旁路，改写他人正文必须由那条特性的线带着自己的规格与证据去做。
  - pole_b: 档 II 项 MUST NOT 从而消失（两档都有上报义务）：shift 清单必须逐条点名「语料编号 → 承接特性 → 应当改哪个文件」，并在原正文留一处可复核的移交标记；「移交」不是「免责」。
- **discriminating_evidence**: 对每一条档 II 项，检查「修复它的正确位置是否就是那条特性的正文」；结果二值——是（留在档 II）／否（应改判为档 I）。判据只看修复位置，不看缺陷大小或修复难度。
- **expected_sacrifice**: SC-020 Source ↓ 本特性的「归零」统计不含档 II 项，所以「A–H 驱动到零」在报告里会分成两个数字（档 I 归零 / 档 II 移交），比单一数字难读。
- **revision_trigger**: 出现 ≥2 次「档 II 项移交后，承接特性线在合理周期内未处置，且该正文已被下一次取代再次引用」→ 重开，评估把该类别（而非该条）升为档 I，并把升档写成类别判据的一次修订。

### T-006 — 语义面复用 085 的 spec-local team 与既有分片协议，不新建并发设施

- **decision**: 回顾的语义面由 `085` 的 spec-local Temporary Goal/Team（slug `092-non-disposable`）承载，并发度取状态脊的 `agent_concurrency_requested`（本线 24），有效值按既有声明公式取最小值并带具名理由降级（FR-046 / FR-050 / D-7）。
- **antithesis**: 为回顾专门写一个分片调度器（自己的片定义、自己的重试、自己的结果合并），让回顾的并发形态与阶段执行解耦；当回顾需要跑在「没有正在进行的 SDD 阶段」的时刻（例如用户在任意时刻手工触发一次全树回顾）时它更优——不必借用阶段的生命周期。
- **binding_constraints**:
  - pole_a: MUST NOT 新增第二个调度器、第二个并发上限常量或第二套派发协议（FR-050）；并发上的每一个数字都必须能追到既有声明。
  - pole_b: 回顾 MUST 仍能把 4,357 个文件在可接受时间内判完，且分片 MUST 互不重叠、并集覆盖候选集合、无空片（FR-047），不同并发度 MUST 得到按名相同的条目集合（FR-049）。
- **discriminating_evidence**: 以并发度 24 与并发度 4 各跑一次同一棵树的分片回顾，比较条目集合（按名）；结果二值——两次按名相同（是／否）。为「否」说明分片协议有隐藏的顺序依赖，必须先修协议再谈并发。
- **expected_sacrifice**: SC-009 Source ↓ 回顾无法在团队未创建时运行（FR-051 要求 clarify 与 plan 双 U4 之后才建 team），所以「随时可跑的一次回顾」这一便利被放弃。
- **revision_trigger**: 出现 ≥2 次「用户要求在没有活动阶段的树上手工跑回顾、而 team 机制无法承载」→ 重开，在既有 085 契约内追加一种触发形态（MUST NOT 新建第二套并发实现）。

### T-007 — 豁免是有限期的，不引入「永久豁免」

- **decision**: `exempt` MUST 同时携带 `reason` / `expiry_kind`（`on-date` / `on-condition` / `on-review` 三值封闭）/ `expiry_value` / `expiry_recheck`（绝对日期）；到期或谓词不可求值时该条目重新成为未处置条目（FR-006 / FR-007 / D-4）。
- **antithesis**: 允许「永久豁免」——一条经用户确认的豁免在写下之后不再被重新检出，除用户主动撤销；当豁免的对象是一类**不会随时间变化的事实**（例如一段被冻结的历史记录的措辞）时它更优——不制造每年都要人工再确认一次的噪声。
- **binding_constraints**:
  - pole_a: 本特性要消灭的正是「这个问题留到将来」（理念原话）；一个无到期形态的豁免就是那个行为的合法化身，MUST NOT 存在（FR-006）。
  - pole_b: 豁免 MUST NOT 变成需要持续人工值班的负担：`on-condition` 的谓词由引擎求值，`on-review` 只要求一个绝对日期，且不可求值时的结果是 `unevaluated`（可见），不是「仍然有效」。
- **discriminating_evidence**: 构造一条 `expiry_recheck` 已过去的 `exempt`，重跑回顾；结果二值——它是否重新出现在未处置集合里（是／否）。为「否」则该机制没有到期语义，重开。
- **expected_sacrifice**: SC-017 Source ↓ 每一次到期都要有人重新裁定，长期看会周期性产生一批「必须再看一眼」的条目；这是主动选择的代价，不是缺陷。
- **revision_trigger**: 出现 ≥2 次「到期后重新处置的条目里有 ≥80% 被再次豁免、且理由与上次相同」→ 重开，评估把该类事实升为「结构性不适用」（改判据），而不是放宽豁免的到期形态。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/092-non-disposable/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output — 13 findings, each with its measurement
├── data-model.md        # Phase 1 output — entities, the entry state machine, the expiry model
├── quickstart.md        # Phase 1 output — 9 scenarios, one per detection class + the seam
├── contracts/           # Phase 1 output — 7 contract files
├── feature-ref.md       # Phase 1 output — binding, delivery surface, corpus map, FR/SC index
├── notes/input-review-080-090.md   # the validation corpus (dated input record, zero rules)
├── tasks.md             # Phase 2 output (/speckit.tasks command — NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

### Source Code (repository root)

Only the directories this feature creates or changes, one line each. **`shared/` and `scripts/` are the framework
sources**; their `.specify/` counterparts are produced by `scripts/python/sync-mirrors.py` and MUST NOT be
hand-edited (constitution XI, 「Two hats」).

```text
scripts/python/                     # + non-disposable-check.py — the new read-only deterministic engine
shared/definitions/                 # + non-disposable-definitions.md — the owner page (the one rule owner)
shared/declarations/facts/          # + non-disposable-review-surface.yaml — the ten roots as a closed-set fact
shared/definitions/framework-map.md # EDIT — one registration row for the new owner page (Directory Governance)
templates/commands/history.md       # EDIT — the four-stage delegation bullet list + the seam pointer
skills/internal/manage-history/SKILL.md  # EDIT — the review / design / confirm / execute seam (steps 0/A/B)
templates/instructions-template.md  # EDIT — ONE pointer line into the existing section (never a new `##`)
.specify/instructions.md            # regenerated from the template by scripts/bash/generate-instructions.sh
                                    #   (AGENTS.md is a symlink to it and flows; never hand-edited)
.specify/memory/glossary.md         # EDIT — four terms pointing at the owner page
.specify/memory/features.md         # EDIT — the 092 row (Draft -> Planned at this stage)
.specify/memory/features/092.md     # NEW — the feature detail (Overview / Key Changes / Notes / Related Files)
.specify/memory/register.md         # EDIT — the D-1…D-8 decision registration rows (see § ID Register Duty)
tests/contract/                     # + test_non_disposable_contract.py — the seven-face guard with mutation legs
```

**Structure Decision**: the feature extends the existing **engine-beside-engine** shape (`scripts/python/` holds one
stdlib read-only script per deterministic question — `sanitize-utils.py`, `closure-acceptance-check.py`,
`renumber-utils.py`, `account-clause-coverage.py` are its siblings) and the existing **one-owner-page** shape
(`shared/definitions/*-definitions.md`). No new top-level directory, no new package, no new entry point beyond the
one `/speckit.history` that already exists.

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

Baseline measured **before** any edit (2026-11-09): `python3 scripts/python/sync-mirrors.py --check` on the pairs
this feature touches. The criterion below is **"no NEW drift on the pairs this spec touches"**, never a bare exit
code — unrelated drift may predate this feature and an absolute "all green" would be an unpassable criterion.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `scripts/python/non-disposable-check.py` (NEW) | `.specify/scripts/python/non-disposable-check.py` via `sync-mirrors.py` (pair `("scripts", ".specify/scripts", True, set())` — strict: the projection block is inserted, so the pair is **not** byte-equal by construction) | `sync-mirrors.py --check` reports no new drift; the mirror carries the projection marker exactly once and its `_bridge_*` block sits before `if __name__ == "__main__":` |
| `shared/definitions/non-disposable-definitions.md` (NEW) | `.specify/shared/definitions/non-disposable-definitions.md` (pair `("shared", ".specify/shared", …)`, byte-equal) | `diff -q` on the pair, judged against the pre-edit baseline |
| `shared/definitions/framework-map.md` (EDIT) | `.specify/shared/definitions/framework-map.md` (same pair) | `diff -q` on the pair |
| `shared/declarations/facts/non-disposable-review-surface.yaml` (NEW) | `.specify/shared/declarations/facts/non-disposable-review-surface.yaml` (same pair) | `diff -q` on the pair |
| `skills/internal/manage-history/SKILL.md` (EDIT) | `.specify/skills/internal/manage-history/SKILL.md` via the `("skills/internal", ".specify/skills/internal", …)` pair | `diff -q` on the pair |
| `templates/commands/history.md` (EDIT) | per-tool copies via `commands/`: `.claude/commands/speckit.history.md`, `.github/prompts/speckit.history.prompt.md`, `.qoder/commands/speckit.history.md`, `.opencode/command/speckit.history.md`, `.codex/…`, `.hermes/…` (whatever `regen-command-copies.py` renders for this tree; **`.specify/templates/commands/` is retired** — never a mirror) | `regen-command-copies.py` re-run; every rendered copy contains the edit; `tests/contract/test_docs_command_template.py::test_c10_runtime_copies_exist_for_every_present_tool` green |
| `templates/instructions-template.md` (EDIT) | `.specify/templates/instructions-template.md` (pair `("templates", ".specify/templates", False, {"commands"})`) | `diff -q` on the pair |
| `templates/instructions-template.md` (EDIT) | `.specify/instructions.md` + `AGENTS.md`/`CLAUDE.md`/`QODER.md`/`.github/copilot-instructions.md` — **generated**, never mirrored by `sync-mirrors.py` | `scripts/bash/generate-instructions.sh` re-run; `wc -c .specify/instructions.md` within `INSTRUCTIONS_BUDGET_BYTES`; the five compatibility files are still symlinks (`/speckit.instructions` repair path, never a hand edit) |

**Frozen-file obligation (R7).** `templates/commands/history.md` and `skills/internal/manage-history/SKILL.md` are
both inside `tests/contract/test_expression_compatibility.py`'s 069a hash manifest. The edit is legal only together
with an `ALLOWED_POST_BASELINE_CHANGES` registration whose markers are **added by this change** (a marker that
already existed cannot witness a drift) and whose `reason` names this feature.

## Execution Premises

Owner of this table's shape, its `Status` and `Decision` value domains and its invalid-row rule: `shared/workflow/acceptance-hardening.md` § Execution Premises — this skeleton carries the column set and nothing else, so a value domain written here would be a second definition.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | A CPython ≥3.8 interpreter is available and the new engine needs no third-party import, so it runs on the same interpreter as its siblings. | `/usr/bin/python3 --version` → `Python 3.11.0rc1`; `pyproject.toml:5` → `requires-python = ">=3.8"`; the new engine's import list is stdlib + two sibling modules whose own heads declare "stdlib-only" | verified | — |
| EP-002 | `pytest` is available and the pre-existing contract-suite red set is stable enough to serve as a comparison baseline, so "no NEW failure" is decidable. | `090` recorded `pytest 9.0.3`; the frozen baseline is the failed node-id set, not a count (SC-013's own criterion) | verified | — |
| EP-003 | The declaration layer is readable through `declaration_reader.py` and a new `closed-set` fact needs no new kind and no new required key. | `shared/declarations/contract.yaml` → `fact_kinds` contains `closed-set`, `required_fact_keys` = the five keys the sibling `flow-class-classes.yaml` carries; today's `declaration_reader.py --action list` loads all 23 facts | verified | — |
| EP-004 | The review surface is enumerable and its size is measurable without reading file contents, so the coverage declaration can be checked against an independent enumeration. | `find` over the ten roots on `62f95298` → 4,357 files (per-root readings in § Execution Premises evidence and in `quickstart.md`) | verified | — |
| EP-005 | The semantic face can be carried by the existing 085 spec-local team at the spine's declared concurrency (24), so no second scheduler is needed. | `.specify/state/092-non-disposable.md` → `agent_concurrency_requested: 24` / `agent_concurrency_effective: 24`; `085` contract C-002…C-005 fix the effective-value formula and the named-downgrade rule | verified | — |
| EP-006 | `closure-acceptance-check.py` can be invoked as a subprocess and its `--json` payload is stable enough to consume, so the status check reuses the verdict instead of re-deriving it. | `closure-acceptance-check.py --json` emits `verdict` + `reasons`; `tests/contract/test_closure_acceptance_check.py` pins the payload shape | verified | — |
| EP-007 | The A–H corpus is consumable as a fixture set: at least two of its entries reproduce on this tree today, so a quickstart scenario can run against reality rather than against a synthetic tree. | `harness-triple-check.py --action verify` → 3 `unclassified-candidate`, exit 1 (`084/verification.md:70` claims 0); `generate-instructions.sh:100` → `INSTRUCTIONS_BUDGET_BYTES=38400` under a reason block deriving `37888` | verified | — |
| EP-008 | `git` is available in the working tree, because the zero-write proof and the `archive` disposition are both defined in git terms. | `git rev-parse --short HEAD` → `62f95298`; `git status --porcelain` → 7 pre-existing entries (2 modified-or-untracked in this line's own writes) | verified | — |

## Inherited Blockers

Dependency set: none — this feature consumes no dependency artifact's measured blocker rows.

**Dependency artifacts (declared, never implied)** — stated as prose, because the gate that reads this section
parses the *first table* under the heading as the blocker table; a second table above it would be read as one:
- `085-sdd-temporary-goal-team` — **included**: its team/并发 contract is the mechanism this feature reuses (FR-046 / FR-050 / FR-051).
- `089-script-interface-contract` — **included as a neighbour**, not as a dependency: its delivered shape (owner page + contract + guard) is the template for this feature's seven-face landing.
- `084-harness-triple-structure` — **included**: the declaration layer this feature writes into is its surface, and `harness-triple-check.py --action verify` is the reading that proves corpus entry A2.
- `047` / `045-sanitize-command` — **included as a vocabulary owner only** (FR-060): its four closed sets are read by pointer and none of its findings is inherited.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| IV — Test-First partial: the guards for the engine cannot be written before the engine exists | The subject of the contract is a new deterministic engine; a guard that asserts "the engine reports `status-claims-implemented-but-blocked` on a `Implemented`-vs-`block` copy tree" has nothing to run against until the engine's first green run exists | Writing the guards against a stub would satisfy the letter (red first) while proving nothing about the real judgement — the stub would supply the verdict the guard checks. The compromise kept: each guard must carry a **mutation leg** (break the subject, assert red), so a green is a claim that has been shown to be falsifiable |

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Research | [`research.md`](research.md) | 13 findings (R1–R13), each with the command/measurement behind it |
| Data model | [`data-model.md`](data-model.md) | 9 entities (E-1…E-9) + 2 state machines + the expiry model + § Human-Facing Output Shape |
| Contracts | `contracts/` | 7 files, 54 clauses: `detection-categories` C-101…C-108, `status-and-verification` C-201…C-207, `disposition` C-301…C-308, `four-stage-command` C-401…C-409, `renumber-and-supersede` C-501…C-507, `detection-engine-cli` C-601…C-608, `report-schema` C-701…C-707 |
| Quickstart | [`quickstart.md`](quickstart.md) | 10 scenarios — § 1/§ 2 reproduce on the tree as it stands (corpus A2 / F2), § 3…§ 7 one per remaining detection class, § 8 the four-stage seam, § 9 the concurrency slice, § 10 the post-repair zero reading |
| Feature reference | [`feature-ref.md`](feature-ref.md) | binding table + 15-row delivery surface + § 4 corpus map (pointer to the 35 rows) + § 3 FR→SC→contract index (all 65 FR and all 20 SC cited) + § 5 shift list + § 6 open items |

**Drift from the Phase 0 expectation**: two adjustments were forced by measurement, both recorded in `research.md`
rather than smoothed over — (i) the anti-goal lens produced **seven** decision tensions instead of the four the
requirements named, because OI-2, OI-4 and the certainty/semantics boundary each carry two independently-adoptable
poles rather than one (T-002…T-005), and the mechanism/landing/corpus/concurrency choices are load-bearing on their
own terms (T-001, T-006, T-007); (ii) the contracts are **seven** files, not the five names § 3 of the assignment
listed, because the report schema and the engine CLI surface are the two faces a guard can address mechanically and
folding them into another file would have put two owners in one document.

## Implement Package Proposal *(input for `/speckit.tasks`; not a gate input — see R12)*

`decomposition-check.py --mode plan` measures **the requirements artifact only** (65 FR ≤ 120 → `proceed`); it
knows nothing about packages. This partition is therefore a **design proposal** for the tasks stage, sized under the
existing `decompose-implement-v1` rule (task groups ≤ 8 tasks per group, `070` data-model E13) and the spine's
`decomposition_slot_cap: 2`.

| # | Package | Owns (territory) | Depends on | Read-only? |
|---|---------|------------------|-----------|-----------|
| P1 | **Owner + declaration + registration** — the rule owner page, the `closed-set` fact, the framework-map row, the glossary four terms, the registry row + detail, the register decision rows | `shared/definitions/non-disposable-definitions.md`, `shared/declarations/facts/non-disposable-review-surface.yaml`, `shared/definitions/framework-map.md`, `.specify/memory/{glossary,features,register}.md`, `.specify/memory/features/092.md` | — | no |
| P2 | **The deterministic engine** — `scripts/python/non-disposable-check.py` (8 classes, coverage declaration, `--scope`, `--json`, exit 0/1/2, zero write) | `scripts/python/non-disposable-check.py` | P1 (reads the fact + owner page) | no |
| P3 | **The history seam** — `manage-history` steps 0/A/B, `templates/commands/history.md` delegation list, the per-tool copies, the `.tmp` confirm artifact, the four-segment evidence | `skills/internal/manage-history/SKILL.md`, `templates/commands/history.md`, the rendered command copies | P1, P2 | no |
| P4 | **The three pointer faces** — one line each into `templates/instructions-template.md` (inside an existing section), the regenerated `.specify/instructions.md` + `AGENTS.md`, and the `manage-history` review pointer | `templates/instructions-template.md`, `.specify/instructions.md`, `AGENTS.md` | P3 (the pointer must point at something that exists) | no |
| P5 | **The contract guard** — `tests/contract/test_non_disposable_contract.py`: seven-face existence, the four frozen sanitize sets unchanged, both constitution count pins unmoved, the mutation legs, the expression-baseline registration | `tests/contract/test_non_disposable_contract.py`, `tests/contract/test_expression_compatibility.py` (allowance entry only) | P1…P4 | no |
| P6 | **The repair lane, 档 I** — the A–H entries this feature repairs, each with its four-segment evidence; ends with a re-run driving 档 I to zero | the spec bodies the 档 I rows name (see § A–H Corpus Mapping), `.specify/specs/092-non-disposable/test-evidence/repair-*.md` | P2, P3, P5 | no |
| P7 | **The shift list, 档 II** — the corpus→owner handoff table and its one-line markers | `feature-ref.md` § Shift List, one marker line per receiving body | P2 | no |
| P8 | **Stage verification** — the closure run, the evidence index, `verification.md` | `.specify/specs/092-non-disposable/verification.md`, `test-evidence/` | P1…P7 | no |

**Serialization.** P1 precedes P2 (the engine reads the declaration and the owner page); P2 precedes P3/P7; P3
precedes P4; P5 follows P4 (it guards faces that must exist); P6 follows P5 (the repair lane's evidence must be
read against a working engine and a red-able guard); P8 last. P6 and P7 may run concurrently with each other, which
is the only real parallelism inside the implement stage — everything else is a chain. **No two write packages share
a path**, so the write-alone rule of the existing scheduler is satisfied without any new mechanism.

**Why the ceiling matters here.** 65 FR sits at 54% of the FR ceiling: there is room for the tasks stage to add
rows, and no room to split this feature into two slices without inventing a boundary the requirements do not have.

## Risk Register *(implementation-time, carried into `/speckit.tasks`)*

| # | Risk | Discriminating reading | Mitigation written into the artifacts |
|---|------|------------------------|---------------------------------------|
| RK-1 | The expression-compatibility freeze reds on the two edited frozen sources | `pytest -m contract tests/contract/test_expression_compatibility.py` | The allowance entry with `added_markers` (R7, § Mirror Obligations) |
| RK-2 | The engine's `status-unreadable` class re-derives the verdict instead of consuming it | one subprocess call to `closure-acceptance-check.py` in the engine, asserted by a guard that replaces the checker with a failing stub | FR-028, `contracts/status-and-verification.contract.md` C-2xx |
| RK-3 | The `archive` disposition loses the file (a delete in disguise) | after a repair run, `git status --porcelain` shows a rename pair, never a deletion; the guard asserts the mapping row exists | FR-034/FR-058, `contracts/disposition.contract.md` C-3xx |
| RK-4 | The review surface silently grows to "everything under `.specify/`" | the declaration file is the only source; a sibling directory produces a hint, never a candidate | FR-036…FR-041, `contracts/detection-engine-cli.contract.md` |
| RK-5 | The repair lane rewrites a 档 II body while "fixing" it | the shift list asserts the receiving body is untouched by this feature's diff; 档 II files never appear in the repair lane's changed-path list | FR-056, § A–H Corpus Mapping tier column |
| RK-6 | The five-part seam is documented but the command template drifts back | the guard asserts both the skill and the template name the four stages, with a mutation leg that deletes one stage name and expects red | FR-029, `contracts/four-stage-command.contract.md` |

## Shift List *(档 II handoff — the deliverable, not a deferral)*

Every row below MUST reach a receiving feature line. This feature lands **one marker line** in each receiving body
(a one-line `<!-- 092 handoff: <corpus id> → <receiving feature> -->` style marker, placed where the defect is) and
**nothing else**; the repair itself stays with that line (FR-056).

| Receiving line | Corpus ids | What it must change |
|----------------|-----------|---------------------|
| 081-acceptance-hardening | D1, D2 | one owner for the state machine and the reason set; the other two sites become pointers |
| 084-harness-triple-structure | D3, E5 | the dual "goes to yaml" criterion; the exclusion-row count |
| 088-speckit-visualization | D4 | one reporter cadence |
| 090-re-anchoring | D5, F2 | the eight-member rule anchor's four spellings; the budget block's arithmetic |
| 082 / 083 (self-explanatory + mechanism-policy) | D6 | declared precedence between the two adjacent criteria |
| 083-mechanism-policy-separation | E1, E2, E3, F5 | scope contradiction, baseline triple, phantom principle, skill counts |
| 089-script-interface-contract | E4 | the `applicable + exempt == candidates` identity |
| 087-arch-diagram-docs | E6 | Overview vs its own clarify ruling |
| 080 / 077 / 079 / 069 / 069b / 082 (dated bodies) | F1, F3 | quoted ceiling/roster values where they are neither history nor the owner |
| `.specify/memory/features.md` + `features/080.md` | F4 | feature-total arithmetic and 080's spec-dir registration |
| 086-efficient-test-execution | H1 | the `.specify/skills/external/…` path literal |
| 082 / 085 | H2 | the two nonexistent evidence paths |


## A–H Corpus Mapping (per-entry)

The requirements table maps the eight **groups** to their FR/SC. `requirements.md` § A–H Corpus Mapping charges this
stage with the **per-entry** expansion ("逐条的映射 MUST 在 plan / tasks 阶段展开为一行"). The table below is that
expansion: **35 entries** (A 6, B 5, C 4, D 6, E 6, F 5, G 3, H 3), counted from the corpus file's own table rows
and list items (`research.md` R9). Each row carries the **tier** from FR-056's closed two-value criterion and the
**detection class** that must reproduce it.

`档 I` = this feature delivers the mechanism **and** the first repair, and the entry must reach name-level zero
here. `档 II` = this feature delivers the detection **and** a shift row; the repair belongs to the receiving
feature's own body and MUST NOT be written by this feature.

Columns: `ID` (corpus entry) · `Sev` · `Class` (owner page's closed detection class) · `Tier` · `Carrier` (what
changes / who receives it) · `SC` (the success criterion whose reading covers it).

| ID | Sev | Class | Tier | Carrier | SC |
|----|-----|-------|------|---------|-----|
| A1 | CRITICAL | `status-unreadable` | I | 089 `verification.md` gains the machine-readable per-SC block + smoke record; the registry row is reconciled against `closure-acceptance-check.py`'s verdict | SC-008 |
| A2 | CRITICAL | `false-closed-set` | I | 084's `unclassified 0` claim is completed (the reading is taken from the engine, not the claim); `harness-triple-check.py --action verify` is the reproduction used by `quickstart.md` § 1 | SC-008 |
| A3 | HIGH | `status-unreadable` | I | 090's registry row moves `Planned` → its closure-consistent value (closure is `accept`, 4/4 SC); the contradiction is what the check reports | SC-008 |
| A4 | HIGH | `status-unreadable` | I | 089 `tasks.md` structural errors (`[US*]` labels in a non-story phase) are completed as records so the status block and the task structure agree | SC-008 |
| A5 | HIGH | `status-unreadable` | I | 085 `plan.md` decision-tension records are completed to the owner's six-field form (`dtr-rejected-form` ×3) | SC-008 |
| A6 | HIGH | `status-unreadable` | I | 080 gains the post-081 common schema fields (`**Path**:` markers, `smoke_command`) — a record completion, not a conclusion change | SC-008 |
| B1 | HIGH | `superseded-live` | I | 086 `contracts/runner-contract-086.contract.md` § C-016 gains the superseded marker + pointer to `089/contracts/mirror-projection.contract.md`; the guard `tests/contract/test_run_tests_runner_contract.py` `…_byte_identical` is retired or replaced in the same change | SC-005 |
| B2 | HIGH | `superseded-live` | I | 085 `contracts/temporary-goal-team.md` / `checkpoint-and-agents.md` follow the owner (`create-mode.md`, `checkpoint-protocol.md`): `team/<slug>/team.md` and the five-part checkpoint | SC-005 |
| B3 | MEDIUM | `superseded-live` | I | 067 `contracts/runner-contract.md` "Serial is the default" is superseded by 086's parallel default: marker + pointer, old text retained | SC-005 |
| B4 | MEDIUM | `orphan-path` | I | 088 `efficiency-model.md` § evidence-path names `final-failed.txt` while the closure reading is `final-failed-r6.txt`; by clarify OI-3 the file exists → `superseded-live`/`correct`, the original text retained in the disposition record | SC-005 |
| B5 | MEDIUM | `orphan-path` | I | the two-slot evidence path has three spellings (owner, 085, 086): one owner spelling + pointers; the other two become pointers in the disposition record | SC-005 |
| C1 | HIGH | `renumber-live-binding` | I | 089 `requirements.md:12` `Feature ID: 086`, `tasks.md:3,5` headers, `feature-ref.md:7,12,78` → 089 | SC-007 |
| C2 | HIGH | `renumber-live-binding` | I | 089 `tasks.md` T081's live instruction to edit "features.md (086 row)" / `features/086.md` → the 089 row | SC-007 |
| C3 | HIGH | `renumber-live-binding` | I | 089 `team/086-script-interface-contract/` directory name and `name: SDD Temporary Team 086` → the 089 slug (a directory rename, `git mv` semantics) | SC-007 |
| C4 | MEDIUM | `renumber-live-binding` | I | 088's eight contract headers `**Feature**: 087`, the main team name and the dogfood slug → 088 | SC-007 |
| D1 | HIGH | `multi-owner` | II | 081 `requirements.md:136,156` + `contracts/state-vocabulary.contract.md:17`; the owner is `shared/workflow/acceptance-hardening.md` — the repair is 081's own body | SC-006 |
| D2 | HIGH | `multi-owner` | II | 081's closed reason set: one owner (the owner doc's seven-member set), the requirements table and `tasks-081b.md:232` become pointers — 081's body | SC-006 |
| D3 | HIGH | `multi-owner` | II | `harness-triple-definitions.md:41-59` vs `084/requirements.md:143`: two mutually exclusive forms of the "goes to yaml" criterion — the owner doc's body | SC-006 |
| D4 | HIGH | `multi-owner` | II | 088's reporter cadence 15 min vs 30 s across `create-mode.md`, `reporting-obligations.md`, `progress-reporting.md` — 088's body | SC-006 |
| D5 | HIGH | `multi-owner` | II | 090's "rule anchor eight members" four spellings (`re-anchoring-definitions.md` §1.1/§1.2/§3, `RULE_SET`) — 090's body | SC-006 |
| D6 | MEDIUM | `multi-owner` | II | 082 / 083 adjacent criteria with no declared precedence (`self-explanatory-definitions.md`, `mechanism-policy-definitions.md`) — the two owners' bodies | SC-006 |
| E1 | HIGH | `false-closed-set` | II | 083 `requirements.md:160,186,220` scope self-contradiction (FR-011 vs FR-026) — 083's body | SC-008 |
| E2 | HIGH | `false-closed-set` | II | 083's three "baseline" values and `post_change == baseline` — 083's plan/verification bodies | SC-008 |
| E3 | HIGH | `false-closed-set` | II | 083's "first-class principle" absent from the roster — 083's body | SC-008 |
| E4 | HIGH | `false-closed-set` | II | 089's `applicable + exempt == candidates` identity (`367 + 737 ≠ 751`, tasks `:23,38`) — 089's body | SC-008 |
| E5 | MEDIUM | `false-closed-set` | II | 084 exclusion rows 8 vs 38 (`requirements.md:203` vs `contracts/migration-batches.contract.md:132`) — 084's bodies | SC-008 |
| E6 | MEDIUM | `false-closed-set` | II | 087 Overview contradicts its own clarify ruling (`requirements.md:37` vs `:41,155,301`) — 087's body | SC-008 |
| F1 | HIGH | `stale-constant` | II | the decomposition ceilings: **value owner measured** = `decomposition-check.py` `FR_CEILING`/`TASK_CEILING` (pinned to `admission-check.py` by `test_sdd_loop_driver_gates.py:67-68`), already pointed at from `efficiency-model.md:300`; the remaining hits are dated records and delivered bodies that quoted a then-current value (`080/077/079/069b/069/082`) → shift to those lines, **not** rewritten here | SC-006 |
| F2 | HIGH | `stale-constant` | II | `scripts/bash/generate-instructions.sh:100` declares `38400` under a reason block deriving `37888`, with two self-contradicting subtractions — a delivered script body, shift to it (the 090 review already carries the same defect) | SC-006 |
| F3 | MEDIUM | `stale-constant` | II | constitution roster counts copied into plans (17/18 vs live 22 / template 21) — each copying body | SC-006 |
| F4 | MEDIUM | `multi-owner` | II | feature-total arithmetic stale (76→77 vs 85) and 080's spec dir registered under ID 062 — the registry's own body | SC-006 |
| F5 | MEDIUM | `stale-constant` | II | 083's skill counts disagree (15+38 vs 54 vs 16+38) — 083's body | SC-006 |
| G1 | HIGH | `superseded-live` (guard side) | I | 090's ordering guard lost its only positional comparison: `tests/contract/test_sdd_loop_driver_reanchor.py` gains the additive goal-first mutation leg (asserts red) — a first-round repair | SC-005 |
| G2 | MEDIUM | `deferral-marker` (guard side) | I | the `first_no = "1"` / `assert first_no == "1"` tautology is replaced by an assertion that reads the actual first item | SC-005 |
| G3 | MEDIUM | `superseded-live` (guard side) | I | `RULE_SET` omits ⑧ and splits ①, so deleting "report discipline" cannot red — the set is completed against the owner's rule anchor | SC-005 |
| H1 | HIGH | `orphan-path` | II | 086 writes the mirror as `.specify/skills/external/...` (a directory that never existed) — 086's body | SC-005, SC-007 |
| H2 | MEDIUM | `orphan-path` | II | 082's nonexistent session file; 085 GATE-1's nonexistent `test-evidence/final-failed.txt` — those bodies | SC-005, SC-007 |
| H3 | LOW | — (recorded exclusion) | excluded | `.specify/.tmp/086-*` historical measurement paths are **legitimate history** (FR-020's third legitimate duplicate); registered as an exclusion, never as a finding | SC-005 |

**Tier tally**: 档 I = **19** entries (A1–A6, B1–B5, C1–C4, G1–G3), 档 II = **15** entries (D1–D6, E1–E6, F1–F5, H1–H2), excluded = **1** (H3). Total 35.

**Two-way check (FR-056's reporting duty).**

- Every corpus group has at least one carrier — no empty group.
- Every detection class has at least one corpus entry **except** `deferral-marker`: the corpus review never
  specifically looked for retention wording, so its only instances here are the two guard-side G rows (which are
  deferral-shaped rather than deferral-worded). This is the **expected** gap `requirements.md` § A–H Corpus Mapping
  already names; `deferral-marker` is carried by FR-002…FR-005 and proven by `quickstart.md` § 2 instead of by a
  corpus row.
- `renumber-live-binding` has corpus entries but **no** entry for the "a history record was rewritten" leg
  (FR-023/SC-007 limb 3); that leg is proven by `quickstart.md` § 5's mutation, not by a corpus row — recorded here
  so a later reader does not read the corpus as complete coverage of FR-023.

## ID Register Duty *(disclosed gap, owned by implement)*

The clarify session coined eight durable decisions `D-1`…`D-8`, and `.specify/memory/register.md` — the **sole
sanctioned writer** of durable identifiers — carries no row for them. FR-063 落点 7 requires a register entry for
this feature; the decision rows are the same obligation one level down. Measured (read-only) at this stage:

```text
python3 - <<'EOF'   # register row scan, same parsing rule as renumber-utils.register_rows
import re, pathlib
rows = [l for l in pathlib.Path(".specify/memory/register.md").read_text(encoding="utf-8").splitlines() if l.startswith("|")]
print([c for l in rows for c in re.findall(r"\bD-?\d+\b", l)][:12])
EOF
```

The scan returns only `D1–D9` (a goal's interview decisions) and `D-A`/`D-B`/`D-01`; **`D-1`…`D-8` of this feature
are unregistered**. This is a correction the plan stage can name but MUST NOT perform: `requirements.md` and the
checkpoint are tracked artifacts, and register.md is a canonical single-owner registry — writing eight rows into it
is a governance write that belongs to the implement stage's delivery of FR-063 落点 7, together with the feature
row. Recorded here, carried by package **P1**, and disclosed at wrap-up (fast fail: a correction would have been
local and reversible, but the registry is an *owned canonical* file whose writer discipline reserves the edit to the
landing change — this is a **decision-free** deferral, not a silent one).

## Open Decision Surface *(OI-4 / OI-5 — reported, not absorbed)*

- **OI-4** — whether the constitution should carry a Non-Disposable principle. Clarify judged "no" from the verbatim
  goal (D-2); this plan restates the gap as `T-002` and lands **nothing** that would pre-empt the answer (FR-065
  forbids pre-writing a principle number or a count pin). Reading for the driver/user: the feature ships with owner
  page + confirmation gate as its strongest normative surface.
- **OI-5** — whether the constitution's XI 「Mechanism Fix」 sub-clause should become a pointer to the owner page.
  Both surfaces describe "not one-shot", but their criteria differ (fix the mechanism vs. dispose of the residue);
  merging them is forbidden in-place because it would rewrite delivered constitution text. Reported here; not
  repaired.

## Landing Checklist *(seven faces, one owner, zero new principles)*

| # | Face | Artifact | Guard reading |
|---|------|----------|---------------|
| 1 | Owner page (NEW) | `shared/definitions/non-disposable-definitions.md` | exists, non-empty, declares what it owns, carries the two mapping tables and the adjudication rule |
| 2 | Declaration fact (NEW) | `shared/declarations/facts/non-disposable-review-surface.yaml` | loads through `declaration_reader.py`, `kind: closed-set`, the five required keys present, ten roots in the declared order |
| 3 | Glossary (4 terms) | `.specify/memory/glossary.md` | `Non-Disposable` / `Disposition（处置）` / `Review Surface（回顾面）` / `Exemption（豁免）` each point at the owner page and restate none of its criteria |
| 4 | Registry row + detail | `.specify/memory/features.md`, `.specify/memory/features/092.md` | row present, status `Planned`, detail carries the XI 边界 line |
| 5 | Existing guard | `tests/contract/test_non_disposable_contract.py` | the four `sanitize-utils.py` sets byte-unchanged; `test_constitution_double_landing.py` and `test_fast_fail_discipline.py` count pins unmoved; a mutation leg per closed set |
| 6 | Three pointer faces | `templates/instructions-template.md` + `.specify/instructions.md` / `AGENTS.md`; `skills/internal/manage-history/SKILL.md` | one line each, appended **inside an existing section** — `test_fast_fail_discipline.py::test_a7_section_counts_20_to_21_and_21_to_22` pins the top-level `##` counts (its `TPL_EXPECTED` / `LIVE_EXPECTED` locals own the numbers) and MUST stay unchanged; `wc -c .specify/instructions.md` stays within `INSTRUCTIONS_BUDGET_BYTES` (measured headroom before the edit: 38,400 − 35,821 = 2,579 B) |
| 7 | Decision record | `.specify/memory/register.md` + `shared/definitions/framework-map.md` row | one register row per the ID Register Duty above; the directory registration row in the existing table |
