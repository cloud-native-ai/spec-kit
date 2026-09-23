# Verification Log — 052-fast-fail-principle

feature=052-fast-fail-principle
feature_title=快速失败纪律(Fast Fail)
run_command=/speckit.implement
run_date=2026-09-23
run_outcome=partial-completion
tasks_total=63
tasks_closed=58
tasks_open=5
tasks_deferred=0

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
SC-007_note=quickstart 场景 8 实跑:`--workspace-root` 一次性根内 record → list 得 `count: 1`,真实存据按标记过滤仍为 `{"count": 0, "matches": []}`(反空真哨兵:证明隔离生效而非查询读空),`rm -rf` 后目录不存在。**partial 的理由**:SC-007 的后半("清单每次提升对应至少 1 条观察记录或 1 次可定位的用户纠正,留痕率 100%")在本轮**无样本**——两份清单自落地以来未发生过任何条目移动,故留痕率不可测,不能记为 100%。机制侧已由 `test_c18`(双向规则 + 留痕要求 + 禁止静默调参)守卫。
SC-007_unblock=待首次真实清单移动发生后,核对其留痕(反馈条目 ID / 提交号 / 会话原话之一)。

SC-008_status=deferred
SC-008_value=不可得
SC-008_note=读者测试要求**未参与本特性实现**的读者,对一份上送件样本在**不打开任何其他工件**的前提下从处置集中选出一项并说明理由。本轮的实现者即本会话,不满足独立性。
SC-008_deferred_reason=需要未参与实现的独立读者;单会话不可得。先例:Feature 051 的同类 SC 亦记 deferred。MUST NOT 以"四要素标题齐备"替代(SC-008 明文禁止该循环判定)。

SC-009_status=partial
SC-009_value=披露率 100%(本轮自身);干净运行显式陈述 不适用(本轮非干净运行)
SC-009_note=本轮全部顺手修复均在阶段报告与收尾报告中逐项披露(共 6 处修复 + 3 处自身断言缺陷 + 1 次演练残留清理),未出现未披露的就地修复;因披露而新增的打断次数为 0(合并在阶段报告中呈现)。**partial 的理由**:SC-009 的第三项"干净运行的显式陈述在场率 100%"在本轮无样本——本轮有异常也有修复,不属干净运行。该义务由 `test_c17`(STR-013 在场)与 quickstart 场景 12(`repairs=0 fails=0 -> True`;`repairs=2 -> False`;`fails=1 -> False`)守卫,即"只有干净运行需要该陈述"这一判据已被实跑验证。
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
SC-013_value=编排者侧 4/4 分类正确;子代理侧 4/4 回传携显式异常行
SC-013_note=**编排者侧**(可由演练取证):quickstart 场景 10 实跑四例分类为 `anomaly-halt / clean / incomplete / incomplete`——第四例"行内提及 `ANOMALY:`"正确落到 `incomplete` 而**非** `clean`,证明行首判据生效;`doc carries the rule: True`。**子代理侧**(不可由契约测试断言,因回传不落盘):本轮实际派发 4 个子代理(SC-001 两轮各 2 个),派发提示均要求行首 `ANOMALY:` 或 `未发现异常`,**4/4 回传携显式异常行**(首轮 A 1 条 / B 2 条,次轮 C 2 条 / D 2 条),无一行缺失,故未出现"缺行被判为干净"的情形。

SC-014_status=pass
SC-014_value=原样重派 0 次;异常停后续动作 1/1 为上送
SC-014_note=本轮唯一一次异常停是 FR-014 同一性键不可达(T013 的 SC-001 取样检出),其后续动作为**上送用户裁定**(四要素上送件 + 封闭处置集),用户选定甲案后按裁定级联落地为 T063。原样重派次数 **0**。`test_i21` 绿:真源文档点名排除既有的**全部**三条失败规则(两振停滞 / 连续两次派发失败即降级 / 非并行任务失败即停),quickstart 场景 11 实跑 `next action: surface-to-user | allowed: True | forbidden: False`。

SC-015_status=deferred
SC-015_value=不可得(无运营周期)
SC-015_note=三个数(快速失败率 / 用户推翻率 / 清单净生长方向)需要一段运营期的带标记反馈存据才能导出。本轮无该存据(真实存据按标记过滤为 `count: 0`)。
SC-015_deferred_reason=度量而非门禁:需累积一段时期的 `[fast-fail]` 标记条目。机制侧已就位——`test_c19` 断言三个数在真源文档中被载明、且声明由既有存据导出、MUST NOT 新增计数器或台账。**MUST NOT 编造数值**(STR-006 与真源文档的两条红线)。

# -- Gates (re-validated against the current tree, not trusted from the all-tasks-done state) --

