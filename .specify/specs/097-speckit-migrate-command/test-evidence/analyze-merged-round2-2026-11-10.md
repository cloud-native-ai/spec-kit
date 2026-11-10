# Analyze — Merged Findings Report, Round 2（097-speckit-migrate-command）

**Stage**: analyze · Round 2（C/H 修复轮之后的重新过门；并发波 W1/W2/W3）· **Date**: 2026-11-10
**Inputs（只读）**: `test-evidence/analyze-findings-round2-W1.md`（29 行：requirements.md + checklists）、`analyze-findings-round2-W2.md`（14 行：plan.md / data-model.md / quickstart.md / 3 份契约）、`analyze-findings-round2-W3.md`（19 行：tasks.md + 宪法 D 通道）——三路文件级互斥读域。
**Authority**: 本特性 spec 全目录（requirements / plan / research / data-model / contracts / quickstart / feature-ref / tasks / checklists）+ `.specify/constitution.md` + `analyze-artifacts` 契约（`.specify/skills/internal/analyze-artifacts/`）。
**确定性归并规则**: ①分节 = 按严重度 HIGH → MEDIUM → LOW（本轮无 CRITICAL 新增）；②节内字典序 = finding ID（`W1-* < W2-* < W3-*`，同波内数字序）；③重复 id = 先声明先得 + 指针替代（含跨轮次归一化：round-2 W2 的 14 个原始 id 与 round-1 W2-01…W2-13 数字碰撞，按内容逐一裁定为「指针回 round-1 id」或「顺延重编号 W2-14…W2-20」，映射表见 §10）。
**Read-only**: 本波未修改任何 spec 制品、未修复任何 finding；产物仅本文件（+ Wrap-up 记账引擎记录）。集成者未撰写上游制品；三个 worker 均为 fresh-context 只读检测，same-author 委派条件成立。
**Validation status（未做，不可省）**: 3 条 HIGH（W3-09 升格、W3-15 新增、W3-16 新增）**尚待驱动侧独立只读验证波**（契约 §7）。验证完成前本文件不构成 analyze gate 的通过证据；MEDIUM/LOW 不阻断门。
**H 问责（§5 H 通道，源 W1 round-2）**: `unchecked=39; dispositioned=39 (raised-as-finding=23, covered-by=16); undispositioned=0; 39 − (23 + 16) = 0`；`[Gap] 子集: unchecked=16, raised=10, covered-by=6, undispositioned=0`。**计数更正**：round-1 报告 `[Gap] 15/15`，本轮机械重数为 **16**（round-1 记 15 为计数错误，记于此不静默）。逐条 ledger 见附录 A。
**Cap accounting**: 契约「≤50 findings」为**单次检测通道**产物上限；本文件是三路互斥读域的确定性归并（29 / 14 / 19，各自低于上限）。当前开放账本 55 行，相对单通道上限溢出 5 行（字典序末位 LOW 四条 + 一条 MEDIUM），按阶段指令不截断，在 §8 Metrics 显式记账。

---

## 0. C/H 汇总与指针（不修复）

> 只做汇总与指针：不验证、不降级、不修改任何制品。验证波完成后按验证裁决重写。

### 0.1 Round-1 C/H（11 = CRITICAL 2 + HIGH 9）修复复核状态

| ID | 原严重度 | Round-2 复核结论 | 复核来源与证据 | 残差 |
|----|----------|------------------|----------------|------|
| W3-01 | CRITICAL | **fixed（复核确认）** | W3 round-2 §A：sigil 已改为行内 `<!-- deferred: reason -->`（tasks.md:77），宪法 VII（L224）字面满足 | 无 |
| W3-02 | CRITICAL | **fixed（复核确认）** | W3 round-2 §A：DoD-7 L39 / GATE-4 L51 / T048 L264 载体均已是 `verification.log` | **W3-16**（pkg07 写域 L113 仍写 `verification.md`）+ **W3-18**（该载体被 `.gitignore` `*.log` 忽略） |
| W1-01 | HIGH | **fixed（复核确认）** | W1 round-2 §1：FR-018 已明示干跑回执走输出流、不落盘（requirements.md:134） | 无 |
| W1-02 | HIGH | **fixed（复核确认）** | W1 round-2 §1：FR-018 字段清单补齐；FR-020 已定义 `source.json` 读取与 `unavailable` 回退（:134/:139） | 无 |
| W1-03 | HIGH | **fixed（复核确认）** | W1 round-2 §1：FR-023 构成清单补三类并绑定 SC-001 五维（:145） | 无 |
| W1-04 | HIGH | **fixed（复核确认）** | W1 round-2 §1：FR-019 要求机器可读 outcome token（:135） | 无 |
| W1-05 | HIGH | **fixed（复核确认）** | W1 round-2 §1：FR-019 补结局优先级聚合规则（:135） | 无 |
| W1-06 | HIGH | **fixed（复核确认）** | W1 round-2 §1：FR-005 钉名 `get_resource_path()` 判定与框架源/客户端来源切换（:115） | 无 |
| W2-01 | HIGH | **fixed（修复记录 + 间接重测）** | 修复处置：E-8 templates-generated 行改为 4 个镜像对（data-model.md:121），与 :124 两对合计 6。W2 round-2 §已检查面机械重测「镜像对 4+2=6（E-8 ↔ migrate-engine.md:15）」一致；**W2 round-2 读域不含旧 id，未做显式重裁**——独立验证依据为修复轮 confirm（11/11） | 无 |
| W2-04 | HIGH | **fixed（修复记录 + 间接重测）** | 修复处置：`error` 显式声明为退出类别、非 outcome token（data-model.md:102、migrate-cli.md:39）。W2 round-2 §已检查面重测「4 类结局（E-5/C-3/C-4）一致」；同上未做旧 id 显式重裁 | 无 |
| W3-03 | HIGH | **fixed（复核确认）** | W3 round-2 §A：DoD-1 Check 已只统计任务行，实测返回 25 | **W3-15**（修复新增的变异判据机械不成立） |

### 0.2 Round-2 C/H（3 HIGH，open，待独立验证）

| ID | 严重度 | 锚点 | 一句话事实 | 指针 / 验证状态 |
|----|--------|------|------------|-----------------|
| W3-09 | HIGH（round-1 MEDIUM **升格**） | tasks.md DoD-3（L35）× T013（L154） | DoD-3 的「源码守卫在任一复制实现被移除时转红」仍与 no-second-engine 方向相反，且其 Check 只运行套件、无法验证该变异主张；承载 DoD-3，按 closed-set-claims § 处置升格 HIGH | 本文 §2；源 W3。**待独立验证** |
| W3-15 | HIGH（本轮新增） | tasks.md DoD-1（L33） | W3-03 修复新增的可转红判据「删除任一任务行的 FR 引用必须使该计数小于 25」机械不成立：23 个 FR 由 ≥2 条任务行点名，实删 T014 行的 FR-001 后计数仍为 25 | 本文 §2；源 W3。**待独立验证**；集成者复测 R2 一致 |
| W3-16 | HIGH（本轮新增） | tasks.md Package Map pkg07 写域（L113）× T048（L264）/ DoD-7（L39）/ GATE-4（L51） | W3-02 的载体修复未传播完：pkg07 写域仍列 `verification.md`，而真正的闭包载体是 `verification.log`；pkg07 执行者按声明写域无权写该载体，同一事实两个名字 | 本文 §2；源 W3。**待独立验证**；集成者复测 R7 一致 |

**C/H 合计**: CRITICAL 0（round-1 两条已复核 fixed）· HIGH 3（open，待验证）。

