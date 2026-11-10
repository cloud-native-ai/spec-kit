# Analyze 报告（Round 2 · merged）— 099-speckit-seal

> 全 spec 第二轮分析（r1 修复面复裁 + 跨制品一致性 + 074 用例可复核性）。严格只读：未修改任何制品，不自动修复；修复只以建议形式给出。本文件是阶段交付物；确定性读数见同目录 `analyze-r2-gates-2026-11-10.txt`（校验器、074 基线、STR 表、注册表、同名清单、修复锚点复核）与 `analyze-coverage-r2-2026-11-10.json`（覆盖会计引擎完整负载）。

## 顶部计数与指针

| 项 | 值 |
|----|----|
| 轮次 / 判定对象 | Round 2（全量：r1 findings 全严重度复裁 + 新检测） / `.specify/specs/099-speckit-seal/` 全目录（28 FR / 9 SC / 3 RS / 3 STR；plan 6 决策张力 / 12 执行前提 / 9 工作包；4 契约 45 条款；data-model 14 实体 / 16 校验规则；research R-01…R-21（21 条实测）；quickstart S-1…S-9；checklist 40 条） |
| 运行 | `r20261110T121314Z-b099` · stage=analyze（Round 2） · 单 Worker 串行（requested=24 / effective=1 / reason=`budget-reserve`） |
| 四元组 | flow_class=execution；source=declaration；marker=；error=- |
| **结论** | **CONDITIONAL — 0 CRITICAL / 1 HIGH / 5 MEDIUM / 1 LOW（7 条 open）**；r1 的 **7 条 HIGH 全部 closed**（证据见「Rerun Delta」）；新增 1 条 HIGH（F-05，`proposed`）为 B-01 修复的**残留实例**（plan P8 验收锚仍写旧口径）。实现前须修复 F-05（文本级回修）并复跑，或由用户显式裁定处置 |
| Findings 分布（open） | A 0 · B 0 · C 2 · D 0 · E 1 · F 3 · G 1 · I 0；H（清单问责）残差 0（unchecked 40 = raised 10 + covered-by 30） |
| 覆盖 | FR 28/28 被契约条款引用（100%）；条款差量**不可判**（`baseline-missing`，§E-02 延续）；spec 内结构校验 0 error；FR→row / SC→row trace 复验成立（28/28 + 9/9，0 single-row FR）；074 验收基线（57 / 32 / 26 / 8 行 / Path 0）本轮逐项复现 |
| 特性联动 | Feature 099 已绑定：注册行 `.specify/features.md:102` + 详情 `.specify/features/099-speckit-seal.md`；状态对一致（`Planned` == `Planned`）；阶段注记陈旧（§G-01 延续）；Total Features 90 |
| 宪法 | 22 原则 22/22 Pass（plan 22 行对 live 宪法逐名核对，0 mismatch）；0 冲突；1 项计划内叙述收敛（T014，非 finding） |
| 权威指针 | 宪法 `.specify/constitution.md`；分析契约 `.specify/skills/internal/analyze-artifacts/SKILL.md` + `references/`；状态脊 `/storage/project/cloud-native-ai/spec-kit/.specify/state/099-speckit-seal.md`；证据目录 `.specify/specs/099-speckit-seal/test-evidence/` |
| 只读声明 | 制品零修改；唯一落盘是本报告与两份阶段证据（`analyze-r2-gates-2026-11-10.txt`、`analyze-coverage-r2-2026-11-10.json`）；后续修复命令由用户/下游阶段执行 |

### 复核状态（C/H review 标记）

