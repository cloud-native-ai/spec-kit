# Verification Log — 052-fast-fail-principle

feature=052-fast-fail-principle
feature_title=快速失败纪律(Fast Fail)
run_command=/speckit.implement
run_date=2026-09-23
run_outcome=partial-completion
tasks_total=63
tasks_closed=63
tasks_open=0
tasks_deferred=0
revalidation_date=2026-09-24
revalidation_scope=T058 穷尽派生命令审计(`notes/derived-command-audit.md`)+ GATE-1…GATE-9 对当前树全部重跑;状态**未**翻转(见 GATE-1_note 与 notes_revalidation)

# -- Baseline (recorded once, BEFORE any /speckit.implement work changed the tree) --

baseline_commit=80a8c1fb0e27c70c797974affb8e88510558da19
baseline_date=2026-09-23
baseline_branch=052-fast-fail-principle

baseline_gate_total=23
baseline_gate_destructive=13
baseline_gate_governance_kept=10
baseline_gate_violations=0
baseline_gate_integer_headroom=0
baseline_blocking_patterns=17
baseline_policy_docs=2
baseline_mirror_diff_shared=2
baseline_mirror_diff_agents=0
baseline_mirror_diff_templates=2
baseline_mirror_diff_skills=38
baseline_regen_pending=84
baseline_tests_failed=76
baseline_tests_passed=2684
baseline_template_h2_sections=18
baseline_live_h2_sections=19
baseline_template_principles=13
baseline_live_principles=15
baseline_command_must_include=7
baseline_constitution_version=1.12.0
baseline_shared_guidelines_count=12
baseline_factory_agent_presets=2
baseline_payload_field_rows=5
baseline_ufc_dedup_pin=8
baseline_live_instructions_bytes=28168
baseline_instructions_budget_bytes=32768

# -- Post-run measurements (all from live commands, never carried over from memory) --

final_gate_total=23
final_gate_violations=0
final_scanner_git_diff=empty
final_mirror_diff_shared=0
final_mirror_diff_agents=0
final_mirror_diff_templates=2
final_mirror_diff_skills=36
final_regen_pending=0
final_tests_failed=68
final_tests_passed=2797
final_tests_skipped=2
final_template_h2_sections=19
final_live_h2_sections=20
final_template_principles=14
final_live_principles=16
final_command_must_include=8
final_constitution_version=1.13.0
final_shared_guidelines_count=13
final_payload_field_rows=6
final_ufc_dedup_pin=9
final_live_instructions_bytes=30862
final_guard_functions=105
final_guard_passing=105
final_contract_clauses=107
final_doc_lines=308
final_doc_blocking_hits=0
final_clause_interval_lines=5
final_clause_interval_bytes=801

# -- Re-validation 2026-09-24 (T058 audit + full gate re-run) --
# Tree is NOT the 2026-09-23 landing tree: 052's 15 commits (5fc6a2f3..b7aeba9d) are followed by
# 15+ non-052 commits, and three files outside this feature's scope were mid-edit by a concurrent
# session during the run. Every value below is live output; the final_* block above stays as the
# implementation-run record and is NOT overwritten.

rev_gate_total=23
rev_gate_violations=0
rev_gate_destructive=13
rev_gate_governance_kept=10
rev_blocking_patterns=17
rev_policy_docs=2
rev_tests_failed=65
rev_tests_passed=2927
rev_tests_skipped=2
rev_new_failure_names=0
rev_healed_baseline_failures=11
rev_guard_functions=105
rev_guard_passing=105
rev_gate5_passing=227
rev_mirror_diff_shared=0
rev_mirror_diff_templates=2
rev_mirror_diff_skills=30
rev_mirror_diff_agents=0
rev_mirror_diff_scripts=1
rev_mirror_skills_new_members=0
rev_payload_field_rows=7
rev_live_instructions_bytes=30944
rev_instructions_budget_bytes=32768
rev_template_h2_sections=19
rev_live_h2_sections=20
rev_constitution_template_principles=14
rev_live_principles=16
rev_constitution_version=1.13.0
rev_command_must_include=8
rev_ufc_dedup_pin=9
rev_shared_guidelines_count=13
rev_factory_agent_presets=2
rev_doc_lines=308
rev_doc_blocking_hits=0
rev_clause_interval_lines_raw=6
rev_clause_interval_lines_nonblank=5
rev_clause_interval_bytes=801
rev_clause_prompt_bytes_drill=931
rev_contract_clauses=107
rev_ff_entries=15
rev_rp_entries=6
rev_quickstart_scenarios=12
rev_audit_items=198
rev_audit_matched=191
rev_audit_mismatched=5
rev_audit_not_reproducible=2
rev_audit_not_run=0
rev_audit_corrections=4
rev_audit_correction_sites=8

