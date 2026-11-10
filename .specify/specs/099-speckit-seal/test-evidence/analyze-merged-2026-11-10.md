# Analyze 报告（Round 1 · merged）— 099-speckit-seal

> 全 spec 首轮分析（requirements / clarify / plan / tasks / checklist / contracts / 设计产物 + 特性注册表 + 宪法）。严格只读：未修改任何制品，不自动修复；修复只以建议形式给出。本文件是阶段交付物；确定性读数见同目录 `analyze-gates-2026-11-10.txt`（校验器、074 基线、注册表读数）与 `analyze-coverage-2026-11-10.json`（覆盖会计引擎完整负载）。

## 顶部计数与指针

| 项 | 值 |
|----|----|
| 轮次 / 判定对象 | Round 1 / `.specify/specs/099-speckit-seal/` 全目录（28 FR / 9 SC / 3 RS / 3 STR；plan 6 决策张力 / 12 执行前提 / 9 工作包；4 契约 45 条款；data-model 14 实体 / 16 校验规则；research R-01…R-21；quickstart S-1…S-9；checklist 40 条） |
| 运行 | `r20261110T121314Z-b099` · stage=analyze · 单 Worker 串行（requested=24 / effective=1 / reason=`budget-reserve`） |
| 四元组 | flow_class=execution；source=declaration；marker=；error=- |
| **结论** | **CONDITIONAL — 0 CRITICAL / 7 HIGH / 5 MEDIUM / 0 LOW（12 findings）**；7 条 HIGH 全部为 `proposed`（独立复核波未派发，见「复核状态」）。实现前须修复 HIGH 对应需求并复跑，或由用户显式裁定处置 |
| Findings 分布 | A 0 · B 1 · C 4 · D 0 · E 2 · F 4 · G 1 · I 0；H（清单问责）残差 0（unchecked 40 = raised 10 + covered-by 30） |
| 覆盖 | FR 28/28 被契约条款引用（100%）；条款差量**不可判**（`baseline-missing`，§E-02）；spec 内结构校验 0 error；074 验收基线（57 / 32 / 26）本轮复现 |
| 特性联动 | Feature 099 已绑定：注册行 `.specify/features.md:102` + 详情 `.specify/features/099-speckit-seal.md`；状态对一致（`Planned` == `Planned`）；阶段注记陈旧（§G-01） |
| 宪法 | 22 原则 22/22 Pass；0 冲突；1 项计划内叙述收敛（T014，见「Constitution Alignment Issues」） |
| 权威指针 | 宪法 `.specify/constitution.md`；分析契约 `.specify/skills/internal/analyze-artifacts/SKILL.md` + `references/`；状态脊 `/storage/project/cloud-native-ai/spec-kit/.specify/state/099-speckit-seal.md`；证据目录 `.specify/specs/099-speckit-seal/test-evidence/` |
| 只读声明 | 制品零修改；唯一落盘是本报告与两份阶段证据；后续修复命令由用户/下游阶段执行 |

### 复核状态（C/H review 标记）

- `validated` = 已由独立 fresh-context 只读复核者确认；`proposed` = 检测结论，等待独立复核波（owner `.specify/skills/internal/analyze-artifacts/references/validation-and-report.md` § 5.5）。
- 本轮按派发的并发读数 `effective=1（budget-reserve）` 单 Worker 串行执行，独立复核波**未派发**，故 7 条 HIGH 全部标 `(review: proposed)`；无 CRITICAL。
- 复核度量：sent 0 / confirm 0 / downgrade 0 / reject 0；降级率 **N/A**（未运行）。
- 同一作者门：**不触发**——本 spec 链由本 SDD 循环的前序阶段运行撰写（提交历史可查），非本会话作者；检测为直读检测（同 checklist 阶段同一判定，先例 `checklists/2026-11-10-requirements-quality.md:12`）。
- 严重度推导：`propagation_surface = none` 的行封顶 MEDIUM；有具名下游的行按缺陷类别取 HIGH/MEDIUM。行内第一个判定列即 `propagation_surface`（owner `.specify/shared/workflow/objective-analysis-gate.md` rule 3）。