- `validated` = 已由独立 fresh-context 只读复核者确认；`proposed` = 检测结论，等待独立复核波（owner `.specify/skills/internal/analyze-artifacts/references/validation-and-report.md` § 5.5）。
- 本轮按派发的并发读数 `effective=1（budget-reserve）` 单 Worker 串行执行，独立复核波**未派发**，故唯一 HIGH（F-05）标 `(review: proposed)`；无 CRITICAL。MEDIUM/LOW 按契约跳过验证。
- 复核度量：sent 0 / confirm 0 / downgrade 0 / reject 0；降级率 **N/A**（未运行）。
- 同一作者门：**不触发**——本 spec 链由本 SDD 循环的前序阶段运行撰写（提交历史可查），非本会话作者；检测为直读检测（同 checklist 阶段同一判定，先例 `checklists/2026-11-10-requirements-quality.md:12`）。
- 严重度推导：`propagation_surface = none` 的行封顶 MEDIUM；有具名下游的行按缺陷类别取 HIGH/MEDIUM。行内第一个判定列即 `propagation_surface`（owner `.specify/shared/workflow/objective-analysis-gate.md` rule 3）。F-05 承载 P8 的 SC-006 验收锚 → 按「不可测/冲突的验收标准」判 HIGH（owner `.specify/shared/guidelines/closed-set-claims.md` § 处置）。
- 覆盖采样（zero-finding floor 的等价执行）：r2 有 C/H，但为加固覆盖结论仍执行——0 条 single-row FR；抽 5 条 FR（FR-003 / FR-013 / FR-016 / FR-022 / FR-028）复读其 trace 行，全部至少一行行内引用成立（详见 Coverage Summary）。

### 检测通过范围（本轮实际运行）

A 重复 · B 歧义 · C 欠规定 · D 宪法（plan 22 行 Constitution Check 对 live 22 原则逐名程序化核对）· E 覆盖（accountant + FR→row / SC→row trace 机检 + 未映射任务）· F 不一致（含封闭集声明检查，owner `.specify/shared/guidelines/closed-set-claims.md`；对 r1 修复引入/应消除的措辞做全链短语扫描）· G 特性相关性与阶段记录 · H 清单问责 · I 决策张力（`validate-decision-tensions.py`：6 records，六标签全 pass，high=0）。

---

## A. Duplication（重复）— 0 行

零发现取证：FR-012 的 15 项输出件封闭宇宙与 `contracts/merge-back.contract.md` C-013 逐项比对**完全一致**（15/15，含 r1 修复新增的文件级规则）；FR/SC/STR 编号连续与引用可解析由 `validate-requirements.py`（0 error / 0 warning）与 `validate-tasks.py`（pass）钉住；`feature-ref.md` 的 FR→条款映射由 `clause_extract.py` 从契约引用组**再生**，本轮实跑输出与文件表格逐项一致（28/28，最大差集为空）。FR-012 ↔ C-013 的枚举复述通过 one-source-of-truth 的 stale-copy 判定（两侧逐字一致，契约层是符合性 owner），**不构成 finding**。

## B. Ambiguity（歧义）— 0 行（open）

- **B-01 已 closed**（见 Rerun Delta）：SC-006 / US3 / Independent Test / FR-027 / C-043 / plan Summary / T-005 / quickstart S-7 / tasks DoD-6·T043·T044 已统一为「五项是下限 + 额外阻断逐条点名」。**残留实例另立 §F-05**（plan P8 行未随修复，属不一致面，不重复计为 B 类）。
- 零发现取证：live 制品无 `TODO` / `TKTK` / `???` 占位符（grep 0 命中）；无可测性缺失的模糊形容词新增。

## C. Underspecification（欠规定）— 2 行（open）

| ID | propagation_surface | Category | Severity | Location(s) | Summary | Recommendation |
|----|---------------------|----------|----------|-------------|---------|----------------|
| C-01 | `data-model.md` §2 E1/E2（审计更正记录形态）及未来审计更正消费者 | C Underspecification | MEDIUM（carried over） | `requirements.md:125`（FR-002）；`contracts/status-sealed.contract.md:29`（C-026）；`data-model.md:42`（E1） | 审计更正 `Sealed → Ready for Review` 要求「携带使原封装结论不成立的证据并落在两处载体」，但证据的最小形态（字段/出处/判定人）仍无可判定义；E1–E14 无对应实体或字段，`archive-gate`/漂移守卫无从校验一次回退是否合法 | 在 requirements/data-model 定义审计更正证据的最小载体（如 review.md 追加段 + 注册表行与详情同批引用），并指明校验器（CHK002） |
| C-02 | `scripts/python/seal-utils.py`（T028 前置条件）；`tests/contract/test_seal_seal.py`（T026） | C Underspecification | MEDIUM（carried over） | `requirements.md:132`（FR-006）；`data-model.md:70`（E2 `review.paths[]`） | 「当前 `review.md`（若存在多个，取当前记录集合，归档记录不计）」仍缺「当前集合」的派生规则（命名约定或记录指针）；仓内实测并存 `review-081a.md`、`review-r1.md`、`review-second-slice.md` 等异构记录，引擎无法机械区分当前与归档 | 裁定并记录 review 记录「当前集合」派生规则（如：spec 根 `review.md` 为当前，`review-*.md` 不计），写入契约与夹具（CHK005） |