# -- Success Criteria --

SC-001_status=partial
SC-001_value=判定级 12/12 = 100%;规则级 首轮 11/12 = 91.7% → 次轮 12/12 = 100%
SC-001_note=两轮双评审取证于 `notes/sc001-dual-review.md`,四个互不共享上下文的只读子代理(首轮 A/B、次轮 C/D),12 场景表与派发提示逐字相同故两轮可比。次轮在 FR-014 同一性键裁定落地后达成规则级 100%。**仍为 partial 的理由**:两轮都在真源文档尚有五个空节(`## 子代理派发注入`、`## 生长闭环`、`## 与相邻纪律的边界`、`## 冲突裁决顺序`、`## 范围限制`)时进行,四位评审者各自上报了这一点;九节现已全部填实,但**未对完整文档跑第三轮**。12 个场景所依赖的判据全部落在当时已填成的三节内,故次轮结论对这些场景有效,但 SC-001 的措辞是"按真源文档",严格读法要求对完整文档复跑。
SC-001_unblock=以同一份 12 场景表对已填实的完整文档再跑一轮双评审;若规则级仍为 12/12 则可改判 pass。

SC-002_status=pass
SC-002_value=7/7
SC-002_note=`test_c14_seven_named_failures_locatable` 与 `test_c15_named_failure_sentinel` 均绿;quickstart 场景 7 实跑 `FF-2`…`FF-8` 各命中 **1**。断言按 7 项逐项进行,不按清单总条数(FR-020:清单可生长,不设钉子)。清单实际条数为 FF 15 + RP 6 = 21。

SC-003_status=pass
SC-003_value=独立措辞定义点 1;复述扫描命中 0
SC-003_note=`test_a18_convergence_scope_bounded` 绿:对 `shared/` 与 `templates/` 递归扫描 9 个节标题 + STR-005/STR-006 字面量 + `- **FF-` / `- **RP-` 条目前缀,offenders 为空(真源文档自身除外),并配伴生断言证明拥有者确实携带全部 needle。`## 范围限制` 被显式排除并附实测理由(与 `user-facing-comprehension.md` 的同名章节碰撞,属两条纪律各自的节而非复述),排除理由本身也被断言仍成立。

SC-004_status=pass
SC-004_value=章节集合差 0;既有章节被改动 0
SC-004_note=`test_a7` 绿(模板 19 / 活动 20,且模板章节集 ⊆ 活动章节集);`test_instructions_section_propagation.py` 与 `test_user_facing_comprehension_section.py` 的 `test_c7`/`test_c8` 两根位置钉子实跑 passed。`git diff --numstat` 对 `templates/instructions-template.md` 为纯插入(0 删除),即既有章节零改动。四条兼容性符号链接仍为符号链接。

SC-005_status=pass
SC-005_value=total 23(相等);violations 0;扫描器 diff 空;新增文本命中 0
SC-005_note=quickstart 场景 4 逐字提取实跑得 `frozen: 23 live: 23 violations: 0` + `TOTAL-EQUAL`;`git diff --stat` 对 `scripts/python/scan-confirmation-gates.py` 与其余五个引擎为空(GATE-3);真源文档 308 行逐行 `BLOCKING_RE` 命中 **0**;`test_g1`…`test_g17` 全绿。⚠️ 相等判据 MUST 用直接比较而非 `--baseline` 旗标:该旗标读基线的**顶层** `total` 键而 050 基线把它嵌在 `confirmationGates` 下,且其退出码只反映 violations(变异演练:冻结值改 99 仍 `EXIT=0`)。GATE-2 已据此改写。