### 检测通过范围（本轮实际运行）

A 重复 · B 歧义 · C 欠规定 · D 宪法（plan 22 行 Constitution Check 对 live 22 原则逐名复核）· E 覆盖（accountant + FR→row / SC→row trace + 未映射任务）· F 不一致（含封闭集声明检查，owner `.specify/shared/guidelines/closed-set-claims.md`）· G 特性相关性与阶段记录 · H 清单问责 · I 决策张力（`validate-decision-tensions.py`：6 records，六标签全 pass，high=0）。

---

## A. Duplication（重复）— 0 行

采样与判据（零发现的取证）：FR-012 的 15 项输出件封闭宇宙与 `contracts/merge-back.contract.md` C-013 逐项比对**完全一致**（15/15）；FR/SC/STR 编号连续性由 `validate-requirements.py`（0 error / 0 warning）与 `validate-tasks.py`（pass）钉住；`feature-ref.md` 的 FR→条款映射由 `clause_extract.py` 从契约引用组再生（28/28），非手抄。FR-012 ↔ C-013 的枚举复述通过 one-source-of-truth 的 stale-copy 判定（两侧逐字一致，契约层是符合性 owner），**不构成 finding**。

## B. Ambiguity（歧义）— 1 行

| ID | propagation_surface | Category | Severity | Location(s) | Summary | Recommendation |
|----|---------------------|----------|----------|-------------|---------|----------------|
| B-01 | SC-006 验证面（`tests/integration/test_seal_074_round.py` T042；回合记录 T043/T044） | B Ambiguity | HIGH（review: proposed） | `requirements.md:191`（SC-006）；`requirements.md:69`（US3）；`requirements.md:162`（FR-027） | 「Sealed **或**与 FR-027 五项实测输入**一一对应**的具名阻断清单」把合法阻断面收窄为恰好五项。本轮实测存在五项之外的确定性阻断来源（目录同名产物，§C-03/§F-01；未枚举的 STR 同号不同义，§F-04），它们会以 `conflict-open` 进入拒绝清单，现文会被读作不合规 | 终态表述改为「至少逐条覆盖五项；其他具名阻断只要逐条点名即合规」，并补一条覆盖「额外阻断」的验收断言（CHK036 需求修改，非实现任务） |

## C. Underspecification（欠规定）— 4 行