### 0.3 门状态声明

- 3 条 HIGH 经独立只读验证确认前，本文件**不构成** analyze gate 通过证据；验证波由驱动侧派发（契约 §7）。
- 无 CRITICAL 新增；无宪法类 CRITICAL（round-1 的两条 CRITICAL 已按宪法字面修复并经 W3 round-2 复核）。
- MEDIUM/LOW 共 52 行按契约不阻断门（§2–§4 的余量部分）。

---

## 1. Round-1 C/H 复核补充事实（11 行，细节归 worker）

- W1 round-2 对本读域 24 条 round-1 findings 做了**全严重度重裁**（非 C/H-only）：6/6 HIGH 复核 fixed；18 条 M/L 中 2 条 incidental fixed（W1-11 经 FR-019 修复、W1-14 经 FR-005 修复），16 条 open（15 MEDIUM + 1 LOW），逐条见 §3/§4。
- W3 round-2 对 tasks.md 做了全严重度重裁：W3-01/W3-02（CRITICAL）与 W3-03（HIGH）fixed；W3-09 升格 HIGH；W3-04…W3-14 残差 open；新增 W3-15…W3-19。
- W2 round-2 明确声明「读域不含任何 round-1 findings 文件，本文件不声称关闭 round-1 条目」；W2-01/W2-04 的 fixed 结论来自修复处置记录（`analyze-repair-dispositions-2026-11-10.md`），W2 round-2 仅在被检面机械重测处提供一致读数（见 §0.1）。
- 修复传播残差（系统观察，见 §9 S-1）：W3-02 的修复未传播到 Package Map（→W3-16）；W3-03 的修复引入的新判据本身不成立（→W3-15）。

---

## 2. HIGH（3 行，open，待验证）

| ID | 状态 | 锚点 | 一句话事实 | 建议归属 |
|----|------|------|------------|----------|
| W3-09 | R1-open · **MEDIUM→HIGH 升格** | tasks.md DoD-3（L35）× T013（L154） | DoD-3 的 "源码守卫在任一复制实现被移除时转红" 仍与 no-second-engine 方向相反，且其 Check 只运行套件、无法验证该变异主张；该断言承载 DoD-3，按 closed-set-claims § 处置（DoD/验证门承载的不可测断言 → HIGH）升格。 | /speckit.tasks（更正红条件方向，或补一条变异红测） |
| W3-15 | **R2-new** | tasks.md DoD-1（L33） | 修复后新增的可转红判据 "删除任一任务行的 FR 引用必须使该计数小于 25" 机械不成立：25 个 FR 中 23 个由 ≥2 条任务行点名，实删 T014 行的 FR-001 后计数仍为 25（`sed '170s/FR-001//' … \| wc -l` → 25），只有删掉单点 FR-004/FR-008（T016/T015）才降到 24；声称的 "任一" 红条件无法按字面满足。 | /speckit.tasks（改为 "删除某 FR 的全部行内引用后该 FR 必须消失" 的变异，或按每条 FR 的引用行清单执行删除；保留实测读数） |
| W3-16 | **R2-new** | tasks.md Package Map pkg07 写域（L113）× T048（L264）/ DoD-7（L39）/ GATE-4（L51） | W3-02 的载体修复未传播完：pkg07 写域仍列 `verification.md`，而 T048 实际写、DoD-7/GATE-4 实际查的是 `verification.log`；pkg07 执行者按声明写域无权写真正的闭包载体，同一事实在文件内出现两个名字（冲突声明）。 | /speckit.tasks |

---

## 3. MEDIUM（33 行 open：25 carried-over + 8 new）

