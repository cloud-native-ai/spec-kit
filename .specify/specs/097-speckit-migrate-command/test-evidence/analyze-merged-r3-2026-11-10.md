# Analyze — Merged Findings Report, Round 3（097-speckit-migrate-command）

**Stage**: analyze · Round 3（r3 修复轮之后的全 spec 重过门；单 Worker 串行，`requested=24 / effective=1 / reason=budget-reserve`）· **Date**: 2026-11-10
**Inputs（只读）**: 本特性 spec 全目录（requirements 236 行 / plan 202 行 / tasks 380 行 / data-model 143 行 / 3 契约 / research / quickstart / feature-ref / 2 checklists）+ `.specify/constitution.md`（v1.19.0）+ 冻结基线 `coverage-baseline.txt`（640 names）+ 前两轮合并账本（`analyze-merged-2026-11-10.md`、`analyze-merged-round2-2026-11-10.md`）+ r3 修复面（`tasks.md` L33/L35/L113/L154/L264、根 `.gitignore` L37–39）。
**Authority**: `.specify/skills/internal/analyze-artifacts/` 契约 + `.specify/shared/workflow/objective-analysis-gate.md` + `.specify/shared/guidelines/closed-set-claims.md`。
**Method**: 检测 = 本轮单 Worker 全量通读 + 对 r3 修复面逐项机械复测；验证 = 契约 §5.5 独立只读验证波，**3 个外部子进程**（recipe 7 形态，`--tools Read Grep Glob Bash --no-session-persistence`），3 条 closure 全部 `confirm`（downgrade 0 / reject 0）。**Read-only**: 本波未修改任何 spec 制品；产物仅本文件与 `analyze-gates-r3-2026-11-10.txt`（+ Wrap-up 记账引擎记录）。
**Gate 判定**: **PASS** —— **open CRITICAL 0 / open HIGH 0**（4 条 r3 修复项经独立验证 `validated`）；open MEDIUM 32 / LOW 19 按契约不阻断门。

---

## 0. 计数与指针（顶部汇总，不修复）

| 量 | 读数 | 指针 |
|----|------|------|
| open CRITICAL | **0** | §1；round-1 两条 CRITICAL 已于 R2 复核 fixed，本轮重读无回归 |
| open HIGH | **0** | §1；W3-09 / W3-15 / W3-16 本轮复核 fixed 且 validated |
| C/H 复核锚点 | **validated 4 / proposed 0** | §0.1 表 |
| open MEDIUM | **32**（全部 carried-over） | §2 |
| open LOW | **19**（全部 carried-over） | §3 |
| 本轮 New findings | **0** | §6 |
| 本轮 Resolved | **4**（W3-09 H / W3-15 H / W3-16 H / W3-18 M） | §6 |
| 验证波 | 3 dispatched / 3 confirm / 0 downgrade / 0 reject | §9 |
| H 问责 | unchecked 39 / dispositioned 39 / undispositioned **0**；[Gap] 16 = raised 10 + covered-by 6 | 附录 A |
| clause accountant | `status: uncovered`（exit 1）；claimed 11；clause-uncovered 644（4 beyond 640）；fr-uncovered 21（4/25）；25 error / 1 warning | §5.1 |

### 0.1 r3 修复面复裁（C/H 复核锚点标 validated/proposed）

| ID | 原严重度 | 本轮复核裁定 | 锚点标记 | 修复后锚点（实测） | 验证来源 |
|----|----------|--------------|----------|--------------------|----------|
| W3-09 | HIGH | **fixed** | `validated` | `tasks.md:35`（DoD-3）、`tasks.md:154`（T013） | 独立验证 confirm：五类守卫「真实源判 clean + 合成第二实现判违例」双向断言、方向正确、Check 同次套件执行；五类 token 机械计数各 1 |
| W3-15 | HIGH | **fixed** | `validated` | `tasks.md:33`（DoD-1） | 独立验证 confirm：按 FR 的红判据成立——基线 25/48 行；单点 FR-004@175、FR-008@171 删除后各 24；FR-001 双删（170+175）24、单删 25（预期不判红）；全部读数复现 |
| W3-16 | HIGH | **fixed** | `validated` | `tasks.md:113`（pkg07 写域）、`:39` DoD-7、`:51` GATE-4、`:264` T048 | 独立验证 confirm：四处载体均为 `verification.log`；`grep -c 'verification\.md' tasks.md` = **0** |
| W3-18 | MEDIUM | **fixed** | `validated` | `.gitignore:37` `*.log` → `:39` `!.specify/specs/*/verification.log`；`tasks.md:264` T048 | 独立验证 confirm：`git check-ignore -q <carrier>` **exit 1**（不再被忽略）；`-v` 命中负规则行 |