SC-006_status=pass
SC-006_value=模板 1 / 命令 1 / 活动原则 15→16 / 版本 1.13.0 / plan-template 改动 0 而渲染行数 15→16
SC-006_note=quickstart 场景 3 实跑相符;`test_x18_downstream_gate_rows_15_to_16` 以"去掉 XVI 后枚举得 15、含 XVI 得 16"实测动态枚举的传导,并配双向伴生断言;`test_constitution_double_landing.py` 19 passed(四钉上调为 14/16/8/(1,13)、watchlist 2→3、其自带的删除任一侧即红的变异探针)。

SC-007_status=partial
SC-007_value=标记检索命中 1(隔离根内);真实存据仍 0;留痕率 不适用
SC-007_note=quickstart 场景 8 实跑:`--workspace-root` 一次性根内 record → list 得 `count: 1`,真实存据按标记过滤仍为 `{"count": 0, "matches": []}`(反空真哨兵:证明隔离生效而非查询读空),`rm -rf` 后目录不存在。**partial 的理由**:SC-007 的后半("清单每次提升对应至少 1 条观察记录或 1 次可定位的用户纠正,留痕率 100%")在本轮**无样本**——两份清单自落地以来未发生过任何条目移动,故留痕率不可测,不能记为 100%。机制侧已由 `test_c18`(双向规则 + 留痕要求 + 禁止静默调参)守卫。 **2026-09-23 的落地后运行同样没有为本 SC 产生样本**(2026-09-24 追加):该次 `/speckit.feedback consume` 运行有 12 次派发与 18 条异常回传,但 SC-007 的后半要的是**清单条目真实移动过一次**的留痕,而两份清单自落地以来**仍无任何条目移动**,故留痕率仍不可测,`status` 保持 `partial` 不变。⚠️ 编排者在该运行中曾一度以为这批样本能解 SC-007 / SC-009 的 partial,实测核对后才发现映射错了——它们真正对应的是 SC-013 / SC-014(见二者的落地后佐证);此处记录该误判,以免后人再按同一条路走一遍。
SC-007_unblock=待首次真实清单移动发生后,核对其留痕(反馈条目 ID / 提交号 / 会话原话之一)。

SC-008_status=deferred
SC-008_value=不可得
SC-008_note=读者测试要求**未参与本特性实现**的读者,对一份上送件样本在**不打开任何其他工件**的前提下从处置集中选出一项并说明理由。本轮的实现者即本会话,不满足独立性。
SC-008_deferred_reason=需要未参与实现的独立读者;单会话不可得。先例:Feature 051 的同类 SC 亦记 deferred。MUST NOT 以"四要素标题齐备"替代(SC-008 明文禁止该循环判定)。

SC-009_status=partial
SC-009_value=披露率 100%(本轮自身);干净运行显式陈述 不适用(本轮非干净运行)
SC-009_note=本轮全部顺手修复均在阶段报告与收尾报告中逐项披露(共 6 处修复 + 3 处自身断言缺陷 + 1 次演练残留清理),未出现未披露的就地修复;因披露而新增的打断次数为 0(合并在阶段报告中呈现)。**partial 的理由**:SC-009 的第三项"干净运行的显式陈述在场率 100%"在本轮无样本——本轮有异常也有修复,不属干净运行。该义务由 `test_c17`(STR-013 在场)与 quickstart 场景 12(`repairs=0 fails=0 -> True`;`repairs=2 -> False`;`fails=1 -> False`)守卫,即"只有干净运行需要该陈述"这一判据已被实跑验证。 **2026-09-23 的落地后运行同样没有为本 SC 产生样本**(2026-09-24 追加):SC-009 的第三项要的是一次**既无快速失败也无顺手修复的干净运行**,而该运行既有 18 条异常也有修复,故不构成本项的样本,`status` 保持 `partial` 不变(该批样本被误映射到本 SC 与 SC-007 的经过见 SC-007_note)。
SC-009_unblock=在一次既无快速失败也无顺手修复的运行中核对其收尾报告含 STR-013 起首的陈述。

SC-010_status=pass
SC-010_value=8/8 点位各 1 行指针;正文改写 0 行
SC-010_note=`test_a16`/`test_a17` 绿(每个点位恰 1 行指针、指针不在代码围栏内、其自身行为正文片段仍在场;伴生断言证明 8 行指针确实都存在)。`git diff --numstat` 对 8 个文件逐个为 `2 0`(2 插入 / **0 删除**),即行为正文逐字未变。⚠️ 首次插入时 `templates/commands/todo.md` 的指针落进了围栏示例块内(`## Group N: <theme/module>` 是示例标题),已由围栏感知的重插修复,故 `test_a16` 增加了"指针 MUST NOT 在围栏内"这一断言。