| ID | 状态 | 锚点 | 一句话事实 | 建议归属 |
|----|------|------|------------|----------|
| W1-07 | R1-open · deferred | requirements.md:99, :115, :118（FR-005 / FR-008 / Edge Cases） | 钉名 owner 缺席/执行报错或维度不可评估时的降级语义仍未定义；Edge Cases 只有符号链接一例。 | requirements.md（补降级结局，禁止把不可评估当作 clean） |
| W1-08 | R1-open · deferred | requirements.md:131 §FR-015 / :93 Edge Cases | FR-015 仍未定义单批确认的覆盖范围/拒绝粒度，也未定义交互终端下 EOF、空回车、取消的结局。 | requirements.md（补确认交互契约与拒绝语义） |
| W1-09 | R1-open · deferred | requirements.md:131 §FR-015 | 钉名唯一 owner，但未要求从 confirmation-gates 派生/导入并以漂移测试钉住；命令内复制清单仍可通过现有验收。 | requirements.md / plan（补派生方式与漂移断言） |
| W1-10 | R1-open · deferred | requirements.md:116 §FR-006 / :172 §SC-001 | 「零写入/哈希不变/逐项零差异」的比较单元（内容哈希、模式/可执行位、符号链接目标、空目录、权限变更）仍未钉名；SC-001「应用前后文件树哈希对照」措辞与干跑零写入的测量点不一致。 | requirements.md § SC-001 / Measurement Sources |
| W1-12 | R1-open · deferred | requirements.md:117 §FR-007 / :130 §FR-014 | 维度①与④对同一镜像文件仍可能双重命中；归属、去重与处置优先级未定义。 | requirements.md |
| W1-13 | R1-open · deferred | requirements.md:115 §FR-005 / :117 §FR-007 | FR-005 owner 清单仍不含 init 的 `copy_local_templates` / `rewrite_paths` / `generate_commands`；平台资产变体（sh/ps、工具命令目录交集）的选择规则未定义。 | requirements.md（补 owner 或由 plan 钉名并回填） |
| W1-15 | R1-open · deferred | requirements.md:133 §FR-017 / :177 §SC-006 / :92 Edge Cases | 仍只操作化「已归档未写」与「已归档且已写」；写入中、回执未更新及中断后工作区被用户改动的续跑判定未定义。 | requirements.md（补中断点集合与续跑判定） |
| W1-16 | R1-open · deferred | requirements.md:145 §FR-023 / :175 §SC-004 | 七类构成与五维已绑定，但构成类到具名注册表条目/检查器发现的逐项映射、构建时实时派生机制、SC-004 的「类/代」计量单位仍开放。 | requirements.md |
| W1-17 | R1-open · deferred | requirements.md:145 §FR-023 / :174 §SC-003 | 「已最新夹具」的构造基（init 现场投影树还是 migrate 收敛后的树）未定义；以后者构造会使 clean 断言循环取证。 | requirements.md（钉名构造基与独立 oracle） |
| W1-18 | R1-open · deferred | requirements.md:100 Edge Cases / :231 §A6 / :134 §FR-018 | 两写者并发回执测试仍只落在 Edge Cases 与 A6；FR-018 只要求一文一件，无对应 SC/Measurement Source 的可转红断言。 | requirements.md（补可转红断言）；tasks 承接 |
| W1-19 | R1-open · deferred | requirements.md:178 §SC-007 / :126 §FR-013 | SC-007 仍未指名 sanitize 迁移类检查器/动作集合；FR-013 的「静止指针」无字段或固定文本形态。 | requirements.md（钉名检查器集合与指针形态） |
| W1-20 | R1-open · deferred | requirements.md:110 §FR-003 / :135 §FR-019 / :182–192 | FR-003 缺 `.specify/` 的拒绝路径与 FR-019 输入错误退出 2 仍无 SC 或 Measurement Source。 | requirements.md（补 SC 与 measurement source） |
| W1-21 | R1-open · deferred | requirements.md:115 §FR-005 / :175 §SC-004 | 三禁令中仅「按源版本号选择路径」经 SC-004 变异转红；「不读 `.specify/version`」「不按模板指纹猜测」无负向断言。 | requirements.md § SC / tasks（补负向测试） |
| W1-22 | R1-open · deferred | requirements.md:123 §FR-010 / :172 §SC-001 | 「MUST NOT 读写 sanitize 发现台账」仍无 SC/Measurement Source；文件树哈希无法证明未读台账或未触发 `--action collect`。 | requirements.md § SC / tasks |
| W1-23 | R1-open · deferred | requirements.md:153–158 Runtime Stack（Premises 列） | Premises 列引用 EP-001…EP-004，requirements.md 内仍无 Premises 定义或 owner 指针。 | requirements.md（补 Premises 节）或 plan（改为指针） |
| W1-25 | **R2-new** | requirements.md:125 §FR-012 / :178 §SC-007 / checklist:37 CHK015 | FR-012 要求在同一变更内把 sanitize Migration lane 的定位声明收敛为「周期复检兜底」，但 9 条 SC 与 Measurement Sources 都没有该声明的验收面（SC-007 只断言迁移残留零发现与 goal/team 静止指针），round-1 的 `covered-by FR-012` 处置构成循环引用。 | requirements.md（扩 SC-007 或新增 Measurement Source；若定为评审型验收须明示） |
| W1-26 | **R2-new** | requirements.md:130 §FR-014 / :116 §FR-006 | `converged`（已收敛，零写入）被列为差异项的处置结果，但需求未定义差异项在何种情形下零写入即算收敛，也未声明 FR-006 计划中的「拟处置」是否必须取自同一六值集；实现可把未处置差异标为 `converged` 而计划与回执仍自洽。 | requirements.md（clarify：定义 `converged` 触发条件与计划/回执处置词表关系，或从执行性处置集移除该值） |
| W1-27 | **R2-new** | requirements.md:116 §FR-006 / :172 §SC-001 / :182–192 | FR-006 要求同一棵树的重复干跑产出逐项相同的计划，但 9 条 SC 与 Measurement Sources 均无该确定性的验收断言（SC-001 只测干跑零写入与应用后第二次运行 clean），稳定排序无从判红。 | requirements.md（在 SC-001/SC-003 或 Measurement Sources 补「重复干跑逐项一致」断言） |
| W2-02 | R1-open · **R2 复核增补**（原 r2W2-04） | data-model.md:41 E-2 / :55–71 E-3 / migrate-cli.md:62–65 C-4 | 回执 `workspace` 字段三处不一致：E-2 称「回执中记录」、C-4 把 `workspace` 绝对路径列为回执易变字段，E-3 的回执 schema 却无该字段；且 apply 模式下 stdout 包络 `receipt` 字段的内容未规定。 | data-model E-3 / migrate-cli C-4 |
| W2-03 | R1-open · **R2 复核增补**（原 r2W2-06） | data-model.md:59 E-3 / :85, :90 E-4 | E-3 的 `status=aborted` 与 E-4 的 `change=removed-stale` 在六份文件内均无任何触发/指派规则（仅出现在枚举与列举中），实现与回执测试无法判定何时产出这两个值。 | data-model E-3 / E-4 |
| W2-05 | R1-open · **R2 复核增补**（原 r2W2-03） | data-model.md:23 E-1 / :122 E-8 / migrate-engine.md:32 C-3 | `mechanism` 值 `mirror-engine` 在 C-3 的处置映射中从不被指派；同一「锚点搬迁」的机制在 E-8 被钉为 `relocate`、在 C-3 又写成 `relocate / anchor-engine`——机制 token 映射不闭合。 | migrate-engine C-3 / data-model E-8 |
| W2-07 | R1-open · **LOW→MEDIUM 重定级**（原 r2W2-02） | plan.md:151–166 WP 表 / :33 / :200；feature-ref.md:30, :39, :46 | WP 表 14 行合计只指派 23/25 个 FR：FR-004、FR-013 未出现在任何 WP 的 FR 列（feature-ref 矩阵分别记为 WP01、WP03），FR-020 只挂在验收 WP12（feature-ref 记为 WP02/WP06）；与同文件两处「25/25 FR 覆盖」主张之间缺少 WP 级载体。 | plan § Work Packages（或 feature-ref 的 FR→WP 矩阵） |
| W2-14 | **R2-new**（原 r2W2-01） | data-model.md:108 E-6 / :113 E-7 / migrate-engine.md:15 C-2 / :43–50 C-4 | E-6 的 `framework-source` 影响列称「模板/技能/代理参照面对照仍可用（见契约 C-4）」，但 C-4 是客户端参照树规则，E-7 又明确框架源不建参照树、资产期望态由 C-2 的 sync-mirrors 镜像对回答——框架源分支的期望态来源在两处互相抵触。 | data-model E-6 / migrate-engine C-2（统一为 C-2 口径并改正指针） |
| W2-15 | **R2-new**（原 r2W2-05） | migrate-engine.md:80 C-7 / :36 C-3 / data-model.md:26 E-1 / :48 E-2 | C-7 要求把「旧回执 done 且目标已等于期望」的项「记 `converged`」，但 C-3 说 converged 项不进入计划、E-1 的 `status` 枚举无该值，E-1 指向的 E-2 也不含该排除规则——该记录没有可落位的载体。 | migrate-engine C-7 / data-model E-1 |
| W3-04 | R1-open · **R2 复现+扩展** | tasks.md 追溯表（L330–L358）× 行内引用（T005/T034/T038/T039） | 追溯表与行内引用漂移仍在：表列而该行未点名 4 处（FR-002→T039、FR-021→T034、FR-022→T034、FR-025→T039），行点名而未入表 2 处（T034→FR-025、T039→SC-009），仅推断 1 处（FR-007→T005）；本轮另见 SC-009→T038 表列而 T038 文本只点名 FR-021。 | /speckit.tasks |
| W3-05 | R1-open · **R2 复现** | tasks.md 追溯表 SC-007 行（L340）× T015（L171） | SC-007 在任务行文本中 0 次出现，唯一归属为追溯表 L340 指向 T015；Phase Map 的 US1 criteria（L23）只列 SC-001/SC-003；`tasks-validator.txt` 的 "distinct SC cited: 9" 由表行贡献，不是行级覆盖证据。 | /speckit.tasks（在 T015 文本点名 SC-007，或改映射到真实断言行） |
| W3-06 | R1-open · deferred | tasks.md 前置清单（L7）× DoD-9（L41）× T045（L261） | 前置清单声明 quickstart.md 含 scenarios 0–5，DoD-9 与 T045 只执行场景 1–5；场景 0 无执行行、无取证行，也无豁免声明。 | /speckit.tasks |
| W3-07 | R1-open · deferred | T026（L201）/ T027（L202）× T023（L195）× 环境节（L62） | T026 的 `platform-no-symlink` 拒绝分支与 T027 的 `site/`、`.specify/memory/**`、项目扩展保护，仍未进入唯一 US2 测试行 T023 的有界断言清单；环境节称该平台降级 "由模拟行使" 却未指名模拟载体。 | /speckit.tasks（把两类行为写入 T023 或新增测试行，并指名模拟方式） |
| W3-08 | R1-open · deferred | tasks.md FR-004/FR-005/FR-011/FR-012 追溯行 | 四条 FR 仍只映射到实现、文档、镜像行（依次 T016；T010/T011/T018；T019/T020；T041/T042），无任何测试行点名；Tests Mode ON 下其红先测试归属不可见。 | /speckit.tasks（补测试行映射或点名的断言） |
| W3-10 | R1-open · deferred | tasks.md Tests 契约（L11）× pkg02–pkg06 写域（L105–L115） | red-first 读数仍集中写入 `notes/red-first-evidence.md`，但 pkg02–pkg06 写域均未声明该路径；pkg05 与 pkg06 声明可重叠，两个执行者会并发写同一账本，违反「记录类数据一文一件」。 | /speckit.tasks（按条目分文件，或把重叠面串行化并补写域声明） |
| W3-17 | **R2-new** | T023（L195）× DoD-4（L36） | T023 的第四个变异 "weaken the assertion to existence-only" 是测试侧弱化，弱化断言不会让套件转红，与 "four mutations turn the file red" 矛盾；DoD-4 又要求 T028 记录 "四个变异结果"。 | /speckit.tasks（改为实现侧变异——如归档内容失真、仅复制不搬移——并保留四条红读数） |
| W3-18 | **R2-new** | T048（L264）× 仓库 `.gitignore` L37 `*.log` | T048 选定的宪法 VII 载体 `verification.log` 被仓库 `.gitignore` 的 `*.log` 规则忽略（修复处置记录已记该残差），而 T048 行文本未要求负规则、强制纳入或等价受控载体，闭包记录可能在版本库中消失。 | /speckit.tasks（把「载体须受版本控制」写进行文本，与 W3-16 一并收敛） |
| W3-19 | **R2-new** | T035（L242）× T033（L237）/ T034（L238）/ T039（L246） | T035 要求模板 "verbatim restatement" 四类结局与退出码，但三条钉住行都不断言模板内的表：T033 只断言两个字面量与禁用词，T034 比较运行期行为，T039 断言装配形态，模板内的结局表可无守卫漂移（One Source of Truth 的漂移副本风险）。 | /speckit.tasks（T033/T039 增一条「模板结局表与 owner 逐字一致」的断言，或让模板改为引用 `specify migrate --help`） |