GATE-1_status=pass
GATE-1_note=`comm -13 baseline current` 输出**为空**——零新增失败(最强形态,不再是"新增全在守卫内")。全量套件 **68 failed / 2797 passed / 2 skipped**;基线 76 条中治好 **8** 条(镜像字节相等类 4 条、按工具副本再生类 1 条、feedback 引用形态与路由类 3 条),76 − 8 = 68 与实测一致。守卫文件 `test_fast_fail_discipline.py` **105/105 全绿**,故不再向失败集贡献任何条目。
GATE-2_status=pass
GATE-2_note=直接比较形态实跑得 `frozen: 23 live: 23 violations: 0` + `TOTAL-EQUAL`;`head -1` 输出 `blocking confirmation gates: 23`。
GATE-3_status=pass
GATE-3_note=`git diff --stat <BASE_SHA> -- scripts/ src/specify_cli/ skills/create-team/scripts/ templates/plan-template.md` 输出为空。
GATE-4_status=pass
GATE-4_note=集合包含判据:shared 0 ⊆ 冻结 2;agents 0 = ok;templates 2 = 冻结 2;skills 36 ⊆ 冻结 38 且**零新增成员**(机械集合比较,非条数比较——条数一度同为 38 而成员已换手)。
GATE-5_status=pass
GATE-5_note=`test_fast_fail_discipline.py` **105 passed**;`test_constitution_double_landing.py` 19 passed;`test_user_facing_comprehension_doc.py` 23 passed;`test_user_facing_comprehension_section.py` / `test_instructions_section_propagation.py` / `test_proactive_trigger_section.py` 合计 37 passed;`test_confirmation_gates_sweep.py` 40 passed(实现期补入的第三处钉子)。
GATE-6_status=pass
GATE-6_note=`cmp shared/guidelines/fast-fail.md .specify/shared/guidelines/fast-fail.md` 静默 → BYTE-IDENTICAL。
GATE-7_status=fail
GATE-7_note=仍有 5 个任务为 `[ ]`(T058 的完整审计、T060、T061、T062 与 T054 的 SC-001 第三轮义务);故本项**不满足**,不得报为完成。
GATE-8_status=pass
GATE-8_note=本文件覆盖 SC-001…SC-015 全部 15 条,每条含 status / value / note 三字段;deferred 两条各附 `deferred_reason`。
GATE-9_status=pass
GATE-9_note=`validate-tasks.py` EXIT=0,0 error,1 warning(T014/T015 并行安全,已核实为误报并在 tasks.md Notes 说明理由:两行写入集不相交,均只把真源文档作为指针目标提及;消除该警告需删去路径引用,属为迁就校验器启发式而削弱制品精度,与 FR-064 同取向,故不取)。

# -- DoD --

DoD_status=partial
DoD_note=DoD-1…DoD-10 均可对当前树复核为真(真源文档 9 节填实且镜像字节相等;常驻章节位置与节数;宪章双落点与四钉;注入子句与全部副本;守卫与既有守卫全绿;门控中立;镜像相对判据;名字级回归;12 场景全部实跑;类 ⑪ 登记与四处留痕)。**DoD-11 未达成**(本文件已写成,但 SC-001/007/009 为 partial、SC-008/015 为 deferred,故 MUST NOT 报为全部达成);**DoD-12 部分达成**(派生命令审计已跑 19 项且零不符,但 tasks.md/plan.md/research.md/quickstart.md 中印出的命令未逐条穷尽复跑)。

# -- Run-level notes --

notes=本运行是 **partial run**:63 个任务闭合 58、开放 5,停在一个树洁净、门禁 GATE-1…GATE-6 与 GATE-8/GATE-9 全绿、GATE-7 因未闭合任务而为 fail 的检查点上。Feature 052 状态**仍为 `Planned`**——推进到 `Implemented` 归 Pre-Status-Flip Gate,而该门要求 Completion Gate 全绿,GATE-7 未过,故**本轮 MUST NOT 落 `Implemented`**。
notes_midrun_directive=2026-09-23 用户中途裁定(FR-014 同一性键拆为复发键与独立键)已按 Mid-Run User Directives 协议处理:上游 `requirements.md` 先改并把指令原文逐字追加进 `## Clarifications` › `### Session 2026-09-23`(append-only,行数 12 → 13 已核验),级联 `data-model.md` E2 / `contracts/discipline-doc.md` C-10(g) / 真源文档 / `test_c10`,新工作以**新任务号 T063** 追加而未重排既有 ID,并复跑双评审取证规则级一致率由 11/12 升至 12/12。
notes_upstream_defects=三条上游缺陷按 FR-077 如实上报、未顺手改写:① `Inherited premises` 悬空指针——存在于 `templates/instructions-template.md:41` 但不在活动的 `.specify/instructions.md`,而 10 个文件指向它;根因实测为 `generate-instructions.sh` 只做**整章节**增量注入,既有章节**内部**的新增永远传播不到已初始化项目(该机制同时正面印证本特性 D-1 取"新增顶级章节"的理由);② `scan-confirmation-gates.py --baseline` 的两个缺陷(键层级错位 + 退出码只反映 violations);③ `render_agents_for_tool` 对未知 tool 键**静默返回 `rendered: 0`**(`.github/agents` 的键是 `copilot` 而非 `github`)。另:活动指令文件中 Feature 051 的 `## User-Facing Comprehension` 节仍含"刷新指令即恢复镜像副本"的假承诺句式(实测命中行归属该节,本特性自己的章节区间命中数为 0),FR-077 明文规定该同类问题 MUST 单独上报而 MUST NOT 由本特性改写。
notes_self_defects=运行期查出的自身缺陷 9 处,其中 6 处顺手修复(各附变异演练或实跑取证)、1 处上送用户裁定、3 处属上游只上报。自身失误一次已修复并取证:变异演练的清理用了被 alias 成交互模式的 `cp` 且后接 `&& rm -f`,导致备份被删、演练文本残留在 `templates/commands/analyze.md`,已外科式移除并复核 `numstat = 2/0` 与其余七个文件一致。

deferred_tasks=(none — 本轮无 `[~]` 任务;5 个开放任务为 `[ ]`,属未完成而非已移交)