| ID | propagation_surface | Category | Severity | Location(s) | Summary | Recommendation |
|----|---------------------|----------|----------|-------------|---------|----------------|
| C-01 | `data-model.md` §2 E1/E2（审计更正记录形态）及未来审计更正消费者 | C Underspecification | MEDIUM | `requirements.md:125`（FR-002）；`contracts/status-sealed.contract.md:27`（C-026）；`data-model.md:42`（E1） | 审计更正 `Sealed → Ready for Review` 要求「携带使原封装结论不成立的证据并落在两处载体」，但证据的最小形态（字段/出处/判定人）无任何可判定义；E1–E14 无对应实体或字段，`archive-gate`/漂移守卫无从校验一次回退是否合法 | 在 requirements/data-model 定义审计更正证据的最小载体（如 review.md 追加段 + 注册表行与详情同批引用），并指明校验器（CHK002） |
| C-02 | `scripts/python/seal-utils.py`（T028 前置条件）；`tests/contract/test_seal_seal.py`（T026） | C Underspecification | MEDIUM | `requirements.md:132`（FR-006）；`data-model.md:70`（E2 `review.paths[]`） | 「当前 `review.md`（若存在多个，取当前记录集合，归档记录不计）」缺「当前集合」的派生规则（命名约定或记录指针）；仓内实测并存 `review-081a.md`、`review-r1.md`、`review-second-slice.md` 等异构记录，引擎无法机械区分当前与归档 | 裁定并记录 review 记录「当前集合」派生规则（如：spec 根 `review.md` 为当前，`review-*.md` 不计），写入契约与夹具（CHK005） |
| C-03 | `merge-plan`/`merge-apply`（T020/T023）+ 夹具（T018） | C Underspecification | HIGH（review: proposed） | `requirements.md:141`（FR-012）；`contracts/merge-back.contract.md:23`（C-013）、`:99`（C-021） | 目录型候选（`contracts/`、`checklists/`、`test-evidence/`、`notes/`）没有文件级合并单位与同名文件规则。074 实测同名：`checklists/requirements.md`×3 侧、`checklists/readiness-2026-10-29.md`×2、`test-evidence/{plan-stage-checks.md,tasks-stage-checks.md,targeted-set-v1-baseline.txt}`×3、`contracts/nested-invocation.md`（父+074a）、`contracts/report-and-attribution.md`（父+074b）；这些输入上 FR-013 确定性 / FR-017 冲突显式性均无可适用判据 | 在 C-013 增补目录型候选的文件级单位与同名三态（两侧同名 → 单元级 `merge` 或冲突；仅一侧 → `create`/`keep`），或把目录候选收窄为按文件枚举的派生列表（CHK016） |
| C-04 | FR-016 检出（T020/T023）+ 074 回合 T039/T044 | C Underspecification | HIGH（review: proposed） | `requirements.md:145`（FR-016）；`contracts/merge-back.contract.md:63`（C-017）；`skills/internal/create-team/SKILL.md:99,101` | `[[STR-NNN]]` 是**文档局部**记号（`shared/definitions/sdd-routing-definitions.md:16` 明写登记处为「本特性切片的 requirements.md § Shared Strings」），而 create-team/SKILL.md 使用 `[[STR-004..006]]` 时未声明登记处。需求未给 token→注册表的绑定规则，「对分片本地 ID 的引用」无法机械判定 | 定义 token 归属注册表的绑定/解析规则（缺省解析域 + 使用处声明要求），写入 C-017 与冲突夹具（CHK030） |

## D. Constitution Alignment（宪法对齐）— 0 行

复核方式：plan § Constitution Check 的 22 行（I–XXII）对 `.specify/constitution.md` 的 22 个原则标题逐名核对（I–XXII 全部存在），并抽查 VII（工作流门）、XIV（单一真源）、XXI（脚本接口契约）、XXII（Re-Anchoring）对应的设计落点（C-027 / C-025 / C-003 / plan § Execution Model fast-fail 注入条款）。**无 MUST 冲突、无缺失强制章节或质量门。** 一处**计划内**叙述收敛记录于下（非 finding）：宪法 `## Feature Governance` § Feature Lifecycle Management 的状态枚举仍以 `Completed` 收尾，不含 `Sealed`；FR-003 与 T014 已把「schema owner 为准、叙述面同次收敛（经 `manage-constitution` 程序与版本号递增）」排进同一变更。若实现时 T014 被丢弃，则该处将升级为 D 类 CRITICAL。

## E. Coverage Gaps（覆盖缺口）— 2 行

