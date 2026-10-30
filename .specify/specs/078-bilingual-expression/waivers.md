# 078 Checklist 豁免门裁决 — bilingual-convention-2026-10-30.md（35 条）

**裁决阶段**：implement Part 4（T019 checklist 豁免门；2026-10-30T12:10Z）
**裁决口径**：每条给 satisfied（由具名工件闭合）或 waiver（风险显式接受）；逐条 grounding 到唯一 owner 路径。
**前置事实**：analyze 指引 F-01/C-01…C-07 已于 Part 2/3 吸收进 owner 文档头部与相应章节（实测 grep 在场）。

## Requirement Completeness

- CHK001 satisfied — 覆盖判定完全由 FR-007 封闭集决定；封闭集之外显式不受约束（owner 文档 § 覆盖定义面「清单本身之外的面不受约束」），非 silently unconstrained。
- CHK002 satisfied — 无面归属的定义处的程序 = 经 owner 文档修订封闭集（owner 文档 § 覆盖定义面「封闭集增删只能经本文件修订」）。
- CHK003 satisfied — owner 文档 § 检查器与守卫 C-01 行：`--scope full` 输入规模（数十文件线性读取、亚秒至秒级）+ census 墙钟 >60s 重开条件（T-004）。
- CHK004 satisfied — owner 文档头部示范声明（C-02）：本文件自身定义行按登记逐字形态示范双语（声明：是）。
- CHK005 satisfied — owner 文档头部 Shared Strings 维护协议（C-03）：STR 字面量增改归 requirements.md 修订；消费点由契约测试漂移守卫核验。

## Requirement Clarity

- CHK006 satisfied — FR-002 以「被定义的位置」四例界定定义处（定义行/词汇表条目/首次定义/章节标题概念名）并显式排除每次提及；可判定信号清单按 FR-002 要求落在 owner 文档 S1…S4；quickstart S1 提供自足四步核对标本（notes/quickstart-run.md S1 实跑）。信号清单归 owner 文档是记录的架构决定，非缺口。
- CHK007 satisfied — ambient「一句话摘要」形态由契约测试钉死（小节内四组枚举关键词零命中 + [[STR-001]] 指针；T006/T012/T013/T018 多轮断言全过）。
- CHK008 satisfied — 无声明文档的主语言缺省信号（CJK/拉丁占比高者）成文于 owner 文档 S4，requirements Edge Cases 首条同向。
- CHK009 satisfied — owner 文档 C-04 行成文：段落级方向信号未登记，按文档级执行、无法判定时按段落各自语言执行方向规则（保守缺省成文，非悬置）。
- CHK010 satisfied — 「首次定义」语义判断显式置于机械范围之外（owner 文档 S 节「首次定义语义判断不在机械范围」），承载面记为评审面（FR-010 + review 抽样 us11）；是记录的边界决定。
- CHK011 satisfied — 「记为已知差异」的具名存储 = E6 存量差异清单（`test-evidence/us10-e6-legacy-divergence.txt`，dated record、append-only），消费方 = 各文档下次自然修订者（FR-016），owner 文档 § 迁移边界指针到位。

## Requirement Consistency

- CHK012 satisfied — owner 文档头部 seed 声明（F-01）：requirements 的 FR-004/FR-007 枚举是封闭集初始内容（seed），唯一 owner 归 owner 文档，requirements 复写不构成分叉。
- CHK013 satisfied — 同 F-01 seed 声明；迁移方向 = requirements(seed) → owner 文档（own），单一 owner 无分叉。
- CHK014 satisfied — 方向规则仅 [[STR-002]]/[[STR-003]] 两形态（plan § Measured Premises 与 clarify Session 裁定半角形态，实测无第三方向/宽度进入需求文本）。
- CHK015 satisfied — FR-013 与 jargon 白名单只指针（owner 文档 § 与相邻纪律的交界不重述成员资格）。
- CHK016 satisfied — STR-002/003 占位语义与消费方一致：形态常量逐字取自 owner 文档 C-005 唯一登记行（checker.md C-005），夹具/检查器按登记字面量消费，契约腿钉死。

## Measurability