SC-011_status=pass
SC-011_value=通道覆盖 3/3;副本逐字节一致 100%(10/10)
SC-011_note=通道一(编排者内联提示)由真源文档规定落点与形态(`test_i15`);通道二 = 2 份出厂预设 + 两处制作者要求(`test_i8`/`test_i9`/`test_i10`);通道三 = 团队载荷第六字段行(`test_i13`,实测 5→6)。quickstart 场景 5 实跑:拥有者 **1 对**定界符 / **5 行 / 801 字节**(≤10/≤1200),2 份预设 + **4 棵**按工具树共 **8** 个副本全部 `byte-identical: True`,2 份镜像 `MIRROR-OK`。`test_i12` 断言守卫对象是**有界集合**(2 预设 + 2 制作者要求),并断言本模块源码不枚举用户自建的实例目录。

SC-012_status=pass
SC-012_value=四步取证齐全;演练制品计数归零
SC-012_note=quickstart 场景 6 逐字提取实跑:`prompt bytes: 931` → 子句命中 **3 → 0 → restored 且 3 → `No such file or directory`**,exit 0。取证记入 `notes/red-first-evidence.md` 与 `notes/quickstart-run.md` 两处。演练目录 `/tmp/ffdrill` 已复核不存在。

SC-013_status=pass
SC-013_value=编排者侧 4/4 分类正确;子代理侧 实现期 4/4 + 落地后另一次运行 12/12 回传携显式异常行(静默回传 0)
SC-013_note=**编排者侧**(可由演练取证):quickstart 场景 10 实跑四例分类为 `anomaly-halt / clean / incomplete / incomplete`——第四例"行内提及 `ANOMALY:`"正确落到 `incomplete` 而**非** `clean`,证明行首判据生效;`doc carries the rule: True`。**子代理侧**(不可由契约测试断言,因回传不落盘):本轮实际派发 4 个子代理(SC-001 两轮各 2 个),派发提示均要求行首 `ANOMALY:` 或 `未发现异常`,**4/4 回传携显式异常行**(首轮 A 1 条 / B 2 条,次轮 C 2 条 / D 2 条),无一行缺失,故未出现"缺行被判为干净"的情形。 **落地后佐证(2026-09-23 的另一次运行,2026-09-24 追加;不属于实现期取证,MUST NOT 被读作实现期就跑了 12 次)**:本 SC 的 status/value 判定于实现期(上文 4 次派发);此后一次真实的 `/speckit.feedback consume` 运行提供了大得多的样本——该运行分两波共 **12 次子代理派发**(第一波 5 个并行只读核验器、第二波 7 个并行修复代理),**12/12** 的派发提示都**逐字携带**了真源文档的注入子句(`<!-- fast-fail-clause:begin -->` … `:end -->` 之间的拥有者字面量)并要求一条显式异常回传行;回传共 **18 条行首 `ANOMALY:`**(第一波 3 条、第二波 15 条)加若干 `未发现异常`,**静默回传 0 次**(无任何一次回传缺异常行)。样本来源:编排者提供的该运行实测数据;回传不落盘,故无法由命令复核——这正是本 SC 子代理侧只度量不设阈值的原因。

SC-014_status=pass
SC-014_value=原样重派 0 次(实现期 0 + 落地后另一次运行 0);异常停后续动作 实现期 1/1 为上送 + 落地后 18/18 未被就地修平
SC-014_note=本轮唯一一次异常停是 FR-014 同一性键不可达(T013 的 SC-001 取样检出),其后续动作为**上送用户裁定**(四要素上送件 + 封闭处置集),用户选定甲案后按裁定级联落地为 T063。原样重派次数 **0**。`test_i21` 绿:真源文档点名排除既有的**全部**三条失败规则(两振停滞 / 连续两次派发失败即降级 / 非并行任务失败即停),quickstart 场景 11 实跑 `next action: surface-to-user | allowed: True | forbidden: False`。 **落地后佐证(2026-09-23 的另一次运行,2026-09-24 追加;不属于实现期取证)**:该次 `/speckit.feedback consume` 运行的 12 次派发回传了 **18 条行首 `ANOMALY:`**,其中**没有一条被子代理就地修平**——每条要么被子代理自己判为「裁定」并停在本层上交,要么判为「纠正」并在回传中披露;编排者对每条都做了归属处置(接受其纠正 / 自行修复 / 记为未决项),**原样重派 0 次**。这为本 SC 的两条命题(异常停不被原样重派、异常停不被就地消化)提供了实现期之外的真实运行样本;数据来源与不可命令复核的理由同 SC-013_note。