- **C-03 已 closed**：FR-012 现含目录型候选的**文件级合并单位**与同名三态（`merge` / `create` / `keep`），契约 C-013、data-model E5/V9、tasks T018–T023/T040 同链落盘。
- **C-04 已 closed**：FR-016 现含 **token→注册表绑定**（spec 自身 § Shared Strings 为登记处；spec 外文档须显式声明；未声明时跨登记处解析，零命中/多命中不同值判冲突），C-017 与 tasks T018/T019/T020/T023 同链落盘。

## D. Constitution Alignment（宪法对齐）— 0 行

复核方式：plan § Constitution Check 的 22 行（I–XXII）对 `.specify/constitution.md` 的 22 个原则标题**程序化**逐名核对（22/22，name mismatch 0），并复查 VII（工作流门）、XIV（单一真源）、XXI（脚本接口契约）、XXII（Re-Anchoring）对应的设计落点。**无 MUST 冲突、无缺失强制章节或质量门。** 一处**计划内**叙述收敛记录于下（非 finding）：宪法 `## Feature Governance` § Feature Lifecycle Management 的状态枚举仍以 `Completed` 收尾，不含 `Sealed`；FR-003 与 T014 已把「schema owner 为准、叙述面同次收敛（经 `manage-constitution` 程序与版本号递增）」排进同一变更。若实现时 T014 被丢弃，则该处将升级为 D 类 CRITICAL。

## E. Coverage Gaps（覆盖缺口）— 1 行（open）

| ID | propagation_surface | Category | Severity | Location(s) | Summary | Recommendation |
|----|---------------------|----------|----------|-------------|---------|----------------|
| E-02 | `tasks.md` T050 coverage-final 对照 + 覆盖门禁证据 | E Coverage Gaps | MEDIUM（carried over） | `.specify/specs/099-speckit-seal/coverage-baseline.txt`（缺席）；`tasks.md:102`（T002 把冻结排进 implement 阶段） | 覆盖会计引擎本轮再次报 `status: baseline-missing`（exit 2；corpus 290 文件 / parsed 183 / named-unparseable 107）——「absent baseline is NOT an empty exemption list」，覆盖差量仍不可判定；冻结基线是 `/speckit.tasks` 的 C-6 义务，T002 却把它推迟到 implement 阶段 | 由 tasks 阶段（或最迟 implement 入口前）执行 `account-clause-coverage.py --spec-dir .specify/specs/099-speckit-seal --freeze > coverage-baseline.txt`，然后复跑 analyze 覆盖步骤；MUST NOT 把 baseline 缺席读作通过 |

- **E-01 已 closed**：FR-008 现定义「分片已闭合」判据（`- [ ]` / `- [>]` 计数 0；`- [~]` 须在分片 `verification.md` 的 `deferred_tasks=` 有名）+ 封闭拒绝码 `slice-unclosed`；Edge Cases、C-042、data-model E12、tasks T026/T028、quickstart S-5 同链落盘。

## F. Inconsistency（不一致）— 3 行（open；F-01 / F-02 / F-04 已 closed）