**验证边界（照录，不静默扩大）**：
- W3-09：测试文件本体尚不存在（T013 未执行），「五 callable 已实现且曾转绿」本轮不可观察；Check 仍只运行套件——其判别力由**测试内变异断言**承载（DoD-3 原文已明示），属口径澄清而非主张缩水。
- W3-15：未逐一运行其余 22 个 FR 的删除变异（构造论证 + 3 个抽样已复现全部记录读数）；`sed` 单行替换只删首现，样本每行至多一次。
- W3-16：一致性核验限 `tasks.md` 内（`requirements/plan/acceptance-hardening` 不在验证读域）；0 命中为大小写敏感字面量。
- W3-18：`verification.log` 当前尚不存在且未被跟踪——实测证明的是规则对真实路径的**忽略判定**，不是「已有闭包制品受控」。

**round-1 C/H（11 = CRITICAL 2 + HIGH 9）**：R2 已复核 fixed（W2-01/W2-04 为修复记录 + 间接重测）；本轮全量重读 `requirements/plan/data-model/contracts`（r3 未触碰这些文件）与 `tasks.md` 相关行，**无回归**，不重开、不重标 validated（其 closed 状态来自 R2 记录）。

---

## 1. HIGH（0 行 open）

- **开放 HIGH = 0**。round-2 遗留的 3 条 HIGH（W3-09 升格、W3-15 新增、W3-16 新增）经 r3 修复后，本轮复核全部 `fixed`，且经 §9 独立验证波 `confirm`；锚点与边界见 §0.1。
- **本轮 New HIGH = 0**：八通道（A duplication / B ambiguity / C underspecification / D constitution / E coverage / F inconsistency / G feature / I decision-tension）+ H checklist 通道全量重跑，未产出新 HIGH。
- 依驱动门判据（`dispatch-recipes.md` § 质量门编排：analyze 门 = 报告 C/H 为零或已处置），**本报告构成 analyze gate 通过证据**。

---

## 2. MEDIUM（32 行 open，全部 carried-over，字典序）