SC-015_status=deferred
SC-015_value=不可得(无运营周期)
SC-015_note=三个数(快速失败率 / 用户推翻率 / 清单净生长方向)需要一段运营期的带标记反馈存据才能导出。本轮无该存据(真实存据按标记过滤为 `count: 0`)。
SC-015_deferred_reason=度量而非门禁:需累积一段时期的 `[fast-fail]` 标记条目。机制侧已就位——`test_c19` 断言三个数在真源文档中被载明、且声明由既有存据导出、MUST NOT 新增计数器或台账。**MUST NOT 编造数值**(STR-006 与真源文档的两条红线)。

# -- Gates (re-validated against the current tree, not trusted from the all-tasks-done state) --
# 2026-09-24 全部九项对当前树重跑。当前树 = 052 的 15 个提交(5fc6a2f3..b7aeba9d)+ 其后 15+ 个非 052 提交;
# 运行期间另有三个 052 之外的文件处于并发会话的未提交编辑中(见 GATE-1_note)。下列每个值都是本轮实跑输出。

GATE-1_status=pass
GATE-1_note=**2026-09-24 编排者复跑后转绿**。名字级判据实跑:`bash .specify/scripts/bash/run-tests.sh --names-out …/current-failed.txt -q tests/` → **65 failed / 2927 passed / 2 skipped**,`comm -13 baseline current` 输出**为空** ⇒ 零新增失败。伴生量(证明这不是空集比较):基线 **76** 条中治好 **11** 条(76 − 11 = 65,与实测一致);守卫文件 `test_fast_fail_discipline.py` 在 current-failed 中贡献 **0** 条。**前一轮 fail 的根因已消除且与本特性无关**:唯一新增名曾是 `tests/contract/test_specify_script_paths.py::test_review_prerequisite_flags_are_supported`,该测试以 `check=True` 对**真实仓库**跑 `check-prerequisites.sh --include-plan`,而 Feature 053 当时只有 `requirements.md`、无 `plan.md`,故 exit 1。其**自身 docstring 声明的命题是「旗标被接受」**,却把判定绑在「当前特性恰好有 plan.md」这一环境状态上——每轮 `/speckit.requirements` 到 `/speckit.plan` 之间都会红。已按该命题重修:拒旗标表现为 usage/Unknown option 错误,而「缺 plan.md/tasks.md」恰是 `--include-*` 被解析并执行的**证据**,故两种结局都通过,并配反空真哨兵(容忍的非零退出 MUST 匹配 `(plan|tasks)\.md not found`)。变异演练:注入 `--include-bogus-flag` → 该哨兵变红并点名 `Unknown option` → 精确反向替换复原 → `diff -q` 与备份 BYTE-IDENTICAL、7 passed。另一臂(exit 0 全键断言)在 052 的临时 worktree 中实跑取证:脚本解析到 052、`AVAILABLE_DOCS` 含 plan.md 与 tasks.md、7 passed;worktree 已 `--force` 移除、`git worktree list` 回到 1 条、052 分支零污染。 **前一轮(2026-09-24 子代理轮)记录**:两次实跑得 68 failed / 2922 passed(`comm -13` 3 条,其中 2 条源于并发编辑的中间态——两测试经 `runpy` 载入分类模块时其模块级 `TABLE = _parse_table()` 抛错,数分钟后同一解析返回 25 条即自愈)与 66 failed / 2924 passed(`comm -13` 1 条,即上述 `test_specify_script_paths` 一项)。
GATE-2_status=pass
GATE-2_note=直接比较形态实跑得 `frozen: 23 live: 23 violations: 0` + **`TOTAL-EQUAL`**;`scan-confirmation-gates.py | head -1` → `blocking confirmation gates: 23`。被否决的 `--baseline` 形态本轮亦重跑,其两个缺陷仍复现:`baseline delta total: **+23**`(读顶层 `total` 键,而 050 基线把该值嵌在 `confirmationGates` 下)且 `EXIT=0`(退出码只反映 violations)。
GATE-3_status=pass
GATE-3_note=**度量窗口已订正,三段并记**。① 门禁原文的字面形态 `git diff --stat -- scripts/ src/specify_cli/ skills/create-team/scripts/ templates/plan-template.md`(不带 SHA)输出为空——但该形态在洁净树上恒空真,正是本制品 Notes 自己点名的盲检,不足以承担判据;② 2026-09-23 记录所用的 `git diff --stat <BASE_SHA> -- …` 窗口今**非空**(8 个文件:`generate-instructions.sh`、`update-feature-index.sh`(删除)、`feedback-utils.py`、`goal-utils.py`、`validate-tasks.py`、`match-team-preset.py`、`verify-territory-disjoint.py`、`plan-template.md`);归属实测:`git log BASE_SHA..HEAD -- <四路径>` 列出 5 个提交,其中携 052 主题者 **0** 个;③ 窗口收窄到 052 自己的提交区间 `git diff --stat 80a8c1fb b7aeba9d -- <四路径>` → **为空**。故"052 对引擎与脚本零改动"成立;不成立的是"BASE_SHA..HEAD 即 052 的改动面"这一前提。
GATE-4_status=pass
GATE-4_note=集合包含判据成立,但**工具已替换并在此披露**:`sync-mirrors.py` 被本次派发的硬约束禁止(任何模式),故以只读等价物复刻其语义(`ast.literal_eval` 取 `MIRROR_PAIRS` / `IGNORE_NAMES` + `filecmp.cmp(shallow=False)`,并复刻 MISS/DIFF/EXTRA 与 `ok … (N files)` 的判定分支)。实测:**shared DIFF 0** ⊆ 冻结 2;**templates DIFF 2** = 冻结 2(`proactive-trigger-seed.json`、`skills-template.md`);**skills DIFF 30** ⊆ 冻结 38,机械集合比较 `live − frozen` = **空**(新增成员 **0**,治好 8);**agents files=2 / MISS 0 / DIFF 0** ⇒ 引擎将印 `ok    agents/ == .specify/agents/templates/ (2 files)`。另:`scripts` scope DIFF **1**(`.specify/scripts/python/trigger-utils.py`,改前既有漂移,且不在本门禁点名的四个 scope 内)。
GATE-5_status=pass
GATE-5_note=七文件合跑 **227 passed**;逐文件:`test_fast_fail_discipline.py` **105**、`test_constitution_double_landing.py` **19**、`test_user_facing_comprehension_doc.py` **23**、`test_user_facing_comprehension_section.py` **11**、`test_proactive_trigger_section.py` **24**、`test_instructions_section_propagation.py` **2**、`test_confirmation_gates_sweep.py` **43**(实现期记 40,该文件此后由 052 之外的提交增 3 条)。六条 `-k` 分区逐行重跑:T011 **19** / T018 **15** / T026 **18** / T037 **25** / T043 **3** / T052 **22**,收集数与各区间认领条款数相等(反空真哨兵:六者皆非零)。
GATE-6_status=pass
GATE-6_note=`cmp shared/guidelines/fast-fail.md .specify/shared/guidelines/fast-fail.md` 静默 → **BYTE-IDENTICAL**;两份出厂预设与其 `.specify/agents/templates/` 镜像亦各 **MIRROR-OK**;真源文档 308 行、逐行 `BLOCKING_RE` 命中 **0**、四个项目专名命中 **0**。
GATE-7_status=pass
GATE-7_note=`grep -cE '^- \[[ >]\]' tasks.md` → **0**;sigil 实测 `[X]`=**63** / `[ ]`=**0** / `[>]`=**0** / `[~]`=**0**(合计 63,**零残留、零移交**)。前一轮记为 `[~]` 的 T058 已于 2026-09-24 由编排者改判 `[X]`:两项残留(`regen-command-copies.py --check` 与 quickstart 场景 8 的隔离 `record`)均已实跑且与制品所印相符(前者 EXIT=0 并输出 `OK: all per-tool command copies match the source templates.`;后者隔离根内 `count = 1` 满足印出的 `≥ 1`、真实存据 `total_entries` 前后均为 3 未污染、临时根删净且残留 0),取证见 `notes/derived-command-audit.md` §12 N2/N3 与 §15。**移交理由本身已订正**:派发禁令写得过宽——`--check` 是只读模式,`--workspace-root` 隔离形态不触及真实存据。
GATE-8_status=pass
GATE-8_note=`for n in $(seq -w 1 15); do grep -q "SC-0$n\|SC-$n" … || echo "MISSING SC-$n"; done` 输出**为空**(15/15 在场,每条含 status / value / note 三字段;deferred 两条各附 `deferred_reason`)。
GATE-9_status=pass
GATE-9_note=`python3 .specify/scripts/python/validate-tasks.py …/tasks.md` → **EXIT=0**,0 error,1 warning。仍是 T014/T015 的 `[P]` 并行安全告警;校验器本体已由 052 之后的提交改写,告警措辞变为 "WRITES […] while T015 only references it as a read-only target",判定不变(两行写入集不相交,属误报,理由见 tasks.md › Notes)。