---

## 4. LOW（19 行 open：12 carried-over + 7 new）

| ID | 状态 | 锚点 | 一句话事实 | 建议归属 |
|----|------|------|------------|----------|
| W1-24 | R1-open · deferred | requirements.md:108 §FR-001 / :200 STR-003 | 显式 `--dry-run` 与裸默认的等价性、以及 `--dry-run` 与 `--apply` 并用的结局仍未定义（契约 C-1/C-7 已答，需求层未回填）。 | requirements.md / plan（补旗标组合契约） |
| W1-28 | **R2-new** | checklist:6 | checklist 头部机械读数与需求现状不符：requirements.md 实为 236 行 / 36,445 B（清单记 35,235 B，修复轮后未更新），Clarifications 实为 6 + 5 问（清单记 6 + 4 问）。集成者复测 R6 一致。 | checklist（重生成或更正头部读数） |
| W1-29 | **R2-new** | checklist:11 | Detection path 声明三路「作用域不相交」，但同段枚举的 Detector B 与 Detector C 重叠于 FR-024/FR-025 与 SC-003…SC-005，且后文又记录「2 组双检测器重叠合并」，不相交声明与自身枚举矛盾。集成者复测 R10 一致。 | checklist（更正检测路径记录） |
| W2-06 | R1-open · **R2 复现**（原 r2W2-08/09） | data-model.md:119 E-8 / migrate-engine.md:62–65 C-5 | 两处 Markdown 表结构破损：E-8 的表头行与标题写在同一行（L119），C-5 的复用边界表被「链接修复的职责说明」正文（L62）从中截断、后三行落在表外。 | 制品作者修复排版，不改语义 |
| W2-08 | R1-open · **R2 复现**（原 r2W2-10） | plan.md:100, :199；quickstart.md:5 | quickstart 开头称「四段旅程」，页面含场景 0–5 六节，plan L199 按「6 个场景」登记，plan L100 目录树注释仍写「4 个用户旅程场景」；计数口径未声明（哪四段算旅程、0 与 5 为何不计）。 | plan.md / quickstart.md（对齐计数或写明口径） |
| W2-09 | R1-open · 未复现（仍按未修处理） | plan.md:177 EP-006；quickstart.md:68 | EP-006 指向 `contracts/migrate-engine.md`「§ 平台降级」而该契约无此章节；quickstart 场景 4 的「`refuse` 语义如 C-3」未限定文件（两份契约各有一节 C-3）。集成者复测 R10 仍成立。 | plan EP-006 改指 C-3/C-4；quickstart 引用补文件名 |
| W2-10 | R1-open · 未复现（仍按未修处理） | migrate-engine.md:3, :23 | 契约头部 Spec 行声明覆盖 `FR-005…FR-018、FR-023…FR-025`，但正文 C-2 引用 FR-020（不在该区间内），头部枚举与正文引用不一致。集成者复测 R8 仍成立。 | migrate-engine 头部补 FR-020 或复核正文引用 |
| W2-11 | R1-open · 未复现（仍按未修处理） | plan.md:155 WP03；data-model.md:30 E-1 | 去重键不一致：WP03 写「按 target 去重」，E-1 的唯一性规则是 `(dimension, target)` 唯一，两入口若按不同键去重会产生不同计划。集成者复测仍成立。 | plan WP03 对齐 E-1 的键 |
| W2-12 | R1-open · 未复现（仍按未修处理） | data-model.md:139–143；migrate-cli.md:83–86 | 「干跑零写入」「先归档后替换」不变量在 data-model I-1/I-2、cli C-7、plan Constraints 与 quickstart 多处重述且无唯一 owner 声明；I 集合（5 条）与 C-7 集合（4 条）成员不同。 | 声明 data-model 不变量为 owner，C-7 标注为测试投影 |
| W2-13 | R1-open · 未复现（仍按未修处理） | quickstart.md:10–16 | 场景 0 的实测在仓库外 ad-hoc 目录 `~/tmp/speckit-migrate-quickstart` 执行，与临时目录纪律（sanctioned temp root、禁 ad-hoc 目录）不一致。 | quickstart 作者：改用已登记临时根或明确表述为用户自选目录 |
| W2-16 | **R2-new**（原 r2W2-07） | data-model.md:48 E-2 / :86 E-4 | data-model 内两处内部引用不可解析：E-2 写「apply 计划随 E-4 回执固化」（回执是 E-3，E-4 是 ArchiveEntry），E-4 的 `digest` 写「见实现说明」但六份文件无该锚点。 | data-model（改为 E-3 与可解析锚点） |
| W2-17 | **R2-new**（原 r2W2-11） | data-model.md:94–102 E-5；migrate-cli.md:31–39 C-3 | outcome→exitCode 五值封闭表在 E-5 与 C-3 各存一份完整副本，而两处都声明 FR-019 为 owner——按 OSOT 决策测试这是第三份非机器再生的手写副本，改动需同步两文件。 | data-model E-5 / migrate-cli C-3（保留一处、另一处改指针） |
| W2-18 | **R2-new**（原 r2W2-12） | migrate-cli.md:71 C-5 | 交互确认只钉住非 TTY 分支（blocked/exit 3）；「一次单批确认」的接受/拒绝输入协议与提示形态未定义，RED-first 的交互拒绝测试缺少可钉住的输入契约。 | migrate-cli C-5 |
| W2-19 | **R2-new**（原 r2W2-13） | migrate-template.md:7–13 T-1 | T-1 称 frontmatter「只有两个键（与既有命令模板一致）」，但仓内 29 个源命令模板中 23 个带第三键（handoffs/scripts/argument-hint），两键形态只与 sanitize 等 6 个模板一致——理由句与仓内事实不符。集成者复测 R3：29 / 二键 6 / 其余 23。 | migrate-template T-1（改写为「与 sanitize 等两键模板一致」） |
| W2-20 | **R2-new**（原 r2W2-14） | migrate-engine.md:32 C-3 归档列 / :80 C-7 / data-model.md:83–84 E-4 | 搬迁条目的回执字段命名漂移：C-3/C-7 用 from→to 并称搬迁类 `archiveTo` 即 `to`，而 E-4 的 ArchiveEntry 只有 `path` / `archiveTo`，不存在 `to` 字段。 | migrate-engine C-7 / data-model E-4 |
| W3-11 | R1-open · deferred | T004（L134）× § Premises（L98）× Notes（L376） | T004 仍在实现入口对同一 spec 再次 `--freeze`，而 § Premises 已记录生成期冻结（640 names），重跑目的未说明。 | /speckit.tasks |
| W3-12 | R1-open · deferred | T041（L257）/ T043（L259）/ T033（L237） | "its mirror pair see `.specify/...` is synced in T042/T044" 句法仍不成立；T033 存在同型句 "see `tests/contract/test_qoder_command_frontmatter.py`"。 | /speckit.tasks（改写为「镜像副本由 T042/T044 同步」） |
| W3-13 | R1-open · deferred | § Green Partition（L360–L371）× Notes（L376） | 四个未声明条款（cli C-6/C-7、engine C-5/C-8）与 template T-1…T-6 被描述为 "由点名它们的测试行文本钉住"，但 Green Partition 未列出任何钉住行，主张在文件内不可审计。 | /speckit.tasks |
| W3-14 | R1-open · deferred | Notes（L376） | "The contractor's live delta" 使用计量主体之外的生造主体（计数所有者为 clause-coverage accountant）。 | /speckit.tasks |