| ID | propagation_surface | Category | Severity | Location(s) | Summary | Recommendation |
|----|---------------------|----------|----------|-------------|---------|----------------|
| E-01 | C-042 拒绝码封闭集 + `tests/contract/test_seal_seal.py` 夹具（T025/T026）+ 引擎 T028 | E Coverage Gaps | HIGH（review: proposed） | `requirements.md:187`（SC-002）；`requirements.md:107`（Edge Cases）；`data-model.md:168-184`（E12）；`contracts/records-and-boundaries.contract.md:88`（C-042） | SC-002 与 Edge Cases 的「分片未闭合」失败类没有 FR 定义、没有封闭拒绝码——`merge-incomplete` 只覆盖「manifest 缺失 / 覆盖不全 / `not-applicable` 依据缺失」，SC-002 宣称的八类之一没有判定入口（data-model E12 的 10 码表亦无对应码） | 新增 FR（分片任务行闭合判据 + 计数来源）与封闭拒绝码（如 `slice-unclosed`），或把 SC-002 该类改指向既有码并扩展其定义（CHK021） |
| E-02 | `tasks.md` T050 coverage-final 对照 + 覆盖门禁证据 | E Coverage Gaps | MEDIUM | `.specify/specs/099-speckit-seal/coverage-baseline.txt`（缺席）；`tasks.md:102`（T002 把冻结排进 implement 阶段） | 覆盖会计引擎本轮报 `status: baseline-missing`（exit 2）——「absent baseline is NOT an empty exemption list」，覆盖差量无法判定；冻结基线是 `/speckit.tasks` 的 C-6 义务，T002 却把它推迟到 implement 阶段 | 由 tasks 阶段（或最迟 implement 入口前）执行 `account-clause-coverage.py --spec-dir .specify/specs/099-speckit-seal --freeze > coverage-baseline.txt`，然后复跑 analyze 覆盖步骤；MUST NOT 把 baseline 缺席读作通过（分析契约 §3 要求 phase-visible 呈现，本条即该呈现） |

## F. Inconsistency（不一致）— 4 行

| ID | propagation_surface | Category | Severity | Location(s) | Summary | Recommendation |
|----|---------------------|----------|----------|-------------|---------|----------------|
| F-01 | `merge-apply` 写入器（T023）+ 确定性测试（T022） | F Inconsistency | HIGH（review: proposed） | `requirements.md:141`（FR-012「两侧皆有 → `merge`」）；`requirements.md:148`（FR-019 dated-record 红线）；`contracts/merge-back.contract.md:23`（C-013）、`:91`（C-020） | `test-evidence/` 三侧全有，目录级 `merge` 在 dated-record 目录上没有合法语义：复制即第二份测量（违 FR-019），不复制则动作名不实。需求未给第三个动作或限定例外 | 为 dated-record 目录（`test-evidence/`、`checkpoints/`）定义「汇总指针视图」动作语义（如父级 `create` 指针文件、分片原件不改写），并在 C-013/C-020 同批写明（CHK017） |
| F-02 | C-013 必选下限 + T040 + seal 前置条件 T028 | F Inconsistency | HIGH（review: proposed） | `requirements.md:141`（FR-012）；`requirements.md:161`（FR-026）；`requirements.md:132`（FR-006）；`contracts/merge-back.contract.md:23`（C-013）；`tasks.md:221`（T040） | FR-012/C-013 的必选下限只有父 `verification.md`、父 `review.md` 与合并清单，未含父 `code-review.md`；FR-026 却要求回合产出「两片 `review.md` + `code-review.md` 的汇总视图与指针」，且 FR-006 的 `code-review-blocking` 前置依赖「当前 `code-review.md`」——拆分父级上该输入可能不存在 | 把父 `code-review.md` 汇总指针视图加入必选下限（C-013 与 T040 同批），并定义其缺席时的具名拒绝语义（CHK018） |
| F-03 | none（C-039 已收窄；引擎与测试继承契约，不继承矛盾） | F Inconsistency | MEDIUM | `requirements.md:33`（US1「工作树」）；`requirements.md:112`（Edge Cases）；`requirements.md:136`（FR-010）；`contracts/records-and-boundaries.contract.md:64`（C-039） | dirty 判定范围在需求内并存两种表述（「工作树」vs「父 spec 树」）；C-039 已收窄为 `git status --porcelain -- <parent-spec-dir>` 并明写排除目录外路径，但需求文本未收敛 | 收敛 FR-010 / Edge Cases / US1 三处措辞为「父 spec 树」，并按 C-039 指针引用（CHK010） |
| F-04 | SC-006 回合记录（T039/T044）+ `test_seal_074_round.py` | F Inconsistency | HIGH（review: proposed） | `requirements.md:162`（FR-027(b)）；`requirements.md:191`（SC-006）；实测：`.specify/specs/074a-authorized-routing/requirements.md:90`、`.specify/specs/074b-nested-governance/requirements.md:72`、`.specify/specs/074-goal-team-sdd-unification/requirements.md:444-451` | FR-027 的五项实测输入遗漏两项实测「同号不同义」：074a 本地 `STR-010` = `"seats"` vs 父 `STR-010` = `"## Nested SDD Runs"`（074a 已声明映射 `STR-010 → 父 STR-011`）；074b 本地 `STR-007` = `"## Nested SDD Runs"` vs 父 `STR-007` = `"completed"`（已声明映射 `→ 父 STR-010`）。二者会作为 `conflict-open` 出现在回合，但不在五项点名内 | 把 FR-027/SC-006 的枚举改为「至少五项 + 回合实测新增冲突逐条点名」，或在 (b) 中补列 074a `STR-010` 与 074b `STR-007`（CHK031） |