# -- DoD --

DoD_status=met
DoD_note=2026-09-24 编排者对当前树逐条复核,**12 项全部达成**。DoD-1…DoD-10 仍为真(真源文档 9 节且与镜像字节相等;常驻章节位置合法、节数 19/20;宪章双落点与四钉 14/16/8/(1,13);注入子句与全部副本字节相等;守卫 105/105 与既有守卫合跑 227 全绿;门控中立 total 23 相等且扫描器在 052 窗口零改动;镜像取集合包含的相对判据,skills live 30 − frozen 38 = **新增成员 0**;名字级回归见 GATE-1,现为空;12 个 quickstart 场景全部重跑;类 ⑪ 登记与四处留痕在场)。**DoD-11 由 partial 订正为达成**——其原文要求三件事:逐条给出 SC-001…SC-015 的状态、不可得者记 `[~]` 并说明理由、MUST NOT 编造通过率;三者均已满足(GATE-8 绿:15/15 有状态行;SC-008/015 为 deferred 且各附 `deferred_reason`;SC-001/007/009 为 partial 且各附 `unblock`)。前一轮把 DoD-11 读成「15 条 SC 全部 pass」,那是**另一个命题**:DoD-11 管的是如实报告,不是全绿。**DoD-12 由「基本达成、残留 2 项已移交」升为达成**:198 项 check item 全部核完(相符 **191** / 不符 5——4 项制品值缺陷已订正或加日期化注解、1 项属当前树实况 / 不可复现 2 为计划期草稿子句三数,已改核**落地**子句 6 原始行·5 非空行·801 字节·逐行 0 命中 / 部分未实跑 **0**),残留归零;两处双重枚举锁步一致亦复核(封闭处置集四项在真源文档 / `data-model.md` E6 / `contracts/discipline-doc.md` C-17(b) 三处各命中;子句长度上限 ≤10 行 / ≤1200 字节两处一致)。**按 Pre-Status-Flip Gate 第 6 步显式披露一处 void 项**:GATE-3 的字面形态(不带 SHA 的 `git diff --stat -- <四路径>`)在洁净树上**恒空真**,其前提「`BASE_SHA..HEAD` 即 052 的改动面」已被实测证伪(该窗口含 8 个文件、5 个提交,携 052 主题者 **0** 个)。该项判为 **void 而非 unmet**——不阻断翻转,但已附实测于 GATE-3_note、在 `tasks.md` 的门禁项上加内联注解,并在此处surface;真正承担判据的是收窄到 052 自身提交区间 `80a8c1fb..b7aeba9d` 的度量,其输出为空。**5 条 SC 非 pass(3 partial + 2 deferred)不构成 DoD 未达成**:DoD-11 明文允许「不可得者记 `[~]` 并说明理由」;SC-001 的第三轮双评审义务记在 `SC-001_unblock`,SC-008 需独立读者、SC-015 需一段运营周期,二者各附 `deferred_reason`。