| ID | 状态 | 锚点 | 一句话事实（R2 记录，R3 重读仍成立） | 建议归属 |
|----|------|------|----------------------------------------|----------|
| W1-07 | carried-over | requirements.md:99, :115, :118（FR-005/FR-008/Edge Cases） | owner 缺席/执行报错或维度不可评估时的降级语义仍未定义；Edge Cases 只有符号链接一例。 | requirements.md |
| W1-08 | carried-over | requirements.md:131 §FR-015 / :93 | 单批确认的覆盖范围/拒绝粒度、交互终端 EOF/空回车/取消的结局未定义。 | requirements.md |
| W1-09 | carried-over | requirements.md:131 §FR-015 | 确认门清单未要求从 confirmation-gates 派生并以漂移测试钉住。 | requirements.md / plan |
| W1-10 | carried-over | requirements.md:116 §FR-006 / :172 §SC-001 | 「零写入/哈希不变/逐项零差异」比较单元未钉名；SC-001 措辞与干跑零写入测量点不一致。 | requirements.md |
| W1-12 | carried-over | requirements.md:117 §FR-007 / :130 §FR-014 | 维度①与④对同一镜像文件可能双重命中；归属/去重/优先级未定义。 | requirements.md |
| W1-13 | carried-over | requirements.md:115 §FR-005 / :117 §FR-007 | FR-005 owner 清单缺 init 的 `copy_local_templates`/`rewrite_paths`/`generate_commands` 与平台变体选择规则。 | requirements.md |
| W1-15 | carried-over | requirements.md:133 §FR-017 / :177 §SC-006 / :92 | 中断点集合（写入中、回执未更新、续跑前工作区被改）与续跑判定未定义。 | requirements.md |
| W1-16 | carried-over | requirements.md:145 §FR-023 / :175 §SC-004 | 七类构成到具名注册表/检查器的逐项映射、构建时派生机制、SC-004 计量单位仍开放。 | requirements.md |
| W1-17 | carried-over | requirements.md:145 §FR-023 / :174 §SC-003 | 「已最新夹具」构造基（init 投影树 vs migrate 收敛树）未定义；后者会循环取证。 | requirements.md |
| W1-18 | carried-over | requirements.md:100 / :231 §A6 / :134 §FR-018 | 两写者并发回执测试只在 Edge Cases 与 A6，无对应 SC/Measurement Source 的可转红断言。 | requirements.md；tasks 承接 |
| W1-19 | carried-over | requirements.md:178 §SC-007 / :126 §FR-013 | SC-007 未指名 sanitize 迁移类检查器/动作集合；静止指针无字段或固定文本形态。 | requirements.md |
| W1-20 | carried-over | requirements.md:110 §FR-003 / :135 §FR-019 / :182–192 | FR-003 缺 `.specify/` 拒绝路径与 FR-019 输入错误退出 2 仍无 SC/Measurement Source。 | requirements.md |
| W1-21 | carried-over | requirements.md:115 §FR-005 / :175 §SC-004 | 三禁令中仅「按源版本号选择路径」经 SC-004 变异转红；「不读 `.specify/version`」「不按指纹猜」无负向断言。 | requirements.md §SC / tasks |
| W1-22 | carried-over | requirements.md:123 §FR-010 / :172 §SC-001 | 「MUST NOT 读写 sanitize 发现台账」无 SC/Measurement Source；树哈希证明不了未读台账。 | requirements.md §SC / tasks |
| W1-23 | carried-over | requirements.md:153–158 Runtime Stack（Premises 列） | Premises 列引用 EP-001…EP-004，requirements.md 内无 Premises 定义或 owner 指针。 | requirements.md / plan |
| W1-25 | carried-over | requirements.md:125 §FR-012 / :178 §SC-007 / checklist:37 CHK015 | FR-012 的 lane 定位声明收敛无 SC 验收面；round-1 的 covered-by FR-012 构成循环引用。 | requirements.md |
| W1-26 | carried-over | requirements.md:130 §FR-014 / :116 §FR-006 | `converged` 作为差异项处置结果的触发条件未定义；实现可把未处置差异标 `converged`。 | requirements.md |
| W1-27 | carried-over | requirements.md:116 §FR-006 / :172 §SC-001 / :182–192 | 「重复干跑逐项相同」的确定性无验收断言（SC-001 只测零写入与二次 clean）。 | requirements.md |
| W2-02 | carried-over | data-model.md:41 E-2 / :55–71 E-3 / migrate-cli.md:62–65 C-4 | 回执 `workspace` 字段三处不一致：E-2 称记录、C-4 列为易变字段、E-3 schema 无该字段。 | data-model E-3 / migrate-cli C-4 |
| W2-03 | carried-over | data-model.md:59 E-3 / :85, :90 E-4 | `status=aborted` 与 `change=removed-stale` 无任何触发/指派规则。 | data-model E-3/E-4 |
| W2-05 | carried-over | data-model.md:23 E-1 / :122 E-8 / migrate-engine.md:32 C-3 | `mechanism=mirror-engine` 从不被指派；锚点搬迁机制在 E-8 为 `relocate`、C-3 写 `relocate / anchor-engine`，token 映射不闭合。 | migrate-engine C-3 / data-model E-8 |
| W2-07 | carried-over | plan.md:151–166 WP 表 / :33 / :200；feature-ref.md:30, :39, :46 | WP 表 14 行合计只指派 23/25 个 FR（FR-004、FR-013 缺席；FR-020 仅 WP12），与两处「25/25」主张缺 WP 级载体。 | plan §Work Packages |
| W2-14 | carried-over | data-model.md:108 E-6 / :113 E-7 / migrate-engine.md:15 C-2 / :43–50 C-4 | E-6 的 framework-source 影响列指向客户端规则 C-4，与 E-7/C-2「框架源不建参照树」抵触。 | data-model E-6 / migrate-engine C-2 |
| W2-15 | carried-over | migrate-engine.md:80 C-7 / :36 C-3 / data-model.md:26 E-1 / :48 E-2 | C-7 要求把「旧回执 done 且目标已等于期望」记 `converged`，但 C-3 说 converged 不入计划、E-1 无该值、E-2 无排除规则——无载体。 | migrate-engine C-7 / data-model E-1 |
| W3-04 | carried-over | tasks.md:330–358 追溯表 × 行内引用（T005/T034/T038/T039） | 表↔文双轨漂移：表列行未点名 4 处、行点名未入表 2 处（T034→FR-025、T039→SC-009）、推断 1 处、SC-009→T038 表列而 T038 只点名 FR-021。 | /speckit.tasks |
| W3-05 | carried-over | tasks.md:340 SC-007 行 × T015（L171） | SC-007 在任务行文本 0 次出现，唯一归属为追溯表；`tasks-validator` 的 9 SC 由表行贡献，非行级证据。 | /speckit.tasks |
| W3-06 | carried-over | tasks.md:7 前置清单 × DoD-9（L41）× T045（L261） | quickstart 场景 0 无执行行、无取证行、无豁免声明（T045/DoD-9 只覆盖 1–5）。 | /speckit.tasks |
| W3-07 | carried-over | T026（L201）/T027（L202）× T023（L195）× 环境节（L62） | `platform-no-symlink` 拒绝分支与 `site/`、`.specify/memory/**`、项目扩展保护未进 T023 断言清单；模拟载体未指名。 | /speckit.tasks |
| W3-08 | carried-over | tasks.md FR-004/FR-005/FR-011/FR-012 追溯行 | 四条 FR 无任何测试行点名（仅实现/文档/镜像行），Tests Mode ON 下红先归属不可见。 | /speckit.tasks |
| W3-10 | carried-over | tasks.md:11 Tests 契约 × pkg02–pkg06 写域（L108–L112） | red-first 读数集中写 `notes/red-first-evidence.md`，pkg02–pkg06 写域未声明该路径；pkg05/pkg06 可重叠并发写同一账本。 | /speckit.tasks |
| W3-17 | carried-over | T023（L195）× DoD-4（L36） | 第四个变异「weaken the assertion to existence-only」是测试侧弱化，不会转红，与「four mutations turn the file red」矛盾。 | /speckit.tasks |
| W3-19 | carried-over | T035（L242）× T033（L237）/T034（L238）/T039（L246） | T035 要求模板 verbatim 转述四类结局与退出码，但三条钉住行都不断言模板内结局表，可无守卫漂移。 | /speckit.tasks |