## G. Feature Relevance & Accuracy（特性相关性与阶段记录）— 1 行

| ID | propagation_surface | Category | Severity | Location(s) | Summary | Recommendation |
|----|---------------------|----------|----------|-------------|---------|----------------|
| G-01 | none（注册表行与详情自身的阶段注记） | G Feature Relevance & Accuracy | MEDIUM | `.specify/features.md:102`；`.specify/features/099-speckit-seal.md:20` | 阶段记录陈旧：tasks 与 checklist 阶段产物已落盘（`tasks.md` 51 行、`checklists/2026-11-10-requirements-quality.md`），但注册行注记仍写「planned via /speckit.plan」、详情 `## Latest Review` 仍写「当前阶段为 plan」。`shared/workflow/feature-integration.md` § Core Protocol steps 2–3 的阶段记录义务（plan/tasks/implement 阶段 mandatory）未随阶段推进。状态 `Planned` 本身合法（tasks 维持 `Planned`），但 lawful status 不豁免阶段记录 | implement 前由 `manage-features` reconcile 刷新注册行注记与详情阶段行；本阶段按 feature-integration 属 `/speckit.tasks` 的已发生义务，记入本报告供下游收口 |

## H. Checklist Accountability（清单问责）— 残差 0

判定对象：`checklists/2026-11-10-requirements-quality.md` 的 40 条未勾选项（`checklists/requirements.md` 全部已勾选，不计）。每项给出机读处置标记：

**raised-as-finding（10）**

- CHK002 disposition: raised-as-finding C-01
- CHK005 disposition: raised-as-finding C-02
- CHK010 disposition: raised-as-finding F-03
- CHK016 disposition: raised-as-finding C-03
- CHK017 disposition: raised-as-finding F-01
- CHK018 disposition: raised-as-finding F-02
- CHK021 disposition: raised-as-finding E-01
- CHK030 disposition: raised-as-finding C-04
- CHK031 disposition: raised-as-finding F-04
- CHK036 disposition: raised-as-finding B-01

**covered-by（30）**