| ID | propagation_surface | Category | Severity | Location(s) | Summary | Recommendation |
|----|---------------------|----------|----------|-------------|---------|----------------|
| F-03 | none（C-039 已收窄；引擎与测试继承契约，不继承矛盾） | F Inconsistency | MEDIUM（carried over） | `requirements.md:33`（US1「工作树」）；`requirements.md:112`（Edge Cases）；`requirements.md:136`（FR-010）；`contracts/records-and-boundaries.contract.md:64`（C-039） | dirty 判定范围在需求内仍并存两种表述（US1「工作树」vs FR-010/Edge Cases「父 spec 树」）；C-039 已收窄为 `git status --porcelain -- <parent-spec-dir>` 并明写排除目录外路径，但需求文本未收敛 | 收敛 FR-010 / Edge Cases / US1 三处措辞为「父 spec 树」，并按 C-039 指针引用（CHK010） |
| F-05 | plan P8 验收锚 → 074 回合的实现派发与验收判读 | F Inconsistency | **HIGH**（review: proposed；new — B-01 残留实例） | `plan.md:310`（P8 行「阻断清单与 FR-027 五项一一对应」） | r1 B-01 的修复波更新了 requirements/契约/plan Summary/T-005/quickstart/tasks，但 plan P8 工作包的**验收锚**仍保留旧口径「五项**一一对应**」——与 SC-006「至少逐条覆盖 + 五项之外逐条点名即合规」直接冲突；该短语是封闭集声明（owner `shared/guidelines/closed-set-claims.md`），会把合法的第六类阻断读成不合规，且 P8 是 074 回合的派发验收依据 | 文本级回修 `plan.md:310`：改为「阻断清单逐条覆盖 FR-027 五项（下限）+ 额外具名阻断逐条点名」；同步做一次**短语级全链扫描**（grep `一一对应` / `恰好五项`）确认无其他残留；修复后复跑 analyze（Round 3 或 F-05-only 复裁） |
| F-06 | none（plan / feature-ref 的叙述面自身） | F Inconsistency | LOW（new） | `plan.md:62`、`plan.md:169`、`feature-ref.md:115`（另 `.specify/features.md:102` 行内注记含同短语，归 §G-01 一并刷新） | research 计数漂移：`research.md` 实有 **21** 条记录（R-01…R-21，`grep -cE '^## R-[0-9]{2}'` = 21），上述三处写「R-01…R-20」；同文件 `plan.md:327` 与 `tasks.md:7` 写「R-01…R-21」，制品内自相矛盾 | 三处改为「R-01…R-21」；该行随 G-01 的注册行刷新一并处理 |

- **F-01 已 closed**：dated-record 目录（`test-evidence/`、`checkpoints/`）同名文件改为「父级 `keep` + 合并清单指针纳入；仅分片有时父级指针视图 `create`，原件字节不变」（FR-012 / FR-019 / C-013 / C-020 / E5·V9 / T019·T021·T023·T040）。
- **F-02 已 closed**：FR-012 必选下限加入父 `code-review.md` 汇总指针视图；FR-006 缺 `review.md` **或** `code-review.md` → `review-missing`（exit 1）；C-013 / C-021 / C-042 / E12 / T028 / T040 同链落盘。
- **F-04 已 closed**：FR-027(b) 现枚举两组实测同号不同义（074a 本地 `STR-010`=`"seats"` → 父 `STR-011`；074b 本地 `STR-004`–`STR-007`=`completed`/`blocked`/`failed`/`## Nested SDD Runs` → 父 `STR-007`–`STR-010`）；父表逐行复核一致（gates §8）；tasks T039/T044、quickstart S-2 同步。

## G. Feature Relevance & Accuracy（特性相关性与阶段记录）— 1 行（open）