---

## 3. LOW（19 行 open，全部 carried-over，字典序）

| ID | 状态 | 锚点 | 一句话事实（R2 记录，R3 重读仍成立） | 建议归属 |
|----|------|------|----------------------------------------|----------|
| W1-24 | carried-over | requirements.md:108 §FR-001 / :200 STR-003 | 显式 `--dry-run` 与裸默认的等价性、`--dry-run`+`--apply` 并用的结局在需求层未回填（契约 C-1/C-7 已答）。 | requirements.md / plan |
| W1-28 | carried-over | checklist:6 | 头部机械读数与需求现状不符：requirements 实为 236 行 / **36,445 B**（清单记 35,235 B）、Clarifications 实为 **6+5**（清单记 6+4）；同类新增读数——tasks.md 实为 380 行 / **53,050 B**（清单记 51,508 B）。 | checklist（重生成或更正） |
| W1-29 | carried-over | checklist:11 | Detection path 声明三路「作用域不相交」，但 Detector B/C 重叠于 FR-024/025、SC-003…005，且同段记录「2 组双检测器重叠合并」，自相矛盾。 | checklist |
| W2-06 | carried-over | data-model.md:119 E-8 / migrate-engine.md:62–65 C-5 | 两处 Markdown 表结构破损：E-8 标题与表头同行；C-5 表被 L62 正文截断、后三行落表外。 | 制品作者修复排版 |
| W2-08 | carried-over | plan.md:100, :199；quickstart.md:5 | 「四段旅程」vs 场景 0–5 六节；plan L199 登记 6 个场景、L100 注释写 4 个，计数口径未声明。 | plan / quickstart |
| W2-09 | carried-over | plan.md:177 EP-006；quickstart.md:68 | EP-006 指向 `migrate-engine.md`「§ 平台降级」而该契约无此章节；quickstart「如 C-3」未限定文件。 | plan EP-006；quickstart |
| W2-10 | carried-over | migrate-engine.md:3, :23 | 契约头部 FR 区间 `FR-005…FR-018、FR-023…FR-025` 不含 FR-020，正文 C-2 禁止行引用 FR-020。 | migrate-engine 头部 |
| W2-11 | carried-over | plan.md:155 WP03；data-model.md:30 E-1 | 去重键不一致：WP03「按 target 去重」vs E-1 `(dimension, target)` 唯一。 | plan WP03 |
| W2-12 | carried-over | data-model.md:139–143；migrate-cli.md:83–86 | 干跑零写入/先归档后替换不变量多处重述且无唯一 owner 声明；I 集合（5）与 C-7 集合（4）成员不同。 | data-model 声明 owner |
| W2-13 | carried-over | quickstart.md:10–16 | 场景 0 实测在仓库外 ad-hoc 目录 `~/tmp/speckit-migrate-quickstart` 执行，与临时目录纪律不一致。 | quickstart 作者 |
| W2-16 | carried-over | data-model.md:48 E-2 / :86 E-4 | E-2 写「apply 计划随 E-4 回执固化」（回执是 E-3）；E-4 `digest` 写「见实现说明」而六份文件无该锚点。 | data-model |
| W2-17 | carried-over | data-model.md:94–102 E-5；migrate-cli.md:31–39 C-3 | outcome→exitCode 五值封闭表在 E-5 与 C-3 各存一份完整手写副本（双处声明 FR-019 为 owner），改动需同步两文件。 | E-5 / C-3 保留一处 |
| W2-18 | carried-over | migrate-cli.md:71 C-5 | 交互确认只钉非 TTY 分支；「一次单批确认」的接受/拒绝输入协议与提示形态未定义。 | migrate-cli C-5 |
| W2-19 | carried-over | migrate-template.md:7–13 T-1 | T-1 称 frontmatter「只有两个键（与既有命令模板一致）」，但仓内 29 个源模板中 23 个带第三键（二键仅 6 个）。 | migrate-template T-1 |
| W2-20 | carried-over | migrate-engine.md:32 C-3 / :80 C-7 / data-model.md:83–84 E-4 | 搬迁条目命名漂移：C-3/C-7 用 from→to 并称搬迁类 `archiveTo` 即 `to`，E-4 ArchiveEntry 只有 `path`/`archiveTo`，无 `to` 字段。 | migrate-engine C-7 / data-model E-4 |
| W3-11 | carried-over | T004（L134）× §Premises（L98）× Notes（L376） | T004 在实现入口对同一 spec 再次 `--freeze`，与生成期冻结（640 names）目的未说明。 | /speckit.tasks |
| W3-12 | carried-over | T041（L257）/T043（L259）/T033（L237） | "its mirror pair see `.specify/...` is synced in T042/T044" 句法不成立；T033 同型句。 | /speckit.tasks |
| W3-13 | carried-over | §Green Partition（L360–L371）× Notes（L376） | 未声明条款与 T-1…T-6 被描述为「由点名它们的测试行文本钉住」，但 Green Partition 未列出任何钉住行；**R3 增补**：C-5 的锚点布局结构守卫（「无布局判定/移动实现」）不在 T013 五类守卫内，该条款的钉住主张连近似载体都缺。 | /speckit.tasks |
| W3-14 | carried-over | Notes（L376） | "The contractor's live delta" 使用计量主体之外的生造主体（计数所有者为 clause-coverage accountant）。 | /speckit.tasks |