# -- Run-level notes --

notes=本运行是 **partial run**:63 个任务闭合 58、开放 5,停在一个树洁净、门禁 GATE-1…GATE-6 与 GATE-8/GATE-9 全绿、GATE-7 因未闭合任务而为 fail 的检查点上。Feature 052 状态**仍为 `Planned`**——推进到 `Implemented` 归 Pre-Status-Flip Gate,而该门要求 Completion Gate 全绿,GATE-7 未过,故**本轮 MUST NOT 落 `Implemented`**。(2026-09-24 订正:本行的"闭合 58、开放 5"是 09-23 关闭 T060–T062 之前的旧值,与本文件 header 的计数自相矛盾;header 为权威,今值见 `tasks_*` 三行与下方 `notes_revalidation`。)
notes_midrun_directive=2026-09-23 用户中途裁定(FR-014 同一性键拆为复发键与独立键)已按 Mid-Run User Directives 协议处理:上游 `requirements.md` 先改并把指令原文逐字追加进 `## Clarifications` › `### Session 2026-09-23`(append-only,行数 12 → 13 已核验),级联 `data-model.md` E2 / `contracts/discipline-doc.md` C-10(g) / 真源文档 / `test_c10`,新工作以**新任务号 T063** 追加而未重排既有 ID,并复跑双评审取证规则级一致率由 11/12 升至 12/12。
notes_upstream_defects=三条上游缺陷按 FR-077 如实上报、未顺手改写:① `Inherited premises` 悬空指针——存在于 `templates/instructions-template.md:41` 但不在活动的 `.specify/instructions.md`,而 10 个文件指向它;根因实测为 `generate-instructions.sh` 只做**整章节**增量注入,既有章节**内部**的新增永远传播不到已初始化项目(该机制同时正面印证本特性 D-1 取"新增顶级章节"的理由);② `scan-confirmation-gates.py --baseline` 的两个缺陷(键层级错位 + 退出码只反映 violations);③ `render_agents_for_tool` 对未知 tool 键**静默返回 `rendered: 0`**(`.github/agents` 的键是 `copilot` 而非 `github`)。另:活动指令文件中 Feature 051 的 `## User-Facing Comprehension` 节仍含"刷新指令即恢复镜像副本"的假承诺句式(实测命中行归属该节,本特性自己的章节区间命中数为 0),FR-077 明文规定该同类问题 MUST 单独上报而 MUST NOT 由本特性改写。
notes_self_defects=运行期查出的自身缺陷 9 处,其中 6 处顺手修复(各附变异演练或实跑取证)、1 处上送用户裁定、3 处属上游只上报。自身失误一次已修复并取证:变异演练的清理用了被 alias 成交互模式的 `cp` 且后接 `&& rm -f`,导致备份被删、演练文本残留在 `templates/commands/analyze.md`,已外科式移除并复核 `numstat = 2/0` 与其余七个文件一致。