| ID | propagation_surface | Category | Severity | Location(s) | Summary | Recommendation |
|----|---------------------|----------|----------|-------------|---------|----------------|
| G-01 | none（注册表行与详情自身的阶段注记） | G Feature Relevance & Accuracy | MEDIUM（carried over） | `.specify/features.md:102`；`.specify/features/099-speckit-seal.md:20` | 阶段记录仍陈旧：tasks / checklist / analyze（两轮）产物已落盘，但注册行注记仍写「planned via /speckit.plan」、详情 `## Latest Review` 仍写「当前阶段为 plan」；`shared/workflow/feature-integration.md` § Core Protocol steps 2–3 的阶段记录义务未随阶段推进。状态 `Planned` 本身合法，但 lawful status 不豁免阶段记录（另该行注记含 research「R-01…R-20」短语，随 §F-06 一并改） | implement 前由 `manage-features` reconcile 刷新注册行注记与详情阶段行；本阶段按 feature-integration 属 `/speckit.tasks` 的已发生义务，记入本报告供下游收口 |

## H. Checklist Accountability（清单问责）— 残差 0

判定对象：`checklists/2026-11-10-requirements-quality.md` 的 40 条未勾选项（`checklists/requirements.md` 全部已勾选，不计）。清单是 dated 评估记录，本轮**未修改**；每项给出机读处置标记，括注为 r2 状态：

**raised-as-finding（10）**

- CHK002 disposition: raised-as-finding C-01（r2: open — MEDIUM carried over）
- CHK005 disposition: raised-as-finding C-02（r2: open — MEDIUM carried over）
- CHK010 disposition: raised-as-finding F-03（r2: open — MEDIUM carried over）
- CHK016 disposition: raised-as-finding C-03（r2: **closed** — FR-012 文件级单位/同名三态 + C-013 + E5/V9 + T018–T023/T040）
- CHK017 disposition: raised-as-finding F-01（r2: **closed** — 指针纳入语义 FR-012/FR-019 + C-013/C-020 + E5/V9）
- CHK018 disposition: raised-as-finding F-02（r2: **closed** — 必选下限 + `review-missing`：FR-012/FR-006 + C-013/C-021/C-042 + E12）
- CHK021 disposition: raised-as-finding E-01（r2: **closed** — FR-008 闭合判据 + `slice-unclosed` + C-042 + E12 + T026/T028）
- CHK030 disposition: raised-as-finding C-04（r2: **closed** — token→注册表绑定 FR-016 + C-017 + 夹具 T018/T019）
- CHK031 disposition: raised-as-finding F-04（r2: **closed** — FR-027(b) 两组枚举 + T039/T044 + S-2）
- CHK036 disposition: raised-as-finding B-01（r2: **closed**，残留实例另立 F-05 — SC-006 下限口径全链同步，唯 plan P8 行未随）

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
- CHK033 disposition: covered-by test-evidence/checklist-readings-2026-11-10.txt §B（r2 复测一致：57/32/26、父无 review/code-review、verification 8 SC 行）
- CHK034 disposition: covered-by test-evidence/checklist-gates-2026-11-10.txt（r2 复测：父与 074b 闭包判定器均 exit 2；见 gates §17）
- CHK035 disposition: covered-by .specify/features/074-goal-team-sdd-unification.md:40（驱动者记录，非 user-authored）
- CHK037 disposition: covered-by contracts/merge-back.contract.md § C-022 + data-model.md § 6 E8
- CHK038 disposition: covered-by contracts/records-and-boundaries.contract.md § C-043 + plan.md § Disclosed Rulings 5
- CHK039 disposition: covered-by data-model.md § 4 E3 `artifacts[].action` / `checks` + V9
- CHK040 disposition: covered-by contracts/records-and-boundaries.contract.md § C-038 + merge-back § C-020 + data-model.md V14

**计数方程（可观察）**：`unchecked(40) = raised-as-finding(10) + covered-by(30)`；`unraised + undispositioned = 0`。分析门禁不被本 pass 阻断。

## I. Decision Tension Records（决策张力记录）— 0 行

确定性读数（`validate-decision-tensions.py --spec .specify/specs/099-speckit-seal --json`，exit 0）：6 条记录（T-001…T-006），六标签 `dtr-anchor` / `dtr-section-missing` / `dtr-record-incomplete` / `dtr-tension-id` / `dtr-rejected-form` / `expected-sacrifice-unmapped` 全部 pass，`channel.high = 0`；333 行扫描。T-005 的 `discriminating_evidence` 已随 B-01 修复改为「至少逐条覆盖五项实测输入、并逐条点名额外阻断」。无需复评。