---

## 4. 跨制品一致性（串联读全 spec）

### 4.1 r3 修复面复裁读数（本轮实测，2026-11-10）

| # | 读点 | 读数 | 结论 |
|---|------|------|------|
| R11 | DoD-1 基线：任务行 / FR 去重 | **48 / 25**；单点 FR 恰为 FR-004、FR-008（其余 23 条 ≥2 行） | 与 DoD-1 文本一致 |
| R12 | DoD-1 变异：`sed '175s/FR-004//'` / `sed '171s/FR-008//'` / FR-001 双删 / 单删 | **24 / 24 / 24 / 25** | 红判据机械成立（W3-15 fixed） |
| R13 | DoD-3 五类守卫 token（`no second …`） | path-rewrite regex / command renderer / link roster / mirror-pair roster / obsolete roster 各 **1** | 五类齐全、方向已正（W3-09 fixed） |
| R14 | 载体名残留：`grep -c 'verification\.md' tasks.md` | **0**；pkg07(L113）/DoD-7(L39）/GATE-4(L51）/T048(L264）四处均为 `verification.log` | W3-16 fixed |
| R15 | `.gitignore` L37 `*.log` + L39 `!` 负规则；`git check-ignore -q <carrier>` | `-v` 命中负规则行；**exit 1**（不被忽略） | W3-18 fixed |

### 4.2 八条制品链（断点归位；R2 → R3）

**链 1 — 期望态来源链**（FR-005/FR-007 → plan T-001/T-002 → engine C-2 → E-6/E-7/E-8 → T010/T011/T018）
一致：装载点、维度 token、双工作区 guard 同源不变。断点：W1-13、W1-21、W2-14、W2-05、W3-08（carried）。

**链 2 — 处置与结局链**（FR-014/FR-019 → E-5 + cli C-3/C-4 + engine C-3 → T005/T013/T014/T016/T021）
一致：六值域由 FR-014 拥有、四类结局与 error 分离。断点：W1-26、W2-15、W2-03、W2-17（carried）。

**链 3 — 回执与续跑链**（FR-017/FR-018/FR-020 → E-3/E-4 + engine C-7 → T006/T009/T029/T031/T048）
一致：回执/归档落点、干跑回执走输出流、`source.json` 回退不变;T048 载体受控已闭合（W3-18 fixed）。断点：W2-02、W2-16、W2-20、W2-03、W3-10（carried）。

**链 4 — 安全与确认链**（FR-015/FR-016 → cli C-5 + engine C-6 → T023–T027）
一致：双键、非交互 blocked、零执行不变。断点：W1-08、W1-09、W1-10、W2-18、W3-07、W3-17（carried）。

**链 5 — 验收与夹具链**（FR-023…FR-025 + SC-001/003 → engine C-8 → T007/T015/T022/T023/T028/T029/T032/T045/T046）
一致：声明驱动构造、五维对齐不变。**DoD-1（W3-15）与 DoD-3（W3-09）判别力已修复**；断点：W1-16、W1-17、W1-25、W1-27、W3-06、W3-19（carried）。

**链 6 — 分发与装配链**（FR-021/FR-022 → template T-1…T-6 → T033–T040）
一致：四副本再生、AUTO-GENERATED、COMMAND_BASELINE 29→30 不变。断点：W2-19、W3-04、W3-05、W3-13（carried）。

**链 7 — 宪法载体链**（宪法 VII ↔ tasks sigil / GATE-4 / T048）
一致：sigil（tasks.md:77）与载体名（`verification.log`）全副本闭合；载体受控（负规则实测生效）。**R3 断点清零**（W3-02→W3-16 传播闭合、W3-18 闭合）；机制侧残差（`templates/tasks-template.md` 等仍用 `verification.md`）维持 accepted upstream observation。

**链 8 — checklist 问责链**（checklists/ ↔ findings）
一致：39 条全部已处置（23 raised + 16 covered-by，undispositioned 0）；[Gap] 16 条同上。断点：见附录 A。

---

## 5. Coverage / Feature / Constitution / Unmapped

### 5.1 Coverage Summary

| Item | Reading |
|---|---|
| FR / SC / STR | 25 / 9 / 4（`[[STR-NNN]]` 引用全部可解析） |
| User Stories / Edge Cases / Assumptions | 4 / 10 / 11（A1–A11） |
| Clarifications | 2 场，6 + 5 = **11 问**（checklist 头部记 6+4 → W1-28） |
| FR → task（纸面） | **25/25** 追溯表有行；任务行 **48**、无缺号（R11 实测） |
| FR → task（行级证据） | 弱于纸面：W3-04（表↔文漂移）、W3-05（SC-007 行级 0）、W3-08（FR-004/005/011/012 无测试行）；**W3-15 已修复移出本行** |
| 零 C/H 重读抽样（zero-finding floor） | 抽样 **8 行**：全部单任务承载 FR（FR-004@T016、FR-008@T015）+ 样本 T005/T013/T015/T023/T029/T033/T048 逐行重读——行存在、引用可解析、单点 FR 恰为两条（与 DoD-1 一致），无新缺口 |
| clause accountant（本轮实测） | `status: uncovered`（exit 1）；claimed 11；fr-uncovered 21（4/25）；clause-uncovered 644（4 beyond baseline 640）；unparsable 108；25 error / 1 warning |
| 夹具覆盖 | 三类夹具声明驱动构造在 C-8 具名；需求层一致性 W1-16/W1-17（carried） |

### 5.2 Feature Linkage Summary（G 通道）

| 项 | 读数 |
|----|------|
| 绑定 | Feature 024（Specification Workspace Versioning）；requirements.md:14–17 与 checklist 头部一致 |
| 索引行 | `.specify/features.md` L33：`Planned`，Spec Path 指向 097 requirements，Last Updated `2026-11-10 (plan: …)`——状态/路径/日期合规 |
| 详情文件 | `.specify/features/024-specification-workspace-versioning.md`：`Planned`，Latest Review/Key Changes 已含 097 plan 记录 |
| G 通道结论 | **零 finding**。观察（不升级）：索引行 Last Updated 叙事仍以 "plan:" 起首，tasks/checklist/analyze 工件已存在；日期为当日、无陈旧，下次 registry 触碰时顺带更新 |

### 5.3 Constitution Alignment Issues

- **无 CRITICAL**。D 通道全量重跑零冲突；r3 修复（载体名、受控载体、可转红判据）均按宪法 VII/VI 字面闭合。
- decision tension 校验器（`validate-decision-tensions.py --json`）：`status: ok`，2 记录，6 类标签 0 失败（R3 实测）。
- 机制侧与宪法字面的分叉（上游模板仍用 `verification.md`）维持 accepted upstream observation，不在本特性内稀释。
- W2-17（E-5/C-3 双份五值表）维持 LOW：owner 声明存在、两份表为契约/模型投影；不升格为宪法 CRITICAL（沿用前两轮裁定，见 §8 S-2）。

### 5.4 Unmapped Tasks

- 未发现「无任何 FR/SC 锚点」的任务行：48 行均有阶段归属与至少一个 FR/SC 引用或追溯表映射。
- 反向漂移登记：W3-04（T034/T039 行内点名未全部入表；SC-009→T038 表列而 T038 只点名 FR-021）、W3-05（SC-007 行级 0 次）、W3-08（四条 FR 无测试行）。

---

## 6. Rerun Delta（R2 → R3）

| 类别 | 条目 | 数量 |
|------|------|------|
| **Resolved** | W3-09（H）、W3-15（H）、W3-16（H）、W3-18（M）——证据见 §0.1/§4.1（R11–R15）与 §9 验证波 | **4** |
| **New** | 无（八通道 + H 通道全量重跑；r3 修复未引入新 finding；补充读数并入既有 W1-28/W3-13 scope note，不另立 ID） | **0** |
| **Carried-over** | M 32 + L 19（§2/§3 全部标注 carried-over） | **51** |
| **当前开放账本** | 55（R2 open）− 4（resolved）+ 0（new）= **51**（H 0 · M 32 · L 19） | 51 |

**判定声明（两个方向分开）**：R2 账本中的全部 C/H **已清零且经独立验证**；本轮重跑**未产生新 C/H**。「清空历史 C/H 积压」与「本轮干净重跑」在本报告同时成立，且前者不替代后者。

---

## 7. Metrics

| 指标 | 读数 |
|------|------|
| 输入 | 全 spec 目录（11 文件 / ~126 KB）+ 宪法 567 行 + 基线 640 names + 前两轮账本 |
| 归并后开放账本 | **51**：CRITICAL 0 · HIGH 0 · MEDIUM 32 · LOW 19 |
| Resolved（本轮） | 4（3H · 1M） |
| New（本轮） | 0 |
| C/H 复核锚点 | validated 4 / proposed 0 |
| 验证波 | 3 dispatched · confirm 3 · downgrade 0 · reject 0（downgrade 率 0/3） |
| H 问责 | unchecked 39 / dispositioned 39 / undispositioned 0；[Gap] 16：raised 10 / covered-by 6 |
| FR→task | 纸面 25/25（100%）；行级缺口见 §5.1 |
| Feature linkage | 024 绑定成立（100%）；G 零 finding |
| clause accountant | uncovered（exit 1）；claimed 11；fr-uncovered 21（4/25）；clause-uncovered 644（4 beyond 640） |
| decision tension | status ok（2 记录 / 6 标签 0 失败） |
| 相对单通道 50 行上限 | 溢出 1 行（32+19 = 51）；按驱动阶段指令不截断，此处显式记账 |

---

## 8. Systemic Observations（聚合，不提升任何单行严重度）

- **S-1 修复传播闭合（R2 首要观察 → 本轮关闭）**：W3-02→W3-16（载体第四副本）与 W3-03→W3-15（修复新增判据）两条传播链在 r3 均以**机械读数**闭合；r3 修复把「同一事实全部副本」与「新判据可执行性实测」作为完成判据，做法生效。
- **S-2 修复记录自身的表述精度**：`analyze-repair-dispositions-r3` 的 W3-09 行括号称「补齐 C-5 的 obsolete roster，共五类」，但 `migrate-engine.md` C-5 并无 obsolete-roster 结构守卫行（其五类枚举只在 DoD-3/T013）。该差异只存在于修复记录（dated record），不改变任务/契约的可执行形态；建议后续修复记录引用锚点时逐字核对（并入 W3-13 的同一主题）。
- **S-3 DoD 判别力（改善中）**：W3-15/W3-09 已从「声称会转红但机制不成立」改为「可执行形态 + 实测读数」；W3-17（T023 第四变异）与 W3-19（T035 结局表无守卫）为同一主题的残余。
- **S-4 覆盖证据双轨**：W3-04/W3-05/W3-08 未动——追溯表、行内文本与 SC/Measurement Sources 三处不成闭环；SC-007 行级覆盖仍为 0。
- **S-5 封闭词表多处漂移**：结局表双份手写副本（W2-17）、`converged` 无载体（W2-15）、机制 token 不闭合（W2-05）、`aborted`/`removed-stale` 无触发（W2-03）。
- **S-6 回执与指针卫生**：W2-02/W2-16/W2-20 合计指向 `workspace` 字段、E-2→E-4 引用与 from→to 命名的三处不可解析/不一致。
- **S-7 结构损伤簇**：E-8 表头粘连与 C-5 表体截断（W2-06）仍为早期 LOW 未修；建议修复流程增加 Markdown 结构校验。
- **S-8 单文件账本并发**：W3-10 的 red-first 单文件与「记录类数据一文一件」冲突，影响 implement 并行派发设计。

---

## 9. Validation wave（独立只读验证，2026-11-10）

- **载体**：recipe 7 形态的 subprocess 派发（`.specify/skills/internal/create-team/scripts/dispatch.sh`，`qodercli` 1.1.85），3 个进程并行；flags：`-p --output-format stream-json --permission-mode auto --tools Read Grep Glob Bash --no-session-persistence`。未使用任何宿主会话创建 API。
- **读域隔离**：每个 validator 只收到 1 条 closure finding（ID/类别/主张/严重度）+ 证据位置，禁止读取任何 merged/findings/disposition 记录。
- **裁定**：`confirm` 3 / `downgrade` 0 / `reject` 0（W3-16 与 W3-18 合并为一个 validator，两 verdict 均 confirm）。
- **边界照录**（§0.1）；未观察到越权写入：验证波前后 `git status --porcelain` 仅含前序未提交文件与本轮 evidence 产物，spec 制品零变更。
- **降级率**：0/3 —— 无证据表明检测过评严重度。

---

## 10. Wrap-up 记账

- **单元**：analyze round 3（unit: `skill:analyze-artifacts`@097）。
- **引擎记录**：Run Determination / Exec Quant / Feedback Record 三步均已按 `## Wrap-up` 执行，三引擎均返回 **duplicate**（同一 `skill:analyze-artifacts × r20261110T081104Z-b097` 已由 round-1 记录），按驱动契约「duplicate 的跳过同样计入满足」计为已记账，无新记录文件；round-1 的既有记录即本 run 的权威记账。Feedback 引擎附带读数 `count_since_submission=399 / threshold=10 / should_prompt=true`——**阈值提示（非阻塞）**：可随时用 `/speckit.feedback` 打包上送；不影响本阶段。
- **产物**：本文件 + `analyze-gates-r3-2026-11-10.txt`（门禁与修复面实测原始读数）；未修改任何 spec 制品。
- **Token 反思（token-efficiency）**：本轮以「全量重读 + carried 账本复用」组合运行；对未触碰的制品采用 prior-anchor 复用、仅对 r3 触碰的 `tasks.md` 逐项重锚，属有意的效率取舍；可改进点已作为 feedback point 记录（引擎 duplicate，未新增条目）。
- **异常**：无异常；无即修（nothing to report is something to say）。
- **上游偏差**：`checkpoints/01-requirements.md`、`02-clarify.md` 与 `test-evidence/analyze-validation-round2-2026-11-10.md` 为前序阶段未提交文件，本阶段不代提交、不还原（沿用 round-1/round-2 记录）。

---

## 附录 A — Checklist H 逐条 disposition ledger（沿用 R2 逐字保留）

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

**计数核对**：39 − (23 raised + 16 covered-by) = 0；[Gap] 16 − (10 raised + 6 covered-by) = 0。全部 raised ID 均为本报告 §2/§3 中的 open carried finding；全部 covered-by 锚点在当前 requirements 中可解析。