- CHK001 disposition: covered-by contracts/status-sealed.contract.md § C-025/C-029（七面漂移守卫）
- CHK003 disposition: covered-by contracts/status-sealed.contract.md § C-027
- CHK004 disposition: covered-by contracts/status-sealed.contract.md § C-031 / C-007
- CHK006 disposition: covered-by contracts/records-and-boundaries.contract.md § C-044
- CHK007 disposition: covered-by templates/feature-details-template.md § Canonical Status State Machine
- CHK008 disposition: covered-by contracts/records-and-boundaries.contract.md § C-042 + test-evidence/checklist-gates-2026-11-10.txt
- CHK009 disposition: covered-by contracts/seal-engine.contract.md § C-005/C-006 + records-and-boundaries § C-038
- CHK011 disposition: covered-by data-model.md § 3 + V5（C-032 封闭字段集）
- CHK012 disposition: covered-by data-model.md § 8 E10（`## Latest Review` 追加语义）
- CHK013 disposition: covered-by contracts/merge-back.contract.md § C-011
- CHK014 disposition: covered-by contracts/merge-back.contract.md § C-012
- CHK015 disposition: covered-by contracts/merge-back.contract.md § C-011 + data-model.md § 5 E4（封闭二形；活数据两片均命中第一形）
- CHK019 disposition: covered-by contracts/merge-back.contract.md § C-014
- CHK020 disposition: covered-by contracts/merge-back.contract.md § C-018 + data-model.md V11
- CHK022 disposition: covered-by contracts/merge-back.contract.md § C-021 + plan.md § Disclosed Rulings 1
- CHK023 disposition: covered-by contracts/merge-back.contract.md § C-019 + data-model.md § 12 E14
- CHK024 disposition: covered-by data-model.md § 4（`artifacts[]`/`id_maps`/`dispositions[]`/`checks`）+ V9/V10/V13/V16
- CHK025 disposition: covered-by contracts/merge-back.contract.md § C-015 + requirements.md § Assumption A6
- CHK026 disposition: covered-by contracts/merge-back.contract.md § C-015 + data-model.md V10/V13
- CHK027 disposition: covered-by contracts/merge-back.contract.md § C-016
- CHK028 disposition: covered-by contracts/merge-back.contract.md § C-017
- CHK029 disposition: covered-by contracts/merge-back.contract.md § C-017（实测 create-team/SKILL.md:99,101 与父 STR-007/008/009 同值）
- CHK032 disposition: covered-by .specify/glossary.md（既有词汇协议指针）
- CHK033 disposition: covered-by test-evidence/checklist-readings-2026-11-10.txt §B（本轮复测一致：57/32/26、父无 review/code-review、verification 8 SC 行）
- CHK034 disposition: covered-by test-evidence/checklist-gates-2026-11-10.txt（本轮复测：父与 074b 均 exit 2）
- CHK035 disposition: covered-by .specify/features/074-goal-team-sdd-unification.md:40（驱动者记录，非 user-authored）
- CHK037 disposition: covered-by contracts/merge-back.contract.md § C-022 + data-model.md § 6 E8
- CHK038 disposition: covered-by contracts/records-and-boundaries.contract.md § C-043 + plan.md § Disclosed Rulings 5
- CHK039 disposition: covered-by data-model.md § 4 E3 `artifacts[].action` / `checks` + V9
- CHK040 disposition: covered-by contracts/records-and-boundaries.contract.md § C-038 + merge-back § C-020 + data-model.md V14

**计数方程（可观察）**：`unchecked(40) = raised-as-finding(10) + covered-by(30)`；`unraised + undispositioned = 0`。分析门禁不被本 pass 阻断。

## I. Decision Tension Records（决策张力记录）— 0 行

确定性读数（`validate-decision-tensions.py --spec .specify/specs/099-speckit-seal --json`，exit 0）：6 条记录（T-001…T-006），六标签 `dtr-anchor` / `dtr-section-missing` / `dtr-record-incomplete` / `dtr-tension-id` / `dtr-rejected-form` / `expected-sacrifice-unmapped` 全部 pass，`channel.high = 0`。人工抽核：六条均含 `decision` / `antithesis` / 双极 `binding_constraints` / `discriminating_evidence` / `expected_sacrifice` / `revision_trigger`；`expected_sacrifice` 逐条解析到对应 SC 的 Measurement Source（SC-003/SC-001/SC-004/SC-007/SC-006/SC-008）。无需复评。

---

## Coverage Summary（覆盖摘要）