---

## Rerun Delta（复跑差量）

### Resolved Since Last Run（7）

| ID | 级别 | 关闭证据（本轮直读复核） |
|----|------|--------------------------|
| B-01 | HIGH | `requirements.md:191`（SC-006「五项之外的实测阻断只需逐条点名即合规」+ 验收断言）；`:69`（US3「下限而非上限」）；`:73`（IT）；`:162`（FR-027「五项是下限」）；C-043「五项是下限」；plan:31 / :145；quickstart S-7:171；tasks DoD-6 / T043 / T044 / Phase 6 IT。**残留实例 → §F-05** |
| C-03 | HIGH | `requirements.md:141`（目录型候选文件级单位 + 同名三态）；C-013:27–37；data-model E5:132 / V9:112；tasks T018（夹具）/T019/T020/T021/T023/T040 |
| C-04 | HIGH | `requirements.md:145`（token→注册表绑定）；C-017:72–80；tasks T018（未声明登记处夹具）/T019/T020/T023 |
| E-01 | HIGH | `requirements.md:134`（FR-008 分片闭合判据）；`:107`（Edge Case）；C-042:93（`slice-unclosed`）；data-model E12:180；tasks T026/T028；quickstart S-5:122 |
| F-01 | HIGH | `requirements.md:141`（dated-record 指针纳入）/`:148`（FR-019）；C-013:30–32 / C-020:102–108；data-model E5/V9；tasks T019/T021/T023/T040 |
| F-02 | HIGH | `requirements.md:141`（必选下限含父 `code-review.md`）/`:132`（`review-missing` 双文件）；C-013:32–35 / C-021:116；C-042:92；data-model E12:174；tasks T028/T040 |
| F-04 | HIGH | `requirements.md:162`（FR-027(b) 两组实测枚举）；父 STR 表逐行复核（gates §8：STR-007…011 = completed/blocked/failed/`## Nested SDD Runs`/seats）；074a:90 映射行；074b:69/:72 映射行；tasks T039/T044；quickstart S-2 |

### New Since Last Run（2）

| ID | 级别 | 来源说明 |
|----|------|----------|
| F-05 | **HIGH**（review: proposed） | r1 B-01 的**残留实例**（修复波更新了 Summary/T-005，未覆盖 P8 验收锚 `plan.md:310`）；措辞级全链扫描 `一一对应` 仅此一处 live 命中（另一处为 dated checklist） |
| F-06 | LOW | 本轮新检测；research 记录计数漂移（21 条 vs 三处「R-01…R-20」），非修复引入 |

### Carried Over（5，main table 标 `carried over`）

C-01 · C-02 · F-03 · E-02 · G-01（均为 MEDIUM；r2 重新验证缺陷仍成立，见各节）。

> **判定纪律**：headline 不以「r1 的 7 条 HIGH 已清」读作 ready to implement——F-05 是新发现的 open HIGH（见 validation-and-report § 6：cleared backlog ≠ clean rerun）。

## Coverage Summary（覆盖摘要）