---

## 5. 跨制品一致性（串联读全 spec）

本节由集成者通读全 spec 目录（requirements → plan → research → data-model → contracts → quickstart → feature-ref → tasks → checklists）后写成；不新增 finding，只把三路读域的结论接成可读的链，并记录只读核对读数。

### 5.1 集成者只读核对（本轮实际执行）

| # | 命令 / 读点 | 读数 | 影响的 finding |
|---|-------------|------|----------------|
| R1 | `python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/097-speckit-migrate-command`（未传 `--freeze`） | exit 1，`status: uncovered`；claimed clauses **11**；scanned files 289；clause universe 2014；`[clause-uncovered]` 644（**4 beyond** the 640-name baseline）；`[fr-uncovered]` 21（**4 of 25 FRs** cited）；`[clause-unparsable]` 108（1 处 parse doubt）；25 error(s) / 1 warning | §6 Coverage；与 tasks § Notes「4/25」披露互证；修复轮未改变该 lane（与 round-1 R1 读数逐项相同） |
| R2 | DoD-1 机械复跑：任务行 `grep -E '^- \[[ xX>~]\] T[0-9]{3} '` → FR token 去重计数；FR 行多重度；`sed '170s/FR-001//'` 变异 | 计数 **25**；单行点名 FR 仅 **FR-004、FR-008**（其余 23 条 ≥2 行）；删 T014 行 FR-001 后仍 **25** | W3-15 机械成立（「任一」红判据不成立） |
| R3 | 命令模板 frontmatter 键数普查（`templates/commands/*.md`，脚本解析） | 29 个模板：**二键 6**（feedback / humanize / improve / measure / sanitize / status）；其余 23（handoffs 20、argument-hint 3、scripts 15 组合） | W2-19（原 r2W2-13）成立 |
| R4 | `.gitignore` 实读 | L37 `*.log` → `verification.log` 被忽略 | W3-18 成立 |
| R5 | `grep -cE '^- \[[ xX>~]\] T[0-9]{3} .*SC-007'` tasks.md | **0** | W3-05 成立 |
| R6 | checklist 头部读数字面 vs `wc -lc` | 清单记 requirements 35,235 B / Clarifications 6+4；实测 236 行 / **36,445 B**、Clarifications **6+5=11 问**；`[Gap]` 实为 16 | W1-28 成立；[Gap] 15→16 更正 |
| R7 | tasks.md pkg07 写域（L113）vs T048（L264）/ DoD-7（L39）/ GATE-4（L51） | pkg07 = `verification.md`；三处闭包载体 = `verification.log` | W3-16 成立 |
| R8 | data-model.md / migrate-engine.md 结构读点 | E-8 标题与表头粘连（L119）；C-5 表被 L62 正文截断（后三行 L63–65 在表外）；C-7 L80 `converged` vs C-3 L36 与 E-1 L26（status 无 converged）；C-2 L23 引用 FR-020；契约头部（L3）区间不含 FR-020 | W2-06（原 r2W2-08/09）、W2-15、W2-10 成立 |
| R9 | feature-ref.md FR→WP 矩阵 vs plan WP 表 | feature-ref：FR-004→WP01、FR-013→WP03、FR-020→WP02/WP06（25/25）；plan WP 表：FR-004/FR-013 缺席、FR-020 仅 WP12（23/25） | W2-07 成立（矩阵与 WP 表漂移） |
| R10 | quickstart / plan 计数注释；checklist detection path | quickstart L5「四段旅程」vs 场景 0–5 六节；plan L100「4 个用户旅程场景」vs L199「6 个场景」；EP-006（plan L177）指向不存在的「§ 平台降级」；quickstart L68「如 C-3」未限定文件；checklist L11 Detector B/C 重叠 FR-024/025、SC-003…SC-005 | W2-08、W2-09、W1-29 成立 |

### 5.2 八条制品链（断点归位）

**链 1 — 期望态来源链**（FR-005 / FR-007 → plan T-001/T-002 → engine C-2 → data-model E-6/E-7/E-8 → tasks T010/T011/T018）
一致事实：引擎装载点（客户端 `get_resource_path()` / 框架源工作区自身 `.specify/scripts/python/`）在 FR-005（requirements.md:115）与 C-2（engine:21）一致；维度 token 顺序由 E-8 唯一拥有、C-1 与 T005 只引用；双工作区 guard 与 `check_legacy_install_residue` 同源（E-6、C-2、T010）。
断点：W1-13（FR-005 owner 清单缺 init 复制机制）、W1-21（两条禁令无负向断言）、W2-14（E-6 的 framework-source 参照面指针与 E-7/C-2 抵触）、W2-05（mechanism token 映射不闭合）、W3-08（FR-005 无测试行点名）。

**链 2 — 处置与结局链**（FR-014 / FR-019 → data-model E-5 + cli C-3/C-4 + engine C-3 → tasks T005/T013/T014/T016/T021）
一致事实：六值处置域由 FR-014 唯一拥有，C-3 逐字映射，I-5 以测试提取比对；四类 outcome 与 `error` 退出类别已显式分离（E-5:100–102、cli C-3:39、C-4:66）；结局聚合规则（requirements.md:135）与 E-5 的 blocked 触发行一致。
断点：W1-26（`converged` 在 FR-014 的触发未定义）、W2-15（`converged` 记录无可落位载体）、W2-03（`aborted` / `removed-stale` 无触发）、W2-17（E-5 与 C-3 双份五值表）。