| 判定 lane | 结果 | 证据 |
|-----------|------|------|
| FR 被契约条款引用 | **pass** — 28/28（uncovered 0） | `analyze-coverage-2026-11-10.json` → `fr: {universe:28, claimed:28, uncovered:[]}` |
| 条款覆盖差量 | **不可判（fail）** — `baseline-missing`，baseline 持有 0 名 | 同上 → `status: baseline-missing`、`checks[coverage-baseline-delta]`；补救与责任见 §E-02 |
| 条款不可解析 | 685 条 corpus 级 uncovered（baseline 缺席下的全量面，**不可读作本 spec 缺口**）；107 个文件无条款 id（corpus 级 owner-form 噪声） | 同上 → `checks[clause-uncovered]` / `checks[clause-unparsable]` |
| spec 结构校验 | `validate-requirements.py` 0 error / 0 warning（251 行 / 37 定义行 / 3 共享字符串）；`validate-tasks.py` pass | `analyze-gates-2026-11-10.txt` §2–§3 |
| FR → 任务覆盖 | 28/28（`tasks.md` § FR → row trace；每 FR 在至少一行内逐字引用；`pre-analyze-check --stage tasks` → `decision=pass, errors=0`；101 条 advisory 均为未来路径与模板占位符，属 do-not-flag） | `analyze-gates-2026-11-10.txt` §5 |
| SC → 任务覆盖 | 9/9（`tasks.md` § SC → row trace + C-045 首红模块映射） | `tasks.md:351-363`；`contracts/records-and-boundaries.contract.md:120-136` |
| 074 验收基线可复核 | **复现** — 父 57 open / 0 closed；074a 32 closed / 0 open；074b 26 closed / 0 open；父无 `review.md`/`code-review.md`；父 `verification.md` 41 行 / 8 条 SC 状态行（提交 `91726a641` 落盘）；父 requirements `**Path**` 标记 0 | `analyze-gates-2026-11-10.txt` §6；SC-006 五项读数逐项成立 |

## Feature Linkage Summary（特性联动摘要）

| 字段 | 值 | 判定 |
|------|----|------|
| Feature 绑定 | 099 Speckit Seal — requirements § Related Feature + 注册行 `.specify/features.md:102` + 详情文件 | 绑定成立（confidence high） |
| 状态对一致 | 注册行 `Planned` == 详情 `**Status**: Planned` | 一致（`state-drift` 不触发） |
| Spec 路径 | `.specify/specs/099-speckit-seal/requirements.md` | 正确 |
| 特性计数 | `**Total Features**: 90`（plan/feature-ref 声称 89 → 90） | 一致 |
| 阶段记录 | 注册行注记与详情 Latest Review 仍写 plan 阶段；tasks/checklist 阶段产物已落盘 | **陈旧 — §G-01** |
| 相邻特性边界 | 074 = 验收目标（非依赖）；review/sanitize/feature/goal 各自 owner 按指针抵达（C-035/FR-022） | 一致 |

## Constitution Alignment Issues（宪法对齐）

- **0 冲突（0 CRITICAL）**：22 原则 22/22 Pass（plan 22 行，对 live 宪法 I–XXII 逐名核对）。
- 计划内收敛（非 finding，留痕）：`### Feature Lifecycle Management` 状态枚举以 `Completed` 收尾、未含 `Sealed`；FR-003 + T014 经 `manage-constitution` 在同批收敛叙述与版本号。若 T014 未落地，该项升级为 D 类 CRITICAL。
- 质量门：Tests Mode ON（原则 IV）；脚本接口契约（原则 XXI）由 C-003 与引擎契约测试钉住；测试入口唯一（`scripts/bash/run-tests.sh`，原则 XX）；零新增机制（原则 IX/XIV，C-036）。无缺失强制章节。

## Unmapped Tasks（未映射任务）

| 任务行 | 状态 | 判定 |
|--------|------|------|
| T001 | 无行内 FR/SC 引用 | Setup 基础设施（冻结镜像/副本基线与证据落点），按 Phase Map「all」承担全阶段前置；非覆盖缺口。其余 50 行均带至少一个 FR 或 SC/C 编号 |

## Systemic Observations（系统性观察）