| 判定 lane | 结果 | 证据 |
|-----------|------|------|
| FR 被契约条款引用 | **pass** — 28/28（uncovered 0） | `analyze-coverage-r2-2026-11-10.json` → `fr: {universe:28, claimed:28, uncovered:[]}`；`clause_extract` 再生映射与 `feature-ref.md` 逐项一致 |
| 条款覆盖差量 | **不可判（fail）** — `baseline-missing`（exit 2） | 同上 → `status: baseline-missing`、`checks[coverage-baseline-delta]`；补救与责任见 §E-02 |
| 条款不可解析 | 685 条 corpus 级 uncovered / 107 个无条款 id 文件（corpus 级 owner-form 噪声，**不可读作本 spec 缺口**） | 同上 → `checks[clause-uncovered]` / `checks[clause-unparsable]`；扫描 290 文件（parsed 183 + named-unparseable 107） |
| spec 结构校验 | `validate-requirements.py` 0 error / 0 warning（251 行 / 37 定义行 / 3 共享字符串）；`validate-tasks.py` PASS；`pre-analyze-check` requirements/plan/tasks 三阶段均 `decision=pass` errors=0（101 advisory 均为未来路径与模板占位符） | `analyze-r2-gates-2026-11-10.txt` §2–§5 |
| FR → 任务覆盖 | 28/28（每 FR ≥1 行行内逐字引用）；trace 表机检复验：28 FR / 9 SC traced，51 行，**0 条 single-row FR**；抽样 5 条 FR（FR-003/013/016/022/028）全部覆盖成立 | gates §15；观察 O-1（trace 含 supporting rows） |
| SC → 任务覆盖 | 9/9（trace + C-045 首红模块映射） | `tasks.md:351-363`；C-045:124–136 |
| 074 验收基线可复核 | **逐项复现** — 父 57 open / 0 closed；074a 32 closed / 0 open；074b 26 closed / 0 open；父无 `review.md`/`code-review.md`；父 `verification.md` 41 行 / 8 条 SC 状态行（提交 `91726a641`）；父 requirements `**Path**` 0；闭包判定器 exit 2 复现（父 `requirements.md:392` / 074b `:210` 均 `SC-001 carries 0 **Path** markers`）；拆分记录 `proposed_slices` 1 处、顺序 074a → 074b；074b `code-review.md` blocking 0；P0 F1 见 review.md:304；两片 `## Parent Mapping` 均存在 | gates §7 / §13 / §17；SC-006 五项读数逐项成立 |
| 决策张力 | 6 records / 六标签 pass / high=0 | gates §4 |

## Feature Linkage Summary（特性联动摘要）

| 字段 | 值 | 判定 |
|------|----|------|
| Feature 绑定 | 099 Speckit Seal — requirements § Related Feature + 注册行 `.specify/features.md:102` + 详情文件 | 绑定成立（confidence high） |
| 状态对一致 | 注册行 `Planned` == 详情 `**Status**: Planned` | 一致（`state-drift` 不触发） |
| Spec 路径 | `.specify/specs/099-speckit-seal/requirements.md` | 正确 |
| 特性计数 | `**Total Features**: 90` | 一致 |
| 阶段记录 | 注册行注记与详情 Latest Review 仍写 plan 阶段；tasks/checklist/analyze 产物已落盘 | **陈旧 — §G-01（carried over）** |
| 相邻特性边界 | 074 = 验收目标（非依赖）；review/sanitize/feature/goal 各自 owner 按指针抵达（C-035/FR-022） | 一致 |

## Constitution Alignment Issues（宪法对齐）

- **0 冲突（0 CRITICAL）**：22 原则 22/22 Pass（plan 22 行对 live 宪法 I–XXII 程序化逐名核对，0 mismatch）。
- 计划内收敛（非 finding，留痕）：`### Feature Lifecycle Management` 状态枚举以 `Completed` 收尾、未含 `Sealed`；FR-003 + T014 经 `manage-constitution` 在同批收敛叙述与版本号。若 T014 未落地，该项升级为 D 类 CRITICAL。
- 质量门：Tests Mode ON（原则 IV）；脚本接口契约（原则 XXI）由 C-003 与引擎契约测试钉住；测试入口唯一（`scripts/bash/run-tests.sh`，原则 XX）；零新增机制（原则 IX/XIV，C-036）。

## Unmapped Tasks（未映射任务）

| 任务行 | 状态 | 判定 |
|--------|------|------|
| T001 | 无行内 FR/SC 引用 | Setup 基础设施（冻结镜像/副本基线与证据落点），按 Phase Map「all」承担全阶段前置；非覆盖缺口。其余 50 行均带至少一个 FR 或 SC/C 编号 |

## Systemic Observations（系统性观察）