**链 3 — 回执与续跑链**（FR-017 / FR-018 / FR-020 → data-model E-3/E-4 + engine C-7 → tasks T006/T009/T029/T031/T048）
一致事实：回执落点 `.specify/memory/migrate/receipts/<run-id>.json` 与归档 `.specify/archive/migrate/<run-id>/<rel>` 在 FR-018、E-3、E-4、C-7、T009 一致；干跑回执走输出流（FR-018:134 ↔ E-3:52/76 ↔ C-7:78）；`source.json` 读取与 `unavailable` 回退（FR-020:139 ↔ E-3 source ↔ T030）。
断点：W2-02（`workspace` 字段三处不一致）、W2-16（E-2→E-4 指错、「见实现说明」无锚点）、W2-20（from→to vs `archiveTo`）、W2-03（`aborted`）、W3-10（红先单文件账本）、W3-18（`verification.log` 被 `.gitignore` 忽略）、W3-16（pkg07 载体名冲突）。

**链 4 — 安全与确认链**（FR-015 / FR-016 → cli C-5 + engine C-6 → tasks T023–T027）
一致事实：双键（`--apply` + 交互单批确认）、非交互 blocked、无确认旗标、未确认破坏项零执行在 FR-015、C-5、C-6、T024 一致；破坏性判据与清单以 confirmation-gates 为唯一 owner，不复述。
断点：W1-08 / W1-09（需求层交互语义与派生）、W1-10（零写入比较单元）、W2-18（C-5 交互输入协议未定义）、W3-07（T023 断言清单不含 platform-no-symlink 与保护类）、W3-17（T023 第四变异不转红）。

**链 5 — 验收与夹具链**（FR-023 / FR-024 / FR-025 + SC-001/SC-003 → engine C-8 → tasks T007/T015/T022/T023/T028/T029/T032/T045/T046）
一致事实：C-8 的声明驱动构造（build_latest / build_legacy / build_mixed）与 FR-023 七类构成、SC-001 五维同名对齐；「最新」夹具在建后 dry-run/重跑均 clean 的语义与 C-8 末条一致。
断点：W1-16 / W1-17（映射与构造基）、W1-25（lane 声明无验收面）、W1-27（重复干跑确定性无验收面）、W3-06（场景 0 无执行/取证行）、W3-15（DoD-1 变异不成立）、W3-09（DoD-3 方向与判别力）、W3-19（T035 模板结局表无守卫）。

**链 6 — 分发与装配链**（FR-021 / FR-022 → template T-1…T-6 → tasks T033–T040）
一致事实：四副本再生、`AUTO-GENERATED` 标记、Qoder frontmatter（`short-description` → `description`）、`COMMAND_BASELINE` 29→30、`.specify/templates/commands/` 退役面在 T-4、T036–T039 一致；round-1 R3 已证 `templates/commands/*.md` 现为 29 个。
断点：W2-19（T-1 两键理由句与仓内 29/6/23 事实不符）、W3-04 / W3-05（追溯双轨与 SC-007 未点名）、W3-13（未声明条款的可审计性）。

**链 7 — 宪法载体链**（宪法 VII ↔ tasks sigil / GATE-4 / T048）
一致事实：sigil 行内 `<!-- deferred: reason -->`（tasks.md:77）与宪法 L224 字面一致（W3-01 fixed 复核）；DoD-7 / GATE-4 / T048 载体均为 `verification.log`（宪法 L223；W3-02 fixed 复核）。
断点：W3-16（pkg07 写域仍写 `verification.md`——修复传播未闭合）、W3-18（`verification.log` 被 `.gitignore` `*.log` 忽略）；机制侧残差（`templates/tasks-template.md` 等仍用 `verification.md`）为 accepted upstream observation（修复处置 § 残差），不在本特性内闭合。

**链 8 — checklist 问责链**（checklists/ ↔ findings）
一致事实：39 条全部已处置（23 raised + 16 covered-by，undispositioned 0）；修复轮后 CHK001/002/010/011/012/014/020/025/026/029/032/035/037/038 已由修复后的 requirements 条款覆盖；[Gap] 16 条全部处置（10 raised + 6 covered-by）。
断点：见附录 A 逐条 ledger；Gap 16 条中 10 条由 8 个 open finding 承载（CHK003/021→W1-07；CHK008→W1-08；CHK009→W1-09；CHK023→W1-10；CHK019/022→W1-13；CHK028→W1-15；CHK036→W1-18；CHK015→W1-25），6 条 covered-by 修复后条款（CHK012/020/025/026/037/038）。

### 5.3 跨波主题簇（重叠登记，无字面重复）

| 簇 | 成员 | 议题 |
|----|------|------|
| K1 回执契约与续跑 | W1-15, W1-18, W2-02, W2-03, W2-16, W2-20, W2-15, W3-10, W3-11, W3-18 | 回执字段/状态/续跑/并发账本/载体受控 |
| K2 结局与处置词表 | W1-26, W2-03, W2-15, W2-17, W2-05 | converged 语义、aborted/removed-stale、双份五值表、机制 token |
| K3 期望态来源与归属 | W1-13, W1-21, W2-05, W2-14, W2-07 | owner 清单、框架源分支、mechanism、FR→WP 载体 |
| K4 验收取证判别力 | W1-10, W1-16, W1-17, W1-18, W1-20, W1-21, W1-22, W1-25, W1-27, W3-05, W3-08, W3-09, W3-13, W3-15, W3-17, W3-19 | 可转红断言、比较单元、变异检查、DoD 判别力、模板结局表守卫 |
| K5 宪法与门载体 | W3-16, W3-18 | 宪法 VII 载体名传播、版本控制载体 |
| K6 交叉引用与计数 | W2-06, W2-07, W2-08, W2-09, W2-10, W2-11, W3-04, W3-12, W3-14, W1-28, W1-29 | 引用失效、计数漂移、术语、结构破损 |
| K7 安全与用户保护 | W1-07, W1-08, W1-09, W2-18, W3-07 | 确认交互、降级、保护类断言、输入协议 |
| K8 夹具与场景 | W1-16, W1-17, W3-06, W2-13 | 夹具构造基、场景覆盖、实测目录 |

### 5.4 归属不对称与修复传播（供修复排序）

- requirements 层的多数 MEDIUM（W1-07…W1-23）在设计层已有部分确定性答复（如 W1-15 ↔ C-7 续跑规则、W1-24 ↔ C-1/C-7），但需求层裁定仍缺；修复时应把设计侧答复回收为建议裁定文本。
- **本轮最显著的集成事实：修复轮本身成为新的漂移源**——W3-02 的载体改名只修了三处字面锚点，第四处副本（pkg07 写域）未同步（→W3-16）；W3-03 的修复新增了机械不成立的红判据（→W3-15）。这要求任何后续修复把「同一事实的全部副本」与「新增判据的可执行性实测」作为修复完成判据。

---

## 6. Coverage / Feature / Constitution / Unmapped 摘要

### 6.1 Coverage Summary

| Item | Reading |
|---|---|
| FR / SC / STR | 25（FR-001…FR-025）/ 9（SC-001…SC-009）/ 4（STR-001…STR-004，全部 `[[STR-NNN]]` 引用可解析） |
| User Stories / Edge Cases / Assumptions | 4 / 10 / 11（A1–A11） |
| Clarifications | 2 场，6 + 5 = **11 问**（checklist 头部记 6+4 → W1-28） |
| SC → FR 映射 | 9/9 SC 可回指 FR（W1 读域） |
| FR → task（纸面） | 25/25 均在追溯表有行；任务行 48、无缺号（W3 机械前提） |
| FR → task（行级证据） | 弱于纸面：W3-04（表↔文漂移，本轮扩展 1 处）、W3-05（SC-007 行级 0 次）、W3-08（FR-004/005/011/012 无测试行）、W3-15（DoD-1 计数红判据不成立） |
| clause accountant（R1） | `status: uncovered`（exit 1）；claimed 11；fr-uncovered 21（4/25 cited）；clause-uncovered 644（4 beyond baseline 640）；unparsable 108 |
| 无专属 SC / Measurement Source 的 FR 分支 | W1-20（FR-003 输入错误）、W1-22（FR-010 台账不可变）、W1-25（FR-012 lane 声明）、W1-27（FR-006 重复干跑确定性） |
| 夹具覆盖 | 三类夹具声明驱动构造在 C-8 已具名；requirements 层一致性见 W1-16/W1-17 |