- CHK017 satisfied — SC-002 分母操作化为 changed-path 信号行（plan 裁决 `--scope changed`；T010 实测 205 信号行、新写内容合规率 100%，22 findings 全分类为非新写内容）。
- CHK018 satisfied — plan T-004 裁决 100% census 不做抽样（重开条件 = 墙钟 >60s 实测）；T015 受控语料端到端验证。
- CHK019 satisfied — 关键词表程序派生自 owner 文档四组枚举（measurement C-001/C-002；us9 快照含 as-of 日期与可重放命令；T018 S7 复跑一致）。
- CHK020 satisfied — SC-003 判定标准逐字成文（小节标题逐字 / 枚举关键词零命中 / [[STR-001]] 指针），T013 pilot 实测 ≥1 次。
- CHK021 satisfied — SC-004 白名单封闭可枚举（tasks T014 六类；us14 审计 69 文件全数落白名单、白名单外修改行数 0）。
- CHK022 satisfied — 「误差 0 / 处数为 0」= 确定性程序的精确计数（检查器零抽样路径 + 逐字比对），仪器行为由契约测试钉死，无未定义误差项。

## Scenario & Edge Case Coverage

- CHK023 satisfied — 词汇表外表格单元格内的类定义内容：S1 信号锚定词汇表表体，其他表格行的定义形态在机械范围外（A7 边界成文），由评审面承担（us11 抽样管道已交付 review）。
- CHK024 satisfied — 自带括号第三方专名与形态检测器的碰撞输出形态成文（owner 文档豁免面 C-05 行：warning 级 finding 留评审裁定，不直接判红）。
- CHK025 satisfied — owner 文档范围声明（C-06）：只约束 zh/en 主语言文档，其他主语言文档不在封闭集内。
- CHK026 satisfied — 标题语言与文档主语言不一致时按 C-04 层级（声明优先 → 保守缺省），豁免面/方向规则不受标题单语影响。
- CHK027 satisfied — owner 文档 C-07 行：未知动作/缺参/路径不存在/文件不可读/owner 清单畸形/词汇表缺失一律退出码 2，不静默跳过（T018 S3b 实测 coverage --path rc=2）。
- CHK028 satisfied — 新信号的登记程序 = owner 文档修订（封闭集增删只能经本文件修订）；登记前 findings 归评审面（C-05 warning 形态 + us11 抽样），检查器不接线门禁（FR-010/T-003）。

## Dependencies & Assumptions

- CHK029 satisfied — 全部 deferral 具名决定阶段与义务：FR-010 退出码（plan/checker 契约）、FR-014 漂移守卫形态（T002 测试三腿）、SC-005 抽样比例（plan T-004 100% census），无无主的 deferral。
- CHK030 satisfied（I-01 处置）— A2/A4 重开条件的监控挂载：显式 inert-by-design + 具名触发器。A2（oracle 升级）触发器 = 每阶段派发的 flow-class-check 再基线（既有机制，requirements 期 re-baseline 已实测发生一次）；A4（用户明示全角优先）触发器 = 用户指令（无被动传感器可行，inert-by-design）；T-001…T-004 重开条件常驻 register.md（status=active），review 阶段 Decision Tensions 复核可见。本行即 I-01 的成文处置。
- CHK031 satisfied — STR 消费方封闭枚举由漂移守卫腿 (i) 白名单钉死（owner 文档 + ambient + 检查器常量三面），新增消费方 MUST 先改守卫（C-03）。
- CHK032 satisfied — glossary-utils 只读复用、行为零改动（T004/T015 复用实测；检查器以其文件位置加载不改其代码）。

## Ambiguities & Conflicts

- CHK033 satisfied — 「锚定语义」落到可观测面：SC-001 复制位置数 / SC-002 合规率 / SC-005 一致性处数，全部精确计数、可失败。
- CHK034 satisfied — 读者面有界：requirements 头部 **Readers** 行（clarify G-clarify-reader 修复）+ owner 文档复用全局基准读者，跨 context 声明不越出该基线。
- CHK035 satisfied — 「自然修订」的操作触发 = 文档的任意编辑即进入下次 changed-scope 分母（SC-002 每交付里程碑实测）；收敛时点在 E6 清单可逐文件核对，不可无限期悬置（FR-016 + us10）。

## 统计

satisfied = 35；waiver = 0。无条目需要以 waiver 消音——35 条全部可由具名工件闭合（多数经 analyze 指引 F-01/C-01…C-07 在 owner 文档成文后闭合）。