1. **修复面收束良好，残留归因明确**（F-05）：7 条 HIGH 的修复都做了跨制品同步，唯 plan P8 行因「按 finding 位置清单驱动修复、未做被修正措辞的短语级全链扫描」而漏网。校准建议：修复轮把「新措辞的 grep 证据」列为与文件清单并列的完成条件（已写入 feedback）。
2. **需求层「输入派生」缺口成簇**（C-01 / C-02 / F-03，均 carried over）：三处都是「一句括注承载机器判定」。建议下轮回修按「判据 + 派生规则 + 校验器」三件套一次收口，避免逐条补丁。
3. **两件审计工具交叉一致**：checklist 的 10 条 `fail` 与 r1 的 10 条 findings 逐条对应；r2 修复复核与 checklist 判定位一一对应。本轮新增的 F-05/F-06 属跨制品措辞/计数面——checklist 的判定域不覆盖此类，属 analyze 独有面（正向信号：两件工具互补而非重复）。
4. **测量纪律良好**：074 基线第二轮逐项复现；STR 表逐行复核一致；DTR 六标签全 pass；结构校验器全绿；宪法逐名核对 0 mismatch；状态对一致。
5. **token-efficiency**：checklist 阶段已把固定规则读数机械写入 `checklist-readings-2026-11-10.txt`，本轮 analyze 仍重导出多数读数（同 r1 反馈）；建议把 readings 升级为机读 digest（JSON），供 analyze 直接消费。
6. **观察 O-1（非 finding）**：tasks § FR→row / SC→row trace 表含 supporting rows——机检显示 22 个 (row, ID) 对未在该行行内逐字引用（如 FR-010→T028、FR-028→T044），但 DoD-1 要求的「每 FR/SC ≥1 行行内引用」不变量成立（28/28 + 9/9）。建议 tasks 阶段注明 trace 的「支持行」语义，或改为机生成。

## Metrics（指标）

| 指标 | 读数 |
|------|------|
| FR / SC / RS / STR | 28 / 9（final 6 · supporting 3）/ 3 / 3；Edge Cases 13；Assumptions A1–A7 |
| 契约 / 实体 / 校验规则 / 研究项 / 走查 | 45 条款（4 文件，clause_extract 复算 10+13+8+14）/ E1–E14 / V1–V16 / R-01…R-21（21 条）/ S-1…S-9 |
| 任务 / 工作包 / DoD / 门禁 / 决策张力 / 执行前提 | 51 / 9 / 10 / 5 / 6（validator clean）/ 12（全 verified） |
| 覆盖 % | FR 100%（28/28）；条款差量 N/A（baseline 缺席）；结构校验 0 error |
| 特性联动 % | 绑定 1/1；属性一致 6/6；阶段记录陈旧 1 |
| Findings 计数（open） | CRITICAL 0 · HIGH 1 · MEDIUM 5 · LOW 1 · 合计 7；A0/B0/C2/D0/E1/F3/G1/I0 |
| r1 findings 处置 | closed 7（B-01、C-03、C-04、E-01、F-01、F-02、F-04）/ rejected 0 / carried 5 |
| C/H 复核 | sent 0 · confirm 0 · downgrade 0 · reject 0（独立波未运行）；`proposed` 1（F-05） |
| Checklist 问责 | unchecked 40 = raised 10 + covered-by 30；残差 0 |

## Next Actions（后续动作 — 不自动修复）

1. **阻断项（HIGH）**：修复 F-05（`plan.md:310` 的旧口径短语，文本级回修；建议同时 grep `一一对应` / `恰好五项` 做全链确认），然后复跑 `/speckit.analyze`（Round 3 或 F-05-only 复裁）。在 F-05 关闭前，本报告不构成「ready to implement」的裁断。
2. **MEDIUM 建议随同批修复**：C-01（审计更正证据最小形态）、C-02（review「当前集合」派生规则）、F-03（dirty 判定范围措辞）、G-01（`manage-features` 刷新阶段注记）；**E-02 的基线冻结是 analyze 覆盖步骤的复跑前提**（由 tasks 阶段或 implement 入口前执行）。
3. **LOW**：F-06 的三处 research 计数改为 R-01…R-21（随 G-01 的注册行刷新一并处理）。
4. 如需，本报告可给出各条的**具体修订编辑草案**——按只读纪律不自动应用，由用户批准后经对应阶段命令执行。