### 6.2 Feature Linkage Summary（G 通道，W1 读域 + 集成者核对）

| 项 | 读数 |
|----|------|
| 绑定 | Feature 024（Specification Workspace Versioning），requirements.md:14–17 与 checklist 头部一致 |
| 索引行 | `.specify/features.md` L33：`Planned`，Spec Path 指向本规格 requirements，Last Updated `2026-11-10 (plan: …)`——状态/路径/日期合规 |
| 详情文件 | `.specify/features/024-specification-workspace-versioning.md`：`Planned`（round-1 R10 核对；本轮修复未触注册表） |
| G 通道结论 | 零 finding；观察（不升级）：索引行叙事仍写 "plan:"，tasks/analyze 工件已存在——下次 registry 触碰时顺带更新 |
| registry 待办 | requirements.md:17 / :218 的待办恢复点已在 plan 阶段关闭（feature-ref 声明），本波核对一致 |

### 6.3 Constitution Alignment Issues

- **无新增 CRITICAL**。round-1 的两条 CRITICAL（W3-01 / W3-02）已按宪法字面（L223 `verification.log`、L224 行内 `<!-- deferred: reason -->`）修复，W3 round-2 复核 fixed；修复的传播残差（W3-16）与载体受控风险（W3-18）按 HIGH/MEDIUM 登记。
- 本轮 3 条 HIGH 均为 DoD/验证门判别力问题（closed-set-claims 处置），非宪法冲突；宪法类不适用 downgrade。
- 机制侧与宪法字面的分叉（上游模板仍用 `verification.md`）维持 accepted upstream observation，不在本特性内稀释（修复处置 § 残差）。
- W1 / W2 读域内的 D 通道零发现：FR-001/FR-022 绑定 XXI；FR-005/007/015 的 owner 声明对齐 XIV；decision tension 校验器 `status: ok`（2 记录，0 标签失败，W2 round-2 机械复核）。

### 6.4 Unmapped Tasks

- 未发现「无任何 FR/SC 锚点」的任务行：48 行均有阶段归属与至少一个 FR/SC 引用或追溯表映射（W3 机械前提）。
- 反向漂移登记：T034、T039 行内点名的 FR/SC 未全部入追溯表；T005 的 FR-007 属推断；SC-009→T038 为本轮新见漂移（W3-04）。

---

## 7. Rerun Delta（Resolved / New / carried-over）

| 类别 | 条目 | 数量 |
|------|------|------|
| **Resolved** | W3-01, W3-02（CRITICAL，复核确认）；W1-01…W1-06、W3-03（HIGH，复核确认）；W2-01, W2-04（HIGH，修复记录 + 间接重测，无显式重裁）；W1-11, W1-14（MEDIUM，incidental fixed 复核确认） | **13** |
| **Carried-over open** | W1-07…W1-23 中 15 MEDIUM + W1-24 LOW；W2-02, W2-03, W2-05, W2-07（重定级 M）+ W2-06, W2-08…W2-13 LOW；W3-04…W3-08, W3-10 MEDIUM + W3-09（升格 H）+ W3-11…W3-14 LOW | **38**（H 1 · M 25 · L 12） |
| **New** | W1-25, W1-26, W1-27, W2-14, W2-15, W3-17, W3-18, W3-19（MEDIUM）；W1-28, W1-29, W2-16…W2-20（LOW）；W3-15, W3-16（HIGH） | **17**（H 2 · M 8 · L 7） |
| **当前开放账本** | 13 resolved + 38 carried + 17 new = 68 状态项；51（round-1）+ 17（new）− 13（resolved）= **55 open**（H 3 · M 33 · L 19） | 55 |

补充披露：
- **W2 跨轮次 id 归一化**：round-2 W2 的 14 行原始 id 与 round-1 W2-01…W2-13 数字碰撞；其中 7 行为 round-1 残差的**再观测**（按内容归并为指针：原 r2W2-02/03/04/06/08/09/10 → W2-07/W2-05/W2-02/W2-03/W2-06/W2-06/W2-08），6 行为新内容（顺延重编号），1 行（原 r2W2-14）顺延重编号；映射见 §10。W1 与 W3 的 id 在 round-1/round-2 间保持稳定（W1-01…W1-24、W3-01…W3-14 语义不变）。
- **H 计数更正**：round-1 `[Gap] 15` → 本轮机械重数 `16`（计数错误更正，不是新 finding）。
- **严重度重定级**：W3-09 MEDIUM→HIGH；W2-07 LOW→MEDIUM（round-2 传播面评估）。

---

## 8. Metrics

| 指标 | 读数 |
|------|------|
| 输入波次 | W1 29 行（复核 6 + 新 5 + 残差 18）· W2 14 行（新 14）· W3 19 行（复核 4 + 残差 10 + 新 5）〔CRITICAL/HIGH/MEDIUM/LOW 按各波自报〕 |
| 归并后开放账本 | **55** 行：HIGH **3** · MEDIUM **33** · LOW **19** · CRITICAL 0 |
| Resolved（本轮） | 13（2C · 9H · 2M） |
| New（本轮） | 17（0C · 2H · 8M · 7L） |
| 重复 id（round-2 输入集内） | 0（脚本机械核对：62 行 · 62 unique） |
| 跨轮次 id 碰撞归一 | 13 数字碰撞 → 7 指针 + 6 重编号；另 1 行顺延重编号；合计重编号 7（W2-14…W2-20） |
| C/H 待独立验证 | **3**（HIGH：W3-09、W3-15、W3-16）；验证波完成前不构成 gate 通过证据 |
| H 问责 | unchecked 39 / dispositioned 39 / undispositioned 0；[Gap] 16：raised 10 / covered-by 6 / undispositioned 0 |
| clause accountant（R1） | `status: uncovered`（exit 1）；claimed 11；fr-uncovered 21（4/25）；clause-uncovered 644（4 beyond baseline 640）；unparsable 108 |
| decision tension（W2 机械复核） | `status: ok`，2 记录，6 类标签 0 失败 |
| FR→task | 纸面 25/25；行级证据缺口见 §6.1 |
| 相对单通道 50 行上限的溢出 | 5 行（4 LOW + 1 MEDIUM）；按确定性归并指令保留于正文，此处显式记账 |
| Rerun delta | Resolved 13 / carried-over 38 / New 17；账本 55 open |

---

## 9. Systemic Observations（聚合，不提升任何单行严重度）