1. **需求层「输入派生」缺口成簇**（C-02 / C-03 / C-04 / E-01）：契约层几乎机器完备，但四条需求级输入派生规则缺失（当前 review 集合、STR token 归属、目录级合并单位、分片闭合判据）。这是 checklist 10 条 fail 的共同底色；聚合记录，不提升任何单行严重度。
2. **074 回合契约窄于实测输入**（F-04 / C-03 / B-01）：实测存在五项之外的同号不同义（074a `STR-010`、074b `STR-007`）与大量目录同名产物；回合以「具名阻断」收尾是合法终态，但 SC-006 的「一一对应」措辞会把合法终态读成不合规。
3. **两件审计工具交叉一致**：本轮 12 条 findings 中 10 条源出 checklist 的 10 条 `fail`（逐条对应）；analyze 自身新增仅 2 条治理面 finding（E-02、G-01），未发现 checklist 漏检的需求级缺陷——正向信号，说明 checklist 门禁有效，缺口在需求文本未修订。
4. **测量纪律良好**：074 基线逐项复现（57/32/26、父无 review 记录、verification 8 行、Path 0）；DTR 六标签全 pass；结构校验器全绿；特性状态对一致。
5. **token-efficiency**：checklist 阶段已把固定规则读数（STR 表对比、目录同名集合、Path 计数、闭包 exit）机械写入 `checklist-readings-2026-11-10.txt`；本轮仍重导出了其中多数读数（本报告 §A/§H/§Coverage 的取证）。建议下游把 readings 升级为机读 digest（JSON），供 analyze 直接消费而非重算。

## Metrics（指标）

| 指标 | 读数 |
|------|------|
| FR / SC / RS / STR | 28 / 9（final 6 · supporting 3）/ 3 / 3；Edge Cases 13；Assumptions A1–A7 |
| 契约 / 实体 / 校验规则 / 研究项 / 走查 | 45 条款（4 文件）/ E1–E14 / V1–V16 / R-01…R-21 / S-1…S-9 |
| 任务 / 工作包 / DoD / 门禁 / 决策张力 / 执行前提 | 51 / 9 / 10 / 5 / 6（validator clean）/ 12（全 verified） |
| 覆盖 % | FR 100%（28/28）；条款差量 N/A（baseline 缺席）；结构校验 0 error |
| 特性联动 % | 绑定 1/1；属性一致 6/6；阶段记录陈旧 1 |
| Findings 计数 | CRITICAL 0 · HIGH 7 · MEDIUM 5 · LOW 0 · 合计 12；A0/B1/C4/D0/E2/F4/G1/I0 |
| C/H 复核 | sent 0 · confirm 0 · downgrade 0 · reject 0（未运行）；`proposed` 7 |
| Checklist 问责 | unchecked 40 = raised 10 + covered-by 30；残差 0 |

## Rerun Delta（复跑差量）

首轮分析，无前序 analyze 报告：resolved / new / carried-over 均不适用。本报告的 finding ID（B-01、C-01…C-04、E-01、E-02、F-01…F-04、G-01）是后续复跑（Round 2）比对差量的稳定基线；Round 2 若声明 C/H-only，须按 skill § Rounds 补提全部 MEDIUM/LOW 的 residue 行。

## Next Actions（后续动作 — 不自动修复）

1. **实现前**：7 条 HIGH（B-01、C-03、C-04、E-01、F-01、F-02、F-04）均为 `proposed`，按 `/speckit.analyze` Handoffs 与 skill § Next actions，应经 `/speckit.requirements`（必要时 `/speckit.plan` / `/speckit.tasks`）修订后复跑；或由用户对个别条目显式裁定处置。MEDIUM 5 条（C-01、C-02、F-03、E-02、G-01）建议随同批修复，其中 E-02 的基线冻结是 analyze 覆盖步骤的复跑前提。
2. **门禁判读**：0 CRITICAL；在 HIGH 未处置前，本报告不构成「ready to implement」的裁断。
3. **建议顺序**：requirements 修订（10 条 checklist fail 对应的 B/C/E/F 行）→ 重新生成 tasks trace → 冻结 `coverage-baseline.txt`（E-02）→ 复跑 `/speckit.analyze`（Round 2）。
4. 如需，本报告可给出 top N 条目的**具体修订编辑草案**——按只读纪律不自动应用，由用户批准后经对应阶段命令执行。