notes_revalidation=2026-09-24 复核(代 `/speckit.implement` 执行一次已授权的门禁复核;**该转换的拥有者仍是 `/speckit.implement`**):T058 的穷尽派生命令审计做完并落盘 `notes/derived-command-audit.md`(198 项;订正 4 类、落在 6 个文件的 8 个位置),GATE-7 由 fail 转 pass;但 **GATE-1 在当前树上为 fail**(1 条新增失败名,根因是 Feature 053 尚无 `plan.md`,与 052 无关,详见 GATE-1_note),GATE-3 需把度量窗口收窄到 052 自己的提交区间才成立,GATE-4 的既定工具被本次派发的硬约束禁止、改以只读等价物核验。按 Pre-Status-Flip Gate"任一门禁红即不翻转",**Feature 052 状态保持 `Planned`,本轮未落 `Implemented`**;`.specify/memory/features/052.md` 与 `.specify/memory/features.md` 的 Status 与日期均未改动。解禁路径:待 053 落地 `plan.md`(或在其分支上)重跑 GATE-1 的 `comm -13` 得空,并解禁 `sync-mirrors.py --check` / `regen-command-copies.py --check` 后重跑 GATE-4 与 T058 的残留 2 项,再由 `/speckit.implement` 执行翻转。

deferred_tasks=(none) —— 2026-09-24 归零。前一轮登记的 T058 已改判 `[X]`(两项残留实跑且与制品所印相符,见 `notes/derived-command-audit.md` §12 N2/N3)。本特性现无任何 `[~]` 任务,故 Pre-Status-Flip Gate 第 1 步(转换延期任务)与第 4 步(延期登记)均无对象。