- **S-1 修复传播不闭合（本轮首要观察）**：W3-02→W3-16（同一载体事实的第四处副本未同步）与 W3-03→W3-15（修复新增判据机械不成立）表明「修复只改字面锚点」会制造新漂移。建议后续修复以「同一事实全部副本」清单 + 新增判据的可执行性实测作为完成判据。
- **S-2 DoD 判别力**：W3-15、W3-09、W3-17 同属「声称会转红但机制上不会」；DoD-1/3/4 的变异子句需逐条保留实测读数。
- **S-3 覆盖证据双轨**：W3-04 / W3-05 / W3-08 + W1-25 / W1-27——追溯表、行内文本与 SC/Measurement Sources 三处不成闭环；SC-007 行级覆盖为 0。
- **S-4 封闭词表多处漂移**：结局表双份手写副本（W2-17）、`converged` 无载体（W2-15）、机制 token 不闭合（W2-05）、`aborted` / `removed-stale` 无触发（W2-03）。
- **S-5 回执与指针卫生**：W2-02 / W2-16 / W2-20 合计指向 `workspace` 字段、E-2→E-4 引用与 from→to 命名的三处不可解析/不一致。
- **S-6 结构损伤簇（修复后遗留）**：E-8 表头粘连与 C-5 表体截断（W2-06，早期 LOW 未被修复轮触及）；建议修复流程增加 Markdown 结构校验。
- **S-7 单文件账本并发**：W3-10 的 red-first 单文件与「记录类数据一文一件」冲突，影响 implement 并行派发设计。
- **S-8 机制侧与宪法字面残差**：W3-18（`.gitignore *.log` 吞掉 `verification.log`）与上游模板的 `verification.md` 分叉；前者随 tasks 修复可闭，后者为 accepted upstream observation。

---

## 10. 归并日志（确定性核对）

- **分节**：HIGH（3）/ MEDIUM（33）/ LOW（19）；节内按 ID 字典序（`W1-<W2-<W3-`，同波数字序）核对成立。
- **round-2 输入集重复 id**：脚本解析三份输入的表格行（`^| W[0-9]-NN |`）→ 62 行、62 unique、跨文件重复 0；无同轮指针替代行。
- **跨轮次重复 id（W2）**：round-2 W2 从 W2-01 重新编号，与 round-1 W2-01…W2-13 数字碰撞。按「先声明先得」：round-1 id 保留语义；round-2 行按内容裁定后归一：

| round-2 W2 原始 id | 内容匹配 round-1？ | 归并结果 |
|---|---|---|
| W2-01 | 否（E-6 framework-source 来源抵触） | 新 id **W2-14** |
| W2-02 | 是（↔ R1 W2-07 WP 覆盖；并升格 MEDIUM） | 指针 → **W2-07** |
| W2-03 | 是（↔ R1 W2-05 mirror-engine） | 指针 → **W2-05** |
| W2-04 | 是（↔ R1 W2-02 workspace 字段） | 指针 → **W2-02** |
| W2-05 | 否（converged 无载体） | 新 id **W2-15** |
| W2-06 | 是（↔ R1 W2-03 aborted；补 removed-stale） | 指针 → **W2-03** |
| W2-07 | 否（E-2→E-4 引用、digest 锚点） | 新 id **W2-16** |
| W2-08 | 是（↔ R1 W2-06 前半 E-8 表头） | 指针 → **W2-06** |
| W2-09 | 是（↔ R1 W2-06 后半 C-5 表体） | 指针 → **W2-06** |
| W2-10 | 是（↔ R1 W2-08 4 vs 6 场景） | 指针 → **W2-08** |
| W2-11 | 否（outcome 表双份副本） | 新 id **W2-17** |
| W2-12 | 否（C-5 交互输入协议） | 新 id **W2-18** |
| W2-13 | 否（T-1 两键理由句） | 新 id **W2-19** |
| W2-14 | 否（from→to vs archiveTo） | 新 id **W2-20** |

- **逐行保真**：新行照抄 worker 的「一句话事实 / 建议归属」；指针归并行的 round-2 增补内容已并入目标行（标注「R2 复核增补 / R2 复现」）；W1/W3 残差行沿用其 round-2 报告的复现事实。
- **C/H 不重裁**：本文件对所有 C/H 只做汇总、指针与状态登记，不裁定 confirm/downgrade/reject——该裁定归独立验证波。
- **只读证据**：R1–R10 均为只读命令/读点；accountant 未传 `--freeze`；未修改任何制品。
- **未做事项（明示）**：C/H 独立验证波（驱动后续派发）；任何修复（本阶段禁止）。

---

## 11. Wrap-up 记账

- **单元**：analyze wave 集成（unit: `skill:analyze-artifacts`@097，round 2）。
- **输入**：三份 round-2 worker 报告（29 / 14 / 19 行）+ 本特性 spec 全目录（requirements 236 行 / 36,445 B；plan 202 行；tasks 48 任务行；6 份设计制品）。
- **产物**：本文件（唯一 spec 面写点）；未修改任何 spec 制品。
- **引擎记录**：Run Determination / Exec Quant / Feedback Record 三步已按 `## Wrap-up` 执行；三引擎均返回 `duplicate`（同一 `skill:analyze-artifacts × r20261110T081104Z-b097` 已由 round-1 记录），按驱动契约「duplicate 的跳过同样计入满足」计为已记账，无新记录文件；round-1 的既有记录即本 run 的权威记账。
- **验证**：新增/升格 C/H = 3（均 HIGH）；不自我验证，交由驱动侧独立验证波。
- **异常**：无异常；无即修（nothing to report is something to say）。
- **上游偏差**：`checkpoints/01-requirements.md`、`02-clarify.md` 仍为前序阶段未提交文件，本阶段不代提交、不还原（沿用 round-1 记录）。

---

## 附录 A — Checklist H 逐条 disposition ledger（源 W1 round-2，逐字保留）

`unchecked=39; dispositioned=39; undispositioned=0; [Gap] subset: unchecked=16, raised=10, covered-by=6, undispositioned=0`

```
CHK001 disposition: covered-by requirements.md § FR-005
CHK002 disposition: covered-by requirements.md § FR-005
CHK003 disposition: raised-as-finding W1-07
CHK004 disposition: raised-as-finding W1-21
CHK005 disposition: raised-as-finding W1-12
CHK006 disposition: raised-as-finding W1-24
CHK007 disposition: raised-as-finding W1-08
CHK008 disposition: raised-as-finding W1-08
CHK009 disposition: raised-as-finding W1-09
CHK010 disposition: covered-by requirements.md § FR-019
CHK011 disposition: covered-by requirements.md § FR-019
CHK012 disposition: covered-by requirements.md § FR-019
CHK013 disposition: raised-as-finding W1-10
CHK014 disposition: covered-by requirements.md § FR-018
CHK015 disposition: raised-as-finding W1-25
CHK016 disposition: covered-by requirements.md § SC-007
CHK017 disposition: raised-as-finding W1-19
CHK018 disposition: raised-as-finding W1-10
CHK019 disposition: raised-as-finding W1-13
CHK020 disposition: covered-by requirements.md § FR-005
CHK021 disposition: raised-as-finding W1-07
CHK022 disposition: raised-as-finding W1-13
CHK023 disposition: raised-as-finding W1-10
CHK024 disposition: covered-by requirements.md § SC-001
CHK025 disposition: covered-by requirements.md § FR-020
CHK026 disposition: covered-by requirements.md § FR-018
CHK027 disposition: raised-as-finding W1-15
CHK028 disposition: raised-as-finding W1-15
CHK029 disposition: covered-by requirements.md § FR-016, § FR-017
CHK030 disposition: raised-as-finding W1-16
CHK031 disposition: raised-as-finding W1-16
CHK032 disposition: covered-by requirements.md § FR-023
CHK033 disposition: raised-as-finding W1-17
CHK034 disposition: raised-as-finding W1-16
CHK035 disposition: covered-by requirements.md § Measurement Sources & Collection Methods
CHK036 disposition: raised-as-finding W1-18
CHK037 disposition: covered-by requirements.md § FR-002, § FR-025
CHK038 disposition: covered-by requirements.md § FR-022, § SC-009
CHK039 disposition: raised-as-finding W1-19
```
